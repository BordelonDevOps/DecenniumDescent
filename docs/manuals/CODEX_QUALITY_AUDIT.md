# Codex of the Heartcell — Quality Audit

*Generated alongside `Codex_of_the_Heartcell.md` from `src/bestiary_data_full.json` (708 entries) and Bestiary.xlsx's own NeedsReview column. Read-only audit — no source files were modified.*

## Headline counts

| Metric | Count |
|---|---|
| Monsters indexed | 708 |
| Gate Guardian chapters written | 10 / 10 |
| Entries flagged **STUB — Director must re-skin** | 509 (71.9%) — see problem #1 below for why this is so high |
| Excel `NeedsReview` rows (any severity) | 430 |
| Distinct attack names across all entries | 40 (4 generic names cover 1,131 of all attack instances) |
| Codex word count | ~148,631 words |

## Gate Guardian coverage checklist

| # | Guardian | Tier / Floor (gazetteer) | Lore | Staging | Lair/Terrain | Tactics | Reward-as-bait | Honesty box |
|---|---|---|---|---|---|---|---|---|
| 1 | Vaskor, the Stone Maw | T1 / Floor 10, Warded Gate | done | done | done | done | done | done |
| 2 | The Bloom That Hungers | T2 / Floor 20, Sporemist Gate | done | done | done | done | done | done |
| 3 | Ashthirst the Hollow | T3 / Floor 30, Lavaflow Gate | done | done | done | done | done | done |
| 4 | Gor Vekk, Architect of Ends | T4 / Floor 40, Radiance Gate | done | done | done | done | done | done |
| 5 | Choralith, Voice Below | T5 / Floor 50, Canticle Gate | done | done | done | done | done | done |
| 6 | Lumen of the Shattered Thread | T6 / Floor 60, Lumen Gate (unmapped) | done | done | done | done | done | done |
| 7 | Xarog, the Pactbound Furnace | T7 / Floor 70, Furnace Gate (unmapped) | done | done | done | done | done | done |
| 8 | Eirfax, the Dusk Crowned | T8 / Floor 80, Crown Gate (unmapped) | done | done | done | done | done | done |
| 9 | Threxus, the Iron Spiral | T9 / Floor 90, Spiral Gate (unmapped) | done | done | done | done | done | done |
| 10 | The Marquis of Silence | T10 / Floor 100, Marquis Gate (unmapped) | done | done | done | done | done | done |

All ten Gate Guardian chapters are complete in Part II, including the cross-tier Seal Ladder CR-curve honesty table.

## Top 50 worst data problems

## Gate Guardian data contradictions (all 10, see Part II for full detail)

1. **Vaskor, the Stone Maw** — sheet Type is Ooze; field description calls it "a colossal earth elemental." Codex runs it as Elemental.
2. **Vaskor, the Stone Maw** — field description claims "Floor 20, Heart of the Verdant Wild"; Chronicle gazetteer places it at Floor 10, Warded Gate, Yieldheart Caverns.
3. **The Bloom That Hungers** — field description claims "Floor 10, the Echoing Grotto"; gazetteer places it at Floor 20, Sporemist Gate, Bloomdeep Marsh.
4. **The Bloom That Hungers** — CR 5 is the lowest of all ten Gate Guardians despite guarding the second seal; the difficulty curve is inverted at this point.
5. **Ashthirst the Hollow** — field description's location name ("Fields of Whispering Grasses") and Zone ("Aethel Jungles") both contradict the Anvil of Brogi forge setting the gazetteer assigns it.
6. **Gor Vekk, Architect of Ends** — sheet Type is Fey; field description calls it "an ancient aberration."
7. **Gor Vekk, Architect of Ends** — CR 29 is dramatically inflated for a Tier 4 ("Expert") seal — higher than the Tier 8 and Tier 9 guardians. Field description also claims "Floor 90," a 50-floor discrepancy from the gazetteer's Floor 40.
8. **Choralith, Voice Below** — field description claims "Floor 40, the Sepulcher of Silent Thrones," directly colliding with Gor Vekk's field description, which also claims Floor 40. Gazetteer resolves both: Choralith is Floor 50, Gor Vekk is Floor 40.
9. **Lumen of the Shattered Thread** — Type is Undead, but field description says its "form shifts between the four elements," reading as Elemental rather than Undead. Field description claims Floor 50; gazetteer places it at Floor 60.
10. **Xarog** — the sheet contains two entries for the same name: a stray Excel-sandbox row ("Xarog the Pactbound Furnace," no comma, Elemental CR 10, generic Freak Bite/Tail Lash attacks, no Gate Guardian tag) and the intended companion-authored row ("Xarog, the Pactbound Furnace," with comma, Fiend CR 26, tagged Gate Guardian). Recommend deleting the no-comma row.
11. **Xarog, the Pactbound Furnace** — field description claims "Floor 80"; gazetteer places it at Floor 70.
12. **Eirfax, the Dusk Crowned** — sheet Type is Fiend; field description calls it "a twilight fey lord." Field description claims "Floor 70"; gazetteer places it at Floor 80.
13. **Threxus, the Iron Spiral** — sheet Type is Fey; field description calls it "a massive construct of spiraling iron and radiant energy." Field description claims "Floor 60"; gazetteer places it at Floor 90 — the largest floor discrepancy (30 floors) among all ten seals.
14. **The Marquis of Silence** — sheet Type is Ooze; field description calls it "a demon lord of unimaginable power."
15. **The Marquis of Silence** — Alignment is listed as Chaotic Good, which cannot be reconciled with a demon lord "who rules through silence and fear" under any reading. Flag for correction to an evil alignment.
16. **Seal Ladder overall** — the intended Novice→Legendary difficulty curve is not monotonic: Tiers 2 and 9 dip below the seal immediately before them, and Tiers 4 and 7 spike dramatically above their neighbors. See the Seal Ladder table at the end of Part II.

