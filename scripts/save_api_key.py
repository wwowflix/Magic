from vault_manager import VaultManager

vault = VaultManager()
vault.save_secret('OPENAI_API_KEY', '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')

secret = vault.load_secret('OPENAI_API_KEY')
print('✅ API key saved and loaded successfully:', secret[:10] + '...')
