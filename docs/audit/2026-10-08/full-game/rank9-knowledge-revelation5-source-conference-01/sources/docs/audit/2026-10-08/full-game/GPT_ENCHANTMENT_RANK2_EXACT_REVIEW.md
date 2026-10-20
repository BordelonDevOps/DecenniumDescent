# GPT exact review — seven rank-two Enchantment spells

Source: Calibration Review, ChatGPT conversation `6a7a0fa2-eee0-83ea-92e9-6723a9f67ede`.
Actual reviewed turn: `00bba327-328e-4d29-ab68-e74fce17e831`; agent message: `e51c8c66-5c43-4d22-bce7-fdcbad2f7a21`.
Captured through the app reader after Chrome showed Response complete. Full response below; app source-reference markers are retained as returned. Scope is provisional manuscript approval only.

---

I read all **three ordered attachments together** and have the complete submission: all seven cards, shared literal/default fields, the full proposed `ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md`, and the five unchanged class evidence cards. :chatgpt-content-reference{index="0"} :chatgpt-content-reference{index="1"} :chatgpt-content-reference{index="2"}

**Disposition: all seven cards and the shared Enchantment-control integration are APPROVED for this bounded manuscript stage. I find no required functional repair.** The interpretations below are binding exact-review clarifications of the submitted text; they do not promote the cards yet.

## Six requested completion decisions

### 1. Shared virtual control cycle/budget — APPROVED

Approve one open **virtual control cycle and one ordinary behavior budget per target**, not one per spell.

The exact scope is:

- Dire Charm and Crown of Madness use the recurring virtual START/END cadence when established outside initiative.
- If both coexist on one target, they share that same six-second cycle and the same Action/movement/interaction economy.
- A later cast during an already-open cycle gets **no fresh START and no replenished behavior budget**.
- One-shot Command, Confusing Flash, or Illusive Commands does **not** gain a new repeating cadence from this overlay. However, if its compelled behavior falls into the same current six-second/regular-turn opportunity, its demand competes for the **same actual remaining behavior budget** through Compelled Budget Arbitration.

So the rule prevents multiplying Actions while avoiding a retroactive timing rewrite of the older one-shot spells. The submitted integration supports that distinction. :chatgpt-content-reference{index="3"}

### 2. Entering initiative with an already-used virtual cycle — APPROVED

Approve exactly:

- already-received virtual START/order opportunity is not replayed;
- Action/movement/interaction already spent in that open virtual cycle remains spent when mapped into the first actual regular turn;
- those budgets are not refilled merely because initiative was established;
- the next still-unresolved repeat save occurs at that first actual regular turn's END;
- later cycles use normal real regular START/END markers;
- the original absolute spell deadline remains unchanged.

One important interpretation: **ordinary actual regular-start processing still happens** at the first real regular turn—Reaction refresh, recharge/death-save/start effects, etc., under the normal combat rules. What does **not** replay is the Enchantment control START/order opportunity or already-spent ordinary behavior budget. The virtual START explicitly was not itself a manufactured combat turn or resource-refresh event. :chatgpt-content-reference{index="4"}

No text repair required.

### 3. Illusive Commands partial replacement — APPROVED

Yes.

If a new failed-save Illusive Commands instruction contains:

- a hard Action component that is blocked; **and**
- an independently valid soft movement/interaction component,

the surviving soft component is a genuinely established new instruction and **replaces the prior pending Illusive Commands record**.

Example: an instruction effectively requiring “walk to the altar and perform [blocked whole Action]” may still establish the legal walking portion if that portion independently satisfies the authored instruction.

By contrast:

- saved-against cast → no replacement;
- wholly invalid instruction → no replacement;
- hard component blocked **and no independently valid soft component remains** → no replacement.

This matches the exact card's “at least one valid component” rule. :chatgpt-content-reference{index="5"}

### 4. Dire Charm repeat saves stop when its application is empty — APPROVED

Yes.

Each cast/application ID schedules repeat saves only while **at least one component originating from that application remains active**.

Therefore:

- Charmed-only application keeps its saves until that Charmed component ends.
- servant-only application keeps its saves until servant control ends.
- full application keeps saves while either component remains.
- when replacement/removal leaves that old application with **zero components**, stop scheduling its saves immediately.
- an old application's already-scheduled save can never remove a replacement component belonging to another application.

No hard-control allowance is refunded. :chatgpt-content-reference{index="6"} :chatgpt-content-reference{index="7"}

### 5. Native Attack Action and ammunition — APPROVED

Dire Charm and Crown of Madness may command an **ordinary Attack Action**, which means the target receives exactly the attack sequence its ordinary Attack Action inherently provides:

- inherent Extra Attack;
- native NPC Multiattack when Multiattack actually is that creature's ordinary Action;
- normal weapon/natural/unarmed sequence belonging to that Action.

It grants **no extra Action or extra attacks beyond that Action**.

Ordinary required ammunition is spent normally. That includes normal arrows, bolts, bullets, etc. It does **not** authorize compulsory expenditure of:

- magical/special limited ammunition with a distinct expendable feature;
- consumables;
- charges;
- RP;
- spellcasting;
- recharge/per-rest abilities;
- optional finite class resources/riders.

