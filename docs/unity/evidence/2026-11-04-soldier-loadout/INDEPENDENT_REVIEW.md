# Independent review: Soldier Level 1 initial card selection

Reviewer: `/root/source_review` (read-only review)

Scope: pinned Soldier source fidelity, schema/persistence compatibility across schemas 21–26, selection/grant validation and likely dispatch/restore regressions.

Findings: no actionable functional findings. The four choices match the pinned Champion Level 1 example and its four-choice / minimum-two-active schedule. Automatic Overwatch remains separate. The new profile blocks the old level-up pair, avoiding duplicate Tactical Reposition. Selection records are bounded, copied, persisted and checked against matching grants, profile, class and source revision. The enum value was appended and record serialization is schema27-gated, preserving prior schema layouts by inspection.

The reviewer recommended testing feature use after restore. A regression was added that restores the snapshot, begins tactical combat and activates Tactical Reposition through the shared Bonus Action ledger. The reviewer did not execute tests or compare historical save bytes; those claims are not attributed to the review.

## Limits

The review confirms only this increment. It does not certify the full Soldier build, the unconnected Warning Shot/Covering Fire/Shield Trained effects, Unity compilation, release eligibility or gameplay balance. The full headless suite and package/source binding validators were run separately; see `HEADLESS_RESULTS.json`, `PACKAGE_RESULTS.json` and `RULE_BINDINGS_VALIDATION.json`.
