function Open-PR {
  param(
    [string]$Base = 'main',
    [string]$Title = $(git log -1 --pretty=%s),
    [string]$Body  = "Automated PR: $((git log -1 --pretty=%B).Trim())"
  )
  $branch = git rev-parse --abbrev-ref HEAD
  if ($branch -eq 'main') {
    Write-Host "You're on main; switch to a feature branch first." -ForegroundColor Yellow
    return
  }
  gh pr create --base $Base --head $branch --title $Title --body $Body
}

function Merge-PR {
  param(
    [int]$Number,
    [switch]$NoWatch
  )
  if ($Number) {
    $pr = $Number
  } else {
    $branch = git rev-parse --abbrev-ref HEAD
    if (-not $branch) { Write-Host "Cannot determine current branch." -ForegroundColor Yellow; return }
    if ($branch -eq 'main' -or $branch -eq 'origin/main') {
      Write-Host "You are on 'main'. Pass -Number <PR#> or switch to a feature branch." -ForegroundColor Yellow
      return
    }
    $pr = gh pr list -H $branch --json number --jq '.[0].number' 2>$null
  }
  if (-not $pr) {
    Write-Host "No PR found for this branch. Create one via: gh pr create -B main -H <branch>" -ForegroundColor Yellow
    return
  }
  Write-Host "Using PR #$pr" -ForegroundColor Cyan
  if ($NoWatch) { gh pr checks $pr } else { gh pr checks $pr --watch }
  gh pr merge $pr --squash --auto
}
