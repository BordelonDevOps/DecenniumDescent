# Correction attempt log

## Reproduced GPT findings

The three baseline failures and their root causes are summarized in [REPRODUCTION.md](REPRODUCTION.md). The original GPT hold remains preserved in the parent [review record](../../GPT_REVIEW.md).

## Test fixture adjustments

- The first late-cause fixture path collided with the companion's tactical cell. The report is retained as `attempts/late-scenario-initial-occupied-square.json`; the corrected path avoided that occupied cell and reproduced the actual `InvalidResult` from the checkpoint validator.
- The first retreat fixture tried to leave the closed route through exploration from a non-origin cell and returned `ExpeditionPressureRouteDepartureUnsupported`. The report is retained as `attempts/retreat-scenario-initial-setup.json`. The final fixture starts at the authored route origin and exercises tactical retreat and the actual opportunity response.
- The first post-fix late-cause continuation tried to restart a completed route, then called a single-route helper after adding a continuation route. Those are retained as `attempts/late-scenario-initial-continuation-route.json`; the acceptance now uses a second explicit TEST_ONLY route and pauses that route by its own identity.

## Compiler iteration

The first Core validation attempts caught incorrect helper qualification after moving causal projection and attack-membership logic into the shared Core rules class. The exact compiler reports are retained in `attempts/compile-first-correction.json`, `attempts/compile-second-correction.json`, and `attempts/compile-third-correction.json`. The calls were qualified through `ExpeditionPressureRules`; the focused cases, full C# suite and dedicated three-assembly compile then passed.

No test failure was hidden or used to weaken source validation. The final validator compares checkpoint IDs with the source rows available at that checkpoint's causal position and keeps later rows available for the explicitly agreed derived reconciliation.
