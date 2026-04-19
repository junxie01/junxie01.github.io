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
from datetime import datetime
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

# --- Configuration ---
BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
POSTS_DIR = CONTENT_DIR / "posts"
TEMPLATES_DIR = BASE_DIR / "templates"

# Direct deployment: output to docs/ directory for GitHub Pages
SUBDIR = ""
SITE_DIR = BASE_DIR / "site"

SITE_NAME = "SEISAMUSE"
AUTHOR = "Jun Xie"
RECENT_POSTS_COUNT = 5
POSTS_PER_PAGE = 20

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
        extensions=MD_EXTENSIONS,
        extension_configs=MD_EXTENSION_CONFIGS,
    )
    html = md.convert(text)
    md.reset()
    return html


def estimate_reading_time(text):
    """Estimate reading time in minutes (avg 200 words/min for academic text)."""
    word_count = len(text.split())
    return max(1, math.ceil(word_count / 200))


def load_post(filepath):
    """Load a single Markdown post with frontmatter."""
    post = frontmatter.load(filepath)

    # Extract metadata
    title = post.get("title", filepath.stem.replace("-", " ").title())
    date_raw = post.get("date", None)

    # Parse date
    if isinstance(date_raw, datetime):
        date_str = date_raw.strftime("%Y-%m-%d")
    elif isinstance(date_raw, str):
        date_str = date_raw[:10]  # Take YYYY-MM-DD portion
    else:
        date_str = "undated"

    tags = post.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]

    excerpt = post.get("excerpt", post.get("description", ""))
    if not excerpt and len(post.content) > 0:
        # Auto-generate excerpt from first paragraph
        first_para = post.content.strip().split("\n\n")[0]
        excerpt = first_para[:160].rstrip() + ("..." if len(first_para) > 160 else "")
    # Render excerpt as Markdown so links work
    excerpt_html = render_markdown(excerpt) if excerpt else ""

    slug = post.get("slug", filepath.stem)
    content_html = render_markdown(post.content)
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
        "date_sort": date_str,
        "tags": tags,
        "excerpt": excerpt_html,
        "slug": slug,
        "content": content_html,
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

    print("[2/6] Loading about page...")
    about_content = load_about()
    links_content = load_links()
    link_pages = load_link_pages()
    print(f"  Found {len(link_pages)} link sub-page(s)")

    # Build homepage
    print("[3/6] Building pages...")
    tpl_index = env.get_template("index.html")
    write_file(
        SITE_DIR / "index.html",
        tpl_index.render(
            **common,
            active="home",
            recent_posts=posts[:RECENT_POSTS_COUNT],
        ),
    )

    # Build paginated blog listing
    tpl_blog = env.get_template("blog.html")
    total_pages = max(1, math.ceil(len(posts) / POSTS_PER_PAGE))
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
                posts=page_posts,
                current_page=page_num,
                total_pages=total_pages,
            ),
        )
    print(f"  Blog: {total_pages} page(s)")

    # Build individual posts + copy assets
    print("[4/5] Building blog posts...")
    tpl_post = env.get_template("post.html")
    assets_copied = 0
    for post in posts:
        write_file(
            SITE_DIR / "blog" / f"{post['slug']}.html",
            tpl_post.render(
                **common,
                active="blog",
                post=post,
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
        tag_slug = tag.lower().replace(" ", "-").replace("/", "-")
        write_file(
            SITE_DIR / "blog" / "tag" / tag_slug / "index.html",
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
            links_content=links_content,
            link_pages=link_pages,
        ),
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

    # Copy static asset directories from content/ to site/
    print("[5/6] Copying assets...")
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

    print(f"\n[6/6] Done! Site built in '{SITE_DIR.relative_to(BASE_DIR)}/'")
    print(f"  Total: {len(posts)} posts, {total_pages} blog pages, {len(link_pages)} link sub-pages, 4 static pages")
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
