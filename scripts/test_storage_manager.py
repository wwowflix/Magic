from storage_manager import StorageManager


def test_storage_manager(tmp_path):
    test_dir = tmp_path / "my_test_dir"
    sm = StorageManager()

    # Should create the folder
    sm.ensure_folder(str(test_dir))
    assert test_dir.exists()
    assert test_dir.is_dir()

    # Call again - should not error
    sm.ensure_folder(str(test_dir))
    assert test_dir.exists()
