#!/usr/bin/env bash
# ============================================================================
# P2P Demo — ⑤ 付款階段：Content Safety 偵測
#
# 這支 script 自動執行 Content Safety 展示：
#   1. 顯示 Guardrail Instruction（可直接貼入 Agent）
#   2. 執行 Azure AI Content Safety API demo（如果環境已部署）
#   3. 列出測試案例供 Portal 手動測試
#
# 用法：
#   bash data/p2p/run_05_payment_safety.sh
#   bash data/p2p/run_05_payment_safety.sh --api-only    # 只跑 API demo
#   bash data/p2p/run_05_payment_safety.sh --show-only   # 只顯示素材，不呼叫 API
#
# 前提：
#   - 若要跑 API demo：需要 Azure AI Content Safety 資源
#   - 若只看素材：不需額外資源
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PAYMENT_DIR="$SCRIPT_DIR/05_payment"

API_ONLY=false
SHOW_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --api-only)  API_ONLY=true ;;
        --show-only) SHOW_ONLY=true ;;
    esac
done

PYTHON="${PYTHON:-${PROJECT_ROOT}/.venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="$(command -v python3 2>/dev/null || command -v python 2>/dev/null)"
fi

cd "$PROJECT_ROOT"

echo "============================================================"
echo "  P2P ⑤ 付款階段 — Content Safety 防護 (自動化)"
echo "============================================================"
echo ""

# ------------------------------------------------------------------
# Step 1: 顯示 Guardrail Instruction
# ------------------------------------------------------------------
if ! $API_ONLY; then
    GUARDRAIL="$PAYMENT_DIR/guardrail_instruction.md"

    echo "▶ Step 1: Guardrail Instruction"
    echo ""

    if [[ -f "$GUARDRAIL" ]]; then
        echo "  ✅ 已有 guardrail instruction：$GUARDRAIL"
        echo ""
        echo "  --- Guardrail 重點 ---"
        echo "  • Decision Safety — 禁止核准付款、必須人工授權"
        echo "  • Contract Safety — 禁止法律判斷、建議轉法務"
        echo "  • Data Protection — 禁止匯出敏感財務資料"
        echo "  • Prompt Injection — 維持角色、拒絕覆寫指令"
        echo "  • Escalation — NT\$500,000 以上標記、新供應商標記"
        echo "  ---"
        echo ""
        echo "  使用方式：將 guardrail text 貼入既有 Agent 的 instruction 末尾"
    else
        echo "  ⚠️  找不到 guardrail instruction"
    fi

    echo ""
fi

# ------------------------------------------------------------------
# Step 2: 執行 Content Safety API Demo
# ------------------------------------------------------------------
if ! $SHOW_ONLY; then
    echo "▶ Step 2: Azure AI Content Safety API Demo"
    echo ""
    echo "  送出正常 + 惡意文字 → 偵測風險等級"
    echo ""

    "$PYTHON" scripts/17_demo_content_safety.py || {
        echo ""
        echo "  ⚠️  Content Safety API demo 無法執行。"
        echo "     這可能是因為尚未部署 Azure AI Content Safety 資源。"
        echo "     您仍可使用 guardrail instruction 做 Portal 手動展示。"
    }

    echo ""
fi

# ------------------------------------------------------------------
# Step 3: 顯示測試案例
# ------------------------------------------------------------------
if ! $API_ONLY; then
    TEST_CASES="$PAYMENT_DIR/safety_test_cases.md"

    echo "▶ Step 3: Foundry Portal 手動測試案例"
    echo ""

    if [[ -f "$TEST_CASES" ]]; then
        echo "  ✅ 已有 13 個測試案例：$TEST_CASES"
        echo ""
        echo "  --- 測試案例摘要 ---"
        echo "  正常問題 (3)："
        echo "    N1: 付款排程查詢"
        echo "    N2: 發票狀態查詢"
        echo "    N3: 現金流分析"
        echo ""
        echo "  Decision Safety (3)："
        echo "    D1: 直接核准付款"
        echo "    D2: 催促快速付款"
        echo "    D3: 偽裝緊急情境"
        echo ""
        echo "  Contract Safety (3)："
        echo "    C1: 法律判斷請求"
        echo "    C2: 合約違約判斷"
        echo "    C3: 罰則計算"
        echo ""
        echo "  Prompt Injection (4)："
        echo "    P1: 直接覆寫指令"
        echo "    P2: 角色切換攻擊"
        echo "    P3: Markdown 注入"
        echo "    P4: 多語言繞過"
        echo "  ---"
    else
        echo "  ⚠️  找不到 safety_test_cases.md"
    fi

    echo ""
fi

echo "============================================================"
echo "  ✅ 付款階段 demo 準備完成"
echo ""
echo "  展示建議："
echo "  1. 先在 Portal 展示原始 Agent 的正常回答"
echo "  2. 貼上 guardrail instruction 到 Agent"
echo "  3. 依序用 D1/C1/P1 測試防護效果"
echo "  4. (加分) 用 17_demo_content_safety.py 展示 API 層偵測"
echo "============================================================"
