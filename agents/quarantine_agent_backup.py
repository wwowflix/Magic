import os
import shutil
import sys

QUARANTINE_DIR = 'quarantine'

def quarantine_script(script_path):
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    base_name = os.path.basename(script_path)
    dest = os.path.join(QUARANTINE_DIR, base_name)
    print(f'Moving {script_path} to quarantine.')
    shutil.move(script_path, dest)

if __name__ == '__main__':
    # Example usage: pass failing script path as argument
    if len(sys.argv) < 2:
        print('Usage: python quarantine_agent.py <script_path>')
        sys.exit(1)
    script = sys.argv[1]
    quarantine_script(script)
