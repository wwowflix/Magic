with open("outputs/logs/license_audit.log", "r", encoding="utf-8") as f:
    lines = f.readlines()
flagged = [l for l in lines if "EXPIRED" in l or "UNLICENSED" in l]
with open(
    "outputs/logs/11H_license_audit_log_scanner.log", "w", encoding="utf-8"
) as out:
    out.write("".join(flagged))
print(f"?? License audit completed: {len(flagged)} issues found.")
