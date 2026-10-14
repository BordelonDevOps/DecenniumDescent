# Bound Flora sources

Copied from the verified submission, not replacement source text. Source hashes bind whole archived files. Review scope is the four Flora interfaces, not other feat contents.

## S1 — Complete three current feat records

Path: `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/candidate.json`

SHA-256: `87f6348f95b0cd5969b50a8d7ab896863ab450091cc835c9653152f77f3747bd`

Location: `/feats (IDs conjure_flora, trapcasting, verdant_bond)`

```json
[
  {
    "id": "conjure_flora",
    "name": "Conjure Flora",
    "cohort": "magic_extended",
    "sourceObject": {
      "id": "conjure_flora",
      "name": "Conjure Flora",
      "description": "Seeds answer your call, rooting as guardians, lashing as spears, blooming as verdict. Prestige lineage: Verdant Animist. completed from the existing development record.)",
      "prerequisite": "Spellcasting ability, proficiency in Nature",
      "effect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
      "type": "Magic",
      "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
      "legacyEffect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
      "status": "provisional-complete",
      "balanceReview": true,
      "draft": false,
      "deprecated": false,
      "needsReview": true
    },
    "reviewStatus": "Source-authored; exact candidate review pending.",
    "operationalRules": "Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW to make the second-capacity clause usable, at level 10 this same committed use permits one additional Action before the first plant expires to create one second plant; no second rest use, no later replacement of that spent creation. This is an explicit proposed addition to the printed one-seedling creation, not a recovered rule. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.\nNEW ordinary command scheduling: each plant has one attached phase immediately after its owner’s regular turn, not an independent initiative turn. Its ordinary commanded action requires the owner’s shared Bonus Action within60ft through the specified perceivable command channel and spends the one offensive companion allowance per owner per numbered round if offensive. With no legal command it has no autonomous attack. Trapcasting’s explicitly adopted entry-trigger or burst is a separate narrow exception spending that same shared offensive allowance, never another free attack.\nKEEP the already-operative SUP-07 floraBody/dc acquisition requirement: at acquisition permanently select and record one actual possessed spellcasting route as this feat's DC provider. Use DC 8 + current PB + that route's current casting-ability modifier; do not invent Wisdom, Spellcraft or another default. This source choice is separate from the later seedling mode/burst-type choice. Ownership initializes only the finite creation allowance and body capacity, with no plant, pending additional creation, command or active effect. All printed acquisition predicates and the actual earned feat opportunity remain required.",
    "workedCases": [
      "Two active plants can extend where the single 1d6 lash originates; they do not produce 2d6 or two attacks.",
      "At level 10, a second Action during the first plant’s lifetime can consume the one proposed additional-creation entitlement; it does not allow repeated replacement plants."
    ],
    "payloadOperational": "Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW to make the second-capacity clause usable, at level 10 this same committed use permits one additional Action before the first plant expires to create one second plant; no second rest use, no later replacement of that spent creation. This is an explicit proposed addition to the printed one-seedling creation, not a recovered rule. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.\nNEW ordinary command scheduling: each plant has one attached phase immediately after its owner’s regular turn, not an independent initiative turn. Its ordinary commanded action requires the owner’s shared Bonus Action within60ft through the specified perceivable command channel and spends the one offensive companion allowance per owner per numbered round if offensive. With no legal command it has no autonomous attack. Trapcasting’s explicitly adopted entry-trigger or burst is a separate narrow exception spending that same shared offensive allowance, never another free attack.\nKEEP the already-operative SUP-07 floraBody/dc acquisition requirement: at acquisition permanently select and record one actual possessed spellcasting route as this feat's DC provider. Use DC 8 + current PB + that route's current casting-ability modifier; do not invent Wisdom, Spellcraft or another default. This source choice is separate from the later seedling mode/burst-type choice. Ownership initializes only the finite creation allowance and body capacity, with no plant, pending additional creation, command or active effect. All printed acquisition predicates and the actual earned feat opportunity remain required.",
    "selectionEnabled": false,
    "exactApproved": false,
    "runtimeApproved": false,
    "sharedRulesRef": "shared_rules.json",
    "supplementsRef": "supplements.json"
  },
  {
    "id": "trapcasting",
    "name": "Trapcasting",
    "cohort": "magic_extended",
    "sourceObject": {
      "id": "trapcasting",
      "name": "Trapcasting",
      "description": "Roots, thorns, and spore-mines—you sow violence that waits patiently to bloom. Prestige lineage: Verdant Animist. completed from the existing development record.)",
      "prerequisite": "Conjure Flora or Verdant Bond",
      "effect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot area, 2d6 damage, type chosen at conjuring).",
      "type": "Magic",
      "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
      "legacyEffect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot AoE, 2d6 damage, type chosen at conjuring).",
      "status": "provisional-complete",
      "balanceReview": true,
      "draft": false,
      "deprecated": false,
      "needsReview": true
    },
    "reviewStatus": "Source-authored; exact candidate review pending.",
    "operationalRules": "Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.\nNEW phase exception is explicit: its first eligible hostile-entry attack may occur on that actual entry outside the ordinary attached phase, but spends the same owner-round offensive companion allowance immediately. Its paid burst likewise spends that allowance; neither can occur when it is already spent. Placement itself is not an entry-trigger unless this exact procedure expressly says so. General Conjure Flora commands retain their attached phase, shared Bonus Action and sensory channel.",
    "workedCases": [
      "Forced hostile entry can trigger a plant, but another plant cannot produce a second offensive outcome after the group allowance is spent that round.",
      "Detonation consumes the actual plant even if every creature saves. An expired plant cannot be detonated."
    ],
    "payloadOperational": "Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.\nNEW phase exception is explicit: its first eligible hostile-entry attack may occur on that actual entry outside the ordinary attached phase, but spends the same owner-round offensive companion allowance immediately. Its paid burst likewise spends that allowance; neither can occur when it is already spent. Placement itself is not an entry-trigger unless this exact procedure expressly says so. General Conjure Flora commands retain their attached phase, shared Bonus Action and sensory channel.",
    "selectionEnabled": false,
    "exactApproved": false,
    "runtimeApproved": false,
    "sharedRulesRef": "shared_rules.json",
    "supplementsRef": "supplements.json"
  },
  {
    "id": "verdant_bond",
    "name": "Verdant Bond",
    "cohort": "magic_extended",
    "sourceObject": {
      "id": "verdant_bond",
      "name": "Verdant Bond",
      "description": "The green speaks to you in sap and silence. You answer with growth. Prestige lineage: Verdant Animist. completed from the existing development record.)",
      "prerequisite": "Proficiency in Nature, spellcasting ability",
      "effect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
      "type": "Magic",
      "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
      "legacyEffect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
      "status": "provisional-complete",
      "balanceReview": true,
      "draft": false,
      "deprecated": false,
      "needsReview": true
    },
    "reviewStatus": "Source-authored; exact candidate review pending.",
    "operationalRules": "While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Distinct eligible flat feat bonuses add under FS-03; this same feat contributes only once. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.\nSOURCE ally scope: the owner may be the one chosen message recipient. It triggers on that recipient’s first genuinely future qualifying passage after recording, not immediate creation beside the tree; the audible stored message is not private telepathy or general tree fluency.",
    "workedCases": [
      "With an active qualifying plant, a spell actually cast through the Ranger route gains the stated+1DC. An independently acquired eligible Spell Focus+1 adds, for+2total; duplicate Verdant Bond does not.",
      "The stored message is audible to anyone close enough to hear when the designated ally triggers it."
    ],
    "payloadOperational": "While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Distinct eligible flat feat bonuses add under FS-03; this same feat contributes only once. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.\nSOURCE ally scope: the owner may be the one chosen message recipient. It triggers on that recipient’s first genuinely future qualifying passage after recording, not immediate creation beside the tree; the audible stored message is not private telepathy or general tree fluency.",
    "selectionEnabled": false,
    "exactApproved": false,
    "runtimeApproved": false,
    "sharedRulesRef": "shared_rules.json",
    "supplementsRef": "supplements.json"
  }
]
```

