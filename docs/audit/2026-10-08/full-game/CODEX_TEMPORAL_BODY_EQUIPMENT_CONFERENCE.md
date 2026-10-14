# Complete parent integration: ordinary body/equipment gaps

Both prerequisites now have actual notebook closure: the59-method operation journal and the15-method exact-reference Transaction extension (207 regression methods remain passing). Full parent restoration and all seven larger domains remain open. I am now joining the actual source holders, rather than declaring reference transport to be full restoration.

The source comparison exposes an ordinary-play gap relevant to the full game: the reviewed form guide says Druid gear melds, but DruidState has no Body/equipment reference. Its shift/revert/end methods do not update TransformationWorld.Body.equipment/melded/size/mass or request reversion placement. The current operation journal calls those native methods directly. In contrast, transformation spells do update the same Body and maintain melded/lost gear, sponsor slots and placement flags. A complete temporal planner cannot restore an ordinary state that the shared world never actually represented.

Please settle these three connected issues from the attached actual code and rules. Label recovered rules versus new provisional decisions. We need a complete implementable ordinary bridge, not a Boolean claiming gear/geometry is handled. Keep current stat/cadence/conservation and no-refund rules intact.

1. SHARED BODY / ORDINARY DRUID EVENTS. Confirm the exact bridge over the one real Body: initial Druid entry melds eligible currently equipped items; form-to-form changes preserve the original meld set without returning/re-equipping items or replenishing them; actual final reversion/expiry/damage ending returns only surviving, still-owned original melded items. A spell replacing a Druid form is a continuous transformation and must not briefly make gear usable. Describe when Body.size, placement flags and geometry must update on entry/change/end, and how a failed placement is resolved without granting a free move or consuming entry costs before legality is known. Address Tiny Hawk, optional Large forms, flying/burrowing/unsupported endings, and the fact that the present kernel's geometry supports only finite level ground. We must develop the missing interactions, not silently call the limited geometry a complete game.

2. MASS AND SAME PHYSICAL IDENTITY. The Druid profiles specify size but no mass. Body.mass participates in True Polymorph object-output caps, so borrowing unchanged root mass would become an unspoken gameplay rule. Please identify existing mass authority if present; otherwise settle a usable explicit provisional rule for mass across these bounded Druid forms/variants. Compare retaining root mass versus a profile-based mass rule, including Tiny flight, Large forms, carrying/load and True Polymorph's min(current mass, original mass) cap. Do not introduce harvestable/saleable derivative material or duplicate physical roots. Specify what must be recorded at actual entry and what current conserved inventory/load owns.

3. EQUIPMENT / PHYSICAL CUSTODY / RECONCILIATION. The selected form guide leaves the complete item/anatomy compatibility matrix unfinished. Establish common source-grounded defaults now for worn armor, shields/held weapons, passive numeric magic, carried containers, and newly acquired external gear, distinguishing all26 Druid profiles from the12 finite spell profiles with explicit hands. Define what restores to the original meld set, what remains usable external equipment, what must drop at the legal current/nearest adjacent placement, and which real transfer/destruction blocks versus survives temporal restoration. Identify any exact remaining source exception rather than treating every item as a generic Boolean certificate. Current item charges/stock/durability and ownership stay conserved. The original item and class catalogs remain authoritative and intact.

The current profile/equipment rules and actual native fields follow. This is a source/design conference for the next integrated ordinary/temporal body layer, not a request to approve unimplemented behavior. Once settled, I will implement the ordinary bridge and full proposed-state/watch/commit path and submit actual tests. Full-game flow and GitHub delivery remain open.

## docs/mechanics/FORM_TEMP_HP_PLAYTEST.md
Source SHA-256 `a447c60f2dfaaca11f7bd0d4f89bbabe95a29587d3c9d4b81fa26d1bca5faba4`

```
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

```

## docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md
Source SHA-256 `b0551148795953c4435cd2e528fcfca84f9cfae97a6684f2b7334a10955dde23`

