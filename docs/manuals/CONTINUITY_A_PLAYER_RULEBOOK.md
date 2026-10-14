# Continuity A — Player Rulebook audit (Expedition / Teams / Resonance / Rests–Death)

**Agent:** Continuity A  
**Date:** 2026-07-30 (re-scan: DM-01 + BB-01)  
**Scope:** Rebuild book line vs **Player Rulebook** (`rulebook_output.txt`, UTF-16LE)  
**Topics:** Expedition 12, five teams & periods, Resonance language, rests & death (when mentioned)  
**Do not:** commit/push · silently overwrite rulebook text

**Rulebook baseline (authoritative):**

| Topic | Rulebook cite |
|-------|----------------|
| Expedition cap | `rulebook_output.txt` **3801–3926** — up to **12 characters** per Expedition; organizational cap, not combat-party cap |
| Five teams | Combat 4–6 · Recon 1–3 · Research 1–3 · Resource 2–4 · Support 1–3 (**3807–3831**) |
| Day periods | Morning / afternoon / evening; multi-period tasks (**3833–3837**) |
| Resonance | **6069–6132** — RP pool; **not spell slots**; short rest = ¼ max + casting mod; long rest = full RP; Oracle uses RC, not RP (**6104**) |
| Death / dying | **6021–6038** — death saves, stabilize DC 10 Medicine, instant death at max HP damage |
| Base-camp rest | Expedition base camps include **safe resting location** (**3907–3908**) — no horn-hour coupling in this block |

See also [`EXPEDITION_STRUCTURE_CANON.md`](../mechanics/EXPEDITION_STRUCTURE_CANON.md).

---

## 1. Pass / fail — rebuild book line

Per [`DIRECTOR_REBUILD_BRIEF.md`](./DIRECTOR_REBUILD_BRIEF.md) / [`BOOK_LINEUP.md`](./BOOK_LINEUP.md).  
**Re-scan stamp:** 2026-07-30 — **DM-01**, **TB-01**, **GZ-01**, **BB-01** on disk.

| Code | Title | Path | Status | Pass/fail | Notes |
|------|-------|------|--------|-----------|-------|
| **DM-01** | The Director's Crucible | `The_Directors_Crucible.md` | **ON DISK** | **PASS** | 24-chapter rebuild — see §1.2. Minor terminology drift (A-DR-1). |
| **BB-01** | Codex of the Heartcell | `Codex_of_the_Heartcell.md` | **ON DISK** | **PASS** | Monster/ecology — see §1.4. |
| **TB-01** | Instruments of the Weave | `Instruments_of_the_Weave.md` | **ON DISK** | **PASS** | §1.3 (prior pass). |
| **GZ-01** | Chronicle of the Decennial Opening | `Chronicle_of_the_Decennial_Opening.md` | **ON DISK** | **PASS** | §1.1 (prior pass). |

### 1.1 GZ-01 — Chronicle of the Decennial Opening ✅

| Topic | Result |
|-------|--------|
| Expedition 12 | **PASS** — cap cited; coalition example (two 12-seat Expeditions). |
| Teams | **PASS** — Recon / Research / Support in tier seeds. |
| Resonance language | **PASS** — cosmology/ecology only; not spell slots. |
| Rests / death | **PASS** — long rest +8 h labeled table assumption; no death-save prose as RAW override. |

### 1.2 DM-01 — The Director's Crucible ✅ (24 chapters)

