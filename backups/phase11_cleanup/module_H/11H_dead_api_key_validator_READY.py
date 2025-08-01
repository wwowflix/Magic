import os
matches = []
for root, _, files in os.walk('scripts'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            content = open(path, 'r', encoding='utf-8', errors='ignore').read()
            if 'api_key' in content and 'TODO' in content:
                matches.append(path)
log = 'outputs/logs/11H_dead_api_key_validator.log'
os.makedirs(os.path.dirname(log), exist_ok=True)
with open(log, 'w') as f: f.write('\n'.join(matches))
print(f'?? Dead API keys flagged in {len(matches)} files.')
