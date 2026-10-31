#!/usr/bin/env python3
"""Prepare a current-source, one-identity Faction Perfection review packet."""
from __future__ import annotations
import hashlib, json, shutil, zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

A=Path(__file__).resolve().parent
ROOT=A.parents[4]
OUT=A/'rank9_faction_perfection_review_338_prepared'
PK=OUT/'packet'
ARCHIVE=OUT/'DD_Rank9_FactionPerfection_Review338.zip'
DELIVERY=OUT/'DD_Rank9_FactionPerfection_Review338_DELIVERY.json'
QUEUE=A/'CURRENT_SPELL_QUEUE_337.json'
PENDING=A/'CURRENT25_PENDING_IDENTITY_AUDIT_337.json'
HANDOFF=A/'CURRENT_HANDOFF_337.json'
SNAPSHOT=A/'CURRENT_SPELL_REVIEW_SNAPSHOT_337.md'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CORE=ROOT/'DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
RETURN287=A/'rank9_alignmentfactionpurification5_return287_received/DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip'
RETURN336=A/'rank9_alignment_perfection_return336_received/DD_AlignmentPerfection_Director_Return336_HELD.zip'
RETURN337=A/'rank9_faction_incarnate_return337_received/DD_FactionIncarnate_Director_Return337_HELD.zip'
SPELL='faction-perfection'; BLOCKER='AFP211-B04'; NEXT='corruption-purification'; NEXT_BLOCKER='AFP211-B05'; GROUP='rank9-alignment-faction-purification5'
AUTH={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173}
SOURCES=[
 'DescentReviewChanges/ReviewBible/docs/mechanics/REPUTATION.md',
 'DescentReviewChanges/ReviewBible/src/data/reputation.js',
 'DescentReviewChanges/ReviewBible/src/data/resonance-economy.js',
 'DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md',
]

def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b)&0xffffffff:08x}'
def bind(path):
 b=path.read_bytes(); return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def load(path): return json.loads(path.read_text(encoding='utf-8'))
def save(path,obj): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def find_id(node,ident):
 if isinstance(node,dict):
  if node.get('id')==ident: return node
  for v in node.values():
   got=find_id(v,ident)
   if got is not None:return got
 elif isinstance(node,list):
  for v in node:
   got=find_id(v,ident)
   if got is not None:return got
 return None

