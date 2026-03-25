# 使用 Solution Accelerators 更快建構方案 – Foundry IQ + Fabric IQ（Workshop）

這個 repo 提供一套實作型 workshop，示範如何建構能同時回答**文件問題**與**資料問題**的 AI PoC。

正式使用者文件一律以 `workshop/docs/` 為主；這份 README 只保留 repo 入口、適用對象與開始路徑。

## 開啟 Workshop


[![Open in GitHub Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue?logo=github)](https://codespaces.new/payton-chou-ms/e2e-ms-foundry-workshop)
[![Open in VS Code](https://img.shields.io/badge/VS%20Code-Dev%20Containers-blue?logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/payton-chou-ms/e2e-ms-foundry-workshop)
[![GitHub Repository](https://img.shields.io/badge/GitHub-e2e--ms--foundry--workshop-181717?logo=github)](https://github.com/payton-chou-ms/e2e-ms-foundry-workshop)
[![Open in VS Code Web](https://img.shields.io/badge/VS%20Code-Open%20in%20Web-blue?logo=visualstudiocode)](https://vscode.dev/azure/?vscode-azure-exp=foundry&agentPayload=eyJiYXNlVXJsIjogImh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9wYXl0b24tY2hvdS1tcy9lMmUtbXMtZm91bmRyeS13b3Jrc2hvcC9tYWluL2luZnJhL3ZzY29kZV93ZWIiLCAiaW5kZXhVcmwiOiAiL2luZGV4Lmpzb24iLCAidmFyaWFibGVzIjogeyJhZ2VudElkIjogIiIsICJjb25uZWN0aW9uU3RyaW5nIjogIiIsICJ0aHJlYWRJZCI6ICIiLCAidXNlck1lc3NhZ2UiOiAiIiwgInBsYXlncm91bmROYW1lIjogIiIsICJsb2NhdGlvbiI6ICIiLCAic3Vic2NyaXB0aW9uSWQiOiAiIiwgInJlc291cmNlSWQiOiAiIiwgInByb2plY3RSZXNvdXJjZUlkIjogIiIsICJlbmRwb2ludCI6ICIifSwgImNvZGVSb3V0ZSI6IFsiYWktcHJvamVjdHMtc2RrIiwgInB5dGhvbiIsICJkZWZhdWx0LWF6dXJlLWF1dGgiLCAiZW5kcG9pbnQiXX0=)

---

## 適合誰

- 想快速跑通 Foundry IQ + Fabric IQ 的實作 PoC
- 想把預設情境換成自己的產業與使用案例
- 想用這個 repo 做 workshop、demo 或技術 deep dive

## 從哪裡開始

請依你現在的目的，直接走下面三條入口之一：

| 目的 | 從這裡開始 |
|------|--------------|
| 想先理解 workshop 主線與學習順序 | `workshop/docs/index.md` |
| 需要自己部署 Azure 與 Fabric 環境 | `workshop/docs/01-deploy/00-admin-deploy-share.md` |
| 已經拿到現成環境，只要執行與驗證 | `workshop/docs/01-deploy/00-participant-run-validate.md` |

其餘正式內容請直接看：

- `workshop/docs/01-deploy/index.md`
- `workshop/docs/02-customize/index.md`
- `workshop/docs/03-understand/index.md`
- `workshop/docs/04-cleanup/index.md`

## Repo 內容重點

- `workshop/docs/`：正式 workshop 文件
- `scripts/`：建置、部署、資料生成與測試腳本
- `infra/`：Azure 基礎架構與 Foundry 相關資源
- `data/`：預設與靜態範例資料
- `multi_agent/`：多代理工作流範例

## 正式文件位置

本 repo 的正式使用者文件一律以 `workshop/docs/` 為主；README 不再維護第二份操作手冊。

如果你偏好網站閱讀，可直接使用：

- Workshop：https://payton-chou-ms.github.io/e2e-ms-foundry-workshop/

## 授權

MIT
