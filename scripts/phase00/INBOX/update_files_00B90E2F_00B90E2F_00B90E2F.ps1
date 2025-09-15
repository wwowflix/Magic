# Paths
$projectRoot = "D:\MAGIC"
$scriptsPath = Join-Path $projectRoot "scripts"
$readmePath = Join-Path $projectRoot "README.md"

# --- orchestrator.py content ---
$orchestratorCode = @"
import os
import json
import logging
from vault_manager import VaultManager
from storage_manager import StorageManager

logging.basicConfig(filename='logs/orchestrator.log', level=logging.INFO)

class OrchestratorLogger:
    def __init__(self, log_file='logs/orchestrator.log'):
        self.logger = logging.getLogger('orchestrator')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def info(self, message):
        self.logger.info(message)
        print(message)

    def error(self, message):
        self.logger.error(message)
        print(message)

def load_secrets():
    vault = VaultManager()
    api_key = vault.load_secret('OPENAI_API_KEY')
    if api_key:
        logging.info(f'🔐 Loaded OPENAI_API_KEY: {api_key}')
    else:
        logging.error('❌ OPENAI_API_KEY not found.')
        raise Exception("API key not found! Please save it in vault first.")
    return api_key

def check_storage():
    sm = StorageManager()
    folders_needed = ['inputs', 'outputs', 'logs', 'temp', 'scraped_data', 'ai_outputs']
    missing = sm.check_missing_folders(folders_needed)
    if missing:
        for f in missing:
            sm.ensure_folder(f)
    else:
        logging.info('✅ All folders exist.')

def track_budget(cost_this_run, budget_file='budget.json', max_budget=500):
    if os.path.exists(budget_file):
        with open(budget_file, 'r') as f:
            total_spent = json.load(f).get('spent', 0)
    else:
        total_spent = 0

    total_spent += cost_this_run

    with open(budget_file, 'w') as f:
        json.dump({'spent': total_spent}, f, indent=2)

    if total_spent > max_budget:
        logging.error(f'🚨 Budget exceeded! Spent: {total_spent}, Limit: {max_budget}')
        raise Exception(f'🚨 Budget exceeded! Spent: {total_spent}, Limit: {max_budget}')
    else:
        logging.info(f'✅ Budget OK. Spent: {total_spent} of {max_budget}')

if __name__ == '__main__':
    log = OrchestratorLogger()
    log.info('MAGIC Orchestrator started.')
    check_storage()
    api_key = load_secrets()
    track_budget(50)
    log.info('MAGIC orchestrator completed.')
"@

# --- vault_manager.py content ---
$vaultManagerCode = @"
import os
import json
import logging
from cryptography.fernet import Fernet

logging.basicConfig(filename='logs/vault_manager.log', level=logging.INFO)

class VaultManager:
    def __init__(self, key_path='.vault.key', vault_path='vault.json'):
        self.key_path = key_path
        self.vault_path = vault_path
        self.key = self.load_key()
        self.cipher = Fernet(self.key)

    def load_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, 'rb') as f:
                key = f.read()
            logging.info('Encryption key loaded.')
        else:
            key = Fernet.generate_key()
            with open(self.key_path, 'wb') as f:
                f.write(key)
            logging.info('Encryption key generated and saved.')
        return key

    def save_secret(self, name, secret):
        vault = {}
        if os.path.exists(self.vault_path):
            with open(self.vault_path, 'r') as f:
                try:
                    vault = json.load(f)
                except json.JSONDecodeError:
                    vault = {}
        encrypted = self.cipher.encrypt(secret.encode()).decode()
        vault[name] = encrypted
        with open(self.vault_path, 'w') as f:
            json.dump(vault, f, indent=2)
        logging.info(f'Secret saved for {name}')
        print(f'🔐 Secret saved for {name}')

    def load_secret(self, name):
        if not os.path.exists(self.vault_path):
            logging.error('Vault file does not exist.')
            return None
        with open(self.vault_path, 'r') as f:
            vault = json.load(f)
        encrypted = vault.get(name)
        if not encrypted:
            logging.error(f'Secret {name} not found.')
            return None
        decrypted = self.cipher.decrypt(encrypted.encode()).decode()
        logging.info(f'Secret loaded for {name}')
        return decrypted
"@

# --- storage_manager.py content ---
$storageManagerCode = @"
import os
import logging

logging.basicConfig(filename='logs/storage_manager.log', level=logging.INFO)

class StorageManager:
    def __init__(self, base_path='.'):
        self.base_path = base_path

    def check_missing_folders(self, folders):
        missing = []
        for folder in folders:
            path = os.path.join(self.base_path, folder)
            if not os.path.exists(path):
                missing.append(folder)
        return missing

    def ensure_folder(self, folder_name):
        path = os.path.join(self.base_path, folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info(f'Created folder: {path}')
            print(f'✅ Created folder: {path}')
        else:
            logging.info(f'Folder already exists: {path}')
"@

# --- README.md content ---
$readmeContent = @"
# MAGIC Project

## Vault Usage

Secrets such as API keys are stored securely using an encrypted vault system.

- The vault encryption uses the **Fernet** symmetric encryption from the `cryptography` Python package.
- A unique encryption key is saved locally in a file named `.vault.key`.
- Secrets are stored encrypted inside `vault.json`.

### How to Save a Secret

Use the `VaultManager` class in `vault_manager.py`:

```python
from vault_manager import VaultManager

vault = VaultManager()
vault.save_secret('OPENAI_API_KEY', 'sk-your-real-api-key')
