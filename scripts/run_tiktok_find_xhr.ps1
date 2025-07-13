cd D:\MAGIC\scripts
python .\tiktok_find_xhr.py | Tee-Object -FilePath D:\MAGIC\data\xhr_log.txt
Write-Host "✅ TikTok XHR scan complete!"
Write-Host "Check your file:"
Write-Host "D:\MAGIC\data\xhr_log.txt"
