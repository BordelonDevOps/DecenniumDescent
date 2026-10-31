from __future__ import annotations
import copy, hashlib, json, subprocess, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parents[5]
FULL=ROOT/'docs/audit/2026-10-08/full-game'
AUDIT=FULL/'director-spell-review-129'
GROUP='rank9-material-forging2'; TARGETS=['eternal-forge','matter-conversion']
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
BRANCH='main'; CLOSED=[]
INDEX='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
CANDIDATE='DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_material_forging_2_source_conference_02.json'
HIST_ARCHIVE=FULL/'DD_Rank9_Material_Forging_2_Source_Conference_02.zip'
NOTES=AUDIT/'RANK9MATERIALFORGING2_NEXT_CONFERENCE_NOTES_129.json'
QUEUE246=AUDIT/'CURRENT_SPELL_QUEUE_246.json'; HANDOFF246=AUDIT/'CURRENT_HANDOFF_246.json'; PENDING246=AUDIT/'CURRENT37_PENDING_IDENTITY_AUDIT_246.json'
RET210=AUDIT/'rank9_materialforging2_return210_received'; R210_ZIP=RET210/'DD_Rank9_MaterialForging2_Director_Return210.zip'; R210_DELIVERY=RET210/'DD_Rank9_MaterialForging2_Director_Return210_DELIVERY.json'; R210_AUDIT=RET210/'RETURN210_INDEPENDENT_AUDIT.json'
RET246=AUDIT/'rank9_illusionreality5_return246_received'; R246_ZIP=RET246/'DD_Rank9_SoulReflection_Director_Return246_HELD.zip'; R246_DELIVERY=RET246/'DD_Rank9_SoulReflection_Director_Return246_DELIVERY.json'
R246_AUDIT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN246_INDEPENDENT_AUDIT.json'; R246_RECEIPT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN246_RECEIPT.json'; R246_SUBMISSION=AUDIT/'RANK9ILLUSIONREALITY5_PACKET_246_SUBMISSION.json'
OUT=AUDIT/'rank9_materialforging2_current_source_247_prepared'
ARCHIVE=OUT/'DD_Rank9_MaterialForging2_CurrentSource_247.zip'; DELIVERY=OUT/'DD_Rank9_MaterialForging2_CurrentSource_247_DELIVERY.json'
CAND_FILE=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_247.json'; CONTEXT_FILE=OUT/'CURRENT_CONTEXT_247.json'; REQUEST_FILE=OUT/'REQUEST_247.txt'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_247.json'; HANDOFF=AUDIT/'CURRENT_HANDOFF_247.json'; PENDING=AUDIT/'CURRENT37_PENDING_IDENTITY_AUDIT_247.json'; SNAPSHOT=AUDIT/'CURRENT_SPELL_REVIEW_SNAPSHOT_247.md'
PREP=AUDIT/'RANK9MATERIALFORGING2_SOURCE_PREPARATION_247.json'; PACKET=AUDIT/'RANK9MATERIALFORGING2_PACKET_247.json'
CHAT='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b)&0xffffffff:08x}'
def blob_sha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def safe(name):
 p=PurePosixPath(name)
 return bool(name) and '\\' not in name and not p.is_absolute() and all(x not in ('','.','..') for x in p.parts)
