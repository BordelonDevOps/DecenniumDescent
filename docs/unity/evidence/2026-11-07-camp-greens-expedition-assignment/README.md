# Camp Greens assignment and Unity compile evidence

## C# increment

This increment connects the existing site-aware expedition assignment authority to the already adopted Camp Greens crop procedure. It adds bounded planting, tending, and harvesting assignment kinds. Assignment records continue to point to the existing work ledger and crop task records; the crop/task authority remains responsible for costs, timing, growth, harvest, and inventory output. No duplicate crop state or new save fields were introduced, and the schema 61 layout is unchanged.

The acceptance scenario directs a companion to the prepared plot, continues lead exploration, plants, saves and restores during work, advances the existing seven-day growth process through assigned daily care, then harvests. It checks shared travel/work/crop/inventory authorities, idempotent start, the exact eight-pound crop lot, save/restore, and deterministic continuation. The plot location and single prepared plot are TEST_ONLY LabModel fixture assumptions; this does not add general farming automation, arbitrary plot discovery, autonomous companion planning, or production UI.

## Validation

- Full shared-source C# regression suite: **1,235 / 1,235 passed**. Result: `FULL_TEST_RESULTS.json`.
- Focused assigned Camp Greens scenario: **1 / 1 passed**. Result: `FOCUSED_RESULTS.json`.
- Package static validation: **18 / 18 passed**, covering 271 assets with 271 unique GUIDs. Result: `PACKAGE_RESULTS.json`.
- Rule-binding evidence validation: **4 sources, 17 profiles, 340 RP cells, 23 named tests passed**. Result: `RULE_BINDINGS_VALIDATION.json`.
- Changed C# source hashes: `CHANGED_SOURCE_HASHES.json`.

## Unity import/compile smoke check

The isolated qualification copy imported the actual local package `com.decennium.foundation@0.1.0` from the reviewed base commit `e1301fab95dbd5ed483d55f93fab015fff9be7c5` using Unity **6000.3.28f1** (revision `8f082d2fe476`). `DECENNIUM_TEST_ONLY` was enabled through `Decennium.Foundation.EditorTools.LaboratoryGate.Enable`. Unity exited with code 0 and no compiler failure matches. It produced `Decennium.Foundation.Core`, `Decennium.Foundation.Persistence`, and `Decennium.Foundation.LabModel` assemblies; names, byte sizes, and SHA-256 values are recorded in `unity-qualification-results/UNITY_COMPILE_RESULTS.json`.

The existing locked Unity package versions were unchanged. Before/after manifests, lockfiles, project settings, command exit records, and Editor logs are retained in `unity-qualification-results/`. Evidence text has normalized line endings and trailing horizontal whitespace; credential-like token values in logs are redacted in this repository copy. The recorded `logSha256` hashes the sanitized final compile log, and `rawQualificationLogSha256` records the untouched original’s hash. The untouched qualification copy and raw logs remain at `C:\Users\cbord\Documents\ChatGPT\Decennium Descent\qualification-e1301fab` on the development machine.

The Editor emitted a LicensingClient validation warning and noted that the WindowsStandalone native extension is absent. The Editor still compiled the required assemblies successfully. Edit Mode tests, Play Mode, scene/runtime integration, and player builds were not run; this was an import/compile smoke check only.

## Compatibility corrections made during qualification

The initial qualification attempts exposed three concrete issues, recorded in the result JSON: the temporary package-registration helper enumerated a non-enumerable UPM request result; its local package URI resolved one directory too high; and two existing `.meta` files lacked a final line feed and failed Unity YAML parsing. The helper and qualification-copy URI were corrected. The two metadata files were minimally corrected in the Engine branch, preserving their GUIDs:

- `ReadyActionRecords.cs.meta`
- `ReadyActionCodec.cs.meta`

The final Unity compile passed after those corrections. The Unity check was performed against the reviewed base commit before the Camp Greens code increment, as requested; the smoke result does not claim that the later C# increment was compiled by Unity.
