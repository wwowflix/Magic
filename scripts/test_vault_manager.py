import os
import json
import pytest
import vault_manager

from vault_manager import VaultManager

def test_vault_save_and_load(tmp_path):
    # Patch VAULT_FILE in the vault_manager module
    vault_manager.VAULT_FILE = str(tmp_path / "vault.json")

    vm = VaultManager()
    vm.save_secret("TEST_KEY", "TEST_VALUE")
    result = vm.load_secret("TEST_KEY")

    assert result == "TEST_VALUE"

    with open(vault_manager.VAULT_FILE, "r") as f:
        data = json.load(f)
    assert data["TEST_KEY"] == "TEST_VALUE"



