#!/usr/bin/env python3
"""
SEISAMUSE — Static Site Builder
Converts Markdown content into a clean academic website.

Usage:
    python build.py          # Build the entire site
    python build.py serve    # Build and start local preview server
"""

import os
import sys
import math
import shutil
import json
import re
import html
from datetime import date, datetime
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor

# --- Configuration ---
BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
POSTS_DIR = CONTENT_DIR / "posts"
THOUGHTS_DIR = CONTENT_DIR / "thoughts"
TEMPLATES_DIR = BASE_DIR / "templates"

# Direct deployment: output to docs/ directory for GitHub Pages
SUBDIR = ""
SITE_DIR = BASE_DIR / "site"

SITE_NAME = "SEISAMUSE"
AUTHOR = "Jun Xie"
SITE_URL = "https://www.seis-jun.xyz"
SITE_DESCRIPTION = "Personal academic website of Jun Xie — Seismologist and Geophysicist"
RECENT_POSTS_COUNT = 5
RECENT_THOUGHTS_COUNT = 3
POSTS_PER_PAGE = 15
SITE_START_DATE = date(2020, 5, 26)

# Markdown extensions for richer rendering
MD_EXTENSIONS = [
    "extra",        # tables, fenced code, footnotes, etc.
    "codehilite",   # syntax highlighting
    "toc",          # table of contents
    "meta",         # metadata
    "smarty",       # smart quotes
]

MD_EXTENSION_CONFIGS = {
    "codehilite": {"css_class": "highlight", "linenums": False},
}

MORE_MARKER_RE = re.compile(r"<!--\s*(?:less|more)\s*-->", re.I)
FENCED_CODE_RE = re.compile(r"```.*?```", re.S)


class StrikethroughExtension(Extension):
    """Support GitHub-style ~~strikethrough~~ text."""

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            SimpleTagInlineProcessor(r"()~~(.*?)~~", "del"),
            "strikethrough",
            175,
        )


def get_jinja_env():
    """Create Jinja2 template environment."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,  # We trust our own HTML
    )
    return env


def render_markdown(text):
    """Convert Markdown text to HTML."""
    md = markdown.Markdown(
        extensions=[*MD_EXTENSIONS, StrikethroughExtension()],
        extension_configs=MD_EXTENSION_CONFIGS,
    )
    html = md.convert(text)
    md.reset()
    return html


def estimate_reading_time(text):
    """Estimate reading time in minutes (avg 200 words/min for academic text)."""
    word_count = len(text.split())
    return max(1, math.ceil(word_count / 200))


def clean_search_text(text):
    """Convert Markdown-ish source into compact plain text for search."""
    if not text:
        return ""
    text = html.unescape(str(text))
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\{%\s*asset_img\s+.*?%\}", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#>*_~`]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def truncate_text(text, limit=160):
    """Trim plain text without breaking Markdown syntax."""
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def count_text_units(text):
    """Count CJK characters and Latin words for a compact site word count."""
    text = clean_search_text(text)
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    text_without_cjk = re.sub(r"[\u4e00-\u9fff]", " ", text)
    word_count = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text_without_cjk))
    return cjk_count + word_count


def format_compact_number(value):
    """Format large counters for the sidebar."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M".replace(".0M", "M")
    if value >= 1_000:
        return f"{value / 1_000:.1f}k".replace(".0k", "k")
    return str(value)


def make_auto_excerpt(first_para, limit=160):
    """Create a safe excerpt from source Markdown.

    If the first paragraph is short as visible text, render it whole so links
    survive. If it is too long, fall back to escaped plain text instead of
    truncating raw Markdown in the middle of a link or image.
    """
    excerpt_text = clean_search_text(first_para)
    if FENCED_CODE_RE.search(first_para) or "```" in first_para:
        excerpt_text = truncate_text(excerpt_text, limit)
        return f"<p>{html.escape(excerpt_text)}</p>" if excerpt_text else "", excerpt_text

    if len(excerpt_text) <= limit:
        return render_markdown(first_para), excerpt_text

    excerpt_text = truncate_text(excerpt_text, limit)
    return f"<p>{html.escape(excerpt_text)}</p>", excerpt_text


def get_auto_excerpt_source(content):
    """Use an explicit summary marker before falling back to the first block."""
    content = content.strip()
    if not content:
        return ""

    before_marker = MORE_MARKER_RE.split(content, maxsplit=1)[0].strip()
    if before_marker:
        return before_marker

    return content.split("\n\n", 1)[0].strip()


