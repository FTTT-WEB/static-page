# FTTT Static Site - Project Review Report

**Date**: May 25, 2026  
**Review Scope**: 404 errors and broken links/images  
**Current Branch**: feature/updateByAlison (PR #12)

---

## Executive Summary

The project is a Jekyll-based static site for the FTTT training center website. The recent PR (#12) has made progress migrating from WordPress image URLs to Jekyll-compatible paths. However, there are some issues causing 404 errors that need to be fixed.

**Critical Issues Found**: 1  
**Minor Issues Found**: 1+

---

## Issues Found

### 🔴 **CRITICAL: Image Path with Double Slash**
**File**: [jekyll-site/課程介紹.md](jekyll-site/課程介紹.md#L14)  
**Line**: 14  
**Issue**: 
```html
<img src="/assets/images//課表介紹.png" alt="課表介紹">
```
**Problem**: Double slash (`//`) causes incorrect URL resolution  
**Fix**: Remove extra slash:
```html
<img src="/assets/images/課表介紹.png" alt="課表介紹">
```

---

### 🟡 **POTENTIAL: Image Path Absoluteness for GitHub Pages**
**Affected Files**: 
- [jekyll-site/訓練生活.md](jekyll-site/訓練生活.md) (multiple images)
- [jekyll-site/訓練沿革.md](jekyll-site/訓練沿革.md) (multiple images)
- [jekyll-site/課程介紹.md](jekyll-site/課程介紹.md) (multiple images)
- [jekyll-site/訓練目的與目標.md](jekyll-site/訓練目的與目標.md)

**Issue**: Images use absolute paths like `/assets/images/晨興.jpg`
**Context**: Site deploys to GitHub Pages at: `https://fttt-web.github.io/static-page/`  
**baseurl Setting**: Correctly set to `/static-page` in `_config.pages.yml`

**Explanation**: 
- Markdown images with `/assets/...` paths are being rendered as-is in HTML
- The layout template correctly uses `{{ site.baseurl }}` for CSS: `<link rel="stylesheet" href="{{ site.baseurl }}/assets/css/main.css">`
- However, markdown image paths are NOT automatically prefixed with baseurl by Jekyll
- When deployed to GitHub Pages subdirectory, `/assets/images/image.jpg` becomes `https://fttt-web.github.io/assets/images/image.jpg` (WRONG)
- Should be: `https://fttt-web.github.io/static-page/assets/images/image.jpg`

**Current Image Paths in Markdown**:
```markdown
![晨興](/assets/images/晨興.jpg)  ❌ Will 404 on GitHub Pages
```

**Recommended Fix**:
```markdown
![晨興]({{ site.baseurl }}/assets/images/晨興.jpg)  ✅ Correct
```
Or use relative paths:
```markdown
![晨興](/static-page/assets/images/晨興.jpg)  ✅ Also works
```

---

### ✅ **FIXED: Navigation Links**
**Status**: Good progress on PR #12

**What was fixed**:
- Old WordPress page ID links removed/commented out: `/?page_id=265`
- Replaced with proper Jekyll paths:
  - ❌ Old: `<a href="/?page_id=265">文章</a>`
  - ✅ New: `[文章](/性格/性格_關於性格的要點)`

**Files Already Fixed**:
- [jekyll-site/性格.md](jekyll-site/性格.md) - Lines 40-46
- [jekyll-site/基督的身體.md](jekyll-site/基督的身體.md) - Lines 33-36

---

## File Status Summary

| File | Issue | Status |
|------|-------|--------|
| 訓練生活.md | Image paths may 404 on GH Pages | ⚠️ Needs Review |
| 訓練沿革.md | Image paths may 404 on GH Pages | ⚠️ Needs Review |
| 課程介紹.md | Double slash + image paths | 🔴 **Critical** |
| 訓練目的與目標.md | Image paths may 404 on GH Pages | ⚠️ Needs Review |
| 性格.md | Navigation links fixed | ✅ Good |
| 基督的身體.md | Navigation links fixed | ✅ Good |

---

## Configuration Check

**Jekyll Config** (`_config.yml`):
```yaml
permalink: /:name:/  # Generates pages as directories with index.html
```

**GitHub Pages Config** (`_config.pages.yml`):
```yaml
baseurl: /static-page  # ✅ Correct for subdirectory deployment
```

**Generated Site Structure**:
```
_site/
├── index.html
├── 訓練生活/
│   └── index.html
├── 基督的身體/
│   ├── index.html
│   └── 基督身體_基督的身體是召會的內在意義/
│       └── index.html
└── assets/
    └── images/
        ├── 晨興.jpg ✅ All images present
        ├── 運動.jpg
        ├── 整潔.jpg
        └── ... (29 image files total)
```

---

## Recommendations

### Priority 1: Fix Critical Issues
1. **Fix double slash in [jekyll-site/課程介紹.md](jekyll-site/課程介紹.md#L14)**
   - Change `/assets/images//課表介紹.png` to `/assets/images/課表介紹.png`

### Priority 2: Fix Image Paths for GitHub Pages
Use a Jekyll filter/include or convert all markdown images to use baseurl:

**Option A - Edit markdown to use Liquid template syntax** (requires template support):
```markdown
![晨興]({{ site.baseurl }}/assets/images/晨興.jpg)
```

**Option B - Use relative paths** (simpler):
```markdown
![晨興](/static-page/assets/images/晨興.jpg)
```

**Option C - Create a Jekyll custom filter** (most flexible):
```ruby
# _plugins/prepend_baseurl.rb
module Jekyll
  class ImagePathFilter
    def image_url(path)
      "#{@site.config['baseurl']}#{path}"
    end
  end
end
```

### Priority 3: Verify After Fix
After making changes:
1. Run `./build-pages.sh` to rebuild the site
2. Check `_site/` output for correct paths
3. Test locally with: `bundle exec jekyll serve --baseurl /static-page`
4. Deploy and test on GitHub Pages

---

## Local Development vs GitHub Pages

**Local Build** (`build-local.sh`):
- Uses `_config.yml` only
- baseurl is empty (runs at http://localhost:4000/)
- Images at `/assets/images/` work fine

**GitHub Pages Build** (`build-pages.sh`):
- Uses `_config.yml` + `_config.pages.yml`
- baseurl is `/static-page`
- Images at `/assets/images/` will **404** because GitHub Pages serves from `/static-page/`

---

## Next Steps

1. **Fix the double slash** - Quick win ✅
2. **Test image paths** - Run build and verify _site output
3. **Update markdown images** - Use one of the recommended options (B is easiest)
4. **Deploy and validate** - Test on GitHub Pages
5. **Close PR #12** - Once all fixes are verified

---

## Additional Notes

- All 29 expected image files are present in `/assets/images/`
- Jekyll site structure is correctly set up with permalink: /:name:/
- Page generation is working (all 21+ pages build successfully)
- No broken markdown links found (old WordPress ID links already removed)
- Navigation between pages should work after image fixes

