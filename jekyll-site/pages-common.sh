#!/bin/bash
# Shared helpers for GitHub Pages build/deploy scripts.
# Sourced by build-pages.sh and deploy-pages.sh — not meant to be run directly.

# Read PATH_PREFIX from env, or fall back to Jekyll baseurl in _config.pages.yml.
# Override with env: PATH_PREFIX="" or PATH_PREFIX=/static-page
read_pages_path_prefix() {
  if [ -n "${PATH_PREFIX+x}" ]; then
    printf '%s' "$PATH_PREFIX"
    return
  fi

  local raw
  raw=$(grep -E '^[[:space:]]*baseurl:' _config.pages.yml | head -1 \
    | sed -E 's/^[[:space:]]*baseurl:[[:space:]]*//; s/[[:space:]]+#.*$//; s/[[:space:]]*$//')
  # Strip surrounding quotes
  raw=$(printf '%s' "$raw" | sed -E 's/^["'\'']//; s/["'\'']$//')
  printf '%s' "$raw"
}

# Portable in-place sed (GNU sed and BSD/macOS sed).
sed_inplace() {
  local expression=$1
  shift
  if sed --version >/dev/null 2>&1; then
    sed -i -e "$expression" "$@"
  else
    sed -i '' -e "$expression" "$@"
  fi
}

# Prefix root-absolute asset paths with PATH_PREFIX when needed.
# Safe for both subdirectory (/static-page) and root (empty) deployments.
# No-op when PATH_PREFIX is empty. Idempotent when paths already include the prefix
# (Jekyll {{ site.baseurl }} already rewrote them).
fix_asset_paths() {
  local path_prefix=$1
  local site_dir=${2:-_site}

  if [ -z "$path_prefix" ]; then
    echo "PATH_PREFIX is empty — skipping asset path prefixing (root-domain deploy)."
    return
  fi

  # Normalize: ensure leading slash, no trailing slash
  path_prefix="/${path_prefix#/}"
  path_prefix="${path_prefix%/}"

  echo "Fixing image paths for PATH_PREFIX: ${path_prefix}"
  while IFS= read -r -d '' file; do
    sed_inplace "s|src=\"/assets/|src=\"${path_prefix}/assets/|g" "$file"
    sed_inplace "s|src=\"/wp-content/|src=\"${path_prefix}/wp-content/|g" "$file"
    sed_inplace "s|src=\"${path_prefix}//|src=\"${path_prefix}/|g" "$file"
  done < <(find "$site_dir" -name '*.html' -print0)
}

# Human-readable live URL for the current PATH_PREFIX.
pages_live_url() {
  local path_prefix=$1
  if [ -z "$path_prefix" ]; then
    printf 'https://www.fttt.org.tw/'
  else
    path_prefix="/${path_prefix#/}"
    path_prefix="${path_prefix%/}"
    printf 'https://fttt-web.github.io%s/' "$path_prefix"
  fi
}
