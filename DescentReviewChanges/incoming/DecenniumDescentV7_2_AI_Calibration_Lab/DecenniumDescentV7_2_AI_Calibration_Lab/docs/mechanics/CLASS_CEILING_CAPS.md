# Class ceiling caps (GM fiat / draft)

**Status:** Permanent **GM-fiat** playtest guardrails until author-promoted — **not** auto-enforced rules. Derived from `BALANCE_PLAYER_CLASSES.md` §3 outlier risks. These caps bound action economy, copy limits, aura stacking, resource overflow, and deployable multiplication until full rules are authored.

**Continuity:** Worker 3 · 2026-07-30 · T1–5 ship label 2026-07-31

**Companion data:** `src/data/class-ceiling-caps.js` (Builder/Sheet informational callouts — labeled GM fiat)

---

## How to use

- Director **announces** the relevant cap before it binds a player; companion callouts are reminders only.
- Apply at the table **before** promoting any L11–20 draft milestone or Oracle/Paladin draft tree to canon.
- When prose and caps conflict, **caps win for playtest**; log conflicts for author review.
- All values are **ceilings**, not targets — staying under a cap does not imply balance.

---

## Mirrorsage

| Category | Draft cap | Notes |
|---|---|---|
| Actions / round | **1** witnessed copy release (action or bonus action, not both) | Spell Mimicry + echoed abilities share this limit |
| Echo slots | **6** concurrent witnessed spells (L11+); **1** permanent Infinite Reflection slot (L20) | Swapping schools ends prior hold unless milestone says otherwise |
| Copy eligibility | No legendary, 1/day, 1/encounter, or boss-unique effects | Copied ability cannot exceed source owner's level-gated tier |
| RP discount | Half-cost echoes **min 1 RP**; max **2 RP** total discount per round from Adaptive Resonance | First echo each encounter at half cost still respects min 1 |
| Mirror Beast shifts | **2** per encounter (L16+); shift never grants extra copy release that round | Focus +1 per battle (L18) does not add actions |

**Playtest ledger:** Track echo slot contents, copy releases/round, RP spent on echoes.

---

## Oracle

| Category | Draft cap | Notes |
|---|---|---|
| Revelation Charges | **3–7** pool; **no** short-rest recovery | L11 draft raises cap to 7; income is trigger-based only |
| RC recovery / round | **1** RC regained per round from **all** Prophecy Triggers combined | Failed-save regain (L16 draft) counts toward this cap |
| Actions / round | **1** Revelation activation per round | Tier III (3 RC) counts as one activation |
| Turn denial | **1** hard deny (stun, skip turn, auto-fail) per **target** per encounter from Revelations | Soft control (disadvantage, −2) not capped here |
| Prophetic Surge | **1/day**; cannot same-round stack with trigger RC regain above the 1/round cap | Grand Revelation foreshadow (L17) is narrative, not extra RC |

**Playtest ledger:** RC start/end per round, trigger source, revelation names activated.

---

## Paladin

| Category | Draft cap | Notes |
|---|---|---|
| Actions / round | Extra Attack + **1** Divine Smite **or** 1 leveled spell (not both smite riders) | L7 reactive Smite/spell trigger counts as that one rider |
| Aura stacking | **One** Paladin aura radius active; **one** reactive aura trigger per round | L6/L7/L15 auras do not stack bonuses — take highest |
| Lay on Hands | Pool = **5 × level**; max **50%** of remaining pool spent per round | Full Cleansing Wave (L17, 1/rest) exempt from per-round spend cap |
| Aura Surge | **1/rest** (L17 draft) | Does not grant extra actions beyond normal turn |
| Oath revelation smite | **1/long rest** apply revelation rider without slot (L16 draft) | No duplicate hard control on same target from oath spells |

**Playtest ledger:** Smite uses, LoH spent, aura triggers, oath spell riders.

---

## Warrior

