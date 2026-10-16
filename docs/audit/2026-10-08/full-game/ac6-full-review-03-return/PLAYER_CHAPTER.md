# AC6 Abjuration/Conjuration — Complete Provisional Player Procedures

This chapter is the complete current AC6 authored procedure reference for the fourteen rank-six cohort identities and sixteen printed placements. It is a replacement review candidate, not adoption. Frozen source/access records remain authoritative evidence; explicitly labeled NEW rules below complete missing operational behavior without settling named cosmology, soul/native origin, campaign era, runtime balance or publication.

## Shared operating rules
### AC6-PRICE-01
NEW AC6 bridge using accepted AC5 pricing order; does not alter AC5.
For an ordinary AC6 spell, start from its actual base spell RP price (rank6 generally 13; Alignment Nexus Conjuration8 is 21). Apply accepted Resonance Nexus ordinary -2 spell-price reduction first when genuinely eligible, then mandatory Resonance Dampening Field +2 if applicable, then final Resonance Influence Ease/Strain. A discount never changes generating rank. Resonance Forge cycle 5 RP is protected conversion principal and is not a spell price or subject to these modifiers.
### AC6-DAMAGE-ROOT-01
NEW per-card dealer/root mapping constrained by accepted Null/damage-root rules.
Forbiddance: caster is dealer at each new field exposure root. Chain Arc: caster is dealer and one shared selection/damage event still creates recipient-specific damage roots using that caster state at root creation. Skybrand: effect has no creature identity; caster is dealer separately for each attack root. Greater Air Pet, Faction Army soldier and Greater Planar Ally are their own creature dealers for their own attacks/auras. Pure damage transfer preserves the original root flag; genuinely new reflected damage follows its source.
### AC6-HEAL-TARGET-02
NEW scoped target predicate for only Greater Air Pet and Faction Army soldier profiles.
While the original summon source exists, Greater Air Pet and each Faction Army soldier body count as an active creature and living ally for otherwise legal HP-healing. This grants no natural biology, soul/native origin, resurrection, disease/curse treatment or generic summon healing. A genuine heal above 0 restores the same NullDisabled body without refreshing source duration or command history. Greater Planar Ally uses GA-HEAL-01 instead.
### AC6-SUMMON-SUPPRESS-01
NEW AC6 scoped completion chosen for coherence with accepted AC5 same-body paused summons.
Full antimagic suppression of Greater Air Pet, Greater Planar Ally, or an individual Faction Army soldier does not end or recreate the body. The same body, identity, HP, Null state, deadline, carried real cargo and source parent remain; manifestation is suppressed, Speed becomes 0 and it cannot act, command, attack, provide intrinsic attacks/traits or satisfy physical-service permissions from the suppressed source. All real clocks continue. If the original source independently expires, is replaced, dismissed, loses concentration where required, or otherwise ends while suppressed, the body ends normally. When suppression ends before source ending, the same body resumes at the same legal position/state; no missed action/command is replayed.
### AC6-COMPANION-01
Current shared command integration.
All actual commanded companions/devices of one owner share one Bonus Action command and one offensive companion Action per numbered round unless a source explicitly overrides it. Commands occur during the owner regular turn, require actual channel/range/perception/LoE as printed, and execute in the attached phase after the whole owner turn. Extra turns do not reset the ledger. A newly created asset may receive an otherwise available command that round, but creation gives no free attack.
### AC6-CHAIN-RANDOM-01
NEW Chain Arc fair-selection completion.
At each successor hop, freeze the stable candidate array before drawing. Use a fair physical die with equal face mapping when practical; otherwise use an exact uniform N-entry draw. A legal reroll such as Fate Coin replaces that one original selection result against the unchanged candidate array and must use the replacement. Hidden Director-only draws remain hidden; a player who cannot perceive the die/event cannot spend Fate Coin. Once a successor is committed, later immunity, death, movement or lawful removal does not redraw earlier/later committed successors.
### AC6-SEAL-REMOVAL-01
Current negative interoperability conclusion; no new dispel permission created.
Resonance Seal protection cannot currently be selectively suppressed and then dispelled through the same accepted Lesser Antimagic/Greater Dispel transaction. Accepted Greater Dispel captures immutable termination operations; only the operation targeting the suppressing Antimagic field ignores that same field. Operations targeting Seal/parent at suppressed loci are suppressed and are not rescanned after field removal. Wizard class Dispel is a rank3 spell and is itself suppressed when its application locus is suppressed. An actual future/selective source could change this only through its exact text.
### AC6-NEXUS-TRANSPORT-01
NEW scoped Alignment Nexus Conjuration8 classification only.
Alignment Nexus Conjuration8 gateway crossings are both planar transitions and teleportation for predicates that expressly reference either. This is source-specific and does not change accepted AC5 Alignment Portal, which remains planar/extradimensional and non-teleport. Voluntary crossing therefore interacts with No Escape, Verdict Absolute and Reign of Ashes according to each exact predicate; forced movement remains governed by the exact voluntary/benefit wording.
### AC6-NEXUS-PLANE-BONUS-01
NEW bounded Nexus Conjuration8 benefit; no plane ontology claim.
While the Nexus parent remains live, an aligned creature physically present on the designated destination plane may receive the source-specific temporary +2 Nexus benefit at the events the Nexus procedure states. This does not make that plane intrinsically aligned, identify Wheel cosmology, infer soul/native origin, or grant the bonus after parent ending. Eligibility uses current effective alignment under accepted overlay ordering.
### AC6-FORGE-CYCLE-01
NEW Resonance Forge conversion interface using Forge revision02.
After a legal Forge cast, each complete cycle costs exactly 5 actual RP from one capable present participant plus 10 uninterrupted actual active minutes by the required workers and credits up to 60 adjusted manufacturing minutes in the current source work phase. The 5 RP is protected conversion principal, not an ordinary spell price. Interrupted cycles spend RP/time but give no cycle credit. A completed cycle does not independently stabilize an unfinished phase; source phase boundaries control stabilized work. Ordinary reviewed crafting XP/first-success/triviality remain in force.
### AC6-NEXUS-FAMILY-01
NEW family guard for the two Alignment Nexus modes.
One Alignment Nexus parent application per caster. Divination6 and Conjuration8 are distinct operations of one source identity; successful replacement ends the previous parent after normal commitment. Each event receives at most one Nexus bonus from this spell family even if multiple geometric/plane predicates might otherwise overlap.

## Summon / effect profiles
```json
{
  "AC6-GREATER-AIR-PET-PROFILE-01": {
    "id": "AC6-GREATER-AIR-PET-PROFILE-01",
    "status": "NEW scoped summon-only profile",
    "size": "Medium",
    "footprintFeet": [
      5,
      5
    ],
    "bodyMassPounds": 40,
    "armorClass": 18,
    "baseHitPoints": 65,
    "abilities": {
      "STR": 10,
      "DEX": 18,
      "CON": 14,
      "INT": 4,
      "WIS": 10,
      "CHA": 6
    },
    "speed": {
      "walk": 30,
      "fly": 40,
      "hover": true
    },
    "attack": {
      "name": "Wind Slash",
      "activation": "commanded offensive Action",
      "range": "melee 5 feet",
      "attackModifier": "owner current source-qualified spell attack",
      "damage": "2d8 slashing"
    },
    "projectileDefense": "When a projectile attack would otherwise hit this body, roll one public physical d2 after hit determination and before hit payload: 1=miss/deflected; 2=retain hit. One d2 governs all hit-dependent components of that projectile. Independent area effects use their own geometry and are not projectile attacks merely because delivered by a missile.",
    "saves": "All six saves use original source-owner current PB as total modifier; other ability checks use listed ability modifier without proficiency unless a real source adds it.",
    "healingScope": "AC6-HEAL-TARGET-02 only.",
    "lifecycle": "Finite concentration summon; qualifying Null damage can leave same NullDisabled0 body. AC6-SUMMON-SUPPRESS-01 pauses same body under full suppression. Concentration/expiry/replacement/dismissal/source-ending remain real. No corpse/loot/intrinsic item on ending."
  },
  "AC6-FACTION-SOLDIER-PROFILE-01": {
    "id": "AC6-FACTION-SOLDIER-PROFILE-01",
    "status": "NEW spell-created faction-representation profile; not real personnel transfer",
    "size": "Medium",
    "footprintFeet": [
      5,
      5
    ],
    "armorClass": 16,
    "baseHitPoints": 20,
    "speed": 30,
    "attack": {
      "name": "Martial Strike",
      "activation": "commanded offensive Action",
      "attackModifier": "+8",
      "range": "melee 5 feet",
      "damage": "1d8 slashing"
    },
    "intrinsicEquipment": "Appearance/intrinsic arms and armor are part of the temporary body and vanish with it; they are not stock, loot or transferable faction property.",
    "realCargo": "Genuine externally supplied objects retain their identities and drop once at actual position on source ending.",
    "healingScope": "AC6-HEAL-TARGET-02 only.",
    "lifecycle": "Each soldier is a separate body/HP/position. NullDisabled0 preserves that body while parent exists. AC6-SUMMON-SUPPRESS-01 pauses same body; parent expiry/concentration/replacement ends all remaining bodies once."
  },
  "AC6-GREATER-PLANAR-ALLY-PROFILE-01": {
    "id": "AC6-GREATER-PLANAR-ALLY-PROFILE-01",
    "status": "NEW unadopted summon-only profile for the printed CR6 assistance role; no certified challenge rating or imported bestiary approval.",
    "size": "Large",
    "footprintFeet": [
      10,
      10
    ],
    "standingHeightFeet": 10,
    "bodyMassPounds": 450,
    "armorClass": 17,
    "baseHitPoints": 120,
    "walkingSpeedFeet": 40,
    "abilities": {
      "STR": 18,
      "DEX": 12,
      "CON": 18,
      "INT": 10,
      "WIS": 12,
      "CHA": 10
    },
    "tags": [
      "creature",
      "summoned",
      "extraplanar"
    ],
    "classification": "No additional Elemental/Fiend/Humanoid/Undead/Construct type or native-plane identity is assigned. The explicit extraplanar tag is the spell's mechanical source assertion, not proof of a cosmological ancestry.",
    "saves": "All six saving throws use the actual original source-owner current PB as total modifier. Other checks use the printed ability modifier without proficiency. No trade, armor, weapon or tool proficiency is granted.",
    "sensesAndCommunication": "Ordinary sight and hearing. Understands the source-owner's spoken simple commands only; no speaking language, telepathy, remote sensory feed, supernatural knowledge, darkvision or other special sense.",
    "anatomyAndCargo": "Two actual hands, two feet and a complete Large body. May carry real cargo totaling at most200pounds AND8Load, within its hands/body capacity. These are an explicit maximum, not permission to ignore actual equipment, grasping, support or other tighter capacity rules. No riding/saddle, flight, swimming adaptation or free passenger support. Real externally supplied equipment is actual custody but supplies no unprinted attack or proficiency.",
    "attack": {
      "name": "Greater Planar Strikes",
      "action": "One commanded offensive Action containing two separate melee spell attacks",
      "reachFeet": 5,
      "attackModifier": "Original casting source-owner current PB + current actual source casting modifier",
      "hit": "2d8 + 4 physical damage per hit; choose bludgeoning, piercing or slashing once at creation for both strikes",
      "critical": "Double that attack's damage dice, not flat4",
      "magical": true
    },
    "otherActions": [
      "Dodge",
      "Dash",
      "Disengage",
      "Search using actual checks",
      "Simple object manipulation under real action/custody rules"
    ],
    "limits": "No autonomous offensive Action, opportunity attack, Reaction, spellcasting, special resistance/immunity, self-heal, class engine, resource pool, work crew, teaching, legal faction credential or compelled memory. It has no independently expendable equipment or saleable intrinsic weapons.",
    "healingScope": "NEW GA-HEAL-01, only for this profile while its original summon source exists: treat it as an active creature and a living ally for an otherwise legal ally/creature HP-healing effect, subject to actual willingness, range, perception, components, blockers, costs, source ceilings and no-healing flags. This narrowly supplies an operational target predicate; it asserts no biological or soul identity and grants no resurrection, regrowth, numeric track cure or generic healing of other summons/Constructs. A real eligible heal above0 ends its Null Disabled state on the same body.",
    "lifecycle": "Finite one-hour summon body. Ordinary damaging 0HP follows its source ordinary body-ending rule; qualifying Null damage instead leaves the same NullDisabled0 body while source exists. GA-HEAL-01 handles its scoped legal HP-healing. AC6-SUMMON-SUPPRESS-01 pauses the same body under full suppression rather than ending it. One-hour expiry, dismissal, replacement and other real source endings remain real. The printed CR6 role is not numerical certification."
  },
  "AC6-SKYBRAND-EFFECT-01": {
    "id": "AC6-SKYBRAND-EFFECT-01",
    "status": "effect-only profile",
    "body": "Visible nonphysical weapon-shaped magical effect fitting one 5-foot cube; no HP, inventory, support, cover, flanking body or creature dealer identity.",
    "movement": "Up to 30 feet of effect movement per valid command route.",
    "offense": "One commanded offensive activation contains exactly two separate melee spell attacks, reach5ft, each 1d12 lightning, using owner spell attack; revalidate each target at attack time.",
    "dealer": "Owner/caster is damage dealer separately for each attack root.",
    "ending": "Concentration/source ending or eligible dispel/suppression removes the effect; no item remains."
  },
  "AC6-RESONANCE-FORGE-FIXTURE-01": {
    "id": "AC6-RESONANCE-FORGE-FIXTURE-01",
    "massLb": 300,
    "armorClass": 17,
    "hitPoints": 50,
    "space": "5-foot cube",
    "workEnvelopeMaxLb": 500,
    "durationSeconds": 28800,
    "cycleRule": "AC6-FORGE-CYCLE-01"
  }
}
```

