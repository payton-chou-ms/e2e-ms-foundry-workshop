# T-03 多模型部署策略實作紀錄

## 目的

為 `infra/modules/foundry.bicep` 建立可維持主流程穩定的多模型部署骨架，讓必要模型固定部署，選配模型以參數化方式開啟或跳過，並把部署規劃結果輸出給 `azd` 與後續文件使用。

## 本次實作範圍

### 1. 必要模型維持明確、固定

- chat model 仍由 `gptModelName` / `gptModelVersion` / `gptDeploymentCapacity` 控制
- embedding model 仍由 `embeddingModel` / `embeddingDeploymentCapacity` 控制
- chat deployment SKU 改由既有 `deploymentType` 參數實際驅動，不再是未使用參數

### 2. 新增選配模型參數入口

在 `infra/modules/foundry.bicep` 新增 `optionalModelDeployments` 型別化參數，每個項目包含：

- `name`
- `modelName`
- `modelFormat`
- `skuName`
- `capacity`
- `enabled`
- `modelVersion`（選填）

在 `infra/main.bicep` 新增同名參數並傳遞到 module。

### 3. 新增選配模型的條件部署

- `enabled = true` 的項目才會建立 `Microsoft.CognitiveServices/accounts/deployments`
- `enabled = false` 的項目只保留在輸入清單中，不會被部署
- 選配模型採 `@batchSize(1)` 逐一部署，降低同時併發申請多個模型部署時的配額與錯誤放大風險

### 4. 新增部署結果輸出

模組新增輸出：

- `optionalModelDeployments`
- `enabledOptionalModelDeploymentNames`
- `skippedOptionalModelDeploymentNames`
- `deployedModelSummaries`
- `chatDeploymentSkuName`
- `embeddingDeploymentSkuName`

`infra/main.bicep` 也同步輸出：

- `AZURE_OPTIONAL_MODEL_DEPLOYMENTS`
- `AZURE_ENABLED_OPTIONAL_MODEL_DEPLOYMENT_NAMES`
- `AZURE_SKIPPED_OPTIONAL_MODEL_DEPLOYMENT_NAMES`
- `AZURE_DEPLOYED_MODEL_SUMMARIES`
- `AZURE_CHAT_DEPLOYMENT_SKU`
- `AZURE_EMBEDDING_DEPLOYMENT_SKU`

### 5. 清理參數檔漂移

`infra/main.parameters.json` 已移除失效的 `imageTag` 參數，並加入：

- `optionalModelDeployments: []`

## Best-Effort 策略說明

### 目前可做到的安全策略

本次實作的 best-effort 定義是：

1. 主流程必要模型固定部署
2. 選配模型預設不部署
3. 每個選配模型可獨立 `enabled` / `disabled`
4. 文件與後續腳本可以根據輸出判斷哪些模型是規劃部署、哪些被明確跳過

### 目前不能宣稱的行為

ARM / Bicep 本身不提供「某個模型部署失敗但主部署自動繼續成功」的真正 continue-on-error 語義。

因此：

- 若使用者把某個選配模型設為 `enabled = true`
- 而該模型因 region、quota、preview、provider support 或 tenant policy 無法部署

則整個 ARM deployment 仍可能失敗。

所以本 repo 目前的正確說法應是：

- **支援選配模型的參數化啟用與顯式跳過**
- **不支援 Bicep 層級自動吞掉失敗後繼續完成整體部署**

## 建議參數格式

```json
{
  "optionalModelDeployments": {
    "value": [
      {
        "name": "gpt-5-4",
        "modelName": "gpt-5.4",
        "modelFormat": "OpenAI",
        "skuName": "GlobalStandard",
        "capacity": 50,
        "enabled": false,
        "modelVersion": "2025-02-01"
      },
      {
        "name": "claude-sonnet-4-6",
        "modelName": "claude-sonnet-4-6",
        "modelFormat": "Anthropic",
        "skuName": "Standard",
        "capacity": 10,
        "enabled": false,
        "modelVersion": ""
      }
    ]
  }
}
```

## 驗證結果

已完成：

- `infra/modules/foundry.bicep` diagnostics clean
- `infra/main.parameters.json` 無錯誤
- `infra/main.bicep` 與 module 連接正常

目前殘留但與 T-03 無直接衝突的既有 warning：

- `secondaryLocation` 未使用
- `azureOpenAIApiVersion` 未使用
- `azureAiAgentApiVersion` 未使用

這些屬於既有主檔清理工作，可在後續 IaC 整理時一併處理。