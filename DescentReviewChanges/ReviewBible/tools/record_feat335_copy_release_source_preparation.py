"""Index a prepared source clarification without claiming a sent review."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_EXACT_SUBMISSION.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_COPY_RELEASE_QUESTIONS.json'
    delta = A / 'FEAT335_COPY_RELEASE_QUESTIONS_PROGRESS_DELTA.json'
    preservation = A / 'navigation-before-copy-release-questions'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    state = read(previous); now = datetime.now(timezone.utc).isoformat()
    preparation = A / 'FEAT335_COPY_RELEASE_SOURCE_01_PREPARATION.json'
    packet = read(preparation)
    assert packet['status'] == 'prepared-not-sent' and packet['payloadsVerified'] == 23
    assert packet['sourceFilesUnchanged'] and len(packet['currentOperativeParity']) == 3
    for key in ['archive', 'manifest', 'request', 'context']:
        assert info(G / packet[key]['path']) == packet[key]
    context = read(G / packet['context']['path'])
    for b in context['sourceBindings']: assert info(G / b['path']) == b
    scope = ('DI7 exact seven-card review remains sent once and pending in Calibration Review Part2. '
        'Independent feat-copy source audit prepared FEAT335-COPY-RELEASE-SOURCE-01 with23 verified payloads. '
        'The three current complete feat procedures exactly match their acquisition contracts. '
        'The request asks for an explicit canonical Refrain identity, concentration tags for all seven profiles, '
        'and the applicable feat-copy strain engine/Limit without silently merging different source formulas. '
        'No new rule or paid copy release was implemented. The packet is prepared, not sent, and must wait for '
        'the terminal DI7 reply. Historical component/capture evidence remains scoped and unchanged. '
        'Ordinary412reviewed/436pending and all closure/selection/human approval fields remain unchanged. '
        'Weekly usage47percent was checked; owner stop at50 remains mandatory. Nothing deleted or pushed; '
        'cosmology remains after final actual joint flow agreement, authorized push and verified remote.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before = read(ledger_path); ledger = deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).append(preparation.relative_to(G).as_posix())
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'copy-release-source-questions',
                'recordedAtUtc': now, 'payloadsVerified': 23, 'currentProcedureParity': 3,
                'sourceQuestions': 3, 'sent': False, 'newRules': 0, 'paidReleaseExecuted': False})
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if old['id'] not in {'DD-14', 'DD-69'}: assert old == new
    assert {k:v for k,v in before.items() if k != 'aspects'} == {k:v for k,v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "DI7_EXACT_SUBMISSION_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain) == 1 and text.count(state['status']) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "FEAT335_COPY_RELEASE_QUESTIONS_PROGRESS_DELTA.json")["changes"]\n')
    text = text.replace(state['status'], scope, 1)
    marker = '    pending = [\n'; assert text.count(marker) == 1
    items = [('Prepared copy-release source questions — not sent', preparation),
             ('Complete copy-release source question archive', G / packet['archive']['path']),
             ('Three exact source questions and scope', G / packet['request']['path'])]
    text = text.replace(marker, marker + ''.join('        (' + json.dumps(label) + ', ' +
        json.dumps(p.relative_to(A).as_posix()) + '),\n' for label, p in items))
    compile(text, str(nav), 'exec'); preserved = []
    for p in [ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        dest = preservation / p.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(p.read_bytes()); assert dest.read_bytes() == p.read_bytes()
        preserved.append({**info(p), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text, encoding='utf-8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': [
        {'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)}
        for p in [ledger_path, nav]], 'allOtherAspectsUnchanged': True,
        'allClosureAndHumanEvidenceUnchanged': True, 'sourceInformationDeleted': 0, 'newRuleAdoptions': 0}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), status=scope,
        goalTurnClassification='progress', previousGoalTurnClassification='progress',
        coverageLedger=info(ledger_path), coverageDelta=info(delta),
        navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
                    'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        featCopyReleaseQuestions={'preparation': info(preparation), **packet})
    state['safeNextActions'] = [
        state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_COPY_RELEASE_QUESTIONS. Latest weekly usage47percent; stop at50.',
        'Continue actual pending DI7-EXACT-REVIEW-01 in Chrome3 Calibration Review Part2, tab125745960. It is still analyzing the submitted package. Do not resend on timeout; re-mark handoff.',
        'FEAT335-COPY-RELEASE-SOURCE-01 is prepared, NOT sent:23payloads; archive1768982bytes SHA922898bd1cf1fd64fb6c77639f2fdefd3266417b05344567031a5cf04b9c5196. Wait for terminal DI7 reply before sending it. Questions CRS01history identity, CRS02concentration, CRS03strain engine/Limit require actual source discussion; no unilateral rule adopted.',
        'Successful prepare_feat335_copy_release_questions.py and recorder are write-once; do not rerun or overwrite. Source rules, original contracts and historical reports unchanged; three current candidate operative pairs verified identical.',
        'When DI7 verdict arrives preserve exact reply/archive, independently verify all package hashes and guarded operations before applying. Do not treat source clarification, structural pass or seven-card verdict as whole-game approval.',
        'Owner usage stop takes priority over all work. At threshold save pending-review state, explicitly pause goal and report; do not reset or buy credits.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).append(info(preservation / 'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'],
                      'copyQuestionsSent': False, 'DI7VerdictPending': True}))


if __name__ == '__main__': main()
