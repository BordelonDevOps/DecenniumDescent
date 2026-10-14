# -*- coding: utf-8 -*-
"""Build Codex of the Heartcell: guardian set-pieces + lexicon with stub flags."""
from __future__ import annotations

import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "manuals"

GUARDIANS = [
    ("Vaskor", "T1 Yieldheart / Warded Gate", "Possibility", "Automaton logic and crystal wards"),
    ("The Bloom That Hungers", "T2 Bloomdeep / Sporemist Gate", "Choice", "Spore, mire, and appetite"),
    ("Ashthirst the Hollow", "T3 Anvil of Brogi / Lavaflow Gate", "Difference", "Heat, slag, and hollow thirst"),
    ("Gor Vekk", "T4 Isles of Eternal Radiance / Radiance Gate", "Conflict", "Radiance, mirrors, sun-shard bait"),
    ("Choralith", "T5 Sanctum of Echoing Choirs / Canticle Gate", "Motion", "Sound, echo, soft quit line"),
    ("Lumen of the Shattered Thread", "T6 Crossroads / Lumen Gate", "Time", "Broken Weave-threads"),
    ("Xarog", "T7 Pactbound Arena / Furnace Gate", "History", "Oaths, bloodsport, bargains"),
    ("Eirfax", "T8 Duskshard Pools / Crown Gate", "Identity", "Twilight basins, crowns in reflection"),
    ("Threxus", "T9 Veiled Iron Spiral / Spiral Gate", "Will", "Iron helix tightening the Weave"),
    ("The Marquis of Silence", "T10 Silencebound Void / Marquis Gate", "Life", "Hush beneath the song"),
]

ECOLOGY = {
    "Aberration": "Wrong geometry where the Spiral thins. Emphasize incomprehension.",
    "Beast": "Travel pressure and harvest nodes as often as set-piece fights.",
    "Celestial": "Higher harmony stained by Pact politics — rarely simple allies.",
    "Construct": "Labor, weapons, and evidence of older engineering (Anvil bands).",
    "Dragon": "Apex ambition; hoards seed surface wars for generations.",
    "Elemental": "Terrain is half the encounter.",
    "Fey": "Adjacent-fold bargains cost more than steel.",
    "Fiend": "Chaos-Realm discord that feeds the dissonance the Pact requires.",
    "Giant": "Siege and camp-breakers; force triage choices.",
    "Humanoid": "Peoples and politics; slaughter has reputational cost.",
    "Monstrosity": "Twisted life that should not breed true — until it does.",
    "Ooze": "Punish poor watches and sealed corridors.",
    "Plant": "Bloomdeep control and attrition.",
    "Undead": "History that refuses silence.",
}


def load_monsters():
    jp = ROOT / "src" / "bestiary_data_full.json"
    data = json.loads(jp.read_text(encoding="utf-8"))
    monsters = data if isinstance(data, list) else data.get("monsters") or []
    by = {(m.get("name") or "").strip(): m for m in monsters if m.get("name")}
    wb = openpyxl.load_workbook(ROOT / "Bestiary.xlsx", read_only=True, data_only=True)
    ws = wb["Monsters"]
    rows = ws.iter_rows(values_only=True)
    header = [str(h) if h else f"c{i}" for i, h in enumerate(next(rows))]
    idx = {h: i for i, h in enumerate(header)}

    def cell(r, k, default=None):
        i = idx.get(k)
        if i is None or i >= len(r):
            return default
        return r[i] if r[i] is not None else default

    for r in rows:
        name = cell(r, "Name")
        if not name:
            continue
        name = str(name).strip()
        m = by.get(name) or {"name": name}
        by[name] = m
        for src, dst in [
            ("Size", "size"),
            ("Type", "type"),
            ("Alignment", "alignment"),
            ("Challenge", "challengeRating"),
            ("XP", "xp"),
            ("Zone Found", "zoneFound"),
            ("AC", "armorClass"),
            ("HP", "hitPoints"),
            ("Speed", "speed"),
            ("Traits", "excelTraits"),
            ("Combat Provenance", "combatProvenance"),
            ("NeedsReview", "needsReview"),
            ("Attack1 Name", "a1n"),
            ("Attack1 Bonus", "a1b"),
            ("Attack1 Damage", "a1d"),
            ("Attack1 Type", "a1t"),
            ("Attack2 Name", "a2n"),
            ("Multiattack", "multiattack"),
            ("Save DC", "saveDC"),
        ]:
            v = cell(r, src)
            if v is not None:
                m[dst] = v
    wb.close()
    return sorted(by.values(), key=lambda m: (m.get("name") or "").lower())


