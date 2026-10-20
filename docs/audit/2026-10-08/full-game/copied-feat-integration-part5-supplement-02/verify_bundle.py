"""Read-only byte/source/full-value verification. Never import project modules.

Run from any directory: python verify_bundle.py
--report writes only a NEW report path, never overwrites evidence.
"""
from pathlib import Path, PurePosixPath
import argparse
import ast
import hashlib
import io
import json
import stat
import sys
import zipfile

sys.dont_write_bytecode = True
B = Path(__file__).resolve().parent
PRIOR_NAME = 'DD_Part5_Copied_Feat_Integration_Review_01.zip'
PRIOR_BYTES = 36867306
PRIOR_SHA = '006c3705fa56717b4aa6b4a7fcf08e658e91a1568bbbf2b3cb8a471df42dd064'
PAYLOAD = 'DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py'
PACKAGES = {
 'DD_Feat335_Copy_Release_Integration_01.zip': (1712852, '406770ec3851e2c43b04d1fedbaf084e5cbcf6a04c914ecb06686cdab2ad66ad'),
 'DD_Feat335_Copy_Payloads_01.zip': (2178844, 'c1df09249077b47d2b05f01ec3392a9066d939206dde518a5f609abe7b1b4261'),
 'DD_Feat335_Copy_Classes_01.zip': (2236603, '6d3e0d415576a6481fbe3072af4473ada373cb22e90cefab460c077f77ce1626'),
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def bound(data, binding):
    return len(data) == binding['bytes'] and digest(data) == binding['sha256']

def read(path):
    return json.loads((B / path).read_bytes())

def safe(name):
    path = PurePosixPath(name)
    return (bool(name) and not path.is_absolute() and '..' not in path.parts
            and '\\' not in name and ':' not in name
            and str(path) == name.rstrip('/'))

def open_zip(data):
    archive = zipfile.ZipFile(io.BytesIO(data))
    infos = archive.infolist(); names = [i.filename for i in infos]
    if len(names) != len(set(names)) or any(not safe(i.filename) or stat.S_ISLNK(i.external_attr >> 16)
        or i.flag_bits & 1 for i in infos):
        raise ValueError('Unsafe, encrypted or duplicate archive member')
    if archive.testzip() is not None:
        raise ValueError('Archive CRC failed')
    return archive

def apply_values(files, operations, reverse=False):
    result = dict(files)
    for op in reversed(operations) if reverse else operations:
        if op['kind'] != 'replace-exact-text' or not safe(op['path']):
            raise ValueError('Unsupported operation or unsafe path')
        before, after = (op['after'], op['before']) if reverse else (op['before'], op['after'])
        text = result[op['path']].decode('utf8')
        if not before or text.count(before) != 1:
            raise ValueError('Exact unique before-value missing: ' + op['id'])
        result[op['path']] = text.replace(before, after, 1).encode('utf8')
    return result

def verify(check_manifest=True):
    checks = []
    def need(name, condition):
        checks.append({'id': name, 'passed': bool(condition)})
        if not condition:
            raise ValueError('Verification failed: ' + name)
    raw = (B / 'history' / PRIOR_NAME).read_bytes()
    need('prior-return-exact-archive', len(raw) == PRIOR_BYTES and digest(raw) == PRIOR_SHA)
    prior = open_zip(raw)
    pm = json.loads(prior.read('MANIFEST.json'))
    need('prior-complete-members', len(prior.namelist()) == 52 and len(pm['files']) == 51
         and set(prior.namelist()) == {'MANIFEST.json'} | {e['path'] for e in pm['files']})
    for entry in pm['files']:
        need('prior-binding:' + entry['path'], bound(prior.read(entry['path']), entry))
    union = {}; records = []
    for name, (size, sha) in PACKAGES.items():
        nested_bytes = prior.read('inputs/' + name)
        need('input-archive:' + name, len(nested_bytes) == size and digest(nested_bytes) == sha)
        nested = open_zip(nested_bytes); manifest = json.loads(nested.read('MANIFEST.json'))
        for entry in manifest['sources']:
            data = nested.read('sources/' + entry['path'])
            need('source-binding:' + name + ':' + entry['path'], bound(data, entry))
            if entry['path'] in union:
                need('overlap-identical:' + name + ':' + entry['path'], union[entry['path']] == data)
            union[entry['path']] = data; records.append({'archive': name, **entry})
    need('full-source-member-records', records == read('evidence/SOURCE_MEMBER_RECORDS_UNCHANGED.json'))
    need('source-counts', len(records) == 157 and len(union) == 78)
    need('all38-class-python-members-present', sum(1 for e in records if e['archive'] == 'DD_Feat335_Copy_Classes_01.zip' and e['path'].endswith('.py')) == 38)
    bindings = read('ARTIFACT_BINDINGS.json')['files']
    original = {}; proposal = {}; successor = {}
    for entry in bindings:
        path = entry['path']; original[path] = prior.read('baseline/' + path)
        proposal[path] = prior.read('proposed/' + path)
        successor[path] = (B / 'successor' / path).read_bytes()
        need('original-binding:' + path, bound(original[path], entry['original']) and union[path] == original[path])
        need('prior-proposal-binding:' + path, bound(proposal[path], entry['return01Proposal']))
        need('successor-binding:' + path, bound(successor[path], entry['supplement02Successor']))
        ast.parse(successor[path].decode('utf8'))
        need('unchanged-other-proposals:' + path, path == PAYLOAD or successor[path] == proposal[path])
    need('new-baseline-original', (B / 'baseline_original' / PAYLOAD).read_bytes() == original[PAYLOAD])
    need('new-baseline-prior-proposal', (B / 'baseline_return01' / PAYLOAD).read_bytes() == proposal[PAYLOAD])
    old = json.loads(prior.read('CODE_OPERATIONS.json'))['operations']
    new = read('CODE_OPERATIONS_FROM_RETURN01.json')['operations']
    cumulative = read('CUMULATIVE_CODE_OPERATIONS_FROM_ORIGINAL.json')['operations']
    need('exact-three-new-ops-one-file', len(new) == 3 and {o['path'] for o in new} == {PAYLOAD})
    need('verbatim-prior-eleven-ops', len(old) == 11 and cumulative == old + new)
    need('old-entire-forward-equality', apply_values(original, old) == proposal)
    need('old-entire-reverse-equality', apply_values(proposal, old, True) == original)
    need('new-entire-forward-equality', apply_values(proposal, new) == successor)
    need('new-entire-reverse-equality', apply_values(successor, new, True) == proposal)
    need('cumulative-entire-forward-equality', apply_values(original, cumulative) == successor)
    need('cumulative-entire-reverse-equality', apply_values(successor, cumulative, True) == original)
    for filename in ['CODE_BINDINGS.json', 'CODE_OPERATIONS.json', 'FINDINGS.json', 'RETAINED_LIMITATIONS.json', 'READY_GAP_MATRIX.json']:
        need('prior-evidence-copy:' + filename, (B / 'history' / ('RETURN01_' + filename)).read_bytes() == prior.read(filename))
    for filename in ['healing_playtest_rules.py', 'form_temphp_playtest_rules.py', 'feat335_copy_payload_fixtures.py']:
        path = 'DescentReviewChanges/ReviewBible/tools/' + filename
        need('source-copy:' + filename, (B / 'sources' / path).read_bytes() == union[path])
    corrections = open_zip(prior.read('inputs/DD_Part5_Control_Ready_Corrections_01.zip'))
    healing = 'sources/DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md'
    need('source-healing-chapter-unchanged', (B / healing).read_bytes() == corrections.read(healing))
    targeted = read('evidence/TARGETED_TEST_RESULTS.json')
    regressions = read('evidence/RETURN01_REGRESSIONS_RERUN.json')
    need('targeted-report36', targeted['testsRun'] == len(targeted['results']) == 36 and targeted['failures'] == targeted['errors'] == 0 and all(r['status'] == 'PASS' for r in targeted['results']))
    need('retained-regression-report47', regressions['testsRun'] == len(regressions['results']) == 47 and regressions['failures'] == regressions['errors'] == 0 and all(r['status'] == 'PASS' for r in regressions['results']))
    for label, count, history_count in [('release', 136, 19), ('payloads', 115, 27), ('classes', 205, 22)]:
        now = read('evidence/EXISTING_' + label.upper() + '_REPLAY.json')
        old_report = json.loads(prior.read('tests/results/proposed_' + label + '_replay.json'))
        need('existing-report:' + label, now['checks'] == count and not now['failures'])
        need('all-history-objects:' + label, len(now['histories']) == history_count and now['histories'] == old_report['histories'])
        if label == 'release':
            need('all-ready-histories-unchanged', now['readyLifecycleHistories'] == old_report['readyLifecycleHistories'])
            need('source-acceptance-coverage-unchanged', now['acceptanceCoverage'] == old_report['acceptanceCoverage'])
    for variant in ['ORIGINAL', 'RETURN01', 'SUPPLEMENT02']:
        cases = read('evidence/REPRODUCTION_' + variant + '.json')['cases']
        need('diagnostic-case-count:' + variant, len(cases) == 5)
        for case in cases[:4]:
            need('mend-diagnostic:' + variant + ':' + case['id'],
                 (case['error'] is None and case['hp'] == 32 and case['result']['targets']['target']['nextHealingCandidates'] == [])
                 if variant == 'SUPPLEMENT02' else (case['error'] is not None and case['hp'] == 30 and case['failureAtomic']))
        last = cases[-1]
        need('expiry-diagnostic:' + variant,
             last['secondExpiry'] == [] and last['finalGrantState'] == 'natural-expiry'
             and (last['returned'] == last['expected'] if variant == 'SUPPLEMENT02' else last['returned'] is None))
    need('exact-local-liveness-guards', successor[PAYLOAD].count(b'r.present and not r.suppressed and r.next_healing') == 2
         and b'any(r.next_healing for r in' not in successor[PAYLOAD])
    need('explicit-instruction-forwarding', b'instructions=self.buffers.expire(marker);self.projection()\n        return instructions' in successor[PAYLOAD])
    if check_manifest:
        manifest = read('MANIFEST.json')
        names = {e['path'] for e in manifest['files']}
        actual = {p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file()}
        need('full-supplement-member-set', actual == names | {'MANIFEST.json'} and len(names) == len(manifest['files']))
        for entry in manifest['files']:
            need('supplement-binding:' + entry['path'], safe(entry['path']) and bound((B / entry['path']).read_bytes(), entry))
    report = {'scope': 'Read-only source, structural, full-value forward/reverse, report and preservation verification. No project code imported or gameplay run by this verifier.',
              'checks': len(checks), 'failures': 0, 'results': checks,
              'sourceMemberRecords': len(records), 'uniqueSourcePaths': len(union),
              'return01ArchivePreserved': True, 'supplementManifestChecked': check_manifest}
    return report, union, prior

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    args = parser.parse_args()
    if args.report and (Path(args.report).exists() or Path(args.report).resolve().is_relative_to(B)):
        raise SystemExit('Use a new report path outside the evidence bundle')
    report, _, _ = verify()
    if args.report:
        with Path(args.report).open('x', encoding='utf8') as out:
            json.dump(report, out, indent=2); out.write('\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}, indent=2))
