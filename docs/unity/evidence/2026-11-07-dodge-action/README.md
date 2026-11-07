# Schema56 Dodge Action evidence

This packet records the source-bound, TEST_ONLY addition of Dodge to the shared combat simulation. It does not claim the complete engine or general release content is finished.

## Source and implementation

The pinned rule is the Dodge row in `COMBAT_ACTION_PLAYTEST.md` at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Its checked-in snapshot and SHA-256 are referenced by [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The source says Dodge lasts until the actor's next regular start, grants disadvantage to attacks from attackers the actor can see, grants advantage on DEX saves, and fails while the actor is Incapacitated or has Speed 0. Runtime eligibility checks those conditions dynamically until the fixed expiry.

Schema56 appends `DodgeRecord` history and preserves older codec layouts. The opt-in shared profile routes the Action through its existing turn ledger; it reuses the existing actor-life, condition, effective-speed, visibility, turn-schedule, attack/save and deterministic RNG authorities. No separate clock or random source was added.

## Runnable acceptance

- `dodge_uses_shared_action_persists_disadvantages_visible_attack_and_expires_at_next_start` covers query purity and Action cost, shared Action payment, conflicting Action rejection, save/restore, a visible attack's disadvantage and exact next-start expiry.
- `hunting_trap_pending_overwatch_push_is_gated_before_save_and_then_resolves` covers the integrated Overwatch attack and hunting-trap DEX-save consumers while Dodge is active.

## Validation

- C# 9 warnings-as-errors regression suite: **PASS, 1,205/1,205**. See [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json).
- Static package validation: **PASS, 18/18 checks, 253 assets and 253 unique GUIDs**. This checks package structure and dependencies only. See [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json).
- `git diff --check`: rerun after this packet was added; its result is recorded in `SOURCE_BINDINGS.json`.
- [GPT's excerpt review](GPT_REVIEW.md) found no confirmed blocker. GPT did not inspect the checkout or run validation. The review's conditional concern about failed Action payment was checked against the shared candidate-copy/validate/commit transaction; the optional follow-ups are condition suppression/recovery across save/restore and unseen-attacker/advantage-cancellation coverage.

## Limits

This is an explicitly opted-in TEST_ONLY profile. Dodge is wired to current club/unarmed, repeating-crossbow and Overwatch attacks, and current suppression-fire and hunting-trap Dexterity saves. Other attack or DEX-save implementations are not claimed to consume the effect. Runtime presentation and gameplay validation were not run.
