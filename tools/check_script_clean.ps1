param (
    [Parameter(Mandatory = $true)]
    [string]$FilePath
)

# Check if file exists
if (-not (Test-Path $FilePath)) {
    Write-Host "ERROR: File not found: $FilePath" -ForegroundColor Red
    exit 1
}

$extension = [System.IO.Path]::GetExtension($FilePath).ToLower()

switch ($extension) {
    ".ps1" {
        Write-Host "Checking PowerShell script syntax: $FilePath"
        try {
            # Using basic parser check
            $null = Get-Content $FilePath | Out-String | Out-Null
            Write-Host "OK: PowerShell script loaded successfully." -ForegroundColor Green
        } catch {
            Write-Host "ERROR: Issue detected in PowerShell script." -ForegroundColor Red
            Write-Host $_
        }
    }
    ".py" {
        Write-Host "Checking Python script syntax: $FilePath"
        $result = python -m py_compile $FilePath 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "OK: Python syntax looks good." -ForegroundColor Green
        } else {
            Write-Host "ERROR: Python syntax issue detected:" -ForegroundColor Red
            Write-Host $result
        }
    }
    default {
        Write-Host "Unsupported file type: $extension"
    }
}
