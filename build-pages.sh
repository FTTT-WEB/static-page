#!/bin/bash
# build-pages.sh
# Build Jekyll site for GitHub Pages using PATH_PREFIX (Jekyll baseurl).
#
# Works for both:
#   - subdirectory: PATH_PREFIX=/static-page → https://fttt-web.github.io/static-page/
#   - custom domain root: PATH_PREFIX=""     → https://www.fttt.org.tw/
#
# Override without editing config:
#   PATH_PREFIX="" ./build-pages.sh
#   PATH_PREFIX=/static-page ./build-pages.sh
#
# Usage: ./build-pages.sh

set -e

cd "$(dirname "$0")" || exit 1
# shellcheck source=pages-common.sh
source ./pages-common.sh

PATH_PREFIX=$(read_pages_path_prefix)
LIVE_URL=$(pages_live_url "$PATH_PREFIX")

echo "🔨 Building Jekyll site for GitHub Pages..."
echo "   Config: _config.yml + _config.pages.yml"
if [ -z "$PATH_PREFIX" ]; then
  echo "   PATH_PREFIX: (empty — root domain)"
else
  echo "   PATH_PREFIX: $PATH_PREFIX"
fi
echo ""

rm -rf _site
bundle exec jekyll build \
  --config _config.yml,_config.pages.yml \
  --baseurl "$PATH_PREFIX"

if [ -f "_site/index.html" ]; then
  fix_asset_paths "$PATH_PREFIX" _site

  echo ""
  echo "✅ Build successful!"
  echo ""
  echo "📍 Site ready at: jekyll-site/_site/"
  echo ""
  echo "Next steps:"
  echo "  1. Deploy: ./deploy-pages.sh"
  echo "  2. Check: ${LIVE_URL}"
else
  echo "❌ Build failed"
  exit 1
fi
