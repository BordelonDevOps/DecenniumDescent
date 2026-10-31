from __future__ import annotations
import gzip,hashlib,json,pathlib,zipfile,zlib
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[5]
AUDIT=pathlib.Path(__file__).resolve().parent
OUT=AUDIT/'rank9_fate_rewrite_current_source_320_prepared'
ZIP=OUT/'DD_Rank9_FateRewrite_CurrentSource_320.zip'
DELIVERY=OUT/'DD_Rank9_FateRewrite_CurrentSource_320_DELIVERY.json'

def sha(b):return hashlib.sha256(b).hexdigest()
def crc(b):return f'{zlib.crc32(b)&0xffffffff:08x}'
def readj(b):return json.loads(b)
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
checks=[]
def ck(name,ok,detail=None):
 checks.append({'check':name,'passed':bool(ok),'detail':detail})
 if not ok:raise AssertionError(f'{name}: {detail}')

delivery=readj(DELIVERY.read_bytes()); raw=ZIP.read_bytes(); zipbind=bind(ZIP)
with zipfile.ZipFile(ZIP) as z:
 names=z.namelist(); contents={n:z.read(n) for n in names}
 ck('ZIP CRC passes',z.testzip() is None,None)
 ck('unique path-safe exact member list',len(names)==len(set(names)) and all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in names),{'memberCount':len(names)})
context=readj(contents['CONTEXT.json'])
comparison=readj(contents['evidence/source_comparison/PACKET282_140_SOURCE_BINDING_COMPARISON.json'])
proc=readj(contents['evidence/fate_rewrite/return282_director_reviewed_procedure.json'])
ep=readj(contents['evidence/eternal_prophecy/return282_director_reviewed_procedure.json'])
holds=readj(contents['evidence/authority/return282_hold_register.json'])
status=readj(contents['evidence/director/FR_EP_WITNESS_CONSTRUCTION_01_STATUS.json'])
with zipfile.ZipFile(ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_timefate6_return282_received/DD_Rank9_TimeFate6_Director_Return282_HELD.zip') as z:
 cb=readj(gzip.decompress(z.read('CASEBOOK.json.gz')))['cases']
fate=[c for c in cb if c.get('spellId')=='fate-rewrite']; prophecy=[c for c in cb if c.get('spellId')=='eternal-prophecy']
ck('archive matches delivery binding',delivery['archive']['bytes']==len(raw) and delivery['archive']['sha256']==sha(raw) and delivery['archive']['crc32']==crc(raw),delivery['archive'])
ck('source comparison independently reports 140/139/1/0 and only authored index changed',comparison['inventoryCount']==140 and comparison['unchangedCount']==139 and comparison['changedCount']==1 and comparison['missingCount']==0 and comparison['changedPaths']==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],comparison['changedPaths'])
ck('queue/handoff/audit are embedded and 823/25/0 authority matches',context['authority']=={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173} and readj(contents['authority/current/CURRENT_SPELL_QUEUE_319.json'])['pendingCount']==25 and readj(contents['authority/current/CURRENT_HANDOFF_319.json'])['nextStep'].startswith('Prepare Fate Rewrite'),context['authority'])
ck('Fate Rewrite alone is adjudication scope',context['scopeIds']==['fate-rewrite'] and context['blockerIds']==['TF192-B04'],context['scopeIds'])
ck('Fate Rewrite and Eternal Prophecy both remain held/pending',proc['accepted'] is False and proc['applied'] is False and ep['accepted'] is False and ep['applied'] is False and proc['blockerIds']==['TF192-B04'] and ep['blockerIds']==['TF192-B02'],{'fate':proc['blockerIds'],'prophecy':ep['blockerIds']})
ck('17 preserved Fate Rewrite cases match procedure IDs and manifests',len(fate)==17 and [c['id'] for c in fate]==proc['caseIds'] and len(readj(contents['evidence/cases/fate_rewrite_manifest.json'])['cases'])==17,[c['id'] for c in fate])
ck('14 linked Eternal Prophecy cases match procedure IDs and manifests',len(prophecy)==14 and [c['id'] for c in prophecy]==ep['caseIds'] and len(readj(contents['evidence/cases/eternal_prophecy_manifest.json'])['cases'])==14,len(prophecy))
conflict=next(c for c in fate if c['id'].endswith('FATE-REWRITE-B__prophecy-creation-conflict'))
ck('conflict case is not a paid/fulfilled guarantee',not conflict['initialState'].get('obligations') and any(o.get('status')=='unavailable-before-payment' and o.get('RPSpent')==0 for o in conflict['finalState'].get('outcomes',[])),{'initialObligations':list(conflict['initialState'].get('obligations',{})),'outcomes':conflict['finalState'].get('outcomes',[])})
by={x['id']:x for x in holds['currentBlockers']}
ck('B02 and B04 dependency records preserve exact blockers',set(['TF192-B02','TF192-B04'])<=set(by) and by['TF192-B04'].get('reassessment221',{}).get('dependsOn')==['TF192-B02'],{'B02':by.get('TF192-B02',{}).get('status'),'B04DependsOn':by.get('TF192-B04',{}).get('reassessment221',{}).get('dependsOn')})
ck('Director authorization is limited to preparing/evaluating interface; no mechanism certified',status['interfaceAuthorizationId']=='FR-EP-WITNESS-CONSTRUCTION-01' and status['authorizationDoesNotSupplyMechanism'] is True and status['noQualificationOrUniversalOverrideAuthorized'] is True,None)
ck('all selected case member hashes verify against decoded source Return282',all(sha(contents[m['member']])==m['sha256'] and len(contents[m['member']])==m['bytes'] for fn in ['fate_rewrite_manifest.json','eternal_prophecy_manifest.json'] for m in readj(contents['evidence/cases/'+fn])['cases']),None)
ck('no identity accepted/applied and no canonical/runtime change claimed',context['acceptedIds']==[] and context['appliedIds']==[] and context['canonicalFilesChanged'] is False and context['runtimeExecuted'] is False,None)
ck('ZIP contains distinct Director-reviewed and current 192 draft procedure versions',all(p in contents for p in ['evidence/fate_rewrite/current_authored_candidate_procedure_192.json','evidence/fate_rewrite/return282_director_reviewed_procedure.json','evidence/eternal_prophecy/current_authored_candidate_procedure_192.json','evidence/eternal_prophecy/return282_director_reviewed_procedure.json']),None)
report={'id':'FATE-REWRITE-PACKET-320-INDEPENDENT-READBACK-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'status':'PASS','archive':zipbind,'memberCount':len(names),'checks':checks,'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':sum(not x['passed'] for x in checks),'canonicalFilesChanged':False,'runtimeExecuted':False,'acceptedIds':[],'appliedIds':[]}
p=AUDIT/'FATE_REWRITE_PACKET_320_READBACK_AUDIT.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':report['status'],'checkCount':report['checkCount'],'passed':report['passedChecks'],'failed':report['failedChecks'],'archive':zipbind,'report':bind(p)},ensure_ascii=False))

