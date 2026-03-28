"""Helpers for resolving active scenarios and their storage metadata."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCENARIO_CATALOG_PATH = REPO_ROOT / "data" / "scenario_catalog.json"


def load_scenario_catalog() -> dict:
    with SCENARIO_CATALOG_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)



def normalize_container_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9-]", "-", value.lower())
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    normalized = normalized[:63].strip("-")
    if len(normalized) < 3:
        normalized = f"scn-{normalized}".strip("-")
    return normalized[:63]



def normalize_resource_token(value: str, max_length: int | None = None) -> str:
    normalized = re.sub(r"[^a-z0-9-]", "-", value.lower())
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    if not normalized:
        normalized = "demo"
    if max_length is not None:
        normalized = normalized[:max_length].strip("-")
    return normalized or "demo"



def scenario_resource_suffix(scenario_key: str) -> str:
    return scenario_key.replace("_", "-")



def scenario_short_name(scenario: dict | str) -> str:
    if isinstance(scenario, dict):
        short_name = scenario.get("shortName")
        scenario_key = scenario["key"]
    else:
        short_name = None
        scenario_key = scenario

    if short_name:
        return normalize_resource_token(short_name, max_length=24)

    aliases = {
        "default": "telco",
        "telecommunications": "telco",
        "retail_launch_incident": "retail-launch",
        "contract_keyword_review": "contract-review",
        "manufacturing": "mfg",
    }
    if scenario_key in aliases:
        return aliases[scenario_key]

    cleaned_key = scenario_key.removeprefix("static_")
    token_aliases = {
        "telecommunications": "telco",
        "manufacturing": "mfg",
    }
    parts = [token_aliases.get(part, part) for part in cleaned_key.split("_") if part]
    return normalize_resource_token("-".join(parts), max_length=24)



def solution_short_name(value: str | None, max_length: int = 6) -> str:
    normalized = normalize_resource_token(value or "demo")
    compact = re.sub(r"[^a-z0-9]", "", normalized)
    if len(compact) <= max_length:
        return compact or "demo"
    return compact[-max_length:]



def build_deployment_name(base_name: str | None, scenario: dict | str, role: str, *, max_length: int = 64) -> str:
    scenario_slug = scenario_short_name(scenario)
    role_slug = normalize_resource_token(role, max_length=20)
    parts = [solution_short_name(base_name), scenario_slug, role_slug]
    return normalize_resource_token("-".join(part for part in parts if part), max_length=max_length)



def build_scenario_resource_name(base_name: str, scenario_key: str, separator: str = "-") -> str:
    suffix = scenario_resource_suffix(scenario_key)
    if base_name.endswith(f"{separator}{suffix}"):
        return base_name
    return f"{base_name}{separator}{suffix}"



def list_scenarios(capability: str | None = None) -> list[dict]:
    catalog = load_scenario_catalog()
    scenarios = catalog.get("scenarios", [])
    if not capability:
        return scenarios
    return [
        scenario
        for scenario in scenarios
        if scenario.get("capabilities", {}).get(capability, False)
    ]



def _match_catalog_entry_by_data_folder(data_folder: str | None, catalog: dict) -> dict | None:
    if not data_folder:
        return None

    data_path = Path(data_folder).expanduser()
    if not data_path.is_absolute():
        data_path = (REPO_ROOT / data_path).resolve()
    else:
        data_path = data_path.resolve()

    for scenario in catalog.get("scenarios", []):
        scenario_path = (REPO_ROOT / scenario["dataFolder"]).resolve()
        if scenario_path == data_path:
            return scenario
    return None



def _derive_dynamic_scenario(data_folder: str) -> dict:
    data_path = Path(data_folder).expanduser()
    if not data_path.is_absolute():
        data_path = (REPO_ROOT / data_path).resolve()
    else:
        data_path = data_path.resolve()

    try:
        relative_path = data_path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        relative_path = data_path.as_posix()
    scenario_key = re.sub(r"[^a-z0-9_]+", "_", data_path.name.lower()).strip("_")
    if not scenario_key:
        scenario_key = "custom"

    return {
        "key": scenario_key,
        "title": data_path.name,
        "shortName": normalize_resource_token(scenario_key, max_length=24),
        "dataFolder": relative_path,
        "blobContainer": normalize_container_name(scenario_key),
        "capabilities": {
            "blob": True,
            "search": True,
            "foundryIq": True,
            "fabricIq": True,
        },
        "dynamic": True,
    }



def resolve_scenario(
    scenario_key: str | None = None,
    data_folder: str | None = None,
    *,
    require_capability: str | None = None,
) -> dict:
    catalog = load_scenario_catalog()
    explicit_key = bool(scenario_key)
    explicit_data_folder = bool(data_folder)
    selected_key = scenario_key or os.getenv("SCENARIO_KEY")
    selected_data_folder = data_folder or os.getenv("DATA_FOLDER")

    scenario = None
    if selected_key:
        scenario = next((item for item in catalog.get("scenarios", []) if item["key"] == selected_key), None)
        if scenario is None:
            if selected_data_folder:
                matched_scenario = _match_catalog_entry_by_data_folder(selected_data_folder, catalog)
                scenario = matched_scenario or _derive_dynamic_scenario(selected_data_folder)
                scenario["key"] = selected_key
            else:
                raise ValueError(f"找不到 scenario key：{selected_key}")
        elif explicit_data_folder:
            matched_scenario = _match_catalog_entry_by_data_folder(selected_data_folder, catalog)
            if matched_scenario is None:
                scenario = _derive_dynamic_scenario(selected_data_folder)
                scenario["key"] = selected_key
            elif matched_scenario["key"] == selected_key:
                scenario = matched_scenario
        elif not explicit_key and selected_data_folder:
            matched_scenario = _match_catalog_entry_by_data_folder(selected_data_folder, catalog)
            if matched_scenario and matched_scenario["key"] == selected_key:
                scenario = matched_scenario
    else:
        scenario = _match_catalog_entry_by_data_folder(selected_data_folder, catalog)
        if scenario is None and selected_data_folder:
            scenario = _derive_dynamic_scenario(selected_data_folder)

    if scenario is None:
        default_key = catalog.get("defaultScenario", "default")
        scenario = next(item for item in catalog.get("scenarios", []) if item["key"] == default_key)

    if require_capability and not scenario.get("capabilities", {}).get(require_capability, False):
        raise ValueError(f"情境 '{scenario['key']}' 不支援 {require_capability} 流程")

    abs_data_folder = (REPO_ROOT / scenario["dataFolder"]).resolve()
    return {
        **scenario,
        "dataFolder": scenario["dataFolder"],
        "absoluteDataFolder": str(abs_data_folder),
    }



def resolve_data_paths(scenario: dict) -> dict[str, Path]:
    data_dir = Path(scenario["absoluteDataFolder"])
    config_dir = data_dir / "config"
    docs_dir = data_dir / "documents"
    tables_dir = data_dir / "tables"

    if not config_dir.exists():
        config_dir = data_dir
    if not docs_dir.exists():
        docs_dir = data_dir

    return {
        "data_dir": data_dir,
        "config_dir": config_dir,
        "docs_dir": docs_dir,
        "tables_dir": tables_dir,
    }



def build_scenario_env(scenario: dict, extra: dict | None = None) -> dict[str, str]:
    env = dict(os.environ)
    env["SCENARIO_KEY"] = scenario["key"]
    env["DATA_FOLDER"] = scenario["dataFolder"]
    env["AZURE_STORAGE_BLOB_CONTAINER"] = scenario["blobContainer"]
    if extra:
        env.update(extra)
    return env
