"""Parse school spell lists from docx/md and diff vs src/data/spells.js.

Safe merge (--apply): add new spells only, or append missing class tags on existing spells.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WNS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

SCHOOLS = [
    "Conjuration",
    "Divination",
    "Enchantment",
    "Evocation",
    "Illusion",
    "Necromancy",
    "Transmutation",
    "Universal",
]

LEVEL_HEADER = re.compile(
    r"(?:Level\s+(\d+)|Cantrips?\s*\(Level\s+0\))",
    re.I,
)
SPELL_LINE = re.compile(r"^\d+\.\s+(.+)$")
MD_SPELL_HEADER = re.compile(r"^###\s+\d+\.\s+(.+)$")
MD_FIELD = re.compile(r"^\*\s+\*\*([^:*]+):\*\*\s*(.+)$")


@dataclass
class CanonSpell:
    name: str
    school: str
    level: int
    description: str = ""
    source: str = ""


@dataclass
class AppSpell:
    key: str
    name: str
    school: str
    level: int
    classes: list[str] = field(default_factory=list)
    description: str = ""


def slug_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def docx_paragraphs(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    out: list[str] = []
    for p in root.iter(f"{WNS}p"):
        text = "".join(t.text or "" for t in p.iter(f"{WNS}t")).strip()
        if text:
            out.append(text)
    return out


def parse_docx_spell_list(path: Path, school: str) -> list[CanonSpell]:
    spells: list[CanonSpell] = []
    level = 0
    for line in docx_paragraphs(path):
        lh = LEVEL_HEADER.search(line)
        if lh:
            level = 0 if "cantrip" in line.lower() else int(lh.group(1))
            continue
        m = SPELL_LINE.match(line)
        if not m:
            continue
        body = m.group(1).strip()
        if "–" in body:
            name, desc = body.split("–", 1)
        elif "-" in body and not body.startswith("5-ft"):
            parts = body.split("-", 1)
            name, desc = (parts[0], parts[1]) if len(parts) == 2 else (body, "")
        else:
            name, desc = body, ""
        name = name.strip()
        if not name or len(name) > 64:
            continue
        spells.append(
            CanonSpell(
                name=name,
                school=school,
                level=level,
                description=desc.strip(),
                source=path.name,
            )
        )
    return spells


def parse_md_spell_list(path: Path, school: str) -> list[CanonSpell]:
    text = path.read_text(encoding="utf-8")
    spells: list[CanonSpell] = []
    current: dict[str, str | int] = {}
    for line in text.splitlines():
        header = MD_SPELL_HEADER.match(line.strip())
        if header:
            if current.get("name"):
                spells.append(
                    CanonSpell(
                        name=str(current["name"]),
                        school=school,
                        level=int(current.get("level", 0)),
                        description=str(current.get("description", "")),
                        source=path.name,
                    )
                )
            current = {"name": header.group(1).strip(), "level": 0, "description": ""}
            continue
        fm = MD_FIELD.match(line.strip())
        if fm and current:
            key, val = fm.group(1).strip().lower(), fm.group(2).strip()
            if key == "level":
                current["level"] = int(re.search(r"\d+", val).group()) if re.search(r"\d+", val) else 0
            elif key == "description":
                current["description"] = val
    if current.get("name"):
        spells.append(
            CanonSpell(
                name=str(current["name"]),
                school=school,
                level=int(current.get("level", 0)),
                description=str(current.get("description", "")),
                source=path.name,
            )
        )
    return spells


def load_class_school_mapping() -> dict[str, list[str]]:
    path = ROOT / "class_spell_school_mapping.csv"
    if not path.is_file():
        return {}
    mapping: dict[str, list[str]] = {}
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        schools = [s for s in reader.fieldnames or [] if s and s != ""]
        for row in reader:
            cls = row.get("", row.get("Class", "")).strip()
            if not cls:
                continue
            mapping[cls] = [s for s in schools if str(row.get(s, "0")).strip() == "1"]
    return mapping


def default_classes_for_school(school: str, mapping: dict[str, list[str]]) -> list[str]:
    return sorted(cls for cls, schools in mapping.items() if school in schools)


def parse_app_spells() -> dict[str, AppSpell]:
    text = (ROOT / "src/data/spells.js").read_text(encoding="utf-8")
    spells: dict[str, AppSpell] = {}
    # match each spell object block
    for m in re.finditer(
        r'"([a-z0-9-]+)"\s*:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}',
        text,
        re.S,
    ):
        key, block = m.group(1), m.group(2)
        name_m = re.search(r'name:\s*"([^"]+)"', block)
        if not name_m:
            continue
        name = name_m.group(1)
        school_m = re.search(r'school:\s*"([^"]+)"', block)
        level_m = re.search(r"level:\s*(\d+)", block)
        classes_m = re.search(r"classes:\s*\[([^\]]*)\]", block)
        desc_m = re.search(r'description:\s*"((?:\\.|[^"\\])*)"', block, re.S)
        classes: list[str] = []
        if classes_m:
            classes = re.findall(r'"([^"]+)"', classes_m.group(1))
        spells[normalize_name(name)] = AppSpell(
            key=key,
            name=name,
            school=school_m.group(1) if school_m else "",
            level=int(level_m.group(1)) if level_m else 0,
            classes=classes,
            description=(desc_m.group(1).replace('\\"', '"') if desc_m else ""),
        )
    return spells


def collect_canon_spells() -> list[CanonSpell]:
    canon: list[CanonSpell] = []
    md_map = {
        "Abjuration": "abjuration_school_rebalanced.md",
        "Evocation": "evocation_school_spells_expanded.md",
        "Necromancy": "necromancy_school_spells_expanded.md",
        "Transmutation": "transmutation_school_spells_expanded.md",
        "Universal": "universal_school_spells_expanded.md",
    }
    for school in SCHOOLS:
        docx = ROOT / f"{school}_Spell_List.docx"
        if docx.is_file():
            canon.extend(parse_docx_spell_list(docx, school))
        md = ROOT / md_map.get(school, "")
        if md and md.is_file():
            canon.extend(parse_md_spell_list(md, school))
    # dedupe by normalized name, prefer md (richer description)
    by_name: dict[str, CanonSpell] = {}
    for s in canon:
        k = normalize_name(s.name)
        prev = by_name.get(k)
        if not prev or len(s.description) > len(prev.description):
            by_name[k] = s
    return list(by_name.values())


def diff_report(app: dict[str, AppSpell], canon: list[CanonSpell], mapping: dict[str, list[str]]) -> dict:
    new_spells: list[dict] = []
    class_tag_adds: list[dict] = []
    in_app_not_canon: list[str] = []
    canon_names = {normalize_name(c.name) for c in canon}

    for c in canon:
        nk = normalize_name(c.name)
        existing = app.get(nk)
        if not existing:
            new_spells.append(
                {
                    "name": c.name,
                    "school": c.school,
                    "level": c.level,
                    "source": c.source,
                    "suggestedClasses": default_classes_for_school(c.school, mapping),
                }
            )
            continue
        suggested = default_classes_for_school(c.school, mapping)
        missing_classes = [cls for cls in suggested if cls not in existing.classes]
        if missing_classes:
            class_tag_adds.append(
                {
                    "name": existing.name,
                    "key": existing.key,
                    "addClasses": missing_classes,
                    "school": c.school,
                }
            )

    for nk, s in app.items():
        if nk not in canon_names:
            in_app_not_canon.append(s.name)

    return {
        "appSpellCount": len(app),
        "canonSpellCount": len(canon),
        "newSpells": new_spells,
        "classTagAdds": class_tag_adds,
        "appOnlyNames": sorted(in_app_not_canon)[:50],
        "appOnlyCount": len(in_app_not_canon),
    }


def apply_safe_updates(
    report: dict,
    app: dict[str, AppSpell],
    canon: list[CanonSpell],
    mapping: dict[str, list[str]],
    *,
    args_apply_tags: bool = False,
) -> tuple[int, int]:
    path = ROOT / "src/data/spells.js"
    text = path.read_text(encoding="utf-8")
    added = 0
    tag_updates = 0

    canon_by_name = {normalize_name(c.name): c for c in canon}

    # append new spells before closing export
    if report["newSpells"]:
        inserts: list[str] = []
        seen_keys = {s.key for s in app.values()}
        for item in report["newSpells"]:
            c = canon_by_name[normalize_name(item["name"])]
            key = slug_key(c.name)
            base = key
            n = 2
            while key in seen_keys:
                key = f"{base}-{n}"
                n += 1
            seen_keys.add(key)
            classes = item["suggestedClasses"] or ["Wizard"]
            desc = (c.description or f"{c.school} spell from canon school list.").replace('"', '\\"')
            inserts.append(
                f'  "{key}": {{\n'
                f'    name: "{c.name}",\n'
                f"    level: {c.level},\n"
                f'    school: "{c.school}",\n'
                f'    castingTime: "1 action",\n'
                f'    range: "See spell description",\n'
                f'    components: "V, S",\n'
                f'    duration: "Instantaneous",\n'
                f'    description: "{desc}",\n'
                f"    classes: [{', '.join(json.dumps(x) for x in classes)}]\n"
                f"  }}"
            )
            added += 1
        marker = "\n};\n\n// Utility functions"
        if marker in text:
            text = text.replace(marker, ",\n" + ",\n".join(inserts) + marker, 1)

    if args_apply_tags:
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

    if added or tag_updates:
        path.write_text(text, encoding="utf-8")
    return added, tag_updates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Append canon spells missing from spells.js")
    parser.add_argument(
        "--apply-tags",
        action="store_true",
        help="Add missing class tags (additive merge from school mapping)",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args()

    mapping = load_class_school_mapping()
    app = parse_app_spells()
    canon = collect_canon_spells()
    report = diff_report(app, canon, mapping)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"app_spells={report['appSpellCount']}")
        print(f"canon_unique={report['canonSpellCount']}")
        print(f"new_spells={len(report['newSpells'])}")
        print(f"class_tag_adds={len(report['classTagAdds'])}")
        print(f"app_only={report['appOnlyCount']}")
        for school in SCHOOLS:
            school_new = [s for s in report["newSpells"] if s["school"] == school]
            if school_new:
                print(f"  {school} new: {len(school_new)}")
                for s in school_new[:8]:
                    print(f"    + {s['name']} (L{s['level']})")
                if len(school_new) > 8:
                    print(f"    ... +{len(school_new)-8} more")

    report_path = ROOT / "tools" / "spell_school_diff_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.apply or args.apply_tags:
        added, tags = apply_safe_updates(
            report, app, canon, mapping, args_apply_tags=args.apply_tags
        )
        print(f"applied: new_spells={added} class_tag_updates={tags}")


if __name__ == "__main__":
    main()
