import os
import re

def apply_remediation(script_path, error_message):
    if "FileNotFoundError" in error_message:
        match = re.search(r"No such file or directory: [\'\"]([^\'\"]+)[\'\"]", error_message)
        if match:
            missing_file = match.group(1)
            try:
                os.makedirs(os.path.dirname(missing_file), exist_ok=True)
                with open(missing_file, "w", encoding="utf-8") as f:
                    f.write("# Auto-created missing file\n")
                return True
            except Exception:
                return False
    elif "UnicodeDecodeError" in error_message:
        fallback_path = "outputs/fallback_input.txt"
        try:
            os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
            with open(fallback_path, "w", encoding="utf-8") as f:
                f.write("Fallback content")
            return True
        except Exception:
            return False
    return False
