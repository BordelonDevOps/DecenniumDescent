# Continuity C — IP scrub (`docs/manuals/*.md`)

**Agent:** Continuity C  
**Date:** 2026-07-30  
**Scope:** All six markdown files under `docs/manuals/`  
**Rule:** No foreign tabletop product brands in published prose; stock monster/people names need Aethel reskins or explicit stub labels before ship.

---

## Executive summary

| Category | Count (approx.) | Action |
|----------|-----------------|--------|
| Forbidden brand / edition refs | 2 files (meta) | **Fixed** in this pass |
| Foreign book citations (DMG / PHB) | 5 lines in Director manual | **Fixed** → Player Rulebook Environment |
| `drow` in Director NPC blurbs | 6 lines | **Fixed** → `Umbrin` |
| `Hybrid-B` (internal label) | 6 mentions, Director manual | **OK** in collaborator docs; strip from player-facing Crucible |
| Duplicate stock + Aethel reskin pairs | 9 families, ~100+ headings | **Writer / Codex** — remove stock side from Excel + re-ingest |
| Bare stock lexicon entries (no reskin) | Majority of 763 rows | **Writer queue** — rename or mark `stub: stock alias` |
| Lifted PHB-style chapter dump | Director manual §Ch.2–3+ | **Writer queue** — replace with DD-original prose |

---

## Fixed in this pass (trivial, applied)

| File | Change |
|------|--------|
| `BOOK_LINEUP.md` | Removed `EllatharTheHalfling/DnD-Books` and `` `5e/Books` `` reference |
| `DIRECTOR_REBUILD_BRIEF.md` | Same — structure-only framing, no product path |
| `AGENT_SIMULATION_REFERENCE.md` | “DM Guide” → “primary Director reference” |
| `README_MANUALS.md` | “Dungeon Master / Director” → “Director” |
| `Decennium_Descent_Directors_Manual.md` | 4× “chapter 5 of the Dungeon Master’s Guide” → Player Rulebook Environment (heat/cold) |
| `Decennium_Descent_Directors_Manual.md` | 1× “Player’s Handbook” → Player Rulebook Environment |
| `Decennium_Descent_Directors_Manual.md` | 6× NPC blurbs: `drow` → `Umbrin` |

---

## Forbidden brands — hits

### Resolved (meta / collaborator)

| File | Line | Hit | Status |
|------|------|-----|--------|
| `BOOK_LINEUP.md` | 13 | `DnD-Books`, `` `5e/Books` `` | **Fixed** |
| `DIRECTOR_REBUILD_BRIEF.md` | 5 | Same | **Fixed** |

### Not found in scope

- Pathfinder, Paizo, Volo, Trench Crusade, Wizards of the Coast, SRD, OGC, Open Game License, Forgotten Realms, Underdark (exact string)

### Borderline / contextual (no change)

| File | Context | Notes |
|------|---------|-------|
| `Decennium_Descent_Directors_Manual.md` | Lore uses “trench” (battlefield geography) | Not *Trench Crusade* — keep |
| `Decennium_Descent_Directors_Manual.md` | Lowercase “wizards” in narrative; capitalized **Wizards** in dumped class chapter | Class chapter is PHB-adjacent dump — see writer queue |
| `Decennium_Descent_Directors_Manual.md` | `P2_CASUAL_5E.md` in playtest log table | Filename only, historical record — OK in internal annex; do not quote “5e” in published prose |

---

## Hybrid-B (player-facing risk)

| File | Lines | Verdict |
|------|-------|---------|
| `Decennium_Descent_Directors_Manual.md` | 1993–2088, 7226 | **Internal OK** — section already warns: do not print on sheets/UI. Keep in Director archive + `RESONANCE_CANON.md`. |
| Published **The Director's Crucible** (DM-01) | — | **Writer:** use “Resonance” / “Resonance Points (RP)” only; move “Hybrid-B” to `SRC-01` or code comments |

---

## Bestiary — duplicate stock vs Aethel reskin

The bestiary already defines Aethel names but **still lists the stock headings and index strings**. Gate rosters and sims should use the right column only.

| Stock (remove / alias) | Aethel canon (keep) | Stock `###` headings | Notes |
|------------------------|---------------------|----------------------|-------|
| **Drow** (+ all variants) | **Umbrin** (+ variants) | 10 | Includes `Drow Priestess of **Lolth**` → `Umbrin Spider-Priestess` |
| **Beholder** (+ zombie, in lair) | **Gaze Tyrant** (+ husk, sovereign) | 5+ | |
| **Mind Flayer** (+ arcanist, lich) | **Voidmind** (+ arcanist, archivist, lich) | 4+ | |
| **Kuo-toa** (+ archpriest, whip) | **Depth Toad** (+ archpriest, taskmaster) | 4+ | |
| **Duergar** (+ variants) | **Deep Dwarf** (+ matching rank names) | 8+ | `Svirfneblin` still bare — see below |
| **Yuan-ti** (+ malison, etc.) | **Serpent-Blood** (+ matching ranks) | 8+ | |
| **Myconid** (+ sovereign, sprout) | **Sporefolk** (+ adult, sovereign, sprout) | 3+ | |
| **Githyanki** (+ ranks) | **Astral Reaver** (+ ranks) | 5+ | |
| **Githzerai** (+ ranks) | **Astral Ascetic** (+ ranks) | 4+ | |

**Recommended procedure (Codex Writer + generator):**

1. Edit `Bestiary.xlsx` — delete or rename stock rows to Aethel column.  
2. `python scripts/generate_official_manuals.py`  
3. Add one-line lexicon note on first Umbrin entry: *“Umbrin — deep-folk of the Bloomdeep; replaces retired stock alias ‘drow’ in Director materials.”*

