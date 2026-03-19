# T-11 PII 評估

## 決策

採用 Azure Language PII detection 的最小文字 redaction demo，不把 PII 偵測直接塞進主 agent tool loop。

## 主要產出

- `scripts/12_demo_pii_redaction.py`

## Demo 範圍

- 輸入一段帶 email、電話、地址、帳號的文字
- 呼叫 PII detection
- 輸出 redacted text 與偵測到的 entity 類別

## 需要的設定

- `AZURE_LANGUAGE_ENDPOINT` 或 `LANGUAGE_ENDPOINT`
- `AZURE_LANGUAGE_KEY` 或 `LANGUAGE_KEY`

## Skip 條件

- 未安裝 `azure-ai-textanalytics`
- 未設定 Language endpoint/key
- 服務或權限尚未就緒

## 結論

PII 是合理的 optional governance demo，但目前更適合作為獨立 pre/post-processing 範例，而不是 workshop 主 agent 的預設內建能力。