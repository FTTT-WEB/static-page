#!/usr/bin/env python3
"""
Fallback static builder: Renders generated Markdown pages into HTML using the
Jekyll layout template to create a `_site/` preview without Ruby/Jekyll.

Features:
- Preserves HTML embeds (YouTube iframes, etc.)
- Fixes relative paths for CSS, JS, and images
- Handles nested directory structure
- Supports YAML front matter in markdown files

Run from workspace root:
  /Users/bird/Code/fttt/static-page/.venv/bin/python jekyll-site/fallback_build.py
"""

from pathlib import Path
import re
import markdown
import shutil

# ============================================================================
# Configuration: Define base paths
# ============================================================================
BASE = Path('/Users/bird/Code/fttt/static-page/jekyll-site')
PAGES = BASE  # Pages are now in root directory (*.md files alongside index.md)
LAYOUT = BASE / '_layouts' / 'default.html'
CONFIG = BASE / '_config.yml'
OUT = BASE / '_site'


# ============================================================================
# Configuration Readers
# ============================================================================

def read_site_title():
    """
    Read the site title from _config.yml.
    Returns 'FTTT Static Clone' as default if not found.
    """
    if not CONFIG.exists():
        return 'FTTT Static Clone'

    txt = CONFIG.read_text(encoding='utf-8', errors='ignore')
    match = re.search(r'^title:\s*(.+)$', txt, flags=re.MULTILINE)

    if not match:
        return 'FTTT Static Clone'

    # Strip quotes and whitespace from the title value
    val = match.group(1).strip()
    return val.strip('"').strip("'")


def read_baseurl():
    """
    Read the baseurl from _config.yml for proper asset path prefixing.
    Returns empty string if not found or empty.
    """
    if not CONFIG.exists():
        return ''

    txt = CONFIG.read_text(encoding='utf-8', errors='ignore')
    match = re.search(r'^baseurl:\s*(.*)$', txt, flags=re.MULTILINE)

    if not match:
        return ''

    # Strip quotes and whitespace from the baseurl value
    val = match.group(1).strip().strip('"').strip("'")
    return val


# ============================================================================
# Markdown Processing
# ============================================================================

def parse_front_matter(text):
    """
    Parse YAML front matter from markdown text.

    Expected format:
        ---
        title: Page Title
        key: value
        ---
        # Markdown content here

    Returns:
        tuple: (front_matter_dict, markdown_body)
    """
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            fm_raw = parts[1]
            body = parts[2]
        else:
            fm_raw = ''
            body = text
    else:
        fm_raw = ''
        body = text

    # Parse front matter into a dictionary
    fm = {}
    for line in fm_raw.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            fm[key.strip()] = value.strip().strip('"').strip("'")

    return fm, body


def preserve_html_blocks(text):
    """
    Extract HTML blocks (like iframes) before markdown processing to prevent
    markdown from mangling them. Replaces them with unique placeholders.

    Args:
        text: Markdown text that may contain HTML blocks

    Returns:
        tuple: (text_with_placeholders, placeholder_to_html_map)
    """
    html_blocks = {}
    counter = 0

    # Find and replace iframe blocks with placeholders
    pattern = r'<iframe[^>]*>.*?</iframe>'

    for match in re.finditer(pattern, text, re.DOTALL):
        # Use a unique placeholder that markdown won't interpret
        placeholder = f"YOUTUBEEMBED{counter}YOUTUBEEMBED"
        html_blocks[placeholder] = match.group(0)
        counter += 1

    # Replace all iframes with placeholders
    for placeholder, iframe_html in html_blocks.items():
        text = text.replace(iframe_html, placeholder, 1)

    return text, html_blocks


def restore_html_blocks(html_text, placeholder_map):
    """
    Restore HTML blocks after markdown processing by replacing placeholders
    with the original HTML. Tries multiple patterns since markdown may have
    wrapped placeholders in <p> or <strong> tags.

    Args:
        html_text: HTML output from markdown processor
        placeholder_map: Dictionary mapping placeholders to original HTML

    Returns:
        str: HTML with placeholders replaced by original HTML blocks
    """
    for placeholder, original_html in placeholder_map.items():
        # Try different patterns markdown might have created
        patterns_to_try = [
            f"<p>{placeholder}</p>",                    # Wrapped in <p>
            f"<p><strong>{placeholder}</strong></p>",   # Wrapped in <p> and <strong>
            f"<strong>{placeholder}</strong>",          # Just <strong>
            placeholder                                  # Plain placeholder
        ]

        for pattern in patterns_to_try:
            if pattern in html_text:
                html_text = html_text.replace(pattern, original_html)
                break

    return html_text