| Topic | Result | Evidence |
|-------|--------|----------|
| **Expedition 12** | **PASS** | Ch 4 + Ch 24: **twelve characters** organizational cap; **24 = two or three coordinating Expeditions**; Ch 23 sim protocol repeats cap. No single oversized roster as RAW. |
| **Teams** | **PASS** | Ch 2–4, 14, 24: five teams + size bands match **3807–3831**; morning/afternoon/evening; multi-period tasks; Quick / Scene / Parallel / Between-session (**3896–3900**); worked twelve-seat example; base camp types (**3913–3916**). |
| **Resonance language** | **PASS** | Ch 12: **pool, not slots**; cost formula, overcast, multiclass RP, Oracle **RC** separate (**6104**); Ch 21 warns against “spell slots.” **Retune** / **Full Harmony** used as Director labels **with explicit mapping** (“A short rest grants a Retune”; “A long rest grants Full Harmony”) — companion flavor, mechanics match **6113–6116**. |
| **Rests / death** | **PASS** | Ch 2: death saves, Hit Dice on short rest = **paper track** (rulebook procedures, not replaced). Ch 24 **Death and dying (Player Rulebook canon, summarized)** matches **6023–6034**. Long rest **+8 h** horn advance labeled **Session convenience** (Ch 24 clocks table). Ch 3: 120 h horn **superseded**; 2400/1200 canonical. |

**DM-01 checklist (§4):** All items checked.

### 1.3 TB-01 — Instruments of the Weave ✅

| Topic | Result |
|-------|--------|
| Expedition 12 | **PASS** |
| Teams | **PASS** — full period planner + five teams |
| Resonance language | **PASS** — defers to rulebook; short/long rest in camp table |
| Rests / death | **PASS** — no death procedures authored |

### 1.4 BB-01 — Codex of the Heartcell ✅

| Topic | Result | Evidence |
|-------|--------|----------|
| **Expedition 12** | **PASS (N/A)** | No roster-cap prose; no violations. |
| **Teams** | **PASS** | Gate Seal tactics: **Combat / Support / Research** off-map work — matches rulebook team vocabulary (**3807–3831**). |
| **Resonance language** | **PASS** | **Resonance Fields** = zone name; “resonance” in ecology/Director-only blocks — not spell slots or RP economy. |
| **Rests / death** | **PASS (N/A)** | No player-facing rest, death-save, or resurrection procedures. Canticle soft-quit vs horn PoNR correctly distinguished (Part I § Gate Seal Rules). |

**BB-01 checklist (§4):** All items checked.

---

**Legacy v0.1 (archived):**

| File | Pass/fail | Summary |
|------|-----------|---------|
| `Decennium_Descent_Directors_Manual.md` | **SUPERSEDED** | Replaced by DM-01; retain for diff only. Prior **CONDITIONAL PASS** (120 h appendix drift) — **DM-01 resolves horn prose** (Ch 3, 23). |
| `Decennium_Descent_Bestiary_of_Aethel.md` | **PASS** | Superseded by BB-01 for rebuild line; team boilerplate still aligned. |

---

## 2. Drift list (scanned vs Player Rulebook)

| ID | Severity | Source | Rulebook says | Book says | Action |
|----|----------|--------|---------------|-----------|--------|
| **A-DR-1** | Low | **DM-01** Ch 10, 12; legacy manual | **Short Rest** / **Long Rest** (**6113–6116**) | **Retune** / **Full Harmony** as Director teaching labels | **OK** — DM-01 maps explicitly to short/long rest in Ch 12. Do not publish Retune/Full Harmony as player-facing rulebook names without owner gate. |
| **A-DR-2** | Low | GZ-01; DM-01 Ch 24; TB-01 | Expedition block has no horn-hour coupling | Long rest **+8 h** Opening/Horn — **Session convenience** / table assumption | GM layer; labeled in DM-01/GZ-01. |
| **A-DR-3** | Low | DM-01 Ch 14; TB-01 Part IX | No mass-initiative cap in expedition block | ~**8 detailed initiative** actors | GM advice; consistent across rebuild books. |
| **A-DR-4** | **Resolved (DM-01)** | Legacy Directors Manual appendices | — | 120 h vs 1200 h mixed | **DM-01 Ch 3, 23** prefer 2400/1200; flag 120 h superseded. Legacy file only. |
| **A-DR-5** | Info | BB-01, TB-01, GZ-01, DM-01 | Team names match RAW | Combat / Recon / Research / Resource / Support throughout | **Aligned.** |
| **A-DR-6** | Info | DM-01 Ch 3, TB-01, GZ-01 | No horn prose in player rulebook | 2400 h Opening, 1200 h PoNR | Owner lock (Q-OV-1); not Player Rulebook overwrite. |
| **A-DR-7** | Info | GZ-01 Part IV | Published Appendix B | Pending folk-religion rename note | Continuity B / Q-OV-3. |
| **A-DR-8** | Low | TB-01 Part V | Base camps = safe rest (**3907–3908**) | Unupgraded camp: short rest only | Director provisional; TB-01 only. |
| **A-DR-9** | Info | TB-01 Part VI; DM-01 Ch 10 | Resonance System = RP economy | “Four Resonance tracks” = **faction rep** | Naming collision; no mechanics conflict. |
| **A-DR-10** | Low | DM-01 Ch 12 | Oracle RC via Prophecy Trigger | Session grants **+1 RC on short rest** — announced as companion convenience | Correctly flagged non-canon; Ch 12 explicit. |
| **A-DR-11** | Low | DM-01 Ch 12 | Burnout below 25% pool (**6132**) | Burnout consequences = **draft stub**; table default offered | Director provisional until owner ratifies; does not overwrite rulebook overcast text. |

