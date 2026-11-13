Actual Unity Rules Engine Development reply `d283220e-72b5-4770-9821-4a8aba17807a`, recorded verbatim apart from trailing whitespace.

## INT-04 recipe-4 scenario verification — approved

**Reviewed contract:** `9d0e791836eef7ee89c123d24e18ed380ba1f7cf`
**Engine under verification:** `75872e1e01fea9b17fce0c5c6c34d56679848961`
**Controlling successor ruling:** `2e34e0fe-dffb-41b5-bc10-2548217c284d`

**Approve this bounded verification contract, with the clarifications below. Codex may implement the verifier without another preliminary source/API packet. No gameplay, profile, fingerprint or save-format change is authorized.**

**Use an exact-bound standalone verifier for this first slice. Do not register a new package headless case or require another full-suite execution solely for this verification-only work.** INT-04’s direct prerequisite is the accepted selected INT-03 headless minimum; this work tests the existing connected behavior rather than expanding its authority.

## 1. Verification format and regression requirement

Run the verifier against the **existing accepted assemblies**, with their exact hashes and actual loaded identities recorded. Leave the engine sources, registered tests and **1,489-case inventory unchanged**.

The final packet should reference the accepted 1,489-case report and inventory as **prior execution evidence**. Report the new standalone scenario executions and assertions separately. Do not describe them as a new 1,490-case suite or imply that the prior regression was rerun.

A standalone PowerShell verifier, or a separate verification host using the public C# APIs, is acceptable. It may decode actual saves through `SnapshotCodec` for trusted observations, but must not replace internal state, inject receipts or use production manufacturing/healing helpers to calculate expected answers.

**If verification exposes a concrete engine discrepancy, stop treating that branch as passed.** Report the smallest reproducible mismatch for a scoped correction review. Any subsequent compiled engine or package-test change requires its own exact build and regression evidence. That contingency is not a reason to rerun the unchanged engine suite now.

## 2. The proposed rule expectations are supported

The pinned recipe-4 card specifies DC 8, four active hours, five standard units, the four component occurrences, finished mass of **0.2 lb including a 0.1 lb container**, and **2d4+2** ordinary magical nonspell healing. Its specific improvement option retains Standard quantity with every container at maximum/current structural HP 2; it does not increase potency.

The crafting procedure supplies the Exceptional margin of **5–9**, the **125% yield rounded down**, the post-check choice, and the first nontrivial successful recipe award of **4 trade XP once**. That award is not doubled by the recipe’s own XP field. Masterwork catalyst retention is a separate rule and does not apply to these Exceptional branches.

Approve these principal expectations:

| Boundary | Required expectation |
|---|---|
| **Admission** | Reserve the four component quantities and the two supplementary vials; book the worker; charge the same specimen into the apparatus. Do not equate reduced availability with physical consumption. No labor, check or output is earned merely by starting. |
| **Stabilization** | Earn the accepted **900 active seconds** and the actual stabilization event. Claims remain outstanding; no quality roll or finished dose yet. |
| **Completion check** | Earn another **13,500 active seconds**, totaling **14,400**. Resolve the actual check once and reach its genuine pending choice. |
| **Exceptional Full Yield** | `floor(5 × 125 / 100) = 6` doses. Consume the required components and **one** supplementary vial; release the unused extra. |
| **Exceptional Durability** | Five doses, with each container’s structural maximum/current HP **2**. Consume the same component inputs; release **both** supplementary vials. No increased healing or additional draw. |
| **Dose use** | Consume one actual dose through the current Action, hand, access and eligibility rules. Preserve its retained empty vial and the other doses. |
| **Continuation** | Keep formula, order, claims, XP, output and used-dose history through real encounter closure, paid travel and save/resume. |

The **900 + 13,500 split is the accepted selected procedure**, not a new universal phase rule for every four-hour recipe.

Three implementation details need explicit treatment:

**Four component claims are not necessarily four total reservation records.** Account separately for the supplementary-packaging reservation. Verify component and packaging quantities, their lot identities, terminal disposition and balance changes—not merely the number of claim objects.

**XP is a change from the actual prior state.** Establish the first-success and nontriviality prerequisites, then verify a single +4 award and persistent success history. Do not assume all earlier research or trade activity left every XP field zero.

**Durability applies to the container’s structural HP.** It does not change the drinker’s maximum HP, dose count, healing formula or effect duration.

## 3. Preserve a genuinely independent expected-value calculation

The proposed separation is sound: the accepted public input supplies actions; the selected fixture supplies starting facts; the pinned rules supply the expected relationships. Decoded engine records are the **observations to test**, not the source of their own expected answers.

### Bind fixture authority separately from the command file

The walkthrough identifies commands, actors and items, but does not itself establish every initialized attribute, credential, lot or facility property. Retain the exact selected factory/profile bindings alongside the input-file hash.

At the relevant checkpoint, assert the actual learned formula, qualified worker, physical tools, zero applicable extra modifiers, exact specimen identity and current access. A failed precondition must produce a named verification failure—not a substitute value, altered snapshot or skipped branch.

### Pin the RNG calculation precisely

Approve a small independent calculator for the required d20 and d4 checks, seeded from the **authentic saved pre-event RNG word**.

