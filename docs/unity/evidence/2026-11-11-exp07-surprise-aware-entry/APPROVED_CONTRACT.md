Review reply: e5fe03c7-546d-43c1-babf-66c42a005584

## EXP-07 surprise-aware entry — source/API contract approved

**Approve one opt-in schema90 TEST_ONLY genuine encounter entry with the hero’s surprise determined by the proposed explicit Director binding, plus the independently warned control. No additional EXP-04 subsystem is required for this selected scope.**

**Reviewed packet:** `7045915f3c6a7c2e4943304f8fa7d74aacbcd316`
**Governing source:** `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`

The repository comparison confirms no package-source changes after accepted schema89. The requirements below settle the implementation contract; **no further preliminary source/API ruling is needed**.

### 1. Awareness authority is sufficient

The pinned source packet contains V6 paragraphs **8078** and **8086**: the Director determines who is caught unaware, and surprise can apply to one participant independently. The packet’s recorded book hash matches the book binding supplied here. A Stealth-versus-passive-Perception comparison is a possible determination method, not an obligatory additional roll for every authored scenario.

**Approve the following bounded integration:** fingerprint the Director authority, exact encounter, hero, actual defender, precontact awareness basis and selected decision before initialization. In the surprise profile, the hero first recognizes this defender’s threat at entry; in the warned profile, an explicit advance-warning fact establishes the contrary.

Apply the decision **once at the successful genuine entry**, before initiative and the first decision. A declared or partial approach supplies no applied surprise record. Failed entry supplies neither surprise nor additional RNG.

Both actors may see each other at entry. Present visibility does not retrospectively establish advance warning. Conversely, the authored decision must not override contradictory represented warning or prior threat-awareness evidence. Hidden, Invisible, failed sight and empty knowledge collections remain insufficient by themselves.

This authority applies only to the selected first contact with the later defender—not the earlier fight, the whole party, reinforcement admission or schema89 re-engagement.

### 2. First Start, Reaction and first End

Use the existing schedule and ordinary resource authorities. The source explicitly retains passive processing while restricting the first turn, and prohibits Reaction until that turn ends.

| Boundary | Required behavior |
|---|---|
| **Genuine entry** | Surprised hero has **no usable initial Reaction**. Initiative, paid approach and physical state otherwise follow existing rules. |
| **Before first own Start** | No hero Reaction offer or payment may bypass the restriction. Do not manufacture a declined offer or bank a missed opportunity. |
| **First regular Start** | Process normal expiration, resource refresh, recovery and other applicable Start effects. The refreshed Reaction remains unusable while surprise is pending. |
| **First regular turn** | Deny voluntary movement, Action and Bonus Action. Preserve otherwise legal simple interaction, stance selection and passive rules. |
| **Actual first End** | Resolve outgoing consequences and mandatory choices, complete the real slot, then clear the surprise restriction before subsequent decisions. |
| **After End** | The already-refreshed ordinary Reaction may be spent on a **new legal trigger**, subject to independent restrictions. End grants no second resource or extra refresh. |

This matches the existing `ReactionClock`: `RegularStart` refreshes availability while preserving `SurprisePending`; `EndFirstRegularTurn` clears the restriction without replenishing availability. **Reuse that semantic distinction rather than adding another spendable Reaction pool.**

For the measured defender-first control, the genuine hero Start is **`23165/2`, ordinal 1**, and its End completes at **`23171/2`**. Derive these from the actual initiative and turn history; do not hard-code “six seconds after entry” or ordinal 1 universally.

A rejected End, pending response, unrelated actor’s End, extra turn, query or duplicate receipt cannot clear the restriction. Removal of surprise does not remove Stunned, Focused or another independent prohibition.

### 3. Stance, free interaction and shared permission handling

**Approve normal zero-time stance selection during the surprised hero’s first regular turn**, under the existing stance timing rule. Preserve the ordinary requirement to select before End when applicable. Do not select a stance automatically or waive its independent restrictions.

The actual pack-skin drop may remain the first free interaction. The subsequent pickup costs an Action and therefore rejects during the restricted turn, without changing custody, interaction count or expenditure. The current portable handler already distinguishes those costs; the new permission restriction must reach its second-interaction check rather than blocking all handling.

