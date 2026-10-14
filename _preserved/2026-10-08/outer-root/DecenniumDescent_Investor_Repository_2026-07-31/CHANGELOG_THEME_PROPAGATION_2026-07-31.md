# Theme Propagation & Investor Repository Pass — 2026-07-31

This pass applies the current Decennium Descent canon across the product and turns the working repository into a compact investor/development package.

## 1. Core canon propagated

- Preserved the public Crucible tradition: Calan'thir and Asmodeus genuinely built and governed the known Crucible.
- Preserved the deeper Director truth: the Heartcell predates the Crucible and was created by the Silent Ones / Old Ones.
- Added the Matrix of Oblivion as an explicit Director design grammar: Possibility → Choice → Difference → Conflict → Motion → Time → History → Memory → Identity → Will → Life.
- Added Director guidance that players should experience the Matrix before they can name it.
- Added Unity / false resonance as counterfeit harmony that destroys meaningful distinction rather than ordinary peace itself.
- Added explicit guardrails against treating ordinary peace, equality, banks, guilds, or collective institutions as automatic Unity vectors.

## 2. Goblin canon integrated at the correct information layer

### Player layer
- Reframed goblins as survivors, brokers, builders, financiers, insurers, expedition backers, and institutional actors.
- Added goblin involvement in the Aethel banking conglomerate and Decennial expedition finance.
- Added the ancient anti-goblin crusade as disputed history with incompatible surviving interpretations.
- Preserved goblin internal diversity, reformers, dissidents, and distrust of concentrated obligation.

### Director layer
- Added goblins' elevated metaphysical susceptibility to Unity.
- Explicitly separated susceptibility from morality, guilt, or universal complicity.
- Added Moloch's Coinfather pattern: value → surveillance; obligation → identity; prosperity → dependency.
- Preserved the difficult crusade question: crusaders may have recognized a genuine existential vector without making collective extermination morally or factually equivalent to universal goblin culpability.

## 3. Player Rulebook aligned to the setting

- Added **Peoples of the Opening**, tying all fourteen peoples to the Decennial cycle rather than presenting them as generic fantasy cultures detached from the central premise.
- Standardized current underground terminology around **Umbrin** and the **Murk**.
- Removed the orphan Fighter chapter and made the **17 selectable base-class** roster authoritative.
- Added **Hero Paths Are Philosophies, Not Moral Verdicts**.
- Removed Good / Neutral / Evil labels from Hero Path headers while retaining path identity and consequences.
- Standardized the Player Rulebook on **Director** instead of mixing DM, GM, and Game Master language.
- Replaced remaining named legacy spells and external-rulebook references with Aethel-neutral language.
- Reframed player cosmography as mortal interpretation rather than omniscient objective truth.
- Renamed major inherited planar labels in player-facing material, including **Wheel of Testimony**, **Verdant Reflection**, **Veiled Expanse**, and the **Nine Infernal Courts** family of terminology.
- Cleaned several obvious inherited proper names from racial naming examples.

## 4. Resonance architecture consolidated

- Weave casters now consistently use **Resonance Points** where the current rules call for them.
- Oracle remains a deliberate exception using **Revelation Charges**.
- Legacy spell-slot wording was removed from relevant class features, recovery rules, prestige/capstone language, and multiclass explanations.
- Mirrorsage storage terminology remains distinct where a "slot" is a literal storage mechanic rather than a casting resource.

## 5. Director book expanded

Added or strengthened:

- **The Matrix as an Invisible Design Language**
- **False Resonance and Unity**
- **The Goblin Question**
- **Moloch and the Coinfather Pattern**
- public-vs-secret cosmology boundaries
- conflict/war-as-dissonance guardrails that deny cosmic function as moral absolution
- Wheel of Testimony language for mortal planar models

## 6. Bestiary naming and publication-status cleanup

- Propagated Aethel naming across canonical Excel sources, generated JSON, Bestiary, and Codex.
- Removed targeted high-recognition legacy identifiers and half-reskinned family/rank names.
- Finalized Aethel rank naming including:
  - Hush-Broker Scriptor / Chainmaw / Manyclaw / Mirefin / Spearbound / Dreadwing / Plaguehand / Longarm
  - Order-Drone Unit / Pair / Triad / Tetrad / Quintet / Covenant Engine
  - Spiral Breach Gnawer / Brood-Sage / Ripper / Colossus / Augur
