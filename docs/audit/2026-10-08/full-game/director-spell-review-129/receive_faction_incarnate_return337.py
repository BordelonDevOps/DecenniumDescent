#!/usr/bin/env python3
"""Independently verify Return337 and advance tracking without canonical edits."""
from __future__ import annotations
import hashlib,json,shutil,zlib
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
from zipfile import ZipFile

A=Path(__file__).resolve().parent; ROOT=A.parents[4]
RECEIVED=A/'rank9_faction_incarnate_return337_received'; ARCHIVE=RECEIVED/'DD_FactionIncarnate_Director_Return337_HELD.zip'; DELIVERY=RECEIVED/'DD_FactionIncarnate_Director_Return337_HELD_DELIVERY.json'; PAYLOAD=RECEIVED/'payload'
DOWNLOADS=Path(r'C:\Users\cbord\Downloads')
PREP=A/'rank9_faction_incarnate_review_337_prepared_v2'; PREP_ARCHIVE=PREP/'DD_Rank9_FactionIncarnate_Review337.zip'; PREP_DELIVERY=PREP/'DD_Rank9_FactionIncarnate_Review337_DELIVERY.json'
QUEUE_IN=A/'CURRENT_SPELL_QUEUE_336.json'; PENDING_IN=A/'CURRENT25_PENDING_IDENTITY_AUDIT_336.json'; HANDOFF_IN=A/'CURRENT_HANDOFF_336.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'; INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'; CORE=ROOT/'DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
AUTH={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173}
SPELL='faction-incarnate'; BLOCKER='AFP211-B03'; NEXT='faction-perfection'; NEXT_BLOCKER='AFP211-B04'; GROUP='rank9-alignment-faction-purification5'

def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b)&0xffffffff:08x}'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def bind(p):
 b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
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

