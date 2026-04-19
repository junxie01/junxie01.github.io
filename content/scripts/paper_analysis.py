#!/usr/bin/env python3
"""
paper-analysis — Analyze a research paper and generate a blog post.

Usage:
    python3 paper_analysis.py <pdf_file_or_url>
    python3 paper_analysis.py paper.pdf
    python3 paper_analysis.py https://arxiv.org/abs/2401.12345

Requires:
    pip3 install PyPDF2 PyMuPDF requests
    export GEMINI_API_KEY="your-key-here"   # https://aistudio.google.com/apikey
"""

import os
import sys
import re
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# --- Configuration ---
# Priority: GROQ (fast & free) > GEMINI > fallback error
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_MAX_INPUT_CHARS = 15000  # ~4k tokens for prompt, rest for paper (12k TPM limit)

GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

PROJECT_ROOT = Path(__file__).resolve().parent
POSTS_DIR = PROJECT_ROOT / "content" / "posts"
IMAGES_DIR = PROJECT_ROOT / "content" / "images"

MIN_IMAGE_SIZE = 5000  # Skip tiny images (icons, logos) under 5KB
MIN_IMAGE_DIM = 100    # Skip images smaller than 100px in either dimension

ANALYSIS_PROMPT = """You are an expert academic paper analyst. Analyze the given paper and write a structured analysis in the EXACT format below. Fill in every section. Write in a mix of Chinese and English as appropriate for a Chinese researcher's blog.

Use this EXACT format (keep all the headings exactly as shown):

## Paper Information

- **Title**: [Full paper title]
- **First Author**: [Name]
- **Corresponding Author**: [Name]
- **Affiliation**: [Institution]
- **Journal**: [Journal, Year, Volume, Pages]
- **DOI**: [DOI]

## Author Background

### First Author's Representative Works
1. [Citation 1]
2. [Citation 2]
3. [Citation 3]

## Abstract (Translated)

[Translate the abstract into Chinese]

## Research Context

### Importance
[Why this research matters - 2-3 paragraphs, in Chinese]

### Previous Studies
- **[Author et al. (Year)]**: [What they did and found]. *Journal Name, Volume, Pages.*
- **[Author et al. (Year)]**: [What they did and found]. *Journal Name, Volume, Pages.*
- **[Author et al. (Year)]**: [What they did and found]. *Journal Name, Volume, Pages.*
- **[Author et al. (Year)]**: [What they did and found]. *Journal Name, Volume, Pages.*
- **[Author et al. (Year)]**: [What they did and found]. *Journal Name, Volume, Pages.*

(List at least 5 key prior studies mentioned in the paper with full citations)

### Limitations of Previous Research
[Gaps before this paper, in Chinese]

## Methodology

### Data
[Datasets used, time period, spatial coverage]

### Methods
[Technical approaches, algorithms, models]

## Results

[Key findings, in Chinese]

## Discussion

### Innovations
[What is new about this work]

### Contributions
[How this advances the field]

### Limitations
[Acknowledged weaknesses or future work]

## Personal Thoughts

*[留待补充]*

Now analyze the paper below. Remember: use the EXACT heading format shown above."""

SLUG_PROMPT = ""  # unused, slug generated locally now


def select_best_figures(images, max_count=3):
    """Pick the 3 most representative figures: first, best middle, last."""
    if not images:
        return []
    if len(images) <= max_count:
        return images

    first = images[0]
    last = images[-1]

    # Pick the "best" middle figure: largest by pixel area (likely a key result figure)
    middle_candidates = images[1:-1]
    best_middle = max(middle_candidates, key=lambda img: img["width"] * img["height"])

    return [first, best_middle, last]


