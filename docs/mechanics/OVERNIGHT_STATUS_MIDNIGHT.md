# Midnight status — early wake check (~12am)



**For:** Owner · **Date:** 2026-07-30 · **Commit:** none



Full morning brief: **[`OVERNIGHT_HANDOFF.md`](./OVERNIGHT_HANDOFF.md)** — paths, coffee review, wave log.  

Deep log: [`OVERNIGHT_BRIEFING.md`](./OVERNIGHT_BRIEFING.md) · detail: [`OVERNIGHT_PROGRESS.md`](./OVERNIGHT_PROGRESS.md)



---



## One glance



| | |

|---|---|

| **Waves** | **1–63 done** (incl. 11b, 14b, 15b, 18b, 20b, 22b, 25b, 26b, 27b, 29b, 33a, 33b, 34b, 35b, 35c, 36, 37, 38b, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 48b, 49, 50a, 51, 52, 52b, 53, 54, 55, 55b, 56, 57, 58, 59, 60, 61, 62, 63) |

| **P0 / P1** | **0 / 0** — vague queue clear |

| **Build** | **Green** — `npx tsc --noEmit` + `npm run build` pass (wave 63) |

| **ASK OWNER** | **0 open blockers** |

| **Playtest** | Chargen → Session → Encounters/Generators → Dungeon Guide — **ready** |



**Verdict:** Playtest-ready. Overnight work continues; nothing needs you at midnight.



---



## Locks (do not revert)



- **Umbrin** — product demonym (not Drow / Umbral Elf). Murkish; Obsidian Highborn subrace.

- **Resonance** — RP economy. Oracle uses Revelation Charges, not RP.

- **Hybrid-B** — internal label only; never in UI.



**Latest (wave 63):** PLAYTEST_SMOKE stretch for **Overcast Burnout hint** (Mage L17+ tier 8+, RP &lt; 25% post-cast), **Ethos row**, and **Druid arch attunement**. Class-draft L11–20 gap fill: **Cleric/Monk/Ranger/Dragoon/Tinker L13/L15/L17** (14 milestones). **`npx tsc --noEmit` + `npm run build` green.** **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. **Coffee primary:** author tone review Oracle/Paladin/Umbrin; L11–20 author tables; Resonance multiclass formula author sign-off.



*Checkpoint only — see [`OVERNIGHT_HANDOFF.md`](./OVERNIGHT_HANDOFF.md) for full wave list and start-here docs.*

---

## Wave 64 addendum — Shaman Session totem stub

**Waves:** 1–64 done · **Commit:** none  
**Build:** `npx tsc --noEmit` + `npm run build` green (wave 64).

Session now provides a deliberately table-facing Shaman totem tracker: place/recall Spirit, Echo, Divining, or Blight totems from L6; L13 exposes a second active slot as a draft milestone; long rest clears placements. Effects, duration, and targeting are intentionally not automated.

Class scan confirms Paladin/Wizard/Warrior L13/L15/L17 are already canon in `class-details.js`; no duplicate draft content was created. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

---

## Wave 65 addendum — Shaman smoke + hero-form depth

**Waves:** 1–65 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` green (wave 65).

The smoke path now verifies Shaman totem place/recall at L6, both L13 draft slots, full-slot enforcement, and long-rest clearing without proposing per-totem automation. The remaining 13 concise Druid hero-form traits received descriptive depth only; their existing mechanics did not change. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

---

## Wave 66 addendum — Burnout recovery + Items empty state

**Waves:** 1–66 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` green (wave 66).

Session now clears the one-shot **Overcast check** hint through Short Rest, Long Rest, and direct **Full** Resonance recovery; the existing Overcast **Clear** control remains a fourth exit. The Burnout threshold/badge logic is unchanged. Items Library now gives zero-result searches a clear explanation and one-click **Clear all filters** recovery. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

---

## Wave 67 addendum — Session glossary + library parity

**Waves:** 1–67 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` pending.

The continuity glossary now defines the persisted Session fields behind Shaman totem slots, Druid arch attunement, Ethos, and the transient Burnout cast hint, preserving all existing draft and GM-resolution boundaries. Spells and Bestiary now match Items Library’s actionable zero-results recovery: **Clear all filters** restores a browsable catalog without deleting learned/favorite spell selections or other user state. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 67 validation update

`npx tsc --noEmit` and `npm run build` both passed (wave 67).

---

## Wave 68 addendum — Recovery smoke coverage + Ashen Grove draft context

**Waves:** 1–68 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` pending.

The optional smoke path now covers zero-result recovery for Items, Spells (including Learned/Favorites), and Bestiary, plus the three Burnout-hint rest/full-restore exits. Circle of the Ashen Grove’s two hero forms are explicitly **Draft** in the shared path display; six existing trait blurbs gained flavor-only context with no mechanics changed. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 68 validation update

`npx tsc --noEmit` and `npm run build` both passed (build ~49s).

---

## Wave 69 addendum — Encounters filter recovery parity

**Waves:** 1–69 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` green (build ~48s).

Floor Encounters now treats an active search as recoverable filter state: it reports the matching tier count, retains jump-to-tier controls for positive matches, and provides **Clear filters** in the result row. A true zero-result query receives a dedicated reset card; a query that only empties the current tier’s haven or POI column gets the same in-place reset. Unmapped-depth no-data prose is unchanged without a search.

Generators was checked but intentionally unchanged because it has no filter-driven catalog/result set. No Druid trait batch was duplicated after waves 65 and 68; Oracle, Paladin, Umbrin, totem automation, and rules math remain untouched.

---

## Wave 70 addendum — Encounter smoke stretch + cosmology draft flavor

**Waves:** 1–70 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` green; `npm run build` pending.

Floor Encounters now has deterministic smoke inputs for both reset surfaces: `zzzz-wave-70` checks the global zero-tier card, while T1 `Crystalfront` checks the POI-only local reset. Both are specified to retain the selected tier and **Load in Session** control.

Cosmology World sections X and XI are visibly marked draft while six concise export/forbidden-school labels gain flavor-only context. Existing named goods, places, schools, and all mechanics remain unchanged. Oracle, Paladin, Umbrin, totem automation, and 3D work remain untouched.

### Wave 70 validation update

`npx tsc --noEmit` **passed** (~8s) and `npm run build` **passed** (~41s).

