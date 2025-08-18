import re
from pathlib import Path


def fix_reddit_script(script_path):
    try:
        # Read with explicit UTF-8 encoding
        content = Path(script_path).read_text(encoding="utf-8")

        # Fix common issues
        fixed = re.sub(r"(if subreddit_list is None:\s*)(subreddits =)", r"\1    \2", content)
        fixed = re.sub(r"[^\x00-\x7F]+", "", fixed)  # Remove non-ASCII

        # Save with BOM to ensure Windows compatibility
        output_path = script_path.replace(".py", "_fixed.py")
        Path(output_path).write_text(fixed, encoding="utf-8-sig")

        return output_path
    except Exception as e:
        print(f"Error fixing script: {e}")
        return None


# Example usage
fixed_path = fix_reddit_script(r"D:\MAGIC\reddit_api.py")
if fixed_path:
    print(f"Successfully created fixed version at: {fixed_path}")
    print("You can now run:")
    print(f"python {fixed_path}")
else:
    print("Failed to fix the Reddit script")
