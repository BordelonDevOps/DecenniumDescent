# Language exact-review evidence package

Read `LAX_Language_Communication_Exact_Verdict.md` first. `LAX_CORRECTIONS.json` supplies the three exact changes, complete replacement field objects and complete replacement LA-T30. `LAX_CASE_DISPOSITIONS.json` contains all16 direction applications and32 semantic case dispositions.

The submitted archive and its184 payloads are unmodified. The package contains no rewritten source catalog, pending-spell implementation, font, game runtime or promotion receipt. Reviewer-local proposed corrections were tested in a separate extracted copy; those results do not claim owner-repository fulfillment.

Evidence distinguishes: original460 source checks; original492/496 candidate outcome (four missing links); independent705/711 read-only comparisons (the same links plus two authored consistency findings); proposed496/496 candidate result; and44 focused checks, of which14 are executable reference-contract fixtures and30 are static/source comparisons. These totals overlap and must not be summed as unique mechanical tests. All32 sequence judgments are authored semantic assessments, not runtime passes.

Reproduce immutable checks, standard library only:

```text
python verify_language_exact_review.py PATH_TO_FROZEN_TREE --archive PATH_TO_ORIGINAL_ZIP --output OUTSIDE_TREE_REPORT.json
```

After applying the exact named changes to a separate working tree, reproduce focused checks:

```text
python verify_lax_named_corrections.py PATH_TO_FROZEN_TREE PATH_TO_CORRECTED_TREE --output OUTSIDE_TREES_REPORT.json
```

The original candidate validator writes its named report: run it only in the corrected working copy, with the one prescribed provenance assertion change. The source validator supplied inside the original archive is read-only on its original source ZIP. Preserve every original report. The review label may change only after the verdict's finite fulfillment conditions and version-bound receipt; runtime/class/spell/feat/whole-game/cosmology flags are not promoted.
