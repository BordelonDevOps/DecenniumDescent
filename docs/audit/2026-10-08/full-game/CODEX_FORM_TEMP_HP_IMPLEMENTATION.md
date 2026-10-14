# Form and temporary-HP exact implementation review

Codex → Calibration Review. The full175 source roles were individually discussed, then your12 boundaries and5 profile clarifications were reconciled. Here is the actual guide, all26 complete-source form profiles, executable helper and adversarial tests. Source integrity passes175+5 plus Druid metadata; originals/frozen class rules are unchanged.

The helper passed152 contract checks and1053 shield arbitration/damage-state scenarios. Scope is deliberately the selected interfaces, not all clauses of175 cards or a whole runtime. Nine explicitly unfinished named components remain deferred (TimeLoop; Chef/InspiringLeader/SoulCage; HarmonicBulwark; four transformation spells). BloodRitual target count, other feat clauses, item/anatomy matrix and natural-weapon interoperability remain separately visible.

Review actual code against your decisions, especially: payment before arbitration; linked versus independent riders; fixed/default expiry; no zero-grant identity; NecroticAffinity one event/after-resistance/pre-oldTHP prevention/post-final-packet grant; SpiritWalk never attacked; same-body Core damage and forced reversion; source-level gates and subtype choice; natural renewal/local Surges; shared Slam/recharge and rest uses; optional entry-only Broodspawn; independent Mooncursed ally shields. Look for implementation defects, atomicity problems and mismatches with the guide.

Integration contracts: caller certifies all source access, actual source-specific costs not debited by selected methods, legal geometry/targets, actual clocks/rests, exact AC compatibility, defense/roll resolution and final state after legal death replacement. Source-qualified full rider text is returned for canonical engines, not claimed executed by this helper. CreatureWorld is shared for form-bound swarm cleanup. Core tempHP scalar must match the canonical BufferLedger projection; after grants/removal caller updates its projection before subsequent Core use. ProtectiveProgramming uses a unique hit dependency removed after that hit, affecting only an accepted matching grant.

Do not treat passing tests as design approval. Please identify concrete defects or confirm closure of the selected reference interface, explicitly keeping the deferred components and whole game open. All records remain preserved.

## docs/mechanics/FORM_TEMP_HP_PLAYTEST.md
SHA256 e84c7abf385a242c4ae2e5f14d65e376fb3c15fc349b6f942452cf4f458ec2d4
```markdown
# Forms and temporary HP

**Implementation draft; GPT review and validation pending.** This overlay covers175 exact source roles, five support passages,26 Druid form profiles and selected common interfaces. It does not close full class cards, feats, ancestry, ordinary spell catalogs, equipment or the whole game. Original cards and historical text remain unchanged in the [source register](FORM_TEMP_HP_SOURCE_BINDINGS.md).

## One active shield

Temporary HP is a single active grant with its own identity, source, owner, recipient, remaining points, endpoint and explicitly attached permissions. A larger new offer replaces it; a smaller or equal offer is discarded. Equal values preserve the existing grant and its deadline. Discarded shields do not remain underneath. A rejected offer cannot lend its duration or linked rider to the winner. A zero offer creates no grant.

Pay the legal source's printed costs before comparing shields. Costs are not refunded because the new shield loses. Druid Buffer Reserve pays the entire offered amount, not just the increase over an existing shield. Preflight actual source access, targets, geometry, actions, components and resources before paying anything; illegal activations spend nothing.

Unless the source states a different shield lifetime, a grant ends at the recipient's next completed long rest. “Until lost” or “until lost or replaced” only restates depletion; it does not exempt a grant from that default. Explicit fixed deadlines and source dependencies take precedence, even when they outlast a long rest. An ongoing ability's general duration does not automatically shorten an instantaneous shield that it generates.

Temporary HP absorbs post-defense damage before normal HP. It is not healing: it cannot stabilize, revive, wake an Unconscious creature, remove Wounds, reset death counters or pay direct/sacrificial HP costs. A living creature at0 can receive it without gaining any of those benefits. A dead body is not a valid holder. A prohibition on HP healing does not implicitly prohibit a separately legal shield.

## Exact endpoints and riders

Use actual owner/recipient regular-turn markers, absolute deadlines and encounter identities, not extra-turn or copied clocks. Source-specific rules remain in the exact card; this table resolves the important ambiguities.

| Source | Shield endpoint / linked boundary |
|---|---|
| Crimson Bloodshield | End of its three owner turns. Its one Reaction is attached only to its accepted grant; depletion/replacement/expiry removes permission. |
| Bloodbond; Lingering Malice | Each trigger/pulse makes a default long-rest grant; ending concentration does not erase it. |
| Nature's Blessing; Dread Shelter; Nano-Aegis command | Start/cast/command shield uses default long-rest lifetime; Speed, DR and support mode keep their separate clocks. |
| Protective Programming | Offer before the triggering hit. Resolve that hit, then remove any remainder of this particular grant. A stronger unrelated shield that won comparison is unaffected. |
| Monk Support; Warder Arrow and capstone | Default long-rest grants. Permanent availability or an instantaneous attack is not a permanent shield. |
| Harmonized Core; Arcane Leech; Primordial Surge; King's Smite; Noble Bearing | Default long-rest lifetime, including the sources that merely say “until lost.” |
| Linked Ward | After the actual triggering packet, default long-rest grant. |
| Final Stand | After actual triggering packet; shield and triggered resistance end at the ally's next regular end. The redirection itself ends at the Paladin's next regular start. **New grammatical integration.** |
| Unbroken Covenant | Until the Lock ends; this clause is explicit in preserved source provenance. |
| Last King's Gift | After damage, until encounter end. Its existing death-prevention gate remains separate. |
| Soldier Rally Point | Shield until encounter end; next-save bonus only until Soldier's next regular start. |
| Soldier Rallying Cry | Encounter end. |
| Dragoon Bastion Descent | Shield until Dragoon's next regular start; resistance until used or that start; cleanse instantaneous. **New grammatical integration.** |
| Bear / Earth Warden | Bound to that form instance; no refill at renewal. |
| Mooncursed ally Howl | Independent default long-rest grants, surviving Druid reversion. **New bridge clarification.** |
| Overflowing Light | Original two-round endpoint; if this exact grant is still active with at least1 point, allow ending one actual Frightened, Poisoned or Staggered condition. Rejection, replacement, depletion or holder/dependency removal gives no cleanse. Mastery raises only the cap10→20. |
| Protective Verse | One-minute shield and a separate one-minute next-qualifying-save rider. The rider can survive shield replacement. |
| Arcane Sanctuary | Each accepted pulse until owner's next regular start or source end, whichever first. Its attack bonus is a separate zone effect. |
| Empowered Link | Half the eligible source numeric benefit, rounded down/minimum1 where applicable; shared benefit duration capped at owner's next regular end. It cannot share resources, Actions, resistance or other excluded effects. |

Other explicit minute, round, turn and encounter endpoints retain their exact source wording. Cleric return shields, Crimson Pact, Mirrorsage Ward profiles, Mage Resonance Shield and Soulbound use their printed one-minute deadlines. Light Binding ends at owner's next regular end. Momentum Shield, Bolstering Presence, Aura Surge, Black Manifestation, Final Command, Mutation Surge and Wizard Abjuration use their printed next regular start. Momentum Barrier lasts one minute. A source with no specified shield endpoint uses the default.

King's Smite and Noble Bearing first resolve their shared internal component: when Noble applies, produce one Noble offer instead of a King's Smite offer. Each is half actual radiant Smite damage, rounded down, capped atS+M. Then compare that one offer with the recipient's existing shield. Their word “replaces” does not override an unrelated equal shield. Transfer-generated shields use the prior redirection package's actual absorbed amount, single-root restrictions and source caps; they appear after the causal packet and cannot retroactively protect it.

Each excess-healing point has one conversion owner. A source that explicitly converts its own excess has priority over external generic converters. Channel Life's packet forbids excess-to-temp-HP conversion by any provider; independent fixed shields still resolve normally. These are the existing healing interfaces, not a second excess pool.

## Druid: one body throughout

Keep your own HP, ability scores, saves, proficiency, conditions, personality and body identity. No copied monster statistics, separate beast HP or overflow pool exists. Base forms cannot speak; Arch/Hero forms can. Default size Medium, walking30, ordinary senses and operative character AC; change only the printed form traits. Hawk is Tiny; Bear, Earth Warden and Hero forms may be Large if legal space permits. No form invents hands or hand-based equipment use.

Equipment melds and cannot be used. **New AC bridge:** calculate `formNormalAC` from effects that remain operative in the form. Exclude worn armor's AC calculation, shield AC, effects requiring melded equipment use and unclassified item bonuses. A passive magical numeric item bonus requires the equipment adapter to certify anatomy compatibility. Apply the form's exact formula after that calculation, never adding worn armor again. Equipment returns in its prior state on reversion; shifting never repairs, reloads, restores charges or refreshes it. The full item/anatomy matrix remains unfinished.

Five Base forms unlock at1. Choose Circle at2; the chosen Circle's Arch path begins3, with its level6 feature. Circle Hero forms arrive at their printed10/14 gates. At11 attune at most two of the five Arch forms at a completed long rest. This is form acquisition, not another class promotion. All exact profiles and their complete original effects are in [the26-form register](../../data/playtest/druid_form_profiles.json).

At a completed long rest record:

- Shift uses2/3/4/5/6/7/8 at levels1/4/7/10/13/16/19. The conflicting historical schedule remains preserved.
- Buffer Reserve `2 × Druid level + M`.
- Form Surge Reserve `PB`.

These recorded reserves do not refill just because level, proficiency or form changes. At20 shift-use costs become zero, while Buffer Reserve, Surges and source-specific uses remain finite.

To enter a legal different profile, pay a Bonus Action and one shift use below20. End the previous instance and its dependent effects, create a fresh instance lasting10 minutes, clear Refrain's remembered spell/count, and retain Dissonance. Then resolve entry benefits. Bear offers `min(20, reserve)` and Earth Warden `min(30, reserve)`; deduct the whole offer even if a stronger shield wins. Both forms remain legal with reserve0. Natural attacks do not clear Refrain.

Early reversion costs a Bonus Action and no shift use; it does not clear Refrain. An early attempt to enter the already-current identical profile is rejected unpaid. At the exact natural10-minute endpoint, choosing to renew the same profile costs a shift use below20, with no new Bonus Action. Keep the same instance, local uses and existing effects; extend only the form endpoint. Do not refill its buffer, repeat entry effects, clear Refrain or extend a swarm/smoke effect's independent deadline. Declining renewal ends it normally. A later genuine reentry creates a new instance but cannot replenish shared reserves or per-rest abilities.

Elemental subtypes Air/Earth/Fire/Water and Vermin bat/ground choices are part of the profile identity. Switching subtype is a real new entry. Elemental entry additionally spends one of its two long-rest uses; natural renewal of the same subtype spends no new Elemental use. **New bounded profile completion:** Elemental attacks use lightning/bludgeoning/fire/cold respectively; Earth Warden's ordinary claw is slashing. An existing natural form attack without printed reach uses5 feet. These choices import no monster stat block.

## Attacks, specials and ending a form

One Action makes one printed natural attack, using currentPB+actualWIS and current Druid DC. A named Howl, Slam, Breath, summon, Smoke, Blast or Thunder Step replaces that Action's ordinary attack. Preserve each exact range, dice, save, condition and frequency. Natural/form attacks remain explicit categories; unrelated weapon-only procs are not authorized until the missing global taxonomy is reviewed. Expressly natural/form-qualified features such as Circle Forms and Primal Strike still work.

Local Surge use is keyed by actual form instance plus specific special. Legal commitment spends the opportunity and one Surge before rolls; miss/save/failure provides no refund. Mooncursed's ally and enemy Howls share one opportunity. Broodmother Spawn and critical-negation are separate opportunities, each requiring a Surge. Sky Serpent and Tempest's wet bonuses are attack riders, not extra attacks.

Broodmother's optional spawn exists only inside the entry transaction. A legal chosen spawn spends its Surge; an illegal or declined spawn spends none and does not undo entry. Once entry closes, there is no later spawn window for that instance. The separate critical-negation remains available. Carrion/Broodmother bodies use the reviewed creature profiles, independent lifetime and shared command budget; ending the parent instance ends them, while independent paid summons remain.

Earth Warden Slam's recharge2 belongs to the owner/source and persists across reversion/reentry. Tick only canonical regular starts or the protected six-second outside-initiative equivalent. Frost Breath's1/SR, Blazewood Blast's1/LR and Elemental entry's2/LR are likewise source/owner clocks, never form-instance refreshes.

Mooncursed ally Howl: choose and order one to three legal allies before rolling a shared2d8. Sequentially offer `min(roll, reserve)` to each; deduct each entire offer before arbitration. Roll12 with reserve9 offers9,0,0. No voluntary under-offering or free redistribution. Zero creates no grant. A legal Howl at reserve0 still spends its Action, Surge and local opportunity. Its accepted ally shields survive form ending and expire by the ordinary recipient long-rest rule.

Resolve an incoming packet once through existing defenses, temporary HP, real HP, Wounds and death/prevention rules. The form's traits remain for that whole packet. After actual same-packet replacement/prevention settles, actual0 HP, Incapacitated or death ends the form administratively. A valid “instead remain at1” prevents that zero-state reversion. Remove form-dependent shields/effects; never reroll damage in humanoid form. If unsupported after flight ends, start ordinary falling from the current location. Existing concentration and independent effect rules remain authoritative.

Beast Spells18 supplies verbal/somatic components for Druid spells in form but no access to melded materials. At20 waive only noncostly unconsumed components. Preparation, approved spell access, RP, Dissonance, actual components and the one-concentration limit remain separate gates.

## Bard, feats, ancestry and other transformations

Preserve Bard's distinct `resourceCost`, maintenance, recharge, Crescendo, C=max(1,CHA), tags and Echo fields. Lingering Notes is not a Chant start and triggers no other Bard effect. Chorus Shield is start-only. Renewal Crescendo shields only the initial recipient for1 round. Inspiring Performance Crescendo shields only on start until next start. Harmonic Ward offersS+2C on an initial Crescendo pulse andS+C on later paid pulses, each a fresh nonstacking grant until next start. It is not a Chant or Echo-eligible.

Empowered Summoning offers2PB at actual creation, using default lifetime and removal if the recipient entity ends; later PB changes do not refill it. Field Medic's actual healer-kit stabilization happens first, then itsPB grant. Blood Ritual offers2×level to self and exactlylevel to each eligible witnessing/blood-sharing ally, independent of whatever shield wins the self comparison. Allies' lifetime is1 hour; self uses default. No HP payment is invented for a drop of blood. Blood Ritual target-count completion remains visible. Chef, Inspiring Leader and Soul Cage need their named completion batches; no unknown quantities or “healing disadvantage” are silently filled in.

**Necrotic Affinity's new pipeline bridge:** after ordinary defenses and passive necrotic resistance, letD be qualifying spell/supernatural necrotic damage before existing temporary HP. A legal Reaction preventsfloor(D/2). Existing shields then absorb the remaining packet, and ordinary HP/death/Wounds/prevention settle. If still a legal living holder, offerfloor(D/2) afterward until the holder's next regular end. This is prevention, not healing/transfer. D=1 can spend the Reaction but creates no grant. An actual death creates no corpse shield; living0 can receive it without stabilization. The event may invoke this transaction only once. Other feat clauses are outside this selected component review.

V6 Consume Decay: Action, adjacent actual corpse/significant decay, level shield for1 hour,1/LR. The source does not consume a physical corpse; do not add a corpse-resource debit. Battle Cry: Bonus Action, hearing allies30 feet, level shield,1/SR orLR, default lifetime. Soul Drain: failed printedCON save, actual resolved necrotic damage becomes shield, default lifetime. **New anti-farm bridge:** no friendly, staged, trivial, summoned/created or repeatedly revived sacrificial targets for Soul Drain's grant.

Keep ordinary spell Resonance Shield, Heroism, False Life and Spare the Dying's existing operational overlays distinct from class names. Spare the Dying grants no shield. Heroism's shield ends with its spell. Harmonic Bulwark and the four transformation spells remain named unfinished source profiles, not newly selectable from this chassis.

Non-Druid transformation names inherit none of Shapeshift's rules or reserves. Lich is a physiology state; Mirror forms are the already-reviewed companion appearance/movement changes; Monk forms are defensive states; Warrior mutations preserve the same character with only their stated changes; Oracle Consumed has its exact intrinsic anatomy/gear-refit consequences.

Spirit Walk is one character with body/spirit positions and one HP, shield, condition, resource, concentration and action ledger. The spirit is never a legal attack target and cannot receive effects requiring a physical target. For a legal non-attack area including both representations, deduplicate by character identity and resolve once. Distinct independently created legal effect events remain distinct. Nothing transfers damage between the representations or creates another corpse.

## Reference implementation boundary

[Helper](../../tools/form_temphp_playtest_rules.py) implements one-shield identity/arbitration, clock/rest/dependency removal, linked permissions, Core projection reconciliation, Necrotic Affinity staging, source amount examples, spatial identity deduplication,26 profile gates, form transactions, reserve payments, local and owner-wide use clocks and ending dependencies. The caller still certifies actual access, all costs outside these selected methods, legal targets/space, anatomy-compatible AC, exact deadlines, defenses, rolls, concentration, source-specific riders and final state after death replacement. Use canonical ledgers rather than independent copies for each feature. Do not interpret returned source profiles as already applied attacks or conditions.

The complete equipment compatibility matrix, global natural-weapon taxonomy, full feat/ancestry/spell catalogs, Time Loop world conservation, human balance and the full runtime remain unfinished. All175 exact roles have been discussed; that is not a claim that every clause on every card is implemented or the whole game is complete.

```

