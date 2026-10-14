"""Verify the received ACQ-04 package and apply its exact additive directions.

One-use operation. Existing bytes are preserved before changes; the separate
sixteen behavioral acceptance groups are not claimed complete here.
"""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import zipfile
from apply_feat_exact_01_acq03 import read, info, encoded, at

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'; V = A / 'feat327-acq04-source'


def main():
    receipt = A / 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json'
    received_path = A / 'FEAT327_ACQ_04_RECEIVED_DECISION.json'
    preservation = A / 'feat-exact-01-before-acq04'
    assert all(not p.exists() for p in [receipt, received_path, preservation])
    archive = A / 'FEAT327_ACQ04_Addendum_and_Evidence.zip'
    expected_archive = '6b8b40aa97338f2eab9e9214184991e4f4428f24495a07ca3d930c48c145a49a'
    assert info(archive)['sha256'] == expected_archive
    output_manifest = read(V / 'OUTPUT_MANIFEST.json')
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == 10
        assert set(z.namelist()) == set(output_manifest['files']) | {'OUTPUT_MANIFEST.json'}
        for name, bound in output_manifest['files'].items():
            data = z.read(name)
            assert len(data) == bound['bytes'] and sha256(data).hexdigest() == bound['sha256']
            assert (V / name).read_bytes() == data
    submitted = read(V / 'SUBMITTED_PACKAGE_MANIFEST.json')
    with zipfile.ZipFile(A / 'DD_FEAT327_ACQ04_External_Credentials_Source.zip') as z:
        assert z.read('PACKAGE_MANIFEST.json') == (V / 'SUBMITTED_PACKAGE_MANIFEST.json').read_bytes()
        for path, bound in submitted.items():
            assert info(G / path) == {'path': path, **bound}, path
    reproduction = []
    for name in ['SOURCE_BINDING_AUDIT.json', 'BOUND_SOURCE_EXCERPTS.json', 'SUBMITTED_PACKAGE_MANIFEST.json']:
        original_bytes = (V / name).read_bytes()
        local_path = A / 'feat327-acq04-local-reproduction' / name
        local_bytes = local_path.read_bytes()
        # The supplied checker uses platform-default text newlines on Windows.
        assert b'\r' not in original_bytes
        assert local_bytes == original_bytes or local_bytes == original_bytes.replace(b'\n', b'\r\n'), name
        assert read(V / name) == read(local_path), name
        reproduction.append({'reviewer': info(V / name), 'local': info(local_path),
                             'byteEqual': local_bytes == original_bytes, 'onlyDifference': None if local_bytes == original_bytes else 'LF versus Windows CRLF'})
    audit = read(V / 'SOURCE_BINDING_AUDIT.json')
    assert audit['checksExecuted'] == 101 and not audit['failedChecks'] and audit['payloadCount'] == 27
    reply = read(A / 'FEAT327_ACQ_04_GPT_RESPONSE.json')
    assert reply['status'] == 'complete' and len(reply['nodes']) == 1
    message_id = 'a469c764-37b9-4beb-9a8c-f485a071eb8d'
    assert set(reply['nodes'][0]['messageIds'].split()) == {message_id}
    assert expected_archive in reply['nodes'][0]['text']
    policy_source = V / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_POLICY.json'
    policy = read(policy_source); instructions = read(V / 'ACQ04_DERIVED_OPERATIONS.json')
    op = instructions['operations'][0]
    assert op['append'] == '\n\n' + policy['sharedAppend']
    public_path = G / op['path']; public = read(public_path)
    assert at(public, op['identityGuard']['pointer']) == op['identityGuard']['equals']
    old_wording = at(public, op['pointer'])
    assert sha256(old_wording.encode()).hexdigest() == op['expectedOldStringSha256']
    new_wording = old_wording + op['append']
    planned = {}; changes = []
    for path in [public_path, R / 'data/director/feat_candidates/exact_01/shared_rules.json']:
        value = read(path)
        assert value == public, 'Verify actual internal/public parity before mirroring'
        value['rules'][1]['wording'] = new_wording
        planned[path] = encoded(value)
    shared_md = R / 'docs/feats/exact-candidate-01/SHARED_RULES.md'
    text = shared_md.read_text(encoding='utf-8')
    assert text.count(old_wording) == 1
    planned[shared_md] = text.replace(old_wording, new_wording).encode('utf-8')
    contract_path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    contracts = read(contract_path); old_contracts = deepcopy(contracts)
    added_refs = {}
    for item in instructions['operations'][2:]:
        assert item['op'] == 'add_json_field' and item['path'] == contract_path.relative_to(G).as_posix()
        assert at(contracts, item['identityGuard']['pointer']) == item['identityGuard']['equals']
        parent_pointer, key = item['pointer'].rsplit('/', 1)
        row = at(contracts, parent_pointer)
        assert key == 'externalCredentialPolicyRef' and key not in row
        row[key] = item['value']; added_refs[row['id']] = item['value']
    assert set(added_refs) == set(policy['dispositions'])
    planned[contract_path] = encoded(contracts)
    md_path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md'
    md = md_path.read_text(encoding='utf-8')
    refs_text = '\n## External credential policy references — FEAT327-ACQ-04\n\n'
    refs_text += 'These four references supplement the unchanged prerequisite trees and complete procedures under ACQ04-EC1. Conditional test evidence never establishes actual campaign eligibility.\n\n| Feat ID | Controlling policy |\n|---|---|\n'
    for sid, reference in added_refs.items():
        target = reference.removeprefix('docs/audit/2026-10-08/full-game/')
        refs_text += f'| `{sid}` | [ACQ04-EC1 disposition]({target}) |\n'
    assert '## External credential policy references' not in md
    planned[md_path] = (md + refs_text).encode('utf-8')
    policy_target = A / policy_source.name
    assert not policy_target.exists() and len(planned) == 5
    # Every old output is preserved before the first replacement.
    for path, data in planned.items():
        bound = info(path); dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, dest)
        assert dest.read_bytes() == path.read_bytes()
        changes.append({'before': {**bound, 'preservedCopy': dest.relative_to(G).as_posix()},
                        'after': {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}})
    manifest = preservation / 'PRESERVATION_MANIFEST.json'
    manifest.write_bytes(encoded([x['before'] for x in changes]))
    received = {'receivedAtUtc': datetime.now(timezone.utc).isoformat(), 'id': policy['id'],
        'replyMessageId': message_id, 'reply': info(A / 'FEAT327_ACQ_04_GPT_RESPONSE.json'),
        'chatUrl': reply['chatUrl'], 'browserId': reply['browserId'], 'tabId': reply['tabId'],
        'archive': info(archive), 'outputManifest': info(V / 'OUTPUT_MANIFEST.json'),
        'returnedPayloadsVerified': 9, 'submittedPayloadsVerified': 27,
        'reviewerChecksReproduced': 101, 'reproductionComparison': reproduction,
        'completeAddendum': info(V / 'FEAT327_ACQ04_CONTROLLING_ADDENDUM.md'),
        'exactDirections': info(V / 'ACQ04_DERIVED_OPERATIONS.json'), 'policySource': info(policy_source),
        'acceptanceCases': info(V / 'ACQ04_ACCEPTANCE_CASES.json'),
        'disposition': 'KEEP four procedures; adopt scoped evidence contract and explicit current-source dispositions',
        'finiteBehavioralAcceptanceComplete': False, 'candidateApproved': False, 'cosmologyReviewed': False}
    received_path.write_bytes(encoded(received))
    for path, data in planned.items():
        path.write_bytes(data)
    shutil.copyfile(policy_source, policy_target)
    # Independent reverse-difference comparison: remove only the four new fields.
    restored = read(contract_path)
    for row in restored['records']:
        if row['id'] in added_refs:
            assert row.pop('externalCredentialPolicyRef') == added_refs[row['id']]
    assert restored == old_contracts
    for change in changes:
        assert info(G / change['after']['path']) == change['after']
    for path in [public_path, R / 'data/director/feat_candidates/exact_01/shared_rules.json']:
        restored = read(path)
        assert restored['rules'][1]['wording'] == new_wording
        restored['rules'][1]['wording'] = old_wording
        assert restored == public
    assert shared_md.read_text(encoding='utf-8').replace(new_wording, old_wording) == text
    assert md_path.read_text(encoding='utf-8') == md + refs_text
    for path, bound in submitted.items():
        if path not in {x['after']['path'] for x in changes}:
            assert info(G / path) == {'path': path, **bound}
    record = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'addendumId': policy['id'],
        'status': 'exact-additions-applied-behavioral-acceptance-outstanding',
        'actualGptDecision': info(received_path), 'preservationManifest': info(manifest),
        'changes': changes, 'newFiles': [info(policy_target)], 'addedContractReferences': added_refs,
        'sourceChecks': {'returnedManifestVerified': True, 'submittedSourcesUnchangedBeforeApplication': 27,
            'reproducedSourceChecks': 101, 'reproductionFilesContentEqual': 3,
            'reproductionDifference': 'Only platform text newlines in the two generated JSON files; original bytes retained',
            'existingContractFieldsUnchanged': True, 'fourProceduresAndTreesUnchanged': True,
            'allOtherSharedRulesAndExistingFS02TextUnchanged': True, 'internalPublicParity': True,
            'allOtherSubmittedInputsUnchanged': True, 'currentApprovalSelectionFlagsUnchanged': True},
        'finiteBehavioralAcceptanceComplete': False, 'onlyThisNamedIssueClosed': False,
        'candidateApproved': False, 'sourceInformationDeleted': False, 'cosmologyReviewed': False}
    receipt.write_bytes(encoded(record))
    print(json.dumps({'received': info(received_path), 'applied': info(receipt),
        'changedFiles': len(changes), 'newPolicyFiles': 1, 'sourceChecksReproduced': 101,
        'behavioralAcceptanceComplete': False}, indent=2))


if __name__ == '__main__':
    main()
