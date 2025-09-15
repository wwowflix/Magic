# deploy_to_github.ps1
# =====================
# This script automates:
# git add . → git commit → git push
# so your latest changes go live on GitHub.

Set-Location 'D:\MAGIC\scripts'
git add .
git commit -m 'Auto-deploy updates'
git push origin main