## S2 — Complete current SUP-07 Flora body

Path: `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/supplements.json`

SHA-256: `59635b07655f06f4d3fab872b2665638a683702ad89a5322fe2df426fcd96146`

Location: `/groups/6/value/floraBody`

```json
{
  "size": "Tiny, occupies a supported 5 ft square as a low plant; does not block traversal or grant cover; zeroSpeed and no voluntary movement. Can be carried only as an ordinary object-body interaction; lifting/uprooting ends it immediately without harvest.",
  "statistics": "Plant creature; no assumed language, mind immunity or world-origin claim. AC 12, HP 5+owner PB snapshotted at creation; saves +owner PB, other checks +0. No damage/condition immunities or special senses unless an actual source grants them. It perceives commands within 60 ft through ordinary sight/hearing; Silence matters for spoken commands. It has no independent initiative, Action, Bonus Action or Reaction, and no attack outside the commanded profiles or the final expressly bounded Trapcasting exception. Zero HP permanently destroys it instead of creating a dying body. No corpse, reward, harvest, resource/soul collection, loot or Supply credit. Ordinary legal damage and healing may affect the actual creature but cannot recreate a destroyed plant, refill its creation entitlement or extend its deadline.",
  "dc": "At acquisition select one actual possessed spellcasting route; use DC 8+current PB+that route’s current ability modifier. No phantom Wisdom/Spellcraft statistic. Actual source-specific component/target defenses still apply.",
  "cadence": "Action creates;1/SR or LR, capacity 1 or 2 at 10. NEW level 10 completion: after the first creation, one additionalAction before that first seedling expires may create the second without a second rest use. This one extra creation entitlement is bound to that original committed use and is consumed once; if missed/lost it is not banked. Each plant has its own original minute deadline. No replacement/revival can restore the entitlement. Any command, trap orBurst with a hostile result uses the owner’s one shared offensive-companion allowance per numbered round; one selected mode outcome for the coordinated group. Ordinary command: owner shared Bonus Action, actual perceptible60ft channel, attached phase after owner regular turn. One action outcome and one offensive allowance per owner/numbered round; Trapcasting spends that same allowance at its exact entry/burst event. No independent turn is added.",
  "endpoints": "Poisoned/Restrained records also end if the generating plant ends; no concentration is required. Reapplying same profile follows ordinary nonstacking rules. Burst consumes one body before resolving a 10 ft-radius area, all creaturesDEXsave,2d6 selectedtype half on success. Chosenmode/type doesnotchange aftercreation. No destroyed body can command or trap during the resolving event.",
  "commandChoice": "Every seedling may use the printed Lash command. Its selected creation mode additionally determines its Spore or Entangle option and its Trapcasting result/burst type; selecting Lash leaves that basic profile. A coordinated command chooses only one permitted outcome from one actual participating plant. Other plants extend the legal Lash origin as printed but never multiply damage, control areas or offense allowances.",
  "modes": [
    {
      "id": "lash",
      "command": "One creature within 10 ft of any commandedplant makesDEXsave;1d6 piercing, half on success. One shared attack outcome, not a die perplant.",
      "trap": "Entering creatureDEXsave;failure 1d6 piercing, success 0.",
      "burstType": "piercing"
    },
    {
      "id": "spore",
      "command": "One creature within 10 ft of any commandedplant makesCONsave orPoisoned until its next future regular end. No damage; actual poison/Poisoned immunities apply.",
      "trap": "Entering creatureDEXsave;failurePoisoned until its next future regular end, successnone.",
      "burstType": "poison"
    },
    {
      "id": "entangle",
      "command": "Choose one 10 ft square within 10 ft of a commandedplant, withsupportedground/lineofeffect. Each creature in it makesSTRsave orRestrained until its next future regular end. On its turn an affected creature may spendAction for STR(Athletics) or DEX(Acrobatics) vsflora DC to end its ownrecord. No damaginggrowth or freewall.",
      "trap": "Entering creatureDEXsave;failureRestrained until its next future regular end with sameActionescape, successnone.",
      "burstType": "piercing"
    }
  ]
}
```

## S3 — Complete three current acquisition contracts

Path: `docs/audit/2026-10-08/full-game/FEAT_EXACT_01_ACQUISITION_CONTRACTS.json`

SHA-256: `ec458dd43dc613cae6c2f5eaf72b909a1e1a8cb69420487ec4b8d13e451cc547`

Location: `/records (same three IDs)`

