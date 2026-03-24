#!/bin/bash
# build-pages.sh
# Build Jekyll site for GitHub Pages deployment with /static-page baseurl
# Usage: ./build-pages.sh

set -e

cd "$(dirname "$0")" || exit 1

echo "🔨 Building Jekyll site for GitHub Pages..."
echo "   Config: _config.yml + _config.pages.yml"
echo "   Baseurl: /static-page"
echo ""

rm -rf _site
bundle exec jekyll build --config _config.yml,_config.pages.yml

if [ -f "_site/index.html" ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📍 Site ready at: jekyll-site/_site/"
    echo ""
    echo "Next steps:"
    echo "  1. Deploy: ./deploy-pages.sh"
    echo "  2. Check: https://fttt-web.github.io/"
else
    echo "❌ Build failed"
    exit 1
fi