Compose surprise into the shared permission assessment used by queries, execution, movement and Reaction eligibility. The current shared and combat permission projections are separate integration points; updating only one command handler would be insufficient.

Do **not** implement surprise by setting Incapacitated, Unconscious, blindness or base Speed 0. Do not make the existing life/condition `Aware` predicate false merely because the actor was caught unaware at entry. Surprise supplies no attack advantage, automatic critical, concentration loss or immunity to forced movement.

**The Bonus Action projection is sufficient evidence when this profile has no actual granted use.** Do not add a feature merely to produce a test command.

### 4. Minimal state and compatible envelope

**Approve append-only schema90 TEST_ONLY**, selected before initialization with distinct surprised and warned fingerprints. Preserve schema89 and all earlier layouts, fingerprints and behavior.

Persist one bounded awareness decision and its lifecycle provenance: source/Director binding, participant and threat, actual entry receipt, selected outcome, first regular Start identity, and actual first-End completion evidence. Keep the existing interval as the resource authority; derive the restriction from this recorded lifecycle.

No generic “apply surprise” gameplay command is needed. Do not permit a caller to introduce, renew or clear surprise retrospectively. Later retreat, roster changes or re-engagement must not reapply the original entry decision.

Validation and canonical replay must reject altered authority, actor/threat, entry, first-turn or early-End claims. Restoring during the restricted slot must preserve the restriction; restoring after its End must preserve its completion. Do not retag authentic schema89 saves.

### 5. Six implementation acceptance groups

| Group | Required evidence |
|---|---|
| **1. Authored awareness and actual entry** | Real connected approach and partial movement; surprised and warned profiles with the same physical setup and initiative inputs. Reject missing/contradictory authority and unrelated or retrospective surprise. No extra awareness RNG. |
| **2. Initial Reaction and exact lifetime** | The real leave-reach movement offers the aware hero a Reaction but not the surprised hero before its first Start. Denial persists after Start; an actual new post-End opportunity permits payment. Rejected/duplicate End cannot alter the lifetime. |
| **3. First-turn permissions and costs** | Otherwise-legal movement, Club Action and Action-cost second interaction reject unchanged. Free drop and lawful stance work. Bonus Action projection denies without granting a new feature. Normal later voluntary decisions remain available. |
| **4. Passive timing and independent restrictions** | The restricted slot still consumes its actual time. Demonstrate an applicable due effect and concurrent shared work without duplication. Clearing surprise does not clear an independent Reaction prohibition. No skipped turn or fabricated refresh. |
| **5. Persistence and integrity** | Before-entry, entered, first-turn, post-End and continued saves replay identically. Isolate forged authority, entry/actor, first-Start/End and resource claims; retain query purity, command conflicts and once-only lifecycle evidence. |
| **6. Compatibility and exact execution** | Authentic schema89 aware baseline and relevant earlier controls remain unchanged. Retain wrong-profile/Release rejection, exact bindings, focused and completed relevant historical results, standalone compilation and static package validation. |

The aware predecessor already demonstrates the real pre-Start opportunity, paid first-turn attack, free versus Action-cost handling, and post-End opportunity payment. It is a suitable comparator, **not evidence that surprise is already implemented**.

### Supplement and inspection limits

**Accept the schema89 full-run supplement:** the pinned report records **1,436/1,436 passed, zero failures**, on accepted source `344c33f11fbd4c2d3919c2f3f68cb0ec4db072b1`. Its four recorded assembly digests agree with the proposed baseline’s bindings. This does not substitute for schema90 evidence.

I inspected the proposal, bindings, complete baseline verifier, relevant observed results, pinned extracted V6 paragraphs, Combat Action provisions, `ReactionClock`, and the shared/combat permission and portable-interaction paths.

**I did not execute C#, run the verifier, load binaries or saves, recompute hashes, freshly extract the DOCX, change repository files or run Unity.** The source determination uses the pinned extracted packet, not a claimed fresh XML extraction.

**Final disposition: approved for bounded implementation.** The required work is the entry-bound awareness record, shared permission integration and exact first-End lifecycle—not a new stealth/hearing subsystem. Implementation and the six evidence groups are the next gate; earlier acceptances stand, and Unity gameplay integration remains deferred.
