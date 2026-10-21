# Exact sources — Arcane Feedback follow-through

## wizard#/cards/60

```json
{
  "id": "wizard.supplement.arcane-feedback",
  "name": "Arcane Feedback",
  "className": "Wizard",
  "band": "Hero",
  "path": null,
  "sourceKind": "supplement",
  "minimumClassLevel": 15,
  "acquisition": "automatic",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Instantaneous",
  "frequency": "At most once per round",
  "effect": "Source progression line 5191, converted from historical slot wording to RP. After your Counterspell successfully negates a spell, restore 1 RP, never above your normal maximum. A counter produced by a companion, reflected spell or copied Counterspell does not trigger this feature.",
  "prerequisite": "See class engine and progression.",
  "source": {
    "line": 5191,
    "reference": null,
    "originalText": "| 15 | Arcane Feedback (after successfully countering a spell, recover 1 RP once per round) |",
    "status": "source-derived"
  },
  "designStatus": "provisional-playtest",
  "spellRank": null
}
```

## wizard#/cards/17

```json
{
  "id": "wizard.base.counterspell",
  "name": "Counterspell",
  "className": "Wizard",
  "band": "Base",
  "path": null,
  "sourceKind": "active",
  "minimumClassLevel": 2,
  "acquisition": "automatic",
  "activation": "Reaction",
  "cost": "3 RP",
  "rangeAndTarget": "One creature you perceive casting a spell within 60 feet",
  "duration": "Instantaneous",
  "frequency": "Automatic at Wizard 2; recharge 2 rounds",
  "effect": "Counterspell. Tags: arch-source, automatic, wizard-spell, abjuration, disruption. Trigger when a creature begins casting a spell. Make an Intelligence check adding proficiency against DC 10 + twice the spell's rank, treating rank 0 as 0. Success negates the triggering spell after its costs are paid; failure lets it resolve. This is gained automatically at Wizard 2 and is never also selected from the Arch pool.",
  "source": {
    "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
    "line": 5222,
    "originalText": "Counterspell: Disrupt an enemy's spellcasting, potentially negating their spell entirely."
  },
  "designStatus": "provisional-playtest",
  "spellRank": 1
}
```

## wizard#/cards/29

```json
{
  "id": "wizard.hero.spellbinder.counterpulse",
  "name": "Counterpulse",
  "className": "Wizard",
  "band": "Hero",
  "path": "Spellbinder",
  "sourceKind": "active",
  "minimumClassLevel": 12,
  "acquisition": "selection",
  "activation": "Triggered",
  "cost": "1 RP",
  "rangeAndTarget": "Caster whose spell you successfully Counterspelled",
  "duration": "Until end of target's next turn",
  "frequency": "At most once per round",
  "effect": "Counterpulse. Tags: hero, spellbinder, counter, control. Immediately after your Counterspell succeeds, spend 1 RP. The countered caster is Silenced until the end of its next turn. This is part of the successful counter event rather than another spell cast and cannot trigger another Counterpulse.",
  "source": {
    "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
    "line": 5251,
    "originalText": "Counterpulse: Countering a spell silences the caster for 1 round"
  },
  "designStatus": "provisional-playtest",
  "spellRank": null
}
```

## combat, lines 29–37

29: Establish terrain, light, hazards, objectives, exits and cargo; determine awareness; roll `d20 + DEX modifier + legal bonuses`. Highest first. Players choose player/player ties; the Director resolves ties involving NPCs. Keep the resulting ordered slots for the encounter. A round represents approximately six seconds. A **regular turn** is a creature's normal initiative slot even if it cannot act. An extra turn is distinct.
30: 
31: A turn normally permits movement, one Action, a Bonus Action when an actual rule grants a use, and one ordinary free object interaction. A second ordinary interaction or an Action-time object activation uses an Action. Brief communication is not an extra Action. Conditions and specific features may restrict these permissions.
32: 
33: The shared limit is one **extra full Action per creature per numbered round**. Such an Action cannot grant another extra Action, Bonus Action or Reaction. This cap is independent of Reaction timing. Extra turns do not by themselves refresh Reactions, recharge, periodic ticks, recovery ticks or the regular-turn allowances defined here.
34: 
35: **Reaction interpretation.** Begin an encounter with one available Reaction unless surprised or otherwise prohibited. Refresh at each regular own-turn start; never at the numbered round boundary or an extra turn. A late-initiative creature can therefore react before its first turn, refresh, and react again in the same numbered round. A legal trigger, available resource and all feature prerequisites are still required.
36: 
37: **Explicit additional Reactions.** A reviewed card can grant a separate limited use without refreshing the ordinary resource. Warrior Mind Shock supplies its stated once-per-duration non-attack Reaction; spending one resource does not consume/reset the other. Surprise, Incapacitated and Focused still restrict both. It grants no Counterspell knowledge or waived costs. Extra turns refresh neither. Per-dose reapplication/stacking and other specific grants remain part of the class semantic pass.

