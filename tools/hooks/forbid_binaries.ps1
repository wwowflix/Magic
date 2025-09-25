param()
$patterns = '\.(exe|msi|whl|zip|7z|iso|dll)$'
$changed  = git diff --cached --name-only
$hits     = $changed | Where-Object { $_ -match $patterns }
if ($hits) {
  Write-Host "Blocked binary file(s) from commit:" -ForegroundColor Red
  $hits | ForEach-Object { Write-Host " - $_" }
  Write-Host "Use Releases or Git LFS for binary artifacts." -ForegroundColor Yellow
  exit 1
}
exit 0