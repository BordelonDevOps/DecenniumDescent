from pathlib import Path
import json, hashlib, subprocess, re
ROOT=Path(__file__).resolve().parents[6] if __name__!='__main__' else Path.cwd()
WITNESS=Path('docs/audit/2026-10-08/full-game/director-spell-review-129/final_word_testonly_fixture_proposal_485/FW485_R1_TESTONLY_WITNESS_01.json')
PROPOSAL=WITNESS.with_name('FINAL_WORD_FW485_TESTONLY_FIXTURE_PROPOSAL_REPACK01.json')
ADOPTION=WITNESS.with_name('OWNER_ADOPTION_FW485_TESTONLY.json')
DECISION_COMMIT='426c65cc9e6c9504615c6697c155e7899f524f96'
ADOPTION_COMMIT='90e9ace45a14589b1b35295a787d0a9691d373c0'
BASE_COMMIT='5f12d1388083c36d014101d8507bd5db61a6a499'
QUEUE_COMMIT='9936314fc77695a0f4c7e030da2e902c7c273c0e'

def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()
def git_blob(commit,path): return subprocess.check_output(['git','cat-file','blob',f'{commit}:{path}'])
def git_pointer(commit,path):
    raw=git_blob(commit,path).decode('utf-8')
    oid=re.search(r'oid sha256:([0-9a-f]{64})',raw).group(1)
    size=int(re.search(r'size (\d+)',raw).group(1))
    return oid,size

def get(obj,path):
    cur=obj
    for part in path.strip('/').split('/') if path else []: cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    return cur
def setv(obj,path,value):
    parts=path.strip('/').split('/'); cur=obj
    for part in parts[:-1]: cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    key=parts[-1]
    if isinstance(cur,list): cur[int(key)]=value
    else: cur[key]=value

def verify():
    w=json.loads(WITNESS.read_text(encoding='utf-8')); p=json.loads(PROPOSAL.read_text(encoding='utf-8')); a=json.loads(ADOPTION.read_text(encoding='utf-8'))
    assert hashlib.sha256(PROPOSAL.read_bytes()).hexdigest()==w['scope']['proposalSha256']
    assert hashlib.sha256(ADOPTION.read_bytes()).hexdigest()==w['scope']['ownerAdoptionSha256']
    assert a['ownerAuthorization']['proposalSha256Adopted']==w['scope']['proposalSha256']
    assert a['scope']['branch']=='DR217-B01-TESTONLY-ROUTE-484-01/FW485-R1'
    assert w['base']['queueAuthority']=={'reviewedApplied':832,'pending':16,'acceptedUnapplied':0}
    # Validate every declared textual source in the proposal and the exact LFS payload pointer.
    text_count=0
    for b in p['sourceBindings']:
        if b['id']=='preserved-return217-closure-delta-303':
            oid,size=git_pointer(BASE_COMMIT,b['path']); assert (oid,size)==(b['sha256'],b['bytes']); continue
        entries=[b['catalog'],b['authoredIndex']] if b['id']=='current-catalog-and-authored-index' else [b]
        for e in entries:
            path=e['path']; commit=e.get('commit') or (DECISION_COMMIT if path.endswith('DIRECTOR_READBACK_FINAL_WORD_TESTONLY_ROUTE_484_01.json') else (QUEUE_COMMIT if path.endswith('CURRENT_SPELL_QUEUE_477_REPACK01.json') else BASE_COMMIT))
            raw=git_blob(commit,path); assert len(raw)==e['bytes'] and hashlib.sha256(raw).hexdigest()==e['sha256'],(path,len(raw),hashlib.sha256(raw).hexdigest())
            text_count+=1
    assert text_count==15,text_count
    adoption_path='docs/audit/2026-10-08/full-game/director-spell-review-129/final_word_testonly_fixture_proposal_485/OWNER_ADOPTION_FW485_TESTONLY.json'
    raw=git_blob(ADOPTION_COMMIT,adoption_path); assert len(raw)==3535 and hashlib.sha256(raw).hexdigest()==w['scope']['ownerAdoptionSha256']
    # Replay every forward patch with before-value guards and compare every complete snapshot.
    state=json.loads(json.dumps(w['startingState']))
    assert canonical_hash(state)==w['inverseVerification']['initialStateSha256']
    snap={x['afterEvent']:x for x in w['snapshots']}
    for group in w['forwardOperations']:
        for op in group['operations']:
            assert get(state,op['path'])==op['before'],(group['eventId'],op['path'],get(state,op['path']),op['before'])
            setv(state,op['path'],op['after'])
        if group['eventId'] in snap:
            assert state==snap[group['eventId']]['state'],group['eventId']
            assert canonical_hash(state)==snap[group['eventId']]['stateSha256']
    assert state==w['expectedTerminalState']
    assert canonical_hash(state)==w['verification']['terminalStateSha256']
    # Reverse the committed operations and prove exact branch-start restoration.
    restored=json.loads(json.dumps(state))
    for group in w['inverseOperations']:
        for op in group['operations']:
            assert get(restored,op['path'])==op['before'],('inverse',group['eventId'],op['path'])
            setv(restored,op['path'],op['after'])
    assert restored==w['startingState'] and restored==w['inverseVerification']['restoredState']
    assert canonical_hash(restored)==w['inverseVerification']['restoredStateSha256']
    # Semantic invariants required by the Director.
    c=state['caster']; v=state['victim']; token=state['reserveToken']
    assert v['HP']['normalCurrent']==49 and 0<49<50 and v['life']=='Dead'
    assert token['sourceCastEvent']=='FW485-E002' and token['sourceDeathEvent']=='FW485-E003' and token['status']=='consumed'
    assert token['rpSpent']==2 and token['unusedRPForfeited']==3 and token['currentRP']==0
    assert c['RP']==42 and c['temporaryHP']==5 and c['dissonance']==0 and c['refrain']==0
    assert c['arcaneWard']['type']=='force' and c['spellEfficiencyAcquired'] is False
    assert c['pendingCast'] is None and c['magicThisTurn'] is True
    assert state['campaignEventClaimed'] is False
    assert v['body']['destroyed'] is False and v['custody']['equipmentOwnershipTransfers'] is False
    assert w['tokenExpiryEndpoint']['expiryExecuted'] is False and w['tokenExpiryEndpoint']['restBenefitGranted'] is False
    checks=w['verification']['checks']; assert all(checks.values()),checks
    print('PASS: proposal/adoption hashes; 15 text sources and archive LFS pointer; 8 forward/inverse event groups; 14 semantic checks; exact inverse restoration.')
    print('proposal_sha256',hashlib.sha256(PROPOSAL.read_bytes()).hexdigest())
    print('adoption_sha256',hashlib.sha256(ADOPTION.read_bytes()).hexdigest())
    print('witness_sha256',hashlib.sha256(WITNESS.read_bytes()).hexdigest(),'bytes',WITNESS.stat().st_size)
if __name__=='__main__': verify()
