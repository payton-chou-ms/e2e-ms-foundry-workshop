"""完整方案建置腳本。"""

from load_env import load_all_env
import argparse
import subprocess
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# Configuration
# ============================================================================

STEPS = {
    "01": {"script": "01_generate_sample_data.py", "name": "產生範例資料", "time": "約 2 分鐘"},
    "02": {"script": "02_create_fabric_items.py", "name": "建立 Fabric 項目", "time": "約 30 秒"},
    "03": {"script": "03_load_fabric_data.py", "name": "把資料載入 Fabric", "time": "約 1 分鐘"},
    "04": {"script": "04_generate_agent_prompt.py", "name": "產生 Agent Prompt", "time": "約 5 秒"},
    "05": {"script": "05_create_fabric_agent.py", "name": "建立 Fabric Data Agent", "time": "約 30 秒"},
    "06": {"script": "06_upload_to_search.py", "name": "上傳到 AI Search", "time": "約 1 分鐘"},
    "06b": {"script": "06b_upload_to_foundry_knowledge.py", "name": "建立 Foundry IQ Knowledge Base", "time": "約 1 分鐘"},
    "07": {"script": "07_create_foundry_agent.py", "name": "建立 Foundry Agent", "time": "約 10 秒"},
    "07b": {"script": "07b_create_foundry_iq_agent.py", "name": "建立 Foundry IQ Agent", "time": "約 10 秒"},
    "07-search": {"script": "07_create_foundry_agent.py", "name": "建立 Foundry Agent（只用 Search）", "time": "約 10 秒", "args": ["--foundry-only"]},
    "08": {"script": "08_test_foundry_agent.py", "name": "測試 Foundry Agent", "time": "互動式"},
    "08b": {"script": "08b_test_foundry_iq_agent.py", "name": "測試 Foundry IQ Agent", "time": "互動式"},
    "cu-defaults": {"script": None, "name": "設定 Content Understanding 預設值", "time": "約 5 秒"},
}

# Default pipeline order
DEFAULT_PIPELINE = ["01", "02", "03", "04", "05", "06", "07"]
FOUNDRY_ONLY_PIPELINE = ["cu-defaults", "01", "06", "07-search"]
FOUNDRY_IQ_PIPELINE = ["01", "06b", "07b"]

# ============================================================================
# Parse Arguments
# ============================================================================