## data/playtest/druid_form_profiles.json
SHA256 8f9a0ec5deff92ea836d558fff3ee5db5937c469186f27e469e014391c6ee424
```json
{
  "status": "DRAFT; 26 profiles, implementation review pending",
  "profiles": {
    "druid.base.wolf-form-striker": {
      "sourceId": "druid.base.wolf-form-striker",
      "sourceSha256": "7f886ec4aad2d5dc08b8eb79ac0ab2b2b83064449c2dd44a7a1ca73453864576",
      "sourceProcedure": {
        "id": "druid.base.wolf-form-striker",
        "name": "Wolf Form (Striker)",
        "className": "Druid",
        "band": "Base",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 1,
        "acquisition": "automatic",
        "activation": "Action attack; passive form traits",
        "cost": "One shift to enter",
        "rangeAndTarget": "Self; bite 5 ft",
        "duration": "While in Wolf",
        "frequency": "One bite/Action",
        "effect": "Speed 40 ft; advantage on hearing/smell Perception. Bite 1d8 piercing+WIS; target STR save against Druid DC or Prone, once/target/round. All damage remains your own HP.",
        "spellRank": null
      },
      "minimumLevel": 1,
      "circle": null,
      "archAttunement": false,
      "canSpeak": false,
      "size": "Medium",
      "mayLarge": false,
      "movement": {
        "walk": 40
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d8+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.base.bear-form-tank": {
      "sourceId": "druid.base.bear-form-tank",
      "sourceSha256": "d62efe277f4dfe0f210af41e3bb70eca6646d24f7501fa709a0269b5c4d349b7",
      "sourceProcedure": {
        "id": "druid.base.bear-form-tank",
        "name": "Bear Form (Tank)",
        "className": "Druid",
        "band": "Base",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 1,
        "acquisition": "automatic",
        "activation": "Action attack; passive form traits",
        "cost": "One shift; buffer drawn from reserve",
        "rangeAndTarget": "Self; claw 5 ft",
        "duration": "While in Bear",
        "frequency": "One claw/Action",
        "effect": "Gain up to 20 temporary HP from reserve; AC max(normal, 14). Claw 2d6 slashing+WIS+1. Buffer disappears on reversion and cannot be refilled through free shifting.",
        "spellRank": null
      },
      "minimumLevel": 1,
      "circle": null,
      "archAttunement": false,
      "canSpeak": false,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "floor",
        "amount": 14
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d6+WIS+1",
        "damageType": "slashing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 20,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.base.hawk-form-scout": {
      "sourceId": "druid.base.hawk-form-scout",
      "sourceSha256": "4534b24051e4e8540c7c4138f95d729e014a25be5cc554e72e25d10c0c9653b8",
      "sourceProcedure": {
        "id": "druid.base.hawk-form-scout",
        "name": "Hawk Form (Scout)",
        "className": "Druid",
        "band": "Base",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 1,
        "acquisition": "automatic",
        "activation": "Action attack; passive form traits",
        "cost": "One shift",
        "rangeAndTarget": "Self; talon 5 ft",
        "duration": "While in Hawk",
        "frequency": "One talon/Action",
        "effect": "Tiny, flight 60 ft, walking 10 ft, advantage on sight Perception. Talon 1d4 slashing+WIS; advantage if you descended at least 10 ft immediately before attack. No carrying Medium allies or casting spells before 18.",
        "spellRank": null
      },
      "minimumLevel": 1,
      "circle": null,
      "archAttunement": false,
      "canSpeak": false,
      "size": "Tiny",
      "mayLarge": false,
      "movement": {
        "walk": 10,
        "fly": 60
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d4+WIS",
        "damageType": "slashing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.base.boar-form-brawler": {
      "sourceId": "druid.base.boar-form-brawler",
      "sourceSha256": "d1288f0ae961f47cdaf529e43a8f37b48873aa800032377dc8506c26c58710ec",
      "sourceProcedure": {
        "id": "druid.base.boar-form-brawler",
        "name": "Boar Form (Brawler)",
        "className": "Druid",
        "band": "Base",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 1,
        "acquisition": "automatic",
        "activation": "Action attack; passive form traits",
        "cost": "One shift",
        "rangeAndTarget": "Self; tusk 5 ft",
        "duration": "While in Boar",
        "frequency": "One tusk/Action",
        "effect": "Resistance to slashing. Tusk 1d6 piercing+WIS. After moving 10 ft directly toward target, first hit/turn adds 1d6 and STR save or push 5 ft; no repeated charges from forced movement.",
        "spellRank": null
      },
      "minimumLevel": 1,
      "circle": null,
      "archAttunement": false,
      "canSpeak": false,
      "size": "Medium",
      "mayLarge": false,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d6+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.base.panther-form-stealth": {
      "sourceId": "druid.base.panther-form-stealth",
      "sourceSha256": "8daa235b54a30f029be0ab4ec9285f0787742efb78cd905b848ebcb572158396",
      "sourceProcedure": {
        "id": "druid.base.panther-form-stealth",
        "name": "Panther Form (Stealth)",
        "className": "Druid",
        "band": "Base",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 1,
        "acquisition": "automatic",
        "activation": "Action attack; passive form traits",
        "cost": "One shift",
        "rangeAndTarget": "Self; claw 5 ft",
        "duration": "While in Panther",
        "frequency": "One claw/Action",
        "effect": "Speed 40 ft, darkvision 60 ft, +4 Stealth. Claw 2d4 slashing+WIS; after 20 ft straight approach hit, STR save or Grappled. Escape Action against Druid DC; ends on separation/reversion. Only one held target, no free Restrained.",
        "spellRank": null
      },
      "minimumLevel": 1,
      "circle": null,
      "archAttunement": false,
      "canSpeak": false,
      "size": "Medium",
      "mayLarge": false,
      "movement": {
        "walk": 40
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d4+WIS",
        "damageType": "slashing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.arch.dire-wolf": {
      "sourceId": "druid.arch.dire-wolf",
      "sourceSha256": "b384946f0b86e1ad7b0b45561e0b50f3468f65d7bc8c4e90ff363194486b7987",
      "sourceProcedure": {
        "id": "druid.arch.dire-wolf",
        "name": "Dire Wolf",
        "className": "Druid",
        "band": "Arch",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 11,
        "acquisition": "automatic",
        "activation": "Action attack or Howl",
        "cost": "One shift; Howl 1 Form Surge",
        "rangeAndTarget": "Self; bite 5 ft; Howl 30 ft",
        "duration": "Form 10 minutes; fear up to 3 rounds",
        "frequency": "Howl 1/shift and finite reserve",
        "effect": "Arch attunement required. Speed 40 ft, bite 2d6 piercing+WIS; advantage when active ally threatens target 5 ft. Howl Action up to 3 enemies WIS save or Frightened, repeat end each turn, maximum 3 rounds. No free bite with Howl.",
        "spellRank": null
      },
      "minimumLevel": 11,
      "circle": null,
      "archAttunement": true,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": false,
      "movement": {
        "walk": 40
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d6+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "howl": {
          "action": "action",
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.arch.earth-warden-dire-bear": {
      "sourceId": "druid.arch.earth-warden-dire-bear",
      "sourceSha256": "8ceb2cb1ea880743953a06d50a1c0e098eba154298b3755a7efa689556e18af6",
      "sourceProcedure": {
        "id": "druid.arch.earth-warden-dire-bear",
        "name": "Earth Warden (Dire Bear)",
        "className": "Druid",
        "band": "Arch",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 11,
        "acquisition": "automatic",
        "activation": "Action Slam",
        "cost": "One shift; buffer reserve",
        "rangeAndTarget": "Self; 10 ft radius up to 3 creatures",
        "duration": "While in Earth Warden",
        "frequency": "Slam recharge 2",
        "effect": "Arch attunement required. Gain up to 30 temp HP from reserve, nonmagical physical resistance. Slam DEX save 2d6 bludgeoning+WIS and Prone on failure, half damage no Prone success. Ordinary claw 1d8+WIS when Slam unavailable.",
        "spellRank": null
      },
      "minimumLevel": 11,
      "circle": null,
      "archAttunement": true,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d8+WIS",
        "damageType": "slashing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 30,
      "specials": {
        "slam": {
          "action": "action",
          "payment": "recharge2"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.arch.sky-serpent": {
      "sourceId": "druid.arch.sky-serpent",
      "sourceSha256": "fb02c57b9530f327172b8a1c001f8528f4a4086e4659d954e713c7946468c708",
      "sourceProcedure": {
        "id": "druid.arch.sky-serpent",
        "name": "Sky Serpent",
        "className": "Druid",
        "band": "Arch",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 11,
        "acquisition": "automatic",
        "activation": "Action bite; passive traits",
        "cost": "One shift",
        "rangeAndTarget": "Self; bite 5 ft",
        "duration": "While in Sky Serpent",
        "frequency": "One bite/Action",
        "effect": "Arch attunement required. Flight 80 ft with hover, +2 DEX saves. Bite 2d8 lightning+WIS. Once/shift may spend 1 Form Surge to add 1d4 against wet target; no repeated electrical propagation.",
        "spellRank": null
      },
      "minimumLevel": 11,
      "circle": null,
      "archAttunement": true,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": false,
      "movement": {
        "walk": 30,
        "fly": 80
      },
      "hover": true,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d8+WIS",
        "damageType": "lightning",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "wet": {
          "action": null,
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.arch.ironhorn-ram": {
      "sourceId": "druid.arch.ironhorn-ram",
      "sourceSha256": "08721f755db519afdb198be9a11f8df1b8e2062022c4b2ed7428f552af5d2b9d",
      "sourceProcedure": {
        "id": "druid.arch.ironhorn-ram",
        "name": "Ironhorn Ram",
        "className": "Druid",
        "band": "Arch",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 11,
        "acquisition": "automatic",
        "activation": "Action ram; passive traits",
        "cost": "One shift",
        "rangeAndTarget": "Self; ram 5 ft",
        "duration": "While in Ironhorn Ram",
        "frequency": "One ram/Action",
        "effect": "Arch attunement required. AC max(normal, 17), immune Prone. Ram 1d8+WIS bludgeoning; after 20 ft straight approach first hit/turn adds 3d6, STR against Druid DC or push 10 ft. No bonus against same target more than once/round.",
        "spellRank": null
      },
      "minimumLevel": 11,
      "circle": null,
      "archAttunement": true,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": false,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "floor",
        "amount": 17
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d8+WIS",
        "damageType": "bludgeoning",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.arch.shadow-lynx": {
      "sourceId": "druid.arch.shadow-lynx",
      "sourceSha256": "a0a1750c467c1afc4289e067406f9488b165c86971105261790ad671c238de64",
      "sourceProcedure": {
        "id": "druid.arch.shadow-lynx",
        "name": "Shadow Lynx",
        "className": "Druid",
        "band": "Arch",
        "path": null,
        "sourceKind": "form",
        "minimumClassLevel": 11,
        "acquisition": "automatic",
        "activation": "Reaction Blink; Action claw",
        "cost": "One shift; Blink 1 Form Surge",
        "rangeAndTarget": "Self; claw 5 ft",
        "duration": "Blink instant; form 10 minutes",
        "frequency": "Blink 1/shift and finite reserve",
        "effect": "Arch attunement required. Claw 2d4+WIS magical slashing; +2 Stealth while motionless. When attack would hit, Reaction teleport 30 ft to visible empty space, causing triggering attack to miss if you leave its reach/range. Next claw before end next turn advantage. No blanket immunity to magical damage.",
        "spellRank": null
      },
      "minimumLevel": 11,
      "circle": null,
      "archAttunement": true,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": false,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d4+WIS",
        "damageType": "slashing",
        "intrinsicallyMagical": true
      },
      "entryBuffer": 0,
      "specials": {
        "blink": {
          "action": "reaction",
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.land.blight-elk": {
      "sourceId": "druid.hero.land.blight-elk",
      "sourceSha256": "359c36eac3bfd49ee16f5a309642ef6aec0c3f0486f37991c610895c861231fe",
      "sourceProcedure": {
        "id": "druid.hero.land.blight-elk",
        "name": "Blight Elk",
        "className": "Druid",
        "band": "Hero",
        "path": "Land",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action antlers; passive aura",
        "cost": "One shift",
        "rangeAndTarget": "Land Hero; 5 ft aura",
        "duration": "While in Blight Elk",
        "frequency": "Aura once/enemy/round, max 3 enemies",
        "effect": "Antlers 2d8+WIS piercing. Enemy starting within 5 ft CON save or 1d4 poison. Wither unattended mundane vegetation within 5 ft cosmetically; tainted water is visibly foul and harmless after 10 minutes. No mass contamination or permanent resource fabrication.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Land",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d8+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.land.tanglemaw": {
      "sourceId": "druid.hero.land.tanglemaw",
      "sourceSha256": "b916c4ba9ccc394e5cf2eb6cbc02344c0e211daec1698938f6d2403aaab415ab",
      "sourceProcedure": {
        "id": "druid.hero.land.tanglemaw",
        "name": "Tanglemaw",
        "className": "Druid",
        "band": "Hero",
        "path": "Land",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action bite; passive traits",
        "cost": "One shift",
        "rangeAndTarget": "Land Hero; bite 5 ft; sense 30 ft",
        "duration": "While in Tanglemaw",
        "frequency": "Retaliation once/round",
        "effect": "Bite 2d6+WIS piercing, STR save or Restrained until end next turn, escape Action against DC. Thorny Body deals 1d4 piercing to one melee attacker after hit; no reflections. Sense ground-contact locations 30 ft on same connected surface, not identities through stone walls.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Land",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d6+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.moon.beastlord-alpha-animal-hybrid": {
      "sourceId": "druid.hero.moon.beastlord-alpha-animal-hybrid",
      "sourceSha256": "0c08e78f8f2d4d467d2ef31331896514dc61775ed3397fa5357eba633d87fb5a",
      "sourceProcedure": {
        "id": "druid.hero.moon.beastlord-alpha-animal-hybrid",
        "name": "Beastlord (Alpha Animal Hybrid)",
        "className": "Druid",
        "band": "Hero",
        "path": "Moon",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action bite or Howl",
        "cost": "One shift; Howl 1 Form Surge",
        "rangeAndTarget": "Moon Hero; bite 5 ft/Howl 15 ft",
        "duration": "While in Beastlord; fear 1 turn",
        "frequency": "Howl 1/shift and finite reserve",
        "effect": "Bite 2d6+WIS piercing; first hit/turn adds 1d4 of one chosen fire/cold/lightning, not all three. Up to 2 beast allies 30 ft gain+1 first attack/turn. Howl Action up to 3 enemies WIS save or Frightened until end next turn.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Moon",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d6+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "howl": {
          "action": "action",
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.moon.mooncursed": {
      "sourceId": "druid.hero.moon.mooncursed",
      "sourceSha256": "ce968a8db6c8ebac99dc9d8d7ef4f99c949e173df8eed26e5dd75a8175bd3054",
      "sourceProcedure": {
        "id": "druid.hero.moon.mooncursed",
        "name": "Mooncursed",
        "className": "Druid",
        "band": "Hero",
        "path": "Moon",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action bite or Howl",
        "cost": "One shift; Howl 1 Form Surge",
        "rangeAndTarget": "Moon Hero; bite 5 ft/Howl 30 ft",
        "duration": "While in Mooncursed",
        "frequency": "Howl 1/shift and finite reserve",
        "effect": "Resistance to nonmagical physical damage except silver; other types unchanged. Bite 2d6+WIS piercing, +1d8 once/turn under real full moon. Howl Action choose up to 3 allies gain 2d8 temp HP total roll, or 3 enemies WIS save or Frightened through end next turn. Temp HP draws from Buffer Reserve per recipient.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Moon",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d6+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "howl": {
          "action": "action",
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.moon.elemental-shapeshifting": {
      "sourceId": "druid.hero.moon.elemental-shapeshifting",
      "sourceSha256": "1d9ad7f20980737543dc037fc1318a7462e3995e17afec48de94312ac3f5c0b7",
      "sourceProcedure": {
        "id": "druid.hero.moon.elemental-shapeshifting",
        "name": "Elemental Shapeshifting",
        "className": "Druid",
        "band": "Hero",
        "path": "Moon",
        "sourceKind": "form",
        "minimumClassLevel": 14,
        "acquisition": "automatic",
        "activation": "Bonus Action",
        "cost": "One shift and one elemental use",
        "rangeAndTarget": "Moon Circle self",
        "duration": "10 minutes",
        "frequency": "2/long rest",
        "effect": "Choose bounded elemental form: AC 16, natural attack 2d8+WIS chosen element, one/Action. Air flight 60 lightning resistance; Earth burrow 20 through loose soil physical DR 2; Fire fire resistance and melee attacker 1d4 fire once/round; Water swim 60 water breathing cold resistance. Retain own HP/abilities, no external stat blocks.",
        "spellRank": null
      },
      "minimumLevel": 14,
      "circle": "Moon",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "fixed",
        "amount": 16
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d8+WIS",
        "damageType": "chosen-element",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.storm.tempest-raptor": {
      "sourceId": "druid.hero.storm.tempest-raptor",
      "sourceSha256": "0f6b5667a0e9f772174a0e56e8b9f4ef174fd16d47d2bb7a6fe6ff148f8683ad",
      "sourceProcedure": {
        "id": "druid.hero.storm.tempest-raptor",
        "name": "Tempest Raptor",
        "className": "Druid",
        "band": "Hero",
        "path": "Storm",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action claw; passive traits",
        "cost": "One shift",
        "rangeAndTarget": "Storm Hero; claw 5 ft",
        "duration": "While in Tempest Raptor",
        "frequency": "One claw/Action; retaliation once/round",
        "effect": "Flight 60 ft, advantage on saves against wind/lightning while airborne. Claw 2d6+WIS lightning; wet target adds 1d4 once/shift for 1 Form Surge. After melee hit on you, attacker takes 1d6 lightning once/round; no repeated disarm chains.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Storm",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30,
        "fly": 60
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d6+WIS",
        "damageType": "lightning",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "wet": {
          "action": null,
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.storm.thunderhorn-stag": {
      "sourceId": "druid.hero.storm.thunderhorn-stag",
      "sourceSha256": "80904406e241853bf23018ba3194ea3b49941321ceaf05b417ce9cca3be8526a",
      "sourceProcedure": {
        "id": "druid.hero.storm.thunderhorn-stag",
        "name": "Thunderhorn Stag",
        "className": "Druid",
        "band": "Hero",
        "path": "Storm",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action antlers or Thunder Step",
        "cost": "One shift; Step 1 Form Surge",
        "rangeAndTarget": "Storm Hero; antlers 5 ft; teleport 30 ft",
        "duration": "While in Thunderhorn Stag",
        "frequency": "Step 1/shift and finite reserve",
        "effect": "Antlers 1d8+WIS piercing; after 20 ft approach first hit/turn also 2d8 thunder and CON save or Deafened through end next turn. Step Action teleport 30 ft, departure 10 ft radius up to 3 creatures CON save 2d8 thunder, half success. Sense natural storm approach 24 hours, no exact prediction of magical weather.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Storm",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d8+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "step": {
          "action": "action",
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.thorns.blight-elk": {
      "sourceId": "druid.hero.thorns.blight-elk",
      "sourceSha256": "f9db8ef944e9bfe024c3fb740c2efb6f4240b0938b1db4e098f4ce540e2e22dc",
      "sourceProcedure": {
        "id": "druid.hero.thorns.blight-elk",
        "name": "Blight Elk",
        "className": "Druid",
        "band": "Hero",
        "path": "Thorns",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action antlers; passive aura",
        "cost": "One shift",
        "rangeAndTarget": "Thorns Hero; 5 ft aura",
        "duration": "While in Blight Elk",
        "frequency": "Aura once/enemy/round, max 3 enemies",
        "effect": "Antlers 2d8+WIS piercing, +1d4 poison once/turn against Poisoned. Enemies starting 5 ft CON save or 1d4 poison. Ground 10 ft around you is difficult terrain for enemies, no lasting thorns after movement/reversion.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Thorns",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d8+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.thorns.tanglemaw": {
      "sourceId": "druid.hero.thorns.tanglemaw",
      "sourceSha256": "daff5c2781baba250c2131a002539a6f80d7a7a2884ebaaed94b81d541d90e08",
      "sourceProcedure": {
        "id": "druid.hero.thorns.tanglemaw",
        "name": "Tanglemaw",
        "className": "Druid",
        "band": "Hero",
        "path": "Thorns",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action bite; passive traits",
        "cost": "One shift",
        "rangeAndTarget": "Thorns Hero; bite 5 ft; sense 30 ft",
        "duration": "While in Tanglemaw",
        "frequency": "Retaliation once/round",
        "effect": "Bite 2d6+WIS piercing, STR save or Restrained through end next turn, Action escape DC. One melee attacker/round takes 1d4 piercing; one creature restrained by your bite takes 1d4 at start turn. Ground sense 30 ft same surface and advantage against Prone; no wall-penetrating identification.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Thorns",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d6+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.winterfang.snow-leopard": {
      "sourceId": "druid.hero.winterfang.snow-leopard",
      "sourceSha256": "45a815d53f107787811abec352814026ffae437e83a0891e5bf3a8f21f262755",
      "sourceProcedure": {
        "id": "druid.hero.winterfang.snow-leopard",
        "name": "Snow Leopard",
        "className": "Druid",
        "band": "Hero",
        "path": "Winterfang",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action claw; passive traits",
        "cost": "One shift",
        "rangeAndTarget": "Winterfang Hero; claw 5 ft",
        "duration": "While in Snow Leopard",
        "frequency": "One claw/Action",
        "effect": "Claw 2d6+WIS cold, +1d4 once/turn against slowed foe. +5 Stealth on ice/snow and advantage on legal Hide there; source+10 reduced provisionally. Ignore ordinary ice/snow movement penalties, not magical restraining ice.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Winterfang",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d6+WIS",
        "damageType": "cold",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.winterfang.frost-wyrmling": {
      "sourceId": "druid.hero.winterfang.frost-wyrmling",
      "sourceSha256": "be5a32836802126e195e59a8de64ea3c1e7ec3d8926ca051284bf326d39f526f",
      "sourceProcedure": {
        "id": "druid.hero.winterfang.frost-wyrmling",
        "name": "Frost Wyrmling",
        "className": "Druid",
        "band": "Hero",
        "path": "Winterfang",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action breath or claw",
        "cost": "One shift; breath one short-rest use",
        "rangeAndTarget": "Winterfang Hero; 30 ft cone up to 3 creatures",
        "duration": "While in Frost Wyrmling",
        "frequency": "Breath 1/short rest, shared across shifts",
        "effect": "AC normal+2, cold immunity. Claw 1d8+WIS cold. Breath 4d6 cold DEX half. One breath target may have cold resistance ignored once/shift for 1 Form Surge; immunity remains. No general physical resistance from cold terrain in this draft.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Winterfang",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "add",
        "amount": 2
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d8+WIS",
        "damageType": "cold",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "breath": {
          "action": "action",
          "payment": "short-rest"
        },
        "ignore-cold-resistance": {
          "action": null,
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.rotshaper.carrion-rat-king": {
      "sourceId": "druid.hero.rotshaper.carrion-rat-king",
      "sourceSha256": "66cae86b4ff384703f2aef8cc07dfd610085034b0922e02a461f86e74f20cc66",
      "sourceProcedure": {
        "id": "druid.hero.rotshaper.carrion-rat-king",
        "name": "Carrion Rat King",
        "className": "Druid",
        "band": "Hero",
        "path": "Rotshaper",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action bite or summon",
        "cost": "One shift; summon 1 Form Surge",
        "rangeAndTarget": "Rotshaper Hero; bite 5 ft/swarm 30 ft",
        "duration": "While in Carrion Rat King",
        "frequency": "Summon 1/shift and finite reserve",
        "effect": "Bite 1d8+WIS piercing+2d6 poison; CON save or Poisoned through end next turn. Immune disease/Poisoned, not poison damage. Summon Action creates one bounded engine swarm 1 minute, same command budget; replaces previous form swarm.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Rotshaper",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d8+WIS piercing + 2d6 poison",
        "damageType": "mixed",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "summon": {
          "action": "action",
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.rotshaper.insect-broodmother": {
      "sourceId": "druid.hero.rotshaper.insect-broodmother",
      "sourceSha256": "52edbedf9bfbdf8057259f3758ebfd144820c93a27c2170fd34e4d6f70297d82",
      "sourceProcedure": {
        "id": "druid.hero.rotshaper.insect-broodmother",
        "name": "Insect Broodmother",
        "className": "Druid",
        "band": "Hero",
        "path": "Rotshaper",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action bite; passive traits",
        "cost": "One shift; spawning 1 Form Surge",
        "rangeAndTarget": "Rotshaper Hero; up to 2 swarms adjacent",
        "duration": "While in Insect Broodmother",
        "frequency": "Spawn once/shift and finite reserve",
        "effect": "AC normal+3, climb 30 walls/ceilings, bite 1d8+WIS piercing. On entry optional spend surge spawn 2 bounded shared profile swarms, both end with form, combined one commanded attack/turn. Once/shift for another Form Surge turn one crit against you into normal hit; no infinite insects.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Rotshaper",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30,
        "climb": 30
      },
      "hover": false,
      "ac": {
        "mode": "add",
        "amount": 3
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d8+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "spawn": {
          "action": null,
          "payment": "surge"
        },
        "negate-critical": {
          "action": null,
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.rotshaper.master-of-vermin": {
      "sourceId": "druid.hero.rotshaper.master-of-vermin",
      "sourceSha256": "762dc5ac770d66998e89219fad3ca15abc6f5bb3755316d4bb388d76682283b5",
      "sourceProcedure": {
        "id": "druid.hero.rotshaper.master-of-vermin",
        "name": "Master of Vermin",
        "className": "Druid",
        "band": "Hero",
        "path": "Rotshaper",
        "sourceKind": "form",
        "minimumClassLevel": 14,
        "acquisition": "automatic",
        "activation": "Bonus Action",
        "cost": "One shift",
        "rangeAndTarget": "Rotshaper Circle self",
        "duration": "10 minutes",
        "frequency": "Normal shift limit",
        "effect": "Swarm form: own HP/AC, physical resistance, Speed 30, fit Tinygaps, natural attack S d6+WIS piercing. No flight unless choosing bats (flight 30), which forfeits physical resistance. Replacing a summoning spell's beast with swarm uses same single companion budget and paid spell, never multiplied dice/creatures.",
        "spellRank": null
      },
      "minimumLevel": 14,
      "circle": "Rotshaper",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "S d6+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {},
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.ashen-grove.charbear": {
      "sourceId": "druid.hero.ashen-grove.charbear",
      "sourceSha256": "aea389ba9868189c5ee1db218d3623978ad55bab07d432188912cba18493e50d",
      "sourceProcedure": {
        "id": "druid.hero.ashen-grove.charbear",
        "name": "Charbear",
        "className": "Druid",
        "band": "Hero",
        "path": "Ashen Grove",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action claw or Smoke",
        "cost": "One shift; Smoke 1 Form Surge",
        "rangeAndTarget": "Ashen Hero; claw 5 ft/aura 5 ft/smoke 10 ft",
        "duration": "While in Charbear; smoke 3 rounds",
        "frequency": "Smoke 1/shift; aura/retaliation caps",
        "effect": "Claw 2d8+WIS fire; first hit/turn Burn 1d4 next turn. Up to 3 enemies starting 5 ft CON save or 1d6 fire. Smoke Action opaque 10 ft radius sphere centered fixed point you occupy, concentration 3 rounds; all vision blocked, no poison in this draft. Wind 20 mph disperses.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Ashen Grove",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "2d8+WIS",
        "damageType": "fire",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "smoke": {
          "action": "action",
          "payment": "surge"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    },
    "druid.hero.ashen-grove.blazewood-stag": {
      "sourceId": "druid.hero.ashen-grove.blazewood-stag",
      "sourceSha256": "17a078d0e7095877419b9b0626f73d0c24c578be8a18c568ce2b1f89695ed07f",
      "sourceProcedure": {
        "id": "druid.hero.ashen-grove.blazewood-stag",
        "name": "Blazewood Stag",
        "className": "Druid",
        "band": "Hero",
        "path": "Ashen Grove",
        "sourceKind": "form",
        "minimumClassLevel": 10,
        "acquisition": "automatic",
        "activation": "Action antlers or Conflagration",
        "cost": "One shift; blast one long-rest use",
        "rangeAndTarget": "Ashen Hero; antlers 5 ft/blast 10 ft",
        "duration": "While in Blazewood Stag",
        "frequency": "Blast 1/long rest across shifts",
        "effect": "Antlers 1d8+WIS piercing; 20 ft charge adds 2d6 fire once/turn. Leave up to 3 fire tiles/turn, last until start next turn, DEX save or 1d8 fire once/creature/round. Blast Action 6d6 fire DEX half up to 3 creatures 10 ft, not free on reversion.",
        "spellRank": null
      },
      "minimumLevel": 10,
      "circle": "Ashen Grove",
      "archAttunement": false,
      "canSpeak": true,
      "size": "Medium",
      "mayLarge": true,
      "movement": {
        "walk": 30
      },
      "hover": false,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "identity": [
          "formAttack",
          "naturalAttack"
        ],
        "countPerAction": 1,
        "rangeFeet": 5,
        "attack": "PB+WIS",
        "damage": "1d8+WIS",
        "damageType": "piercing",
        "intrinsicallyMagical": false
      },
      "entryBuffer": 0,
      "specials": {
        "blast": {
          "action": "action",
          "payment": "long-rest"
        }
      },
      "normalSensesRetained": true,
      "handBasedEquipmentUse": false,
      "integrationStatus": "DRAFT; profile clarification and implementation review pending",
      "riderResolution": "Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list."
    }
  }
}

```

