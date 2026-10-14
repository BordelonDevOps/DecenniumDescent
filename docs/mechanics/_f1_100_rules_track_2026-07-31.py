"""F1–100 / T6–10 Rules & Director deep-tier track (2026-07-31).

- Extends Opening milestone awards through Tiers 6–10 (no CR→XP).
- Inserts clearly marked OPEN Level 97 Old God (Q6) placeholder — does not invent.
- Adds Deep Opening Director stance pointer (ops already in Ch 63–68 / Ch 57).
- Mirrors player-facing milestone wording to full Opening (public-safe).
Backup before edits. No commit.
"""
from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[2]
DIRECTOR = ROOT / "docs" / "manuals" / "The_Directors_Crucible_Complete_Director_Edition.docx"
PLAYER = ROOT / "decennium descent player rulebook.docx"
BACKUP_DIR = ROOT / "backups"


def set_text(paragraph, text: str) -> None:
    if paragraph.runs:
        paragraph.runs[0].text = text
        for r in paragraph.runs[1:]:
            r.text = ""
    else:
        paragraph.add_run(text)


def find_prefix(doc: Document, prefix: str):
    for p in doc.paragraphs:
        if (p.text or "").strip().startswith(prefix):
            return p
    raise SystemExit(f"MISSING prefix: {prefix!r}")


def find_exact(doc: Document, text: str):
    for p in doc.paragraphs:
        if (p.text or "").strip() == text:
            return p
    raise SystemExit(f"MISSING exact: {text!r}")


def insert_paragraph_after(paragraph, text: str = "") -> Paragraph:
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    if text:
        new_para.add_run(text)
    return new_para


def backup(path: Path, stamp: str, label: str) -> Path:
    BACKUP_DIR.mkdir(exist_ok=True)
    dest = BACKUP_DIR / f"{label}_{stamp}{path.suffix}"
    shutil.copy2(path, dest)
    print("BACKUP", dest)
    return dest


