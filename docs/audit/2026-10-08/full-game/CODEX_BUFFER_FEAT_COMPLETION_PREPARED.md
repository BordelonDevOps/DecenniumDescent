# Eight named feats — completion preparation

**Prepared, not submitted or adopted.** The form/buffer conference reviewed selected components of seven feats. Completing Soul Cage also requires the existing Lifeleech feat: its printed soul charges explicitly power Soul Cage. This is a semantic dependency supplement, not a new feat. All335 registry records remain preserved.

Questions for the later full-clause conference:

1. Chef needs an actual food quantity, ingredients/tool use, recipients, shield amount, consumption action/time, shelf life and rest eligibility. Prevent portable infinite rest-food caches while preserving the source's long-rest cooking role. Distinguish necessary food consumption from trading surplus meal items in the existing economy.
2. Inspiring Leader needs exact recipient count, self eligibility, hearing/language/range, interruption, shield amount and per-recipient refresh frequency. Preserve the printed ten minutes and Charisma13 prerequisite. Repeated speeches should not evade a shared source-family limit.
3. Empowered Summoning retains Charisma14, creation-time2PB shield, and PB on each summoned creature's first damage roll per round. Define actual summons versus bound/returned existing creatures, caster/source attribution, area damage, shared rolls, attacks versus damage ticks and multiclass companions. Do not multiply one roll's PB over all targets or refresh it by dismissal/recreation. Keep the existing shared command budget.
4. Field Medic retains Medicine training, a Bonus Action option to use a healer's kit and PB shield after actual stabilization. The reviewed Core kit use automatically stabilizes one living dying creature and consumes one actual kit use; replayed stabilization of an already Stable target is illegal. Does the feat's second sentence apply to all actual stabilization by this owner, including a Medicine Action or spell, or only the kit? State one source-faithful interpretation and any new restriction explicitly.
5. Blood Ritual retains Constitution13, level4, ten minutes and1/LR. Self offer2×level and each eligible ally offerlevel are already agreed; allies last1 hour, self uses default recipient LR. Complete target count, blood-sharing consent, presence/range/interruption, the independent curse/disease save advantage's deadline and its next-save scope. No HP loss is printed for the drop of blood. Do not grant any actual lycanthropic oath merely from its thematic prerequisite language.
6. Necrotic Affinity retains Religion proficiency OR level8. Its resistance/Reaction prevention/post-packet shield is already reviewed; complete the separate melee-hit1d6 once-per-turn and24-hour anti-resurrection clauses. Clarify own turn versus every actual turn, natural melee attacks, extra Actions, damage provenance and final killer attribution. Translate “effects of fifth level or lower” to this game's actual rank/access system, including class abilities without spell ranks. No copied kill, staged target or temporary form should create a new corpse or soul entitlement.
7. Lifeleech's necrotic spell healing requires actual damage, eligibility, target and pulse limits, excess handling and the existing Critical/healing-prohibition procedures. Its soul spark and Soul Cage capture need one owner charge pool and one entitlement per real eligible death. Preserve cap3; do not double a kill's charge from both feats. Specify party/created/summoned/revived target exclusions explicitly as new integration where absent.
8. Soul Cage requires Lifeleech OR spellcasting ability plus level8. Clarify the exact prerequisite grammar. Complete black-crystal requirements, ownership, soul consent/eligibility, capture action and timing, range/perception, competing captors, resurrection/Soul Bind interaction, soul release and charge decay. Is a charge truly the trapped soul or a residue that does not prevent resurrection? Avoid leaving that world consequence implicit.
9. Soul Cage's one-charge2d8 shield and two-charge3d8 necrotic Agony Lance need activation, target, range, DC/stat owner, save, lifetime, per-use frequency and paid-failure rules. “Disadvantage on the next healing it receives” has no defined generic healing roll: choose and label an operational conversion, not a silently assumed half-heal. Specify how fixed healing, rolled healing, stabilization, shields and resurrection interact.
10. Present full source-qualified feat objects with prerequisites, acquisition/repeatability, every action/cost/target/deadline/frequency and each clause. Preserve original and legacy text. Identify prior reviewed interfaces, genuinely new design choices and remaining external catalog dependencies. Full object drafting and bounded validation precede promotion; passing old buffer tests is not full-feat approval.


## chef
```json
{
  "id": "chef",
  "sourceObject": {
    "id": "chef",
    "name": "Chef",
    "description": "You are an accomplished cook.",
    "prerequisite": "None",
    "effect": "You can cook special food during a long rest that provides temporary hit points to your party.",
    "type": "General",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "sourceObjectSha256": "0e5b2a5c446a30438540005e0f2bc1754523b0c07f23a3d58d9738758d823de0"
}
```

## inspiring_leader
```json
{
  "id": "inspiring_leader",
  "sourceObject": {
    "id": "inspiring_leader",
    "name": "Inspiring Leader",
    "description": "You can inspire others through stirring words.",
    "prerequisite": "Charisma 13 or higher",
    "effect": "You can spend 10 minutes inspiring your companions, giving them temporary hit points.",
    "type": "General",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "sourceObjectSha256": "ccf20f2fc5f38ad47473a963c27e49c6cfd5be9d2f2da6b314d71ba583e47d3e"
}
```

