from __future__ import annotations
import hashlib,json,zlib,zipfile,subprocess
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT=AUDIT/'rank9_materialforging2_current_source_230_prepared'
ARCHIVE=OUT/'DD_Rank9_MaterialForging2_CurrentSource_230.zip'; DELIVERY=OUT/'DD_Rank9_MaterialForging2_CurrentSource_230_DELIVERY.json'
CAND=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_230.json'; CONTEXT=OUT/'CURRENT_CONTEXT_230.json'; REQUEST=OUT/'REQUEST_230.txt'
HIST=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_material_forging_2_source_conference_02.json'
HISTZIP=ROOT/'docs/audit/2026-10-08/full-game/DD_Rank9_Material_Forging_2_Source_Conference_02.zip'
PACKET=AUDIT/'RANK9MATERIALFORGING2_PACKET_230.json'; PREP=AUDIT/'RANK9MATERIALFORGING2_SOURCE_PREPARATION_230.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_230.json'; HANDOFF=AUDIT/'CURRENT_HANDOFF_230.json'; PENDING=AUDIT/'CURRENT37_PENDING_IDENTITY_AUDIT_230.json'
NOTES=AUDIT/'RANK9MATERIALFORGING2_NEXT_CONFERENCE_NOTES_129.json'
R210=AUDIT/'rank9_materialforging2_return210_received'; R229=AUDIT/'rank9_illusionreality5_return229_received'
R229AUDIT=AUDIT/'RANK9ILLUSIONREALITY5_RETURN229_INDEPENDENT_AUDIT.json'
REPORT=AUDIT/'RANK9MATERIALFORGING2_PACKET_230_INDEPENDENT_AUDIT.json'; RECEIPT=AUDIT/'RANK9MATERIALFORGING2_PACKET_230_RECEIPT.json'
AUTH={'reviewedApplied':811,'pending':37,'acceptedUnapplied':0,'completeStandaloneProcedures':535,'scopedInterfaces':173}
TARGETS=['eternal-forge','matter-conversion']; GROUP='rank9-material-forging2'
def digest(p):
 h=hashlib.sha256();c=0;n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);c=zlib.crc32(b,c);n+=len(b)
 return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def mdigest(z,n):
 h=hashlib.sha256();c=0;s=0
 with z.open(n) as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);c=zlib.crc32(b,c);s+=len(b)
 return s,h.hexdigest(),f'{c&0xffffffff:08x}'
def readj(z,n):return json.loads(z.read(n).decode('utf-8-sig'))
def add(c,n,p,d=None):c.append({'check':n,'passed':bool(p),'detail':d})
def info(p):
 n,s,c=digest(p);return {'path':p.relative_to(ROOT).as_posix(),'bytes':n,'sha256':s,'crc32':c}
