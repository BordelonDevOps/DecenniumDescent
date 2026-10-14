# Completed independent review of the 70-test repairs

ChatGPT said:

The six previously reported findings are repaired correctly in this revision. The new scheduler progression, environment/physical coupling, current external-dependency checks, exact max-HP source table, BufferLedger invariants, and Soul Bind state validation all address the concrete failures from the 52-test version. The 70-test report is consistent with those repairs. 
Pasted text

I still find three reproducible blockers inside the admitted foundational scope. They are not part of the seven deferred integrations.

Scheduler.regular_start() does not prove that the supplied Wallet belongs to the actor whose turn is starting. The cursor/order repair is correct, but the API still takes actor and wallet independently. It validates the actor against initiative[cursor], then clears that actor's Time Loop debt while setting whatever supplied wallet's Reaction to True. 
Pasted text

Reproducer: A and B both have outstanding debts; cursor points to A. Call regular_start('a', wallets['b'], now). It passes. A's debt is cleared, but B's Reaction is refreshed out of turn while A's canonical Wallet remains unchanged.

Minimal repair: the scheduler must not accept an unverified Wallet alias. Prefer a kernel/world wrapper that obtains self.wallets[actor] internally and then advances the scheduler, or otherwise provide an authoritative registry and require wallet is canonical_wallets[actor]. Add a regression specifically passing B's real Wallet while starting A's turn.

TemporalHealingCommitLedger.records still admits an unsupported one-shot if the live registry is malformed directly. register() correctly restricts new records to feat:soul_cage:agony, but _validate_holders() validates the ledger's field names without validating each existing record. 
Pasted text
 
Pasted text

Reproducer:

Plain text
healing.records["x"] =
    OneShot("x", "future:unreviewed-source", "a", "b",
            True, ClockMarker(60))

With a participant owner/target, capture can serialize it and kernel_plan() can later restore it because the restoration path checks owner/target and deadline but not source_id. That contradicts the kernel's stated rule that unsupported active state blocks rather than silently opting in.

Minimal repair: at both capture/preflight, validate every current one-shot:

dictionary key == effect_id;
exact supported source ID;
expected clock policy (Agony requires an absolute expiry and no rest-epoch substitute);
owner/target are canonical scene identities;
availability/history shape is internally valid.

This validation should not wait for the later FeatWorld synchronization adapter. Creation/refresh/removal synchronization can remain deferred; admission correctness belongs to the already-implemented one-shot adapter.

An external dependency can still be associated with a different external effect identity. The new dependency reconciliation is much better, but the external-effects dictionary key is never required to equal ExternalEffect.identity. For a new dependency, lookup is performed by dep.effect_id, while the later check only requires effect.identity == effect.record.application_id. 
Pasted text

Concrete reproducer:

Plain text
dependency.effect_id = "dep-A"

external.effects["dep-A"] =
    ExternalEffect(
        identity="effect-B",
        owner="outside",
        target="b",
        kind="maximum-hp",
        record=MaxHpRecord(
            application_id="effect-B",
            ...
        )
    )

The lookup succeeds under "dep-A", owner/target/kind are valid, and "effect-B" == record.application_id, so the plan accepts a dependency whose claimed effect ID is not the effect actually being overlaid.

Minimal repair: require for every external effects entry:

Plain text
dictionaryKey == effect.identity
              == effect.record.application_id

and, when satisfying an ExternalDependency, require:

Plain text
dep.effect_id == effect.identity

Add tests for both a mismatched dictionary key and a dependency pointing to a differently identified-but-otherwise-valid max-HP record.

Everything else I checked in the six-repair area now behaves as intended. In particular, environment roots and geometry restore/retire together, outsider support/reachability is preflighted, exact max-HP source policies replace prefix guessing, malformed active shields are rejected, and pending/bound Soul Bind states are checked against actual life/death identity. 
Pasted text
 
Pasted text
 The new regressions directly cover those repairs. 
Pasted text

So the current disposition is:

FOUNDATIONAL TIME LOOP KERNEL — original six findings repaired; three narrow admitted-scope blockers remain. Do not close the bounded kernel yet.

playable_plan() correctly remains disabled, the seven transformation/Druid/creature/device/remaining-lifecycle/FeatWorld/control-pulse integrations remain open, and this does not advance the final whole-game review or GitHub-push gate. 
Pasted text
