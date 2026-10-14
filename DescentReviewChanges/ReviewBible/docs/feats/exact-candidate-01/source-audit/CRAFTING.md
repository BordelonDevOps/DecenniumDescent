# Crafting — complete source/question reconciliation

Source-authored exact candidate; separate exact review pending. Selection/runtime disabled. Original catalogs unchanged.

## CTF-01 — Arcane Focus

### Original complete object

```json
{
  "id": "arcaneFocus",
  "name": "Arcane Focus",
  "description": "You can focus magical energy more effectively.",
  "prerequisite": "Spellcasting ability",
  "effect": "You can use your spellcasting focus to cast spells without material components worth less than 100 gp.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Spell materials and Scribing activation",
  "question": "Define less-than100gp,consumed versus nonconsumed components,actual focus use/hands,spell eligibility and any interaction with stored spells. Preserve the full description/effect; never apply a spell-component exception to crafting ingredients automatically."
}
```

### Final source decision

Retain NEW actual-focus component substitution below100gp; sum repeated reference requirements and preserve unpriced unique/irreplaceable bodies, V/S and all noncomponent costs.

### Complete candidate procedure

When you personally cast a spell you are actually entitled to cast, you may use a complete functional focus legal for that casting source to replace material-component requirements whose specified reference value is strictly less than100gp. NEW: this is an explicit exception for both consumed and nonconsumed components; total repeated units of the same required component within this cast before comparing the threshold. Components without an explicit price qualify as ordinary unpriced materials; a source-specific unique named object, target/body or expressly irreplaceable component does not become an unpriced generic material. A100gp component does not qualify. Hold/manipulate or display the focus exactly as the governing source permits; S,V,casting time,RP,concentration and other requirements remain. This feat cannot replace the actual target, a creature’s remains as a target, an item being enchanted or a required personally bonded object. For a reviewed Scribing payload actually cast by you, use the same cast-level rule only if otherwise eligible; activating a noncast magic item does not invoke this feat. Crafting ingredients, sacrificial recipe bodies, research costs and stored spell creation remain real unless their own exact procedure is a qualifying cast. Record each waived component and its stated reference value; market discounts cannot push an intrinsically100gp component under the threshold.

### Final authored examples

A legal cast calls for three20gp packets of the same consumed dust. The60gp total is below100gp and the actual source-legal focus replaces them. A separate100gp gem on that cast is still required.

Buying a100gp-reference pearl for90gp does not make it replaceable. A Scribing manufacture order still consumes its real ink and parchment even when a later eligible reader can waive a qualifying casting component.

### Preserved submitted procedure

When you personally cast a spell you are actually entitled to cast, you may use a complete functional focus legal for that casting source to replace material-component requirements whose specified reference value is strictly less than100gp. NEW: this is an explicit exception for both consumed and nonconsumed components; total repeated units of the same required component within this cast before comparing the threshold. Components without an explicit price qualify as ordinary unpriced materials; a source-specific unique named object, target/body or expressly irreplaceable component does not become an unpriced generic material. A100gp component does not qualify. Hold/manipulate or display the focus exactly as the governing source permits; S,V,casting time,RP,concentration and other requirements remain. This feat cannot replace the actual target, a creature’s remains as a target, an item being enchanted or a required personally bonded object. For a reviewed Scribing payload actually cast by you, use the same cast-level rule only if otherwise eligible; activating a noncast magic item does not invoke this feat. Crafting ingredients, sacrificial recipe bodies, research costs and stored spell creation remain real unless their own exact procedure is a qualifying cast. Record each waived component and its stated reference value; market discounts cannot push an intrinsically100gp component under the threshold.

### Preserved submitted examples

A legal cast calls for three20gp packets of the same consumed dust. The60gp total is below100gp and the actual source-legal focus replaces them. A separate100gp gem on that cast is still required.

Buying a100gp-reference pearl for90gp does not make it replaceable. A Scribing manufacture order still consumes its real ink and parchment even when a later eligible reader can waive a qualifying casting component.

## CTF-02 — Artisan

### Original complete object

```json
{
  "id": "artisan",
  "name": "Artisan",
  "description": "You are skilled in crafting.",
  "prerequisite": "Intelligence 13+",
  "effect": "Choose one type of artisan's tools. You gain proficiency and can create masterwork items.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Artisan credential and Masterwork wording",
  "question": "Choose the actual artisan tool,trade initialization and duplicate-training behavior. Decide what can create masterwork items authorizes against the quality table,formula/access and gear-grade rules; it need not mean automatic Masterwork outcome."
}
```

### Final source decision

Retain one actual artisan credential/trade1; Masterwork remains earned quality and access is not supplied.

### Complete candidate procedure

Choose one actual artisan-tool proficiency from the reviewed trade reference or another specifically profiled artisan tool; gain that proficiency. Initialize only its mapped trade at level1/zeroXP if previously untrained, retaining any existing greater level. NEW: “can create masterwork items” confirms access to that chosen tool’s legitimate Masterwork outcome when an otherwise authorized recipe/model qualifies; it is neither an automatic quality result nor access to every Masterwork-named recipe. Roll the existing quality procedure and satisfy trade level, formula, station, material and visibility gates. No generic creation bridge is granted by Artisan itself. Existing proficiency produces no automatic Expertise or free second choice; select an eligible unowned tool when available.

### Final authored examples

Selecting Weaver’s tools grants its proficiency and Tailoring1 if untrained. A legal recipe with result margin10 can yield its permitted Masterwork result, but a failed roll remains failed.

A level1 artisan cannot attempt a level12 restricted formula simply because its title contains Masterwork. Smith’s-tool ownership without the selected credential does not supply trained PB.

### Preserved submitted procedure

Choose one actual artisan-tool proficiency from the reviewed trade reference or another specifically profiled artisan tool; gain that proficiency. Initialize only its mapped trade at level1/zeroXP if previously untrained, retaining any existing greater level. NEW: “can create masterwork items” confirms access to that chosen tool’s legitimate Masterwork outcome when an otherwise authorized recipe/model qualifies; it is neither an automatic quality result nor access to every Masterwork-named recipe. Roll the existing quality procedure and satisfy trade level, formula, station, material and visibility gates. No generic creation bridge is granted by Artisan itself. Existing proficiency produces no automatic Expertise or free second choice; select an eligible unowned tool when available.

### Preserved submitted examples

Selecting Weaver’s tools grants its proficiency and Tailoring1 if untrained. A legal recipe with result margin10 can yield its permitted Masterwork result, but a failed roll remains failed.

A level1 artisan cannot attempt a level12 restricted formula simply because its title contains Masterwork. Smith’s-tool ownership without the selected credential does not supply trained PB.

## CTF-03 — Bowyer

### Original complete object

```json
{
  "id": "bowyer",
  "name": "Bowyer",
  "description": "You are skilled at crafting and using bows.",
  "prerequisite": "Proficiency with longbow or shortbow",
  "effect": "You can craft masterwork bows and arrows. Your ranged attacks with bows deal +1 damage.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Bow/arrows,physical grade and flat damage",
  "question": "Define the bow-making credential/formula/station and Masterwork meaning,alongside its separate+1 bow-attack damage. Resolve arrows versus bow output and existing weapon bonus families,critical hits and prerequisite weapon proficiency without erasing either clause."
}
```

### Final source decision

Retain narrow bow-craft credential and actual mundane-model bridge; personal bow damage and structural workmanship remain distinct.

### Complete candidate procedure

Keep the printed proficiency with Longbow or Shortbow acquisition gate. NEW: this feat grants the narrow trained Bowyer craft credential for the shared mundane-creation bridge: add PB once to DEX construction of Shortbow, Longbow or a20-Arrow retail bundle using actual carpenter’s tools and a suitable bench. It is not general carpenter proficiency, a new trade level or access to magical Blacksmithing formulas, whose host list excludes bows/ammunition. Masterwork means the bridge’s earned P50 durability option, not automatic grade/accuracy/damage. Separately, whenever you hit with a legal ranged attack actually made with a Shortbow or Longbow, add+1 to its ordinary weapon damage component. NEW: an explicitly profiled bow-family model also qualifies if its profile actually says bow; crossbow, sling, thrown arrow, spell or bow-butt improvised melee does not. The personal+1 works with any legally used bow, not just one you made; arrows you sell do not confer your personal bonus. Flat+1 is not doubled on a critical and does not add to separate poison or spell-rider components.

### Final authored examples

A bow hit with ordinary rolled weapon damage7 becomes8 before target defenses. A critical doubles its eligible damage dice, then adds this flat1 once.

A buyer firing an arrow you crafted gets that arrow’s actual profile, not your personal+1. Your separately legal crossbow shot receives no Bowyer damage bonus.

### Preserved submitted procedure

Keep the printed proficiency with Longbow or Shortbow acquisition gate. NEW: this feat grants the narrow trained Bowyer craft credential for the shared mundane-creation bridge: add PB once to DEX construction of Shortbow, Longbow or a20-Arrow retail bundle using actual carpenter’s tools and a suitable bench. It is not general carpenter proficiency, a new trade level or access to magical Blacksmithing formulas, whose host list excludes bows/ammunition. Masterwork means the bridge’s earned P50 durability option, not automatic grade/accuracy/damage. Separately, whenever you hit with a legal ranged attack actually made with a Shortbow or Longbow, add+1 to its ordinary weapon damage component. NEW: an explicitly profiled bow-family model also qualifies if its profile actually says bow; crossbow, sling, thrown arrow, spell or bow-butt improvised melee does not. The personal+1 works with any legally used bow, not just one you made; arrows you sell do not confer your personal bonus. Flat+1 is not doubled on a critical and does not add to separate poison or spell-rider components.

### Preserved submitted examples

A bow hit with ordinary rolled weapon damage7 becomes8 before target defenses. A critical doubles its eligible damage dice, then adds this flat1 once.

A buyer firing an arrow you crafted gets that arrow’s actual profile, not your personal+1. Your separately legal crossbow shot receives no Bowyer damage bonus.

## CTF-04 — Burglar

### Original complete object

```json
{
  "id": "burglar",
  "name": "Burglar",
  "description": "You are skilled at breaking and entering.",
  "prerequisite": "Dexterity 13+",
  "effect": "You gain proficiency with thieves' tools and can pick locks and disable traps more effectively.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Thieves tools and trap interaction",
  "question": "Bind the tool proficiency and more-effectively clause to actual lock/trap procedures. Decide whether any additional numeric or action benefit exists; do not turn it into permission to disarm every magical rune/device."
}
```

### Final source decision

The reviewed ordinary lock is already Action/DC15. Preserve it, +2 scoped tool checks and unchanged-state retry restriction.

### Complete candidate procedure

Gain thieves’-tools proficiency. NEW completion of “more effectively”: add+2 to actual checks using those tools to pick an accessible mechanical lock or safely disable an identified, accessible mechanical trap. PB still applies once; tool expertise replaces PB rather than adding another PB. This benefit does not reveal traps, find secret passages, open a structure without manipulating its lock or disarm an effect that has no usable mechanical disarm interface. Use the actual lock/trap’s printed time, DC, failure and retry procedure; for the reviewed ordinary mechanical lock, retain one Action and DC15, with failure consuming time and an unchanged-state retry requiring a materially different supported approach, better tools or new evidence. Simple obvious unlocked mechanisms need no roll. Magical devices keep explicit magical disarm requirements; a genuine mechanical safety on one can be manipulated only within its actual scope. This feat grants no trap immunity or faster-than-source Action. A different lock or trap without a governing profile requires its actual bounded mechanism/time/DC, not an automatic ordinary-lock conversion.

### Final authored examples

With DEX+3 and PB+2, an actual lock check gets+7 including this feat’s+2. If explicit tool Expertise applies, it gets+9, not+11.

A visible glyph with no mechanical switch offers no qualifying thieves’-tools attempt. A documented mechanical pressure switch can be disabled using its own DC/time without automatically removing a separate spell.

### Preserved submitted procedure

Gain thieves’-tools proficiency. NEW completion of “more effectively”: add+2 to actual checks using those tools to pick an accessible mechanical lock or safely disable an identified, accessible mechanical trap. PB still applies once; tool expertise replaces PB rather than adding another PB. This benefit does not reveal traps, find secret passages, open a structure without manipulating its lock or disarm an effect that has no usable mechanical disarm interface. Use the actual lock/trap’s printed time, DC, failure and retry procedure; if none exists, NEW ordinary accessible mechanical lock default is one minute and DC15, with failure consuming time and an unchanged-state retry requiring a materially different supported approach, better tools or new evidence. Simple obvious unlocked mechanisms need no roll. Magical devices keep explicit magical disarm requirements; a genuine mechanical safety on one can be manipulated only within its actual scope. This feat grants no trap immunity or generic faster Action.

### Preserved submitted examples

With DEX+3 and PB+2, an actual lock check gets+7 including this feat’s+2. If explicit tool Expertise applies, it gets+9, not+11.

A visible glyph with no mechanical switch offers no qualifying thieves’-tools attempt. A documented mechanical pressure switch can be disabled using its own DC/time without automatically removing a separate spell.

## CTF-05 — Craftsman

### Original complete object

```json
{
  "id": "craftsman",
  "name": "Craftsman",
  "description": "You are skilled in creating items.",
  "prerequisite": "Intelligence 13 or higher",
  "effect": "You gain proficiency with artisan's tools and can craft items in half the normal time.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Half-time creation and other reductions",
  "question": "Define craft-items scope,chosen tool(s),trade initialization and half-normal-time interaction with Forge Dwarf,fractional minutes,assistant hours and first phases. Distinguish creation from research,repair,harvest,training and servicing; source scope must be decided explicitly."
}
```

### Final source decision