def main():
 RECEIVED.mkdir(parents=True,exist_ok=True)
 for name in (ARCHIVE.name,DELIVERY.name):
  src=DOWNLOADS/name; dst=RECEIVED/name
  if not src.is_file(): raise RuntimeError(f'Missing downloaded Director file: {src}')
  if dst.exists() and dst.read_bytes()!=src.read_bytes(): raise RuntimeError(f'Conflicting existing received file: {dst}')
  if not dst.exists(): shutil.copy2(src,dst)
 d=load(DELIVERY); archive_bytes=ARCHIVE.read_bytes(); delivery_bytes=DELIVERY.read_bytes(); checks=[]
 def check(i,ok,detail): checks.append({'id':i,'passed':bool(ok),'detail':detail})
 check('delivery-identity',d.get('id')=='FACTION-INCARNATE-DIRECTOR-RETURN337-DELIVERY' and d.get('reviewId')=='Return337',str(d.get('id')))
 a=d.get('archive',{}); check('archive-name-size-sha-crc',a.get('fileName')==ARCHIVE.name and a.get('bytes')==len(archive_bytes)==772372 and a.get('sha256')==sha(archive_bytes)=='240676d59192588617a75ce2186da474d42f6386d2d43286df66963a23c09beb' and a.get('crc32','').lower()==crc(archive_bytes)=='4d31fc8b',json.dumps({'bytes':len(archive_bytes),'sha256':sha(archive_bytes),'crc32':crc(archive_bytes)}))
 check('scope-exact-one-held-identity',d.get('heldIds')==[SPELL] and d.get('blockerIds')==[BLOCKER] and d.get('acceptedIds')==[] and d.get('appliedIds')==[],str(d.get('heldIds')))
 check('application-not-authorized',d.get('applicationAuthorization')=={'authorized':False,'authorizedIds':[],'canonicalMutationAuthorized':False},json.dumps(d.get('applicationAuthorization')))
 check('authority-unchanged',d.get('authority')==AUTH, json.dumps(d.get('authority')))
 check('next-priority-exact',d.get('nextPendingIdentity')==NEXT and d.get('nextBlockerId')==NEXT_BLOCKER and d.get('nextPendingGroup')==GROUP, json.dumps({'identity':d.get('nextPendingIdentity'),'blocker':d.get('nextBlockerId'),'group':d.get('nextPendingGroup')}))
 check('seal-claims-pass',d.get('sealVerification',{}).get('checksPassed')==89 and d.get('sealVerification',{}).get('checksFailed')==0 and len(d.get('sealVerification',{}).get('checks',[]))==89 and all(x.get('status')=='PASS' for x in d.get('sealVerification',{}).get('checks',[])), 'Director claims 89/89 seal checks pass.')
 names=[]; member_rows=[]; safe=True
 with ZipFile(ARCHIVE) as z:
  names=z.namelist(); bad=z.testzip()
  for n in names:
   pp=PurePosixPath(n)
   if pp.is_absolute() or '..' in pp.parts or '\\' in n or not n: safe=False
   b=z.read(n); member_rows.append({'path':n,'bytes':len(b),'sha256':sha(b),'crc32':crc(b)})
  check('zip-integrity-and-safe-unique-names',bad is None and safe and len(names)==len(set(names)),f'crc={bad}; members={len(names)}; safe={safe}')
  ext={x['path']:x for x in d.get('members',[])}; actual={x['path']:x for x in member_rows}
  allow=set(d.get('exactAllowlist',[]))
  ext_ok=set(ext)==set(actual)==allow and len(names)==d.get('archiveMemberCount')==43 and d.get('payloadMemberCount')==42 and len(ext)==43
  for n,row in ext.items():
   got=actual.get(n,{})
   ext_ok=ext_ok and all(got.get(k)==row.get(k) for k in ('bytes','sha256','crc32'))
  check('external-member-roster-and-bindings',ext_ok,f'external={len(ext)} zip={len(names)}')
  inner=json.loads(z.read('MEMBER_MANIFEST.json')); im={x['path']:x for x in inner.get('members',[])}; payload_names=set(names)-{'MEMBER_MANIFEST.json'}
  inner_ok=inner.get('payloadMemberCount')==42 and len(im)==42 and set(im)==payload_names
  for n,row in im.items():
   got=actual.get(n,{})
   inner_ok=inner_ok and all(got.get(k)==row.get(k) for k in ('bytes','sha256','crc32'))
  check('internal-manifest-exact-payload',inner_ok,f'inner={len(im)} payload={len(payload_names)}')
  if not safe or bad or not ext_ok or not inner_ok: raise RuntimeError('Unsafe, corrupt, or unbound Return337 archive; extraction refused.')
  if PAYLOAD.exists() and any(PAYLOAD.iterdir()):
   for n in names:
    p=PAYLOAD.joinpath(*PurePosixPath(n).parts)
    if not p.is_file() or p.read_bytes()!=z.read(n): raise RuntimeError(f'Existing extraction mismatch: {n}')
  else:
   PAYLOAD.mkdir(parents=True,exist_ok=True)
   for n in names:
    p=PAYLOAD.joinpath(*PurePosixPath(n).parts); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(z.read(n))
 dec=load(PAYLOAD/'DIRECTOR_DECISION.json'); counts=load(PAYLOAD/'COUNTS.json'); hold=load(PAYLOAD/'HOLD_REGISTER.json'); valid=load(PAYLOAD/'VALIDATION.json'); coverage=load(PAYLOAD/'CASE_COVERAGE.json'); boundary=load(PAYLOAD/'BOUNDARY_RECONCILIATION.json'); queue_status=load(PAYLOAD/'QUEUE_STATUS.json'); src_rec=load(PAYLOAD/'SOURCE_RECONCILIATION.json'); proc=load(PAYLOAD/'PROCEDURE_STATUS.json'); sem=load(PAYLOAD/'SEMANTIC_RECONCILIATION.json'); quals=load(PAYLOAD/'QUALIFICATIONS.json')
 check('director-decision-and-no-mutation',dec.get('reviewedIds')==[SPELL] and dec.get('acceptedIds')==[] and dec.get('appliedIds')==[] and dec.get('heldIds')==[SPELL] and dec.get('authorityBefore')==AUTH==dec.get('authorityAfter') and dec.get('applicationAuthorization')=={'authorized':False,'authorizedIds':[],'canonicalMutationAuthorized':False} and dec.get('canonicalMutation') is False, 'Exact one-identity HOLD; authority unchanged; no canonical mutation/application.')
 reqs=hold.get('requirements',[]); reqmap={x.get('id'):x for x in reqs}
 check('three-open-spell-contracts',set(reqmap)=={'AFP337-W01','AFP337-W02','AFP337-W03'} and all(x.get('parentBlocker')==BLOCKER and x.get('status')=='OPEN' for x in reqs),json.dumps(sorted(reqmap)))
 check('question-allocation', {k:v.get('questions') for k,v in reqmap.items()}=={'AFP337-W01':['FI9-14','FI9-16'],'AFP337-W02':['FI9-13'],'AFP337-W03':['FI9-15','FI9-17']},'Five prior question identities assigned to three open contracts.')
 check('source-validation-102',valid.get('status')=='PASS' and valid.get('checkCount')==102 and valid.get('passed')==102 and valid.get('failed')==0 and counts.get('sourceDataChecksPassed')==102 and counts.get('sourceDataChecksFailed')==0,'102/102 source/data checks pass.')
 check('semantic-disposition-six-pass-three-held',sem.get('result')=='HOLD' and sem.get('passed')==6 and sem.get('held')==3 and counts.get('semanticChecks')==9 and counts.get('semanticPasses')==6 and counts.get('semanticHeldFindings')==3 and {x.get('requirementId') for x in sem.get('checks',[]) if x.get('status')=='HELD'}==set(reqmap),'Six pass; exactly three remaining contract findings.')
 case_rows=coverage.get('preservedComponents',[])
 check('prior-two-fi-components-preserved-without-replay',{x.get('id') for x in case_rows}=={'AFP211-FI-profile','AFP211-FI-admission'} and all(x.get('currentStatus')=='PRESERVED_NOT_REPLAYED_OR_REAUDITED' and x.get('completePaidSpellWitness') is False and x.get('clockStatus')=='NOT_DEMONSTRATED' for x in case_rows) and coverage.get('freshReplayCases')==0 and coverage.get('freshForwardOperations')==0 and coverage.get('freshInverseOperations')==0 and coverage.get('freshClockChecks')==0 and coverage.get('newIntegratedCases')==0 and coverage.get('completePaidPositiveEncounters')==0 and coverage.get('requiredPaidPositiveEncounters')==2, 'Prior traces retained; no replay; two paid positive encounters absent.')
 check('closed-shared-evidence-finding',boundary.get('closedEvidenceFinding')=={'id':'AFP211-E01','status':'CLOSED','reopened':False} and boundary.get('comparatorCasesReplayed')==0 and boundary.get('comparatorAcceptanceReopened')==0 and all(x.get('casesReplayed') is False and x.get('acceptanceReopened') is False and x.get('transferToIncarnate') is False for x in boundary.get('exactComparatorBindings',[])), 'AFP211-E01 remains closed; comparator cases and permission transfers excluded.')
 check('comparator-boundary-exact-three', {x.get('id') for x in boundary.get('exactComparatorBindings',[])}=={'faction-paragon','faction-aegis','faction-citadel'} and all(x.get('exactCurrentComparisonVerified') is True for x in boundary.get('exactComparatorBindings',[])), 'Three exact comparison envelopes verified without reopening acceptance.')
 check('procedure-remains-incomplete',proc.get('status')=='SOURCE_BOUND_INCOMPLETE_NOT_OPERATIONAL' and proc.get('accepted') is False and proc.get('applied') is False and proc.get('nativeCard',{}).get('operational') is None,'No operational procedure accepted or applied.')
 check('qualification-set-retained',len(quals.get('qualificationIds',[]))==7 and set(quals.get('qualificationIds',[]))=={f'AFP231-Q0{i}' for i in range(1,8)},'Seven prior qualifications retained.')
 check('queue-status-next-priority',queue_status.get('authority')==AUTH and SPELL in queue_status.get('pendingIds',[]) and queue_status.get('nextPendingIdentity')==NEXT and queue_status.get('nextBlockerId')==NEXT_BLOCKER and queue_status.get('nextPendingGroup')==GROUP and queue_status.get('remainingClosureTasks')==25 and queue_status.get('firstReviewTasks')==0,'Queue remains 25 pending; Faction Perfection is next.')
 current_full_rows=src_rec.get('fullCurrentSourceFilesVerified',[]); current_full_ok=len(current_full_rows)==3 and all((ROOT/x['path']).is_file() and all(bind(ROOT/x['path'])[k]==x[k] for k in ('path','bytes','sha256','crc32')) for x in current_full_rows)
 check('return337-source-reconciliation',src_rec.get('targetExactRowComparisons') is True and len(src_rec.get('tenEmbeddedSourceBindingsVerified',[]))==10 and len(current_full_rows)==3 and current_full_ok and src_rec.get('historical130RowComparison','').startswith('Supplied historical comparison reports only the authored index changed.') and 'not all130' in src_rec.get('historical130RowComparison',''),'Current full catalog/index/Core bindings verified; exact target rows and historical comparison scope preserved.')
 check('delivery-self-hash-disclosure',d.get('deliverySelfHash')=='Excluded to avoid circularity; digest in separate SEAL_RESULT.json.', 'Manifest self-hash explicitly external; local receipt records independently computed delivery SHA-256.')
 # Reconcile all packet contents against the exact locally prepared input packet and live current files.
 prepzip=PREP_ARCHIVE.read_bytes(); prepdel=PREP_DELIVERY.read_bytes(); prepmeta=load(PREP_DELIVERY)
 check('review337-source-archive-binding',d.get('sourcePacket',{}).get('bytes')==len(prepzip) and d.get('sourcePacket',{}).get('sha256')==sha(prepzip) and d.get('sourcePacket',{}).get('crc32','').lower()==crc(prepzip),json.dumps(d.get('sourcePacket',{})))
 check('review337-source-delivery-binding',d.get('sourceDelivery',{}).get('bytes')==len(prepdel) and d.get('sourceDelivery',{}).get('sha256')==sha(prepdel) and d.get('sourceDelivery',{}).get('crc32','').lower()==crc(prepdel),'Input delivery matches pushed Review337 delivery.')
 with ZipFile(PREP_ARCHIVE) as pz, ZipFile(ARCHIVE) as rz:
  pair=[('00_CURRENT_AUTHORITY_336.json','input/00_CURRENT_AUTHORITY_336.json'),('01_CURRENT_FACTION_INCARNATE_CATALOG_ROW.json','input/01_CURRENT_FACTION_INCARNATE_CATALOG_ROW.json'),('02_CURRENT_FACTION_INCARNATE_INDEX_ROW.json','input/02_CURRENT_FACTION_INCARNATE_INDEX_ROW.json'),('03_CURRENT_CORE_FACTION_INCARNATE_ROW.json','input/03_CURRENT_CORE_FACTION_INCARNATE_ROW.json'),('04_RETURN287_TARGET_DECISION_AND_HOLD.json','input/04_RETURN287_TARGET_DECISION_AND_HOLD.json'),('05_RETURN287_TARGET_SOURCE_PROPOSAL.json','input/05_RETURN287_TARGET_SOURCE_PROPOSAL.json'),('06_RETURN287_TARGET_QUESTION_DISPOSITIONS.json','input/06_RETURN287_TARGET_QUESTION_DISPOSITIONS.json'),('07_RETURN287_TARGET_CASE_DISPOSITIONS.json','input/07_RETURN287_TARGET_CASE_DISPOSITIONS.json'),('08_RETURN287_PRESERVED_CONDITIONAL_CASES.json','input/08_RETURN287_PRESERVED_CONDITIONAL_CASES.json'),('09_FACTION_COMPARATOR_BOUNDARIES.json','input/09_FACTION_COMPARATOR_BOUNDARIES.json'),('10_RETURN336_CURRENT_GROUP_CONTEXT.json','input/10_RETURN336_CURRENT_GROUP_CONTEXT.json'),('11_CURRENT_SOURCE_RECONCILIATION.json','input/11_CURRENT_SOURCE_RECONCILIATION.json'),('MEMBER_MANIFEST.json','input/MEMBER_MANIFEST.json'),('REQUEST_337.md','input/REQUEST_337.md')]
  pair_ok=all(pz.read(x)==rz.read(y) for x,y in pair)
  ctx=['CURRENT25_PENDING_IDENTITY_AUDIT_336.json','CURRENT_HANDOFF_336.json','CURRENT_SPELL_QUEUE_336.json','CURRENT_SPELL_REVIEW_SNAPSHOT_336.md']
  pair_ok=pair_ok and all(pz.read('context/'+n)==rz.read('input/context/'+n) for n in ctx)
  pair_ok=pair_ok and rz.read('input/REVIEW337_DELIVERY_AS_RECEIVED.json')==prepdel
  source_rows=prepmeta.get('sourceSetBindings',[])
  source_ok=len(source_rows)==10
  for s in source_rows:
   pm=s.get('packetMember',''); base=Path(pm).name
   source_ok=source_ok and pz.read(pm)==rz.read('input/'+pm) and (ROOT/s['path']).read_bytes()==pz.read(pm) and len(pz.read(pm))==s['bytes'] and sha(pz.read(pm))==s['sha256'] and crc(pz.read(pm))==s['crc32']
  check('all-prior-inputs-and-context-byte-exact',pair_ok,'Target history, question/case records, queue336 and request bind to submitted Review337 source packet.')
  check('ten-live-source-files-byte-exact',source_ok,'All 10 embedded current source files match Review337 ZIP and local source bytes.')
 # Check the submitted exact target catalog/index/core row extracts against live sources.
 cat=load(CATALOG); idx=load(INDEX); core=load(CORE); target=load(PAYLOAD/'input/01_CURRENT_FACTION_INCARNATE_CATALOG_ROW.json'); ix=load(PAYLOAD/'input/02_CURRENT_FACTION_INCARNATE_INDEX_ROW.json'); core_target=load(PAYLOAD/'input/03_CURRENT_CORE_FACTION_INCARNATE_ROW.json')
 live_cat=find_id(cat,SPELL); live_ix=find_id(idx,SPELL); core_rows=[]
 def walk(v):
  if isinstance(v,dict):
   if v.get('name')=='Faction Incarnate':core_rows.append(v)
   for q in v.values():walk(q)
  elif isinstance(v,list):
   for q in v:walk(q)
 walk(core)
 check('target-catalog-index-core-current',target==live_cat and ix==live_ix and core_rows==[core_target] and target.get('operational') is None and ix.get('authoredStatus')=='pending-authored-procedure','Exact live current rows remain pending and unchanged.')
 # Verify current 336 queue context from embedded source packet bytes.
 q336=load(QUEUE_IN); p336=load(PENDING_IN); h336=load(HANDOFF_IN)
 check('current-authority-source-bindings',q336.get('currentAuthority')==AUTH and p336.get('authority')==AUTH and h336.get('authority')==AUTH and q336.get('next')==SPELL and q336.get('activeReview',{}).get('blockerIds')==[BLOCKER],'Current local queue336 names the returned target at 823/25/0.')
 if any(not x['passed'] for x in checks): raise RuntimeError('Return337 independent verification failed: '+json.dumps([x for x in checks if not x['passed']],ensure_ascii=False))
 recorded=datetime.now(timezone.utc).isoformat(timespec='seconds'); archive_ref=bind(ARCHIVE); delivery_ref=bind(DELIVERY)
 decision_path=PAYLOAD/'DIRECTOR_DECISION.json'; hold_path=PAYLOAD/'HOLD_REGISTER.json'; audit_path=A/'FACTION_INCARNATE_RETURN337_INDEPENDENT_AUDIT.json'; receipt_path=A/'FACTION_INCARNATE_RETURN337_RECEIPT.json'
 audit={'id':'FACTION-INCARNATE-RETURN337-INDEPENDENT-AUDIT','recordedAtUtc':recorded,'status':'PASS_RETURN337_SEALED_HOLD_AFP211_B03','archive':archive_ref,'delivery':delivery_ref,'archiveMemberCount':len(member_rows),'checks':checks,'checkCount':len(checks),'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'decision':'HOLD','acceptedIds':[],'appliedIds':[],'heldIds':[SPELL],'applicationAuthorizedIds':[],'authority':AUTH,'openContractIds':['AFP337-W01','AFP337-W02','AFP337-W03'],'closedEvidenceFinding':'AFP211-E01','nextIdentity':NEXT,'nextBlockerIds':[NEXT_BLOCKER],'deliverySelfHashNote':'The received manifest says its own digest is in a separate SEAL_RESULT.json, but no such member or separate download was provided. This audit independently binds the exact downloaded delivery JSON bytes by size/SHA/CRC.','canonicalFilesChanged':False,'applicationPerformed':False}
 save(audit_path,audit)
 receipt={'id':'FACTION-INCARNATE-RETURN337-RECEIPT','recordedAtUtc':recorded,'decision':'HOLD','blockerIds':[BLOCKER],'archive':archive_ref,'delivery':delivery_ref,'directorDecision':bind(decision_path),'holdRegister':bind(hold_path),'independentAudit':bind(audit_path),'acceptedIds':[],'appliedIds':[],'heldIds':[SPELL],'applicationAuthorizedIds':[],'openContractIds':['AFP337-W01','AFP337-W02','AFP337-W03'],'closedEvidenceFinding':'AFP211-E01','authority':AUTH,'nextIdentity':NEXT,'nextBlockerIds':[NEXT_BLOCKER],'nextGroup':GROUP,'canonicalFilesChanged':False,'applicationPerformed':False}
 save(receipt_path,receipt)
 # Advance only queue/handoff/audit records; the canonical catalog/index/Core remain untouched.
 queue=load(QUEUE_IN); pending=load(PENDING_IN); handoff=load(HANDOFF_IN); held=set(queue.get('separatelyRetainedHolds',[])); held.add(SPELL); held=sorted(held)
 next_group=GROUP; qpath=A/'CURRENT_SPELL_QUEUE_337.json'; ppath=A/'CURRENT25_PENDING_IDENTITY_AUDIT_337.json'; hpath=A/'CURRENT_HANDOFF_337.json'; snap=A/'CURRENT_SPELL_REVIEW_SNAPSHOT_337.md'
 decision_ref=bind(decision_path); audit_ref=bind(audit_path); receipt_ref=bind(receipt_path)
 queue.update({'id':'SPELL-REVIEW-QUEUE-337','recordedAtUtc':recorded,'supersedesQueue':bind(QUEUE_IN),'currentAuthority':AUTH,'pendingCount':25,'acceptedUnapplied':0,'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'nextGroup':next_group,'next':NEXT,'nextPendingIds':[NEXT],'nextPendingCount':1,'heldThisStep':[SPELL],'separatelyRetainedHolds':held,'pendingIdentityAudit':ppath.relative_to(ROOT).as_posix(),'currentHandoff':hpath.relative_to(ROOT).as_posix(),'currentPacket':None,'currentPacketStatus':'RETURN337_FACTION_INCARNATE_HELD_FACTION_PERFECTION_AFP211_B04_NEXT','activeReview':{'spellId':NEXT,'blockerIds':[NEXT_BLOCKER],'packet':None,'status':'DIRECTOR_RETURN337_NEXT_PRIORITY'},'currentReturn':receipt_ref,'currentReturnReceipt':receipt_ref,'currentReturnArchive':archive_ref,'currentReturnDelivery':delivery_ref,'currentReturnAudit':audit_ref,'currentReturnDecision':decision_ref,'currentReturnAcceptedIds':[],'currentReturnAppliedIds':[],'currentReturnHeldIds':[SPELL],'currentReturnBlockers':{**queue.get('currentReturnBlockers',{}),SPELL:[BLOCKER]},'currentDirectorInstruction':'Return337 holds Faction Incarnate / AFP211-B03. AFP337-W01 manifestation/useful faction output, W02 invocation/faction/caster relationship, and W03 profile-specific lifecycle plus two paid useful encounters remain open. Shared companion scheduling is established but does not supply Incarnate powers or permissions. AFP211-E01 stays closed; both prior conditional traces were preserved without replay. Next Director priority: Faction Perfection / AFP211-B04. Apply only an exact sealed acceptance.','directorConnectionStatus':'Return337 independently verified. Faction Incarnate remains held; next is Faction Perfection / AFP211-B04.','applicationPerformed':False,'canonicalFilesChanged':False,'githubChanges':False})
 save(qpath,queue)
 pending.update({'id':'SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-337','recordedAtUtc':recorded,'status':'PASS_CURRENT_823_25_RETURN337_FACTION_INCARNATE_HOLD_FACTION_PERFECTION_NEXT','supersedes':PENDING_IN.name,'authority':AUTH,'pendingCount':25,'acceptedIds':[],'appliedIds':[],'heldThisStep':[SPELL],'separatelyHeldIds':held,'nextGroup':next_group,'nextIdentity':NEXT,'nextBlockerIds':[NEXT_BLOCKER],'nextPendingIds':[NEXT],'nextPendingCount':1,'nextStep':'Review Faction Perfection / AFP211-B04 using current authority and sources. Preserve AFP211-B01/B02 holds, AFP211-B03 W01-W03 and closed AFP211-E01; apply only an exact sealed acceptance.','sourceQueue':qpath.relative_to(ROOT).as_posix(),'currentQueueBinding':bind(qpath),'currentReturn':receipt_ref,'currentReturnDelivery':delivery_ref,'currentReturnAudit':audit_ref,'currentReturnReceipt':receipt_ref,'noPendingTargetSilentlyAccepted':True,'allCurrentPendingIdentitiesReviewed':True,'unreviewedPendingIds':[],'canonicalFilesChanged':False,'applicationPerformed':False})
 save(ppath,pending)
 handoff.update({'id':'CURRENT-HANDOFF-337','recordedAtUtc':recorded,'supersedes':HANDOFF_IN.name,'status':'RETURN337_VERIFIED_FACTION_INCARNATE_HELD_FACTION_PERFECTION_NEXT_823_25_0','authority':AUTH,'queue':qpath.relative_to(ROOT).as_posix(),'queueBinding':bind(qpath),'pendingIdentityAudit':ppath.name,'pendingIdentityAuditBinding':bind(ppath),'currentDirectorReturn':receipt_ref,'currentReturnReceipt':receipt_ref,'currentReturnAudit':audit_ref,'currentReturnArchive':archive_ref,'currentReturnDelivery':delivery_ref,'heldThisStep':[SPELL],'separatelyRetainedHolds':held,'acceptedIds':[],'appliedIds':[],'applicationPerformed':False,'canonicalFilesChanged':False,'currentBlocker':{'identity':NEXT,'blockerId':NEXT_BLOCKER,'group':next_group},'nextPendingGroup':{'group':next_group,'pendingIds':[NEXT],'pendingCount':1,'reportedByDirector':True},'nextStep':'Review Faction Perfection / AFP211-B04. Preserve Faction Incarnate AFP337-W01-W03 and AFP211-E01 closed; apply only an exact sealed acceptance.','directorConnectionStatus':'Return337 sealed Faction Incarnate HOLD; the Director designates Faction Perfection / AFP211-B04 as next.'})
 save(hpath,handoff)
 snap.write_text('# Spell review status — queue 337\n\nReturn337 holds Faction Incarnate / AFP211-B03. Independent verification passed '+str(len(checks))+'/'+str(len(checks))+' checks. Authority remains **823 applied, 25 pending, 0 accepted-unapplied** (547 complete standalone procedures; 173 scoped interfaces).\n\nThe Director confirmed shared companion scheduling but found the Incarnate-specific useful manifestation, explicit invocation/faction/caster relationship, and complete recipient lifecycle plus two paid useful encounters remain open. AFP211-E01 stays closed; both earlier conditional components were preserved without replay or re-audit. No canonical files changed and no application was authorized.\n\nNext Director-prioritized identity: **Faction Perfection / AFP211-B04**.\n',encoding='utf-8',newline='\n')
 print(json.dumps({'status':'PASS','checks':len(checks),'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'archiveMembers':len(member_rows),'held':SPELL,'pending':25,'next':NEXT,'receipt':str(receipt_path),'deliveryBytes':len(delivery_bytes),'deliverySha256':sha(delivery_bytes)},ensure_ascii=False,indent=2))
if __name__=='__main__': main()