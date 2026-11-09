# Morale Rest contract (schema65, TEST_ONLY)

## Source authority

The behavior comes from pinned candidate rules at ReviewBible revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`:

- `DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md`, blob `7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4`, SHA-256 `32ca16894c29ba2906f8d510ef9781951bc8780e4a91ee84671f250f4de62b5f`.
- `DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md`, blob `466871fc128dc5f06043a874da2b9c1d94ed80a5`, SHA-256 `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`.

The Strain source marks Morale Rest `NEW`. These source rows are reviewed-candidate rules and do not grant production or release authority.

## Directly sourced behavior

- Morale Rest is four consecutive safe hours of voluntarily chosen recreation.
- It cannot use forced substance use, productive work, expedition travel, or simultaneous sleep/Short Rest.
- At most one beneficial Morale Rest applies in any 24 elapsed hours.
- It may remove one eligible Expedition Strain point, never a Wound.
- A distinct Morale Rest and qualifying secure Long Rest may each provide their own point reduction; there is no shared one-point cap.

## Codex/GPT operational completion

GPT reviewed the exact pinned passages and agreed to this bounded TEST_ONLY implementation contract. These are operational completions, not new sourced rules:

1. A finite fingerprinted profile admits actors and binds an explicit recreation activity to separate `SafeRecreation` and `MoraleRestEligible` site facts. Neither fact is inferred from Long Rest safety or qualification. The actor issues a voluntary start command; start/interruption consume no time, resource, check or RNG.
2. `RuleClock` records one 14,400-second interval. The participant cannot start it while assigned or performing incompatible work, traversing/travelling, consuming provisions, sleeping or in Short/Long Rest. A participant cannot initiate incompatible work, travel or rest while the interval is active. Other actors continue compatible work on the shared clock. Interruption earns no benefit and restart requires a new complete interval. A represented event that makes voluntary recreation impossible interrupts at its event boundary; emergency transitions without an authoritative event remain gated.
3. Boundary processing settles provisioning, Rest Debt and mandatory effects before Morale eligibility. Morale never clears or satisfies Rest Debt. Outstanding debt alone does not block Morale removal; an active point still needs both recovery flags, no applicable source/provisioning block, and the source's collapse exclusion. Null-classified Rest Debt points remain ineligible.
4. A qualifying completed interval consumes Morale's own 24-hour allowance even if no point can be removed or no candidate exists. A completion inside the allowance grants nothing and does not reset it. Gate clearance is not retroactive. Secure Long Rest keeps its independent allowance.
5. Recovery reuses the shared no-time exact-point patient-choice command. It freezes time and unrelated mutations, preserves any accepted clock continuation, and revalidates the exact actor, activity, completion, site and selected point. It never substitutes another point.
6. A Morale interval cannot overlap any part of a Long Rest interval, including its awake portion.
7. Schema65 uses one shared Strain history and typed recovery cause. The Morale interval and beneficial completion have distinct records. The shared recovery offer identifies its `RecoveryKind`, activity/completion, actor, exact offered point IDs, initiating command and choice. Removal points to `RecoveryKind + RecoveryCompletionId`. It creates no fake Long Rest and no second removal ledger. Schema64 codec bytes and profile/replay semantics remain unchanged.

## Authoritative records and consumers

- `ExpeditionMoraleRestIntervalRecord`: actor, site/activity IDs, actual start and planned end, actual end/status, start/end command IDs and revisions.
- `ExpeditionMoraleRestBenefitRecord`: actor, interval identity, exact qualifying completion time, optional recovery-offer ID and revision.
- `ExpeditionStrainRecoveryOfferRecord`: typed recovery kind, activity/completion references, initiating command, frozen ordered point IDs and chosen point/resolution revision.
- `ExpeditionStrainRemovalRecord`: existing gain/point identity and mutation order, with typed recovery kind/completion reference.
- `RuleClock`, world position/traversal, `WorkLedger`, assignment/work records, ordinary intake, Rest Watch/Rest Debt, existing daily-provisioning settlements, Strain projection, condition/life authorities, command/query/receipt flow, `ManufacturingAdvanceRecord`, and versioned snapshot codecs remain shared authorities.

No parallel clock, work ledger, inventory, RNG, character state, Strain counter, or recovery history is introduced.

## Runnable acceptance contract

The connected schema65 case must show two eligible daily-provisioning Strain points produced by actual unsupported-day settlements; actual lot-backed food/water intake opens the existing recovery gate; Morale runs while a companion's actual assigned work progresses, including mid-interval save/restore; coincident provisioning/Rest Debt boundaries settle first; Morale removes exactly one point without clearing active debt or changing HP/death/Wounds; a separate secure Long Rest later removes the other point under its own allowance. It also covers blocked/no-candidate and cooldown completions, incapacity/manual interruption and fresh restart, Long Rest overlap rejection, query/execution parity, pending-choice freeze, retained accepted clock targets, save/restore, duplicate protection and deterministic whole/split replay.

Scope remains finite TEST_ONLY content. General recreation catalogs, dynamic safety, unrepresented emergency dispatch, Haven care, other Strain-source recovery and Unity integration are outside this contract.
