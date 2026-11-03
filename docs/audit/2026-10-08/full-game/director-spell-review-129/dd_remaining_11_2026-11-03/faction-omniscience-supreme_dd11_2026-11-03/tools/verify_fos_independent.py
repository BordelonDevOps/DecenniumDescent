#!/usr/bin/env python3
"""Independent static verification for the DD11 Faction Omniscience witness.

This script reads the serialized packet and exact source objects; it does not import
or call the witness builder. It verifies branch semantics and executes every stated
forward/inverse JSON operation against snapshots.
"""
from pathlib import Path
import hashlib, json, math, subprocess, unicodedata, sys

REPO=Path(r'C:\ep480fix')
PKG=Path(r'C:\Users\cbord\AppData\Local\Temp\DD_Remaining_11_20261103')
BASE='3b4e4be0388a56db26ece31bfcba01da01a80139'
P=Path(__file__).resolve().parents[1]
W=json.loads((P/'WITNESS_PACKET.json').read_text(encoding='utf-8'))
A=json.loads((P/'ACTOR_PROFILES.json').read_text(encoding='utf-8'))
SB=json.loads((P/'SOURCE_BINDINGS.json').read_text(encoding='utf-8'))
C=json.loads((P/'DIRECTOR_CONTRACT.json').read_text(encoding='utf-8'))
checks=[]
def ck(name,ok,detail=None):
    checks.append({'check':name,'pass':bool(ok),'detail':detail})
    if not ok: raise AssertionError((name,detail))
def norm(x):
    if isinstance(x,str):return unicodedata.normalize('NFC',x)
    if isinstance(x,list):return [norm(i) for i in x]
    if isinstance(x,dict):return {norm(k):norm(v) for k,v in x.items()}
    return x
