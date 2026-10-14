"""Apply class tags by spell name (handles duplicate keys)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "tools" / "spell_school_diff_report.json"
SPELLS = ROOT / "src" / "data" / "spells.js"


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    by_name = {item["name"]: item["addClasses"] for item in report["classTagAdds"]}
    text = SPELLS.read_text(encoding="utf-8")
    updates = 0
    tags_added = 0

    pattern = re.compile(
        r'(\{[^{}]*?name:\s*"(?P<name>[^"]+)"[^{}]*?classes:\s*\[)(?P<classes>[^\]]*)(\])',
        re.S,
    )

    def repl(m: re.Match[str]) -> str:
        nonlocal updates, tags_added
        name = m.group("name")
        if name not in by_name:
            return m.group(0)
        existing = re.findall(r'"([^"]+)"', m.group("classes"))
        missing = [c for c in by_name[name] if c not in existing]
        if not missing:
            return m.group(0)
        merged = existing + missing
        new_classes = ", ".join(json.dumps(c) for c in merged)
        updates += 1
        tags_added += len(missing)
        return m.group(1) + new_classes + m.group(3)

    text = pattern.sub(repl, text)
    if updates:
        SPELLS.write_text(text, encoding="utf-8")
    print(f"blocks_updated={updates} class_tags_added={tags_added}")


if __name__ == "__main__":
    main()
