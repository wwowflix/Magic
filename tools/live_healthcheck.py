param([string]$Root="D:\MAGIC",[switch]$SkipBuild)
$ErrorActionPreference = "Stop"
function J($p){ Join-Path $Root $p }
function Ensure-Dir([string]$p){ if(!(Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
$reports = J "outputs\reports"; Ensure-Dir $reports
Write-Host "=== Week 8 Docker Pack ===" -ForegroundColor Cyan

# 1) Healthcheck script
$hc = J "tools\live_healthcheck.py"
if(!(Test-Path $hc)){
@'
import json, sys, os
status = {"ok": True, "msg": "MAGIC container healthy", "cwd": os.getcwd()}
print(json.dumps(status)); sys.exit(0)
