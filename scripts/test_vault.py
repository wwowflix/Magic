import os
import logging
from vault_manager import VaultManager

log_path = r"D:\MAGIC\data\logs\vault_test.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

vault = VaultManager()
vault.save_secret("TEST_KEY", "TEST_VAL")
val = vault.load_secret("TEST_KEY")
print("Loaded:", val)
