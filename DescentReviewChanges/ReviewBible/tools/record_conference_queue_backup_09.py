"""Refresh navigation for verified backup and prepared systemic conferences."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_DC25_REBOUND_PERSISTENT_ACTIVE_08.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_CONFERENCE_QUEUE_BACKUP_09.json'
    delta = A / 'CONFERENCE_QUEUE_BACKUP_09_NAVIGATION_DELTA.json'
    report = A / 'CONFERENCE_QUEUE_BACKUP_09_NAVIGATION_CHECK.json'
    keep = A / 'navigation-before-conference-queue-backup-09'
    assert not any(p.exists() for p in [checkpoint, delta, report, keep])
    start, guide, builder = G / 'START_HERE.md', R / 'docs/DEVELOPMENT_DIRECTION.md', R / 'tools/build_review_map.py'
    ledger, mapfile, buildfile = R / 'data/playtest/game_development_coverage.json', G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json'
    raw = {p: p.read_bytes() for p in [start, guide, builder, ledger, mapfile, buildfile]}
    now = datetime.now(timezone.utc).isoformat()
    saved = []
    for path, content in raw.items():
        copy = keep / path.relative_to(G)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(content)
        saved.append({'source': info(path), 'preservedCopy': info(copy)})
    (keep / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    receiptpath = G / 'docs/audit/2026-10-18/github-snapshot-conferences/PUSH_RECEIPT.json'
    receipt = read(receiptpath)
    assert receipt['commit'] == receipt['remoteMain'] == '9cfd0ab4029176a5e1075344a908f50a3fb8fdde'
    text = raw[start].decode('utf8').replace(previous.name, checkpoint.name)
    text = text.replace('Latest verified GitHub backup is **40ad7bb**; subsequent pending cohort development and new review follow-through are local.', 'Latest verified GitHub backup is **9cfd0ab**; the subsequently prepared memory and Creation conferences and this navigation update are local.')
    replacements = {
        '**Accelerated digital spell review:**': '**Accelerated digital spell review:** Counts remain **480 reviewed / 368 pending**, with 108 accepted interfaces. The actual [25-spell conference verdict](docs/audit/2026-10-08/full-game/DAMAGE_CONTROL_25_CONFERENCE_07_RECEIPT.json) and all 23 corrections are preserved in pending Current08. The [exact rebound09 packet](docs/audit/2026-10-08/full-game/DAMAGE_CONTROL_25_EXACT_REBOUND_09_PREPARATION.json) is ready but unsent: full 25-spell model, 70 current case records, both complete manuscripts and exact evidence. Three local HP/cut example corrections still need GPT concurrence. The [presentation check](docs/audit/2026-10-08/full-game/DAMAGE_CONTROL_25_PRESENTATION_09_CHECK.json) confirms no procedure or case changed during formatting. No 25-spell membership was added.',
        '**Persistent spell development:**': '**Persistent spell development:** Persistent20 Current06 remains in actual GPT review. Illusion14 conference11 (14 procedures, 28 original/current cases, three supplements) and Control15 conference11 (15 procedures, 30 original/current cases) remain prepared unsent. Missing CR/native-attack/companion-check premises remain conditional. The separate [memory conference](docs/audit/2026-10-08/full-game/MEMORY_2_CONFERENCE_01_PREPARATION.json) now contains two full original proposals, four original/conditional cases, eight design questions and 24 complete files. The [Creation conference](docs/audit/2026-10-08/full-game/CREATION_CONFERENCE_01_PREPARATION.json) contains its complete original proposal, two original/conditional cases, seven findings, eight questions and 35 full files. These systemic choices remain unadopted; no original source or scenario was deleted.',
        '**Owner-directed sequence:**': '**Owner-directed sequence:** The latest verified preservation push is [9cfd0ab](docs/audit/2026-10-18/github-snapshot-conferences/PUSH_RECEIPT.json), preserving the returned 25-spell review, exact rebound09, persistent06 submission, illusion/control11 packets and checkpoint08. All 22,916 expected blobs matched; all prior tracked files remain. The later memory/Creation packets and checkpoint09 are local. Careful cosmology work began after its required push. Continue development and actual GPT conferences until review completion or 20% allowance remains; progress backups do not close whole-game review.'
    }
    for marker, replacement in replacements.items():
        i = text.index(marker)
        j = text.index('\n\n', i)
        text = text[:i] + replacement + text[j:]
    start.write_text(text, encoding='utf8', newline='\n')
    text = raw[guide].decode('utf8').replace(previous.name, checkpoint.name)
    i, j = text.index('## Current continuation'), text.index('The [current checkpoint]')
    text = text[:i] + '''## Current continuation

- Counts remain **480 reviewed / 368 pending**, 848 identities, 204 complete standalone procedures and 108 accepted interfaces. AC6/DE4 acceptance remains closed.
- The actual 25-spell conference07 final and all 23 complete corrections are preserved. Pending Current08 and exact rebound09 supply the full model, 70 current cases, both manuscripts and evidence. Three locally corrected HP/cut examples require concurrence. Rebound09 is prepared, unsent and unadopted.
- Persistent20 conference06 is actually submitted in user turn 28a42338-ffbd-4fb8-9a49-ec96d447762d and remains active in Review Continuation Part4. GPT already knows the earlier 40ad7bb backup and control/illusion progress. Do not interrupt or duplicate its review.
- Illusion14 conference11 and Control15 conference11 are prepared unsent. Their original scenarios remain intact; unavailable source inputs remain explicitly conditional.
- Memory2 conference01 is prepared with two complete original proposals, four original/conditional traces, eight design forks and 24 full files. Creation conference01 is prepared with one original proposal, two original/conditional traces, seven findings, eight design forks and 35 full files. No substantial new systemic memory/material rule has been chosen.
- GitHub main is verified at 9cfd0ab4029176a5e1075344a908f50a3fb8fdde. Its snapshot includes exact rebound09 and the full persistent/illusion/control work. Memory2, Creation and checkpoint09 were prepared afterward and remain local. No source deletion or history rewrite occurred.
- At the next substantive GPT exchange, report the verified backup, exact rebound09's three local corrections, complete control11 packet and new memory/Creation conferences. Preserve and verify the actual persistent response first.
- All 75 domain gates retain their actual states. Runtime, human gameplay, numerical balance, cosmology/canon, whole-game flow and release remain separate. Continue until review completion or any reported allowance reaches 20% remaining; latest weekly observation is 23% used / 77% remaining, with the secondary window unavailable.

''' + text[j:]
    guide.write_text(text, encoding='utf8', newline='\n')
    evidence = [A / name for name in ['DAMAGE_CONTROL_25_EXACT_REBOUND_09_PREPARATION.json', 'DAMAGE_CONTROL_25_PRESENTATION_09_CHECK.json', 'MEMORY_2_CONFERENCE_01_PREPARATION.json', 'CREATION_CONFERENCE_01_PREPARATION.json']] + [receiptpath]
    coverage = read(ledger)
    before = deepcopy(coverage)
    for row in coverage['aspects']:
        if row['id'] in ['DD-11', 'DD-12']:
            row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'conference-queue-backup-09', 'recordedAtUtc': now, 'reviewed': 480, 'pending': 368, 'newSpellIdentitiesAccepted': 0, 'memoryCreationPreparedUnsent': True, 'exactRebound09PreparedUnsent': True, 'githubVerifiedCommit': receipt['commit'], 'runtimeTestsExecuted': 0, 'fullDomainClosureChanged': False})
    for old, new in zip(before['aspects'], coverage['aspects']):
        assert all(old[k] == new[k] for k in ['status', 'closure', 'humanEvidence', 'completionClass'])
        if old['id'] not in ['DD-11', 'DD-12']:
            assert old == new
    ledger.write_bytes(encoded(coverage))
    code = raw[builder].decode('utf8')
    tail = ' + read(A / "DC25_REBOUND_PERSISTENT_ACTIVE_08_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail) == 1
    code = code.replace(tail, tail.rstrip('\n') + ' + read(A / "CONFERENCE_QUEUE_BACKUP_09_NAVIGATION_DELTA.json")["changes"]\n')
    additions = [('Damage25 exact rebound09 — prepared unsent', 'DAMAGE_CONTROL_25_EXACT_REBOUND_09_PREPARATION.json'), ('Memory2 systemic conference01 — prepared unsent', 'MEMORY_2_CONFERENCE_01_PREPARATION.json'), ('Creation economic conference01 — prepared unsent', 'CREATION_CONFERENCE_01_PREPARATION.json')]
    code = code.replace('    pending = [\n', '    pending = [\n' + ''.join('        ' + repr(t) + ',\n' for t in additions), 1)
    scope = 'Video-game-only development:480reviewed/368pending;108acceptedinterfaces. Persistent20 actual review active. Damage25 exact rebound09,illusion14/control15 conference11 and memory2/Creation conferences prepared unsent. GitHub9cfd0ab verified;later memory/Creation/navigation local. All75domain gates preserved;77percent remaining observed;stopat20percent.'
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant) and k.value == 'notebookReview']
    assert len(nodes) == 1
    code = code.replace(ast.get_source_segment(code, nodes[0]), repr(scope), 1)
    compile(code, str(builder), 'exec')
    builder.write_text(code, encoding='utf8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': [{'before': next({**s['source'], 'preservedCopy': s['preservedCopy']['path']} for s in saved if s['source']['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, guide, ledger, builder]], 'all75DomainGatesUnchanged': True, 'newRuleAdoptionsByNavigation': 0, 'sourceInformationDeleted': 0}))
    current = deepcopy(read(previous))
    current.update(id='ACTIVE-AUTHORING-CONFERENCE-QUEUE-BACKUP-09', recordedAtUtc=now, status=scope, previousCheckpoint=info(previous), lastUsageObservation={'weeklyUsedPercent': 23, 'weeklyRemainingPercent': 77, 'shortWindowReported': False}, coverageLedger=info(ledger), navigationDelta=info(delta), preservedNavigation=info(keep / 'PRESERVATION_MANIFEST.json'), newRuleAdoptions=0)
    current['latestVerifiedGitHubBackup'] = {'receipt': info(receiptpath), 'commit': receipt['commit'], 'remoteMainVerified': receipt['remoteMain'], 'scope': receipt['scope'], 'laterLocalWork': ['memory2conference01', 'Creationconference01', 'checkpoint09']}
    current['verifiedGitHubBackup'] = deepcopy(current['latestVerifiedGitHubBackup'])
    current['next25'] = {'draft': info(R / 'data/director/spell_proposals/damage_control_25_current_08.json'), 'sourceConference07Returned': True, 'actualFinalReceipt': info(A / 'DAMAGE_CONTROL_25_CONFERENCE_07_RECEIPT.json'), 'exactRebound09': info(A / 'DD_Damage_Control_25_Exact_Rebound_09.zip'), 'exactPreparation': info(evidence[0]), 'exactSubmitted': False, 'adopted': False, 'originalScenarios': 36, 'currentCases': 70, 'localSupplementCorrectionsAwaitingConcurrence': 3}
    current['damageControl25Current'].update(exactReboundPreparation=info(evidence[0]), exactSubmitted=False, remaining='Send prepared exact rebound09 to actual GPT, verify disposition and exact artifact hashes, then integrate only actually accepted scope.')
    current['memory2'] = {'candidate': info(R / 'data/director/spell_review/memory_2_conference_01.json'), 'preparation': info(evidence[2]), 'archive': info(A / 'DD_Memory_2_Conference_01.zip'), 'submitted': False, 'adopted': False, 'originalProcedures': 2, 'originalAndConditionalCases': 4, 'questions': 8, 'systemicChoicesNotYetMade': True}
    current['creation'] = {'candidate': info(R / 'data/director/spell_review/creation_conference_01.json'), 'preparation': info(evidence[3]), 'archive': info(A / 'DD_Creation_Conference_01.zip'), 'submitted': False, 'adopted': False, 'originalProcedures': 1, 'originalAndConditionalCases': 2, 'findings': 7, 'questions': 8, 'systemicChoicesNotYetMade': True}
    current['nextGptProgressUpdate'] = 'Preserve actual persistent20 final before the next substantive exchange. Report verified GitHub9cfd0ab, prepared damage25 exact09 and three local example repairs, full control11 packet, memory2 and Creation conference packets. GPT has not yet received those latest milestones. Send full relevant exact files, not summaries as substitutes.'
    checkpoint.write_bytes(encoded(current))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(builder)], capture_output=True, text=True, encoding='utf8')
    assert run.returncode == 0, (run.stdout[-1500:], run.stderr[-1500:])
    build = read(buildfile)
    assert not build['missingLinks']
    current['navigation'] = {'map': info(mapfile), 'build': info(buildfile), 'existingDistinctLinks': build['existingDistinctLinks'], 'missingLinks': []}
    checkpoint.write_bytes(encoded(current))
    report.write_bytes(encoded({'checkpoint': info(checkpoint), 'delta': info(delta), 'all75DomainGatesUnchanged': True, 'existingDistinctLinks': build['existingDistinctLinks'], 'missingLinks': [], 'newRuleAdoptionsByNavigation': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0}))
    print(json.dumps(read(report)))


if __name__ == '__main__':
    main()
