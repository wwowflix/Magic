from vault_manager import VaultManager

vault = VaultManager()
api_key = vault.load_secret("OPENAI_API_KEY")
print("Loaded API key:", api_key)
