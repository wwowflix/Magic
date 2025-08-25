import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from ai_remediator import apply_remediation_ai
apply_remediation_ai(os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "_ai_probe.py"), error_text="SyntaxError: invalid syntax")
print("ai suggestion logged")