def extract_images_from_pdf(pdf_path, output_dir):
    """Extract images from a PDF file using PyMuPDF."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("  [WARN] PyMuPDF not installed. Skipping image extraction.")
        print("         Install with: pip3 install PyMuPDF")
        return []

    doc = fitz.open(pdf_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    images = []
    img_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)

        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
            except Exception:
                continue

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            width = base_image.get("width", 0)
            height = base_image.get("height", 0)

            # Skip tiny images (icons, decorations)
            if len(image_bytes) < MIN_IMAGE_SIZE:
                continue
            if width < MIN_IMAGE_DIM or height < MIN_IMAGE_DIM:
                continue

            img_count += 1
            filename = f"figure{img_count}.{image_ext}"
            img_path = output_dir / filename
            img_path.write_bytes(image_bytes)
            images.append({
                "filename": filename,
                "fig_num": img_count,
                "page": page_num + 1,
                "width": width,
                "height": height,
                "size_kb": len(image_bytes) // 1024,
            })

    doc.close()
    return images


def extract_figure_captions(pdf_path):
    """Extract figure captions from the PDF text."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        return {}

    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            full_text += t + "\n"

    # Match patterns like "Figure 1.", "Fig. 1.", "Figure 1:", "FIGURE 1."
    captions = {}
    pattern = r'(?:Figure|Fig\.?)\s*(\d+)[.:\s]\s*([^\n]{10,300})'
    for match in re.finditer(pattern, full_text, re.IGNORECASE):
        fig_num = int(match.group(1))
        caption_text = match.group(2).strip()
        # Take first sentence if very long
        if len(caption_text) > 200:
            caption_text = caption_text[:200].rsplit('.', 1)[0] + '.'
        captions[fig_num] = caption_text

    return captions


def translate_captions(captions):
    """Translate figure captions to Chinese using AI."""
    if not captions:
        return {}

    caption_list = "\n".join(f"Figure {n}: {text}" for n, text in sorted(captions.items()))
    prompt = f"""Translate these figure captions to Chinese. Return ONLY the translations, one per line, in the format "Figure N: 中文翻译". Keep figure numbers unchanged.

{caption_list}"""

    try:
        result = call_ai(prompt, timeout=30)
        translated = {}
        for line in result.strip().split("\n"):
            m = re.match(r'Figure\s*(\d+)[:\s]\s*(.+)', line, re.IGNORECASE)
            if m:
                translated[int(m.group(1))] = m.group(2).strip()
        return translated
    except Exception:
        return captions  # Fallback to English captions


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("Error: PyPDF2 not installed. Run: pip3 install PyPDF2")
        sys.exit(1)

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def fetch_arxiv_text(url):
    """Fetch paper text from an arXiv URL."""
    import urllib.request

    # Convert abstract URL to PDF URL
    if "abs" in url:
        pdf_url = url.replace("/abs/", "/pdf/") + ".pdf"
    elif "pdf" not in url:
        pdf_url = url + ".pdf"
    else:
        pdf_url = url

    tmp_path = "/tmp/paper_analysis_tmp.pdf"
    print(f"  Downloading PDF from {pdf_url}...")
    urllib.request.urlretrieve(pdf_url, tmp_path)
    return tmp_path, extract_text_from_pdf(tmp_path)


def get_paper_text(source):
    """Get paper text from a file path or URL. Returns (pdf_path, text)."""
    if source.startswith("http"):
        if "arxiv" in source:
            return fetch_arxiv_text(source)
        else:
            print("Error: Only arXiv URLs and local PDF files are supported.")
            sys.exit(1)
    else:
        path = Path(source)
        if not path.exists():
            print(f"Error: File not found: {source}")
            sys.exit(1)
        if path.suffix.lower() == ".pdf":
            return str(path), extract_text_from_pdf(path)
        else:
            return None, path.read_text(encoding="utf-8")


def call_groq(prompt, timeout=120):
    """Call Groq API (free, fast)."""
    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": "You are an expert academic paper analyst."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 4096,
            },
            timeout=timeout,
        )
        if response.status_code == 429:
            wait = 60
            print(f"  Rate limited. Waiting {wait}s...")
            time.sleep(wait)
            response = requests.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": "You are an expert academic paper analyst."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4096,
                },
                timeout=timeout,
            )
        response.raise_for_status()
    except requests.ConnectionError:
        print("Error: Cannot connect to Groq API. Check your network.")
        sys.exit(1)
    except requests.HTTPError as e:
        print(f"Error: Groq API returned {e.response.status_code}")
        print(f"  {e.response.text[:300]}")
        sys.exit(1)

    return response.json()["choices"][0]["message"]["content"].strip()