## classRules, lines 11–19

11: An ability is known only if granted or selected by the draft schedule. Satisfy all printed prerequisites, target legality, action availability, recharge and resource costs before spending anything. A failed legal attack/save attempt still pays; an illegal activation spends nothing. No resource goes below 0 or above its cap. A class feature name shared with a spell does not grant both versions; use the version selected, with its own cost and timing. Names and source text are preserved; the current card is the operational draft.
12: 
13: ## Action and timing limits
14: 
15: One regular Action, one Bonus Action if a feature permits it, normal movement and one Reaction between starts of your turns. A free trigger costs no Action only if expressly stated. All grants share **one extra full Action per creature per round**. An extra Action cannot grant another Action, recharge itself, or start another extra-Action grant. It supplies no extra Bonus Action or Reaction. A card granting additional attacks is not permission to repeat all class riders on every hit: obey each rider's frequency.
16: 
17: Recharge N sets a counter to N after use; reduce once at the start of the owner's regular initiative turn, whether able to act or not. Extra turns/Actions do not tick it. Outside combat tick once per 6 elapsed seconds, without double counting. Recharge 2 used on turn 1 is ready on turn 3. A positive counter can be reset/shortened at most once per ability per round. Zero counters are not legal reset targets and expend no reset use. Resets never restore RP or per-rest uses or grant an immediate activation.
18: 
19: An encounter is a genuine scene of uncertain opposition chosen by the Director, not a player declaration used to reset resources. No encounter gain from attacking allies, one's summons, harmless animals, helpless captives or reused corpses. Out-of-combat abilities retain all printed costs and time. Short-rest means a completed uninterrupted hour of permitted recovery; long-rest means a completed 8-hour Rest Watch. This time convention is a draft integration. Expedition pressure, supplies, safe locations and rest debt still matter. A long rest also refreshes short-rest uses; a short rest never refreshes long-rest uses. Weekly uses refresh after seven full in-world days, not repeated rests.

## Historical verifier, lines 129–143 — inspected, not run

```python
 ck('case','4 disclosed conditional branches',sum(c['disposition']=='CONDITIONAL_EXTERNAL_PREMISE' for c in allcases)==4)
 for c in allcases:
  ck('case',c['id']+' complete final',bool(c['timeline']) and c['timeline'][-1]['after']==c['finalState'])
  for j,e in enumerate(c['timeline']):
   b,a=e['before'],e['after'];ck('state',c['id']+f'/{j} time',b['time']==a['time']==e['time'])
   ck('state',c['id']+f'/{j} complete actor bounds',all(0<=x['rp']<=x['maxRP'] and 0<x['hp']<=x['maxHP'] and 0<=x['D'] and x['movementSpent']<=30 for x in a['actors'].values()))
   for cid,r in a['castRecords'].items():
    if cid not in b['castRecords']:
     owner=r['owner'];before=b['actors'][owner];after=a['actors'][owner]
     # Any new genuine commitment has spent exactly its real declared Action/Reaction/BA; callbacks never create a fresh budget.
     ck('action',c['id']+f'/{j}/{cid} one actual budget',sum(bool(before[k]) and not bool(after[k]) for k in ['action','bonusAvailable','reaction'])==1)
     ck('cost',c['id']+f'/{j}/{cid} bounded price',r['quote']['total']==sum(r['quote'][k] for k in ['base','extra','dampening','burden','protectedPrincipal']))
     feedback=1 if r['name']=='wizard.base.counterspell' and r['state']=='resolved' and any(x.get('ArcaneFeedback')==1 or x.get('actualArcaneFeedback')==1 for x in a['observations'][len(b['observations']):]) else 0
     ck('cost',c['id']+f'/{j}/{cid} actual RP transition',before['rp']-after['rp']==r['quote']['total']-feedback)
     ck('action',c['id']+f'/{j}/{cid} declared real budget',before[r['actualBudgetSpent']] is True and after[r['actualBudgetSpent']] is False)
```

This calculation verifies a numeric observation; it neither locates a spent round receipt nor establishes an original-source replay gate.
