# Short Rest verification status

Implementation commit: `44837a2ed2be8a558ca6d37544621dac6400ab9d` on `Engine`.

- The expanded registered connected case passes, including exact accepted arrival, independent expiry, pending/interrupted restore, full restart, cadence, current authority and forgery controls, and byte-identical public C# replay. [Focused report](compile/headless.json)
- C# 9 standalone compilation and all static package checks pass. Every report source hash was checked against the committed engine archive before retention. [Standalone](compile/standalone.json) · [Static](compile/static.json) · [Exact bindings](FOCUSED_BINDINGS.json)
- The full exact regression is running as `98b14ad829504931b5fb54d1d3fe91a9`: all 1,498 accepted predecessor names in their existing order plus the registered Short Rest case. Six processes use copied, hash-bound assemblies and assignments. Completion has not yet been claimed.
- All three public console histories pass. Their 75 checkpoints match restored console, uninterrupted console and direct public C#. The partitioned and whole-hour branches agree on causal deadlines, gameplay outcomes and RNG. Authentic wire96–102 saves round-trip and continue byte-identically, and both complete wire95 default/Fishing Trap console transcripts match their accepted references. [Public results](public/results.json) · [Prior profiles](prior/results.json) · [Wire95 connected results](connected/results.json) · [Exact packet bindings](BINDINGS.json)
- GPT has been asked to review committed source and focused evidence while the exact regression runs. The source/API approval remains distinct from implementation acceptance. The pending full regression must finish before acceptance or a successor.

The retained failed development probes are historical diagnostics, not final passes. The first differed from the approved public combat sequence; the second omitted the required explicit clock advance before applying a detached test condition. Both test probes were corrected and the expanded focused case then passed. No successor module has started.