| Category | Draft cap | Notes |
|---|---|---|
| Mutation slots | **3** prepared (L11+); **4** for Apex Form **1/encounter** (L20) | Preview slot (L18) is temporary 3 rounds, double strain on expiry |
| Mutations / round | **1** activation per round; Reflexive Mutation **1/round** (L17) | Serum Overclock (L9): 2 serums at once counts as 1 activation |
| Actions / round | Action Surge + **1** mutation activation max in the same round | Brutality Threshold unlock **1/short rest** |
| Toxicity strain | Allies take **half** strain when sharing (L16); one ally ignores strain **1/encounter** | Preview slot expiry applies **double** strain to self |
| Damage gate | Brutality Threshold at **100% max HP dealt** unlocks Transcendent tier **3 rounds** | Resets on short rest |

**Playtest ledger:** Active mutations, activations/round, strain applied, Brutality Threshold triggers.

---

## Dragoon

| Category | Draft cap | Notes |
|---|---|---|
| Momentum cap | **5** (L1–12); **6** (L13+); overflow above cap → temp HP = **tier floor × overflow stacks** (L17) | Overflow does not raise cap further |
| Overflow damage | **+1d6 per stack above cap**, max **+2d6/turn** from overflow (L12+) | Apex Assault landing damage included |
| Actions / round | Extra Attack + **1** Wyvern's Flow **or** Apex Assault (not both full leaps) | L17: 1 free Apex at max Momentum **1/encounter** |
| Momentum refund | **1** Momentum refunded per turn from Wyvern's Flow on hit (L13+) | Dragon's Roar and similar do not stack refunds same turn |
| Sky Sovereign (L20) | **1/day** 1-minute mode; opportunity-attack immunity does not add extra attacks | Difficult terrain on landing tiles persists 1 round |

**Playtest ledger:** Momentum start/end, overflow stacks, leaps/round, refund sources.

---

## Tinker

| Category | Draft cap | Notes |
|---|---|---|
| Concurrent deployables | **3** gadgets (L16+); only **2** autonomous actors may take independent turns; **2** Anacite Drones share one HP pool | Dual Drone (L11) uses shared deploy action economy |
| Flask / bomb capacity | **4** concurrent (L11+); remote detonation **60 ft**, no LOS (L13+) | Danger Close (L15): ally-safe detonation only |
| Deployable HP | Base threshold + draft **+2** milestones; **Mech Overdrive +2** when overcharged | No single deployable above **2 × character level** HP (draft ceiling) |
| Damage | Overcharge **double** on one device **1/short rest** (L17); first remote detonation **+5 ft** radius **1/encounter** | Friendly fire redirects per Danger Close |
| Duration | Encounter unless **Mech Overdrive** (L20): one gadget permanent for battle | Permanent gadget: first activation each round **no action** |
| Actions / round | **1** deploy + **1** remote detonation; activating **2** deployables same turn = **1 bonus action total** (L16) | Shared once/turn deploy economy for drones |

**Playtest ledger:** Deployable count, HP remaining, detonations/round, overcharge uses.

---

## Cross-class notes

- **Resonance:** Mirrorsage (hybrid), Paladin (half), Dragoon/Tinker (minor) use draft RP curves — caps here do not replace RP pool limits in `resonance-economy.js`.
- **Multiclass:** Apply each class's caps to features from that class; action economy caps are **shared** across classes (still one copy release, one revelation, etc., per round total unless author rules otherwise).
- **Promotion:** Any cap marked draft here must be revalidated when corresponding `class-draft-levels.js`, `oracle-mysteries.js`, or `paladin-oaths.js` entries graduate from draft.

---

## Worker 3 continuity

- Created this document and `class-ceiling-caps.js` from `BALANCE_PLAYER_CLASSES.md` §3 outlier list.
- Builder/Sheet show informational **Draft ceiling caps** callouts for the six flagged classes only.
- No class kit rewrites; no numeric promotion to canon.
