# Unity Rules Engine Development consultation

**Date:** 2026-11-04
**Topic:** Applying DC when the registered Overwatch Bleed profile refreshes.

The consultation asked whether a same-owner/source reapplication before the scheduled tick replaces the active record's applying DC when the Soldier's class DC has changed.

GPT recommended preserving the original record's applying DC, identity and arbitration order. It reasoned that the pinned `custom_condition_bindings.json` `/definitions/38` specifies refresh without added dice and Medicine against the recorded applying DC, but does not explicitly authorize replacing that DC during refresh. The reapplication's current DC remains in the refresh audit event. Medicine does not dynamically recalculate it. Once the old record ends, a new lawful application gets a new identity and captures the then-current DC.

Codex agrees. This interpretation is recorded as a **new provisional consensus completion**, not recovered source text, in [`OVERWATCH_RULE_DECISIONS.md`](../../OVERWATCH_RULE_DECISIONS.md). No owner escalation was needed under the standing delegation.

## Cross-target applications, Medicine degrees, and ordinary removal

**Date:** 2026-11-04
**Topic:** Scope and audit corrections found during independent schema23 review.

### Same owner/source on different targets

GPT recommends that applications to different targets are independent. The source-backed constraint is that `custom_condition_bindings.json` `/familyRules/2` performs arbitration within one family at one target's timing marker, while the shared arbitration text states that different target markers resolve separately. The `/definitions/38` group cap therefore applies inside that target-marker arbitration; its owner-only group string is not a global one-victim slot. A same-owner/source event against B while A is still present creates a B-specific record, with its current applying DC, identity/order and next target marker, and leaves A unchanged. Same-target refresh still preserves A's existing DC, identity and order under the provisional refresh completion above. Each target's occurrence still needs its own lawful originating event.

This is a **source-backed scope interpretation**, not a new multi-target feature grant. The code already partitioned refresh by target; schema23 now records a regression case proving A and B remain independent. Source reference implementation path cited by GPT: `DescentReviewChanges/ReviewBible/tools/custom_condition_rules.py`, `arbitrate_periodic_applications` lines 91–114; mixed-target inputs are rejected before grouping.

### Medicine task degree and audit

GPT confirmed that the existing raw `total >= ApplyingDc` comparison was a source-conformance defect. `CONDITIONS_PLAYTEST.md`, Bleeding, requires WIS Medicine and says Success or Critical Success ends Bleed. `CORE_RESOLUTION_PLAYTEST.md`, Rolls, applies natural 20/1 degree adjustment after determining the total. Medicine now uses the shared `PlaytestRolls.TaskCheck`; its event retains natural result, modifier, DC, check total, adjusted degree, cure outcome and RNG provenance. Replay recomputes the event instead of trusting a serialized success flag. Tests cover natural 20 upgrading a below-DC check and natural 1 downgrading a raw success.

### Ordinary condition removal

GPT recommends deferring ordinary-remover invocation until an actual remover source is connected. `/definitions/38` `cure.ordinaryConditionRemoval=true` establishes eligibility, while remover prerequisites and exact one/all/owner scope remain tied to the remover. The flag does not grant a generic ability or define its action cost, target choice, acquisition or scope. Schema23 therefore exposes no caller-selected generic removal command. The internal ending operation remains limited to source-qualified Medicine and healing. When connected, ordinary removal must also recognize eligible present suppressed records, under `CUSTOM_CONDITION_BINDINGS.md`, `cure-presence-suppression`.

This is an **implementation boundary**, not a gameplay-rule decision. Schema23 implements the Bleed tick/Medicine/healing subset, not every registered cure path.
