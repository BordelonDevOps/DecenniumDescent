"""Record the preserved first return and live repair conference without adoption."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    now = datetime.now(timezone.utc).isoformat()
    receipt = A / 'BANISHMENT_REPAIR_02_SUBMISSION_RECEIPT.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_BANISHMENT_REPAIR_02_SUBMISSION.json'
    delta = A / 'BANISHMENT_REPAIR_02_NAVIGATION_DELTA.json'
    keep = A / 'navigation-before-banishment-repair-02'
    assert not any(p.exists() for p in [receipt, checkpoint, delta, keep])
    native = A / 'BANISHMENT_REPAIR_02_NATIVE_DELIVERY.json'
    request = A / 'BANISHMENT_REPAIR_02_REQUEST.txt'
    dom = A / 'BANISHMENT_REPAIR_02_SUBMITTED_DOM.txt'
    proof = A / 'PART4_BANISHMENT_REPAIR_02_SUBMITTED.jpg'
    audit = A / 'BANISHMENT_CURRENT_REVIEW_01_LOCAL_AUDIT.json'
    delivery = read(native)
    turn = delivery['turns'][0]
    assert turn['items'][0]['content'][0]['text'] == request.read_text(encoding='utf8').rstrip()
    assert 'button "Stop"' in dom.read_text(encoding='utf8')
    assert read(audit)['failureCount'] == 0 and read(audit)['semanticFindingCount'] == 5
    rec = {
        'recordedAtUtc': now, 'threadTitle': delivery['thread']['title'],
        'threadId': delivery['thread']['id'], 'userTurnId': turn['id'],
        'browserId': '3', 'tabId': '125746308',
        'conversationUrl': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
        'request': info(request), 'nativeDelivery': info(native),
        'exactRequestDeliveryVerified': True, 'liveObservation': info(dom), 'proof': info(proof),
        'generationConfirmedLiveAtObservation': True,
        'firstReturn': info(A / 'DD_Banishment_Current_Review_01_Return.zip'),
        'localAudit': info(audit), 'structuralChecks': 88, 'structuralFailures': 0,
        'semanticFindings': 5, 'expectedReturn': 'DD_Banishment_Repair_02_Return.zip',
        'banishmentAdopted': False, 'sourceInformationDeleted': 0,
        'runtimeTestsExecuted': 0, 'humanPlaytested': False,
    }
    receipt.write_bytes(encoded(rec))
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC4_APPLICATION_BANISHMENT_SUBMISSION_01.json'
    start = G / 'START_HERE.md'
    nav = R / 'tools/build_review_map.py'
    ledger = R / 'data/playtest/game_development_coverage.json'
    originals, saved = {}, []
    for p in [start, nav, ledger, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        raw = p.read_bytes()
        q = keep / p.relative_to(G)
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_bytes(raw)
        originals[p] = raw
        saved.append({**info(p), 'preservedCopy': q.relative_to(G).as_posix()})
    (keep / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text = originals[start].decode()
    old = previous.relative_to(G).as_posix()
    assert text.count(old) == 1
    text = text.replace(old, checkpoint.relative_to(G).as_posix(), 1)
    begin = text.index('**Active spell review:**')
    end = text.index('\n\n', begin)
    text = text[:begin] + '**Active spell review:** The [complete 15-spell AC4 chapter](DescentReviewChanges/ReviewBible/docs/spells/candidates/ABJURATION_CONJURATION_RANK4_REVIEWED_03.md) remains exactly accepted and locally integrated. **Banishment is under repair in Review Continuation Part 4.** Its [first GPT return and local audit](docs/audit/2026-10-08/full-game/BANISHMENT_CURRENT_REVIEW_01_LOCAL_AUDIT.json) preserve all 49 sources and 28 historical scenarios; 88 source/output/preservation checks pass. Five findings remain: finite closure when no physical space fits, exact Paladin restriction scope, escape/empty-cell lifecycle, case-ledger/source-reference defects, and incomplete concrete examples. The [repair request is delivered and GPT is responding](docs/audit/2026-10-08/full-game/BANISHMENT_REPAIR_02_SUBMISSION_RECEIPT.json). Banishment remains unadopted; no runtime or human tests are claimed.' + text[end:]
    start.write_text(text, encoding='utf8', newline='\n')
    cov = json.loads(originals[ledger])
    before = deepcopy(cov)
    for ident in ['DD-11', 'DD-12']:
        row = next(r for r in cov['aspects'] if r['id'] == ident)
        prior = deepcopy(row)
        row['validationEvidence'].extend([audit.relative_to(G).as_posix(), receipt.relative_to(G).as_posix()])
        row.setdefault('currentEvidenceAddenda', []).append({
            'id': 'banishment-first-return-repair02', 'recordedAtUtc': now,
            'structuralChecks': 88, 'structuralFailures': 0, 'semanticFindings': 5,
            'reviewedSpells': 434, 'pendingSpells': 414, 'banishmentAdopted': False,
            'runtimeTestsExecuted': 0, 'humanPlaytested': False,
        })
        assert all(row[k] == prior[k] for k in ['status', 'closure', 'humanEvidence', 'completionClass'])
    assert [r for r in cov['aspects'] if r['id'] not in ['DD-11', 'DD-12']] == [r for r in before['aspects'] if r['id'] not in ['DD-11', 'DD-12']]
    ledger.write_bytes(encoded(cov))
    scope = 'AC4 remains accepted/applied:434 reviewed/414 pending ordinary spells. Banishment first return preserved;88 structural checks pass but five semantic/evidence repairs are required. Repair02 delivered to actual Part4 and generation observed live. No Banishment adoption or runtime/human/balance/canon/whole-game/publication approval.'
    code = originals[nav].decode()
    tail = ' + read(A / "AC4_APPLICATION_BANISHMENT_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail) == 1
    code = code.replace(tail, tail.rstrip('\n') + ' + read(A / "BANISHMENT_REPAIR_02_NAVIGATION_DELTA.json")["changes"]\n', 1)
    values = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant) and k.value == 'notebookReview']
    assert len(values) == 1
    code = code.replace(ast.get_source_segment(code, values[0]), repr(scope), 1)
    items = [('Banishment — first return,88 checks and five required repairs', audit.name), ('Banishment — active Repair02 conference', receipt.name)]
    code = code.replace('    pending = [\n', '    pending = [\n' + ''.join('        ' + repr(x) + ',\n' for x in items), 1)
    compile(code, str(nav), 'exec')
    nav.write_text(code, encoding='utf8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': [{'before': next(x for x in saved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, ledger, nav]], 'sourceInformationDeleted': 0, 'newSpellAdoptions': 0, 'fullDomainClosureChanged': False}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf8')
    assert run.returncode == 0, (run.stdout[-1500:], run.stderr[-1500:])
    build = read(A / 'REVIEW_MAP_BUILD.json')
    assert not build['missingLinks']
    state = read(previous)
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), status=scope,
                 goalTurnClassification='progress', previousGoalTurnClassification='progress',
                 coverageDelta=info(delta), coverageLedger=info(ledger), ownerStartPage=info(start),
                 newRuleAdoptions=0, newRuleAdoptionScope='No new rules adopted; Banishment first return requires repair.',
                 navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': build['existingDistinctLinks'], 'missingLinks': []})
    state['banishmentFirstReturnAudit'] = {'archive': rec['firstReturn'], 'audit': info(audit), 'status': 'Preserved, independently reviewed; five repair findings, not jointly accepted.'}
    state['activeGptReview'] = {
        'reviewId': 'BANISHMENT-REPAIR-02', 'threadId': rec['threadId'], 'title': rec['threadTitle'],
        'browserId': '3', 'tabId': '125746308', 'conversationUrl': rec['conversationUrl'],
        'submission': info(receipt), 'userTurnId': rec['userTurnId'],
        'status': 'Actual browser confirmed generating; exact submitted request verified against native user turn.',
        'generationConfirmedLiveAtObservation': True, 'expectedReturn': rec['expectedReturn'],
        'returnReceived': False, 'newRulesAdopted': False,
    }
    state['safeNextActions'] = [
        'Read the SAME live Part4 response to user turn ' + rec['userTurnId'] + '; do not submit duplicate review or treat native idle as terminal.',
        'Preserve DD_Banishment_Repair_02_Return.zip when complete. Verify original49source bindings, unchanged ordinary source/access and all28 historical scenarios; review all30 current cases plus added BAN-X cases and five repair dispositions.',
        'Independently resolve finite closure under physical exhaustion, exact No Escape/Verdict Absolute/Reign of Ashes predicates, primary escape/empty-cell lifecycle, corrected ledgers/sourceRefs and actual costs/geometry. First return is NOT accepted.',
        'AC4 is already accepted/applied;434 reviewed/414 pending. No rerunning one-shot application scripts. Continue remaining spell groups and full75-area backlog after this review. Latest verified GitHub backup18c6e3a; later work remains local.',
    ]
    state['resumedBlockedAudit'] = {'classification': 'progress', 'evidence': info(audit), 'meaningfulProgress': scope}
    state.setdefault('preservationManifests', []).append(info(keep / 'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'receipt': info(receipt), 'checkpoint': info(checkpoint), 'links': build['existingDistinctLinks'], 'missingLinks': 0, 'newRulesAdopted': False}))


if __name__ == '__main__':
    main()
