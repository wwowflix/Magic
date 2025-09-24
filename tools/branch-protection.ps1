function Get-BranchProtection {
  param([string]$Owner,[string]$Repo,[string]$Branch='main')
  gh api -H "Accept: application/vnd.github+json" "repos/$Owner/$Repo/branches/$Branch/protection" |
    ConvertFrom-Json
}

function Show-RequiredChecks {
  param([string]$Owner,[string]$Repo,[string]$Branch='main')
  $bp = Get-BranchProtection -Owner $Owner -Repo $Repo -Branch $Branch

  Write-Host ("`nRequired checks on {0}/{1}:{2}:" -f $Owner,$Repo,$Branch) -ForegroundColor Cyan
  $contexts = @()
  if ($bp.required_status_checks -and $bp.required_status_checks.contexts) {
    $contexts = @($bp.required_status_checks.contexts)
  }
  if ($contexts.Count) { $contexts | Sort-Object | ForEach-Object { Write-Host "  - $_" } }
  else { Write-Host "  (none)" }

  $strict = $false
  if ($bp.required_status_checks -and $bp.required_status_checks.strict -ne $null) {
    $strict = [bool]$bp.required_status_checks.strict
  }
  Write-Host ("  (strict: {0})" -f $strict)
}

function Set-Strict {
  param([string]$Owner,[string]$Repo,[string]$Branch='main',[bool]$Strict=$true)
  @{ required_status_checks = @{ strict = $Strict } } |
    ConvertTo-Json -Depth 5 |
    gh api -X PATCH -H "Accept: application/vnd.github+json" `
      "repos/$Owner/$Repo/branches/$Branch/protection/required_status_checks" --input -
}

function Set-RequiredChecks {
  param([string]$Owner,[string]$Repo,[string]$Branch='main',[string[]]$Contexts)
  $args = @(); foreach ($c in $Contexts) { $args += @('-f',"contexts[]=$c") }
  gh api -X PUT -H "Accept: application/vnd.github+json" `
    "repos/$Owner/$Repo/branches/$Branch/protection/required_status_checks/contexts" @args
}

function Add-RequiredChecks {
  param([string]$Owner,[string]$Repo,[string]$Branch='main',[string[]]$ContextsToAdd)
  $bp   = Get-BranchProtection -Owner $Owner -Repo $Repo -Branch $Branch
  $new  = @($bp.required_status_checks.contexts + $ContextsToAdd | Where-Object { $_ } | Select-Object -Unique)
  Set-RequiredChecks -Owner $Owner -Repo $Repo -Branch $Branch -Contexts $new
}

function Remove-RequiredChecks {
  param([string]$Owner,[string]$Repo,[string]$Branch='main',[string[]]$ContextsToRemove)
  $bp   = Get-BranchProtection -Owner $Owner -Repo $Repo -Branch $Branch
  $new  = @($bp.required_status_checks.contexts | Where-Object { $_ -and ($_ -notin $ContextsToRemove) })
  Set-RequiredChecks -Owner $Owner -Repo $Repo -Branch $Branch -Contexts $new
}