import os
import re
import requests

# CONFIG
TARGET_FOLDER = "docs/"  # Folder with Markdown or text docs
LOG_FILE = "outputs/logs/broken_links_report.txt"
CHECK_EXTENSIONS = [".md", ".txt"]

# Regex for links and images
LINK_PATTERN = r"\[.*?\]\((.*?)\)"
IMAGE_PATTERN = r"!\[.*?\]\((.*?)\)"

broken_links = []


def is_url_dead(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code >= 400
    except:
        return True


for root, _, files in os.walk(TARGET_FOLDER):
    for file in files:
        if any(file.endswith(ext) for ext in CHECK_EXTENSIONS):
            path = os.path.join(root, file)
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                    links = re.findall(LINK_PATTERN, content)
                    images = re.findall(IMAGE_PATTERN, content)
                    all_links = links + images
                    for link in all_links:
                        if link.startswith("http") and is_url_dead(link):
                            broken_links.append(f"{path} → ❌ Broken URL: {link}")
                        elif not link.startswith("http") and not os.path.exists(link):
                            broken_links.append(
                                f"{path} → ❌ Missing local file: {link}"
                            )
            except Exception as e:
                broken_links.append(f"{path} → ⚠️ {e}")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if broken_links:
        f.write("🚨 Broken links or embeds found:\n" + "\n".join(broken_links))
    else:
        f.write("✅ All links and embeds look fine.\n")

print(f"🔗 Link check complete. Report saved to: {LOG_FILE}")
