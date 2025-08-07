param(
  [string]$DatabaseId = $Env:NOTION_DATABASE_ID,
  [string]$Token      = $Env:NOTION_TOKEN
)

# build headers
$headers = @{
  "Authorization"  = "Bearer $Token"
  "Notion-Version" = "2022-06-28"
  "Content-Type"   = "application/json"
}

# paginate through the database
$allPages   = @()
$startCursor = $null
do {
  $body = @{ page_size = 100 }
  if ($startCursor) { $body.start_cursor = $startCursor }
  $resp = Invoke-RestMethod `
    -Uri "https://api.notion.com/v1/databases/$DatabaseId/query" `
    -Method POST -Headers $headers `
    -Body ( $body | ConvertTo-Json )
  $allPages   += $resp.results
  $startCursor = $resp.next_cursor
} while ($resp.has_more)

# write out to a file
$allPages | ConvertTo-Json -Depth 10 | Out-File notion_export.json -Encoding utf8

Write-Host "✅ Exported" $allPages.Count "pages to D:\MAGIC\notion_export.json"
