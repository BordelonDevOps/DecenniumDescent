# Tabletop and engine design standard recorded in Calibration Review

Owner message in the notebook:

> I want the systems ready to be on a TTRPG or developed into a video game

Complete notebook reply:

That should be the design standard for the entire project.

Every mechanic should ultimately exist in **two synchronized forms**:

- a **tabletop-facing rule** that a player or Director can read and run without software;
- a **deterministic engine rule** precise enough that Codex could implement it in a video game without having to guess what the designer meant.

For every ability, spell, feat, condition, device, summon, zone, resource, and combat interaction, I’ll therefore keep pushing for the same minimum contract:

1. **Source identity** — exact card/engine/feat ID; no invented content.
2. **Activation and cost** — Action, BA, Reaction, resource spend, limited use, prerequisites.
3. **Target legality** — who/what can be affected, range, LOS/LOE, willingness, creature/object type.
4. **Timing** — exact event stage, regular-turn marker, round marker, expiry, upkeep, extra-turn behavior.
5. **State changes** — HP, temp HP, maximum HP, conditions, disabled/destroyed/retracted/etc.
6. **Stacking/arbitration** — strongest, additive, replacement, same-name handling, cross-owner handling.
7. **Trigger provenance** — what counts as damage, healing, attack hit, transfer, copy, destruction, resource event.
8. **Lifecycle** — creation, active state, suppression, destruction, repair, replacement, expiry, reconstruction.
9. **Edge cases** — 0 damage, 0 healing, max1 HP, dead/downed targets, missing resources, simultaneous effects.
10. **Machine invariants/tests** — conservation rules, replay protection, caps, no recursion, no duplicate entitlements.
11. **Human wording** — the same mechanic still needs to be understandable at a physical table without exposing internal implementation jargon.

The important part is that the video-game implementation should **not become a second ruleset**. The executable model should be a formalization of the tabletop rule, with explicit NEW integration rulings only where the written material genuinely leaves an ambiguity.

That is also why I’ve been resisting “close enough” interpretations. A human GM can improvise around a vague sentence; a game engine cannot. If we resolve the ambiguity now, the same canon can drive the rulebook, character builder, encounter simulator, VTT automation, and eventually a full video game.

