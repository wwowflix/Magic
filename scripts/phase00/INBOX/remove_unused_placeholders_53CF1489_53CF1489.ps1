Get-ChildItem -Path "D:\MAGIC\scripts" -Recurse -Filter *_placeholder.py | ForEach-Object {
    if (-not (Select-String -Path $_.FullName -Pattern "# PROMOTED" -Quiet)) {
        Remove-Item $_.FullName -Force
        Write-Host "🗑️ Removed unused placeholder: $($_.FullName)"
    }
}
