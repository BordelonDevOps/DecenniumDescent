# T1–5 rules package stamp

**Date:** 2026-07-31  
**Workspace:** `DecenniumDescent-main`  
**Owner phase DoD:** Tier 1–5 table-ready — Rules / Director lineup / blocking owner Qs  
**No commit.**

---

## Decisions applied

| Topic | Decision | Basis |
|-------|----------|--------|
| **XP awards** | **Milestone-only official for Opening campaigns** (T1–5). L1–20 thresholds remain canon. No published CR→XP. Session CR→XP = **optional / non-canon** (no save write-back). | Neither Player Rulebook nor DM-01 had a CR→XP table; DM-01 already preferred milestones / Director judgment. Owner brief: ship milestone-only if nothing solid. |
| **DM-01** | Promote **`The_Directors_Crucible_Complete_Director_Edition.docx`** as official DM-01. Sister Codex / Instruments / Chronicle stay active. Missing `The_Directors_Crucible.*` + generated Directors Manual dumps = superseded / archive. | Gap BIB-2 / owner Phase 0. |
| **Q-OV-4** | **Closed.** Silent Ones / Heartcell GM-only already in DM-01 Ch 8 (table cell) + Canon Guardrails + glossary; strengthened with explicit **“Silent Ones ARE the Old Ones (same entity).”** Player Rulebook unchanged on secrets. | Owner option (1) — published Director corpus. |
| **Burnout** | Permanent **GM fiat** (suggested playtest: disadvantage on Weave checks until end of next turn). Session badges = reminders only. | DM-01 already said until final table; wired enforcement not ready. |
| **Ceiling caps** | Permanent **GM fiat** informational caps; not auto-enforced. | CLASS_CEILING_CAPS.md draft → ship label. |
| **Non-core RP pools** | Wizard / Mage / Cleric / Druid = rulebook-complete. Other Weave classes = **draft** companion estimates (Session `*` marker). | DM-01 + Player table note. |

Clock canon unchanged: Opening **2400h / 100 days**; Horn **1200h / day 50**.

---

## Files changed

### Books (backed up under `backups/`)

| File | Change |
|------|--------|
| `decennium descent player rulebook.docx` | Opening milestone advancement section; Beyond 1st Level clarified; RP draft note; Burnout + ceiling GM-fiat |
| `rulebook_output.txt` | Refreshed UTF-16LE extract |
| `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx` | Awards → Opening milestones; Burnout/pool/ceiling fiat; Always checklist; Silent Ones = Old Ones (Ch 8 table + Guardrails + glossary) |

### Continuity / lineup

| File | Change |
|------|--------|
| `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` | DM-01 primary; Q-OV-4 resolved; audit opens DM-01 |
| `docs/manuals/BOOK_LINEUP.md` | Complete Edition = DM-01; missing/archive paths marked |
| `docs/manuals/AGENT_SIMULATION_REFERENCE.md` | Points at Complete Edition |
| `.cursor/rules/continuity-rulebooks.mdc` | DM-01 + override status |
| `docs/mechanics/XP_ADVANCEMENT_CANON.md` | Milestone Opening official |
| `docs/mechanics/CLASS_CEILING_CAPS.md` | GM-fiat ship label |
| `docs/playtest/READY_TO_CONTINUE.md` | Q-OV table + lock M |

### Companion labels

| File | Change |
|------|--------|
| `src/components/SessionTracker.tsx` | Banner + XP/Burnout labels |
| `src/components/ClassCeilingCapsCallout.tsx` | GM fiat badge |
| `src/data/resonance-economy.js` | `BURNOUT_EFFECT_STUB` GM-fiat copy |

### Scripts (edit helpers; not product)

- `docs/mechanics/_t1_5_rules_package_2026-07-31.py`
- `docs/mechanics/_t1_5_director_patch_2026-07-31.py`

---

## Remaining blockers (outside this ownership / still open)

| Blocker | Owner? | Notes |
|---------|--------|-------|
| **Q-OV-2** expedition max 12 | **RESOLVED** | Owner lock 2026-07-31; coalitions text already OK for RAW |
| **Level 97 Old God (Q6)** | Gaps remain | **RESOLVED** — **Floor 97 = regular zone with hidden chamber (Old Ones sleep); true conquest L100 boss → focusing crystal → weaken Old God; else L30 mind-control near wipe.** [`LEVEL_97_OLD_GOD_Q6_OPEN.md`](./LEVEL_97_OLD_GOD_Q6_OPEN.md); not required for T1–5 ops |
| **T1–5 encounter cards / budgets** | Other agents | Floor Encounters operationalization |
| **Gate Guardians combat freeze + Session HP** | Other agents | Guardians authored draft; wire real HP |
| **Crafting `components[]`** | Other agents | Avoided per brief |
| **Bestiary sandbox draft rows** | Other agents | Avoided xlsx |
| **T6–10 product stance** | Owner | **Defined** 2026-07-31 — [`F1_100_RULES_TRACK_2026-07-31.md`](./F1_100_RULES_TRACK_2026-07-31.md) |
| **Print/PDF pipeline** | Production | Not rules |
| **Non-core RP author tables** | Author | Draft badges honest for playtest |

---

## Continuity notes

- Did **not** invent cosmology; Silent Ones = Old Ones only as owner lock already held.
- Did **not** put Heartcell / Silent Ones into Player Rulebook.
- Did **not** promote draft CR→XP to canon.
- Did **not** commit.

*Stamp issued 2026-07-31.*
