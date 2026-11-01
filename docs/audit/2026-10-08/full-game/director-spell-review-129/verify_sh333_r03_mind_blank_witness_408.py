#!/usr/bin/env python3
"""Independent data replay and bounded R03 semantic assertions; no builder import."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

root=Path(sys.argv[1]);checks=[]
def load(n): return json.loads((root/n).read_bytes())
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def digest(x): return hashlib.sha256(x).hexdigest()
def check(n,p):
    checks.append({'id':n,'pass':bool(p)})
    if not p: raise AssertionError(n)
def get(x,p):
    for k in p[1:].split('/') if p else []:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
def apply(s,ops,absent):
    for p in absent:
        try:get(s,p)
        except (KeyError,IndexError):pass
        else:raise AssertionError('add path already exists: '+p)
    for op in ops:
        check('scoped-patch',bool(op['path']))
        parts=op['path'].split('/');parent=get(s,'/'.join(parts[:-1]));k=parts[-1].replace('~1','/').replace('~0','~')
        k=int(k) if isinstance(parent,list) else k
        if op['op']=='test':check('patch-precondition',parent[k]==op['value'])
        elif op['op']=='add':check('patch-add-absent',k not in parent);parent[k]=copy.deepcopy(op['value'])
        elif op['op']=='replace':parent[k]=copy.deepcopy(op['value'])
        elif op['op']=='remove':del parent[k]
        else:raise AssertionError(op['op'])
    return s

bindings=load('SOURCE_BINDINGS_408.json');revision=bindings['baseCommit']
repo=subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()
for row in bindings['bindings']:
    raw=(root/row['member']).read_bytes()
    check('source-size-'+row['member'],len(raw)==row['bytes'])
    check('source-hash-'+row['member'],digest(raw)==row['sha256'])
    current=subprocess.check_output(['git','show',revision+':'+row['repositoryPath']],cwd=repo)
    check('source-git-byte-parity-'+row['member'],raw==current)
    for p in row['jsonPointers']:get(json.loads(raw),p)

statefile=load('SNAPSHOTS_408.json');states=statefile['states'];data=load('EVENTS_408.json');events=data['events']
parent=load('PARENT_408.json');bind=load('PARENT_BINDING_408.json');expected=load('EXPECTED_TERMINAL_COMPARISONS_408.json')
check('initial-parent-exact',states['S000']==parent)
check('parent-canonical-hash',digest(canonical(parent))==bind['canonicalSHA256'])
profiles_raw=(root/'sources/PARENT_ACTOR_PROFILES.json').read_bytes()
check('parent-profile-hash',digest(profiles_raw)==bind['profileSHA256'])
profiles=json.loads(profiles_raw);profile=load('sources/W17D.json')
check('exact-W17D-extraction',profiles['W17D']==profile)
check('mind-blank-acquired-prepared',profile['ordinaryLearning'][14]['selected'][2]==profile['prepared'][11]==profile['spellbook'][38]=='mind-blank')
ward=load('sources/WARD149.json');idx=load('sources/INDEX.json');receipt=load('sources/ACCEPTANCE149.json')
check('accepted-Mind-Blank','mind-blank' in receipt['directorDecision']['acceptedIds'])
check('accepted-procedure-binding',digest((root/'sources/WARD149.json').read_bytes())==idx['entries'][77]['completeEnvelopeBinding']['sha256'])
check('accepted-school',ward['spells'][3]['nativeCardAndAccessUnchanged']['classAccess']['Wizard']['school']=='Abjuration')
check('suppression-not-cure','suppressed, not cured' in ward['spells'][3]['procedure'])
check('source-local-ending-distinct','Rider-only suppression cancels only the affected relay' in load('sources/DECAY285.json')['spellLocalProcedure']['relationEnding'])
check('whole-ward-end-permission','during its actual regular turn' in ward['sharedRules']['text'])

history=load('HISTORICAL_CONTINUATION_408.json')
for e in history:
    check('historical-before-hash',digest(canonical(e['before']))==e['beforeSHA256'])
    check('historical-after-hash',digest(canonical(e['after']))==e['afterSHA256'])
for i in range(len(history)-1):check('historical-continuity',history[i]['after']==history[i+1]['before'])
check('historical-fork-continuity',history[0]['before']==parent)
archive_checked=False
if len(sys.argv)>2:
    archive_raw=Path(sys.argv[2]).read_bytes()
    check('original-archive-bytes',len(archive_raw)==bind['archiveBytes'])
    check('original-archive-hash',digest(archive_raw)==bind['archiveSHA256'])
    with zipfile.ZipFile(sys.argv[2]) as z:
        check('original-archive-crcs',z.testzip() is None)
        raw=z.read(bind['member']);check('original-member-hash',digest(raw)==bind['memberSHA256'])
        original=json.loads(raw)
        check('original-fork-pointer',original['events'][159]['after']==parent)
        check('original-profile-bytes',z.read('ACTOR_PROFILES.json')==profiles_raw)
        for e in history:
            old=original['events'][e['originalIndex']]
            check('original-continuation-exact',all(old[k]==v for k,v in e.items() if k!='originalIndex'))
    archive_checked=True

def box(v):
    x,y,z=v['pos'];w,d,h=v['box'];return ((x-w/2,x+w/2),(y-d/2,y+d/2),(z,z+h))
def intersects(a,b):return all(min(u[1],v[1])>max(u[0],v[0]) for u,v in zip(a,b))
def ray_blocked(a,b,bb):
    low,high=0.,1.
    for axis,(left,right) in enumerate(bb):
        delta=b[axis]-a[axis]
        if delta==0:
            if a[axis]<=left or a[axis]>=right:return False
        else:
            ends=sorted(((left-a[axis])/delta,(right-a[axis])/delta))
            low=max(low,ends[0]);high=min(high,ends[1])
    return low<high

cur=copy.deepcopy(parent);previous=200
for e in events:
    check('time-monotone',e['tick']>=previous);previous=e['tick']
    check('forward-before-snapshot',cur==states[e['beforeStateId']])
    check('forward-before-hash',digest(canonical(cur))==e['beforeSHA256'])
    cur=apply(cur,e['forward'],e['forwardAbsentPaths'])
    check('forward-after-hash',digest(canonical(cur))==e['afterSHA256'])
    check('forward-after-snapshot',cur==states[e['afterStateId']])
    check('one-regular-turn-at-most',sum(bool(a['turnActive']) for a in cur['actors'].values())<=1)
    check('avatar-parent-source-preserved',cur['sources']['A:cast1']==parent['sources']['A:cast1'])
    check('all-real-property-preserved',cur['objects']==parent['objects'])
    check('Ferry-physical-body-preserved',all(cur['actors']['F'][k]==parent['actors']['F'][k] for k in ['pos','box','HP','maxHP','equipment','massLb','type','sourceOwner','plane']))
    check('no-new-summon-body',set(cur['bodies'])==set(parent['bodies']))
    check('source-qualifications-preserved',cur['qualifications']==parent['qualifications'])
    check('hold-list-preserved',cur['holds']==parent['holds'])
    check('historical-prefix-not-rewritten',cur['witnessLedger']==parent['witnessLedger'])
terminal=copy.deepcopy(cur)
for e in reversed(events):
    check('inverse-start',cur==states[e['afterStateId']])
    cur=apply(cur,e['inverse'],e['inverseAbsentPaths'])
    check('inverse-hash',digest(canonical(cur))==e['beforeSHA256'])
    check('inverse-snapshot',cur==states[e['beforeStateId']])
check('full-exact-restoration',cur==parent)

bykind={e['kind']:e for e in events if e['kind'] in ['castCommit','counterWindow','wardResolution','sourceLocalTermination','originalOrderDeadline','recipientWardEnding']}
def before(kind):return states[bykind[kind]['beforeStateId']]
def after(kind):return states[bykind[kind]['afterStateId']]
commit=after('castCommit');counter_before=before('counterWindow');counter=after('counterWindow');est=after('wardResolution');local=after('sourceLocalTermination');deadline=after('originalOrderDeadline');ended=after('recipientWardEnding')
check('cast-order',[bykind[k]['tick'] for k in ['castCommit','counterWindow','wardResolution','sourceLocalTermination','originalOrderDeadline','recipientWardEnding']]==[210,211,220,220,510,520])
check('lawful-current-caster',before('castCommit')['actors']['C']['turnActive'] and before('castCommit')['actors']['C']['actions']['Action']==1)
check('paid-64-to43',before('castCommit')['actors']['C']['RP']==64 and commit['actors']['C']['RP']==43)
check('Action-paid',commit['actors']['C']['actions']['Action']==0)
check('cast-family-strain',commit['actors']['C']['preparedSeen']==['mind-blank'] and commit['actors']['C']['dissonance']==0 and commit['actors']['C']['refrain']==0)
check('no-concentration-displacement',commit['actors']['C']['concentration'] is None and commit['actors']['A']['concentration']==parent['actors']['A']['concentration'])
check('components-source-bound',commit['actors']['C']['equipment']['leftHand']=='focus-C' and commit['actors']['C']['equipment']['rightHand'] is None and not commit['actors']['C']['conditions'])
check('consent-precedes-payment',commit['witness408']['willingness']['at']==201 and commit['witness408']['willingness']['decision']=='affirmative')
for a in ['A','B','C','N1','N2','F']:check('counter-declines-no-actor-change-'+a,counter_before['actors'][a]==counter['actors'][a])
rows={r['actor']:r for r in counter['witness408']['counterWindow']}
check('four-eligible-explicit-declines',all(rows[a]['eligible'] and rows[a]['decision']=='TEST_ONLY_DECLINE' and rows[a]['actualCost']==0 and rows[a]['actualReactionSpent']==0 for a in ['A','B','N1','N2']))
check('self-not-prohibited',rows['C']['eligibility']=='UNADJUDICATED' and not rows['C']['selfCounterProhibitionAsserted'])
for a in ['A','B','N1','N2']:
    row=rows[a];actor=counter['actors'][a];p=profiles[actor['profileId']]
    check('counter-automatic-access-'+a,'wizard.base.counterspell' in p['alwaysPrepared'] and p['classLevel']==17)
    check('counter-resource-binding-'+a,row['RPAvailable']==actor['RP'] and row['preDissonance']==actor['dissonance'] and row['recharge']==actor['recharge'].get('wizard.base.counterspell',0)==0)
    check('counter-actual-grid-range-'+a,max(abs(x-y) for x,y in zip(actor['pos'],counter['actors']['C']['pos']))==row['gridDistanceFeet']<=60)
    ray=row['perceptionAndLoE']
    check('counter-ray-endpoints-'+a,all(lo<=v<=hi for v,(lo,hi) in zip(ray['from'],box(actor))) and all(lo<=v<=hi for v,(lo,hi) in zip(ray['to'],box(counter['actors']['C']))))
    for k,v in {**counter['actors'],**counter['bodies']}.items():
        if k not in (a,'C'):check('counter-line-clear-'+a+'-'+k,not ray_blocked(ray['from'],ray['to'],box(v)))
check('ward-grid-range',max(abs(x-y) for x,y in zip(commit['actors']['C']['pos'],commit['actors']['F']['pos']))==5)
for k,v in {**commit['actors'],**commit['bodies']}.items():
    if k not in ('C','F'):check('ward-line-clear-'+k,not ray_blocked([40,-5,5.5],[45,0,5.5],box(v)))
for e in events:
    st=states[e['afterStateId']]
    for k,v in {**st['actors'],**st['bodies']}.items():
        bb=box(v);check('bounded-supported-'+k,bb[2][0]==0 and bb[2][1]<=100 and bb[0][0]>=-500 and bb[0][1]<=500 and bb[1][0]>=-500 and bb[1][1]<=500)
    if e['kind']=='auraCheckpoint':
        for r in e['evidence']['checks']:
            v=({**st['actors'],**st['bodies']})[r['recipient']]
            d=sum(max(u[0]-w[1],w[0]-u[1],0)**2 for u,w in zip(box(v),box(st['bodies']['A:cast1:body1'])))
            check('aura-distance-recomputed',d==r['distanceSquared'] and d>100)
    if e['kind']=='continued_bodyMovement':
        old=next(h for h in history if h['originalIndex']==e['evidence']['historicalIndex'])
        path=old['details']['route'];mover=old['details']['bodyId'];before_move=states[e['beforeStateId']]
        check('paid-route-length',sum(max(abs(a-b) for a,b in zip(path[i],path[i+1])) for i in range(len(path)-1))==15)
        for a,b in zip(path,path[1:]):
            va=copy.deepcopy(before_move['bodies'][mover]);vb=copy.deepcopy(va);va['pos']=a;vb['pos']=b
            hull=tuple((min(x[0],y[0]),max(x[1],y[1])) for x,y in zip(box(va),box(vb)))
            for k,v in {**before_move['actors'],**before_move['bodies']}.items():
                if k!=mover:check('swept-body-clear-'+k,not intersects(hull,box(v)))
check('ward-alone-does-not-cancel',est['relations']['relay:3']['status']=='pending' and est['relations']['relay:3']['suppression']['sourceId']=='C:mind-blank:SH408')
check('only-local-source-terminates',local['relations']['relay:3']['status']=='cancelled' and local['relations']['relay:3']['endedReason']=='DECAY_SOURCE_LOCAL_RIDER_SUPPRESSION')
for name in ['relations','hardGuards','ownerRoundBudgets','bodies']:
    a=copy.deepcopy(before('wardResolution')[name]);b=copy.deepcopy(local[name])
    if name=='relations':a.pop('relay:3');b.pop('relay:3')
    check('resolution-other-'+name+'-unchanged',a==b)
check('original-expiry-not-rewritten',all(s['relations']['relay:3']['expires']==510 for s in states.values()))
check('ward-original-hour-clock',est['sources']['C:mind-blank:SH408']['expires']-est['sources']['C:mind-blank:SH408']['formationTick']==360000)
check('deadline-before-ward-end',deadline['tick']==510 and deadline['sources']['C:mind-blank:SH408']['active'] and ended['tick']==520)
check('no-double-terminal',deadline['witness408']['deadlineObservations'][0]['secondTerminationPerformed'] is False)
check('ward-ending-on-F-turn',ended['actors']['F']['turnActive'] and ended['actors']['F']['lastRegularStart']==500)
check('ward-ending-no-Action',before('recipientWardEnding')['actors']['F']['actions']==ended['actors']['F']['actions'])
check('no-stale-resumption',ended['witness408']['resumptionChecks'][0]['stillValidOrder'] is False and ended['witness408']['resumptionChecks'][0]['resume'] is False)
check('no-spent-Ferry-guard','A:F:encounter' not in terminal['hardGuards'])
check('other-spent-guards-retained',terminal['hardGuards']==expected['expectedSpentGuards'])
check('no-Ferry-root4','root:4' not in terminal['rootLedger'])
check('all-other-body-terminal-states',terminal['bodies']==expected['expectedUnchangedBodies'])
check('other-relay-terminal-states',{k:terminal['relations'][k] for k in ['relay:1','relay:2']}==expected['expectedOtherRelations'])
check('owner-command-budgets',terminal['ownerRoundBudgets']==expected['expectedOwnerRoundBudgets'])
check('other-damage-settlement',terminal['actors']['B']['HP']==85 and terminal['actors']['C']['HP']==104 and terminal['actors']['F']['HP']==9)
check('no-RP-refund',terminal['actors']['C']['RP']==43)
for a,start,end in [('C',200,280),('N1',300,380),('N2',400,480),('F',500,580)]:
    rr=terminal['witness408']['regular'][a]
    check('one-start-'+a,rr['startsConsumed']==([] if a=='C' else [start]))
    check('one-end-'+a,rr['endsConsumed']==[end] and rr['nextEnd']==end+600)
    check('expire-regular-wallet-'+a,all(terminal['actors'][a]['actions'][k]==0 for k in ['Action','BA','objectInteraction']) and rr['movementRemaining']==0)
    check('reaction-not-expired-'+a,terminal['actors'][a]['actions']['Reaction']==1)
check('idle-turn-strain-recovery',terminal['actors']['N1']['dissonance']==terminal['actors']['N2']['dissonance']==1)
check('idle-turn-Refrain-retained',terminal['actors']['N1']['refrain']==terminal['actors']['N2']['refrain']==1)
check('all-companion-phases-closed',all(not p['open'] and p['movementRemaining']==0 for p in terminal['witness408']['phaseBudgets'].values()))
check('movement-still-paid',terminal['witness408']['phaseBudgets']['N2:cast1:minion']['movementSpent']==15)
check('queue-counts-unchanged',load('sources/QUEUE404.json')['currentAuthority']=={'reviewedApplied':829,'pending':19,'acceptedUnapplied':0,'completeStandaloneProcedures':553,'scopedInterfaces':173})
check('no-identity-acceptance',data['acceptedIds']==data['appliedIds']==[] and not data['applicationAuthorized'] and not data['queueChanged'])

result={'id':'SH408-SEPARATE-REPLAY-SEMANTIC-VERIFIER','status':'PASS','baseCommit':revision,
 'sourceBindings':len(bindings['bindings']),'forwardEvents':len(events),'inverseEvents':len(events),'snapshots':len(states),
 'assertionsPassed':len(checks),'failures':0,'exactParentRestoration':True,'newRulesAdopted':False,
 'parentArchiveIndependentlyChecked':archive_checked,
 'lifecycleFinding':'Ward suppresses, does not cure. Decay source independently terminates its relay; original510 deadline passes while ward active; ward ends520; no still-valid order resumes.',
 'scope':'R03 bounded conditional data witness only; no whole-identity, campaign, runtime, canon or queue approval.',
 'checks':checks}
(root/'VERIFICATION_408.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
