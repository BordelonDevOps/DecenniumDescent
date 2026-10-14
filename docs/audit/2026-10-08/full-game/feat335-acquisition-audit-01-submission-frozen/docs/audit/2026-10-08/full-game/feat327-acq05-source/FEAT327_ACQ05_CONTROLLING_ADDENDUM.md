# FEAT327-ACQ-05 — Animal Companion purchase, attempt and transfer

**Controlling narrow source-authoring addendum. No exact feat-candidate or runtime approval.**

## Decision

Keep the original Animal Handling prerequisite, the printed feat identity, FS-01 nonrepeatability/earned opportunities, FS-06 finite initial allowance and beneficial-rest rules, FS-10/EX58 control budgets, the three SUP-02 bodies, and the complete Companion Training/Ranger procedures. Adopt the explicitly NEW purchase-versus-bond and start/interruption boundaries below. Correct “new paid acquisition” so it never requires a second purchase of the same nonrepeatable feat.

A lawful feat purchase establishes permanent ownership immediately and independently of animal availability. A valid bond attempt consumes its allowance at its start. An interrupted attempt does not resume or refund. An owner cannot attempt a second feat bond while retaining the first: actual release/death and a beneficial owner Long-Rest completion ordered afterward precede replacement. Receiving owners use their own actual engine and costs, not the sender’s grant or rest history.

The original source does not specify the spend event or separate the first purchase from first bond sufficiently; these are NEW finite authoring choices, not alleged verbatim original rules. The retained source already supplies a separate one-hour release, a post-release/death rest requirement, no invented animal and one bond at a time. Allowing the same previously released living individual to be a later eligible target is an explicitly NEW rebond interpretation, not a second body.

## Inspection and source authority

The actual ZIP is 1,349,269 bytes, SHA-256 `c629c3014ea78ce69aca4f30e9dbdba2ba37d297a8e97cac5b33b52848d8082e`. Its root is `PACKAGE_MANIFEST.json`, not a guessed FILE_MANIFEST name. All21 listed payload hashes and byte sizes match. Executed96 read-only source, exact-patch, preservation/parity and reference-arithmetic checks pass. Inputs remain untouched; patch rehearsal is in-memory only.

Inspection covered the complete Animal Companion and Companion Training objects/procedures and acquisition contracts, the complete relevant FS-01/06/10 rules and SUP-02 templates, Ranger’s engine/native Beast Companion source, the relevant EX58 rest/control sections, source-audit history, and the local companion model/report limits. This is not inspection or acceptance of every unrelated feat procedure in the full envelopes. The110 local model checks were NOT rerun; their wider imported prerequisite suite is not fully present in this narrow ZIP. The20 acceptance groups below are authored expectations, not executed lifecycle/gameplay tests or authenticated campaign events.

### Exact source anchors

All bindings, complete clauses and original hashes are in [ACQ05_BOUND_SOURCES.md](ACQ05_BOUND_SOURCES.md) and its JSON counterpart.

| Anchor | Controlling submitted location |
|---|---|
| S1/S8 | Public `candidate.json /feats/10` and `FEAT_EXACT_01_ACQUISITION_CONTRACTS.json /records/10`: Animal Companion; printed Animal Handling gate, complete current procedure and nonrepeatability. |
| S2/S3/S4 | Public `shared_rules.json /rules/0`, `/rules/5`, `/rules/9`: FS-01, FS-06 and FS-10. |
| S5 | Public `supplements.json /groups/1`: SUP-02’s three complete bodies; current ordinaryHP/native anatomy required. |
| S6/S7 | `data/public/class_playtests/ranger.json /engine/7` and `/cards/29`, `ranger.hero.warder.beast-companion`: actual class and receiving-engine restrictions. |
| S9/S10 | Contracts `/records/297`: Companion Training OR gate; foundation `/classes/15`: actual Warrior4/8 opportunities. |
| S11/S12 | `EXPEDITION_PLAYER_BOOK.md` FL-03 lines55–66 and TR-02 lines862–877: one clock, rest/work, genuine control, no automatic taming or additional companion phase. |
| S13/S14/S15 | General-combat audit GC-04, full supplied companion model, report limits: source/proposal history and the existing successful-hour model’s expressly partial scope. |

## Exact operative replacements

Apply the four spans below only within Animal Companion’s current operative text. The exact old strings and replacement strings, identity guards and current locations are packaged in `ACQ05_EXACT_OPERATIONS.json`. Do not globally replace the same words in historical source/proposal copies.


### ACQ05-PURCHASE-ATTEMPT

