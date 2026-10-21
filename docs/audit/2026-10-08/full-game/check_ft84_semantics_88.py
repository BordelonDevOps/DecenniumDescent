"""One-shot independent source/arithmetic/state review. Does not import returned code."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
from math import ceil
from datetime import datetime, timezone
import json, hashlib

G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
R=G/'DescentReviewChanges/ReviewBible'
P=A/'feat335-work-compositions84-part5-return-01'
OUT=A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json'
SAVED=A/Path(__file__).name
assert not OUT.exists() and not SAVED.exists(), 'One-shot outputs already exist'
def j(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(name,value,detail=None):
 row={'check':name,'pass':bool(value)}
 if detail is not None:row['detail']=detail
 checks.append(row)
def eq(name,actual,expected):ck(name,actual==expected,None if actual==expected else {'actual':actual,'expected':expected})
outer=j(P/'CASEBOOK.json')['cases'];C=[c['completeSpecificationCase'] for c in outer]
def check(i,label,v):ck(C[i]['id']+': '+label,v)
def same(i,label,a,b):eq(C[i]['id']+': '+label,a,b)
prior=j(A/'ACTIVE_AUTHORING_CHECKPOINT_GPT_PERTINENT_INTAKE_87.json')
baselines=[prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]
for b in baselines:eq('Canonical unchanged '+b['path'],info(G/b['path']),b)
bindings=j(P/'SOURCE_BINDINGS.json')['sources']
for path,b in bindings.items():
 got=info(G/path);eq('Bound source remains exact '+path,(got['bytes'],got['sha256']),(b['bytes'],b['sha256']))
wizard=j(R/'data/public/class_playtests/wizard.json')
scribing=wizard['cards'][1]
ck('Wizard Spell Scribing actual rank formula','1 hour and 25 gp' in scribing['effect'] and '2 hours and 50 gp' in scribing['effect'])
recipe=next(x for x in j(R/'data/crafting/advanced_craft_recipe_candidate_public.json')['cards'] if x['recipeId']=='recipe-121')
rs=recipe['sourceRecipe'];rw=recipe['operational']['work']
eq('Recipe121 actual research minimum',rs['discovery']['minimumResearchHours'],0)
eq('Recipe121 actual construction and incorporation',(rw['activeMinutes'],rw['includedFirstPhaseMinutes'],rw['DC']),(240,15,8))
eq('Recipe121 actual ingredient quantities',[(x['name'],x['quantity']) for x in rs['components']],[('Luminous Crystal',2),('bronze dragon rib',1)])
eq('Recipe121 actual host reserve and assistant cap',(recipe['operational']['maximumOrderedBodyReserve'],rs['workRequirements']['maximumAssistants']),(6,0))
model=j(P/'MODEL.json');procedures=j(P/'SELECTED_PROCEDURES.json')['procedures']
candidate=j(R/'data/director/feat_candidates/exact_01/candidate.json')
for p in procedures:
 record=next(x for x in candidate['records'] if x['id']==p['id'])
 eq(p['id']+' complete original preserved',p['completeOriginalRecord'],record)
 eq(p['id']+' complete operative before',p['before'],record['operationalRules'])
 ck(p['id']+' existing operative text retained',p['after'].startswith(p['before']))
 ck(p['id']+' selection/exact/runtime remain false',not p['candidateSelectionEnabled'] and not p['exactApproved'] and not p['runtimeApproved'])
eq('Six complete procedure successors',len(procedures),6)
eq('All57 distinct cases',len({x['id'] for x in C}),57)
for flag in ['canonicalApplied','parent335Accepted','runtimeImplemented','sourceInformationDeleted']:eq('MODEL '+flag,model[flag],False)
for i,x in enumerate(C):
 check(i,'authored conditional case, no runtime execution',x['runtimeExecuted'] is False and outer[i]['realRuntimeExecuted'] is False and outer[i]['ruleSelectedButProjectApplied'] is False)
 check(i,'explicit scope/premises/source references',bool(x['scope']) and bool(x['premises']) and bool(outer[i]['sourceRefs']))

# Independent phase integration from initial credit and actual interval inputs.
# 900-active-second phases; exact final remaining phase; interruption forfeits pending only.
def phases(i,required,finalkey=None):
 x=C[i];initial=x['initialState'];s={'creditSeconds':initial.get('creditSeconds',initial.get('creditedSeconds',0)),'pendingSeconds':0,'lostSeconds':0,'activeSeconds':0,'time':0}
 for n,e in enumerate(x['events']):
  if not isinstance(e.get('event'),dict):continue
  same(i,f'phase{n} complete before',e['before'],s)
  ev=e['event'];check(i,f'phase{n} interval nonoverlap',ev['start']>=s['time'])
  work=ev['seconds'];s['activeSeconds']+=work;s['time']=ev['start']+work
  while work>0:
   threshold=min(900,required-s['creditSeconds'])
   assert threshold>0,(i,'unpermitted surplus work')
   take=min(work,threshold-s['pendingSeconds']);work-=take;s['pendingSeconds']+=take
   if s['pendingSeconds']==threshold:s['creditSeconds']+=threshold;s['pendingSeconds']=0
  if ev.get('interrupt'):s['lostSeconds']+=s['pendingSeconds'];s['pendingSeconds']=0
  same(i,f'phase{n} complete after',e['after'],s)
 expected={'requiredSeconds':required,'creditedSeconds':s['creditSeconds'],'pendingSeconds':s['pendingSeconds'],'lostSeconds':s['lostSeconds'],'actualActiveSeconds':s['activeSeconds'],'elapsedSeconds':s['time'],'complete':s['creditSeconds']==required,'completionOpportunities':int(s['creditSeconds']==required)}
 final=x['finalState'][finalkey] if finalkey else x['finalState']
 same(i,'all phase summary fields',{k:v for k,v in final.items() if k!='trace'},expected)
 return expected

# Written copying versus actual teaching, material identity, fractional stock and payment.
for i in [0,1,2]:
 x=C[i];s=x['initialState'];f=x['finalState'];actor=s['actor'];src=s['source']
 written=src['completeLegitimateText'] and src['languageNotationUsable'] and src['bookAlreadyOwned']
 required=480*60//(2 if written else 1)
 progress=phases(i,required,'credits');total=F(0);remaining=[]
 for lot,line in zip(s['materialLots'],f['materialsConsumed']['lines']):
  factor=F(3,4) if written and lot['category']=='mundane' else F(1)
  units=F(lot['quantity'])*factor
  if lot['indivisible']:units=F(ceil(units))
  same(i,lot['id']+' consumed units',F(line['required']),units)
  same(i,lot['id']+' exact line price',F(line['lineExactCp']),units*lot['unitCp'])
  same(i,lot['id']+' factor',F(line['reductionFactor']),factor)
  check(i,lot['id']+' actual stock sufficient',F(lot['quantity'])>=units)
  total+=units*lot['unitCp'];remaining.append((lot['id'],F(lot['quantity'])-units))
 same(i,'remaining stock',[(r['id'],F(r['quantity'])) for r in f['materialsRemaining']],remaining)
 same(i,'aggregate exact bill',F(f['materialsConsumed']['exactTotalCp']),total)
 same(i,'single final copper ceiling',f['materialsConsumed']['finalPurchaseCp'],ceil(total))
 fee=2*(progress['actualActiveSeconds']//60) if i==1 else 0
 same(i,'real agreed instructor fee',f['teacherFeeCp'],fee)
 same(i,'wallet after bill and fees',f['walletCp'],s['walletCp']-ceil(total)-fee)
 same(i,'only actual ritual record',f['bookEntries'],['Detect Magic ritual-record only'])
 check(i,'no classbook cast XP or RP creation',not f['normalWizardBookAcquisition'] and f['noCastOrXP'] and f['RP']==actor['RP']==0)
 same(i,'actual level12 PB and skill',(actor['PB'],actor['Arcana'],actor['History']),(4,7,7))
 same(i,'three distinct paid feat opportunities',sorted(actor['paidMilestones']),['12','4','8'])
 check(i,'no concurrent ASI gains',actor['noASIIncreasesAtThoseMilestones'])
same(3,'full genuine unclassified bill can coexist with time benefit',C[3]['finalState'],{'walletCp':1000,'bookEntries':['Detect Magic ritual-record'],'activeSeconds':14400,'materialDiscount':0})
for i in range(4,10):
 for k,v in C[i]['initialState'].items():same(i,'predicate-only no debit '+k,C[i]['finalState'][k],v)
 check(i,'predicate disposition disclosed',bool(C[i]['finalState']['adjudication']))
phases(10,14400,'credit')
same(10,'successful ink plus actual declared waste',F(C[10]['finalState']['inkConsumed']),F(15,4)+F(1,4))
same(10,'ink remains physical',C[10]['finalState']['inkRemaining'],1)
same(11,'strongest single time factor rounded once',C[11]['finalState']['minutes'],ceil(F(C[11]['initialState']['baseMinutes'],2)))
same(11,'aggregate small divisible bill',C[11]['finalState']['bill']['finalPurchaseCp'],ceil(F(2)*F(3,4)+F(2)*F(3,4)+1))
same(11,'single indivisible unit retained',C[11]['finalState']['oneIndivisibleSheetRequired'],ceil(F(3,4)))
same(12,'separate rank2 Wizard route',(C[12]['finalState']['activeMinutes'],C[12]['finalState']['costCp'],C[12]['finalState']['RitualBookEntryGranted']),(2*60,2*25*100,False))
same(13,'prospective remaining-work discount',C[13]['finalState'],{'actualWorkMinutes':120+ceil(F(480-120,2)),'completedRitualRecords':1,'retroactiveRefundCp':0})

# Narrow research processes, actual assistants, one proficiency, completion and no manufacturing.
for i in [14,15]:
 x=C[i];s=x['initialState'];f=x['finalState'];src=s['source']
 baseline=480 if i==14 else 60*max(8,rs['discovery']['minimumResearchHours'])
 same(i,'source-bound baseline',src['baselineMinutes'],baseline)
 progress=phases(i,baseline*30,'progress')
 roll=x['events'][-1]['result'];modifier=(s['INT']-10)//2;pb=2+(s['level']-1)//4
 assistant=1 if src['assistant'] is not None else 0
 same(i,'single ability/PB/assistant arithmetic',roll['total'],roll['die']+modifier+pb+assistant)
 same(i,'source DC',roll['DC'],15 if i==14 else rw['DC'])
 same(i,'binary success',roll['success'],roll['total']>=roll['DC'])
 same(i,'completion roll mirror',f['completionCheck'],roll)
 fee=2*progress['actualActiveSeconds']//60 if i==14 else 200
 same(i,'fee retains lost actual work',f['actualAgreedFeeCp'],fee)
 same(i,'wallet',f['walletCp'],s['walletCp']-fee)
 same(i,'actual notes stock',f['notesSheetsUsed']+f['notesSheetsRemaining'],s['workingStock']['ordinaryNotesSheets'])
 check(i,'no manufactured stock output or extra proficiency',f['manufactureInputsConsumed']==0 and f['XP']==0 and f['RP']==0 and not f['newLanguageOrItem'])
for i in [16,17]:
 e=C[i]['events'][0];f=C[i]['finalState'];total=e['die']+e['INT']+e['PB']+int(C[i]['premises']['actualEligibleAssistantAllWork'])
 same(i,'actual assistant comparison',(f['total'],f['success']),(total,total>=e['DC']))
 same(i,'no unsupported retry',f['retryWithoutNewEvidenceOrMethod'],False)
phases(18,ceil(F(481*60,2)))
phases(19,14400)
for i in range(20,26):
 same(i,'other process original duration',C[i]['finalState']['requiredMinutes'],C[i]['initialState']['requiredMinutes'])
 check(i,'no universal clock or knowledge',not C[i]['finalState']['newPhaseClockApplied'] and not C[i]['finalState']['newEvidenceGranted'])
for i in range(26,31):
 for k,v in C[i]['initialState'].items():same(i,'no invented admission '+k,C[i]['finalState'][k],v)
 check(i,'no extra roll or Watch',not C[i]['finalState']['extraRoll'] and not C[i]['finalState']['extraWorkWatch'])

# Native once/24h gadget commitment, uninterrupted work, one existing random result, and custody.
for i in [31,32,33,35]:
 x=C[i];s=deepcopy(x['initialState']);commit,finish=x['events'];start=commit['time']
 same(i,'full committed before state',commit['before'],s)
 check(i,'actual stock and elapsed-use gate',s['partsLots']>0 and start>=s['nextUseAt'])
 build='build-'+str(s['useSpent']+1)
 s['partsLots']-=1;s['useSpent']+=1;s['nextUseAt']=start+24*3600;s['receipts'].append(build);s['activeGadget']=None
 same(i,'complete commitment state',commit['after'],s)
 seconds=finish['time']-start;s['actualWorkSeconds']+=seconds
 required=600 if i==31 else 300
 if i==33:check(i,'interruption before required completion',seconds<required)
 else:
  same(i,'actual required uninterrupted time',seconds,required)
  s['activeGadget']={'id':build+'-body','profile':'clamp (source worked-case d4=3; activation not tested)','weightLb':1,'AC':10,'HP':1,'createdAt':finish['time'],'expiresAt':finish['time']+3600,'holder':s['owner'],'activationExecuted':False}
 same(i,'complete final construction state',finish['after'],s);same(i,'final state mirror',x['finalState'],s)
for i in [34,36,*range(38,43)]:same(i,'blocked/replay no physical or use reset',C[i]['finalState'],C[i]['initialState'])
s=deepcopy(C[37]['initialState']);s['activeGadget']['holder']='actual-recipient'
same(37,'actual handoff changes custody only',C[37]['finalState'],s)

# Unarmed physical kits: pauses retain usable work, failed closed attempt retains only real frame.
for i in [43,44,45]:
 x=C[i];s=deepcopy(x['initialState']);s['usableWorkSeconds']=0
 for n,e in enumerate(x['events']):
  same(i,f'kit{n} complete before',e['before'],s)
  seconds=e['end']-e['start'];s['actualWorkSeconds']+=seconds;s['usableWorkSeconds']+=seconds
  if 'die' in e:
   total=e['die']+(x['premises']['INT']-10)//2+x['premises']['PB'];success=total>=12
   same(i,'source binary task total',(e['total'],e['DC'],e['success']),(total,12,success))
   same(i,'completed required time',s['usableWorkSeconds'],30*60//2)
   s['cordLb']=0;s['attemptClosed']=True
   if success:
    s['frameLb']=0;s['kits']=[{'id':'kit-1','type':'snare','weightLb':2,'armed':False,'setter':None}]
  same(i,f'kit{n} complete after',e['after'],s)
 same(i,'complete kit final state',x['finalState'],s)
for i,discount in [(46,True),(47,False),(48,False),(49,False),(50,False),(51,True)]:
 x=C[i];s=x['initialState'];f=x['finalState']
 same(i,'source-qualified strongest active factor',f['activeMinutes'],ceil(F(s['baseMinutes'],2)) if discount else s['baseMinutes'])
 same(i,'separate conditional fixed wait unchanged',f['fixedWaitMinutes'],s['fixedWaitMinutes'])
x=C[52];credited=actual=0;lengths=[15*60,(240//2-15)*60]
same(52,'source-bound phase lengths',x['initialState']['phaseSeconds'],lengths)
for n,e in enumerate(x['events']):
 actual+=e['workSeconds'];done=e['workSeconds']==lengths[e['phase']]
 if done:credited+=lengths[e['phase']]
 same(52,f'phase{n} actual and credit',(e['actualSeconds'],e['creditedSeconds'],e['completed']),(actual,credited,done))
same(52,'completed labor, check still due, no output',x['finalState'],{'creditedSeconds':credited,'actualSeconds':actual,'completionCheckNowDue':True,'outputsAlreadyGranted':0})
for i in range(53,57):
 x=C[i];s=deepcopy(x['initialState']);e=x['events'][0]
 eligible=e['wholeJobMinutes']<=30 and e['insideRestMinutes']>=e['wholeJobMinutes']
 s['HP']=min(s['maxHP'],s['HP']+e['actualBaseRestoration']+(x['premises']['PB'] if eligible else 0))
 s['materialCp']-=e['spentMaterialCp'];s['beneficialRestGrantedByThisTest']=False
 same(i,'whole-job rest boundary and complete state',x['finalState'],s)

holds=j(P/'HOLD_REGISTER.json')
eq('Five independent whole-positive holds retained',holds['independentWholePositiveCaseHolds'],['IN6-09-A','IN6-09-B','EN5-01-A','EN5-01-B','EN6-03-B'])
eq('Seven narrowly disclosed integration holds',len(holds['holds']),7)
eq('Coverage unchanged',holds['appliedBaseline'],{'reviewed':525,'pending':323,'standalone':249,'interfaces':173,'acceptedUnapplied':50})
for b in baselines:eq('Final canonical unchanged '+b['path'],info(G/b['path']),b)
failed=[x for x in checks if not x['pass']]
if failed:
 print(json.dumps({'failed':failed,'passed':len(checks)-len(failed)},ensure_ascii=False,indent=2,default=str));raise SystemExit(1)
report={'id':'FT84-INDEPENDENT-SEMANTIC-REVIEW-88','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'ACCEPTED_SCOPED_AUTHORED_FOLLOWTHROUGH_UNAPPLIED_PARENT335_NOT_ACCEPTED',
 'archive':info(A/'DD_Feat335_Work_Compositions_84_Part5_Return_01.zip'),'model':info(P/'MODEL.json'),
 'priorIntake':info(A/'FEAT335_WORK_COMPOSITIONS_PART5_RETURN01_INTAKE_87.json'),
 'review':{'questionsReadInFull':3,'completeOriginalAndSuccessorProceduresRead':6,'completeCasesRead':57,'sourceCrossCheck':['Wizard Spell Scribing','LA06/LA07 language','Crafting/Harvest work and formula research','recipe-121','six affected feat records','Bowyer','Combat Engineering','Master Smithing','Tinker Adept'],
 'acceptedScope':['FT84-Q01 complete written ritual-copy predicate and actual bill classification','FT84-Q02 NEW phases for only LA07 ordinary Translate/Decipher and existing-available-formula research','FT84-Q03 source-authorized physical creation including Contraption and Trapsetter; original exclusions remain'],
 'newAuthorship':['Q01 narrow material category completion, not a universal bill','Q02 two-process fifteen-minute phase credit and exact final remainder','Q03 unphased assembly usable-work preservation without protection or free product'],
 'interpretationNotes':['Tutor presence alone does not disqualify actual complete written copying. Unclassified genuine full-price materials do not remove the independent time benefit.','Unpaid Spell Scribe predicate rejects the discount, not an independently legal baseline learning route.','Case31 is explicitly an independent baseline comparator before operative Craftsman; its printed paid-history slice is not used to claim an acquired-but-disabled live character.','Case19 assumes a real independently supported loss; it does not author a generic progress-loss source.','Kit usableWorkSeconds in a closed failed attempt is historical labor, not reusable new-job credit.','Category fixedWaitMinutes are explicitly conditional boundary fixtures, not new waits imposed on those processes.','Recipe121 case validates labor only; it does not claim completion roll, ingredient/output settlement or full recipe execution.'],
 'noConcreteSemanticContradictionFound':True},
 'coverageMeaning':'All57 authored cases were read. Independent calculations check time, bill, research rolls, stocks, complete gadget/kit/rest transitions and stated boundary nonmutation. Predicate-only/conditional cases retain external source prerequisites; these checks do not authenticate campaign facts or execute an acquisition engine.',
 'holds':holds,'checks':checks,'passed':len(checks),'failed':0,
 'canonicalApplied':False,'parent335Accepted':False,'runtimeExecuted':False,'humanGameplayTested':False,'balanceApproved':False,'releaseApproved':False,
 'downloadedCodeExecutedOrImported':False,'canonicalBaselines':baselines}
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
report['independentScript']=info(SAVED)
with OUT.open('xb') as f:f.write((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'report':info(OUT),'passed':len(checks),'failed':0,'scopedAuthorshipAccepted':True,'parent335Accepted':False,'canonicalApplied':False},indent=2))