def call_gemini(prompt, timeout=120, max_retries=3):
    """Call Google Gemini API with automatic retry on rate limits."""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set.")
        print("  1. Get a free key at: https://aistudio.google.com/apikey")
        print("  2. export GEMINI_API_KEY='your-key-here'")
        print("  3. (Optional) Add to ~/.zshrc for persistence")
        sys.exit(1)

    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 8192,
                    },
                },
                timeout=timeout,
            )
            if response.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited. Waiting {wait}s before retry ({attempt+1}/{max_retries})...")
                time.sleep(wait)
                continue
            response.raise_for_status()
            break
        except requests.ConnectionError:
            print("Error: Cannot connect to Gemini API. Check your network.")
            sys.exit(1)
        except requests.Timeout:
            print("Error: Gemini API timed out. Try again.")
            sys.exit(1)
        except requests.HTTPError as e:
            error_body = e.response.text[:300] if e.response else str(e)
            print(f"Error: Gemini API returned {e.response.status_code}")
            print(f"  {error_body}")
            sys.exit(1)
    else:
        print("Error: Still rate limited after retries. Wait a minute and try again.")
        sys.exit(1)

    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        print("Error: Unexpected Gemini response format.")
        print(json.dumps(data, indent=2)[:500])
        sys.exit(1)


def call_ai(prompt, timeout=120):
    """Call the best available AI API."""
    if GROQ_API_KEY:
        print(f"  Using Groq ({GROQ_MODEL})...")
        return call_groq(prompt, timeout)
    elif GEMINI_API_KEY:
        print(f"  Using Gemini ({GEMINI_MODEL})...")
        return call_gemini(prompt, timeout)
    else:
        print("Error: No API key set. Set one of:")
        print("  export GROQ_API_KEY='your-key'    # https://console.groq.com (recommended)")
        print("  export GEMINI_API_KEY='your-key'   # https://aistudio.google.com/apikey")
        sys.exit(1)


def analyze_paper(paper_text):
    """Get structured analysis from AI."""
    # Truncate based on backend
    if GROQ_API_KEY:
        max_chars = GROQ_MAX_INPUT_CHARS
        print(f"  (Groq free tier: truncating to ~{max_chars//1000}k chars)")
    else:
        max_chars = 200000  # Gemini supports 1M tokens

    if len(paper_text) > max_chars:
        paper_text = paper_text[:max_chars] + "\n\n[... truncated ...]"

    print(f"  Calling AI for analysis...")

    prompt = ANALYSIS_PROMPT + "\n\n" + paper_text
    analysis = call_ai(prompt)

    return analysis


def extract_title(analysis):
    """Extract title from the analysis text."""
    match = re.search(r'\*\*Title\*\*:\s*(.+)', analysis)
    if match:
        return match.group(1).strip()
    # Fallback: first line after ## Paper Information
    match = re.search(r'##\s*Paper Information\s*\n(.*)', analysis)
    if match:
        return match.group(1).strip()
    return "Paper Analysis"


def get_slug(title):
    """Generate a filename slug from the title locally (no API call)."""
    # Remove non-ascii, lowercase, split into words
    ascii_title = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    words = ascii_title.lower().split()
    # Pick first 3-4 meaningful words (skip short ones)
    stop_words = {'a', 'an', 'the', 'of', 'in', 'on', 'for', 'and', 'to', 'by', 'with', 'from', 'is', 'at', 'its'}
    keywords = [w for w in words if w not in stop_words and len(w) > 2][:4]
    slug = '-'.join(keywords) if keywords else 'paper-reading'
    return slug


def get_next_paper_number():
    """Find the next Paper Reading number by scanning existing posts."""
    max_num = 0
    for f in POSTS_DIR.glob("*paper-read*.md"):
        match = re.search(r'paper-read(?:ing)?-(\d+)', f.stem)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    return max_num + 1


def generate_markdown(analysis, title, tags, images=None, slug="", captions=None, reading_num=1):
    """Wrap the analysis in a blog post with frontmatter, figures inserted inline."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Insert figures at appropriate positions in the analysis
    if images and len(images) >= 1:
        img_tags = []
        for i, img in enumerate(images):
            fig_num = img.get("fig_num", i+1)
            cap_text = ""
            if captions:
                cap_text = captions.get(fig_num, "")
            prefix = f"\u56fe{fig_num} "
            full_cap = prefix + cap_text if cap_text else prefix.strip()
            img_tags.append(f"\n\n![{full_cap}](/images/paper-{slug}/{img['filename']})\n\n<center><em>{full_cap}</em></center>\n")

        # Figure 1 → after Research Context (before ## Methodology)
        # Figure 2 → after Methodology (before ## Results)
        # Figure 3 → after Results (before ## Discussion)
        insert_points = [
            (r'(## Methodology)', img_tags[0] + '\n\1'),
        ]
        if len(images) >= 2:
            insert_points.append(
                (r'(## Results)', img_tags[1] + '\n\1'),
            )
        if len(images) >= 3:
            insert_points.append(
                (r'(## Discussion)', img_tags[2] + '\n\1'),
            )

        for pattern, replacement in insert_points:
            analysis = re.sub(pattern, replacement, analysis, count=1)

    post_title = f"Paper Reading ({reading_num})"

    md = f"""---
