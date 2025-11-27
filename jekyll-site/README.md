# jekyll-site

This folder contains a Jekyll site with pages converted from the original WordPress site at `www.fttt.org.tw/`.

## Quick Start

### Prerequisites
- Ruby with Bundler (for Jekyll)
- `ghp-import` for GitHub Pages deployment: `pip install ghp-import`

### Local Development

Build and serve locally with **empty baseurl**:

```bash
cd /Users/bird/Code/fttt/static-page/jekyll-site

# One command to build and serve
./deploy-local.sh
```

The site will be available at `http://localhost:4000/` with asset paths like `/assets/...` (no `/static-page` prefix).

**Or separately:**
```bash
# Just build
./build-local.sh

# Then serve manually
bundle exec jekyll serve --config _config.yml,_config.local.yml
```

### Deployment to GitHub Pages

Deploy with one command:

```bash
cd /Users/bird/Code/fttt/static-page/jekyll-site

# Build with /static-page baseurl and deploy
./deploy-pages.sh
```

**Or separately:**
```bash
# Build for GitHub Pages
./build-pages.sh

# Then deploy
./deploy-pages.sh
```

The generated site will have asset paths like `/static-page/assets/...` for GitHub Pages subdirectory.

---

## Project Structure

- **Source pages:** `./*.md` and `index.md` (in root jekyll-site directory)
- **Layout template:** `_layouts/default.html`
- **Assets:** `assets/` (images, CSS, JS)
- **Configuration:**
  - `_config.yml` - Shared configuration
  - `_config.local.yml` - Local development (baseurl: "")
  - `_config.pages.yml` - GitHub Pages (baseurl: /static-page)

---

## Scripts

| Script | Purpose | When to Use |
|--------|---------|------------|
| `build-local.sh` | Build for local dev | Before testing locally |
| `build-pages.sh` | Build for GitHub Pages | Before deploying to GitHub Pages |
| `deploy-local.sh` | Build + serve locally | Testing before deployment |
| `deploy-pages.sh` | Build + deploy to GitHub Pages | Publishing changes |

---

## How to Create / Modify / Delete Pages

### Create a Page

1. **Create the Markdown file** at `jekyll-site/<slug>.md` where `<slug>` is the URL-friendly name

2. **Add YAML front matter:**
   ```yaml
   ---
   layout: default
   title: 頁面標題 – 臺灣福音工作全時間訓練網站
   ---
   ```

3. **Add content** in Markdown format

4. **Build and test:**
   ```bash
   bundle exec jekyll build
   # Open in browser: http://localhost:4000/<slug>/
   ```

### Modify a Page

1. Edit the `.md` file
2. Rebuild: `bundle exec jekyll build`
3. Changes appear in browser after refresh

### Delete a Page

1. Remove the `.md` file
2. Rebuild: `bundle exec jekyll build`
3. Page is removed from the built site

---

## Build Outputs

- **Local development:** `_site/` with paths like `/assets/...`
- **GitHub Pages:** `_site/` with paths like `/static-page/assets/...`

## Typical Workflow

### First Time Setup
```bash
cd jekyll-site
bundle install  # Install Jekyll and dependencies
```

### Daily Development
```bash
cd jekyll-site

# View locally while editing
./deploy-local.sh

# Make changes to .md files, save
# Refresh browser to see changes
```

### Publishing to GitHub Pages
```bash
cd jekyll-site

# Build with GitHub Pages config and deploy
./deploy-pages.sh

# Or if you prefer separate steps:
./build-pages.sh      # Build
./deploy-pages.sh     # Deploy
```

	---
	```

- **Step 3 — Content:**
	- Write Markdown normally. For YouTube embeds include the embed iframe directly:
		```html
		<iframe width="100%" height="480" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>
		```
	- Reference images using absolute paths from the site root, e.g.:
		```markdown
		![alt text](/assets/images/my-image.png)
		```

- **Step 4 — Add assets:**
	- Put images in `jekyll-site/assets/images/` and reference them as `/assets/images/<name>`.

- **Step 5 — Add to navigation (optional):**
	- Edit the HTML navigation in `jekyll-site/_layouts/default.html` and add a new `<li>` link inside the `<nav id="site-navigation">` list.

- **Step 6 — Rebuild & preview:**
	- Run the build and open `http://localhost:8000/<slug>/index.html`.

**Modify a Page**
- Open `jekyll-site/pages/<slug>.md` and edit content as needed.
- If you add or change images, add them to `jekyll-site/assets/images/` and update the image path.
- If you change an iframe or HTML embed, keep using the embed URL `https://www.youtube.com/embed/...`.
- Re-run the fallback build and refresh the browser.

**Delete a Page**
- Remove the source file: `rm jekyll-site/pages/<slug>.md` (or move it to a backup folder).
- Remove the navigation link from `jekyll-site/_layouts/default.html`.
- Optionally remove unused images from `jekyll-site/assets/images/`.
- Re-run the build so `_site/` no longer contains the page.

---

**Validation & testing checklist (post-build)**
- Confirm `_site/<slug>/index.html` exists.
- Open page in browser via `http://localhost:8000/<slug>/index.html`.
- Confirm images load (network tab) and paths are `/assets/images/...`.
- Confirm YouTube embeds display and play.
- Resize the browser (or use DevTools) to verify responsive layout.
- Verify navigation links (header menu) point to correct pages.

**Common troubleshooting**
- If CSS or images do not appear, ensure you're serving with `python -m http.server` from `_site/` (file:// doesn't allow some resources).
- If iframes show placeholders like `YOUTUBEEMBED...YOUTUBEEMBED`, re-run the builder; the builder extracts and restores HTML blocks—placeholders should be replaced.

**Commit & deploy**
- Typical local workflow:
	```bash
	git add jekyll-site/pages/<slug>.md jekyll-site/assets/images/<file> jekyll-site/_layouts/default.html
	git commit -m "Add/Update page: <slug>"
	git push
	```

- Deploy options:
	- Let GitHub Pages build from source (requires Jekyll/Ruby/Gems on CI).
	- Or run the fallback builder locally and push the contents of `_site/` to a branch (e.g., `gh-pages`) that GitHub Pages serves.