def main():
 checks=[]; d=json.loads(DELIVERY.read_text(encoding='utf-8-sig')); packet=json.loads(PACKET.read_text(encoding='utf-8-sig')); prep=json.loads(PREP.read_text(encoding='utf-8-sig'))
 n,s,c=digest(ARCHIVE); dn,ds,dc=digest(DELIVERY); hn,hs,hc=digest(HISTZIP)
 add(checks,'Packet230 archive and delivery bind exact bytes/SHA/CRC and label',(n,s,c)==(d['archive']['bytes'],d['archive']['sha256'],d['archive']['crc32']) and d['archive']['path']==ARCHIVE.relative_to(ROOT).as_posix() and packet['archive']['sha256']==s and prep['archive']['sha256']==s,{'bytes':n,'sha256':s,'crc32':c})
 add(checks,'Candidate/context/request sidecars match independent delivery bindings',all((p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())==(row['bytes'],row['sha256']) for p,row in [(CAND,d['candidate']),(CONTEXT,d['context']),(REQUEST,d['request'])]),{'candidate':d['candidate'],'context':d['context'],'request':d['request']})
 with zipfile.ZipFile(ARCHIVE) as z:
  names=z.namelist(); unsafe=[x for x in names if x.startswith(('/','\\')) or '\\' in x or PurePosixPath(x).is_absolute() or '..' in PurePosixPath(x).parts]; m=readj(z,'MANIFEST.json'); rows={x['path']:x for x in m['members']}
  add(checks,'Archive has exact unique safe allowlisted members and valid ZIP CRCs',len(names)==len(set(names))==d['members']==215 and len(rows)==d['manifestBindings']==214 and set(names)==set(rows)|{'MANIFEST.json'} and not unsafe and z.testzip() is None,{'members':len(names),'manifestRows':len(rows),'unsafe':unsafe[:8]})
  bad=[]
  for name,row in rows.items():
   if mdigest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()):bad.append(name)
  add(checks,'Every archive member matches external delivery size/SHA/CRC',not bad,{'checked':len(rows),'failures':bad[:12]})
  ir=rows; payload=set(names)-{'MANIFEST.json'}
  add(checks,'Internal manifest has the exact payload allowlist and agrees with delivery counts',set(ir)==payload and len(ir)==d['manifestBindings']==214 and m['memberCountExcludingSelf']==214 and m['sourceCommit']==d['sourceCommit'] and m['sourceBranch']==d['sourceBranch'] and m['sourceAuthority']==AUTH and m['group']==GROUP and m['pendingIds']==TARGETS,{'payload':len(payload),'internalRows':len(ir)})
  bad=[]
  for name,row in ir.items():
   if mdigest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()):bad.append(name)
  add(checks,'Every payload member matches internal manifest',not bad,{'checked':len(ir),'failures':bad[:12]})
  candidate=readj(z,'CURRENT_SOURCE_CONFERENCE_CANDIDATE_230.json'); context=readj(z,'CURRENT_CONTEXT_230.json'); notes=readj(z,'NOTES/RANK9MATERIALFORGING2_NEXT_CONFERENCE_NOTES_129.json')
  queue=readj(z,'current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_230.json'); handoff=readj(z,'current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_230.json'); pending=readj(z,'current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_230.json')
  index=readj(z,'current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'); catalog=readj(z,'current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json')
  r210=readj(z,'evidence/RETURN210_DELIVERY.json'); r210audit=readj(z,'evidence/RETURN210_INDEPENDENT_AUDIT.json'); r210decision=readj(z,'evidence/RETURN210.zip') if False else None
  r229d=readj(z,'evidence/RETURN229_DELIVERY.json'); r229audit=readj(z,'evidence/RETURN229_INDEPENDENT_AUDIT.json')
  historic=readj(z,'current/'+HIST.relative_to(ROOT).as_posix())
  # Historical archive is a separate sealed input. Verify all 174 source bindings against it.
  historical_archive=z.read('historical/DD_Rank9_Material_Forging_2_Source_Conference_02.zip')
 add(checks,'Fresh packet scope and authority match current index/catalog and queue',candidate['currentAuthority']==AUTH and candidate['currentBranch']=='main' and candidate['currentSourceCommit']==d['sourceCommit'] and [r['spellId'] for r in candidate['records']]==TARGETS and candidate['currentPendingGroup']=={'group':GROUP,'spellIds':TARGETS,'count':2} and d['sourceAuthority']==AUTH and d['group']==GROUP and d['pendingIds']==TARGETS and d['accepted'] is False and d['applied'] is False and context['sourceAuthority']==AUTH and context['targetGroup']['pendingIds']==TARGETS and queue['currentAuthority']==AUTH and handoff['currentAuthority']==AUTH and pending['pendingCount']==37 and pending['authority']==AUTH,{'targetIds':TARGETS,'authority':AUTH})
 entries={x['id']:x for x in index['entries']}; spells={x['id']:x for x in catalog['spells']}
 add(checks,'Both target identities remain pending with exact native access and no accepted procedure',all(entries[s]['authoredStatus']=='pending-authored-procedure' and entries[s]['sourceStatus']=='blocked-pending-operational-review' and spells[s]['status']=='blocked-pending-operational-review' and spells[s]['operational'] is None for s in TARGETS) and all(s in pending['pendingIds'] for s in TARGETS) and index['authoredCounts']=={'reviewed':811,'pending':37},{'targets':TARGETS})
 add(checks,'Twenty-four original questions, both addenda, four new main cases and five future requirements are preserved',len(candidate['questions'])==24 and len(notes['completeOriginalQuestionsUnchanged'])==24 and len(notes['focusedAdditionalQuestions'])==2 and len(notes['requiredNewCases'])==4 and len(candidate['futureCaseRequirements'])==5 and len(notes['originalFutureCaseRequirementsUnchanged'])==5 and d['sourceBindings']==174,{'questions':len(candidate['questions']),'addenda':len(notes['focusedAdditionalQuestions']),'mainCases':len(notes['requiredNewCases']),'futureRequirements':len(candidate['futureCaseRequirements'])})
 # Preserve the exact historical source archive and its 174 source bindings.
 import io
 with zipfile.ZipFile(io.BytesIO(historical_archive)) as hz:
  hist_bad=[]
  for row in candidate['historicalSourceBindings']:
   if mdigest(hz,'sources/'+row['path'])[:2]!=(row['bytes'],row['sha256']):hist_bad.append(row['path'])
 add(checks,'Historical source candidate/archive and all 174 original source rows remain exact',hn==d['historicalSourceArchive']['bytes'] and hs==d['historicalSourceArchive']['sha256'] and len(candidate['historicalSourceBindings'])==174 and not hist_bad,{'archiveBytes':hn,'archiveSha256':hs,'sourceRows':174,'failures':hist_bad[:8]})
 current_bad=[]
 with zipfile.ZipFile(ARCHIVE) as source_zip:
  for row in candidate['sourceBindings']:
   name='sources_current/'+row['path']
   try: packed=mdigest(source_zip,name)
   except KeyError: current_bad.append(row['path']); continue
   p=ROOT/row['path']
   if not p.exists() or packed[:2]!=(row['bytes'],row['sha256']) or (p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())!=(row['bytes'],row['sha256']):current_bad.append(row['path'])
 add(checks,'All 174 refreshed source bindings match both packet copies and current working-tree bytes',len(candidate['sourceBindings'])==174 and not current_bad,{'checked':len(candidate['sourceBindings']),'failures':current_bad[:8]})
 # Locate current snapshot queue and exact previous/current group order.
 groups=queue['currentPendingGroups']; pos=next(i for i,x in enumerate(groups) if x['group']==GROUP); prev=groups[pos-1]
 add(checks,'Queue order is Illusion/Reality5 then Material Forging2 and exactly these two pending IDs',prev['group']=='rank9-illusion-reality5' and groups[pos]['pendingIds']==TARGETS and queue['nextGroup']==GROUP and queue['next']['pendingIds']==TARGETS and queue['pendingCount']==37,{'previous':prev['group'],'current':groups[pos]['group'],'pendingIds':groups[pos]['pendingIds']})
 add(checks,'Return210 prior decision is independently checked and retains exact per-spell blockers',r210['accepted'] is False and r210['applied'] is False and r210['acceptedIds']==[] and r210['heldIds']==TARGETS and [x['id'] for x in r210['blockers']]==['MF210-B01','MF210-B02'] and all(x['passed'] is True for x in r210audit['checks']),{'heldIds':r210['heldIds'],'blockers':[x['id'] for x in r210['blockers']],'sourceAuditChecks':len(r210audit['checks'])})
 add(checks,'Return229 hold remains preserved outside the two-identity packet scope',r229audit['status']=='PASS' and r229audit['failedChecks']==0 and r229d['heldIds']==['soul-reflection'] and r229d['blockerIds']==['IR207-B02'] and r229d['applied'] is False and 'soul-reflection' not in d['pendingIds'],{'return229Held':r229d['heldIds'],'blocker':r229d['blockerIds']})
 add(checks,'Packet does not apply changes or open runtime, implementation, play, balance or release gates',not candidate.get('runtimeTestsExecuted') and not candidate.get('humanPlaytests') and not candidate.get('sourceInformationDeleted') and candidate.get('noNewRuleAdoptions') is True and candidate.get('canonicalChanges') is False and candidate.get('applicationChanges') is False and queue.get('githubChanges') is False and d['accepted'] is False and d['applied'] is False,{'canonicalChanges':False,'applicationChanges':False})
 # Verify the current pending audit was derived from the exact local index and reports no accepted pending target.
 live=sorted(x['id'] for x in index['entries'] if x.get('authoredStatus')=='pending-authored-procedure')
 add(checks,'Pending audit equals all 37 pending authored-index IDs and includes both targets',len(live)==37 and sorted(pending['pendingIds'])==live and all(x in live for x in TARGETS) and pending['noPendingTargetWasSilentlyAccepted'] is True,{'pendingCount':len(live)})
 passed=sum(x['passed'] for x in checks)
 report={'id':'RANK9MATERIALFORGING2-PACKET-230-INDEPENDENT-AUDIT','status':'PASS' if passed==len(checks) else 'FAIL','checkedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(ARCHIVE),'delivery':info(DELIVERY),'sourceCommit':d['sourceCommit'],'sourceBranch':d['sourceBranch'],'authority':AUTH,'targetIds':TARGETS,'previousBlockers':d['previousReturn210']['blockerIds'],'previousOutsideScopeHolds':d['previousReturn229OutsideScope']['heldIds'],'sourceBindingsVerified':len(candidate['sourceBindings']),'checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed,'checks':checks}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');rn,rs,rc=digest(REPORT)
 receipt={'id':'RANK9MATERIALFORGING2-PACKET-230-RECEIPT','status':report['status'],'archive':report['archive'],'delivery':report['delivery'],'independentAudit':{'path':REPORT.relative_to(ROOT).as_posix(),'bytes':rn,'sha256':rs,'crc32':rc},'checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed}
 RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 packet=json.loads(PACKET.read_text(encoding='utf-8-sig'));packet['status']='PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT';packet['independentAudit']=info(REPORT);packet['auditReceipt']=info(RECEIPT);PACKET.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 prep=json.loads(PREP.read_text(encoding='utf-8-sig'));prep['independentAudit']=info(REPORT);prep['auditReceipt']=info(RECEIPT);PREP.write_text(json.dumps(prep,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for p in (QUEUE,HANDOFF):
  x=json.loads(p.read_text(encoding='utf-8-sig')); x['currentPacketAudit']=info(REPORT); x['currentPacketAuditReceipt']=info(RECEIPT)
  x['nextPreparedRequest']['status']='PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT';x['nextPreparedRequest']['independentAudit']=info(REPORT);x['nextPreparedRequest']['auditReceipt']=info(RECEIPT)
  if p==HANDOFF:x['status']='PACKET230_PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT_811_37';x['resumePriority']='Submit packet230 for exactly eternal-forge and matter-conversion to GPT; send repeated follow-up pings if needed, independently audit the returned ZIP and DELIVERY.json, then apply only exact accepted IDs.'
  else:x['packetStatus']='PACKET230_PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT'
  p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'checkCount':len(checks),'passedChecks':passed,'failedChecks':len(checks)-passed,'report':str(REPORT),'receipt':str(RECEIPT),'failed':[x for x in checks if not x['passed']]},ensure_ascii=False,indent=2))
 if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
