import json, sys, os
OK = True
reasons = []
for p in ["scripts", "tools", "outputs", "requirements.lock.txt"]:
    if not os.path.exists(p):
        OK = False; reasons.append(f"missing:{p}")
print(json.dumps({"healthy": OK, "reasons": reasons}))
sys.exit(0 if OK else 1)
