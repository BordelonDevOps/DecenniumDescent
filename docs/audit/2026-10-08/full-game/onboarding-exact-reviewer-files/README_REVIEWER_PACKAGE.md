# Exact onboarding and charter reviewer package

Read NWX_Onboarding_and_Charter_Exact_Verdict.md first. This is one exact verdict for all six manuscripts and NW-01–20. Six named teaching/editorial corrections have sixteen exact replacement sites; the source/card mechanics remain unchanged.

NWX_CORRECTION_REGISTER.json carries exact old/replacement strings. All sixteen anchors were checked by an in-memory dry run only; the submission was not modified. NWX_FOCUSED_REVIEW_EXPECTATIONS.json contains eighteen finite acceptance expectations, not claimed live runtime passes. ONBOARDING_READ_ONLY_AUDIT.json records the 200 checks actually run against the immutable submission.

The submitted archive is not bundled or modified. To reproduce the read-only audit with Python and the originally supplied helper files:

```text
python audit.py --root PATH_TO_UNMODIFIED_EXTRACTED_SUBMISSION --archive PATH_TO_ORIGINAL_ZIP --out PATH_TO_SEPARATE_REPORT_DIRECTORY
```

No packages or network access are required. The report directory must be outside the submitted tree. This checks the preserved original submission, not an edited teaching tree; validate the corrected texts against the correction register separately.

Conditional acceptance applies only after the named corrections and finite receipt conditions. No pending class/spell/feat promotion, DD-01 closure, human teaching/balance result, runtime certification, GitHub push or cosmology review is granted. The fulfilled 687/687 recipe and 433/433 public gate carries forward.
