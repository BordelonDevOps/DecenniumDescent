"""Own bounded healing-composition specifications. No imported project/returned modules."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
from math import ceil
import hashlib,json,zipfile

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
OUT=A/'FEAT335_HEALING_COMPOSITIONS_89.json';ZIP=A/'DD_Feat335_Healing_Compositions_89.zip';SAVED=A/Path(__file__).name
for p in [OUT,ZIP,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def check(label,v):
 checks.append({'check':label,'pass':bool(v)})
 if not v:raise AssertionError(label)
def equal(label,a,b):
 if a!=b:raise AssertionError((label,a,b))
 checks.append({'check':label,'pass':True})
source_paths=[R/'data/director/feat_candidates/exact_01/candidate.json',R/'data/director/feat_candidates/exact_01/shared_rules.json',R/'data/public/feat_candidates/exact_01/candidate.json',R/'data/public/class_playtests/warrior.json',R/'data/public/class_playtests/oracle.json',R/'data/public/class_playtests/shaman.json',R/'docs/mechanics/HEALING_DEATH_PLAYTEST.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/GAMEPLAY_LOOP_CANON.md',R/'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md',R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md',A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md',A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_SEMANTIC_REVIEW_88.json']
before={p:info(p) for p in source_paths};candidate=j(source_paths[0]);shared=j(source_paths[1]);warrior=j(source_paths[3])
selected=[candidate['records'][i] for i in [8,62,68,76,94,155,307]]
equal('Seven exact selected feat identities',[r['id'] for r in selected],['field_surgeon','durable','healer','quick_recovery','herbalist','life_drinker','bioStabilizer'])
for rec in selected:check(rec['id']+' still disabled/unapproved',rec['selectionEnabled'] is False and rec['exactApproved'] is False and rec['runtimeApproved'] is False)
check('Warrior genuine4/8 paid feat opportunities',all(next(x for x in warrior['schedule'] if x['classLevel']==lv)['asiOrFeat'] for lv in [4,8]))
equal('Warrior actual Bloodthick source',warrior['cards'][73]['id'],'warrior.supplement.bloodthick-node')
equal('Warrior real second mutation source',warrior['cards'][72]['id'],'warrior.supplement.ironhide-graft')
check('Actual finite reserve formula','3 L+M' in warrior['engine'][24])
text=(R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md').read_text(encoding='utf-8')
check('Core explicitly rejects per-die Wound penalty','It does not reduce each healing die' in text)
check('Actual long-rest recovery is half expended','Recover half expended Hit Dice, rounded up' in (R/'docs/mechanics/GAMEPLAY_LOOP_CANON.md').read_text(encoding='utf-8'))
equal('Warrior8 CON16 foundation maximum',12+7*7+8*3,85)

actors={
 'HD-W8':{'scope':'Paid feat/HP/Hit Die slice, not a complete authenticated campaign character','class':'Warrior','level':8,'CONBeforeDurable':15,'CON':16,'CONModifier':3,'PB':3,'fixedHPBases':[12,7,7,7,7,7,7,7],'maxHP':85,'HitDice':'8d12','paidFeats':{'4':'durable','8':'quick_recovery'},'otherASIIncrease':False,'actualCompletedRestIsExternalPrerequisite':True},
 'DURABLE-NEG':{'scope':'Independent signed-CON boundary; Quick Recovery not granted','class':'Wizard','level':4,'CONBeforeDurable':8,'CON':9,'CONModifier':-1,'paidFeats':{'4':'durable'},'dieSize':6},
 'MEDIC-W8':{'scope':'Paid feat and actual kit/action slice; physical/legal source prerequisites explicitly supplied','class':'Wizard','level':8,'WIS':16,'PB':3,'paidFeats':{'4':'healer','8':'field_surgeon'},'kits':{'kit-A':{'charges':10,'weightLb':3,'fullPriceGp':5}},'noFreeAction':True},
 'LIFE-W8':{'scope':'Actual prerequisite/paid-feat slice; no full attack engine execution','class':'Warrior','level':8,'CON':16,'INT':13,'PB':3,'maxHP':85,'paidFeats':{'4':'hemocraft, permanent INT choice','8':'life_drinker'},'actualHemocraftAcquisition':'INT13 prerequisite and paid4 opportunity; retained source-qualified receipt, no free prerequisite grant','reserveMaximum':16},
 'BIO-W8':{'scope':'Source-qualified equipped/active loadout slice; no full serum/acquisition dispatcher executed','class':'Warrior','level':8,'STR':16,'CON':16,'M':3,'PB':3,'maxHP':85,'paidFeats':{'4':'bioStabilizer'},'classChoiceAt3':'warrior.arch.mutation-efficiency plus actual separate Active choice','equipped':['warrior.supplement.bloodthick-node','warrior.supplement.ironhide-graft'],'slotSources':['warrior.supplement.mutation-slot-i','warrior.supplement.mutation-slot-ii'],'actualActivationHistory':'Two lawful prior activations with actual costs/durations supplied externally; no fresh injection or invented dose in this diagnostic','reserveMaximum':27},
 'HERBALIST-W8':{'scope':'Paid feature/skill slice; actual permanent Nature5+ and WIS13 acquisition credential, kit, suitable herbs and container must be supplied','class':'Wizard','level':8,'PB':3,'WIS':16,'paidFeats':{'4':'herbalist'},'trainedNatureCredential':'External actual acquisition premise, not a free proficiency or a temporary bonus'}}
cases=[]
def add(id,refs,premises,initial,events,final,expected):
 for k,v in expected.items():equal(id+' '+k,final[k],v)
 cases.append({'id':id,'sourceRefs':refs,'premises':premises,'initialState':deepcopy(initial),'events':deepcopy(events),'finalState':deepcopy(final),'independentExpectedFields':deepcopy(expected),'runtimeExecuted':False,'scope':'Own isolated specification from the exact candidate and accepted interfaces; actual providers, campaign facts and engine dispatch remain external.'})

def heal(s,raw,*,half=False,blocked=False,reserve=None,passive=False,no_secondary=False):
 # These vectors intentionally have no conditional class bonuses, per-die reducers,
 # competing local reducers or other multipliers. Do not claim the full healing engine.
 legal=0 if blocked else (raw//2 if half else raw)
 ceiling=max(1,s['maxHP']-1) if s['wounds']>=3 else s['maxHP']
 room=max(0,ceiling-s['HP']);available=s.get(reserve,0) if reserve else legal
 gain=min(legal,room,available);excess=max(0,legal-max(0,s['maxHP']-s['HP']))
 s['HP']+=gain
 if reserve:s[reserve]-=gain
 return {'raw':raw,'postReductionLegal':legal,'effectiveCeiling':ceiling,'ordinaryMissingBefore':max(0,s['maxHP']-(s['HP']-gain)),'actualGain':gain,'reserveSpent':gain if reserve else 0,'mathematicalExcess':excess,'eligibleExcessBeforeAnyConverter':0 if passive or no_secondary else excess,'secondaryHealingResourceTriggersAllowed':not no_secondary,'conversionActuallyExecuted':False}

# Durable + Quick Recovery: actual per-die floor, one addition per beneficial rest.
def hd_state(**kw):
 s={'HP':20,'maxHP':85,'wounds':0,'CONModifier':3,'PB':3,'remainingHD':8,'spentHD':0,'quickRestClaims':[],'appliedEvents':[],'RP':0,'reserve':5,'kitCharges':10,'lastHealing':None};s.update(kw);return s
def hd_event(s,e):
 if e['id'] in s['appliedEvents']:return {'replay':True,'noMutation':True}
 if not e.get('actualBeneficialCompletedRest',True):return {'admitted':False,'reason':'no actual beneficial completed rest recovery permission'}
 rolls=e['rolls']
 if not rolls:return {'admitted':False,'reason':'no spent Hit Die; no Quick Recovery claim'}
 assert 0<len(rolls)<=s['remainingHD'] and all(1<=n<=e.get('dieSize',12) for n in rolls)
 amounts=[max(n+s['CONModifier'],2*s['CONModifier'],0) for n in rolls]
 extra=s['PB'] if e['restId'] not in s['quickRestClaims'] and e.get('quick',True) else 0
 if extra:s['quickRestClaims'].append(e['restId'])
 s['remainingHD']-=len(rolls);s['spentHD']+=len(rolls);s['appliedEvents'].append(e['id'])
 s['lastHealing']=heal(s,sum(amounts)+extra,half=e.get('totem',False),blocked=e.get('blocked',False))
 return {'individualDieAmounts':amounts,'quickPB':extra,'ordinaryHealing':deepcopy(s['lastHealing'])}
def hd_case(id,initial,inputs,expected):
 s=deepcopy(initial);events=[]
 for e in inputs:
  before=deepcopy(s);receipt=hd_event(s,e);events.append({'input':e,'before':before,'receipt':receipt,'after':deepcopy(s)})
 add(id,['feat:durable','feat:quick_recovery','healing:ordinary','core:wounds','shared:FS-06'],{'actor':'HD-W8 unless signed-CON case','restLegality':'actual completed one-hour rest within at-most-two allowance supplied; no rest is completed/reset by this function','totemIfPresent':'actual operative Shaman card42 aura/paid source supplied, not conjured by boolean','broadBlockIfPresent':'actual current broad HP-gain prohibition supplied','noOtherModifiers':True},initial,events,s,expected)
hd_case('FH89-HD01-installments',hd_state(),[{'id':'a','restId':'R1','rolls':[1,2]},{'id':'b','restId':'R1','rolls':[1]}],{'HP':41,'remainingHD':5,'spentHD':3,'quickRestClaims':['R1']})
hd_case('FH89-HD02-blocked-first',hd_state(),[{'id':'a','restId':'R1','rolls':[1],'blocked':True},{'id':'b','restId':'R1','rolls':[1]}],{'HP':26,'spentHD':2,'quickRestClaims':['R1']})
hd_case('FH89-HD03-full-first',hd_state(HP=85),[{'id':'a','restId':'R1','rolls':[1]}],{'HP':85,'spentHD':1,'quickRestClaims':['R1']})
hd_case('FH89-HD04-no-dice',hd_state(),[{'id':'a','restId':'R1','rolls':[]}],{'HP':20,'spentHD':0,'quickRestClaims':[],'appliedEvents':[]})
hd_case('FH89-HD05-critical',hd_state(HP=80,wounds=3),[{'id':'a','restId':'R1','rolls':[1]}],{'HP':84,'spentHD':1,'wounds':3})
hd_case('FH89-HD06-critical-already-full',hd_state(HP=85,wounds=3),[{'id':'a','restId':'R1','rolls':[1]}],{'HP':85,'spentHD':1,'wounds':3})
hd_case('FH89-HD07-local-half',hd_state(wounds=2),[{'id':'a','restId':'R1','rolls':[1],'totem':True}],{'HP':24,'spentHD':1,'wounds':2})
hd_case('FH89-HD08-duplicate',hd_state(),[{'id':'a','restId':'R1','rolls':[1]},{'id':'a','restId':'R1','rolls':[1]}],{'HP':29,'spentHD':1,'appliedEvents':['a']})
hd_case('FH89-HD09-third-rest-ineligible',hd_state(),[{'id':'a','restId':'R3','rolls':[1],'actualBeneficialCompletedRest':False}],{'HP':20,'spentHD':0,'quickRestClaims':[],'appliedEvents':[]})
hd_case('FH89-HD10-interrupted-rest',hd_state(),[{'id':'a','restId':'interrupted','rolls':[1],'actualBeneficialCompletedRest':False}],{'HP':20,'spentHD':0,'quickRestClaims':[]})
hd_case('FH89-HD11-signed-con-zero',hd_state(CONModifier=-1,PB=2,remainingHD=4,HP=3,maxHP=14),[{'id':'a','restId':'R1','rolls':[1],'dieSize':6,'quick':False}],{'HP':3,'spentHD':1,'quickRestClaims':[]})
hd_case('FH89-HD12-signed-con-positive',hd_state(CONModifier=-1,PB=2,remainingHD=4,HP=3,maxHP=14),[{'id':'a','restId':'R1','rolls':[6],'dieSize':6,'quick':False}],{'HP':8,'spentHD':1,'quickRestClaims':[]})

# Long Rest HD recovery is its own operation; these vectors do not simulate the rest's other rewards.
for spent,wounds,expected in [(0,0,0),(1,0,1),(3,0,2),(3,1,1),(5,2,1),(5,3,0),(8,3,1)]:
 initial={'totalHD':8,'unspentHD':8-spent,'spentHD':spent,'wounds':wounds,'HP':20}
 restored=min(spent,max(0,ceil(Fraction(spent,2))-wounds));s=deepcopy(initial);s['unspentHD']+=restored;s['spentHD']-=restored;s['HDRecovered']=restored
 add(f'FH89-LR-{spent}-{wounds}',['core:wounds','loop:Long Rest','shared:FS-06'],{'actualBeneficialLongRestAlreadyCompleted':'external full Watch/24h eligibility premise','otherRestRewards':'outside this isolated HD recovery operation'},initial,[{'operation':'recover actual expended Hit Dice once','normalRecovery':ceil(Fraction(spent,2))}],s,{'HDRecovered':expected,'HP':20,'wounds':wounds})

# Ordinary Healer versus direct Field Surgeon. Simultaneous mixed-feature ordering is not invented.
def patient(**kw):
 s={'HP':0,'maxHP':85,'wounds':2,'life':'dying','stableDeadline':None,'deathSuccess':1,'deathFailure':1,'kitCharges':10,'kitWeightLb':3,'recipientRestEpoch':'SR1','recipientLREpoch':'LR1','healerClaims':[],'surgeonClaims':[],'eventsApplied':[],'actionsSpent':0,'prone':True};s.update(kw);return s
def stabilize(s,now,d4):
 if s['life']!='dying' or s['HP']!=0:return False
 s['life']='stable';s['deathSuccess']=s['deathFailure']=0;s['stableDeadline']=now+d4*3600;return True
def become_positive(s):
 if s['HP']>0:s['life']='living';s['stableDeadline']=None;s['deathSuccess']=s['deathFailure']=0
def medic(s,e):
 if e['id'] in s['eventsApplied']:return {'duplicate':True}
 if s['life']=='dead':return {'admitted':False,'reason':'dead target'}
 if e['mode']=='surgeon':
  if not e['actualNewStabilization'] or s['recipientLREpoch'] in s['surgeonClaims']:return {'admitted':False,'reason':'no new eligible stabilization or family spent'}
  s['surgeonClaims'].append(s['recipientLREpoch']);s['eventsApplied'].append(e['id'])
  if not e.get('blocked',False):s['HP']=min(s['maxHP'],s['HP']+1);become_positive(s)
  return {'operation':'direct recovery','ordinaryHealingModifiersApplied':False,'actualGain':0 if e.get('blocked',False) else 1,'newActionOrKitCost':0}
 healing=e['mode']=='healer' and s['recipientRestEpoch'] not in s['healerClaims']
 if not healing and s['life']!='dying':return {'admitted':False,'reason':'no available treatment or actual stabilization'}
 assert s['kitCharges']>0
 s['kitCharges']-=1;s['actionsSpent']+=1;s['eventsApplied'].append(e['id'])
 if healing:s['healerClaims'].append(s['recipientRestEpoch'])
 transitioned=stabilize(s,e['time'],e.get('stableD4',2))
 result=heal(s,max(0,sum(e['dice'])+e['WISModifier']),half=e.get('totem',False),blocked=e.get('blocked',False)) if healing else None
 become_positive(s)
 return {'genuineStabilization':transitioned,'ordinaryHealing':result,'oneChargeFundsTreatment':True,'fieldSurgeonNotAutomaticallyGranted':True}
def med_case(id,initial,inputs,expected):
 s=deepcopy(initial);events=[]
 for e in inputs:
  b=deepcopy(s);receipt=medic(s,e);events.append({'input':e,'before':b,'receipt':receipt,'after':deepcopy(s)})
 add(id,['feat:healer','feat:field_surgeon','core:stabilize','equipment:kit','healing:ordinary-versus-direct'],{'actor':'MEDIC-W8','actualActionHandAdjacencyLivingAccess':'explicit fixture premise at each admitted Action','restEpochs':'actual recipient completed-rest identities supplied; practitioner swap does not change them','noSimultaneousCrossFeatureDispatcherClaim':True},initial,events,s,expected)
base={'id':'med1','mode':'healer','time':100,'dice':[3,2],'WISModifier':3,'stableD4':2}
med_case('FH89-MED01-dying-treatment',patient(),[base],{'HP':8,'life':'living','kitCharges':9,'actionsSpent':1,'stableDeadline':None,'wounds':2,'prone':True,'healerClaims':['SR1']})
med_case('FH89-MED02-blocked-treatment',patient(),[dict(base,blocked=True)],{'HP':0,'life':'stable','kitCharges':9,'stableDeadline':7300,'healerClaims':['SR1'],'deathFailure':0})
med_case('FH89-MED03-already-stable',patient(life='stable',stableDeadline=9000),[base],{'HP':8,'life':'living','kitCharges':9,'stableDeadline':None})
med_case('FH89-MED04-dead-ineligible',patient(life='dead'),[base],{'HP':0,'life':'dead','kitCharges':10,'actionsSpent':0,'healerClaims':[]})
med_case('FH89-MED05-shared-recipient-use',patient(),[base,dict(base,id='med2',practitioner='second-actual-Healer')],{'HP':8,'kitCharges':9,'actionsSpent':1,'healerClaims':['SR1']})
med_case('FH89-MED06-spent-still-stabilizes',patient(healerClaims=['SR1']),[base],{'HP':0,'life':'stable','kitCharges':9,'actionsSpent':1,'stableDeadline':7300,'healerClaims':['SR1']})
med_case('FH89-MED07-ordinary-halved',patient(),[dict(base,totem=True)],{'HP':4,'life':'living','kitCharges':9,'wounds':2})
fs={'id':'fs1','mode':'surgeon','actualNewStabilization':True,'blocked':False,'totem':True}
med_case('FH89-FS01-direct-ignores-ordinary-half',patient(life='stable',stableDeadline=7300,kitCharges=9,actionsSpent=1,deathSuccess=0,deathFailure=0),[fs],{'HP':1,'life':'living','stableDeadline':None,'kitCharges':9,'actionsSpent':1,'surgeonClaims':['LR1'],'wounds':2})
med_case('FH89-FS02-blocked-spends-family',patient(life='stable',stableDeadline=7300,deathSuccess=0,deathFailure=0),[dict(fs,blocked=True),dict(fs,id='fs2',practitioner='another-actual-surgeon')],{'HP':0,'life':'stable','stableDeadline':7300,'surgeonClaims':['LR1'],'kitCharges':10})
med_case('FH89-FS03-no-new-stabilization',patient(life='stable',stableDeadline=7300),[dict(fs,actualNewStabilization=False)],{'HP':0,'life':'stable','surgeonClaims':[],'stableDeadline':7300})

# Life Drinker exact damage metric and two ordered events drawing one finite personal reserve.
def life_case(id,hp,reserve,rawDamage,targetHP,targetTemp,critical,**opt):
 initial={'HP':hp,'maxHP':85,'wounds':opt.get('wounds',0),'lifeReserve':reserve,'mutationReserve':7,'level':8,'targetHP':targetHP,'targetTemp':targetTemp,'sourceReceipts':[]}
 s=deepcopy(initial);events=[]
 eligible=opt.get('eligible',True)
 absorbed=min(targetTemp,rawDamage);hpLoss=min(targetHP,max(0,rawDamage-absorbed));actual=absorbed+hpLoss
 s['targetTemp']-=absorbed;s['targetHP']-=hpLoss
 for trigger,base in [('critical',actual//2 if critical else 0),('drop',8 if targetHP>0 and s['targetHP']==0 else 0)]:
  if not eligible or not (critical if trigger=='critical' else targetHP>0 and s['targetHP']==0):continue
  b=deepcopy(s);s['sourceReceipts'].append(id+':'+trigger)
  result=heal(s,base,blocked=opt.get('blocked',False),reserve='lifeReserve',no_secondary=True)
  events.append({'trigger':trigger,'actualDamageDealt':actual,'before':b,'ordinaryHealing':result,'after':deepcopy(s)})
 add(id,['feat:life_drinker','shared:FS-07','healing:actualDamageDealt','healing:reserve'],{'actor':'LIFE-W8','actualDirectMeleeCriticalAndHostile':'qualified attack outcome supplied; no attack/save/defense engine executed','damageAlreadyPostDefenses':True,'sourceEligible':eligible,'excludedOrigins':'copied/reflected/no-resource/cost/artificial kills cannot qualify','riderNotAddedAgain':'any actual blood-qualified1d4 already included in the supplied native resolved damage'},initial,events,s,opt['expected'])
life_case('FH89-LIFE01-overkill-two-triggers',20,16,12,3,4,True,expected={'HP':31,'lifeReserve':5,'targetHP':0,'targetTemp':0,'mutationReserve':7})
life_case('FH89-LIFE02-reserve-two',20,2,12,3,4,True,expected={'HP':22,'lifeReserve':0,'targetHP':0})
life_case('FH89-LIFE03-cap-first-then-zero',83,16,12,3,4,True,expected={'HP':85,'lifeReserve':14,'targetHP':0})
life_case('FH89-LIFE04-blocked',20,16,12,3,4,True,blocked=True,expected={'HP':20,'lifeReserve':16,'targetHP':0})
life_case('FH89-LIFE05-critical-ceiling',84,16,12,3,4,True,wounds=3,expected={'HP':84,'lifeReserve':16,'wounds':3})
life_case('FH89-LIFE06-no-resource-source',20,16,12,3,4,True,eligible=False,expected={'HP':20,'lifeReserve':16,'sourceReceipts':[]})
life_case('FH89-LIFE07-absorbed-temp-only',20,16,5,30,8,True,expected={'HP':22,'lifeReserve':14,'targetHP':30,'targetTemp':3})

# Bio-Stabilizer modifies a real Bloodthick pulse, including BT0; no independent pulse.
def bio_case(id,hp,reserve,bt,mutations,expected,**opt):
 initial={'HP':hp,'maxHP':85,'wounds':opt.get('wounds',0),'mutationReserve':reserve,'lifeReserve':11,'BT':bt,'pulseReceipts':[],'processedOriginalStartMarkers':[],'alive':opt.get('alive',True)};s=deepcopy(initial)
 if opt.get('regularStart',True):s['processedOriginalStartMarkers'].append('original-start-7')
 eligible=opt.get('realEncounter',True) and opt.get('regularStart',True) and opt.get('bloodthickActive',True) and s['alive'] and not opt.get('passiveBlocked',False)
 events=[]
 if eligible:
  base=min(bt,4 if opt.get('stackOverflow',False) else 3)+(1 if mutations>=2 else 0)
  s['pulseReceipts'].append('Bloodthick:original-start-7')
  result=heal(s,base,half=opt.get('totem',False),blocked=opt.get('blocked',False),reserve='mutationReserve',passive=True)
  events=[{'actualRegularStart':'original-start-7','baseBT':bt,'activeMutationCount':mutations,'afterEarlierLifeProcessing':True,'healing':result}]
 add(id,['feat:bioStabilizer','warrior:cards/73','warrior:engine/24','combat:regular-start-order','healing:passive-excess-exclusion'],{'actor':'BIO-W8 except explicitly qualified StackOverflow variant','actualEligibility':opt,'earlierDeathSave':'already resolved authoritative outcome supplied; function does not execute prior death save or grant an action at0','otherMutationIfActive':'actual Ironhide Graft; two equipped slots and Mutation Efficiency supplied','sourcePulseOnce':'one original marker only; this does not dispatch the world scheduler'},initial,events,s,expected)
bio_case('FH89-BIO01-reserve-one',20,1,2,2,{'HP':21,'mutationReserve':0,'lifeReserve':11})
bio_case('FH89-BIO02-BT-zero',20,10,0,2,{'HP':21,'mutationReserve':9})
bio_case('FH89-BIO03-one-mutation',20,10,2,1,{'HP':22,'mutationReserve':8})
bio_case('FH89-BIO04-full',85,10,2,2,{'HP':85,'mutationReserve':10})
bio_case('FH89-BIO05-critical',84,10,2,2,{'HP':84,'mutationReserve':10},wounds=3)
bio_case('FH89-BIO06-broad-block',20,10,2,2,{'HP':20,'mutationReserve':10},blocked=True)
bio_case('FH89-BIO07-passive-block',20,10,2,2,{'HP':20,'mutationReserve':10,'pulseReceipts':[]},passiveBlocked=True)
bio_case('FH89-BIO08-outside-encounter',20,10,2,2,{'HP':20,'mutationReserve':10,'pulseReceipts':[]},realEncounter=False)
bio_case('FH89-BIO09-extra-turn',20,10,2,2,{'HP':20,'mutationReserve':10,'pulseReceipts':[]},regularStart=False)
bio_case('FH89-BIO10-dormant',20,10,2,2,{'HP':20,'mutationReserve':10,'pulseReceipts':[]},bloodthickActive=False)
bio_case('FH89-BIO11-survives-prior-death-save',0,10,2,2,{'HP':3,'mutationReserve':7})
bio_case('FH89-BIO12-died-before-pulse',0,10,2,2,{'HP':0,'mutationReserve':10,'pulseReceipts':[]},alive=False)
bio_case('FH89-BIO13-half',20,10,2,2,{'HP':21,'mutationReserve':9},totem=True)
bio_case('FH89-BIO14-empty-reserve',20,0,2,2,{'HP':20,'mutationReserve':0})

# Herbalist creates one actual dose at rest completion with snapshotted PB, then consumes it.
for suffix,beneficial,blocked,expectedHP in [('completed',True,False,27),('blocked-application',True,True,20),('interrupted',False,False,20)]:
 initial={'HP':20,'maxHP':85,'wounds':0,'herbsHalfPoundLots':1,'actualDoseContainerIdentity':'container-1','preparedMinutes':0,'salves':[],'doseUsed':False,'RP':0};s=deepcopy(initial)
 s['herbsHalfPoundLots']-=1;s['preparedMinutes']=30
 events=[{'time':3600,'operation':'commit actual stock and30 permitted light-activity minutes','noConcurrentGuardOrWork':True}]
 if beneficial:
  dose={'id':'salve-LR1','container':'container-1','recordedPB':3,'createdAt':28800,'expiresAt':115200};s['salves'].append(dose)
  events.append({'time':28800,'operation':'actual beneficial Long Rest completion','dose':deepcopy(dose)})
  result=heal(s,4+dose['recordedPB'],blocked=blocked);s['salves']=[];s['doseUsed']=True
  events.append({'time':28860,'operation':'one actual Action with hand/adjacency applies complete dose','d6':4,'healing':result})
 add('FH89-HERB-'+suffix,['feat:herbalist','shared:FS-06','healing:ordinary'],{'actor':'HERBALIST-W8','actualHerbsKitCleanSurfaceContainerAndEligibleLightActivity':'explicit external premises; no generic work/rest overlap','containerScope':'Actual container identity retained. This diagnostic selects no new salvage/destruction rule for the physical vessel after interruption or application.','sourceStudyNotResearchDiscounted':True,'noRestCreatedByScript':True},initial,events,s,{'HP':expectedHP,'herbsHalfPoundLots':0,'actualDoseContainerIdentity':'container-1','salves':[],'doseUsed':beneficial,'RP':0})

# Persistent reserve capacities: advancement and borrowed rest labels do not refill pools.
for name,maximum,current,newmaximum,expected in [('level-up',16,5,18,5),('level-loss',16,15,12,12),('suppression-restored',16,5,16,5)]:
 initial={'maximum':maximum,'current':current,'HP':20};s={'maximum':newmaximum,'current':min(current,newmaximum),'HP':20}
 add('FH89-RESERVE-'+name,['feat:life_drinker','shared:FS-06'],{'actualAuthorizedCapacityChange':'external premise, no newly granted level-loss or retraining rule','notAnEligibleRefill':True},initial,[{'newMaximum':newmaximum}],s,{'current':expected,'HP':20})

for case in cases:
 for key in ['maxHP','wounds','RP','kitWeightLb','prone']:
  if key in case['initialState']:equal(case['id']+' preserves '+key,case['finalState'][key],case['initialState'][key])
 if case['id'].startswith('FH89-HD'):
  for key in ['reserve','kitCharges']:equal(case['id']+' unrelated '+key,case['finalState'][key],case['initialState'][key])
 if case['id'].startswith('FH89-BIO'):
  equal(case['id']+' separate Life reserve',case['finalState']['lifeReserve'],case['initialState']['lifeReserve'])
 if case['id'].startswith('FH89-LIFE'):
  equal(case['id']+' separate Mutation reserve',case['finalState']['mutationReserve'],case['initialState']['mutationReserve'])
for p,b in before.items():equal('Full source unchanged '+b['path'],info(p),b)
check('Distinct case identities',len(cases)==len({x['id'] for x in cases}))
report={'id':'FEAT335-HEALING-COMPOSITIONS-89','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'ISOLATED_SOURCE_QUALIFIED_SPECIFICATIONS_PARENT_EXACT_REVIEW_PENDING',
 'sourceBindings':[before[p] for p in source_paths],'fullSelectedFeatRecords':selected,'fullPrerequisiteFeatRecords':[candidate['records'][294]],'fullSharedRules':shared,'actorSlices':actors,'cases':cases,'caseCount':len(cases),'checks':checks,'passed':len(checks),'failed':0,
 'scope':['Seven exact feat records preserved in full. Durable/Quick Recovery including actual per-die minimum and rest-family consumption; Core Wound Hit Die recovery; Healer and Field Surgeon separate operations; Life Drinker ordered finite healing; Bio-Stabilizer passive pulse/reserve; Herbalist actual dose lifecycle.','All expected scalar outcomes are independently specified; functions are newly authored isolated models from source. Full initial/final states and actual input receipts retained.','Sources/actors/stocks/world eligibility are conditional fixtures, not authenticated campaign characters or engine-generated events. No source feature, lawful preparation, component or actual rest is silently granted.'],
 'remainingScope':['Parent335 all exact semantic/acquisition gates remain. These are bounded cases, not execution of seven complete source features.','Combined nested Healer/Field Surgeon/Field Medic trigger scheduling must retain exact declared application/order and normal state transitions; not simulated by these separate vectors.','Full healing conditional-add-on preview, competing reducers, actual maximum-HP engine, resurrection, death saves and global scheduler remain governed by their existing contracts; only explicitly named arithmetic/inputs above executed.','Life Drinker attack and rider eligibility and inherited origin flags are supplied outcomes; no attack engine or meaningful-hostile oracle executed.','Actual rest legality, resource-refill dispatcher, equipment custody/save persistence and completed character acquisition remain integration obligations.'],
 'approvalBoundaries':{'sourcePreserved':True,'canonicalApplied':False,'parent335Accepted':False,'runtimeExecuted':False,'humanGameplayTested':False,'balanceApproved':False,'cosmologyChanged':False,'releaseApproved':False},
 'actualExecution':{'kind':'Own Python standard-library isolated specifications','downloadedCodeExecuted':False,'projectModulesImported':False,'worldRuntimeExecuted':False},'sourceInformationDeleted':False}
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
report['script']=info(SAVED)
with OUT.open('xb') as f:f.write(enc(report))
files={'REPORT.json':OUT.read_bytes(),'INDEPENDENT_SPECIFICATION.py':SAVED.read_bytes()}
for p in source_paths:files['sources/'+p.relative_to(G).as_posix()]=p.read_bytes()
manifest={'id':'FEAT335-HEALING89-MANIFEST','files':[{'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()} for name,data in sorted(files.items())],'executionBoundary':'Read-only source packet. Supplied code need not be run; no execution permission is conveyed.'}
files['MANIFEST.json']=enc(manifest)
with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,data in files.items():z.writestr(name,data)
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(files)==len(set(z.namelist()))
 for name,data in files.items():assert z.read(name)==data
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'cases':len(cases),'checks':len(checks),'failed':0,'fullSourceFiles':len(source_paths),'zipMembers':len(files)},indent=2))