# Globe of Invulnerability
**Spell ID:** `globe-of-invulnerability`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 6 | 11 | 13 |
| Druid | Abjuration | 6 | 11 | 13 |
| Mage | Abjuration | 6 | 11 | 13 |
| Wizard | Abjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action, 60 feet, V/S/F and the sphere blocking spells of fifth level/Tier 5 or lower. NEW the operative measure is the original generating spell's actual rank 0 through 5; Tier here means spell rank, not material tier, class level, RP paid or a name-based estimate. An actually authorized rank-changing source uses its real generating rank; discounts/surcharges alone change no rank. Preserve the original conflicting terminology and Instantaneous metadata. NEW create one fixed 10-foot-radius sphere centered on a perceived point within range/line of effect, concentration up to 60 elapsed seconds. It is nonphysical, supplies no cover/support/collision and does not follow its caster.

NEW block a qualifying spell's new local application to a creature/object/point inside the globe when that component's genuine authorized origin is outside the globe at resolution. Use the actual originating body/legally authorized remote source, not arbitrary animation graphics or the target's position as a fabricated origin. Origin on the boundary counts outside; a recipient intersecting the protected interior is protected as a whole discrete body/item. Outgoing spells from inside and spells genuinely originating inside remain legal, including against inside recipients. An outside-to-outside spell path can pass through without protecting its outside recipient; this is a recipient ward, not an opaque antimagic wall. A spell's nonspell costs/casting commitments and concentration still occur; blocking its payload gives no refund or retroactive Counterspell.

For multi-target spells, prevent only qualifying protected recipient applications. Other targets remain independently legal. An outside-origin instantaneous area can resolve elsewhere, but its protected interior recipients receive no damage, condition, healing, teleport-arrival or created object/body application from that low-rank component. A genuine arrival originating outside is checked at its destination: a protected destination leaves the transported body at its actual origin under the transport source's ordinary failure rule, without free retargeting. This is not a general planar rule. A created summon outside can later move inside physically; its already-created real body does not become a new cast on every step. Its source-defined ordinary nonspell attack is not automatically blocked merely because a low-rank spell created it.

Existing creature-attached buffs/curses and completed instantaneous changes are not dispelled, suspended or ended when the globe forms or a bearer walks in. An already-established externally anchored ongoing area of rank 0-5 has only its covered local ongoing expression blocked while the globe applies; original concentration, duration, spent ticks and exterior effects continue. No queued pulse on leaving/expiry. A genuine new reapplication counts as new, not as protected historical work. Spell-granted intrinsic weapon enchantments remain established benefits; a newly triggered independent spell payload with its own actual originating interface is checked separately, without converting the entire physical weapon hit into a spell. Nonspell class abilities, ordinary projectiles, magical item engines and rank6+ spells are unaffected unless their actual source expressly makes them eligible spell components.

The globe itself is rank6. An outside lower-rank attempt aimed at its protected anchor is blocked even if that attempt would otherwise have a higher-rank dispel procedure; an inside eligible dispel, rank6+ source or actual explicit ward-bypass permission retains its scope. A spell that expressly ignores spell blocking overrides only this barrier component, not cover or unrelated legality. Suppression removes the globe's local protection while the original clock runs; it does not suppress every protected creature's unrelated magic. Concentration ending, expiry or actual removal ends it. Multiple globes supply the union of their operative protected volumes, no stronger rank ceiling; adjudicate origin/recipient against each separately. One active globe per caster, with normal concentration commitment and successful replacement rules. No hidden spell-rank or effect inventory is reported to the caster.

CURRENT AUTHORITY: Wizard Arch Dispel Magic /cards/19 is explicitly tagged wizard-spell and has normalized spellRank3. Its3RP price and higher-target check do NOT make it a magical nonspell or rank6. Thus an outside-origin class Dispel capable of selecting this rank6 Globe is nevertheless a rank3 incoming application and is blocked at its protected anchor. From a genuinely inside authorized origin it can resolve its actual INT+PB check against DC10+target rank. Ordinary Dispel Magic is separately rank3/base5RP and can select only actual rank0-3 effects; it cannot select the rank6 Globe in the first place. An actual magical nonspell is judged by its own source; no spell rank is guessed from cost or theme. This corrects the older AC6-N02 audit wording, not the accepted class card.

ACCEPTED TERMINAL RETURN: ordinary Banishment BAN-CLOSE-03 has an explicit narrow exception to endpoint transport prevention at mandatory closure. This Globe does not trap an ended ordinary Banishment cell by blocking its terminal rank4 arrival. Settle all extant identities through that accepted source, including actual occupied placement/conflict handling; no physical wall, support, death or size rule is bypassed. New voluntary transport, new exile applications and other spells receive no general exception. The accepted AC5-BANISH-EXT-01 bridge expressly extends the stated ordinary Banishment closure and placement protections only to Banish Elemental and Elemental Banishment. Those two named AC5 exiles receive that accepted terminal-return exception; no other transport spell inherits it by name or theme.