**Clarification:** The draft flavor batch expands eight concise labels under the X/XI draft markers; no source facts or rules changed.

---

## Wave 71 addendum — Draft badge consistency + trade flavor

**Waves:** 1–71 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` green (build ~50s).

Circle of the Ashen Grove’s existing draft hero forms now retain their visible status through Builder selection, Character Sheet review, and Session form selection/active status. The shared helper simply forwards existing form metadata; no form mechanics, unlocks, or traits changed.

World X’s already-draft Economy & Trade extract adds flavor-only presentation to the existing **Divine Essence** and **Shard Markets** labels. Named goods, locations, Naegul’s protection, no-theft rule, and all mechanics are unchanged. Oracle, Paladin, Umbrin, totem automation, and 3D work remain deferred.

---

## Wave 72 addendum — Ashen Grove smoke + legends draft flavor

**Waves:** 1–72 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` pending.

The smoke guide now tests persisted Ashen Grove draft status through Builder selection, refresh, Sheet review, Session form selection, and active-form status—plus a non-Ashen leak guard. World XIII is visibly marked draft; its three existing Legends & Songs source labels retain their text while receiving one short presentation-only color line each. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 72 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~43s).

---

## Wave 73 addendum — Appendix draft flavor + Dungeon Guide recovery

**Waves:** 1–73 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` pending.

World XV’s existing Appendix labels now carry short presentation-only Draft color beneath a visible draft marker; chronology, lineage, dungeon reference, calendar facts, and mechanics are unchanged. Dungeon Guide Tier Details now recovers from a zero-match search or mapped-only combination with a dedicated empty state and **Clear filters**, instead of rendering a stale tier. Oracle, Paladin, Umbrin, totem automation, and 3D work remain untouched.

### Wave 73 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~47s).

---

## Wave 74 addendum — Dungeon Guide overview recovery smoke

**Waves:** 1–74 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` pending.

Dungeon Guide’s **Overview** now treats an empty tier grid as recoverable filter state: it replaces passive copy with an in-place **Clear filters** action that restores the grid without changing the selected tier or encounter data. `PLAYTEST_SMOKE.md` adds a deterministic `zzzz-wave-74` stretch covering this reset. No fresh lore flavor was added because the remaining World sections are source-gap, mechanics, or superseded; Oracle, Paladin, Umbrin, totem automation, and 3D work remain untouched.

### Wave 74 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s).

---

## Wave 75 addendum — Dungeon Guide paired recovery smoke

**Waves:** 1–75 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` pending.

Dungeon Guide now has paired deterministic smoke coverage for the existing Tier Details and Overview zero-result recovery: `zzzz-wave-75` plus **Mapped tiers only** verifies each reset restores its tier controls without changing the selected tier. Mechanics also recovers an empty filtered Victory Consequences list with explicit copy and **Clear filters**, returning all ten rows on reset. No source facts, mechanics, Oracle/Paladin/Umbrin review, prestige prose, totem automation, or 3D work changed.

### Wave 75 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s).

---

## Wave 83 addendum — final prestige capstone draft batch

**Waves:** 1–83 done · **Commit:** none  
**Validation:** pending.

Beastmaster and Chronomancer now carry expanded presentation-only capstone prose and the existing shared **draft** badge in Builder and Character Sheet. `PLAYTEST_SMOKE.md` names their Builder → Sheet provenance check. The full 18-path scan finds **0** prestige capstones without `draftCapstone`. No capstone resolution, mechanics, eligibility, prerequisites, Oracle/Paladin/Umbrin review, totem automation, cosmology/dungeon factual work, or 3D work changed.

---

## Wave 81 addendum — third prestige capstone draft batch

**Waves:** 1–81 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` and `npm run build` pending.

Wyrmslayer, Verdant Animist, Mooncursed, and Giant Killer now have expanded presentation-only capstone prose and the existing shared **draft** badge in Builder and Character Sheet. The smoke guide names a Builder → Sheet check for exactly those four paths. **6** prestige capstones remain undrafted. No capstone resolution, mechanics, eligibility, prerequisites, Oracle/Paladin/Umbrin review, totem automation, cosmology/dungeon factual work, or 3D work changed.

### Wave 81 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~43s). Commit: none.

---

## Wave 82 addendum — fourth prestige capstone draft batch

**Waves:** 1–82 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` pending.

Soulrender, Blademaster, Berserker, and Storm Lord now have expanded presentation-only capstone prose and the existing shared **draft** badge in Builder and Character Sheet. The smoke guide names a Builder → Sheet check for exactly those four paths. **2** prestige capstones remain undrafted: Beastmaster and Chronomancer. No capstone resolution, mechanics, eligibility, prerequisites, Oracle/Paladin/Umbrin review, totem automation, cosmology/dungeon factual work, or 3D work changed.

### Wave 82 validation update

`npx tsc --noEmit` passed (~12s) and `npm run build` passed (~42s). Commit: none.

---

## Wave 76 addendum — Races draft color + prestige hallmark provenance

**Waves:** 1–76 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~48s).

World VIII **Races of Aethel** now uses the existing draft-extract treatment: its five source labels are unchanged, with short presentation-only color lines added beneath them. Three previously terse prestige hallmarks—Bloodbound’s **Bloodletting Strikes**, Forge Master’s **Ember Pulse**, and Hexblade’s **Doom Sigil**—now carry compact draft flavor and a visible **draft** badge in Builder and Character Sheet. No source facts, prestige mechanics, Oracle/Paladin/Umbrin review, totem automation, or 3D work changed.

---

## Wave 77 addendum — Prestige smoke + draft provenance

**Waves:** 1–77 done · **Commit:** none  
**Validation:** pending.

The smoke guide now explicitly checks World VIII’s draft marker and Builder → Sheet badges for the three wave 76 prestige hallmarks. The next short batch adds draft-marked, presentation-only flavor to Sapper’s **Demolition Pack** and **Saboteur’s Toolkit**, plus Soulrender’s **Echo of Death**; existing indexed rendering shows each in Builder and Character Sheet. No prestige mechanics, Oracle/Paladin/Umbrin review, totem automation, Dungeon Guide recovery, source promotion, or 3D work changed.

### Wave 77 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~45s).

---

## Wave 78 addendum — Prestige thin batch + Myth & History draft flavor

**Waves:** 1–78 done · **Commit:** none  
**Validation:** pending.

Hexblade’s **Blade Hunger**, Storm Lord’s **Eye of the Tempest**, Verdant Animist’s **Living Terrain**, and Warlock’s **Pact Sigils** now carry short draft flavor and existing Builder/Sheet **draft** badges. World VII **Myth & History** is visibly draft, with five source labels preserved and five presentation-only color lines added. No mechanics, requirements, capstones, chronology, people, places, dungeon facts, Oracle/Paladin/Umbrin review, totem automation, or 3D work changed.

### Wave 78 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s).

---

## Wave 83 final append — prestige capstone completion

**Waves:** 1–83 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` + `npm run build` passed (build ~47s).

