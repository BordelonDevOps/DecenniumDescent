from __future__ import annotations
import copy, hashlib, json, pathlib, shutil, zipfile, zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
DOWNLOADS = pathlib.Path(r'C:\Users\cbord\Downloads')
OUT = AUDIT / 'rank9_collapse_timeline_return322_received'
ZIP_NAME = 'DD_Rank9_CollapseTimeline_Director_Return322_HELD.zip'
DELIVERY_NAME = 'DD_Rank9_CollapseTimeline_Director_Return322_HELD_DELIVERY.json'
AUTHORITY = {'reviewedApplied': 823, 'pending': 25, 'acceptedUnapplied': 0,
             'completeStandaloneProcedures': 547, 'scopedInterfaces': 173}

def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b) & 0xffffffff:08x}'
def pretty(o): return (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
def bind(p):
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'bytes': len(b), 'sha256': sha(b), 'crc32': crc(b)}
def readj(p): return json.loads(p.read_text(encoding='utf-8'))
def safe(n):
    q = pathlib.PurePosixPath(n)
    if not n or q.is_absolute() or '..' in q.parts or '\\' in n: raise ValueError(n)

checks = []
def ck(name, ok, detail=None):
    checks.append({'check': name, 'passed': bool(ok), 'detail': detail})
    if not ok: raise AssertionError(f'{name}: {detail}')

OUT.mkdir(parents=True, exist_ok=True)
for name in (ZIP_NAME, DELIVERY_NAME):
    src, dst = DOWNLOADS / name, OUT / name
    if not src.is_file(): raise FileNotFoundError(src)
    if dst.exists() and dst.read_bytes() != src.read_bytes(): raise RuntimeError(f'download differs: {dst}')
    if not dst.exists(): shutil.copyfile(src, dst)
zip_path, delivery_path = OUT / ZIP_NAME, OUT / DELIVERY_NAME
delivery, raw = readj(delivery_path), zip_path.read_bytes()
ck('outer archive matches sealed bytes/SHA-256/CRC32', len(raw) == delivery['archive']['bytes'] and sha(raw) == delivery['archive']['sha256'] and crc(raw) == delivery['archive']['crc32'], delivery['archive'])
ck('sealed scope holds only Collapse Timeline, with no acceptance/application', delivery['status'] == 'SEALED_HELD' and delivery['acceptedIds'] == [] and delivery['appliedIds'] == [] and delivery['heldIds'] == ['collapse-timeline'] and delivery['blockerIds'] == ['TF192-B05'] and delivery['dependencyIds'] == ['TF192-B02'], {k: delivery.get(k) for k in ('status','acceptedIds','appliedIds','heldIds','blockerIds','dependencyIds')})
ck('authority, task counts and next identity match current queue', delivery['authority'] == AUTHORITY and delivery['remainingClosureTasks'] == 25 and delivery['firstReviewTasks'] == 0 and delivery['nextIdentity'] == 'eternal-prophecy' and delivery['nextBlocker'] == 'TF192-B02' and delivery['canonicalEdits'] is False and delivery['applicationPerformed'] is False, {k: delivery.get(k) for k in ('authority','remainingClosureTasks','firstReviewTasks','nextIdentity','nextBlocker')})