## Systemic problems found across the general Lexicon (708 entries)

17. **Type field is effectively random relative to creature name across the whole sheet — the single largest driver of the 509-entry STUB count.** Cross-checking all 708 names against an ordinary-usage archetype dictionary (~300 recognizable names covering Beasts, Humanoids, Undead, Fiends, Giants, Dragons, and more) found **432 mismatches** — roughly the same hit rate one would expect from assigning Type uniformly at random across 14 categories (~93% mismatch odds). This is not a handful of edge cases; it is evidence the sandbox generator assigned Type independently of Name for the entire 708-row sheet. Treat every un-reviewed Type field in `Bestiary.xlsx` as unverified until a Director or the next ingest pass confirms it by hand.
18. **Reused sandbox attack names.** Only 40 distinct attack names exist across all 708 monsters' attack lists. Four of them — *Tail Lash* (433 uses), *Monstrous Claw* (253), *Freak Bite* (237), *Aberrant Lash* (208) — account for 1,131 of the total attack instances. The remaining 36 bespoke names appear exactly once each (almost entirely on the ten Gate Guardians).
19. **Culture families with internally randomized Type/Size.** Named humanoid-culture families (Umbrin, Deep Dwarf, Serpent-Blood, Astral Reaver, Astral Ascetic, Depth Toad, Gaze Tyrant, Voidmind, Cave Gnome) each have their Type and Size assigned independently per rank rather than consistently — e.g. Umbrin ranges across Beast, Giant, Construct, Celestial, Aberration, and Plant, and from Tiny to Gargantuan, across its ten members. See Part IV for the full list and the Codex's blanket correction (treat all as Humanoid/Aberration as noted per family).
20. **Excel's own `NeedsReview` column is populated on 430 of 708 rows (60.7%)** — 151 of those are Size corrections explicitly marked `cr-suspect-high` (the Challenge Rating looks too high for the sheet's current Size), 46 more are Size corrections without that suffix, and the remaining 233 are Hit Point corrections only.
21. **Old Bestiary of Aethel grammar bugs (fixed in this Codex).** Ecology section headers read "On Feys," "On Monstrositys," and "On Undeads" in the prior draft — corrected here to "The Fey," "Monstrosities," and "The Undead."
22. **Old Bestiary of Aethel boilerplate (fixed in this Codex).** Every one of the prior draft's 700+ entries repeated the identical sentence "Directors: decide whether this creature is a patrol, a nest guardian, a harvest node, or a political actor. Resource teams want parts; Research teams want behavior notes; Recon wants routes that avoid fair fights." verbatim, regardless of Type. This Codex replaces that with combinatorial, Type-specific ecology text (see `scripts/codex_ecology_phrases.js`).
23. **Old Bestiary "Traits" copy-paste bug (documented, not present in this Codex's own prose).** Many prior-draft entries' Traits line read "Draft stats from CR X Medium monstrosity band (excel-sandbox generator)" even when the creature in question was neither Medium nor a Monstrosity (e.g. a Huge Aberration). This Codex's honesty notes reference the creature's actual sheet Size/Type instead.
24. **IP scrub backlog.** 15+ individually-flagged stock/iconic names remain unrenamed pending owner sign-off (Flumph, Owlbear, Tarrasque, the full Yugoloth/Modron/Demon-hierarchy rank families, Star Spawn, Neogi, Slaad, Eladrin, Sorrowsworn, Abishai, and the ten deity-locked orc/gnoll/firenewt/xvart rank names) — see the Naming & IP Reskin Ledger in Part V.
25. Name/Type mismatch: **Depth Toad Archpriest** — sheet Type **Aberration**, name implies **Humanoid**.
26. Name/Type mismatch: **Quasit** — sheet Type **Aberration**, name implies **Fiend**.
27. Name/Type mismatch: **Umbrin Matron** — sheet Type **Aberration**, name implies **Humanoid**.
28. Name/Type mismatch: **Vargouille** — sheet Type **Aberration**, name implies **Fiend**.
29. Name/Type mismatch: **Chasme** — sheet Type **Aberration**, name implies **Fiend**.
30. Name/Type mismatch: **Glabrezu** — sheet Type **Aberration**, name implies **Fiend**.
31. Name/Type mismatch: **Quipper** — sheet Type **Aberration**, name implies **Beast**.
32. Name/Type mismatch: **Shadow** — sheet Type **Aberration**, name implies **Undead**.
33. Name/Type mismatch: **Azer** — sheet Type **Aberration**, name implies **Elemental**.
34. Name/Type mismatch: **Bodak** — sheet Type **Aberration**, name implies **Undead**.
35. **Depth Toad Archpriest** — culture family entry sheet-typed **Aberration** instead of the expected Humanoid/Aberration.
36. **Umbrin Matron** — culture family entry sheet-typed **Aberration** instead of the expected Humanoid/Aberration.
37. **Deep Dwarf Mind Master** — culture family entry sheet-typed **Aberration** instead of the expected Humanoid/Aberration.
38. **Umbrin Inquisitor** — culture family entry sheet-typed **Beast** instead of the expected Humanoid/Aberration.
39. **Umbrin** — culture family entry sheet-typed **Beast** instead of the expected Humanoid/Aberration.
40. **Voidmind Archivist** — culture family entry sheet-typed **Beast** instead of the expected Humanoid/Aberration.
41. **Umbrin Favored Consort** — culture family entry sheet-typed **Beast** instead of the expected Humanoid/Aberration.
42. **Depth Toad Taskmaster** — culture family entry sheet-typed **Celestial** instead of the expected Humanoid/Aberration.
43. Excel NeedsReview: **Vargouille** — `size:Small->Large; cr-suspect-high` (Size Large, CR 7, HP 123).
44. Excel NeedsReview: **Shadow** — `size:Small->Large; cr-suspect-high` (Size Large, CR 8, HP 142).
45. Excel NeedsReview: **Bodak** — `size:Small->Large; cr-suspect-high` (Size Large, CR 9, HP 157).
46. Excel NeedsReview: **Cow** — `size:Small->Large; cr-suspect-high` (Size Large, CR 9, HP 157).
47. Excel NeedsReview: **Swarm of Ravens** — `size:Small->Large; cr-suspect-high` (Size Large, CR 10, HP 172).
48. Excel NeedsReview: **Gorgon** — `size:Small->Huge; cr-suspect-high` (Size Huge, CR 11, HP 187).
49. Excel NeedsReview: **Swashbuckler** — `size:Medium->Huge; cr-suspect-high` (Size Huge, CR 11, HP 187).
50. Excel NeedsReview: **Alkilith** — `size:Small->Huge; cr-suspect-high` (Size Huge, CR 12, HP 202).

## Recommended next owner actions

1. Decide Gor Vekk's and Xarog's true intended CR (Part II, Seal Ladder) — the current sheet cannot be run as a monotonic difficulty curve without a Director-side scaling decision.
2. Delete the stray no-comma "Xarog the Pactbound Furnace" duplicate row from `Bestiary.xlsx`.
3. Approve or amend the proposed renames in the Naming & IP Reskin Ledger (Part V of the Codex) before any are locked into `Bestiary.xlsx`.
4. Consider a dedicated Excel pass to normalize Type/Size on the culture-family rows (Umbrin, Deep Dwarf, Serpent-Blood, Astral Reaver/Ascetic, Depth Toad, Gaze Tyrant, Voidmind) so they stop randomizing independently per rank.
5. Correct the Marquis of Silence's Alignment field (currently Chaotic Good) and Vaskor/Gor Vekk/Threxus/Marquis's Type fields per the Gate Seal honesty boxes in Part II.