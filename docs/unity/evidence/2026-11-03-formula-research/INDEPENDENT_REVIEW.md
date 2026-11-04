# Independent engineering review

Reviewer: `/root/source_review`. Scope: schema15 formula work, shared scheduling, copying supplies, access/authority, pending choices, replay and codec.

Two actionable defects were independently found and corrected with permanent regressions:

1. `AwaitingCheck` resume incorrectly required another labor window. A researcher finishing at the final16-hour boundary while incapable could never resolve the earned check after recovering at16hours+1second. Only the fully worked check now bypasses the new-labor-window requirement; access, current capability, participation and other prerequisites remain enforced.
2. Formula commands bypassed tactical pending-choice gates. The reviewer reproduced a fully worked remote research check consuming RNG while a paid unarmed knockout decision was pending. The later knockout completion rejected its now-mismatched retained RNG, stranding the choice. All formula commands now reject while KO/OA/Press choices are pending. The permanent lawful regression verifies unchanged state/RNG and successful original knockout completion before research resumes.

The parent also changed prior-failure selection to actual completion chronology rather than array order, because canonical serialization sorts identities; added an explicit exhausted-writing-supply diagnostic; and corrected a test setup that attempted a plot-only Drop away from the plot to use legal Stow. These are not attributed as reviewer discoveries.

Final candidate: `engine/artifacts/run-20261104T035948452Z-f9684f01`. The reviewer independently executed25 nondisk formula/active-work cases; all passed. The cases cover both review regressions, finite supply cancellation and memory restore, source check boundaries, current inventory grants, retries, exclusive labor, Watch endpoints and condition completion order. All109 compiled-source hashes matched. No remaining actionable finding was reported in the bounded profile.

The parent receipt reports864/864. The reviewer did not independently rerun the full suite, disk cases, legacy byte comparison or Unity. Those parent C# checks have separate receipts. The review does not qualify arbitrary research, manufacturing, a complete engine or release content.