If the order leaves attack method open, controller chooses another legal ordinary method if available. If none exists without forbidden resource expenditure, the instruction fails.

**Confusing Flash remains expressly different:** its source-specific authored procedure compels **exactly one ordinary attack**, not the target's full Extra Attack/Multiattack sequence. The shared rule expressly preserves that exception. :chatgpt-content-reference{index="8"}

### 6. Arbitration overlay applies to existing Command/Confusing Flash — APPROVED

Yes. This is a **NEW cross-spell integration rule**, not a rewrite of those frozen cards.

Compelled Budget Arbitration expressly applies to:

- existing **Command**;
- existing **Confusing Flash**;
- Illusive Commands;
- Dire Charm;
- Crown of Madness.

Their own effects, durations and source-specific limits remain unchanged.

Priority is based on the **specific mandatory instruction**, not simply oldest underlying ongoing spell:

- Command / Confusing Flash / Illusive Commands → timestamp when their instruction successfully establishes.
- Dire Charm / Crown → timestamp each turn when that specific order is issued.
- genuine simultaneity → underlying effect application order, then stable source/mechanical ID.

Earlier valid instruction claims an indivisible budget first. Compatible demands can be fulfilled by one genuine execution. Later incompatible demands receive no duplicate Action/inter­action/movement. A losing ongoing instruction remains active but ineffective for that contested opportunity; it is not dispelled and gets no refund. :chatgpt-content-reference{index="9"}

This also preserves the two existing points you highlighted:

- Command **Grovel** does not inherently consume the Action; becoming/remaining Prone can coexist with another Action when actually legal.
- Confusing Flash Attack remains exactly its authored **single attack**, despite the general ordinary-Attack-Action rule.

---

# Per-card exact status

### Zone of Truth — APPROVED

Both placements/access modes are preserved correctly. Unified fixed 15-ft-radius geometry, concentration minute, one CHA save per first eligible exposure/application, total-cover suppression/resumption, deliberate-lie definition and no save-result oracle all remain consistent.

Divination rank 4 remains Divination/7 RP only for Cleric/Ranger/Shaman access; Enchantment rank 2 remains Enchantment/3 RP for its actual classes. The behavioral restriction itself is not information acquisition for Protection from Scrying purposes. :chatgpt-content-reference{index="10"}

No repair.

### Deep Mesmerize — APPROVED

CHA save, actual Stunned only, two future target-END duration, positive post-defense/pre-temp-HP damage ending, no rank-1 unaware import, and normal hard-control handling are all correct.

No repair.

### Dire Charm — APPROVED

The split-component architecture, same-caster Charmed refresh, cross-caster servant replacement, application-ID saves, native Attack Action, ordinary ammunition, per-turn audible/understood conscious orders, and no continuing 30-ft tether are all approved.

No repair.

### Group Pacify — APPROVED

Initial 15-ft-cone enemy snapshot, independent WIS saves, concentration minute, prospective prohibition on new hostile commitments even in an already-running fight, recognized-ally provocation and no hearing tether are correct.

Its broad hostile-initiation restriction is still a categorical restriction rather than automatic whole-Action denial.

No repair.

### Illusive Commands — APPROVED

Short simple instruction rather than one word, WIS/hearing/language, next-turn execution, soft/hard component split and partial replacement rule are all approved.

No repair.

### Calm Emotions — APPROVED

Fixed 20-ft-radius sphere, first eligible exposure history, one acceptance/WIS result per application, temporary cover suppression/resumption, and suppression specifically of actual **Frightened mechanical effects** are correct.

The five class comparison cards support the manuscript's restraint: Mooncursed, Momentum Rampage, Divine Fury, Fury of the Host and Beast Empathy do not become disabled merely because their names/flavor involve emotion. Only actual Frightened components are suppressed where applicable. :chatgpt-content-reference{index="11"}

No repair.

### Crown of Madness — APPROVED

Application-only Humanoid gate, WIS, concentration minute, non-Charmed control, movement + one ordinary Action, native Attack Action, mental order/no sensory feed, repeat END saves and cross-caster Crown replacement are coherent.

No repair.

---

## Shared manuscript status

`ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md` is **APPROVED for inclusion with this spell batch**, subject to the normal provisional-playtest status.

Specifically approved as NEW shared rules:

- ordinary compelled Attack Action semantics;
- split application/component IDs;
- Compelled Budget Arbitration;
- one shared outside-initiative virtual control cycle/budget per target;
- carry-forward into first actual regular turn;
- fixed-zone eligibility/save history.

These are authored tabletop integration procedures only. As the manuscript itself correctly states, they are **not claims that the stateful runtime scheduler already implements them**. :chatgpt-content-reference{index="12"}

## Overall disposition

**No required functional repairs.**

All seven exact rank-two Enchantment cards **and the accompanying shared Enchantment-control integration manuscript are approved for provisional manuscript promotion when Codex performs the promotion step.**

Current state remains **222 reviewed / 626 unfinished** until that promotion actually occurs.

This review does **not** approve runtime implementation, numerical/human balance, final game flow, GitHub push, whole-game closure, publication, or cosmology. Cosmology remains owner-deferred until **after the authorized GitHub push is completed and the remote commit is verified**.

