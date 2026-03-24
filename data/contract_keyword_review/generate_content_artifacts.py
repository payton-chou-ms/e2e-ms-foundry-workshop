"""Generate comparable contract content and rule lists for the contract review demo.

This script prefers Azure Content Understanding for Office documents and falls back
to local Office XML extraction when the Azure endpoint is unavailable. The output
files are intentionally checked into the demo folder so the live tour can consume
pre-generated artifacts without calling Azure at runtime.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]


class LiveCuError(RuntimeError):
    """Expected live Azure Content Understanding failure."""


def _env_file_has_core_azure_values(env_path: Path) -> bool:
    try:
        content = env_path.read_text(encoding="utf-8")
    except OSError:
        return False

    return any(
        token in content
        for token in (
            "AZURE_AI_PROJECT_ENDPOINT=",
            "AZURE_AI_SEARCH_ENDPOINT=",
            "AZURE_AI_ENDPOINT=",
        )
    )


def load_all_env() -> None:
    import os

    azure_dir = ROOT_DIR / ".azure"
    shell_env_name = os.environ.get("AZURE_ENV_NAME", "").strip()
    default_env_name = ""

    config_path = azure_dir / "config.json"
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        default_env_name = str(config.get("defaultEnvironment", "")).strip()

    candidate_env_names = []
    if shell_env_name:
        candidate_env_names.append(shell_env_name)
    if default_env_name and default_env_name not in candidate_env_names:
        candidate_env_names.append(default_env_name)

    for env_name in candidate_env_names:
        env_path = azure_dir / env_name / ".env"
        if env_path.exists() and _env_file_has_core_azure_values(env_path):
            load_dotenv(env_path)
            break

    project_env = ROOT_DIR / ".env"
    if project_env.exists():
        load_dotenv(project_env, override=False)


def resolve_env_value(*names: str) -> tuple[str | None, str | None]:
    import os

    for name in names:
        value = os.getenv(name)
        if value:
            return value, name
    return None, None


load_all_env()

IMPORT_ERROR = None

try:
    from azure.ai.contentunderstanding import ContentUnderstandingClient
    from azure.core.credentials import AzureKeyCredential
    from azure.identity import DefaultAzureCredential
except ImportError as exc:  # pragma: no cover - depends on local runtime
    IMPORT_ERROR = exc


WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
SHEET_NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


@dataclass(frozen=True)
class InputFile:
    source_path: Path
    markdown_path: Path
    json_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cu-analyzer-id",
        default="prebuilt-layout",
        help="inline data upload 時使用的 Content Understanding analyzer id。預設為 prebuilt-layout。",
    )
    parser.add_argument(
        "--use-local-fallback",
        action="store_true",
        help="Azure Content Understanding 無法使用時，自動退回本機 Office XML 萃取。",
    )
    parser.add_argument(
        "--require-live-cu",
        action="store_true",
        help="強制要求使用真實 Azure Content Understanding；若服務回空內容或環境未就緒，直接失敗，不退回本機萃取。",
    )
    parser.add_argument(
        "--processing-location",
        choices=["geography", "dataZone", "global"],
        help="選填：覆蓋 Content Understanding 的 processing location。",
    )
    return parser.parse_args()


def build_input_files(base_dir: Path) -> list[InputFile]:
    intermediate_dir = base_dir / "intermediate"
    return [
        InputFile(
            source_path=base_dir / "input" / "06-合約範本.docx",
            markdown_path=intermediate_dir / "06-合約範本-可比較內容.md",
            json_path=intermediate_dir / "06-合約範本-可比較段落.json",
        ),
        InputFile(
            source_path=base_dir / "input" / "07-待審閱合約.docx",
            markdown_path=intermediate_dir / "07-待審閱合約-可比較內容.md",
            json_path=intermediate_dir / "07-待審閱合約-可比較段落.json",
        ),
    ]


def create_client() -> ContentUnderstandingClient | None:
    if IMPORT_ERROR is not None:
        return None

    endpoint, _ = resolve_env_value(
        "CONTENTUNDERSTANDING_ENDPOINT",
        "CONTENT_UNDERSTANDING_ENDPOINT",
        "AZURE_AI_ENDPOINT",
    )
    if not endpoint:
        return None

    key, _ = resolve_env_value(
        "CONTENTUNDERSTANDING_KEY",
        "CONTENT_UNDERSTANDING_KEY",
        "AZURE_AI_KEY",
    )
    credential = AzureKeyCredential(key) if key else DefaultAzureCredential()
    return ContentUnderstandingClient(endpoint=endpoint, credential=credential)


def analyze_with_content_understanding(
    client: ContentUnderstandingClient,
    file_path: Path,
    analyzer_id: str,
    processing_location: str | None,
) -> str:
    with open(file_path, "rb") as handle:
        file_bytes = handle.read()

    poller = client.begin_analyze_binary(
        analyzer_id=analyzer_id,
        binary_input=file_bytes,
        processing_location=processing_location,
    )
    result = poller.result()
    if not getattr(result, "contents", None):
        raise LiveCuError(
            f"Azure Content Understanding 沒有回傳內容：{file_path.name}。"
            f"目前 analyzer `{analyzer_id}` 沒有產生內容；"
            "請改用可產生 markdown 的 analyzer，例如 prebuilt-layout、prebuilt-read 或 prebuilt-document。"
        )

    markdown = getattr(result.contents[0], "markdown", "") or ""
    normalized = markdown.strip()
    if not normalized or normalized == "```text\n\n```":
        raise LiveCuError(
            f"Azure Content Understanding markdown 為空：{file_path.name}。"
            f"目前 analyzer `{analyzer_id}` 沒有產生可用 markdown。"
        )
    return markdown


def paragraph_from_markdown(markdown: str) -> list[dict[str, str | int]]:
    blocks: list[dict[str, str | int]] = []
    raw_blocks = [block.strip() for block in markdown.split("\n\n")]
    for index, block in enumerate(raw_blocks, start=1):
        if not block:
            continue
        text = " ".join(line.strip() for line in block.splitlines() if line.strip())
        if not text:
            continue
        blocks.append(
            {
                "id": index,
                "kind": "markdown-block",
                "text": text,
            }
        )
    return blocks


def _word_text(node: ET.Element) -> str:
    texts: list[str] = []
    for text_node in node.findall(".//w:t", WORD_NS):
        texts.append(text_node.text or "")
    return "".join(texts).strip()


def extract_docx_locally(file_path: Path) -> list[dict[str, str | int]]:
    blocks: list[dict[str, str | int]] = []
    with ZipFile(file_path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find("w:body", WORD_NS)
    if body is None:
        return blocks

    counter = 1
    for child in list(body):
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            text = _word_text(child)
            if text:
                blocks.append({"id": counter, "kind": "paragraph", "text": text})
                counter += 1
            continue

        if tag == "tbl":
            rows: list[str] = []
            for row in child.findall(".//w:tr", WORD_NS):
                cells: list[str] = []
                for cell in row.findall("w:tc", WORD_NS):
                    cell_text = _word_text(cell)
                    if cell_text:
                        cells.append(cell_text)
                if cells:
                    rows.append(" | ".join(cells))
            if rows:
                blocks.append(
                    {
                        "id": counter,
                        "kind": "table",
                        "text": " / ".join(rows),
                    }
                )
                counter += 1
    return blocks


def comparable_markdown(title: str, paragraphs: Iterable[dict[str, str | int]]) -> str:
    lines = [f"# {title}", ""]
    for item in paragraphs:
        lines.append(f"{item['id']}. {item['text']}")
    lines.append("")
    return "\n".join(lines)


def save_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_shared_strings(archive: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []

    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    shared: list[str] = []
    for si in root.findall("a:si", SHEET_NS):
        texts: list[str] = []
        for node in si.iterfind(".//a:t", SHEET_NS):
            texts.append(node.text or "")
        shared.append("".join(texts))
    return shared


def sheet_cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    value_node = cell.find("a:v", SHEET_NS)
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//a:t", SHEET_NS)).strip()
    if value_node is None:
        return ""
    raw = (value_node.text or "").strip()
    if cell_type == "s" and raw.isdigit():
        index = int(raw)
        if index < len(shared_strings):
            return shared_strings[index].strip()
    return raw


def parse_rules_workbook(file_path: Path) -> list[dict[str, str]]:
    with ZipFile(file_path) as archive:
        shared_strings = build_shared_strings(archive)
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))

        relationship_map = {
            rel.attrib["Id"]: f"xl/{rel.attrib['Target']}"
            for rel in relationships
            if "Id" in rel.attrib and "Target" in rel.attrib
        }

        target_path: str | None = None
        sheets = workbook.find("a:sheets", SHEET_NS)
        for sheet in list(sheets) if sheets is not None else []:
            if sheet.attrib.get("name") != "規則":
                continue
            relationship_id = sheet.attrib.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            )
            target_path = relationship_map.get(relationship_id)
            break

        if not target_path:
            raise RuntimeError("找不到規則工作表")

        root = ET.fromstring(archive.read(target_path))
        rows = root.findall(".//a:sheetData/a:row", SHEET_NS)
        if not rows:
            return []

        header_row = rows[0]
        headers = [
            sheet_cell_value(cell, shared_strings).strip()
            for cell in header_row.findall("a:c", SHEET_NS)
        ]

        items: list[dict[str, str]] = []
        for row in rows[1:]:
            values = [
                sheet_cell_value(cell, shared_strings).replace("\n", " ").strip()
                for cell in row.findall("a:c", SHEET_NS)
            ]
            if not any(values):
                continue

            padded_values = values + [""] * (len(headers) - len(values))
            item = {
                header or f"column_{index + 1}": padded_values[index]
                for index, header in enumerate(headers)
            }
            items.append(item)
        return items


def rules_to_markdown(items: list[dict[str, str]]) -> str:
    lines = ["# 規則清單", ""]
    lines.append("| 規則 | 規則名稱 | 適用合約類型 | 關鍵字 | 可/不可改 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for item in items:
        lines.append(
            "| {rule} | {name} | {contract_type} | {keywords} | {editable} |".format(
                rule=item.get("規則", ""),
                name=item.get("規則名稱", "").replace("|", "、"),
                contract_type=item.get("適用合約類型", "").replace("|", "、"),
                keywords=item.get("關鍵字", "").replace("|", "、"),
                editable=item.get("可/不可改", "").replace("|", "、"),
            )
        )
    lines.append("")
    return "\n".join(lines)


def generate_doc_artifacts(
    client: ContentUnderstandingClient | None,
    input_file: InputFile,
    cu_analyzer_id: str,
    processing_location: str | None,
    use_local_fallback: bool,
    require_live_cu: bool,
) -> None:
    source_mode = "local-office-xml"
    paragraphs: list[dict[str, str | int]]
    print(f"[INFO] 處理文件：{input_file.source_path.name}", flush=True)

    if client is not None:
        try:
            print("[INFO] 使用 Data 模式呼叫 CU", flush=True)
            markdown = analyze_with_content_understanding(
                client=client,
                file_path=input_file.source_path,
                analyzer_id=cu_analyzer_id,
                processing_location=processing_location,
            )
            source_mode = f"content-understanding-data:{cu_analyzer_id}"
            paragraphs = paragraph_from_markdown(markdown)
        except LiveCuError:
            if require_live_cu or not use_local_fallback:
                raise
            print("[WARN] Live CU 失敗，改用本機 Office XML fallback", flush=True)
            paragraphs = extract_docx_locally(input_file.source_path)
    else:
        if require_live_cu:
            raise RuntimeError(
                "找不到可用的 Azure Content Understanding client。"
                "請先確認已安裝 SDK、已登入 Azure，且 `AZURE_ENV_NAME` 或 `.azure/<env>/.env` 指向正確環境。"
            )
        paragraphs = extract_docx_locally(input_file.source_path)

    title = input_file.source_path.stem
    input_file.markdown_path.write_text(
        comparable_markdown(title=title, paragraphs=paragraphs),
        encoding="utf-8",
    )
    save_json(
        input_file.json_path,
        {
            "source": input_file.source_path.name,
            "generated_by": source_mode,
            "paragraphs": paragraphs,
        },
    )
    print(f"[INFO] 完成：{input_file.source_path.name} ({source_mode})", flush=True)


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    client = create_client()

    for input_file in build_input_files(base_dir):
        generate_doc_artifacts(
            client=client,
            input_file=input_file,
            cu_analyzer_id=args.cu_analyzer_id,
            processing_location=args.processing_location,
            use_local_fallback=args.use_local_fallback,
            require_live_cu=args.require_live_cu,
        )

    rules = parse_rules_workbook(base_dir / "input" / "04-規則檔.xlsx")
    save_json(base_dir / "intermediate" / "04-規則清單.json", rules)
    (base_dir / "intermediate" / "04-規則清單.md").write_text(
        rules_to_markdown(rules),
        encoding="utf-8",
    )

    print("已產生可比較內容與規則清單：")
    print("- intermediate/06-合約範本-可比較內容.md")
    print("- intermediate/06-合約範本-可比較段落.json")
    print("- intermediate/07-待審閱合約-可比較內容.md")
    print("- intermediate/07-待審閱合約-可比較段落.json")
    print("- intermediate/04-規則清單.json")
    print("- intermediate/04-規則清單.md")


if __name__ == "__main__":
    main()