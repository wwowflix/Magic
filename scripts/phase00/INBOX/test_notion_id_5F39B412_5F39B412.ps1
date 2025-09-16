Write-Host "Testing Notion API connection..." -ForegroundColor Cyan

# Load .env variables
$envFile = ".\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^(?<key>[^#=]+)=(?<value>.*)$") {
            Set-Item -Path "Env:\$($matches['key'])" -Value $matches['value']
        }
    }
} else {
    Write-Host ".env file not found." -ForegroundColor Red
    exit 1
}

# Get values
$NOTION_TOKEN = $Env:NOTION_TOKEN
$DATABASE_ID = $Env:NOTION_DATABASE_ID

if (-not $NOTION_TOKEN -or -not $DATABASE_ID) {
    Write-Host "Missing NOTION_TOKEN or NOTION_DATABASE_ID." -ForegroundColor Red
    exit 1
}

# Send request
try {
    $response = Invoke-RestMethod `
        -Uri "https://api.notion.com/v1/databases/$DATABASE_ID" `
        -Headers @{
            "Authorization" = "Bearer $NOTION_TOKEN"
            "Notion-Version" = "2022-06-28"
        } `
        -Method GET

    if ($response.object -eq "database") {
        Write-Host "`nConnected to Notion database successfully!" -ForegroundColor Green
        Write-Host "Database Name: $($response.title[0].plain_text)"
        Write-Host "Database ID: $DATABASE_ID`n"
    } else {
        Write-Host "`nReceived response, but not a valid database object." -ForegroundColor Yellow
        $response | ConvertTo-Json -Depth 4
    }
}
catch {
    Write-Host "`nFailed to connect to Notion API." -ForegroundColor Red
    Write-Host "Please check:"
    Write-Host "1. That the Database ID is correct (32 characters from the URL)"
    Write-Host "2. That the Integration is shared with the database"
    Write-Host "3. That the NOTION_TOKEN is valid"
    Write-Host "`nRaw error message:"
    Write-Host $_.Exception.Message -ForegroundColor DarkYellow
}
