"""Record exact cone follow-through and preserved copied-source correction."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(path): return json.loads(path.read_bytes())


def main():
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_FINITE_INVENTORY.json'
    checkpoint = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_BOUNDARY_AND_COPY_SOURCE.json'
    delta = A/'DI7_BOUNDARY_COPY_PROGRESS_DELTA.json'
    preservation = A/'navigation-before-di7-boundary-copy'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    state = read(previous); now = datetime.now(timezone.utc).isoformat()
    report_path = A/'DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json'
    source_delta_path = A/'DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json'
    report, source_delta = read(report_path), read(source_delta_path)
    assert report['status'] == 'pass' and report['checks'] == 82 and report['historyCount'] == 24 and not report['failures']
    for binding in report['sourceBindings']: assert info(G/binding['path']) == binding
    for c in source_delta['changes']:
        assert info(G/c['after']['path']) == c['after'] and digest((G/c['before']['preservedCopy']).read_bytes()) == c['before']['sha256'] and c['exactInverseBytesVerified']
    scope = ('Exact fractional Mass cone boundaries now pass through all4 paid provider routes:60/30 included, lateral30.1 and forward60.1 excluded, actual total cover clips the boundary. '
        'The82-check/24-history report closes D7T-03-01 and also validates actual Wizard Alignment Suggestion originals copied by all4 Fate providers, including their own stats/payments and postcommit target invalidation. '
        'A narrowly preserved evaluator correction selects the original generating source for a copied child, avoiding false ordinary-access rejection for Cleric/Shaman; it grants no ordinary repertoire. '
        'The original136-check alignment report/module bytes are preserved with an exact inverse. '
        'The immutable93-case inventory plus this addendum now support87 conditional cases,2 structural cases,2 bounded gaps,1 package pending and1 external submission pending. '
        'D7T-08-02 broader actual Fate admission and D7T-10-01 nonempty independent entitlement remain explicitly open. No full49/93 or exact approval is claimed. '
        'Ordinary412/436 and all approval/human/source records remain unchanged. Fresh weekly usage46percent; stop at50 mandatory. Nothing deleted or pushed; cosmology remains after joint flow agreement, authorized push and verified remote.')
    ledger_path, nav = R/'data/playtest/game_development_coverage.json', R/'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']; before = read(ledger_path); ledger = deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09','DD-12','DD-14','DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, source_delta_path])
            row.setdefault('currentEvidenceAddenda', []).append({'id':'DI7-fractional-boundary-and-copied-source', 'recordedAtUtc':now, 'checks':82, 'histories':24, 'closedInventoryGap':'D7T-03-01', 'full49Fulfilled':False, 'exactCardsApproved':False})
    for old,new in zip(before['aspects'],ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if old['id'] not in {'DD-09','DD-12','DD-14','DD-69'}: assert old == new
    assert {k:v for k,v in before.items() if k!='aspects'} == {k:v for k,v in ledger.items() if k!='aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_FINITE_INVENTORY_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain) == 1 and text.count(state['status']) == 1
    text = text.replace(chain, chain.rstrip('\n')+' + read(A / "DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_BOUNDARY_COPY_PROGRESS_DELTA.json")["changes"]\n').replace(state['status'],scope,1)
    marker = '    pending = [\n'; assert text.count(marker) == 1
    text = text.replace(marker,marker+'        ("Exact fractional cone and copied alignment source —82 checks in24 histories", "DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json"),\n        ("Copied alignment source lookup —preserved previous evaluator and inverse", "DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json"),\n')
    compile(text,str(nav),'exec'); preserved=[]
    for path in [ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preservation/path.relative_to(G); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(path.read_bytes())
        assert dest.read_bytes()==path.read_bytes(); preserved.append({**info(path),'preservedCopy':dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text,encoding='utf-8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [ledger_path,nav]],'allOtherAspectsUnchanged':True,'allClosureAndHumanEvidenceUnchanged':True,'sourceInformationDeleted':0,'spellPromotions':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification='progress',status=scope,
        coverageLedger=info(ledger_path),coverageDelta=info(delta),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        di7BoundaryAndCopySource={'report':info(report_path),'checks':82,'histories':24,'sourceCorrection':info(source_delta_path),'currentAlignmentModule':info(R/'tools/di7_alignment_transactions.py'),'closedGap':'D7T-03-01','remainingGaps':report['remainingInventoryGaps']})
    state['di7FiniteEvidenceInventory']['currentAddendum']=info(report_path)
    state['di7FiniteEvidenceInventory']['currentStatusCounts']={'conditional-execution-evidence':87,'structural-preservation-evidence':2,'bounded-evidence-gap':2,'package-preparation-pending':1,'external-submission-pending':1}
    state['di7FiniteEvidenceInventory']['boundedGaps']=report['remainingInventoryGaps']
    state['activeGptReview']['instruction']='No reply pending. Two explicit Fate evidence gaps remain; preserve/currently bound complete-seven package and actual separate GPT exact review still pending.'
    state['safeNextActions']=[state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_BOUNDARY_AND_COPY_SOURCE. Fresh weekly usage46percent; stop at50 mandatory.',
        'Paid alignment136/32, Shaman62/26 and exact boundary/copied-source82/24 all passed. Do not rerun successful write-once validators or overwrite their reports.',
        'AlignmentTransactions current source lookup now reads the original generating provider for fate-echo-copy and verifies its exact binding, while child stats stay with actual Fate provider. Previous module preserved under source-before-di7-alignment-copy-source and exact delta/inverse. All4 provider copies plus invalidated targets pass.',
        'DI7_FINITE_93_EVIDENCE_INVENTORY remains immutable; DI7_BOUNDARY_AND_COPY_SOURCE_CHECK closes D7T-03-01. Current87 conditional+2 structural+2 gaps+1 package+1 external pending; not full49/93.',
        'D7T-08-02 broader admission gap: actual Counterspell original can be executed by existing DI7Sources/FateTransactions (Reaction source already admitted to ordinary evaluator), directly observed, resolved then rejected as Fate original by activation rule. Other complete source candidates include damaging Arcane Ray/Ray of Frost, indirect Summon Lesser Skeleton and recursive Arcane Echo, but their complete upstream cast adapters are not yet supplied; do not fake successful original receipts.',
        'D7T-10-01 nonempty independent entitlement remains. Current Fate Coin/Alignment Suggestion require V/S/F and no consumed stock/charge. Preliminary catalog field scan found no separate material/cost fields; absence of a structured field is not proof that all prose has no costs. Do not invent a material/charge or source. Exact acceptance contract explicitly leaves source-qualified independent entitlements as bounded prerequisites for a particular copied mode.',
        'Prior feat335_copy_source_components.py provides source-component witnesses for arcane-ray,burning-hands,lifedraw,false-life,slow,shield,mist-step, explicitly conditional upstream casting; it is not an actual ordinary cast engine and cannot silently fill the above gap.',
        'Keep14 original/corrected examples,13 mechanical issues and DI7-X14 receipt,18 exact substitutions, AP-AS actual readers and preserved sources. After bounded evidence resolution prepare complete7 public/internal envelopes and operational dependencies, then send once to actual Calibration Review Part2 Chrome3 tab125745960. No generic preliminary conference; any remaining unsupported runtime should be labeled, not certified.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests',[]).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'navigationLinks':navigation['existingDistinctLinks'],'weeklyUsagePercent':46}))


if __name__=='__main__': main()
