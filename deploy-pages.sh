#!/bin/bash
# deploy-pages.sh
# Deploy Jekyll site to GitHub Pages gh-pages branch
# Usage: ./deploy-pages.sh
#
# Prerequisites:
#   - Build site first: ./build-pages.sh
#   - ghp-import installed: pip install ghp-import
#
# Uses the same PATH_PREFIX as build-pages.sh (_config.pages.yml baseurl, or PATH_PREFIX env).
# Works for both /static-page and root custom-domain deploys.
#
# For a root-domain deploy (PATH_PREFIX="") a CNAME file is written so the GitHub
# Pages custom domain survives the force-push. Override the domain with:
#   PAGES_DOMAIN=example.org PATH_PREFIX="" ./deploy-pages.sh

set -e

cd "$(dirname "$0")" || exit 1
# shellcheck source=pages-common.sh
source ./pages-common.sh

PATH_PREFIX=$(read_pages_path_prefix)
LIVE_URL=$(pages_live_url "$PATH_PREFIX")
PAGES_DOMAIN=${PAGES_DOMAIN:-www.fttt.org.tw}

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
if [ -z "$PATH_PREFIX" ]; then
  echo "PATH_PREFIX: (empty — root domain)"
else
  echo "PATH_PREFIX: $PATH_PREFIX"
fi
echo "=================================="
echo ""

# Re-apply in case _site was built earlier or by another tool
fix_asset_paths "$PATH_PREFIX" _site

echo ""

# Deploy to gh-pages branch.
# Root-domain deploy keeps a CNAME file so the custom domain isn't reset by the
# force-push. Subdirectory (project-page) deploy must not carry a CNAME.
if [ -z "$PATH_PREFIX" ]; then
  echo "Writing CNAME: ${PAGES_DOMAIN}"
  ghp-import -n -p -f -c "$PAGES_DOMAIN" _site
else
  ghp-import -n -p -f _site
fi

echo ""
echo "✅ Deployment successful!"
echo ""
echo "📍 Live site: ${LIVE_URL}"
echo ""
echo "Note: Changes may take a few moments to appear on GitHub Pages"
