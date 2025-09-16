# Set base project path
$base = "D:\MAGIC"

# Create folder structure
$folders = @("scripts", "logs", "inputs", "outputs", "docs")
foreach ($f in $folders) {
    $full = Join-Path $base $f
    if (-Not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full | Out-Null
        Write-Host "📁 Created folder: $f"
    }
}

# Define files and content (PowerShell-safe)
$files = @(
    @{ Path = "scripts\setup_folders.py"; Content = "import os`nfolders = ['inputs', 'outputs', 'scripts', 'logs']`nfor folder in folders:`n    os.makedirs(folder, exist_ok=True)`nprint('✅ Folder structure created.')" },
    @{ Path = "scripts\env_loader.py"; Content = "from dotenv import load_dotenv`nimport os`nload_dotenv()`nprint('✅ Environment loaded from .env')" },
    @{ Path = "scripts\logger.py"; Content = "import logging`nimport os`nos.makedirs('logs', exist_ok=True)`nlogging.basicConfig(filename='logs/pipeline.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')" },
    @{ Path = "scripts\test_stub_trend.py"; Content = "print('✅ Stub for trend agent')" },
    @{ Path = "scripts\cost_guard.py"; Content = "MAX_DAILY_SPEND = 5.0`nprint(f'🔒 Daily API spend is capped at ${MAX_DAILY_SPEND}')" },
    @{ Path = "scripts\auth_test.py"; Content = "print('🔑 Testing API credentials... (OpenAI, ElevenLabs, etc.)')" },
    @{ Path = "scripts\config.py"; Content = "ROOT = 'D:/MAGIC'`nTIMEOUT = 30`nRETRIES = 3" },
    @{ Path = "docs\naming.md"; Content = "# 📄 Naming Conventions`n- Use `snake_case` filenames`n- Add timestamps: e.g., `trends_2025-07-18.csv`" },
    @{ Path = "README.md"; Content = "# 🧠 Magic – AI Automation System`nThis project automates trend discovery, content generation, publishing, and monetization." }
)

# Write files if missing
foreach ($file in $files) {
    $fullPath = Join-Path $base $file.Path
    if (-Not (Test-Path $fullPath)) {
        $folder = Split-Path $fullPath
        if (-Not (Test-Path $folder)) {
            New-Item -ItemType Directory -Path $folder | Out-Null
        }
        Set-Content -Path $fullPath -Value $file.Content
        Write-Host "📄 Created: $($file.Path)"
    } else {
        Write-Host "✅ Exists: $($file.Path)"
    }
}
