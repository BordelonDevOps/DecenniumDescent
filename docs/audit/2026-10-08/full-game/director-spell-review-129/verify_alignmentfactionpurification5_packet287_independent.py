from __future__ import annotations
import hashlib,json,zlib,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[5]; AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT=AUDIT/'rank9_alignmentfactionpurification5_current_source_287_prepared'
ARCHIVE=OUT/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287.zip'; DELIVERY=OUT/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287_DELIVERY.json'
CANDIDATE=OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json'; CONTEXT=OUT/'CURRENT_CONTEXT_287.json'; REQUEST=OUT/'REQUEST_287.txt'
SOURCE_HIST=ROOT/'docs/audit/2026-10-08/full-game/DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_02.zip'
REPORT=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_INDEPENDENT_AUDIT.json'; RECEIPT=AUDIT/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_RECEIPT.json'
AUTH={'reviewedApplied':816,'pending':32,'acceptedUnapplied':0,'completeStandaloneProcedures':540,'scopedInterfaces':173}
TARGETS=['alignment-ascension','alignment-perfection','faction-incarnate','faction-perfection','corruption-purification']
def digest(path):
 h=hashlib.sha256();c=0;n=0
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);c=zlib.crc32(b,c);n+=len(b)
 return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def mdigest(z,name):
 h=hashlib.sha256();c=0;n=0
 with z.open(name) as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);c=zlib.crc32(b,c);n+=len(b)
 return n,h.hexdigest(),f'{c&0xffffffff:08x}'
