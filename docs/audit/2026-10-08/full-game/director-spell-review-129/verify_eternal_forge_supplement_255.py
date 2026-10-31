from __future__ import annotations
import copy, hashlib, json, pathlib, zipfile

HERE=pathlib.Path(__file__).resolve().parent; REPO=HERE.parents[4]
PACKET=HERE/'ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_255.json'
AUDIT=HERE/'ETERNAL_FORGE_MF210_B01_SUPPLEMENT_255_INDEPENDENT_AUDIT.json'

def canonical(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def sha(v): return hashlib.sha256(canonical(v)).hexdigest()
def file_sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def parts(path): return [] if path=='' else [x.replace('~1','/').replace('~0','~') for x in path[1:].split('/')]
def get(root,ps):
    x=root
    for p in ps: x=x[int(p)] if isinstance(x,list) else x[p]
    return x
def parent(root,ps):
    x=root
    for p in ps[:-1]: x=x[int(p)] if isinstance(x,list) else x[p]
    return x,ps[-1]
def apply(state,ops):
    x=copy.deepcopy(state)
    for o in ops:
        ps=parts(o['path']); op=o['op']
        if op=='test': assert get(x,ps)==o['value'],f"test failed {o['path']}"
        elif op=='replace':
            p,k=parent(x,ps); assert (int(k)<len(p) if isinstance(p,list) else k in p),f"missing {o['path']}"
            if isinstance(p,list): p[int(k)]=copy.deepcopy(o['value'])
            else: p[k]=copy.deepcopy(o['value'])
        elif op=='add':
            p,k=parent(x,ps); assert k not in p,f"exists {o['path']}"; p[k]=copy.deepcopy(o['value'])
        elif op=='remove':
            p,k=parent(x,ps)
            if isinstance(p,list): del p[int(k)]
            else: del p[k]
        else: raise AssertionError('unsupported operation '+op)
    return x

p=json.loads(PACKET.read_text(encoding='utf-8')); audit=json.loads(AUDIT.read_text(encoding='utf-8'))
branch=p['eventReplay']['branches'][0]; base=p['priorCase']['endState']
assert sha(base)==p['priorCase']['endSnapshotSHA256']==p['eventReplay']['baseStateSHA256']==branch['baseStateSHA256']
assert p['authority']=={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0}
correction=HERE/'ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_254.json'
assert p['correctionOf']=={'packet':'ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_254.json','bytes':501529,
    'sha256':'75780d2989b4bf0f07ad2db0d55e0b1a4674140d8dae17176f3948ed9e0622ee',
    'correctionScope':['MF254-W2-C01 prepared-family history and castF3 Dissonance','MF254-W2-C02 B regular-start chronology','MF254-W2-C03 turnCast commitment flags','cumulative regularStartsProcessed ledger']}
assert correction.stat().st_size==p['correctionOf']['bytes'] and file_sha(correction)==p['correctionOf']['sha256']
registry=p['sourceBindings'][11]
assert registry['path']=='DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_01.json'
assert registry['bytes']==236021 and registry['sha256']=='40fe3da68084e8c9b875f5d21c5ff607867147153ab4f9f7e483f35b2c5fd1f6'
assert p['acceptedIds']==[] and p['appliedIds']==[] and p['canonicalChanges'] is False and p['applicationChanges'] is False
assert p['priorCase']['caseId']=='MF210-F02' and p['priorCase']['endEventId']=='MF210-F02:6'
assert base['time']==12.1 and base['actors']['A']['RP']==38
assert base['items']['bracelet-1']['imprintRoot']['id']=='castF2' and base['items']['bracelet-1']['charges']==0

# Reproduce every bound file and archive-member hash independently.
for b in p['sourceBindings']:
    path=REPO/b['path']
    if 'packetMember' in b:
        with zipfile.ZipFile(path) as z: data=z.read(b['packetMember'])
        assert len(data)==b['bytes'] and hashlib.sha256(data).hexdigest()==b['sha256'],b['packetMember']
    else:
        data=path.read_bytes(); assert len(data)==b['bytes'] and hashlib.sha256(data).hexdigest()==b['sha256'],b['path']

# Source packet independently confirms the exact F02 endpoint.
archive=REPO/p['priorCase']['sourceArchive']['path']
assert archive.stat().st_size==p['priorCase']['sourceArchive']['bytes'] and file_sha(archive)==p['priorCase']['sourceArchive']['sha256']
with zipfile.ZipFile(archive) as z: original=json.loads(z.read('cases/MF210-F02.json'))
source_end=original['events'][-1]
assert source_end['id']=='MF210-F02:6' and sha(source_end['after'])==sha(base)

# Verify monotonic forward replay and reverse every event exactly to its predecessor.
state=copy.deepcopy(base); before_states=[]; after_states={}; fwd=inv=0
for e in branch['events']:
    assert sha(state)==e['beforeSHA256'],e['id']+' before'
    before_states.append(copy.deepcopy(state)); state=apply(state,e['forward'])
    assert sha(state)==e['afterSHA256'],e['id']+' after'; after_states[e['id']]=copy.deepcopy(state); fwd+=len(e['forward']); inv+=len(e['inverse'])
assert sha(state)==branch['finalStateSHA256'] and sha(state)==audit['finalStateSHA256']
for e,expected_before in zip(reversed(branch['events']),reversed(before_states)):
    assert sha(state)==e['afterSHA256'],e['id']+' reverse-start'
    state=apply(state,e['inverse']); assert sha(state)==sha(expected_before),e['id']+' inverse'
assert sha(state)==sha(base)
state=copy.deepcopy(base)
for e in branch['events']: state=apply(state,e['forward'])

# Lifecycle, payment, identity, and outcome checks.
old=state['items']['bracelet-1']; new=state['items']['bracelet-2']; a=state['actors']['A']; b=state['actors']['B']
assert state['time']==172806.6 and a['RP']==13 and b['RP']==0
assert (old['owner'],old['custodian'],old['HP'],old['charges'],old['maximumCharges'])==('A','B-right-wrist',2,0,1)
assert old['processedDawns']==['MF210-W2-CLOCK-01:jewelcrafting-dawn:1','MF210-W2-CLOCK-01:jewelcrafting-dawn:2']
assert old['imprintRoot']['id']=='castF2' and old['imprintRoot']['active'] is False and old['imprintRoot']['endReason']=='actual-successful-dispel'
assert new['id']=='bracelet-2' and new['imprintRoot']['id']=='castF3' and new['imprintRoot']['active'] is True and new['charges']==1
assert old['provenance']==['castF2'] and new['provenance']==['castF3']
assert a['resourceHistory'][-3]['spell']=='antimagic-field-lesser' and a['resourceHistory'][-3]['cost']==10
assert a['resourceHistory'][-2]['spell']=='greater-dispel' and a['resourceHistory'][-2]['cost']==10
assert a['resourceHistory'][-1]['spell']=='eternal-forge' and a['resourceHistory'][-1]['cost']==26
assert [x['chargesAfter'] for x in state['supplement']['dawnEvents']]==[0,1]
assert state['supplement']['dawnEvents'][0]['eligible'] is False and state['supplement']['dawnEvents'][1]['eligible'] is True
assert state['supplement']['chargeTransactions'][0]['declaredBeforeRoll'] is True
assert state['rolls'][-2]['id']=='hideW2' and state['rolls'][-2]['chargeDebitedBeforeDice'] is True and state['rolls'][-2]['total']==18
assert state['rolls'][-1]['id']=='dispelW2' and state['rolls'][-1]['total']==28 and state['rolls'][-1]['DC']==28
assert state['rolls'][-1]['kind']=='Greater Dispel rank-check'
assert state['rolls'][-1]['centerPerceived'] is True and state['rolls'][-1]['centerDistanceFeet']==3.905
assert state['rolls'][-1]['maximumRangeFeet']==30 and state['rolls'][-1]['radiusFeet']==30
assert state['rolls'][-1]['immutableCapturedApplications']==['castF2']
assert state['rolls'][-1]['alliesIncludedInCaptureRule'] is True and state['rolls'][-1]['castF2NotSuppressed'] is True
assert state['terminalCasts']['greaterDispelW2']['paidRP']==10
assert state['terminalCasts']['greaterDispelW2']['paidAction']=='Action'
assert state['terminalCasts']['greaterDispelW2']['components']=='V/S/F'
assert state['supplement']['spellEvents'][-2]['castId']=='greaterDispelW2'
assert state['supplement']['imprintEndings'][0]['physicalBodyPreserved'] is True
assert state['supplement']['imprintEndings'][0]['HP']==2 and state['supplement']['imprintEndings'][0]['charges']==0
assert state['supplement']['imprintEndings'][0]['owner']=='A'
assert state['supplement']['imprintEndings'][0]['custodian']=='B-right-wrist'
assert state['supplement']['objectDamageEvents'][0]['itemHPBefore']==5 and state['supplement']['objectDamageEvents'][0]['itemHPAfter']==2
assert state['supplement']['objectDamageEvents'][0]['wearerHPBefore']==state['supplement']['objectDamageEvents'][0]['wearerHPAfter']==10
assert state['supplement']['rests'][0]['arithmetic']['recovery']==21
assert state['supplement']['rests'][0]['arithmetic']['before']==38 and state['supplement']['rests'][0]['arithmetic']['after']==59
assert state['supplement']['rests'][0]['id']=='MF210-W2-RETUNE-REST-01'
assert state['supplement']['rests'][0]['safeAndPermittedCircumstances'] is True
assert state['supplement']['rests'][0]['completionId']=='MF210-W2-RETUNE-REST-01-COMPLETE'
assert state['supplement']['rests'][0]['overlappingActiveWork'] is False
assert state['supplement']['rests'][0]['automaticHPRecovery'] is False
assert state['supplement']['rests'][0]['RefrainReset'] is False
assert state['supplement']['rests'][0]['rememberedSpellNameReset'] is False
assert state['supplement']['rests'][0]['preparedFamilyHistoryReset'] is False
assert state['supplement']['rests'][0]['durationSeconds']==3600
assert state['supplement']['rests'][0]['beneficialShortRestsSinceLongRest']==1
assert state['supplement']['rests'][0]['maximum']==2
assert state['actors']['B']['conscious'] is True and state['actors']['B']['incapacitated'] is False
assert state['actors']['B']['HP']==10 and state['actors']['B']['profile']['HP']==10
assert state['actors']['B']['profile']['class'] is None and state['actors']['B']['profile']['classLevel'] is None
assert state['actors']['B']['profile']['spellcasting'] is False and state['actors']['B']['profile']['learned']==[]
assert state['actors']['B']['profile']['prepared']==[] and state['actors']['B']['profile']['inventory']==[]
assert state['actors']['B']['profile']['ACDerivation']=='unarmored 10 + DEX 2; no armor or shield'
assert state['actors']['B']['profile']['body']['wristAnatomy'].find('explicit local fixture input')>=0
assert state['actors']['B']['profile']['body']['rightWristPointFeet']==[2.5,0,3]
assert state['scene']['w2Geometry']['BoccupiedBoxFeet']==[[2.5,-2.5,0],[7.5,2.5,6]]
assert state['scene']['w2Geometry']['handoffPointFeet']==state['scene']['w2Geometry']['BRightWristPointFeet']==[2.5,0,3]
assert [x['cost'] for x in state['supplement']['custodyHistory']]==['A Action','B free object interaction','B Action to don']
assert state['supplement']['receiver']['competingEquipmentEffects']==[]
assert state['supplement']['receiver']['otherStealthBonuses']==[]
assert state['supplement']['receiver']['rightWristPointFeet']==[2.5,0,3]
assert state['supplement']['dawnEvents'][0]['identity'].endswith('dawn:1')
assert state['supplement']['dawnEvents'][1]['identity'].endswith('dawn:2')
assert state['supplement']['activeEffects']['amfW2']['status']=='ended-at-deadline'
assert a['usedPreparedFamilies']==['eternal-forge','antimagic-field-lesser','greater-dispel']
assert a['regularStartsProcessed']==[0,6,12,18,24,86398,86460,172800.4,172806.4]
assert b['regularStartsProcessed']==[18.2,24.2,86460.2,172800.2,172806.2]
assert a['resourceHistory'][-3]['firstFamily'] is True and a['resourceHistory'][-3]['baseDissonance']==0
assert a['resourceHistory'][-2]['firstFamily'] is True and a['resourceHistory'][-2]['baseDissonance']==0
assert a['resourceHistory'][-1]['firstFamily'] is False and a['resourceHistory'][-1]['baseDissonance']==2
assert a['resourceHistory'][-1]['RefrainAdded']==0 and a['resourceHistory'][-1]['DissonanceAfter']==2
assert a['Dissonance']==2 and a['turnCast'] is True
assert after_states['MF247-F-W2-E20-PAID-GREATER-DISPEL']['actors']['A']['turnCast'] is True
assert after_states['MF247-F-W2-E20-PAID-GREATER-DISPEL']['actors']['A']['Dissonance']==0
assert after_states['MF247-F-W2-E22-A-NEXT-TURN']['actors']['A']['turnCast'] is False
assert after_states['MF247-F-W2-E23-SECOND-PAID-FORGE']['actors']['A']['turnCast'] is True
for cast_id, expected in [('amfW2',(True,0,0)),('greaterDispelW2',(True,0,0)),('castF3',(False,2,2))]:
    mirror=state['terminalCasts'][cast_id]
    assert (mirror['firstFamily'],mirror['baseDissonance'],mirror['DissonanceAfter'])==expected
    assert mirror['turnCast'] is True
assert after_states['MF247-F-W2-E13-SUNDER-START-DRAW']['actors']['B']['regularStart']==24.2
assert after_states['MF247-F-W2-E13-SUNDER-START-DRAW']['actors']['B']['Action']==0
assert 86460.2 not in after_states['MF247-F-W2-E13-SUNDER-START-DRAW']['actors']['B']['regularStartsProcessed']
assert after_states['MF247-F-W2-E14-SUNDER-HIT']['actors']['B']['regularStart']==24.2
assert after_states['MF247-F-W2-E15-CLOSE-SUNDER']['actors']['B']['regularStart']==86460.2
assert after_states['MF247-F-W2-E15-CLOSE-SUNDER']['supplement']['initiativeEpisodes'][-1]['turnStarts'][-1]['timeSeconds']==86460.2
assert after_states['MF247-F-W2-E15-CLOSE-SUNDER']['supplement']['initiativeEpisodes'][-1]['turnStarts'][-1]['budgetRefreshed'] is True
assert after_states['MF247-F-W2-E15-CLOSE-SUNDER']['supplement']['initiativeEpisodes'][-1]['endSeconds']==86460.3
assert all(86460.2 not in x['actors']['B']['regularStartsProcessed'] for x in after_states.values() if x['time']<86460.2)
assert p['sourceDecision']['summary'].find('Greater Dispel')>=0
assert 'Arch Dispel Magic for the actual castF2 ending' not in p['sourceDecision']['summary']
assert all('MF210-F-wizard-arch-dispel-magic.json' not in x['path'] for x in p['sourceBindings'])
assert p['componentW1']['status']=='COMPLETE_COMPONENT_WITNESS'

audit.update({'status':'CORRECTION_LOCAL_FORWARD_INVERSE_SOURCE_AND_SEMANTIC_CHECKS_PASS_PENDING_GPT_DIRECTOR_REVIEW',
    'verifiedForwardOperations':fwd,'verifiedInverseOperations':inv,
    'checksPending':['GPT semantic review'],
    'checks':{'exactF02Checkpoint':True,'sourceBindings':True,'allForwardHashes':True,'allInverseHashes':True,
        'fixedDawnIdentities':True,'suppressedDawnNoRefill':True,'noCatchUpAfterResume':True,'positiveHPLaterRefill':True,
        'realPreRollChargeSpend':True,'objectDamageOnly':True,'paidDispelCheck':True,'physicalBodyPreserved':True,
        'distinctPaidCreation':True,'preparedFamilyHistoryPreserved':True,'castF3DissonanceAndMirrors':True,
        'turnCastFlagsAtCommitment':True,'cumulativeTurnStartLedgers':True,'BStartAfterAttackAt86460_2':True,
        'registrySourceExactBytes':True,'correctionPacket254BoundExact':True,
        'authorityUnchanged':True,'canonicalChanges':False,'applicationChanges':False},
    'directorReviewStillRequired':True})
AUDIT.write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'result':'PASS','events':len(branch['events']),'forwardOperations':fwd,'inverseOperations':inv,
    'packetBytes':PACKET.stat().st_size,'packetSHA256':file_sha(PACKET),'auditSHA256':file_sha(AUDIT),
    'authority':p['authority'],'acceptedIds':p['acceptedIds'],'appliedIds':p['appliedIds']},indent=2))
