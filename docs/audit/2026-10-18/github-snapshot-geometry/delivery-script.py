"""Preserve full current review packets without adopting pending spell cohorts."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('geometry_delivery_helpers', HERE / 'deliver_progress_2026_10_16_video_game.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
G, D, A = h.G, h.D, h.A
BASE = '9cfd0ab4029176a5e1075344a908f50a3fb8fdde'
W = HERE.parent / 'audit_work/github-snapshot-2026-10-18-geometry'
REPORT = 'docs/audit/2026-10-18/github-snapshot-geometry'
STATUS = 'SNAPSHOT_STATUS_2026-10-18_GEOMETRY.md'
CHECKPOINT = f'{A}/ACTIVE_AUTHORING_CHECKPOINT_GEOMETRY_LIFE_CONFERENCE_10.json'
lp, git, digest, write_new, jsraw = h.lp, h.git, h.digest, h.write_new, h.jsraw
for module in [h, h.p]:
    module.BASE, module.W, module.REPORT, module.STATUS = BASE, W, REPORT, STATUS
h.p.tree = lambda ref=BASE: h.oldtree(ref)


def scan():
    h.scan()
    path = W / 'plan.json'
    plan = json.loads(path.read_bytes())
    plan.update(ownerInstruction='Preserve progress on GitHub, keep actual GPT involved, and continue until review completion or 20% allowance remains.', scope='Actual persistent20 conference06 return, exact DC25 rebound10 and persistent20 rebound07, corrected control15 conference12 and memory/Creation/terrain conference02, active actual companion/life10 conference01, queue05 and checkpoint10.')
    path.write_bytes(jsraw(plan))


def assemble():
    plan = json.loads((W / 'plan.json').read_bytes())
    assert not plan['credentialPatternAlerts']
    assert git('status', '--porcelain=v1', '-z') == b''
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    expected, paths = {}, []
    for row in plan['included']:
        expected[row['path']] = row['gitBlob']
        if row['changedFromBaseline']:
            raw = lp(G / row['path']).read_bytes()
            assert digest(raw) == row['sha256'], row['path']
            dst = lp(D / row['path'])
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(raw)
            assert digest(dst.read_bytes()) == row['sha256']
            paths.append(row['path'])
    index = h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts'] == {'reviewed': 480, 'pending': 368}
    assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product'] == 'video-game-only'
    bindings = {name: h.p.binding(f'{A}/{name}') for name in [
        'PERSISTENT_DAMAGE_20_CONFERENCE_06_RECEIPT.json',
        'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_PREPARATION.json',
        'DAMAGE_CONTROL_25_EXACT_REBOUND_10_PREPARATION.json',
        'CONTROL_15_CONFERENCE_12_PREPARATION.json',
        'MEMORY_2_CONFERENCE_02_PREPARATION.json',
        'CREATION_CONFERENCE_02_PREPARATION.json',
        'MATERIAL_TERRAIN_8_CONFERENCE_02_PREPARATION.json',
        'COMPANION_LIFE_10_CONFERENCE_01_ACTUAL_SUBMISSION.json',
        'REMAINING_WORK_QUEUE_05_CHECK.json',
        'GEOMETRY_LIFE_CONFERENCE_10_NAVIGATION_CHECK.json',
    ]}
    notice = f'> **Latest development backup — 18 October 2026 UTC:** Video-game development continues with actual GPT. **480 ordinary spells reviewed / 368 pending.** Current source-preserving corrections, complete review packets and active companion/life conference are saved. See [snapshot status]({STATUS}). Earlier backup notices below are preserved history.\n\n'
    overlays = []
    for name in ['README.md', 'START_HERE.md']:
        raw = lp(G / name).read_bytes()
        preserved = f'{REPORT}/source-before/{name}'
        write_new(D / preserved, raw)
        delivered = notice.encode() + raw
        lp(D / name).write_bytes(delivered)
        overlays.append({'path': name, 'sourceSha256': digest(raw), 'deliveredSha256': digest(delivered), 'preservedSource': preserved})
        paths.extend([name, preserved])
    status = f'''# Decennium Descent development backup — 18 October 2026 UTC

Active video-game development continues with the actual GPT notebook. This preservation snapshot records work since `{BASE}`. Ordinary spell accounting remains **480 reviewed / 368 pending** across 848 identities, including 204 complete standalone procedures and 108 accepted interfaces. AC6 and DE4 retain their scoped acceptance. No pending cohort is adopted by this backup.

GPT's actual persistent20 conference06 review archive and final response are preserved. All nine complete before/after operations were applied and independently reversed to the original candidate. Three separate local repairs address the Ranger companion's HP-only lifecycle, a suppressor's occupied space and range, and the Warrior HP source binding. Pending Current07 retains every prior case and adds the two GPT-requested cases: 57 current cases and all 40 original scenarios. Exact rebound07 is prepared with all 20 procedures, complete current casebook, source files, manuscripts and evidence. Its additional local repairs still require actual GPT concurrence.

Damage/Control25 Current09 and exact rebound10 repair occupied-space, swept-body, support and class-HP examples while preserving all 25 procedures, 70 case identities and 36 original scenarios. Exact rebound09 was never submitted and is superseded. Control15 Current12 and conference12 retain all procedures and original scenarios while repairing body geometry, five out-of-range anti-magic placements, duplicate caster occupancy and actual whole-body contacts. Memory2, Creation and material/terrain8 conference02 likewise preserve their complete original proposals and open questions alongside explicit geometry deltas. These packets are prepared, unsubmitted and unaccepted. Illusion14 conference11 is also prepared and awaits review; a zero-match text search is not a semantic geometry validation.

Companion/life10 conference01 is actually submitted to Review Continuation Part4 and was still generating at this snapshot boundary. It contains ten full original procedures, twenty original scenarios, forty-seven full source files and sixteen substantive design questions. It is a preauthorship conference with zero new current case vectors; source gaps and new creature profiles remain explicit proposals. Queue05 records 95 pending spell identities in eight current prepared or active packets, forty other earlier complete proposals, 232 without a complete procedure found and one receipt-only record. Together these retain all 368 pending identities without promoting a review count.

Continue from the [active checkpoint]({CHECKPOINT}), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). Navigation verified 1,316 distinct links with none missing. All 75 domain gates retain their actual statuses and evidence requirements. The checkpoint and each packet preparation record bind exact bytes and SHA-256 hashes.

The [manifest]({REPORT}/manifest.json) records exact selected file hashes and locally retained exclusions. Every prior tracked Git entry is preserved. Existing backup boundaries retain private configuration, unrelated raw browser/sidebar captures, third-party books, imported assets, dependencies, generated folders and archives containing excluded materials locally. Original archives are not rewritten. No source deletion, remote import into the authoring folder or force push is used.

This snapshot verifies preservation and authored files. It does not establish engine implementation, runtime behavior, human gameplay, balance, cosmology/canon, whole-game flow or release approval. Development continues until the review is complete or a reported usage allowance reaches 20% remaining; the latest observed allowance was 71% remaining.
'''
    delivery = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'ownerInstruction': plan['ownerInstruction'], 'status': 'Active development; preservation snapshot', 'videoGameOnly': True, 'authoredSpellCounts': index['authoredCounts'], 'activeCheckpoint': h.p.binding(CHECKPOINT), 'currentEvidence': bindings, 'pendingCohortsAdopted': False, 'sourceInformationDeleted': 0, 'historyRewritten': False, 'wholeGameAcceptanceClaimed': False}
    manifest = dict(plan, assembledAtUtc=datetime.now(timezone.utc).isoformat(), deliveryOverlays=overlays, allSelectedSourcesHashedAtScan=True, changedSourcesReverifiedAtAssembly=True)
    extras = {STATUS: status.encode(), f'{REPORT}/DELIVERY_CHECKPOINT.json': jsraw(delivery), f'{REPORT}/manifest.json': jsraw(manifest), f'{REPORT}/delivery-script.py': Path(__file__).read_bytes()}
    for name, raw in extras.items():
        write_new(D / name, raw)
        paths.append(name)
    for name in set(paths):
        expected[name] = h.p.blob(lp(D / name).read_bytes())
    write_new(W / 'expected-staged-blobs.json', jsraw(expected))
    write_new(W / 'stage-paths.nul', b'\0'.join(n.encode() for n in sorted(set(paths))) + b'\0')
    print(json.dumps({'sourceFilesHashedAtScan': len(plan['included']), 'changedSourcesReverifiedAtAssembly': sum(x['changedFromBaseline'] for x in plan['included']), 'pathsToStage': len(set(paths)), 'counts': index['authoredCounts']}))


if __name__ == '__main__':
    {'scan': scan, 'assemble': assemble, 'verify': h.p.verify}[sys.argv[1]]()
