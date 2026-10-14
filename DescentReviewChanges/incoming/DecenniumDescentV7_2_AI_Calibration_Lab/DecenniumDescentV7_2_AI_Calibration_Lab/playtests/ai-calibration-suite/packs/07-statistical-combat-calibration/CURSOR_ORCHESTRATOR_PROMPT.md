Run the `07-statistical-combat-calibration` test pack.

Primary question: Do hit chances, damage, healing, resource curves, and survival rates behave consistently across levels before full class complexity is added?

Evidence standard: Executable seeded Monte Carlo with frozen baseline fixtures and confidence intervals.

Read the pack README, agent roster, source manifest, scenario matrix, and result schema. Create separate agents. Freeze fixtures before revealing opposition. Run every scenario. Store raw results in this pack's `results/` directory. Do not edit canon. Record RULES_HALT events. Compile the report with `python compile_results.py`.
