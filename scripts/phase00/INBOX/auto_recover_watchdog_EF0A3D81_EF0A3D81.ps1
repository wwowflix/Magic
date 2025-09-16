while ($true) {
    Write-Host "🔄 Running Auto-Recover Agent..."
    python "scripts\phase17\module_C\17C_auto_recover_agent_READY.py"
    Write-Host "✅ Cycle completed. Waiting 5 minutes..."
    Start-Sleep -Seconds 300   # Wait 5 minutes before next run
}
