"""Record paid Shaman interface evidence without claiming exact-card acceptance."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(path):
    return json.loads(path.read_bytes())


def main():
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_SUPREME_AND_SHAMAN_RULING.json'
    checkpoint = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_SHAMAN_EXECUTION.json'
    delta = A/'DI7_SHAMAN_EXECUTION_PROGRESS_DELTA.json'
    preservation = A/'navigation-before-di7-shaman-execution'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    state = read(previous)
    now = datetime.now(timezone.utc).isoformat()
    report_path = A/'DI7_SHAMAN_TRANSACTIONS_CHECK.json'
    report = read(report_path)
    assert report['status'] == 'pass' and report['checks'] == 62 and report['historyCount'] == 26
    assert not report['failures'] and report['shaman9Executed']
    assert len(report['sourceExpectationCoverage']) == 9
    for binding in report['sourceBindings']:
        assert info(G/binding['path']) == binding, binding['path']
    expectations = read(R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json')
    assert sum(len(g['variants']) for g in expectations['groups']) == 49
    assert sum(len(g['variants']) for g in expectations['supplementalSourceExpectations']) == 44
    scope = ('Shaman casting-interface follow-through passes62 checks in26 conditional paid histories, mapping all9 source expectations. '
             'Actual selected Totem Casting pays2RP and creates its own timed concentration object before a qualifying ordinary cast. '
             'The step5 vent follows concentration displacement, never discounts RP or removes stored strain, and is occupied by a qualifying zero-strain cantrip. '
             'Outside-first/inside-later, overlapping own totems, another owner aura, countered casts, suppression, expiry, destruction, incapacity and next-round opportunity are exercised. '
             'All7 DI7 commitment boundaries, actual Detect Poison, actual Fate outer/child costs and concentration, Ready hold/release and forecast order are covered. '
             'Conditional upstream action grants, round phase, movement, damage and world facts are not authenticated campaign grants. Stone combat bonuses and other totem profiles are not claimed executed. '
             'The separate spell payload reports retain their own scope. Next compile49 original expectations plus44 source supplements into93 linked cases and submit the complete seven public/internal candidates for actual GPT exact acceptance. '
             'No full49 fulfillment, exact approval, ordinary promotion, human playtest, deletion, push or cosmology review is claimed. Ordinary coverage412/436 remains. '
             'Fresh weekly usage45percent; owner stop at50 remains. Final joint whole-game flow precedes authorized push, verified remote and careful cosmology.')
    ledger_path = R/'data/playtest/game_development_coverage.json'
    nav = R/'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before = read(ledger_path)
    ledger = deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).append(report_path.relative_to(G).as_posix())
            row.setdefault('currentEvidenceAddenda', []).append({
                'id': 'DI7-Shaman-paid-casting-interface', 'recordedAtUtc': now,
                'checks': 62, 'conditionalHistories': 26, 'shamanExpectationsExecuted': 9,
                'full49Fulfilled': False, 'exactCardsApproved': False})
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if old['id'] not in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            assert old == new
    assert {k:v for k,v in before.items() if k != 'aspects'} == {k:v for k,v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_SUPREME_SHAMAN_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain) == 1 and text.count(state['status']) == 1
    text = text.replace(chain, chain.rstrip('\n')+' + read(A / "DI7_SHAMAN_EXECUTION_PROGRESS_DELTA.json")["changes"]\n')
    text = text.replace(state['status'], scope, 1)
    marker = '    pending = [\n'
    assert text.count(marker) == 1
    text = text.replace(marker, marker+'        ("Shaman paid casting interface —62 checks in26 histories; all9 source expectations", "DI7_SHAMAN_TRANSACTIONS_CHECK.json"),\n')
    compile(text, str(nav), 'exec')
    preserved = []
    for path in [ledger_path, nav, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
        dest = preservation/path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(path.read_bytes())
        assert dest.read_bytes() == path.read_bytes()
        preserved.append({**info(path), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger))
    nav.write_text(text, encoding='utf-8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': [
        {'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [ledger_path, nav]],
        'allOtherAspectsUnchanged': True, 'allClosureAndHumanEvidenceUnchanged': True, 'sourceInformationDeleted': 0, 'spellPromotions': 0}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout)
        print(run.stderr)
        raise SystemExit(run.returncode)
    navigation = read(A/'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks']
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), goalTurnClassification='progress',
                 previousGoalTurnClassification='progress', status=scope, coverageLedger=info(ledger_path), coverageDelta=info(delta),
                 navigation={'map': info(G/'REVIEW_MAP.html'), 'receipt': info(A/'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
                 di7ShamanTransactions={'report': info(report_path), 'checks': 62, 'histories': 26,
                    'module': info(R/'tools/di7_shaman_transactions.py'), 'validator': info(R/'tools/validate_di7_shaman_transactions.py'),
                    'sourceExpectationCoverage': report['sourceExpectationCoverage'], 'conditionalPremises': report['conditionalPremises'],
                    'remaining': report['remaining'], 'full49Fulfilled': False})
    state['di7ShamanVentRuling']['expectationsExecuted'] = True
    state['activeGptReview']['instruction'] = 'No reply pending. All source rulings applied and bounded interface follow-through recorded. Compile93 finite cases, resolve any evidence gaps and submit the complete seven exact candidates separately.'
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_SHAMAN_EXECUTION. Fresh weekly usage45percent; stop at50 mandatory.',
        'Shaman62/26 covers all9 source expectations. Preserve its successful write-once report and module hashes; do not rerun successful validators.',
        'Compile16groups49 originals plus4Shield+19geometry+4Faction-reference+8Supreme-time+9Shaman expectations (93total) against exact actual history/check IDs. Distinguish source/preservation checks, executed conditional histories, unsupported adapters and pending external submission.',
        'Preserve all14 original/corrected examples,13 mechanical issues and DI7-X14 receipt,18 exact source operations, AP-AS-01 active counterparts and all subsequent source clarification delta chains in the exact package.',
        'No GPT reply pending. Calibration Review Part2 Chrome3 tab125745960. Submit full current7 public/internal/manuscript/expectations and operational dependencies for separate exact acceptance; source agreement never promotes cards.',
        'Keep all earlier reports and qualifications. No deletion, promotion, human approval, whole-game acceptance, push or cosmology occurred.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).append(info(preservation/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'weeklyUsagePercent': 45}))


if __name__ == '__main__':
    main()