```json
[
  {
    "id": "conjure_flora",
    "name": "Conjure Flora",
    "originalObject": {
      "id": "conjure_flora",
      "name": "Conjure Flora",
      "description": "Seeds answer your call, rooting as guardians, lashing as spears, blooming as verdict. Prestige lineage: Verdant Animist. completed from the existing development record.)",
      "prerequisite": "Spellcasting ability, proficiency in Nature",
      "effect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
      "type": "Magic",
      "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
      "legacyEffect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
      "status": "provisional-complete",
      "balanceReview": true,
      "draft": false,
      "deprecated": false,
      "needsReview": true
    },
    "printedPrerequisitePresent": true,
    "printedPrerequisite": "Spellcasting ability, proficiency in Nature",
    "candidatePointer": "/feats/298",
    "requirements": {
      "kind": "all",
      "requirements": [
        {
          "kind": "actualSpellcastingRoute",
          "grantsNoPoolRankOrClass": true,
          "castingPrerequisitePolicyRef": "FEAT327-ACQ-03"
        },
        {
          "kind": "actualProficiency",
          "credential": "Nature"
        }
      ]
    },
    "additionalUniversalAcquisitionGate": "One actual unspent class-scheduled ASI/feat opportunity or separately authorized feat grant; prerequisite success never creates a choice.",
    "actualClassScheduleRequired": true,
    "candidateSelectionEnabled": false,
    "acquisitionDoesNotGrantUseWithoutOngoingPredicates": true,
    "completeOperativeProcedure": "Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW to make the second-capacity clause usable, at level 10 this same committed use permits one additional Action before the first plant expires to create one second plant; no second rest use, no later replacement of that spent creation. This is an explicit proposed addition to the printed one-seedling creation, not a recovered rule. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.\nNEW ordinary command scheduling: each plant has one attached phase immediately after its owner’s regular turn, not an independent initiative turn. Its ordinary commanded action requires the owner’s shared Bonus Action within60ft through the specified perceivable command channel and spends the one offensive companion allowance per owner per numbered round if offensive. With no legal command it has no autonomous attack. Trapcasting’s explicitly adopted entry-trigger or burst is a separate narrow exception spending that same shared offensive allowance, never another free attack.\nKEEP the already-operative SUP-07 floraBody/dc acquisition requirement: at acquisition permanently select and record one actual possessed spellcasting route as this feat's DC provider. Use DC 8 + current PB + that route's current casting-ability modifier; do not invent Wisdom, Spellcraft or another default. This source choice is separate from the later seedling mode/burst-type choice. Ownership initializes only the finite creation allowance and body capacity, with no plant, pending additional creation, command or active effect. All printed acquisition predicates and the actual earned feat opportunity remain required.",
    "requirementsStatus": "Source-derived finite validation contract; actual positive/negative actor histories still require testing.",
    "boundaryCasesValidated": false,
    "repeats": {
      "policy": "nonrepeatable",
      "permanentChoice": true
    },
    "sourceDecision": "Adopt three closed finite plant profiles with actual attached command phases and capacity/creation entitlements; no anonymous autonomous attack, corpse, harvest or class minion grant.",
    "requiresLegacyOrContextReceiptWithoutCreatingIt": false
  },
  {
    "id": "trapcasting",
    "name": "Trapcasting",
    "originalObject": {
      "id": "trapcasting",
      "name": "Trapcasting",
      "description": "Roots, thorns, and spore-mines—you sow violence that waits patiently to bloom. Prestige lineage: Verdant Animist. completed from the existing development record.)",
      "prerequisite": "Conjure Flora or Verdant Bond",
      "effect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot area, 2d6 damage, type chosen at conjuring).",
      "type": "Magic",
      "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
      "legacyEffect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot AoE, 2d6 damage, type chosen at conjuring).",
      "status": "provisional-complete",
      "balanceReview": true,
      "draft": false,
      "deprecated": false,
      "needsReview": true
    },
    "printedPrerequisitePresent": true,
    "printedPrerequisite": "Conjure Flora or Verdant Bond",
    "candidatePointer": "/feats/329",
    "requirements": {
      "kind": "any",
      "requirements": [
        {
          "kind": "ownedFeat",
          "id": "conjure_flora"
        },
        {
          "kind": "ownedFeat",
          "id": "verdant_bond"
        }
      ]
    },
    "additionalUniversalAcquisitionGate": "One actual unspent class-scheduled ASI/feat opportunity or separately authorized feat grant; prerequisite success never creates a choice.",
    "actualClassScheduleRequired": true,
    "candidateSelectionEnabled": false,
    "acquisitionDoesNotGrantUseWithoutOngoingPredicates": true,
    "completeOperativeProcedure": "Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.\nNEW phase exception is explicit: its first eligible hostile-entry attack may occur on that actual entry outside the ordinary attached phase, but spends the same owner-round offensive companion allowance immediately. Its paid burst likewise spends that allowance; neither can occur when it is already spent. Placement itself is not an entry-trigger unless this exact procedure expressly says so. General Conjure Flora commands retain their attached phase, shared Bonus Action and sensory channel.",
    "requirementsStatus": "Source-derived finite validation contract; actual positive/negative actor histories still require testing.",
    "boundaryCasesValidated": false,
    "repeats": {
      "policy": "nonrepeatable",
      "permanentChoice": true
    },
    "sourceDecision": "Adopt entry-trigger/burst exceptions explicitly spending the same one owner-round offensive-companion allowance as ordinary plant commands; no simultaneous free offense or recreated plants.",
    "requiresLegacyOrContextReceiptWithoutCreatingIt": false
  },
  {
    "id": "verdant_bond",
    "name": "Verdant Bond",
    "originalObject": {
      "id": "verdant_bond",
      "name": "Verdant Bond",
      "description": "The green speaks to you in sap and silence. You answer with growth. Prestige lineage: Verdant Animist. completed from the existing development record.)",
      "prerequisite": "Proficiency in Nature, spellcasting ability",
      "effect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
      "type": "Magic",
      "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
      "legacyEffect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
      "status": "provisional-complete",
      "balanceReview": true,
      "draft": false,
      "deprecated": false,
      "needsReview": true
    },
    "printedPrerequisitePresent": true,
    "printedPrerequisite": "Proficiency in Nature, spellcasting ability",
    "candidatePointer": "/feats/332",
    "requirements": {
      "kind": "all",
      "requirements": [
        {
          "kind": "actualProficiency",
          "credential": "Nature"
        },
        {
          "kind": "actualSpellcastingRoute",
          "grantsNoPoolRankOrClass": true,
          "castingPrerequisitePolicyRef": "FEAT327-ACQ-03"
        }
      ]
    },
    "additionalUniversalAcquisitionGate": "One actual unspent class-scheduled ASI/feat opportunity or separately authorized feat grant; prerequisite success never creates a choice.",
    "actualClassScheduleRequired": true,
    "candidateSelectionEnabled": false,
    "acquisitionDoesNotGrantUseWithoutOngoingPredicates": true,
    "completeOperativeProcedure": "While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Distinct eligible flat feat bonuses add under FS-03; this same feat contributes only once. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.\nSOURCE ally scope: the owner may be the one chosen message recipient. It triggers on that recipient’s first genuinely future qualifying passage after recording, not immediate creation beside the tree; the audible stored message is not private telepathy or general tree fluency.",
    "requirementsStatus": "Source-derived finite validation contract; actual positive/negative actor histories still require testing.",
    "boundaryCasesValidated": false,
    "repeats": {
      "policy": "nonrepeatable",
      "permanentChoice": true
    },
    "sourceDecision": "Adopt actual plant-linked Druid/Ranger/Shaman route bonus and one finite real audible message; include owner as an eligible ally, preserve LAX evidence and original spell access.",
    "requiresLegacyOrContextReceiptWithoutCreatingIt": false
  }
]
```

## S4 — Complete current FS-01, FS-06, FS-07 and FS-10

Path: `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/shared_rules.json`

SHA-256: `382078e9245d54dc06f55f4a525e6567dcbb0e8771a743ef9f8db9d37fab4e74`

Location: `/rules (IDs FS-01, FS-06, FS-07, FS-10)`

