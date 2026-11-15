# TAC-06 resurrection source/API review packet

Status: pending actual GPT review. No resurrection implementation has begun.

The [source/API contract](SOURCE_API_CONTRACT.md) selects Cleric/Saint Resurrection and records concrete missing connected prerequisites. It proposes the mapped CHR-02 class-entry/access and shared RP source/API gate first, with later TAC-07/TAC-08/CHR-03/CHR-05 source-specific dependencies still individually gated. The payment ambiguity is explicit and needs consensus. There is no new fixture grant, wire version or production authority.

[Source bindings](SOURCE_API_BINDINGS.json) retain the exact selected card and classified healing binding plus immutable source and engine-audit hashes. [Validation](CONTRACT_VALIDATION.json) checks those source bytes, selectors and unchanged engine; it does not certify runtime behavior. Reproduce from repository root with `python -X utf8 docs/unity/evidence/2026-11-15-tac06-resurrection/Verify-Contract.py`.

Accepted predecessor: Flesh Warden implementation `0742794a7c1f8e15dd4e38ff72ae21dd61762b4a`, evidence `16984cdf3d79450d42880140dacaa69634c8ae42`, actual GPT response `7b1e6b05-b5aa-5853-9cae-0bb428e20edb`, acknowledged at baseline `2082003073be9124e7a3e6c15113828cceee56e6`. Its [final acceptance](../2026-11-14-tac06-maximum-hp/GPT_FINAL_REVIEW.md) and [completed evidence](../2026-11-14-tac06-maximum-hp/README.md) remain unchanged: 1,503 cases, 73 connected checkpoints and authentic wire95-103 compatibility. These are predecessor results, not resurrection results.

Compilation, C# tests and a connected resurrection scenario are NOT RUN for this documentation-only gate. Full engine completion remains open; Unity gameplay integration stays deferred. Commit only this packet's exact files, submit the immutable commit to Unity Rules Engine Development Part 2, and retain the actual review before acting on a successor.
