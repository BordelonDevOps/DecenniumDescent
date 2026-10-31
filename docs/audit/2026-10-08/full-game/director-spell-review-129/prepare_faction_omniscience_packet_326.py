from __future__ import annotations
import gzip,hashlib,json,pathlib,zipfile,zlib
from datetime import datetime,timezone
from typing import Any
ROOT=pathlib.Path(__file__).resolve().parents[5];AUDIT=pathlib.Path(__file__).resolve().parent
OUT=AUDIT/'rank9_faction_omniscience_supreme_current_source_326_build03_prepared'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json';CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
CAND=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198'
BASELINE=AUDIT/'rank9_knowledgerevelation5_current_source_283_prepared'/'DD_Rank9_KnowledgeRevelation5_CurrentSource_283.zip'
CAND283=AUDIT/'rank9_knowledgerevelation5_current_source_283_prepared'/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_283.json'
RET283DIR=AUDIT/'rank9_knowledgerevelation5_return283_received';RET283=RET283DIR/'DD_Rank9_KnowledgeRevelation5_Director_Return283_HELD.zip';RET283D=RET283DIR/'DD_Rank9_KnowledgeRevelation5_Director_Return283_HELD_DELIVERY.json'
RET242DIR=AUDIT/'rank9_knowledgerevelation5_return242_received';RET242=RET242DIR/'DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD.zip';RET242D=RET242DIR/'DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD_DELIVERY.json'
COMPARISON=AUDIT/'rank9_fate_rewrite_current_source_320_prepared'/'PACKET282_140_SOURCE_BINDING_COMPARISON.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_325.json';HANDOFF=AUDIT/'CURRENT_HANDOFF_325.json';PENDING=AUDIT/'CURRENT25_PENDING_IDENTITY_AUDIT_325.json'
SEASON=ROOT/'DescentReviewChanges/incoming/DecenniumDescentv7/04_Seasonal_Decennial/04-seasonal-decennial-persistence'
AUTH={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173}
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def crc(b:bytes)->str:return f'{zlib.crc32(b)&0xffffffff:08x}'
def canonical(o:Any)->bytes:return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pretty(o:Any)->bytes:return(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def bind(p:pathlib.Path)->dict[str,Any]:
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def j(b:bytes)->Any:return json.loads(b)
def put(m:dict[str,bytes],n:str,b:bytes)->None:
 q=pathlib.PurePosixPath(n)
 if not n or q.is_absolute() or '..' in q.parts or '\\' in n:raise ValueError(n)
 if n in m:raise ValueError('duplicate '+n)
 m[n]=b
def putj(m,n,o):put(m,n,pretty(o))

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 if any(OUT.iterdir()):raise RuntimeError(f'nonempty packet directory {OUT}')
 index_raw,catalog_raw=INDEX.read_bytes(),CATALOG.read_bytes();index,catalog=j(index_raw),j(catalog_raw)
 q,h,p=(j(x.read_bytes()) for x in (QUEUE,HANDOFF,PENDING));comp=j(COMPARISON.read_bytes())
 entry=next(x for x in index['entries'] if x.get('id')=='faction-omniscience-supreme');row=next(x for x in catalog['spells'] if x.get('id')=='faction-omniscience-supreme')
 proc=j((CAND/'procedures/faction-omniscience-supreme.json').read_bytes())
 casebook=j(gzip.decompress((CAND/'CASEBOOK.json.gz').read_bytes()))['cases'];cases=[x for x in casebook if x.get('spellId')=='faction-omniscience-supreme']
 caseids=proc['caseIds']
 if len(cases)!=8 or [x['id'] for x in cases]!=caseids:raise AssertionError('target cases do not match current FOS procedure')
 if q['next']!='faction-omniscience-supreme' or q['pendingCount']!=25 or q['closureTasksRemaining']!=25 or q['currentAuthority']!=AUTH:raise AssertionError('queue325 not current or not directed to FOS')
 if entry['authoredStatus']!='pending-authored-procedure' or row['operational'] is not None or proc['accepted'] or proc['applied']:raise AssertionError('FOS no longer pending or source not preserved')
 for rec in comp['rows']:
  path=ROOT/rec['path'];raw=path.read_bytes()
  if len(raw)!=rec['currentBytes'] or sha(raw)!=rec['currentSha256']:raise AssertionError('current 140-source binding mismatch: '+rec['path'])
 if comp['inventoryCount']!=140 or comp['unchangedCount']!=139 or comp['changedCount']!=1 or comp['missingCount']!=0 or comp['changedPaths']!=['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json']:raise AssertionError('current 140-source comparison delta not the expected index-only change')
 cand_files=['CANDIDATE_PACKAGE_MANIFEST.json','MEMBER_MANIFEST.json','EVIDENCE_MANIFEST.json','COUNTS.json','CURRENT_CONTEXT_UNCHANGED.json','DIRECTOR_DECISION.json','FACT_SOURCE_REGISTER.json','SOURCE_OBLIGATIONS.json','SOURCE_VERIFICATION.json','SOURCE_CONFLICT_DISPOSITIONS.json','QUESTION_DISPOSITIONS.json','FUTURE_OBLIGATION_DISPOSITIONS.json','HOLD_REGISTER.json','CARRIED_HOLDS_196.json','QUALIFICATIONS.json','INDEPENDENT_SEMANTIC_FAILURE_CHECK.json','ACTOR_PROFILES.json','CLOCK_AND_INVERSE_RESULTS.json','DATA_INTEGRITY_CHECK.json','REMOTE_SOURCE_BINDINGS.json','ADDITIONAL_SOURCE_BINDINGS.json','SUPPLEMENTAL_SOURCE_PACKAGE_MAP.json','PROFILE_SOURCE_CHECK.json','procedures/faction-omniscience-supreme.json']
 for rel in cand_files:
  if not (CAND/rel).is_file():raise FileNotFoundError(CAND/rel)
 hold=j((CAND/'HOLD_REGISTER.json').read_bytes());b01=next(x for x in hold['newHolds'] if x['id']=='KR198-B01')
 if b01['status']!='OPEN' or b01['blocking'] is not True:raise AssertionError('current B01 hold not open')
 with zipfile.ZipFile(RET283) as z:r283=j(z.read('DIRECTOR_DECISION.json'));minwit=j(z.read('MINIMUM_WITNESS.json')) if 'MINIMUM_WITNESS.json' in z.namelist() else None
 with zipfile.ZipFile(RET242) as z:r242=j(z.read('DIRECTOR_DECISION.json'))
 if 'faction-omniscience-supreme' not in r283['heldIds'] or r283['acceptedIds'] or r283['appliedIds']:raise AssertionError('Return283 not the expected sealed FOS hold')
 season_files=[SEASON/'COMPILED_REPORT.md',SEASON/'SEASONAL_REPORT.md',SEASON/'campaign_ledgers/SEA-FACTION-WAR/seed-331.json',SEASON/'campaign_ledgers/SEA-FACTION-WAR/seed-502.json']
 season_files += sorted((SEASON/'results/SEA-FACTION-WAR/seed-331').glob('*.json'))+sorted((SEASON/'results/SEA-FACTION-WAR/seed-502').glob('*.json'))
 for sp in season_files:
  if not sp.is_file():raise FileNotFoundError(sp)
 ledger_review={'id':'SEA-FACTION-WAR-LEDGER-CANDIDATE-REVIEW-326','classification':'Unadjudicated candidate evidence; not represented as source-qualified canon or an actual historical campaign ledger.','files':[bind(f) for f in season_files],'observations':['Both seed files identify scenarioId SEA-FACTION-WAR and numeric simulation seeds/cycle records, but do not carry an explicit canonical factionId or field-level source provenance.','The compiled report records explicit source gaps and says no silent canon edits; it describes a persistence simulation, not an authorized spell-input ledger.','The files may contain useful finite institutional/faction-war premises. Director is asked to decide whether any exact fields are source-qualified for this spell, and what additional binding or owner/campaign authority is required.','No simulated record is promoted to campaign truth by packet preparation.']}

 members={}
 put(members,'authority/current/authored_review_index.json',index_raw)
 put(members,'authority/current/faction_omniscience_current_catalog_and_index_row.json',pretty({'bindings':{'index':bind(INDEX),'catalog':bind(CATALOG)},'indexEntry':entry,'catalogRow':row}))
 for path,name in ((QUEUE,'authority/current/CURRENT_SPELL_QUEUE_325.json'),(HANDOFF,'authority/current/CURRENT_HANDOFF_325.json'),(PENDING,'authority/current/CURRENT25_PENDING_IDENTITY_AUDIT_325.json')):put(members,name,path.read_bytes())
 put(members,'evidence/source_comparison/current_worktree_140_source_comparison.json',COMPARISON.read_bytes())
 for rel in cand_files:put(members,'evidence/faction_omniscience/current_candidate/'+rel,(CAND/rel).read_bytes())
 putj(members,'evidence/faction_omniscience/current_candidate/KR198-B01_EXACT_HOLD.json',b01)
 case_rows=[]
 for c in cases:
  fname=c['id'].replace('/','__')+'.json';name='evidence/cases/faction-omniscience-supreme/'+fname;raw=canonical(c);put(members,name,raw);case_rows.append({'id':c['id'],'member':name,'bytes':len(raw),'sha256':sha(raw)})
 putj(members,'evidence/cases/faction-omniscience-supreme_manifest.json',{'count':len(case_rows),'procedureCaseIds':caseids,'sourceCasebookBinding':bind(CAND/'CASEBOOK.json.gz'),'cases':case_rows})
 put(members,'evidence/prior_review/Return283_HELD.zip',RET283.read_bytes());put(members,'evidence/prior_review/Return283_HELD_DELIVERY.json',RET283D.read_bytes())
 put(members,'evidence/prior_review/Return242_HELD.zip',RET242.read_bytes());put(members,'evidence/prior_review/Return242_HELD_DELIVERY.json',RET242D.read_bytes())
 put(members,'evidence/prior_review/current_source_candidate_283.json',CAND283.read_bytes())
 for f in season_files:put(members,'evidence/unqualified_seasonal_candidates/'+f.relative_to(SEASON).as_posix(),f.read_bytes())
 putj(members,'evidence/unqualified_seasonal_candidates/LEDGER_CANDIDATE_SCOPE_REVIEW.json',ledger_review)
 request='''# Director request: Faction Omniscience Supreme / KR198-B01 only (Packet326)\n\nPlease review only `faction-omniscience-supreme` / `KR198-B01` at current authority **823 applied / 25 pending / 0 accepted-unapplied** (547 complete standalone procedures / 173 scoped interfaces), as expressly directed by Return323. This is one identity only; do not adjudicate the prior Eternity, Collapse Timeline or Fate Rewrite holds, or any other pending spell.\n\nThe packet binds the live index/catalog row, current queue325/handoff325/pending audit, all eight preserved FOS cases and current candidate evidence, and a checked current 140-file source comparison (139 unchanged; one authored-index change). Return283 and Return242 are included as earlier sealed holds; their historical authorities (816/32 and 811/37) are not current authority.\n\nA new possible evidence source has appeared in the current worktree after those returns: `incoming/DecenniumDescentv7/04_Seasonal_Decennial/04-seasonal-decennial-persistence`, with SEA-FACTION-WAR seed records 331 and 502 and their agent outputs. These files provide simulated faction-war cycle records, faction standings/debts and some future state, but the report records source gaps and no silent canon edits. The packet includes exact bytes and path bindings as unadjudicated candidate evidence only. Please decide explicitly whether any part constitutes a source-authorized exact canonical faction ledger or useful source-qualified future premises. Do not promote simulation fixtures or missing records into campaign facts.\n\nReassess `KR198-B01` only. The historical minimum witness required an exact established canonical faction and complete finite past/current/branch ledger, provenance/privacy/absence controls, true continuity/split/dissolution events, concrete likely-future premises, and complete positive/adverse dossiers through the admitted cast route. Determine whether the new seasonal artifacts close any of those elements; if they do not close the whole positive-content blocker, state exactly which fields need stronger provenance or authority and the smallest additional witness. Preserve source/privacy/absence limits and all six KR198-H qualifications.\n\nReturn acceptedIds, appliedIds, heldIds, blocker/qualification IDs, current authority, closure count, data/package/seal checks, exact next identity and rationale. No acceptance or application is requested. Do not execute supplied programs, modify canon or infer runtime/play/balance/cosmology/domain/completion/release approval.\n'''
 put(members,'REQUEST.md',request.encode())
 context={'id':'FACTION-OMNISCIENCE-SUPREME-PACKET-326','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'scopeIds':['faction-omniscience-supreme'],'blockerIds':['KR198-B01'],'authority':AUTH,'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'nextIdentity':'faction-omniscience-supreme','currentQueue':bind(QUEUE),'currentHandoff':bind(HANDOFF),'pendingAudit':bind(PENDING),'currentIndex':bind(INDEX),'currentCatalog':bind(CATALOG),'currentSourceComparison':{'total':140,'unchanged':139,'changed':1,'changedPaths':comp['changedPaths']},'targetCases':len(cases),'historicalReturn283':bind(RET283),'historicalReturn242':bind(RET242),'candidateSourceBinding':bind(CAND/'CANDIDATE_PACKAGE_MANIFEST.json'),'seasonalLedgerCandidateFiles':[bind(f) for f in season_files],'seasonalRecordsRemainUnadjudicated':True,'acceptedIds':[],'appliedIds':[],'heldIds':[],'canonicalFilesChanged':False,'runtimeExecuted':False}
 putj(members,'CONTEXT.json',context)
 archive=OUT/'DD_Rank9_FactionOmniscienceSupreme_CurrentSource_326.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name in sorted(members):z.writestr(name,members[name])
 checks=[]
 def ck(n,ok,d=None):
  checks.append({'check':n,'passed':bool(ok),'detail':d})
  if not ok:raise AssertionError(f'{n}: {d}')
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();ck('archive CRC, exact unique allowlist and safe member paths',z.testzip() is None and len(names)==len(set(names)) and set(names)==set(members) and all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in names),{'members':len(names)})
  ck('all packed member hashes match prepared inputs',all(sha(z.read(n))==sha(members[n]) for n in names),len(names))
 ck('queue325 directs exact FOS identity at current 823/25/0 authority',q['next']=='faction-omniscience-supreme' and q['currentAuthority']==AUTH and h['currentBlocker']=='TF192-B02' and p['pendingCount']==25,{'next':q['next'],'authority':q['currentAuthority']})
 ck('current FOS source remains pending and unoperational',entry['authoredStatus']=='pending-authored-procedure' and row['operational'] is None and proc['accepted'] is False and proc['applied'] is False,{'entry':entry['authoredStatus'],'operational':row['operational']})
 ck('exact FOS hold remains KR198-B01 with eight preserved target cases',b01['status']=='OPEN' and b01['blocking'] is True and set(b01['linkedCaseIds'])==set(caseids) and len(cases)==8,{'blocker':b01['id'],'cases':len(cases)})
 ck('all 140 current source rows match their current bytes and hashes',len(comp['rows'])==140 and all(len((ROOT/x['path']).read_bytes())==x['currentBytes'] and sha((ROOT/x['path']).read_bytes())==x['currentSha256'] for x in comp['rows']),{'rows':len(comp['rows'])})
 ck('140-source comparison remains 139 unchanged / one index-only delta',comp['inventoryCount']==140 and comp['unchangedCount']==139 and comp['changedCount']==1 and comp['missingCount']==0 and comp['changedPaths']==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],comp['changedPaths'])
 ck('Return283 is a prior FOS-only sealed hold; no acceptance/application',r283['heldIds']==['faction-omniscience-supreme'] and r283['acceptedIds']==[] and r283['appliedIds']==[] and r283['sourceAuthority']=={'reviewedApplied':816,'pending':32,'acceptedUnapplied':0,'completeStandaloneProcedures':540,'scopedInterfaces':173},r283['heldIds'])
 ck('seasonal records are bound as candidates with explicit source-gap notes',len(season_files)>=16 and all((ROOT/x['path']).is_file() and bind(ROOT/x['path'])==x for x in ledger_review['files']) and ledger_review['classification'].startswith('Unadjudicated'),{'files':len(season_files)})
 ck('no seasonal simulation was promoted to canon or current campaign truth',context['seasonalRecordsRemainUnadjudicated'] is True and 'No simulated record is promoted' in ' '.join(ledger_review['observations']),None)
 ck('no acceptance/application/canonical edit/runtime during packet build',context['acceptedIds']==[] and context['appliedIds']==[] and context['canonicalFilesChanged'] is False and context['runtimeExecuted'] is False,None)
 archive_binding=bind(archive);audit={'id':'FACTION-OMNISCIENCE-SUPREME-PACKET-326-INDEPENDENT-AUDIT','recordedAtUtc':context['recordedAtUtc'],'status':'PASS','archive':archive_binding,'memberCount':len(members),'scopeIds':['faction-omniscience-supreme'],'authority':AUTH,'targetCaseCount':len(cases),'sourceInventory':{'total':140,'unchanged':139,'changed':1,'changedPaths':comp['changedPaths']},'unadjudicatedSeasonalFiles':len(season_files),'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':0,'checks':checks,'canonicalFilesChanged':False,'runtimeExecuted':False,'acceptedIds':[],'appliedIds':[]}
 aud=AUDIT/'FACTION_OMNISCIENCE_SUPREME_PACKET_326_INDEPENDENT_AUDIT.json';aud.write_bytes(pretty(audit))
 reqp=OUT/'FACTION_OMNISCIENCE_SUPREME_DIRECTOR_REQUEST_326.md';reqp.write_text(request,encoding='utf-8',newline='\n')
 delivery={'id':'FACTION-OMNISCIENCE-SUPREME-PACKET-326-DELIVERY','status':'PREPARED_FOR_DIRECTOR_REVIEW','recordedAtUtc':context['recordedAtUtc'],'scopeIds':['faction-omniscience-supreme'],'blockerIds':['KR198-B01'],'authority':AUTH,'archive':{'path':archive.relative_to(ROOT).as_posix(),**archive_binding},'request':{'path':reqp.relative_to(ROOT).as_posix(),**bind(reqp)},'independentAudit':{'path':aud.relative_to(ROOT).as_posix(),**bind(aud)},'targetCaseCount':len(cases),'seasonalCandidateFileCount':len(season_files),'acceptedIds':[],'appliedIds':[],'heldIds':[],'closureTasksRemaining':25,'runtimeExecuted':False}
 dp=OUT/'DD_Rank9_FactionOmniscienceSupreme_CurrentSource_326_DELIVERY.json';dp.write_bytes(pretty(delivery))
 print(json.dumps({'status':'PASS','archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'members':len(members),'targetCases':len(cases),'seasonalFiles':len(season_files),'checks':len(checks),'audit':str(aud),'delivery':str(dp)},ensure_ascii=False))
if __name__=='__main__':main()