```json
[
  {
    "id": "FS-01",
    "title": "Authority, identity and acquisition",
    "disposition": "ADOPT EXPLICIT NEW COMPLETION",
    "wording": "These are source/proposal-authoring directions for 327 exact existing IDs, not approval of assembled operational cards. Preserve all 335 originals, eight already-reviewed full feats, every description/effect/legacy alternative, original questions, absent/null distinctions and prior labels. A real class-scheduled feat/ASI opportunity pays for a grant; merely reaching a total level, possessing an item, meeting prerequisites or reading this register gives no selection. Unqualified Level means total character level; named Warrior or other class gates use that class level. Check printed permanent ability, actual feat ownership and credential prerequisites at acquisition. A half-feat ability increase is capped at 20, contributes zero rather than reducing a higher score, and does not grant another selection. The pure ASI option requires its full legal allocation. Numerical skill prerequisites require actual proficiency and permanent governing ability modifier plus the applicable normal PB or replacing Expertise contribution, excluding equipment, temporary modifiers, situational feats, Help and advantage. Preserve the acquisition snapshot. Later prerequisite loss does not erase a grant; ongoing equipped/active/body requirements can disable its use.\nNEW nonrepeatability: each identity is acquired once, except the explicitly repeatable ASI, Armor Proficiency for a distinct missing tier, Resilient for a different save, and Weapon Focus for a different actual weapon type. Elemental Affinity/Adept, Spell Focus and other chosen-type feats do not gain unprinted repeatability. One same-named source represented in two catalogs is not two selections. The twelve explicitly mapped Warrior mutation-feat pairs are one paid identity; their actual class gates and active-mutation conditions control as stated in HM rows. Other shared names do NOT merge class, ancestry, item, feat, ordinary-spell or supplement permissions.\n\nWarrior mutation-feat acquisition uses the equipped-loadout rules in the Warrior engine as corrected by FEAT327-ACQ-02: at most two equipped Advanced mutations per actual tree and at most one equipped Apex mutation across all trees, within the actual unlocked total slots. Dormant equipped mutations count toward those ceilings. Evaluate each feat's equipped and active prerequisites only at the acquisition or use-time checkpoints that its exact procedure specifies. A temporary all-equipped activation does not supply an equipped prerequisite, slot, mutation, class level or feat opportunity. Preserve each feat's acquisition snapshot and existing ongoing operating conditions.",
    "basis": [
      "All nine sharedProposal objects",
      "CHARACTER_CREATION_PLAYTEST.md",
      "MAXIMUM_HP_PLAYTEST.md",
      "heritage_mutation/originalWarriorCounterpartPairs"
    ],
    "exactCardApproval": false
  },
  {
    "id": "FS-06",
    "title": "One clock, deadlines, rests and initial uses",
    "disposition": "ADOPT EXPLICIT NEW COMPLETION",
    "wording": "Use EX58's single elapsed clock, eight-hour Watches, actual task minutes, two-active-work-Watch ceiling and scheduled Rest. A change of scene, gate, holder, location, initiative, class representation or calendar label does not reset a resource. SR/LR in these new procedures mean the actual beneficial completed owner rest, with one beneficial Long Rest per 24 elapsed hours and at most two beneficial Short Rests between beneficial Long Rests. A qualifying long rest restores a short-rest allowance as already governed. Extra safe Rest paying Rest Debt alone provides no second resource recovery. Recipient-rest limits use the actual named recipient's rest epoch.\nNEW initial acquisition completion: the newly acquired limited-use feat begins with its specified full finite allowance, unless it expressly starts empty (such as accumulated stacks/charges). Reacquisition/alias duplication cannot initialize it again. An increase in a PB-based maximum increases capacity only, not current unspent uses. Genuine maximum-HP/RP/RC, Hit Die, reserve and slot changes never heal or refill unrelated current values.\nUse each explicit own-turn/any-turn/round predicate literally. A per-round allowance has one numbered global-round identity; extra turns do not refresh it. A default 'your turn' feat allowance uses the owner's regular interval unless its exact source direction expressly retains any actual turn. Newly completed missing durations use the next future original regular marker specified by the row, not the already-underway marker, retaining virtual/absolute deadlines across schedule changes. Outside initiative use the governed six-second phase without double ticks. A missed trigger is not queued for later. An early ending does not refund time or a use.",
    "basis": [
      "EX58 FL-03",
      "CLASS_PLAYTEST_RULES.md",
      "TEX-ADD regular-turn recharge correction",
      "all cohort resource conventions"
    ],
    "exactCardApproval": false
  },
  {
    "id": "FS-07",
    "title": "Damage, current capacity, healing and causal budgets",
    "disposition": "ADOPT EXPLICIT NEW COMPLETION",
    "wording": "Keep the reviewed damage/prevention/temp-HP/HP/Wound/death order and exact immunity/resistance/interception windows. Numeric actual damage means actual normal HP lost plus actual temporary HP absorbed, excluding overkill, damage prevented and mere state assignments. That metric never defeats an explicit no-resource origin, no-trigger ward/temp-HP rule or other causal prohibition: only source-qualified events can fund a resource benefit. Preserve those flags through every descendant. Capacity changes are not damage or healing. Ordinary healing observes actual blockers, modifiers, finite reserves and the Critical ceiling; direct state recovery is identified separately and remains subject to broad HP-gain prohibition. A successful stabilization or life-state change does not silently remove Wounds, Prone or another unconsciousness cause.\nNEW common anti-loop binding for the new feat rewards: preserve original actor, paid event and target; no staged cooperative threat, vanished/no-resource body, copied packet, reflected retaliation, cost damage or manufactured repeat kill supplies another free resource, attack, healing conversion or reset. Explicit independent printed exceptions are listed in the relevant row, not inferred by name. A root's refunded RP cannot exceed the real unrefunded payment eligible for that particular refund, and headroom still caps restoration. One refund record cannot be spent twice by Arcane Resonance and Arcane Recall. A new feat supplies no RP pool. Reactions require actual availability; specifically passive post-zero registration/recovery exceptions do not grant an Action or Reaction at zero HP. Automatic death processing still precedes later generic regeneration unless the exact source supplies the narrow earlier recovery window.",
    "basis": [
      "HEALING_DEATH_PLAYTEST.md",
      "MAXIMUM_HP_PLAYTEST.md",
      "BODY_EQUIPMENT_PLAYTEST.md",
      "CLASS_PLAYTEST_RULES.md",
      "LRX spell records"
    ],
    "exactCardApproval": false
  },
  {
    "id": "FS-10",
    "title": "Actions, command channels, mounts and personal movement",
    "disposition": "ADOPT EXPLICIT NEW COMPLETION",
    "wording": "Keep one additional FULL Action per creature/numbered round and the existing prohibition on additional Actions generating another additional Action/Bonus Action/Reaction. A source that explicitly grants a separate later Bonus Action has only its named window. Free attacks are not full Actions and cannot recursively grant other free attacks unless an exact existing exception says so. Ordinary Attack Action, card technique, weapon attack, spell attack and cantrip are not interchangeable labels.\nUse one physical creature identity, controller record, movement pool and authoritative phase. All controlled companions retain the governed shared Bonus Action command and one offensive/control companion action per owner/round. A source may command two bodies for nonoffensive actions only where stated; it does not grant two offensive actions. The feat owner must actually send the required audible/visible/mental channel; known language, trained signals, Silence and source range matter. Existing Tinker devices use actual reviewed channels and shared budgets.\nA bonded animal may be a mount only if its actual body, training, size, seat, tack, load and access meet EX58. It does not gain a second phase for being both companion and mount. Register the applicable EX58 mounted-control phase before operation; do not switch schemas midround to obtain unused budgets. Unmounted feat companions use the explicitly supplied after-owner-regular-turn phase. Mount and rider remain separate targets and actor budgets. Cavalry adds10 to each ACTUAL existing mount locomotion Speed while legally ridden, before applicable burden, terrain and later multipliers; it creates no mode, carrying capacity or engine. Route pace uses the actual resulting limiting profile under EX58, not a second free journey. The rider's being carried is not personal walking, Dragoon Momentum or a movement-cost discount. Mount/dismount uses the actual half-current-walk movement cost, access, one-per-regular-interval allowance and fitting seat; an extra Action does not reset it.",
    "basis": [
      "EX58 TR-03/04/05 and transport profiles",
      "CLASS_PLAYTEST_RULES.md",
      "Ranger/Dragoon/Tinker current engines",
      "BODY_EQUIPMENT_PLAYTEST.md"
    ],
    "exactCardApproval": false
  }
]
```

