"""Verify remaining class tag gaps."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / "tools/spell_school_diff_report.json").read_text(encoding="utf-8"))
text = (ROOT / "src/data/spells.js").read_text(encoding="utf-8")

spells_by_name: dict[str, list[list[str]]] = {}
for m in re.finditer(
    r'name:\s*"([^"]+)"[^{}]*?classes:\s*\[([^\]]*)\]',
    text,
    re.S,
):
    classes = re.findall(r'"([^"]+)"', m.group(2))
    spells_by_name.setdefault(m.group(1), []).append(classes)

for item in report["classTagAdds"]:
    name = item["name"]
    entries = spells_by_name.get(name, [])
    still_missing = []
    for add in item["addClasses"]:
        if not any(add in e for e in entries):
            still_missing.append(add)
    print(f"{name} ({len(entries)} entries): still missing {still_missing or 'NONE'}")
