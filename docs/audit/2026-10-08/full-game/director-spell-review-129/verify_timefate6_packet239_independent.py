from __future__ import annotations
import hashlib,json,pathlib,re,zipfile,zlib
from datetime import datetime,timezone

ROOT=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT=BASE/'rank9_timefate6_current_source_239_prepared'
PACKET=OUT/'DD_Rank9_TimeFate6_CurrentSource_239.zip'; DELIVERY=OUT/'DD_Rank9_TimeFate6_CurrentSource_239_DELIVERY.json'
QUEUE=BASE/'CURRENT_SPELL_QUEUE_239.json'; HANDOFF=BASE/'CURRENT_HANDOFF_239.json'; PENDING=BASE/'CURRENT37_PENDING_IDENTITY_AUDIT_239.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'; CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
P238=BASE/'rank9_agencycontrol9_current_source_238_prepared/DD_Rank9_AgencyControl9_CurrentSource_238.zip'
P238D=BASE/'rank9_agencycontrol9_current_source_238_prepared/DD_Rank9_AgencyControl9_CurrentSource_238_DELIVERY.json'
R238=BASE/'rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip'; R238D=BASE/'rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json'
R238A=BASE/'RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json'; R238R=BASE/'RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json'
R221=BASE/'rank9_timefate6_return221_received/DD_Rank9_TimeFate4_Director_Return221_HELD.zip'; R221D=BASE/'rank9_timefate6_return221_received/DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json'
R221A=BASE/'RANK9_TIMEFATE6_RETURN221_INDEPENDENT_AUDIT.json'; R221R=BASE/'RANK9_TIMEFATE6_RETURN221_RECEIPT.json'
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
IDS=['time-stop','fate-rewrite','collapse-timeline','eternal-prophecy']; checks=[]
def rawjson(b):return json.loads(b.decode('utf-8-sig'))
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def match(b,row):
 d=digest(b);return isinstance(row,dict) and all(d[k]==row.get(k) for k in ('bytes','sha256')) and (row.get('crc32') is None or row['crc32']==d['crc32'])
def safe(n):
 p=pathlib.PurePosixPath(n);return bool(n) and '\\' not in n and not p.is_absolute() and all(x not in ('','.','..') and not x.startswith('.') for x in p.parts)
def ck(name,ok,detail=None):checks.append({'check':name,'passed':bool(ok),'detail':detail})

