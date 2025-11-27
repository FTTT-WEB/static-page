# FTTT 訓練中心網站

## Getting Started

1. 安裝 `ruby`。個人推薦使用 `rbenv` 來安裝。 以下為各環境使用 `rbenv` 來安裝 `ruby` 的指令。

```sh
# MacOS
brew install rbenv ruby-build
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

# Linux (若使用 Windows，請安裝 wsl 再使用y)
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init - bash)"' >> ~/.bashrc

git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
source ~/.bashrc
```

2. 安裝 `jekyll` 和 `bundle`。 Jekyll 是個靜態網站產生器，我們只要寫對應的 Markdown 格式就可以建立對應的網站。 Bundler 則是 `ruby` 的依賴管理工具。

```sh
gem install jekyll bundler
bundle init     # 建立 Gemfile
echo 'gem "jekyll"' >> Gemfile  # 將 jekyll 加到 Gemfile 裡面
```

3. 常用指令：

```
bundle exec jekyll serve    # 在本地執行本地伺服器
bundle exec jekyll build    # 生成網站，將所有檔案輸出到 ./_site 目錄中
```

## 📝 如何建立新頁面

本網站使用 Jekyll 靜態網站產生器。以下說明如何建立新頁面：

### 步驟 1: 建立 Markdown 檔案

在 `jekyll-site/pages/` 目錄下建立新的 `.md` 檔案，例如：`新頁面名稱.md`

**檔案命名規則：**

- 使用繁體中文或英文
- 檔案名稱會成為網址的一部分
- 例如：`訓練說明.md` → 網址為 `/pages/訓練說明/`

### 步驟 2: 加入 Front Matter

每個頁面檔案開頭必須包含 Front Matter（YAML 前置資料）：

```markdown
---
layout: default
title: 頁面標題 – 臺灣福音工作全時間訓練網站
---
```

**Front Matter 說明：**

- `layout: default` - 使用預設的頁面模板（必須）
- `title:` - 頁面標題，會顯示在瀏覽器標籤和頁面標題中

### 步驟 3: 撰寫內容

在 Front Matter 下方開始撰寫您的內容，使用 Markdown 語法：

```markdown
---
layout: default
title: 我的新頁面 – 臺灣福音工作全時間訓練網站
---

# 頁面主標題

這是頁面內容的第一段。

## 子標題

更多內容...

### 圖片

![圖片說明](/assets/images/圖片檔名.png)

### YouTube 影片

<iframe width="100%" height="480" src="https://www.youtube.com/embed/影片ID" title="影片標題" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

### 步驟 4: 加入導航選單（選用）

如果需要將新頁面加入網站導航選單，請編輯 `jekyll-site/_layouts/default.html` 檔案，在適當位置加入：

```html
<li class="menu-item"><a href="/pages/頁面名稱.html">選單顯示名稱</a></li>
```

### 步驟 5: 測試頁面

1. **啟動本地伺服器：**

   ```bash
   cd jekyll-site
   bundle exec jekyll serve
   ```

2. **在瀏覽器中查看：**

   - 訪問 `http://localhost:4000/pages/頁面名稱/`
   - 檢查頁面是否正確顯示

3. **檢查錯誤：**
   - 查看終端機是否有錯誤訊息
   - 確認所有圖片和連結路徑正確

### 常用 Markdown 語法

- **標題：** `# 一級標題`、`## 二級標題`、`### 三級標題`
- **粗體：** `**粗體文字**`
- **斜體：** `*斜體文字*`
- **連結：** `[連結文字](網址)`
- **圖片：** `![圖片說明](/assets/images/檔名.png)`
- **列表：**
  ```markdown
  - 項目 1
  - 項目 2
  - 項目 3
  ```
- **編號列表：**
  ```markdown
  1. 第一項
  2. 第二項
  3. 第三項
  ```

### 檔案結構範例

```
jekyll-site/
├── pages/
│   ├── home.md          # 首頁
│   ├── 關於訓練.md      # 現有頁面
│   └── 我的新頁面.md    # 您的新頁面
├── assets/
│   ├── images/          # 圖片檔案放在這裡
│   ├── css/
│   └── js/
└── _layouts/
    └── default.html     # 頁面模板
```

### 注意事項

1. **圖片路徑：** 所有圖片應放在 `assets/images/` 目錄，使用絕對路徑 `/assets/images/檔名.png`
2. **檔案編碼：** 確保檔案使用 UTF-8 編碼
3. **檔案名稱：** 避免使用特殊字元（如 `?`, `#`, `&` 等）
4. **測試：** 每次修改後記得測試，確保頁面正常顯示

### 需要幫助？

- 查看現有頁面範例：`pages/關於訓練.md`、`pages/訓練沿革.md`
- 參考 Jekyll 官方文件：https://jekyllrb.com/docs/
- 檢查 `docs/` 目錄下的其他說明文件
