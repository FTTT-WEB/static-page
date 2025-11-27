# ✅ Jekyll Setup Complete - Summary

Your Jekyll site is now fully configured with **clean, easy-to-use scripts** for both local development and GitHub Pages deployment. Here's what was set up:

## What Was Changed

### 1. **Configuration Files** ⚙️
- **`_config.yml`** - Base config (title, url, markdown settings)
- **`_config.local.yml`** - Local dev override (`baseurl: ""`)
- **`_config.pages.yml`** - GitHub Pages override (`baseurl: /static-page`)

### 2. **Build & Deploy Scripts** 🛠️
Four simple scripts handle all workflows:

| Script | Purpose |
|--------|---------|
| `build-local.sh` | Build for local development |
| `build-pages.sh` | Build for GitHub Pages |
| `deploy-local.sh` | Build + serve locally |
| `deploy-pages.sh` | Build + deploy to GitHub Pages |

### 3. **Updated Documentation** 📚
- **`README.md`** - Quick start with new scripts
- **`JEKYLL_CONFIG.md`** - Technical configuration reference

## Three Main Workflows

### 🚀 Local Development (Test Before Publishing)
```bash
cd jekyll-site
./deploy-local.sh
```

**What it does:**
- Builds site with `baseurl: ""`
- Starts Jekyll server
- Opens at `http://localhost:4000/`

**Asset paths:** `/assets/` (no /static-page prefix)

### 🚀 Build for GitHub Pages (Manual Deployment)
```bash
cd jekyll-site
./build-pages.sh
```

**What it does:**
- Builds site with `baseurl: /static-page`
- Outputs to `_site/` directory
- Ready for manual deployment

**Asset paths:** `/static-page/assets/`

### 🚀 Deploy to GitHub Pages (One Command)
```bash
cd jekyll-site
./deploy-pages.sh
```

**What it does:**
- Builds site with `baseurl: /static-page`
- Deploys to GitHub Pages gh-pages branch
- Live at `https://fttt-web.github.io/static-page/`

**Asset paths:** `/static-page/assets/`

## Configuration Details

### _config.yml (Shared)
Contains all common settings:
```yaml
title: FTTT Static Clone
url: ""
markdown: kramdown
permalink: /:name:/
exclude: [Gemfile, Gemfile.lock, README.md, ...]
```

### _config.local.yml (Local Dev)
```yaml
baseurl: ""
```

### _config.pages.yml (GitHub Pages)
```yaml
baseurl: /static-page
```

## Script Behavior

### build-local.sh
```bash
./build-local.sh
# → Removes _site/
# → Builds with _config.yml + _config.local.yml
# → Asset paths: /assets/
```

### deploy-local.sh
```bash
./deploy-local.sh
# → Runs build-local.sh
# → Starts: bundle exec jekyll serve
# → Available: http://localhost:4000/
```

### build-pages.sh
```bash
./build-pages.sh
# → Removes _site/
# → Builds with _config.yml + _config.pages.yml
# → Asset paths: /static-page/assets/
```

### deploy-pages.sh
```bash
./deploy-pages.sh
# → Checks if _site/ exists (if not, runs build-pages.sh)
# → Runs: ghp-import -n -p -f _site
# → Live: https://fttt-web.github.io/static-page/
```

## File Organization

```
jekyll-site/
├── _config.yml              # Shared config
├── _config.local.yml        # Local override
├── _config.pages.yml        # GitHub Pages override
├── build-local.sh           # Build locally
├── build-pages.sh           # Build for GitHub Pages
├── deploy-local.sh          # Serve locally
├── deploy-pages.sh          # Deploy to GitHub Pages
├── index.md                 # Home page
├── *.md                     # Content pages
├── _layouts/
│   └── default.html         # Master layout
├── assets/
│   ├── images/
│   ├── theme/
│   └── wp-includes-js/
└── _site/                   # Generated output
```

## Typical Workflow

### First Time Setup
```bash
cd jekyll-site
bundle install  # Install dependencies
```

### Daily Development
```bash
cd jekyll-site
./deploy-local.sh

# Make changes to .md files
# Refresh browser to see changes
# Press Ctrl+C to stop server
```

### Publishing Changes
```bash
cd jekyll-site
./deploy-pages.sh

# Deployed! Check: https://fttt-web.github.io/static-page/
```

## Key Features

✅ **Separate scripts** - Clear purpose for each command  
✅ **Separate configs** - No manual baseurl switching  
✅ **Single source** - One set of markdown files  
✅ **No path conflicts** - Different paths for local vs. GitHub Pages  
✅ **Fully documented** - Each script has inline help  
✅ **Easy to remember** - Logical naming and workflow  

## Important Notes

⚠️ **Always use the scripts** - Don't run raw Jekyll commands  
⚠️ **Keep pages in root** - All `.md` files in `jekyll-site/` directory  
⚠️ **One config per environment** - Use `_config.local.yml` for local, `_config.pages.yml` for deployment  

## Reference Files

- **Config files:** `jekyll-site/_config*.yml`
- **Build scripts:** `jekyll-site/build-*.sh`
- **Deploy scripts:** `jekyll-site/deploy-*.sh`
- **Documentation:** `jekyll-site/README.md` and `JEKYLL_CONFIG.md`

---

**Ready to go!** 🎉 Your site is fully configured with simple, easy-to-remember commands for both local development and GitHub Pages deployment.
