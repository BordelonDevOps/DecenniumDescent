"""Observe the actual completion boundary in isolated archived sources; reject reversed event order."""
import argparse
import difflib
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

PROBE = '''#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System.Linq;
namespace Decennium.Foundation.Laboratory
{
    // Evidence instrumentation only; never copied into the engine branch.
    public static class ShortRestOrderProbe
    {
        public static bool DeferExpiry { get; } = DEFER;
        public static int Count { get; private set; }
        public static Observation Last { get; private set; }
        public static void Observe(Snapshot state, ShortRestRecord rest)
        {
            Count++;
            Last = new Observation(state, rest);
        }
        public sealed class Observation
        {
            public string Clock { get; }
            public string RestBeforeWrite { get; }
            public long TemporaryHp { get; }
            public string GrantId { get; }
            public long GrantRevision { get; }
            public string GrantEnd { get; }
            public string GrantEndedAt { get; }
            internal Observation(Snapshot state, ShortRestRecord rest)
            {
                Clock = state.RuleClock.ToString();
                RestBeforeWrite = state.ShortRests.Single(x => x.Id == rest.Id).Outcome.ToString();
                TemporaryHp = state.Lives.Single(x => x.ActorId == rest.ActorId).TemporaryHp;
                GrantId = state.ConsumeDecay.CommandId;
                GrantRevision = state.ConsumeDecay.Revision;
                GrantEnd = state.ConsumeDecay.End.ToString();
                GrantEndedAt = state.ConsumeDecay.EndedAt?.ToString();
            }
        }
    }
}
#endif
'''

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--implementation', required=True)
    parser.add_argument('--pending', type=Path, required=True)
    parser.add_argument('--run', type=Path, required=True)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    run = args.run.resolve()
    run.mkdir(parents=True, exist_ok=False)
    raw = subprocess.check_output(['git', 'archive', '--format=zip', args.implementation, 'engine'])
    archive = zipfile.ZipFile(io.BytesIO(raw))
    source_names = [name for name in archive.namelist() if name.endswith('.cs') and any(
        part in name for part in ['/Runtime/Core/', '/Runtime/Persistence/', '/Laboratory/Model/'])]
    compiler = 'engine/tools/Compile-Foundation.ps1'
    rest_path = 'engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs'
    expiry_path = 'engine/com.decennium.foundation/Laboratory/Model/OrdinaryInventory.cs'
    probe_path = 'engine/com.decennium.foundation/Laboratory/Model/ShortRestOrderProbe.cs'
    results = {}
    pwsh = shutil.which('pwsh')
    for variant in ['observed-original', 'reversed-order']:
        folder = run / variant
        source = folder / 'source'
        source.mkdir(parents=True)
        changed = {}
        for name in source_names + [compiler]:
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(name))
        original_rest = archive.read(rest_path).decode('utf-8-sig')
        anchor = '            state.ShortRests = state.ShortRests.Select(x => x.Id == rest.Id ? ended : x).ToArray();'
        assert original_rest.count(anchor) == 1
        observed_rest = original_rest.replace(anchor, '            if (completed) ShortRestOrderProbe.Observe(state, rest);\n' + anchor)
        if variant == 'reversed-order':
            observed_rest = observed_rest.replace(anchor, anchor + '\n' +
                '            if (completed && ShortRestOrderProbe.DeferExpiry && state.ConsumeDecay?.Active == true\n' +
                '                && state.ConsumeDecay.Deadline == state.RuleClock) ExpireConsumeDecay(state, state.ConsumeDecay);')
            original_expiry = archive.read(expiry_path).decode('utf-8-sig')
            expiry_anchor = 'if (scheduledBuffer?.Active == true && scheduledBuffer.Deadline == s.RuleClock)'
            assert original_expiry.count(expiry_anchor) == 1
            changed[expiry_path] = (original_expiry, original_expiry.replace(expiry_anchor,
                'if (scheduledBuffer?.Active == true && scheduledBuffer.Deadline == s.RuleClock && !ShortRestOrderProbe.DeferExpiry)'))
        changed[rest_path] = (original_rest, observed_rest)
        changed[probe_path] = ('', PROBE.replace('DEFER', 'true' if variant == 'reversed-order' else 'false'))
        patches = []
        for name, (before, after) in changed.items():
            (source / name).write_text(after, encoding='utf-8', newline='')
            patches.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                fromfile='a/' + name, tofile='b/' + name))
        (folder / 'instrumentation.patch').write_text(''.join(patches), encoding='utf-8', newline='')
        manifest = {name: {'originalSha256': sha(archive.read(name)) if name in source_names else None,
            'observedSha256': sha((source / name).read_bytes())} for name in source_names + [probe_path]}
        (folder / 'source-hashes.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        compiled = subprocess.run([pwsh, '-NoProfile', '-File', str(source / compiler), '-ResultsRoot', str(folder / 'build')],
            capture_output=True, text=True)
        (folder / 'compile.log').write_text(compiled.stdout + compiled.stderr, encoding='utf-8')
        if compiled.returncode:
            raise RuntimeError(f'{variant} compile failed: {compiled.stdout} {compiled.stderr}')
        reports = list((folder / 'build').glob('compile-*/results.json'))
        assert len(reports) == 1
        report = json.loads(reports[0].read_text(encoding='utf-8-sig'))
        assert report['status'] == 'PASS'
        for entry in report['sourceHashes']:
            name = 'engine/' + entry['path'].replace('\\', '/')
            assert entry['sha256'].lower() == manifest[name]['observedSha256'], name
        command = [pwsh, '-NoProfile', '-File', str(packet / 'Observe-ShortRestOrder.ps1'),
            '-AssemblyRoot', str(reports[0].parent), '-PendingSave', str(args.pending.resolve()), '-Output', str(folder / 'results.json')]
        if variant == 'reversed-order':
            command.append('-ExpectReversed')
        observed = subprocess.run(command, capture_output=True, text=True)
        (folder / 'observation.log').write_text(observed.stdout + observed.stderr, encoding='utf-8')
        if observed.returncode:
            raise RuntimeError(f'{variant} observation failed: {observed.stdout} {observed.stderr}')
        results[variant] = json.loads((folder / 'results.json').read_text(encoding='utf-8-sig'))
    assert results['observed-original']['OrderingAssertion'] == 'PASS'
    assert results['reversed-order']['OrderingAssertion'] == 'EXPECTED_FAIL'
    summary = dict(Status='PASS', Implementation=args.implementation, SourceArchiveSha256=sha(raw),
        PendingSaveSha256=sha(args.pending.read_bytes()), Variants=results,
        Scope='Evidence-only source copies; uninstrumented engine and regression assemblies unchanged')
    (run / 'results.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print('PASS: original-order observation and targeted reversed-order assertion failure')

if __name__ == '__main__':
    main()
