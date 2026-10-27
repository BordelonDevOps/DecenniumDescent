from __future__ import annotations
import copy, hashlib, json, subprocess, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
FULL=ROOT/'docs/audit/2026-10-08/full-game'
GROUP='rank9-illusion-reality5'
IDS=['supreme-illusion','mirrored-world','ethereal-disjunction','illusory-reality','soul-reflection']
AUTH={'reviewedApplied':798,'pending':50,'acceptedUnapplied':0,'completeStandaloneProcedures':522,'scopedInterfaces':173}
BRANCH='codex/ordinary-spell-review-complete'
CANDIDATE='DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_illusion_reality_5_source_conference_01.json'
ARCHIVE=FULL/'DD_Rank9_Illusion_Reality_5_Source_Conference_01.zip'
NOTES=AUDIT/'RANK9ILLUSIONREALITY5_NEXT_CONFERENCE_NOTES_129.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_205.json'; PENDING=AUDIT/'CURRENT50_PENDING_IDENTITY_AUDIT_205.json'; HANDOFF=AUDIT/'CURRENT_HANDOFF_205.json'
INDEX='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
OUT=AUDIT/'rank9_illusionreality5_current_source_206_prepared'
PACKET=AUDIT/'RANK9ILLUSIONREALITY5_PACKET_206.json'; PREP=AUDIT/'RANK9ILLUSIONREALITY5_SOURCE_PREPARATION_206.json'
QUEUE_OUT=AUDIT/'CURRENT_SPELL_QUEUE_206.json'; PENDING_OUT=AUDIT/'CURRENT50_PENDING_IDENTITY_AUDIT_206.json'; HANDOFF_OUT=AUDIT/'CURRENT_HANDOFF_206.json'
CHAT='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
def sha(b): return hashlib.sha256(b).hexdigest()
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def git_blob(commit,path): return subprocess.check_output(['git','cat-file','blob',f'{commit}:{path}'],cwd=ROOT)
def blobid(commit,path): return subprocess.check_output(['git','rev-parse',f'{commit}:{path}'],cwd=ROOT,text=True).strip()
def read(b): return json.loads(b.decode('utf-8-sig'))
def bind(path,b): return {'path':path,'bytes':len(b),'sha256':sha(b)}
def safe(name):
 p=PurePosixPath(name)
 return bool(name) and '\\' not in name and not p.is_absolute() and all(part not in ('','.','..') and not part.startswith('.') for part in p.parts)