Retain NEW strongest half active creation factor; actual first incorporation phase, paid labor and fixed calendar waits are controlled by the final common work rule.

### Complete candidate procedure

Choose one actual artisan-tool proficiency and initialize only its mapped trade if needed. NEW: the time benefit applies to creation work that you personally lead and are otherwise eligible to perform, including non-artisan creation trades, not merely your selected tool. Use half the ordinary active manufacturing time with the shared strongest-discount rule; all required assistants attend that adjusted work. This creates no general proficiency in other trades. It covers a recipe’s active creation phases, including the mundane bridge where separately authorized. It does not reduce repair, harvesting, preservation, teaching, research, formula copying, ritual casting, training, services merely using a completed item, rest, or independently fixed incubation/calendar waits. Recalculate a new order’s full required time before setting its phases; do not retroactively claim unworked time on an old order. A feat acquired mid-order changes only its remaining unworked active creation requirement, with completed work retained and the change logged once.

### Final authored examples

An ordinary8-hour eligible artisan order takes4hours with Craftsman; having Forge Dwarf as well still takes4hours, while its separate quality adjustment remains available.

A24-hour independent curing wait remains24hours. A2-hour self-repair is still2hours because repair is not creation, even if the repaired item was originally made with Craftsman.

### Preserved submitted procedure

Choose one actual artisan-tool proficiency and initialize only its mapped trade if needed. NEW: the time benefit applies to creation work that you personally lead and are otherwise eligible to perform, including non-artisan creation trades, not merely your selected tool. Use half the ordinary active manufacturing time with the shared strongest-discount rule; all required assistants attend that adjusted work. This creates no general proficiency in other trades. It covers a recipe’s active creation phases, including the mundane bridge where separately authorized. It does not reduce repair, harvesting, preservation, teaching, research, formula copying, ritual casting, training, services merely using a completed item, rest, or independently fixed incubation/calendar waits. Recalculate a new order’s full required time before setting its phases; do not retroactively claim unworked time on an old order. A feat acquired mid-order changes only its remaining unworked active creation requirement, with completed work retained and the change logged once.

### Preserved submitted examples

An ordinary8-hour eligible artisan order takes4hours with Craftsman; having Forge Dwarf as well still takes4hours, while its separate quality adjustment remains available.

A24-hour independent curing wait remains24hours. A2-hour self-repair is still2hours because repair is not creation, even if the repaired item was originally made with Craftsman.

## CTF-06 — Diligent Researcher

### Original complete object

```json
{
  "id": "diligent_researcher",
  "name": "Diligent Researcher",
  "description": "An Intelligence-trained researcher completes the listed library research in half the time.",
  "prerequisite": "Intelligence 13+",
  "effect": "When using a library, archive, or research facility, complete ordinary research in half the usual active time. This does not bypass access, language, or material requirements.",
  "type": "Skill",
  "legacyEffect": "Halve research time in libraries",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Research time and actual access",
  "question": "Define ordinary research,required library/archive/facility,active hours,task batching and combination with Scribing research aids. Preserve the explicit access/language/material restrictions; do not make a shorter research clock generate unavailable information or formulas."
}
```

### Final source decision

Retain half actual library research time, not copying/training, and strongest same-process factor with real evidence and access.

### Complete candidate procedure

While personally leading ordinary research with actual relevant library/archive/facility access, halve that task’s required active research time. NEW: ordinary research includes an already authorized formula-research or linguistic reconstruction project using qualifying relevant references; it does not grant the project, its evidence or its gated result. It excludes copying, encoding, teaching, language training, meditation, casting, crafting and separate elapsed waits. All source prerequisites, actual materials, staff/access charges and check/DC remain. A named Scribing research aid can supply its exact check bonus, while another research-time discount competes under the strongest single factor. Qualified project assistants must attend the adjusted required work; the feat does not discount their unrelated work. Use each project’s phase-credit precision, permitting its existing final fractional phase; there is no automatic new research batch, second roll or repeated unchanged-evidence retry.

### Final authored examples

An authorized8-hour decipher project using an actual archive takes4active hours; it still needs adequate evidence, one full check and access to the passage. An unavailable cipher key is not created by the time reduction.

A320-hour language course remains320hours under this feat. A Scribing research reference’s eligible+2 can affect the research check, but a second half-time source does not make4hours into2.

### Preserved submitted procedure

While personally leading ordinary research with actual relevant library/archive/facility access, halve that task’s required active research time. NEW: ordinary research includes an already authorized formula-research or linguistic reconstruction project using qualifying relevant references; it does not grant the project, its evidence or its gated result. It excludes copying, encoding, teaching, language training, meditation, casting, crafting and separate elapsed waits. All source prerequisites, actual materials, staff/access charges and check/DC remain. A named Scribing research aid can supply its exact check bonus, while another research-time discount competes under the strongest single factor. Qualified project assistants must attend the adjusted required work; the feat does not discount their unrelated work. Use each project’s phase-credit precision, permitting its existing final fractional phase; there is no automatic new research batch, second roll or repeated unchanged-evidence retry.

### Preserved submitted examples

An authorized8-hour decipher project using an actual archive takes4active hours; it still needs adequate evidence, one full check and access to the passage. An unavailable cipher key is not created by the time reduction.

A320-hour language course remains320hours under this feat. A Scribing research reference’s eligible+2 can affect the research check, but a second half-time source does not make4hours into2.

## CTF-07 — Forge

### Original complete object

```json
{
  "id": "forge",
  "name": "Forge",
  "description": "Racial feat tied to Dwarf heritage.",
  "prerequisite": "Dwarf heritage",
  "effect": "Forged – All crafted armor has +10% durability and you resist fire by +10%.",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Percentage durability and fire defense",
  "question": "Resolve all crafted armor+10% durability and resist fire by+10% against structural HP,craft workmanship,equipment grade and existing resistance. Define actor/output scope,rounding,selection,source prerequisite and whether an explicit new defense layer is needed; do not silently replace10% with normal resistance."
}
```

### Final source decision

Retain prospective armor-only P10 physical workmanship and distinct NEW personal10% fire reduction; do not reclassify armor or compound workmanship.

### Complete candidate procedure

Require actual Dwarf heritage. NEW: when you are the lead and personally complete a newly crafted armor suit, record a P10 physical durability workmanship source on that exact output. “All crafted armor” means your own completed outputs, including a lawful transformative recipe whose actual armor host qualifies; purchased suits or merely repaired suits do not acquire it. Shields are excluded unless an exact armor profile expressly includes them. Use the reviewed strongest percentage workmanship family: P10 competes with P25/P50 rather than multiplying. Compute baselineB after actual size/grade, improved maximum B+max(1,floor(B×P/100)) for positiveP, apply any persistent flaw last, and preserve the actual damage deficit. This is permanent physical workmanship, unaffected by magic suppression, with no automatic current-HP healing beyond the existing capacity/deficit calculation. Separately, your personal fire-damage defense is explicitly10%, not standard half resistance. NEW: after ordinary fire immunity/resistance/vulnerability and other passive flat reductions, multiply the remaining nonnegative fire component by0.90 and round down once for this step before later eligible reactions/tempHP. One Forge instance applies once; it does not improve another creature wearing your armor or turn your fire defense into20%.

### Final authored examples

Your Standard heavy armor baseline20 gainsP10 and maximum22. If it legitimately earnsP50 instead, maximum30 controls, not33. Merely repairing an old suit does not create a newP10 record.

An11-fire component becomes5 after normal resistance and its normal rounding, then4 after Forge’s0.90 step. A companion wearing your forged armor gains its workmanship, not your personal fire defense.

### Preserved submitted procedure

Require actual Dwarf heritage. NEW: when you are the lead and personally complete a newly crafted armor suit, record a P10 physical durability workmanship source on that exact output. “All crafted armor” means your own completed outputs, including a lawful transformative recipe whose actual armor host qualifies; purchased suits or merely repaired suits do not acquire it. Shields are excluded unless an exact armor profile expressly includes them. Use the reviewed strongest percentage workmanship family: P10 competes with P25/P50 rather than multiplying. Compute baselineB after actual size/grade, improved maximum B+max(1,floor(B×P/100)) for positiveP, apply any persistent flaw last, and preserve the actual damage deficit. This is permanent physical workmanship, unaffected by magic suppression, with no automatic current-HP healing beyond the existing capacity/deficit calculation. Separately, your personal fire-damage defense is explicitly10%, not standard half resistance. NEW: after ordinary fire immunity/resistance/vulnerability and other passive flat reductions, multiply the remaining nonnegative fire component by0.90 and round down once for this step before later eligible reactions/tempHP. One Forge instance applies once; it does not improve another creature wearing your armor or turn your fire defense into20%.

### Preserved submitted examples

Your Standard heavy armor baseline20 gainsP10 and maximum22. If it legitimately earnsP50 instead, maximum30 controls, not33. Merely repairing an old suit does not create a newP10 record.

An11-fire component becomes5 after normal resistance and its normal rounding, then4 after Forge’s0.90 step. A companion wearing your forged armor gains its workmanship, not your personal fire defense.

## CTF-08 — Herbalist

### Original complete object

```json
{
  "id": "herbalist",
  "name": "Herbalist",
  "description": "Nature-trained herbalists with Wisdom 13+ craft the listed advanced healing salves.",
  "prerequisite": "Nature 5+, Wisdom 13+",
  "effect": "Gain proficiency with an herbalism kit. During a long rest with supplies, create one healing salve that restores 1d6 + proficiency bonus hit points; unused salves spoil after 24 hours.",
  "type": "Skill",
  "legacyEffect": "Craft advanced healing salves",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Rest-time salve and recipe access",
  "question": "Bind herbalism proficiency,the Nature5+ prerequisite,actual supplies,one healing-salve output,activation and1d6+PB. Resolve Long Rest activity exception,expiry after24hours,stacking,reserve/value and whether the salve is distinct from reviewed Herbalism formulas."
}
```

### Final source decision

Retain one real herb remedy during a permitted beneficial-LR light activity with inputs, recipient access and24h expiry; no rest or stock duplication.

### Complete candidate procedure

Gain herbalism-kit proficiency; initialize Herbalism1/zeroXP if needed. Keep Nature5+ and WIS13 using the proposed permanent trained-skill bridge. NEW special rest procedure: during one otherwise legal Long Rest, spend30actual minutes of its allowed light activity preparing one salve with your functional kit, a clean working surface,0.5lb of genuinely suitable fresh mundane herbs/binder (ordinary reference1gp) and one actual sealable dose container. This is the feat’s explicit narrow rest-compatible preparation exception; it consumes those minutes, precludes simultaneous guarding/work and must still fit the governing rest’s allowed wakeful activity. Consume stock at preparation start. One output is created only when that same beneficial Long Rest completes; an interrupted nonbeneficial rest yields no salve and no refund. The completed salve records your PB then, expires24elapsed hours after completion, and has no automatic sale value/buyer. One Action, one hand and adjacency applies the whole dose to one living creature, including living at0HP; it restores1d6+recordedPB ordinary HP through the reviewed healing pipeline, then is consumed even if healing is blocked. No save, Wound removal, poison/disease cure or revival. Multiple genuinely created salves are independent consumed doses; no stacking passive buff. The feat supplies this one specific salve, not access to the separately reviewed Herbalism formulas, their quality/yield/XP, or unlimited supplies. More than one completion within the same actual rest identity is impossible.

### Final authored examples

A maker withPB3 completes the rest at06:00. The salve heals1d6+3 if used before06:00next day; transfer to aPB6 ally does not change its stored amount or expiration.

The herbs were consumed before an interruption prevented a beneficial rest. No dose appears. A later separately completed rest needs new stock; a previous spoiled salve cannot be relabeled fresh.

### Preserved submitted procedure

Gain herbalism-kit proficiency; initialize Herbalism1/zeroXP if needed. Keep Nature5+ and WIS13 using the proposed permanent trained-skill bridge. NEW special rest procedure: during one otherwise legal Long Rest, spend30actual minutes of its allowed light activity preparing one salve with your functional kit, a clean working surface,0.5lb of genuinely suitable fresh mundane herbs/binder (ordinary reference1gp) and one actual sealable dose container. This is the feat’s explicit narrow rest-compatible preparation exception; it consumes those minutes, precludes simultaneous guarding/work and must still fit the governing rest’s allowed wakeful activity. Consume stock at preparation start. One output is created only when that same beneficial Long Rest completes; an interrupted nonbeneficial rest yields no salve and no refund. The completed salve records your PB then, expires24elapsed hours after completion, and has no automatic sale value/buyer. One Action, one hand and adjacency applies the whole dose to one living creature, including living at0HP; it restores1d6+recordedPB ordinary HP through the reviewed healing pipeline, then is consumed even if healing is blocked. No save, Wound removal, poison/disease cure or revival. Multiple genuinely created salves are independent consumed doses; no stacking passive buff. The feat supplies this one specific salve, not access to the separately reviewed Herbalism formulas, their quality/yield/XP, or unlimited supplies. More than one completion within the same actual rest identity is impossible.

### Preserved submitted examples

A maker withPB3 completes the rest at06:00. The salve heals1d6+3 if used before06:00next day; transfer to aPB6 ally does not change its stored amount or expiration.

The herbs were consumed before an interruption prevented a beneficial rest. No dose appears. A later separately completed rest needs new stock; a previous spoiled salve cannot be relabeled fresh.

## CTF-09 — Jack of All Trades

### Original complete object

