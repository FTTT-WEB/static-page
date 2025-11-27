#!/usr/bin/env python3
"""
Enrich Jekyll Site with YouTube Embeds and Images
================================================

This script:
1. Extracts YouTube video IDs from HTML backups
2. Downloads images from the original website
3. Updates Markdown pages with YouTube embeds and image references

Usage:
  python3 enrich_jekyll_site.py
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup
import time

# Configuration
WORKSPACE = Path('/Users/bird/Code/fttt/static-page')
BACKUP_DIR = WORKSPACE / 'page_backups'
JEKYLL_OUT = WORKSPACE / 'jekyll-site'
PAGES_OUT = JEKYLL_OUT / 'pages'
ASSETS_OUT = JEKYLL_OUT / 'assets'
IMAGES_OUT = ASSETS_OUT / 'images'

BASE_URL = "https://www.fttt.org.tw"

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

def extract_youtube_from_html(html_path: Path) -> List[Dict]:
    """Extract YouTube embed information from HTML file"""
    videos = []

    if not html_path.exists():
        return videos

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find all YouTube iframes
        iframes = soup.find_all('iframe')

        for iframe in iframes:
            src = iframe.get('src', '')
            title = iframe.get('title', '')

            # Extract video ID from YouTube URL
            # Pattern: https://www.youtube.com/embed/VIDEO_ID
            match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', src)
            if match:
                video_id = match.group(1)
                videos.append({
                    'id': video_id,
                    'url': f'https://www.youtube.com/embed/{video_id}',
                    'title': title,
                    'src': src
                })

        # Also find YouTube watch URLs in the content
        content = soup.get_text()
        watch_pattern = r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
        for match in re.finditer(watch_pattern, content):
            video_id = match.group(1)
            videos.append({
                'id': video_id,
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'title': 'YouTube video',
                'src': None
            })

        # Remove duplicates
        seen = set()
        unique_videos = []
        for v in videos:
            if v['id'] not in seen:
                seen.add(v['id'])
                unique_videos.append(v)

        return unique_videos
    except Exception as e:
        print(f"✗ Error extracting YouTube from {html_path}: {e}")
        return videos

def extract_images_from_html(html_path: Path) -> List[Dict]:
    """Extract image information from HTML file"""
    images = []

    if not html_path.exists():
        return images

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find all img tags (excluding icons and very small images)
        img_tags = soup.find_all('img')

        for img in img_tags:
            src = img.get('src', '')
            alt = img.get('alt', '')

            # Skip external tracking pixels and data URIs
            if not src or 'fttt.org.tw' not in src or src.startswith('data:'):
                continue

            # Skip very tiny images (likely icons)
            width = img.get('width', '')
            height = img.get('height', '')
            if width and height:
                try:
                    if int(width) < 50 or int(height) < 50:
                        continue
                except:
                    pass

            images.append({
                'src': src,
                'alt': alt,
                'title': img.get('title', ''),
                'lazy': img.get('loading') == 'lazy'
            })

        # Remove duplicates
        seen = set()
        unique_images = []
        for img in images:
            if img['src'] not in seen:
                seen.add(img['src'])
                unique_images.append(img)

        return unique_images
    except Exception as e:
        print(f"✗ Error extracting images from {html_path}: {e}")
        return images

def download_image(url: str, dest_dir: Path) -> Optional[str]:
    """Download an image and save it locally, return relative path"""
    try:
        # Make full URL if relative
        if not url.startswith('http'):
            url = urljoin(BASE_URL, url)

        # Skip if not from fttt.org.tw
        if 'fttt.org.tw' not in url:
            return None

        # Determine filename
        parsed_path = urlparse(url).path
        filename = Path(parsed_path).name

        # If no filename, create one
        if not filename:
            filename = f"image_{hash(url) % 10000}.jpg"

        # Check if file already exists
        dest_path = dest_dir / filename
        if dest_path.exists():
            print(f"  ⏭️  Skipped (exists): {filename}")
            return f"/assets/images/{filename}"

        # Download image
        response = session.get(url, timeout=10)
        response.raise_for_status()

        # Save file
        with open(dest_path, 'wb') as f:
            f.write(response.content)

        print(f"  ✓ Downloaded: {filename}")
        return f"/assets/images/{filename}"

    except Exception as e:
        print(f"  ✗ Failed to download {url}: {e}")
        return None

def extract_page_title_from_html(html_path: Path) -> str:
    """Extract page title from HTML"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Try to get from h1 or h2 with wp-block-heading class
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            if 'wp-block-heading' in tag.get('class', []):
                return tag.get_text(strip=True)

        # Fallback to title tag
        title = soup.find('title')
        if title:
            text = title.get_text(strip=True)
            # Remove site name suffix
            text = re.sub(r'\s*–?\s*臺灣福音工作全時間訓練網站\s*$', '', text)
            return text

        return "Untitled"
    except:
        return "Untitled"

