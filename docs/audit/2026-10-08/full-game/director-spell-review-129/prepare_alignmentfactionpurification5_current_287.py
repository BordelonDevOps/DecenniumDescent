from __future__ import annotations
import copy, hashlib, json, subprocess, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
FULL=ROOT/'docs/audit/2026-10-08/full-game'
AUDIT=FULL/'director-spell-review-129'
GROUP='rank9-alignment-faction-purification5'
TARGETS=['alignment-ascension','alignment-perfection','faction-incarnate','faction-perfection','corruption-purification']
AUTH={'reviewedApplied':816,'pending':32,'acceptedUnapplied':0,'completeStandaloneProcedures':540,'scopedInterfaces':173}
BRANCH='main'
INDEX='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
CANDIDATE='DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_alignment_faction_purification_5_source_conference_02.json'
HIST_ARCHIVE=FULL/'DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_02.zip'
PREPARATION=FULL/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_PREPARATION.json'
CHECK=FULL/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_CHECK.json'
REQUEST=FULL/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_REQUEST.txt'
SUBMISSION=FULL/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_SUBMISSION_211.json'
R286=AUDIT/'rank9_impactexile4_return286_received'
R286_ZIP=R286/'DD_Rank9_ImpactExile4_Director_Return286_HELD.zip'; R286_DELIVERY=R286/'DD_Rank9_ImpactExile4_Director_Return286_HELD_DELIVERY.json'
R286_AUDIT=AUDIT/'RANK9IMPACTEXILE4_RETURN286_INDEPENDENT_AUDIT.json'; R286_RECEIPT=AUDIT/'RANK9IMPACTEXILE4_RETURN286_RECEIPT.json'; R286_SUBMISSION=AUDIT/'RANK9IMPACTEXILE4_PACKET_286.json'
R285=AUDIT/'rank9_summonhosts5_return285_received'; R285_ZIP=R285/'DD_Rank9_SummonHosts5_Director_Return285_HELD.zip'; R285_DELIVERY=R285/'DD_Rank9_SummonHosts5_Director_Return285_HELD_DELIVERY.json'
R285_AUDIT=AUDIT/'RANK9SUMMONHOSTS5_RETURN285_INDEPENDENT_AUDIT.json'; R285_RECEIPT=AUDIT/'RANK9SUMMONHOSTS5_RETURN285_RECEIPT.json'
R284=AUDIT/'rank9_planargates5_return284_received'; R284_ZIP=R284/'DD_Rank9_PlanarGates5_Director_Return284_HELD.zip'; R284_DELIVERY=R284/'DD_Rank9_PlanarGates5_Director_Return284_HELD_DELIVERY.json'
R284_AUDIT=AUDIT/'RANK9_PLANARGATES5_RETURN284_INDEPENDENT_AUDIT.json'; R284_RECEIPT=AUDIT/'RANK9_PLANARGATES5_RETURN284_RECEIPT.json'
QUEUE286=AUDIT/'CURRENT_SPELL_QUEUE_286.json'; HANDOFF286=AUDIT/'CURRENT_HANDOFF_286.json'; PENDING286=AUDIT/'CURRENT32_PENDING_IDENTITY_AUDIT_286.json'
OUT=AUDIT/'rank9_alignmentfactionpurification5_current_source_287_prepared'
ARCHIVE=OUT/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287.zip'; DELIVERY=OUT/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287_DELIVERY.json'
CAND_FILE=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json'; CONTEXT_FILE=OUT/'CURRENT_CONTEXT_287.json'; REQUEST_FILE=OUT/'REQUEST_287.txt'
QUEUE287=AUDIT/'CURRENT_SPELL_QUEUE_287.json'; HANDOFF287=AUDIT/'CURRENT_HANDOFF_287.json'; PENDING287=AUDIT/'CURRENT32_PENDING_IDENTITY_AUDIT_287.json'; SNAPSHOT287=AUDIT/'CURRENT_SPELL_REVIEW_SNAPSHOT_287.md'
PREP=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_SOURCE_PREPARATION_287.json'; PACKET=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287.json'
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
 index=read(ROOT/INDEX); catalog=read(ROOT/CATALOG); q0=read(QUEUE286); h0=read(HANDOFF286); p0=read(PENDING286); hist=read(ROOT/CANDIDATE)
 assert q0['currentAuthority']==h0['currentAuthority']==p0['authority']==AUTH and p0['pendingCount']==32
 pending=sorted(x['id'] for x in index['entries'] if x.get('authoredStatus')=='pending-authored-procedure')
 assert len(pending)==32 and pending==sorted(p0['pendingIds'])
 assert index['authoredCounts']=={'reviewed':816,'pending':32} and index['representationCounts']['completeReviewedStandaloneProcedures']==540
 entries={x['id']:x for x in index['entries']}; spells={x['id']:x for x in catalog['spells']}
 assert all(s in spells and entries[s]['authoredStatus']=='pending-authored-procedure' and entries[s]['sourceStatus']=='blocked-pending-operational-review' for s in TARGETS)
 group=targetrow(q0['currentPendingGroups']); assert group['pendingIds']==TARGETS and group['pendingCount']==5
 r286audit=read(R286_AUDIT); r286d=read(R286_DELIVERY); r286sub=read(R286_SUBMISSION)
 assert r286audit['status']=='PASS' and r286audit['checkCount']==16 and r286d['heldIds']==['reverse-gravity-field'] and r286d['blockerIds']=={'reverse-gravity-field':['IE204-B02']} and r286d['applied'] is False and r286sub['status']=='RETURN286_AUDITED_HELD_NEXT_ALIGNMENT_FACTION_PURIFICATION5_816_32_0'
 r285audit=read(R285_AUDIT); r285d=read(R285_DELIVERY); r285r=read(R285_RECEIPT)
 r284audit=read(R284_AUDIT); r284d=read(R284_DELIVERY); r284r=read(R284_RECEIPT)
 assert r285audit['status']=='PASS' and r285d['heldIds']==['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'] and r285d['applied'] is False
 assert r284audit['status']=='PASS' and r284d['heldIds']==['banishment-gate','conjure-demiplane-fortress'] and r284d['applied'] is False
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
 # Freeze the independently audited Return286 and current authority before preparing the next request.
 def fi(p): return info(p)
 r286info=fi(R286_ZIP); r286dinfo=fi(R286_DELIVERY); r286ainfo=fi(R286_AUDIT); r286rinfo=fi(R286_RECEIPT)
 r285info=fi(R285_ZIP); r285dinfo=fi(R285_DELIVERY); r285ainfo=fi(R285_AUDIT); r285rinfo=fi(R285_RECEIPT)
 r284info=fi(R284_ZIP); r284dinfo=fi(R284_DELIVERY); r284ainfo=fi(R284_AUDIT); r284rinfo=fi(R284_RECEIPT)
 pending_audit=copy.deepcopy(p0)
 pending_audit.update({'id':'CURRENT32-PENDING-IDENTITY-AUDIT-287','recordedAtUtc':now,'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN286','lastDirectorReturn':{'archive':r286info,'deliveryManifest':r286dinfo,'independentAudit':r286ainfo,'receipt':r286rinfo,'acceptedIds':[],'appliedIds':[],'heldIds':['reverse-gravity-field'],'blockerIds':{'reverse-gravity-field':['IE204-B02']}},'preparedNextGroup':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':5,'historicalContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','freshPacketRequiredForCurrentAuthority':True}})
 PENDING287.write_bytes(enc(pending_audit))
 queue=copy.deepcopy(q0)
 queue.update({'id':'SPELL-REVIEW-QUEUE-287','recordedAtUtc':now,'supersedesQueue':'SPELL-REVIEW-QUEUE-286','pendingIdentityAudit':fi(PENDING287),'currentReturnAudit':r286ainfo,'currentReturnDelivery':r286dinfo,'currentReturnArchive':r286info,'currentReturnDecision':'RANK9-IMPACTEXILE4-DIRECTOR-RETURN286','currentReturnReceipt':r286rinfo,'currentReturnBinding':r286info,'currentReturnSourceArchive':q0.get('currentPacket'),'currentReturnSourceDelivery':q0.get('currentDeliveryManifest'),'currentPacketAudit':r286ainfo,'currentPacketAuditReceipt':r286rinfo,'packetStatus':'RETURN286_AUDITED_HELD_NEXT_ALIGNMENT_FACTION_PURIFICATION5_816_32_0','status':'RETURN286_AUDITED_HELD_NEXT_ALIGNMENT_FACTION_PURIFICATION5_816_32_0','nextGroup':GROUP,'next':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':5,'status':'FRESH_CURRENT_PACKET_REQUIRED_AT_AUTHORITY_816_32_0','freshPacketRequiredForCurrentAuthority':True},'nextPreparedRequest':{'group':GROUP,'pendingIds':TARGETS,'pendingCount':5,'status':'FRESH_PACKET287_PREPARATION_IN_PROGRESS','freshPacketRequiredForCurrentAuthority':True,'historicalContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','previousReturn286OutsideScope':{'heldIds':['reverse-gravity-field'],'blockerIds':{'reverse-gravity-field':['IE204-B02']},'audit':r286ainfo},'otherPreservedHolds':[{'heldIds':['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'],'blockerIds':{'summon-elemental-avatar':['SH202-B01'],'summon-herald-of-the-planes':['SH202-B02'],'summon-avatar-of-decay':['SH202-B03']},'audit':r285ainfo},{'heldIds':['banishment-gate','conjure-demiplane-fortress'],'blockerIds':{'banishment-gate':['PG200-B03','PG200-B04'],'conjure-demiplane-fortress':['PG200-B06']},'audit':r284ainfo}],'packet':None,'deliveryManifest':None,'independentAudit':None,'auditReceipt':None},'lastReviewedBatch':{'group':'rank9-impact-exile4','pendingIds':['reverse-gravity-field'],'acceptedIds':[],'appliedIds':[],'heldIds':['reverse-gravity-field'],'blockerIds':{'reverse-gravity-field':['IE204-B02']},'returnArchive':r286info,'returnAudit':r286ainfo},'githubChanges':False})
 target_row=targetrow(queue['currentPendingGroups']); target_row.update({'status':'FRESH_PACKET287_PREPARATION_IN_PROGRESS_816_32_0','freshPacketRequiredForCurrentAuthority':True,'currentAuthority':AUTH,'previousHeldBatch':{'ids':['reverse-gravity-field'],'blockers':{'reverse-gravity-field':['IE204-B02']},'acceptedIds':[],'appliedIds':[]},'previousReturn286':r286info})
 QUEUE287.write_bytes(enc(queue))
 handoff=copy.deepcopy(h0)
 handoff.update({'id':'CURRENT-HANDOFF-287','recordedAtUtc':now,'status':'RETURN286_AUDITED_HELD_PACKET287_PREPARATION_816_32','currentAuthority':AUTH,'pendingIdentityAudit':fi(PENDING287),'queue':fi(QUEUE287),'currentQueueBinding':fi(QUEUE287),'currentReturnBinding':r286info,'currentReturnDelivery':r286dinfo,'currentReturnAudit':r286ainfo,'currentReturnReceipt':r286rinfo,'currentReturnDecision':'RANK9-IMPACTEXILE4-DIRECTOR-RETURN286','latestBatch':{'group':'rank9-impact-exile4','pendingIds':['reverse-gravity-field'],'acceptedIds':[],'appliedIds':[],'heldIds':['reverse-gravity-field'],'blockerIds':{'reverse-gravity-field':['IE204-B02']},'returnArchive':r286info,'independentAudit':r286ainfo},'nextStep':'Prepare, independently audit, and submit a fresh 816/32 current-source packet287 to GPT for only the five Rank9 Alignment/Faction Purification identities. Reassess AFP211-B01 through AFP211-B05 against current sources, preserve closed AFP211-E01 and every unrelated hold, audit the sealed return, then apply only exact accepted IDs.','nextGroup':GROUP,'nextPendingCount':5,'unacceptedThisStep':['reverse-gravity-field'],'currentPacket':None,'currentPacketDelivery':None,'currentPacketAudit':None,'currentPacketAuditReceipt':None,'nextPreparedRequest':queue['nextPreparedRequest'],'githubChanges':False,'resumePriority':'Build and independently audit packet287, send it to GPT, check browser progress frequently and ping again if needed, then audit the sealed director return before considering any exact accepted IDs.'})
 HANDOFF287.write_bytes(enc(handoff))
 SNAPSHOT287.write_text(f'# Current Ordinary Spell Review Snapshot 287\n\nAuthority: **816 reviewed/applied / 32 pending / 0 accepted-unapplied**; 540 complete standalone procedures and 173 scoped interfaces.\n\nReturn286 independently passed 16/16 and held reverse-gravity-field (IE204-B02); no acceptance or application occurred. The next group is **Rank9 Alignment/Faction Purification5**: {", ".join(TARGETS)}. Reassess AFP211-B01 through AFP211-B05; retain the closed shared-evidence finding AFP211-E01 and all unrelated holds.\n\nReturn285 Summon Hosts holds and Return284 Planar Gates holds remain unchanged outside scope. This packet does not amend canonical files or open runtime, implementation, human-play, balance, cosmology, domain, completion or release gates.\n',encoding='utf-8')
 # Refresh the full source candidate with current authority and exact target catalog/index entries.
 candidate=copy.deepcopy(hist)
 candidate.update({'id':'CURRENT-SOURCE-CONFERENCE-CANDIDATE-287','recordedAtUtc':now,'status':'PREPARED_CURRENT_AUTHORITY_816_32_EXACT_ALIGNMENT_FACTION_PURIFICATION5_GROUP','currentSourceCommit':head,'currentBranch':branch,'currentWorkingTreeSnapshot':True,'currentAuthority':AUTH,'currentPendingGroup':{'group':GROUP,'spellIds':TARGETS,'count':5},'historicalSourceBindings':copy.deepcopy(hist['sourceBindings']),'sourceBindings':refreshed,'sourceBindingRefresh':{'sourceFiles':len(refreshed),'changedSinceHistoricalCandidate':changed,'sourceContentsFromCurrentWorkingTree':True,'sourceCommitBase':head},'records':[copy.deepcopy(r) for r in hist['records']],'priorAFP211DispositionToReassess':{'contentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','reassessAgainstCurrentSources':True},'priorReturn286OutsideScope':{'heldIds':['reverse-gravity-field'],'blockerIds':{'reverse-gravity-field':['IE204-B02']},'archive':r286info,'delivery':r286dinfo,'audit':r286ainfo,'receipt':r286rinfo},'priorReturn285OutsideScope':{'heldIds':['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'],'blockerIds':{'summon-elemental-avatar':['SH202-B01'],'summon-herald-of-the-planes':['SH202-B02'],'summon-avatar-of-decay':['SH202-B03']},'archive':r285info,'delivery':r285dinfo,'audit':r285ainfo,'receipt':r285rinfo},'priorReturn284OutsideScope':{'heldIds':['banishment-gate','conjure-demiplane-fortress'],'blockerIds':{'banishment-gate':['PG200-B03','PG200-B04'],'conjure-demiplane-fortress':['PG200-B06']},'archive':r284info,'delivery':r284dinfo,'audit':r284ainfo,'receipt':r284rinfo}})
 for r in candidate['records']:
  sid=r['spellId']; r['currentIndexEntry']=copy.deepcopy(entries[sid]); r['completeCurrentCatalogSourceAndAccess']=copy.deepcopy(spells[sid]); r['status']='Pending at current 816/32/0 authority; reassess AFP211 blocker evidence against refreshed current sources.'
 candidate['currentAuthorityEvidence']={'currentIndex':info(ROOT/INDEX),'currentCatalog':info(ROOT/CATALOG),'currentQueue':fi(QUEUE287),'currentHandoff':fi(HANDOFF287),'currentPendingIdentityAudit':fi(PENDING287),'latestReturn286Audit':r286ainfo,'targetIdsStillPending':TARGETS}
 cbytes=enc(candidate)
 context={'id':'RANK9-ALIGNMENT-FACTION-PURIFICATION5-CURRENT-DIRECTOR-CONTEXT-287','recordedAtUtc':now,'sourceCommit':head,'sourceBranch':branch,'currentWorkingTreeSnapshot':True,'sourceAuthority':AUTH,'targetGroup':{'group':GROUP,'pendingIds':TARGETS,'count':5},'currentIndexCounts':index['authoredCounts'],'pendingIdentityAudit':fi(PENDING287),'currentQueue':fi(QUEUE287),'currentHandoff':fi(HANDOFF287),'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'refreshedSourceBindings':130,'changedHistoricalSourceBindings':changed,'preservation':{'originalQuestions':28,'focusedAdditionalQuestions':0,'futureCaseRequirements':7,'sixPrintedPlacementsAcrossFiveIdentities':True,'newRuleAdoptions':0},'previousContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','priorReturn286OutsideScope':{'archive':r286info,'delivery':r286dinfo,'audit':r286ainfo,'receipt':r286rinfo,'heldIds':['reverse-gravity-field'],'blockerIds':{'reverse-gravity-field':['IE204-B02']}},'priorReturn285OutsideScope':{'archive':r285info,'delivery':r285dinfo,'audit':r285ainfo,'receipt':r285rinfo,'heldIds':['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'],'blockerIds':{'summon-elemental-avatar':['SH202-B01'],'summon-herald-of-the-planes':['SH202-B02'],'summon-avatar-of-decay':['SH202-B03']}},'priorReturn284OutsideScope':{'archive':r284info,'delivery':r284dinfo,'audit':r284ainfo,'receipt':r284rinfo,'heldIds':['banishment-gate','conjure-demiplane-fortress'],'blockerIds':{'banishment-gate':['PG200-B03','PG200-B04'],'conjure-demiplane-fortress':['PG200-B06']}},'canonicalChanges':False,'runtimeExecuted':False,'applyChanges':False}
 request=(f'GPT director — continue the ordinary spell review at current authority 816 reviewed/applied / 32 pending / 0 accepted-unapplied (540 complete standalone procedures; 173 scoped interfaces). Review ONLY alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection, and corruption-purification in rank9-alignment-faction-purification5.\n\n'
  f'This packet snapshots branch {branch}, HEAD {head}, and refreshed current working-tree source bytes. Use all 130 refreshed source bindings, current catalog/index/access, queue287/handoff287/pending audit287, the complete source conference02 archive, all 28 original questions and seven future-case requirements. Preserve all six printed placements across the five identities and every native class route, cost, source, lifecycle, and accepted-interface boundary. No new rules are preselected.\n\n'
  'Reassess historical content blockers AFP211-B01 through AFP211-B05 against current sources and evidence. AFP211-E01 is recorded as closed shared evidence; verify and preserve that disposition. Return286 held reverse-gravity-field under IE204-B02; Return285 held the three Summon Hosts identities under SH202-B01/B02/B03; Return284 held banishment-gate and conjure-demiplane-fortress under PG200-B03/B04/B06. All remain outside this packet and must stay unchanged.\n\n'
  'Select dispositions for every original question; distinguish source facts from incomplete integrated witness coverage; report source-linked procedures, useful positive cases, meaningful adverse branches, all forward/inverse replay totals, and exact acceptance/hold decisions with minimum missing witnesses. Do not invent unstated values, reputation scales, permissions, class access, profiles, targets or cosmology. Do not change canonical files, apply decisions, or run supplied programs. Keep runtime, implementation, human-play, balance, cosmology, domain, completion and release gates closed. Return a sealed decision ZIP with matching DELIVERY.json and the exact next pending group. Continue through response caps until both files are attached.' )
 request_bytes=request.encode('utf-8')
 # Snapshot current root plus group-specific preparation and all prior-return boundaries.
 current_paths=[
  'START_HERE.md',INDEX,CATALOG,
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_286.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_286.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_286.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_RETURN286_INDEPENDENT_AUDIT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_RETURN286_RECEIPT.json',
  'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_PACKET_286.json',
  'docs/audit/2026-10-08/full-game/RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_CHECK.json',
  'docs/audit/2026-10-08/full-game/RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_PREPARATION.json',
  'docs/audit/2026-10-08/full-game/RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_REQUEST.txt',
  'docs/audit/2026-10-08/full-game/RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_SUBMISSION_211.json',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_02_SUBMISSION_210.json',
  'docs/audit/2026-10-08/full-game/RANK9_MATERIAL_FORGING_2_SOURCE_PROVENANCE_RECONCILIATION_210.json'
 ]
 current_files={p:(ROOT/p).read_bytes() for p in current_paths if (ROOT/p).exists()}
 current_files[CANDIDATE]=(ROOT/CANDIDATE).read_bytes()
 current_files[QUEUE287.relative_to(ROOT).as_posix()]=QUEUE287.read_bytes()
 current_files[HANDOFF287.relative_to(ROOT).as_posix()]=HANDOFF287.read_bytes()
 current_files[PENDING287.relative_to(ROOT).as_posix()]=PENDING287.read_bytes()
 current_files[PREPARATION.relative_to(ROOT).as_posix()]=PREPARATION.read_bytes()
 current_files[CHECK.relative_to(ROOT).as_posix()]=CHECK.read_bytes()
 evidence={
  'evidence/RETURN286.zip':R286_ZIP.read_bytes(),'evidence/RETURN286_DELIVERY.json':R286_DELIVERY.read_bytes(),'evidence/RETURN286_INDEPENDENT_AUDIT.json':R286_AUDIT.read_bytes(),'evidence/RETURN286_RECEIPT.json':R286_RECEIPT.read_bytes(),
  'evidence/RETURN285.zip':R285_ZIP.read_bytes(),'evidence/RETURN285_DELIVERY.json':R285_DELIVERY.read_bytes(),'evidence/RETURN285_INDEPENDENT_AUDIT.json':R285_AUDIT.read_bytes(),'evidence/RETURN285_RECEIPT.json':R285_RECEIPT.read_bytes(),
  'evidence/RETURN284.zip':R284_ZIP.read_bytes(),'evidence/RETURN284_DELIVERY.json':R284_DELIVERY.read_bytes(),'evidence/RETURN284_INDEPENDENT_AUDIT.json':R284_AUDIT.read_bytes(),'evidence/RETURN284_RECEIPT.json':R284_RECEIPT.read_bytes()
 }
 out_files={'CURRENT_CONTEXT_287.json':enc(context),'CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json':cbytes,'REQUEST_287.txt':request_bytes,'historical/DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_02.zip':histzip}
 for path,raw in current_files.items():out_files['current/'+path]=raw
 for name,raw in source_files.items():out_files[name]=raw
 out_files.update(evidence)
 for name in out_files:assert safe(name),name
 OUT.mkdir(parents=True,exist_ok=True)
 CAND_FILE.write_bytes(cbytes);CONTEXT_FILE.write_bytes(enc(context));REQUEST_FILE.write_bytes(request_bytes)
 rows=[]
 with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,raw in sorted(out_files.items()):z.writestr(name,raw);rows.append({'path':name,'bytes':len(raw),'sha256':sha(raw),'crc32':crc(raw)})
  manifest={'id':'RANK9-ALIGNMENT-FACTION-PURIFICATION5-CURRENT-SOURCE-MANIFEST-287','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':TARGETS,'memberCountExcludingSelf':len(rows),'members':rows}
  z.writestr('MANIFEST.json',enc(manifest))
 with zipfile.ZipFile(ARCHIVE) as z:
  assert z.testzip() is None and len(z.namelist())==len(rows)+1==len(set(z.namelist()))
  for row in rows:
   raw=z.read(row['path']);assert (len(raw),sha(raw),crc(raw))==(row['bytes'],row['sha256'],row['crc32'])
 archive_info=info(ARCHIVE);candidate_info={'path':CAND_FILE.relative_to(ROOT).as_posix(),'bytes':CAND_FILE.stat().st_size,'sha256':sha(CAND_FILE.read_bytes())};context_info={'path':CONTEXT_FILE.relative_to(ROOT).as_posix(),'bytes':CONTEXT_FILE.stat().st_size,'sha256':sha(CONTEXT_FILE.read_bytes())};request_info={'path':REQUEST_FILE.relative_to(ROOT).as_posix(),'bytes':len(request_bytes),'sha256':sha(request_bytes)}
 delivery={'id':'RANK9-ALIGNMENT-FACTION-PURIFICATION5-CURRENT-SOURCE-DELIVERY-287','status':'PREPARED_UNAUDITED_UNSENT','archive':archive_info,'members':len(rows)+1,'manifestBindings':len(rows),'sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'group':GROUP,'pendingIds':TARGETS,'accepted':False,'applied':False,'candidate':candidate_info,'context':context_info,'request':request_info,'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'sourceBindings':130,'changedSourceBindings':changed,'priorAFP211ContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','previousReturn286':{'archive':r286info,'heldIds':['reverse-gravity-field'],'blockers':{'reverse-gravity-field':['IE204-B02']},'audit':r286ainfo},'previousReturn285':{'archive':r285info,'heldIds':['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'],'blockers':{'summon-elemental-avatar':['SH202-B01'],'summon-herald-of-the-planes':['SH202-B02'],'summon-avatar-of-decay':['SH202-B03']},'audit':r285ainfo},'previousReturn284':{'archive':r284info,'heldIds':['banishment-gate','conjure-demiplane-fortress'],'blockers':{'banishment-gate':['PG200-B03','PG200-B04'],'conjure-demiplane-fortress':['PG200-B06']},'audit':r284ainfo},'conversation':CHAT}
 delivery_bytes=enc(delivery);DELIVERY.write_bytes(delivery_bytes)
 prep={'id':'RANK9ALIGNFACTIONPURIFICATION5-SOURCE-PREPARATION-287','recordedAtUtc':now,'status':'PREPARED_UNAUDITED_UNSENT','sourceCommit':head,'sourceBranch':branch,'sourceAuthority':AUTH,'targetGroup':GROUP,'pendingIds':TARGETS,'archive':archive_info,'deliveryManifest':info(DELIVERY,delivery_bytes),'candidate':candidate_info,'context':context_info,'historicalCandidate':info(ROOT/CANDIDATE),'historicalSourceArchive':info(HIST_ARCHIVE,histzip),'refreshedSourceBindings':130,'changedHistoricalBindings':changed,'originalQuestions':28,'focusedAdditionalQuestions':0,'futureCaseRequirements':7,'printedPlacements':6,'newRuleAdoptions':0,'previousContentBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','previousReturns':{'return286':{'heldIds':['reverse-gravity-field'],'blockerIds':{'reverse-gravity-field':['IE204-B02']},'auditStatus':r286audit['status']},'return285':{'heldIds':['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'],'blockerIds':{'summon-elemental-avatar':['SH202-B01'],'summon-herald-of-the-planes':['SH202-B02'],'summon-avatar-of-decay':['SH202-B03']},'auditStatus':r285audit['status']},'return284':{'heldIds':['banishment-gate','conjure-demiplane-fortress'],'blockerIds':{'banishment-gate':['PG200-B03','PG200-B04'],'conjure-demiplane-fortress':['PG200-B06']},'auditStatus':r284audit['status']}},'canonicalChanges':False,'accepted':False,'applied':False}
 PREP.write_bytes(enc(prep))
 packet={'id':'RANK9ALIGNFACTIONPURIFICATION5-PACKET-287','status':'PREPARED_UNAUDITED_UNSENT','group':GROUP,'pendingIds':TARGETS,'sourceAuthority':AUTH,'sourceBranch':branch,'sourceCommit':head,'archive':archive_info,'deliveryManifest':info(DELIVERY,delivery_bytes),'candidate':candidate_info,'originalQuestions':28,'focusedAdditionalQuestions':0,'totalQuestions':28,'futureCaseRequirements':7,'printedPlacements':6,'refreshedSourceBindings':130,'previousBlockers':['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'],'closedSharedEvidenceBlocker':'AFP211-E01','priorReturn286OutsideScope':{'heldIds':['reverse-gravity-field'],'blockerIds':{'reverse-gravity-field':['IE204-B02']}},'priorReturn285OutsideScope':{'heldIds':['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'],'blockerIds':{'summon-elemental-avatar':['SH202-B01'],'summon-herald-of-the-planes':['SH202-B02'],'summon-avatar-of-decay':['SH202-B03']}},'priorReturn284OutsideScope':{'heldIds':['banishment-gate','conjure-demiplane-fortress'],'blockerIds':{'banishment-gate':['PG200-B03','PG200-B04'],'conjure-demiplane-fortress':['PG200-B06']}},'canonicalChanges':False,'independentAudit':None}
 PACKET.write_bytes(enc(packet))
 # Point live tracking at packet287 while keeping it explicitly unaudited and unapplied.
 q=read(QUEUE287); info_delivery=info(DELIVERY,delivery_bytes);info_prep=info(PREP,PREP.read_bytes())
 q['nextPreparedRequest'].update({'status':'PACKET287_PREPARED_UNAUDITED_UNSENT','packet':archive_info,'deliveryManifest':info_delivery,'candidate':candidate_info,'sourcePreparation':info_prep})
 q['currentPacket']=archive_info;q['currentDeliveryManifest']=info_delivery;q['currentPreparation']=info_prep;q['status']='PACKET287_PREPARED_UNAUDITED_816_32_0';q['packetStatus']='PACKET287_PREPARED_UNAUDITED_816_32_0'
 QUEUE287.write_bytes(enc(q))
 h=read(HANDOFF287);h['nextPreparedRequest']=q['nextPreparedRequest'];h['currentPacket']=archive_info;h['currentPacketDelivery']=info_delivery;h['currentPreparation']=info_prep;h['currentQueueBinding']=info(QUEUE287,QUEUE287.read_bytes());h['status']='PACKET287_PREPARED_UNAUDITED_816_32';h['resumePriority']='Independently audit packet287 before submitting to GPT; monitor browser, send focused pings if needed, audit the sealed return, and apply only exact accepted IDs.';HANDOFF287.write_bytes(enc(h))
 old=(ROOT/'START_HERE.md').read_text(encoding='utf-8-sig').splitlines();old[0]=f'**Current ordinary spell-review handoff [287](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_287.json):** Return286 independently audited PASS 16/16 and held reverse-gravity-field under IE204-B02; authority remains **816 reviewed-applied / 32 pending / 0 accepted-unapplied**. Fresh packet287 for only alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection and corruption-purification is prepared for independent audit; reassess AFP211-B01 through AFP211-B05 while preserving closed AFP211-E01 and all other holds.'
 (ROOT/'START_HERE.md').write_text('\n'.join(old)+'\n',encoding='utf-8')
 print(json.dumps({'status':'PREPARED_UNAUDITED_UNSENT','sourceCommit':head,'branch':branch,'authority':AUTH,'targets':TARGETS,'sourceBindings':len(refreshed),'changedBindings':changed,'originalQuestions':28,'futureRequirements':7,'members':len(rows)+1,'archiveBytes':archive_info['bytes'],'archiveSha256':archive_info['sha256'],'deliveryBytes':DELIVERY.stat().st_size,'out':str(ARCHIVE)},indent=2))
if __name__=='__main__':main()
