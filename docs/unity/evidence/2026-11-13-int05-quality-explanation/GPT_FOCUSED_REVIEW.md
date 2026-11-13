Actual Unity Rules Engine Development reply `46dfc1e6-bec8-4e57-b555-b154d36dab47`, recorded verbatim apart from trailing whitespace.

## INT-05 pending recipe-4 explanation — focused review passes

**Reviewed source:** `8ff2ceea32ded339bb043b9669718535683ee577`
**Reviewed evidence:** `abcd529d826751abf01f7d315d539d42ed362a04`
**Controlling authorization:** `1ae13e3c-5679-4aa9-95ce-364d2676ef79`

**I found no concrete source or focused-evidence blocker. No correction or additional focused scenario is requested. Hold final acceptance solely for E1: the completed exact-bound 1,491-case regression.**

The source-to-evidence comparison contains one documentation/artifact commit and **no subsequent engine or console-source changes**. Continue the current bound run; no rebuild or restart is requested.

## 1. Read-only API, authority and information boundary — met

The implementation checks the Player seat and valid decision ID, obtains the current grant, captures state under the session lock, and requires the matching revision and actual top pending decision. `OwnedQualityOrder` additionally checks worker control, inventory permission, the selected connected order, known recipe-4 formula and Exceptional quality. A matching awaiting order alone cannot bypass a higher-priority decision.

The method uses ordinary `Simulation.QueryCommand` admission for each proposed native choice. That path performs current preflight and assesses a detached state; it does not execute or commit the choice. The temporary probe ID is neither returned nor committed, and the implementation avoids collisions with existing receipts. The focused history deliberately commits `quality.explanation` beforehand to exercise that handling.

The returned objects contain get-only values and a copied read-only alternatives collection. They expose the approved public source labels—not the internal manifest or its authority-reference collection. The observed DTO has no raw snapshot, material-lot identifiers, grant payload, future roll or predicted effective healing. Its healing text correctly distinguishes **2d4+2 magical nonspell healing** from container durability.

This is an advisory result. Actual submission retains current authority, stale-revision, duplicate and conflict checks.

## 2. Shared settlement calculation — met

The new `ManufacturingOutput` calculation is shared by explanation, actual settlement and connected-result validation. It retains `ManufacturingRules.Yield`, the source-vessel count and the existing durability condition. The explanation derives supplementary release from the **actual outstanding packaging claim**; a legitimate zero-extra order has no claim and reports zero consumption/release.

The inspected tests compare each explanation with real settlement:

| Actual Exceptional order | Explained and observed result |
|---|---|
| Two extras, Full Yield | Six one-HP doses; one supplementary vial consumed and one released |
| Two extras, Durability | Five two-HP doses; zero supplementary vials consumed and two released |
| Zero extras | Full Yield omitted and rejected by native admission; Durability produces five two-HP doses without a packaging claim |

The zero-extra branch is reached by changing the real manufacturing-start input and executing the history—not by modifying a saved reservation.

**Mishap ordering is preserved.** The refactor calculates the required output quantities, settles inputs, and only then performs the existing d6 and consequences. The later `inputsSettled` path still avoids a second debit. Component consumption, catalyst handling, XP and specimen settlement remain in their existing paths. The broader compatibility check for these shared changes is appropriately included in the pending full suite.

No schema, content fingerprint, gameplay command or existing console/view shape was changed.

## 3. Focused controls and connected evidence — met

The two registered controls cover repeated read-only queries, immutable alternatives, real option settlement, authentic pending restoration, revocation, re-enabling access, stale submission, exact duplicate and conflicting-ID behavior. They compare complete saved bytes around the relevant query and terminal controls.

The missing-knowledge, missing-inventory-permission, unsupported-Masterwork and higher-priority-knockout inputs are explicitly labelled **detached selector probes**. They are not claimed as restored or executed histories. Their use here is appropriate; the positive pending order and zero-extra branches are genuine public executions.

The public continuation verifier adds checks beyond those registered cases. It restores the accepted r106 save, repeats the explanation, compares the complete permitted view—including separately ordered `KnownTargets`—checks the exact DTO property sets, and requires unchanged pending bytes. It then continues through normal public submission and newly planned automatic-defender actions.

Its retained r107, r115 and r165 identities match the accepted Full Yield reference. The dose remains **4 and 1 on the d4s, seven potential healing, three actual healing, and one spent Action**. The final r165 digest remains:

```text
6f1bc7afa0f5727e76dccc26d0d33911682f791a3ca3e971ca1350c64dcdd521
```

These are retained verifier results I inspected, not executions I performed.

The separate connected report retains the accepted Default and Fishing Trap histories: **277/322 responses, 223/242 committed actions and all six checkpoint identities**. Their recorded complete-transcript digests match the accepted predecessors. **I compared the recorded identities; I did not independently hash or reread every transcript row.**

## 4. Build evidence and remaining E1

The packet records two passing focused cases: one in the headless compilation/execution report and the second in `zero-vials-result.json`. Standalone C# 9 compilation passes Core, Persistence and LabModel. Static validation records **18/18 passing checks, 399 assets and 399 unique GUIDs**. This is not Unity import, compilation or gameplay validation.

The query measurements—84.1792 ms first observation and 0.7852 ms warm p95 across 20 observations—remain descriptive. No new performance criterion was imposed, and these figures do not close broader P1.

| Approved acceptance group | Disposition |
|---|---|
| **1. Pure, accurate explanation** | **Met** |
| **2. Explanation-to-settlement agreement** | **Met** |
| **3. Authority, privacy and lifecycle** | **Met** |
| **4. Exact implementation compatibility** | **Focused/build portions met; E1 pending** |

The manifest correctly leaves `regressionCases` null. Final closure requires the **unchanged 1,489 predecessor cases plus the two new registered cases**, totaling **1,491**, on the reviewed assembly set. The retainer checks source inputs against the implementation archive and requires the established launch/start/completion, loaded-module, assignment and ordered-journal bindings when finalizing the run.

**That completed execution is the sole remaining acceptance condition.** No redundant scenario, separate historical run or new source/API packet is requested.

## Inspection limits and final disposition

I inspected the implementation diff, new explanation and shared-calculation logic, focused test controls, relevant existing query preflight, public continuation verifier and outputs, connected report, build/static summaries, bindings, retention logic and source-to-evidence comparison.

**I did not compile, execute tests or scripts, load DLLs or binary saves, recompute artifact hashes, independently replay the histories or run Unity.**

**Final focused ruling: hold `8ff2ceea32ded339bb043b9669718535683ee577` only for completed E1. No concrete correction is required.** Prior acceptances stand; no successor is selected or authorized in this review. Wider INT-05, broader P1, production authority and Unity integration retain their existing limits.
