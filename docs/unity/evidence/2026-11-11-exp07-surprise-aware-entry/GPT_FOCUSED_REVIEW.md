Review reply: 9522ec88-f720-4e0d-9cae-51455696bb6d

## EXP-07 schema90 surprise-aware entry — focused review supported; final acceptance held for historical evidence

**Source reviewed:** `216217d0dfa1781ea1b3ab41c3ba1d4a5e089ec7`
**Focused evidence reviewed:** `983c5d86859cfcaa42c3c2b0ecd308b10a0afab8`
**Controlling contract:** `e5fe03c7-546d-43c1-babf-66c42a005584`

**The inspected source and focused evidence satisfy groups 1–5 within the approved scope. I found no concrete runtime or provenance defect and request no source correction. Group 6 remains pending solely for E1: the completed, exact-bound historical regression.**

The implementation-to-evidence comparison shows one documentation/artifact commit and **no subsequent package-source changes**. No successor is selected or authorized by this review.

## 1. Disposition of the six groups

| Approved group | Current assessment |
|---|---|
| **1. Authored awareness and actual entry** | **Met.** Distinct preselected Director bindings identify the actual hero, defender and awareness basis. Application occurs only at successful genuine entry, before initiative. The warned control has identical physical timing and initiative inputs. Actual failed arrival preserves movement without applying surprise or consuming initiative. |
| **2. Initial Reaction and exact lifetime** | **Met.** Real departure offers the warned hero a Reaction but produces no offer for the surprised hero. The first regular Start refreshes the ordinary resource behind the restriction. Actual first End releases that restriction, and a new departure produces a paid Reaction attack. Rejected and duplicate Ends preserve state. |
| **3. First-turn permissions and costs** | **Met.** Shared and tactical projections deny otherwise-available movement, Action and Bonus Action. Actual Club and movement requests reject unchanged. Stance and first free handling remain legal; the Action-cost second handling rejects. A later regular turn supports a real paid attack. |
| **4. Passive timing and independent restrictions** | **Met.** The restricted slot consumes its actual elapsed time. An existing absolute condition expires at its own deadline, and real companion labor advances once. Clearing surprise does not remove the independent Focused prohibition. |
| **5. Persistence and integrity** | **Met.** Partial approach, entry, first Start, restricted turn, first End and subsequent combat/ordinary continuation replay exactly. Constructor and saved-state controls cover authority, participant/threat, entry, first Start, early End and false expenditure. |
| **6. Compatibility and exact execution** | **Partially met — E1 pending.** Focused execution, compilation, static checks, profile rejection and authentic schema89 controls are retained. The required 497-case historical execution has no completed report in this pinned packet. |

I read **all six focused test bodies and their helpers**, including their substantive assertions—not merely the six-pass summary.

## 2. Source authority and genuine entry

The implementation follows the approved distinction between **an authored Director determination** and automatic sensory inference. `SurpriseAwarenessBinding` requires the pinned source revision, specific Director authority, exact encounter/participant/threat identities and the evidence identifier corresponding to the selected outcome. The profile is selected before initialization and receives a distinct fingerprint. It creates no generic command for imposing surprise later.

`BeginLaterEncounter` applies the decision only after actual arrival passes the existing engagement assessment, then performs the existing initiative rolls. The decision is bound to that arrival command, revision and epoch origin. The assessment also checks for contradictory represented threat evidence before applying the selected surprise basis.

The focused trace confirms:

| Branch | Arrival | Initiative | RNG after boundary |
|---|---:|---|---:|
| Surprised hero | `23159/2` | Hero 9 / defender 12 | `502002592` |
| Explicitly warned hero | `23159/2` | Hero 9 / defender 12 | `502002592` |
| Actual mid-edge loss of defender sight | `23159/2` | No initiative | `3247499250` |

The failed branch retains the paid five-foot arrival and records `LaterEncounterAwarenessUnavailable`, with neither a surprise decision nor a later-encounter entry.

**Evidence qualification:** the prior-threat-versus-direct-sight comparison is a detached query test using altered observer records. It demonstrates the real assessment predicate; it is not presented as a command-created prior warning history. The Blinded-defender interruption is the separate actual-command negative control.

## 3. Reaction lifetime, permissions and first-End ordering

### Resource availability and permission remain separate

The governing combat source preserves regular processing during surprise, denies Reaction until the first regular turn ends, and explicitly permits an otherwise legal simple free interaction. Surprise is not Incapacitated or Unconscious.

The implementation maintains those distinctions:

- Genuine entry derives the surprised hero’s initial Reaction availability through the restricted permission projection.
- `RecordSurpriseFirstStart` performs the ordinary refresh and records the actual first marker.
- `SurprisePermissions.Restrict` continues to deny Reaction while the recorded restriction is pending.
- Completion changes the lifecycle record; it does **not** replenish or replace the interval’s resource.

The ordinary opportunity predicate checks both the actual Reaction resource and `CurrentPermissions`. Thus the restriction prevents creating a usable offer rather than manufacturing a declined attack afterward.

### The demonstrated lifetime uses actual events

| Event | Retained observation |
|---|---|
| First real leave-reach event | Warned hero receives `move.95`; surprised branch completes movement without an offer |
| Hero’s first regular Start | `23165/2`, ordinal **1**; ordinary resource refreshed but permission denied |
| Actual first End | `23171/2`, `tactical.command.99`; restriction ends |
| New post-End trigger | `move.101` |
| Actual Reaction payment | `attack.102` spends the existing ordinary Reaction |

These are distinct events. No missed pre-Start opportunity is banked for later use.

