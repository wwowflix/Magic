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

