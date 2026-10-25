"""Refresh navigation only; canonical spell index is read and verified, never edited."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-129'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
index=G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
assert hashlib.sha256(index.read_bytes()).hexdigest()=='a03b61fe6b2bbebc9b019e5576287603c6b9a84708beb361e9b9c5e5e35cc535'
q=read(A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json');h=read(D/'CURRENT_HANDOFF_129.json');receipts=[]
for p in sorted(D.glob('RANK*_PACKET_129.json')):
 r=read(p);assert r['status']=='PREPARED_NOT_SENT'
 ap=Path(r['archive']['path']);b=ap.read_bytes();assert len(b)==r['archive']['bytes'] and hashlib.sha256(b).hexdigest()==r['archive']['sha256']
 receipts.append(str(p))
h['newPreparedPackets']=list(dict.fromkeys(h['newPreparedPackets']+receipts))
h['lastUpdatedAtUtc']=datetime.now(timezone.utc).isoformat()
prepared=[g['group'] for g in q['groups'] if g['currentPhase']=='current-director-conference-prepared-129-unsent']
nextgroups=[g['group'] for g in q['groups'] if g['currentPhase']=='prepared-awaiting-review']
h['preparation129']={'verifiedUnsentPacketReceipts':receipts,'count':len(receipts),'lastFullyReadAndPrepared':prepared[-1],'nextSourceGroup':nextgroups[0] if nextgroups else None,'canonicalIndexSha256Unchanged':hashlib.sha256(index.read_bytes()).hexdigest(),'newAccepted':0,'newApplied':0,'preparationIsNotAcceptance':True}
write(D/'CURRENT_HANDOFF_129.json',h)
cp=A/'ACTIVE_AUTHORING_CHECKPOINT_ORDINARY_SPELL_REVIEW_129.json';c=read(cp);c['lastUpdatedAtUtc']=h['lastUpdatedAtUtc'];c['preparation129']=h['preparation129'];write(cp,c)
print(json.dumps(h['preparation129'],indent=2))
