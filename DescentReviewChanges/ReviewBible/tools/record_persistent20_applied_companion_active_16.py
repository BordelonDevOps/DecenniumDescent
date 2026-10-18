"""Record verified persistent20 integration and actual companion conference."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now = datetime.now(timezone.utc).isoformat()
    stem = 'PERSISTENT20_APPLIED_COMPANION_ACTIVE_16'
    cp = A / ('ACTIVE_AUTHORING_CHECKPOINT_' + stem + '.json')
    delta = A / (stem + '_NAVIGATION_DELTA.json')
    report = A / (stem + '_CHECK.json')
    keep = A / 'navigation-before-persistent20-applied-companion-active-16'
    assert not any(p.exists() for p in [cp, delta, report, keep])
    checks = []
    def ck(name, value):
        checks.append({'check': name, 'passed': bool(value)})
        assert value, name
    P = R / 'data/director/spell_review'
    qp = P / 'remaining_work_queue_11.json'; q = read(qp)
    registry = P / 'accepted_interface_registry_06.json'
    inventory = P / 'ordinary_spell_inventory_05.json'
    indexp = R / 'data/public/spell_playtests/authored_review_index.json'
    receipt = A / 'PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_RECEIPT.json'
    appcheck = A / 'PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_CHECK.json'
    rcheck = A / 'PERSISTENT20_REGISTRY_QUEUE_06_CHECK.json'
    submission = A / 'COMPANION_LIFE_10_CURRENT_04_ACTUAL_SUBMISSION.json'
    push = G / 'docs/audit/2026-10-18/github-snapshot-damage25/PUSH_RECEIPT.json'
    oldcp = A / 'ACTIVE_AUTHORING_CHECKPOINT_SOURCE_CONFERENCES_15.json'
    ck('Exact current membership', read(indexp)['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    ck('Application has no failures', read(appcheck)['failureCount'] == 0)
    ck('Twenty accepted identities', len(read(receipt)['acceptedSpellIds']) == 20)
    ck('249 standalone procedures', read(receipt)['standaloneAfter'] == 249)
    ck('Queue disjoint current groups', len(q['groups']) == 14 and sum(g['identityCount'] for g in q['groups']) == len({i for g in q['groups'] for i in g['identities']}) == 106)
    ck('323 pending rows', len(q['rows']) == 323 and q['ordinarySpellCounts'] == {'total': 848, 'reviewed': 525, 'pending': 323})
    for binding in q['sourceBindings']:
        ck('Current queue binding ' + binding['path'], info(G / binding['path']) == binding)
    start = G / 'START_HERE.md'; guide = R / 'docs/DEVELOPMENT_DIRECTION.md'
    builder = R / 'tools/build_review_map.py'; ledger = R / 'data/playtest/game_development_coverage.json'
    mapfile = G / 'REVIEW_MAP.html'; buildfile = A / 'REVIEW_MAP_BUILD.json'
    raw = {p: p.read_bytes() for p in [start, guide, builder, ledger, mapfile, buildfile]}
    replacements = {
        '**Current position —': '''**Current position — 18 October 2026:** **525 ordinary spells reviewed / 323 pending**, with 249 complete standalone procedures across all 848 identities. The [current authored index](DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json), [checkpoint16](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_PERSISTENT20_APPLIED_COMPANION_ACTIVE_16.json) and [review map](REVIEW_MAP.html) are the entry points. Working folder: `C:\\Github\\DecenniumDescent`. Continue until the review is complete or any reported allowance reaches 20% remaining; the latest observation was 60% remaining.''',
        '**GPT is reviewing persistent20:**': '''**Persistent20 accepted and applied:** Actual GPT accepted the eight Exact07 artifacts unchanged. The [application receipt](docs/audit/2026-10-08/full-game/PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_RECEIPT.json) and [1,108-check verification](docs/audit/2026-10-08/full-game/PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_CHECK.json) bind 20 procedures, 21 placements, 40 preserved original scenarios and 57 current cases. Read the [player chapter](DescentReviewChanges/ReviewBible/docs/spells/candidates/PERSISTENT_DAMAGE_20_REVIEWED_07.md), [Director chapter](DescentReviewChanges/ReviewBible/docs/director-only/spells/PERSISTENT_DAMAGE_20_REVIEWED_07.md) or [exact model](DescentReviewChanges/ReviewBible/data/public/spell_candidates/persistent_damage_20_reviewed_07.json). Original and sealed pending labels remain history; the actual acceptance receipt controls. Conditional fixtures and pending counterpart permissions retain their limits. Runtime, human gameplay and numerical balance remain unproven.''',
        '**Companion/life10 is the next case conference:**': '''**GPT is reviewing companion/life10:** The full [Current04 packet](docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_PREPARATION.json) was [actually submitted](docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_ACTUAL_SUBMISSION.json) to Review Continuation Part 4, user turn `3215cb75-04cf-48fb-8d6b-9dbc93d04850`. It contains all ten procedures, twenty original scenario texts, 27 current main cases and five explicit questions. Two Command Undeath cases remain conditional on an authoritative exact CR2 Undead. The [sent update](docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_SUBMITTED_REQUEST.txt) includes persistent20's actual acceptance and the verified GitHub backup. Preserve the complete actual reply and reconcile its decisions before any adoption; no result is inferred while GPT reviews.''',
        '**Remaining spell work:**': '''**Remaining spell work:** [Queue11](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_11.json) retains 323 pending identities: 106 in fourteen active/prepared groups, with 216 other original-source identities and one receipt task. [Registry06](DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json) contains 173 scoped interfaces, preserving all 143 earlier entries. Its persistent20 additions retain full procedures and root mappings. The [rank-seven mechanics16 source conference](docs/audit/2026-10-08/full-game/RANK7_MECHANICS_16_SOURCE_CONFERENCE_01_PREPARATION.json) combines the preserved Evocation8 and Enchantment8 preparations, classifies each spell separately (one tier A, twelve B, three C), and asks 33 new questions. It remains UNSENT with no current worked cases or adoption. Information8, Eye of Judgement and the other prepared conferences remain separate reviews.''',
        '**GitHub preservation:**': '''**GitHub preservation:** [Verified main `3ece00c`](docs/audit/2026-10-18/github-snapshot-damage25/PUSH_RECEIPT.json) includes damage25's application and source conferences through checkpoint15: 23,896 expected blobs verified and all 23,767 prior tracked entries retained. Persistent20's actual final/application, registry06, queue11, companion Current04's actual submission, the combined rank-seven source packet and checkpoint16 are later local progress. No source information was deleted or history rewritten. All 75 domain gates remain separate; this progress does not establish whole-game flow, runtime, balance, cosmology or release approval.'''
    }
    edited = {}
    for p in [start, guide]:
        text = raw[p].decode('utf8'); parts = text.split('\n\n')
        for prefix, paragraph in replacements.items():
            hits = [i for i, part in enumerate(parts) if part.startswith(prefix)]
            ck('One navigation paragraph ' + p.name + prefix, len(hits) == 1)
            if p == guide:
                paragraph = paragraph.replace('(docs/audit/', '(../../../docs/audit/').replace('(DescentReviewChanges/ReviewBible/data/', '(../data/').replace('(DescentReviewChanges/ReviewBible/docs/', '(').replace('(REVIEW_MAP.html)', '(../../../REVIEW_MAP.html)')
            parts[hits[0]] = paragraph
        text = '\n\n'.join(parts).replace('505 reviewed authored procedures; 343 pending.', '525 reviewed authored procedures; 323 pending.').replace('229 procedures use complete standalone representations', '249 procedures use complete standalone representations')
        text = text.replace('[143-entry interface registry](../data/director/spell_review/accepted_interface_registry_05.json)', '[173-entry interface registry](../data/director/spell_review/accepted_interface_registry_06.json)')
        edited[p] = text
    coverage = read(ledger); previous = deepcopy(coverage)
    coverage.setdefault('activeOrdinarySpellReviewHistory', []).append(deepcopy(coverage['activeOrdinarySpellReview']))
    coverage['activeOrdinarySpellReview'] = {'recordedAtUtc': now, 'ordinaryOperational': 525, 'ordinaryPending': 323, 'standaloneProcedures': 249, 'scope': 'Verified authored-candidate acceptance and application; historical evidence, runtime, human balance and all domain gates remain separate.', 'authoredIndex': info(indexp), 'latestAcceptance': info(receipt), 'currentRegistry': info(registry), 'currentQueue': info(qp), 'activeGptSubmission': info(submission), 'runtimeVerified': False}
    for before, after in zip(previous['aspects'], coverage['aspects']):
        if after['id'] in ['DD-11', 'DD-12']:
            after['reviewEvidence'].append(receipt.relative_to(G).as_posix())
            after['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [appcheck, rcheck])
            after.setdefault('currentEvidenceAddenda', []).append({'id': 'persistent20-applied-companion-active-16', 'recordedAtUtc': now, 'acceptedProcedures': 20, 'currentCases': 57, 'historicalScenarios': 40, 'runtimeTestsExecuted': 0, 'fullDomainClosureChanged': False})
        else: ck('Unrelated domain identical ' + before['id'], before == after)
        ck('Domain gate unchanged ' + before['id'], all(before[k] == after[k] for k in ['status', 'closure', 'humanEvidence', 'completionClass']))
    code = raw[builder].decode('utf8'); tail = ' + read(A / "SOURCE_CONFERENCES_15_NAVIGATION_DELTA.json")["changes"]\n'
    ck('Unique delta tail', code.count(tail) == 1)
    code = code.replace(tail, tail.rstrip('\n') + ' + read(A / "PERSISTENT20_APPLIED_COMPANION_ACTIVE_16_NAVIGATION_DELTA.json")["changes"]\n')
    code = code.replace('    featured = [\n', '    featured = [\n' + ''.join('        ' + repr(x) + ',\n' for x in [('Current checkpoint16 — persistent20 applied, companion review active', cp.relative_to(G).as_posix()), ('Persistent20 — jointly accepted complete procedures', 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/persistent_damage_20_reviewed_07.json'), ('Current323 pending identities — queue11', qp.relative_to(G).as_posix())]), 1)
    code = code.replace('    pending = [\n', '    pending = [\n' + ''.join('        ' + repr(x) + ',\n' for x in [('Persistent20 — actual final applied, 1108 checks', appcheck.name), ('Companion Current04 — full actual conference active', submission.name), ('Rank7 mechanics16 —33 questions, prepared unsent', 'RANK7_MECHANICS_16_SOURCE_CONFERENCE_01_PREPARATION.json')]), 1)
    for old, new in {'Current checkpoint15 — source conferences prepared': 'Checkpoint15 history — source conferences prepared', 'Current343 pending identities — queue10': 'Queue10 history — before persistent20 acceptance', 'Persistent20 exact07 — actual review active': 'Persistent20 submission history — accepted and applied', 'Rank7 Evocation8 —16 source-only questions, unsent': 'Evocation8 parent preparation — superseded by mixed16 dispatch', 'accepted_interface_registry_05.json': 'accepted_interface_registry_06.json'}.items():
        code = code.replace(old, new)
    scope = 'Video game only. 525 reviewed / 323 pending; 249 standalone procedures; 173 scoped interfaces. Persistent20 Exact07 and damage25 Exact10 accepted and applied. Companion Current04 full packet actually submitted: 27 main cases, 2 exact CR2 holds, 5 questions. Queue11: 106 identities in 14 groups, 217 other source/receipt items. Rank7 mechanics16 source conference prepared unsent, 33 questions, per-spell tiers 1A/12B/3C. All75 domain gates unchanged. GitHub3ece00c covers checkpoint15; later integration is local. Latest allowance60percent remaining; stop at20percent or completed review.'
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant) and k.value == 'notebookReview']
    ck('Unique map status', len(nodes) == 1)
    code = code.replace(ast.get_source_segment(code, nodes[0]), repr(scope), 1); compile(code, str(builder), 'exec')
    # All dependent inputs and edit anchors have passed before writes.
    saved = []
    for p, data in raw.items():
        dst = keep / p.relative_to(G); dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(data)
        saved.append({'source': info(p), 'preservedCopy': info(dst)})
    (keep / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    for p, text in edited.items(): p.write_text(text, encoding='utf8', newline='\n')
    ledger.write_bytes(encoded(coverage)); builder.write_text(code, encoding='utf8', newline='\n')
    changes = [{'before': next({**b['source'], 'preservedCopy': b['preservedCopy']['path']} for b in saved if b['source']['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, guide, ledger, builder]]
    originalindex = A / 'source-before-persistent20-exact07-application/authored_review_index.json'
    changes.append({'before': {**info(indexp, originalindex.read_bytes()), 'preservedCopy': originalindex.relative_to(G).as_posix()}, 'after': info(indexp)})
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': changes, 'spellApplicationAuthority': info(receipt), 'all75DomainGatesUnchanged': True, 'newRuleAdoptionsByNavigation': 0, 'sourceInformationDeleted': 0}))
    checkpoint = deepcopy(read(oldcp))
    checkpoint.update(id='ACTIVE-AUTHORING-PERSISTENT20-APPLIED-COMPANION-ACTIVE-16', recordedAtUtc=now, status=scope, previousCheckpoint=info(oldcp), authoredCounts={'reviewed': 525, 'pending': 323, 'total': 848, 'standalone': 249}, currentAuthoredIndex=info(indexp), persistent20Application=info(receipt), persistent20Verification=info(appcheck), acceptedInterfaceRegistry=info(registry), currentInventory=info(inventory), currentWorkQueue=info(qp), companionLife10=next(g for g in q['groups'] if g['group'] == 'companion-life10'), remainingPreparedGroups=q['groups'], latestVerifiedGitHubBackup=read(push), laterLocalWork=['Persistent20 actual final and verified application', 'Registry06/inventory05/queue11', 'Companion Current04 actual full submission', 'Enchantment8 parent and combined rank7 mechanics16 source conference', 'Checkpoint16 navigation'], lastUsageObservation={'usedPercent': 40, 'remainingPercent': 60, 'windowMinutes': 10080, 'secondary': 'unavailable'}, nextAction='Preserve the actual companion Current04 final and reconcile all decisions before adoption. Keep GPT informed of persistent20 successful application and current queue. Continue source-grounded pending preparation and subsequent actual conferences until review complete or20percent remaining.', coverageLedger=info(ledger), navigationDelta=info(delta), preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'))
    checkpoint['previousGptReview'] = deepcopy(checkpoint['activeGptReview'])
    checkpoint['activeGptReview'] = {'chat': 'Review Continuation Part 4', 'threadId': '6ad1acef-455c-83ea-bc33-56e4adaec9c8', 'userTurn': '3215cb75-04cf-48fb-8d6b-9dbc93d04850', 'submission': info(submission), 'archive': info(A/'DD_Companion_Life_10_Current_04_Draft.zip'), 'status': 'Full packet actually submitted; no final yet recorded'}
    checkpoint['rank7Mechanics16'] = info(A/'RANK7_MECHANICS_16_SOURCE_CONFERENCE_01_PREPARATION.json')
    cp.write_bytes(encoded(checkpoint))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(builder)], capture_output=True, text=True, encoding='utf8')
    ck('Review map builds ' + run.stderr[-1000:], run.returncode == 0)
    build = read(buildfile); ck('No missing map links', not build['missingLinks'])
    checkpoint['navigation'] = {'map': info(mapfile), 'build': info(buildfile), 'existingDistinctLinks': build['existingDistinctLinks'], 'missingLinks': []}; cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint': info(cp), 'delta': info(delta), 'checks': checks, 'checkCount': len(checks), 'failures': 0, 'existingDistinctLinks': build['existingDistinctLinks'], 'missingLinks': [], 'all75DomainGatesUnchanged': True, 'newRuleAdoptionsByNavigation': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0}))
    print(json.dumps({'checkpoint': info(cp), 'checks': len(checks), 'links': build['existingDistinctLinks'], 'failures': 0}))

if __name__ == '__main__': main()