packet=PACKET.read_bytes();delivery=rawjson(DELIVERY.read_bytes());q=rawjson(QUEUE.read_bytes());h=rawjson(HANDOFF.read_bytes());p=rawjson(PENDING.read_bytes())
index=rawjson(INDEX.read_bytes());catalog=rawjson(CATALOG.read_bytes())
ck('Packet239 ZIP matches delivery bytes, SHA-256 and CRC32',match(packet,delivery.get('archive')) and delivery.get('status')=='PREPARED_UNSENT',digest(packet))
ck('delivery, queue, handoff and pending snapshot agree on 811/37/0 authority and exact Time/Fate IDs',delivery.get('sourceAuthority')==q.get('currentAuthority')==h.get('currentAuthority')==p.get('authority')==AUTH and delivery.get('group')=='rank9-time-fate6' and delivery.get('pendingIds')==IDS and p.get('pendingCount')==37 and set(IDS)<=set(p.get('pendingIds',[])) and q.get('nextGroup')=='rank9-time-fate6' and h.get('nextGroup')=='rank9-time-fate6',{'authority':delivery.get('sourceAuthority'),'pendingIds':delivery.get('pendingIds')})
ix={x['id']:x for x in index['entries']};cat={x['id']:x for x in catalog['spells']}
ck('all four targets remain pending and non-operational in current index/catalog',index.get('authoredCounts')=={'reviewed':811,'pending':37} and index.get('representationCounts',{}).get('completeReviewedStandaloneProcedures')==535 and all(ix[s]['authoredStatus']=='pending-authored-procedure' and ix[s]['sourceStatus']=='blocked-pending-operational-review' and cat[s].get('operational') is None for s in IDS),{'indexCounts':index.get('authoredCounts')})
with zipfile.ZipFile(PACKET) as z:
 names=z.namelist(); ns=set(names)
 ck('ZIP directory is sound, paths are safe, unique, and manifest is exact',z.testzip() is None and len(names)==len(ns)==delivery.get('memberCount') and all(safe(n) for n in names) and 'MANIFEST.json' in ns,{'members':len(names),'unique':len(ns)})
 manifest=rawjson(z.read('MANIFEST.json')); rows={x.get('path'):x for x in manifest.get('members',[]) if isinstance(x,dict)}
 ck('embedded manifest covers every payload member and declares current packet scope',manifest.get('sourceAuthority')==AUTH and manifest.get('group')=='rank9-time-fate6' and manifest.get('pendingIds')==IDS and manifest.get('payloadMemberCount')==len(rows)==len(names)-1 and set(rows)==ns-{'MANIFEST.json'},{'payload':len(rows),'zip':len(names)})
 bad=[n for n,row in rows.items() if not match(z.read(n),row)]
 ck('every payload member matches embedded size, SHA-256 and CRC32',not bad,bad[:12])
 candidate=rawjson(z.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_239.json'));context=rawjson(z.read('CURRENT_CONTEXT_239.json'))
 source_rows=candidate.get('sourceBindings',[]); source_bad=[]
 ck('candidate and director context bind exact current group, authority, 140 sources and Return238',candidate.get('currentAuthority')==context.get('sourceAuthority')==AUTH and candidate.get('currentPendingGroup')=={'group':'rank9-time-fate6','spellIds':IDS,'count':4} and len(source_rows)==140 and context.get('pendingIds')==IDS and context.get('return238Audit',{}).get('sha256')==digest(R238A.read_bytes())['sha256'] and candidate.get('currentAgencyControlReturn238AuditBinding',{}).get('sha256')==digest(R238A.read_bytes())['sha256'],{'sources':len(source_rows),'authority':candidate.get('currentAuthority')})
 for row in source_rows:
  n='sources_current/'+row['path']
  if n not in ns or not match(z.read(n),row) or (ROOT/row['path']).read_bytes()!=z.read(n):source_bad.append(row['path'])
 ck('all 140 source bindings verify against packet and current working-tree bytes',not source_bad,source_bad[:12])
 # Previously sealed history and the latest return/source evidence must be byte-exact inside the packet.
 bundle={'authority_history/return221/DD_Rank9_TimeFate4_Director_Return221_HELD.zip':R221,
  'authority_history/return221/DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json':R221D,
  'authority_history/return221/INDEPENDENT_AUDIT.json':R221A,'authority_history/return221/RECEIPT.json':R221R,
  'authority_history/return238/DD_Rank9_AgencyControl2_Director_Return238.zip':R238,
  'authority_history/return238/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json':R238D,
  'authority_history/return238/INDEPENDENT_AUDIT.json':R238A,'authority_history/return238/RECEIPT.json':R238R,
  'authority_history/packet238/DD_Rank9_AgencyControl9_CurrentSource_238.zip':P238,'authority_history/packet238/DD_Rank9_AgencyControl9_CurrentSource_238_DELIVERY.json':P238D}
 bundle_bad=[n for n,path in bundle.items() if n not in ns or z.read(n)!=path.read_bytes()]
 ck('Return221, Return238 and Packet238 source evidence are bundled byte-exactly',not bundle_bad,bundle_bad)
 ck('previous Time/Fate ruling remains all-held; Return238 is audited and selects this exact next group',rawjson(R221D.read_bytes()).get('heldIds')==IDS and rawjson(R221D.read_bytes()).get('acceptedIds')==[] and rawjson(R221D.read_bytes()).get('applied') is False and rawjson(R221A.read_bytes()).get('checksFailed')==0 and rawjson(R238A.read_bytes()).get('status')=='PASS' and rawjson(R238D.read_bytes()).get('nextPendingGroup')=={'group':'rank9-time-fate6','spellIds':IDS},None)
 req=z.read('REQUEST_239.txt').decode()
 ck('request confines GPT review to four pending IDs, carries forward blockers, and forbids application',all(x in req for x in IDS+['TF192-B01','TF192-B02','TF192-B04','TF192-B05']) and 'Review only' in req and 'Keep all acceptances unapplied' in req and 'completed feats' in req,{'requestBytes':len(req)})
 prep=rawjson((BASE/'RANK9_TIMEFATE6_SOURCE_PREPARATION_239.json').read_bytes())
 ck('preparation record passes declared checks and records no canonical changes or application',prep.get('checksPassed')==10 and prep.get('checksFailed')==0 and prep.get('canonicalChangesBeforePreparation') is False and prep.get('accepted') is False and prep.get('applied') is False,{'status':prep.get('status'),'passed':prep.get('checksPassed'),'failed':prep.get('checksFailed')})

fail=[x for x in checks if not x['passed']]
report={'id':'RANK9-TIME-FATE6-PACKET239-INDEPENDENT-AUDIT','checkedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not fail else 'FAIL','archive':{'path':PACKET.relative_to(ROOT).as_posix(),**digest(packet)},'deliveryManifest':{'path':DELIVERY.relative_to(ROOT).as_posix(),**digest(DELIVERY.read_bytes())},'authority':AUTH,'group':'rank9-time-fate6','pendingIds':IDS,'sourceBindingsVerified':140,'checkCount':len(checks),'passedChecks':len(checks)-len(fail),'failedChecks':len(fail),'checks':checks,'scopeLimitation':'Validates packet transfer, source/member binding, authority scope and preserved prior decision evidence; it does not independently adjudicate the underlying game rules.'}
report_path=BASE/'RANK9_TIMEFATE6_PACKET239_INDEPENDENT_AUDIT.json';report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt={'id':'RANK9-TIME-FATE6-PACKET239-RECEIPT','status':report['status'],'archive':report['archive'],'deliveryManifest':report['deliveryManifest'],'independentAudit':{'path':report_path.relative_to(ROOT).as_posix(),**digest(report_path.read_bytes())},'checkCount':len(checks),'passedChecks':len(checks)-len(fail),'failedChecks':len(fail),'scopeLimitation':report['scopeLimitation']}
(BASE/'RANK9_TIMEFATE6_PACKET239_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'checks':len(checks),'passed':len(checks)-len(fail),'failed':len(fail),'failures':fail,'packet':report['archive']},ensure_ascii=False,indent=2))
