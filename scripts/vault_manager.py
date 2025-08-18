# vault_manager.py

from cryptography.fernet import Fernet
import os
import logging

logging.basicConfig(filename="orchestrator.log", level=logging.DEBUG)


class VaultManager:
    def __init__(self, key_file=".vault.key"):
        self.key_file = key_file
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            logging.info(f"Created new vault key: {self.key_file}")
        else:
            with open(self.key_file, "rb") as f:
                key = f.read()
            logging.info(f"Loaded existing vault key: {self.key_file}")
        self.fernet = Fernet(key)

    def encrypt(self, plaintext):
        token = self.fernet.encrypt(plaintext.encode())
        logging.info("Encrypted a value.")
        return token

    def decrypt(self, token):
        plaintext = self.fernet.decrypt(token).decode()
        logging.info("Decrypted a value.")
        return plaintext


if __name__ == "__main__":
    vault = VaultManager()
    secret = "my_api_key_123"
    encrypted = vault.encrypt(secret)
    print("Encrypted:", encrypted)
    decrypted = vault.decrypt(encrypted)
    print("Decrypted:", decrypted)