def extract_toc(content_html):
    """Extract table of contents from HTML content and add anchor IDs to headings."""
    toc = []
    heading_re = re.compile(r'<h([123])([^>]*)>(.*?)</h\1>')

    def replace_heading(match):
        level = match.group(1)
        attrs = match.group(2)
        text_html = match.group(3)
        # Extract plain text (remove any nested HTML tags)
        text = re.sub(r'<[^>]+>', '', text_html)
        if not text.strip():
            return match.group(0)

        # Check if heading already has an id
        existing_id = None
        id_match = re.search(r'id=["\']([^"\']+)["\']', attrs)
        if id_match:
            existing_id = id_match.group(1)

        if existing_id:
            # Use existing id for TOC
            toc.append({
                "level": int(level),
                "text": text.strip(),
                "id": existing_id,
            })
            return match.group(0)

        # Create anchor ID from text (keep CJK, Latin, digits, and common punctuation)
        anchor = re.sub(r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffefa-zA-Z0-9\s-]', '', text.lower())
        anchor = re.sub(r'[\s]+', '-', anchor)
        anchor = anchor.strip('-')
        if not anchor:
            anchor = f"heading-{len(toc)}"

        # Ensure uniqueness
        base_anchor = anchor
        counter = 1
        while any(item["id"] == anchor for item in toc):
            anchor = f"{base_anchor}-{counter}"
            counter += 1

        toc.append({
            "level": int(level),
            "text": text.strip(),
            "id": anchor,
        })

        return f'<h{level}{attrs} id="{anchor}">{text_html}</h{level}>'

    content_html = heading_re.sub(replace_heading, content_html)
    return toc, content_html