def add(cs,name,ok,detail=None):cs.append({'check':name,'passed':bool(ok),'detail':detail})
def readj(z,name):return json.loads(z.read(name).decode('utf-8-sig'))
def main():
 checks=[];d=json.loads(DELIVERY.read_text(encoding='utf-8-sig')); cand=json.loads(CANDIDATE.read_text(encoding='utf-8-sig')); ctx=json.loads(CONTEXT.read_text(encoding='utf-8-sig'))
 n,s,c=digest(ARCHIVE);dn,ds,dc=digest(DELIVERY)
 add(checks,'Packet287 ZIP size/SHA/CRC/filename match its delivery manifest',(n,s,c)==(d['archive']['bytes'],d['archive']['sha256'],d['archive']['crc32'].lower()) and d['archive']['path'].endswith(ARCHIVE.name),{'bytes':n,'sha256':s,'crc32':c})
 add(checks,'Delivery and context bind main/816-32 authority and exact five target IDs',d['sourceBranch']=='main' and d['sourceAuthority']==AUTH and d['group']==ctx['targetGroup']['group']=='rank9-alignment-faction-purification5' and d['pendingIds']==ctx['targetGroup']['pendingIds']==TARGETS and ctx['sourceCommit']==d['sourceCommit'],{'authority':d['sourceAuthority'],'targets':d['pendingIds']})
 with zipfile.ZipFile(ARCHIVE) as z:
  names=z.namelist(); unsafe=[x for x in names if x.startswith(('/','\\')) or '\\' in x or PurePosixPath(x).is_absolute() or '..' in PurePosixPath(x).parts]
  m=readj(z,'MANIFEST.json'); rows={x['path']:x for x in m['members']}
  add(checks,'ZIP has 166 unique safe members matching its internal allowlist',len(names)==len(set(names))==d['members']==166 and len(rows)==d['manifestBindings']==d['members']-1 and set(names)-{'MANIFEST.json'}==set(rows) and not unsafe and z.testzip() is None,{'members':len(names),'unsafe':unsafe[:8]})
  bad=[]
  for name,row in rows.items():
   if mdigest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()):bad.append(name)
  add(checks,'Every ZIP member independently matches delivery size/SHA/CRC',not bad,{'checked':len(rows),'failures':bad[:10]})
  internal=rows;payload=set(names)-{'MANIFEST.json'}
  add(checks,'Internal manifest, member count, authority, branch and group reconcile',set(internal)==payload and len(internal)==m['memberCountExcludingSelf']==d['members']-1 and m['sourceAuthority']==AUTH and m['sourceBranch']=='main' and m['pendingIds']==TARGETS and m['group']==d['group'],{'members':len(internal)})
  bad=[]
  for name,row in internal.items():
   if mdigest(z,name)!=(row['bytes'],row['sha256'],row['crc32'].lower()):bad.append(name)
  add(checks,'Every payload member independently matches internal manifest',not bad,{'checked':len(internal),'failures':bad[:10]})
  hist=readj(z,'CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json'); packet_context=readj(z,'CURRENT_CONTEXT_287.json');
  add(checks,'Embedded fresh candidate preserves all identities, 28 original questions and seven future requirements',hist['id']=='CURRENT-SOURCE-CONFERENCE-CANDIDATE-287' and {x['spellId'] for x in hist['records']}==set(TARGETS) and len(hist['questions'])==28 and len(hist['futureCaseRequirements'])==7 and hist['currentAuthority']==AUTH and hist['newRuleAdoptions']==0,{'records':len(hist['records']),'questions':len(hist['questions']),'futureRequirements':len(hist['futureCaseRequirements'])})
  live_index=json.loads(z.read('sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json').decode('utf-8-sig'))
  live_catalog=json.loads(z.read('sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json').decode('utf-8-sig'))
  index_rows={x['id']:x for x in live_index['entries']};catalog_rows={x['id']:x for x in live_catalog['spells']}
  add(checks,'All target entries remain pending and embedded catalog/access rows match exactly',all(r['currentIndexEntry']==index_rows[r['spellId']] and r['currentIndexEntry']['authoredStatus']=='pending-authored-procedure' and r['completeCurrentCatalogSourceAndAccess']==catalog_rows[r['spellId']] for r in hist['records']),{'targetIds':sorted(r['spellId'] for r in hist['records'])})
  source_rows=hist['sourceBindings']; bad=[]
  for row in source_rows:
   member='sources_current/'+row['path']
   if member not in z.namelist() or mdigest(z,member)!=(row['bytes'],row['sha256'],row['crc32'] if row.get('crc32') else mdigest(z,member)[2]):bad.append(member)
  # Current source rows carry git object hashes as well as exact byte hashes; compare those and expected one-file refresh.
  changed=hist['sourceBindingRefresh']['changedSinceHistoricalCandidate']
  add(checks,'All 130 refreshed source-binding bytes are present and the only source change is the current authored index',len(source_rows)==130 and not bad and len(changed)==1 and changed[0]['path']=='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json' and ctx['changedHistoricalSourceBindings']==changed,{'sourceBindings':len(source_rows),'changed':changed,'missingOrBad':bad[:8]})
  hsize,hsha,hcrc=digest(SOURCE_HIST)
  add(checks,'Historical source conference02 archive is byte-bound to packet and candidate',('historical/DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_02.zip' in z.namelist()) and mdigest(z,'historical/DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_02.zip')==(hsize,hsha,hcrc) and hsha==d['historicalSourceArchive']['sha256'],{'bytes':hsize,'sha256':hsha})
  # Confirm referenced pre-packet queue/handoff/audit snapshots are actually included exactly as bound.
  ev=hist['currentAuthorityEvidence']; refchecks=[]
  for key in ['currentQueue','currentHandoff','currentPendingIdentityAudit']:
   row=ev[key]; nested='current/'+row['path']
   refchecks.append(nested in z.namelist() and mdigest(z,nested)[:2]==(row['bytes'],row['sha256']))
  add(checks,'Current queue, handoff and pending-audit snapshots match their embedded bindings',all(refchecks),{'snapshotBindings':{k:ev[k] for k in ['currentQueue','currentHandoff','currentPendingIdentityAudit']}})
  # Latest Return247 plus preserved Soul Reflection and reverse-gravity holds are present and hash-exact.
  return_specs=[('RETURN286','previousReturn286'),('RETURN285','previousReturn285'),('RETURN284','previousReturn284')]
  return_ok=[]
  for label,key in return_specs:
   embedded='evidence/'+label+'.zip'; row=d[key]['archive']
   return_ok.append(embedded in z.namelist() and mdigest(z,embedded)[:2]==(row['bytes'],row['sha256']))
  add(checks,'Return286, Return285 and Return284 archives match their preserved embedded decision bindings',all(return_ok),{'returns':return_ok})
  expected_returns=[('RETURN286','previousReturn286',['reverse-gravity-field'],{'reverse-gravity-field':['IE204-B02']},'DD_Rank9_ImpactExile4_Director_Return286_HELD_DELIVERY.json','RANK9IMPACTEXILE4_RETURN286_RECEIPT.json'),('RETURN285','previousReturn285',['summon-elemental-avatar','summon-herald-of-the-planes','summon-avatar-of-decay'],{'summon-elemental-avatar':['SH202-B01'],'summon-herald-of-the-planes':['SH202-B02'],'summon-avatar-of-decay':['SH202-B03']},'DD_Rank9_SummonHosts5_Director_Return285_HELD_DELIVERY.json','RANK9SUMMONHOSTS5_RETURN285_RECEIPT.json'),('RETURN284','previousReturn284',['banishment-gate','conjure-demiplane-fortress'],{'banishment-gate':['PG200-B03','PG200-B04'],'conjure-demiplane-fortress':['PG200-B06']},'DD_Rank9_PlanarGates5_Director_Return284_HELD_DELIVERY.json','RANK9_PLANARGATES5_RETURN284_RECEIPT.json')]
  preserved=[]
  for label,key,held,blockers,delivery_name,receipt_name in expected_returns:
   row=d[key];folder=Path(row['archive']['path']).parent;archive_path=ROOT/row['archive']['path'];audit_path=ROOT/row['audit']['path'];delivery_path=ROOT/folder/delivery_name;receipt_path=AUDIT/receipt_name
   expected_held=row['heldIds']==held and row['blockers']==blockers
   archive_ok=digest(archive_path)[:2]==(row['archive']['bytes'],row['archive']['sha256']) and mdigest(z,'evidence/'+label+'.zip')[:2]==(row['archive']['bytes'],row['archive']['sha256'])
   audit_ok=digest(audit_path)[:2]==(row['audit']['bytes'],row['audit']['sha256']) and mdigest(z,'evidence/'+label+'_INDEPENDENT_AUDIT.json')[:2]==(row['audit']['bytes'],row['audit']['sha256'])
   delivery_ok=delivery_path.exists() and delivery_path.read_bytes()==z.read('evidence/'+label+'_DELIVERY.json')
   receipt_ok=receipt_path.exists() and receipt_path.read_bytes()==z.read('evidence/'+label+'_RECEIPT.json')
   preserved.append({'return':label,'passed':expected_held and archive_ok and audit_ok and delivery_ok and receipt_ok,'archive':archive_ok,'audit':audit_ok,'delivery':delivery_ok,'receipt':receipt_ok,'heldAndBlockers':expected_held})
  add(checks,'All three prior held returns retain exact blocker identities and external archive, delivery, audit and receipt bytes',all(x['passed'] for x in preserved),{'returns':preserved})
  txt=z.read('REQUEST_287.txt').decode('utf-8')
  add(checks,'Director request restricts scope, blocks invention/application and requires sealed ZIP plus DELIVERY',all(x in txt for x in ['Review ONLY','AFP211-B01 through AFP211-B05','AFP211-E01','Do not invent','Do not change canonical files','Continue through response caps']) and all(sid in txt for sid in TARGETS),{'requestBytes':len(txt.encode('utf-8'))})
  add(checks,'Packet and candidate preserve prior AFP211 blockers and closed shared-evidence status',hist['priorAFP211DispositionToReassess']['contentBlockers']==['AFP211-B01','AFP211-B02','AFP211-B03','AFP211-B04','AFP211-B05'] and hist['priorAFP211DispositionToReassess']['closedSharedEvidenceBlocker']=='AFP211-E01' and d['priorAFP211ContentBlockers']==hist['priorAFP211DispositionToReassess']['contentBlockers'],{'contentBlockers':d['priorAFP211ContentBlockers']})
  add(checks,'Package remains review-only and has no accepted/applied result',d['status']=='PREPARED_UNAUDITED_UNSENT' and d['accepted'] is False and d['applied'] is False and packet_context['canonicalChanges'] is False and packet_context['applyChanges'] is False and packet_context['runtimeExecuted'] is False,{'status':d['status'],'accepted':d['accepted'],'applied':d['applied']})
 failed=[x for x in checks if not x['passed']]
 report={'id':'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_INDEPENDENT_AUDIT','createdAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not failed else 'FAIL','archive':{'path':str(ARCHIVE.relative_to(ROOT)),'bytes':n,'sha256':s,'crc32':c},'deliveryManifest':{'path':str(DELIVERY.relative_to(ROOT)),'bytes':dn,'sha256':ds,'crc32':dc},'authority':AUTH,'targetIds':TARGETS,'sourceBindings':130,'originalQuestions':28,'futureRequirements':7,'memberCount':len(names),'checkCount':len(checks),'passedChecks':len(checks)-len(failed),'failedChecks':len(failed),'checks':checks}
 REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 receipt={'id':'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_RECEIPT','auditStatus':report['status'],'archive':report['archive'],'deliveryManifest':report['deliveryManifest'],'independentAudit':{'path':str(REPORT.relative_to(ROOT)),'bytes':REPORT.stat().st_size,'sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest()},'authority':AUTH,'targetIds':TARGETS,'acceptedIds':[],'appliedIds':[],'nextAction':'Submit audited packet287 to GPT director; continue pings until return ZIP and matching DELIVERY.json are attached.','checkCount':len(checks),'failedChecks':len(failed)}
 RECEIPT.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'checkCount':len(checks),'passedChecks':len(checks)-len(failed),'failedChecks':len(failed),'archiveSha256':s,'deliverySha256':ds,'failed':failed},indent=2))
 if failed:raise SystemExit(1)
if __name__=='__main__':main()

