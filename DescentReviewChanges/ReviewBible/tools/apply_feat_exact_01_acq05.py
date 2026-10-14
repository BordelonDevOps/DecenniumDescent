"""One-use application of actual GPT ACQ-05's seven guarded source replacements.

Preserve historical source direction, reports and original bytes. This operation
does not execute the twenty separately authored lifecycle acceptance groups.
"""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import zipfile
from apply_feat_exact_01_acq03 import read, info, encoded, at

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
V = A / 'feat327-acq05-source'


def main():
    receipt_path = A / 'FEAT327_ACQ_05_DERIVED_OPERATIONS.json'
    decision_path = A / 'FEAT327_ACQ_05_RECEIVED_DECISION.json'
    preservation = A / 'feat-exact-01-before-acq05'
    assert all(not p.exists() for p in [receipt_path, decision_path, preservation])
    archive = A / 'FEAT327_ACQ05_Addendum_and_Evidence.zip'
    archive_hash = '2e54e75f770b29d242045c892a4db39fefcb3d080c14aeef07747df0dbd41a48'
    assert info(archive)['sha256'] == archive_hash and archive.stat().st_size == 62411
    output_manifest = read(V / 'FILE_MANIFEST.json')
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == 11
        assert set(z.namelist()) == set(output_manifest['files']) | {'FILE_MANIFEST.json'}
        for name, bound in output_manifest['files'].items():
            data = z.read(name)
            assert len(data) == bound['bytes'] and sha256(data).hexdigest() == bound['sha256']
            assert (V / name).read_bytes() == data
    ops = read(V / 'ACQ05_EXACT_OPERATIONS.json')
    submission = A / ops['submission']['archive']
    assert info(submission)['sha256'] == ops['submission']['sha256']
    with zipfile.ZipFile(submission) as z:
        submitted = json.loads(z.read('PACKAGE_MANIFEST.json'))
        assert len(submitted) == 21
        for rel, bound in submitted.items():
            assert info(G / rel) == {'path': rel, **bound}, rel
    reviewer_path = V / 'ACQ05_EXECUTED_CHECK_REPORT.json'
    local_path = A / 'FEAT327_ACQ_05_LOCAL_REPRODUCTION.json'
    reviewer, local = read(reviewer_path), read(local_path)
    assert reviewer == local and local['checks'] == local['passed'] == 96 and local['failed'] == 0
    reviewer_bytes, local_bytes = reviewer_path.read_bytes(), local_path.read_bytes()
    assert local_bytes == reviewer_bytes or local_bytes == reviewer_bytes.replace(b'\n', b'\r\n')
    reply_path = A / 'FEAT327_ACQ_05_GPT_RESPONSE.json'
    reply = read(reply_path)
    message_id = 'bda5be25-7b23-4bd0-8afb-8adbb01a18f7'
    assert reply['status'] == 'response-complete' and len(reply['nodes']) == 1
    assert set(reply['nodes'][0]['messageIds'].split()) == {message_id}
    assert archive_hash in reply['nodes'][0]['text']
    assert ops['operationCount'] == len(ops['operations']) == 7
    assert ops['distinctExistingFiles'] == len({o['path'] for o in ops['operations']}) == 5
    originals, values, planned = {}, {}, {}
    for op in ops['operations']:
        rel = op['path']; path = G / rel
        if rel not in values:
            values[rel] = read(path) if op['op'] == 'replace_json_string' else path.read_text(encoding='utf-8')
            originals[rel] = deepcopy(values[rel])
        if op['op'] == 'replace_json_string':
            parent, key = op['pointer'].rsplit('/', 1)
            row = at(values[rel], parent)
            assert row['id'] == op['recordIdGuard'] == 'animal_companion'
            assert row[key] == op['old']
            row[key] = op['replacement']
        else:
            assert op['op'] == 'replace_text' and op['expectedOccurrences'] == 1
            assert values[rel].count(op['old']) == 1
            values[rel] = values[rel].replace(op['old'], op['replacement'])
    for rel, value in values.items():
        planned[G / rel] = encoded(value) if isinstance(value, dict) else value.encode('utf-8')
    # This index is prerequisite-only: no sixth procedure mirror exists to edit.
    contract_md = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md'
    assert ops['operations'][0]['old'] not in contract_md.read_text(encoding='utf-8')
    build = read(A / 'FEAT_EXACT_CANDIDATE_01_BUILD.json')
    protected_paths = set(build['originalSourceBindings']) | set(build['artifacts']) | set(submitted)
    protected_paths.add(contract_md.relative_to(G).as_posix())
    before_bindings = {rel: info(G / rel) for rel in sorted(protected_paths)}
    changes = []
    for path, data in planned.items():
        dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        assert dest.read_bytes() == path.read_bytes()
        changes.append({'before': {**info(path), 'preservedCopy': dest.relative_to(G).as_posix()},
            'after': {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}})
    manifest_path = preservation / 'PRESERVATION_MANIFEST.json'
    manifest_path.write_bytes(encoded([x['before'] for x in changes]))
    decision = {'receivedAtUtc': datetime.now(timezone.utc).isoformat(), 'id': 'FEAT327-ACQ-05',
        'replyMessageId': message_id, 'reply': info(reply_path), 'chatUrl': reply['chatUrl'],
        'browserId': '3', 'tabId': '125745532', 'archive': info(archive),
        'outputManifest': info(V / 'FILE_MANIFEST.json'), 'returnedPayloadsVerified': 10,
        'submittedPayloadsVerified': 21, 'reviewerChecksReproduced': 96,
        'reproductionComparison': {'reviewer': info(reviewer_path), 'local': info(local_path),
            'jsonEqual': True, 'byteEqual': reviewer_bytes == local_bytes,
            'onlyDifference': None if reviewer_bytes == local_bytes else 'LF versus Windows CRLF'},
        'completeAddendum': info(V / 'FEAT327_ACQ05_CONTROLLING_ADDENDUM.md'),
        'exactDirections': info(V / 'ACQ05_EXACT_OPERATIONS.json'),
        'lifecycleRecordContract': info(V / 'ACQ05_LIFECYCLE_RECORD_CONTRACT.json'),
        'acceptanceCases': info(V / 'ACQ05_ACCEPTANCE_EXPECTATIONS.json'),
        'disposition': 'Adopt paid ownership before bonding, attempt expenditure at valid start, and receiving-engine-specific replacement/transfer costs.',
        'finiteBehavioralAcceptanceComplete': False, 'candidateApproved': False, 'cosmologyReviewed': False}
    decision_path.write_bytes(encoded(decision))
    for path, data in planned.items():
        path.write_bytes(data)
    # Reverse only the seven prescribed edits and compare whole prior values.
    restored = {rel: read(G / rel) if rel.endswith('.json') else (G / rel).read_text(encoding='utf-8') for rel in values}
    for op in reversed(ops['operations']):
        rel = op['path']
        if op['op'] == 'replace_json_string':
            parent, key = op['pointer'].rsplit('/', 1)
            row = at(restored[rel], parent)
            assert row[key] == op['replacement']
            row[key] = op['old']
        else:
            assert restored[rel].count(op['replacement']) == 1
            restored[rel] = restored[rel].replace(op['replacement'], op['old'])
    assert restored == originals
    for change in changes:
        assert info(G / change['after']['path']) == change['after']
    for rel, bound in before_bindings.items():
        if rel not in values:
            assert info(G / rel) == bound, rel
    procedures = [at(read(G / op['path']), op['pointer']) for op in ops['operations'] if op['op'] == 'replace_json_string']
    assert len(procedures) == 5 and len(set(procedures)) == 1
    assert (V / 'ACQ05_ANIMAL_COMPANION_OPERATIVE.txt').read_text(encoding='utf-8').rstrip('\n') == procedures[0]
    receipt = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'addendumId': 'FEAT327-ACQ-05',
        'status': 'seven-exact-replacements-applied-twenty-behavioral-groups-outstanding',
        'actualGptDecision': info(decision_path), 'preservationManifest': info(manifest_path),
        'changes': changes, 'newFiles': [], 'beforeProtectedBindings': before_bindings,
        'sourceChecks': {'operationsApplied': 7, 'existingFilesChanged': 5, 'reviewerChecksReproduced': 96,
            'wholeFileReverseEquality': True, 'currentProcedureParity': True,
            'allOtherBoundSourcesUnchanged': True, 'originalsAndSourceDirectionPreserved': True,
            'prerequisitesAndRepeatMetadataPreserved': True, 'approvalAndSelectionFlagsUnchanged': True,
            'acquisitionMarkdownHasNoProcedureMirror': True},
        'historicalModel': info(R / 'tools/feat_exact_01_companion_acquisition_model.py'),
        'historicalReport': info(A / 'FEAT_EXACT_01_COMPANION_ACQUISITION_CHECK.json'),
        'historicalModelLimitation': 'Old completion-first payment staging is historical and must not govern the ACQ-05 purchase/attempt chronology. Its bounded HP results remain compatible.',
        'finiteBehavioralAcceptanceComplete': False, 'onlyThisNamedIssueClosed': False,
        'candidateApproved': False, 'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False}
    receipt_path.write_bytes(encoded(receipt))
    print(json.dumps({'received': info(decision_path), 'applied': info(receipt_path),
        'changedFiles': 5, 'guardedOperations': 7, 'sourceChecksReproduced': 96,
        'behavioralAcceptanceComplete': False}, indent=2))


if __name__ == '__main__':
    main()
