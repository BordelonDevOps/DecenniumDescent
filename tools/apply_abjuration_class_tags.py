"""Add Abjuration school class tags from class_spell_school_mapping.csv."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPELLS = ROOT / "src" / "data" / "spells.js"
MAPPING = ROOT / "class_spell_school_mapping.csv"

ABJ_CLASSES = []
with MAPPING.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cls = row.get("", row.get("Class", "")).strip()
        if cls and str(row.get("Abjuration", "0")).strip() == "1":
            ABJ_CLASSES.append(cls)
ABJ_CLASSES = sorted(ABJ_CLASSES)


def main() -> None:
    text = SPELLS.read_text(encoding="utf-8")
    updates = 0
    tags = 0

    pattern = re.compile(
        r'(\{[^{}]*?school:\s*"Abjuration"[^{}]*?classes:\s*\[)([^\]]*)(\])',
        re.S,
    )

    def repl(m: re.Match[str]) -> str:
        nonlocal updates, tags
        existing = re.findall(r'"([^"]+)"', m.group(2))
        missing = [c for c in ABJ_CLASSES if c not in existing]
        if not missing:
            return m.group(0)
        merged = existing + missing
        updates += 1
        tags += len(missing)
        return m.group(1) + ", ".join(json.dumps(c) for c in merged) + m.group(3)

    text = pattern.sub(repl, text)
    if updates:
        SPELLS.write_text(text, encoding="utf-8")
    print(f"abjuration_blocks_updated={updates} tags_added={tags}")


if __name__ == "__main__":
    main()
