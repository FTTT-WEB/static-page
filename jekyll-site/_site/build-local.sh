#!/bin/bash
# build-local.sh
# Build Jekyll site for local development with empty baseurl
# Usage: ./build-local.sh

set -e

cd "$(dirname "$0")" || exit 1

echo "🔨 Building Jekyll site for local development..."
echo "   Config: _config.yml + _config.local.yml"
echo "   Baseurl: (empty)"
echo ""

rm -rf _site
bundle exec jekyll build --config _config.yml,_config.local.yml

if [ -f "_site/index.html" ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📍 Site ready at: jekyll-site/_site/"
    echo ""
    echo "Next steps:"
    echo "  1. View locally: bundle exec jekyll serve"
    echo "  2. Check: http://localhost:4000/"
else
    echo "❌ Build failed"
    exit 1
fi