```
# Transformation and Harmonic Bulwark playtest rules

**REVIEWED / reference-VALIDATED within the five-spell scope.** This guide supplies five promoted operational-playtest overlays and twelve finite forms. The catalog now contains83 operational drafts and765 unfinished spells. The candidate versions remain preserved as review history. Original spells, class access, printed schools, base RP and the frozen class packet remain preserved. All new boundaries below are provisional design decisions agreed in the notebook, not recovered original rules. Numerical balance and table playtesting remain outstanding.

## Cast summary

All five use an Action and V/S/F. Ordinary known/prepared access, class-level gates, base RP, component legality, Dissonance/Refrain, exact class modifications, countering and concentration damage checks remain mandatory.

| Spell | Operational range/targets | Base RP | Effect clock |
|---|---|---:|---|
| Harmonic Bulwark |60ft; one willing perceived creature|5 plus chosen X|Cast instantaneous; accepted shield to depletion/replacement/recipient's completed long rest|
| Polymorph |60ft; one perceived physical creature|7|Concentration60seconds|
| Shapechange |Self|26|Concentration60seconds|
| True Polymorph |120ft; one eligible physical creature or discrete object|26|Concentration60seconds, then until dispelled without concentration|
| Mass Polymorph |120ft;1–10 distinct perceived physical creatures|26|One concentration record,60seconds|

These are the selected spells' unchanged base costs; exact class access is read from the preserved catalog. Shapechange's printed120-foot source field remains in provenance; operational Self is explicitly NEW. Harmonic Bulwark's Action/range/components are NEW design, not a proven merge with the older Mana Shield name.

Before paying, choose legal targets, output profiles/templates and all spatial placements. For a concentration spell, account for the original anatomy that will return when your own old concentration ends. That projected anatomy must still be eligible for the prospective cast. Check all costs and components. Then:

1. Commit Action and actual RP payment, with ordinary class cadence consequences.
2. End your previous concentration, including all remaining Mass links, even if the new spell subsequently fails.
3. Resolve countering and initial saves. No post-commit refund.
4. Apply successful transformations. An anatomy maintained by another source persists until a successful legal replacement. No displaced anatomy remains underneath the new form.

Beginning an unrelated concentration spell does not end an already permanent True Polymorph. Starting any new concentration spell must use the shared concentration ledger, including spells outside this packet.

## Harmonic Bulwark

Choose additional conversion payment X from0 through current PB before commitment. The shield offered to the chosen recipient is **5 × (actual base RP paid + X)**. An exact legal discount can reduce the base payment. X is additional, actually paid and never discounted. Dissonance or other surcharge payments add no shield credit. Refrain affects post-cast Dissonance under ordinary rules; this spell invents no immediate Refrain surcharge.

A zero-credit fresh cast is illegal. Free casts do not mint shield value. An exact effect copying an already-resolved buffer event needs its own explicit permission. Pay Action, actual cast cost and X before countering and the normal strongest-only comparison. A stronger or equal existing shield stays, but the entire payment remains spent. A countered spell produces no offer. The accepted shield belongs to the recipient, does not heal, and normally ends at that recipient's next completed long rest.

Example: actual base payment3, X2 and surcharge2 costs7RP and offers25temporaryHP. It does not offer35. If the recipient already has25 or more, their current grant stays with its original lifetime.

## The finite spell forms

The profiles below are NEW bounded spell rules. They are not monster stat blocks or Druid forms. Polymorph and Mass use only R4. Shapechange and True may use R4 or R9. The names do not grant creature-type tags.

| Profile | Tier | Size | Movement (ft) | Speech/hands | AC | One natural attack | Additional anatomy |
|---|---|---|---|---|---|---|---|
| Humanoid |R4|Medium|walk30|yes/yes|normal|1d6+M bludgeoning|—|
| Predator |R4|Medium|walk40|no/no|max(normal,13)|1d8+M slashing|—|
| Brute |R4|Large|walk30|no/no|max(normal,15)|2d6+M bludgeoning|—|
| Avian |R4|Small|walk10, fly50|no/no|max(normal,13)|1d6+M slashing|—|
| Aquatic |R4|Medium|walk20, swim50|no/no|max(normal,14)|1d8+M piercing|water breathing|
| Burrower |R4|Medium|walk30, loose-soil burrow15|no/no|max(normal,14)|1d8+M bludgeoning|—|
| Greater brute |R9|Large|walk40|no/no|max(normal,17)|2d8+M bludgeoning|—|
| Greater winged |R9|Large|walk20, fly60|no/no|max(normal,16)|2d8+M slashing|—|
| Elemental air |R9|Medium|fly60, hover|no/no|16|2d8+M lightning|lightning resistance|
| Elemental earth |R9|Large|walk30, loose-soil burrow20|no/no|17|2d8+M bludgeoning|—|
| Elemental fire |R9|Medium|walk40|no/no|16|2d8+M fire|fire resistance|
| Elemental water |R9|Medium|walk20, swim60|no/no|16|2d8+M cold|cold resistance, water breathing|

All supplied attacks have5-foot reach and one attack per ordinary Attack Action. No Multiattack, legendary action, class, resource pool or monster ability is imported. Exact existing subject features may modify the action only when they explicitly apply to natural/form attacks or the Attack Action without an unavailable weapon/anatomical requirement. Weapon-only features remain gated. Being granted by a spell does not automatically make an attack magical for resistance/immunity bypass; no generic magical-attack flag is granted. Broader taxonomy remains a separate exact-source interface.

“Normal” AC excludes melded armor/shields and includes only certified compatible passives and actually worn compatible external equipment. Fixed elemental AC remains the specified value. Ordinary sight/hearing remain; no special senses are granted. The chosen anatomy replaces size, movement, anatomical senses, speech, hands, original anatomical attacks and anatomy-dependent defenses. Original wings/claws/gills do not persist underneath an incompatible form unless their exact source says otherwise. Nonanatomical features retain their own predicates.

## Identity, attack statistics and equipment

Keep one physical identity and one current/max HP ledger, current temporary-HP grant, Wounds/injuries, death state, conditions, actual attributes, PB, class resources, rest/recharge uses, initiative, concentration and independent effect clocks. A form is never a second HP pool. Body matter lost or destroyed remains lost. Existing class abilities use the subject's normal statistics when anatomy permits them.

The transformed subject owns its attacks, damage and kills. Polymorph, Mass and Shapechange supplied attacks use the original caster's **current** spell attack and M=max(1, casting modifier). True snapshots caster spell attack, DC, PB, M and source class at casting, throughout shaping and permanence. Supplied natural attacks are not spell casts and do not automatically trigger caster “your spell deals damage,” spell-kill or per-cast resource features.

Creature-origin subjects retain their original creature-type, ancestry, class and soul identity. Object-origin manifestations have the `transformed-object` origin tag; profile names grant no humanoid/beast/elemental/undead tag. Immutable earliest origin follows every chain of transformations and control changes.

Original carried/equipped gear melds into a record and is unavailable for ordinary weapon/shield/component use. Compatible certified passive bonuses may remain. A handed form can acquire and use real external gear normally. On an internal Shapechange switch, keep compatible external items and drop incompatible items in the current space or nearest legal adjacent space; never add them to the old meld set. Dropped items remain there.

When a different successful transformation replaces a record, atomically close the old record, restore its still-existing original meld set, include legitimate currently equipped external items, and capture that resulting gear as the new record's meld set. There is no intervening action/reaction/targeting window. Destroyed, consumed, dropped or lost items are never recreated. This also applies when a spell ends a Druid form. Suppression is not record closure and never recaptures gear. Original melded gear remains inaccessible while suppressed, including weapons, armor and material components. External gear remains real and usable only when root anatomy is certified compatible.

## Initial saves, repeats and agency

Polymorph, Mass and True creature→creature allow a willing recipient to waive the initial CON save. Otherwise resolve CON against the original caster's current DC (True uses its casting snapshot). Success leaves the target unchanged. Exact transformation immunity and legendary defenses still apply.

Each unwilling transformed target may repeat that save at each original regular-turn end, and after the first event in each numbered round that causes **positive actual normal HP damage**, after all prevention and temporary HP. Temporary-HP-only loss does not qualify. Each target has a separate round ledger; a recast does not create a second damage-triggered save from the same round. Finish the actual packet and all same-packet death prevention before deciding whether a link remains for its repeat save.

The subject retains its decisions and an ordinary form attack. Losing hands/speech may restrict particular abilities, but the transformation does not impose whole-Action denial. A willing temporary creature-origin recipient with action-capable expressed anatomy can reject Polymorph, Mass or shaping True with its Action on its original regular turn. This permission remains while suppressed: a creature-origin object form temporarily expressing its root creature anatomy can reject then. Unsuppressed object anatomy is actionless and cannot reject; object-origin identities gain no player-style rejection right. Changing one's mind does not create hostile repeat saves. Shapechange uses ordinary concentration release and cannot invoke its internal switch while suppressed.

Mass makes independent saves for1–10 targets using preselected R4 profiles. For each target, O is the footprint remaining on a successful save and T is the footprint on failure/waiver. Before paying, every pair must support O/O, O/T, T/O and T/T without illegal overlap; each individual footprint must also fit terrain/other bodies. A target's own O/T may overlap. Apply successful changes simultaneously. Ending/replacing one target link leaves other links intact. There is no ongoing range tether.

## Endings, switching, suppression and geometry

Polymorph, Mass and Shapechange end at cast time+60seconds. True's stabilization checkpoint is the same absolute60seconds. Extra turns never extend these clocks. At a shared timestamp: finish an already-started event packet; process due hostile repeats; end successful saves; then expire temporary spells or stabilize surviving True links; then administrative cleanup. A successful final repeat prevents permanence.

Actual0HP, death or external Incapacitated after every same-packet replacement ends temporary spell anatomy, including both creature→creature and creature→object during True shaping. A legal “remain at1” keeps the form. Reversion never heals, clears Wounds, restores temporary HP or rerolls damage. Permanent True does not end merely at0/death; later dispel returns a still-dead/damaged original body and cannot recreate missing matter. Structural0 destroys an object-origin manifestation and releases its slot.

Shapechange's internal switch costs a Bonus Action, requires a different legal profile and space, and occurs at most once on each later original regular turn. It cannot occur on the casting turn, including a cast on an extra turn, and never occurs on an extra turn. It pays no new RP, makes no spellcast/Refrain event, resets no resources, and grants no free attack. Losing unsupported flight invokes ordinary falling.

A spell may successfully replace a Druid form, ending actual form-dependent effects without refunds. A Druid cannot Shapeshift while any spell-transformation record is active, including suppressed or permanent records. Temporary replacement requires at least the existing rank. Permanent True requires another successful True or an exact named exception. Same-profile new casts remain legal paid casts. These precedence checks apply to an old record that survives commitment; your own concentration record already ends when the new concentration cast commits.

Antimagic suppresses every transformation without ending its record. The root anatomy is expressed, concentration remains required where applicable, and the original clock continues. Temporary spells may expire while suppressed. True may stabilize while suppressed if concentration remains valid, then resume its permanent anatomy later. Suppression never releases a companion slot or creates a second hidden form. A suppressed record still follows the same replacement precedence.

Mandatory reversion uses the **same spatial anchor**. If root anatomy cannot fit, report `placementConflict` to canonical geometry. No automatic teleport through walls, free relocation or invented crushing damage occurs. Until resolved, overlap cannot establish legal movement/targeting through a barrier. **Open whole-game dependency:** the general mandatory-reversion geometry conflict procedure. The helper exposes this boundary rather than claiming that geometry subsystem is complete.

## True Polymorph object modes

True allows creature→creature, willing creature→object, eligible object→creature, and eligible object→object. Only one object/body is produced. Object input must be a discrete nonmagical, unattended, uncarried, unworn, unattuned Large-or-smaller object with canonical current/max structural HP. Artifacts, active magical devices, terrain/building structures, corpses/significant remains and undefined-durability objects are ineligible.

Those fresh-object admission checks apply to introducing an ordinary outside object. An already-active True Polymorph object anatomy can be replaced by another legal True Polymorph without pretending it is an unattended nonmagical outside object. A creature-origin person in object anatomy retains agency: creature-profile replacement permits a willing waiver or requires a CON save if unwilling; object-profile replacement requires willingness. Returning that person to creature anatomy preserves their original HP/Wounds/class/soul and creates no companion slot. Object-origin recasts retain all origin, value and slot constraints.

Object outputs are Tiny through Large, within one size category of the actual input, AC12, inert and nonmagical. Allowed templates: barrier/slab, ramp/wedge, open-container, static-furniture, simple-one-piece-tool. Static joined pieces and open hollow containers are allowed; actuated mechanisms, working hinges/latches/locks/keys, gears/clocks/traps, precision instruments, pressure vessels and documents/credentials are not. No output grants material resistance/immunity.

Require documented physical mass. Output mass cannot exceed the current input mass or earliest origin ceiling. Object-origin recoverable/sale value cannot exceed its earliest documented value; missing necessary mass/value makes that mode ineligible. Creature-origin object anatomy has no independent sale/salvage/harvest value. No mode produces food, medicine, ammunition, currency, gemstones, rare crafting material, valuables, consumable stock or magical properties. Chains never rebase the ceilings upward.

Creature→object retains the same character HP/Wounds/resources/history but supplies speed0, no Actions/Bonus Actions/Reactions, no speech/senses/hands. This is `actionlessObjectAnatomy`, **not** an automatic Incapacitated condition. A caster can therefore maintain their self-targeted shaping spell. Actual external Incapacitated still ends concentration/shaping normally. Permanent object anatomy has no voluntary rejection.

Object→creature uses a non-humanoid finite profile and exactly its existing structural current/max HP ledger. It has ordinary sight/hearing, saves equal to captured caster PB, ordinary unproficient checks+0, no special senses unless listed, no Wounds/death saves/Stable/dying state, soul, class/rest resources, reproduction, resurrection or XP/loot/corpse entitlement. At structural0, it is destroyed; dispel does not rebuild it. Temporary HP may protect it. Ordinary healing cannot repair it, even after later transformations; exact nonorganic repair is a separate source interface.

Creature-origin currently in object anatomy cannot newly receive effects requiring a creature/living creature/ally creature. Ordinary healing eligibility returns with creature anatomy if other requirements permit it. Already-attached effects retain their own exact lifetimes; a pulse needing fresh creature eligibility must recheck it. Transformation does not convert healing into object repair.

## Object companions

A successful object→creature application reserves one object-creature slot immediately, including shaping. It belongs to the original creating caster and stays occupied through stabilization, suppression, control changes and legal creature-profile replacements by other casters. Recasting the same body consumes no second slot and does not transfer control or sponsorship. A distinct second permanent creature cannot be created while the slot is occupied.

Release the slot only on actual ending/dispel to the original object, physical destruction or an allowed replacement into object anatomy. A later fresh object→creature casting after such an ending uses its new creating caster's slot. No free dismissal exists after stabilization. Existing companion transformations do not automatically change their owner/allegiance.

Use the current controller's **shared** companion Bonus Action command and one offensive-companion allowance,60-foot command range and actual perception, attached resolution, and uncommanded move+Dodge. No separate full damaging turn appears. Source-qualified exceptions remain exact. If an issued command becomes illegal, resources stay spent and the order does not execute. Supplied attacks still belong to the subject, with the original transformation caster's statistics.

## Evidence and implementation boundary

Notebook decisions are preserved in `docs/audit/2026-10-08/full-game/GPT_TRANSFORMATION_SPELL_FIRST_REVIEW.md`, `GPT_TRANSFORMATION_SPELL_BOUNDARIES.md` and `GPT_TRANSFORMATION_SPELL_FINAL_INTERFACES.md` in the main project. Exact source objects/hashes are in `TRANSFORMATION_SPELL_SOURCE_CANDIDATES.json`. The profiles carry evidence hashes. `batch_transformations.json` is the reviewed operational source; `candidate_transformations.json` remains inactive historical evidence.

`transformation_spell_playtest_rules.py` is a bounded contract reference. The caller owns actual known/prepared access, range/LOS/components, canonical price/class cadence, rolls, geometry, same-packet prevention, concentration damage saves, turn/round calendar and source eligibility. It receives actual finalized HP state and never owns a second HP pool. All adapters must share one concentration ledger, buffer ledger, form identity registry and controller command ledger. The Druid guard is the only integration change to the existing form helper. GPT independently reviewed the actual code and216 contract checks plus729 spatial scenarios; the [bounded closure](../../../../docs/audit/2026-10-08/full-game/GPT_TRANSFORMATION_SPELL_FINAL_CLOSURE.md) supports this provisional promotion. Wider interfaces remain open.

```

