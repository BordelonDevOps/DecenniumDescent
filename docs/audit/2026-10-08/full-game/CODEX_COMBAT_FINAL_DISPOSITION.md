# Combat exact findings: implemented disposition

Both material fixes and the requested clarifications are implemented. Validation now PASS112 bounded checks plus285 movement-cost invariant states.

1. `marker_deadline(..., excluded_current_marker=None)` computes the first strictly future scheduled marker, compares that exact marker to the excluded current-end marker, and advances6 only if equal. Tests cover application1/end3→9; application4/excluded3→9; applicationexactly3/excluded3→9; two future ends with current end excluded→15. No blind Boolean skip remains.
2. Added `ManeuverAttempts`: separate Pin and Silence tokens, refreshed only by increasing regular-start ordinals. Legal declare-and-roll consumes on hit/miss; rejected illegal declaration consumes nothing. Extra turn and round boundary do not reset. Tests cover all your listed cases plus repeated-marker rejection and optional-maneuver conflict.
3. Ally-targeted bare N-round buffs explicitly use source-start convention; explicit target/pulse/absolute clock wins. Guide cites your exact review.
4. Ready effect duration explicitly begins at release; setup casting/cost/hold/Ready clocks stay at preparation. Separate helper tests prepared0/released4/3 elapsed rounds→22, and prepared1/released4/target end phase3/3 target markers→21. Release-before-prepare rejected. Caller still validates unexpired legal Ready state.
5. Added exact HP-helper scope sentence and Boolean-only Hide helper scope. Simultaneous arbitration remains outside HP helper, as documented. Secure Cargo/Load terminology remains open.

One specific-source exception found while collecting the next Strain sources needs your explicit acknowledgement so the generic Reaction rule does not erase it:

`data/public/class_playtests/warrior.json`, card `warrior.supplement.mind-shock`, serumProfile, Via Serum Injection, cost Dose consumption and normal Strain, duration3rounds, frequency Per prepared dose:

> Gain +2 on saving throws against spells. Once during the duration gain one additional Reaction usable only for movement, defense, Counterspell-like disruption already possessed or another non-attack reaction; it cannot make an attack. Side effect: -1 on Perception checks for the duration. Serum Tolerance suppresses that penalty.

Original source preserved on card: `| Mind Shock | +2 Save vs spells | +1 reaction use this turn | 3 rounds | Minor Hallucinations |`.

Proposed boundary: our interval model governs the ORDINARY Reaction. A reviewed explicit extra-Reaction card is a separate limited source grant, not a refresh of the ordinary resource and not a general permission for extra reactions. Mind Shock cannot make attacks or bypass Focused/Surprise/Incapacitated restrictions, and cannot teach Counterspell. Exact per-dose refresh/reapplication and all other class resource-grant interactions remain part of the all-source semantic pass; do not claim the ordinary `ReactionClock` helper models these. The guide now explicitly states this helper exclusion; source-card text is unchanged. Please confirm that source preservation and generic boundary, or identify a needed correction.

After the above bounded combat disposition, please proceed to the attached Strain namespace conference. This is continuing the whole-game work; the six broad combat ledger rows stay open. No original source has been deleted.
