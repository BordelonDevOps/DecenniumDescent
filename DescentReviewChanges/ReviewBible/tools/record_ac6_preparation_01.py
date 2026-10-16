"""Save independent AC6 progress while retaining the existing AC5 conference."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_BANISHMENT_APPLICATION_AC5_SUBMISSION_02.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_INTERFACE_PREPARATION_01.json'
    delta = A / 'AC6_INTERFACE_PREPARATION_01_NAVIGATION_DELTA.json'
    keep = A / 'navigation-before-ac6-interface-preparation-01'
    observation = A / 'AC5_CURRENT_REVIEW_02_LIVE_OBSERVATION_03.txt'
    report = A / 'AC6_CURRENT_SOURCE_INTERFACE_AUDIT_01.json'
    checks = A / 'AC6_CURRENT_SOURCE_INTERFACE_CHECK_01.json'
    forge = R / 'data/director/spell_proposals/resonance_forge_revision_02.json'
    assert not any(p.exists() for p in [checkpoint, delta, keep])
    assert read(checks)['failureCount'] == 0
    assert 'button "Stop"' in observation.read_text(encoding='utf8')
    start = G / 'START_HERE.md'
    nav = R / 'tools/build_review_map.py'
    ledger = R / 'data/playtest/game_development_coverage.json'
    saved, originals = [], {}
    for p in [start, nav, ledger, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        raw = p.read_bytes(); q = keep / p.relative_to(G)
        q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(raw)
        originals[p] = raw
        saved.append({**info(p), 'preservedCopy': q.relative_to(G).as_posix()})
    (keep / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text = originals[start].decode()
    assert text.count(previous.relative_to(G).as_posix()) == 1
    text = text.replace(previous.relative_to(G).as_posix(), checkpoint.relative_to(G).as_posix(), 1)
    marker = '**Current GPT conference:**'
    insert = text.index('\n\n', text.index(marker))
    text = text[:insert] + '\n\n**Next spell group, prepared for review:** [The full AC6 audit](docs/audit/2026-10-08/full-game/AC6_CURRENT_SOURCE_INTERFACE_AUDIT_01.json) retains 14 identities and 16 printed placements, including both Alignment Nexus operations. It records 19 current issues, 40 comparison cards and 32 required new scenarios. The [complete Resonance Forge draft correction](DescentReviewChanges/ReviewBible/data/director/spell_proposals/resonance_forge_revision_02.json) includes six worked examples using actual Blacksmithing recipes. These drafts remain unadopted and unsent; the live AC5 review must finish and its source bindings be refreshed before the next conference.' + text[insert:]
    start.write_text(text, encoding='utf8', newline='\n')
    cov = json.loads(originals[ledger]); before = deepcopy(cov)
    for ident in ['DD-11', 'DD-12']:
        row = next(r for r in cov['aspects'] if r['id'] == ident); old = deepcopy(row)
        row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [report, checks, forge])
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'ac6-current-interface-preparation-01', 'recordedAtUtc': now, 'spellIdentities': 14, 'printedPlacements': 16, 'interfaceIssues': 19, 'comparisonCards': 40, 'completeForgeExamples': 6, 'status': 'Unsent preparation; no adopted rules or domain closure.', 'checks': 199, 'failures': 0})
        assert all(row[k] == old[k] for k in ['status', 'closure', 'humanEvidence', 'completionClass'])
    assert [r for r in cov['aspects'] if r['id'] not in ['DD-11', 'DD-12']] == [r for r in before['aspects'] if r['id'] not in ['DD-11', 'DD-12']]
    ledger.write_bytes(encoded(cov))
    code = originals[nav].decode()
    tail = ' + read(A / "BANISHMENT_APPLICATION_AC5_SUBMISSION_02_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail) == 1
    code = code.replace(tail, tail.rstrip('\n') + ' + read(A / "AC6_INTERFACE_PREPARATION_01_NAVIGATION_DELTA.json")["changes"]\n', 1)
    code = code.replace('    pending = [\n', '    pending = [\n        ("AC6 — full current source/interface preparation, unsent", "AC6_CURRENT_SOURCE_INTERFACE_AUDIT_01.json"),\n        ("AC6 — preparation source checks, not runtime", "AC6_CURRENT_SOURCE_INTERFACE_CHECK_01.json"),\n', 1)
    code = code.replace('    featured = [\n', '    featured = [\n        ("Resonance Forge — complete draft correction awaiting GPT", "DescentReviewChanges/ReviewBible/data/director/spell_proposals/resonance_forge_revision_02.json"),\n', 1)
    scope = '435 reviewed / 413 pending ordinary spells. Banishment is accepted and applied. The actual Part 4 AC5 review was confirmed generating this turn; subsequent page observations timed out, with the same tab still present and no terminal response observed. Independent AC6 preparation preserves all 14 identities/16 placements and records 19 issues plus a complete Forge correction with six examples. No new spell adoption, runtime, human balance or whole-game approval.'
    values = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant) and k.value == 'notebookReview']
    assert len(values) == 1
    code = code.replace(ast.get_source_segment(code, values[0]), repr(scope), 1)
    compile(code, str(nav), 'exec'); nav.write_text(code, encoding='utf8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': [{'before': next(x for x in saved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, ledger, nav]], 'sourceInformationDeleted': 0, 'newSpellAdoptions': 0, 'fullDomainClosureChanged': False}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf8')
    assert run.returncode == 0, (run.stdout[-1500:], run.stderr[-1500:])
    build = read(A / 'REVIEW_MAP_BUILD.json'); assert not build['missingLinks']
    state = read(previous)
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), status=scope, goalTurnClassification='progress', previousGoalTurnClassification='progress', coverageDelta=info(delta), coverageLedger=info(ledger), ownerStartPage=info(start), newRuleAdoptions=0, newRuleAdoptionScope='Independent AC6 preparation and complete unadopted Forge revision; no rule application this turn.', navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': build['existingDistinctLinks'], 'missingLinks': []})
    state['activeGptReview'].update(status='Same Part 4 AC5 turn. Live Stop control and source-reading output confirmed earlier this turn. Later DOM/Stop observations timed out; browser inventory still confirms the same tab and native read exposes only the submitted user message, not a terminal assistant response. Do not infer stopped/completed or resubmit.', lastSuccessfulObservation=info(observation), observationTimeoutMeansTerminal=False)
    state['ac6CurrentPreparation'] = {'report': info(report), 'check': info(checks), 'forgeRevision': info(forge), 'counts': read(report)['counts'], 'status': 'Unsent; AC5 dependencies must refresh before future conference.', 'sourceBindings': 80, 'checks': 199, 'failures': 0, 'newSpellAdoptions': 0}
    state['safeNextActions'] = [
        'Re-poll the SAME Part 4 tab125746308 and AC5 user turn f0368c5a-e495-4d6c-814e-2d67355f7828. An observation timeout is not terminal; do not reload, restart or resubmit solely because observation failed.',
        'Preserve and independently review expected DD_AC5_Current_Review_02_Return.zip once actually returned: all86source bindings,16full cards/17placements,22historical texts and32new scenarios, exact issue dispositions and full profiles. None of these16spells is adopted yet.',
        'Use AC6_CURRENT_SOURCE_INTERFACE_AUDIT_01.json and the full Forge revision02 for subsequent preparation. The old11full proposals/22cases and3receipt records remain untouched. All14identities including both Alignment Nexus modes require complete authoring.',
        'For AC6, resolve Null-disabled finite summons, current alignment/root/transfer rules, exact class versus ordinary spell classifications, protected Banishment closure, eight still-unreviewed CR6 source profiles and the real Blacksmithing interface. Do not claim source checks are semantic review.',
        'Refresh pending AC5 comparisons and all current source hashes after that live conference reaches exact acceptance. Then confer with actual GPT on complete AC6 work; do not turn current unknowns into permanent deferrals.',
        'Keep the entire75-area goal intact: further spells, environment/disease/consumables, feats, bestiary, Director content, packaging, companion implementation and final joint flow remain open. Latest verified GitHub backup18c6e3a predates this local work.',
    ]
    state['resumedBlockedAudit'] = {'classification': 'progress', 'meaningfulProgress': 'Saved full14-identity AC6 source preparation,19semantic issues and complete Forge revision with six real-recipe worked examples;199source/pointer checks passed.', 'evidence': info(checks)}
    state.setdefault('preservationManifests', []).append(info(keep / 'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'links': build['existingDistinctLinks'], 'missingLinks': 0, 'ordinarySpells': state['currentOrdinarySpellCounts'], 'newSpellAdoptions': 0}))


if __name__ == '__main__':
    main()
