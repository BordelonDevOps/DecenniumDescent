from __future__ import annotations
import copy, hashlib, json, subprocess, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
FULL=ROOT/'docs/audit/2026-10-08/full-game'
GROUP='rank9-illusion-reality5'; TARGETS=['soul-reflection']
CLOSED=['supreme-illusion','mirrored-world','ethereal-disjunction','illusory-reality']
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
BRANCH='main'; CANDIDATE='DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_illusion_reality_5_source_conference_01.json'
HIST_ARCHIVE=FULL/'DD_Rank9_Illusion_Reality_5_Source_Conference_01.zip'; NOTES=AUDIT/'RANK9ILLUSIONREALITY5_NEXT_CONFERENCE_NOTES_129.json'
INDEX='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'; CATALOG='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
OUT=AUDIT/'rank9_illusionreality5_current_source_229_prepared'; ARCHIVE=OUT/'DD_Rank9_IllusionReality5_CurrentSource_229.zip'; DELIVERY=OUT/'DD_Rank9_IllusionReality5_CurrentSource_229_DELIVERY.json'
CANDIDATE_FILE=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_229.json'; CONTEXT_FILE=OUT/'CURRENT_CONTEXT_229.json'; REQUEST_FILE=OUT/'REQUEST_229.txt'
PREP=AUDIT/'RANK9ILLUSIONREALITY5_SOURCE_PREPARATION_229.json'; PACKET=AUDIT/'RANK9ILLUSIONREALITY5_PACKET_229.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_229.json'; HANDOFF=AUDIT/'CURRENT_HANDOFF_229.json'; PENDING=AUDIT/'CURRENT37_PENDING_IDENTITY_AUDIT_229.json'
CHAT='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
RETURN207=AUDIT/'rank9_illusionreality5_return207_received'; R207_ZIP=RETURN207/'DD_Rank9_IllusionReality5_Director_Return207.zip'; R207_DELIVERY=RETURN207/'DD_Rank9_IllusionReality5_Director_Return207_DELIVERY.json'
R207_AUDIT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN207_INDEPENDENT_AUDIT.json'; R207_RECEIPT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN207_RECEIPT.json'
R207_DECISION=AUDIT/'RANK9ILLUSIONREALITY5_DIRECTOR_DECISION_207.json'; R207_ACCEPT=AUDIT/'RANK9ILLUSIONREALITY5_EXACT_ACCEPTANCE_207.json'; R207_APP=AUDIT/'RANK9ILLUSIONREALITY5_APPLICATION_207.json'; R207_VALID=AUDIT/'RANK9ILLUSIONREALITY5_APPLICATION_VALIDATION_207.json'
R207_PACKET=AUDIT/'RANK9ILLUSIONREALITY5_PACKET_206.json'; R207_PACKET_AUDIT=AUDIT/'RANK9ILLUSIONREALITY5_PACKET206_INDEPENDENT_VERIFICATION.json'; R207_PREP=AUDIT/'RANK9ILLUSIONREALITY5_SOURCE_PREPARATION_206.json'
R228=AUDIT/'rank9_impactexile4_return228_received'; R228_ZIP=R228/'DD_Rank9_ImpactExile1_Director_Return228.zip'; R228_DELIVERY=R228/'DD_Rank9_ImpactExile1_Director_Return228_DELIVERY.json'
R228_AUDIT=AUDIT/'RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json'; R228_RECEIPT=AUDIT/'RANK9IMPACTEXILE4_RETURN228_RECEIPT.json'; R228_SUBMISSION=AUDIT/'RANK9IMPACTEXILE4_PACKET_228_SUBMISSION.json'


def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b)&0xffffffff:08x}'
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def bind(path,b): return {'path':path,'bytes':len(b),'sha256':sha(b)}
def info(p,raw=None):
 b=p.read_bytes() if raw is None else raw
 return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def blob_sha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def safe(name):
 p=PurePosixPath(name)
 return bool(name) and '\\' not in name and not p.is_absolute() and all(x not in ('','.','..') for x in p.parts)

