# T-18 MkDocs 導覽更新紀錄

## 產出

- `workshop/mkdocs.yml`

## 完成內容

- 將 Deep Dive 導覽順序調整為更貼近五主軸敘事
- 將 `Foundry Agent`、`Foundry Tool` 提前到 `Foundry IQ` 之前，對齊 `model -> agent -> tool -> IQ -> control plane` 的閱讀節奏
- 保持頁面標題與現有文件標題一致，避免導覽與頁面命名漂移

## 驗證

- YAML diagnostics clean
- `python3 -m mkdocs build --config-file /workspaces/nc-iq-workshop/workshop/mkdocs.yml` 可通過