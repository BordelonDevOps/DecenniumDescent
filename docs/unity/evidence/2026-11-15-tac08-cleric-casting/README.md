# TAC-08 ordinary Cleric casting: initial source audit

**Source/API contract preparation is in progress. This is not a submitted contract or implementation approval.** The preceding actual CHR-03 acceptance `d08e491b-080b-5502-b548-ac63821e401a` selects this next gate; Codex agrees. Accepted baseline is `07894d8a0d42de50d9d7e66a1191313389f50820`, with engine source `34229ec6f19c9569dd35fd7b6013b99f37759c85` and final evidence `a59225eb63cf03af376bb4aae3ba7619465589fe`. [Actual acceptance and successor agreement](../2026-11-15-chr03-cleric-settlement/GPT_FINAL_REVIEW.md).

The next contract must bind exact operational spell procedures and their concrete TAC-02/TAC-05/TAC-07 prerequisites. CHR-05 remains downstream of the required TAC-08 capabilities. The Cleric uses its accepted known-caster procedure; no Wizard book or Druid preparation system is inferred. All ordinary casting remains unsupported in the accepted baseline.

## Exact source evidence

[Source bindings](SOURCE_BINDINGS.json) freeze 52 authority, gameplay-source, accepted-review and runtime files. [Spell candidates](SPELL_CANDIDATES.json) preserve the exact operational records, card/procedure hashes, authored-review hashes and Cleric access for all six currently relevant identities. These are evidence copies; the original catalog and registry remain the rule owners. Their reviewed/provisional status is not release authority.

| Owned identity | Cleric rank / base RP | Components | Concentration | Source behavior requiring a real consumer |
|---|---|---|---|---|
| Arcane Ward | 0 / 0 | V/S/F | No | +1 AC through the caster's next regular start; actual strongest-flat stacking and same-name later expiry |
| Guidance | 0 / 0 | V/S | No | Optional pre-roll consumption for one actual ability check; one shared-RNG d4; no attack/save substitution |
| Spare the Dying | 0 / 0 | V/S | No | Actual living, dying, 0-HP target becomes Stable without HP, consciousness, Wound or resource recovery |
| Sanctuary | 1 / 2 | V/S/F | Yes, at most one minute | Per-attacker-turn WIS admission save, legal retarget/forgo behavior and exact offensive break |
| Purify Food and Drink | 1 / 2 | V/S/F | No | A real separated food/drink batch, finite 5-pound OR 1-gallon limit, qualified ordinary contamination removal and preserved quantity/custody |
| Detect Magic | 1 / 2 | V/S/F | Yes, at most ten minutes | Actual eligible aura presence/outline, later paid Action for unprotected broad school/category, total-cover and information limits |

All six source procedures specify Action activation and 30-foot range. Detect Magic ownership still requires the genuine accepted Cleric2 transaction. The table summarizes evidence, not the final admitted casting scope; the full procedures in the bound catalog govern.

## Concrete findings

- The accepted `SpellRepertoireRecords.cs` explicitly reports `CastingSupported => false` and returns `OrdinarySpellcastingUnsupported`. Shared command queries reach that denial. Known ownership is already source-bound and chronological; it supplies no cast effect or focus.
- `ConditionCombatPolicy.CommitCondition` receives the shared `EndConcentration` consequence but expressly has no concentration state to end in the accepted profile. Actual concentration storage, damage saves, incapacity endings, replacement, expiry and historical replay must be designed together before admitting a maintained spell.
- The shared casting procedure requires legal repertoire/components/targets first; then legal cast payment and chronological Dissonance/Refrain at cast beginning, prior to interruption resolution. A failed illegal request remains atomic and unchanged. A legal resisted/negated cast cannot refund payment or restore displaced concentration.
- Class rules supply ordinary Dissonance thresholds, repeated-name Refrain, regular-turn decay and Grounding; idle/weapon turns do not reset Refrain. Cleric's protected vent requires actual expenditure of at least two Conviction on a Rite/Invocation. Current Conviction is unavailable in the accepted profile, so capacity alone cannot trigger it. Existing RP funding must remain finite; source recovery text cannot be treated as already implemented.
- The reviewed equipment guide supplies the missing focus interpretation: Cleric F uses an actual holy symbol; held, visibly worn and shield-borne cases have distinct hand consequences. A focus-only hand may also supply S, whereas a worn/shield-borne focus does not free an S hand. Religious-implements proficiency or kit is not itself a consecrated focus. Physical admission, custody, handling and hand restrictions need an explicit proposal rather than a name-only flag.

## Work still required for the complete contract

Specify the proposed spell scope and every required effect consumer without silently omitting difficult clauses. Audit the accepted physical inventory/hand state, action and turn ownership, observations/geometry, damage/life processing and condition chronology. Establish the actual focus origin, Guidance recipient choice before a check, Sanctuary save/retarget transaction, separated consumable and contamination facts, and source-qualified aura/protected-information facts. Any missing capability or rule must remain explicit until resolved with GPT.

Define shared cast state/history, complete preflight and atomic settlement, strain/cadence and due-event ordering, concentration lifecycle, owner-filtered queries, command receipts and versioned persistence. An unavailable counterspell source cannot become an invented reaction; the admitted interruption scope must be explicit. Keep distinct class and spell grants, real effect provenance and original resource accounting.

Design genuine connected casting witnesses using the current exploration/combat/acquisition/management/advancement state and finite resources. Do not inject HP, RNG, resources or earned history to satisfy a scenario. Retain supported wire95–108 histories, deterministic replay, denial/rollback proofs, all 1,524 accepted predecessor cases, source/compile/static evidence and actual implementation review in the eventual acceptance requirements.

Then write and submit the complete source/API contract for actual GPT review. No runtime implementation may begin before that approval and resolution of concrete blockers.

## Audit limits

[The verifier](support/Verify-SourceAudit.py) checks pinned Git blobs, exact procedure/card/review hashes and the unchanged accepted engine. [Its result](SOURCE_AUDIT.json) is source evidence only. It is a pre-implementation audit, not a runtime regression; do not rerun its unchanged-engine/unsupported-casting assertions after implementing an approved successor.

The local canon-manifest checkout has CRLF line endings while its committed blob uses LF. Both byte lengths and hashes are recorded, and equivalence is checked only for that explicit line-ending difference. No source file is normalized or rewritten.

No compilation, gameplay test, new cast, whole-engine completion or Unity integration is claimed. The full reusable C# simulation remains the active goal.
