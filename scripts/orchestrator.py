import os
import json
import logging
from vault_manager import VaultManager
from storage_manager import StorageManager

LOG_DIR = r"data\logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'orchestrator.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

class Orchestrator:
    REQUIRED_FOLDERS = [
        r"data\inputs",
        r"data\outputs",
        r"data\logs",
        r"data\temp",
        r"data\scraped_data",
        r"data\ai_outputs"
    ]

    def __init__(self, max_budget=500):
        self.vault = VaultManager()
        self.storage = StorageManager()
        self.ensure_folders()
        self.api_key = self.load_api_key()
        self.max_budget = max_budget

    def ensure_folders(self):
        for folder in self.REQUIRED_FOLDERS:
            self.storage.ensure_folder(folder)
        logging.info("All required folders ensured.")

    def load_api_key(self):
        api_key = self.vault.load_secret("OPENAI_API_KEY")
        if not api_key:
            logging.error("API key not found in vault.")
            raise Exception("API key not found in vault. Please save it first.")
        logging.info(f"API key loaded successfully. Starting with: {api_key[:8]}...")
        return api_key

    def track_budget(self, cost_this_run, budget_file=r"budget.json"):
        if not os.path.exists(budget_file):
            with open(budget_file, "w") as f:
                json.dump({"spent": 0}, f)
        with open(budget_file, "r") as f:
            data = f.read()
            if not data.strip():
                total_spent = 0
            else:
                total_spent = json.loads(data).get("spent", 0)
        total_spent += cost_this_run
        if total_spent > self.max_budget:
            logging.error(f"Budget exceeded! Spent: {total_spent}, Limit: {self.max_budget}")
            raise Exception(f"Budget exceeded! Spent: {total_spent}, Limit: {self.max_budget}")
        with open(budget_file, "w") as f:
            json.dump({"spent": total_spent}, f)
        logging.info(f"Budget OK. Spent: {total_spent} of {self.max_budget}")

if __name__ == "__main__":
    logging.info("MAGIC Orchestrator started.")
    orch = Orchestrator()
    try:
        orch.track_budget(10)
    except Exception as e:
        logging.error(str(e))
        print(str(e))
    logging.info("MAGIC Orchestrator completed.")
    print("Orchestrator ran successfully.")

# Expose Orchestrator for imports
__all__ = ["Orchestrator"]