def sanitize_for_xml(text):
    """Sanitize text for safe inclusion in XML, handling CDATA breaks and invalid characters."""
    if not text:
        return ""
    text = str(text)
    # Replace ]]> with ]]&gt; to prevent breaking CDATA sections
    text = text.replace(']]>', ']]&gt;')
    # Remove invalid XML control characters (except \t, \n, \r)
    # Valid XML chars: #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
    import re
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    # Replace common HTML entities with their Unicode characters or numeric references
    # XML only supports &lt; &gt; &amp; &apos; &quot; - all others must be converted
    html_entities = {
        '&nbsp;': '&#160;', '&ensp;': '&#8194;', '&emsp;': '&#8195;',
        '&thinsp;': '&#8201;', '&zwnj;': '&#8204;', '&zwj;': '&#8205;',
        '&lrm;': '&#8206;', '&rlm;': '&#8207;', '&shy;': '&#173;',
        '&ndash;': '&#8211;', '&mdash;': '&#8212;', '&lsquo;': '&#8216;',
        '&rsquo;': '&#8217;', '&sbquo;': '&#8218;', '&ldquo;': '&#8220;',
        '&rdquo;': '&#8221;', '&bdquo;': '&#8222;', '&dagger;': '&#8224;',
        '&Dagger;': '&#8225;', '&bull;': '&#8226;', '&hellip;': '&#8230;',
        '&permil;': '&#8240;', '&prime;': '&#8242;', '&Prime;': '&#8243;',
        '&lsaquo;': '&#8249;', '&rsaquo;': '&#8250;', '&oline;': '&#8254;',
        '&euro;': '&#8364;', '&trade;': '&#8482;',
        '&laquo;': '&#171;', '&raquo;': '&#187;',
        '&iexcl;': '&#161;', '&cent;': '&#162;', '&pound;': '&#163;',
        '&curren;': '&#164;', '&yen;': '&#165;', '&brvbar;': '&#166;',
        '&sect;': '&#167;', '&uml;': '&#168;', '&copy;': '&#169;',
        '&ordf;': '&#170;', '&not;': '&#172;', '&reg;': '&#174;',
        '&macr;': '&#175;', '&deg;': '&#176;', '&plusmn;': '&#177;',
        '&sup2;': '&#178;', '&sup3;': '&#179;', '&acute;': '&#180;',
        '&micro;': '&#181;', '&para;': '&#182;', '&middot;': '&#183;',
        '&cedil;': '&#184;', '&sup1;': '&#185;', '&ordm;': '&#186;',
        '&frac14;': '&#188;', '&frac12;': '&#189;', '&frac34;': '&#190;',
        '&iquest;': '&#191;', '&times;': '&#215;', '&divide;': '&#247;',
        '&Agrave;': '&#192;', '&Aacute;': '&#193;', '&Acirc;': '&#194;',
        '&Atilde;': '&#195;', '&Auml;': '&#196;', '&Aring;': '&#197;',
        '&AElig;': '&#198;', '&Ccedil;': '&#199;', '&Egrave;': '&#200;',
        '&Eacute;': '&#201;', '&Ecirc;': '&#202;', '&Euml;': '&#203;',
        '&Igrave;': '&#204;', '&Iacute;': '&#205;', '&Icirc;': '&#206;',
        '&Iuml;': '&#207;', '&ETH;': '&#208;', '&Ntilde;': '&#209;',
        '&Ograve;': '&#210;', '&Oacute;': '&#211;', '&Ocirc;': '&#212;',
        '&Otilde;': '&#213;', '&Ouml;': '&#214;', '&Oslash;': '&#216;',
        '&Ugrave;': '&#217;', '&Uacute;': '&#218;', '&Ucirc;': '&#219;',
        '&Uuml;': '&#220;', '&Yacute;': '&#221;', '&THORN;': '&#222;',
        '&szlig;': '&#223;', '&agrave;': '&#224;', '&aacute;': '&#225;',
        '&acirc;': '&#226;', '&atilde;': '&#227;', '&auml;': '&#228;',
        '&aring;': '&#229;', '&aelig;': '&#230;', '&ccedil;': '&#231;',
        '&egrave;': '&#232;', '&eacute;': '&#233;', '&ecirc;': '&#234;',
        '&euml;': '&#235;', '&igrave;': '&#236;', '&iacute;': '&#237;',
        '&icirc;': '&#238;', '&iuml;': '&#239;', '&eth;': '&#240;',
        '&ntilde;': '&#241;', '&ograve;': '&#242;', '&oacute;': '&#243;',
        '&ocirc;': '&#244;', '&otilde;': '&#245;', '&ouml;': '&#246;',
        '&oslash;': '&#248;', '&ugrave;': '&#249;', '&uacute;': '&#250;',
        '&ucirc;': '&#251;', '&uuml;': '&#252;', '&yacute;': '&#253;',
        '&thorn;': '&#254;', '&yuml;': '&#255;',
    }
    for entity, replacement in html_entities.items():
        text = text.replace(entity, replacement)
    return text


def parse_post_date(date_raw):
    """Return display date and full datetime sort key for a post."""
    if isinstance(date_raw, datetime):
        parsed = date_raw
        return parsed.strftime("%Y-%m-%d"), parsed.strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(date_raw, date):
        parsed = datetime.combine(date_raw, datetime.min.time())
        return parsed.strftime("%Y-%m-%d"), parsed.strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(date_raw, str):
        value = date_raw.strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                parsed = datetime.strptime(value, fmt)
                return parsed.strftime("%Y-%m-%d"), parsed.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass

        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return parsed.strftime("%Y-%m-%d"), parsed.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass

        if re.match(r"^\d{4}-\d{2}-\d{2}", value):
            date_str = value[:10]
            return date_str, f"{date_str} 00:00:00"

    return "undated", "0000-00-00 00:00:00"


