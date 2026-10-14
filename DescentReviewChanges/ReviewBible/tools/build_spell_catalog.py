"""Build the authoritative Decennium Descent spell catalog from Player Rulebook spell lists.

The Player Rulebook contains 936 school placements (104 per school) representing
848 unique named spells. The app catalog stores each spell once and preserves every
school/level placement in `placements`, with class-specific access levels derived
from `class_spell_school_mapping.csv`.

Oracle, Soldier, and Warrior are intentionally excluded from Weave spell access:
Oracle uses Revelation Charges; Soldier and Warrior use their class engines.
"""
from __future__ import annotations

import csv
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "rulebook_output.txt"
MAPPING = ROOT / "class_spell_school_mapping.csv"
PROGRESSION = ROOT / "class_spell_progression.csv"
OUT_JS = ROOT / "src/data/spells.js"
OUT_PLACEMENTS = ROOT / "src/data/spell-placements.json"
OUT_REPORT = ROOT / "docs/mechanics/SPELL_CATALOG_CANON.md"

SCHOOLS = [
    "Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation",
    "Illusion", "Necromancy", "Transmutation", "Universal",
]
NON_WEAVE = {"Oracle", "Soldier", "Warrior"}
CANON_CLASSES = [
    "Bard", "Cleric", "Crimson Agent", "Dragoon", "Druid", "Mage", "Monk",
    "Mirrorsage", "Oracle", "Ranger", "Shaman", "Soldier", "Thief", "Tinker",
    "Warrior", "Wizard", "Paladin",
]

SCHOOL_HEADING = re.compile(
    r"^# Expanded (Abjuration|Conjuration|Divination|Enchantment|Evocation|Illusion|Necromancy|Transmutation|Universal) Spell List",
    re.M,
)
LEVEL_HEADING = re.compile(r"^##\s+(?:Cantrips \(Level 0\)|Level\s+(\d+)\s+Spells)", re.I)
SPELL_LINE = re.compile(r"^\d+\.\s+\*\*(.+?)\*\*\s*[–-]\s*(.+)$")


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def parse_rulebook() -> list[dict]:
    text = RULEBOOK.read_text(encoding="utf-8", errors="ignore")
    start = text.index("## Spell Lists")
    section = text[start:]
    headers = list(SCHOOL_HEADING.finditer(section))
    if len(headers) != 9:
        raise RuntimeError(f"Expected 9 spell-school headings, found {len(headers)}")
    entries: list[dict] = []
    for i, match in enumerate(headers):
        school = match.group(1)
        seg = section[match.end(): headers[i + 1].start() if i + 1 < len(headers) else len(section)]
        level: int | None = None
        for raw in seg.splitlines():
            line = raw.strip()
            mh = LEVEL_HEADING.match(line)
            if mh:
                level = 0 if "Cantrips" in line else int(mh.group(1))
                continue
            sm = SPELL_LINE.match(line)
            if sm and level is not None:
                entries.append({
                    "name": sm.group(1).strip(),
                    "school": school,
                    "level": level,
                    "summary": sm.group(2).strip(),
                })
    return entries


def load_mapping() -> dict[str, list[str]]:
    with MAPPING.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        mapping: dict[str, list[str]] = {}
        for row in reader:
            cls = (row.get("") or row.get("Class") or "").strip()
            if not cls:
                continue
            mapping[cls] = [school for school in SCHOOLS if str(row.get(school, "0")).strip() == "1"]
    # Wizard is the universal scholarly caster in the current Player Rulebook.
    mapping["Wizard"] = list(SCHOOLS)
    # These classes do not draw on the general Weave spell catalog.
    for cls in NON_WEAVE:
        mapping[cls] = []
    return mapping


def load_progression() -> dict[str, dict]:
    with PROGRESSION.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        out: dict[str, dict] = {}
        for row in reader:
            cls = row["Class"].strip()
            learn_levels: dict[int, int] = {}
            for rank in range(10):
                raw = (row.get(f"Rank{rank}") or "").strip()
                if raw:
                    learn_levels[rank] = int(raw)
            out[cls] = {
                "mode": row["Mode"].strip(),
                "maxRank": int(row["MaxRank"] or 0),
                "learnLevels": learn_levels,
            }
        return out


