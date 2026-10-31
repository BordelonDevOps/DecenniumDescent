from __future__ import annotations
import hashlib, json, pathlib, re, zipfile, zlib
from datetime import datetime, timezone
ROOT=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
PD=BASE/'rank9_agencycontrol9_current_source_238_prepared'
ARCHIVE=PD/'DD_Rank9_AgencyControl9_CurrentSource_238.zip'
DELIVERY=PD/'DD_Rank9_AgencyControl9_CurrentSource_238_DELIVERY.json'
PREP=BASE/'RANK9_AGENCYCONTROL9_SOURCE_PREPARATION_238.json'
REPORT=BASE/'RANK9_AGENCYCONTROL9_PACKET238_INDEPENDENT_AUDIT.json'
RECEIPT=BASE/'RANK9_AGENCYCONTROL9_PACKET238_RECEIPT.json'
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
IDS=['absolute-domination','puppetmaster-s-realm']
NEXT={'group':'rank9-agency-control9','spellIds':IDS}
checks=[]
def dig(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def j(raw): return json.loads(raw.decode('utf-8-sig'))
def okbind(raw,b):
 d=dig(raw); return isinstance(b,dict) and all(d.get(k)==b.get(k) for k in ('bytes','sha256')) and (b.get('crc32') is None or d['crc32']==b['crc32'])
def safe(n):
 p=pathlib.PurePosixPath(n); return bool(n) and not n.startswith('/') and '\\' not in n and not re.match(r'^[A-Za-z]:',n) and all(x not in ('','.','..') for x in p.parts)
def ck(name,passed,detail=None):checks.append({'check':name,'passed':bool(passed),'detail':detail})
delivery_raw=DELIVERY.read_bytes(); delivery=j(delivery_raw); archive_raw=ARCHIVE.read_bytes(); prep=j(PREP.read_bytes())
ck('outer ZIP matches DELIVERY bytes, SHA-256 and CRC32',okbind(archive_raw,delivery.get('archive')),{'actual':dig(archive_raw),'expected':delivery.get('archive')})
ck('delivery, candidate and preparation bind exact authority, group and target IDs',delivery.get('status')=='PREPARED_UNSENT' and delivery.get('sourceAuthority')==AUTH and delivery.get('group')==NEXT['group'] and delivery.get('pendingIds')==IDS and delivery.get('accepted') is False and delivery.get('applied') is False and prep.get('sourceAuthority')==AUTH and prep.get('group')==NEXT['group'] and prep.get('pendingIds')==IDS and prep.get('checksPassed')==10 and prep.get('checksFailed')==0,{'authority':delivery.get('sourceAuthority'),'group':delivery.get('group'),'ids':delivery.get('pendingIds'),'prepChecks':[prep.get('checksPassed'),prep.get('checksFailed')]})
with zipfile.ZipFile(ARCHIVE) as z:
 names=z.namelist(); name_set=set(names)
 ck('ZIP integrity, unique member paths and safe paths pass',z.testzip() is None and len(names)==len(name_set) and all(safe(n) for n in names),{'members':len(names),'unique':len(name_set)})
 man=j(z.read('MANIFEST.json')); rows=man.get('members',[]); mmap={r.get('path'):r for r in rows if isinstance(r,dict)}
 ck('embedded manifest exactly covers all payload members',man.get('id')=='RANK9-AGENCY-CONTROL9-CURRENT-SOURCE-PACKET-MANIFEST-238' and man.get('sourceAuthority')==AUTH and man.get('group')==NEXT['group'] and man.get('pendingIds')==IDS and set(mmap)==name_set-{'MANIFEST.json'} and len(names)==delivery.get('memberCount') and len(rows)==delivery.get('payloadMemberCount'),{'manifestMembers':len(mmap),'zipMembers':len(names),'deliveryCount':delivery.get('memberCount')})
 bad=[n for n,r in mmap.items() if not okbind(z.read(n),r)]
 ck('every payload member matches embedded size, SHA-256 and CRC32',not bad,bad[:12])
 cand=j(z.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_238.json')); ctx=j(z.read('CURRENT_CONTEXT_238.json')); request=z.read('REQUEST_238.txt').decode('utf-8')
 ck('candidate records only the selected exact two pending IDs at current authority',cand.get('currentAuthority')==AUTH and cand.get('currentPendingIds')==IDS and cand.get('currentPendingGroup',{}).get('spellIds')==IDS and cand.get('countsUnchanged')=={'reviewed':811,'pending':37} and cand.get('currentWardControlReturn237ArchiveDelivered') is True and len(cand.get('records',[]))==9 and {r.get('spellId') for r in cand.get('records',[]) if r.get('currentPending')}==set(IDS),{'authority':cand.get('currentAuthority'),'pendingIds':cand.get('currentPendingIds'),'currentPending':[r.get('spellId') for r in cand.get('records',[]) if r.get('currentPending')],'wardArchiveDelivered':cand.get('currentWardControlReturn237ArchiveDelivered')})
 ck('current candidate and director context bind index, catalog, queue, handoff and pending snapshot',ctx.get('sourceAuthority')==AUTH and ctx.get('targetGroup',{}).get('pendingIds')==IDS and ctx.get('sourceFileCount')==96 and all(ctx.get(k)==cand.get(c) for k,c in [('currentIndexBinding','currentIndexBinding'),('currentCatalogBinding','currentCatalogBinding')]) and ctx.get('queueBinding')==cand.get('currentQueueBinding') and ctx.get('handoffBinding')==cand.get('currentHandoffBinding') and ctx.get('pendingAuditBinding')==cand.get('currentPendingAuditBinding'),{'target':ctx.get('targetGroup'),'sourceCount':ctx.get('sourceFileCount')})
 source_rows=cand.get('sourceBindings',[]); source_bad=[]
 for row in source_rows:
  member='sources_current/'+row.get('path','')
  if member not in name_set or not okbind(z.read(member),row):source_bad.append(row.get('path'))
  local=ROOT/pathlib.Path(row.get('path',''))
  if not local.is_file() or not okbind(local.read_bytes(),row):source_bad.append('LOCAL:'+str(row.get('path')))
 ck('all 96 source files match packet bindings and current working-tree bytes',len(source_rows)==96 and not source_bad,{'sourceRows':len(source_rows),'failures':source_bad[:12]})
 index=j(z.read('current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'))
 catalog=j(z.read('current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'))
 q=j(z.read('current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_237.json'))
 h=j(z.read('current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_237.json'))
 pend=j(z.read('current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_237.json'))
 ir={r.get('id'):r for r in index.get('entries',[])}; cards={r.get('id'):r for r in catalog.get('spells',[])}
 ck('current index/catalog confirm both identities remain pending and unoperational',index.get('authoredCounts')=={'reviewed':811,'pending':37} and index.get('representationCounts',{}).get('completeReviewedStandaloneProcedures')==535 and sum(r.get('authoredStatus')=='pending-authored-procedure' for r in index.get('entries',[]))==37 and all(ir.get(i,{}).get('authoredStatus')=='pending-authored-procedure' and ir.get(i,{}).get('sourceStatus')=='blocked-pending-operational-review' and cards.get(i,{}).get('operational') is None for i in IDS),{'counts':index.get('authoredCounts'),'pending':sum(r.get('authoredStatus')=='pending-authored-procedure' for r in index.get('entries',[]))})
 ck('prior queue/handoff/pending audit agree on 811/37 authority and agency identities pending',q.get('currentAuthority')==h.get('currentAuthority')==pend.get('authority')==AUTH and pend.get('pendingCount')==37 and all(i in pend.get('pendingIds',[]) for i in IDS) and any(g.get('group')==NEXT['group'] and g.get('pendingIds')==IDS for g in q.get('currentPendingGroups',[])),{'q':q.get('currentAuthority'),'h':h.get('currentAuthority'),'pending':pend.get('authority')})
 # Bind sealed Return237 and exact delivery/audit files embedded in this packet to local files.
 return_base='docs/audit/2026-10-08/full-game/director-spell-review-129/'
 retzip_rel=return_base+'rank9_wardcontrol6_return237_received/DD_Rank9_WardControl2_Director_Return237.zip'
 retdel_rel=return_base+'rank9_wardcontrol6_return237_received/DD_Rank9_WardControl2_Director_Return237_DELIVERY.json'
 retaudit_rel=return_base+'RANK9_WARDCONTROL6_RETURN237_INDEPENDENT_AUDIT.json'
 retreceipt_rel=return_base+'RANK9_WARDCONTROL6_RETURN237_RECEIPT.json'
 retzip_raw=z.read('current/'+retzip_rel); retdel=j(z.read('current/'+retdel_rel)); retaudit=j(z.read('current/'+retaudit_rel)); retreceipt=j(z.read('current/'+retreceipt_rel))
 retlocal=ROOT/retzip_rel; retlocaldel=ROOT/retdel_rel
 with zipfile.ZipFile(retlocal) as rz: retdecision=j(rz.read('DIRECTOR_DECISION.json'))
 ck('sealed Return237 ZIP, matching delivery, audit and receipt are embedded byte-identically to local records',all(z.read('current/'+rel)==(ROOT/rel).read_bytes() for rel in [retzip_rel,retdel_rel,retaudit_rel,retreceipt_rel]) and okbind(retlocal.read_bytes(),retaudit.get('archive',{})) and okbind(retlocaldel.read_bytes(),retaudit.get('deliveryManifest',{})) and okbind(retlocal.read_bytes(),retreceipt.get('archive',{})) and okbind(retlocaldel.read_bytes(),retreceipt.get('deliveryManifest',{})),{'returnHash':dig(retlocal.read_bytes()),'deliveryHash':dig(retlocaldel.read_bytes()),'auditStatus':retaudit.get('status')})
 ck('Return237 is held/unapplied, PASS 17/17, and selected this exact Agency group',retaudit.get('status')==retreceipt.get('status')=='PASS' and retaudit.get('checkCount')==retreceipt.get('checkCount')==17 and retdecision.get('heldIds')==['nullification-wave','reality-anchor'] and retdecision.get('acceptedIds')==retdecision.get('appliedIds')==[] and retdel.get('nextPendingGroup')==NEXT and retdecision.get('authorityAfter')==AUTH,{'held':retdecision.get('heldIds'),'next':retdel.get('nextPendingGroup'),'audit':retaudit.get('status')})
 packet237=(BASE/'rank9_wardcontrol6_source_packet_237_refreshed/DD_Rank9_WardControl6_CurrentSource_237.zip').read_bytes(); packet237_delivery=j((BASE/'rank9_wardcontrol6_source_packet_237_refreshed/DD_Rank9_WardControl6_CurrentSource_237_DELIVERY.json').read_bytes())
 ck('Return237 source packet link still matches independently reviewed Packet237 archive and delivery',okbind(packet237,retdel.get('sourcePacket',{})) and okbind(packet237,packet237_delivery.get('archive',{})),{'packet':dig(packet237),'deliveryArchive':packet237_delivery.get('archive')})
 # Validate prior Agency gates are supplied, held and retained.
 agency=ctx.get('priorAgencyReturn190Holds',{}); blockers=agency.get('blockers',{})
 ck('the two exact prior Agency blockers and qualifications are retained',set(agency.get('ids',[]))==set(IDS) and blockers.get('absolute-domination',{}).get('blockerIds')==['AG190-B01'] and blockers.get('puppetmaster-s-realm',{}).get('blockerIds')==['AG190-B02'],{'ids':agency.get('ids'),'blockers':{i:blockers.get(i,{}).get('blockerIds') for i in IDS}})
 ck('the request asks for only the two pending identities and preserves no-application gates',all(x in request for x in ('Review only the two currently pending','absolute-domination and puppetmaster-s-realm','Do not re-review accepted Agency/Control9 identities or feats','Keep every acceptance unapplied','do not edit canonical files','runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates')),{'requestBytes':len(request)})
 ck('packet delivery and authority explicitly prohibit acceptance/application before GPT review',delivery.get('accepted') is False and delivery.get('applied') is False and delivery.get('sourceAuthority')==AUTH and delivery.get('group')==NEXT['group'] and delivery.get('pendingIds')==IDS,{'accepted':delivery.get('accepted'),'applied':delivery.get('applied')})
fail=[x for x in checks if not x['passed']]
report={'id':'RANK9-AGENCY-CONTROL9-PACKET238-INDEPENDENT-AUDIT','checkedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not fail else 'FAIL','archive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),**dig(archive_raw)},'deliveryManifest':{'path':DELIVERY.relative_to(ROOT).as_posix(),**dig(delivery_raw)},'authority':delivery.get('sourceAuthority'),'group':delivery.get('group'),'pendingIds':delivery.get('pendingIds'),'sourceBindingsVerified':len(source_rows),'checkCount':len(checks),'passedChecks':len(checks)-len(fail),'failedChecks':len(fail),'checks':checks}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt={'id':'RANK9-AGENCY-CONTROL9-PACKET238-RECEIPT','status':report['status'],'archive':report['archive'],'deliveryManifest':report['deliveryManifest'],'independentAudit':{'path':REPORT.relative_to(ROOT).as_posix(),**dig(REPORT.read_bytes())},'checkCount':len(checks),'passedChecks':len(checks)-len(fail),'failedChecks':len(fail)}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'checkCount':len(checks),'passedChecks':len(checks)-len(fail),'failedChecks':len(fail),'failures':fail,'archive':report['archive'],'group':delivery.get('group'),'pendingIds':delivery.get('pendingIds')},ensure_ascii=False,indent=2))
