"""Save casting-boundary progress and the actual bounded GPT acquisition question."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p):
    return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_CANDIDATE_ASSEMBLY_AND_ALIGNMENT_COMPONENT.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_CAST_TRANSACTIONS_AND_ACQ19_SUBMISSION.json'
    delta = A / 'DI7_CAST_TRANSACTIONS_PROGRESS_DELTA.json'
    submission = A / 'DI7_ACQ19_SUBMISSION.json'
    preservation = A / 'navigation-before-di7-cast-transactions'
    assert all(not p.exists() for p in [checkpoint, delta, submission, preservation])
    state = read(previous); now = datetime.now(timezone.utc).isoformat()
    report_path = A / 'DI7_CAST_TRANSACTIONS_CHECK.json'; report = read(report_path)
    assert report['status'] == 'pass' and report['checks'] == 185 and report['historyCount'] == 62 and not report['failures']
    for b in report['sourceBindings']:
        assert info(G / b['path']) == b
    archive = A / 'DD_DI7_ACQ19_Clarification.zip'
    assert archive.stat().st_size == 165813 and digest(archive.read_bytes()) == 'd6975cff7f2dee1281f1188a468d9db39940cea6e6e84300109b98225cbc09cc'
    manifest_path = A / 'di7-acquisition-19-question/PACKAGE_MANIFEST.json'; manifest = read(manifest_path)
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == 15 and len(set(z.namelist())) == 15 and manifest['payloadCount'] == 14
        for row in manifest['files']:
            data = z.read(row['path']); assert len(data) == row['bytes'] and digest(data) == row['sha256']
    dom_path = A / 'DI7_ACQ19_SENT_DOM.txt'; screenshot = A / 'DI7_ACQ19_SENT.png'; dom = dom_path.read_text(encoding='utf-8')
    assert 'DI7-ACQ19' in dom and 'DD_DI7_ACQ19_Clarification.zip' in dom and 'ChatGPT is responding' in dom and 'button "Stop"' in dom and screenshot.exists()
    receipt = {'recordedAtUtc': now, 'reviewId': 'DI7-ACQ19', 'status': 'submitted-once-reply-observed-running',
        'archive': info(archive), 'manifest': info(manifest_path), 'payloadsVerified': 14,
        'question': info(A / 'di7-acquisition-19-question/QUESTION.md'), 'visibleProof': info(screenshot), 'sentDOM': info(dom_path),
        'browserId': '3', 'tabId': '125745952', 'conversationUrl': state['activeGptReview']['conversationUrl'],
        'recovery': 'Previous handoff tab no longer existed; listed existing tab timed out. A fresh view of the exact same conversation recovered it. This new bounded question was sent once; the earlier source conference was not resent.',
        'scope': 'Confirm the distinction between minimum rank access19 and actual repertoire acquisition for Mirrorsage/Shaman under the existing even-level fallback. No seven-card or335 exact approval requested.',
        'pendingResponse': True, 'replyReceived': False, 'sevenCardExactReviewSubmitted': False, 'fullFiniteFulfilled': False,
        'sourceInformationDeleted': 0, 'cosmologyReviewed': False, 'pushed': False}
    submission.write_bytes(encoded(receipt))
    scope = ('DI7 casting follow-through now has185 checks across62 explicitly conditional histories. '
        'The evaluator executes source-qualified ranked learning, Wizard book study/preparation, body/V/S/F/target gates, Action/Reaction/RP commitments, Dissonance/Refrain, protected Wizard first-family strain, concentration displacement and nested ordinary Counterspell with Core task degrees. '
        'Six spells reach a separately marked payload boundary; Fate Echo deliberately rejects a standalone outer cast until its atomic child/reservation/Ready adapter exists. '
        'No payload or full49-variant fulfillment is claimed. The unchanged source tables distinguish rank7 access at19 from new known-spell additions at even levels for Mirrorsage/Shaman; positive ordinary learned fixtures use20. '
        'A single bounded DI7-ACQ19 question with14 verified source/evidence payloads was sent to actual GPT in the same Calibration Review Part2; the reply was visibly responding. '
        'The original DI7 source verdict remains received; no duplicate source conference or full335 review was sent. '
        'Seven candidates remain unapproved, ordinary authored coverage412/436 unchanged, and the owner50percent stop remains controlling with fresh usage37percent. '
        'Final actual joint whole-game agreement precedes authorized push, verified remote and careful cosmology. Nothing deleted or pushed.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before_ledger = read(ledger_path); ledger = deepcopy(before_ledger)
    for row in ledger['aspects']:
        if row['id'] in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [report_path, submission])
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'DI7-cast-transactions-and-ACQ19-question', 'recordedAtUtc': now, 'checks': 185,
                'conditionalHistories': 62, 'payloadsExecuted': False, 'fullFiniteFulfilled': False, 'boundedGptQuestionSubmitted': True})
    for before, after in zip(before_ledger['aspects'], ledger['aspects']):
        assert all(before.get(k) == after.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if before['id'] not in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}: assert before == after
    assert {k: v for k, v in before_ledger.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_CANDIDATE_ASSEMBLY_PROGRESS_DELTA.json")["changes"]\n'; assert text.count(chain) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "DI7_CAST_TRANSACTIONS_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status']) == 1; text = text.replace(state['status'], scope, 1)
    marker = '    pending = [\n'; assert text.count(marker) == 1
    items = [('DI7 actual conditional cast commitments and nested counters —185 checks', report_path),
        ('DI7-ACQ19 bounded source question —sent once; reply pending', submission),
        ('DI7-ACQ19 complete source packet', archive), ('DI7-ACQ19 visible dispatch proof', screenshot)]
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
        di7CastTransactions={'report': info(report_path), 'checks': 185, 'histories': 62, 'payloadsExecuted': False, 'fullFiniteFulfilled': False, 'acquisitionQuestion': info(submission)},
        activeGptReview={**receipt, 'instruction': 'Observe the existing live DI7-ACQ19 reply; do not resend. The seven-card source conference is already complete, and exact-card submission still waits for finite follow-through.'},
        newRuleAdoptions=0, newRuleAdoptionCountScope='Conditional casting evidence and one bounded acquisition question only; no source rule or approval changes.')
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_CAST_TRANSACTIONS_AND_ACQ19_SUBMISSION. Latest fresh weekly usage37percent; at50 save and pause under owner instruction.',
        'Use computer-use/browser3, live tab125745952, same Calibration Review Part2. Re-mark the tab for continuation. DI7-ACQ19 was sent once with14 payloads,165813-byte archive SHAd6975cff7f2dee1281f1188a468d9db39940cea6e6e84300109b98225cbc09cc. Reply was visibly responding. Observe it before acting; no resubmission.',
        'Continue Fate Echo atomic forecast/reservation, original observation, actual child payment/payload and Ready adapter on top of the source-bound casting model. Existing evaluator deliberately rejects standalone Fate outer casting.',
        'DI7_CAST_TRANSACTIONS_CHECK is185/62. It executes actual conditional learning/preparation/payment/counters but ends six DI7 spells at a payload boundary. Full payloads, totem aura integration, alignment clock/cast integration and all49 expectations remain.',
        'Keep the earlier182 assembly and64 alignment behavior/26-history evidence with explicit limits. Do not rerun or overwrite successful one-use scripts/reports.',
        'Known-spell acquisition finding is submitted for GPT confirmation, not a new rule: access19 does not supply an odd-level learning addition. Level20 positive fixtures and missing-level19-route rejection preserve current fallback.',
        'After complete finite49-variant follow-through, send all seven complete cards/public/internal envelopes for separate exact review. Then continue the wider full-feat, bestiary, Director and packaging work.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).append(info(preservation / 'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': [], 'pendingGptReview': 'DI7-ACQ19'}))


if __name__ == '__main__':
    main()