## tools/form_temphp_playtest_rules.py
Source SHA-256 `97566962d3eddeca5966b4b58bbb3a5e53dc34d529afb5de033d4358397e2151`

```
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
        self.form_instances=set()
        self.spell_anatomies={}

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


class OwnerRechargeClock:
    """One owner timeline, shared by regular starts and downtime.

    The canonical six-second owner-marker phase survives initiative transitions.
    Reordering/extra turns cannot create earlier ticks. The scheduler must supply
    every actual regular start while in initiative. Outside, elapsed intervals
    consume the same next-due marker, never an additional parallel clock.
    """
    def __init__(self):
        self.mode='initiative';self.now=ClockMarker(0);self.next_tick=6
        self.ticks=0;self.last_regular=0;self.anchored=False

    def _time(self,now):
        marker=clock_marker(now);require(marker>=self.now,'Recharge time cannot move backward')
        return marker

    def _anchor(self,marker):
        if not self.anchored:
            self.next_tick=marker.seconds+6;self.anchored=True

    def regular_start(self,index,now,*,actual_regular_marker):
        marker=self._time(now);integer(index,'actual regular marker',1)
        require(self.mode=='initiative' and actual_regular_marker and index>self.last_regular,
                'New actual regular initiative marker required')
        self._anchor(marker)
        self.last_regular=index;self.now=marker
        if marker.seconds>=self.next_tick:
            self.ticks+=1;self.next_tick=marker.seconds+6

    def leave_initiative(self,now):
        marker=self._time(now);require(self.mode=='initiative','Already outside initiative')
        self._anchor(marker)
        self.now=marker;self.mode='outside'

    def advance_outside(self,now):
        marker=self._time(now);require(self.mode=='outside','Elapsed ticks only outside initiative')
        self._anchor(marker)
        if marker.seconds>=self.next_tick:
            count=int((marker.seconds-self.next_tick)//6)+1
            self.ticks+=count;self.next_tick+=6*count
        self.now=marker

    def enter_initiative(self,now):
        self.advance_outside(now);self.mode='initiative'

    def use(self,now):
        marker=self._time(now)
        self._anchor(marker)
        if self.mode=='outside':self.advance_outside(marker)
        else:self.now=marker
        # The cast/action does not tick or reset an existing owner's phase.
        return self.ticks


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
        self.recharge_clock=OwnerRechargeClock()
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

    def completed_long_rest(self,stats,epoch,*,attuned,actual_completed,now):
        self._stats(stats);self._validate_attunement(stats,attuned)
        require(actual_completed and epoch==self.long_epoch+1,'Actual next completed owner LR required')
        self.recharge_clock.advance_outside(now)
        self.long_epoch=epoch;self.short_epoch+=1;self._refill(stats,attuned)
        # Receiving default buffers is a separate recipient-calendar operation.
        # Form instances/local flags and independent clocks are NOT refreshed.

    def completed_short_rest(self,epoch,*,actual_completed,now):
        require(actual_completed and epoch==self.short_epoch+1,'Actual next completed SR required')
        self.recharge_clock.advance_outside(now)
        self.short_epoch=epoch
        self.rest_uses={k:v for k,v in self.rest_uses.items() if not k.startswith('short:')}

    def regular_start(self,index,now,*,actual_regular_marker):
        integer(index,'canonical regular marker',1)
        require(actual_regular_marker and index>self.regular_index,'No extra-turn/repeated recharge tick')
        self.recharge_clock.regular_start(index,now,actual_regular_marker=actual_regular_marker)
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
        require(self.owner not in self.buffers.spell_anatomies,
                'End active spell anatomy through its legal procedure before Druid Shapeshift')
        p=self._legal_profile(stats,source_id,variant,large);marker=clock_marker(now)
        identity(instance_id)
        require(instance_id not in self.buffers.form_instances,'Form instance identity already used anywhere in this world')
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
        self.buffers.form_instances.add(instance_id)
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
        # Canonical clock progress is independent of whether this ability is used.
        ticks=self.recharge_clock.use(now)
        if special_id=='spawn':require(f.entry_open,'Brood spawn requires the actual entry window')
        if q['payment']=='surge':
            require(special_id not in f.spent and self.surges>0,'Local special or global Form Surge exhausted')
        elif q['payment']=='recharge2':
            require(ticks>=self.recharges.get(f.source_id,0),'Slam source recharge still active across shifts')
        else:
            kind='short:' if q['payment']=='short-rest' else 'long:'
            require(self.rest_uses.get(kind+f.source_id,0)==0,'Shared per-rest special already spent')
        wallet.validate(action=q['action']);wallet.pay(action=q['action'])
        if q['payment']=='surge':f.spent.add(special_id);self.surges-=1
        elif q['payment']=='recharge2':self.recharges[f.source_id]=ticks+2
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

## tools/transformation_spell_playtest_rules.py
Source SHA-256 `91697863f6d19043787e17f19b4c127e6c32de32ad3867393566212533081d39`

```
"""Five-spell reference adapter. CANDIDATE: independent review pending.

Not a complete combat engine. Caller supplies canonical cast/access/geometry
legality, current caster statistics, actual save results, original-turn markers,
and already-finalized HP outcomes. One world/ledger per game; do not copy HP or
command ledgers. All preflight occurs before payment, then concentration ends,
then counters/saves resolve. Nothing here grants a class feature or source use.
"""
from dataclasses import dataclass, field
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import json

from spell_playtest_rules import SpellRuleError, integer
from form_temphp_playtest_rules import BufferLedger, BufferGrant, require
from redirection_playtest_rules import identity
from device_lifecycle_playtest_rules import Wallet, CommandLedger

PROFILES={p['id']:p for p in json.loads((Path(__file__).resolve().parents[1]/'data/playtest/spell_form_profiles.json').read_text(encoding='utf-8'))['profiles']}
SPELLS={'polymorph':4,'shapechange':9,'true-polymorph':9,'mass-polymorph':9}
SIZES=('Tiny','Small','Medium','Large','Huge','Gargantuan')
TEMPLATES=frozenset({'barrier/slab','ramp/wedge','open-container','static-furniture','simple-one-piece-tool'})


@dataclass(frozen=True)
class CastStats:
    owner: str
    source_class: str
    attack: int
    dc: int
    pb: int
    modifier: int

    def __post_init__(self):
        identity(self.owner);identity(self.source_class)
        require(type(self.attack) is int,'Actual signed spell attack required')
        integer(self.dc,'spell DC',1);integer(self.pb,'PB',2,6)
        integer(self.modifier,'M=max(1, casting modifier)',1)


