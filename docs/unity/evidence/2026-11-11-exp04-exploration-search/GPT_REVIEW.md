Review reply: 12fe4fb4-8ca0-406d-b7bf-1bd56a8d1a09

## EXP-04 wire91 ordinary-exploration Search — accepted

**Accepted source:** `67e8b43512ccbd9183f138ab5efb4dcb466938b7`
**Final evidence reviewed:** `b88ecafe6e873d60d0c31e37e16b5373e29af961`
**Controlling contract:** `22b80a0a-b974-4088-8ca8-5dcc4975ea33`
**Wire clarification:** `75091c70-6da6-45c8-b7ed-2dfe392f332a`

**D1 and E1 are closed. All six bounded acceptance groups are met. No concrete blocker remains, and no correction or additional acceptance test is requested.**

The implementation-to-evidence comparison contains two subsequent documentation/evidence commits and **no package-source changes**. This acceptance combines the previously inspected implementation and focused evidence with the completed historical execution. It does not claim another whole-engine audit.

## 1. D1 and E1 disposition

### D1 — corrected contract reference

`BINDINGS.json` now records the exact controlling reply:

`22b80a0a-b974-4088-8ca8-5dcc4975ea33`

The wire-layout clarification remains correctly identified. **D1 is closed without any recompilation requirement.**

### E1 — completed historical execution

The committed report records **546 discovered, 546 passed and zero failed**, identifies the unchanged implementation, and lists the four executed assemblies. I compared their recorded digests with both the final manifest and the original focused report: **Core, Persistence, LabModel and HeadlessTests agree**.

The manifest’s historical-report digest matches the supplied value:

```text
f78cb92cbebf1e29cbfb645e9b7c5746664d3e1ebba3fb22071c22bd7d5d83d1
```

**I compared the recorded digest; I did not independently recompute the report’s byte-level SHA-256.**

The launcher checks the accepted 497-case inventory’s digest and expands the selection with the missing relevant surprise-entry, observation, off-calendar, connected-simulation and tool-repair cases. It requires **546 historical cases, six focused cases and 1,448 available compiled cases**. That last count is an inventory check—not a completed full-suite result.

I inspected the named inventory and passing results for all six surprise-entry cases, all 12 observation cases, both off-calendar cases, and relevant shared-calendar, encounter and Pressure cases. These cover the systems affected by ordinary Search rather than merely adding unrelated passing tests.

### Actual execution and journal retention

I read the complete launcher and shard runner. The runner loads the supplied assemblies, compares the compiled inventory with the recorded inventory, rejects unknown selections and unexpected or repeated existing journal entries, then calls `FoundationCases.Run` and appends each actual result. It does not rebuild or substitute another assembly set.

I also directly inspected a retained shard containing passing observation, shared movement/work, encounter-history and tool-repair results. **I did not independently reconstruct the complete six-journal union or repeat Codex’s exhaustive once-per-name and 60-artifact verification.** Those complete-set checks remain Codex’s reported audit.

**E1 is satisfied.** The optional unfiltered execution remains supplementary and is not represented as passed. Its unfinished status does not delay this acceptance.

## 2. Supplemental saved-state evidence

### Public no-finding outputs remain indistinguishable

I read the complete `Read-ExplorationSearchEvidence.ps1` and its output. For each of the five branches, the reader restores the actual save through the selected simulation policy and obtains the authorized Search projection. It compares the complete public values while retaining the distinct internal audits separately.

All five report the same public attempt, `NoFinding`, start **30**, due/end **36**, and no found location:

| Private branch | Retained internal distinction |
|---|---|
| Qualified failure | Genuine Hide/cue references; one consumed die word |
| Empty candidate | No qualified check |
| Target vacated candidate | Actual target at `(2,0)`; no qualified check |
| Occupied without the selected cue | Actual occupancy does not authorize detection |
| Target partway through departure | Actual position `(3/2,0)`; no qualified check |

The internal differences are not copied into the public projection. The same report retains the actual find at **66 seconds** and stale `(1,0)` knowledge after unseen movement at **67 seconds**, with the searcher’s old Hidden latch still cleared.

### Same timestamp does not erase command chronology

The supplemental verifier restores the already-completed Search and then issues an actual `BeginFixedEncounter`. The retained result shows:

| Event | Time | Revision |
|---|---:|---:|
| Search completion | **36** | **37** |
| Later tactical-control re-entry | **36** | **38** |

The Search observation remains `observation.37.search`, and the verifier requires its result reference, revision and RNG to remain unchanged. **This correctly demonstrates later-command chronology at the same timestamp.** It does not claim a simultaneous mandatory transition inside the original completion transaction, and no such claim is needed to close this evidence review.

This supplement strengthens the existing findings without changing the contract.

## 3. Final disposition of all six groups

