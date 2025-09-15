from vault_manager import VaultManager


def main():
    vault = VaultManager()
    api_key = vault.load_secret("OPENAI_API_KEY")
    if api_key:
        print("[OK] Loaded API key successfully:")
        print(api_key)
    else:
        print("? API key not found. Please save it first.")


if __name__ == "__main__":
    main()