def load_post(filepath):
    """Load a single Markdown post with frontmatter."""
    post = frontmatter.load(filepath)

    # Extract metadata
    title = str(post.get("title") or filepath.stem.replace("-", " ").title())
    date_raw = post.get("date", None)

    date_str, date_sort = parse_post_date(date_raw)

    tags = post.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    tags = [str(t).strip() for t in tags if str(t).strip()]

    excerpt_source = post.get("excerpt", post.get("description", ""))
    excerpt_text = clean_search_text(excerpt_source)
    excerpt_html = render_markdown(excerpt_source) if excerpt_source else ""
    if not excerpt_source and len(post.content) > 0:
        # Auto-generate excerpt from first paragraph without breaking links.
        first_para = get_auto_excerpt_source(post.content)
        excerpt_html, excerpt_text = make_auto_excerpt(first_para)

    slug = post.get("slug", filepath.stem)
    content_html = render_markdown(post.content)
    toc, content_html = extract_toc(content_html)
    reading_time = estimate_reading_time(post.content)

    # Check for post asset folder (Hexo-style: same name as .md file)
    asset_dir = filepath.parent / filepath.stem
    has_assets = asset_dir.is_dir()

    # Process Hexo asset_img tags: {% asset_img filename alt_text %}
    # These images are in the post's asset folder (if it exists) or global images/ folder
    import re
    if has_assets:
        # Replace {% asset_img filename alt_text %} with <img src="/blog/assets/<slug>/filename">
        content_html = re.sub(
            r'\{%\s*asset_img\s+(\S+)\s*(.*?)\s*%\}',
            f'<img src="/blog/assets/{slug}/\\1" alt="\\2">',
            content_html,
        )
        # Also rewrite relative markdown image paths to point to blog assets folder
        content_html = re.sub(
            r'src="(?!http|/|data:)([^"]+)"',
            f'src="/blog/assets/{slug}/\\1"',
            content_html,
        )
        # Also fix absolute /images/ paths from markdown rendering
        content_html = re.sub(
            r'src="/images/',
            'src="/images/',
            content_html,
        )
    else:
        # No asset folder exists, replace asset_img with global images path
        content_html = re.sub(
            r'\{%\s*asset_img\s+(\S+)\s*(.*?)\s*%\}',
            f'<img src="/images/\\1" alt="\\2">',
            content_html,
        )
        # Also fix absolute /images/ paths from markdown rendering
        content_html = re.sub(
            r'src="/images/',
            'src="/images/',
            content_html,
        )

    return {
        "title": title,
        "date": date_str,
        "date_sort": date_sort,
        "tags": tags,
        "excerpt": excerpt_html,
        "excerpt_text": excerpt_text,
        "slug": slug,
        "content": content_html,
        "toc": toc,
        "search_text": clean_search_text(post.content),
        "reading_time": reading_time,
        "source_path": filepath,
        "has_assets": has_assets,
    }


def load_all_posts():
    """Load all posts from the content/posts directory."""
    posts = []
    if not POSTS_DIR.exists():
        return posts

    for filepath in POSTS_DIR.glob("*.md"):
        try:
            post = load_post(filepath)
            posts.append(post)
        except Exception as e:
            print(f"  [WARN] Skipping {filepath.name}: {e}")

    # Sort by date, newest first
    posts.sort(key=lambda p: p["date_sort"], reverse=True)
    return posts


def parse_thought_datetime(date_raw, filepath):
    """Parse thought datetime from frontmatter, falling back to filename."""
    parsed = None

    if isinstance(date_raw, datetime):
        parsed = date_raw
    elif isinstance(date_raw, date):
        parsed = datetime.combine(date_raw, datetime.min.time())
    elif isinstance(date_raw, str):
        value = date_raw.strip()
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d",
        ):
            try:
                parsed = datetime.strptime(value, fmt)
                break
            except ValueError:
                continue

    if parsed is None:
        match = re.match(r"(\d{4}-\d{2}-\d{2})(?:[-_ ]?(\d{2})(\d{2})(?:\d{2})?)?", filepath.stem)
        if match:
            date_part = match.group(1)
            hour = match.group(2) or "00"
            minute = match.group(3) or "00"
            parsed = datetime.strptime(f"{date_part} {hour}:{minute}", "%Y-%m-%d %H:%M")

    if parsed is None:
        parsed = datetime(1970, 1, 1)

    return parsed


def load_thought(filepath):
    """Load a short thought from content/thoughts."""
    thought = frontmatter.load(filepath)
    thought_dt = parse_thought_datetime(thought.get("date"), filepath)

    tags = thought.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    tags = [str(t).strip() for t in tags if str(t).strip()]

    content_source = thought.content.strip()
    content_html = render_markdown(content_source) if content_source else ""
    inline_match = re.fullmatch(r"\s*<p>(.*?)</p>\s*", content_html, re.S)
    content_inline = inline_match.group(1) if inline_match else ""
    slug = str(thought.get("slug") or filepath.stem)

    return {
        "slug": slug,
        "date": thought_dt.strftime("%Y-%m-%d"),
        "time": thought_dt.strftime("%H:%M"),
        "datetime": thought_dt.strftime("%Y-%m-%d %H:%M"),
        "date_sort": thought_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "tags": tags,
        "content": content_html,
        "content_inline": content_inline,
        "excerpt_text": clean_search_text(content_source),
        "source_path": filepath,
    }


