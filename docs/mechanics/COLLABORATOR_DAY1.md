# Collaborator — Day 1 checklist

**Audience:** Someone joining Decennium Descent for the first time  
**Time:** ~2–3 hours (read + one smoke run + one small draft task)  
**Workspace:** `DecenniumDescent-main`  
**Parent onboarding:** [`docs/COLLABORATOR_ONBOARDING.md`](../COLLABORATOR_ONBOARDING.md)

**Morning owner:** Start with [`OVERNIGHT_HANDOFF.md`](./OVERNIGHT_HANDOFF.md) — waves status, naming locks, coffee-review draft queue.

---

## Morning — read before you edit (45–60 min)

| Order | Doc | Why |
|-------|-----|-----|
| 1 | [`COLLABORATOR_ONBOARDING.md`](../COLLABORATOR_ONBOARDING.md) | Chain of command, **draft flags**, **Director OK gate**, 17-class roster |
| 2 | [`src/data/CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md) | Approved terms — **Umbrin**, Umbra, Calan'thir, First Choir, **Resonance** |
| 3 | [`src/data/CONTINUITY_REPORT.md`](../../src/data/CONTINUITY_REPORT.md) | Audited items; open ASK OWNER rows |
| 4 | [`MECHANICS_ROADMAP.md`](../MECHANICS_ROADMAP.md) | Director Status — shipped vs draft |

**Gates:** Draft in `src/data/*` and `docs/` freely; keep `draft: true` on provisional entries. Lore → **Continuity**. Scope / acceptance → **Director OK** before treating content as product canon. ASK OWNER → human owner only.

---

## Midday — playtest smoke (30–45 min)

1. `npm run dev` → `http://localhost:8500`
2. Follow [`PLAYTEST_SMOKE.md`](./PLAYTEST_SMOKE.md) **Path A** (Umbrin Oracle) or **Path B** (Umbrin Mage)
3. Confirm: SAVE → SESSION load → Encounters/Generators **Load in Session** → Dungeon Guide **Mechanics** tab
4. `npx tsc --noEmit` — exit **0**

**Pass:** No red console errors; **Oracle Paths shows RC (Revelation Charges), not Weave RP**; Mage/Weave casters show RP pool; handoff brief on SESSION tab.

---

## Afternoon — lore + mechanics touchstone (45–60 min)

### Umbrin (product race)

Read [`UMBRIN_LORE.md`](./UMBRIN_LORE.md) (`draft: true`). **Umbrin** is the product demonym — not Drow, not Umbral Elf in new copy. Murkish · Obsidian Highborn · Obsidian Burn exile (`draft`).

**Optional:** One Murk factions bullet or typo fix — keep `draft: true`; run cosmology names past Continuity.

### Resonance (player-facing name)

Read [`RESONANCE_CANON.md`](./RESONANCE_CANON.md). Player-facing spell economy is **Resonance / Resonance Points (RP)** — **never "Hybrid-B"** in UI, sheets, or tooltips (internal code/docs label only).

| Track | Who | Pool |
|-------|-----|------|
| **Weave RP** | Wizard, Mage, Cleric, Druid, … | Resonance Points; reputation modifies max RP and spell cost |
| **Oracle RC** | Oracle only | **Revelation Charges** via **Paths** (Mystery / Curse) — no Weave RP tab |

Multiclass Weave: §7 formula + Builder secondary class dropdowns (or JSON `secondaryClass` / `classLevels`).

**Optional:** Wizard L8 + Cleric L4 in Builder → confirm Weave tab max RP reflects multiclass merge.

---

## End of day — report back

1. Smoke path completed? (Y/N + blockers)
2. One onboarding confusion
3. One draft item to promote next (Oracle mystery, Paladin oath, Umbrin lore, L11–20 table, …)

---

## Quick links

| Topic | File |
|-------|------|
| Chargen flow | [`CHARGEN_PROGRESSION.md`](./CHARGEN_PROGRESSION.md) |
| Session / rests / RP | [`SESSION_LOOP.md`](./SESSION_LOOP.md) |
| **Morning owner brief** | [`OVERNIGHT_HANDOFF.md`](./OVERNIGHT_HANDOFF.md) |
| Vague queue (P0/P1) | [`OVERNIGHT_VAGUE_QUEUE.md`](./OVERNIGHT_VAGUE_QUEUE.md) |

**Do not on Day 1:** Unity/Unreal, SWTOR assets, bulk rulebook txt edits, 18th class, ASK OWNER policy without owner sign-off.
