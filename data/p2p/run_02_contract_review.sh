#!/usr/bin/env bash
# ============================================================================
# P2P Demo — ② 採購階段：合約關鍵字審閱
#
# 這支 script 自動執行合約審閱的完整流程：
#   1. 用 Azure Content Understanding 將合約 docx 轉成可比較段落
#   2. 從規則檔萃取規則清單
#   3. 列出產出的中間產物
#
# 用法：
#   bash data/p2p/run_02_contract_review.sh
#   bash data/p2p/run_02_contract_review.sh --cu-analyzer-id prebuilt-layout
#
# 前提：
#   - 已執行 azd up 並完成環境設定
#   - 已安裝 azure-ai-contentunderstanding（pip install -r requirements.txt）
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONTRACT_DIR="$PROJECT_ROOT/data/contract_keyword_review"

echo "============================================================"
echo "  P2P ② 採購階段 — 合約關鍵字審閱 (自動化)"
echo "============================================================"
echo ""

# ------------------------------------------------------------------
# Step 1: 重建中間產物（Azure Content Understanding）
# ------------------------------------------------------------------
echo "▶ Step 1: 重建合約中間產物..."
echo "  輸入資料夾：$CONTRACT_DIR/input/"
echo "  腳本：generate_content_artifacts.py"
echo ""

cd "$PROJECT_ROOT"

PYTHON="${PYTHON:-${PROJECT_ROOT}/.venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="$(command -v python3 2>/dev/null || command -v python 2>/dev/null)"
fi

"$PYTHON" "$CONTRACT_DIR/generate_content_artifacts.py" "$@"

echo ""

# ------------------------------------------------------------------
# Step 2: 檢查產出
# ------------------------------------------------------------------
echo "▶ Step 2: 檢查中間產物..."
echo ""

INTERMEDIATE_DIR="$CONTRACT_DIR/intermediate"
OUTPUT_DIR="$CONTRACT_DIR/output"

expected_files=(
    "$INTERMEDIATE_DIR/04-規則清單.json"
    "$INTERMEDIATE_DIR/04-規則清單.md"
    "$INTERMEDIATE_DIR/06-合約範本-可比較內容.md"
    "$INTERMEDIATE_DIR/06-合約範本-可比較段落.json"
    "$INTERMEDIATE_DIR/07-待審閱合約-可比較內容.md"
    "$INTERMEDIATE_DIR/07-待審閱合約-可比較段落.json"
)

all_ok=true
for f in "${expected_files[@]}"; do
    if [[ -f "$f" ]]; then
        echo "  ✅ $(basename "$f")"
    else
        echo "  ❌ $(basename "$f") — 找不到"
        all_ok=false
    fi
done

echo ""

# ------------------------------------------------------------------
# Step 3: 顯示結果摘要
# ------------------------------------------------------------------
echo "▶ Step 3: 結果摘要"
echo ""

if [[ -f "$INTERMEDIATE_DIR/04-規則清單.md" ]]; then
    rule_count=$(grep -c "^|" "$INTERMEDIATE_DIR/04-規則清單.md" 2>/dev/null || echo "0")
    echo "  規則清單：約 $rule_count 列"
fi

for json_file in "$INTERMEDIATE_DIR"/*-可比較段落.json; do
    if [[ -f "$json_file" ]]; then
        para_count=$(grep -c '"id"' "$json_file" 2>/dev/null || echo "0")
        echo "  $(basename "$json_file")：$para_count 個段落"
    fi
done

if [[ -f "$OUTPUT_DIR/09-審閱結果.html" ]]; then
    echo "  審閱結果 HTML：✅ 已存在"
else
    echo "  審閱結果 HTML：⚠️  尚未產生（需在 Foundry Portal 執行 Reviewer Agent）"
fi

echo ""

if $all_ok; then
    echo "============================================================"
    echo "  ✅ 合約審閱中間產物已全部就緒"
    echo ""
    echo "  下一步："
    echo "  1. 在 Foundry Portal 建立 Contract Reviewer Agent"
    echo "  2. 上傳中間產物作為 Knowledge"
    echo "  3. 使用 config/sample_questions.txt 中的問題測試"
    echo "============================================================"
else
    echo "============================================================"
    echo "  ⚠️  部分中間產物缺失，請檢查 Content Understanding 設定"
    echo "============================================================"
    exit 1
fi
