from __future__ import annotations
import hashlib,json,zlib,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[5]; AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'; OUT=AUDIT/'rank9_illusionreality5_current_source_229_prepared'
ARCHIVE=OUT/'DD_Rank9_IllusionReality5_CurrentSource_229.zip'; DELIVERY=OUT/'DD_Rank9_IllusionReality5_CurrentSource_229_DELIVERY.json'; CANDIDATE=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_229.json'; CONTEXT=OUT/'CURRENT_CONTEXT_229.json'; REQUEST=OUT/'REQUEST_229.txt'
PACKET=AUDIT/'RANK9ILLUSIONREALITY5_PACKET_229.json'; PREP=AUDIT/'RANK9ILLUSIONREALITY5_SOURCE_PREPARATION_229.json'; QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_229.json'; HANDOFF=AUDIT/'CURRENT_HANDOFF_229.json'
REPORT=AUDIT/'RANK9ILLUSIONREALITY5_PACKET_229_INDEPENDENT_AUDIT.json'; RECEIPT=AUDIT/'RANK9ILLUSIONREALITY5_PACKET_229_RECEIPT.json'
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}; TARGET=['soul-reflection']; CLOSED=['supreme-illusion','mirrored-world','ethereal-disjunction','illusory-reality']; NEXT={'group':'rank9-illusion-reality5','pendingIds':TARGET}
def digest(path):
 h=hashlib.sha256();c=0;n=0
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b);c=zlib.crc32(b,c);n+=len(b)
 return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def mdigest(z,name):
 h=hashlib.sha256();c=0;n=0
 with z.open(name) as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);c=zlib.crc32(b,c);n+=len(b)
 return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def j(z,n):return json.loads(z.read(n).decode('utf-8-sig'))
def add(checks,name,ok,detail=None):checks.append({'check':name,'passed':bool(ok),'detail':detail})
def info(p):
 n,s,c=digest(p);return {'path':p.relative_to(ROOT).as_posix(),'bytes':n,'sha256':s,'crc32':c}