```json
{
  "id": "jack_of_all_trades",
  "name": "Jack of All Trades",
  "description": "Intelligence 12+ opens the listed two untrained skill slots.",
  "prerequisite": "Intelligence 12+",
  "effect": "Choose two skills in which you lack proficiency. Add half your proficiency bonus, rounded down, to checks using those skills.",
  "type": "General",
  "legacyEffect": "Gain 2 untrained skill slots",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Two untrained skill slots",
  "question": "Preserve the full current clause and legacyEffect. Define selection,half-PB floor,loss/retargeting after gaining proficiency and skill versus tool boundaries. It cannot be assumed to establish a trade credential or grant a second PB contribution."
}
```

### Final source decision

Retain two permanent missing-skill choices with halfPB replacing absent proficiency, not two Expertise grants or all tools.

### Complete candidate procedure

At acquisition choose two distinct actual skills in which you lack proficiency. On an actual check using one of those skills, add floor(currentPB/2) while you remain unproficient. This is the proficiency contribution, not a bonus added to a different full/half/expert proficiency contribution on the same check; use one actually applicable strongest contribution. It does not count as trained proficiency, satisfy a proficient prerequisite, initialize a trade, modify tools, attacks, saves or an unskilled ability check. NEW: if you later gain proficiency in a chosen skill, use that full contribution and retain the original selection as inactive; there is no free retargeting or banked choice. If that separate proficiency is actually lost, this feat’s same half-PB contribution can resume. No new skill slots or free respec are created by its legacy wording.

### Final authored examples

AtPB3 a chosen untrained History check adds1. If you later acquire History proficiency it adds3, not4; the feat does not grant a replacement chosen skill.

A Smith’s-tools crafting check receives no halfPB from a selected Engineering skill. This feat does not turn that character into a trained Blacksmith or satisfy an actual proficiency requirement.

### Preserved submitted procedure

At acquisition choose two distinct actual skills in which you lack proficiency. On an actual check using one of those skills, add floor(currentPB/2) while you remain unproficient. This is the proficiency contribution, not a bonus added to a different full/half/expert proficiency contribution on the same check; use one actually applicable strongest contribution. It does not count as trained proficiency, satisfy a proficient prerequisite, initialize a trade, modify tools, attacks, saves or an unskilled ability check. NEW: if you later gain proficiency in a chosen skill, use that full contribution and retain the original selection as inactive; there is no free retargeting or banked choice. If that separate proficiency is actually lost, this feat’s same half-PB contribution can resume. No new skill slots or free respec are created by its legacy wording.

### Preserved submitted examples

AtPB3 a chosen untrained History check adds1. If you later acquire History proficiency it adds3, not4; the feat does not grant a replacement chosen skill.

A Smith’s-tools crafting check receives no halfPB from a selected Engineering skill. This feat does not turn that character into a trained Blacksmith or satisfy an actual proficiency requirement.

## CTF-10 — Linguist

### Original complete object

```json
{
  "id": "linguist",
  "name": "Linguist",
  "description": "You have studied languages and codes.",
  "prerequisite": "Intelligence 14+",
  "effect": "Learn 3 additional languages",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Three languages and ancient-language gates",
  "question": "Preserve all description/effect clauses and define legal language selections,duplicate choices,fluency and any source limits. Resolve relation to Language Insight and texts without automatically granting every ancient/hidden language."
}
```

### Final source decision

Retain three LAX-constrained actual language choices; no cipher, general deciphering or bank from exhausted acquisition choices.

### Complete candidate procedure

Choose three distinct eligible language competencies not already fully known. Apply the reviewed permanent-language grant convention to their attested speaking/comprehension/reading/writing modes; a written-only tradition has only its actual modes. The Director’s genuine available choice/contact list, named-source restrictions and duplicate/exhaustion procedure control. This explicit acquisition grant needs no ordinary course or retroactive tuition, but invents no anatomy, teacher, protected curriculum, hidden-language authority, Cipher skill or Language Insight. NEW: the description’s study of codes is narrative only; the printed effect supplies no extra cipher DC, speed or automatic decoding. Existing known language does not make an unknown script’s contents true, complete or deciphered.

### Final authored examples

An eligible choice of ordinary Gnomish grants its actual spoken and written modes, with Dwarvish script familiarity, but does not also grant Orcish semantics.

An unspent choice can select an eligible missing written mode that the grant permits. An already completed choice cannot be exchanged every Long Rest for whichever inscription appears next.

### Preserved submitted procedure

Choose three distinct eligible language competencies not already fully known. Apply the reviewed permanent-language grant convention to their attested speaking/comprehension/reading/writing modes; a written-only tradition has only its actual modes. The Director’s genuine available choice/contact list, named-source restrictions and duplicate/exhaustion procedure control. This explicit acquisition grant needs no ordinary course or retroactive tuition, but invents no anatomy, teacher, protected curriculum, hidden-language authority, Cipher skill or Language Insight. NEW: the description’s study of codes is narrative only; the printed effect supplies no extra cipher DC, speed or automatic decoding. Existing known language does not make an unknown script’s contents true, complete or deciphered.

### Preserved submitted examples

An eligible choice of ordinary Gnomish grants its actual spoken and written modes, with Dwarvish script familiarity, but does not also grant Orcish semantics.

An unspent choice can select an eligible missing written mode that the grant permits. An already completed choice cannot be exchanged every Long Rest for whichever inscription appears next.

## CTF-11 — Merchant’s Guile

### Original complete object

```json
{
  "id": "merchant_s_guile",
  "name": "Merchant’s Guile",
  "description": "Charisma 13+ supports the feat's listed ten-percent improvement to trade prices.",
  "prerequisite": "Charisma 13+",
  "effect": "When buying or selling ordinary goods, improve the final negotiated price by up to 10 percent after a successful Persuasion, Deception, or relevant Profession check. This cannot override monopolies or fixed guild tariffs.",
  "type": "Skill",
  "legacyEffect": "+10% better prices on trade",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Negotiated prices and finite buyers",
  "question": "Define ordinary goods,relevant Profession/check DC/action,up-to10% direction and timing,stacking,minimum/maximum quotes,rounding and repeated negotiations. Preserve fixed tariffs/monopolies; no guaranteed market,arbitrage or automatic artifact-price modifier."
}
```

### Final source decision

Retain predeclared attainable mundane bargain and10% maximum; FEX03 binds the10min subtask within unchanged disposition/settlement work.

### Complete candidate procedure

Use with an actual willing transaction in ordinary mundane goods, a finite buyer/seller and a quoted quantity. Exclude artifacts, magic-item effects, labor/services, taxes, guild tariffs and monopolies unless their own exact rule expressly admits ordinary negotiation. NEW procedure: before the check the provider states its ordinary quote, whether the deal is negotiable, the supported improvement ceiling0–10%, the relevant approach and a concrete price-persuasion DC, default15 for an ordinary receptive negotiation. Spend10actual minutes and make CHA/Persuasion for honest bargaining, CHA/Deception for an actual plausible misrepresentation, or an actually applicable established Profession credential with its ordinary ability; this does not create a new Profession skill. Success or Critical Success gives the agreed ceiling, default10% if a negotiable ordinary deal has no smaller stated ceiling; Failure/Critical Failure gives no feat discount and preserves the source’s actual deception consequences. The result changes the final otherwise-negotiated purchase by×(1-ceiling) or sale by×(1+ceiling), before final copper rounding, with no double count of the same concession. NEW same concession family: multiple owners/repeated checks cannot compound this feat or claim another10% on the same deal. A change of speaker or splitting one order does not reset unchanged-state negotiation. Keep the actual provider’s predeclared floor/ceiling and refusal; no roll creates stock, consent or guaranteed profit. Reconcile the final58-question social/settlement verdict before adoption.

### Final authored examples

A real100gp ordinary sale quote with an agreed10% ceiling becomes110gp after a successful check. Two feat owners cannot turn that same negotiated deal into121gp.

A fixed guild tariff remains fixed. A separately willing ordinary seller offering only a3% concession gives3% on success, with the ceiling disclosed before work; the feat does not secretly convert success into a different costly-agreement outcome.

### Preserved submitted procedure

Use with an actual willing transaction in ordinary mundane goods, a finite buyer/seller and a quoted quantity. Exclude artifacts, magic-item effects, labor/services, taxes, guild tariffs and monopolies unless their own exact rule expressly admits ordinary negotiation. NEW procedure: before the check the provider states its ordinary quote, whether the deal is negotiable, the supported improvement ceiling0–10%, the relevant approach and a concrete price-persuasion DC, default15 for an ordinary receptive negotiation. Spend10actual minutes and make CHA/Persuasion for honest bargaining, CHA/Deception for an actual plausible misrepresentation, or an actually applicable established Profession credential with its ordinary ability; this does not create a new Profession skill. Success or Critical Success gives the agreed ceiling, default10% if a negotiable ordinary deal has no smaller stated ceiling; Failure/Critical Failure gives no feat discount and preserves the source’s actual deception consequences. The result changes the final otherwise-negotiated purchase by×(1-ceiling) or sale by×(1+ceiling), before final copper rounding, with no double count of the same concession. NEW same concession family: multiple owners/repeated checks cannot compound this feat or claim another10% on the same deal. A change of speaker or splitting one order does not reset unchanged-state negotiation. Keep the actual provider’s predeclared floor/ceiling and refusal; no roll creates stock, consent or guaranteed profit. Reconcile the final58-question social/settlement verdict before adoption.

### Preserved submitted examples

A real100gp ordinary sale quote with an agreed10% ceiling becomes110gp after a successful check. Two feat owners cannot turn that same negotiated deal into121gp.

A fixed guild tariff remains fixed. A separately willing ordinary seller offering only a3% concession gives3% on success, with the ceiling disclosed before work; the feat does not secretly convert success into a different costly-agreement outcome.

## CTF-12 — Polyglot

### Original complete object

```json
{
  "id": "polyglot",
  "name": "Polyglot",
  "description": "An Intelligence 14+ linguist gains the feat's listed three bonus spoken, read, and written languages.",
  "prerequisite": "Intelligence 14+",
  "effect": "Learn three languages of your choice and gain advantage on checks to identify unfamiliar dialects or scripts related to them.",
  "type": "Skill",
  "legacyEffect": "Speak, read, and write 3 bonus languages",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Languages and related-script advantage",
  "question": "Define the three language choices,related dialect/script scope,identification versus fluency and actual check timing. Combine with Scribing references and Language Insight without converting identification advantage into automatic translation."
}
```

### Final source decision

Retain three actual languages and their bounded dialect/script recognition; identification is not translation or universal fluency.

### Complete candidate procedure

Choose three distinct eligible languages using the same reviewed acquisition, availability, duplicate and attested-mode rules as Linguist. The current effect preserves the described spoken/read/written grant; no ordinary course is required for this explicit grant. Gain advantage only on an actually required check to identify an unfamiliar dialect or script genuinely related to one of these three recorded choices. Shared script can support a script-identification relationship without supplying semantic comprehension. Use the language guide’s ordinary one-minute recognition procedure and relevant INT/History DC10/15/20 as applicable. The advantage does not apply automatically to every translation, cipher, ancient script, communication or Language Insight check. An obvious known identity needs no roll; nondiagnostic evidence cannot become diagnostic by rolling twice. NEW: record the three choices as the specific family anchors; other languages known from unrelated sources do not expand this feat’s bonus.

### Final authored examples

You choose Gnomish through Polyglot. Its known Dwarvish script can support advantage to identify a diagnostic related inscription’s script, but the result does not teach the inscription’s unknown grammar.

A completely unrelated hidden cipher gains no Polyglot advantage just because you also speak Common. A plain text in a language you know needs no comprehension roll or advantage roll.

### Preserved submitted procedure

Choose three distinct eligible languages using the same reviewed acquisition, availability, duplicate and attested-mode rules as Linguist. The current effect preserves the described spoken/read/written grant; no ordinary course is required for this explicit grant. Gain advantage only on an actually required check to identify an unfamiliar dialect or script genuinely related to one of these three recorded choices. Shared script can support a script-identification relationship without supplying semantic comprehension. Use the language guide’s ordinary one-minute recognition procedure and relevant INT/History DC10/15/20 as applicable. The advantage does not apply automatically to every translation, cipher, ancient script, communication or Language Insight check. An obvious known identity needs no roll; nondiagnostic evidence cannot become diagnostic by rolling twice. NEW: record the three choices as the specific family anchors; other languages known from unrelated sources do not expand this feat’s bonus.

### Preserved submitted examples

You choose Gnomish through Polyglot. Its known Dwarvish script can support advantage to identify a diagnostic related inscription’s script, but the result does not teach the inscription’s unknown grammar.

A completely unrelated hidden cipher gains no Polyglot advantage just because you also speak Common. A plain text in a language you know needs no comprehension roll or advantage roll.

## CTF-13 — Prodigy

### Original complete object

```json
{
  "id": "prodigy",
  "name": "Prodigy",
  "description": "You have exceptional talent in multiple areas.",
  "prerequisite": "Half-elf, half-orc, or human",
  "effect": "You gain one skill proficiency, one tool proficiency, fluency in one language, and expertise in one skill.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Mixed grants and ancestry prerequisite",
  "question": "Map the literal Half-elf/half-orc/human requirement to current ancestry identities with actual evidence. Preserve skill,tool,language andexpertise grants; define duplicate choices and artisan versus any-tool scope. No ancestry/cosmology expansion is inferred."
}
```

### Final source decision

Retain literal ancestry gate, one skill/tool/language followed by one skill Expertise; grant ordering permits the newly learned skill.

### Complete candidate procedure

Retain the literal Half-elf, Half-orc or human prerequisite. The current Human identity qualifies; absent a genuine current or historical character receipt establishing Half-elf/Half-orc, do not infer eligibility from Elf, Orc, another mixed description or cosmetic name. At acquisition choose one new actual skill proficiency, one new actual tool proficiency from any genuinely profiled tool category, one eligible language grant, then one skill in which you are now proficient but do not already have Expertise. NEW: resolving in this order permits the newly gained skill to be the Expertise choice. Expertise replaces PB with2PB only for that skill’s checks; it is not doubled again by another Expertise source and grants no tool expertise. A primary-trade tool grant initializes its actual trade at1/zeroXP; other tools do not invent trades. Apply ordinary language modes/contact gates and duplicate/exhausted choices; no unprinted ability-score increase, ancestry transformation or repeat acquisition.

