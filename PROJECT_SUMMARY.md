# SEISAMUSE Project Summary

## Quick Reference for New Sessions

### What This Is
Minimalist academic personal website for Jun Xie (seismologist/geophysicist at Academy of Precision Measurement Science and Technology). Built with Python + Jinja2 + Markdown.

### Key Files
| File | Purpose |
|------|---------|
| `build.py` | Static site generator — run `python3 build.py` to rebuild |
| `content/posts/*.md` | Blog posts (196 migrated from Hexo) |
| `content/about.md` | About page content |
| `content/links.md` | Links page (Markdown editable) |
| `content/images/` | Shared images |
| `content/scripts/` | Downloadable scripts |
| `templates/*.html` | Jinja2 templates |
| `site/` | Generated output (deploy this folder to GitHub Pages) |

### Features Implemented
- [x] 196 posts migrated from Hexo
- [x] Pagination (20 posts/page)
- [x] Tag filtering (`/blog/tag/<tag>/`)
- [x] Clickable tags on posts
- [x] Donation modal with Alipay/WeChat QR
- [x] Avatar using `seisamuse.png`
- [x] Markdown excerpts render properly
- [x] Links page editable via `content/links.md`
- [x] Script downloads from `/scripts/`

### Skills Available
- `paper-analysis`: Analyze papers → structured blog posts

### Common Tasks
```bash
# Rebuild site
python3 build.py

# Add new post
echo "---
title: New Post
date: 2024-06-15
tags: [seismology]
---

Content here." > content/posts/2024-06-15-new-post.md
python3 build.py
```

### URLs (after build)
- Home: `/`
- Blog: `/blog/`
- Tags: `/blog/tag/<tag>/`
- Scripts: `/scripts/filename.py`
- Images: `/images/filename.png`

### Deployment
GitHub Pages: build site with `python3 build.py`, then push contents of `site/` folder to `junxie01.github.io` repo.

---
Last updated: 2026-04-19
