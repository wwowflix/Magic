import os
import time

TRIGGER_FOLDER = "D:/MAGIC/inbox"
TRIGGER_KEYWORDS = ["emergency", "rebuild", "resync"]

print("ðŸ” Trigger Monitor running...")

while True:
    for filename in os.listdir(TRIGGER_FOLDER):
        for keyword in TRIGGER_KEYWORDS:
            if keyword in filename.lower():
                print(f"ðŸš¨ Trigger detected: {filename} â†’ Matched: {keyword}")
                # Later you can trigger agents here
    time.sleep(5)
