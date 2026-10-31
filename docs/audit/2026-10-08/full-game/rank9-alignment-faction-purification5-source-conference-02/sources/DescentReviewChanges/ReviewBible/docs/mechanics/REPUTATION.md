# Reputation — Canon Interaction Rules

**Status:** Playable canon

Reputation records how Aethel's institutions respond to the character. It is not a morality score and it is not a hidden multiplier on the laws of magic.

## Scale

Faction standing is stored as `{ [factionId]: score }` on the character save, normally from **−3 (Hated)** through **+3 (Honored)**. Backgrounds and play can set or change starting standing.

## What reputation can change

A faction may change:

- prices, credit, insurance, salvage rights, and expedition sponsorship;
- access to restricted libraries, teachers, rituals, recipes, laboratories, temples, circles, and sanctuaries;
- information quality, contacts, safe houses, legal treatment, hostility, and political support;
- availability of a **named** focus, training feature, consumable, or scene benefit whose rules are written explicitly.

## What reputation does not change automatically

Reputation does **not** silently modify:

- a spell's Resonance Rank;
- base RP cost;
- natural maximum RP;
- Dissonance gained from a cast;
- the Frayed / Discordant / Fractured thresholds;
- a character's moral alignment.

If a guild teaches a cheaper technique or a shrine grants a recovery boon, that is an explicit earned benefit, not proof that the Weave itself favors members of that institution.

## Magic connection

The universal magic rules are in [`RESONANCE_CANON.md`](./RESONANCE_CANON.md). Faction standing can provide **tools for dealing with magic**, but never rewrites the underlying resonance law merely because the character is liked or hated.

## Companion implementation

- `src/data/reputation.js` owns faction definitions and starting standing.
- `character-storage.js` persists the reputation map.
- `resonance-economy.js` retains compatibility helper names for old saves/code, but automatic reputation-to-RP and reputation-to-spell-cost modifiers return **0** under current canon.

This separation is deliberate: institutions matter socially and materially; Resonance/Dissonance remain metaphysical rules.
