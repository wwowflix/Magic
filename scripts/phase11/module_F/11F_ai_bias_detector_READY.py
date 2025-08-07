import os
import re

def detect_bias_in_line(line):
    flagged = []

    bias_terms = [
        ("man", "Consider gender-neutral terms like 'person'"),
        ("blacklist", "Use alternatives like 'blocklist'"),
        ("whitelist", "Use alternatives like 'allowlist'"),
        ("crazy", "Avoid insensitive mental health terminology"),
        ("normal people", "Avoid exclusionary phrasing"),
    ]

    for term, suggestion in bias_terms:
        if re.search(rf'\b{term}\b', line, re.IGNORECASE):
            flagged.append((term, suggestion))
    
    return flagged

def scan_output_file(file_path):
    issues = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            hits = detect_bias_in_line(line)
            for term, suggestion in hits:
                issues.append(f"Line {i}: '{term}' found – {suggestion}")
    return issues

def main():
    folder = "outputs"
    test_file = os.path.join(folder, "sample_output.txt")

    if not os.path.exists(test_file):
        print("⚠️ No sample output found to scan.")
        return

    issues = scan_output_file(test_file)
    if issues:
        print("⚠️ Bias issues detected:")
        for issue in issues:
            print("   " + issue)
    else:
        print("[PASS] No AI bias detected in sample output.")

if __name__ == "__main__":
    main()