The evidence must identify the exact accepted `xorshift32-v1` transition and bounded-die mapping, including unsigned arithmetic and any rejection behavior. The algorithm name alone is not sufficient. Do not assume a convenient modulo formula, call the engine’s dice helper for the expected face, or select a replacement seed.

Check accepted faces, any rejected words, the final RNG word and the resulting total. This corroborates the selected event’s arithmetic; it does not claim an independent audit of every earlier random event.

### Check healing before the cap

This is particularly important in the proposed witness:

\[
\text{potential}=d4_1+d4_2+2,\qquad
\text{actual}=\min(\text{potential},26-23)=3
\]

**Final HP of 26 alone cannot distinguish the correct formula from an incorrectly stronger potion.** Independently verify the two faces, **pre-cap potential**, final RNG word, actual restoration, Action expenditure and dose transition.

The actual combat damage and 23/26 pre-use state are fixture preconditions reached through real play. Verify them; do not inject them. Likewise, establish the absence of applicable blockers or modifiers before applying this simple cap equation. The selected source classifies the effect as ordinary magical nonspell healing under actual caps and blockers.

## 4. Branches, retries and restored execution

Approve the three proposed executions:

**Full Yield uninterrupted**, **Full Yield with the actual quality/opportunity restores**, and **Durability from the genuine pending-quality save**.

The two Full Yield executions must agree at the matching r107, r115 and r165 checkpoints. That establishes persistence/replay equivalence alongside—not instead of—the independent rule assertions.

The Durability branch must satisfy its own quantities, container state, XP and dose-use expectations. **Do not require its final canonical bytes to equal Full Yield**, because its finite outputs legitimately differ.

Reusing subsequent command payloads is appropriate while those commands remain legal. Automatic defender decisions must still be obtained through the actual public driver. Do not repair a branch’s position, turn, stock or RNG to preserve a planned transcript.

For the exact retries, retain the original IDs, revisions and payloads and require `Duplicate` plus unchanged complete canonical state. For the fresh same-turn sibling dose, establish that it is otherwise eligible—actual unspent sibling, proper custody/access, reach and hand state—so the observed `Unavailable` result is meaningful in the already-paid-Action context. Require no receipt, no state/RNG change and an unchanged permitted view, followed by successful continuation through the next original command.

The session need not gain a private rejection-reason field for this test.

## 5. Retained evidence and acceptance groups

The verifier should fail closed on an unexpected response, missing checkpoint, unexecuted branch or failed precondition. An exception converted into a generic response must not accidentally count as the intended negative result.

Retain the following five evidence groups:

| Group | Required retained evidence |
|---|---|
| **1. Authority and independent expectations** | Exact rule/source pins and relevant occurrences; selected fixture and input bindings; a readable expectation table identifying which values come from rules, fixture facts or independent arithmetic. Include the recipe-4 source excerpt and exact RNG technical binding. |
| **2. Actual execution and conservation** | Public inputs/responses, relevant permitted views, checkpoint revisions/clocks, raw claim/lot/order/booking facts, independent expected values, observed values and named assertion results for both quality choices. |
| **3. Use, retry and rejection** | Pre-use eligibility and RNG, independently calculated faces/potential, actual healing and Action transition, retained vial identity, sibling conservation, exact duplicates and the otherwise-legal fresh rejection. |
| **4. Persistence and verifier sensitivity** | Branch-distinct saves and hashes, uninterrupted/restored Full Yield equality, and checks demonstrating that deliberately incorrect **observation records supplied to the verifier** fail named invariants. Do not inject those altered records into the simulation. |
| **5. Exact execution provenance** | Verifier revision/hash, accepted engine source/archive identity, actual loaded assembly digests/module identities, run/environment information, complete branch results and bindings to the unchanged accepted 1,489-case inventory/report. |

For sensitivity checks, a few targeted corruptions are sufficient: wrong yield, consumed-versus-reserved quantity, doubled XP, incorrect healing addend, or a missing paid Action/retained vial. These demonstrate that the assertions can fail; report them as **verifier self-checks**, not additional successful gameplay scenarios.

Keep saved-state inspection inside this trusted verification process. It does not authorize exposing hidden records through the Player view.

No new performance target is imposed on this semantic verification slice. Existing P1 findings and measurement qualifications remain unchanged.

## Inspection limits and final ruling

I inspected the proposed contract, the pinned public recipe-4 card, relevant crafting quality/material/XP rules, healing procedure and the previously approved connected-batch boundaries. The V4 file’s blob identity was available, but its full JSON content was not returned by the attempted file read; I am not claiming an independent extraction of `/recipes/3`. Retain that exact occurrence with the implemented oracle evidence.

I did not execute a verifier, compile, run tests, load assemblies or saves, recompute hashes, or modify repository files. This is approval of the verification contract, not acceptance of results that do not yet exist.

**Final ruling: approve `9d0e791836eef7ee89c123d24e18ed380ba1f7cf` as the bounded INT-04 recipe-4 verification contract. Implement it as an exact-bound standalone verifier against the unchanged accepted engine. No new registered case or redundant full-suite run is required for this verification-only slice.**

Return the actual standalone execution and evidence for acceptance. The selected INT-03 minimum and prior module acceptances remain closed; broader INT-04, P1, production authority and Unity gameplay integration are not promoted by this ruling.
