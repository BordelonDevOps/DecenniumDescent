Run the `16-rules-fuzz-property-tests` test pack.

Primary question: Can randomly generated legal states violate invariants, produce impossible resources, leak hidden canon, or make the gameplay loop unable to advance?

Evidence standard: Executable property tests over at least one hundred thousand generated state transitions.

Read the pack README, agent roster, source manifest, scenario matrix, and result schema. Create separate agents. Freeze fixtures before revealing opposition. Run every scenario. Store raw results in this pack's `results/` directory. Do not edit canon. Record RULES_HALT events. Compile the report with `python compile_results.py`.
