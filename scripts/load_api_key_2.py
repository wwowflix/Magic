# -*- coding: utf-8 -*-
import json
import os

def load_api_key(key_name):
    vault_path = os.path.join(os.path.dirname(__file__), 'vault.json')
    with open(vault_path, 'r', encoding='utf-8-sig') as f:
        secrets = json.load(f)
    value = secrets.get(key_name)
    print(f'Loaded API key for {key_name}: {value}')
    return value



