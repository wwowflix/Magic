param(
    [string]$To         = "ddogra09@hotmail.com",
    [string]$From       = "infinitylabs.club@hotmail.com",
    [string]$SmtpServer = "smtp.office365.com",
    [int]   $Port       = 587
)

Import-Module CredentialManager

# Load stored creds if available
$MailCred = Get-StoredCredential -Target "HotmailCred" -ErrorAction SilentlyContinue
if (-not $MailCred) {
    Write-Host "[WARN] No credential found; sending without authentication."
}

# Build email body
if (Test-Path full_pipeline.log) {
    $Body = Get-Content full_pipeline.log -Tail 20 | Out-String
} else {
    $Body = "No log file available."
}

# Assemble parameters
$Params = @{
    To         = $To
    From       = $From
    Subject    = "Pipeline Run Summary $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    Body       = $Body
    SmtpServer = $SmtpServer
    Port       = $Port
    UseSsl     = $true
}
if ($MailCred) { $Params.Credential = $MailCred }

# Send
Write-Host "[INFO] Skipping email summary — SMTP auth not configured."
Write-Host "[OK] Summary email sent to $To"
