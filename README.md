# 使用 Solution Accelerators 更快建構方案 – Foundry IQ + Fabric IQ（Workshop）

建構可同時結合**非結構化文件知識**與**結構化企業資料**的 AI 代理程式，同時保留一條清楚的路徑，讓你能說明這個 PoC 背後的五個核心主軸，以及第六個延伸主題「多代理程式延伸」。

## 這個機會點

組織的重要知識通常分散在文件（PDF、政策文件、操作手冊）與結構化系統（資料庫、資料倉儲）中。透過 AI 串接這些來源，使用者就能在單一對話介面中取得整合後的答案。

## 方案內容

這個實作練習會建立一個智慧代理程式，具備以下能力：

- **部署必要模型**，供對話與向量嵌入使用，並將選配延伸模型獨立管理
- **建立提示詞代理程式**，在 Microsoft Foundry 中協調問題、指令與工具呼叫
- **定義嚴格的 tool contract**，以明確 guardrail 執行 SQL 與文件檢索
- **從文件建立可搜尋知識層**，透過 Azure AI Search 與 `search_documents` 取得可引用段落
- **提供情境與資料脈絡**，讓代理程式能依 schema prompt 產生唯讀 SQL
- **結合兩者**，回答更複雜的商業問題

## 五個核心主軸 + 一個延伸主題

這個 workshop 的執行路徑維持簡潔，但技術敘事現在已整理成五個核心主軸，並另外保留一個延伸主題：

| 主題 | 作用 |
|------|------|
| **Foundry Model** | 區分提供推理能力的核心部署，以及提供嵌入與其他延伸能力的部署 |
| **Foundry Agent** | 用 instructions 與 tools 定義可重用的 agent 行為 |
| **Foundry Tool** | 讓 agent 透過內建工具與自訂函式安全地取用外部資料或執行動作 |
| **Foundry IQ + Fabric IQ** | 讓答案 grounded 到企業文件與商業資料 |
| **Foundry Control Plane** | 用 Foundry project、connections、managed identity 與 Azure RBAC 治理執行環境與資源存取 |
| **多代理程式延伸** | 在不破壞主 workshop 教學主線的前提下，延伸成多角色工作流 |

主 workshop 路徑仍聚焦在兩個對使用者最可見的能力：

1. 透過 Foundry IQ 進行文件 grounding
2. 透過 Fabric IQ 進行結構化資料 grounding

其他主軸則用來說明這個體驗是如何被建構與治理的；多代理程式延伸則是後續情境化擴充，不是主流程必要條件。

---

## 這份 README 的角色

這份 README 是**入口頁**，幫你快速判斷這個 repo 是什麼、你應該從哪裡開始，以及正式文件在哪裡。

如果你要看完整操作步驟，請直接前往 `workshop/docs/` 對應頁面，而不是把 README 當成第二份操作手冊。

## 開啟 Workshop


[![Open in GitHub Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue?logo=github)](https://codespaces.new/payton-chou-ms/e2e-ms-foundry-workshop)
[![Open in VS Code](https://img.shields.io/badge/VS%20Code-Dev%20Containers-blue?logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/payton-chou-ms/e2e-ms-foundry-workshop)
[![GitHub Repository](https://img.shields.io/badge/GitHub-e2e--ms--foundry--workshop-181717?logo=github)](https://github.com/payton-chou-ms/e2e-ms-foundry-workshop)
[![Open in VS Code Web](https://img.shields.io/badge/VS%20Code-Open%20in%20Web-blue?logo=visualstudiocode)](https://vscode.dev/azure/?vscode-azure-exp=foundry&agentPayload=eyJiYXNlVXJsIjogImh0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9wYXl0b24tY2hvdS1tcy9lMmUtbXMtZm91bmRyeS13b3Jrc2hvcC9tYWluL2luZnJhL3ZzY29kZV93ZWIiLCAiaW5kZXhVcmwiOiAiL2luZGV4Lmpzb24iLCAidmFyaWFibGVzIjogeyJhZ2VudElkIjogIiIsICJjb25uZWN0aW9uU3RyaW5nIjogIiIsICJ0aHJlYWRJZCI6ICIiLCAidXNlck1lc3NhZ2UiOiAiIiwgInBsYXlncm91bmROYW1lIjogIiIsICJsb2NhdGlvbiI6ICIiLCAic3Vic2NyaXB0aW9uSWQiOiAiIiwgInJlc291cmNlSWQiOiAiIiwgInByb2plY3RSZXNvdXJjZUlkIjogIiIsICJlbmRwb2ludCI6ICIifSwgImNvZGVSb3V0ZSI6IFsiYWktcHJvamVjdHMtc2RrIiwgInB5dGhvbiIsICJkZWZhdWx0LWF6dXJlLWF1dGgiLCAiZW5kcG9pbnQiXX0=)

---

## 你會在這裡完成什麼

這個 workshop 會帶你完成四件事：

1. 把一個可同時回答文件與資料問題的 AI PoC 跑起來
2. 依自己的產業與使用案例重建資料、文件與測試問題
3. 理解這個 PoC 背後的模型、代理程式、工具、接地流程與控制平面
4. 視需要再往多代理程式工作流延伸

## 從哪裡開始

請依你手上的環境，直接從正式文件選一條路徑開始：

| 如果你現在要做的事 | 從這裡開始 |
|----------------------|--------------|
| 想先理解 workshop 的完整流程與學習順序 | `workshop/docs/index.md` |
| 需要自己部署 Azure 與 Fabric 環境 | `workshop/docs/01-deploy/00-admin-deploy-share.md` |
| 已經拿到現成環境，只要執行與驗證 | `workshop/docs/01-deploy/00-participant-run-validate.md` |
| 想換成自己的產業與使用案例 | `workshop/docs/02-customize/` |
| 想 deep dive | `workshop/docs/03-understand/` |
| 清理資源 | `workshop/docs/04-cleanup/` |

## 最短啟動方式

如果你只是要先快速跑起來，可先照下面順序做：

用 Codespaces 開啟這個 repo </br>
[![Open in GitHub Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue?logo=github)](https://codespaces.new/payton-chou-ms/e2e-ms-foundry-workshop)

再執行下面的命令
```bash
# Login and deploy
azd auth login --tenant-id <TENANT_ID>  --use-device-code
azd up --subscription <SUBSCRIPTION_ID>
# After deploy, upload doc and create agent to test
python scripts/00_build_solution.py --foundry-only
python scripts/08_test_foundry_agent.py --foundry-only
python scripts/00_build_solution.py --foundry-iq
python scripts/08b_test_foundry_iq_agent.py
```

參考頁面：

- [Workshop 部署總覽](workshop/docs/01-deploy/index.md)
- [建置方案](workshop/docs/01-deploy/04-run-scenario.md)
- [主流程腳本 01-08](workshop/docs/01-deploy/05b-script-core-pipeline.md)
- [快速建置與測試](workshop/docs/01-deploy/05a-script-core-paths.md)

## 正式文件位置

本 repo 的正式使用者文件一律以 `workshop/docs/` 為主。

你可以直接從這些入口閱讀：

- `workshop/docs/index.md`
- `workshop/docs/00-get-started/workshop-flow.md`
- `workshop/docs/01-deploy/index.md`
- `workshop/docs/02-customize/index.md`
- `workshop/docs/03-understand/index.md`
- `workshop/docs/04-cleanup/index.md`

如果你偏好網站閱讀，可直接使用：

- Workshop：https://payton-chou-ms.github.io/e2e-ms-foundry-workshop/

## 授權

MIT