Beastmaster and Chronomancer now have presentation-only `draftCapstone` records and the existing shared Builder/Sheet **draft** badge. The full scan reports **18/18** draft-badged prestige capstones and **0** undrafted. Oracle/Paladin/Umbrin review, totem automation, and capstone mechanics remain untouched.

---

## Wave 84 addendum — prestige scheduling + unmapped-depth draft extract

**Waves:** 1–84 done · **Commit:** none  
**Validation:** pending.

Wave 83’s complete prestige-capstone presentation pass is logged for morning author scheduling: **18/18** draft-badged, **0** undrafted. Dungeon Guide now shows T6–T10’s existing source labels as visibly provisional **Draft extract** content: source-bounded survivor-rumor flavor for their tier, haven, POI, gate, and boss labels plus an in-context scope note. T6–T10 remain unmapped; no routes, hazards, mechanics, maps, rewards, or new facts were created. Oracle/Paladin/Umbrin review, prestige mechanics, feat/item mechanics, totem automation, and 3D work remain untouched.

### Wave 84 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~50s). No commit created.

### Wave 84 hallmark completion update

All **18/18** prestige paths have hallmark records; **0** are under 80 characters. The final two under the 100-character presentation target—Sapper’s **Saboteur’s Toolkit** and Soulrender’s **Echo of Death**—now use longer explicit draft copy with no rule change.

### Wave 84 final validation

`npx tsc --noEmit` and `npm run build` passed (build ~47s). The final scan reports **0** hallmarks under 80 or 100 characters and **18/18** draft capstones. No commit created.

---

## Wave 85 addendum — unmapped-depth visibility + feat draft batch
**Waves:** 1–85 done · **Commit:** none  
**Validation:** pending.

Dungeon Guide now visibly renders the existing T6–T10 `draftNote` records as a **Draft extract** badge and warning panel in Tier Details; the note is searchable, while all five tiers remain unmapped. The smoke guide supplies a deterministic T6–T10 visibility pass. A separate four-entry feat batch replaces generic placeholders for Acrobatic Mastery, Arcane Armor, Arcane Flexibility, and Arcane Pulse with explicitly draft presentation copy based only on their existing prerequisites and effects; Builder marks exactly those entries **Draft**. No feat behavior, dungeon procedure, Oracle/Paladin/Umbrin review, totem automation, or 3D work changed.

### Wave 85 validation update
`npx tsc --noEmit` passed (~10s) and `npm run build` passed (~43s). No commit created.

---

## Wave 86 addendum — generic feat draft batch
**Waves:** 1–86 done · **Commit:** none  
**Validation:** pending.

Arcane Recall, Arcane Transfusion, Armor Crusher, and Battle Awareness now use bounded, presentation-only draft descriptions and `draft: true`; the existing Builder feat cards render the compact **Draft** badge. The provenance smoke names all four through their Magic, Combat, and General filters. The exact generic-placeholder scan leaves **84** entries; the short-effect scan finds **8** draft feats solely because their source effect strings remain intentionally untouched. No prerequisite, effect, selection behavior, or automation changed. No Oracle/Paladin/Umbrin review, totem automation, T6–T10 mapped content, 3D work, deletion, or commit occurred.

### Wave 86 scan correction
The completed exact-placeholder scan reports **112** remaining descriptions; this supersedes the earlier provisional **84** figure.

### Wave 86 validation update
`npx tsc --noEmit` passed (~7s) and `npm run build` passed (~47s). No commit created.

---

## Wave 87 addendum — generic feat draft batch
**Waves:** 1–87 done · **Commit:** none  
**Validation:** pending.

Battlefield Commander, Battlefield Tactician, Beast Whisperer, Berserker Rage, Bleeding Edge, Blood Magic, Brace for Impact, and Break Line now use bounded, presentation-only draft descriptions and `draft: true`; the existing Builder feat cards render the compact **Draft** badge. The provenance smoke names all eight through their Combat, Skill, and Magic filters. The exact generic-placeholder scan leaves **104** entries. No prerequisite, effect, selection behavior, or automation changed. No Oracle/Paladin/Umbrin review, totem automation, T6–T10 mapped content, 3D work, deletion, or commit occurred.

### Wave 87 validation update
`npx tsc --noEmit` passed (~8s) and `npm run build` passed (~41s). The exact generic-placeholder scan reports **104** remaining. No commit created.

---

## Wave 88 addendum — generic feat draft batch
**Waves:** 1–88 done · **Commit:** none  
**Validation:** pending.

Bull Rush, Channeled Flow, Cleaving Momentum, Climb Anywhere, Close Quarters Combat, Cold Reader, Combat Intuition, and Combat Slide now use bounded, presentation-only draft descriptions and `draft: true`; the existing Builder feat cards render the compact **Draft** badge. The type-filtered provenance smoke names all eight through Combat, Magic, and Skill filters. The exact generic-placeholder scan leaves **96** entries. No prerequisite, effect, selection behavior, or automation changed. No Oracle/Paladin/Umbrin review, totem automation, T6–T10 mapped content, 3D work, deletion, or commit occurred.

### Wave 88 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~44s). The exact generic-placeholder scan reports **96** remaining. No commit created.

---

## Wave 89 addendum — generic feat draft batch
**Waves:** 1–89 done · **Commit:** none  
**Validation:** pending.

Concentrated Will, Counterspell Adept, Crippling Strike, Cultural Expert, Danger Sense, Diligent Researcher, Disarming Blow, and Disguise Expert now use bounded, presentation-only draft descriptions and `draft: true`; the existing Builder feat cards render the compact **Draft** badge. The compact type-filtered provenance smoke names all eight through Magic, Combat, Skill, and General filters. The exact generic-placeholder scan leaves **88** entries. No prerequisite, effect, selection behavior, or automation changed. No Oracle/Paladin/Umbrin review, totem automation, T6–T10 mapped content, 3D work, deletion, or commit occurred.

