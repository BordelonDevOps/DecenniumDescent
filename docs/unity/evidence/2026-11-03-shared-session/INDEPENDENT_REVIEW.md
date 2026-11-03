# Independent engineering review

Reviewer: separate Codex `source_review` agent, read-only, under development brief section14. This is distinct from the owner-designated GPT product discussion. The reviewer did not rerun the C# suite, disk tests or Unity.

Schema2 integration: no remaining actionable findings. The reviewer inspected23 named session cases, verified the save-destination schema/content/TestOnly compatibility guard and independently reconstructed the prior208-byte schema1 initial fixture. Its SHA-256 matched `757aa73dfb8d99113559b7e2aa5118376d1d92541b06be805e7ea710dfa6404f`. The reviewer independently calculated the largest accepted schema2 payload as1,025,126 bytes,23,450 below1MiB.

The review covered explicit schema selection; rejection of hidden work/time in schema1 and a nonzero legacy tick field in schema2; immutable ledger ownership; aggregate worker references and record bounds; authority/revocation before replay; fresh-ID settlement rejection; rollback of combined work/world/time/RNG mutations; versioned mapping and nested checksum/count/string/rational guards; restored continuation and explicit recovery. GPT separately suggested protecting incompatible existing save destinations; that guard was added with a three-way regression before final review.

Prototype clock/traversal review found two arithmetic defects:

- Exploration calculated an unrepresentable full endpoint before clamping to a valid earlier milestone. The implementation now compares the unbounded BigInteger target against the milestone before converting to RuleTime. Regression `prototype_clock_bounds_before_unrepresentable_target` distinguishes a due-now boundary, a later representable boundary and an unbounded overflowing request.
- Decimal multiplication could silently round doubled running pace even in a checked context. The implementation now compares exact coefficient/scale values and rejects an unrepresentable exact result. Regression `prototype_running_pace_rejects_decimal_precision_loss` includes both a precision-loss input and an exactly representable removable-trailing-zero input.

The reviewer confirmed both fixes and checked the three reviewed policy/test file hashes against the247/247 passing result. No further actionable findings remained within the inspected scope. The original review used a separate .NET decimal probe; expected golden bytes and maximal size were independently derived.

Limits remain explicit: schema2 is a TEST_ONLY work fixture with no actual labor credit, job completion or yield. Clock helpers accept the caller's earliest milestone and do not run a scheduler, choose initiative phases or persist round identity. Traversal calculations do not validate routes, spend actions or move bodies. Camp Greens execution, cooperative behavior, physical crash qualification and Unity remain unimplemented or untested as recorded in the handoff.
