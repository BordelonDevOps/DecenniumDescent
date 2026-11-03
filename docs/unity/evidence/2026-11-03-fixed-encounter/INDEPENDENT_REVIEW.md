# Fixed-roster scheduler review

2026-11-03. The separate `/root/source_review` agent reviewed the bounded schema7 scheduler, historical handling integration, shared Action spending, authority/retry ordering and persistence. The reviewer made no edits and did not rerun the complete suite.

Two concrete restore defects were independently reproduced in memory and corrected:

1. A food-handling record renamed to `inventory.9223372036854775807.handling` restored at revision2, then prevented a valid `EndRegularTurn` from committing. History now rejects future revisions, regular-start collisions and duplicate action revisions. Boundaries, food/vessel interactions and Dash must match their committed command receipts. Regression: `encounter_restore_rejects_future_food_history_before_it_can_stall_turns`, with additional collision and unrelated-receipt cases.
2. Removing both a paid Dash record and its receipt while retaining revision2 restored a free Action. Post-entry receipts must now cover every committed revision without gaps. Regression: `encounter_restore_rejects_missing_action_and_its_receipt`. The reviewer independently confirmed the original reproduction now rejects with `InvalidEncounterCommandHistory`.

The final review found no remaining defects within this scope and verified all57 compiled source hashes against466/466 PASS, including25 encounter cases, in `run-20261103T223757917Z-8e3f4a95`. Exact slot repetition, six seconds per round without a wrap surcharge, shared Dash/second-interaction spending, ending a spent turn, background crop milestones and current authority before retries were inspected.

The parent ran the complete466-case headless suite,8 package checks and source-binding validation. The parent also compared46 overlapping saved outputs from the441-case schema1–6 baseline; all matched byte-for-byte. Randomly named recovery-evidence paths were excluded when unmatched. The reviewer did not independently perform that legacy comparison.

Scope remains a supplied fixed roster of capable nonsurprised actors with no actor effects, attacks, reactions, extra turns or end-round events. The scheduler does not implement procedures for content it cannot admit. General spatial legality, full character/life persistence, roster transitions, encounter exit, Unity execution and release qualification remain outside this checkpoint. Receipt matching detects structurally inconsistent histories; it does not authenticate edited saves.
