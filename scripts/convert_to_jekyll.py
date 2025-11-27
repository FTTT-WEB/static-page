#!/usr/bin/env python3
"""
Converter: mirrored HTML -> Jekyll pages + copy referenced assets

Usage: run from workspace root (/Users/bird/Code/fttt/static-page)
  python3 jekyll-site/convert_to_jekyll.py

It will read the mirrored files under `www.fttt.org.tw/` and create files under `jekyll-site/`.
"""

import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Workspace paths (adjust if necessary)
WORKSPACE = Path('/Users/bird/Code/fttt/static-page')
MIRROR = WORKSPACE / 'live_fetch' / 'www.fttt.org.tw'  # Use fresh fetch instead of HTTrack
OUT = WORKSPACE / 'jekyll-site'
PAGES_OUT = OUT / 'pages'
ASSETS_OUT = OUT / 'assets'
UPLOADS_OUT = ASSETS_OUT / 'uploads'
CSS_OUT = ASSETS_OUT / 'css'
THEME_OUT = ASSETS_OUT / 'theme'

MAPPING = [
    ('index.html', -1),  # homepage with page_id 240
    ('page_125.html', 125),
    ('page_87.html', 87),
    ('page_86.html', 86),
    ('page_85.html', 85),
    ('page_89.html', 89),
    ('page_52.html', 52),
    ('page_60.html', 60),
    ('page_61.html', 61),
    ('page_62.html', 62),
    ('page_63.html', 63),
    ('page_64.html', 64),
    ('page_70.html', 70),
    ('page_71.html', 71),
    ('page_72.html', 72),
    ('page_5016.html', 5016),
    ('page_6871.html', 6871),
    ('page_4182.html', 4182),
    ('page_120.html', 120),
    ('page_5147.html', 5147),
]

def safe_mkdir(p: Path):
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

def find_local_asset(src_path: str):
    """Try to resolve an asset path found in HTML (relative path from site root) to a file in the mirror.

    Returns Path or None
    """
    if src_path.startswith('http://') or src_path.startswith('https://'):
        # try to map absolute URLs to mirror root if they point to www.fttt.org.tw
        # Otherwise skip (external)
        if 'www.fttt.org.tw' not in src_path:
            return None
        # convert to path after domain
        parts = src_path.split('www.fttt.org.tw')
        if len(parts) > 1:
            rel = parts[1]
        else:
            rel = src_path
    else:
        rel = src_path

    # normalize leading slash
    if rel.startswith('/'):
        rel = rel[1:]

    cand = MIRROR / rel
    if cand.exists():
        return cand

    # common fallback: sometimes HTTrack wrapped files and gave .html extension; try replacing .html with image ext
    stem = cand.stem
    parent = cand.parent
    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.docx', '.zip', '.svg', '.webp']:
        attempt = parent / (stem + ext)
        if attempt.exists():
            return attempt

    # try glob by stem
    for p in parent.glob(stem + '.*'):
        if p.exists():
            return p

    return None

def copy_asset(src: Path, dest_root: Path):
    rel_parts = src.parts
    # try to keep path after wp-content/uploads or keep last two directories
    try:
        idx = rel_parts.index('wp-content')
        rel = Path(*rel_parts[idx:])
    except ValueError:
        rel = Path(*rel_parts[-3:])

    dest = dest_root / rel
    safe_mkdir(dest.parent)
    shutil.copy2(src, dest)
    return dest

def slug_from_filename(path: Path):
    name = path.stem
    return name.replace('index', 'page').replace('.', '-').lower()

def extract_main(soup: BeautifulSoup):
    # look for common WP container
    main = soup.select_one('.entry-content') or soup.select_one('#content') or soup.body
    return main

def convert_all():
    safe_mkdir(PAGES_OUT)
    safe_mkdir(UPLOADS_OUT)
    safe_mkdir(CSS_OUT)
    safe_mkdir(THEME_OUT)

    created = []
    assets_copied = set()

    for src_filename, page_id in MAPPING:
        src = MIRROR / src_filename
        if not src.exists():
            print(f"SKIP: source not found: {src}")
            continue

        html = src.read_text(encoding='utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'lxml')

        # title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else f'page-{page_id}'

        main = extract_main(soup)
        if main is None:
            body_html = soup.body.decode_contents() if soup.body else html
        else:
            body_html = ''.join(str(x) for x in main.contents)

        # find assets in main
        asset_paths = set()
        temp_soup = BeautifulSoup(body_html, 'lxml')
        for img in temp_soup.find_all('img'):
            if img.get('src'):
                asset_paths.add(img['src'])
        for a in temp_soup.find_all('a'):
            if a.get('href') and ('wp-content/uploads' in a['href'] or '.pdf' in a['href'] or '.docx' in a['href']):
                asset_paths.add(a['href'])

        # also capture theme and css referenced in head (for styling)
        for link in soup.find_all('link'):
            href = link.get('href')
            if not href:
                continue
            if 'wp-content/themes' in href or 'wp-includes' in href or href.endswith('.css'):
                asset_paths.add(href)

        # Copy assets
        for ap in sorted(asset_paths):
            local = find_local_asset(ap)
            if local:
                if 'wp-content/uploads' in str(local):
                    dest = copy_asset(local, UPLOADS_OUT)
                elif 'wp-content/themes' in str(local) or 'wp-includes' in str(local):
                    dest = copy_asset(local, THEME_OUT)
                else:
                    dest = copy_asset(local, ASSETS_OUT)
                assets_copied.add(str(dest.relative_to(OUT)))
                # rewrite paths in body_html to new asset path
                new_rel = '/' + str(Path('assets') / Path(*Path(dest).relative_to(OUT).parts[1:])).replace('\\','/')
                body_html = body_html.replace(ap, new_rel)
            else:
                # leave external URLs as-is (YouTube etc.)
                pass

        # convert to markdown
        md_body = md(body_html, heading_style="ATX")

        # use custom slug for index
        if page_id == -1:
            slug = 'index'
        else:
            slug = f'page_{page_id}'
        out_file = PAGES_OUT / f'{slug}.md'
        fm = [
            '---',
            f'title: "{title}"',
            f'original_page_id: {page_id if page_id != -1 else 240}',
            f'original_file: {src.name}',
            'layout: default',
            '---',
            '',
        ]

        out_file.write_text('\n'.join(fm) + md_body, encoding='utf-8')
        created.append(out_file)
        print(f'CREATED: {out_file} (assets: {len(asset_paths)})')

    # create a small css shim (copy theme css if found)
    print('\nSummary:')
    print(f'Pages created: {len(created)}')
    print(f'Assets copied: {len(assets_copied)}')
    if len(assets_copied) > 0:
        print('Sample assets:')
        for a in list(assets_copied)[:20]:
            print(' -', a)

if __name__ == '__main__':
    print('Starting conversion: mirror -> jekyll-site')
    convert_all()
