# Unity Rules Engine Development consultation

Captured from https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206, response `19ff2fcc-eec4-5053-9070-c0ae144c6030`, on 2026-11-03. This is product/source guidance, not new owner approval or execution evidence. Repository sources govern. The earlier ZIP remains unimported and its claimed historical tests are not counted in Engine results.

I checked **Engine at `935d14398da013e6b7fb411f73c8e5a63fd0c8ef`**, whose parent is your stated main base. Your CHR-02 work can continue. Several dependencies already have portable procedures; the remaining gaps should stay explicit rather than block that work.

The [current canon registry](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/docs/canon/CANON_MANIFEST.json) assigns conflicting combat rules to Core Systems. Below, **reviewed playtest** means an authored amendment available for provisional implementation—not recovered book canon, Chris’s approval of a new design, or release approval.

**1. Initiative, turns, reactions and clock transitions**

The exact source is [`COMBAT_ACTION_PLAYTEST.md`, “Encounter and action resources” and “Time and event ordering”](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#encounter-and-action-resources). Its source table distinguishes recovered rules from **NEW** reviewed interpretations.

Specified behavior:

- Initiative is `d20 + DEX modifier + legal bonuses`, highest first. **Players choose player/player ties; the Director resolves ties involving NPCs.** Keep the resulting ordered slots. Higher DEX, rerolls or entity-ID ordering are not supplied tie rules.
- A regular turn is the normal initiative slot, including when its creature cannot act. Extra turns are distinct.
- One **extra full Action per creature per numbered round**; it cannot generate another extra Action, Bonus Action or Reaction. This is separate from reaction refresh.
- Begin with one ordinary Reaction unless surprised or otherwise prohibited. Refresh only at the creature’s **regular turn start**—never at a round boundary or extra turn. Consequently, a late-initiative creature can react before its first turn, refresh, and react again that round.
- Surprise prohibits reactions until the first regular turn ends. Explicit additional-Reaction grants remain separate resources with their own restrictions.
- Ordinary reinforcements enter at round end and act next round. An explicit midround entrant acts this round only when its complete ordered slot remains upcoming; entry during that slot counts as passed.
- Extra turns do not refresh ordinary reactions, recharge, periodic/recovery ticks or regular-turn allowances.

Duration rules are also specified:

| Situation | Reviewed procedure |
|---|---|
| Hostile target-bound `N rounds` | Nth future regular target-end marker; exclude the current in-progress turn’s end. |
| Bare self/source/ally buff or source-controlled aura | Nth future source-start marker. Explicit timing overrides this default. |
| “Next turn” | Next future regular turn of the named creature. |
| Bare `N rounds` applied outside initiative | Absolute deadline `application time + N × 6 seconds`; entering initiative preserves it. |
| Initiative changes or removal | Existing effects retain their original repeating virtual marker; no restart. |

Regular-start ordering is: expire start-ending effects → refresh/recharge → due legal absolute recovery → death save → other start/periodic effects → voluntary decisions. End triggers, damage, saves and maintenance precede end-expiry. Simultaneous effects use recorded application ordering and printed internal ordering; extra turns never manufacture another regular marker.

**Portable reference:** [`combat_playtest_rules.py`](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/tools/combat_playtest_rules.py), particularly `ReactionClock`, `ExtraActionClock`, `reinforcement_first_round`, `marker_deadline`, `absolute_duration` and `ordered_effects`. These are bounded helpers; callers supply legal actions and scheduling.

**Transition still unresolved:** direct-exploration cadence, initial start/end marker phases, position conversion and pause policy. The helper explicitly says the scheduler supplies start/end ordering. Neither evenly dividing six seconds among actors nor advancing six seconds per actor is established.

[Expedition FL-03](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-03) does establish **one elapsed clock**, unchanged by entering initiative, Haven or another team. You can implement deadline preservation and marker identity now while leaving the unresolved cadence behind an explicit interface.

**2. Exploration movement, falling and digging**

A bounded tactical movement ledger is already specified in [“Movement and geometry”](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md#movement-and-geometry):

- Preserve **spent movement cost** across mode/Speed changes.
- Cap is `(1 + legal Dash count) × current mode Speed`.
- Terrain costs 1/2/3 per foot; strongest terrain applies, with additional crawl/squeeze costs.
- The reviewed **NEW** grid convention makes orthogonal and diagonal neighboring tiles five feet, with the stated blocked-corner restriction.

That does not settle direct-control running or the exploration collision model.

| Dependency | Current source and boundary |
|---|---|
| Running | `RULE_MAP.json` **EXP-01** explicitly leaves pace, geometry, collision and followers unresolved: tactical Dash does not define running input. |
| Jumping | [Jump card](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_PLAYTEST_STARTER.md#spell-jump) triples normal horizontal/vertical distance, still spends movement and requires legal landing. It supplies no baseline jump formula, trajectory or automatic hazardous-jump success. |
| Climbing | [Spider Climb card](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_PLAYTEST_STARTER.md#spell-spider-climb) specifies walking Speed on physically supporting walls/ceilings, hands free. This is spell-specific, not ordinary climbing. |
| Swimming/current | [`environment-foundations-local-draft-01/MODEL.json`, EF-06](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/docs/audit/2026-10-08/full-game/environment-foundations-local-draft-01/MODEL.json) contains proposed numbers, but explicitly says **unsubmitted/unadopted**, `newRulesAdopted:false`, `activeOperational:false`. Do not adopt them as rules. |

**Falling has a procedure**, rather than a complete gap: [`SPELL_INTEGRATION_RULES.md`, “Falling bridge”](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md#falling-bridge--new-provisional-procedure). It explicitly labels itself a provisional invention:

- Loss of support starts Falling immediately.
- Fix the first descent at the initiating regular slot’s end **next round**, then once per round there. Extra actions/turns and initiative changes do not move or multiply it.
- Outside initiative, when rescue/timing matters, establish order and use a virtual slot immediately before the first regular slot. Everyone receives one normal opportunity before descent.
- Ordinary descent is up to **300 feet per step**. Impact is `min(10, floor(uncontrolled distance / 20))d6`.
- Feather Fall retains **Action** activation, reduces descent to 60 feet per step and has its separate momentum-reset/impact rules.
- Positive falling damage produces Prone; genuine support ends Falling.

This can be implemented provisionally as written. It does **not** establish a physical gravity constant.

**Mining is not arbitrary digging.** [`MINING_CANDIDATE_GUIDE.md`, “Choose the procedure”](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/MINING_CANDIDATE_GUIDE.md#choose-the-procedure) supplies:

- Prospect: 10 active minutes.
- Assay: 1 active minute.
- Exposed extraction: normally 60 active minutes—5 setup, 50 removal, 5 sorting/receipt.
- One already exposed, workable parcel, at most **50 lb gross including gangue and 1 ft³**.

Its explicit boundary is: **“It promises no excavation rate or tunnel.”** General soil/rock removal, structural excavation, volumes, support collapse and tunneling require their own profiles. The [development brief §8](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/docs/unity/DEVELOPMENT_BRIEF.md#8-exploration-subsystem) supports explicitly permitted digging locations and expressly excludes arbitrary terrain destruction.

These are bounded findings, not proof that every historical book/archive lacks a traversal rule. The current mapping still records those dependencies as unresolved.

**3. Farming**

[`RULE_MAP.json`, MGT-08](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json) explicitly records:

> No complete ordinary crop/job procedure located in bounded reviewed sources.

It requires crop/site/input/time/yield/season/failure rules and AI assignment scope. Acceptance specifically says **Druidcraft does not replace farming**.

Therefore:

- Worker identity, reservations, scheduling and persistent job infrastructure are independently implementable.
- Crop growth, yield, tending intervals, unattended growth versus active labor, abandonment and seasonal consequences need source decisions.
- A generic Watch task cannot supply an unspecified crop result. Herbalism recipes and harvesting procedures likewise do not establish cultivation.

This is an explicit source gap to resolve together before presenting a concrete proposal to Chris—not grounds to fabricate a farming loop.

**4. Shared simulation, companion work and save/resume**

There are actual work rules to port:

- **[FL-02/03](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-02):** record activity, location, intended result, lead/assistants and actual start/end. No incompatible activities during the same seconds. Generic Watch work needs 480 **active** minutes; exact procedures retain their own interruption rules.
- **[FL-24](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-24):** Haven Turn means 24 elapsed hours, not automatic completion. Queue actual workers, facilities, materials and intervals.
- **[Crafting](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md):** reserve real ingredients; preserve one work-order identity and one completion roll. Completed phases persist; forced interruption loses unfinished progress in the current phase. Consumed quantities are deducted once at resolution or deliberate abandonment. `role=tool` does not override `consumed=true`.
- **[Fishing](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_RECIPE_PLAYTEST.md):** reservations precede commitment; first exposure commits opportunity/bait. Postcommit interruption does not refund them. Each six seconds credited as active work commits the worker’s Action and required hands.
- **Unattended traps:** five active setup minutes, passive fifty-minute soak, one scheduled check, then five active retrieval minutes. Catch remains physically in the trap. Handover preserves the original attempt, configuration, roll and pending event. No duplicate catch or automatic backpack delivery.

Do not generalize crafting interruption loss or trap passive-work permission to every job.

Also distinguish expedition workers from **source-bound combat companions**. [`CREATURE_LIFECYCLE_PLAYTEST.md`](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md#at-the-table) gives the latter owner-linked command/offensive allowances and an attached phase, not an independent turn or generic autonomous-worker entitlement.

**Engineering recommendation—not a new gameplay approval:** extend the existing transactional core with persistent job records, reservations and an ordered milestone queue. Each procedure supplies its own commitment, interruption, resumption and settlement behavior. Persist marker identities, pending choices, RNG, committed costs and result transaction IDs. Resolve each milestone once; visible and offscreen work read the same state.

That follows [brief §§6–7, 10 and 12](https://github.com/BordelonDevOps/DecenniumDescent/blob/935d14398da013e6b7fb411f73c8e5a63fd0c8ef/docs/unity/DEVELOPMENT_BRIEF.md). It does not choose a new player-facing save restriction. Either serialize interruptible resolution stages or explicitly select a supported save boundary; never discard pending effects.

**5. Earlier C# candidate: access and provenance**

The exact earlier archive is available here:

[DD_Unity_Rules_Foundation_v0_1_0.zip](https://chatgpt.com/library?file_id=libfile_b44b2459033c81918a9885c387791be8&account_id=personal)

- Source commit: `1a1a772b940fef551ba08967b6b34ed92abf3a95`.
- Archive SHA-256: `9ed9064b7b8d042cdf746bc5dbd963cbba7057c23ffd440c3302327ae1b23995`.
- Exact source hashes and attachment provenance: `DecenniumRules/Sources/implementation-provenance.json`.
- Historical execution evidence: `Validation/results.json` and `Validation/console-tests.log`, recording **76 standalone passing cases**. I have not rerun or integrated them into Engine in this review.

Potential selective reuse:

| Candidate path | Reuse boundary |
|---|---|
| `Runtime/TurnResources.cs` | Turn budgets, movement budget and duration arithmetic; not integrated into saved encounter state. |
| `Runtime/Vitality.cs`, `InjuryModifiers.cs` | Candidate implementations/tests to reconcile against current source bindings. |
| `Tests/RuleCases.cs` | Independent examples to adapt—not additive coverage merely by copying. |
| `Runtime/RuleSession.cs`, `SaveCodec.cs` | Separate architecture/schema; **not replacements** for the current Engine transaction/persistence implementation. |

The candidate’s microsecond clock is an engineering choice, not an approved global timing rule. Its saved state is incomplete for encounters/jobs, and its old manifest is not the current registry. Retain your widened arithmetic and existing foundation.

After CHR-02, the independently implementable sequence is **regular-turn/reaction/duration helpers → worker/reservation ledger → a source-bound fishing or crafting lifecycle with interruption and save/resume**. Direct running/jump geometry, general excavation and crop production remain explicit dependencies. No merge or repository changes were made during this review.
