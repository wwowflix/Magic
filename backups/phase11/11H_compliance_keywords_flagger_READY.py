import os, re
KEYWORDS = ['GDPR', 'HIPAA', 'PCI', 'confidential', 'classified']
matches = []
for root, _, files in os.walk('scripts'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    for kw in KEYWORDS:
                        if kw in line:
                            matches.append(f"{path} ? Line {i}: {kw}")
log = "outputs/logs/11H_compliance_keywords_flagger.log"
os.makedirs(os.path.dirname(log), exist_ok=True)
with open(log, 'w', encoding='utf-8') as f: f.write('\n'.join(matches))
print(f"? Compliance flagging done. {len(matches)} hits. See log.")
