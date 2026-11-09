#!/usr/bin/env python3
"""Validate local Markdown links without external network requests."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
errors = []
pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
for file in root.rglob("*.md"):
    for raw in pattern.findall(file.read_text(encoding="utf-8")):
        path = raw.split("#", 1)[0].strip().strip('"').split(" ", 1)[0]
        if not path or path.startswith(("http://", "https://", "mailto:", "data:", "/")):
            continue
        dest = (file.parent / unquote(path)).resolve()
        if not dest.is_relative_to(root) or not dest.exists():
            errors.append(f"{file.relative_to(root)} -> {raw}")
if errors:
    print("Broken local links:\n" + "\n".join(errors))
    sys.exit(1)
print("OK: local Markdown links verified.")
