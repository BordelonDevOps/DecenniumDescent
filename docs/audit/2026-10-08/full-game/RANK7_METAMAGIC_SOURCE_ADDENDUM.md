# Rank-seven Meta Surge — class and feat source addendum

Prepared, unsent source evidence. No spell or feat is approved by this addendum.

Meta Surge promises that all metamagic effects cost no extra resources for one minute. Its mechanical review must explicitly reconcile that promise with actual native modifiers, rather than import a sorcery-point subsystem.

The current Mage Arch Metaspell Access card costs zero, permits one permanently selected Reach/Widen/Sculpt mode and is usable once per long rest. The source feat Metamagic Adept promises two options and two sorcery points but remains pending full review. The prepared MF-22 question explicitly leaves option definitions, costs, recovery and combination unresolved.

Required decisions: identify exactly which effects qualify; distinguish a price from a selection or frequency gate; determine whether the spell waives points, RP surcharges or limited-use expenditures; preserve the underlying spell costs and source-event chronology unless explicitly changed. Do not refill already spent points, grant unselected modes or silently make the printed waiver ineffective. The complete existing card, original feat and prior question are retained below.

## Complete current Mage card

```json
{
  "id": "mage.arch.metaspell-access",
  "name": "Metaspell Access",
  "className": "Mage",
  "band": "Arch",
  "path": null,
  "sourceKind": "passive",
  "minimumClassLevel": 5,
  "acquisition": "selection",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "One Mage spell you are beginning to cast",
  "duration": "For that spell",
  "frequency": "1/long rest; choose one metamagic mode when this feature is acquired",
  "effect": "Metaspell Access. Tags: arcanist, metamagic. Choose one mode permanently: Reach increases one spell's range by 30 feet; Widen increases one circular radius or cone length by 5 feet; Sculpt lets up to M creatures automatically succeed on that spell's initial area save and take no damage if success normally halves damage. Apply the chosen mode once per long rest before casting; it does not alter RP cost or create another cast.",
  "source": {
    "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
    "line": 2915,
    "originalText": "Metaspell Access: Choose one Universal Metamagic effect to apply to a spell once per day."
  },
  "designStatus": "provisional-playtest",
  "spellRank": null
}
```

## Complete original feat

```json
{
  "id": "metamagicAdept",
  "name": "Metamagic Adept",
  "description": "You have learned to modify your spells in subtle ways.",
  "prerequisite": "Spellcasting ability, Level 4",
  "effect": "Learn 2 metamagic options, gain 2 sorcery points",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

## Existing MF-22 source question

```json
{
  "featId": "metamagicAdept",
  "questionId": "MF-22",
  "sourceObject": {
    "id": "metamagicAdept",
    "name": "Metamagic Adept",
    "description": "You have learned to modify your spells in subtle ways.",
    "prerequisite": "Spellcasting ability, Level 4",
    "effect": "Learn 2 metamagic options, gain 2 sorcery points",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "sourceObjectSha256": "6789eefb5394fffc5e00aeb163e3ca3428ba6332670027c2c426648730fcf615",
  "fullClauseQuestion": "Preserve two selected metamagic options and two sorcery points, but neither a point-to-RP exchange nor an imported external option list is authorized. Compare the complete provisional Mage Metaspell Access card; explicitly resolve feat option identities, costs, recovery, timing and combining modes. A matching metamagic tag does not grant class acquisition or convert one-per-rest uses into points.",
  "currentOperationalStatus": "full-feat-review-pending"
}
```

