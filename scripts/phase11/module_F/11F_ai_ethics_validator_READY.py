# [PASS] Script: 11F_ai_ethics_validator_READY.py

import re
import os

ETHICS_FLAGS = {
    "discrimination": r"(if\s+user\.race|gender\s*==)",
    "manipulation": r"(dark_pattern|click_trap)",
    "transparency": r"(blackbox_model|hidden_logic)",
    "bias": r"(biased_data|training_bias)"
}

def scan_code(file_path):
    flagged_issues = []
    if not os.path.exists(file_path):
        return ["❌ File not found."]
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()
        for issue, pattern in ETHICS_FLAGS.items():
            if re.search(pattern, code, re.IGNORECASE):
                flagged_issues.append(f"⚠️ Potential {issue} detected.")
    return flagged_issues or ["[PASS] No ethical issues found."]

if __name__ == "__main__":
    test_file = "scripts/phase11/module_F/11F_example_test_case_READY.py"
    results = scan_code(test_file)
    for r in results:
        print(r)

