Actual Unity Rules Engine Development reply `79ea7c8b-da8e-44e7-8bfd-fe9902ab599d`, recorded verbatim apart from trailing whitespace.

## EXP-05 local travel and finite mining — focused requirements met

**Reviewed source:** `24fd553441c802c5b322c489804dc1fada71a98f`
**Reviewed evidence:** `720f4df1e193a2439cf1ffadc5df97aca41bcb66`
**Controlling authorization:** `02a9ed1a-d334-43a3-acdc-2ac91a4bb1f4`

**Groups 1–4 are met on the inspected source and focused evidence. Group 5’s persistence, compatibility and build portions are supported. I found no concrete blocker and request no code correction or additional focused scenario. Final acceptance remains held solely for E1: the completed exact 1,485-case regression.**

The source-to-evidence comparison contains one documentation/artifact commit and **no subsequent engine or console-source changes**. No successor is authorized by this interim review.

## 1. Disposition against the approved requirements

| Requirement | Focused verdict |
|---|---|
| **1. Actual travel progress** | **Met.** The public projection derives fractional position and expenditure from the existing traversal and current timing owner. Partial restoration preserves the edge and allowance. |
| **2. Existing finite-site work** | **Met.** Actual arrival precedes the original mining procedure. The existing worker, finite selection, labor, check, recovery and subsequent sale remain connected. |
| **3. Persistent revisit** | **Met.** Departure, restoration and actual return preserve the original unit dispositions. The fresh mining retry rejects without another receipt; ordinary movement continues. |
| **4. Permitted public operation** | **Met within the selected scope.** Own traversal is exposed only through the controlled actor view. Current site details require the authorized owner’s local presence; the opposing seat receives no site view. |
| **5. Compatibility and replay** | **Focused portion met; E1 pending.** Restored and uninterrupted console histories and public C# replay agree. Authentic r208 restoration, compilation and static checks are retained; the full regression remains unfinished. |

## 2. The projection uses existing movement authority

The complete diff changes **three files**: `ConnectedExpeditionView.cs`, the visibility of two existing allowance helpers in `TestOnlySharedWorldPolicy.cs`, and the registered session-case file. There is no new movement command, clock, resource ledger, mining procedure or serialized state.

`ExpeditionTraversalView` obtains exact coordinates from `WorldPositionResolver.Position`. It separately reports the current edge’s paid distance and remaining distance. For allowance ownership, it uses `WorldTiming.ForActor`: scheduled actors read their actual personal interval, while off-calendar actors read their actual activity interval. The remaining-allowance calculations reuse the existing helpers rather than duplicate movement arithmetic.

That distinction matters in the connected witness. At **r23, clock `43/2`**, the companion’s public view reports:

| Fact | Actual value |
|---|---:|
| Edge | `(4,3) → (3,3)` |
| Exact position | **`(7/2,3)`** |
| Paid on this edge | **`5/2 ft`** |
| Remaining on this edge | **`5/2 ft`** |
| Activity interval | **3**, `world.fixed-calendar` |
| Total interval movement spent | **`15/2 ft`** |
| Remaining interval allowance | **`45/2 ft`** |

Thus the projection preserves expenditure from the preceding step in that interval; it does not mistake current-edge progress for total expenditure or grant a fresh allowance on reload. The older integer position remains the traversal anchor, while the new `Traversal.ExactX/ExactY` explicitly supplies the fractional position.

The registered control independently starts an ordinary companion edge, saves while partially traversed, restores it, compares position and allowance fields, retries the original step as `Duplicate`, completes both branches, and compares the final canonical bytes. It also rejects the first-opponent seat’s attempt to command that movement.

## 3. Site visibility and finite disposition are correctly separated

### Local information is not a remote depletion query

`ProjectMiningSite` requires control of the selected deposit owner and permission to use that owner’s inventory. Its fresh local details additionally require ordinary mode, no traversal by that worker, awareness, sight capability and the existing same-cell/cardinal range.

When those local conditions fail, the view retains the **already-known site identity and location**, but returns `ClaimClosed: null` and no unit records. It does not manufacture a remembered current stock state. The first-opponent view receives no mining-site projection.

The actual partial-edge console view demonstrates those restrictions: the companion receives its exact traversal, but the site is not reported as locally observed and its unit details are empty. The first-opponent view has neither the companion’s traversal nor the site view.

This is a bounded projection of the existing known, exposed site—not a general discovery or remote-assay capability. The inherited owned-item projection remains separate; the new site view does not grant physical access to those items.

### `ClaimClosed` is not presented as “everything is gone”

The new flag uses the same “an attempt already exists for this deposit” condition that causes the existing resolver to return `MiningDepositClaimClosed`. That prevents a fresh extraction; it does **not** assert that every physical unit was destroyed or removed.

The unit records retain the actual distinction:

- **Iron: `Extracted`**, with its original recovered-lot identity.
- **Copper: `Forfeited`**, with no recovered-lot identity.

The inherited mining procedure marks unselected accessible units Forfeited when removal work commits. Successful extraction moves the same selected physical lot into its receiver rather than creating another mineral identity.

