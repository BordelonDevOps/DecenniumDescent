#!/usr/bin/env python3
"""Prepare a current-source, one-identity Corruption Purification review packet."""
from __future__ import annotations
import hashlib,json,shutil,zlib
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED

A=Path(__file__).resolve().parent
ROOT=A.parents[4]
OUT=A/'rank9_corruption_purification_review_339_prepared'
PK=OUT/'packet'
ARCHIVE=OUT/'DD_Rank9_CorruptionPurification_Review339.zip'
DELIVERY=OUT/'DD_Rank9_CorruptionPurification_Review339_DELIVERY.json'
QUEUE=A/'CURRENT_SPELL_QUEUE_338.json'
PENDING=A/'CURRENT25_PENDING_IDENTITY_AUDIT_338.json'
HANDOFF=A/'CURRENT_HANDOFF_338.json'
SNAPSHOT=A/'CURRENT_SPELL_REVIEW_SNAPSHOT_338.md'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CORE=ROOT/'DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
OLD=A/'rank9_alignmentfactionpurification5_current_source_287_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json'
RETURN287=A/'rank9_alignmentfactionpurification5_return287_received/DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip'
RETURN336=A/'rank9_alignment_perfection_return336_received/DD_AlignmentPerfection_Director_Return336_HELD.zip'
RETURN337=A/'rank9_faction_incarnate_return337_received/DD_FactionIncarnate_Director_Return337_HELD.zip'
RETURN338=A/'rank9_faction_perfection_return338_received/DD_FactionPerfection_Director_Return338_HELD.zip'
SPELL='corruption-purification';BLOCKER='AFP211-B05';GROUP='rank9-alignment-faction-purification5'
AUTH={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173}
SOURCE_PATHS=[
 'DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_RESEARCH_REVIEWED_01.md',
 'DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md',
 'DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md',
 'DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md',
 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank6_reviewed_06.json',
 'DescentReviewChanges/ReviewBible/docs/spells/candidates/ABJURATION_CONJURATION_RANK6_REVIEWED_06.md',
]

