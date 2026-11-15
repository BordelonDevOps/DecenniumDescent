# CHR-03 complete earned Cleric settlement contract

Status: **DRAFT HELD FOR TAC-05 FRIGHTENED PREREQUISITE.** Actual dependency response `aee19602-eb93-5f80-b5f7-90dd14d2fcee` selects its separate source/API contract, implementation and acceptance before complete CHR-03 contract review; Codex agrees. [Exact dependency decision](GPT_DEPENDENCY_REVIEW.md). Context guidance `68898ea2-4ba8-52e5-afe9-ac081a2dbd12` is approved and Codex agrees; runtime implementation still requires actual review of this complete contract.

Baseline: `459b8bf54ea46ecf45a0622ce99d5f18a77bd57f`, after actual TAC-07 acceptance `cfcdfb41-f117-51a3-a87b-34a665b97b6d`. The accepted runtime source is `8d90200ed57bd59e4d7814deea2b4c9fe1073dc5`; the final predecessor evidence is `e89b4b5459172778303fba899bb6a262131173fe`. This contract completes the earlier CHR-03 source audit, whose actual response `b6c973bf-8890-57ea-b9e4-135b527b2ad9` approved the milestone and retained Radiance/Judging Light/Conviction Pool while holding implementation.

## Authority and dependency order

