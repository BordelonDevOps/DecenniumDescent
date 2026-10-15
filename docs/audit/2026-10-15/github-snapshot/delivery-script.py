"""Create a non-destructive progress backup for the owner's October 15 push request."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib, importlib.util, json, os, subprocess, sys, zipfile

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('previous_delivery_policy', HERE/'deliver_progress_2026_10_14.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)  # Reuse screening/helpers; never rerun the completed delivery.
G, D = policy.G, policy.D
W = HERE.parent/'audit_work/github-snapshot-2026-10-15'
REPORT = 'docs/audit/2026-10-15/github-snapshot'
A = 'docs/audit/2026-10-08/full-game'
BASE = 'a3f75a0ce577f51bd39153a872ef05ba9e877642'
lp, git, digest, write_new, jsraw = policy.lp, policy.git, policy.digest, policy.write_new, policy.jsraw

def tree():
    result = {}
    for row in git('ls-tree', '-r', '-z', BASE).split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            result[name.decode()] = {'mode': mode, 'oid': oid}
    return result

def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def binding(name):
    raw = lp(G/name).read_bytes()
    return {'path': name, 'bytes': len(raw), 'sha256': digest(raw)}

def scan():
    assert git('status', '--porcelain=v1', '-z') == b'', 'Delivery checkout has local changes.'
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == BASE
    assert not W.exists(), 'Do not overwrite delivery evidence.'
    baseline = tree()
    args = ['rg', '--files', '--hidden', '--no-ignore', '-g', '!Descent assets/**']
    for part in policy.SKIP:
        args += ['-g', f'!**/{part}/**']
    names = sorted(n.replace('\\', '/') for n in subprocess.run(args, cwd=G, capture_output=True, text=True, encoding='utf-8', check=True).stdout.splitlines())
    included, excluded, alerts = [], [], []
    for n in names:
        p = lp(G/n)
        assert not p.is_symlink(), n
        before = p.stat()
        raw = p.read_bytes()
        assert (before.st_size, before.st_mtime_ns) == (p.stat().st_size, p.stat().st_mtime_ns), n
        row = {'path': n, 'bytes': len(raw), 'sha256': digest(raw), 'gitBlob': blob(raw)}
        why = policy.reason(n)
        changed = baseline.get(n, {}).get('oid') != row['gitBlob']
        if not why and p.suffix.lower() == '.zip':
            with zipfile.ZipFile(p) as z:
                blocked = [{'path': x.filename, 'reason': policy.reason(x.filename)} for x in z.infolist() if not x.is_dir() and policy.reason(x.filename)]
                blocked = [x for x in blocked if not x['reason'].startswith('generated')]
                if blocked:
                    why = 'immutable archive contains locally retained material; original archive preserved locally'
                    row['retainedMembers'] = blocked
                if changed and not why:
                    for item in z.infolist():
                        if not item.is_dir() and Path(item.filename).suffix.lower() in policy.TEXT:
                            if any(rx.search(z.read(item)) for rx in policy.SECRET):
                                alerts.append(n+' :: '+item.filename)
                                why = 'credential-pattern review required; preserved locally'
        if not why and p.suffix.lower() in policy.TEXT and any(rx.search(raw) for rx in policy.SECRET):
            alerts.append(n)
            why = 'credential-pattern review required; preserved locally'
        if not why and len(raw) >= 100*1024*1024:
            why = 'oversized regular Git blob; preserved locally'
        if why:
            row['reason'] = why
            excluded.append(row)
        else:
            row['changedFromBaseline'] = changed
            included.append(row)
    plan = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'ownerInstruction': 'Push what we have done to github.', 'scope': 'Current saved development backup; no whole-game or cosmology approval claimed.', 'sourceRoot': str(G), 'deliveryRoot': str(D), 'baseCommit': BASE, 'included': included, 'excluded': excluded, 'excludedTreesPreservedLocally': ['Descent assets', *policy.SKIP], 'credentialPatternAlerts': alerts, 'sourceInformationDeleted': 0}
    write_new(W/'plan.json', jsraw(plan))
    changes = [x['path'] for x in included if x['changedFromBaseline']]
    write_new(W/'changed-source-paths.json', jsraw(changes))
    print(json.dumps({'includedFiles': len(included), 'includedBytes': sum(x['bytes'] for x in included), 'changedOrNewSourceFiles': len(changes), 'excludedFiles': len(excluded), 'exclusionReasons': dict(Counter(x['reason'] for x in excluded)), 'credentialPatternAlerts': alerts, 'changedSourceList': str(W/'changed-source-paths.json')}))

def assemble():
    plan = json.loads((W/'plan.json').read_bytes())
    assert not plan['credentialPatternAlerts']
    assert git('status', '--porcelain=v1', '-z') == b''
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    expected, paths = {}, []
    for row in plan['included']:
        raw = lp(G/row['path']).read_bytes()
        assert digest(raw) == row['sha256'], row['path']
        expected[row['path']] = row['gitBlob']
        if row['changedFromBaseline']:
            dest = lp(D/row['path'])
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            assert digest(dest.read_bytes()) == row['sha256'], row['path']
            paths.append(row['path'])
    index = json.loads(lp(G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json').read_bytes())
    assert index['authoredCounts'] == {'reviewed': 419, 'pending': 429}
    ops = json.loads(lp(G/f'{A}/FEAT335_COPY_RELEASE_SOURCE_01_DERIVED_OPERATIONS.json').read_bytes())
    for change in ops['changes']:
        assert binding(change['after']['path']) == change['after']
        prior = binding(change['before']['preservedCopy'])
        assert prior['sha256'] == change['before']['sha256']
    check = json.loads(lp(G/f'{A}/FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json').read_bytes())
    assert check['checks'] == 1022 and check['status'] == 'source-application-verified; behavioral-acceptance-pending'
    evidence_names = ['ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI7_ACCEPTANCE_AND_RESUME.json', 'FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json', 'FEAT335_COPY_RELEASE_SOURCE_01_DERIVED_OPERATIONS.json', 'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json', 'COSMOLOGY_SOURCE_AUTHORITY_01_PREPARATION.json', 'COSMOLOGY_SOURCE_AUTHORITY_01_SENT_DOM.txt', 'COSMOLOGY_SOURCE_AUTHORITY_01_SENT.png']
    checkpoint = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'scope': 'Saved-file delivery checkpoint; does not replace prior immutable review receipts.', 'authoredSpellCounts': index['authoredCounts'], 'copyRelease': {'status': 'GPT source addendum received and applied to four derived files', 'sourceAndPreservationChecks': 1022, 'behavioralExamplesExecuted': 0, 'behavioralExamplesStillRequired': 13}, 'cosmology': {'status': 'Source/authority packet sent; no returned verdict captured in this snapshot.', 'sourceFiles': 34, 'payloads': 40, 'findings': 6, 'doctrineChanges': 0, 'approvalClaimed': False}, 'navigation': 'DI7 status reconciled. Copy-source application operations still need addition to review-map binding chain and a new authoring checkpoint; older pending-review statements are historical.', 'nextWork': ['Integrate copy-source derived operations and latest review statuses into navigation.', 'Retrieve and preserve the actual cosmology notebook response before acting on it.', 'Implement and verify the thirteen copy-release acceptance behaviors, then continue remaining authored review.'], 'weeklyUsageUsedPercentAtPreflight': 16, 'ownerStopAtUsedPercent': 50, 'wholeGameAcceptanceClaimed': False, 'sourceInformationDeleted': 0, 'evidence': [binding(f'{A}/{n}') for n in evidence_names]}
    notice = '> **Progress snapshot — 15 October 2026:** See [the current snapshot status](SNAPSHOT_STATUS_2026-10-15.md). **419 spells reviewed / 429 pending.** The copy-release source rulings have been received and applied; behavioral validation remains open. The first cosmology source/authority packet has been sent. Earlier status statements below are retained history and may lag this snapshot. Whole-game acceptance remains open.\n\n'
    overlays = []
    for n in ['README.md', 'START_HERE.md']:
        original = lp(G/n).read_bytes()
        preserved = f'{REPORT}/source-before/{n}'
        write_new(D/preserved, original)
        delivered = notice.encode()+original
        lp(D/n).write_bytes(delivered)
        overlays.append({'path': n, 'sourceSha256': digest(original), 'deliveredSha256': digest(delivered), 'preservedSource': preserved, 'change': 'Current snapshot notice prepended; source content retained byte-for-byte.'})
        paths += [n, preserved]
    status = f'''# Decennium Descent progress snapshot — 15 October 2026

This snapshot fulfills the owner's request to push the saved work to GitHub. It builds on the verified October 14 backup `{BASE}`. The game remains in development.

- **Spells:** 419 reviewed and 429 pending out of 848. The seven DI7 acceptances and the reconciled navigation are included.
- **Copy-release feats:** GPT's source addendum resolves the three submitted rules questions. The four derived source files now include those directions, with 1,022 source/preservation checks recorded. The thirteen behavioral acceptance examples have not yet been executed; this is not full feat or runtime approval.
- **Cosmology:** The first careful source/authority packet was sent after the verified October 14 push. It contains 34 source files, 40 payloads and six evidence-linked findings. No returned cosmology verdict is captured in this snapshot, and no cosmology doctrine was changed or approved.
- **Preserved work:** Base, Arch and Hero class manuscripts, Paladin oaths and oathbreaks, crafting, other game content and earlier review evidence remain present with their scoped statuses.
- **Still open:** Remaining spell and feat work, navigation follow-up for the newest copy-source changes, further authored reviews, final joint whole-game flow, runtime coverage, human playtesting and balance approval.

The [delivery checkpoint]({REPORT}/DELIVERY_CHECKPOINT.json) identifies the current evidence and next work. The [copy-source application receipt]({A}/FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json) and [derived operations]({A}/FEAT335_COPY_RELEASE_SOURCE_01_DERIVED_OPERATIONS.json) control the newest copy-release changes. The latest general authoring checkpoint predates those changes; its older pending-review statements are retained history.

The [manifest]({REPORT}/manifest.json) records all selected source fingerprints and local exceptions. No source information or tracked Git entry was deleted. Historical receipts and packets were not rerun or overwritten. Raw browser captures, private configuration, third-party reference books, dependencies and generated work directories remain preserved locally under the existing delivery policy. This repository includes Director material and is a development backup, not a player-only publication.

Weekly Codex usage was 16% at preflight; the owner's 50% stop limit remains in effect. This delivery makes no claim that development or the cosmology review is complete.
'''
    extras = {'SNAPSHOT_STATUS_2026-10-15.md': status.encode(), f'{REPORT}/DELIVERY_CHECKPOINT.json': jsraw(checkpoint), f'{REPORT}/delivery-script.py': Path(__file__).read_bytes()}
    manifest = dict(plan)
    manifest.update({'assembledAtUtc': datetime.now(timezone.utc).isoformat(), 'deliveryOverlays': overlays, 'previousDeliveryPolicy': 'docs/audit/2026-10-14/github-snapshot/delivery-script.py', 'allSelectedSourcesReverified': True, 'wholeGameAcceptanceClaimed': False, 'cosmologyDoctrineChanged': False})
    extras[f'{REPORT}/manifest.json'] = jsraw(manifest)
    for n, raw in extras.items():
        write_new(D/n, raw)
        paths.append(n)
    for n in set(paths):
        expected[n] = blob(lp(D/n).read_bytes())
    write_new(W/'expected-staged-blobs.json', jsraw(expected))
    write_new(W/'stage-paths.nul', b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesReverified': len(plan['included']), 'pathsToStage': len(set(paths)), 'preservedPriorEntries': len(tree()), 'sourceInformationDeleted': 0}))

def verify():
    expected = json.loads((W/'expected-staged-blobs.json').read_bytes())
    entries = {}
    for row in git('ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            assert stage == '0'
            entries[name.decode()] = {'mode': mode, 'oid': oid}
    assert all(entries.get(n, {}).get('oid') == oid for n, oid in expected.items()), 'Staged blob mismatch'
    baseline = tree()
    assert all(n in entries for n in baseline), 'Tracked entry deleted'
    retained = set(baseline)-set(expected)
    assert all(entries[n] == baseline[n] for n in retained), 'Retained entry changed'
    assert not set(entries)-set(expected)-retained, 'Unexpected staged entry'
    assert git('diff', '--name-only', '--diff-filter=D', '--cached') == b''
    report = {'verifiedAtUtc': datetime.now(timezone.utc).isoformat(), 'expectedBlobsVerified': len(expected), 'totalIndexEntries': len(entries), 'priorTrackedEntriesRetained': len(baseline), 'priorEntriesNotOverlaid': len(retained), 'deletedEntries': 0, 'stagedBlobMismatches': 0, 'validationScope': 'Snapshot integrity and preservation; no additional game behavior tests run.'}
    write_new(W/'staged-verification.json', jsraw(report))
    write_new(D/f'{REPORT}/STAGED_VERIFICATION.json', jsraw(report))
    print(json.dumps(report))

if __name__ == '__main__':
    {'scan': scan, 'assemble': assemble, 'verify': verify}[sys.argv[1]]()
