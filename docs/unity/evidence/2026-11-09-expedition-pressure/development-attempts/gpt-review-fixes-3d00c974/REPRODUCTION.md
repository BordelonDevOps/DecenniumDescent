# GPT review finding reproductions

The baseline reports below run against the reviewed `3d00c974` runtime before the C# correction. Each report retains the compiled source hashes and the exact focused failure.

| GPT finding | Baseline result |
| --- | --- |
| Schema67 exact-Watch Haven admission records the legacy settlement reason and continues after restore | [Assertion failure](reproduction/schema67-exact-watch/results.json): the current code recorded `WatchEnd`, while schema67 requires `HavenArrivalAtWatchEnd`. |
| A late same-Watch attack remains evidence after an immutable early Haven checkpoint | [Command rejection](reproduction/late-watch-cause/results.json): the first committed attack returned `InvalidResult` because validation compared it against the checkpoint's earlier cause set. |
| An attack and tactical retreat at one RuleTime retain receipt order, including the departure opportunity attack | [Command rejection](reproduction/same-time-retreat/results.json): the opportunity response returned `InvalidResult`; exposure membership used strict end-time comparison, and collection ignored the just-ended exposure. |

The after-fix focused results are in `validation/focused/`. The connected late-cause report saves after two duplicate-category attacks, restores, admits at the actual obstruction deadline, verifies the original checkpoint is unchanged, starts the explicit continuation route on the next Watch, and verifies its `PressureBefore` carries the derived value once. The same-time case saves and restores the actual tactical retreat with both attack records linked to the closed exposure.

These are bounded TEST_ONLY cases over the fixed route/combat fixtures. They do not authorize production Haven content, new Pressure source categories, or a second roll/consequence.
