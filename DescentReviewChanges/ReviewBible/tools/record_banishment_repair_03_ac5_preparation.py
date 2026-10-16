"""Preserve current review/navigation state after Repair03 and AC5 source work."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, difflib, html, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    now = datetime.now(timezone.utc).isoformat()
    receipt = A / 'BANISHMENT_REPAIR_03_SUBMISSION_RECEIPT.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_BANISHMENT_REPAIR_03_AC5_PREPARATION.json'
    delta = A / 'BANISHMENT_REPAIR_03_AC5_NAVIGATION_DELTA.json'
    keep = A / 'navigation-before-banishment-repair-03-ac5'
    assert not any(p.exists() for p in [receipt, checkpoint, delta, keep])
    native = A / 'BANISHMENT_REPAIR_03_NATIVE_DELIVERY.json'
    request = A / 'BANISHMENT_REPAIR_03_REQUEST.txt'
    dom = A / 'BANISHMENT_REPAIR_03_SUBMITTED_DOM.txt'
    live = A / 'BANISHMENT_REPAIR_03_LIVE_DOM.txt'
    proof = A / 'PART4_BANISHMENT_REPAIR_03_SUBMITTED.jpg'
    audit = A / 'BANISHMENT_REPAIR_02_LOCAL_AUDIT.json'
    ac5 = A / 'AC5_CURRENT_SOURCE_INTERFACE_AUDIT_01.json'
    classes = A / 'AC5_CLASS_INTERFACE_ADDENDUM_02.json'
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
    a = read(audit)
    assert a['failureCount'] == 0 and a['semanticFindingCount'] == 4
    rec = {
        'recordedAtUtc': now, 'threadTitle': delivery['thread']['title'], 'threadId': delivery['thread']['id'],
        'userTurnId': turn['id'], 'browserId': '3', 'tabId': '125746308',
        'conversationUrl': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
        'request': info(request), 'nativeDelivery': info(native),
        'deliveryVerification': {'literalByteEquality': False, 'allContentPreserved': True, 'normalization': 'ChatGPT Show in text field inserted Markdown escape backslashes and encoded16spaces as HTML entities; exact diff restricted to those changes, unescape restores original text exactly.', 'differences': changes},
        'submissionObservation': info(dom), 'liveObservation': info(live), 'proof': info(proof),
        'generationConfirmedLiveAtObservation': True,
        'preservedRepair02': info(A / 'DD_Banishment_Repair_02_Return.zip'),
        'localAudit': info(audit), 'structuralChecks': 200, 'structuralFailures': 0, 'semanticFindings': 4,
        'expectedReturn': 'DD_Banishment_Repair_03_Return.zip', 'banishmentAdopted': False,
        'sourceInformationDeleted': 0, 'runtimeTestsExecuted': 0, 'humanPlaytested': False,
    }
    receipt.write_bytes(encoded(rec))
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_BANISHMENT_REPAIR_02_SUBMISSION.json'
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
    text = text[:begin] + '**Active spell review:** The accepted 15-spell AC4 module remains applied. **Banishment Repair03 is live in Review Continuation Part 4.** [Repair02 is preserved and independently audited](docs/audit/2026-10-08/full-game/BANISHMENT_REPAIR_02_LOCAL_AUDIT.json): 200 source/output/preservation/reference checks pass, but four findings remain. Protected return berths conflict with mandatory anatomy endings; active old/new closure text disagrees; summon examples need legal visible space; and the escape-with-secondary example needs a valid concentration arrangement. [Repair03 supplies the exact existing body rule and a real Mage familiar alternative](docs/audit/2026-10-08/full-game/BANISHMENT_REPAIR_03_SUBMISSION_RECEIPT.json). Banishment remains unadopted.\n\n**Next spell preparation:** [The current AC5 source audit](docs/audit/2026-10-08/full-game/AC5_CURRENT_SOURCE_INTERFACE_AUDIT_01.json) covers all16 identities/17 printed placements,39 current comparison records,74 source files and four changed historical bindings. It retains11 old proposals/22 examples and adds12 integration questions/24 required examples. [The class addendum](docs/audit/2026-10-08/full-game/AC5_CLASS_INTERFACE_ADDENDUM_02.json) independently reads25 operative cards, adding ten specific issues and eight examples. Both are unsent; refresh the Banishment dependency before dispatch. No new spell adoption or runtime/human test is claimed.' + text[end:]
    start.write_text(text, encoding='utf8', newline='\n')
    cov = json.loads(originals[ledger])
    before = deepcopy(cov)
    for ident in ['DD-11', 'DD-12']:
        row = next(r for r in cov['aspects'] if r['id'] == ident)
        prior = deepcopy(row)
        row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [audit, receipt, ac5, classes])
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'banishment-repair03-ac5-preparation', 'recordedAtUtc': now, 'structuralChecks': 200, 'structuralFailures': 0, 'semanticFindings': 4, 'banishmentAdopted': False, 'nextCohortSourceIds': 16, 'currentClassCardsRead': 25, 'runtimeTestsExecuted': 0})
        assert all(row[k] == prior[k] for k in ['status', 'closure', 'humanEvidence', 'completionClass'])
    assert [r for r in cov['aspects'] if r['id'] not in ['DD-11','DD-12']] == [r for r in before['aspects'] if r['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    scope = '434 reviewed/414 pending ordinary spells. Banishment Repair02 preserved:200 structural checks pass, four semantic/example findings remain. Repair03 delivered/live with exact mandatory body-ending authority. Next AC5 preparation covers16identities/17placements,74sources,39comparisons and25independently read class cards. No new adoption or runtime/human/balance/canon/whole-game/publication approval.'
    code = originals[nav].decode()
    tail = ' + read(A / "BANISHMENT_REPAIR_02_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail) == 1
    code = code.replace(tail, tail.rstrip('\n') + ' + read(A / "BANISHMENT_REPAIR_03_AC5_NAVIGATION_DELTA.json")["changes"]\n', 1)
    values = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value == 'notebookReview']
    assert len(values) == 1
    code = code.replace(ast.get_source_segment(code,values[0]),repr(scope),1)
    items = [('Banishment — Repair02 audit and mandatory-ending conflict',audit.name),('Banishment — active Repair03 conference',receipt.name),('AC5 — current16-spell source/interface audit, unsent',ac5.name),('AC5 —25 independently read class interfaces, unsent',classes.name)]
    code = code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec')
    nav.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]],'sourceInformationDeleted':0,'newSpellAdoptions':0,'fullDomainClosureChanged':False}))
    run = subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode == 0,(run.stdout[-1000:],run.stderr[-1000:])
    build = read(A/'REVIEW_MAP_BUILD.json')
    assert not build['missingLinks']
    state = read(previous)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='No new rules adopted; Banishment Repair03 live, AC5 preparation unsent.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['banishmentRepair02Audit'] = {'archive':rec['preservedRepair02'],'audit':info(audit),'status':'Four source/operative/example findings; no adoption.'}
    state['activeGptReview'] = {'reviewId':'BANISHMENT-REPAIR-03','threadId':rec['threadId'],'title':rec['threadTitle'],'browserId':'3','tabId':'125746308','conversationUrl':rec['conversationUrl'],'submission':info(receipt),'userTurnId':rec['userTurnId'],'status':'Actual browser confirmed generating; complete request preserved through UI Markdown escapes, independently verified.','generationConfirmedLiveAtObservation':True,'expectedReturn':rec['expectedReturn'],'returnReceived':False,'newRulesAdopted':False}
    state['ac5CurrentPreparation'] = {'audit':info(ac5),'classAddendum':info(classes),'status':'Prepared unsent; full16spell scope; refresh current Banishment dependency before dispatch.','sourceFiles':74,'currentComparisons':39,'selectedClassCardsRead':25,'additionalAuthoredExamplesRequired':32}
    state['safeNextActions'] = [
        'Read SAME Part4 response to user turn '+rec['userTurnId']+'. Browser live status is authoritative; native idle alone is not terminal. Do not resubmit or restart on observation timeout.',
        'Preserve DD_Banishment_Repair_03_Return.zip; verify49source bindings, original source/access and all28historical scenarios. Review all retained34current cases and added repairs; old and new closure references must agree.',
        'Check finite ending against exact BODY_EQUIPMENT mandatory reversion: source expiry/death/0HP cannot fail to protect a berth. A canonical origin-plane placement conflict may remain if explicitly specified, but no active Banishment cell may persist beyond its endpoint. Verify legitimate Mage nonconcentration familiar + Faction Portal escape and actual in-cell summon geometry.',
        'AC5 current preparation is ready for later full16spell authoring; not sent.74source files,39comparisons (34reviewed/5pending),17class envelopes,73lexical navigation hits and25independently read cards. Four old source drifts include Ranger Nature\'s Whisper NWQ classification. Refresh Banishment and source bindings after acceptance before dispatch.',
        'Keep full75-area goal;434reviewed/414pending ordinary spells. AC4 already applied, one-shot scripts must not be rerun. Latest verified GitHub backup18c6e3a; later work local. Human/runtime/balance/publication and final whole-game flow gates remain open.',
    ]
    state['resumedBlockedAudit'] = {'classification':'progress','evidence':info(audit),'meaningfulProgress':scope}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'receipt':info(receipt),'checkpoint':info(checkpoint),'links':build['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))


if __name__ == '__main__':
    main()