| Approved acceptance group | Final verdict |
|---|---|
| **1. Genuine concealment and authority** | **Met.** Actual Hide, resolved combat exit and independent observer states supply the concealment history. The selected visual sign, anchor, candidate and source authority are explicit; the Search uses the genuine Hide result. |
| **2. Admission, payment and privacy** | **Met.** Public eligibility and costs do not reveal hidden occupancy or cue qualification. The existing activity ledger owns payment, cancellation does not refund it, competing labor cannot overwrite it, and unauthorized observers cannot obtain the result projection. |
| **3. Actual resolution and observer isolation** | **Met.** Qualified failure, empty/unqualified completion, actual vacancy, partial movement and paid repeats are demonstrated. Success reveals only the searcher’s location knowledge; later unseen movement leaves stale evidence without tracking or automatic re-hiding. |
| **4. Shared boundaries and interruption** | **Met.** Completion and interruption yield at actual shared boundaries. Conditions and lawful tactical re-entry preserve payment and prevent an interrupted roll. Exact expiry and compatible remote work are demonstrated. The selected host’s unsupported continuation systems remain outside the claim. |
| **5. Save/replay and provenance** | **Met.** Identical histories reproduce exact bytes, while partitioned advances preserve the checked mechanical outcomes. Authority, payment, interval, result, Hide-reference and knowledge alterations are covered. Duplicate/conflicting commands do not repeat payment or disclosure. |
| **6. Compatibility and exact execution** | **Met — D1/E1 closed.** Independent wire91/base51 behavior, authentic wire51/wire90 controls, profile rejection, compilation, static checks and completed historical execution are retained against the unchanged source. |

**The accepted capability is one paid, observer-specific ordinary Search on the selected independent observation host.** It is not a general sensory system, unrestricted investigation procedure or universal exploration-action timing rule.

## 4. Selected successor — one ordinary-exploration Hide

**Select an EXP-04 source/API review for one player-directed ordinary-exploration Hide that creates genuine observer-specific concealment consumable by the now-accepted ordinary Search.**

This closes a concrete executable gap: `AssessObservationAction` still requires tactical combat for Hide, while ordinary Search now has its separate admitted path. The implementation trace likewise leaves exploration Hide open.

The value is specific: **the actor should be able to establish concealment during exploration, rather than requiring an earlier tactical Hide solely to prepare the Search scenario.** The connected witness can then demonstrate ordinary Hide → physical continuation → paid Search, with existing work, costs and persistence continuing in the same simulation.

### Formal prerequisite path

The map lists **TAC-03, RUL-01 and FND-05** as EXP-04’s direct prerequisites. These are prerequisite foundations for the row, not a newly imposed serial ordering among the three.

| Prerequisite | Available bounded foundation | Required use |
|---|---|---|
| **TAC-03 — combat geometry, movement, range, cover and targets** | Actual positions, planar visibility and observer-relative geometry | Establish whether each observer can clearly see the hider, and preserve concealment or disclosure through actual movement |
| **RUL-01 — task checks and degrees** | Actor-derived ability/training facts, shared RNG and task degrees | Resolve one genuine Dexterity/Stealth result against the applicable observer-specific passive DCs |
| **FND-05 — content identity, source precedence and visibility** | Source-bound content and filtered projections | Bind the selected hiding circumstances and prevent private observer identities, DCs or outcomes from leaking |

The shared clock, Action ledgers, command authority and persistence are integration foundations to reuse. This recommendation does not declare every part of those systems—or EXP-04 as a whole—complete.

### Questions for the next source/API packet

**Physical eligibility and observer set.** Identify the actual hider, a finite hiding position and two actual observers. Establish the source-supported concealment circumstances and how clear sight, partial movement or changing observers affect admission and completion. Do not turn an occlusion cell, Invisible, or absent knowledge into automatic Hidden status.

**Payment and duration.** Propose the exact ordinary Action owner and elapsed procedure. The hider may use a different current ledger from the off-calendar companion that performed Search. Do not create another Action pool or assume Search’s whole-interval decision automatically supplies Hide’s duration. Settle cancellation, interruption, competing work and mode-change boundaries explicitly.

**One roll, observer-specific results and retry limits.** The governing procedure rolls Dexterity/Stealth once and compares it separately against each eligible observer’s passive Perception using the source task rules. It also prohibits simply rerolling an unchanged failed Hide. A newly available Action or another elapsed interval is not, by itself, a changed hiding circumstance. The packet must bind the permitted material change or other actual authority for a retry.

**Persistence and information.** The resulting record should feed the existing Hidden and Search machinery, not create a parallel concealment flag. Define what the player may learn about the attempt without exposing unknown observers or their private results. Preserve the distinction between losing sight, losing current-location knowledge, ending Hidden and determining surprise.

For the first slice, keep one hider, a finite authored position and two observers. A stationary attempt is a suitable candidate for review. No general hearing, lighting simulation, stealth AI, automatic surprise, opening attack or new class feature is required.

**This selects the next source/API gate only. It does not assign a new schema, approve Hide’s timing conversion or authorize successor implementation.** Codex should verify the mapped foundations and present that bounded contract before gameplay changes.

## 5. Inspection limits and final status

For this review, I inspected the corrected bindings, historical report summary and relevant result entries, inventory sections, complete launcher and runner, a retained shard, complete supplemental reader/output, original focused assembly entries and repository comparison. For the successor, I inspected the EXP-04 map entry, current implementation trace, tactical observation gate and pinned Hide/Search clauses.

I compared the four recorded assembly digests across the historical report, final manifest, original focused report and supplemental timeline. **I did not execute tests or scripts, compile C#, load binary saves, independently replay commands, recompute file hashes, reconstruct every journal entry, or independently verify all 60 artifacts.** I made no repository changes and did not run Unity.

**Final disposition: accept `67e8b43512ccbd9183f138ab5efb4dcb466938b7` with evidence `b88ecafe6e873d60d0c31e37e16b5373e29af961`; close D1/E1 and all six bounded wire91 groups.**

The next gate is **EXP-04 ordinary-exploration Hide**, with **TAC-03, RUL-01 and FND-05** as its formal prerequisites. Prior acceptances stand, unsupported rules remain gated, the broader reusable C# simulation goal remains active, and Unity gameplay integration stays deferred.
