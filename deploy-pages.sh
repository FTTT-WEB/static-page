#!/bin/bash
# deploy-pages.sh
# Deploy Jekyll site to GitHub Pages gh-pages branch
# Usage: ./deploy-pages.sh
#
# Prerequisites:
#   - Build site first: ./build-pages.sh
#   - ghp-import installed: pip install ghp-import

set -e

cd "$(dirname "$0")" || exit 1

# Check if _site exists and has been built
if [ ! -f "_site/index.html" ]; then
    echo "⚠️  _site/ not found or not built"
    echo ""
    echo "Building now..."
    ./build-pages.sh
fi

echo ""
echo "=================================="
echo "Deploying to GitHub Pages..."
echo "=================================="
echo ""

# Fix image paths in content: prefix /assets/ and /wp-content/ with /static-page
echo "Fixing image paths..."
find _site -name "*.html" -exec sed -i '' 's|src="/assets/|src="/static-page/assets/|g' {} \;
find _site -name "*.html" -exec sed -i '' 's|src="/wp-content/|src="/static-page/wp-content/|g' {} \;
find _site -name "*.html" -exec sed -i '' 's|src="/static-page//|src="/static-page/|g' {} \;

echo ""

# Deploy to gh-pages branch
ghp-import -n -p -f _site

echo ""
echo "✅ Deployment successful!"
echo ""
echo "📍 Live site: https://fttt-web.github.io/static-page/"
echo ""
echo "Note: Changes may take a few moments to appear on GitHub Pages"
