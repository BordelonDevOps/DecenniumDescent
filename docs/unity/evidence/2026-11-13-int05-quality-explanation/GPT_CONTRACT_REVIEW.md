Actual Unity Rules Engine Development reply `1ae13e3c-5679-4aa9-95ce-364d2676ef79`, recorded verbatim apart from trailing whitespace.

## INT-05 pending recipe-4 quality explanation — approved for implementation

**Reviewed contract:** `4f53b6dcf794a5e014852172d7a99601265693d3`
**Accepted engine baseline:** `75872e1e01fea9b17fce0c5c6c34d56679848961`

**Approve the bounded read-only C# API and shared-calculation approach. No blocking source/API issue remains. Codex may implement this scope without another preliminary packet.**

The comparison with the accepted INT-04 packet contains only the contract, recorded review and handoff changes—no engine or console edits.

The direct dependencies remain **FND-05 and INT-03**, using their accepted selected scopes. INT-04 supplies supporting independent verification; it is not an additional formal prerequisite. This does not close broader FND-05, INT-03 or INT-05.

## 1. Public API and information boundary

Approve the proposed signature:

```csharp
ExpeditionManufacturingQualityExplanation ExplainManufacturingQuality(
    ExpeditionSeat seat,
    long expectedRevision,
    string decisionId);
```

The method must evaluate one coherent state under the existing session lock. Require the current Player grant, matching revision, the actual **top pending ManufacturingQuality decision**, its controlled worker and required inventory permission, the selected connected recipe-4 order, existing formula knowledge and **Exceptional** quality. Return the same `null` for the specified invalid, inaccessible, unsupported or resolved requests.

Use `ActingActor` rather than merely finding an arbitrary awaiting-quality order. The existing decision selector gives knockout, indexed opportunity and Press their precedence before manufacturing; the new query must not expose a lower-priority decision as currently actionable.

The successful result must be **detached and immutable**, including its ordered alternatives and source labels. It may contain the proposed revision, decision/worker/recipe identities, actual quality, projected quantities, structural vial HP and supplementary packaging settlement. It must not return raw records, grants, component-lot identities, future dice or estimated actual healing.

The result is advisory. Holding an old explanation does not bypass subsequent revocation, revision checks, pending-choice ownership or normal command admission. Querying must not create a receipt or reserve an option.

**Masterwork remains uniformly unsupported by this first explanation API.** Do not suppress its catalyst decision and present an incomplete preview. A valid supported request with no admissible alternatives should also return `null`, not a misleading success object.

## 2. FND-05 binding is sufficient—but project only the public subset

The existing manifest binds `recipe-4` to an exact semantic source address, marks it public but **requiring existing knowledge**, and supplies supported manufacturing and produced-item handlers. It also contains internal review records and authority references that are not appropriate public output.

Accordingly, approve projection of the exact recipe source revision/blob/pointer and reviewed public recipe reference, subject to the current knowledge and handler checks. **Do not forward the whole `ContentDefinitionBinding` or `AuthorityReferences` collection.** Public visibility alone is not proof that this worker knows the formula.

Keep the effect description limited to the supported source meaning:

> Ordinary magical nonspell healing: **2d4+2**, subject to the recipient’s actual caps and blockers. Quality does not increase potency.

This is a rule label, not a prediction of a future dose’s roll or effective healing. It grants no new production authority or recipe discovery.

## 3. Shared settlement math — approved, with compatibility requirements

The existing assessment already checks the actual awaiting order, native quality choice, catalyst-selection shape and Full Yield’s packaging eligibility. Reuse that assessment and the existing command preflight under the current grant. **Do not call settlement—or execute a speculative command on a copy—to produce the explanation.**

Approve extraction of one pure calculation used by both the explanation and actual settlement. Preserve `ManufacturingRules.Yield`, source-vessel accounting and native container-HP behavior rather than copying the independent INT-04 oracle into production code.

For the genuine Exceptional order with two reserved supplementary vials, the expected explanation is:

