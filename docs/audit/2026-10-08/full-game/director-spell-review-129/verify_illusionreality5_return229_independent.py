from __future__ import annotations
import hashlib, json, zlib, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED=AUDIT/'rank9_illusionreality5_return229_received'
ARCHIVE=RECEIVED/'DD_Rank9_IllusionReality1_Director_Return229.zip'
DELIVERY=RECEIVED/'DD_Rank9_IllusionReality1_Director_Return229_DELIVERY.json'
SOURCE_PACKET=AUDIT/'rank9_illusionreality5_current_source_229_prepared/DD_Rank9_IllusionReality5_CurrentSource_229.zip'
SOURCE_DELIVERY=AUDIT/'rank9_illusionreality5_current_source_229_prepared/DD_Rank9_IllusionReality5_CurrentSource_229_DELIVERY.json'
PACKET_RECORD=AUDIT/'RANK9ILLUSIONREALITY5_PACKET_229.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_229.json'
REPORT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN229_INDEPENDENT_AUDIT.json'
RECEIPT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN229_RECEIPT.json'
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
TARGET=['soul-reflection']; CLOSED=['supreme-illusion','mirrored-world','ethereal-disjunction','illusory-reality']
NEXT={'group':'rank9-material-forging2','pendingIds':['eternal-forge','matter-conversion']}
def digest(path):
 h=hashlib.sha256(); c=0; n=0
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):
   h.update(b); c=zlib.crc32(b,c); n+=len(b)
 return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def mdigest(z,name):
 h=hashlib.sha256(); c=0; n=0
 with z.open(name) as f:
  for b in iter(lambda:f.read(1024*1024),b''):
   h.update(b); c=zlib.crc32(b,c); n+=len(b)
 return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def readj(z,name): return json.loads(z.read(name).decode('utf-8-sig'))
