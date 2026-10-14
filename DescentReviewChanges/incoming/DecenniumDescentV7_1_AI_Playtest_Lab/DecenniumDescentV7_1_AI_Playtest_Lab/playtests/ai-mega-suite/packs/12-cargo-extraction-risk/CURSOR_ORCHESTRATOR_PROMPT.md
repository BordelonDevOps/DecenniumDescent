Run the `12-cargo-extraction-risk` test pack.

Primary question: Do Load, capacity, Extraction Class, Attention, Mapping, and cargo priorities create rational tradeoffs without making profit arbitrary?

Evidence standard: Large seeded route/cargo matrix with loss, delay, casualty, and profit distributions.

Read the pack README, agent roster, source manifest, scenario matrix, and result schema. Create separate agents. Freeze fixtures before revealing opposition. Run every scenario. Store raw results in this pack's `results/` directory. Do not edit canon. Record RULES_HALT events. Compile the report with `python compile_results.py`.