@dataclass(frozen=True)
class CastPrice:
    spell_id: str
    rank: int
    base_paid: int
    other_paid: int
    quote: dict=field(compare=False)

    @classmethod
    def from_quote(cls,quote,*,actual_base_paid=None,exact_reduction_authorized=False):
        """Consume canonical quote_cast result; exact class discounts are external.

        This does not establish known/prepared access or grant a discount. Those
        gates must already have passed in the caller's source-qualified preflight.
        Refrain/Dissonance/trauma follow quote plus the canonical class interface.
        """
        base=integer(quote['baseRpCost'],'quoted base RP',0)
        extra=integer(quote['additionalRpCost'],'quoted additional RP',0)
        surcharge=integer(quote['surcharge'],'quoted surcharge',0)
        require(quote['cost']==base+extra+surcharge,'Inconsistent canonical quote')
        paid=base if actual_base_paid is None else integer(actual_base_paid,'actual base paid',0,base)
        require(paid==base or exact_reduction_authorized,'Exact base reduction authority required')
        identity(quote['spellId']);integer(quote['rank'],'rank',0,9)
        return cls(quote['spellId'],quote['rank'],paid,extra+surcharge,deepcopy(quote))

    @property
    def total(self):return self.base_paid+self.other_paid


def harmonic_bulwark(ledger,stats,price,wallet,grant_id,target,conversion,now,*,legal,countered=False):
    """Commit everything before countering/arbitration; return cadence quote.

    Exact free-copy permissions need their own source adapter. This method is a
    fresh paid cast and will not mint an offer with zero credited RP.
    """
    require(isinstance(ledger,BufferLedger) and isinstance(stats,CastStats),'Canonical state required')
    require(legal and price.spell_id=='harmonic-bulwark' and price.rank==3,'Legal Harmonic Bulwark cast required')
    integer(conversion,'conversion X',0,stats.pb)
    credited=price.base_paid+conversion
    require(credited>0,'Zero credited RP cannot create a fresh shield')
    if not hasattr(ledger,'ordinary_cast_events'):ledger.ordinary_cast_events=set()
    require(grant_id not in ledger.ordinary_cast_events,'Cast identity already committed, including countered casts')
    grant=BufferGrant(grant_id,'ordinary-spell:harmonic-bulwark',stats.owner,target,5*credited,
                      rest_epoch=ledger.rest_epochs.get(target,0))
    ledger.validate_offer(grant,now)
    wallet.validate(rp=price.total+conversion,action='action')
    wallet.pay(rp=price.total+conversion,action='action')
    ledger.ordinary_cast_events.add(grant_id)
    return {'paidRP':price.total+conversion,'creditedRP':credited,'cadenceQuote':deepcopy(price.quote),
            'offer':None if countered else ledger.offer(grant,now),'countered':bool(countered)}


class ConcentrationLedger:
    """One ledger shared by ALL concentration spells, including other adapters.

    Each entry's end callback must be total/nonthrowing after valid preflight.
    Starting after payment always destroys the former entry, even if the new
    spell is countered or every target saves. Call end on actual concentration
    failure/incapacitation or a legal voluntary release.
    """
    def __init__(self):self.current={}

    def end(self,owner,reason):
        old=self.current.pop(owner,None)
        if old:old[1](reason)
        return old[0] if old else None

    def start_committed(self,owner,cast_id,on_end):
        old=self.end(owner,'new-concentration')
        self.current[owner]=(cast_id,on_end)
        return old

    def detach(self,owner,cast_id):
        if self.current.get(owner,(None,))[0]==cast_id:del self.current[owner]


@dataclass(frozen=True)
class PhysicalOrigin:
    identity: str
    kind: str
    size: str
    type_tags: frozenset=frozenset()
    mass: int | None=None
    value: int | None=None

    def __post_init__(self):
        identity(self.identity);require(self.kind in ('creature','object'),'Immutable origin kind required')
        require(self.size in SIZES,'Actual original size required')
        if self.mass is not None:integer(self.mass,'recorded origin mass',1)
        if self.value is not None:integer(self.value,'documented original value',0)


@dataclass
class Body:
    """Single underlying physical identity. No transformation HP field exists.

    life is the actual mutable/canonical character or structural ledger object;
    the adapter never heals, reconstructs or replaces it. Origin is immutable.
    Gear IDs and availability represent real items, not inventory creation.
    """
    origin: PhysicalOrigin
    life: object
    size: str
    mass: int | None=None
    equipment: set=field(default_factory=set)
    melded: set=field(default_factory=set)
    lost_items: set=field(default_factory=set)
    destroyed: bool=False
    anatomy: str | None=None
    slot_sponsor: str | None=None
    controller: str | None=None
    placement_pending: bool=False
    placement_conflict: bool=False

    @property
    def identity(self):return self.origin.identity


@dataclass(frozen=True)
class Selection:
    target: str
    profile: str | None
    willing: bool
    # Geometry caller supplies occupied cells at the post-concentration-save
    # stage; every possible unchanged/transformed shape must individually fit.
    original_cells: frozenset
    transformed_cells: frozenset
    legal: bool
    object_template: str | None=None
    object_size: str | None=None
    object_mass: int | None=None
    object_value: int | None=None
    object_input_eligible: bool=False
    mundane_output_certified: bool=False


@dataclass
class Link:
    identity: str
    cast_id: str
    target: str
    profile: str | None
    willing: bool
    deadline: int
    state: str='shaping'
    object_template: str | None=None
    object_size: str | None=None
    object_mass: int | None=None
    last_switch: int | None=None
    suppressed: bool=False


@dataclass
class Cast:
    identity: str
    spell_id: str
    caster: str
    rank: int
    stats: CastStats
    casting_regular_index: int
    links: list=field(default_factory=list)
    state: str='committed'


def validate_mass_space(selections):
    require(1<=len(selections)<=10 and len({s.target for s in selections})==len(selections),
            'Choose1..10 distinct physical targets')
    for s in selections:
        require(s.legal and s.original_cells and s.transformed_cells,'Both possible footprints must individually fit')
    for a,b in combinations(selections,2):
        for aa,bb in product((a.original_cells,a.transformed_cells),(b.original_cells,b.transformed_cells)):
            require(aa.isdisjoint(bb),'Independent Mass outcomes could overlap')


