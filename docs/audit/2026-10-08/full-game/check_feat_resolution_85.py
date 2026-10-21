"""Independent, source-bound resolution slices. No project module imports.

Legal event/ownership/geometry premises are explicit; this is neither the game
runtime nor a claim to have executed complete characters or all335 feats.
"""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
from datetime import datetime,timezone
import hashlib,json,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';I=R/'data/director/feat_candidates/exact_01'
ROOT=A/'feat335-resolution-cases-85';OUT=A/'FEAT335_RESOLUTION_CASES_85.json';CHECK=A/'FEAT335_RESOLUTION_CHECK_85.json';ZIP=A/'DD_Feat335_Resolution_Cases_85.zip';SAVED=A/Path(__file__).name
for p in [ROOT,OUT,CHECK,ZIP,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[];cases=[]
def ck(label,actual,expected=True):
 ok=actual==expected;checks.append({'check':label,'pass':ok,'actual':actual,'expected':expected})
 if not ok:raise AssertionError(label+': '+repr(actual)+' != '+repr(expected))
def case(cid,title,inputs,actual,expected,sources,qualification='Independent conditional specification calculation. Actual source ownership, acquisition, event legality, geometry, defenses and bodily predicates are supplied premises; no full campaign engine or complete actor ran.'):
 ck(cid+' '+title,actual,expected);cases.append({'id':cid,'title':title,'inputs':deepcopy(inputs),'computed':deepcopy(actual),'expected':deepcopy(expected),'sources':sources,'qualification':qualification})
def rejects(cid,title,inputs,fn,sources):
 try:fn();result=False
 except ValueError:result=True
 case(cid,title,inputs,{'rejected':result},{'rejected':True},sources)
paths=[I/'candidate.json',I/'shared_rules.json',R/'data/public/feat_candidates/exact_01/candidate.json',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/HEALING_DEATH_PLAYTEST.md',R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',R/'data/playtest/equipment_acquisition_candidate.json',R/'data/public/class_playtests/warrior.json',R/'data/public/class_playtests/mage.json',A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md',A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json',A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_COMPOSITIONS_84.json']
bindings=[info(p) for p in paths];records={x['id']:x for x in j(paths[0])['records']};public={x['id']:x for x in j(paths[2])['feats']};shared=j(paths[1]);warrior=j(paths[8]);mage=j(paths[9]);equipment={x['id']:x for x in j(paths[7])['items']}
ids=['anatomy_lore','precision_strike','giant_slayer','piercer','healer','quick_recovery','arcaneResonance','arcane_recall','elvenAccuracy','lucky','resilient_mind']
selected={k:records[k] for k in ids}
for k,r in selected.items():
 ck(k+' public/internal exact wording',r['operationalRules'],public[k]['operationalRules']);ck(k+' remains unpromoted',not r['selectionEnabled'] and not r['exactApproved'] and not r['runtimeApproved'])
ck('Real Warrior feat schedule',warrior['asiClassLevels'],[4,8,12,16,19]);ck('Actual Warrior20 has no RP',warrior['rpByClassLevel'][19],0);ck('Actual Mage12 RP capacity',mage['rpByClassLevel'][11],35)
spear=equipment['simple-melee-weapons.spear'];kit=equipment['adventuring-gear.healer-s-kit']
ck('Actual one-handed spear source',spear['sourceFields']['Damage'],'1d6 piercing');ck('Actual full healer kit charges',kit['chargesWhenFull'],10)
core=paths[3].read_text(encoding='utf-8');healing=paths[4].read_text(encoding='utf-8')
for text in ['Natural 1 and 20 have no generic special outcome','post-temp damage minus HP before the hit','Use pre-event Wounds','failure that began with three Wounds kills']:
 ck('Exact Core contract '+text,text in core)
for text in ['tempAbsorbed plus actualHpDamage','Reserve spends only actualHP restored','Broad HP prohibition makes legal healing and excess0']:
 ck('Exact healing contract '+text,text in healing)

def attack(face,modifier,ac,critical_low=20):
 if face not in range(1,21):raise ValueError('No actual d20 face')
 hit=face!=1 and (face==20 or face+modifier>=ac)
 return {'hit':hit,'critical':hit and face>=critical_low,'keptNatural':face,'total':face+modifier}
def task(face,modifier,dc):
 total=face+modifier;degree=3 if total>=dc+10 else 2 if total>=dc else 0 if total<=dc-10 else 1
 degree=max(0,min(3,degree+(1 if face==20 else -1 if face==1 else 0)))
 return {'total':total,'degree':['critical-failure','failure','success','critical-success'][degree],'binarySuccess':degree>=2}
for n,args,expected in [
 (1,(12,10,12,20),{'hit':True,'critical':False,'keptNatural':12,'total':22}),
 (2,(1,50,12,20),{'hit':False,'critical':False,'keptNatural':1,'total':51}),
 (3,(20,-20,25,20),{'hit':True,'critical':True,'keptNatural':20,'total':0}),
 (4,(19,0,20,19),{'hit':False,'critical':False,'keptNatural':19,'total':19}),
 (5,(19,1,20,19),{'hit':True,'critical':True,'keptNatural':19,'total':20})]:
 case('FR85-01-'+str(n),'Attack uses AC and actual natural face',dict(zip(['face','modifier','AC','criticalLow'],args)),attack(*args),expected,['Core attacks','FS-05'])
for n,args,expected in [(1,(20,0,40),{'total':20,'degree':'failure','binarySuccess':False}),(2,(1,30,20),{'total':31,'degree':'success','binarySuccess':True}),(3,(10,5,15),{'total':15,'degree':'success','binarySuccess':True})]:
 case('FR85-02-'+str(n),'Core task degree shifts do not promise an automatic outcome',dict(zip(['face','modifier','DC'],args)),task(*args),expected,['Core tasks','FS-05'])
case('FR85-03','Binary saves do not inherit task natural shifts',{'saves':[{'face':1,'modifier':20,'DC':20},{'face':20,'modifier':0,'DC':25}]},[1+20>=20,20>=25],[True,False],['Core saves','FS-05'])
case('FR85-04','Opposed equal totals preserve the old state',{'initiatorNatural':20,'initiatorModifier':0,'defenderNatural':10,'defenderModifier':10,'oldState':'target not grappled'},{'initiatorChangesState':20>10+10,'state':'target not grappled'},{'initiatorChangesState':False,'state':'target not grappled'},['Core opposed','FS-05'],qualification='Opposed tie comparison only, not a complete grapple Action or eligibility check; task natural shifts are not added as hidden numeric modifiers.')

def positions(dice,mode,replacement=None):
 vals=list(dice)
 if len(vals)!=(1 if mode=='normal' else 2) or any(x not in range(1,21) for x in vals):raise ValueError('Wrong original die procedure')
 if replacement is not None:idx,new=replacement;vals[idx]=new
 return {'positions':vals,'kept':max(vals) if mode=='advantage' else min(vals)}
case('FR85-05','Lucky under disadvantage replaces a position, not the whole disadvantage procedure',{'original':[18,3],'mode':'disadvantage','additionalFace':20,'replacePosition':0},positions([18,3],'disadvantage',(0,20)),{'positions':[20,3],'kept':3},['lucky','FS-05'])
case('FR85-06','Replacing the low position is a different lawful Lucky choice',{'original':[18,3],'mode':'disadvantage','additionalFace':20,'replacePosition':1},positions([18,3],'disadvantage',(1,20)),{'positions':[18,20],'kept':18},['lucky'])
ea=positions([20,4],'advantage',(0,2));lu=positions(ea['positions'],'advantage',(0,19))
case('FR85-07','Elven Accuracy replacement precedes Lucky; discarded20is not a kept natural20',{'actualElfReceipt':True,'actualEligibleDEXAttackWithAdvantage':True,'initial':[20,4],'ElvenChosenIndex':0,'ElvenNewFace':2,'LuckyNewFace':19,'LuckyReplaceIndex':0},{'afterElven':ea,'afterLucky':lu,'natural20Trigger':lu['kept']==20},{'afterElven':{'positions':[2,4],'kept':4},'afterLucky':{'positions':[19,4],'kept':19},'natural20Trigger':False},['elvenAccuracy','lucky','arcaneResonance'],qualification='Explicit source-qualified die-position slice; no Elf ancestry, paid feats, attack or additional Lucky point is granted. One actual Elven and one actual Lucky use are assumed authorized and consumed.')
case('FR85-08','A whole-save replacement keeps the original advantage and uses its worse replacement',{'legallyAuthorizedWholeSaveReroll':True,'original':[3,5],'replacement':[1,2],'sameModifier':2,'DC':12,'beforeConsequences':True},{'oldTotal':max([3,5])+2,'newTotal':max([1,2])+2,'newSuccess':max([1,2])+2>=12},{'oldTotal':7,'newTotal':4,'newSuccess':False},['FS-05'],qualification='The source contract for an already authorized whole-save replacement is tested; this case does not create a feat or a universal reroll entitlement. No prior outcome or cost is reversed.')

def percent(native,ratios):
 if any(x<0 for x in native):raise ValueError('Negative native packet')
 total=sum(native);result=list(native);increments=[]
 for ratio in ratios:
  amount=int(F(total)*ratio);shares=[F(amount*x,total) if total else F(0) for x in native];distributed=[int(x) for x in shares]
  order=sorted(range(len(native)),key=lambda i:(-(shares[i]-distributed[i]),i))
  for i in order[:amount-sum(distributed)]:distributed[i]+=1
  result=[a+b for a,b in zip(result,distributed)];increments.append({'amount':amount,'typed':distributed})
 return {'native':native,'increments':increments,'result':result}
case('FR85-09','Three actual percentage feats floor independently from native19',{'native':[19],'eligibleFeats':['anatomy_lore','precision_strike ordinary mode','giant_slayer']},percent([19],[F(1,2),F(1,2),F(1,5)]),{'native':[19],'increments':[{'amount':9,'typed':[9]},{'amount':9,'typed':[9]},{'amount':3,'typed':[3]}],'result':[40]},['FS-04','anatomy_lore','precision_strike','giant_slayer'])
case('FR85-10','Mixed native types preserve integer totals and component order',{'native':[7,4],'ratios':['1/2','1/2','1/5']},percent([7,4],[F(1,2),F(1,2),F(1,5)]),{'native':[7,4],'increments':[{'amount':5,'typed':[3,2]},{'amount':5,'typed':[3,2]},{'amount':2,'typed':[1,1]}],'result':[14,9]},['FS-04'],qualification='Typed distribution diagnostic, not a newly authored weapon/spell profile. Actual separate component eligibility is a premise and no multiplier is applied to external riders.')
case('FR85-11','Largest remainder ties retain original component order',{'native':[1,1],'ratio':'1/2'},percent([1,1],[F(1,2)]),{'native':[1,1],'increments':[{'amount':1,'typed':[1,0]}],'result':[2,1]},['FS-04'])
case('FR85-12','An external7point rider is outside each native percentage base',{'native':19,'externalRider':7},{'nativeAfterPercent':sum(percent([19],[F(1,2),F(1,2),F(1,5)])['result']),'includingSeparateRiderBeforeDefenses':sum(percent([19],[F(1,2),F(1,2),F(1,5)])['result'])+7},{'nativeAfterPercent':40,'includingSeparateRiderBeforeDefenses':47},['FS-04'])

def damage(before,amount,critical=False,maiming=False,wound_face=None,injury_face=None):
 s=deepcopy(before)
 if s['dead'] or min(amount,s['hp'],s['temp'],s['maximum'])<0 or s['hp']>s['maximum']:raise ValueError('Not a valid living damage state')
 pre_hp=s['hp'];pre_wounds=s['wounds'];absorbed=min(s['temp'],amount);s['temp']-=absorbed;post=amount-absorbed;lost=min(pre_hp,post);s['hp']-=lost
 out={'state':s,'resolved':amount,'tempAbsorbed':absorbed,'postTemp':post,'actualNormalHpLost':lost,'actualDamage':lost+absorbed,'overkill':max(0,post-pre_hp),'woundSave':None,'instantDeath':False}
 if post-pre_hp>=s['maximum']:
  s['dead']=True;s['stable']=False;s['stableDeadline']=None;out['instantDeath']=True;return out
 triggers=[]
 if pre_hp>0 and s['hp']==0:triggers.append('positive-to-zero')
 if 2*post>=s['maximum']:triggers.append('half-maximum')
 if maiming:triggers.append('actual-maiming')
 if triggers:
  if wound_face is None:raise ValueError('Actual Wound save face required')
  dc=max(10,post//2);total=wound_face+s['conSaveBeforeWoundPenalty']-pre_wounds;success=total>=dc
  out['woundSave']={'triggerKinds':triggers,'saveCount':1,'DC':dc,'natural':wound_face,'preEventWounds':pre_wounds,'total':total,'success':success}
  if not success:
   if pre_wounds==3:s['dead']=True;s['stable']=False;s['stableDeadline']=None;return out
   s['wounds']+=1
   if dc-total>=5:
    if injury_face not in range(1,7):raise ValueError('Actual Injury face required')
    s['injuries'].append({'woundNumber':s['wounds'],'d6':injury_face})
 if pre_hp==0 and post>0:
  s['stable']=False;s['stableDeadline']=None
  if s['usesDeathSaves']:
   s['deathFailures']+=2 if critical else 1
   if s['deathFailures']>=3:s['dead']=True
  else:s['dead']=True
 if pre_hp>0 and s['hp']==0:
  s['prone']=True;s['stable']=False;s['stableDeadline']=None
  if not s['usesDeathSaves']:s['dead']=True
 return out
base={'hp':10,'temp':5,'maximum':30,'wounds':1,'injuries':[],'conSaveBeforeWoundPenalty':6,'usesDeathSaves':True,'deathFailures':0,'deathSuccesses':0,'stable':False,'stableDeadline':None,'dead':False,'prone':False}
actor={'kind':'TEST_ONLY source-qualified acquisition slice, not a complete character','class':'Warrior','classLevel':20,'PB':6,'STR':18,'DEX':14,'INT':14,'SurvivalProficiency':'actual credential is an explicit premise','paidFeatOpportunities':{'4':'anatomy_lore','8':'precision_strike','12':'giant_slayer','16':'piercer'},'RPMaximum':0,'currentActualTurn':'warrior-regular-1','markMode':'damage','actualLargeTargetVisibleAndReachableWithin60ft':True,'weapon':spear['id'],'oneHanded':True,'targetHasPerceivablePhysicalWeakPoint':True}
ck('Distinct actual Warrior paid opportunities',len(actor['paidFeatOpportunities'])==4 and all(int(x) in warrior['asiClassLevels'] for x in actor['paidFeatOpportunities']))
attack_result=attack(20,6+4-2,18)
native=sum([6,5,4])+4 # original critical base dice [4,5], Piercer rerolls first to6; separate post-doubling critical die4.
percent_result=percent([native],[F(1,2),F(1,2),F(1,5)]);resolved=percent_result['result'][0]//2
hit=damage(base,resolved,critical=True,wound_face=4)
expected_state={**base,'hp':0,'temp':0,'wounds':2,'prone':True}
case('FR85-13','Full scoped spear hit: critical dice, Piercer, three independent bonuses, resistance, tempHP and one overlapping Wound save',{'attacker':actor,'targetBefore':base,'targetAC':18,'keptAttackD20':20,'ordinaryPrecisionPenalty':-2,'criticalBaseDice':[4,5],'PiercerReroll':{'index':0,'replacement':6},'PiercerExtraCriticalDie':4,'nativeSTRModifier':4,'actualPiercingResistance':True,'woundNatural':4},{'attack':attack_result,'nativeDamage':native,'percentageIncrements':[x['amount'] for x in percent_result['increments']],'damage':hit,'markConsumed':True,'PrecisionTurnUsed':True,'PiercerTurnUsed':True},{'attack':{'hit':True,'critical':True,'keptNatural':20,'total':28},'nativeDamage':19,'percentageIncrements':[9,9,3],'damage':{'state':expected_state,'resolved':20,'tempAbsorbed':5,'postTemp':15,'actualNormalHpLost':10,'actualDamage':15,'overkill':5,'woundSave':{'triggerKinds':['positive-to-zero','half-maximum'],'saveCount':1,'DC':10,'natural':4,'preEventWounds':1,'total':9,'success':False},'instantDeath':False},'markConsumed':True,'PrecisionTurnUsed':True,'PiercerTurnUsed':True},['actual Spear','actual Warrior schedule','anatomy_lore','precision_strike','giant_slayer','piercer','FS-04/05/07','Core damage order'],qualification='Complete bounded attack/damage slice. Warrior paid opportunities and printed prerequisites are source-consistent; remaining class/heritage choices, actual Survival credential, legal attack/mark geometry, Large target body, resistance and companion-free ownership are declared test premises. No complete character builder, world engine, class reaction, concentration effect or battlefield scheduler ran.')
instant=damage(base,45,critical=True)
case('FR85-14','Instant death stops Wound processing and never turns overkill into numeric actual damage',{'before':base,'resolved':45}, {'dead':instant['state']['dead'],'actualDamage':instant['actualDamage'],'overkill':instant['overkill'],'woundSave':instant['woundSave'],'instantDeath':instant['instantDeath']},{'dead':True,'actualDamage':15,'overkill':30,'woundSave':None,'instantDeath':True},['Core instant death','FS-07'])
fatal=damage({**base,'wounds':3},20,critical=True,wound_face=4)
case('FR85-15','A failed Wound save at three Wounds is fatal without a fourth Wound',{'before':{**base,'wounds':3},'resolved':20,'woundFace':4},{'dead':fatal['state']['dead'],'wounds':fatal['state']['wounds'],'deathFailures':fatal['state']['deathFailures'],'injuries':fatal['state']['injuries']},{'dead':True,'wounds':3,'deathFailures':0,'injuries':[]},['Core Wounds','FS-07'])
maim=damage({**base,'wounds':0,'conSaveBeforeWoundPenalty':3},0,maiming=True,wound_face=2,injury_face=2)
case('FR85-16','Actual Maiming can trigger its one save without numeric damage',{'before':{**base,'wounds':0,'conSaveBeforeWoundPenalty':3},'resolved':0,'actualMaiming':True,'woundFace':2,'injuryFace':2},{'hp':maim['state']['hp'],'temp':maim['state']['temp'],'actualDamage':maim['actualDamage'],'wounds':maim['state']['wounds'],'injuries':maim['state']['injuries'],'saveCount':maim['woundSave']['saveCount']},{'hp':10,'temp':5,'actualDamage':0,'wounds':1,'injuries':[{'woundNumber':1,'d6':2}],'saveCount':1},['Core Maiming and linked Injury','FS-07'])
stable={**base,'hp':0,'stable':True,'stableDeadline':7300,'prone':True}
absorb=damage(stable,3)
case('FR85-17','TempHP-only absorption preserves Stable and its real deadline',{'before':stable,'resolved':3},{'hp':absorb['state']['hp'],'temp':absorb['state']['temp'],'stable':absorb['state']['stable'],'deadline':absorb['state']['stableDeadline'],'failures':absorb['state']['deathFailures'],'actualDamage':absorb['actualDamage']},{'hp':0,'temp':2,'stable':True,'deadline':7300,'failures':0,'actualDamage':3},['Core already-zero damage','FS-07'])
zero=damage({**stable,'temp':0},1,critical=True)
case('FR85-18','An actual critical hit reaching a Stable0body ends Stable and adds two failures',{'before':{**stable,'temp':0},'resolved':1,'actualCritical':True},{'hp':zero['state']['hp'],'stable':zero['state']['stable'],'deadline':zero['state']['stableDeadline'],'failures':zero['state']['deathFailures'],'actualDamage':zero['actualDamage'],'dead':zero['state']['dead']},{'hp':0,'stable':False,'deadline':None,'failures':2,'actualDamage':0,'dead':False},['Core already-zero damage','FS-07'])

def healer_treatment(before,kit_charges,recipient_epoch,used,now,d4,wis,blocked=False,stabilize_only=False):
 s=deepcopy(before);ent=set(used)
 if s['dead'] or kit_charges<1:raise ValueError('Unavailable living target or actual kit charge')
 if not stabilize_only and recipient_epoch in ent:raise ValueError('Recipient healing entitlement spent')
 if stabilize_only and (s['hp']>0 or s['stable']):raise ValueError('No dying-to-Stable transition')
 kit_charges-=1
 if not stabilize_only:ent.add(recipient_epoch)
 transition=s['hp']==0 and not s['stable']
 if transition:s['stable']=True;s['deathFailures']=0;s['deathSuccesses']=0;s['stableDeadline']=now+d4*3600
 potential=0 if stabilize_only else max(0,2+3+wis)
 ceiling=max(1,s['maximum']-1) if s['wounds']==3 else s['maximum']
 gain=0 if blocked else min(potential,max(0,ceiling-s['hp']))
 s['hp']+=gain
 if s['hp']>0:s['stable']=False;s['stableDeadline']=None;s['deathFailures']=0;s['deathSuccesses']=0
 return {'state':s,'kitCharges':kit_charges,'recipientEntitlementsUsed':sorted(ent),'actualStabilizationTransition':transition,'ordinaryHealingPotential':potential,'actualHpRestored':gain}
patient=deepcopy(hit['state']);after_heal=healer_treatment(patient,9,'recipient-rest-7',[],100,2,2)
expected_healed={**patient,'hp':7}
case('FR85-19','A genuine next medic Action stabilizes and heals the same living target for one kit charge',{'patientBefore':patient,'medicClass':'Warrior4','paidFeatOpportunity':'Warrior4:healer','medicWIS':14,'actualKitCharges':9,'actualNextMedicActionBeforeRecipientRegularStart':True,'adjacentReachableLivingTarget':True,'recipientRestEpoch':'recipient-rest-7','eventElapsedSeconds':100,'stabilizationD4':2,'healing2d4':[2,3]},after_heal,{'state':expected_healed,'kitCharges':8,'recipientEntitlementsUsed':['recipient-rest-7'],'actualStabilizationTransition':True,'ordinaryHealingPotential':7,'actualHpRestored':7},['healer','actual Healer kit','Core stabilization','healing interface'],qualification='Bounded sequential continuation of FR85-13 with a separate source-qualified medic and an actual available Action before the patient\'s next regular start. No skipped death save, second Action for the attacker or free kit is inferred. Medic full acquisition/body/geometry are supplied premises. Prone and both Wounds remain.')
blocked_heal=healer_treatment(patient,9,'recipient-rest-7',[],100,2,2,True)
case('FR85-20','Blocked HP gain preserves genuine stabilization and consumes the same charge/entitlement',{'patientBefore':patient,'HPGainBlocked':True,'eventElapsedSeconds':100,'stabilizationD4':2},blocked_heal,{'state':{**patient,'stable':True,'stableDeadline':7300},'kitCharges':8,'recipientEntitlementsUsed':['recipient-rest-7'],'actualStabilizationTransition':True,'ordinaryHealingPotential':7,'actualHpRestored':0},['healer','Core stabilization','broad HP prohibition'])
rejects('FR85-21','A second practitioner cannot repeat recipient healing before the recipient rests',{'patient':blocked_heal['state'],'sharedEntitlement':['recipient-rest-7']},lambda:healer_treatment(blocked_heal['state'],10,'recipient-rest-7',['recipient-rest-7'],102,2,2),['healer'])
rejects('FR85-22','Known Dead target cannot be healed by spending a kit charge',{'patient':fatal['state']},lambda:healer_treatment(fatal['state'],9,'recipient-rest-7',[],100,2,2),['healer','Core Dead'])
critical_patient={**patient,'hp':28,'wounds':3}
critical_heal=healer_treatment(critical_patient,9,'recipient-rest-7',[],100,2,2)
case('FR85-23','Healer respects Critical ceiling without changing maximum or Wounds',{'before':critical_patient,'healing2d4':[2,3],'WISModifier':2},{'hp':critical_heal['state']['hp'],'maximum':critical_heal['state']['maximum'],'wounds':critical_heal['state']['wounds'],'actualGain':critical_heal['actualHpRestored'],'stabilization':critical_heal['actualStabilizationTransition'],'kitCharges':critical_heal['kitCharges']},{'hp':29,'maximum':30,'wounds':3,'actualGain':1,'stabilization':False,'kitCharges':8},['healer','Core Critical ceiling'])

def refund(before,kind,receipt,rank,request=0,trigger=True):
 s=deepcopy(before)
 if not trigger or s['uses'][kind]==0 or s['maximum']<=0:raise ValueError('No source-qualified recovery')
 p=s['payments'][receipt];available=p['paid']-p['refunded'];headroom=s['maximum']-s['current']
 if kind=='recall':cap=min(rank,5)
 elif kind=='resonance':
  if rank!=1:raise ValueError('No rank1 paid receipt')
  cap=2
 else:raise ValueError('Unknown source')
 amount=min(cap,available,headroom)
 if amount<=0:raise ValueError('Decline before committing: no funded recovery')
 s['current']+=amount;p['refunded']+=amount;s['uses'][kind]-=1
 return {'state':s,'recovered':amount}
rp={'class':'Mage','classLevel':12,'maximum':mage['rpByClassLevel'][11],'current':30,'Dissonance':1,'uses':{'recall':1,'resonance':1},'payments':{'rank1-cast-A':{'rank':1,'paid':2,'refunded':0,'restEpoch':'owner-rest-4','status':'completed-personal-cast'}}}
recall=refund(rp,'recall','rank1-cast-A',1);resonance=refund(recall['state'],'resonance','rank1-cast-A',1)
expected_rp=deepcopy(rp);expected_rp['current']=32;expected_rp['uses']={'recall':0,'resonance':0};expected_rp['payments']['rank1-cast-A']['refunded']=2
case('FR85-24','Arcane Recall and later Arcane Resonance share the same actual2RPexpense',{'before':rp,'actualMageFeatPayments':{'Mage4':'arcaneResonance','Mage12':'arcane_recall'},'priorPaidRank1Base':2,'RecallAtCastCompletion':True,'laterOwnKeptNatural20WeaponAttackAgainstActiveIndependentHostile':True,'laterAttackDamageMayBePrevented':True},{'RecallGain':recall['recovered'],'ResonanceGain':resonance['recovered'],'final':resonance['state']},{'RecallGain':1,'ResonanceGain':1,'final':expected_rp},['actual Mage12 pool and feat schedule','arcane_recall','arcaneResonance','FS-07'],qualification='The full original paid receipt is an explicit source-qualified premise; the earlier cast itself, spell identity/access/components/history and hostile weapon attack are not executed by this refund slice. This does not claim a new source or retroactive cast funding. No current RP maximum or Dissonance is changed by refund arithmetic.')
for label,change,kind,rank,trigger in [('free',{'paid':0,'refunded':0},'resonance',1,True),('already-refunded',{'paid':2,'refunded':2},'resonance',1,True),('wrong-rank',{'paid':5,'refunded':0},'resonance',3,True),('discarded20',{'paid':2,'refunded':0},'resonance',1,False)]:
 s=deepcopy(rp);s['payments']['rank1-cast-A'].update(change,rank=rank)
 rejects('FR85-25-'+label,'No RP recovery without an actual eligible unpaid balance and trigger',{'before':s,'kind':kind,'rank':rank,'qualifiedTrigger':trigger},lambda s=s,kind=kind,rank=rank,trigger=trigger:refund(s,kind,'rank1-cast-A',rank,trigger=trigger),['arcaneResonance','FS-07'])
s=deepcopy(rp);s['current']=35
rejects('FR85-26','Full pool does not spend a recovery use or raise capacity',{'before':s},lambda:refund(s,'recall','rank1-cast-A',1),['arcane_recall'])
case('FR85-27','Genuine Mage class capacity growth is not a refill',{'oldMageClassLevel':3,'newMageClassLevel':4,'oldCurrent':3},{'oldMaximum':mage['rpByClassLevel'][2],'newMaximum':mage['rpByClassLevel'][3],'newCurrent':min(3,mage['rpByClassLevel'][3])},{'oldMaximum':8,'newMaximum':10,'newCurrent':3},['actual Mage pool table','FS-06/07'])

for row in bindings:ck('Full source unchanged '+row['path'],info(G/row['path']),row)
report={'id':'FEAT335-RESOLUTION-85','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS_SOURCE_BOUND_SPECIFICATION_SLICES_NOT_PARENT_ACCEPTANCE','sourceBindings':bindings,'fullSelectedFeatRecords':selected,'fullSharedRules':[r for r in shared['rules'] if r['id'] in ['FS-03','FS-04','FS-05','FS-06','FS-07']],'fullActualEquipmentRecords':{'spear':spear,'healerKit':kit},'cases':cases,'caseCount':len(cases),'topLevelCaseCount':27,'scope':'Native roll families, selected reroll positions, three actual percentage feats, full bounded spear-damage/Wound/healer sequence, instant death/Maiming/Stable boundaries and shared actual RP refund expense. FXC-07 and full335 exact review remain open.','remainingScope':['Quick Recovery installment/blocked-first-event and actual Hit Die/rest ledgers.','Per-die healing, compatible reduction plans, finite actual reserves and source-specific no-resource gates through secondary descendants.','All remaining actual native feat numeric/source-resolution cases and complete authored660case semantic audit.','Full actor, body, acquisition and world/scheduler authentication belong to later implementation; these cases declare their operation-specific premises.'],'approvalBoundaries':{'newRuleAdoptions':0,'canonicalChange':False,'full335Approved':False,'runtimeTesting':False,'humanTesting':False,'balanceApproved':False,'wholeGameComplete':False},'actualExecution':'Only this newly authored standard-library diagnostic ran. No supplied project/downloaded Python imports or Unity/game runtime.','sourceInformationDeleted':0}
payload={'REPORT.json':enc(report),'check_feat_resolution_85.py':Path(__file__).read_bytes(),'README.md':b'# Feat resolution specification evidence\n\nIndependent conditional source-bound calculations, full original input files and full selected procedures. The linked attack/damage/healer slice is explicit about paid opportunities, legal event premises and preserved Wounds/Prone. Runtime, complete actors, full335review, human testing and balance are not claimed.\n'}
for p in paths:payload['sources/'+p.relative_to(G).as_posix()]=p.read_bytes()
payload['MANIFEST.json']=enc({n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payload.items())})
ROOT.mkdir()
for n,b in payload.items():
 p=Path('\\\\?\\'+str((ROOT/n).resolve()));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in sorted(payload.items()):z.writestr(n,b)
with zipfile.ZipFile(ZIP) as z:
 ck('Exact unique archive membership',set(z.namelist())==set(payload) and len(z.namelist())==len(payload));ck('Archive CRC',z.testzip() is None)
 for n,b in payload.items():ck('Archive roundtrip '+n,z.read(n)==b)
OUT.write_bytes(enc(report));SAVED.write_bytes(Path(__file__).read_bytes());CHECK.write_bytes(enc({'report':info(OUT),'archive':info(ZIP),'checkCount':len(checks),'failures':0,'checks':checks,'runtimeTestsExecuted':0,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'check':info(CHECK),'caseCount':len(cases),'checks':len(checks),'failures':0}))
