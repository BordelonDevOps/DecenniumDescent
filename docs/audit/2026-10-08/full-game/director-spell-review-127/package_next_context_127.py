"""Fresh data-only outer wrappers for the next already prepared director conferences."""
from pathlib import Path
import json,zipfile,hashlib,datetime
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-127';R=G/'DescentReviewChanges/ReviewBible'
def sha(b):return hashlib.sha256(b).hexdigest()
def data(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
common={
 'accepted/DD_Time_Cast5_Accepted_127.zip':D/'DD_Time_Cast5_Accepted_127.zip',
 'accepted/TIME5_EXACT_ACCEPTANCE_127.json':D/'TIME5_EXACT_ACCEPTANCE_127.json',
 'accepted/TIME5_APPLICATION_127.json':D/'TIME5_APPLICATION_127.json',
 'accepted/TIME5_APPLICATION_VALIDATION_127.json':D/'TIME5_APPLICATION_VALIDATION_127.json',
 'accepted/BODY8_APPLICATION_127.json':D/'BODY8_APPLICATION_127.json',
 'accepted/BODY8_APPLICATION_VALIDATION_127.json':D/'BODY8_APPLICATION_VALIDATION_127.json',
 'accepted/TIME5_NATIVE_CARD_COMPARISON_127.json':D/'TIME5_NATIVE_CARD_COMPARISON_127.json',
 'current/authored_review_index.json':R/'data/public/spell_playtests/authored_review_index.json',
 'current/CURRENT_SPELL_QUEUE_127.json':A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_127.json',
 'current/APPLICATION_CHECKPOINT_127.json':A/'ACTIVE_AUTHORING_CHECKPOINT_ORDINARY_SPELL_REVIEW_127.json'
}
base_names=['MagicModifiers7','LifeMatter5','Information8','EyeJudgement1']
results=[]
for name in base_names:
 orig=A/f'DD_{name}_Director_Conference_126.zip';target=A/f'DD_{name}_Director_Conference_127.zip';assert not target.exists()
 payload={k:v.read_bytes() for k,v in common.items()};payload['prepared/'+orig.name]=orig.read_bytes()
 readme=f'''# {name} current director conference127

Open the complete prepared conference126 archive under prepared/ for the full original native records, questions, proposals, cases, source bindings and prior accepted context. That archive is exact historical input, not replaced or silently edited.

This outer wrapper supplies current accepted/applied authority: Body/Defense8 applied127 after independent126 acceptance, and Time/Cast5 accepted/applied127. Current authored index is610 reviewed /238 pending /334 standalone /173 scoped interfaces /0 accepted-unapplied. Old counts/status labels inside historical inputs are superseded only by these exact receipts. Transport6 is separately under director review and remains unaccepted here.

Time5 current accepted model includes case-only local corrections, all fully reversible and independently checked: book handling moves to the original Time Skip turn12.3 before departure18, so no ordinary voluntary event intervenes between return START24 and immediate Sigil Rewrite24.01; two Antimagic selection points use open air at7ft native range; the Contingency Fireball LOAD/release fixes the same visible body-surface origin. All five selected procedures, six shared clauses,22 question answers, native source/access and retained holds remain unchanged. All16 native endpoint cards match current accepted cards.16,561 final static data/source/mirror/cost checks pass. This is authored data, not engine or human/balance verification.

The owner explicitly directs continuing pending spells until accepted and then applying each accepted authored batch. Do not reopen335 feats, previous72 applied spells, Body8 or Time5. Preserve all source-content and implementation holds. This {name} packet is still pending authoring/exact review, and the included acceptance never promotes it automatically. Produce complete procedures and real native cases, including original scenario obligations or precise whole-case qualifications, and exact complete download/reconstruction evidence. Do not execute supplied programs or historical gameplay/authoring runners.
'''
 payload['README.md']=readme.encode();manifest={'id':name.upper()+'-DIRECTOR-CONFERENCE-127','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':k,'bytes':len(b),'sha256':sha(b)} for k,b in sorted(payload.items())]};payload['MANIFEST.json']=data(manifest)
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
  for k,b in payload.items():z.writestr(k,b)
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(payload)
  for row in manifest['files']:assert len(z.read(row['path']))==row['bytes'] and sha(z.read(row['path']))==row['sha256']
 result={'id':name+'-127','path':str(target),'bytes':target.stat().st_size,'sha256':sha(target.read_bytes()),'members':len(payload),'bindings':len(manifest['files']),'status':'PREPARED_NOT_SENT','currentCounts':{'appliedReviewed':610,'pending':238,'standalone':334,'acceptedUnapplied':0}}
 (D/(name.upper()+'_PACKET_127.json')).write_bytes(data(result));results.append(result)
print(json.dumps(results,indent=2))
