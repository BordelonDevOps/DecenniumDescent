from __future__ import annotations
import copy, hashlib, json, subprocess, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
FULL=ROOT/'docs/audit/2026-10-08/full-game'
AUDIT=FULL/'director-spell-review-129'
GROUP='rank9-alignment-faction-purification5'
TARGETS=['alignment-ascension','alignment-perfection','faction-incarnate','faction-perfection','corruption-purification']
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
BRANCH='main'
INDEX='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
CANDIDATE='DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_alignment_faction_purification_5_source_conference_02.json'
HIST_ARCHIVE=FULL/'DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_02.zip'
PREPARATION=FULL/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_PREPARATION.json'
CHECK=FULL/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_CHECK.json'
REQUEST=FULL/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_REQUEST.txt'
SUBMISSION=FULL/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_SUBMISSION_211.json'
R247=AUDIT/'rank9_materialforging2_return247_received'
R247_ZIP=R247/'DD_Rank9_MaterialForging2_Director_Return247_HELD.zip'; R247_DELIVERY=R247/'DD_Rank9_MaterialForging2_Director_Return247_DELIVERY.json'
R247_AUDIT=AUDIT/'RANK9MATERIALFORGING2_RETURN247_INDEPENDENT_AUDIT.json'; R247_RECEIPT=AUDIT/'RANK9MATERIALFORGING2_RETURN247_RECEIPT.json'; R247_SUBMISSION=AUDIT/'RANK9MATERIALFORGING2_PACKET_247_SUBMISSION.json'
R246=AUDIT/'rank9_illusionreality5_return246_received'; R246_ZIP=R246/'DD_Rank9_SoulReflection_Director_Return246_HELD.zip'; R246_DELIVERY=R246/'DD_Rank9_SoulReflection_Director_Return246_DELIVERY.json'
R246_AUDIT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN246_INDEPENDENT_AUDIT.json'; R246_RECEIPT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN246_RECEIPT.json'
R245=AUDIT/'rank9_impactexile4_return245_received'; R245_ZIP=R245/'DD_Rank9_ImpactExile1_Director_Return245_HELD.zip'; R245_DELIVERY=R245/'DD_Rank9_ImpactExile1_Director_Return245_DELIVERY.json'
R245_AUDIT=AUDIT/'RANK9IMPACTEXILE4_RETURN245_INDEPENDENT_AUDIT.json'; R245_RECEIPT=AUDIT/'RANK9IMPACTEXILE4_RETURN245_RECEIPT.json'
QUEUE247=AUDIT/'CURRENT_SPELL_QUEUE_247.json'; HANDOFF247=AUDIT/'CURRENT_HANDOFF_247.json'; PENDING247=AUDIT/'CURRENT37_PENDING_IDENTITY_AUDIT_247.json'
OUT=AUDIT/'rank9_alignmentfactionpurification5_current_source_248_prepared'
ARCHIVE=OUT/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_248.zip'; DELIVERY=OUT/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_248_DELIVERY.json'
CAND_FILE=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_248.json'; CONTEXT_FILE=OUT/'CURRENT_CONTEXT_248.json'; REQUEST_FILE=OUT/'REQUEST_248.txt'
QUEUE248=AUDIT/'CURRENT_SPELL_QUEUE_248.json'; HANDOFF248=AUDIT/'CURRENT_HANDOFF_248.json'; PENDING248=AUDIT/'CURRENT37_PENDING_IDENTITY_AUDIT_248.json'; SNAPSHOT248=AUDIT/'CURRENT_SPELL_REVIEW_SNAPSHOT_248.md'
PREP=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_SOURCE_PREPARATION_248.json'; PACKET=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_248.json'
CHAT='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b)&0xffffffff:08x}'
def git_blob_sha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def safe(name):
 p=PurePosixPath(name)
 return bool(name) and '\\' not in name and not p.is_absolute() and all(x not in ('','.','..') for x in p.parts)
def info(p,raw=None):
 b=p.read_bytes() if raw is None else raw
 return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def targetrow(groups): return next(g for g in groups if g['group']==GROUP)
