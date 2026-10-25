from __future__ import annotations
import hashlib,json,pathlib,re,zipfile
from datetime import datetime,timezone
R=pathlib.Path('C:/Github/DecenniumDescent');A=R/'docs/audit/2026-10-08/full-game/director-spell-review-129'
INDEX=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CAT=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
idx=json.loads(INDEX.read_text(encoding='utf-8'));catalog=json.loads(CAT.read_text(encoding='utf-8'))
queue_files=sorted((p for p in A.glob('CURRENT_SPELL_QUEUE_*.json') if re.fullmatch(r'CURRENT_SPELL_QUEUE_\d+\.json',p.name)),key=lambda p:int(p.stem.rsplit('_',1)[1]))
pending_files=sorted((p for p in A.glob('CURRENT*_PENDING_IDENTITY_AUDIT_*.json') if re.fullmatch(r'CURRENT\d+_PENDING_IDENTITY_AUDIT_\d+\.json',p.name)),key=lambda p:int(p.stem.rsplit('_',1)[1]))
handoff_files=sorted((p for p in A.glob('CURRENT_HANDOFF_*.json') if re.fullmatch(r'CURRENT_HANDOFF_\d+\.json',p.name)),key=lambda p:int(p.stem.rsplit('_',1)[1]))
queue_path=queue_files[-1];pending_path=pending_files[-1];handoff_path=handoff_files[-1]
queue=json.loads(queue_path.read_text(encoding='utf-8'));pending=json.loads(pending_path.read_text(encoding='utf-8'));handoff=json.loads(handoff_path.read_text(encoding='utf-8'))
assert idx['authoredCounts']['pending']==queue['currentAuthority']['pending']==pending['pendingCount']
assert idx['authoredCounts']['reviewed']==queue['currentAuthority']['reviewedApplied']
group=queue['currentPendingGroups'][0];ids=group['pendingIds'];assert ids and len(ids)==group['pendingCount']
candidate=R/group['candidate']['path'];archive=R/group['archive']['path']
assert bind(candidate)==group['candidate'] and bind(archive)==group['archive']
prev=idx['additionalStandaloneEnvelopes'][-1]
prev_model=(INDEX.parent/prev['file']).resolve();assert bind(prev_model)==prev['binding']
prev_dir=prev_model.parent
prev_receipt=prev_dir/'EXACT_ACCEPTANCE.json';prev_holds=prev_dir/'HOLD_REGISTER.json'
inputs=[
 ('authority/authored_review_index.json',INDEX),('authority/catalog.json',CAT),
 (f'authority/{queue_path.name}',queue_path),(f'authority/{pending_path.name}',pending_path),(f'authority/{handoff_path.name}',handoff_path),
 ('authority/latest_accepted/MODEL.json',prev_model)
]
if prev_receipt.is_file():inputs.append(('authority/latest_accepted/EXACT_ACCEPTANCE.json',prev_receipt))
if prev_holds.is_file():inputs.append(('authority/latest_accepted/HOLD_REGISTER.json',prev_holds))
prev_adjud=prev_dir/'HOLD_ADJUDICATION.json'
if prev_adjud.is_file():inputs.append(('authority/latest_accepted/HOLD_ADJUDICATION.json',prev_adjud))
inputs.extend([('source/current_candidate.json',candidate),('history/current_source_archive.zip',archive)])
pending_count=idx['authoredCounts']['pending'];reviewed=idx['authoredCounts']['reviewed'];version=int(queue_path.stem.rsplit('_',1)[1])
slug='-'.join(group['group'].split('-')).upper().replace('-','')
request_path=A/f'NEXT_{group["group"].upper().replace("-","_")}_REQUEST_{version}.txt'
out=A/f'DD_{group["group"].upper().replace("-","")}_Context_{version}.zip'
delivery_path=A/f'DD_{group["group"].upper().replace("-","")}_Context_{version}_DELIVERY.json'
request=f'''DIRECTOR REQUEST — {group['group']} — LIVE AUTHORITY {reviewed}/{pending_count}

Review exactly the next current pending identities: {', '.join(ids)}. The attached context packet includes the exact current index, catalog, queue, pending audit, handoff, latest accepted model/receipt/holds, and exact source candidate/archive. Current authority is {reviewed} reviewed/applied, {pending_count} pending, zero accepted-unapplied; complete reviewed standalone procedures: {queue['currentAuthority'].get('completeReviewedStandaloneProcedures','see queue')}. Use the attached live index and queue as authority; historical counts in older source files are superseded. Do not reopen feats, the completed 335-feat review, completed 16 spells, or any applied batch.

Return one complete proposed authored operational procedure per listed identity. Preserve each exact native card and all class-access rows. Resolve every original question explicitly, preserve original scenarios, question dispositions, and source/physical holds, and supply complete reversible full-state cases for every required source question and materially distinct new branch. Mark new local choices as spell-local authorship; do not promote them to global authority. Keep source facts, physical prerequisites, identities, and unsupported campaign examples held where absent. Preserve all provenance, resource, custody, timing, and failure state.

Do not execute supplied or historical programs, run the game, or change the canonical index/catalog. Return one clean ZIP with a complete exact member manifest and SHA-256 bindings plus a separate delivery JSON bound to the ZIP. Keep accepted=false and applied=false at {reviewed}/{pending_count}. No hidden or temporary archive members. Report exact counts for procedures, questions, cases/branches, events, reversible operations, validations, and holds. Preserve the attached source candidate/archive byte-exactly.
'''
request_path.write_text(request,encoding='utf-8',newline='\n')
inputs.append((f'request/{request_path.name}',request_path))
records=[]
for arc,p in inputs:
 b=p.read_bytes();records.append({'path':arc,'bytes':len(b),'sha256':sha(b),'sourcePath':p.relative_to(R).as_posix()})
manifest={'id':f'SPELL-DIRECTOR-CONTEXT-MANIFEST-{version}','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'authority':{'reviewed':reviewed,'pending':pending_count,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':queue['currentAuthority'].get('completeReviewedStandaloneProcedures')},'group':group['group'],'scope':ids,'members':records,'memberCount':len(records)}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for arc,p in inputs:z.write(p,arc)
 z.writestr('CONTEXT_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
blob=out.read_bytes()
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and len(z.namelist())==len(records)+1
 for rec in records:
  b=z.read(rec['path']);assert len(b)==rec['bytes'] and sha(b)==rec['sha256']
delivery={'id':f'SPELL-DIRECTOR-CONTEXT-DELIVERY-{version}','file':out.name,'bytes':len(blob),'sha256':sha(blob),'members':len(records)+1,'manifestBindings':len(records),'authority':manifest['authority'],'group':group['group'],'scope':ids,'requestBinding':next(x for x in records if x['path'].startswith('request/')),'candidate':bind(candidate),'archive':bind(archive),'accepted':False,'applied':False}
delivery_path.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(delivery,ensure_ascii=False,indent=2))