## tools/form_temphp_playtest_rules.py
SHA256 8c7c8197897a225fe7dfb8aef4b388747f5a46fb91771f4b64bce19cb03f1f39
```python
"""Bounded form/buffer reference, implementation review PENDING.

Caller owns actual source access, costs, targets, range, rolls, condition and
calendar legality. Use ONE BufferLedger per world and one DruidState per owner.
No scalar temp-HP copies may independently create/spend shields. Explicit clock
markers and completed-rest epochs come from the canonical scheduler.
"""
from dataclasses import dataclass, field, replace
from copy import deepcopy
from pathlib import Path
import json
from control_playtest_rules import ClockMarker, clock_marker, require_deadline
from spell_playtest_rules import SpellRuleError, integer
from redirection_playtest_rules import identity
from device_lifecycle_playtest_rules import Wallet
from core_playtest_rules import damage_event


def require(value, message):
    if not value: raise SpellRuleError(message)


@dataclass
class BufferGrant:
    grant_id: str
    source_id: str
    owner: str
    target: str
    remaining: int
    expiry: ClockMarker | None = None
    # None means an explicitly fixed/source-dependent lifetime, not default LR.
    rest_epoch: int | None = None
    dependencies: tuple = ()
    riders: set = field(default_factory=set)
    state: str = 'pending'

    def __post_init__(self):
        for v in (self.grant_id,self.source_id,self.owner,self.target): identity(v)
        integer(self.remaining,'offered temporary HP',0)
        if self.expiry is not None: require_deadline(self.expiry)
        if self.rest_epoch is not None: integer(self.rest_epoch,'recipient LR epoch',0)
        require(self.expiry is not None or self.rest_epoch is not None or self.dependencies,
                'Declare explicit expiry/dependency or default recipient LR epoch')
        for dep in self.dependencies: identity(dep)
        require(self.riders <= {'bloodshield-reaction','overflowing-cleanse'},'Unknown linked rider')
        if 'bloodshield-reaction' in self.riders:
            require(self.source_id=='crimson-agent.arch.veinweave-bloodshield','Wrong Bloodshield source')
        if 'overflowing-cleanse' in self.riders:
            require(self.source_id=='oracle.supplement.life.overflowing-light' and self.expiry is not None,
                    'Overflowing Light requires its explicit two-round endpoint')


class BufferLedger:
    """Grant identities persist after ending; no hidden shield or replay refill.

    expire() must run at actual scheduler deadlines. Side effects are returned
    as instructions; this helper never decides eligible conditions or cleanses
    automatically. A projection into Core is checked and reconciled atomically.
    """
    def __init__(self):
        self.grants={}; self.active={}; self.rest_epochs={}; self.damage_events=set()
        self.absorptions={}

    def amount(self,target):
        ident=self.active.get(target)
        return self.grants[ident].remaining if ident else 0

    def current(self,target):
        ident=self.active.get(target)
        return self.grants.get(ident)

    def validate_offer(self,grant,now):
        require(isinstance(grant,BufferGrant) and grant.state=='pending','Supply a new uncommitted grant')
        require(grant.grant_id not in self.grants,'Grant identity already processed')
        marker=clock_marker(now)
        if grant.expiry is not None: require(marker<grant.expiry,'Grant deadline already passed')
        if grant.rest_epoch is not None:
            require(grant.rest_epoch==self.rest_epochs.get(grant.target,0),'Stale recipient rest epoch')
        current=self.current(grant.target)
        if current and current.expiry is not None:
            require(marker<current.expiry,'Resolve existing scheduled expiry before offering a new grant')

    def offer(self,grant,now=0):
        """Caller pays the legal source BEFORE this nonstack comparison.

        No current reviewed source overrides equal-retains-existing. Noble's
        paired Smite components are merged BEFORE calling this method once.
        """
        self.validate_offer(grant,now)
        g=deepcopy(grant)
        if not g.remaining:
            return {'accepted':False,'amount':0,'grantId':None}
        self.grants[g.grant_id]=g
        current=self.current(g.target)
        if current and current.remaining>=g.remaining:
            g.state='rejected'; return {'accepted':False,'amount':g.remaining,'grantId':None}
        if current: self.end(g.target,'replaced')
        g.state='active'; self.active[g.target]=g.grant_id
        return {'accepted':True,'amount':g.remaining,'grantId':g.grant_id}

    def end(self,target,reason,*,now=None):
        require(reason in ('replaced','depleted','natural-expiry','long-rest','dependency-ended','body-ended'),
                'Unknown buffer ending')
        g=self.current(target)
        if g is None:return []
        if reason=='natural-expiry':
            require(now is not None and g.expiry is not None and clock_marker(now)>=g.expiry,
                    'Natural expiry requires the actual fixed deadline')
        events=[]
        if reason=='natural-expiry' and g.remaining>0 and 'overflowing-cleanse' in g.riders:
            events.append({'sourceId':g.source_id,'grantId':g.grant_id,'target':target,
                           'chooseUpTo':1,'eligibleConditions':('Frightened','Poisoned','Staggered')})
        g.state=reason; g.remaining=0; g.riders.clear(); del self.active[target]
        return events

    def expire(self,now):
        marker=clock_marker(now); events=[]
        for target in list(self.active):
            g=self.current(target)
            if g.expiry is not None and marker>=g.expiry: events+=self.end(target,'natural-expiry',now=marker)
        return events

    def end_dependency(self,dependency):
        identity(dependency)
        for target in list(self.active):
            if dependency in self.current(target).dependencies:self.end(target,'dependency-ended')

    def completed_long_rest(self,target,epoch):
        integer(epoch,'new recipient LR epoch',1)
        require(epoch==self.rest_epochs.get(target,0)+1,'Process each actual completed LR exactly once')
        g=self.current(target)
        if g and g.rest_epoch is not None:self.end(target,'long-rest')
        self.rest_epochs[target]=epoch

    def consume_linked_reaction(self,target,grant_id,wallet,*,legal):
        g=self.current(target)
        require(legal and g is not None and g.grant_id==grant_id and 'bloodshield-reaction' in g.riders,
                'No current legal Bloodshield permission')
        wallet.validate(action='reaction'); wallet.pay(action='reaction')
        g.riders.remove('bloodshield-reaction')
        return {'sourceId':g.source_id,'grantId':g.grant_id,'reactionSpent':True}

    def core_damage(self,target,event_id,state,resolved_damage,*,now=0,**core_options):
        """Already defended packet, exactly one Core HP/Wound/death resolution.

        Returned life state is authoritative. Source-specific same-packet
        replacements remain the caller's existing Core/death adapter obligation;
        finalize Druid reversion only AFTER those settle the actual state.
        """
        identity(event_id); key=(target,event_id)
        require(key not in self.damage_events,'Damage event already resolved for this character')
        require(state.temp_hp==self.amount(target),'Core temporary-HP projection differs from grant ledger')
        current=self.current(target)
        require(current is None or current.expiry is None or clock_marker(now)<current.expiry,
                'Resolve scheduled shield expiry before damage')
        result,events=damage_event(state,resolved_damage,**core_options)
        self.damage_events.add(key)
        g=self.current(target)
        if g:
            g.remaining=result.temp_hp
            if not g.remaining:self.end(target,'depleted')
        return result,events

    def necrotic_affinity(self,target,event_id,post_defense_damage,wallet,expiry,*,legal):
        """Reaction at post-defense/after-resistance stage, BEFORE old buffer.

        Caller verifies spell/supernatural necrotic origin and actual access.
        Use returned remainingDamage in the canonical packet, then finish below.
        """
        identity(target); identity(event_id); require_deadline(expiry)
        integer(post_defense_damage,'post-defense necrotic damage',1)
        key=(target,event_id)
        require(legal and key not in self.absorptions and key not in self.damage_events,
                'Legal pending unique necrotic event required')
        wallet.validate(action='reaction'); wallet.pay(action='reaction')
        absorbed=post_defense_damage//2
        self.absorptions[key]={'amount':absorbed,'expiry':expiry,'finished':False}
        return {'prevented':absorbed,'remainingDamage':post_defense_damage-absorbed,
                'isHealing':False,'isTransfer':False}

    def finish_necrotic_affinity(self,target,event_id,grant_id,now,*,living_holder):
        key=(target,event_id); pending=self.absorptions.get(key)
        require(pending is not None and not pending['finished'] and key in self.damage_events,
                'Finish once after canonical damage has actually resolved')
        grant=None
        if pending['amount'] and living_holder:
            grant=BufferGrant(grant_id,'feat:necrotic_affinity',target,target,pending['amount'],expiry=pending['expiry'])
            self.validate_offer(grant,now)
        pending['finished']=True
        return self.offer(grant,now) if grant else None


def blood_ritual_offers(level):
    integer(level,'character level',1,20)
    return {'self':2*level,'eachEligibleAlly':level,'allyLifetimeSeconds':3600}


def post_event_buffer_amount(source_id,actual_amount,*,eligible,scale=None,modifier=None):
    """Only these already-resolved causal amounts; never rolled/raw damage.

    Necrotic Affinity uses its separate staged adapter above.
    """
    integer(actual_amount,'actual causal amount',0)
    require(eligible,'Actual source trigger/anti-farm/target legality required')
    if source_id in ('paladin.supplement.oath-of-the-martyr-king.king-s-smite',
                     'paladin.supplement.oath-of-the-martyr-king.noble-bearing'):
        integer(scale,'S',1,4);integer(modifier,'M',1)
        return min(actual_amount//2,scale+modifier)
    if source_id=='v6-trait:soul-drain':return actual_amount
    raise SpellRuleError('Use the source-specific established amount adapter')


def one_character_area_targets(position_hits):
    """Input is already-filtered legal positions for ONE area/event.

    Each pair is (canonical character identity, representation identity).
    Independent attack/event calls are deliberately not coalesced together.
    """
    result=[]
    for character,position in position_hits:
        identity(character); identity(position)
        if character not in result:result.append(character)
    return result


def spirit_walk_position_eligible(*,is_spirit,is_attack,physical_target_required,native_eligible):
    return bool(native_eligible and (not is_spirit or (not is_attack and not physical_target_required)))


@dataclass(frozen=True)
class DruidStats:
    owner: str
    level: int
    pb: int
    wisdom: int
    scale: int
    modifier: int

    def __post_init__(self):
        identity(self.owner);integer(self.level,'Druid level',1,20);integer(self.pb,'PB',1)
        integer(self.scale,'S',1,4);integer(self.modifier,'M',1)
        require(isinstance(self.wisdom,int) and not isinstance(self.wisdom,bool),'Actual signed WIS required')


@dataclass
class FormInstance:
    instance_id: str
    source_id: str
    variant: str | None
    expiry: ClockMarker
    large: bool=False
    spent: set=field(default_factory=set)
    state: str='active'
    entry_open: bool=False


PROFILES=json.loads((Path(__file__).resolve().parents[1]/'data/playtest/druid_form_profiles.json').read_text(encoding='utf-8'))['profiles']
ARCH_IDS=frozenset(k for k,v in PROFILES.items() if v['archAttunement'])
CIRCLES=frozenset(('Land','Moon','Storm','Thorns','Winterfang','Rotshaper','Ashen Grove'))


def shift_capacity(level):
    integer(level,'Druid level',1,20)
    return 2+sum(level>=gate for gate in (4,7,10,13,16,19))


class DruidState:
    """Same-body forms and shared finite reserves; no HP or condition copy.

    The owner-wide class cadence dictionary is mutated only for real entries.
    creatures, when supplied, is the SAME CreatureWorld used by companion rules.
    Caller ends other exact form-dependent effect records from returned IDs.
    A canonical calendar owns regular marker indices and actual rest completion.
    """
    def __init__(self,stats,circle,buffers,cadence,*,attuned=(),creatures=None):
        require(circle in CIRCLES or (circle is None and stats.level==1),'Choose legal Druid Circle')
        require(isinstance(buffers,BufferLedger),'Canonical buffer ledger required')
        require(set(cadence)>= {'refrain','rememberedSpell','dissonance'},'Canonical class cadence required')
        self.owner=stats.owner;self.circle=circle;self.buffers=buffers;self.cadence=cadence
        self.creatures=creatures;self.current=None;self.instances={}
        self.long_epoch=0;self.short_epoch=0;self.regular_index=0;self.recharges={}
        self.rest_uses={};self.attuned=()
        self._validate_attunement(stats,attuned)
        self._refill(stats,attuned)

    def _stats(self,stats):
        require(isinstance(stats,DruidStats) and stats.owner==self.owner,'Use current original-owner Druid stats')

    def _validate_attunement(self,stats,attuned):
        require(len(attuned)==len(set(attuned)) and len(attuned)<=2 and set(attuned)<=ARCH_IDS,
                'Choose at most two distinct supplied Arch forms')
        require(stats.level>=11 or not attuned,'Arch attunement starts at11')

    def _refill(self,stats,attuned):
        self.shifts=shift_capacity(stats.level);self.buffer_capacity=2*stats.level+stats.modifier
        self.reserve=self.buffer_capacity;self.surges=stats.pb;self.surge_capacity=stats.pb
        self.attuned=tuple(attuned);self.rest_uses={}

    def completed_long_rest(self,stats,epoch,*,attuned,actual_completed):
        self._stats(stats);self._validate_attunement(stats,attuned)
        require(actual_completed and epoch==self.long_epoch+1,'Actual next completed owner LR required')
        self.long_epoch=epoch;self.short_epoch+=1;self._refill(stats,attuned)
        # Receiving default buffers is a separate recipient-calendar operation.
        # Form instances/local flags and independent clocks are NOT refreshed.

    def completed_short_rest(self,epoch,*,actual_completed):
        require(actual_completed and epoch==self.short_epoch+1,'Actual next completed SR required')
        self.short_epoch=epoch
        self.rest_uses={k:v for k,v in self.rest_uses.items() if not k.startswith('short:')}

    def regular_start(self,index,*,actual_regular_marker):
        integer(index,'canonical regular marker',1)
        require(actual_regular_marker and index>self.regular_index,'No extra-turn/repeated recharge tick')
        self.regular_index=index

    def _active(self,now):
        require(self.current is not None and self.current.state=='active' and clock_marker(now)<self.current.expiry,
                'Resolve form endpoint before acting')
        return self.current

    def _legal_profile(self,stats,source_id,variant,large):
        self._stats(stats);require(source_id in PROFILES,'Only supplied bounded Druid forms')
        p=PROFILES[source_id]
        require(stats.level>=p['minimumLevel'],'Form level gate not met')
        require(p['circle'] is None or p['circle']==self.circle,'Wrong Circle')
        require(not p['archAttunement'] or source_id in self.attuned,'Form is not long-rest attuned')
        require(not large or p['mayLarge'],'This form does not permit Large size')
        if source_id.endswith('elemental-shapeshifting'):
            require(variant in ('air','earth','fire','water'),'Choose actual Elemental subtype')
        elif source_id.endswith('master-of-vermin'):
            require(variant in ('ground','bats'),'Choose actual Vermin subtype')
        else:require(variant is None,'This form has no independently changeable subtype')
        return p

    def shift(self,stats,source_id,instance_id,now,wallet,*,legal,variant=None,large=False,
              spawn=False,spawn_legal=False):
        p=self._legal_profile(stats,source_id,variant,large);marker=clock_marker(now)
        identity(instance_id);require(instance_id not in self.instances,'Form instance identity already used')
        require(legal,'Actual movement/space/capability/source preflight failed')
        if self.current:
            old=self._active(marker)
            require((old.source_id,old.variant)!=(source_id,variant),'Early identical-form requests are unpaid and rejected')
        require(stats.level==20 or self.shifts>0,'No shift use')
        elemental=source_id.endswith('elemental-shapeshifting')
        require(not elemental or self.rest_uses.get('long:elemental',0)<2,'Elemental uses exhausted')
        wallet.validate(action='bonus')
        amount=min(p['entryBuffer'],self.reserve)
        grant=BufferGrant(instance_id+':entry',source_id,self.owner,self.owner,amount,dependencies=(instance_id,)) if amount else None
        if grant:self.buffers.validate_offer(grant,marker)
        wallet.pay(action='bonus')
        if stats.level<20:self.shifts-=1
        if elemental:self.rest_uses['long:elemental']=self.rest_uses.get('long:elemental',0)+1
        old_id=self._end('changed')
        form=FormInstance(instance_id,source_id,variant,ClockMarker(marker.seconds+600,marker.phase),large)
        self.current=form;self.instances[instance_id]=form
        self.cadence['refrain']=0;self.cadence['rememberedSpell']=None
        self.reserve-=amount
        offered=self.buffers.offer(grant,marker) if grant else None
        spawn_payment=None
        if source_id.endswith('insect-broodmother'):
            form.entry_open=True
            if spawn and spawn_legal and self.surges>0:
                spawn_payment=self.special(stats,now,wallet,'spawn',legal=True)
            form.entry_open=False
        return {'formInstance':instance_id,'endedDependency':old_id,'entryBuffer':offered,
                'spawnPayment':spawn_payment,'optionalSpawnWindowClosed':True}

    def _end(self,reason):
        if self.current is None:return None
        f=self.current;f.state=reason;self.current=None
        self.buffers.end_dependency(f.instance_id)
        if self.creatures is not None:self.creatures.end_dependency(form=f.instance_id)
        return f.instance_id

    def revert(self,now,wallet,*,legal):
        self._active(now);require(legal,'Actual voluntary reversion must be legal')
        wallet.validate(action='bonus');wallet.pay(action='bonus')
        return self._end('voluntary-reversion')

    def natural_endpoint(self,stats,now,*,renew):
        self._stats(stats);marker=clock_marker(now);f=self.current
        require(f is not None and f.state=='active' and marker==f.expiry,'Process actual form endpoint exactly')
        if not renew:return {'endedDependency':self._end('expired')}
        require(stats.level==20 or self.shifts>0,'No shift use for renewal')
        if stats.level<20:self.shifts-=1
        f.expiry=ClockMarker(f.expiry.seconds+600,f.expiry.phase)
        return {'renewedSameInstance':f.instance_id,'expiry':f.expiry}

    def finalize_damage_state(self,*,actual_hp,incapacitated,dead,unsupported):
        integer(actual_hp,'actual final HP',0)
        if self.current is None:return None
        if actual_hp==0 or incapacitated or dead:
            ident=self._end('forced-reversion')
            return {'endedDependency':ident,'beginOrdinaryFall':bool(unsupported),'secondDamageResolution':False}
        return None

    def profile(self,stats,now,form_normal_ac,*,ac_components_certified):
        self._stats(stats);f=self._active(now);integer(form_normal_ac,'operative form normal AC',0)
        require(ac_components_certified,'Exclude melded armor/shield/unclassified item bonuses first')
        p=deepcopy(PROFILES[f.source_id]);mode=p['ac']['mode'];n=p['ac']['amount']
        p['ac']=max(form_normal_ac,n) if mode=='floor' else form_normal_ac+n if mode=='add' else n if mode=='fixed' else form_normal_ac
        p['size']='Large' if f.large else p['size'];p['formInstance']=f.instance_id
        p['attack']['attack']=stats.pb+stats.wisdom;p['saveDC']=8+stats.pb+stats.wisdom
        p['attack']['magicalAgainstPhysicalDefenses']=p['attack']['intrinsicallyMagical'] or (self.circle=='Moon' and stats.level>=6)
        if f.variant in ('air','earth','fire','water'):
            p['attack']['damageType']={'air':'lightning','earth':'bludgeoning','fire':'fire','water':'cold'}[f.variant]
            p['elementalSubtype']=f.variant
            p['movement'].update({'air':{'fly':60},'earth':{'burrowLooseSoil':20},'fire':{},'water':{'swim':60}}[f.variant])
        if f.variant in ('ground','bats'):
            p['physicalResistance']=f.variant=='ground'
            if f.variant=='bats':p['movement']['fly']=30
        p['mayCastDruidSpells']=stats.level>=18
        p['materialComponents']='At20 waive noncostly unconsumed only; otherwise no access to melded materials'
        return p

    def attack(self,stats,now,wallet,*,legal):
        self._stats(stats);f=self._active(now);require(legal,'Actual natural attack target/capability required')
        wallet.validate(action='action');wallet.pay(action='action')
        attack=deepcopy(PROFILES[f.source_id]['attack'])
        if f.variant in ('air','earth','fire','water'):
            attack['damageType']={'air':'lightning','earth':'bludgeoning','fire':'fire','water':'cold'}[f.variant]
        return {'sourceId':f.source_id,'formInstance':f.instance_id,
                'profile':attack,'attack':stats.pb+stats.wisdom,
                'WIS':stats.wisdom,'S':stats.scale,'saveDC':8+stats.pb+stats.wisdom,
                'magicalAgainstPhysicalDefenses':attack['intrinsicallyMagical'] or (self.circle=='Moon' and stats.level>=6),
                'circleFormsFirstHitBonus':stats.scale if self.circle=='Moon' and stats.level>=2 else 0,
                'circleFormsFrequency':'First actual natural-form hit on own turn only; canonical hit ledger required',
                'exactRiders':PROFILES[f.source_id]['sourceProcedure']['effect'],
                'unrelatedWeaponProcAuthorized':False}

    def special(self,stats,now,wallet,special_id,*,legal):
        self._stats(stats);f=self._active(now);p=PROFILES[f.source_id]
        require(special_id in p['specials'] and legal,'Actual printed special and all gates required')
        q=p['specials'][special_id]
        if special_id=='spawn':require(f.entry_open,'Brood spawn requires the actual entry window')
        if q['payment']=='surge':
            require(special_id not in f.spent and self.surges>0,'Local special or global Form Surge exhausted')
        elif q['payment']=='recharge2':
            require(self.regular_index>=self.recharges.get(f.source_id,0),'Slam source recharge still active across shifts')
        else:
            kind='short:' if q['payment']=='short-rest' else 'long:'
            require(self.rest_uses.get(kind+f.source_id,0)==0,'Shared per-rest special already spent')
        wallet.validate(action=q['action']);wallet.pay(action=q['action'])
        if q['payment']=='surge':f.spent.add(special_id);self.surges-=1
        elif q['payment']=='recharge2':self.recharges[f.source_id]=self.regular_index+2
        else:self.rest_uses[kind+f.source_id]=1
        return {'sourceId':f.source_id,'formInstance':f.instance_id,'specialId':special_id,
                'sourceProcedure':deepcopy(p['sourceProcedure']),'refundOnFailure':False,
                'createsExtraAttack':False,'formSurgePaid':q['payment']=='surge'}

    def mooncursed_howl(self,stats,now,wallet,recipients,shared_roll,grant_ids,*,legal):
        f=self._active(now)
        require(f.source_id=='druid.hero.moon.mooncursed','Requires actual Mooncursed form')
        require(1<=len(recipients)<=3 and len(recipients)==len(set(recipients))==len(grant_ids),
                'Select and order one to three distinct legal allies before rolling')
        require(len(set(grant_ids))==len(grant_ids),'Distinct offered grant IDs')
        integer(shared_roll,'shared 2d8',2,16)
        grants=[];reserve=self.reserve
        for target,ident in zip(recipients,grant_ids):
            identity(target);identity(ident);amount=min(shared_roll,reserve);reserve-=amount
            g=BufferGrant(ident,f.source_id,self.owner,target,amount,
                          rest_epoch=self.buffers.rest_epochs.get(target,0)) if amount else None
            if g:self.buffers.validate_offer(g,now)
            grants.append(g)
        self.special(stats,now,wallet,'howl',legal=legal)
        self.reserve=reserve
        return [self.buffers.offer(g,now) if g else None for g in grants]

```

