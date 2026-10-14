# Floor 1–100 Task Force — Master stamp

**Date:** 2026-07-31  
**Role:** Integration spine (continuity + product polish)  
**Workspace:** `DecenniumDescent-main`  
**Commit:** none  
**Update protocol:** Re-read sibling stamps below when they land; flip Expected → Actual; re-run §4 continuity checklist.

---

## 0. Master verdict (this snapshot)

| Slice | Readiness | Notes |
|-------|-----------|-------|
| **Tier 1–5 campaign product** | **~92–95%** table-ready | All T1–5 packages + continuity PASS; ship polish = `out/` rebuild |
| **Floor 1–100 full product** | **~85–90%** | All sibling tracks DONE (rules, setting, encounters, bestiary T6–10); floors still `mapped: false`; Q6 / peace-trigger / Interstice flesh open |
| **Honest ship label today** | **“Full Opening runnable with Director ops + toolkits + trusted bestiary; deep floors not room-mapped; endgame authorship open”** | Freeze ship still needs `out/` rebuild + owner Q6 / peace-trigger for endgame |

**Closest path to “full 1–100”:** (1) owner answers Q6 / peace-trigger, (2) optionally flesh Interstice beyond stub, (3) promote `mapped: true` when room keys exist, (4) rebuild companion `out/`.

---

## 1. Sibling track board

| Track | Expected stamp | Status (2026-07-31 integration pass) | Actual / notes |
|-------|----------------|--------------------------------------|----------------|
| **T1–5 Rules** | `T1_5_RULES_PACKAGE_2026-07-31.md` | **DONE** | Milestone Opening; DM-01; Q-OV-4 closed; Burnout/ceilings GM fiat |
| **T1–5 Encounters** | `T1_5_ENCOUNTERS_2026-07-31.md` | **DONE** | Toolkit JSON + MD; T6–10 out of scope |
| **T1–5 Bestiary** | `T1_5_BESTIARY_COMBAT_2026-07-31.md` | **DONE** | 159 trusted at T1–5 stamp; superseded totals in live JSON (see §3) |
| **T1–5 Crafting** | `T1_5_CRAFTING_COMPONENTS_2026-07-31.md` | **DONE** | 623 filled; 218 needsReview |
| **Continuity (books)** | `CONTINUITY_AUDIT_DMG_PLAYER_2026-07-31.md` | **DONE** + **re-scan** §4 | PASS; Q-OV-4 resolved |
| **Setting / Chronicle T6–10** | `F1_100_SETTING_TRACK_2026-07-31.md` | **DONE** | Digest [`F51_100_Director_Deep_Gazetteer.md`](../manuals/F51_100_Director_Deep_Gazetteer.md) |
| **Rules T6–10 / deep Opening** | `F1_100_RULES_TRACK_2026-07-31.md` | **DONE** | Full-Opening milestones; Deep Opening stance; Q6 locked (regular zone + hidden chamber); clocks 2400/1200 |
| **Encounters T6–10** | `T6_10_ENCOUNTERS_2026-07-31.md` | **DONE** | 35 cards / 16 rosters; floors still `mapped: false`; EV not XP |
| **Bestiary T6–10** | `T6_10_BESTIARY_COMBAT_2026-07-31.md` | **DONE** | **696** trusted / **11** sandbox; **10 / 10** Guardians frozen (`gate-guardian-trusted`) |
| **Integration spine** | **This file** | **THIS PASS** | Bestiary T6–10 flipped DONE; % + blockers refreshed; continuity re-verify PASS |

*(All F1–100 sibling tracks complete. Scaffolds retired.)*

---

## 2. Integration deliverables (this spine)

| Deliverable | Path |
|-------------|------|
| Master stamp | `docs/mechanics/F1_100_TASK_FORCE_MASTER_2026-07-31.md` |
| Continuity FAIL fixes | `CONTINUITY_AUDIT_*`, `RULESET_VULNERABILITIES.md`, archive Directors Manual clock rows, `BESTIARY_SCRUB_LOG.md` |
| Deep-tier crafting guidance | `DEEP_TIER_CRAFTING_DIRECTOR_GUIDANCE_2026-07-31.md` + `directorGuidance` on 218 recipes + `_enrich_deep_tier_crafting_guidance.py` |
| Director one-pager | [`docs/manuals/HOW_TO_RUN_FLOOR_1_100_DIRECTOR_ONE_PAGER.md`](../manuals/HOW_TO_RUN_FLOOR_1_100_DIRECTOR_ONE_PAGER.md) |
| Instruments pointer | Part III Director rule → deep-tier guidance |

**Not done (rebuild note only):** static Next export under `out/` may lag Session/crafting/encounter/bestiary source — run `npm run build` before shipping a frozen companion. Do not hand-edit `out/`.

---

## 3. Product metrics (live)

| Metric | Value |
|--------|------:|
| Recipes total / filled components | 623 / 623 |
| Craft `ready` (T1–5 clean) | 405 |
| Craft `needsReview` + `directorGuidance` | 218 / 218 |
| Bestiary JSON / trusted `draft: false` | 707 / **696** |
| Remaining bestiary sandbox / draft | **11** |
| Floor tiers mapped | **5 / 10** (T6–10 `mapped: false`) |
| Live Gate Guardians named + trusted | **10 / 10** |
| Opening clocks product (`HORN_AT`, hornRule) | **1200 / 2400** |
| Purge verifier LIVE-WRONG | **0** |