### Wave 89 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **88** remaining. No commit created.

---

## Wave 90 addendum — generic feat draft batch
**Waves:** 1–90 done · **Commit:** none  
**Validation:** pending.

Dispel Precision, Double Tap, Draw Cut, Dungeon Cartographer, Echo Spell, Efficient Caster, Empowered Summoning, and Energy Sink now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The exact generic-placeholder scan leaves **80** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 90 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~46s). No commit created.

---

## Wave 91 addendum — generic feat draft batch
**Waves:** 1–91 done · **Commit:** none  
**Validation:** pending.

Ether Anchor, Exploit Weakness, Field Medic, Field Surgeon, Flash Cast, Fleet of Foot, Forensic Investigator, and Foresight Surge now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The exact generic-placeholder scan leaves **72** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 91 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **72** remaining. No commit created.

---

## Wave 92 addendum — generic feat draft batch
**Waves:** 1–92 done · **Commit:** none  
**Validation:** pending.

Herbalist, Illusionist’s Trick, Inspiring Presence, Intuitive Reflex, Jack of All Trades, Librarian's Eye, Lingering Magic, and Lock Savant now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The exact generic-placeholder scan leaves **64** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 92 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~44s). The exact generic-placeholder scan reports **64** remaining. No commit created.

---

## Wave 93 addendum — generic feat draft batch
**Waves:** 1–93 done · **Commit:** none  
**Validation:** pending.

Lunge, Magical Fortitude, Mana Burn, Mental Buffer, Mental Fortress, Merchant’s Guile, Mirror Cast, and Mystic Focus now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The exact generic-placeholder scan leaves **56** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 93 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **56** remaining. No commit created.

---

## Wave 94 addendum — generic feat draft batch
**Waves:** 1–94 done · **Commit:** none  
**Validation:** pending.

Mystic Recoil, Natural Leader, Night Hunter, Overchannel, Overrun, Planar Knowledge, Polyglot, and Precise Shot now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The exact generic-placeholder scan leaves **48** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 94 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~42s). The exact generic-placeholder scan reports **48** remaining. No commit created.

---

## Wave 95 addendum — generic feat draft batch
**Waves:** 1–95 done · **Commit:** none  
**Validation:** pending.

Precision Throw, Protective Casting, Punishing Blow, Quick Learner, Quick Recovery, Quick Ritualist, Reckless Swing, and Resilient Mind now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The exact generic-placeholder scan leaves **40** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 95 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~42s). The exact generic-placeholder scan reports **40** remaining. No commit created.

---

## Wave 96 addendum — generic feat draft batch
**Waves:** 1–96 done · **Commit:** none  
**Validation:** pending.

Ritual Channeler, Rogue’s Escape, Runic Scholar, Runic Shield, Savage Momentum, Shattering Smash, Shield Bash, and Shield Expert now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The exact generic-placeholder scan is expected to leave **32** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 96 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~41s). The exact generic-placeholder scan reports **32** remaining. No commit created.

---

## Wave 97 addendum — generic feat draft batch
**Waves:** 1–97 done · **Commit:** none  
**Validation:** pending.

Silent Casting, Silent Movement, Silver Tongue, Skill feats1. Master Tracker, Spell Deflection, Spell Reservoir, Spell Scribe, and Spellweave now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The exact generic-placeholder scan is expected to leave **24** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 97 validation update
`npx tsc --noEmit` passed. `npm run build` passed (build ~41s). The exact generic-placeholder scan reports **24** remaining. No commit created.

---

## Wave 98 addendum — generic feat draft batch
**Waves:** 1–98 done · **Commit:** none  
**Validation:** pending.

Steady Hands, Still Casting, Stubborn Resolve, Sure Shot, Tactical Flanker, Tactical Insight, Target Mark, and Temporal Flux now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The malformed Wave 97 display label `Skill feats1. Master Tracker` was normalized to the clearly matching source title **Master Tracker** only; no mechanics changed. The exact generic-placeholder scan is expected to leave **16** entries. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 98 validation update
Pending `npx tsc --noEmit` and `npm run build`. No commit created.

### Wave 98 validation complete
`npx tsc --noEmit` passed (~7s) and `npm run build` passed (~41s). The exact generic-placeholder scan reports **16** remaining. No commit created.

---

## Wave 99 addendum — generic feat draft batch
**Waves:** 1–99 done · **Commit:** none  
**Validation:** pending.

Tenacity, Tinker Adept, Tough as Nails, Trap Sense, Twin Cast, Unshakeable, Unstoppable Force, and Versatile Artisan now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged; the compact type-filtered smoke path covers the eight cards. The canonical exact generic-placeholder queue leaves **8** records; the raw literal match’s pre-existing duplicate `master_tracker` is excluded because the visible Master Tracker record was normalized in wave 98. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**.

### Wave 99 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~46s). No commit created.

---

## Wave 100 addendum — final generic feat presentation pass
**Waves:** 1–100 done · **Commit:** none  
**Validation:** pending.

Versatile Grip, Volley, Weapon Finesse, Weapon Mastery, Whip Control, Whirlwind Striker, Wilderness Chef, and Wilderness Walker now have bounded presentation-only draft descriptions with the existing Builder **Draft** badge. Their prerequisite and effect strings, feat selection behavior, and all automation remain unchanged. The exact generic-placeholder scan now returns **0**.

The raw literal exception was confirmed as a true duplicate: `master_tracker` and `skill_feats1_master_tracker` share a name, prerequisite, and effect but differ in ID/type. The former still had a Skill placeholder, so its presentation was drafted too; neither record was deleted, merged, retyped, or otherwise mechanically changed. Author decision required.

**Suggested wave 101:** resolve the Master Tracker canonical-record question with the author, then take a bounded source-backed encounter, dungeon, or generator playtest pass. Oracle/Paladin/Umbrin author-tone review remains out of scope.

### Wave 100 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **0** remaining. No commit created.

---

## Wave 101 addendum — Session rest feedback

**Waves:** 1–101 done · **Commit:** none  
**Validation:** pending.

The Session horn clock now distinguishes a time-only **Advance +8h** from the resource-restoring **Long rest (+8h)**. Short/Long Rest display an accessible outcome summary with affected ally count and the existing resource/reset effects, reducing table ambiguity without changing recovery rules.

