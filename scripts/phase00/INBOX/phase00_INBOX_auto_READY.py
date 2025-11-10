"""
MAGIC phase00 INBOX module READY script.

This script performs initial readiness checks for the INBOX module in phase00.
It verifies the presence of the INBOX directory and ensures it contains at least one Python script.
"""

import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger("phase00.INBOX.READY")

def run():
    """
    Entry point for the phase00 INBOX readiness check.
    Performs basic validation and returns status information.
    Returns:
        dict: A dictionary containing status, phase, module, and details or error message.
    """
    try:
        logger.info("Starting INBOX readiness check for phase00.")

        inbox_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "INBOX")
        inbox_dir = os.path.normpath(inbox_dir)

        if not os.path.isdir(inbox_dir):
            logger.error(f"INBOX directory missing: {inbox_dir}")
            return {
                "status": "ERROR",
                "phase": "phase00",
                "module": "INBOX",
                "message": f"Missing directory: {inbox_dir}",
                "auto_generated": False,
            }
        logger.info(f"INBOX directory found: {inbox_dir}")

        py_files = [f for f in os.listdir(inbox_dir) if f.endswith(".py") and os.path.isfile(os.path.join(inbox_dir, f))]
        if not py_files:
            logger.warning("No Python scripts found in INBOX directory.")
            return {
                "status": "WARN",
                "phase": "phase00",
                "module": "INBOX",
                "message": "No Python scripts found in INBOX directory.",
                "auto_generated": False,
            }
        logger.info(f"Found Python scripts in INBOX: {py_files}")

        logger.info("INBOX readiness check completed successfully.")
        return {
            "status": "OK",
            "phase": "phase00",
            "module": "INBOX",
            "auto_generated": False,
            "details": {
                "inbox_dir": inbox_dir,
                "python_files_count": len(py_files),
                "python_files": sorted(py_files),
            },
        }

    except Exception as e:
        logger.exception("Exception during INBOX readiness check.")
        return {
            "status": "ERROR",
            "phase": "phase00",
            "module": "INBOX",
            "message": f"Exception: {str(e)}",
            "auto_generated": False,
        }

if __name__ == "__main__":
    result = run()
    print(result)
