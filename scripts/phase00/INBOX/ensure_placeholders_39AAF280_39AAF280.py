import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--phases", required=True, help="Comma-separated phase numbers (e.g., 11)"
)
parser.add_argument(
    "--modules", required=True, help="Comma-separated module letters (e.g., A,B,C)"
)
args = parser.parse_args()

base_path = "scripts"

for phase in args.phases.split(","):
    for module in args.modules.split(","):
        folder = os.path.join(base_path, f"phase{phase}", f"module_{module}")
        os.makedirs(folder, exist_ok=True)

        placeholder_filename = f"{phase}{module}_placeholder_READY.py"
        placeholder_path = os.path.join(folder, placeholder_filename)

        if not os.path.exists(placeholder_path):
            with open(placeholder_path, "w", encoding="utf-8") as f:
                f.write(
                    f"""# Auto-generated placeholder
print("Phase {phase} Module {module} placeholder executed")

def main():
    print("✅ [{phase}{module}] placeholder logic stub")

if __name__ == "__main__":
    main()
"""
                )
            print(f"✅ Created: {placeholder_path}")
        else:
            print(f"⚠️ Already exists: {placeholder_path}")
