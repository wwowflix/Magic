#!/usr/bin/env python3
import pathlib
import re

ROOT = pathlib.Path(".").resolve()


def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write(p: pathlib.Path, s: str):
    if not s.endswith("\n"):
        s += "\n"
    p.write_text(s, encoding="utf-8")


def patch_lexer(p: pathlib.Path) -> bool:
    s = read(p)
    # fix bad escapes around backslash checks and slices
    s2 = s
    s2 = s2.replace('startswith("\\"):"', 'startswith("\\\\"):')  # line 193
    s2 = s2.replace('len("\\") :]', 'len("\\\\"):]')  # lines 194 & 197 (space variants)
    # more tolerant cleanup via regex:
    s2 = re.sub(r'startswith\("\\\\?"\)', 'startswith("\\\\")', s2)
    s2 = re.sub(r'len\("\\\\?"\)\s*:\s*\]', 'len("\\\\"):]', s2)
    if s2 != s:
        write(p, s2)
        return True
    return False


def patch_magic_dashboard(p: pathlib.Path) -> bool:
    s = read(p)
    # normalize mojibake and remove the extra trailing quote
    s2 = s
    s2 = s2.replace(
        'st.title("ðŸ§ MAGIC "" Trends Intelligence HQ")"',
        'st.title("🧠 MAGIC — Trends Intelligence HQ")',
    )
    if s2 == s:
        # fallback: fix common mojibake pieces individually and extra quote
        s2 = re.sub(
            r'st\.title\(".*?MAGIC.*?HQ"\)"',
            'st.title("MAGIC — Trends Intelligence HQ")',
            s,
        )
    if s2 != s:
        write(p, s2)
        return True
    return False


def patch_reddit(p: pathlib.Path) -> bool:
    s = read(p)
    # target the exact shown pattern: pass on line 36, then top-level lines 37-40
    pat = re.compile(
        r"(if __name__\s*==\s*['\"]__main__['\"]\s*:\s*\n\s*pass\s*\n)"
        r"\s*subreddits\s*=\s*\[.*?\]\s*\n"
        r"\s*trending_posts\s*=\s*fetch_reddit_trends\(subreddits\)\s*\n"
        r"\s*for\s+post\s+in\s+trending_posts:\s*\n"
        r"\s*print\(post\)",
        re.DOTALL,
    )
    repl = (
        "if __name__ == '__main__':\n"    subreddits = ['technology', 'machinelearning', 'ArtificialIntelligence']\n"    trending_posts = fetch_reddit_trends(subreddits)\n"    for post in trending_posts:\n"        print(post)"
    )
    s2, n = pat.subn(repl, s)
    if n == 0:
        # fallback: handle minor whitespace differences
        pat2 = re.compile(
            r"(if __name__\s*==\s*['\"]__main__['\"]\s*:\s*\n\s*pass[^\n]*\n)"
            r"(.*?)$",
            re.DOTALL,
        )
        if pat2.search(s):
            # Replace block starting at pass with indented version of detected lines if they exist  # noqa: E501
            lines = s.splitlines()
            try:
                i_main = next(
                    i
                    for i, l in enumerate(lines)  # noqa: E741
                    if re.search(r"if __name__\s*==\s*['\"]__main__['\"]\s*:", l)
                )
                i_pass = next(
                    i
                    for i in range(i_main + 1, len(lines))
                    if lines[i].strip().startswith("pass")
                )
                # from pass+1 to pass+4 we rewrite concrete expected lines
                if i_pass + 4 < len(lines):
                    lines[i_pass + 1 : i_pass + 5] = [
                        "    subreddits = ['technology', 'machinelearning', 'ArtificialIntelligence']",  # noqa: E501
                        "    trending_posts = fetch_reddit_trends(subreddits)",
                        "    for post in trending_posts:",
                        "        print(post)",
                    ]
                    s2 = "\n".join(lines) + ("\n" if not s.endswith("\n") else "")
                    n = 1
            except StopIteration:
                pass
    if n > 0 and s2 != s:
        write(p, s2)
        return True
    return False


def main():
    changed = 0
    # 1) lexer.py
    lp = ROOT / "scripts" / "lexer.py"
    if lp.exists() and patch_lexer(lp):
        changed += 1

    # 2) magic_dashboard.py
    md = ROOT / "scripts" / "magic_dashboard.py"
    if md.exists() and patch_magic_dashboard(md):
        changed += 1

    # 3–5) reddit trio
    for name in ("reddit_api_final.py", "reddit_api_fixed.py", "reddit_api_2.py"):
        rp = ROOT / "scripts" / name
        if rp.exists() and patch_reddit(rp):
            changed += 1

    print(f"PATCH_ROUND7 changed={changed}")


if __name__ == "__main__":
    main()
