# DI7 Shaman casting interface

KEEP / existing-source clarification. Source ruling: [DI7-SHAMAN-VENT-01](../../../../../docs/audit/2026-10-08/full-game/DI7_SHAMAN_VENT_RECEIVED.json).

DI7-SHAMAN-VENT-01 — Shaman vent checkpoint. Evaluate the Shaman’s once-per-round ordinary-spell totem vent at casting-sequence step 5, after step 4 has committed the cast and established any required concentration, ending incompatible prior concentration. Use the caster’s actual position, the actual ownership and active state of the totem aura, this cast’s qualifying ordinary Shaman spell route, and that Shaman’s existing once-per-round use history at this checkpoint. Do not retain a pre-commit aura snapshot.

The first qualifying ordinary spell cast while inside at least one of that Shaman’s own still-active totem auras automatically occupies the round’s opportunity and generates 1 less Dissonance, minimum 0. This remains the first qualifying cast even when its generated Dissonance was already 0; it does not remove accumulated Dissonance or preserve the opportunity for a later spell. An earlier cast outside an own active aura, or through an excluded route, does not occupy this opportunity.

Establishing incompatible concentration at step 4 ends the shared totem burden and its auras before this determination. That cast therefore receives no totem vent and does not occupy the first-inside opportunity. A later counter, failed result, aura restoration or movement does not replay the checkpoint, refund an occupied opportunity or restore displaced concentration. Multiple own overlapping totems provide only one reduction and share the Shaman’s one round opportunity; another Shaman’s aura does not qualify.

An ordinary Fate Echo outer cast may qualify independently. Its fate-echo-copy child is not an ordinary learned Shaman spell and neither receives nor occupies this ordinary-spell-only vent. A concentration-requiring child ends incompatible totems at its own commitment, without undoing the outer cast’s earlier valid vent. A readied outer cast must account for its actual held-spell concentration; a nonconcentration payload does not exempt its Ready hold from concentration displacement. Release supplies no second outer casting or vent checkpoint.

The vent grants no RP reduction, does not revise already committed RP, and cannot bypass pre-commit casting restrictions. Fate’s required forecast and later child revalidation still use the actual chronological strain and resource state under their existing rules. The existing source-governed round boundary remains unchanged.

These source-derived expectations do not certify execution, exact seven-card acceptance or full runtime.