def patch_director(stamp: str) -> list[str]:
    backup(DIRECTOR, stamp, "Complete_Director_Edition_pre_f1_100_rules")
    doc = Document(str(DIRECTOR))
    edits: list[str] = []

    # --- Milestone awards: T1–10 / Floors 1–100 ---
    awards = find_prefix(doc, "Treasure and awards. The cumulative level 1–20 XP thresholds")
    set_text(
        awards,
        "Treasure and awards. The cumulative level 1–20 XP thresholds in the Player "
        "Rulebook are canon for level and proficiency when XP tracking is in force. "
        "For Opening campaigns across the full Decennial Opening (Tiers 1–10 / Floors "
        "1–100, including deep push past the Canticle Gate), milestone advancement is "
        "official: award levels at Gate seals (Warded through Marquis), major arc beats, "
        "the Old God Interstice crossing when used, or other milestones announced before "
        "the Opening begins. Depth does not unlock a CR→XP economy — no published "
        "CR→XP or encounter-budget table exists in this book or the Player Rulebook. "
        "Companion Session CR→XP helpers remain optional and non-canon — label them "
        "playtest if used; they do not write to character saves. Outside Opening scope, "
        "specific encounter awards remain Director judgment unless a published adventure "
        "provides them.",
    )
    edits.append("awards-t6-10")

    always_xp = find_prefix(doc, "Label provisional combat statistics and any optional CR→XP")
    set_text(
        always_xp,
        "Label provisional combat statistics and any optional CR→XP companion helpers "
        "as playtest / non-canon. Opening campaigns (Tiers 1–10 / Floors 1–100) use "
        "milestone advancement as official; do not present Session draft XP as rulebook "
        "awards, and do not invent CR→XP to “catch up” deep-tier parties.",
    )
    edits.append("always-xp-t6-10")

    # --- Deep Opening stance after Part IX intro ---
    part_ix = find_prefix(
        doc,
        "The Tier Gazetteer names the dominant image, key locations, and canonical Guardian",
    )
    # Insert in reverse so final order reads stance heading → body → blank
    insert_paragraph_after(
        part_ix,
        "After the Horn (hour 1200 / day 50), treat extraction reliability, rescue "
        "contracts, and ally commitment as visibly thinning even if the party is still "
        "on early floors — the Horn is a calendar event, not a Floor-50 trigger. Soft "
        "quit at the Bar of Last Refuge / Canticle Gate remains a cultural threshold "
        "and is never equated with the Horn. Past Canticle, run Tier 6 as the last "
        "normal civilization depth, then Tiers 7–10 as controlled mystery (maps decay, "
        "supply fails, testimony fragments). Stage the seal ladder in order: Lumen → "
        "Xarog → (optional Interstice) → Eirfax → Threxus → Marquis. Endgame options "
        "are extraction, entrapment at seal, Gate or Marquis victory, transformation, "
        "or deliberate remain — see Chapter 57. Do not invent a Floor-97 room to fill "
        "Level 97 myth; that seam is OPEN (Q6) below Chapter 34.",
    )
    insert_paragraph_after(part_ix, "Deep Opening Director Stance (Tiers 6–10 / Floors 51–100)")
    edits.append("deep-opening-stance")

    # --- Q6 OPEN placeholder after Ch 34 Crossing Consequences ---
    crossing = find_prefix(doc, "Each character should leave with one personal consequence.")
    # Insert newest-first so reading order is heading → body → note
    insert_paragraph_after(
        crossing,
        "Continuity note: companion stamp docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md "
        "mirrors this placeholder. Owner lock J / READY_TO_CONTINUE.md.",
    )
    insert_paragraph_after(
        crossing,
        "What is published and playable here is the Old God Interstice between Tiers 7 "
        "and 8 (this chapter; Chapter 65). What remains unanswered is whether a distinct "
        "Floor-97 chamber is ever authored, and whether the Level 97 imprisoning myth "
        "relates to Silent Ones / Old Ones / Heartcell. Until the owner answers: (1) do "
        "not equate Level 97 with the Interstice; (2) do not invent that relationship; "
        "(3) treat World-of-Aethel Level 97 prose as myth-history flavor, not an "
        "encounter index; (4) if players reach Floors 91–100, stage Marquis / Void "
        "content from Chapters 10 and 68 without forcing a Level-97 set piece.",
    )
    insert_paragraph_after(
        crossing,
        "OPEN PLACEHOLDER — Level 97 Old God (Q6). Owner asked 2026-07-30; explicitly "
        "unanswered. World of Aethel myth-history (Binding of the Old God, 666 AE) says "
        "an eleventh unnamed shard was imprisoned at Level 97 of the Great Descent and "
        "contact was forbidden. That sentence is lore residue — not a published floor "
        "card, not a Gate Guardian, and not automatically this Interstice.",
    )
    insert_paragraph_after(
        crossing,
        "OPEN — Level 97 Old God (Q6) — do not invent",
    )
    edits.append("q6-placeholder")

    # --- Canon Guardrails: Q6 line after Interstice guardrail ---
    interstice_guard = find_exact(
        doc,
        "The Old God Interstice lies between Tiers 7 and 8 and is not another tier.",
    )
    insert_paragraph_after(
        interstice_guard,
        "OPEN (Q6): Level 97 Old God myth from World of Aethel is unanswered — do not "
        "equate it with the Interstice or Silent Ones / Heartcell without owner lock.",
    )
    edits.append("guardrails-q6")

    doc.save(str(DIRECTOR))
    print("SAVED", DIRECTOR)
    return edits


def patch_player(stamp: str) -> list[str]:
    backup(PLAYER, stamp, "decennium_descent_player_rulebook_pre_f1_100_rules")
    doc = Document(str(PLAYER))
    edits: list[str] = []

    mile = find_prefix(doc, "For Opening campaigns (Tier 1–5 play through a Decennial Opening)")
    set_text(
        mile,
        "For Opening campaigns (the full Decennial Opening — including Expeditions that "
        "push past the Bar of Last Refuge and continue toward deeper Gates), milestone "
        "advancement is the official method: the Director awards a level when the "
        "Expedition hits a Gate seal, completes a major arc beat, or reaches another "
        "announced milestone. Tell the table which milestones grant levels before the "
        "Opening begins. Deeper floors do not change this method.",
    )
    edits.append("player-milestones-full-opening")

    # Keep CR→XP denial language aligned (still no CR→XP)
    xp_note = find_prefix(doc, "The Character Advancement table remains canon for total character level")
    set_text(
        xp_note,
        "The Character Advancement table remains canon for total character level, "
        "proficiency bonus, and for tables that opt into XP tracking. This book does "
        "not publish creature or encounter XP awards at any depth. Any companion Session "
        "CR→XP helper is optional and non-canon — it never replaces Director milestones "
        "for Opening campaigns and does not write XP to your character sheet automatically.",
    )
    edits.append("player-no-crxp")

    doc.save(str(PLAYER))
    print("SAVED", PLAYER)
    return edits


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    d_edits = patch_director(stamp)
    p_edits = patch_player(stamp)
    print("EDITS_DIRECTOR", d_edits)
    print("EDITS_PLAYER", p_edits)


if __name__ == "__main__":
    main()