def canon(x):return json.dumps(norm(x),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def h(x):return hashlib.sha256(canon(x)).hexdigest()
def resolve(parent,path):
    q=parent
    parts=[i.replace('~1','/').replace('~0','~') for i in path.split('/')[1:]]
    for k in parts[:-1]:q=q[int(k)] if isinstance(q,list) else q[k]
    return q,parts[-1] if parts else None
def apply(s,ops):
    import copy
    z=copy.deepcopy(s)
    for o in ops:
        q,k=resolve(z,o['path'])
        if k is None:
            assert z==o.get('before');z=copy.deepcopy(o.get('after'));continue
        if isinstance(q,list):
            i=int(k);exists=i<len(q)
            assert exists==o['beforeExists'],o['path']
            if exists:assert q[i]==o['before'],o['path']
            if o['afterExists']:
                if exists:q[i]=copy.deepcopy(o['after'])
                else:q.insert(i,copy.deepcopy(o['after']))
            elif exists:q.pop(i)
        else:
            exists=k in q;assert exists==o['beforeExists'],o['path']
            if exists:assert q[k]==o['before'],o['path']
            if o['afterExists']:q[k]=copy.deepcopy(o['after'])
            elif exists:del q[k]
    return z
branches=W['branches']; ids=[b['branchId'] for b in branches]
ck('contract hash',W['contractSha256']==hashlib.sha256((PKG/'contracts/faction-omniscience-supreme.json').read_bytes()).hexdigest(),W['contractSha256'])
ck('scope only',W['scope']=='STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY' and all(not b['fixtureScope']['canonical'] and not b['fixtureScope']['campaignExistenceVerified'] and not b['fixtureScope']['runtimeExecution'] for b in branches))
ck('exact branch set',len(branches)==11 and len(set(ids))==11,ids)
counts={case:sum(b['caseId']==case for b in branches) for case in ('FOS-P1','FOS-P2','FOS-A1','FOS-A2')}
ck('all required cases and coverage counts',counts=={'FOS-P1':3,'FOS-P2':3,'FOS-A1':4,'FOS-A2':1},counts)
for route,case in [('Wizard/Divination','FOS-P1'),('Cleric/Divination','FOS-P2')]:
    route_br=[b for b in branches if b['route']==route and b['caseId']==case]
    ck('two paid useful native-route encounters:'+route,len(route_br)>=2 and len({b['encounterId'] for b in route_br})>=2)

# Exact Git blob provenance, source profiles, and candidate acquisition.
for binding in SB['baseDirectorContractSources']:
    raw=subprocess.check_output(['git','-C',str(REPO),'show',f"{binding['commit']}:{binding['repositoryPath']}"])
    ck('historical source exact:'+binding['repositoryPath'],len(raw)==binding['bytes'] and hashlib.sha256(raw).hexdigest()==binding['sha256'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==binding['gitBlobSha1'])
for binding in SB['currentSources']:
    raw=subprocess.check_output(['git','-C',str(REPO),'show',f"{binding['commit']}:{binding['path']}"])
    ck('current source exact:'+binding['path'],len(raw)==binding['bytes'] and hashlib.sha256(raw).hexdigest()==binding['sha256'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==binding['gitBlobSha1'] and bool(binding.get('pointers')))
for cl in ('wizard','cleric'):
    d=json.loads(subprocess.check_output(['git','-C',str(REPO),'show',f'{BASE}:DescentReviewChanges/ReviewBible/data/public/class_playtests/{cl}.json']))
    actor=next(x for x in A['actors'] if x['className'].lower()==cl)
    p=actor['classSpellProfile']
    ck('class RP/rank source:'+cl,actor['maxRP']==d['rpByClassLevel'][16] and actor['classRankMaximum']==d['maxSpellRankByClassLevel'][16]==9)
    ck('level-17 source spell access:'+cl,actor['singleClassLevel']==17 and actor['targetSpell']['firstLegalAcquisitionLevel']==17 and actor['rank9SpellAccess'])
    ck('ability/HP/PB construction:'+cl,actor['abilityScores']['CON']==19 and actor['proficiencyBonus']==6 and actor['hp']['currentHP']==actor['hp']['maximumHP'] and actor['armorClass']==12)
ck('Wizard Counterspell response disclosure',next(x for x in A['actors'] if x['className']=='Wizard')['classSpellProfile']['counterspellPrepared'])

# Every branch is independently replayed from serialized pre/post snapshots.
replay_events=0;replay_ops=0
for b in branches:
    ck('branch fixture:'+b['branchId'],b['fixtureScope']['classification']=='NEW_DIRECTOR_AUTHORED_TEST_ONLY' and b['initialState']['audit']['nativeCatalogMutated'] is False and b['initialState']['audit']['campaignFactsAsserted'] is False and b['initialState']['audit']['canonChanged'] is False)
    st=b['initialState'];ck('initial snapshot hash:'+b['branchId'],h(st)==b['initialStateSHA256'])
    if b['events']:ck('initial event linkage:'+b['branchId'],b['events'][0]['beforeState']==st)
    last_t=-1;ordinal_by_time={};previous=st;turn_starts={};turn_ends={}
    for e in b['events']:
        replay_events+=1;replay_ops+=len(e['forward'])+len(e['inverse'])
        t=e['elapsedMs'];ordinal_by_time[t]=ordinal_by_time.get(t,0)+1
        ck('chronology '+b['branchId']+'/'+e['id'],t>=last_t and e['sameTimeOrdinal']==ordinal_by_time[t]);last_t=t
        ck('state chain '+b['branchId']+'/'+e['id'],e['beforeState']==previous and h(e['beforeState'])==e['beforeStateSHA256'] and h(e['afterState'])==e['afterStateSHA256'])
        ck('forward replay '+b['branchId']+'/'+e['id'],apply(e['beforeState'],e['forward'])==e['afterState'])
        ck('inverse replay '+b['branchId']+'/'+e['id'],apply(e['afterState'],e['inverse'])==e['beforeState'])
        if e['eventType']=='REGULAR_TURN_START':turn_starts[e['details'].get('turnId',e['id'])]=1
        if e['eventType']=='REGULAR_TURN_END':turn_ends[e['id'].removesuffix('-END')]=1
        previous=e['afterState']
    ck('terminal hash and linkage:'+b['branchId'],previous==b['terminalState'] and h(b['terminalState'])==b['terminalStateSHA256'])
    ck('turns close exactly:'+b['branchId'],b['terminalState']['world']['activeTurn'] is None and len([e for e in b['events'] if e['eventType']=='REGULAR_TURN_START'])==len([e for e in b['events'] if e['eventType']=='REGULAR_TURN_END']))
    # Floor, bodies, carrying and range are read from the full starting state.
    st=b['initialState'];floor=st['world']['floor'];actors=list(st['actors'].values())
    bodies=[a['body'] for a in actors if a.get('body')]
    ck('body support:'+b['branchId'],all(body['supportedBy']==floor['id'] and body['bounds'][2][0]==0 for body in bodies) and floor['supportedLoadLb']<=floor['capacityLb'])
    for i,x in enumerate(bodies):
        for y in bodies[i+1:]:
            overlap=all(min(x['bounds'][k][1],y['bounds'][k][1])-max(x['bounds'][k][0],y['bounds'][k][0])>0 for k in range(3))
            ck('nonoverlapping bodies:'+b['branchId'],not overlap)
    caster=st['actors']['caster'];prof=caster['profile'];focus=prof['components']['focusItemId']
    ck('held focus and free hand:'+b['branchId'],prof['components']['V'] and prof['components']['S'] and prof['components']['F'] and prof['components']['focusHand']=='left' and prof['components']['rightHandFree'] and any(i['id']==focus and i['owner']=='caster' and i['custodian']=='caster' for i in caster['inventory']['items']))
    ck('reachable fixture actors:'+b['branchId'],all(a['location']['plane']=='TEST-PLANE-A' for a in actors))
    # Every spell commitment is paid and obeys the bound RP/Dissonance rules.
    for e in [x for x in b['events'] if x['eventType']=='SPELL_COMMIT']:
        before=e['beforeState']['actors']['caster'];after=e['afterState']['actors']['caster'];det=e['details'];spell=before['lastSpell']
        D=before['resources']['Dissonance'];limit=before['resources']['dissonanceLimit']
        surcharge=0 if D<limit else (1 if D<limit+3 else (2 if D<limit+6 else 3))
        repeat=before['refrainCount'] if before['lastSpell']==e['sourceID'] else 0
        discount=0;win=before.get('spellEfficiencyWindow')
        if win and win.get('status')=='AVAILABLE' and win.get('family')=='Divination' and before['world']['regularTurnNumber']<=win.get('expiresAfterTurn',-1):discount=win['discountRP']
        expected=26+surcharge-discount
        ck('paid RP and strain '+e['id'],det['finalRPCost']==expected and after['resources']['RP']==before['resources']['RP']-expected and after['resources']['Dissonance']==D+2+repeat and det['refrainAdded']==repeat and after['actionBudget']['actionsSpent']==before['actionBudget']['actionsSpent']+1 and after['magicThisTurn'] is True,{'cost':det['finalRPCost'],'expected':expected,'preD':D,'refrain':repeat})
        ck('spell commitment provenance '+e['id'],e['sourceID']=='faction-omniscience-supreme' and det['baseRPCost']==26 and det['V'] and det['S'] and det['F'])
        afterStart=e['beforeState']['actors']['caster']
        ck('rank/preparation/range '+e['id'],afterStart['profile']['rank9SpellAccess'] and afterStart['profile']['targetSpell']['repertoireState']=='known/prepared as appropriate' and e['afterState']['actors']['caster']['pendingCast']['rangeFt']<=120 and e['afterState']['actors']['caster']['pendingCast']['lineOfEffect']=='clear')
        win_after=after.get('spellEfficiencyWindow')
        if after['profile']['className']=='Wizard' and not win:
            ck('Wizard efficiency opens for next turn '+e['id'],win_after and win_after['status']=='AVAILABLE' and win_after['expiresAfterTurn']==e['afterState']['world']['regularTurnNumber']+1)
    for e in [x for x in b['events'] if x['eventType']=='RESPONSE_WINDOW']:
        de=e['details']; ck('response candidates recorded '+e['id'],len(de['evaluatedResponders'])==3 and de['counterspellDeclared'] is False)
        for r in de['evaluatedResponders']:
            ck('response decision explicit '+e['id']+'/'+r['actorId'],r['decision'] in ('DECLINES_WITHOUT_DECLARATION','NOT_ELIGIBLE_NO_COUNTERSPELL_ACCESS'))
        selfrow=next(r for r in de['evaluatedResponders'] if r['actorId']=='caster')
        if selfrow['spellAccess']:ck('self-counter eligibility not inferred '+e['id'],selfrow['decision']=='DECLINES_WITHOUT_DECLARATION' and selfrow['eligibilityAdjudication']=='not made for self-declined candidate')

# Positive useful dossier and retrieval behavior.
positive=[b for b in branches if b['caseId'] in ('FOS-P1','FOS-P2')]
expected_ids=['branch-east','dispatch-plan','ferry-report','founded','governance','stores']
for b in positive:
    target='helper' if b['caseId']=='FOS-P2' else 'caster'
    mem=b['terminalState']['actors'][target]['memory']
    ck('recipient-only acquired memory '+b['branchId'],len(mem)==1 and len(b['terminalState']['actors']['helper']['memory'])==(1 if target=='helper' else 0) and len(b['terminalState']['actors']['caster']['memory'])==(1 if target=='caster' else 0))
    d=mem[0]['dossier'];ck('complete permitted dossier '+b['branchId'],[r['id'] for r in d['records']]==expected_ids and all(not r.get('protected',False) for r in d['records']))
    ck('privacy/report classification '+b['branchId'],not any(r['id']=='secret-person' for r in d['records']) and next(r for r in d['records'] if r['id']=='ferry-report')['kind']=='report')
    remote=next(r for r in d['records'] if r['id']=='branch-east')
    ck('same-plane remote history '+b['branchId'],remote['plane']=='TEST-PLANE-A' and remote['location']['distanceFromInstitutionMiles']==500 and remote['location']['plane']=='TEST-PLANE-A')
    f=d['forecast'];ck('supported bounded forecast '+b['branchId'],f['horizonMs']==604800000 and f['evidenceIds']==['dispatch-plan','ferry-report'] and f['forcesFutureActors'] is False and 'alternative' in f and 'qualitativeUncertainty' in f)
    ck('complete paid positive output '+b['branchId'],b['terminalState']['actors']['caster']['spellHistory'][0]['result']=='SUCCESS')
    if b['caseId']=='FOS-P1':
        re=b['terminalState']['retrieval'];ck('focused stores retrieval '+b['branchId'],re['actionSpent'] is True and re['result']['unreservedGrainCrates']==80 and re['supportedForecast']['evidenceIds']==['dispatch-plan','ferry-report'])
    else:
        comm=b['terminalState']['communication'];ck('ordinary subset communication '+b['branchId'],comm['actionCost']==0 and len(comm['learnedFacts'])==3 and all(x['id'] in ('governance','stores','ferry-report') for x in comm['learnedFacts']) and comm['futureForced'] is False)

# Four adverse variants share exactly one public no-information surface.
a1=[b for b in branches if b['caseId']=='FOS-A1'];surfaces=[b['terminalState']['deliveredResult'] for b in a1]
ck('A1 neutral public surface',len(a1)==4 and all(x=={'status':'No information available'} for x in surfaces) and len({json.dumps(x,sort_keys=True) for x in surfaces})==1)
scenarios={b['variant']:b['initialState']['queryContext'] for b in a1}
ck('A1 distinct factual causes',scenarios['protected-member']['protected'] is True and scenarios['missing-record']['recordExists'] is False and scenarios['unestablished-institution']['institutionId']!=C['model']['fixture']['id'] and scenarios['unauthorized-cross-plane-record']['sourcePlane']!='TEST-PLANE-A')
ck('A1 paid before neutral resolution',all(next(e for e in b['events'] if e['eventType']=='SPELL_COMMIT')['details']['finalRPCost']==26 and b['terminalState']['actors']['caster']['spellHistory'][0]['result']=='UNAVAILABLE' for b in a1))
ck('A1 no hidden diagnostics in public response',all(set(b['terminalState']['deliveredResult'])=={'status'} for b in a1))

# Versioned recast/idempotency, complete turn markers, historical memory and no future control.
a2=next(b for b in branches if b['caseId']=='FOS-A2');state=a2['terminalState'];evs=a2['events'];casts=[e for e in evs if e['eventType']=='SPELL_COMMIT']
ck('A2 two distinct paid cast receipts',len(casts)==2 and casts[0]['receiptKey']!=casts[1]['receiptKey'] and all(e['details']['finalRPCost']==26 for e in casts))
dup=next(e for e in evs if e['eventType']=='IDEMPOTENT_CALLBACK');pre=dup['beforeState']['actors']['caster'];post=dup['afterState']['actors']['caster']
ck('A2 duplicate callback no gameplay mutation',dup['details']['expectedNoOp'] and pre['resources']==post['resources'] and pre['spellHistory']==post['spellHistory'] and pre['memory']==post['memory'] and pre['actionBudget']==post['actionBudget'] and dup['afterState']['duplicateCallback']['receipt']==dup['beforeState']['receiptRegistry'][dup['receiptKey']])
upd=next(e for e in evs if e['eventType']=='VERSIONED_SOURCE_UPDATE');ck('A2 versioned changed source',upd['details']['versionBefore']==1 and upd['details']['versionAfter']==2 and upd['afterState']['sourceMutation']['receiptId']=='TEST-DISPATCH-WITHDRAWAL-v2')
ends=[e for e in evs if e['eventType']=='REGULAR_TURN_END'];idle=next(e for e in ends if e['details'].get('idleEligible'))
ck('A2 one real idle-turn decay',idle['beforeState']['actors']['caster']['magicThisTurn'] is False and idle['beforeState']['actors']['caster']['resources']['Dissonance']==2 and idle['afterState']['actors']['caster']['resources']['Dissonance']==1 and idle['afterState']['actors']['caster']['refrainCount']==1)
ck('A2 spell efficiency expires before recast',state['actors']['caster']['spellEfficiencyWindow']['status']=='EXPIRED' and casts[1]['details']['spellEfficiencyDiscount']==0)
mem=state['actors']['caster']['memory'];ck('A2 old memory preserved and historical',len(mem)==2 and mem[0]['historical'] is True and mem[0]['dossier']['forecast']['evidenceIds']==['dispatch-plan','ferry-report'] and mem[1]['historical'] is False)
ck('A2 withdrawn plan affects new forecast',not any(r['id']=='dispatch-plan' and r['value'].get('status')!='withdrawn' for r in mem[1]['dossier']['records'] if isinstance(r['value'],dict)) and mem[1]['dossier']['forecast']['evidenceIds']==['ferry-report'] and state.get('futureActorControl',{}).get('forced') is False)
ck('A2 refrain survives idle and applies +1',casts[1]['details']['refrainAdded']==1 and casts[1]['details']['dissonanceAdded']==3 and state['actors']['caster']['resources']['RP']==12 and state['actors']['caster']['resources']['Dissonance']==4)
ck('no canonical/runtime/campaign promotion',all(b['terminalState']['audit']['nativeCatalogMutated'] is False and b['terminalState']['audit']['campaignFactsAsserted'] is False and b['terminalState']['audit']['canonChanged'] is False for b in branches))

result={'id':'FOS-DD11-SEMANTIC-AND-REPLAY-VALIDATION-01','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','identity':'faction-omniscience-supreme','scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','checksPassed':sum(x['pass'] for x in checks),'checksFailed':sum(not x['pass'] for x in checks),'checks':checks,'replay':{'branchCount':len(branches),'eventCount':replay_events,'forwardAndInverseOperationCount':replay_ops,'canonicalStateHash':'SHA-256 of NFC-normalized sorted compact UTF-8 JSON'},'verificationMethod':{'builderImported':False,'packetReadBack':True,'sourceGitBlobsVerified':True,'fullStateTransitionsReplayed':True,'semanticAssertionsIndependentOfBuilderBooleans':True,'unityOrRuntimeExecuted':False}}
(P/'SEMANTIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','checksPassed','checksFailed','replay')},indent=2))
if result['status']!='PASS':sys.exit(1)
