import importlib
import types


def test_import_scripts_phase11_module_A_11A_anomaly_log_writer_READY():
    mod = importlib.import_module(
        "scripts.phase11.module_a.11A_anomaly_log_writer_READY"
    )
    assert isinstance(mod, types.ModuleType)