## empowered_summoning
```json
{
  "id": "empowered_summoning",
  "sourceObject": {
    "id": "empowered_summoning",
    "name": "Empowered Summoning",
    "description": "A charismatic summoner calls allies with increased health and damage.",
    "prerequisite": "Charisma 14+",
    "effect": "Creatures you summon gain temporary hit points equal to twice your proficiency bonus and add your proficiency bonus to the first damage roll they make each round.",
    "type": "Magic",
    "legacyEffect": "Summoned allies +10% HP and damage",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "afba301851de043876c6bb7d07d91ea717dd38a05ef6f2609540f0588a6bc31c"
}
```

## field_medic
```json
{
  "id": "field_medic",
  "sourceObject": {
    "id": "field_medic",
    "name": "Field Medic",
    "description": "Trained medical care stabilizes allies faster during combat.",
    "prerequisite": "Trained in Medicine",
    "effect": "You may use a healer’s kit as a bonus action. When you stabilize a creature, it gains temporary hit points equal to your proficiency bonus.",
    "type": "General",
    "legacyEffect": "Stabilize allies in combat faster",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "e12c23ca62a26cc73da76870d8066b93ea9e29e1518604d0e1e76b354ebc3dab"
}
```

## blood_ritual
```json
{
  "id": "blood_ritual",
  "sourceObject": {
    "id": "blood_ritual",
    "name": "Blood Ritual",
    "description": "Under the moon's gaze you bind flesh to curse through rites older than the cities of Aethel. Prestige lineage: Mooncursed. completed from the existing development record.)",
    "prerequisite": "Constitution 13+, level 4+",
    "effect": "Once per long rest, as part of a 10-minute ritual using your blood, you gain temporary hit points equal to twice your level and advantage on the next saving throw against curse or disease effects. Required for many lycanthropic oaths. Allies who witness the ritual and share a drop of blood gain half your temporary hit points (rounded down) for 1 hour.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "Once per long rest, as part of a 10-minute ritual using your blood, you gain temporary hit points equal to twice your level and advantage on the next saving throw against curse or disease effects. Required for many lycanthropic oaths. Allies who witness the ritual and share a drop of blood gain half your temporary hit points (rounded down) for 1 hour.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "5aaa8868de08ed8e614580b12164631975ce589856efeaf5c015ab44505904f7"
}
```

## necrotic_affinity
```json
{
  "id": "necrotic_affinity",
  "sourceObject": {
    "id": "necrotic_affinity",
    "name": "Necrotic Affinity",
    "description": "Death's chill is an old friend on Aethel's battlefields—you channel grave-cold through fist and focus without flinching, as if the Binding left a door ajar in your marrow. Prestige lineage: Gravetouched. completed from the existing development record.)",
    "prerequisite": "Proficiency in Religion or level 8+",
    "effect": "You have resistance to necrotic damage. Once per turn when you hit with a melee attack, you can deal an additional 1d6 necrotic damage. When you take necrotic damage from a spell or supernatural effect, you can use your reaction to absorb half of it (rounded down) and add that amount as temporary hit points until the end of your next turn. Creatures you kill with necrotic damage cannot be raised by effects of 5th level or lower for 24 hours.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You have resistance to necrotic damage. Once per turn when you hit with a melee attack, you can deal an additional 1d6 necrotic damage. When you take necrotic damage from a spell or supernatural effect, you can use your reaction to absorb half of it (rounded down) and add that amount as temporary hit points until the end of your next turn. Creatures you kill with necrotic damage cannot be raised by effects of 5th level or lower for 24 hours.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "c179a7e4246e9e668e859a699a56179c5ae85fe69d22691d7e9fda1cfe0b23ea"
}
```

## soul_cage
```json
{
  "id": "soul_cage",
  "sourceObject": {
    "id": "soul_cage",
    "name": "Soul Cage",
    "description": "You trap the departing in black crystal—voices pressed flat until you need their scream. Prestige lineage: Soulrender. completed from the existing development record.)",
    "prerequisite": "Lifeleech or spellcasting ability, level 8+",
    "effect": "When a hostile creature dies within 30 feet, you may bind its soul to a black crystal, storing up to 3 soul charges. Spend 1 charge to shield an ally for 2d8 temporary HP, or spend 2 charges to fire an Agony Lance (3d8 necrotic, save for half, and the target has disadvantage on the next healing it receives).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When a hostile creature dies within 30 feet, you may bind its soul to a black crystal, storing up to 3 soul charges. Spend 1 charge to shield an ally for 2d8 temporary HP, or spend 2 charges to fire an Agony Lance (3d8 necrotic, save for half, and the target has disadvantage on the next healing it receives).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "34a051cc5c242b04c7a7b784acbf69249adc0042ba2a27721ba3433283c9d1fc"
}
```

## lifeleech
```json
{
  "id": "lifeleech",
  "sourceObject": {
    "id": "lifeleech",
    "name": "Lifeleech",
    "description": "Your magic does not merely harm—it siphons the vigor that death has not yet claimed. Prestige lineage: Soulrender. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability",
    "effect": "When you deal necrotic damage with a spell, you regain hit points equal to half the necrotic damage dealt. When a hostile creature dies within 30 feet, you absorb a soul spark, gaining 1 soul charge (max 3). Soul charges can power Soul Cage abilities.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you deal necrotic damage with a spell, you regain hit points equal to half the necrotic damage dealt. When a hostile creature dies within 30 feet, you absorb a soul spark, gaining 1 soul charge (max 3). Soul charges can power Soul Cage abilities.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "1ec74c9ea62fd5d8cd1ee136c1589d4b6b752b55adb162c35d54c783321fc932"
}
```
