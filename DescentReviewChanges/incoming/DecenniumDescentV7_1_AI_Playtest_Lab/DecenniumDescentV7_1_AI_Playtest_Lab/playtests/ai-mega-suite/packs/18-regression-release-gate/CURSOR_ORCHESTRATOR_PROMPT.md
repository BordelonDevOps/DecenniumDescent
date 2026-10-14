Run the `18-regression-release-gate` test pack.

Primary question: After a proposed patch, did a targeted fix introduce new combat, expedition, economy, canon, data, or usability failures?

Evidence standard: Baseline metric comparison and complete repository validators.

Read the pack README, agent roster, source manifest, scenario matrix, and result schema. Create separate agents. Freeze fixtures before revealing opposition. Run every scenario. Store raw results in this pack's `results/` directory. Do not edit canon. Record RULES_HALT events. Compile the report with `python compile_results.py`.
