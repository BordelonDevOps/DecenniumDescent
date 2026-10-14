# Eight named feats — full-clause source conference

**Prepared conference packet; submission is recorded only after visible browser confirmation. No feat is promoted by this packet.** The form/buffer conference reviewed selected components of seven feats. Completing Soul Cage also requires the existing Lifeleech feat: its printed soul charges explicitly power Soul Cage. This is a semantic dependency supplement, not a new feat. All335 registry records remain preserved.

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

## Existing reviewed interfaces — preserve these while completing missing clauses


### docs/mechanics/FORM_TEMP_HP_PLAYTEST.md

File SHA256: b1b418b9ea9725e42f3c82d7abd41d049d4d534b6497cccc836b6ce250510096

Line91: Empowered Summoning offers2PB at actual creation, using default lifetime and removal if the recipient entity ends; later PB changes do not refill it. Field Medic's actual healer-kit stabilization happens first, then itsPB grant. Blood Ritual offers2×level to self and exactlylevel to each eligible witnessing/blood-sharing ally, independent of whatever shield wins the self comparison. Allies' lifetime is1 hour; self uses default. No HP payment is invented for a drop of blood. Blood Ritual target-count completion remains visible. Chef, Inspiring Leader and Soul Cage need their named completion batches; no unknown quantities or “healing disadvantage” are silently filled in.

Line93: **Necrotic Affinity's new pipeline bridge:** after ordinary defenses and passive necrotic resistance, letD be qualifying spell/supernatural necrotic damage before existing temporary HP. A legal Reaction preventsfloor(D/2). Existing shields then absorb the remaining packet, and ordinary HP/death/Wounds/prevention settle. If still a legal living holder, offerfloor(D/2) afterward until the holder's next regular end. This is prevention, not healing/transfer. D=1 can spend the Reaction but creates no grant. An actual death creates no corpse shield; living0 can receive it without stabilization. The event may invoke this transaction only once. Other feat clauses are outside this selected component review.


### docs/mechanics/HEALING_DEATH_PLAYTEST.md

File SHA256: 8d68794687b97da70aaff9953f9724e31e9fa3c8568fd4c2f9e8fd05d34c93f7

Line28: | actualHpDamage | NormalHP lost to the packet after true prevention; recovery and state-assignment loss excluded |

Line29: | actualDamageDealt | NEW anti-overkill bridge: tempAbsorbed plus actualHpDamage; numeric actual-damage drains/reflections |

Line31: Ordinary “damages,” “takes damage” and “damaging hit” predicates use a positive resolved packet. Actual-HP wording (Burning Blood/Rewind Wound) uses actualHpDamage. Numeric actual-damage wording (Sanguine Rite/Echo Leech/Merciful Smite/Wound Eater/Gravebrand) uses actualDamageDealt. Source attack/hit predicates remain distinct.

Line33: Example: HP10/temp10 takes5: numeric actual damage5, actualHP damage0, positive packet. HP1 under a floor takes5: numeric0 but positive packet. HP3 takes12: numeric3, raw post-temp12. HP0 takes1: numeric0, positive packet and normal death-failure consequences.

Line74: Within each permitted reduction plan: formula/bonuses; per-die adjustments; compatible exact fractional multipliers with one floor after multiplication; compatible flat reductions; floor at0; broad HP prohibition; maximum/Critical/reserve caps. Intrinsic Wound Eater and systemic Corrupted remain independent factors. Duplicate same-stat per-die penalties use the strongest. Dice remain dice when maximized/shared; flat Lay on Hands and stored numeric Echoes have zero healing dice.

Line78: Every present, operative, applicable next-positive-healing reduction consumes exactly once when the final event commits if its pre-reduction HP potential was positive. This includes reducers whose arithmetic branch lost to Totem or whose actual gain was later blocked. Zero potential and suppressed records consume none. Two-pass preview never consumes twice.

Line80: Critical at3Wounds caps ordinary healing at max(1, effective maximum minus1); it is not a maximumHP reduction and healing cannot lower currentHP. Reserve spends only actualHP restored. A final heal8 with room3 spends3 reserve; blocked healing spends0, other activation costs remain paid. Revival/form changes/encounter starts do not replenish reserve.

Line86: Actual positiveHP restoration is required for Radiance's cure, Renewal's Stamina, Sanctified Reprisal and Life Prophecy's RC trigger. Meditative Healing's laterKi and Transcendent Meditation's second-pulseKi are independent components and still resolve when healing caps/blocks. Blood Tithe uses its actual qualifying hostile Bleed-death trigger and finite use; not staged farming.

Line96: Stronger source flags override generic provenance: Vitality Link's child blocks every further link; Echo Leech blocks secondary healing/resource triggers; Blood Feast blocks damage/resource triggers; Merciful Smite blocks Smite/heal-copy chains; Crown Undying blocks redirection/heal-copy chains; Echoes/Spiral copies retain their explicit exclusions. Source payment and direct/actual-gain predicates still apply before a child exists.

Line100: OrdinaryMissingHP = effective maximum minus currentHP. Genuine excess is max(0, legal post-reduction healing minus OrdinaryMissingHP). Broad HP prohibition makes legal healing and excess0. Critical's ceiling does not redefine missingHP: max20/HP19/Critical/legalheal10 restores0 but has9 genuine excess; the missing1 is not excess. At HP20, legalheal10 has10 excess.

Line102: This quantity alone grants no conversion. A legal converter must satisfy its own costs/caps/cadences. One excess point can fund only one conversion. Source-internal Overflowing Light resolves before outside Cosmic Equilibrium uses remaining excess. Channel Life attaches a packet-wide prohibition on ALL excess-to-tempHP conversion, including another owner's feature. It permits an otherwise eligible Cosmic damage conversion.

Line104: **NEW agreed source exclusion:** Unpaid passive regeneration bounded by Mutation Recovery Reserve cannot supply excess-healing conversions unless a future source explicitly grants an exception. This covers Bloodthick Node, Rapid Coagulation, Regenerative Mutation and Bio-Stabilizer as a Bloodthick modifier. FullHP/Critical may compute mathematical excess but grants no Cosmic conversion and spends no Reserve. Do not extend this exclusion to otherwise eligible paid/finite healing merely because it restores0HP.


## Dependency and preservation check

All8 original feat objects and all335 registry entries remain preserved and byte-identical in the main project and review copy. Feat file SHA256842d14e868aa93d51fc6f21e39bc9dd3a1b872cdffcf467ffaa99a4cc3f779b6. Soul Cage explicitly names Lifeleech in prerequisites; Lifeleech explicitly says its charges power Soul Cage. Treat them together; do not create a second charge resource merely because they are two feats.

The new transformation conference also established immutable earliest physical origin: an object-origin creature cannot produce a soul, ordinary healing or corpse entitlement through anatomy changes. Creature-origin identity persists through object anatomy and back. No transformed object is an eligible manufactured soul farm. These remain constraints, not permission to invent a new generic soul economy.

Please answer the ten source questions with complete operational candidate objects for every clause of all eight feats, using exact source IDs, prerequisites and provenance. Identify any truly new numbers, durations, costs and anti-farm restrictions. Preserve distinctions between temporary HP, ordinary healing, stabilization, resurrection prohibition and actual soul custody. Point out new dependent sources that must be read rather than silently copying their effects. The complete objects, code and tests will return for independent implementation review before promotion.
