"""Record the received Shield amendment, finite follow-through and all7 ACQ checks."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest, node


def read(p): return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_SHIELD_TRANSACTIONS.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_SHIELD_RULING_AND_ALL7_ACQUISITION.json'
    delta = A / 'DI7_SHIELD_LATE_ACQUISITION_PROGRESS_DELTA.json'
    preservation = A / 'navigation-before-di7-shield-late-acquisition'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    now = datetime.now(timezone.utc).isoformat(); state = read(previous)
    shield_path = A / 'DI7_SHIELD_LATE_TRANSACTIONS_CHECK.json'; shield = read(shield_path)
    acq_path = A / 'DI7_ALL_SEVEN_ACQUISITION_CHECK.json'; acq = read(acq_path)
    received_path = A / 'DI7_SHIELD_LATE_ADMISSION_RECEIVED.json'; received = read(received_path)
    operations_path = A / 'DI7_SHIELD_LATE_DERIVED_OPERATIONS.json'; operations = read(operations_path)
    assert shield['status'] == acq['status'] == 'pass' and not shield['failures'] and not acq['failures']
    assert (shield['checks'], shield['historyCount'], acq['checks'], acq['historyCount']) == (95, 36, 385, 77)
    for report in [shield, acq]:
        for binding in report['sourceBindings']: assert info(G / binding['path']) == binding
    assert received['replyReceived'] and not received['pendingResponse'] and received['newRuleAdoptions'] == 1
    assert len(operations['changes']) == 4
    for change in operations['changes']:
        saved = G / change['before']['preservedCopy']; current = G / change['after']['path']
        assert digest(saved.read_bytes()) == change['before']['sha256'] and info(current) == change['after']
        if current.suffix == '.json':
            inverse = read(current)
            for op in reversed(change['operations']):
                obj, key = node(inverse, op['pointer']); assert obj[key] == op['replacement']
                if op.get('add'): del obj[key]
                else: obj[key] = op['old']
            assert encoded(inverse) == saved.read_bytes()
        else:
            inverse = current.read_text(encoding='utf-8')
            for op in reversed(change['operations']):
                assert inverse.count(op['replacement']) == 1; inverse = inverse.replace(op['replacement'], op['old'], 1)
            assert inverse.encode() == saved.read_bytes()
    scope = ('Actual GPT DI7-SHIELD-LATE-01 is received and applied: the recipient first-component admission closes across Shield applications, including no-admission; later suppression recovery/new establishment/replacement cannot reopen it. '
        'An already admitted same live ward can resume after suppression before expiry, including its second occurrence; replacement inherits no coverage. '
        'One NEW minimal family-wide admission completion supplements KEEP timing. Exact insertion and suppression sentence are propagated to public/internal/manuscript, with current expectation supplement4, preserved bytes and inverse proof for all4 changed files. Original16groups/49variants and source histories remain unchanged. '
        'Updated Shield evaluator95 checks/36 conditional histories exercises A/B1/B2/C, failed/countered replacement, per-recipient and positive-share checkpoints plus the earlier bounded suite. Incoming spell schedules/retarget/transfer eligibility and intervening legal timing remain explicit premises, not newly granted action windows. '
        'All-seven acquisition matrix385 checks/77 conditional histories executes below-class gates, no19 learning or cast, actual known lower-rank replacement rejection, actual selected20, lost provider/Bloodcaller, same-rank replacement and no refill of learning slots. The6-to7 impossibility is a separate exhaustive rank-bound proof, not an invented learned rank6 Mirrorsage card or full rest simulation. '
        'No full49(+4supplement) closure or exact seven approval. Ordinary authored coverage412/436 remains unchanged. Fresh weekly usage40percent; stop at50 persists. '
        'Final actual joint whole-game flow precedes authorized push, verified remote and careful cosmology. Nothing deleted or pushed.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before = read(ledger_path); ledger = deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [received_path, operations_path, shield_path, acq_path])
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'DI7-Shield-ruling-and-all7-acquisition', 'recordedAtUtc': now,
                'shieldChecks': 95, 'shieldConditionalHistories': 36, 'acquisitionChecks': 385, 'acquisitionConditionalHistories': 77,
                'timingSourceQuestionPending': False, 'newRuleAdoptions': 1, 'full49Fulfilled': False, 'exactCardsApproved': False})
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if old['id'] not in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_SHIELD_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "DI7_SHIELD_LATE_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_SHIELD_LATE_ACQUISITION_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status']) == 1; text = text.replace(state['status'], scope, 1)
    pending_label = 'Shield late-first-admission question \\u2014sent once; source reply pending'
    assert text.count(pending_label) == 1; text = text.replace(pending_label, 'Original Shield timing question \\u2014see received applied amendment')
    marker = '    pending = [\n'; assert text.count(marker) == 1
    items = [('Shield timing source ruling received —family-wide first-admission closure', received_path),
        ('Shield exact operative amendments —preservation and inverse proof', operations_path),
        ('Current Shield evaluator —95 checks in36 conditional histories', shield_path),
        ('All-seven acquisition matrix —385 checks in77 conditional histories', acq_path),
        ('Shield timing ruling —visible completed GPT response', A / 'DI7_SHIELD_LATE_ADMISSION_RECEIVED.png')]
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
    state.setdefault('priorCompletedGptObservations', []).append(deepcopy(state['activeGptReview']))
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), goalTurnClassification='progress', previousGoalTurnClassification='progress', status=scope,
        coverageLedger=info(ledger_path), coverageDelta=info(delta),
        navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        di7ShieldTimingRuling=received,
        di7ShieldCurrentTransactions={'report': info(shield_path), 'checks': 95, 'histories': 36, 'currentModule': info(R / 'tools/di7_shield_late_transactions.py'), 'full49Fulfilled': False},
        di7AllSevenAcquisition={'report': info(acq_path), 'checks': 385, 'histories': 77, 'rank6Qualification': acq['qualification']},
        newRuleAdoptions=1, newRuleAdoptionCountScope='DI7-SHIELD-LATE-01 family-wide negative-admission/replacement completion only; no new acquisition grant.')
    state['activeGptReview'].update(status='DI7-SHIELD-LATE-01-terminal-received-applied-conditional-followthrough-complete', currentObservation=info(received_path),
        pendingResponse=False, replyReceived=True, browserId='3', tabId='125745960',
        instruction='DI7-SHIELD-LATE-01 is received and applied with95/36 local conditional evidence. Do not resend. Continue remaining substantive spell work, then exact seven-card review after finite follow-through.')
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_SHIELD_RULING_AND_ALL7_ACQUISITION. Latest fresh weekly usage40percent; owner stop at50 remains mandatory.',
        'Actual GPT DI7-SHIELD-LATE-01 is terminal, exact2 operative text edits applied and four focused expectations added. Original49 remain intact. Source-before-di7-shield-late preserves all4 files; navigation chain includes that delta.',
        'Use di7_shield_late_transactions.ShieldLateTransactions as current evaluator. The original module/report68/27 are preserved pre-ruling history. Current95/36 includes closed no-admission, replacement noninheritance, same-record resume, own recipient and positive-share checkpoints with stated upstream premises.',
        'All7 ACQ19 check385/77 is complete for its stated scope; actual no18/no19/selected20/lost-provider/Bloodcaller and same-rank replacement histories, plus separate exhaustive lower-rank6-bound proof. Do not mislabel the proof as a learned rank6 Mirrorsage grant or a simulated rest.',
        'Continue Mass Revelation, Vision Quest, Faction Omniscience and Resonance Sight Supreme payloads using paid casting and source-qualified protected facts. Suggestion initiative/virtual-phase clock and actual Shaman totem ordinary vent remain open. Compile49+4 finite evidence before separate exact seven-card review.',
        'Current candidate sourceDirectionAddenda identifies the Shield authority; original sourceDirectionBinding and historical envelopes remain exact base-direction history, not silently overwritten.',
        'Do not rerun successful write-once builders/reports. Preserve before bytes and measured same-path deltas. No status promotion or full-game gate without actual evidence.',
        'Chrome3 tab125745960 is the same Calibration Review Part2; re-mark if continuing browser work. No response pending.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).extend([info(A / 'source-before-di7-shield-late/PRESERVATION_MANIFEST.json'), info(preservation / 'PRESERVATION_MANIFEST.json')])
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': [], 'weeklyUsagePercent': 40, 'pendingGptReply': False}))


if __name__ == '__main__': main()
