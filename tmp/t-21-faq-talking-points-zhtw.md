# T-21 FAQ / Talking Points 補強紀錄

## 產出

- `workshop/docs/03-understand/00-foundry-model.md`
- `workshop/docs/03-understand/02-foundry-agent.md`
- `workshop/docs/03-understand/03-foundry-tool.md`
- `workshop/docs/03-understand/04-control-plane.md`

## 完成內容

- 為 Foundry Model 補上 FAQ，聚焦 chat / embeddings 分工與 optional deployment 說法
- 為 Foundry Agent 補上 FAQ，聚焦 Foundry-managed definition 與 local runtime loop 分工
- 為 Foundry Tool 補上 FAQ，聚焦 strict contract、guardrails 與 extension layering
- 為 Control Plane 補上 FAQ，聚焦 project endpoint、Azure scaffolding 與 control plane / UX 差異
- 每頁都保留簡短 talking point，可直接拿來口頭說明

## 驗證

- Markdown diagnostics clean
- `python3 -m mkdocs build --config-file /workspaces/nc-iq-workshop/workshop/mkdocs.yml` 可通過