def build(entries: list[dict], mapping: dict[str, list[str]], progression: dict[str, dict]) -> OrderedDict[str, dict]:
    by_name: OrderedDict[str, list[dict]] = OrderedDict()
    display_name: dict[str, str] = {}
    for entry in entries:
        nk = entry["name"].casefold()
        display_name.setdefault(nk, entry["name"])
        by_name.setdefault(nk, []).append(entry)

    catalog: OrderedDict[str, dict] = OrderedDict()
    used_keys: set[str] = set()
    for nk, placements in by_name.items():
        name = display_name[nk]
        key = slug(name)
        if key in used_keys:
            base = key
            n = 2
            while f"{base}-{n}" in used_keys:
                n += 1
            key = f"{base}-{n}"
        used_keys.add(key)

        schools = []
        levels = []
        summaries = []
        for p in placements:
            if p["school"] not in schools:
                schools.append(p["school"])
            if p["level"] not in levels:
                levels.append(p["level"])
            if p["summary"] not in summaries:
                summaries.append(p["summary"])

        class_levels: dict[str, int] = {}
        class_schools: dict[str, str] = {}
        class_learn_levels: dict[str, int] = {}
        for cls in CANON_CLASSES:
            if cls in NON_WEAVE:
                continue
            allowed = set(mapping.get(cls, []))
            candidates = [p for p in placements if p["school"] in allowed]
            if not candidates:
                continue
            chosen_rank = min(p["level"] for p in candidates)
            prog = progression.get(cls, {"maxRank": 0, "learnLevels": {}})
            if chosen_rank > prog["maxRank"]:
                continue
            learn_level = prog["learnLevels"].get(chosen_rank)
            if learn_level is None or learn_level > 20:
                continue
            chosen = next(p for p in candidates if p["level"] == chosen_rank)
            class_levels[cls] = chosen_rank
            class_schools[cls] = chosen["school"]
            class_learn_levels[cls] = learn_level

        catalog[key] = {
            "name": name,
            "level": min(p["level"] for p in placements),
            "resonanceRank": min(p["level"] for p in placements),
            "school": placements[0]["school"],
            "schools": schools,
            "placements": placements,
            "classLevels": class_levels,
            "classRanks": class_levels,
            "classLearnLevels": class_learn_levels,
            "classSchools": class_schools,
            "castingTime": "Not specified in current rulebook",
            "range": "Not specified in current rulebook",
            "components": "Not specified in current rulebook",
            "duration": "Not specified in current rulebook",
            "description": summaries[0],
            "alternateSummaries": summaries[1:],
            "classes": [cls for cls in CANON_CLASSES if cls in class_levels],
            "status": "canon",
            "source": "Player Rulebook — Spell Lists",
        }
    return catalog


