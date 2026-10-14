"""Apply additive class tags from spell_school_diff_report.json to spells.js."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "tools" / "spell_school_diff_report.json"
SPELLS = ROOT / "src" / "data" / "spells.js"


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    text = SPELLS.read_text(encoding="utf-8")
    tag_updates = 0
    tags_added = 0

    for item in report["classTagAdds"]:
        key = item["key"]
        add = item["addClasses"]
        pattern = rf'("{re.escape(key)}"\s*:\s*\{{[^}}]*?classes:\s*\[)([^\]]*)(\])'
        m = re.search(pattern, text, re.S)
        if not m:
            continue
        existing = re.findall(r'"([^"]+)"', m.group(2))
        missing = [c for c in add if c not in existing]
        if not missing:
            continue
        merged = existing + missing
        new_classes = ", ".join(json.dumps(c) for c in merged)
        text = text[: m.start()] + m.group(1) + new_classes + m.group(3) + text[m.end() :]
        tag_updates += 1
        tags_added += len(missing)

    if tag_updates:
        SPELLS.write_text(text, encoding="utf-8")

    print(f"spells_updated={tag_updates} class_tags_added={tags_added}")


if __name__ == "__main__":
    main()
