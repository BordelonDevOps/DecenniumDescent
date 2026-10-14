"""Record paid Vision lifecycle and bounded private-answer projection evidence."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p): return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_SHIELD_RULING_AND_ALL7_ACQUISITION.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_VISION_TRANSACTIONS.json'
    delta = A / 'DI7_VISION_PROGRESS_DELTA.json'
    preservation = A / 'navigation-before-di7-vision'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    state = read(previous); now = datetime.now(timezone.utc).isoformat()
    report_path = A / 'DI7_VISION_TRANSACTIONS_V2_CHECK.json'; report = read(report_path)
    operations_path = A / 'DI7_VISION_COMMUNICATION_DERIVED_OPERATIONS.json'; operations = read(operations_path)
    assert report['status'] == 'pass' and report['checks'] == 97 and report['historyCount'] == 44 and not report['failures']
    for binding in report['sourceBindings']: assert info(G / binding['path']) == binding
    assert len(operations['changes']) == 1
    for change in operations['changes']:
        saved = G / change['before']['preservedCopy']; current = G / change['after']['path']
        assert digest(saved.read_bytes()) == change['before']['sha256'] and info(current) == change['after']
        inverse = current.read_text(encoding='utf-8')
        for op in reversed(change['operations']):
            assert inverse.count(op['replacement']) == 1; inverse = inverse.replace(op['replacement'], op['old'], 1)
        assert inverse.encode() == saved.read_bytes()
    scope = ('Vision Quest now has97 checks across44 conditional histories, extending the existing source-bound paid casting boundary. '
        'Four actual ordinary provider routes, related/self anchor, fixed question, conscious stationary concentration60seconds, no early answer, normal completion once, actual countered cast, forced movement/incapacity/suppression/concentration failure, later Silence, life damage/binary concentration saves, source application order at the exact deadline and actual voluntary ending before a paid Counterspell are executed. '
        'Private answer projection uses supported central facts and feasible steps, at most150words/3steps and30-day future horizon with uncertainty, no work/action/access grant. '
        'Equivalent actual paid inquiries by distinct casters in the same conditional world and repeated same-caster Refrain histories agree; changed established facts may alter answers. '
        'Unknown/protected-existence/protected-text results disclose no hidden reason, IDs or counts; native scope subject/field/school/rank/query-time/fact-time and authorized masking are exercised as explicitly supplied conditional protection interfaces. '
        'Native protection acquisition/casting/arbitration, semantic truth/feasibility adjudication, incoming damage/conditions and full rest/character history remain upstream premises, not authenticated gameplay. '
        'Communication now delivers only the actual source-qualified received literal excerpt; no automatic whole-answer or private-metadata copy. The initial84/41 report and original helper bytes are preserved with exact inverse proof. '
        'No new rule, candidate text, promotion, full49+4 or exact-card approval. Mass/Faction/Supreme payloads, Suggestion initiative clock and Shaman ordinary totem vent remain. '
        'Ordinary authored coverage412/436 unchanged. Fresh weekly usage41percent; owner stop at50 remains. Final joint whole-game flow precedes authorized push, verified remote and careful cosmology; nothing deleted or pushed.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before = read(ledger_path); ledger = deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, operations_path])
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'DI7-Vision-paid-lifecycle-private-projection', 'recordedAtUtc': now,
                'checks': 97, 'conditionalHistories': 44, 'nativeProtectionGrantsAuthenticated': False,
                'full49Fulfilled': False, 'exactCardsApproved': False})
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if old['id'] not in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_SHIELD_LATE_ACQUISITION_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "DI7_VISION_COMMUNICATION_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_VISION_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status']) == 1; text = text.replace(state['status'], scope, 1)
    marker = '    pending = [\n'; assert text.count(marker) == 1
    items = [('Vision Quest current lifecycle and private answers —97 checks in44 conditional histories', report_path),
        ('Vision communication refinement —preserved helper and inverse proof', operations_path),
        ('Vision initial bounded evidence —84 checks in41 histories; see current97/44', A / 'DI7_VISION_TRANSACTIONS_CHECK.json')]
    text = text.replace(marker, marker + ''.join('        (' + json.dumps(label) + ', ' + json.dumps(p.relative_to(A).as_posix()) + '),\n' for label, p in items))
    compile(text, str(nav), 'exec'); preserved = []
    for path in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        dest = preservation / path.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(path.read_bytes())
        assert dest.read_bytes() == path.read_bytes(); preserved.append({**info(path), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text, encoding='utf-8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': [{'before': next(x for x in preserved if x['path'] == path.relative_to(G).as_posix()), 'after': info(path)} for path in [ledger_path, nav]],
        'allOtherAspectsUnchanged': True, 'allClosureAndHumanEvidenceUnchanged': True, 'sourceInformationDeleted': 0, 'spellPromotions': 0}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), goalTurnClassification='progress', previousGoalTurnClassification='progress', status=scope,
        coverageLedger=info(ledger_path), coverageDelta=info(delta),
        navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        di7VisionTransactions={'report': info(report_path), 'checks': 97, 'histories': 44, 'module': info(R / 'tools/di7_vision_transactions.py'),
            'remaining': report['remaining'], 'conditionalPremises': report['conditionalPremises'], 'full49Fulfilled': False},
        newRuleAdoptions=0, newRuleAdoptionCountScope='Execution of existing Vision/source information rules only; no new protection ability or exact approval.')
    state['activeGptReview']['instruction'] = 'No reply pending. Shield timing is received/applied. Current Vision97/44 is local conditional evidence, not GPT acceptance. Continue remaining spell payloads and finite49+4 compilation before exact seven-card review.'
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_VISION_TRANSACTIONS. Latest fresh weekly usage41percent; owner stop at50 remains mandatory.',
        'Vision current module di7_vision_transactions.py and reportV2 97/44: real conditional paid casting/lifecycle and private bounded fact projection. Actual excerpt communication only. Initial84/41 and old module bytes remain preserved; do not rerun either write-once validator.',
        'The generic native protection scope/grant cases are explicit upstream conditional interfaces, not real named player ability acquisitions or actual campaign facts. Do not claim native protection casting or overlapping protection arbitration implemented. Semantic question/fact/step correctness stays Director-established.',
        'Continue Mass Revelation, Faction Omniscience and Supreme Sight using paid casting and source-qualified conditional information. Vision fact projector is reusable only within its stated scope; each spell must retain its own all-facts and geometry/lifecycle rules.',
        'Then integrate Suggestion original initiative/virtual-phase clock and actual ordinary Shaman totem vent, assemble16groups49original variants plus4Shield supplemental cases, and submit all7 complete public/internal cards for separate exact review.',
        'Current Shield uses ShieldLateTransactions and95/36. All7 acquisition385/77 retains its separate rank6-upper-bound proof qualification. Actual GPT ACQ19 and Shield late rulings are both terminal; do not resend.',
        'No current source-card or selection/status changes this turn. Preserve before bytes and measured same-path deltas for future mutations; no source deletion or rewritten historical hashes.',
        'Chrome3 same Calibration Review Part2 last live tab125745960; re-mark only when continuing browser work. No response pending.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).extend([info(A / 'source-before-di7-vision-communication/PRESERVATION_MANIFEST.json'), info(preservation / 'PRESERVATION_MANIFEST.json')])
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': [], 'weeklyUsagePercent': 41, 'pendingGptReply': False}))


if __name__ == '__main__': main()
