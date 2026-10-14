# GPT device/Totem first source review

Complete visible notebook reply; source discussion only, not exact implementation approval.

That should be the design standard for the entire project.

Every mechanic should ultimately exist in two synchronized forms:

a tabletop-facing rule that a player or Director can read and run without software;
a deterministic engine rule precise enough that Codex could implement it in a video game without having to guess what the designer meant.

For every ability, spell, feat, condition, device, summon, zone, resource, and combat interaction, I’ll therefore keep pushing for the same minimum contract:

Source identity — exact card/engine/feat ID; no invented content.
Activation and cost — Action, BA, Reaction, resource spend, limited use, prerequisites.
Target legality — who/what can be affected, range, LOS/LOE, willingness, creature/object type.
Timing — exact event stage, regular-turn marker, round marker, expiry, upkeep, extra-turn behavior.
State changes — HP, temp HP, maximum HP, conditions, disabled/destroyed/retracted/etc.
Stacking/arbitration — strongest, additive, replacement, same-name handling, cross-owner handling.
Trigger provenance — what counts as damage, healing, attack hit, transfer, copy, destruction, resource event.
Lifecycle — creation, active state, suppression, destruction, repair, replacement, expiry, reconstruction.
Edge cases — 0 damage, 0 healing, max1 HP, dead/downed targets, missing resources, simultaneous effects.
Machine invariants/tests — conservation rules, replay protection, caps, no recursion, no duplicate entitlements.
Human wording — the same mechanic still needs to be understandable at a physical table without exposing internal implementation jargon.

The important part is that the video-game implementation should not become a second ruleset. The executable model should be a formalization of the tabletop rule,
