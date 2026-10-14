"""Preserve the finite Shield evaluator and its specific unresolved source seam."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_FATE_AND_ACQ19_CLARIFICATION.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_SHIELD_TRANSACTIONS.json'
    delta = A / 'DI7_SHIELD_PROGRESS_DELTA.json'
    preservation = A / 'navigation-before-di7-shield'
    submission_path = A / 'DI7_SHIELD_LATE_ADMISSION_SUBMISSION.json'
    assert all(not p.exists() for p in [checkpoint, delta, preservation, submission_path])
    now = datetime.now(timezone.utc).isoformat(); state = read(previous)
    report_path = A / 'DI7_SHIELD_TRANSACTIONS_CHECK.json'; report = read(report_path)
    assert report['status'] == 'pass' and report['checks'] == 68 and report['historyCount'] == 27 and not report['failures']
    for b in report['sourceBindings']: assert info(G / b['path']) == b
    submission = {'id': 'DI7-SHIELD-LATE-01', 'recordedAtUtc': now, 'sentOnce': True,
        'question': info(A / 'DI7_SHIELD_LATE_ADMISSION_QUESTION.txt'),
        'visibleProof': info(A / 'DI7_SHIELD_LATE_ADMISSION_SENT.png'),
        'url': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'browserId': '3', 'tabId': '125745960', 'pendingResponse': True, 'replyReceived': False,
        'scope': 'Whether an already-started occurrence admits after initial suppression or newly established/replaced ward; committed same-record suppression baseline.',
        'notAnExactCardApprovalRequest': True, 'doNotResend': True}
    submission_path.write_bytes(encoded(submission))
    scope = ('Premonition Shield now has68 checks across27 conditional histories over the existing source-bound paid DI7 casting boundary. '
        'Four actual ordinary provider learning/preparation/RP/Action/strain routes establish a nonconcentration two-use ward. '
        'Automatic misses, zero-damage saves/hits and an actual paid beneficial Fate Coin consume; grouped beam roots, later scheduled tick, second-occurrence continuation/interleaved third, retarget final recipient, pre-mitigation20-to15/5 split, post-defense skip prevention, defenses/tempHP/Maiming, replacement/counter/failure, caster versus recipient death, suppression/dispel and half-open60-second expiry are exercised. '
        'Incoming attack/retarget/source-transfer legality and damaging spell schedules remain explicit upstream premises, not full source-feature execution. '
        'A previously unavailable ward becoming available during an already-started occurrence is explicitly rejected pending actual GPT DI7-SHIELD-LATE-01, sent once with the complete procedure; new/replaced applications are included in that timing question. '
        'This specific newly encountered seam supersedes the earlier next-submission-only-seven-card plan without resending any prior source conference. '
        'No candidate text or source status changed, no full49 fulfillment or exact approval. Ordinary authored coverage412/436 remains. '
        'Weekly usage39percent; stop at50 persists. Final actual joint whole-game flow precedes authorized push, verified remote and careful cosmology. Nothing deleted or pushed.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before = read(ledger_path); ledger = deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, submission_path])
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'DI7-Shield-conditional-occurrences', 'recordedAtUtc': now,
                'checks': 68, 'conditionalHistories': 27, 'timingSourceQuestionPending': True, 'full49Fulfilled': False, 'exactCardsApproved': False})
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if old['id'] not in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}: assert old == new
    assert {k: v for k, v in before.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_FATE_ACQ19_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "DI7_SHIELD_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status']) == 1; text = text.replace(state['status'], scope, 1)
    marker = '    pending = [\n'; assert text.count(marker) == 1
    items = [('Premonition Shield paid wards and conditional occurrences —68 checks in27 histories', report_path),
        ('Shield late-first-admission question —sent once; source reply pending', submission_path),
        ('Complete Shield source timing question', A / 'DI7_SHIELD_LATE_ADMISSION_QUESTION.txt'),
        ('Shield timing question submitted —visible proof', A / 'DI7_SHIELD_LATE_ADMISSION_SENT.png')]
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
        di7ShieldTransactions={'report': info(report_path), 'checks': 68, 'histories': 27, 'openSeams': report['openSeams'], 'full49Fulfilled': False},
        di7ShieldTimingQuestion=submission,
        newRuleAdoptions=0, newRuleAdoptionCountScope='Finite execution of already authored Shield source. Late-first-admission explicitly unresolved.')
    state['activeGptReview'].update(status='DI7-SHIELD-LATE-01-sent-once-source-response-pending', currentObservation=info(submission_path),
        pendingResponse=True, replyReceived=False, browserId='3', tabId='125745960', url=submission['url'],
        instruction='Read DI7-SHIELD-LATE-01 response in Calibration Review Part2. Sent once; do not resend. Preserve the exact source ruling before adapting the evaluator or candidates.')
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_SHIELD_TRANSACTIONS. Latest fresh weekly usage39percent; owner stop at50 remains mandatory.',
        'Read actual GPT DI7-SHIELD-LATE-01 from live Chrome3 tab125745960, same Part2 conversation. It is a narrow newly encountered suppression/replacement timing issue, not seven-card acceptance. Save exact response and visible proof; do not resend.',
        'Shield report68/27 is a bounded conditional reference. Paid ward/FateCoin sources and damage stages execute; incoming damaging spell source schedules/attack/retarget/transfer eligibility remain explicit supplied premises. Initial-unavailable then late-first-admission rejects pending ruling; do not claim full49.',
        'If the source ruling adds text, preserve all active candidate bytes first, apply exact guarded source operations to public/internal/guide counterparts with inverse proof and navigation delta. Original source verdict and proposal remain historical.',
        'Continue information spells Mass/Vision/Faction/Supreme with the paid casting boundary and source-qualified conditional facts, then the complete49-variant evidence matrix and separate exact seven-card review.',
        'ACQ19 is terminal KEEP and applied. Fulfill all7 per-ID acquisition negative18/19/replacement cases and actual selected20 choices; no independent19 grant. Suggestion initiative/virtual-phase clock and actual Shaman totem ordinary vent remain open.',
        'Do not rerun successful write-once scripts/reports. Preserve before bytes and measured same-path deltas. Counts/status/closure/human flags stay unchanged unless their actual gates are met.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).append(info(preservation / 'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': [], 'weeklyUsagePercent': 39, 'pendingGptReply': True}))


if __name__ == '__main__': main()
