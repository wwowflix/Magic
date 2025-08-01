import os
log_blocks = []
for root, _, files in os.walk('scripts'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'def ' in content and 'log' not in content:
                    log_blocks.append(path)
with open('outputs/logs/11H_logging_coverage_analyzer.log', 'w') as f:
    f.write('\n'.join(log_blocks))
print(f"?? Found {len(log_blocks)} scripts missing logging.")
