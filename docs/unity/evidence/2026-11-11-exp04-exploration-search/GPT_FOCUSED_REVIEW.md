Review reply: 267120d3-d19a-41ad-aa07-edada1ee2626

## EXP-04 wire91 ordinary-exploration Search — focused review supported; final acceptance held for historical evidence

**Source reviewed:** `67e8b43512ccbd9183f138ab5efb4dcb466938b7`
**Focused evidence reviewed:** `e7c5b03a3f14b8bc5c0b1c18fb90a519dd833a63`
**Controlling contract:** `22b80a0a-b974-4088-8ca8-5dcc4975ea33`
**Wire clarification:** `75091c70-6da6-45c8-b7ed-2dfe392f332a`

**Groups 1–5 are met on the inspected source and focused evidence. I found no concrete runtime or provenance blocker and request no gameplay correction. Group 6 remains pending for E1: the completed, exact-bound historical regression.**

There is **one nonblocking manifest typo to correct**, identified below. It does not require recompilation or another gameplay run.

The source-to-evidence comparison contains one documentation/artifact commit and **no subsequent package-source changes**. No successor is selected or authorized.

## 1. Disposition of the six groups

| Approved group | Current assessment |
|---|---|
| **1. Genuine concealment and authority** | **Met.** The case executes actual Hide and combat exit, retains independent concealment against two living observers, and binds the selected visual sign, searcher anchor, occluded candidate and existing Hide result. Declaration uses the genuine ordinary interval and payment receipt. |
| **2. Admission, payment and privacy** | **Met.** Public queries and discovery do not depend on hidden occupancy or cue qualification. Payment uses the existing activity ledger, survives cancellation and cannot be overwritten by competing labor. Unauthorized result access is denied, and all public no-finding properties are compared across distinct private outcomes. |
| **3. Actual resolution and observer isolation** | **Met.** Qualified failure, empty/unqualified completion, actual vacancy, partial target movement and separately paid repeats are exercised. The eventual success updates only the searcher’s knowledge. Later unseen movement preserves stale evidence without restoring the old Hidden latch or tracking the target. |
| **4. Shared boundaries and interruption** | **Met within the selected host.** Long advances stop at the actual Search endpoint. Actual Blinded dispatch and lawful fixed-calendar re-entry interrupt without a roll or refund. Exact Poisoned expiry precedes the check, and independent repair receives elapsed work once. |
| **5. Save/replay and provenance** | **Met.** Identical histories replay byte-identically; different clock partitions preserve the checked mechanical outcome and knowledge. Isolated payment, interval, completion, Hide-reference and knowledge mutations reject. Authority construction, duplicate commands and conflicting IDs are covered. |
| **6. Compatibility and exact execution** | **Partially met — E1 pending.** Independent wire91/base51 behavior, legacy commitment rejection, authentic wire51/wire90 controls, profile rejection, focused execution, compilation and static checks are retained. The required historical execution is not yet a completed result in this packet. |

I read **all six focused case bodies and their helpers**, including their assertions—not merely the pass counts.

## 2. Sensory authority and public information

### The visual sign does not become sight through the blocker

Initialization checks that the anchor, candidate and sign are valid positions; the nominated occlusion cell blocks sight; the fringe is geometrically visible from the anchor; and the creature’s candidate position is not directly visible along that channel.

At completion, `QualifyingSearchHide` checks the actual resolved target position, observer-relative Hidden state and available sign. It obtains the existing Hide record through `ActiveSearchHide`. The new path then calls the shared `RecordSearchResult`, which is also used by tactical Search. **There is no second Search calculator or fabricated Stealth DC.**

The retained authority trace records the genuine Hide at **1 second**, total **18**, followed by declaration at **30 seconds**, interval **5**, paid by `test.search.36` at revision **36**.

### No-finding filtering is substantive

`AssessExplorationSearch` uses public actor eligibility, activity timing, candidate bounds and reach. It does not call the private target/cue qualification procedure. Discovery enumerates candidate cells rather than discovering an eligible hidden actor first.

The focused test compares all public properties of `ExplorationSearchView` across:

