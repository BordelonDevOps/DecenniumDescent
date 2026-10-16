"""Record Repair03 findings and the live same-chat Repair04 conference."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, difflib, html, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    now = datetime.now(timezone.utc).isoformat()
    receipt = A / 'BANISHMENT_REPAIR_04_SUBMISSION_RECEIPT.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_BANISHMENT_REPAIR_04_SUBMISSION.json'
    delta = A / 'BANISHMENT_REPAIR_04_NAVIGATION_DELTA.json'
    keep = A / 'navigation-before-banishment-repair-04'
    assert not any(p.exists() for p in [receipt, checkpoint, delta, keep])
    native = A / 'BANISHMENT_REPAIR_04_NATIVE_DELIVERY.json'
    request = A / 'BANISHMENT_REPAIR_04_REQUEST.txt'
    submitted = A / 'BANISHMENT_REPAIR_04_SUBMITTED_DOM.txt'
    live = A / 'BANISHMENT_REPAIR_04_LIVE_DOM.txt'
    proof = A / 'PART4_BANISHMENT_REPAIR_04_SUBMITTED.jpg'
    audit = A / 'BANISHMENT_REPAIR_03_LOCAL_AUDIT.json'
    delivery = read(native)
    turn = delivery['turns'][0]
    original = request.read_text(encoding='utf8').rstrip()
    received = turn['items'][0]['content'][0]['text']
    changes = []
    for op, i, j, k, l in difflib.SequenceMatcher(None, original, received, autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        assert (op == 'insert' and received[k:l] == '\\') or (op == 'replace' and original[i:j] == ' ' and received[k:l] == '&#x20;'), (op, original[i:j], received[k:l])
        changes.append({'operation': op, 'originalRange': [i,j], 'deliveredRange': [k,l], 'original': original[i:j], 'delivered': received[k:l]})
    assert html.unescape(received).replace('\\', '') == original
    assert 'button "Stop"' in live.read_text(encoding='utf8')
    audit_data = read(audit)
    assert audit_data['failureCount'] == 0 and audit_data['semanticFindingCount'] == 4
    rec = {
        'recordedAtUtc': now, 'threadTitle': delivery['thread']['title'], 'threadId': delivery['thread']['id'],
        'userTurnId': turn['id'], 'browserId': '3', 'tabId': '125746308',
        'conversationUrl': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
        'request': info(request), 'nativeDelivery': info(native),
        'deliveryVerification': {'literalByteEquality': original == received, 'allContentPreserved': True, 'normalization': 'UI Markdown escape insertion only; complete exact diff recorded; unescape restores the original text.', 'differences': changes},
        'submissionObservation': info(submitted), 'liveObservation': info(live), 'proof': info(proof),
        'generationConfirmedLiveAtObservation': True,
        'preservedRepair03': info(A / 'DD_Banishment_Repair_03_Return.zip'),
        'localAudit': info(audit), 'structuralChecks': audit_data['checkCount'], 'structuralFailures': 0, 'semanticFindings': 4,
        'expectedReturn': 'DD_Banishment_Repair_04_Return.zip', 'banishmentAdopted': False,
        'sourceInformationDeleted': 0, 'runtimeTestsExecuted': 0, 'humanPlaytested': False,
    }
    receipt.write_bytes(encoded(rec))
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_BANISHMENT_REPAIR_03_AC5_PREPARATION.json'
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
    assert text.count(previous.relative_to(G).as_posix()) == 1
    text = text.replace(previous.relative_to(G).as_posix(), checkpoint.relative_to(G).as_posix(), 1)
    begin = text.index('**Active spell review:**')
    end = text.index('\n\n', begin)
    text = text[:begin] + '**Active spell review:** The accepted 15-spell AC4 module remains applied. **Banishment Repair04 is live in Review Continuation Part 4.** [Repair03 is preserved and independently audited](docs/audit/2026-10-08/full-game/BANISHMENT_REPAIR_03_LOCAL_AUDIT.json): 214 source/output/preservation/reference checks pass; all49 sources,35 case IDs and28 historical scenarios are retained. Four bounded issues remain: the Oracle reroll cites the wrong current card/frequency; old reservation language survives in one example; three geometry examples need correction; and new physical-conflict semantics must preserve actual location and usable source predicates. [The same-chat correction request is confirmed delivered](docs/audit/2026-10-08/full-game/BANISHMENT_REPAIR_04_SUBMISSION_RECEIPT.json). Banishment remains unadopted; finite ending and the real nonconcentration familiar escape are retained candidate improvements.' + text[end:]
    start.write_text(text, encoding='utf8', newline='\n')
    cov = json.loads(originals[ledger])
    before = deepcopy(cov)
    for ident in ['DD-11', 'DD-12']:
        row = next(r for r in cov['aspects'] if r['id'] == ident)
        prior = deepcopy(row)
        row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [audit, receipt])
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'banishment-repair04-conference', 'recordedAtUtc': now, 'structuralChecks': 214, 'structuralFailures': 0, 'semanticFindings': 4, 'currentCasesRead': 35, 'banishmentAdopted': False, 'runtimeTestsExecuted': 0})
        assert all(row[k] == prior[k] for k in ['status', 'closure', 'humanEvidence', 'completionClass'])
    assert [r for r in cov['aspects'] if r['id'] not in ['DD-11','DD-12']] == [r for r in before['aspects'] if r['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    scope = '434 reviewed/414 pending ordinary spells. Banishment Repair03 preserved:214 structural checks pass,49 sources/35 cases/28 historical scenarios retained; four bounded semantic corrections sent and live as Repair04 in the same actual GPT continuation. No new adoption or runtime/human/balance/canon/whole-game/publication approval. Full16-spell AC5 preparation remains unsent.'
    code = originals[nav].decode()
    tail = ' + read(A / "BANISHMENT_REPAIR_03_AC5_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail) == 1
    code = code.replace(tail, tail.rstrip('\n') + ' + read(A / "BANISHMENT_REPAIR_04_NAVIGATION_DELTA.json")["changes"]\n', 1)
    values = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value == 'notebookReview']
    assert len(values) == 1
    code = code.replace(ast.get_source_segment(code,values[0]),repr(scope),1)
    items = [('Banishment — Repair03 independent audit and four corrections',audit.name),('Banishment — active Repair04 conference',receipt.name)]
    code = code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec')
    nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]],'sourceInformationDeleted':0,'newSpellAdoptions':0,'fullDomainClosureChanged':False}))
    run = subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode == 0,(run.stdout[-1000:],run.stderr[-1000:])
    build = read(A/'REVIEW_MAP_BUILD.json')
    assert not build['missingLinks']
    state = read(previous)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='No new rules adopted; Banishment Repair04 live, AC5 preparation unsent.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['banishmentRepair03Audit'] = {'archive':rec['preservedRepair03'],'audit':info(audit),'status':'Four bounded source/operative/example/scope corrections; no adoption.'}
    state['activeGptReview'] = {'reviewId':'BANISHMENT-REPAIR-04','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':rec['userTurnId'],'status':'Actual browser confirmed generating with an acknowledgement of all four requested corrections; native message content verified through exact Markdown-escape diff.','generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False}
    state['safeNextActions'] = [
        'Read SAME Part4 response to user turn '+rec['userTurnId']+'. Browser live status is authoritative; native idle alone is not terminal. Do not resubmit or restart on observation timeout.',
        'Preserve DD_Banishment_Repair_04_Return.zip; verify49source bindings, original source/access, all28historical scenarios and all35retained current case IDs. Review BAN-R04-01..04 dispositions and new actual conflict-resolution examples.',
        'Verify Oracle31/1-long-rest and Wizard17/3RP/recharge2, no active reservation instructions, same-anchor Large return on open terrain, post-admission cell bounds and legal pre-commit Pet square. Distinguish inherited placement order from NEW local conflict semantics; no blanket loss of all spatial identity or silent global body-rule change.',
        'Keep accepted finite Banishment ending as candidate and actual Mage familiar/Portal escape. Banishment remains pending until exact coherent acceptance and controlled application.',
        'AC5 full16spell preparation remains unsent; refresh Banishment dependency and74source bindings before dispatch. Preserve class addendum and32additional proposed examples.',
        'Full75-area goal remains active:434reviewed/414pending ordinary spells, latest verified GitHub backup18c6e3a; later work local. Human/runtime/balance/publication and final whole-game flow gates remain open.',
    ]
    state['resumedBlockedAudit'] = {'classification':'progress','evidence':info(audit),'meaningfulProgress':scope}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'receipt':info(receipt),'checkpoint':info(checkpoint),'links':build['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))


if __name__ == '__main__':
    main()
