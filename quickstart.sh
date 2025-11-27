#!/bin/bash
# Quick Start Script for FTTT Jekyll Site
# This script helps you build and serve your Jekyll site

set -e

JEKYLL_DIR="/Users/bird/Code/fttt/static-page/jekyll-site"
PARENT_DIR="/Users/bird/Code/fttt/static-page"

echo "=================================="
echo "  FTTT Jekyll Site - Quick Start  "
echo "=================================="
echo ""

# Check if Jekyll dir exists
if [ ! -d "$JEKYLL_DIR" ]; then
    echo "❌ Error: Jekyll directory not found at $JEKYLL_DIR"
    exit 1
fi

echo "📁 Project directory: $JEKYLL_DIR"
echo ""

# Menu
echo "Choose an option:"
echo ""
echo "1) Build with Jekyll (requires Ruby)"
echo "2) Quick preview with Python (no Ruby needed)"
echo "3) View project structure"
echo "4) Check asset status"
echo "5) Open in browser"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Building Jekyll site..."
        cd "$JEKYLL_DIR"

        if ! command -v jekyll &> /dev/null; then
            echo "❌ Jekyll not found. Installing dependencies..."
            if command -v bundle &> /dev/null; then
                bundle install
            else
                echo "❌ Bundler not found. Please install Ruby and Bundle first."
                echo "   Follow: https://jekyllrb.com/docs/installation/"
                exit 1
            fi
        fi

        echo "✓ Starting Jekyll server..."
        echo "📍 Visit http://localhost:4000 in your browser"
        echo ""
        bundle exec jekyll serve
        ;;

    2)
        echo ""
        echo "🐍 Using Python fallback build..."
        cd "$JEKYLL_DIR"

        if [ -f "fallback_build.py" ]; then
            python3 fallback_build.py
            echo ""
            echo "✓ Site built to jekyll-site/_site/"
            echo "📍 You can now open the files in your browser"
        else
            echo "❌ fallback_build.py not found"
            exit 1
        fi
        ;;

    3)
        echo ""
        echo "📂 Project Structure:"
        echo ""
        cd "$JEKYLL_DIR"
        tree -L 2 -I '_site' 2>/dev/null || find . -maxdepth 2 -not -path '*/\.*' -not -path '*/_site*' | head -20
        ;;

    4)
        echo ""
        echo "📊 Asset Status:"
        echo ""

        echo "✓ Images in assets/images/:"
        if [ -d "$JEKYLL_DIR/assets/images" ]; then
            ls -lh "$JEKYLL_DIR/assets/images/" | tail -n +2 | awk '{print "  - " $9 " (" $5 ")"}'
            IMAGE_COUNT=$(ls -1 "$JEKYLL_DIR/assets/images/" | wc -l)
            echo "  Total: $IMAGE_COUNT images"
        else
            echo "  ❌ No images directory"
        fi

        echo ""
        echo "✓ Pages with YouTube embeds:"
        EMBED_COUNT=$(grep -r "youtube.com/embed" "$JEKYLL_DIR/pages/" 2>/dev/null | wc -l)
        echo "  Found $EMBED_COUNT YouTube embeds across all pages"

        echo ""
        echo "✓ Total pages:"
        PAGE_COUNT=$(ls -1 "$JEKYLL_DIR/pages/"*.md 2>/dev/null | wc -l)
        echo "  $PAGE_COUNT Markdown files"
        ;;

    5)
        echo ""
        echo "🌐 Opening in browser..."

        # Check if _site exists and has content
        if [ -f "$JEKYLL_DIR/_site/index.html" ]; then
            open "$JEKYLL_DIR/_site/index.html"
            echo "✓ Opened generated site from _site/"
        elif [ -f "$JEKYLL_DIR/pages/home.md" ]; then
            echo "💡 Site not yet built. Run option 1 or 2 first to generate _site/"
            echo ""
            echo "You can also open pages directly:"
            read -p "Open home.md preview? (y/n): " preview
            if [ "$preview" = "y" ]; then
                open "$JEKYLL_DIR/pages/home.md"
            fi
        else
            echo "❌ No site found to open"
        fi
        ;;

    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "Done! 🎉"
echo "=================================="
