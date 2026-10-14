# Notebook scope explanation after owner question

The initial review was interrupted by the owner asking what was being checked. This completed reply explains scope; it contains no independent findings or approval.

ChatGPT said:

I’m checking whether the bounded Time Loop kernel itself can produce a wrong state even when all seven missing integrations are absent.

Specifically:

Atomicity: whether preflight can pass, then commit partially mutates state before failing; whether stale plans, replaced objects, new fields, or changed registries are caught before any Time Loop cost/state is committed.
Reaction/resource conservation: whether multiple Oracles can accidentally regain Reactions or 1/LR uses; whether RC/per-encounter state rewinds without also refunding RP, consumables, rest uses, recharge clocks, or elapsed time.
Iteration identity: whether the new round/turn IDs are genuinely fresh while historical event IDs stay permanently reserved, so you can reuse encounter abilities without duplicating rewards/resources.
One-shot effects: especially Agony. I’m checking that an effect available at the snapshot can become available again in the new timeline without deleting evidence that it was consumed in the discarded timeline, while an effect already consumed at the snapshot stays consumed.
HP / maximum HP / death state: whether snapshot HP is restored against the current legal max HP, not stale gear/progression; whether Stable recovery or Soul Bind absolute deadlines can accidentally replay; and whether Time Loop creates fake healing, resurrection, damage, or death triggers.
Physical conservation: whether restoring a body or structure can leave behind a harvested part, raised corpse, crafted derivative, transferred item, or persistent slot and thereby duplicate matter; also whether it can wrongly erase legitimate current inventory.
Geometry: in the finite ground-plane model only, whether participant restoration can overlap outsiders, remove their support, trap/enclose them, or change their reachable space without direct overlap.
External effects: whether an outside caster's concentration, max-HP effect, or other current external record is silently erased or recreated.
Memory: whether only the invoking Oracle and snapshot allies retain actually perceived information, with no hidden-roster leakage.
Scope honesty: whether the guide/code claims anything beyond what is actually implemented. In particular, playable_plan() must remain blocked, unsupported holders must reject, and the seven missing integrations must remain visibly missing.

What I am not checking yet is whether Druid forms, transformations, CreatureWorld, devices, RemainingWorld, FeatWorld, or control/pulse systems work through Time Loop. Those are explicitly the next adapters. Right now I’m looking for defects in the foundation they will plug into.
