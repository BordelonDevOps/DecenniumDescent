# Owning-checkpoint pure comparison contract

Actual GPT response `85928cb9-1fa3-5c6e-a904-0efc862bf2bd` and Codex concurrence agree on this architectural direction. The complete operation/field/evidence contract and runtime implementation remain unapproved. The exact response is retained in GPT_ARCHITECTURE_REVIEW_02.json. This supersedes the earlier unresolved choice of architectural approach in PURE_ASSESSMENT_AUDIT.md; transitive purity and concrete type/access review still remain required.

## Agreed authority and observation boundary

The actual owning Simulation invokes an optional checkpoint assessment capability after current command/authority/receipt preflight and within the one coherent observation. The private checkpoint verifies the actual origin object, selected policy identity, current revision, wire/profile identity, passage terms and complete canonical bytes of the actual current snapshot. A fresh detached copy of current owned state is the input; `VerifiedSimulationOrigin.Capture()` is the validated origin and cannot replace a later current state.

Identical bytes in another Simulation do not transfer ownership. Only existing construction and successful verified transitions establish/advance the private PlanningPassage. Reads cannot create, repair, extend or expose it. A valid proof of no qualifying crossing preserves the native passage-evidence denial. A missing/mismatched checkpoint is a verification-capability failure, not a claim that a gameplay crossing did not occur. No read falls back to Initial, ReplayReceipt, canonical reconstruction, a resolver or a new historical ledger.

Preserve the original cutoff: crossing completion after the episode's relevant SourceRevision does not satisfy that planning basis. Current position alone is insufficient. Every new description/discovery/assessment path reaching planning admission uses this capability; fixing only direct AssessCommandV1 would leave an inadmissible hidden replay path.

## One writer with unchanged public validation

Extract one private canonical writer from the existing SnapshotCodec.Encode body. Public Encode continues Validation.Snapshot and then invokes that writer. Public Decode/save, original construction, authoritative execution and strict restore retain all existing validation and retained-dice/history checks. The checkpoint uses the same writer solely to compare against its already validated predecessor, without invoking validation or returning unchecked bytes to the caller.

Preserve every original schema marker, ordering rule, optional field, exact numeric representation, component encoding, limit and checksum. The comparison must neither normalize nor repair state. Stored RNG state and recorded dice are serialized as opaque fields; no RNG draw, reconstructed roll, command replay, choice settlement or deadline advancement is allowed. Audit all nested writers, helpers and property accessors, including the work-ledger and condition-journal component encoders.

## Proposed concrete assembly access

Current references are Core → no project assemblies; Persistence → Core; LabModel → Core and Persistence. They remain unchanged. Simulation owns the optional assessment interface in Core; the actual TEST_ONLY checkpoint implementation remains private in LabModel. Core must not gain a reference to Persistence or LabModel.

Propose a private `SnapshotCodec.EncodeCanonical` writer and an internal boolean comparison `SnapshotCodec.MatchesValidatedPredecessor(Snapshot current, byte[] expectedCanonical)`. The internal comparison calls the private writer, compares complete bytes and returns only match/failure; it neither returns encoded bytes nor retains caller buffers. Public Encode remains validated. This is not a public skipValidation option or unchecked save path.

Because the checkpoint is in LabModel, propose a narrowly declared friend assembly from Persistence to **Decennium.Foundation.LabModel**, with both the friend declaration and internal comparison member guarded by exact source condition `DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)`. The Unity asmdef keeps its existing editor/development constraints; the headless harness compiles the same source with HEADLESS_TESTS. No asmdef or dependency broadening is proposed. No friendship to the Unity presentation assembly or a general caller is proposed. The trusted private checkpoint is the sole non-test call site within the gated LabModel for the internal comparison; tests drive the actual owning checkpoint and may inspect internals only as labelled test evidence. Do not expose a caller-controlled comparison capability, predecessor array or PlanningPassage through the session/console.

This exact assembly-access proposal is not yet reviewed. Freeze the optional Core assessment interface/result type alongside the complete native fact/parameter DTO design. If the existing compilation/access constraints require another arrangement, return it for actual review before coding; do not introduce an unchecked public shortcut.

