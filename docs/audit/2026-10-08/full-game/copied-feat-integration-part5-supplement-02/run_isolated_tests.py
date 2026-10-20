"""Explicitly execute isolated reference tests in temporary reconstructed trees.

Never points modules at a project checkout; never applies the proposal. Default
verification is in verify_bundle.py, which does not execute reference modules.
This runner requires a NEW output directory outside this evidence bundle.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
from verify_bundle import verify, B


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output.exists() or output.is_relative_to(B) or B.is_relative_to(output):
        raise SystemExit('Output must be a new directory outside the bundle, not its ancestor')
    if not output.parent.is_dir():
        raise SystemExit('Output parent must already exist')
    verification, union, prior = verify()
    output.mkdir()
    runs = []
    def run(name, command):
        result = subprocess.run(command, capture_output=True, text=True, timeout=45)
        with (output / (name + '.log')).open('x', encoding='utf8') as out:
            out.write(result.stdout + result.stderr)
        runs.append({'id': name, 'exitCode': result.returncode})
        if result.returncode:
            raise RuntimeError(name + ' failed; inspect the retained log')
        return result
    with tempfile.TemporaryDirectory(prefix='dd_copy_followup_') as directory:
        temporary = Path(directory)
        bindings = json.loads((B / 'ARTIFACT_BINDINGS.json').read_bytes())['files']
        trees = {}
        for variant in ['original', 'return01', 'successor']:
            files = dict(union)
            if variant != 'original':
                for entry in bindings:
                    path = entry['path']
                    files[path] = prior.read('proposed/' + path) if variant == 'return01' else (B / 'successor' / path).read_bytes()
            tree = temporary / variant
            for path, data in files.items():
                target = tree / path; target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            trees[variant] = tree
        before = {variant: snapshot(tree) for variant, tree in trees.items()}
        for variant, tree in trees.items():
            result = run('probe_' + variant, [sys.executable, '-B', str(B / 'tests/diagnostic_worker.py'), str(tree)])
            with (output / ('probe_' + variant + '.json')).open('x', encoding='utf8') as out:
                out.write(result.stdout)
            cases = json.loads(result.stdout)['cases']
            for case in cases[:4]:
                expected = (case['error'] is None and case['hp'] == 32) if variant == 'successor' else (case['error'] is not None and case['hp'] == 30 and case['failureAtomic'])
                if not expected:
                    raise RuntimeError('Diagnostic result diverged: ' + case['id'])
            if (cases[-1]['returned'] == cases[-1]['expected']) != (variant == 'successor'):
                raise RuntimeError('Expiry instruction result diverged')
        run('targeted36', [sys.executable, '-B', str(B / 'tests/test_targeted_followup.py'),
            '--source-root', str(trees['successor']), '--report', str(output / 'targeted.json')])
        for filename in ['run_checks.py', 'test_copy_review_regressions.py']:
            (temporary / filename).write_bytes(prior.read('tests/' + filename))
        run('prior47', [sys.executable, '-B', str(temporary / 'test_copy_review_regressions.py'),
            '--source-root', str(trees['successor']), '--report', str(output / 'prior47.json')])
        history_comparisons = []
        for label in ['release', 'payloads', 'classes']:
            filename = 'validate_feat335_copy_' + label + '_01.py'
            report = output / (label + '.json')
            run(label, [sys.executable, '-B', str(temporary / 'run_checks.py'), str(trees['successor']), filename, str(report)])
            current = json.loads(report.read_bytes())
            old = json.loads(prior.read('tests/results/proposed_' + label + '_replay.json'))
            if current['histories'] != old['histories']:
                raise RuntimeError('Full prior history differs: ' + label)
            history_comparisons.append({'suite': label, 'checks': current['checks'],
                'historyCount': len(current['histories']), 'fullHistoryEquality': True})
        if before != {variant: snapshot(tree) for variant, tree in trees.items()}:
            raise RuntimeError('A reconstructed reference source changed during testing')
    result = {'scope': 'Isolated reference helpers with conditional fixtures, not game runtime, Oracle acquisition, condition removal, human testing or balance.',
              'runs': runs, 'targetedTests': 36, 'priorRegressionTests': 47,
              'existingHelperAssertions': 456, 'historyComparisons': history_comparisons,
              'allReconstructedSourceBytesUnchanged': True, 'projectFilesApplied': 0,
              'pathRelocation': 'Existing DI7 locator rebound only in memory by the unchanged prior runner.'}
    with (output / 'RUN_SUMMARY.json').open('x', encoding='utf8') as out:
        json.dump(result, out, indent=2); out.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