with zipfile.ZipFile(zip_path) as z:
    names = [i.filename for i in z.infolist()]
    for n in names: safe(n)
    ck('ZIP CRC, paths, unique names and exact allowlist pass', z.testzip() is None and len(names) == len(set(names)) == delivery['memberCount'] == 43 and set(names) == set(delivery['exactAllowlist']), {'members': len(names)})
    mm = {x['path']: x for x in delivery['members']}
    ck('delivery manifest binds every member by exact bytes/SHA/CRC', set(mm) == set(names) and all(len(z.read(n)) == mm[n]['bytes'] and sha(z.read(n)) == mm[n]['sha256'] and crc(z.read(n)) == mm[n]['crc32'] for n in names), {'bound': len(mm)})
    manifest = json.loads(z.read('MANIFEST.json'))
    im = {x['path']: x for x in manifest['members']}
    ck('inner manifest binds all 42 non-manifest members', manifest['payloadEntryCount'] == 42 and set(im) == set(names)-{'MANIFEST.json'} and all(len(z.read(n)) == im[n]['bytes'] and sha(z.read(n)) == im[n]['sha256'] and crc(z.read(n)) == im[n]['crc32'] for n in im), {'bound': len(im)})
    payload = {n: z.read(n) for n in names}
    d = json.loads(payload['DIRECTOR_DECISION.json']); b = json.loads(payload['BLOCKER_REASSESSMENT.json'])
    v = json.loads(payload['DATA_VALIDATION.json']); pck = json.loads(payload['PACKAGE_CHECKS.json'])
    r = json.loads(payload['CASE_RESULTS.json']); rem = json.loads(payload['REMAINING_QUEUE.json'])
    sem = json.loads(payload['INDEPENDENT_SEMANTIC_FAILURE_CHECK.json'])
    q321 = json.loads(payload['authority/CURRENT_SPELL_QUEUE_321.json'])
    h321 = json.loads(payload['authority/CURRENT_HANDOFF_321.json'])
    a321 = json.loads(payload['authority/CURRENT25_PENDING_IDENTITY_AUDIT_321.json'])
    ck('inner decision holds only Collapse Timeline at B05', d['status'] == 'HOLD' and d['scopeIds'] == ['collapse-timeline'] and d['acceptedIds'] == [] and d['appliedIds'] == [] and d['heldIds'] == ['collapse-timeline'] and d['authorityAfter'] == AUTHORITY and d['nextIdentity'] == 'eternal-prophecy' and d['nextBlocker'] == 'TF192-B02', d)
    ck('B05 missing-witness and out-of-scope holds are preserved', b['id'] == 'TF192-B05' and b['status'] == 'OPEN' and b['dependencyIds'] == ['TF192-B02'] and b['newMechanismAuthorized'] is False and b['promiseQualified'] is False and b['waiver'] is False and set(['TF192-B02','TF192-B04']).issubset(set(delivery['preservedOutsideScopeBlockerIds'])) and 'TF192-H-HISTORY' in b['preservedConditionalQualification'], {'blocker': b['id'], 'dependencies': b['dependencyIds'], 'preserved': delivery['preservedOutsideScopeBlockerIds']})
    ck('1,102 data checks pass', v['status'] == 'PASS' and v['checkCount'] == v['passedChecks'] == delivery['dataCheckCount'] == 1102 and v['failedChecks'] == 0, {'checks': v['checkCount'], 'passed': v['passedChecks'], 'failed': v['failedChecks']})
    ck('12 package checks pass', pck['status'] == 'PASS' and pck['checkCount'] == delivery['packageConsistencyCheckCount'] == 12 and all(x['passed'] for x in pck['checks']), {'count': pck['checkCount']})
    c = r['counts']
    ck('17 target cases replay 156 events and 312 forward/inverse operations', c['targetCases'] == 17 and c['targetEvents'] == 156 and c['forwardOperations'] == c['inverseOperations'] == 312 and c['fullReverseTraversals'] == 17 and all(x.get('replay') == 'PASS' for x in r['results']), c)
    ck('140 source bindings verify with 139 unchanged and one index-only delta', c['sourceBindings'] == 140 and c['unchangedSources'] == 139 and c['changedSources'] == 1 and delivery['sourcePacket']['sha256'] == '2d3bd8e3101b5f46acc17aa72a8416ac3c61b17dd2eb4ac3ebcecdfdfabc5685', c)
    ck('Eternal Prophecy remains context-only and B02 stays open', c['linkedContextCasesByteVerifiedOnly'] == 14 and b['newMechanismAuthorized'] is False and sem['dependencyIds'] == ['TF192-B02'] and sem['numericReplayNotSemanticCompletion'] is True, {'contextCases': c['linkedContextCasesByteVerifiedOnly'], 'dependencies': sem['dependencyIds']})
    ck('all 25 pending identities remain and next is Eternal Prophecy/B02', rem['nextAfterThisHold'] == 'eternal-prophecy' and rem['nextBlocker'] == 'TF192-B02' and rem['closureTasks'] == 25 and len(rem['all25PendingIds']) == 25 and rem['canonicalQueueEdited'] is False, {'next': rem['nextAfterThisHold'], 'blocker': rem['nextBlocker']})
    ck('embedded authority inputs match queue321 and explicit prior next', q321['currentAuthority'] == AUTHORITY and q321['pendingCount'] == 25 and h321['authority'] == AUTHORITY and a321['pendingCount'] == 25 and q321['next'] == 'collapse-timeline', {'queue': q321['id'], 'handoff': h321['id'], 'audit': a321['id']})
    for n, content in payload.items():
        dst = OUT / pathlib.Path(*pathlib.PurePosixPath(n).parts)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and dst.read_bytes() != content: raise RuntimeError(f'extracted bytes mismatch: {dst}')
        if not dst.exists(): dst.write_bytes(content)

