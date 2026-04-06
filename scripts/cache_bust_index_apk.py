#!/usr/bin/env python3
"""Append GITHUB_SHA to every APK URL string in pygbag's index.html (browser cache bust)."""
import os
import re
import sys
from pathlib import Path

INDEX = Path(os.environ.get("INDEX_HTML", "build/web/index.html"))


def discover_apk_basename(text: str) -> str:
    """Find the game bundle filename, e.g. lazer_balls.apk (pygbag template varies)."""
    patterns = (
        r"^\s*apk\s*=\s*[\"']([^\s\"'?]+\.apk)",  # apk = "name.apk"
        r"platform\.fopen\s*\(\s*[\"']([^\s\"'?]+\.apk)",  # fopen("name.apk"
        r"MM\.prepare\s*\(\s*[\"']([^\s\"'?]+\.apk)",  # prepare("name.apk"
    )
    for pat in patterns:
        m = re.search(pat, text, re.MULTILINE)
        if m:
            return m.group(1)
    # e.g. print("""... lazer_balls.apk""")
    m = re.search(r"\b([A-Za-z0-9_.]+\.apk)\b", text)
    if m:
        return m.group(1)
    return ""


def main() -> None:
    sha = os.environ.get("GITHUB_SHA", "").strip() or "local"
    sha = sha[:12]

    if not INDEX.is_file():
        print(f"error: {INDEX} not found — pygbag build may have failed", file=sys.stderr)
        sys.exit(1)

    text = INDEX.read_text(encoding="utf-8-sig")
    base = discover_apk_basename(text)
    if not base or not base.endswith(".apk"):
        print("error: could not discover *.apk bundle name in index.html", file=sys.stderr)
        sys.exit(1)

    escaped = re.escape(base)
    # Replace name.apk and name.apk?old with name.apk?v=<sha> everywhere (loader + print text).
    pat = re.compile(escaped + r"(?:\?v=[A-Za-z0-9]+)?")
    text2, n = pat.subn(f"{base}?v={sha}", text)
    if n == 0:
        print("error: APK basename found but regex replaced nothing", file=sys.stderr)
        sys.exit(1)

    INDEX.write_text(text2, encoding="utf-8")
    print(f"Patched {n} occurrence(s) of {base!r} with v={sha}")


if __name__ == "__main__":
    main()