# ============================================================================
# Path and URL Handling
# ============================================================================

def prefix_baseurl_in_content(html_content, baseurl):
    """
    Prefix baseurl to all /assets/ paths in content for proper asset loading
    when the site is deployed to a subdirectory.

    Example:
        If baseurl='/my-site', transforms:
        src="/assets/img.jpg" → src="/my-site/assets/img.jpg"

    Args:
        html_content: HTML content to process
        baseurl: Base URL prefix from config

    Returns:
        str: HTML with prefixed asset paths
    """
    if not baseurl:
        return html_content

    # Replace /assets/ with /baseurl/assets/ in src and href attributes
    html_content = re.sub(
        r'(src="|href=")(/assets/)',
        rf'\g<1>{baseurl}\g<2>',
        html_content
    )

    return html_content


# ============================================================================
# Main Build Function
# ============================================================================

def render():
    """
    Main build function that:
    1. Reads configuration
    2. Copies static assets
    3. Processes markdown files into HTML
    4. Applies layout template
    5. Writes output to _site/ directory
    """
    # Read site configuration
    site_title = read_site_title()
    baseurl = read_baseurl()

    # Verify layout template exists
    if not LAYOUT.exists():
        print(f'❌ Layout not found: {LAYOUT}')
        return

    layout_t = LAYOUT.read_text(encoding='utf-8', errors='ignore')

    # Create output directory
    OUT.mkdir(parents=True, exist_ok=True)

    # Copy static assets (css/js/images) to _site/
    src_assets = BASE / 'assets'
    dst_assets = OUT / 'assets'

    if src_assets.exists():
        if dst_assets.exists():
            shutil.rmtree(dst_assets)
        shutil.copytree(src_assets, dst_assets)
        print(f'✓ COPIED assets → {dst_assets}')

    # Track created files for summary
    created = []

    # Collect all markdown files to process (PAGES is now BASE, so all .md files)
    all_pages = sorted(PAGES.glob('*.md'))

    # Exclude README.md and other non-page files
    all_pages = [p for p in all_pages if p.stem not in ['README', 'Gemfile']]

    # Process each markdown file
    for mdfile in sorted(all_pages):
        txt = mdfile.read_text(encoding='utf-8', errors='ignore')

        # Parse YAML front matter and markdown body
        fm, body_md = parse_front_matter(txt)
        title = fm.get('title', mdfile.stem)

        # Extract HTML blocks to preserve them during markdown processing
        body_md, html_blocks = preserve_html_blocks(body_md)

        # Convert markdown to HTML with extensions for tables and raw HTML
        html_body = markdown.markdown(
            body_md,
            extensions=['extra', 'tables']
        )

        # Restore the HTML blocks that were temporarily removed
        html_body = restore_html_blocks(html_body, html_blocks)

        # Prefix baseurl to asset paths for correct loading
        html_body = prefix_baseurl_in_content(html_body, baseurl)

        # Apply layout template with content and metadata
        page_html = layout_t
        page_html = page_html.replace('{{ content }}', html_body)
        page_html = page_html.replace('{{ page.title }}', title)
        page_html = page_html.replace('{{ site.title }}', site_title)
        page_html = page_html.replace('{{ site.baseurl }}', baseurl)

        # Determine output path based on file location
        slug = mdfile.stem

        if slug == 'index':
            # Root index.md → _site/index.html
            out_file = OUT / 'index.html'
            out_file.write_text(page_html, encoding='utf-8')
            created.append(out_file)
            print(f'✓ WROTE index.html')
        else:
            # Other pages → _site/{slug}/index.html
            out_dir = OUT / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / 'index.html'
            out_file.write_text(page_html, encoding='utf-8')
            created.append(out_file)
            print(f'✓ WROTE {slug}/index.html')

    # Print build summary
    print(f'\n✅ Fallback build complete. Files written: {len(created)}')
    print(f'📁 Open in browser: file://{OUT}/index.html')


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == '__main__':
    render()