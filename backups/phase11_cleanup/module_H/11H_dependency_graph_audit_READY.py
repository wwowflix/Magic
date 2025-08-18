import os
from collections import defaultdict

imports = defaultdict(set)
for root, _, files in os.walk("scripts"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.startswith("import") or line.startswith("from"):
                        imports[file].add(line.strip())
with open("outputs/logs/11H_dependency_graph_audit.log", "w") as f:
    for file, lines in imports.items():
        f.write(f"{file} imports:\n" + "\n".join(lines) + "\n\n")
print("?? Dependency audit complete.")
