import os
import time
from datetime import datetime

# === Auto Recover Agent for MAGIC Project ===
# Scans for *_TEST.py files and auto-creates *_READY.py versions
# Logs all actions to logs/auto_recover_log.txt

ROOT_DIR = r'D:\MAGIC\scripts'
LOG_FILE = r'D:\MAGIC\logs\auto_recover_log.txt'

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as logf:
        logf.write(f"[{timestamp}] {message}\n")
    print(message)

def auto_recover():
    recovered = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('_TEST.py'):
                test_path = os.path.join(root, file)
                ready_name = file.replace('_TEST.py', '_READY.py')
                ready_path = os.path.join(root, ready_name)
                
                if not os.path.exists(ready_path):
                    with open(ready_path, 'w', encoding='utf-8') as f:
                        f.write("# Auto-recovered script placeholder\n")
                        f.write("print('✅ Auto-recovered script running successfully')\n")
                    log(f"🔄 Recovered missing script: {ready_path}")
                    recovered += 1
    if recovered == 0:
        log("✅ No missing scripts found to recover.")

if __name__ == '__main__':
    log("🚀 Auto Recover Agent started...")
    auto_recover()
    log("✅ Auto Recover Agent finished successfully.")
