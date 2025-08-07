import os
import re

def scan_for_guardrail_violations(file_path):
    issues = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

        # Check for unsafe prompt keywords
        risky_keywords = ["ignore previous", "jailbreak", "bypass filter", "simulate being"]
        for word in risky_keywords:
            if word in content.lower():
                issues.append(f"⚠️ Prompt injection risk keyword found: '{word}'")

        # Check for use of OpenAI key in plain text
        if "sk-" in content:
            issues.append("⚠️ Possible hardcoded OpenAI API key found.")

        # Check for insecure eval/exec usage
        if "eval(" in content or "exec(" in content:
            issues.append("⚠️ Use of 'eval' or 'exec' detected.")

    return issues

def main():
    folder = "scripts/phase11/module_F"
    flagged = False

    for filename in os.listdir(folder):
        if filename.endswith("_READY.py") and filename != os.path.basename(__file__):
            path = os.path.join(folder, filename)
            print(f"🔍 Scanning: {filename}")
            issues = scan_for_guardrail_violations(path)
            if issues:
                flagged = True
                for issue in issues:
                    print(f"   {issue}")

    if not flagged:
        print("[PASS] All scripts passed OpenAI guardrail checks.")

if __name__ == "__main__":
    main()

