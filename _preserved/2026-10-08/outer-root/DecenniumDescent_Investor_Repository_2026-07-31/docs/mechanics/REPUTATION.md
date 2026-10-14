# Reputation — companion implementation

**Status:** First playable (2026-07-29). Tracks faction standing for playtest prep and session adjustments. **Resonance economy is canon (Hybrid-B, "Resonance")** — see [`RESONANCE_CANON.md`](./RESONANCE_CANON.md). Core RP modifiers from the 4 Resonance tracks are **wired** in `resonance-economy.js` and flow through Builder, Sheet, and SessionTracker.

**Canon source:** Rulebook Ch4 (`rulebook_output.txt` ~3795–3801, background starting reputation ~3960+) and Weave Ch Resonance tracks (~6144–6158).

---

## What it does now

| Surface | Behavior |
|---------|----------|
| **Character Builder → Past tab** | Selecting a background applies mapped starting faction scores. Full faction editor with ± controls. |
| **Character Sheet** | Read-only compact list of non-neutral standings; shows background starting-reputation prose. |
| **Session Tracker** | Pick a saved hero → ± adjust active faction scores; persists via `upsertCharacter()`. |
| **Save field** | `reputation` — object `{ [factionId]: score }` normalized in `character-storage.js`. |

---

## Tiers and scores

Rulebook tiers: **Hated → Disliked → Neutral → Liked → Honored**.

Companion maps integer scores **−3…+3** to tiers:

| Score | Tier |
|-------|------|
| ≤ −2 | Hated |
| −1 | Disliked |
| 0 | Neutral (default when unset) |
| +1 | Liked |
| +2+ | Honored |

Unset factions behave as **Neutral (0)** until a background or manual edit sets them.

---

## Factions

**Data:** `src/data/reputation.js`

- **4 Resonance tracks** (rulebook Weave chapter — canon, not draft): Academic Factions, Religious Orders, Arcane Guilds, Nature Circles.
- **Social / background factions** extracted from Ch4 background starting-reputation prose (e.g. Aethel Authorities, Merchant Guilds, Dark Cults).
- Entries marked `draft: true` are companion placeholders where the rulebook names a group loosely or only in one background — Aethel tone, pending author promotion.

**Umbrin note (`draft: true`):** No dedicated "Umbrin" faction id — bias is narrative. Umbrin are broadly distrusted by civic and mainstream faith tracks but may hold **strange alliances** with Underworld, Planar Trading Guilds, Corruption Scholars, or Anti-Cult Alliances when stories overlap. See [`UMBRIN_LORE.md`](./UMBRIN_LORE.md).

Background → starting scores: `BACKGROUND_STARTING_REPUTATION` keyed by background name (matches `backgrounds.js`).

---

## Resonance link — **wired (core modifiers)**

**Resonance** (canon name; internal ruling label "Hybrid-B") ties reputation to:

- **RP pool size** — Arcane Guilds ±1..±2 max RP (`maxRpRepModifier()`)
- **Spell cost** — class-relevant track ±1 RP per cast (`spellCostRepModifier()`)
- **Retune recovery** — Nature Circles ±1 on short rest (`retuneRepBonus()`)

Implemented in `resonance-economy.js`; Builder, Sheet, and SessionTracker consume via `resolveMaxRp()` and `computeSpellCost()`. Player-editable `resonancePoints` on the character save is unchanged — computed max and cost previews update from reputation; current RP is not silently rewritten.

**Not yet wired:** Academic spell-learning discounts, Religious divine failure chance, Nature urban-prep restriction (Ch9 prose extras).

---

## Playtest checklist

- [ ] Background selected → expected factions show non-zero on Builder Past tab
- [ ] Save → reload → scores persist on sheet and Session picker
- [ ] Session ± updates save back to `dd_characters`
- [ ] Draft factions show `(draft)` badge in Builder editor
- [ ] Resonance RP updates when reputation changes on a combatant already on the tracker (re-pull character or manual adjust)

---

## Related docs

- [`CHARGEN_PROGRESSION.md`](./CHARGEN_PROGRESSION.md) — backgrounds and save shape
- [`SESSION_LOOP.md`](./SESSION_LOOP.md) — session surfaces
- [`RESONANCE_CANON.md`](./RESONANCE_CANON.md) — canon Resonance system (Hybrid-B)
- [`../MECHANICS_BIBLE.md`](../MECHANICS_BIBLE.md) §2 Resonance economy
- [`../../src/data/CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md) — Reputation term
- [`UMBRIN_LORE.md`](./UMBRIN_LORE.md) — Umbrin exile lore (`draft: true`) and faction bias notes
