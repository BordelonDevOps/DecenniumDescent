from __future__ import annotations
import gzip,hashlib,json,pathlib,zipfile,zlib
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[5];AUDIT=pathlib.Path(__file__).resolve().parent
OUT=AUDIT/'rank9_collapse_timeline_current_source_322_prepared';ZIP=OUT/'DD_Rank9_CollapseTimeline_CurrentSource_322.zip';DELIVERY=OUT/'DD_Rank9_CollapseTimeline_CurrentSource_322_DELIVERY.json'
RET282=AUDIT/'rank9_timefate6_return282_received/DD_Rank9_TimeFate6_Director_Return282_HELD.zip';RET320=AUDIT/'rank9_fate_rewrite_return320_received/DD_Rank9_FateRewrite_Director_Return320_HELD.zip'
def sha(b):return hashlib.sha256(b).hexdigest()
def crc(b):return f'{zlib.crc32(b)&0xffffffff:08x}'
def j(b):return json.loads(b)
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
checks=[]
def ck(n,ok,d=None):
 checks.append({'check':n,'passed':bool(ok),'detail':d})
 if not ok:raise AssertionError(f'{n}: {d}')
raw=ZIP.read_bytes();delivery=j(DELIVERY.read_bytes())
with zipfile.ZipFile(ZIP) as z:
 names=z.namelist();payload={n:z.read(n) for n in names}
 ck('ZIP CRC and safe unique exact member list',z.testzip() is None and len(names)==len(set(names)) and set(names)==set(payload) and all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in names),{'members':len(names)})
ck('archive matches current delivery hash, bytes and CRC',len(raw)==delivery['archive']['bytes'] and sha(raw)==delivery['archive']['sha256'] and crc(raw)==delivery['archive']['crc32'],delivery['archive'])
ctx=j(payload['CONTEXT.json']);comp=j(payload['evidence/source_comparison/PACKET282_140_SOURCE_BINDING_COMPARISON.json']);proc=j(payload['evidence/collapse_timeline/return282_director_reviewed_procedure.json']);ep=j(payload['evidence/eternal_prophecy/return282_linked_dependency_procedure.json']);blockers=j(payload['evidence/authority/TF192-B02_and_TF192-B05.json'])
with zipfile.ZipFile(RET282) as z:allcases=j(gzip.decompress(z.read('CASEBOOK.json.gz')))['cases']
ct=[x for x in allcases if x.get('spellId')=='collapse-timeline'];epcases=[x for x in allcases if x.get('spellId')=='eternal-prophecy']
ck('current queue321 is 823/25/0 and names Collapse Timeline as the only next identity',ctx['authority']=={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173} and ctx['nextIdentity']=='collapse-timeline' and j(payload['authority/current/CURRENT_SPELL_QUEUE_321.json'])['next']=='collapse-timeline',ctx['authority'])
ck('only Collapse Timeline is adjudication scope; dependencies are context only',ctx['scopeIds']==['collapse-timeline'] and ctx['linkedContextIds']==['eternal-prophecy','fate-rewrite'],ctx['scopeIds'])
ck('Return320 sealed Fate Rewrite hold remains byte/hash bound',sha(payload['evidence/fate_rewrite/Return320_HELD.zip'])==sha(RET320.read_bytes()) and j(payload['evidence/fate_rewrite/Return320_HELD_DELIVERY.json'])['heldIds']==['fate-rewrite'],None)
ck('source comparison preserves 140/139/1 index-only',comp['inventoryCount']==140 and comp['unchangedCount']==139 and comp['changedCount']==1 and comp['missingCount']==0 and comp['changedPaths']==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],comp['changedPaths'])
ck('17 Collapse Timeline cases match procedure and all source case hashes',len(ct)==17 and [c['id'] for c in ct]==proc['caseIds'] and all(sha(payload[f'evidence/cases/collapse_timeline/{c["id"]}.json'])==sha(json.dumps(c,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()) for c in ct),len(ct))
ck('14 Eternal Prophecy cases are bound as linked-only context',len(epcases)==14 and ep['accepted'] is False and ep['applied'] is False and j(payload['evidence/cases/eternal_prophecy_linked_context_manifest.json'])['linkedContextOnly'] is True,{'cases':len(epcases)})
ck('TF192-B05 stays open and depends on unresolved TF192-B02',proc['blockerIds']==['TF192-B05'] and blockers['TF192-B05']['reassessment221']['dependsOn']==['TF192-B02'] and blockers['TF192-B02']['status']=='OPEN',None)
ck('TF192-H-HISTORY remains a separate external/parent-history hold','TF192-H-HISTORY' in proc['holdIds'] and 'TF192-H-HISTORY' in blockers['TF192-B05']['minimumMissingWitness282'],proc['holdIds'])
ck('questions and future obligations match the reviewed scope',len(j(payload['evidence/collapse_timeline/questions_and_obligations.json'])['questions'])==7 and len(j(payload['evidence/collapse_timeline/questions_and_obligations.json'])['focusedAddenda'])==1 and len(j(payload['evidence/collapse_timeline/questions_and_obligations.json'])['futureCaseRequirements'])==5,None)
ck('only pending procedures, no canonical/runtime/acceptance claim',not any(x in str(ctx) for x in ['applicationPerformed']) and ctx['acceptedIds']==[] and ctx['appliedIds']==[] and ctx['canonicalFilesChanged'] is False and ctx['runtimeExecuted'] is False,None)
ck('current native index/catalog entries remain pending',j(payload['authority/current/collapse_timeline_and_eternal_prophecy_rows.json'])['indexEntries']['collapse-timeline']['authoredStatus']=='pending-authored-procedure' and j(payload['authority/current/collapse_timeline_and_eternal_prophecy_rows.json'])['catalogRows']['collapse-timeline']['operational'] is None,None)
report={'id':'COLLAPSE-TIMELINE-PACKET-322-INDEPENDENT-READBACK-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'status':'PASS','archive':bind(ZIP),'memberCount':len(names),'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':sum(not x['passed'] for x in checks),'checks':checks,'canonicalFilesChanged':False,'runtimeExecuted':False,'acceptedIds':[],'appliedIds':[]}
p=AUDIT/'COLLAPSE_TIMELINE_PACKET_322_READBACK_AUDIT.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
# Attach separate readback audit to packet delivery and tracker.
deliv=j(DELIVERY.read_bytes());deliv['readbackAudit']=bind(p);DELIVERY.write_text(json.dumps(deliv,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':report['status'],'checkCount':report['checkCount'],'passed':report['passedChecks'],'failed':report['failedChecks'],'archive':bind(ZIP),'readback':bind(p),'delivery':bind(DELIVERY)},ensure_ascii=False))