def sha(b):return hashlib.sha256(b).hexdigest()
def crc(b):return f'{zlib.crc32(b)&0xffffffff:08x}'
def bind(path):
 b=path.read_bytes();return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def save(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def find_id(node,ident):
 if isinstance(node,dict):
  if node.get('id')==ident:return node
  for v in node.values():
   got=find_id(v,ident)
   if got is not None:return got
 elif isinstance(node,list):
  for v in node:
   got=find_id(v,ident)
   if got is not None:return got
 return None

def main():
 marker=OUT/'PREPARATION_AUDIT_339.json'
 if OUT.exists() and any(OUT.rglob('*')) and (not marker.exists() or load(marker).get('id')!='CORRUPTION-PURIFICATION-REVIEW339-PREPARATION-AUDIT'):
  raise RuntimeError(f'Refusing to overwrite non-owned output: {OUT}')
 PK.mkdir(parents=True,exist_ok=True)
 queue,pending,handoff=load(QUEUE),load(PENDING),load(HANDOFF)
 catalog,index,core=load(CATALOG),load(INDEX),load(CORE)
 spell,index_row=find_id(catalog,SPELL),find_id(index,SPELL)
 core_rows=[]
 def walk(n):
  if isinstance(n,dict):
   if n.get('name')=='Corruption Purification':core_rows.append(n)
   for v in n.values():walk(v)
  elif isinstance(n,list):
   for v in n:walk(v)
 walk(core)
 if spell is None or index_row is None or len(core_rows)!=1:raise RuntimeError('Current Corruption Purification rows incomplete or ambiguous.')
 with ZipFile(RETURN287) as z:
  decision=json.loads(z.read('DIRECTOR_DECISION.json'));holdreg=json.loads(z.read('HOLD_REGISTER.json'));questions=json.loads(z.read('QUESTION_DISPOSITIONS.json'));case_disp=json.loads(z.read('CASE_DISPOSITIONS.json'));procedures=json.loads(z.read('PROCEDURES.json'));comparator=json.loads(z.read('COMPARATOR_VERIFICATION.json'))
  target_decision=next(x for x in decision['decisions'] if x.get('id')==SPELL)
  target_hold=next(x for x in holdreg['identityBlockers'] if x.get('id')==BLOCKER)
  target_qids={'CP9-22','CP9-23','CP9-24','CP9-25','CP9-26','AFP9-27'}
  target_questions=[x for x in questions if x.get('id') in target_qids]
  target_case_ids=['AFP211-CP-ordinary-removal','AFP211-CP-new-exposure']
  cases={x:json.loads(z.read(f'cases/{x}.json')) for x in target_case_ids}
  target_case_disp=[x for x in case_disp if x.get('id') in target_case_ids]
  procedure=next(x for x in procedures if x.get('id')==SPELL)
  comparator_summary={'id':comparator.get('id'),'status':comparator.get('status'),'reopened':comparator.get('reopened'),'comparators':[{'id':x.get('id'),'scope':x.get('scope'),'reopened':x.get('reopened')} for x in comparator.get('comparators',[])]}
 old_doc=load(OLD);old_record=next(x for x in old_doc.get('records',[]) if x.get('spellId')==SPELL)
 with ZipFile(RETURN336) as z:d336=json.loads(z.read('DIRECTOR_DECISION.json'))
 with ZipFile(RETURN337) as z:d337=json.loads(z.read('DIRECTOR_DECISION.json'))
 with ZipFile(RETURN338) as z:d338=json.loads(z.read('DIRECTOR_DECISION.json'))
 if queue.get('currentAuthority')!=AUTH or queue.get('next')!=SPELL or queue.get('activeReview',{}).get('blockerIds')!=[BLOCKER]:raise RuntimeError('Queue338 does not designate Corruption Purification / AFP211-B05.')
 if target_hold.get('spellIds')!=[SPELL] or target_hold.get('decision')!='hold' or {x.get('id') for x in target_questions}!=target_qids:raise RuntimeError('Return287 target hold/question history incomplete.')
 if target_decision.get('accepted') is not False or target_decision.get('applied') is not False:raise RuntimeError('Prior target was not a sealed hold.')
 if len(cases)!=2 or len(target_case_disp)!=2 or any(x.get('completeSpellWitness') is not False for x in target_case_disp):raise RuntimeError('Prior components are not bounded conditional traces.')
 if comparator.get('id')!='AFP211-E01' or comparator.get('status')!='CLOSED' or comparator.get('reopened') is not False or len(comparator.get('comparators',[]))!=6:raise RuntimeError('Closed comparator boundary mismatch.')
 source_bindings=[]
 for i,rel in enumerate(SOURCE_PATHS):
  path=ROOT/rel
  if not path.is_file():raise RuntimeError(f'Missing current relevant source: {rel}')
  row=bind(path);row['packetMember']=f'sources/{i:02d}_{path.name}';source_bindings.append(row)
 catalog_comparators={x:find_id(catalog,x) for x in ['corruption-cleanse','corruption-ward']}
 input_rows={
  '00_CURRENT_AUTHORITY_338.json':{'authority':AUTH,'queue':bind(QUEUE),'pendingAudit':bind(PENDING),'handoff':bind(HANDOFF),'activeReview':queue.get('activeReview'),'separatelyRetainedHolds':queue.get('separatelyRetainedHolds',[])},
  '01_CURRENT_CORRUPTION_PURIFICATION_CATALOG_ROW.json':spell,
  '02_CURRENT_CORRUPTION_PURIFICATION_INDEX_ROW.json':index_row,
  '03_CURRENT_CORE_CORRUPTION_PURIFICATION_ROW.json':core_rows[0],
  '04_RETURN287_TARGET_DECISION_AND_HOLD.json':{'historicalAuthorityOnly':decision.get('authorityBefore'),'targetDecision':target_decision,'identityHold':target_hold,'priorArchiveBinding':bind(RETURN287)},
  '05_RETURN287_TARGET_SOURCE_PROPOSAL.json':{'candidateBinding':bind(OLD),'targetRecord':old_record,'incompleteProcedureProposal':procedure},
  '06_RETURN287_TARGET_QUESTION_DISPOSITIONS.json':target_questions,
  '07_RETURN287_TARGET_CASE_DISPOSITIONS.json':target_case_disp,
  '08_RETURN287_PRESERVED_CONDITIONAL_CASES.json':{'caseIds':target_case_ids,'cases':cases,'dataReplayPreviouslyPassed':True,'completePositiveSpellWitness':False,'completeActorClockWitness':False,'replayedOrReauditedFor339':False},
  '09_CLOSED_COMPARATOR_BOUNDARY.json':comparator_summary,
  '10_PRIOR_RETURNS_AND_CURRENT_HOLDS.json':{'return336':{'archive':bind(RETURN336),'heldIds':d336.get('heldIds'),'closedEvidenceFinding':d336.get('closedEvidenceFinding')},'return337':{'archive':bind(RETURN337),'heldIds':d337.get('heldIds'),'closedEvidenceFinding':{'id':'AFP211-E01','status':'CLOSED','reopened':False}},'return338':{'archive':bind(RETURN338),'heldIds':d338.get('heldIds'),'openContracts':['AFP338-W01','AFP338-W02'],'closedEvidenceFinding':d338.get('closedEvidenceFinding')},'scope':'Prior holds and AFP211-E01 remain closed. Comparator and lower-rank effects are comparison-only; no permissions, cures, geometry or procedures transfer.'},
  '11_CURRENT_SOURCE_RECONCILIATION.json':{'fullCurrentSourceFilesVerified':[bind(CATALOG),bind(INDEX),bind(CORE)],'targetExactCatalogRowComparedToReturn287':old_record.get('completeCurrentCatalogSourceAndAccess')==spell,'targetExactIndexRowComparedToReturn287':old_record.get('currentIndexEntry')==index_row,'sourceSetBindings':source_bindings,'comparisonOnlyRows':catalog_comparators,'sourceInterpretation':'SOULS_RESEARCH_REVIEWED_01.md §8 expressly leaves Purification pending. The exact Corruption Purge/Cleanse, Corruption Ward, Null Veil and Corruption Immunity scopes remain boundaries only; their procedures do not fill the rank9 cure matrix.'},
 }
 for n,v in input_rows.items():save(PK/'input'/n,v)
 for i,rel in enumerate(SOURCE_PATHS):
  src=ROOT/rel;dst=PK/'sources'/f'{i:02d}_{src.name}';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for src in (QUEUE,PENDING,HANDOFF,SNAPSHOT):
  dst=PK/'context'/src.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 request='''# Director review request — Corruption Purification / AFP211-B05

Review only Corruption Purification, one identity. Current queue338 designates it next at 823 reviewed/applied, 25 pending, 0 accepted-unapplied (547 complete standalone procedures; 173 scoped interfaces). Historical Return287 authority 816/32 is not current. Preserve the exact native promise and current source access, including Abjuration rank9, Action, 120 feet, V/S/F, base26RP and the Core duration field Until Dispelled. Do not reduce the native “permanently removes all corruption from an area or creature” promise to a lower-rank Purge, temporary suppression, a few-point reduction or another identity.

Reassess retained directions CP9-22 through CP9-26 and AFP9-27 against the bound current sources. They are directions with mandatory holds, not acceptance. Resolve the exact explicit cure matrix for ordinary Corrupted records, numeric corruption, KT knowledge, PT exposure, symptoms, intrinsic/protected sources and parent/dependent effects; distinguish a cured completed source from genuinely new future exposure. Keep knowledge, memory, history, physical consequences, anatomy, HP and Wounds unchanged unless an exact authorized source says otherwise. Preserve the exact Null Veil purge routes; do not create a fourth purge or erase knowledge.

Retain permanent completed removal as the selected direction and reconcile it expressly with Core Until Dispelled, stating exactly what is or is not still dispellable without adding an ongoing ward or blanket future immunity. Keep separate bounded creature and area modes, willing creature admission and environmental admission, actual hidden occupants, exact occupied area geometry, partial/intersecting or indivisible sources, remote dependencies and persistent cleaned-region provenance. Do not invent a radius, extent, save, permission bypass or new source value. Lower-rank Corruption Cleanse/Purge/Ward and closed Corruption Immunity envelopes are comparison-only and confer no rank9 cure, geometry, protection, duration or permission.

The two prior components AFP211-CP-ordinary-removal and AFP211-CP-new-exposure are preserved as bounded conditional traces only; do not replay, re-audit or promote them to target-spell casts/positive witnesses. Require two complete paid useful witnesses: a real creature cure and a multi-source area cure with exact protected exceptions, dependencies, future exposure and dispel settlement, with source-qualified actors, legal paid casts, full states/clocks and forward/inverse operations. Keep AFP211-E01 CLOSED and preserve the Return336/337/338 holds. No canonical mutation or application is authorized by this review request. If any content or positive witness remains missing, issue a sealed one-identity HOLD with the smallest exact contracts, unchanged authority and next pending identity as determined from the current queue. Attach a sealed ZIP and matching DELIVERY.
'''
 (OUT/'REQUEST_339.md').write_text(request,encoding='utf-8',newline='\n')
 payload=[]
 for f in sorted(PK.rglob('*')):
  if f.is_file() and f.name!='MEMBER_MANIFEST.json':
   b=f.read_bytes();payload.append({'path':f.relative_to(PK).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)})
 save(PK/'MEMBER_MANIFEST.json',{'id':'CORRUPTION-PURIFICATION-REVIEW339-PAYLOAD-MANIFEST','payloadMemberCount':len(payload),'members':payload})
 members=[]
 for f in [OUT/'REQUEST_339.md',*sorted(PK.rglob('*'))]:
  if f.is_file():
   b=f.read_bytes();name='REQUEST_339.md' if f==OUT/'REQUEST_339.md' else f.relative_to(PK).as_posix();members.append({'path':name,'bytes':len(b),'sha256':sha(b),'crc32':crc(b)})
 with ZipFile(ARCHIVE,'w',ZIP_DEFLATED,compresslevel=9) as z:
  z.write(OUT/'REQUEST_339.md','REQUEST_339.md')
  for f in sorted(PK.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(PK).as_posix())
 ab=ARCHIVE.read_bytes()
 with ZipFile(ARCHIVE) as z:
  if z.testzip() or len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!={r['path'] for r in members}:raise RuntimeError('Archive roster/integrity failed.')
  for r in members:
   b=z.read(r['path'])
   if (len(b),sha(b),crc(b))!=(r['bytes'],r['sha256'],r['crc32']):raise RuntimeError('Archive member mismatch: '+r['path'])
 delivery={'id':'CORRUPTION-PURIFICATION-REVIEW339-DELIVERY','reviewId':'Review339','targetIds':[SPELL],'blockerIds':[BLOCKER],'authority':AUTH,'acceptedIds':[],'appliedIds':[],'decisionRequested':'current-source reassessment only; no canonical mutation/application','archive':{'fileName':ARCHIVE.name,'bytes':len(ab),'sha256':sha(ab),'crc32':crc(ab)},'archiveMemberCount':len(members),'members':members,'exactAllowlist':[r['path'] for r in members],'priorReturn287':bind(RETURN287),'currentReturn336':bind(RETURN336),'currentReturn337':bind(RETURN337),'currentReturn338':bind(RETURN338),'sourceSetBindings':source_bindings,'sourceChecks':{'currentTargetCatalogRowMatchesReturn287':input_rows['11_CURRENT_SOURCE_RECONCILIATION.json']['targetExactCatalogRowComparedToReturn287'],'currentTargetIndexRowMatchesReturn287':input_rows['11_CURRENT_SOURCE_RECONCILIATION.json']['targetExactIndexRowComparedToReturn287'],'priorConditionalCaseReplayOrReaudit':False},'nextIfHeld':'Determine only from current queue and sealed Director decision.'}
 save(DELIVERY,delivery)
 checks=[
  {'id':'current-authority-and-queue-priority','passed':queue.get('currentAuthority')==AUTH and queue.get('next')==SPELL and queue.get('activeReview',{}).get('blockerIds')==[BLOCKER]},
  {'id':'exact-live-catalog-index-core-rows','passed':spell.get('id')==SPELL and index_row.get('id')==SPELL and core_rows[0].get('name')=='Corruption Purification'},
  {'id':'prior-hold-and-selected-directions','passed':target_hold.get('id')==BLOCKER and target_hold.get('spellIds')==[SPELL] and {x.get('id') for x in target_questions}==target_qids},
  {'id':'preserved-components-not-complete-witnesses','passed':len(cases)==len(target_case_disp)==2 and all(x.get('completeSpellWitness') is False for x in target_case_disp)},
  {'id':'closed-comparator-boundary','passed':comparator.get('id')=='AFP211-E01' and comparator.get('status')=='CLOSED' and comparator.get('reopened') is False and len(comparator.get('comparators',[]))==6},
  {'id':'no-prior-target-acceptance-or-application','passed':target_decision.get('accepted') is False and target_decision.get('applied') is False and target_hold.get('accepted') is False and target_hold.get('applied') is False},
  {'id':'all-current-source-bindings','passed':len(source_bindings)==len(SOURCE_PATHS) and all((ROOT/r['path']).is_file() and bind(ROOT/r['path'])=={k:v for k,v in r.items() if k!='packetMember'} for r in source_bindings)},
  {'id':'archive-and-manifest-integrity','passed':len(members)==len(ZipFile(ARCHIVE).namelist()) and ZipFile(ARCHIVE).testzip() is None},
 ]
 if not all(c['passed'] for c in checks):raise RuntimeError('Preparation audit failed: '+json.dumps(checks))
 save(marker,{'id':'CORRUPTION-PURIFICATION-REVIEW339-PREPARATION-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'status':'PASS','checks':checks,'checkCount':len(checks),'passed':sum(c['passed'] for c in checks),'failed':0,'archive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':len(ab),'sha256':sha(ab),'crc32':crc(ab)},'delivery':{'path':DELIVERY.relative_to(ROOT).as_posix(),'bytes':DELIVERY.stat().st_size,'sha256':sha(DELIVERY.read_bytes())},'memberCount':len(members),'authority':AUTH,'target':SPELL,'blocker':BLOCKER,'canonicalMutation':False})
 print(json.dumps({'status':'PASS','checks':len(checks),'archive':str(ARCHIVE),'bytes':len(ab),'sha256':sha(ab),'delivery':str(DELIVERY),'members':len(members),'sourceFiles':len(source_bindings)},indent=2))

if __name__=='__main__':main()
