\D:\MAGIC = 'D:\MAGIC'
\D:\MAGIC\scripts = Join-Path \D:\MAGIC 'scripts'
\D:\MAGIC\scripts\orchestrator.py = Join-Path \D:\MAGIC\scripts 'orchestrator.py'

\import logging
import os
import json
from vault_manager import VaultManager
from storage_manager import StorageManager

logging.basicConfig(filename='logs/orchestrator.log', level=logging.INFO)

class Orchestrator:
    REQUIRED_FOLDERS = [
        'data/inputs',
        'data/outputs',
        'data/logs',
        'data/temp',
        'data/scraped_data',
        'data/ai_outputs'
    ]

    def __init__(self):
        self.logger = logging.getLogger('orchestrator')
        self.vault = VaultManager()
        self.storage_manager = StorageManager(base_path='data')

    def check_folders(self):
        missing = []
        for folder in self.REQUIRED_FOLDERS:
            if not os.path.exists(folder):
                missing.append(folder)
                self.storage_manager.ensure_folder(folder)
                self.logger.info(f"✅ Created folder: {folder}")
        if not missing:
            self.logger.info("✅ All required folders exist.")

    def load_secrets(self):
        api_key = self.vault.load_secret('OPENAI_API_KEY')
        if not api_key:
            self.logger.error("❌ API key not found in vault. Please save it first.")
            raise Exception("API key not found! Please save it in the vault first.")
        self.logger.info(f"Using API key starting with: {api_key[:10]}...")
        return api_key

if __name__ == '__main__':
    orch = Orchestrator()
    orch.logger.info("MAGIC Orchestrator started.")
    orch.check_folders()
    api_key = orch.load_secrets()
    orch.logger.info("MAGIC orchestrator completed.") = @'
import logging
import os
import json
from vault_manager import VaultManager
from storage_manager import StorageManager

logging.basicConfig(filename='logs/orchestrator.log', level=logging.INFO)

class Orchestrator:
    REQUIRED_FOLDERS = [
        'data/inputs',
        'data/outputs',
        'data/logs',
        'data/temp',
        'data/scraped_data',
        'data/ai_outputs'
    ]

    def __init__(self):
        self.logger = logging.getLogger("orchestrator")
        self.vault = VaultManager()
        self.storage_manager = StorageManager(base_path="data")

    def check_folders(self):
        missing = []
        for folder in self.REQUIRED_FOLDERS:
            if not os.path.exists(folder):
                missing.append(folder)
                self.storage_manager.ensure_folder(folder)
                self.logger.info(f"✅ Created folder: {folder}")
        if not missing:
            self.logger.info("✅ All required folders exist.")

    def load_secrets(self):
        api_key = self.vault.load_secret("OPENAI_API_KEY")
        if not api_key:
            self.logger.error("❌ API key not found in vault. Please save it first.")
            raise Exception("API key not found! Please save it in the vault first.")
        self.logger.info(f"Using API key starting with: {api_key[:10]}...")
        return api_key

if __name__ == "__main__":
    orch = Orchestrator()
    orch.logger.info("MAGIC Orchestrator started.")
    orch.check_folders()
    api_key = orch.load_secrets()
    orch.logger.info("MAGIC orchestrator completed.")
'@

Set-Content -Path \D:\MAGIC\scripts\orchestrator.py -Value \import logging
import os
import json
from vault_manager import VaultManager
from storage_manager import StorageManager

logging.basicConfig(filename='logs/orchestrator.log', level=logging.INFO)

class Orchestrator:
    REQUIRED_FOLDERS = [
        'data/inputs',
        'data/outputs',
        'data/logs',
        'data/temp',
        'data/scraped_data',
        'data/ai_outputs'
    ]

    def __init__(self):
        self.logger = logging.getLogger('orchestrator')
        self.vault = VaultManager()
        self.storage_manager = StorageManager(base_path='data')

    def check_folders(self):
        missing = []
        for folder in self.REQUIRED_FOLDERS:
            if not os.path.exists(folder):
                missing.append(folder)
                self.storage_manager.ensure_folder(folder)
                self.logger.info(f"✅ Created folder: {folder}")
        if not missing:
            self.logger.info("✅ All required folders exist.")

    def load_secrets(self):
        api_key = self.vault.load_secret('OPENAI_API_KEY')
        if not api_key:
            self.logger.error("❌ API key not found in vault. Please save it first.")
            raise Exception("API key not found! Please save it in the vault first.")
        self.logger.info(f"Using API key starting with: {api_key[:10]}...")
        return api_key

if __name__ == '__main__':
    orch = Orchestrator()
    orch.logger.info("MAGIC Orchestrator started.")
    orch.check_folders()
    api_key = orch.load_secrets()
    orch.logger.info("MAGIC orchestrator completed.") -Encoding UTF8
Write-Host "✅ orchestrator.py updated with vault integration and folder checks."
