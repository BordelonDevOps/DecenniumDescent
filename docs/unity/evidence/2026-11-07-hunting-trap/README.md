# Schema55 ordinary hunting-trap evidence

This evidence packet covers a TEST_ONLY implementation of one reviewed authored PLAYTEST procedure. It does not claim the full rules engine or EXP-06 is complete.

## Source and implementation

The pinned hunting-trap procedure and relevant equipment/body compatibility sources are copied to `sources/`. `SOURCE_BINDINGS.json` records their source revision and SHA-256 hashes, lists the changed implementation files and their hashes, and names the focused acceptance cases. The authoritative source is `EQUIPMENT_ITEM_PROCEDURES.md`, “Traps and restraints,” at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba`; the equipment catalog separately records the physical item as 25 lb. The procedure is reviewed authored PLAYTEST text, not original-book wording or release approval.

Schema55 adds persisted deployment, action, trigger and tether records while retaining the existing portable-equipment item as the sole physical device. It shares the command transaction, clock, work reservations, inventory, exploration/tactical movement, route checkpoint motion, Overwatch ordering, RNG, actor-life consequences and canonical snapshot codec. Delegated integration completions and unsupported edges are recorded in [HUNTING_TRAP_RULE_DECISIONS.md](../../HUNTING_TRAP_RULE_DECISIONS.md).

## Runnable acceptance

The six focused cases exercise:

- shared exploration clock, mining work, portable-item mass/custody, set, trigger, save/restore, damage, exact tether, movement rejection, self-release, reset and retrigger;
- actual authored route checkpoint entry, split advance, save/restore, duplicate command, exact pause, release and explicit resume;
- the segment-completion exception;
- route mapping/schema composition;
- an actual tactical Overwatch shot followed by pending-entry Push rejection with committed shot/RNG unchanged, then a supported rider continuation;
- the pending-entry movement geometry gate.

## Validation

- Headless C# 9 warnings-as-errors suite: **PASS, 1,204/1,204**, zero failures. PowerShell 7.6.9 / .NET 10.0.14. Full report and package-source hashes: [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json).
- Static package validation: **PASS, 18/18 checks, 253 package assets and 253 unique GUIDs**. This validates package structure and dependency references only; it is not runtime integration or release-build validation. Report and source hashes: [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json).
- `git diff --check`: **PASS** at the implementation checkpoint; rerun against the final documentation and commit tree.
- GPT review: “Unity Rules Engine Development” found no confirmed blocker in the supplied implementation summary. It confirmed the reservation arithmetic and route endpoint exception, noted the separate already-established-tether Push gate, and listed three nonblocking focused regressions. See [GPT_REVIEW.md](GPT_REVIEW.md). GPT did not inspect the local checkout or run validation.
- Runtime integration, standalone build and gameplay were **NOT RUN**.

## Limits

The implementation admits explicit TEST_ONLY trap profiles and fixture-authored compatible bodies, anchors and trigger cells. It has no general hazard framework, arbitrary trigger geometry, concealed-trap discovery, moving/destroyed anchors, aerial or anatomy-incompatible entrants, teleport entry, route mid-leg trigger support or fractional tactical displacement. A Push beyond three feet while an entry is pending remains explicitly unsupported. This increment does not complete EXP-06 or the C# rules engine.