**Replace this exact old span:**

NEW acquisition: with actual Animal Handling proficiency, select one already real willing/tamed Beast, noncorrupted, INT<7, that fits one of the three finite body templates below. Finding, buying or taming it requires actual campaign access/consent; the feat creates no animal, stocked shop or universal charm. Spend one uninterrupted hour together at touch range; one bond attempt per completedLR, noRP. One feat bond at a time.

**With:**

NEW ACQ-05 purchase/bond distinction: acquire Animal Companion once by committing one actual earned unspent feat opportunity while meeting its actual Animal Handling proficiency prerequisite and all other acquisition gates. Record that paid grant and its acquisition snapshot atomically. The animal and bonding hour are not conditions of purchasing the feat. Ownership begins at that commitment, with no companion and one unspent bond attempt under FS-06; it grants neither an animal nor an earlier completed Long Rest. Animal identity, matching template and any actually sourced sense choice belong to each bond record, not a permanently locked feat-purchase choice. The retained nonrepeatability/permanent-choice metadata does not prohibit the replacements expressly allowed here. Canceling a proposed purchase before commitment spends no opportunity. A completed purchase is not refunded or repeated because no animal is available, a bond attempt fails, or a bond later ends. Animal Companion ownership alone can satisfy Companion Training's printed parent alternative, but supplies neither its separate feat opportunity nor a creature on which to use it.

NEW ACQ-05 bond attempt: an owner of this feat with actual Animal Handling proficiency, no current feat bond, no other pending bond attempt, an unspent attempt and any required post-bond-ending Long Rest may select one already real, positive-HP living, willing/tamed, noncorrupted Beast with INT<7 fitting one of the three finite templates. The selected animal must have no incompatible existing bond, including another Animal Companion or Ranger bond. Finding, buying or taming it still needs actual lawful access and its real willing/tamed relationship to this owner; no animal, stocked shop, consent or charm is supplied. Preserve its actual identity, ordinary profile, current/maximum HP, conditions, injuries, native movement, breathing, custody and required template choices. In one ordered start event, recheck admission, reserve this owner and animal for the work, spend the one attempt, and begin the hour. Merely proposing a target or rejecting it before that event does not spend an attempt; it never reverses a previously completed feat purchase. Starting costs no RP, second feat opportunity or universal fee. An attempt cannot begin while an existing feat bond is retained; such a rejected proposal does not release or alter that bond.

Spend one uninterrupted hour of actual bonding work together at touch range. Keep the same owner and animal, actual access, the required proficiency and animal eligibility throughout the work and at completion; the owner must remain able to perform it. This is active work, not beneficial rest, and grants no extra work Watch, assistant shortcut, handover or overlapping incompatible task. Loss of required touch-range access, willing/tamed eligibility, qualifying body state, or the owner's ability to continue, including incapacitation, or voluntary abandonment terminates the attempt. Elapsed time, real losses and the spent attempt persist; no partial hour, resumed fraction or same-epoch retry is awarded. The prospective animal remains in its actual current ordinary state; no feat profile or command entitlement was installed. After a full lawful hour, atomically complete the one bond and apply the existing template/HP conversion to the animal's latest lawful ordinary state, using the owner's then-current governing statistics. No new bond check or success chance is added. Admission alone or an incomplete hour cannot establish a companion.

The initial allowance is one attempt at feat purchase. Each genuinely completed beneficial owner Long Rest thereafter sets the allowance to one, never adds a stored second attempt. Apply FS-06's actual rest limits and one elapsed clock: no reset from Short Rest, debt-only Rest, a repeated rest receipt, a scene, a new target, a new controller, a new day label or level growth. Do not credit active bonding or release work as rest. An invalid claimed completion record is evidence rejection, not an attempt or feat-payment refund: reconcile the real start/interruption/rest history. Missing history cannot be replaced by an assumed unspent allowance. One feat bond at a time.


### ACQ05-REPLACEMENT

**Replace this exact old span:**

Death/release never creates replacement: after a new completedLR, a new real animal and full hour are required.

**With:**

NEW ACQ-05 replacement boundary: when an established feat bond ends through release or death, record that actual ending event. Before this owner begins any later feat bond, require a genuinely beneficial owner Long Rest whose completion is ordered after that event, as well as an available attempt, a real eligible living target and the full new hour. A rest completed before the ending event or an unused prior allowance cannot satisfy that replacement gate. A qualifying completion after the event is sufficient; no additional rule requires the whole rest to have started after it. Existing active-work/rest restrictions still apply. Replacement is a use of the already-owned nonrepeatable feat, not a second purchase. NEW explicit rebond interpretation: a previously released living animal may be selected again if it genuinely qualifies; it is a new bond to the same physical individual, not a new or refreshed animal. A dead animal never becomes eligible merely through rest, release, purchase or this procedure.


