# MAGIC Project Setup Script (Windows PowerShell)

Write-Host "Setting up virtual environment..."

# Create virtual environment
python -m venv venv

# Activate it
.\\venv\\Scripts\\Activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete. You're ready to go!"
