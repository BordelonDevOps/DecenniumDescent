#!/usr/bin/env python3
"""Scrub D&D / Forgotten Realms IP from bestiary JSON and xlsx (owner ruling #4)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "src" / "bestiary_data_full.json"
XLSX_PATH = ROOT / "Bestiary.xlsx"
XLSX_LEGACY_PATH = ROOT / "final_bestiary.xlsx"

# Aethel-neutral renames — removes FR deities, iconic D&D setting names, and SRD-protected labels.
RENAME_MAP = {
    # Umbrin line (was Drow / Lolth; interim label Umbral Elf superseded 2026-07-29 PM)
    "Drow Priestess of Lolth": "Umbrin Spider-Priestess",
    "Drow Matron Mother": "Umbrin Matron",
    "Drow Arachnomancer": "Umbrin Arachnomancer",
    "Drow Elite Warrior": "Umbrin Elite Warrior",
    "Drow Favored Consort": "Umbrin Favored Consort",
    "Drow House Captain": "Umbrin House Captain",
    "Drow Inquisitor": "Umbrin Inquisitor",
    "Drow Mage": "Umbrin Mage",
    "Drow Shadowblade": "Umbrin Shadowblade",
    "Drow": "Umbrin",
    "Umbral Elf Spider-Priestess": "Umbrin Spider-Priestess",
    "Umbral Elf Matron": "Umbrin Matron",
    "Umbral Elf Arachnomancer": "Umbrin Arachnomancer",
    "Umbral Elf Elite Warrior": "Umbrin Elite Warrior",
    "Umbral Elf Favored Consort": "Umbrin Favored Consort",
    "Umbral Elf House Captain": "Umbrin House Captain",
    "Umbral Elf Inquisitor": "Umbrin Inquisitor",
    "Umbral Elf Mage": "Umbrin Mage",
    "Umbral Elf Shadowblade": "Umbrin Shadowblade",
    "Umbral Elf": "Umbrin",
    # Voidmind line (was Mind Flayer / Illithid / Alhoon)
    "Mind Flayer Arcanist": "Voidmind Arcanist",
    "Mind Flayer Lich": "Voidmind Lich",
    "Mind Flayer": "Voidmind",
    "Alhoon": "Voidmind Archivist",
    # Gaze Tyrant line (was Beholder kin)
    "Beholder (in lair)": "Gaze Tyrant (in lair)",
    "Beholder Zombie": "Gaze Tyrant Husk",
    "Death Tyrant (in lair)": "Gaze Tyrant Sovereign (in lair)",
    "Death Tyrant": "Gaze Tyrant Sovereign",
    "Beholder": "Gaze Tyrant",
    "Gauth": "Lesser Gaze Tyrant",
    # Astral Reaver / Ascetic line (was Gith)
    "Githyanki Supreme Commander": "Astral Reaver Supreme Commander",
    "Githyanki Kith'rak": "Astral Reaver War-Captain",
    "Githyanki Gish": "Astral Reaver Spellblade",
    "Githyanki Knight": "Astral Reaver Knight",
    "Githyanki Warrior": "Astral Reaver Warrior",
    "Githzerai Enlightened": "Astral Ascetic Enlightened",
    "Githzerai Anarch": "Astral Ascetic Anarch",
    "Githzerai Monk": "Astral Ascetic Monk",
    "Githzerai Zerth": "Astral Ascetic Sentinel",
    # Deep kin
    "Duergar Xarrorn": "Deep Dwarf Xarrorn",
    "Duergar Soulblade": "Deep Dwarf Soulblade",
    "Duergar Stone Guard": "Deep Dwarf Stone Guard",
    "Duergar Kavalrachni": "Deep Dwarf Kavalrachni",
    "Duergar Mind Master": "Deep Dwarf Mind Master",
    "Duergar Hammerer": "Deep Dwarf Hammerer",
    "Duergar Screamer": "Deep Dwarf Screamer",
    "Duergar Warlord": "Deep Dwarf Warlord",
    "Duergar Despot": "Deep Dwarf Despot",
    "Duergar": "Deep Dwarf",
    "Svirfneblin": "Cave Gnome",
    # Depth / serpent cults
    "Kuo-toa Archpriest": "Depth Toad Archpriest",
    "Kuo-toa Whip": "Depth Toad Taskmaster",
    "Kuo-toa": "Depth Toad",
    "Yuan-ti Nightmare Speaker": "Serpent-Blood Nightmare Speaker",
    "Yuan-ti Mind Whisperer": "Serpent-Blood Mind Whisperer",
    "Yuan-ti Pureblood": "Serpent-Blood Pureblood",
    "Yuan-ti Broodguard": "Serpent-Blood Broodguard",
    "Yuan-ti Abomination": "Serpent-Blood Abomination",
    "Yuan-ti Anathema": "Serpent-Blood Anathema",
    "Yuan-ti Pit Master": "Serpent-Blood Pit Master",
    "Yuan-ti Malison": "Serpent-Blood Malison",
    # Sporefolk (was Myconid)
    "Myconid Sovereign": "Sporefolk Sovereign",
    "Myconid Adult": "Sporefolk Adult",
    "Myconid Sprout": "Sporefolk Sprout",
    # Lore quality pass 2026-07-30 (Codex ledger + deity locks) — keep scrub in sync
    "Flumph": "Lumen Drifter",
    "Owlbear": "Hookbeast",
    "Tarrasque": "Worldbreaker",
    "Intellect Devourer": "Mind Leech",
    "Neothelid": "Spiral Worm",
    "Draegloth": "Umbrin Warborn",
    "Drider": "Umbrin Arachnid",
    "Displacer Beast": "Refractor Panther",
    "Hook Horror": "Rip-Auger",
    "Umber Hulk": "Deep Borer",
    "Rust Monster": "Corrosion Grazer",
    "Carrion Crawler": "Charnel Crawler",
    "Aarakocra": "Skyfolk of the High Vents",
    "Kenku": "Mimic-Crow",
    "Tortle": "Shellkin",
    "Tortle Druid": "Shellkin Warden",
    "Thri-kreen": "Chitin-Strider",
    "Bullywug": "Bogkin",
    "Grung": "Poison-Skin",
    "Grung Elite Warrior": "Poison-Skin Elite",
    "Grung Wildling": "Poison-Skin Wildling",
    "Gnoll Fang of Yeenoghu": "Gnoll Fang of the Howling Fracture",
    "Orc Blade of Ilneval": "Orc Blade of the Iron March",
    "Orc Eye of Gruumsh": "Orc Eye of the One-Eyed Pact",
    "Orc Hand of Yurtrus": "Orc Hand of the Rot Sigil",
    "Orc Nurtured One of Yurtrus": "Orc Nurtured One of the Rot Sigil",
    "Orc Red Fang of Shargaas": "Orc Red Fang of the Veiled Hunt",
    "Orc Claw of Luthic": "Orc Claw of the Den-Mother",
    "Spawn of Kyuss": "Spawn of the Worm Spiral",
    "Firenewt Warlock of Imix": "Firenewt Warlock of the Ember Court",
    "Xvart Warlock of Raxivort": "Xvart Warlock of the Nine-Legged Choir",
    "Merrenoloth": "Ferry-Wraith of the Hush",
    "Ultroloth": "Court Broker of the Hush",
    "Arcanaloth": "Hush-Broker Arcanaloth",
    "Canoloth": "Hush-Broker Canoloth",
    "Dhergoloth": "Hush-Broker Dhergoloth",
    "Hydroloth": "Hush-Broker Hydroloth",
    "Mezzoloth": "Hush-Broker Mezzoloth",
    "Nycaloth": "Hush-Broker Nycaloth",
    "Oinoloth": "Hush-Broker Oinoloth",
    "Yagnoloth": "Hush-Broker Yagnoloth",
    "Duodrone": "Order-Drone Duodrone",
    "Monodrone": "Order-Drone Monodrone",
    "Pentadrone": "Order-Drone Pentadrone",
    "Quadrone": "Order-Drone Quadrone",
    "Tridrone": "Order-Drone Tridrone",
    "Marut": "Order-Drone Marut",
    "Black Abishai": "Pact Devil (Black Court)",
    "Blue Abishai": "Pact Devil (Blue Court)",
    "Green Abishai": "Pact Devil (Green Court)",
    "Red Abishai": "Pact Devil (Red Court)",
    "White Abishai": "Pact Devil (White Court)",
    "Blue Slaad": "Chaos-Husk Blue",
    "Death Slaad": "Chaos-Husk Death",
    "Gray Slaad": "Chaos-Husk Gray",
    "Green Slaad": "Chaos-Husk Green",
    "Red Slaad": "Chaos-Husk Red",
    "Slaad Tadpole": "Chaos-Husk Tadpole",
    "Autumn Eladrin": "Season-Bound Autumn",
    "Spring Eladrin": "Season-Bound Spring",
    "Summer Eladrin": "Season-Bound Summer",
    "Winter Eladrin": "Season-Bound Winter",
    "Angry Sorrowsworn": "Angry Grief-Bound",
    "Hungry Sorrowsworn": "Hungry Grief-Bound",
    "Lonely Sorrowsworn": "Lonely Grief-Bound",
    "Lost Sorrowsworn": "Lost Grief-Bound",
    "Wretched Sorrowsworn": "Wretched Grief-Bound",
    "Star Spawn Grue": "Spiral Breach Grue",
    "Star Spawn Hulk": "Spiral Breach Hulk",
    "Star Spawn Larva Mage": "Spiral Breach Larva Mage",
    "Star Spawn Mangler": "Spiral Breach Mangler",
    "Star Spawn Seer": "Spiral Breach Seer",
    "Neogi": "Void Broker",
    "Neogi Hatchling": "Void Broker Hatchling",
    "Neogi Master": "Void Broker Master",
    "Balor": "Fracture-Kin Balor",
    "Marilith": "Fracture-Kin Marilith",
    "Glabrezu": "Fracture-Kin Glabrezu",
    "Nalfeshnee": "Fracture-Kin Nalfeshnee",
    "Vrock": "Fracture-Kin Vrock",
    "Hezrou": "Fracture-Kin Hezrou",
    "Babau": "Fracture-Kin Babau",
    "Dretch": "Fracture-Kin Dretch",
    "Manes": "Fracture-Kin Manes",
    "Molydeus": "Fracture-Kin Molydeus",
    "Nabassu": "Fracture-Kin Nabassu",
    "Goristro": "Fracture-Kin Goristro",
    "Yochlol": "Fracture-Kin Yochlol",
    "Armanite": "Fracture-Kin Armanite",
    "Bulezau": "Fracture-Kin Bulezau",
    "Shoosuva": "Fracture-Kin Shoosuva",
    "Maurezhi": "Fracture-Kin Maurezhi",
    "Alkilith": "Fracture-Kin Alkilith",
    "Wastrilith": "Fracture-Kin Wastrilith",
    "Sibriex": "Fracture-Kin Sibriex",
    "Chasme": "Fracture-Kin Chasme",
    "Quasit": "Fracture-Kin Quasit",
    "Barlgura": "Fracture-Kin Barlgura",
    "Shadow Demon": "Fracture-Kin Shadow Demon",
    "Vargouille": "Fracture-Kin Vargouille",
}


def rename_value(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        return value
    if value in RENAME_MAP:
        return RENAME_MAP[value]
    out = value
    for old, new in sorted(RENAME_MAP.items(), key=lambda x: -len(x[0])):
        if old in out:
            out = out.replace(old, new)
    return out


def scrub_json() -> int:
    with JSON_PATH.open(encoding="utf-8") as f:
        creatures = json.load(f)

    count = 0
    for creature in creatures:
        old_name = creature.get("name", "")
        new_name = rename_value(old_name)
        if new_name != old_name:
            creature["name"] = new_name
            count += 1
        for field in ("description", "tags", "zoneFound"):
            if field in creature and isinstance(creature[field], str):
                creature[field] = rename_value(creature[field])

    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(creatures, f, indent=2, ensure_ascii=False)

    return count


def scrub_xlsx_path(path: Path) -> int:
    from openpyxl import load_workbook

    if not path.exists():
        return 0
    wb = load_workbook(path)
    count = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                val = cell.value
                if isinstance(val, str):
                    new_val = rename_value(val)
                    if new_val != val:
                        cell.value = new_val
                        count += 1
    wb.save(path)
    return count


def scrub_xlsx() -> int:
    return scrub_xlsx_path(XLSX_PATH) + scrub_xlsx_path(XLSX_LEGACY_PATH)


if __name__ == "__main__":
    import sys
    json_count = 0 if "--xlsx-only" in sys.argv else scrub_json()
    xlsx_cells = scrub_xlsx()
    print(f"JSON entries renamed: {json_count}")
    print(f"XLSX cell replacements: {xlsx_cells}")
