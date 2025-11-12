import json,sys,os
# Minimal health probe: ensure a few critical paths exist
OK = True
reasons = []
for p in ["scripts", "tools", "outputs", "requirements.lock.txt"]:
    if not os.path.exists(p):
        OK = False; reasons.append(f"missing:{p}")
result = {"healthy": OK, "reasons": reasons}
print(json.dumps(result))
sys.exit(0 if OK else 1)
