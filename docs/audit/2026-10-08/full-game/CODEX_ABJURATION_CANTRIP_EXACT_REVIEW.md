# Exact twelve-card Abjuration manuscript review

The body/equipment manuscript closure is recorded and the agreed rules are now in the active review guide. All original game sources remain preserved. Here are the actual twelve new ordinary-spell cards in a candidate file excluded from the operational batch loader.83 spells remain selectable; these12 are not promoted. Please review all exact fields and resolve these remaining concrete points before promotion:

1. Repelling Pulse: your phrase externally supported would literally exclude every object on a floor or table. The card excludes held/attached/secured objects but explicitly allows ordinary ground, table or shelf support. It stops at illegal spaces and uses ordinary Falling only if support is lost. Confirm.
2. Aura Sight: require existing visual perception, including an independently functioning special sight; hearing an invisible creature does not become vision. The spell itself grants no invisible/concealed vision. Confirm.
3. Fortify Object: source-qualified numerical units matter. Gameplay Loop uses the exact integrity0..3 stages below, not HP. Reducing2 HP cannot be silently applied as reducing2 integrity stages. The candidate proposes at casting choose an actual native track: reduce the next positive structural-HP damage by2 OR the next positive damage-caused integrity loss by1 stage, never both. No repair, ordinary wear/cost prevention or invented missing track. This one-stage branch is NEW and requires your review; the source table is evidence of the track, not authorization of the spell effect or a claim that the entire staged Gameplay Loop is promoted. Settle this into one usable card without requiring a simulator.
4. One-minute endpoints and replacement: cards with one pending entitlement are across ALL casters. Gesture keeps only the new concentration dependency; consuming the save also consumes it when advantage already came from elsewhere. Harmonic is consumed even when a stronger flat bonus wins. Nullify has only one chosen cantrip type across all casters. Confirm exact minute/round expiry and no old expiration clearing a later replacement.
5. Warding Mark gives only its binary glow; observers can make ordinary deductions from that result. Its descriptor must match an actual explicit CURRENT source-authorized record, not invented secret identity/ancestry inferred from appearance. Clarify transformation/illusion interaction using the existing one-body rules if needed; do not invent new creature tags.
6. Purify Drop uses an exact provisional0.05mL ceiling rather than approximate wording. Repel Vermin excludes actual encounter combatants, not a harmless creature merely because its statistics happen to be recorded somewhere. Confirm these bounds.

Source/card validation performed:12 unique existing IDs; all required fields and types present; exact Core blocks preserved per card; all access remains source-derived rank0; candidate loading leaves83 operational entries. This is structural/source verification, not a claim of complete effect execution or numerical balance. Please confirm or give precise repairs to this exact manuscript; no code approval is requested.

## Existing staged integrity source

Path: data/public/Decennium_Descent_Gameplay_Loop_v1.json; SHA256: 2638699842278c485ea9efdd0728c31ae90a18f25dbe741ac8c14671b0bca78b

```json
{
  "range": [
    0,
    3
  ],
  "3": "Sound",
  "2": "Worn; no penalty",
  "1": "Damaged; checks using it suffer -2",
  "0": "Broken; unusable until repaired",
  "repairSuccess": 1,
  "repairCriticalSuccess": 2
}
```

## Exact candidate cards

