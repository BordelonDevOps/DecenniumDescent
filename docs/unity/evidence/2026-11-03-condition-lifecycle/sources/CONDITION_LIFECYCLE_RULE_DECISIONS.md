# Generic condition lifecycle completion policies

Status: **ADOPTED PROVISIONAL CONSENSUS POLICY**, local 2026-11-03, under the owner's delegation to Codex and Unity Rules Engine Development. This is neither recovered source wording nor release promotion. The delegation is recorded in [the owner receipt](MOVEMENT_AND_UNARMED_RULE_DECISIONS.md#owner-receipt).

The source baseline is `CONDITIONS_PLAYTEST.md` shared handling and the relevant named entries, supplemented by `CUSTOM_CONDITION_BINDINGS.md`'s cure-presence-suppression supersession. Exact source bytes and tests are bound in [the lifecycle evidence](evidence/2026-11-03-condition-lifecycle/SOURCE_BINDINGS.json). GPT dispositions `c0c25deb-9762-54aa-8f80-c2722ee497c9` and `f8481dae-24cd-5239-bef9-82e62b2731e9` are preserved in [the guidance receipt](evidence/2026-11-03-condition-lifecycle/GPT_GUIDANCE.json).

## Three new provisional completions

1. **An inherited component prevented at initial admission remains absent for that application.** If Stunned, Paralyzed, Petrified or Unconscious is lawfully applied while the target is immune specifically to Incapacitated, admit the parent's other clauses and record that its inherited Incapacitated component was prevented. Losing immunity does not create that missing component. A genuinely new application checks immunity again. This differs from an admitted component subsequently suppressed by acquired immunity, which can resume while still present and unexpired.

2. **A generic eligible cure of Incapacitated removes the named component without removing its parent.** Remove eligible independent Incapacitated records and permanently end eligible inherited Incapacitated components, including suppressed components. Retain the parent's other effects and original endpoint. Record component removal separately from admission prevention. Parent and inherited-component cure eligibility may differ when a specific source supplies an exception. An explicitly narrower remover retains its exact scope.

3. **Each lawful new Unconscious application resolves its own onset once.** Issue its drop-held-items and fall-Prone consequences once even if another independent Unconscious cause already exists. Actual item restrictions and named component immunity still apply; already-Prone stays Prone and empty hands lose nothing. Duplicate command replay, loading, ending suppression and ordinary refresh are not new applications and must not repeat onset. A prevented fall is settled, not deferred until immunity ends.

## Source interpretations and boundaries

Parent immunity suppresses its ongoing clauses, including inherited components. Immunity to an inherited component affects only that component. Neither reverses completed world changes. Prone caused by Unconscious has its own endpoint: legal standing or explicit removal. Ending Unconscious does not stand the creature or retrieve equipment; clearing Prone does not end Unconscious or replay its old fall.

When previously admitted Incapacitated becomes effective after suppression, incompatible current concentration must end. This enforces the current state and does not replay the old drop/fall onset. Removing Incapacitated later does not restore ended concentration. Exact fractional time and within-instant phases remain distinct; advancing over an interval must retain intermediate concentration-loss events even if the condition also expires before the final time.

An operative Petrified application supplies named Poisoned prevention/suppression, with the grant's provenance attached to that Petrified application. Suppressing its Incapacitated component does not remove poison protection; suppressing or ending Petrified does. Other immunity grants remain independent. Existing Poisoned can resume if still present and unexpired; a prevented new Poisoned application does not become dormant history. This does not implement general poison or disease payloads.

Cure eligibility tests present, unexpired records, including suppressed ones. Specific cure prerequisites and source exceptions remain mandatory. Damage immunity is distinct from condition immunity. Same-name nonnumeric penalties apply once while independent application records retain their sources and endings. No default duration, application DC, refresh, action cost or save is inferred.

## Current C# scope

The immutable helper admits 14 generic non-track identities and feeds resolved components into the existing condition calculations. Relationship conditions, periodic Bleed/fire families, numeric tracks, Staggered's episode/rider, source hard-denial caps and actual spell/feature eligibility remain separate. A host must atomically commit returned state and consequences after authorizing the actual command; this helper supplies neither that authority nor duplicate-command handling.

The helper does not mutate HP, death state, held equipment or actual concentration. Its life-permission bridge preserves the existing zero-HP/death restrictions even under external named immunity. It adds no snapshot schema, persistence codec, combat command or Unity integration. Those are the next integration dependency, not completed by pure lifecycle tests.
