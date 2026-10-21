"""One-shot full defense casebook evidence; bounded reference work, not runtime."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
import json, hashlib, math, zipfile
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'
I=R/'data/director/feat_candidates/exact_01'; D=A/'feat335-ft84-derived-review-92/after/DescentReviewChanges/ReviewBible'
PREP=A/'FEAT335_DEFENSE_CASEBOOK_SEMANTIC_PREPARATION_96.json'
ROOT=A/'feat335-defense-casebook-97'; OUT=A/'FEAT335_DEFENSE_ORIGINAL_CASEBOOK_REVIEW_97.json'; ZIP=A/'DD_Feat335_Defense_Casebook_Review_97.zip'; SAVED=A/Path(__file__).name
for p in (ROOT,OUT,ZIP,SAVED): assert not p.exists(),str(p)
def j(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes(); return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,ok): checks.append({'check':n,'pass':bool(ok)}); assert ok,n
ck('Exact preserved semantic preparation96',info(PREP)['sha256']=='c619605b328f2df50116731bcf9039c8bda191d80753cd6bf41988abb00adb32')
prep=j(PREP)
for row in prep['sourceBindings']:ck('Preparation source unchanged '+row['path'],info(G/row['path'])==row)
candidate=j(I/'candidate.json'); selected=[r for r in candidate['records'] if r['cohort']=='general_defense']; records={r['id']:r for r in selected}
examples=j(I/'example_dispositions.json'); fa=j(I/'additional_boundary_expectations.json'); cases=[x for x in examples['cases'] if x['featId'] in records]; boundaries=[x for x in fa['cases'] if x['featId'] in records]
ck('31 full records62 originals4 boundaries',len(selected)==31 and len(cases)==62 and len(boundaries)==4)
ck('All full prepared records equal actual candidate',selected==prep['completeSelectedRecords'])
notes={x['id']:x for x in prep['originalCaseSemanticNotes']}; boundary_notes={x['completeOriginalDisposition']['id']:x for x in prep['additionalBoundarySemanticNotes']}
ck('Exact semantic-note coverage',set(notes)=={x['id'] for x in cases} and set(boundary_notes)=={x['id'] for x in boundaries})
proposal=j(R/'data/director/general_defense_feat_operating_proposal_internal.json')
reviews=[]; boundary_reviews=[]
for x in cases:
 idx=int(x['sourcePointer'].rsplit('/',1)[1]); value=proposal
 for part in x['sourcePointer'].split('/')[1:]: value=value[int(part)] if isinstance(value,list) else value[part]
 ck(x['id']+' full original source and expected case',value==x['original'] and x['completeExpectedOutcome']==records[x['featId']]['workedCases'][idx])
 ck(x['id']+' full preserved semantic disposition',notes[x['id']]['completeOriginalDisposition']==x and bool(notes[x['id']]['semanticNote']))
 reviews.append({'id':x['id'],'featId':x['featId'],'completeOriginalDisposition':deepcopy(x),'reviewResult':'CONSISTENT_WITH_EXACT_CURRENT_AUTHORING_AND_STATED_CONDITIONS','reasoning':notes[x['id']]['semanticNote'],'qualification':'Complete stated-case semantic review against current candidate and full linked sources. Acquisition, world credentials, real actor/equipment/events and existing feature ownership remain conditional premises. This does not execute the game.','runtimeExecuted':False,'canonicalApplied':False})
for x in boundaries:
 ck(x['id']+' exact full boundary preserved',boundary_notes[x['id']]['completeOriginalDisposition']==x)
 boundary_reviews.append({'id':x['id'],'featId':x['featId'],'completeOriginalDisposition':deepcopy(x),'reviewResult':'CONSISTENT_WITH_EXACT_CURRENT_AUTHORING_AND_STATED_CONDITIONS','reasoning':boundary_notes[x['id']]['semanticNote'],'runtimeExecuted':False,'canonicalApplied':False})
public={r['id']:r for r in j(R/'data/public/feat_candidates/exact_01/candidate.json')['feats']}
derived={r['id']:r for r in j(D/'data/director/feat_candidates/exact_01/candidate.json')['records']}
derived_public={r['id']:r for r in j(D/'data/public/feat_candidates/exact_01/candidate.json')['feats']}
chapter=(R/'docs/feats/exact-candidate-01/GENERAL_DEFENSE.md').read_text(encoding='utf-8-sig')
for r in selected:
 ck(r['id']+' unchanged complete derived record',r==derived[r['id']])
 ck(r['id']+' exact public and derived-public procedures/cases',all(r[k]==p[r['id']][k] for p in [public,derived_public] for k in ['operationalRules','workedCases']))
 ck(r['id']+' full chapter procedure/cases',r['operationalRules'] in chapter and all(s in chapter for s in r['workedCases']))
calcs=[]
def C(n,refs,inputs,actual,expected,scope):
 cid='GD97-N'+str(n).zfill(2);ck(cid+' expected result',actual==expected)
 calcs.append({'id':cid,'originalCaseIds':refs,'inputs':inputs,'calculatedResult':actual,'expectedResult':expected,'scope':scope,'runtimeExecuted':False})
def ability_mod(score):return (score-10)//2
def half_score(score):return score+max(0,min(1,20-score))
C(1,['GD-01-E01'],{'singleSTR':18,'splitSTR':19,'splitWIS':13,'oneActualOpportunity':True},{'singleSTR':18+2,'split':[19+1,13+1],'pointsEach':[2,1+1]},{'singleSTR':20,'split':[20,14],'pointsEach':[2,2]},'Full legal pure-ASI allocations; opportunity cannot also buy another feat.')
C(2,['GD-14-E01','GD-14-E02','GD-17-E01'],{'scores':[15,20,22]},[half_score(v) for v in [15,20,22]],[16,20,22],'Half-feat increases preserve scores above20; do not use this partial allocation for the pure ASI option.')
C(3,['GD-03-E01','GD-03-E02'],{'runningBaselineFeet':16,'STRModifiers':[3,-1],'realApproachFeet':10},{'spans':[16+max(0,s) for s in [3,-1]],'totalMovementCosts':[10+16+max(0,s) for s in [3,-1]]},{'spans':[19,16],'totalMovementCosts':[29,26]},'Legal running jump and enough real movement assumed; terrain, gravity and clearance still control.')
C(4,['GD-03-E02'],{'climbFeet':10,'athleteRemovesClimbingSurcharge':True,'difficultTerrainCostPerFoot':2},10*2,20,'Ordinary climbing surcharge removed; the independent terrain cost remains.')
C(5,['GD-04-E01','GD-04-E02'],{'baseArmorSeconds':[60,61],'featFactor':'1/2','oneIndependentHelperFactor':'1/2','ordinaryIntervalSeconds':6},{'featOnly60':math.ceil(60/2),'withHelperSeconds':[math.ceil(Fraction(n,4)) for n in [60,61]],'intervalsFor15Seconds':math.ceil(15/6),'shieldActions':1},{'featOnly60':30,'withHelperSeconds':[15,16],'intervalsFor15Seconds':3,'shieldActions':1},'61-second fixture illustrates single final rounding only. Actual source suit/work and legal complete Actions/intervals are required; no extra-helper stacking or free shield use.')
C(6,['GD-05-E01'],{'criticalMeleeWeaponRolledDice':[3,4],'nativeFlat':3,'berserkerFlat':2,'rangedOrdinaryDamage':7},{'criticalTotal':sum([3,4])+3+2,'rangedTotal':7},{'criticalTotal':12,'rangedTotal':7},'Two actual critical dice are supplied; the flat feat2 is added once before defenses.')
C(7,['GD-05-E02'],{'bludgeoningComponent':11,'applicableResistanceSources':2},11//2,5,'Same-scope resistance is one half regardless of duplicate sources; Stunned ends the rage via actual Incapacitated.')
C(8,['GD-07-E01','GD-07-E02'],{'hitDieFaces':[1,1],'signedCON':[3,-1]},[max(face+con,2*con,0) for face,con in [(1,3),(1,-1)]],[6,0],'Raw ordinary Hit Die healing before real modifiers, prohibition and capacity; no Hit Dice created.')
C(9,['GD-08-E01'],{'actualUnarmedNativeBase':{'type':'bludgeoning','amount':3},'chosenElement':'lightning','separateFireRider':2},{'nativeBase':{'type':'lightning','amount':3},'separateFireRider':2,'totalBeforeDefenses':3+2},{'nativeBase':{'type':'lightning','amount':3},'separateFireRider':2,'totalBeforeDefenses':5},'Type substitution on admitted unarmed base, not a new damage die or blanket conversion of riders; source qualification remains required.')
def penalty(pending,operative=True):return (1-pending,pending) if operative else (0,1)
# Explicit conditional event stream from FA01; it generates no clocks or permissions.
state={'foodWaterPending':0,'sleepPending':0,'strainAdded':0,'restDebt':False,'dueHour':None,'beneficialLRRewardsAlreadySpent':1};trace=[]
for event,hour in [('missRest',24),('foodWaterOnly',24),('debtDue',40),('missRest',48),('foodWaterOnly',48),('safeRestComplete',56)]:
 before=deepcopy(state);added=0
 if event=='missRest':
  if state['restDebt']:state['sleepPending'],added=penalty(state['sleepPending'])
  state['restDebt']=True;state['dueHour']=hour+16
 elif event=='debtDue':
  assert state['restDebt'] and state['dueHour']==hour
  state['sleepPending'],added=penalty(state['sleepPending'])
 elif event=='foodWaterOnly':state['foodWaterPending'],added=penalty(state['foodWaterPending'])
 else:state['restDebt']=False;state['sleepPending']=0;state['dueHour']=None
 state['strainAdded']+=added;trace.append({'event':event,'hour':hour,'before':before,'strainAddedNow':added,'after':deepcopy(state)})
C(10,['GD-09-E01','GD-09-E02','FA-01'],{'worldStartHour':0,'scheduledRestWatches':[[16,24],[40,48]],'actualSafeRest':[48,56],'orderedEvents':[(t['event'],t['hour']) for t in trace]},{'addedPerEvent':[t['strainAddedNow'] for t in trace],'resetDeadlineAfterSecondMiss':trace[3]['after']['dueHour'],'final':state},{'addedPerEvent':[0,0,0,1,1,0],'resetDeadlineAfterSecondMiss':64,'final':{'foodWaterPending':0,'sleepPending':0,'strainAdded':2,'restDebt':False,'dueHour':None,'beneficialLRRewardsAlreadySpent':1}},'Original canonical due event evaluated once at40; missing the next scheduled Rest at48 produces the second sleep event and resets debt deadline64. No hourly replay or extra rest refill.')
C(11,['FA-02'],{'foodWaterPenaltyWouldBeOmitted':True,'independentMandatoryOilShortage':True,'dailyOriginalPenalty':1},max(0,1),1,'One independently unsupported day, not one point for each missing supply.')
C(12,['GD-09-E01','GD-09-E02'],{'pendingBeforeSuppression':1,'operativeAtActualCheckpoint':False},list(penalty(1,False)),[0,1],'At the real suppressed checkpoint clear only that cause credit and apply original one penalty; do not replay older prevented penalties.')
C(13,['GD-11-E01'],{'size':'Medium','STR':18,'poundCarryCoefficient':15,'ordinaryLoadCoefficient':1,'featCapacityFactor':2},{'ordinaryCarryLb':18*15,'newCarryLb':18*15*2,'ordinaryLoad':18,'newLoad':18*2,'newPushDragLiftLb':18*15*2*2},{'ordinaryCarryLb':270,'newCarryLb':540,'ordinaryLoad':18,'newLoad':36,'newPushDragLiftLb':1080},'Actual admitted body capacity; weight/custody remain unchanged and larger weapons keep their own profiles.')
C(14,['GD-12-E01'],{'fireComponent':9,'radiantComponent':5},{'fireAfterResistance':9//2,'radiantUnchanged':5,'packetTotal':9//2+5},{'fireAfterResistance':4,'radiantUnchanged':5,'packetTotal':9},'Hardy heat-to-fire selection retained; component rounding does not halve unrelated radiant damage.')
def healer(blocked):
 charges=10;charges-=1;raw=3+2+3;hp=0 if blocked else min(20,raw)
 return {'charges':charges,'rawHealing':raw,'HP':hp,'lifeState':'Stable' if hp==0 else 'livingPositive','recipientEntitlementSpent':True,'stableDeadlineRetained':hp==0}
C(15,['GD-13-E01','GD-13-E02'],{'dyingHP':0,'maximumHP':20,'actualKitCharges':10,'faces':[3,2],'WIS':3,'genuineStabilizationFirst':True},{'ordinary':healer(False),'broadHPGainBlock':healer(True)},{'ordinary':{'charges':9,'rawHealing':8,'HP':8,'lifeState':'livingPositive','recipientEntitlementSpent':True,'stableDeadlineRetained':False},'broadHPGainBlock':{'charges':9,'rawHealing':8,'HP':0,'lifeState':'Stable','recipientEntitlementSpent':True,'stableDeadlineRetained':True}},'Bounded already-legal Healer event: one charge/recipient entitlement covers stabilization and healing; deadline die and actual expiry remain original Core state, not newly generated by this projection.')
C(16,['GD-14-E01','GD-20-E01','GD-22-E01'],{'permanentScoreBefore':15,'permanentScoreAfter':16},[ability_mod(15),ability_mod(16)],[2,3],'Derived modifier recomputation, no separate feat opportunity or resource refill.')
C(17,['GD-22-E01'],{'storedBaseHPByLevel':[8,5,5],'CONBefore':15,'CONAfter':16,'currentHPBefore':20},{'baseMaxBefore':sum(max(1,v+ability_mod(15)) for v in [8,5,5]),'baseMaxAfter':sum(max(1,v+ability_mod(16)) for v in [8,5,5]),'currentHPAfter':20},{'baseMaxBefore':24,'baseMaxAfter':27,'currentHPAfter':20},'Conditional separate CON selection; true attained-level bases and per-level floor retained before HP ledger, capacity increase does not heal.')
C(18,['GD-15-E01'],{'elapsedYears':2,'ordinaryAgingFactor':'1/2','existingBiologicalAge':40},{'elapsedYears':2,'newBiologicalYears':int(2*Fraction(1,2)),'newBiologicalAge':40+int(2*Fraction(1,2))},{'elapsedYears':2,'newBiologicalYears':1,'newBiologicalAge':41},'Prospective natural aging only; no age reversal or automatic change to discrete magical aging.')
C(19,['GD-15-E02'],{'deathSaveAdvantageFaces':[1,12],'alreadyDead':False},{'selected':max(1,12),'successesAdded':int(max(1,12)>=10),'failuresAdded':0},{'selected':12,'successesAdded':1,'failuresAdded':0},'Select actual advantage result before death-save natural result rules; Instant Death produces no roll.')
C(20,['GD-16-E01','GD-23-E02'],{'actualWISCharmedSave':True,'IronWill':2,'ResilientMind':1,'sameEffectAlsoPsychic':True},2+1,3,'Distinct eligible feat bonuses once each; source mental predicate, not two Iron Will bonuses for two mental qualities.')
C(21,['GD-18-E01'],{'suitBaseAC':14,'DEXScores':[16,14,8]},[14+min(ability_mod(s),3 if s>=16 else 2) for s in [16,14,8]],[17,16,13],'Actual medium suit formula with feature-specific cap; negative modifiers remain negative. Shield/other sources separate.')
C(22,['GD-19-E01'],{'DC':15,'modifier':2,'initialAdvantageFaces':[3,7],'replacementAdvantageFaces':[2,6],'initialUses':1},{'originalTotal':max(3,7)+2,'replacementTotal':max(2,6)+2,'replacementPass':max(2,6)+2>=15,'usesAfter':1-1},{'originalTotal':9,'replacementTotal':8,'replacementPass':False,'usesAfter':0},'Paid precommit whole-save replacement keeps its new failure; no self-reroll or immunity.')
C(23,['GD-20-E01'],{'DEXAfterFeat':16,'ordinaryMediumBaseAC':14,'hasMediumArmorMaster':False},14+min(ability_mod(16),2),16,'Moderately Armored does not acquire a different feat or raise the ordinary medium cap.')
def quick(blockFirst):
 used=False;heals=[]
 for native,blocked in [(5,blockFirst),(6,False),(4,False)]:
  raw=native+(3 if not used else 0);used=True;heals.append({'raw':raw,'HPGainBeforeCaps':0 if blocked else raw})
 return heals
C(24,['GD-21-E01','GD-21-E02'],{'PB':3,'nativeHitDieHealingEvents':[5,6,4],'firstTwoSum':11},{'normalEvents':quick(False),'blockedFirstEvents':quick(True),'normalFirstTwoTotal':sum(x['raw'] for x in quick(False)[:2]),'noHitDiceBonus':0},{'normalEvents':[{'raw':8,'HPGainBeforeCaps':8},{'raw':6,'HPGainBeforeCaps':6},{'raw':4,'HPGainBeforeCaps':4}],'blockedFirstEvents':[{'raw':8,'HPGainBeforeCaps':0},{'raw':6,'HPGainBeforeCaps':6},{'raw':4,'HPGainBeforeCaps':4}],'normalFirstTwoTotal':14,'noHitDiceBonus':0},'Already-legal completed SR and actual HD spending; first blocked addition remains spent. No runtime rest scheduling or healing-cap execution.')
C(25,['GD-22-E02'],{'WIS':16,'PB':3,'twoProficiencySources':True},{'proficiencyContribution':max(3,3),'saveModifier':ability_mod(16)+max(3,3)},{'proficiencyContribution':3,'saveModifier':6},'Duplicate save proficiency does not become Expertise or2PB.')
C(26,['GD-16-E02','GD-23-E01'],{'ordinaryCONConcentrationModifier':4,'ResilientMindConcentration':2,'causalPsychicDamage':True},{'modifier':4+2,'IronWillBonus':0,'WISOnlyBonus':0},{'modifier':6,'IronWillBonus':0,'WISOnlyBonus':0},'Concentration purpose is independent of incoming damage type; Incapacitated can end concentration without any roll.')
C(27,['GD-24-E01'],{'preexistingWounds':3,'postTempDamage':10,'ordinaryCONModifier':4,'originalFace':7,'alternativeReplacementFaces':[10,5]},{'DC':max(10,10//2),'effectiveModifier':4-3,'originalTotal':7+4-3,'replacementTotals':[d+4-3 for d in [10,5]],'replacementSurvival':[d+4-3>=max(10,10//2) for d in [10,5]]},{'DC':10,'effectiveModifier':1,'originalTotal':8,'replacementTotals':[11,6],'replacementSurvival':[True,False]},'Two distinct conditional reroll branches at an actually failed Wound save begun at3; failure commits death. No reroll of its own replacement or no-save Instant Death.')
C(28,['GD-25-E01','GD-25-E02'],{'currentLevels':[7,8],'maxWithTenacity7':40,'currentHP':35},{'bonuses':[7,8],'maximumAfterRemoval':40-7,'currentAfterRemoval':min(35,40-7),'clampedAmount':35-min(35,40-7),'damageFromClamp':0},{'bonuses':[7,8],'maximumAfterRemoval':33,'currentAfterRemoval':33,'clampedAmount':2,'damageFromClamp':0},'Current-level capacity record; removal clamps without damage/Wounds/healing/first-fall triggers.')
C(29,['GD-26-E01','GD-26-E02'],{'ToughAcquisitionLevel':4,'laterLevel':10,'baseMaximum':30,'currentHP':25},{'bonus':2*4,'suppressedMaximum':30,'restoredMaximum':30+2*4,'restoredCurrentHP':25},{'bonus':8,'suppressedMaximum':30,'restoredMaximum':38,'restoredCurrentHP':25},'Original acquisition snapshot is retained through suppression and restoration; no automatic +20 or heal at level10.')
def nails_event_replay():
 amount=2*5;seen=set()
 for event in ['actual-level6','actual-level6']:
  if event not in seen:amount+=2;seen.add(event)
 return {'bonus':amount,'eventsRecorded':len(seen)}
C(30,['GD-27-E01','GD-27-E02'],{'acquisitionLevel':5,'level6EventDeliveries':2},nails_event_replay(),{'bonus':12,'eventsRecorded':1},'One actual advancement identity credited once; this bounded idempotency projection grants no leveling or retraining permission.')
C(31,['GD-25-E01','GD-26-E01','GD-27-E01','GD-30-E01'],{'currentLevel':6,'ToughAcquisitionLevel':4,'ToughAsNailsAcquisitionLevel':5,'baseMaximum':30,'currentHP':20},{'distinctFeatBonusTotal':6+8+12+12,'effectiveMaximum':30+6+8+12+12,'currentHP':20},{'distinctFeatBonusTotal':38,'effectiveMaximum':68,'currentHP':20},'Conditional four distinct legally acquired HP feats, no systemic reductions in fixture; duplicate identities are never added.')
C(32,['GD-29-E01'],{'actualNonmagicalSilverWeaponOwnSlashingDamage':11,'sameFeatPassiveMatches':2},11//2,5,'Cursebound one passive family prevents double halving; external riders need independent provenance.')
def floor_wound(post_temp,hp,maximum,con,face,wounds):
 instant=post_temp-hp>=maximum
 if instant:return {'HP':0,'dead':True,'floorUseSpent':False,'wounds':wounds}
 floor_applied=hp>0 and post_temp>=hp
 after_hp=1 if floor_applied else max(0,hp-post_temp)
 significant=2*post_temp>=maximum
 failed=significant and face+con-wounds<max(10,post_temp//2)
 dead=failed and wounds==3
 return {'HP':0 if dead else after_hp,'dead':dead,'floorUseSpent':floor_applied,'wounds':wounds if dead or not failed else wounds+1}
C(33,['GD-29-E02'],{'transformed':True,'HP':10,'maximum':30,'CONModifier':3,'existingWounds':3,'woundFace':5,'postTempAmounts':[20,40]},[floor_wound(v,10,30,3,5,3) for v in [20,40]],[{'HP':0,'dead':True,'floorUseSpent':True,'wounds':3},{'HP':0,'dead':True,'floorUseSpent':False,'wounds':3}],'20damage is independently significant even after floor; its failed preexisting3-Wound save kills.40damage reaches Instant Death before floor. Not a general damage engine.')
C(34,['GD-29-E02'],{'ordinaryFormEnd':10,'nextOriginalRegularTurnEnd':15,'alternativeLaterEnd':30},{'shortFormExtendedTo':max(10,15),'longFormStillEnds':max(30,15)},{'shortFormExtendedTo':15,'longFormStillEnds':30},'Only ordinary elapsed endpoint extension; failed concentration, upkeep, invalid body or suppression still ends as sourced.')
C(35,['GD-30-E01'],{'effectiveMaximum':21,'HPs':[10,11]},[2*hp<21 for hp in [10,11]],[True,False],'Strict integer threshold, no rounded-half boundary.')
C(36,['GD-30-E01'],{'initialHP':11,'effectiveMaximum':21,'incomingPoison':4,'defenseEvaluatedBeforeLoss':True},{'resistanceAtDefense':2*11<21,'postHP':11-4,'resistanceAfterLossForFutureEvent':2*(11-4)<21},{'resistanceAtDefense':False,'postHP':7,'resistanceAfterLossForFutureEvent':True},'Only this poison component with no tempHP/other defense in fixture; later threshold crossing cannot retroactively halve it.')
C(37,['GD-30-E02'],{'necroticAfterPassives':5,'fireAfterPassives':4,'paidReactionAvailable':True},{'necroticAfterPaidStep':5//2,'fireUnchanged':4,'combinedBeforeTempHP':5//2+4},{'necroticAfterPaidStep':2,'fireUnchanged':4,'combinedBeforeTempHP':6},'One actual paid Reaction/use before tempHP, not another passive resistance or free temporaryHP.')
C(38,['GD-30-E02'],{'originalNecrotic':11,'actualSeparatePassiveNecroticResistance':True,'paidDarkFortitudeReaction':True},{'afterPassive':11//2,'afterPaidStep':(11//2)//2},{'afterPassive':5,'afterPaidStep':2},'Two separately authorized stages with their own flooring; legal ability to react is an independent premise.')
def delayed_recovery(earlier_heal=0,dead=False,blocked=False,same_episode=True):
 hp=earlier_heal;attempt=not dead and hp==0 and same_episode
 gain=1 if attempt and not blocked else 0;hp+=gain
 return {'HP':hp,'directRecoveryAttempted':attempt,'riderStarted':gain>0,'spentUseRestored':False,'dead':dead}
C(39,['GD-31-E01','GD-31-E02','FA-25'],{'priorDropSurvived':True,'useCommitted':True,'nextOriginalRegularStartReached':True,'branches':['healed5','dead','living0','blockedLiving0','differentEpisode']},[delayed_recovery(earlier_heal=5),delayed_recovery(dead=True),delayed_recovery(),delayed_recovery(blocked=True),delayed_recovery(same_episode=False)],[{'HP':5,'directRecoveryAttempted':False,'riderStarted':False,'spentUseRestored':False,'dead':False},{'HP':0,'directRecoveryAttempted':False,'riderStarted':False,'spentUseRestored':False,'dead':True},{'HP':1,'directRecoveryAttempted':True,'riderStarted':True,'spentUseRestored':False,'dead':False},{'HP':0,'directRecoveryAttempted':True,'riderStarted':False,'spentUseRestored':False,'dead':False},{'HP':0,'directRecoveryAttempted':False,'riderStarted':False,'spentUseRestored':False,'dead':False}],'Already-registered same real episode only, direct recovery before death save; no Action/Reaction or recovery of a corpse. Existing Wounds/Prone/independent Unconscious remain outside this HP projection.')
C(40,['GD-31-E02'],{'successfulRecoverySecond':100,'riderSeconds':60,'evaluationSeconds':[159,160]},[t<100+60 for t in [159,160]],[True,False],'Absolute elapsed one-minute endpoint, no extra-turn/Action reset.')
C(41,['GD-31-E02'],{'actualPersonalSharedAreaEvent':True,'nativeFireRoll':8,'flatNecroticRider':2,'targets':['A no defense','B necrotic resistance']},{'sharedPreDefenseComponents':[8,2],'targetTotals':[8+2,8+2//2]},{'sharedPreDefenseComponents':[8,2],'targetTotals':[10,9]},'Rider once per actual shared event/roll, each target defenses independently; no per-component multiplication or Lifeleech reclassification.')
C(42,['GD-31-E02'],{'actualPersonalCriticalMeleeDice':[3,4],'nativeFlat':3,'recoveryFlatNecrotic':2},sum([3,4])+3+2,12,'Native critical dice already rolled; recovery flat2 stays once and retains feat provenance.')
linked={ref for c in calcs for ref in c['originalCaseIds']};ck('All calculation references resolve actual reviewed cases',linked<={x['id'] for x in cases+boundaries})
mental=proposal['sharedProposal']['mentalPredicate']
ck('Full original finite mental predicate retained',all(t in mental for t in ['Charmed','Frightened','possession','psychic damage','concentration']))
ck('Actual source decision adopts finite mental predicate', 'Adopt finite mental-effect predicate' in records['iron_will']['sourceDirection']['decision'])
paths=[G/row['path'] for row in prep['sourceBindings']]+[PREP,R/'data/public/feat_candidates/exact_01/candidate.json',D/'data/director/feat_candidates/exact_01/candidate.json',D/'data/public/feat_candidates/exact_01/candidate.json',R/'docs/feats/exact-candidate-01/source-audit/GENERAL_DEFENSE.md',R/'docs/mechanics/MAXIMUM_HP_PLAYTEST.md',R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',R/'docs/mechanics/CONDITIONS_PLAYTEST.md',A/'FEAT335_RESOLUTION_CASES_85.json']
paths=list(dict.fromkeys(paths));source_bytes={p.relative_to(G).as_posix():p.read_bytes() for p in paths}
report={'id':'FEAT335-DEFENSE-ORIGINAL-CASEBOOK-REVIEW-97','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'31_FULL_PROCEDURES62_ORIGINAL_POSITIONS4_BOUNDARIES_REVIEWED_WITH42_BOUNDED_CALCULATIONS_PARENT_PENDING','scope':'Full general_defense authored semantic review of all62 original positions and FA01/02/25/27 using the exact complete source-backed candidate. Original mental-predicate dependency is carried explicitly; no new mechanics or canonical integration.','sourceBindings':[info(p) for p in paths],'completeSelectedRecords':selected,'originalCaseReviews':reviews,'additionalBoundaryReviews':boundary_reviews,'numericAndStateCalculations':calcs,'completeIllustrativeEnduranceEventTrace':trace,'fullRetainedSourceMentalPredicate':{'source':info(R/'data/director/general_defense_feat_operating_proposal_internal.json'),'pointer':'/sharedProposal/mentalPredicate','completeText':mental,'currentDecision':records['iron_will']['sourceDirection']['decision'],'qualification':'Source-linked current wording resolves the two stated case pairs. Exact shared-rule/public presentation references only the shared proposed predicate; explicit self-contained carriage remains a parent assembly/presentation dependency, not newly authored permission.'},'coverage':{'cohort':'general_defense','fullFeatProcedures':31,'originalCasePositions':62,'additionalBoundaries':4,'boundedCalculations':len(calcs),'originalCasesWithNumericalProjection':sum(x['id'] in linked for x in cases),'additionalCasesWithNumericalProjection':sum(x['id'] in linked for x in boundaries)},'reviewFindings':['No contradictory complete expected outcome identified among62 original cases and4 FA boundaries under their explicit premises and linked sources. Real acquisition/exposure/lineage/body/world evidence remains conditional.','Endurance uses actual canonical daily and debt events: t24food omitted, t40sleep omitted, distinct t48food/sleep each add1, real safe rest48to56clears debt but adds no extra rest resources. The missed-Rest48 reset would be due64 if unpaid.','Tough retains acquisition snapshot; Tenacity/Dark Fortitude track current level; Tough as Nails preserves idempotent later advancement. Distinct HP identities add capacity without healing, and clamps cause no damage.','Mental Fortress replaces the whole advantaged save and keeps failure. Iron Will/Resilient Mind use the exact adopted finite predicate retained at original proposal sharedProposal/mentalPredicate, not all WIS/CON rolls or psychic-caused concentration. Keep that full definition in later parent/public assembly.','Healer stabilization precedes ordinary healing; recipient entitlement and one charge remain spent even under broad HP-gain block. Quick Recovery commits PB with its first actual HD event, so a blocked event cannot reserve a retry.','Cursebound floor follows Instant Death and cannot prevent later fatal Wounds; Undying registers only after a survived positive-to-zero event and recovers only in that same living-zero episode. Positive healing or death cancels it.','Defense31 full records are unchanged in isolatedFT84-derived92; private/public exact procedures and worked cases plus the authored chapter agree. No lineage, class, curse or plane was invented.'],'remainingScope':['Parent335 remains pending:432 other original positions and18 additional boundaries remain after this cohort is registered; finite supplements, acquisition/world evidence, mirrors, native-copy chains and all existing holds remain separate.','The source-resolved mental-effect definition must remain explicitly available in final assembled shared/public rules; this casebook is not whole public-package acceptance.','Reference arithmetic/event projections do not execute the runtime, scheduler, life-state system, exposure authentication, spell/class interactions or actual campaign.','No human gameplay, numerical balance, cosmology, whole-game or release approval.'],'checks':checks,'passed':len(checks),'failed':0,'newMechanicsAuthored':0,'canonicalApplied':False,'parent335Accepted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproved':False,'cosmologyDecisions':0,'actuallySentToGpt':False}
payload=enc(report);script=Path(__file__).read_bytes();ROOT.mkdir()
for rel,b in source_bytes.items():
 dst=ROOT/'sources'/rel;dst.parent.mkdir(parents=True,exist_ok=True);put(dst,b)
for p,b in [(SAVED,script),(ROOT/Path(__file__).name,script),(OUT,payload),(ROOT/'REVIEW.json',payload)]:put(p,b)
put(ROOT/'README.txt',b'Full defense casebook97:31 complete procedures,62 original cases,4 FA boundaries,42 bounded calculations. Full source history/individual rationales retained. Unapplied; no runtime or parent335 acceptance. Source-resolved mental-predicate carriage remains an explicit final-assembly dependency. No supplied program needs execution.\n')
files=sorted(p for p in ROOT.rglob('*') if p.is_file());manifest={'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}
put(ROOT/'MANIFEST.json',enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(p for p in ROOT.rglob('*') if p.is_file()):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 assert all(len(z.read(x['path']))==x['bytes'] and sha(z.read(x['path']))==x['sha256'] for x in manifest['files'])
assert all((G/rel).read_bytes()==b for rel,b in source_bytes.items())
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'coverage':report['coverage'],'checks':len(checks),'failed':0,'fullSourceFiles':len(paths),'archiveMembers':len(manifest['files'])+1},indent=2))
