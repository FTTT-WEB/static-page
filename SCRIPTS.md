# Shell 腳本說明書

本文件以「使用情境」說明 `jekyll-site/` 目錄下 5 支 `.sh` 腳本的用途與用法。

---

## 情境一：我想在本機開發、即時預覽修改結果

**使用：`./deploy-local.sh`**

```bash
./deploy-local.sh
```

做的事：
1. 自動呼叫 `build-local.sh` 先建置一次網站（baseurl 為空）
2. 啟動 Jekyll 本地伺服器：`bundle exec jekyll serve`
3. 開啟 <http://localhost:4000/> 即可預覽，存檔會自動重新整理

按 `Ctrl+C` 停止伺服器。

---

## 情境二：我只想建置本機版本，不需要啟動伺服器

**使用：`./build-local.sh`**

```bash
./build-local.sh
```

做的事：
- 清除舊的 `_site/` 後重新建置
- 套用 `_config.yml` + `_config.local.yml`（baseurl 為空，適合本機瀏覽）
- 建置成功會提示可用 `bundle exec jekyll serve` 啟動伺服器

適合情境：只想確認網站能不能正常建置、不需要立刻預覽。

---

## 情境三：我要把網站部署到自訂網域（www.fttt.org.tw）

**使用：`build-pages.sh` + `deploy-pages.sh`，`PATH_PREFIX` 設為空字串**

```bash
PATH_PREFIX="" ./build-pages.sh
PATH_PREFIX="" ./deploy-pages.sh
```

做的事：
- `build-pages.sh` 用空的 baseurl 建置網站到 `_site/`
- `deploy-pages.sh` 會將 `_site/` 用 `ghp-import` 強制推送到 `gh-pages` 分支
- 因為是根網域部署，會自動寫入 `CNAME` 檔（預設 `www.fttt.org.tw`），確保自訂網域設定不會被強制推送洗掉
  - 若要換網域：`PAGES_DOMAIN=example.org PATH_PREFIX="" ./deploy-pages.sh`
- 部署完成會印出正式網址：`https://www.fttt.org.tw/`

前置需求：已安裝 `ghp-import`（`pip install ghp-import`）。

---

## 情境四：我要把網站部署到 GitHub Pages 專案子路徑

**使用：`build-pages.sh` + `deploy-pages.sh`，`PATH_PREFIX` 設為 `/static-page`**

```bash
PATH_PREFIX=/static-page ./build-pages.sh
PATH_PREFIX=/static-page ./deploy-pages.sh
```

做的事：
- 與情境三相同，但 baseurl 是 `/static-page`
- 建置後會自動修正頁面中 `/assets/`、`/wp-content/` 開頭的圖片路徑，加上前綴，避免子路徑部署時圖片跑版
- 因為是子路徑部署，**不會**寫入 `CNAME`
- 正式網址：`https://fttt-web.github.io/static-page/`

⚠️ 建置與部署務必使用**相同的 `PATH_PREFIX`**，否則圖片路徑會對不上。

---

## 情境五：我沒特別指定 PATH_PREFIX，直接執行部署腳本

**使用：`./build-pages.sh` 或 `./deploy-pages.sh`（不帶環境變數）**

```bash
./build-pages.sh
./deploy-pages.sh
```

做的事：
- 沒有設定 `PATH_PREFIX` 環境變數時，腳本會自動讀取 `_config.pages.yml` 裡的 `baseurl` 設定值當作預設
- 其餘行為同情境三或情境四，依 `_config.pages.yml` 目前設定的值而定

適合情境：不確定要不要改路徑、只想沿用專案目前設定值部署。

---

## 情境六：我只想建置，晚點再部署

**使用：只跑 `./build-pages.sh`**

```bash
PATH_PREFIX="" ./build-pages.sh   # 或指定其他 PATH_PREFIX
```

建置完成後可以先打開 `_site/index.html` 確認內容，之後再執行 `./deploy-pages.sh`。
若忘記先建置就直接執行 `deploy-pages.sh`，它會偵測 `_site/index.html` 不存在，自動幫你先建置一次。

---

## 附註：pages-common.sh 是什麼？

`pages-common.sh` **不是**直接執行的腳本，而是共用函式庫，被 `build-pages.sh` 和 `deploy-pages.sh` 用 `source` 引入，提供：

- `read_pages_path_prefix`：讀取 `PATH_PREFIX`（環境變數優先，否則讀 `_config.pages.yml`）
- `fix_asset_paths`：修正 HTML 內圖片路徑前綴
- `pages_live_url`：依 `PATH_PREFIX` 組出對應的正式網址
- `sed_inplace`：跨平台（macOS / Linux）相容的 in-place sed

不需要、也不應該直接執行這支腳本。
