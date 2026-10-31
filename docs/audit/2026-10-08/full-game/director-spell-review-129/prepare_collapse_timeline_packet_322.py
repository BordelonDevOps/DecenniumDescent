from __future__ import annotations
import gzip,hashlib,json,pathlib,zipfile,zlib
from datetime import datetime,timezone
from typing import Any
ROOT=pathlib.Path(__file__).resolve().parents[5]
AUDIT=pathlib.Path(__file__).resolve().parent
OUT=AUDIT/'rank9_collapse_timeline_current_source_322_prepared'
BASELINE=AUDIT/'rank9_timefate6_current_source_282_prepared'/'DD_Rank9_TimeFate6_CurrentSource_282.zip'
RETURN282=AUDIT/'rank9_timefate6_return282_received'/'DD_Rank9_TimeFate6_Director_Return282_HELD.zip'
RETURN320=AUDIT/'rank9_fate_rewrite_return320_received'/'DD_Rank9_FateRewrite_Director_Return320_HELD.zip'
RETURN320_DELIVERY=AUDIT/'rank9_fate_rewrite_return320_received'/'DD_Rank9_FateRewrite_Director_Return320_HELD_DELIVERY.json'
RETURN320_AUDIT=AUDIT/'FATE_REWRITE_RETURN320_INDEPENDENT_AUDIT.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_321.json';HANDOFF=AUDIT/'CURRENT_HANDOFF_321.json';PENDING=AUDIT/'CURRENT25_PENDING_IDENTITY_AUDIT_321.json'

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def crc(b:bytes)->str:return f'{zlib.crc32(b)&0xffffffff:08x}'
def can(o:Any)->bytes:return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
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
 q,h,p=(j(x.read_bytes()) for x in [QUEUE,HANDOFF,PENDING])
 with zipfile.ZipFile(BASELINE) as z:base_candidate=j(z.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json'))
 with zipfile.ZipFile(RETURN282) as z:
  proc_raw=z.read('procedures/collapse-timeline.json');ep_raw=z.read('procedures/eternal-prophecy.json');fr_raw=z.read('procedures/fate-rewrite.json')
  hold_raw=z.read('HOLD_REGISTER.json');case_gz=z.read('CASEBOOK.json.gz');qdisp_raw=z.read('QUESTION_DISPOSITIONS.json');binding_raw=z.read('SOURCE_BINDING.json')
  target_raw=z.read('evidence/CURRENT_TARGET_ROWS.json');notes_raw=z.read('evidence/ORIGINAL_CONFERENCE_NOTES_129.json');temporal_raw=z.read('evidence/current/TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json')
 proc,ep,fr,hold=j(proc_raw),j(ep_raw),j(fr_raw),j(hold_raw);book=j(gzip.decompress(case_gz));all_cases=book['cases']
 cases=[x for x in all_cases if x.get('spellId')=='collapse-timeline'];ep_cases=[x for x in all_cases if x.get('spellId')=='eternal-prophecy']
 if [x['id'] for x in cases]!=proc['caseIds'] or len(cases)!=17:raise AssertionError('Collapse Timeline case IDs do not match exact reviewed procedure')
 if [x['id'] for x in ep_cases]!=ep['caseIds'] or len(ep_cases)!=14:raise AssertionError('Linked EProp case binding mismatch')
 local_proc_raw=(CANDIDATE/'procedures/collapse-timeline.json').read_bytes();local_ep_raw=(CANDIDATE/'procedures/eternal-prophecy.json').read_bytes()
 frow=next(x for x in catalog['spells'] if x.get('id')=='collapse-timeline');eprow=next(x for x in catalog['spells'] if x.get('id')=='eternal-prophecy')
 findex=next(x for x in index['entries'] if x.get('id')=='collapse-timeline');eindex=next(x for x in index['entries'] if x.get('id')=='eternal-prophecy')
 blockers={x['id']:x for x in hold['currentBlockers'] if x['id'] in ['TF192-B02','TF192-B05']}
 if set(blockers)!={'TF192-B02','TF192-B05'}:raise AssertionError('Missing linked blocker record')
 with zipfile.ZipFile(BASELINE) as z: baseline_candidate_raw=z.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json')
 qids=proc['questionIds'];qdisp=j(qdisp_raw)
 questions=[x for x in base_candidate['questions'] if x.get('id') in qids and x.get('id')!='TIME129-ADD02']
 if {x['id'] for x in questions}!=set(qids)-{'TIME129-ADD02'}:raise AssertionError('Missing CT source questions')
 dispositions=[x for x in qdisp.get('dispositions',[]) if x.get('questionId') in qids or x.get('id') in qids]
 addenda=[x for x in qdisp.get('focusedAddenda',[]) if x.get('originalQuestionUnchanged',{}).get('id')=='TIME129-ADD02']
 if not addenda:raise AssertionError('Missing TIME129-ADD02 addendum')
 reqids={'TF9-CAST','TF9-COLLAPSE','TF9-PROPHECY','TF9-TEMPORAL-CONFLICT','TF9-PERSISTENCE'}
 req=[x for x in base_candidate['futureCaseRequirements'] if x.get('id') in reqids]
 if {x['id'] for x in req}!=reqids:raise AssertionError('Missing Collapse Timeline future obligations')
 with zipfile.ZipFile(RETURN320) as z: fdecision=j(z.read('DIRECTOR_DECISION.json')); b04=j(z.read('BLOCKER_REASSESSMENT.json'))
 comp_path=AUDIT/'rank9_fate_rewrite_current_source_320_prepared'/'PACKET282_140_SOURCE_BINDING_COMPARISON.json'
 comp=j(comp_path.read_bytes())
 if comp['inventoryCount']!=140 or comp['unchangedCount']!=139 or comp['changedCount']!=1 or comp['changedPaths']!=['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json']:raise AssertionError('Packet282 source comparison delta mismatch')
 if fdecision['heldIds']!=['fate-rewrite'] or fdecision['acceptedIds'] or fdecision['appliedIds']:raise AssertionError('Return320 status mismatch')
 with zipfile.ZipFile(RETURN320) as z:pass
 queue_authority=q['currentAuthority']
 if q['next']!='collapse-timeline' or q['pendingCount']!=25 or q['closureTasksRemaining']!=25:raise AssertionError('Queue321 does not authorize current target')

 members={}
 put(members,'authority/current/authored_review_index.json',index_raw)
 putj(members,'authority/current/collapse_timeline_and_eternal_prophecy_rows.json',{'bindings':[bind(INDEX),bind(CATALOG)],'indexEntries':{'collapse-timeline':findex,'eternal-prophecy':eindex},'catalogRows':{'collapse-timeline':frow,'eternal-prophecy':eprow}})
 for path,name in [(QUEUE,'authority/current/CURRENT_SPELL_QUEUE_321.json'),(HANDOFF,'authority/current/CURRENT_HANDOFF_321.json'),(PENDING,'authority/current/CURRENT25_PENDING_IDENTITY_AUDIT_321.json')]:put(members,name,path.read_bytes())
 put(members,'evidence/source_comparison/PACKET282_140_SOURCE_BINDING_COMPARISON.json',comp_path.read_bytes())
 putj(members,'evidence/native/current_target_rows_return282.json',{'archive':bind(RETURN282),'member':'evidence/CURRENT_TARGET_ROWS.json','rows':j(target_raw)})
 put(members,'evidence/native/return282_source_binding.json',binding_raw)
 put(members,'evidence/native/original_conference_notes_129.json',notes_raw)
 put(members,'evidence/native/temporal_reference_transaction_review_status.json',temporal_raw)
 putj(members,'evidence/authority/TF192-B02_and_TF192-B05.json',blockers)
 put(members,'evidence/collapse_timeline/return282_director_reviewed_procedure.json',proc_raw)
 put(members,'evidence/collapse_timeline/current_authored_candidate_procedure_192.json',local_proc_raw)
 put(members,'evidence/eternal_prophecy/return282_linked_dependency_procedure.json',ep_raw)
 put(members,'evidence/fate_rewrite/return282_linked_procedure_context.json',fr_raw)
 put(members,'evidence/fate_rewrite/Return320_HELD.zip',RETURN320.read_bytes())
 put(members,'evidence/fate_rewrite/Return320_HELD_DELIVERY.json',RETURN320_DELIVERY.read_bytes())
 put(members,'evidence/fate_rewrite/Return320_INDEPENDENT_AUDIT.json',RETURN320_AUDIT.read_bytes())
 put(members,'evidence/authority/return282_hold_register.json',hold_raw)
 putj(members,'evidence/collapse_timeline/questions_and_obligations.json',{'sourceCandidate':{'archive':bind(BASELINE),'member':'CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json','sha256':sha(baseline_candidate_raw)},'questions':questions,'priorDispositions':dispositions,'focusedAddenda':addenda,'futureCaseRequirements':req})
 source_ref={'archive':bind(RETURN282),'member':'CASEBOOK.json.gz','bytes':len(case_gz),'sha256':sha(case_gz),'decodedCaseCount':len(all_cases)}
 for label,cs in [('collapse_timeline',cases),('eternal_prophecy_linked_context',ep_cases)]:
  manifest=[]
  for c in cs:
   raw=can(c);name=f'evidence/cases/{label}/{c["id"]}.json';put(members,name,raw);manifest.append({'id':c['id'],'member':name,'bytes':len(raw),'sha256':sha(raw)})
  putj(members,f'evidence/cases/{label}_manifest.json',{'count':len(manifest),'procedureCaseIds':proc['caseIds'] if label=='collapse_timeline' else ep['caseIds'],'sourceCasebook':source_ref,'cases':manifest,'linkedContextOnly':label!='collapse_timeline'})
 request=f'''# Director request: Collapse Timeline / TF192-B05 only (Packet322)\n\nPlease adjudicate only `collapse-timeline` / `TF192-B05` at current authority **823 applied / 25 pending / 0 accepted-unapplied** (547 complete standalone procedures / 173 scoped interfaces). This is the next identity expressly directed by Return320. Do not re-open Fate Rewrite or adjudicate Eternal Prophecy; they are linked dependency context only.\n\nPacket322 binds queue321/handoff321/current 25-pending audit, current index and spell rows, a fresh-current Packet282 140-source comparison (139 unchanged, only the authored index changed), the exact Return282 Collapse Timeline procedure and all 17 preserved cases, relevant questions TF9-Q01/Q23–Q26/Q31/Q32/TIME129-ADD02, five future obligations, Return282 blocker records for TF192-B05 and TF192-B02, and the sealed Return320 Fate Rewrite hold. The 14 linked Eternal Prophecy cases are carried as byte-verified context only.\n\nExisting positive future-policy and time-horizon cases demonstrate authored finite future branches but not a source-complete committed guarantee. The prior Director blocker says B05 requires one complete guarantee plus exact external/parent histories and compatible/incompatible future traces. Return320 verifies the linked guarantee gap remains unresolved under TF192-B02. Unknown external and parent history operands remain TF192-H-HISTORY.\n\nPlease assess the Collapse Timeline target only. If the current cases do not close B05, seal the hold with the exact missing guarantee/external-parent witness and state the next identity after this hold. Preserve TF192-B04, TF192-B02, TF192-H-HISTORY, all five separate holds and all qualifications. No acceptance or application is requested.\n\nNo runtime, canonical, implementation, balance, playtest, cosmology, domain, completion or release approval is requested. Return acceptedIds, appliedIds, heldIds, blockers/dependencies, current authority, closure-task count and next identity.\n'''
 put(members,'REQUEST.md',request.encode())
 ctx={'id':'COLLAPSE-TIMELINE-PACKET-322','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'scopeIds':['collapse-timeline'],'linkedContextIds':['eternal-prophecy','fate-rewrite'],'blockerIds':['TF192-B05','TF192-B02'],'authority':queue_authority,'pendingCount':25,'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'nextIdentity':'collapse-timeline','nextBlocker':'TF192-B05','sourceBaseline':bind(BASELINE),'currentQueue':bind(QUEUE),'currentHandoff':bind(HANDOFF),'pendingAudit':bind(PENDING),'return320':bind(RETURN320),'sourceComparison':{'inventory':140,'unchanged':139,'changed':1,'changedPaths':comp['changedPaths']},'targetCaseCount':len(cases),'linkedEternalProphecyCasesByteVerifiedOnly':len(ep_cases),'acceptedIds':[],'appliedIds':[],'heldIds':[],'canonicalFilesChanged':False,'runtimeExecuted':False}
 putj(members,'CONTEXT.json',ctx)
 archive=OUT/'DD_Rank9_CollapseTimeline_CurrentSource_322.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name in sorted(members):z.writestr(name,members[name])
 raw=archive.read_bytes();arcbind=bind(archive)
 checks=[]
 def ck(n,ok,d=None):
  checks.append({'check':n,'passed':bool(ok),'detail':d})
  if not ok:raise AssertionError(f'{n}: {d}')
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();ck('ZIP CRC, safe unique paths and exact allowlist',z.testzip() is None and len(names)==len(set(names)) and set(names)==set(members) and all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in names),{'members':len(names)})
  ck('every packed member SHA matches prepared bytes',all(sha(z.read(n))==sha(members[n]) for n in members),len(names))
 ck('current authority and queue321 identify Collapse Timeline as only next target',queue_authority=={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173} and q['next']=='collapse-timeline' and h['currentBlocker']=='TF192-B04' and p['closureTasksRemaining']==25,queue_authority)
 ck('Fate Rewrite Return320 sealed hold remains unchanged',fdecision['heldIds']==['fate-rewrite'] and fdecision['acceptedIds']==[] and fdecision['appliedIds']==[] and fdecision['authorityAfter']==queue_authority,{'held':fdecision['heldIds']})
 ck('Collapse Timeline procedure targets TF192-B05 and depends on TF192-B02',proc['blockerIds']==['TF192-B05'] and blockers['TF192-B05']['reassessment221']['dependsOn']==['TF192-B02'],proc['blockerIds'])
 ck('current FRewrite/EProp/C-Timeline index rows remain pending and unaccepted',findex['authoredStatus']=='pending-authored-procedure' and eindex['authoredStatus']=='pending-authored-procedure' and frow['operational'] is None and eprow['operational'] is None,{'Fate':findex['authoredStatus'],'EProp':eindex['authoredStatus']})
 ck('Return282 current source comparison is exact 140/139/1 index-only',comp['inventoryCount']==140 and comp['unchangedCount']==139 and comp['changedCount']==1 and comp['missingCount']==0 and comp['changedPaths']==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],comp['changedPaths'])
 ck('all 17 Collapse Timeline cases match exact reviewed procedure case IDs',len(cases)==17 and [x['id'] for x in cases]==proc['caseIds'],len(cases))
 ck('14 linked EProp cases are marked linked context only',len(ep_cases)==14 and ep['accepted'] is False and ep['applied'] is False,{'cases':len(ep_cases),'linkedOnly':True})
 ck('questions and five future obligations match target set',set(x['id'] for x in questions)==set(qids)-{'TIME129-ADD02'} and len(addenda)==1 and {x['id'] for x in req}==reqids,{'questions':len(questions),'obligations':len(req)})
 ck('all current source paths unaffected except authored index',comp['unchangedCount']==139 and comp['changedPaths']==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],None)
 ck('no identity accepted/applied or canonical/runtime changes during packet build',ctx['acceptedIds']==[] and ctx['appliedIds']==[] and ctx['canonicalFilesChanged'] is False and ctx['runtimeExecuted'] is False,None)
 audit={'id':'COLLAPSE-TIMELINE-PACKET-322-INDEPENDENT-AUDIT','recordedAtUtc':ctx['recordedAtUtc'],'status':'PASS','archive':arcbind,'memberCount':len(members),'scopeIds':['collapse-timeline'],'authority':queue_authority,'caseCount':len(cases),'linkedProphecyCases':len(ep_cases),'sourceInventory':{'total':140,'unchanged':139,'changed':1,'changedPaths':comp['changedPaths']},'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':0,'checks':checks,'canonicalFilesChanged':False,'runtimeExecuted':False,'acceptedIds':[],'appliedIds':[]}
 aud=AUDIT/'COLLAPSE_TIMELINE_PACKET_322_INDEPENDENT_AUDIT.json';aud.write_bytes(pretty(audit))
 reqp=OUT/'COLLAPSE_TIMELINE_DIRECTOR_REQUEST_322.md';reqp.write_text(request,encoding='utf-8',newline='\n')
 cmp=OUT/'PACKET282_140_SOURCE_BINDING_COMPARISON.json';cmp.write_bytes(pretty(comp))
 delivery={'id':'COLLAPSE-TIMELINE-PACKET-322-DELIVERY','status':'PREPARED_FOR_DIRECTOR_REVIEW','recordedAtUtc':ctx['recordedAtUtc'],'scopeIds':['collapse-timeline'],'linkedContextIds':['eternal-prophecy','fate-rewrite'],'blockerIds':['TF192-B05','TF192-B02'],'authority':queue_authority,'archive':{'path':archive.relative_to(ROOT).as_posix(),**arcbind},'request':{'path':reqp.relative_to(ROOT).as_posix(),**bind(reqp)},'independentAudit':{'path':aud.relative_to(ROOT).as_posix(),**bind(aud)},'sourceComparison':{'path':cmp.relative_to(ROOT).as_posix(),**bind(cmp)},'acceptedIds':[],'appliedIds':[],'heldIds':[],'closureTasksRemaining':25,'runtimeExecuted':False}
 dp=OUT/'DD_Rank9_CollapseTimeline_CurrentSource_322_DELIVERY.json';dp.write_bytes(pretty(delivery))
 print(json.dumps({'status':'PASS','archive':str(archive),'bytes':len(raw),'sha256':sha(raw),'members':len(members),'cases':len(cases),'linkedContextCases':len(ep_cases),'checks':len(checks),'audit':str(aud),'delivery':str(dp),'authority':queue_authority},ensure_ascii=False))
if __name__=='__main__':main()
