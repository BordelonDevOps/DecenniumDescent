# Resonance Architecture Decision

**Status:** Resolved canon. The live rules use the **Resonance Point (RP)** system summarized in [`RESONANCE_CANON.md`](./RESONANCE_CANON.md).

This file records the design rationale without preserving superseded parallel magic systems as if they were still candidates.

## Decision

Decennium Descent uses a **single Resonance Point pool** for Weave casters. It does not use a generic multiclass spell-slot pool.

Core principles:

1. **Spells cost RP.** Cost scales from spell level and may be modified by affinity, specialization, reputation, and other authored class features.
2. **Resonance is a setting mechanic, not a rename.** Casting represents a character forcing, harmonizing with, or reshaping the Weave.
3. **Recovery matters.** Long-rest recovery is the baseline; authored class/subclass features may provide constrained short-rest or other recovery.
4. **Overcasting is part of the identity.** Additional RP can alter a spell when a feature or rule explicitly permits it.
5. **Class resources remain distinct.** Crescendo, Momentum, Blood Gauge, Revelation Charges, and similar resources are not silently converted into RP.
6. **Oracle is an explicit exception.** Oracle uses **Revelation Charges** and Mystery/Curse mechanics, not RP.
7. **No hidden slot layer.** “Slot” may still describe storage capacity in a non-spell mechanic (for example an Echo storage slot), but it is not the default Weave-casting currency.

## Why this model won

The RP architecture better supports the project's defining themes:

- **Resonance has metaphysical meaning.** It ties ordinary spellcasting to the same vocabulary as the First Song, Heartcell, false resonance, and the Matrix.
- **Player choice is visible.** A fungible pool creates meaningful decisions about conserving, pushing, retuning, and overcasting.
- **Reputation and identity can matter mechanically.** The system can make relationships with factions, schools, environments, or disciplines alter how efficiently a caster touches the Weave.
- **The companion can calculate the difficult parts.** The digital tool can expose a clean current/max RP interface while handling authored modifiers behind it.

## Implementation rule

When a current document and an older note conflict, use this order:

1. `RESONANCE_CANON.md`
2. Player Rulebook
3. current class-specific rules
4. companion implementation
5. older playtest/design commentary

Legacy spell-slot wording should be treated as migration residue and removed when encountered in live product material.

## Open engineering work

The design decision is closed, but implementation can still improve:

- multiclass RP reconciliation;
- automatic reputation/affinity modifiers;
- overcast UI and validation;
- clearer class-specific RP pool presentation;
- balance testing at low and high levels.

These are implementation questions, not a reopening of the underlying magic-system decision.
