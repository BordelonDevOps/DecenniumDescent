from __future__ import annotations
import hashlib,json,pathlib,zipfile,zlib
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[5];AUDIT=pathlib.Path(__file__).resolve().parent
OUT=AUDIT/'rank9_faction_omniscience_supreme_current_source_326_build03_prepared'
ARCHIVE=OUT/'DD_Rank9_FactionOmniscienceSupreme_CurrentSource_326.zip';DELIVERY=OUT/'DD_Rank9_FactionOmniscienceSupreme_CurrentSource_326_DELIVERY.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def crc(b):return f'{zlib.crc32(b)&0xffffffff:08x}'
def pretty(o):return(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def ck(cs,n,ok,detail=None):
 cs.append({'check':n,'passed':bool(ok),'detail':detail})
 if not ok:raise AssertionError(f'{n}: {detail}')
d=json.loads(DELIVERY.read_text(encoding='utf-8'));raw=ARCHIVE.read_bytes();cs=[]
ck(cs,'archive matches delivery bytes/SHA-256/CRC32',len(raw)==d['archive']['bytes'] and sha(raw)==d['archive']['sha256'] and crc(raw)==d['archive']['crc32'],d['archive'])
ck(cs,'delivery is FOS/KR198-B01 only with no acceptance/application',d['scopeIds']==['faction-omniscience-supreme'] and d['blockerIds']==['KR198-B01'] and d['acceptedIds']==[] and d['appliedIds']==[] and d['heldIds']==[],d)
with zipfile.ZipFile(ARCHIVE) as z:
 names=z.namelist();ck(cs,'ZIP CRC and unique safe paths',z.testzip() is None and len(names)==len(set(names)) and all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in names),{'members':len(names)})
 payload={n:z.read(n) for n in names};ctx=json.loads(payload['CONTEXT.json']);m=json.loads(payload['evidence/cases/faction-omniscience-supreme_manifest.json']);q=json.loads(payload['authority/current/CURRENT_SPELL_QUEUE_325.json']);comp=json.loads(payload['evidence/source_comparison/current_worktree_140_source_comparison.json']);r283=json.loads(zipfile.ZipFile(__import__('io').BytesIO(payload['evidence/prior_review/Return283_HELD.zip'])).read('DIRECTOR_DECISION.json'));cand=json.loads(payload['evidence/unqualified_seasonal_candidates/LEDGER_CANDIDATE_SCOPE_REVIEW.json'])
 ck(cs,'all 8 target case files exactly match current procedure manifest',m['count']==8 and all(x['member'] in payload and len(payload[x['member']])==x['bytes'] and sha(payload[x['member']])==x['sha256'] for x in m['cases']),m['count'])
 ck(cs,'current authority/queue and explicit next target bind 823/25/0',ctx['authority']=={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173} and q['currentAuthority']==ctx['authority'] and q['next']=='faction-omniscience-supreme' and ctx['closureTasksRemaining']==25,{'next':q['next'],'authority':ctx['authority']})
 ck(cs,'current 140 source comparison remains 139 unchanged/one index-only delta',comp['inventoryCount']==140 and comp['unchangedCount']==139 and comp['changedCount']==1 and comp['changedPaths']==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],comp['changedPaths'])
 ck(cs,'Return283 prior FOS hold remains historical and unapplied',r283['heldIds']==['faction-omniscience-supreme'] and r283['acceptedIds']==[] and r283['appliedIds']==[] and r283['sourceAuthority']['pending']==32,{'held':r283['heldIds'],'historicalPending':r283['sourceAuthority']['pending']})
 ck(cs,'20 seasonal candidate files are explicitly unadjudicated and not promoted to canon',ctx['seasonalRecordsRemainUnadjudicated'] is True and cand['classification'].startswith('Unadjudicated') and len(cand['files'])==20,{'files':len(cand['files']),'classification':cand['classification']})
 audit={'id':'FACTION-OMNISCIENCE-SUPREME-PACKET-326-READBACK-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'status':'PASS','archive':bind(ARCHIVE),'delivery':bind(DELIVERY),'memberCount':len(names),'targetCaseCount':8,'unadjudicatedSeasonalFiles':20,'checkCount':len(cs),'passedChecks':sum(x['passed'] for x in cs),'failedChecks':sum(not x['passed'] for x in cs),'checks':cs,'scopeIds':['faction-omniscience-supreme'],'blockerIds':['KR198-B01'],'acceptedIds':[],'appliedIds':[],'canonicalFilesChanged':False,'runtimeExecuted':False}
 out=AUDIT/'FACTION_OMNISCIENCE_SUPREME_PACKET_326_READBACK_AUDIT.json';out.write_bytes(pretty(audit))
 print(json.dumps({'status':'PASS','audit':bind(out),'archive':bind(ARCHIVE),'delivery':bind(DELIVERY),'checks':len(cs)},ensure_ascii=False))
