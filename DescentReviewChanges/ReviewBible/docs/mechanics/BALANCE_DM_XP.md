# DM balance audit — XP, CR, and encounters

**Audit date:** 2026-07-30  
**Scope:** Rulebook material available in this workspace; Bestiary, Floor Encounters, Generator, and Session surfaces.  
**Status:** [`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md) confirms the L1–L20 cumulative XP thresholds and total-level multiclass rule from the editable player-rulebook docx. It does **not** establish XP awards, CR-to-XP, encounter budgets, or party-size adjustments. Do not infer those missing rules from companion UI values.

## 1. XP: source rules versus companion behavior

### Rulebook-supported position

The editable player rulebook confirms XP-based level advancement and publishes cumulative L1–L20 thresholds. It also makes XP cost depend on total character level for multiclass characters.

No reviewed source establishes:

- XP awards for creatures, goals, hazards, exploration, or gate bosses;
- sharing/splitting rules, level disparity adjustments, or awards for defeated versus bypassed foes;
- a CR-to-XP table; or
- encounter difficulty, encounter budgets, or party/rest adjustments.

The Oracle extract does use “once per encounter/day” language for class abilities, but it establishes no general encounter or XP procedure. These are author-source holes, not values for a DM to reverse-engineer.

### What the companion currently does

| Surface | Current behavior | DM meaning |
|---|---|---|
| Character Builder → Advancement | Stores a free numeric `xp` field. Its level +/- controls set XP to the hard-coded 1–20 thresholds: 0, 500, 1,500, 3,000, 5,500, 9,000, 13,500, 19,000, 25,500, 33,000, 42,000, 53,000, 66,000, 82,000, 101,000, 124,000, 151,000, 182,000, 217,000, 256,000. | **Legacy-unverified and in conflict with the confirmed rulebook table.** It does not calculate or award XP. Manual level changes overwrite the field with the selected level’s threshold. |
| Character Sheet | Displays the saved XP number. | Display only. |
| Bestiary | Each record has an `xp` field and displays it beside CR in the library. | Reference/display only. The source relationship between CR and XP is not documented by the available rulebook extract. |
| Bestiary → Session | Handoff sends name, listed HP, CR, and zone only. | Monster XP is discarded; Session cannot total, split, or award it. |
| Session | Has no XP state, award control, encounter XP total, character XP write-back, or level-up workflow. | Award and progression remain entirely table-facing. |

**Important distinction:** the UI’s advancement thresholds and Bestiary `xp` values may be useful legacy reference data, but neither is evidence of the game’s intended XP system until an XP/advancement rulebook chapter is ingested and reconciled.

## 2. Encounter building and CR guidance available now

### Bestiary

- The Bestiary supports filtering/searching by listed CR, creature type, size, zone, and a derived “tier zone.”
- Its tier-zone filter maps CR bands mechanically: CR ≤2 → T1, ≤4 → T2, then two CR per tier through ≤18 → T9, and CR >18 → T10.
- This is a browse/filter heuristic in `MonstersLibrary`, not a documented party-level encounter budget or a floor encounter rule.
- The library displays each monster’s listed CR and XP, but provides no party-size, party-level, action-economy, terrain, rest, or multi-foe adjustment.

### Floor Encounters and generators

- `floor-encounters.json` supplies tier identity, floor bands, difficulty labels, gate-boss names, safe havens, and points of interest.
- T1–T5 are mapped as location/reference material; T6–T10 explicitly carry draft/rumor notes and are `mapped: false`. Their route details, hazards, maps, and encounter resolution are unconfirmed.
- `EncountersBrowser` can hand off a tier brief, a chosen site, and a fallback haven. It does not select creatures, calculate CR, generate a balanced roster, attach rewards, or award XP.
- Generator encounter packs supply scene prompts/briefs, not a budgeted creature roster or resolution procedure.

### Session

- Session accepts Bestiary foes, manual enemies, and tier gate bosses; it provides initiative, HP, conditions, notes, horn time, and table-facing resource tracking.
- A Bestiary foe preserves source name, listed/stat-block HP, CR, and zone in notes. CR is not used for math after import.
- A manually added enemy receives `20 + tier × 8` HP. A gate boss receives the explicit placeholder `40 + tier × 25` HP. Neither formula is CR-, XP-, party-, or source-stat-based.
- Session explicitly labels gate-boss HP as a stub and directs the DM to pull an actual Bestiary record when one exists.

## 3. Gaps and continuity risks

1. **XP advancement is only partially source-backed.** Level thresholds and total-level advancement are confirmed, but award triggers, values, sharing, CR conversion, and encounter math are unavailable. The companion must not imply its conflicting hard-coded thresholds are canon.
2. **No XP workflow.** Session neither records encounter awards nor distributes them to saved characters; Bestiary XP does not cross the handoff boundary.
3. **No encounter calculator.** There is no party-level/size input, CR aggregation, difficulty target, multiplier, daily/rest budget, or post-build validation.
4. **CR tier mapping is only a UI heuristic.** The two-CR-per-tier mapping is not source-backed and does not account for party level, creature count, abilities, terrain, or boss design.
5. **Floor Encounters are location briefs, not encounter plans.** Even mapped tiers do not connect POIs or gate bosses to a creature roster, CR target, reward, or resolution rule.
6. **Gate bosses have no verified stat blocks or budgets.** Session’s `40 + tier × 25` is visibly a placeholder and should never be used as an encounter balance recommendation.
7. **T6–T10 are unmapped.** Their haven/POI/boss labels are GM-improv seeds only; there are no confirmed routes, hazards, maps, procedures, rewards, or encounter-resolution rules.
8. **Bestiary data needs source validation before automation.** The companion can display CR/XP and import listed HP, but their provenance and completeness are not established by the available rules extract.

## 4. Recommended DM tools, in dependency order

1. **Ingest CR/encounter award rules from the rulebook.** Builder Advancement already uses confirmed L1–L20 thresholds (`CANON_XP_THRESHOLDS` in `xp-economy.js`). Do not ship an award or encounter calculator before CR/award rules are sourced.
2. **Keep explicit “unverified legacy data” boundaries.** Bestiary XP, CR-tier filtering, gate-boss HP, and all CR-based simulation proxies remain unverified; label them so they are not mistaken for confirmed DM rules.
3. **Build a source-backed encounter worksheet.** Inputs: party members and levels, target difficulty, creature roster, and relevant modifiers. Outputs: only the calculations and caveats actually stated by the source.
4. **Wire an award ledger after the source is settled.** Start with a Session-local proposed award, per-character split/override, confirmation, and explicit write-back to saved character XP. Preserve manual GM awards for noncombat goals if the source supports them.
5. **Promote Floor Encounters from briefs to encounter cards only when authored.** Each card needs a source-backed creature roster or substitute rule, terrain/hazard procedure, success/failure consequence, reward/XP guidance, and a mapped/draft status.
6. **Replace gate-boss HP stubs with linked, source-validated stat blocks.** If no stat block exists, retain the GM-facing stub label rather than inventing CR, XP, attacks, or rewards.

## 5. Smoke checklist — XP and encounter to Session

Use this after any XP or encounter-tool change. It supplements [`PLAYTEST_SMOKE.md`](./PLAYTEST_SMOKE.md); it does not authorize a DM to use unverified values as rules.

### Current companion boundaries

- [ ] In **CHARACTERS**, confirm the Advancement panel shows a manually editable XP field and its 1–20 threshold display.
- [ ] Change level with +/- and confirm the XP field resets to that displayed threshold; record that this is a UI behavior, not a validated award.
- [ ] Save and reload the character; confirm the same XP number persists and the Sheet displays it.
- [ ] In **BESTIARY**, select a creature and confirm CR and listed XP are visible as reference fields.
- [ ] Use **Add foe in Session**. Confirm the foe arrives once with source HP and notes containing CR and zone; confirm no XP total or award control appears.
- [ ] In **ENCOUNTERS**, load a mapped tier/site/haven into Session. Confirm tier and scene notes transfer, but no monster roster, CR budget, XP award, or reward is claimed.
- [ ] Add a gate boss. Confirm it is labelled as tier-scaled **stub HP** and does not claim a CR, XP award, or balanced encounter.
- [ ] Repeat the Floor Encounters handoff for T6–T10. Confirm the draft/unmapped warning remains visible and no procedure, route, hazard, map, reward, or encounter resolution is implied.

### Acceptance checks for a future source-backed tool

- [ ] The tool cites the exact ingested XP/CR source section for every table/formula it uses.
- [ ] Party composition and encounter roster are both visible before a difficulty result is shown.
- [ ] The result distinguishes source rule, GM override, and unresolved/draft data.
- [ ] Awarding XP shows the total, split/override, affected saved characters, and write-back confirmation.
- [ ] Noncombat awards, if supported by the source, are not silently omitted.
- [ ] Bestiary handoff preserves the fields required by the calculator; Session retains an audit trail without fabricating missing stats.

## Evidence map

- Confirmed advancement source: `decennium descent player rulebook.docx`, Chapter 1 / **Beyond 1st Level** and **Character Advancement**; mirror extraction: `rulebook_output.txt` lines 80–128. See [`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md).
- Missing XP-award/CR/encounter source: `tools/oracle_rulebook_extract.txt` is Oracle-only; no reviewed source supplies award, CR-to-XP, or budget rules.
- XP field and hard-coded thresholds: `src/components/CharacterBuilder.tsx`.
- Bestiary CR/XP display and CR-to-tier filter heuristic: `src/components/MonstersLibrary.tsx`, `src/bestiary_data_full.json`.
- Floor encounter status and T6–T10 draft boundary: `src/data/floor-encounters.json`, `src/components/EncountersBrowser.tsx`.
- Handoff payloads and Session behavior: `src/lib/session-handoff.ts`, `src/components/SessionTracker.tsx`, `src/lib/session-utils.ts`.
- Existing handoff smoke and dungeon/session boundaries: [`PLAYTEST_SMOKE.md`](./PLAYTEST_SMOKE.md), [`SESSION_LOOP.md`](./SESSION_LOOP.md), [`WORLD_DUNGEON_LOOP.md`](./WORLD_DUNGEON_LOOP.md), `src/data/CONTINUITY_GLOSSARY.md`.
