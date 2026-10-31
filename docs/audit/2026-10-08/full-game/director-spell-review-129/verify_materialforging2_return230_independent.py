from __future__ import annotations
import hashlib, json, zlib, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED=AUDIT/'rank9_materialforging2_return230_received'
ARCHIVE=RECEIVED/'DD_Rank9_MaterialForging2_Director_Return230.zip'
DELIVERY=RECEIVED/'DD_Rank9_MaterialForging2_Director_Return230_DELIVERY.json'
SOURCE_PACKET=AUDIT/'rank9_materialforging2_current_source_230_prepared/DD_Rank9_MaterialForging2_CurrentSource_230.zip'
SOURCE_DELIVERY=AUDIT/'rank9_materialforging2_current_source_230_prepared/DD_Rank9_MaterialForging2_CurrentSource_230_DELIVERY.json'
PACKET_RECORD=AUDIT/'RANK9MATERIALFORGING2_PACKET_230_SUBMISSION.json'
PRIOR210=RECEIVED.parent/'rank9_materialforging2_return210_received/DD_Rank9_MaterialForging2_Director_Return210.zip'
PRIOR229=RECEIVED.parent/'rank9_illusionreality5_return229_received/DD_Rank9_IllusionReality1_Director_Return229.zip'
REPORT=AUDIT/'RANK9MATERIALFORGING2_RETURN230_INDEPENDENT_AUDIT.json'
RECEIPT=AUDIT/'RANK9MATERIALFORGING2_RETURN230_RECEIPT.json'
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
TARGET=['eternal-forge','matter-conversion']
NEXT={'group':'rank9-alignment-faction-purification5','pendingIds':['alignment-ascension','alignment-perfection','faction-incarnate','faction-perfection','corruption-purification']}

def digest(path):
    h=hashlib.sha256(); c=0; n=0
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b); c=zlib.crc32(b,c); n+=len(b)
    return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def member_digest(z,name):
    h=hashlib.sha256(); c=0; n=0
    with z.open(name) as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b); c=zlib.crc32(b,c); n+=len(b)
    return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def readj(z,name): return json.loads(z.read(name).decode('utf-8-sig'))
