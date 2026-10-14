"""One-shot verify after Opening clock purge. Disposable."""
from __future__ import annotations

import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
skip = {"node_modules", ".next", "dist", "out", "backups", ".git"}
exts = {".md", ".txt", ".json", ".ts", ".tsx", ".js", ".mjs", ".py"}

patterns = [
    (r"HORN_AT\s*=\s*120\b(?!\d)", "HORN_AT=120"),
    (r"At 120 hours(?: underground)?, a giant horn", "At 120 hours horn"),
    (r"horn sounds at \*\*120 hours\*\*", "horn 120 marked"),
    (r"\b240-hour Opening\b", "240-hour Opening"),
    (r"\bHorn at hour 120\b", "Horn hour 120"),
    (r"\b120 hours underground\b", "120h underground"),
    (r"Opening lasts 240 hours", "Opening lasts 240"),
    (r"Opening = 240 hours", "Opening = 240"),
    (r"ten-day Opening", "ten-day Opening"),
    (r"Horn at \*\*120\b", "Horn **120"),
    (r"legacy \*\*120-hour", "legacy 120-hour"),
    (r"HORN_AT=120\b(?!\d)", "HORN_AT=120"),
    (r"still.*?HORN_AT.*?120\b(?!\d)", "still HORN_AT 120"),
]

archive_parts = (
    "SIM_0",
    "SIM_1",
    "SIM_2",
    "SIM_3",
    "SIM_4",
    "SIM_5",
    "SIM_6",
    "T4_",
    "_opening_clock_scan",
    "_scan_opening",
    "_analyze_opening",
    "_target_clock",
    "_final_clock",
    "_purge_clock_verify",
    "OPENING_CLOCK_CONTINUITY_CHECK",
    "bible_clock",
)

live_wrong = []
archive = []
typo = []

for p in root.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in exts:
        continue
    if any(s in p.parts for s in skip):
        continue
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        continue
    masked = re.sub(r"1200|2400", "XXXX", text)
    rel = str(p.relative_to(root)).replace("\\", "/")
    lines = text.splitlines()
    for pat, label in patterns:
        for m in re.finditer(pat, masked, re.I):
            line_no = masked[: m.start()].count("\n") + 1
            snip = lines[line_no - 1].strip()[:160] if 0 < line_no <= len(lines) else ""
            if re.search(
                r"120 feet|expedition.{0,15}\b12\b|CR.?12|\bXP\b.?120|chapter.?12|6.?12 hour",
                snip,
                re.I,
            ):
                continue
            rec = {"file": rel, "line": line_no, "label": label, "snip": snip}
            if "DIRECTOR_BIBLE_CLOCK_TYPO" in rel or "OPENING_CLOCK_PURGE" in rel:
                typo.append(rec)
            elif any(a in rel for a in archive_parts):
                archive.append(rec)
            elif re.search(
                r"\btypo\b|corrected to|was a typo|pre-purge|historical (archive|record|sim)|dated archive",
                snip,
                re.I,
            ):
                typo.append(rec)
            else:
                live_wrong.append(rec)

print(f"LIVE-WRONG: {len(live_wrong)}")
for r in live_wrong:
    print(f"  {r['file']}:{r['line']} [{r['label']}] {r['snip']}")
print(f"TYPO/CONTEXT: {len(typo)}")
print(f"ARCHIVE: {len(archive)}")
checks = [
    ("src/components/SessionTracker.tsx", "HORN_AT = 1200"),
    ("src/data/dungeon-mechanics.json", "1200 hours"),
    ("src/data/floor-encounters.json", "1200 hours"),
    ("src/components/MonstersLibrary.tsx", "1200 hours"),
    ("scripts/ingest-data.mjs", "1200 hours"),
]
for f, s in checks:
    t = (root / f).read_text(encoding="utf-8", errors="ignore")
    print(f"CHECK {f}: {'OK' if s in t else 'MISSING ' + s}")