The revisit therefore correctly reports a closed extraction opportunity **and** the separate unit dispositions. Copper’s remaining physical matter is not relabelled as an extracted reward or nonexistent stock. The iron’s recovery link is historical provenance, not a claim that the companion still owns the sold lot.

## 4. The connected route uses real work and preserves continuation

The public input history performs the departure and return before starting mining. At r24 the companion has arrived, and the saved state contains no mining attempt yet. `StartMining` then creates the actual attempt, followed by the ordinary **1,800-second** advance and physical retrieval of the recovered iron.

The retained result reports `mining.extraction.25`, **1,800 active seconds**, natural **10**, modifier **+2**, Success, and one subsequent sale of that same recovered lot for **2 cp**. The payment remains historical sale evidence, not a new claim about currently available cash.

The walkthrough generator adjusts command-derived identifiers and elapsed inputs to accommodate the added travel. Its additional **`31/2` seconds** on the later advance is actual operator input, allowing the required research labor and interval refresh to occur. It does not change the resolver, shorten work, reset time or install completion.

On the later revisit, the console records the restored departure, paid return to cardinal reach, the two terminal mineral dispositions, and a fresh mining request returning `Unavailable` at **the same revision 221 and clock `113725/2`**. Subsequent paid travel reaches r223.

### What the three execution paths prove

The verifier compares pending and final save hashes across:

**Restored console execution**, **console execution with loads omitted**, and **a fresh public C# session replaying the committed history**.

The direct C# path reconstructs commands with `CommandHistory.Read`, checks their correspondence to the console’s committed IDs and revisions, and submits them through the normal public seat/session methods. For automatic defender inputs, it calls `AdvanceAutomaticDefender` afresh rather than simply injecting the archived defender command.

**Evidence qualification:** this third path is receipt-based public replay, not a third independent JSON parser. It replays committed inputs; the negative repeat-mining request is checked separately against the actual console response. I am not describing every rejected console input as independently replayed by that C# loop.

The retained identities agree:

```text
Partial edge:
ef38495fc38f025462a928bafc252c046989a2d7f1749313d627e41e383ef6bd

Final r223:
90d28e236200e017267f367f20d244f3df2223a355f09b1ebec5ac35ae491e41

Authentic accepted EXP-04 r208:
484c52179f7788ff456d3a2b318f1be6872f649e696f0bdd062317b23d712228
```

The verifier separately restores the authentic EXP-04 save and requires byte-identical re-encoding. The report records final clock **`113737/2`**, 277 console inputs and 223 committed C# actions.

**I compared these recorded identities; I did not independently recompute the save hashes.**

## 5. Builds, timing and the sole remaining E1

The exact focused report records **one discovered case, one pass and zero failures** for `exp05_session_exact_local_traversal_restore`. The connected walkthrough supplements that registered case; it is not an additional registered test count.

The standalone C# 9 report passes Core, Persistence and LabModel. Static validation passes **18/18 checks**, with **397 assets and 397 unique GUIDs**. These are retained Codex executions I inspected, not executions I performed, and they do not establish Unity import or gameplay validation.

The retention script binds compilation/static source entries to the implementation archive and checks all three pending/final save pairs before retaining the report. The manifest records **371 headless, 272 standalone and 783 static source inputs**, together with the four executed DLL digests. I inspected that binding logic and its output; I did not repeat the complete source or artifact hash audit.

The added command-and-view observations range from approximately **11.2 to 76.5 ms**. The separately measured full partial-edge restore is **857.635 ms**, at the much earlier r23 history. These are individual observations under the stated workload conditions—not p95 evidence or a claim that late-history restoration has improved. **No additional performance hold is introduced; broader P1 remains unchanged.**

### E1 closure requirement

The launcher requires the ordered **1,484 accepted predecessor cases plus this one new case**, for **1,485 total**. The finalizer requires completed ordered journals, unique passing rows, no errors, exact inventory equality and agreement with the focused result. The current manifest correctly leaves `regressionCases` null.

**Only that completed exact-bound execution remains. No replacement focused witness or redundant second regression is requested.**

## Inspection limits and final disposition

I inspected the complete three-file implementation diff, the new registered case, the relevant session-view code, inherited mining admission/settlement paths, `README.md`, `BINDINGS.json`, `New-TravelWalkthrough.py`, the complete `Test-TravelWalkthrough.ps1`, selected actual console inputs and responses, connected results, retention and regression-launch scripts, build/static summaries, and the source-to-evidence comparison.

**I did not execute programs or scripts, compile C#, load DLLs or binary saves, independently replay gameplay, recompute digests, inspect all 277 console responses, modify repository files or run Unity.**

**Hold final acceptance of `24fd553441c802c5b322c489804dc1fada71a98f` solely for E1. Groups 1–4 and the focused portions of group 5 are met; no concrete correction is currently requested.**

The increment stays within EXP-05’s approved **TAC-01, MGT-01 and EXP-04** dependency scope. Prior acceptances stand. The requested **MGT-06 finite unattended-trap source/API gate remains the next separate step after actual EXP-05 acceptance**, not authorized implementation now. Broader P1 and INT-03 remain open, production authority is unchanged, and Unity gameplay integration stays deferred.
