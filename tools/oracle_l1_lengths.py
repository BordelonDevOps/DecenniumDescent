"""Measure Oracle L1 revelation description lengths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src/data/oracle-mysteries.js").read_text(encoding="utf-8")

# Split on mystery id blocks
for m in re.finditer(
    r'id: "(\w+)".*?level1: \{[^}]*?description:\s*"((?:[^"\\]|\\.)*)"',
    text,
    re.DOTALL,
):
    mid = m.group(1)
    desc = m.group(2)
    start = text.index(f'id: "{mid}"')
    end = text.find("\n  {", start + 1)
    if end == -1:
        end = len(text)
    draft = "draft: true" in text[start:end]
    print(f"{len(desc):3d} draft={draft} | {mid}")