parser = argparse.ArgumentParser(
    description="端到端建置流程：資料 → 知識庫 → Agent → API → App",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
範例：
    python scripts/00_build_solution.py                # 建立完整方案
    python scripts/00_build_solution.py --from 04      # 從第 04 步開始
    python scripts/00_build_solution.py --only 07      # 只執行指定步驟
    python scripts/00_build_solution.py --skip-fabric  # 略過 Fabric 步驟
    python scripts/00_build_solution.py --foundry-only # 不需要 Fabric，只走 Search 路徑
"""
)

parser.add_argument("--foundry-only", action="store_true",
                    help="Foundry-only 模式：完全略過 Fabric，只使用 AI Search")
parser.add_argument("--foundry-iq", action="store_true",
                    help="Foundry 原生 IQ 模式：建立可直接在 Foundry 使用的 knowledge-base agent")
parser.add_argument("--industry", type=str,
                    help="產生資料用的產業（覆蓋 .env 設定）")
parser.add_argument("--usecase", type=str,
                    help="產生資料用的使用情境（覆蓋 .env 設定）")
parser.add_argument("--size", choices=["small", "medium", "large"],
                    help="資料量大小（覆蓋 .env 設定）")
parser.add_argument("--scenario", type=str,
                    help="既有情境 key（傳給 scenario-aware 腳本）")
parser.add_argument("--clean", action="store_true",
                    help="清除並重新建立 Fabric 項目（切換情境時使用）")

parser.add_argument("--from", dest="from_step", type=str,
                    help="從這一步開始（例如：--from 04）")
parser.add_argument("--only", nargs="+", type=str,
                    help="只執行這些步驟（例如：--only 07 08）")

parser.add_argument("--skip-fabric", action="store_true",
                    help="略過 Fabric 設定步驟（02、03）")
parser.add_argument("--skip-search", action="store_true",
                    help="略過 AI Search 上傳（06）")
parser.add_argument("--skip-agents", action="store_true",
                    help="略過 agent 建立與測試（05、07、08）")

parser.add_argument("--dry-run", action="store_true",
                    help="只顯示將要執行的內容，不實際執行")
parser.add_argument("--continue-on-error", action="store_true",
                    help="即使某一步失敗也繼續往下執行")

args = parser.parse_args()

# ============================================================================
# Determine Pipeline
# ============================================================================

if args.foundry_only and args.foundry_iq:
    print("錯誤：--foundry-only 和 --foundry-iq 不能同時使用")
    sys.exit(1)

if args.only:
    pipeline = args.only
elif args.foundry_only:
    pipeline = FOUNDRY_ONLY_PIPELINE.copy()
elif args.foundry_iq:
    pipeline = FOUNDRY_IQ_PIPELINE.copy()
else:
    pipeline = DEFAULT_PIPELINE.copy()

if args.scenario:
    pipeline = [step for step in pipeline if step != "01"]

# Apply --from filter
if args.from_step:
    try:
        start_idx = pipeline.index(args.from_step)
        pipeline = pipeline[start_idx:]
    except ValueError:
        print(f"錯誤：流程中沒有步驟 '{args.from_step}'")
        print(f"可用步驟：{pipeline}")
        sys.exit(1)

# Apply skip filters
if args.skip_fabric:
    pipeline = [s for s in pipeline if s not in ["02", "03"]]
if args.skip_search:
    pipeline = [s for s in pipeline if s != "06"]
if args.skip_agents:
    pipeline = [s for s in pipeline if s not in ["05", "07", "08"]]

# ============================================================================
# Validate
# ============================================================================

# Check all scripts exist
for step in pipeline:
    script_file = STEPS[step]["script"]
    if script_file is None:
        continue
    script_path = os.path.join(script_dir, script_file)
    if not os.path.exists(script_path):
        print(f"警告：找不到腳本：{script_file}")

# Load environment from azd + project .env
load_all_env()

# Data generation arguments: CLI > .env
if "01" in pipeline:
    args.industry = args.industry or os.getenv("INDUSTRY")
    args.usecase = args.usecase or os.getenv("USECASE")
    args.size = args.size or os.getenv("DATA_SIZE", "small")

    if not args.industry or not args.usecase:
        print("\n" + "="*60)
        print("資料產生")
        print("="*60)
        print("\n在 .env 或 CLI 參數中都找不到 INDUSTRY / USECASE。")
        print("\n可用的範例情境：")
        print("-" * 60)
        print(f"  {'產業':<18} {'使用情境':<40}")
        print("-" * 60)
        samples = [
            ("Telecommunications", "Network operations and service management"),
            ("Retail", "Inventory management with sales analytics"),
            ("Manufacturing", "Production line tracking with quality control"),
            ("Insurance", "Claims processing and policy management"),
            ("Finance", "Transaction monitoring and fraud detection"),
            ("Energy", "Grid monitoring and outage response"),
            ("Education", "Student enrollment and course management"),
            ("Hospitality", "Hotel reservations and guest services"),
            ("Logistics", "Fleet management with delivery tracking"),
            ("Real Estate", "Property listings and lease management"),
        ]
        for ind, uc in samples:
            print(f"  {ind:<18} {uc:<40}")
        print("-" * 60)
        print()
        if not args.industry:
            args.industry = input("產業：").strip()
            if not args.industry:
                print("錯誤：必須提供產業。請在 .env 設定 INDUSTRY，或使用 --industry。")
                sys.exit(1)
        if not args.usecase:
            args.usecase = input("使用情境：").strip()
            if not args.usecase:
                print("錯誤：必須提供使用情境。請在 .env 設定 USECASE，或使用 --usecase。")
                sys.exit(1)

# ============================================================================
# Print Plan
# ============================================================================

print("\n" + "="*60)
if args.foundry_iq:
    print("Foundry 原生 IQ 流程")
else:
    print("Foundry IQ + Fabric IQ 流程")
print("="*60)

print(f"\n步驟（共 {len(pipeline)} 步）：")
for i, step in enumerate(pipeline, 1):
    info = STEPS[step]
    print(f"  {i}. {info['name']} ({info['time']})")

if args.industry:
    print(f"\n  產業：{args.industry}")
    print(f"  使用情境：{args.usecase}")
if args.scenario:
    print(f"  Scenario：{args.scenario}")

if args.dry_run:
    print("\n[DRY RUN] 不會真的執行任何腳本。")
    sys.exit(0)

print()
input("按 Enter 開始執行...")
print()

# ============================================================================
# Run Pipeline
# ============================================================================


def run_step(step_id):
    """Run a single pipeline step."""
    info = STEPS[step_id]
    script_path = os.path.join(
        script_dir, info["script"]) if info["script"] else None

    print(f"> [{step_id}] {info['name']}...", end=" ", flush=True)

    # Inline step: configure Content Understanding defaults
    if step_id == "cu-defaults":
        try:
            from azure.ai.contentunderstanding import ContentUnderstandingClient
            from azure.identity import DefaultAzureCredential
            endpoint = os.getenv("AZURE_AI_ENDPOINT")
            if not endpoint:
                print("略過（未設定 AZURE_AI_ENDPOINT）")
                return True
            client = ContentUnderstandingClient(
                endpoint=endpoint, credential=DefaultAzureCredential())
            try:
                defaults = client.get_defaults()
                if defaults.get("modelDeployments"):
                    print("[OK]（已設定）")
                    return True
            except Exception:
                pass
            client.update_defaults(model_deployments={
                "gpt-4.1-mini": "gpt-4.1-mini",
                "text-embedding-3-large": "text-embedding-3-large",
            })
            print("[OK]")
            return True
        except Exception as exc:
            print(f"略過（{exc}）")
            return True

    if not script_path or not os.path.exists(script_path):
        print("略過（找不到腳本）")
        return True

    # Build command
    cmd = [sys.executable, script_path]

    # Add step-specific arguments defined in STEPS
    if "args" in info:
        cmd.extend(info["args"])

    # Add arguments for data generation script
    if step_id == "01" and args.industry:
        cmd.extend(["--industry", args.industry])
        cmd.extend(["--usecase", args.usecase])
        if args.size:
            cmd.extend(["--size", args.size])

    # Pass --clean to step 02 if requested
    if step_id == "02" and args.clean:
        cmd.append("--clean")

    if args.scenario and step_id != "01":
        cmd.extend(["--scenario", args.scenario])

    # Create a clean environment that forces re-reading from .env
    # Remove DATA_FOLDER so child process reads fresh value from .env
    clean_env = os.environ.copy()
    clean_env.pop("DATA_FOLDER", None)
    clean_env.pop("SCENARIO_KEY", None)

    # Run with output captured
    result = subprocess.run(cmd, cwd=os.path.dirname(script_dir),
                            capture_output=True, text=True, env=clean_env)

    if result.returncode != 0:
        print("[FAIL] 失敗")
        print(
            f"\n  錯誤輸出：\n{result.stderr[-500:] if result.stderr else result.stdout[-500:]}")
        return False

    print("[OK]")
    return True


# Track results
results = {}
failed = False

for step in pipeline:
    success = run_step(step)
    results[step] = success

    if not success:
        failed = True
        if not args.continue_on_error:
            print(
                f"\n流程已停止。若要忽略失敗並繼續，請加上 --continue-on-error。")
            break

# ============================================================================
# Summary
# ============================================================================

print("\n" + "-"*60)

if failed:
    print("⚠ 流程執行完成，但有錯誤")
    sys.exit(1)
else:
    print("[OK] 流程已成功完成！")
    if args.foundry_only:
        print("\n下一步：python scripts/08_test_foundry_agent.py --foundry-only")
    elif args.foundry_iq:
        print("\n下一步：python scripts/08b_test_foundry_iq_agent.py")
    else:
        print("\n下一步：python scripts/08_test_foundry_agent.py")
