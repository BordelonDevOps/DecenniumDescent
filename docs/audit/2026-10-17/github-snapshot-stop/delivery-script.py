"""Final saved-work backup, with no further game authoring, at the owner's stop request."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys, zipfile, io

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('previous_delivery_helpers', HERE/'deliver_progress_2026_10_16_video_game.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
G, D, A = h.G, h.D, h.A
BASE = '42e1050bc8c7833a0634e1c90c8a7d9973531342'
W = HERE.parent/'audit_work/github-snapshot-2026-10-17-stop'
REPORT = 'docs/audit/2026-10-17/github-snapshot-stop'
STATUS = 'SNAPSHOT_STATUS_2026-10-17_STOP.md'
lp, git, digest, write_new, jsraw = h.lp, h.git, h.digest, h.write_new, h.jsraw
for module in [h, h.p]:
    module.BASE, module.W, module.REPORT, module.STATUS = BASE, W, REPORT, STATUS
h.p.tree = lambda ref=BASE: h.oldtree(ref)

def preserve_download():
    raw = Path('C:/Users/cbord/Downloads/DD_AC6_Semantic_Current_06_Review.zip').read_bytes()
    assert len(raw) == 6039 and digest(raw) == '26b1bb61248744f1fdd8bec3d728a694cc7a9cadcc6a1f2b91bdd2f86e53be7a'
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert sorted(z.namelist()) == ['REVIEW.json', 'VERDICT.md']
        assert z.testzip() is None
        review = json.loads(z.read('REVIEW.json'))
        assert digest(z.read('REVIEW.json')) == 'c8cbec68eda9398a68b8dd151b174efeafe68f4dc9a0194e6b754e0ce5a2b163'
        assert digest(z.read('VERDICT.md')) == '67f7d6c5ab3d21211a066c30eff15fb23fbaf43cb9e6d5f60d1936b56b297c52'
    write_new(G/A/'DD_AC6_Semantic_Current_06_Review.zip', raw)
    return review

def scan():
    # Retain prior backup screening boundaries and all tracked history.
    h.scan()
    path = W/'plan.json'
    plan = json.loads(path.read_bytes())
    plan['ownerInstruction'] = 'push them. I dont want github interferring with this. stop after the push please.'
    plan['scope'] = 'Final backup of saved work at owner stop request; no further development or rule adoption.'
    path.write_bytes(jsraw(plan))

def assemble():
    plan = json.loads((W/'plan.json').read_bytes())
    assert not plan['credentialPatternAlerts']
    assert git('status', '--porcelain=v1', '-z') == b''
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    expected, paths = {}, []
    for row in plan['included']:
        expected[row['path']] = row['gitBlob']
        if row['changedFromBaseline']:
            raw = lp(G/row['path']).read_bytes()
            assert digest(raw) == row['sha256'], row['path']
            dst = lp(D/row['path'])
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(raw)
            assert digest(dst.read_bytes()) == row['sha256']
            paths.append(row['path'])
    index = h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts'] == {'reviewed': 451, 'pending': 397}
    assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product'] == 'video-game-only'
    notice = f'> **Latest backup — 17 October 2026:** Saved work is backed up and development is stopped at the owner\'s request. The video-game-only direction remains active. **451 ordinary spells reviewed / 397 pending.** AC6 and DE4 have not been newly adopted. See [snapshot status]({STATUS}). Earlier status below is preserved history.\n\n'
    overlays = []
    for name in ['README.md', 'START_HERE.md']:
        raw = lp(G/name).read_bytes()
        preserved = f'{REPORT}/source-before/{name}'
        write_new(D/preserved, raw)
        delivered = notice.encode() + raw
        lp(D/name).write_bytes(delivered)
        overlays.append({'path': name, 'sourceSha256': digest(raw), 'deliveredSha256': digest(delivered), 'preservedSource': preserved})
        paths.extend([name, preserved])
    status = f'''# Decennium Descent saved-work backup — 17 October 2026

Development is stopped at the owner's explicit request after this push. The completed video-game-only direction integration was already backed up in `{BASE}`. This final snapshot also preserves the subsequent saved review files, without continuing game development.

Ordinary spell accounting remains **451 reviewed / 397 pending**. The recovered AC6 Current06 review archive is preserved exactly as downloaded. Its 6,039-byte archive and two member hashes were checked for preservation; the eight accepted input bindings still require verification before any local adoption. No AC6 promotion or count change is claimed.

The DE4 Current04 fixture proposal and its check report remain drafts. A source-reference correction is still pending: the new Wizard school/protected-dissonance evidence should refer to engine entries 9 and 11, not entry 7; the N24 Abjuration-specialization evidence should include entry 9. The stop request takes precedence over making those further development changes. The Fate guard amendment remains unadopted.

The [video-game direction](DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md), [verbatim directive](DescentReviewChanges/ReviewBible/docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md), and [prior active checkpoint]({A}/ACTIVE_AUTHORING_CHECKPOINT_VIDEO_GAME_ONLY_01.json) remain available. This snapshot status records the later saved drafts and the stop instruction; historical receipts remain unchanged.

The [manifest]({REPORT}/manifest.json) records hashes and exclusions. Source material and existing tracked history are preserved without deletion or force-push. Established backup exclusions remain local, including unrelated browser/sidebar captures, private configuration, third-party reference books, imported assets, dependencies and generated folders. GitHub is a backup destination; this operation does not import remote changes into the authoring folder.

This push verifies backup integrity only. It does not claim new rules acceptance, runtime tests, human playtesting, balance, full cosmology approval, whole-game completion or release approval.
'''
    checkpoint = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'ownerInstruction': plan['ownerInstruction'], 'status': 'Stop development after verified push', 'videoGameOnly': True, 'authoredSpellCounts': index['authoredCounts'], 'newRuleAdoptions': 0, 'ac6Adopted': False, 'de4Adopted': False, 'sourceInformationDeleted': 0, 'historyRewritten': False, 'wholeGameAcceptanceClaimed': False}
    manifest = dict(plan, assembledAtUtc=datetime.now(timezone.utc).isoformat(), deliveryOverlays=overlays, allSelectedSourcesHashedAtScan=True, changedSourcesReverifiedAtAssembly=True)
    extras = {STATUS: status.encode(), f'{REPORT}/DELIVERY_CHECKPOINT.json': jsraw(checkpoint), f'{REPORT}/manifest.json': jsraw(manifest), f'{REPORT}/delivery-script.py': Path(__file__).read_bytes()}
    for name, raw in extras.items():
        write_new(D/name, raw)
        paths.append(name)
    for name in set(paths):
        expected[name] = h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json', jsraw(expected))
    write_new(W/'stage-paths.nul', b'\0'.join(n.encode() for n in sorted(set(paths))) + b'\0')
    print(json.dumps({'sourceFilesHashedAtScan': len(plan['included']), 'changedSourcesReverifiedAtAssembly': sum(x['changedFromBaseline'] for x in plan['included']), 'pathsToStage': len(set(paths)), 'newRuleAdoptions': 0}))

if __name__ == '__main__':
    {'preserve-download': preserve_download, 'scan': scan, 'assemble': assemble, 'verify': h.p.verify}[sys.argv[1]]()
