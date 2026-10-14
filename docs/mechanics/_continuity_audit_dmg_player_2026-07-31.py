# -*- coding: utf-8 -*-
"""Continuity audit: DMG vs Player Rulebook — 2026-07-31. No commit."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DMG = ROOT / "docs/mechanics/_audit_extracts/dmg_2026-07-31.txt"
PLAYER = ROOT / "docs/mechanics/_audit_extracts/player_2026-07-31.txt"
OUT_JSON = ROOT / "docs/mechanics/_audit_extracts/audit_hits_2026-07-31.json"

LIVE_GUARDIANS = [
    "Vaskor",
    "Bloom That Hungers",
    "Ashthirst",
    "Gor Vekk",
    "Choralith",
    "Lumen of the Shattered",
    "Xarog",
    "Eirfax",
    "Threxus",
    "Marquis of Silence",
]
RETIRED_AS_GUARDIANS = [
    "Velkyrion",
    "Zeharra",
    "Kharix",
    "Hollow King",
    "Cindervore",
    "Vox Prime",
]


def load(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def find_lines(text: str, pattern: str, maxn: int = 40, flags: int = re.I):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(pattern, line, flags):
            hits.append({"line": i, "text": line.strip()[:220]})
            if len(hits) >= maxn:
                break
    return hits


def context_hits(text: str, needle_re: str, ctx_keys, exclude_re=None, maxn=30):
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        masked = re.sub(r"2400|1200", "XXXX", line)
        if not re.search(needle_re, masked, re.I):
            continue
        if exclude_re and re.search(exclude_re, line, re.I):
            continue
        ctx = " ".join(lines[max(0, i - 2) : i + 3]).lower()
        if any(k.lower() in ctx for k in ctx_keys):
            out.append({"line": i + 1, "text": line.strip()[:220]})
            if len(out) >= maxn:
                break
    return out


def run():
    dmg = load(DMG)
    player = load(PLAYER)
    report = {"dmg_chars": len(dmg), "player_chars": len(player), "checks": {}}

    # --- CLOCKS ---
    clocks = {}
    for label, text in [("dmg", dmg), ("player", player)]:
        clocks[label] = {
            "2400": find_lines(text, r"2400\s*(hours?|h\b)"),
            "1200_opening": find_lines(text, r"1200.*(hour|day\s*50)|hour\s*1200"),
            "day50": find_lines(text, r"day\s*50"),
            "stale_240_120_near_opening": context_hits(
                text,
                r"\b240\b|\b120\b",
                ["opening", "horn", "descent", "seal", "day 50", "point of no"],
                exclude_re=r"120\s*(ft|feet)|240\s*(ft|feet)|2400|1200",
            ),
            "soft_quit": find_lines(
                text,
                r"Bar of Last Refuge|Canticle|soft quit|Sanctum of Echoing|turn back",
            ),
            "horn_explicit": find_lines(text, r"\bThe Horn\b|Horn sounds|point of no return"),
        }
    report["checks"]["clocks"] = clocks

    # --- EXPEDITION ---
    exped = {}
    for label, text in [("dmg", dmg), ("player", player)]:
        exped[label] = {
            "cap12": find_lines(
                text,
                r"up to 12|12-person|12 characters|maximum of 12|max(?:imum)?\s*12|12-seat",
            ),
            "24pc": find_lines(text, r"\b24\s*(PCs?|characters|person)"),
            "coalition": find_lines(text, r"coalition|coordinat(?:e|ing)|multiple [Ee]xpeditions"),
            "five_teams": find_lines(
                text,
                r"Combat Team|Reconnaissance|Resource Team|Support Team|five (activity )?teams",
            ),
            "periods": find_lines(text, r"morning.{0,30}afternoon.{0,30}evening|three periods"),
        }
    report["checks"]["expedition"] = exped

    # --- COSMOLOGY LAYERS ---
    cosmo = {}
    for label, text in [("dmg", dmg), ("player", player)]:
        cosmo[label] = {
            "SilentOnes": find_lines(text, r"Silent Ones?"),
            "OldOnes": find_lines(text, r"\bOld Ones?\b"),
            "Heartcell": find_lines(text, r"Heartcell"),
            "Calanthir": find_lines(text, r"Calan.?thir"),
            "Asmodeus": find_lines(text, r"Asmodeus"),
            "Crucible": find_lines(text, r"\bCrucible\b|Calan.?thir.?s Trial"),
            "Ulnak": find_lines(text, r"Ul.?nak"),
            "loot_bait": find_lines(text, r"loot as bait|bait for"),
            "built_machine": find_lines(
                text, r"built the (prison|machine|Heartcell)|taught the world to call"
            ),
        }
    report["checks"]["cosmology"] = cosmo

    # --- APPENDIX B ---
    appb = {}
    for label, text in [("dmg", dmg), ("player", player)]:
        appb[label] = {
            "title_faiths": find_lines(text, r"Faiths and Cosmologies of Aethel"),
            "title_lore": find_lines(text, r"The Lore of Aethel"),
            "folk_disclaimer": find_lines(
                text,
                r"mortal (theology|belief|religious)|folk religion|not objective|not.{0,20}objective cosmic",
            ),
            "Appendix_B": find_lines(text, r"Appendix B"),
            "Fifteenfold": find_lines(text, r"Fifteenfold|fifteen-god|Primeval Pantheon"),
            "GreatWheel": find_lines(text, r"Great Wheel"),
            "BloodWar": find_lines(text, r"Blood War"),
            "worship_masks": find_lines(text, r"worship masks|masks/faces|theological abstractions"),
        }
    report["checks"]["appendix_b"] = appb

    # --- GUARDIANS ---
    guards = {}
    for label, text in [("dmg", dmg), ("player", player)]:
        live = {g: find_lines(text, re.escape(g)) for g in LIVE_GUARDIANS}
        retired = {g: find_lines(text, re.escape(g)) for g in RETIRED_AS_GUARDIANS}
        # retired used as gate guardian?
        retired_as_gate = []
        for g, hits in retired.items():
            for h in hits:
                # check nearby context in full text
                pass
        lines = text.splitlines()
        for g in RETIRED_AS_GUARDIANS:
            for i, line in enumerate(lines):
                if re.search(re.escape(g), line, re.I):
                    ctx = " ".join(lines[max(0, i - 2) : i + 3]).lower()
                    if any(
                        k in ctx
                        for k in ["gate guardian", "gate boss", "tier boss", "floor 10", "guardian"]
                    ):
                        retired_as_gate.append(
                            {"name": g, "line": i + 1, "text": line.strip()[:200], "role": "gate-context"}
                        )
        guards[label] = {
            "live_counts": {g: len(v) for g, v in live.items()},
            "live_hits": {g: v[:5] for g, v in live.items() if v},
            "retired_counts": {g: len(v) for g, v in retired.items()},
            "retired_hits": {g: v[:5] for g, v in retired.items() if v},
            "retired_as_gate_context": retired_as_gate[:20],
        }
    report["checks"]["guardians"] = guards

    # --- UMBRIN / DROW / SWTOR ---
    ip = {}
    for label, text in [("dmg", dmg), ("player", player)]:
        ip[label] = {
            "Umbrin": find_lines(text, r"\bUmbrin\b"),
            "Drow": find_lines(text, r"\bDrow\b"),
            "SWTOR": find_lines(text, r"SWTOR|Star Wars|The Old Republic|Jedi|Sith"),
            "dark_elf": find_lines(text, r"dark elves?|Dark Elf"),
        }
    report["checks"]["ip_scrub"] = ip

    # --- PLAYER SPOILERS (deep director) ---
    spoiler_pats = {
        "SilentOnes": r"Silent Ones?",
        "Heartcell": r"Heartcell",
        "loot_as_bait": r"loot as bait|treasure is bait",
        "built_prison": r"built the prison|taught the world to call it a dungeon",
        "Ul_nak_secret": r"Ul.?nak",
        "revelation_ladder": r"Custodians|Bearers|Signatories",
        "eight_actor": r"eight-actor|eight actor",
        "EV_combat": r"expected value|EV combat",
        "floor_building_engine": r"floor-building engine|rival-[Ee]xpedition",
    }
    spoilers = {k: find_lines(player, v) for k, v in spoiler_pats.items()}
    report["checks"]["player_spoilers"] = spoilers

    # --- DMG vs PLAYER shared topic snippets ---
    report["shared_snippets"] = {
        "player_opening_block": find_lines(player, r"Decennial Opening|Opening lasts|Horn sounds"),
        "dmg_opening_block": find_lines(dmg, r"Opening lasts|Horn sounds|2400-hour Opening"),
        "player_expedition_block": find_lines(
            player, r"12-Person Expedition|up to 12 characters|Expeditions in Aethel"
        ),
        "dmg_expedition_block": find_lines(
            dmg, r"12-person|up to 12|Expedition cap|multiple Expeditions"
        ),
        "player_public_myth": find_lines(
            player, r"Calan.?thir.*Asmodeus|Asmodeus.*Calan.?thir|jointly built|public myth"
        ),
        "dmg_public_secret": find_lines(
            dmg, r"public myth|Heartcell|Silent Ones|two-layer|discovered"
        ),
    }

    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print concise verdict-oriented summary
    def count_map(d):
        return {k: len(v) if isinstance(v, list) else v for k, v in d.items()}

    print("=== AUDIT SUMMARY ===")
    print(f"DMG chars={len(dmg)} PLAYER chars={len(player)}")
    print("\n-- CLOCKS --")
    for lab in ("dmg", "player"):
        c = clocks[lab]
        print(
            f"  {lab}: 2400={len(c['2400'])} 1200={len(c['1200_opening'])} day50={len(c['day50'])} "
            f"stale240/120={len(c['stale_240_120_near_opening'])} softquit={len(c['soft_quit'])}"
        )
        for h in c["stale_240_120_near_opening"][:5]:
            print(f"    STALE L{h['line']}: {h['text']}")

    print("\n-- EXPEDITION --")
    for lab in ("dmg", "player"):
        e = exped[lab]
        print(
            f"  {lab}: cap12={len(e['cap12'])} 24pc={len(e['24pc'])} coalition={len(e['coalition'])} "
            f"teams={len(e['five_teams'])} periods={len(e['periods'])}"
        )

    print("\n-- COSMOLOGY (player spoilers concern) --")
    for k, hits in cosmo["player"].items():
        if hits:
            print(f"  PLAYER {k}: {len(hits)}")
            for h in hits[:4]:
                print(f"    L{h['line']}: {h['text']}")
    print("  DMG SilentOnes=", len(cosmo["dmg"]["SilentOnes"]), "Heartcell=", len(cosmo["dmg"]["Heartcell"]))

    print("\n-- APPENDIX B --")
    for lab in ("dmg", "player"):
        a = appb[lab]
        print(
            f"  {lab}: Faiths={len(a['title_faiths'])} Lore={len(a['title_lore'])} "
            f"folk={len(a['folk_disclaimer'])} AppB={len(a['Appendix_B'])}"
        )
        for h in (a["title_faiths"] + a["title_lore"] + a["folk_disclaimer"])[:6]:
            print(f"    L{h['line']}: {h['text']}")

    print("\n-- GUARDIANS --")
    for lab in ("dmg", "player"):
        g = guards[lab]
        live_present = [n for n, c in g["live_counts"].items() if c]
        retired_present = [n for n, c in g["retired_counts"].items() if c]
        print(f"  {lab}: live={live_present} retired={retired_present}")
        print(f"    retired_as_gate={g['retired_as_gate_context'][:5]}")

    print("\n-- IP --")
    for lab in ("dmg", "player"):
        i = ip[lab]
        print(
            f"  {lab}: Umbrin={len(i['Umbrin'])} Drow={len(i['Drow'])} "
            f"SWTOR={len(i['SWTOR'])} dark_elf={len(i['dark_elf'])}"
        )
        for h in i["Drow"][:5] + i["SWTOR"][:5] + i["dark_elf"][:5]:
            print(f"    L{h['line']}: {h['text']}")

    print("\n-- PLAYER SPOILERS --")
    for k, hits in spoilers.items():
        if hits:
            print(f"  FAIL? {k}: {len(hits)}")
            for h in hits[:5]:
                print(f"    L{h['line']}: {h['text']}")

    print(f"\nWrote {OUT_JSON}")


if __name__ == "__main__":
    run()
