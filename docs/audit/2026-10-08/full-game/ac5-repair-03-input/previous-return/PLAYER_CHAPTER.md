# Rank-5 Abjuration / Conjuration — Current Provisional Player Procedures

## Status and authority
These sixteen procedures are a **NEW provisional authored-playtest candidate** for the complete requested rank-5 Abjuration/Conjuration cohort. Printed source/access records remain preserved in `SPELLS_MODEL.json`. Older shared proposals are historical evidence only.

This chapter does **not** choose a campaign era, equate unresolved planes, infer soul/native origin from creature type, alter accepted AC4, or alter accepted ordinary Banishment.

## Shared price order — AC5-PRICE-01
For an actual spell cast: validate source access and legal caster; calculate its ordinary RP-priced component and exact class/source reductions or waivers; then apply at most one operative **Resonance Nexus −2** to the remaining discountable RP component, minimum 0; then apply accepted **Resonance Dampening Field +2 RP** if applicable; then apply one final Resonance Influence Ease/Burden, minimum 0. Protected X/principal, HP, materials, ammunition, charges, uses and nonspell-resource costs remain separate unless their exact source says otherwise.

Nexus never creates an RP price for a charge/use-only spell. Dampening retains its accepted special +2 interface for an actual spell route with no ordinary RP-price interface. Paying RP for a nonspell does not make it a spell.

### Resonance Barrier conversion
For Resonance Barrier only, its creditable base is the actual base amount remaining after exact base reductions/waivers and Nexus. Dampening, Dissonance and Burden are noncreditable. Final Ease is allocated against creditable base first. Protected X is separately paid and creditable. Pool = `5 × (creditableBasePaid + X)`.

## Planar metadata — AC5-PLANAR-META-01
Where a card needs a plane, it uses an opaque stable `planeKey` for an actual campaign/source plane record. A `planeKey` carries no automatic alignment, deity, native species, soul destination, Wheel, dominion or tributary meaning. `lastArrivedFromPlaneKey` and `createdFromPlaneKey` are operational travel/source provenance only. Unknown provenance remains **Indeterminate**.

## AC5 exile bridge
Only **Banish Elemental** and **Elemental Banishment** reuse the accepted ordinary-Banishment generated cell, custody, clocks, independent escape, finite closure, placement/conflict and narrow terminal endpoint-blocker machinery through `AC5-BANISH-EXT-01`. They do not inherit ordinary Banishment's target eligibility, save, rank/access or duration.

## Damage-root checkpoints
Living Magma creates its root when a failed save establishes its recurring rider; all three later ticks descend from that root. Fire Pet attacks and Fire Pet aura recipient checkpoints use the Pet as dealer. Massive Elemental Blast creates a separate root per recipient with the caster as dealer. Resonance Barrier prevention creates no damage root.

## AC5 finite summoned bodies
The authored **Greater Fire Pet** and **Faction Champion** profiles are active creatures and living allies for ordinary HP-healing/living-creature targeting only while their finite bodies exist. This does not establish biology, native plane, soul, corpse, faction personhood or loot. Qualifying Null damage to 0 follows the accepted finite-summon Disabled-0 branch while the original source persists.


# AB5-01 — Antimagic Field (Lesser)

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 5 | 9 | 10 |
| Druid | Abjuration | 5 | 9 | 10 |
| Mage | Abjuration | 5 | 9 | 10 |
| Tinker | Abjuration | 5 | 18 | 10 |
| Wizard | Abjuration | 5 | 9 | 10 |
| Paladin | Abjuration | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** 10-ft sphere suppresses magic effects and spells.
- **Catalog placements:** [{"name": "Antimagic Field (Lesser)", "school": "Abjuration", "level": 5, "summary": "10-ft sphere suppresses magic effects and spells."}]
- **Core:** casting `1 action`, range `10 feet`, duration `Instantaneous`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `10-ft sphere suppresses magic effects and spells.`

## Complete current procedure
Action; range 10 feet; V/S/F; base 10 RP. Preserve the source's 10-foot sphere and suppression promise. NEW: choose one perceived fixed point within 10 feet and line of effect; create a fixed 10-foot-radius sphere with concentration up to 60 elapsed seconds, explicitly replacing the source's insufficient Instantaneous field duration for this authored procedure. The volume is clipped by actual solid total-cover barriers from the center and never follows a creature.

The field suppresses the local expression of actual ongoing spells and explicitly magical nonspell technique expressions only where their real body/effect/anchor intersects the operative volume. It supplies no rank ceiling. It does not retroactively undo completed damage, healing, movement, transmutation, consumed items, permanent ordinary matter, HP loss or source history. It does not erase class engines, learned facts, RP pools, injuries or intrinsic nonmagical traits. A magic item keeps its mundane body/ownership/contents while its magical enhancements/actions are unavailable. A creature-attached spell buff is wholly unavailable while the creature intersects; a large wall/field loses only its intersecting portion unless its own indivisible source says otherwise.

An otherwise legal spell cast may still be committed inside: pay its real final price, Action/components/cadence and concentration transition. If the spell's relevant manifestation originates inside the field, suppress that payload at resolution; there is no queued later release and no refund. Do not invent an imaginary straight-line beam/path for teleportation or nonprojectile magic. For current Dimensional Door, an origin and endpoint both outside the field are unaffected even if a drawn line crosses it; an origin actually inside the field has its spell payload suppressed after legal commitment. A remote ongoing effect outside is not canceled merely because its concentrating caster enters the field.

Ranger Nature's Whisper is an explicitly magical NONSPELL technique. Inside the field its Action+1 RP+Recharge 3 commitment remains a nonspell event; the magical payload/rider is unavailable with no rank, Counterspell window or Nexus/Dampening price. A still-live Nature's Whisper rider on an actor inside the field is unusable while suppressed but its clock continues.

Oracle's Burden prevents generic remove/suspend of the intrinsic Oracle Curse, so this field does not erase or suspend the Curse engine. Curse Manifestation, Tongues and Consumed retain only their own exact suppression/appearance permissions and timers.

Instances of Lesser Antimagic do not suppress one another; overlapping instances form the union of active volumes. This same-family exception only prevents oscillation and grants no ability to cast a new field from inside another without paying/satisfying the new cast, whose payload is itself exempt only because it is this family.

For Greater Fire Pet and Faction Champion use AC5-ANTIMAGIC-SUMMON-01. For accepted ordinary Banishment, only actual suppression of the application itself invokes its own accepted closure/end rule; merely suppressing its distant caster does not reach the generated cell/application. For Banish Elemental and Elemental Banishment, AC5-BANISH-EXT-01 expressly gives the same close-on-actual-suppression behavior.

