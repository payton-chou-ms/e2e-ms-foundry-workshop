#!/usr/bin/env bash
# ============================================================================
# P2P Demo — ④ 發票階段：Content Understanding + 三單比對
#
# 這支 script 自動執行發票辨識的完整流程：
#   1. 用 Content Understanding 辨識發票圖片 → 得到 Markdown
#   2. 顯示 CU 辨識出的關鍵欄位
#   3. 提示如何搭配 Data Agent 做三單比對
#
# 用法：
#   bash data/p2p/run_04_invoice.sh
#   bash data/p2p/run_04_invoice.sh --file path/to/custom_invoice.png
#
# 前提：
#   - 已執行 azd up 並完成環境設定
#   - 已安裝 azure-ai-contentunderstanding（pip install -r requirements.txt）
#   - sample_invoice.png 已放入 data/p2p/04_invoice/
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INVOICE_DIR="$SCRIPT_DIR/04_invoice"
DEFAULT_INVOICE="$INVOICE_DIR/sample_invoice.png"

echo "============================================================"
echo "  P2P ④ 發票階段 — Content Understanding 辨識 (自動化)"
echo "============================================================"
echo ""

PYTHON="${PYTHON:-${PROJECT_ROOT}/.venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="$(command -v python3 2>/dev/null || command -v python 2>/dev/null)"
fi

cd "$PROJECT_ROOT"

# ------------------------------------------------------------------
# Step 1: 確認發票檔案
# ------------------------------------------------------------------
INVOICE_FILE=""

# Parse --file argument
while [[ $# -gt 0 ]]; do
    case "$1" in
        --file) shift; INVOICE_FILE="${1:-}"; shift ;;
        *)      INVOICE_FILE="$1"; shift ;;
    esac
done

SKIP_CU=false

if [[ -z "$INVOICE_FILE" ]]; then
    if [[ -f "$DEFAULT_INVOICE" ]]; then
        INVOICE_FILE="$DEFAULT_INVOICE"
        echo "▶ 使用預設發票：$INVOICE_FILE"
    else
        echo "ℹ️  找不到預設發票 $DEFAULT_INVOICE"
        echo "   → 跳過 CU Live Demo，改用預建的辨識結果繼續展示"
        echo "   → 如需 Live Demo，請將發票圖片放入 data/p2p/04_invoice/sample_invoice.png"
        SKIP_CU=true
    fi
else
    echo "▶ 使用指定檔案：$INVOICE_FILE"
fi

echo ""

# ------------------------------------------------------------------
# Step 2: 執行 Content Understanding
# ------------------------------------------------------------------
if $SKIP_CU; then
    echo "▶ Step 1: Content Understanding 辨識發票...（已跳過 — 無發票圖片）"
else
    echo "▶ Step 1: Content Understanding 辨識發票..."
    echo "  輸入：$INVOICE_FILE"
    echo ""

    "$PYTHON" scripts/09_demo_content_understanding.py \
        --file "$INVOICE_FILE" \
        --max-markdown-chars 5000
fi

echo ""

# ------------------------------------------------------------------
# Step 3: 顯示已有的 CU 輸出 Markdown
# ------------------------------------------------------------------
CU_OUTPUT="$INVOICE_DIR/invoice_cu_output.md"

echo "▶ Step 2: CU 輸出 Markdown（預建版本）"
echo ""

if [[ -f "$CU_OUTPUT" ]]; then
    echo "  ✅ 已有預建的 CU 輸出：$CU_OUTPUT"
    echo ""
    echo "  --- 三單比對關鍵欄位 ---"
    # Extract key fields from the markdown
    grep -E "^\- \*\*" "$CU_OUTPUT" 2>/dev/null || true
    echo "  ---"
else
    echo "  ⚠️  尚無預建 CU 輸出。"
    echo "     上面 Step 1 的 CU Live Demo 輸出即為辨識結果。"
    echo "     可手動整理到 $CU_OUTPUT"
fi

echo ""

# ------------------------------------------------------------------
# Step 4: Data Agent 查詢提示
# ------------------------------------------------------------------
echo "▶ Step 3: 搭配 Data Agent 三單比對"
echo ""
echo "  Fabric Data Agent 已建好："
echo "  Group ID: bf6bf65b-0e83-4d35-aed3-be111694187a"
echo "  Agent ID: 6d11a596-ad2a-45a0-ad89-8ffc0564b5c0"
echo ""
echo "  建議在 Foundry Portal 用以下問題測試 Data Agent："
echo ""
echo "  1. PO 4500001332 的採購明細是什麼？"
echo "  2. 料號 MZ-RM-R300-01 的歷史採購紀錄？"
echo "  3. PO 4500001332 的收貨紀錄，數量是否為 53？"
echo ""

# ------------------------------------------------------------------
# Step 5: 顯示 Sample Questions
# ------------------------------------------------------------------
SAMPLE_Q="$INVOICE_DIR/sample_questions.txt"

echo "▶ Step 4: 發票 Agent 完整測試問題"
echo ""

if [[ -f "$SAMPLE_Q" ]]; then
    cat "$SAMPLE_Q"
else
    echo "  ⚠️  找不到 sample_questions.txt"
fi

echo ""
echo "============================================================"
echo "  ✅ 發票階段 demo 準備完成"
echo ""
echo "  下一步："
echo "  1. 在 Foundry Portal 建立 Invoice Agent"
echo "     → 使用 04_invoice/invoice_agent_instruction.md 作為 instruction"
echo "  2. 將 CU 輸出 Markdown 交給 Agent 做三單比對"
echo "  3. 搭配 Data Agent 查 PO/GR 紀錄"
echo "============================================================"
