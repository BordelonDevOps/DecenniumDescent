from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
data=json.loads((HERE/'MAXIMUM_HP_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
lines=['''# Maximum HP, thresholds and composition — exact source conference

Codex → Calibration Review. Please reply below18,000 characters. Preserve every source. Classify ALL supplied51 class passages plus7 feat records by exact source ID, separating actual maximum-HP modifiers, thresholds, percentage healing/damage, guards and exclusions. Lexical matches are not semantic completeness. No ordinary spell source object matched this wording; this is not proof of no hidden maxHP behavior in unfinished spells/items/monsters. This is a bounded composition proposal, not promotion of all feats.

Existing closed bridge: multiply rational systemic maximumHP factors against the same otherwise-applicable maximum, floor ONCE, minimum1. Expedition4+ contributes3/4; Exhaustion4+ contributes1/2; base100 gives37. CurrentHP clamps down to effective maximum without damage/Wounds/resource/death-failure triggers. Removal raises capacity without healing or resetting counters. Critical's max(1,effectiveMaximum−1) is HEALING ceiling, not another maxHP multiplier. At lethal track6, actual life transitions remain handled by the already reviewed lethal-track module; numerical recomputation alone must not re-kill a collapsed survivor.

We need explicit source-backed or labeled NEW decisions:

1. Complete stage equation: base character/creature maximum + compatible permanent bonuses + active temporary bonuses − reductions, then systemic factors once? Or do temporary flat drains apply AFTER multipliers? Choose and justify with examplesbase101,FleshWarden+20,Monk−9,Exhaustion×1/2,Expedition×3/4. Track modifiers separately to avoid repeated multiplication and recast/suppression drift. Does flatstrongest rule apply across distinct permanent FEATS or only class technique bonuses?
2. Monkengine9 'largest reduction from your Monk features': previous131discussion treated perowner. Do reductions from different Monkowners stack, or does firstsentence 'do not stack on samecreature' require globalstrongest? Source is internallyambiguous. We need explicit resolution, not silently change earlierperownerdecision. Different sourceIDs sameowner max only; suppressedlargest revealsnexteligible while clocksstilltick. Repeatedsamecard applications fromsameowner? strongestamount/longestremainingendpoint or separateeffects withseparateexpiry? Unless earlierend, anycompletedshortorlongrest ofTARGETclearsallMonktrauma, regardlessrestrewardcaps? Ifrestinterruptednone. Parent DeathlessSilence target-end passive suppression mustnotshorten separatemaximumHPreduction.
3. FleshWardenequipped+2WarriorL capacityonly, noheal. SummoncreationwithWizardConjuration+L orFleshAscendant+2L initialHPdoesitstartatfinalboostedmaximum? Latergainingcontrol/equippingbonus onlycapacitywithoutheal. Conjuration+FleshAscendantsameundead summon: compatibleadditive vsstrongestclassflat? FleshAscendant engine24 explicitly 'afterlistedbase' but no explicitstack. Changingcontroller vsfixedcaster schoolbonus trackownerandeligibility. Do not inventcompanioncap/newheal oncontroller swaps.
4. Feats: Tenacity+1percharacterlevel grows; Tough exacttext says+twicelevelWHENgained but nofuturelevel clause; ToughasNailsexplicitgrows+2perlaterlevel. KeepTough acquisition-levelsnapshot vsinferfuturegrowth? Source-specific and preserve source; don't useanothergame'smemory. DarkFortitude+2percharacterlevel dynamic. Same-name duplicates no stack; distinctfeatbenefits stack or strongest? Constitutionbasegrowth/advancementprocedures stillseparate. FamiliarBond 'gains hitpoints equaltolevel' maximumvsimmediatehealingambiguous; proposedcapacitybonus, initialcreationfullboostedHP; latercapacitygainnoheal. Its attackcommandlifecycle remainsopen.
5. CurrentHPclampnotdamage norHPpayment; doesDecaypreventcapacityrestoration? Expectedno. AddingmaxHPwithoutHPgain changespercentthresholds; dynamicpassivesrecomputebut event 'firstfallbelow/atquarter' mustnottriggermerelymaximumchanges. Distinguish actualdamage/loss/healing transitions. Becomingabovehalfsolelymaximumdecrease doesn'tsatisfy 'untilHEALEDabovehalf'. MythicCarapace/Butcherformendswhenbelowquarter: continuousendconditionvsdamagecrossing? Theirdurationwordingneedsindividualdisposition.
6. Fractioncomparison: avoidroundedthresholderrors useexactcrossmultiply (at/belowquarter 4HP<=max, strictlybelowhalf2HP<max). Percentagehealing floorformula atresolutioneffectiveMaxunlesssourceexplicitprevalue; preserve min1onlywheresourcegrantsit. WoundEaterIII no min1 atsmallmax; DivineRebirthhalf nofreeinventedfloor unlessexistingrevivalbridgeapplies. Thresholdsnapshotatselection/beforeattack vsafterevent percard. RewindWound stored HP snapshot maximum atthatdamageevent, no retroactivequalify aftermaxchange. Brutalityprogress threshold state alreadyreviewed snapshot rules; don'treopenunchangedcode.
7. Stat update on dead/stable/0HP creatures leaves life/death counters untouched; minimummax1neverresurrects. ReducingmaxbelowcurrentTempHPdoesnotclampTempHP (independentbuffer), unlesssourceexplicit. Removingdebuff nothealing so doesn't trigger ordinarycure/HPgainprocs. HealingceilingCritical recomputesaftermaximumchanges.
8. Source-order with damaging attack that ALSO lowersmaxHP: resolve attack damage+Wounds/InstantDeath againstpretrauma maximum, thenapply successfuldrainclamp tosurvivingtarget? Existinghit-rider ordering sourceexactneeddecide. MaxHPincreasewithin sameevent mustnotrewrite alreadyfrozen actualDamage metrics. Offer adversarial examplesbeforecoding.

Return a bounded sharedprocedure, all58individualclassifications and openevidencedependencies. No whole-game completion.
''']
for r in data['classRecords']:
    if r['kind']=='class-card':
        c=r['card'];lines += ['## '+c['id'],json.dumps({k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')},ensure_ascii=False)]
    else:lines += [f"## {r['owner']}.engine[{r['engineIndex']}]",r['text']]
for r in data['featRecords']:lines += ['## feat:'+r['sourceId'],json.dumps(r['sourceObject'],ensure_ascii=False)]
for path in ('tools/strain_playtest_rules.py','docs/mechanics/STRAIN_PLAYTEST.md'):
    text=(ROOT/path).read_text(encoding='utf-8')
    if path.endswith('.py'):text=text[text.index('def combined_maximum_hp'):text.index('def track_penalties')]
    else:text='\n'.join(line for line in text.splitlines() if 'maximum' in line.lower())
    lines += ['## Already reviewed '+path,text]
(HERE/'CODEX_MAXIMUM_HP_CONFERENCE.md').write_text('\n\n'.join(lines),encoding='utf-8')
print('Prepared maximumHP58-source conference, not submitted.')
