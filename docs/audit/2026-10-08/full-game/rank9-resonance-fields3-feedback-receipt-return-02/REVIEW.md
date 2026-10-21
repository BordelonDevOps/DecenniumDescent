# Resonance Fields3 — bounded Arcane Feedback receipt follow-through

## Disposition

**Confirmed missing explicit durable Feedback use/settlement, corrected as a proposed state representation.** No field procedure, shared rule, source access, class card or selected question is changed. This is not independent local acceptance, canonical application or game-runtime validation. Applied525/323/249/173 and50 accepted-but-unapplied remain unchanged; these three fields remain independently unaccepted.

The source card is `wizard#/cards/60`: after the owner's actual successful Counterspell negates a spell, restore1 RP at most once per round, capped at normal maximum. Companion, reflected and copied Counterspell do not trigger it. Complete source text is retained in `sources/wizard.json`, `SOURCE_EVIDENCE.json` and `SOURCE_EXCERPTS.md`.

## Why the existing records were not sufficient

The original full states provide actual counter cast records, numeric RP and observations, and an `eventsApplied` list. The list can distinguish a repeated whole event ID. Neither it nor the cast records defines a Feedback-specific mapping to the original owner, negated cast and actual numbered round, or gates a different qualifying counter in that same round. No supplied executable derivation completes those missing relationships.

The historical verifier at lines129–143 derives a1RP arithmetic adjustment from the new observations. It does not enforce a spent Feedback use or durable source-settlement rule. Its complete file remains historical; it was inspected as text, not executed. Generic RF9-PERSISTENCE-01 does require durable identities but does not itself implement this class-feature ledger.

Thus this is not a claim that narration is meaningless, nor that a duplicate necessarily executed twice in a game. It is a demonstrable missing authoring-state/derivation boundary. The proposed receipt makes the already-credited use explicit.

## Exact state completion

Only these two existing independent branches change:

- `/currentVectors/4/independentBranches/2` — `RF9-NS-A-counter`.
- `/currentVectors/5/independentBranches/0` — `RF9-NS-B-counterpulse`.

Each complete initial/before/after/final state now supplies the explicit fixture numbered-round context and a private feature namespace at `actors[owner].limitedUses["wizard.supplement.arcane-feedback"]`. Before the award the namespace is empty. After it, `roundUses` points to the full terminal receipt in `sourceSettlements`. The same terminal state is retained in the final mirror.

The durable key is the tuple **scope, actual owner, feature, original counter cast ID**. A delivery/callback ID or current round is deliberately not part of that source-settlement key. The receipt separately binds the original round, original event, actual negated cast, native source, qualification and positive award.

`RF9-NS-A-counter`: native Counter1 spends3 RP and the real Reaction, then recovers1: **64→61→62**. Its source-correct recharge2 and all Dissonance/matrix/other histories remain exact. `RF9-NS-B-counterpulse`: Supreme makes the actual class-counter fee1, then Feedback recovers1: **64→63→64**. Its real zero-priced Counterpulse remains separately spent at `counterpulse-round1`; no second spell/counter transaction is introduced.

No existing actor quantity, Action/Reaction, root, source cost, condition, RNG, geometry or observation changes. Removing just the added receipt/context fields from either branch recovers its complete original data.

## Round and replay rules

The complete combat source explicitly separates numbered rounds and ordinary Reaction refresh: a late-initiative creature can react before its first regular turn and refresh Reaction at that real START within the SAME numbered round. Extra turns do not refresh Reaction; the numbered-round boundary does not refresh it either.

Both affected awards occur in explicitly supplied fixture round1, marker0 through the next boundary6. These are fixture bindings, not `floor(time/6)` runtime derivations or a new global cadence rule. E's actual START2 and B's START1 do not reset Feedback's round1 history.

A committed positive recovery publishes its round claim, source receipt and RP atomically. A known source replay is read-only even under a renamed callback, JSON reload or later round. A distinct qualifying source in an already-spent round receives no second recovery and may retain its own terminal no-award receipt. A later NEW source in a NEW genuine numbered round can qualify if its actual counter is lawful. No callback grants another Reaction or bypasses recharge/acquisition/components/costs.

