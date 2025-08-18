import os

scripts = set()
referenced = set()
for root, _, files in os.walk("scripts"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            scripts.add(path)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "import " in line or "from " in line:
                        referenced.add(line.strip())
orphans = scripts - referenced
with open("outputs/logs/11H_orphan_file_detector.log", "w") as f:
    f.write("\n".join(orphans))
print(f"?? Found {len(orphans)} orphan Python files.")
