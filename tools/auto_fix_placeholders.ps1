# tools\auto_fix_placeholders.ps1
$phasePath = "scripts\phase11"
$placeholderCode = @'
def main():
    pass

if __name__ == "__main__":
    main()
'@

Get-ChildItem -Path $phasePath -Recurse -Filter "*_READY.py" | ForEach-Object {
    $filePath = $_.FullName
    $content = Get-Content $filePath -Raw

    if ([string]::IsNullOrWhiteSpace($content) -or $content -notmatch "def\s+main") {
        Set-Content -Path $filePath -Value $placeholderCode -Encoding UTF8
        Write-Host "Fixed placeholder in:" $filePath
    }
    else {
        Write-Host "Skipped (already valid):" $filePath
    }
}
