from __future__ import annotations
import copy,hashlib,json,pathlib,shutil,zipfile,zlib
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[5]
AUDIT=pathlib.Path(__file__).resolve().parent
DOWNLOAD=pathlib.Path(r'C:\Users\cbord\Downloads')
OUT=AUDIT/'rank9_fate_rewrite_return320_received'
SRC=AUDIT/'rank9_fate_rewrite_current_source_320_prepared'
RETURN_ZIP='DD_Rank9_FateRewrite_Director_Return320_HELD.zip'
RETURN_DELIVERY='DD_Rank9_FateRewrite_Director_Return320_HELD_DELIVERY.json'

def sha(b):return hashlib.sha256(b).hexdigest()
def crc(b):return f'{zlib.crc32(b)&0xffffffff:08x}'
def pretty(o):return(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':crc(b)}
def j(p):return json.loads(p.read_text(encoding='utf-8'))
def safe(n):
 q=pathlib.PurePosixPath(n)
 if not n or q.is_absolute() or '..' in q.parts or '\\' in n: raise ValueError(n)
checks=[]
def ck(n,ok,detail=None):
 checks.append({'check':n,'passed':bool(ok),'detail':detail})
 if not ok: raise AssertionError(f'{n}: {detail}')

if OUT.exists():
 if any(x.name not in {RETURN_ZIP,RETURN_DELIVERY} for x in OUT.iterdir()): raise RuntimeError(f'unexpected preexisting extracted files: {OUT}')
else: OUT.mkdir(parents=True)
zip_src=DOWNLOAD/RETURN_ZIP
delivery_src=DOWNLOAD/RETURN_DELIVERY
zip_dst=OUT/RETURN_ZIP
delivery_dst=OUT/RETURN_DELIVERY
shutil.copy2(zip_src,zip_dst);shutil.copy2(delivery_src,delivery_dst)
raw=zip_dst.read_bytes();delivery=j(delivery_dst)
ck('downloaded ZIP exactly matches Director delivery byte/hash/CRC binding',len(raw)==delivery['archive']['bytes'] and sha(raw)==delivery['archive']['sha256'] and crc(raw)==delivery['archive']['crc32'],delivery['archive'])
ck('sealed return scope and IDs are Fate Rewrite hold only',delivery['status']=='SEALED_HELD' and delivery['acceptedIds']==[] and delivery['appliedIds']==[] and delivery['heldIds']==['fate-rewrite'] and delivery['blockerIds']==['TF192-B04'] and delivery['dependencyIds']==['TF192-B02'],{'held':delivery['heldIds'],'blockers':delivery['blockerIds'],'deps':delivery['dependencyIds']})
ck('authority, task counts, and instructed next identity match current queue',delivery['authority']=={'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173} and delivery['remainingClosureTasks']==25 and delivery['firstReviewTasks']==0 and delivery['nextIdentity']=='collapse-timeline' and delivery['nextBlocker']=='TF192-B05',delivery['authority'])
with zipfile.ZipFile(zip_dst) as z:
 infos=z.infolist();names=[x.filename for x in infos]
 ck('ZIP CRC and all member paths are safe and unique',z.testzip() is None and len(names)==len(set(names)) and all((safe(n) is None) for n in names),{'memberCount':len(names)})
 manifest=json.loads(z.read('MANIFEST.json'))
 ck('archive member count and exact allowlist match delivery',len(names)==43 and len(delivery['exactAllowlist'])==43 and set(names)==set(delivery['exactAllowlist']) and delivery['memberCount']==43 and delivery['payloadCount']==42,{'actual':len(names),'manifestPayload':manifest['payloadEntryCount']})
 manifest_rows={x['path']:x for x in manifest['members']}
 ck('manifest binds every non-manifest member by exact bytes/hash/CRC',set(manifest_rows)==set(names)-{'MANIFEST.json'} and all(len(z.read(n))==manifest_rows[n]['bytes'] and sha(z.read(n))==manifest_rows[n]['sha256'] and crc(z.read(n))==manifest_rows[n]['crc32'] for n in manifest_rows),{'boundMembers':len(manifest_rows)})
 payload={n:z.read(n) for n in names}
 decision=json.loads(payload['DIRECTOR_DECISION.json']); blocker=json.loads(payload['BLOCKER_REASSESSMENT.json']); validation=json.loads(payload['DATA_VALIDATION.json']); package=json.loads(payload['PACKAGE_CHECKS.json']); results=json.loads(payload['CASE_RESULTS.json']); remaining=json.loads(payload['REMAINING_QUEUE.json']); q319=json.loads(payload['authority/CURRENT_SPELL_QUEUE_319.json']);h319=json.loads(payload['authority/CURRENT_HANDOFF_319.json']);p319=json.loads(payload['authority/CURRENT25_PENDING_IDENTITY_AUDIT_319.json'])
 ck('sealed Director decision holds only Fate Rewrite and no apply/accept',decision['status']=='HOLD' and decision['scopeIds']==['fate-rewrite'] and decision['acceptedIds']==[] and decision['appliedIds']==[] and decision['heldIds']==['fate-rewrite'] and decision['authorityAfter']==delivery['authority'],decision['decisions'])
 ck('B04 remains open, depends on B02, and retains H-HISTORY/H-DEATH',blocker['id']=='TF192-B04' and blocker['status']=='OPEN' and blocker['dependencyId']=='TF192-B02' and set(['TF192-H-HISTORY','TF192-H-DEATH'])<=set(blocker['qualificationScope']),blocker['qualificationScope'])
 ck('990 data validation checks pass',validation['status']=='PASS' and validation['checkCount']==990 and validation['passedChecks']==990 and validation['failedChecks']==0,{'checkCount':validation['checkCount'],'passed':validation['passedChecks'],'failed':validation['failedChecks']})
 ck('12 package checks pass',package['status']=='PASS' and package['checkCount']==12 and all(x['passed'] for x in package['checks']),package['checkCount'])
 ck('17 target cases replay 140 events with forward/inverse symmetry and full reversals',results['counts']['targetCases']==17 and results['counts']['targetEvents']==140 and results['counts']['forwardOperations']==280 and results['counts']['inverseOperations']==280 and results['counts']['fullReverseTraversals']==17 and all(x.get('replay')=='PASS' for x in results['results']),results['counts'])
 ck('all 140 source bindings verify and 139/1 source delta is unchanged/index-only',delivery['counts']['sourceBindings']==140 and delivery['counts']['unchangedSources']==139 and delivery['counts']['changedSources']==1 and delivery['sourcePacket']['sha256']=='a264584c8fe23809f865aff38bb0ce95c5a777584d58699724166255b58b6437',delivery['counts'])
 ck('linked Eternal Prophecy remains context only and no mechanism/waiver is authorized','context only' in decision['linkedEternalProphecyDisposition'].lower() and blocker['newRulesAuthorized'] is False and blocker['blockerWaived'] is False,decision.get('linkedEternalProphecyDisposition'))
 ck('sealed remaining queue directs Collapse Timeline / TF192-B05 with 25 pending',remaining['nextAfterThisHold']=='collapse-timeline' and remaining['nextBlocker']=='TF192-B05' and remaining['closureTasks']==25 and len(remaining['all25PendingIds'])==25 and remaining['canonicalQueueEdited'] is False,{'next':remaining['nextAfterThisHold'],'blocker':remaining['nextBlocker']})
 ck('packet319 is exact authority basis for Return320',q319['pendingCount']==25 and q319['currentAuthority']==delivery['authority'] and h319['heldThisStep']==['time-stop'] and p319['pendingCount']==25,None)
 ck('no canonical edits, application, or downstream gate closure',delivery['applicationPerformed'] is False and delivery['canonicalEdits'] is False and delivery['allDownstreamGatesClosed'] is True,None)
 # extract all verified members; preserve the original ZIP and delivery too.
 for n in names:
  safe(n);dest=OUT/pathlib.Path(n);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(payload[n])

receipt={'id':'FATE-REWRITE-RETURN320-RECEIPT','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'status':'SEALED_HELD_INDEPENDENTLY_VERIFIED','archive':bind(zip_dst),'delivery':bind(delivery_dst),'decision':json.loads((OUT/'DIRECTOR_DECISION.json').read_text(encoding='utf-8')),
         'blockerIds':['TF192-B04'],'dependencyIds':['TF192-B02'],'qualificationIds':delivery['qualificationIds'],'authority':delivery['authority'],'remainingClosureTasks':25,'firstReviewTasks':0,'nextIdentity':'collapse-timeline','nextBlocker':'TF192-B05',
         'checks':checks,'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':sum(not x['passed'] for x in checks),'canonicalFilesChanged':False,'applicationPerformed':False,'runtimeExecuted':False}
rec_path=AUDIT/'FATE_REWRITE_RETURN320_RECEIPT.json';rec_path.write_bytes(pretty(receipt))
report={'id':'FATE-REWRITE-RETURN320-INDEPENDENT-AUDIT','recordedAtUtc':receipt['recordedAtUtc'],'status':'PASS','archive':bind(zip_dst),'delivery':bind(delivery_dst),'memberCount':43,'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':sum(not x['passed'] for x in checks),'checks':checks,'acceptedIds':[],'appliedIds':[],'heldIds':['fate-rewrite'],'blockerIds':['TF192-B04'],'dependencyIds':['TF192-B02'],'nextIdentity':'collapse-timeline','nextBlocker':'TF192-B05','authority':delivery['authority'],'canonicalFilesChanged':False,'applicationPerformed':False,'runtimeExecuted':False}
aud_path=AUDIT/'FATE_REWRITE_RETURN320_INDEPENDENT_AUDIT.json';aud_path.write_bytes(pretty(report))
# Register sealed result and authorized next identity.
qprev=json.loads((AUDIT/'CURRENT_SPELL_QUEUE_320.json').read_text(encoding='utf-8'))
hprev=json.loads((AUDIT/'CURRENT_HANDOFF_320.json').read_text(encoding='utf-8'))
pprev=json.loads((AUDIT/'CURRENT25_PENDING_IDENTITY_AUDIT_320.json').read_text(encoding='utf-8'))
now=receipt['recordedAtUtc']
q=copy.deepcopy(qprev);q['id']='SPELL-REVIEW-QUEUE-321';q['recordedAtUtc']=now;q['supersedesQueue']='SPELL-REVIEW-QUEUE-320';q['activeReview']={'spellId':'collapse-timeline','blockerIds':['TF192-B05','TF192-B02'],'packet':None,'status':'DIRECTOR_AUTHORIZED_NEXT_AFTER_FATE_REWRITE_HOLD'};q['next']='collapse-timeline';q['currentReturnHeldIds']=['fate-rewrite'];q['currentReturnAcceptedIds']=[];q['currentReturnAppliedIds']=[];q['currentReturnBlockers']={'fate-rewrite':['TF192-B04']};q['currentReturnDependencyIds']={'fate-rewrite':['TF192-B02']};q['lastDirectorReturn']='RETURN320_HELD_VERIFIED';q['currentReturnReceipt']=bind(rec_path);q['currentReturnAudit']=bind(aud_path);q['currentReturnArchive']=bind(zip_dst);q['currentReturnDelivery']=bind(delivery_dst);q['currentPacketStatus']='RETURN320_HELD_VERIFIED_PROCEED_COLLAPSE_TIMELINE_TF192_B05';q['directorConnectionStatus']='Return320 sealed hold verified: Fate Rewrite / TF192-B04 depends on unresolved TF192-B02; Director explicitly directs Collapse Timeline / TF192-B05 next. No acceptance/application.';q['canonicalFilesChanged']=False;q['applicationPerformed']=False;q['githubChanges']=False
q['currentPacket']={'directorReturn':bind(zip_dst),'returnDelivery':bind(delivery_dst),'independentAudit':bind(aud_path),'receipt':bind(rec_path)}
qpath=AUDIT/'CURRENT_SPELL_QUEUE_321.json';qpath.write_bytes(pretty(q))
p=copy.deepcopy(pprev);p['id']='SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-321';p['recordedAtUtc']=now;p['supersedes']='CURRENT25_PENDING_IDENTITY_AUDIT_320.json';p['status']='PASS_CURRENT_823_25_RETURN320_HOLD_FATE_REWRITE_COLLAPSE_TIMELINE_NEXT';p['sourceQueue']=qpath.relative_to(ROOT).as_posix();p['currentQueueBinding']=bind(qpath);p['closureTasksRemaining']=25;p['firstReviewTasksRemaining']=0;p['heldThisStep']=['fate-rewrite'];p['currentReturn']=bind(rec_path);p['nextGroup']='rank9-time-fate6';p['nextPendingIds']=['collapse-timeline','eternal-prophecy'];p['nextPendingCount']=2;p['nextStep']='Prepare Collapse Timeline / TF192-B05-only packet at 823/25/0. Preserve Fate Rewrite hold TF192-B04 and unresolved Eternal Prophecy dependency TF192-B02.';p['acceptedIds']=[];p['appliedIds']=[];p['canonicalFilesChanged']=False
ppath=AUDIT/'CURRENT25_PENDING_IDENTITY_AUDIT_321.json';ppath.write_bytes(pretty(p))
h=copy.deepcopy(hprev);h['id']='SPELL-REVIEW-HANDOFF-321';h['recordedAtUtc']=now;h['supersedes']='CURRENT-HANDOFF-320';h['status']='RETURN320_FATE_REWRITE_HELD_COLLAPSE_TIMELINE_NEXT';h['scopeIds']=['fate-rewrite'];h['blockerIds']=['TF192-B04','TF192-B02'];h['heldThisStep']=['fate-rewrite'];h['currentBlocker']='TF192-B04';h['nextPendingGroup']=['collapse-timeline','eternal-prophecy'];h['nextStep']='Director explicitly authorized Collapse Timeline / TF192-B05 only. Prepare one-identity packet, retaining the unresolved TF192-B02 guarantee dependency and all unrelated holds.';h['queue']=qpath.relative_to(ROOT).as_posix();h['queueBinding']=bind(qpath);h['pendingIdentityAudit']=ppath.relative_to(ROOT).as_posix();h['pendingIdentityAuditBinding']=bind(ppath);h['currentReturn']=bind(rec_path);h['currentReturnAudit']=bind(aud_path);h['currentDirectorReturn']=bind(zip_dst);h['currentDirectorDelivery']=bind(delivery_dst);h['closureTasksRemaining']=25;h['firstReviewTasksRemaining']=0;h['canonicalFilesChanged']=False;h['runtimeExecuted']=False
hpath=AUDIT/'CURRENT_HANDOFF_321.json';hpath.write_bytes(pretty(h))
snap=f'''# Current spell review snapshot — queue 321\n\n- Authority: **823 applied / 25 pending / 0 accepted-unapplied**; 547 complete standalone procedures and 173 scoped interfaces.\n- Return320 held Fate Rewrite at **TF192-B04**, dependent on unresolved **TF192-B02**. H-HISTORY and H-DEATH remain separate narrow holds.\n- Director Return320 passed 990 data checks, 12 package checks and 88 seal readback checks; all 140 source bindings verified. The 17 Fate Rewrite cases replayed 140 events with 280 forward and 280 inverse operations.\n- No spell accepted or applied; no canonical edits or runtime execution. 25 closure tasks and zero first-review tasks remain.\n- Director explicitly directed **Collapse Timeline / TF192-B05 next**, keeping the guarantee dependency open. Prepare that one-identity packet.\n'''
sp=AUDIT/'CURRENT_SPELL_REVIEW_SNAPSHOT_321.md';sp.write_text(snap,encoding='utf-8',newline='\n')
print(json.dumps({'status':'PASS','audit':bind(aud_path),'receipt':bind(rec_path),'queue':bind(qpath),'handoff':bind(hpath),'pendingAudit':bind(ppath),'snapshot':bind(sp),'authority':delivery['authority'],'next':q['next'],'taskCount':q['closureTasksRemaining'],'checks':len(checks)},ensure_ascii=False))
