from pathlib import Path, PurePosixPath
import json, hashlib, zipfile
from datetime import datetime, timezone

R=Path(r'C:\Github\DecenniumDescent'); A=R/'docs/audit/2026-10-08/full-game'; O=A/'spell-review-resume-116'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
q=read(R/'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json')
accepted_names={'illusion-perception14','control15','companion-life10','rank8-damage6','rank7-identity-casting5','rank9-resonance-fields3'}
groups=[]; checks=[]
for g in q['groups']:
    p=R/g['archive']['path']; b=p.read_bytes()
    assert len(b)==g['archive']['bytes'] and sha(b)==g['archive']['sha256'],g['group']
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None,g['group']
        names=z.namelist()
        assert len(names)==len(set(names))
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
    assert len(g['identities'])==g['identityCount']
    checks.append({'group':g['group'],'archiveBinding':True,'crc':True,'safeUniqueMembers':True,'identityCount':True})
    accepted=g['group'] in accepted_names
    groups.append({k:g[k] for k in ['group','identities','identityCount','candidate','archive']} | {
        'currentPhase':'accepted-unapplied' if accepted else ('conference-submitted-116' if g['group']=='rank7-mechanics16' else 'prepared-awaiting-review'),
        'historicalPhase':g['phase'],
        'riskCounts':g.get('riskCounts'),
    })
allids=[x for g in groups for x in g['identities']]
assert len(allids)==323 and len(set(allids))==323
assert set(allids)=={x['id'] for x in q['rows']}
accepted=[x for g in groups if g['currentPhase']=='accepted-unapplied' for x in g['identities']]
assert len(accepted)==53
for file,gn in [('RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json','rank8-damage6'),('RANK7_IDENTITY_CASTING5_PART5_EXACT_AUTHORING_ACCEPTANCE_79.json','rank7-identity-casting5'),('RANK9_RESONANCE_FIELDS3_PART5_EXACT_AUTHORING_ACCEPTANCE_90.json','rank9-resonance-fields3')]:
    d=read(A/file); g=next(g for g in groups if g['group']==gn)
    assert set(d['identities'])==set(g['identities'])
    model=R/d['selectedSuccessor']['path'];assert sha(model.read_bytes())==d['selectedSuccessor']['sha256']
current={'id':'SPELL-REVIEW-QUEUE-116','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'sourceQueue':str(R/'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json'),
 'sourceQueueSha256':sha((R/'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json').read_bytes()),
 'currentCounts':{'appliedReviewed':525,'indexPending':323,'acceptedUnapplied':53,'needsAcceptance':270,'submittedAwaitingReturn':16,'otherUnaccepted':254},
 'groups':groups,'acceptedIdentities':accepted,
 'sourceArchiveAudit':{'groupCount':56,'passed':True,'checks':checks},
 'scope':'Current review navigation only. Original queue and all archives unchanged; no new semantic acceptance, canonical application or runtime execution.',
 'latestAcceptanceReceipts':['RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json','RANK7_IDENTITY_CASTING5_PART5_EXACT_AUTHORING_ACCEPTANCE_79.json','RANK9_RESONANCE_FIELDS3_PART5_EXACT_AUTHORING_ACCEPTANCE_90.json'],
 'nextSuggestedGroups':['memory2','material-terrain8','body-defense8','time-cast5','transport6','magic-modifiers7']}
write(O/'CURRENT_SPELL_QUEUE.json',current)
prep=read(O/'PREPARATION.json')
dom=(O/'GPT_SENT_DOM.txt').read_text(encoding='utf-8')
assert 'ChatGPT is responding' in dom and 'Continue the ordinary-spell review.' in dom
write(O/'ACTUAL_DISPATCH.json',{'id':'SPELL-REVIEW-116-ACTUAL-DISPATCH','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'conversation':'Calibration Review Part 5','conversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad4a867-f330-83e9-829e-bf2bb41a6c09',
 'actuallySent':True,'responseObserved':'ChatGPT is responding','requestFile':str(O/'GPT_REQUEST.txt'),'requestSha256':sha((O/'GPT_REQUEST.txt').read_bytes()),
 'sourceArchive':prep['sourceArchive'],'contextArchive':prep['contextArchive'],'proof':{'dom':str(O/'GPT_SENT_DOM.txt'),'screenshot':str(O/'GPT_SENT.png')},
 'acceptedNewIdentities':0,'canonicalApplied':False})
print('56 archive hashes/CRC/safe-member/identity checks pass; all323 identities unique;53 accepted and270 remaining. Actual dispatch recorded.')
