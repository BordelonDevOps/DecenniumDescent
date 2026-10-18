"""Preserve the actual DC25 review and subsequent full-source conference work."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('conference_delivery_helpers', HERE / 'deliver_progress_2026_10_16_video_game.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
G, D, A = h.G, h.D, h.A
BASE = '40ad7bb573e1d9a7cb776c20bd82a03ebe3b9d77'
W = HERE.parent / 'audit_work/github-snapshot-2026-10-18-conferences'
REPORT = 'docs/audit/2026-10-18/github-snapshot-conferences'
STATUS = 'SNAPSHOT_STATUS_2026-10-18_CONFERENCES.md'
CHECKPOINT = f'{A}/ACTIVE_AUTHORING_CHECKPOINT_DC25_REBOUND_PERSISTENT_ACTIVE_08.json'
lp, git, digest, write_new, jsraw = h.lp, h.git, h.digest, h.write_new, h.jsraw
for module in [h, h.p]:
    module.BASE, module.W, module.REPORT, module.STATUS = BASE, W, REPORT, STATUS
h.p.tree = lambda ref=BASE: h.oldtree(ref)


def scan():
    h.scan()
    path = W / 'plan.json'
    plan = json.loads(path.read_bytes())
    plan.update(ownerInstruction='Preserve progress on GitHub, keep actual GPT involved, and continue until review completion or 20% allowance remains.', scope='Actual DC25 conference07 review, corrected DC25 Current08 and exact rebound09, active persistent20 conference06, full illusion14 and control15 conference11 packets.')
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
    assert h.p.read(f'{A}/DAMAGE_CONTROL_25_PRESENTATION_09_CHECK.json')['all25ProceduresAnd70CasesUnchanged']
    bindings = {name: h.p.binding(f'{A}/{name}') for name in [
        'DAMAGE_CONTROL_25_CONFERENCE_07_RECEIPT.json',
        'DAMAGE_CONTROL_25_EXACT_REBOUND_09_PREPARATION.json',
        'PERSISTENT_DAMAGE_20_CONFERENCE_06_ACTUAL_SUBMISSION.json',
        'CONTROL_15_CONFERENCE_11_PREPARATION.json',
        'DC25_REBOUND_PERSISTENT_ACTIVE_08_NAVIGATION_CHECK.json',
    ]}
    notice = f'> **Latest development backup — 18 October 2026 UTC:** Video-game development continues with actual GPT. **480 ordinary spells reviewed / 368 pending.** The returned 25-spell corrections and new full conference packets are preserved. See [snapshot status]({STATUS}). Earlier backup notices below are preserved history.\n\n'
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

GPT's actual Damage/Control25 conference07 final response required changes. Its original six-file archive is preserved, all 23 complete before/after corrections were verified and applied to pending Current08, and all original source objects and cases remain available. Three additional example repairs correct two Wizard HP calculations and specify the ice cut needed to justify its support allocation; those repairs still require GPT concurrence. Exact rebound09 contains the complete 25-spell model, 70-record current casebook, player and director manuscripts, source hashes and evidence manifest. Its presentation check confirms the procedures and cases match rebound08 except version identifiers. The new packet is prepared, not yet submitted or accepted.

Persistent20 conference06 is actually submitted to Review Continuation Part4 and was still generating at the snapshot boundary. It retains 20 procedures, 40 original scenarios, seven supplements, eight adversarial cases and 24 substantive questions. Illusion14 conference11 is prepared with 14 procedures, all 28 original vectors and three supplements. Control15 conference11 is prepared with all 15 procedures and 30 original/current scenarios. Conditional source gaps remain explicit, including unavailable operative creature CR and opposed ability-check inputs; these are not asserted as executed game tests. Both conference11 packets remain unsubmitted. Two memory spells and Creation remain separate review work.

Continue from the [active checkpoint]({CHECKPOINT}), [exact rebound preparation]({A}/DAMAGE_CONTROL_25_EXACT_REBOUND_09_PREPARATION.json), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). The active checkpoint precedes exact rebound09 packaging; the preparation record supplies that subsequent milestone. Navigation verified 1,301 distinct links with none missing. All 75 domain gates retain their actual statuses and evidence requirements.

The [manifest]({REPORT}/manifest.json) records exact selected file hashes and locally retained exclusions. Every prior tracked Git entry is preserved. Existing backup boundaries retain private configuration, unrelated raw browser/sidebar captures, third-party books, imported assets, dependencies, generated folders and archives containing excluded materials locally. Original archives are not rewritten. No source deletion, remote import into the authoring folder or force push is used.

This snapshot verifies preservation and authored files. It does not establish engine implementation, runtime behavior, human gameplay, balance, cosmology/canon, whole-game flow or release approval. Development continues until the review is complete or a reported usage allowance reaches 20% remaining; the latest observed allowance was 78% remaining.
'''
    delivery = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'ownerInstruction': plan['ownerInstruction'], 'status': 'Active development; preservation snapshot', 'videoGameOnly': True, 'authoredSpellCounts': index['authoredCounts'], 'activeCheckpoint': h.p.binding(CHECKPOINT), 'subsequentAndCurrentEvidence': bindings, 'pendingCohortsAdopted': False, 'sourceInformationDeleted': 0, 'historyRewritten': False, 'wholeGameAcceptanceClaimed': False}
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