def generate_youtube_embed_markdown(video_id: str, title: str = "") -> str:
    """Generate Markdown for YouTube embed"""
    # Using HTML for better control of the iframe
    return f'<iframe width="100%" height="480" src="https://www.youtube.com/embed/{video_id}" title="{title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n'

def map_backup_files_to_pages() -> Dict[Path, Path]:
    """Map backup HTML files to Markdown pages"""
    mapping = {}

    # Read all markdown files and their titles
    md_files = list(PAGES_OUT.glob('*.md'))

    for md_file in md_files:
        # Read the title from front matter
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            title_match = re.search(r'title:\s*([^\n]+)', content)
            if title_match:
                title = title_match.group(1).strip()

                # Find matching backup file
                for backup_file in BACKUP_DIR.glob('*.html'):
                    backup_title = extract_page_title_from_html(backup_file)
                    if title.lower() in backup_title.lower() or backup_title.lower() in title.lower():
                        mapping[md_file] = backup_file
                        break

    return mapping

def process_pages():
    """Process all pages and add YouTube embeds and images"""

    print("\n" + "=" * 70)
    print("ENRICHING JEKYLL SITE WITH YOUTUBE & IMAGES")
    print("=" * 70)

    # Create image directory
    safe_mkdir(IMAGES_OUT)

    # Map markdown files to backup HTML
    print("\n📋 Mapping pages to backups...")
    page_mapping = map_backup_files_to_pages()

    if not page_mapping:
        print("✗ No page mappings found. Attempting fallback mapping...")
        # Fallback: try to match by filename patterns
        md_files = list(PAGES_OUT.glob('*.md'))
        backup_files = list(BACKUP_DIR.glob('*.html'))

        for md_file in md_files:
            # Try to match by checking all backups
            for backup_file in backup_files:
                try:
                    with open(md_file, 'r') as mf:
                        md_content = mf.read()
                    with open(backup_file, 'r') as bf:
                        backup_content = bf.read()

                    # Check if they share significant content
                    if 'wp-block-heading' in backup_content:
                        page_mapping[md_file] = backup_file
                        break
                except:
                    pass

    print(f"✓ Found {len(page_mapping)} page mappings\n")

    # Process each page
    for md_file, backup_file in page_mapping.items():
        print(f"\n📄 Processing: {md_file.name}")
        print(f"   Backup: {backup_file.name}")

        # Extract YouTube videos
        videos = extract_youtube_from_html(backup_file)
        print(f"   🎥 Found {len(videos)} YouTube video(s)")

        # Extract images
        images = extract_images_from_html(backup_file)
        print(f"   🖼️  Found {len(images)} image(s)")

        # Download images
        downloaded_images = {}
        if images:
            print("   ⬇️  Downloading images...")
            for img_info in images:
                local_path = download_image(img_info['src'], IMAGES_OUT)
                if local_path:
                    downloaded_images[img_info['src']] = local_path
            time.sleep(1)  # Be respectful to the server

        # Update markdown file with embeds and images
        if videos or downloaded_images:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    md_content = f.read()

                # Add YouTube videos to the end
                if videos:
                    md_content += "\n\n## 影音資源\n\n"
                    for video in videos:
                        md_content += generate_youtube_embed_markdown(video['id'], video['title'])
                        md_content += "\n"

                # If images were downloaded, add them
                if downloaded_images:
                    md_content += "\n\n## 圖片\n\n"
                    for orig_src, local_path in downloaded_images.items():
                        filename = Path(orig_src).name
                        md_content += f"![{filename}]({local_path})\n\n"

                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(md_content)

                print(f"   ✓ Updated: {md_file.name}")
            except Exception as e:
                print(f"   ✗ Error updating {md_file.name}: {e}")

def create_asset_manifest():
    """Create a manifest of all downloaded assets"""
    manifest = {
        'generated': str(Path.cwd()),
        'images': [],
        'videos': []
    }

    # List all images
    if IMAGES_OUT.exists():
        for img in IMAGES_OUT.glob('*'):
            if img.is_file():
                manifest['images'].append(img.name)

    # Save manifest
    manifest_path = JEKYLL_OUT / 'assets_manifest.json'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n📋 Asset manifest saved to: {manifest_path}")

def main():
    """Main execution"""

    # Check if directories exist
    if not BACKUP_DIR.exists():
        print(f"✗ Backup directory not found: {BACKUP_DIR}")
        return

    if not PAGES_OUT.exists():
        print(f"✗ Pages directory not found: {PAGES_OUT}")
        return

    # Process pages
    process_pages()

    # Create manifest
    create_asset_manifest()

    print("\n" + "=" * 70)
    print("✅ ENRICHMENT COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Images saved to: {IMAGES_OUT}")
    print(f"📄 Updated pages: {PAGES_OUT}")
    print("\nNext steps:")
    print("  1. Review the updated pages in jekyll-site/pages/")
    print("  2. Build the Jekyll site: cd jekyll-site && bundle install && jekyll serve")
    print("  3. Or use fallback: python3 jekyll-site/fallback_build.py")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()
