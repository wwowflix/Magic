$ErrorActionPreference = "Stop"
Set-Location D:\MAGIC
python self_healing_runner_v5.py --phases 0-17
python tools/notion_sync_agent.py
