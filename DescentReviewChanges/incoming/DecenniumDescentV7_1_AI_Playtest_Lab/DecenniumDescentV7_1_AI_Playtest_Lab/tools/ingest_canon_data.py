"""Ingest canon docx sources into src/data (feats, prestige, racial variants, races)."""
from __future__ import annotations

import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "src", "data")
WNS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def docx_paragraphs(path: str) -> list[str]:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    paras: list[str] = []
    for p in root.iter(f"{WNS}p"):
        texts = [t.text for t in p.iter(f"{WNS}t") if t.text]
        if texts:
            paras.append("".join(texts))
    return paras


def slug_id(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return s or "feat"


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def extract_named_objects(source: str, const_name: str) -> list[dict]:
    start = source.find(f"const {const_name}")
    if start < 0:
        return []
    i = source.index("{", start)
    depth = 0
    end = -1
    for j in range(i, len(source)):
        if source[j] == "{":
            depth += 1
        elif source[j] == "}":
            depth -= 1
            if depth == 0:
                end = j
                break
    block = source[start : end + 1]
    feats: list[dict] = []
    pat = re.compile(
        r"(\w+)\s*:\s*\{\s*name:\s*\"([^\"]+)\"\s*,\s*description:\s*\"((?:\\.|[^\"\\])*)\""
        r"\s*,\s*prerequisite:\s*\"((?:\\.|[^\"\\])*)\"\s*,\s*effect:\s*\"((?:\\.|[^\"\\])*)\""
        r"\s*,\s*type:\s*\"([^\"]+)\"",
        re.S,
    )
    for m in pat.finditer(block):
        feats.append(
            {
                "id": m.group(1),
                "name": m.group(2),
                "description": m.group(3).replace('\\"', '"'),
                "prerequisite": m.group(4).replace('\\"', '"'),
                "effect": m.group(5).replace('\\"', '"'),
                "type": m.group(6).replace("_", " ").title().replace(" ", "_"),
            }
        )
    # normalize type casing to match UI (General, Combat, Magic, etc.)
    type_map = {
        "General": "General",
        "Combat": "Combat",
        "Magic": "Magic",
        "Skill": "Skill",
        "Racial": "Racial",
        "Vital_Mutation": "Vital_mutation",
        "Combat_Mutation": "Combat_mutation",
        "Aberrant_Mutation": "Aberrant_mutation",
        "Social": "Social",
    }
    for f in feats:
        raw = f["type"]
        f["type"] = type_map.get(raw, raw.replace("_", " ").title())
    return feats


def parse_feat_block(paras: list[str], feat_type: str, *, stop_at: str | None = None, max_count: int | None = None) -> list[dict]:
    feats: list[dict] = []
    i = 0
    while i < len(paras):
        line = paras[i]
        if stop_at and stop_at in line:
            break
        if max_count is not None and len(feats) >= max_count:
            break
        if line.startswith("Decennium Descent") or line.startswith("These feats"):
            i += 1
            continue

        name: str | None = None
        m = re.match(r"(\d+)\.\s+(.+)", line)
        if m:
            name = m.group(2).strip()
        elif (
            line
            and not line.startswith("Effect:")
            and not line.startswith("Requirement")
            and re.match(r"^[A-Z]", line)
            and i + 1 < len(paras)
            and paras[i + 1].strip().startswith("Effect:")
        ):
            name = line.strip()

        if name and i + 2 < len(paras):
            eff_line = paras[i + 1].strip()
            req_line = paras[i + 2].strip()
            if eff_line.startswith("Effect:") and req_line.startswith("Requirement"):
                effect = eff_line.split(":", 1)[1].strip()
                req = req_line.split(":", 1)[1].strip()
                # strip accidental section header glued to requirement
                if "Decennium Descent" in req:
                    req = req.split("Decennium Descent", 1)[0].strip()
                    # stop after this feat if we hit embedded next section
                    feats.append(
                        {
                            "id": slug_id(name),
                            "name": name,
                            "description": f"{feat_type} feat from the Decennium Descent compendium.",
                            "prerequisite": req or "None",
                            "effect": effect,
                            "type": feat_type,
                        }
                    )
                    if stop_at:
                        break
                    i += 3
                    continue
                feats.append(
                    {
                        "id": slug_id(name),
                        "name": name,
                        "description": f"{feat_type} feat from the Decennium Descent compendium.",
                        "prerequisite": req or "None",
                        "effect": effect,
                        "type": feat_type,
                    }
                )
                i += 3
                continue
        i += 1
    return feats


def ingest_docx_feats() -> list[dict]:
    """Parse feat docx sources. Main Feats docx contains General+Combat+Magic sections."""
    out: list[dict] = []
    main = os.path.join(ROOT, "Decennium_Descent_Feats.docx")
    if os.path.isfile(main):
        out.extend(parse_feat_block(docx_paragraphs(main), "General", stop_at=None, max_count=None))
    # Standalone lists (same content split out; merge dedupes)
    files = [
        ("Decennium_Descent_Combat_Feats.docx", "Combat"),
        ("Decennium_Descent_Magic_Feats.docx", "Magic"),
        ("Decennium_Descent_Skill_Feats.docx", "Skill"),
    ]
    for fname, ftype in files:
        path = os.path.join(ROOT, fname)
        if os.path.isfile(path):
            out.extend(parse_feat_block(docx_paragraphs(path), ftype, stop_at=None, max_count=None))
    return out


def ingest_game_feats() -> list[dict]:
    gd = open(os.path.join(ROOT, "game-data.js"), encoding="utf-8").read()
    add = open(os.path.join(ROOT, "additional-feats.js"), encoding="utf-8").read()
    return extract_named_objects(gd, "FEATS") + extract_named_objects(add, "ADDITIONAL_FEATS")


def merge_feats(*pools: list[dict]) -> list[dict]:
    """Later pools override earlier by normalized name."""
    by_name: dict[str, dict] = {}
    for pool in pools:
        for f in pool:
            key = normalize_name(f["name"])
            existing = by_name.get(key)
            if existing:
                merged = {**existing, **f}
                if not f.get("description") or "compendium" in f.get("description", ""):
                    merged["description"] = existing.get("description") or f.get("description", "")
                by_name[key] = merged
            else:
                by_name[key] = dict(f)
    # ensure unique ids
    seen_ids: set[str] = set()
    result = []
    for f in sorted(by_name.values(), key=lambda x: x["name"].lower()):
        fid = f.get("id") or slug_id(f["name"])
        base = fid
        n = 2
        while fid in seen_ids:
            fid = f"{base}_{n}"
            n += 1
        f["id"] = fid
        seen_ids.add(fid)
        result.append(f)
    return result


def parse_racial_variants() -> list[dict]:
    path = os.path.join(ROOT, "Decennium_Descent_Finalized_Racial_Abilities_and_Feats.docx")
    if not os.path.isfile(path):
        return []
    text = "\n".join(docx_paragraphs(path))
    chunks = re.split(r"\n(?=[A-Z][^\n]+\([A-Za-z]+\)\s*\n➤)", text)
    variants: list[dict] = []
    for chunk in chunks:
        header = re.match(r"([^\n]+)\(([A-Za-z]+)\)", chunk)
        if not header:
            continue
        subrace = header.group(1).strip()
        parent = header.group(2).strip()
        ability_m = re.search(r"➤ New Ability:\s*(.+?)(?=➤|\Z)", chunk, re.S)
        feat_m = re.search(r"➤ Racial Feat:\s*(.+?)(?=\n[A-Z]|\Z)", chunk, re.S)
        ability = re.sub(r"\s+", " ", ability_m.group(1).strip()) if ability_m else ""
        racial_feat = re.sub(r"\s+", " ", feat_m.group(1).strip()) if feat_m else ""
        feat_name = racial_feat.split("–", 1)[0].split("-", 1)[0].strip()
        if "–" in racial_feat or "-" in racial_feat:
            parts = re.split(r"[–-]", racial_feat, maxsplit=1)
            feat_name = parts[0].strip()
            feat_effect = parts[1].strip() if len(parts) > 1 else racial_feat
        else:
            feat_effect = racial_feat
        variants.append(
            {
                "subrace": subrace,
                "parentRace": parent,
                "ability": ability,
                "racialFeat": {"name": feat_name, "effect": feat_effect},
            }
        )
    return variants


def racial_feat_entries(variants: list[dict]) -> list[dict]:
    seen: set[str] = set()
    feats: list[dict] = []
    for v in variants:
        rf = v.get("racialFeat") or {}
        name = rf.get("name", "").strip()
        if not name or normalize_name(name) in seen:
            continue
        seen.add(normalize_name(name))
        feats.append(
            {
                "id": slug_id(name),
                "name": name,
                "description": f"Racial feat tied to {v['parentRace']} heritage.",
                "prerequisite": f"{v['parentRace']} heritage",
                "effect": rf.get("effect", ""),
                "type": "Racial",
            }
        )
    return feats


def parse_prestige_docx() -> list[dict]:
    path = os.path.join(ROOT, "Decennium_Prestige_Classes.docx")
    text = "\n".join(docx_paragraphs(path))
    idx = text.find("1. Battlemage")
    block = text[idx:] if idx >= 0 else text
    entries = re.split(r"\n(?=\d+\. [A-Z])", block)
    prestige: list[dict] = []

    for entry in entries:
        m = re.match(r"(\d+)\. ([^\n]+)", entry)
        if not m:
            continue
        num, name = int(m.group(1)), m.group(2).strip()
        if num > 18:
            continue

        def grab(label: str) -> str:
            pat = rf"\*\*{re.escape(label)}\*\*:?\s*(.+?)(?=\*\*[A-Z]|\n\d+\. |\Z)"
            g = re.search(pat, entry, re.S)
            return re.sub(r"\s+", " ", g.group(1).strip()) if g else ""

        cap_m = re.search(
            r"\*\*Capstone[^*]*\*\*:?\s*(.+?)(?=\*\*Combat Role|\nCharacter Story|\Z)",
            entry,
            re.S,
        )
        capstone = re.sub(r"\s+", " ", cap_m.group(1).strip()) if cap_m else ""

        sig_m = re.search(r"\*\*Signature Mechanics\*\*:(.+?)(?=\*\*Capstone|\Z)", entry, re.S)
        hallmarks: list[str] = []
        if sig_m:
            for line in sig_m.group(1).split("\n"):
                line = line.strip().lstrip("- ")
                if line and not line.startswith("**"):
                    hallmarks.append(re.sub(r"\*\*", "", line))

        bm = re.search(r"Base Class:\s*([^\n]+)", entry)
        role_m = re.search(r"\*\*Combat Role\*\*:?\s*(.+?)(?=\nCharacter Story|\Z)", entry, re.S)
        combat_role = re.sub(r"\s+", " ", role_m.group(1).strip()) if role_m else ""
        combat_role = combat_role.split("Character Story")[0].strip()

        prestige.append(
            {
                "num": num,
                "name": name,
                "baseClass": bm.group(1).strip() if bm else "",
                "summary": grab("Overview"),
                "requirements": grab("Requirements"),
                "unlock": grab("Unlock"),
                "entrance": grab("Unlock") or grab("Requirements")[:160],
                "hallmarks": hallmarks[:8],
                "capstone": capstone,
                "combatRole": combat_role,
            }
        )
    return prestige


def builder_races_template() -> list[dict]:
    """Canonical builder race list (clean traits; subrace names match racial doc)."""
    return [
        {
            "name": "Amphibian",
            "info": "Aquatic humanoids with a deep connection to water and wetlands.",
            "abilityScoreIncrease": "Constitution +2, Wisdom +1",
            "size": "Medium",
            "speed": "30 feet, Swim 30 feet",
            "traits": ["Amphibious", "Natural Swimmer", "Poison Resistance", "Swamp Camouflage"],
            "languages": ["Common", "Aquan"],
            "subraces": ["River Amphibian", "Poison Amphibian", "Jungle Amphibian"],
        },
        {
            "name": "Umbrin",
            "info": "Truly dark and mysterious elves of The Murk — obsidian-skinned children of exile. Calan'thir and the First Choir shunned them and burned their flesh to living obsidian when they were banished from his light. They worship a perverse idea of Umbra, not the wholesome faith of the Choir, and are hated by most surface folk — yet capable of very strange alliances when necessity demands.",
            "abilityScoreIncrease": "Dexterity +2, Charisma +1",
            "size": "Medium",
            "speed": "30 feet",
            "traits": ["Superior Darkvision", "Sunlight Sensitivity", "Umbrin Magic", "Umbrin Weapon Training"],
            "languages": ["Common", "Elvish", "Murkish"],
            "subraces": ["Obsidian Highborn", "Shadow Blade", "Cavern Mystic"],
        },
        {
            "name": "Drakari",
            "info": "Draconic humanoids with elemental ancestry and natural magic.",
            "abilityScoreIncrease": "Strength +2, Charisma +1",
            "size": "Medium",
            "speed": "30 feet",
            "traits": ["Draconic Ancestry", "Breath Weapon", "Damage Resistance", "Draconic Pride"],
            "languages": ["Common", "Draconic"],
            "subraces": [
                "Flame Drakari",
                "Frost Drakari",
                "Storm Drakari",
                "Stone Drakari",
                "Gale Drakari",
                "Wave Drakari",
            ],
        },
        {
            "name": "Dwarf",
            "info": "Stout folk tied to stone, forge, and mountain halls.",
            "abilityScoreIncrease": "Constitution +2",
            "size": "Medium",
            "speed": "25 feet",
            "traits": ["Darkvision", "Dwarven Resilience", "Dwarven Combat Training", "Stonecunning"],
            "languages": ["Common", "Dwarvish"],
            "subraces": ["Mountain Dwarf", "Forge Dwarf", "Deep Dwarf"],
        },
        {
            "name": "Elf",
            "info": "Graceful, long-lived beings with keen senses and magical affinity.",
            "abilityScoreIncrease": "Dexterity +2",
            "size": "Medium",
            "speed": "30 feet",
            "traits": ["Darkvision", "Keen Senses", "Fey Ancestry", "Trance"],
            "languages": ["Common", "Elvish"],
            "subraces": ["High Elf", "Wood Elf", "Twilight Elf"],
        },
        {
            "name": "Feykin",
            "info": "Humanoids touched by fey magic and seasonal power.",
            "abilityScoreIncrease": "Dexterity +2, Charisma +1",
            "size": "Medium",
            "speed": "30 feet",
            "traits": ["Fey Ancestry", "Natural Magic", "Fey Step", "Seasonal Affinity"],
            "languages": ["Common", "Sylvan"],
            "subraces": ["Summer Fey", "Winter Fey", "Twilight Fey"],
        },
        {
            "name": "Gnome",
            "info": "Curious small folk who delight in invention and discovery.",
            "abilityScoreIncrease": "Intelligence +2",
            "size": "Small",
            "speed": "25 feet",
            "traits": ["Darkvision", "Gnome Cunning", "Natural Illusionist"],
            "languages": ["Common", "Gnomish"],
            "subraces": ["Tinker Gnome", "Arcanist Gnome", "Prankster Gnome"],
        },
        {
            "name": "Goblin",
            "info": "Resourceful survivors with knack for scrap and improvisation.",
            "abilityScoreIncrease": "Dexterity +2, Constitution +1",
            "size": "Small",
            "speed": "30 feet",
            "traits": ["Darkvision", "Nimble Escape", "Fury of the Small"],
            "languages": ["Common", "Goblin"],
            "subraces": ["Boom Goblin", "Scrap Goblin", "Shadow Goblin"],
        },
        {
            "name": "Human",
            "info": "Adaptable and ambitious; the most widespread people of Aethel.",
            "abilityScoreIncrease": "All ability scores +1 OR one ability +2 and a bonus feat",
            "size": "Medium",
            "speed": "30 feet",
            "traits": ["Extra Language", "Extra Skill", "Versatility"],
            "languages": ["Common"],
            "subraces": ["Imperial Human", "Nomadic Human", "Scholarly Human"],
        },
        {
            "name": "Mycelian",
            "info": "Fungal humanoids connected to decay, renewal, and spore communion.",
            "abilityScoreIncrease": "Constitution +2, Wisdom +1",
            "size": "Medium",
            "speed": "30 feet",
            "traits": ["Fungal Body", "Spore Communication", "Decay Resistance", "Regeneration"],
            "languages": ["Common", "Mycelian"],
            "subraces": ["Spore Mycelian", "Decay Mycelian", "Symbiotic Mycelian"],
        },
        {
            "name": "Ogre",
            "info": "Large, powerful humanoids known for strength and surprising wisdom.",
            "abilityScoreIncrease": "Strength +2, Constitution +1",
            "size": "Large",
            "speed": "30 feet",
            "traits": ["Powerful Build", "Natural Armor", "Intimidating Presence"],
            "languages": ["Common", "Giant"],
            "subraces": ["Mountain Ogre", "War Ogre", "Marsh Ogre"],
        },
        {
            "name": "Orc",
            "info": "Fierce warriors with strong tribal culture and martial honor.",
            "abilityScoreIncrease": "Strength +2, Constitution +1",
            "size": "Medium",
            "speed": "30 feet",
            "traits": ["Darkvision", "Aggressive", "Powerful Build", "Relentless Endurance"],
            "languages": ["Common", "Orc"],
            "subraces": ["War Orc", "Shaman Orc", "Hunter Orc"],
        },
        {
            "name": "Troll",
            "info": "Regenerating giants with incredible resilience and survival instinct.",
            "abilityScoreIncrease": "Constitution +2, Strength +1",
            "size": "Large",
            "speed": "30 feet",
            "traits": ["Regeneration", "Powerful Build", "Natural Armor", "Keen Smell"],
            "languages": ["Common", "Giant"],
            "subraces": ["Swamp Troll", "Stone Troll", "Blood Troll"],
        },
        {
            "name": "Undead",
            "info": "Beings who retained consciousness beyond death through varied means.",
            "abilityScoreIncrease": "Constitution +2, Intelligence +1",
            "size": "Medium",
            "speed": "30 feet",
            "traits": ["Undead Nature", "Damage Resistance", "Deathless", "Darkvision"],
            "languages": ["Common"],
            "subraces": ["Lichborn", "Revenant", "Wraith"],
        },
    ]


def races_for_data_module(builder_races: list[dict]) -> list[dict]:
    out = []
    for r in builder_races:
        bonuses: dict[str, int] = {}
        asi = r["abilityScoreIncrease"]
        if "All ability" not in asi:
            for part in re.findall(r"([A-Za-z]+)\s*\+(\d+)", asi):
                bonuses[part[0].title()] = int(part[1])
        out.append(
            {
                "id": slug_id(r["name"]),
                "name": r["name"],
                "info": r["info"],
                "abilityScoreIncrease": r["abilityScoreIncrease"],
                "abilityBonuses": bonuses,
                "size": r["size"],
                "speed": r["speed"],
                "traits": r["traits"],
                "languages": r["languages"],
                "subraces": r["subraces"],
            }
        )
    return out


def write_js_module(path: str, export_name: str, data: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"/** Auto-generated canon ingest */\nexport const {export_name} = ")
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write(f";\nexport default {export_name};\n")


def main() -> None:
    os.makedirs(DATA, exist_ok=True)

    game_feats = ingest_game_feats()
    docx_feats = ingest_docx_feats()
    variants = parse_racial_variants()
    racial_feats = racial_feat_entries(variants)

    # game-data base, docx canon overrides, racial feats appended
    merged = merge_feats(game_feats, docx_feats, racial_feats)

    write_js_module(os.path.join(DATA, "feats.js"), "feats", merged)

    prestige = parse_prestige_docx()
    with open(os.path.join(DATA, "prestige-lorebook.json"), "w", encoding="utf-8") as f:
        json.dump(prestige, f, indent=2, ensure_ascii=False)

    with open(os.path.join(DATA, "racial-variants.json"), "w", encoding="utf-8") as f:
        json.dump(variants, f, indent=2, ensure_ascii=False)

    builder = builder_races_template()
    write_js_module(os.path.join(DATA, "builder-races.js"), "builderRaces", builder)
    write_js_module(os.path.join(DATA, "races.js"), "races", races_for_data_module(builder))

    caps = sum(1 for p in prestige if p.get("capstone"))
    types: dict[str, int] = {}
    for feat in merged:
        types[feat["type"]] = types.get(feat["type"], 0) + 1

    # Prestige feat references without standalone definitions
    rb_path = os.path.join(ROOT, "rulebook_output.txt")
    missing_prestige: list[str] = []
    if os.path.isfile(rb_path):
        buf = open(rb_path, "rb").read()
        rb = buf.decode("utf-16le" if buf[:2] == b"\xff\xfe" else "utf-8", errors="replace")
        refs: set[str] = set()
        merged_names = {normalize_name(f["name"]) for f in merged}
        for line in rb.splitlines():
            if "Feats:" not in line:
                continue
            for part in re.split(r",\s*", line.split("Feats:", 1)[1]):
                name = part.strip().strip("-").strip()
                if name and normalize_name(name) not in merged_names:
                    refs.add(name)
        missing_prestige = sorted(refs)

    print(
        f"feats={len(merged)} docx={len(docx_feats)} game={len(game_feats)} racial_feats={len(racial_feats)}"
    )
    print(f"feat_types={types}")
    print(f"prestige={len(prestige)} capstones={caps} racial_variants={len(variants)}")
    if missing_prestige:
        print(f"prestige_feat_refs_missing={len(missing_prestige)} (no standalone canon entry)")
    comp_path = os.path.join(ROOT, "Decennium_Descent_330_Feat_Compendium.docx")
    if os.path.isfile(comp_path) and len(docx_paragraphs(comp_path)) < 20:
        print("class_specific_feats=0 (330 compendium is a stub; 180 class feats not in repo)")


if __name__ == "__main__":
    main()