now = datetime.now(timezone.utc).isoformat(timespec='seconds')
receipt = {'id':'COLLAPSE-TIMELINE-RETURN322-RECEIPT','recordedAtUtc':now,'status':'SEALED_HELD_INDEPENDENTLY_VERIFIED','archive':bind(zip_path),'delivery':bind(delivery_path),'decision':readj(OUT/'DIRECTOR_DECISION.json'),'acceptedIds':[],'appliedIds':[],'heldIds':['collapse-timeline'],'blockerIds':['TF192-B05'],'dependencyIds':['TF192-B02'],'preservedOutsideScopeBlockerIds':['TF192-B02','TF192-B04'],'authority':AUTHORITY,'remainingClosureTasks':25,'firstReviewTasks':0,'nextIdentity':'eternal-prophecy','nextBlocker':'TF192-B02','checks':checks,'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':sum(not x['passed'] for x in checks),'canonicalFilesChanged':False,'applicationPerformed':False,'runtimeExecuted':False}
receipt_path = AUDIT/'COLLAPSE_TIMELINE_RETURN322_RECEIPT.json'; receipt_path.write_bytes(pretty(receipt))
audit = {'id':'COLLAPSE-TIMELINE-RETURN322-INDEPENDENT-AUDIT','recordedAtUtc':now,'status':'PASS','archive':bind(zip_path),'delivery':bind(delivery_path),'memberCount':43,'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':sum(not x['passed'] for x in checks),'checks':checks,'acceptedIds':[],'appliedIds':[],'heldIds':['collapse-timeline'],'blockerIds':['TF192-B05'],'dependencyIds':['TF192-B02'],'nextIdentity':'eternal-prophecy','nextBlocker':'TF192-B02','authority':AUTHORITY,'canonicalFilesChanged':False,'applicationPerformed':False,'runtimeExecuted':False}
audit_path = AUDIT/'COLLAPSE_TIMELINE_RETURN322_INDEPENDENT_AUDIT.json'; audit_path.write_bytes(pretty(audit))

