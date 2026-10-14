# Fishing exact-review audit evidence

This is an internal audit of the supplied three-part Fishing operational candidate. It is not a game runtime or a publication build.

## Files and execution

`FISHING_EXACT_OPERATIONAL_VERDICT.md` contains the finite correction gate and conditional promotion authorization.

`fishing_reference_submitted.py` is a local transcription of the submitted helper, with no intended logic changes. `fixture_submitted.py` transcribes the submitted Fixture class, adapting its imports to local test inputs. `source_register_mechanical_inputs.json` contains only the source-derived mechanical fields required by the probes, not the full original source cards. The independent Part A numeric transcription is in `arithmetic_crosscheck.py`.

Run with Python's standard library from this directory:

```text
python arithmetic_crosscheck.py
python adversarial_probes.py
```

The results are saved to `arithmetic_results.json` and `adversarial_results.json`. `review_execution_summary.json` distinguishes locally executed work from the original repository checks that were not rerun.

An `accepted` result in the adversarial log describes the submitted helper's behavior; it is not a rules approval. The probes include inconsistent or insufficient synthetic governing records to expose missing bindings, plus valid timelines or material-loss cases. They make no actual campaign claims.

These probes are counterexamples, not a complete post-repair acceptance suite. A stricter evidence schema will require enriched positive fixtures. Retain the substantive positive and negative cases specified in the verdict rather than treating old incomplete fixtures as sufficient evidence.

The original repository's 220 checks, six candidate artifact hashes, and 63 protected repository hashes were not independently rerun or verified here. The mounted source-verdict file itself was checked and matched the supplied SHA-256. No original source file was edited and no GitHub action was performed.
