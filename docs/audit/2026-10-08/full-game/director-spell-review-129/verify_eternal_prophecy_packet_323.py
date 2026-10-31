from __future__ import annotations
import hashlib,json,pathlib,zipfile,zlib
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[5];AUDIT=pathlib.Path(__file__).resolve().parent
OUT=AUDIT/'rank9_eternal_prophecy_current_source_323_build02_prepared'
ARCHIVE=OUT/'DD_Rank9_EternalProphecy_CurrentSource_323.zip';DELIVERY=OUT/'DD_Rank9_EternalProphecy_CurrentSource_323_DELIVERY.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def crc(b):return f'{zlib.crc32(b)&0xffffffff:08x}'
def pretty(o):return(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def ck(checks,n,ok,detail=None):
 checks.append({'check':n,'passed':bool(ok),'detail':detail})
 if not ok:raise AssertionError(f'{n}: {detail}')
d=json.loads(DELIVERY.read_text(encoding='utf-8'));raw=ARCHIVE.read_bytes();checks=[]
ck(checks,'archive matches delivery bytes, SHA-256 and CRC32',len(raw)==d['archive']['bytes'] and sha(raw)==d['archive']['sha256'] and crc(raw)==d['archive']['crc32'],d['archive'])
ck(checks,'delivery scope is Eternal Prophecy / B02 only',d['scopeIds']==['eternal-prophecy'] and d['blockerIds']==['TF192-B02'] and d['acceptedIds']==[] and d['appliedIds']==[] and d['heldIds']==[],d)
with zipfile.ZipFile(ARCHIVE) as z:
 names=z.namelist();ck(checks,'ZIP CRC and member-name safety/uniqueness',z.testzip() is None and len(names)==len(set(names)) and all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in names),{'members':len(names)})
 payload={n:z.read(n) for n in names};context=json.loads(payload['CONTEXT.json']);ep=json.loads(payload['evidence/eternal_prophecy/return282_director_reviewed_procedure.json']);manifest=json.loads(payload['evidence/cases/eternal_prophecy_manifest.json']);q=json.loads(payload['authority/current/CURRENT_SPELL_QUEUE_323.json']);h=json.loads(payload['authority/current/CURRENT_HANDOFF_323.json']);p=json.loads(payload['authority/current/CURRENT25_PENDING_IDENTITY_AUDIT_323.json']);comp=json.loads(payload['evidence/source_comparison/PACKET282_140_SOURCE_BINDING_COMPARISON.json']);fr=json.loads(payload['evidence/fate_rewrite/Return320_INDEPENDENT_AUDIT.json']);ct=json.loads(payload['evidence/collapse_timeline/Return322_INDEPENDENT_AUDIT.json'])
 ck(checks,'all exact target case files match the procedure manifest',manifest['count']==14 and [x['id'] for x in manifest['cases']]==ep['caseIds'] and all(x['member'] in payload and sha(payload[x['member']])==x['sha256'] and len(payload[x['member']])==x['bytes'] for x in manifest['cases']),manifest['count'])
 ck(checks,'current authority and next item match queue/handoff/pending audit',context['authority']=={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173} and q['next']=='eternal-prophecy' and h['nextPendingGroup']==['eternal-prophecy'] and p['pendingCount']==25 and context['closureTasksRemaining']==25,{'next':q['next'],'authority':q['currentAuthority']})
 ck(checks,'current source comparison remains 140 total /139 unchanged /one index-only change',comp['inventoryCount']==140 and comp['unchangedCount']==139 and comp['changedCount']==1 and comp['changedPaths']==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],comp['changedPaths'])
 ck(checks,'sealed prior Fate Rewrite and Collapse Timeline holds remain intact',fr['heldIds']==['fate-rewrite'] and fr['acceptedIds']==[] and fr['appliedIds']==[] and ct['heldIds']==['collapse-timeline'] and ct['acceptedIds']==[] and ct['appliedIds']==[],{'Fate Rewrite':fr['heldIds'],'Collapse Timeline':ct['heldIds']})
 audit={'id':'ETERNAL-PROPHECY-PACKET-323-READBACK-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'status':'PASS','archive':bind(ARCHIVE),'delivery':bind(DELIVERY),'memberCount':len(names),'targetCaseCount':14,'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':sum(not x['passed'] for x in checks),'checks':checks,'scopeIds':['eternal-prophecy'],'blockerIds':['TF192-B02'],'acceptedIds':[],'appliedIds':[],'canonicalFilesChanged':False,'runtimeExecuted':False}
 out=AUDIT/'ETERNAL_PROPHECY_PACKET_323_READBACK_AUDIT.json';out.write_bytes(pretty(audit))
 print(json.dumps({'status':'PASS','audit':bind(out),'archive':bind(ARCHIVE),'delivery':bind(DELIVERY),'checks':len(checks)},ensure_ascii=False))
