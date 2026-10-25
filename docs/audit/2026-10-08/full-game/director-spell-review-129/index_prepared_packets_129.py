"""Bind already-prepared packets into navigation without changing canonical procedures."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,collections
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-129'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
ip=G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json';raw=ip.read_bytes();idx=read(ip)
assert sha(raw)=='a03b61fe6b2bbebc9b019e5576287603c6b9a84708beb361e9b9c5e5e35cc535'
qp=A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json';q=read(qp);updated=[]
for rp in sorted(D.glob('RANK*_PACKET_129.json')):
 r=read(rp);assert r['status']=='PREPARED_NOT_SENT';label=rp.name.removesuffix('_PACKET_129.json');notes=read(D/(label+'_NEXT_CONFERENCE_NOTES_129.json'))
 g=next(g for g in q['groups'] if set(g['identities'])==set(notes['identities']));assert g['currentPhase']=='current-director-conference-prepared-129-unsent'
 p=Path(r['archive']['path']);b=p.read_bytes();assert len(b)==r['archive']['bytes'] and sha(b)==r['archive']['sha256']
 if g.get('currentPacket') and g['currentPacket']!=str(p):g.setdefault('priorPreparedPackets',[]).append(g['currentPacket'])
 g['currentPacket']=str(p);g['currentPacketBinding']=r['archive'];g['currentPacketReceipt']=str(rp);g['independentReview']=str(D/(label+'_NEXT_CONFERENCE_NOTES_129.json'));g['actuallySent']=False
 updated.append(g['group'])
pending={e['id'] for e in idx['entries'] if e['authoredStatus']!='reviewed-authored-operational-playtest'}
groups=[g for g in q['groups'] if set(g['identities'])&pending];flat=[sid for g in groups for sid in g['identities']]
assert len(flat)==len(set(flat))==232 and set(flat)==pending
inventory={'id':'CURRENT232-PACKET-INVENTORY-129','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'counts':{'reviewedApplied':616,'pending':232,'acceptedUnapplied':0,'pendingGroups':len(groups),'refreshedRank8Rank9Packets':len(updated)},'updatedGroups':updated,'indexSha256Unchanged':sha(raw),'groups':[{'group':g['group'],'identities':g['identities'],'currentPhase':g['currentPhase'],'currentPacket':g.get('currentPacket'),'currentPacketReceipt':g.get('currentPacketReceipt')} for g in groups],'scope':'Navigation/source-conference readiness only. Current canonical acceptance is unchanged. Each future conference must receive current applied context at dispatch.'}
q['lastUpdatedAtUtc']=inventory['recordedAtUtc'];q['currentPacketInventory']=str(D/'CURRENT232_PACKET_INVENTORY_129.json');write(qp,q);write(D/'CURRENT232_PACKET_INVENTORY_129.json',inventory)
assert ip.read_bytes()==raw
print(json.dumps({'counts':inventory['counts'],'pendingPhaseCounts':dict(collections.Counter(g['currentPhase'] for g in groups)),'packetNavigationUpdated':len(updated),'canonicalChanges':False},indent=2))