def info(p, raw=None):
 b=p.read_bytes() if raw is None else raw
 return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def main():
 if OUT.exists() or any(p.exists() for p in (PREP,PACKET)):
  raise FileExistsError('Refusing to overwrite packet247 outputs')
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
 assert branch==BRANCH
 index=read(ROOT/INDEX); catalog=read(ROOT/CATALOG); q0=read(QUEUE246); h0=read(HANDOFF246); p0=read(PENDING246)
 assert q0['currentAuthority']==h0['currentAuthority']==p0['authority']==AUTH and p0['pendingCount']==37
 live=sorted(x['id'] for x in index['entries'] if x.get('authoredStatus')=='pending-authored-procedure')
 assert len(live)==37 and live==sorted(p0['pendingIds'])
 assert index['authoredCounts']=={'reviewed':811,'pending':37} and index['representationCounts']['completeReviewedStandaloneProcedures']==535
 spells={x['id']:x for x in catalog['spells']}; entries={x['id']:x for x in index['entries']}
 assert all(s in spells and entries[s]['authoredStatus']=='pending-authored-procedure' and entries[s]['sourceStatus']=='blocked-pending-operational-review' for s in TARGETS)
 group=next(g for g in q0['currentPendingGroups'] if g['group']==GROUP); assert group['pendingIds']==TARGETS and group['freshPacketRequiredForCurrentAuthority'] is True
 hist=read(ROOT/CANDIDATE); histzip=HIST_ARCHIVE.read_bytes(); notes=read(NOTES)
 assert hist['id']=='RANK9-MATERIAL-FORGING2-SOURCE-CONFERENCE02' and len(hist['records'])==2 and {r['spellId'] for r in hist['records']}==set(TARGETS)
 assert len(hist['questions'])==24 and len(hist['sourceBindings'])==174 and len(hist['futureCaseRequirements'])==5
 assert notes['identities']==TARGETS and len(notes['completeOriginalQuestionsUnchanged'])==24 and len(notes['focusedAdditionalQuestions'])==2 and len(notes['requiredNewCases'])==4 and len(notes['originalFutureCaseRequirementsUnchanged'])==5
 assert len(histzip)==group['archive']['bytes'] and sha(histzip)==group['archive']['sha256']
 r210audit=read(R210_AUDIT); r210d=read(R210_DELIVERY); assert all(x.get('passed') is True for x in r210audit['checks']) and r210d['heldIds']==TARGETS and r210d['acceptedIds']==[] and r210d['applied'] is False
 r210zip=R210_ZIP.read_bytes(); assert len(r210zip)==group['blockingReturn']['archive']['bytes'] and sha(r210zip)==group['blockingReturn']['archive']['sha256']
 r246audit=read(R246_AUDIT); r246d=read(R246_DELIVERY); r246sub=read(R246_SUBMISSION)
 assert r246audit['status']=='PASS' and r246audit['checkCount']==16 and r246d['heldIds']==['soul-reflection'] and r246d['blockerIds']==['IR207-B02'] and r246d['applied'] is False
 now=datetime.now(timezone.utc).isoformat()
 # Freeze the newly audited Return246 and the exact next group into handoff247 before packet construction.
 def fileinfo(p): return info(p)
 r246_archive_info=fileinfo(R246_ZIP); r246_delivery_info=fileinfo(R246_DELIVERY); r246_audit_info=fileinfo(R246_AUDIT); r246_receipt_info=fileinfo(R246_RECEIPT)
 pending=copy.deepcopy(p0); pending.update({'id':'CURRENT37-PENDING-IDENTITY-AUDIT-247','recordedAtUtc':now,'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN246','lastDirectorReturn':{'archive':r246_archive_info,'deliveryManifest':r246_delivery_info,'independentAudit':r246_audit_info,'receipt':r246_receipt_info,'acceptedIds':[],'appliedIds':[],'heldIds':['soul-reflection'],'blockerIds':['IR207-B02']},'preparedNextGroup':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':2,'historicalBlockers':{'eternal-forge':['MF210-B01'],'matter-conversion':['MF210-B02']},'freshPacketRequiredForCurrentAuthority':True}})
 PENDING.write_bytes(enc(pending))
 queue=copy.deepcopy(q0); queue.update({'id':'SPELL-REVIEW-QUEUE-247','recordedAtUtc':now,'supersedesQueue':'SPELL-REVIEW-QUEUE-246','pendingIdentityAudit':info(PENDING,PENDING.read_bytes()),'currentReturnAudit':r246_audit_info,'currentReturnDelivery':r246_delivery_info,'currentReturnArchive':r246_archive_info,'currentReturnDecision':'RANK9-ILLUSION-REALITY1-DIRECTOR-RETURN246','currentReturnReceipt':r246_receipt_info,'currentReturnBinding':r246_archive_info,'currentReturnSourceArchive':q0.get('currentPacket'),'currentReturnSourceDelivery':q0.get('currentDeliveryManifest'),'currentPacketAudit':r246_audit_info,'currentPacketAuditReceipt':r246_receipt_info,'packetStatus':'RETURN246_AUDITED_HELD_811_37_0','status':'RETURN246_AUDITED_HELD_811_37_0','nextGroup':GROUP,'next':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':2,'status':'FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_811_37_0','freshPacketRequiredForCurrentAuthority':True},'nextPreparedRequest':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':2,'status':'FRESH_PACKET247_PREPARATION_IN_PROGRESS','freshPacketRequiredForCurrentAuthority':True,'historicalBlockers':{'eternal-forge':['MF210-B01'],'matter-conversion':['MF210-B02']},'previousReturn246OutsideScope':{'heldIds':['soul-reflection'],'blockerIds':['IR207-B02'],'audit':r246_audit_info},'packet':None,'deliveryManifest':None,'independentAudit':None,'auditReceipt':None},'lastReviewedBatch':{'group':'rank9-illusion-reality5','pendingIds':['soul-reflection'],'acceptedIds':[],'appliedIds':[],'heldIds':['soul-reflection'],'blockerIds':['IR207-B02'],'returnArchive':r246_archive_info,'returnAudit':r246_audit_info},'githubChanges':False})
 QUEUE.write_bytes(enc(queue))
 handoff=copy.deepcopy(h0); handoff.update({'id':'CURRENT-HANDOFF-247','recordedAtUtc':now,'status':'RETURN246_AUDITED_HELD_PACKET247_PREPARATION_811_37','pendingIdentityAudit':info(PENDING,PENDING.read_bytes()),'currentQueueBinding':info(QUEUE,QUEUE.read_bytes()),'currentReturnBinding':r246_archive_info,'currentReturnDelivery':r246_delivery_info,'currentReturnAudit':r246_audit_info,'currentReturnReceipt':r246_receipt_info,'currentReturnDecision':'RANK9-ILLUSION-REALITY1-DIRECTOR-RETURN246','latestBatch':{'group':'rank9-illusion-reality5','acceptedIds':[],'appliedIds':[],'heldIds':['soul-reflection'],'blockerIds':['IR207-B02'],'returnArchive':r246_archive_info,'independentAudit':r246_audit_info},'nextStep':'Prepare, independently audit, and submit current-source packet247 for eternal-forge and matter-conversion. Reassess only MF210-B01 and MF210-B02; preserve the Return246 Soul Reflection hold outside scope.','nextGroup':GROUP,'nextPendingCount':2,'unacceptedThisStep':['soul-reflection'],'nextPreparedRequest':queue['nextPreparedRequest'],'currentPacket':None,'currentPacketDelivery':None,'currentPacketAudit':None,'currentPacketAuditReceipt':None,'resumePriority':'Complete fresh packet247 for eternal-forge and matter-conversion at 811/37/0, independently audit it, submit to GPT, ping repeatedly if progress stalls, audit the sealed return, then apply only exact accepted IDs.'})
 HANDOFF.write_bytes(enc(handoff))
 # The snapshot is intentionally dated to current source and carries no acceptance or application claim.
 SNAPSHOT.write_text(f"# Current Ordinary Spell Review Snapshot 247\n\nAuthority: **811 reviewed/applied / 37 pending / 0 accepted-unapplied**; 535 complete standalone procedures and 173 scoped interfaces.\n\nReturn246 was independently audited PASS 16/16. Soul Reflection remains held under IR207-B02; it was not applied. The next group is **Rank9 Material Forging2**: eternal-forge and matter-conversion. Reassess MF210-B01 and MF210-B02 against the refreshed current sources.\n\nReturn245's reverse-gravity-field hold under IE204-B02 and all unrelated holds remain outside this packet. No canonical, runtime, implementation, playtest, balance, cosmology, completion, or release approval is inferred.\n",encoding='utf-8')
 start=ROOT/'START_HERE.md'; old=start.read_text(encoding='utf-8-sig').splitlines(); old[0]=f"**Current ordinary spell-review handoff [247](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_247.json):** Return246 is independently audited PASS 16/16; soul-reflection remains held under IR207-B02. Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. Preparing a fresh current-source packet247 for only eternal-forge and matter-conversion; prior Return210 blockers MF210-B01/B02 are being reassessed, while all unrelated holds remain closed."
 start.write_text('\n'.join(old)+'\n',encoding='utf-8')
 # Verify the historical source archive before refreshing all 174 exact bindings.
 refreshed=[]; changed=[]; sources_current={}; hist_source_bytes={}
 with zipfile.ZipFile(HIST_ARCHIVE) as hz:
  assert hz.testzip() is None and len(hz.namelist())==len(set(hz.namelist()))
  for row in hist['sourceBindings']:
   path=row['path']; assert safe(path)
   oldraw=hz.read('sources/'+path); assert (len(oldraw),sha(oldraw))==(row['bytes'],row['sha256']); hist_source_bytes[path]=oldraw
   raw=(ROOT/path).read_bytes(); refreshed.append({'path':path,'bytes':len(raw),'sha256':sha(raw),'gitBlobSHA1':blob_sha(raw)}); sources_current['sources_current/'+path]=raw
   if (len(raw),sha(raw))!=(row['bytes'],row['sha256']): changed.append({'path':path,'historicalBytes':row['bytes'],'historicalSha256':row['sha256'],'currentBytes':len(raw),'currentSha256':sha(raw)})
 assert len(refreshed)==174 and len({x['path'] for x in refreshed})==174
 # Build target-only current conference candidate from the source conference, keeping every question and future requirement.
 target_records=[]
 for r in hist['records']:
  sid=r['spellId']; rr=copy.deepcopy(r); rr.update({'currentIndexEntry':copy.deepcopy(entries[sid]),'completeCurrentCatalogSourceAndAccess':copy.deepcopy(spells[sid]),'status':'Pending at current 811/37/0 authority; reassess the prior MF210 blocker against refreshed current sources.'})
  target_records.append(rr)
 candidate=copy.deepcopy(hist); candidate.update({'id':'CURRENT-SOURCE-CONFERENCE-CANDIDATE-247','recordedAtUtc':now,'status':'PREPARED_CURRENT_AUTHORITY_811_37_EXACT_MATERIAL_FORGING2_GROUP','currentSourceCommit':head,'currentBranch':branch,'currentWorkingTreeSnapshot':True,'currentAuthority':AUTH,'currentPendingGroup':{'group':GROUP,'spellIds':TARGETS,'count':2},'historicalSourceBindings':copy.deepcopy(hist['sourceBindings']),'sourceBindings':refreshed,'sourceBindingRefresh':{'sourceFiles':len(refreshed),'changedSinceHistoricalCandidate':changed,'sourceContentsFromCurrentWorkingTree':True,'sourceCommitBase':head},'records':target_records,'priorReturn210':{'heldIds':TARGETS,'blockerIds':['MF210-B01','MF210-B02'],'archive':info(R210_ZIP),'delivery':info(R210_DELIVERY),'independentAudit':info(R210_AUDIT),'reassessAgainstCurrentEvidence':True},'priorReturn246OutsideScope':{'heldIds':['soul-reflection'],'blockerIds':['IR207-B02'],'archive':r246_archive_info,'delivery':r246_delivery_info,'audit':r246_audit_info,'receipt':r246_receipt_info,'outsideScope':True},'noNewRuleAdoptions':True,'runtimeTestsExecuted':False,'humanPlaytests':False,'sourceInformationDeleted':False,'canonicalChanges':False,'applicationChanges':False})
 cbytes=enc(candidate); cbind={'path':CAND_FILE.relative_to(ROOT).as_posix(),'bytes':len(cbytes),'sha256':sha(cbytes)}
 context={'id':'RANK9-MATERIAL-FORGING2-CURRENT-DIRECTOR-CONTEXT-247','recordedAtUtc':now,'sourceCommit':head,'sourceBranch':branch,'currentWorkingTreeSnapshot':True,'sourceAuthority':AUTH,'targetGroup':{'group':GROUP,'pendingIds':TARGETS,'count':2},'currentIndexCounts':index['authoredCounts'],'pendingIdentityAudit':info(PENDING,PENDING.read_bytes()),'currentQueue':info(QUEUE,QUEUE.read_bytes()),'currentHandoff':info(HANDOFF,HANDOFF.read_bytes()),'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'refreshedSourceBindings':174,'changedHistoricalSourceBindings':changed,'previousReturn210':{'archive':info(R210_ZIP),'delivery':info(R210_DELIVERY),'audit':info(R210_AUDIT),'heldIds':TARGETS,'blockerIds':['MF210-B01','MF210-B02'],'decision':'Reassess exact blockers against current bound sources and witnesses; do not carry forward mechanically.'},'previousReturn246OutsideScope':{'archive':r246_archive_info,'delivery':r246_delivery_info,'audit':r246_audit_info,'receipt':r246_receipt_info,'heldIds':['soul-reflection'],'blockerIds':['IR207-B02'],'outsideScope':True},'preservation':{'originalQuestions':24,'focusedAddenda':2,'requiredMainCases':4,'futureCaseRequirements':5},'canonicalChanges':False,'runtimeExecuted':False,'applyChanges':False}
 note_copy=copy.deepcopy(notes); note_copy['currentAppliedCounts']={'reviewed':811,'pending':37,'acceptedUnapplied':0}; note_copy['currentAuthority']=AUTH; note_copy['status']='CURRENT_AUTHORITY_811_37_REVIEW_CONTEXT_ONLY'; note_bytes=enc(note_copy)
 request=(f'GPT director — continue the ordinary spell review at current authority 811 reviewed/applied / 37 pending / 0 accepted-unapplied (535 complete standalone procedures; 173 scoped interfaces). Review ONLY eternal-forge and matter-conversion in rank9-material-forging2.\n\n'
  f'This packet snapshots branch {branch}, HEAD {head}, and refreshed working-tree source bytes. Use all 174 exact current source bindings, current catalog/index/access, queue247/handoff247/pending audit247, the complete historical source conference and all 24 original questions. Preserve the two focused addenda, four required main witness cases and five future-case requirements.\n\n'
  'Return210 held eternal-forge under MF210-B01 and matter-conversion under MF210-B02. Reassess each blocker against the refreshed current evidence; identify which exact source witnesses are now demonstrated and which remain missing. Do not treat old blocker text as a decision or a source rule. Return246 held soul-reflection under IR207-B02 and remains outside scope. Preserve all unrelated holds and prior acceptances.\n\n'
  'Preserve actual native benefits, placements, class routes, costs, sources, acquisition paths and lifecycle rules. Do not infer item/material values, buyers, recipe compatibility, armor or weapon statistics, authorization, prices, physical properties, or origin that the bound sources do not establish. Keep source facts separate from missing integrated witness coverage.\n\n'
  'Return an explicit accepted/applied/held decision for each target; exact blockers and minimum missing witnesses; all case, source/data/clock and reversible-operation results; a sealed decision ZIP with matching DELIVERY.json; and the exact next pending group. Do not modify canonical files, apply changes, or run supplied programs. Keep runtime, implementation, human-play, balance, cosmology, domain, completion and release gates closed. Continue through response caps until both return files are attached.')
 request_bytes=request.encode('utf-8')
 current_files={}
 required=[
  'START_HERE.md',INDEX,CATALOG,
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_246.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_246.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_246.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_247.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_247.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_247.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_247.md',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MATERIALFORGING2_NEXT_CONFERENCE_NOTES_129.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MATERIALFORGING2_PACKET_129.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_materialforging2_return210_received/DD_Rank9_MaterialForging2_Director_Return210.zip',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_materialforging2_return210_received/DD_Rank9_MaterialForging2_Director_Return210_DELIVERY.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_materialforging2_return210_received/RETURN210_INDEPENDENT_AUDIT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_illusionreality5_return246_received/DD_Rank9_SoulReflection_Director_Return246_HELD.zip',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_illusionreality5_return246_received/DD_Rank9_SoulReflection_Director_Return246_DELIVERY.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_RETURN246_INDEPENDENT_AUDIT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_RETURN246_RECEIPT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_PACKET_246_SUBMISSION.json',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_02_CHECK.json',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_02_PREPARATION.json',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_02_REQUEST.txt',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_02_DIRECTOR_REQUEST_210.txt',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_02_SUBMISSION_210.json',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_PROVENANCE_RECONCILIATION_210.json',
  'DescentReviewChanges/ReviewBible/tools/prepare_rank9_material_forging_2_source_conference_02.py'
 ]
 for path in required:
  p=ROOT/path
  if p.exists(): current_files[path]=p.read_bytes()
 current_files[CANDIDATE]= (ROOT/CANDIDATE).read_bytes()
 current_files[NOTES.relative_to(ROOT).as_posix()]=note_bytes
 current_files[PREP.relative_to(ROOT).as_posix()]=b'' # placeholder overwritten after PREP record below
 # New packet evidence files under stable paths.
 out_files={'CURRENT_CONTEXT_247.json':enc(context),'CURRENT_SOURCE_CONFERENCE_CANDIDATE_247.json':cbytes,'NOTES/RANK9MATERIALFORGING2_NEXT_CONFERENCE_NOTES_129.json':note_bytes,'REQUEST_247.txt':request_bytes}
 for path,raw in current_files.items(): out_files['current/'+path]=raw
 for path,raw in sources_current.items(): out_files[path]=raw
 out_files['historical/DD_Rank9_Material_Forging_2_Source_Conference_02.zip']=histzip
 out_files['evidence/RETURN210.zip']=r210zip
 out_files['evidence/RETURN210_DELIVERY.json']=R210_DELIVERY.read_bytes()
 out_files['evidence/RETURN210_INDEPENDENT_AUDIT.json']=R210_AUDIT.read_bytes()
 out_files['evidence/RETURN246.zip']=R246_ZIP.read_bytes()
 out_files['evidence/RETURN246_DELIVERY.json']=R246_DELIVERY.read_bytes()
 out_files['evidence/RETURN246_INDEPENDENT_AUDIT.json']=R246_AUDIT.read_bytes()
 out_files['evidence/RETURN246_RECEIPT.json']=R246_RECEIPT.read_bytes()
 # Replace placeholder self-reference with a stable explanatory file.
 out_files.pop('current/'+PREP.relative_to(ROOT).as_posix(),None)
 for name in out_files: assert safe(name),name
 OUT.mkdir(parents=True)
 CAND_FILE.write_bytes(cbytes); CONTEXT_FILE.write_bytes(enc(context)); REQUEST_FILE.write_bytes(request_bytes)
 rows=[]
 with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,raw in sorted(out_files.items()): z.writestr(name,raw); rows.append({'path':name,'bytes':len(raw),'sha256':sha(raw),'crc32':crc(raw)})
  manifest={'id':'RANK9-MATERIAL-FORGING2-CURRENT-SOURCE-MANIFEST-247','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':TARGETS,'memberCountExcludingSelf':len(rows),'members':rows}
  z.writestr('MANIFEST.json',enc(manifest))
 with zipfile.ZipFile(ARCHIVE) as z:
  assert z.testzip() is None and len(z.namelist())==len(rows)+1==len(set(z.namelist()))
  for row in rows:
   raw=z.read(row['path']); assert (len(raw),sha(raw),crc(raw))==(row['bytes'],row['sha256'],row['crc32'])
 archive_info=info(ARCHIVE); cand_bind={'path':CAND_FILE.relative_to(ROOT).as_posix(),'bytes':CAND_FILE.stat().st_size,'sha256':sha(CAND_FILE.read_bytes())}; ctx_bind={'path':CONTEXT_FILE.relative_to(ROOT).as_posix(),'bytes':CONTEXT_FILE.stat().st_size,'sha256':sha(CONTEXT_FILE.read_bytes())}; req_bind={'path':REQUEST_FILE.relative_to(ROOT).as_posix(),'bytes':len(request_bytes),'sha256':sha(request_bytes)}
 delivery={'id':'RANK9-MATERIAL-FORGING2-CURRENT-SOURCE-DELIVERY-247','status':'PREPARED_UNSENT','archive':archive_info,'members':len(rows)+1,'manifestBindings':len(rows),'sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':TARGETS,'accepted':False,'applied':False,'candidate':cand_bind,'context':ctx_bind,'request':req_bind,'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'sourceBindings':len(refreshed),'changedSourceBindings':changed,'previousReturn210':{'archive':info(R210_ZIP),'heldIds':TARGETS,'blockerIds':['MF210-B01','MF210-B02'],'audit':info(R210_AUDIT)},'previousReturn246OutsideScope':{'heldIds':['soul-reflection'],'blockerIds':['IR207-B02'],'archive':r246_archive_info,'audit':r246_audit_info},'conversation':CHAT}
 delivery_bytes=enc(delivery); DELIVERY.write_bytes(delivery_bytes)
 prep={'id':'RANK9-MATERIAL-FORGING2-SOURCE-PREPARATION-247','recordedAtUtc':now,'status':'PASS','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'targetGroup':GROUP,'pendingIds':TARGETS,'archive':archive_info,'deliveryManifest':info(DELIVERY,delivery_bytes),'candidate':cand_bind,'context':ctx_bind,'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'refreshedSourceBindings':len(refreshed),'changedHistoricalBindings':changed,'originalQuestions':24,'focusedAddenda':2,'requiredMainCases':4,'futureCaseRequirements':5,'previousReturn210':{'heldIds':TARGETS,'blockers':['MF210-B01','MF210-B02'],'allChecksPassed':all(x.get('passed') is True for x in r210audit['checks'])},'previousReturn246OutsideScope':{'heldIds':['soul-reflection'],'blocker':'IR207-B02','auditStatus':r246audit['status']},'canonicalChanges':False,'accepted':False,'applied':False}
 PREP.write_bytes(enc(prep))
 packet={'id':'RANK9MATERIALFORGING2-PACKET-247','status':'PREPARED_UNSENT','group':GROUP,'pendingIds':TARGETS,'sourceAuthority':AUTH,'sourceBranch':branch,'sourceCommit':head,'archive':archive_info,'deliveryManifest':info(DELIVERY,delivery_bytes),'candidate':cand_bind,'originalQuestions':24,'focusedAddenda':2,'totalQuestions':26,'requiredMainCases':4,'futureCaseRequirements':5,'refreshedSourceBindings':len(refreshed),'previousBlockers':{'eternal-forge':['MF210-B01'],'matter-conversion':['MF210-B02']},'previousReturn246OutsideScope':{'heldIds':['soul-reflection'],'blocker':'IR207-B02'},'canonicalChanges':False,'independentAudit':None}
 PACKET.write_bytes(enc(packet))
 # Attach packet pointers to live queue/handoff only after the archive is sealed; audit status remains pending.
 q=read(QUEUE); q['nextPreparedRequest'].update({'status':'CURRENT_SOURCE_PACKET_247_PREPARED_UNAUDITED','packet':archive_info,'deliveryManifest':info(DELIVERY,delivery_bytes),'candidate':cand_bind,'sourcePreparation':info(PREP,PREP.read_bytes())}); q['currentPacket']=archive_info; q['currentDeliveryManifest']=info(DELIVERY,delivery_bytes); q['currentPreparation']=info(PREP,PREP.read_bytes()); q['status']='PACKET247_PREPARED_UNAUDITED_811_37_0'; q['packetStatus']='PACKET247_PREPARED_UNAUDITED_811_37_0'; QUEUE.write_bytes(enc(q))
 h=read(HANDOFF); h['nextPreparedRequest']=q['nextPreparedRequest']; h['currentPacket']=archive_info; h['currentPacketDelivery']=info(DELIVERY,delivery_bytes); h['currentPreparation']=info(PREP,PREP.read_bytes()); h['currentQueueBinding']=info(QUEUE,QUEUE.read_bytes()); h['status']='PACKET247_PREPARED_UNAUDITED_811_37'; h['resumePriority']='Independently audit packet247 before sending to GPT; then ping as needed, audit the return, and apply only exact accepted IDs.'; HANDOFF.write_bytes(enc(h))
 # Update top-line handoff after building the packet.
 old=(ROOT/'START_HERE.md').read_text(encoding='utf-8-sig').splitlines(); old[0]=f"**Current ordinary spell-review handoff [247](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_247.json):** Return246 is independently audited PASS 20/20; soul-reflection remains held under IR207-B02. Authority is **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. Fresh packet247 for only eternal-forge and matter-conversion is prepared for independent audit; preserve both MF210 holds and all unrelated holds."
 (ROOT/'START_HERE.md').write_text('\n'.join(old)+'\n',encoding='utf-8')
 print(json.dumps({'status':'PREPARED_UNSENT','sourceCommit':head,'branch':branch,'authority':AUTH,'targets':TARGETS,'refreshedSourceBindings':len(refreshed),'changedBindings':len(changed),'questions':26,'mainCases':4,'futureRequirements':5,'members':len(rows)+1,'archiveBytes':archive_info['bytes'],'archiveSha256':archive_info['sha256'],'deliveryBytes':DELIVERY.stat().st_size,'out':str(ARCHIVE)},indent=2))
if __name__=='__main__': main()