| Alternative | Doses | Structural HP per vial | Supplementary consumed | Supplementary released |
|---|---:|---:|---:|---:|
| Full Yield | 6 | 1 current / 1 maximum | 1 | 1 |
| Durability | 5 | 2 current / 2 maximum | 0 | 2 |

**Packaging release comes from the actual outstanding claim and existing settlement convention—not all available inventory and not an assumed constant of two.** With zero supplementary vials legitimately reserved, omit Full Yield, retain Durability, and report zero supplementary consumption/release. Absence of a packaging claim in that valid branch is not an error.

Preserve these implementation boundaries:

- Calculate the needed plan before claim mutation, or otherwise ensure later reads do not accidentally interpret already-settled claims as the original reservation.
- Keep component settlement, catalyst retention, XP, dose creation and connected specimen disposition in their existing authoritative paths.
- Preserve the Mishap sequence: input settlement occurs **before** its d6 and consequences, and the later `inputsSettled` path must not settle again.
- Preserve older recipe/profile behavior, including zero-output outcomes. Do not impose the new explanation’s Exceptional-only restriction on the shared engine calculator.

The current settlement code makes that ordering explicit. Its duplicated yield/packaging/container arithmetic can be shared without changing the rule, but the extraction must not become a lifecycle rewrite.

No schema field, fingerprint, new gameplay command or serialized preview is needed.

## 4. Acceptance evidence — approve the four proposed groups

| Group | Required evidence |
|---|---|
| **1. Pure, accurate explanation** | Reach the genuine pending state through public commands. Repeated queries preserve complete canonical bytes and existing permitted views. Verify stable source labels, ordered alternatives and exact quantities. Include the actual zero-extra-vial branch; do not create it by editing a snapshot. |
| **2. Explanation-to-settlement agreement** | Restore the pending save into independent sessions and execute each displayed native option. Compare actual packaging consumption/release, output count and structural HP with the explanation. Preserve the established healing, Action and continuation behavior using the standalone oracle or an equivalent connected reproduction. |
| **3. Authority, privacy and lifecycle** | Exercise wrong/invalid seat, revocation, stale revision, mismatched/malformed ID, before-pending and resolved queries. Require uniform null and unchanged state. Verify unsupported quality gating, restoration under current grants, stale-preview submission and existing duplicate/conflict behavior. Inspect the result’s complete public shape for prohibited data. |
| **4. Exact implementation compatibility** | Retain changed-source and executed-assembly bindings, C# 9 warnings-as-errors compilation, package checks, focused registered cases, authentic saves/replay, and the complete exact suite containing **all 1,489 predecessors plus the new registered cases**. |

Include evidence that a higher-priority pending decision cannot be bypassed by this query. Reuse an existing admitted control where available; a clearly labelled detached projection may supplement an otherwise unreachable combination without inventing new gameplay.

**This increment changes compiled engine/session code and shared settlement calculation, so it needs a new exact full regression.** The earlier standalone-verifier exemption does not apply. Keep standalone assertions distinct from registered case counts.

The existing public view and console response shapes should remain unchanged. The new API can be tested directly through C#; console exposure and Unity presentation remain outside this increment. Record query costs, but no new performance gate or P1 optimization is introduced here.

## Inspection limits and final ruling

I inspected the exact contract and commit, the documentation-only comparison, current session locking/grants/decision precedence, quality assessment and settlement paths, manufacturing definitions/calculations, and the finite content-manifest binding and visibility model.

I did not execute code, compile, run tests, load saves or modify repository files. This approves the implementation contract; it does not pre-accept an implementation or its results.

**Final ruling: authorize the bounded INT-05 owner-scoped pending recipe-4 quality explanation at `4f53b6dcf794a5e014852172d7a99601265693d3`, under the requirements above. No further preliminary review is required.**

Prior acceptances stand. Wider explanation/discovery, other qualities and recipes, broader P1, production promotion and Unity integration retain their existing limits.
