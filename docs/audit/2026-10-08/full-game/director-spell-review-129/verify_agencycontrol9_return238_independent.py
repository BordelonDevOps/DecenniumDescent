from __future__ import annotations
import hashlib,json,pathlib,re,zipfile,zlib
from datetime import datetime,timezone
ROOT=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RCV=BASE/'rank9_agencycontrol9_return238_received'
ARCHIVE=RCV/'DD_Rank9_AgencyControl2_Director_Return238.zip'
DELIVERY=RCV/'DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json'
SOURCE_PACKET=BASE/'rank9_agencycontrol9_current_source_238_prepared/DD_Rank9_AgencyControl9_CurrentSource_238.zip'
SOURCE_DELIVERY=BASE/'rank9_agencycontrol9_current_source_238_prepared/DD_Rank9_AgencyControl9_CurrentSource_238_DELIVERY.json'
PACKET_AUDIT=BASE/'RANK9_AGENCYCONTROL9_PACKET238_INDEPENDENT_AUDIT.json'
PACKET_RECEIPT=BASE/'RANK9_AGENCYCONTROL9_PACKET238_RECEIPT.json'
REPORT=BASE/'RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json'
RECEIPT=BASE/'RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json'
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
TARGETS=['absolute-domination','puppetmaster-s-realm']
BLOCKERS={'absolute-domination':['AG190-B01'],'puppetmaster-s-realm':['AG190-B02']}
QUALS=['AG190-H-SOURCE','AG190-H-PHYSICAL','AG190-H-CONTENT','AG190-H-LIFECYCLE','AG190-H-RUNTIME','AG190-H-PLAY','AG190-H-BALANCE','AG190-H-COSMOLOGY','AG190-H-DOMAIN','AG190-H-RELEASE']
NEXT={'group':'rank9-time-fate6','spellIds':['time-stop','fate-rewrite','collapse-timeline','eternal-prophecy']}
checks=[]
def dig(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'}
def readj(raw):return json.loads(raw.decode('utf-8-sig'))
def matches(raw,expected):
 got=dig(raw); return isinstance(expected,dict) and all(got.get(k)==expected.get(k) for k in ('bytes','sha256')) and (expected.get('crc32') is None or got['crc32']==expected['crc32'])
def safe(name):
 p=pathlib.PurePosixPath(name);return bool(name) and not name.startswith('/') and '\\' not in name and not re.match(r'^[A-Za-z]:',name) and all(x not in ('','.','..') for x in p.parts)
def ck(name,passed,detail=None):checks.append({'check':name,'passed':bool(passed),'detail':detail})
archive_raw=ARCHIVE.read_bytes();delivery_raw=DELIVERY.read_bytes();d=readj(delivery_raw)
source_raw=SOURCE_PACKET.read_bytes();source_delivery=readj(SOURCE_DELIVERY.read_bytes());pa=readj(PACKET_AUDIT.read_bytes());pr=readj(PACKET_RECEIPT.read_bytes())
ck('downloaded Return238 ZIP matches its exact delivery binding',d.get('return')==238 and matches(archive_raw,d.get('archive')) and d['archive'].get('path')==ARCHIVE.name,{'actual':dig(archive_raw),'expected':d.get('archive')})
ck('decision disposition, authority and next-group IDs are exact',d.get('accepted') is False and d.get('applied') is False and d.get('acceptedIds')==d.get('appliedIds')==[] and d.get('heldIds')==TARGETS and d.get('authority')==AUTH and d.get('nextPendingGroup')==NEXT and d.get('blockerIds')==['AG190-B01','AG190-B02'],{'authority':d.get('authority'),'accepted':d.get('acceptedIds'),'applied':d.get('appliedIds'),'held':d.get('heldIds'),'next':d.get('nextPendingGroup')})
ck('Return238 source packet binding exactly matches Packet238',matches(source_raw,d.get('sourcePacket',{})) and matches(source_raw,source_delivery.get('archive',{})) and matches(source_raw,source_delivery.get('archive',{})) and source_delivery.get('sourceAuthority')==AUTH and source_delivery.get('group')=='rank9-agency-control9' and source_delivery.get('pendingIds')==TARGETS,{'packet':dig(source_raw),'bound':d.get('sourcePacket')})
with zipfile.ZipFile(ARCHIVE) as z:
 names=z.namelist(); name_set=set(names)
 ck('Return238 ZIP central directory, safe names and unique members pass',z.testzip() is None and len(names)==len(name_set)==d.get('memberCount')==64 and all(safe(n) for n in names),{'members':len(names),'unique':len(name_set)})
 external={r.get('path'):r for r in d.get('members',[]) if isinstance(r,dict)};allow=d.get('exactAllowlist',[])
 ck('external allowlist, external member rows and ZIP names exactly agree',len(allow)==len(external)==64 and set(allow)==name_set==set(external),{'allowlist':len(allow),'externalRows':len(external),'zipMembers':len(names)})
 ext_bad=[n for n in names if n not in external or not matches(z.read(n),external.get(n,{}))]
 ck('all 64 ZIP members match external size, SHA-256 and CRC32 rows',not ext_bad,ext_bad[:12])
 embedded=readj(z.read('MEMBER_MANIFEST.json'));mm={r.get('path'):r for r in embedded.get('members',[]) if isinstance(r,dict)}
 ck('embedded member manifest covers exactly the 63 non-self members',embedded.get('return')==238 and embedded.get('manifestSelfExcluded') is True and embedded.get('payloadMemberCount')==63 and len(mm)==63 and set(mm)==name_set-{'MEMBER_MANIFEST.json'},{'declared':embedded.get('payloadMemberCount'),'members':len(mm)})
 int_bad=[n for n,row in mm.items() if not matches(z.read(n),row)]
 ck('all non-self members match embedded hash, size and CRC32',not int_bad,int_bad[:12])
 decision=readj(z.read('DIRECTOR_DECISION.json')); counts=readj(z.read('COUNTS.json')); case_index=readj(z.read('CASE_INDEX.json'))
 ck('sealed decision remains unapplied and preserves authority',decision.get('return')==238 and decision.get('accepted') is False and decision.get('applied') is False and decision.get('applicationPerformed') is False and decision.get('canonicalFilesEdited') is False and decision.get('acceptedIds')==decision.get('appliedIds')==[] and decision.get('heldIds')==TARGETS and decision.get('authorityBefore')==decision.get('authorityAfter')==AUTH and d.get('authority')==AUTH,{'return':decision.get('return'),'before':decision.get('authorityBefore'),'after':decision.get('authorityAfter')})
 per={r.get('spellId'):r for r in decision.get('perIdentity',[])}
 expected_per_quals={'absolute-domination':QUALS,'puppetmaster-s-realm':QUALS+['H150-ROSTER']}
 ck('both per-identity blocker decisions and retained qualifications match the director table',set(per)==set(TARGETS) and all(per[i].get('accepted') is False and per[i].get('applied') is False and per[i].get('blockerIds')==BLOCKERS[i] and per[i].get('qualificationIds')==expected_per_quals[i] for i in TARGETS) and d.get('qualificationIds')==QUALS+['H150-ROSTER'],{'blockers':{i:per.get(i,{}).get('blockerIds') for i in TARGETS},'perIdentityQualifications':{i:per.get(i,{}).get('qualificationIds') for i in TARGETS},'qualifications':d.get('qualificationIds')})
 holds=readj(z.read('HOLD_REGISTER.json'))
 hold_rows={row.get('id'):row for row in holds.get('blockers',[]) if 'acceptance blocker' in row.get('kind','')}
 ck('source witness findings keep both minimum blockers open and preserve ward holds',set(hold_rows)=={x for values in BLOCKERS.values() for x in values} and all(hold_rows[BLOCKERS[i][0]].get('closed') is False and hold_rows[BLOCKERS[i][0]].get('blockingForIds')==[i] for i in TARGETS) and d.get('preservedWardHoldIds')==['WC188-B01','WC188-B02'] and holds.get('preservedUnrelatedBlockerIds')==['WC188-B01','WC188-B02'] and holds.get('additionalInheritedQualificationIds')==['H150-ROSTER','WC188-H-UNIQUE-PROPERTY'],{'blockers':list(hold_rows),'ward':d.get('preservedWardHoldIds'),'inherited':holds.get('additionalInheritedQualificationIds')})
 next_doc=readj(z.read('NEXT_PENDING_GROUP.json'))
 ck('sealed NEXT_PENDING_GROUP and delivery select exactly the four currently pending Time/Fate6 IDs',next_doc==NEXT and d.get('nextPendingGroup')==NEXT,{'next':next_doc})
 case_rows=case_index.get('cases',[]);case_paths=[r.get('path') for r in case_rows];case_members={n for n in names if n.startswith('cases/')}
 agg={key:sum(int(row.get(key,0)) for row in case_rows) for key in ('events','forwardOperations','inverseOperations')}
 ck('case index, member paths and aggregate reversible replay counts reconcile',len(case_rows)==15 and len(case_members)==15 and set(case_paths)==case_members and agg=={'events':315,'forwardOperations':630,'inverseOperations':630} and counts.get('cases')==15 and counts.get('events')==315 and counts.get('forwardEventOperations')==630 and counts.get('inverseEventOperations')==630 and all(r.get('numericReplay')=='PASS' for r in case_rows),{'caseCount':len(case_rows),'caseMembers':len(case_members),'aggregates':agg})
 case_member_bad=[];case_source_bad=[]
 local_cases=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01/cases'
 for row in case_rows:
  n=row['path']; raw=z.read(n)
  if not matches(raw,row):case_member_bad.append(n)
  local=local_cases/pathlib.Path(n).name
  if not local.is_file() or local.read_bytes()!=raw:case_source_bad.append(n)
 ck('all 15 prior Agency case bytes remain unchanged from the already-applied reviewed package',not case_member_bad and not case_source_bad,{'returnBindingFailures':case_member_bad[:10],'priorPackageDifferences':case_source_bad[:10]})
 preservation=readj(z.read('PRESERVATION_CHECK.json'));semantic=readj(z.read('PRESERVED_SEMANTIC_ASSERTIONS_CHECK.json'));proposal=readj(z.read('PROPOSAL_CHECK.json'))
 ck('preservation, preserved semantic assertions and proposal package integrity pass',preservation.get('status')==semantic.get('status')==proposal.get('status')=='PASS' and preservation.get('checkCount')==30 and preservation.get('failureCount')==0 and semantic.get('checkCount')==10 and semantic.get('failureCount')==0 and proposal.get('checkCount')==8 and proposal.get('failureCount')==0 and all(r.get('pass') is True for r in preservation.get('checks',[])+semantic.get('checks',[])+proposal.get('checks',[])),{'checks':[preservation.get('checkCount'),semantic.get('checkCount'),proposal.get('checkCount')]})
 data=readj(z.read('DATA_INTEGRITY_CHECK.json'));clock=readj(z.read('CLOCK_CHECK.json'));actor=readj(z.read('ACTOR_ACCESS_CHECK.json'));source=readj(z.read('SOURCE_CHECK.json'))
 ck('data, clock, actor-access and source replay checks all pass at declared totals',data.get('checkCount')==3840 and len(data.get('checks',[]))==3840 and all(x.get('pass') is True for x in data['checks']) and clock.get('status')=='PASS' and clock.get('checkCount')==len(clock.get('checks',[]))==2972 and clock.get('failureCount')==0 and actor.get('status')=='PASS' and actor.get('checkCount')==len(actor.get('checks',[]))==1265 and actor.get('failureCount')==0 and source.get('status')=='PASS' and source.get('checkCount')==len(source.get('checks',[]))==904 and source.get('sourceBindingsVerified')==96 and source.get('failureCount')==0,{'data':data.get('checkCount'),'clock':clock.get('checkCount'),'actor':actor.get('checkCount'),'source':source.get('checkCount')})
 src=readj(z.read('SOURCE_BINDINGS.json')); rows=src.get('sourceBindings',[])
 ck('SOURCE_BINDINGS binds exact current Packet238 archive, delivery and all 96 sources',len(rows)==96 and src.get('packet',{}).get('sha256')==dig(source_raw)['sha256'] and src.get('delivery',{}).get('sha256')==dig(SOURCE_DELIVERY.read_bytes())['sha256'] and src.get('externalSourceArchiveRequired') is True and src.get('notDuplicatedInReturn') is True,{'sourceRows':len(rows),'packet':src.get('packet'),'delivery':src.get('delivery')})
 source_bad=[]
 with zipfile.ZipFile(SOURCE_PACKET) as source_zip:
  source_names=set(source_zip.namelist())
  for row in rows:
   n='sources_current/'+row['path']
   if n not in source_names or not matches(source_zip.read(n),row):source_bad.append(row['path'])
 ck('all 96 current source bindings verify against exact Packet238 source members',not source_bad,source_bad[:12])
 with zipfile.ZipFile(SOURCE_PACKET) as source_zip:
  packet_manifest=readj(source_zip.read('MANIFEST.json'))
 ck('Return238 carries the exact embedded Packet238 manifest and current decision evidence',src.get('packetManifest')==packet_manifest and z.read('evidence/PACKET238_DELIVERY.json')==SOURCE_DELIVERY.read_bytes() and z.read('evidence/PACKET238_INDEPENDENT_AUDIT.json')==PACKET_AUDIT.read_bytes() and z.read('evidence/PACKET238_RECEIPT.json')==PACKET_RECEIPT.read_bytes() and pa.get('status')=='PASS' and pa.get('checkCount')==16 and pr.get('status')=='PASS',{'packetAudit':pa.get('status'),'packetAuditChecks':pa.get('checkCount')})
 semantic_failure=readj(z.read('INDEPENDENT_SEMANTIC_FAILURE_CHECK.json'))
 ck('independent semantic gate passes while both missing source witnesses remain open',semantic_failure.get('status')=='PASS' and semantic_failure.get('decisionStatus')=='HELD_REQUIRED_SOURCE_WITNESSES' and semantic_failure.get('acceptedIds')==semantic_failure.get('appliedIds')==[] and semantic_failure.get('heldIds')==TARGETS and semantic_failure.get('failureCount')==0 and semantic_failure.get('checkCount')==14,{'status':semantic_failure.get('status'),'held':semantic_failure.get('heldIds'),'checkCount':semantic_failure.get('checkCount')})
 package_checks=d.get('packageChecks',{}); pc=package_checks.get('checks',[])
 ck('delivery reports all 195 package-integrity checks passing',package_checks.get('checkCount')==195 and len(pc)==195 and all(x.get('pass') is True for x in pc),{'checks':package_checks.get('checkCount'),'failures':[x for x in pc if x.get('pass') is not True][:5]})
 # Archive-bound delivery is exact and no action or canonical edits occurred.
 ck('no spell application, canonical edit, or other cohort reopening occurred',decision.get('applicationPerformed') is False and decision.get('canonicalFilesEdited') is False and decision.get('noOtherCohortReopened') is True and holds.get('allOtherCurrentHoldsUnchanged') is True,{'applied':decision.get('applied'),'canonicalEdited':decision.get('canonicalFilesEdited'),'noOtherCohortReopened':decision.get('noOtherCohortReopened')})
fail=[x for x in checks if not x['passed']]
report={'id':'RANK9-AGENCY-CONTROL9-RETURN238-INDEPENDENT-AUDIT','checkedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not fail else 'FAIL','return':238,'archive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),**dig(archive_raw)},'deliveryManifest':{'path':DELIVERY.relative_to(ROOT).as_posix(),**dig(delivery_raw)},'authority':d.get('authority'),'acceptedIds':d.get('acceptedIds'),'appliedIds':d.get('appliedIds'),'heldIds':d.get('heldIds'),'blockerIds':d.get('blockerIds'),'qualificationIds':d.get('qualificationIds'),'nextPendingGroup':d.get('nextPendingGroup'),'checkCount':len(checks),'passedChecks':len(checks)-len(fail),'failedChecks':len(fail),'checks':checks,'scopeLimitation':'Independent verification covers archive transfer, member integrity, source bindings to the exact Packet238 archive, preserved case bytes against the previously applied Agency package, replay totals, and decision scope. It does not independently adjudicate the underlying game rules beyond the recorded source and case evidence.'}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt={'id':'RANK9-AGENCY-CONTROL9-RETURN238-RECEIPT','status':report['status'],'archive':report['archive'],'deliveryManifest':report['deliveryManifest'],'independentAudit':{'path':REPORT.relative_to(ROOT).as_posix(),**dig(REPORT.read_bytes())},'checkCount':len(checks),'passedChecks':len(checks)-len(fail),'failedChecks':len(fail),'scopeLimitation':report['scopeLimitation']}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'checkCount':len(checks),'passedChecks':len(checks)-len(fail),'failedChecks':len(fail),'failures':fail,'archive':report['archive'],'heldIds':d.get('heldIds'),'next':d.get('nextPendingGroup')},ensure_ascii=False,indent=2))
