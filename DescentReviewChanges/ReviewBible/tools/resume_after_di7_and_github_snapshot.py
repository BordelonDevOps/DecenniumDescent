"""Record the completed DI7 review, verified backup and resumed source conference."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PACKAGING_NAVIGATION.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_ACCEPTANCE_AND_RESUME.json'
    delta = A / 'DI7_ACCEPTANCE_RESUME_NAVIGATION_DELTA.json'
    preserved_root = A / 'navigation-before-di7-acceptance-and-resume'
    submission_path = A / 'FEAT335_COPY_RELEASE_SOURCE_01_SUBMISSION.json'
    assert all(not p.exists() for p in [checkpoint, delta, preserved_root, submission_path])
    now = datetime.now(timezone.utc).isoformat()
    state = read(previous)
    pause = read(A / 'PAUSED_AT_50_PERCENT_2026-10-13.json')
    for b in pause['bindings']:
        assert hashlib.sha256(Path(b['path']).read_bytes()).hexdigest() == b['sha256']
    acceptance_path = A / 'DI7_EXACT_ACCEPTANCE_RECEIPT.json'
    acceptance = read(acceptance_path)
    index_path = R / 'data/public/spell_playtests/authored_review_index.json'
    index = read(index_path)
    assert index['authoredCounts'] == {'reviewed': 419, 'pending': 429}
    assert len(acceptance['acceptedSpellIds']) == 7
    assert acceptance['status'] == 'exact-authored-acceptance-recorded'
    assert acceptance['operativeCorrections'] == 0 and not acceptance['runtimeSelectionEnabled']
    pact_path = A / 'FEAT335_PACT_SIGILS_CHECK.json'; pact = read(pact_path)
    assert pact['checks'] == 140 and pact['historyCount'] == 45 and not pact['failures']
    push_path = G / 'docs/audit/2026-10-14/github-snapshot/PUSH_RECEIPT.json'
    push = read(push_path)
    assert push['commit'] == push['verifiedRemoteCommit'] == 'a3f75a0ce577f51bd39153a872ef05ba9e877642'
    assert not push['wholeGameAcceptanceClaimed'] and not push['cosmologyReviewed']
    preparation = read(A / 'FEAT335_COPY_RELEASE_SOURCE_01_PREPARATION.json')
    dom_path = A / 'FEAT335_COPY_RELEASE_SOURCE_01_SENT_DOM.txt'
    proof_path = A / 'FEAT335_COPY_RELEASE_SOURCE_01_SENT.png'
    dom = dom_path.read_text(encoding='utf-8')
    assert 'ChatGPT is responding' in dom and 'button "Stop"' in dom
    assert 'DD_Feat335_Copy_Release_Source_01.zip' in dom and 'Continuation on 15 October 2026' in dom
    assert proof_path.is_file()
    submission = {'reviewId': preparation['reviewId'], 'recordedAtUtc': now,
        'status': 'sent-once-response-running-at-submission-observation', 'archive': preparation['archive'],
        'preparation': info(A / 'FEAT335_COPY_RELEASE_SOURCE_01_PREPARATION.json'),
        'payloadsVerifiedBeforeSending': 23, 'currentSourceBindingsVerified': True,
        'prompt': info(A / 'FEAT335_COPY_RELEASE_SOURCE_01_RESUMED_PROMPT.txt'),
        'sentDOM': info(dom_path), 'visibleProof': info(proof_path),
        'browserId': '3', 'tabId': '125745968', 'conversationUrl': pause['browser']['url'],
        'pendingResponseAtObservation': True, 'replyReceived': False, 'newRuleAdoptions': 0,
        'copyReleaseExecuted': False, 'fullFeatCandidateApproved': False,
        'instruction': 'Observe the same submitted conversation; do not resend after an observation timeout.'}
    scope = ('DI7 exact authored acceptance is recorded for seven complete spell procedures, all14 examples and93 expectation dispositions. '
        'Ordinary authored coverage is419 reviewed/429 pending;143 complete standalone procedures supplement276 preserved legacy operational records. '
        'The exact submitted-source verifier reproduced1819 passing checks locally; DI7-EV01 distinguishes the unsupported False Life evaluator adapter from an authored prohibition. '
        'Accepted candidate files and historical labels remain unchanged. Pact sigils have140 passing checks across45 conditional histories, not full Forbidden Pact or335-feat approval. '
        'The owner explicitly requested an unfinished-work backup; GitHub main commit a3f75a0ce577f51bd39153a872ef05ba9e877642 was pushed and remotely verified. '
        'Whole-game flow, human balance and player-only publication remain open. Development resumed15October with measured weekly usage14percent and mandatory stop50. '
        'FEAT335-COPY-RELEASE-SOURCE-01 was sent once to actual GPT and was running at submission; no answer is pre-adopted. '
        'Cosmology review is now eligible after the verified backup, but no cosmology doctrine was reviewed or changed in this reconciliation. No source information deleted.')
    start = G / 'START_HERE.md'; old_start = start.read_bytes().decode('utf-8'); new_start = old_start; replacements = []
    def replace_line(prefix, replacement):
        nonlocal new_start
        old = [x for x in new_start.splitlines() if x.startswith(prefix)]
        assert len(old) == 1, prefix
        assert new_start.count(old[0]) == 1
        new_start = new_start.replace(old[0], replacement, 1)
        replacements.append({'old': old[0], 'replacement': replacement})
    replace_line('**Current joint review:**',
        '**Current joint review:** GPT accepted all [seven DI7 exact spell procedures](docs/audit/2026-10-08/full-game/DI7_EXACT_ACCEPTANCE_RECEIPT.json). The [authored spell index](DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json) now records **419 reviewed / 429 pending**, with 143 complete standalone procedures. The [copy-release source conference](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_SUBMISSION.json) was sent once to GPT; its three questions remain unresolved pending the actual answer. All 335 feat identities retain their scoped candidate status; [Pact sigil evidence](docs/audit/2026-10-08/full-game/FEAT335_PACT_SIGILS_CHECK.json) adds 140 checks across 45 conditional histories. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_ACCEPTANCE_AND_RESUME.json). Development resumed at 14% weekly Codex usage; the owner requires stopping at **50%**.')
    replace_line('**Current position:', '**Current position: 15 October 2026.** The owner-requested progress backup is verified on GitHub. The finish line remains a coherent campaign-playtest candidate; final joint flow, human balance, publication approval and full companion implementation remain open.')
    replace_line('| Ordinary spells |', '| Ordinary spells | **419 reviewed authored procedures; 429 pending.** All 848 identities remain indexed; 143 procedures use complete standalone representations | Remaining spell development, receipt-only decisions and full runtime/class integration; ten ancestry-only spells remain separate |')
    replace_line('| Final delivery |', '| Final delivery | The [owner-requested progress backup was pushed and remotely verified](docs/audit/2026-10-14/github-snapshot/PUSH_RECEIPT.json) at `a3f75a0ce577f51bd39153a872ef05ba9e877642`. Its exact manifest records 18,899 copied source files and locally retained exceptions; no sources were deleted. This was a progress backup, not final whole-game approval. The [joint flow gate](docs/audit/2026-10-08/full-game/FINAL_FLOW_AND_GITHUB_DELIVERY.md) remains open for completion claims. Careful cosmology source review may now begin after this verified baseline. |')
    replace_line('**Player/Director delivery is still open.**', '**Player/Director delivery is still open.** The [packaging inventory](docs/audit/2026-10-08/full-game/PLAYER_DIRECTOR_PACKAGING_INVENTORY_01.json) is its historical snapshot of 51 public-data files and 79 Director-data files. Public paths include restricted candidates and do not imply approval. The current authored index combines 276 preserved legacy operational records and 143 complete standalone procedures. The GitHub progress backup contains both audiences; no separate secret-free player build is certified. Cosmology sources retain their original bytes pending the careful post-push review.')
    # A queued row must not keep presenting the just-submitted questions as unsent.
    old_phrase = '[Copy-release questions](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_PREPARATION.json) are prepared but unsent.'
    new_phrase = '[Copy-release questions were submitted once](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_SUBMISSION.json); the source answer remains pending.'
    assert new_start.count(old_phrase) == 1
    new_start = new_start.replace(old_phrase, new_phrase, 1)
    replacements.append({'old': old_phrase, 'replacement': new_phrase})
    inverse = new_start
    for op in reversed(replacements):
        assert inverse.count(op['replacement']) == 1
        inverse = inverse.replace(op['replacement'], op['old'], 1)
    assert inverse == old_start
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    before = read(ledger_path); ledger = deepcopy(before)
    ledger['activeOrdinarySpellReview'] = {'recordedAtUtc': now, 'ordinaryOperational': 419, 'ordinaryPending': 429,
        'scope': 'Current authored accounting; activeLowRankSpellReview remains the historical low-rank receipt.',
        'authoredIndex': info(index_path), 'latestAcceptance': info(acceptance_path), 'runtimeVerified': False}
    touched = {'DD-09', 'DD-12', 'DD-14', 'DD-50', 'DD-61', 'DD-65', 'DD-69'}
    for row in ledger['aspects']:
        if row['id'] in touched:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'di7-acceptance-and-post-backup-resume', 'recordedAtUtc': now,
                'acceptance': acceptance_path.relative_to(G).as_posix(), 'pactSigils': pact_path.relative_to(G).as_posix(),
                'backup': push_path.relative_to(G).as_posix(), 'cosmologyReviewed': False, 'fullDomainClosed': False})
            evidence = [acceptance_path, pact_path, push_path, submission_path]
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in evidence)
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if old['id'] not in touched: assert old == new
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "PACKAGING_OWNER_NAVIGATION_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "DI7_EXACT_ACCEPTANCE_RECORDING_OPERATIONS.json")["changes"] + read(A / "DI7_ACCEPTANCE_RESUME_NAVIGATION_DELTA.json")["changes"]\n')
    notebook_nodes = [v for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Dict) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant) and k.value == 'notebookReview']
    assert len(notebook_nodes) == 1 and isinstance(notebook_nodes[0], ast.Constant)
    original_status_literal = ast.get_source_segment(text, notebook_nodes[0])
    assert text.count(original_status_literal) == 1
    text = text.replace(original_status_literal, repr(scope), 1)
    text = text.replace('ledger["activeLowRankSpellReview"]["ordinaryOperational"]', 'ledger["activeOrdinarySpellReview"]["ordinaryOperational"]')
    text = text.replace('ledger["activeLowRankSpellReview"]["ordinaryPending"]', 'ledger["activeOrdinarySpellReview"]["ordinaryPending"]')
    marker = '    pending = [\n'; assert text.count(marker) == 1
    text = text.replace(marker, marker + '        ("DI7 exact authored acceptance — seven recorded", "DI7_EXACT_ACCEPTANCE_RECEIPT.json"),\n        ("Copy-release source conference — submitted", "FEAT335_COPY_RELEASE_SOURCE_01_SUBMISSION.json"),\n        ("Pact sigils — 140 checks, 45 conditional histories", "FEAT335_PACT_SIGILS_CHECK.json"),\n')
    compile(text, str(nav), 'exec')
    preserved = []
    for p in [start, ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        dest = preserved_root / p.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(p.read_bytes())
        assert dest.read_bytes() == p.read_bytes()
        preserved.append({**info(p), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preserved_root / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    submission_path.write_bytes(encoded(submission))
    start.write_bytes(new_start.encode('utf-8')); ledger_path.write_bytes(encoded(ledger)); nav.write_text(text, encoding='utf-8', newline='\n')
    changes = [{'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, ledger_path, nav]]
    changes[0].update(operations=replacements, inverseReconstructsExactBeforeBytes=True)
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': changes, 'sourceInformationDeleted': 0,
        'allClosureAndHumanEvidenceUnchanged': True, 'rulesChanged': 0, 'acceptedCardBytesUnchanged': True}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode: print(run.stdout[-2000:]); print(run.stderr[-5000:]); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.setdefault('priorCompletedGptObservations', []).append({'historicalSubmission': state['activeGptReview'], 'terminalAcceptance': info(acceptance_path)})
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), status=scope,
        goalTurnClassification='progress', previousGoalTurnClassification='progress',
        coverageLedger=info(ledger_path), coverageDelta=info(delta), activeGptReview=submission,
        ordinaryAuthoredCountsCurrent=index['authoredCounts'], currentAuthoredIndex=info(index_path),
        di7ExactAcceptance=info(acceptance_path), pactSigilsEvidence=info(pact_path),
        progressBackup={'receipt': info(push_path), 'commit': push['commit'], 'wholeGameAcceptance': False}, pushed=True,
        usageAtResume={'usedPercent': 14, 'windowDurationMins': 10080, 'resetsAt': 1792678562, 'stopAtUsedPercent': 50},
        higherSpellCountsSnapshotScope='Historical pre-DI7-acceptance proposal snapshot retained unchanged; use current authored index and exact acceptance for present membership.',
        navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        ownerStartPage=info(start), cosmologyReviewEligibleAfterVerifiedBackup=True, cosmologyReviewed=False)
    state['featCopyReleaseQuestions'] = {**state['featCopyReleaseQuestions'], 'status': submission['status'], 'submission': info(submission_path)}
    state['safeNextActions'] = [
        'Check weekly usage before substantial work and periodically; stop at50percent used, save progress and pause under the owner instruction. No reset or purchase.',
        'Authoritative checkpoint AFTER_DI7_ACCEPTANCE_AND_RESUME. Ordinary authored index419/429; DI7 accepted, unchanged candidates and DI7-EV01 receipt control. Do not rerun one-use completed builders or acceptance recorder.',
        'Observe actual GPT FEAT335-COPY-RELEASE-SOURCE-01 in Chrome3 tab125745968. Submitted once; revalidate live response, preserve reply and exact downloadable evidence before deriving guarded source changes.',
        'Continue all remaining spells, feats, bestiary, Director procedures, integration and packaging. No full335-feat or whole-game acceptance is established by finite suites.',
        'Verified progress-backup commit a3f75a0ce577f51bd39153a872ef05ba9e877642 satisfies the owner post-push sequencing dependency. Begin careful cosmology inventory/authority and passage comparison, keep alternatives and public/Director boundaries, confer with actual GPT before material resolution.',
        'Final actual whole-game joint flow, human playtesting and balance/publication decisions remain separate open gates. The earlier progress push did not close them.'
    ]
    state.setdefault('preservationManifests', []).append(info(preserved_root / 'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    links = []
    for op in replacements:
        for target in re.findall(r'\]\(([^)]+)\)', op['replacement']):
            if '://' in target or target.startswith('#'): continue
            p = (G / unquote(target.split('#')[0])).resolve()
            assert p.is_relative_to(G.resolve()) and p.is_file(), target
            links.append(target)
    assert info(index_path)['sha256'] == pause['indexSha256']
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'changedLinksChecked': len(set(links)), 'ordinaryAuthoredCounts': index['authoredCounts'], 'sourceInformationDeleted': 0, 'rulesChanged': 0}))

if __name__ == '__main__': main()
