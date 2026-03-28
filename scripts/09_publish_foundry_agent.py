"""Foundry Agent 發布前檢查腳本。"""

import argparse
import json
import os
import subprocess
import sys

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from load_env import load_all_env
from optional_demo_utils import print_demo_header
from foundry_trace import configure_foundry_tracing


def warn(message: str) -> None:
    print(f"[WARN] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def info(message: str) -> None:
    print(message)


def exit_skip(message: str, strict: bool) -> None:
    warn(message)
    if strict:
        sys.exit(1)
    print("[SKIP] 發布流程保留給手動 UI 操作。主 workshop 流程可以繼續。")
    sys.exit(0)


def run_az(command_args):
    result = subprocess.run(
        ["az", *command_args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def parse_project_endpoint(endpoint: str):
    marker = ".services.ai.azure.com/api/projects/"
    if marker not in endpoint:
        return None, None

    left, project_name = endpoint.split(marker, 1)
    account_name = left.split("https://", 1)[-1]
    return account_name, project_name.strip("/")


def resolve_agent_inputs(agent_id_arg: str, agent_name_arg: str, data_folder: str):
    agent_id = agent_id_arg or os.getenv("FOUNDRY_AGENT_ID")
    agent_name = agent_name_arg or os.getenv("FOUNDRY_AGENT_NAME")

    if not data_folder:
        return agent_id, agent_name

    config_dir = os.path.join(os.path.abspath(data_folder), "config")
    if not os.path.exists(config_dir):
        config_dir = os.path.abspath(data_folder)

    agent_ids_path = os.path.join(config_dir, "agent_ids.json")
    if os.path.exists(agent_ids_path):
        with open(agent_ids_path) as handle:
            agent_ids = json.load(handle)
        agent_id = agent_id or agent_ids.get("agent_id")
        agent_name = agent_name or agent_ids.get("agent_name")

    return agent_id, agent_name


parser = argparse.ArgumentParser()
parser.add_argument("--agent-id", default="")
parser.add_argument("--agent-name", default="")
parser.add_argument("--teams", action="store_true",
                    help="列印 Teams / Microsoft 365 Copilot 檢查清單")
parser.add_argument("--strict", action="store_true",
                    help="若缺少前置條件，回傳非 0 結束碼")
args = parser.parse_args()


load_all_env()

ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
DATA_FOLDER = os.getenv("DATA_FOLDER")

print_demo_header(
    title="Foundry Agent 發布前檢查",
    description="檢查現有 Foundry agent 是否已準備好進入手動發布流程。",
    env_items=[
        {"name": "AZURE_AI_PROJECT_ENDPOINT", "value": ENDPOINT},
        {"name": "DATA_FOLDER", "value": DATA_FOLDER},
        {"name": "FOUNDRY_AGENT_ID", "value": os.getenv("FOUNDRY_AGENT_ID")},
        {"name": "FOUNDRY_AGENT_NAME",
            "value": os.getenv("FOUNDRY_AGENT_NAME")},
    ],
)

if not ENDPOINT:
    exit_skip("未設定 AZURE_AI_PROJECT_ENDPOINT。請先執行 'azd up'。", args.strict)

agent_id, agent_name = resolve_agent_inputs(
    args.agent_id, args.agent_name, DATA_FOLDER)
if not agent_id and not agent_name:
    exit_skip(
        "找不到 agent 識別資訊。請先執行 admin_prepare_docs_demo.py 或 admin_prepare_docs_data_demo.py 建立 agent，或自行提供 --agent-id / --agent-name。",
        args.strict,
    )

account_name, project_name = parse_project_endpoint(ENDPOINT)
info("這支腳本不會自動發布，只會檢查前置條件並列出下一步手動操作。")
ok(f"已載入 Project endpoint：{ENDPOINT}")
if account_name and project_name:
    ok(f"Foundry account：{account_name}")
    ok(f"Foundry project：{project_name}")
else:
    warn("無法從 endpoint 完整解析 account 與 project 名稱。")

print("\n檢查目標 agent...")
credential = DefaultAzureCredential()

try:
    project_client = AIProjectClient(endpoint=ENDPOINT, credential=credential)
except Exception as exc:
    exit_skip(f"無法初始化 AIProjectClient：{exc}", args.strict)

trace_session = configure_foundry_tracing(
    project_client=project_client,
    scenario_name="09_publish_foundry_agent",
    service_name="e2e-ms-foundry-workshop.agent-publish",
)

if trace_session.enabled:
    print("[OK] 已啟用 Foundry tracing")
elif trace_session.warning:
    print(f"警告：{trace_session.warning}")

try:
    with project_client:
        if agent_id:
            with trace_session.span("get-agent"):
                agent = project_client.agents.get(agent_id)
        else:
            with trace_session.span("get-agent"):
                agent = project_client.agents.get(agent_name)
except Exception as exc:
    identifier = agent_id or agent_name
    exit_skip(f"無法解析 agent '{identifier}'：{exc}", args.strict)

ok(f"已找到 Agent：{agent.name}")
ok(f"Agent ID：{agent.id}")

print("\n檢查 Azure CLI 登入狀態...")
code, stdout, stderr = run_az(["account", "show", "-o", "json"])
if code != 0:
    warn("Azure CLI 尚未準備好，或尚未登入。")
    if stderr:
        print(f"       {stderr}")
else:
    try:
        account = json.loads(stdout)
        ok(f"Azure 訂用帳戶：{account.get('name', '<unknown>')}")
        ok(f"訂用帳戶 ID：{account.get('id', '<unknown>')}")
        ok(f"Tenant ID：{account.get('tenantId', '<unknown>')}")
    except json.JSONDecodeError:
        warn("無法從 Azure CLI 輸出解析帳戶資訊。")

    print("\n檢查 Microsoft.BotService provider 註冊狀態...")
code, stdout, stderr = run_az(["provider", "show", "--namespace",
                              "Microsoft.BotService", "--query", "registrationState", "-o", "tsv"])
if code != 0:
    warn("無法確認 Microsoft.BotService provider 的註冊狀態。")
    if stderr:
        print(f"       {stderr}")
else:
    state = stdout or "<unknown>"
    if state.lower() == "registered":
        ok("Microsoft.BotService provider 已註冊")
    else:
        warn(f"Microsoft.BotService provider 狀態：{state}")
        print("       在註冊完成前，發布到 Teams / Microsoft 365 Copilot 可能會失敗。")

    print("\n發布指引（手動 UI 流程）：")
    print("  1. 開啟 Foundry 入口網站，選擇目標 agent 版本。")
    print("  2. 先把 agent 發布成 Agent Application。")
    print("  3. 發布後，記下新的應用程式身分與 endpoint。")
    print("  4. 重新設定工具所需下游 Azure 資源的 RBAC。")
    print("  5. 如有需要，再繼續執行 'Publish to Teams and Microsoft 365 Copilot'。")

    print("\nRBAC 提醒：")
    print("  - 發布後會建立新的 Agent Application 身分。")
    print("  - 原本在 project 中可用的工具權限，發布後可能會失效，直到重新指派 RBAC。")
    print("  - 請重新檢查 Azure AI Search、Storage 與其他已連接的 Azure 資源。")

if args.teams:
    print("\nTeams / Microsoft 365 Copilot 檢查清單：")
    print("  1. 先確認這個 agent 版本已在 Foundry 中測試成功。")
    print("  2. 確認你可以在目前訂用帳戶中建立 Azure Bot Service 資源。")
    print("  3. 先準備好中繼資料：名稱、短描述、完整描述、發行者、網站、隱私權網址、條款網址。")
    print("  4. 小型試點可選 Individual scope；若有管理員核准可選 Organization scope。")
    print("  5. 打包後，先在 Teams 內測試，再擴大發佈。")
    print("  6. 目前已發布體驗中的串流回應與引用能力仍有限制。")

print("\n結果：")
print("  這支腳本只完成發布前檢查。")
print("  請改用 UI 完成最後發布，讓 workshop 保持簡單、聚焦示範。")