def main():
 checks=[];d=json.loads(DELIVERY.read_text(encoding='utf-8-sig')); n,s,c=digest(ARCHIVE);dn,ds,dc=digest(DELIVERY)
 add(checks,'Archive bytes/SHA/CRC and label match the external packet delivery',(n,s,c)==(d['archive']['bytes'],d['archive']['sha256'],d['archive']['crc32'].lower()) and d['archive']['path']==ARCHIVE.relative_to(ROOT).as_posix(),{'bytes':n,'sha256':s,'crc32':c})
 add(checks,'Candidate, context and request sidecars match their delivery bindings',all((p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())==(row['bytes'],row['sha256']) for p,row in [(CANDIDATE,d['candidate']),(CONTEXT,d['context']),(REQUEST,d['request'])]),{'candidate':d['candidate'],'context':d['context'],'request':d['request']})
 with zipfile.ZipFile(ARCHIVE) as z:
  names=z.namelist(); unsafe=[x for x in names if x.startswith(('/','\\')) or '\\' in x or PurePosixPath(x).is_absolute() or '..' in PurePosixPath(x).parts]
  add(checks,'Archive has exact unique safe members and valid ZIP CRCs',len(names)==len(set(names))==d['members'] and not unsafe and z.testzip() is None,{'members':len(names),'unsafe':unsafe[:8]})
  m=j(z,'MANIFEST.json'); rows={x['path']:x for x in m['members']}; payload=set(names)-{'MANIFEST.json'}
  add(checks,'Internal manifest is exact and names the current group/authority',set(rows)==payload and len(rows)==d['manifestBindings'] and m['sourceCommit']==d['sourceCommit'] and m['sourceBranch']==d['sourceBranch'] and m['sourceAuthority']==AUTH and m['group']==NEXT['group'] and m['pendingIds']==TARGET and m['closedAcceptedIds']==CLOSED,{'payloadMembers':len(payload),'manifestRows':len(rows)})
  bad=[]
  for name,row in rows.items():
   if mdigest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()):bad.append(name)
  add(checks,'Every packet member matches its independent size/SHA/CRC manifest row',not bad,{'checked':len(rows),'failures':bad[:12]})
  candidate=j(z,'CURRENT_SOURCE_CONFERENCE_CANDIDATE_229.json'); context=j(z,'CURRENT_CONTEXT_229.json'); notes=j(z,'NOTES/RANK9ILLUSIONREALITY5_NEXT_CONFERENCE_NOTES_129.json')
  q=j(z,'current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_229.json')
  h=j(z,'current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_229.json')
  pend=j(z,'current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_229.json')
  index=j(z,'current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
  catalog=j(z,'current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json')
  r207a=j(z,'evidence/RETURN207_INDEPENDENT_AUDIT.json');r207r=j(z,'evidence/RETURN207_RECEIPT.json');r207app=j(z,'evidence/RETURN207_APPLICATION.json');r207valid=j(z,'evidence/RETURN207_APPLICATION_VALIDATION.json')
  r228a=j(z,'evidence/RETURN228_INDEPENDENT_AUDIT.json');r228d=j(z,'evidence/RETURN228_DELIVERY.json')
  hist=j(z,'HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json')
  histzip=z.read('HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip')
 add(checks,'Current candidate, context and packet delivery agree on the exact one-identity scope and authority',candidate['currentAuthority']==AUTH and candidate['currentBranch']=='main' and candidate['currentSourceCommit']==d['sourceCommit'] and [x['spellId'] for x in candidate['records']]==TARGET and candidate['currentPendingGroup']=={'group':NEXT['group'],'spellIds':TARGET,'count':1} and d['sourceAuthority']==AUTH and d['group']==NEXT['group'] and d['pendingIds']==TARGET and d['accepted'] is False and d['applied'] is False and context['sourceAuthority']==AUTH and context['targetGroup']['pendingIds']==TARGET,{'scope':TARGET,'authority':AUTH})
 add(checks,'All 31 original questions, two focused addenda, 10 required cases and five future requirements are retained',len(candidate['questions'])==31 and len(notes['completeOriginalQuestionsUnchanged'])==31 and len(notes['focusedAdditionalQuestions'])==2 and len(notes['requiredNewCases'])==10 and len(candidate['futureCaseRequirements'])==5 and d['sourceBindings']==157,{'questions':len(candidate['questions']),'addenda':len(notes['focusedAdditionalQuestions']),'mainCases':len(notes['requiredNewCases']),'futureRequirements':len(candidate['futureCaseRequirements'])})
 add(checks,'Pending audit and current index agree on all 37 pending identities and Soul Reflection remains pending',pend['pendingCount']==37 and pend['authority']==AUTH and sorted(pend['pendingIds'])==sorted(x['id'] for x in index['entries'] if x.get('authoredStatus')=='pending-authored-procedure') and 'soul-reflection' in pend['pendingIds'] and q['nextGroup']==NEXT['group'] and q['next']['pendingIds']==TARGET and h['nextGroup']==NEXT['group'],{'pendingCount':len(pend['pendingIds']),'target':TARGET})
 add(checks,'Return207 accepted/applied identities stay closed and Soul Reflection remains held on its exact prior blocker',r207a['status']=='PASS' and r207a['acceptedIds']==CLOSED and r207a['heldIds']==TARGET and r207r['acceptedIds']==CLOSED and r207r['blockers']['soul-reflection']['blockerIds']==['IR207-B02'] and r207app['status'].startswith('APPLIED_FOUR_EXACT') and r207valid['status']=='PASS' and all(next(x for x in index['entries'] if x['id']==sid)['authoredStatus']=='reviewed-authored-operational-playtest' for sid in CLOSED),{'acceptedAppliedClosed':CLOSED,'held':TARGET,'blocker':'IR207-B02'})
 add(checks,'Return228 is independently audited held and outside Soul Reflection scope',r228a['status']=='PASS' and r228a['failedChecks']==0 and r228d['heldIds']==['reverse-gravity-field'] and r228d['applied'] is False and r228d['authority']==AUTH and candidate['previousReturn228OutsideScope']['outsideScope'] is True,{'return228Held':r228d['heldIds']})
 add(checks,'The current queue order places Soul Reflection after Impact/Exile4 and before Material Forging2',len(q['currentPendingGroups'])>12 and q['currentPendingGroups'][11]['group']=='rank9-impact-exile4' and q['currentPendingGroups'][12]['group']==NEXT['group'] and q['currentPendingGroups'][12]['pendingIds']==TARGET and q['currentPendingGroups'][13]['group']=='rank9-material-forging2',{'previous':q['currentPendingGroups'][11]['group'],'current':q['currentPendingGroups'][12]['group'],'next':q['currentPendingGroups'][13]['group']})
 add(checks,'Historical source candidate and exact archive remain bound to queue provenance',len(hist['records'])==5 and hist['questions']==candidate['questions'] and d['historicalCandidate']['sha256']==hashlib.sha256(z.read('HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json')).hexdigest() and len(histzip)==d['historicalSourceArchive']['bytes'] and hashlib.sha256(histzip).hexdigest()==d['historicalSourceArchive']['sha256'],{'historicalRecords':len(hist['records']),'historicalSourceBindings':len(hist['sourceBindings'])})
 # Verify all refreshed source bindings against local current bytes and packet copies.
 refreshed=candidate['sourceBindings']; failures=[]
 for row in refreshed:
  p=ROOT/row['path']; name='sources_current/'+row['path']
  if not p.exists() or (p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())!=(row['bytes'],row['sha256']) or mdigest(z,name)!=(row['bytes'],row['sha256'],rows[name]['crc32'].lower()): failures.append(row['path'])
 add(checks,'All 157 refreshed source bindings match current files and packet copies',len(refreshed)==157 and not failures,{'checked':len(refreshed),'failures':failures[:12]})
 # Verify source bindings against the historical conference archive before refreshing.
 hist_fail=[]
 with zipfile.ZipFile(__import__('io').BytesIO(histzip)) as hz:
  for row in candidate['historicalSourceBindings']:
   name='sources/'+row['path']
   if mdigest(hz,name)[:2]!=(row['bytes'],row['sha256']):hist_fail.append(row['path'])
 add(checks,'All historical source bindings remain intact in the original source conference archive',len(candidate['historicalSourceBindings'])==157 and not hist_fail,{'checked':len(candidate['historicalSourceBindings']),'failures':hist_fail[:12]})
 qual=candidate.get('runtimeTestsExecuted'); current_entries={x['id']:x for x in index['entries']}
 add(checks,'Application, canonical and downstream approval gates remain closed',candidate.get('runtimeTestsExecuted') is False and candidate.get('humanPlaytests') is False and candidate.get('sourceInformationDeleted') is False and all(current_entries[x]['authoredStatus']=='reviewed-authored-operational-playtest' for x in CLOSED) and current_entries['soul-reflection']['authoredStatus']=='pending-authored-procedure',{'canonicalChanges':False,'accepted':False,'applied':False})
 passed=sum(x['passed'] for x in checks); report={'id':'RANK9ILLUSIONREALITY5-PACKET-229-INDEPENDENT-AUDIT','status':'PASS' if passed==len(checks) else 'FAIL','checkedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(ARCHIVE),'delivery':info(DELIVERY),'sourceCommit':d['sourceCommit'],'sourceBranch':d['sourceBranch'],'authority':AUTH,'targetIds':TARGET,'closedAcceptedAppliedIds':CLOSED,'priorBlocker':'IR207-B02','checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed,'checks':checks}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');rn,rs,rc=digest(REPORT)
 receipt={'id':'RANK9ILLUSIONREALITY5-PACKET-229-RECEIPT','status':report['status'],'archive':info(ARCHIVE),'delivery':info(DELIVERY),'independentAudit':{'path':REPORT.relative_to(ROOT).as_posix(),'bytes':rn,'sha256':rs,'crc32':rc},'checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed};RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 if passed!=len(checks):raise SystemExit(1)
 packet=json.loads(PACKET.read_text(encoding='utf-8-sig'));packet['status']='PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT';packet['independentAudit']=info(REPORT);packet['auditReceipt']=info(RECEIPT);PACKET.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 prep=json.loads(PREP.read_text(encoding='utf-8-sig'));prep['independentAudit']=info(REPORT);prep['auditReceipt']=info(RECEIPT);PREP.write_text(json.dumps(prep,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for p in (QUEUE,HANDOFF):
  x=json.loads(p.read_text(encoding='utf-8-sig'));x['currentPacketAudit']=info(REPORT);x['currentPacketAuditReceipt']=info(RECEIPT)
  x['nextPreparedRequest']['status']='PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT';x['nextPreparedRequest']['independentAudit']=info(REPORT);x['nextPreparedRequest']['auditReceipt']=info(RECEIPT)
  if p==HANDOFF:x['status']='PACKET229_PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT_811_37';x['resumePriority']='Submit packet229 for exactly soul-reflection to GPT; send repeated follow-up pings if needed, independently audit the returned ZIP and DELIVERY.json, then apply only exact accepted IDs.'
  else:x['packetStatus']='PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT'
  p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed,'archiveBytes':n,'archiveSha256':s,'report':str(REPORT),'receipt':str(RECEIPT)},indent=2))
if __name__=='__main__':main()
