# T-12 Image Generation 評估

## 決策

採用 `gpt-image-1` 類型部署的獨立示範腳本，並明確把它定位成 optional model demo。

## 主要產出

- `scripts/13_demo_image_generation.py`

## Demo 範圍

- 讀取 Azure OpenAI endpoint / key
- 嘗試解析環境中的 image deployment
- 呼叫 `/images/generations` REST API
- 將 base64 圖檔寫出到本地檔案

## Deployment 解析策略

優先順序：

1. `AZURE_IMAGE_MODEL_DEPLOYMENT`
2. `AZURE_IMAGE_MODEL`
3. `AZURE_DEPLOYED_MODEL_SUMMARIES`
4. `AZURE_OPTIONAL_MODEL_DEPLOYMENTS`

## Skip 條件

- 找不到 image-capable deployment
- 未設定 Azure OpenAI endpoint / key
- 該環境尚未開通 image generation

## 結論

Image Generation 與 T-03 的 optional deployment strategy 已對齊：

- 不列入主流程必要能力
- 有部署就可單獨示範
- 沒部署就清楚 skip