# Copied-feat targeted follow-up — supplement02

## Verdict

**Both reported defects are confirmed in the original reference code and in Return01's exact proposed payload.** They should have appeared in the prior final disposition. They were omissions, not justified exclusions for unsupported active healing sources or unimplemented Oracle acquisition.

This separately bound supplement selects **three exact text operations in one Python reference file**. It preserves the complete Return01 archive and all its nested evidence. It does not restart the seven-profile review, change a gameplay rule, apply code, or change any accepted spell artifact/index/runtime flag.

`CONFIRM_BOTH_OMITTED_DEFECTS__SELECT_EXACT_THREE_OPERATION_REFERENCE_CODE_SUPPLEMENT__NOT_APPLIED`

The supplied applied baseline remains **525 reviewed / 323 pending / 249 standalone / 173 scoped interfaces**, with **39 accepted-but-unapplied spell identities**. Those are not incremented by this reference-code correction.

## CFI-06 — inactive next-healing records must not block Mend

### Source basis

The unchanged `healing_playtest_rules.py` uses:

```python
live = [r for r in reductions if r.present and not r.suppressed]
```

Its final next-healing candidate list is derived from that live list, and its contract leaves actual source limits and consumption to the caller. The preserved `HEALING_DEATH_PLAYTEST.md`, lines76–78, likewise excludes suppressed reducers from participation and consumption while retaining consumption for present, operative, applicable sources at a committed positive-potential healing event.

Return01 instead used `any(r.next_healing ...)` at both the declaration and paid-resolution guards. That rejected records the actual arithmetic and consumption-candidate logic ignore. `LIMIT-DEFENSES`'s valid open active-source adapter does not justify this inactive-record rejection.

Complete source references and exact line ranges are in `SOURCE_REFERENCES.json` / `SOURCE_EXCERPTS.md`. Full helper and chapter bytes are included under `sources/`.

### Reproduction and correction

Both supplied paid Mend cases reproduce in the original and Return01-proposed trees. With `nativeDice:[4,4]`, either an absent record or a present-but-suppressed record leaves the recipient at30HP and raises `New next-healing source needs its actual consumption adapter`. The failure is atomic, but the attempt is still incorrectly rejected. Independently testing the declaration guard finds the same erroneous rejection before payment.

Both guards now use:

```python
r.present and not r.suppressed and r.next_healing
```

The supplied successful paths now restore **30→32HP**, report **no next-healing candidates**, keep the already paid RP at42, and preserve the inactive reducer record without consuming or removing it. Canonical LifeState references remain intact.

An actually present, unsuppressed next-healing source is still rejected pending its real source-owned adapter. An active reducer's losing the strongest arithmetic comparison does not grant free consumption or permission. A reducer that becomes operative after declaration is rechecked before payload mutation. A previously unresolved paid attempt can proceed when its current record is genuinely suppressed, without charging again. Ordinary live non-next reductions and broad HP-gain prohibition remain in force.

This corrects inactive-record handling only. It does not implement active next-healing source eligibility, consumption or resource accounting. The positive inactive tests and protective active rejections are reported separately.

## CFI-07 — natural-expiry instructions must survive the shared-world boundary

### Source basis

The existing `BufferLedger` contract explicitly requires one shared world ledger, runs expiry at actual supplied deadlines, and **returns side effects as instructions**. It does not choose eligible conditions or cleanse automatically.

For a qualifying `oracle.supplement.life.overflowing-light` grant with positive temporary HP remaining at natural expiry, the existing helper returns:

```json
{
  "sourceId": "oracle.supplement.life.overflowing-light",
  "grantId": "actual-prior-overflow",
  "target": "target",
  "chooseUpTo": 1,
  "eligibleConditions": ["Frightened", "Poisoned", "Staggered"]
}
```

Return01's `CopyPayloadWorld.advance()` called `self.buffers.expire(marker);self.projection()` and discarded that list. This permanently ended the shared grant while losing its source-owned instruction. A later expiry cannot recover it. The copy world's declared integration includes canonical shared-buffer mutation, so Oracle acquisition being outside that adapter does not license this loss from an already-lawfully-established source.

The source helper's own implementation-review status remains as preserved. This follow-up validates the narrow caller-contract defect; it does not certify the full BufferLedger or Oracle system.

### Reproduction and correction

The supplied5-tempHP, deadline12 fixture reproduces in both original and Return01. The grant becomes `natural-expiry`, temporary HP becomes0, `advance()` returns `None`, and another `expire(12)` returns `[]`.

The successor retains the existing validation, source-deadline ordering and projection update, then returns the complete instruction list:

```python
instructions = self.buffers.expire(marker)
self.projection()
return instructions
```

The fixture now returns the exact original instruction. Source ID, grant ID, target and choice envelope are unchanged; the ended grant retains `prior-owner` for downstream lookup. A simultaneous copied Ward still ends only its own dependent buffer; it does not gain the other source's cleanse. Multiple actual source grants retain the helper's existing order. Replaced, depleted, dependency-ended and plain no-rider buffers gain no new natural-expiry cleanse.