class TransformationWorld:
    """Bounded anatomy/concentration bridge; no hidden previous-form stack."""
    def __init__(self,buffers,concentration):
        require(isinstance(buffers,BufferLedger) and isinstance(concentration,ConcentrationLedger),'Canonical shared ledgers required')
        self.buffers=buffers;self.concentration=concentration
        self.bodies={};self.casts={};self.links={};self.slots={};self.druids={}
        self.damage_rounds=set();self.damage_events=set();self.regular_ends=set();self.commands={}
        self.events=[]
        # Shared with the Druid admission bridge, including suppressed records.
        if not hasattr(buffers,'spell_anatomies'):buffers.spell_anatomies={}

    def add_body(self,body,*,druid=None):
        require(isinstance(body,Body) and body.identity not in self.bodies,'Register each physical identity once')
        require(body.size in SIZES and body.life is not None,'Actual anatomy and HP ledger required')
        require(not body.anatomy and not body.melded and not body.slot_sponsor,'Register at original anatomy, or restore complete serialized world')
        self.bodies[body.identity]=body
        if druid is not None:
            require(druid.owner==body.identity and druid.buffers is self.buffers,'Druid must share world and owner')
            self.druids[body.identity]=druid

    def current(self,target):
        body=self.bodies[target]
        return self.links.get(body.anatomy)

    def _current_creature(self,body):
        link=self.current(body.identity)
        if link and not link.suppressed:return link.profile is not None
        return body.origin.kind=='creature'

    def _validate_selection(self,spell_id,rank,s,caster):
        identity(s.target);require(s.target in self.bodies,'Known physical target required')
        b=self.bodies[s.target];old=self.current(s.target)
        require(s.legal and not b.destroyed,'Legal live physical target required')
        require(s.original_cells and s.transformed_cells,'Both individually legal footprints required')
        ends_own_concentration=bool(old and old.state=='shaping' and self.casts[old.cast_id].caster==caster)
        active_transformed_object=bool(old and old.profile is None and self.casts[old.cast_id].spell_id=='true-polymorph')
        # Validate target anatomy after the mandatory end of own concentration.
        creature=b.origin.kind=='creature' if ends_own_concentration else self._current_creature(b)
        if spell_id!='true-polymorph':require(creature,'This spell requires creature anatomy')
        if spell_id=='shapechange':require(s.target==caster and s.willing,'Shapechange is self only')
        if old and not ends_own_concentration:
            if old.state=='permanent':
                require(spell_id=='true-polymorph','Permanent True anatomy requires a new True Polymorph')
            else:require(rank>=self.casts[old.cast_id].rank,'New rank cannot replace higher-rank anatomy')
        if s.profile is not None:
            require(s.profile in PROFILES,'Unknown finite spell profile')
            p=PROFILES[s.profile]
            require(spell_id not in ('polymorph','mass-polymorph') or p['tier']=='R4','R9 profile unavailable')
            require(b.origin.kind!='object' or s.profile!='spellform.humanoid','Object origin cannot gain humanoid profile')
        else:
            require(spell_id=='true-polymorph' and (not (creature or b.origin.kind=='creature') or s.willing),
                    'Object output requires True and willingness of a retained creature-origin person')
            require(s.object_template in TEMPLATES and s.mundane_output_certified,'Bounded inert mundane template required')
            input_size=b.origin.size if ends_own_concentration else b.size
            input_mass=b.origin.mass if ends_own_concentration else b.mass
            require(s.object_size in SIZES[:4] and abs(SIZES.index(s.object_size)-SIZES.index(input_size))<=1,'Object output size illegal')
            require(input_mass is not None and b.origin.mass is not None,'Canonical current/origin mass required')
            integer(s.object_mass,'output mass',1,min(input_mass,b.origin.mass))
            if b.origin.kind=='object':
                require(b.origin.value is not None,'Original documented value required')
                integer(s.object_value,'output value',0,b.origin.value)
            else:require(s.object_value==0,'Creature body has no independent recoverable/sale value')
        if not creature:
            require(spell_id=='true-polymorph' and (active_transformed_object or s.object_input_eligible),
                    'Fresh outside objects require eligibility; an active True object record uses legal replacement')
        if b.origin.kind=='object' and s.profile is not None:
            sponsor=caster if ends_own_concentration else b.slot_sponsor or caster
            occupant=self.slots.get(sponsor)
            occupied_link=self.current(occupant) if occupant is not None else None
            freed_by_commit=bool(occupied_link and occupied_link.state=='shaping' and self.casts[occupied_link.cast_id].caster==caster)
            require(occupant in (None,b.identity) or freed_by_commit,'Original caster object-creature slot occupied')
        return b

    def cast(self,cast_id,spell_id,stats,price,wallet,selections,now,regular_index,*,legal,resolve_save,countered=False):
        """resolve_save(target, DC) executes only AFTER committed payment.

        It returns True on success (or an exact legendary defense); False on
        failure. Caller must provide a nonthrowing authoritative resolver. All
        actual die rolls/target condition legality remain in the combat engine.
        """
        identity(cast_id);integer(now,'cast timestamp',0);integer(regular_index,'original regular index',0)
        require(legal and spell_id in SPELLS and price.spell_id==spell_id and price.rank==SPELLS[spell_id],'Legal canonical quote/access required')
        require(cast_id not in self.casts and cast_id not in self.buffers.form_instances,'Cast identity already used')
        require(len(selections)==1 or spell_id=='mass-polymorph','Single-target spell')
        if spell_id=='mass-polymorph':validate_mass_space(selections)
        else:require(len(selections)==1,'Exactly one target required')
        for s in selections:
            self._validate_selection(spell_id,price.rank,s,stats.owner)
            require(cast_id+':'+s.target not in self.buffers.form_instances,'World form/link identity already used')
        wallet.validate(rp=price.total,action='action')
        # All potentially invalid requests rejected above. No refunds below.
        wallet.pay(rp=price.total,action='action')
        record=Cast(cast_id,spell_id,stats.owner,price.rank,stats,regular_index)
        self.casts[cast_id]=record;self.buffers.form_instances.add(cast_id)
        self.concentration.start_committed(stats.owner,cast_id,lambda reason:self._end_cast(cast_id,reason))
        if countered:
            record.state='countered';self.concentration.detach(stats.owner,cast_id)
            return {'castId':cast_id,'links':[],'paidRP':price.total,'countered':True,'cadenceQuote':deepcopy(price.quote)}
        successful=[]
        for s in selections:
            body=self.bodies[s.target]
            # Object anatomy never strips a retained creature-origin person's
            # save. Object-origin creature targets retain normal current-form saves.
            needs_save=(self._current_creature(body) or body.origin.kind=='creature') and not s.willing
            if not needs_save or not resolve_save(s.target,stats.dc):successful.append(s)
        # Choices are fixed before rolling; no sequential geometry re-evaluation.
        for s in successful:self._apply(record,s,now)
        record.state='active' if record.links else 'no-target-links'
        if not record.links:self.concentration.detach(stats.owner,cast_id)
        return {'castId':cast_id,'links':list(record.links),'paidRP':price.total,'countered':False,'cadenceQuote':deepcopy(price.quote)}

    def _apply(self,record,s,now):
        b=self.bodies[s.target]
        old=self.current(s.target)
        if old:self._end_link(old,'replaced',continuous=True)
        druid=self.druids.get(s.target)
        if druid and druid.current:druid._end('spell-transformation')
        link_id=record.identity+':'+s.target
        link=Link(link_id,record.identity,s.target,s.profile,s.willing,now+60,
                  object_template=s.object_template,object_size=s.object_size,object_mass=s.object_mass)
        self.links[link_id]=link;record.links.append(link_id);self.buffers.form_instances.add(link_id)
        b.anatomy=link_id
        self.buffers.spell_anatomies[b.identity]=link_id
        b.placement_pending=False;b.placement_conflict=False
        # Close-and-recapture: old record restores still-existing meld items,
        # then this new record captures them without an intervening action window.
        b.melded.update(b.equipment);b.equipment.clear()
        b.size=PROFILES[s.profile]['size'] if s.profile else s.object_size
        if s.profile is None:b.mass=s.object_mass
        if b.origin.kind=='object' and s.profile:
            if b.slot_sponsor is None:b.slot_sponsor=record.caster;b.controller=record.caster
            self.slots[b.slot_sponsor]=b.identity
        elif b.slot_sponsor:self._release_slot(b)

    def _release_slot(self,b):
        if b.slot_sponsor and self.slots.get(b.slot_sponsor)==b.identity:del self.slots[b.slot_sponsor]
        b.slot_sponsor=None

    def _end_link(self,link,reason,*,continuous=False):
        if link.state not in ('shaping','permanent'):return
        b=self.bodies[link.target];record=self.casts[link.cast_id]
        link.state=reason
        if b.anatomy==link.identity:b.anatomy=None
        if self.buffers.spell_anatomies.get(b.identity)==link.identity:
            del self.buffers.spell_anatomies[b.identity]
        self.buffers.end_dependency(link.identity)
        b.equipment.update(b.melded-b.lost_items);b.melded.clear()
        b.size=b.origin.size;b.mass=b.origin.mass
        if not continuous:self._release_slot(b)
        if not continuous:
            b.placement_pending=True
            self.events.append({'target':b.identity,'reason':reason,'sameSpatialAnchor':True,
                                'placementCheckRequired':True,'noHealingOrAutomaticMovement':True})
        if not any(self.links[i].state=='shaping' for i in record.links):
            self.concentration.detach(record.caster,record.identity)

    def _end_cast(self,cast_id,reason):
        record=self.casts[cast_id]
        for ident in record.links:
            link=self.links[ident]
            if link.state=='shaping':self._end_link(link,reason)
        record.state=reason

    def _active(self,target,now,*,allow_boundary=False,allow_suppressed=False):
        link=self.current(target)
        require(link is not None and link.state in ('shaping','permanent'),'No operative spell anatomy')
        require(allow_suppressed or not link.suppressed,'Anatomy is currently suppressed')
        if link.state=='shaping':
            require(now<=link.deadline if allow_boundary else now<link.deadline,'Resolve actual60-second checkpoint first')
        return link

    def repeat_save(self,target,stats,now,*,trigger,event_or_turn,round_number=None,normal_hp_damage=0,success):
        link=self._active(target,now,allow_boundary=True,allow_suppressed=True);record=self.casts[link.cast_id]
        require(link.state=='shaping' and not link.willing and link.profile is not None,'No hostile repeat-save permission')
        require(stats.owner==record.caster,'Original caster statistics required')
        identity(event_or_turn)
        if trigger=='regular-end':
            key=(target,event_or_turn)
            require(key not in self.regular_ends,'Original regular endpoint already handled')
            self.regular_ends.add(key)
        elif trigger=='damage':
            integer(normal_hp_damage,'actual normal HP damage',1);integer(round_number,'numbered round',1)
            key=(target,round_number)
            require(key not in self.damage_rounds,'First positive HP damage repeat already used this round')
            require((target,event_or_turn) not in self.damage_events,'Damage event already processed')
            self.damage_rounds.add(key)
            self.damage_events.add((target,event_or_turn))
        else:raise SpellRuleError('Only actual original regular end or first positive normal-HP damage')
        dc=record.stats.dc if record.spell_id=='true-polymorph' else stats.dc
        if success:self._end_link(link,'repeat-save')
        return {'dc':dc,'ended':bool(success),'target':target}

    def checkpoint(self,now,*,started_packets_and_due_saves_finished):
        integer(now,'absolute checkpoint',0)
        require(started_packets_and_due_saves_finished,'Finish packets and due repeat saves before checkpoint')
        result=[]
        for link in self.links.values():
            if link.state!='shaping' or now<link.deadline:continue
            record=self.casts[link.cast_id]
            if record.spell_id=='true-polymorph':
                link.state='permanent';self.concentration.detach(record.caster,record.identity)
                result.append({'link':link.identity,'state':'permanent'})
            else:
                self._end_link(link,'expired');result.append({'link':link.identity,'state':'expired'})
        return result

    def reject(self,target,now,wallet,*,actual_regular_turn,legal):
        link=self._active(target,now,allow_suppressed=True);record=self.casts[link.cast_id];b=self.bodies[target]
        action_capable=(not link.suppressed and link.profile is not None) or (link.suppressed and b.origin.kind=='creature')
        require(link.state=='shaping' and link.willing and b.origin.kind=='creature' and action_capable and legal and actual_regular_turn,
                'Only a willing temporary creature-origin recipient with expressed action-capable anatomy may reject')
        require(record.spell_id!='shapechange','Shapechange uses ordinary concentration release')
        wallet.validate(action='action');wallet.pay(action='action');self._end_link(link,'willing-rejection')

    def finalize_damage_state(self,target,*,actual_hp,incapacitated,dead,destroyed=False,unsupported=False):
        """After Core damage and ALL same-packet replacement/prevention. No reroll."""
        integer(actual_hp,'actual final HP',0);b=self.bodies[target];link=self.current(target)
        recorded_hp=b.life.get('hp') if isinstance(b.life,dict) else b.life.hp
        require(recorded_hp==actual_hp,'Project the actual finalized canonical HP ledger before anatomy cleanup')
        if b.origin.kind=='object' and actual_hp==0:
            b.destroyed=True
            if link:self._end_link(link,'physical-destruction')
        elif destroyed:
            b.destroyed=True
            if link and link.state=='shaping':self._end_link(link,'physical-destruction')
        elif link and link.state=='shaping' and (actual_hp==0 or incapacitated or dead):self._end_link(link,'forced-reversion')
        return {'sameHPLedger':b.life,'beginOrdinaryFall':bool(unsupported),'secondDamageResolution':False}

    def check_reversion_placement(self,target,*,fits_at_current_anchor):
        b=self.bodies[target]
        require(b.placement_pending,'No pending root-anatomy placement check')
        b.placement_pending=False;b.placement_conflict=not fits_at_current_anchor
        return {'placementConflict':b.placement_conflict,'sameSpatialAnchor':True,
                'requiresCanonicalGeometryResolution':b.placement_conflict,'automaticDamage':0,'automaticRelocation':False}

    def clear_geometry_conflict(self,target,*,canonical_resolution_completed):
        require(canonical_resolution_completed,'Actual canonical geometry resolution required')
        self.bodies[target].placement_pending=False;self.bodies[target].placement_conflict=False

    def dispel(self,target,*,legal):
        require(legal and self.current(target) is not None,'Actual successful dispel required')
        self._end_link(self.current(target),'dispelled')

    def set_suppressed(self,target,now,*,suppressed,legal):
        link=self._active(target,now,allow_suppressed=True);b=self.bodies[target]
        require(legal and link.suppressed!=suppressed,'Actual changed antimagic state required')
        link.suppressed=bool(suppressed)
        b.size=b.origin.size if suppressed else PROFILES[link.profile]['size'] if link.profile else link.object_size
        b.mass=b.origin.mass if suppressed or link.profile else link.object_mass
        # No gear recapture, slot release, benefit entry, HP change or clock reset.
        b.placement_pending=True
        return {'sameRecord':link.identity,'deadline':link.deadline,'placementCheckRequired':True,
                'sameMeldSet':frozenset(b.melded),'slotSponsor':b.slot_sponsor}

    def _stats_for(self,link,stats):
        record=self.casts[link.cast_id]
        require(isinstance(stats,CastStats) and stats.owner==record.caster,'Use original caster statistics')
        return record.stats if record.spell_id=='true-polymorph' else stats

    def profile(self,target,stats,now,form_normal_ac,*,ac_components_certified):
        link=self._active(target,now);b=self.bodies[target]
        require(not b.placement_pending and not b.placement_conflict,'Resolve physical placement before movement/targeting')
        integer(form_normal_ac,'operative form normal AC',0)
        require(ac_components_certified,'Exclude melded armor/shield; certify compatible passives/external equipment')
        types=sorted(b.origin.type_tags) if b.origin.kind=='creature' else ['transformed-object']
        if link.profile is None:
            return {'ac':12,'size':link.object_size,'movement':{},'speech':False,'hands':False,
                    'ordinarySenses':False,'actions':False,'bonusActions':False,'reactions':False,
                    'actionlessObjectAnatomy':True,'appliesIncapacitated':False,'targetKind':'object',
                    'originTypeTags':types,'grantedResistances':[],'sameHPLedger':b.life}
        p=deepcopy(PROFILES[link.profile]);mode=p['ac']['mode'];amount=p['ac']['amount']
        p['ac']=form_normal_ac if mode=='normal' else max(form_normal_ac,amount) if mode=='floor' else amount
        provider=self._stats_for(link,stats)
        p['attack'].update({'attack':provider.attack,'modifier':provider.modifier,'reachFeet':5,
                            'attacker':target,'statProvider':provider.owner,'spellcast':False,
                            'directCasterSpellDamage':False,'sourceSpell':self.casts[link.cast_id].spell_id,
                            'sourceLink':link.identity})
        p.update({'targetKind':'creature','typeTags':types,'sameHPLedger':b.life,'ordinarySenses':True,
                  'grantsSpecialSenses':False,'grantsResources':False,'grantsMultiattack':False})
        if b.origin.kind=='object':p.update({'saves':provider.pb,'ordinaryChecks':0,'soul':False,
            'wounds':False,'deathSaves':False,'resurrection':False,'ordinaryHealing':False,
            'companionPhase':'attached','uncommanded':['move','Dodge']})
        return p

    def healing_target_eligible(self,target,*,native_eligible):
        b=self.bodies[target]
        return bool(native_eligible and not b.destroyed and b.origin.kind=='creature' and self._current_creature(b))

    def acquire_external_gear(self,target,item_id,now,*,compatible_and_equipped):
        link=self._active(target,now);b=self.bodies[target];identity(item_id)
        require(link.profile is not None and PROFILES[link.profile]['hands'] and compatible_and_equipped,
                'Actual compatible external equipment required')
        require(item_id not in b.melded and item_id not in b.equipment and item_id not in b.lost_items,'Item identity unavailable/already recorded')
        b.equipment.add(item_id)

    def mark_item_lost(self,target,item_id,*,actual_loss):
        require(actual_loss,'Actual destroyed/consumed/lost item event required')
        b=self.bodies[target];require(item_id in b.melded or item_id in b.equipment,'Unknown held/melded item')
        b.equipment.discard(item_id);b.melded.discard(item_id);b.lost_items.add(item_id)

    def switch_shapechange(self,target,profile,now,regular_index,wallet,*,original_regular_turn,legal,retained_gear,drop_placement_legal,unsupported=False):
        link=self._active(target,now);record=self.casts[link.cast_id];b=self.bodies[target]
        require(record.spell_id=='shapechange' and record.caster==target,'Only actual self Shapechange may switch')
        require(original_regular_turn and regular_index>record.casting_regular_index and regular_index!=link.last_switch,
                'Switch once on a later original regular turn only')
        require(profile in PROFILES and profile!=link.profile and legal,'Different legal finite profile required')
        require(b.origin.kind!='object' or profile!='spellform.humanoid','Object-origin humanoid prohibited')
        keep=set(retained_gear)
        require(keep<=b.equipment and (not keep or PROFILES[profile]['hands']),'Only certified anatomy-compatible external gear may remain')
        dropped=b.equipment-keep
        require(not dropped or drop_placement_legal,'Resolve legal current/nearest adjacent item placement before switch')
        wallet.validate(action='bonus');wallet.pay(action='bonus')
        b.equipment=keep;link.profile=profile;link.last_switch=regular_index;b.size=PROFILES[profile]['size']
        return {'sameRecord':link.identity,'droppedItemIds':sorted(dropped),'spellcast':False,'paidRP':0,
                'refrainEvent':False,'beginOrdinaryFall':bool(unsupported and not PROFILES[profile]['movement'].get('fly'))}

    def attack(self,target,stats,now,wallet,*,legal):
        link=self._active(target,now);b=self.bodies[target]
        require(legal and b.origin.kind=='creature' and link.profile is not None,'Legal subject natural attack required; object companions use command adapter')
        require(not b.placement_pending and not b.placement_conflict,'Unresolved placement cannot authorize targeting')
        provider=self._stats_for(link,stats)
        wallet.validate(action='action');wallet.pay(action='action')
        return self._attack_packet(link,provider)

    def _attack_packet(self,link,provider):
        attack=deepcopy(PROFILES[link.profile]['attack'])
        attack.update({'reachFeet':5,'attacker':link.target,'statProvider':provider.owner,'attack':provider.attack,
                       'modifier':provider.modifier,'sourceSpell':self.casts[link.cast_id].spell_id,
                       'sourceLink':link.identity,'spellcast':False,'directCasterSpellDamage':False,
                       'importsMultiattack':False,'weaponOnlyFeaturesAuthorized':False})
        return attack

    def command(self,target,order_id,now,round_number,ledger,wallet,*,mode,legal,distance,owner_perceives):
        link=self._active(target,now);b=self.bodies[target];identity(order_id)
        require(b.origin.kind=='object' and link.profile is not None and b.slot_sponsor is not None,'Active object-origin creature required')
        require(isinstance(ledger,CommandLedger) and ledger.owner==b.controller,'Current controller canonical shared command ledger required')
        require(not b.placement_pending and not b.placement_conflict,'Resolve placement before issuing a command')
        require(legal and owner_perceives and 0<=distance<=60,'Actual60-foot command legality required')
        require(mode in ('support','attack','control') and order_id not in self.commands,'Fresh supported command required')
        ledger.activate(round_number,mode,wallet)
        self.commands[order_id]={'target':target,'link':link.identity,'controller':b.controller,'mode':mode,'resolved':False}
        return {'orderId':order_id,'phase':'attached','independentTurn':False}

    def resolve_command(self,order_id,stats,now,*,attached_phase,still_legal):
        order=self.commands.get(order_id)
        require(order is not None and not order['resolved'] and attached_phase,'Actual unresolved attached command required')
        b=self.bodies[order['target']];link=self.current(b.identity)
        order['resolved']=True
        if (not still_legal or not link or link.identity!=order['link'] or link.suppressed
            or b.controller!=order['controller'] or b.destroyed or b.placement_pending or b.placement_conflict
            or (link.state=='shaping' and now>=link.deadline)):
            return {'executed':False,'refunded':False}
        self._active(b.identity,now)
        if order['mode']=='attack':return {'executed':True,'attack':self._attack_packet(link,self._stats_for(link,stats))}
        return {'executed':True,'mode':order['mode'],'damageAuthorized':False,'profileGrantsNoExtraControlPower':True}

    def uncommanded(self,target,now):
        link=self._active(target,now);b=self.bodies[target]
        require(b.origin.kind=='object' and link.profile is not None,'Actual object companion required')
        return {'options':['move','Dodge'],'damageAuthorized':False,'independentTurn':False}

