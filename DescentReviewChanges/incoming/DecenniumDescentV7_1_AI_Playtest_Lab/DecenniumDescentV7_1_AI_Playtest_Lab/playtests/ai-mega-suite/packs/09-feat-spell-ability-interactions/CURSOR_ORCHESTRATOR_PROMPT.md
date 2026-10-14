Run the `09-feat-spell-ability-interactions` test pack.

Primary question: Which combinations create mandatory choices, invalid states, infinite loops, excessive stacking, or unusable options?

Evidence standard: Complete static scan plus targeted agent review of highest-risk combinations.

Read the pack README, agent roster, source manifest, scenario matrix, and result schema. Create separate agents. Freeze fixtures before revealing opposition. Run every scenario. Store raw results in this pack's `results/` directory. Do not edit canon. Record RULES_HALT events. Compile the report with `python compile_results.py`.
