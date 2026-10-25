# Part B — exact source excerpts and selection boundary

The recovered sixteen procedures and six clauses remain literal draft data. The following full native cards explain actual class accounting; no new feature is granted.

## Mage source `/cards/12` — mage.base.lightning.lightning

```json
{
  "id": "mage.base.lightning.lightning",
  "name": "Lightning",
  "className": "Mage",
  "band": "Base",
  "path": "Lightning",
  "sourceKind": "supplement",
  "minimumClassLevel": 2,
  "acquisition": "automatic",
  "activation": "Passive",
  "cost": "0; Storm Arc costs 2 RP when primed",
  "rangeAndTarget": "Self; finisher starts on one enemy within 60 feet and may jump twice within 15 feet",
  "duration": "Permanent Focus; finisher instantaneous",
  "frequency": "Choose at Mage 2; finisher recharge 3 rounds",
  "effect": "Elemental Focus — Lightning. Tags: focus, lightning. Once on each of your turns after a Lightning Mage spell damages a creature, arc S lightning damage to one different enemy within 10 feet. FINISHER — Storm Arc: after a completed Lightning Nuke Chain, Bonus Action, 2 RP. Make separate Mage spell attacks against one enemy within 60 feet and up to two additional different enemies, each within 15 feet of the previous target. Each hit deals S d6 lightning. A target critically hit by Storm Arc makes a Constitution save; failure Stuns it until the end of its next turn.",
  "source": {
    "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
    "line": 2909,
    "originalText": "Lightning: +15% jump chance, arc disruption. Finisher: Storm Arc – Jumps to 3 enemies, stuns on crit"
  },
  "designStatus": "provisional-playtest",
  "spellRank": 1
}
```

## Mage source `/cards/17` — mage.arch.elemental-mastery

```json
{
  "id": "mage.arch.elemental-mastery",
  "name": "Elemental Mastery",
  "className": "Mage",
  "band": "Arch",
  "path": null,
  "sourceKind": "passive",
  "minimumClassLevel": 7,
  "acquisition": "selection",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your current Elemental Focus spells",
  "duration": "Permanent",
  "frequency": "Always",
  "effect": "Elemental Mastery. Tags: arcanist, focus. Improve the secondary effect of your current Focus. Fire Burns from your Focus cards last one additional turn but never stack. Cold Focus Speed reductions increase by another 5 feet, minimum 0. Lightning Focus's once-per-turn secondary arc increases from S flat lightning damage to S d4 lightning damage. Pivoted Focus uses the corresponding upgraded rider.",
  "source": {
    "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
    "line": 2916,
    "originalText": "Elemental Mastery: Increase the effectiveness of your chosen element's secondary effects."
  },
  "designStatus": "provisional-playtest",
  "spellRank": null
}
```

## Mage source `/cards/14` — mage.arch.overload-crits

```json
{
  "id": "mage.arch.overload-crits",
  "name": "Overload Crits",
  "className": "Mage",
  "band": "Arch",
  "path": null,
  "sourceKind": "passive",
  "minimumClassLevel": 3,
  "acquisition": "selection",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "One enemy within 10 feet of a creature critically hit by your damaging Mage spell",
  "duration": "Instantaneous",
  "frequency": "At most once per turn",
  "effect": "Overload Crits. Tags: arcanist, critical. When a damaging Mage spell scores a critical hit, choose one different enemy within 10 feet of the critically hit target. It takes damage of the same type equal to 50% of the spell's base unmodified damage dice total before critical extra dice, rounded down once, minimum 1. Flat bonuses, riders and critical extra dice are not copied again.",
  "source": {
    "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
    "line": 2913,
    "originalText": "Overload Crits: Critical strikes deal +50% splash damage to nearby enemies."
  },
  "designStatus": "provisional-playtest",
  "spellRank": null
}
```

## Accepted Lesser Antimagic — original CANDIDATE counterpart7

Action; range 10 feet; V/S/F; base 10 RP. Preserve the source's 10-foot sphere and suppression promise. NEW: choose one perceived fixed point within 10 feet and line of effect; create a fixed 10-foot-radius sphere with concentration up to 60 elapsed seconds, explicitly replacing the source's insufficient Instantaneous field duration for this authored procedure. The volume is clipped by actual solid total-cover barriers from the center and never follows a creature.

The field suppresses the local expression of actual ongoing spells and explicitly magical nonspell technique expressions only where their real body/effect/anchor intersects the operative volume. It supplies no rank ceiling. It does not retroactively undo completed damage, healing, movement, transmutation, consumed items, permanent ordinary matter, HP loss or source history. It does not erase class engines, learned facts, RP pools, injuries or intrinsic nonmagical traits. A magic item keeps its mundane body/ownership/contents while its magical enhancements/actions are unavailable. A creature-attached spell buff is wholly unavailable while the creature intersects; a large wall/field loses only its intersecting portion unless its own indivisible source says otherwise.

An otherwise legal spell cast may still be committed inside: pay its real final price, Action/components/cadence and concentration transition. If the spell's relevant manifestation originates inside the field, suppress that payload at resolution; there is no queued later release and no refund. Do not invent an imaginary straight-line beam/path for teleportation or nonprojectile magic. For current Dimensional Door, an origin and endpoint both outside the field are unaffected even if a drawn line crosses it; an origin actually inside the field has its spell payload suppressed after legal commitment. A remote ongoing effect outside is not canceled merely because its concentrating caster enters the field.