```json
{
  "status": "CANDIDATE — source-discussed; exact manuscript and proposed clarifications awaiting review",
  "scope": "Twelve ordinary rank-0 Abjuration spells; no runtime or whole-game approval",
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md"
  ],
  "spells": [
    {
      "id": "repelling-pulse",
      "activation": "Action",
      "rangeFeet": 5,
      "targets": "One Small or Tiny creature you can perceive, or one discrete unattended and unsecured object no larger than Small and no heavier than 10 pounds, within range.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "A creature makes a Strength save against your spell DC: failure permits the push; success means no movement. Eligible objects move automatically.",
      "effect": "A creature that fails its Strength save, or an eligible object, is pushed up to 5 feet directly away from you. Stop before solid terrain or an illegally occupied space.",
      "scaling": "None.",
      "limitations": "Worn, held, attached, restrained, locked or secured objects are ineligible. Ordinary ground, table or shelf support alone does not make an otherwise movable object ineligible. No chain push, Prone, disarm, free attack or collision damage. Removing support begins ordinary Falling; this spell adds no impact damage. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 5 feet, V/S, instantaneous and 5-foot push. NEW: Small/Tiny creature interpretation, 10-pound object ceiling, Strength save, custody and collision rules. Ground-support clarification is proposed for exact review.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 2,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Repelling Pulse",
            "effect": "Push a small object or creature 5 ft away.",
            "source_paragraph": 8985,
            "casting_time": "1 action",
            "range": "5 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Utility"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "sense-magic",
      "activation": "Action",
      "rangeFeet": 10,
      "targets": "Self; sense qualifying active magic within 10 feet and line of effect.",
      "duration": "Until the start of your next regular turn",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "You know only whether at least one active magical aura or ongoing magical effect is within the sensing area.",
      "scaling": "None.",
      "limitations": "Total cover blocks the sense. It supplies no direction, count, distance, owner, school, spell identity, rank, properties, creature identity, hidden curse, dormant enchantment, alignment or statistics. Nonmagical concealment or invisibility creates no magical signal. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 10 feet, V/S, one-round presence detection. NEW: Self, exact endpoint, no concentration, line of effect and yes/no information boundary.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 3,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Sense Magic",
            "effect": "Detect presence of magic within 10 ft for 1 round.",
            "source_paragraph": 8986,
            "casting_time": "1 action",
            "range": "10 feet",
            "duration": "1 round",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Detection"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "warding-gesture",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One willing creature you can perceive within range, including yourself.",
      "duration": "Concentration, up to 1 minute; ends on consumption",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "The target gains advantage on its next saving throw caused by a spell or an effect explicitly classified as magical. Consume the benefit after that qualifying save, regardless of success, failure or advantage from another source.",
      "scaling": "None.",
      "limitations": "A target has only one pending Warding Gesture across all casters. Recasting replaces the older pending benefit and its concentration dependency; it never stores an extra save. Nonmagical hazards and ordinary weapon effects do not qualify. If no qualifying save occurs, the benefit expires when its concentration or duration ends. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 30 feet, concentration1minute, M/F interpreted as the class focus and next magical-save advantage. NEW: one willing target rather than self-only reading of gain, exact eligibility, all-caster replacement and consumption.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 4,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Warding Gesture",
            "effect": "Gain advantage on next save against magic.",
            "source_paragraph": 8987,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Concentration, up to 1 minute",
            "components": "V, S, M/F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Ward"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "barrier-flicker",
      "activation": "Reaction — after an eligible projectile-based ranged attack is declared against the target, before its attack roll",
      "rangeFeet": 30,
      "targets": "One willing creature you can perceive within range, including yourself, targeted by the triggering projectile attack.",
      "duration": "The triggering attack only",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Grant the protected creature +2 AC against the triggering attack, then the spell ends.",
      "scaling": "None.",
      "limitations": "A projectile is a physical ranged or thrown weapon, or an effect explicitly firing or launching a projectile. Beams, rays, save-based effects, melee reach and attacks already rolled are ineligible unless an exact source establishes projectile eligibility before the roll. Strongest applicable flat AC bonus applies; multiple Flickers never add. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Reaction, 30 feet, V/S, momentary projectile defense and +2 AC versus one ranged attack. NEW CONFLICT RULING: before-roll trigger, one willing target, no concentration or offensive spell attack. Original Core Spell attack and concentration1minute metadata remain preserved as rejected alternatives.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 5,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Barrier Flicker",
            "effect": "Create momentary shield against projectiles (+2 AC vs one ranged attack).",
            "source_paragraph": 8988,
            "casting_time": "1 reaction",
            "range": "30 feet",
            "duration": "Concentration, up to 1 minute",
            "components": "V, S",
            "resolution": "Spell attack",
            "tags": [
              "Ward"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "nullify-element",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One willing creature you can perceive within range, including yourself.",
      "duration": "Until the start of your next regular turn",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Choose acid, cold, fire, lightning or thunder when cast. The target gains resistance to that type.",
      "scaling": "None.",
      "limitations": "A target can have only one Nullify Element at a time across all casters. A later cast replaces the earlier chosen type and duration, even if it selects a different type. Resistance to the same type never stacks into increased resistance or immunity. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 30 feet, V/S, one round and elemental resistance. NEW: one willing target rather than self-only gain, exact five-type list from reviewed Elemental Resistance, next-start endpoint, no concentration and all-caster single-type replacement.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 6,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Nullify Element",
            "effect": "Gain resistance to one element for 1 round.",
            "source_paragraph": 8989,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "1 round",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Ward"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "aura-sight",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "Self; observe already-visible creatures and objects within 30 feet and line of effect.",
      "duration": "Until the start of your next regular turn",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "You see a magical outline on each already-visible creature or object in the area that currently bears an active magical aura.",
      "scaling": "None.",
      "limitations": "You must already visually perceive the underlying target, through ordinary sight or an independently operating sight ability. This spell supplies no ability to see an invisible or concealed target and does not turn hearing a hidden creature into seeing it. Total cover blocks it. It identifies no school, spell, rank, caster, property, curse, alignment, creature type, statistics or motive. Unattached magical areas are not outlined. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 30 feet, V/S, one round and aura vision. NEW: Self, active-aura and existing-vision eligibility, exact endpoint, no concentration and limited information. Independent special-sight clarification is proposed for review.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 8,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Aura Sight",
            "effect": "See magical auras on objects or creatures for 1 round.",
            "source_paragraph": 8991,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "1 round",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Detection"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "fortify-object",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One discrete Small-or-smaller object you can perceive within range, with actual structural HP or a defined integer durability-stage record. Its current custodian must be willing if worn, held or carried.",
      "duration": "Until the start of your next regular turn, or until consumed",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "When casting, choose one actual damage track on the target: structural HP or integrity stages. After ordinary defenses, reduce the first positive damage packet to the chosen structural HP track by 2, minimum 0, then end this ward. Proposed integrity alternative: for a defined integer integrity-stage track, reduce the first positive damage-caused loss by 1 stage, minimum 0, then end the ward. Protect only the chosen track; never apply both reductions from one ward.",
      "scaling": "None.",
      "limitations": "No HP, temporary HP, repair, healing, maximum HP, AC, resistance, permanence, charges, ammunition or immunity is granted. A packet already reduced to0 by ordinary defenses does not consume the ward; a positive packet reduced to0 by this ward does. No protection against routine time-based wear or non-damage costs. One pending Fortify Object per object across all casters; later casting replaces the ward rather than queuing reductions. An undefined object damage track cannot be invented by the spell. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 30 feet, V/S and temporarily strengthening a small object. NEW CONFLICT RULING: finite one-packet ward replaces Instantaneous metadata. Proposed2HP reduction follows GPT; proposed1-stage alternative is a new explicit review question because Gameplay integrity3..0 is not HP.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 9,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Fortify Object",
            "effect": "Temporarily strengthen a small object against damage.",
            "source_paragraph": 8992,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Ward"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "detect-corruption",
      "activation": "Action",
      "rangeFeet": 10,
      "targets": "Self; sample the area within 10 feet and line of effect.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Learn whether at least one creature, object, area or active effect in the area currently has an explicit canonical Corruption record, tag or state.",
      "scaling": "None.",
      "limitations": "Total cover blocks detection. No permanent sense, direction, count, severity, identity, source, numeric Corruption value, hidden consequence, cure, alignment or statistics is supplied. Do not infer Corruption from appearance, faction, species, damage type, poison, disease, school, theme or suspicion. The spell reports only its defined presence result. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 10 feet, V/S, instantaneous and Corruption presence. NEW: explicit current Corruption predicate, Self, line of effect, no concentration and information limits.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 11,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Detect Corruption",
            "effect": "Sense presence of corruption within 10 ft.",
            "source_paragraph": 8994,
            "casting_time": "1 action",
            "range": "10 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Detection",
              "Corruption"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "harmonic-protection",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One willing creature within range and line of effect that can hear the casting tone, including yourself if you can hear it.",
      "duration": "Up to 1 minute; ends on the next saving throw",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "The target gains +1 to its next saving throw within the duration. Consume the benefit on that save regardless of success or failure, even if another stronger flat bonus prevents the+1 from numerically applying.",
      "scaling": "None.",
      "limitations": "One pending Harmonic Protection per target across all casters; later casting refreshes the endpoint, not the number of uses. Apply the strongest same-stat flat bonus; do not add this to another flat save bonus. Deafness at casting prevents eligibility, but later deafness does not cancel an already granted benefit. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 30 feet, V/S, a tone and+1 to next save. NEW CONFLICT RULING:1minute future-save entitlement rather than unresolved Instantaneous metadata; hearing at entry, no concentration, all-caster cap and consumption.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 12,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Harmonic Protection",
            "effect": "Create a tone that grants +1 to next saving throw.",
            "source_paragraph": 8995,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Ward"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "purify-drop",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One physically separated droplet of liquid you can perceive within range, no larger than 0.05mL.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Remove ordinary nonmagical dirt, sediment, harmless contamination or unwanted mundane dissolved impurities from that one droplet.",
      "scaling": "None.",
      "limitations": "The drop must already be separate from a continuous volume. No effect on the rest of a barrel, pool, vial, tank or body. Does not neutralize poison, toxins, pathogens, disease, Corruption, curses, magical contamination, alchemical reagents, medicine, drugs, enchantments or bodily conditions. Removed impurities cannot be recovered as reagents, salt, metal or other resources. Creates no water or supplies. Each casting treats only one drop. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action,30feet,V/S,instantaneous and one drop of mundane purification. NEW: separated-droplet test, exact provisional0.05mL ceiling, hazard/resource exclusions and no propagation. Exact ceiling replaces approximate wording for reproducibility.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 13,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Purify Drop",
            "effect": "Cleanse one drop of liquid of mundane impurities.",
            "source_paragraph": 8996,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Restoration"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "repel-vermin",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "Self; ordinary eligible vermin within a 30-foot avoidance field.",
      "duration": "1 minute",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Ordinary natural nonmagical insects and rodents no larger than Small do not willingly move closer to you. When already nearby and free to choose movement, they prefer a safe unobstructed route farther away.",
      "scaling": "None.",
      "limitations": "Summons, transformed creatures, trained companions, controlled or magical creatures, internal parasites and statted encounter combatants are ineligible. No creature must enter hazards or barriers, abandon necessary shelter, Dash or spend an Action to flee. It may remain if no safe route exists. No Charmed/Frightened, attack prevention, summon dismissal, disease cure, parasite expulsion or immunity to bites/contamination. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action,30feet,V/S,1minute and ordinary insects/rodents avoiding you. NEW: Self-centered field, no concentration, natural nuisance-only eligibility and safe voluntary behavior. A creature participating as a combatant is excluded, regardless of whether its incidental statistics were previously written down.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 14,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Repel Vermin",
            "effect": "Small non-magical insects and rodents avoid you for 1 minute.",
            "source_paragraph": 8997,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "1 minute",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Utility"
            ],
            "rp_cost": 0
          }
        }
      ]
    },
    {
      "id": "warding-mark",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One fixed solid surface or ground point you can perceive within range.",
      "duration": "Concentration, up to 1 minute",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Place one visible magical mark. Choose one named species/template actually known to the caster, or one exact canonical creature type/tag already present on operational records. The mark glows while at least one creature matching that explicit descriptor is within10feet of it with line of effect.",
      "scaling": "None.",
      "limitations": "Do not infer or invent creature taxonomy. With no explicit matching record, it does not guess. Walls and closed barriers block triggering. Teleportation counts when the creature actually occupies the area. The mark directly reports only presence, not which creature, square, identity, disguise, alignment, statistics, intent or lore. Recasting uses normal concentration replacement. Dispel Minor may end this ongoing rank-0 mark when legally targeted. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action,30feet,V/S/F,concentration1minute and a mark glowing for creature types. NEW: fixed surface,10foot trigger, one exact descriptor, current presence with line of effect, no inferred taxonomy and no extra information. A viewer may make ordinary deductions from the visible binary result; the spell does not prevent reasoning.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
      "sourceCoreEntries": [
        {
          "index": 15,
          "original": {
            "school": "Abjuration",
            "level": 0,
            "name": "Warding Mark",
            "effect": "Place a small mark that glows when specific creature types approach.",
            "source_paragraph": 8998,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Concentration, up to 1 minute",
            "components": "V, S, M/F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Ward"
            ],
            "rp_cost": 0
          }
        }
      ]
    }
  ]
}
```
