"""Verify current pending routing against actual index and already prepared exact packet receipts."""
from pathlib import Path
import json,hashlib,datetime
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-129';Q=A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json';I=G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
r=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()
def path(v):
 p=Path(v);return p if p.is_absolute() else G/p
indexHash=sha(I);idx=r(I);assert idx['authoredCounts']=={'reviewed':623,'pending':225};pending={v['id'] for v in idx['entries'] if v['authoredStatus']!='reviewed-authored-operational-playtest'}
packets={}
for sub in ['director-spell-review-127','director-spell-review-128','director-spell-review-129']:
 for p in (A/sub).glob('*PACKET*.json'):
  rec=r(p);b=rec.get('archive',rec)
  if isinstance(b,dict) and all(k in b for k in ['path','bytes','sha256']):packets[str(path(b['path']))]=(p,b)
q=r(Q);old=Q.read_bytes();rows=[]
for g in q['groups']:
 ids=set(g['identities'])&pending
 if not ids:continue
 assert ids==set(g['identities'])
 current=g.get('currentPacket')
 if not current:current=g['preparedCurrentPacket']['archive']['path']
 p=path(current)
 if p.suffix=='.json':rec=r(p);p=path(rec.get('archive',rec)['path'])
 assert str(p) in packets,(g['group'],str(p))
 rp,b=packets[str(p)];assert p.stat().st_size==b['bytes'] and sha(p)==b['sha256'],g['group']
 g['currentPacket']=str(p);g['currentPacketReceipt']=str(rp)
 rows.append({'group':g['group'],'identities':g['identities'],'phase':g['currentPhase'],'archive':b,'receipt':str(rp),'bindingsVerifiedNow':True})
flat=[sid for v in rows for sid in v['identities']];assert len(flat)==len(set(flat))==225 and set(flat)==pending and len(rows)==43
now=datetime.datetime.now(datetime.timezone.utc).isoformat();out=D/'CURRENT225_PACKET_INVENTORY_129.json';assert not out.exists()
save(out,{'id':'CURRENT225-PACKET-INVENTORY-129','recordedAtUtc':now,'counts':idx['authoredCounts'],'groups':rows,'groupsCount':43,'pendingExactlyOnce':225,'allCurrentPacketArchiveBindingsVerified':True,'indexSha256Unchanged':indexHash,'scope':'Navigation only. One sent LifeMatter5 conference;42 prepared conferences still unaccepted. No new authored acceptance/application.'})
backup=D/'CURRENT_SPELL_QUEUE.before_route_refresh_129.json';assert not backup.exists();backup.write_bytes(old);q['currentPacketInventory']=str(out);q['lastUpdatedAtUtc']=now;save(Q,q)
for p in [D/'LIFEMATTER5_SEND_RECEIPT_129.json']:
 v=r(p);v.update({'status':'SENT_UI_AND_THREAD_RECEIPT_VERIFIED','requestId':'778fe783-5364-48b1-b62d-033fe02dbeeb','threadVerification':'read_thread returns exact user request ID and all three attached filenames; thread is active.'});save(p,v)
for p in [D/'CURRENT_HANDOFF_129.json',A/'ACTIVE_AUTHORING_CHECKPOINT_ORDINARY_SPELL_REVIEW_129.json',Q]:
 v=r(p);v['director'].update({'activeRequest':'778fe783-5364-48b1-b62d-033fe02dbeeb','activeRequestStatus':'SENT_UI_AND_THREAD_RECEIPT_VERIFIED'});v['currentPacketInventory']=str(out)
 if 'lifeMatter5Send129' in v:v['lifeMatter5Send129']=r(D/'LIFEMATTER5_SEND_RECEIPT_129.json')
 save(p,v)
assert sha(I)==indexHash
print(json.dumps({'pending':225,'groups':43,'allArchiveBindingsVerified':True,'canonicalIndexUnchanged':True,'navigationUpdated':str(out)}))