### Final authored examples

A Human chooses Investigation proficiency and then Investigation Expertise, thieves’ tools and an eligible language. AtPB3 its Investigation contribution is6; thieves’ tools still contributes only3 when applicable.

An Orc with no qualifying Half-orc receipt cannot acquire this feat by relabeling its ancestry. A preserved genuinely qualifying legacy character can retain that explicit receipt without creating a new ancestry catalog entry.

### Preserved submitted procedure

Retain the literal Half-elf, Half-orc or human prerequisite. The current Human identity qualifies; absent a genuine current or historical character receipt establishing Half-elf/Half-orc, do not infer eligibility from Elf, Orc, another mixed description or cosmetic name. At acquisition choose one new actual skill proficiency, one new actual tool proficiency from any genuinely profiled tool category, one eligible language grant, then one skill in which you are now proficient but do not already have Expertise. NEW: resolving in this order permits the newly gained skill to be the Expertise choice. Expertise replaces PB with2PB only for that skill’s checks; it is not doubled again by another Expertise source and grants no tool expertise. A primary-trade tool grant initializes its actual trade at1/zeroXP; other tools do not invent trades. Apply ordinary language modes/contact gates and duplicate/exhausted choices; no unprinted ability-score increase, ancestry transformation or repeat acquisition.

### Preserved submitted examples

A Human chooses Investigation proficiency and then Investigation Expertise, thieves’ tools and an eligible language. AtPB3 its Investigation contribution is6; thieves’ tools still contributes only3 when applicable.

An Orc with no qualifying Half-orc receipt cannot acquire this feat by relabeling its ancestry. A preserved genuinely qualifying legacy character can retain that explicit receipt without creating a new ancestry catalog entry.

## CTF-14 — Quick Learner

### Original complete object

```json
{
  "id": "quick_learner",
  "name": "Quick Learner",
  "description": "Intelligence 14+ supports instantly learning one language, tool, or lore.",
  "prerequisite": "Intelligence 14+",
  "effect": "After 30 days of downtime training, learn one language or tool proficiency. You may use this feat only once for each category.",
  "type": "Skill",
  "legacyEffect": "Learn one language, tool, or lore instantly",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Specific30-day training route",
  "question": "Define day/active-hour requirements,instructor/facility/cost,one use per category,eligible languages/tools and trade initialization. Reconcile with the reviewed80-active-hour ordinary trade route,which already defers to a named specific source; do not erase either time statement."
}
```

### Final source decision

Retain NEW two lifetime-category30day/120active-hour projects; no compression of the calendar, free teacher or triple work Watch.

### Complete candidate procedure

The current effect’s30days controls over the preserved instant/lore wording. NEW specific route: choose a language course or one tool proficiency, with a qualified willing instructor or a complete legitimately usable instructional curriculum. Each of30consecutive project days is an elapsed24-hour interval anchored to this project; complete4active hours of relevant training within each. No same hour counts for another project/work/rest, and missing the4-hour requirement ends this attempt while preserving actual learned fragments and costs; a new attempt requires a fresh30-day record. The project cannot finish before720elapsed hours and120active hours. Language grants use genuine available access and attested full ordinary modes; tools require actual practice kit and a qualified instructor, using the trade framework’s level5 teacher when a mapped trade is involved. NEW tuition reference follows actual instruction at1gp/8hours, so120teacher-hours ordinarily15gp, plus actual tools/facility/living costs; real voluntary/quoted terms may differ. Upon completion grant that proficiency/language once and mark that category used for this feat permanently: at most one language and one tool over its lifetime. The two category projects may be sequential, or concurrent only with distinct legal hours and participants. The ordinary80-hour trade route and ordinary language course remain available independently; this source-specific feat neither retimes those routes nor makes the unused category vanish. No lore credential, automatic Expertise, free formula or instantaneous learning.

### Final authored examples

A30-day tool project contributes4hours each day for120hours; the new mapped trade starts at1/zeroXP at completion. A normal80-hour course could still be chosen instead without spending this feat’s tool category.

Finishing twenty-nine days then spending only3hours on day30 does not finish the route. Past work and paid tuition remain real; it cannot be converted into a retroactive30-day completion by changing the date label.

### Preserved submitted procedure

The current effect’s30days controls over the preserved instant/lore wording. NEW specific route: choose a language course or one tool proficiency, with a qualified willing instructor or a complete legitimately usable instructional curriculum. Each of30consecutive project days is an elapsed24-hour interval anchored to this project; complete4active hours of relevant training within each. No same hour counts for another project/work/rest, and missing the4-hour requirement ends this attempt while preserving actual learned fragments and costs; a new attempt requires a fresh30-day record. The project cannot finish before720elapsed hours and120active hours. Language grants use genuine available access and attested full ordinary modes; tools require actual practice kit and a qualified instructor, using the trade framework’s level5 teacher when a mapped trade is involved. NEW tuition reference follows actual instruction at1gp/8hours, so120teacher-hours ordinarily15gp, plus actual tools/facility/living costs; real voluntary/quoted terms may differ. Upon completion grant that proficiency/language once and mark that category used for this feat permanently: at most one language and one tool over its lifetime. The two category projects may be sequential, or concurrent only with distinct legal hours and participants. The ordinary80-hour trade route and ordinary language course remain available independently; this source-specific feat neither retimes those routes nor makes the unused category vanish. No lore credential, automatic Expertise, free formula or instantaneous learning.

### Preserved submitted examples

A30-day tool project contributes4hours each day for120hours; the new mapped trade starts at1/zeroXP at completion. A normal80-hour course could still be chosen instead without spending this feat’s tool category.

Finishing twenty-nine days then spending only3hours on day30 does not finish the route. Past work and paid tuition remain real; it cannot be converted into a retroactive30-day completion by changing the date label.

## CTF-15 — Skill Expert

### Original complete object

```json
{
  "id": "skill_expert",
  "name": "Skill Expert",
  "description": "You have honed your proficiency with particular skills.",
  "prerequisite": "None",
  "effect": "You gain proficiency in one skill and expertise in one skill you're proficient with.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Skill expertise and tool double-counting",
  "question": "Specify skill proficiency/expertise choices,already-proficient requirement,order,duplicate expertise and later changes. A skill expertise grant is not automatic expertise in an associated crafting tool or a second proficiency bonus on one roll."
}
```

### Final source decision

Retain source-only proficiency plus Expertise, including selection of the new skill; no unprinted ability-score increase.

### Complete candidate procedure

Choose one actual skill in which you lack proficiency and gain it. Then choose one skill in which you are now proficient and lack Expertise; its applicable PB contribution becomes2PB. NEW: the newly chosen skill may be selected for Expertise. Record the two grants separately and preserve their acquisition order. No additional ability increase is inferred from a familiar external feat of the same name. Multiple Expertise sources never produce4PB, and skill Expertise does not automatically apply to an associated tool/crafting check. Choices are permanent unless an actual reviewed retraining procedure applies. If every eligible choice is already satisfied, record that portion exhausted with no extra resource or future floating selection.

### Final authored examples

You gain Medicine proficiency and select Medicine for Expertise in the same acquisition. PB2 contributes4to Medicine checks, once, rather than2+4.

Already having Arcana Expertise means choosing Arcana again adds nothing; choose another eligible proficient skill for the Expertise grant. Smith’s-tools crafting does not inherit Arcana Expertise.

### Preserved submitted procedure

Choose one actual skill in which you lack proficiency and gain it. Then choose one skill in which you are now proficient and lack Expertise; its applicable PB contribution becomes2PB. NEW: the newly chosen skill may be selected for Expertise. Record the two grants separately and preserve their acquisition order. No additional ability increase is inferred from a familiar external feat of the same name. Multiple Expertise sources never produce4PB, and skill Expertise does not automatically apply to an associated tool/crafting check. Choices are permanent unless an actual reviewed retraining procedure applies. If every eligible choice is already satisfied, record that portion exhausted with no extra resource or future floating selection.

### Preserved submitted examples

You gain Medicine proficiency and select Medicine for Expertise in the same acquisition. PB2 contributes4to Medicine checks, once, rather than2+4.

Already having Arcana Expertise means choosing Arcana again adds nothing; choose another eligible proficient skill for the Expertise grant. Smith’s-tools crafting does not inherit Arcana Expertise.

## CTF-16 — Skilled

### Original complete object

```json
{
  "id": "skilled",
  "name": "Skilled",
  "description": "You gain proficiency in any combination of three skills or tools of your choice.",
  "prerequisite": "None",
  "effect": "Gain proficiency in three skills or tools",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
{
  "topic": "Three skills/tools and starting choices",
  "question": "Specify distinct choices,eligible tool credentials,duplicate grants,trade level1 initialization and class/background interactions. Preserve any combination of three; distinguish broad tool choices from an artisan-only grant."
}
```

### Final source decision

Retain three distinct missing skills/tools, real primary trade initialization, no Expertise or repeatability.

### Complete candidate procedure

Choose any combination totaling three distinct eligible skill or tool proficiencies not already possessed. NEW: resolve fixed existing class/background grants first, then these actual choices in order. Any-tool scope includes profiled non-artisan tools such as Fishing tackle, Herbalism kit or thieves’ tools; it does not grant every tool in a kit family. Each primary-trade credential can initialize only its mapped trade at level1/zeroXP, while already higher lawful training remains. No Expertise, ability score, extra PB, formula or physical kit is granted. Choice exhaustion and later duplicates follow the shared rule; a later class/background gain does not freely retarget this historical selection. The feat is not repeatable under this proposal because the source does not say so.

### Final authored examples

Choosing Nature, Herbalism kit and Fishing tackle grants exactly those three proficiencies and can initialize Herbalism1 and Fishing1. It supplies neither physical kit nor food/ingredients.

Choosing the same skill three times is not Expertise. A later grant of one selected tool retains both provenance records but still gives one PB contribution and no new free choice.

### Preserved submitted procedure

Choose any combination totaling three distinct eligible skill or tool proficiencies not already possessed. NEW: resolve fixed existing class/background grants first, then these actual choices in order. Any-tool scope includes profiled non-artisan tools such as Fishing tackle, Herbalism kit or thieves’ tools; it does not grant every tool in a kit family. Each primary-trade credential can initialize only its mapped trade at level1/zeroXP, while already higher lawful training remains. No Expertise, ability score, extra PB, formula or physical kit is granted. Choice exhaustion and later duplicates follow the shared rule; a later class/background gain does not freely retarget this historical selection. The feat is not repeatable under this proposal because the source does not say so.

### Preserved submitted examples

Choosing Nature, Herbalism kit and Fishing tackle grants exactly those three proficiencies and can initialize Herbalism1 and Fishing1. It supplies neither physical kit nor food/ingredients.

Choosing the same skill three times is not Expertise. A later grant of one selected tool retains both provenance records but still gives one PB contribution and no new free choice.

## CTF-17 — Tinker Adept

### Original complete object

```json
{
  "id": "tinker_adept",
  "name": "Tinker Adept",
  "description": "Tinkering 5+ supports the listed +5 to complex mechanical repairs.",
  "prerequisite": "Tinkering 5+",
  "effect": "Gain +2 on checks to repair complex mechanisms. Repairs completed during a short rest restore additional durability equal to your proficiency bonus.",
  "type": "Skill",
  "legacyEffect": "+5 to complex mechanical repairs",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Complex repairs and extra durability",
  "question": "Define Tinkering5+ against the actual trade-level credential,+2 eligible checks,short-rest repair compatibility and additional durability equalPB. Decide current-HP restoration versus maximum-HP increase,caps,materials and once-per-repair behavior; avoid repeatable free permanent HP."
}
```

### Final source decision

Retain explicitly NEW <=30min actual repair/light-activity exception inside a beneficial Short Rest; existing long repair/service/charge rules are unchanged.

### Complete candidate procedure

Require actual trained Tinkering trade level5or higher. Keep current+2repair wording over the preserved+5description/legacy wording. Add+2 to an actual eligible check to repair a complex mechanical mechanism using its governing repair credential and procedure; merely being made of metal does not make an object complex. NEW definition: a functioning assembly with interdependent moving, timing, pressure or control components, including a qualifying trap, clockwork or siege mechanism; no generic magic repair permission is added. If an actual authorized repair completes during your own beneficial Short Rest, add currentPB to that repair’s structural-current-HP restoration, capped at its recorded maximum, once for the physical target and completed repair. NEW narrow rest exception permits at most30active repair minutes inside that Short Rest with compatible light activity, actual tools, materials and safe access; longer repairs must be done as work and do not receive the rest clause merely because an observer rests nearby. This never raises maximumHP, refreshes charges/service, repairs a missing body or turns an unsuccessful check into success. Most ordinary full-restoration repairs already reach maximum, so their extraPB is capped away; an actual partial-restoration repair can benefit. Neither the feat nor taking a rest creates a free generic repair attempt.
NEW rest-repair limit: the entire genuinely authorized repair procedure must fit within at most30active minutes of the owner’s real beneficial short rest. Completing only the last30minutes of an eight-hour reconstruction does not qualify. On success the bonus restores at mostPB additional currentHP within the existing maximum; it creates no extra maximum, missing primary body, service/recharge/fuel, RP or formula. Keep actual repair cost, prerequisites and complete required labor.

### Final authored examples

