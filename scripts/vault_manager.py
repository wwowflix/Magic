import os
import json
import logging

VAULT_FILE = r"vault.json"

class VaultManager:
    def __init__(self):
        if not os.path.exists(VAULT_FILE):
            with open(VAULT_FILE, "w") as f:
                json.dump({}, f)
            logging.info("Vault file created.")
        else:
            logging.info("Vault file already exists.")
        logging.info("VaultManager initialized.")

    def save_secret(self, key, value):
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)
        data[key] = value
        with open(VAULT_FILE, "w") as f:
            json.dump(data, f)
        logging.info(f"Secret saved for key: {key}")

    def load_secret(self, key):
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)
        value = data.get(key, None)
        if value:
            logging.info(f"Secret loaded for key: {key}")
        else:
            logging.warning(f"Secret for key {key} not found in vault.")
        return value

__all__ = ["VaultManager"]
