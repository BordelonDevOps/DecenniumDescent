#!/usr/bin/env python3
"""Independently receive and advance the Faction Perfection Return338 HOLD."""
from __future__ import annotations
import hashlib,json,shutil,zlib
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
from zipfile import ZipFile

A=Path(__file__).resolve().parent
ROOT=A.parents[4]
PREP=A/'rank9_faction_perfection_review_338_prepared'
PREPZIP=PREP/'DD_Rank9_FactionPerfection_Review338.zip'
PREPDEL=PREP/'DD_Rank9_FactionPerfection_Review338_DELIVERY.json'
DOWNLOADS=Path.home()/'Downloads'
INZIP=DOWNLOADS/'DD_FactionPerfection_Director_Return338_HELD.zip'
INDEL=DOWNLOADS/'DD_FactionPerfection_Director_Return338_HELD_DELIVERY.json'
RECEIVED=A/'rank9_faction_perfection_return338_received'
PAYLOAD=RECEIVED/'payload'
ARCHIVE=RECEIVED/INZIP.name
DELIVERY=RECEIVED/INDEL.name
AUDIT=A/'FACTION_PERFECTION_RETURN338_INDEPENDENT_AUDIT.json'
RECEIPT=A/'FACTION_PERFECTION_RETURN338_RECEIPT.json'
QUEUE=A/'CURRENT_SPELL_QUEUE_338.json'
PENDING=A/'CURRENT25_PENDING_IDENTITY_AUDIT_338.json'
HANDOFF=A/'CURRENT_HANDOFF_338.json'
SNAPSHOT=A/'CURRENT_SPELL_REVIEW_SNAPSHOT_338.md'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CORE=ROOT/'DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
AUTH={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173}
SPELL='faction-perfection';BLOCKER='AFP211-B04';NEXT='corruption-purification';NEXT_BLOCKER='AFP211-B05';GROUP='rank9-alignment-faction-purification5'
checks=[]