def js_dump(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def write_js(catalog: OrderedDict[str, dict]) -> None:
    payload = js_dump(catalog)
    text = f'''/**\n * AUTHORITATIVE SPELL CATALOG — generated from Player Rulebook `## Spell Lists`.\n *\n * 936 school placements / 848 unique spells. Do not hand-edit this file; run\n * `python tools/build_spell_catalog.py` after changing the Player Rulebook extract.\n * Oracle uses Revelation Charges and is intentionally excluded from Weave access.\n * Soldier and Warrior likewise do not use the general Weave catalog.\n */\nexport const SPELLS = {payload};\n\nexport const SPELL_SCHOOLS = {js_dump(SCHOOLS)};\nexport const SPELL_LEVELS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];\n\nexport function getSpellsBySchool(school) {{\n  return Object.values(SPELLS).filter((spell) => (spell.schools || [spell.school]).includes(school));\n}}\n\nexport function getSpellsByLevel(level) {{\n  return Object.values(SPELLS).filter((spell) => spell.level === level || (spell.placements || []).some((p) => p.level === level));\n}}\n\nexport function getSpellsByClass(className) {{\n  return Object.values(SPELLS).filter((spell) => Object.prototype.hasOwnProperty.call(spell.classLevels || {{}}, className));\n}}\n\nexport function searchSpells(query) {{\n  const q = String(query || "").toLowerCase();\n  return Object.values(SPELLS).filter((spell) =>\n    spell.name.toLowerCase().includes(q) ||\n    spell.description.toLowerCase().includes(q) ||\n    (spell.schools || [spell.school]).some((s) => s.toLowerCase().includes(q))\n  );\n}}\n\nexport function getSpellsBySchoolAndLevel(school, level) {{\n  return Object.values(SPELLS).filter((spell) =>\n    (spell.placements || []).some((p) => p.school === school && p.level === level)\n  );\n}}\n\nexport function getCantrips() {{ return getSpellsByLevel(0); }}\nexport function getHighLevelSpells(minLevel = 6) {{\n  return Object.values(SPELLS).filter((spell) => Math.max(...(spell.placements || [{{ level: spell.level }}]).map((p) => p.level)) >= minLevel);\n}}\nexport function getSpellCount() {{ return Object.keys(SPELLS).length; }}\nexport function getSpellsByComponent(component) {{\n  const q = String(component || "").toLowerCase();\n  return Object.values(SPELLS).filter((spell) => spell.components.toLowerCase().includes(q));\n}}\nexport function getSpellsByDuration(durationType) {{\n  const q = String(durationType || "").toLowerCase();\n  return Object.values(SPELLS).filter((spell) => spell.duration.toLowerCase().includes(q));\n}}\n\nexport default SPELLS;\n'''
    OUT_JS.write_text(text, encoding="utf-8")


def write_report(entries: list[dict], catalog: OrderedDict[str, dict], mapping: dict[str, list[str]], progression: dict[str, dict]) -> None:
    multi = [s for s in catalog.values() if len(s["placements"]) > 1]
    lines = [
        "# Spell Catalog Canon",
        "",
        "This file documents the authoritative spell-data contract used by the Player Rulebook and companion app.",
        "",
        f"- **School placements:** {len(entries)}",
        f"- **Unique spells:** {len(catalog)}",
        f"- **Multi-school or multi-level names:** {len(multi)}",
        "- **Resonance Ranks:** 0–9",
        "- **General Weave casters:** 14 of 17 base classes",
        "- **Acquisition model:** class-specific learning levels; one spell can arrive at different character levels for different classes",
        "- **Oracle:** Revelation Charges only; no general Weave spellbook",
        "- **Soldier / Warrior:** no general Weave spellbook",
        "",
        "## Class school access and acquisition",
        "",
    ]
    for cls in CANON_CLASSES:
        schools = mapping.get(cls, [])
        prog = progression.get(cls, {"mode": "none", "maxRank": 0, "learnLevels": {}})
        if cls == "Oracle":
            desc = "Revelation Caster — Mystery/Curse/Revelation Charges; no general Weave ranks"
        elif not schools:
            desc = "No general Weave spell access"
        else:
            curve = ", ".join(f"R{rank}@L{lvl}" for rank, lvl in sorted(prog["learnLevels"].items()))
            desc = f"{prog['mode']} Weave; max Rank {prog['maxRank']}; {', '.join(schools)}; {curve}"
        lines.append(f"- **{cls}:** {desc}")
    lines += [
        "",
        "## Overlap and acquisition rule",
        "",
        "A named spell may appear in more than one school and at more than one Resonance Rank. The catalog stores that spell once while preserving every school/rank placement. For a given class, the lowest eligible placement determines the spell's **Resonance Rank and thread** for that class. The class's own acquisition curve then determines the **character level at which that class can learn it**. This intentionally allows the same spell to be learned by different classes at different character levels, in the tradition of class-driven MMORPG spell lists, without cloning the spell into separate records.",
        "",
        "This separation is deliberate: **Resonance Rank is not character level**. A shared spell can be early training for one class and advanced training for another.",
        "",
        "## Dissonance contract",
        "",
        "Spell access is governed by Resonance Rank and class learning level; repeated casting is governed separately by Dissonance. Rank 1–5 spells generate 1 base Dissonance, Rank 6–9 generate 2, and immediate repetition builds Refrain (+1/+2/+3). Cantrips cost 0 RP but repeated cantrips still build Refrain. Ordinary casters stop ranked casting at Fractured Dissonance; Lich and Necromancer are the explicit Traumatic Casting exceptions defined in `RESONANCE_CANON.md`.",
        "",
        "## Metadata status",
        "",
        "The current Player Rulebook gives concise rules summaries for all 936 placements but does not specify a complete casting-time/range/components/duration block for every unique spell. The companion therefore labels those four fields as `Not specified in current rulebook` rather than importing incompatible legacy-system metadata. This is deliberate; no missing mechanical field is silently invented.",
    ]
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    entries = parse_rulebook()
    if len(entries) != 936:
        raise RuntimeError(f"Expected 936 rulebook spell placements; found {len(entries)}")
    mapping = load_mapping()
    progression = load_progression()
    catalog = build(entries, mapping, progression)
    if len(catalog) != 848:
        raise RuntimeError(f"Expected 848 unique rulebook spells; found {len(catalog)}")
    OUT_PLACEMENTS.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_js(catalog)
    write_report(entries, catalog, mapping, progression)
    print(f"spell_placements={len(entries)} unique_spells={len(catalog)}")


if __name__ == "__main__":
    main()
