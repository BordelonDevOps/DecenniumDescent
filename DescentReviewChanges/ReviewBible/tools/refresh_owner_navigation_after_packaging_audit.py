"""Refresh stale owner navigation with preserved text and current receipts."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import re
import subprocess
import sys
from urllib.parse import unquote
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_COPY_RELEASE_QUESTIONS.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PACKAGING_NAVIGATION.json'
    delta = A / 'PACKAGING_OWNER_NAVIGATION_PROGRESS_DELTA.json'
    preservation = A / 'navigation-before-packaging-owner-refresh'
    assert all(not p.exists() for p in [checkpoint, delta, preservation])
    state = read(previous); now = datetime.now(timezone.utc).isoformat()
    audit_path = A / 'PLAYER_DIRECTOR_PACKAGING_INVENTORY_01.json'; audit = read(audit_path)
    assert audit['counts']['publicDataFiles'] == 51 and audit['counts']['directorDataFiles'] == 79
    for b in audit['publicDataFiles'] + audit['directorDataFiles'] + audit['sourceBindings']:
        assert info(G / b['path']) == b
    ex58_path = A / 'EX58_X01_FULFILLMENT.json'; ex58 = read(ex58_path)
    assert ex58['exactCandidateAuthoredApproval'] and not ex58['wholeGameFlowConfirmed']
    assert state['featSourceVerdict']['candidateAssembled'] and not state['featSourceVerdict']['exactCandidateApproved']
    assert state['featAcquisitionAudit']['correctionsFulfilled'] and not state['featAcquisitionAudit']['fullFeatCandidateApproved']
    start = G / 'START_HERE.md'; old_start = start.read_bytes().decode('utf-8')
    new_start = old_start; replacements = []
    def line_replace(prefix, replacement):
        nonlocal new_start
        matches = [line for line in new_start.splitlines() if line.startswith(prefix)]
        assert len(matches) == 1, prefix
        old = matches[0]; assert new_start.count(old) == 1
        new_start = new_start.replace(old, replacement, 1)
        replacements.append({'textReplace': True, 'old': old, 'replacement': replacement})
    line_replace('**Current joint review:**',
        '**Current joint review:** Seven rank-7 Divination spell candidates are in [exact review with GPT](docs/audit/2026-10-08/full-game/DI7_EXACT_REVIEW_01_SUBMISSION.json); the verdict is pending. The [authored spell index](DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json) remains **412 reviewed / 436 pending**, including the [136 complete standalone low-rank procedures](docs/audit/2026-10-08/full-game/LOW_RANK_136_EXACT_FULFILLMENT.json). All 335 feat identities have assembled candidate procedures; the [327-source ruling](docs/audit/2026-10-08/full-game/FEAT327_SOURCE_VERDICT_RESPONSE.json), acquisition corrections and named finite checks do not yet constitute full feat approval. Three [copy-release rule questions](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_PREPARATION.json) are prepared for after the spell verdict. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_PACKAGING_NAVIGATION.json) for the active queue. The owner requested a stop at **50% weekly Codex usage**; the latest measured usage is 48%.')
    line_replace('**Current position:',
        '**Current position: 13 October 2026.** The working finish line is a coherent campaign-playtest candidate. Human balance, publication approval and full companion implementation remain separate gates.')
    line_replace('| Feats | **8 of 335 reviewed;',
        '| Feats | **8 previously reviewed; 327 source-directed candidates assembled.** All 335 identities are retained; acquisition corrections and selected cadence, flora, nature and copy-capture checks are recorded | Full effect/use integration and exact review of the complete feat candidate; no full-suite approval |')
    line_replace('| Feats | [Internal feat queue]',
        '| Feats | The [complete source verdict](docs/audit/2026-10-08/full-game/FEAT327_SOURCE_VERDICT_RESPONSE.json) and [335-entry acquisition assembly](docs/audit/2026-10-08/full-game/FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json) supersede the old unsent-source status. [Nature’s finite scope is fulfilled](docs/audit/2026-10-08/full-game/FEAT335_NATURE_FINITE_FULFILLMENT.json); other effect/use work and full exact approval remain open. [Copy-release questions](docs/audit/2026-10-08/full-game/FEAT335_COPY_RELEASE_SOURCE_01_PREPARATION.json) are prepared but unsent. |')
    line_replace('| Expedition to Haven |',
        '| Expedition to Haven | The [corrected EX58 candidate completed exact authored review](docs/audit/2026-10-08/full-game/EX58_X01_FULFILLMENT.json): 58 source directions, 190 chapter examples, 29 transport profiles, 24 social scenarios and 21 integrated events. [Read the player book](DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md). Actual campaign grants, runtime and human balance remain separate; the earlier source handoff is preserved history. |')
    marker = '## Source books and authority'
    assert new_start.count(marker) == 1
    packaging = ('**Player/Director delivery is still open.** The [current packaging inventory](docs/audit/2026-10-08/full-game/PLAYER_DIRECTOR_PACKAGING_INVENTORY_01.json) records 51 public-data files and 79 Director-data files. Public paths include restricted candidates; they are not automatically approved for play. The legacy spell catalog contains only 276 operational entries, while the authored index adds 136 complete standalone procedures. The companion app remains development/owner tooling with broader reference data; no separate secret-free player build is certified. Cosmology content and doctrine remain for the required post-push review.\n\n')
    new_start = new_start.replace(marker, packaging + marker, 1)
    replacements.append({'textReplace': True, 'old': marker, 'replacement': packaging + marker})
    footer = '\nThe [complete start page before this status refresh](docs/audit/2026-10-08/full-game/navigation-before-packaging-owner-refresh/START_HERE.md) preserves every prior paragraph and link. This refresh changes navigation and status only.\n'
    new_start += footer
    replacements.append({'append': True, 'replacement': footer})
    inverse = new_start
    for op in reversed(replacements):
        if op.get('append'):
            assert inverse.endswith(op['replacement']); inverse = inverse[:-len(op['replacement'])]
        else:
            assert inverse.count(op['replacement']) == 1
            inverse = inverse.replace(op['replacement'], op['old'], 1)
    assert inverse == old_start
    # Check changed links now; the new checkpoint and preserved file are created below.
    generated = {checkpoint.resolve(), (preservation / 'START_HERE.md').resolve()}
    checked_links = []
    for op in replacements:
        for target in re.findall(r'\]\(([^)]+)\)', op['replacement']):
            if '://' in target or target.startswith('#'): continue
            q = (G / unquote(target.split('#')[0])).resolve()
            assert q.is_relative_to(G.resolve()) and (q.is_file() or q in generated), target
            checked_links.append(q.relative_to(G).as_posix())
    scope = ('Owner navigation now reflects the actual pending DI7 exact review, completed EX58 authored review and assembled335-feat source/acquisition state, retaining all earlier text in an exact preserved start page. '
        'Read-only packaging inventory hashes51 public and79 Director data files and traces literal local imports from both companion entrypoints. '
        'Public-path status does not confer approval; catalog-only spell export omits136 reviewed standalone procedures. '
        'Both entrypoints reach32 data sources; zero unresolved literal local imports is not a secret-free compiled-build or runtime claim. '
        'No audience projection, rule, candidate approval or cosmology doctrine changed. Actual GPT DI7 review remains live; copy source questions remain prepared and unsent. '
        'Usage48percent; owner stop50 remains mandatory. No source information deleted, GitHub push or whole-game signoff.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']; before = read(ledger_path); ledger = deepcopy(before)
    for row in ledger['aspects']:
        if row['id'] in {'DD-61', 'DD-65', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).append(audit_path.relative_to(G).as_posix())
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'packaging-source-inventory-and-owner-navigation',
                'recordedAtUtc': now, 'publicFiles': 51, 'directorFiles': 79, 'sourceGraphs': 2,
                'playerReleaseApproved': False, 'runtimeChanged': False})
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert all(old.get(k) == new.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if old['id'] not in {'DD-61', 'DD-65', 'DD-69'}: assert old == new
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "FEAT335_COPY_RELEASE_QUESTIONS_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain) == 1 and text.count(state['status']) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "PACKAGING_OWNER_NAVIGATION_PROGRESS_DELTA.json")["changes"]\n')
    text = text.replace(state['status'], scope, 1)
    marker = '    pending = [\n'; assert text.count(marker) == 1
    text = text.replace(marker, marker + '        ("Player/Director packaging inventory — release gate open", "PLAYER_DIRECTOR_PACKAGING_INVENTORY_01.json"),\n')
    compile(text, str(nav), 'exec'); preserved = []
    for p in [start, ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        dest = preservation / p.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(p.read_bytes()); assert dest.read_bytes() == p.read_bytes()
        preserved.append({**info(p), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    assert start.read_bytes().decode('utf-8') == old_start
    start.write_bytes(new_start.encode('utf-8'))
    ledger_path.write_bytes(encoded(ledger)); nav.write_text(text, encoding='utf-8', newline='\n')
    changes = [{'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, ledger_path, nav]]
    changes[0]['operationScope'] = 'Current status and source-linked owner navigation only; complete old bytes retained.'
    changes[0]['operations'] = replacements
    changes[0]['inverseReconstructsExactBeforeBytes'] = True
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': changes, 'sourceStatusBindings': [info(ex58_path), state['featSourceVerdict']['response']],
        'changedLinksChecked': sorted(set(checked_links)), 'allClosureAndHumanEvidenceUnchanged': True, 'sourceInformationDeleted': 0, 'newRuleAdoptions': 0}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode: print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), status=scope,
        goalTurnClassification='progress', previousGoalTurnClassification='progress',
        coverageLedger=info(ledger_path), coverageDelta=info(delta),
        navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
                    'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        playerDirectorPackagingInventory={'report': info(audit_path), 'playerReleaseApproved': False,
            'ownerStartPage': info(start), 'previousStartPage': info(preservation / 'START_HERE.md')})
    state['safeNextActions'][1] = 'Authoritative checkpoint AFTER_PACKAGING_NAVIGATION. Latest weekly usage48percent; stop at50.'
    state['safeNextActions'].insert(-1, 'Packaging inventory and START_HERE status refreshed. No player export or runtime certified; future export must use complete authored spell representations and explicit candidate/audience gates. Successful inventory/refresher are write-once; preserve original reports and do not rerun.')
    state.setdefault('preservationManifests', []).append(info(preservation / 'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    assert all((G / rel).is_file() for rel in checked_links)
    print(json.dumps({'checkpoint': info(checkpoint), 'startPage': info(start), 'changedLinksVerified': len(set(checked_links)),
                      'navigationLinks': navigation['existingDistinctLinks'], 'rulesChanged': 0}))


if __name__ == '__main__': main()