## Preserved printed effect
- Original name: Globe of Invulnerability
- Original placements: [{"name": "Globe of Invulnerability", "school": "Abjuration", "level": 6, "summary": "Sphere blocks spells of 5th level or lower."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Guards and Wards
**Spell ID:** `guards-and-wards`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Bard | Universal | 6 | 16 | 13 |
| Cleric | Abjuration | 6 | 11 | 13 |
| Druid | Abjuration | 6 | 11 | 13 |
| Mage | Abjuration | 6 | 11 | 13 |
| Mirrorsage | Universal | 6 | 16 | 13 |
| Wizard | Abjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP both Abjuration/Universal placements, Action, 60 feet, V/S/M-or-F and concentration up to one minute, filling an area with multiple defensive spells. NEW choose one perceived fixed center and a 20-foot-radius sphere with center line of effect. At casting name up to three actually perceived willing creatures within range, optionally yourself, as recognized passers for this cast. This list cannot change later, grants no allegiance/identity credential and is not selected from hidden membership. The following three explicitly NEW constituent spells form one rank-six cast and shared concentration, rather than free castings of Arcane Lock, Fog Cloud or Warning Ward from the catalog.

CLOSURE WARD: choose up to three actual nonliving closed doors/lids/gates entirely within the area and visible to the caster at resolution. No suitable closures simply means no closure targets; the other two constituents still form. Each selected closure is magically secured. A recognized passer can open/close it normally if the underlying physical locks/permissions also allow that act. Another creature can use an Action for STR (Athletics) or, with actual suitable trained thieves' tools, the appropriate DEX tool task against the original spell DC. Success/Critical Success permits that one opening without removing the ward; failure spends the Action, and a new actual forced-opening effort can try again as this explicit repeated physical-task permission. Ordinary locks remain their distinct actual Action/DC15 procedure; defeating the magic alone does not undo them. The ward does not close an open occupied door, crush a body, increase object HP, repair damage or create a door in empty space. Moving/destroying the real closure outside the field ends only its ward participation.

VEIL WARD: the operative field heavily obscures normal vision through its interior for unrecognized observers. Recognized passers see through this specific veil using ordinary sight, not through actual darkness, smoke, Hidden creatures or walls. This is a NEW magical visual veil, not physical fog or an illusory depicted scene. A genuinely applicable reviewed sight source can work only within its actual scope. True Seeing remains pending in the authored index; its older proposal is comparison evidence and grants no accepted bypass here. The veil creates no physical cover, removes no known location and adds no separate Invisible condition. Entering/leaving does not preserve a benefit beyond the live field or turn an unrecognized observer into a recognized one.

WATCH WARD: when an unrecognized creature first actually crosses from outside into the live field in a numbered round, including forced movement or a genuine teleport arrival, it emits a six-elapsed-second ordinary visible outline while inside this field. Occupants already present at creation are not entry events; reentry during the same caster/target/Guards-and-Wards round cannot restart the outline, including through replacement casts. The outline marks actual visible position through this ward's own veil but not through physical walls, and supplies no attack modifier, alignment/identity report or remote alarm to an absent caster. It does not remove a separate actual Invisible condition for unrelated sight-required purposes. A creature may leave and reenter during its original outline interval, resuming only the still-live remainder. No save, damage, Action denial or hard-control claim is supplied by these three layers.

Each constituent keeps one parent cast/rank/owner/DC/deadline. Ordinary dispelling of the addressable Guards and Wards source ends all its remaining layers; no separate three Counterspell windows, charges or concentration records exist. A source explicitly able to bypass/remove one selected magical lock/visual marking can affect only that actual component, without regenerating it through the parent. A removed individual closure ward stays removed for this cast. Local suppression suspends only actual intersecting expressions and clocks continue. Missed entries during suppression never queue a future outline; resumption is not entry. Expiry, concentration ending or actual parent removal ends all surviving layers, without repairing/breaking physical doors or curing other sources. One parcel per caster; a newly formed parcel replaces the old under the normal concentration procedure. There is no permanent secure building, unattended attack engine, free spell repertoire or additional work crew.

NEW exact visibility completion: Watch produces an ordinary visible outline of the occupied silhouette where the observer has a real sight path. This specific marker can supply that position through this parcel's Veil, including when the bearer separately has Invisible, but it does not make the bearer itself seen for a source requiring sight of the actual creature and does not remove Invisible's combat modifiers. Actual total cover hides the outline. Recognition is a fixed cast list, not shared sight or an extra targeting channel. A removed Watch application on one body cannot regenerate during its already-spent family entry interval; future genuinely new eligible entries follow the source-removal scope and live parent. Outside initiative use fixed six-second entry intervals, preserving a spent current interval when initiative begins; do not reset on recast.

## Preserved printed effect
- Original name: Guards and Wards
- Original placements: [{"name": "Guards and Wards", "school": "Abjuration", "level": 6, "summary": "Fill area with multiple defensive spells."}, {"name": "Guards and Wards", "school": "Universal", "level": 6, "summary": "Fill area with multiple defensive spells."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Forbiddance
**Spell ID:** `forbiddance`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 6 | 11 | 13 |
| Druid | Abjuration | 6 | 11 | 13 |
| Mage | Abjuration | 6 | 11 | 13 |
| Wizard | Abjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action, 60 feet, V/S/F and an area damaging creatures of specified alignments; preserve Instantaneous as incomplete metadata. NEW choose one perceived center within range/line of effect and one to three complete alignment pairs from the nine combinations of Lawful/Neutral/Chaotic and Good/Neutral/Evil. These are selection categories in the current canonical two-axis system, not judgments created by this spell. The choice is fixed for the cast. Create a stationary 20-foot-radius sphere, concentration up to 60 elapsed seconds, with center line of effect. No planar travel prohibition, sacred ground, permanent consecration, faction restriction or creature-type exclusion is added.

At formation, and on later actual creature regular STARTs inside or actual entry into the live field, the Director privately compares the recipient's current actual mechanical alignment record with the selected complete pairs. Both actual axes must be recorded and exactly match a selected pair; an unknown axis is not guessed from behavior, ancestry, faith, faction, corruption or appearance. A genuinely applicable active alignment overlay participates under its own source rules. Protection that specifically prevents this source from using alignment for its predicate prevents the matching application within its stated scope. A Divination-only information protection does not automatically block this Abjuration damage spell, and the spell does not reveal the protected data to its caster. No valid recorded match means no damage attempt, not a public declaration of neutrality or alignment.

Each matching exposed creature makes WIS against the original spell DC for NEW 3d8 force damage, half rounded down on success. Roll one shared raw amount for recipients at the same actual event; different genuine later events can roll again. No radiant/necrotic or deity preference is inferred. Across all Forbiddance applications/casters, each target has at most one save/damage opportunity per numbered round, including creation; choose the earliest eligible operative source for simultaneous overlaps. Record the exposure before the save/damage so immunity, success or prevention does not grant another attempt. Initial nonmatching eligibility consumes no exposure, but a later genuine alignment change requires an actual future START/entry event, not an immediate extra pulse. Forced movement and teleport arrival can constitute actual entry, without extra damage from repeatedly crossing in one round.

Outside initiative, formation can have its eligible first pulse and later occupants have six-second spell pulse opportunities using the same shared interval exposure. Map the next unresolved periodic opportunity to the next actual regular START on entering initiative, without an additional transition pulse. An owner-attached recipient uses its real regular attached-phase start for this stated spell-only tick; if no phase exists the original six-second spell schedule continues without creating an Action/turn. Suppressed opportunities are spent without queued damage; suppression ending is neither entry nor START. No hard-control claim, compelled conduct, movement barrier or continuing damage condition is added.

The source supplies no readout of who matched, saved, was immune or had an unknown/protected alignment. Ordinary actually visible effects remain observable and may support ordinary inferences; the spell does not guarantee secrecy against observation or authorize an additional alignment diagnostic. Leaving the area stops further eligibility without ending the field. Concentration loss, expiry, removal or a newly formed same-caster replacement ends it under the actual source rules. All ordinary damage consequences remain after ending, with no permanent alignment change, historical rewrite, extra corpse effect or claimed cosmology.

CURRENT ALIGNMENT ORDER: evaluate the real underlying alignment history/AP-AS-01 first, then the earliest eligible active AC4 Lock/Anchor snapshot last on each locked axis under AC4-ALIGN-01. Leaving or suppressing that locking source exposes the then-live underlying value; it does not resurrect an old snapshot. A later Purge remains a real paid record beneath the lock and changes no locked effective value until the lock is inactive. For each future qualifying exposure read the actual effective complete pair at that event, never infer undefined axes.

NEW ROOT CHECKPOINT: when a qualifying recipient has actually claimed the family exposure and reaches damage resolution, create one root for that recipient/event with dealer=this field's actual caster; snapshot that character's then-current unsuppressed Null Veil. Shared raw dice do not merge roots. Each later eligible pulse is a genuinely new root; the original field creation does not permanently fix every future pulse's Veil flag. Pure redirection/transfer descendants inherit the existing root. A suppressed event creates no damage packet and supplies no deferred pulse. This source-only periodic attached-phase checkpoint creates no companion turn, Action, Reaction or rest clock.

## Preserved printed effect
- Original name: Forbiddance
- Original placements: [{"name": "Forbiddance", "school": "Abjuration", "level": 6, "summary": "Area deals damage to creatures of specific alignments."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Resonance Seal
**Spell ID:** `resonance-seal`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 6 | 11 | 13 |
| Druid | Abjuration | 6 | 11 | 13 |
| Mage | Abjuration | 6 | 11 | 13 |
| Wizard | Abjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action, 60 feet, V/S/F, locking one magical effect in place and preventing dispelling by normal means. Preserve Instantaneous metadata. NEW select one individually perceptible ongoing magical application with a discrete spatial origin/area and actual dispel interface, perceived within range/line of effect, owned by you or explicitly permitted by its actual current source owner/controller. A fixed effect can qualify even if it currently has no movement permission. A permanently creature/carried-object-attached effect is excluded rather than immobilizing its bearer. A class engine, whole creature, permanent item enchantment without a separate eligible ongoing application, completed instantaneous result or nonexistent aura is not a target. No rank cap or resistance roll is added once those real permissions are present.

NEW maintain one nonconcentration Seal for up to seven elapsed days, ending earlier when the protected application ends. Fix that application's spatial origin at its actual current world position. It loses authorized relocation/recentering while sealed, but keeps its actual source-permitted radius/shape evolution and unrelated effects; anchoring is not a frozen event clock or expanded shape permission. The parent's owner, rank, DC, concentration, duration, recipient set, charges, pulses, resource history and ordinary source-ending permissions remain. A one-minute parent still ends after its original minute. The Seal neither maintains another caster's concentration nor prevents their voluntary ending, source destruction, legitimate expiry or an independently specified non-dispel ending.

Normal dispelling cannot end the protected application or this Seal itself while protection operates, including an otherwise eligible Greater Dispel. A source explicitly overriding nondispellable/anchored protection retains only its real written scope; no high-rank automatic bypass is invented. Counterspell can stop the Seal before establishment. Actual suppression is distinct: it suspends the Seal's protection/anchor while the original seven-day clock continues. A separately legal dispel can then affect an otherwise eligible parent or Seal only if it can actually resolve through that suppression environment and its own normal rank/target rules. This creates no permission to cast inside antimagic or assume that a low-rank dispel can remove a rank-six Seal. If a mobile parent moves while the Seal is suppressed, on resumption the Seal fixes its then-current origin, not a backward teleport to the old point; this is a NEW specific resumption rule, with no renewed duration or lost-history reset.

One active Resonance Seal per caster. A genuinely established new Seal replaces that caster's old one, freeing the old parent's movement/ordinary dispel eligibility without ending it. Hidden failure/countering creates no replacement. The caster may end their Seal with an Action while personally perceiving its anchor within60feet and line of effect. Separate other casters' Seals retain their own original deadlines; fixing the same origin supplies no cumulative protection rank or added duration. A genuinely conflicting attempt to establish a second origin for an already immovable effect does not move that effect; its current actual position is the only admissible anchor.

NEW exclude Resonance Seal, Spell Seal and Resonance Anchor themselves from this spell's eligible targets, preventing cross-protection loops among these three families. The earlier Spell Seal proposal remains unadopted and unchanged. This draft proposes no automatic amendment to it: any later reciprocal exclusion requires its own explicit joint disposition. Only Resonance Seal targeting is defined here. Reviewed Resonance Anchor is unchanged and keeps its own normal dispellability. Compared with the distinct proposed Spell Seal, Resonance Seal has actual spatial anchoring, source-owner permission, one active caster slot and a seven-day maximum; Spell Seal proposes broader application targeting and a24-hour nondispel-only benefit. Neither is silently merged or renamed. No body, RP, charge, missed pulse, old effect or frozen lifetime is created by either name.

CURRENT TRANSPORT/CLOCK LIMIT: the target is one eligible spatial magical application, not a body, vehicle, entire plane or generated Banishment cell. Sealing an eligible portal anchor cannot suppress a mandatory independent closure/expiry or preserve its destination beyond the portal source. It cannot keep ordinary Banishment open or stop BAN-CLOSE-03. A later actual suppressor must establish suppression of this Seal before the protection ceases; mere intent, caster entry into an unrelated field, or a purported high-rank dispel does not supply that premise. Suppression does not by itself prove that a dispel can operate in the same location. AC5 Antimagic Field (Lesser) and Greater Dispel are now jointly accepted. Apply AC5-ANTIMAGIC-IO-04: a Greater Dispel operation at an antimagic-suppressed Seal or parent locus is itself suppressed; the target-field self-exemption applies only to an operation targeting that Antimagic field. Snapshot all operations before any removals, with no same-cast rescan. Suppressing Seal therefore does not by itself establish a successful dispel route.

CURRENT EXECUTABLE REMOVAL CONCLUSION: apply AC6-SEAL-REMOVAL-01. The accepted Lesser Antimagic + Greater Dispel combination does not create a successful selective suppress-then-dispel route for Seal/parent at the same suppressed locus. Wizard class Dispel /cards/19 is a rank3 spell, not a magical nonspell.

## Preserved printed effect
- Original name: Resonance Seal
- Original placements: [{"name": "Resonance Seal", "school": "Abjuration", "level": 6, "summary": "Lock a magical effect in place; it cannot be dispelled by normal means."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Planar Barrier
**Spell ID:** `planar-barrier`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 6 | 11 | 13 |
| Druid | Abjuration | 6 | 11 | 13 |
| Mage | Abjuration | 6 | 11 | 13 |
| Wizard | Abjuration | 6 | 11 | 13 |

## Complete current procedure
### Activation And Geometry

KEEP Abjuration6, Action,60feet,V/S/F,base13RP and concentration up to60elapsed seconds. NEW choose a fixed vertical rectangular wall up to30feet wide and15feet high, with1foot thickness, resting on actual ground. Choose its full position/orientation before commitment; every point must be within60feet and caster line of effect at formation. Width and height use whole5foot panels, producing at most18panels. No curved dome, moving wall or physical material is supplied. The initial volume must be free of creature bodies and solid terrain; known conflict fails preflight, a hidden conflict discovered at resolution defeats the whole paid formation. The wall is visible but transparent to ordinary sight/sound and does not itself supply cover.

### Eligibility

NEW PB-PRED-01, scoped only to this wall: a creature qualifies if an actual operative source explicitly classifies it as extraplanar, or an actual established native-plane relationship places its native plane elsewhere than the wall's plane. A mere current visitor is not assigned a native plane. A record that expressly changes/suppresses that classification is honored for its stated duration. Without either affirmative established basis, this wall imposes no blocking branch; that operational absence is not proof the creature is native or non-extraplanar. Elemental, Fey, Fiend, Humanoid, summoned, outsider and extraplanar are not interchangeable labels. The Director may record a genuinely NEW campaign creature classification explicitly before play, but may not claim it was recovered from cosmology or infer it from a hidden soul theory.

### Physical Crossing

An operative panel blocks a qualifying creature's attempted voluntary or forced physical crossing at its boundary, including that body carried, dragged, grappled or ridden by another. Every separately transported creature retains its own eligibility; hiding a qualifying passenger under a cloak does not turn it into gear. Stop the actual crossing transaction before any qualifying body intersects the panel; no part is severed, squeezed through by changing its name, or left behind without an independently legal release. Movement used to reach the boundary remains spent; impossible remaining movement is not performed. A nonqualifying carrier can release the passenger through its actual available action and move alone if then legal. Nonqualifying bodies, ordinary objects, air, sound and actual attacks pass under their own rules. Going around a real edge remains possible. The wall deals no damage, imposes no extra save and grants no free force or opportunity attack.

### Falling And Placement

NEW selective-wall limitation: it supplies no horizontal support. Unsupported falling continues through its top/bottom and uses the ordinary real Falling history; the wall does not become a one-foot-wide platform or halt a Fall Marker. A lateral forced crossing can stop while the creature continues to fall along its actual remaining vertical trajectory. Actual other terrain/support still matters. The wall does not reserve a berth or eject a body when eligibility changes. If an existing body becomes qualifying while intersecting a panel, that entire5x5panel becomes pending for that wall until no qualifying body intersects it; it supplies no blocking while pending. Once clear it resumes prospectively, with no crushing, relocation, missed action, damage or refreshed duration.

### Teleport And Terminal Return

The wall checks an actual transport destination footprint against its operative thickness for qualifying creature bodies; a destination that intersects is barred by this scoped magical endpoint-prevention rule. A fitting destination beyond the wall does not cross a fictitious physical path and is permitted unless another actual rule prevents that transport. An origin alone touching the wall does not bar leaving. Apply each transport source's normal atomic failure/payment rule. Ordinary Banishment's accepted BAN-CLOSE-03 terminal return expressly overrides endpoint transport prevention: this wall cannot keep that ended cell open. It does not remove real terrain or other bodies. If that mandatory return legally places a qualifying body in the wall thickness, the occupied panel becomes pending under the rule above; no general voluntary-transit bypass is granted.

### Suppression And Ending

The wall is a nonphysical ongoing rank6 spell with one parent source and its explicit panels. Local suppression makes intersected panels inactive while its original clock and concentration continue. At resumption, a panel occupied by a qualifying creature remains pending until clear. Entry/resumption is not an attack or a new casting. Losing an underlying ground support invalidates the panels depending on it for the remainder of this cast; it does not move or drop a physical wall. One active Planar Barrier per caster; normal concentration commitment and successful replacement rules apply. Expiry, concentration ending or eligible whole-source dispel ends all panels. No saleable fragments, teleport, planar knowledge or permanent ownership boundary remain.

### Current Panel Precision

Fixed 5-foot panels are the authored wall cells. Local suppression records the exact clipped portion of each panel that the suppressor actually covers; it does not convert the sphere into rectangular suppression. On resumption, previously suppressed clear portions return. Any exact suppressed portion intersecting a qualifying body remains absent until clear; unsuppressed portions were never removed. No crushing/ejection or tactical reselection is created.

## Preserved printed effect
- Original name: Planar Barrier
- Original placements: [{"name": "Planar Barrier", "school": "Abjuration", "level": 6, "summary": "Create a wall that blocks extraplanar creatures."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Corruption Purge
**Spell ID:** `corruption-purge`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Abjuration | 6 | 11 | 13 |
| Druid | Abjuration | 6 | 11 | 13 |
| Mage | Abjuration | 6 | 11 | 13 |
| Wizard | Abjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action, 60 feet, V/S/F, instantaneous removal of ALL corruption effects from an area OR creature. NEW before commitment choose creature mode with one perceived creature in range/line of effect, or area mode with a fixed20-foot-radius sphere centered at a perceived point in range/line of effect. The area includes actual environmental effects and every creature occupant with center line of effect, including caster/allies, without requiring individual perception. The criterion is an actual current canonical mechanical source expressly identifying the active record as Corruption. Appearance, evil alignment, faction, ancestry, necrotic damage, ordinary poison or a suggestive name does not supply that predicate.

Creature mode: a willing recipient receives automatic removal; an unwilling recipient makes CON against the spell DC, success resisting all of this cast's removal on that creature, failure allowing the following purge. Area mode applies the same independent willingness/save procedure to each creature occupant, while environmental records do not receive a creature's save. Resolve hidden willingness/protection/records only after legal costs, without an extra diagnostic report. For an admitted creature, end every actual qualifying removable Corruption effect currently on it, including all ordinary Corrupted condition sources and major nonintrinsic Corruption applications. This is not limited to one record or only minor records like Corruption Cleanse. A source calling its corruption permanent or giving it no ordinary expiry does not alone make it immune to this expressly stronger purge.

An explicit source-specific removal exception still governs: a unique record stating that only a named cure can remove it, that it cannot be cleansed by magic, or another actual protection applicable to this purge is not silently overridden by a generic higher rank. Keep the record and its exact unmet exception; do not relabel it minor, remove its hidden parent or claim whole-person purification. Innate ancestry, a class engine, intrinsic Oracle Curse/Burden and actual physiological changes that are now completed consequences rather than ongoing removable effects are not reclassified as targets. Corruption/Unity Exposure numeric tracks are not automatically active effect records; this spell supplies no unprinted track reset, historical alignment reversal, trait removal, HP healing, Wound cure, stabilization or resurrection. A separately actually purgeable track source could supply its own explicit procedure, which must be recorded rather than inferred.

NEW for ordinary spatially divisible environmental Corruption, remove the operative intersection inside the sphere while retaining the same source's outside extent and actual remaining clock. This expressly broader area completion is separate from lower Cleanse's minor/whole-extent rule. A genuinely indivisible or specially protected environmental source needs its own actual removal eligibility and complete required extent; an overlapping corner does not destroy an entire distant dungeon engine. Remove all admitted environmental records in the snapshot, not merely one chosen symptom. Source-specific automatic future reapplication retains its actual schedule; the purge grants no grace period, continuing aura or immunity and does not destroy a separate generator unless that generator itself was an eligible selected effect. Record the removed portion so merely redrawing the surviving area cannot replay a historical removed application without a genuinely authorized new one.

Take one pre-removal snapshot after interrupts and apply its real source dependencies in stable source/application order. If removing a parent already ends a captured child, do not process/award it twice or expand the snapshot to new recipients behind a disappeared barrier. Removing a symptom cannot infer that an unselected major cause ended. Actual observed relief remains visible evidence, but there is no enumerated source, alignment, soul or private diagnosis delivered to the caster. After the instantaneous purge there is no ongoing spell to dispel backward; real consequences and protected records remain. Each new cast pays actual costs and can affect genuinely newly present qualifying records, without manufacturing a new source or a universal theory of Corruption.

CURRENT NULL BOUNDARY: Null Veil is its own accepted setting record with three exact named purge routes; it is not an ordinary Corruption application merely because it is harmful. This spell is not one of those routes and adds no fourth route. Preserve Veil, its exposure history and source protections, as well as numeric Exposure, Wounds and the intrinsic Oracle Curse. An actual source expressly creating a separate removable Corruption rider on the same character remains independently eligible: keeping Veil does not shield unrelated valid Corruption effects.

## Preserved printed effect
- Original name: Corruption Purge
- Original placements: [{"name": "Corruption Purge", "school": "Abjuration", "level": 6, "summary": "Remove all corruption effects from an area or creature."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Summon Greater Air Pet
**Spell ID:** `summon-greater-air-pet`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 6 | 11 | 13 |
| Mage | Conjuration | 6 | 11 | 13 |
| Shaman | Conjuration | 6 | 16 | 13 |
| Wizard | Conjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action, 60 feet, V/S/F, concentration up to one minute, HP65, AC18,2d8 wind slash and50% miss chance against projectiles. NEW form one Medium Elemental in a perceived unoccupied legal whole-body space within range/line of effect. Base body mass40lb; STR10,DEX18,CON14,INT4,WIS10,CHA6; Fly40 with Hover and walk30. Ordinary sight/hearing, no darkvision or unprinted immunities/resistances. All six saving throws use original source-owner current PB as total modifier; other checks use listed ability modifiers without proficiency. No hands, tool operation, passenger support or cargo-carriage permission is granted by the wind body. Actual source-qualified maximum-HP modifiers apply to base65; healing cannot refill an ended body or reset its identity.

Use one actual owner BA command within60feet with owner perception/line of effect and a spoken order that the pet can hear. It understands only those simple command meanings, with no learned speaking language or sensory feed. In its owner's attached phase it may move and make one melee spell attack at reach5feet using the original casting source's current attack modifier. On hit deal2d8 slashing with no ability damage bonus; wind is the depiction, not a new damage type. Apply normal attack critical/defenses. It does not copy lower Air Pet's expressly printed two attacks. The real command/offensive allowance can support this attack on the creation turn only if still available; the casting Action itself supplies none. Otherwise it only moves defensively and Dodges while capable.

NEW projectile defense applies to each genuinely separate projectile whose direct impact would otherwise hit this pet: arrows, bolts, thrown weapons and actual source-described magical missiles traveling to it. A mere beam, touch, nonprojectile magical attack, area blast, ambient damage or source that only looks like a projectile without that actual mechanism does not qualify. After the projectile's actual hit determination and legal attack-roll rerolls/pre-hit interruptions, but before damage/on-hit riders, roll one fair d2 for this projectile/pet event:1 turns that direct hit into a Miss,2 leaves its determined hit/critical intact. Already-missed attacks roll no chance. A natural20 hit still faces this specific miss chance; a genuinely explicit source that ignores miss chances overrides it within scope. An automatic-hit projectile also receives this defense unless that source explicitly bypasses it. No attack/save/check reroll feature automatically rerolls this separate d2 unless its actual wording covers that chance roll.

Keep one chance result per projectile/defender event lineage. Multiple damage components of one projectile share it; a redirected/copy callback cannot reroll it as a new hit on the same body. Genuinely separate projectiles have separate chance results, even if their source used one attack roll. If a legitimate later effect actually reopens the original attack determination, retain the already-resolved chance for that same projectile rather than drawing until favorable. Deflection cancels that direct hit and its hit riders, not an independently legitimate area explosion at a real miss/scatter position specified by the original source. This grants no general explosion immunity, half damage, disadvantage or protection to other creatures. Multiple instances of this same defense do not add extra50% rolls.

One Greater Air Pet per caster, separate from lower Air Pet's identity but sharing all owner commands/offense. A genuinely formed new one replaces the old; ordinary concentration commitment may already have ended it. Ordinary non-Null damage reaching zero HP ends this finite body with no corpse, item, harvest or free resummon. Qualifying Null damage instead preserves this same source/body at NullDisabled0: Incapacitated, Speed0, no Actions/Bonus Actions/Reactions/commands. Its actual Hover trait prevents a fall solely from Speed0 while the body/source remains; independent source ending still removes that support. Further qualifying Null hits cannot refresh it. Independent expiry, concentration end, replacement, dismissal or actual source removal still ends it, whether disabled or positive HP. NEW full suppression of this created source ends this pet immediately, rather than storing an intangible body for return; narrowly scoped rider suppression affects only that rider. Any real object physically resting against/carried externally with it loses that support at its actual position under ordinary support/Falling rules. No weather control, unlimited air, wind cargo transport or planar-origin conclusion follows from this profile.

NEW AC6-HEAL-TARGET-02: while this created finite creature body exists, expressly treat Greater Air Pet as a living ally/creature for otherwise legal ordinary HP healing, including actual Cleric Healing Rite. This is a scoped new target extension, not a claim about biology, soul, resurrection, native plane or applicability to every summon. Healing above0 ends this body's NullDisabled state, without resetting source deadline, HP maximum, conditions or command histories. It grants no free healing, rest pool or corpse/repair route. AC4 Water Pet/Envoy and pending AC5 Fire Pet/Champion extensions do not automatically grant this one.

For a projectile d2, actual Fate Coin can replace that one die only after its face is available to the reacting player, with a held available coin, real Reaction, perception of the actual local impact event within30feet/LoE, and the shared Mark Omen/Fate Coin original-roll-lineage guard unused. The projectile's earlier attack roll and the later d2 are separate roll events; multiple damage components are not multiple d2 events. A secret Director die is not revealed by the coin. A legal d2 replacement commits once and its final face owns the same event; a result1 removes the direct hit and its on-hit riders even if the original attack was natural20. A separate source-defined explosion uses its own real position/save and gets no d2 merely because a projectile delivered it.

NEW suppression choice retained for joint review: full suppression of the Greater Air Pet created manifestation ends it. This differs from accepted AC4 Water Pet and the current pending AC5 Fire Pet pause model; it is deliberately source-specific and requires actual GPT agreement. Merely suppressing its projectile rider removes that defense temporarily without ending the body, while its deadline continues. The dealer of a real wind-slash root is the Pet, not its Veiled owner.

CURRENT AC6 SUPPRESSION/NULL COMPLETION: use AC6-SUMMON-SUPPRESS-01 instead of any older early-ending full-suppression sentence. Qualifying Null damage at 0 leaves the same occupying NullDisabled0 body while source concentration lasts. AC6-HEAL-TARGET-02 supplies only the narrow HP-healing target predicate for this profile. Its Wind Slash damage dealer/root owner is the Pet body itself, not the owner.

## Preserved printed effect
- Original name: Summon Greater Air Pet
- Original placements: [{"name": "Summon Greater Air Pet", "school": "Conjuration", "level": 6, "summary": "HP 65, AC 18, 2d8 wind slash, 50% miss chance vs projectiles."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Elemental Warp Field
**Spell ID:** `elemental-warp-field`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 6 | 11 | 13 |
| Mage | Conjuration | 6 | 11 | 13 |
| Shaman | Conjuration | 6 | 16 | 13 |
| Wizard | Conjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action, range10feet, V/S/F and allies within10feet gaining resistance to elemental damage. Preserve Core Instantaneous as a metadata conflict. NEW the spell creates a10-foot-radius sphere centered on and moving with the caster's actual body, concentration up to60elapsed seconds. It is not a chosen remote center or a fixed ten-foot diameter. A recipient must actually be an ally of the caster at the damage event, inside the real sphere and have caster-to-recipient line of effect. NEW include the caster as its own eligible ally for this benefit. A false declaration of friendliness does not change actual relationships, and the effect grants no private allegiance readout, loyalty or standing change.

NEW bind elemental to the native five-type set used by the reviewed Conjure Elemental Lance: acid, cold, fire, lightning and thunder. A qualifying recipient gains resistance to all five while eligible, not one selected type. Force, necrotic, radiant, psychic, poison and ordinary physical types are not elemental solely because a magical spell, elemental creature or colorful weapon caused them. A mixed packet uses each actual damage type independently. Apply the existing single resistance step for the qualifying component with normal rounding and genuine vulnerability/immunity rules; do not halve again for another Elemental Warp Field, armor resistance or multiple allies sharing the aura.

Evaluate actual position, relation and line of effect at the recipient defense stage of that real damage event. Entering the aura grants future eligibility immediately; leaving or losing actual ally status removes it immediately, with no lingering minute on each creature. Moving the caster changes the live sphere but neither retargets already resolved damage nor refunds HP. A damage-sharing branch follows the reviewed transfer stage: if that branch normally applies the final recipient's defenses, use that recipient's current eligibility; a branch already post-defense gains no second mitigation merely because it arrives inside this field. The source supplies no new transfer, split, reflect or retaliation permission.

The caster need not spend later Actions to maintain the aura beyond actual concentration. If an actual Incapacitated/death state ends that concentration, the field ends through that ordinary rule; the spell does not invent its own unconscious-persistence exception. Temporary inability to speak or an ordinary condition that does not actually end concentration is not automatically expiry. Suppression suspends the locally affected benefit while the original deadline/concentration continue; when applicable suppression ends, only the still-live aura returns. Missed resistance cannot be applied retroactively to damage that already resolved. The field is visible only to senses that can actually perceive such magical effects; no automatic illumination or concealment is added.

Different casters can maintain independent fields, and each retains its actual deadline and source. Overlap gives resistance once, not immunity, a pool of reduced damage, refreshed temporary HP or a longer shared duration. One active field per caster; ordinary concentration commitment and genuinely formed replacement apply. Actual removal, expiry or concentration loss ends that source's benefit, exposing any separately still-valid resistance source. Warp is only part of the name here: no teleport, spatial displacement, extra movement, rest, healing, charge refill or RP regeneration is printed or proposed.

This defense creates no damage root or new damage-dealer identity. Real pre-defense Bloodbond/Veinlock sharing splits the finalized raw components first; each resulting recipient uses its own actual eligibility once. Actual post-defense transfer such as Aegis follows ordinary type defenses and pure prevention, then carries its existing types/root into the protector without a second mitigation/prevention step. Only the actual transfer source supplies rounding, selection, cap, trigger and resource restrictions; the field itself supplies none.

## Preserved printed effect
- Original name: Elemental Warp Field
- Original placements: [{"name": "Elemental Warp Field", "school": "Conjuration", "level": 6, "summary": "Allies within 10 ft gain resistance to elemental damage."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Chain Arc
**Spell ID:** `chain-arc`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 6 | 11 | 13 |
| Mage | Conjuration | 6 | 11 | 13 |
| Shaman | Conjuration | 6 | 16 | 13 |
| Wizard | Conjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action, 60feet, V/S/F, instantaneous lightning arcing randomly across six targets for3d8 damage. NEW declare one initial perceived creature within60feet and line of effect. It can be ally or caster if otherwise legal; no object, corpse or fake image is an eligible creature target. After the counter/interruption window revalidate that initial target. If it is now illegal, the paid cast ends with no chain and no replacement selection. Otherwise take one pre-damage snapshot of actual creature identities, positions and arc line-of-effect geometry. The chain has at most six distinct creature identities total: the first target plus at most five random successors, never six hits on the same body.

For each successor, form the finite candidate set of unvisited actual creatures within30feet of the immediately previous selected creature's snapshotted position and with line of effect from it. Include allies and the caster when eligible; no selective exclusion after results. NEW successors need not be perceived by the caster or within the caster's original60foot range, because this spell's actual random arc selects from its local geometry. This is a source-specific targeting extension, not a general permission for hidden-target spells. Director-held hidden identities can be candidates without revealing a roster or new diagnostic to the caster. Order the candidate set by stable preexisting encounter/body identity, assign indices1..N, and draw one uniform integer from1..N using a declared fair1dN/digital die. Select that one index once. This is a finite draw, not repeated d20 rejection until a favorable or legal result appears. A known empty set ends the chain immediately; do not invent targets or revisit an earlier identity to reach six.

Build the entire chain in that snapshot before any damage. Remove each selected identity from later candidate sets, even if its body occupies multiple squares. The recorded random selections and order cannot be changed after observing saves, HP loss or immunity. Each selected creature then independently makes DEX for a shared rolled3d8 lightning, full on failure or half rounded down on success before defenses. A selected creature's successful save, lightning immunity, zero damage or death from its packet does not sever already-established later arcs. No attack roll, critical damage, extra damage from metal, conductive-water expansion, stun, blindness or recursive fork is added. A creature actually removed before its own already-selected packet by an independent legal immediate response follows that response's real effect; no replacement or fresh random draw is supplied, and the other pre-established selections remain.

The draw method is transparent, but a public list of hidden candidates, their number, exact positions, alignment or defenses is not a spell benefit. Ordinary visible lightning/harm remains observable, and the spell does not promise that an affected hidden creature leaves no evidence. With fewer available targets the cast simply affects fewer than six. Its longest theoretical six-body straight sequence is initial60plus five30foot jumps, but every actual hop still needs the snapshotted geometry; no arbitrary farthest endpoint is targeted directly. A genuine subsequent cast pays again and forms a new chain; copies/echoes obey their actual event/source permissions rather than reusing a random choice as an extra hit. After instantaneous resolution there is no continuing chain, charge, creature, storm or lingering field to dispel. This spell remains distinct from the proposed freely selected four-target10d8 Chain Lightning; neither damage amount nor selection rule is imported from that separate identity.

NEW ROLL/ROOT COMPLETION: each successor draw is a distinct original die event, completed and any permitted replacement resolved before that successor is committed and the following candidate set is built. A legal Fate Coin replacement of a visible physical1dN changes this one index using the same original candidate ordering; never rebuild the candidate set to favor its new face. It cannot revisit the same selection after consequences or reroll a hidden die. Actual perception/30feet/LoE and the single Mark Omen/Fate Coin lineage guard remain prerequisites. A digital uniform draw is not automatically eligible for a feature expressly limited to a physical die; record the method and apply that feature's exact interpretation rather than grant new information or authority.

After all legal selections and their roll replacements are final, create the instantaneous cast's recipient damage roots together before the first recipient damage packet: each has the caster as dealer, that caster's actual Veil state at this common checkpoint, its own recipient identity and the same cast lineage. Subsequent pure transfers retain those flags. Independent events later removing a selected recipient can prevent its pending packet but cannot redraw or erase the other already-established roots/arcs. No actualDamageDealt, Wound, death or resource trigger occurs merely because an identity was selected or a root allocated.

CURRENT FAIR-DRAW COMPLETION: apply AC6-CHAIN-RANDOM-01. Stable candidate arrays are fixed before each physical/random draw; allies and unseen locally eligible creatures remain in the array. Fate Coin can reroll a public physical selection die only when its actual reaction/guard predicates are met. No retry-until-valid and no post-damage redraw.

## Preserved printed effect
- Original name: Chain Arc
- Original placements: [{"name": "Chain Arc", "school": "Conjuration", "level": 6, "summary": "Jumping lightning: 6 targets, 3d8 damage, arcs randomly."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Conjure Skybrand Weapon
**Spell ID:** `conjure-skybrand-weapon`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 6 | 11 | 13 |
| Mage | Conjuration | 6 | 11 | 13 |
| Shaman | Conjuration | 6 | 16 | 13 |
| Wizard | Conjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action, 60feet, V/S/F and a floating weapon making two attacks per round for1d12 lightning. Preserve Instantaneous metadata. NEW create one nonphysical visible weapon-shaped magical effect fitting a5-foot cube at a perceived unoccupied point within range/line of effect, concentration up to60elapsed seconds. Its appearance is chosen from ordinary weapons the caster knows, but it is not a held/equippable item or actual creature/object with HP. Ordinary weapon damage cannot destroy it; an actually eligible dispel/suppression or source-ending effect can. It provides no collision, support, physical cover, flanking body, grip, cargo, trade material or transferred weapon proficiency.

NEW command it using the owner's real Bonus Action during their regular turn, while perceiving it within60feet and line of effect. It shares the global companion/device command and offensive allowance even though it has no creature chassis. One command directs a route of up to30feet of effect movement and one offensive activation containing exactly two separate melee spell attacks, each with reach5feet from its actual current point. Use original source-owner current spell-attack modifier; each hit deals1d12 lightning with no added ability damage. Ordinary attack critical doubles that attack's die only. The two attacks are the printed exception inside one offensive Action, not two commands, two independent turns or two offensive allowances. Choose the first actual legal perceived target when issuing the command; the order may identify a second target then or direct the second attack at the same one. No new target unknown to the owner is discovered by the blade.

Execute only in the owner's actual attached phase after the whole turn. The blade may split its one30foot movement budget before/between the two attacks, following the declared legal route. It can float through open three-dimensional space without support, but cannot pass solid barriers or leave its actual source-authorized movement path; no teleport or incorporeal wall passage is supplied. It may overlap an actual creature's space as a nonphysical effect without collision, but must have its own real attack line of effect and actual5foot reach at each attack. Recheck selected target availability then; an invalid second target yields no second attack and no new target chosen from hidden outcomes unless the original legal order already supplied that target as its alternative. A missed/invalid attack never frees unused offense for another companion or supplies a third attack. Separate hit packets keep their own defenses and source-trigger restrictions.

The creation turn can use an actually unspent BA command and global offense, but the creation Action gives no free pair of attacks. Without a valid command it stays at its current point, with no autonomous Move/Dodge, opportunity attack, Reaction, attack on entrants or maintained damaging aura. Owner incapacity after a valid issued command does not itself revoke it, but genuine concentration ending/removal does. Moving beyond60feet from the owner leaves the effect present for its remaining clock but unavailable for a new command until the actual command geometry is legal again. No remote senses or extra body lets the caster aim at unseen targets.

At most one Skybrand per caster. A genuinely formed replacement ends the old and retains owner command/offense history; concentration commitment may already have displaced the old. Suppression makes the affected effect/attacks unavailable while its original position, used attacks and deadline remain; a queued activation spanning unavailable execution is lost without a refund. Resumption adds no attack/movement or new phase. Expiry, concentration loss or actual removal ends it without dropping a saleable sword or damaging nearby creatures. No creature death, item destruction, harvest, resource recovery or passive weather/lightning effect is generated by its ending.

NEW ROOT/ASSET COMPLETION: Skybrand is an effect, not an independent creature dealer. Each of its two real attacks that reaches damage resolution creates its own new damage root, dealer=the actual original caster, evaluating that character's actual unsuppressed Null Veil at that checkpoint. Thus a genuine independently legal Veil change between attacks would affect the second new root, but the spell grants no such change, extra Reaction, mid-action turn or one-hour exposure shortcut. A later ordinary owner START ending that owner's accepted Veil suppression affects roots from a later command normally. Damage descendants retain their existing root.

Suppression rechecks at each actual effect movement/attack checkpoint. If an already-issued activation is unable to execute because its effect is suppressed, its remaining movement/attacks expire in that attached phase; they cannot resume or move to another companion when suppression ends. If a first attack resolved and the source then truly ends, only that already-resolved outcome remains; the second is absent, not a free offense token.

## Preserved printed effect
- Original name: Conjure Skybrand Weapon
- Original placements: [{"name": "Conjure Skybrand Weapon", "school": "Conjuration", "level": 6, "summary": "Floating weapon makes 2 attacks/round for 1d12 lightning."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Planar Ally (Greater)
**Spell ID:** `planar-ally-greater`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 6 | 11 | 13 |
| Mage | Conjuration | 6 | 11 | 13 |
| Shaman | Conjuration | 6 | 16 | 13 |
| Wizard | Conjuration | 6 | 11 | 13 |

## Complete current procedure
### Casting And Formation

KEEP Conjuration6, Action,60feet,V/S/F,base13RP and one hour of extraplanar assistance. NEW no concentration; exactly3600elapsed seconds from successful formation. Choose one perceived unoccupied actual10x10foot whole-body space with at least10feet vertical clearance in range and line of effect, on support capable of the body plus actual admitted cargo. Known illegality fails preflight; hidden or intervening invalidity defeats the paid formation without a substitute location. A countered cast creates no replacement. A successful new Greater Planar Ally replaces the caster's previous Greater Planar Ally, wherever it is, conserving real property.

### Identity And Role

NEW explicitly form the complete summon-only profile AC6-GREATER-PLANAR-ALLY-PROFILE-01. This is a new finite creature identity, not a transport/copy/conscription of a named existing person or an automatic grant to choose any printed CR6 monster. It preserves the source's CR6 assistance role as a design target. Eight actual CR6 entries in the bounded67-entry source candidate are preserved for comparison; none is treated as operationally approved or extraplanar solely from its type. The proposed120HP/AC17/two2d8+4 profile and intended challenge role need numerical playtesting. Extraplanar is an explicit source tag; no specific home/native plane or soul has been invented. Formation is this spell's creature-creation event, not traveler transit; a rule preventing actual planar travel does not automatically suppress creation unless its exact text covers it.

### Command And Assistance

Use the actual owner-wide Bonus Action command during the owner's regular turn, within60feet, with owner perception/line of effect and a command the ally can actually hear. Execute one movement budget and one selected legal Action in the attached phase after the entire owner turn. A valid offensive command permits its two printed strikes within one offensive Action, not two owner commands. Choose legal targets and any lawful alternatives from what the owner actually perceives when commanding; revalidate reach, target and line of effect at each attack. Split the one movement budget before/between attacks if declared. A miss or invalid later target does not refund offense or grant a hidden new target. Other companions cannot spend a second offensive Action that numbered round. Without a command it may move defensively and Dodge while capable. No independent initiative turn or extra-turn reset is created.

### Noncombat Use

A real command may direct its profiled basic Action, manipulation or Search. Carrying and movement use the actual profile and real spent time. It may move supplied cargo or manipulate an unattended simple object, but it supplies no automatic Help advantage, profession, autonomous offscreen project, expedition roster office, extra Watch, training or institutional service. It cannot perform a job requiring missing proficiency or an ability it lacks. Real gear, whole bodies, Load and weight are not erased by apparent magical anatomy. A prospective action must still be physically possible in the available geometry.

### Healing Null And Ending

Use AC6-GREATER-PLANAR-ALLY-PROFILE-01 and GA-HEAL-01. Qualifying Null damage reaching 0 leaves the same occupying NullDisabled0 body while its one-hour source exists. Use AC6-SUMMON-SUPPRESS-01 for full suppression: the same body/HP/deadline/cargo remain paused, rather than ending/recreating the summon. Real one-hour expiry, replacement or dismissal still ends it. At source ending, carried/held real objects drop once at the real current position; intrinsic anatomy/attacks vanish without loot/corpse/XP/resource trigger. The CR6 phrase is a printed role/design target, not a certified numerical CR or approval of any named bestiary entry.

## Preserved printed effect
- Original name: Planar Ally (Greater)
- Original placements: [{"name": "Planar Ally (Greater)", "school": "Conjuration", "level": 6, "summary": "Summon a CR 6 extraplanar creature to assist for 1 hour."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Resonance Forge
**Spell ID:** `resonance-forge`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 6 | 11 | 13 |
| Mage | Conjuration | 6 | 11 | 13 |
| Shaman | Conjuration | 6 | 16 | 13 |
| Wizard | Conjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action,60feet,V/S/F and creating a magical forge that can craft items using Resonance Points. Preserve Core Instantaneous as the incomplete lifetime metadata. NEW create one fixed magical forge/anvil/work surface occupying a5-foot cube on a perceived stable unoccupied supporting surface in range/line of effect. It has actual300lb working mass, structural AC17/HP50, immunity to fire/poison/psychic damage and otherwise ordinary appropriate object defenses. It is a temporary conjured fixture, not detachable metal inventory or a creature. It lasts eight elapsed hours without concentration and provides controlled forging heat, ordinary anvil support and local ordinary working light within10feet, with no facility check bonus. It supplies neither the lead's actual Smith's tools/credential nor a complete secure workshop, Haven, storage, guards or another trade's station. Workpieces/material for the current order must fit its5foot work envelope and total at most500lb. It cannot be moved/recentered; actual loss of suitable support ends it.

NEW revision: eligible RP-funded production includes one otherwise legal, complete, reviewed Blacksmithing creation order, including its actual magical nonartifact recipe-imprint process. This is an explicit spell-specific acceleration of that entire recipe's active creation work; it is not restricted to mundane heating or metal-only ingredients. Use only a recipe with a complete operational output and a Forge-and-Anvil production interface whose real workpieces fit this fixture. All actual skill levels, tools, training, formula/discovery access, ingredients, ordered complete mundane base reservations, model/size/grade restrictions, work phases, output limits and required site category still apply. The forge supplies its compatible station and the stated work replacement; it supplies no base item, ingredient, formula or automatic success. An independently specified complete mundane metal-body recipe can also qualify if its source expressly permits this station for its entire active manufacture. Enchanting, Rune Carving and Tinkering are not admitted merely for containing metal: another trade needs its own complete reviewed compatibility rule. The forge cannot waive a required specialized facility or turn a field-prohibited recipe into field crafting. Living growth, incubation/calendar waits, attunement, recharge, servicing, repair, rework and formula research receive no manufacturing credit. Printing the recipe's actual magical imprint on its reserved body is now expressly permitted; inventing an artifact or an unreviewed output is not.

Preregister the one actual work order and source-authorized time modifiers first, rounding any legitimate modifier once under its own rule. Record the remaining adjusted active manufacturing minutes and original phases. One NEW forge cycle takes ten actual uninterrupted active minutes by the eligible lead and all claimed assistants and credits up to sixty of those remaining adjusted manufacturing minutes. This is an explicit replacement of work, not a demand to repeat the credited hour afterward. The final partial cycle still costs ten actual minutes and credits only its actual remaining work; unused credit is lost, never banked for another item/order. Choose ordinary work instead when that is preferable. No time feature further reduces this fixed ten-minute magical cycle or multiplies its sixty-minute credit unless a genuinely explicit later source says so. Other actual nonmanufacturing waits remain completely unchanged.

Before each cycle begins, one capable willing participant physically attending the forge for that cycle pays exactly5actualRP from one of their own legitimate RP pools. This may be the trained lead or a separate sponsor. These5RP are protected conversion principal: they cannot be discounted, waived, supplied by an unqualified imaginary pool or split into a nominal zero payment through Nexus/Influence. This operation is not another spell cast, does not use a second Counterspell window or Dissonance event, and cannot be financed by reusing the initial13RP casting payment. The sponsor's ten minutes are actual active participation and cannot also be rest, a different job or another forge cycle. Only a separately genuinely qualified full-time assistant within the recipe's cap supplies its actual+1; sponsorship itself grants no assistant bonus or trade XP.

Pay at the start and award work credit only after that entire legal cycle completes with the same real order, materials, tools, forge and participants. Interruption or loss of eligibility spends the paid RP and actual elapsed time but grants no partial cycle credit. Preserve earlier completed work according to the original work order's actual phase/stabilization procedure; the forge does not make an unfinished phase automatically secure or resurrect spoiled inputs. Suppression makes the fixture unavailable and interrupts an active cycle while the forge's eight-hour clock continues; unfinished real work/material remains where it physically was. Ending/destruction likewise drops only real stock and gives no RP refund, product or duplicate reservation. Rest cannot refill a paid cycle retroactively, and no source generates RP by dismantling the forge or its apparent fuel.

At actual completion of all remaining work, make exactly the ordinary one batch creation check and resolve its real six crafting outcome bands, natural1 Mishap, quality, source-qualified ancestry quality benefit, yield, catalyst retention and bounded failure recovery. RP does not guarantee success, grade, charges or a higher material tier. All actual ingredients/hosts and maximum-yield reserves are consumed/transformed/returned exactly once through their real recipe procedure. Finished output made from real reserved bodies and stock persists under its actual recipe-imprint procedure after this forge ends; the temporary fixture itself never becomes an ingredient, saleable item or permanent body reserve. NEW revision: retain the reviewed crafting learning procedure for the actual lead, including the actual recipe/trade identity, first-success history, triviality and ordinary success awards. The forge adds no XP multiplier, second work order, assistant award or reset of history. A failure-research award still requires its independently satisfied actual-input, actual-work and useful-finding predicates; credited recipe minutes are not falsely reported as elapsed personal work. The older proposal's blanket no-XP penalty is withdrawn in this unadopted revision because no governing source supplies it. Other pending spells, including Fabricate, are not changed by this proposal.

Only one order can use this fixture at a time, and one active Resonance Forge exists per caster. A successfully created replacement ends the old fixture without copying work/order/stock; failed formation leaves an old valid forge. The caster may dismiss it during their regular turn without an Action. ZeroHP, expiry, actual dispelling or loss of support ends it; temporary suppression alone can resume the same damaged fixture before its original deadline but never replays lost cycles. Workers count actual elapsed work minutes against EX58's daily work/rest limits, not the credited recipe minutes as a second Watch or free rest period. Real buyers, appraisal, price references and material provenance still govern any sale. The5RP/ten-minute/sixty-minute exchange and eight-hour station are consequential new balance choices awaiting joint review.

NEW explicit phase bridge: a completed ten-minute cycle grants its stated recipe-work credit within the current original phase. It does not automatically establish a new safe phase boundary. Reaching that source phase's full adjusted credit requirement stabilizes the incorporated inputs and progress under the source rule; elapsed perishability and personal work/rest clocks advance by actual time only. Forced interruption before a phase stabilizes loses that phase's unfinished credited progress, including credit from earlier completed cycles in that same phase, as the reviewed ordinary phase rule requires. Paid cycle RP is never returned. A voluntarily scheduled pause is safe only at an actual completed phase boundary or another source-permitted breakpoint. This bridge does not rewrite the recipe's material, failure or completion process.

## Preserved printed effect
- Original name: Resonance Forge
- Original placements: [{"name": "Resonance Forge", "school": "Conjuration", "level": 6, "summary": "Create a magical forge that can craft items using Resonance Points."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Faction Army
**Spell ID:** `faction-army`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Druid | Conjuration | 6 | 11 | 13 |
| Mage | Conjuration | 6 | 11 | 13 |
| Shaman | Conjuration | 6 | 16 | 13 |
| Wizard | Conjuration | 6 | 11 | 13 |

## Complete current procedure
KEEP Action,60feet,V/S/F,concentration up to one minute and3d6soldiers from an allied faction. NEW choose one actual canonical faction known to the caster. NEW gate, requiring comparison against the eventual accepted Faction Champion: actual alliedStatus=true, current institutional standing above0 on the reviewed -3..+3 scale, actual permission to invoke this faction's magical aid, and no current aid ban, all at commitment and resolution. Membership alone is neither sufficient nor required unless the actual institution makes it part of that permission. This is a source-specific spell predicate, not a general membership credential or right to command real faction personnel. Hidden loss of eligibility gives paid failure without reporting private institutional records. Before commitment declare up to18ordered legal perceived whole-body formation spaces within60feet/line of effect; fewer spaces are permitted but can limit arrivals.

After a legal cast survives interruption and the faction predicate remains valid, roll3d6 once for the number,3through18. NEW the spell forms that many temporary soldier representations of the chosen faction's known ordinary martial appearance, using the declared spaces in order. Recheck each space at formation; use only the first available valid spaces on that original declared list until the rolled count is reached. If too few fit, form fewer, with no after-results new placement or RP refund. Preserve the roll and missing slots; later space becoming free creates no delayed soldier. This explicitly chosen bounded representation model retains real faction affiliation in the spell's admission/presentation but does not transport, copy, conscript or injure named real soldiers elsewhere. It grants no secret memories, legal rank, faction orders, signature authority or impersonation of a unique official. No original person's consent or inventory is silently overwritten.

NEW each arrived soldier is a separate actual Medium Humanoid-type magical companion with baseHP20,AC14,walk30,body mass160lb,STR12,DEX12,CON12,INT8,WIS10,CHA8. Ordinary sight/hearing; all six saves use original source-owner current PB total, other checks use printed ability modifiers without proficiency. Each has its own currentHP, position, conditions and source-qualified maximum modifiers. Its sole profiled attack is one melee spell attack at reach5feet using that creating source's current attack modifier,1d8slashing with no added ability damage. No inherent Multiattack, Reaction, ranged attack, spellcasting, special resistance/immunity or trade credential is copied from the faction's actual members. Its apparent armor/shield/weapon are intrinsic manifestations of this profile, not detachable equipment, rare uniforms or merchant stock.

All3d6bodies share the owner's existing one BA command and one offensive companion Action per numbered round with every other asset. One real command selects one soldier and its one legal Move plus profiled/basic Action for the existing attached phase; it is not a free army-wide volley. Others can move defensively and Dodge while capable in that same owner-linked phase, with real independent body occupancy and conditions. Thus the count remains multiple actual bodies that can hold different legal spaces and absorb separate incoming attacks, not one generic minion with a multiplied damage number. It creates no extra flank/cover advantage beyond actual geometry and the existing rules. Creation itself supplies no free attack; an actually unspent creation-turn command/offense can operate normally. A soldier losing eligibility before its commanded act causes the ordinary failed command without handing the unused act to another body.

The soldiers understand simple spoken commands they can actually hear within the normal60foot command scope; no speaking language, remote perception or off-screen plan execution is granted. Genuine real supplied gear has actual mass/custody and can make movement or a profiled task physically impossible, but gives no new printed attack or extra command. The cohort cannot become twelve new expedition roster members, assistants, work offices, teachers, faction voters or a recruitment reward from its temporary appearance. Actual witnessed conduct may have ordinary social consequences, but formation grants no automatic standing increase, permission, wages, supplies or institutional service.

One active Faction Army cohort per caster across every faction. A genuinely formed nonempty new cohort replaces its old cohort without transferring bodies/HP; ordinary concentration commitment may already have ended it. An individual reaching0 from ordinary non-Null damage vanishes and frees no replacement slot. Accepted qualifying Null damage instead leaves that same finite soldier NullDisabled0 while its source exists: Incapacitated, Speed0, no Actions/Bonus Actions/Reactions/commands. Later Null damage does not create a fresh body or deadline. Independent source ending, including the explicitly proposed full suppression endpoint below, remains real. Expiry, concentration ending or eligible parent removal ends every remaining representation, with no real-person return journey, corpse, harvest, death resource or intrinsic item. NEW full suppression of an individual manifestation ends that body permanently for this cast; suppression of the parent ends all, while narrow condition suppression retains its ordinary scope. Real carried objects drop at their actual last positions and belong to the actual custody ledger. The faction's real roster and stock are unchanged because those people/items were never transported. The many-body/one-command tactical balance and temporary representation interpretation are explicit new decisions for actual GPT discussion, not assumptions about planar origins.

NEW BODY/HEALING COMPLETION: each soldier has two ordinary hands and feet, with up to100lb AND6Load genuine carried capacity, subject to actual hand/body/equipment rules; neither number grants more hands or free interactions. Its intrinsic attack requires one usable hand but supplies no detachable weapon. Known impossible load/manipulation fails preflight. Temporary bodies are not free skilled workers or expedition roster/assistant slots. Apply AC6-HEAL-TARGET-02 separately to each still-existing soldier: it is an eligible creature/living ally for otherwise legal normal-HP healing, including Healing Rite; healing above0 clears only its NullDisabled state. No generic physiology/soul/native identity, resurrection, corpse or rest pool is inferred. Intrinsic equipment never enters ordinary inventory; genuine supplied objects keep identity/custody and drop exactly once at actual ending.

Each commanded soldier attack has dealer=that soldier body, not the owner/controller. Full suppression ending the individual/parent remains an explicit NEW source-specific proposal, requiring comparison against the pending AC5 Champion pause rule rather than silently importing it. Later faction standing/permission change does not retroactively end an already-admitted cohort absent an actual source-ending rule; it affects future casts and real social consequences.

CURRENT AC6 SUPPRESSION/NULL COMPLETION: each soldier uses AC6-SUMMON-SUPPRESS-01 for full suppression and AC6-HEAL-TARGET-02 for narrow HP-healing. Full parent suppression pauses every still-existing soldier body; individual local suppression pauses only intersecting bodies. Intrinsic temporary equipment is part of the suppressed/ending representation; genuine external cargo keeps its own identity and drops once on source ending. Soldier attacks use the soldier as damage dealer/root owner.

## Preserved printed effect
- Original name: Faction Army
- Original placements: [{"name": "Faction Army", "school": "Conjuration", "level": 6, "summary": "Summon 3d6 soldiers from an allied faction."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.

# Alignment Nexus
**Spell ID:** `alignment-nexus`  
**Review status:** NEW provisional authored-playtest replacement candidate; not adopted

## Access
| Class | School | Rank | Min class level | Base RP |
|---|---|---:|---:|---:|
| Cleric | Divination | 6 | 11 | 13 |
| Druid | Conjuration | 8 | 15 | 21 |
| Mage | Conjuration | 8 | 15 | 21 |
| Mirrorsage | Divination | 6 | 16 | 13 |
| Shaman | Divination | 6 | 16 | 13 |
| Wizard | Divination | 6 | 11 | 13 |

## Complete current procedure
### Access

KEEP one source identity with two fully distinct printed operations. Current actual class rows grant Divination6/base13/range60 to Cleric11, Wizard11, Mirrorsage16 and Shaman16; they grant Conjuration8/base21/range120 to Druid15 and Mage15. No other mode is granted by a global minimum-rank/header, another school's progression or this proposal. Both retain Action and V/S/F. All original placements, including conflicting global metadata and Core Instantaneous, remain intact as evidence. NEW each mode receives its own explicit finite concentration duration below.

### Alignment And Bonus

At successful resolution snapshot the caster's actually defined effective complete alignment pair after accepted underlying history/overlays. If either axis is genuinely undefined, the paid cast establishes no Nexus and supplies no alignment diagnosis. This pair never changes for that application. A creature benefits only when its actual current complete effective pair matches at the creation of an eligible roll. NEW the Nexus insight benefit is +2 to that creature's actual attack-roll, saving-throw and ability-task modifier, before rolling. It changes no AC, damage, DC, HP, RP, rank, critical range, proficiency, automatic result or fixed opposed total. The source's actual normal resolution and information rules still apply. A reroll/replacement of that same original event retains its original modifier set under its own source, rather than resnapshotting alignment to ratchet a bonus.

### Overlap And Identity

Both modes share one explicitly NEW family, alignment-nexus.insight. A creature receives at most one+2 from that family at an event, regardless of casts, modes, plane effects or casters; choose the earliest eligible active source for equal applicable benefits. This does not reclassify any unrelated class/item bonus into a new universal stacking family. One active Alignment Nexus per caster across both modes. Beginning either new concentration ends the caster's old concentration under ordinary rules even if the new cast later fails. Other casters retain independent records and clocks.

### Readout

Eligibility supplies no public roster, alignment identification, oath permission, compelled choice, belief change or origin inference. Hostile matching creatures can benefit just as allies can. Neither mode rewrites alignment to make a creature qualify. Its own bonus is a local magical expression at the beneficiary; actual local suppression can suspend that expression without changing the underlying alignment record.

### Current Integration

```json
{
  "modeAccess": "Use only the actual class row: Cleric11/Wizard11 Divination6 13RP 60ft; Mirrorsage16/Shaman16 Divination6 13RP 60ft; Druid15/Mage15 Conjuration8 21RP 120ft. No Wizard Conjuration8 access is invented.",
  "transportClassification": "AC6-NEXUS-TRANSPORT-01: Conjuration8 crossings are planar transitions and teleportation for this spell only. This intentionally differs from accepted AC5 Alignment Portal.",
  "portalBodies": "Each live mouth is a fixed physical 10-foot-wide by 15-foot-high aperture with exact pose. Whole-body entry and exit footprints must fit. The portal itself does not create difficult terrain. Actual terrain rate is 1/2/3 movement per foot, then crawling adds +1 per foot and squeezing +1 per foot. Thus 5ft difficult+squeeze costs15ft; difficult+crawl+squeeze costs20ft.",
  "planeBenefit": "AC6-NEXUS-PLANE-BONUS-01 preserves the temporary destination-plane +2 aligned-recipient benefit while parent is live; this is spell metadata, not intrinsic plane alignment/cosmology.",
  "blockers": "Actual accepted Dimensional Anchor tests the traveler transition endpoints, not portal formation. Other exact voluntary/teleport predicates use their own text. Closing the portal grants no free return; travelers remain where they actually are."
}
```

## Preserved printed effect
- Original name: Alignment Nexus
- Original placements: [{"name": "Alignment Nexus", "school": "Conjuration", "level": 8, "summary": "Create a portal to a plane that empowers creatures of your alignment."}, {"name": "Alignment Nexus", "school": "Divination", "level": 6, "summary": "Create a zone where creatures of your alignment gain insight bonuses."}]
- Original operational metadata remains preserved in `SPELLS_MODEL.json`; this chapter does not rewrite it.
