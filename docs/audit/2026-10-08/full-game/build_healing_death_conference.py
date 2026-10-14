from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
data=json.loads((HERE/'HEALING_DEATH_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
parts=['''# Healing, death replacement and resurrection source conference

This is the next bounded interface pass. The source candidate packet preserves74class cards,5class engines and6ordinary spell catalog objects. Its lexical matches include explicit exclusions/false positives. NONE of the six ordinary spells is operational yet: their original source metadata is evidence, not permission to treat a summary as playable. Please classify each supplied source as actual rule/application/modifier, exclusion/bookkeeping or dependency. Do not delete any original.

## Decisions needed against the exact sources

1. Separate living0HP recovery, numeric HP healing, HP-setting/state recovery, minimum-HP prevention, would-die replacement, actual resurrection and companion reconstruction. 'Revive' in a title or summary is not sufficient. Build a deterministic damage-event order with source-specific windows, not one generic 'Death Ward' rule. Existing CoreInstantDeath/Wound/zeroHP/death counters remain the starting contract. Explicit features can override only what they actually say. Simultaneous saves/reactions/alternatives need selection/priority and prevent repeated-cost refunds or multiple resurrection procs.

2. HP floor versus HP gain: Redundant Organs/Last King's Gift say remain at1 rather than dropping0; is that loss prevention even under Decay/noHPgain? What if already0? Phoenix Rebirth/Unyielding Light actually regain HP after damage, so prohibition applies and does not refund uses. Mercy Veil/Thousand Petals damage floor versus instant death, post-temp damage Wound threshold and fatal Wound save: do floors change effective actual damage for Wound/concentration/reflective or lifedrain amounts, or preserve full damage with finalHPfloor? State exact snapshots. Ward versus damage which would kill by massive damage, third deathfailure, failedWoundat3, Exhaustion6, expeditionStrain6 and explicit HP-bypassing instantkill requires separate answers.

3. Ritual of Undeath Death Ward says first WOULD DIE ->instead1HP (then dualhumanoid/undead untiltargetnextend), not first0HP. It has1minute and costs/usecaps; don't import ordinaryspellDeathWard'sdifferenttext. At0 underDecay, a would-die replacement might prevent death but cannotrestore1HP; propose Stable0 with cleared deathcounters and retained deferred recovery only if this is an explicitly NEW source-specific bridge. Or explain why it must fail. Resolve lethaltrack endpoints without an infinite unkillable6pointstate. Replacement cannot resurrect someone alreadydead, repaira destroyedvitalbody or reset allclassresources unless sourceexplicitlydoes. Trackconsumptiononce/woulddeath evenifhealingprevented; no automaticnewward.

4. Remaining conscious at0: Mage Undying Spellform and Oracle False Life BoonIII have differentAction/move/speakpermissions and endpoints. Deathsaveatregularstartstillhappens whileconscious/Stable? On a failedthird deathsave featurecannotkeepactingifdead. Healing above0endsfeature, but otherunconscious/proneeffectsremain. Mage endpenaltyonefaileddeathsave maykill; ifalreadyStable? Needdefine how applieswithoutillegalStable+counters. Oracle choice tocastRevelation still paysresource andcastingrisk; no extraplayerturns. Multiple0HPfeaturesfrommulticlass do notgrantmultipleActionwindows.

5. Resurrection generic eligibility: willing identity/soul, whether sourcebodycan sustainlife, timewindow, corpse ownership/location/LoE and ritualinterruption. Preserveactualshortclasswindows andcaps; do notinventallfeatures1minute. Wounds/Corruption/OracleCurse/debts/resourcespersistCore506unlessspecific. ThreeWoundsaliveisCriticalnotinstantdeath. How returnfromdeath whenExhaustion6 or expeditionStrain6remains? Need explicit candidatepolicy and recoverypath so no silentauto-cleansing or permanentunrecoverableloop. Disease/poison/environmentpersistentcause: resurrectionnotimmunity, immediatehazardevent vs continuous lethalstate specified. Do resurrection1HP/state-setting trigger ordinaryhealingamplifiers/reductions/HPgates? Decay blocksallHPgain; it separately sayscorpsecannotraisedinarea. Distinguishsuppressed ordinaryhealing fromdirectresurrectionblock. Couldlife returnStable0 withallHPgainblocked, or doeswholeeffectfail? Consistencywithbodyeligibility/sourceactualnewHPneeded.

6. Actual revival cards: ClericResurrection/CelestialResurgence/DivineRebirth, MonkThousandPetals, PaladinGraceReversal etc: preservecosts/caps/eligiblecorpsewindows. Monk 'cannotrevive samecreature twice' scopeperuse/perMonk/lifetime needs explicitdisposition. Death-window wordsendpreviousregularturn/last3turns needvirtualmarkeroutcombatbridge. DivineRebirth replace1HPwithhalfmax: calculateeffectivecurrentmax,round/minimum1,healceilingWounds andresource nonrestoration. Multiplecasters/copies/corpsefarming protections actualsource-specificnotunboundednew restrictions.

7. Healing arithmetic and eligibility gates: source rolled amount and permittedflatbonus, healingsource multipliers, Corruptedhalf, Paladinaurahalves/flat-S+M, CriticalWoundceiling/currentmax, actualHPgain, reserve spending andwhen-healedprocs. Decide duplicatevsindependentmultiplier/flatstacking, round-once versus eachstep, andpreventnegativehealing. HPgainforbidden vsordinaryHPhealing-only versuspassiveregen-only aredifferent. Clearlysay whether healingprovidedby anautomaticclassfeaturecountsregeneration vs paidpulse/lifedrain/restHD/state-recovery. Blessed/resurrection/tempHPnotassumedhealing. Bloodcures maytriggerfrompositivepotentialmagicalheal evenifactualgain0underclosedperiodicrule. MutationRecoveryReserve paysactualHPonly. Do notretroactivelyalterclosedmarktriggeractualdamage rules.

8. Prohibition/blockaura anatomy: DirgeofRuin says 'selectedlivingcreaturescannotbereturnedfromdeathwhileinsideaura' – trackselectedcreatureidentitythroughdeath/corpse, no targetfailsbecausedeadnotlivingliteral. Bodymovedout/selectionended returnbecomespossible, no retroactiveundo. OracleDecay corpseblockwithin2tiles, SoulBind/Denialnewspellscopes, linked/planar/extractionneedsfullsource. No genericnohealingeffectstopsTempHP/stabilizationunlessexplicit.

9. Six unfinished ordinary spells: author individually reviewable operationalcandidates fromattachedoriginals, with explicitNEWtarget/body/time/HP/ending/cost/state gaps. Keep Coreclasses/ranks/RP,casttime/range/componentsunlessexplicitjustifiedconflict. OrdinaryDeathWard(CoreAction60ftconcentration1minrank4/7RP)firstwoulddrop0->1 notclasswoulddie. StitchFate(Action120ftrank8/21RP)faileddeathsaveorreviveDYINGneedsactiontimingmeaning (notretroactivelyinterruptdeathwithanAction); distinguishrecoveringalive0vsresurrection. Resurrection(Action120ftrank7/17RP)andTrueResurrection(Action120ftrank9/26RPbodyless)needboundedoperationalchoiceswithout silentlyimportingothergames'1hour/diamonds/100years. MassResurrectionDenial sourceInstantaneous conflictsongoingblock; resolveexplicitduration/cure/counterplay,notpermanentblanketbasedgenericmetadata. SoulBindrank9dyingtargetrequiresactualeligibility/save/afterdeathrecord/willingPCagency/cureendpoint,notunconsentedNPCretirementthroughunboundedspell. Dissonance/Refrain/Counterspell/concentrationcommonrulesapply. Draftsremaininactiveuntilreviewandvalidation.

10. Follow-up cure audit fromcontrolreview: 'activeeffecteligibility' differsfrom 'presentrecordremovable'. Suppressedrecordswithrunningclocks maystillbecured; SanctifyGroundStaggered explicitallpresent. Existingperiodichelperusesactive_recordforMedicine/fire/healingcureselectionwhich excludes suppressed/immune. Determineexactcure semanticsagainstproperrecordpresence, especiallypreexistingcoveredBleedwhileimmune, ratherthanreapplyingoldstatewhenimmunityends. Don'tchangefamilydamagearbitrationorinventspecialcurebypass. EachsuppressedBloodCurserecordmayretainexistinglegalcuresave? Actualsourcepermissionrequired.

Please identify source conflicts and NEW decisions clearly, give operational rules plus adversarial examples, and state whatremainsopen afterthisboundedpass. Discuss actualsources, notgenericadvice.

## Closed Core interface for preservation
''']
parts.extend(['\n```markdown\n',(ROOT/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md').read_text(encoding='utf-8'),'\n```\n'])
parts.append('\n## Exact current class procedures\n\n```json\n')
brief=[]
for r in data['classRecords']:
 if r['kind']=='class-card':
  brief.append({'kind':r['kind'],'owner':r['owner'],**{k:r['card'].get(k) for k in ('id','name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')},'sourceObjectSha256':r['sourceObjectSha256']})
 else:brief.append(r)
parts.append(json.dumps(brief,ensure_ascii=False,indent=2));parts.append('\n```\n')
parts.append('\n## Exact unfinished ordinary spell records (not operational)\n\n```json\n')
parts.append(json.dumps(data['spellCatalogRecords'],ensure_ascii=False,indent=2));parts.append('\n```\n')
custom=json.loads((ROOT/'data/playtest/custom_condition_bindings.json').read_text(encoding='utf-8'))
parts.append('\n## Previously reviewed Decay and Doomed profiles\n\n```json\n')
parts.append(json.dumps([x for x in custom['definitions'] if x['mechanicalId'] in ('oracle.decay','oracle.doomed')],ensure_ascii=False,indent=2));parts.append('\n```\n')
parts.append('''\n## Existing track bridge that is NOT a resurrection decision

ExpeditionStrain0–6: everypositiveunpreventedgainthatwouldreach/exceed6resolvesdeathunlessTHATsourceexplicitnonlethalexceptioncollapse. Repeatedgainat6lethalotherwise; preventedgainnone. CollapsealiveUnconsciousSpeed0noact/travel,doesnotitselfsetHP0/createStable/deathsave. Independentdying0remainsdying. Only24hHavencare/explicittreatmentcanreducecollapsed6; qualifyingremovablegateMetpointsremoved;specialgatedpointsremain. Loweringbelow6endsowncollapseonly,notdeadstate. Serum0–3differentnamespace. Exhaustion6death,differenttrack;noautomaticresurrectionfromlevelremoval. Resurrectionat6wasdeliberatelyleftOPEN. Wounddeathat3isfailedsubsequentWoundsave,notstatic3Wounddeath. Fullsourceevidencepreservedinpreviousconferences.
''')
parts[0]=(HERE/'HEALING_DEATH_QUESTIONS.md').read_text(encoding='utf-8')
(HERE/'CODEX_HEALING_DEATH_CONFERENCE.md').write_text(''.join(parts),encoding='utf-8')
print(f'Prepared healing/death conference (not yet submitted): {sum(map(len,parts))} characters')
