# MAGIC Project

## Overview

MAGIC is an orchestrator-based pipeline integrating:
- secure vault management
- folder storage management
- budget enforcement
- scraping modules
- AI content generation
- automated testing

## Setup

1. Create virtual environment:
    `powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    `

2. Install dependencies:
    `powershell
    pip install -r requirements.txt
    `

3. Run orchestrator:
    `powershell
    python .\scripts\orchestrator.py
    `

4. Run tests:
    `powershell
    pytest .\scripts
    `

## Logs

Logs are saved under:
D:\MAGIC\data\logs\

## Budget Tracking

- Max budget is configured in orchestrator.py.
- Budget usage tracked in budget.json.

## License

MIT License

[![Python application](https://github.com/Diksha090587/Magic/actions/workflows/python-app.yml/badge.svg)](https://github.com/Diksha090587/Magic/actions/workflows/python-app.yml)

---

## Logging Instructions

All core scripts (vault_manager.py, storage_manager.py, orchestrator.py) include logging to help debug and monitor processes.

- Logs are saved under:

    D:\MAGIC\data\logs\

- Main orchestrator logs:

    orchestrator.log

- Other test logs:

    vault_test.log
    storage_test.log

Check these logs to trace errors, see budget usage, and monitor successful operations.

---

## Folder Structure

The following folders are required for the pipeline:

    data/
      inputs/
      outputs/
      logs/
      temp/
      scraped_data/
      ai_outputs/

These folders are automatically created if missing when you run:

    python .\scripts\orchestrator.py

All inputs, outputs, logs, and temporary data are stored under data/ to keep the workspace organized.

---

## Running Tests

All test files are located under:

    D:\MAGIC\scripts\

### Run All Tests

To run all tests:

    pytest .\scripts

### Run a Specific Test

Example for vault tests:

    pytest .\scripts\test_vault_manager.py

### Test Files

| Test File | Purpose |
|-----------|---------|
| test_budget.py | Tests budget enforcement logic |
| test_vault_manager.py | Tests saving and loading secrets in the vault |
| test_storage_manager.py | Tests automatic folder creation |
| test_trends_scraper.py | Tests dummy scraper returns topic list |
| test_ai_content.py | Tests dummy AI content generation |

---

## Budget Tracking and Enforcement

MAGIC includes budget tracking to avoid exceeding API costs.

- The orchestrator tracks cumulative spend in a JSON file:

    budget.json

- You can configure your max budget in orchestrator.py:

    orch = Orchestrator(max_budget=500)

- If the total budget is exceeded, MAGIC raises an error and stops further operations.

To reset budget usage, delete or edit udget.json.

Run tests with:

    pytest .\scripts\test_budget.py
---

## Logging Instructions

All core scripts (vault_manager.py, storage_manager.py, orchestrator.py) include logging to help debug and monitor processes.

- Logs are saved under:

    D:\MAGIC\data\logs\

- Main orchestrator logs:

    orchestrator.log

- Other test logs:

    vault_test.log
    storage_test.log

Check these logs to trace errors, see budget usage, and monitor successful operations.
