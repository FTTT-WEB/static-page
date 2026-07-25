# FTTT 訓練中心網站

由 WordPress 遷移而來的 Jekyll 靜態網站。

## 專案結構

- `jekyll-site/`：網站原始碼、資源與部署腳本
- `scripts/`：遷移及內容轉換工具
- `docs/`：遷移與部署的歷史文件

網站操作細節請見 [`jekyll-site/README.md`](jekyll-site/README.md)。

## 開始使用

```bash
cd jekyll-site
bundle install
pip install ghp-import
./deploy-local.sh
```

本地網站：<http://localhost:4000/>

## 部署

`PATH_PREFIX` 決定網站部署路徑；建置和部署時應使用相同值：

```bash
# https://www.fttt.org.tw/
PATH_PREFIX="" ./build-pages.sh
PATH_PREFIX="" ./deploy-pages.sh

# https://fttt-web.github.io/static-page/
PATH_PREFIX=/static-page ./build-pages.sh
PATH_PREFIX=/static-page ./deploy-pages.sh
```

若未設定 `PATH_PREFIX`，腳本會使用 `_config.pages.yml` 的 `baseurl`。

根網域部署會寫入 `CNAME` 檔案（`www.fttt.org.tw`），確保每次強制推送後 GitHub Pages
自訂網域不會被重設。可用 `PAGES_DOMAIN=example.org` 覆寫。

## 編輯內容

- 頁面：`jekyll-site/` 下的 Markdown 檔案
- 導覽：`jekyll-site/_includes/header.html`
- 樣式：`jekyll-site/assets/css/main.css`
- 圖片：`jekyll-site/assets/images/`

內部連結及圖片應包含 Jekyll 路徑前綴：

```markdown
![圖片說明]({{ site.baseurl }}/assets/images/檔名.png)
```
