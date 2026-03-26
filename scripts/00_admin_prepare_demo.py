"""Public entry point for preparing the demo environment."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

from content_understanding_defaults import ensure_content_understanding_defaults
from load_env import load_all_env
from scenario_utils import build_scenario_env, list_scenarios, resolve_scenario


load_all_env()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
INTERNAL_CALL_ENV = "PREPARE_DEMO_INTERNAL_CALL"


def get_default_shared_scenarios() -> list[str]:
    return [scenario["key"] for scenario in list_scenarios()]


def run_step(label: str, command: list[str], env: dict[str, str], dry_run: bool) -> bool:
    printable = " ".join(command)
    print(f"  - {label}: {printable}")
    if dry_run:
        return True

    result = subprocess.run(command, cwd=REPO_ROOT, text=True, env=env)
    if result.returncode != 0:
        print(f"[FAIL] {label}")
        return False

    print(f"[OK] {label}")
    return True


def build_base_env() -> dict[str, str]:
    env = dict(os.environ)
    env.pop("DATA_FOLDER", None)
    env.pop("SCENARIO_KEY", None)
    env[INTERNAL_CALL_ENV] = "1"
    return env


def run_preload(args: argparse.Namespace, base_env: dict[str, str]) -> bool:
    preload_cmd = [
        sys.executable,
        os.path.join(SCRIPT_DIR, "00_admin_preload_scenarios.py"),
        "--scenarios",
        *args.scenarios,
    ]
    if args.skip_blob:
        preload_cmd.append("--skip-blob")
    if args.skip_search:
        preload_cmd.append("--skip-search")
    if args.skip_foundry_knowledge:
        preload_cmd.append("--skip-foundry-iq")
    if args.skip_fabric:
        preload_cmd.append("--skip-fabric")
    if args.clean_fabric:
        preload_cmd.append("--clean-fabric")
    if args.dry_run:
        preload_cmd.append("--dry-run")

    return run_step("Scenario preload", preload_cmd, base_env, args.dry_run)


def run_agent_creation(args: argparse.Namespace, base_env: dict[str, str]) -> bool:
    failed = False

    for scenario_key in args.scenarios:
        scenario = resolve_scenario(scenario_key)
        scenario_env = build_scenario_env(scenario, extra=base_env)
        capabilities = scenario.get("capabilities", {})

        print(f"\n[{scenario_key}] {scenario['title']}")

        if not args.skip_foundry_only_agent:
            if capabilities.get("search", False):
                success = run_step(
                    "Foundry-only agent",
                    [
                        sys.executable,
                        os.path.join(SCRIPT_DIR, "07_create_foundry_agent.py"),
                        "--foundry-only",
                        "--scenario",
                        scenario_key,
                    ],
                    scenario_env,
                    args.dry_run,
                )
                failed = failed or not success
                if not success and not args.continue_on_error:
                    return False
            else:
                print("  - Foundry-only agent: 略過（scenario 不支援 search）")

        if not args.skip_foundry_iq_agent:
            if capabilities.get("foundryIq", False):
                success = run_step(
                    "Foundry-native IQ agent",
                    [
                        sys.executable,
                        os.path.join(
                            SCRIPT_DIR, "07b_create_foundry_iq_agent.py"),
                        "--scenario",
                        scenario_key,
                    ],
                    scenario_env,
                    args.dry_run,
                )
                failed = failed or not success
                if not success and not args.continue_on_error:
                    return False
            else:
                print("  - Foundry-native IQ agent: 略過（scenario 不支援 foundryIq）")

    return not failed


def run_build_mode(args: argparse.Namespace, base_env: dict[str, str]) -> bool:
    command = [
        sys.executable,
        os.path.join(SCRIPT_DIR, "00_build_solution.py"),
        "--yes",
    ]

    if args.mode == "foundry-only":
        command.append("--foundry-only")
    elif args.mode == "foundry-iq":
        command.append("--foundry-iq")

    if args.from_step:
        command.extend(["--from", args.from_step])
    if args.scenario:
        command.extend(["--scenario", args.scenario])
    if args.industry:
        command.extend(["--industry", args.industry])
    if args.usecase:
        command.extend(["--usecase", args.usecase])
    if args.size:
        command.extend(["--size", args.size])
    if args.clean:
        command.append("--clean")
    if args.dry_run:
        command.append("--dry-run")
    if args.continue_on_error:
        command.append("--continue-on-error")

    return run_step(f"Build mode: {args.mode}", command, base_env, args.dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="單一入口：準備 workshop demo 環境",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
    python scripts/00_admin_prepare_demo.py
    python scripts/00_admin_prepare_demo.py --mode foundry-only
    python scripts/00_admin_prepare_demo.py --mode foundry-iq
    python scripts/00_admin_prepare_demo.py --mode full --from-step 02
    python scripts/00_admin_prepare_demo.py --mode full --clean --industry Insurance --usecase \"Property insurance with claims processing\"
""",
    )
    parser.add_argument(
        "--mode",
        choices=["shared", "preload-only",
                 "foundry-only", "foundry-iq", "full"],
        default="shared",
        help="shared=共享環境預載+兩種 agent；preload-only=只做 scenario preload；其餘模式沿用舊 build pipeline",
    )
    parser.add_argument(
        "--scenarios",
        nargs="+",
        default=None,
        help="shared / preload-only 模式要準備的 scenario key；未指定時會處理 scenario catalog 中全部項目",
    )
    parser.add_argument(
        "--scenario", help="foundry-only / foundry-iq / full 模式使用的單一 scenario key")
    parser.add_argument("--from-step", help="full 模式可指定從哪一步開始，例如 02")
    parser.add_argument("--industry", type=str,
                        help="full 模式覆蓋 .env 的 INDUSTRY")
    parser.add_argument("--usecase", type=str, help="full 模式覆蓋 .env 的 USECASE")
    parser.add_argument(
        "--size", choices=["small", "medium", "large"], help="full 模式覆蓋 .env 的 DATA_SIZE")
    parser.add_argument("--clean", action="store_true",
                        help="full 模式清除並重建 Fabric 項目")
    parser.add_argument("--skip-cu-defaults", action="store_true")
    parser.add_argument("--skip-preload", action="store_true")
    parser.add_argument("--skip-foundry-only-agent", action="store_true")
    parser.add_argument("--skip-foundry-iq-agent", action="store_true")
    parser.add_argument("--skip-blob", action="store_true")
    parser.add_argument("--skip-search", action="store_true")
    parser.add_argument("--skip-foundry-knowledge", action="store_true")
    parser.add_argument("--skip-fabric", action="store_true")
    parser.add_argument("--clean-fabric", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()

    if args.mode in {"shared", "preload-only"}:
        args.scenarios = args.scenarios or get_default_shared_scenarios()
    else:
        args.scenarios = args.scenarios or []

    if args.mode in {"foundry-only", "foundry-iq", "full"} and args.scenarios:
        print("警告：build 模式只會使用 --scenario；--scenarios 會被忽略。")

    if args.mode in {"shared", "preload-only"} and args.skip_preload and args.skip_foundry_only_agent and args.skip_foundry_iq_agent:
        print("錯誤：全部步驟都被略過了，至少要執行一種 prepare 工作。")
        return 1

    print(f"\n{'='*60}")
    print("Admin Demo Prepare")
    print(f"{'='*60}")
    print(f"Mode：{args.mode}")
    if args.mode in {"shared", "preload-only"}:
        print(f"Scenarios：{', '.join(args.scenarios)}")
    elif args.scenario:
        print(f"Scenario：{args.scenario}")

    base_env = build_base_env()

    if not args.skip_cu_defaults:
        configured, message = ensure_content_understanding_defaults()
        if configured:
            print(f"  - Content Understanding defaults: {message}")
        else:
            print(f"  - Content Understanding defaults: 略過（{message}）")

    if args.mode == "preload-only":
        success = run_preload(args, base_env)
        return 0 if success else 1

    if args.mode == "shared":
        failed = False
        if not args.skip_preload:
            success = run_preload(args, base_env)
            failed = not success
            if not success and not args.continue_on_error:
                return 1

        success = run_agent_creation(args, base_env)
        failed = failed or not success

        print(f"\n{'='*60}")
        if failed:
            print("Prepare 完成，但部分步驟失敗")
            print(f"{'='*60}")
            return 1

        if args.dry_run:
            print("Dry run 完成")
        else:
            print("Demo prepare 完成")
            if len(args.scenarios) == 1 and args.scenarios[0] == "default":
                print("下一步：python scripts/08_test_foundry_agent.py --foundry-only")
                print("       或 python scripts/08b_test_foundry_iq_agent.py")
        print(f"{'='*60}")
        return 0

    success = run_build_mode(args, base_env)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
