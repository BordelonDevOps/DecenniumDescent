from __future__ import annotations
import hashlib, json, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED=AUDIT/'rank9_alignmentfactionpurification5_return287_received'
ARCHIVE=RECEIVED/'DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip'
DELIVERY=RECEIVED/'DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD_DELIVERY.json'
SOURCE_DIR=AUDIT/'rank9_alignmentfactionpurification5_current_source_287_prepared'
SOURCE_PACKET=SOURCE_DIR/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287.zip'
SOURCE_DELIVERY=SOURCE_DIR/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287_DELIVERY.json'
PACKET=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287.json'
PACKET_SUBMISSION=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_SUBMISSION.json'
PACKET_AUDIT=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_INDEPENDENT_AUDIT.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_287.json'
HANDOFF=AUDIT/'CURRENT_HANDOFF_287.json'
PENDING=AUDIT/'CURRENT32_PENDING_IDENTITY_AUDIT_287.json'
REPORT=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_RETURN287_INDEPENDENT_AUDIT.json'
RECEIPT=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_RETURN287_RECEIPT.json'
AUTH={'reviewedApplied':816,'pending':32,'acceptedUnapplied':0,'completeStandaloneProcedures':540,'scopedInterfaces':173}
TARGETS=['alignment-ascension','alignment-perfection','faction-incarnate','faction-perfection','corruption-purification']
BLOCKERS={'alignment-ascension':['AFP211-B01'],'alignment-perfection':['AFP211-B02'],'faction-incarnate':['AFP211-B03'],'faction-perfection':['AFP211-B04'],'corruption-purification':['AFP211-B05']}
NEXT={'group':'rank9-projection-confinement2','pendingIds':['astral-projection','imprisonment']}

def digest(raw:bytes): return (len(raw),hashlib.sha256(raw).hexdigest(),f'{zlib.crc32(raw)&0xffffffff:08x}')
def path_digest(p:Path): return digest(p.read_bytes())
def member_digest(z:zipfile.ZipFile,n:str): return digest(z.read(n))
def readj(p:Path): return json.loads(p.read_text(encoding='utf-8-sig'))
def readm(z:zipfile.ZipFile,n:str): return json.loads(z.read(n).decode('utf-8-sig'))
def add(checks,name,passed,detail=None): checks.append({'check':name,'passed':bool(passed),'detail':detail})
def safe_member(n):
 p=PurePosixPath(n)
 return bool(n) and '\\' not in n and not p.is_absolute() and all(x not in ('','.','..') for x in p.parts)
