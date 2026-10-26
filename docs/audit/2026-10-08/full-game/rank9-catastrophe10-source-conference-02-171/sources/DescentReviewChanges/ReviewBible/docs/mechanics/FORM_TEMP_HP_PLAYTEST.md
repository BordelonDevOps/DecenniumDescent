# Forms and temporary HP

**REVIEWED / reference-VALIDATED — selected form and temporary-HP interfaces.** This overlay covers 175 exact source roles, five support passages, 26 Druid form profiles and selected common interfaces. GPT approved the corrected reference and its clock-initialization addendum; 165 contract checks and 1,053 shield/damage scenarios pass. It does not close full class cards, feats, ancestry, ordinary spell catalogs, equipment or the whole game. Original cards and historical text remain unchanged in the [source register](FORM_TEMP_HP_SOURCE_BINDINGS.md). Use the [Druid form quick reference](DRUID_FORM_QUICK_REFERENCE.md) for the compact form and special-cost tables.

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

The reference uses one `OwnerRechargeClock` timeline across both contexts. In initiative, actual regular starts consume due owner markers; extra turns do not tick. Outside initiative, advancing actual elapsed time consumes the same six-second markers. Leaving and reentering initiative preserves the next due marker, so an elapsed tick and a turn start at that same boundary cannot count twice. Actual completed rests advance this downtime clock, allowing a two-round recharge to mature during the rest. Form changes themselves provide no ticks.

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

Form instance IDs are reserved globally in the shared world buffer ledger, including forms with no entry shield. A second owner cannot reuse one: duplicate IDs fail before payment or cleanup. This prevents one Druid's reversion from ending another Druid's form-dependent swarms. All completed/ended instance IDs remain reserved to prevent later identity reuse.

The complete equipment compatibility matrix, global natural-weapon taxonomy, full feat/ancestry/spell catalogs, Time Loop world conservation, human balance and the full runtime remain unfinished. All175 exact roles have been discussed; that is not a claim that every clause on every card is implemented or the whole game is complete.

[Confirmed notebook closure](../../../../docs/audit/2026-10-08/full-game/GPT_FORM_TEMP_HP_FINAL_CLOSURE.md) records the bounded approval. The five named transformation/buffer spell proposals continue separately; their original deferred classification is retained as review history.

The five originally deferred ordinary spells now have a [separately reviewed and promoted interface](TRANSFORMATION_SPELL_PLAYTEST.md), with216 checks and729 spatial scenarios. Their historical source snapshots remain unchanged and exact approved overlay evolution is validated. The full Chef, Inspiring Leader and Soul Cage clauses are now [separately reviewed and provisionally promoted](BUFFER_FEAT_PLAYTEST.md) within the complete eight-feat package. Time Loop world conservation is the single remaining originally deferred component.