---

## Bestiary — high-priority stock names (no reskin yet)

These read as imported stat-block titles. Either adopt an Aethel name from the rename table below or tag `stub: stock alias (Director draft)` until rewritten.

### Deity / pantheon-locked (FR/OGL flavor)

| Stock name | Recommended Aethel stub |
|------------|-------------------------|
| Drow Priestess of **Lolth** | Umbrin Spider-Priestess (Bloomdeep spiral cult) |
| Gnoll Fang of **Yeenoghu** | Gnoll Fang of the Howling Fracture |
| Orc Blade of **Ilneval** | Orc Blade of the Iron March |
| Orc Eye of **Gruumsh** | Orc Eye of the One-Eyed Pact |
| Orc Hand / Nurtured One of **Yurtrus** | Orc Hand of the Rot Sigil |
| Orc Red Fang of **Shargaas** | Orc Red Fang of the Veiled Hunt |
| Spawn of **Kyuss** | Spawn of the Worm Spiral |

### Iconic monsters (strong product association)

| Stock | Suggested rename / stub |
|-------|-------------------------|
| Beholder / Gauth / Death Tyrant | Gaze Tyrant* (partial — finish deprecating stock headings) |
| Mind Flayer / Intellect Devourer / Neothelid | Voidmind* / Mind Leech / Spiral Worm |
| Flumph | Lumen Drifter (Undercell harmless aberration) |
| Owlbear | Hookbeast |
| Tarrasque | Worldbreaker (singular myth — one per cycle) |
| Abishai (color variants) | Pact Devil — color by Chaos-Realm court |
| Alhoon | Voidmind Archivist (lich-adjacent) |
| Draegloth | Umbrin Warborn |
| Drider | Umbrin Arachnid (if distinct from Arachnomancer) |

### Peoples / rank names still stock

`Duergar`, `Svirfneblin`, `Aarakocra`, `Kenku`, `Tortle`, `Grung`, `Tabaxi`-class names, `Thri-kreen`, `Bullywug`, `Kobold` (people OK if generic), full **Gith** line, **Slaad** line, **Yugoloth** proper names (`Merrenoloth`, `Ultroloth`, …), **Modron** drones, **Eladrin** seasons, **Sorrowsworn**, **Star Spawn***, **Neogi**, **Hook Horror**, **Umber Hulk**, **Rust Monster**, **Carrion Crawler**, etc.

\*Star Spawn / Neogi: either full Aethel rewrite or `stub: Spiral breach echo` label in ecology line.

---

## Bestiary — index strings (CR appendix lists)

Lines ~8068–8167 repeat **both** stock and reskin names in comma-separated rosters (e.g. `Drow Inquisitor` beside `Umbrin Inquisitor`). After Excel cleanup, regenerate; until then Directors should **call Umbrin / Gaze Tyrant / Voidmind** at table and treat stock strings as legacy aliases.

---

## Director manual — writer queue (non-trivial)

| Issue | Location | Recommendation |
|-------|----------|----------------|
| PHB multiclassing paragraph | ~3321 | Replace with DD multiclass + Resonance cross-ref; remove “chapter 6” external cite |
| Small / heavy weapons “chapter 6” | ~2486 | Point to Player Rulebook equipment chapter |
| Full **Classes** / **Wizard** chapter dump | ~3315–6425 | Not in Player Rulebook class list (Mage, not Wizard). Strip or rewrite for Crucible; do not ship PHB table verbatim |
| `barbarian` / `paladin` / `wizard` in multiclass example | ~3321 | Use DD classes (Warrior, Oathbound, Mage, …) |
| Historical `P2_CASUAL_5E.md` path | ~1730 | OK in SRC annex; optional rename file to `P2_CASUAL_LEGACY.md` in playtest folder (out of scope unless owner asks) |

---

## Rename quick-reference (Codex lexicon)

Use in `Bestiary.xlsx` **Name** column; ecology one-liner can say “formerly indexed as …” in Director draft only, not player books.

```
Drow*                    → Umbrin*
Beholder*                → Gaze Tyrant*
Mind Flayer*             → Voidmind*
Kuo-toa*                 → Depth Toad*
Duergar*                 → Deep Dwarf*
Yuan-ti*                 → Serpent-Blood*
Myconid*                 → Sporefolk*
Githyanki*               → Astral Reaver*
Githzerai*               → Astral Ascetic*
Flumph                   → Lumen Drifter
Owlbear                  → Hookbeast
Tarrasque                → Worldbreaker
Intellect Devourer       → Mind Leech
Draegloth                → Umbrin Warborn
Svirfneblin              → Deep Gnome (or merge into Deep Dwarf culture)
```

---

## Clean files (no action)

| File | Result |
|------|--------|
| `AGENT_SIMULATION_REFERENCE.md` | Clean after meta fix |
| `README_MANUALS.md` | Clean after meta fix |
| `BOOK_LINEUP.md` | Clean after meta fix |
| `DIRECTOR_REBUILD_BRIEF.md` | Clean after meta fix |

---

## Next owners

| Agent | Task |
|-------|------|
| **Codex Writer** | Excel scrub: drop stock side of duplicate pairs; deity-name variants |
| **Crucible Writer** | Remove PHB dump chapters; Resonance without Hybrid-B label in DM-01 |
| **Packager** | Re-run `generate_official_manuals.py` after Excel pass; verify docx |
| **Owner** | Approve Worldbreaker / Hookbeast / Pact Devil naming if locked for BB-01 |

---

*Regenerate this report after the next manual ingest or major Director rewrite.*
