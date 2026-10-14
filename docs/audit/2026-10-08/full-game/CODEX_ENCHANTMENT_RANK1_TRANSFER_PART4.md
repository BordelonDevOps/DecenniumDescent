PART 4 OF 4. Concatenate parts in numerical order after removing this first line; all four belong to one exact manuscript packet.
 {
  "id": "alignment-suggestion",
  "activation": "Action",
  "targets": "One creature you perceive within30feet and line of effect. No requirement that its alignment be known; hidden canonical axes are resolved after paid casting.",
  "duration": "Concentration, up to1minute. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": true,
  "resolution": "The target makes a Wisdom save. Success: no new overlay. Failure: snapshot your actual current alignment orientation. For each axis defined both for you and for the target, compute one step toward your snapshotted value along Lawful–Neutral–Chaotic and Good–Neutral–Evil. Compute the target baseline without any previous Alignment Suggestion overlay on that target, retaining all independent actual alignment effects/records. An already matching or undefined axis gains no changed-value overlay. If at least one axis changes, replace the prior same-spell overlay with the new recorded axis values/deadline. A failed-save cast that changes no defined axis creates no new overlay and does not itself replace a valid older one; mandatory concentration transitions remain independent.",
  "effect": "The changed values are the target’s actual effective canonical alignment for rules that query those axes during the overlay, including real alignment-gated spells/items. Example: baseline Chaotic Evil targeted by a Lawful Good caster becomes Neutral Neutral; one such overlay never jumps two steps. Its values remain fixed until expiry/removal/replacement and do not recompute every time another underlying record changes. Unchanged/unoverlaid axes follow their actual underlying records. An independent effect such as Corrupted can change underlying alignment while this spell persists; that change remains and is exposed when the applicable overlay ends. One Alignment Suggestion overlay per target across casters; recasting cannot use its old overlay as a staircase for another same-spell step.",
  "limitations": "The spell grants no automatic knowledge of either character’s axes, including whether a value changed. Actual information protections still govern observations. It never compels matching behavior, belief, confession, loyalty, PvP, personality or oathbreaking; conduct clauses still judge actual conduct. Ending removes only this overlay, without restoring an old alignment snapshot, deleting independent changes or reviving a replaced overlay. Caster orientation is fixed at application, not tracked through later caster changes. Ward tag creates no ward. More specific alignment-changing effects retain their actual interaction rules; this card does not invent a general priority engine for every unrelated overlay",
  "designNotes": "PRESERVED: Action/30feet/V,S,M/F as focus, WIS, concentration minute and actual push toward caster alignment. NEW: temporary canonical one-step overlay on both eligible axes. Exact-review proposals: compute without previous same-spell overlay to prevent recast ratcheting, overlay only genuinely changed axes, fixed values, and no new application when no defined axis changes; independent base changes survive ending.",
  "sourcePlacements": [
   {
    "name": "Alignment Suggestion",
    "school": "Enchantment",
    "level": 1,
    "summary": "Subtly push target toward your alignment (WIS save)."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 340,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Alignment Suggestion",
     "effect": "Subtly push target toward your alignment (WIS save).",
     "source_paragraph": 9400,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Concentration, up to 1 minute",
     "components": "V, S, M/F",
     "resolution": "Wisdom save",
     "tags": [
      "Ward",
      "Alignment"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "resonance-influence",
  "activation": "Action",
  "targets": "One creature you perceive within30feet and line of effect. Choose Ease or Burden at casting; Ease requires actual willingness at application.",
  "duration": "Until the next qualifying spell commits or up to1minute, no concentration. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": false,
  "resolution": "Ease: automatic on a willing target; establish a pending−1RP final-price modifier. Burden: target makes a Wisdom save even if willing unless an independent rule grants a save waiver; failure establishes pending+1RP, success creates no replacement. One pending Resonance Influence record per target across casters; a successful eligible application replaces the previous mode/deadline. Invalid or saved-against application does not erase a valid old record.",
  "effect": "For the target’s next actual spell cast whose procedure has an RP-price interface, compute the ordinary legal RP price first: actual class/source rank/base, mandatory printed spell extras, applicable Dissonance surcharge, and only the exact eligible class/source reductions or waivers with their scopes/minimums. Then apply this spell’s final±1, minimum0, with no credit/refund. An ordinary0RP cantrip qualifies: Burden prices it at1; Ease leaves it0 and is still consumed. A genuine RP-priced spell reduced/waived to0 also qualifies; this final modifier can make its payment1. A charge-only item spell or free technique with no RP-price interface does not qualify and consumes nothing. An RP-priced actual class/item spell can qualify; paying RP for a nonspell technique alone does not. Validate adjusted affordability and all other preflight rules, then consume the record atomically at legal cast commitment with payment. Later failure/countering does not refund the rider. An illegal/unaffordable attempted cast never commits and leaves it available.",
  "limitations": "Ready pays/consumes at spell preparation, not release. This new application cannot retroactively alter its own already-paid casting price; a previously existing Influence may price that cast normally. Ordinary class minimums govern their own discount calculations first; the final Ease may then reduce an otherwise1RP result to0. Mandatory extras remain in that ordinary price, not omitted, though Ease can offset1RP of the resulting total. Other non-RP costs, charges, limited uses, rank/access/repertoire, components, Fractured restriction, Dissonance and Refrain are unchanged. A pending hostile+1 requires real adjusted affordability but does not grant the caster hidden knowledge of RP pools or pricing failures. Current quote_cast helper lacks this stateful modifier and class-discount integration; this card is a tabletop interface, not a runtime implementation",
  "designNotes": "PRESERVED: Action/30feet/V,S,F and next-spell RP cost±1. NEW: modes, willingness/WIS, minute, final-price ordering, replacement and cast-commit consumption. Exact-review proposal explicitly includes a normally RP-priced cast made free by another source, while excluding a source with no RP-price interface; final modifier follows source-specific minimum calculations.",
  "sourcePlacements": [
   {
    "name": "Resonance Influence",
    "school": "Enchantment",
    "level": 1,
    "summary": "Target's next spell costs +1 or -1 Resonance Points."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 341,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Resonance Influence",
     "effect": "Target's next spell costs +1 or -1 Resonance Points.",
     "source_paragraph": 9401,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Automatic or opposed as described",
     "tags": [
      "Resonance"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "enthrall",
  "activation": "Action",
  "targets": "Choose up to3 distinct creatures you perceive within30feet and line of effect that can hear your casting words/tone at application.",
  "duration": "Concentration, up to1minute. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": true,
  "resolution": "Each eligible target independently makes a Wisdom save. Success: no effect on that target. Failure: captivate it, imposing disadvantage on all actual Perception checks for the duration, including checks about you or your tone.",
  "effect": "This affects actual rolled Perception checks under normal advantage/disadvantage rules; it neither creates a check nor changes its task permissions. Hearing is needed only at application. No continuing song, performance, instrument, sound, hearing or30foot tether is added. You still provide the audible V component and normal S/F. The three-target set is fixed on casting; no later replacement target can be added without another paid spell. Independent Enthrall sources have their own durations and concentration, but repeated disadvantage never stacks.",
  "limitations": "No automatic Search failure, passive-Perception−5, Hidden state, Stunned, Charmed, awareness deletion, forced movement or Action loss. Loss of this caster’s concentration ends this cast’s applications; another caster’s valid application remains. The source Enchantment rank2/Core349/3RP placement is preserved but unassigned and not selectable: it grants no all-hearers mode, extra-RP upgrade or additional class access. Current class access selects only this reviewed-candidate rank1 mode",
  "designNotes": "PRESERVED: rank1 Action/30feet/V,S,F, plural captivated creatures and Perception disadvantage. NEW: three targets, hearing, WIS and concentration minute. Rank2 all-hearers/WIS source remains intact as an unassigned variant pending a separate access/identity decision; no historical information is discarded.",
  "sourcePlacements": [
   {
    "name": "Enthrall",
    "school": "Enchantment",
    "level": 1,
    "summary": "Captivate nearby creatures; they have disadvantage on Perception checks."
   },
   {
    "name": "Enthrall",
    "school": "Enchantment",
    "level": 2,
    "summary": "Captivate all creatures that can hear you (WIS save negates)."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 343,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Enthrall",
     "effect": "Captivate nearby creatures; they have disadvantage on Perception checks.",
     "source_paragraph": 9403,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Automatic or opposed as described",
     "tags": [
      "Utility"
     ],
     "rp_cost": 2
    }
   },
   {
    "index": 349,
    "original": {
     "school": "Enchantment",
     "level": 2,
     "name": "Enthrall",
     "effect": "Captivate all creatures that can hear you (WIS save negates).",
     "source_paragraph": 9411,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Wisdom save",
     "tags": [
      "Utility"
     ],
     "rp_cost": 3
    }
   }
  ]
 }
]

## Explicit questions

Especially assess: Alignment Suggestion ignores its previous same-spell overlay to prevent recast ratcheting; only changed axes overlaid, no-change cast establishes/replaces nothing, independent underlying changes persist. Resonance Influence applies final±1 after actual source discount/minimum/waiver and can offset mandatory Resonance Shield1; does Burden make Mage Spell Sharing free cast cost1? Please explicitly resolve this exception. Also review Sleep all-applications physical waking, pending Flash/Command replacement, Command one-time Drop vs turn-long Halt/Grovel, Voice of Peace participant snapshot, Faction Charm independent faction records, Distract already-cancelled parent handling, Laughter current-turn repeat save vs never-deferred prevention. Rank2 Enthrall remains preserved unassigned. All provisional manuscript work, no runtime/balance/full-game certification.

## Exact relevant existing class source cards

DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json SHA256 25387b0dcfae0d53d689486d4b05d8ef5b24bed1b70f0baab970a82dbd370f89

{"id": "cleric.hero.saint.merciful-sacrament", "name": "Merciful Sacrament", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your Sacrament", "duration": "For that activation", "frequency": "1/short rest", "effect": "Merciful Sacrament. Tags: saint, sacrament. When you start Sacrament and at least one living ally inside its initial zone is at or below one-quarter maximum HP, you may reduce that Sacrament's Conviction cost to 0. Its RP cost and all other requirements remain. Because no Conviction is spent, this waived cost does not vent Dissonance.", "spellRank": null}

{"field": "engine", "index": 3, "text": "Cleric techniques use only their printed RP and Conviction costs. All RP is paid from the Cleric's Core Systems V 2 Resonance Point pool. A Cleric technique is not automatically an ordinary spell-rank cast and does not receive Overcast, spell-slot, cost-discount or spell-proc benefits unless a feature explicitly says otherwise. Ordinary spells continue to use Core V 2 spellcasting rules."}

DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json SHA256 c64782e192e2e63e5abed5728f9213c9d4cf956bce1a75da7a156dbfd1141e0b

{"id": "mage.arch.spell-efficiency", "name": "Spell Efficiency", "activation": "Passive", "cost": "0", "rangeAndTarget": "Self", "duration": "Until end of your next regular turn", "frequency": "At most once per turn", "effect": "Spell Efficiency. Tags: arcanist, resonance, focus. After you legally cast a Focus-eligible spell, your next differently named Focus-eligible spell of the same current element before the end of your next regular turn costs 1 less RP, minimum 1 RP. This reduction cannot apply to Focus finishers, Resonance Surge's additional cost or a spell already reduced to 0 by another explicit feature.", "spellRank": null}

{"id": "mage.hero.archmage.spell-sharing", "name": "Spell Sharing", "activation": "Action", "cost": "4 RP plus the shared card's printed RP cost", "rangeAndTarget": "One willing ally within 30 feet", "duration": "Until end of ally's next regular turn", "frequency": "1/short rest", "effect": "Spell Sharing. Tags: archmage, spell-sharing. Choose one Base or Arch Mage spell card you know with an Action activation and printed base RP cost 4 or less. Pay both costs now. The ally may cast that card once before the end of its next turn without paying RP, using your Mage spell attack and DC. It cannot share summons, Counterspell, Hero cards, finishers, Resonance Surge or another Spell Sharing.", "spellRank": null}

{"id": "mage.supplement.resonance-apex-new-playtest-capstone", "name": "Resonance Apex — NEW Playtest Capstone", "activation": "Triggered", "cost": "0 additional RP", "rangeAndTarget": "One Mage spell you are beginning to cast", "duration": "For that cast", "frequency": "1/long rest", "effect": "Before paying for one Mage spell, reduce that spell's printed RP cost by up to 10 RP, minimum final cost 0. This capstone is new playtest design and is not claimed as a recovered historical feature. The cast cannot also use Resonance Surge or generic Overcast. It remains one spell cast, follows ordinary Focus/Nuke Chain rules, and alters Dissonance only through rules that would already apply to that cast.", "spellRank": null}

DescentReviewChanges/ReviewBible/data/public/class_playtests/mirrorsage.json SHA256 9179729dd39e0a81f4f6d78b9fbb0c7fb296fb5d418aaa238d7ff6aa02b2bd3a

{"id": "mirrorsage.hero.light-weaver.sacred-echo-slot", "name": "Sacred Echo Slot", "activation": "Passive", "cost": "0", "rangeAndTarget": "One restricted archive slot", "duration": "While known", "frequency": "Continuous", "effect": "Add one slot usable only for Mend or Ward, total storage cap 6. If already at 6, designate one existing slot sacred instead; once/short rest its release costs 1 less RP, minimum 1. No duplicate slot or free record.", "spellRank": null}

DescentReviewChanges/ReviewBible/data/public/class_playtests/shaman.json SHA256 c88fcad8c14734cc852a95aee7b3686fd64ea2a8cfb9d014f4297b7efec94a62

{"id": "shaman.supplement.elder-spirit-accord-new-hero-capstone", "name": "Elder Spirit Accord — new Hero capstone", "activation": "Triggered", "cost": "1 long-rest use", "rangeAndTarget": "Your chosen Hero ultimate", "duration": "One activation", "frequency": "1/long rest", "effect": "When starting Elemental Chorus, Omen Loop or Bloodroot Trail, reduce its RP cost by 3, minimum 1, and add M to one damage/healing roll from that use. You must know that ability and still spend its own limited use. If you do not know it, instead reduce one known Hero technique's RP cost by 3, minimum 1. No extra duration, flask, totem, command or repeated cast.", "spellRank": null}

DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json SHA256 8ab2f4f43bcbced418fb266e5bd3216cff491b0c442c16f93438bd3556672c8b

{"id": "wizard.arch.spell-efficiency", "name": "Spell Efficiency", "activation": "Passive", "cost": "0", "rangeAndTarget": "Repeated prepared matrices", "duration": "Until end of your next regular turn", "frequency": "At most once per turn", "effect": "Spell Efficiency. Tags: arch, passive, resonance. After you cast a prepared matrix, the next cast of that SAME matrix family before the end of your next regular turn costs 1 less RP, minimum 1. This cost reduction does not suppress Refrain, cannot reduce Overcast or additional feature costs and cannot combine with itself.", "spellRank": null}

{"id": "wizard.hero.elementalist.core-sync", "name": "Core Sync", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your current Elemental Affinity", "duration": "Permanent", "frequency": "Always", "effect": "Core Sync. Tags: hero, elementalist, passive, elemental. Rank-1 and rank-2 Wizard spells whose primary damage type matches your current Elemental Affinity cost 1 less RP, minimum 1. Once per long rest as a Bonus Action you may change your Elemental Affinity to Fire, Cold, Lightning or Earth; changing it does not alter currently active spell effects.", "spellRank": null}

{"field": "engine", "index": 13, "text": "RITUAL CASTING is automatic at Wizard 2. A Wizard spell in your spellbook with the Ritual tag can be cast from the book without being prepared by increasing its casting time by at least 10 minutes. A ritual cast costs 0 RP unless that ritual explicitly lists a consumed RP cost, cannot be used during an encounter and cannot generate or vent Dissonance through ordinary casting strain."}

{"field": "engine", "index": 15, "text": "MATRIX MASTERY MODIFICATIONS. After acquiring Matrix Mastery, each prepared ordinary spell matrix may carry at most one modification chosen during preparation. QUICK SUBSTITUTION: once per short rest, replace one matrix marked Quick Substitution with another spellbook spell of exactly the same rank using a 1-minute ritual instead of the normal 10-minute midday swap; the replacement loses the modification until the next long rest. COMPONENT ENHANCEMENT: when casting a damaging or healing matrix, spend 1 additional RP to add one extra die of the spell's primary damage or healing die to one roll; if the spell has no such die this modification has no effect. MATRIX LINKING: pair two different prepared matrix families during preparation; after legally casting one, the other costs 1 less RP, minimum 1, if cast before the end of your next regular turn, at most once per pair per round. STABILITY REINFORCEMENT: gain +2 on concentration saves caused by damage while maintaining that matrix. A matrix modification never creates another spell cast or proc event."}
