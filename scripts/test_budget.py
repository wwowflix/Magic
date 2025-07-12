import pytest
import os
import json
from orchestrator import Orchestrator

def test_budget_blocking(tmp_path):
    budget_file = tmp_path / 'budget.json'
    budget_file.write_text('{"spent": 0}')
    orch = Orchestrator(max_budget=500)

    # Spend below budget should pass
    orch.track_budget(100, budget_file=str(budget_file))

    # Spending over budget should raise Exception
    with pytest.raises(Exception):
        orch.track_budget(500, budget_file=str(budget_file))
