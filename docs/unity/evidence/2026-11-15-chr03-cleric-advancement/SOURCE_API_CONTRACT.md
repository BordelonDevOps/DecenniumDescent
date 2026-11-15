# Earned Cleric 1 → 2: source/API contract and dependency findings

Status: **PENDING ACTUAL GPT REVIEW — not implementation-ready.** Baseline is `29eed15d770de93f00217a0d9977c5bb489cfca4`, after actual acceptance of the connected Cleric/shared-RP module. This packet supplies the selected CHR-03 source/API gate; it does not claim an advancement implementation.

## Authority and mapped order

The single canon manifest and promotion hierarchy remain authoritative. Character creation, shared class rules and normalized Cleric entries retain their reviewed/provisional playtest scope at `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. The class guide is a rendered companion to that normalized packet, not a second rules owner. Published source and proposed playtest completions are not silently merged or promoted.

The actual final review `84bd8644-f237-55a4-8d15-c8a18ddda017` selected CHR-03 under CHR-02 and required a genuine earned advancement after RP spending, capacity4/currentRP1, no advancement healing/recovery, and complete source choices. It expressly required identifying mandatory missing level-2 capabilities before approval.

The map keeps CHR-03 ← CHR-02 separate from TAC-07 ← CHR-02/FND-05 and TAC-08 ← TAC-07/TAC-02/TAC-05. CHR-05 retains CHR-03/TAC-02/TAC-05/TAC-08. This audit identifies concrete cross-module capability needs for the selected Cleric route; it does not edit those direct edges or move every CHR-03 path behind TAC-08.

## Required source facts

| Obligation | Exact binding and consequence |
|---|---|
| Earned advancement | `CHARACTER_CREATION_PLAYTEST.md#gain-a-level`; `XP_ADVANCEMENT_CANON.md#official-opening-advancement-t110--floors-1100`. Director-announced Opening milestones grant levels; other milestones must be announced before the Opening begins. Creature CR, kill count, manufacturing XP and an arbitrary client-provided award ID are not the reward law. |
| One chronological level | Advance the existing Cleric class from1 to2; total level2, PB2, unchanged abilities/training/initial source provenance. No second first-class construction, multiclass or Saint entitlement. |
| HP and Hit Dice | `character_foundation.json /classes/1`: d8, fixed later-level base5. Append one base5 level and one new unspent d8; preserve the first die's state. With CON10, base maximum8→13; current HP stays8 in the selected witness. Preserve temporary HP, injuries, Stable/dead/downed state and independent conditions. Maximum changes use the existing shared life/capacity path. |
| RP | Cleric `/rpByClassLevel/0..1` is3→4. Re-derive the existing shared pool and use capacity reconciliation, preserving currentRP1 and original one-time funding3. No new funding event, recovery, RNG draw or invented Long Rest. |
| Automatic level-2 acquisition | Cleric `/engine/8`, `/engine/9`, and card `cleric.base.invocation-attunement`: choose exactly one of Radiance/Judgment/Renewal/Flame/Veil/Echoes, acquire Attunement plus only the selected path bonus. The selected bonus becomes active immediately. It is not either of the two selections. No free later path replacement exists. |
| Scheduled selections | Cleric `/schedule/1`: choose2 distinct additional eligible Base cards, minimumActives0, no ASI/feat. Exclude automatic/path supplements, already owned cards and illegal class-level/path choices. Unused selections cannot be banked. |
| Repertoire | `CHARACTER_CREATION_PLAYTEST.md#gain-a-level` step5 and `CLASS_PLAYTEST_RULES.md#spell-repertoires-and-acquisition`: update legal repertoire. The fallback full-caster procedure grants one ranked spell at each later class level, unless a more specific class rule overrides it. The inspected Cleric engine/guide supplies no replacement known/prepared count. `SPELL_INTEGRATION_RULES.md#select-a-spell` requires an actual operational identity, class-specific placement/rank/access and recorded legal acquisition. Capacity alone supplies no unnamed spell. |
| Resource separation | Existing Divine Favor ownership does not establish current Conviction. The selected source engine grants starting/full Conviction after an actual Long Rest; none occurred in the accepted profile. Advancement cannot invent that history or initialize a fabricated zero/full balance. |

These facts retain the predecessor's narrow admission: its initial Cleric selection and tactical Healing Rite are accepted, while ordinary casting/repertoire, Conviction and recovery remain unsupported. Acceptance of that initial slice does not silently satisfy new mandatory level-2 acquisitions.

## Concrete candidate choices and their obligations

For continuity with the accepted authored level-1 build, the candidate level-2 selections are **Judging Light and Conviction Pool**, the exact next row of the published legal Saint example. That example is a legal selection example, not an automatic Saint/path grant or a requirement that every Cleric take those cards. Their IDs are `cleric.base.judging-light` and `cleric.base.conviction-pool`.