title: "{post_title}"
date: {today}
tags: [{tags}]
excerpt: "{title}"
---

{analysis}
"""
    return md, today, reading_num


def guess_tags(analysis):
    """Guess appropriate tags from the analysis content."""
    tag_keywords = {
        "seismology": ["seism", "earthquake", "seismic"],
        "geophysics": ["geophys", "mantle", "crust"],
        "ocean": ["ocean", "swell", "marine", "microseism"],
        "tomography": ["tomograph"],
        "machine-learning": ["machine learning", "deep learning", "neural"],
        "ambient-noise": ["ambient noise", "cross-correlation"],
        "DAS": ["DAS", "distributed acoustic"],
        "GPS": ["GPS", "GNSS", "geodetic"],
        "InSAR": ["InSAR", "interferom"],
        "glaciology": ["glacier", "ice sheet", "glacial"],
    }
    lower = analysis.lower()
    tags = ["paper"]
    for tag, keywords in tag_keywords.items():
        if any(kw.lower() in lower for kw in keywords):
            tags.append(tag)
    # Cap at 5 tags
    return ", ".join(tags[:5])


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 paper_analysis.py <pdf_file_or_url>")
        print("Examples:")
        print("  python3 paper_analysis.py paper.pdf")
        print("  python3 paper_analysis.py https://arxiv.org/abs/2401.12345")
        sys.exit(1)

    source = sys.argv[1]
    print(f"\n{'='*50}")
    backend = "Groq" if GROQ_API_KEY else "Gemini"
    print(f"  Paper Analysis — {backend}")
    print(f"{'='*50}\n")

    # Step 1: Extract text and images
    print("[1/5] Extracting paper text...")
    pdf_path, paper_text = get_paper_text(source)
    word_count = len(paper_text.split())
    print(f"  Extracted ~{word_count} words")

    # Step 2: AI analysis (natural language — no JSON!)
    print("[2/5] Analyzing with AI...")
    analysis = analyze_paper(paper_text)
    print(f"  Analysis complete ({len(analysis)} chars)")

    # Step 3: Extract metadata
    print("[3/5] Extracting metadata...")
    title = extract_title(analysis)
    tags = guess_tags(analysis)
    slug = get_slug(title)

    # Step 4: Extract images from PDF
    images = []
    captions_zh = {}
    if pdf_path:
        print("[4/5] Extracting images from PDF...")
        img_output_dir = IMAGES_DIR / f"paper-{slug}"
        images = extract_images_from_pdf(pdf_path, img_output_dir)
        if images:
            print(f"  Found {len(images)} figure(s), selecting best 3...")
            images = select_best_figures(images, max_count=3)
            print(f"  Selected {len(images)} key figure(s)")
            # Clean up unselected images
            selected_files = {img["filename"] for img in images}
            for f in img_output_dir.iterdir():
                if f.name not in selected_files:
                    f.unlink()

            # Extract and translate captions
            print("  Extracting figure captions...")
            raw_captions = extract_figure_captions(pdf_path)
            if raw_captions:
                print(f"  Found {len(raw_captions)} caption(s), translating...")
                captions_zh = translate_captions(raw_captions)
            else:
                print("  No captions found in text.")
        else:
            print("  No significant figures found in PDF.")
    else:
        print("[4/5] No PDF — skipping image extraction.")

    # Step 5: Generate and save
    print("[5/5] Generating blog post...")
    reading_num = get_next_paper_number()
    md_content, today, reading_num = generate_markdown(analysis, title, tags, images, slug, captions_zh, reading_num)

    # Save file
    filename = f"{today}-paper-reading-{reading_num}.md"
    output_path = POSTS_DIR / filename
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md_content, encoding="utf-8")

    print(f"  Saved to: {output_path.relative_to(PROJECT_ROOT)}")
    print(f"\n  Title: Paper Reading ({reading_num})")
    print(f"  Paper: {title}")
    print(f"  Tags:  {tags}")
    if images:
        print(f"  Figs:  {len(images)} figures in content/images/paper-{slug}/")
    print(f"\n  Next: review the post, then run 'python3 build.py' to publish.")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