## tools/validate_form_temphp_playtests.py
SHA256 f5ff9ae431abee20ed5bcfbcb490d202a1d83a06eba54323dfcdc06392917da4
```python
"""Adversarial contract checks, not full card/rider or human balance tests."""
from pathlib import Path
import json
from copy import deepcopy
from dataclasses import replace
from form_temphp_playtest_rules import *
from core_playtest_rules import LifeState
from creature_lifecycle_playtest_rules import CreatureWorld, Creature

checks=0
def check(value,label):
    global checks
    assert value,label
    checks+=1
def rejects(fn,label):
    try:fn()
    except SpellRuleError:check(True,label)
    else:raise AssertionError(label)

def grant(ident,amount,*,source='test',target='d',expiry=None,rest=0,deps=(),riders=()):
    return BufferGrant(ident,source,'d',target,amount,expiry,rest,deps,set(riders))

def state(level=20,circle='Moon',*,attuned=(),creatures=None):
    stats=DruidStats('d',level,6,4,4,4)
    ledger=BufferLedger(); cadence={'refrain':3,'rememberedSpell':'test-spell','dissonance':9}
    return stats,DruidState(stats,circle,ledger,cadence,attuned=attuned,creatures=creatures)

def main():
    global checks
    b=BufferLedger()
    b.offer(grant('old',8,expiry=ClockMarker(30),rest=None))
    b.offer(grant('small',7,expiry=ClockMarker(100),rest=None))
    check(b.current('d').grant_id=='old','Smaller grant cannot refresh')
    b.offer(grant('tie',8,expiry=ClockMarker(100),rest=None))
    check(b.current('d').expiry==ClockMarker(30),'Tie retains original deadline')
    rejects(lambda:b.offer(grant('tie',50)),'Rejected ID cannot later refill')
    b.offer(grant('bigger',9))
    check(b.grants['old'].state=='replaced' and b.amount('d')==9,'Only one active grant')
    b.end('d','depleted');check(b.amount('d')==0,'Old grant never reappears')
    b.offer(grant('zero',0));check('zero' not in b.grants,'Zero creates no grant identity')
    b.offer(grant('default',4));b.completed_long_rest('d',1)
    check(b.amount('d')==0,'Default ends at actual recipient LR')
    rejects(lambda:b.completed_long_rest('d',1),'No repeated rest reset')
    rejects(lambda:b.offer(grant('stale',5,rest=0)),'Stale recipient epoch rejected')
    b.offer(grant('fixed',5,expiry=ClockMarker(100),rest=None),50)
    b.completed_long_rest('d',2);check(b.amount('d')==5,'Explicit lifetime may outlast LR')
    b.expire(100);check(b.amount('d')==0,'Exact fixed endpoint')

    blood='crimson-agent.arch.veinweave-bloodshield'
    b=BufferLedger();b.offer(grant('unrelated',10))
    b.offer(grant('rejected-blood',10,source=blood,riders=('bloodshield-reaction',)))
    w=Wallet();rejects(lambda:b.consume_linked_reaction('d','rejected-blood',w,legal=True),'Rejected shield has no permission')
    check(w.reaction,'Invalid permission does not pay Reaction')
    b.offer(grant('blood',12,source=blood,riders=('bloodshield-reaction',)))
    b.consume_linked_reaction('d','blood',w,legal=True)
    check(not w.reaction and not b.current('d').riders,'One current linked Reaction')
    rejects(lambda:b.consume_linked_reaction('d','blood',Wallet(),legal=True),'No repeated linked use')
    b.offer(grant('blood2',13,source=blood,riders=('bloodshield-reaction',)))
    b.offer(grant('other',14));rejects(lambda:b.consume_linked_reaction('d','blood2',Wallet(),legal=True),'Replacement removes linked use')

    overflow='oracle.supplement.life.overflowing-light'
    for reason in ('replaced','depleted','dependency-ended','body-ended','long-rest'):
        b=BufferLedger();b.offer(grant('ol',3,source=overflow,expiry=ClockMarker(12),rest=None,riders=('overflowing-cleanse',)))
        check(not b.end('d',reason),'No false natural-expiry cleanse: '+reason)
        check(not b.expire(12),'No delayed cleanse after '+reason)
    b=BufferLedger();b.offer(grant('ol',3,source=overflow,expiry=ClockMarker(12),rest=None,riders=('overflowing-cleanse',)))
    rejects(lambda:b.end('d','natural-expiry',now=11),'Cannot fabricate early natural expiry')
    rejects(lambda:b.core_damage('d','late',LifeState(20,20,3),1,now=12),'Expired buffer cannot protect late event')
    check(not b.expire(11),'No early cleanse');events=b.expire(12)
    check(len(events)==1 and events[0]['chooseUpTo']==1,'One optional actual eligible cleanse')
    check(not b.expire(13),'No repeat cleanse')

    b=BufferLedger();b.offer(grant('program',10,source='tinker.hero.artificer.protective-programming',rest=None,deps=('hit1',)))
    life,events=b.core_damage('d','hit1',LifeState(20,20,10),3)
    check(life.hp==20 and life.temp_hp==7 and events['tempAbsorbed']==3,'Shield before one hit')
    b.end_dependency('hit1');check(b.amount('d')==0,'Programming remainder ends after that hit')
    b=BufferLedger();b.offer(grant('larger',20));b.offer(grant('program',10,rest=None,deps=('hit1',)))
    b.end_dependency('hit1');check(b.amount('d')==20,'Rejected one-hit shield cannot end winner')

    b=BufferLedger();b.offer(grant('shield',6))
    original=LifeState(30,8,6,wounds=(None,),stable=False,death_successes=0)
    out,e=b.core_damage('d','damage',original,4)
    check(out.hp==8 and out.wounds==(None,) and b.amount('d')==2,'THP mitigates without healing/Wound removal')
    check(original.temp_hp==6,'Core input immutable')
    rejects(lambda:b.core_damage('d','damage',out,4),'No duplicate canonical damage')
    rejects(lambda:b.core_damage('d','other',replace(out,temp_hp=100),4),'Divergent scalar HP projection rejected')
    b=BufferLedger();b.offer(grant('dying',10))
    out,e=b.core_damage('d','dmg',LifeState(20,0,10,death_failures=1),5)
    check(out.hp==0 and not out.stable and out.death_failures==1,'Buffer cannot stabilize/reset dying')

    b=BufferLedger();b.offer(grant('old',3));w=Wallet()
    q=b.necrotic_affinity('d','necro',9,w,ClockMarker(12),legal=True)
    check(q['prevented']==4 and q['remainingDamage']==5 and not w.reaction,'After-resistance half prevention')
    out,e=b.core_damage('d','necro',LifeState(20,20,3),q['remainingDamage'])
    check(out.hp==18 and e['tempAbsorbed']==3,'Old shield protects remainder only')
    b.finish_necrotic_affinity('d','necro','new',0,living_holder=True)
    check(b.amount('d')==4 and out.hp==18,'New shield only after damage')
    rejects(lambda:b.necrotic_affinity('d','necro',9,Wallet(),ClockMarker(12),legal=True),'No repeat absorption')
    rejects(lambda:b.finish_necrotic_affinity('d','necro','new2',0,living_holder=True),'No repeat post-packet grant')
    b=BufferLedger();b.necrotic_affinity('d','one',1,Wallet(),ClockMarker(12),legal=True)
    b.core_damage('d','one',LifeState(20,20),1)
    check(b.finish_necrotic_affinity('d','one','no-grant',0,living_holder=True) is None and not b.grants,'One damage can pay without zero grant')
    b=BufferLedger();q=b.necrotic_affinity('d','fatal',100,Wallet(),ClockMarker(12),legal=True)
    out,e=b.core_damage('d','fatal',LifeState(20,1),q['remainingDamage'])
    check(out.dead,'Test actual instant death')
    b.finish_necrotic_affinity('d','fatal','corpse',0,living_holder=False)
    check(not b.grants,'No post-event corpse shield')

    check(blood_ritual_offers(7)=={'self':14,'eachEligibleAlly':7,'allyLifetimeSeconds':3600},'Blood Ritual uses own offer not winner')
    check(post_event_buffer_amount('paladin.supplement.oath-of-the-martyr-king.king-s-smite',99,eligible=True,scale=2,modifier=3)==5,'Smite actual half and cap')
    rejects(lambda:post_event_buffer_amount('v6-trait:soul-drain',8,eligible=False),'Actual ancestry anti-farm gate')
    check(one_character_area_targets([('d','body'),('d','spirit'),('ally','body2')])==['d','ally'],'One area deduplicates same body identity')
    check(not spirit_walk_position_eligible(is_spirit=True,is_attack=True,physical_target_required=False,native_eligible=True),'Spirit never attack target')
    check(not spirit_walk_position_eligible(is_spirit=True,is_attack=False,physical_target_required=True,native_eligible=True),'Physical-required effect excluded')
    check(spirit_walk_position_eligible(is_spirit=True,is_attack=False,physical_target_required=False,native_eligible=True),'Legal nonphysical area exposure')

    bear='druid.base.bear-form-tank';wolf='druid.base.wolf-form-striker';hawk='druid.base.hawk-form-scout'
    stats,d=state(10);d.buffers.offer(grant('large-shield',50));w=Wallet()
    entered=d.shift(stats,bear,'bear1',0,w,legal=True)
    check(d.shifts==4 and d.reserve==4 and not w.bonus_action,'Entry pays full20 reserve and shift/BA')
    check(d.buffers.current('d').grant_id=='large-shield','Failed comparison still consumes reserve')
    check(d.cadence=={'refrain':0,'rememberedSpell':None,'dissonance':9},'Only Refrain clears')
    before=(d.reserve,d.shifts);w=Wallet()
    rejects(lambda:d.shift(stats,bear,'repeat',1,w,legal=True),'Early identical form rejected')
    check(before==(d.reserve,d.shifts) and w.bonus_action,'Illegal identical shift costs nothing')
    d.cadence['refrain']=2;d.cadence['rememberedSpell']='again'
    d.natural_endpoint(stats,600,renew=True)
    check(d.current.instance_id=='bear1' and d.reserve==4 and d.shifts==3,'Renew same instance without refill')
    check(d.cadence['refrain']==2 and d.current.expiry==ClockMarker(1200),'Renew does not clear Refrain')
    rejects(lambda:d.natural_endpoint(stats,700,renew=True),'No early renew')
    d.revert(601,Wallet(),legal=True)
    check(d.cadence['refrain']==2 and d.shifts==3 and d.buffers.amount('d')==50,'Revert preserves unrelated shield and cadence')
    d.shift(stats,bear,'bear2',602,Wallet(),legal=True)
    check(d.reserve==0,'New entry only remaining reserve offered')
    d.revert(603,Wallet(),legal=True);d.shift(stats,bear,'bear3',604,Wallet(),legal=True)
    check(d.reserve==0 and 'bear3:entry' not in d.buffers.grants,'Zero-reserve form still legal, no grant')
    rejects(lambda:d.shift(stats,wolf,'illegal',605,Wallet(),legal=False),'Illegal geometry does not mutate')

    stats,d=state(20);d.shift(stats,bear,'f',0,Wallet(),legal=True)
    check(d.shifts==8 and d.reserve==24,'Level20 free shifts do not refill finite benefits')
    d.natural_endpoint(stats,600,renew=True)
    check(d.reserve==24 and d.current.instance_id=='f','Level20 renewal preserves exact grant')
    check(d.finalize_damage_state(actual_hp=1,incapacitated=False,dead=False,unsupported=False) is None,'Actual instead1 retains form')
    result=d.finalize_damage_state(actual_hp=0,incapacitated=False,dead=False,unsupported=True)
    check(result['beginOrdinaryFall'] and not result['secondDamageResolution'] and not d.buffers.amount('d'),'Forced end/fall no second HP pool')
    stats,d=state();d.shift(stats,hawk,'h',0,Wallet(),legal=True)
    p=d.profile(stats,1,12,ac_components_certified=True)
    check(p['size']=='Tiny' and p['movement']=={'walk':10,'fly':60} and not p['canSpeak'],'Exact Hawk profile')
    check(p['mayCastDruidSpells'],'Beast Spells uses actual18 gate')
    rejects(lambda:d.profile(stats,1,20,ac_components_certified=False),'No unclassified melded AC')

    # Exact-source profile gates and an ordinary Action for all26 bodies.
    for index,(ident,p) in enumerate(PROFILES.items()):
        stats,d=state(20,p['circle'] or 'Moon',attuned=(ident,) if p['archAttunement'] else ())
        variant='air' if ident.endswith('elemental-shapeshifting') else 'ground' if ident.endswith('master-of-vermin') else None
        d.shift(stats,ident,'form'+str(index),0,Wallet(),legal=True,variant=variant)
        profile=d.profile(stats,0,12,ac_components_certified=True)
        check(profile['sourceId']==ident and profile['attack']['attack']==10,'Actual source profile '+ident)
        w=Wallet();attack=d.attack(stats,0,w,legal=True)
        check(w.actions==0 and not attack['unrelatedWeaponProcAuthorized'],'One natural Action '+ident)
    stats,d=state(10,'Moon')
    rejects(lambda:d.shift(stats,'druid.arch.dire-wolf','x',0,Wallet(),legal=True),'Arch level11 gate')
    stats,d=state(20,'Moon')
    rejects(lambda:d.shift(stats,'druid.arch.dire-wolf','x',0,Wallet(),legal=True),'Attunement required')
    rejects(lambda:d.shift(stats,'druid.hero.storm.tempest-raptor','x',0,Wallet(),legal=True),'No cross-Circle Hero form')

    moon='druid.hero.moon.mooncursed';stats,d=state();d.shift(stats,moon,'moon',0,Wallet(),legal=True)
    d.reserve=9;d.buffers.offer(grant('ally-big',20,target='a'))
    out=d.mooncursed_howl(stats,1,Wallet(),['a','b','c'],12,['a1','b1','c1'],legal=True)
    check(d.reserve==0 and out[0]['amount']==9 and not out[0]['accepted'] and out[1:]==[None,None],'Sequential9/0/0, rejected offer still pays')
    check(d.surges==5 and 'howl' in d.current.spent,'One shared mode opportunity')
    rejects(lambda:d.special(stats,1,Wallet(),'howl',legal=True),'Enemy mode cannot reuse same Howl')
    d.shift(stats,wolf,'w',2,Wallet(),legal=True);d.shift(stats,moon,'moon2',3,Wallet(),legal=True)
    d.mooncursed_howl(stats,3,Wallet(),['b'],5,['empty'],legal=True)
    check(d.surges==4 and 'empty' not in d.buffers.grants,'Exhausted legal Howl pays but creates no zero grant')
    stats,d=state();d.shift(stats,moon,'moon',0,Wallet(),legal=True)
    d.mooncursed_howl(stats,1,Wallet(),['a'],8,['ally'],legal=True)
    d.revert(2,Wallet(),legal=True);check(d.buffers.amount('a')==8,'Mooncursed ally shield survives reversion')
    d.buffers.completed_long_rest('a',1);check(d.buffers.amount('a')==0,'Mooncursed uses recipient default lifetime')

    earth='druid.arch.earth-warden-dire-bear';stats,d=state(attuned=(earth,));d.regular_start(1,actual_regular_marker=True)
    d.shift(stats,earth,'earth',0,Wallet(),legal=True);d.special(stats,0,Wallet(),'slam',legal=True)
    d.shift(stats,wolf,'wolf',1,Wallet(),legal=True);d.shift(stats,earth,'earth2',2,Wallet(),legal=True)
    rejects(lambda:d.special(stats,2,Wallet(),'slam',legal=True),'Slam recharge survives shifts')
    rejects(lambda:d.regular_start(2,actual_regular_marker=False),'Extra turn cannot tick recharge')
    d.regular_start(2,actual_regular_marker=True);rejects(lambda:d.special(stats,6,Wallet(),'slam',legal=True),'Recharge2 not ready next start')
    d.regular_start(3,actual_regular_marker=True);d.special(stats,12,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==5,'Slam ready at second later regular start')

    frost='druid.hero.winterfang.frost-wyrmling';stats,d=state(circle='Winterfang')
    d.shift(stats,frost,'frost',0,Wallet(),legal=True);d.special(stats,0,Wallet(),'breath',legal=True)
    d.shift(stats,wolf,'wolf',1,Wallet(),legal=True);d.shift(stats,frost,'frost2',2,Wallet(),legal=True)
    rejects(lambda:d.special(stats,2,Wallet(),'breath',legal=True),'Breath remains spent across new instances')
    d.completed_short_rest(1,actual_completed=True);d.special(stats,3,Wallet(),'breath',legal=True)
    check(d.rest_uses['short:'+frost]==1,'Actual SR restores source use only')
    rejects(lambda:d.completed_short_rest(1,actual_completed=True),'No fabricated repeated SR')

    elemental='druid.hero.moon.elemental-shapeshifting';stats,d=state()
    d.shift(stats,elemental,'air',0,Wallet(),legal=True,variant='air')
    d.natural_endpoint(stats,600,renew=True)
    check(d.rest_uses['long:elemental']==1,'Same Elemental renew does not pay entry use')
    d.shift(stats,elemental,'water',601,Wallet(),legal=True,variant='water')
    check(d.attack(stats,601,Wallet(),legal=True)['profile']['damageType']=='cold','Subtype identity sets actual damage')
    rejects(lambda:d.shift(stats,elemental,'fire',602,Wallet(),legal=True,variant='fire'),'Two Elemental entries remain finite at20')
    saved=d.surges;d.completed_long_rest(stats,1,attuned=(),actual_completed=True)
    check(d.reserve==44 and d.surges==6 and d.current.instance_id=='water','Actual LR refills reserve, not form identity')

    brood='druid.hero.rotshaper.insect-broodmother';world=CreatureWorld();stats,d=state(circle='Rotshaper',creatures=world)
    out=d.shift(stats,brood,'brood',0,Wallet(),legal=True,spawn=True,spawn_legal=False)
    check(out['spawnPayment'] is None and d.surges==6,'Invalid optional spawn does not undo form or pay')
    rejects(lambda:d.special(stats,1,Wallet(),'spawn',legal=True),'No later spawn window')
    d.special(stats,1,Wallet(),'negate-critical',legal=True)
    check(d.surges==5,'Separate crit-negation still available')
    d.shift(stats,wolf,'wolf',2,Wallet(),legal=True)
    out=d.shift(stats,brood,'brood2',3,Wallet(),legal=True,spawn=True,spawn_legal=True)
    check(out['spawnPayment']['formSurgePaid'] and d.surges==4,'Valid entry spawn pays exactly one Surge')
    c=Creature('swarm','d','d','druid',brood,'swarm','finite',20,20,20,15,30,expiry=ClockMarker(63),parent_form='brood2')
    independent=replace(c,instance_id='independent',parent_form=None)
    world.creatures['swarm']=c;world.creatures['independent']=independent
    d.natural_endpoint(stats,603,renew=True)
    check(c.expiry==ClockMarker(63),'Renewal never extends independent creature deadline')
    d.revert(604,Wallet(),legal=True)
    check(c.state=='ended' and independent.state=='active','Parent ending only removes its own dependent swarm')

    # Enumerate competing values and damage: winner never stacks and conservation.
    scenarios=0
    for old in range(9):
        for new in range(9):
            for damage in range(13):
                b=BufferLedger()
                if old:b.offer(grant('old',old))
                b.offer(grant('new',new))
                winner=max(old,new)
                out,e=b.core_damage('d','packet',LifeState(100,100,winner),damage)
                assert b.amount('d')==max(0,winner-damage)
                assert out.hp==100-max(0,damage-winner)
                if old and old>=new and damage<old:assert b.current('d').grant_id=='old'
                scenarios+=1
    check(scenarios==1053,'Arbitration/damage conservation scenarios')
    report={'status':'PASS','checks':checks,'arbitrationDamageScenarios':scenarios,
            'formProfiles':len(PROFILES),'reviewStatus':'IMPLEMENTED; GPT implementation review pending',
            'scope':'Selected grant/form interface only; not full source cards, item/weapon taxonomy, full runtime or human balance.'}
    out=Path(__file__).resolve().parents[1]/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json'
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
if __name__=='__main__':main()

```

## docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json
SHA256 e93edfbe056a5e10034e8a47730b5ccff90864827f66d5c68c372837bc2cd370
```json
{
  "status": "PASS",
  "checks": 152,
  "arbitrationDamageScenarios": 1053,
  "formProfiles": 26,
  "reviewStatus": "IMPLEMENTED; GPT implementation review pending",
  "scope": "Selected grant/form interface only; not full source cards, item/weapon taxonomy, full runtime or human balance."
}

```

## docs/mechanics/FORM_TEMP_HP_SOURCE_VALIDATION.json
SHA256 c0d708b52f492dfc5a1ee4e6fbf0636381cb2f50577c14417f6427c977602f30
```json
{
  "status": "PASS",
  "meaning": "Source preservation/integrity only, not discussion or implementation approval",
  "sourceRecords": 175,
  "supportingPassages": 5,
  "druidMetadata": "PASS"
}

```

## Exact175 disposition IDs
```json
[
  {
    "id": "cleric.engine[7]",
    "role": "GUARD/PREV — Cleric",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "cleric.hero.saint.divine-rebirth",
    "role": "BUF/PREV — Cleric",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "cleric.hero.saint.resurrection",
    "role": "BUF/PREV — Cleric",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "crimson-agent.engine[5]",
    "role": "GUARD/PREV — Crimson Agent",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "crimson-agent.arch.veinweave-bloodshield",
    "role": "BUF-LINKED — Crimson Agent",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "crimson-agent.hero.bloodweaver.bloodbond",
    "role": "BUF/PREV — Crimson Agent",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "crimson-agent.hero.bloodweaver.crimson-pact",
    "role": "BUF/PREV — Crimson Agent",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "dragoon.hero.dragon-guardian.momentum-shield",
    "role": "BUF — Dragoon",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "dragoon.hero.dragon-guardian.bastion-descent",
    "role": "BUF — Dragoon",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "dragoon.hero.dragon-guardian.momentum-barrier",
    "role": "BUF — Dragoon",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "druid.engine[0]",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.engine[1]",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.engine[2]",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.engine[3]",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.engine[4]",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.engine[5]",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.engine[6]",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.druidic",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.spellcasting",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.shapeshifting",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.wolf-form-striker",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.bear-form-tank",
    "role": "FORM+BUFFER — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.hawk-form-scout",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.boar-form-brawler",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.panther-form-stealth",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.timeless-body",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.beast-spells",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.archdruid",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.dire-wolf",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.earth-warden-dire-bear",
    "role": "FORM+BUFFER — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.sky-serpent",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.ironhorn-ram",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.shadow-lynx",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.land.bonus-cantrip",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.land.natural-recovery",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.land.land-s-stride",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.land.nature-s-ward",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.land.blight-elk",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.land.tanglemaw",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.land.nature-s-sanctuary",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.moon.combat-shapeshifting",
    "role": "PREV/FORM dependency — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.moon.circle-forms",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.moon.primal-strike",
    "role": "FORM-CORE — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.moon.beastlord-alpha-animal-hybrid",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.moon.mooncursed",
    "role": "FORM+BUFFER — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.moon.elemental-shapeshifting",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.storm.storm-magic",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.storm.thunderous-strike",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.storm.storm-s-embrace",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.storm.tempest-raptor",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.storm.thunderhorn-stag",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.storm.eye-of-the-storm",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.thorns.toxic-affinity",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.thorns.blighted-touch",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.thorns.withering-aura",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.thorns.blight-elk",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.thorns.tanglemaw",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.thorns.master-of-decay",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.winterfang.frost-magic",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.winterfang.cold-resistance",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.winterfang.winter-s-embrace",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.winterfang.snow-leopard",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.winterfang.frost-wyrmling",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.winterfang.master-of-winter",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.rotshaper.vermin-affinity",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.rotshaper.swarm-summoning",
    "role": "PREV/FORM dependency — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.rotshaper.plague-bearer",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.rotshaper.carrion-rat-king",
    "role": "FORM+CREATURE-DEPENDENCY — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.rotshaper.insect-broodmother",
    "role": "FORM+CREATURE-DEPENDENCY — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.rotshaper.master-of-vermin",
    "role": "FORM+CREATURE-DEPENDENCY — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.ashen-grove.fire-affinity",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.base.ashen-grove.blazing-rebirth",
    "role": "BUF — Druid non-form",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.arch.ashen-grove.flame-stride",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.ashen-grove.charbear",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.ashen-grove.blazewood-stag",
    "role": "FORM — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "druid.hero.ashen-grove.master-of-ash",
    "role": "ADJACENT/GUARD — Druid",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats."
    ]
  },
  {
    "id": "mage.base.resonance-shield",
    "role": "BUF — Mage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mage.hero.archmage.empowered-link",
    "role": "BUF-MOD — Mage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mage.hero.archmage.harmonized-core",
    "role": "BUF — Mage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mage.hero.archmage.arcane-sanctuary",
    "role": "BUF — Mage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mage.hero.lich.lingering-malice",
    "role": "BUF — Mage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mage.hero.lich.soulbound-ritual",
    "role": "BUF/PREV — Mage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mirrorsage.engine[2]",
    "role": "BUF/PREV — Mirrorsage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mirrorsage.hero.light-weaver.radiant-archive",
    "role": "BUF/PREV — Mirrorsage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mirrorsage.hero.light-weaver.blessing-echo",
    "role": "BUF/PREV — Mirrorsage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mirrorsage.hero.light-weaver.light-binding",
    "role": "BUF/PREV — Mirrorsage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "monk.base.discipline-initiate",
    "role": "BUF — Monk",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.engine[13]",
    "role": "GUARD/PREV — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.spiral-touched.spiral-touched-boon-v",
    "role": "DEFER — Time Loop",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "oracle.supplement.flame.flame-revelation-mastery",
    "role": "BUF/PREV — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.life.overflowing-light",
    "role": "BUF/PREV — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.life.life-revelation-mastery",
    "role": "BUF/PREV — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.engine[5]",
    "role": "BUF — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.base.bolstering-presence",
    "role": "BUF — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oathbreaker-shared.dread-shelter",
    "role": "BUF — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oathbreaker-shared.black-manifestation",
    "role": "BUF — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oath-of-mercy.channel-life",
    "role": "HEAL-GUARD/PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression",
    "role": "HEAL-GUARD/PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oath-of-the-ancients.primordial-surge",
    "role": "BUF — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oath-of-the-chain.linked-ward",
    "role": "BUF/REDIRECTION-PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oath-of-the-chain.final-stand",
    "role": "BUF/REDIRECTION-PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oath-of-the-chain.unbroken-covenant",
    "role": "BUF/REDIRECTION-PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin",
    "role": "HEAL-GUARD/PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oath-of-the-martyr-king.king-s-smite",
    "role": "BUF/SMITE-PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oath-of-the-martyr-king.noble-bearing",
    "role": "BUF/SMITE-PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oath-of-the-martyr-king.last-king-s-gift",
    "role": "BUF/DEATH-PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura",
    "role": "HEAL-GUARD/PREV — Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "ranger.engine[5]",
    "role": "BUF — Ranger",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "ranger.hero.warder.nature-s-blessing",
    "role": "BUF — Ranger",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "ranger.supplement.master-of-the-hunt-new-hero-capstone",
    "role": "BUF — Ranger",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "shaman.arch.totem-pulse",
    "role": "BUF — Shaman",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "shaman.hero.bloodcaller.blight-totem",
    "role": "HEAL-GUARD/PREV — Shaman",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "soldier.base.rally-point",
    "role": "BUF — Soldier",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "soldier.hero.champion.rallying-cry",
    "role": "BUF — Soldier",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "soldier.supplement.final-command",
    "role": "BUF — Soldier",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "tinker.hero.artificer.protective-programming",
    "role": "BUF/DEVICE-PREV — Tinker",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "tinker.hero.artificer.nano-aegis-drone",
    "role": "BUF/DEVICE-PREV — Tinker",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.base.mutation-surge",
    "role": "BUF — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.hero.wardborn.aegis-incarnate",
    "role": "REDIRECTION/PREV — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.supplement.bone-hardened",
    "role": "DR/PREV — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "wizard.engine[10]",
    "role": "BUF — Wizard",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "wizard.hero.spellbinder.knowledge-shield",
    "role": "BUF-RIDER — Wizard",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "wizard.hero.spellbinder.spell-absorption",
    "role": "BUF — Wizard",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "wizard.hero.necromancer.arcane-leech",
    "role": "BUF — Wizard",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mage.hero.lich.undead-immunities",
    "role": "TRANSFORMATION GUARD — Mage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mirrorsage.arch.advanced-mirrorcall",
    "role": "APPEARANCE / prior creature interface — Mirrorsage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "mirrorsage.arch.mirror-shift",
    "role": "APPEARANCE / prior creature interface — Mirrorsage",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.base.serum-tolerance",
    "role": "GUARD — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.arch.intimidating-transformation",
    "role": "TRANSFORMATION-CONTROL only — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.hero.wardborn.controlled-transformation",
    "role": "COSMETIC TRANSFORMATION — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.hero.wardborn.warding-mutation",
    "role": "TEMPORARY TRANSFORMATION DEFENSE — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.hero.ironskin.adaptive-perfection",
    "role": "TEMPORARY TRANSFORMATION DEFENSE — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.hero.ironskin.adaptive-mutation",
    "role": "TEMPORARY TRANSFORMATION DEFENSE — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.hero.dreadspawn.abomination-ascendant",
    "role": "ANATOMY TRANSFORMATION — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.hero.dreadspawn.apex-aberration-1-day",
    "role": "TEMPORARY TRANSFORMATION DEFENSE — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.hero.dreadspawn.horrific-mutation",
    "role": "TRANSFORMATION-CONTROL only — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.supplement.apex-form",
    "role": "MUTATION STATE, not Druid form — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "warrior.supplement.butcherform-chassis",
    "role": "MUTATION STATE, not Druid form — Warrior",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "monk.arch.tortoise.final-form-bastion-of-breath",
    "role": "NAMED “FORM”, no body replacement — Monk",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "monk.hero.iron-fist-master.steel-reflection-form",
    "role": "NAMED “FORM”, no body replacement — Monk",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.shared.oracle-s-burden",
    "role": "INTRINSIC TRANSFORMATION/curse state — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.curse.consumed",
    "role": "INTRINSIC TRANSFORMATION/curse state — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.consumed.consumed-boon-i",
    "role": "INTRINSIC TRANSFORMATION/curse state — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.consumed.consumed-boon-ii",
    "role": "INTRINSIC TRANSFORMATION/curse state — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.consumed.consumed-boon-iii",
    "role": "INTRINSIC TRANSFORMATION/curse state — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.consumed.consumed-boon-iv",
    "role": "INTRINSIC TRANSFORMATION/curse state — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.consumed.consumed-boon-v",
    "role": "INTRINSIC TRANSFORMATION/curse state — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.ancestor.spirit-walk",
    "role": "ONE CHARACTER / TWO POSITIONS — Oracle",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "oracle.supplement.stars.clarity",
    "role": "PERCEPTION/PREV — Oracle/Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "paladin.hero.divine-sense",
    "role": "PERCEPTION/PREV — Oracle/Paladin",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "bard.base.lingering-notes",
    "role": "BARD-BUFFER / structured card",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "bard.base.chant-of-renewal",
    "role": "BARD-BUFFER / structured card",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "bard.arch.chorus-shield",
    "role": "BARD-BUFFER / structured card",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "bard.harmony.protective-verse",
    "role": "BARD-BUFFER / structured card",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "bard.harmony.inspiring-performance",
    "role": "BARD-BUFFER / structured card",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "bard.virtuoso.harmonic-resonance",
    "role": "BARD-BUFFER / structured card",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "feat:chef",
    "role": "FEAT — incomplete buffer contract",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "feat:empowered_summoning",
    "role": "FEAT — bounded buffer source",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "feat:field_medic",
    "role": "FEAT — bounded buffer source",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "feat:inspiring_leader",
    "role": "FEAT — incomplete buffer contract",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "feat:blood_ritual",
    "role": "FEAT — bounded buffer source",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Full feat target-count completion remains open; this interface fixes only independent offered amounts/lifetimes and no invented blood HP cost."
    ]
  },
  {
    "id": "feat:necrotic_affinity",
    "role": "FEAT — bounded buffer source",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": [
      "Selected resistance/Reaction prevention/post-packet shield integration only; extra-hit and anti-resurrection clauses still need full feat review."
    ]
  },
  {
    "id": "feat:soul_cage",
    "role": "FEAT — incomplete buffer contract",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "ordinary-spell:resonance-shield",
    "role": "SPELL — operational buffer overlay",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "ordinary-spell:heroism",
    "role": "SPELL — operational buffer overlay",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "ordinary-spell:spare-the-dying",
    "role": "SPELL — PREV stabilization",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "ordinary-spell:false-life",
    "role": "SPELL — operational buffer overlay",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "ordinary-spell:harmonic-bulwark",
    "role": "SPELL — blocked buffer review",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "ordinary-spell:shapechange",
    "role": "SPELL — blocked transformation review",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "ordinary-spell:polymorph",
    "role": "SPELL — blocked transformation review",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "ordinary-spell:true-polymorph",
    "role": "SPELL — blocked transformation review",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "ordinary-spell:mass-polymorph",
    "role": "SPELL — blocked transformation review",
    "status": "DEFERRED: exact role discussed; named component completion pending",
    "open": [
      "Named component remains unimplemented; needs its specific content/world-state completion batch."
    ]
  },
  {
    "id": "v6-trait:consume-decay",
    "role": "V6 ancestry buffer",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "v6-trait:battle-cry",
    "role": "V6 ancestry buffer",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  },
  {
    "id": "v6-trait:soul-drain",
    "role": "V6 ancestry buffer",
    "status": "IMPLEMENTED / TESTED: selected role; GPT implementation review pending",
    "open": []
  }
]
```
