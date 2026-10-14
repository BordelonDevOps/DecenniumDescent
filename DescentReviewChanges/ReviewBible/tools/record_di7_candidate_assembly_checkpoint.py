"""Record DI7 candidate assembly and bounded alignment behavior without promotion."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, V, info, encoded, digest, node


def read(p):
    return json.loads(p.read_bytes())


def main():
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_NATURE_FULFILLMENT_AND_DI7_VERDICT.json'
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_CANDIDATE_ASSEMBLY_AND_ALIGNMENT_COMPONENT.json'
    delta = A / 'DI7_CANDIDATE_ASSEMBLY_PROGRESS_DELTA.json'
    readiness_path = A / 'DI7_EXACT_01_CURRENT_READINESS.json'
    preservation = A / 'navigation-before-di7-candidate-assembly'
    assert all(not p.exists() for p in [checkpoint, delta, readiness_path, preservation])
    state = read(previous)
    assembly_path = A / 'DI7_EXACT_01_ASSEMBLY_CHECK.json'
    component_path = A / 'DI7_ALIGNMENT_COMPONENT_CHECK.json'
    operations_path = A / 'DI7_AP_AS_01_DERIVED_OPERATIONS.json'
    assembly, component, operations = read(assembly_path), read(component_path), read(operations_path)
    assert assembly['status'] == component['status'] == 'pass' and not assembly['failures'] and not component['failures']
    assert assembly['checks'] == 182 and component['historyCount'] == 26
    for binding in assembly['outputs'] + assembly['authorityBindings'] + component['sourceBindings']:
        assert info(G / binding['path']) == binding
    for change in operations['changes']:
        before, after = change['before'], change['after']
        p = G / after['path']; saved = G / before['preservedCopy']
        assert info(p) == after and len(saved.read_bytes()) == before['bytes'] and digest(saved.read_bytes()) == before['sha256']
        current = p.read_bytes()
        if change['operations'][0].get('type') == 'exact-text':
            for op in reversed(change['operations']):
                assert current.count(op['replacement'].encode()) == 1
                current = current.replace(op['replacement'].encode(), op['old'].encode(), 1)
        else:
            data = json.loads(current)
            for op in reversed(change['operations']):
                obj, key = node(data, op['pointer']); assert obj[key] == op['replacement']; obj[key] = deepcopy(op['old'])
            current = encoded(data, saved.read_bytes() == encoded(json.loads(saved.read_bytes()), True))
        assert current == saved.read_bytes()
    preserve_checks = sum(x.endswith('-preserved') for x in component['passedChecks'])
    behavior_checks = component['checks'] - preserve_checks
    assert behavior_checks == 64 and preserve_checks == 520
    now = datetime.now(timezone.utc).isoformat()
    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    index_path = R / 'data/public/spell_playtests/authored_review_index.json'
    index_bytes = index_path.read_bytes(); index = read(index_path); original_index = deepcopy(index)
    assert index['authoredCounts'] == {'reviewed': 412, 'pending': 436}
    assert index['representationCounts'] == {'preservedLegacyOperationalRecords': 276, 'completeReviewedStandaloneProcedures': 136}
    old_sha = index['sourceCatalogSha256']
    assert old_sha == '1227af1d81eebf793adda68b6b375f3b351629929eb022526fb8ce4642b0c584'
    index['sourceCatalogSha256'] = digest(catalog_path.read_bytes())
    crlf = index_bytes == encoded(original_index, True)
    assert encoded(original_index, crlf) == index_bytes
    inverse = deepcopy(index); inverse['sourceCatalogSha256'] = old_sha
    assert inverse == original_index and encoded(inverse, crlf) == index_bytes
    scope = ('DI7 seven complete source-directed candidates and14 corrected original examples are assembled in full public/internal records and a readable manuscript. '
        'All18 guarded substitutions match the actual GPT reference descendants, with exact inverse preservation;182 assembly checks pass. '
        'AP-AS-01 is applied in8 active counterpart/card/guide files with202 current catalog dependency bindings refreshed; original bytes and embedded historical records remain preserved. '
        'The discovery index receives only the measured current catalog hash, preserving every entry and status. '
        'The alignment component has64 behavioral assertions across26 conditional histories plus520 unchanged identity/acquisition/immunity/allowance assertions. '
        'It covers the named pair, binary saves and outside-initiative effect lifecycles; actual casting/payment/provider/components/counter and Suggestion initiative-clock integration remain open. '
        'The16 groups/49 complete DI7 expectations are not yet fulfilled, and no exact-card review or promotion is claimed. '
        'Overall authored spell coverage stays412 reviewed/436 pending across276 catalog records and136 standalone procedures. '
        'Latest weekly usage37percent used; stop at50 remains controlling. Final joint whole-game flow agreement precedes authorized push, verified remote and careful cosmology. Nothing deleted or pushed.')
    ledger_path = R / 'data/playtest/game_development_coverage.json'; nav = R / 'tools/build_review_map.py'
    assert info(ledger_path) == state['coverageLedger']
    old_ledger = read(ledger_path); ledger = deepcopy(old_ledger)
    evidence = [assembly_path, component_path, operations_path, readiness_path]
    for row in ledger['aspects']:
        if row['id'] in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            row.setdefault('completedScopes', []).append(scope)
            row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda', []).append({'id': 'DI7-candidate-assembly-and-alignment-component', 'recordedAtUtc': now,
                'completeCandidates': 7, 'assemblyChecks': 182, 'alignmentBehaviorAssertions': 64, 'conditionalHistories': 26,
                'fullDI7FiniteFollowthroughComplete': False, 'exactCardsApproved': False})
    for before, after in zip(old_ledger['aspects'], ledger['aspects']):
        assert all(before.get(k) == after.get(k) for k in ['closure', 'humanEvidence', 'ownerEvidence'])
        if before['id'] not in {'DD-09', 'DD-12', 'DD-14', 'DD-69'}:
            assert before == after
    assert {k: v for k, v in old_ledger.items() if k != 'aspects'} == {k: v for k, v in ledger.items() if k != 'aspects'}
    text = nav.read_text(encoding='utf-8')
    chain = ' + read(A / "NATURE_FULFILLMENT_DI7_VERDICT_PROGRESS_DELTA.json")["changes"]\n'
    assert text.count(chain) == 1
    text = text.replace(chain, chain.rstrip('\n') + ' + read(A / "DI7_AP_AS_01_DERIVED_OPERATIONS.json")["changes"] + read(A / "DI7_CANDIDATE_ASSEMBLY_PROGRESS_DELTA.json")["changes"]\n')
    assert text.count(state['status']) == 1
    text = text.replace(state['status'], scope, 1)
    pending_marker = '    pending = [\n'
    assert text.count(pending_marker) == 1
    items = [('DI7 complete candidate assembly —182 preservation and parity checks', assembly_path),
        ('DI7 alignment component —64 behavior assertions in26 conditional histories', component_path),
        ('DI7 current readiness —full casting and finite follow-through remain', readiness_path),
        ('AP-AS-01 applied counterpart changes —preserved originals and exact inverse', operations_path),
        ('AP-AS-01 controlling active readers', A / 'DI7_AP_AS_01_ACTIVE_COUNTERPART_CONTROL.json')]
    text = text.replace(pending_marker, pending_marker + ''.join('        (' + json.dumps(label) + ', ' + json.dumps(p.relative_to(A).as_posix()) + '),\n' for label, p in items))
    marker = '    featured = [\n'; assert text.count(marker) == 1
    candidate_files = [R / 'data/public/spell_candidates/divination_rank7_exact_01.json', R / 'data/director/spell_candidates/divination_rank7_exact_01.json', R / 'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md']
    text = text.replace(marker, marker + ''.join('        (' + json.dumps(label) + ', ' + json.dumps(p.relative_to(G).as_posix()) + '),\n' for label, p in zip(
        ['Seven Divination candidates —public complete cards, unapproved', 'Seven Divination candidates —internal full source envelope', 'Seven Divination candidates —readable manuscript'], candidate_files)))
    compile(text, str(nav), 'exec')
    preserved = []
    for p in [index_path, ledger_path, nav, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        dest = preservation / p.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(p.read_bytes()); assert dest.read_bytes() == p.read_bytes()
        preserved.append({**info(p), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    index_path.write_bytes(encoded(index, crlf)); ledger_path.write_bytes(encoded(ledger)); nav.write_text(text, encoding='utf-8', newline='\n')
    readiness = {'recordedAtUtc': now, 'candidateId': 'DI7-EXACT-01', 'status': 'assembled-with-partial-finite-behavior-evidence',
        'assembly': info(assembly_path), 'alignmentComponent': info(component_path), 'alignmentBehaviorAssertions': behavior_checks,
        'unchangedIdentityAndAcquisitionAssertions': preserve_checks, 'conditionalHistories': 26,
        'APASOperations': info(operations_path), 'currentAuthoredIndex': info(index_path), 'catalogBinding': info(catalog_path),
        'indexRebindOnly': {'pointer': '/sourceCatalogSha256', 'old': old_sha, 'replacement': index['sourceCatalogSha256'], 'everyOtherFieldUnchanged': True},
        'overallAuthoredCounts': index['authoredCounts'], 'representationCounts': index['representationCounts'],
        'fullFiniteGroups': 16, 'fullFiniteVariants': 49, 'fullFiniteFulfilled': False,
        'nextWork': ['Integrate source-qualified DI7 ordinary casting/provider/repertoire/components/cost/concentration/counter histories.',
            'Execute the remaining Mass/Shield/Fate/Vision/Faction/Supreme and shared49-variant contract; alignment component requires actual-cast and Suggestion phase-clock integration.',
            'Then submit all seven complete candidates and public/internal envelopes for separate exact review in the existing actual GPT chat. Do not resend the finished source conference.'],
        'exactApproved': False, 'selectionEnabled': False, 'runtimeImplemented': False, 'cosmologyReviewed': False, 'pushed': False}
    readiness_path.write_bytes(encoded(readiness))
    changes = [{'before': next(x for x in preserved if x['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [index_path, ledger_path, nav]]
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': changes, 'allOtherAspectsUnchanged': True,
        'allClosureAndHumanEvidenceUnchanged': True, 'sourceInformationDeleted': 0, 'spellPromotions': 0}))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if run.returncode:
        print(run.stdout); print(run.stderr); raise SystemExit(run.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now, previousCheckpoint=info(previous), goalTurnClassification='progress', status=scope,
        coverageLedger=info(ledger_path), coverageDelta=info(delta),
        navigation={'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        di7CandidateAssembly=readiness, newRuleAdoptions=0,
        newRuleAdoptionCountScope='Seven candidates remain unapproved. Only the already source-agreed AP-AS-01 named interface is propagated; this is not a new exact-card adoption.')
    state['newSpellCohort'].update(reviewStatus='source-conference-complete; seven-exact-candidates-assembled; finite-followthrough-and-exact-review-pending',
        currentAssembly=info(assembly_path), currentReadiness=info(readiness_path), alignmentComponent=info(component_path))
    state['activeGptReview']['instruction'] = 'The actual DI7 source verdict is received. Seven full candidates and AP-AS-01 propagation now exist. Finish meaningful finite49-variant follow-through and actual-cast seams, then send the seven complete candidates for their separate exact review. No source-conference resubmission.'
    state['safeNextActions'] = [state['safeNextActions'][0],
        'Authoritative checkpoint AFTER_DI7_CANDIDATE_ASSEMBLY_AND_ALIGNMENT_COMPONENT. Fresh weekly usage37percent used at checkpoint. Owner stop at50 persists.',
        state['activeGptReview']['instruction'],
        'Do not rerun write-once apply_di7_ap_as_01.py/build_di7_exact_01_candidates.py/validate_di7_alignment_component.py or this recorder. Preserve successful reports; add new versioned evidence when extending behavior.',
        'DI7_ALIGNMENT_COMPONENT_CHECK has64 behavioral assertions across26 histories plus520 unchanged-record assertions. It is conditional effect-component evidence only; it supplies no actual acquisition/payment/counter or Suggestion initiative clock. Do not count the four D7T13 variants fully fulfilled.',
        'DI7_EXACT_01_ASSEMBLY_CHECK has182 exact source-preservation and rendering checks. Original proposal/review input and18 guarded descendants are unchanged outside named operations. Active counterpart changes and index hash-only rebind are in measured deltas.',
        'Nature47 finite variants remain fulfilled. Continue copy paid release and other full-feat, bestiary, Director and packaging scopes after the appropriate DI7 work.',
        'Chrome3 recovered tab125745946 points at Calibration Review Part2; actual DI7 source verdict terminal, no reply pending. Use computer-use skill and re-mark live tab when resuming actual GPT collaboration.',
        state['safeNextActions'][-1]]
    state.setdefault('preservationManifests', []).append(info(preservation / 'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint': info(checkpoint), 'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': [], 'readiness': info(readiness_path), 'weeklyUsedPercent': 37}))


if __name__ == '__main__':
    main()