- Updated the defensive scrub script so repeated runs do not reintroduce doubled prefixes.
- Verified the two bestiary workbooks contain no targeted retired rank names, doubled prefixes, or spreadsheet formula-error strings.
- Added `docs/development/BESTIARY_PUBLICATION_STATUS.md`.
- Corrected the Bestiary and Codex so they no longer imply that compatibility/prototype creature shells are already final commercial publication copy.

**Important:** the bestiary pipeline is intentionally still a development scaffold. Many ordinary creature concepts/stat shells need a full independent authorship/provenance/publication pass. The investor repository now says this explicitly instead of overstating completion.

## 7. Repository cleanup

The extracted working repository was reduced from roughly **919 MB** to roughly **13 MB** while retaining the current books, canon, mechanics, structured source data, app source, maintained tooling, and curated playtest evidence.

Removed from the distributable package:

- `node_modules/`
- `.next/`, `out/`, generated local builds
- approximately 163 MB of third-party D&D/Pathfinder reference PDFs
- private/local backups and pre-edit Word files
- redundant modular Word documents already compiled into current books
- superseded Director drafts
- completed one-off migration/patch scripts
- raw temporary analysis output
- stale generated fragments and obsolete content generators
- Python cache folders

The remaining repository contains **215 files** before ZIP packaging.

## 8. Investor/navigation documents added or rewritten

- `README.md`
- `INVESTOR_OVERVIEW.md`
- `REPOSITORY_GUIDE.md`
- `docs/CURRENT_SYSTEM_STATUS.md`
- `docs/canon/CANON_CORE.md`
- `docs/canon/UNITY_FALSE_RESONANCE.md`
- `docs/canon/THEMATIC_DESIGN_LANGUAGE.md`
- `docs/canon/PLAYER_DIRECTOR_BOUNDARY.md`
- `docs/development/BESTIARY_PUBLICATION_STATUS.md`
- consolidated mechanics/source-of-truth references

## 9. Engineering and integrity checks

- TypeScript `tsc --noEmit` passed before dependency-cache removal.
- Final repository intentionally omits `node_modules`; fresh verification requires `npm ci`.
- Production Next.js build could not complete in the packaging sandbox because the package mirror returned 404 while Next.js attempted to retrieve its Linux SWC binary.
- Markdown relative-link audit: **0 missing links**.
- Maintained `scripts/` / `tools/` reference audit: **0 missing referenced paths**.
- Bestiary source ingest: **708 Excel rows / 707 live JSON rows / 1 hidden row skipped**.
- Targeted Player/Director/Cosmology/Bestiary/Codex terminology scan completed after edits.

## 10. Document render QA

Latest edited books were rendered through the DOCX QA workflow. Complete PDFs were produced for the Player Rulebook, Director's Crucible, Chronicle, Cosmology, Bestiary, and Codex. Large Player/Codex PNG rasterization exceeded the sandbox time limit after the PDFs had already completed; targeted pages from the completed PDFs were then rendered and visually inspected.

Inspected sections included:

- Player character-creation Director terminology
- Peoples of the Opening
- dwarf naming cleanup
- goblin finance/crusade rewrite
- Hero Path philosophy statement
- Wheel of Testimony / planar cosmography
- Matrix design language
- Unity / false resonance
- Goblin Question and Moloch pattern
- Bestiary publication-status cover
- Codex publication-status cover and naming/source-hygiene section

No clipping or overlap was found in the inspected edited sections.

## 11. Protected open canon questions

This pass does **not** invent answers to intentionally unresolved canon, including:

- the exact relationship of the Level 97 Old God encounter to the Silent Ones beyond current locks;
- the precise threshold at which peace/stillness becomes existentially dangerous;
- any still-open authorship detail the current canon briefs explicitly preserve as unresolved.

Those remain development questions rather than accidental contradictions.
