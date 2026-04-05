#!/usr/bin/env bash
# ============================================================================
# P2P Demo — 一鍵執行全部三個階段
#
# 依序執行：
#   ② 採購 — 合約關鍵字審閱（Content Understanding）
#   ④ 發票 — 發票辨識 + 三單比對提示
#   ⑤ 付款 — Content Safety 防護展示
#
# 用法：
#   bash data/p2p/run_all.sh           # 執行全部
#   bash data/p2p/run_all.sh --stage 4 # 只跑第 4 階段（發票）
#   bash data/p2p/run_all.sh --stage 5 # 只跑第 5 階段（付款）
#   bash data/p2p/run_all.sh --dry-run # 只顯示會執行什麼，不實際執行
#
# 前提：
#   - 已執行 azd up 並完成環境設定
#   - 已安裝 requirements.txt 中的依賴
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

STAGE=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --stage)
            shift
            STAGE="${1:-}"
            if [[ ! "$STAGE" =~ ^[245]$ ]]; then
                echo "Invalid stage: $STAGE (valid: 2, 4, 5)" >&2
                exit 1
            fi
            ;;
        --dry-run) DRY_RUN=true ;;
        2|4|5)     STAGE="$1" ;;
        *)
            echo "Unknown argument: $1" >&2
            echo "Usage: bash run_all.sh [--stage 2|4|5] [--dry-run]" >&2
            exit 1
            ;;
    esac
    shift
done

run_stage() {
    local label="$1"
    local script="$2"
    shift 2

    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  $label"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    if $DRY_RUN; then
        echo "  [dry-run] 會執行: bash $script $*"
        return 0
    fi

    if bash "$script" "$@"; then
        echo ""
        echo "  ──── $label ✅ 完成 ────"
    else
        echo ""
        echo "  ──── $label ⚠️ 有問題，但繼續下一階段 ────"
    fi
}

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  P2P 採購到付款 — 自動化 Demo 執行                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "  階段 ②：合約關鍵字審閱（Content Understanding）"
echo "  階段 ④：發票辨識 + 三單比對"
echo "  階段 ⑤：Content Safety 防護"
echo ""

if [[ -n "$STAGE" ]]; then
    echo "  → 只執行階段 $STAGE"
fi

if $DRY_RUN; then
    echo "  → Dry-run 模式：只顯示指令，不實際執行"
fi

echo ""

# ── Stage ② ──
if [[ -z "$STAGE" || "$STAGE" == "2" ]]; then
    run_stage \
        "② 採購 — 合約關鍵字審閱" \
        "$SCRIPT_DIR/run_02_contract_review.sh"
fi

# ── Stage ④ ──
if [[ -z "$STAGE" || "$STAGE" == "4" ]]; then
    run_stage \
        "④ 發票 — Content Understanding 辨識" \
        "$SCRIPT_DIR/run_04_invoice.sh"
fi

# ── Stage ⑤ ──
if [[ -z "$STAGE" || "$STAGE" == "5" ]]; then
    run_stage \
        "⑤ 付款 — Content Safety 防護" \
        "$SCRIPT_DIR/run_05_payment_safety.sh"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  全部 P2P Demo 已執行完畢                                  ║"
echo "║                                                          ║"
echo "║  如需在 Foundry Portal 手動測試：                          ║"
echo "║  • Invoice Agent instruction → 04_invoice/                ║"
echo "║  • Guardrail instruction → 05_payment/                    ║"
echo "║  • Safety test cases → 05_payment/safety_test_cases.md    ║"
echo "╚════════════════════════════════════════════════════════════╝"
