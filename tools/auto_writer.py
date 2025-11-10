#!/usr/bin/env python
"""
auto_writer.py

Uses OpenAI to fill MAGIC *_READY.py scripts with real Python logic.

Safety rules:
- Only targets small / auto-generated stubs:
  - files ending with "_auto_READY.py", OR
  - files containing the marker "MAGIC auto-generated stub"
- Never touches bigger/manual files.

Usage examples:
    python tools/auto_writer.py --root E:\MAGIC\scripts --dry-run --max-files 5
    python tools/auto_writer.py --root E:\MAGIC\scripts --phase phase11 --max-files 20
"""

from __future__ import annotations
import argparse
from pathlib import Path
import os
import sys
import textwrap
from typing import List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=str,
        required=True,
        help="Root scripts folder, e.g. E:\\MAGIC\\scripts",
    )
    parser.add_argument(
        "--phase",
        type=str,
        default=None,
        help="Optional phase filter, e.g. 'phase11' (only process files under that folder)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=10,
        help="Maximum number of files to process in one run (default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write anything, just show which files WOULD be updated.",
    )
    return parser.parse_args()


def find_candidate_files(root: Path, phase_filter: Optional[str], max_files: int) -> List[Path]:
    """
    Find *_READY.py files that are safe to overwrite (auto stubs only).
    """
    candidates: List[Path] = []

    for path in root.rglob("*_READY.py"):
        # ❌ never touch __pycache__ folders
        if "__pycache__" in path.parts:
            continue

        # Optional phase filter (e.g. only phase11)
        if phase_filter and phase_filter not in path.parts:
            continue

        name = path.name
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            # If can't read, skip silently
            continue

        # Only touch REAL auto-stubs:
        # i.e. files that still contain the original stub marker text.
        if "MAGIC auto-generated stub" in text:
            candidates.append(path)

        if len(candidates) >= max_files:
            break

    return candidates



def build_prompt_for_file(path: Path, repo_root: Path) -> str:
    """
    Build the LLM prompt for a given stub file.
    """
    rel = path.relative_to(repo_root)
    parts = rel.parts

    # Best-effort phase/module extraction
    phase_name = next((p for p in parts if p.startswith("phase")), "unknown_phase")
    module_name = "unknown"
    if len(parts) >= 3:
        # e.g. scripts/phaseXX/MODULE/file.py
        module_name = parts[2]

    stub_text = path.read_text(encoding="utf-8")

    prompt = f"""
You are an expert Python engineer working on the MAGIC project (Multi-Agent Governance, Intelligence & Control).

You are editing this file:

  - Relative path: {rel}
  - Phase: {phase_name}
  - Module: {module_name}

Current contents of the file (a stub):

{stub_text}

GOAL:
- Replace this stub with REAL, production-quality Python code for MAGIC.
- Keep a clear function `def run()` as the main entrypoint that returns a dict-like status or structured result.
- Add a short docstring at the top explaining what this script does.
- Include basic logging or print statements for key events.
- Handle errors defensively with try/except where reasonable.

CONSTRAINTS:
- Output MUST be valid Python code only (no markdown, no explanations).
- Do NOT include any backticks or code fences.
- Do NOT call external network APIs.
- Prefer using only Python standard library.

Now output the COMPLETE Python file implementation, ready to save as {rel}.
"""
    return textwrap.dedent(prompt).strip()


def extract_code_from_response(content: str) -> str:
    """
    If the model accidentally returns markdown fences, strip them.
    Otherwise, return content as-is.
    """
    if "```" not in content:
        return content

    lines = content.splitlines()
    in_block = False
    code_lines: List[str] = []

    for line in lines:
        if line.strip().startswith("```"):
            in_block = not in_block
            continue
        if in_block:
            code_lines.append(line)

    if code_lines:
        return "\n".join(code_lines)
    return content


def ensure_client() -> "OpenAI":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set. "
            "Set it before running auto_writer.py."
        )
    if OpenAI is None:
        raise RuntimeError("openai package not installed. Run: pip install openai")
    # New-style OpenAI client
    client = OpenAI(api_key=api_key)
    return client


def call_llm(prompt: str) -> str:
    """
    Call the OpenAI chat completion API and return Python code.
    """
    client = ensure_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You generate complete Python files for the MAGIC automation system. "
                    "Output ONLY Python code, nothing else."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content or ""
    return extract_code_from_response(content)


def process_file(path: Path, repo_root: Path, dry_run: bool) -> None:
    """
    Process a single stub file:
    - Build prompt
    - (Optional) call LLM
    - Write back new code
    """
    rel = path.relative_to(repo_root)
    print(f"\n=== Processing: {rel} ===")

    prompt = build_prompt_for_file(path, repo_root)

    if dry_run:
        print("[DRY-RUN] Would send prompt to LLM for this file.")
        print("---------- Prompt preview (first 40 lines) ----------")
        preview_lines = "\n".join(prompt.splitlines()[:40])
        print(preview_lines)
        print("-----------------------------------------------------")
        return

    try:
        new_code = call_llm(prompt)
    except Exception as e:
        print(f"[ERROR] LLM call failed for {rel}: {e}", file=sys.stderr)
        return

    try:
        path.write_text(new_code, encoding="utf-8")
        print(f"[OK] Updated file: {rel}")
    except Exception as e:
        print(f"[ERROR] Failed to write file {rel}: {e}", file=sys.stderr)


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"[ERROR] Scripts root does not exist: {root}", file=sys.stderr)
        return 1

    repo_root = root.parents[0]  # assumes <repo>/scripts

    candidates = find_candidate_files(root, args.phase, args.max_files)

    if not candidates:
        print("[INFO] No candidate *_READY.py stub files found with current filters.")
        return 0

    print(f"[INFO] Found {len(candidates)} candidate files (max {args.max_files}).")
    for p in candidates:
        process_file(p, repo_root, args.dry_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
