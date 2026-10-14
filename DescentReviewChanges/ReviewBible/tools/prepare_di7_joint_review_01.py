"""One-use exact source package for seven DI7 proposed procedures, no adoption."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, shutil, zipfile
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'


def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    root=A/'di7-joint-review-01-input';archive=A/'DD_DI7_Joint_Review_01.zip';receipt=A/'DI7_JOINT_REVIEW_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    proposal=R/'data/director/spell_proposals/divination_rank7.json';old=read(proposal);current=deepcopy(old)
    original_paths=[G/rel for rel in old['sourceFiles']]
    paths=original_paths+[proposal,R/'docs/spells/proposals/DIVINATION_RANK7.md',
        A/'DIVINATION_RANK7_OPERATING_PROPOSAL_CHECK.json',A/'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_AFTER_DI7_CHECK.json',
        A/'FEAT335_NATURE_SOURCE_CHECK_01_CONTROLLING_RECORD.json',A/'FEAT335_NATURE_SOURCE_PROPAGATION_CHECK.json',
        A/'FEAT335_NATURE_SOURCE_CHECK_01_REPRODUCED.json',A/'feat335-nature-source-check-01-verdict/FEAT335_NATURE_SOURCE_CHECK_01_ADDENDUM.md',
        A/'feat335-nature-source-check-01-verdict/EXACT_NATURE_CORRECTIONS.json',Path(__file__)]
    paths=list(dict.fromkeys(paths));before={p:info(p) for p in paths};changes=[]
    for rel,binding in old['sourceFiles'].items():
        actual=before[G/rel];measured={k:actual[k] for k in ['bytes','sha256']}
        if measured!=binding:changes.append({'path':rel,'historical':binding,'current':measured})
    assert {c['path'] for c in changes}=={
        'DescentReviewChanges/ReviewBible/data/director/higher_spell_operating_proposal_index.json',
        'DescentReviewChanges/ReviewBible/data/public/class_playtests/ranger.json'}
    for entry in current['completeClassComparisons']:
        p=G/entry['path'];entry.update(bytes=before[p]['bytes'],sha256=before[p]['sha256'],completeCurrentEnvelope=read(p))
    for rel,entry in current['currentGoverningDocuments'].items():
        p=G/rel;entry['currentFile']={k:before[p][k] for k in ['bytes','sha256']};entry['fullCurrentText']=p.read_text(encoding='utf-8')
    current['historicalSourceFiles']=deepcopy(old['sourceFiles'])
    current['sourceFiles']={rel:{k:before[G/rel][k] for k in ['bytes','sha256']} for rel in old['sourceFiles']}
    current['reviewInputRebase']={'id':'DI7-JOINT-REVIEW-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'originalProposal':before[proposal],'changedBindings':changes,
        'scope':'Review-input descendant only. Seven procedures, original questions,14 examples,14 explicit joint issues and deferred receipt are unchanged. Current17 class envelopes and governing documents are rebased; original complete proposal remains included unchanged.',
        'nature':'The actual Nature completion is adopted and source-propagated; its16 behavior groups/47 variants remain pending. No whole335 feat approval is implied.'}
    for key in ['records','sharedProposal','explicitJointIssues','completeCurrentCounterparts','earlierUnadoptedCounterpartProposals',
                'unresolvedCounterpartQuestions','completeOriginalPreparations','completeUntouchedDeferredReceipts']:
        assert current[key]==old[key]
    assert len(current['records'])==7 and len(current['explicitJointIssues'])==14
    assert [r['spellId'] for r in current['completeUntouchedDeferredReceipts']]==['planar-summons-greater']
    assert all(r['status']=='unadopted-unsent-operating-proposal' for r in current['records'])
    catalog_path=R/'data/public/spell_playtests/catalog.json';index_path=catalog_path.with_name('authored_review_index.json')
    catalog={s['id']:s for s in read(catalog_path)['spells']};index={s['id']:s for s in read(index_path)['entries']}
    for row in current['records']:
        sid=row['spellId'];assert catalog[sid]==row['fullSourceAndCurrentAccessRecord'] and catalog[sid]['operational'] is None
        assert index[sid]['authoredStatus']=='pending-authored-procedure'
    for row in current['completeCurrentCounterparts']:
        sid=row['id'];entry=index[sid];assert row['currentAuthoredIndexEntry']==entry
        obj=read(index_path.parent/entry['procedureFile'])
        for key in entry['wholeCardPointer'].strip('/').split('/'):obj=obj[int(key)] if isinstance(obj,list) else obj[key]
        assert row['completeCurrentAuthoredRecord']==obj
    root.mkdir();manifest={}
    for p in paths:
        rel=p.relative_to(G).as_posix();dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        assert dest.read_bytes()==p.read_bytes();manifest[rel]=before[p]
    save(root/'CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json',current)
    request=('DI7-JOINT-REVIEW-01 — actual joint source/procedure review of the seven complete rank-seven Divination proposals.\n\n'
        'Read CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json first. It contains all seven full proposed procedures, their exact historical sources/Core placements/class access, two authored examples each,14 explicit joint issues,14 complete counterpart records, earlier unadopted comparisons, unresolved source-only comparisons,17 complete class envelopes and full current governing documents. Every46 source input file is also attached at its actual repository path, together with the unchanged original proposal/manuscript/checks. The historical proposal says UNSENT; this is its first actual dispatch, not a prior approval.\n\n'
        'Resolve DI7-X01–13 against these complete sources. Distinguish KEEP from NEW minimum explicit completions. Mass Revelation must retain all four categories with bounded lie/hostility/evidence predicates. Premonition Shield must keep exactly two qualifying damage-prevention events and define misses/zero/nondamage/multi-beam/later ticks/transfer stages. Fate Echo must remain a non-damaging historic spell copy distinct from Cast Echo and feat-copy profiles: decide actual observation/window/rank/mode/source entitlement plus paid nested casting, components/materials, concentration, Dissonance/Refrain and independent interrupt histories. Vision Quest must provide actionable bounded guidance without invented metaphysical origin. Faction Omniscience must honor institution-wide actual current activity without quietly reducing the promise to one agent; apply only real field-specific protections and unknown facts. Alignment Purge must explicitly settle temporary True Neutral versus suppressed predicates and its conflict with reviewed Alignment Suggestion/target-baseline rules, without automatic oathbreak or rewritten underlying identity. Resonance Sight Supreme must retain actual historical effects with precise scope/unknown/protection behavior.\n\n'
        'The written14 examples and arithmetic checks are not runtime, world authentication or human balance results. No source is made authoritative merely by being included. Pending comparison proposals supply no approved rule. If a source remains insufficient, name the concrete unanswered boundary rather than inventing a wider gate or requesting unchanged whole-source resubmission. Give complete source-bound decisions and exact guarded procedure/shared-proposal replacements where needed, with finite distinguishing follow-through expectations. A downloadable addendum/evidence archive with byte count and SHA256 is preferred. Do not alter local files; Codex will preserve and propagate reviewed changes.\n\n'
        'DI7-X14/DI7-02 is receipt-only: Greater Planar Summons remains two extraplanar allies,CR8 each, and wholly unadopted. Do not review its operation, cosmology, origins, planes, consent/arrival/return or any setting doctrine before authorized GitHub push and verified remote. Likewise guidance/information/alignment discussion here is mechanics only.\n\n'
        'Continuity: your Nature addendum is received intact (194878bytes, SHA888a7319acc2556d1ec1736cac4c78a4354e2fed574007f7d1bf376b096a2960). All18 payloads verified;124 checks reproduce;137 local exact-propagation/preservation checks updated3 fields/paragraphs and3 current mirrors. Nature16 NWT groups/47 variants are still required local follow-through. Do not re-audit the completed Nature source decision or unchanged335 feats.\n\n'
        'Rebase: only two original source files changed since DI7 preparation: the higher-spell index now registers these same seven unadopted drafts; Ranger now contains your exact Nature completion. Both current files and the historical source bindings are included. All seven proposals/questions/examples and all original objects remain unchanged. Final whole-game flow agreement, authorized GitHub delivery, verified remote, then careful cosmology remain separate later gates.\n')
    (root/'REQUEST.txt').write_text(request,encoding='utf-8',newline='\n')
    for name in ['REQUEST.txt','CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json']:
        p=root/name;meta=info(p);manifest[name]={'bytes':meta['bytes'],'sha256':meta['sha256']}
    save(root/'PACKAGE_MANIFEST.json',manifest)
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    assert before=={p:info(p) for p in paths}
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(manifest)+1
        for name,meta in manifest.items():
            from hashlib import sha256
            b=z.read(name);assert len(b)==meta['bytes'] and sha256(b).hexdigest()==meta['sha256']
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'reviewId':'DI7-JOINT-REVIEW-01','archive':info(archive),
        'manifest':info(root/'PACKAGE_MANIFEST.json'),'payloads':len(manifest),'sourceInputFiles':46,'mechanicalSpells':7,
        'authoredExamples':14,'jointIssues':14,'deferredReceipts':1,'rebase':changes,'status':'prepared-not-sent',
        'ordinaryCatalogCounts':read(index_path)['authoredCounts'],'sourceInformationDeleted':0,'adopted':False,'cosmologyReviewed':False}
    save(receipt,result);print(json.dumps(result))


if __name__=='__main__':main()
