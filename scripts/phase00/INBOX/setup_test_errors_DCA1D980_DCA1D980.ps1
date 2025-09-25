# ============================================
# setup_test_errors.ps1
# Creates dummy scripts to simulate errors
# for Week 3 auto-remediation testing
# ============================================

$testDir = "D:\MAGIC\scripts\phase99\module_ZZ"
if (!(Test-Path $testDir)) {
    New-Item -ItemType Directory -Path $testDir -Force | Out-Null
}

# 1️⃣ FileNotFoundError simulation
@"
import sys
with open('non_existent_input.txt', 'r') as f:
    data = f.read()
print("This should fail because the file does not exist.")
"@ | Out-File "$testDir\99Z_file_not_found_test_READY.py" -Encoding UTF8

# 2️⃣ UnicodeEncodeError simulation
@"
data = 'Hello World – This contains a non-ASCII dash'
with open('outputs/test_unicode.log', 'w', encoding='ascii') as f:
    f.write(data)
"@ | Out-File "$testDir\99Z_unicode_error_test_READY.py" -Encoding UTF8

# 3️⃣ ImportError simulation
@"
import non_existent_module
print("This should fail because module does not exist.")
"@ | Out-File "$testDir\99Z_import_error_test_READY.py" -Encoding UTF8

Write-Host "✅ Test error scripts created in $testDir"
