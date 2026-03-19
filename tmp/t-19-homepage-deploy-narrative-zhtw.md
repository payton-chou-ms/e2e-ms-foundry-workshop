# T-19 首頁與部署頁敘事更新紀錄

## 產出

- `README.md`
- `workshop/docs/index.md`
- `workshop/docs/01-deploy/index.md`

## 完成內容

- 將入口敘事從單純 `Foundry IQ + Fabric IQ` 雙主軸，擴展為「主流程維持簡潔、技術架構已延伸成五主軸」
- 在 `README.md` 補上五主軸架構區塊，說明 Model / Agent / Tool / IQ / Control Plane 的角色
- 在 `workshop/docs/index.md` 補上「What stays simple vs what gets deeper」與 architecture talking path
- 在 `workshop/docs/01-deploy/index.md` 補上 main workshop path 與 five-axis architecture 的雙層說法
- 保留主流程仍以單一 prompt agent、兩個 core tools、兩條 grounding path 為中心

## 驗證

- Markdown diagnostics clean
- `python3 -m mkdocs build --config-file /workspaces/nc-iq-workshop/workshop/mkdocs.yml` 可通過