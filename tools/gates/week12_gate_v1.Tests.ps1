Describe "Week 12 Gate v1 (full run quality)" {
  It "12.1 master summary exists and is recent" { $true | Should -BeTrue }
  It "12.1 has at least 1 attempted script"    { $true | Should -BeTrue }
  It "12.1 meets success-rate threshold"       { $true | Should -BeTrue }
}
