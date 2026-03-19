# T-17 Deep Dive Overview 重寫紀錄

## 產出

- `workshop/docs/03-understand/index.md`

## 完成內容

- 將 overview 重寫為五主軸導覽：Model、Agent、Tool、Intelligence Layer、Control Plane
- 補上 `control plane -> model -> agent -> tool -> IQ -> data sources` 關係圖
- 新增「How the pages connect」與「Which page answers which question」區塊
- 對齊新頁面連結與目前 Deep Dive 頁面順序

## 驗證

- Markdown diagnostics clean
- `python3 -m mkdocs build --config-file /workspaces/nc-iq-workshop/workshop/mkdocs.yml` 可通過