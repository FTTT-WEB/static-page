#!/usr/bin/env python3
"""
WordPress to Jekyll Converter
Crawls WordPress pages and converts them to Jekyll format, preserving original design.

Usage:
  python3 crawl_and_convert.py
"""

import os
import sys
import time
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, List
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Configuration
WORKSPACE = Path('/Users/bird/Code/fttt/static-page')
MIRROR_DIR = WORKSPACE / 'page_backups'
JEKYLL_OUT = WORKSPACE / 'jekyll-site'
PAGES_OUT = JEKYLL_OUT / 'pages'
ASSETS_OUT = JEKYLL_OUT / 'assets'

# Base URLs and pages to crawl
BASE_URL = "https://www.fttt.org.tw"
PAGES_TO_CRAWL = [
    ("https://www.fttt.org.tw/", "Home"),
    ("https://www.fttt.org.tw/?page_id=125", None),
    ("https://www.fttt.org.tw/?page_id=87", None),
    ("https://www.fttt.org.tw/?page_id=86", None),
    ("https://www.fttt.org.tw/?page_id=85", None),
    ("https://www.fttt.org.tw/?page_id=89", None),
    ("https://www.fttt.org.tw/?page_id=52", None),
    ("https://www.fttt.org.tw/?page_id=60", None),
    ("https://www.fttt.org.tw/?page_id=61", None),
    ("https://www.fttt.org.tw/?page_id=62", None),
    ("https://www.fttt.org.tw/?page_id=63", None),
    ("https://www.fttt.org.tw/?page_id=64", None),
    ("https://www.fttt.org.tw/?page_id=70", None),
    ("https://www.fttt.org.tw/?page_id=71", None),
    ("https://www.fttt.org.tw/?page_id=72", None),
    ("https://www.fttt.org.tw/?page_id=5016", None),
    ("https://www.fttt.org.tw/?page_id=6871", None),
    ("https://www.fttt.org.tw/?page_id=4182", None),
    ("https://www.fttt.org.tw/?page_id=120", None),
    ("https://www.fttt.org.tw/?page_id=5147", None),
]

# Session for requests
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})

def safe_mkdir(p: Path):
    """Create directory safely"""
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {p}")

def sanitize_filename(name: str) -> str:
    """Sanitize a string to be used as a filename"""
    # Remove the site name suffix if present
    name = re.sub(r'\s*–?\s*臺灣福音工作全時間訓練網站\s*$', '', name)
    # Remove special characters but keep spaces and hyphens
    name = re.sub(r'[^\w\s\-]', '', name)
    # Replace spaces with hyphens
    name = re.sub(r'\s+', '-', name)
    # Remove multiple hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-').lower()
    return name

def download_asset(url: str, base_path: Path) -> Optional[Path]:
    """Download an asset and save it locally"""
    try:
        # Parse URL
        parsed = urlparse(url)
        
        # Skip external assets and data URIs
        if parsed.netloc and 'fttt.org.tw' not in parsed.netloc:
            return None
        if url.startswith('data:'):
            return None
        
        # Make full URL if relative
        if not url.startswith('http'):
            url = urljoin(BASE_URL, url)
        
        # Download
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        # Determine file path
        path = urlparse(url).path
        filename = Path(path).name or 'asset'
        
        # Create subdirectories based on URL path
        path_parts = Path(path).parts
        if len(path_parts) > 1:
            rel_dir = Path(*path_parts[:-1])
            save_dir = base_path / rel_dir
        else:
            save_dir = base_path
        
        safe_mkdir(save_dir)
        save_path = save_dir / filename
        
        # Don't overwrite existing files
        if save_path.exists():
            return save_path
        
        save_path.write_bytes(response.content)
        print(f"  ✓ Downloaded: {save_path.relative_to(WORKSPACE)}")
        return save_path
    except Exception as e:
        print(f"  ✗ Failed to download {url}: {e}")
        return None

def extract_page_title_from_h3(soup: BeautifulSoup) -> Optional[str]:
    """Extract the page title from wp-block-heading class"""
    # First try to find heading with wp-block-heading class
    heading = soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], class_='wp-block-heading')
    if heading:
        title = heading.get_text().strip()
        return title if title else None
    
    # Fallback to first h1
    h1 = soup.find('h1')
    if h1 and h1.get('class') is None:  # Skip site title h1s
        title = h1.get_text().strip()
        return title if title else None
    
    # Fallback to h2
    h2 = soup.find('h2')
    if h2:
        title = h2.get_text().strip()
        return title if title else None
    
    return None

def extract_content(soup: BeautifulSoup) -> Tuple[str, BeautifulSoup]:
    """
    Extract main content while preserving structure.
    Returns (header_html, main_content_soup, footer_html)
    """
    # Extract header
    header = soup.find('header')
    header_html = str(header) if header else ""
    
    # Extract footer
    footer = soup.find('footer')
    footer_html = str(footer) if footer else ""
    
    # Extract main content
    main = soup.find('main')
    if not main:
        main = soup.find('div', class_='content')
    if not main:
        main = soup.find('article')
    if not main:
        # Fallback: find the main content area
        main = soup.find('div', id='content')
    
    return header_html, main if main else soup, footer_html

