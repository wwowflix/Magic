# ===============================
# MAGIC Unified Watchdog Script
# Runs Log Writer → File Watchdog → Auto-Recover in a loop
# ===============================

while ($true) {

    Write-Host "🔄 Starting MAGIC self-healing cycle..." -ForegroundColor Cyan

    # Step 1: Log Writer Agent
    python agents\awareness\log_writer_agent.py
    Write-Host "✅ Log Writer Agent completed." -ForegroundColor Green

    # Step 2: File Watchdog Agent
    python agents\awareness\file_watchdog_agent.py
    Write-Host "✅ File Watchdog Agent completed." -ForegroundColor Green

    # Step 3: Auto-Recover Agent
    python scripts\phase17\module_C\17C_auto_recover_agent_READY.py
    Write-Host "✅ Auto-Recover Agent completed." -ForegroundColor Green

    Write-Host "✅ Cycle complete. Next scan in 2 minutes..." -ForegroundColor Yellow

    Start-Sleep -Seconds 120
}