A permitted partial mechanical repair restores2of a device’s missing8HP during a legal rest; withPB3 this feat restores5total, not5maximumHP. Actual materials and the original procedure still apply.

A successful ordinary repair already restores the device to maximum10. Its additionalPB grants0extraHP, not a new maximum13, and repairing it again cannot permanently increase its durability.

### Preserved submitted procedure

Require actual trained Tinkering trade level5or higher. Keep current+2repair wording over the preserved+5description/legacy wording. Add+2 to an actual eligible check to repair a complex mechanical mechanism using its governing repair credential and procedure; merely being made of metal does not make an object complex. NEW definition: a functioning assembly with interdependent moving, timing, pressure or control components, including a qualifying trap, clockwork or siege mechanism; no generic magic repair permission is added. If an actual authorized repair completes during your own beneficial Short Rest, add currentPB to that repair’s structural-current-HP restoration, capped at its recorded maximum, once for the physical target and completed repair. NEW narrow rest exception permits at most30active repair minutes inside that Short Rest with compatible light activity, actual tools, materials and safe access; longer repairs must be done as work and do not receive the rest clause merely because an observer rests nearby. This never raises maximumHP, refreshes charges/service, repairs a missing body or turns an unsuccessful check into success. Most ordinary full-restoration repairs already reach maximum, so their extraPB is capped away; an actual partial-restoration repair can benefit. Neither the feat nor taking a rest creates a free generic repair attempt.

### Preserved submitted examples

A permitted partial mechanical repair restores2of a device’s missing8HP during a legal rest; withPB3 this feat restores5total, not5maximumHP. Actual materials and the original procedure still apply.

A successful ordinary repair already restores the device to maximum10. Its additionalPB grants0extraHP, not a new maximum13, and repairing it again cannot permanently increase its durability.

## CTF-18 — Versatile Artisan

### Original complete object

```json
{
  "id": "versatile_artisan",
  "name": "Versatile Artisan",
  "description": "Tool Proficiency supports the listed crafting from one additional discipline.",
  "prerequisite": "Tool Proficiency",
  "effect": "Craft items from one additional discipline.",
  "type": "Skill",
  "legacyEffect": "Craft items from one additional discipline",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "One additional discipline",
  "question": "Define discipline selection,primary-tool proficiency,trade level,formula/access,knowledge and prerequisites. Decide whether the source grants only cross-discipline use or a new trained credential; owning another kit cannot answer the question."
}
```

### Final source decision

Retain one real missing primary credential from16 disciplines at level1, including nonartisan disciplines; no borrowed skill levels.

### Complete candidate procedure

Keep the printed requirement for an actual tool proficiency; owning tools is insufficient. NEW complete interpretation: select one of the16reviewed crafting disciplines for which you do not yet have its primary credential. Gain that exact primary-tool proficiency and initialize the discipline at level1/zeroXP. This is the feat’s cross-discipline training grant, not an ability to use one existing kit in every trade or import your highest trade level. Selection can include a non-artisan discipline because the source says discipline, not artisan-tool category. All formula/skill-level/station/material and protected-knowledge gates remain. If all16are already trained, this grant is exhausted; it supplies no Expertise, second specialization or additional trade level. An unrelated tool proficiency can satisfy the printed acquisition requirement but does not itself train a trade before this selection.

### Final authored examples

A Blacksmith10 selects Herbalism and gains Herbalism-kit proficiency and Herbalism1/zeroXP. Herbalism recipes above4still need sufficient Herbalism level and actual formula access.

A trained thieves’-tools user can select Tinkering through this feat, but must obtain real Tinker’s tools and an appropriate station before manufacturing. Lockpicks do not transform into a workshop.

### Preserved submitted procedure

Keep the printed requirement for an actual tool proficiency; owning tools is insufficient. NEW complete interpretation: select one of the16reviewed crafting disciplines for which you do not yet have its primary credential. Gain that exact primary-tool proficiency and initialize the discipline at level1/zeroXP. This is the feat’s cross-discipline training grant, not an ability to use one existing kit in every trade or import your highest trade level. Selection can include a non-artisan discipline because the source says discipline, not artisan-tool category. All formula/skill-level/station/material and protected-knowledge gates remain. If all16are already trained, this grant is exhausted; it supplies no Expertise, second specialization or additional trade level. An unrelated tool proficiency can satisfy the printed acquisition requirement but does not itself train a trade before this selection.

### Preserved submitted examples

A Blacksmith10 selects Herbalism and gains Herbalism-kit proficiency and Herbalism1/zeroXP. Herbalism recipes above4still need sufficient Herbalism level and actual formula access.

A trained thieves’-tools user can select Tinkering through this feat, but must obtain real Tinker’s tools and an appropriate station before manufacturing. Lockpicks do not transform into a workshop.

## CTF-19 — Combat Engineering

### Original complete object

```json
{
  "id": "combat_engineering",
  "name": "Combat Engineering",
  "description": "Walls, choke points, and kill-zones—you treat battlefields as structures waiting to be built or broken. Prestige lineage: Sapper. completed from the existing development record.)",
  "prerequisite": "Intelligence 13+, proficiency in Engineering",
  "effect": "You can construct field fortifications, barricades, or emplaced cover in half the normal time; emplaced cover grants +2 AC (instead of +1) to allies behind it. You gain +2 to Engineering checks involving siege devices, bridges, and structural weak points. Once per short rest, you may designate a 10-foot choke point as a kill-zone for 1 minute: the first hostile creature entering it must succeed on a Dexterity save or take 2d6 damage (type chosen when built — piercing, fire, or bludgeoning) and have speed halved until the end of its turn.",
  "type": "Skill",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You can construct field fortifications, barricades, or emplaced cover in half the normal time; emplaced cover grants +2 AC (instead of +1) to allies behind it. You gain +2 to Engineering checks involving siege devices, bridges, and structural weak points. Once per short rest, you may designate a 10-foot choke point as a kill-zone for 1 minute: the first hostile creature entering it must succeed on a Dexterity save or take 2d6 damage (type chosen when built — piercing, fire, or bludgeoning) and have speed halved until the end of its turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Fortifications,siege checks and kill-zone",
  "question": "Define construction baselines,half-time,+2 versus+1 emplaced-cover AC,Engineering checks,10foot kill-zone build/activation/one-short-rest budget,DC,damage type and first-hostile event. Reconcile with normal cover and Tinkering traps without dropping its non-trap clauses."
}
```

### Final source decision

Retain full finite barricade and supervised kill-zone procedures, source+2 normalized to existing half cover, no compound time/output/XP.

### Complete candidate procedure

Halve active construction time for actual field fortifications, barricades or emplaced cover you personally lead; use the strongest applicable creation/construction discount once and pay for genuine materials, tools and participants. NEW fallback field-barricade profile: one5-foot-wide,3-foot-high braced wooden panel,20lb of real planks/bracing plus2gp ordinary hardware reference, carpenter’s or Tinker’s tools and60active minutes before this feat’s reduction; DC12 INT/Engineering at completion, binary Core task resolution. Success makes one physical20lb panel withAC15/10structuralHP; failure spends time and hardware, preserves only actually remaining reusable planks and creates no useful cover. This profile is not a crafting quality/yield/XP route. Larger works need their own complete plan and quantities, not an extrapolated instant fortress. Emplaced cover you build supplies the source+2AC where the actual obstruction provides half cover; the older+1comparison is retained as history, not added to the reviewed+2AC/+2DEX half-cover rule. Best cover only; no extra+2on top of ordinary cover. An obstruction too small to supply half cover gives no manufactured bonus. Add+2 to actual Engineering checks about siege devices, bridges or structural weak points, not every tool or attack roll.

NEW complete kill-zone procedure: spend10active minutes with actual tools and5lb of appropriate expendable mundane spikes, weights/cord or fuel/ignition supplies (reference10gp) preparing two adjacent5-foot ground squares within one10-foot choke point; select piercing, bludgeoning or fire before work. This is a fixed feat preparation, not another discounted recipe; supplies are consumed when preparing the setup. One setup per owner may exist, remains until moved/destroyed or24elapsed hours pass, and has one exposed control assemblyAC15/5HP. Spend an Action while conscious within30feet and able to see the prepared area to designate/arm it, expending one Short-Rest use for one minute. The first actual hostile entrant onto its ground during that minute, including forced arrival, triggers once if you are still conscious within30feet and can perceive that entry; ordinary occupants when armed and creatures flying above the ground do not enter its trigger. The entrant makes DEX saveDC8+PB+INT modifier snapshotted at activation; failure takes2d6chosen damage and halves all its nonteleport Speeds until the end of its current turn if it entered on that turn, otherwise until its next regular-turn end. Success avoids both. Discharge or timeout expends the setup; no repeat trigger, ally damage exemption on other traps, unused-use refund or remote knowledge. The zone ends if its control assembly is Broken, moved or disconnected from the prepared squares. This explicit manually supervised feat mechanism does not redefine ordinary Tinkering/rune traps.

### Final authored examples

A qualifying barricade takes30active minutes with this feat, not15when Craftsman is also present. A defender withhalf cover has+2AC/+2DEX from best cover, not+4AC.

Your activated piercing zone catches the first hostile grounded entrant; it succeeds its save and takes0damage. The setup is still discharged and the Short-Rest use remains spent; a second entrant triggers nothing.

### Preserved submitted procedure

Halve active construction time for actual field fortifications, barricades or emplaced cover you personally lead; use the strongest applicable creation/construction discount once and pay for genuine materials, tools and participants. NEW fallback field-barricade profile: one5-foot-wide,3-foot-high braced wooden panel,20lb of real planks/bracing plus2gp ordinary hardware reference, carpenter’s or Tinker’s tools and60active minutes before this feat’s reduction; DC12 INT/Engineering at completion, binary Core task resolution. Success makes one physical20lb panel withAC15/10structuralHP; failure spends time and hardware, preserves only actually remaining reusable planks and creates no useful cover. This profile is not a crafting quality/yield/XP route. Larger works need their own complete plan and quantities, not an extrapolated instant fortress. Emplaced cover you build supplies the source+2AC where the actual obstruction provides half cover; the older+1comparison is retained as history, not added to the reviewed+2AC/+2DEX half-cover rule. Best cover only; no extra+2on top of ordinary cover. An obstruction too small to supply half cover gives no manufactured bonus. Add+2 to actual Engineering checks about siege devices, bridges or structural weak points, not every tool or attack roll.

NEW complete kill-zone procedure: spend10active minutes with actual tools and5lb of appropriate expendable mundane spikes, weights/cord or fuel/ignition supplies (reference10gp) preparing two adjacent5-foot ground squares within one10-foot choke point; select piercing, bludgeoning or fire before work. This is a fixed feat preparation, not another discounted recipe; supplies are consumed when preparing the setup. One setup per owner may exist, remains until moved/destroyed or24elapsed hours pass, and has one exposed control assemblyAC15/5HP. Spend an Action while conscious within30feet and able to see the prepared area to designate/arm it, expending one Short-Rest use for one minute. The first actual hostile entrant onto its ground during that minute, including forced arrival, triggers once if you are still conscious within30feet and can perceive that entry; ordinary occupants when armed and creatures flying above the ground do not enter its trigger. The entrant makes DEX saveDC8+PB+INT modifier snapshotted at activation; failure takes2d6chosen damage and halves all its nonteleport Speeds until the end of its current turn if it entered on that turn, otherwise until its next regular-turn end. Success avoids both. Discharge or timeout expends the setup; no repeat trigger, ally damage exemption on other traps, unused-use refund or remote knowledge. The zone ends if its control assembly is Broken, moved or disconnected from the prepared squares. This explicit manually supervised feat mechanism does not redefine ordinary Tinkering/rune traps.

### Preserved submitted examples

A qualifying barricade takes30active minutes with this feat, not15when Craftsman is also present. A defender withhalf cover has+2AC/+2DEX from best cover, not+4AC.

Your activated piercing zone catches the first hostile grounded entrant; it succeeds its save and takes0damage. The setup is still discharged and the Short-Rest use remains spent; a second entrant triggers nothing.

## CTF-20 — Core Infusion

### Original complete object

```json
{
  "id": "core_infusion",
  "name": "Core Infusion",
  "description": "You drive elemental or arcane cores into steel and stone until the metal remembers how to burn, freeze, or sing. Prestige lineage: Forge Master. completed from the existing development record.)",
  "prerequisite": "Proficiency in Craft (Blacksmith), spellcasting ability or Engineering",
  "effect": "When you finish a long rest, you may infuse one weapon or armor you crafted with a minor property (e.g., +1 fire damage, +1 AC, or resistance to one energy type) for 24 hours. Relic-tier work requires a forge and rare materials. While wearing or wielding an item you infused, you gain +2 to Craft (Blacksmith) checks to repair it, and once per short rest you may re-roll one failed Craft check on that item.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you finish a long rest, you may infuse one weapon or armor you crafted with a minor property (e.g., +1 fire damage, +1 AC, or resistance to one energy type) for 24 hours. Relic-tier work requires a forge and rare materials. While wearing or wielding an item you infused, you gain +2 to Craft (Blacksmith) checks to repair it, and once per short rest you may re-roll one failed Craft check on that item.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Temporary imprints and personal crafting identity",
  "question": "Define the Long Rest infusion,one personally crafted weapon/armor,minor-property menu,24hour duration,Relic materials/forge and overwrite/removal. Separately resolve+2 repair and one-short-rest Craft reroll,eligibility,timing and interaction with permanent reviewed enhancements."
}
```

### Final source decision

Retain closed minor-property menu, personal manufacture provenance and one active owner/body imprint; worn/held repair access is an actual additional predicate.

### Complete candidate procedure