def main():
 marker=OUT/'PREPARATION_AUDIT_338.json'
 if OUT.exists() and any(OUT.rglob('*')) and (not marker.exists() or load(marker).get('id')!='FACTION-PERFECTION-REVIEW338-PREPARATION-AUDIT'):
  raise RuntimeError(f'Refusing to overwrite non-owned output: {OUT}')
 PK.mkdir(parents=True,exist_ok=True)
 queue,pending,handoff=load(QUEUE),load(PENDING),load(HANDOFF)
 catalog,index,core=load(CATALOG),load(INDEX),load(CORE)
 spell,index_row=find_id(catalog,SPELL),find_id(index,SPELL)
 core_rows=[]
 def walk(n):
  if isinstance(n,dict):
   if n.get('name')=='Faction Perfection':core_rows.append(n)
   for v in n.values():walk(v)
  elif isinstance(n,list):
   for v in n:walk(v)
 walk(core)
 if spell is None or index_row is None or len(core_rows)!=1: raise RuntimeError('Current Faction Perfection rows incomplete or ambiguous.')
 with ZipFile(RETURN287) as z:
  decision=json.loads(z.read('DIRECTOR_DECISION.json'))
  holdreg=json.loads(z.read('HOLD_REGISTER.json'))
  questions=json.loads(z.read('QUESTION_DISPOSITIONS.json'))
  case_disp=json.loads(z.read('CASE_DISPOSITIONS.json'))
  procedures=json.loads(z.read('PROCEDURES.json'))
  comparator=json.loads(z.read('COMPARATOR_VERIFICATION.json'))
  target_decision=next(x for x in decision['decisions'] if x.get('id')==SPELL)
  target_hold=next(x for x in holdreg['identityBlockers'] if x.get('id')==BLOCKER)
  target_questions=[x for x in questions if x.get('id') in {'FP9-19','FP9-20','AFP9-27'}]
  target_cases=['AFP211-FP-maximum','AFP211-FP-independent-gates']
  cases={x:json.loads(z.read(f'cases/{x}.json')) for x in target_cases}
  target_case_disp=[x for x in case_disp if x.get('id') in target_cases]
  procedure=next(x for x in procedures if x.get('id')==SPELL)
  prior_comparator={'id':comparator.get('id'),'status':comparator.get('status'),'reopened':comparator.get('reopened'),'comparators':[{'id':x.get('id'),'scope':x.get('scope'),'reopened':x.get('reopened')} for x in comparator.get('comparators',[])]}
 prior_record=load(A/'rank9_alignmentfactionpurification5_current_source_287_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json')
 prior_record=next(x for x in prior_record.get('records',[]) if x.get('spellId')==SPELL)
 with ZipFile(RETURN336) as z:
  d336=json.loads(z.read('DIRECTOR_DECISION.json'))
  e01_336=d336.get('closedEvidenceFinding',{})
 with ZipFile(RETURN337) as z:
  d337=json.loads(z.read('DIRECTOR_DECISION.json'))
  e01_337={'id':'AFP211-E01','status':'CLOSED','reopened':False}
 if queue.get('currentAuthority')!=AUTH or queue.get('next')!=SPELL or queue.get('activeReview',{}).get('blockerIds')!=[BLOCKER]: raise RuntimeError('Queue337 does not designate Faction Perfection / AFP211-B04.')
 if target_hold.get('spellIds')!=[SPELL] or target_hold.get('decision')!='hold' or {x.get('id') for x in target_questions}!={'FP9-19','FP9-20','AFP9-27'}: raise RuntimeError('Return287 target hold/question history incomplete.')
 if target_decision.get('accepted') is not False or target_decision.get('applied') is not False: raise RuntimeError('Prior target was not a sealed hold.')
 if len(cases)!=2 or len(target_case_disp)!=2 or any(x.get('completeSpellWitness') is not False for x in target_case_disp): raise RuntimeError('Prior components are not valid bounded traces.')
 if comparator.get('id')!='AFP211-E01' or comparator.get('status')!='CLOSED' or comparator.get('reopened') is not False or len(comparator.get('comparators',[]))!=6: raise RuntimeError('Closed comparator boundary mismatch.')
 source_bindings=[]
 for i,rel in enumerate(SOURCES):
  path=ROOT/rel
  if not path.is_file():raise RuntimeError(f'Missing current source {rel}')
  row=bind(path);row['packetMember']=f'sources/{i:02d}_{path.name}';source_bindings.append(row)
 current={'catalog':bind(CATALOG),'authoredIndex':bind(INDEX),'core':bind(CORE)}
 input_rows={
  '00_CURRENT_AUTHORITY_337.json':{'authority':AUTH,'queue':bind(QUEUE),'pendingAudit':bind(PENDING),'handoff':bind(HANDOFF),'activeReview':queue.get('activeReview'),'separatelyRetainedHolds':queue.get('separatelyRetainedHolds',[])},
  '01_CURRENT_FACTION_PERFECTION_CATALOG_ROW.json':spell,
  '02_CURRENT_FACTION_PERFECTION_INDEX_ROW.json':index_row,
  '03_CURRENT_CORE_FACTION_PERFECTION_ROW.json':core_rows[0],
  '04_RETURN287_TARGET_DECISION_AND_HOLD.json':{'historicalAuthorityOnly':decision.get('authorityBefore'),'targetDecision':target_decision,'identityHold':target_hold,'priorArchiveBinding':bind(RETURN287)},
  '05_RETURN287_TARGET_SOURCE_PROPOSAL.json':{'candidateBinding':bind(A/'rank9_alignmentfactionpurification5_current_source_287_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json'),'targetRecord':prior_record,'incompleteProcedureProposal':procedure},
  '06_RETURN287_TARGET_QUESTION_DISPOSITIONS.json':target_questions,
  '07_RETURN287_TARGET_CASE_DISPOSITIONS.json':target_case_disp,
  '08_RETURN287_PRESERVED_CONDITIONAL_CASES.json':{'caseIds':target_cases,'cases':cases,'dataReplayPreviouslyPassed':True,'completePositiveSpellWitness':False,'completeActorClockWitness':False,'replayedOrReauditedFor338':False},
  '09_CLOSED_COMPARATOR_BOUNDARY.json':prior_comparator,
  '10_PRIOR_RETURNS_AND_CURRENT_HOLDS.json':{'return336':{'archive':bind(RETURN336),'decision':{'heldIds':d336.get('heldIds'),'acceptedIds':d336.get('acceptedIds'),'appliedIds':d336.get('appliedIds'),'closedEvidenceFinding':e01_336}},'return337':{'archive':bind(RETURN337),'decision':{'heldIds':d337.get('heldIds'),'acceptedIds':d337.get('acceptedIds'),'appliedIds':d337.get('appliedIds'),'closedEvidenceFinding':e01_337}},'scope':'Retain prior identity holds and AFP211-E01 closed. No comparator permission, benefits, profile, or other identity decision transfers.'},
  '11_CURRENT_SOURCE_RECONCILIATION.json':{'fullCurrentSourceFilesVerified':[current['catalog'],current['authoredIndex'],current['core']],'targetExactCatalogRowComparedToReturn287':prior_record.get('completeCurrentCatalogSourceAndAccess')==spell,'targetExactIndexRowComparedToReturn287':prior_record.get('currentIndexEntry')==index_row,'sourceSetBindings':source_bindings,'priorSourceHistoricalIndexNote':'Return287 reported one authored-index change among its 130-file historical set. This review independently binds the exact current catalog/index/Core and all four current reputation/integration sources; it does not claim a fresh 130-file comparison.'},
 }
 for n,v in input_rows.items():save(PK/'input'/n,v)
 for i,rel in enumerate(SOURCES):
  src=ROOT/rel; dst=PK/'sources'/f'{i:02d}_{src.name}';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for src in (QUEUE,PENDING,HANDOFF,SNAPSHOT):
  dst=PK/'context'/src.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 request='''# Director review request — Faction Perfection / AFP211-B04

Review only Faction Perfection, one identity, against the exact current source bindings. Current queue337 designates it next at 823 reviewed/applied, 25 pending, 0 accepted-unapplied (547 complete standalone procedures; 173 scoped interfaces). Preserve the exact native promise: one target’s reputation with one actual nominated faction becomes maximized and the target gains significant benefits. The current Core placement is Abjuration rank 9, Action, 120 feet, Instantaneous, V/S/F, 26 RP; catalog access is Cleric/Druid/Mage/Wizard Abjuration, rank 9, minimum class level 17, base 26 RP. Preserve all native fields and do not silently convert the effect into a different global reputation system.

Reassess selected directions FP9-19, FP9-20 and AFP9-27 without treating their selection as acceptance. Use a willing target and one actually identified faction; standing, membership, office, alliance and invocation permission remain independent. Current standing-v1 supplies −3..+3; +2 Honored is not maximum; current reputation/resonance guidance supplies no automatic RP/rank/Dissonance modifier. The current source lists broad benefit categories (prices, access, information, legal treatment, support, etc.) and says a named focus/training/consumable/scene benefit must have explicit written rules. It does not itself specify a concrete provider, benefit, eligibility, availability, terms, quantity, finite entitlement, cost, consumption or later-use behavior. Do not invent one or treat a category as an actual service.

The prior bounded component traces AFP211-FP-maximum and AFP211-FP-independent-gates are preserved byte-exactly as conditional components only; do not replay or relabel them as complete paid spell witnesses. They show no actual paid cast, complete actor-clock history or concrete benefit encounter. A positive review needs a fully source-qualified maximum-standing effect while independent membership/invocation gates remain false, then at least one real concrete benefit interaction and a separate later interaction after actual history/misconduct, showing finite eligibility, cost/consumption, no repeat reward/reset, with complete legal casting/payment and source-clock evidence.

Keep AFP211-E01 CLOSED. The six comparator identities in the attached closure record remain comparison-only; do not reopen them or transfer their benefits, permissions, resources or procedures. Preserve the Return336/337 unrelated holds and exact queue priority. No canonical mutation or application is authorized by this review request. If the bound sources still lack concrete benefit content or a complete positive witness, return a focused sealed one-identity HOLD naming the smallest exact contracts, authority counts and current next pending identity. Only an exact sealed acceptance may be applied.
'''
 (OUT/'REQUEST_338.md').write_text(request,encoding='utf-8',newline='\n')
 payload=[]
 for f in sorted(PK.rglob('*')):
  if f.is_file() and f.name!='MEMBER_MANIFEST.json':
   b=f.read_bytes();payload.append({'path':f.relative_to(PK).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)})
 save(PK/'MEMBER_MANIFEST.json',{'id':'FACTION-PERFECTION-REVIEW338-PAYLOAD-MANIFEST','payloadMemberCount':len(payload),'members':payload})
 members=[]
 for f in [OUT/'REQUEST_338.md',*sorted(PK.rglob('*'))]:
  if f.is_file():
   b=f.read_bytes();name='REQUEST_338.md' if f==OUT/'REQUEST_338.md' else f.relative_to(PK).as_posix();members.append({'path':name,'bytes':len(b),'sha256':sha(b),'crc32':crc(b)})
 with ZipFile(ARCHIVE,'w',ZIP_DEFLATED,compresslevel=9) as z:
  z.write(OUT/'REQUEST_338.md','REQUEST_338.md')
  for f in sorted(PK.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(PK).as_posix())
 ab=ARCHIVE.read_bytes()
 with ZipFile(ARCHIVE) as z:
  if z.testzip() or len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!={r['path'] for r in members}:raise RuntimeError('Archive roster/integrity failed.')
  for r in members:
   b=z.read(r['path'])
   if (len(b),sha(b),crc(b))!=(r['bytes'],r['sha256'],r['crc32']):raise RuntimeError('Archive member binding failed: '+r['path'])
 delivery={'id':'FACTION-PERFECTION-REVIEW338-DELIVERY','reviewId':'Review338','targetIds':[SPELL],'blockerIds':[BLOCKER],'authority':AUTH,'acceptedIds':[],'appliedIds':[],'decisionRequested':'current-source reassessment only; no canonical mutation/application','archive':{'fileName':ARCHIVE.name,'bytes':len(ab),'sha256':sha(ab),'crc32':crc(ab)},'archiveMemberCount':len(members),'members':members,'exactAllowlist':[r['path'] for r in members],'priorReturn287':bind(RETURN287),'currentReturn336':bind(RETURN336),'currentReturn337':bind(RETURN337),'sourceSetBindings':source_bindings,'sourceChecks':{'currentTargetCatalogRowMatchesReturn287':input_rows['11_CURRENT_SOURCE_RECONCILIATION.json']['targetExactCatalogRowComparedToReturn287'],'currentTargetIndexRowMatchesReturn287':input_rows['11_CURRENT_SOURCE_RECONCILIATION.json']['targetExactIndexRowComparedToReturn287'],'priorConditionalCaseReplayOrReaudit':False},'nextIfHeld':'Determine only from current queue and sealed Director decision.'}
 save(DELIVERY,delivery)
 checks=[
  {'id':'current-authority-and-queue-priority','passed':queue.get('currentAuthority')==AUTH and queue.get('next')==SPELL and queue.get('activeReview',{}).get('blockerIds')==[BLOCKER]},
  {'id':'exact-live-catalog-index-core-rows','passed':spell.get('id')==SPELL and index_row.get('id')==SPELL and core_rows[0].get('name')=='Faction Perfection'},
  {'id':'historical-hold-and-selected-directions','passed':target_hold.get('id')==BLOCKER and target_hold.get('spellIds')==[SPELL] and {x.get('id') for x in target_questions}=={'FP9-19','FP9-20','AFP9-27'}},
  {'id':'preserved-component-traces-not-complete-witnesses','passed':len(cases)==len(target_case_disp)==2 and all(x.get('completeSpellWitness') is False for x in target_case_disp)},
  {'id':'closed-comparator-boundary','passed':comparator.get('id')=='AFP211-E01' and comparator.get('status')=='CLOSED' and comparator.get('reopened') is False and len(comparator.get('comparators',[]))==6},
  {'id':'no-prior-target-acceptance-or-application','passed':target_decision.get('accepted') is False and target_decision.get('applied') is False and target_hold.get('accepted') is False and target_hold.get('applied') is False},
  {'id':'current-source-file-bindings','passed':len(source_bindings)==4 and all((ROOT/r['path']).is_file() and bind(ROOT/r['path'])=={k:v for k,v in r.items() if k!='packetMember'} for r in source_bindings)},
  {'id':'archive-members-and-byte-bindings','passed':len(members)==len(ZipFile(ARCHIVE).namelist()) and not ZipFile(ARCHIVE).testzip()},
 ]
 if not all(c['passed'] for c in checks):raise RuntimeError('Preparation audit failed: '+json.dumps(checks))
 save(marker,{'id':'FACTION-PERFECTION-REVIEW338-PREPARATION-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'status':'PASS','checks':checks,'checkCount':len(checks),'passed':sum(c['passed'] for c in checks),'failed':0,'archive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':len(ab),'sha256':sha(ab),'crc32':crc(ab)},'delivery':{'path':DELIVERY.relative_to(ROOT).as_posix(),'bytes':DELIVERY.stat().st_size,'sha256':sha(DELIVERY.read_bytes())},'memberCount':len(members),'authority':AUTH,'target':SPELL,'blocker':BLOCKER,'canonicalMutation':False})
 print(json.dumps({'status':'PASS','checks':len(checks),'archive':str(ARCHIVE),'bytes':len(ab),'sha256':sha(ab),'delivery':str(DELIVERY),'members':len(members),'sourceFiles':len(source_bindings)},indent=2))

if __name__=='__main__':main()
