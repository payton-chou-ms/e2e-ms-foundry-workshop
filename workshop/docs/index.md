# 總覽

這個 workshop 的目標，是讓你親手完成一個能同時回答文件問題與資料問題的 AI PoC。你會從可運作的範例開始，理解它的部署方式、接地方式，以及後續如何改成自己的情境。

你可以把這套內容當成一條學習路徑：先把 PoC 跑起來，再回頭理解底層設計，最後再把它改成自己的 use case。

## 哪些部分維持簡潔，哪些部分可進一步展開

這個 workshop 的 runtime 刻意維持簡潔，方便你先掌握主流程：

- 一個 prompt agent
- 兩個 core tools
- 兩條 grounding path：文件走 Foundry IQ，商業資料走 Fabric IQ

但底層的技術敘事現在已經擴展成五個主軸：

| Axis | Why it matters |
|------|----------------|
| **Foundry Model** | 說明哪些模型部署提供推理能力，哪些部署提供嵌入與其他延伸能力 |
| **Foundry Agent** | 說明 agent 如何結合 instructions、tools 與 knowledge sources 來協調回應 |
| **Foundry Tool** | 說明 agent 如何透過內建工具與自訂函式安全地取用資料或執行動作 |
| **Foundry IQ + Fabric IQ** | 說明答案如何 grounded 到文件與資料 |
| **Foundry Control Plane** | 說明 project、connections、managed identity 與 Azure RBAC 如何治理資源存取 |

這個 workshop flow 仍然優先強調簡潔的 runtime 路徑。五主軸的結構則是為了讓你在把 PoC 跑通之後，能進一步理解背後的技術設計。

## 選擇你的路徑

這個 workshop 支援兩種操作模式：

| Path | Intended user | Outcome |
|------|---------------|---------|
| **Admin deploy and share** | 想自行完成整套環境準備的學員 | 部署 Azure 資源、設定 Fabric，並整理出可重複使用的環境 |
| **Participant run and validate** | 已拿到現成環境的學員 | 使用已準備好的環境驗證範例情境並執行代理程式 |

如果你是自己從頭操作，請先走 admin 路徑，再進行 participant 驗證。

## Workshop 流程

| Step | Description | Time |
|------|-------------|------|
| **1. 部署方案** | 選擇 admin 路徑或 participant 路徑，然後設定預設情境 | ~15 min |
| **2. 依使用案例自訂** | 針對特定產業與使用案例進行客製化 | ~20 min |
| **3. Deep dive** | 用於 Q&A 的技術 deep dive | ~15 min |
| **4. 清理** | 刪除 Azure 資源 | ~5 min |

## 如何理解這套架構

建議你先按這個順序理解：

1. 先看成果：一個代理程式可以同時回答文件與資料問題。
2. 再看 runtime path：一個 prompt agent 加上兩個 core tools。
3. 最後再展開五個主軸，理解背後的技術骨架。

這樣可以讓你先掌握主線，再逐步進入技術細節。

!!! tip "PoC 前建議"
    1. 先完整做一次 **Step 1**，確認部署與流程可正常運作
    2. 再執行 **Step 2**，針對你的使用案例做客製化
    3. 最後閱讀 **Step 3**，準備回答技術問題

!!! note "文件位置"
    本 workshop 的完整文件請直接參考本網站內容。
    若需要查看原始 Markdown 檔案，位置在 `workshop/docs/`。

---

[快速開始 →](00-get-started/index.md)
