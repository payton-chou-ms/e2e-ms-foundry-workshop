# 後續步驟

## 你已準備好做下一輪練習

如果你已經完成主流程、看懂答案從哪裡來，下一步就是把同一套流程換成不同情境，讓它更接近你真正想示範或學習的內容。

### 你現在可以做什麼

- **重新產生情境**：用不同產業與 use case 再跑一次
- **練習文件問題**：觀察文件證據如何回到答案裡
- **練習資料問題**：觀察自然語言如何被轉成查詢
- **練習組合式問題**：同時用到文件與資料來源
- **往後延伸**：再看多代理、發佈或選配 demo

### 快速參考：重新產生情境

```bash
# 每次要換新情境時：
python scripts/00_build_solution.py --clean \
  --industry "Your Industry" \
  --usecase "Brief description of your use case"
```

**保險範例：**
```bash
python scripts/00_build_solution.py --clean \
  --industry "Insurance" \
  --usecase "Property and casualty insurance with claims processing, policy management, and fraud detection"
```

### 建議你的下一步

1. 換一個產業或 use case，再跑一次完整 build
2. 準備 5 到 7 題同時涵蓋文件、資料、組合式問題
3. 回頭看深入解析，把你剛剛做的步驟對回技術主線

### 資源

- [Microsoft Foundry 文件](https://learn.microsoft.com/azure/ai-studio/)
- [Microsoft Fabric 文件](https://learn.microsoft.com/fabric/)
- [負責任 AI 實務](https://www.microsoft.com/ai/responsible-ai)


---

[← 清理資源](index.md) | [回到總覽 →](../index.md)
