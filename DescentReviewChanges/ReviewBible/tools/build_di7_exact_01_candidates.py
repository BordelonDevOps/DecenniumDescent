"""Assemble unapproved DI7 cards from exact GPT substitutions, without promotion."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
from apply_di7_ap_as_01 import G, R, A, V, digest, info, encoded, node


def read(p):
    return json.loads(p.read_bytes())


def main():
    public_path = R / 'data/public/spell_candidates/divination_rank7_exact_01.json'
    internal_path = R / 'data/director/spell_candidates/divination_rank7_exact_01.json'
    manuscript_path = R / 'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md'
    evidence_path = A / 'DI7_EXACT_01_ASSEMBLY_CHECK.json'
    descendants = A / 'di7-exact-01-source-descendants'
    assert all(not p.exists() for p in [public_path, internal_path, manuscript_path, evidence_path, descendants])
    corrections = read(V / 'EXACT_DI7_CORRECTIONS.json')
    references = read(V / 'REFERENCE_DESCENDANTS.json')
    original = G / corrections['canonicalSubmittedPath']
    input_path = A / 'di7-joint-review-01-input' / corrections['currentReviewInputPath']
    assert digest(original.read_bytes()) == corrections['submittedSha256']
    assert digest(input_path.read_bytes()) == corrections['reviewInputSha256']
    assert len(corrections['changes']) == 18
    proofs, derived, outputs = [], [], []
    checks = []

    def check(name, condition):
        assert condition, name
        checks.append(name)

    for source, ref, filename in zip([original, input_path], references, ['original-proposal.source-directions.json', 'current-review-input.source-directions.json']):
        before_bytes = source.read_bytes()
        before = read(source)
        after = deepcopy(before)
        for operation in corrections['changes']:
            guard = operation.get('recordGuard')
            if guard:
                obj, key = node(after, guard['pointer'])
                check(source.name + ':' + guard['pointer'], obj[key] == guard['equals'])
            obj, key = node(after, operation['pointer'])
            check(source.name + ':old:' + operation['pointer'], obj[key] == operation['old'])
            obj[key] = deepcopy(operation['replacement'])
        after_bytes = encoded(after)
        reference_path = V / ref['newReferencePath']
        check(source.name + ':reviewer-whole-descendant', after_bytes == reference_path.read_bytes())
        check(source.name + ':reviewer-sha', digest(after_bytes) == ref['newSha256'] and len(after_bytes) == ref['newBytes'])
        inverse = deepcopy(after)
        for operation in reversed(corrections['changes']):
            obj, key = node(inverse, operation['pointer'])
            check(source.name + ':inverse:' + operation['pointer'], obj[key] == operation['replacement'])
            obj[key] = deepcopy(operation['old'])
        check(source.name + ':all-other-object-fields', inverse == before)
        check(source.name + ':inverse-original-bytes', encoded(inverse) == before_bytes or encoded(inverse, True) == before_bytes)
        out = descendants / filename
        outputs.append((out, after_bytes))
        proofs.append({'source': info(source), 'reviewerReference': info(reference_path), 'newDescendant': info(out, after_bytes), 'operations': 18,
            'inverseObjectAndOriginalBytesVerified': True, 'allOtherFieldsUnchanged': True, 'sourceRemainsImmutable': True})
        derived.append(after)

    current = derived[1]
    register = read(V / 'DI7_SOURCE_DECISION_REGISTER.json')
    dispositions = read(V / 'DI7_ORIGINAL_EXAMPLE_DISPOSITIONS.json')
    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    catalog = read(catalog_path)
    catalog_by_id = {x['id']: x for x in catalog['spells']}
    control = A / 'DI7_AP_AS_01_ACTIVE_COUNTERPART_CONTROL.json'
    apas = read(V / 'ALIGNMENT_SUGGESTION_AP_AS_01.json')
    check('AP-AS active catalog', catalog_by_id['alignment-suggestion']['operational']['resolution'] == apas['operationsOnNewDerivedCopies'][0]['replacement'])
    check('AP-AS preserved control exists', control.exists())
    metadata = {
        'mass-revelation': (60, 'One fixed 60-foot cone; source-origin line of effect; caster-only instantaneous snapshot.', 'Instantaneous', False),
        'premonition-shield': (120, 'One willing perceived ally, including self, within range and line of effect.', '60 elapsed seconds from resolution, or earlier termination; two qualifying occurrences.', False),
        'fate-echo': (120, 'One eligible original directly observed within 120 feet and line of effect; copied payload uses its own fresh targeting rules.', 'Outer and child commitments as specified; child duration follows its actual source; Ready has its own hold.', False),
        'vision-quest': (120, 'Self trance; one fixed question with a materially related perceived anchor within range and line of effect.', 'Concentration for 60 uninterrupted elapsed seconds from resolution; ordered answer at normal completion.', True),
        'faction-omniscience': (120, 'One known existing faction, nominated through a perceived local reference creature within range and line of effect.', 'Nonconcentration private feed for 60 elapsed seconds from resolution.', False),
        'alignment-purge': (120, 'One perceived creature within range and line of effect; hidden defined-axis eligibility is resolved after payment.', 'Concentration for at most 60 elapsed seconds from resolution.', True),
        'resonance-sight-supreme': (120, 'One perceived point within range and line of effect; fixed 20-foot-radius sphere with current center-to-portion line of effect.', 'Instantaneous', False),
    }
    now = datetime.now(timezone.utc).isoformat()
    cards = []
    for index, record in enumerate(current['records']):
        spell_id = record['spellId']
        source = record['fullSourceAndCurrentAccessRecord']
        check(spell_id + ':full-source-unchanged', source == catalog_by_id[spell_id])
        source_sha = digest(json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
        check(spell_id + ':original-source-object-sha', source_sha == record['sourceRecordSha256'])
        check(spell_id + ':preserved-null-status', source['operational'] is None and source['status'] == 'blocked-pending-operational-review')
        check(spell_id + ':access', source['classAccess'] == {
            provider: {'rank': 7, 'minimumClassLevel': level, 'school': 'Divination', 'baseRpCost': 17}
            for provider, level in [('Cleric', 13), ('Mirrorsage', 19), ('Shaman', 19), ('Wizard', 13)]})
        examples = [x for x in dispositions if x['spellId'] == spell_id]
        check(spell_id + ':corrected-original-examples', len(examples) == 2 and [x['replacement'] for x in examples] == record['workedCases'])
        feet, targets, duration, concentration = metadata[spell_id]
        preserved = {k: deepcopy(v) for k, v in record.items() if k not in ['procedure', 'workedCases']}
        cards.append({'id': spell_id, 'name': source['name'], 'candidateStatus': 'complete-source-directed-candidate-awaiting-finite-followthrough-and-exact-review',
            'approved': False, 'selectable': False, 'preservedSourceAndProposalFields': preserved,
            'operationalCandidate': {'activation': 'Action', 'school': 'Divination', 'rank': 7, 'baseRpCost': 17,
                'components': ['V', 'S', 'F'], 'rangeFeet': feet, 'targetingSummary': targets, 'durationSummary': duration,
                'concentrationRequiredByOuterEffect': concentration,
                'concentrationQualification': 'Fate Echo Ready holding and concentration children have their own mandatory transitions; false here is not an exemption.' if spell_id == 'fate-echo' else 'Use the full spell-specific lifecycle and shared casting rules.',
                'classAccess': deepcopy(source['classAccess']), 'completeProcedure': record['procedure'], 'workedCases': deepcopy(record['workedCases']),
                'examplesEvidenceKind': 'Authored conditional examples; no claim of full-procedure execution.',
                'summaryFieldsDoNotReplaceFullProcedure': True},
            'sourceDirectionBinding': {'file': proofs[1]['newDescendant'], 'pointer': f'/records/{index}'}})
    check('seven cards and fourteen examples', len(cards) == 7 and sum(len(x['operationalCandidate']['workedCases']) for x in cards) == 14)
    check('fourteen original issue IDs retained', [x['id'] for x in register['jointIssues']] == [x['id'] for x in current['explicitJointIssues']])
    check('seventeen full class envelopes', len(current['completeClassComparisons']) == 17)
    public = {'schemaVersion': '1.0', 'candidateId': 'DI7-EXACT-01', 'createdAtUtc': now,
        'status': 'UNAPPROVED-SOURCE-DIRECTED-CANDIDATES', 'exactReviewReceived': False, 'selectionEnabled': False,
        'scope': 'Seven complete authored candidate procedures. Source-direction agreement is recorded; finite follow-through and separate exact-card review remain. No ordinary catalog entry is promoted.',
        'sharedOperatingRules': deepcopy(current['sharedProposal']), 'cards': cards,
        'alignmentPairControllingException': {'id': 'AP-AS-01', 'scope': apas['scope'], 'classification': apas['classification'],
            'completeCurrentAlignmentSuggestionCard': deepcopy(catalog_by_id['alignment-suggestion']), 'currentCatalogBinding': info(catalog_path),
            'lowerCardReplacement': apas['operationsOnNewDerivedCopies'][0]['replacement'], 'sharedGuideReplacement': apas['operationsOnNewDerivedCopies'][1]['replacement'], 'authority': info(control)},
        'issueMap': [{'id': x['id'], 'affectedSpellIds': x['affectedSpellIds'], 'disposition': x['disposition'], 'decision': x['decision'], 'exactApproval': False} for x in register['jointIssues']],
        'audienceBoundary': 'Procedure text and explicitly conditional examples only. Actual world facts, protection maps, faction membership, actor grants and campaign dossiers remain private prerequisites.',
        'receiptOnlyBoundary': 'DI7-X14 / Planar Summons (Greater) remains unchanged with no authored operation. Cosmology follows the later verified GitHub push.',
        'runtimeImplemented': False, 'cosmologyReviewed': False, 'sourceInformationDeleted': 0, 'pushed': False}
    public_bytes = encoded(public)
    active_counterparts = []
    for item in current['completeCurrentCounterparts']:
        spell_id = item['id']
        index = next(i for i, x in enumerate(catalog['spells']) if x['id'] == spell_id)
        active_counterparts.append({'id': spell_id, 'completeCurrentCatalogCard': deepcopy(catalog_by_id[spell_id]),
            'currentCatalogBinding': {**info(catalog_path), 'pointer': f'/spells/{index}'},
            'sourceComparisonStatus': 'Only an actual current approved operative procedure can qualify as a payload; historical/unapproved comparison objects grant no permission.'})
    guide_path = R / 'docs/mechanics/SPELL_INTEGRATION_RULES.md'
    internal = {'candidateId': 'DI7-EXACT-01', 'createdAtUtc': now, 'status': public['status'], 'completePublicEnvelope': public,
        'publicEnvelopeBinding': info(public_path, public_bytes), 'sourceDirectionAuthority': read(V / 'DI7_CONTROLLING_CORRECTION_RECORD.json'),
        'preservedSourceDirectionEnvelope': current,
        'historicalEnvelopeQualification': 'All original comparison/source/hash/status fields remain exact submission history. Consult the active counterpart section and current integration guide below for AP-AS-01; no historical comparison overrides the named correction.',
        'activeCounterparts': active_counterparts, 'completeCurrentSpellIntegrationGuide': {'binding': info(guide_path), 'text': guide_path.read_text(encoding='utf-8')},
        'activeCounterpartControl': read(control), 'completeSourceDecisionRegister': register, 'originalExampleDispositions': dispositions,
        'fieldContracts': read(V / 'DI7_FIELD_CONTRACTS.json'), 'exactAcceptanceContract': read(V / 'DI7_NEXT_EXACT_ACCEPTANCE_CONTRACT.json'),
        'finiteExpectations': read(V / 'FINITE_DI7_EXPECTATIONS.json'), 'finiteFollowthroughComplete': False,
        'finiteEvidenceQualification': 'This assembly receipt verifies exact preservation, propagation, bindings and rendering. The 49 authored behavioral variants are not certified as executed by this receipt.',
        'sourceDescendantProofs': proofs, 'exactReviewReceived': False, 'selectionEnabled': False, 'runtimeImplemented': False, 'cosmologyReviewed': False, 'pushed': False}
    lines = ['# Divination rank 7 — exact candidate 01', '', public['scope'], '',
        'These are complete unapproved candidate cards. Original source fields are preserved in the accompanying public/internal records. KEEP and NEW labels distinguish retained source from the agreed authored directions.', '', '## Shared operating rules', '']
    for key, value in public['sharedOperatingRules'].items():
        lines.extend([f'### {key}', '', value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2), ''])
    for card in cards:
        op = card['operationalCandidate']
        lines.extend([f"## {card['name']} ({card['id']})", '',
            f"Action · Divination rank 7 · base 17 RP · V/S/F · {op['rangeFeet']} feet", '',
            'Access: Cleric/Wizard class 13; Mirrorsage/Shaman class 19, with actual retained acquisition and repertoire.', '',
            op['targetingSummary'], '', op['durationSummary'], '', op['concentrationQualification'], '',
            op['completeProcedure'], '', '### Corrected conditional examples', ''])
        for example in op['workedCases']:
            lines.extend([example, ''])
    lines.extend(['## Alignment Suggestion counterpart', '', apas['operationsOnNewDerivedCopies'][0]['replacement'], '', apas['operationsOnNewDerivedCopies'][1]['replacement'], '', '## Boundaries', '', public['audienceBoundary'], '', public['receiptOnlyBoundary'], ''])
    manuscript = '\n'.join(lines)
    for card in cards:
        check(card['id'] + ':full-procedure-rendered-once', manuscript.count(card['operationalCandidate']['completeProcedure']) == 1)
        for example in card['operationalCandidate']['workedCases']:
            check(card['id'] + ':whole-example-rendered', manuscript.count(example) == 1)
    check('public/internal parity', internal['completePublicEnvelope'] == public)
    for spell_id in metadata:
        check(spell_id + ':catalog unpromoted', catalog_by_id[spell_id]['operational'] is None)
    outputs.extend([(public_path, public_bytes), (internal_path, encoded(internal)), (manuscript_path, manuscript.encode())])
    for p, b in outputs:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
        check(p.name + ':written bytes', p.read_bytes() == b)
    evidence = {'recordedAtUtc': now, 'candidateId': 'DI7-EXACT-01', 'status': 'pass', 'checks': len(checks), 'passedChecks': checks, 'failures': [],
        'scope': 'Exact guarded source descent and byte inverse, full source/access preservation, unchanged status/null, public/internal and rendered-procedure parity. Not execution of all49 behavioral expectations.',
        'sourceDescendantProofs': proofs, 'outputs': [info(p) for p, _ in outputs], 'activeCounterpartOperations': info(A / 'DI7_AP_AS_01_DERIVED_OPERATIONS.json'),
        'authorityBindings': [info(V / name) for name in ['EXACT_DI7_CORRECTIONS.json', 'DI7_SOURCE_DECISION_REGISTER.json', 'DI7_ORIGINAL_EXAMPLE_DISPOSITIONS.json', 'DI7_NEXT_EXACT_ACCEPTANCE_CONTRACT.json']],
        'cards': 7, 'correctedOriginalExamples': 14, 'mechanicalIssues': 13, 'receiptOnlyIssues': 1, 'authoredFiniteGroups': 16, 'authoredFiniteVariants': 49,
        'finiteBehaviorFollowthroughComplete': False, 'ordinaryCountsUnchanged': {'reviewed': 412, 'pending': 436}, 'exactApproved': False,
        'selectionEnabled': False, 'runtimeImplemented': False, 'sourceInformationDeleted': 0, 'cosmologyReviewed': False, 'pushed': False}
    evidence_path.write_bytes(encoded(evidence))
    print(json.dumps({'evidence': info(evidence_path), 'checks': len(checks), 'cards': 7, 'examples': 14, 'finiteBehaviorFollowthroughComplete': False}))


if __name__ == '__main__':
    main()