def load_all_thoughts():
    """Load all thoughts from the content/thoughts directory."""
    thoughts = []
    if not THOUGHTS_DIR.exists():
        return thoughts

    for filepath in THOUGHTS_DIR.glob("*.md"):
        try:
            thoughts.append(load_thought(filepath))
        except Exception as e:
            print(f"  [WARN] Skipping thought {filepath.name}: {e}")

    thoughts.sort(key=lambda item: item["date_sort"], reverse=True)
    return thoughts


def group_thoughts_by_date(thoughts):
    """Group thoughts by date for the archive page."""
    groups = []
    current_group = None

    for thought in thoughts:
        if current_group is None or current_group["date"] != thought["date"]:
            current_group = {"date": thought["date"], "thoughts": []}
            groups.append(current_group)
        current_group["thoughts"].append(thought)

    return groups


def load_about():
    """Load the about page content."""
    about_file = CONTENT_DIR / "about.md"
    if about_file.exists():
        post = frontmatter.load(about_file)
        return render_markdown(post.content)
    return "<p>About page content coming soon.</p>"


def load_links():
    """Load the links page content from Markdown."""
    links_file = CONTENT_DIR / "links.md"
    if links_file.exists():
        post = frontmatter.load(links_file)
        return render_markdown(post.content)
    return None


def parse_markdown_link_item(line):
    """Parse a simple Markdown bullet link into card data."""
    match = re.match(r"^\s*[-*]\s+\[([^\]]+)\]\(([^)]+)\)\s*(?:-\s*)?(.*)$", line)
    if not match:
        return None
    title, url, description = match.groups()
    description = description.strip()
    return {
        "title": title.strip(),
        "url": url.strip(),
        "description": description,
        "description_html": render_markdown(description) if description else "",
    }


def link_item_type(section_title, item):
    """Assign a compact display type for link cards."""
    title = item["title"].lower()
    if section_title == "Resource Categories":
        return "Resource"
    if section_title == "Tools & Scripts":
        return "Script"
    if "paper weekly" in title:
        return "Reading"
    if "earthquake" in title:
        return "Seismology"
    if "paper hot" in title or "fish guard" in title:
        return "Tool"
    return "Site"


def link_item_action(item):
    """Choose a lightweight action label for a link card."""
    url = item["url"]
    if "/scripts/" in url:
        return "Script \u2192"
    if "github.com" in url:
        return "GitHub \u2192"
    if url.startswith("/links/"):
        return "Browse \u2192"
    return "Open \u2192"


def load_link_sections():
    """Load Projects & Resources as structured card sections from links.md."""
    links_file = CONTENT_DIR / "links.md"
    if not links_file.exists():
        return []

    post = frontmatter.load(links_file)
    sections = []
    current = None
    section_order = {
        "My Projects": 1,
        "Resource Categories": 2,
        "Tools & Scripts": 3,
    }

    for line in post.content.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            title = heading.group(1).strip()
            current = {"title": title, "items": []}
            sections.append(current)
            continue

        if current is None:
            continue

        item = parse_markdown_link_item(line)
        if item:
            item["type"] = link_item_type(current["title"], item)
            item["action_label"] = link_item_action(item)
            current["items"].append(item)

    sections = [section for section in sections if section["items"]]
    sections.sort(key=lambda section: section_order.get(section["title"], 99))
    return sections


def build_home_projects(link_sections, limit=4):
    """Return the compact project list for the homepage sidebar."""
    for section in link_sections:
        if section["title"] == "My Projects":
            return section["items"][:limit]
    return []


def load_link_pages():
    """Load all link sub-pages from content/links/ directory."""
    links_dir = CONTENT_DIR / "links"
    pages = []
    if not links_dir.exists():
        return pages

    for filepath in links_dir.glob("*.md"):
        try:
            post = frontmatter.load(filepath)
            slug = filepath.stem
            pages.append({
                "title": post.get("title", slug.replace("-", " ").title()),
                "description": post.get("description", ""),
                "order": post.get("order", 999),
                "slug": slug,
                "content": render_markdown(post.content),
            })
        except Exception as e:
            print(f"  [WARN] Skipping link page {filepath.name}: {e}")

    pages.sort(key=lambda p: p["order"])
    return pages