**Morning ASK OWNER:** retain both duplicate Master Tracker records (`master_tracker`, `skill_feats1_master_tracker`) until the canonical identity/type is chosen; do not delete, merge, or retype either record.

**Suggested wave 102:** manually smoke this rest feedback, then take one source-bounded Floor Encounters playtest-friction pass without inventing encounter content.

### Wave 101 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~48s). No commit created.

---

## Wave 102 addendum — chosen encounter handoffs

**Waves:** 1–102 done · **Commit:** none  
**Validation:** pending.

Floor Encounters now makes its Session bridge choiceful without adding any encounter material: the tier button stages its default site and fallback haven, while each existing Point of Interest or Safe Haven can be sent as the specific `Site` or `Fallback haven` line. The existing tier, floor, gate-boss, complementary default, draft-depth, and Session handoff behavior remain intact.

The smoke guide now checks both selected-entry paths and confirms that **Advance +8h** remains time-only while Short/Long Rest provide their distinct ally-count outcome feedback.

**Morning ASK OWNER:** retain both duplicate Master Tracker records (`master_tracker`, `skill_feats1_master_tracker`) until the canonical identity/type is chosen; do not delete, merge, or retype either record.

**Suggested wave 103:** browser-smoke the two selected-entry handoffs plus rest feedback, then take one source-bounded Generator usability pass using existing outputs only.

### Wave 102 validation update
`npx tsc --noEmit` and `npm run build` passed (build ~47s). No commit created.

---

## Wave 103 midnight stamp — Generator pack handoff guardrails (2026-07-30)

**Status:** Generators now stages only an already displayed pack in Session. The handoff control stays disabled until a pack is built, and tier selection clears the old pack so its text cannot be paired with a different tier. Copy and handoff actions visibly confirm success or provide a recovery message.

**Smoke pending:** Browser-check the two Wave 102 non-default encounter entry handoffs, the rest-feedback distinction, and the new Generator pack-first/tier-freshness/copy path. The IDE browser was unavailable in this run.

**Boundary:** No generator or encounter tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending the owner’s canonical-record decision.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~47s).

---

## Wave 104 midnight stamp — Bestiary selected-foe handoff (2026-07-30)

**Status:** The Bestiary now stages a selected source stat block directly into Session as one editable foe. The bridge preserves name, listed HP, CR, and zone; Session confirms the arrival and leaves initiative, HP, conditions, and resolution under GM control.

**Smoke pending:** Browser-check this new selected-foe path together with Wave 102’s non-default POI/haven handoffs and Wave 103’s pack-first, tier-clear, and clipboard-recovery checks. The IDE browser remains unavailable.

**Boundary:** No source tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending the owner’s canonical-record decision.

**Validation:** Pending Wave 104 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). The existing non-fatal `SessionTracker` exhaustive-deps warnings remain; no commit created.

---

## Wave 105 midnight stamp — Session saved-character refresh discoverability (2026-07-30)

**Status:** Session’s Add saved character card now identifies its browser-local source, labels available heroes with class and level, and reports the resulting count after **Refresh saved list**. The copy makes clear that adding a hero creates an editable encounter copy; later hero changes remain in Characters.

**Smoke pending:** Browser-check the saved-list return/refresh path with the existing Bestiary foe, selected POI/haven, and Generator pack-first/tier-clear/clipboard smoke rows. The IDE browser remains unavailable.

**Boundary:** Session correctly states that it has no separate JSON-import action. No character-storage semantics, automated inventory, encounter resolution, source tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending owner direction.

**Validation:** Pending Wave 105 typecheck and build.

### Validation update

`npm run build` passed (~44s) with the two existing non-fatal `SessionTracker` exhaustive-deps warnings. `npx tsc --noEmit` then passed (~9s); its initial concurrent run raced Next’s `.next` generation and was rerun after the build. No commit created.

---

## Wave 106 midnight stamp — Spell cast-preview handoff (2026-07-30)

**Status:** Spell Library cards now stage selected spell reference fields in Session through **Preview in Session**. Session confirms the spell, school, tier, casting time, range, and duration, then points to the existing caster spell lookup / Overcast controls.

**Smoke pending:** Browser-check the new spell-preview path plus the saved-list refresh return/feedback path and the prior Bestiary, selected POI/haven, and Generator handoffs when browser attachment is available. The unavailable browser attachment is non-blocking.

**Boundary:** The preview does not select a caster, spend RP, resolve a cast, add combatants, or alter saved characters. Oracle remains a Revelation Charge class. No character-storage semantics, automated inventory, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

**Validation:** Pending Wave 106 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~54s). The two existing non-fatal `SessionTracker` exhaustive-deps warnings remain. No commit created.

---

## Wave 107 midnight stamp — Items reference-preview handoff (2026-07-30)

**Status:** Selected Items Library details now stage only existing item reference fields in Session through **Preview in Session**. The teal banner confirms name, rarity, tier, category, source type, and description, then leaves Scene notes, acquisition, crafting, use, and inventory entirely GM-resolved.

**Smoke pending:** Browser-check a dropped and a crafted item preview with the pending saved-list, spell, Bestiary, POI/haven, and Generator handoffs when attachment is available. Browser attachment remains non-blocking.

**Boundary:** No inventory or RP-spend automation, source-table change, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending owner direction.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~41s). The two existing non-fatal `SessionTracker` exhaustive-deps warnings remain.

---

## Wave 111 midnight stamp — Character Sheet printable draft-badge parity (2026-07-30)

**Status:** Prestige hallmark and capstone draft markers now share the Character Sheet’s printable **Draft** badge. Print preview retains the same provenance labels shown on screen; existing prestige content and mechanics are unchanged.

**Smoke pending:** Use the appended Sheet print-preview row alongside the Wave 109 active-turn and Wave 110 Session recovery rows when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No prestige data, source tables, character storage, Session behavior, inventory/RP/cast automation, encounter resolution, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 111 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 112 midnight stamp — Session dismissal confirmation (2026-07-30)

**Status:** Dismissing stacked local arrival notices now produces an accessible count confirmation that explicitly preserves Scene notes, combatants, tier, horn time, turn, round, and resources. A later existing Session handoff clears the stale confirmation so the new arrival remains the visible current state.

