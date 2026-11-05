# Site-aware repair traversal checkpoint

This checkpoint removes the tool-repair fixture's hidden `(3,3)` work-position constant. The authored repair fixture now supplies the site position, and repair admission checks the actor's actual position. The regression travels from the companion's starting point to a different authored site, saves and restores during a partial edge, and then starts the existing repair procedure only after arrival.

This remains TEST_ONLY integration. It does not add a persisted expedition assignment intent, a general site directory, an assistant plan, autonomous routes or production site authority.

- [Source bindings](SOURCE_BINDINGS.json)
- [Source-binding validation](RULE_BINDINGS_VALIDATION.json)
- [Site-aware work decisions](../../SITE_AWARE_WORK_RULE_DECISIONS.md)
- [Full 1,102-case suite](HEADLESS_RESULTS.json)
- [C# compile](COMPILE_RESULTS.json)
- [Static package checks](PACKAGE_RESULTS.json)

The related [Trap](../2026-11-05-fishing-stock-manifest/README.md) and [companion travel](../2026-11-05-companion-travel/README.md) checkpoints cover the other admitted site and traversal boundaries.

Source-scope correction: the prior manifest described BODY_EQUIPMENT_PLAYTEST.md too broadly as a repair-procedure source. The actual generic repair contract is Expedition Player Book FL-18. The historical manifest and validation receipt remain frozen; the corrected scope is pinned and validated in the [schema39 assignment evidence](../2026-11-05-expedition-assignments/SOURCE_BINDINGS.json).