`CompleteSurpriseFirstEnd` checks the actual first-turn identity and scheduled endpoint, waits for pending advancement/choices to finish, and accepts only the relevant End or supported continuation. The shared resolver calls it after the existing successful-resolution and reconciliation paths. Structural validation independently checks the recorded End receipt, actor, target turn and completion boundary.

The focused rejected-End witness is specifically **`StanceRequired`**, followed by exact duplicate and command-ID conflict controls. I am not describing it as an executed pending-manufacturing continuation test; that continuation handling was inspected in source.

### Actual handling distinguishes free interaction from an Action

The first-turn case establishes that the same step and Club attack are available in the warned control but rejected in the surprised branch. It then performs the real pack-skin drop in both branches.

For the surprised hero, the drop changes actual placement and spends one interaction, with no Action, elapsed time or RNG change. Pickup as the second interaction rejects unchanged; the warned control actually pays its Action for that pickup. A subsequent genuine hero turn admits and pays the Club attack.

The Bonus Action check is correctly limited to the shared permission projection. It verifies denial while retaining the underlying resource and without creating a character-feature grant. It is **not** a claimed execution of a nonexistent Bonus Action ability.

## 4. Passive timing and historical integrity

The independent-work branch begins the restricted hero slot at `23177/2`, with **`9/2` seconds** of real companion crop progress. The existing condition expires at `23179/2`; actual End occurs at `23183/2`, with crop progress **`15/2`**.

Afterward, the hero’s ordinary Reaction resource remains available, but its independently selected Focused stance prevents an actual new leave-reach offer. This demonstrates that ending surprise removes only its own restriction. The restored branch reproduces the same bytes.

The integrity case isolates five saved-state changes:

| Alteration | Required rejection exercised |
|---|---|
| Swapped participant and threat | Genuine encounter/threat binding |
| False arrival command | Surprise-entry provenance |
| Wrong first-Start ordinal | First regular Start validation |
| Fabricated early End | First-End completion validation |
| False Action expenditure | **`InvalidSharedWorldReplay`** |

The record constructors separately reject an invalid Director identifier or mismatched evidence/outcome, and profile controls reject a different selected awareness branch, an older profile or Release execution.

The test helper starts from a fresh capture for each mutation and requires the identified error. The expenditure case specifically requires historical replay rejection rather than accepting an arbitrary structural exception.

The codec stores the authority and lifecycle evidence, while the existing interval remains the resource authority. The new payload is appended only for schema90 after the inherited re-engagement payload.

**No additional integrity addendum or gameplay correction is requested on the inspected evidence.**

## 5. Compatibility and retained execution

The compatibility verifier does more than compare selected response fields. It reruns the original aware baseline, removes only the expected assembly metadata from both reports, and compares the complete remaining serialized reports. It also checks the authentic active, closed and continued schema89 files against their predecessor bindings, restores each under its original policy and requires byte-identical re-encoding with no surprise record.

The retained result reports all those checks passing, including the original aware final-save digest:

`d478ba6c1856eff78060a8fc02435a5721f81c353e1a16bd63742d28aaba1b61`

I inspected the verifier and result; **I did not rerun them or independently open the binary saves**.

| Retained evidence | Result inspected |
|---|---|
| Focused report | **6 discovered, 6 passed, zero failed** |
| Standalone compilation | **Core, Persistence and LabModel PASS**, C# 9 |
| Runtime without Laboratory defines | **Core/Persistence PASS**, warnings treated as errors |
| Static package validation | **18/18 passed; 365 assets and 365 unique GUIDs** |
| Authentic schema89 compatibility | Complete aware-trace comparison and three authentic save restorations passed |
| Historical / optional unfiltered | **Pending in this pinned packet** |

These are **Codex’s retained executions that I reviewed**, not executions I performed. Runtime compilation without Laboratory defines is not production approval; static validation explicitly excludes Unity import, compilation and release-build validation.

I compared the four recorded assembly digests across the bindings, focused report and compatibility report; they agree. The manifest’s focused-report digest matches the supplied `5c2b39ff…ade7d1`. **I did not independently recompute that digest or repeat the complete 339/250/140/719 source and package comparisons.** Those complete-set checks remain Codex’s reported audit.

## 6. E1 and inspection limits

**E1 is the completed relevant historical regression against this exact implementation and assembly set.** The stated 497-case historical run and optional 1,442-case full run are not represented as passed.

A completed exact unfiltered result containing the required historical cases may satisfy E1; a redundant second execution is not required. No new source/API ruling or added gameplay test is requested by this evidence hold.

For this review, I inspected the complete new policy, records, validator and codec; all six focused cases/helpers; relevant genuine-entry, permission, opportunity, first-End, query and serialization paths; the three traces; compatibility verifier/results; focused results; compilation summaries; all 18 static checks; bindings; and repository comparisons. I also checked the pinned combat surprise and timing clauses.

For existing files, that means the relevant paths and changes—not a fresh whole-engine audit. I did not freshly extract the V6 DOCX or reread the pending historical test inventory.

**I did not compile or execute C#, run scripts, load binary saves or assemblies, independently replay gameplay, recompute artifact hashes, modify repository files or run Unity.**

### Final disposition

**Hold final acceptance of `216217d0dfa1781ea1b3ab41c3ba1d4a5e089ec7` solely for E1, the completed exact historical regression evidence.**

**Groups 1–5 are supported by the inspected implementation and focused evidence. No concrete source correction is currently requested.** Group 6 remains incomplete until the immutable regression addendum is reviewed.

Earlier acceptances stand. No successor is selected, the broader reusable C# simulation remains active, and Unity gameplay integration stays deferred.
