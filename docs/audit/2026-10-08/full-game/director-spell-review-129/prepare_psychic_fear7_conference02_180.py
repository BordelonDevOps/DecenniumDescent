from __future__ import annotations
import copy, hashlib, json, subprocess, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / 'docs/audit/2026-10-08/full-game'
AUD = FULL / 'director-spell-review-129'
IDS = ['phantom-armageddon','phantom-cataclysm','psychic-scream','frightful-sovereignty','mass-phantom-killer','weird','reality-break']
AUTH = {'reviewedApplied':755,'pending':93,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':479,'scopedInterfaces':173}
OLD_CANDIDATE = ROOT / 'DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_psychic_fear_7_source_conference_01.json'
OLD_ARCHIVE = FULL / 'DD_Rank9_Psychic_Fear_7_Source_Conference_01.zip'
OLD_NOTES = AUD / 'RANK9PSYCHICFEAR7_NEXT_CONFERENCE_NOTES_129.json'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE = AUD / 'CURRENT_SPELL_QUEUE_179.json'
HANDOFF = AUD / 'CURRENT_HANDOFF_179.json'
PENDING = AUD / 'CURRENT93_PENDING_IDENTITY_AUDIT_179.json'
LATEST = [
 AUD/'RANK9_STORMCONTROL6_APPLICATION_179.json',
 AUD/'RANK9_STORMCONTROL6_EXACT_ACCEPTANCE_177.json',
 AUD/'RANK9_STORMCONTROL6_APPLICATION_VALIDATION_179.json',
 AUD/'RANK9_STORMCONTROL6_GPT_RETURN_177.json',
 ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9stormcontrol6_reviewed_177/MODEL.json',
 AUD/'rank9_stormcontrol6_return177_received/DD_Rank9_StormControl6_Director_Return177.zip'
]
CANDIDATE = ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_psychic_fear_7_source_conference_02_180.json'
OUTPUT = FULL/'rank9-psychic-fear7-source-conference-02-180'
ARCHIVE = FULL/'DD_Rank9_Psychic_Fear_7_Source_Conference_02_180.zip'
CHECK = FULL/'RANK9_PSYCHIC_FEAR7_SOURCE_CONFERENCE_02_CHECK_180.json'
PREP = FULL/'RANK9_PSYCHIC_FEAR7_SOURCE_CONFERENCE_02_PREPARATION_180.json'
REQUEST = FULL/'RANK9_PSYCHIC_FEAR7_SOURCE_CONFERENCE_02_REQUEST_180.txt'
NOTES = AUD/'RANK9PSYCHICFEAR7_NEXT_CONFERENCE_NOTES_180.json'
PENDING_AFTER = AUD/'CURRENT93_PENDING_IDENTITY_AUDIT_180.json'
QUEUE_AFTER = AUD/'CURRENT_SPELL_QUEUE_180.json'
HANDOFF_AFTER = AUD/'CURRENT_HANDOFF_180.json'
CACHE = {}

def enc(obj): return (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(raw): return hashlib.sha256(raw).hexdigest()
def repository_bytes(path):
 rel=path.resolve().relative_to(ROOT).as_posix()
 if rel not in CACHE:
  try: CACHE[rel]=subprocess.check_output(['git','cat-file','blob',f'HEAD:{rel}'],cwd=ROOT,stderr=subprocess.DEVNULL)
  except subprocess.CalledProcessError: CACHE[rel]=path.read_bytes()
 return CACHE[rel]
def bind(path, rel=None):
 raw=repository_bytes(path)
 return {'path':rel or path.resolve().relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
def write(path, raw): path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(raw)
def resolve_pointer(obj,pointer):
 cur=obj
 for part in pointer.strip('/').split('/') if pointer else []:
  part=part.replace('~1','/').replace('~0','~')
  cur=cur[int(part)] if isinstance(cur,list) else cur[part]
 return cur

def main():
 outputs=[CANDIDATE,OUTPUT,ARCHIVE,CHECK,PREP,REQUEST,NOTES,PENDING_AFTER,QUEUE_AFTER,HANDOFF_AFTER]
 assert not any(p.exists() for p in outputs), 'Refusing to overwrite an existing fresh conference artifact.'
 index_raw,catalog_raw=INDEX.read_bytes(),CATALOG.read_bytes()
 index,catalog,queue,handoff,pending,old,old_notes=map(read,[INDEX,CATALOG,QUEUE,HANDOFF,PENDING,OLD_CANDIDATE,OLD_NOTES])
 assert queue['currentAuthority']==handoff['currentAuthority']==AUTH
 assert index['authoredCounts']=={'reviewed':755,'pending':93}
 assert pending['pendingCount']==93 and len(pending['pendingIds'])==93
 assert queue['nextGroup']=='rank9-psychic-fear7' and queue['currentPendingGroups'][0]['group']=='rank9-psychic-fear7'
 group=copy.deepcopy(queue['currentPendingGroups'][0])
 assert group['pendingIds']==IDS and group['pendingCount']==7
 live_pending={r['id'] for r in index['entries'] if r.get('authoredStatus')=='pending-authored-procedure'}
 assert len(live_pending)==93 and set(pending['pendingIds'])==live_pending and set(IDS)<=live_pending
 assert index['representationCounts']['completeReviewedStandaloneProcedures']==479
 assert len(old['records'])==7 and [r['spellId'] for r in old['records']]==IDS
 assert len(old['questions'])==23 and len(old_notes['focusedAdditionalQuestions'])==2
 assert len(old_notes['requiredNewCases'])==14 and all(not q['decisionSelected'] for q in old['questions']+old_notes['focusedAdditionalQuestions'])
 old_archive_raw=OLD_ARCHIVE.read_bytes()
 with zipfile.ZipFile(OLD_ARCHIVE) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
  archived_candidate=z.read('CANDIDATE.json')
  assert json.loads(archived_candidate)==old
 old_raw=repository_bytes(OLD_CANDIDATE)
 assert json.loads(old_raw.decode('utf-8-sig'))==old
 notes=copy.deepcopy(old_notes)
 notes.update({'id':'RANK9PSYCHICFEAR7-INDEPENDENT-CONFERENCE-180','status':'PREPARED_FRESH_UNSENT_NOT_ACCEPTED','currentAppliedCounts':{'reviewed':755,'pending':93,'acceptedUnapplied':0},'preparedAgainst':{'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'index':bind(INDEX),'catalog':bind(CATALOG),'queue':bind(QUEUE),'handoff':bind(HANDOFF),'pendingIdentityAudit':bind(PENDING)}})
 cases=[]
 for sid,reqs in {
  'phantom-armageddon':['Actual rank17 Necromancy route, full60ft enemy area and12d10necrotic with selected independent fear/save admission, truthful hostility and actual geometry.','Genuine damage/fear defenses, unknown fear-source location and exact chosen fear clock, suppression/source death with no locator or repeated blast.'],
  'phantom-cataclysm':['Actual Wizard Illusion source, complete chosen enemy area and subjective world-ending perception,12d10psychic plus native one-round stun under exact admission.','Actual psychic immunity versus stun immunity/used allowance, source-qualified True Seeing, original one-round endpoint and survival/body transition without restored damage.'],
  'psychic-scream':['Actual Wizard Enchantment cast with up to10distinct targets and14d6, positive selected final-death head-remains consequence and real headless/multihead/form/survival/Null branches.','Actual Mage Evocation acquired route and full14d6 plus selected finite stun, genuine immunity/hard-control and damage-before-rider order; preserve unused Illusion placement without granting access.'],
  'frightful-sovereignty':['Actual all-enemy6d6psychic and WIS-governed native three-round flight, known source, complete safe locomotion/path/terrain budget with selected Action rule.','Blocked or unknown-source route, true fear defense, suppression and companion phase, retained movement/Action spending and no free Dash or repeated6d6.'],
  'mass-phantom-killer':['Actual five independent enemy applications and6d6per-round, full selected finite clock and each initial/pulse/endingWIS outcome.','Separate owner overlap, target death or source-qualified form transition, changed hostility/range, suppressed pulse with live ending saves and exact no-bank phase bridge.'],
  'weird':['Actual Wizard Enchantment source,30ft all-creature nightmare captivity with4d10recurrence and complete selected sensory/action/body state including allied exposure.','Actual wake/aid/TrueSeeing and sleep/fear/mental defense predicates, own-damage interaction, independent suppression/endings and retained prior damage through finite escape.'],
  'reality-break':['Actual Wizard Illusion one-target10d12force and complete selected useful secondary-effect procedure, all table operands/weights or declared choice, exact pluralWIS schedule.','Every selected state branch with actual motion/denial/perception predicates, genuine used allowance, source ending/suppression and no rerolled effect or replayed damage.']
 }.items():
  for i,req in enumerate(reqs): cases.append({'id':f'RANK9PSYCHICFEAR7-180-{sid.upper()}-{chr(65+i)}','spellId':sid,'requiredEvidence':req,'status':'REQUIRED_NEW_CASE_NOT_AUTHORED'})
 notes['requiredNewCases']=cases
 notes['scope']='Preparation only. This fresh conference supersedes older pending-count and accepted-comparison labels for exactly these seven identities. No rule adoption, runtime test, human playtest, balance, cosmology, or release approval.'
 NOTES_RAW=enc(notes); write(NOTES,NOTES_RAW)
 index_by={r['id']:r for r in index['entries']}; catalog_by={r['id']:r for r in catalog['spells']}
 historical_refs={k:copy.deepcopy(group[k]) for k in ['candidate','archive'] if k in group}
 current_group=copy.deepcopy(group); current_group.pop('candidate',None); current_group.pop('archive',None); current_group['status']='CURRENT_755_93_SCOPE; fresh conference02 artifacts are recorded separately'
 registry_path=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json'
 registry=read(registry_path)
 source_paths={r['path'] for r in old['sourceBindings']}
 source_paths|={INDEX.relative_to(ROOT).as_posix(),CATALOG.relative_to(ROOT).as_posix(),QUEUE.relative_to(ROOT).as_posix(),HANDOFF.relative_to(ROOT).as_posix(),PENDING.relative_to(ROOT).as_posix(),NOTES.relative_to(ROOT).as_posix(),registry_path.relative_to(ROOT).as_posix()}
 source_paths|={p.relative_to(ROOT).as_posix() for p in LATEST}
 for p in source_paths: assert (ROOT/p).is_file(),f'Missing live source {p}'
 source_bindings=[{**bind(ROOT/rel,rel),'packetPath':f'sources/{i:03d}.bin'} for i,rel in enumerate(sorted(source_paths),1)]
 candidate=copy.deepcopy(old); now=datetime.now(timezone.utc).isoformat()
 candidate.update({'id':'RANK9-PSYCHIC-FEAR7-SOURCE-CONFERENCE02-180','recordedAtUtc':now,'sourceGitBranch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),'sourceGitCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'status':'FRESH_SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'Fresh source context bound to the current 755 applied-reviewed / 93 pending / 0 accepted-unapplied authority. Conference01 remains byte-exact historical context only.','supersedes':'This Conference02 packet controls the current review scope for exactly the seven Psychic Fear identities. Current index, catalog, queue, handoff, pending audit, latest applied batch and live source bindings are refreshed. Conference01 is historical evidence only.','currentAuthority':{**AUTH,'index':bind(INDEX),'catalog':bind(CATALOG),'currentQueue':bind(QUEUE),'currentHandoff':bind(HANDOFF),'pendingIdentityAudit':bind(PENDING),'latestApplication':bind(LATEST[0]),'latestExactAcceptance':bind(LATEST[1]),'latestApplicationValidation':bind(LATEST[2]),'latestDirectorReturnReceipt':bind(LATEST[3]),'latestCandidateModel':bind(LATEST[4]),'latestReturnArchive':bind(LATEST[5])},'countsUnchanged':{'reviewed':755,'pending':93,'acceptedUnapplied':0},'historicalConference01':{'authority':old.get('countsUnchanged'),'workspaceCandidate':bind(OLD_CANDIDATE),'archiveMemberCandidate':{'path':'CANDIDATE.json in historical archive','bytes':len(archived_candidate),'sha256':sha(archived_candidate)},'workspaceVsArchiveCandidate':'Exact candidate content is retained as prior context; Conference01 baseline and comparisons are historical only.','archive':{'path':OLD_ARCHIVE.relative_to(ROOT).as_posix(),'bytes':len(old_archive_raw),'sha256':sha(old_archive_raw)},'queueHistoricalReferences':historical_refs,'qualification':'Historical Conference01 source context only. It does not determine current acceptance, applied counts or pending counts.'},'sourceBindings':source_bindings,'currentPendingIds':IDS,'currentQueueGroup':current_group,'currentPendingIdentityAudit':{'id':pending['id'],**bind(PENDING),'pendingCount':93,'pendingIds':pending['pendingIds']},'currentAcceptedBatchSinceConference01':{'ids':read(LATEST[1])['acceptedIds'],'application':bind(LATEST[0]),'acceptance':bind(LATEST[1]),'validation':bind(LATEST[2]),'directorReturnReceipt':bind(LATEST[3]),'candidateModel':bind(LATEST[4]),'returnArchive':bind(LATEST[5]),'scope':'Immediately preceding Storm Control6 batch is applied; full current index/catalog and refreshed accepted-interface contexts are authoritative.'},'priorConferenceQuestionSetPreserved':{'questionCount':23,'allStillUnselected':True},'focusedAdditionalQuestions':copy.deepcopy(notes['focusedAdditionalQuestions']),'allQuestions':copy.deepcopy(old['questions'])+copy.deepcopy(notes['focusedAdditionalQuestions']),'requiredNewCaseObligations':cases,'originalFutureCaseRequirementsUnchanged':copy.deepcopy(notes['originalFutureCaseRequirementsUnchanged']),'focusedAdditionalQuestionSource':bind(NOTES),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False})
 candidate['currentQueueStatus']={'reviewedApplied':755,'pending':93,'acceptedUnapplied':0}
 assert len(candidate['records'])==7
 for record in candidate['records']:
  sid=record['spellId']; assert record['completeCurrentCatalogSourceAndAccess']==catalog_by[sid]
  assert index_by[sid]['authoredStatus']=='pending-authored-procedure'
  record['completeCurrentCatalogSourceAndAccess']=copy.deepcopy(catalog_by[sid]); record['currentIndexEntry']=copy.deepcopy(index_by[sid]); record['currentQueueStatus']={'identity':sid,'group':'rank9-psychic-fear7','pending':True,'reviewedApplied':755,'pendingCount':93}; record['status']='Fresh Conference02 source context; all dispositions remain unselected.'
 for counterpart in candidate['completeAppliedCounterparts']:
  sid=counterpart['spellId']; entry=index_by[sid]; env_path=(INDEX.parent/entry['procedureFile']).resolve(); envelope=read(env_path); ptr=entry.get('wholeCardPointer') or entry['procedurePointer']; counterpart['source']=bind(env_path); counterpart['pointer']=ptr; counterpart['completeCurrentCard']=copy.deepcopy(resolve_pointer(envelope,ptr)); shared=entry.get('sharedRulesPointer'); counterpart['completeSharedRules']=copy.deepcopy(resolve_pointer(envelope,shared) if shared else envelope.get('sharedRules',{})); counterpart['indexEntry']=copy.deepcopy(entry)
 for interface in candidate['currentAcceptedInterfaceComparisons']:
  ptr=interface['registryPointer']; interface['completeEntryUnchanged']=copy.deepcopy(registry['entries'][int(ptr.split('/')[-1])])
 for row in candidate['completeCosmologySourcesAndAuthority']:
  old_bind=row.get('source') or row.get('binding')
  if isinstance(old_bind,dict) and old_bind.get('path') and (ROOT/old_bind['path']).is_file(): row['source']=bind(ROOT/old_bind['path'])
 candidate['allQuestions']=copy.deepcopy(old['questions'])+copy.deepcopy(notes['focusedAdditionalQuestions'])
 assert len(candidate['questions'])==23 and len(candidate['focusedAdditionalQuestions'])==2 and len(candidate['allQuestions'])==25
 assert len({q['id'] for q in candidate['allQuestions']})==25 and all(not q['decisionSelected'] for q in candidate['allQuestions'])
 assert set().union(*(set(q['spellIds']) for q in candidate['allQuestions']))==set(IDS)
 assert len(cases)==14 and candidate['currentPendingIds']==IDS
 candidate_raw=enc(candidate); write(CANDIDATE,candidate_raw)
 case_ids=[c['id'] for c in cases]
 request=(f"GPT — review the attached fresh Rank9 Psychic Fear7 Conference02 packet against the current GitHub branch.\n\nAuthority: 755 applied-reviewed / 93 pending / 0 accepted-unapplied; 479 complete standalone procedures; 173 scoped interfaces.\nExact scope: {', '.join(IDS)} only.\n\nResolve all 23 preserved source questions and both focused additions (25 total). Return complete source-faithful procedures, every disposition, the 14 required main cases plus all distinct substantive branches, reversible event/state evidence, exact accepted IDs, exact blockers, complete retained holds, and your independent semantic failure check. Required case IDs: {', '.join(case_ids)}. Preserve current native class/school routes and actual access; a listed school placement is not an acquired route. Preserve source chronology and per-actor regular turns, spell pulse schedules, durations, opportunity costs, damage/riders, concentration, Ready, suppression, source death, and finite endings. Keep physical body/corpse changes, private perception, fear, stun, sleep/captivity, damage, force, movement, and secondary effects separately scoped. Resolve all uncertainty that can be resolved from exact sources; otherwise preserve explicit, narrow holds. Do not invent targets, immunities, feature access, random outcomes, or unspecified tables.\n\nUse current live index/catalog/queue/handoff/source bindings in Conference02; historical Conference01 and prior comparison labels do not override the current 755/93 authority. Do not edit canonical index/catalog or reopen completed/applied spell cohorts or the closed feat review. Keep source/access, runtime, human-play, balance, cosmology, domain-closure and release qualifications explicit. Mark accepted=true and applied=false only for exact IDs that pass; otherwise leave them unaccepted and unapplied and state exact blockers.\n")
 write(REQUEST,request.encode('utf-8'))
 output_files=[]
 def add(path,raw): write(path,raw); output_files.append(path)
 add(OUTPUT/'CANDIDATE.json',candidate_raw); add(OUTPUT/'REQUEST.txt',request.encode())
 add(OUTPUT/'historical/Conference01_ARCHIVE.zip',old_archive_raw); add(OUTPUT/'historical/Conference01_CANDIDATE.json',old_raw); add(OUTPUT/'historical/Conference01_ARCHIVE_MEMBER_CANDIDATE.json',archived_candidate)
 authority={'id':'RANK9-PSYCHIC-FEAR7-CURRENT-AUTHORITY-UPDATE-180','recordedAtUtc':now,'authority':AUTH,'scopeIds':IDS,'index':bind(INDEX),'catalog':bind(CATALOG),'queue':bind(QUEUE),'handoff':bind(HANDOFF),'pendingIdentityAudit':bind(PENDING),'latestAppliedBatch':{k:bind(p) for k,p in zip(['application','acceptance','validation','directorReturnReceipt','candidateModel','returnArchive'],LATEST)},'focusedQuestionSource':bind(NOTES),'qualification':'Fresh static source context only; no procedure, runtime, playtest, balance, cosmology or release approval.'}
 add(OUTPUT/'CURRENT_AUTHORITY_UPDATE.json',enc(authority)); source_rows=[]
 for row in source_bindings:
  dst=OUTPUT/PurePosixPath(row['packetPath']); add(dst,repository_bytes(ROOT/row['path'])); source_rows.append({'repositoryPath':row['path'],'packetPath':row['packetPath'],'bytes':row['bytes'],'sha256':row['sha256']})
 add(OUTPUT/'SOURCES_MANIFEST.json',enc({'id':'RANK9-PSYCHIC-FEAR7-CONFERENCE02-SOURCES-180','sources':source_rows}))
 add(OUTPUT/'README.md',('# Rank9 Psychic Fear7 Source Conference02\n\nFreshly bound to 755/93/0 authority. Scope: seven pending identities, 23 preserved questions plus two focused additions, and 14 required main-case obligations. Conference01 is historical context only. Dispositions remain unselected; no canonical or runtime changes.\n').encode())
 checks=[]
 def ck(label,ok): checks.append({'check':label,'passed':bool(ok)}); assert ok,label
 ck('Live authority matches index, queue, handoff and pending audit',queue['currentAuthority']==handoff['currentAuthority']==AUTH and index['authoredCounts']=={'reviewed':755,'pending':93} and pending['pendingCount']==93)
 ck('Exact seven Psychic Fear identities are current next pending group',group['group']=='rank9-psychic-fear7' and group['pendingIds']==IDS and set(IDS)<=live_pending)
 ck('All 23 prior questions and two focused additions remain unselected',len(candidate['allQuestions'])==25 and len({q['id'] for q in candidate['allQuestions']})==25 and all(not q['decisionSelected'] for q in candidate['allQuestions']))
 ck('All fourteen source-specific main case obligations are present',len(cases)==14 and [c['id'] for c in cases]==case_ids)
 ck('Seven pending cards and index entries bind current catalog and index',all(r['completeCurrentCatalogSourceAndAccess']==catalog_by[r['spellId']] and r['currentIndexEntry']==index_by[r['spellId']] for r in candidate['records']))
 ck('Current accepted counterparts, scoped interfaces and cosmology source list refreshed',len(candidate['completeAppliedCounterparts'])==7 and len(candidate['currentAcceptedInterfaceComparisons'])==42 and len(candidate['completeCosmologySourcesAndAuthority'])==11)
 ck('All source bindings use exact current Git blobs and their archive members match',all(bind(ROOT/r['path'])=={k:r[k] for k in ('path','bytes','sha256')} and (OUTPUT/PurePosixPath(r['packetPath'])).read_bytes()==repository_bytes(ROOT/r['path']) for r in source_bindings))
 ck('Latest Return177 acceptance, application and validation are included and valid',all(p.is_file() for p in LATEST) and read(LATEST[2])['status']=='PASS' and read(LATEST[1])['acceptedIds']==['cosmic-implosion','frozen-eternity','hellstorm','storm-of-vengeance','thunder-wrath','storm-cage'])
 ck('Conference01 archive and candidate remain byte-exact historical evidence',(OUTPUT/'historical/Conference01_ARCHIVE.zip').read_bytes()==old_archive_raw and json.loads((OUTPUT/'historical/Conference01_CANDIDATE.json').read_bytes())==old and json.loads((OUTPUT/'historical/Conference01_ARCHIVE_MEMBER_CANDIDATE.json').read_bytes())==old)
 ck('No canonical rules, runtime, playtest, or cosmology decisions are adopted',candidate['newRuleAdoptions']==candidate['runtimeTestsExecuted']==candidate['humanPlaytests']==candidate['cosmologyDecisions']==0 and not candidate['wholeGameComplete'])
 ck('Canonical catalog and index remain byte-identical',INDEX.read_bytes()==index_raw and CATALOG.read_bytes()==catalog_raw)
 check_doc={'id':'RANK9-PSYCHIC-FEAR7-CONFERENCE02-CHECK-180','recordedAtUtc':now,'status':'PASS','checkCount':len(checks),'checksFailed':0,'checks':checks,'currentAuthority':AUTH,'scopeIds':IDS,'questionCount':25,'requiredMainCaseCount':14,'sourceBindingCount':len(source_bindings)}
 write(CHECK,enc(check_doc)); write(OUTPUT/'SOURCE_CHECK.json',enc(check_doc))
 members=[]
 for p in sorted(OUTPUT.rglob('*')):
  if p.is_file() and p.name!='MANIFEST.json': raw=p.read_bytes(); members.append({'path':p.relative_to(OUTPUT).as_posix(),'bytes':len(raw),'sha256':sha(raw)})
 manifest={'id':'RANK9-PSYCHIC-FEAR7-CONFERENCE02-MANIFEST-180','candidate':{'path':'CANDIDATE.json','bytes':len(candidate_raw),'sha256':sha(candidate_raw)},'currentAuthority':AUTH,'scopeIds':IDS,'memberCount':len(members),'members':members,'historicalConference01Archive':{'path':'historical/Conference01_ARCHIVE.zip','bytes':len(old_archive_raw),'sha256':sha(old_archive_raw)},'liveCurrentSourceBindings':source_bindings}
 add(OUTPUT/'MANIFEST.json',enc(manifest))
 with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(OUTPUT.rglob('*')):
   if p.is_file(): z.write(p,p.relative_to(OUTPUT).as_posix())
 with zipfile.ZipFile(ARCHIVE) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
  assert z.read('CANDIDATE.json')==candidate_raw and json.loads(z.read('SOURCE_CHECK.json'))['checksFailed']==0
  for row in source_bindings: assert z.read(row['packetPath'])==repository_bytes(ROOT/row['path'])
 prep={'id':'RANK9-PSYCHIC-FEAR7-CONFERENCE02-PREPARATION-180','recordedAtUtc':now,'status':'PREPARED_UNSENT','sourceGitBranch':candidate['sourceGitBranch'],'sourceGitCommit':candidate['sourceGitCommit'],'candidate':bind(CANDIDATE),'archive':bind(ARCHIVE),'check':bind(CHECK),'request':bind(REQUEST),'manifest':{'path':(OUTPUT/'MANIFEST.json').relative_to(ROOT).as_posix(),'bytes':len((OUTPUT/'MANIFEST.json').read_bytes()),'sha256':sha((OUTPUT/'MANIFEST.json').read_bytes())},'memberCount':len(z.namelist()),'sourceBindingCount':len(source_bindings),'questionCount':25,'requiredMainCaseCount':14,'currentAuthority':AUTH,'reviewIds':IDS}
 write(PREP,enc(prep)); write(OUTPUT/'PREPARATION.json',enc(prep))
 pending_after={'id':'CURRENT93-PENDING-IDENTITY-AUDIT-180','recordedAtUtc':now,'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET','indexBinding':bind(INDEX),'catalogBinding':bind(CATALOG),'authoredCounts':index['authoredCounts'],'pendingCount':93,'pendingIds':sorted(live_pending),'allPendingExistInSourceCatalog':all(sid in catalog_by for sid in live_pending),'closed335AndCompletedCohortsReopened':False,'acceptedUnapplied':0}
 write(PENDING_AFTER,enc(pending_after))
 q=copy.deepcopy(queue); q.update({'id':'SPELL-REVIEW-QUEUE-180','recordedAtUtc':now,'packetStatus':'RANK9_PSYCHIC_FEAR7_FRESH_PACKET_PREPARED_UNSENT','currentAuthority':AUTH,'pendingIdentityAudit':{'path':PENDING_AFTER.name,'pending':93,'sha256':sha(PENDING_AFTER.read_bytes())}})
 next_group=next(x for x in q['currentPendingGroups'] if x['group']=='rank9-psychic-fear7'); next_group.update({'candidate':prep['candidate'],'archive':prep['archive'],'freshPacketRequiredForCurrentAuthority':False,'status':'FRESH_PACKET_PREPARED_UNSENT'})
 q['nextGroup']='rank9-psychic-fear7'; q['next']={'group':'rank9-psychic-fear7','pendingCount':7,'candidate':prep['candidate'],'archive':prep['archive'],'freshPacketRequiredForCurrentAuthority':False,'status':'FRESH_PACKET_PREPARED_UNSENT'}
 q['sourceConferencePrepared']={'candidate':prep['candidate'],'archive':prep['archive'],'check':prep['check'],'preparation':bind(PREP),'request':bind(REQUEST),'status':'prepared-unsent'}
 write(QUEUE_AFTER,enc(q))
 h=copy.deepcopy(handoff); h.update({'id':'CURRENT-HANDOFF-180','recordedAtUtc':now,'status':'RANK9_PSYCHIC_FEAR7_FRESH_PACKET_PREPARED_UNSENT','currentQueueBinding':bind(QUEUE_AFTER),'pendingIdentityAudit':{'id':pending_after['id'],'path':PENDING_AFTER.name,'pendingCount':93,'sha256':sha(PENDING_AFTER.read_bytes())},'nextGroup':'rank9-psychic-fear7','resumePriority':'Publish and submit the exact fresh 755/93 Psychic Fear7 packet to the same GPT director; independently audit its exact return, apply only exact accepted IDs, push that batch, and continue until pending reaches zero.','nextPreparedRequest':{'group':'rank9-psychic-fear7','candidate':prep['candidate'],'archive':prep['archive'],'request':bind(REQUEST),'freshPacketRequiredForCurrentAuthority':False}})
 h['currentIndexBinding']=bind(INDEX); h['currentCatalogBinding']=bind(CATALOG); h['sourceConferencePrepared']={'candidate':prep['candidate'],'archive':prep['archive'],'check':prep['check'],'preparation':bind(PREP),'request':bind(REQUEST),'status':'prepared-unsent'}; h['directorSubmission']={'status':'prepared-unsent','group':'rank9-psychic-fear7','reviewIds':IDS,'candidate':prep['candidate'],'archive':prep['archive'],'request':bind(REQUEST)}
 write(HANDOFF_AFTER,enc(h))
 print(json.dumps({'status':'PASS_PREPARED_UNSENT','candidate':prep['candidate'],'archive':prep['archive'],'checks':len(checks),'sourceBindingCount':len(source_bindings),'archiveMemberCount':len(z.namelist()),'authority':AUTH,'reviewIds':IDS},indent=2))
if __name__=='__main__': main()
