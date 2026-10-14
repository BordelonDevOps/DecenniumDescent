"""One-shot ingest: rulebook extracts -> src/data JSON."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_prestige(rb: str) -> list:
    idx = rb.find("1. Battlemage")
    end = rb.find("# Chapter 7: Using Ability Scores")
    block = rb[idx:end]
    entries = re.split(r"\n(?=\d+\. [A-Z])", block)
    prestige = []
    for entry in entries:
        m = re.match(r"(\d+)\. ([^\n]+)", entry)
        if not m:
            continue
        num, name = int(m.group(1)), m.group(2).strip()
        if num > 18:
            continue

        def grab(label: str, text: str) -> str:
            pat = rf"\*\*{re.escape(label)}\*\*:?\s*(.+?)(?=\*\*[A-Z]|\n\d+\. |\Z)"
            g = re.search(pat, text, re.S)
            return re.sub(r"\s+", " ", g.group(1).strip()) if g else ""

        cap_m = re.search(
            r"\*\*Capstone[^*]*\*\*:?\s*(.+?)(?=\*\*Combat Role|\nCharacter Story|\Z)",
            entry,
            re.S,
        )
        capstone = re.sub(r"\s+", " ", cap_m.group(1).strip()) if cap_m else ""

        sig_m = re.search(
            r"\*\*Signature Mechanics\*\*:(.+?)(?=\*\*Capstone|\Z)", entry, re.S
        )
        hallmarks = []
        if sig_m:
            for line in sig_m.group(1).split("\n"):
                line = line.strip().lstrip("- ")
                if line and not line.startswith("**Overview"):
                    hallmarks.append(re.sub(r"\*\*", "", line))

        bm = re.search(r"Base Class:\s*([^\n]+)", entry)
        role_m = re.search(
            r"\*\*Combat Role\*\*:?\s*(.+?)(?=\nCharacter Story|\Z)", entry, re.S
        )
        combat_role = re.sub(r"\s+", " ", role_m.group(1).strip()) if role_m else ""
        combat_role = combat_role.split("Character Story")[0].strip()

        prestige.append(
            {
                "num": num,
                "name": name,
                "baseClass": bm.group(1).strip() if bm else "",
                "summary": grab("Overview", entry),
                "requirements": grab("Requirements", entry),
                "unlock": grab("Unlock", entry),
                "entrance": grab("Unlock", entry) or grab("Requirements", entry)[:160],
                "hallmarks": hallmarks[:6],
                "capstone": capstone,
                "combatRole": combat_role or grab("Combat Role", entry),
            }
        )
    return prestige


def parse_world_sections(world: str) -> list:
    sections = []
    for m in re.finditer(
        r"### (VII\.[^\n]+|VIII\.[^\n]+|IX\.[^\n]+|X\.[^\n]+|XI\.[^\n]+|XII\.[^\n]+|XIII\.[^\n]+|XIV\.[^\n]+|XV\.[^\n]+)\n([\s\S]*?)(?=### |\Z)",
        world,
    ):
        title = m.group(1).strip()
        body = m.group(2).strip()
        bullets = [b.strip().lstrip("- ") for b in re.findall(r"^- .+", body, re.M)]
        subsections = [sm.group(1).strip() for sm in re.finditer(r"^  - (.+)", body, re.M)]
        sections.append(
            {
                "id": title.split(".")[0].strip(),
                "title": title,
                "bullets": bullets,
                "subsections": subsections,
            }
        )
    return sections


def main() -> None:
    rulebook_path = os.path.join(ROOT, "rulebook_output.txt")
    with open(rulebook_path, "rb") as f:
        raw = f.read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        rb = raw.decode("utf-16", errors="replace")
    else:
        rb = raw.decode("utf-8", errors="replace")

    prestige = parse_prestige(rb)
    with open(
        os.path.join(ROOT, "src", "data", "prestige-lorebook.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(prestige, f, indent=2, ensure_ascii=False)

    with open(
        os.path.join(ROOT, "The_World_of_Aethel_Lore_EXTRACT.txt"),
        encoding="utf-8",
        errors="replace",
    ) as f:
        world = f.read()
    sections = parse_world_sections(world)

    with open(
        os.path.join(ROOT, "The_Cosmology_of_Decennium_Descent_EXTRACT.txt"),
        encoding="utf-8",
        errors="replace",
    ) as f:
        cos = f.read()
    first_song_full = cos.split("Chapter II")[0].strip()
    first_song_excerpt = first_song_full[:2400] + (
        "…" if len(first_song_full) > 2400 else ""
    )

    with open(
        os.path.join(ROOT, "src", "data", "cosmology-lore.json"), encoding="utf-8"
    ) as f:
        cos_json = json.load(f)

    cos_json["source"] = (
        "The Cosmology of Decennium Descent.docx + The World of Aethel Lore.docx "
        "(player rulebook canon)"
    )
    cos_json["firstSong"] = first_song_excerpt
    cos_json["firstSongChapters"] = re.findall(
        r"Chapter [IVXLC\d]+:?[^\n]*", cos
    )[:12]
    cos_json["worldSections"] = sections
    cos_json["worldOutline"] = "\n".join(
        f"### {s['title']}\n" + "\n".join(f"- {b}" for b in s["bullets"])
        for s in sections
    )

    with open(
        os.path.join(ROOT, "src", "data", "cosmology-lore.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(cos_json, f, indent=2, ensure_ascii=False)

    cycle = next((s for s in sections if s["id"] == "XII"), None)
    myth = next((s for s in sections if s["id"] == "VII"), None)
    bestiary = next((s for s in sections if s["id"] == "XIV"), None)
    appendix = next((s for s in sections if s["id"] == "XV"), None)

    dungeon = {
        "source": "decennium descent player rulebook.docx + The World of Aethel Lore.docx",
        "hornRule": (
            "At 1200 hours (day 50 of the 2400-hour Opening), a giant horn sounds throughout the Decennium — "
            "the point of no return. Adventurers must retreat or risk being trapped in the depths for 10 years "
            "until the next Cycle. Soft quit at Floor 50 Canticle is separate from the Horn."
        ),
        "cycle": {
            "calendar": (
                "400-day year, 10 months of 40 days; Holyday on the 10th of each month; "
                "final 10 days = Twilight Week when divine and mortal boundaries blur."
            ),
            "rotation": (
                "10-year rotation — the Shardspire activates in the tenth year. "
                "Cycles are named after their victor."
            ),
            "entryClasses": cycle["bullets"][1:5] if cycle else [],
            "victoryConsequences": (
                cycle["bullets"][4] if cycle and len(cycle["bullets"]) > 4 else ""
            ),
            "mythHistory": myth["bullets"] if myth else [],
        },
        "expedition": {
            "maxSize": 12,
            "summary": (
                "Expeditions distribute up to 12 characters across combat, reconnaissance, "
                "research, resource, and support activities — not every member delves at once."
            ),
            "teams": [
                {
                    "name": "Combat Team",
                    "size": "4–6",
                    "function": "Battles, dungeon delving, immediate threats",
                },
                {
                    "name": "Reconnaissance",
                    "size": "1–3",
                    "function": "Scouting, mapping, intelligence",
                },
                {
                    "name": "Research",
                    "size": "1–3",
                    "function": "Artifacts, lore, identification",
                },
                {
                    "name": "Resource",
                    "size": "2–4",
                    "function": "Hunting, gathering, crafting",
                },
                {
                    "name": "Support",
                    "size": "1–3",
                    "function": "Camp, healing, equipment maintenance",
                },
            ],
            "timePeriods": ["morning", "afternoon", "evening"],
        },
        "gateBosses": [
            b for b in (bestiary["bullets"] if bestiary else []) if b.startswith("Lv")
        ],
        "timeline": appendix["subsections"] if appendix else [],
        "prestigeUnlock": {
            "prerequisitePath": (
                "Minimum base-class level, feats, skills, and a unique unlock event."
            ),
            "discoveryPath": (
                "Narrative discovery via location, NPC, ritual, or thematic quest chain."
            ),
        },
    }
    with open(
        os.path.join(ROOT, "src", "data", "dungeon-mechanics.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(dungeon, f, indent=2, ensure_ascii=False)

    print(f"prestige={len(prestige)} sections={len(sections)}")


if __name__ == "__main__":
    main()
