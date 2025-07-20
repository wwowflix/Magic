# orchestrator.py

import logging
from vault_manager import VaultManager
from storage_manager import StorageManager

class OrchestratorLogger:
    def __init__(self, log_file='orchestrator.log'):
        self.logger = logging.getLogger('orchestrator')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

def load_api_key_from_vault():
    vault = VaultManager()
    # Example of encrypting a real key first time:
    # encrypted_key = vault.encrypt('YOUR_REAL_API_KEY')
    # Save encrypted_key securely for later use.
    
    # For now, we simulate decrypting:
    encrypted_key = vault.encrypt('super_secret_api_key')
    decrypted_key = vault.decrypt(encrypted_key)
    print('🔐 Decrypted API Key:', decrypted_key)
    return decrypted_key

def check_storage():
    sm = StorageManager()
    folders_needed = ['inputs', 'outputs', 'logs', 'temp']
    missing = sm.check_missing_folders(folders_needed)
    if missing:
        for f in missing:
            sm.ensure_folder(f)
    else:
        print('✅ All folders exist.')

def budget_check(current_cost, max_budget):
    if current_cost > max_budget:
        raise Exception(f'Budget exceeded! Cost: {current_cost}, Limit: {max_budget}')
    else:
        print('✅ Budget within limits.')

if __name__ == '__main__':
    log = OrchestratorLogger()
    log.info('MAGIC Orchestrator started.')
    check_storage()
    api_key = load_api_key_from_vault()
    log.info(f'API Key loaded: {api_key}')
    budget_check(50, 100)