```

## tools/temporal_playtest_rules.py
Source SHA-256 `e54059bd9f9dfc187ff5d6695365bed9ab8fe96583ade3dbd3d4af1cfcba1661`

```
class PhysicalRecord:
    identity: str
    kind: str  # inventory, temporal-entity, root
    owner: str | None
    roots: tuple = ()
    created_iteration: int = -1
    survives: bool = True
    source_owner: str | None = None
    external_binding: str | None = None
    persistent_enrollment: str | None = None

class Inventory:
    physical: dict = field(default_factory=dict)
    # Quantity/stock/history never restore. Each discrete transferable item also
    # has a PhysicalRecord so derivatives cannot hide behind a stack quantity.
    quantities: dict = field(default_factory=dict)
    expenditure_events: set = field(default_factory=set)

class Pose:
    anchor: tuple
    offsets: frozenset = frozenset({(0, 0)})

    def cells(self):
        require(len(self.anchor) == 2 and all(type(x) is int for x in self.anchor), '2D integer anchor required')
        require(bool(self.offsets) and (0, 0) in self.offsets, 'Nonempty anchor footprint required')
        require(all(len(v) == 2 and all(type(n) is int for n in v) for v in self.offsets),
                'Explicit integer footprint offsets required')
        return frozenset((self.anchor[0] + x, self.anchor[1] + y) for x, y in self.offsets)