## S5 — ACQ-03 acquisition-scope and later loss

Path: `docs/audit/2026-10-08/full-game/FEAT327_ACQ_03_GPT_ADDENDUM.md`

SHA-256: `c0987fdca662fcd0dd4459358fdd4b02de178e0a560b9d9702fe16269af470bb`

Location: `lines20–34`

20: Casting-prerequisite snapshot bridge — FEAT327-ACQ-03. NEW acquisition completion. Apply this bridge only to an actual feat acquisition prerequisite or its expressly required acquisition selection, subject to a more specific acquisition rule in that feat’s final procedure. A casting prerequisite requires a source-qualified personal spellcasting entitlement already acquired by the character and still retained at the acquisition snapshot. Record the actual grant, exact spell identity and source version, casting route, relevant class/rank gates, and the repertoire or preparation evidence that makes that route available. Class-level capacity, an RP or RC pool, a spell merely appearing on a permitted list, ownership of a spellbook or scroll, item-enabled casting, an unacquired class feature, and the prospective benefit of the feat being acquired do not by themselves supply this entitlement.
21: 
22: Retained entitlement versus immediate casting legality. A retained personal grant does not lose its acquisition credential merely because its renewable charge is currently empty, RP is insufficient, components or a suitable casting hand/voice are unavailable, the character is unconscious, or an existing temporary prohibition or suppression prevents casting. Ignore those immediate-use impediments only when evaluating this casting credential. Do not refill a resource, restore components, lift a prohibition, perform a cast, or establish that the feat-selection transaction itself is otherwise lawful. Actual casting still requires every current action, component, body, target, range, payment, concentration, strain and source-specific condition. An expressly ongoing or currently-active prerequisite in a particular feat remains an ongoing or currently-active prerequisite.
23: 
24: Qualifying repertoire and preparation. For a known-spell route, require the exact spell actually learned or personally granted, with its applicable source gates satisfied. For an ordinary prepared route, require the spell actually prepared at the snapshot, an actually acquired always-prepared grant, or another already-established source exception that authorizes casting it without ordinary preparation. An unprepared spellbook entry and the ability to prepare or substitute it later are insufficient for that spell’s credential. A future study period, rest, substitution, level-up selection or other repertoire change cannot be anticipated. A ritual route qualifies when the character actually possesses its ritual-casting permission and the particular spell meets that permission’s exact book, tag, rank and other repertoire requirements; no ritual need already have been cast. Do not extend one spell’s ritual overlay to another spell. Loss of a required repertoire source follows the actual class procedure: Wizard’s surviving prepared matrices remain available under its spellbook-loss rule, while an unprepared lost-book entry is not made available by merely planning its reconstruction.
25: 
26: Generic and specific predicates. “Spellcasting ability,” “Actual personal spellcasting ability,” and “Ability to cast at least one spell” require at least one qualifying personal spell route under this bridge; a qualifying rank-0 spell is sufficient. “Ability to cast cantrips” requires a qualifying rank-0 route. A named-spell prerequisite requires the exact required spell identity and permitted source version, not a similarly named class technique or item effect. A school prerequisite requires an actual matching school on the qualifying route. A rank prerequisite uses the spell rank actually supplied by that route and the final normalized predicate’s existing exact-rank or minimum-rank comparison, not total character level, maximum possible class rank, available RP, damage, or a higher price paid for a lower-rank spell. Where one predicate combines identity, school, rank or route restrictions, one qualifying route must satisfy that complete predicate; do not combine different routes’ most favorable fields. Distinct alternatives retain their existing AND/OR structure.
27: 
28: Removal, replacement and expiry. Reevaluate the retained grant and repertoire for every new feat acquisition. An actually removed, expired or lawfully retrained-away grant cannot support a new acquisition unless another independently qualifying route exists. Replacing a prepared matrix removes that ordinary prepared route for later snapshots unless another valid route to the spell remains. Temporary suppression or renewable depletion is not removal. Exhausting a genuinely nonrenewable permission follows its actual source: if the permission terminates, it no longer supplies a retained route. Under FS-01, a previously acquired feat keeps its original acquisition snapshot; later prerequisite loss does not erase that historical acquisition or waive any of the feat’s actual ongoing operating conditions.
29: 
30: Unassigned schools and required school choices. Preserve each source spell’s actual school value, explicit null or absent field. An absent, null or unassigned school is not Universal, Enchantment, Evocation, a wildcard, or a school inferred from damage type or a grant’s name. A school-unassigned personal rank-0 grant can satisfy generic spellcasting and cantrip predicates, but cannot itself satisfy a school-specific predicate. Supplementary Spell Focus additionally requires its mandatory permanent selection of an actual school supported by at least one qualifying acquired spell route at that same snapshot. Satisfying its generic spellcasting prerequisite without a supported school choice is insufficient to complete its acquisition. Another genuine route may support that choice. Subsequent loss or suppression of the supporting route does not reselect the school or erase the original acquisition; later benefits still require actual eligible casts through that fixed school.
31: 
32: Authored-candidate evidence versus runtime selection. For authored-candidate qualification, use the exact complete controlling authored spell procedure and its actual source-access binding, supported by the applicable review and fulfillment chain. A preserved earlier blocked catalog snapshot does not override an explicitly reviewed, version-linked operational descendant merely because the original remains unchanged. A separate selectionEnabled:false or disabled runtime adapter does not by itself invalidate that authored evidence. Neither a favorable label nor the existence of a reviewed spell supplies the character’s personal grant or repertoire history. Genuinely unfinished, null, unsupported or operationally unavailable payloads remain unavailable as positive casting witnesses. Preserve original statuses and live selection flags; this acquisition bridge neither enables runtime selection nor promotes another card.
33: 
34: Snapshot and payment. Preserve the exact prerequisite text and record the qualifying grant, spell/source/mode, actual school-field state and rank, repertoire/preparation or ritual basis, applicable class gates, controlling authored-procedure reference, and acquisition time. Temporary use blocks may be recorded separately but are not treated as grant removal. Missing grant, preparation, source-version or required-school evidence leaves that predicate unestablished rather than assumed true. Check all other printed ability, level, ownership, credential and earned-opportunity requirements independently. The feat’s own prospective spell grant cannot bootstrap its prerequisite, and one paid opportunity cannot fund two acquisitions.

## S6 — Complete combat encounter resources and time/event ordering sections

Path: `DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md`

SHA-256: `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6`

Location: `lines27–70`

