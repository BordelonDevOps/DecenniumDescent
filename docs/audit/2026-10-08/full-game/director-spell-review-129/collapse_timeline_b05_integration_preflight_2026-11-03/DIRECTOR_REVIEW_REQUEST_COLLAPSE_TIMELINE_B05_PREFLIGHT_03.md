# Director review — Collapse Timeline B05 integration preflight revision 03

This is a proposal-only readiness request. Revision 02 was returned REVISE. Revision 03 incorporates CT-P02-C01 through CT-P02-C04. No owner premise has been adopted, and no Collapse fixture or witness has been constructed.

- Current main base: `9a0280d4e3bcbe888f44cb403c4cd747913dce8b`.
- Superseded revision 01 proposal: `COLLAPSE_TIMELINE_B05_INTEGRATION_PREFLIGHT_01.json` — SHA-256 `8c9e97911f15b00b71ae82d2796bf6d90688af04446b5269f021e888cb544056`.
- Superseded revision 02 proposal: `COLLAPSE_TIMELINE_B05_INTEGRATION_PREFLIGHT_02.json` — SHA-256 `3275e6eadb0ddf4281be935ac6a7ef801bacd4ba248e7ae25889dc28208220d8`.
- Revision 03 proposal: `COLLAPSE_TIMELINE_B05_INTEGRATION_PREFLIGHT_03.json` — SHA-256 `c233ee36ccb5072735aa7b8537985551ab887090ac09882d25e67523e85a6b35`.
- Queue482 remains 837 applied / 11 pending / 0 accepted-unapplied, with Collapse Timeline next and TF192-B05/TF192-B02 open.
- The proposal binds 27 exact source files and 83 JSON pointers in its source-binding inventory. All 83 resolve against the pinned source bytes at the revision 03 base. The current revision makes no source or premise changes.

Revision 03 incorporates the four exact Director corrections:

- **CT-P02-C01:** At 2001 ms, T’s source actor record now explicitly appends the Collapse cast receipt to `/actors/T/resourceHistory`, sets `/actors/T/seenFamilies` to `["collapse-timeline"]`, `/actors/T/lastSpell` to `"collapse-timeline"`, and `/actors/T/spellsThisTurn` to `1` before W’s Counterspell response. W’s inherited Eternal Prophecy family/name remain unchanged. The proposed inverses distinguish a selected-settlement rollback, which retains these paid-root writes, from full audit restoration, which removes them.
- **CT-P02-C02:** Regular marker histories are explicit and append once: W starts `[0,6000]`, ends `[1900,7900]`; T starts `[2000,8000]`, ends `[3900]`. START markers reset only `spellsThisTurn`; family/name and cast history persist. Reaction remains 1 after T END3900. The stale 20-ft reference is corrected to 30 ft. Branch event registries now follow the shared schedule order, including disclosure at 100 ms and incompatible-only support loss at 4000 ms before W START6000.
- **CT-P02-C03:** Both branch `clockSchedulePointer` values now resolve to `/proposedTestOnlyInputSpecification/sharedClockSchedule`.
- **CT-P02-C04:** The revision 01 and revision 02 SHA labels are corrected above. This request, manifest, proposal, and proposed owner wording bind revision 03’s actual proposal SHA-256 `c233ee36ccb5072735aa7b8537985551ab887090ac09882d25e67523e85a6b35`.

The Director previously confirmed that C06 is resolved within this bounded TEST_ONLY scope: the sole support plate is unavailable through the inclusive source-mapped deadline and returns at deadline+1 ms, with no replacement/retrieval in this fixture. That establishes neither native guarantee authority nor an actual guarantee failure. The prior review also verified the proposal/request/manifest hashes, all 27 source-file hashes, and the collision-clear 30-ft route. Revision 03 introduces no replacement premise.

Please return `PASS_FOR_OWNER_ADOPTION`, `REVISE` with exact pointers and terms, or `HOLD` with the precise gap, bound to proposal SHA-256 `c233ee36ccb5072735aa7b8537985551ab887090ac09882d25e67523e85a6b35` and branches `CT-B05-BRANCH-COMPAT-01` / `CT-B05-BRANCH-INCOMPAT-01`.

Do not construct either witness or seal, accept/apply Collapse Timeline, close B05/B02, claim native guarantee authority, or change canon/runtime/campaign/queue. A separate exact owner adoption is required before any witness construction.

Proposed owner wording, only after a Director readiness PASS:

> I adopt exact Collapse Timeline B05 integration preflight revision 03, SHA-256 `c233ee36ccb5072735aa7b8537985551ab887090ac09882d25e67523e85a6b35`, solely for construction and submission of bounded TEST_ONLY branches `CT-B05-BRANCH-COMPAT-01` and `CT-B05-BRANCH-INCOMPAT-01` for static authored-procedure review. This adopts only the conditional W/T Wizard-profile inputs; exact T acquisition/preparation and cast/focus/hand/anchor/resource/counter transaction, including the explicit T actor-history writes before W’s response; the source-mapped objective disclosure and complete six-second W/T schedule with one-time start/end histories; synthetic geometry, Collapse-specific support/cache/focus objects, and ordinary carry/placement; the incompatible candidate’s finite sole-support unavailability through the inclusive source-mapped deadline, with availability at deadline + 1 ms and no replacement/retrieval in this fixture; and the specified isolated versions, retained payments, generated-state hashes and reversible settlement. It does not transfer EP480 exceptional terminal/restoration behavior or permission, establish native guarantee authority, assert campaign events, seal a witness, close TF192-B05 or TF192-B02, qualify the promise, accept/apply Collapse Timeline, or change canon, catalog/source, runtime, campaign or queue. All listed qualifications remain open.