def process_html_for_jekyll(html_content: str, url: str, page_num: int) -> Tuple[str, Optional[str]]:
    """
    Process HTML content:
    1. Extract title from H3
    2. Download assets
    3. Convert to markdown
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title from H3
    page_title = extract_page_title_from_h3(soup)
    
    if not page_title:
        # Fallback to page title tag
        title_tag = soup.find('title')
        if title_tag:
            page_title = title_tag.get_text().strip()
            # Remove site name if present
            page_title = re.sub(r'\s*[-|]\s*.*$', '', page_title)
    
    print(f"  Page title extracted: {page_title}")
    
    # Extract main content
    header_html, main_content, footer_html = extract_content(soup)
    
    # Download assets from the page
    assets_dir = ASSETS_OUT / 'page_assets'
    
    # Download images
    for img in main_content.find_all('img'):
        src = img.get('src')
        if src:
            asset_path = download_asset(src, assets_dir)
            if asset_path:
                # Update img src to relative path
                rel_path = asset_path.relative_to(JEKYLL_OUT)
                img['src'] = f"/{rel_path}"
    
    # Download links (documents, PDFs, etc)
    for a in main_content.find_all('a'):
        href = a.get('href')
        if href and not href.startswith('http'):
            # Check if it's a document
            if any(href.endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip']):
                asset_path = download_asset(href, assets_dir)
                if asset_path:
                    rel_path = asset_path.relative_to(JEKYLL_OUT)
                    a['href'] = f"/{rel_path}"
    
    # Convert to markdown
    main_html = str(main_content)
    markdown_content = md(main_html)
    
    # Clean up markdown
    markdown_content = re.sub(r'\n\n+', '\n\n', markdown_content)  # Remove excessive blank lines
    
    return markdown_content.strip(), page_title

def crawl_page(url: str, suggested_title: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Crawl a single page.
    Returns: (page_content_markdown, page_title, filename)
    """
    try:
        print(f"\n🔄 Crawling: {url}")
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        # Save backup
        safe_mkdir(MIRROR_DIR)
        page_id = re.search(r'page_id=(\d+)', url)
        if page_id:
            backup_file = MIRROR_DIR / f"page_{page_id.group(1)}.html"
        else:
            backup_file = MIRROR_DIR / "index.html"
        
        backup_file.write_text(response.text, encoding='utf-8')
        print(f"  ✓ Backup saved: {backup_file.name}")
        
        # Process content
        markdown_content, page_title = process_html_for_jekyll(response.text, url, 0)
        
        # Use suggested title if provided
        if suggested_title:
            page_title = suggested_title
        
        # Generate filename from title
        if page_title:
            filename = sanitize_filename(page_title)
        else:
            page_id = re.search(r'page_id=(\d+)', url)
            filename = f"page_{page_id.group(1)}" if page_id else "home"
        
        print(f"  ✓ Converted to markdown")
        print(f"  ✓ Page title: {page_title}")
        print(f"  ✓ Filename: {filename}.md")
        
        return markdown_content, page_title, filename
        
    except Exception as e:
        print(f"  ✗ Error crawling {url}: {e}")
        return None, None, None

def create_jekyll_page(content: str, title: str, filename: str) -> Path:
    """Create a Jekyll markdown page with front matter"""
    safe_mkdir(PAGES_OUT)
    
    # Create front matter
    front_matter = f"""---
layout: default
title: {title}
---

{content}
"""
    
    # Write file
    page_path = PAGES_OUT / f"{filename}.md"
    page_path.write_text(front_matter, encoding='utf-8')
    print(f"  ✓ Jekyll page created: {page_path.relative_to(WORKSPACE)}")
    
    return page_path

def update_config():
    """Update Jekyll config with site title"""
    config_path = JEKYLL_OUT / '_config.yml'
    config_content = config_path.read_text(encoding='utf-8', errors='ignore')
    
    # Add site settings
    if 'url:' not in config_content:
        config_content += '\nurl: "https://www.fttt.org.tw"\n'
    
    config_path.write_text(config_content, encoding='utf-8')
    print(f"✓ Updated Jekyll config")

def main():
    print("=" * 60)
    print("WordPress to Jekyll Converter")
    print("=" * 60)
    
    # Create directories
    safe_mkdir(PAGES_OUT)
    safe_mkdir(ASSETS_OUT)
    safe_mkdir(MIRROR_DIR)
    
    print(f"\n📁 Output directories created")
    print(f"  - Pages: {PAGES_OUT.relative_to(WORKSPACE)}")
    print(f"  - Assets: {ASSETS_OUT.relative_to(WORKSPACE)}")
    print(f"  - Backups: {MIRROR_DIR.relative_to(WORKSPACE)}")
    
    # Crawl pages
    print(f"\n📥 Starting to crawl {len(PAGES_TO_CRAWL)} pages...")
    print("=" * 60)
    
    created_pages = []
    failed_pages = []
    
    for url, suggested_title in PAGES_TO_CRAWL:
        content, title, filename = crawl_page(url, suggested_title)
        
        if content and title and filename:
            create_jekyll_page(content, title, filename)
            created_pages.append((filename, title))
        else:
            failed_pages.append(url)
        
        # Be respectful to the server
        time.sleep(2)
    
    # Update config
    update_config()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Conversion Complete!")
    print("=" * 60)
    print(f"✓ Successfully created: {len(created_pages)} pages")
    print(f"✗ Failed: {len(failed_pages)} pages")
    
    if created_pages:
        print("\n📄 Created pages:")
        for filename, title in created_pages:
            print(f"  - {filename}.md: {title}")
    
    if failed_pages:
        print("\n⚠️  Failed to crawl:")
        for url in failed_pages:
            print(f"  - {url}")
    
    print("\n📝 Next steps:")
    print(f"  1. Review pages in: {PAGES_OUT}")
    print(f"  2. Update _layouts/default.html if needed")
    print(f"  3. Run: jekyll serve (if Ruby/Jekyll installed)")
    print(f"  4. Or run: python3 jekyll-site/fallback_build.py (for preview)")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