### Completed handoff, still-open downstream work

The new positive test captures the returned instruction into a caller-owned recorder. Another test confirms that the existing Frightened/Poisoned/Staggered/Blinded condition set is **not automatically modified**. This proves positive output preservation, not Oracle acquisition or gameplay condition removal.

The real caller must route every nonempty result to the actual source/target choice adapter. Actual eligibility, zero-or-one selection, removal, timing, processing receipts, acknowledgment, save/load and crash recovery remain separate. An ignored return is not recoverable by expiring again. No durable outbox or production event dispatcher has been invented by this correction.

The delivered nine `world.advance` callsites are in fixtures/validators, not an established production receiver. Their original finite cases do not include the lost external-source expiry event. `DOWNSTREAM_HANDOFF_BOUNDARY.json` records those complete call lines and their source hashes. Returning an instruction is not claimed as completion of that larger integration.

## Complete diagnostic dispositions

| Supplied case | Disposition | Successor result |
|---|---|---|
| LOCAL-COPY-INACTIVE-MEND-ABSENT | Confirmed defect; corrected at supplied paid inputs |30→32HP; no consumption candidates; absent record retained.|
| LOCAL-COPY-INACTIVE-MEND-SUPPRESSED | Confirmed defect; corrected at supplied paid inputs |30→32HP; no consumption candidates; suppressed record retained.|
| LOCAL-COPY-SHARED-BUFFER-EXPIRY-01 | Confirmed instruction-loss defect; corrected boundary handoff |One exact source-owned instruction returned; tempHP0; second expiry empty; no automatic cleanse.|

Two additional complete before-declaration cases verify the other guard. `CASE_DISPOSITIONS.json` contains the full user objects and complete original, Return01 and successor reproduction states for all five cases. It is not an identifier-only census.

The user's one-shot script is preserved as text and was not executed. The raw local receipt02 and14,719-byte local preflight were not attached in this turn; their reported hashes are recorded, not falsely byte-verified from the inline excerpts. Fresh independent probes used separate archival trees and output paths.

## Exact files and reconstruction

Only `DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py` changes in this supplement.

| Baseline/successor | Bytes | SHA256 |
|---|---:|---|
| Original source |22,515|`c53e48e9be34798f9053f07fa55e07169ec3117ad7fd7c8f6731074747455455`|
| Return01 proposed payload |22,991|`35e746cfe14b88073539eac763c063c5d05d630bc582ebd0c1187c6aba80f1e3`|
| Supplement02 successor |23,519|`2b45d33ff0bdc6230aa4fbfd563f59bc0e2537616210ade940d2dd22954ccc1d`|

The three operations replace the complete `advance()` method, the exact declaration guard and the exact paid-payload guard. `CODE_OPERATIONS_FROM_RETURN01.json` supplies full before/after text. The whole four-file successor is included; capture, class-release and release files are unchanged from Return01.

The **14 cumulative operations** from the original four files retain Return01's11 verbatim and append these3. This is an alternative to applying Return01 then this supplement. Do not apply both paths. Both full forward reconstructions and both reversals are byte-exact. No fuzzy, line-number-only or partial patch is authorized. Stop and reconcile actual local drift before future owner-authorized application.

## Tests, preservation and limits

**36 new targeted isolated tests pass**, including both inactive guards across all inactive Boolean states, active-source atomic rejections, later reactivation, retained reducer/HP object identity, ordinary reductions, no double resolution, exact positive expiry handoff, source-owner retention, multiple-grant output, no re-emission and no automatic cleansing.

The **47 Return01 regression tests** and **456 existing helper assertions** (136 release,115 payloads,205 classes) pass on the complete successor. All **68 ordinary histories** compare in full with Return01's proposed histories; the seven Ready lifecycle histories and source acceptance coverage also remain identical. Reconstructed source bytes did not change during the tests. The existing DI7 Windows locator was rebound only in memory by the unchanged prior runner.

The separate read-only verifier checks preserved archive/member bindings,157 source-member records across78 distinct paths, exact operations/reversals, preserved histories and report consistency. It imports no project code. Test results are not inferred from hash-check counts.

**No game-engine runtime, human gameplay or balance test was performed.** Full cross-round Ready, linked Shaman positive canonical movement, native concentration transitions, durable canonical-ledger ownership, unimplemented Boon/Step variants, active next-healing consumption and downstream expiry processing remain open. The prior whole positive-case content/contest holds remain IN6-09-A, IN6-09-B, EN5-01-A, EN5-01-B and EN6-03-B. The separate Control15/Mental Prison authoring acceptance is not reopened.

The complete unchanged Return01 ZIP preserves all seven previous input/acceptance archives and the prior Control/Ready correction history. No accepted24 spell artifacts, original cases, prior verdict bytes, JSON rules, project index, runtime flags, CR values, creature checks or cosmology are changed. No blanket335-feat,75-domain, whole-game or release approval follows. No unsent cohort was reviewed. Rank8Damage6 and Rank7IdentityCasting5 remain the next delivered conferences.
