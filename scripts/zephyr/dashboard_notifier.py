#!/usr/bin/env python3
"""
dashboard_notifier.py

Notifies the system/dashboard that new trends have been processed.
Currently just prints confirmation, but can be extended to Slack, Notion, etc.
"""

import datetime
import os

timestamp = datetime.datetime.utcnow().isoformat()
signal_file = "D:/MAGIC/outputs/trends/dashboard_signal.log"

with open(signal_file, "a", encoding="utf-8") as f:
    f.write(f"[{timestamp}] ✅ Dashboard updated with new trends\n")

print(f"✅ Dashboard notified at {timestamp}")
