"""Bind the two GPT-requested Short Rest evidence closures to exact source and artifacts."""
import argparse
import difflib
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import zipfile


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(test, message):
    if not test:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--implementation', required=True)
    parser.add_argument('--ordering', type=Path, required=True)
    parser.add_argument('--requests', type=Path, required=True)
    parser.add_argument('--replacement', type=Path, required=True)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    raw = subprocess.check_output(['git', 'archive', '--format=zip', args.implementation, 'engine'])
    archive = zipfile.ZipFile(io.BytesIO(raw))
    artifacts = {}

    def retain(source, relative):
        target = packet / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        payload = target.read_bytes()
        artifacts[relative] = dict(bytes=len(payload), sha256=sha(payload))

    ordering = read(args.ordering / 'results.json')
    require(ordering['Status'] == 'PASS' and ordering['Implementation'] == args.implementation
            and ordering['SourceArchiveSha256'] == sha(raw), 'Ordering evidence has the wrong source.')
    pending_sha = sha((packet / 'focused/short-rest-pending.ddsave').read_bytes())
    require(ordering['PendingSaveSha256'] == pending_sha, 'Ordering pending save differs.')
    retain(args.ordering / 'results.json', 'ordering/results.json')
    for variant, expected in [('observed-original', 'PASS'), ('reversed-order', 'EXPECTED_FAIL')]:
        folder = args.ordering / variant
        result = read(folder / 'results.json')
        require(result == ordering['Variants'][variant] and result['OrderingAssertion'] == expected
                and result['Observations'] == 1 and result['FinalRest'] == 'Completed'
                and result['FinalGrant'] == 'Expired' and result['PendingSaveSha256'] == pending_sha,
                f'Ordering variant failed: {variant}')
        observation = result['AtCompletionWrite']
        require(observation['Clock'] == result['ExpectedDeadline'] and observation['RestBeforeWrite'] == 'Active'
                and observation['GrantId'] == result['ExpectedGrantId']
                and observation['GrantRevision'] == result['ExpectedGrantRevision'], 'Wrong boundary or grant identity.')
        if expected == 'PASS':
            require(observation['TemporaryHp'] == 0 and observation['GrantEnd'] == 'Expired'
                    and observation['GrantEndedAt'] == result['ExpectedDeadline'] and result['AssertionFailure'] is None,
                    'Original ordering assertion did not establish expiry before completion.')
        else:
            require(observation['TemporaryHp'] == 3 and observation['GrantEnd'] == 'None'
                    and observation['GrantEndedAt'] is None
                    and result['AssertionFailure'].startswith('ORDER_BEFORE_COMPLETION:'),
                    'The deliberate reverse did not fail the ordering assertion itself.')
        manifest = read(folder / 'source-hashes.json')
        patches = []
        changed = {}
        for name, binding in manifest.items():
            original = archive.read(name) if name in archive.namelist() else None
            payload = (folder / 'source' / name).read_bytes()
            require(binding['originalSha256'] == (sha(original) if original is not None else None)
                    and binding['observedSha256'] == sha(payload), f'Ordering source binding differs: {name}')
            if original != payload:
                changed[name] = (original or b'', payload)
                retain(folder / 'source' / name, f'ordering/{variant}/changed-source/{name}')
        # The generator inserts the expiry patch first, then the rest patch and new probe.
        ordered_changes = sorted(changed, key=lambda name: (
            0 if name.endswith('/OrdinaryInventory.cs') else 1 if name.endswith('/SharedShortRest.cs') else 2))
        for name in ordered_changes:
            before, after = changed[name]
            patches.extend(difflib.unified_diff(before.decode('utf-8-sig').splitlines(keepends=True),
                after.decode('utf-8-sig').splitlines(keepends=True), fromfile='a/' + name, tofile='b/' + name))
        require(''.join(patches).encode('utf-8') == (folder / 'instrumentation.patch').read_bytes(),
                'Retained instrumentation patch differs from exact source changes.')
        reports = list((folder / 'build').glob('compile-*/results.json'))
        require(len(reports) == 1, 'Expected one isolated compilation.')
        report = read(reports[0])
        require(report['status'] == 'PASS', 'Instrumented source did not compile.')
        for entry in report['sourceHashes']:
            name = 'engine/' + entry['path'].replace('\\', '/')
            require(entry['sha256'].lower() == manifest[name]['observedSha256'], 'Compiled instrumentation source differs.')
        retain(reports[0], f'ordering/{variant}/compile.json')
        for name, binding in result['Assemblies'].items():
            dll = f'Decennium.Foundation.{name}.dll'
            file = reports[0].parent / dll
            require(sha(file.read_bytes()) == binding['sha256'] and bool(binding['moduleId']), 'Instrumented assembly differs.')
            retain(file, f'ordering/{variant}/assemblies/{dll}')
        for name in ('source-hashes.json', 'instrumentation.patch', 'compile.log', 'observation.log', 'results.json'):
            retain(folder / name, f'ordering/{variant}/{name}')

    direct = read(args.requests / 'results.json')
    require(direct['Status'] == 'PASS', 'Typed request verification did not pass.')
    real = read(packet / 'regression/shardA.started.json')['assemblies']
    for name, binding in direct['Assemblies'].items():
        require(real[f'Decennium.Foundation.{name}.dll'] == binding,
                'Typed request verifier must use the unchanged full-regression assemblies.')
    total_requests = total_noncommitted = total_checkpoints = 0
    for branch, result in direct['Branches'].items():
        source = packet / 'public' / branch / 'Restored'
        folder = args.requests / branch
        require(result['InputSha256'] == sha((source / 'inputs.jsonl').read_bytes())
                and result['ReferenceResponsesSha256'] == sha((source / 'responses.jsonl').read_bytes())
                and result['RequestsSha256'] == sha((folder / 'requests.json').read_bytes()),
                'Typed verification transcript binding differs.')
        requests = read(folder / 'requests.json')
        expected = [json.loads(line) for line in (source / 'responses.jsonl').read_text(encoding='utf-8-sig').splitlines()]
        require(len(requests) == len(expected) == result['Inputs'], 'Incomplete typed request stream.')
        total_requests += len(requests)
        for index, row in enumerate(requests):
            require(row['Input'] == index, 'Typed request order differs.')
            if row['Response'] not in ('Saved', 'Restored', 'ViewMatched', 'ConsoleParsingOnly'):
                require(row['Response'] == expected[index]['Response'], 'Typed response differs from console.')
            if 'UnchangedSha256' in row:
                total_noncommitted += 1
                for field in ('BeforeSnapshot', 'AfterSnapshot'):
                    file = folder / row[field]
                    require(sha(file.read_bytes()) == row['UnchangedSha256'], 'Denied/retried request changed complete state.')
                    retain(file, f'direct-requests/{branch}/{file.name}')
        require(result['Unavailable'] >= 5 and result['Duplicates'] >= 1 and result['Conflicts'] >= 1
                and result['ConsoleParsingOnly'] == 2, 'Missing typed denial or retry controls.')
        for name, digest in result['DirectCheckpoints'].items():
            require(sha((folder / name).read_bytes()) == digest == sha((source / name).read_bytes()),
                    'Typed checkpoint differs from console.')
            retain(folder / name, f'direct-requests/{branch}/{name}')
            total_checkpoints += 1
        retain(folder / 'requests.json', f'direct-requests/{branch}/requests.json')
    require(total_checkpoints == 75, 'Missing public checkpoints.')
    retain(args.requests / 'results.json', 'direct-requests/results.json')
    replacement = read(args.replacement / 'results.json')
    require(replacement['Status'] == 'PASS' and replacement['Writes'] == 32 and replacement['Replacements'] == 31
            and replacement['CoreSha256'] == real['Decennium.Foundation.Core.dll']['sha256']
            and replacement['PersistenceSha256'] == real['Decennium.Foundation.Persistence.dll']['sha256'],
            'Repeated-destination diagnostic differs from reviewed assemblies.')
    require(replacement['Inputs'] == [pending_sha, sha((packet / 'focused/short-rest-completed.ddsave').read_bytes())],
            'Repeated-destination diagnostic input differs.')
    prior = None
    for index, observation in enumerate(replacement['Observations']):
        require(observation['Iteration'] == index and observation['PrimarySha256'] == replacement['Inputs'][index % 2]
                and observation['BackupSha256'] == prior, 'Repeated-destination diagnostic lost a complete primary or backup.')
        prior = observation['PrimarySha256']
    require(sha((args.replacement / 'repeated.ddsave').read_bytes()) == prior
            and sha((args.replacement / 'repeated.ddsave.bak').read_bytes()) == replacement['Observations'][-1]['BackupSha256'],
            'Repeated-destination final bytes differ.')
    for name in ('results.json', 'repeated.ddsave', 'repeated.ddsave.bak'):
        retain(args.replacement / name, f'development/replacement-probe/{name}')
    bindings = dict(status='PASS', implementationCommit=args.implementation, sourceArchiveSha256=sha(raw),
        review='644f055d-ece6-5e4f-b9cd-68cafdffdc45', designApproval='89079b81-6322-52eb-ae4a-44670a5a1f97',
        ordering=dict(original='PASS', reversed='EXPECTED_FAIL', instrumentedCopiesOnly=True),
        directRequests=dict(inputs=total_requests, noncommittedCompleteSnapshotComparisons=total_noncommitted,
                            checkpointComparisons=total_checkpoints, assemblies=direct['Assemblies']),
        repeatedSaveDiagnostic=dict(writes=32, replacements=31, originalIoFailureCause='Not established'),
        artifacts=dict(sorted(artifacts.items())))
    (packet / 'REVIEW_CLOSURE_BINDINGS.json').write_text(json.dumps(bindings, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in bindings.items() if key != 'artifacts'}))


if __name__ == '__main__':
    main()
