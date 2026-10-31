from __future__ import annotations
import gzip, hashlib, json, pathlib, zipfile, zlib
from datetime import datetime, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
OUT = AUDIT / 'rank9_eternal_prophecy_current_source_323_build02_prepared'
BASELINE = AUDIT/'rank9_timefate6_current_source_282_prepared'/'DD_Rank9_TimeFate6_CurrentSource_282.zip'
RETURN282 = AUDIT/'rank9_timefate6_return282_received'/'DD_Rank9_TimeFate6_Director_Return282_HELD.zip'
RETURN320 = AUDIT/'rank9_fate_rewrite_return320_received'/'DD_Rank9_FateRewrite_Director_Return320_HELD.zip'
RETURN320_DELIVERY = AUDIT/'rank9_fate_rewrite_return320_received'/'DD_Rank9_FateRewrite_Director_Return320_HELD_DELIVERY.json'
RETURN320_AUDIT = AUDIT/'FATE_REWRITE_RETURN320_INDEPENDENT_AUDIT.json'
RETURN322_DIR = AUDIT/'rank9_collapse_timeline_return322_received'
RETURN322 = RETURN322_DIR/'DD_Rank9_CollapseTimeline_Director_Return322_HELD.zip'
RETURN322_DELIVERY = RETURN322_DIR/'DD_Rank9_CollapseTimeline_Director_Return322_HELD_DELIVERY.json'
RETURN322_AUDIT = AUDIT/'COLLAPSE_TIMELINE_RETURN322_INDEPENDENT_AUDIT.json'
INDEX = ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
CANDIDATE = ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192'
QUEUE = AUDIT/'CURRENT_SPELL_QUEUE_323.json'
HANDOFF = AUDIT/'CURRENT_HANDOFF_323.json'
PENDING = AUDIT/'CURRENT25_PENDING_IDENTITY_AUDIT_323.json'
COMPARISON = AUDIT/'rank9_fate_rewrite_current_source_320_prepared'/'PACKET282_140_SOURCE_BINDING_COMPARISON.json'
AUTHORITY = {'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173}

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
 q,h,p=(j(x.read_bytes()) for x in (QUEUE,HANDOFF,PENDING))
 comp=j(COMPARISON.read_bytes())
 with zipfile.ZipFile(BASELINE) as z:base_candidate=j(z.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json'))
 with zipfile.ZipFile(RETURN282) as z:
  proc_raw=z.read('procedures/eternal-prophecy.json');fr_raw=z.read('procedures/fate-rewrite.json');ct_raw=z.read('procedures/collapse-timeline.json')
  hold_raw=z.read('HOLD_REGISTER.json');case_gz=z.read('CASEBOOK.json.gz');qdisp_raw=z.read('QUESTION_DISPOSITIONS.json')
  binding_raw=z.read('SOURCE_BINDING.json');target_raw=z.read('evidence/CURRENT_TARGET_ROWS.json')
  notes_raw=z.read('evidence/ORIGINAL_CONFERENCE_NOTES_129.json')
  temporal={name:z.read(f'evidence/current/{name}.json') for name in ('TEMPORAL_KERNEL_REVIEW_STATUS','TEMPORAL_PARENT_HISTORY_REVIEW_STATUS','TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS')}
  source_delivery=z.read('evidence/INPUT_DELIVERY.json');source_manifest=z.read('evidence/INPUT_MANIFEST.json')
 proc=j(proc_raw);book=j(gzip.decompress(case_gz));all_cases=book['cases']
 cases=[x for x in all_cases if x.get('spellId')=='eternal-prophecy']
 if [x['id'] for x in cases]!=proc['caseIds'] or len(cases)!=14:raise AssertionError('Eternal Prophecy case IDs mismatch exact held procedure')
 local_proc_raw=(CANDIDATE/'procedures/eternal-prophecy.json').read_bytes()
 row=next(x for x in catalog['spells'] if x.get('id')=='eternal-prophecy')
 entry=next(x for x in index['entries'] if x.get('id')=='eternal-prophecy')
 blocker={x['id']:x for x in j(hold_raw)['currentBlockers'] if x['id']=='TF192-B02'}
 if set(blocker)!={'TF192-B02'}:raise AssertionError('TF192-B02 missing from current hold register')
 if q['next']!='eternal-prophecy' or q['pendingCount']!=25 or q['closureTasksRemaining']!=25:raise AssertionError('queue323 does not direct Eternal Prophecy at current authority')
 for record in comp['rows']:
  pth=ROOT/record['path']
  if not pth.is_file() or len(pth.read_bytes())!=record['currentBytes'] or sha(pth.read_bytes())!=record['currentSha256']:
   raise AssertionError(f"current source drift: {record['path']}")
 if comp['inventoryCount']!=140 or comp['unchangedCount']!=139 or comp['changedCount']!=1 or comp['missingCount']!=0 or comp['changedPaths']!=['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json']:
  raise AssertionError('140-source comparison does not bind current packet state')
 qids=proc['questionIds'];qdisp=j(qdisp_raw)
 questions=[x for x in base_candidate['questions'] if x.get('id') in qids and x.get('id')!='TIME129-ADD02']
 addenda=[x for x in qdisp.get('focusedAddenda',[]) if x.get('originalQuestionUnchanged',{}).get('id')=='TIME129-ADD02']
 if {x['id'] for x in questions}!=set(qids)-{'TIME129-ADD02'} or not addenda:raise AssertionError('missing EProp source questions or focused addendum')
 dispositions=[x for x in qdisp.get('dispositions',[]) if x.get('questionId') in qids or x.get('id') in qids]
 req=[x for x in base_candidate['futureCaseRequirements'] if x.get('id')=='TF9-PROPHECY']
 if len(req)!=1:raise AssertionError('missing exact TF9-PROPHECY requirement')
 with zipfile.ZipFile(RETURN320) as z:fr_decision=j(z.read('DIRECTOR_DECISION.json'));fr_b04=j(z.read('BLOCKER_REASSESSMENT.json'));fr_ep_auth=j(z.read('context/FR_EP_WITNESS_CONSTRUCTION_01_STATUS.json'))
 with zipfile.ZipFile(RETURN322) as z:ct_decision=j(z.read('DIRECTOR_DECISION.json'));ct_b05=j(z.read('BLOCKER_REASSESSMENT.json'))
 if fr_decision['heldIds']!=['fate-rewrite'] or ct_decision['heldIds']!=['collapse-timeline']:raise AssertionError('prior sealed holds changed or malformed')
 if row['operational'] is not None or entry['authoredStatus']!='pending-authored-procedure' or proc['accepted'] or proc['applied']:raise AssertionError('current EProp identity is not pending or source changed')

 members={}
 put(members,'authority/current/authored_review_index.json',index_raw)
 putj(members,'authority/current/eternal_prophecy_index_and_catalog_row.json',{'bindings':{'index':bind(INDEX),'catalog':bind(CATALOG)},'indexEntry':entry,'catalogRow':row})
 for path,name in ((QUEUE,'authority/current/CURRENT_SPELL_QUEUE_323.json'),(HANDOFF,'authority/current/CURRENT_HANDOFF_323.json'),(PENDING,'authority/current/CURRENT25_PENDING_IDENTITY_AUDIT_323.json')):put(members,name,path.read_bytes())
 put(members,'evidence/source_comparison/PACKET282_140_SOURCE_BINDING_COMPARISON.json',COMPARISON.read_bytes())
 putj(members,'evidence/source_comparison/CURRENT_SOURCE_BINDING_RECHECK.json',{'inventoryCount':140,'checkedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'checkedCurrentRows':len(comp['rows']),'allCurrentBytesAndSha256Match':True,'indexCurrentSha256':sha(index_raw),'catalogCurrentSha256':sha(catalog_raw),'comparison':comp})
 putj(members,'evidence/native/current_target_rows_return282.json',{'archive':bind(RETURN282),'member':'evidence/CURRENT_TARGET_ROWS.json','rows':j(target_raw)})
 put(members,'evidence/native/return282_source_binding.json',binding_raw)
 put(members,'evidence/native/original_conference_notes_129.json',notes_raw)
 put(members,'evidence/native/source_delivery_manifest.json',source_delivery)
 put(members,'evidence/native/source_input_manifest.json',source_manifest)
 for name,data in temporal.items():put(members,'evidence/native/'+name+'.json',data)
 put(members,'evidence/authority/TF192-B02_current_blocker.json',pretty(blocker['TF192-B02']))
 put(members,'evidence/eternal_prophecy/return282_director_reviewed_procedure.json',proc_raw)
 put(members,'evidence/eternal_prophecy/current_authored_candidate_procedure_192.json',local_proc_raw)
 put(members,'evidence/fate_rewrite/Return320_HELD.zip',RETURN320.read_bytes())
 put(members,'evidence/fate_rewrite/Return320_HELD_DELIVERY.json',RETURN320_DELIVERY.read_bytes())
 put(members,'evidence/fate_rewrite/Return320_INDEPENDENT_AUDIT.json',RETURN320_AUDIT.read_bytes())
 put(members,'evidence/fate_rewrite/FR_EP_WITNESS_CONSTRUCTION_01_STATUS.json',pretty(fr_ep_auth))
 put(members,'evidence/collapse_timeline/Return322_HELD.zip',RETURN322.read_bytes())
 put(members,'evidence/collapse_timeline/Return322_HELD_DELIVERY.json',RETURN322_DELIVERY.read_bytes())
 put(members,'evidence/collapse_timeline/Return322_INDEPENDENT_AUDIT.json',RETURN322_AUDIT.read_bytes())
 put(members,'evidence/collapse_timeline/Return322_BLOCKER_REASSESSMENT.json',pretty(ct_b05))
 put(members,'evidence/authority/return282_hold_register.json',hold_raw)
 put(members,'evidence/eternal_prophecy/questions_and_obligations.json',pretty({'sourceCandidate':{'archive':bind(BASELINE),'member':'CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json'},'questions':questions,'priorDispositions':dispositions,'focusedAddenda':addenda,'futureCaseRequirements':req}))
 source_ref={'archive':bind(RETURN282),'member':'CASEBOOK.json.gz','bytes':len(case_gz),'sha256':sha(case_gz),'decodedCaseCount':len(all_cases)}
 case_rows=[]
 for c in cases:
  name=f'evidence/cases/eternal_prophecy/{c["id"]}.json';raw=canonical(c);put(members,name,raw);case_rows.append({'id':c['id'],'member':name,'bytes':len(raw),'sha256':sha(raw)})
 putj(members,'evidence/cases/eternal_prophecy_manifest.json',{'count':len(case_rows),'procedureCaseIds':proc['caseIds'],'sourceCasebook':source_ref,'cases':case_rows,'targetCasesOnly':True})
 request='''# Director request: Eternal Prophecy / TF192-B02 only (Packet323)\n\nPlease review only `eternal-prophecy` / `TF192-B02` at current authority **823 applied / 25 pending / 0 accepted-unapplied** (547 complete standalone procedures / 173 scoped interfaces), as expressly directed by Return322. This is a one-identity review; do not re-open or adjudicate Fate Rewrite, Collapse Timeline, Time Stop, or the separately retained holds.\n\nThe packet binds current queue323/handoff323/pending audit, current index/catalog spell row and candidate procedure, and a current 140-source comparison (139 unchanged, one authored-index delta) whose current hashes/byte counts were rechecked against all 140 files. It includes the Return282 EProp procedure, all 14 exact target cases, source questions and dispositions, TF9-PROPHECY future requirement, current B02 hold language, source binding/target rows, temporal-reference status, and sealed Return320/Return322 hold artifacts.\n\nThe native text promises a self-fulfilling prophecy that *must come true within 1 year*. Existing lawful route examples and paid pending obligations do not yet resolve every-route/intervention prevention through the deadline, nor item/destination loss or exact external-parent history. Return320 retains that source-complete guarantee blocker; Return322 independently held Collapse Timeline on the same dependency. The prior FR_EP_WITNESS_CONSTRUCTION_01 authorization permits preparing/evaluating the interface while both identities remain pending; it does not authorize a new guarantee mechanism, source permission, waiver, or qualification of the promise.\n\nPlease reassess only B02 using the packet’s exact cases. If still open, seal a precise held disposition stating the minimum authorized finite mechanism or explicit owner authorization needed, preserve the unconditional source text, exact external/parent-history limits and existing holds, and identify the next identity. If the evidence supports a narrower witness, state it without inventing permission. No acceptance or application is requested.\n\nReturn acceptedIds, appliedIds, heldIds, blockers/dependencies, authority, closure tasks, data/package/seal checks and next identity. Do not execute supplied programs or change canonical files. Runtime, implementation, human play, balance, cosmology, domain, completion and release gates remain outside this request.\n'''
 put(members,'REQUEST.md',request.encode())
 context={'id':'ETERNAL-PROPHECY-PACKET-323','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'scopeIds':['eternal-prophecy'],'blockerIds':['TF192-B02'],'authority':AUTHORITY,'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'nextIdentity':'eternal-prophecy','sourceBaseline':bind(BASELINE),'currentQueue':bind(QUEUE),'currentHandoff':bind(HANDOFF),'pendingAudit':bind(PENDING),'return320':bind(RETURN320),'return322':bind(RETURN322),'sourceComparison':{'inventory':140,'unchanged':139,'changed':1,'changedPaths':comp['changedPaths']},'targetCaseCount':len(cases),'questionIds':qids,'futureRequirements':['TF9-PROPHECY'],'acceptedIds':[],'appliedIds':[],'heldIds':[],'canonicalFilesChanged':False,'runtimeExecuted':False}
 putj(members,'CONTEXT.json',context)
 archive=OUT/'DD_Rank9_EternalProphecy_CurrentSource_323.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name in sorted(members):z.writestr(name,members[name])
 checks=[]
 def ck(n,ok,d=None):
  checks.append({'check':n,'passed':bool(ok),'detail':d})
  if not ok:raise AssertionError(f'{n}: {d}')
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();ck('ZIP CRC, safe unique paths and exact member set',z.testzip() is None and len(names)==len(set(names)) and set(names)==set(members) and all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in names),{'members':len(names)})
  ck('every packed member matches prepared bytes',all(sha(z.read(n))==sha(members[n]) for n in names),len(names))
 ck('queue323 authorizes only EProp/B02 at 823/25/0',q['next']=='eternal-prophecy' and q['pendingCount']==25 and q['currentAuthority']==AUTHORITY and q['closureTasksRemaining']==25 and h['currentBlocker']=='TF192-B05' and p['pendingCount']==25,{'next':q['next'],'authority':q['currentAuthority']})
 ck('Return320 Fate Rewrite and Return322 Collapse Timeline holds remain sealed and unapplied',fr_decision['heldIds']==['fate-rewrite'] and not fr_decision['acceptedIds'] and not fr_decision['appliedIds'] and ct_decision['heldIds']==['collapse-timeline'] and not ct_decision['acceptedIds'] and not ct_decision['appliedIds'],{'fateRewrite':fr_decision['heldIds'],'collapseTimeline':ct_decision['heldIds']})
 ck('current EProp source remains pending and unoperational',entry['authoredStatus']=='pending-authored-procedure' and row['operational'] is None and proc['accepted'] is False and proc['applied'] is False,{'status':entry['authoredStatus'],'operational':row['operational']})
 ck('TF192-B02 remains open and identifies all-routes/item/destination guarantee gap',blocker['TF192-B02']['status']=='OPEN' and 'all routes/intervention' in blocker['TF192-B02']['missing'] and 'item/destination' in blocker['TF192-B02']['missing'] and blocker['TF192-B02']['reassessment282']['inheritedOriginalBlockerUnchanged'] is True,blocker['TF192-B02']['missing'])
 ck('all 14 target cases exactly match current reviewed procedure',len(cases)==14 and [x['id'] for x in cases]==proc['caseIds'],len(cases))
 ck('all source questions, focused addendum and sole prophecy future requirement bind exactly',set(x['id'] for x in questions)==set(qids)-{'TIME129-ADD02'} and any(x.get('originalQuestionUnchanged',{}).get('id')=='TIME129-ADD02' for x in addenda) and len(req)==1 and req[0]['id']=='TF9-PROPHECY',{'questions':len(questions),'addenda':len(addenda),'requirement':req[0]['id']})
 ck('current 140-source comparison has 139 unchanged and one index-only delta',comp['inventoryCount']==140 and comp['unchangedCount']==139 and comp['changedCount']==1 and comp['missingCount']==0 and comp['changedPaths']==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],comp['changedPaths'])
 ck('current bytes and SHA-256 match every comparison row',len(comp['rows'])==140 and all(sha((ROOT/x['path']).read_bytes())==x['currentSha256'] and len((ROOT/x['path']).read_bytes())==x['currentBytes'] for x in comp['rows']),{'rows':len(comp['rows'])})
 ck('FR-EP interface-construction authorization does not authorize mechanism or source qualification',fr_ep_auth['interfaceAuthorizationId']=='FR-EP-WITNESS-CONSTRUCTION-01' and fr_ep_auth['blockerIds']==['TF192-B04','TF192-B02'] and fr_ep_auth['authorizationDoesNotSupplyMechanism'] is True and fr_ep_auth['noQualificationOrUniversalOverrideAuthorized'] is True,fr_ep_auth['interfaceAuthorizationScope'])
 ck('packet build has no acceptance, application, canonical edit or runtime action',context['acceptedIds']==[] and context['appliedIds']==[] and context['canonicalFilesChanged'] is False and context['runtimeExecuted'] is False,None)
 archive_binding=bind(archive);audit={'id':'ETERNAL-PROPHECY-PACKET-323-INDEPENDENT-AUDIT','recordedAtUtc':context['recordedAtUtc'],'status':'PASS','archive':archive_binding,'memberCount':len(members),'scopeIds':['eternal-prophecy'],'authority':AUTHORITY,'targetCaseCount':len(cases),'sourceInventory':{'total':140,'unchanged':139,'changed':1,'changedPaths':comp['changedPaths']},'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':0,'checks':checks,'canonicalFilesChanged':False,'runtimeExecuted':False,'acceptedIds':[],'appliedIds':[]}
 aud=AUDIT/'ETERNAL_PROPHECY_PACKET_323_INDEPENDENT_AUDIT.json';aud.write_bytes(pretty(audit))
 reqp=OUT/'ETERNAL_PROPHECY_DIRECTOR_REQUEST_323.md';reqp.write_text(request,encoding='utf-8',newline='\n')
 delivery={'id':'ETERNAL-PROPHECY-PACKET-323-DELIVERY','status':'PREPARED_FOR_DIRECTOR_REVIEW','recordedAtUtc':context['recordedAtUtc'],'scopeIds':['eternal-prophecy'],'blockerIds':['TF192-B02'],'authority':AUTHORITY,'archive':{'path':archive.relative_to(ROOT).as_posix(),**archive_binding},'request':{'path':reqp.relative_to(ROOT).as_posix(),**bind(reqp)},'independentAudit':{'path':aud.relative_to(ROOT).as_posix(),**bind(aud)},'sourceComparison':{'path':COMPARISON.relative_to(ROOT).as_posix(),**bind(COMPARISON)},'targetCaseCount':len(cases),'acceptedIds':[],'appliedIds':[],'heldIds':[],'closureTasksRemaining':25,'runtimeExecuted':False}
 dp=OUT/'DD_Rank9_EternalProphecy_CurrentSource_323_DELIVERY.json';dp.write_bytes(pretty(delivery))
 print(json.dumps({'status':'PASS','archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'members':len(members),'cases':len(cases),'checks':len(checks),'audit':str(aud),'delivery':str(dp)},ensure_ascii=False))

if __name__=='__main__':main()
