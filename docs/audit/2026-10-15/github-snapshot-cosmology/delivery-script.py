"""Preserve the owner's newly requested backup after the scoped cosmology reviews."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib, importlib.util, json, subprocess, sys, zipfile

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('delivery_policy', HERE/'deliver_progress_2026_10_14.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)  # Helpers only; no previous delivery is rerun.
G, D = policy.G, policy.D
W = HERE.parent/'audit_work/github-snapshot-2026-10-15-cosmology'
REPORT = 'docs/audit/2026-10-15/github-snapshot-cosmology'
A = 'docs/audit/2026-10-08/full-game'
BASE = '80944e024b1dba5b1f31707b4dd951d53d9f74c8'
STATUS = 'SNAPSHOT_STATUS_2026-10-15_COSMOLOGY.md'
lp, git, digest, write_new, jsraw = policy.lp, policy.git, policy.digest, policy.write_new, policy.jsraw

def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def tree(ref=BASE):
    result = {}
    for row in git('ls-tree', '-r', '-z', ref).split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            result[name.decode()] = {'mode': mode, 'oid': oid}
    return result

def binding(name):
    raw = lp(G/name).read_bytes()
    return {'path': name, 'bytes': len(raw), 'sha256': digest(raw)}

def read(name):
    return json.loads(lp(G/name).read_bytes())

def scan():
    assert git('status', '--porcelain=v1', '-z') == b''
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == BASE
    assert not W.exists(), 'Preserve prior delivery evidence.'
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
                        if not item.is_dir() and Path(item.filename).suffix.lower() in policy.TEXT and any(rx.search(z.read(item)) for rx in policy.SECRET):
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
    plan = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'ownerInstruction': 'Push what we have done to github.', 'scope': 'Saved development backup after two scoped cosmology reviews; no whole-game acceptance claimed.', 'sourceRoot': str(G), 'deliveryRoot': str(D), 'baseCommit': BASE, 'included': included, 'excluded': excluded, 'excludedTreesPreservedLocally': ['Descent assets', *policy.SKIP], 'credentialPatternAlerts': alerts, 'sourceInformationDeleted': 0}
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
    index = read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts'] == {'reviewed': 419, 'pending': 429}
    origin = read(f'{A}/COSMOLOGY_CREATION_ORIGIN_01_APPLICATION_CHECK.json')
    assert origin['exactSummariesVerified'] == 4 and origin['originalSourceHashesUnchanged'] == 34
    assert origin['fullCosmologyApproved'] is False and origin['sourceInformationDeleted'] == 0
    for key in ['authority', 'candidate', 'manuscript']:
        assert binding(origin[key]['path']) == origin[key], key
    authoring = read(f'{A}/ACTIVE_AUTHORING_CHECKPOINT_AFTER_CREATION_ORIGIN_REVIEW.json')
    assert authoring['activeGptReview'] is None
    assert authoring['wholeGameFlowConfirmed'] is False
    for change in read(f'{A}/CREATION_ORIGIN_COMPLETION_NAVIGATION_DELTA.json')['changes']:
        assert binding(change['after']['path']) == change['after']
        assert binding(change['before']['preservedCopy'])['sha256'] == change['before']['sha256']
    evidence = ['ACTIVE_AUTHORING_CHECKPOINT_AFTER_CREATION_ORIGIN_REVIEW.json', 'COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DECISION.json', 'COSMOLOGY_CREATION_ORIGIN_01_RECEIVED_DECISION.json', 'COSMOLOGY_CREATION_ORIGIN_01_APPLICATION_CHECK.json', 'COSMOLOGY_PUBLICATION_SOURCE_CHECK_01.json', 'COPY_SOURCE_COSMOLOGY_NAVIGATION_DELTA.json', 'CREATION_ORIGIN_COMPLETION_NAVIGATION_DELTA.json', 'FEAT335_COPY_RELEASE_SOURCE_01_APPLICATION_CHECK.json']
    checkpoint = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'scope': 'Saved-file delivery checkpoint; prior immutable review receipts remain unchanged.', 'authoredSpellCounts': index['authoredCounts'], 'cosmology': {'completedScopedReviews': ['COSMOLOGY-SOURCE-AUTHORITY-01', 'COSMOLOGY-CREATION-ORIGIN-01'], 'creationOriginSummariesVerified': 4, 'originalSourceHashesUnchanged': 34, 'openOriginDependencies': 11, 'publicationSourceCheck': 'Eight recorded patch anchors verified in current player book and both living extracts; not a full public-boundary certification.', 'originalCosmologyDocumentsModified': False, 'fullCosmologyApproved': False, 'nextDomain': 'gods and pantheons'}, 'copyRelease': {'sourceAndPreservationChecksPreviouslyRecorded': 1022, 'behavioralExamplesExecuted': 0, 'behavioralExamplesStillRequired': 13}, 'navigation': 'Reconciled through creation/origin review, with prior navigation preserved.', 'pendingNotebookRequest': None, 'wholeGameAcceptanceClaimed': False, 'sourceInformationDeleted': 0, 'weeklyUsageUsedPercentAtPreflight': 18, 'ownerStopAtUsedPercent': 50, 'evidence': [binding(f'{A}/{n}') for n in evidence]}
    notice = f'> **Latest progress backup — 15 October 2026:** See [the current snapshot status]({STATUS}). The source/authority and creation/origin cosmology reviews are recorded, with original documents preserved. **419 spells reviewed / 429 pending.** Full cosmology and whole-game review remain open. Earlier status statements below are retained history.\n\n'
    overlays = []
    for n in ['README.md', 'START_HERE.md']:
        original = lp(G/n).read_bytes()
        preserved = f'{REPORT}/source-before/{n}'
        write_new(D/preserved, original)
        delivered = notice.encode()+original
        lp(D/n).write_bytes(delivered)
        overlays.append({'path': n, 'sourceSha256': digest(original), 'deliveredSha256': digest(delivered), 'preservedSource': preserved, 'change': 'Current snapshot notice prepended; source content retained byte-for-byte.'})
        paths += [n, preserved]
    status = f'''# Decennium Descent progress backup — 15 October 2026, cosmology reviews

This backup fulfills the owner's latest request to push the saved work to GitHub. It continues from `{BASE}`. The game remains in development.

- The actual GPT source/authority and creation/origin reviews, submissions, returned evidence, source preservation copies and decision records are included.
- The [creation and origins companion](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CREATION_ORIGINS_REVIEWED_01.md) contains four verified reviewed summaries, seven fact/belief/revelation rows, nine issue dispositions and eleven explicitly unresolved dependencies. It is a scoped Director/reviewer document. Original cosmology documents remain unchanged; full cosmology approval is open.
- The publication-source check confirms eight recorded patch anchors in the current player book and both living text extracts. It does not certify the full public/Director boundary.
- Navigation and the authoring checkpoint now incorporate these scoped reviews and the copy-release source rulings.
- Ordinary spells remain **419 reviewed and 429 pending**. Copy-release source changes have 1,022 recorded source/preservation checks; the thirteen behavioral acceptance examples remain unexecuted.
- Base, Arch and Hero manuscripts, Paladin oaths and oathbreaks, crafting and other saved work retain their existing scoped statuses.

Continue from the [latest authoring checkpoint]({A}/ACTIVE_AUTHORING_CHECKPOINT_AFTER_CREATION_ORIGIN_REVIEW.json). Gods and pantheons are the next cosmology domain. Remaining spells and feats, other authored reviews, final joint whole-game flow, runtime work, human playtesting and balance approval remain open.

The [delivery checkpoint]({REPORT}/DELIVERY_CHECKPOINT.json), [manifest]({REPORT}/manifest.json) and [staged verification]({REPORT}/STAGED_VERIFICATION.json) document this backup. No source information or tracked Git entry was deleted. Historical receipts and successful one-use outputs were preserved. Raw browser captures, private configuration, third-party reference books, dependencies and generated work directories remain local under the existing delivery policy. The repository contains Director material and is a development backup.

Weekly Codex usage was 18% at preflight; the owner's 50% stop limit remains in effect. This push does not declare the game or cosmology complete.
'''
    extras = {STATUS: status.encode(), f'{REPORT}/DELIVERY_CHECKPOINT.json': jsraw(checkpoint), f'{REPORT}/delivery-script.py': Path(__file__).read_bytes()}
    manifest = dict(plan)
    manifest.update({'assembledAtUtc': datetime.now(timezone.utc).isoformat(), 'deliveryOverlays': overlays, 'previousDeliveryPolicy': 'docs/audit/2026-10-14/github-snapshot/delivery-script.py', 'allSelectedSourcesReverified': True, 'wholeGameAcceptanceClaimed': False, 'originalCosmologyDocumentsModified': False})
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
