# Jekyll Configuration Guide

## Overview

This project uses a dual-mode Jekyll setup with clean script separation:
1. **Local Development** - `./deploy-local.sh` with `/assets` paths
2. **GitHub Pages Deployment** - `./deploy-pages.sh` with `/static-page/assets` paths

## Configuration Files

**`_config.yml`** (Base Configuration - Shared)
- `title`, `url`, `markdown`, `permalink`, `exclude`
- No baseurl defined here

**`_config.local.yml`** (Local Development)
- `baseurl: ""` (empty for localhost)
- Loaded with: `--config _config.yml,_config.local.yml`

**`_config.pages.yml`** (GitHub Pages)
- `baseurl: /static-page` (for subdirectory deployment)
- Loaded with: `--config _config.yml,_config.pages.yml`

## Build & Deploy Scripts

### build-local.sh
Builds site with local configuration (`baseurl: ""`).
```bash
./build-local.sh
```
- Removes old `_site/`
- Builds with `_config.yml,_config.local.yml`
- Output: `_site/` with paths like `/assets/`

### deploy-local.sh
Builds locally and starts Jekyll server.
```bash
./deploy-local.sh
```
- Runs `build-local.sh`
- Starts `bundle exec jekyll serve` with local config
- Available at: `http://localhost:4000/`

### build-pages.sh
Builds site with GitHub Pages configuration (`baseurl: /static-page`).
```bash
./build-pages.sh
```
- Removes old `_site/`
- Builds with `_config.yml,_config.pages.yml`
- Output: `_site/` with paths like `/static-page/assets/`

### deploy-pages.sh
Deploys to GitHub Pages gh-pages branch.
```bash
./deploy-pages.sh
```
- Checks if site is built; if not, runs `build-pages.sh`
- Runs `ghp-import -n -p -f _site`
- Publishes to: `https://fttt-web.github.io/static-page/`

## Workflow Comparison

| Task | Script | baseurl | Asset Paths | URLs |
|------|--------|---------|-------------|------|
| Local Dev | `./deploy-local.sh` | "" | `/assets/` | `http://localhost:4000/{page}/` |
| Local Build | `./build-local.sh` | "" | `/assets/` | `file://_site/{page}/` |
| GitHub Build | `./build-pages.sh` | `/static-page` | `/static-page/assets/` | `https://fttt-web.github.io/static-page/{page}/` |
| GitHub Deploy | `./deploy-pages.sh` | `/static-page` | `/static-page/assets/` | `https://fttt-web.github.io/static-page/{page}/` |

## File Structure

```
jekyll-site/
├── _config.yml                 # Base config (title, url, etc.)
├── _config.local.yml           # Local override (baseurl: "")
├── _config.pages.yml           # GitHub Pages override (baseurl: /static-page)
├── build-local.sh              # Build for local dev
├── build-pages.sh              # Build for GitHub Pages
├── deploy-local.sh             # Build + serve locally
├── deploy-pages.sh             # Deploy to GitHub Pages
├── index.md                    # Home page
├── *.md                        # Content pages
├── _layouts/
│   └── default.html            # Master layout
├── assets/
│   ├── images/
│   ├── theme/
│   └── wp-includes-js/
└── _site/                      # Generated output (git-ignored)
```

## Key Design Properties

✅ **Single source truth** - One set of markdown files  
✅ **No path conflicts** - Different configs for each build  
✅ **Clean separation** - Distinct scripts for local vs. deploy  
✅ **Easy maintenance** - Config changes in one place  
✅ **Standard Jekyll** - No custom builders needed  

## Troubleshooting

### Local pages show 404s
- Ensure baseurl is empty in `_config.local.yml`
- Clear cache: `rm -rf _site && ./build-local.sh`

### GitHub Pages shows 404s
- Ensure baseurl is `/static-page` in `_config.pages.yml`
- Use `./deploy-pages.sh` (not manual commands)

### Scripts not executable
```bash
chmod +x build-local.sh build-pages.sh deploy-local.sh deploy-pages.sh
```

### Changes not visible after deploy
- Rebuild and redeploy: `./deploy-pages.sh`
- GitHub Pages may take 1-2 minutes to update

## References

- [Jekyll Docs](https://jekyllrb.com/docs/)
- [Multiple Config Files](https://jekyllrb.com/docs/configuration/options/#configuration-file-locations)
- [GitHub Pages Deployment](https://jekyllrb.com/docs/github-pages/)
