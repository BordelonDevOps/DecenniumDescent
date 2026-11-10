# MGT-04 GPT review correction packet

**Status:** The concrete findings from GPT's review of `fd561c5e8b08e915b3d79ca952a16db04da3e36e` have been addressed in the correction commit below. The exact implementation review is pending. MGT-04 and the engine are not marked complete; no successor module has started.

**Reviewed source candidate:** [`11e77c50012d97acd5f24e91b523283ed957a96a`](https://github.com/BordelonDevOps/DecenniumDescent/commit/11e77c50012d97acd5f24e91b523283ed957a96a) on `Engine`.

## Scope, requirements and authorities

This is a bounded correction to the existing `TEST_ONLY` recipe-347 craft-to-mining increment. It preserves the agreed recipe source contract in [MGT04_RECIPE347_RULE_DECISIONS.md](../../MGT04_RECIPE347_RULE_DECISIONS.md) and the pinned source rows in the [MGT-04 source bindings](../2026-11-09-mgt04-recipe347/SOURCE_BINDINGS.json). It adds no new recipe, character-creation, advancement, class, or balance rules.

The increment remains bound to the existing shared `WorkLedger`, active work progress, `RuleClock`, character/check facts, RNG, inventory lots, physical portable equipment and structures, mining records, command receipts, and snapshot codec. Recipe-produced behavior is version-scoped; historical schema49 mining and the prior schema18/20 Alchemy/portable paths retain their legacy rules. Counted ingredients remain single authoritative WorkLedger/inventory lots with physical mass and packed volume derived from the current integer quantity.

## GPT findings addressed

GPT's review of the previous candidate identified these acceptance blockers:

1. Mishap 3 reduced the Miner’s-tools structure HP, while fixture validation still required full HP. Validation now derives current HP from the persisted, ordered Mishap damage facts and preserves the same structure identity, maximum HP, material and mass.
2. Recipe Mining recalibration used hard-coded site assumptions. The recipe path now verifies the incident's actual Miner’s-tools target, authored workshop and intact station, item's actual ground location/custody/access, worker reach, and positive `mining-tools` training. The separate legacy Alchemy path is preserved.
3. Counted inventory accepted fractional quantities. Commands and portable-lot snapshot validation now reject fractional indivisible handles; legal whole-unit splits, mass, volume, custody and save/replay remain covered.
4. Recipe lifecycle behavior leaked into schema49 mining. Paused pending claims and relocated historical use results now retain their pre-recipe behavior; the newer release/relocation lifecycle applies only to recipe-produced tools.
5. The connected acceptance did not show the full gameplay path. A runnable case now connects authored exploration, a tactical encounter, physical cache acquisition, physical storage, recipe work, the same output used at two deposits, and continued exploration, with restored branches compared byte-for-byte.
6. Half-open Work Watch endpoint behavior needed an explicit assertion. The focused case now asserts that adjacent intervals meet exactly at the shared 32-hour endpoint.

One detail in the previous GPT note appears inconsistent with the checked source: it referred to `AssayKitStructureId` as the mishap target. `SharedRecipe347.cs` passes `MiningToolsStructureId` to the mishap fact, and the correction retains that actual Miner’s-tools target. This is recorded for source-level reconciliation, not treated as a gameplay-rule disagreement.

## Exact changed files

Source commit `11e77c50012d97acd5f24e91b523283ed957a96a` changes these seven files:

- `engine/com.decennium.foundation/Laboratory/Model/PortableEquipment.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedCraftingConsequences.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedRecipe347.cs`
- `engine/com.decennium.foundation/Laboratory/Model/TestOnlyInventoryPolicy.cs`
- `engine/com.decennium.foundation/Runtime/Core/MiningRecords.cs`
- `engine/com.decennium.foundation/Runtime/Core/PortableEquipmentRecords.cs`
- `engine/com.decennium.foundation/Tests/EditMode/Recipe347Cases.cs`

## Runnable acceptance scenarios and validation

Each focused run compiled the C# 9 shared-source harness with warnings as errors and retained 276 source hashes.

- [Mishap 3 damage, save/restore and deterministic completion replay — PASS 1/1](focused/run-20261110T093545812Z-3a3b9f6e/results.json). The case saves one active second before the automatic result check, restores two branches, advances both through the same boundary, checks identical settlement and HP 5→4, validates no output and correct material settlement, then restores and replays the duplicate clock command without applying damage twice.
- [Six result bands and source-qualified Mining remedy — PASS 1/1](focused/run-20261110T094131912Z-0860b3c8/results.json). The inaccessible-kit branch is produced through recorded pickup, movement and drop commands, so it remains a valid replayable snapshot.
- [Schema49 pending-claim and historical-result compatibility — PASS 1/1](focused/run-20261110T084002959Z-6f639889/results.json).
- [Counted-lot whole-unit transfer, storage, physical conservation and replay — PASS 1/1](focused/run-20261110T092731881Z-ce7b9364/results.json).
- [Connected exploration → encounter → acquire → manage → craft → use at two deposits → continue — PASS 1/1](focused/run-20261110T090323985Z-9509b9eb/results.json). The scenario verifies persisted/restored branches and deterministic continuation.
- [Core, Persistence and LabModel standalone compilation — PASS](compile/compile-20261110T092633663Z-3ab97ffd/results.json), C# 9 warnings-as-errors, 201 source hashes.
- [Static package validation — PASS 18/18](package/static-20261110T091546082Z-ad9a9ba3/results.json), 302 assets and 302 unique GUIDs.
- `git diff --check` passed before the source commit.

The full regression suite was attempted from this correction worktree, compiled, then remained CPU-active without producing a report for more than 17 minutes. It was stopped; this run is **incomplete**, not a pass or a code failure. Its evidence directory is `full-suite/run-20261110T091238560Z-ba74c8a7/`. The earlier 1,314/1,314 full-suite result belongs to the pre-correction candidate and is not claimed as validation of this commit.

Unity Editor import, Editor tests, Play Mode, player builds and observed player gameplay were not run. The connected acceptance is a C# simulation scenario, not presentation integration.

## Review gate

Please review the exact source commit, seven-file diff, pinned sources, acceptance runs, full-suite limitation, and the source discrepancy above. Codex will not start the next mapped module until GPT confirms that the blockers are closed and the next step follows the approved dependency order. See [the review request](GPT_REVIEW_REQUEST.md); the actual GPT response will be recorded separately after it arrives.
