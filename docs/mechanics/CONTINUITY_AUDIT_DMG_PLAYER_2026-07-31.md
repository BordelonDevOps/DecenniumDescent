# Continuity audit — Director's Crucible ↔ Player Rulebook

**Stamp:** 2026-07-31  
**Scope:** Shared procedures + lore boundaries behind the DM bible and Player Rulebook while T1–5 implementation agents work elsewhere.  
**No commit.**

---

## Sources opened

| Layer | Path |
|-------|------|
| **DM bible** | `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx` |
| **Player Rulebook** | `decennium descent player rulebook.docx` |
| **Living extract** | `rulebook_output.txt` (UTF-16LE — verified aligned on Opening / App B / expedition coalition) |
| **Continuity SoT** | `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` |
| **Locks / stamps** | `DESCENT_WINDOW_CANON.md`, `OPENING_CLOCK_PURGE_2026-07-31.md`, `DIRECTOR_BIBLE_CLOCK_TYPO_FIX_2026-07-31.md`, `OWNER_COSMOLOGY_LOCKS_2026-07-30.md`, `EXPEDITION_STRUCTURE_CANON.md`, `APPENDIX_B_FOLK_RELIGION.md`, `PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md`, `BESTIARY_LORE_PASS_2026-07-30.md` / guardian ingest locks |
| **Working extracts** | `docs/mechanics/_audit_extracts/dmg_2026-07-31.txt`, `player_2026-07-31.txt`, `audit_hits_2026-07-31.json` |

---

## Verdict

**Overall: PASS with residual open overrides (not literature FAILs).**

