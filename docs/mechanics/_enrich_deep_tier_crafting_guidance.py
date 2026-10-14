#!/usr/bin/env python3
"""Idempotent: attach directorGuidance to needsReview crafting recipes. Does not empty components."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "src" / "data" / "crafting-recipes.json"

GUIDE = {
    "skill_11_plus_deep_tier_provisional": (
        "Deep-tier provisional (skill 11+ → dungeon tier 6–10). Components are real costs — do not treat as free craft. "
        "Director: (1) require components as listed or 1:1 Instruments salvage swap; (2) gate availability behind Floor/tier "
        "access or a named haven workshop; (3) if the result feels too strong for current floor, add downtime hours "
        "(skillLevel × 2 hours suggested) or a rare catalyst from the current Gate zone; (4) never invent Heartcell/Silent Ones parts."
    ),
    "legendary_or_mythic_provisional": (
        "Legendary/Mythic quality — provisional balance. Components are real costs — do not empty or waive casually. "
        "Director: (1) treat as campaign-defining rewards (Gate seal, research breakthrough, or named NPC commission); "
        "(2) require full listed components or Instruments tier salvage of equal or higher tier; "
        "(3) optional: add a Resonance ritual (1 long rest + Weave check DC 15 + skillLevel) before completion; "
        "(4) keep Heartcell/Silent Ones names out of the public craft ledger."
    ),
}


def main() -> None:
    recipes = json.loads(PATH.read_text(encoding="utf-8"))
    changed = 0
    for r in recipes:
        if not r.get("needsReview"):
            if "directorGuidance" in r:
                del r["directorGuidance"]
                changed += 1
            continue
        reason = r.get("needsReviewReason") or ""
        guide = GUIDE.get(reason)
        if guide and r.get("directorGuidance") != guide:
            r["directorGuidance"] = guide
            changed += 1
        if r.get("needsReview") and r.get("status") != "needsReview":
            r["status"] = "needsReview"
            changed += 1
    PATH.write_text(json.dumps(recipes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nr = sum(1 for r in recipes if r.get("needsReview"))
    empty = sum(1 for r in recipes if not r.get("components"))
    print(f"ok recipes={len(recipes)} needsReview={nr} empty_components={empty} field_updates={changed}")


if __name__ == "__main__":
    main()