Partial publication, conflicting IDs, or missing authoritative outcomes are integration errors—not invitations to recover the point again. Storage transactions and crash recovery remain unimplemented requirements.

The correction selects the positive awards and spent-round denials. Prohibited/cap-zero diagnostics are nonaward projections only: they preserve existing prohibitions and cap without selecting an unrelated convention for whether an unused class frequency is consumed by an unawarded trigger. Previously spent receipts are never erased/refunded.

## Independent numerical/state diagnostics

The new standard-library diagnostic runs **31 cases / 64 assertions**, with zero failures. Full inputs, before/after states, expected values, source qualifications and outcomes are in `FEEDBACK_DIAGNOSTICS.json`.

It verifies the two positive payment/recovery projections, original omissions, duplicate/renamed callback, reload, old-source replay after a round boundary, own-START Reaction versus round-use distinction, a distinct same-round counter, retained no-award receipt, new-round distinct eligibility, actual native qualification exclusions, prohibited recovery, maximum cap and incomplete/conflicting receipt rejection.

The conditional same-round comparison uses the actual ordinary rank3/5RP Counterspell source, not the class card while its recharge is1. The complete W17-Conj book already includes it, but its main fixture does not prepare it; the independent diagnostic explicitly requires actual prior preparation and a lawful native cast. Sixteen prepared matrices fit its actual limit23, but no in-encounter preparation or acquisition is granted. Its real E START2 can supply ordinary Reaction refresh; it is not invented by the award rule. A genuinely paid/qualified second event gives **62→57→57**, not58.

At the next numbered round boundary6, Reaction does not refresh. A real E regular START8 can make the class recharge1→0 and refresh Reaction. A separately supplied actual successful native class counter at9.2 pays3 and recovers1: **57→54→55**. These are expressly conditional native-transaction inputs to the reward projection, not proof of action reachability, complete native cadence execution or an opponent's unprovided cast. Both old round/source receipts remain.

The positive core states retain the complete existing case facts. The additional tests execute neither project code nor a game scheduler. JSON roundtrip tests are not production save/load validation.

## Full mirrors, sources and history

`MODEL/currentVectors` equals the complete `CASE_DISPOSITIONS/cases` array. The Director's full casebook JSON is replaced exactly; its existing complete procedures, questions and holds remain intact. `FEEDBACK_RECEIPT_CONTRACT.json` equals the new model's complete receipt-completion record. Both full affected branches and every original value appear in `AFFECTED_CASES.json`.

The three procedures, six shared clauses,24 selected answers, templates/feature accounting, source/native access records, all other cases and all holds are unchanged. Main case/branch counts remain7/28; four original conditional branches remain. The five independent whole-positive holds IN6-09-A, IN6-09-B, EN5-01-A, EN5-01-B and EN6-03-B are not cleared. No parent335 acceptance occurs.

The exact54,459,580-byte Return01 ZIP and the complete current937,873-byte packet are included unchanged. Their own full source/context archives and earlier reports remain complete historical evidence. Original source aliases resolve through the routing map into Return01's nested input archives; no absent loose path is claimed. No historical report is relabelled as a new execution.

## Complete reconstruction

From exact Return01 MODEL: **6 operations**—three successor metadata replacements, two full branch replacements, and one added receipt contract. From the original candidate: **27 operations in two explicitly ordered stages**—the preserved21 original operations inside the historical container, then these6. These are alternatives; do not apply both paths to one state.

All before/after values are complete bound archive/member/pointer references, with canonical value hashes and complete source/successor file hashes. Reversal restores the exact original bytes and key order. Complete artifact replacement references are supplied separately; they are not additional gameplay patches.

MODEL: **5,129,434 bytes**, SHA256 `5b02270f39fce01c392b6e8187ce9e144f06957d908140c5c18cf96f1e78952a`.

## Implementation and review reservation

No canonical file, registry, index, class source, production helper, field rule or runtime flag is modified. No game/project module or supplied historical script is run. Source preservation/reconstruction, isolated receipt diagnostics, actual implementation, human gameplay, balance, cosmology,75-domain closure and release remain distinct. The owner's implementation reservation remains. Independent exact acceptance of these three proposed fields remains pending.
