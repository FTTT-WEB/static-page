# FTTT 訓練中心網站

靜態 Jekyll 網站，由 WordPress 遷移而來。使用 Markdown 管理內容，支援本地開發和 GitHub Pages 部署。

**目錄**
1. [快速開始](#快速開始)
2. [專案架構](#專案架構)
3. [開發指南](#開發指南)
4. [測試與部署](#測試與部署)

---

## 快速開始

### 系統需求

- Ruby 3.1+ (建議使用 rbenv 管理)
- Git

### 環境配置

#### macOS

使用 Homebrew 和 rbenv 安裝 Ruby：

```bash
# 1. 安裝 rbenv 和 ruby-build
brew install rbenv ruby-build

# 2. 初始化 rbenv
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

# 3. 安裝 Ruby 3.1+
rbenv install 3.1.0
rbenv global 3.1.0

# 4. 驗證安裝
ruby --version
```

#### WSL/Ubuntu

使用 Git 和手動配置安裝 Ruby：

```bash
# 1. 複製 rbenv 和 ruby-build
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build

# 2. 設定環境變數
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init - bash)"' >> ~/.bashrc
source ~/.bashrc

# 3. 安裝 Ruby 3.1+
rbenv install 3.1.0
rbenv global 3.1.0

# 4. 驗證安裝
ruby --version
```

### 專案初始化

```bash
# 1. 複製專案
git clone https://github.com/FTTT-WEB/static-page.git
cd static-page/jekyll-site

# 2. 安裝依賴
bundle install

# 3. 準備完成！
```

---

## 專案架構

```
static-page/
├── jekyll-site/                    # Jekyll 網站主目錄
│   ├── _config.yml                 # 基礎配置
│   ├── _config.local.yml           # 本地開發配置 (baseurl: "")
│   ├── _config.pages.yml           # GitHub Pages 配置 (baseurl: /static-page)
│   │
│   ├── _layouts/
│   │   └── default.html            # 主頁面模板（包含 header、footer、CSS）
│   │
│   ├── _includes/
│   │   ├── header.html             # 頁面頭部（導航選單）
│   │   └── footer.html             # 頁面底部（版權資訊）
│   │
│   ├── assets/
│   │   ├── css/
│   │   │   └── main.css            # 主樣式表
│   │   ├── js/
│   │   │   └── main.js             # 主 JavaScript
│   │   └── images/                 # 所有圖片（logo、頁面圖片等）
│   │
│   ├── *.md                        # 頁面內容（Markdown 格式）
│   │   ├── index.md                # 首頁
│   │   ├── 關於訓練.md
│   │   ├── 訓練沿革.md
│   │   └── ... 其他頁面
│   │
│   ├── build-local.sh              # 本地開發建置腳本
│   ├── build-pages.sh              # GitHub Pages 建置腳本
│   ├── deploy-local.sh             # 本地開發 + 啟動伺服器
│   └── deploy-pages.sh             # GitHub Pages 建置 + 部署
│
├── page_backups/                   # 舊版 HTML 頁面備份
└── README.md                       # 本檔案
```

### 配置檔說明

| 檔案 | 用途 | baseurl |
|------|------|---------|
| `_config.yml` | 共通設定 | - |
| `_config.local.yml` | 本地開發覆蓋 | `""` (無) |
| `_config.pages.yml` | GitHub Pages 覆蓋 | `/static-page` |

Jekyll 會自動合併配置檔，選定的配置會覆蓋基礎設定。

---

## 開發指南

### 建立新頁面

#### 步驟 1：建立 Markdown 檔案

在 `jekyll-site/` 目錄（根目錄）建立新的 `.md` 檔案：

```bash
# 例如：
touch jekyll-site/新頁面名稱.md
```

**檔案命名規則：**
- 使用繁體中文或英文
- 避免特殊字元（`?`, `#`, `&` 等）
- 檔案名稱會成為網址的一部分

#### 步驟 2：加入 Front Matter

在檔案開頭加入 YAML 前置資料：

```markdown
---
layout: default
title: 頁面標題
---

# 頁面主標題

這是您的內容...
```

**Front Matter 說明：**
- `layout: default` - 使用預設頁面模板（必須）
- `title:` - 頁面標題，顯示在瀏覽器標籤和 meta 標籤中

#### 步驟 3：撰寫內容

使用 Markdown 語法撰寫頁面內容：

```markdown
# 一級標題

## 二級標題

### 三級標題

**粗體文字** 和 *斜體文字*

- 項目 1
- 項目 2

1. 第一項
2. 第二項

[連結文字](https://example.com)

![圖片說明](/assets/images/檔名.png)

> 引用文字

| 欄位 1 | 欄位 2 |
|--------|--------|
| 資料 1 | 資料 2 |
```

#### 步驟 4：加入導航選單（選用）

編輯 `jekyll-site/_includes/header.html`，在適當位置加入新選單項目：

```html
<li class="menu-item"><a href="{{ site.baseurl }}/頁面名稱/">頁面顯示名稱</a></li>
```

範例（新增副選單項目）：
```html
<li class="menu-item menu-item-has-children">
  <a href="{{ site.baseurl }}/父頁面/">父頁面</a>
  <ul class="sub-menu">
    <li class="menu-item"><a href="{{ site.baseurl }}/子頁面/">子頁面</a></li>
  </ul>
</li>
```

### 更新頁面內容

1. 編輯對應的 `.md` 檔案
2. 保存後，本地伺服器會自動重新構建
3. 刷新瀏覽器查看變更

### 更新頁面樣式和布局

#### 修改 CSS

編輯 `jekyll-site/assets/css/main.css`（全站樣式）或 `jekyll-site/_layouts/default.html` 中的 `<style>` 區塊（內聯樣式）。

#### 修改 HTML 布局

- **頁面結構：** 編輯 `jekyll-site/_layouts/default.html`
- **頁面頭部：** 編輯 `jekyll-site/_includes/header.html`
- **頁面底部：** 編輯 `jekyll-site/_includes/footer.html`

修改後執行本地測試（見下一節）。

### 管理圖片

1. 將圖片放在 `jekyll-site/assets/images/` 目錄
2. 在 Markdown 中引用：
   ```markdown
   ![圖片說明](/assets/images/檔名.png)
   ```
3. 支援格式：PNG、JPG、GIF、SVG 等

### 嵌入 YouTube 影片

在 Markdown 中使用 iframe：

```html
<iframe width="100%" height="480"
  src="https://www.youtube.com/embed/影片ID"
  title="影片標題"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen>
</iframe>
```

---

## 測試與部署

### 本地開發

#### 方法 1：快速啟動（建議）

```bash
cd jekyll-site
bash deploy-local.sh
```

這會執行以下操作：
1. 使用本地配置構建站點（`baseurl` 為空）
2. 啟動 Jekyll 開發伺服器

然後訪問：`http://localhost:4000/`

#### 方法 2：分步操作

```bash
cd jekyll-site

# 僅構建（不啟動伺服器）
bash build-local.sh

# 啟動伺服器
bundle exec jekyll serve --config _config.yml,_config.local.yml
```

#### 監看檔案變更

啟動伺服器後，任何檔案變更都會自動重新構建。刷新瀏覽器查看。

### GitHub Pages 部署

#### 前置準備

- 確保 repository 名稱為 `static-page`
- 確保 GitHub Pages 設定為 `gh-pages` 分支

#### 部署步驟

```bash
cd jekyll-site

# 方法 1：一鍵部署（推薦）
bash deploy-pages.sh

# 方法 2：分步操作
bash build-pages.sh          # 使用 /static-page baseurl 構建
# 手動審查 _site/ 目錄
gh-import -n -p -f _site     # 部署到 gh-pages 分支
```

部署後訪問：`https://fttt-web.github.io/static-page/`

### 構建腳本說明

| 腳本 | 用途 | baseurl | 伺服器 |
|------|------|---------|--------|
| `build-local.sh` | 本地構建 | `` (空) | ❌ |
| `deploy-local.sh` | 本地開發 | `` (空) | ✅ |
| `build-pages.sh` | GitHub Pages 構建 | `/static-page` | ❌ |
| `deploy-pages.sh` | GitHub Pages 部署 | `/static-page` | ❌ |

### 常見問題

**Q: 為什麼本地和 GitHub Pages 需要不同的 baseurl？**

A: 本地開發時網站在根目錄 (`http://localhost:4000/`)，但 GitHub Pages 在子目錄 (`https://fttt-web.github.io/static-page/`)。不同的 baseurl 確保所有路徑（CSS、JS、圖片、連結）都能正確加載。

**Q: 修改後頁面沒有變更？**

A:
1. 確認本地伺服器正在運行
2. 檢查終端是否有構建錯誤
3. 強制刷新瀏覽器（Cmd+Shift+R 或 Ctrl+Shift+R）
4. 檢查檔案編碼為 UTF-8

**Q: 如何預覽部署到 GitHub Pages 後的效果？**

A:
```bash
bash build-pages.sh
bundle exec jekyll serve --config _config.yml,_config.pages.yml --baseurl /static-page
```

然後訪問 `http://localhost:4000/static-page/`

---

## 參考資源

- [Jekyll 官方文件](https://jekyllrb.com/docs/)
- [Markdown 語法指南](https://guides.github.com/features/mastering-markdown/)
- [GitHub Pages 說明](https://docs.github.com/en/pages)