def sha(b):return hashlib.sha256(b).hexdigest()
def crc(b):return f'{zlib.crc32(b)&0xffffffff:08x}'
def bind(path):
 b=path.read_bytes();return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def save(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def check(cid,passed,detail):checks.append({'id':cid,'passed':bool(passed),'detail':detail})
def find_id(node,ident):
 if isinstance(node,dict):
  if node.get('id')==ident:return node
  for v in node.values():
   q=find_id(v,ident)
   if q is not None:return q
 elif isinstance(node,list):
  for v in node:
   q=find_id(v,ident)
   if q is not None:return q
 return None

def safe_name(name):
 p=PurePosixPath(name)
 return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name and ':' not in name and not name.startswith('/')

def read_return(name):
 with ZipFile(ARCHIVE) as z:return z.read(name)

def main():
 if not INZIP.is_file() or not INDEL.is_file():raise FileNotFoundError('Primary Return338 ZIP or DELIVERY download is missing.')
 RECEIVED.mkdir(parents=True,exist_ok=True)
 if INZIP.resolve()!=ARCHIVE.resolve():shutil.copyfile(INZIP,ARCHIVE)
 if INDEL.resolve()!=DELIVERY.resolve():shutil.copyfile(INDEL,DELIVERY)
 archive_bytes=ARCHIVE.read_bytes();delivery_bytes=DELIVERY.read_bytes();d=json.loads(delivery_bytes)
 check('delivery-identity',d.get('id')=='FACTION-PERFECTION-DIRECTOR-RETURN338-DELIVERY' and d.get('reviewId')=='Return338','Return338 delivery identity and target review.')
 exp=d.get('archive',{});check('archive-name-size-sha-crc',exp.get('fileName')==ARCHIVE.name and (exp.get('bytes'),exp.get('sha256'),exp.get('crc32'))==(len(archive_bytes),sha(archive_bytes),crc(archive_bytes)),json.dumps({k:exp.get(k) for k in ('bytes','sha256','crc32')}))
 check('one-identity-held',d.get('heldIds')==[SPELL] and d.get('blockerIds')==[BLOCKER] and d.get('acceptedIds')==[] and d.get('appliedIds')==[],'Exact Faction Perfection / AFP211-B04 hold only.')
 authz=d.get('applicationAuthorization',{});check('application-not-authorized',authz=={'authorized':False,'authorizedIds':[],'canonicalMutationAuthorized':False},json.dumps(authz))
 check('authority-unchanged',d.get('authority')==AUTH,json.dumps(d.get('authority')))
 check('next-priority-exact',d.get('nextPendingIdentity')==NEXT and d.get('nextBlockerId')==NEXT_BLOCKER and d.get('nextPendingGroup')==GROUP,'Corruption Purification / AFP211-B05 remains next.')
 seal=d.get('sealVerification',{});sealchecks=seal.get('checks',[]);check('claimed-seal-checks-pass',seal.get('checksFailed')==0 and seal.get('checksPassed')==75 and len(sealchecks)==75 and all(x.get('status')=='PASS' for x in sealchecks),'Director claims 75/75 seal checks pass.')
 with ZipFile(ARCHIVE) as z:
  names=z.namelist();name_set=set(names);bad=[n for n in names if not safe_name(n)]
  check('zip-integrity-and-safe-unique-names',z.testzip() is None and len(names)==len(name_set) and not bad,f'zip integrity; members={len(names)}; unsafe={bad[:3]}')
  external_rows=d.get('members',[]);external_map={x.get('path'):x for x in external_rows};allow=d.get('exactAllowlist',[])
  check('external-roster-and-allowlist',len(external_rows)==len(names)==36 and len(external_map)==len(external_rows) and set(allow)==name_set==set(external_map) and all(safe_name(n) for n in allow),f'external={len(external_rows)} zip={len(names)}')
  ext_bind_ok=True
  for row in external_rows:
   b=z.read(row['path']);ext_bind_ok=ext_bind_ok and (len(b),sha(b),crc(b))==(row.get('bytes'),row.get('sha256'),row.get('crc32'))
  check('external-member-byte-bindings',ext_bind_ok,'Every external delivery size/SHA/CRC matches the exact ZIP member bytes.')
  root_manifest=json.loads(z.read('MEMBER_MANIFEST.json'));root_rows=root_manifest.get('members',[])
  root_ok=root_manifest.get('archiveMemberCount')==len(names) and root_manifest.get('exactPayloadAllowlist')==[n for n in names if n!='MEMBER_MANIFEST.json'] and len(root_rows)==len(names)-1
  for row in root_rows:
   if row.get('path') not in name_set or row.get('path')=='MEMBER_MANIFEST.json':root_ok=False;continue
   b=z.read(row['path']);root_ok=root_ok and (len(b),sha(b),crc(b))==(row.get('bytes'),row.get('sha256'),row.get('crc32'))
  check('internal-payload-manifest',root_ok,'Return338 root manifest exactly binds all nonmanifest payload members.')
  inner=json.loads(z.read('evidence/MEMBER_MANIFEST.json'));inner_rows=inner.get('members',[]);inner_names={x.get('path') for x in inner_rows}
  inner_payload={n[len('evidence/'):]:n for n in names if n.startswith(('evidence/context/','evidence/input/','evidence/sources/'))}
  inner_ok=inner.get('payloadMemberCount')==20 and inner_names==set(inner_payload)
  for row in inner_rows:
   n='evidence/'+row['path']
   if n not in name_set:inner_ok=False;continue
   b=z.read(n);inner_ok=inner_ok and (len(b),sha(b),crc(b))==(row.get('bytes'),row.get('sha256'),row.get('crc32'))
  check('nested-evidence-manifest',inner_ok,'Nested evidence manifest exactly binds all 20 prepared-input/context members.')
  decision=json.loads(z.read('DIRECTOR_DECISION.json'));hold=json.loads(z.read('HOLD_REGISTER.json'));counts=json.loads(z.read('COUNTS.json'));coverage=json.loads(z.read('CASE_COVERAGE.json'));queue_status=json.loads(z.read('QUEUE_STATUS.json'));source_rec=json.loads(z.read('SOURCE_RECONCILIATION.json'));semantic=json.loads(z.read('SEMANTIC_RECONCILIATION.json'));procedure=json.loads(z.read('PROCEDURE_STATUS.json'));qdis=json.loads(z.read('QUESTION_DISPOSITIONS.json'))
  check('director-decision-no-mutation',decision.get('reviewedIds')==[SPELL] and decision.get('heldIds')==[SPELL] and decision.get('acceptedIds')==[] and decision.get('appliedIds')==[] and decision.get('applicationAuthorization')==authz and decision.get('canonicalMutation') is False,'Exact sealed one-target HOLD; no application/canonical mutation.')
  check('decision-hold-contract',len(decision.get('decisions',[]))==1 and decision['decisions'][0].get('id')==SPELL and decision['decisions'][0].get('decision')=='HOLD' and decision['decisions'][0].get('blockerIds')==[BLOCKER],'One decision only: Faction Perfection / AFP211-B04.')
  reqs=hold.get('requirements',[]);reqids=[x.get('id') for x in reqs]
  check('two-exact-open-contracts',hold.get('spellId')==SPELL and hold.get('blockerId')==BLOCKER and hold.get('status')=='OPEN' and reqids==['AFP338-W01','AFP338-W02'] and all(x.get('status')=='OPEN' for x in reqs),'W01 concrete finite benefit; W02 paid maximum-standing plus useful and later interactions.')
  check('question-dispositions-exact',qdis.get('scope')==SPELL and {x.get('id') for x in qdis.get('records',[])}=={'FP9-19','FP9-20','AFP9-27'},'Only the two target questions and one shared integration direction are dispositioned.')
  preserved=coverage.get('preservedComponents',[])
  check('conditional-cases-not-replayed',coverage.get('spellId')==SPELL and {x.get('id') for x in preserved}=={'AFP211-FP-maximum','AFP211-FP-independent-gates'} and all(x.get('currentStatus')=='PRESERVED_NOT_REPLAYED_OR_REAUDITED' and x.get('completePaidSpellWitness') is False and x.get('clockStatus')=='NOT_DEMONSTRATED' for x in preserved) and coverage.get('freshCaseReplays')==0 and coverage.get('freshCaseReaudits')==0 and coverage.get('newIntegratedCases')==0,'Both prior conditional components retained without replay, re-audit or promotion.')
  check('no-complete-witness-or-benefit-interaction',counts.get('completePaidSpellWitnesses')==0 and counts.get('concreteBenefitUseWitnesses')==0 and counts.get('freshForwardOperations')==0 and counts.get('freshInverseOperations')==0 and counts.get('freshClockChecks')==0 and counts.get('newGameRules')==0,'No new cast, benefit-use witness, case execution or rules authored.')
  check('closed-e01-and-comparator-scopes',decision.get('closedEvidenceFinding')=={'id':'AFP211-E01','status':'CLOSED','reopened':False} and counts.get('closedComparatorScopesRetained')==6 and counts.get('comparatorCasesReplayed')==0,'AFP211-E01 stays closed; six comparator scopes retained.')
  check('procedure-stays-nonoperational',procedure.get('id')==SPELL and procedure.get('status')=='SOURCE_BOUND_INCOMPLETE_NOT_OPERATIONAL' and procedure.get('accepted') is False and procedure.get('applied') is False and procedure.get('completeOperationalProcedure') is False and procedure.get('nativeCard',{}).get('operational') is None,'Target native card remains operational:null and unaccepted/unapplied.')
  current_pending=load(A/'CURRENT25_PENDING_IDENTITY_AUDIT_337.json').get('pendingIds',[])
  check('authority-and-queue-next',queue_status.get('authority')==AUTH and set(queue_status.get('pendingIds',[]))==set(current_pending) and queue_status.get('remainingClosureTasks')==25 and queue_status.get('firstReviewTasks')==0 and queue_status.get('nextPendingIdentity')==NEXT and queue_status.get('nextBlockerId')==NEXT_BLOCKER and queue_status.get('canonicalQueueUpdated') is False,'Queue stays 25 pending / zero first-review; next is AFP211-B05.')
  check('source-check-counts',counts.get('sourceDataChecksPassed')==79 and counts.get('sourceDataChecksFailed')==0 and counts.get('semanticPasses')==6 and counts.get('semanticHeldFindings')==2 and semantic.get('result')=='HOLD','Director reports 79 source/data checks and semantic 6 pass / 2 held.')
  check('source-input-packet-binding',source_rec.get('sourcePacket',{}).get('bytes')==PREPZIP.stat().st_size and source_rec.get('sourcePacket',{}).get('sha256')==sha(PREPZIP.read_bytes()) and source_rec.get('sourceDelivery',{}).get('bytes')==PREPDEL.stat().st_size and source_rec.get('sourceDelivery',{}).get('sha256')==sha(PREPDEL.read_bytes()),'Return binds the exact submitted Review338 ZIP and DELIVERY.')
  check('submitted-delivery-as-received',z.read('evidence/REVIEW338_DELIVERY_AS_RECEIVED.json')==PREPDEL.read_bytes(),'Embedded submitted delivery is byte-exact to the pushed source packet.')
  # The embedded input members and current full authority files are checked against their live/pushed counterparts.
  input_map={'context/CURRENT25_PENDING_IDENTITY_AUDIT_337.json':A/'CURRENT25_PENDING_IDENTITY_AUDIT_337.json','context/CURRENT_HANDOFF_337.json':A/'CURRENT_HANDOFF_337.json','context/CURRENT_SPELL_QUEUE_337.json':A/'CURRENT_SPELL_QUEUE_337.json','context/CURRENT_SPELL_REVIEW_SNAPSHOT_337.md':A/'CURRENT_SPELL_REVIEW_SNAPSHOT_337.md'}
  input_ok=all(z.read('evidence/'+name)==path.read_bytes() for name,path in input_map.items())
  for name in ['00_CURRENT_AUTHORITY_337.json','01_CURRENT_FACTION_PERFECTION_CATALOG_ROW.json','02_CURRENT_FACTION_PERFECTION_INDEX_ROW.json','03_CURRENT_CORE_FACTION_PERFECTION_ROW.json','04_RETURN287_TARGET_DECISION_AND_HOLD.json','05_RETURN287_TARGET_SOURCE_PROPOSAL.json','06_RETURN287_TARGET_QUESTION_DISPOSITIONS.json','07_RETURN287_TARGET_CASE_DISPOSITIONS.json','08_RETURN287_PRESERVED_CONDITIONAL_CASES.json','09_CLOSED_COMPARATOR_BOUNDARY.json','10_PRIOR_RETURNS_AND_CURRENT_HOLDS.json','11_CURRENT_SOURCE_RECONCILIATION.json']:
   member='input/'+name;expected=PREP/'packet'/member
   input_ok=input_ok and expected.is_file() and z.read('evidence/'+member)==expected.read_bytes()
 check('prepared-context-and-input-byte-exact',input_ok,'All 16 queue/context and target-history/source input members match pushed Review338 packet bytes.')
 live_source_rows=source_rec.get('embeddedCurrentSourcesVerified',[]);source_ok=len(live_source_rows)==4
 for row in live_source_rows:
  path=ROOT/row['path'];member=row.get('packetMember','');source_ok=source_ok and path.is_file() and (path.read_bytes()==read_return('evidence/'+member)==(PREP/'packet'/member).read_bytes()) and bind(path)['bytes']==row['bytes'] and bind(path)['sha256']==row['sha256'] and bind(path)['crc32']==row['crc32']
 check('four-live-source-bindings',source_ok,'All four reputation/integration sources match local current bytes and submitted packet.')
 full_rows=source_rec.get('fullCurrentFilesVerified',[]);full_ok=len(full_rows)==3
 for row in full_rows:
  path=ROOT/row['path'];full_ok=full_ok and path.is_file() and (path.stat().st_size==row['bytes'] and sha(path.read_bytes())==row['sha256'] and crc(path.read_bytes())==row['crc32'])
 check('three-current-authority-source-bindings',full_ok and source_rec.get('targetExactRowComparisons') is True,'Current full catalog/index/Core size/SHA/CRC and target row comparisons verified.')
 live_catalog=json.loads(CATALOG.read_text(encoding='utf-8'));live_index=json.loads(INDEX.read_text(encoding='utf-8'));live_core=json.loads(CORE.read_text(encoding='utf-8'))
 catrow=json.loads(read_return('evidence/input/01_CURRENT_FACTION_PERFECTION_CATALOG_ROW.json'));idxrow=json.loads(read_return('evidence/input/02_CURRENT_FACTION_PERFECTION_INDEX_ROW.json'));corerow=json.loads(read_return('evidence/input/03_CURRENT_CORE_FACTION_PERFECTION_ROW.json'))
 corerows=[]
 def walk(n):
  if isinstance(n,dict):
   if n.get('name')=='Faction Perfection':corerows.append(n)
   for v in n.values():walk(v)
  elif isinstance(n,list):
   for v in n:walk(v)
 walk(live_core)
 check('target-rows-match-current-live-sources',catrow==find_id(live_catalog,SPELL) and idxrow==find_id(live_index,SPELL) and corerows==[corerow],'Exact catalog, authored-index and Core target rows match current checkout.')
 # Bind each exact submitted input manifest member back to the actual Review338 outer archive.
 with ZipFile(PREPZIP) as pz:
  submitted_manifest=json.loads(pz.read('MEMBER_MANIFEST.json')); submitted={r['path']:r for r in submitted_manifest['members']}
  source_pair_ok=True
  for row in live_source_rows:
   source_pair_ok=source_pair_ok and pz.read(row['packetMember'])==read_return('evidence/sources/'+Path(row['packetMember']).name)
  source_pair_ok=source_pair_ok and all(pz.read(n)==read_return('evidence/'+n) for n in input_map.keys())
 check('original-submission-member-pairs',source_pair_ok,'Return338 evidence source/context members byte-match corresponding submitted ZIP members.')
 if any(not c['passed'] for c in checks):raise RuntimeError('Return338 independent verification failed: '+json.dumps([c for c in checks if not c['passed']],ensure_ascii=False))
 # Extract only verified safe members after all archive and member checks have passed.
 with ZipFile(ARCHIVE) as z:
  for name in sorted(n for n in z.namelist() if n!='MEMBER_MANIFEST.json'):
   dst=PAYLOAD.joinpath(*PurePosixPath(name).parts);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(z.read(name))
 timestamp=datetime.now(timezone.utc).isoformat(timespec='seconds')
 archive_ref=bind(ARCHIVE);delivery_ref=bind(DELIVERY);decision_path=PAYLOAD/'DIRECTOR_DECISION.json';hold_path=PAYLOAD/'HOLD_REGISTER.json'
 audit={'id':'FACTION-PERFECTION-RETURN338-INDEPENDENT-AUDIT','recordedAtUtc':timestamp,'status':'PASS_RETURN338_SEALED_HOLD_AFP211_B04','archive':archive_ref,'delivery':delivery_ref,'archiveMemberCount':len(names),'checks':checks,'checkCount':len(checks),'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'decision':'HOLD','acceptedIds':[],'appliedIds':[],'heldIds':[SPELL],'applicationAuthorizedIds':[],'authority':AUTH,'openContractIds':['AFP338-W01','AFP338-W02'],'closedEvidenceFinding':'AFP211-E01','nextIdentity':NEXT,'nextBlockerIds':[NEXT_BLOCKER],'deliverySelfHashNote':'This receipt independently binds the exact downloaded DELIVERY JSON by size/SHA/CRC and verifies all 36 archive member bindings; the external archive is the decision record.','canonicalFilesChanged':False,'applicationPerformed':False,'incomingDuplicateCopiesIgnored':2}
 save(AUDIT,audit)
 receipt={'id':'FACTION-PERFECTION-RETURN338-RECEIPT','recordedAtUtc':timestamp,'decision':'HOLD','blockerIds':[BLOCKER],'archive':archive_ref,'delivery':delivery_ref,'directorDecision':bind(decision_path),'holdRegister':bind(hold_path),'independentAudit':bind(AUDIT),'acceptedIds':[],'appliedIds':[],'heldIds':[SPELL],'applicationAuthorizedIds':[],'openContractIds':['AFP338-W01','AFP338-W02'],'closedEvidenceFinding':'AFP211-E01','authority':AUTH,'nextIdentity':NEXT,'nextBlockerIds':[NEXT_BLOCKER],'nextGroup':GROUP,'canonicalFilesChanged':False,'applicationPerformed':False}
 save(RECEIPT,receipt)
 # Advance only queue/handoff records. Preserve existing unrelated accepted and held state.
 q=load(A/'CURRENT_SPELL_QUEUE_337.json');p=load(A/'CURRENT25_PENDING_IDENTITY_AUDIT_337.json');h=load(A/'CURRENT_HANDOFF_337.json')
 retained=sorted(set(q.get('separatelyRetainedHolds',[]))|{SPELL})
 decision_ref=bind(decision_path);audit_ref=bind(AUDIT);receipt_ref=bind(RECEIPT)
 qpath=QUEUE;ppath=PENDING;hpath=HANDOFF
 q.update({'id':'SPELL-REVIEW-QUEUE-338','recordedAtUtc':timestamp,'supersedesQueue':bind(A/'CURRENT_SPELL_QUEUE_337.json'),'currentAuthority':AUTH,'pendingCount':25,'acceptedUnapplied':0,'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'nextGroup':GROUP,'next':NEXT,'nextPendingIds':[NEXT],'nextPendingCount':1,'heldThisStep':[SPELL],'separatelyRetainedHolds':retained,'pendingIdentityAudit':ppath.relative_to(ROOT).as_posix(),'currentHandoff':hpath.relative_to(ROOT).as_posix(),'currentPacket':None,'currentPacketStatus':'RETURN338_FACTION_PERFECTION_HELD_CORRUPTION_PURIFICATION_AFP211_B05_NEXT','activeReview':{'spellId':NEXT,'blockerIds':[NEXT_BLOCKER],'packet':None,'status':'DIRECTOR_RETURN338_NEXT_PRIORITY'},'currentReturn':receipt_ref,'currentReturnReceipt':receipt_ref,'currentReturnArchive':archive_ref,'currentReturnDelivery':delivery_ref,'currentReturnAudit':audit_ref,'currentReturnDecision':decision_ref,'currentReturnAcceptedIds':[],'currentReturnAppliedIds':[],'currentReturnHeldIds':[SPELL],'currentReturnBlockers':{**q.get('currentReturnBlockers',{}),SPELL:[BLOCKER]},'currentDirectorInstruction':'Return338 holds Faction Perfection / AFP211-B04. AFP338-W01 concrete significant benefit/finite entitlement and W02 a paid maximum-standing effect plus useful initial/later benefit interactions remain open. Maximum +3 semantics and independent permissions are established; AFP211-E01 stays closed. The two prior conditional components remain unreplayed. Next Director priority: Corruption Purification / AFP211-B05. Application is not authorized.','directorConnectionStatus':'Return338 independently verified. Faction Perfection remains held; next is Corruption Purification / AFP211-B05.','applicationPerformed':False,'canonicalFilesChanged':False,'githubChanges':False})
 save(QUEUE,q)
 p.update({'id':'SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-338','recordedAtUtc':timestamp,'status':'PASS_CURRENT_823_25_RETURN338_FACTION_PERFECTION_HOLD_CORRUPTION_PURIFICATION_NEXT','supersedes':(A/'CURRENT25_PENDING_IDENTITY_AUDIT_337.json').name,'authority':AUTH,'pendingCount':25,'acceptedIds':[],'appliedIds':[],'heldThisStep':[SPELL],'separatelyHeldIds':retained,'nextGroup':GROUP,'nextIdentity':NEXT,'nextBlockerIds':[NEXT_BLOCKER],'nextPendingIds':[NEXT],'nextPendingCount':1,'nextStep':'Review Corruption Purification / AFP211-B05 using current authority and exact current sources. Preserve AFP211-E01 closed and all earlier holds; apply only an exact sealed acceptance.','sourceQueue':QUEUE.relative_to(ROOT).as_posix(),'currentQueueBinding':bind(QUEUE),'currentReturn':receipt_ref,'currentReturnDelivery':delivery_ref,'currentReturnAudit':audit_ref,'currentReturnReceipt':receipt_ref,'noPendingTargetSilentlyAccepted':True,'allCurrentPendingIdentitiesReviewed':True,'unreviewedPendingIds':[],'canonicalFilesChanged':False,'applicationPerformed':False})
 save(PENDING,p)
 h.update({'id':'CURRENT-HANDOFF-338','recordedAtUtc':timestamp,'supersedes':(A/'CURRENT_HANDOFF_337.json').name,'status':'RETURN338_VERIFIED_FACTION_PERFECTION_HELD_CORRUPTION_PURIFICATION_NEXT_823_25_0','authority':AUTH,'queue':QUEUE.relative_to(ROOT).as_posix(),'queueBinding':bind(QUEUE),'pendingIdentityAudit':PENDING.name,'pendingIdentityAuditBinding':bind(PENDING),'currentDirectorReturn':receipt_ref,'currentReturnReceipt':receipt_ref,'currentReturnAudit':audit_ref,'currentReturnArchive':archive_ref,'currentReturnDelivery':delivery_ref,'heldThisStep':[SPELL],'separatelyRetainedHolds':retained,'acceptedIds':[],'appliedIds':[],'applicationPerformed':False,'canonicalFilesChanged':False,'currentBlocker':{'identity':NEXT,'blockerId':NEXT_BLOCKER,'group':GROUP},'nextPendingGroup':{'group':GROUP,'pendingIds':[NEXT],'pendingCount':1,'reportedByDirector':True},'nextStep':'Review Corruption Purification / AFP211-B05; preserve all prior holds and AFP211-E01 closed; apply only an exact sealed acceptance.','directorConnectionStatus':'Return338 sealed Faction Perfection HOLD; the Director designates Corruption Purification / AFP211-B05 as next.'})
 save(HANDOFF,h)
 SNAPSHOT.write_text('# Spell review status — queue 338\n\nReturn338 holds Faction Perfection / AFP211-B04. Independent verification passed '+str(len(checks))+'/'+str(len(checks))+' checks. Authority remains **823 applied, 25 pending, 0 accepted-unapplied** (547 complete standalone procedures; 173 scoped interfaces).\n\nThe Director established maximum standing at +3 and kept independent membership/invocation gates separate. The current sources still lack a concrete significant benefit with a provider, eligibility, terms, availability and finite entitlement, and a full paid maximum-standing plus initial/later benefit-use witness. AFP211-E01 stays closed; both earlier conditional components were preserved without replay or re-audit. No canonical files changed and no application was authorized.\n\nNext Director-prioritized identity: **Corruption Purification / AFP211-B05**.\n',encoding='utf-8',newline='\n')
 print(json.dumps({'status':'PASS','checks':len(checks),'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'archiveMembers':len(names),'held':SPELL,'pending':25,'next':NEXT,'receipt':str(RECEIPT),'deliveryBytes':len(delivery_bytes),'deliverySha256':sha(delivery_bytes)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
