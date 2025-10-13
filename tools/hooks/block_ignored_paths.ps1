param()
$staged = (git diff --cached --name-only -z) -split "`0" | ? { $_ }
$pattern = '(^|/)\.env($)|(^|/)\.coverage($)|(^|/)\.artifacts(/|$)'
$bad = $staged | ? { $_ -match $pattern }
if($bad){
  Write-Host "🚫 Refusing to commit ignored/secret artifacts:" -ForegroundColor Red
  $bad | % { Write-Host " - $_" -ForegroundColor Yellow }
  exit 1
}
exit 0