qprev = readj(AUDIT/'CURRENT_SPELL_QUEUE_322.json'); hprev = readj(AUDIT/'CURRENT_HANDOFF_322.json'); pprev = readj(AUDIT/'CURRENT25_PENDING_IDENTITY_AUDIT_322.json')
q = copy.deepcopy(qprev)
q.update({'id':'SPELL-REVIEW-QUEUE-323','recordedAtUtc':now,'supersedesQueue':'SPELL-REVIEW-QUEUE-322','nextPendingIds':['eternal-prophecy'],'nextPendingCount':1,'activeReview':{'spellId':'eternal-prophecy','blockerIds':['TF192-B02'],'packet':None,'status':'DIRECTOR_AUTHORIZED_NEXT_AFTER_COLLAPSE_TIMELINE_HOLD'},'next':'eternal-prophecy','lastDirectorReturn':'RETURN322_HELD_VERIFIED','currentReturnAcceptedIds':[],'currentReturnAppliedIds':[],'currentReturnHeldIds':['collapse-timeline'],'currentReturnBlockers':{'collapse-timeline':['TF192-B05']},'currentReturnDependencyIds':{'collapse-timeline':['TF192-B02']},'currentReturnArchive':bind(zip_path),'currentReturnDelivery':bind(delivery_path),'currentReturnAudit':bind(audit_path),'currentReturnReceipt':bind(receipt_path),'currentReturnDecision':bind(OUT/'DIRECTOR_DECISION.json'),'currentPacketStatus':'RETURN322_HELD_VERIFIED_PROCEED_ETERNAL_PROPHECY_TF192_B02','pendingIdentityAudit':'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT25_PENDING_IDENTITY_AUDIT_323.json','directorConnectionStatus':'Return322 verified: Collapse Timeline/B05 remains held and dependent on B02. Director explicitly directs Eternal Prophecy/B02 next. Fate Rewrite/B04 and H-HISTORY remain preserved; no acceptance/application.','githubChanges':False,'canonicalFilesChanged':False,'applicationPerformed':False,'currentPacket':{'directorReturn':bind(zip_path),'returnDelivery':bind(delivery_path),'independentAudit':bind(audit_path),'receipt':bind(receipt_path)},'acceptedThisStep':[],'appliedThisStep':[],'currentDirectorInstruction':'Review Eternal Prophecy / TF192-B02 only, as directed by Return322; preserve Collapse Timeline B05, Fate Rewrite B04 and H-HISTORY without implied acceptance or promise weakening.'})
qpath = AUDIT/'CURRENT_SPELL_QUEUE_323.json'; qpath.write_bytes(pretty(q))
pending = copy.deepcopy(pprev)
pending.update({'id':'SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-323','recordedAtUtc':now,'supersedes':'CURRENT25_PENDING_IDENTITY_AUDIT_322.json','status':'PASS_CURRENT_823_25_RETURN322_HOLD_COLLAPSE_TIMELINE_ETERNAL_PROPHECY_NEXT','sourceQueue':qpath.relative_to(ROOT).as_posix(),'currentQueueBinding':bind(qpath),'heldThisStep':['collapse-timeline'],'currentReturn':bind(receipt_path),'nextPendingIds':['eternal-prophecy'],'nextPendingCount':1,'nextStep':'Prepare Eternal Prophecy / TF192-B02-only current-authority packet at 823/25/0. Preserve Collapse Timeline / TF192-B05 and Fate Rewrite / TF192-B04; retain exact external/parent history holds.','acceptedIds':[],'appliedIds':[],'canonicalFilesChanged':False})
ppath = AUDIT/'CURRENT25_PENDING_IDENTITY_AUDIT_323.json'; ppath.write_bytes(pretty(pending))
h = copy.deepcopy(hprev)
h.update({'id':'SPELL-REVIEW-HANDOFF-323','recordedAtUtc':now,'supersedes':'CURRENT-HANDOFF-322','status':'RETURN322_COLLAPSE_TIMELINE_HELD_ETERNAL_PROPHECY_NEXT','scopeIds':['collapse-timeline'],'blockerIds':['TF192-B05','TF192-B02','TF192-B04','TF192-H-HISTORY'],'heldThisStep':['collapse-timeline'],'currentBlocker':'TF192-B05','nextPendingGroup':['eternal-prophecy'],'nextStep':'Director explicitly directed Eternal Prophecy / TF192-B02 only. Prepare its one-identity packet while preserving Collapse Timeline B05, Fate Rewrite B04 and H-HISTORY.','queue':qpath.relative_to(ROOT).as_posix(),'queueBinding':bind(qpath),'pendingIdentityAudit':ppath.relative_to(ROOT).as_posix(),'pendingIdentityAuditBinding':bind(ppath),'currentReturn':bind(receipt_path),'currentReturnAudit':bind(audit_path),'currentDirectorReturn':bind(zip_path),'currentDirectorDelivery':bind(delivery_path),'closureTasksRemaining':25,'firstReviewTasksRemaining':0,'canonicalFilesChanged':False,'runtimeExecuted':False})
hpath = AUDIT/'CURRENT_HANDOFF_323.json'; hpath.write_bytes(pretty(h))
snapshot = f'''# Current spell review snapshot — queue 323\n\n- Authority: **823 applied / 25 pending / 0 accepted-unapplied**; 547 complete standalone procedures and 173 scoped interfaces.\n- Return322 independently verified and sealed **Collapse Timeline held at TF192-B05**. Missing evidence is a source-complete paid committed guarantee, exact affected external/parent histories, and compatible plus rejected-incompatible future branches preserving payments, actors, clocks, custody and the original objective/deadline.\n- Director Return322 passed 1,102 data checks and 12 package checks; all 140 source bindings verified. The 17 target cases replayed 156 events with 312 forward and 312 inverse operations; replay did not close the semantic gap.\n- No acceptance, application, canonical edits or runtime execution. **TF192-B02, Fate Rewrite / TF192-B04, and TF192-H-HISTORY remain open.** 25 closure tasks and zero first-review tasks remain.\n- Director explicitly directed **Eternal Prophecy / TF192-B02 next**. Prepare that one-identity packet; preserve the exact unresolved guarantee dependency.\n'''
sp = AUDIT/'CURRENT_SPELL_REVIEW_SNAPSHOT_323.md'; sp.write_text(snapshot,encoding='utf-8',newline='\n')
print(json.dumps({'status':'PASS','audit':bind(audit_path),'receipt':bind(receipt_path),'queue':bind(qpath),'handoff':bind(hpath),'pendingAudit':bind(ppath),'snapshot':bind(sp),'checks':len(checks),'next':q['next'],'authority':AUTHORITY},ensure_ascii=False))