Player Rulebook and Complete Director Edition agree on Opening **2400/1200**, soft quit ≠ Horn, expedition **12** + five teams + coordinating multi-Expedition larger forces, public Crucible myth (Calan'thir & Asmodeus), folk-religion Appendix B, live Gate Guardian names only (Director), Umbrin (no Drow/SWTOR), and no deep Director spoilers in the player book.

One clear DM-bible Session Zero contradiction (secret discoverer language labeled as “public myth”) was **fixed**. Several Continuity docs still teaching purged **120h** as live Session truth were **corrected**.

---

## PASS / FAIL matrix

| Checklist item | DMG | Player | Continuity docs / runtime | Result |
|----------------|-----|--------|---------------------------|--------|
| Opening **2400h / 100 days** | Present (Ch clocks + Event Engine) | Present (**The Decennial Opening**) | `DESCENT_WINDOW_CANON` + purge stamp | **PASS** |
| Horn **1200h / day 50** PoNR | Present | Present | `HORN_AT = 1200`, `hornRule` day-50 | **PASS** |
| No live Opening=**240** / Horn=**120** | Typo callout only; Event Engine **0–240** = first *phase* of 2400h Opening (not Opening duration) | None as Opening clocks | Product purge **LIVE-WRONG = 0**; some docs had stale teaching → **fixed this pass** | **PASS** (after Continuity doc fixes) |
| Soft quit Floor 50 / Bar ≠ Horn | Explicit (Bar of Last Refuge, Canticle) | Explicit (Sanctum / Bar ≠ Horn) | Canon stamps agree | **PASS** |
| Expedition max **12**; five teams; larger = coordinating Expeditions | Cap twelve; five teams; periods; coalition wording | Cap 12; five teams; “force larger than twelve… coordinating” | `EXPEDITION_STRUCTURE_CANON`; Q-OV-2 **RESOLVED** 2026-07-31 (**12 max**) | **PASS** (RAW); **RESOLVED** Q-OV-2 |
| Silent Ones = Old Ones (GM); public = Calan'thir & Asmodeus | Ch 8 lock + Guardrails + glossary (Q-OV-4 closed) | Public myth only; no Silent Ones / Heartcell | Owner locks Q1/Q3; packaging in DM-01 | **PASS** layers; **RESOLVED** Q-OV-4 |
| Heartcell vs public Crucible | Director-secret marked | Absent (correct) | SoT secret stratum | **PASS** |
| Live Gate Guardian names only | All 10 live names; no Velkyrion/Zeharra/Kharix/Hollow King/Cindervore/Vox Prime as guardians | Player-safe “named Gate Guardian” only — no roster (intentional) | Bestiary / Q7 locks | **PASS** |
| Appendix B = folk religion (player) | Director teaches mortal models ≠ objective truth | Title **Faiths and Cosmologies…** + disclaimer + masks/abstractions reframes | Q-OV-3 patched 2026-07-31 | **PASS**; optional tone scrub **OPEN** |
| Umbrin not Drow; no SWTOR | No Drow/SWTOR | Umbrin present; **0** whole-word Drow | Product path clean | **PASS** |
| Player book has no deep Director spoilers | N/A | No Silent Ones / Heartcell / loot-as-bait / Ul'nak / revelation ladder | Alignment stamp intentional omissions | **PASS** |

---

## FAILs — fixed this pass

| ID | Issue | Fix | Path(s) |
|----|-------|-----|---------|
| **F-1** | DMG Session Zero item 2 labeled “public Crucible myth” but used **secret** discoverer/activator wording (`discovered, claimed, modified, activated`) — contradicted owner Q3 + DMG Ch 8 public myth | Rewrote to **jointly built** / complete public explanation; secret layer pointed to Ch 8 | `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx` · backup `backups/The_Directors_Crucible_Complete_Director_Edition_pre_continuity_audit_20260731_080206.docx` |
| **F-2** | Continuity docs still taught Session horn as live **120h** after purge | Updated Wired table / prose to **1200 / 2400** | `SESSION_LOOP.md`, `COMBAT_SYSTEM_COMPARE.md`, `RULESET_VULNERABILITIES.md` (D-04), `OVERNIGHT_VAGUE_QUEUE.md` (VQ-24), `BESTIARY_LORE_PASS_2026-07-30.md`, `OWNER_COSMOLOGY_LOCKS_2026-07-30.md` bottom line, `CONTINUITY_DETAILED_CHECK.md` Q4/Q5/open-overrides rows |
| **F-3** | Continuity SoT still listed rebuild Directors Manual as primary and asked “ASK OWNER” for off-repo title — Complete Director Edition already owner/alignment SoT | Promoted Complete Director Edition to primary Director bible row | `CONTINUITY_SOURCE_OF_TRUTH.md` §2 |

---

## FAILs / opens — still open (not silently rewritten)

| ID | Issue | Disposition |
|----|-------|-------------|
| **O-1 / Q-OV-2** | Optional charter-exception paragraph for large Cycle delves vs coalitions-only | **RESOLVED** 2026-07-31 — owner locked **12 max**; coalitions-only; no 24-PC charter |
| **O-2 / Q-OV-4** | Silent Ones authorship packaging | **RESOLVED 2026-07-31** — DM-01 Ch 8 + Canon Guardrails + glossary (“Silent Ones ARE the Old Ones”); companion `SILENT_ONES_CANON.md` remains mirror. Matrix/Cosmology public `.docx` prose unchanged by design. |
| **O-3** | Appendix B remaining history/nations encyclopedia voice (tone scrub) | **OPEN** — optional; load-bearing folk reframes already applied |
| **O-4** | Legacy `decennium descent player rulebook.doc` may lag `.docx` SoT | **OPEN** — do not treat `.doc` as SoT |
| **O-5** | Rebuild `Decennium_Descent_Directors_Manual.docx/.md` may lag Complete Edition | **OPEN** — regenerate when owner wants twin sync |
| **O-6** | Historical playtest sims (`SIM_*`, `T4_*`) still *record* pre-purge 120h UI | **ARCHIVE** — intentional; not teaching formulas |
| **O-7** | Gate Guardian **public** names in Player Rulebook | **OPEN** — currently deferred to Director materials (alignment stamp) |

---

## Shared-topic comparison (load-bearing)

| Topic | DMG | Player | Aligned? |
|-------|-----|--------|----------|
| Opening calendar | 2400h / Horn 1200 / seal 2400 | Same | Yes |
| Soft quit | Bar / Tier 5 Sanctum ≠ Horn | Same | Yes |
| Public myth | Joint Calan'thir & Asmodeus Crucible | Same (player-facing complete) | Yes (after F-1) |
| Secret authorship | Silent Ones/Old Ones → Heartcell | Absent | Correct split |
| Expedition structure | 12 / five teams / periods / coalitions | Same | Yes |
| Folk religion | Mortal models ≠ Director cosmology | App B renamed + disclaimer | Yes |
| Guardians | Live bestiary roster staged | Unnamed “Gate Guardian” pointer | Intentional |

---

## Method notes

- Extracted both `.docx` files to UTF-8 under `docs/mechanics/_audit_extracts/` before compare.
- Scanned Opening/Horn, expedition, cosmology spoilers, Appendix B, guardians, Umbrin/Drow/SWTOR.
- Re-read DMG after Session Zero edit; `discovered, claimed, modified` count = **0**.
- Did **not** touch XP/crafting/encounter files other agents may be editing.
- Did **not** large-rewrite the DM bible beyond the one Session Zero contradiction with locks.
- Player Rulebook needed **no** further literature edit this pass (Opening / coalition / App B / spoiler boundary already matched alignment stamp).

---

## Scripts / backups

| Artifact | Role |
|----------|------|
| `docs/mechanics/_continuity_audit_dmg_player_2026-07-31.py` | Scan harness |
| `docs/mechanics/_fix_dmg_session_zero_myth_2026-07-31.py` | Session Zero myth patch |
| `backups/The_Directors_Crucible_Complete_Director_Edition_pre_continuity_audit_20260731_080206.docx` | Pre-fix DM bible |

*Audit issued 2026-07-31 — no commit.*

---

## Addendum — F1–100 integration re-scan (same day)

**Agent:** Floor 1–100 integration spine. **Sources re-opened:** Player UTF-16 extract, DM-01 clocks, Session/`hornRule`, gateBosses, Setting stamp + F51–100 gazetteer, crafting JSON.

| Item | Result |
|------|--------|
| Clocks 2400/1200 product | **PASS** (`HORN_AT=1200`; purge LIVE-WRONG=0) |
| Guardians live roster ×10 | **PASS** |
| Expedition 12 | **PASS**; Q-OV-2 **RESOLVED** (**12 max**) |
| Drow in Player extract | **0** — Q-02 closed |
| Player Silent Ones / Heartcell | **0** |
| Milestone Opening | **PASS**; T6–10 rules stamp still pending |
| Q-OV-4 row in this audit | **Corrected to RESOLVED** (was stale OPEN) |
| Literature FAILs fixed | Archive Directors Manual 120h teaching; RULESET XP/Drow/Burnout drift |

Master: [`F1_100_TASK_FORCE_MASTER_2026-07-31.md`](./F1_100_TASK_FORCE_MASTER_2026-07-31.md).