def stub_reason(m: dict) -> str | None:
    """Hard stubs only — do not mark every sandbox row as STUB."""
    reasons = []
    size = (m.get("size") or "").lower()
    typ = (m.get("type") or "").lower()
    name = (m.get("name") or "").lower()
    cr = m.get("challengeRating")
    try:
        cr_f = float(cr)
    except (TypeError, ValueError):
        cr_f = None
    if size == "tiny" and typ == "undead" and cr_f == 0:
        reasons.append("Tiny Undead CR 0 band mismatch")
    if typ == "undead" and any(x in name for x in ("aarakocra", "abjurer")):
        reasons.append("type mismatch vs name")
    if m.get("needsReview") in (True, "Y", "y", "yes", "TRUE", 1):
        reasons.append("NeedsReview")
    # Note provisional attacks without forcing STUB banner on every row
    return "; ".join(reasons) if reasons else None


def guardian_chapter(name, where, principle, terrain) -> str:
    return f"""
## Gate Seal — {name}

**Seat:** {where}  
**Principle pressure:** {principle}  
**Terrain tell:** {terrain}

### Staging
Treat {name} as a **tier seal**, not a random boss. Telegraph the principle for a full period before the fight: omens, lesser encounters, research clues, and a clear retreat cost.

### Lair and omens
- Approach hazard tied to {terrain}
- A false bargain or false map offered by a rival or floor civ
- One research object that only makes sense after the seal

### Tactics (Director)
Open with terrain denial, punish clustered Combat teams, and force Support/Research off-map work so the fight is not the only story. If using provisional Excel numbers, announce draft status.

### Bait and aftermath
Victory should spill **loot that seeds surface conflict** and reactivate seal machinery in fiction. Defeat should cost Opening hours and morale — not a TPK by default unless the table chose deadly stakes.

### DIRECTOR ONLY
Seal victories feed the Heartcell's public Crucible face. Do not narrate Silent Ones by name; let Custodian/Signatory language appear in residual records if the party has earned that rung.
"""