**Smoke pending:** Run the appended dismissal-confirmation/new-arrival-reset rows with Waves 109–111 when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No handoff payload outcome, table state, character storage, inventory/RP/cast automation, encounter resolution, source table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 112 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 123 midnight stamp — Hero-path reference clarity (2026-07-30)

**Status:** Builder and Sheet/print now replace an otherwise blank hero-path area with a source-bounded note when the existing class reference contains no hero-path entries. Existing arch-path content remains visible; no path or progression outcome is inferred.

**Smoke pending:** The appended smoke rows cover the Hero-path Builder → save → Sheet/print path and Wave 122’s Cosmology **Draft extract** notice before selection. Browser execution remains non-blocking.

**Coffee queue:** Master Tracker canonical record/type; Oracle/Paladin/Umbrin tone; Resonance multiclass draft; Drow → Umbrin re-ingest. No author review was performed.

**Boundary:** No class/path source, progression, save, Cosmology, dungeon, Session, inventory/RP/cast automation, content table, or mapped T6–T10 material changed. No deletion or commit occurred; `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 123 typecheck and production build.

### Validation update

`npx tsc --noEmit` passed; `npm run build` passed in ~41s. Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 122 midnight stamp — Cosmology draft-extract visibility (2026-07-30)

**Status:** The existing Cosmology draft batches are now visibly announced before selection in both lore pickers. Wave 121’s feat no-match and People & traits Sheet/print paths have a combined smoke addendum; browser execution remains non-blocking.

**Boundary:** No cosmology/dungeon source material, content table, T6–T10 mapped material, feat/people/trait/class/Resonance/save rule, Session behavior, inventory/RP/cast automation, encounter resolution, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** `npx tsc --noEmit` passed; `npm run build` passed in ~42s with only the two intentionally deferred `SessionTracker` exhaustive-deps warnings. No commit created.

---

## Wave 121 final midnight stamp — Hero-state clarity (2026-07-30)

**Status:** Existing feat data now has a reachable zero-result recovery in Builder, and existing saved people/lineage data now has print-safe trait visibility on Sheet. The owner checklist is appended to the handoff; author tone and Resonance decisions remain deferred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (~51s). Only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` warnings remain; no commit created.

---

## Wave 121 midnight stamp — Hero-state clarity + coffee checklist (2026-07-30)

**Status:** Builder Feats now supports a zero-result recovery using its existing feat data, and the printable Sheet now makes saved people/lineage traits visible without inferring effects. The morning handoff now appends the three owner decisions needed before new canon or author-tone work: Master Tracker canonical record, Oracle/Paladin/Umbrin tone, and the Resonance multiclass draft.

**Smoke pending:** Run the appended no-match feat search and Builder → save → Sheet/print people-trait rows when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No feat, people, trait, class, Resonance, storage, Session, inventory/RP/cast automation, encounter, source-table, cosmology, or dungeon rule changed. No content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 121 typecheck and production build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 120 midnight stamp — Oracle recorded-state parity (2026-07-30)

**Status:** Oracle Paths now names blank saved selection state for both **Mystery** and **Oracle's Curse** without changing their content: **No Oracle Mystery recorded** / **No Oracle's Curse recorded**. The printable Sheet repeats each L1-required blank state and retains the existing **Draft** badges and Builder recovery route.

**Smoke pending:** Run the appended Wave 120 blank-both and one-recorded-selection Builder → save → Sheet/print rows alongside the Wave 118–119 recorded-state rows when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No Mystery/Curse source data, Oracle rules, revelations, boons, storage semantics, progression, Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 120 typecheck and production build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~49s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 119 midnight stamp — Sacred Oath recorded-state parity (2026-07-30)

**Status:** Paladin Paths now identifies an unselected existing `sacredOath` as **No Sacred Oath recorded** and preserves the known L3 timing. The Character Sheet and print use the same blank-state language while keeping the required-at-L3 marker and the existing Builder recovery path.

**Smoke pending:** Run the appended Wave 118 Ethos and Wave 119 Sacred Oath blank → save → Sheet/print rows when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No oath source data, oath rules, class features, storage semantics, progression, Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 119 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~55s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 118 midnight stamp — Ethos recorded-state parity (2026-07-30)

**Status:** Builder now explains an unselected Ethos using only its existing saved-state and spell-cost-preview role. The printable Character Sheet always exposes that state: it shows **Ethos not recorded** until a saved value exists, then shows the existing selected value.

**Smoke pending:** Run the appended blank → save → Sheet/print and selected → save → Sheet rows when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No ethos source table, spell-cost rule, character-storage shape, class, feature, Resonance, Session behavior, inventory/RP/cast automation, encounter resolution, content table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

**Validation:** Pending Wave 118 typecheck and build.

**Suggested wave 119:** Browser-smoke Waves 116–118 when available. Otherwise, take one further source-bounded Builder clarity gap using an existing saved state only.

### Validation update

`npx tsc --noEmit` passed. `npm run build` passed in ~42s; production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 117 midnight stamp — Sheet prestige-path intent parity (2026-07-30)

**Status:** The existing saved Arch-path selection now carries the same intent-only boundary onto the printable Character Sheet: it records intended direction and does not grant prerequisites or features. Existing requirements and draft badges remain visible.

**Smoke pending:** Run the appended Builder → Sheet → print check when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No prestige source data, prerequisite, feature, class, Resonance, character-storage rule, Session behavior, automation, encounter resolution, content table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

**Validation:** `npx tsc --noEmit` passed; `npm run build` passed in ~41s, reporting only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings.

**Suggested wave 118:** Browser-smoke Wave 117 when attachment is available. Otherwise, keep work to one source-bounded Builder clarity gap using existing saved state.

---

## Wave 116 midnight stamp — Prestige-path intent clarity (2026-07-30)

**Status:** Selecting an Arch path in Builder’s **Class** tab now clearly records intended progression only. The notice directs the player to the existing **Paths** detail for requirements and draft markers and states that selection does not grant prerequisites or features.

**Smoke pending:** Run the appended Class → Paths check alongside Wave 114–115’s Builder → Sheet → print rows when browser attachment is available. Browser work remains non-blocking.

**Boundary:** No prestige source data, prerequisites, features, class/Resonance/storage rule, Session behavior, inventory/RP/cast automation, encounter resolution, source table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two existing `SessionTracker` hook warnings remain deferred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~49s); production build repeats only the two existing `SessionTracker` exhaustive-deps warnings.

