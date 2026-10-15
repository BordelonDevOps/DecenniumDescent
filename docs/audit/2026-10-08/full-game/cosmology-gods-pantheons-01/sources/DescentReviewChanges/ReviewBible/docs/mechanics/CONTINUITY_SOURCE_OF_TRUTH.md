# Continuity — Source of Truth (ReviewBible pack)

**Status:** Compact pack pointer — updated 2026-08-05 (canon manifest lock).  
**This file does not independently own domain or override facts.**

## Sync model (owner lock 2026-08-05 §1)

1. **Owner spoken lock** — intent only; not auto-edit of locked books.
2. **`docs/canon/CANON_MANIFEST.json`** (main repo; dual-written under `DescentReviewChanges/docs/canon/`) — single registry of domain → authoritative file(s).
3. **Domain authoritative files** listed in the manifest (Core Systems, Crafting v4, MM Canon Rewrite packs, feats registry, Player Rulebook domains, etc.).
4. **This ReviewBible pack** — assembled review build (main baseline + promoted changes). Open books here for audits.
5. **Main ops protocol** — `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` (STOP-and-ask + Q-OV tracker). Ops only; not a second copy of domain rules.
6. Playtests / experiments — never silent promotion to canon.

Promotion hierarchy: `docs/canon/REPOSITORY_PROMOTION.md`  
Incoming packs: `DescentReviewChanges/incoming/`

## Authoritative books in this pack (when not reassigned by manifest)

- Player: `decennium descent player rulebook.docx`
- Director: `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx`

Supporting briefs in this pack (`docs/canon/*`, `docs/mechanics/*_CANON.md`) are **implementation / thematic aids**. If they conflict with a registered domain bible or the Player/Director books, follow the manifest + STOP-and-ask gate — do not treat this compact file as a second SoT.

## Locked baselines (mirrored summary — owned elsewhere)

These numbers are **mirrored for pack convenience**. Canonical ownership: main ops tracker `locked-baselines` domain in `CANON_MANIFEST.json` + published books / domain bibles. **Do not diverge this list independently.**

- Opening: **2,400 hours / 100 days**
- Horn / point of no return: **1,200 hours / day 50**
- Dungeon: **100 floors / 10 tiers**
- Expedition max: **12 characters** per Expedition (Q-OV-2 closed). T4 24-PC sims = playtest only.
- **Level 97 / Old God:** Director crystal-path dual-layer (2026-08-05) — see main ops Continuity §5 Q6; public knowledge ends at failed Sixth Gate.
- Selectable base classes: **17**
- Fighter/Swashbuckler: legacy aliases only
- Umbrin: current product term
- Weave casters: **Resonance Points**
- Oracle: Revelation Charges
- Appendix B: mortal religion/cosmography, not omniscient proof
- Player public origin: Calan'thir + Asmodeus / Crucible
- Director deep origin: Silent Ones/Old Ones / Heartcell
- Unity: false resonance
- Goblin Unity susceptibility: Director truth, never racial morality

## Drift

When main working-tree books lag this assembled pack for material **not** reassigned by the manifest, prefer this pack. When the manifest registers a newer domain bible (e.g. Core Systems, Crafting v4), that domain file wins over stale pack or main copies until promotion completes.

## Change discipline

1. Check `CANON_MANIFEST.json` for which file owns the fact.
2. Edit the authoritative domain file / book first (or stage in `incoming/` if new).
3. Propagate into structured data and UI.
4. Promote per `REPOSITORY_PROMOTION.md` — never auto-approve root drops into this pack.
