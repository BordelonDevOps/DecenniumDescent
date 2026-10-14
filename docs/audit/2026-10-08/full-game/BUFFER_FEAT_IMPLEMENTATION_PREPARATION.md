# Eight-feat implementation preparation

**Not an implementation or adopted rule.** The15 grouped boundary questions have been visibly submitted as `CODEX_BUFFER_FEAT_BOUNDARY_CONFERENCE.md`. Read the actual completed reply before choosing unresolved quantities, caps or timing. All335 original feat entries remain unchanged.

## Existing adapters to reuse

- `tools/form_temphp_playtest_rules.py`: `BufferLedger`, `BufferGrant`, `blood_ritual_offers`, and the reviewed two-stage `necrotic_affinity`/`finish_necrotic_affinity`. Use one world ledger and recipient long-rest epochs. Offer comparison happens after legal source cost; equal retains old. Never make another independent scalar temporary-HP pool.
- `tools/device_lifecycle_playtest_rules.py`: canonical `Wallet` and owner-wide `CommandLedger`. Empowered Summoning modifies an eligible summon; it does not grant a new command or offensive budget.
- `tools/core_playtest_rules.py`: authoritative `LifeState`, `stabilize`, saving throws and actual damage state. Field Medic uses an actual dying→Stable transition, not a new pseudo-healing operation; kit use/inventory is still a real paid resource.
- `tools/healing_playtest_rules.py`: `healing_packet` for exact two-pass ordinary healing; `HealingReduction` with exact `Fraction(1,2)` and a shared group key for any approved Agony next-heal rider; `HealingCommitLedger` for one-shot consumption/idempotency. The packet's `nextHealingCandidates` includes all operative applicable next-positive reducers, including those whose arithmetic branch loses or whose eventual heal is blocked/capped.
- The existing healing packet's optional `reserve` caps actualHP gained, but `genuineExcess` is independently calculated. Do not assume that merely passing a reserve prevents excess-conversion farming. Implement the actual Lifeleech budget/excess decision explicitly after the reply.
- `HealingChain` carries source/root/visited guards and propagated blocker flags. `ExcessLedger` allocates each permitted point once. A computed number grants no conversion permission.
- Existing `RecipientLedger` in the pulse helper is round-based; Chef/Inspiring Leader need actual recipient completed-LR epochs instead. Do not accidentally substitute caster rests or encounter IDs.
- Immutable body/origin semantics from `transformation_spell_playtest_rules.py` are mandatory for soul eligibility, actual healing targeting and Necrotic Affinity seals. Do not treat a new form ID as a new physical soul/body.

## Required regression categories

1. Every exact prerequisite and actual legal acquisition opportunity; no duplicate feat/resource grant and no unstated retraining.
2. Chef batch creation only at the agreed rest/cooking transaction; real ingredient consumption; expiry/rest ties; servings used once; recipient-family cap across multiple chefs; rejected shields; no crafted-recipe powers from mundane food.
3. Speech uninterrupted duration, language/hearing/range, owner versus individual recipient interruptions, self exclusion, recipient rest family cap, exact stat snapshot and strongest-only shield.
4. Summon creation slot/body lineage and root identity: real new paid roots, same-root recreation, several distinct summons, per-creature first rolled damage, shared area roll once, no fixed-damage bonus, no new command budget.
5. Field Medic kit BA versus Medicine/spell transitions; real kit stock; already-Stable rejection; actual new dying episodes; independent subsequent1HP recovery; no corpse healing or Wound removal.
6. Blood Ritual use commits once, interruption remains spent, other-ally selection and presence, self/ally different lifetime, amount independent of arbitration, independent next-curse/disease save advantage.
7. Necrotic Affinity: existing post-resistance Reaction pipeline unchanged; once-actual-turn melee die including off-turn/natural attacks; broad printed qualifying necrotic-kill scope; final actual death/provenance/mixed-type attribution; exact24-hour rank-bound seal and no fake rank for class resurrection.
8. Lifeleech: actual necrotic damage/overkill/THP distinction, predetermined area target, per-root/canonical-round cap, out-of-combat timing, finite recovery, zero/capped/blocked HP, exact excess and causal-child permissions, no natural-attack/Agony-as-spell confusion.
9. Shared Soul Charge pool0..3, one owner entitlement per actual death, body/rest history, no corpse re-scan or replay, multiple owners, full-capacity/declined-capture rules, origin/soul eligibility, black-crystal loss/replacement/transfer without charge duplication.
10. Soul Cage shield cost before arbitration; Agony costs before saves/defenses; half damage separately from healing rider; same-family reducer stacking/expiry/consumption, dispel permissions and no ordinary heal reduction on resurrection/stabilization/THP.

The eight feats require actual implementation plus independent GPT review before promotion. Full economy, soul taxonomy, class prestige/ordinary Soul Cage spell, broader acquisition/retraining and the remaining327 feat entries remain separate coverage obligations.