class EnvironmentAnchor:
    identity: str
    blocked: frozenset = frozenset()
    support: frozenset = frozenset()

class Geometry:
    cells: frozenset
    fixed_support: frozenset
    poses: dict = field(default_factory=dict)
    anchors: dict = field(default_factory=dict)
    # This bounded adapter supports a finite orthogonal level ground plane.
    # Flying/elevation/portals/forced growth require additional reviewed adapters.
    movement_model: str = 'finite-level-ground'

def _physical_plan(self, snap):
        rows = self.inventory.physical
        require(all(k == v.identity for k, v in rows.items()), 'Physical identity mismatch')
        require(snap.physical_ids <= rows.keys(), 'Physical history/identity was removed')
        for key, before in snap.physical_baseline.items():
            current = rows[key]
            require((before.kind, before.roots, before.source_owner) ==
                    (current.kind, current.roots, current.source_owner),
                    'Immutable physical provenance changed or reused an identity')
        for actor in snap.roster | snap.environment:
            before, current = snap.physical_baseline[actor], rows[actor]
            require(before.survives, 'Snapshot physical body must actually exist')
            require((before.owner, before.external_binding, before.persistent_enrollment) ==
                    (current.owner, current.external_binding, current.persistent_enrollment),
                    'Participant body ownership/enrollment changed; source adapter required')
        roots_in_scope = set(snap.roster | snap.environment)
        retire = set()

        def roots(identity, seen):
            require(identity not in seen, 'Physical provenance cycle')
            require(identity in rows, 'Missing provenance root: ' + identity)
            row = rows[identity]
            shape(row, PhysicalRecord)
            if not row.roots:
                return {identity}
            result = set()
            for parent in row.roots:
                result |= roots(parent, seen | {identity})
            return result

        for identity, row in rows.items():
            rootset = roots(identity, set())
            if not row.survives or identity in snap.physical_ids or not rootset & roots_in_scope:
                continue
            require(row.kind == 'temporal-entity', 'Surviving transferable derivative blocks restoration')
            require(rootset <= roots_in_scope, 'Mixed physical roots require a source adapter')
            require(row.source_owner in snap.roster, 'Derivative source outside temporal closure')
            require(row.external_binding is None and row.persistent_enrollment is None,
                    'Cannot rewrite an external source slot or persistent enrollment')
            retire.add(identity)
        return retire

def _space(geometry, anchors):
        blocked = frozenset().union(*(a.blocked for a in anchors.values()))
        support = geometry.fixed_support | frozenset().union(*(a.support for a in anchors.values()))
        require(blocked <= geometry.cells and support <= geometry.cells, 'Environment outside finite boundary')
        return blocked, support

def _reachable(geometry, pose, blocked, support):
        def legal(anchor):
            cells = replace(pose, anchor=anchor).cells()
            return cells <= geometry.cells and cells <= support and not cells & blocked
        require(legal(pose.anchor), 'Body cannot occupy its current/restored footprint')
        visited, todo = {pose.anchor}, [pose.anchor]
        while todo:
            x, y = todo.pop()
            for p in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if p not in visited and legal(p):
                    visited.add(p)
                    todo.append(p)
        return visited

def _geometry_plan(self, snap, retire):
        g = self.geometry
        poses = {k: data(v) for k, v in g.poses.items() if k not in retire}
        poses.update(data(snap.poses))
        anchors = {k: data(v) for k, v in g.anchors.items() if k not in retire}
        anchors.update(data(snap.anchors))
        before_blocked, before_support = self._space(g, g.anchors)
        blocked, support = self._space(g, anchors)
        occupied = set()
        for actor, pose in poses.items():
            cells = pose.cells()
            require(cells <= g.cells and cells <= support and not cells & blocked,
                    'Illegal restored footprint or lost support')
            require(not cells & occupied, 'Atomic restored footprints overlap')
            occupied |= cells
            if actor not in snap.roster:
                # Conservative: retain every ground location previously reachable
                # by the outsider, so an environment restore cannot trap/enclose it.
                before = self._reachable(g, pose, before_blocked, before_support)
                after = self._reachable(g, pose, blocked, support)
                require(before <= after, 'Environment restoration restricts a protected outsider')
        return poses, anchors
