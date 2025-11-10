

image: magic-health:latest



command: python -m pytest -q tests/smoke -k "phase11 and \_ok"



result: ✅ 100% pass (with PYTEST\_DISABLE\_PLUGIN\_AUTOLOAD=1)
