# MAGIC 🚀

**MAGIC** (Modular AI Generation & Integration Console) is a modular Python framework for orchestrating AI-driven workflows.  

It combines:

✅ Secure API key management  
✅ Automated folder & storage handling  
✅ Budget tracking and enforcement  
✅ Data scraping  
✅ AI content generation  
✅ Automated testing  
✅ GitHub integration with CI/CD

Your one-stop system for building scalable, monetized AI pipelines.

---

## 🚀 Quick Start

### 1. Create Virtual Environment

\\\powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
\\\

---

### 2. Run the Orchestrator

\\\powershell
python .\scripts\orchestrator.py
\\\

✅ This:
- Loads API keys securely
- Ensures all folders exist
- Initializes logs
- Tracks budget

---

## 🔒 Vault Management

All secrets (like API keys) are stored securely in a local vault file:

\\\
D:\MAGIC\vault.json
\\\

- Save secrets:
\\\python
from vault_manager import VaultManager
vm = VaultManager()
vm.save_secret("OPENAI_API_KEY", "sk-...")
\\\

- Load secrets:
\\\python
api_key = vm.load_secret("OPENAI_API_KEY")
\\\

Logs will confirm vault operations.

---

## 📂 Folder Structure

MAGIC organizes files under:

\\\
data/
  inputs/
  outputs/
  logs/
  temp/
  scraped_data/
  ai_outputs/
\\\

✅ Created automatically by \orchestrator.py\.  
✅ Keeps workspace neat and organized.

---

## 📝 Logging

MAGIC logs all operations for easy debugging:

\\\
D:\MAGIC\data\logs\
\\\

- Main orchestrator logs:
  \\\
  orchestrator.log
  \\\

- Test-specific logs:
  \\\
  vault_test.log
  storage_test.log
  \\\

Check logs for:
- Errors
- Budget usage
- Process flow

---

## 💰 Budget Tracking & Enforcement

MAGIC prevents accidental overspending on API calls.

- Tracks cumulative costs in:
\\\
budget.json
\\\

- Configure your budget:

\\\python
orch = Orchestrator(max_budget=500)
\\\

✅ Exceeds budget → raises an error and halts operations.  

Reset budget by deleting or editing \udget.json\.

---

## 🧪 Running Tests

MAGIC uses **pytest** for automated testing.

### Run All Tests:

\\\powershell
pytest .\scripts
\\\

### Run One Test:

\\\powershell
pytest .\scripts\test_vault_manager.py
\\\

### Test Files

| Test File                      | Purpose                                       |
|--------------------------------|-----------------------------------------------|
| test_budget.py                 | Tests budget enforcement logic                |
| test_vault_manager.py          | Tests saving/loading secrets in the vault     |
| test_storage_manager.py        | Tests automatic folder creation               |
| test_trends_scraper.py         | Tests dummy scraper returns topics            |
| test_ai_content.py             | Tests dummy AI content generation             |

✅ All tests log results for debugging.

---

## ✅ .gitignore

To keep your repo clean, these files/folders are ignored:

\\\
scripts/orchestrator_backup.py
__pycache__/
*.pyc
*.pyo
venv/
.VENV/
.env/
*.log
.DS_Store
Thumbs.db
\\\

---

## 🤖 GitHub Actions (CI/CD)

MAGIC runs all tests automatically on every push to GitHub.

- Workflow config:
  \\\
  .github/workflows/python-app.yml
  \\\

- Build badge:

  [![Python application](https://github.com/Diksha090587/Magic/actions/workflows/python-app.yml/badge.svg)](https://github.com/Diksha090587/Magic/actions/workflows/python-app.yml)

✅ Ensures your code is always stable and production-ready.

---

## 💡 Next Steps

MAGIC is fully scaffolded. Time to expand!

✅ Add real scrapers:
- TikTok trending hashtags
- Reddit hot posts
- YouTube autocomplete

✅ Integrate affiliate marketing:
- Monetize AI-generated videos
- Insert affiliate links into content

✅ Automate video generation:
- Combine AI text, voice, and visuals

Let’s make MAGIC your ultimate AI monetization engine. 🚀

---

## 📄 License

[MIT License](LICENSE)