Ranger Nature's Whisper is an explicitly magical NONSPELL technique. Inside the field its Action+1 RP+Recharge 3 commitment remains a nonspell event; the magical payload/rider is unavailable with no rank, Counterspell window or Nexus/Dampening price. A still-live Nature's Whisper rider on an actor inside the field is unusable while suppressed but its clock continues.

Oracle's Burden prevents generic remove/suspend of the intrinsic Oracle Curse, so this field does not erase or suspend the Curse engine. Curse Manifestation, Tongues and Consumed retain only their own exact suppression/appearance permissions and timers.

Instances of Lesser Antimagic do not suppress one another; overlapping instances form the union of active volumes. This same-family exception only prevents oscillation and grants no ability to cast a new field from inside another without paying/satisfying the new cast, whose payload is itself exempt only because it is this family.

For Greater Fire Pet and Faction Champion use AC5-ANTIMAGIC-SUMMON-01. For accepted ordinary Banishment, only actual suppression of the application itself invokes its own accepted closure/end rule; merely suppressing its distant caster does not reach the generated cell/application. For Banish Elemental and Elemental Banishment, AC5-BANISH-EXT-01 expressly gives the same close-on-actual-suppression behavior.

Suppression never pauses absolute/source clocks and does not bank missed attacks, aura starts, periodic damage, saves or commands. On exit/end, only still-live source expressions resume with the same remaining HP/pools/deadlines. Wall of Force uses its own safe segment-resumption rule.

Repair04 incoming/output completion: use AC5-ANTIMAGIC-IO-04. An instantaneous effect cast outside is not immune merely because its source is outside: inspect the actual recipient/area/destination manifestation. Local damage/healing inside is suppressed with no packet/root; an outside-origin Dimensional Door whose destination footprint is inside fails atomically after cost, while outside→outside remains unaffected regardless of an imaginary line. A legal Greater Dispel or exact class Dispel resolves captured termination operations under AC5-ANTIMAGIC-IO-04; the target Antimagic application ignores only its own suppression, while a different Antimagic field can still suppress that termination operation; ordinary Counterspell remains only a cast-time response before the field exists. Spell Preservation’s primary-book anti-destruction remains source-intrinsic even while magical book usability is suppressed.

## Cover, sight, Hide and Search

Keep **visibility**, **known location**, and **line of effect** separate. Seeing through a barrier does not itself permit attacking through it. Best cover only: half +2 AC/DEX saves; three-quarters +5; total prevents direct targeting through that obstruction. Never add +2 and +5. For areas, evaluate line/cover from the area's origin to each target; total cover there excludes a creature unless the effect explicitly travels around/through the obstruction. The origin point itself must be legally targetable.

Within normal ranged range, no range penalty; beyond normal through long, disadvantage; beyond long, illegal. Ranged attacks also have disadvantage when within5ft of a non-Incapacitated hostile that can see the attacker, even if the attacker cannot see that hostile. All advantage/disadvantage follows the single cancellation rule.

NEW **Hide**: permitted only against observers unable to see you clearly or where a feature permits. Roll DEX Stealth once, record natural die and total. Against each observer's passive DC `10 + WIS Perception modifier including applicable proficiency`, use the Core four-degree task system. Meet DC succeeds before natural1/20 degree adjustment; Success/Critical Success establishes Hidden for that observer. No unsourced passive ±5 adjustment for advantage/disadvantage. Actual Search rolls use their normal modifiers.

Hidden means that observer cannot see you and does not know your location. Clear sight or learning your position ends Hidden for that observer. Moving between hiding places can retain Hidden only if no clear sight/revealing event occurs. A failed Hide cannot simply be rerolled unchanged; a materially new hiding position, concealment, distraction, sight-breaking event or express reroll feature is required. Hidden is not a generic immunity or a free stealth roll for every move.

**Search** Action: WIS Perception for sensory detection; INT Investigation for appropriate traces/deduction; Core Arcana/Engineering where relevant. Directly locating a Hidden creature defaults to Perception against its recorded final Stealth total as a static DC, using task degrees/natural shifts. Success reveals location only to the searcher and ends Hidden for that observer, without automatically granting sight. Communicate normally to inform others. Search can be repeated on later turns by paying the Action.

Attacks against unseen targets have disadvantage; unseen attackers have advantage, subject to the **Core Invisible exception**: once its position is known, Invisible's own attack modifiers end for that observer and cannot immediately return solely because it remains Invisible. Independent darkness, smoke, blindness or hiding can still supply modifiers.

Resolve an attack using pre-attack information; afterward reveal location to observers able to perceive its evidence. If an unseen target's location is unknown, do not directly choose it for a creature-target effect. A weapon/projectile can instead attack a suspected space: wrong space automatically misses; correct space uses unseen rules. A “creature you can see” requirement is never met by position knowledge alone. Area effects can target legal points under their own rules.


## Supplied occupied-body ramp counterexample

At foot[12,6,7.5], occupied box min[9.5,3.5,7.5]/max[14.5,8.5,13.5]. The ramp point[12.16,5.88,7.65] is strictly interior and lies exactly onz=3+.6x-.45y. A safe-footing assertion is not a valid replacement for a clear swept body. The current PartA suffix is therefore conditional, not operationally validated.