---

## 4. Continuity re-scan (integration pass — bestiary land)

**Sources opened:** Continuity SoT · Player `rulebook_output.txt` (UTF-16LE) · DM-01 via Continuity audit · `F1_100_RULES_TRACK` · `T6_10_ENCOUNTERS` · `T6_10_BESTIARY_COMBAT` · `F1_100_SETTING_TRACK` · T1–5 stamps · Session / dungeon / floor JSON · `_purge_clock_verify.py`.

| Checklist | Result | Evidence |
|-----------|--------|----------|
| Opening **2400** / Horn **1200** | **PASS** | Player extract; Session `HORN_AT=1200`; JSON hornRule; purge LIVE-WRONG=0 |
| No live Opening=240 / Horn=120-as-PoNR | **PASS** | Product purge LIVE-WRONG=0 |
| Soft quit ≠ Horn | **PASS** | Books + Session copy |
| Expedition max **12** | **PASS** | Rulebook + gazetteer; Q-OV-2 **RESOLVED** 2026-07-31 (**12 max**; T4 24-PC = playtest only) |
| Live Guardian names only + trusted ×10 | **PASS** | All 10 `gate-guardian-trusted`, `draft: false` in `src/bestiary_data_full.json` |
| Umbrin / no Drow product leak | **PASS** | Player extract **0** whole-word Drow |
| Player spoilers (Silent Ones / Heartcell) | **PASS** | Player extract **0** |
| Milestone XP consistency | **PASS** (T1–10) | Full-Opening milestones official; CR→XP denied in Rules + Encounter stamps; EV toolkits only |
| Setting gazetteer clocks / 12 / secrets | **PASS** | F51–100 digest aligned |
| Q-OV-4 Silent Ones packaging | **RESOLVED** | DM-01 Ch 8 |

### FAILs this pass

None — clear continuity checks all **PASS**. No edits required.

### Remaining true blockers (do not silently close)

| ID | Blocker | Owner? |
|----|---------|--------|
| **Q6** | Level 97 Old God — → regular zone + hidden chamber | **RESOLVED** 2026-07-31 — mechanical gaps remain |
| **Peace trigger** | Undefined numeric / narrative threshold | Yes |
| **Q-OV-2** | Expedition max **12** | **RESOLVED** 2026-07-31 |
| **Floors `mapped: false`** | T6–10 toolkits shipped; JSON still unmapped until room keys | Intentional |
| **`out/` rebuild** | Static export may lag live source | Before freeze ship |
| **Interstice flesh** | Stub/digest OK; deeper Chronicle/DM sync still thin | Author / optional |
| **Non-core RP / Oracle / Paladin drafts** | Author | Should-have |

---

## 5. Path to keep this master stamp current

1. When a sibling writes `F1_100_*_2026-07-31.md` (or renames), update §1 Status + Actual.  
2. Re-run: `python docs/mechanics/_purge_clock_verify.py` (expect LIVE-WRONG 0).  
3. Re-check Player UTF-16 extract for Drow / Silent Ones / Heartcell = 0.  
4. Confirm milestone language in any new T6–10 rules/docs does **not** invent CR→XP.  
5. Confirm Guardians match live roster (Vaskor → Marquis) and stay `draft: false`.  
6. Crafting: after `fill-crafting-components.mjs`, re-run `_enrich_deep_tier_crafting_guidance.py`.  
7. Bump §0 readiness % when T6–10 `mapped: true` and/or Q6/peace close.  
8. Rebuild `out/` once for ship; leave a one-line note here with build date.

---

## 6. What to re-verify when siblings finish mid-flight

| Sibling lands | Re-verify |
|---------------|-----------|
| Rules T6–10 | **LANDED** — Milestone-only; Q6 locked (regular zone + hidden chamber); Player book no secrets; clocks untouched |
| Encounters T6–10 | **LANDED** — Live Guardian names; EV not XP; `mapped` flags honest; expedition 12 |
| Bestiary T6–10 | **LANDED** — 10 Guardians trusted; 696/11; no Silent Ones sheet lore |
| Any DM-01 / Player `.docx` edit | Continuity SoT override gate; refresh extracts |

---

## 7. Related one-pager & guidance

- Directors run sheet: [`HOW_TO_RUN_FLOOR_1_100_DIRECTOR_ONE_PAGER.md`](../manuals/HOW_TO_RUN_FLOOR_1_100_DIRECTOR_ONE_PAGER.md)  
- Deep craft: [`DEEP_TIER_CRAFTING_DIRECTOR_GUIDANCE_2026-07-31.md`](./DEEP_TIER_CRAFTING_DIRECTOR_GUIDANCE_2026-07-31.md)  
- Continuity SoT: [`CONTINUITY_SOURCE_OF_TRUTH.md`](./CONTINUITY_SOURCE_OF_TRUTH.md)  
- Bestiary T6–10: [`T6_10_BESTIARY_COMBAT_2026-07-31.md`](./T6_10_BESTIARY_COMBAT_2026-07-31.md)

*Master stamp updated 2026-07-31 — all sibling tracks DONE; bestiary T6–10 integrated. No commit.*
