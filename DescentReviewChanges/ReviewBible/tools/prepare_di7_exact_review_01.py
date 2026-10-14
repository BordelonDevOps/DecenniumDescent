"""Freeze the complete seven-card exact review, preserving bounded evidence."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, V, info, encoded, digest


def read(p): return json.loads(p.read_bytes())


def main():
    root=A/'di7-exact-review-01-input'; archive=A/'DD_DI7_Exact_Review_01.zip'; receipt=A/'DI7_EXACT_REVIEW_01_PREPARATION.json'
    assert all(not p.exists() for p in [archive,receipt])
    # The first preparation reached Windows' nested path-length limit while
    # copying preservation files. Its incomplete local copies remain intact.
    # Write complete archive members directly from their original paths; the
    # verified archive, not that partial staging tree, is the review deliverable.
    paths=set()
    def include(p):
        p=Path(p); assert p.is_file(), str(p); p.relative_to(G); paths.add(p)
    public_path=R/'data/public/spell_candidates/divination_rank7_exact_01.json'
    internal_path=R/'data/director/spell_candidates/divination_rank7_exact_01.json'
    manuscript_path=R/'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md'
    expectations_path=R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'
    public,internal,expectations=read(public_path),read(internal_path),read(expectations_path)
    assert internal['completePublicEnvelope']==public and internal['publicEnvelopeBinding']==info(public_path) and internal['finiteExpectations']==expectations
    assert len(public['cards'])==7 and len(public['issueMap'])==14 and len(internal['originalExampleDispositions'])==14
    assert sum(len(g['variants']) for g in expectations['groups'])==49
    assert sum(len(g['variants']) for g in expectations['supplementalSourceExpectations'])==44
    assert not public['selectionEnabled'] and not public['exactReviewReceived']
    for p in [public_path,internal_path,manuscript_path,expectations_path,
              R/'docs/spells/candidates/DI7_SHAMAN_CASTING_INTERFACE.md',
              R/'data/public/spell_playtests/catalog.json',R/'data/public/spell_playtests/authored_review_index.json',
              R/'data/director/spell_proposals/divination_rank7.json',R/'docs/spells/proposals/DIVINATION_RANK7.md',
              A/'DI7_FINITE_93_EVIDENCE_INVENTORY.json', A/'DI7_AP_AS_01_ACTIVE_COUNTERPART_CONTROL.json',Path(__file__)]: include(p)
    # Full earlier input is preserved, including every original card/question,
    # counterpart, all17 class envelopes and all governing prose.
    original_input=A/'di7-joint-review-01-input/CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json'
    include(original_input)
    for rel in read(original_input)['sourceFiles']: include(G/rel)
    for p in V.rglob('*'):
        if p.is_file(): include(p)
    for p in (A/'di7-exact-01-source-descendants').rglob('*'):
        if p.is_file(): include(p)
    inventory=read(A/'DI7_FINITE_93_EVIDENCE_INVENTORY.json')
    report_paths=[G/x['path'] for x in inventory['reports'].values()]+[A/'DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json',A/'DI7_FATE_MODE_ADMISSION_CHECK.json',A/'DI7_ALIGNMENT_COMPONENT_CHECK.json']
    for p in report_paths:
        include(p); report=read(p); assert report['status']=='pass' and not report['failures']
        for binding in report.get('sourceBindings',[])+report.get('authorityBindings',[]): include(G/binding['path'])
    delta_names=['DI7_AP_AS_01_DERIVED_OPERATIONS.json','DI7_ACQ19_DERIVED_OPERATIONS.json','DI7_SHIELD_LATE_DERIVED_OPERATIONS.json',
        'DI7_VISION_COMMUNICATION_DERIVED_OPERATIONS.json','DI7_GEOMETRY_DERIVED_OPERATIONS.json','DI7_FACTION_REFERENCE_DERIVED_OPERATIONS.json',
        'DI7_SUPREME_TIME_SCOPE_DERIVED_OPERATIONS.json','DI7_SHAMAN_VENT_DERIVED_OPERATIONS.json','DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json']
    deltas=[]
    for name in delta_names:
        p=A/name; include(p); delta=read(p); deltas.append(info(p))
        for change in delta['changes']:
            preserved=G/change['before']['preservedCopy']; include(preserved); include(G/change['after']['path'])
            assert digest(preserved.read_bytes())==change['before']['sha256'] and preserved.stat().st_size==change['before']['bytes']
    # Literal source replies and bounded questions support each actual applied
    # addendum; screenshots/entire chat history are unnecessary to this upload.
    for prefix in ['DI7_ACQ19','DI7_SHIELD_LATE_ADMISSION','DI7_GEOMETRY_3D','DI7_FACTION_REFERENCE','DI7_SUPREME_TIME_SCOPE','DI7_SHAMAN_VENT']:
        for p in A.glob(prefix+'*'):
            if p.is_file() and p.suffix in {'.json','.txt'} and ('RECEIVED' in p.name or 'CLARIFICATION' in p.name or 'QUESTION' in p.name): include(p)
    # Nature is a separate completed finite scope, never a spell/copy grant.
    include(A/'FEAT335_NATURE_FINITE_FULFILLMENT.json')
    # Import closure of the delivered evaluators: exact original source files,
    # not rewritten portable versions or unexecuted counterfeit reports.
    parsed=set()
    while True:
        pending=[p for p in paths if p.suffix=='.py' and p not in parsed]
        if not pending: break
        for p in pending:
            tree=ast.parse(p.read_text(encoding='utf-8-sig')); parsed.add(p)
            for node in ast.walk(tree):
                modules=[node.module] if isinstance(node,ast.ImportFrom) and node.module else [a.name for a in node.names] if isinstance(node,ast.Import) else []
                for module in modules:
                    candidate=R/'tools'/(module.split('.')[0]+'.py')
                    if candidate.is_file(): include(candidate)
    before={p:info(p) for p in paths}
    current_classes=[]
    for entry in internal['preservedSourceDirectionEnvelope']['completeClassComparisons']:
        p=G/entry['path']; assert p in paths
        current_classes.append({'path':entry['path'],'currentBinding':before[p], 'matchesEmbeddedEnvelope':read(p)==entry['completeCurrentEnvelope']})
    context={'reviewId':'DI7-EXACT-REVIEW-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'request':'Separate exact review of the complete seven source-directed candidates, not another preliminary source conference.',
        'currentCandidates':[before[p] for p in [public_path,internal_path,manuscript_path,expectations_path]],
        'currentClassEnvelopes':current_classes,'sourceChangesAndPreservation':deltas,
        'finiteEvidence':{'original':49,'supplements':44,'total':93,'inventory':info(A/'DI7_FINITE_93_EVIDENCE_INVENTORY.json'),
            'followThroughAddenda':[info(A/'DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json'),info(A/'DI7_FATE_MODE_ADMISSION_CHECK.json')],
            'status':'Exact scopes differ. Historical inventory remains immutable. D7T-03-01 now executed; D7T-08-02 has paid Reaction/miss histories plus source-necessary predicate proofs; D7T-10-01 has actual own stats and selected-mode empty-cost evidence, with nonempty independent-entitlement adapters explicitly unavailable.',
            'noBlanketFulfillmentClaim':True,'authoringVersusRuntime':'We request exact authored operational review. No full arbitrary-payload engine, authentic campaign grants or human balance result is asserted.'},
        'all14ExamplesAndIssuesPreserved':True,'guardedOriginalOperations':18,'APASActiveReadersIncluded':True,
        'historicalStatusHandling':'Historical proposal/shared UNSENT labels are retained source bytes. This sidecar describes the actual new submission; they do not assert this package was sent earlier or confer approval.',
        'sourceBindingHandling':'Reports retain their original input hashes. Exact same-path before/after deltas and preserved copies are included. New source bindings never silently recertify a historical run.',
        'reproductionHandling':'Tools retain original Windows G/R/A constants and write-once output assertions. Review in an isolated scratch extraction, redirect roots only in your scratch/import environment and write fresh output names. Never overwrite or relabel supplied historical reports. Do not run one-use application/build scripts as current validators.',
        'ordinaryCounts':{'reviewed':412,'pending':436,'total':848},'promotions':0,'selectionEnabled':False,'exactApprovalReceived':False,
        'postPushReceipt':'DI7-X14/Greater Planar Summons is unchanged receipt-only; do not develop cosmology before authorized GitHub push and verified remote.'}
    request='''DI7-EXACT-REVIEW-01 — complete seven-card exact review

This is the separate exact submission requested by DI7-NEXT-EXACT-CONTRACT. Read CURRENT_REVIEW_CONTEXT.json, then the full public/internal divination_rank7_exact_01.json envelopes and DIVINATION_RANK7_EXACT_01.md at their repository paths. All seven complete procedures, all shared prose, all14 original/corrected examples and13 mechanical plus DI7-X14 receipt issues are present. Original source objects,18 guarded substitutions/inverses, active AP-AS-01 lower-card/guide counterparts, current17 class envelopes, complete governing documents, exact source addenda and preserved historical versions are included.

The actual source decisions ACQ19, Shield late admission, 3D geometry, Faction perceived reference, Supreme historical time scope and Shaman vent are applied with before-byte preservation and inverse records. Candidate/public/internal/rendering parity was checked. No original source/status/null, ordinary count, class/feat grant or receipt-only operation was promoted.

Please review the exact seven authored cards for correctness, completeness and flow against your contract, including the full shared/public/internal envelopes. Return an explicit per-card verdict and concrete guarded corrections for any issue. A downloadable addendum/evidence archive with byte count and SHA256 is preferred. Codex will preserve and apply corrections. Do not edit local files or request an unchanged generic source conference.

Finite evidence is deliberately precise: DI7_FINITE_93_EVIDENCE_INVENTORY.json maps49 original+44 supplemental cases to exact report histories. Read its later DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json and DI7_FATE_MODE_ADMISSION_CHECK.json addenda. All reports state conditional actor/world premises; no fixture authenticates a campaign. Later alignment136/32 checks use real conditional paid casts; current copied-source lookup correction preserves that earlier module and adds all4 real Fate providers. Shaman62/26 and Supreme74/31 include all9 and8 additional source expectations. No report is relabeled a new run when its source input changed.

Two review-sensitive qualifications need an explicit verdict, not a false pass: D7T-08-02 uses actual paid/observed Counterspell Reaction and Lifedraw miss originals, plus exact source necessary-predicate proofs for Shield, rank0 damage, damaging summon, recursive Arcane Echo, rank9, pending payload and missing adapters. The negative predicate proves inadmissibility independent of an original outcome; it does not execute those rejected payloads. D7T-10-01 fully executes the selected Coin/Suggestion child modes and own statistics/focus/price/fresh outcomes; their full actual sources have no separately consumed material or acquired charge. No hypothetical charge was invented. A payload requiring a nonempty independent entitlement remains inadmissible until its real source and full adapter exist, as the complete Fate procedure and your boundedRemainingDependencies require. We do NOT certify an arbitrary special-material/charge runtime. Assess whether these bounded authoring results satisfy the finite contract; if further evidence is necessary, name its exact real source/mode/predicate, without inventing a cost or requiring all future payloads.

All14 examples remain authored conditional teaching examples, with separately indexed executed evidence. Nature finite fulfillment is supplied only as separate nonspell context; no unchanged335-feat resubmission or certification is requested. Ordinary412 reviewed/436 pending, all candidate approval/selection/runtime flags, prior comparison scopes and human balance gates remain unchanged.

DI7-X14/Greater Planar Summons stays wholly receipt-only. No plane/origin/arrival/return/consent/setting doctrine is to be developed. Required later order remains actual joint whole-game flow agreement, already-authorized GitHub commit/push, verified remote, then careful cosmology. This is seven-card review only, not whole-game approval.
'''
    root.mkdir(exist_ok=True)
    manifest={}
    for p in sorted(paths):
        rel=p.relative_to(G).as_posix(); manifest[rel]={'bytes':before[p]['bytes'],'sha256':before[p]['sha256']}
    for name,data in [('CURRENT_REVIEW_CONTEXT.json',encoded(context)),('REQUEST.txt',request.encode('utf-8'))]:
        (root/name).write_bytes(data); manifest[name]={'bytes':len(data),'sha256':digest(data)}
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded(manifest))
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(paths): z.write(p,p.relative_to(G).as_posix())
        for name in ['CURRENT_REVIEW_CONTEXT.json','REQUEST.txt','PACKAGE_MANIFEST.json']: z.write(root/name,name)
    assert before=={p:info(p) for p in paths}
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(manifest)+1
        for name,meta in manifest.items():
            data=z.read(name); assert len(data)==meta['bytes'] and digest(data)==meta['sha256']
    result={'reviewId':'DI7-EXACT-REVIEW-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'prepared-not-sent',
        'archive':info(archive),'manifest':info(root/'PACKAGE_MANIFEST.json'),'request':info(root/'REQUEST.txt'),'context':info(root/'CURRENT_REVIEW_CONTEXT.json'),
        'payloadsVerified':len(manifest),'mechanicalSpells':7,'originalExamples':14,'originalMechanicalIssues':13,'receiptOnlyIssues':1,
        'allCurrentSourceFilesUnchangedDuringBuild':True,'archiveIsCompleteAuthoritativeDeliverable':True,
        'partialStagingTree':'Preserved incomplete first-attempt source copies remain in the input folder after a Windows nested path-length failure; the archive was built directly from current original files and independently verified in full.',
        'exactApproval':False,'full93Fulfilled':False,'spellPromotions':0,'sourceInformationDeleted':0,'pushed':False,'cosmologyReviewed':False}
    receipt.write_bytes(encoded(result)); print(json.dumps(result))


if __name__=='__main__': main()
