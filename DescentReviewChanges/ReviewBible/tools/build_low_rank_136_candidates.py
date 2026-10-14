"""Author complete review-only cards from the final LR source directions.

This tool writes separate candidate artifacts. It never imports, changes or promotes
the live spell catalog. The final source records and field absence remain intact.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'low-rank137-source-reviewer-files'
INTERNAL = R / 'data/playtest/spell_drafts/candidate_low_rank_136.json'
PUBLIC = R / 'data/public/spell_playtests/candidate_low_rank_136.json'
MANUSCRIPT = R / 'docs/playtest/LOW_RANK_136_CANDIDATE.md'
PUBLIC_MANUSCRIPT = PUBLIC.with_suffix('.md')
CASES = R / 'data/playtest/spell_drafts/low_rank_137_authored_boundaries.json'
PUBLIC_CASES = PUBLIC.parent / 'low_rank_137_authored_boundaries.json'
CASEBOOK = R / 'docs/playtest/LOW_RANK_137_AUTHORED_BOUNDARIES.md'
PUBLIC_CASEBOOK = PUBLIC_CASES.with_suffix('.md')


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    path.write_text(text, encoding='utf-8', newline='\n')


# Editorial substitutions only. All operative sentences, quantities and exceptions
# remain verbatim from the final register, which is retained beside the candidate.
INTRO = {
    'Adopt the supplied Silent Echo proposal as NEW authoring direction. ': '',
    'Adopt the supplied Blurred Visage proposal. ': '',
    'Adopt the supplied minor-disguise proposal: ': '',
    'Adopt the supplied Silence proposal. ': '',
    'Adopt the proposal: ': '',
}
FIELDS = {
    'activation': 'castingTime', 'range': 'range', 'components': 'components',
    'target': 'targets', 'duration': 'duration', 'resolution': 'resolution',
    'procedure': 'effect', 'limitsAndLifecycle': 'limitations',
    'numericParameters': 'numericParameters',
}
PUBLIC_CARD_FIELDS = (
    'id', 'name', 'status', 'selectionEnabled', 'visibility', 'sourceQuestionId',
    'sourceDecisionId', 'sourceReceipt', 'classAccess', 'additionalRpCost',
    'bookBindings', 'sourceModeBindings', 'sourceBookMentionDoesNotGrantAcquisition',
    'operationalCandidate', 'sharedRuleIds', 'sourceConflicts',
    'operationPrerequisites', 'authoredBoundary', 'newDecisionNotice',
    'reviewEvidence',
)


def operational(row):
    if row['authoring'] is None:
        assert row['spellId'] == 'blink'
        return None
    result = {dest: deepcopy(row['authoring'][src]) for src, dest in FIELDS.items()}
    for before, after in INTRO.items():
        if result['effect'].startswith(before):
            result['effect'] = after + result['effect'][len(before):]
            result['effect'] = result['effect'][0].upper() + result['effect'][1:]
            break
    result['costProcedure'] = (
        'Use the actual acquired class grant and its preserved classAccess row for '
        'rank, minimum class level, school and base RP. Apply that class’s completed '
        'casting engine, current repeat history, discounts, Dissonance surcharge and '
        'this identity’s additionalRpCost; use LR-G01, LR-G02 and the explicit '
        'payload/wrapper exceptions in this card. Oracle RC is separate. Sufficient '
        'resources do not grant acquisition. Pay committed costs even on a miss, '
        'successful resistance or counter. There is no generic upcast or level scaling.'
    )
    return result


def card(row):
    receipt = deepcopy(row['fullSourceAndCurrentAccessRecord'])
    out = {
        'id': row['spellId'], 'name': row['name'],
        'status': 'receipt-only-post-push-cosmology' if row['authoring'] is None else 'candidate-exact-review-pending',
        'selectionEnabled': False, 'visibility': receipt['visibility'],
        'sourceQuestionId': row['questionId'], 'sourceDecisionId': row['decisionId'],
        'sourceReceipt': receipt,
        'bookBindings': deepcopy(row['bookBindings']),
        'sourceModeBindings': deepcopy(row['sourceModeBindings']),
        'sourceBookMentionDoesNotGrantAcquisition': True,
        'operationalCandidate': operational(row),
        'sharedRuleIds': deepcopy(row['sharedPolicyRefs']),
        'sourceConflicts': deepcopy(row['explicitConflictDispositions']),
        'operationPrerequisites': deepcopy(row['particularOperationPrerequisites']),
        'authoredBoundary': deepcopy(row['workedBoundary']),
        'newDecisionNotice': row['authoring']['newDecisionNotice'] if row['authoring'] else None,
        'reviewEvidence': {
            'sourceReviewId': 'LR-SOURCE-2026-10-11',
            'exactCandidateApproval': False, 'catalogPromotionAuthorized': False,
            'runtimeVerified': False, 'humanPlaytested': False,
        },
        'internalSourceAuthoringRecord': deepcopy(row),
    }
    # Preserve absence rather than fill in an invented null/default.
    for field in ('classAccess', 'additionalRpCost'):
        if field in receipt:
            out[field] = deepcopy(receipt[field])
    return out


def project_card(value):
    return {key: deepcopy(value[key]) for key in PUBLIC_CARD_FIELDS if key in value}


def manuscript(envelope):
    lines = [
        '# Low-rank spell candidates — complete review manuscript', '',
        '**Status: 136 authored candidates awaiting exact joint review; Blink is a preserved receipt.**', '',
        'These separate draft cards are unavailable in the operational catalog. Their full original '
        'source records, class access and all 141 book bindings are in the companion JSON. '
        'The 20 shared rules below are part of every applicable card. NEW labels identify '
        'source-authoring decisions; they do not claim those details were printed in the old sources.', '',
        'The full-game flow review, human playtesting, GitHub push and later careful cosmology '
        'review remain separate. No source has been deleted or promoted by creating this manuscript.', '',
        '## Shared operating rules', '',
    ]
    for policy in envelope['sharedRules']:
        lines += [f"### {policy['id']} — {policy['title']}", '', policy['wording'], '']
    lines += ['## Complete cards', '']
    for c in envelope['spells']:
        lines += [f"### {c['sourceQuestionId']} — {c['name']}", '',
                  f"Identity: `{c['id']}`. Source decision: `{c['sourceDecisionId']}`. Status: **{c['status']}**.", '']
        if 'classAccess' in c:
            lines += ['| Actual class access | Rank | Minimum class level | School | Base RP |',
                      '| --- | --- | --- | --- | --- |']
            for name, access in c['classAccess'].items():
                lines.append('| ' + ' | '.join([name] + [str(access.get(k, '(absent)')) for k in ('rank', 'minimumClassLevel', 'school', 'baseRpCost')]) + ' |')
            lines += ['', f"Additional RP cost: {json.dumps(c.get('additionalRpCost', '(absent)'), ensure_ascii=False)}. Acquisition and the actual class engine still apply.", '']
        op = c['operationalCandidate']
        if op is None:
            lines += ['**No operational procedure.** Preserve the original Blink record and literal source references. '
                      'Cosmology review follows the authorized push and verified remote commit.', '']
        else:
            for key, label in [('castingTime','Casting time'),('range','Range'),('components','Components'),
                               ('targets','Targets and mode'),('duration','Duration'),('resolution','Resolution'),
                               ('costProcedure','Cost and access'),('effect','Effect'),('limitations','Limits and ending')]:
                lines += [f'**{label}.** {op[key]}', '']
            lines += ['**Numerical parameters.**', '', '```json', json.dumps(op['numericParameters'], ensure_ascii=False, indent=2), '```', '']
        lines += ['**Shared rules.** ' + ', '.join(c['sharedRuleIds']) + '.', '',
                  '**Source-mode bindings.**', '', '```json', json.dumps(c['sourceModeBindings'], ensure_ascii=False, indent=2), '```', '']
        for label, key in [('Source conflict disposition','sourceConflicts'), ('Use-time prerequisite','operationPrerequisites')]:
            for text in c[key]:
                lines += [f'**{label}.** {text}', '']
        lines += [f"**Authored example ({c['authoredBoundary']['kind']}).** {c['authoredBoundary']['wording']}", '']
        if c['newDecisionNotice']:
            lines += [f"**Source-authoring notice.** {c['newDecisionNotice']}", '']
    return '\n'.join(lines)


def boundaries(register):
    worked = read(P / 'LR_WORKED_BOUNDARIES.json')
    proposals = read(P / 'LR_8_PROPOSAL_DISPOSITIONS.json')
    cases = []
    for original in worked['perSpellBoundaries']:
        cases.append({'id': 'LR-C-' + original['questionId'], 'group': 'per-identity',
                      'questionIds': [original['questionId']], 'authoredExpectation': deepcopy(original),
                      'runtimePassed': False})
    for original in worked['jointBoundaries']:
        cases.append({'id': original['id'], 'group': 'joint-sequence',
                      'questionIds': deepcopy(original['questionIds']), 'authoredExpectation': deepcopy(original),
                      'runtimePassed': False})
    for proposal in proposals['records']:
        for original in proposal['boundaryDispositions']:
            cases.append({'id': original['id'], 'group': 'proposal', 'questionIds': [proposal['questionId']],
                          'authoredExpectation': deepcopy(original), 'runtimePassed': False})
    assert len(cases) == 187 and len({c['id'] for c in cases}) == 187
    out = {'schemaVersion': '1.0', 'status': 'authored-expectations-awaiting-exact-review',
           'scope': '137 identity examples (Blink receipt included), 18 joint sequences and 32 proposal boundaries. '
                    'No record is an executed gameplay test or human balance result.', 'cases': cases}
    lines = ['# Low-rank spell authored boundary casebook', '', out['scope'], '']
    for c in cases:
        lines += [f"## {c['id']}", '', 'Applies to: ' + ', '.join(c['questionIds']) + '.', '',
                  '```json', json.dumps(c['authoredExpectation'], ensure_ascii=False, indent=2), '```', '']
    return out, '\n'.join(lines)


def main():
    if (A / 'LOW_RANK_136_EXACT_FULFILLMENT.json').exists():
        raise RuntimeError('The reviewed LRX procedures already exist. This historical baseline builder must not overwrite their corrections or review labels; use the frozen submission for baseline reproduction.')
    from manifest_loader import load_protected_manifest
    protected = load_protected_manifest(G)
    assert len(protected) == 342
    for relative, expected in protected.items():
        assert digest(G / relative) == expected, f'Protected input drift: {relative}'
    register = read(P / 'LR_137_AUTHORING_REGISTER.json')
    records = register['records']
    catalog = {s['id']: s for s in read(R / 'data/public/spell_playtests/catalog.json')['spells']}
    assert len(records) == len({r['spellId'] for r in records}) == 137
    for row in records:
        assert row['fullSourceAndCurrentAccessRecord'] == catalog[row['spellId']], row['spellId']
        assert row['fullSourceAndCurrentAccessRecord']['operational'] is None
    metadata = {
        'schemaVersion': '1.0', 'version': 'LR-CANDIDATE-1',
        'status': 'DRAFT-EXACT-REVIEW-PENDING-NOT-SELECTABLE',
        'scope': '136 complete ordinary spell candidates plus Blink receipt. Separate authored review envelope; '
                 'no live catalog promotion, numerical-balance or runtime certification.',
        'selectionEnabled': False,
        'sourceReview': {'id': 'LR-SOURCE-2026-10-11',
                         'finalReplyId': '6ecc2e79-e637-4c69-ac48-61069296008c',
                         'registerSha256': digest(P / 'LR_137_AUTHORING_REGISTER.json'),
                         'sharedRulesSha256': digest(P / 'LR_SHARED_OPERATING_DIRECTIONS.json'),
                         'sourceVerdictSha256': digest(P / 'LR_137_SOURCE_AUTHORING_VERDICT.md')},
        'sharedRules': deepcopy(read(P / 'LR_SHARED_OPERATING_DIRECTIONS.json')['policies']),
    }
    internal = {**deepcopy(metadata), 'spells': [card(row) for row in records]}
    public = {**deepcopy(metadata), 'spells': [project_card(c) for c in internal['spells']]}
    assert sum(c['operationalCandidate'] is not None for c in public['spells']) == 136
    save(INTERNAL, internal)
    save(PUBLIC, public)
    doc = manuscript(public)
    save(MANUSCRIPT, doc)
    save(PUBLIC_MANUSCRIPT, doc)
    cases, casebook = boundaries(register)
    for path in (CASES, PUBLIC_CASES):
        save(path, cases)
    for path in (CASEBOOK, PUBLIC_CASEBOOK):
        save(path, casebook)
    mapping = {'status': 'candidate-authoring-map-not-approval', 'records': []}
    for index, row in enumerate(records):
        mapping['records'].append({
            'questionId': row['questionId'], 'spellId': row['spellId'], 'sourceDecisionId': row['decisionId'],
            'sourceQuestion': row['sourceQuestion'], 'disposition': row['disposition'],
            'publicCardPointer': f'/spells/{index}',
            'fullOperationalPointer': f'/spells/{index}/operationalCandidate',
            'manuscriptHeading': f"{row['questionId']} — {row['name']}",
            'authoringToCandidateFieldMap': FIELDS if row['authoring'] else {},
            'sourceModeBindings': deepcopy(row['sourceModeBindings']),
            'bookBindings': deepcopy(row['bookBindings']),
            'exactCandidateApproval': False,
        })
    mapping_path = A / 'LOW_RANK_136_CANDIDATE_QUESTION_MAP.json'
    save(mapping_path, mapping)
    paths = [INTERNAL, PUBLIC, MANUSCRIPT, PUBLIC_MANUSCRIPT, CASES, PUBLIC_CASES, CASEBOOK, PUBLIC_CASEBOOK, mapping_path]
    for relative, expected in protected.items():
        assert digest(G / relative) == expected, f'Protected input drift after authoring: {relative}'
    receipt = {'status': 'complete-candidate-artifacts-authored-exact-review-pending',
               'mechanicalCards': 136, 'receiptOnly': ['blink'], 'bookBindings': sum(len(r['bookBindings']) for r in records),
               'sharedRules': len(metadata['sharedRules']), 'authoredBoundaryRecords': len(cases['cases']),
               'protectedSubmittedInputsUnchanged': len(protected),
               'sourceRecordsEqualCurrentPublicCatalog': 137,
               'sourceRecordsPromoted': 0, 'runtimeVerified': False, 'humanPlaytested': False,
               'artifacts': {str(p.relative_to(G)).replace('\\', '/'): {'bytes': p.stat().st_size, 'sha256': digest(p)} for p in paths}}
    save(A / 'LOW_RANK_136_CANDIDATE_AUTHORING_RECEIPT.json', receipt)
    print(json.dumps({k: v for k, v in receipt.items() if k != 'artifacts'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
