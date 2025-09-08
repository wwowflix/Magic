import argparse, os, time


def cleanup(path="outputs", retention_days=7, max_mb=2048):
    cutoff = time.time() - (retention_days * 86400)
    total_size = 0
    for root, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                st = os.stat(fp)
            except FileNotFoundError:
                continue
            total_size += st.st_size
            if st.st_mtime < cutoff:
                print("Deleting old file:", fp)
                try:
                    os.remove(fp)
                except Exception as e:
                    print("  Error:", e)
    mb = total_size / (1024 * 1024)
    if mb > max_mb:
        print(f"âš  Folder {path} is {mb:.1f} MB (limit {max_mb} MB)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Cleanup logs/tmp and warn on size cap.")
    p.add_argument("--path", default="outputs")
    p.add_argument("--retention-days", type=int, default=7)
    p.add_argument("--max-mb", type=int, default=2048)
    a = p.parse_args()
    cleanup(a.path, a.retention_days, a.max_mb)
