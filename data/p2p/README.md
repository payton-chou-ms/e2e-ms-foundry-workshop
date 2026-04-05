# P2P (Procure-to-Pay) 展示素材

本資料夾統一存放 P2P 五階段中，實際要展示的三個 Agent 所需素材。

## Quick Start — 三行就能跑

```bash
# 1. 確認已登入 Azure 且 azd 環境已設定
az account show && azd env list

# 2. 一鍵執行全部三階段（②採購 → ④發票 → ⑤付款）
bash data/p2p/run_all.sh

# 3. 或只跑單一階段
bash data/p2p/run_all.sh --stage 2   # 只跑合約審閱
bash data/p2p/run_all.sh --stage 4   # 只跑發票辨識
bash data/p2p/run_all.sh --stage 5   # 只跑 Content Safety
```

> **沒有 `sample_invoice.png`？** 階段 ④ 會自動跳過 CU Live Demo，改用預建的辨識結果繼續展示。

## 目錄結構

```
data/p2p/
├── README.md                          ← 本檔
├── run_all.sh                         # 🔹 一鍵執行全部階段
├── run_02_contract_review.sh          # 🔹 自動執行 ② 合約審閱
├── run_04_invoice.sh                  # 🔹 自動執行 ④ 發票辨識
├── run_05_payment_safety.sh           # 🔹 自動執行 ⑤ Content Safety
├── 02_contract_review/                # ② 採購 — 合約審閱（已完成）
│   └── 引用 data/contract_keyword_review/
├── 04_invoice/                        # ④ 發票 — CU + Data Agent 三單比對
│   ├── sample_invoice.png             # 範例電子發票圖片（需手動放入）
│   ├── invoice_cu_output.md           # CU 辨識結果（結構化 Markdown）
│   ├── invoice_agent_instruction.md   # Invoice Agent system prompt
│   └── sample_questions.txt           # 發票階段測試問題
├── 05_payment/                        # ⑤ 付款 — Content Safety
│   ├── guardrail_instruction.md       # Governance guardrail text
│   └── safety_test_cases.md           # 惡意 prompt 測試案例（13 案例）
└── multi_agent/                       # Multi-Agent Workflow 示意
    ├── README.md                      # 架構圖 + Mermaid + 使用說明
    └── p2p_workflow.yaml              # P2P 五角色 workflow 定義
```

## 五階段分工

| # | 階段 | 狀態 | 說明 |
|---|------|------|------|
| ① | 請購 | ⏭️ 跳過 | 由其他同事負責 |
| ② | 採購 | ✅ 已完成 | 合約審閱 → `data/contract_keyword_review/` |
| ③ | 收貨 | ⏭️ 跳過 | 與採購展示方式接近 |
| ④ | 發票 | ✅ 已完成 | CU Live Demo + Fabric Data Agent 三單比對 |
| ⑤ | 付款 | ✅ 已完成 | Content Safety / Prompt Shield |

## Fabric Data Agent（④ 發票）

- **Group ID**: `bf6bf65b-0e83-4d35-aed3-be111694187a`
- **Agent ID**: `6d11a596-ad2a-45a0-ad89-8ffc0564b5c0`
- **測試問題**: 單號 `4500001332`、料號 `MZ-RM-R300-01`

## 完整計劃

詳見 [`docs/plans/p2p-multi-agent-workshop-plan.md`](../../docs/plans/p2p-multi-agent-workshop-plan.md)

## 自動化 Shell Scripts

四支腳本，讓同學不需要手動逐步操作，直接跑就能看到結果：

### 一鍵全跑

```bash
bash data/p2p/run_all.sh           # 依序跑 ②→④→⑤
bash data/p2p/run_all.sh --stage 4 # 只跑第 4 階段
bash data/p2p/run_all.sh --dry-run # 不執行，只顯示會跑什麼
```

### 單獨執行

| Script | 階段 | 說明 |
|--------|------|------|
| `run_02_contract_review.sh` | ② 採購 | 執行 CU 合約審閱 → 產出 6 個中繼檔案 |
| `run_04_invoice.sh` | ④ 發票 | 執行 CU 發票辨識 → 顯示辨識結果 + Data Agent 提示 |
| `run_05_payment_safety.sh` | ⑤ 付款 | 顯示 guardrail → 呼叫 Content Safety API → 印出測試案例 |

```bash
# 範例
bash data/p2p/run_02_contract_review.sh
bash data/p2p/run_04_invoice.sh
bash data/p2p/run_05_payment_safety.sh --api-only   # 跳過說明，只跑 API
bash data/p2p/run_05_payment_safety.sh --show-only   # 不呼叫 API，僅展示素材
```
