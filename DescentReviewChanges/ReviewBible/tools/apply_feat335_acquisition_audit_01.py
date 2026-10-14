"""Apply the fourteen reviewed edits after complete before-byte preservation."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from copy import deepcopy
import json
import shutil

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
V = A / 'feat335-acquisition-audit-01-verdict'


def read(path):
    return json.loads(path.read_text('utf-8-sig'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def save_new(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def locate(data, pointer):
    for token in pointer.strip('/').split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        data = data[int(token)] if isinstance(data, list) else data[token]
    return data


def main():
    operations_path = V / 'GUARDED_CORRECTIONS.json'
    operations = read(operations_path)['operations']
    assert len(operations) == 14
    preservation = A / 'before-feat335-acquisition-audit-01-corrections'
    receipt = A / 'FEAT335_ACQUISITION_AUDIT_01_DERIVED_OPERATIONS.json'
    assert not preservation.exists() and not receipt.exists()
    originals, parsed, texts, touched = {}, {}, {}, {}
    for number, op in enumerate(operations):
        path = G / op['path']
        assert path.resolve().is_relative_to(G.resolve())
        if op['path'] not in originals:
            originals[op['path']] = path.read_bytes()
        assert sha256(originals[op['path']]).hexdigest() == op['submittedSha256'], op['path']
        if op['op'] == 'replace_json_string':
            data = parsed.setdefault(op['path'], json.loads(originals[op['path']].decode('utf-8-sig')))
            parent_pointer, field = op['pointer'].rsplit('/', 1)
            parent = locate(data, parent_pointer)
            guard = op['recordGuard']
            assert parent['id'] == guard.get('id', guard.get('ruleId'))
            assert parent[field] == op['old'], op['pointer']
            parent[field] = op['replacement']
        elif op['op'] == 'replace_text':
            text = texts.setdefault(op['path'], originals[op['path']].decode('utf-8'))
            assert text.count(op['old']) == op['expectedOccurrences'], op['section']
            texts[op['path']] = text.replace(op['old'], op['replacement'])
        else:
            raise AssertionError('Unrecognized operation')
        touched.setdefault(op['path'], []).append(number)
    descendants = {rel: (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8') for rel, data in parsed.items()}
    descendants.update({rel: text.encode('utf-8') for rel, text in texts.items()})
    for rel, text in texts.items():
        if rel.endswith('.py'):
            compile(text, rel, 'exec')
    # Reconstruct the before-version from only the permitted JSON/string fields.
    for rel, data in parsed.items():
        reverse = deepcopy(data)
        for op in reversed([o for o in operations if o['path'] == rel]):
            parent, field = op['pointer'].rsplit('/', 1)
            locate(reverse, parent)[field] = op['old']
        assert reverse == json.loads(originals[rel].decode('utf-8-sig')), rel
    for rel, text in texts.items():
        reverse = text
        for op in reversed([o for o in operations if o['path'] == rel]):
            assert reverse.count(op['replacement']) == op['expectedOccurrences']
            reverse = reverse.replace(op['replacement'], op['old'])
        assert reverse.encode('utf-8') == originals[rel], rel
    saved = []
    for rel, old in originals.items():
        target = preservation / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(old)
        assert target.read_bytes() == (G / rel).read_bytes()
        saved.append({**info(G / rel), 'preservedCopy': target.relative_to(G).as_posix()})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'
    save_new(manifest, saved)
    unchanged_paths = [R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'data/director/feat_candidates/exact_01/supplements.json',
        R / 'data/public/spell_playtests/catalog.json', R / 'data/public/spell_playtests/authored_review_index.json',
        A / 'FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json', A / 'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json',
        A / 'FEAT_EXACT_01_FLORA_ACQUISITION_CHECK.json', R / 'tools/feat_exact_01_flora_acquisition.py']
    unchanged = [info(path) for path in unchanged_paths]
    for rel, data in descendants.items():
        assert (G / rel).read_bytes() == originals[rel]
        (G / rel).write_bytes(data)
        assert (G / rel).read_bytes() == data
    assert unchanged == [info(path) for path in unchanged_paths]
    pub = read(R / 'data/public/feat_candidates/exact_01/candidate.json')
    internal = read(R / 'data/director/feat_candidates/exact_01/candidate.json')
    contracts = read(A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')
    flora = pub['feats'][298]['operationalRules']
    assert flora == pub['feats'][298]['payloadOperational'] == internal['records'][287]['operationalRules'] == internal['records'][287]['payloadOperational'] == contracts['records'][298]['completeOperativeProcedure']
    assert flora in (R / 'docs/feats/exact-candidate-01/MAGIC_EXTENDED.md').read_text('utf-8')
    shared = read(R / 'data/public/feat_candidates/exact_01/shared_rules.json')['rules'][1]['wording']
    assert shared == read(R / 'data/director/feat_candidates/exact_01/shared_rules.json')['rules'][1]['wording']
    assert shared in (R / 'docs/feats/exact-candidate-01/SHARED_RULES.md').read_text('utf-8')
    data = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'auditId': 'FEAT335-ACQUISITION-AUDIT-01',
        'status': 'Fourteen guarded corrections applied and exactly preserved; finite acceptance evidence still pending.',
        'sourceOperations': info(operations_path), 'applier': info(Path(__file__)), 'preservationManifest': info(manifest),
        'operationCount': 14, 'changedFiles': len(descendants),
        'changes': [{'before': next(s for s in saved if s['path'] == rel), 'after': info(G / rel), 'operationIndexes': touched[rel]} for rel in descendants],
        'unchangedHistoricalAndSourceFiles': unchanged, 'newSourceIntegration': 'FAA-03 narrow profile-classification bridge only; other findings retain existing source rules.',
        'allOtherJsonFieldsAndTextUnchanged': True, 'originalObjectsPreserved': True, 'candidateFlagsUnchanged': True,
        'correctionsFulfilled': False, 'fullFeatCandidateApproved': False, 'runtimeImplemented': False,
        'sourceInformationDeleted': 0, 'cosmologyReviewed': False, 'pushed': False,
        'knownFollowThrough': ['Fresh immutable FAA04 report descendants; inherited contract source bindings remain historical and must be resolved explicitly.',
          'Reconcile current-total-level Flora capacity with the separately preserved FloraAcquisition override; reviewer edit retains the earlier opportunity-level expression.',
          'Paid STR/DEX provider and parent/child sequences; source-qualified unarmed/Claws adapter and use-gate boundaries; remaining finite initial-state groups.']}
    save_new(receipt, data)
    print(json.dumps({'receipt': info(receipt), 'operations': 14, 'changedFiles': len(descendants), 'historicalReportsChanged': 0, 'finiteAcceptancePending': True}, indent=2))


if __name__ == '__main__':
    main()
