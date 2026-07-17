# FTTT Jekyll site

## Setup

```bash
bundle install
pip install ghp-import
```

## Develop

```bash
./deploy-local.sh
```

Open <http://localhost:4000/>.

## Deploy

`PATH_PREFIX` selects the deployment path. Build and deploy with the same value:

```bash
# https://www.fttt.org.tw/
PATH_PREFIX="" ./build-pages.sh
PATH_PREFIX="" ./deploy-pages.sh

# https://fttt-web.github.io/static-page/
PATH_PREFIX=/static-page ./build-pages.sh
PATH_PREFIX=/static-page ./deploy-pages.sh
```

If `PATH_PREFIX` is unset, scripts use `baseurl` from `_config.pages.yml`.

## Content

- Pages: Markdown files in this directory and its content subdirectories
- Layout and navigation: `_layouts/default.html` and `_includes/`
- Assets: `assets/`
- Build output: `_site/`

Use the configured path prefix for internal links and images:

```markdown
![說明]({{ site.baseurl }}/assets/images/example.png)
```