def add(checks,name,ok,detail=None): checks.append({'check':name,'passed':bool(ok),'detail':detail})
def main():
 checks=[]; d=json.loads(DELIVERY.read_text(encoding='utf-8-sig')); packet=json.loads(PACKET_RECORD.read_text(encoding='utf-8-sig'))
 n,s,c=digest(ARCHIVE); dn,ds,dc=digest(DELIVERY); sn,ss,sc=digest(SOURCE_PACKET); sdn,sds,sdc=digest(SOURCE_DELIVERY)
 add(checks,'Return229 bytes/SHA-256/CRC32 and archive label match delivery',(n,s,c)==(d['archive']['bytes'],d['archive']['sha256'],d['archive']['crc32'].lower()) and d['archive']['path']==ARCHIVE.name,{'bytes':n,'sha256':s,'crc32':c})
 add(checks,'Return229 binds the independently audited packet229 and its delivery manifest',(sn,ss)==(d['sourcePacket']['bytes'],d['sourcePacket']['sha256']) and sc==d['sourcePacket']['crc32'].lower() and packet['archive']['sha256']==ss and sds==packet['deliveryManifest']['sha256'] and sdc==packet['deliveryManifest']['crc32'].lower(),{'sourcePacketBytes':sn,'sourcePacketSha256':ss,'packetRecordSha256':packet['archive']['sha256'],'sourceDeliverySha256':sds})
 with zipfile.ZipFile(ARCHIVE) as z:
  names=z.namelist(); ext={r['path']:r for r in d['members']}; unsafe=[x for x in names if x.startswith(('/','\\')) or '\\' in x or PurePosixPath(x).is_absolute() or '..' in PurePosixPath(x).parts]
  add(checks,'ZIP has exactly 75 unique safe members matching the delivery allowlist',len(names)==len(set(names))==len(ext)==d['exactArchiveMemberCount']==75 and set(names)==set(ext) and not unsafe and z.testzip() is None,{'archiveMembers':len(names),'deliveryMembers':len(ext),'unsafe':unsafe[:8]})
  bad=[]
  for name,row in ext.items():
   if mdigest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()): bad.append(name)
  add(checks,'Every member independently matches delivery size/SHA/CRC',not bad,{'checked':len(ext),'failures':bad[:12]})
  manifest=readj(z,'MANIFEST.json'); ir={x['path']:x for x in manifest['members']}; payload=set(names)-{'MANIFEST.json'}
  add(checks,'Internal manifest and external MANIFEST self-binding agree',set(ir)==payload and len(ir)==d['payloadMemberCountExcludingManifest']==74 and manifest['memberCountExcludingSelf']==74 and ext['MANIFEST.json']['sha256']==d['memberManifest']['sha256'] and mdigest(z,'MANIFEST.json')==(d['memberManifest']['bytes'],d['memberManifest']['sha256'],d['memberManifest']['crc32'].lower()),{'internalRows':len(ir),'payloadMembers':len(payload)})
  bad=[]
  for name,row in ir.items():
   if mdigest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()): bad.append(name)
  add(checks,'Every payload member independently matches the internal manifest',not bad,{'checked':len(ir),'failures':bad[:12]})
  decision=readj(z,'DIRECTOR_DECISION.json'); counts=readj(z,'COUNTS.json'); replay=readj(z,'CASE_REPLAY.json'); dispositions=readj(z,'CASE_DISPOSITIONS.json'); semantic=readj(z,'INDEPENDENT_SEMANTIC_FAILURE_CHECK.json'); hold=readj(z,'HOLD_REGISTER.json'); nxt=readj(z,'NEXT_PENDING_GROUP.json'); reassess=readj(z,'SOURCE_REASSESSMENT.json'); nullreplay=readj(z,'NULL_ACQUISITION_REPLAY.json'); audit_summary=readj(z,'AUDIT_SUMMARY.json'); validation=readj(z,'VALIDATION.json'); sourceverify=readj(z,'SOURCE_VERIFICATION.json')
  add(checks,'Decision is held only for Soul Reflection with unchanged authority and no application',d['id']=='RANK9-ILLUSION-REALITY1-RETURN229-DELIVERY' and d['authority']==AUTH and d['accepted'] is False and d['applied'] is False and d['acceptedIds']==[] and d['appliedIds']==[] and d['heldIds']==TARGET and d['blockerIds']==['IR207-B02'] and decision['scope']==TARGET and decision['authorityBefore']==AUTH and decision['authorityAfter']==AUTH and decision['accepted'] is False and decision['applied'] is False and decision['heldIds']==TARGET,{'authority':d['authority'],'heldIds':d['heldIds'],'blockers':d['blockerIds']})
  identity=decision['perIdentity'][0]; witnesses=identity['minimumMissingWitnesses']; expected_categories=['Changed-form recipient and reversion','Attached and genuinely phase-less recipient','Original target zero/death settlement','Reflection-origin active concentration ending','Entrusted original cargo']
  add(checks,'IR207-B02 ruling retains exactly the five specified minimum witness categories',identity['spellId']=='soul-reflection' and identity['blockerIds']==['IR207-B02'] and len(witnesses)==5 and [x['category'] for x in witnesses]==expected_categories and all(x['blockerId']=='IR207-B02' for x in witnesses) and reassess['minimumWitnesses']==witnesses,{'categories':[x['category'] for x in witnesses]})
  add(checks,'Semantic audit distinguishes passing replay from missing integrated coverage',semantic['status']=='HELD_INCOMPLETE_REQUIRED_WITNESS_COVERAGE' and len(semantic['remainingAcceptanceGateFailures'])==1 and semantic['remainingAcceptanceGateFailures'][0]['id']=='IR207-B02' and semantic['remainingAcceptanceGateFailures'][0]['minimumWitnesses']==[x['id'] for x in witnesses] and all(x['passed'] is True for x in semantic['scopedBoundaryChecks']),{'semanticStatus':semantic['status'],'boundaryChecks':semantic['semanticBoundaryCheckCount']})
  case_rows=replay['cases']; add(checks,'Ten preserved combat cases all replay successfully without promoting full semantic acceptance',replay['summary']['cases']==10 and len(case_rows)==10 and all(x['replayPassed'] is True for x in case_rows) and replay['summary']['failures']==[] and len(dispositions['targetCases'])==10 and sum(x['kind']=='main' and x['fullObligationDisposition']=='TRACE_VALID_BUT_IDENTITY_HELD_INCOMPLETE_COVERAGE' for x in dispositions['targetCases'])==2,{'cases':len(case_rows),'mainObligations':sum(x['kind']=='main' and x['fullObligationDisposition']=='TRACE_VALID_BUT_IDENTITY_HELD_INCOMPLETE_COVERAGE' for x in dispositions['targetCases'])})
  combat=(sum(x['events'] for x in case_rows),sum(x['forwardOperations'] for x in case_rows),sum(x['inverseOperations'] for x in case_rows))
  add(checks,'Combat replay totals reconcile at 331 events and 662 forward/inverse operations',combat==(331,662,662) and (replay['summary']['events'],replay['summary']['forwardOperations'],replay['summary']['inverseOperations'])==(331,662,662) and (counts['combatEvents'],counts['combatForwardOperations'],counts['combatInverseOperations'])==(331,662,662),{'events':combat[0],'forward':combat[1],'inverse':combat[2]})
  add(checks,'Supplemental acquisition and proposal operations reconcile and invert cleanly',nullreplay['events']==2 and nullreplay['forwardOperations']==4 and nullreplay['inverseOperations']==4 and nullreplay['checkCount']==38 and nullreplay['failures']==[] and all(x['passed'] is True for x in nullreplay['checks']) and d['counts']['proposalForwardOperations']==2 and d['counts']['proposalInverseOperations']==2 and replay['summary']['proposalOperations']==4,{'acquisitionEvents':2,'acquisitionForward':4,'acquisitionInverse':4,'proposalForward':2,'proposalInverse':2})
  add(checks,'Source/data/clock and package checks report no failures',replay['summary']['checkCount']+nullreplay['checkCount']==d['counts']['dataSourceClockIntegrityChecks']==16269 and replay['summary']['failures']==[] and nullreplay['failures']==[] and audit_summary['checkCount']==16269 and audit_summary['failures']==[] and d['packageChecks']['count']==d['packageChecks']['passed']==306 and d['packageChecks']['failed']==0 and all(x['passed'] is True for x in d['packageChecks']['checks']) and validation['status']=='REPLAY_AND_SOURCE_INTEGRITY_PASS_ACCEPTANCE_HELD' and validation['failures']==[],{'checks':16269,'packageChecks':d['packageChecks']['count'],'failed':0})
  add(checks,'Both full main obligations remain incomplete and 31 questions/2 addenda/5 future requirements are preserved',counts['incompleteMainObligations']==2 and counts['originalRequiredMainCasesPreserved']==10 and counts['originalQuestionsPreserved']==31 and counts['focusedAddendaPreserved']==2 and counts['futureRequirementsPreserved']==5 and d['counts']==counts,{'incompleteMainObligations':counts['incompleteMainObligations'],'originalCases':counts['originalRequiredMainCasesPreserved'],'questions':counts['originalQuestionsPreserved'],'addenda':counts['focusedAddendaPreserved'],'future':counts['futureRequirementsPreserved']})
  qualification=decision['qualifications']
  add(checks,'Return207 acceptances, Return228 hold and all downstream gates are preserved',decision['closedAppliedIdsPreserved']==CLOSED and decision['Return228OutsideScope']['heldIds']==['reverse-gravity-field'] and decision['Return228OutsideScope']['blockerIds']==['IE204-B02'] and all(qualification.get(k) is False for k in ['applied','canonicalFilesEdited','githubChanged','runtimeApproved','gameExecuted','sourceProgramsExecuted','historicalProgramsExecuted','implementationApproved','humanPlaytested','balanceApproved','cosmologyApproved','domainClosure','completionClaim','releaseApproved']),{'closedAcceptedApplied':decision['closedAppliedIdsPreserved'],'return228':decision['Return228OutsideScope']})
  add(checks,'Next pending group matches both return authority and current queue order',nxt['authority']==AUTH and nxt['nextGroup']==NEXT['group'] and nxt['pendingIds']==NEXT['pendingIds'] and d['nextPendingGroup']==NEXT['group'] and d['nextPendingIds']==NEXT['pendingIds'] and nxt['freshCurrentPacketRequired'] is True and not nxt['reviewOrApplicationPerformedForNextGroup'],{'group':nxt['nextGroup'],'ids':nxt['pendingIds']})
  add(checks,'All 157 current source bindings match the packet229 member bytes and the packet delivery',len(sourceverify['sourceBindings'])==157 and sourceverify['sourcePacket']['sha256']==ss and sourceverify['sourceDelivery']['sha256']==sds,{'sourceBindings':len(sourceverify['sourceBindings'])})
  source_fail=[]
  with zipfile.ZipFile(SOURCE_PACKET) as pz:
   queue_member='current/'+nxt['queueBinding']['path']
   queue_digest=mdigest(pz,queue_member)
   queue_snapshot=readj(pz,queue_member)
   for row in sourceverify['sourceBindings']:
    name='sources_current/sources_current/'+row['path']
    try: actual=mdigest(pz,name)
    except KeyError: source_fail.append(row['path']); continue
    if actual[:2]!=(row['bytes'],row['sha256']): source_fail.append(row['path'])
   prior=d['externalPriorArchiveBinding']; prior_actual=mdigest(pz,prior['packetMember'])
  add(checks,'All source binding hashes and embedded prior Return207 archive hash match packet229',not source_fail and prior_actual==(d['externalPriorArchiveBinding']['bytes'],d['externalPriorArchiveBinding']['sha256'],d['externalPriorArchiveBinding']['crc32'].lower()),{'checked':len(sourceverify['sourceBindings']),'sourceFailures':source_fail[:8],'priorArchive':prior_actual})
  add(checks,'Packet-bound current queue bytes agree with the return queue binding',queue_digest==(nxt['queueBinding']['bytes'],nxt['queueBinding']['sha256'],nxt['queueBinding']['crc32'].lower()),{'queueSha256':queue_digest[1]})
 rows=queue_snapshot['currentPendingGroups']; pos=next(i for i,x in enumerate(rows) if x['group']=='rank9-illusion-reality5'); qnext=rows[pos+1]
 add(checks,'Return names the actual next group in current queue order',qnext['group']==NEXT['group'] and qnext['pendingIds']==NEXT['pendingIds'],{'next':qnext})
 passed=sum(x['passed'] for x in checks)
 report={'id':'RANK9ILLUSIONREALITY5-RETURN229-INDEPENDENT-AUDIT','status':'PASS' if passed==len(checks) else 'FAIL','checkedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':{'path':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':n,'sha256':s,'crc32':c},'delivery':{'path':DELIVERY.relative_to(ROOT).as_posix(),'bytes':dn,'sha256':ds,'crc32':dc},'sourcePacket':{'path':SOURCE_PACKET.relative_to(ROOT).as_posix(),'bytes':sn,'sha256':ss},'authority':d['authority'],'targetIds':TARGET,'acceptedIds':d['acceptedIds'],'appliedIds':d['appliedIds'],'heldIds':d['heldIds'],'blockerIds':d['blockerIds'],'counts':d['counts'],'nextPendingGroup':NEXT,'checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed,'checks':checks}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); rn,rs,rc=digest(REPORT)
 receipt={'id':'RANK9ILLUSIONREALITY5-RETURN229-RECEIPT','status':report['status'],'archive':report['archive'],'delivery':report['delivery'],'independentAudit':{'path':REPORT.relative_to(ROOT).as_posix(),'bytes':rn,'sha256':rs,'crc32':rc},'checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed}
 RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed,'report':str(REPORT),'receipt':str(RECEIPT),'failed':[x for x in checks if not x['passed']]},ensure_ascii=False,indent=2))
 if passed!=len(checks): raise SystemExit(1)
if __name__=='__main__': main()
