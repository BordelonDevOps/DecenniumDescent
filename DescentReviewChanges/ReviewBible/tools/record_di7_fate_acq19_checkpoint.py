"""Record finite Fate composites and the received KEEP acquisition clarification."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest, node


def read(p):
    return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_CAST_TRANSACTIONS_AND_ACQ19_SUBMISSION.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_FATE_AND_ACQ19_CLARIFICATION.json'
    delta = A / 'DI7_FATE_ACQ19_PROGRESS_DELTA.json'
    preservation = A / 'navigation-before-di7-fate-acq19'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    state = read(previous); now = datetime.now(timezone.utc).isoformat()
    fate_path = A / 'DI7_FATE_TRANSACTIONS_CHECK.json'; fate = read(fate_path)
    received_path = A / 'DI7_ACQ19_RECEIVED.json'; received = read(received_path)
    operations_path = A / 'DI7_ACQ19_DERIVED_OPERATIONS.json'; operations = read(operations_path)
    assert fate['status'] == 'pass' and fate['checks'] == 68 and fate['historyCount'] == 34 and not fate['failures']
    for b in fate['sourceBindings']:
        assert info(G / b['path']) == b
    assert received['replyReceived'] and not received['pendingResponse'] and received['newRuleAdoptions'] == 0
    for b in [received['responseDom'], received['visibleProof'], received['exactReplacement'], received['appliedOperation'], received['currentExpectations']]:
        assert info(G / b['path']) == b
    assert len(operations['changes']) == 1
    change = operations['changes'][0]; saved = G / change['before']['preservedCopy']; p = G / change['after']['path']
    assert info(p) == change['after'] and digest(saved.read_bytes()) == change['before']['sha256']
    data = read(p)
    for op in reversed(change['operations']):
        obj, key = node(data, op['pointer']); assert obj[key] == op['replacement']; obj[key] = op['old']
    assert encoded(data) == saved.read_bytes()
    scope = ('Fate Echo now has68 checks across34 conditional histories extending the185-check/62-history DI7 casting boundary. '
        'Actual source-qualified original cast/outcome and identified observation feed the outer/child forecast, exclusive RP reservation, separate payment/history/counter windows, actual intervening Counterspell repricing, concentration and Ready preparation/release/expiry. '
        'Complete Fate Coin and Alignment Suggestion child results are exercised; source/caster/repertoire/lineage/object custody remain distinct. '
        'Other copied modes and independent engine/material requirements need their actual adapters, and the Suggestion initiative clock, Shaman totem vent, other spell payloads and full49-variant acceptance remain open. '
        'Actual GPT DI7-ACQ19 is terminal and confirms KEEP: Mirrorsage/Shaman retain rank7 minimum access19, but the hybrid fallback grants no new ranked learning addition at19 and same-or-lower replacement cannot upgrade rank6. '
        'Level20 may actually select one spell; no independent19 acquisition source is supplied, and Bloodcaller loss remains. '
        'The exact one-expectation clarification is applied to a new current expectations file and the active internal envelope, with original bytes preserved and exact inverse proof; no class/rank/cost/status changes. '
        'GPT did not rerun the185 local checks or approve the seven cards. Ordinary authored coverage412/436 remains unchanged. '
        'Fresh weekly usage39percent; stop at50 persists. Final actual joint whole-game flow precedes authorized push, verified remote and careful cosmology. Nothing deleted or pushed.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before_ledger = read(ledger_path); ledger = deepcopy(before_ledger)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [fate_path, received_path, operations_path])
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'DI7-Fate-and-ACQ19-KEEP-clarification', 'recordedAtUtc': now,
                'fateChecks': 68, 'fateConditionalHistories': 34, 'acquisitionClarificationReceived': True, 'full49Fulfilled': False, 'exactCardsApproved': False})
    for before, after in zip(before_ledger['aspects'], ledger['aspects']):
        assert all(before.get(k) == after.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if before['id'] not in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}: assert before == after
    assert {k: v for k, v in before_ledger.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_CAST_TRANSACTIONS_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "DI7_ACQ19_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_FATE_ACQ19_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status']) == 1; text = text.replace(state['status'], scope, 1)
    label_before = 'DI7-ACQ19 bounded source question \\u2014sent once; reply pending'
    assert text.count(label_before) == 1; text = text.replace(label_before, 'DI7-ACQ19 original question \\u2014see received KEEP clarification')
    marker = '    pending = [\n'; assert text.count(marker) == 1
    items = [('Fate Echo paid composites and Ready —68 checks in34 conditional histories', fate_path),
        ('DI7-ACQ19 received KEEP ruling —rank eligibility is not acquisition', received_path),
        ('DI7-ACQ19 exact expectation change —preserved original and inverse proof', operations_path),
        ('DI7-ACQ19 completed GPT response —visible proof', A / 'DI7_ACQ19_RECEIVED.png')]
    text = text.replace(marker, marker + ''.join('        (' + json.dumps(label) + ', ' + json.dumps(p.relative_to(A).as_posix()) + '),\n' for label, p in items))
    compile(text, str(nav), 'exec'); preserved = []
    for p in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        dest = preservation / p.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(p.read_bytes())
        assert dest.read_bytes() == p.read_bytes(); preserved.append({**info(p), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text, encoding='utf-8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': [{'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [ledger_path, nav]],
        'allOtherAspectsUnchanged': True, 'allClosureAndHumanEvidenceUnchanged': True, 'sourceInformationDeleted': 0, 'spellPromotions': 0}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations', []).append(deepcopy(state['activeGptReview']))
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), goalTurnClassification='progress', previousGoalTurnClassification='progress', status=scope,
        coverageLedger=info(ledger_path), coverageDelta=info(delta),
        navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        di7FateTransactions={'report': info(fate_path), 'checks': 68, 'histories': 34, 'completedChildModes': fate['completedChildModes'], 'full49Fulfilled': False},
        di7AcquisitionClarification=received,
        newRuleAdoptions=0, newRuleAdoptionCountScope='Finite Fate behavior and exact KEEP clarification only. No new learning grant or exact-card approval.')
    state['di7CastTransactions']['laterAcquisitionRuling'] = info(received_path)
    state['activeGptReview'].update(status='DI7-ACQ19-terminal-KEEP-clarification-received-applied', currentObservation=info(received_path),
        pendingResponse=False, replyReceived=True, instruction='DI7-ACQ19 is received and applied. Do not resend. Finish meaningful finite49-variant follow-through, then submit all seven assembled cards for separate exact review.')
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_FATE_AND_ACQ19_CLARIFICATION. Latest fresh weekly usage39percent; owner stop at50 remains mandatory.',
        'Actual GPT DI7-ACQ19 is terminal. Exact one-expectation KEEP clarification applied; no new19 learning grant. Current expectations: data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json. Original source expectations and prior internal envelope are preserved.',
        'Continue Premonition Shield actual occurrence/prevention/replacement/suppression and information spells Mass/Vision/Faction/Supreme. Integrate existing paid casting and the source-qualified conditional facts. Full49 variants remain incomplete.',
        'Fate evidence68/34 executes original Fate Coin/Alignment Suggestion, identified observation, outer+child payments/reservations/counters, repricing after real Counterspell, concentration, Ready and source-owned effects. Other copied modes/material/engine predicates require real adapters; no blanket full-spell implementation.',
        'Fulfill the clarified acquisition row for each of seven IDs, including denied19 same-or-lower replacement and one selected20 spell. Existing positive hybrid cases use20; avoid inventing an independent19 source.',
        'Suggestion initiative/virtual-phase clock and actual Shaman totem ordinary-cast vent still need integration. Preserve the separately successful64-behavior/26-history alignment component and185/62 casting reports with their stated limits.',
        'Do not rerun successful write-once scripts/reports. Source changes need preserved before bytes and measured same-path deltas in navigation chain; never replace historical hashes with current ones.',
        'Chrome3 live tab125745952 is the same Calibration Review Part2; re-mark on next browser turn. No response pending. Next substantive submission is the seven complete exact candidates after49-variant follow-through, not a repeat source conference.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).extend([info(A / 'source-before-di7-acq19-clarification/PRESERVATION_MANIFEST.json'), info(preservation / 'PRESERVATION_MANIFEST.json')])
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': [], 'weeklyUsagePercent': 39, 'pendingGptReply': False}))


if __name__ == '__main__': main()
