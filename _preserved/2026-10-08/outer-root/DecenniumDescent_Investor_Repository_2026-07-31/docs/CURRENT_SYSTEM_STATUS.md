# Current System Status

**Snapshot:** 2026-07-31 investor/distributable pass.

## Product Material

| Area | Current state |
|---|---|
| Player Rulebook | Active compiled book; 17-class roster; race/class progression; Resonance terminology; current Appendix B framing |
| Director's Crucible | Active authoritative Director book; public-vs-secret cosmology, Heartcell, Matrix, Unity/false resonance guardrails |
| Director supplements | Instruments and Chronicle active; Codex/Bestiary retained as clearly labeled development volumes; deep-tier gazetteer and operational toolkits active |
| Dungeon | 100-floor / 10-tier framework; 100-day Opening; day-50 Horn |
| Classes | 17 selectable base classes; Arch/Hero progression; companion data mirrors current ethos terminology |
| Peoples | 14 player peoples with variants; Player Rulebook now connects each people to the Decennial Opening |
| Magic | Resonance Points for Weave casters; class-specific alternatives such as Oracle Revelation Charges retained |
| Bestiary | Structured Excel source + metadata source + generated companion JSON. Aethel naming/ecology work is active; many ordinary creature shells remain compatibility/prototype development material and are not final commercial copy. |
| Crafting | Validated Excel source + companion structured data |
| Playtesting | Curated expedition, tier, newcomer, balance, and simulation reports retained in `docs/playtest/` |
| Companion app | Next.js/React source with character, spell, monster, item, crafting, dungeon, and session tooling |

## Theme Propagation Completed in This Snapshot

- public Crucible history remains player-facing while Director truth preserves the older Heartcell layer;
- Matrix principles are now an explicit Director design grammar;
- goblin culture is tied to expedition finance and contested crusade history without exposing Unity to players;
- Director canon now contains goblin susceptibility, Moloch/Coinfather exploitation, false resonance, and anti-collective-guilt guardrails;
- Hero Paths are framed as philosophies/methods rather than Good/Neutral/Evil verdicts;
- retired Fighter chapter removed from the compiled Player Rulebook; 17 classes are authoritative;
- remaining stock named-spell and external-rulebook references in the compiled Player Rulebook were scrubbed or rewritten;
- retained Director sister books use Umbrin terminology consistently.

## Engineering Verification

- TypeScript `tsc --noEmit`: **passed before the dependency-cache cleanup** performed for this distributable package. The final repository intentionally omits `node_modules`, so lint/build checks require `npm ci` first.
- `npm run build`: source compilation could not be completed inside the packaging sandbox because Next.js attempted to download a platform SWC binary and the sandbox package mirror returned 404. A normal connected development machine should run `npm ci && npm run lint && npm run build` as the release check.

## Current Development Priorities

The remaining work is refinement rather than a missing core premise:

1. finish any class/path entries still explicitly marked draft in structured data;
2. complete the bestiary publication pass: replace compatibility/prototype creature shells with independently authored Aethel creatures, then finish combat-stat authoring and balance;
3. deepen Floors 51–100 encounter specificity while preserving Matrix design pressure;
4. continue visual/layout publication work for the books;
5. run wider human table playtests beyond simulation-driven stress tests;
6. harden the companion for deployment, persistence, and future account/campaign integration.

See `docs/MECHANICS_ROADMAP.md` and `docs/mechanics/RULESET_VULNERABILITIES.md` for the deeper technical backlog.
