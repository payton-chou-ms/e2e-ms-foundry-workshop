# 總覽

一個好的 PoC 能幫助客戶具體想像這個方案對業務會帶來什麼影響。它會把對話從「這點子很有趣」推進到真正的「值得深入探索」。真正的挑戰在於，要做出一個有貼近感的 PoC，往往需要數週的客製工作，包括基礎架構、資料流程、整合，以及能反映客戶情境的專屬案例。

這個 workshop 會帶你學會如何使用 solution accelerators 快速部署產業化情境，讓你從第一次對話開始就能展示真實價值。

## 哪些部分維持簡潔，哪些部分可進一步展開

這個 workshop 的 runtime 刻意維持簡潔：

- 一個 prompt agent
- 兩個 core tools
- 兩條 grounding path：文件走 Foundry IQ，商業資料走 Fabric IQ

但底層的技術敘事現在已經擴展成五個主軸：

| Axis | Why it matters |
|------|----------------|
| **Foundry Model** | 說明必要與選配模型部署如何分工 |
| **Foundry Agent** | 說明協調流程如何被建立、讀取、追蹤與發佈 |
| **Foundry Tool** | 說明嚴格的 function contract 與安全邊界 |
| **Foundry IQ + Fabric IQ** | 說明答案如何 grounded 到文件與資料 |
| **Control Plane** | 說明 Azure 資源拓樸、connections 與 RBAC |

這個 workshop flow 仍然優先強調簡潔的 runtime 路徑。五主軸的結構則是為了讓你在 PoC 打動客戶之後，能進一步回答技術問題。

## 選擇你的路徑

這個 workshop 支援兩種操作模式：

| Path | Intended user | Outcome |
|------|---------------|---------|
| **Admin deploy and share** | 平台管理員或方案負責人 | 部署 Azure 資源、設定 Fabric，並為其他人準備可重用環境 |
| **Participant run and validate** | 方案建構者、業務或客戶工程師 | 使用已準備好的環境驗證範例情境並執行代理程式 |

如果同一個人負責完整 setup，請先走 admin 路徑，再進行 participant 驗證。

## Workshop 流程

| Step | Description | Time |
|------|-------------|------|
| **1. 部署方案** | 選擇 admin 路徑或 participant 路徑，然後設定預設情境 | ~15 min |
| **2. 依使用案例自訂** | 針對特定產業與使用案例進行客製化 | ~20 min |
| **3. Deep dive** | 用於 Q&A 的技術 deep dive | ~15 min |
| **4. 清理** | 刪除 Azure 資源 | ~5 min |

## 如何說明這套架構

在與客戶對話時，建議按照這個順序說明：

1. 先從業務成果開始：一個代理程式可以同時回答文件與資料問題。
2. 再說明 runtime path：一個 prompt agent 加上兩個 core tools。
3. 只有當聽眾需要更多技術細節時，再展開五個主軸。

這樣可以讓 workshop 的前段維持容易進入，同時保留足夠可信的架構說法。

!!! tip "PoC 前建議"
    1. 先完整做一次 **Step 1**，確認部署與流程可正常運作
    2. 再執行 **Step 2**，針對你的使用案例做客製化
    3. 最後閱讀 **Step 3**，準備回答技術問題

!!! note "文件唯一內容來源"
    canonical workshop 內容位於 `workshop/docs/`。
    產生出來的 site 輸出與 PDF 產生物應視為發佈輸出，而不是獨立維護的手寫內容。

---

[快速開始 →](00-get-started/index.md)
