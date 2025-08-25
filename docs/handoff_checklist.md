# Handoff Checklist — MAGIC v1.0
Date: 2025-08-25 16:05:00 +05:30
Commit: 13ab0cdc

## 1) How to Run
- Activate venv, then: python .\self_healing_runner_v5.py --manifest .\phase_manifest.json --summary-dir .\outputs\full_run\<ts>
- Cleanup agent (manual trigger): python .\tools\cleanup_agent.py <root> --emit-retry --verbose
- Retry queue: python .\tools\retry_queue.py

## 2) Automation Signals (paths)
- Master summary: $(D:\MAGIC\outputs\full_run\20250825_155813\phase_master_summary.tsv)
- Remediation metrics: outputs\remediation\remediate_metrics.json
- AI suggestions: outputs\remediation\ai_suggestions\*.jsonl
- Patches: outputs\remediation\patches\*.diff (backups in outputs\remediation\backups\)
- Alerts log: outputs\remediation\alerts_sent.jsonl

## 3) Ops Env Vars
- GitHub: GH_REPO, GH_TOKEN
- Notion: NOTION_TOKEN, NOTION_DATABASE_ID
- Quality gate (optional): REQUIRE_QUALITY=1, MIN_SUCCESS=80

## 4) Playbooks
- Failed script flow: retry → orchestrator → AI suggestion → patch → runner subset → alerts if still FAIL
- Cleanup flow: stale → cleanup_agent → retry_request → retry_queue

## 5) Gates to Run
- Week 10: 	ools\gates\pending_gate.Tests.ps1
- Week 11: week11_gate_v3/4/5/6.Tests.ps1
- Week 12: week12_gate_v1.Tests.ps1, week12_gate_v2.Tests.ps1

## 6) Known Issues / TODOs
- Post-mortem: add top failures + owners
- Confirm tokens on prod runners
- Set CI step to run gates with REQUIRE_QUALITY=1