def main():
 # Re-running this local packet builder is idempotent over its own named outputs.
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
 assert branch==BRANCH
 index=read(ROOT/INDEX); catalog=read(ROOT/CATALOG); q0=read(QUEUE247); h0=read(HANDOFF247); p0=read(PENDING247); hist=read(ROOT/CANDIDATE)
 assert q0['currentAuthority']==h0['currentAuthority']==p0['authority']==AUTH and p0['pendingCount']==37
 pending=sorted(x['id'] for x in index['entries'] if x.get('authoredStatus')=='pending-authored-procedure')
 assert len(pending)==37 and pending==sorted(p0['pendingIds'])
 assert index['authoredCounts']=={'reviewed':811,'pending':37} and index['representationCounts']['completeReviewedStandaloneProcedures']==535
 entries={x['id']:x for x in index['entries']}; spells={x['id']:x for x in catalog['spells']}
 assert all(s in spells and entries[s]['authoredStatus']=='pending-authored-procedure' and entries[s]['sourceStatus']=='blocked-pending-operational-review' for s in TARGETS)
 group=targetrow(q0['currentPendingGroups']); assert group['pendingIds']==TARGETS and group['pendingCount']==5
 r247audit=read(R247_AUDIT); r247d=read(R247_DELIVERY); r247sub=read(R247_SUBMISSION)
 assert r247audit['status']=='PASS' and r247audit['checkCount']==19 and r247d['heldIds']==['eternal-forge','matter-conversion'] and r247d['applied'] is False and r247sub['status']=='RETURN247_AUDITED_HELD_NEXT_ALIGNMENT_FACTION_PURIFICATION5_811_37_0'
 r246audit=read(R246_AUDIT); r246d=read(R246_DELIVERY); r246r=read(R246_RECEIPT)
 r245audit=read(R245_AUDIT); r245d=read(R245_DELIVERY); r245r=read(R245_RECEIPT)
 assert r246audit['status']=='PASS' and r246d['heldIds']==['soul-reflection'] and r246d['applied'] is False
 assert r245audit['status']=='PASS' and r245d['heldIds']==['reverse-gravity-field'] and r245d['applied'] is False
 assert hist['id']=='RANK9-ALIGNMENT-FACTION-PURIFICATION5-SOURCE-CONFERENCE02' and hist['currentAuthority']=={'reviewedApplied':804,'pending':44,'acceptedUnapplied':0,'completeStandaloneProcedures':528,'scopedInterfaces':173}
 assert len(hist['records'])==5 and {r['spellId'] for r in hist['records']}==set(TARGETS) and len(hist['questions'])==28 and len(hist['sourceBindings'])==130 and len(hist['futureCaseRequirements'])==7 and hist['newRuleAdoptions']==0
 with zipfile.ZipFile(HIST_ARCHIVE) as hz:
  histzip=HIST_ARCHIVE.read_bytes()
  assert hz.testzip() is None and len(hz.namelist())==len(set(hz.namelist()))
  assert len(histzip)==group['archive']['bytes'] and sha(histzip)==group['archive']['sha256']
  source_files={}; refreshed=[]; changed=[]
  for row in hist['sourceBindings']:
   path=row['path']; assert safe(path)
   oldraw=hz.read('sources/'+path)
   assert (len(oldraw),sha(oldraw))==(row['bytes'],row['sha256'])
   raw=(ROOT/path).read_bytes()
   current={'path':path,'bytes':len(raw),'sha256':sha(raw),'gitBlobSHA1':git_blob_sha(raw)}
   refreshed.append(current); source_files['sources_current/'+path]=raw
   if (len(raw),sha(raw))!=(row['bytes'],row['sha256']): changed.append({'path':path,'historicalBytes':row['bytes'],'historicalSha256':row['sha256'],'currentBytes':len(raw),'currentSha256':sha(raw)})
 assert len(refreshed)==130 and len({x['path'] for x in refreshed})==130
 assert len(changed)==1 and changed[0]['path']==INDEX
 # Confirm the target spell source rows have not changed since candidate02; access remains source-owned.
 record_by_id={r['spellId']:r for r in hist['records']}
 for sid in TARGETS:
  historical=record_by_id[sid]['completeCurrentCatalogSourceAndAccess'] if 'completeCurrentCatalogSourceAndAccess' in record_by_id[sid] else record_by_id[sid].get('sourceCatalogRecord')
  current=spells[sid]
  assert current['id']==sid and entries[sid]['authoredStatus']=='pending-authored-procedure'
  if historical:
   assert historical.get('classAccess')==current.get('classAccess')
 now=datetime.now(timezone.utc).isoformat()
 # Freeze the independently audited Return247 and current authority before preparing the next request.
 def fi(p): return info(p)
 r247info=fi(R247_ZIP); r247dinfo=fi(R247_DELIVERY); r247ainfo=fi(R247_AUDIT); r247rinfo=fi(R247_RECEIPT)
 r246info=fi(R246_ZIP); r246dinfo=fi(R246_DELIVERY); r246ainfo=fi(R246_AUDIT); r246rinfo=fi(R246_RECEIPT)
 r245info=fi(R245_ZIP); r245dinfo=fi(R245_DELIVERY); r245ainfo=fi(R245_AUDIT); r245rinfo=fi(R245_RECEIPT)
 pending_audit=copy.deepcopy(p0)
 pending_audit.update({'id':'CURRENT37-PENDING-IDENTITY-AUDIT-248','recordedAtUtc':now,'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN247','lastDirectorReturn':{'archive':r247info,'deliveryManifest':r247dinfo,'independentAudit':r247ainfo,'receipt':r247rinfo,'acceptedIds':[],'appliedIds':[],'heldIds':['eternal-forge','matter-conversion'],'blockerIds':['MF210-B01','MF210-B02']},'preparedNextGroup':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':5,'historicalContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','freshPacketRequiredForCurrentAuthority':True}})
 PENDING248.write_bytes(enc(pending_audit))
 queue=copy.deepcopy(q0)
 queue.update({'id':'SPELL-REVIEW-QUEUE-248','recordedAtUtc':now,'supersedesQueue':'SPELL-REVIEW-QUEUE-247','pendingIdentityAudit':fi(PENDING248),'currentReturnAudit':r247ainfo,'currentReturnDelivery':r247dinfo,'currentReturnArchive':r247info,'currentReturnDecision':'RANK9-MATERIAL-FORGING2-DIRECTOR-RETURN247','currentReturnReceipt':r247rinfo,'currentReturnBinding':r247info,'currentReturnSourceArchive':q0.get('currentPacket'),'currentReturnSourceDelivery':q0.get('currentDeliveryManifest'),'currentPacketAudit':r247ainfo,'currentPacketAuditReceipt':r247rinfo,'packetStatus':'RETURN247_AUDITED_HELD_NEXT_ALIGNMENT_FACTION_PURIFICATION5_811_37_0','status':'RETURN247_AUDITED_HELD_NEXT_ALIGNMENT_FACTION_PURIFICATION5_811_37_0','nextGroup':GROUP,'next':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':5,'status':'FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_811_37_0','freshPacketRequiredForCurrentAuthority':True},'nextPreparedRequest':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':5,'status':'FRESH_PACKET248_PREPARATION_IN_PROGRESS','freshPacketRequiredForCurrentAuthority':True,'historicalContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','previousReturn247OutsideScope':{'heldIds':['eternal-forge','matter-conversion'],'blockerIds':['MF210-B01','MF210-B02'],'audit':r247ainfo},'otherPreservedHolds':[{'heldIds':['soul-reflection'],'blockerIds':['IR207-B02'],'audit':r246ainfo},{'heldIds':['reverse-gravity-field'],'blockerIds':['IE204-B02'],'audit':r245ainfo}],'packet':None,'deliveryManifest':None,'independentAudit':None,'auditReceipt':None},'lastReviewedBatch':{'group':'rank9-material-forging2','pendingIds':['eternal-forge','matter-conversion'],'acceptedIds':[],'appliedIds':[],'heldIds':['eternal-forge','matter-conversion'],'blockerIds':{'eternal-forge':['MF210-B01'],'matter-conversion':['MF210-B02']},'returnArchive':r247info,'returnAudit':r247ainfo},'githubChanges':False})
 target_row=targetrow(queue['currentPendingGroups']); target_row.update({'status':'FRESH_PACKET248_PREPARATION_IN_PROGRESS_811_37_0','freshPacketRequiredForCurrentAuthority':True,'currentAuthority':AUTH,'previousHeldBatch':{'ids':['eternal-forge','matter-conversion'],'blockers':['MF210-B01','MF210-B02'],'acceptedIds':[],'appliedIds':[]},'previousReturn247':r247info})
 QUEUE248.write_bytes(enc(queue))
 handoff=copy.deepcopy(h0)
 handoff.update({'id':'CURRENT-HANDOFF-248','recordedAtUtc':now,'status':'RETURN247_AUDITED_HELD_PACKET248_PREPARATION_811_37','currentAuthority':AUTH,'pendingIdentityAudit':fi(PENDING248),'queue':fi(QUEUE248),'currentQueueBinding':fi(QUEUE248),'currentReturnBinding':r247info,'currentReturnDelivery':r247dinfo,'currentReturnAudit':r247ainfo,'currentReturnReceipt':r247rinfo,'currentReturnDecision':'RANK9-MATERIAL-FORGING2-DIRECTOR-RETURN247','latestBatch':{'group':'rank9-material-forging2','acceptedIds':[],'appliedIds':[],'heldIds':['eternal-forge','matter-conversion'],'blockerIds':{'eternal-forge':['MF210-B01'],'matter-conversion':['MF210-B02']},'returnArchive':r247info,'independentAudit':r247ainfo},'nextStep':'Prepare, independently audit, and submit a fresh 811/37 current-source packet248 to GPT for only the five Rank9 Alignment/Faction Purification identities. Reassess AFP211-B01 through AFP211-B05 against current sources, preserve closed AFP211-E01 and every unrelated hold, audit the sealed return, then apply only exact accepted IDs.','nextGroup':GROUP,'nextPendingCount':5,'unacceptedThisStep':['eternal-forge','matter-conversion'],'currentPacket':None,'currentPacketDelivery':None,'currentPacketAudit':None,'currentPacketAuditReceipt':None,'nextPreparedRequest':queue['nextPreparedRequest'],'githubChanges':False,'resumePriority':'Build and independently audit packet248, send it to GPT, check browser progress frequently and ping again if needed, then audit the sealed director return before considering any exact accepted IDs.'})
 HANDOFF248.write_bytes(enc(handoff))
 SNAPSHOT248.write_text(f'# Current Ordinary Spell Review Snapshot 248\n\nAuthority: **811 reviewed/applied / 37 pending / 0 accepted-unapplied**; 535 complete standalone procedures and 173 scoped interfaces.\n\nReturn247 independently passed 19/19 and held eternal-forge (MF210-B01) and matter-conversion (MF210-B02); neither was applied. The next group is **Rank9 Alignment/Faction Purification5**: {", ".join(TARGETS)}. Reassess AFP211-B01 through AFP211-B05; retain the closed shared-evidence finding AFP211-E01 and all unrelated holds.\n\nSoul Reflection remains held under IR207-B02; reverse-gravity-field remains held under IE204-B02. This packet does not amend canonical files or open runtime, implementation, human-play, balance, cosmology, domain, completion or release gates.\n',encoding='utf-8')
 # Refresh the full source candidate with current authority and exact target catalog/index entries.
 candidate=copy.deepcopy(hist)
 candidate.update({'id':'CURRENT-SOURCE-CONFERENCE-CANDIDATE-248','recordedAtUtc':now,'status':'PREPARED_CURRENT_AUTHORITY_811_37_EXACT_ALIGNMENT_FACTION_PURIFICATION5_GROUP','currentSourceCommit':head,'currentBranch':branch,'currentWorkingTreeSnapshot':True,'currentAuthority':AUTH,'currentPendingGroup':{'group':GROUP,'spellIds':TARGETS,'count':5},'historicalSourceBindings':copy.deepcopy(hist['sourceBindings']),'sourceBindings':refreshed,'sourceBindingRefresh':{'sourceFiles':len(refreshed),'changedSinceHistoricalCandidate':changed,'sourceContentsFromCurrentWorkingTree':True,'sourceCommitBase':head},'records':[copy.deepcopy(r) for r in hist['records']],'priorAFP211DispositionToReassess':{'contentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','reassessAgainstCurrentSources':True},'priorReturn247OutsideScope':{'heldIds':['eternal-forge','matter-conversion'],'blockerIds':['MF210-B01','MF210-B02'],'archive':r247info,'delivery':r247dinfo,'audit':r247ainfo,'receipt':r247rinfo},'priorReturn246OutsideScope':{'heldIds':['soul-reflection'],'blockerIds':['IR207-B02'],'archive':r246info,'delivery':r246dinfo,'audit':r246ainfo,'receipt':r246rinfo},'priorReturn245OutsideScope':{'heldIds':['reverse-gravity-field'],'blockerIds':['IE204-B02'],'archive':r245info,'delivery':r245dinfo,'audit':r245ainfo,'receipt':r245rinfo}})
 for r in candidate['records']:
  sid=r['spellId']; r['currentIndexEntry']=copy.deepcopy(entries[sid]); r['completeCurrentCatalogSourceAndAccess']=copy.deepcopy(spells[sid]); r['status']='Pending at current 811/37/0 authority; reassess AFP211 blocker evidence against refreshed current sources.'
 candidate['currentAuthorityEvidence']={'currentIndex':info(ROOT/INDEX),'currentCatalog':info(ROOT/CATALOG),'currentQueue':fi(QUEUE248),'currentHandoff':fi(HANDOFF248),'currentPendingIdentityAudit':fi(PENDING248),'latestReturn247Audit':r247ainfo,'targetIdsStillPending':TARGETS}
 cbytes=enc(candidate)
 context={'id':'RANK9-ALIGNMENT-FACTION-PURIFICATION5-CURRENT-DIRECTOR-CONTEXT-248','recordedAtUtc':now,'sourceCommit':head,'sourceBranch':branch,'currentWorkingTreeSnapshot':True,'sourceAuthority':AUTH,'targetGroup':{'group':GROUP,'pendingIds':TARGETS,'count':5},'currentIndexCounts':index['authoredCounts'],'pendingIdentityAudit':fi(PENDING248),'currentQueue':fi(QUEUE248),'currentHandoff':fi(HANDOFF248),'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'refreshedSourceBindings':130,'changedHistoricalSourceBindings':changed,'preservation':{'originalQuestions':28,'focusedAdditionalQuestions':0,'futureCaseRequirements':7,'sixPrintedPlacementsAcrossFiveIdentities':True,'newRuleAdoptions':0},'previousContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','priorReturn247OutsideScope':{'archive':r247info,'delivery':r247dinfo,'audit':r247ainfo,'receipt':r247rinfo,'heldIds':['eternal-forge','matter-conversion'],'blockerIds':['MF210-B01','MF210-B02']},'priorReturn246OutsideScope':{'archive':r246info,'delivery':r246dinfo,'audit':r246ainfo,'receipt':r246rinfo,'heldIds':['soul-reflection'],'blockerIds':['IR207-B02']},'priorReturn245OutsideScope':{'archive':r245info,'delivery':r245dinfo,'audit':r245ainfo,'receipt':r245rinfo,'heldIds':['reverse-gravity-field'],'blockerIds':['IE204-B02']},'canonicalChanges':False,'runtimeExecuted':False,'applyChanges':False}
 request=(f'GPT director — continue the ordinary spell review at current authority 811 reviewed/applied / 37 pending / 0 accepted-unapplied (535 complete standalone procedures; 173 scoped interfaces). Review ONLY alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection, and corruption-purification in rank9-alignment-faction-purification5.\n\n'
  f'This packet snapshots branch {branch}, HEAD {head}, and refreshed current working-tree source bytes. Use all 130 refreshed source bindings, current catalog/index/access, queue248/handoff248/pending audit248, the complete source conference02 archive, all 28 original questions and seven future-case requirements. Preserve all six printed placements across the five identities and every native class route, cost, source, lifecycle, and accepted-interface boundary. No new rules are preselected.\n\n'
  'Reassess historical content blockers AFP211-B01 through AFP211-B05 against current sources and evidence. AFP211-E01 is recorded as closed shared evidence; verify and preserve that disposition. Return247 held eternal-forge and matter-conversion under MF210-B01/B02; Return246 held soul-reflection under IR207-B02; Return245 held reverse-gravity-field under IE204-B02. All remain outside this packet and must stay unchanged.\n\n'
  'Select dispositions for every original question; distinguish source facts from incomplete integrated witness coverage; report source-linked procedures, useful positive cases, meaningful adverse branches, all forward/inverse replay totals, and exact acceptance/hold decisions with minimum missing witnesses. Do not invent unstated values, reputation scales, permissions, class access, profiles, targets or cosmology. Do not change canonical files, apply decisions, or run supplied programs. Keep runtime, implementation, human-play, balance, cosmology, domain, completion and release gates closed. Return a sealed decision ZIP with matching DELIVERY.json and the exact next pending group. Continue through response caps until both files are attached.' )
 request_bytes=request.encode('utf-8')
 # Snapshot current root plus group-specific preparation and all prior-return boundaries.
 current_paths=[
  'START_HERE.md',INDEX,CATALOG,
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_247.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_247.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_247.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MATERIALFORGING2_RETURN247_INDEPENDENT_AUDIT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MATERIALFORGING2_RETURN247_RECEIPT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MATERIALFORGING2_PACKET_247_SUBMISSION.json',
  'docs/audit/2026-10-08/full-game/RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_CHECK.json',
  'docs/audit/2026-10-08/full-game/RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_PREPARATION.json',
  'docs/audit/2026-10-08/full-game/RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_REQUEST.txt',
  'docs/audit/2026-10-08/full-game/RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_SUBMISSION_211.json',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_02_SUBMISSION_210.json',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_PROVENANCE_RECONCILIATION_210.json'
 ]
 current_files={p:(ROOT/p).read_bytes() for p in current_paths if (ROOT/p).exists()}
 current_files[CANDIDATE]=(ROOT/CANDIDATE).read_bytes()
 current_files[QUEUE248.relative_to(ROOT).as_posix()]=QUEUE248.read_bytes()
 current_files[HANDOFF248.relative_to(ROOT).as_posix()]=HANDOFF248.read_bytes()
 current_files[PENDING248.relative_to(ROOT).as_posix()]=PENDING248.read_bytes()
 current_files[PREPARATION.relative_to(ROOT).as_posix()]=PREPARATION.read_bytes()
 current_files[CHECK.relative_to(ROOT).as_posix()]=CHECK.read_bytes()
 evidence={
  'evidence/RETURN247.zip':R247_ZIP.read_bytes(),'evidence/RETURN247_DELIVERY.json':R247_DELIVERY.read_bytes(),'evidence/RETURN247_INDEPENDENT_AUDIT.json':R247_AUDIT.read_bytes(),'evidence/RETURN247_RECEIPT.json':R247_RECEIPT.read_bytes(),
  'evidence/RETURN246.zip':R246_ZIP.read_bytes(),'evidence/RETURN246_DELIVERY.json':R246_DELIVERY.read_bytes(),'evidence/RETURN246_INDEPENDENT_AUDIT.json':R246_AUDIT.read_bytes(),'evidence/RETURN246_RECEIPT.json':R246_RECEIPT.read_bytes(),
  'evidence/RETURN245.zip':R245_ZIP.read_bytes(),'evidence/RETURN245_DELIVERY.json':R245_DELIVERY.read_bytes(),'evidence/RETURN245_INDEPENDENT_AUDIT.json':R245_AUDIT.read_bytes(),'evidence/RETURN245_RECEIPT.json':R245_RECEIPT.read_bytes()
 }
 out_files={'CURRENT_CONTEXT_248.json':enc(context),'CURRENT_SOURCE_CONFERENCE_CANDIDATE_248.json':cbytes,'REQUEST_248.txt':request_bytes,'historical/DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_02.zip':histzip}
 for path,raw in current_files.items():out_files['current/'+path]=raw
 for name,raw in source_files.items():out_files[name]=raw
 out_files.update(evidence)
 for name in out_files:assert safe(name),name
 OUT.mkdir(parents=True,exist_ok=True)
 CAND_FILE.write_bytes(cbytes);CONTEXT_FILE.write_bytes(enc(context));REQUEST_FILE.write_bytes(request_bytes)
 rows=[]
 with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,raw in sorted(out_files.items()):z.writestr(name,raw);rows.append({'path':name,'bytes':len(raw),'sha256':sha(raw),'crc32':crc(raw)})
  manifest={'id':'RANK9-ALIGNMENT-FACTION-PURIFICATION5-CURRENT-SOURCE-MANIFEST-248','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':TARGETS,'memberCountExcludingSelf':len(rows),'members':rows}
  z.writestr('MANIFEST.json',enc(manifest))
 with zipfile.ZipFile(ARCHIVE) as z:
  assert z.testzip() is None and len(z.namelist())==len(rows)+1==len(set(z.namelist()))
  for row in rows:
   raw=z.read(row['path']);assert (len(raw),sha(raw),crc(raw))==(row['bytes'],row['sha256'],row['crc32'])
 archive_info=info(ARCHIVE);candidate_info={'path':CAND_FILE.relative_to(ROOT).as_posix(),'bytes':CAND_FILE.stat().st_size,'sha256':sha(CAND_FILE.read_bytes())};context_info={'path':CONTEXT_FILE.relative_to(ROOT).as_posix(),'bytes':CONTEXT_FILE.stat().st_size,'sha256':sha(CONTEXT_FILE.read_bytes())};request_info={'path':REQUEST_FILE.relative_to(ROOT).as_posix(),'bytes':len(request_bytes),'sha256':sha(request_bytes)}
 delivery={'id':'RANK9-ALIGNMENT-FACTION-PURIFICATION5-CURRENT-SOURCE-DELIVERY-248','status':'PREPARED_UNAUDITED_UNSENT','archive':archive_info,'members':len(rows)+1,'manifestBindings':len(rows),'sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':TARGETS,'accepted':False,'applied':False,'candidate':candidate_info,'context':context_info,'request':request_info,'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'sourceBindings':130,'changedSourceBindings':changed,'priorAFP211ContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','previousReturn247':{'archive':r247info,'heldIds':['eternal-forge','matter-conversion'],'blockers':['MF210-B01','MF210-B02'],'audit':r247ainfo},'previousReturn246':{'archive':r246info,'heldIds':['soul-reflection'],'blockers':['IR207-B02'],'audit':r246ainfo},'previousReturn245':{'archive':r245info,'heldIds':['reverse-gravity-field'],'blockers':['IE204-B02'],'audit':r245ainfo},'conversation':CHAT}
 delivery_bytes=enc(delivery);DELIVERY.write_bytes(delivery_bytes)
 prep={'id':'RANK9ALIGNFACTIONPURIFICATION5-SOURCE-PREPARATION-248','recordedAtUtc':now,'status':'PREPARED_UNAUDITED_UNSENT','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'targetGroup':GROUP,'pendingIds':TARGETS,'archive':archive_info,'deliveryManifest':info(DELIVERY,delivery_bytes),'candidate':candidate_info,'context':context_info,'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'refreshedSourceBindings':130,'changedHistoricalBindings':changed,'originalQuestions':28,'focusedAdditionalQuestions':0,'futureCaseRequirements':7,'printedPlacements':6,'newRuleAdoptions':0,'previousContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','previousReturns':{'return247':{'heldIds':['eternal-forge','matter-conversion'],'auditStatus':r247audit['status']},'return246':{'heldIds':['soul-reflection'],'auditStatus':r246audit['status']},'return245':{'heldIds':['reverse-gravity-field'],'auditStatus':r245audit['status']}},'canonicalChanges':False,'accepted':False,'applied':False}
 PREP.write_bytes(enc(prep))
 packet={'id':'RANK9ALIGNFACTIONPURIFICATION5-PACKET-248','status':'PREPARED_UNAUDITED_UNSENT','group':GROUP,'pendingIds':TARGETS,'sourceAuthority':AUTH,'sourceBranch':branch,'sourceCommit':head,'archive':archive_info,'deliveryManifest':info(DELIVERY,delivery_bytes),'candidate':candidate_info,'originalQuestions':28,'focusedAdditionalQuestions':0,'totalQuestions':28,'futureCaseRequirements':7,'printedPlacements':6,'refreshedSourceBindings':130,'previousBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','priorReturn247OutsideScope':{'heldIds':['eternal-forge','matter-conversion'],'blockers':['MF210-B01','MF210-B02']},'priorReturn246OutsideScope':{'heldIds':['soul-reflection'],'blocker':'IR207-B02'},'priorReturn245OutsideScope':{'heldIds':['reverse-gravity-field'],'blocker':'IE204-B02'},'canonicalChanges':False,'independentAudit':None}
 PACKET.write_bytes(enc(packet))
 # Point live tracking at packet248 while keeping it explicitly unaudited and unapplied.
 q=read(QUEUE248); info_delivery=info(DELIVERY,delivery_bytes);info_prep=info(PREP,PREP.read_bytes())
 q['nextPreparedRequest'].update({'status':'PACKET248_PREPARED_UNAUDITED_UNSENT','packet':archive_info,'deliveryManifest':info_delivery,'candidate':candidate_info,'sourcePreparation':info_prep})
 q['currentPacket']=archive_info;q['currentDeliveryManifest']=info_delivery;q['currentPreparation']=info_prep;q['status']='PACKET248_PREPARED_UNAUDITED_811_37_0';q['packetStatus']='PACKET248_PREPARED_UNAUDITED_811_37_0'
 QUEUE248.write_bytes(enc(q))
 h=read(HANDOFF248);h['nextPreparedRequest']=q['nextPreparedRequest'];h['currentPacket']=archive_info;h['currentPacketDelivery']=info_delivery;h['currentPreparation']=info_prep;h['currentQueueBinding']=info(QUEUE248,QUEUE248.read_bytes());h['status']='PACKET248_PREPARED_UNAUDITED_811_37';h['resumePriority']='Independently audit packet248 before submitting to GPT; monitor browser, send focused pings if needed, audit the sealed return, and apply only exact accepted IDs.';HANDOFF248.write_bytes(enc(h))
 old=(ROOT/'START_HERE.md').read_text(encoding='utf-8-sig').splitlines();old[0]=f'**Current ordinary spell-review handoff [248](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_248.json):** Return247 independently audited PASS 19/19 and held eternal-forge and matter-conversion; authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. Fresh packet248 for only alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection and corruption-purification is prepared for independent audit; reassess AFP211-B01 through AFP211-B05 while preserving closed AFP211-E01 and all other holds.'
 (ROOT/'START_HERE.md').write_text('\n'.join(old)+'\n',encoding='utf-8')
 print(json.dumps({'status':'PREPARED_UNAUDITED_UNSENT','sourceCommit':head,'branch':branch,'authority':AUTH,'targets':TARGETS,'sourceBindings':len(refreshed),'changedBindings':changed,'originalQuestions':28,'futureRequirements':7,'members':len(rows)+1,'archiveBytes':archive_info['bytes'],'archiveSha256':archive_info['sha256'],'deliveryBytes':DELIVERY.stat().st_size,'out':str(ARCHIVE)},indent=2))
if __name__=='__main__':main()
