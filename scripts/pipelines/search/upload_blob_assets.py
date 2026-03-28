"""Upload scenario source assets into the scenario-specific blob container."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, SCRIPTS_ROOT)

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, ContentSettings

from credential_utils import get_credential
from load_env import load_all_env
from scenario_utils import resolve_data_paths, resolve_scenario

load_all_env()


ASSET_DIRECTORIES = ["documents", "tables", "input", "intermediate", "output"]


def guess_content_type(path: Path) -> str | None:
    explicit = {
        ".md": "text/markdown",
        ".json": "application/json",
        ".csv": "text/csv",
        ".pdf": "application/pdf",
        ".html": "text/html",
        ".txt": "text/plain",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    if path.suffix.lower() in explicit:
        return explicit[path.suffix.lower()]
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed


def iter_asset_files(data_dir: Path) -> list[Path]:
    files: list[Path] = []
    for asset_dir in ASSET_DIRECTORIES:
        root = data_dir / asset_dir
        if not root.exists():
            continue
        files.extend(sorted(path for path in root.rglob("*") if path.is_file()))
    return files


def main():
    parser = argparse.ArgumentParser(description="把情境素材上傳到對應的 Blob container")
    parser.add_argument("--scenario", default=os.getenv("SCENARIO_KEY", ""))
    parser.add_argument("--data-folder", default=os.getenv("DATA_FOLDER"))
    args = parser.parse_args()

    scenario = resolve_scenario(args.scenario or None, args.data_folder, require_capability="blob")
    paths = resolve_data_paths(scenario)
    data_dir = paths["data_dir"]
    config_dir = paths["config_dir"]

    blob_endpoint = os.getenv("AZURE_STORAGE_BLOB_ENDPOINT")
    if not blob_endpoint:
        print("錯誤：未設定 AZURE_STORAGE_BLOB_ENDPOINT")
        print("      請先執行 'azd up' 部署 Azure 資源")
        sys.exit(1)

    container_name = os.getenv("AZURE_STORAGE_BLOB_CONTAINER") or scenario["blobContainer"]
    asset_files = iter_asset_files(data_dir)
    if not asset_files:
        print("錯誤：找不到可上傳的 scenario 素材")
        print(f"      查找位置：{data_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("上傳 Scenario Assets 到 Blob Storage")
    print(f"{'='*60}")
    print(f"Scenario：{scenario['key']}")
    print(f"Data Folder：{scenario['dataFolder']}")
    print(f"Blob Endpoint：{blob_endpoint}")
    print(f"Blob Container：{container_name}")
    print(f"檔案數：{len(asset_files)}")

    service_client = BlobServiceClient(account_url=blob_endpoint, credential=get_credential())
    container_client = service_client.get_container_client(container_name)

    try:
        container_client.get_container_properties()
    except ResourceNotFoundError:
        print(f"注意：找不到 Blob container '{container_name}'，改為自動建立")
        container_client.create_container()

    for existing_blob in container_client.list_blobs():
        container_client.delete_blob(existing_blob.name)

    uploaded_files = []
    for asset_file in asset_files:
        blob_name = asset_file.relative_to(data_dir).as_posix()
        content_type = guess_content_type(asset_file)
        with asset_file.open("rb") as handle:
            kwargs = {"overwrite": True}
            if content_type:
                kwargs["content_settings"] = ContentSettings(content_type=content_type)
            container_client.upload_blob(name=blob_name, data=handle, **kwargs)

        uploaded_files.append(
            {
                "path": blob_name,
                "source": asset_file.relative_to(data_dir).as_posix(),
                "url": f"{blob_endpoint.rstrip('/')}/{container_name}/{blob_name}",
            }
        )

    metadata = {
        "scenario_key": scenario["key"],
        "data_folder": scenario["dataFolder"],
        "blob_endpoint": blob_endpoint,
        "blob_container": container_name,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(uploaded_files),
        "files": uploaded_files,
    }
    manifest_path = config_dir / "blob_manifest.json"
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, ensure_ascii=False)

    print(f"[OK] 已上傳 {len(uploaded_files)} 個檔案")
    print(f"[OK] 已把 manifest 寫入：{manifest_path}")


if __name__ == "__main__":
    main()