### ACQ05-RELEASE

**Replace this exact old span:**

Voluntary release takes one uninterrupted hour and ends the bond without healing; preserve the same physical animal and restore its prior ordinary profile with the same current-HP fraction, not a fresh full animal.

**With:**

Voluntary release requires the owner's one uninterrupted hour of actual release work. NEW ACQ-05 release boundary: record its start, but end the bond only on lawful completion; interruption or abandonment grants no partial-hour credit and leaves the existing bond intact unless an independent event already ended it. A fresh release hour may be begun while the bond still exists. Release consumes no bond attempt, feat opportunity or RP. It does not require a second target or borrow the bonding hour's touch-range requirement; actual owner capacity and uninterrupted work remain mandatory. At completion restore the same living animal's saved ordinary profile with the existing positive-current-HP ratio conversion, preserving its current conditions, injuries and actual custody without healing or refilling it. End the outgoing bond's control entitlement and unexecuted commands; preserve all already-spent body/actor allowances. No automatic transfer of custody or command occurs. Record this end for the post-ending Long-Rest gate.


### ACQ05-TRANSFER

**Replace this exact old span:**

A creature cannot have this and a Ranger bond simultaneously; transferring requires actual release and new paid acquisition, not additive statistics.

**With:**

A creature cannot simultaneously have this and a Ranger bond, or two owners' Animal Companion bonds. NEW ACQ-05 correction of 'new paid acquisition': a transfer requires the outgoing bond to end through its actual lawful release/death/termination procedure, real lawful access/custody for the receiver, and the receiver's independently authorized new bond. An existing Animal Companion feat owner does not buy that nonrepeatable feat again; they spend their own available attempt and full hour and satisfy their own post-ending Long-Rest gate, if any. The sender's rest, feat ownership or spent attempt neither transfers nor resets the receiver's history. A receiver without this feat must first acquire it through their own actual eligible unspent opportunity, or use an independently acquired receiving engine; receiving the animal grants no feat or class feature. An actual Ranger Beast Companion route retains its own acquired Warder/class-level/selection gates, eligible-beast limits, 4 RP, one-hour touch procedure, once-per-beneficial-owner-Long-Rest allowance and native profile/lifecycle. This feat's no-RP route, release hour and attempt rules do not waive or redefine that class engine. A Ranger bond cannot be ended by invoking another engine's feat-release permission. No universal transfer payment, new animal, healing, additive chassis, second controller, extra phase or refunded body/resource budget is granted.


## Receiving-engine interpretation

For an existing feat owner, replacement costs their own new full hour and available bond attempt, with the post-ending rest gate where applicable. No second feat purchase or generic currency is charged. A receiver who never owned this feat must meet its prerequisite and pay an independently earned opportunity before using that route. Buying/being given an animal alone grants no specialist chassis. Independently lawful ordinary handling and Companion Training’s existing scope remain available on their own terms, not as an Animal Companion grant.

The supplied Ranger option is `ranger.hero.warder.beast-companion`, `/cards/29`: actual Warder/Ranger16 selection, not automatic possession by anyone called a Ranger; engine7 also retains a willing/tamed noncorrupted Beast with INT<7 and CR no greater than Ranger class level. Its4RP, one-hour touch procedure, once/LR, native companion statistics and continuing injury remain its own. No Animal Companion feat purchase is required for an independently acquired Ranger feature, but no feature is supplied here. An existing incompatible Ranger bond must actually end under its own source; the feat-release hour supplies no Ranger release, refund or new class timing rule. That boundary does not require another general source conference.

## One chronological sequence

The following is an authored conditional fixture, not real campaign history. Supply actual lawful work/rest support and individual animal records in a candidate instantiation.

