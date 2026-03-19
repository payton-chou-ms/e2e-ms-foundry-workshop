# 後續步驟

## 你已準備好建構客戶 PoC！

你現在擁有加速客戶互動所需的一切。

### 你現在可以做什麼

- **快速部署**：Infrastructure as Code 讓設定可重複
- **產生任何情境**：AI 為任何產業建立真實資料
- **展示文件智慧**：Foundry IQ 搭配代理式擷取（agentic retrieval）
- **展示資料智慧**：Fabric IQ 搭配自然語言查詢
- **展示組合能力**：協調代理程式回答複雜問題

### 快速參考：建構客戶 PoC

```bash
# 每次客戶會議之前，產生對應的情境：
python scripts/00_build_solution.py --clean \
  --industry "Customer's Industry" \
  --usecase "Brief description of their use case"
```

**保險客戶範例：**
```bash
python scripts/00_build_solution.py --clean \
  --industry "Insurance" \
  --usecase "Property and casualty insurance with claims processing, policy management, and fraud detection"
```

### 客戶對話要點

| 客戶問題 | 你的回答 |
|----------|----------|
| "實作要多久？" | Solution Accelerator 讓你幾小時內就能有 PoC，幾週內可產出正式版 |
| "能用我們的資料嗎？" | 可連接任何文件與 Fabric/SQL 資料來源 |
| "準確嗎？" | 代理式擷取會規劃並驗證答案，引用來源 |
| "安全嗎？" | 使用 Entra ID 的企業安全性，在你的 Azure 租用戶中執行 |

### 資源

- [Azure AI Foundry 文件](https://learn.microsoft.com/azure/ai-studio/)
- [Microsoft Fabric 文件](https://learn.microsoft.com/fabric/)
- [負責任 AI 實務](https://www.microsoft.com/ai/responsible-ai)


---

[← 清理資源](index.md) | [回到總覽 →](../index.md)
