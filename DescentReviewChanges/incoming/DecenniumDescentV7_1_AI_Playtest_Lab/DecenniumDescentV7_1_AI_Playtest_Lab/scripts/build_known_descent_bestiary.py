from __future__ import annotations

import json
import re
from pathlib import Path


def find_source_root(start: Path) -> Path:
    candidates = []
    for parent in [start, *start.parents]:
        candidates.append(parent / "docs" / "bestiary" / "Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack" / "Monster_Manual_of_the_Known_Descent_Source")
        candidates.append(parent / ".." / ".." / "docs" / "bestiary" / "Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack" / "Monster_Manual_of_the_Known_Descent_Source")
    for candidate in candidates:
        candidate = candidate.resolve()
        if (candidate / "entries").is_dir():
            return candidate
    raise FileNotFoundError("Known Descent source pack not found")


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1).strip() if match else ""


def field(text: str, label: str, default: str = "") -> str:
    match = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$", text, re.M)
    return match.group(1).strip() if match else default


def int_field(text: str, label: str) -> int | None:
    value = field(text, label)
    match = re.search(r"-?\d+", value)
    return int(match.group()) if match else None


def clean_md(value: str) -> str:
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"\*(.*?)\*", r"\1", value)
    value = re.sub(r"`(.*?)`", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def parse_stat_header(block: str):
    match = re.search(r"^\*\*(.+?),\s*([^*]+)\*\*\s*$", block, re.M)
    if not match:
        return "Medium", "Unknown", "Unaligned"
    first, alignment = match.groups()
    parts = first.split(maxsplit=1)
    if len(parts) == 1:
        return parts[0], "Unknown", alignment.strip()
    return parts[0], parts[1], alignment.strip()


def parse_abilities(block: str):
    rows = re.findall(r"\|\s*(-?\d+)\s*\([^)]+\)\s*", block)
    if len(rows) >= 6:
        nums = [int(x) for x in rows[:6]]
        return dict(zip(["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"], nums))
    return None


def parse_actions(block: str):
    actions = []
    action_part = block.split("### Actions", 1)[1] if "### Actions" in block else ""
    for name, body in re.findall(r"^\*\*([^*]+)\.\*\*\s*(.*?)(?=^\*\*[^*]+\.\*\*|^## |\Z)", action_part, re.M | re.S):
        actions.append({"name": clean_md(name), "text": clean_md(body)})
    return actions


def parse_traits(block: str):
    traits = []
    if "### Traits" not in block:
        return traits
    trait_part = block.split("### Traits", 1)[1].split("### Actions", 1)[0]
    for name, body in re.findall(r"^\*\*([^*]+)\.\*\*\s*(.*?)(?=^\*\*[^*]+\.\*\*|\Z)", trait_part, re.M | re.S):
        traits.append({"name": clean_md(name), "text": clean_md(body)})
    return traits


def parse_loot(block: str):
    loot = {}
    for line in block.splitlines():
        if not line.startswith("|") or "---" in line or "Component" in line:
            continue
        cells = [clean_md(x) for x in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0]:
            continue
        detail = cells[2]
        parts = [part.strip() for part in detail.split(",", 1)]
        rate = parts[0] if parts else "Director-set"
        value = parts[1] if len(parts) > 1 else "Director-set"
        loot[f"drop{len(loot)+1}"] = {"drop": cells[0], "rate": rate, "value": value, "tier": cells[1]}
    return loot


def parse_knowledge_table(block: str):
    rows = []
    for line in block.splitlines():
        if not line.startswith("|") or "---" in line or "Result" in line:
            continue
        cells = [clean_md(x) for x in line.strip().strip("|").split("|")]
        if len(cells) >= 2:
            rows.append({"result": cells[0], "information": cells[1]})
    return rows


def parse_entry(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    name_match = re.search(r"^#\s+(.+)$", text, re.M)
    if not name_match:
        raise ValueError(f"No H1 in {path}")
    name = name_match.group(1).strip()
    stat = section(text, "Stat Block")
    size, creature_type, alignment = parse_stat_header(stat)

    challenge_match = re.search(r"\*\*Challenge\*\*\s*([^\s(]+)\s*\((\d+)\s+XP", stat)
    challenge_rating = challenge_match.group(1) if challenge_match else "—"
    xp = int(challenge_match.group(2)) if challenge_match else 0
    armor_match = re.search(r"\*\*Armor\*\*\s*(\d+)", stat)
    hp_match = re.search(r"\*\*Hit Points\*\*\s*(\d+)", stat)
    speed_match = re.search(r"\*\*Speed\*\*\s*([^\n]+)", stat)
    floors_match = re.search(r"\*\*Floors\*\*\s*([^\n]+)", stat)
    tier_match = re.search(r"\*\*Dungeon Range\*\*\s*([^·\n]+)", stat)

    what = section(text, "What It Is")
    tactics = section(text, "How It Fights")
    defeat = section(text, "How to Defeat It")
    habitat = section(text, "Habitat, Goals, and Lair")
    treasure = section(text, "Treasure and Harvest")
    knowledge = section(text, "Creature Knowledge")
    variants = section(text, "Variants and Encounter Use")
    notices = section(text, "What Experienced Expeditions Notice")

    tags = [field(text, "Family"), field(text, "Encounter role"), field(text, "Knowledge status")]
    tags = [x for x in tags if x]

    aliases = []
    if name == "Fracture-Kin Fleshwright":
        aliases.append("Fracture-Kin Sibriex")
    elif name == "Fracture-Kin Nightreaver":
        aliases.append("Fracture-Kin Nabassu")

    result = {
        "id": path.stem,
        "name": name,
        "size": size,
        "type": creature_type,
        "challengeRating": challenge_rating,
        "xp": xp,
        "alignment": alignment,
        "zoneFound": field(text, "Dungeon range", tier_match.group(1).strip() if tier_match else "Known Descent"),
        "armorClass": int(armor_match.group(1)) if armor_match else None,
        "hitPoints": int(hp_match.group(1)) if hp_match else None,
        "speed": speed_match.group(1).strip() if speed_match else "—",
        "abilities": parse_abilities(stat),
        "skills": field(stat, "Skills", "—"),
        "senses": field(stat, "Senses", "—"),
        "languages": field(stat, "Languages", "—"),
        "description": clean_md(what),
        "tags": tags,
        "loot": parse_loot(treasure),
        "ingestSource": str(path.as_posix()),
        "publicationClassification": field(text, "Publication classification", "Public"),
        "knowledgeStatus": field(text, "Knowledge status"),
        "primarySource": field(text, "Primary source"),
        "reliability": field(text, "Reliability"),
        "confirmedRange": field(text, "Confirmed range", floors_match.group(1).strip() if floors_match else ""),
        "rumoredRange": field(text, "Rumored range"),
        "encounterRole": field(text, "Encounter role"),
        "experiencedSigns": clean_md(notices),
        "knowledge": parse_knowledge_table(knowledge),
        "traits": parse_traits(stat),
        "actions": parse_actions(stat),
        "tactics": clean_md(tactics),
        "howToDefeat": clean_md(defeat),
        "habitat": clean_md(habitat),
        "harvest": clean_md(treasure),
        "variants": clean_md(variants),
    }
    if aliases:
        result["compatibilityAliases"] = aliases
    return result


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    source = find_source_root(project)
    entries = [parse_entry(path) for path in sorted((source / "entries").glob("*.md"))]
    output = project / "src" / "bestiary_data_full.json"
    output.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} public dossiers to {output}")


if __name__ == "__main__":
    main()