Require actual Smith’s-tools/Blacksmithing proficiency and either actual spellcasting ability or actual Engineering proficiency. At completion of your beneficial Long Rest, you may touch one functional weapon or armor suit for which you have a genuine personal lead-crafter receipt and place one infusion on it for24elapsed hours. NEW: your own qualifying transformative manufacture counts, but buying, repairing or merely assisting does not. One active infusion per owner; replacing it ends the old one. One infusion slot per body across all owners; a new consensual infusion replaces the existing one rather than adding. The creature holding/wearing it must actually allow the accessible operation; no remote overwrite.

Choose one NEW closed minor property: a weapon adds+1fire to each actual hit made with it; an armor suit gains+1AC in equipment.defense-enhancement; or either body grants resistance to one chosen acid,cold,fire,lightning or thunder damage type while actually properly worn as armor or wielded as a functional weapon. The+1fire is a flat component of the same hit, not critical-doubled or an independent proc; it does not enhance spells merely cast while holding the weapon. Resistances do not double with same-type resistance. The magical infusion suspends while Broken, suppressed, melded or otherwise unusable, with its original clock running; repair/unsuppression can resume the remaining time but cannot refresh it. It is magical item functionality, not a spell, concentration or Counterspell target. The feat grants no Relic item or additional Relic property: any actual Relic work still requires its specifically authorized design, rare materials, forge and access, beyond this closed menu.

While you actually wear/wield your own currently active, usable infused item, gain+2 to actual Blacksmithing repair checks on that same item. Once per Short Rest you may reroll one failed actual Craft check on that same item under the shared reroll timing while this wear/wield eligibility holds. NEW: Craft here includes otherwise authorized Blacksmithing creation/alteration/repair checks actually acting on that item, not unrelated Engineering or research. Physical work still needs the source’s real tools/position and safe access; wearing a suit during a repair is not automatically feasible. A Broken item supplies neither bonus nor reroll because it cannot be functionally worn/wielded for the infusion. The reroll expends only this allowance, pays no duplicate batch cost, and never resurrects an ineligible work order.

### Final authored examples

A personally made functional armor suit with an existing equipment.defense-enhancement+2gains no additionalAC from choosing this infusion’s+1. Choosing a real different resistance instead can supply that separate property.

An infused weapon breaks six hours into its24-hour duration. Its fire property and repair-check feat benefit suspend. Lawful repair four hours later can restore the remaining fourteen hours, not a new full day or free reroll while Broken.

### Preserved submitted procedure

Require actual Smith’s-tools/Blacksmithing proficiency and either actual spellcasting ability or actual Engineering proficiency. At completion of your beneficial Long Rest, you may touch one functional weapon or armor suit for which you have a genuine personal lead-crafter receipt and place one infusion on it for24elapsed hours. NEW: your own qualifying transformative manufacture counts, but buying, repairing or merely assisting does not. One active infusion per owner; replacing it ends the old one. One infusion slot per body across all owners; a new consensual infusion replaces the existing one rather than adding. The creature holding/wearing it must actually allow the accessible operation; no remote overwrite.

Choose one NEW closed minor property: a weapon adds+1fire to each actual hit made with it; an armor suit gains+1AC in equipment.defense-enhancement; or either body grants resistance to one chosen acid,cold,fire,lightning or thunder damage type while actually properly worn as armor or wielded as a functional weapon. The+1fire is a flat component of the same hit, not critical-doubled or an independent proc; it does not enhance spells merely cast while holding the weapon. Resistances do not double with same-type resistance. The magical infusion suspends while Broken, suppressed, melded or otherwise unusable, with its original clock running; repair/unsuppression can resume the remaining time but cannot refresh it. It is magical item functionality, not a spell, concentration or Counterspell target. The feat grants no Relic item or additional Relic property: any actual Relic work still requires its specifically authorized design, rare materials, forge and access, beyond this closed menu.

While you actually wear/wield your own currently active, usable infused item, gain+2 to actual Blacksmithing repair checks on that same item. Once per Short Rest you may reroll one failed actual Craft check on that same item under the shared reroll timing while this wear/wield eligibility holds. NEW: Craft here includes otherwise authorized Blacksmithing creation/alteration/repair checks actually acting on that item, not unrelated Engineering or research. Physical work still needs the source’s real tools/position and safe access; wearing a suit during a repair is not automatically feasible. A Broken item supplies neither bonus nor reroll because it cannot be functionally worn/wielded for the infusion. The reroll expends only this allowance, pays no duplicate batch cost, and never resurrects an ineligible work order.

### Preserved submitted examples

A personally made functional armor suit with an existing equipment.defense-enhancement+2gains no additionalAC from choosing this infusion’s+1. Choosing a real different resistance instead can supply that separate property.

An infused weapon breaks six hours into its24-hour duration. Its fire property and repair-check feat benefit suspend. Lawful repair four hours later can restore the remaining fourteen hours, not a new full day or free reroll while Broken.

## CTF-21 — Hardened Grip

### Original complete object

```json
{
  "id": "hardened_grip",
  "name": "Hardened Grip",
  "description": "Forge heat and battle strain forged your hands into vices. Your weapon stays until you decide otherwise. Prestige lineage: Forge Master. completed from the existing development record.)",
  "prerequisite": "Strength 15+",
  "effect": "You cannot be disarmed while conscious — a successful disarm attempt instead deals 1d4 bludgeoning to the attacker. You gain +2 to Craft (Blacksmith) checks and can wield weapons one size category larger without the normal penalty. Once per short rest, as a bonus action, you may lock your grip: until the start of your next turn, opportunity attacks against you have disadvantage and your next melee hit deals +1d6 damage if you have not moved more than 5 feet since locking.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You cannot be disarmed while conscious — a successful disarm attempt instead deals 1d4 bludgeoning to the attacker. You gain +2 to Craft (Blacksmith) checks and can wield weapons one size category larger without the normal penalty. Once per short rest, as a bonus action, you may lock your grip: until the start of your next turn, opportunity attacks against you have disadvantage and your next melee hit deals +1d6 damage if you have not moved more than 5 feet since locking.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Disarm,size,craft bonus and attack timing",
  "question": "Resolve the no-disarm rule/reflected1d4,consciousness,actual weapons,hands,+2 Craft(Blacksmith),larger weapon use and full bonus-action grip lock. Preserve the movement condition,opportunity-attack disadvantage,+1d6 and duration; no blanket Strongest rule erases unrelated clauses."
}
```

### Final source decision

Retain conscious legal weapon no-disarm replacement, exact nonrecursive retaliation, one-category handling and paid grip-lock timing.

### Complete candidate procedure

While conscious and actually holding a weapon in a legal grip, you cannot be involuntarily disarmed of that weapon. NEW: resolve an otherwise valid disarm attempt normally to determine whether it would succeed, then keep the weapon and deal1d4bludgeoning directly to that initiating attacker instead, subject to its ordinary defenses. This is the source’s special retaliation even for a legal ranged disarm; it is not an attack, critical hit, spell, weapon-damage proc or reflected copy, and cannot recursively trigger itself. A failed attempt deals nothing. It does not prevent voluntary release, destruction/Broken state, severed anatomy, a legal whole-body movement or losing consciousness, and does not protect unrelated held objects merely because they are called important. Add+2 to actual Craft(Blacksmith)/Smith’s-tools checks within the real tool scope. You may wield an actually profiled weapon one size category larger without the penalty imposed solely by that size mismatch; no extra size/damage/reach/hands/proficiency is created. This and Giant Strength confer the same one-category permission, not two categories.

Once per Short Rest, use a Bonus Action while conscious/capable and legally gripping a weapon to lock your grip. Until your next original regular-turn start, opportunity attacks against you have disadvantage. Separately, the next legal melee hit you make during that duration gains+1d6of its ordinary melee damage type only if your cumulative actual displacement since locking is at most5feet. NEW: count voluntary/forced movement, carried movement and actual teleport displacement; in-place rotation is0. Once displacement exceeds5feet, the damage opportunity is lost for this activation even if you return; the opportunity-attack disadvantage persists for its original duration. On the first qualifying hit commit the rider once, with its attack dice doubled on a critical, in the same event. No further rider, free attack or extra Reaction follows. Losing consciousness ends this activation; ending initiative preserves its next regular-start deadline through the existing six-second outside timing, without refresh. Extra turns do not advance the original regular-start expiry.

### Final authored examples

An attacker’s legal disarm would succeed while you consciously hold your sword. You retain it and resolve1d4bludgeoning against that attacker. An unrelated shove can still move you and counts against a current grip-lock movement limit.

After locking, you move5feet and land a melee critical; its single+1d6rider becomes2d6for that hit. If you had moved10feet and returned5, the rider would be lost even though your final location is close; opportunity attacks still have disadvantage until expiry.

### Preserved submitted procedure

While conscious and actually holding a weapon in a legal grip, you cannot be involuntarily disarmed of that weapon. NEW: resolve an otherwise valid disarm attempt normally to determine whether it would succeed, then keep the weapon and deal1d4bludgeoning directly to that initiating attacker instead, subject to its ordinary defenses. This is the source’s special retaliation even for a legal ranged disarm; it is not an attack, critical hit, spell, weapon-damage proc or reflected copy, and cannot recursively trigger itself. A failed attempt deals nothing. It does not prevent voluntary release, destruction/Broken state, severed anatomy, a legal whole-body movement or losing consciousness, and does not protect unrelated held objects merely because they are called important. Add+2 to actual Craft(Blacksmith)/Smith’s-tools checks within the real tool scope. You may wield an actually profiled weapon one size category larger without the penalty imposed solely by that size mismatch; no extra size/damage/reach/hands/proficiency is created. This and Giant Strength confer the same one-category permission, not two categories.

Once per Short Rest, use a Bonus Action while conscious/capable and legally gripping a weapon to lock your grip. Until your next original regular-turn start, opportunity attacks against you have disadvantage. Separately, the next legal melee hit you make during that duration gains+1d6of its ordinary melee damage type only if your cumulative actual displacement since locking is at most5feet. NEW: count voluntary/forced movement, carried movement and actual teleport displacement; in-place rotation is0. Once displacement exceeds5feet, the damage opportunity is lost for this activation even if you return; the opportunity-attack disadvantage persists for its original duration. On the first qualifying hit commit the rider once, with its attack dice doubled on a critical, in the same event. No further rider, free attack or extra Reaction follows. Losing consciousness ends this activation; ending initiative preserves its next regular-start deadline through the existing six-second outside timing, without refresh. Extra turns do not advance the original regular-start expiry.

### Preserved submitted examples

An attacker’s legal disarm would succeed while you consciously hold your sword. You retain it and resolve1d4bludgeoning against that attacker. An unrelated shove can still move you and counts against a current grip-lock movement limit.

After locking, you move5feet and land a melee critical; its single+1d6rider becomes2d6for that hit. If you had moved10feet and returned5, the rider would be lost even though your final location is close; opportunity attacks still have disadvantage until expiry.

## CTF-22 — Master Smithing

### Original complete object

```json
{
  "id": "master_smithing",
  "name": "Master Smithing",
  "description": "Kings queue for your steel. You measure temper, fold, and spell-work in the same breath. Prestige lineage: Forge Master. completed from the existing development record.)",
  "prerequisite": "Proficiency in Craft (Blacksmith), Intelligence 13+",
  "effect": "You can craft masterwork weapons and armor and work toward relic-tier items with appropriate materials and a forge access. Armor you craft reduces armor check penalty by 1 and may include one minor property (e.g., fire resistance 5, silent movement, or +1 to a saving throw) chosen at completion. Weapons you craft gain +1 to damage rolls; once per week you may temper one weapon you personally forged, granting it a named masterwork trait (flaming edge, returning throw, or spell-holding groove) that lasts until the weapon is broken or reforged.",
  "type": "Skill",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You can craft masterwork weapons and armor and work toward relic-tier items with appropriate materials and a forge access. Armor you craft reduces armor check penalty by 1 and may include one minor property (e.g., fire resistance 5, silent movement, or +1 to a saving throw) chosen at completion. Weapons you craft gain +1 to damage rolls; once per week you may temper one weapon you personally forged, granting it a named masterwork trait (flaming edge, returning throw, or spell-holding groove) that lasts until the weapon is broken or reforged.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Masterwork,minor properties and weekly temper",
  "question": "Resolve original Craft(Blacksmith) credential,recipe/forge/material access,armor check penalty-1,fire resistance5 or other minor-property examples,+1 weapon damage and weekly named trait. Give finite flaming/returning/spell-holding procedures or explicit outstanding decisions; do not treat their names as complete mechanics."
}
```

### Final source decision

Retain bounded personal workmanship and three complete weekly-temper traits; historical relic permission remains dependent on its actual design.

### Complete candidate procedure

Require actual Smith’s-tools/Blacksmithing proficiency and INT13. You may use the shared bounded mundane-creation bridge for its legal metal weapon/armor models, or an independently accessible reviewed recipe with all its original gates. “Masterwork” remains an earned quality result, not automatic equipment grade. Relic-tier work still needs an actual authorized design, rare materials, forge and access; this feat does not create a new relic catalog or bypass protected content.

NEW on genuine personal lead completion: an armor suit you craft reduces by1 an actual numeric armor-check penalty imposed by that suit, minimum0penalty; it creates no such penalty where none exists and does not remove Stealth disadvantage or a STR/Load/nonproficiency consequence. At completion choose at most one permanent minor armor property: flat fire reduction5after normal fire resistance/vulnerability but before Forge’s percentage layer; silent movement removing only that suit’s own armor-Stealth disadvantage; or+1to one chosen ability’s saving throws in the existing equipment.jewel-save-enhancement family. The fire/silence/save property is magical, suspends while the suit is Broken, suppressed, melded or improperly worn, and resumes only if the actual suit is lawfully restored. The numeric armor-check workmanship is physical. These properties do not themselves confer a generic new equipment grade, formula, enchantment slot or immunity. Your genuinely crafted weapon gains a permanent physical+1to its ordinary weapon-damage component on a legal hit, usable by its actual wielder; no automatic magical damage eligibility or critical doubling of the flat bonus. One same-feat workmanship identity per physical output, not another+1on each later alteration.