Suppression never pauses absolute/source clocks and does not bank missed attacks, aura starts, periodic damage, saves or commands. On exit/end, only still-live source expressions resume with the same remaining HP/pools/deadlines. Wall of Force uses its own safe segment-resumption rule.

### Explicit NEW scoped authorship
- Fixed 10-foot radius, concentration 60 seconds
- local expression-based suppression without rank cap
- same-family field exemption
- explicit Nature's Whisper nonspell suppression boundary
- profile-specific AC5 summon suppression
- no global projectile/path assumption

# AB5-02 — Banish Elemental

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 5 | 9 | 10 |
| Druid | Abjuration | 5 | 9 | 10 |
| Mage | Abjuration | 5 | 9 | 10 |
| Tinker | Abjuration | 5 | 18 | 10 |
| Wizard | Abjuration | 5 | 9 | 10 |
| Paladin | Abjuration | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** Instantly banish an elemental or outsider (CHA save negates).
- **Catalog placements:** [{"name": "Banish Elemental", "school": "Abjuration", "level": 5, "summary": "Instantly banish an elemental or outsider (CHA save negates)."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Instantaneous`, components `V, S, F`, RP `10`, resolution `Charisma save`, effect `Instantly banish an elemental or outsider (CHA save negates).`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; source Charisma save/Instantaneous metadata retained. Target one perceived creature within 60 feet and line of effect. It is eligible only if current authoritative creature data explicitly says creatureType=Elemental OR explicitly supplies an `outsider` classification/tag for that body. Summoned, extraplanar, foreign, fiendish-looking or unknown-provenance are not synonyms. If eligibility is hidden/unknown, a legal cast may commit and later fail without revealing which fact failed.

Commit ordinary spell costs/concentration transition/counter window, then make the printed CHA save vs actual spell DC. Success: no exile. Failure: require and spend the existing shared hard-control allowance for this source-character/target/encounter; if unavailable, no exile and no soft fallback.

NEW source completion: successful failure creates a nonconcentration exile application lasting 60 elapsed seconds. The source's Instantaneous metadata is preserved as the cast/resolution metadata; the continuing exile deadline is explicit NEW authorship rather than a source rewrite. Use AC5-BANISH-EXT-01 for the generated BAN-CELL-03 cell, same-identity/custody rules, separate-creature handling, legal independent escape, all real clocks, BAN-CLOSE-03 return, canonical placement/BAN-CONFLICT-04 and the narrow terminal endpoint-blocker exception. This spell does not send the target to a named/native/home plane and learns no origin fact.

If the target's independent finite creature source ends in the cell, the body ends normally; close this application immediately and settle only genuine surviving loose cargo. Actual suppression of this exile application closes/ends it rather than pausing it. Death/corpse/body changes inside retain their real rules.

### Explicit NEW scoped authorship
- Eligibility requires explicit Elemental type OR explicit outsider classification; no synonym inference
- 60-second nonconcentration exile layered over preserved Instantaneous cast metadata
- explicit AC5-BANISH-EXT-01 reuse of accepted Banishment topology/closure only
- shared hard-control gate

# AB5-03 — Greater Dispel

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 5 | 9 | 10 |
| Druid | Abjuration | 5 | 9 | 10 |
| Mage | Abjuration | 5 | 9 | 10 |
| Tinker | Abjuration | 5 | 18 | 10 |
| Wizard | Abjuration | 5 | 9 | 10 |
| Paladin | Abjuration | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** End multiple magical effects in 30-ft radius.
- **Catalog placements:** [{"name": "Greater Dispel", "school": "Abjuration", "level": 5, "summary": "End multiple magical effects in 30-ft radius."}]
- **Core:** casting `1 action`, range `30 feet`, duration `Instantaneous`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `End multiple magical effects in 30-ft radius.`

## Complete current procedure
Action; casting-point range 30 feet; V/S/F; base 10 RP; Instantaneous. Choose one perceived center within 30 feet. At resolution take one immutable snapshot of every ongoing independently addressable magical effect application having an affected body, discrete anchor/object effect, or freestanding area portion inside the 30-foot-radius sphere and center line of effect. Allies are included. Individual effect perception is not required; no numerical cap or selective post-result omission exists.

Eligible ordinary spell applications retain their original generating rank. Rank 0-5 ends automatically. Rank 6-9 requires one check per original generating cast using the caster's actual spellcasting ability + PB against DC 10 + 2×recorded rank. Reuse that one roll for all captured applications from the same generating cast. Apply current Core task degrees/natural shifts. A nonspell magical component is eligible only if its own source explicitly supplies a dispel interface/rank/DC; never assign rank 0 by appearance or RP cost.

Capture is fixed before any endings. If a captured Wall of Force ends and reveals another effect behind it, that effect is not added. A captured indivisible wall/field ends as one effect on successful/automatic dispel; recipient-specific applications from one cast end only where captured unless their real parent dependency says ending one ends all. Suppressed-but-still-existing records can be dispelled if this cast itself can reach them. Completed instantaneous consequences, permanent matter, class engines, permanent item enchantments and explicitly nondispellable effects are outside scope.

This is distinct from Wizard class Dispel Magic `/cards/19`: that class spell costs 3 RP, range 60, Recharge 2, auto through rank 3, and uses INT+PB vs DC 10+rank above 3. Sigil Authority `/cards/22` names Counterspell and Dispel Magic only and does not modify Greater Dispel. Xi remains its own consent-based branch-ending source and grants no Greater Dispel permission.

### Explicit NEW scoped authorship
- Immutable 30-ft area snapshot
- rank0-5 automatic; rank6-9 one shared check per generating cast at DC10+2rank
- nonspell only with explicit dispel interface
- no snapshot expansion
- class Dispel/Sigil Authority kept distinct

# AB5-04 — Spell Resistance

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 5 | 9 | 10 |
| Druid | Abjuration | 5 | 9 | 10 |
| Mage | Abjuration | 5 | 9 | 10 |
| Tinker | Abjuration | 5 | 18 | 10 |
| Wizard | Abjuration | 5 | 9 | 10 |
| Paladin | Abjuration | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** Target gains advantage on saves against spells for 1 hour.
- **Catalog placements:** [{"name": "Spell Resistance", "school": "Abjuration", "level": 5, "summary": "Target gains advantage on saves against spells for 1 hour."}]
- **Core:** casting `1 action`, range `60 feet`, duration `1 hour`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Target gains advantage on saves against spells for 1 hour.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; one willing perceived creature with line of effect; duration 3600 elapsed seconds, no concentration. For the duration, the target has ordinary advantage on every saving throw directly required by an actual spell or that spell's still-dependent ongoing/periodic rider, including a printed repeat/ending save and an item/ancestry cast that is genuinely a spell. Spell provenance, not RP payment or appearance, controls.

No save is invented for an automatic spell. This grants no attack disadvantage, AC, damage resistance, immunity or rank ceiling. It does not apply to Counterspell/Dispel ability checks, generic concentration saves caused by damage, Wound/death saves, mundane aftermath, or nonspell class/monster/item techniques.

Advantage does not stack. A Shaman whose `/cards/41` Spell Resistance already grants advantage still rolls one advantaged save. Thief Arcane Resistance `/cards/21` is a separate +2 to spell saves and can combine with the one advantage. Druid Nature's Ward applies only its printed immunities and does not turn every Elemental/Fey/planar effect into automatic success.

Suppression makes this advantage unavailable while the target/application is suppressed, but its one-hour clock continues; missed saves are not rerolled later. Recasting creates a separate paid application with its own expiry but still only one ordinary advantage at a given save.

### Explicit NEW scoped authorship
- Willing target; nonconcentration hour
- causal spell-origin save boundary
- advantage nonstacking with Shaman; Thief +2 remains separate
- no downstream concentration/Wound/death benefit

# AB5-05 — Wall of Force

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 5 | 9 | 10 |
| Druid | Abjuration | 5 | 9 | 10 |
| Mage | Abjuration | 5 | 9 | 10 |
| Tinker | Abjuration | 5 | 18 | 10 |
| Wizard | Abjuration | 5 | 9 | 10 |
| Paladin | Abjuration | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** Create an invisible, impenetrable wall.
- **Catalog placements:** [{"name": "Wall of Force", "school": "Abjuration", "level": 5, "summary": "Create an invisible, impenetrable wall."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Concentration, up to 1 minute`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Create an invisible, impenetrable wall.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds. Create one fixed invisible flat rectangular plane up to 30 feet long × 15 feet high × 1 inch thick in any chosen orientation. Every part must lie within 60 feet and the intended near surface must be perceivable with line of effect. The wall may meet existing supports but cannot overlap a creature or independent object at creation; hidden occupancy can defeat the paid placement without diagnostic or automatic reshaping.

The wall supports itself and ordinary loads on either side, including horizontal platform use. It has no AC/HP and is impenetrable to ordinary physical bodies, projectiles, liquids, gas and sound. Ordinary light/vision passes through it; it remains visually invisible, though touch or an applicable magical sense can reveal the boundary. It blocks ordinary spell/effect line of effect and other effects requiring a physical path. Its finite edges remain open routes.

Do not infer a teleport path. Accepted Dimensional Door has no traversed path and may move from one legal endpoint to another even if a drawn line would intersect the wall, provided its own endpoint/knowledge rules pass. Resonance Beacon likewise uses its own teleport endpoint, not an imagined wall crossing. Dimensional Anchor remains an independent endpoint blocker. A destination footprint cannot overlap the wall itself.

The wall creates no oxygen deletion or automatic breathable volume. It never pushes/crushes at creation/end. Suppression removes only intersecting wall portions while concentration/deadline continues. On resumption recreate only clear portions; an occupied closing segment remains locally pending until clear, without severing/shoving. Expiry/removal ends support immediately and actual unsupported bodies begin ordinary Falling from their current location, one real Fall Marker.

### Explicit NEW scoped authorship
- Finite 30×15×1in plane
- self-support/platform use
- physical/gas/sound and LoE barrier while transmitting light
- safe local suppression/resumption
- teleports judged by their own endpoints, no invented path

# AB5-06 — Resonance Barrier

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 5 | 9 | 10 |
| Druid | Abjuration | 5 | 9 | 10 |
| Mage | Abjuration | 5 | 9 | 10 |
| Tinker | Abjuration | 5 | 18 | 10 |
| Wizard | Abjuration | 5 | 9 | 10 |
| Paladin | Abjuration | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** Convert Resonance Points into a damage-absorbing shield.
- **Catalog placements:** [{"name": "Resonance Barrier", "school": "Abjuration", "level": 5, "summary": "Convert Resonance Points into a damage-absorbing shield."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Concentration, up to 1 minute`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Convert Resonance Points into a damage-absorbing shield.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds; one willing perceived creature with line of effect. Before commitment choose protected conversion principal X from 0..actual caster PB. X is separately paid RP, cannot be discounted/waived by Nexus, Dampening or Influence, and is not part of ordinary spell pricing.

Price the spell through AC5-PRICE-01. For pool credit, compute `creditableBasePaid`: the actual ordinary base component paid after exact base/source reductions and Nexus; Dissonance, Dampening +2, Burden and other surcharges are noncreditable. If final Ease reduces the RP-priced spell amount, allocate Ease against creditable base first, floor 0, then any remaining reduction against noncreditable components. Protected X is separately creditable. Initial prevention pool = 5 × (creditableBasePaid + X). If this is 0, the fresh application cannot form even if some noncreditable surcharge was paid.

This is pure finite damage prevention, not temp HP, AC, armor, a physical object or maximum HP. For an eligible incoming damage packet, apply ordinary type defenses first, then this pool before post-defense damage transfer and temp HP. Spend only actual prevented points. A transferred branch explicitly skipping another prevention/mitigation stage cannot consume this pool. Prevented points are not actualDamageDealt and cannot trigger drain/heal/reflection/recovery.

Same-name pools never add: compare offered pool to currently retained remaining pool. Stronger replaces; equal/weaker paid offer does not refresh retained expiry/source. Suppression makes remaining pool unavailable without spending/refilling it; clocks continue. Pool ends at 0, concentration loss, expiry, recipient death or eligible removal. No refund/cash-out.

Example current price: base10, Dampening +2, pending Ease -1, X2, no Nexus. RP-priced amount 10+2-1=11; Ease reduces creditable base10→9; then separately pay X2 = total13; pool =5×(9+2)=55. With Nexus, base10→8, +2 Dampening→10, Ease→9, X2 total11; creditable base8→7; pool45.

### Explicit NEW scoped authorship
- Protected X0..PB outside price modifiers
- AC5-PRICE-01 integration
- credit only actually paid base after Nexus and Ease allocation; no surcharge credit
- pure prevention before post-defense transfer/tempHP
- strongest remaining same-family pool

# AB5-07 — Planar Protection

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 5 | 9 | 10 |
| Druid | Abjuration | 5 | 9 | 10 |
| Mage | Abjuration | 5 | 9 | 10 |
| Tinker | Abjuration | 5 | 18 | 10 |
| Wizard | Abjuration | 5 | 9 | 10 |
| Paladin | Abjuration | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** Area is warded against creatures from a specific plane.
- **Catalog placements:** [{"name": "Planar Protection", "school": "Abjuration", "level": 5, "summary": "Area is warded against creatures from a specific plane."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Concentration, up to 1 minute`, components `V, S, M/F`, RP `10`, resolution `Automatic or opposed as described`, effect `Area is warded against creatures from a specific plane.`

## Complete current procedure
Action; range 60 feet; V/S/M/F; base 10 RP; concentration up to 60 elapsed seconds. Before payment choose one actual opaque `planeKey` already established in campaign/source records and one perceived center within 60 feet and line of effect. Create a fixed 15-foot-radius spherical ward, clipped by actual solid center line of effect.

NEW eligibility `AC5-PLANAR-META-01`: the ward applies only to a creature body whose current operational travel/source provenance explicitly records `lastArrivedFromPlaneKey == chosenPlaneKey` or `createdFromPlaneKey == chosenPlaneKey`. This says only that the current body actually arrived/was sourced from that plane for these spells. Creature type, Elemental/outsider label, mortal Wheel name, soul/native origin and current location are insufficient. Indeterminate provenance remains Indeterminate and is not secretly detected or blocked.

An eligible creature already inside when the ward forms is not expelled, suppressed or damaged. It may move within and leave; after leaving it cannot cross inward while still eligible. A walking/forced/carried attempted inward crossing stops at the last legal exterior position without free shove/damage. A carried eligible creature is a separate body; the carrier may drop it outside but cannot make it inventory. An actual teleport/portal arrival whose destination footprint would be inside fails atomically for that body/group under its own cost/commitment rule. A teleport from one outside point to another outside point is unaffected; no imagined path through the sphere exists.

Suppression opens the boundary and clocks continue. Bodies that entered during suppression are already-inside on resumption: no ejection/crush; they can remain/move within/leave but cannot reenter after leaving while the ward is operative. Ending the ward never ejects anyone. The ward grants no damage, concealment, attack immunity, information disclosure or native-plane determination.

### Explicit NEW scoped authorship
- Opaque actual planeKey + travel/source provenance predicate
- fixed 15-ft sphere
- already-inside/leave/reentry rule
- forced/carried/teleport endpoint handling
- suppression entry retained without ejection
- no native/soul/Wheel inference

# AB5-08 — Reputation Shield

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 5 | 9 | 10 |
| Druid | Abjuration | 5 | 9 | 10 |
| Mage | Abjuration | 5 | 9 | 10 |
| Tinker | Abjuration | 5 | 18 | 10 |
| Wizard | Abjuration | 5 | 9 | 10 |
| Paladin | Abjuration | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** Target's reputation cannot be lowered for 24 hours.
- **Catalog placements:** [{"name": "Reputation Shield", "school": "Abjuration", "level": 5, "summary": "Target's reputation cannot be lowered for 24 hours."}]
- **Core:** casting `1 action`, range `60 feet`, duration `24 hours`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Target's reputation cannot be lowered for 24 hours.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; one willing perceived creature with line of effect; 86400 elapsed seconds; no concentration. Protect all of that creature's actual institutional standing-v1 records from genuine new negative signed contributions while the shield is operative. A newly encountered faction can initialize ordinary baseline 0 and is then protected.

At each distinct EX58/reputation consequence assignment, keep the full event/provenance/signed proposed amount. Replace an otherwise valid negative contribution with 0 and record `preventedByReputationShield`; do not defer it as debt. Positive contributions remain and use ordinary per-scene signed cap and absolute bounds. Current standing is not frozen at cast-time floor; later gains remain gains and later negative contributions are still prevented.

This does not rewrite a negative event that actually occurred before the shield began, and does not block correction of an erroneous stored score, deduplication or provenance repair. A genuine voluntary transaction requiring payment/surrender of standing cannot receive its benefit while the shield prevents that negative payment; the target can voluntarily end its own shield on its turn without an Action if it wants to pay. Suppression allows new negative consequences normally; resumption does not repair them.

No memories/evidence/law/contracts/fees/allegiance/hostility/consent or NPC agency are changed. Multiple shields still provide only one prevention while any is active, with separate clocks. Expiry creates no deferred penalty and restores no past standing.

### Explicit NEW scoped authorship
- standing-v1 negative-contribution prevention with full provenance
- ordinary caps/gains preserved
- correction and voluntary standing-payment boundaries
- no social mind control/deferred debt

# CJ5-01 — Summon Greater Fire Pet

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 5 | 9 | 10 |
| Mage | Conjuration | 5 | 9 | 10 |
| Ranger | Conjuration | 5 | 17 | 10 |
| Shaman | Conjuration | 5 | 13 | 10 |
| Tinker | Conjuration | 5 | 18 | 10 |
| Wizard | Conjuration | 5 | 9 | 10 |

## Preserved source baseline
- **Catalog effect:** HP 60, AC 17, 2d10 fire, aura burns adjacent foes.
- **Catalog placements:** [{"name": "Summon Greater Fire Pet", "school": "Conjuration", "level": 5, "summary": "HP 60, AC 17, 2d10 fire, aura burns adjacent foes."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Concentration, up to 1 minute`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `HP 60, AC 17, 2d10 fire, aura burns adjacent foes.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds. Create one Greater Fire Pet in one perceived supported unoccupied footprint that fits its Medium body and has line of effect. Use AC5-PROFILE-GREATER-FIRE-PET-01 exactly: HP60, AC17, Speed30, commanded 5-ft Fire Strike for 2d10 fire using original owner's current spell attack, and the passive 5-ft aura.

The aura is not an entry trigger. At each perceived hostile recipient's future regular START while within 5 feet and body-to-recipient line of effect, make DEX vs original owner's current spell DC; failure takes 1d6 fire, success half floor. Max one aura attempt per owner/target/Greater-Fire-Pet family/numbered round, outside initiative once per six seconds. One d6 may be shared across the cycle but saves/defenses/damage roots are per recipient. The owner cannot use the aura as hidden allegiance detection: only creatures the conscious owner actually perceives/regards as hostile qualify.

Use shared Companion Command/global offense budget for Fire Strike; aura is the printed passive exception and does not grant another offensive Action. One Greater Fire Pet per owner, distinct from lower Fire Pet body cap but not from the owner-wide command/offense allowance.

Damage-root identity follows AC5-ROOT-01: commanded attack dealer=pet; each aura recipient root dealer=pet at that START. Owner Null Veil never automatically converts pet damage. Apply AC5-SUMMON-TARGET-01/accepted Null lifecycle: qualifying Null damage to 0 keeps this same finite body Disabled 0 while concentration/source remains, including subsequent Null hits; legal Healing Rite/ordinary living-ally HP healing can restore above 0. Ordinary non-Null damage to 0 removes the body normally. Independent expiry/concentration/replacement still ends it.

Under Lesser Antimagic use AC5-ANTIMAGIC-SUMMON-01. No fire immunity, extra light, fuel, generic Burning condition, corpse or harvestable elemental material is inferred.

### Explicit NEW scoped authorship
- Complete finite profile
- passive aura timing/save/family cap
- AC5 Null/healing extension
- damage-root dealer = pet
- AC5 profile-specific antimagic suppression

## Operative profile
### AC5-PROFILE-GREATER-FIRE-PET-01
- **id:** AC5-PROFILE-GREATER-FIRE-PET-01
- **classification:** NEW finite summoned profile; mechanical type Elemental only for targeting; no native-plane/soul inference
- **size:** Medium
- **creatureType:** Elemental
- **weightLb:** 100
- **hpMax:** 60
- **ac:** 17
- **speedFt:** 30
- **abilities:** `{"STR": 14, "DEX": 14, "CON": 16, "INT": 4, "WIS": 10, "CHA": 6}`
- **saves:** Each saving throw uses original owner's current PB as the total modifier; no ability modifier is added unless another exact source says so.
- **checks:** Raw current ability modifier only; no proficiency.
- **senses:** Ordinary sight/hearing; no inherent darkvision or special sense.
- **defenses:** No inherent resistance/immunity from this profile.
- **command:** Shared Companion Command: owner Bonus Action while conscious, perceiving the body within 60 ft and line of effect; attached phase immediately after owner's whole turn. One global command and one offensive companion Action per owner/numbered round across eligible companions. Without command: defensive Move/Dodge only.
- **attack:** `{"name": "Fire Strike", "activation": "commanded Action", "reachFt": 5, "targets": 1, "attackModifier": "original owner's current spell attack modifier", "damage": "2d10 fire", "critical": "double attack dice only"}`
- **aura:** `{"radiusFt": 5, "lineOfEffect": true, "trigger": "qualifying hostile perceived recipient future regular START", "save": "DEX vs original owner's current spell DC", "damage": "1d6 fire fail; half floor success", "frequency": "max one attempt per owner/target/Greater-Fire-Pet family/numbered round; outside initiative one per 6 sec", "roll": "one shared d6 per owner aura cycle, separate recipient saves/roots", "entry": "no entry tick", "offenseBudget": "passive source exception; does not consume or grant offensive companion Action"}`
- **ending:** One Greater Fire Pet per owner. Successful replacement, concentration/source end, expiry/dismissal or ordinary non-Null damage reaching 0 ends body. Intrinsic manifestation leaves no corpse/loot/fuel. Genuine independently supplied objects remain real and drop/settle normally.
- **nullHealing:** AC5-SUMMON-TARGET-01 + accepted finite-summon Null branch
- **suppression:** AC5-ANTIMAGIC-SUMMON-01

# CJ5-02 — Massive Elemental Blast

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 5 | 9 | 10 |
| Mage | Conjuration | 5 | 9 | 10 |
| Ranger | Conjuration | 5 | 17 | 10 |
| Shaman | Conjuration | 5 | 13 | 10 |
| Tinker | Conjuration | 5 | 18 | 10 |
| Wizard | Conjuration | 5 | 9 | 10 |

## Preserved source baseline
- **Catalog effect:** All enemies in 20 ft radius: 5d8 elemental damage.
- **Catalog placements:** [{"name": "Massive Elemental Blast", "school": "Conjuration", "level": 5, "summary": "All enemies in 20 ft radius: 5d8 elemental damage."}]
- **Core:** casting `1 action`, range `20 feet`, duration `Instantaneous`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `All enemies in 20 ft radius: 5d8 elemental damage.`

## Complete current procedure
Action; casting-point range 20 feet; V/S/F; base 10 RP; Instantaneous. Before payment choose one perceived center within 20 feet and center line of effect, and choose exactly one damage type for the whole cast from acid, cold, fire or lightning. This finite menu is NEW and source-compatible; it does not create a generic `elemental` damage type.

At resolution snapshot every creature in the 20-foot-radius sphere that the caster currently perceives and affirmatively regards as an enemy from available information and that is reached by center line of effect. There is no target-count cap and no hidden allegiance/Invisible-enemy detection. Each target makes DEX vs actual spell DC. Roll 5d8 once; failed save takes full chosen type, success takes half floor, then apply each target's real defenses independently. Each recipient receives a separate damage root under AC5-ROOT-01 with dealer=caster; shared dice do not merge recipient roots.

No objects/allies outside the stated enemy-creature predicate receive this spell packet. No lingering terrain, slow, Burning, corrosion, conductivity chain, fuel/material stock or summoned Elemental is created. Mage Arcane Bypass can be declared for this damaging Mage spell and ignores printed resistance to the chosen type only; immunity remains. Tinker Malfunction Field does not apply because this spell uses saves, not spell attacks.

### Explicit NEW scoped authorship
- One cast chooses acid/cold/fire/lightning
- 20-ft point range distinct from 20-ft radius
- perceived-hostile all-target snapshot
- DEX full/half
- one shared 5d8 but separate damage roots

# CJ5-03 — Living Magma

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 5 | 9 | 10 |
| Mage | Conjuration | 5 | 9 | 10 |
| Ranger | Conjuration | 5 | 17 | 10 |
| Shaman | Conjuration | 5 | 13 | 10 |
| Tinker | Conjuration | 5 | 18 | 10 |
| Wizard | Conjuration | 5 | 9 | 10 |

## Preserved source baseline
- **Catalog effect:** Target must CON save or suffer 1d10/round for 3 rounds.
- **Catalog placements:** [{"name": "Living Magma", "school": "Conjuration", "level": 5, "summary": "Target must CON save or suffer 1d10/round for 3 rounds."}]
- **Core:** casting `1 action`, range `60 feet`, duration `3 rounds`, components `V, S, F`, RP `10`, resolution `Constitution save`, effect `Target must CON save or suffer 1d10/round for 3 rounds.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; one perceived creature with line of effect; source duration 3 rounds. NEW damage type is fire. At resolution target makes the printed CON save vs spell DC. Success prevents this new application. Failure establishes one target-bound recurring magical rider and, under AC5-ROOT-01, creates its damage root immediately at establishment even though no immediate damage packet occurs.

The rider has exactly three future target regular-START damage opportunities. An already underway START is not counted. Each opportunity rolls 1d10 fire separately and resolves ordinary defenses/HP/life consequences. No repeat save and no concentration are added. Outside initiative schedule at application+6,+12,+18 seconds; preserve these ordinal deadlines through initiative transitions/extra turns.

All three ticks descend from the root created on failed-save establishment and inherit that root's creation-time Null flag. Later caster Veil changes do not rewrite them. If a scheduled tick is actually suppressed, consume that ordinal without a damage packet/root child and do not bank/make it up. Fire immunity/prevention can make a tick 0 without ending remaining opportunities. Death/body removal ends the rider; merely reaching 0 while still an active creature does not invent early ending.

One Living Magma application per target across casters. A newly paid cast that successfully fails the target save replaces the still-live older rider; a successful save leaves the old rider intact. The name creates no magma creature/pool/terrain/light/entrapment/generic Burning and ordinary water does not remove it unless an exact source removes ongoing magic.

### Explicit NEW scoped authorship
- Fire damage
- failed-save establishment is root checkpoint
- exactly three future START ticks/no initial packet
- no repeat save/concentration
- suppressed tick consumed, no packet
- one-family replacement

# CJ5-04 — Elemental Banishment

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 5 | 9 | 10 |
| Mage | Conjuration | 5 | 9 | 10 |
| Ranger | Conjuration | 5 | 17 | 10 |
| Shaman | Conjuration | 5 | 13 | 10 |
| Tinker | Conjuration | 5 | 18 | 10 |
| Wizard | Conjuration | 5 | 9 | 10 |

## Preserved source baseline
- **Catalog effect:** Remove 1 summoned enemy from battlefield (CHA save).
- **Catalog placements:** [{"name": "Elemental Banishment", "school": "Conjuration", "level": 5, "summary": "Remove 1 summoned enemy from battlefield (CHA save)."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Concentration, up to 1 minute`, components `V, S, F`, RP `10`, resolution `Charisma save`, effect `Remove 1 summoned enemy from battlefield (CHA save).`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds; printed CHA save. Target exactly one perceived creature within range/line of effect that (a) the caster currently regards as an enemy from available information and (b) has an actual active summon-source identity proving this body was created/summoned by a still-recognizable source. Elemental type, outsider label and extraplanar provenance are irrelevant. A natural Elemental is not eligible merely for being Elemental; an eligible summoned non-Elemental can qualify. Hidden/unknown summon provenance may defeat a paid cast without diagnostic.

Commit ordinary costs/concentration/counter timing, then target makes CHA save. Success: no removal. Failure: require/spend the shared hard-control allowance; if unavailable no exile. On successful failed-save establishment, remove that same summoned enemy to an AC5-BANISH-EXT-01 cell for this spell's own concentration duration. Do not desummon it or send it to a home/native plane.

Use the accepted Banishment custody/real-clock/legal-escape/closure/body-placement interfaces only through AC5-BANISH-EXT-01. A separate carried creature is not gear and does not travel automatically. Genuine noncreature gear/cargo that legally accompanies the target remains the same inventory.

If the summon source itself ends/expires/dismisses/replaces the body while exiled, the body ends under that source; Elemental Banishment ends immediately and closes the cell, returning only surviving genuine loose cargo. Actual suppression of this exile application closes/ends it rather than pausing. Current endpoint blockers apply at establishment; terminal closure keeps the narrow accepted Banishment-only blocker exception through this explicit extension.

### Explicit NEW scoped authorship
- Eligibility = actual summoned enemy, not Elemental/extraplanar synonym
- explicit AC5-BANISH-EXT-01 scope reuse
- source concentration minute preserved
- shared hard-control gate
- summon expiry beats exile and settles cargo

# CJ5-05 — Planar Binding

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Bard | Universal | 5 | 13 | 10 |
| Cleric | Universal | 5 | 9 | 10 |
| Druid | Conjuration | 5 | 9 | 10 |
| Mage | Conjuration | 5 | 9 | 10 |
| Mirrorsage | Universal | 5 | 13 | 10 |
| Ranger | Conjuration | 5 | 17 | 10 |
| Shaman | Conjuration | 5 | 13 | 10 |
| Tinker | Conjuration | 5 | 18 | 10 |
| Wizard | Conjuration | 5 | 9 | 10 |
| Paladin | Universal | 5 | 17 | 10 |

## Preserved source baseline
- **Catalog effect:** Force an extraplanar creature to serve you for 24 hours.
- **Catalog placements:** [{"name": "Planar Binding", "school": "Conjuration", "level": 5, "summary": "Force an extraplanar creature to serve you for 24 hours."}, {"name": "Planar Binding", "school": "Universal", "level": 5, "summary": "Bind extraplanar creature to service."}]
- **Core:** casting `1 action`, range `60 feet`, duration `24 hours`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Force an extraplanar creature to serve you for 24 hours.`
- **Core:** casting `1 action`, range `60 feet`, duration `Instantaneous`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Bind extraplanar creature to service.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP. Preserve both printed placements/access records. The Conjuration source expressly promises 24-hour service; the Universal source retains Instantaneous duration metadata and `Bind extraplanar creature to service.` NEW reconciliation: the casting/binding establishment is instantaneous once resolved, while a successful service record lasts 86,400 elapsed seconds. This preserves the explicit 24-hour promise instead of erasing it to match the Universal metadata.

Target one perceived active creature within 60 feet/line of effect whose current body has explicit operational extraplanar evidence under AC5-PLANAR-META-01: either an exact current source marks the body extraplanar relative to the current plane, or its current travel/source provenance proves arrival/creation from a different actual planeKey. Creature type, outsider/Elemental/summoned labels, mortal Wheel name and supposed native/soul origin are insufficient. Unknown provenance can defeat a paid cast without revealing the hidden fact.

NEW save: target makes CHA vs actual spell DC; a willing creature may elect failure before rolling. On failure require/spend the shared hard-control allowance for this binder/target/encounter. Success creates no service record. A successful failure creates one nonconcentration service record until establishment+86,400 seconds, target death/body-source ending, eligible dispel/removal or replacement of the same binder→target record.

Service never creates/summons/heals/extends the target or grants actions/resources. Once per numbered round the binder may spend a Bonus Action to issue one simple service order through a one-way same-plane command-intent channel; outside initiative, at most one such order per 6 elapsed seconds. The channel reveals no target senses/location/knowledge and is inactive while binder/target are on different planes, though the 24-hour clock continues. An order may require ordinary movement, an ordinary/basic Attack, Dodge, Disengage, Help, Interact or an at-will target action the creature genuinely possesses. It cannot compel RP/spellcasting, charges, recharge/per-rest abilities, consumables/special expendables, permanent property transfer, protected secrets, knowingly binding-oath violation, direct self-harm or knowingly suicidal routes.

Orders use the accepted Compelled Budget Arbitration. They claim only the target's real remaining movement/Action/interaction budget and get a priority timestamp when issued. Impossible/ineligible orders claim no budget and do not end the service record. No second Action, initiative turn, Reaction, Bonus Action or companion-offense token is created. If the target is a companion whose own source requires the original owner's Companion Command/offense allowance before an attack/action exists, Planar Binding cannot bypass that gate; the service order can only constrain an action the source actually makes available.

One live Planar Binding per binder→target pair. Different mandatory controls can coexist and arbitrate by the existing priority rules; none duplicates behavior budgets. A finite summoned target's independent concentration/expiry/replacement/0HP endpoint remains real and can end its body long before 24 hours; Binding ends with the body and never recreates it. Under Lesser Antimagic, suppress only the local binding compulsion expression on an intersecting target; its 24-hour clock continues and the target uses its ordinary agency while suppressed unless another source controls it.

### Explicit NEW scoped authorship
- Preserve both placements and source conflict
- 24h service record with Universal Instantaneous preserved as establishment metadata
- explicit operational extraplanar provenance, not native/soul/type inference
- NEW CHA save + hard-control gate
- one-way same-plane simple service command and Compelled Budget Arbitration
- no finite-resource/spell/extra-action compulsion
- source lifespan not extended

### Preserved source conflict
- `{"field": "duration", "Conjuration": "24 hours", "Universal": "Instantaneous", "authoredResolution": "Instantaneous binding establishment + 24-hour nonconcentration service record; both source texts preserved."}`

# CJ5-06 — Resonance Nexus

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 5 | 9 | 10 |
| Mage | Conjuration | 5 | 9 | 10 |
| Ranger | Conjuration | 5 | 17 | 10 |
| Shaman | Conjuration | 5 | 13 | 10 |
| Tinker | Conjuration | 5 | 18 | 10 |
| Wizard | Conjuration | 5 | 9 | 10 |

## Preserved source baseline
- **Catalog effect:** Create a field where all spells cost 2 fewer Resonance Points.
- **Catalog placements:** [{"name": "Resonance Nexus", "school": "Conjuration", "level": 5, "summary": "Create a field where all spells cost 2 fewer Resonance Points."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Instantaneous`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Create a field where all spells cost 2 fewer Resonance Points.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; source Instantaneous metadata preserved. NEW: create a fixed 10-foot-radius nonphysical sphere at a perceived point within 60 feet/line of effect, concentration up to 60 elapsed seconds. It grants no support/cover, stores no RP and is clipped by actual center line of effect.

An actual spell cast qualifies once, at legal cast commitment, when its original caster's occupied body intersects the operative sphere. Target/area may be outside. Familiar/Echo/projection origin does not substitute for caster location. Actual Reaction spells qualify. Paying RP for a nonspell technique does not. A readied spell is priced at original cast commitment, not release.

Use AC5-PRICE-01 exactly. Nexus is one ordinary -2 reduction after exact class/source reductions/waivers/minima and before AC4 Dampening +2 and final Influence. Overlapping Nexuses provide one -2 total. Nexus cannot reduce protected Resonance Barrier X, HP/material/charge/use costs or standalone nonspell transfers. A route with no ordinary RP-price interface has no Nexus amount to reduce; accepted Dampening may independently create its +2 interface.

A Nexus never retroactively prices its own creation. If beginning a new Nexus ends the caster's prior concentration Nexus, the old field cannot discount the replacement because concentration transition occurs at new commitment; another owner's already-operative field can. Movement/suppression after commitment does not alter/refund the paid price. Suppression simply removes eligibility for future commitments while the original deadline continues.

### Explicit NEW scoped authorship
- Fixed 10-ft concentration field
- AC5-PRICE-01 ordering
- actual caster body at commitment
- one -2 across overlaps
- no charge/nonspell/protected-principal discount
- no self-financed concentration replacement

# CJ5-07 — Faction Champion

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 5 | 9 | 10 |
| Mage | Conjuration | 5 | 9 | 10 |
| Ranger | Conjuration | 5 | 17 | 10 |
| Shaman | Conjuration | 5 | 13 | 10 |
| Tinker | Conjuration | 5 | 18 | 10 |
| Wizard | Conjuration | 5 | 9 | 10 |

## Preserved source baseline
- **Catalog effect:** Summon a powerful warrior from your allied faction.
- **Catalog placements:** [{"name": "Faction Champion", "school": "Conjuration", "level": 5, "summary": "Summon a powerful warrior from your allied faction."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Concentration, up to 1 minute`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Summon a powerful warrior from your allied faction.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds. Before payment choose one canonical factionId and satisfy AC5-CHAMPION-ALLY-01: actual alliedStatus=true, current standing >0, actual invocation permission, and no explicit aid prohibition. Positive standing alone, faction membership alone, Faction Ally membership+permission, or Faction Portal standing+HQ are not substitutes. Hidden loss of eligibility can prevent formation after a paid cast without revealing secret institutional facts.

NEW interpretation of `summon a powerful warrior from your allied faction`: create one bounded temporary Faction Champion representative using AC5-PROFILE-FACTION-CHAMPION-01, rather than transporting/copying a named real NPC. It has no private faction memories, real official identity/rank, contracting authority, secrets or institutional command. Intrinsic martial gear is profile manifestation, not faction inventory/loot.

Place the Medium body in one perceived supported unoccupied fitting footprint within 60 feet/LoE. Use shared Companion Command/global offense rules and its one Champion Strike. One Champion per owner across all factions. A later standing change does not remotely end an already admitted body; the source continues until concentration/expiry/replacement/dismissal/ordinary non-Null 0 HP or real removal.

Apply AC5-SUMMON-TARGET-01/accepted Null lifecycle: qualifying Null damage reaching 0 gives Disabled 0 while source persists; repeated Null hits do not create ordinary death; legal ordinary living-ally HP healing can restore above 0. Under Lesser Antimagic use AC5-ANTIMAGIC-SUMMON-01. Genuine borrowed items remain real/drop normally; intrinsic gear vanishes. No automatic reputation gain, expedition seat, hireling, formula teaching, faction credential, soul/native origin or distant-NPC injury exists.

### Explicit NEW scoped authorship
- AC5-CHAMPION-ALLY-01 four-part gate
- bounded created representative instead of real NPC transport
- complete finite profile
- one slot across factions/shared companion budgets
- AC5 Null/healing and antimagic extensions

## Operative profile
### AC5-PROFILE-FACTION-CHAMPION-01
- **id:** AC5-PROFILE-FACTION-CHAMPION-01
- **classification:** NEW finite summoned representative; mechanical type Humanoid for targeting only; no real NPC transport, membership, native origin or soul inference
- **size:** Medium
- **creatureType:** Humanoid
- **weightLb:** 180
- **hpMax:** 70
- **ac:** 18
- **speedFt:** 30
- **abilities:** `{"STR": 18, "DEX": 12, "CON": 16, "INT": 10, "WIS": 12, "CHA": 12}`
- **saves:** Each saving throw uses original owner's current PB as total modifier.
- **checks:** Raw ability modifier only; no proficiency.
- **senses:** Ordinary sight/hearing only.
- **defenses:** No inherent resistance/immunity.
- **command:** Same shared Companion Command/global offense rules as Greater Fire Pet.
- **attack:** `{"name": "Champion Strike", "activation": "commanded Action", "reachFt": 5, "targets": 1, "attackModifier": "original owner's current spell attack modifier", "damage": "2d8 + original owner's current PB slashing", "critical": "double 2d8 dice only; PB flat is not doubled"}`
- **intrinsicGear:** Apparent armor/weapon/shield are intrinsic manifestation comprising AC/attack profile, not detachable inventory or faction stock.
- **ending:** One Champion per owner across all factions. Replacement/concentration/source end/expiry/dismissal or ordinary non-Null 0 HP ends body. Genuine borrowed items remain real and drop/settle normally; intrinsic gear vanishes.
- **nullHealing:** AC5-SUMMON-TARGET-01 + accepted finite-summon Null branch
- **suppression:** AC5-ANTIMAGIC-SUMMON-01

# CJ5-08 — Alignment Portal

## Preserved access
| Class | School | Rank | Minimum level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 5 | 9 | 10 |
| Mage | Conjuration | 5 | 9 | 10 |
| Ranger | Conjuration | 5 | 17 | 10 |
| Shaman | Conjuration | 5 | 13 | 10 |
| Tinker | Conjuration | 5 | 18 | 10 |
| Wizard | Conjuration | 5 | 9 | 10 |

## Preserved source baseline
- **Catalog effect:** Create a gateway to a plane aligned with your alignment.
- **Catalog placements:** [{"name": "Alignment Portal", "school": "Conjuration", "level": 5, "summary": "Create a gateway to a plane aligned with your alignment."}]
- **Core:** casting `1 action`, range `60 feet`, duration `Instantaneous`, components `V, S, F`, RP `10`, resolution `Automatic or opposed as described`, effect `Create a gateway to a plane aligned with your alignment.`

## Complete current procedure
Action; range 60 feet; V/S/F; base 10 RP; source Instantaneous metadata preserved. The printed effect requires a genuine gateway to a plane aligned with the caster. NEW finite completion: concentration up to 60 elapsed seconds; successful resolution creates two linked 5-foot-wide × 8-foot-high vertical apertures, origin and destination, through which eligible bodies may actually cross. This is not a same-plane teleport or observation-only window.

Before payment:
1. Compute the caster's currently effective canonical nine-point alignment key only if both axes are defined. Apply ordinary underlying records including accepted AP-AS-01 Suggestion/Purge interaction first, then active AC4 Lock/Anchor snapshots last under AC4-ALIGN-01. Undefined axis = no legal compatibility key.
2. Choose an actual destination `planeKey` different from current plane and one genuinely known `siteId` on that plane. Rumor, approximate mortal Wheel label or unproven name-equivalence is insufficient.
3. The actual plane record must carry AC5-ALIGN-PORTAL-META-01 compatibility including the caster's effective key and the chosen known site. This metadata is spell travel permission only, not objective plane alignment/native/soul/deity taxonomy.
4. Choose a perceived clear supported origin aperture within 60 feet/LoE. Destination aperture must have a recorded clear supported fitting area at the known site. Recheck actual endpoint blockers, including accepted Dimensional Anchor, at resolution.

On successful resolution snapshot the compatibility alignment key for this portal application. Later alignment changes do not retroactively collapse the already-open gate. Apertures remain fixed until concentration ends/60 seconds/removal. Ordinary sight may view through the gateway only where the actual aperture geometry permits, but no spell/attack/remote-sense line of effect is created across planes unless that independent source itself permits cross-plane targeting; the portal's operative permission is physical crossing.

Crossing: one creature/group transaction at a time. Entering costs 5 feet ordinary movement; approach movement is normal. A crossing atomically moves the traveler and genuine legally carried noncreature gear to a fitting unoccupied space at/adjacent to the destination aperture. A physically carried creature is a separate traveler in the same atomic packet and all bodies must independently fit/support and satisfy any arrival ward/blocker; it is never gear. Revalidate both endpoint apertures, destination occupancy/support, active Dimensional Anchor/true transport blockers and Planar Protection at each crossing. If known illegal at preflight, no 5-ft crossing movement is committed; if legality changes after a legally committed crossing event, the atomic transfer fails at origin under the source-specific crossing record without partial arrival/bisection. Transit that fully resolves before the absolute deadline completes; at the deadline the portal closes and no new crossing begins. No free return exists after closure.

Successful cross-plane crossing updates only operational travel provenance under AC5-PLANAR-META-01 (`lastArrivedFromPlaneKey` = actual origin planeKey). Suppression of either aperture blocks new crossings while concentration/deadline continues; no traveler is ejected. Planar Protection may block an arrival when the traveler's established provenance matches the ward's chosen planeKey and the destination would enter the ward. No mortal Wheel mapping, soul destination, native species, deity or campaign-era fact is inferred.

### Explicit NEW scoped authorship
- Genuine two-way 60-second gateway layered over preserved Instantaneous metadata
- opaque planeKey + known site + explicit spell-specific compatibility metadata
- effective alignment uses AP-AS-01 then AC4-ALIGN-01
- 5×8 fixed apertures; 5-ft movement atomic crossing
- real cargo/separate-creature/endpoint/ward handling
- travel provenance update only, no ontology

### Preserved source conflict
- `{"field": "duration", "source": "Instantaneous", "authoredResolution": "Instantaneous gate establishment with NEW concentration up to 60 seconds for the continuing gateway; source metadata preserved."}`

# Important separations
- **Cleric Banish Unholy** remains a separate class technique.
- **Wizard Counterspell** and **Wizard Dispel Magic** remain their actual class cards with their own prices/checks/recharges; similarly named ordinary spells do not replace them.
- **Ranger Nature's Whisper** remains a magical nonspell and does not receive Nexus/Dampening spell-price treatment.
- Elemental, outsider, summoned and extraplanar are not synonyms unless a specific card explicitly makes that test.
