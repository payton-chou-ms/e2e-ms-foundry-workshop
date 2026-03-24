# Agent365 納入 Workshop 的建議計畫

## 結論

建議把 Agent365 展示放進 workshop，但不要放進主線部署流程，而是定位成 **選修延伸章節** 或 **deep dive**。

原因很直接：

- 目前 workshop 主軸是 Azure AI Foundry、Search、Fabric、multi-agent workflow 與既有 demo 場景。
- Agent365 帶來的是另一層能力：**把既有 agent 接到 Microsoft 365 / Teams 使用情境**。
- 這個能力很有展示價值，但會增加身份、安裝生命週期、通道互動模型等額外複雜度。
- 如果把它放進主線，會稀釋目前 workshop 的核心學習路徑。

因此較合理的做法是：

- 主線 workshop 仍聚焦在 Foundry agent 與 demo scenario。
- Agent365 作為「如何把 agent 帶到 Microsoft 365 / Teams」的延伸展示。

## 建議定位

最適合的定位是：

1. 放在 `03-understand` 或同層級的 deep dive 區段。
2. 內容上視為「channel integration / enterprise surface」延伸，而不是新的基礎教學章節。
3. 與既有 Retail demo 連結，而不是額外再開一條全新 scenario。

## 為什麼不建議放進主線

Agent365 展示牽涉的重點，和目前主線 workshop 不完全相同：

- Microsoft 365 / Teams 的互動入口
- user identity 與 `aad_object_id` 類型的使用者識別
- 安裝 / 移除事件處理
- 多訊息回覆模式
- typing indicator 與對話體驗細節

這些都很有價值，但屬於「產品化通路整合」議題，不是目前 workshop 主線裡最先要掌握的 Foundry agent 建置流程。

如果直接塞入主線，常見結果會是：

- 學員更難分辨哪一部分是 Foundry 核心概念
- 身份與通道設定成本拉高
- workshop 時間被分散到 Teams / M365 整合細節

## 最佳展示方式

建議以 **Retail demo** 當作 Agent365 的承載場景。

原因：

- Retail demo 已經有明確的商務敘事與多 knowledge base / multi-agent 背景。
- 如果把同一個 Retail assistant 搬到 Teams 或 Microsoft 365 入口，價值會很直觀。
- 學員可以清楚看到：agent 本身沒換場景邏輯，只是換了互動入口與使用者體驗層。

建議展示主軸：

1. 同一個 Retail agent 如何從 Playground / CLI 走向 Teams。
2. 使用者身份如何影響 agent 回覆與後續整合能力。
3. 在 Teams 中如何呈現多段式回覆、狀態提示與互動節奏。

## 建議章節內容

如果要新增一篇 workshop 文件，建議內容可分成以下幾段：

### 1. Agent365 是什麼

說明它在 workshop 裡的角色：

- 它不是取代 Foundry agent。
- 它是把既有 agent 能力帶到 Microsoft 365 / Teams 的展示層。
- 它更接近「agent product surface」而不是「agent core runtime」。

### 2. 這個展示解決什麼問題

建議聚焦三個價值：

- 讓 agent 出現在更貼近工作流的入口
- 利用企業身份資訊提升互動上下文
- 展示多訊息回覆與安裝生命週期這類真實產品行為

### 3. 與現有 workshop 的關係

要明確說明分層：

- Foundry / Search / Fabric / workflow 是底層能力
- Agent365 是前端通道與企業使用情境整合

### 4. Demo flow

建議示範流程：

1. 先用既有 Retail scenario 說明 agent 已可在原本入口運作。
2. 再切到 Agent365 版本，展示同一能力如何進入 Teams。
3. 補充身份、安裝事件、多訊息回覆的差異。
4. 最後說明什麼情境下值得把 workshop 的 agent 進一步產品化成 Agent365 體驗。

### 5. 不納入主線的理由

這一段建議直接寫清楚，避免讀者誤解：

- 這不是所有 workshop 參與者都必須完成的步驟
- 這是給需要 M365 / Teams 整合情境的延伸內容
- 如果先學主線，再看 Agent365，理解成本會更低

## 建議文件放置方式

如果後續要正式放進 workshop 文件，建議新增一頁，例如：

- `workshop/docs/03-understand/06-agent365-extension.md`

並在 `workshop/mkdocs.yml` 的 deep dive / understand 區段加入導覽。

命名方向建議偏向「extension」或「integration」，不要讓它看起來像主線必做步驟。

## 建議實作順序

### Phase 1: 文件化

先補一篇純說明型章節：

- 為什麼要有 Agent365 展示
- 它和現有 Foundry demo 的關係
- 適合展示哪些能力
- 需要哪些額外前置條件

### Phase 2: 最小可展示版本

選一個既有 demo，優先建議 Retail：

- 接一個最小 Agent365 入口
- 展示登入身份、基本問答、多訊息回覆
- 不急著擴大到所有 scenario

### Phase 3: 產品化延伸

如果展示反應好，再往下補：

- 安裝 / 移除事件處理
- 更完整的 Teams 互動模式
- 與企業資料、通知或工作流的延伸整合

## 最後建議

整體建議如下：

1. **要放，但不要放進主線。**
2. **用 Retail 當主要展示場景。**
3. **把 Agent365 定位成 Microsoft 365 / Teams integration deep dive。**
4. **先寫成文件章節，再決定是否做成完整可操作 demo。**

這樣可以保留 Agent365 的展示價值，同時不破壞目前 workshop 的主軸與節奏。