27: ## Encounter and action resources
28: 
29: Establish terrain, light, hazards, objectives, exits and cargo; determine awareness; roll `d20 + DEX modifier + legal bonuses`. Highest first. Players choose player/player ties; the Director resolves ties involving NPCs. Keep the resulting ordered slots for the encounter. A round represents approximately six seconds. A **regular turn** is a creature's normal initiative slot even if it cannot act. An extra turn is distinct.
30: 
31: A turn normally permits movement, one Action, a Bonus Action when an actual rule grants a use, and one ordinary free object interaction. A second ordinary interaction or an Action-time object activation uses an Action. Brief communication is not an extra Action. Conditions and specific features may restrict these permissions.
32: 
33: The shared limit is one **extra full Action per creature per numbered round**. Such an Action cannot grant another extra Action, Bonus Action or Reaction. This cap is independent of Reaction timing. Extra turns do not by themselves refresh Reactions, recharge, periodic ticks, recovery ticks or the regular-turn allowances defined here.
34: 
35: **Reaction interpretation.** Begin an encounter with one available Reaction unless surprised or otherwise prohibited. Refresh at each regular own-turn start; never at the numbered round boundary or an extra turn. A late-initiative creature can therefore react before its first turn, refresh, and react again in the same numbered round. A legal trigger, available resource and all feature prerequisites are still required.
36: 
37: **Explicit additional Reactions.** A reviewed card can grant a separate limited use without refreshing the ordinary resource. Warrior Mind Shock supplies its stated once-per-duration non-attack Reaction; spending one resource does not consume/reset the other. Surprise, Incapacitated and Focused still restrict both. It grants no Counterspell knowledge or waived costs. Extra turns refresh neither. Per-dose reapplication/stacking and other specific grants remain part of the class semantic pass.
38: 
39: **Surprise — V6 plus NEW Bonus Action clarification.** On a surprised creature's first regular turn it cannot voluntarily move or take an Action or Bonus Action. It cannot react until that turn ends. Its slot, durations, passive effects, concentration, periodic effects and recharge still occur. Surprise alone is not Incapacitated or Unconscious. Brief communication and an otherwise legal simple free interaction remain possible.
40: 
41: **Entry — NEW.** Standard end-round reinforcements roll/receive initiative and first act next round. An explicit midround entrant acts this round only if its complete ordered slot is still upcoming; entry during that exact slot counts as already passed. It has its initial Reaction unless prohibited. A summon-specific timing rule overrides this generic entry procedure.
42: 
43: After the final slot, resolve Core's end-round hazards, reinforcements, morale, objectives and boss phases. Conclude the scene with surrender, capture, pursuit, harvesting access and noise consequences under their own rules; winning initiative does not resolve those automatically.
44: 
45: ## Time and event ordering — NEW
46: 
47: For a duration created in initiative, record the relevant original regular start/end marker. Existing effects keep that **virtual marker**, repeating every six seconds if the creature leaves or changes initiative. Reordering, rerolling, extra turns, death/removal or leaving/reentering initiative never restart an existing duration. New effects use the current schedule. Source death still ends concentration, a source-dependent aura/tether or an effect explicitly ending on death.
48: 
49: - A bare hostile target-bound **N rounds** ends at the Nth future regular target-end marker. An in-progress target turn's current end does not count.
50: - A bare self/source buff, ally-targeted buff or source-controlled aura **N rounds** ends at the Nth future source-start marker. Explicit target-turn, pulse or absolute timing overrides this default. Activation during source turn 1 for three rounds ends at source turn 4's start.
51: - **Next turn** means the next future regular turn of the named creature, not the current turn's still-upcoming end. An unqualified next turn refers to source/user under the existing shared rule. Explicit “this turn” can include the current turn.
52: - An outside-initiative bare N-round effect instead gets an absolute application-time + N×6 seconds deadline. Entering initiative preserves that deadline.
53: - Explicit periodic profiles retain their registered clocks and tick counts. Never create a second timer merely because a generic duration rule also exists.
54: 
55: The [exact GPT review](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_EXACT_FINDINGS.md) confirms ally-buff source clocks and excluding the current turn for explicit next-turn endpoints. The helper excludes a specific current-end marker only if that marker would otherwise be selected: application during a turn at time1 with end3 excludes3 and selects9; application at/after3 also selects9, without erroneously skipping again to15.
56: 
57: At a regular turn's **start**, resolve in this order:
58: 
59: 1. Expire start-ending effects and apply immediate state changes from those expirations.
60: 2. Refresh Reaction; tick regular-start recharge/non-action clocks.
61: 3. Resolve already-due absolute state recovery if now legal, including a previously blocked Stable recovery deadline.
62: 4. If still alive, dying and at 0 HP with death saves, make that turn's death save.
63: 5. Resolve other start effects and periodic events in application order.
64: 6. Begin voluntary turn decisions.
65: 
66: At **end**, resolve triggered effects, due damage, saves and maintenance before end-ending effects expire; then the slot finishes. No extra turn creates another regular marker. The caller must not reuse a resolved marker.
67: 
68: For simultaneous effects, earlier application timestamp precedes later. For simultaneous components of one source, its printed internal order controls; otherwise use stable application sequence, with source/mechanical ID as a final tie-break. Record that sequence when creating the effects. Beneficial/harmful labels do not change priority. Periodic family arbitration happens once per family/marker before its damage, retaining the family registry's consumed loser ticks.
69: 
70: Examples: dying at 0 rolls its death save before ordinary start-turn healing; a fatal death save is not undone by ordinary healing. Stable at 0 skips the save, then start-turn damage can break Stable. A natural 20 can restore 1 HP before a due Bleed drops it to 0 as a new drop event. If Decay expires while a Stable recovery deadline is already due, the old deadline resolves once without rerolling recovery time.

## S7 — Complete class reading/action/target/control/damage/companion sections

Path: `DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md`

SHA-256: `adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81`

Location: `lines5–39`