- Last beneficial LR completion is hour0. A proficient Warrior4 pays the real level4 opportunity at hour1, acquiring the feat with no animal and one attempt.
- At hour2 a real eligible animal and valid start consume attempt1→0. Contact fails at2:20. The attempt terminates; no companion/profile conversion occurs, the purchase remains paid, and another proposal at3 is unavailable.
- A genuine supported eight-hour Rest16→24 completes a new beneficial LR,24 elapsed hours after the prior one. It restores one attempt. A full new bond hour24→25 succeeds. A Small ground animal then at ordinary5/10 becomes4/9, preserving its injuries and identity.
- A lawful LR completion at48 restores one attempt while the bond still exists. A proposal for another companion is rejected without spending it or ending the existing bond.
- A separate release hour49→50 completes. The same animal returns to ordinary4/10 under the retained ratio conversion. Its bond ends. The unused attempt does not remove the requirement for a beneficial LR completion after50.
- With the next actual eligible completion at72, a full new attempt72→73 can establish a replacement without another feat opportunity. If interrupted, no old bond returns and the new attempt remains spent. At a later legitimate Warrior8 opportunity, Companion Training is separately paid; Animal Companion ownership can satisfy the OR gate even during an unbonded interval, but neither ownership nor Companion Training creates an animal.

The sender’s post-release rest gate does not become a compulsory extra rest for a different receiving owner. The receiver uses their own initial/refreshed allowance and own prior-bond-ending history. A receiver currently bonded must resolve their own prior bond and rest requirement first. Continuous touch-range work and current event ordering remain required; neither a scene boundary nor a rejected completion record proves a refund.

## Guarded derived operations

Exactly7 replacements affect5 existing files:

1. Public `data/public/feat_candidates/exact_01/candidate.json`: `/feats/10/operationalRules` and `/feats/10/payloadOperational`.
2. Internal `data/director/feat_candidates/exact_01/candidate.json`: `/records/161/operationalRules` and `/records/161/payloadOperational`.
3. Audit-root `FEAT_EXACT_01_ACQUISITION_CONTRACTS.json`: `/records/10/completeOperativeProcedure`.
4. `docs/feats/exact-candidate-01/GENERAL_COMBAT.md`: Animal Companion current procedure only.
5. `docs/feats/exact-candidate-01/source-audit/GENERAL_COMBAT.md`: GC-04 current candidate procedure plus the explicit controlling-addendum note, as one guarded section replacement.

The first, second, fourth and fifth paths are relative to `DescentReviewChanges/ReviewBible/`; the third is under `docs/audit/2026-10-08/full-game/`. Resolve each JSON location by its verified `animal_companion` ID as well as its supplied pointer. On an unexpected descendant, stop that particular write and reconcile its actual diff. No unrelated whole-candidate resubmission is needed.

Leave sourceObject/originalObject, all prerequisite trees, repeats metadata, sourceDirection (including its prior completeAuthoringProcedure), original335Registry, the audit’s preserved submitted procedure/examples and original source decision unchanged. The new addendum controls the corrected current fields; the old source-direction string is historical and must not overwrite them through an old builder. Record addendum/current descendant bindings append-only, without overwriting old source hashes. No FS-01/FS-06/FS-10, Companion Training, SUP-02, Ranger, EX58, approval/selection flag or unrelated procedure edit is authorized.

### Necessary model/evidence follow-up

Preserve the supplied `CompanionAcquisition.acquire_companion_from_completed_history` model/report as historical evidence. In a new derived model or completed-history adapter, represent paid purchase → valid spent attempt start → completion/interruption as ordered distinct facts. Do not execute payment only after the successful hour, require an animal merely to buy the feat, or infer refunded ownership/allowance from rejected completion evidence. Its existing four HP endpoint values remain compatible. A new replay must bind earlier acquisition and attempt-start evidence before those results can demonstrate the completed lifecycle.

`ACQ05_LIFECYCLE_RECORD_CONTRACT.json` supplies the bounded record content. It is a specification, not software conversion. No actual save is migrated and no fabricated campaign records are admitted.

## Finite acceptance and closure

Apply the seven guarded replacements, preserve the historical bytes, verify full current public/internal/contract/manuscript equality, and account for each of the20 named groups in `ACQ05_ACCEPTANCE_EXPECTATIONS.json`. That file distinguishes every authored expectation from the executed checks. A local new model may execute them later; report its actual coverage rather than upgrading the authored labels to runtime evidence.

These purchase/attempt/transfer source questions are settled. Their finite fulfillment can be recorded without another generic conference. The subsequent complete exact-candidate review still assesses the actual assembled feat procedures. No335-acquisition, pending feat/class, runtime, human balance or final whole-game approval is granted. ACQ-03/04 and the completed crafting/language/teaching/EX58 scopes remain carried forward.

The CRPG direction, unchanged twelve-character expedition, parallel activities and host-permission design remain controlling. No manual tabletop-bookkeeping completion gate or additional owner confirmation is introduced. Delivery remains actual final joint whole-game flow agreement → already-authorized commit/push → verified remote commit → careful cosmology review and preservation-based cleanup in their agreed phases. No deletion, push or cosmology work occurs here.
