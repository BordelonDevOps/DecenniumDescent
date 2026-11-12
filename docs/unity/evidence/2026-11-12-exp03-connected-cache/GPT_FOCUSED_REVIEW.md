# Unity Rules Engine Development focused EXP-03 review

Response `13dfe643-d663-464b-b17c-dd202aa66597` reviewed source `e7e3d556f179f472f8c73b35e2fd99074da04df6` and evidence `25d2f00f2e70c70700da81d2f03cbd7b902db370`. [Review chat](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

## EXP-03 connected supply cache — focused requirements met; final acceptance held for regression

**Source reviewed:** `e7e3d556f179f472f8c73b35e2fd99074da04df6`
**Focused evidence reviewed:** `25d2f00f2e70c70700da81d2f03cbd7b902db370`
**Controlling contract:** `84f2499c-22f3-4d15-8762-f67b068e0a17`

**Groups 1–4 are met on the inspected source and focused evidence. Group 5’s public execution, persistence, compatibility and build portions are supported. I found no concrete blocker and request no correction. Final acceptance remains held solely for E1: the completed exact regression.**

The source-to-evidence comparison contains one documentation/artifact commit and **no subsequent package or console-source changes**. No successor is authorized.

## 1. Disposition against the five approved groups

| Approved group | Current verdict |
|---|---|
| **1. Unchanged selected authority** | **Met.** The selected initial state and accepted revision-165 state remain byte-identical. The existing cache, ration root, physical tools and carried reserve retain their original authorities. |
| **2. Paid access lifecycle** | **Met.** Actual retrieval, paid picking, failure, fresh retry, interruption and separate opening are demonstrated. The pending pick restores with its remaining time and original payment. |
| **3. Scoped public information and inputs** | **Met.** Cache-location filtering corrects the locked-stock disclosure. Fresh operations are limited to the approved hero, object and methods. In-cache portioning/intake reject; receipt retries retain their established ordering. |
| **4. Finite retrieval and persistent revisit** | **Met.** Actual pickup depletes the root into one carried descendant. Departure, restoration, remote duplicate delivery and depleted revisit preserve the same stock and chest. Partial pickup and normal carried portioning are separately exercised. |
| **5. Compatibility and exact execution** | **Focused portion met; E1 pending.** Public C# and console continuations agree; authentic predecessor restoration and false-history rejection are retained. The 1,483-case execution has not completed in this packet. |

I read the complete new registered case and its assertions, not merely its passing summary. It is **one registered case containing multiple controls**, supplemented by the connected C#/console walkthrough—not several independently reported focused cases.

## 2. The adapter preserves the approved authority and visibility boundaries

### Existing rules remain authoritative

The implementation does not add a cache, relocate stock, change the selected policy configuration or alter the save layout. Its only inherited cache-resolver edit changes `NearCache` from private to internal so the adapter can reuse the exact same-cell/cardinal reach predicate.

`ReachableCache` additionally requires ordinary mode and no active hero traversal. Fresh cache commands require the hero and the exact cache. `HandleInventory` is limited to the exact root’s available stock and `Pickup`, with the underlying resolver retaining amount, hand, capacity, work and physical-transfer checks.

`Interrupt` is not given a new cancellation mechanism: it reaches the existing resolver, which determines whether the actual working attempt exists. First-opponent and automatic-defender authority are not expanded.

### Locked stock is hidden by physical location

The generic item projection excludes cache-located stock by its actual `ResourceLot.LocationId`, independently of whether the cache is open. This avoids the earlier disclosure and does not incorrectly rely on the open-cache accessibility helper.

The separate cache view supplies a stock token only when the cache is open, reachable and the root has positive available quantity. The empty chest remains visible on revisit, but its stock token and quantity are absent. The API does not equate ownership with physical availability or claim that zero availability always proves physical depletion.

The approved portioning clarification is implemented consistently: fresh `PortionInventory` and `StartIntake` requests reject for lots physically inside this cache. After pickup, filtering follows the child’s new location, so the acquired child appears normally and can be portioned. The focused case retrieves **½ lb**, observes **1½ lb** remaining in the root, and then portions **¼ lb** from the carried child.

### Fresh-state filters do not invalidate legitimate retries

The existing session order is preserved: current seat authority and payload checks, receipt matching, then revision and fresh-target filtering for a new command. Matching receipts still reach `Simulation.Execute` under the current grant.

Consequently, the root becoming empty or the hero leaving reach cannot turn an exact committed pickup into a fresh unavailable request. The connected witness demonstrates that duplicate while remote at revision 179. The focused case separately rejects a revoked pick retry and conflicting reuse of its ID, while allowing the exact original retry after authority is restored.

## 3. Paid work, interruption and finite retrieval are actual execution

The principal route records the expected distinctions:

| Boundary | Retained result |
|---|---|
| **r170 — retrieve tools** | Actual linked tools leave the pack; the clock advances through ordinary handling. |
| **r171 — start first pick** | The lock remains closed, no pick result exists yet, and the six-second attempt is booked. |
| **r172 — partial save** | Two seconds have elapsed; the public view reports four seconds remaining. |
| **r173 — first completion** | Actual natural **11 + 2** fails; the cache remains locked. |
| **r174–175 — new attempt** | Another full six seconds produce natural **16 + 2** and unlock—but do not open—the cache. |
| **r176 — opening** | A separate elapsed second opens the cache and exposes the finite two-pound stock. |
| **r177 — pickup** | Another ordinary handling operation depletes the root and creates `inventory.177.lot`. |
| **r179–181 — departure and revisit** | Restoration preserves the open depleted cache; exact pickup retry is Duplicate, while fresh reopening and pickup reject. |
| **r183 — continuation** | Paid ordinary movement continues at **`113465/2`**. |

Both recorded completed pick attempts have `EndedAt == StartedAt + 6 seconds`. The verifier also checks unchanged RNG and no natural result in the pending save.

### Interruption does not refund the Action or duplicate remote work

The focused branch starts actual companion mining, begins the hero’s pick, advances two seconds and explicitly interrupts. Its assertions check:

- Interrupted status, no natural result and unchanged pick RNG.
- The booking ends at the actual interruption time.
- The hero’s Action remains spent.
- Companion mining receives exactly two seconds.
- An immediate new pick rejects; a later legal attempt books the full interval.

The tactical restriction is also tested at a genuinely adjacent hero position reached through combat commands, not merely from a distant or synthetic tactical state.

**Coverage qualification:** the new case does not independently rerun every inherited Poisoned, injury or timed-condition cache branch. Those rules were not changed; their broader execution remains part of the pending exact regression. I am not counting them as new focused witnesses.

### Physical conservation is checked separately from the public view

The custody audit records:

- Original root: **0 lb**, still identified at the cache.
- One child: **2 lb**, owned and custodied by the hero.
- Hero burden: **68 → 70 lb**.
- Original freshness deadline preserved.
- `TEST_ONLY.actor-skin` still carried with the same **four-pint** reserve lot.

The audit script derives these facts from the retained saves and the existing carrying calculation. It does not infer them from an empty UI token.

## 4. Public continuation, restoration and integrity

The walkthrough reconstructs the accepted route from actual initialization through the public session methods. It requires the initial save and revision-165 save to match their accepted predecessors before performing the cache extension.

It then compares the restored branch with an independently executed, uninterrupted branch using the same commands. The actual PowerShell console receives the serialized public inputs, returns the expected outcomes and produces matching pending and final files.

The retained final canonical digest is:

```text
5ec854b393c09fbf8da8ad15433d41a582ae12efe2629456af5e2606b40483dc
```

The console processes **213 input lines**. Its inspected pending view exposes the current pick and due time while withholding the root token and quantity. The verification script checks the cache-specific response sequence and compares both the pending and final console files with the C# branch.

The false-history test is meaningful: it changes the final chest to closed, encodes and decodes that plausible structure, then requires full session restoration to reject it. Saving the live session afterward must reproduce its pre-rejection final digest. This is **historical validation rejection before adoption**, not merely an invalid-checksum rejection.

The custody audit itself loads and inspects saved state; it is not a second independent simulation replay. The public restore/replay checks above provide that separate evidence.

## 5. Builds, timing and the remaining E1

| Retained check | Result inspected |
|---|---|
| Registered focused execution | **1 discovered, 1 passed, zero failed** |
| Standalone C# 9 compilation | **Core, Persistence and LabModel PASS** |
| Static package validation | **18/18 PASS; 397 assets and 397 unique GUIDs** |
| Authentic compatibility | Exact initial and revision-165 bytes retained; original revision-165 save restores unchanged |
| Full regression | **Pending—not represented as passed** |

These are Codex’s retained executions that I inspected, **not executions I performed**. Static validation is not Unity import, gameplay or release-build validation.

The retention script compares compilation/static source hashes with the implementation’s Git archive, retains the four executed DLLs, and checks the matching predecessor, pending and final file digests. The manifest identifies **371 headless, 272 standalone and 783 static inputs**. **I inspected that logic and its bindings; I did not independently repeat those hash comparisons.**

### Timing does not add a new hold

The reported cache-operation observations are approximately **12–17 ms** for tool retrieval, pick starts/completions, opening and pickup. Full pending and depleted-away restores are **5,622.736 ms** and **5,966.722 ms**, separately retained.

These are single observations, **not p95 measurements or a session-wide performance pass**. They meet this increment’s requirement to expose the added costs without disabling validation. No additional benchmark is requested for this bounded cache review. The existing broader P1 disposition remains unchanged.

### E1 remains explicit

The launcher requires the accepted **1,482 predecessors in order plus this one new case**, for **1,483 total**. The retention logic requires completed ordered journals, unique passing results and agreement with the focused row before producing the final report. The current manifest still has `regressionCases: null`.

**The completed exact-bound execution will satisfy E1; a redundant second regression is not required.**

## Inspection limits and final disposition

I inspected all changed paths, the complete new focused case, relevant current session admission/receipt code, the connected verifier, custody verifier, full cache timeline, representative console transcript sections, retention and regression-launch logic, report summaries, bindings and source-to-evidence comparison.

**I did not execute C# or scripts, compile, load binary saves or DLLs, independently replay the walkthrough, recompute artifact hashes, inspect every console line, modify files or run Unity.** This was a bounded source-and-evidence review, not a fresh whole-engine audit.

**Hold final acceptance of `e7e3d556f179f472f8c73b35e2fd99074da04df6` solely for E1. Groups 1–4 and the focused portions of group 5 are met; no concrete correction is currently requested.**

No source-authority or dependency concern was found. The selected cache remains TEST_ONLY, and EXP-03 retains its direct **EXP-01, MGT-01 and FND-02** prerequisites. Prior acceptances stand; EXP-04 and later work remain gated, broader P1/INT-03 remains open, and Unity gameplay integration stays deferred.