Conviction Pool must raise source-derived Conviction capacity3→5 without filling it. Current Conviction is unsupported in the accepted profile, not zero. A real capacity/ownership representation and an explicit treatment of the uninitialized current resource are therefore needed before this candidate can be called implemented. Judging Light modifies only actual Divine Smite damage against a Cursed/Weakened target; Divine Smite is not selected by this build, so the passive has no trigger yet. Do not invent a Smite grant or hit.

The proposed Invocation choice is **Radiance** (`cleric.base.radiance.radiance`), a meaningful extension of the existing healing path. Once on the Cleric's turn, when its Rite actually restores HP, the player chooses one actually healed living creature; it gains S additional HP and may end either Frightened or Poisoned on itself. At level2 S remains1. The contract must specify the optional beneficiary/cure decision, once-per-turn ledger, actual-healing requirement, condition-component cure semantics, and atomicity with the real healing event. Full-HP use that restores no HP does not qualify. The extra flat healing is not a second Rite and cannot recursively retrigger the passive. Other paths must remain unselected, with no accidental benefits.

Radiance is proposed because it connects to the existing source-bound healing/life/condition machinery. It is not yet implemented, and recording its ID without its mandatory effect would not satisfy this contract. Choosing a different lawful path remains possible only through an explicit reviewed contract; a path must not be selected merely to hide its missing effect.

The earned-spell identity and lawful acquisition are **not selected here**. There is no existing connected repertoire ledger or acquisition operation to hold this mandatory grant. The accepted profile also lacks an executable/accounted initial repertoire. Do not assume empty means zero spells owed, add anonymous capacity, silently discard the level-2 spell, or retroactively create initial known spells. Binding that initial/earned provenance is a concrete TAC-07 prerequisite question.

## Proposed preannounced milestone

Decision A proposes one explicit TEST_ONLY Director-authored milestone at fresh expedition creation, before any campaign command: **complete the connected expedition's two genuine encounters and its actual specimen-to-recipe-4 manufacture, then return from the later encounter with the companion alive**. Bind it to the companion and one fixed milestone ID, source/definition digest, announced revision0 and the actual pre-existing world/encounter/manufacturing identities.

This is a proposed authored campaign objective under the source's permission for previously announced milestones, not a recovered named book reward, a kill-XP formula or an assertion that every such encounter grants a level. It has no production authority. The primary witness already spends RP in the later encounter before normal exit, so actual completion occurs after the paid Healing Rite.

The completion point is the lawful later-encounter closure after the genuine earlier closure and batch settlement, with the companion alive. Returning means returning to ordinary play at the retained physical positions. The declaration supplies no teleport, free trip to a Haven, extra encounter, forced healing use or manufactured resource expenditure.

The trusted host may award only after the actual archived encounter outcomes, consumed specimen/settled batch and living returned companion satisfy that exact declaration. Use the existing host-authority boundary and `CharacterMilestoneRecord`, with new declaration/completion provenance only where needed. Payloads cannot supply their own completion flag, replacement target, prior announcement, reward count or source. Unauthorized, premature, mismatched, repeated and forged awards reject unchanged. The award and the advancement are separate persisted transactions; no automatic class change occurs on encounter exit. Existing Soldier award semantics remain versioned.

## Target API and shared transaction

Once the capability findings below are resolved, propose an opt-in successor profile with its own fingerprint/envelope; preserve authentic wire95–105 saves exactly. Do not decide a new wire number until implementation is approved.

Expose the reviewed immutable announcement at typed startup and read-only owner view. Reuse `AwardCharacterMilestone` with server-derived eligibility, then extend the existing `AdvanceCharacterLevel` request/receipt path with exact Cleric class, fixed-average HP method, two card IDs, one Invocation path and the separately authorized repertoire selection. It must not accept client-supplied level, HP, RP maximum/current, Conviction amount, reward, source revision or funding.

Preflight the actual actor and unconsumed entitlement, supported class/profile, complete choices, source prerequisites, class-level gates, existing work/traversal/tactical/pending-choice restrictions and every mandatory capability before any mutation. An unsupported prerequisite denies the entire request without consuming the milestone. Current host/seat authority precedes idempotency lookup. Preview is side-effect free.

Commit one chronological level, one unspent d8, exact automatic/selected grants, all required source-qualified choices, maximum-HP recalculation, RP reconciliation, supported Conviction-capacity effect, milestone consumption, advancement audit and receipt atomically. Reuse shared character/grant/Hit Die/milestone/life/resource state; no parallel character copy or class-private RP pool. Do not alter clock, RNG, prior funding, spent dice, current HP/RP, stock, wounds, conditions, known-use histories or unsupported resources merely because a level changed.

