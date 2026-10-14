# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "docs" / "manuals" / "The_Directors_Crucible.md"
extra = r"""

---

# Part VI — Expanded Procedures (Gap Fill)

## Adventure Blueprint (One Page)

1. **Want:** What the Expedition thinks it wants (vial, map, rescue, glory).
2. **Cost:** Opening hours, reputation, or a truth they are not ready for.
3. **Opposition:** Surface face + depth face.
4. **Terrain:** One tier tag that changes every fight.
5. **Bait:** One object that causes trouble on return.
6. **Exit:** Extraction plan before day 50 if they are not seal-runners.

Run this blueprint every time someone says they will go deeper.

## NPC Workshop

Ask four questions: What do they sell? What do they fear becoming? Who do they pray to (Fifteenfold mask)? What dungeon object would ruin them?

Then assign a leverage die (d4 soft rumor to d12 hard threat) for when the party ignores them.

## Encounter Budget Sheet

- Party: level band, Combat seat count, healer present Y/N
- Foe HP total / Party DPR = expected rounds
- Foe DPR times rounds = expected incoming
- Healing per round estimate
- Terrain tax (heat, spore, echo): add one step on the hard band
- Escape route known? If no, reduce deadly to hard unless players chose it

## Treasure as Bait — Workshop

For each major drop write: When this reaches the surface, who will try to take it, and why?

If you cannot finish that sentence, the drop is flavor only — upgrade it.

## Faction Turn (Between Delve)

Once per returned expedition, each watched faction does one: recruit, denounce, buy, raid, research, or wait. Track three factions max or you will drown.

## Vertical Map Checklist

- Muster node
- Teaching fight
- Logistics tax
- Mid-tier haven
- Soft quit temptation
- Seal approach omens
- Seal
- Extraction route

## Adjudication Extras

**Chases:** pick a clock (3–5 ticks). Each fail advances environmental doom (collapse, spore, heat). Success spends a period or a resource.

**Siege:** attackers choose burn / starve / bargain. Defenders choose hold / sortie / abandon. Resolve in one scene unless the table wants a war.

**Unusual magic:** if Resonance would break a gate puzzle, charge extra RP and a reputation hit with floor civs who needed that puzzle intact.

## More Tables

### Rival Company Motives (d8)

1. Glory
2. Academic proof
3. Pact zeal
4. Imperial contract
5. Personal revenge
6. Smuggling
7. Prophetic panic
8. Quiet sabotage

### Haven Events (d6)

1. Theft
2. Confession
3. Wedding under wardlight
4. Quarantine
5. Map trade
6. Ghost of a sealed Cycle

### Research Breakthroughs (d6)

1. Glyph partial
2. Signatory title found
3. False creator hymn exposed
4. Material recipe
5. Rival cipher
6. Heartcell symptom without name

## Closing Charge

You are not the antagonist. The silence is. Keep the world noisy enough to live — and honest enough that when the party learns the dungeon's true engineering, they earned it.
"""
p.write_text(p.read_text(encoding="utf-8") + extra, encoding="utf-8")
print("words", len(p.read_text(encoding="utf-8").split()))