def main():
    monsters = load_monsters()
    parts: list[str] = []
    parts.append(
        """# Codex of the Heartcell
## BB-01 — Monster Ecology, Gate Seals, and Lexicon

*Director bestiary. Aligned to Player Rulebook and The Director's Crucible. 2026-07-30.*

**Book code:** BB-01  
**Editable stats source:** `Bestiary.xlsx` (re-ingest after edits)

---

# Part I — How to Use This Codex

## Reading a Decennium Stat Line

| Field | Meaning |
|-------|---------|
| Size / Type / Alignment | Fiction tags; distrust nonsense combos |
| Challenge / XP | Budget aids; XP awards may be draft |
| Zone | Where the Excel ingest places them |
| Armor / HP / Speed | Combat shell |
| Attacks | Prefer Excel names; flag provisional sandbox verbs |
| Traits / Provenance | Honesty layer — draft means say so |

**STUB** means: do not treat as finished lore; reskin before a showcase fight.

## Gate Seal Rules (Director)

1. One guardian per Gate division unless story splits the seal.
2. Soft quit line at Canticle (~Floor 50) is **morale**, not horn PoNR (day 50 / 1200 h).
3. Legendary-feeling turns: lair actions as terrain pulses, not foreign product jargon — call them **Seal Pulses**.
4. Live roster only (see Part II).

---

# Part II — Ten Gate Seals
"""
    )
    for g in GUARDIANS:
        parts.append(guardian_chapter(*g))

    parts.append("\n# Part III — Ecologies of Aethel\n")
    for typ, blurb in ECOLOGY.items():
        count = sum(1 for m in monsters if (m.get("type") or "").lower() == typ.lower())
        parts.append(f"\n## The {typ}\n\n{blurb}\n\nIndexed count: **{count}**.\n")
        parts.append(
            f"**Player knowledge:** rumors and hunter talk.\n"
            f"**Director knowledge:** how this type feeds dissonance or bait circulation.\n"
        )

    parts.append(
        """
# Part IV — DIY Monster (Quick)

1. Role: bruiser / skirmisher / controller / artillery / leader  
2. Tier terrain tag  
3. One tell (sound, heat, spore, bargains…)  
4. Numbers from nearest Excel CR band — mark provisional  
5. Drop that creates surface trouble  

# Part V — Tier Random Pressure (Seeds)

| Tier | d6 pressure |
|------|-------------|
| 1 | Automaton patrol / ward surge / salvage claim fight |
| 2 | Spore timer / mire swallow / false reed signal |
| 3 | Slag rain / swinging anvil window / heat exhaustion |
| 4 | Mirror double / light-sprite theft / sun-shield failure |
| 5 | Echo replay / silence pocket / soft-quit despair event |
| 6–10 | Rumor only — invent from Chronicle stubs |

---

# Part VI — Creature Lexicon (A–Z)

Entries marked **STUB** require Director reskin before showcase use.
"""
    )

    stub_n = 0
    audit_worst: list[str] = []
    for m in monsters:
        name = m.get("name") or "Unknown"
        stub = stub_reason(m)
        if stub:
            stub_n += 1
            if len(audit_worst) < 50:
                audit_worst.append(f"{name}: {stub}")
        meta = (
            f"{m.get('size') or '?'} {m.get('type') or '?'}, "
            f"{m.get('alignment') or 'unaligned'}; "
            f"CR {m.get('challengeRating') if m.get('challengeRating') is not None else '?'}"
            f" ({m.get('xp') if m.get('xp') is not None else '?'} XP); "
            f"Zone: {m.get('zoneFound') or 'unknown'}."
        )
        typ = (m.get("type") or "Monstrosity").title()
        eco = ECOLOGY.get(typ, ECOLOGY.get(typ.rstrip("s"), "Heartcell pressure fauna."))
        zone = m.get("zoneFound") or "the depths"
        lore = (
            f"Found about {zone}. {eco} "
            f"Decide patrol vs nest vs harvest node before rolling initiative."
        )
        if name in {g[0] for g in GUARDIANS}:
            lore = f"**GATE SEAL ENTITY** — see Part II. {lore}"
        block = [f"\n### {name}\n", meta + "\n", lore + "\n"]
        if stub:
            block.append(f"**STUB:** {stub}\n")
        block.append(
            f"Armor {m.get('armorClass') if m.get('armorClass') is not None else '—'}; "
            f"HP {m.get('hitPoints') if m.get('hitPoints') is not None else '—'}; "
            f"Speed {m.get('speed') if m.get('speed') is not None else '—'}.\n"
        )
        if m.get("a1n"):
            line = (
                f"- Attack: {m.get('a1n')} "
                f"(+{m.get('a1b') if m.get('a1b') is not None else '?'}, "
                f"{m.get('a1d') or '?'} {m.get('a1t') or ''})"
            )
            if str(m.get("a1n")) in (
                "Freak Bite",
                "Monstrous Claw",
                "Aberrant Lash",
                "Grave Shriek",
            ):
                line += " *(provisional sandbox name)*"
            block.append(line + "\n")
        if m.get("a2n"):
            block.append(f"- Attack II: {m.get('a2n')}\n")
        if m.get("multiattack"):
            block.append(f"- Multiattack: {m.get('multiattack')}\n")
        if m.get("excelTraits"):
            block.append(f"- Traits: {m.get('excelTraits')}\n")
        parts.extend(block)

    # numeric CR index
    parts.append("\n# Appendix — Index by Challenge (numeric)\n")
    by_cr: dict[float | str, list[str]] = {}
    for m in monsters:
        cr = m.get("challengeRating")
        try:
            key: float | str = float(cr)
        except (TypeError, ValueError):
            key = str(cr) if cr is not None else "?"
        by_cr.setdefault(key, []).append(m.get("name") or "?")

    def sort_key(k):
        return (0, k) if isinstance(k, float) else (1, str(k))

    for cr in sorted(by_cr.keys(), key=sort_key):
        names = ", ".join(by_cr[cr][:60])
        extra = f" (+{len(by_cr[cr]) - 60} more)" if len(by_cr[cr]) > 60 else ""
        parts.append(f"\n## Challenge {cr}\n\n{names}{extra}\n")

    text = "".join(parts)
    path = OUT / "Codex_of_the_Heartcell.md"
    path.write_text(text, encoding="utf-8")

    audit = OUT / "CODEX_QUALITY_AUDIT.md"
    audit.write_text(
        "# Codex quality audit\n\n"
        f"- Monsters indexed: **{len(monsters)}**\n"
        f"- Stub-flagged: **{stub_n}**\n"
        f"- Gate chapters: **{len(GUARDIANS)}/10**\n\n"
        "## Top stub problems (sample)\n\n"
        + "\n".join(f"- {x}" for x in audit_worst)
        + "\n",
        encoding="utf-8",
    )
    print("Codex words", len(text.split()), "stubs", stub_n, "monsters", len(monsters))


if __name__ == "__main__":
    main()