The canon manifest remains the single source registry. Gameplay bindings retain revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4` and their reviewed/provisional playtest status. Neither a successful build nor this contract promotes source content.

The approved map retains CHR-03 ← CHR-02, TAC-07 ← CHR-02/FND-05, TAC-08 ← TAC-02/TAC-05/TAC-07, and CHR-05 ← CHR-03/TAC-02/TAC-05/TAC-08. The accepted initial repertoire and detached settlement interface satisfy a concrete prerequisite of this selected Cleric advancement; they do not change the separate map branches. This module must connect that interface to a real earned transaction.

The selected new opt-in TEST_ONLY profile begins with the accepted initial Cleric companion, actual class entry, five source-qualified initial spells, the original once-only RP funding3, shared character/life/Hit Die/grant/resource state and the same connected expedition. It must not manufacture an already advanced character, retroactively amend wire106, or replace the companion. Allocate the next explicit wire/envelope only after contract approval. Authentic wire95–106 behavior and byte formats remain supported.

## Source obligations and exact selections

| Source obligation | Selected implementation consequence |
|---|---|
| Character creation: Gain a level; XP Advancement: preannounced Opening milestones | One genuine preannounced objective, earned from actual campaign outcomes; separate trusted award and once-only consumption. No kill XP, manufacturing XP or arbitrary client award. |
| Cleric chassis: d8 and later fixed HP base5; CON10 | Append chronological Cleric level2/base5 and one unspent d8. Total level2/PB2. Raw maximum8→13. Preserve existing current HP, old die state and independent life facts. |
| Shared RP and Cleric progression3→4 | Reconcile the existing shared pool's maximum to4. Preserve current RP and original funding. Advancement supplies no new funding, recovery, RNG or elapsed time. |
| Cleric engine8/9 and automatic Attunement | Gain `cleric.base.invocation-attunement` and exactly the selected `cleric.base.radiance.radiance` supplement, at the advancement revision. No other path bonus; no free path replacement. |
| Cleric schedule1: choose2 Base, no active minimum, no ASI | Select exactly `cleric.base.judging-light` and `cleric.base.conviction-pool`. Automatic/path grants do not consume these two choices. No banked choice, Saint, Bishop, Divine Invocation or Divine Smite grant. |
| Conviction engine1/11 and Pool card | Source-derived capacity3 at Cleric1, then5 at Cleric2 with Pool. Current amount is explicitly unavailable. No zero/full balance, funding, spend, recovery or invented Long Rest. |
| Shared repertoire fallback and accepted TAC-07 binding | Retain all five initial records unchanged; append exactly `detect-magic` with EarnedClassLevel provenance, Cleric2/chronological2, the actual consumed milestone and the advancement revision. Cleric2 does not unlock rank2. |
| Radiance and Healing Rite cards | Execute Radiance on an actual qualifying paid Healing Rite, through shared life and condition handling. Merely owning a path ID is insufficient. |

Source choices are fixed admission for this bounded build, not a statement that these are the only lawful Cleric choices. Other paths/cards/spells must receive explicit unsupported diagnostics rather than substituted grants. Judging Light has no trigger while Divine Smite is unowned. Fervent Ritualist does not change Action-time Healing Rite. No Consecrate terrain is created, so the existing Consecrated Ground passive has no fabricated trigger.

## Announced, earned, awarded and consumed milestone

At fresh startup, before any campaign command, require an immutable Director-authored declaration of one TEST_ONLY milestone: complete both existing genuine encounters and the actual specimen-to-recipe-4 batch, then close the later encounter lawfully with the companion alive. Bind the exact actor, fixed milestone ID, declaration/source digest, revision0, encounter identities, specimen identity and batch definition. Construction validates all initial choices and the declaration before creating state or funding.

This is the previously approved authored objective under the source's preannouncement permission, not a new universal reward formula. Its objective does not require spending RP. The primary acceptance witness does spend RP before completion. “Alive” is not a newly invented positive-HP threshold: death and current HP retain their existing distinct meanings. The objective supplies no teleport, free Haven trip, additional encounter, recovery or compulsory waste.

Completion must derive from the actual earlier closure, actual consumed specimen and settled batch, and normal later closure after its genuine combat outcome and outgoing-slot consequences. Record its causal identities, revision and shared-clock stamp only when those predicates become true. A pending/partial closure, incapacitated hostile, unconsumed ingredient, merely reserved order or client completion flag is insufficient. Preserve existing closure transactions and all intervening clock/death/reaction effects.

Completion creates eligibility; it does not award or advance automatically. Reuse `AwardCharacterMilestone` under trusted host authority with the fixed declared actor/ID and revalidated evidence, then persist the existing milestone record and the objective provenance. An award is effective once. A valid duplicate request may return its existing receipt only after current authority checks. A new request to award the same entitlement rejects unchanged. Preserve the older Soldier award semantics under their original profiles.

Award, save, advancement and later continuation are distinct commands. The user can inspect declaration/completion/award/consumption separately. A missing, unearned, mismatched, consumed or forged entitlement cannot be replaced by a caller-provided reward count, source, class level or completion assertion.

## One atomic advancement using shared state

Extend the existing `AdvanceCharacterLevel` request/receipt path with immutable Cleric choices: the exact class path, fixed-average method, two selected card IDs, Radiance Invocation choice and one ranked spell ID. Technical payload field names may follow existing conventions; the semantic request cannot contain target HP, RP/Conviction balances or capacities, a proposed level, source hash, funding event or reward amount.

Use one common assessment for query and execution. Check actual class/profile, source/initial provenance, living/dead state as admitted by the existing advancement path, unconsumed earned entitlement, complete choices, source card/class-level requirements, automatic-versus-selected counts, distinct identities, history capacities, prior Hit Die consistency and the existing tactical/pending-choice/work/traversal restrictions before mutation. Reject unsupported contexts explicitly; never repair them by healing, standing, ending conditions or canceling jobs. Query consumes no RNG, time, resource or entitlement. Current host/seat authority precedes idempotency.

Stage all of the following in the same normal simulation transaction:

1. Append Cleric2/base5 to the existing chronological character; preserve abilities, skills, saves, equipment/training, first-class selection and source revision.
2. Append one unspent d8 at ordinal2; preserve ordinal1 and its spent state.
3. Add the two selected cards and separate automatic Attunement/Radiance grants with actual milestone/revision provenance. Persist exactly one Invocation path.
4. Recalculate raw/effective maximum HP through the shared capacity/life machinery. Preserve current HP subject only to the existing capacity clamp; do not award the newly available HP, change temporary HP, wounds/injuries, Stable/dying/dead facts, posture or independent conditions.
5. Reconcile the existing RP pool to maximum4, preserving current RP and the original funding record.
6. Derive and persist Conviction capacity5 from the same class/grant facts, with current amount unavailable and no spend/recovery interface.
7. Consume the actual milestone, append the matching advancement history, and invoke accepted `SettleClericEarnedRepertoire` on that staged history to append Detect Magic once.
8. Validate the complete result and commit one receipt/revision.

A failure in any step discards the entire staged change, including milestone consumption, grants, capacity changes and knowledge. Do not expose an independent “give spell” operation. `AcquireEarnedSpell` outside this transaction stays unsupported; ordinary casting stays unsupported for all six owned identities. The actual helper must see the genuine staged class, consumed entitlement and matching advancement record, rather than a detached fabricated stand-in.

Advancement does not advance the shared clock or RNG, restore HP/RP, reset cadence/Actions, spend stock, change work or simulate a rest. The required primary transition is HP8/8→8/13 and RP1/3→1/4, with the exact first funding unchanged. A legal secondary branch may preserve RP3→3 while raising the maximum3→4.

## Conviction capacity without a fictional balance

Add a source-bound capacity record/projection associated with the existing actor and owned Divine Favor engine. Bind the Cleric source revision and selected Pool card provenance. Before advancement its maximum is3; after the source-qualified Pool acquisition it is5. Validate each against chronological class/grants and the recorded advancement. Neither constructor nor restore accepts a caller-supplied maximum.

Represent the current amount as unavailable, not numeric0 and not full. Public views expose capacity and the unavailable-current status together. There is no usable balance, funding history, generator, payment, short-rest restoration or long-rest restoration in this slice. Reject forged numeric current values, second Pool acquisition, wrong source and a capacity not supported by the current grants. This fulfills the selected passive's capacity effect under actual prior GPT/Codex agreement without claiming the broader Conviction engine.

## Actual Radiance settlement

The only executable healing Rite in this build is the accepted single-target Healing Rite. Its legal target is therefore the only possible actually healed beneficiary. Use the same source-bound Action/2RP payment, shared S d8+M draw and ordinary healing path; at Cleric2, S=1 and M=2. Preserve range, sight, line of effect, living-target, body, condition, Action and resource checks, including the current periodic-rider interaction boundary.

After the base Rite resolves, qualify Radiance only if it restored positive actual HP to the living target, occurred on the Cleric's admitted own turn, the correct path is owned, and this actor has not used Radiance for that turn. A full-HP or wholly healing-prevented Rite may still pay its lawful base cost but creates no Radiance trigger and consumes no Radiance use. Positive pre-cap healing potential alone is insufficient.

Apply S=1 extra flat HP through the same shared healing limits. Record base healing and additional potential/actual gain separately, with one source Rite ID and one turn identity. Even if the additional HP clamps to0, a genuine qualifying base heal can settle the optional cure; extra HP is not a second Rite, does not roll again and cannot recursively trigger itself or another once-per-Rite modifier.

Proposed single-target choice API: the normal Rite command may carry an immutable conditional cure preference `None`, `Frightened` or `Poisoned`. Beneficiary is the actual base target and cannot be redirected. Validate the enum and authenticated recipient-choice authority before payment. The conditional choice applies only if Radiance actually triggers; it does not cause a full-HP Rite to become a trigger. The recipient's optional decision must not be silently chosen by an unauthorised caster/seat. The supported connected host controls both actors; unsupported cross-seat decision flows must be visible. No general pending multi-target Rite is claimed.

A selected cure must end present, eligible, unexpired records of the chosen condition, including suppressed eligible records, while preserving protected-source exceptions, independent conditions, tracks and components. Poisoned has an existing source-qualified generic named-condition lifecycle. Frightened does not: the current ConditionKind/ConditionHistory rejects that identity, and the existing ConditionClause is only a derived modifier. Its authoritative fear-source relationship, application/end/cure history and actual behavior are the concrete TAC-05 prerequisite selected by actual response `aee19602-eb93-5f80-b5f7-90dd14d2fcee`; this contract cannot claim that branch works or silently reduce Radiance to Poisoned-only. It removes neither wounds nor an underlying Intoxication/Addicted/other independent source merely because that source contributes a Poisoned effect. It does not clear both named conditions, stand the target, restore dropped items or undo prior effects. No eligible record means no cure mutation; retain the lawful healing event rather than manufacture a condition to remove.

Track use by actual actor, calendar epoch and admitted turn/start identity, with the causal Rite and committed revision. Persist history through save/load and control-mode changes. The retained record, not a UI flag, prevents second use. The selected profile has one admitted Action-time Rite and no extra-turn engine; it supplies no new extra Action/turn, off-turn trigger or recharge. Any future broader turn semantics require their own source binding. Reconcile condition consequences and incompatible work through the existing lifecycle path.

Payment, base healing, Radiance extra healing, optional cure, once-per-turn use, RNG state and histories commit atomically. All payload, context, authority and storage-capacity failures reject unchanged. Keep the old level1 wire105/106 path unchanged; only the new profile admits Cleric2/Radiance.

## Approved context: finite post-closure Rite

Actual guidance `68898ea2-4ba8-52e5-afe9-ac081a2dbd12` approves the following as a **NEW bounded TEST_ONLY consensus admission**; Codex agrees. [Exact guidance and scope](GPT_CONTEXT_GUIDANCE.md). The whole contract still needs actual review before implementation.

The primary route has RP1 after advancement and cannot pay another Rite. The alternate genuine connected route preserves original RP3 through the same two encounters and batch, earns/awards/consumes the same declared objective and advances with current RP3 unchanged. It pays one actual post-advancement Rite3→1 on retained real combat injury, with enough recoverable HP for the extra1 to land. Both branches retain genuine earning, save/replay and paid continuation.

Only the new profile, after genuine normal closure and lawful advancement, admits the owned Healing Rite at the Cleric's actual current slot in its retained actor calendar. Use `WorldTiming.ForActor(state, actor)`. Closure clears `Encounter`; `ForEncounter` then falls back to the original calendar and must not identify this post-closure Cleric turn. Require the owning epoch's `SlotAt(RuleClock)` to agree with its processed cursor, its ordered slot actor to be the Cleric, and its local latest regular start to identify that current own slot. The existing interval Action must be unspent, with ordinary physical, living-allied-target, sight/range/line-of-effect, body, authority/revision, busy-state, pending-choice and supported-interaction checks intact.

Radiance use is keyed by actor, owning epoch ID and exact local regular-start marker. The reinforcement interval's `LastStart` uses global encounter numbering; compare it through the phase's local/global conversion and never treat it as an epoch-local ordinal. Save both the causal marker and enough immutable phase provenance to validate that conversion. A wrong original epoch, local/global substitution, reused marker, off-slot activation or stale/unprocessed boundary rejects unchanged.

Resolve every due boundary consequence before voluntary input. Neither advancement nor activation refreshes an Action, creates an allowance or banks skipped turns. The Rite pays the existing Action and2RP, consumes its normal shared healing RNG, and adds no elapsed time. Reach another slot through actual ordinary world advancement or paid movement; pause/load/mode changes provide no refresh. The preserved calendar may continue to contain resolved hostiles without resurrecting them or creating another encounter.

This admission interprets outside-tactical own-turn timing for this specific finite Healing Rite/Radiance context. It grants no general out-of-combat technique policy, spellcasting, new initiative acquisition, extra encounter, fake rest, RP/Conviction recovery or resource funding. A detached level2 fixture cannot replace the connected witness.

## Persistence, query and public boundaries

Persist the new declaration/completion/award linkage, exact advancement choices, four new feature grants, Invocation choice, source-bound Conviction capacity, earned KnownSpell record and Radiance use/effect history in the new envelope. Reuse existing character, milestone, Hit Die, life, RP, clock, RNG, inventory, condition and receipt ledgers; add only genuinely missing provenance/behavior state.

Strict restore must reconstruct the initial state and real command history and validate all causal links. Reject forged early/duplicate completion, award or consumption; class/grant/path/HP/RP/Conviction capacity changes; fabricated funding/current Conviction; wrong earned spell/source/placement/entitlement; orphan Radiance use/cure; mismatched calendar identity and changed recorded outcomes. A structurally valid detached helper result is not sufficient.

Owner views must show the declaration and objective status, actual lawful advancement choices or exact denial, before/after capacities with current values preserved, initial versus earned known spells, Invocation/Radiance source ownership and actual use, unavailable Conviction current and unavailable casting. Foreign/revoked seats must not receive hidden actor/source choices or authority. Typed commands and the console must reach the same assessment/resolver; parser-only errors are not substantive rejection evidence.

Preserve old wire95–106 constructors, fingerprints, payload layouts, canonical bytes and public property shape. No implicit backfill, migration, source repair or automatic grant to a restored old save. Cross-profile restore rejects unchanged.

## Required connected acceptance and controls

**Primary campaign:** retain actual exploration, first encounter, physical specimen/mining/acquisition, management/research/manufacture, preparation and later combat. Use a real Healing Rite on genuine injury before objective completion, leaving RP1. Close lawfully with the companion alive; record earned eligibility, award once, save, advance the same actor and consume once. Show HP8/8→8/13, RP1/3→1/4, old die unchanged plus one unspent d8, exact four new grants/one path, Conviction capacity3→5/current unavailable, initial five spells unchanged plus actual earned Detect Magic. Clock/RNG/funding/stock remain unchanged across advancement. Continue by paid ordinary movement. Demonstrate insufficient RP unchanged after advancement.

**Radiance campaign:** start from the same lawful initial profile and declaration; genuinely earn the objective while preserving original RP3 and enough real combat injury to leave room for a positive extra1 HP. Advance without healing or RP recovery. Use the reviewed post-advancement context for an actual Action/2RP Rite, its normal RNG/base healing and positive Radiance gain; preserve six unspent manufactured doses. Save before and after the trigger and continue by paid movement. The eventual executable stream must establish actual numerical results; this document does not assert an unrun die or HP outcome.

Both campaigns require uninterrupted console, restored console, receipt replay and independent typed dispatch with canonical checkpoint byte equality. Preserve each real denied/retried input's full before/after bytes; name parser-only controls separately. Save around declaration, earned completion before award, award before consumption, advancement, actual Radiance settlement and paid continuation. Do not replace either campaign with detached mutation tests.

Focused negative and mechanical controls additionally cover illegal/missing/duplicate/automatic-as-selected choices, wrong class/path/rank/source, consumed/unearned entitlement, authority-before-retry, stale revision/conflicting IDs, busy/traversal/tactical/pending choice, unchanged clock/RNG/HP/RP/funding, old spent Hit Die and injury/life facts, atomic rollback if earned settlement fails, source/ledger/envelope forgery, full-HP/nonpositive healing, additional-healing cap, single-use cadence, cure None/either condition/protected or suppressed sources/independent components and no recursive trigger. Any injected condition or detached extra-trigger setup must be labelled mechanical TEST_ONLY control, not the connected earning or Radiance witness.

Retain authentic wire95–106 saves, round-trip and actual remaining-command continuation to expected canonical bytes, incompatible profile rejection and old public projection shape. Require C#9 warnings-as-errors headless and standalone compilation, all static package checks and the exact full 1,509 accepted predecessor inventory plus new cases. Keep immutable execution identities, journals, source/binary hashes and actual connected outputs. Commit exact changed files and obtain actual final GPT review and Codex agreement before the successor.

## Review decisions and completion boundary

Complete-contract review must approve/correct the earned transaction, all mandatory grants including real Detect Magic, the capacity/unavailable-current distinction, Radiance choice/cure/cadence/atomicity, and the approved post-advancement context with both connected acceptance streams. There is no implementation approval until that review actually arrives and blockers are resolved.

This is one earned source-bound Cleric advancement toward the reusable C# simulation. Other class levels/builds, retraining, multiclassing, ordinary casting/preparation, RP/Conviction recovery, other card effects and Resurrection remain unsupported rather than invented. Whole-engine completion still requires the approved map and documented gameplay requirements; a contract, fixture, schema or passing suite is evidence, not that completion.
