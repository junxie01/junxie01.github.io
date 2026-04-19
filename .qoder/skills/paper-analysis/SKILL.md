---
name: paper-analysis
description: Analyze academic research papers to extract structured information and generate blog posts. Can be run directly from terminal via `python3 paper_analysis.py <pdf_or_url>` using DeepSeek API, or interactively through Qoder. Use when the user wants to analyze a paper, extract paper information, or create a blog post from a paper analysis.
---

# Paper Analysis for Academic Blog

## Terminal Usage (Recommended)

Run directly from the project root:

```bash
# One-time setup: get free API key at https://aistudio.google.com/apikey
export GEMINI_API_KEY="your-key-here"  # add to ~/.zshrc

# Analyze a local PDF
python3 paper_analysis.py paper.pdf

# Analyze from arXiv URL
python3 paper_analysis.py https://arxiv.org/abs/2401.12345
```

Uses Google Gemini 2.0 Flash (free tier: 1500 req/day, no credit card needed).

## Interactive Usage (via Qoder)

If running interactively, follow the output structure below.

## Output Structure

Generate a Markdown file with the following sections:

```markdown
---
title: "[Paper Title]"
date: YYYY-MM-DD
tags: [paper, field1, field2]
excerpt: "Brief summary of the paper in one sentence."
---

## Paper Information

- **Title**: [Full paper title]
- **First Author**: [Name]
- **Corresponding Author**: [Name]
- **Affiliation**: [Institution/University]
- **Journal**: [Journal Name, Year, Volume, Pages]
- **DOI**: [DOI link]

## Author Background

### First Author's Representative Works
1. [Citation format: Author et al. (Year). Title. Journal.]
2. [Citation format]
3. [Citation format]

## Abstract (Translated)

[Chinese translation of the abstract]

## Research Context

### Importance
[Why this research matters - 2-3 paragraphs]

### Previous Studies
[List and describe specific prior works with citations]
- Study 1: [What they did, what they found]
- Study 2: [What they did, what they found]
- Study 3: [What they did, what they found]

### Limitations of Previous Research
[What gaps or shortcomings existed before this paper]

## Methodology

### Data
[What datasets were used, time period, spatial coverage, sources]

### Methods
[Technical approaches, algorithms, models, tools used]

## Results

[Key findings presented in the paper]

## Discussion

### Innovations
[What is new or unique about this work]

### Contributions
[How this advances the field]

### Limitations
[What the authors acknowledge as weaknesses or future work]

## Personal Thoughts

[Optional: your own commentary or connections to your research]

## References

[Full citation list if available]
```

## Workflow

1. **Receive paper**: User provides paper (PDF, URL, or text)
2. **Extract metadata**: Identify title, authors, affiliations, journal info
3. **Research author**: Find first author's other representative publications
4. **Translate abstract**: Provide Chinese translation
5. **Analyze context**: 
   - Explain research importance
   - Identify and describe 3-5 key prior studies
   - Highlight gaps this paper addresses
6. **Extract methodology**: Data sources and methods
7. **Summarize results**: Key findings
8. **Evaluate**: Innovations, contributions, limitations
9. **Generate file**: Save to `content/posts/YYYY-MM-DD-paper-[keyword].md`

## Tag Selection

Choose 3-5 appropriate tags from:
- Field: seismology, geophysics, glaciology, environmental-seismology
- Method: ambient-noise, tomography, machine-learning, inversion
- Data: DAS, GPS, InSAR, broadband
- Topic: crustal-structure, mantle, earthquakes, hazards

## File Naming

Save as: `content/posts/YYYY-MM-DD-paper-[short-keyword].md`

Example: `2024-06-15-paper-ambient-noise-tomography.md`
