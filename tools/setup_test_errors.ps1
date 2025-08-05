# ============================
# Setup Test Error Scripts for Self-Healing Runner
# ============================

$testDir = "D:\MAGIC\scripts\test"
$manifestPath = "D:\MAGIC\phase_manifest.json"

# 1️⃣ Create folder if not exists
if (!(Test-Path $testDir)) {
    New-Item -ItemType Directory -Path $testDir | Out-Null
    Write-Host "📂 Created folder: $testDir"
}

# 2️⃣ Create test scripts

@"
try:
    with open("missing_input_file.txt", "r") as f:
        data = f.read()
    print("File content:", data)
except FileNotFoundError as e:
    print("❌ FileNotFoundError triggered:", e)
    raise
"@ | Out-File "$testDir\test_file_not_found.py" -Encoding UTF8

@"
text = "This will break: 😃 🚀 🌟"

try:
    with open("ascii_only.txt", "w", encoding="ascii") as f:
        f.write(text)
    print("Write success.")
except UnicodeEncodeError as e:
    print("❌ UnicodeEncodeError triggered:", e)
    raise
"@ | Out-File "$testDir\test_unicode_error.py" -Encoding UTF8

@"
try:
    import non_existent_package_123
    print("Module imported successfully.")
except ImportError as e:
    print("❌ ImportError triggered:", e)
    raise
"@ | Out-File "$testDir\test_import_error.py" -Encoding UTF8

Write-Host "✅ Test scripts created in $testDir"

# 3️⃣ Update manifest (add entries if not already present)

if (Test-Path $manifestPath) {
    $manifest = Get-Content
