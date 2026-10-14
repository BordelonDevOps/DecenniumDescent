# Author review queue — coffee decisions

**Date:** 2026-07-30 · **Scope:** owner decisions recorded and implemented.  
**State:** Mystery/Oath profile tone queues and the nine draft Oracle curse profile passes are complete. **Spiral-Touched** remains the rulebook-complete curse reference; only Mystery of Shadow and Oath of Grief were promoted.

---

## 1. Obsidian Burn theology

**Canon decision recorded (owner, 2026-07-30):** The **Obsidian Burn / Umbrin betrayal** pivot is canon. Umbrin are a people of The Murk; their demonym derives from primordial **Umbra**, not from the deity itself. Calan'thir and the First Choir exiled their forebears, and the Obsidian Burn is remembered as the resulting obsidian sheen. Murk Umbra cults remain a heretical, perverse reading of Umbra rather than Choir orthodoxy.

**Geography decision locked — Proposal 1:** **The Murk** remains the broad region and approach; **Blackglass Reach** is the surface/near-Murk marches; **Veyr-Obsid** is the primary Umbrin city; and **the Quiet Deep** is the deeper underworld. This is canon, not a request for further geography proposals.

**Alliance posture locked:** The world broadly distrusts Umbrin for betrayal and cult association. Alliances are tentative, transactional, and self-serving—not redemption by default.

**Source:** [`UMBRIN_LORE.md`](./UMBRIN_LORE.md) §§2–3 and [`CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md) rows Umbra through Obsidian Burn. This records lore canon only; no `draft: true` flags were changed.

---

## 2. Umbrin personal naming examples — resolved

**Locked canon:** Umbrin (people/adjective/plural), The Murk, Blackglass Reach, Veyr-Obsid, the Quiet Deep, Murkish, Umbra, Calan'thir, First Choir, and Obsidian Highborn.

**Owner ruling implemented:** Personal names: **Vaerith, Sythra, Korven, Zelka, Dravik, Nyssara, Kethren, Vorskai**. Houses: **House Veyr, Ashketh, Rhal-Voss, Obis-Keth**. Optional epithets: **of the Blackglass, Quiet-Step, Ash-Veiled, Deepbound**. The pattern is 2–3 syllables, hard consonants, and sparse apostrophes; it avoids foreign dark-elf and existing EverQuest proper-name clones.

**Source:** [`UMBRIN_LORE.md`](./UMBRIN_LORE.md) and [`CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md).

---

## 3. Master Tracker duplicate — resolved

**Canonical record:** `master_tracker` — **Master Tracker**, type **Skill**, prerequisite **Survival 4+, Wisdom 13+**, effect **Track creatures with +10 accuracy**.

**Retired duplicate:** `skill_feats1_master_tracker` remains in [`src/data/feats.js`](../../src/data/feats.js) as `deprecated: true` for historical save compatibility, but is filtered from Builder types and feat cards. New characters cannot select two identical Master Trackers.

**Status:** Resolved; no history was mass-deleted.

---

## 4. Resonance multiclass — resolved

**Approved Hybrid-B canon:** highest Weave-caster pool + ceil(25% of one secondary Weave-caster pool); tertiary+ classes add no pool. Builder, Sheet, and Session consume the saved secondary-class data.

**Implementation:** The formula is no longer presented as draft. It is now written into `rulebook_output.txt` and the player rulebook; a merged pool remains marked draft only when either contributing class has a separately still-draft pool table. Player-facing copy stays **Resonance / RP**; **Hybrid-B** remains internal documentation only.

**Source:** [`RESONANCE_CANON.md`](./RESONANCE_CANON.md) §7 (and its shipped/draft summary).

---

## 5. Draft → approved promotion candidates — first decisions recorded

**Promoted canon (owner, 2026-07-30):** **Mystery of Shadow** and **Oath of Grief**. Shadow's Murk / Quiet Deep silhouette and Grief's exile-and-betrayal aftermath now fit the locked Umbrin canon. Their full existing profiles remain mechanically unchanged apart from their approval state.

| Group | Candidates ready for owner review | Current source / status |
|---|---|---|
| Oracle Mysteries | Battle, Bones, Cataclysm, Dream, Flame, Life, Stars, Time | Shared `draftMysteryRevelations()` provenance in `oracle-mysteries.js`; Ancestor and Shadow are approved full-tree references. |
| Sacred Oaths | Mercy, Vengeance, Dominion, Flame, Ancients, Silence, Chain, Chains Broken, Martyr King | Every listed oath remains `draft: true` in `paladin-oaths.js`; Oath of Grief is approved canon. |
| Oracle Curses | Wound Eater, Soul-Cracked, Haunted, Tongues, Burning Blood, False Life, Shattered Mind, Consumed, Fate-Bound | Every record remains `draft: true` in `oracle-curses.js`; Spiral-Touched is rulebook-complete. |

## Next step

Leave all remaining Mystery, Oath, and Curse drafts untouched pending individual review. Continue Umbrin work only within the locked Obsidian Burn → Murk → Blackglass Reach → Veyr-Obsid → Quiet Deep continuity and its transactional alliance posture.
