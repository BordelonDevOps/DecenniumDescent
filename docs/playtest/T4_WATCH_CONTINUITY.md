# T4 expedition continuity watch — Isles of Eternal Radiance (EXP-T4-01)

**Agent:** Continuity Watcher (playtest subdivision)  
**Date:** 2026-07-30  
**Architect playtest ID:** `EXP-T4-01`  
**Sim playtest ID:** `EXP-IER-T4-01` *(ID drift — see §0)*  
**Format:** 3 companies × 8 seats (24 PCs) · L8–L10 · good/neutral · T4 floors 31–40  
**Sim status:** **Complete** — [`T4_EXPEDITION_PLAY_REPORT.md`](./T4_EXPEDITION_PLAY_REPORT.md), [`T4_ISSUES_LOG.md`](./T4_ISSUES_LOG.md)

> **Out of scope:** Glassbite Hollow (`EXP-BGR-01`, T1 fringe, 4-PC).

**Inputs read:**

| Source | Role |
|---|---|
| [`T4_EXPEDITION_PLAY_REPORT.md`](./T4_EXPEDITION_PLAY_REPORT.md) | Post-sim play-by-play, calendar, boss probe |
| [`T4_ISSUES_LOG.md`](./T4_ISSUES_LOG.md) | 50 numbered issues |
| [`T4_EXPEDITION_SCENARIO.md`](./T4_EXPEDITION_SCENARIO.md) | Architect scenario (Dawn Concord / Mirror Guild / Choir Covenant) |
| [`T4_ROSTER.md`](./T4_ROSTER.md) | Architect 24-seat casting (17/17 classes) |
| [`NEWCOMER_PLAYER_GUIDE.md`](./NEWCOMER_PLAYER_GUIDE.md) | Player-facing Resonance / Umbrin / death saves |
| [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md) | RP myth-bust; Hybrid-B internal-only |
| [`UMBRIN_LORE.md`](../mechanics/UMBRIN_LORE.md) · [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md) · [`RULESET_VULNERABILITIES.md`](../mechanics/RULESET_VULNERABILITIES.md) | Canon refs |

---

## Executive verdict

| Result | **Pass with drift** |
|---|---|