def main():
 checks=[]
 d=readj(DELIVERY); packet=readj(PACKET); submission=readj(PACKET_SUBMISSION); packet_audit=readj(PACKET_AUDIT); source_delivery=readj(SOURCE_DELIVERY)
 zip_raw=ARCHIVE.read_bytes(); delivery_raw=DELIVERY.read_bytes(); zip_size,zip_sha,zip_crc=digest(zip_raw); del_size,del_sha,del_crc=digest(delivery_raw)
 add(checks,'Return287 ZIP size/SHA/CRC match DELIVERY and the Director-reported seal',(zip_size,zip_sha,zip_crc)==(d['archive']['bytes'],d['archive']['sha256'],d['archive']['crc32'].lower())==(2453374,'f46b0bd2216274667aa8909721adabb4b819e491e28f9835d90cf0c0f6edf96e','9e5da252'),{'bytes':zip_size,'sha256':zip_sha,'crc32':zip_crc})
 add(checks,'Downloaded DELIVERY size/SHA/CRC match the Director-reported seal',(del_size,del_sha,del_crc)==(86150,'37ae35c3cda02bc6a6be32f761f6c964ff16e0a18ccfc1ff62abaa892a8b90b7','215de892'),{'bytes':del_size,'sha256':del_sha,'crc32':del_crc})
 add(checks,'Current Packet287 independent audit and submission both bind the reviewed source archive',packet_audit['status']=='PASS' and packet_audit['checkCount']==16 and packet['archive']['sha256']==d['sourcePacketSHA256']==submission['archive']['sha256'] and submission['auditStatus']=='PASS' and packet['sourceAuthority']==AUTH,{'packetAudit':packet_audit['status'],'checks':packet_audit['checkCount'],'sourcePacketSha256':d['sourcePacketSHA256']})
 add(checks,'Sealed decision authority is unchanged and no spell is accepted or applied',d['authority']==AUTH and d['acceptedIds']==[] and d['appliedIds']==[] and d['heldIds']==TARGETS and d['canonicalChanges'] is False and d['runtimeExecuted'] is False,{'authority':d['authority'],'acceptedIds':d['acceptedIds'],'appliedIds':d['appliedIds'],'heldIds':d['heldIds']})
 with zipfile.ZipFile(ARCHIVE) as z, zipfile.ZipFile(SOURCE_PACKET) as source:
  names=z.namelist(); unsafe=[n for n in names if not safe_member(n)]
  add(checks,'Return ZIP has 110 unique safe members and passes CRC integrity',len(names)==len(set(names))==d['zipMemberCount']==110 and not unsafe and z.testzip() is None,{'members':len(names),'unsafe':unsafe[:5]})
  ext_rows={x['path']:x for x in d['members']}; man=readm(z,'MEMBER_MANIFEST.json'); int_rows={x['path']:x for x in man['members']}; payload=set(names)-{'MEMBER_MANIFEST.json'}
  add(checks,'External DELIVERY roster and internal manifest cover the exact ZIP members',len(ext_rows)==110 and set(ext_rows)==set(names) and len(int_rows)==d['payloadMemberCount']==man['payloadMemberCount']==109 and set(int_rows)==payload and d['memberManifest']['path']=='MEMBER_MANIFEST.json' and member_digest(z,'MEMBER_MANIFEST.json')==(d['memberManifest']['bytes'],d['memberManifest']['sha256'],d['memberManifest']['crc32'].lower()),{'externalMembers':len(ext_rows),'payloadMembers':len(int_rows)})
  bad_ext=[n for n,row in ext_rows.items() if member_digest(z,n)!=(row['bytes'],row['sha256'],row['crc32'].lower())]
  bad_int=[n for n,row in int_rows.items() if member_digest(z,n)!=(row['bytes'],row['sha256'],row['crc32'].lower())]
  add(checks,'All member sizes/SHA/CRC independently match both manifests',not bad_ext and not bad_int,{'externalFailures':bad_ext[:8],'internalFailures':bad_int[:8],'checked':len(int_rows)})
  decision=readm(z,'DIRECTOR_DECISION.json'); counts=readm(z,'COUNTS.json'); current=readm(z,'CURRENT_AUTHORITY.json'); hold=readm(z,'HOLD_REGISTER.json')
  decisions=decision['decisions']; by_id={x['id']:x for x in decisions}
  add(checks,'Director decision covers exactly the five submitted identities as holds under AFP211-B01..B05',set(by_id)==set(TARGETS) and decision['heldIds']==TARGETS and decision['acceptedIds']==[] and decision['appliedIds']==[] and all(by_id[s]['decision']=='HOLD' and by_id[s]['held'] is True and by_id[s]['accepted'] is False and by_id[s]['applied'] is False and by_id[s]['blockerIds']==BLOCKERS[s] for s in TARGETS) and {x['id']:x['blockerIds'] for x in decisions}==BLOCKERS,{'decisions':{s:by_id[s]['blockerIds'] for s in TARGETS}})
  hold_rows={x['id']:x for x in hold['identityBlockers']}
  add(checks,'Hold register binds each exact identity to its blocker and missing witness',set(hold_rows)==set(sum((v for v in BLOCKERS.values()),[])) and all(hold_rows[BLOCKERS[s][0]]['spellIds']==[s] and hold_rows[BLOCKERS[s][0]]['decision']=='hold' for s in TARGETS),{'blockers':sorted(hold_rows)})
  add(checks,'Before/after authority and current-authority payload match 816/32/0',decision['authorityBefore']==decision['authorityAfter']==current['authority']==d['authority']==AUTH and current['acceptedIds']==[] and current['appliedIds']==[] and current['heldIds']==TARGETS,{'counts':counts})
  questions=readm(z,'ORIGINAL_QUESTIONS.json'); qdisp=readm(z,'QUESTION_DISPOSITIONS.json'); futures=readm(z,'ORIGINAL_FUTURE_REQUIREMENTS.json'); fdisp=readm(z,'FUTURE_CASE_DISPOSITIONS.json')
  qids={x.get('id') for x in questions}; qdids={x.get('id') for x in qdisp}
  future_texts=set(futures); disposed_future_texts={x.get('originalRequirement') for x in fdisp}
  add(checks,'All 28 original questions and seven future requirements are preserved and dispositioned exactly once',len(questions)==len(qdisp)==counts['originalQuestions']==counts['selectedQuestionDispositions']==28 and qids==qdids and len(future_texts)==len(fdisp)==counts['futureRequirements']==counts['futureDispositions']==7 and future_texts==disposed_future_texts,{'questions':len(questions),'futureRequirements':len(futures)})
  src_rows=readm(z,'SOURCE_BINDINGS.json');
  source_names=source.namelist(); candidate=readm(source,'CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json'); catalog=readm(source,'sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'); catrows={x['id']:x for x in catalog['spells']}
  source_by_path={x['path']:x for x in candidate['sourceBindings']}; mismatches=[]
  if len(src_rows)!=130 or set(source_by_path)!={x['path'] for x in src_rows}: mismatches.append('source path set')
  for row in src_rows:
   name='sources_current/'+row['path']
   if name not in source_names: mismatches.append(name); continue
   if member_digest(source,name)[:2]!=(row['bytes'],row['sha256']): mismatches.append(name+' packet hash')
   raw=source.read(name); gitsha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
   if row.get('gitBlobSHA1') and gitsha!=row['gitBlobSHA1']: mismatches.append(name+' git blob')
   if row['path'] in source_by_path and (row['bytes'],row['sha256'])!=(source_by_path[row['path']]['bytes'],source_by_path[row['path']]['sha256']): mismatches.append(name+' candidate binding')
  for row in src_rows:
   p=ROOT/row['path']
   if not p.exists() or path_digest(p)[:2]!=(row['bytes'],row['sha256']): mismatches.append(row['path']+' live tree')
  add(checks,'All 130 Return source bindings match the independently audited Packet287 and live source tree',len(src_rows)==130 and not mismatches,{'bindings':len(src_rows),'mismatches':mismatches[:12]})
  native=readm(z,'NATIVE_CARDS.json'); nrows={x['id']:x for x in native}
  add(checks,'All five returned native cards match current catalog cards and preserve 19 access rows',set(nrows)==set(TARGETS) and all(nrows[s]==catrows[s] for s in TARGETS) and counts['nativePlacements']==6 and counts['classAccessRows']==19,{'cards':len(nrows),'nativePlacements':counts['nativePlacements'],'classAccessRows':counts['classAccessRows']})
  comparator=readm(z,'COMPARATOR_VERIFICATION.json'); cmpids={x.get('id') for x in comparator['comparators']}
  add(checks,'AFP211-E01 remains closed using the six exact comparator envelopes',comparator['id']=='AFP211-E01' and comparator['status']=='CLOSED' and comparator['reopened'] is False and len(comparator['comparators'])==counts['verifiedComparatorEnvelopes']==6 and cmpids=={'alignment-avatar','alignment-immunity','corruption-immunity','faction-aegis','faction-citadel','faction-paragon'} and d['closedEvidenceFindings']==['AFP211-E01'],{'comparators':sorted(cmpids),'closed':d['closedEvidenceFindings']})
  replay=readm(z,'REPLAY_RESULTS.json'); cases=replay['cases'];
  add(checks,'All ten component traces pass with exact 10 events and 20 forward/inverse operations',len(cases)==counts['componentCases']==10 and all(x['passed'] is True and x['completeSpellWitness'] is False and x['completeActorClockWitness'] is False for x in cases) and sum(x['events'] for x in cases)==counts['events']==10 and sum(x['forwardOperations'] for x in cases)==counts['forwardOperations']==20 and sum(x['inverseOperations'] for x in cases)==counts['inverseOperations']==20 and counts['fullReverseTraversals']==10,{'cases':len(cases),'events':counts['events'],'forward':counts['forwardOperations'],'inverse':counts['inverseOperations']})
  add(checks,'No complete spell or actor-clock positive witness is claimed',counts['completeOperationalProcedures']==0 and counts['completePositiveSpellCases']==0 and counts['completeActorClockCases']==0 and all(not x['completeSpellWitness'] and not x['completeActorClockWitness'] for x in cases),{'completeProcedures':counts['completeOperationalProcedures'],'completeSpellCases':counts['completePositiveSpellCases'],'completeActorClockCases':counts['completeActorClockCases']})
  next_group=readm(z,'NEXT_PENDING_GROUP.json'); queue_embedded=readm(z,'context/CURRENT_SPELL_QUEUE_287.json');
  next_rows=queue_embedded.get('currentPendingGroups',[]); next_row=next((x for x in next_rows if x.get('group')==NEXT['group']),None)
  add(checks,'Next Projection/Confinement2 group is the exact still-pending queue row',next_group['group']==NEXT['group'] and next_group['pendingIds']==NEXT['pendingIds'] and next_row is not None and next_row['pendingIds']==NEXT['pendingIds'] and next_row['pendingCount']==2 and next_group['reviewStarted'] is False and d['nextPendingGroup']==next_group,{'next':next_group})
  sem=readm(z,'validation/SEMANTIC_CHECKS.json'); arts=readm(z,'validation/ARTIFACT_CHECKS.json'); corr=readm(z,'validation/VALIDATOR_CORRECTION.json')
  add(checks,'All returned package checks, 32 artifact checks and 72 semantic checks pass; validator correction is documented',len(d['packageChecks'])==d['packageCheckCount']==447 and all(x['passed'] is True for x in d['packageChecks']) and len(arts)==d['artifactCheckCount']==32 and all(x['passed'] is True for x in arts) and len(sem)==counts['scopedSemanticChecks']==72 and all(x['passed'] is True for x in sem) and corr.get('correction','').startswith('Compare exact current card against prior card field') and len(corr.get('initialFailedChecks',[]))==5,{'packageChecks':len(d['packageChecks']),'artifactChecks':len(arts),'semanticChecks':len(sem),'correction':corr.get('correctedComparisonsPass')})
  ebind=readm(z,'EXTERNAL_BINDINGS.json'); external=d['externalArchives']; external_paths={
    'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287.zip':SOURCE_PACKET,
    'DD_Rank9_AlignmentFactionPurification5_Director_Return248_HELD.zip':AUDIT/'rank9_alignmentfactionpurification5_return248_received/DD_Rank9_AlignmentFactionPurification5_Director_Return248_HELD.zip',
    'DD_Rank9_AlignmentFactionPurification5_Comparator_Supplement_211.zip':AUDIT/'rank9_alignment_faction_purification5_comparator_supplement_211/DD_Rank9_AlignmentFactionPurification5_Comparator_Supplement_211.zip'}
  external_bad=[]
  for row in external:
   p=external_paths.get(row['filename'])
   if p is None or not p.exists() or path_digest(p)!=(row['bytes'],row['sha256'],row['crc32'].lower()): external_bad.append(row['filename'])
  add(checks,'All three external source, prior-return and comparator archives match their exact bound bytes',len(external)==3 and not external_bad and len(ebind['archives'])==3,{'externalArchives':len(external),'failures':external_bad})
  prior_packet_delivery=readj(SOURCE_DELIVERY)
  previous={
   'Return286':('evidence/RETURN286_DELIVERY.json',['reverse-gravity-field'],{'reverse-gravity-field':['IE204-B02']}),
   'Return285':('evidence/RETURN285_DELIVERY.json',['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'],{'summon-elemental-avatar':['SH202-B01'],'summon-herald-of-the-planes':['SH202-B02'],'summon-avatar-of-decay':['SH202-B03']}),
   'Return284':('evidence/RETURN284_DELIVERY.json',['banishment-gate','conjure-demiplane-fortress'],{'banishment-gate':['PG200-B03','PG200-B04'],'conjure-demiplane-fortress':['PG200-B06']})}
  prior_ok=[]
  for label,(member,ids,blockers) in previous.items():
   old=readm(source,'evidence/'+member.split('/')[-1])
   prior_ok.append(old['heldIds']==ids and old['blockerIds']==blockers and old['acceptedIds']==[] and old['appliedIds']==[])
  add(checks,'Return284, Return285 and Return286 prior holds remain unchanged outside scope',all(prior_ok),{'checks':prior_ok})
  add(checks,'No canonical edit, application, runtime execution or downstream gate approval occurred',d['canonicalChanges'] is False and d['runtimeExecuted'] is False and decision['canonicalChanges'] is False and current['canonicalChanges'] is False and decision['authorityAfter']==AUTH and all(x['accepted'] is False and x['applied'] is False for x in decisions),{'canonicalChanges':d['canonicalChanges'],'runtimeExecuted':d['runtimeExecuted']})
 failed=[x for x in checks if not x['passed']]
 report={'id':'RANK9ALIGNFACTIONPURIFICATION5_RETURN287_INDEPENDENT_AUDIT','createdAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not failed else 'FAIL','archive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':zip_size,'sha256':zip_sha,'crc32':zip_crc},'deliveryManifest':{'path':DELIVERY.relative_to(ROOT).as_posix(),'bytes':del_size,'sha256':del_sha,'crc32':del_crc},'authority':AUTH,'targetIds':TARGETS,'acceptedIds':d['acceptedIds'],'appliedIds':d['appliedIds'],'heldIds':d['heldIds'],'blockers':BLOCKERS,'nextPendingGroup':d['nextPendingGroup'],'memberCount':len(names),'checkCount':len(checks),'passedChecks':len(checks)-len(failed),'failedChecks':len(failed),'checks':checks}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 receipt={'id':'RANK9ALIGNFACTIONPURIFICATION5_RETURN287_RECEIPT','auditStatus':report['status'],'archive':report['archive'],'deliveryManifest':report['deliveryManifest'],'independentAudit':{'path':REPORT.relative_to(ROOT).as_posix(),'bytes':REPORT.stat().st_size,'sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest()},'authority':AUTH,'acceptedIds':[],'appliedIds':[],'heldIds':TARGETS,'blockerIds':BLOCKERS,'nextPendingGroup':NEXT,'checkCount':len(checks),'failedChecks':len(failed)}
 RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'checkCount':len(checks),'passedChecks':len(checks)-len(failed),'failedChecks':len(failed),'archiveSha256':zip_sha,'deliverySha256':del_sha,'failures':failed},ensure_ascii=False,indent=2))
 if failed: raise SystemExit(1)
if __name__=='__main__': main()
