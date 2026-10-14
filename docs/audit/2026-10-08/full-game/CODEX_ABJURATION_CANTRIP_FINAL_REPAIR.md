# Twelve Abjuration cantrips final manuscript repair

Your five exact manuscript repairs are applied below: eight source-clock duration fields; application-qualified replacement for four wards and correct Gesture concentration dependency; Fortify Object prevents2HP or one fewer native Integrity stages lost on the chosen track; Warding Mark matches current source-authorized records and explicit transformation changes; Repel Vermin uses actual combat participation rather than existence of statistics. The other agreed ground-support, actual visual perception and0.05mL limits remain.

Please review this complete repaired artifact and confirm whether the twelve cards can enter the existing operational PLAYTEST manuscript. All source blocks and per-class access stay unchanged, and source/structural checks still pass. Current count remains83 until your actual approval, then it would become95 with753 unfinished. This asks for authored manuscript promotion only, not implementation/runtime, balance, or whole-game/GitHub closure. New mechanics remain explicitly provisional.

{
  "status": "CANDIDATE — five exact manuscript repairs applied; final review pending",
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
      "designNotes": "PRESERVED: Action, 5 feet, V/S, instantaneous and 5-foot push. NEW: Small/Tiny creature interpretation, 10-pound object ceiling, Strength save, custody and collision rules. Ground-support clarification is an explicit provisional clarification.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "duration": "If applied in initiative, expires at the caster's first future regular-start marker after application; preserve that virtual marker through initiative changes. If applied outside initiative, expires 6 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts.",
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
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "duration": "If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual source-start phase through initiative changes. If applied outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts. Ends earlier if concentration ends. Ends earlier when consumed.",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "The target gains advantage on its next saving throw caused by a spell or an effect explicitly classified as magical. Consume the benefit after that qualifying save, regardless of success, failure or advantage from another source.",
      "scaling": "None.",
      "limitations": "A target has only one pending Warding Gesture across all casters. Recasting replaces the older pending benefit and its concentration dependency; it never stores an extra save. Nonmagical hazards and ordinary weapon effects do not qualify. If no qualifying save occurs, the benefit expires when its concentration or duration ends. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling. A replacement is a new application with its own endpoint. An expiration or consumption event belonging to an older application cannot remove the current replacement. Replacing Warding Gesture ends the old effect and releases that old casting's concentration dependency. The new casting owns only its own concentration dependency.",
      "designNotes": "PRESERVED: Action, 30 feet, concentration 1 minute, M/F interpreted as the class focus and next magical-save advantage. NEW: one willing target rather than self-only reading of gain, exact eligibility, all-caster replacement and consumption.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "designNotes": "PRESERVED: Reaction, 30 feet, V/S, momentary projectile defense and +2 AC versus one ranged attack. NEW CONFLICT RULING: before-roll trigger, one willing target, no concentration or offensive spell attack. Original Core Spell attack and concentration 1 minute metadata remain preserved as rejected alternatives.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "duration": "If applied in initiative, expires at the caster's first future regular-start marker after application; preserve that virtual marker through initiative changes. If applied outside initiative, expires 6 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Choose acid, cold, fire, lightning or thunder when cast. The target gains resistance to that type.",
      "scaling": "None.",
      "limitations": "A target can have only one Nullify Element at a time across all casters. A later cast replaces the earlier chosen type and duration, even if it selects a different type. Resistance to the same type never stacks into increased resistance or immunity. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling. A replacement is a new application with its own endpoint. An expiration or consumption event belonging to an older application cannot remove the current replacement.",
      "designNotes": "PRESERVED: Action, 30 feet, V/S, one round and elemental resistance. NEW: one willing target rather than self-only gain, exact five-type list from reviewed Elemental Resistance, next-start endpoint, no concentration and all-caster single-type replacement.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "duration": "If applied in initiative, expires at the caster's first future regular-start marker after application; preserve that virtual marker through initiative changes. If applied outside initiative, expires 6 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "You see a magical outline on each already-visible creature or object in the area that currently bears an active magical aura.",
      "scaling": "None.",
      "limitations": "You must already visually perceive the underlying target, through ordinary sight or an independently operating sight ability. This spell supplies no ability to see an invisible or concealed target and does not turn hearing a hidden creature into seeing it. Total cover blocks it. It identifies no school, spell, rank, caster, property, curse, alignment, creature type, statistics or motive. Unattached magical areas are not outlined. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
      "designNotes": "PRESERVED: Action, 30 feet, V/S, one round and aura vision. NEW: Self, active-aura and existing-vision eligibility, exact endpoint, no concentration and limited information. Independent special-sight clarification is an explicit provisional clarification.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "duration": "If applied in initiative, expires at the caster's first future regular-start marker after application; preserve that virtual marker through initiative changes. If applied outside initiative, expires 6 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts. Ends earlier when consumed.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "When you cast this spell, choose one damage track the target actually possesses: structural HP or Integrity. The first later damage event that would cause a positive loss on that track is modified after the object's ordinary defenses. For structural HP, reduce that event's structural-HP damage by 2, minimum 0. For Integrity, reduce the number of Integrity stages that event would cause the object to lose by 1, minimum 0. Then consume the ward. It never modifies both tracks from one casting.",
      "scaling": "None.",
      "limitations": "No HP, temporary HP, repair, healing, maximum HP, AC, resistance, permanence, charges, ammunition or immunity is granted. A packet already reduced to 0 by ordinary defenses does not consume the ward; a positive packet reduced to 0 by this ward does. No protection against routine time-based wear or non-damage costs. One pending Fortify Object per object across all casters; later casting replaces the ward rather than queuing reductions. An undefined object damage track cannot be invented by the spell. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling. A replacement is a new application with its own endpoint. An expiration or consumption event belonging to an older application cannot remove the current replacement. A target possessing neither actual structural HP nor a defined Integrity track is ineligible. If it possesses both, choose one at casting. An otherwise two-stage loss becomes one stage; an otherwise one-stage loss becomes zero. This prevents loss rather than repairing afterward.",
      "designNotes": "PRESERVED: Action,30 feet,V/S and temporarily strengthening a small object. NEW CONFLICT RULING: one-source-round, one-event ward replaces Instantaneous metadata. Choose the native track at casting: prevent 2 structural-HP damage or 1 Integrity stage of damage-caused loss. These are separate provisional ward values, not unit conversions. The staged integrity 0..3 table is preserved as source evidence; the spell does not promote the whole equipment system.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "duration": "If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual source-start phase through initiative changes. If applied outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts. Ends earlier when consumed.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "The target gains +1 to its next saving throw within the duration. Consume the benefit on that save regardless of success or failure, even if another stronger flat bonus prevents the+1 from numerically applying.",
      "scaling": "None.",
      "limitations": "One pending Harmonic Protection per target across all casters; later casting refreshes the endpoint, not the number of uses. Apply the strongest same-stat flat bonus; do not add this to another flat save bonus. Deafness at casting prevents eligibility, but later deafness does not cancel an already granted benefit. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling. A replacement is a new application with its own endpoint. An expiration or consumption event belonging to an older application cannot remove the current replacement.",
      "designNotes": "PRESERVED: Action, 30 feet, V/S, a tone and+1 to next save. NEW CONFLICT RULING:1 minute future-save entitlement rather than unresolved Instantaneous metadata; hearing at entry, no concentration, all-caster cap and consumption.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "designNotes": "PRESERVED: Action,30 feet,V/S,instantaneous and one drop of mundane purification. NEW: separated-droplet test, exact provisional 0.05 mL ceiling, hazard/resource exclusions and no propagation. Exact ceiling replaces approximate wording for reproducibility.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "duration": "If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual source-start phase through initiative changes. If applied outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Ordinary natural nonmagical insects and rodents no larger than Small do not willingly move closer to you. When already nearby and free to choose movement, they prefer a safe unobstructed route farther away.",
      "scaling": "None.",
      "limitations": "Summons, transformed creatures, trained companions, controlled or magical creatures, internal parasites and creatures currently participating in an encounter as combatants are ineligible. No creature must enter hazards or barriers, abandon necessary shelter, Dash or spend an Action to flee. It may remain if no safe route exists. No Charmed/Frightened, attack prevention, summon dismissal, disease cure, parasite expulsion or immunity to bites/contamination. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling. Merely possessing a stat block or recorded statistics does not make a nuisance animal a combatant. If it genuinely joins combat as a combatant, this spell stops governing its behavior while it participates.",
      "designNotes": "PRESERVED: Action,30 feet,V/S,1 minute and ordinary insects/rodents avoiding you. NEW: Self-centered field, no concentration, natural nuisance-only eligibility and safe voluntary behavior. A creature participating as a combatant is excluded, regardless of whether its incidental statistics were previously written down.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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
      "duration": "If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual source-start phase through initiative changes. If applied outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts. Ends earlier if concentration ends.",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic after legal casting; no spell attack or saving throw.",
      "effect": "Place one visible magical mark. Choose one named species/template genuinely known to the caster and represented by a current source-authorized creature record, or one exact canonical creature type/tag defined by current operational source data. The mark glows while at least one creature whose current canonical mechanical record matches that descriptor is within 10 feet of it with line of effect.",
      "scaling": "None.",
      "limitations": "Do not infer or invent creature taxonomy. With no explicit matching record, it does not guess. Walls and closed barriers block triggering. Teleportation counts when the creature actually occupies the area. The mark directly reports only presence, not which creature, square, identity, disguise, alignment, statistics, intent or lore. Recasting uses normal concentration replacement. Dispel Minor may end this ongoing rank-0 mark when legally targeted. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling. Matching does not infer a record from apparent shape, disguise, name, reputation, guessed ancestry or Director-only identity. Appearance-only changes do not alter matching descriptors. A transformation changes a species/type/tag only if its exact source expressly changes that record; current Druid and bounded spell-form profile names create no new creature types. If an exact source changes a canonical descriptor, use that current changed record while it lasts. Ordinary observers may draw reasonable mundane conclusions from the binary glow.",
      "designNotes": "PRESERVED: Action,30 feet,V/S/F,concentration 1 minute and a mark glowing for creature types. NEW: fixed surface,10 foot trigger, one exact descriptor, current presence with line of effect, no inferred taxonomy and no extra information. A viewer may make ordinary deductions from the visible binary result; the spell does not prevent reasoning.",
      "implementationStatus": "CANDIDATE — exact manuscript review pending; not selectable",
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
        "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
      ],
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