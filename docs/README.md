# MAGIC 🚀

Welcome to **MAGIC** — **M**odular **A**I **G**eneration & **I**ntegration **C**onsole!

This is a Python project designed to help you:
- Safely manage your API keys and secrets
- Automatically create folders and organize your data
- Track how much you spend on APIs and stay within budget
- Scrape trending topics from the internet
- Generate AI-powered content
- Run tests to make sure your code works
- Keep everything version-controlled and backed up on GitHub

It’s like a control center for your AI projects!

---

## 🌟 How to Get Started

Follow these steps to set up MAGIC on your computer.

---

### 1. Install Python

First, install Python (if you don’t have it yet).

✅ Download Python here: https://www.python.org/downloads/

When installing:
- Check **Add Python to PATH**

---

### 2. Create a Virtual Environment

A virtual environment keeps your project’s packages separate from your main computer so you don’t mess up other Python projects.

Open **PowerShell** and run:

    cd D:\MAGIC
    python -m venv venv
    .\venv\Scripts\Activate.ps1

✅ Now your command line will show:

    (venv) PS D:\MAGIC>

---

### 3. Install Required Libraries

Install all Python packages you need:

    pip install -r requirements.txt

✅ This reads from a file called requirements.txt and installs all the packages your project needs.

---

### 4. Run the Orchestrator

Now run MAGIC’s main file:

    python .\scripts\orchestrator.py

✅ This script:
- Loads your API keys from a safe vault
- Makes sure all your folders exist
- Logs everything it does
- Checks your budget so you don’t spend too much money

---

## 🔑 How Secrets and Vaults Work

Some apps need secret info like API keys. Instead of putting them in your code, MAGIC saves them in a vault so no one else can see them.

### Save an API Key:

    from vault_manager import VaultManager
    vm = VaultManager()
    vm.save_secret("OPENAI_API_KEY", "sk-yourkeyhere")

### Load an API Key:

    from vault_manager import VaultManager
    vm = VaultManager()
    api_key = vm.load_secret("OPENAI_API_KEY")

✅ MAGIC uses a file:

    D:\MAGIC\vault.json

Don’t share this file publicly!

---

## 📂 Folder Organization

MAGIC automatically creates these folders:

    data/
        inputs/
        outputs/
        logs/
        temp/
        scraped_data/
        ai_outputs/

✅ These folders keep your project organized:
- **inputs/** → raw data you give the system
- **outputs/** → data MAGIC produces
- **logs/** → logs of everything MAGIC does
- **temp/** → temporary files
- **scraped_data/** → scraped trends or topics
- **ai_outputs/** → AI-generated text or media

---

## 📝 Logs – Where to Look if Things Break

MAGIC writes logs to help you debug issues.

Logs are saved here:

    D:\MAGIC\data\logs\

Important log files:
- orchestrator.log → logs from the main MAGIC script
- vault_test.log → logs from testing the vault
- storage_test.log → logs from testing storage features

✅ Always check these if MAGIC crashes or you see errors!

---

## 💰 Budget Tracking – Stay Under Your API Limit

Some APIs cost money. MAGIC helps make sure you don’t overspend.

It tracks your total spend in:

    budget.json

If your costs go over your budget, MAGIC stops running and logs an error.

### Set Your Budget Limit:

Change the value when you create the orchestrator:

    orch = Orchestrator(max_budget=500)

✅ If you want to start fresh, delete or edit budget.json.

---

## 🧪 Running Tests

MAGIC includes automated tests to check if things work correctly.

### Run All Tests

    pytest .\scripts

✅ This checks everything at once.

---

### Run a Specific Test

Example:

    pytest .\scripts\test_vault_manager.py

✅ Helpful if you only want to test one feature.

---

### What the Tests Do

| Test File                     | What It Tests                                    |
|-------------------------------|--------------------------------------------------|
| test_budget.py                | Checks that the budget limits work               |
| test_vault_manager.py         | Checks saving and loading secrets in the vault   |
| test_storage_manager.py       | Checks that folders are created if missing       |
| test_trends_scraper.py        | Tests a basic dummy scraper                      |
| test_ai_content.py            | Tests basic AI content generation                |

✅ Tests log everything to files for easier debugging.

---

## 🚫 Files You Should Ignore

Some files don’t belong in GitHub (like secrets or backups). That’s why we use a .gitignore file.

MAGIC ignores:

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

✅ This keeps your repo clean and safe.

---

## 🤖 Automatic Testing with GitHub Actions (CI/CD)

MAGIC uses **GitHub Actions** to run tests automatically every time you push changes to GitHub.

- Workflow file location:

      .github/workflows/python-app.yml

### Build Status Badge

If you see this badge in the README:

[![Python application](https://github.com/Diksha090587/Magic/actions/workflows/python-app.yml/badge.svg)](https://github.com/Diksha090587/Magic/actions/workflows/python-app.yml)

✅ It’s green → All tests passed.  
❌ It’s red → Something broke.

---

## 💡 What To Do Next

Congrats — you have MAGIC running!

Here’s how to make it even cooler:

✅ Build real scrapers:
- TikTok trending hashtags
- Reddit hot posts
- YouTube autocomplete topics

✅ Connect MAGIC to:
- Affiliate marketing (to earn money from your content!)
- AI video creation tools (text-to-video)

✅ Set up automatic deployment in the cloud

MAGIC is your blank canvas for any AI project!

---

## 📄 License

MIT License