- A qualified failed check.
- An empty candidate.
- A genuinely vacated candidate.
- An occupied cell without the selected cue.
- A target partway through an unseen departure.

All yield at **36 seconds** with the same public no-finding shape. Internally, the qualified failure retains its real roll and Hide/cue references; the unqualified cases retain zero consumed words. **No dummy rolls are added to conceal the distinction.**

`ObserveExplorationSearch` requires control of the searcher and returns the filtered view. That view omits target identity, cue, Hide reference, die, DC, RNG and interruption diagnostics. The raw snapshot remains explicitly documented as a trusted simulation/persistence interface; this review does not declare arbitrary raw-snapshot exposure safe for players.

### Success does not create ongoing tracking

The six separately paid rolls are **6, 14, 7, 11, 13 and 19**. The success at **66 seconds** discloses `(1,0)` to the companion, clears only its Hidden latch and preserves the other observer’s knowledge.

Actual unseen movement reaches `(2,0)` at **67 seconds**. The searcher retains stale Search evidence at `(1,0)`, with `CurrentLocationKnown=false`, the original evidence time and no restored Hidden latch. The witness remains uninformed.

## 3. Payment, scheduling and interruption

### The ordinary Action is paid once

`BeginExplorationSearch` records the actual interval, candidate and declaration receipt, then calls `PaySearch` on the existing off-calendar ledger. Declaration consumes neither elapsed time nor RNG.

The implementation also closes the specific overwrite hazard identified in the contract: `CommitActiveLabor` rejects an existing Search commitment, and the command-level conflict checks prevent starting incompatible work while that Action remains spent. Cancellation releases the pending stationary claim but does not replace the paid ledger entry. The test permits a subsequent ordinary walk while still rejecting work and another Search until the genuine interval refresh.

### Completion uses the old payment, not a newly refreshed Action

The dispatcher includes the pending Search deadline among its actual boundaries. At that endpoint it defers the searcher’s activity refresh, processes the existing shared consequences, resolves or interrupts Search, and then refreshes the ordinary interval.

The result path reports the actual reached time from the terminal Search record. An enclosing advance to a later requested time does not silently continue beyond the result. Identical retries preserve the state and do not repeat the check.

The partition test appropriately distinguishes two claims: identical command histories must produce identical bytes, while differently partitioned advances compare the actual completion time, roll, outcome, RNG endpoint and knowledge—not equal receipt revisions.

### The off-roster mode-change case is handled explicitly

The mode-change witness enters the existing fixed-calendar tactical control at **33 seconds**. It retains the same encounter and dead resolved opponent, rather than spawning or reviving anything. The companion is still off roster, but the general Search reconciliation sees tactical control and interrupts its pending ordinary Search.

Payment remains, no observation result or roll is created, and later tactical exit does not resume the attempt. The rejected re-entry branch preserves the pending state unchanged.

The separate condition/work branch establishes actual Blinded interruption at **33**, and a normal completion at **36** after Poisoned expires. The independent witness receives **four seconds of real repair labor** through the same advance.

**Inspection qualification:** I inspected the continuation-priority guards in source. I am not claiming an executed manufacturing-choice-at-completion case; this selected observation host does not provide that procedure. No such expansion is requested.

## 4. Independent wire91 layout and integrity

The codec implements the clarified distinction:

**Wire version 91 → schema51 base-feature payload → required private Search extension → one final envelope checksum.**

`WireSchemaVersion` is derived from the required selected component, while `SchemaVersion` remains 51. Snapshot copying retains the immutable Search record. Decoding wire91 explicitly chooses the schema51 base layout before reading the extension; it does not activate unrelated higher-numbered systems.

Validation requires the Search fingerprint and component to agree, requires TEST_ONLY/schema51 authority, and rejects inappropriate later-context records. The ordinary commitment validator also rejects the new Search commitment without the selected wire91 profile. The focused legacy test specifically substitutes that commitment into the original envelope and requires encoding to fail.

The new codec does not serialize another position, resource budget or knowledge pool. The attempt records own declaration and terminal provenance; the existing observation result owns the roll; the existing observer record owns location knowledge.

