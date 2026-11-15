# CHR-02 shared RP contract review

Status: proposed; implementation not started. [Source/API contract](SOURCE_API_CONTRACT.md).

This gate proposes a validated first-class Cleric companion construction and one real paid Healing Rite in the connected expedition. Three decisions remain explicitly pending actual GPT review: the precise dependency refinement for this paid witness, one-time starting RP funding, and the boundary between this class-portion initialization and the unfinished full character-creation pipeline. No existing Warrior is granted Cleric abilities and no predecessor save is altered.

[Bindings](SOURCE_API_BINDINGS.json) retain exact source files, selected card/initial class row and baseline code evidence. [Validation](CONTRACT_VALIDATION.json) checks source identities, printed cost/acquisition, initial numerical facts, dependency edges and unchanged engine. It does not compile or execute this proposed feature. Run `python -X utf8 docs/unity/evidence/2026-11-15-chr02-shared-rp/Verify-Contract.py` from the repository root.

Previous actual review: [resurrection source gate and CHR-02 order](../2026-11-15-tac06-resurrection/GPT_CONTRACT_REVIEW.md), response `50395a8a-f1f7-58ac-81b6-a9e116e35f09`. Baseline: `27a942aa549c78f23d5db300a71590a738b97120`. Accepted engine remains Flesh Warden `0742794a7c1f8e15dd4e38ff72ae21dd61762b4a`, with [1,503-case and connected evidence](../2026-11-14-tac06-maximum-hp/README.md). No new runtime test or scenario is claimed here.

Actual gameplay acceptance requires legal acquisition, finite source payment, real healing and rejection, shared state and saved deterministic continuation through the larger loop. A profile, ledger, schema or passing source check is not completion. Resurrection, full class/spell/creation coverage, production authority and the full engine remain open; Unity integration stays deferred.
