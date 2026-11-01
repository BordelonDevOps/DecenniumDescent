#!/usr/bin/env python3
"""Build a conditional R03 witness. Never edits rules, index, queue or old cases."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

REV = '49210876918b3f1c2a1cee3206896af0f435097b'
BASE = 'docs/audit/2026-10-08/full-game/director-spell-review-129/'
R333 = BASE + 'rank9_summon_avatar_of_decay_return333_received/payload/'
ROOT = Path(subprocess.check_output(['git','rev-parse','--show-toplevel'], text=True).strip())
OUT = ROOT / BASE / 'summon_avatar_of_decay_r03_mind_blank_witness_408'
SID = 'C:mind-blank:SH408'
bindings = []

def enc(x):
    return json.dumps(x, sort_keys=True, separators=(',',':'), ensure_ascii=False, allow_nan=False).encode()

def sha(x):
    return hashlib.sha256(x).hexdigest()

def write(name, x):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(json.dumps(x, indent=2, ensure_ascii=False, allow_nan=False).encode()+b'\n')

def source(name, path, pointers=(), text_locators=()):
    raw = subprocess.check_output(['git','show',REV+':'+path], cwd=ROOT)
    p = OUT/'sources'/name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(raw)
    bindings.append({'member':'sources/'+name,'repositoryPath':path,'commit':REV,
        'gitBlobSHA1':subprocess.check_output(['git','rev-parse',REV+':'+path], cwd=ROOT,text=True).strip(),
        'bytes':len(raw),'sha256':sha(raw),'jsonPointers':list(pointers),'textLocators':list(text_locators),
        'representation':'exact Git blob bytes; text line locators count normalized lines only'})
    return json.loads(raw) if name.endswith('.json') else raw.decode()

def escape(x): return str(x).replace('~','~0').replace('/','~1')

def changes(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        result=[]
        for k in sorted(set(a)|set(b)):
            q=path+'/'+escape(k)
            if k not in a: result.append(('add',q,None,b[k]))
            elif k not in b: result.append(('remove',q,a[k],None))
            else: result.extend(changes(a[k],b[k],q))
        return result
    return [] if a==b else [('replace',path,a,b)]

def locate(x,p):
    keys=[k.replace('~1','/').replace('~0','~') for k in p[1:].split('/')]
    for k in keys[:-1]: x=x[int(k)] if isinstance(x,list) else x[k]
    return x,int(keys[-1]) if isinstance(x,list) else keys[-1]

def patch_for(a,b):
    ops=[]
    for mode,p,old,new in changes(a,b):
        assert p
        if mode!='add': ops.append({'op':'test','path':p,'value':copy.deepcopy(old)})
        if mode=='remove': ops.append({'op':'remove','path':p})
        else: ops.append({'op':mode,'path':p,'value':copy.deepcopy(new)})
    return ops

def bounds(v):
    x,y,z=v['pos']; w,d,h=v['box']
    return [x-w/2,x+w/2,y-d/2,y+d/2,z,z+h]

def overlaps(a,b):
    return all(min(a[2*i+1],b[2*i+1])>max(a[2*i],b[2*i]) for i in range(3))

def ray_hits(a,b,box):
    lo,hi=0.0,1.0
    for i in range(3):
        d=b[i]-a[i]
        if not d:
            if not box[2*i]<a[i]<box[2*i+1]: return False
        else:
            t1=(box[2*i]-a[i])/d; t2=(box[2*i+1]-a[i])/d
            lo=max(lo,min(t1,t2));hi=min(hi,max(t1,t2))
    return max(lo,0)<min(hi,1)

def aura_checks(s, actor):
    av=bounds(s['bodies']['A:cast1:body1']); rows=[]
    recipients={actor:s['actors'][actor],**{k:v for k,v in s['bodies'].items() if v['sourceOwner']==actor}}
    for k,v in recipients.items():
        bb=bounds(v)
        gaps=[max(av[2*i]-bb[2*i+1],bb[2*i]-av[2*i+1],0) for i in range(3)]
        distance2=sum(g*g for g in gaps)
        assert distance2>100, (actor,k,distance2)
        rows.append({'recipient':k,'bodyBounds':bb,'distanceSquared':distance2,'insideAura':False,'newRoot':False})
    return rows

OUT.mkdir(parents=True,exist_ok=True)
queue=source('QUEUE404.json',BASE+'CURRENT_SPELL_QUEUE_404.json',['/currentAuthority','/continuingPriorityOrder'])
source('HANDOFF404.json',BASE+'CURRENT_HANDOFF_404.json')
source('RESIDUAL333.json',R333+'RESIDUAL_BRANCH_DISPOSITIONS.json',['/branches/2'])
proc=source('DECAY285.json',R333+'evidence/EXACT_RETURN285_PROCEDURE.json',
    ['/spellLocalProcedure/admission','/spellLocalProcedure/relationEnding','/commonProcedure/aura','/commonProcedure/clocks'])
source('FERRY333.json',R333+'FERRY_RECONCILIATION.json',['/authorizedExistingLocalCompletion','/ruling'])
profile=source('W17D.json',R333+'evidence/EXISTING_W17D_PROFILE.json',
    ['/ordinaryLearning/14/selected/2','/spellbook/38','/prepared/11','/characterFoundation/equipment','/sourceClassBinding'])
source('W17N.json',R333+'evidence/EXISTING_W17N_PROFILE.json',['/automaticCards','/alwaysPrepared'])
wizard=source('WIZARD.json','DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json',
    ['/cards/17','/engine/11','/engine/12','/engine/17'])
model=source('WARD149.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8ward5_reviewed_149/MODEL.json',
    ['/spells/3/procedure','/spells/3/nativeCardAndAccessUnchanged/classAccess/Wizard','/sharedRules/text'])
index=source('INDEX.json','DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json',['/entries/77'])
receipt=source('ACCEPTANCE149.json',index['entries'][77]['authoredAcceptanceReceipt']['path'])
source('COMBAT.md','DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
    text_locators=['lines27-52 regular turns/reactions/clocks','line115 stance timing','line121 Mobile'])
source('SPELL_INTEGRATION.md','DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md',
    text_locators=['lines31-57 casting commitment, strain and counters','line98 shared hard-denial guard'])
source('RULEBOOK.txt','docs/reference/Player_Rulebook_v6_source_text.txt',
    text_locators=['lines8424-8438 strain and idle-turn recovery','lines8605-8631 components'])
source('CONDITIONS.md','DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md',
    text_locators=['Silenced; Incapacitated; Restrained components predicates'])

archive=Path(sys.argv[1]).read_bytes()
assert sha(archive)=='66ca7f3bc84c96ded94055747841ce767ddd2100f40e289ad13ae3b2e9e5fc21'
member='cases/RANK9SUMMONHOSTS5129-SUMMON-AVATAR-OF-DECAY-A.json'
with zipfile.ZipFile(sys.argv[1]) as z:
    assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==107
    case_raw=z.read(member);case=json.loads(case_raw)
    profiles_raw=z.read('ACTOR_PROFILES.json')
    (OUT/'sources/PARENT_ACTOR_PROFILES.json').write_bytes(profiles_raw)
    assert json.loads(profiles_raw)['W17D']==profile
parent=case['events'][159]['after']
assert sha(enc(parent))==case['events'][159]['afterSHA256']=='a02d43f5ae32b1d4e7284368dc58d2fa518e1f537936d4a739796e279a420a47'
write('PARENT_408.json',parent)
history=[{k:copy.deepcopy(e[k]) for k in ['id','tick','kind','details','before','after','beforeSHA256','afterSHA256']}
         | {'originalIndex':i} for i,e in enumerate(case['events']) if 160<=i<=197]
write('HISTORICAL_CONTINUATION_408.json',history)
write('PARENT_BINDING_408.json',{'archivePath':BASE+'rank9_summonhosts5_return285_received/DD_Rank9_SummonHosts5_Director_Return285_HELD.zip',
    'archiveBytes':len(archive),'archiveSHA256':sha(archive),'member':member,'memberBytes':len(case_raw),
    'memberSHA256':sha(case_raw),'pointer':'/events/159/after','canonicalSHA256':sha(enc(parent)),
    'profileMember':'ACTOR_PROFILES.json','profileBytes':len(profiles_raw),'profileSHA256':sha(profiles_raw),
    'continuationPointers':['/events/'+str(i) for i in range(160,198)],
    'qualification':'Derived JSON extracts have separate byte hashes. Exact parent structure/hash and source-member bytes verified against the archived case. No historical claim is relabeled campaign execution.'})

state=copy.deepcopy(parent); states={'S000':copy.deepcopy(state)}; events=[]

def emit(label, kind, tick, mutate=lambda s:None, evidence=None, refs=()):
    global state
    before=copy.deepcopy(state);assert tick>=before['tick']
    state['tick']=tick;mutate(state)
    if 'witness408' in state:
        state['witness408'].setdefault('eventHistory',[]).append({'id':'SH408:'+str(len(events)+1),'kind':kind,'tick':tick})
    after=copy.deepcopy(state)
    i=len(events);sid='S'+str(i+1).zfill(3); states[sid]=after
    forward=patch_for(before,after);inverse=patch_for(after,before)
    events.append({'id':'SH408:'+str(i+1),'kind':kind,'label':label,'tick':tick,
        'beforeStateId':'S'+str(i).zfill(3),'afterStateId':sid,'beforeSHA256':sha(enc(before)),
        'afterSHA256':sha(enc(after)),'forward':forward,'inverse':inverse,
        'forwardAbsentPaths':[o['path'] for o in forward if o['op']=='add'],
        'inverseAbsentPaths':[o['path'] for o in inverse if o['op']=='add'],
        'evidence':evidence or {},'sourceRefs':list(refs)})

def bootstrap(s):
    s['witness408']={'classification':'CONDITIONAL_TEST_ONLY','campaignEvent':False,'runtimeExecution':False,
      'pendingCast':None,'willingness':None,'castThisTurn':{
        k:any(h['tick']>=v['lastRegularStart'] for h in v['resourceHistory']) for k,v in s['actors'].items()},
      'regular':{k:{'nextEnd':(v['lastRegularStart'] if v['turnActive'] else v['nextRegularStart'])+80,
        'startsConsumed':[],'endsConsumed':[],'stanceExpiry':v['nextRegularStart'],
        'movementRemaining':v['walk'] if v['turnActive'] else 0,'mobileAllowance':0}
        for k,v in s['actors'].items()},'phaseBudgets':{},'counterWindow':[],
      'initialAuraCheckpoint':aura_checks(s,'C'),'suppressionLedger':[], 'sourceTerminationLedger':[],
      'deadlineObservations':[],'resumptionChecks':[],
      'legacyStateQualification':'Initial bytes/qualifications unchanged. Historical Neutral labels outside newly processed turns grant no new stance benefit. New regular choices use Mobile; no legacy stance-dependent benefit is exercised.'}
emit('Bind conditional branch metadata; no budget refresh','branchBinding',200,bootstrap,
     {'parentRegularStartAlreadyProcessed':'C:200','noSecondStart':True})

def consent(s):
    s['witness408']['willingness']={'actor':'F','castId':SID,'decision':'affirmative','at':201,
      'scope':'receive this Mind Blank; not cooperation with Decay or disclosure of contract contents',
      'provenance':'NEW TEST_ONLY decision expressly within the requested conditional witness; no campaign fact',
      'communication':'brief ordinary Common speech, no extra Action'}
emit('Ferry freely accepts this proposed ward','testOnlyWillingness',201,consent,
     refs=['sources/WARD149.json#/sharedRules/text','sources/FERRY333.json#/authorizedExistingLocalCompletion/language'])

def mobile(s,a):
    s['actors'][a]['stance']='Mobile';r=s['witness408']['regular'][a]
    r['stanceExpiry']=s['actors'][a]['nextRegularStart'];r['mobileAllowance']=5
emit('C selects Mobile before its cast','stanceChoice',202,lambda s:mobile(s,'C'),
     {'Speed':30,'AC':12,'movementSpent':0,'freeMovementGranted':0},['sources/COMBAT.md@line115','sources/COMBAT.md@line121'])

def commit(s):
    a=s['actors']['C'];assert a['turnActive'] and a['actions']['Action']==1 and a['RP']==64
    assert a['concentration'] is None and a['dissonance']==0 and a['refrain']==0
    a['actions']['Action']=0;a['RP']=43;a['lastCast']='mind-blank';a['preparedSeen'].append('mind-blank')
    a['resourceHistory'].append({'sourceId':SID,'spell':'mind-blank','rank':8,'baseCost':21,'actualPaid':21,
       'preDissonance':0,'baseDissonance':0,'refrainAdded':0,'tick':210,'firstPreparedFamily':True})
    s['witness408']['castThisTurn']['C']=True
    s['witness408']['pendingCast']={'id':SID,'caster':'C','target':'F','rank':8,'school':'Abjuration',
       'commitTick':210,'cost':21,'ActionPaid':True,'concentrationRequired':False,'priorConcentration':None,
       'components':{'V':'ordinary available speech; Common','S':'right hand free','F':'focus-C held left'},
       'firstPreparedFamily':True,'baseDissonance':0,'Refrain':0,'status':'pending'}
emit('Commit Action, 21 RP and cast history before interruption','castCommit',210,commit,
  {'rangeMetric':'equal orthogonal/diagonal grid','rangeFeet':5,'euclideanFeet':50**0.5,'maximumRangeFeet':120,
   'knowledgeShield':'No trigger: Mind Blank grants immunity, not AC/tempHP/resistance/save bonus; no ally premise added.',
   'matrixModifications':{},'optionalFeaturesUsed':[]},
  ['sources/WARD149.json#/spells/3/procedure','sources/WARD149.json#/sharedRules/text','sources/WIZARD.json#/engine/11','sources/SPELL_INTEGRATION.md@lines33-38'])

def counters(s):
    rows=[]; target=[40,-5,5.5]
    for a in ['A','B','N1','N2']:
        v=s['actors'][a];eye=[v['pos'][0],v['pos'][1],5.5]
        blocked=[k for k,w in {**s['actors'],**s['bodies']}.items() if k not in (a,'C') and ray_hits(eye,target,bounds(w))]
        assert not blocked,(a,blocked)
        distance=max(abs(v['pos'][i]-s['actors']['C']['pos'][i]) for i in range(3))
        assert distance<=60 and v['actions']['Reaction']==1 and v['RP']>=3 and v['dissonance']<13
        assert v['equipment']['leftHand']=='focus-'+a and v['equipment']['rightHand'] is None and not v['conditions']
        rows.append({'actor':a,'source':'wizard.base.counterspell','sourcePointer':'sources/WIZARD.json#/cards/17',
          'acquisition':'automatic Wizard2; bound level17 profile','eligible':True,'gridDistanceFeet':distance,
          'perceptionAndLoE':{'from':eye,'to':target,'occludingBodies':blocked,'ordinaryBrightLight':True},
          'components':{'V':True,'S':'free right hand','F':'held focus-'+a},'ReactionAvailable':1,
          'RPAvailable':v['RP'],'costIfAttempted':3,'preDissonance':v['dissonance'],'dissonanceLimit':13,
          'recharge':v['recharge'].get('wizard.base.counterspell',0),
          'rechargeBasis':'No prior Counterspell commit in source prefix; counter set only on use, not on acquisition.',
          'decision':'TEST_ONLY_DECLINE','actualCost':0,'actualReactionSpent':0,'historyAdded':False,
          'counterCheckDCIfAttempted':26})
    rows.append({'actor':'C','decision':'TEST_ONLY_NO_ATTEMPT','eligibility':'UNADJUDICATED','selfCounterProhibitionAsserted':False,'actualCost':0})
    rows.append({'actor':'F','eligible':False,'reason':'Native Ferry source grants no Counterspell or spellcasting','actualCost':0})
    for k in s['bodies']:
        rows.append({'actor':k,'eligible':False,'reason':'Bound generated profile grants no Counterspell, independent Reaction or repertoire','actualCost':0})
    s['witness408']['counterWindow']=rows
emit('All actual responder decisions; no Counterspell attempted','counterWindow',211,counters,
     {'actualChecksRolled':0,'costsRetained':21},['sources/WIZARD.json#/cards/17','sources/SPELL_INTEGRATION.md@lines36-57'])

def establish(s):
    assert s['witness408']['willingness']['decision']=='affirmative'
    s['sources'][SID]={'id':SID,'spellId':'mind-blank','owner':'C','rank':8,'school':'Abjuration',
       'castTick':210,'formationTick':220,'expires':360220,'originalDeadline':360220,'concentration':False,
       'active':True,'status':'established','bodyIds':[],'recipients':['F'],'history':[]}
    s['actors']['F']['effects'].append({'id':SID,'kind':'MindBlankAbjuration','active':True,'willingAtCast':True,
       'sourceId':SID,'expires':360220})
    s['witness408']['pendingCast']['status']='resolved'
    s['relations']['relay:3']['suppression']={'sourceId':SID,'at':220,'mode':'Abjuration','component':'mentalSpellComponent'}
    s['witness408']['suppressionLedger'].append({'ward':SID,'relation':'relay:3','tick':220,
       'wardOperation':'SUPPRESS_NOT_CURE','sourceControllerPreserved':'A','originalControllerPreserved':'F',
       'originalOrderExpiry':510,'parentSourceExpiry':6020,'guardSpent':False})
emit('Mind Blank suppresses the existing covered expression; it does not cure or terminate its source','wardResolution',220,establish,
     {'wholeWardDurationTicks':360000,'noSaveRequired':True,'existingComponent':True,'freshAdmissionPreventionOnly':False},
     ['sources/WARD149.json#/spells/3/procedure','sources/DECAY285.json#/spellLocalProcedure/admission'])

def local_end(s):
    r=s['relations']['relay:3'];assert r['status']=='pending' and r['expires']==510
    r['status']='cancelled';r['endedAt']=220;r['endedReason']='DECAY_SOURCE_LOCAL_RIDER_SUPPRESSION'
    r['terminationSourcePointer']='sources/DECAY285.json#/spellLocalProcedure/relationEnding'
    s['actors']['F']['controller']=r['originalController']
    s['witness408']['sourceTerminationLedger'].append({'relation':'relay:3','tick':220,'terminalTransitions':1,
       'cause':'The selected Decay source independently cancels its single-order relay on rider suppression.',
       'notMindBlankCure':True,'originalExpiryRetained':510,'parentStillActive':True,'budgetKey':None,
       'noGuardSpend':True,'noActionRefundOrRefresh':True})
emit('Apply the relay source’s own termination rule, separately from the ward','sourceLocalTermination',220,local_end,
  {'ruleNotNew':'Rider-only suppression cancels only the affected relay; source ending while suppressed is terminal.',
   'separateLifecycles':True,'MindBlankDoesNotCure':True},
  ['sources/DECAY285.json#/spellLocalProcedure/relationEnding','sources/WARD149.json#/sharedRules/text'])

def apply_historical(s,e):
    for mode,p,old,new in changes(e['before'],e['after']):
        if p in ('/tick','/witnessLedger'):continue
        obj,key=locate(s,p)
        if p=='/phase' and e['kind']=='regularEnd':
            assert obj[key] in ('regular:'+e['details']['actorId'],'between')
            obj[key]=copy.deepcopy(new)
            continue
        if mode=='add': assert key not in obj;obj[key]=copy.deepcopy(new)
        else:
            assert obj[key]==old,(e['originalIndex'],p,obj[key],old)
            if mode=='remove':del obj[key]
            else:obj[key]=copy.deepcopy(new)
    kind=e['kind'];a=e['details'].get('actorId')
    if kind=='regularStart':
        r=s['witness408']['regular'][a];assert e['tick'] not in r['startsConsumed']
        r['startsConsumed'].append(e['tick']);r['nextEnd']=e['tick']+80
        r['mobileAllowance']=0;r['movementRemaining']=s['actors'][a]['walk'];r['stanceExpiry']=None
        s['actors'][a]['stance']=None;s['witness408']['castThisTurn'][a]=False
    if kind=='regularEnd':
        v=s['actors'][a];r=s['witness408']['regular'][a];assert r['nextEnd']==e['tick']
        r['endsConsumed'].append(e['tick']);r['nextEnd']=e['tick']+600;r['movementRemaining']=0
        v['actions']['Action']=0;v['actions']['BA']=0;v['actions']['objectInteraction']=0
        if not s['witness408']['castThisTurn'][a]:v['dissonance']=max(0,v['dissonance']-1)
    if kind=='forcedOpportunity':
        bid=e['details']['target'];r=s['witness408']['phaseBudgets']
        r[bid]={'originalPhase':e['tick'],'open':True,'Speed':s['bodies'][bid]['walk'],
          'movementSpent':0,'movementRemaining':s['bodies'][bid]['walk'],'ordinaryOffensiveOpportunityConsumed':True,
          'extraActionsGranted':0,'casterBudgetRefreshes':0}
    if kind=='bodyMovement':
        bid=e['details']['bodyId'];r=s['witness408']['phaseBudgets'][bid]
        r['movementSpent']+=e['details']['cost'];r['movementRemaining']-=e['details']['cost']
    if kind=='bodyOpportunityClose':
        bid=e['details']['bodyId'];r=s['witness408']['phaseBudgets'][bid];r['open']=False;r['movementRemaining']=0
    if kind=='uncommandedAttached':
        bid=e['details']['bodyId'];s['witness408']['phaseBudgets'][bid]={'originalPhase':e['tick'],
          'open':False,'Speed':s['bodies'][bid]['walk'],'movementSpent':0,'movementRemaining':0,
          'defensiveDefault':'Dodge','offenseUsed':False,'extraActionsGranted':0,'casterBudgetRefreshes':0}

for e in history:
    i=e['originalIndex']
    if i>=189:break
    evidence={'historicalIndex':i,'historicalEventId':e['id'],'sourceBeforeSHA256':e['beforeSHA256'],
      'sourceAfterSHA256':e['afterSHA256'],'historicalOperandsRetained':True}
    if e['kind']=='regularEnd':
        evidence['currentSourceSettlement']='Expire unused Action/BA/interaction/movement; preserve Reaction/stance until next start; apply idle-turn Dissonance recovery without resetting Refrain.'
    emit(e['kind']+' — preserved opportunity '+str(i),'continued_'+e['kind'],e['tick'],
         lambda s,e=e:apply_historical(s,e),evidence,
         ['HISTORICAL_CONTINUATION_408.json#/'+str(i-160),'sources/COMBAT.md@lines27-52','sources/RULEBOOK.txt@line8438'])
    if e['kind']=='regularStart':
        a=e['details']['actorId']
        emit('Check actual aura geometry at '+a+' regular start','auraCheckpoint',e['tick'],
            evidence={'actor':a,'checks':aura_checks(state,a),'newRoots':0},refs=['sources/DECAY285.json#/commonProcedure/aura'])
        emit(a+' selects Mobile before activity/end','stanceChoice',e['tick'],lambda s,a=a:mobile(s,a),
             {'freeMovementGranted':0},['sources/COMBAT.md@line115','sources/COMBAT.md@line121'])

def deadline(s):
    r=s['relations']['relay:3'];assert r['expires']==510 and r['status']=='cancelled'
    assert s['sources'][SID]['active']
    s['witness408']['deadlineObservations'].append({'relation':'relay:3','tick':510,'originalDeadline':510,
       'deadlineReachedWhileWardActive':True,'execution':False,'ActionSpent':0,'guardSpent':False,
       'sourceAlreadyTerminal':True,'secondTerminationPerformed':False,'potentialStillValidOrder':False})
emit('Original relay opportunity/deadline passes while Mind Blank remains active','originalOrderDeadline',510,deadline,
     {'excludedHistoricalEvents':list(range(189,196)),'reason':'No pending executable relay remains. No Ferry attack, root4, damage or second agency restoration is replayed.'},
     ['sources/DECAY285.json#/spellLocalProcedure/relationEnding','sources/WARD149.json#/spells/3/procedure'])

def ward_end(s):
    f=s['actors']['F'];assert f['turnActive'] and f['lastRegularStart']==500
    q=s['sources'][SID];q['active']=False;q['status']='ended';q['endedAt']=520;q['endedReason']='recipientWholeWardEnding'
    f['effects'][0]['active']=False;f['effects'][0]['endedAt']=520
    s['witness408']['resumptionChecks'].append({'tick':520,'wardEnded':True,'endingCosts':0,
       'originalOrderExpiry':510,'deadlineHasPassed':True,'relayStatus':s['relations']['relay:3']['status'],
       'parentStillActive':s['sources']['A:cast1']['active'],'parentDeadlineUnchanged':6020,
       'stillValidOrder':False,'resume':False,'newAdmission':False,'newAction':False,
       'qualification':'Ward suppression is not cure. A genuinely still-live covered component could resume only with a still-valid original order. This order is terminal under its own source and past its original deadline.'})
emit('Ferry ends its whole ward in its own actual turn, after original order expiry','recipientWardEnding',520,ward_end,
     {'TEST_ONLYDecision':True,'originalWardDeadlineRetained':360220,'perComponentWaiver':False},
     ['sources/WARD149.json#/sharedRules/text','sources/WARD149.json#/spells/3/procedure'])
emit('Observe no stale-order revival; Ferry voluntarily takes no offensive action','noRevivalObservation',521,
     evidence={'relation':'relay:3','status':state['relations']['relay:3']['status'],'ordinaryActionStillAvailable':1,
       'noCompelledIdle':True,'noNewCastOrCommand':True,'newDamageRoots':0})
for e in history:
    if e['originalIndex']>=196:
        emit(e['kind']+' — actual Ferry end','continued_'+e['kind'],e['tick'],lambda s,e=e:apply_historical(s,e),
          {'historicalIndex':e['originalIndex'],'onlyDueRegularEnd':True},
          ['HISTORICAL_CONTINUATION_408.json#/'+str(e['originalIndex']-160),'sources/RULEBOOK.txt@line8438'])

write('AUTHORIZATION_AND_SCOPE_408.json',{
 'baseCommit':REV,'queueAuthority':queue['currentAuthority'],'scope':'SH333-R03 only; conditional TEST_ONLY; no campaign history',
 'userInstruction':'Build a source-bound, explicitly conditional TEST_ONLY witness for the existing relay using the accepted Mind Blank procedure, W17D acquired/prepared profile, and preserved Return285 case; bind willingness, payment, components, budget, concentration, interruption, suppression and no stale revival; exact inverse restoration; no rules/canon/queue/identity change.',
 'userCorrection':'Mind Blank suppresses, not cures. Prove the original order expires before ward end or allow a still-valid order to resume. Keep R03 open unless no stale revival is proved.',
 'newConditionalChoices':['F agrees to this specific ward at tick201','C selects Mobile and casts at210','A/B/N1/N2 decline their eligible counters; C makes no self-counter attempt','newly processed regular actors choose Mobile','F ends its entire ward at520 and otherwise idles'],
 'newRulesAdopted':[],'newActorsObjectsPlanesOrAcquisitions':[],'separateOwnerAuthorizationNeeded':False,
 'lifecycleDistinction':{'ward':'Suppresses a covered expression; cannot cure it.','relay':'The already-bound Decay relationEnding rule independently terminates its order on rider suppression. History/expiry retained.','proof':'The original510 deadline also passes while ward remains active; ward ends520. No banked command is eligible even apart from the source-local termination.'},
 'preservedQualifications':['Inherited Return285 held creation/source qualifications not re-adjudicated or promoted.','No historical event is attributed to the user or to a campaign.','R01/R02/R04 and all unrelated seals/holds unchanged.']})
write('SOURCE_BINDINGS_408.json',{'baseCommit':REV,'bindings':bindings})
write('SNAPSHOTS_408.json',{'encoding':'SHA-256 of UTF-8 JSON sort_keys=true,separators=(comma,colon),ensure_ascii=false; no NaN','states':states})
write('EVENTS_408.json',{'id':'SH333-R03-MIND-BLANK-408','scope':'CONDITIONAL_TEST_ONLY','tickUnitSeconds':0.01,
   'sameTickOrder':'array order; immediate ward suppression and source-specific response share220; regular start precedes same-tick aura checkpoint and stance selection',
   'initialStateId':'S000','terminalStateId':'S'+str(len(events)).zfill(3),'events':events,
   'newRulesAdopted':False,'campaignEvent':False,'runtimeExecution':False,'acceptedIds':[],'appliedIds':[],
   'applicationAuthorized':False,'queueChanged':False,'R02R04Changed':False})
write('EXPECTED_TERMINAL_COMPARISONS_408.json',{'historicalIndex':197,
 'expectedUnchangedBodies':case['events'][197]['after']['bodies'],
 'expectedOtherRelations':{k:case['events'][197]['after']['relations'][k] for k in ['relay:1','relay:2']},
 'expectedOwnerRoundBudgets':case['events'][197]['after']['ownerRoundBudgets'],
 'expectedObjects':parent['objects'],'expectedOriginalSources':parent['sources'],
 'expectedSpentGuards':{k:v for k,v in case['events'][197]['after']['hardGuards'].items() if k!='A:F:encounter'},
 'expectedBHP':85,'expectedFHP':9,'expectedCHP':104,'expectedCRP':43,
 'expectedDifferences':'C paid ward/new cast history; Ferry relay suppressed then source-terminated and expired before ward ending, hence no old Ferry attack/root4/C damage. Normal current turn-end recovery/allowance expiry recorded explicitly.'})
print(json.dumps({'output':str(OUT),'events':len(events),'snapshots':len(states),'sourceBindings':len(bindings),
 'initialCanonicalSHA256':sha(enc(parent)),'terminalCanonicalSHA256':sha(enc(state)),
 'buildStatus':'BUILT_PENDING_SEPARATE_VERIFICATION'},indent=2))
