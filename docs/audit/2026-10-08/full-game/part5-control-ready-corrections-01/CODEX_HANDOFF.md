# Codex handoff — Part 5 Control/Ready scoped corrections

## Instruction boundary

The owner asked for corrections now and will separately instruct Codex to implement them. This package makes **no repository write**. Only the six named decisions and 22 exact operations are selected. Unchanged material in the five complete corrected files remains at its existing pending/provisional status; **neither Control15 nor Feat335 is accepted as a whole**.

Prior Illusion Exact13 and Companion Exact05 acceptances and holds are independent. Do not change their eight bound artifacts to integrate these unrelated corrections. Do not increment the reviewed index from this receipt.

## Use after the owner's instruction

Read `CORRECTION_RECEIPT.json`, `SCOPED_DECISIONS.json`, `HOLD_REGISTER.json`, `SOURCE_REFERENCES.json` and the complete relevant baseline procedures/cases. `POINTER_OPERATIONS.json` contains the exact repository paths, JSON pointers and full before/after values. `ARTIFACT_BINDINGS.json` binds all five before and after byte sequences.

Run verification first from this extracted directory:

```text
python verify_bundle.py --report local_verification.json
python apply_corrections.py
python apply_corrections.py --reverse
```

The last two commands only verify. They do not modify files.

To compare the proposed operation bases against an actual local repository, use its root:

```text
python apply_corrections.py --source-root "C:\path\to\DecenniumDescent"
```

**Any hash or full-before-value mismatch stops the entire plan.** This packet binds supplied archive snapshots, not a later working tree. Never solve drift with an overwrite, deleted history, changed hash assertion or partial application. Read the actual successor in full, identify already-applied equivalents, preserve unrelated later changes, and produce a freshly bound reconciliation for any remaining operations.

To stage verified corrected copies into a NEW directory outside the source repository and this package:

```text
python apply_corrections.py --source-root "C:\path\to\DecenniumDescent" --output "C:\path\to\DD_control_ready_staging"
```

The stager writes only the five named JSONs to that new directory. It never stages index/registry files, Git commits or game-runtime flags. Reverse staging uses `--reverse` and a corrected source root; the resulting files recover the original exact bytes. Original archive copies remain preserved in `baseline/`.

## Actual implementation work remains separate

Implement the selected transactions in the actual engine/adapters using actual source providers. The supplied Python reference models are **test specifications, not production game code** and must not replace existing engine modules. Turn the ten full `IMPLEMENTATION_CASES.json` obligations into actual source-qualified runtime tests. Their missing CR, contest and extra-opportunity premises must remain conditional unless an actual approved provider supplies them.

For Mental Prison, preserve one admission-created original-caster root; consume exit once before callbacks; keep old-exit/new-entry and same-caster concentration displacement ordered. Do not port Spectral Army's different root rule.

For Puppet, first-future-END saves are independent of route execution; do not create phases. For Geas, soft admission cannot silently acquire a full Action. For Dominate Monster, use only its explicitly named save/phase bridge and actual CR-qualified chassis. Ordinary Ready selection occurs at release, while its one paid casting/counter transaction occurs at preparation.

For the copied feats, enforce preparation-round and actual later release-round allowances atomically, with no second RP/components/permission/casting-history transaction. An actually unowned Mirrorsage engine must never be invented. Preserve consumed receipts and original expiry across save/load. All three affected feat operative mirrors and acquisition mirrors must agree.

After any implementation, rerun existing project suites and actual cross-system tests, report precisely what executed, and supply the full exact affected artifacts/renderings for verification. Do not claim approval of those future bytes from this package. Preserve all named holds, source/access records and original scenarios. No cosmology, CR approval, balance, 75-domain, whole-game or release approval follows.