def ensure_dir(path):
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def write_file(path, content):
    """Write content to file."""
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")
    print(f"  -> {path.relative_to(BASE_DIR)}")


def build_search_index(posts):
    """Create a compact client-side search index."""
    index = []
    for post in posts:
        index.append({
            "title": post["title"],
            "date": post["date"],
            "tags": post.get("tags") or [],
            "excerpt": post.get("excerpt_text", ""),
            "slug": post["slug"],
            "url": f"/blog/{post['slug']}.html",
            "content": post.get("search_text", ""),
        })
    return index


def tag_slug(tag):
    """Normalize a tag for tag page URLs."""
    return str(tag).lower().replace(" ", "-").replace("/", "-")


def build_tag_summaries(posts, limit=14):
    """Build popular tag summaries for the blog sidebar."""
    tags = {}
    for post in posts:
        seen_in_post = set()
        for tag in (post.get("tags") or []):
            name = str(tag).strip()
            if not name:
                continue
            slug = tag_slug(name)
            if slug in seen_in_post:
                continue
            seen_in_post.add(slug)
            if slug not in tags:
                tags[slug] = {"name": name, "slug": slug, "count": 0}
            tags[slug]["count"] += 1

    return sorted(
        tags.values(),
        key=lambda item: (-item["count"], item["name"].lower()),
    )[:limit]


def format_archive_month(month_key):
    """Format YYYY-MM as a readable archive month label."""
    try:
        return datetime.strptime(f"{month_key}-01", "%Y-%m-%d").strftime("%B %Y")
    except ValueError:
        return month_key


def build_archive_groups(posts):
    """Group posts by year and month for the archive page."""
    groups = []
    year_group = None
    month_group = None

    for post in posts:
        date_str = str(post.get("date") or "undated")
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            year = date_str[:4]
            month = date_str[:7]
            month_label = format_archive_month(month)
        else:
            year = "Undated"
            month = "Undated"
            month_label = "Undated"

        if year_group is None or year_group["year"] != year:
            year_group = {"year": year, "count": 0, "months": []}
            groups.append(year_group)
            month_group = None

        if month_group is None or month_group["month"] != month:
            month_group = {"month": month, "label": month_label, "count": 0, "posts": []}
            year_group["months"].append(month_group)

        post["archive_date"] = date_str[5:] if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str) else date_str
        month_group["posts"].append(post)
        month_group["count"] += 1
        year_group["count"] += 1

    return groups


def build_archive_years(archive_groups):
    """Build compact year links for archive navigation."""
    return [
        {
            "year": group["year"],
            "count": group["count"],
            "anchor": f"year-{group['year']}",
        }
        for group in archive_groups
    ]


def build_archive_summary(posts, archive_groups):
    """Build summary text for the archive page."""
    years = [
        int(group["year"])
        for group in archive_groups
        if str(group["year"]).isdigit()
    ]
    since = min(years) if years else None
    return {
        "total": len(posts),
        "since": since,
    }


def build_site_stats(posts):
    """Build homepage sidebar stats."""
    total_words = sum(count_text_units(post.get("search_text", "")) for post in posts)
    running_days = max(0, (datetime.now().date() - SITE_START_DATE).days)
    return [
        {"label": "📝 Posts", "value": f"{len(posts):,}"},
        {"label": "🔤 Words", "value": format_compact_number(total_words)},
        {"label": "⏳ Running", "value": f"{running_days:,} days"},
    ]


