"""
MAGIC phase00 QUARANTINE module.

This script performs initial quarantine checks and preparations
for the MAGIC system. It validates quarantine conditions,
logs key events, and returns a structured status report.
"""

import logging
import os
import datetime
import traceback

# Configure basic logging to a file and console
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'phase00_QUARANTINE.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME, mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def check_quarantine_conditions():
    """
    Perform quarantine condition checks.

    Returns:
        dict: A dictionary with keys:
            - 'quarantine_active' (bool): Whether quarantine is active.
            - 'reason' (str): Reason for quarantine or empty string.
            - 'timestamp' (str): ISO formatted timestamp of check.
    """
    quarantine_file = os.path.join(os.path.dirname(__file__), 'QUARANTINE_ACTIVE.flag')
    quarantine_active = False
    reason = ""
    try:
        if os.path.isfile(quarantine_file):
            quarantine_active = True
            try:
                with open(quarantine_file, 'r', encoding='utf-8') as f:
                    reason = f.read().strip()
                    if not reason:
                        reason = "No reason provided"
            except Exception as e:
                logging.warning(f"Failed to read quarantine reason from file: {e}")
                reason = "Unknown reason (failed to read file)"
        else:
            quarantine_active = False
            reason = ""
    except Exception as e:
        logging.error(f"Error checking quarantine file existence: {e}")
        quarantine_active = False
        reason = "Error checking quarantine file"
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    return {
        "quarantine_active": quarantine_active,
        "reason": reason,
        "timestamp": timestamp,
    }

def run():
    """
    Entry point for the MAGIC phase00 QUARANTINE script.

    Returns:
        dict: Status report including quarantine state and metadata.
    """
    logging.info("Starting phase00 QUARANTINE checks.")
    try:
        result = check_quarantine_conditions()
        status = "QUARANTINE_ACTIVE" if result["quarantine_active"] else "OK"
        logging.info(f"Quarantine status: {status}")
        if result["quarantine_active"]:
            logging.info(f"Quarantine reason: {result['reason']}")
        return {
            "status": status,
            "phase": "phase00",
            "module": "QUARANTINE",
            "quarantine_active": result["quarantine_active"],
            "quarantine_reason": result["reason"],
            "checked_at": result["timestamp"],
            "auto_generated": False,
        }
    except Exception as e:
        logging.error(f"Exception during quarantine check: {e}")
        logging.error(traceback.format_exc())
        return {
            "status": "ERROR",
            "phase": "phase00",
            "module": "QUARANTINE",
            "error_message": str(e),
            "auto_generated": False,
        }