**No scored-topic fail in DM-01 or BB-01.**

---

## 3. Owner questions (rulebook overwrite gate only)

Per [`CONTINUITY_SOURCE_OF_TRUTH.md`](../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md) §4.

**No open Continuity A owner questions.** DM-01 maps Retune/Full Harmony to short/long rest in Ch 12; death summary cites Player Rulebook canon; expedition structure defers to rulebook as binding.

### Q-A-1 — Retune / Full Harmony vs rulebook rest names — **CLOSED (2026-07-30)**

DM-01 Ch 12: *“A short rest grants a Retune…”* / *“A long rest grants Full Harmony…”* — explicit mapping, mechanics match **6113–6116**. TB-01 uses short/long rest directly. **No rulebook overwrite proposed.**

---

**Tracked elsewhere (not Player Rulebook overwrites):**

- Horn **1200 h vs 120 h** — Q-OV-1 (**resolved**)  
- Expedition **12 max** — Q-OV-2 (**resolved** 2026-07-31; T4 24-PC = playtest only)  
- Appendix B folk religion — Q-OV-3 (**player patch applied**)  

---

## 4. Re-scan checklist

### DM-01 — The Director's Crucible ✅ (2026-07-30)

- [x] Max **12**, five teams, three periods, resolution methods (Ch 4, 24).
- [x] Coalition language per **3804–3805**, **3925–3926** (Ch 4, 23).
- [x] Resonance: not slots; Oracle RC separate; short/long rest mapped via Retune/Full Harmony (Ch 12).
- [x] Death/rest: Ch 24 summary matches **6023–6034**; paper tracks in Ch 2.
- [x] **120 h** horn superseded; 2400/1200 + flag (Ch 3, 23).
- [x] Pass/fail row updated in §1.

### TB-01 — Instruments of the Weave ✅ (2026-07-30)

- [x] All checklist items (prior pass).

### GZ-01 — Chronicle of the Decennial Opening ✅ (2026-07-30)

- [x] All checklist items (prior pass).

### BB-01 — Codex of the Heartcell ✅ (2026-07-30)

- [x] Team vocabulary in Gate Seal tactics.
- [x] No player-facing rest/death/resurrection procedures as RAW.
- [x] Pass/fail row updated in §1.

---

## 5. Protocol reminder

1. **Player Rulebook wins** for player procedures until owner approves an amendment.
2. **Rebuild line complete** for Continuity A scope: DM-01, BB-01, TB-01, GZ-01 all on disk and scored.
3. Legacy `Decennium_Descent_Directors_Manual.md` superseded by DM-01 for adjudication; use DM-01 + companions going forward.

**Cross-refs:** [`CONTINUITY_SOURCE_OF_TRUTH.md`](../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md) · [`EXPEDITION_STRUCTURE_CANON.md`](../mechanics/EXPEDITION_STRUCTURE_CANON.md) · [`CONTINUITY_REPORT.md`](../../src/data/CONTINUITY_REPORT.md)

*Continuity A re-scan — 2026-07-30 (DM-01 + BB-01). No commit.*
