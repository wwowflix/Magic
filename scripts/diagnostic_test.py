import os
import json

vault_path = os.path.join(os.path.dirname(__file__), 'vault.json')

print(f'Checking if vault.json exists at: {vault_path}')
print('File exists:', os.path.exists(vault_path))

if os.path.exists(vault_path):
    with open(vault_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print('----- vault.json contents -----')
        print(content)
        print('----- end contents -----')
        secrets = json.loads(content)
        print('Loaded secrets:', secrets)
else:
    print('vault.json NOT FOUND!')



