# EX58 exact-candidate verdict and evidence

Controlling document: **EX58_EXACT_VERDICT.md**. There is one required issue,
**EX58-X01**, correcting two class-specific RP pools in EX-W13, with one complete
premise and four numeric replacements. The other authored procedures and examples
are retained. This is not another source conference.

The original candidate is conditionally accepted as an authored operational
playtest candidate only after the finite amendment checks. The original
uncorrected EX-W13 is not accepted. No pending class/spell/feat, runtime, human,
balance, whole-game, push or cosmology approval follows.

## Files and scope

- EX58_EXACT_DISPOSITION_REGISTER.json: all58 directions,15 ECX requirements,
  190 chapter examples,29 transport profiles,four auxiliaries,21 events,
  15 contract families,28 boundaries,24 social cases and12 reputation probes.
- EX58_X01_CORRECTIONS.json: complete old/new fields,25 guarded JSON operations
  across five current case views, four Markdown mirrors, two current binding
  refreshes, and exact preservation boundaries.
- EX_W13_CORRECTED_REFERENCE.json: the full corrected case.
- EX58_X01_SOURCE_EXCERPTS.md: actual submitted source paths, lines and hashes.
- EX58_REFERENCE_AMENDMENT_HASHES.json: eight exact pre-label descendant hashes;
  all411 other payloads, including304 original V3 payloads, stay unchanged.
- EX58_INSPECTION_REGISTER.json: what was actually read/compared and its limits,
  plus all submitted payload bindings.
- SUBMITTED_ASSEMBLY_CHECKS.json and REPRODUCED_ASSEMBLY_CHECKS.json:
  preserved1213-check submission and reproduced1214-check result. The extra
  passing check is the original local V3 README now available in the working copy.
- REVIEWER_BASELINE.json:1584 checks,1582 passes/two failures, bothEX58-X01.
- REVIEWER_REFERENCE_AMENDED.json:1584 passes/zero failures on the separate
  reference-amended tree.
- EX58_X01_STRICT_REFERENCE_CHECKS.json:435 passing strict/reference checks,
  including eight deliberately invalid resource fixtures.
- EX58_EXACT_REVIEW_RECEIPT.json: scoped authority and measured evidence bindings.

No arithmetic/reference result is a general gameplay runtime or authentication
of an actual campaign. The190/28/24 semantic dispositions remain authored review
judgments, not invented executed tests.

## Reproduce with Python 3.12+ standard library

Keep the original archive and extract it to an ORIGINAL_ROOT. Use new report and
output paths. These commands need no network or package installation.

```text
python review_ex58_exact.py ORIGINAL_ROOT ORIGINAL_ZIP baseline_report.json
python apply_ex58_x01_reference.py ORIGINAL_ROOT NEW_REFERENCE_ROOT amendment_report.json
python review_ex58_exact.py NEW_REFERENCE_ROOT ORIGINAL_ZIP corrected_report.json
python validate_ex58_x01_fulfillment.py NEW_REFERENCE_ROOT strict_report.json
```

The baseline correctly reports the two known resource violations. The corrected
reference should pass1584 checks and the strict check435. The amendment script
refuses an existing destination and checks every frozen input before copying.
It changes only eight current candidate files and two current nested component
bindings. It leaves all historical manuscripts, sources, scripts, original
manifests and old reports intact. The original source extraction is never edited.

Strict byte matching is for the **corrected pre-label** tree. After successful
fulfillment, the limited current authored-review wrapper/receipt label changes
authorized in the verdict require a separate reversible label-only proof; they
must not change mechanics, source statuses, runtime selection or original hashes.
The preserved original builder must not be run over corrected outputs; any
maintained generator descendant is separately tracked, not a new source rule.

The supplied assembler render functions are reused without invoking their
mutation-oriented main(). The reviewer code is a reference checker, not a game
engine. The original submission validator was run in a separate working copy,
with its root variables rebound and its preexisting output report preserved
before a fresh report was generated.

Package FILE_MANIFEST.json hashes every payload except itself. It does not
contain its own hash or the enclosing ZIP hash, avoiding circular receipts.