5: ## Reading a class card
6: 
7: Use the class's own level, never total character level, for gates and effects. **L** means that class level; **S** is 1/2/3/4 at class levels 1/5/11/17. **M** means max(1, the class ability modifier), for effect a mounts only. Attacks use d20 + normal character proficiency + the actual appropriate ability modifier. Class save DC is 8 + normal proficiency + actual class ability modifier. Negative modifiers still apply to attacks and DCs. One tile is 5 ft. Fractions round down unless specified. Distances cannot be negative.
8: 
9: A weapon attack uses its usual ability, weapon die and damage type. A technique that says “make one weapon attack” replaces your Action with that attack; it does not also grant a normal Attack Action or Extra Attack. Generic attack-speed language has no effect beyond the exact attacks printed in the draft. A spell attack uses the class's stated casting ability. Natural 1 misses and natural 20 hits/critically doubles damage dice; flat bonuses do not double. A save succeeds at DC; “fails by 10” means the total is at least 10 below DC. Critical-range improvements never stack; use the broadest one.
10: 
11: An ability is known only if granted or selected by the draft schedule. Satisfy all printed prerequisites, target legality, action availability, recharge and resource costs before spending anything. A failed legal attack/save attempt still pays; an illegal activation spends nothing. No resource goes below 0 or above its cap. A class feature name shared with a spell does not grant both versions; use the version selected, with its own cost and timing. Names and source text are preserved; the current card is the operational draft.
12: 
13: ## Action and timing limits
14: 
15: One regular Action, one Bonus Action if a feature permits it, normal movement and one Reaction between starts of your turns. A free trigger costs no Action only if expressly stated. All grants share **one extra full Action per creature per round**. An extra Action cannot grant another Action, recharge itself, or start another extra-Action grant. It supplies no extra Bonus Action or Reaction. A card granting additional attacks is not permission to repeat all class riders on every hit: obey each rider's frequency.
16: 
17: Recharge N sets a counter to N after use; reduce once at the start of the owner's regular initiative turn, whether able to act or not. Extra turns/Actions do not tick it. Outside combat tick once per 6 elapsed seconds, without double counting. Recharge 2 used on turn 1 is ready on turn 3. A positive counter can be reset/shortened at most once per ability per round. Zero counters are not legal reset targets and expend no reset use. Resets never restore RP or per-rest uses or grant an immediate activation.
18: 
19: An encounter is a genuine scene of uncertain opposition chosen by the Director, not a player declaration used to reset resources. No encounter gain from attacking allies, one's summons, harmless animals, helpless captives or reused corpses. Out-of-combat abilities retain all printed costs and time. Short-rest means a completed uninterrupted hour of permitted recovery; long-rest means a completed 8-hour Rest Watch. This time convention is a draft integration. Expedition pressure, supplies, safe locations and rest debt still matter. A long rest also refreshes short-rest uses; a short rest never refreshes long-rest uses. Weekly uses refresh after seven full in-world days, not repeated rests.
20: 
21: ## Targets, concentration and control
22: 
23: Unless expressly stated, perceive the target, remain within range and have line of effect; total cover blocks targeting. “Ally” includes self unless it says OTHER. A list cannot contain a creature twice. Select up to the printed limit; an empty target list is not a valid way to farm activation benefits. Zones remain at their chosen point unless described as an aura; allies can leave and lose their benefits. An aura requires its owner conscious unless the card supplies a bounded exception. An effect ending at “end next turn” means the affected creature's next turn only when the card says target's; otherwise the user's.
24: 
25: One concentration slot for all spells, Chants, Veinweaves, forms or zones that require concentration. Starting another ends the old before the new effect resolves, except for an explicit limited linked-effect rule. Damage prompts CON save against max(10, floor(damage/2)); incapacitation or a failed save ends concentration. The round-down convention is a deliberate pilot interpretation. Concentration does not demand a Bonus Action unless maintenance says so. For a paid 3-pulse effect, start is pulse 1; pay maintenance on each of the next 2 regular turns by turn end for pulses 2/3. Missing payment ends it at that turn's end; otherwise it ends at start of turn 4. No repeated start triggers on maintenance.
26: 
27: Forced movement does not provoke opportunity attacks unless explicitly stated, cannot place a creature inside solid matter, and stops at an obstacle. Grapples use the card's save/DC, can be escaped with an Action and STR(Athletics) or DEX(Acrobatics) against that DC, and end beyond reach. A root sets Speed 0 but does not remove Actions. Slows reduce Speed to minimum 0. Silence blocks verbal spells/audible abilities, not all thought or all class features. Charmed effects never determine a player's beliefs; use only the printed action restrictions.
28: 
29: No repeated hard denial without a new save and cost. For this class suite, a creature can suffer **Stunned, compelled loss of its whole Action/turn, or equivalent hard denial from a given character at most once per encounter**, across that character's class features; later such riders fail while damage and soft riders resolve normally. Record source and target. This draft guard is broader than the older Oracle-only ceiling and is an explicit balance proposal. Reaction denial, Speed reduction, penalties and Frightened do not count as whole-turn loss. Do not silently waive boss immunities, legendary defenses or anatomy.
30: 
31: ## Damage, healing, stacking and companions
32: 
33: Roll once for each shared area/pulse and apply saves/defenses to each target separately; separate attacks roll separately. Halve once for a successful save and apply resistance/immunity normally. Same-named conditions/bonuses do not stack unless a printed cap allows it; same-stat flat bonuses from these class techniques use the strongest. Different resources remain separate. Damage reduction from these class features uses the strongest flat reduction, then applies resistance; it cannot create negative damage or healing. Temporary HP never stack; choose the larger remaining amount. Immunity is not reduced resistance.
34: 
35: Repeated permanent HP recovery must consume finite RP, a per-rest use or another finite resource; a combat-generated gauge alone never enables unlimited healing. Healing cannot exceed maximum HP or erase Wounds, death consequences, debt or Corruption unless explicit. Downed is living at 0 HP; dead is different. Resurrection requires a willing soul and sufficiently intact body, obeys its time window, cannot create a duplicate and never refunds the feature on failure to meet known prerequisites. Sacrificial HP is actual unpreventable loss, cannot be redirected or paid with temporary HP, and is not damage for resource triggers. It cannot reduce the donor below 1 unless a card expressly grants a death-triggered effect.
36: 
37: No damage/healing copy repeats the source's costs, procs, resource generation, critical bonus dice, buffs, actions, cooldown resets or duration. Compute fractions once, capped at 100% of one stored source unless an explicit card states a separately priced higher amount. Copies still cause ordinary damage consequences, concentration checks and death. A copy cannot copy another copy. A target/source record must refer to an actual resolved event, not merely a known ability name.
38: 
39: Where a class card calls for a **standard companion** without a more specific profile, use: Small or Medium; AC 12+floor(PB/2); HP 2 L; walking Speed 30 ft; saves equal owner's PB; one melee or ranged attack (reach 5 ft/range 30 ft) at owner's class attack bonus, damage S d6 of the printed type. It has no independent class features, resources, loot, death triggers or extra turns. All companions belonging to one character share one Bonus Action command and **one damaging attack/action total per round** unless a specifically priced feature grants more. Without a command they move and Dodge. Act immediately after owner. A standard companion lasts 1 minute, disappears at 0 HP and cannot be healed for free by dismissing/resummoning. The creation cost must be paid again. Creature-specific stat blocks override this profile only where explicitly printed.

## S8 — Current turn/rest teaching boundary

Path: `DescentReviewChanges/ReviewBible/docs/playtest/CLASS_RESOURCE_REFERENCE.md`

SHA-256: `9b926a9e07c60ba579edb6b1ffbbbcbeac969e93fb4f8e446621544e988e4b9e`

Location: `lines185–191`