def main():
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
 assert branch==BRANCH
 remote=subprocess.check_output(['git','ls-remote','origin',f'refs/heads/{branch}'],cwd=ROOT,text=True).split()
 assert remote and remote[0]==commit,(commit,remote)
 assert not OUT.exists() and not any(p.exists() for p in (PACKET,PREP,QUEUE_OUT,PENDING_OUT,HANDOFF_OUT))
 queue,pending,handoff,index,catalog=[read(git_blob(commit,p)) for p in (QUEUE.relative_to(ROOT).as_posix(),PENDING.relative_to(ROOT).as_posix(),HANDOFF.relative_to(ROOT).as_posix(),INDEX,CATALOG)]
 assert queue['nextGroup']==handoff['nextGroup']==GROUP
 assert queue['currentAuthority']==handoff['currentAuthority']==AUTH
 assert index['authoredCounts']=={'reviewed':798,'pending':50}
 assert index['representationCounts']['completeReviewedStandaloneProcedures']==522
 assert pending['pendingCount']==queue['pendingCount']==50 and set(IDS)<=set(pending['pendingIds'])
 target=queue['nextPreparedRequest']; assert target['group']==GROUP and target['pendingIds']==IDS and target['freshPacketRequiredForCurrentAuthority'] is True
 candidate_raw=git_blob(commit,CANDIDATE); archive_raw=ARCHIVE.read_bytes(); old_notes_raw=git_blob(commit,NOTES.relative_to(ROOT).as_posix())
 assert len(candidate_raw)==target['candidate']['bytes'] and sha(candidate_raw)==target['candidate']['sha256']
 assert len(archive_raw)==target['archive']['bytes'] and sha(archive_raw)==target['archive']['sha256']
 hist=read(candidate_raw); old_notes=read(old_notes_raw)
 assert [r['spellId'] for r in hist['records']]==IDS and len(hist['sourceBindings'])==157
 assert len(hist['questions'])==31 and len(old_notes['focusedAdditionalQuestions'])==2 and len(old_notes['requiredNewCases'])==10
 entries={e['id']:e for e in index['entries']}; cards={s['id']:s for s in catalog['spells']}
 for sid in IDS:
  assert sid in entries and entries[sid]['authoredStatus']=='pending-authored-procedure' and entries[sid]['sourceStatus']=='blocked-pending-operational-review'
  assert sid in cards
 historical_sources={}
 with zipfile.ZipFile(ARCHIVE) as oldz:
  assert oldz.testzip() is None and len(oldz.namelist())==len(set(oldz.namelist()))
  for row in hist['sourceBindings']:
   raw=oldz.read('sources/'+row['path'])
   assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
   historical_sources[row['path']]=raw
 refreshed=[]; changed=[]; current_sources={}
 for row in hist['sourceBindings']:
  path=row['path']; assert safe(path)
  raw=git_blob(commit,path); r={**bind(path,raw),'gitBlobSHA1':blobid(commit,path)}
  refreshed.append(r); current_sources['sources_current/'+path]=raw
  if raw!=historical_sources[path]: changed.append({'path':path,'historicalBytes':len(historical_sources[path]),'historicalSha256':sha(historical_sources[path]),'currentBytes':len(raw),'currentSha256':sha(raw)})
 assert len(refreshed)==157 and len({r['path'] for r in refreshed})==157
 current=copy.deepcopy(hist)
 current['historicalSourceBindings']=copy.deepcopy(hist['sourceBindings']); current['sourceBindings']=refreshed
 current['currentSourceCommit']=commit; current['currentBranch']=branch; current['currentAuthority']=AUTH
 current['currentPendingGroup']={'group':GROUP,'spellIds':IDS,'count':5}
 current['historicalCandidateBinding']=bind(CANDIDATE,candidate_raw)
 current['historicalSourceArchiveBinding']=bind(ARCHIVE.relative_to(ROOT).as_posix(),archive_raw)
 current['sourceBindingRefresh']={'sourceFiles':len(refreshed),'changedSinceHistoricalCandidate':changed,'sourceContentsFromGitCommit':commit,'allSourceBindingsRefreshed':True}
 current['countsUnchanged']={'reviewed':798,'pending':50,'acceptedUnapplied':0,'completeStandaloneProcedures':522}
 current['status']='CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_798_REVIEWED_50_PENDING'
 current['id']='RANK9-ILLUSION-REALITY5-CURRENT-SOURCE-CONTEXT-206'
 current['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
 for r in current['records']:
  sid=r['spellId']; r['historicalIndexEntry']=copy.deepcopy(r.get('currentIndexEntry')); r['currentIndexEntry']=copy.deepcopy(entries[sid]); r['completeCurrentCatalogSourceAndAccess']=copy.deepcopy(cards[sid])
 current_raw=enc(current)
 notes=copy.deepcopy(old_notes); notes.update({'id':'RANK9ILLUSIONREALITY5-INDEPENDENT-CONFERENCE-206','status':'CURRENT_SOURCE_PACKET_PREPARED_UNSENT_NOT_ACCEPTED','recordedAtUtc':current['recordedAtUtc'],'sourceCommit':commit,'sourceBranch':branch,'currentAppliedCounts':{'reviewed':798,'pending':50,'acceptedUnapplied':0,'completeStandaloneProcedures':522},'sourceChecks':[{'path':x['path'],'historicalExact':True,'currentCommit':commit,'currentSha256':x['sha256']} for x in refreshed],'scope':'Preparation only. The exact current 798/50 authority supersedes historical counts. Preserve all original questions and added questions/cases unchanged. No new rule adopted; runtime, implementation, human play, balance, cosmology, domain closure, completion, or release is not claimed.'})
 notes_raw=enc(notes)
 paths=[INDEX,CATALOG,QUEUE.relative_to(ROOT).as_posix(),PENDING.relative_to(ROOT).as_posix(),HANDOFF.relative_to(ROOT).as_posix(),
 'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_RETURN205_INDEPENDENT_AUDIT.json',
 'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_APPLICATION_205.json',
 'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_EXACT_ACCEPTANCE_205.json',
 'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_APPLICATION_VALIDATION_205.json',
 'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_RETURN205_RECEIPT.json',
 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9impactexile4_reviewed_205/MODEL.json',
 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9impactexile4_reviewed_205/STANDALONE_PROCEDURES.md',
 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9impactexile4_reviewed_205/CANDIDATE_PACKAGE_MANIFEST.json']
 current_files={'current/'+p:git_blob(commit,p) for p in paths}
 current_context={'id':'RANK9-ILLUSION-REALITY5-CURRENT-DIRECTOR-CONTEXT-206','recordedAtUtc':current['recordedAtUtc'],'sourceCommit':commit,'sourceBranch':branch,'sourceAuthority':AUTH,'targetGroup':{'group':GROUP,'pendingIds':IDS,'count':5},'currentIndexCounts':index['authoredCounts'],'pendingIdentityAudit':pending['id'],'currentQueue':queue['id'],'historicalCandidateBinding':bind(CANDIDATE,candidate_raw),'historicalArchiveBinding':bind(ARCHIVE.relative_to(ROOT).as_posix(),archive_raw),'sourceRefresh':{'sourceFileCount':len(refreshed),'changedSinceHistoricalCandidate':changed},'latestAppliedBatch':{'reviewId':'RANK9-IMPACTEXILE4-EXACT-AUTHORED-ACCEPTANCE-205','acceptedIds':['eternal-anvil','transmute-flesh-to-energy','planar-collapse'],'unacceptedIds':['reverse-gravity-field'],'blocker':'IE204-B02','scope':'Three exact static authored procedures are applied. Reverse Gravity Field stays pending because crate durability and rated tether/anchor strength are missing.'},'scopeBoundary':'Do not reopen feats, the completed 16, or completed spell batches. Keep all remaining pending IDs and their evidence holds. Current runtime, source/access, human-play, balance, cosmology, domain closure, and release gates remain unapproved.'}
 request=(f'GPT director — review exactly these five current pending ordinary spells: {", ".join(IDS)}.\n\nSource branch and commit: {branch} / {commit}. Current authority: 798 reviewed-applied / 50 pending / 0 accepted-unapplied; 522 complete standalone procedures; 173 scoped interfaces.\n\nUse the refreshed 157 source bindings and exact current catalog, index, pending audit, queue, handoff, and Return205 application evidence. Preserve all 31 original questions, both focused addenda, all 10 required new cases, and all five future-case requirements. Do not reopen feats, the completed 16, or other completed spells.\n\nReturn one source-faithful standalone static procedure per identity, exact class access and source bindings, question dispositions, all required positive/adverse cases, future-obligation dispositions, reversible state/event operations, and exact manifest. Mark only individually passing identities accepted=true and applied=false; name evidence-specific blockers for every held identity. Do not claim runtime, canonical card/rule, implementation, human-play, balance, cosmology, domain closure, completion, or release approval. Apply only exact independently audited accepted IDs after return.\n')
 files={'CURRENT_CONTEXT_206.json':enc(current_context),'CURRENT_SOURCE_CONFERENCE_CANDIDATE_206.json':current_raw,'HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json':candidate_raw,'HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip':archive_raw,'NOTES/INDEPENDENT_CONFERENCE_206.json':notes_raw,'REQUEST_206.txt':request.encode(),**current_files,**current_sources}
 for name in list(files): assert safe(name),name
 OUT.mkdir(parents=True)
 (OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_206.json').write_bytes(current_raw)
 rows=[]
 zip_path=OUT/'DD_Rank9_IllusionReality5_CurrentSource_206.zip'
 with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,raw in sorted(files.items()):
   z.writestr(name,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
   rows.append({'path':name,'bytes':len(raw),'sha256':sha(raw),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'})
  manifest={'id':'RANK9-ILLUSION-REALITY5-CURRENT-SOURCE-PACKET-MANIFEST-206','sourceCommit':commit,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':IDS,'memberCountExcludingSelf':len(rows),'members':rows}
  z.writestr('MANIFEST.json',enc(manifest),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
 with zipfile.ZipFile(zip_path) as z:
  assert z.testzip() is None and len(z.namelist())==len(rows)+1 and len(z.namelist())==len(set(z.namelist()))
  for r in rows:
   b=z.read(r['path']); assert len(b)==r['bytes'] and sha(b)==r['sha256'] and f'{zlib.crc32(b)&0xffffffff:08x}'==r['crc32']
 archive_binding=bind(zip_path.relative_to(ROOT).as_posix(),zip_path.read_bytes())
 cand_binding=bind((OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_206.json').relative_to(ROOT).as_posix(),current_raw)
 delivery={'id':'RANK9-ILLUSION-REALITY5-CURRENT-SOURCE-DELIVERY-206','status':'PREPARED_UNSENT','archive':archive_binding,'members':len(rows)+1,'manifestBindings':len(rows),'sourceCommit':commit,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':IDS,'candidate':cand_binding,'historicalCandidate':bind(CANDIDATE,candidate_raw),'historicalSourceArchive':bind(ARCHIVE.relative_to(ROOT).as_posix(),archive_raw),'sourceFilesRefreshed':len(refreshed),'sourceFilesChangedSinceHistoricalCandidate':changed,'accepted':False,'applied':False,'conversation':CHAT}
 delivery_raw=enc(delivery); delivery_path=OUT/'DD_Rank9_IllusionReality5_CurrentSource_206_DELIVERY.json';delivery_path.write_bytes(delivery_raw)
 prep={'id':'RANK9-ILLUSION-REALITY5-SOURCE-PREPARATION-206','recordedAtUtc':current['recordedAtUtc'],'status':'PASS','sourceCommit':commit,'sourceBranch':branch,'sourceAuthority':AUTH,'targetGroup':GROUP,'pendingIds':IDS,'currentCandidate':cand_binding,'historicalCandidate':bind(CANDIDATE,candidate_raw),'historicalArchive':bind(ARCHIVE.relative_to(ROOT).as_posix(),archive_raw),'packet':archive_binding,'deliveryManifest':bind(delivery_path.relative_to(ROOT).as_posix(),delivery_raw),'refreshedBindings':len(refreshed),'changedHistoricalBindings':changed,'questions':{'original':31,'addenda':2,'total':33},'requiredMainCases':10,'futureCaseRequirements':5,'canonicalChanges':False,'accepted':False,'applied':False}
 PREP.write_bytes(enc(prep))
 packet_record={'id':'RANK9ILLUSIONREALITY5-PACKET-206','status':'PREPARED_UNSENT','group':GROUP,'pendingIds':IDS,'sourceAuthority':AUTH,'sourceCommit':commit,'archive':archive_binding,'deliveryManifest':bind(delivery_path.relative_to(ROOT).as_posix(),delivery_raw),'candidate':cand_binding,'questions':33,'requiredMainCases':10,'futureCaseRequirements':5,'refreshedSourceBindings':len(refreshed),'canonicalChanges':False}
 PACKET.write_bytes(enc(packet_record))
 pcopy=copy.deepcopy(pending);pcopy.update({'id':'CURRENT50-PENDING-IDENTITY-AUDIT-206','recordedAtUtc':current['recordedAtUtc'],'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET','indexBinding':bind(INDEX,git_blob(commit,INDEX)),'catalogBinding':bind(CATALOG,git_blob(commit,CATALOG)),'authoredCounts':index['authoredCounts'],'currentAuthority':AUTH});PENDING_OUT.write_bytes(enc(pcopy))
 qcopy=copy.deepcopy(queue);qcopy.update({'id':'SPELL-REVIEW-QUEUE-206','recordedAtUtc':current['recordedAtUtc'],'packetStatus':'FRESH_CURRENT_SOURCE_PACKET_PREPARED_UNSENT','parentQueue':queue['id']})
 qcopy['pendingIdentityAudit']={'id':pcopy['id'],'path':PENDING_OUT.relative_to(ROOT).as_posix(),'pendingCount':50,'sha256':sha(PENDING_OUT.read_bytes())}
 qcopy['nextPreparedRequest'].update({'status':'FRESH_CURRENT_SOURCE_PACKET_PREPARED_UNSENT','freshPacketRequiredForCurrentAuthority':False,'currentCandidate':cand_binding,'currentPacket':archive_binding,'deliveryManifest':bind(delivery_path.relative_to(ROOT).as_posix(),delivery_raw),'questions':33,'requiredMainCases':10,'futureCaseRequirements':5})
 QUEUE_OUT.write_bytes(enc(qcopy))
 hcopy=copy.deepcopy(handoff);hcopy.update({'id':'CURRENT-HANDOFF-206','recordedAtUtc':current['recordedAtUtc'],'status':'RANK9_ILLUSION_REALITY5_FRESH_SOURCE_PACKET_PREPARED_UNSENT_50_PENDING','parentHandoff':handoff['id'],'currentQueue':{'path':QUEUE_OUT.relative_to(ROOT).as_posix(),'sha256':sha(QUEUE_OUT.read_bytes())},'currentQueueBinding':bind(QUEUE_OUT.relative_to(ROOT).as_posix(),QUEUE_OUT.read_bytes()),'pendingIdentityAudit':{'id':pcopy['id'],'path':PENDING_OUT.relative_to(ROOT).as_posix(),'pendingCount':50,'sha256':sha(PENDING_OUT.read_bytes())},'sourcePreparation':bind(PREP.relative_to(ROOT).as_posix(),PREP.read_bytes()),'currentPacket':archive_binding,'currentPacketCandidate':cand_binding,'currentPacketDeliveryManifest':bind(delivery_path.relative_to(ROOT).as_posix(),delivery_raw),'directorSubmission':{'status':'prepared-unsent','conversation':CHAT}})
 hcopy['nextPreparedRequest'].update({'status':'FRESH_CURRENT_SOURCE_PACKET_PREPARED_UNSENT','freshPacketRequiredForCurrentAuthority':False,'currentCandidate':cand_binding,'currentPacket':archive_binding,'deliveryManifest':bind(delivery_path.relative_to(ROOT).as_posix(),delivery_raw),'questions':33,'requiredMainCases':10,'futureCaseRequirements':5})
 HANDOFF_OUT.write_bytes(enc(hcopy))
 print(json.dumps({'status':'PASS','sourceCommit':commit,'sourceAuthority':AUTH,'refreshedBindings':len(refreshed),'changedBindings':len(changed),'packetMembers':len(rows)+1,'packetBytes':archive_binding['bytes'],'packetSha256':archive_binding['sha256'],'out':str(zip_path)},indent=2))
if __name__=='__main__': main()