The completed sim **honors T4 zone lore, good/neutral ethos, Gor Vekk projection (not full CR 29 kill), draft XP/combat labeling, and Umbrin Sunlight Sensitivity in radiant light** — fixing the main pre-sim gap. It is **not a valid execution of the architect charter**: the sim used a **fallback roster** (Sunward Lance / Prism Watch / Dawn's Anvil) because scenario/roster were missing at sim time, carries **Glassbite persona/name contamination**, omits **3/17 canon classes**, includes **non-companion races**, and **shortens the goal ladder** (no Radiance Gate F40 install). Treat sim results as **T4 mechanics + zone stress test**; **re-run on architect roster** before architect sign-off.

---

## 0. Fallback roster drift (critical)

| Dimension | Architect (`T4_ROSTER.md`) | Sim (fallback) | Drift |
|---|---|---|---|
| **Playtest ID** | `EXP-T4-01` | `EXP-IER-T4-01` | Medium |
| **Company A** | **Dawn Concord** (vanguard) | **Sunward Lance** | **High** |
| **Company B** | **Mirror Guild** (recon/research) | **Prism Watch** | **High** |
| **Company C** | **Choir Covenant** (support/ritual) | **Dawn's Anvil** | **High** |
| **Class coverage** | **17 / 17** canon classes | **14 / 17** — missing **Tinker, Shaman, Crimson Agent** | **High** |
| **PC names** | Torven, Widget, Mara, Shade Merit, … | Vesper, Kael, Mira, Greta, Dren Voss, … | **High** |
| **Persona carryover** | 15 distinct playtest personas | P1–P4 from **EXP-BGR-01** + ad-hoc fills | **High** |
| **Races** | 13 companion peoples | **Aasimar, Halfling, Warforged** not in `builder-races.js`; "Wood Elf", "Swamp Troll" variants | **High** |
| **Umbrin seats** | **Shade Merit** (C6, neutral-good exile) | **Vesper Ashwhisper** (A1) + **Kethren Quiet-Step** (B3) | Medium — role OK, not architect cast |
| **House name as PC** | — | **Commander Rhal-Voss** → Dren Voss (canon **House Rhal-Voss** is NPC pattern) | Medium |

**Sim input note:** Play report records scenario/roster as **missing at sim time**; both architect files **exist now** — timing/process drift, not ongoing absence.

**Continuity impact:** Encounter balance, persona friction, and class-cap coverage **cannot be mapped 1:1** to architect deliverables. Issues log items on Tinker/Shaman/Crimson Agent coverage, Choir Covenant triage authority, and Mirror Guild slate recovery were **not exercised**.

---

## 1. Architect vs sim — scenario execution

| Architect goal (`T4_EXPEDITION_SCENARIO.md`) | Sim outcome | Match? |
|---|---|---|
| Harvest **3 sun-shard vials** (Radiant Bloom F32) | **3/3** placed at obelisk probe | **Partial** — harvest path different (2 vials mid-ladder, supply issue) |
| Align **Sunforged Obelisk** (F36) | Probe attempted; **blinding radiance fail-forward** R3 | **Partial** — matches projection-fail branch, not full puzzle win |
| Install vials at **Radiance Gate (F40)** at dawn zenith | **Not run** — extraction after F36 retreat | **Fail vs architect** |
| Recover **prism-map slate** (Mirror Reef F34) | Mapping only; no slate recovery called out | **Drift** |
| **E0–E6 encounter ladder** (Ogre RAM×6, Allip+Otyugh, Cloaker×4, Knight×6, Oni+Toad, Gor projection) | **Different foes** (Assassin, Flameskull×2, Duodrone×2, Deva, Berbalang, + company splits) | **High drift** |
| Horn: **72 h T4** + **120 h** total underground buffer | **106 / 120 h** at debrief; 12 calendar days | **Pass** — within rulebook horn |
| **≥18/24 conscious** extraction | All stabilized; partial success narrative | **Pass** |
| Success = **calibration window** at Radiance Gate | **Partial success** — camp + intel, obelisk probe aborted | **Drift** — sim chose shorter win condition |

---

## 2. Canon violations in the sim

### Alignment (ethos + Resonance affinity)

| Check | Finding |
|---|---|
| **Good/neutral gate** | **Pass** — no evil PCs; Umbrin as allies not saboteurs |
| **Resonance affinity/opposition** | **Drift** — RP spends at flat **level × 2**; no alignment line items in play report (same gap as fringe sim) |
| **Deva mis-ID fight** | **Drift** — neutral observer attacked; table acknowledged sandbox aggression — not ethos violation but **zone tone** friction |

### Umbrin lore & geography

| Check | Finding |
|---|---|
| **Product naming** | **Pass** — Umbrin, Murkish wanted (P3), no Drow/Underdark |
| **Sunlight Sensitivity @ T4** | **Pass with drift** — briefing: T4 = **bright light always**; sun-shield vials (12 issued, supply tracked); Umbrin disadvantage Day 10 when vials low — **addresses pre-sim gap** |
| **Reputation / morale** | **Pass** — Umbrin daylight-lead argument Day 9; transactional command (Sera holds line) |
| **Geography** | **Pass** — F31–F36 POIs match `floor-encounters.json` T4; Crystalfront/Shardspire staging consistent |
| **Rhal-Voss as PC** | **Drift** — canon house name used for Gamma commander alt | 

### Hybrid-B

| Check | Finding |
|---|---|
| **Player-facing** | **Pass** — cheatsheet distributed; Hybrid-B only in play report header (internal) |
| **Multiclass merge** | **N/A** — single-class seats |

### Draft labeled?

| Asset | Labeled? | Notes |
|---|---|---|
| Excel-sandbox combat | **Partial** | Narrator renamed some foes (Sunward Sentinels); *Aberrant Lash* on Deva still breaks tone |
| Draft XP | **Yes** | Per-company + 16/24-way splits; boss **½ award** (67,500 ÷ 24) table ruling |
| Gor Vekk | **Yes** | **200 HP manifestation**; retreat R3; not full 135k auto-award |
| Fallback roster | **Disclosed** | Play report § input gap — but sim proceeded without architect file alignment |
| Burnout / caps | **Yes** | Greta burnout badge; Paladin/Warrior/Mirrorsage/Oracle caps cited |

---

## 3. Terminology drift

| Drift | Where | Severity |
|---|---|---|
| Fallback company names vs architect | Sim vs `T4_ROSTER.md` | **High** |
| RP → "slots" / "14 spells" | P1 Vesper, P2 Greta (issues #11, #34) | **High** |
| Hybrid-B in play report header | Internal doc | Low |
| Glassbite character names in T4 sim | Vesper, Helga/Greta, Kael, Kethren, Mira, Torin, Selene | **High** — cross-playtest contamination |
| Play report: guides "not found" | `NEWCOMER_PLAYER_GUIDE.md` exists | Medium — sim-time gap |
| Sandbox attacks on celestials | Deva *Aberrant Lash* (#6) | Medium |
| Non-companion races | Aasimar, Halfling, Warforged (# architect roster uses companion peoples only) | **High** |

---

## 4. Gaps confirmed by sim (T4-applicable R-##)

| ID | Gap | Sim evidence | Still open? |
|---|---|---|---|
| **R-01** | Retune action cost | Free during short rest (assumed) | Yes |
| **R-02** | Death saves / heal-at-0 | Manual ×7; Greta HW on Kethren OK | Yes |
| **R-03** | Hit Dice on short rest | Missing (#48) | Yes |
| **R-04** | Mixed draft/canon RP trust | Vesper 14 draft vs Greta 14 canon Cleric | Yes |
| **R-07** | Sunlight / radiant adjudication | **Improved** — vial supply + disadvantage tracked; not in Session UI (#23) | Partial |
| **R-08** | Sandbox attack identity | Deva, ongoing *Freak Bite* patterns | Yes |
| **R-11** | Alignment on sheets | Not logged on RP spends | Yes |
| **R-12** | Draft XP UX | 16/24 splits manual (#26); ~6,040 PC/session high (#50) | Yes |
| **R-13** | 24 vs 12 PC team cap | Sim ran 24; no mass-init in Session (#23) | Yes |
| **R-14** | Gor Vekk metadata Floor 90 | Issues #4–5 | Yes |
| **R-15** | Mass combat procedure | Joint fights 2× wall-clock (#24); friendly fire (#21) | Yes |
| **R-16** | Mirrorsage / Oracle caps | Neme + Selene — caps followed (#15–16) | Exercised; enforcement still informational |
| **R-18** | **Architect charter not executed** | Fallback roster + shortened ladder | **New — sim-only** |
| **R-19** | Sun-shield supply tracker | Narrative only (#23) | Yes |
| **R-20** | Partial boss XP on retreat | ½ Gor Vekk award — no rules text (#28) | Yes |

---

## 5. Continuity gate cross-check (post-sim)

| Gate | Result | Notes |
|---|---|---|
| **A** Terminology & cosmology | **Pass with drift** | T4 zone OK; sandbox names; fallback names |
| **B** 17-class roster | **Fail vs architect** / **Drift in sim** | Architect 17/17; sim 14/17 |
| **C** Oracle/Paladin draft | **Pass with drift** | Selene Oracle RC; three Paladins; oaths unnamed |
| **E** Character save & UI | **Pass with drift** | Session gaps (#47–48); horn 106/120 manual |
| **F** Dungeon T4 | **Pass** | `floor-encounters.json` T4 honored; F40 gate not reached |
| **Architect charter** | **Not executed** | Re-run required on Dawn Concord / Mirror Guild / Choir Covenant |

---

## 6. Recommendations

1. **Re-run sim** (or live table) on **`T4_ROSTER.md`** with **`T4_EXPEDITION_SCENARIO.md`** full ladder through **Radiance Gate F40**.
2. **Drop non-companion races** (Aasimar, Halfling, Warforged) from any canonical T4 cast.
3. **Remove Glassbite name carryover** unless intentionally linking playtests.
4. Align playtest ID to **`EXP-T4-01`** across report, issues log, and stamp.
5. Keep **sun-shield supply + Umbrin bright-light briefing** — sim validated this as essential.
6. Author **Gor Vekk manifestation** block (200 HP, 3-round timer) as separate from gate-boss row — sim matches scenario E6 intent.

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Continuity Watcher — T4 post-sim (`EXP-T4-01` / sim `EXP-IER-T4-01`) |
| **Date** | 2026-07-30 |
| **Verdict** | **Pass with drift** |
| **Sim validity** | **Partial** — mechanics/zone; not architect roster/scenario |
| **Deliverable** | `docs/playtest/T4_WATCH_CONTINUITY.md` |
| **No commit/push** | Per playtest brief |

**Note (2026-07-30):** T4 sim horn tracking (**106/120 h**) is the **in-delve underground clock** — not the **100-day / 2400 h decennial opening window** ([`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md)). Prior Matrix lore drift (**240 h**) corrected to **2400 h** in extract only.
