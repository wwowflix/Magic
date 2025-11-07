import os, pandas as pd

data = [
    [1, "Rebuild missing Phase 11E scripts", "Regenerate placeholder or recovery versions for all 7 FAIL scripts.", "python tools/rebuild_missing_phase.py --phase 11 --module E", "scripts/phase11/module_e", "All missing scripts restored"],
    [2, "Run self-healing runner on fresh manifest", "Validate all READY scripts after rebuild.", "python tools/self_healing_runner_v5.py --manifest outputs/reports/phase11_module_E_manifest.json", "tools", "✅ Summary TSV with PASS/FAIL status"],
    [3, "Commit all changes to GitHub", "Stage, commit, and push the full Phase 11E recovery.", "git add -A; git commit -m 'fix: phase11E rebuild'; git push", "repo root", "Phase 11E synced with repo"],
    [4, "Sync latest status to Notion", "Push updated statuses to Notion tracker database.", "python tools/notion_sync_agent.py", "tools", "✅ Notion reflects all new states"],
    [5, "Generate updated gap report", "Run Magic gap scanner for phase 0-18.", "python tools/magic_gap_report.py --snapshot outputs/reports/magic_ready_snapshot.txt --phases 0-18", "tools", "E:/MAGIC/outputs/reports/magic_gap_report.tsv"],
    [6, "Activate auto daily health check", "Schedule Windows Task to run self-heal check daily at 9:00 AM.", 'Register-ScheduledJob -Name "MagicSelfHeal" -ScriptBlock { python E:/MAGIC/tools/self_healing_runner_v5.py --manifest E:/MAGIC/outputs/reports/magic_ready_manifest.json } -Trigger (New-JobTrigger -Daily -At 09:00)', "Windows Scheduler", "Daily self-heal check automated"]
]

df = pd.DataFrame(data, columns=['Step','Objective / Why','Detailed Action','PowerShell / Python Command','Target Folder','Expected Output'])
os.makedirs('E:/MAGIC/outputs/reports', exist_ok=True)
path = 'E:/MAGIC/outputs/reports/MAGIC_Next_Action_Plan.xlsx'
df.to_excel(path, index=False)
print(f'✅ Excel written to: {path}')
