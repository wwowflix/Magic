[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)] [string]$Tag,
  [string]$Title = "$Tag – Phase 11 wrap-up",
  [string]$NotesPath = "docs\RELEASE_NOTES.md",
  [string[]]$Assets = @()
)

$ErrorActionPreference = "Stop"

function Get-AuthHeaders {
  if (-not $env:GITHUB_TOKEN -or [string]::IsNullOrWhiteSpace($env:GITHUB_TOKEN)) {
    throw "Set a GitHub token first (fine-grained or classic) in `$env:GITHUB_TOKEN`."
  }
  return @{
    Authorization = "token $($env:GITHUB_TOKEN.Trim())"
    Accept        = "application/vnd.github+json"
    'User-Agent'  = 'ps-release-script'
  }
}

function Upload-ReleaseAsset {
  param(
    [Parameter(Mandatory=$true)] $Rel,
    [Parameter(Mandatory=$true)] [string] $Path,
    [Parameter(Mandatory=$true)] $Headers,
    [Parameter(Mandatory=$true)] [string] $Org,
    [Parameter(Mandatory=$true)] [string] $Repo
  )
  if (-not (Test-Path -LiteralPath $Path)) { Write-Warning "Asset not found: $Path"; return }
  $name = Split-Path -Leaf $Path

  # delete same-named asset to avoid duplicates
  $assets = Invoke-RestMethod -Headers $Headers -Uri ("{0}?per_page=100" -f $Rel.assets_url)
  $existing = $assets | Where-Object { $_.name -eq $name }
  if ($existing) {
    Invoke-RestMethod -Headers $Headers -Method Delete -Uri "https://api.github.com/repos/$Org/$Repo/releases/assets/$($existing.id)" | Out-Null
  }

  $ext = [IO.Path]::GetExtension($name); if ($null -eq $ext) { $ext = '' }
  $ext = $ext.ToLowerInvariant()
  switch ($ext) {
    '.zip'  { $ctype = 'application/zip' }
    '.mp4'  { $ctype = 'video/mp4' }
    '.png'  { $ctype = 'image/png' }
    '.json' { $ctype = 'application/json' }
    '.html' { $ctype = 'text/html' }
    default { $ctype = 'application/octet-stream' }
  }

  $uploadBase = $Rel.upload_url -replace '\{.*$',''
  $uploadUri  = ('{0}?name={1}' -f $uploadBase, [uri]::EscapeDataString($name))

  Invoke-WebRequest -Headers $Headers -Method Post -Uri $uploadUri -InFile $Path -ContentType $ctype | Out-Null
  Write-Host "✔ Uploaded: $name"
}

# detect org/repo from git remote
$remote = git remote get-url origin
if ($remote -notmatch 'github\.com[:/](?<Org>[^/]+)/(?<Repo>[^/.]+)') {
  throw "Could not parse GitHub remote: $remote"
}
$Org  = $Matches.Org
$Repo = $Matches.Repo

$H = Get-AuthHeaders

# confirm auth works
$me = Invoke-RestMethod https://api.github.com/user -Headers $H
Write-Host "Authenticated as $($me.login)"

# body
if (Test-Path -LiteralPath $NotesPath) {
  $Body = Get-Content $NotesPath -Raw
} else {
  $Body = ""
}

# get or create the release
try {
  $Rel = Invoke-RestMethod -Headers $H -Uri "https://api.github.com/repos/$Org/$Repo/releases/tags/$Tag"
  $payload = @{ name = $Title; body = $Body } | ConvertTo-Json -Compress
  $null = Invoke-RestMethod -Headers $H -Method Patch -Uri "https://api.github.com/repos/$Org/$Repo/releases/$($Rel.id)" -Body $payload
} catch {
  if ($_.Exception.Response.StatusCode.Value__ -eq 404) {
    $payload = @{ tag_name = $Tag; name = $Title; body = $Body; draft = $false; prerelease = $false } | ConvertTo-Json -Compress
    $Rel = Invoke-RestMethod -Headers $H -Method Post -Uri "https://api.github.com/repos/$Org/$Repo/releases" -Body $payload
  } else { throw }
}

# upload any assets provided
foreach ($p in $Assets) { Upload-ReleaseAsset -Rel $Rel -Path $p -Headers $H -Org $Org -Repo $Repo }

Write-Host "Release page: $($Rel.html_url)"