Strict restore must reconstruct the actual announcement, completion/award, choices, resource history and single advancement through receipts. Forged/unearned/duplicate milestones, wrong grants, second path, fabricated current resources and changed prior source facts reject. Earlier profiles cannot acquire this capability by deserializing new fields.

## Baseline audit

- `SharedCharacterAdvancement.Assess/Resolve` admits Soldier profiles only, awards arbitrary nonempty actor-scoped milestone IDs under trusted host authority, and appends Soldier6-base/d10 records. It is reusable transaction machinery, not an earned Cleric advancement implementation.
- `CharacterMilestoneRecord` has awarded/consumed revisions but no preannouncement or objective-completion source. The new selected objective needs that evidence.
- `ClericRpProfile.Validate` fixes one Cleric level, maximumHP8, maximumRP3 and the initial four grants. `AssessHealingRite` rejects class levels other than1. New versioned validation is required; weakening the old accepted profile is forbidden.
- `ResonancePoolRecord.ReconcileCapacity` already preserves/clamps current RP and initial funding; reuse it.
- The current Snapshot and connected class APIs contain no authoritative known/prepared/spellbook acquisition ledger, Invocation choice/bonus state or current Conviction ledger. Source catalogs/names are not substitutes.
- No connected general class-choice API, Radiance beneficiary/cure transaction or class-level Conviction capacity lifecycle exists. Existing numerical rules, condition/life helpers and grant records are building blocks, not proof those effects run.

## Concrete review decisions

**A — Milestone policy.** Approve or correct the exact preannounced TEST_ONLY declaration and source-bound completion/award boundary above. The existing free-form Soldier award is insufficient as the earned connected witness.

**B — Mandatory capabilities and order.** Do not authorize an advancement that drops its repertoire grant, silently treats Conviction as0, or records an inactive mandatory path bonus. The recommended immediate dependency refinement is to prepare the **TAC-07 source/API contract for lawful Cleric known-spell acquisition**, including initial versus earned entitlement provenance, before implementing this selected CHR-03 route. TAC-07 already follows accepted CHR-02/FND-05 and need not wait for CHR-03. Determine whether the candidate Conviction Pool capacity/unknown-current representation can be source-faithfully supported in CHR-03, or requires a separately reviewed Cleric resource gate. This does not require forcing all CHR-03 behind TAC-08. No TAC-07 or resource implementation has begun.

**C — Complete successor contract.** Confirm Radiance plus the authored two-card candidate, or specify a source-faithful alternative with every mandatory effect accounted for. Identify the required integration contract for Radiance choice/cure cadence and the supported Conviction capacity representation. Keep this runtime gate closed until B and C are concretely resolved and the complete acquisition contract is reviewed. If a scoped obligation is intentionally deferred, name it explicitly and explain why the source permits the selected advancement to complete; do not equate visible unsupported labels with fulfillment.

## Required runtime evidence after approval

The primary public route must preserve the full accepted exploration → first encounter → acquisition → management/research/manufacture → preparation → later encounter loop. Spend one Action/2RP on genuine injury, finish the announced objective, earn and award its milestone once, save, advance the same companion and consume it once, then continue through paid ordinary movement. Show Cleric1→2, level2/PB2, HP8/8→8/13, a second unspent d8, RP1/3→1/4, unchanged initial funding/stock/RNG/clock across advancement, exact grants/Invocation/repertoire facts and no recovery.

Test actual mandatory passive behavior under legal triggering histories, with detached controls identified separately when needed; acquisition records alone do not prove an effect works. Cover illegal/duplicate selections, automatic grant counted as a selection, wrong path/class, unmet prerequisites, already consumed milestone, unearned/mismatched awards, current authority before retry, ID conflict, stale revision, condition/work/tactical gating, source forgery, no healing/recovery, and preservation of spent dice/injuries/life state. Expanded class resources must have real lawful funding/recovery evidence before spending, without inserting a fake Long Rest.

Require uninterrupted console, restored console, receipt replay and independent typed dispatch with every denial/retry state pair, saves around announcement/earning/award/advancement/continuation, strict forgery rejection, authentic wire95–105 round-trip plus actual remaining-receipt continuation and incompatible-profile rejection, C#9 warnings-as-errors compilation, static package checks and all1,506 accepted cases plus new registered controls. Commit exact files and obtain actual final GPT review before another successor.

No runtime checks are claimed for this documentation-only audit. Broader advancement, all class choices, retraining/multiclassing, casting/recovery, Resurrection, production authority and complete-engine acceptance remain open. Unity gameplay integration remains deferred.
