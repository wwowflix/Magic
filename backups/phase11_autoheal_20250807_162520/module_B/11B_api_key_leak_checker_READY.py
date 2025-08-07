import re

def check_api_keys(file_path):
    pattern = r'(api[_-]?key\s*=\s*["\'][A-Za-z0-9_\-]{16,}["\'])'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(pattern, content, re.IGNORECASE)
            return matches
    except Exception as e:
        print(f"? Error reading file {file_path}: {e}")
        return []

def scan_repo():
    import os
    base = 'scripts'
    for root, _, files in os.walk(base):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                keys = check_api_keys(path)
                if keys:
                    print(f"?? {file}: Potential API key(s) found:")
                    for key in keys:
                        print(f"  • {key}")

if __name__ == "__main__":
    print("?? Starting API Key Leak Scan")
    scan_repo()
    print("? Scan complete")