## Proposed concrete dispatch protocol

The optional interfaces belong to Core, alongside the existing verified-policy interfaces. Proposed names/signatures below describe the design only; no C# declarations have been added:

```csharp
public interface ICommandAssessmentFactsPolicyV1
{
    bool SupportsAssessment(CommandKind kind);
    bool RequiresVerifiedAssessment(CommandKind kind);
    NativeCommandAssessmentV1 AssessFacts(
        Snapshot current, Authority authority, Command command);
}

public interface IVerifiedCommandAssessmentV1
{
    NativeCommandAssessmentV1 AssessFacts(
        VerifiedSimulationOrigin origin, Snapshot current,
        Authority authority, Command command);
}
```

The proposed `NativeCommandAssessmentV1` is an immutable trusted policy result: supported/admissible flags, exact native failure stage/code, current revision, ordered rational cost/reservation/duration facts and conditional continuation facts. It is not a serialized public result or an authority token. The public DTO/disclosure matrix must define each allowed projection before implementation; introducing this carrier does not authorize raw record export.

The new owning-Simulation assessment performs the original current command/authority/receipt preflight, separately enforces the requested observation revision, and returns an exact-retry disposition without fresh gameplay eligibility. For a fresh supported command it captures the current owned snapshot once. If the actual immutable selected policy requires verified assessment, Simulation must use its own current checkpoint implementing `IVerifiedCommandAssessmentV1`; missing capability returns a safe verification failure. It must never fall back to `AssessFacts`, existing QueryCommand or policy Resolve. Unrequired operations use the policy's pure assessor. This protocol adds no caller-selectable verification mode.

In the current proposed scope, `RequiresVerifiedAssessment` is true for `StartNextCharterPlan` when the selected planning policy requires passage evidence. Its private checkpoint validates ownership and complete current bytes, then invokes the same private policy assessment with its immutable passage. The public policy method cannot supply or forge that passage and must reject an attempted direct call requiring the verified route. `AdvanceClock` initial admission describes current gates and conditional future settlement only; it does not inspect historical passage or run planning settlement to predict the future. If any description, discovery, cost or choice helper needs a planning basis, it requests this owning-Simulation assessment rather than calling a replay-capable helper directly.

The policy's existing resolver/restore paths keep their own verified execution and replay-authenticity behavior. Pure-assessment failures distinguish missing/mismatched proof from the native no-qualifying-crossing result. Returned exceptions/codes must be safely mapped without exposing canonical bytes, policy internals or hidden content. Exact public failure vocabulary and `NativeCommandAssessmentV1` field definitions remain part of the complete contract review.

## Required evidence before acceptance

1. Compare the shared writer's bytes with the unchanged validated encoder on genuine supported snapshots: condition/work/casting/Ferry histories, pending states, planning before/after relevant crossing, restored continuations and the historical codec corpus affected by the common writer.
2. Establish the complete new read call graph and instrument the forbidden paths: validators that reconstruct dice, RNG draws, receipt replay, resolvers, deadline advancement, choice settlement and checkpoint/state mutations. Unchanged live RandomState alone is insufficient.
3. Reject wrong owning Simulation with otherwise identical state, stale checkpoint, altered revision/policy/terms/wire/canonical content and mutation of exposed copies. No canonical-byte alias or proof escapes.
4. Cover no crossing, incomplete crossing, qualifying completion, completion beyond cutoff and restored continuation. Native no-evidence denial differs from invalid proof.
5. Confirm successful execution replaces the checkpoint normally; rejection and reads leave it unchanged. Restore obtains its own checkpoint after full existing validation.
6. Preserve public Encode and strict restore rejection of malformed/causally forged histories. Pure equality with a validated predecessor does not validate arbitrary new input.

The current source census covers 284 writer-side method names in 85 persistence files after excluding BinaryReader overloads. It identifies Validation.Snapshot at the Encode entry. This lexical census is only an audit aid: instance calls, property getters, overload resolution and state consumed but not directly encoded still require verification. No pure writer implementation or runtime qualification is claimed.