---

## Wave 115 midnight stamp — Sheet print continuity (2026-07-30)

**Status:** Character Sheet print output now keeps the existing draft Multiclass Resonance merge callout intact, carries the no-second-Weave-pool boundary for recorded secondary classes, and makes the level-feature draft legend/badges print-legible.

**Smoke pending:** Run the appended Wave 115 print-preview checks with Wave 114’s Builder secondary-class and selected-feat paths when browser attachment is available. Browser work remains non-blocking.

**Boundary:** No class, feature, Resonance, or storage rule changed. No inventory/RP/cast automation, Session behavior, source table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 115 `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 114 midnight stamp — Builder secondary-class clarity + printable feat provenance (2026-07-30)

**Status:** Builder now distinguishes a recorded secondary class that adds no eligible second Weave pool from existing multiclass pairs that use the draft RP merge panel. Draft feat badges now follow the selected feat through Builder’s Chosen feats list and onto the printable Character Sheet.

**Smoke pending:** Run the appended non-Weave-secondary / eligible-merge and feat-card-to-print-preview rows, alongside the pending Wave 109–113 Session rows, when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No feat/class/Resonance source rules, character-storage schema, Session state, inventory/RP/cast automation, encounter resolution, source table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 114 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~42s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 113 midnight stamp — Session filtered-table recovery (2026-07-30)

**Status:** A populated Session table whose selected Allies/Foes view has no matches now provides an in-place recovery message and **Show all combatants**. That action changes only display state and expands the existing foes view; table data and current context remain intact.

**Smoke pending:** Run the appended empty-Foes-view and state-preservation rows with Waves 109–112 when browser attachment is available. Browser execution remains non-blocking.

**Boundary:** No handoff payload outcome, combatant data, initiative, turn/round, Scene notes, tier, horn time, resources, character storage, inventory/RP/cast automation, encounter resolution, source table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 113 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave midnight stamp — Umbrin migration (2026-07-30)

**Status:** Rulebook edits are now authorized. `rulebook_output.txt` is the living editable extract; its Umbrin chapter replaces 38 Drow-era references with product canon and removes legacy external names. The current chapter retains existing mechanics, uses Murkish / Umbrin Magic / Obsidian Highborn, and flags the Calan'thir–First Choir Obsidian Burn origin for author review.

**Pending author review:** Obsidian Burn motive and theology; Umbrin name list; Murk cult terminology; subsequent Oracle or Paladin draft promotion.

**Boundary:** No companion code or active data changed. Legacy save migration aliases are retained intentionally. No content tables, T6–T10 mapping, inventory automation, Session hook work, deletion, or commit occurred.

---

## Rulebook wave midnight stamp — Oath of Grief tone pass (2026-07-30)

**Status:** `rulebook_output.txt` remains the editable living source. The full player-rulebook docx is present but was not edited; approved Umbrin Peoples copy still needs a dedicated sync pass.

**Delivered:** Draft **Oath of Grief** prose now frames its conduct and summaries around remembrance and the duty of passage. No mechanics, revelation spells, numbers, or draft status changed.

**Pending author review:** Oath of Grief promotion, Obsidian Burn theology, Umbrin names, Murk-cult terms, and docx synchronization. No deletion or commit occurred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings.

---

## Rulebook wave midnight stamp — docx assessment + Oath of the Chain (2026-07-30)

**Docx:** `python-docx` is installed and the player-rulebook docx is present, but no safe paragraph-scoped, backup-and-compare edit path is available here. The docx is unchanged; `rulebook_output.txt` remains the living Umbrin extract and the sync is explicitly deferred.

**Delivered:** Draft **Oath of the Chain** received a bounded rulebook-voice pass for its theme and vows. Mechanics, revelation spells, numeric values, final gift, and `draft: true` remain unchanged.

**Next:** Sync the docx only through a guarded backup → targeted Peoples replacement → fresh extract → chapter diff workflow, then author-review the Oath before any promotion.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. Production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook midnight stamp — guarded Umbrin docx sync (2026-07-30)

**Status:** The full player-rulebook docx is now synchronized to the living Umbrin extract. A pre-sync backup is stored beside it as `decennium descent player rulebook.pre-umbrin-backup.docx`.

**Delivered:** Targeted Peoples/rulebook replacements use **Umbrin**, **The Murk**, **Murkish**, **Umbrin Magic**, and **Obsidian Highborn**. The provisional Obsidian Burn account is explicitly author-review-only and grants no mechanic.

**Verification:** The saved docx reopened with `python-docx`; the post-save scan has zero whole-word Drow hits. The unrelated “drowsy” word remains. No companion code, mechanics, Oracle/Paladin draft status, broad deletion, or commit changed.

**Next:** Resolve Obsidian Burn theology and Umbrin names before expanding the People. If selecting an Oracle mystery tone pass, preserve `draft: true`.

---

## Rulebook midnight stamp — Cataclysm Oracle mystery tone pass (2026-07-30)

**Status:** Draft **Cataclysm** now has a bounded rulebook-voice pass across its profile and existing **The Unbound Wound** capstone. The prose presents destruction as a dangerous route through an untenable position; all established rules remain intact.

**Boundary:** No charge cost, range, area, duration, damage, immunity, Exhaustion, patron, other Revelation, curse, Umbrin lore, Obsidian Burn theology, or name list changed. Cataclysm remains `draft: true`; no deletion or commit occurred.

**Author queue:** Review the complete Cataclysm draft tree before any promotion. Obsidian Burn theology and Umbrin naming examples await author direction.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook midnight stamp — Life + Stars Oracle mystery tone pass (2026-07-30)

**Status:** Draft **Life** and **Stars** now have bounded rulebook-voice profile passes. Life centers preservation through a hard fight; Stars centers difficult foresight made usable at the moment a battle turns. Both retain `draft: true`; their Revelation trees and all mechanics are unchanged.

**Handoff:** The previous queue stated 8 untouched profiles, but the source/profile audit now identifies 7 without a recorded tone pass: **Battle, Bones, Shadow, Time; Oath of Dominion, Oath of Flame, Oath of the Ancients**. Reconcile that one-profile discrepancy before declaring the queue complete.

**Boundary:** No Obsidian Burn theology, Umbrin naming, promotion, deletion, or commit occurred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook midnight stamp — Oracle curse tone pass (2026-07-30)

**Status:** All nine draft Oracle curse profiles now carry bounded rulebook voice in their blurbs and limitations. **Spiral-Touched** remains the only rulebook-complete curse tree; **9** draft curse trees remain drafts after this pass.

**Boundary:** No curse mechanic, boon, unlock, value, cost, range, duration, damage, or `draft: true` status changed. No Obsidian Burn theology, Umbrin name list, promotion, deletion, or commit occurred.

**Handoff:** The curse tone-pass queue is **0 remaining**. Coffee review still needs author decisions on Obsidian Burn theology, Umbrin names, the Master Tracker duplicate, and the Resonance multiclass draft; promote only individually approved drafts.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook midnight stamp — final five-profile tone pass (2026-07-30)

**Status:** Draft **Battle** and **Bones** now carry bounded rulebook voice for service on the battle line and care owed to the dead. Draft **Oath of Dominion**, **Oath of Flame**, and **Oath of the Ancients** now carry the same treatment for accountable authority, restrained cleansing, and humble protection of living memory.

**Boundary:** Battle/Bones changed only theme, combat role, and reputation; their patrons, full Revelation trees, values, costs, ranges, durations, damage, progression, and shared `draft: true` provenance remain unchanged. The Oaths changed only theme, conduct clauses, and draft source wording; their mechanics, revelation spells, oathbreaker text, final gifts, values, selection timing, and explicit `draft: true` remain unchanged. No Obsidian Burn theology, Umbrin names, promotion, deletion, or commit occurred.

**Handoff:** The reconciled tone-pass queue is **0**. Next, wait for Umbrin lore author blockers to resolve, then take the independent curse-tone review. Run the coffee checklist before the next prose wave to confirm draft labels, author-only lore boundaries, and mechanics preservation.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook midnight stamp — Oath of the Martyr King + Flame mystery tone pass (2026-07-30)

**Status:** Draft **Oath of the Martyr King** now uses bounded rulebook voice for stewardship, responsibility, and sacrifice freely borne before it is asked of another. Its smite, aura, signature power, revelations, oathbreaker text, final gift, numeric values, and `draft: true` status are unchanged.

**Thin follow-up:** Draft **Flame** now has a compact rulebook-voice profile pass for conviction, costly mercy, battlefield purpose, and public reputation. Its patron, full Revelation tree, charges, ranges, durations, damage, and inherited `draft: true` status remain unchanged.

**Boundary:** No Obsidian Burn theology, Umbrin names, mechanic, promotion, deletion, or commit occurred.

**Author queue:** **10** untouched draft Mystery/Oath profiles remain. Suggested next bounded pass: **Oath of Mercy** or **Oath of Vengeance**; retain `draft: true`.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook midnight stamp — Oath of Chains Broken tone pass (2026-07-30)

**Status:** Draft **Oath of Chains Broken** now speaks in bounded rulebook voice about breaking unjust bonds, refusing replacement tyranny, and safeguarding the newly free. Its smite, aura, signature power, revelation spells, oathbreaker text, final gift, all numbers, and `draft: true` status are unchanged.

**Cataclysm note:** A direct source spot-check against the workspace's `rulebook_output.txt` is pending. No contradiction, promotion, or new rulebook assertion has been inferred.

**Author queue:** **14** untouched draft Mystery/Oath profiles remain. Suggested next bounded pass: **Oath of Silence**. Obsidian Burn theology and Umbrin names remain pending author direction.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`; no deletion or commit occurred.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. Production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` warnings; no commit created.

**Cataclysm spot-check update:** `rulebook_output.txt` supports Cataclysm’s destruction/upheaval/instability theme, area-control combat role, and feared reputation. Its only full Mystery tree is Ancestor, so Cataclysm remains draft; no contradiction found.

---

## Rulebook midnight stamp — Oath of Silence + Dream mystery tone pass (2026-07-30)

**Status:** Draft **Oath of Silence** now uses bounded rulebook voice for humble restraint and careful judgment. Its smite, aura, signature power, revelations, oathbreaker text, final gift, numeric values, and `draft: true` status are unchanged.

**Thin follow-up:** Draft **Dream** now has a compact rulebook-voice profile pass for its theme, battlefield role, and public reputation. Its patron, full Revelation tree, charges, ranges, durations, and inherited `draft: true` status remain unchanged.

**Boundary:** No Obsidian Burn theology, Umbrin names, mechanic, promotion, deletion, or commit occurred.

**Author queue:** **12** untouched draft Mystery/Oath profiles remain. Suggested next bounded pass: **Oath of the Martyr King** (or one remaining Mystery profile); retain `draft: true`.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook midnight stamp — Oath of Mercy + Oath of Vengeance tone pass (2026-07-30)

**Status:** Draft **Oath of Mercy** now carries bounded rulebook voice for shelter, healing, and the charge to spare life where protection remains possible. Draft **Oath of Vengeance** now carries the same treatment for disciplined pursuit, sworn judgment, and a genuine surrender honored without deserting allies.

**Boundary:** Their smites, auras, signature powers, revelation spells, oathbreaker text, final gifts, numeric values, and selection timing are unchanged. Both profiles retain `draft: true`. No Obsidian Burn theology, Umbrin names, promotion, deletion, or commit occurred.

**Author queue:** **8** untouched draft Mystery/Oath profiles remain. Suggested next bounded pass: the thinnest remaining Oracle Mystery; retain `draft: true` and review each completed tree before promotion.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook midnight stamp — Shadow + Time Oracle mystery tone pass (2026-07-30)

**Status:** Draft **Shadow** now carries bounded rulebook voice for disciplined silence, concealment, and fear used to control a dangerous moment. Draft **Time** now frames delay and reversal as measured intervention: making enough room for an ally to act without treating causality as consequence-free.

**Boundary:** Only the profile fields for theme, combat role, and reputation changed. Their patrons, complete Revelation trees, costs, ranges, durations, damage, numeric values, and shared `draft: true` provenance remain unchanged. No Obsidian Burn theology, Umbrin names, promotion, deletion, or commit occurred.

**Handoff:** The reconciled seven-profile queue is now **5**: **Battle, Bones; Oath of Dominion, Oath of Flame, Oath of the Ancients**. Take **Bones** next for the remaining Oracle profile, then review each completed draft tree before any promotion.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.