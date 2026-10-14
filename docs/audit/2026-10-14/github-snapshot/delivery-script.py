"""Preserve and assemble the owner's explicitly requested unfinished-work snapshot."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib, json, os, re, shutil, subprocess, sys, zipfile

G = Path('C:/Github/DecenniumDescent')
D = Path('C:/Users/cbord/Documents/ChatGPT/Decennium Descent/github-delivery')
W = Path('C:/Users/cbord/Documents/ChatGPT/Decennium Descent/audit_work/github-snapshot-2026-10-14')
REPORT = 'docs/audit/2026-10-14/github-snapshot'
SKIP = ['node_modules', '.git', '__pycache__', '.next', 'dist', 'build', '.cache', 'out']
BASE = '57bb6d86e0e06d5e4f1e24a6e39a6a7ddb26a2cc'

def lp(p):
    return Path('\\\\?\\' + str(p.resolve())) if os.name == 'nt' else p

def git(*args, data=None):
    return subprocess.run(['git', '-c', 'core.longpaths=true', '-c', 'core.autocrlf=false', *args], cwd=D, input=data, capture_output=True, check=True).stdout

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def write_new(p, raw):
    p = lp(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(raw)

def jsraw(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def reason(name):
    p = Path(name)
    low = name.lower()
    if any(x.lower().startswith('.env') for x in p.parts) or p.suffix.lower() in ['.pem', '.key', '.pfx', '.p12'] or p.name.lower() in ['.npmrc', 'credentials.json', 'id_rsa', 'id_ed25519']:
        return 'private configuration; preserved locally'
    if p.suffix.lower() in ['.tsbuildinfo', '.pyc', '.pyo'] or p.name == 'next-env.d.ts':
        return 'generated compiler artifact; preserved locally'
    if p.suffix.lower() == '.pdf' and ('d&d 5e' in low or 'pathfinder-2e-gamemastery' in low):
        return 'third-party reference book; preserved locally'
    if p.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp', '.gif'] and (re.search(r'browser|screenshot|gpt[-_]|[-_]gpt[-_]', low) or ('docs/audit/' in low and len(p.parts) <= 6 and not 'character-sheet' in low)):
        return 'browser capture may contain unrelated sidebar information; preserved locally'
    if p.suffix.lower() in ['.txt', '.html'] and re.search(r'(?:_dom|browser_dom|dom_snapshot)\.', low):
        return 'raw browser DOM may contain unrelated sidebar information; task review evidence remains separately preserved'
    return None

TOKEN_PATTERNS = [rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', rb'gh[pousr]_[A-Za-z0-9]{30,}', rb'github_pat_[A-Za-z0-9_]{50,}', rb'sk-(?:proj-|svcacct-)[A-Za-z0-9_-]{40,}', rb'AKIA[0-9A-Z]{16}']
SECRET = [re.compile(p) for p in TOKEN_PATTERNS]
TEXT = {'.json', '.md', '.txt', '.js', '.ts', '.tsx', '.jsx', '.mjs', '.cjs', '.py', '.ps1', '.yml', '.yaml', '.toml', '.html', '.xml', '.csv', '.ini', '.cfg', '.sh'}

def scan():
    assert git('status', '--porcelain=v1') == b'', 'Delivery checkout must be clean before assembly.'
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    assert git('rev-parse', 'origin/main').decode().strip() == BASE
    assert not W.exists(), 'Preserve prior delivery evidence.'
    W.mkdir(parents=True)
    args = ['rg', '--files', '--hidden', '--no-ignore', '-g', '!Descent assets/**']
    for n in SKIP:
        args += ['-g', f'!**/{n}/**']
    names = sorted(n.replace('\\', '/') for n in subprocess.run(args, cwd=G, capture_output=True, text=True, encoding='utf-8', check=True).stdout.splitlines())
    included, excluded, alerts = [], [], []
    for i, n in enumerate(names):
        p = lp(G/n)
        assert not p.is_symlink(), n
        before = p.stat()
        raw = p.read_bytes()
        assert (before.st_size, before.st_mtime_ns) == (p.stat().st_size, p.stat().st_mtime_ns), n
        row = {'path': n, 'bytes': len(raw), 'sha256': digest(raw)}
        why = reason(n)
        if not why and p.suffix.lower() == '.zip':
            with zipfile.ZipFile(p) as z:
                blocked = [{'path': x.filename, 'reason': reason(x.filename)} for x in z.infolist() if not x.is_dir() and reason(x.filename)]
            # Generated files within an immutable historical packet are acceptable;
            # private captures/configuration and reference books are not uploaded.
            blocked = [x for x in blocked if not x['reason'].startswith('generated')]
            if blocked:
                why = 'immutable archive contains locally retained material; original archive preserved locally'
                row['retainedMembers'] = blocked
        if not why and p.suffix.lower() in TEXT and any(rx.search(raw) for rx in SECRET):
            alerts.append(n)
            why = 'credential-pattern review required; preserved locally'
        if not why and len(raw) >= 100 * 1024 * 1024:
            why = 'oversized regular Git blob; preserved locally'
        if why:
            row['reason'] = why
            excluded.append(row)
        else:
            included.append(row)
        if i and i % 5000 == 0:
            print(f'Screened {i} files', flush=True)
    plan = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'sourceRoot': str(G), 'deliveryRoot': str(D), 'baseCommit': BASE, 'ownerInstruction': 'Push what we have done to github.', 'scope': 'Progress backup of current authored and review work; not final game acceptance or release.', 'excludedTreesPreservedLocally': ['Descent assets', *SKIP], 'included': included, 'excluded': excluded, 'credentialPatternAlerts': alerts, 'sourceInformationDeleted': 0}
    write_new(W/'plan.json', jsraw(plan))
    print(json.dumps({'includedFiles': len(included), 'includedBytes': sum(x['bytes'] for x in included), 'excludedFiles': len(excluded), 'exclusionReasons': dict(Counter(x['reason'] for x in excluded)), 'credentialPatternAlerts': alerts, 'plan': str(W/'plan.json')}))

def assemble():
    plan = json.loads((W/'plan.json').read_text(encoding='utf-8'))
    assert not plan['credentialPatternAlerts'], 'Review actual credential pattern alerts before assembly.'
    assert git('status', '--porcelain=v1') == b''
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    copied = []
    expected_staged = {}
    for i, row in enumerate(plan['included']):
        p = lp(G/row['path'])
        raw = p.read_bytes()
        assert digest(raw) == row['sha256'], row['path']
        dest = lp(D/row['path'])
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        assert digest(dest.read_bytes()) == row['sha256'], row['path']
        expected_staged[row['path']] = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        copied.append(row['path'])
        if i and i % 5000 == 0:
            print(f'Copied and verified {i} files', flush=True)
    notice = '> **Progress snapshot — 14 October 2026:** The owner requested a backup of the work completed so far. See [SNAPSHOT_STATUS_2026-10-14.md](SNAPSHOT_STATUS_2026-10-14.md) for the current status: **419 spells reviewed, 429 pending**. Development remains paused. Older navigation and review-state statements below are historical and may lag this snapshot. This push does not certify whole-game acceptance.\n\n'
    overlays = []
    for n in ['README.md', 'START_HERE.md']:
        original = lp(D/n).read_bytes()
        preserved = f'{REPORT}/source-before/{n}'
        write_new(D/preserved, original)
        delivered = notice.encode() + original
        lp(D/n).write_bytes(delivered)
        overlays.append({'path': n, 'sourceSha256': digest(original), 'deliveredSha256': digest(delivered), 'preservedSource': preserved, 'change': 'Delivery status notice only; original content appended unchanged.'})
    status = '''# Decennium Descent progress snapshot — 14 October 2026

The owner explicitly requested: “Push what we have done to github.” This authorizes saving the current unfinished work to GitHub now. The earlier final whole-game flow gate remains a requirement for claiming the game complete, rather than a blocker to this requested progress backup.

Development stopped at the owner's 50% weekly usage cutoff. This delivery does not resume game authoring or cosmology review.

- Ordinary spells: **419 authored reviews complete; 429 pending**, across 848 indexed spells. GPT accepted the seven DI7 spells; the exact acceptance is recorded and the index updated.
- The DI7 submission verifier reproduced **1,819 checks with zero failures** locally. The received reviewer evidence retains its separate scope.
- Pact sigils evidence records **140 checks across 45 histories, zero failures**. This is bounded validation, not complete feat or game runtime coverage.
- Base, Arch and Hero class manuscripts, Paladin oaths and oathbreaks, crafting work, other game development, review packets and preservation history are included with their existing status labels.
- The prepared copy-release questions have not been sent. Whole-game joint flow review, further development, human playtesting and balance approval remain pending.
- Cosmology sources are carried as existing bytes. Cosmology has not been reviewed or changed for this snapshot.

The [pause checkpoint](docs/audit/2026-10-08/full-game/PAUSED_AT_50_PERCENT_2026-10-13.json), [spell index](DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json), and [DI7 acceptance receipt](docs/audit/2026-10-08/full-game/DI7_EXACT_ACCEPTANCE_RECEIPT.json) control the latest status. Older START_HERE, review-map and coverage-ledger text still needs reconciliation with DI7 acceptance and the Pact sigils report. Do not rerun or overwrite successful one-use recorders to resolve those historical labels.

## Preservation and delivery

No source information was deleted. This repository is a development backup containing both player and Director materials; it is not a player-only publication. Existing Git history and tracked entries are retained.

The [delivery manifest](docs/audit/2026-10-14/github-snapshot/manifest.json) lists exact source fingerprints and locally retained exceptions. Dependencies, generated build directories, the separate imported-asset workbench, third-party reference books, raw browser captures, and archives containing those private captures remain local. Original archives and documents have not been rewritten to remove their contents. README and START_HERE receive only this snapshot's status notice, with their original source bytes saved alongside the manifest.

Resume with the pause checkpoint. Complete the remaining authored content and final actual GPT whole-game flow review before declaring readiness. The owner has not authorized resuming development beyond this requested push.
'''
    write_new(D/'SNAPSHOT_STATUS_2026-10-14.md', status.encode('utf-8'))
    manifest = dict(plan)
    manifest.update({'assembledAtUtc': datetime.now(timezone.utc).isoformat(), 'allCopiedFilesVerified': True, 'deliveryOverlays': overlays, 'gitHistoryRewritten': False, 'cosmologyReviewed': False, 'navigationReconciled': False, 'authoredSpellCounts': {'reviewed': 419, 'pending': 429}})
    write_new(D/f'{REPORT}/manifest.json', jsraw(manifest))
    write_new(D/f'{REPORT}/delivery-script.py', Path(__file__).read_bytes())
    extra = [f'{REPORT}/source-before/README.md', f'{REPORT}/source-before/START_HERE.md', 'SNAPSHOT_STATUS_2026-10-14.md', f'{REPORT}/manifest.json', f'{REPORT}/delivery-script.py']
    paths = copied + extra
    for n in ['README.md', 'START_HERE.md', *extra]:
        raw = lp(D/n).read_bytes()
        expected_staged[n] = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    write_new(W/'expected-staged-blobs.json', jsraw(expected_staged))
    write_new(W/'stage-paths.nul', b'\0'.join(n.encode('utf-8') for n in paths) + b'\0')
    write_new(W/'assembly.json', jsraw({'pathsToStage': len(paths), 'sourceFilesVerified': len(copied), 'overlays': overlays, 'sourceInformationDeleted': 0}))
    print(json.dumps({'copiedAndVerified': len(copied), 'pathsToStage': len(paths), 'manifest': f'{REPORT}/manifest.json'}))

def verify():
    expected = json.loads((W/'expected-staged-blobs.json').read_text(encoding='utf-8'))
    entries = {}
    for row in git('ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0', 'Unmerged index'
        entries[name.decode('utf-8')] = {'mode': mode, 'oid': oid}
    mismatch = [n for n, oid in expected.items() if entries.get(n, {}).get('oid') != oid]
    assert not mismatch, mismatch
    baseline = {}
    for row in git('ls-tree', '-r', '-z', BASE).split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        baseline[name.decode('utf-8')] = {'mode': mode, 'oid': oid}
    assert all(n in entries for n in baseline), 'Tracked baseline entry deleted'
    retained = [n for n in baseline if n not in expected]
    assert all(entries[n] == baseline[n] for n in retained), 'Unexpected modification to retained baseline entry'
    assert not set(entries) - set(expected) - set(retained), 'Unexpected staged entries'
    idx = json.loads(lp(D/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json').read_bytes())
    assert idx['authoredCounts'] == {'reviewed': 419, 'pending': 429}
    pause = json.loads(lp(D/'docs/audit/2026-10-08/full-game/PAUSED_AT_50_PERCENT_2026-10-13.json').read_bytes())
    for b in pause['bindings']:
        rel = Path(b['path']).relative_to(G)
        assert digest(lp(D/rel).read_bytes()) == b['sha256'], str(rel)
    report = {'verifiedAtUtc': datetime.now(timezone.utc).isoformat(), 'expectedBlobsVerified': len(expected), 'totalIndexEntries': len(entries), 'baselineEntriesRetained': len(baseline), 'baselineEntriesNotOverlaid': retained, 'deletedEntries': 0, 'stagedBlobMismatches': 0, 'pauseEvidenceBindingsVerified': len(pause['bindings']), 'authoredSpellCounts': idx['authoredCounts'], 'validationScope': 'Snapshot integrity and preservation, not game runtime or full authored acceptance.'}
    write_new(W/'staged-verification.json', jsraw(report))
    print(json.dumps(report))

if __name__ == '__main__':
    {'scan': scan, 'assemble': assemble, 'verify': verify}[sys.argv[1]]()