### Isolated integrity controls

| Alteration | Rejection exercised |
|---|---|
| Removal of the paid activity commitment | Lost paid Action before authorized refresh |
| Changed due time | Declaration/interval provenance |
| Substituted observation-result reference | Completion/result binding |
| Fabricated Hide reference | Genuine cue and observer-specific Hide provenance |
| False successful knowledge after a failed Search | **`InvalidSharedWorldReplay`** |
| Invalid Director identifier | Authority construction |

The replay case also checks a duplicate finishing advance without repeated roll or disclosure. Constructor rejection, structural validation and historical replay are distinct evidence layers; I am not describing them as equivalent tests.

**No additional runtime or integrity correction is requested.**

## 5. Evidence correction and remaining acceptance item

### D1 — nonblocking manifest reply-ID typo

`BINDINGS.json` currently records:

```text
approvedSourceApiReply:
22b80a0a-b974-4088-8ca8-5dcc5465ea33
```

It should be:

```text
22b80a0a-b974-4088-8ca8-5dcc4975ea33
```

The README and retained approved-contract text identify the correct ruling. **Correct this field in the historical/final evidence addendum.** It is a documentation repair, not an ambiguity in the reviewed contract, and does not require recompilation or rerunning gameplay.

### E1 — completed exact historical execution

The pinned packet explicitly leaves historical and unfiltered results pending. **The 546 historical and 1,448 unfiltered figures are not passing results in this review.**

Final acceptance requires the completed relevant historical report on this implementation and its executed assemblies, including the affected observation, activity, scheduler and predecessor compatibility coverage.

A completed exact unfiltered report containing those required cases may satisfy E1; a redundant second execution is not required. The optional full run’s unfinished status is not an additional independent hold. This is missing evidence, not a reported regression failure.

## 6. Retained execution and inspection limits

| Evidence inspected | Recorded result |
|---|---|
| Focused cases | **6 discovered, 6 passed, zero failed** |
| Standalone compilation | **Core, Persistence and LabModel PASS**, C# 9 |
| Runtime without Laboratory defines | **Core/Persistence PASS**, warnings treated as errors |
| Static package validation | **18/18 passed; 370 assets and 370 unique GUIDs** |
| Authentic compatibility | Wire51 and wire90 saves restore/re-encode unchanged; the original complete wire51 baseline reproduces |
| Historical / optional unfiltered | **Pending** |

These are **Codex’s retained executions that I inspected**, not executions I performed. Static checks do not establish Unity import or build success, and no-Laboratory compilation does not confer production gameplay authority.

I read the complete compatibility verifier. It compares the entire original wire51 baseline after excluding only assembly metadata, then restores the authentic historical wire51 and wire90 files under their selected policies and checks their original hashes on re-encoding. The retained result reports those checks passing. I did not independently load those files.

I compared all four assembly digests across the manifest, focused report and compatibility report; they agree. I also compared `ExplorationSearchRecords.cs` and `ExplorationSearchValidation.cs` hash entries across the manifest, focused and standalone reports; those agree. **I did not independently hash the files or repeat the complete 344/254/143/729 source/package audit.**

For source inspection, I read the complete new policy, records, validator/filtered view and codec, all six focused cases/helpers, and the relevant changed command/query, activity-payment, shared-advance, result, copy and serialization paths. I also inspected the three traces, compatibility verifier/results, report summaries, all 18 static checks and repository comparison.

**I did not execute C#, compile, run scripts, decode the 18 binary checkpoints, independently replay gameplay, recompute artifact hashes, modify repository files or run Unity.** This was not a fresh whole-engine audit or a fresh extraction of the V6 DOCX.

### Final disposition

**Hold final acceptance of `67e8b43512ccbd9183f138ab5efb4dcb466938b7` for E1, the completed exact historical regression. Groups 1–5 are supported; no gameplay correction is currently requested.**

Correct D1’s manifest reference in the evidence addendum. No successor is selected. Earlier acceptances stand, the broader reusable C# simulation remains active, and Unity gameplay integration remains deferred.
