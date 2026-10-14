# EX58-X01 — verified submitted source excerpts

All locations and hashes below are from the immutable submission. They are source evidence, not newly authored class or spell rules.

## `DescentReviewChanges/ReviewBible/docs/mechanics/classes/mage.md`
SHA256 `08643cfdef39016b1882ea9efd2e03077ced71db97bf0b048271570e356d0d0b`
Submitted lines 66–75:

```text
L66: ## Advancement and resources
L67: 
L68: RP authority: Direct Core Systems V2 table. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.
L69: 
L70: | Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
L71: |---:|---|---:|---:|---|
L72: | 1 | Base | 3 | 1 | Choose 4 Base; at least 2 active; automatic: Spellcasting, Resonance Pool |
L73: | 2 | Base | 5 | 1 | Choose 2 Base; automatic: Fire (Fire), Cold (Cold), Lightning (Lightning) |
L74: | 3 | Arch | 8 | 2 | Choose 2 Arch; at least 1 active |
L75: | 4 | Arch | 10 | 2 | Choose 1 Base/Arch; ASI or feat |
```

## `DescentReviewChanges/ReviewBible/docs/mechanics/classes/dragoon.md`
SHA256 `b5dfdfde3146afb3f54ed5701540f0f93c12271b088afd73ccbfbbacf3091aa1`
Submitted lines 28–50:

```text
L28: Spending Momentum pays before resolution; a hit refund cannot pay its own activation. Burn means 1d4 fire at start of target's next 2 turns, nonstacking. Bleed means 1d4 physical at start of next 2 turns; an Action with a healer's kit ends it. Do Ts give no Momentum or critical triggers. Hard denial uses the shared once-per-target/encounter guard.
L29: 
L30: When casting an ordinary spell after moving at least 20 ft this turn, reduce that cast's Dissonance gain by 1, minimum 0; no automatic RP discount. Dragoon techniques are martial unless their card specifies elemental magic. Use Core V 2 RP and the Dragoon rank gates for separate spellcasting.
L31: 
L32: Use scheduled Base/Arch/Hero choices. Skybound Assault, Momentum Engine and related passives improve the automatic engine rather than unlock basic movement or generation. Lancer's Apex is automatic 9; at 10 choose Dragon Guardian, Drake Rider or Dragon Tyrant. The corresponding Final Flight is automatic 20. Apex Assault is an active technique despite its source passive heading.
L33: 
L34: **Protected source interface:** If the Dragoon moved at least 20 feet before a Weave cast, reduce that cast's Dissonance gain by 1 (minimum 0); Momentum carries the note through motion.
L35: 
L36: ## Advancement and resources
L37: 
L38: RP authority: Explicit fallback: Cleric CoreV2 curve ×0.35, halves upward. Rank access is separate from RP capacity. ASI/feat milestones follow general advancement and are not duplicated by a card.
L39: 
L40: | Class level | Stage | RP maximum | Max ordinary spell rank | Class choices / automatic grants |
L41: |---:|---|---:|---:|---|
L42: | 1 | Base | 1 | 0 | Choose 4 Base; at least 2 active |
L43: | 2 | Base | 1 | 0 | Choose 2 Base |
L44: | 3 | Arch | 2 | 1 | Choose 2 Arch; at least 1 active |
L45: | 4 | Arch | 3 | 1 | Choose 1 Base/Arch; ASI or feat |
L46: | 5 | Arch | 4 | 1 | Choose 1 Arch |
L47: | 6 | Arch | 5 | 1 | Choose 1 Base/Arch |
L48: | 7 | Arch | 6 | 1 | Choose 1 Arch |
L49: | 8 | Arch | 7 | 2 | Choose 1 Base/Arch; ASI or feat |
L50: | 9 | Arch | 8 | 2 | Choose 1 Arch; automatic: Lancer's Apex |
```

## Actual submitted EX-W13 record
File: `DescentReviewChanges/ReviewBible/data/public/expedition_candidate/boundary_records.json`
SHA256 `d7617ed8e13b359ddee4c7d65912259a1896f815cb2e211875f52ec3fe93de04`
Pointer: `/cases/12`.
The current premise fixes the Mage at class level3 and Dragoon at class level8 and asserts no pending feat. Its two source-bound pools nevertheless begin at10RP without an increase to either actual maximum.

```json
{
  "actualSyntheticPremises": "A level-8 Dragoon has genuinely acquired Featherstep. A level-3 Mage ally already cast and maintains actual Swiftness, legally raising the Dragoon’s walking Speed from 30 to 40 for its minute. No pending feat is used.",
  "ongoingEffect": {
    "spellId": "swiftness",
    "sourceCardIndex": 71,
    "caster": "Mage ally",
    "classLevel": 3,
    "castAtSeconds": 0,
    "expiresAtSeconds": 60,
    "ActionSpent": true,
    "RPBefore": 10,
    "RPAfter": 7,
    "DissonanceBefore": 0,
    "DissonanceAfter": 1,
    "components": "actual voice, manipulating hand and held legal focus",
    "willingTarget": "Dragoon",
    "initialDistanceFt": 10,
    "concentrationHeld": true
  },
  "ownTurn": {
    "atSeconds": 12,
    "walkingSpeedFt": 40,
    "dismountCostFt": 20,
    "actualSelfPoweredPathFt": 20,
    "remainingMovementFt": 0,
    "MomentumBefore": 0,
    "MomentumFromMovement": 1,
    "MomentumAfter": 1,
    "weaponHit": false,
    "Action": "Featherstep on willing self",
    "spellRank": 1,
    "classLevel": 8,
    "requiredMinimumClassLevel": 3,
    "STRModifier": 4,
    "PB": 3,
    "DissonanceLimit": 9,
    "RPBefore": 10,
    "RPPrice": 2,
    "RPAfter": 8,
    "previousSpellName": "a different identity; Refrain0",
    "DissonanceBefore": 2,
    "baseGain": 1,
    "movementReduction": 1,
    "finalGain": 0,
    "DissonanceAfter": 2,
    "components": "usable voice, legal held focus, free manipulating hand after dismount; no weapon attack also claimed",
    "newConcentration": "Dragoon holds Featherstep; ally independently retains Swiftness",
    "targetMassWithGearLb": 170,
    "actualEffect": "only the full Featherstep card; no empty-gap flight or added Speed"
  }
}
```

## Exact disposition
The class tables remain unchanged. Change only the current example: Mage8−3=5 and Dragoon7−2=5. No RP reduction is obtained from movement. The original expected movement, Momentum, Dissonance and spell outcomes remain valid. The complete exact replacement and every current representation are in EX58_X01_CORRECTIONS.json.
