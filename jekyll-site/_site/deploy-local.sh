#!/bin/bash
# deploy-local.sh
# Run Jekyll server locally for development and testing
# Usage: ./deploy-local.sh

cd "$(dirname "$0")" || exit 1

# Build first
./build-local.sh

echo ""
echo "=================================="
echo "Starting Jekyll server..."
echo "=================================="
echo ""
echo "📍 Local site: http://localhost:4000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

bundle exec jekyll serve --config _config.yml,_config.local.yml
