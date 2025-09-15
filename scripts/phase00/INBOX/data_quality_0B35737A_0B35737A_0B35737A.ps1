# data_quality.ps1 — clean & reload your CSVs with quality checks (skips empty files)

Set-Location "D:\MAGIC\scripts"

# Mapping of filename → folder
$files = @{
  "google_trends_output.csv" = "."
  "reddit_scrape.csv"        = ".\outputs"
  "youtube_scrape.csv"       = ".\outputs"
  "tiktok_scrape.csv"        = ".\outputs"
}

# Standard column names
$standardNames = @{
  "Date"     = "date"
  "Keyword"  = "keyword"
  "Platform" = "platform"
  "Metric"   = "metric"
  "Author"   = "author"
  "Title"    = "title"
  "URL"      = "url"
}

foreach ($file in $files.Keys) {
  $folder = $files[$file]
  $path   = Join-Path $folder $file

  if (-not (Test-Path $path)) {
    Write-Host "Skipping $file (not found in $folder)."
    continue
  }

  # Quick check: skip if file has only header or is empty
  $raw = Get-Content $path -ErrorAction SilentlyContinue
  if (!$raw -or $raw.Count -le 1) {
    Write-Host "Skipping $file (no data rows)."
    continue
  }

  Write-Host "Processing $file..."
  $data = Import-Csv $path

  # a) Rename columns
  $mapping = @{}
  foreach ($col in $data[0].PSObject.Properties.Name) {
    $mapping[$col] = if ($standardNames.ContainsKey($col)) { $standardNames[$col] } else { $col.ToLower() }
  }
  $data = $data | Select-Object (
    $mapping.GetEnumerator() | ForEach-Object {
      @{ Name = $_.Value; Expression = { $_.PSObject.Properties[$_.Key].Value } }
    }
  )

  # b) Remove duplicates
  $data = $data | Sort-Object date,platform,title -Unique

  # c) Drop blank titles
  $data = $data | Where-Object { $_.title -and $_.title.Trim() -ne "" }

  # d) Keep only valid dates YYYY-MM-DD
  $data = $data | Where-Object { $_.date -match '^\d{4}-\d{2}-\d{2}$' }

  # e) Save back
  $data | Export-Csv $path -NoTypeInformation
  Write-Host "Cleaned $file — $($data.Count) rows remain.`n"
}

# Reload into SQLite
Write-Host "Reloading into SQLite..."
python .\ingest_csvs_to_db.py

Write-Host "✅ Data quality checks done and DB refreshed."