185: ## End a turn, end an encounter, finish a rest
186: 
187: Resolve each deadline at its actual source-defined start, end or elapsed-time endpoint. Tick round-recharge counters once at the start of the owner's regular turn, even when the owner cannot act, under the [timing rules](../mechanics/CLASS_PLAYTEST_RULES.md#action-and-timing-limits). A turn end, extra Action or extra turn does not supply another regular-turn recharge tick. Outside initiative, use the same source's six-second elapsed-time procedure without double counting a boundary. Only a positive counter can be reset or shortened, at most once per named ability per numbered round; a reset is neither a resource refill nor an extra activation.
188: 
189: At encounter end, clear only what the appropriate engine says to clear. Check pending effects and actual deadlines separately. Do not restore RP, HP, Dissonance, stock, stored Echoes or per-rest uses simply because combat ended.
190: 
191: For recovery, record the actual rest and completion time. The current [rest limits](../mechanics/STRAIN_PLAYTEST.md#recovery-and-actual-elapsed-time) allow at most two beneficial short rests between beneficial long rests and one beneficial long rest per 24 elapsed hours. Short rests require one hour; long rests require eight. Supplies, safety and interruptions still matter. Apply each class's own eligible recovery once, retain unrecovered histories, and record the new current amounts without replacing the old entry.

## S9 — Explicit submitted qualification and all four questions

Path: `docs/audit/2026-10-08/full-game/FEAT335_FLORA_USE_SCOPE_QUALIFICATION.json`

SHA-256: `d736918ce95d7789bbabea6f797235425fb826b6d53c48bfcd99ba4858cda939`

Location: `whole object`

```json
{
  "report": {
    "path": "docs/audit/2026-10-08/full-game/FEAT335_FLORA_USE_CHECK.json",
    "bytes": 774121,
    "sha256": "604a615723b6b9593928caa4b89a6f57f5fe0f6de6ed8966a5451fc61a7d942a"
  },
  "status": "bounded-model-evidence-with-explicit-unapproved-inference",
  "checks": 114,
  "histories": 23,
  "qualification": "The report is preserved verbatim. Its newRules:0 does not approve the fixed-at-first-creation level10 inference; the two named growth checks prove local model behavior only, pending FLQ-03. No complete Flora use, FXC04/09 or full feat approval follows.",
  "questions": [
    {
      "id": "FLQ-01",
      "question": "If the exact personally possessed casting route fixed at Flora acquisition is later unavailable, what happens to new creation, existing plants, their DC, commands and armed automatic entry? Distinguish permanent loss and temporary suppression only where current sources do. The numerical DC projection alone does not authorize a use; do not invent a fallback route or reacquisition."
    },
    {
      "id": "FLQ-02",
      "question": "A level10+ first plant is destroyed, uprooted, burst or otherwise ends before its original minute deadline. Does its still-unused second paid-Action creation permission end immediately or survive until that deadline? The phrase before that first seedling expires may not settle early termination. Existing first body must remain ended and every paid use/deadline/history must remain conserved."
    },
    {
      "id": "FLQ-03",
      "question": "A character creates at total8/9, then genuinely reaches total10 before the first plant original deadline. Is the second-creation eligibility fixed at commitment or live while that use remains open? The local level8-creation-then-level10-capacity history assumed fixed eligibility; this is an UNAPPROVED inference, not a source ruling. Decide the governing rule before this check is relied on. No charge/body/HP refill follows merely from capacity growth."
    },
    {
      "id": "FLQ-04",
      "question": "For the later split command/attached-phase implementation, bind temporary owner incapacity, owner death and loss of command channel after a legal commitment to the existing actual companion sources. The current local model collapses a legal command and its immediate phase into one operation, so it does not prove intervening-event behavior. State any genuinely missing Flora-specific rule explicitly as NEW; do not silently inherit Animal Companion death or release rules."
    }
  ],
  "candidateChanged": false,
  "fullFeatExactApproved": false
}
```

## S10 — Prior completed acquisition-audit Flora findings

Path: `docs/audit/2026-10-08/full-game/feat335-acquisition-audit-01-verdict/FINDINGS_AND_REPLACEMENTS.json`

SHA-256: `1fda0aff5c5b27f9b0a8b8262cbf1aa0a92e41bca6acc3299c0b25fd313849cd`

Location: `/findings IDs FAA-01 and FAA-02`

```json
[
  {
    "id": "FAA-01",
    "classification": "KEEP_SOURCE; CORRECT_LOCAL_MODEL_AND_SURFACE_EXISTING_REQUIRED_SELECTION",
    "affectedIds": [
      "conjure_flora",
      "trapcasting"
    ],
    "source": {
      "path": "DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/supplements.json",
      "sha256": "59635b07655f06f4d3fab872b2665638a683702ad89a5322fe2df426fcd96146",
      "pointer": "/groups/6/value/floraBody/dc",
      "quote": "At acquisition select one actual possessed spellcasting route; use DC 8+current PB+that route’s current ability modifier. No phantom Wisdom/Spellcraft statistic. Actual source-specific component/target defenses still apply."
    },
    "problem": "The current named-chain helper accepts Conjure Flora without its mandatory acquisition-time DC provider, rejects an explicit choice, and its initialization omits the provider. Trapcasting histories purchasing that parent inherit the incomplete parent record. The Verdant Bond-only parent path is unaffected.",
    "replacementWording": "KEEP the already-operative SUP-07 floraBody/dc acquisition requirement: at acquisition permanently select and record one actual possessed spellcasting route as this feat's DC provider. Use DC 8 + current PB + that route's current casting-ability modifier; do not invent Wisdom, Spellcraft or another default. This source choice is separate from the later seedling mode/burst-type choice. Ownership initializes only the finite creation allowance and body capacity, with no plant, pending additional creation, command or active effect. All printed acquisition predicates and the actual earned feat opportunity remain required.",
    "newRule": false,
    "evidence": "Actual paid Warrior4 Magic Initiate(Wizard) then Warrior8 Conjure Flora reproduces missing-provider acceptance. Corrected in-memory helper rejects missing/foreign providers before payment and retains the chosen route with empty body state.",
    "closure": "Apply guarded current text/model edits. In fresh descendant traces supply the real provider for every Conjure Flora parent; preserve old traces. Verify no body, no RP, no additional creation at acquisition and no refill on level10 capacity increase."
  },
  {
    "id": "FAA-02",
    "classification": "KEEP_FULL_SOURCE_MENU; CORRECT_LOCAL_MODEL_FILTER",
    "affectedIds": [
      "conjure_flora",
      "stormcaller",
      "voltyros_pact",
      "soul_cage"
    ],
    "source": [
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/supplements.json",
        "sha256": "59635b07655f06f4d3fab872b2665638a683702ad89a5322fe2df426fcd96146",
        "pointer": "/groups/3/value/Dragoon/featCastingAbility",
        "quote": "STR"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/supplements.json",
        "sha256": "59635b07655f06f4d3fab872b2665638a683702ad89a5322fe2df426fcd96146",
        "pointer": "/groups/3/value/Monk/featCastingAbility",
        "quote": "DEX"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/supplements.json",
        "sha256": "59635b07655f06f4d3fab872b2665638a683702ad89a5322fe2df426fcd96146",
        "pointer": "/groups/3/value/Thief/featCastingAbility",
        "quote": "DEX"
      }
    ],
    "problem": "actual_casting_routes() rejects every supplied route whose actual source ability is STR or DEX. This narrows legitimately acquired personal routes. Soul Cage providers() delegates to the same helper. Existing INT/WIS/CHA-only witnesses do not establish the complete menu.",
    "replacementWording": "Validate a route’s canonical ability against STR, DEX, CON, INT, WIS and CHA only after its actually acquired source and qualifying repertoire have been established. Do not invent an ability or a CON route. The supplied current menus establish STR/DEX as well as INT/WIS/CHA. Voltyros INT fallback applies only when there is no actual casting source, not when an otherwise legitimate source has a nonmental ability.",
    "newRule": false,
    "evidence": "Source-qualified, separately paid Initiate(Dragoon), Initiate(Monk) and Initiate(Thief) witnesses reproduce the old rejection. Scoped corrected helper accepts them for Flora/Stormcaller and prevents false Voltyros INT fallback. This is not a cast or complete class build.",
    "closure": "Apply one guarded helper edit and add source-route boundary coverage for all four affected procedures. Fixed explicit INT/WIS/CHA, INT/WIS or INT/CHA menus on other feats stay fixed; do not widen them."
  }
]
```
