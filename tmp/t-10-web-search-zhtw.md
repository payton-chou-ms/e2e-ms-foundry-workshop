# T-10 Web Search 評估

## 決策

採用 Foundry 原生 `WebSearchTool` 的最小 demo，並保留「功能不可用時直接 skip」策略。

## 主要產出

- `scripts/11_demo_web_search.py`

## Demo 範圍

- 建立暫時 agent version
- 使用 `WebSearchTool` 回答公開網路問題
- 印出 inline citations
- 完成後刪除暫時 agent version

## 注意事項

- 此 demo 針對 public web search
- 若後續要比較 Bing grounding / Web Search / Deep Research，應在文件中區分服務邊界與資料合規差異

## Skip 條件

- SDK 缺少 `WebSearchTool`
- project 環境尚未支援 web search

## 結論

Web Search 可做為獨立 optional demo，適合補強 workshop 的即時外部資訊案例，但不該與 SQL + Search 主路徑耦合。