def read_path(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def add(checks,name,ok,detail=None): checks.append({'check':name,'passed':bool(ok),'detail':detail})
def main():
    checks=[]
    d=read_path(DELIVERY); packet=read_path(PACKET_RECORD); source_d=read_path(SOURCE_DELIVERY)
    n,s,c=digest(ARCHIVE); dn,ds,dc=digest(DELIVERY)
    add(checks,'Return230 archive bytes/SHA/CRC and filename match DELIVERY',(n,s,c)==(d['archive']['bytes'],d['archive']['sha256'],d['archive']['crc32'].lower()) and d['archive']['filename']==ARCHIVE.name,{'bytes':n,'sha256':s,'crc32':c})
    add(checks,'Downloaded DELIVERY file is valid JSON and retains expected authority',d['id']=='DD-MATERIAL-FORGING2-DIRECTOR-RETURN230-DELIVERY' and d['authority']==AUTH,{'deliveryBytes':dn,'deliverySha256':ds,'authority':d['authority']})
    sn,ss,sc=digest(SOURCE_PACKET); sdn,sds,sdc=digest(SOURCE_DELIVERY)
    add(checks,'Return binds the exact independently audited packet230 and delivery manifest',(sn,ss,sc)==(d['sourcePacket']['bytes'],d['sourcePacket']['sha256'],d['sourcePacket']['crc32'].lower()) and source_d['archive']['sha256']==ss and source_d['archive']['bytes']==sn and packet['packet']['sha256']==ss and packet['deliveryManifest']['sha256']==sds,{'packetBytes':sn,'packetSha256':ss,'packetRecordSha256':packet['packet']['sha256'],'sourceDeliverySha256':sds})
    p210n,p210s,p210c=digest(PRIOR210); p229n,p229s,p229c=digest(PRIOR229)
    ext=d['externalEvidence']
    add(checks,'External prior Return210 and Return229 archive bindings match local audited returns',(p210n,p210s,p210c)==(ext['priorReturn210']['bytes'],ext['priorReturn210']['sha256'],ext['priorReturn210']['crc32'].lower()) and (p229n,p229s,p229c)==(ext['priorReturn229']['bytes'],ext['priorReturn229']['sha256'],ext['priorReturn229']['crc32'].lower()),{'prior210Sha256':p210s,'prior229Sha256':p229s})
    with zipfile.ZipFile(ARCHIVE) as z:
        names=z.namelist(); ext_rows={r['path']:r for r in d['members']}; unsafe=[x for x in names if x.startswith(('/','\\')) or '\\' in x or PurePosixPath(x).is_absolute() or '..' in PurePosixPath(x).parts]
        add(checks,'ZIP has exactly 109 unique safe members matching delivery allowlist',len(names)==len(set(names))==len(ext_rows)==d['memberCount']==109 and set(names)==set(ext_rows) and not unsafe and z.testzip() is None,{'archiveMembers':len(names),'deliveryMembers':len(ext_rows),'unsafe':unsafe[:8]})
        bad=[]
        for name,row in ext_rows.items():
            if member_digest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()): bad.append(name)
        add(checks,'Every ZIP member independently matches delivery size/SHA/CRC',not bad,{'checked':len(ext_rows),'failures':bad[:12]})
        manifest=readj(z,'MANIFEST.json'); inner={r['path']:r for r in manifest['members']}; payload=set(names)-{'MANIFEST.json'}
        add(checks,'Internal manifest and external manifest rows reconcile',set(inner)==payload and len(inner)==manifest['payloadCount']==d['payloadCount']==108 and manifest['sourcePacket']['sha256']==d['sourcePacket']['sha256'],{'internalRows':len(inner),'payloadMembers':len(payload)})
        bad=[]
        for name,row in inner.items():
            if member_digest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()): bad.append(name)
        add(checks,'Every payload member independently matches internal manifest',not bad,{'checked':len(inner),'failures':bad[:12]})
        decision=readj(z,'DIRECTOR_DECISION.json'); counts=readj(z,'COUNTS.json'); replay=readj(z,'CASE_REPLAY.json'); dispositions=readj(z,'CASE_DISPOSITIONS.json'); semantic=readj(z,'INDEPENDENT_SEMANTIC_FAILURE_CHECK.json'); reassess=readj(z,'BLOCKER_REASSESSMENT.json'); obligations=readj(z,'OBLIGATION_DISPOSITIONS.json'); questions=readj(z,'ORIGINAL_QUESTIONS.json'); qdisp=readj(z,'QUESTION_DISPOSITIONS.json'); future=readj(z,'ORIGINAL_FUTURE_REQUIREMENTS.json'); nxt=readj(z,'NEXT_GROUP.json'); hold=readj(z,'HOLD_REGISTER.json'); authority=readj(z,'CURRENT_AUTHORITY.json'); pres=readj(z,'PRESERVATION_MANIFEST.json'); source_bind=readj(z,'SOURCE_BINDINGS.json'); audit_results=readj(z,'AUDIT_RESULTS.json'); validation=readj(z,'VALIDATION.json')
        add(checks,'Decision holds exactly the two target IDs and preserves 811/37/0 without canonical changes',decision['authority']==AUTH and decision['authority']==d['authority'] and decision['accepted'] is False and decision['applied'] is False and decision['acceptedIds']==[] and decision['heldIds']==TARGET and d['accepted'] is False and d['applied'] is False and d['acceptedIds']==[] and d['heldIds']==TARGET and decision['canonicalChanges'] is False and authority['changes'] is False,{'heldIds':d['heldIds'],'authority':d['authority']})
        decisions={x['id']:x for x in decision['decisions']}; ddec={x['id']:x for x in d['decisions']}
        add(checks,'Per-spell rulings retain Return210 blockers and no acceptance/application',set(decisions)==set(TARGET)==set(ddec) and all(decisions[x]['decision']=='held' and decisions[x]['accepted'] is False and decisions[x]['applied'] is False and decisions[x]['blockerIds']==ddec[x]['blockerIds'] for x in TARGET) and decisions['eternal-forge']['blockerIds']==['MF210-B01'] and decisions['matter-conversion']['blockerIds']==['MF210-B02'],{'blockers':{x:decisions[x]['blockerIds'] for x in TARGET}})
        blockers={x['id']:x for x in reassess['blockers']}
        expected_witnesses={'eternal-forge':['MF230-F-W01','MF230-F-W02','MF230-F-W03'],'matter-conversion':['MF230-M-W01','MF230-M-W02','MF230-M-W03']}
        add(checks,'Both blocker reassessments preserve exact minimum-witness IDs and source-versus-coverage distinctions',set(blockers)=={'MF210-B01','MF210-B02'} and all(blockers[k]['reassessed'] is True and [x['id'] for x in blockers[k]['minimumMissingWitnesses']]==expected_witnesses[next(iter(blockers[k]['spellIds']))] and any(x.get('sourceFactsVersusCoverage') for x in blockers[k]['minimumMissingWitnesses']) for k in blockers),{'witnesses':{k:[x['id'] for x in v['minimumMissingWitnesses']] for k,v in blockers.items()}})
        add(checks,'Semantic audit separates replay success from three open acceptance requirements',semantic['accepted'] is False and semantic['applied'] is False and semantic['semanticAcceptancePassed'] is False and semantic['checkCount']==13 and semantic['passedChecks']==10 and semantic['failedAcceptanceRequirements']==3 and semantic['blockerIds']==['MF210-B01','MF210-B02'] and sum(1 for x in semantic['checks'] if x['passed'] is False)==3,{'passed':semantic['passedChecks'],'failedAcceptanceRequirements':semantic['failedAcceptanceRequirements']})
        case_rows=replay['cases']; case_ids={x['id'] for x in case_rows}; disp_ids={x['id'] for x in dispositions}
        events=sum(x['events'] for x in case_rows); fops=sum(x['forwardOperations'] for x in case_rows); iops=sum(x['inverseOperations'] for x in case_rows)
        add(checks,'All 27 preserved cases replay and every case disposition reconciles',len(case_rows)==27 and len(dispositions)==27 and case_ids==disp_ids and all(x['passed'] is True for x in case_rows) and replay['summary']['cases']==27 and replay['summary']['failedChecks']==0,{'cases':len(case_rows),'failedCases':sum(x['passed'] is not True for x in case_rows)})
        add(checks,'Replay totals reconcile to 50 events and 100 forward/inverse operations',(events,fops,iops)==(50,100,100) and (replay['summary']['events'],replay['summary']['forwardOperations'],replay['summary']['inverseOperations'])==(50,100,100) and (counts['events'],counts['forwardOperations'],counts['inverseOperations'])==(50,100,100) and (d['counts']['events'],d['counts']['forwardOperations'],d['counts']['inverseOperations'])==(50,100,100),{'events':events,'forward':fops,'inverse':iops})
        add(checks,'Four required main cases remain incomplete and 24 questions/2 addenda/5 future requirements remain preserved',len(obligations['requiredMainCases'])==counts['requiredMainCases']==4 and all(x['currentStatus']=='incomplete' for x in obligations['requiredMainCases']) and len(questions)==counts['originalQuestions']==24 and len(qdisp)==counts['currentDispositions']==26 and counts['focusedAddenda']==2 and len(future)==counts['futureRequirements']==5 and counts['requiredMainCasesIncomplete']==4,{'mainCases':len(obligations['requiredMainCases']),'questions':len(questions),'dispositions':len(qdisp),'futureRequirements':len(future)})
        add(checks,'Source binding count and historical carry-forward records agree',len(source_bind['rows'])==counts['sourceBindings']==174 and source_bind['sourcePacket']['sha256']==ss and len(source_bind['changedSinceHistorical'])==1 and pres['completeCaseCount']==27 and pres['allCasesByteExact'] is True and pres['proceduresByteExact'] is True,{'bindings':len(source_bind['rows']),'changedSinceHistorical':len(source_bind['changedSinceHistorical'])})
        prior_members={r['path']:r for r in pres['byteExactMembersAtRootOrCases']}; prior_fail=[]
        with zipfile.ZipFile(PRIOR210) as pz:
            for name,row in prior_members.items():
                if name not in z.namelist() or name not in pz.namelist() or z.read(name)!=pz.read(row['priorArchiveMember']): prior_fail.append(name)
        add(checks,'Byte-exact Return210 procedures, casebook, profiles, requirements and cases are preserved',not prior_fail and len(prior_members)>=30,{'preservedMembers':len(prior_members),'failures':prior_fail[:12]})
        add(checks,'All other holds remain outside scope and authority gates remain closed',bool(hold.get('outsideScopePreserved')) and hold.get('allOtherHolds') is not None and decision['runtimeExecuted'] is False and any('runtime' in str(x).lower() for x in decision['qualifications']),{'outsideScopePreserved':str(hold.get('outsideScopePreserved'))[:400]})
        add(checks,'Return points to the exact next pending five-identity group',nxt['group']==NEXT['group'] and nxt['pendingIds']==NEXT['pendingIds'] and nxt['scope'] and nxt['originalQueueRow']['group']==NEXT['group'] and nxt['originalQueueRow']['pendingIds']==NEXT['pendingIds'] and nxt['originalQueueRow']['pendingCount']==5 and nxt['originalQueueRow']['priorHeldBatch']['ids']==TARGET and nxt['originalQueueRow']['priorHeldBatch']['blockers']==['MF210-B01','MF210-B02'],{'group':nxt['group'],'ids':nxt['pendingIds']})
        add(checks,'Independent check script and validation counts agree with sealed delivery',audit_results['summary']['checkCount']==counts['checkCount']==d['counts']['checkCount']==2615 and audit_results['summary']['passedChecks']==counts['passedChecks']==2615 and counts['failedChecks']==0 and validation['data']['checkCount']==2615 and validation['semantic']['failedAcceptanceRequirements']==3,{'checks':counts['checkCount'],'semanticFailures':validation['semantic']['failedAcceptanceRequirements']})
    failed=[x for x in checks if not x['passed']]
    report={'id':'RANK9MATERIALFORGING2_RETURN230_INDEPENDENT_AUDIT','createdAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not failed else 'FAIL','archive':{'path':str(ARCHIVE.relative_to(ROOT)),'bytes':n,'sha256':s,'crc32':c},'deliveryManifest':{'path':str(DELIVERY.relative_to(ROOT)),'bytes':dn,'sha256':ds,'crc32':dc},'decision':'HELD_NO_APPLICATION','heldIds':TARGET,'blockers':['MF210-B01','MF210-B02'],'nextPendingGroup':NEXT,'caseReplay':{'cases':27,'events':events,'forwardOperations':fops,'inverseOperations':iops},'checkCount':len(checks),'passedChecks':len(checks)-len(failed),'failedChecks':len(failed),'checks':checks}
    REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    receipt={'id':'RANK9MATERIALFORGING2_RETURN230_RECEIPT','auditStatus':report['status'],'archive':report['archive'],'deliveryManifest':report['deliveryManifest'],'independentAudit':{'path':str(REPORT.relative_to(ROOT)),'bytes':REPORT.stat().st_size,'sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest()},'heldIds':TARGET,'acceptedIds':[],'appliedIds':[],'nextPendingGroup':NEXT,'checkCount':len(checks),'failedChecks':len(failed)}
    RECEIPT.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'checkCount':len(checks),'passedChecks':len(checks)-len(failed),'failedChecks':len(failed),'archiveSha256':s,'deliverySha256':ds,'failed':failed,'report':str(REPORT.relative_to(ROOT)),'receipt':str(RECEIPT.relative_to(ROOT))},indent=2))
    if failed: raise SystemExit(1)
if __name__=='__main__': main()
