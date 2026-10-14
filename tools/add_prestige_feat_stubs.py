"""Add stub feats for prestige prerequisites missing from feats.js."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATS = ROOT / "src" / "data" / "feats.js"
LORE = ROOT / "src" / "data" / "prestige-lorebook.json"

STUB_NAMES = [
    "Anatomy Lore",
    "Arcane Adaptation",
    "Arcane Calculus",
    "Arcane Momentum",
    "Beast Lore",
    "Blood Ritual",
    "Combat Engineering",
    "Companion Training",
    "Conjure Flora",
    "Core Infusion",
    "Curse Channeling",
    "Curse Weaving",
    "Cursebound Flesh",
    "Dark Affinity",
    "Dark Binding",
    "Dark Fortitude",
    "Eldritch Combat",
    "Eldritch Echo",
    "Favored Enemy (Dragon)",
    "Forbidden Pact",
    "Frenzied Rage",
    "Giant Slayer",
    "Hardened Grip",
    "Hemocraft",
    "Life Drinker",
    "Lifeleech",
    "Lightning Affinity",
    "Master Smithing",
    "Mimicry",
    "Necrotic Affinity",
    "Precision Strike",
    "Primal Instinct",
    "Quickened Thought",
    "Siege Savant",
    "Slayer's Resolve",
    "Soul Cage",
    "Spell Reflection",
    "Stormcaller",
    "Temporal Theory",
    "Trapcasting",
    "Trapsetter",
    "Undying Flesh",
    "Verdant Bond",
    "Voltyros Pact",
    "Wounding Magic",
]


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return s


def main() -> None:
    lore = json.loads(LORE.read_text(encoding="utf-8"))
    text = FEATS.read_text(encoding="utf-8")
    defined = set(re.findall(r'"name":\s*"([^"]+)"', text))

    # Collect prestige paths referencing each feat
    refs: dict[str, list[str]] = {n: [] for n in STUB_NAMES}
    for p in lore:
        req = p.get("requirements", "")
        m = re.search(r"Feats:\s*(.+?)\s*-\s*Skills:", req)
        if not m:
            continue
        feats = [f.strip() for f in re.split(r",\s*", m.group(1).strip())]
        for f in feats:
            if f in refs:
                refs[f].append(p["name"])

    added: list[str] = []
    inserts: list[str] = []
    for name in STUB_NAMES:
        if name in defined:
            continue
        paths = refs.get(name, [])
        path_note = ", ".join(paths) if paths else "prestige paths"
        inserts.append(
            "  {\n"
            f'    "id": "{slug(name)}",\n'
            f'    "name": "{name}",\n'
            f'    "description": "Placeholder stub — referenced as a prestige class prerequisite ({path_note}). Full feat mechanics await author write-up.",\n'
            f'    "prerequisite": "Needs authoring",\n'
            f'    "effect": "Incomplete — required by prestige path(s); mechanical benefits not yet defined.",\n'
            f'    "type": "Incomplete"\n'
            "  }"
        )
        added.append(name)

    if not inserts:
        print("added=0")
        return

    marker = "\n];\nexport default feats;"
    if marker not in text:
        raise SystemExit("feats.js marker not found")
    text = text.replace(marker, ",\n" + ",\n".join(inserts) + marker, 1)
    FEATS.write_text(text, encoding="utf-8")
    print(f"added={len(added)}")
    for n in added:
        print(f"  {n}")


if __name__ == "__main__":
    main()
