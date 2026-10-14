"""Preserve navigation while recording paid alignment and the93-case inventory."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(path): return json.loads(path.read_bytes())


def main():
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_SHAMAN_EXECUTION.json'
    checkpoint = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_FINITE_INVENTORY.json'
    delta = A/'DI7_FINITE_INVENTORY_PROGRESS_DELTA.json'
    preservation = A/'navigation-before-di7-finite-inventory'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    state = read(previous)
    now = datetime.now(timezone.utc).isoformat()
    report_path = A/'DI7_ALIGNMENT_TRANSACTIONS_CHECK.json'
    inventory_path = A/'DI7_FINITE_93_EVIDENCE_INVENTORY.json'
    report, inventory = read(report_path), read(inventory_path)
    assert report['status'] == 'pass' and report['checks'] == 136 and report['historyCount'] == 32 and not report['failures']
    assert len(report['sourceExpectationCoverage']) == 4
    for binding in report['sourceBindings']: assert info(G/binding['path']) == binding
    assert len(inventory['rows']) == 93 and inventory['boundedEvidenceGaps'] == ['D7T-03-01', 'D7T-08-02', 'D7T-10-01']
    for binding in inventory['currentCandidates']+list(inventory['reports'].values()): assert info(G/binding['path']) == binding
    scope = ('Paid Alignment Purge/Suggestion follow-through passes136 checks in32 conditional histories covering all4 D7T-13 variants. '
        'Actual learned/prepared spells pay RP/Action/strain and resolve binary saves, immunity/undefined records, both overlay orders, genuine no-change/nonreplacement, current caster snapshot, independent underlying changes and same/different-caster replacement. '
        'The new finite extension checks current target/body/concentration at resolution and immediately clears the former caster concentration after a successful family replacement. '
        'Actual source grants and originating movement/conditions/dispels remain conditional upstream premises; earlier successful modules/reports remain unchanged. '
        'The93-case inventory verifies80 distinct source bindings and current public/internal/rendering parity:86 cases have conditional execution evidence,2 structural evidence,3 bounded evidence gaps,1 pending package and1 pending actual external submission. '
        'Open tests are exact cone30.1/60.1 boundaries, complete Fate admission examples and a source-qualified nonempty independent-entitlement child. This is an honest evidence inventory, not full49/93 fulfillment or exact approval. '
        'All14 original/corrected examples,13 mechanical issues/DI7-X14 receipt,18 source operations and active AP-AS preservation remain. '
        'Ordinary412/436, selection/runtime/approval flags and human evidence remain unchanged. Fresh weekly usage45percent; owner stop at50 remains. '
        'No deletion, push or cosmology. Final joint whole-game flow precedes authorized push, verified remote and careful cosmology.')
    ledger_path, nav = R/'data/playtest/game_development_coverage.json', R/'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before = read(ledger_path); ledger = deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, inventory_path])
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'DI7-paid-alignment-and93-evidence-inventory', 'recordedAtUtc': now, 'checks': 136, 'histories': 32, 'inventoryStatuses': inventory['statusCounts'], 'full49Fulfilled': False, 'exactCardsApproved': False})
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if old['id'] not in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}: assert old == new
    assert {k:v for k,v in before.items() if k != 'aspects'} == {k:v for k,v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_SHAMAN_EXECUTION_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain) == 1 and text.count(state['status']) == 1
    text = text.replace(chain, chain.rstrip('\n')+' + read(A / "DI7_FINITE_INVENTORY_PROGRESS_DELTA.json")["changes"]\n').replace(state['status'], scope, 1)
    marker = '    pending = [\n'; assert text.count(marker) == 1
    text = text.replace(marker, marker+'        ("DI7 all93-case evidence inventory —explicit remaining gaps", "DI7_FINITE_93_EVIDENCE_INVENTORY.json"),\n        ("Paid alignment transactions —136 checks in32 histories", "DI7_ALIGNMENT_TRANSACTIONS_CHECK.json"),\n')
    compile(text, str(nav), 'exec')
    preserved = []
    for path in [ledger_path, nav, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
        dest = preservation/path.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(path.read_bytes())
        assert dest.read_bytes() == path.read_bytes()
        preserved.append({**info(path), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text, encoding='utf-8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': [{'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [ledger_path, nav]], 'allOtherAspectsUnchanged': True, 'allClosureAndHumanEvidenceUnchanged': True, 'sourceInformationDeleted': 0, 'spellPromotions': 0}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), goalTurnClassification='progress', previousGoalTurnClassification='progress', status=scope,
        coverageLedger=info(ledger_path), coverageDelta=info(delta), navigation={'map': info(G/'REVIEW_MAP.html'), 'receipt': info(A/'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        di7PaidAlignment={'report': info(report_path), 'checks': 136, 'histories': 32, 'module': info(R/'tools/di7_alignment_transactions.py'), 'validator': info(R/'tools/validate_di7_alignment_transactions.py'), 'sourceExpectationCoverage': report['sourceExpectationCoverage'], 'conditionalPremises': report['conditionalPremises']},
        di7FiniteEvidenceInventory={'report': info(inventory_path), 'builder': info(R/'tools/build_di7_finite_evidence_inventory.py'), 'statuses': inventory['statusCounts'], 'boundedGaps': inventory['boundedEvidenceGaps'], 'full49Fulfilled': False, 'full93Fulfilled': False})
    state['activeGptReview']['instruction'] = 'No reply pending. Resolve the3 explicit finite evidence gaps, prepare all7 exact candidates with all envelopes/examples/issues, and submit for actual separate exact review.'
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_FINITE_INVENTORY. Fresh weekly usage45percent; stop at50 mandatory.',
        'Paid alignment136/32 and Shaman62/26 succeeded. Preserve all successful report/module bytes. New AlignmentTransactions checks actual resolution-time target/body/concentration and immediate previous-caster concentration cleanup; older ClockedFateTransactions retained at its original bytes.',
        'DI7_FINITE_93_EVIDENCE_INVENTORY contains exact history pointers and80 validated source/version chains.86 conditional cases+2 structural+3 bounded gaps+1 package pending+1 external submission pending; not full49/93.',
        'D7T-03-01: execute actual paid geometry with exact30.1/60.1 exclusion operands; current35/65 grid examples are insufficient for the exact requested boundary.',
        'D7T-08-02: original Fate adapter accepts only complete Fate Coin/Alignment Suggestion modes. Add genuine source-bound Reaction-only/damaging/indirect-damage and other boundary admission histories without pretending an unreviewed mode has a complete cast runtime.',
        'D7T-10-01: current two child modes have no independent material/charge. Find an actual complete source-qualified copied mode with independent entitlement, or explicitly bound this unsupported dependency in the exact submission. Never fabricate a charge or mutate a source solely to make a test pass.',
        'Keep the successful evidence inventory immutable. Add a separate follow-through report/update linking exact closed gaps; then prepare the full exact-seven package and send once to actual GPT Calibration Review Part2 Chrome3 tab125745960.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'weeklyUsagePercent': 45}))


if __name__ == '__main__': main()