NEW weekly temper: no earlier than168elapsed hours after your previous successful temper completion, spend8active hours at an actual forge with Smith’s tools,25gp-reference/1lb of actual suitable tempering metal,resin and ink stock and one functional weapon you personally forged. This fixed alteration is not creation-time-discounted; no extra quality roll, output or XP. Commit supplies at start and finish only after all work; interrupted phases follow the craft framework. Record completion and select one named trait below. One trait slot per body; replacing a trait requires another lawful temper and ends the old one. Its magical trait lasts until the weapon becomes Broken or is actually reforged; breaking ends it permanently, ordinary repair does not restore it. Suppression merely pauses usable benefits while the body survives.

Flaming edge: on one actual legal weapon hit per actual turn, you may add1d4fire as part of that same event, doubled on an attack critical. NEW: it shares the weapon’s one printed-elemental-rider expenditure family with any actual Blacksmithing elemental rider; choose one qualifying rider, do not spend the same item/turn for both. Use the reviewed Blacksmithing outside-window, host-turn and transition-guard procedure in full, including persistent physical identity and no refund after mitigation.

Returning throw: after a legal thrown attack with this actual weapon resolves, it may immediately return along a clear unobstructed route of at most60feet to its thrower. An actual compatible free hand catches it; otherwise it lands at the thrower’s feet. It cannot return while Broken, caught/held by another creature, pinned, or across an impassable obstruction; no teleport, automatic escape from custody, extra attack or altered weapon range. An ammunition weapon itself being improvised-thrown uses its actual legal attack, but fired arrows are different bodies and do not inherit this trait.

Spell-holding groove: NEW one-use inscription capacity, not a stored paid cast. An eligible caster spends10active minutes with writing implements and5gp of actual suitable ink to encode one exact independently reviewed ordinary rank1spell the caster genuinely knows through a current casting source. Keep its source identity and complete restrictions; encoding spends noRP and grants no class/list/rank access. One eligible reader may later use that one payload under the reviewed Scribing temporary-repertoire casting rule: actual class/list placement, level/rank, ordinary RP,components,casting time,concentration and cadence all apply; commit and erase the inscription when the cast commits, even if countered. Actual accessible readable groove, functional weapon and source-legal free hands are required; wielding this weapon is not automatically a focus. It gives no extra Action, attack-triggered free spell, automatic hit or spell damage added to a weapon attack. One groove/one payload; a new encoding replaces an unspent one with new work/ink. Ending/breaking/reforging the trait destroys its inscription without a refund.

### Final authored examples

You craft an ordinary suit with no numeric armor-check penalty and choose silent movement. There is no invented-1check bonus; only the suit’s own Stealth disadvantage is removed while that magical property functions, leaving Burden or other Stealth disadvantages intact.

A tempered flaming weapon becomes Broken after its rider was spent. Repair restores its legal body and permanent physical craft workmanship, but not the ended temper trait or a fresh rider budget. A later lawful temper needs the168-hour cadence,8hours and real stock again.

### Preserved submitted procedure

Require actual Smith’s-tools/Blacksmithing proficiency and INT13. You may use the shared bounded mundane-creation bridge for its legal metal weapon/armor models, or an independently accessible reviewed recipe with all its original gates. “Masterwork” remains an earned quality result, not automatic equipment grade. Relic-tier work still needs an actual authorized design, rare materials, forge and access; this feat does not create a new relic catalog or bypass protected content.

NEW on genuine personal lead completion: an armor suit you craft reduces by1 an actual numeric armor-check penalty imposed by that suit, minimum0penalty; it creates no such penalty where none exists and does not remove Stealth disadvantage or a STR/Load/nonproficiency consequence. At completion choose at most one permanent minor armor property: flat fire reduction5after normal fire resistance/vulnerability but before Forge’s percentage layer; silent movement removing only that suit’s own armor-Stealth disadvantage; or+1to one chosen ability’s saving throws in the existing equipment.jewel-save-enhancement family. The fire/silence/save property is magical, suspends while the suit is Broken, suppressed, melded or improperly worn, and resumes only if the actual suit is lawfully restored. The numeric armor-check workmanship is physical. These properties do not themselves confer a generic new equipment grade, formula, enchantment slot or immunity. Your genuinely crafted weapon gains a permanent physical+1to its ordinary weapon-damage component on a legal hit, usable by its actual wielder; no automatic magical damage eligibility or critical doubling of the flat bonus. One same-feat workmanship identity per physical output, not another+1on each later alteration.

NEW weekly temper: no earlier than168elapsed hours after your previous successful temper completion, spend8active hours at an actual forge with Smith’s tools,25gp-reference/1lb of actual suitable tempering metal,resin and ink stock and one functional weapon you personally forged. This fixed alteration is not creation-time-discounted; no extra quality roll, output or XP. Commit supplies at start and finish only after all work; interrupted phases follow the craft framework. Record completion and select one named trait below. One trait slot per body; replacing a trait requires another lawful temper and ends the old one. Its magical trait lasts until the weapon becomes Broken or is actually reforged; breaking ends it permanently, ordinary repair does not restore it. Suppression merely pauses usable benefits while the body survives.

Flaming edge: on one actual legal weapon hit per actual turn, you may add1d4fire as part of that same event, doubled on an attack critical. NEW: it shares the weapon’s one printed-elemental-rider expenditure family with any actual Blacksmithing elemental rider; choose one qualifying rider, do not spend the same item/turn for both. Use the reviewed Blacksmithing outside-window, host-turn and transition-guard procedure in full, including persistent physical identity and no refund after mitigation.

Returning throw: after a legal thrown attack with this actual weapon resolves, it may immediately return along a clear unobstructed route of at most60feet to its thrower. An actual compatible free hand catches it; otherwise it lands at the thrower’s feet. It cannot return while Broken, caught/held by another creature, pinned, or across an impassable obstruction; no teleport, automatic escape from custody, extra attack or altered weapon range. An ammunition weapon itself being improvised-thrown uses its actual legal attack, but fired arrows are different bodies and do not inherit this trait.

Spell-holding groove: NEW one-use inscription capacity, not a stored paid cast. An eligible caster spends10active minutes with writing implements and5gp of actual suitable ink to encode one exact independently reviewed ordinary rank1spell the caster genuinely knows through a current casting source. Keep its source identity and complete restrictions; encoding spends noRP and grants no class/list/rank access. One eligible reader may later use that one payload under the reviewed Scribing temporary-repertoire casting rule: actual class/list placement, level/rank, ordinary RP,components,casting time,concentration and cadence all apply; commit and erase the inscription when the cast commits, even if countered. Actual accessible readable groove, functional weapon and source-legal free hands are required; wielding this weapon is not automatically a focus. It gives no extra Action, attack-triggered free spell, automatic hit or spell damage added to a weapon attack. One groove/one payload; a new encoding replaces an unspent one with new work/ink. Ending/breaking/reforging the trait destroys its inscription without a refund.

### Preserved submitted examples

You craft an ordinary suit with no numeric armor-check penalty and choose silent movement. There is no invented-1check bonus; only the suit’s own Stealth disadvantage is removed while that magical property functions, leaving Burden or other Stealth disadvantages intact.

A tempered flaming weapon becomes Broken after its rider was spent. Repair restores its legal body and permanent physical craft workmanship, but not the ended temper trait or a fresh rider budget. A later lawful temper needs the168-hour cadence,8hours and real stock again.

## CTF-23 — Siege Savant

### Original complete object

```json
{
  "id": "siege_savant",
  "name": "Siege Savant",
  "description": "You read walls like books—knowing which stone sighs before it falls. Prestige lineage: Sapper. completed from the existing development record.)",
  "prerequisite": "Proficiency in Engineering",
  "effect": "You deal +20% damage to constructs, fortifications, and siege engines. Explosives you deploy have +5 feet radius and ignore half cover on the detonation save. You can identify structural weak points with a successful Engineering check, granting allies advantage on the next attack against that structure or construct. Once per short rest, you may collapse a 5-foot section of mundane wall or barricade you have studied for 1 round, creating difficult terrain and granting allies half cover behind the rubble until cleared.",
  "type": "Skill",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You deal +20% damage to constructs, fortifications, and siege engines. Explosives you deploy have +5 feet radius and ignore half cover on the detonation save. You can identify structural weak points with a successful Engineering check, granting allies advantage on the next attack against that structure or construct. Once per short rest, you may collapse a 5-foot section of mundane wall or barricade you have studied for 1 round, creating difficult terrain and granting allies half cover behind the rubble until cleared.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Percent damage,blast radius and structure actions",
  "question": "Resolve+20% target-specific damage/rounding,explosive radius+5feet,half-cover save bypass,weak-point check/next-attack advantage and studied5foot wall collapse. Bind Tinkering siege/traps,actual structure defenses,actions and short-rest budget; no unsupported exemption for magical/unique barriers."
}
```

### Final source decision

Retain literal broad eligible source event, existing actual target authorization, proportional20% arithmetic, finite diagnostic/collapse procedures.

### Complete candidate procedure

Require actual Engineering proficiency. You deal+20%damage with an actual personally caused eligible damage event against a creature actually typed Construct, an independently profiled fortification component or a siege-engine body. NEW: this includes legal direct weapon/spell damage and a genuinely attributable deployed explosive/trap, but grants no object targeting to creature-only effects and excludes copied/reflected damage, another operator’s event, HP-cost payments and a rider already counted through the same event. Determine eligible ordinary damage components including their normal dice and flat bonuses before target defenses; compute one bonus floor(0.20×their nonnegative total). Allocate that integer bonus proportionally among their actual damage types by largest remainder, with ties in the event’s recorded component order; this preserves types and avoids rounding every small component up. Do not recursively increase other percentage bonuses or the generated bonus. Apply actual defenses after the increase; this feature alone does not make damage magical.

An actual explosive you personally deploy gains+5feet to its explicitly circular/spherical blast radius, and targets do not receive half-cover bonuses on that explosion’s actual detonation save. NEW: do not invent a save or radius for a single-target/nonradial effect; three-quarters and total cover remain, and targeting/origin/line rules still apply. Allies are not exempt from the enlarged area. A source expressly prohibiting modification keeps that prohibition. Nonexplosive spells do not become explosives by description.

NEW weak-point study: spend an Action observing a visible structure/component or Construct within60feet and make INT/Engineering againstDC15for ordinary visible engineering orDC20for a genuinely unusual but diagnostically exposed design. An unsupported/fully hidden weakness cannot be invented. On Success/Critical Success, identify one actual weak point to allies who can perceive your explanation within30feet; the next legal attack by one such informed ally against that exact target within1minute has advantage, consumed when declared even if advantage cancels. The marker does not stack and expires if the structure meaningfully changes. Failure allows a retry only after genuinely changed evidence/method, not another free look each round.

Once per Short Rest, after studying one actual mundane wall/barricade section within30feet continuously from your regular-turn start through the start of your next regular turn (six elapsed seconds outside initiative), spend an Action adjacent to it with actual suitable demolition tools to collapse one exposed section at most5feet wide,5feet high and1foot thick. NEW size bounds complete “5-foot section”; thicker bodies lose only that genuine separable section, not an invented tunnel through the remaining wall. A wholly magical barrier is ineligible; a unique mundane wall is not immune merely by its name. The section must be physically reachable and its collapse possible from the actual exposed construction; no automatic reach through other walls. Record real structural/load consequences before use; this does not automatically collapse an entire building. The selected section becomes actual rubble in its original footprint, ordinary difficult terrain and half cover for creatures genuinely positioned behind it, including enemies where the same physical cover applies. It remains until real work clears it. NEW generic clearing is10active minutes per collapsed section with suitable tools/storage for displaced rubble; missing destination or tools prevents clearance. No automatic crushing damage or ejection into occupied space is created; use an independently supported hazard if actual bystanders/loads require one.

### Final authored examples

An eligible event has3piercing and3fire before defenses. Its6total adds1bonus; equal remainders give that1to the first recorded component, producing4piercing/3fire before separate defenses, not an untyped bonus.

A10-foot-radius explosive becomes15feet and ignores half-cover save bonuses, affecting actual allies too. Total cover can still exclude a target; this feature never changes an ordinary single-target Fire Bolt into a blast.

### Preserved submitted procedure

Require actual Engineering proficiency. You deal+20%damage with an actual personally caused eligible damage event against a creature actually typed Construct, an independently profiled fortification component or a siege-engine body. NEW: this includes legal direct weapon/spell damage and a genuinely attributable deployed explosive/trap, but grants no object targeting to creature-only effects and excludes copied/reflected damage, another operator’s event, HP-cost payments and a rider already counted through the same event. Determine eligible ordinary damage components including their normal dice and flat bonuses before target defenses; compute one bonus floor(0.20×their nonnegative total). Allocate that integer bonus proportionally among their actual damage types by largest remainder, with ties in the event’s recorded component order; this preserves types and avoids rounding every small component up. Do not recursively increase other percentage bonuses or the generated bonus. Apply actual defenses after the increase; this feature alone does not make damage magical.

An actual explosive you personally deploy gains+5feet to its explicitly circular/spherical blast radius, and targets do not receive half-cover bonuses on that explosion’s actual detonation save. NEW: do not invent a save or radius for a single-target/nonradial effect; three-quarters and total cover remain, and targeting/origin/line rules still apply. Allies are not exempt from the enlarged area. A source expressly prohibiting modification keeps that prohibition. Nonexplosive spells do not become explosives by description.

