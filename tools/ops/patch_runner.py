import re, pathlib

p = pathlib.Path("tools/self_healing_runner_v5.py")
src = p.read_text(encoding="utf-8", errors="replace")

# -- Clean escaped quotes caused by earlier edits
src = src.replace('\\"""', '"""').replace('\\"', '"')

# -- Ensure `import re` exists after pathlib import
if not re.search(r'(?m)^\\s*import\\s+re\\b', src):
    src = re.sub(r'(?m)^(from\\s+pathlib\\s+import\\s+Path\\s*\\r?\\n)', r'\\1import re\\n', src)

# -- Remove any existing/broken helper and insert a clean one
src = re.sub(r'(?ms)^\\s*def\\s+_module_from_items\\s*\\(items\\):.*?(?=^\\S|\\Z)', '', src)

helper = """def _module_from_items(items):
    \"\"\"Pick module letter from manifest: prefer 'Module'; fallback parse from 'Path' like module_x.\"\"\"
    for it in items:
        if isinstance(it, dict) and it.get("Module"):
            return str(it["Module"]).strip().upper()
    for it in items:
        p = str(it.get("Path", "")) if isinstance(it, dict) else ""
        m = re.search(r"module_([A-Za-z])", p)
        if m:
            return m.group(1).upper()
    return "X"
"""

m = re.search(r'(?m)^PROJECT_ROOT\\s*=\\s*Path\\(__file__\\)\\.resolve\\(\\)\\.parents\\[1\\].*$', src)
if m:
    src = src[:m.end()] + "\\n" + helper + src[m.end():]
else:
    # Fallback: insert after imports
    m2 = re.search(r'(?m)^(?:from\\s+__future__.*\\r?\\n)?(?:import\\s+[^\\r\\n]+\\r?\\n)+', src)
    if m2:
        src = src[:m2.end()] + "\\n" + helper + src[m2.end():]
    else:
        src = helper + "\\n" + src

# -- Normalize summary_path to safe f-string
src = re.sub(
    r'(?ms)^\\s*summary_path\\s*=\\s*summaries_dir\\s*/\\s*(?:\\r?\\n\\s*)?(?:'
    r'f"phase11_module_.*?_summary_\\{ts\\}\\.tsv"|'
    r'"phase11_module_%s_summary_%s\\.tsv"\\s*%\\s*\\(_module_from_items\\(items\\),\\s*ts\\)'
    r')',
    '    summary_path = summaries_dir / f"phase11_module_{_module_from_items(items)}_summary_{ts}.tsv"',
    src
)

p.write_text(src, encoding="utf-8")

print("Patched:", p)