def build_site():
    """Build the entire static site."""
    print(f"\n{'='*50}")
    print(f"  SEISAMUSE — Building Site")
    print(f"{'='*50}\n")

    env = get_jinja_env()
    year = datetime.now().year

    # Common template context — use absolute paths for root deployment
    common = {
        "root": "/",
        "year": year,
    }

    # Load content
    print("[1/5] Loading posts...")
    posts = load_all_posts()
    print(f"  Found {len(posts)} post(s)")

    thoughts = load_all_thoughts()
    print(f"  Found {len(thoughts)} thought(s)")

    print("[2/6] Loading about page...")
    about_content = load_about()
    links_content = load_links()
    link_sections = load_link_sections()
    link_pages = load_link_pages()
    print(f"  Found {len(link_pages)} link sub-page(s)")

    # Build homepage
    print("[3/6] Building pages...")
    today = datetime.now().strftime("%Y-%m-%d")
    today_thoughts = [thought for thought in thoughts if thought["date"] == today]
    thoughts_preview = today_thoughts or thoughts[:RECENT_THOUGHTS_COUNT]
    thoughts_preview_label = "Today" if today_thoughts else "Recent thoughts"

    tpl_index = env.get_template("index.html")
    write_file(
        SITE_DIR / "index.html",
        tpl_index.render(
            **common,
            active="home",
            layout="home",
            recent_posts=posts[:RECENT_POSTS_COUNT],
            thoughts_preview=thoughts_preview,
            thoughts_preview_label=thoughts_preview_label,
            site_stats=build_site_stats(posts),
            home_projects=build_home_projects(link_sections),
        ),
    )

    # Build paginated blog listing
    tpl_blog = env.get_template("blog.html")
    total_pages = max(1, math.ceil(len(posts) / POSTS_PER_PAGE))
    blog_tags = build_tag_summaries(posts)
    archive_groups = build_archive_groups(posts)
    archive_years = build_archive_years(archive_groups)
    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        page_posts = posts[start:end]

        # Page 1 goes to /blog/index.html, others to /blog/page/N/index.html
        if page_num == 1:
            out_path = SITE_DIR / "blog" / "index.html"
        else:
            out_path = SITE_DIR / "blog" / "page" / str(page_num) / "index.html"

        write_file(
            out_path,
            tpl_blog.render(
                **common,
                active="blog",
                layout="blog",
                posts=page_posts,
                top_tags=blog_tags,
                archive_years=archive_years,
                current_page=page_num,
                total_pages=total_pages,
            ),
        )
    print(f"  Blog: {total_pages} page(s)")

    # Build individual posts + copy assets
    print("[4/5] Building blog posts...")
    tpl_post = env.get_template("post.html")
    assets_copied = 0
    for idx, post in enumerate(posts):
        # Get previous and next posts
        prev_post = posts[idx + 1] if idx + 1 < len(posts) else None
        next_post = posts[idx - 1] if idx > 0 else None

        write_file(
            SITE_DIR / "blog" / f"{post['slug']}.html",
            tpl_post.render(
                **common,
                active="blog",
                post=post,
                prev_post=prev_post,
                next_post=next_post,
            ),
        )
        # Copy post asset folder if it exists
        if post.get("has_assets"):
            src_asset_dir = post["source_path"].parent / post["source_path"].stem
            dst_asset_dir = SITE_DIR / "blog" / "assets" / post["slug"]
            if dst_asset_dir.exists():
                shutil.rmtree(dst_asset_dir)
            shutil.copytree(src_asset_dir, dst_asset_dir)
            assets_copied += 1
    if assets_copied:
        print(f"  Copied assets for {assets_copied} post(s)")

    # Build tag pages
    print("  Building tag pages...")
    tpl_tag = env.get_template("tag.html")
    tag_posts = {}  # tag -> list of posts
    for post in posts:
        for tag in (post.get("tags") or []):
            if tag:
                tag_posts.setdefault(tag, []).append(post)
    
    for tag, tag_post_list in tag_posts.items():
        # Normalize tag for URL (lowercase, replace spaces with dashes)
        current_tag_slug = tag_slug(tag)
        write_file(
            SITE_DIR / "blog" / "tag" / current_tag_slug / "index.html",
            tpl_tag.render(
                **common,
                active="blog",
                tag=tag,
                posts=tag_post_list,
            ),
        )
    print(f"    {len(tag_posts)} tag(s)")

    # Build about page
    tpl_about = env.get_template("about.html")
    write_file(
        SITE_DIR / "about" / "index.html",
        tpl_about.render(
            **common,
            active="about",
            layout="wide",
            about_content=about_content,
        ),
    )

    # Build links hub page
    tpl_links = env.get_template("links.html")
    write_file(
        SITE_DIR / "links" / "index.html",
        tpl_links.render(
            **common,
            active="links",
            layout="wide",
            links_content=links_content,
            link_sections=link_sections,
            link_pages=link_pages,
        ),
    )

    # Build thoughts archive page
    tpl_thoughts = env.get_template("thoughts.html")
    write_file(
        SITE_DIR / "thoughts" / "index.html",
        tpl_thoughts.render(
            **common,
            active="thoughts",
            thought_groups=group_thoughts_by_date(thoughts),
        ),
    )

    # Build full blog archive page
    tpl_archives = env.get_template("archives.html")
    write_file(
        SITE_DIR / "archives" / "index.html",
        tpl_archives.render(
            **common,
            active="archives",
            layout="wide",
            archive_groups=archive_groups,
            archive_years=archive_years,
            archive_summary=build_archive_summary(posts, archive_groups),
        ),
    )

    # Build search page and index
    print("[4/6] Building search index...")
    tpl_search = env.get_template("search.html")
    write_file(
        SITE_DIR / "search" / "index.html",
        tpl_search.render(
            **common,
            active="search",
        ),
    )
    write_file(
        SITE_DIR / "search.json",
        json.dumps(build_search_index(posts), ensure_ascii=False, separators=(",", ":")),
    )

    # Build individual link sub-pages
    print("[4/6] Building link sub-pages...")
    tpl_link_page = env.get_template("link_page.html")
    for lp in link_pages:
        write_file(
            SITE_DIR / "links" / lp["slug"] / "index.html",
            tpl_link_page.render(
                **common,
                active="links",
                page_title=lp["title"],
                page_description=lp["description"],
                page_content=lp["content"],
            ),
        )

    # Build Atom feed
    print("[5/7] Building Atom feed...")
    tpl_feed = env.get_template("atom.xml")
    
    # Prepare posts for Atom feed with proper ISO 8601 date format
    atom_posts = []
    for post in posts[:50]:  # Include last 50 posts in Atom feed
        # Convert date to ISO 8601 format for Atom
        try:
            post_date = datetime.strptime(post["date_sort"], "%Y-%m-%d %H:%M:%S")
            # ISO 8601 format with timezone
            updated = post_date.strftime("%Y-%m-%dT%H:%M:%S+08:00")
            published = post_date.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        except ValueError:
            updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
            published = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        
        # Sanitize content to prevent CDATA breaking
        safe_content = sanitize_for_xml(post.get("content", ""))
        safe_excerpt = sanitize_for_xml(post.get("excerpt", ""))
        
        atom_posts.append({
            **post,
            "updated": updated,
            "published": published,
            "content": safe_content,
            "excerpt": safe_excerpt,
        })
    
    # Get the most recent post date for feed updated time
    if atom_posts:
        updated_date = atom_posts[0]["updated"]
    else:
        updated_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    
    write_file(
        SITE_DIR / "atom.xml",
        tpl_feed.render(
            site_name=SITE_NAME,
            site_url=SITE_URL,
            author=AUTHOR,
            updated_date=updated_date,
            posts=atom_posts,
        ),
    )
    legacy_feed_path = SITE_DIR / "feed.xml"
    if legacy_feed_path.exists():
        legacy_feed_path.unlink()
        print("  Removed legacy feed.xml")

    # Copy static asset directories from content/ to site/
    print("[6/7] Copying assets...")
    for asset_dir_name in ["images", "scripts"]:
        src = CONTENT_DIR / asset_dir_name
        dst = SITE_DIR / asset_dir_name
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  Copied {asset_dir_name}/")

    # Copy CSS files - source from docs/css/ (which contains the original CSS)
    css_src = BASE_DIR / "docs" / "css"
    css_dst = SITE_DIR / "css"
    if css_src.exists():
        if css_dst.exists():
            shutil.rmtree(css_dst)
        shutil.copytree(css_src, css_dst)
        print("  Copied css/")

    # Create .nojekyll file to disable Jekyll on GitHub Pages
    nojekyll_path = SITE_DIR / ".nojekyll"
    nojekyll_path.write_text("", encoding="utf-8")
    print(f"  Created .nojekyll")

    print(f"\n[7/7] Done! Site built in '{SITE_DIR.relative_to(BASE_DIR)}/'")
    print(f"  Total: {len(posts)} posts, {len(thoughts)} thoughts, {total_pages} blog pages, {len(link_pages)} link sub-pages, 6 static pages")
    print(f"  Atom feed: atom.xml")
    print(f"{'='*50}\n")


def serve(port=3000):
    """Start a local HTTP server for preview."""
    import http.server
    import functools

    os.chdir(SITE_DIR)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE_DIR))
    server = http.server.HTTPServer(("", port), handler)
    print(f"Serving at http://localhost:{port}")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    build_site()

    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()