NEW weak-point study: spend an Action observing a visible structure/component or Construct within60feet and make INT/Engineering againstDC15for ordinary visible engineering orDC20for a genuinely unusual but diagnostically exposed design. An unsupported/fully hidden weakness cannot be invented. On Success/Critical Success, identify one actual weak point to allies who can perceive your explanation within30feet; the next legal attack by one such informed ally against that exact target within1minute has advantage, consumed when declared even if advantage cancels. The marker does not stack and expires if the structure meaningfully changes. Failure allows a retry only after genuinely changed evidence/method, not another free look each round.

Once per Short Rest, after studying one actual mundane wall/barricade section within30feet continuously from your regular-turn start through the start of your next regular turn (six elapsed seconds outside initiative), spend an Action adjacent to it with actual suitable demolition tools to collapse one exposed section at most5feet wide,5feet high and1foot thick. NEW size bounds complete “5-foot section”; thicker bodies lose only that genuine separable section, not an invented tunnel through the remaining wall. A wholly magical barrier is ineligible; a unique mundane wall is not immune merely by its name. The section must be physically reachable and its collapse possible from the actual exposed construction; no automatic reach through other walls. Record real structural/load consequences before use; this does not automatically collapse an entire building. The selected section becomes actual rubble in its original footprint, ordinary difficult terrain and half cover for creatures genuinely positioned behind it, including enemies where the same physical cover applies. It remains until real work clears it. NEW generic clearing is10active minutes per collapsed section with suitable tools/storage for displaced rubble; missing destination or tools prevents clearance. No automatic crushing damage or ejection into occupied space is created; use an independently supported hazard if actual bystanders/loads require one.

### Preserved submitted examples

An eligible event has3piercing and3fire before defenses. Its6total adds1bonus; equal remainders give that1to the first recorded component, producing4piercing/3fire before separate defenses, not an untyped bonus.

A10-foot-radius explosive becomes15feet and ignores half-cover save bonuses, affecting actual allies too. Total cover can still exclude a target; this feature never changes an ordinary single-target Fire Bolt into a blast.

## CTF-24 — Trapsetter

### Original complete object

```json
{
  "id": "trapsetter",
  "name": "Trapsetter",
  "description": "Tripwire, caltrop, and charge—the ground remembers your name and bites when asked. Prestige lineage: Sapper. completed from the existing development record.)",
  "prerequisite": "Proficiency in Engineering or Disable Device",
  "effect": "You can set a mechanical trap as a bonus action (once per short rest per trap type: snare, caltrop field, or spring-loaded charge). Traps may stun, burn, or slow on a failed save (DC 8 + proficiency + Intelligence modifier). You gain advantage on checks to spot hidden traps and tunnels within 30 feet. When a creature triggers a trap you placed, you may use your reaction to move up to half your speed without provoking opportunity attacks from that creature, repositioning behind cover or into a prepared kill-zone.",
  "type": "Skill",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You can set a mechanical trap as a bonus action (once per short rest per trap type: snare, caltrop field, or spring-loaded charge). Traps may stun, burn, or slow on a failed save (DC 8 + proficiency + Intelligence modifier). You gain advantage on checks to spot hidden traps and tunnels within 30 feet. When a creature triggers a trap you placed, you may use your reaction to move up to half your speed without provoking opportunity attacks from that creature, repositioning behind cover or into a prepared kill-zone.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
{
  "topic": "Fast placement and trap-specific budget",
  "question": "Define the three listed mechanical trap types,physical supplies,bonus action,once per short rest per type,save DC,effect choice/duration and detection advantage. Preserve reaction movement after triggering,range/line of sight,cover and no-opportunity-attack scope; do not equate every Rune/Tinkering formula with one of these types."
}
```

### Final source decision

Restore persistent ordinary caltrop hazard and physical disarm; retain finite prepared snare/charge, setup budgets and source-scoped reaction movement without remote deletion or recycled hard denial.

### Complete candidate procedure

Require Engineering proficiency or the proposed mechanical Disable Device/thieves’-tools credential. NEW three closed prepared-kit options use genuine physical parts and no invented recipe/craft XP: snare (5gp reference,2lb cord/spring/anchor), caltrop field (the actual ordinary20-caltrop source bag, preserving its price/weight), and spring-loaded charge (25gp reference,3lb trigger body plus actual prepared combustible filling). Availability and assembly are real: obtain a genuinely prepared kit from an actual provider, or spend30active minutes with suitable mechanical tools and the same actual parts, DC12 INT/Engineering or DEX/thieves’-tools, using Core binary task outcome. Failure consumes time and expendable cord/filling, retaining only real recoverable frame/metal parts; no free complete kit. The new reference prices are complete kit references, not added again to their component prices. No ordinary Rune or Tinkering formula is silently renamed one of these three options.

Place one held/accessible prepared kit in a real stable unoccupied5-foot ground square within5feet. Normally this feat procedure takes an Action; once per Short Rest for each of the three types, you may use a Bonus Action instead, spending that type’s separate quick-placement allowance. NEW one armed trap of each type per setter; a new enhanced trap of that type cannot arm until the old trap has actually been safely disarmed, discharged, collected or destroyed through a lawful physical event. Merely arming a replacement or changing custody cannot remotely disable an existing trap. Ordinary unenhanced caltrop placements retain their own item rule. It arms at your next original regular-turn start, or after six elapsed seconds outside initiative, preserving the same deadline across mode changes. SnapshotDC8+PB+INT modifier at placement. For snare and charge, the first actual grounded creature entering from outside, including an ally, forced movement or teleport arrival, triggers once; an existing occupant, flying above it, or replayed movement is not another entry. The target makesDEXsave against the storedDC. On failure: snare givesStunned until the target’s next regular-turn end; charge deals2d6fire in that same event with no ongoing Burn; caltrop field uses the reviewed ordinary caltrop failure effect of1piercing, stopping remaining movement that turn and-10walkingSpeed until1HPhealing or an Action removes the caltrop. The caltrop slow is one shared same-area effect, not a new Slow condition, and moving at halfSpeed still avoids its save as under its actual item rule. Success avoids the trap’s feat effect. NEW snare and charge discharge after that first eligible trigger regardless of result; surviving actual metal/body can be recovered, but rearming requires a new prepared kit procedure and actual expendables. A caltrop field remains physically present and hazardous after an entry or successful save. Each actual new entry follows its stored feat DC and ordinary caltrop procedure, including half-Speed avoidance; an unchanged standing position is not another entry. Preserve all actual placed, embedded, removed and recovered pieces; no embedded piece exists simultaneously in the field or returns twice. Loss of actual coverage or stock can reduce the hazard only through the physical source record, not automatic first-trigger discharge. The field continues occupying the setter’s one enhanced-caltrop allowance until it is physically cleared. A charge consumes its filling; this does not duplicate its frame. Placement speed does not shorten preparation or refill after transfer.

The exposed snare/charge assembly isAC15/5HP; caltrops retain their actual ordinary physical pieces. An Action with safe reach disarms your own accessible trap. Another creature that has detected it can spend an Action with actual appropriate tools onDCequal to storedDC using INT/Engineering or DEX/thieves’-tools; failure triggers it only if that actual manipulation enters its working trigger, not arbitrarily against a remote observer. Hidden placement requires actual concealment: record one real setter DEX/Stealth check opposed by the actual search/passive-perception procedure, without granting invisibility. Once visible, ordinary physical removal/destruction still follows actual reach/safety and object rules. A snare/charge whose necessary mechanism is moved, Broken or disconnected becomes disarmed and needs real rearming; a cover prevents its trigger only while physically effective. Moving or covering some caltrops does not magically remove the remainder. NEW safe collection of an accessible unoccupied caltrop square requires one active minute with actual hands, tools/protection as necessary and a real receiver; retain the count and condition of the pieces actually collected. Unsafe manipulation follows the actual hazard. Reconstruction never duplicates stock or the type’s spent quick-placement use.

You have advantage on actual checks to spot hidden traps or tunnel evidence within30feet, not automatic sight through walls or knowledge that a tunnel exists. On a real trigger of any trap you personally placed, after its immediate effect resolves and if you are still capable of taking a Reaction and can perceive the triggering creature within30feet, you may spend that Reaction to move up to half your current applicable Speed. Pay ordinary terrain/mode costs from this distinct movement budget, respect speed0/restraints and actual paths. This movement provokes no opportunity attack from that triggering creature; other creatures’ normal opportunity attacks remain. You may use real cover or a real prepared kill-zone at the destination, but the feat creates neither. One trigger event permits at most one Reaction; copies, already discharged traps and additional targets of one blast are not new triggers.
The snare’s Stunned application uses the existing source/target/encounter hard-denial eligibility and immunity ledger; rearming or changing trap IDs does not reset it. If barred, no substitute damage or condition is awarded. The charge’s2d6fire is immediate damage, not a separate Burn condition. For assembly, resolve Core task degrees/natural shifts and collapse to success/failure; the basic-dismantling no-natural-shift exception does not apply. All other packet body, price and material quantities remain explicitly NEW authoring values, not previously catalogued source statistics.

### Final authored examples

A quick-placed snare is moved before arming and loses its actual trigger arrangement. The quick-placement use remains spent. Another enhanced snare cannot erase an older still-armed snare remotely; that older one must physically cease to be armed.

A caltrop field is entered twice by different creatures. Both qualifying entries resolve the persistent hazard; the first success or failure does not clear it. Actual embedded/removed pieces are tracked once. After a nearby charge trigger, the setter’s paid half-Speed Reaction movement avoids only that triggering creature’s opportunity attack and creates no cover.

### Preserved submitted procedure

Require Engineering proficiency or the proposed mechanical Disable Device/thieves’-tools credential. NEW three closed prepared-kit options use genuine physical parts and no invented recipe/craft XP: snare (5gp reference,2lb cord/spring/anchor), caltrop field (the actual ordinary20-caltrop source bag, preserving its price/weight), and spring-loaded charge (25gp reference,3lb trigger body plus actual prepared combustible filling). Availability and assembly are real: obtain a genuinely prepared kit from an actual provider, or spend30active minutes with suitable mechanical tools and the same actual parts, DC12 INT/Engineering or DEX/thieves’-tools, using Core binary task outcome. Failure consumes time and expendable cord/filling, retaining only real recoverable frame/metal parts; no free complete kit. The new reference prices are complete kit references, not added again to their component prices. No ordinary Rune or Tinkering formula is silently renamed one of these three options.

Place one held/accessible prepared kit in a real stable unoccupied5-foot ground square within5feet. Normally this feat procedure takes an Action; once per Short Rest for each of the three types, you may use a Bonus Action instead, spending that type’s separate quick-placement allowance. NEW one armed trap of each type per setter; arming a replacement disarms the old one without refund or teleportation. It arms at your next original regular-turn start, or after six elapsed seconds outside initiative, preserving the same deadline across mode changes. SnapshotDC8+PB+INT modifier at placement. The first actual grounded creature entering from outside, including an ally, forced movement or teleport arrival, triggers once; an existing occupant, flying above it, or replayed movement is not another entry. The target makesDEXsave against the storedDC. On failure: snare givesStunned until the target’s next regular-turn end; charge deals2d6fire in that same event with no ongoing Burn; caltrop field uses the reviewed ordinary caltrop failure effect of1piercing, stopping remaining movement that turn and-10walkingSpeed until1HPhealing or an Action removes the caltrop. The caltrop slow is one shared same-area effect, not a new Slow condition, and moving at halfSpeed still avoids its save as under its actual item rule. Success avoids the trap’s feat effect. NEW these fields discharge after that first eligible trigger regardless of result; surviving actual metal/body can be recovered, but rearming requires a new prepared kit procedure/consumed expendables. A charge consumes its filling; this does not duplicate its frame. Placement speed does not shorten preparation or refill after transfer.

The exposed snare/charge assembly isAC15/5HP; caltrops retain their actual ordinary physical pieces. An Action with safe reach disarms your own accessible trap. Another creature that has detected it can spend an Action with actual appropriate tools onDCequal to storedDC using INT/Engineering or DEX/thieves’-tools; failure triggers it only if that actual manipulation enters its working trigger, not arbitrarily against a remote observer. Hidden placement requires actual concealment: record one real setter DEX/Stealth check opposed by the actual search/passive-perception procedure, without granting invisibility. Once visible, ordinary physical removal/destruction still follows actual reach/safety and object rules. A trap that is moved,Broken,covered or disconnected becomes disarmed and needs real rearming; reconstruction never duplicates stock or the type’s spent quick-placement use.

You have advantage on actual checks to spot hidden traps or tunnel evidence within30feet, not automatic sight through walls or knowledge that a tunnel exists. On a real trigger of any trap you personally placed, after its immediate effect resolves and if you are still capable of taking a Reaction and can perceive the triggering creature within30feet, you may spend that Reaction to move up to half your current applicable Speed. Pay ordinary terrain/mode costs from this distinct movement budget, respect speed0/restraints and actual paths. This movement provokes no opportunity attack from that triggering creature; other creatures’ normal opportunity attacks remain. You may use real cover or a real prepared kill-zone at the destination, but the feat creates neither. One trigger event permits at most one Reaction; copies, already discharged traps and additional targets of one blast are not new triggers.

### Preserved submitted examples

You quick-place a snare, then transfer the kit before it arms. Moving it disarms it; a later placement does not refund your already spent snare quick-placement use. Caltrop and charge fast-placement uses remain independently available.

An enemy triggers your charge within30feet; after the save/damage you react and move up to half your current Speed behind an existing wall. That enemy cannot make an opportunity attack for this movement, but another eligible adjacent foe still can.
