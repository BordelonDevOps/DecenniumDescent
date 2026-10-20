"""Verify and preserve the proposed Ready successor without executing downloaded code."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from copy import deepcopy
import ast
import hashlib
import io
import json
import stat
import zipfile

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
SOURCE = Path(r'C:\Users\cbord\Downloads\DD_Part5_Copy_Ready_Preparation_Only_Successor_01.zip')
ARCHIVE = A / SOURCE.name
ROOT = A / 'copy-ready-preparation-only-part5-successor-01'
RECEIPT = A / 'COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def binding(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(raw), 'sha256': digest(raw)}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def main():
    assert not any(p.exists() for p in [ARCHIVE, ROOT, RECEIPT])
    checks = []

    def ck(label, ok):
        checks.append({'check': label, 'passed': bool(ok)})
        assert ok, label

    def matches(raw, entry):
        return len(raw) == entry['bytes'] and digest(raw) == entry['sha256']

    def parent(document, pointer):
        parts = [s.replace('~1', '/').replace('~0', '~') for s in pointer.split('/')[1:]]
        current = document
        for part in parts[:-1]:
            current = current[int(part)] if isinstance(current, list) else current[part]
        return current, int(parts[-1]) if isinstance(current, list) else parts[-1]

    def operation(document, op, reverse=False):
        source, dest = ('after', 'before') if reverse else ('before', 'after')
        obj, key = parent(document, op['jsonPointer'])
        exists = 0 <= key < len(obj) if isinstance(obj, list) else key in obj
        label = op['artifactKey'] + op['jsonPointer'] + (' reverse' if reverse else ' forward')
        ck('Exact full operation input ' + label, exists == op[source + 'Exists']
           and (not exists or obj[key] == op[source]))
        order = op.get('parentKeyOrder' + source.title())
        if order is not None:
            ck('Input key order ' + label, isinstance(obj, dict) and list(obj) == order)
        if op[dest + 'Exists']:
            obj[key] = deepcopy(op[dest])
        else:
            del obj[key]
        order = op.get('parentKeyOrder' + dest.title())
        if order is not None:
            ck('Output key set ' + label, isinstance(obj, dict) and set(obj) == set(order))
            ordered = {k: obj[k] for k in order}
            obj.clear()
            obj.update(ordered)

    raw = SOURCE.read_bytes()
    ck('Exact GPT archive', len(raw) == 39831317 and digest(raw) ==
       '41d19bad1b9b2b33b423fd989ddedd919d6a8c9647ec43c43214ddff63ce24d8')
    prior_paths = {'corr': A / 'DD_Part5_Control_Ready_Corrections_01.zip',
        'control': A / 'DD_Control_15_Full_Conference_Part5_Return_02.zip',
        'copy': A / 'DD_Part5_Copied_Feat_Integration_Review_01.zip',
        'supplement02': A / 'DD_Part5_Copied_Feat_Integration_Supplement_02.zip'}
    prior_bytes = {key: p.read_bytes() for key, p in prior_paths.items()}
    prior = {key: zipfile.ZipFile(io.BytesIO(data)) for key, data in prior_bytes.items()}
    cp = json.loads((A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_DEFENSE_FORM_50.json').read_bytes())
    protected_records = [cp['currentAuthoredIndex'], cp['currentAcceptedInterfaceRegistry'],
        cp['currentWorkQueue'], *cp['canonicalHelperBaselinesUnchanged']]
    protected = {G / e['path']: (G / e['path']).read_bytes() for e in protected_records}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names = z.namelist()
        ck('CRC and sixty unique safe members', z.testzip() is None and len(names) == len(set(names)) == 60
           and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts
               and '\\' not in n and ':' not in n and not n.endswith('/')
               and not stat.S_ISLNK(z.getinfo(n).external_attr >> 16) for n in names))
        def read(name):
            return json.loads(z.read(name))
        manifest = read('MANIFEST.json')
        ck('Complete manifest', manifest['fileCount'] == len(manifest['files']) == 59
           and {f['path'] for f in manifest['files']} == set(names) - {'MANIFEST.json'})
        for entry in manifest['files']:
            ck('Manifest ' + entry['path'], matches(z.read(entry['path']), entry))
        ck('Complete Supplement02 exact local archive',
           z.read('history/' + prior_paths['supplement02'].name) == prior_bytes['supplement02'])
        bindings = read('ARTIFACT_BINDINGS.json')['files']
        operations = read('POINTER_OPERATIONS_FROM_PROPOSALS.json')['operations']
        alternative = read('ALTERNATIVE_RULE_OPERATIONS_FROM_ORIGINAL.json')
        ck('Exact operation scope', len(bindings) == 9 and len(operations) == 30
           and len({o['artifactKey'] for o in operations}) == 8
           and len(alternative['operations']) == 26 and len(alternative['files']) == 4)
        for entry in bindings:
            before, after = z.read(entry['baselineFile']), z.read(entry['successorFile'])
            ck('Complete baseline binding ' + entry['key'], matches(before, entry['baseline']))
            ck('Complete successor binding ' + entry['key'], matches(after, entry['successor']))
            source_archive, member = entry['sourceArchiveMember'].split('/', 1)
            ck('Actual preserved input ' + entry['key'], before == prior[source_archive].read(member))
            if entry['kind'] == 'text':
                ops = read('TEXT_OPERATIONS_FROM_PRIOR_HANDOFF.json')['operations']
                ck('Complete text replacement', len(ops) == 1 and ops[0]['artifactKey'] == entry['key']
                   and ops[0]['before'].encode() == before and ops[0]['after'].encode() == after)
                ck('Current handoff matches full successor', z.read('CODEX_HANDOFF.md') == after)
                continue
            current = json.loads(before)
            ops = [o for o in operations if o['artifactKey'] == entry['key']]
            ck('Per-artifact operation count ' + entry['key'], len(ops) == entry['operationCount'])
            for op in ops:
                operation(current, op)
            ck('Full forward bytes ' + entry['key'], encoded(current) == after)
            for op in reversed(ops):
                operation(current, op, reverse=True)
            ck('Full inverse bytes ' + entry['key'], encoded(current) == before)
        for entry in alternative['files']:
            before, after = z.read(entry['baselineFile']), z.read(entry['successorFile'])
            repository_path = next(e['proposedRepositoryPath'] for e in bindings if e['key'] == entry['key'])
            ck('Current unapplied original ' + entry['key'], before == (G / repository_path).read_bytes()
               and matches(before, entry['baseline']) and matches(after, entry['successor']))
            protected[G / repository_path] = before
            current = json.loads(before)
            ops = [o for o in alternative['operations'] if o['artifactKey'] == entry['key']]
            for op in ops:
                operation(current, op)
            ck('Alternative forward complete bytes ' + entry['key'], encoded(current) == after)
            for op in reversed(ops):
                operation(current, op, reverse=True)
            ck('Alternative inverse complete bytes ' + entry['key'], encoded(current) == before)
        for ref in read('SOURCE_REFERENCES.json')['sourceCopies']:
            data = z.read(ref['file'])
            archive_label, member = ref['origin'].split('!', 1)
            archive_label = {'corrections01': 'corr'}.get(archive_label, archive_label)
            ck('Full source origin ' + ref['file'], matches(data, ref) and data == prior[archive_label].read(member))
        for name in names:
            if name.endswith('.py') or name.endswith('.py.txt'):
                ast.parse(z.read(name).decode(), filename=name)
                ck('Python syntax only; no execution ' + name, True)
        def paired(key):
            entry = next(e for e in bindings if e['key'] == key)
            return read(entry['baselineFile']), read(entry['successorFile'])
        before, after = paired('control_context')
        ck('All fifteen Control spells and full cases untouched', len(before['spells']) == 15
           and all(before[k] == after[k] for k in before if k not in ['id', 'status', 'fullConferenceReviewPart5_02'])
           and {k:v for k,v in before['fullConferenceReviewPart5_02'].items() if k != 'copiedFeatReadyBoundary'}
           == {k:v for k,v in after['fullConferenceReviewPart5_02'].items() if k != 'copiedFeatReadyBoundary'})
        before, after = paired('feat_candidate')
        ck('335 native feat objects and nonoperative fields preserved', len(before['feats']) == len(after['feats']) == 335
           and all({k:v for k,v in old.items() if k not in ['operationalRules','payloadOperational']}
               == {k:v for k,v in new.items() if k not in ['operationalRules','payloadOperational']}
               for old,new in zip(before['feats'],after['feats'])))
        policy = read('POLICY_SELECTION.json')
        operative = policy['completeOperativeWording']
        mirrors = [o['after'] for o in operations if o['artifactKey'].startswith('feat_')
                   and isinstance(o['after'], str) and operative in o['after']]
        supplements = paired('feat_supplements')[1]
        decision = supplements['groups'][6]['value']['copyProfileContract']['readyAllowanceDecision']
        ck('Twelve full identical policy mirrors', len(mirrors) == 11 and operative in json.dumps(decision,ensure_ascii=False).replace('\\n','\n'))
        ck('Selected policy and no implementation claims', policy['id'] == 'COPY-READY-ALLOWANCE-02'
           and policy['projectApplied'] is False and policy['runtimeImplemented'] is False
           and policy['otherThreeChoicesReopened'] is False)
        cases = read('CASE_DISPOSITIONS.json')['completeCases']
        ck('42 distinct full specification cases', len(cases) == len({c['id'] for c in cases}) == 42)
        assertion_count = 0
        release_steps = 0
        for case in cases:
            selected = case['selected']
            state = selected['initial']
            trace = selected['trace']
            ck('Event coverage ' + case['id'], [t['event'] for t in trace] == case['events'])
            for n, step in enumerate(trace):
                label = case['id'] + ':' + str(n)
                ck('Trace continuity ' + label, step['before'] == state)
                old, new = step['before'], step['after']
                if step['event']['method'] == 'release':
                    release_steps += 1
                    ck('Release never rewrites allowance or payment/history ' + label,
                       all(old[k] == new[k] for k in ['feat_rounds','class_rounds','rp','authorizations','casts','preparations'])
                       and all(old['counts'][k] == new['counts'][k] for k in ['actions','payments','permissions','components','history','counter_windows']))
                    committed = step['result'] in ['release-committed','release-committed-prevented']
                    ck('Real Reaction and one payload accounting ' + label,
                       new['counts']['reactions'] - old['counts']['reactions'] == int(committed)
                       and new['counts']['payloads'] - old['counts']['payloads'] == int(step['result'] == 'release-committed'))
                    if committed:
                        args = step['event']['arguments']
                        hold = old['hold']
                        ck('Live hold and real deadline ' + label, hold is not None
                           and old['reaction_available'] and old['concentration'] is not None
                           and args['now'] < min(hold['ready_expiry'],hold['capture_expiry'])
                           and new['hold'] is None and not new['reaction_available'])
                state = new
            ck('Complete final state and results ' + case['id'], state == selected['state']
               and [t['result'] for t in trace] == selected['results']
               and trace[-1]['result'] == selected['lastResult'])
            for expected in case['expected']:
                current = selected
                for key in expected['path'].split('.'):
                    current = current[int(key)] if isinstance(current,list) else current[key]
                ck('Independent declared expectation ' + case['id'] + ':' + expected['path'], current == expected['value'])
                assertion_count += 1
        ck('160 declared assertions checked as data', assertion_count == 160)
        for path, before in protected.items():
            ck('Canonical/protected file unchanged ' + path.relative_to(G).as_posix(), path.read_bytes() == before)
        for key, path in prior_paths.items():
            ck('Earlier archive unchanged ' + key, path.read_bytes() == prior_bytes[key])
        with ARCHIVE.open('xb') as output:
            output.write(raw)
        ROOT.mkdir()
        for name in names:
            target = ROOT / PurePosixPath(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as output:
                output.write(z.read(name))
    for archive in prior.values():
        archive.close()
    report = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'preserved-locally-verified-proposed-preparation-only-ready-successor',
        'archive': binding(ARCHIVE), 'script': binding(Path(__file__)),
        'nativeEvidence': binding(A / 'GPT_PART5_COPY_READY_PREPARATION_ONLY_01_RETURN_NATIVE.json'),
        'gptAssistantId': 'b8ed94a4-df57-42af-9750-40f992afbbd0',
        'extractedRoot': ROOT.relative_to(G).as_posix(), 'checks': checks,
        'checkCount': len(checks), 'failures': 0,
        'verificationScope': 'Archive and actual local source bindings; complete forward/inverse reconstruction on both alternative paths; unchanged native objects; case-data continuity, declared expectations and release-accounting/deadline invariants. Downloaded code parsed only.',
        'localCaseDataChecks': {'cases':42,'declaredAssertions':assertion_count,'releaseSteps':release_steps},
        'gptReportedOnly': {'structuralChecks':2233,'isolatedPolicyCases':42,'isolatedAssertions':160,'repeatByteIdentical':True},
        'selectedPolicy': 'COPY-READY-ALLOWANCE-02', 'supersededPolicy': 'COPY-READY-ALLOWANCE-01 both-touched-round accounting only',
        'ownerImplementationReservationRetained': True, 'implementationApplied': False,
        'downloadedCodeExecuted': False, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0,
        'retainedLimitations': 'Full Ready, live predicate and action reachability, canonical persistence, positive missing Step/Boon paths, active next-healing consumption and downstream expiry choice/removal remain separate work. No human-play, balance, cosmology, release or whole-game approval.',
        'authoredCountsUnchanged': {'reviewed':525,'pending':323,'standalone':249,'interfaces':173,'acceptedButUnapplied':39}}
    with RECEIPT.open('x',encoding='utf-8',newline='\n') as output:
        json.dump(report,output,ensure_ascii=False,indent=2)
        output.write('\n')
    print(json.dumps({'receipt':binding(RECEIPT),'archive':binding(ARCHIVE),'checks':len(checks),'failures':0}))


if __name__ == '__main__':
    main()