def main():
 if OUT.exists() or any(p.exists() for p in (PREP,PACKET)): raise FileExistsError('Refusing to overwrite packet229 outputs')
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(); assert branch==BRANCH
 index=read(ROOT/INDEX); catalog=read(ROOT/CATALOG); queue=read(QUEUE); handoff=read(HANDOFF); pending=read(PENDING)
 assert queue['currentAuthority']==handoff['currentAuthority']==pending['authority']==AUTH
 assert queue['nextGroup']==handoff['nextGroup']==GROUP and queue['next']['pendingIds']==TARGETS
 assert queue['packetStatus'].startswith('RETURN228_AUDITED_HELD') and handoff['status'].startswith('RETURN228_AUDITED_HELD')
 assert pending['pendingCount']==37 and TARGETS[0] in pending['pendingIds']
 live=sorted(x['id'] for x in index['entries'] if x.get('authoredStatus')=='pending-authored-procedure')
 assert live==sorted(pending['pendingIds']) and len(live)==37
 assert index['authoredCounts']=={'reviewed':811,'pending':37} and index['representationCounts']['completeReviewedStandaloneProcedures']==535
 entries={x['id']:x for x in index['entries']}; spells={x['id']:x for x in catalog['spells']}
 assert entries[TARGETS[0]]['authoredStatus']=='pending-authored-procedure' and entries[TARGETS[0]]['sourceStatus']=='blocked-pending-operational-review'
 assert all(entries[s]['authoredStatus']=='reviewed-authored-operational-playtest' for s in CLOSED)
 assert all(s in spells for s in TARGETS+CLOSED)
 group=next(g for g in queue['currentPendingGroups'] if g['group']==GROUP)
 assert group['pendingIds']==TARGETS and group['freshPacketRequiredForCurrentAuthority'] is True
 hist_raw=subprocess.check_output(['git','cat-file','blob',f'{head}:{CANDIDATE}'],cwd=ROOT)
 hist_zip_raw=HIST_ARCHIVE.read_bytes(); historical=read(ROOT/CANDIDATE)
 assert len(hist_raw)==group['candidate']['bytes'] and sha(hist_raw)==group['candidate']['sha256']
 assert len(hist_zip_raw)==group['archive']['bytes'] and sha(hist_zip_raw)==group['archive']['sha256']
 assert historical['questions'] and len(historical['questions'])==31
 hist_by_id={x['spellId']:x for x in historical['records']}; assert set(CLOSED+TARGETS)<=set(hist_by_id)
 hist_bindings=historical['sourceBindings']; historical_sources={}
 with zipfile.ZipFile(HIST_ARCHIVE) as hz:
  assert hz.testzip() is None and len(hz.namelist())==len(set(hz.namelist()))
  for row in hist_bindings:
   raw=hz.read('sources/'+row['path']); assert len(raw)==row['bytes'] and sha(raw)==row['sha256']; historical_sources[row['path']]=raw
 notes=read(NOTES); assert len(notes['completeOriginalQuestionsUnchanged'])==31 and len(notes['focusedAdditionalQuestions'])==2
 assert len(notes['requiredNewCases'])==10 and len(notes['originalFutureCaseRequirementsUnchanged'])==5
 r207_audit=read(R207_AUDIT); r207_receipt=read(R207_RECEIPT); r207_delivery=read(R207_DELIVERY); r207_app=read(R207_APP); r207_valid=read(R207_VALID)
 assert r207_audit['status']=='PASS' and r207_receipt['acceptedIds']==CLOSED and r207_audit['acceptedIds']==CLOSED and r207_audit['heldIds']==TARGETS
 assert r207_receipt['blockers'][TARGETS[0]]['blockerIds']==['IR207-B02']
 assert r207_app['status'].startswith('APPLIED_FOUR_EXACT') and r207_valid['status']=='PASS'
 assert r207_delivery['acceptedIds']==CLOSED and r207_delivery['applied'] is False
 r228_audit=read(R228_AUDIT); r228_delivery=read(R228_DELIVERY); assert r228_audit['status']=='PASS' and r228_delivery['heldIds']==['reverse-gravity-field'] and not r228_delivery['applied']

 now=datetime.now(timezone.utc).isoformat(); refreshed=[]; changed=[]; current_sources={}
 for row in hist_bindings:
  path=row['path']; assert safe(path)
  raw=(ROOT/path).read_bytes(); refreshed.append({'path':path,'bytes':len(raw),'sha256':sha(raw),'gitBlobSHA1':blob_sha(raw)}); current_sources['sources_current/'+path]=raw
  if (len(raw),sha(raw))!=(row['bytes'],row['sha256']): changed.append({'path':path,'historicalBytes':row['bytes'],'historicalSha256':row['sha256'],'currentBytes':len(raw),'currentSha256':sha(raw)})
 assert len(refreshed)==157 and len({x['path'] for x in refreshed})==157
 target_record=copy.deepcopy(hist_by_id[TARGETS[0]])
 target_record.update({'currentIndexEntry':copy.deepcopy(entries[TARGETS[0]]),'completeCurrentCatalogSourceAndAccess':copy.deepcopy(spells[TARGETS[0]]),'status':'Pending at current 811/37/0 authority; reassess IR207-B02 only against current source evidence.','closedAcceptedSpellIds':CLOSED})
 candidate=copy.deepcopy(historical); candidate.update({'id':'CURRENT-SOURCE-CONFERENCE-CANDIDATE-229','recordedAtUtc':now,'status':'PREPARED_CURRENT_AUTHORITY_811_37_EXACT_SOUL_REFLECTION_PENDING_IDENTITY','currentSourceCommit':head,'currentBranch':branch,'currentAuthority':AUTH,'countsUnchanged':index['authoredCounts'],'currentPendingGroup':{'group':GROUP,'spellIds':TARGETS,'count':1},'closedAcceptedSpellIds':CLOSED,'closedAcceptedSpellDecisionBinding':{'return':207,'acceptedIds':CLOSED,'appliedIds':CLOSED,'doNotReopen':True,'decision':info(R207_DECISION),'acceptance':info(R207_ACCEPT),'application':info(R207_APP),'independentAudit':info(R207_AUDIT),'receipt':info(R207_RECEIPT)},'previousTargetHold':{'spellId':'soul-reflection','blockerIds':['IR207-B02'],'receipt':info(R207_RECEIPT),'independentAudit':info(R207_AUDIT),'reassessAgainstCurrentEvidence':True},'previousReturn228OutsideScope':{'heldIds':r228_delivery['heldIds'],'audit':info(R228_AUDIT),'receipt':info(R228_RECEIPT),'outsideScope':True},'historicalSourceBindings':copy.deepcopy(hist_bindings),'sourceBindings':refreshed,'sourceBindingRefresh':{'sourceFiles':len(refreshed),'changedSinceHistoricalCandidate':changed,'sourceContentsFromCurrentWorkingTree':True,'sourceCommitBase':head},'currentPendingIdentityAudit':info(PENDING),'records':[target_record]})
 cbytes=enc(candidate); candidate_path=CANDIDATE_FILE.relative_to(ROOT).as_posix()
 current_files={}
 required=[
  'START_HERE.md',INDEX,CATALOG,
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_228.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_228.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_228.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_229.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_229.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_229.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_229.md',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_NEXT_CONFERENCE_NOTES_129.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_RETURN207_INDEPENDENT_AUDIT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_RETURN207_RECEIPT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_DIRECTOR_DECISION_207.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_EXACT_ACCEPTANCE_207.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_APPLICATION_207.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_APPLICATION_VALIDATION_207.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_PACKET_206.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_PACKET206_INDEPENDENT_VERIFICATION.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9ILLUSIONREALITY5_SOURCE_PREPARATION_206.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_RETURN228_RECEIPT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_PACKET_228.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_PACKET_228_SUBMISSION.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_illusionreality5_return207_received/DD_Rank9_IllusionReality5_Director_Return207_DELIVERY.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_illusionreality5_return207_received/DD_Rank9_IllusionReality5_Director_Return207.zip',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_impactexile4_return228_received/DD_Rank9_ImpactExile1_Director_Return228_DELIVERY.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_impactexile4_return228_received/DD_Rank9_ImpactExile1_Director_Return228.zip',
 ]
 for path in required: current_files[path]=(ROOT/path).read_bytes()
 folder=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9illusionreality5_reviewed_207'
 for p in sorted(folder.rglob('*')):
  if p.is_file():
   path=p.relative_to(ROOT).as_posix(); current_files[path]=p.read_bytes()
 current_rows=[{'path':p,'bytes':len(b),'sha256':sha(b),'gitBlobSHA1':blob_sha(b)} for p,b in sorted(current_files.items())]
 context={'id':'RANK9-ILLUSION-REALITY5-CURRENT-DIRECTOR-CONTEXT-229','recordedAtUtc':now,'sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'targetGroup':{'group':GROUP,'pendingIds':TARGETS,'count':1},'currentIndexCounts':index['authoredCounts'],'currentPendingIdentityAudit':info(PENDING),'currentQueue':info(QUEUE),'currentHandoff':info(HANDOFF),'historicalCandidate':info(ROOT/CANDIDATE,hist_raw),'historicalSourceArchive':info(HIST_ARCHIVE,hist_zip_raw),'refreshedSourceBindings':len(refreshed),'changedHistoricalSourceBindings':changed,'return207AcceptedAppliedClosed':{'ids':CLOSED,'audit':info(R207_AUDIT),'receipt':info(R207_RECEIPT),'application':info(R207_APP),'exactAcceptance':info(R207_ACCEPT),'doNotReopen':True},'soulReflectionPriorHold':{'blockerIds':['IR207-B02'],'finding':r207_audit['blocker']['finding'],'minimumCorrection':r207_receipt['blockers'][TARGETS[0]]['blockerRecords'][0]['minimalCorrection'],'reassessAgainstCurrentEvidence':True},'return228OutsideScope':{'heldIds':r228_delivery['heldIds'],'blockerIds':r228_delivery['blockerIds'],'audit':info(R228_AUDIT),'receipt':info(R228_RECEIPT),'noReopen':True},'preservation':{'originalQuestions':31,'focusedAddenda':2,'requiredMainCases':10,'futureCaseRequirements':5},'canonicalChanges':False,'runtimeExecuted':False,'applyChanges':False}
 request=(f'GPT director — continue the ordinary spell review at current authority 811 reviewed/applied / 37 pending / 0 accepted-unapplied, with 535 complete standalone procedures and 173 scoped interfaces. Review ONLY soul-reflection, the sole pending identity in rank9-illusion-reality5.\n\n'
  f'Current source snapshot: branch {branch}, HEAD {head}, plus exact working-tree source bindings in this packet. Use the refreshed 157 source bindings, current queue229/handoff229/pending audit, full historical conference/questions, and Return207/228 evidence. Return207 accepted and applied exactly {", ".join(CLOSED)}; those four are closed. Do not reopen them. Return228 held reverse-gravity-field under IE204-B02 and is outside this scope.\n\n'
  'Preserve all 31 original questions, both focused addenda, all 10 required main cases, five future-case requirements, exact native placement/class access/cost/source/acquisition/prior lifecycle, and every passing/adverse branch. Reassess IR207-B02 against current evidence instead of carrying it mechanically. The prior blocker concerns absent source-bound changed-form/attached/no-phase recipient lifecycle evidence, including original-target zero/death settlement, copied active concentration ending, and actual original cargo entrusted to the reflection. Do not invent recipient profiles, anatomy, phases, healing, or source facts.\n\n'
  'Return an explicit accepted/applied/held decision with exact blockers and minimum missing witnesses, complete case and reversible-operation results, a sealed ZIP plus matching DELIVERY.json, and the exact next pending group. Do not modify canonical files or run supplied programs. Apply no changes in this review. Keep runtime, implementation, human-play, balance, cosmology, domain, completion, and release gates closed. Continue through response caps until both files are attached.')
 files={'CURRENT_CONTEXT_229.json':enc(context),'CURRENT_SOURCE_CONFERENCE_CANDIDATE_229.json':cbytes,'HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json':hist_raw,'HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip':hist_zip_raw,'NOTES/RANK9ILLUSIONREALITY5_NEXT_CONFERENCE_NOTES_129.json':NOTES.read_bytes(),'REQUEST_229.txt':request.encode(),**{'current/'+p:b for p,b in current_files.items()},**{'sources_current/'+p:b for p,b in current_sources.items()}}
 # Bind Return207's exact source target together with the current sources.
 for arc,label in [(R207_ZIP,'evidence/RETURN207.zip'),(R228_ZIP,'evidence/RETURN228.zip')]: files[label]=arc.read_bytes()
 evidence={
  'evidence/RETURN207_DELIVERY.json':R207_DELIVERY,'evidence/RETURN207_INDEPENDENT_AUDIT.json':R207_AUDIT,'evidence/RETURN207_RECEIPT.json':R207_RECEIPT,
  'evidence/RETURN207_DIRECTOR_DECISION.json':R207_DECISION,'evidence/RETURN207_EXACT_ACCEPTANCE.json':R207_ACCEPT,'evidence/RETURN207_APPLICATION.json':R207_APP,'evidence/RETURN207_APPLICATION_VALIDATION.json':R207_VALID,
  'evidence/RETURN207_PACKET206_RECORD.json':R207_PACKET,'evidence/RETURN207_PACKET206_AUDIT.json':R207_PACKET_AUDIT,'evidence/RETURN207_SOURCE_PREPARATION206.json':R207_PREP,
  'evidence/RETURN228_DELIVERY.json':R228_DELIVERY,'evidence/RETURN228_INDEPENDENT_AUDIT.json':R228_AUDIT,'evidence/RETURN228_RECEIPT.json':R228_RECEIPT,'evidence/RETURN228_SUBMISSION.json':R228_SUBMISSION,
 }
 files.update({k:v.read_bytes() for k,v in evidence.items()})
 for name in files: assert safe(name),name
 OUT.mkdir(parents=True)
 CANDIDATE_FILE.write_bytes(cbytes); CONTEXT_FILE.write_bytes(enc(context)); REQUEST_FILE.write_bytes(request.encode())
 rows=[]
 with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,b in sorted(files.items()): z.writestr(name,b); rows.append({'path':name,'bytes':len(b),'sha256':sha(b),'crc32':crc(b)})
  manifest={'id':'RANK9-ILLUSION-REALITY5-CURRENT-SOURCE-MANIFEST-229','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':TARGETS,'closedAcceptedIds':CLOSED,'memberCountExcludingSelf':len(rows),'members':rows}
  z.writestr('MANIFEST.json',enc(manifest))
 with zipfile.ZipFile(ARCHIVE) as z:
  assert z.testzip() is None and len(z.namelist())==len(rows)+1==len(set(z.namelist()))
  for row in rows:
   raw=z.read(row['path']); assert (len(raw),sha(raw),crc(raw))==(row['bytes'],row['sha256'],row['crc32'])
 archive_bytes=ARCHIVE.read_bytes(); archive_bind={'path':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':len(archive_bytes),'sha256':sha(archive_bytes),'crc32':crc(archive_bytes)}
 cand_bind=bind(candidate_path,cbytes); ctx_bind=bind(CONTEXT_FILE.relative_to(ROOT).as_posix(),enc(context));req_bind=bind(REQUEST_FILE.relative_to(ROOT).as_posix(),request.encode())
 delivery={'id':'RANK9-ILLUSION-REALITY5-CURRENT-SOURCE-DELIVERY-229','status':'PREPARED_UNSENT','archive':archive_bind,'members':len(rows)+1,'manifestBindings':len(rows),'sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':TARGETS,'closedAcceptedIds':CLOSED,'accepted':False,'applied':False,'candidate':cand_bind,'context':ctx_bind,'request':req_bind,'historicalCandidate':info(ROOT/CANDIDATE,hist_raw),'historicalSourceArchive':info(HIST_ARCHIVE,hist_zip_raw),'sourceBindings':len(refreshed),'changedSourceBindings':changed,'priorReturn207':{'archive':info(R207_ZIP),'acceptedIds':CLOSED,'heldIds':TARGETS,'blocker':'IR207-B02','audit':info(R207_AUDIT),'receipt':info(R207_RECEIPT)},'priorReturn228OutsideScope':{'heldIds':r228_delivery['heldIds'],'audit':info(R228_AUDIT),'receipt':info(R228_RECEIPT)},'conversation':CHAT}
 delivery_raw=enc(delivery);DELIVERY.write_bytes(delivery_raw)
 prep={'id':'RANK9-ILLUSION-REALITY5-SOURCE-PREPARATION-229','recordedAtUtc':now,'status':'PASS','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'targetGroup':GROUP,'pendingIds':TARGETS,'closedAcceptedIds':CLOSED,'candidate':cand_bind,'context':ctx_bind,'historicalCandidate':info(ROOT/CANDIDATE,hist_raw),'historicalSourceArchive':info(HIST_ARCHIVE,hist_zip_raw),'packet':archive_bind,'deliveryManifest':info(DELIVERY,delivery_raw),'refreshedBindings':len(refreshed),'changedHistoricalBindings':changed,'questions':{'original':31,'addenda':2,'total':33},'requiredMainCases':10,'futureCaseRequirements':5,'priorReturn207':{'acceptedIds':CLOSED,'heldIds':TARGETS,'blocker':'IR207-B02','auditStatus':r207_audit['status']},'priorReturn228OutsideScope':{'heldIds':r228_delivery['heldIds'],'auditStatus':r228_audit['status']},'canonicalChanges':False,'accepted':False,'applied':False}
 PREP.write_bytes(enc(prep))
 packet={'id':'RANK9ILLUSIONREALITY5-PACKET-229','status':'PREPARED_UNSENT','group':GROUP,'pendingIds':TARGETS,'closedAcceptedIds':CLOSED,'sourceAuthority':AUTH,'sourceBranch':branch,'sourceCommit':head,'archive':archive_bind,'deliveryManifest':info(DELIVERY,delivery_raw),'candidate':cand_bind,'questions':33,'requiredMainCases':10,'futureCaseRequirements':5,'refreshedSourceBindings':len(refreshed),'canonicalChanges':False,'independentAudit':None}
 PACKET.write_bytes(enc(packet))
 # Update submission pointers without altering the input sidecars archived above.
 for p in (QUEUE,HANDOFF):
  x=read(p); x['status']='CURRENT_SOURCE_PACKET_229_PREPARED_UNSENT' if p==HANDOFF else x.get('status','')
  if p==QUEUE: x['packetStatus']='CURRENT_SOURCE_PACKET_229_PREPARED_UNSENT'
  x['nextPreparedRequest'].update({'group':GROUP,'pendingIds':TARGETS,'pendingCount':1,'status':'CURRENT_SOURCE_PACKET_229_PREPARED_UNSENT','freshPacketRequiredForCurrentAuthority':False,'packet':archive_bind,'deliveryManifest':info(DELIVERY,delivery_raw),'candidate':cand_bind})
  x['currentPacket']=archive_bind;x['currentPacketDelivery']=info(DELIVERY,delivery_raw)
  if p==HANDOFF:
   x['currentPacketAudit']=None;x['resumePriority']='Submit independently audited packet229 to GPT; ping repeatedly if stalled, independently audit the return, then apply only exact accepted IDs.'
   x['directorSubmission']={'status':'prepared-unsent','conversation':CHAT}
  x['sourcePreparation']=info(PREP,PREP.read_bytes())
  p.write_bytes(enc(x))
 packet['independentAudit']={'status':'PENDING_INDEPENDENT_AUDIT','packet':archive_bind}
 PACKET.write_bytes(enc(packet))
 print(json.dumps({'status':'PASS','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'refreshedBindings':len(refreshed),'changedBindings':len(changed),'originalQuestions':31,'focusedAddenda':2,'requiredMainCases':10,'futureCaseRequirements':5,'packetMembers':len(rows)+1,'packetBytes':archive_bind['bytes'],'packetSha256':archive_bind['sha256'],'out':str(ARCHIVE)},indent=2))
if __name__=='__main__': main()
