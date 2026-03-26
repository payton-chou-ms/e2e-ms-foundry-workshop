"""Admin helper to preload multiple scenarios into Blob, Search, Foundry IQ, and Fabric IQ."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

from load_env import load_all_env
from scenario_utils import build_scenario_env, list_scenarios, resolve_scenario

load_all_env()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)


def run_step(label: str, command: list[str], env: dict[str, str], dry_run: bool) -> None:
    printable = " ".join(command)
    print(f"  - {label}: {printable}")
    if dry_run:
        return

    result = subprocess.run(command, cwd=REPO_ROOT, text=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"步驟失敗：{label}")


def main():
    parser = argparse.ArgumentParser(description="Admin 預先載入多個 scenarios")
    parser.add_argument("--scenarios", nargs="*", default=[],
                        help="要預載的情境 key。若省略，會處理 scenario catalog 中全部項目")
    parser.add_argument("--skip-blob", action="store_true")
    parser.add_argument("--skip-search", action="store_true")
    parser.add_argument("--skip-foundry-iq", action="store_true")
    parser.add_argument("--skip-fabric", action="store_true")
    parser.add_argument("--clean-fabric", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    selected_keys = args.scenarios or [scenario["key"] for scenario in list_scenarios()]

    print(f"\n{'='*60}")
    print("Admin Scenario Preload")
    print(f"{'='*60}")
    print(f"Scenarios：{', '.join(selected_keys)}")

    for scenario_key in selected_keys:
        scenario = resolve_scenario(scenario_key)
        env = build_scenario_env(scenario)
        data_dir = os.path.join(REPO_ROOT, scenario["dataFolder"])
        custom_prepare_script = os.path.join(data_dir, "prepare_search_and_blob_assets.py")

        print(f"\n[{scenario_key}] {scenario['title']}")
        print(f"  Data Folder：{scenario['dataFolder']}")
        print(f"  Blob Container：{scenario['blobContainer']}")

        if not args.skip_blob and (not os.path.exists(custom_prepare_script) or args.skip_search):
            run_step(
                "Blob preload",
                [sys.executable, os.path.join(SCRIPT_DIR, "06a_upload_scenario_assets_to_blob.py"), "--scenario", scenario_key],
                env,
                args.dry_run,
            )

        if scenario["capabilities"].get("fabricIq") and not args.skip_fabric:
            fabric_cmd = [sys.executable, os.path.join(SCRIPT_DIR, "02_create_fabric_items.py"), "--scenario", scenario_key]
            if args.clean_fabric:
                fabric_cmd.append("--clean")
            run_step("Fabric items", fabric_cmd, env, args.dry_run)
            run_step(
                "Fabric load",
                [sys.executable, os.path.join(SCRIPT_DIR, "03_load_fabric_data.py"), "--scenario", scenario_key],
                env,
                args.dry_run,
            )
            run_step(
                "Schema prompt",
                [sys.executable, os.path.join(SCRIPT_DIR, "04_generate_agent_prompt.py"), "--scenario", scenario_key],
                env,
                args.dry_run,
            )

        if scenario["capabilities"].get("search") and not args.skip_search:
            if os.path.exists(custom_prepare_script):
                run_step(
                    "Scenario search prep",
                    [sys.executable, custom_prepare_script],
                    env,
                    args.dry_run,
                )
            else:
                run_step(
                    "Search upload",
                    [sys.executable, os.path.join(SCRIPT_DIR, "06_upload_to_search.py"), "--scenario", scenario_key],
                    env,
                    args.dry_run,
                )

        if scenario["capabilities"].get("foundryIq") and not args.skip_foundry_iq:
            run_step(
                "Foundry IQ knowledge",
                [sys.executable, os.path.join(SCRIPT_DIR, "06b_upload_to_foundry_knowledge.py"), "--scenario", scenario_key],
                env,
                args.dry_run,
            )

    print(f"\n{'='*60}")
    if args.dry_run:
        print("Dry run 完成")
    else:
        print("Scenario preload 完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()