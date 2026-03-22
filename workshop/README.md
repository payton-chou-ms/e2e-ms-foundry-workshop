# Workshop 文件

此資料夾包含 Foundry IQ + Fabric IQ Workshop 的 MkDocs 文件。

## 唯一內容來源

請將 `workshop/docs/` 視為所有面向使用者的 workshop 內容之唯一主要來源。

- `workshop/site/` 是唯一的建置輸出目錄，供本機 MkDocs build 與 GitHub Pages workflow 共用。
- root `site/` 不再使用，也不應再納入版本控管。
- `guides/` 應只放發佈產生物或審閱備註，而不是同一套教學內容的第二份手寫副本。

## 本機開發

### 安裝相依套件

```bash
pip install -r requirements.txt
```

### 本機啟動

```bash
mkdocs serve
```

啟動後可開啟 [http://127.0.0.1:8000](http://127.0.0.1:8000) 預覽。

### 建置靜態網站

```bash
mkdocs build
```

輸出會位於 `workshop/site/` 資料夾。

## 部署到 GitHub Pages

GitHub Pages 以 `.github/workflows/deploy-docs.yml` 自動建置與部署 `workshop/site/`。

如果要在本機手動部署到 `gh-pages` branch，可執行：

```bash
mkdocs gh-deploy
```

此命令會建置網站並推送到 `gh-pages` branch。

## 結構

```
workshop/
├── mkdocs.yml              # MkDocs 設定
├── requirements.txt        # Python 相依套件
├── README.md              # 本檔案
└── docs/
    ├── index.md           # Overview
    ├── 00-get-started/    # 先決條件與 workshop 流程
    ├── 01-deploy/         # 部署方案
    │   ├── index.md
    │   ├── 00-admin-deploy-share.md
    │   ├── 00-participant-run-validate.md
    │   ├── 01-deploy-azure.md
    │   ├── 02-setup-fabric.md
    │   ├── 03-configure.md
    │   └── 04-run-scenario.md
    ├── 02-customize/      # 依客戶情境自訂
    │   ├── index.md
    │   ├── 02-generate.md
    │   └── 03-demo.md
    ├── 03-understand/     # 技術理解與 deep dive
    │   ├── index.md
    │   ├── 00-foundry-model.md
    │   ├── 01-foundry-iq.md
    │   ├── 02-foundry-agent.md
    │   ├── 02-fabric-iq.md
    │   ├── 03-foundry-tool.md
    │   ├── 04-control-plane.md
    │   └── 05-multi-agent-extension.md
    └── 04-cleanup/        # 清理與下一步
```