```

## data/playtest/druid_form_profiles.json
Source SHA-256 `6be62be56c63f96d5657597f98cf62cc68c087ba17626c8a6ce4648386403783`

```
{
  "druid.base.wolf-form-striker": {
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
    "size": "Medium",
    "mayLarge": false,
    "movement": {
      "walk": 40
    },
    "entryBuffer": 0
  },
  "druid.base.bear-form-tank": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 20
  },
  "druid.base.hawk-form-scout": {
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
    "size": "Tiny",
    "mayLarge": false,
    "movement": {
      "walk": 10,
      "fly": 60
    },
    "entryBuffer": 0
  },
  "druid.base.boar-form-brawler": {
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
    "size": "Medium",
    "mayLarge": false,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.base.panther-form-stealth": {
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
    "size": "Medium",
    "mayLarge": false,
    "movement": {
      "walk": 40
    },
    "entryBuffer": 0
  },
  "druid.arch.dire-wolf": {
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
    "size": "Medium",
    "mayLarge": false,
    "movement": {
      "walk": 40
    },
    "entryBuffer": 0
  },
  "druid.arch.earth-warden-dire-bear": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 30
  },
  "druid.arch.sky-serpent": {
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
    "size": "Medium",
    "mayLarge": false,
    "movement": {
      "walk": 30,
      "fly": 80
    },
    "entryBuffer": 0
  },
  "druid.arch.ironhorn-ram": {
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
    "size": "Medium",
    "mayLarge": false,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.arch.shadow-lynx": {
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
    "size": "Medium",
    "mayLarge": false,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.land.blight-elk": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.land.tanglemaw": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.moon.beastlord-alpha-animal-hybrid": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.moon.mooncursed": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.moon.elemental-shapeshifting": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.storm.tempest-raptor": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30,
      "fly": 60
    },
    "entryBuffer": 0
  },
  "druid.hero.storm.thunderhorn-stag": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.thorns.blight-elk": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.thorns.tanglemaw": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.winterfang.snow-leopard": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.winterfang.frost-wyrmling": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.rotshaper.carrion-rat-king": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.rotshaper.insect-broodmother": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30,
      "climb": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.rotshaper.master-of-vermin": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.ashen-grove.charbear": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  },
  "druid.hero.ashen-grove.blazewood-stag": {
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
    "size": "Medium",
    "mayLarge": true,
    "movement": {
      "walk": 30
    },
    "entryBuffer": 0
  }
}
```

## data/playtest/spell_form_profiles.json
Source SHA-256 `6bf641487b429201e7d0d01c725acb1c975949d902687c6cdf3be9d13e25b3d3`

```
{
  "status": "REVIEWED / reference-VALIDATED:12 bounded spell-form profiles",
  "profiles": [
    {
      "id": "spellform.humanoid",
      "tier": "R4",
      "size": "Medium",
      "movement": {
        "walk": 30
      },
      "speech": true,
      "hands": true,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "dice": "1d6",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.humanoid",
        "tier": "R4",
        "size": "Medium",
        "movement": "walk 30",
        "speechHands": "yes / yes",
        "ac": "formNormalAC",
        "naturalAttack": "1d6+M bludgeoning",
        "passiveAnatomy": "none"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.predator",
      "tier": "R4",
      "size": "Medium",
      "movement": {
        "walk": 40
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 13
      },
      "attack": {
        "dice": "1d8",
        "damageType": "slashing",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.predator",
        "tier": "R4",
        "size": "Medium",
        "movement": "walk 40",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,13)",
        "naturalAttack": "1d8+M slashing",
        "passiveAnatomy": "none"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.brute",
      "tier": "R4",
      "size": "Large",
      "movement": {
        "walk": 30
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 15
      },
      "attack": {
        "dice": "2d6",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.brute",
        "tier": "R4",
        "size": "Large",
        "movement": "walk 30",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,15)",
        "naturalAttack": "2d6+M bludgeoning",
        "passiveAnatomy": "none"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.avian",
      "tier": "R4",
      "size": "Small",
      "movement": {
        "walk": 10,
        "fly": 50
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 13
      },
      "attack": {
        "dice": "1d6",
        "damageType": "slashing",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.avian",
        "tier": "R4",
        "size": "Small",
        "movement": "walk 10, fly 50",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,13)",
        "naturalAttack": "1d6+M slashing",
        "passiveAnatomy": "flight"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.aquatic",
      "tier": "R4",
      "size": "Medium",
      "movement": {
        "walk": 20,
        "swim": 50
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 14
      },
      "attack": {
        "dice": "1d8",
        "damageType": "piercing",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": true,
      "sourceProposal": {
        "id": "spellform.aquatic",
        "tier": "R4",
        "size": "Medium",
        "movement": "walk 20, swim 50",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,14)",
        "naturalAttack": "1d8+M piercing",
        "passiveAnatomy": "water breathing"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.burrower",
      "tier": "R4",
      "size": "Medium",
      "movement": {
        "walk": 30,
        "burrowLooseSoil": 15
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 14
      },
      "attack": {
        "dice": "1d8",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.burrower",
        "tier": "R4",
        "size": "Medium",
        "movement": "walk 30, burrow 15 through loose soil",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,14)",
        "naturalAttack": "1d8+M bludgeoning",
        "passiveAnatomy": "loose-soil burrow"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.greater-brute",
      "tier": "R9",
      "size": "Large",
      "movement": {
        "walk": 40
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 17
      },
      "attack": {
        "dice": "2d8",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.greater-brute",
        "tier": "R9",
        "size": "Large",
        "movement": "walk 40",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,17)",
        "naturalAttack": "2d8+M bludgeoning",
        "passiveAnatomy": "none"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.greater-winged",
      "tier": "R9",
      "size": "Large",
      "movement": {
        "walk": 20,
        "fly": 60
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 16
      },
      "attack": {
        "dice": "2d8",
        "damageType": "slashing",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.greater-winged",
        "tier": "R9",
        "size": "Large",
        "movement": "walk 20, fly 60",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,16)",
        "naturalAttack": "2d8+M slashing",
        "passiveAnatomy": "flight"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.elemental-air",
      "tier": "R9",
      "size": "Medium",
      "movement": {
        "fly": 60,
        "hover": true
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "fixed",
        "amount": 16
      },
      "attack": {
        "dice": "2d8",
        "damageType": "lightning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [
        "lightning"
      ],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.elemental-air",
        "tier": "R9",
        "size": "Medium",
        "movement": "fly 60, hover",
        "speechHands": "no / no",
        "ac": "16",
        "naturalAttack": "2d8+M lightning",
        "passiveAnatomy": "lightning resistance"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.elemental-earth",
      "tier": "R9",
      "size": "Large",
      "movement": {
        "walk": 30,
        "burrowLooseSoil": 20
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "fixed",
        "amount": 17
      },
      "attack": {
        "dice": "2d8",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.elemental-earth",
        "tier": "R9",
        "size": "Large",
        "movement": "walk 30, burrow 20 loose soil",
        "speechHands": "no / no",
        "ac": "17",
        "naturalAttack": "2d8+M bludgeoning",
        "passiveAnatomy": "loose-soil burrow"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.elemental-fire",
      "tier": "R9",
      "size": "Medium",
      "movement": {
        "walk": 40
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "fixed",
        "amount": 16
      },
      "attack": {
        "dice": "2d8",
        "damageType": "fire",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [
        "fire"
      ],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.elemental-fire",
        "tier": "R9",
        "size": "Medium",
        "movement": "walk 40",
        "speechHands": "no / no",
        "ac": "16",
        "naturalAttack": "2d8+M fire",
        "passiveAnatomy": "fire resistance"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.elemental-water",
      "tier": "R9",
      "size": "Medium",
      "movement": {
        "walk": 20,
        "swim": 60
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "fixed",
        "amount": 16
      },
      "attack": {
        "dice": "2d8",
        "damageType": "cold",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [
        "cold"
      ],
      "waterBreathing": true,
      "sourceProposal": {
        "id": "spellform.elemental-water",
        "tier": "R9",
        "size": "Medium",
        "movement": "walk 20, swim 60",
        "speechHands": "no / no",
        "ac": "16",
        "naturalAttack": "2d8+M cold",
        "passiveAnatomy": "cold resistance, water breathing"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    }
  ],
  "evidence": [
    {
      "path": "GPT_TRANSFORMATION_SPELL_FIRST_REVIEW.md",
      "sha256": "2d70c89fc53db4e4498c1c0e4a603bfe57e7b02e3d0583330899fd63d7e5009d"
    },
    {
      "path": "GPT_TRANSFORMATION_SPELL_BOUNDARIES.md",
      "sha256": "83e76eb5f04e2b02a0948f95d0d9e72db19d522c0372520cedf01b0b733b927d"
    },
    {
      "path": "GPT_TRANSFORMATION_SPELL_FINAL_INTERFACES.md",
      "sha256": "192f5eadabd7f0f502ea5d831016a17e3eeb22860bf8e4ddb847e38cce91935d"
    }
  ],
  "reviewClosure": "docs/audit/2026-10-08/full-game/GPT_TRANSFORMATION_SPELL_FINAL_CLOSURE.md"
}

```

## data/playtest/class_sources/druid.json
Source SHA-256 `640be091224033cf6d820c2505cfac52fb4d1587644256c48ac587cb645851b4`

```
{
  "sourcePath": "docs/reference/Player_Rulebook_v6_source_text.txt",
  "sourceSha256": "a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b",
  "qualification": "Preserved historical source; already reviewed provisional form overlay controls conflicts. Do not re-import monster-stat replacement.",
  "bookLines": [
    {
      "line": 2433,
      "text": "Shapeshifting"
    },
    {
      "line": 2434,
      "text": "At 1st level, you gain the ability to transform into various animal forms. Shapeshifting is Aethel's native druidic transformation discipline and functions according to the following rules:"
    },
    {
      "line": 2435,
      "text": ""
    },
    {
      "line": 2436,
      "text": "Activation and Duration"
    },
    {
      "line": 2437,
      "text": "You can use a bonus action to assume a beast form. You can remain in beast form for 10 minutes per use. You then revert to your normal form unless you expend another use of this feature. You can revert to your normal form earlier by using a bonus action on your turn."
    },
    {
      "line": 2438,
      "text": ""
    },
    {
      "line": 2439,
      "text": "Uses per Day"
    },
    {
      "line": 2440,
      "text": "At 1st level, you can use your Shapeshifting ability twice per long rest. You gain additional uses as you reach higher levels, as shown in the Shapeshifting Uses column of the Druid table."
    },
    {
      "line": 2441,
      "text": ""
    },
    {
      "line": 2442,
      "text": "Available Forms"
    },
    {
      "line": 2443,
      "text": "At 1st level, you can transform into any of the Base Druid Forms listed below. At 11th level, you gain access to Arch Druid Forms. At 10th level, you gain access to Hero Druid Forms specific to your chosen Circle."
    },
    {
      "line": 2444,
      "text": "Limitations While Transformed"
    },
    {
      "line": 2445,
      "text": "While in beast form:"
    },
    {
      "line": 2446,
      "text": "You cannot cast spells unless specified by your Hero Class"
    },
    {
      "line": 2447,
      "text": "Your ability to speak is limited (only preserved in arch/hero forms)"
    },
    {
      "line": 2448,
      "text": "You retain your mental ability scores (Intelligence, Wisdom, and Charisma)"
    }
  ]
}
```
