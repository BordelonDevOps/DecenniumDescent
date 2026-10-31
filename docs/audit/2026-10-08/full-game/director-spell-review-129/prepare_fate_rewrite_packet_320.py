from __future__ import annotations
import gzip, hashlib, json, pathlib, zipfile, zlib
from datetime import datetime, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
OUT = AUDIT / 'rank9_fate_rewrite_current_source_320_prepared'
BASELINE = AUDIT / 'rank9_timefate6_current_source_282_prepared' / 'DD_Rank9_TimeFate6_CurrentSource_282.zip'
RETURN282 = AUDIT / 'rank9_timefate6_return282_received' / 'DD_Rank9_TimeFate6_Director_Return282_HELD.zip'
CURRENT = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE = AUDIT / 'CURRENT_SPELL_QUEUE_319.json'
HANDOFF = AUDIT / 'CURRENT_HANDOFF_319.json'
PENDING = AUDIT / 'CURRENT25_PENDING_IDENTITY_AUDIT_319.json'
TIME_STOP_RETURN = AUDIT / 'rank9_time_stop_return318_received' / 'DD_Rank9_TimeStop_Director_Return318_HELD.zip'
TIME_STOP_CONTRACT = AUDIT / 'rank9_time_stop_return318_received' / 'TF318_JOINT_INTERFACE_CONTRACT.md'


