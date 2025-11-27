# Jekyll Site Deployment & Usage Guide

## 🎯 Quick Start

Your WordPress site has been converted to a static Jekyll site with 20 pages. Here's how to use it:

## 🚀 Deployment Options

### **Option 1: GitHub Pages (Recommended)**

Perfect for free, automatic hosting:

1. Create a GitHub repository
2. Push the `jekyll-site` folder contents to the repo
3. Enable GitHub Pages in repository settings
4. Your site will be live at `https://username.github.io/repository-name`

```bash
cd jekyll-site
git init
git add .
git commit -m "Initial Jekyll site"
git remote add origin https://github.com/username/your-repo.git
git push -u origin main
```

### **Option 2: Local Jekyll Server (Development)**

Requires Ruby and Jekyll installed:

```bash
cd jekyll-site
bundle install
jekyll serve
# Visit http://localhost:4000
```

### **Option 3: Python Fallback Build (No Ruby needed)**

```bash
cd /Users/bird/Code/fttt/static-page
python3 jekyll-site/fallback_build.py
# Opens jekyll-site/_site with static HTML files
```

### **Option 4: Traditional Web Hosting**

1. Build the site locally: `jekyll build`
2. Upload the `_site/` folder to your web server
3. Point your domain to the `_site` directory

## 📁 Directory Guide

```
jekyll-site/
├── _config.yml              # Site configuration (title, baseurl, etc)
├── _layouts/
│   └── default.html         # Master layout (header, footer, styles)
├── pages/                   # All content pages (20 .md files)
├── assets/                  # CSS, JS, images, fonts
├── _site/                   # Generated static site (after build)
└── Gemfile                  # Ruby dependencies (if using Jekyll)
```

## ✏️ Editing Content

### **To Edit an Existing Page:**

1. Open the `.md` file in `jekyll-site/pages/`
2. Edit the Markdown content (keep the front matter intact)
3. Rebuild/redeploy the site

Example: `jekyll-site/pages/關於訓練.md`

```markdown
---
layout: default
title: 關於訓練 – 臺灣福音工作全時間訓練網站
---

# Your content here
```

### **To Add a New Page:**

1. Create a new `.md` file in `jekyll-site/pages/`
2. Add front matter at the top:

```markdown
---
layout: default
title: Your Page Title
---

# Your content here
```

3. Rebuild/redeploy

## 🎨 Customizing the Design

### **Change the Layout:**

Edit `jekyll-site/_layouts/default.html` to modify:
- Header HTML
- Footer content
- CSS/JavaScript includes
- Meta tags

### **Add Custom CSS:**

1. Create `jekyll-site/assets/custom.css`
2. Link it in `_layouts/default.html`:

```html
<link rel="stylesheet" href="/assets/custom.css">
```

### **Change Site Settings:**

Edit `jekyll-site/_config.yml`:

```yaml
title: Your Site Title
baseurl: ""  # For subdirectories, use "/path"
url: "https://yoursite.com"
```

## 📦 Backup Files

All original WordPress pages are saved in:
- `/Users/bird/Code/fttt/static-page/page_backups/`

These are for reference only. If you need to convert specific content again, they're available.

## 🔗 File Mapping

| Jekyll File | Original WordPress URL |
|---|---|
| home.md | https://www.fttt.org.tw/ |
| 關於訓練.md | https://www.fttt.org.tw/?page_id=125 |
| 訓練沿革.md | https://www.fttt.org.tw/?page_id=87 |
| 訓練目的與目標.md | https://www.fttt.org.tw/?page_id=86 |
| 課程介紹.md | https://www.fttt.org.tw/?page_id=85 |
| 訓練生活.md | https://www.fttt.org.tw/?page_id=89 |
| 訓練八方面.md | https://www.fttt.org.tw/?page_id=52 |
| 職事.md | https://www.fttt.org.tw/?page_id=60 |
| 真理.md | https://www.fttt.org.tw/?page_id=61 |
| 生命.md | https://www.fttt.org.tw/?page_id=62 |
| 事奉.md | https://www.fttt.org.tw/?page_id=63 |
| 基督的身體.md | https://www.fttt.org.tw/?page_id=64 |
| 性格.md | https://www.fttt.org.tw/?page_id=70 |
| 心志.md | https://www.fttt.org.tw/?page_id=71 |
| 語言.md | https://www.fttt.org.tw/?page_id=72 |
| 參加訓練.md | https://www.fttt.org.tw/?page_id=5016 |
| 參加青職短期訓練.md | https://www.fttt.org.tw/?page_id=6871 |
| 訓練負擔.md | https://www.fttt.org.tw/?page_id=4182 |
| 影音專區.md | https://www.fttt.org.tw/?page_id=120 |
| 2025冬季福音開展.md | https://www.fttt.org.tw/?page_id=5147 |

## 🛠️ Troubleshooting

### **Pages not generating?**
- Ensure YAML front matter is correct (3 dashes above and below)
- Check for proper indentation in `_config.yml`
- Run `jekyll build --verbose` for detailed errors

### **CSS/Images not showing?**
- Verify asset paths in `_layouts/default.html`
- Check that files exist in `assets/` directory
- Use relative paths: `/assets/image.png`

### **Chinese characters not displaying?**
- Ensure `_config.yml` has UTF-8 encoding
- Check HTML meta charset: `<meta charset="utf-8">`
- Both are already configured in your site

## 📊 Site Performance

- **Total Pages:** 20
- **Backup Size:** 808 KB
- **Generated Site Size:** ~200 KB (without assets)
- **Load Time:** Fast (static files)
- **SEO:** Full control over metadata

## 🔐 Security

Static Jekyll sites are inherently more secure because:
- No database
- No server-side code execution
- Harder to hack
- Easy to version control with Git

## 📚 Additional Resources

- [Jekyll Official Docs](https://jekyllrb.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [YAML Syntax](https://yaml.org/spec/1.2/spec.html)
- [GitHub Pages Help](https://docs.github.com/en/pages)

## 💡 Pro Tips

1. **Version Control:** Use Git to track changes
   ```bash
   git init jekyll-site
   git add .
   git commit -m "Initial conversion"
   ```

2. **Automated Deployment:** Set up GitHub Actions for auto-deployment
3. **CDN:** Use Cloudflare for faster global distribution
4. **Analytics:** Add Google Analytics code to `_layouts/default.html`
5. **Comments:** Integrate Disqus or other comment systems

## 🆘 Support

For issues or questions:
1. Check Jekyll documentation
2. Review the Markdown syntax in existing pages
3. Verify file structure matches the template
4. Use the backup HTML files to compare original content

---

**Your Jekyll site is ready to deploy!** 🎉

Start with Option 1 (GitHub Pages) for the easiest hosting, or Option 3 (Python build) for local testing.