def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()
def crc(raw: bytes) -> str: return f'{zlib.crc32(raw) & 0xffffffff:08x}'
def canonical(obj: Any) -> bytes: return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def pretty(obj: Any) -> bytes: return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
def bind(path: pathlib.Path, display: str | None = None) -> dict[str, Any]:
    raw = path.read_bytes(); return {'path': display or path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': sha(raw), 'crc32': crc(raw)}
def j(raw: bytes) -> Any: return json.loads(raw)
def safe(name: str) -> None:
    q = pathlib.PurePosixPath(name)
    if not name or q.is_absolute() or '..' in q.parts or '\\' in name: raise ValueError(f'unsafe archive member: {name}')
def add(members: dict[str, bytes], name: str, raw: bytes) -> None:
    safe(name)
    if name in members: raise ValueError(f'duplicate member: {name}')
    members[name] = raw
def addj(members: dict[str, bytes], name: str, value: Any) -> None: add(members, name, pretty(value))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.iterdir():
        if p.is_file(): p.unlink()
        else: raise RuntimeError(f'unexpected nested output: {p}')
    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index, catalog = j(index_raw), j(catalog_raw)
    queue, handoff, pending = (j(p.read_bytes()) for p in [QUEUE, HANDOFF, PENDING])
    with zipfile.ZipFile(BASELINE) as z:
        baseline_candidate_raw = z.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json')
        baseline_manifest = j(z.read('MANIFEST.json'))
        baseline_candidate = j(baseline_candidate_raw)
    baseline_archive_binding = bind(BASELINE)
    old_bindings = baseline_candidate['sourceBindings']
    if len(old_bindings) != 140: raise AssertionError(f'expected Packet282 140 bindings, got {len(old_bindings)}')
    manifest_members = {x['path']: x for x in baseline_manifest['members']}
    comparisons, changed = [], []
    for row in old_bindings:
        rel = row['path']; path = ROOT / pathlib.Path(rel)
        if not path.is_file():
            comparisons.append({'path': rel, 'oldBytes': row['bytes'], 'oldSha256': row['sha256'], 'status': 'MISSING'})
            changed.append(rel); continue
        raw = path.read_bytes(); current_sha = sha(raw)
        status = 'UNCHANGED' if len(raw) == row['bytes'] and current_sha == row['sha256'] else 'CHANGED'
        member = 'sources_current/' + rel
        archived = manifest_members.get(member)
        if not archived or archived['bytes'] != row['bytes'] or archived['sha256'] != row['sha256']:
            raise AssertionError(f'baseline source member not bound: {rel}')
        comparisons.append({'path': rel, 'oldBytes': row['bytes'], 'oldSha256': row['sha256'], 'currentBytes': len(raw), 'currentSha256': current_sha, 'status': status,
                            'unchangedBinding': {'archive': baseline_archive_binding, 'member': member} if status == 'UNCHANGED' else None})
        if status != 'UNCHANGED': changed.append(rel)
    expected_changed = ['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json']
    if changed != expected_changed: raise AssertionError(f'unexpected source delta: {changed}')
    current_bindings = [bind(INDEX), bind(CATALOG)]

    with zipfile.ZipFile(RETURN282) as z:
        proc_raw = z.read('procedures/fate-rewrite.json')
        ep_raw = z.read('procedures/eternal-prophecy.json')
        hold_raw = z.read('HOLD_REGISTER.json')
        casebook_gz = z.read('CASEBOOK.json.gz')
        decision_raw = z.read('DIRECTOR_DECISION.json')
        qdisp_raw = z.read('QUESTION_DISPOSITIONS.json')
        source_binding_raw = z.read('SOURCE_BINDING.json')
        target_rows_raw = z.read('evidence/CURRENT_TARGET_ROWS.json')
        notes_raw = z.read('evidence/ORIGINAL_CONFERENCE_NOTES_129.json')
        temporal_review_raw = z.read('evidence/current/TEMPORAL_REFERENCE_TRANSACTION_REVIEW_STATUS.json')
    proc, ep, holds = j(proc_raw), j(ep_raw), j(hold_raw)
    casebook = j(gzip.decompress(casebook_gz))
    cases_all = casebook.get('cases', [])
    fate_cases = [c for c in cases_all if c.get('spellId') == 'fate-rewrite']
    ep_cases = [c for c in cases_all if c.get('spellId') == 'eternal-prophecy']
    if [c['id'] for c in fate_cases] != proc['caseIds'] or len(fate_cases) != 17: raise AssertionError('Return282 FRewrite case list does not match its exact 17 procedure IDs')
    if [c['id'] for c in ep_cases] != ep['caseIds']: raise AssertionError('Return282 Eternal Prophecy case list does not match its procedure IDs')
    blockers = {x['id']: x for x in holds['currentBlockers'] if x['id'] in {'TF192-B02','TF192-B04'}}
    if set(blockers) != {'TF192-B02','TF192-B04'}: raise AssertionError('missing B02/B04 blocker evidence')
    target_rows = j(target_rows_raw)
    frow = next(x for x in catalog['spells'] if x.get('id') == 'fate-rewrite')
    erow = next(x for x in catalog['spells'] if x.get('id') == 'eternal-prophecy')
    findex = next(x for x in index['entries'] if x.get('id') == 'fate-rewrite')
    eindex = next(x for x in index['entries'] if x.get('id') == 'eternal-prophecy')
    if proc.get('blockerIds') != ['TF192-B04'] or ep.get('blockerIds') != ['TF192-B02']: raise AssertionError('spell procedure blocker IDs changed')

    candidate_proc_path = CURRENT / 'procedures/fate-rewrite.json'
    candidate_ep_path = CURRENT / 'procedures/eternal-prophecy.json'
    candidate_proc_raw, candidate_ep_raw = candidate_proc_path.read_bytes(), candidate_ep_path.read_bytes()
    candidate_proc, candidate_ep = j(candidate_proc_raw), j(candidate_ep_raw)
    # The local 192 proposal drafts and the later Return282 Director-reviewed procedures differ in metadata/boundary scope; bind both as distinct versions and do not relabel the draft as adjudicated.

    qids = proc['questionIds']
    qdisp = j(qdisp_raw)
    baseline_questions = [x for x in baseline_candidate.get('questions', []) if x.get('id') in qids]
    if {x['id'] for x in baseline_questions} != set(qids) - {'TIME129-ADD02'}: raise AssertionError('missing FRewrite original source questions')
    dispositions = [x for x in qdisp.get('dispositions', []) if x.get('questionId') in qids or x.get('id') in qids]
    addenda = [x for x in qdisp.get('focusedAddenda', []) if x.get('originalQuestionUnchanged', {}).get('id') == 'TIME129-ADD02']
    if not addenda: raise AssertionError('missing focused TIME129-ADD02 disposition')
    req_ids = {'TF9-CAST','TF9-REWRITE-POSITIVE','TF9-REWRITE-BOUNDARIES','TF9-PROPHECY','TF9-TEMPORAL-CONFLICT','TF9-PERSISTENCE'}
    requirements = [x for x in baseline_candidate.get('futureCaseRequirements', []) if x.get('id') in req_ids]
    if {x['id'] for x in requirements} != req_ids: raise AssertionError('missing linked FRewrite/Prophecy obligations')

    conflict = next(c for c in fate_cases if c['id'].endswith('FATE-REWRITE-B__prophecy-creation-conflict'))
    initial_obligations = conflict['initialState'].get('obligations', {})
    final_outcomes = conflict['finalState'].get('outcomes', [])
    if initial_obligations or not any(x.get('status') == 'unavailable-before-payment' and x.get('RPSpent') == 0 for x in final_outcomes):
        raise AssertionError('expected proof case is not a conditional pre-payment refusal')

    director_text = (
        'Fate Rewrite / TF192-B04 remains next, as a one-identity packet. Authority stays 823 applied / 25 pending / 0 accepted-unapplied, with 547 procedures / 173 interfaces.\n\n'
        'The exact minimum witness remains: one complete committed guarantee, with lawful creation, payment, original deadline and actual fulfillment history, followed by a useful compatible past rewrite and a conflicting rejected rewrite. Both must preserve current release-time versions, costs, unique custody, memories and all affected descendants.\n\n'
        'I authorize FR-EP-WITNESS-CONSTRUCTION-01, limited to preparing and evaluating the Fate Rewrite/Eternal Prophecy interface while both identities remain pending. Prior whole-spell acceptance of Eternal Prophecy need not precede construction of that evidence. This authorization does not supply or certify the missing guarantee mechanism.\n\n'
        'The substantive dependency remains TF192-B02: the proposed delivery mechanism does not establish the native “must come true” promise when every route and magical intervention remains prevented through the deadline, or the item/destination becomes unavailable. A successful delivery alone cannot prove that guarantee. Closing this requires either an explicitly authorized finite mechanism resolving those adverse branches within stated permissions, or explicit owner approval qualifying the native unconditional promise. No such qualification, antimagic exception, indestructibility, forced compliance or universal override is authorized here.\n\n'
        'Smallest packet: committed guarantee, completion/adverse branch, compatible rewrite, conflicting rejection, release-time validation and full reversibility. Preserve 17 existing Fate Rewrite cases and questions TF9-Q01, Q17–Q22, Q31–Q32, TIME129-ADD02. Keep TF192-H-HISTORY / TF192-H-DEATH and all separate holds. No identity accepted/applied; 25 closure tasks, zero first-review tasks; Collapse Timeline follows Fate Rewrite.'
    )
    status_record = {'id':'FATE-REWRITE-DIRECTOR-STATUS-320','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
                    'source':'visible Director response in Calibration review part 6','scopeIds':['fate-rewrite'],'blockerIds':['TF192-B04','TF192-B02'],
                    'interfaceAuthorizationId':'FR-EP-WITNESS-CONSTRUCTION-01','interfaceAuthorizationScope':'prepare/evaluate Fate Rewrite/Eternal Prophecy interface while both remain pending',
                    'exactMinimumWitness':{'guarantee':'one complete committed guarantee with lawful creation, payment, original deadline, actual fulfillment history','compatibleRewrite':'useful compatible past rewrite preserving predicate and descendants','conflictingRewrite':'conflicting rejected rewrite at correct stage','preserve':['current release-time versions','costs','unique custody','memories','all affected descendants']},
                    'authorizationDoesNotSupplyMechanism':True,'noQualificationOrUniversalOverrideAuthorized':True,
                    'authority':{'reviewedApplied':823,'pending':25,'acceptedUnapplied':0,'completeStandaloneProcedures':547,'scopedInterfaces':173},
                    'remainingClosureTasks':25,'firstReviewTasks':0,'nextAfterFateRewrite':'collapse-timeline','responseText':director_text}

    members: dict[str,bytes] = {}
    add(members,'authority/current/authored_review_index.json',index_raw)
    # Keep current catalog rows scoped, with current byte/hash bindings for the full catalog and index.
    addj(members,'authority/current/fate_rewrite_and_eternal_prophecy_rows.json',{'sourceBindings':current_bindings,
        'indexEntries':{'fate-rewrite':findex,'eternal-prophecy':eindex},'catalogRows':{'fate-rewrite':frow,'eternal-prophecy':erow}})
    for path,name in [(QUEUE,'authority/current/CURRENT_SPELL_QUEUE_319.json'),(HANDOFF,'authority/current/CURRENT_HANDOFF_319.json'),(PENDING,'authority/current/CURRENT25_PENDING_IDENTITY_AUDIT_319.json')]:
        add(members,name,path.read_bytes())
    addj(members,'evidence/source_comparison/PACKET282_140_SOURCE_BINDING_COMPARISON.json',{'baselineArchive':baseline_archive_binding,'baselineCandidate':{'member':'CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json','bytes':len(baseline_candidate_raw),'sha256':sha(baseline_candidate_raw)},
        'inventoryCount':140,'unchangedCount':sum(x['status']=='UNCHANGED' for x in comparisons),'changedCount':sum(x['status']=='CHANGED' for x in comparisons),'missingCount':sum(x['status']=='MISSING' for x in comparisons),'changedPaths':changed,'rows':comparisons,
        'policy':'Packet282 binds the 139 unchanged source files; the changed current authored index is supplied byte-exactly. No other source delta is present.'})
    add(members,'evidence/source_comparison/current_changed/authored_review_index.json',index_raw)
    addj(members,'evidence/native/current_target_rows_return282.json',{'archive':bind(RETURN282),'member':'evidence/CURRENT_TARGET_ROWS.json','rows':j(target_rows_raw)})
    add(members,'evidence/native/return282_source_binding.json',source_binding_raw)
    add(members,'evidence/native/return282_director_decision.json',decision_raw)
    add(members,'evidence/native/current_temporal_reference_review_status.json',temporal_review_raw)
    add(members,'evidence/native/original_conference_notes_129.json',notes_raw)
    add(members,'evidence/authority/return282_hold_register.json',hold_raw)
    addj(members,'evidence/authority/TF192-B02_and_TF192-B04.json',blockers)
    add(members,'evidence/fate_rewrite/return282_director_reviewed_procedure.json',proc_raw)
    add(members,'evidence/fate_rewrite/current_authored_candidate_procedure_192.json',candidate_proc_raw)
    add(members,'evidence/eternal_prophecy/return282_director_reviewed_procedure.json',ep_raw)
    add(members,'evidence/eternal_prophecy/current_authored_candidate_procedure_192.json',candidate_ep_raw)
    addj(members,'evidence/fate_rewrite/questions_obligations.json',{'sourceCandidate':{'archive':baseline_archive_binding,'member':'CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json','sha256':sha(baseline_candidate_raw),
        'baselineSourceQuestionsUnchanged':True},'questions':baseline_questions,'priorDispositions':dispositions,'focusedAddenda':addenda,'futureCaseRequirements':requirements})
    source_case_ref={'archive':bind(RETURN282),'member':'CASEBOOK.json.gz','memberBytes':len(casebook_gz),'memberSha256':sha(casebook_gz),'decodedCaseCount':len(cases_all)}
    for label,case_list in [('fate_rewrite',fate_cases),('eternal_prophecy',ep_cases)]:
        manifests=[]
        for c in case_list:
            raw=canonical(c); name=f'evidence/cases/{label}/{c["id"]}.json'; add(members,name,raw)
            manifests.append({'id':c['id'],'member':name,'bytes':len(raw),'sha256':sha(raw),'canonicalization':'UTF-8 JSON, sorted keys, compact separators, ensure_ascii=false'})
        addj(members,f'evidence/cases/{label}_manifest.json',{'caseCount':len(manifests),'procedureCaseIds':proc['caseIds'] if label=='fate_rewrite' else ep['caseIds'],'sourceCasebook':source_case_ref,'cases':manifests})
    addj(members,'evidence/director/FR_EP_WITNESS_CONSTRUCTION_01_STATUS.json',status_record)
    add(members,'evidence/director/TimeStop_Return318_HELD.zip',TIME_STOP_RETURN.read_bytes())
    add(members,'evidence/director/TF318_JOINT_INTERFACE_CONTRACT.md',TIME_STOP_CONTRACT.read_bytes())
    add(members,'evidence/director/Return282_HELD.zip',RETURN282.read_bytes())

    request = f'''# Director request: Fate Rewrite / TF192-B04 only (Packet320)\n\nPlease adjudicate only `fate-rewrite` / `TF192-B04` at current authority **823 applied / 25 pending / 0 accepted-unapplied** (547 complete standalone procedures / 173 scoped interfaces). The other identities are context only. Do not accept or apply Eternal Prophecy as part of this decision.\n\nThis packet follows your authorization `FR-EP-WITNESS-CONSTRUCTION-01`. It binds the current queue319, handoff319, pending identity audit, current authored index and catalog rows, and a fresh 140-source comparison against Packet282 (139 unchanged; only the authored review index changed). It includes the exact current Fate Rewrite and linked Eternal Prophecy procedures, the TF192-B02/B04 hold records, questions TF9-Q01, Q17–Q22, Q31–Q32 and TIME129-ADD02, six linked future-case obligations, and all 17 preserved Fate Rewrite cases plus the linked Eternal Prophecy cases.\n\nThe existing `FATE-REWRITE-B__prophecy-creation-conflict` is not the required guarantee witness: its initial `obligations` map is empty and it ends with `unavailable-before-payment`, `RPSpent: 0`. The current Eternal Prophecy procedure explicitly records `TF192-GUARANTEE-01` as unresolved when all routes and magical intervention remain prevented or the item/destination becomes unavailable. The interface authorization does not supply this mechanism. No source-complete, actually paid and fulfilled guarantee has been found in the current linked evidence.\n\nPlease confirm whether the evidence identifies any lawful current source/mechanism that closes `TF192-B02` without qualifying or overriding the native unconditional promise. If not, seal Fate Rewrite as held at TF192-B04, state the minimum missing witness, keep TF192-H-HISTORY / TF192-H-DEATH separate, and say whether we should proceed to the next queued identity, Collapse Timeline, while preserving this dependency. No identity is accepted or applied by this submission.\n\nPreserve all other holds and qualifications. No runtime, canonical application, implementation, balance, playtest, cosmology, domain, completion or release approval is requested. Return acceptedIds, appliedIds, heldIds, exact blockers, current authority, closure-task count and next identity.\n'''
    add(members,'REQUEST.md',request.encode())
    context={'id':'FATE-REWRITE-PACKET-320','recordedAtUtc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'scopeIds':['fate-rewrite'],'blockerIds':['TF192-B04'],'linkedContextIds':['eternal-prophecy'],'authority':queue['currentAuthority'],
        'nextPendingIds':queue['nextPendingIds'],'pendingCount':queue['pendingCount'],'closureTasksRemaining':queue['closureTasksRemaining'],'firstReviewTasksRemaining':queue['firstReviewTasksRemaining'],
        'currentQueue':bind(QUEUE),'currentHandoff':bind(HANDOFF),'pendingAudit':bind(PENDING),'baselineSourcePacket':baseline_archive_binding,'sourceComparison':{'inventory':140,'unchanged':sum(x['status']=='UNCHANGED' for x in comparisons),'changed':sum(x['status']=='CHANGED' for x in comparisons),'missing':sum(x['status']=='MISSING' for x in comparisons),'changedPaths':changed},
        'return282':bind(RETURN282),'timeStopReturn318':bind(TIME_STOP_RETURN),'interfaceAuthorizationId':'FR-EP-WITNESS-CONSTRUCTION-01','preservedFateRewriteCases':len(fate_cases),'linkedEternalProphecyCases':len(ep_cases),
        'existingConflictingCreationCaseIsUnpaidRefusal':True,'completePaidFulfilledGuaranteeFound':False,'acceptedIds':[],'appliedIds':[],'heldIds':[],'canonicalFilesChanged':False,'runtimeExecuted':False}
    addj(members,'CONTEXT.json',context)

    archive=OUT/'DD_Rank9_FateRewrite_CurrentSource_320.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name in sorted(members): z.writestr(name,members[name])
    archive_raw=archive.read_bytes(); archive_binding=bind(archive)
    checks=[]
    def ck(name: str, passed: bool, detail: Any=None):
        checks.append({'check':name,'passed':bool(passed),'detail':detail})
        if not passed: raise AssertionError(f'{name}: {detail}')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        ck('archive has a unique safe exact allowlist',len(names)==len(set(names)) and set(names)==set(members) and all(not pathlib.PurePosixPath(x).is_absolute() and '..' not in pathlib.PurePosixPath(x).parts and '\\' not in x for x in names),{'members':len(names)})
        ck('archive CRC and member SHA readback',z.testzip() is None and all(sha(z.read(n))==sha(members[n]) for n in members),{'members':len(names)})
    ck('current queue, handoff and pending audit agree at 823/25/0 and Fate Rewrite next',queue['pendingCount']==25 and queue['closureTasksRemaining']==25 and queue['firstReviewTasksRemaining']==0 and queue['next']=='fate-rewrite' and pending['pendingCount']==25 and handoff['heldThisStep']==['time-stop'],queue['currentAuthority'])
    ck('current FRewrite and EProp remain pending with exact active blockers',findex.get('authoredStatus')=='pending-authored-procedure' and eindex.get('authoredStatus')=='pending-authored-procedure' and proc['blockerIds']==['TF192-B04'] and ep['blockerIds']==['TF192-B02'],{'fate':findex.get('authoredStatus'),'prophecy':eindex.get('authoredStatus')})
    ck('Packet282 source inventory has only the index delta',len(comparisons)==140 and sum(x['status']=='UNCHANGED' for x in comparisons)==139 and changed==expected_changed,changed)
    ck('all 17 preserved Fate Rewrite cases exactly match current procedure IDs',len(fate_cases)==17 and [x['id'] for x in fate_cases]==proc['caseIds'],[x['id'] for x in fate_cases])
    ck('all linked Eternal Prophecy cases exactly match its procedure IDs',[x['id'] for x in ep_cases]==ep['caseIds'],len(ep_cases))
    ck('FateRewrite prophecy-creation conflict has no preexisting obligation and is unpaid refusal',not initial_obligations and any(x.get('RPSpent')==0 and x.get('status')=='unavailable-before-payment' for x in final_outcomes),{'initialObligations':list(initial_obligations),'finalOutcomes':final_outcomes})
    ck('linked Eternal Prophecy plan retains explicit TF192-B02 unresolvedGuarantee', 'TF192-B02' in ep['procedure']['unresolvedGuarantee'] and 'all lawful routes' in ep['procedure']['unresolvedGuarantee'],ep['procedure']['unresolvedGuarantee'][:500])
    ck('Director contract authorizes interface construction only and leaves both spells pending',status_record['interfaceAuthorizationId']=='FR-EP-WITNESS-CONSTRUCTION-01' and status_record['authorizationDoesNotSupplyMechanism'] is True and context['acceptedIds']==[] and context['appliedIds']==[],None)
    ck('scope contains Fate Rewrite alone; Eternal Prophecy is linked context only',context['scopeIds']==['fate-rewrite'] and context['linkedContextIds']==['eternal-prophecy'],context['scopeIds'])
    ck('no acceptance, application, canonical change or runtime execution',context['acceptedIds']==[] and context['appliedIds']==[] and context['canonicalFilesChanged'] is False and context['runtimeExecuted'] is False,None)
    audit={'id':'FATE-REWRITE-PACKET-320-INDEPENDENT-AUDIT','recordedAtUtc':context['recordedAtUtc'],'status':'PASS','archive':archive_binding,'memberCount':len(members),'scopeIds':['fate-rewrite'],'linkedContextIds':['eternal-prophecy'],'authority':queue['currentAuthority'],
           'sourceInventoryCount':140,'unchangedSourceBindings':139,'changedSourceBindings':1,'changedPaths':changed,'fateRewriteCases':len(fate_cases),'eternalProphecyCases':len(ep_cases),'checkCount':len(checks),'passedChecks':len(checks),'failedChecks':0,'checks':checks,
           'criticalFinding':'No source-complete paid/fulfilled guarantee exists in current linked evidence; the existing FRewrite prophecy-conflict case has no starting obligation and refuses pre-payment. Eternal Prophecy TF192-GUARANTEE-01 remains unresolved for all-routes-prevented and unavailable item/destination branches.',
           'acceptedIds':[],'appliedIds':[],'heldIds':[],'canonicalFilesChanged':False,'runtimeExecuted':False}
    audit_path=AUDIT/'FATE_REWRITE_PACKET_320_INDEPENDENT_AUDIT.json'; audit_path.write_bytes(pretty(audit))
    request_path=OUT/'FATE_REWRITE_DIRECTOR_REQUEST_320.md'; request_path.write_text(request,encoding='utf-8',newline='\n')
    comparison_path=OUT/'PACKET282_140_SOURCE_BINDING_COMPARISON.json'; comparison_path.write_bytes(pretty({'baselineArchive':baseline_archive_binding,'inventoryCount':140,'unchangedCount':139,'changedCount':1,'missingCount':0,'changedPaths':changed,'rows':comparisons}))
    delivery={'id':'FATE-REWRITE-PACKET-320-DELIVERY','status':'PREPARED_FOR_DIRECTOR_REVIEW','recordedAtUtc':context['recordedAtUtc'],'scopeIds':['fate-rewrite'],'linkedContextIds':['eternal-prophecy'],'blockerIds':['TF192-B04','TF192-B02'],'authority':queue['currentAuthority'],
              'archive':{'path':archive.relative_to(ROOT).as_posix(),**archive_binding},'request':{'path':request_path.relative_to(ROOT).as_posix(),**bind(request_path)},'independentAudit':{'path':audit_path.relative_to(ROOT).as_posix(),**bind(audit_path)},
              'sourceComparison':{'path':comparison_path.relative_to(ROOT).as_posix(),**bind(comparison_path)},'acceptedIds':[],'appliedIds':[],'heldIds':[],'closureTasksRemaining':25,'runtimeExecuted':False}
    delivery_path=OUT/'DD_Rank9_FateRewrite_CurrentSource_320_DELIVERY.json'; delivery_path.write_bytes(pretty(delivery))
    print(json.dumps({'status':'PASS','archive':str(archive),'archiveBytes':len(archive_raw),'archiveSha256':sha(archive_raw),'memberCount':len(members),'audit':str(audit_path),'delivery':str(delivery_path),'fateRewriteCases':len(fate_cases),'linkedEternalProphecyCases':len(ep_cases),'sourceComparison':{'unchanged':139,'changed':1,'changedPaths':changed},'authority':queue['currentAuthority'],'checks':len(checks)},ensure_ascii=False))

if __name__=='__main__': main()
