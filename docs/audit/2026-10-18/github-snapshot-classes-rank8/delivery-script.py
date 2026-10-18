"""Preserve class-copy implementation and the six-spell rank-eight source audit."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('classes_rank8_delivery_helpers', HERE/'deliver_progress_2026_10_16_video_game.py')
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
G, D, A = h.G, h.D, h.A
BASE = 'e2fb43028e21f74c049aab8926bc2f3ed1966a03'
W = HERE.parent/'audit_work/github-snapshot-2026-10-18-classes-rank8'
REPORT = 'docs/audit/2026-10-18/github-snapshot-classes-rank8'
STATUS = 'SNAPSHOT_STATUS_2026-10-18_CLASSES_RANK8.md'
CHECKPOINT = f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK8_DAMAGE_25.json'
lp, git, digest, write_new, jsraw = h.lp, h.git, h.digest, h.write_new, h.jsraw
for module in [h, h.p]: module.BASE, module.W, module.REPORT, module.STATUS = BASE, W, REPORT, STATUS
h.p.tree = lambda ref=BASE: h.oldtree(ref)
SCOPE = 'Agreed Shaman/Mirrorsage feat-copy integration205 checks/22 conditional histories; rank8 damage6 source conference51 full sources/20 unselected questions/240 preservation checks; queue18/checkpoint25.525 reviewed323 pending unchanged. GPT updates UNSENT because Part4 is full and Part5 creation authorization remains pending. No new rule, source deletion or broad approval.'


def scan():
    h.scan(); p = W/'plan.json'; plan = json.loads(p.read_bytes())
    plan.update(ownerInstruction='Preserve continuing work on GitHub, retain all source information, confer with actual GPT and continue to review completion or20percent remaining.', scope=SCOPE)
    p.write_bytes(jsraw(plan))


def assemble():
    plan = json.loads((W/'plan.json').read_bytes()); assert not plan['credentialPatternAlerts']
    assert git('status', '--porcelain=v1', '-z') == b'' and git('rev-parse', 'HEAD').decode().strip() == BASE
    expected = {}; paths = []
    for row in plan['included']:
        expected[row['path']] = row['gitBlob']
        if row['changedFromBaseline']:
            raw = lp(G/row['path']).read_bytes(); assert digest(raw) == row['sha256'], row['path']
            dst = lp(D/row['path']); dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(raw)
            assert digest(dst.read_bytes()) == row['sha256']; paths.append(row['path'])
    index = h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts'] == {'reviewed': 525, 'pending': 323}
    assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product'] == 'video-game-only'
    test = h.p.read(f'{A}/FEAT335_COPY_CLASSES_01_CHECK.json')
    assert test['checks'] == 205 and not test['failures'] and test['runtimeApproved'] is False
    conference = h.p.read(f'{A}/RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_CHECK.json')
    assert conference['checkCount'] == 240 and conference['questions'] == 20 and conference['newCurrentVectors'] == 0 and conference['failures'] == 0
    notice = f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 ordinary spells reviewed /323 pending.** Shaman/Mirrorsage copy integrations and a six-spell rank-eight source conference are preserved. GPT Part4 is full; continuation creation awaits authorization. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays = []
    for name in ['README.md', 'START_HERE.md']:
        raw = lp(G/name).read_bytes(); preserved = f'{REPORT}/source-before/{name}'; write_new(D/preserved, raw)
        delivered = notice.encode()+raw; lp(D/name).write_bytes(delivered)
        overlays.append({'path': name, 'sourceSha256': digest(raw), 'deliveredSha256': digest(delivered), 'preservedSource': preserved}); paths.extend([name, preserved])
    status = f'''# Decennium Descent development backup —18 October2026 UTC

Video-game-only development continues. This backup preserves work after `{BASE}`. Ordinary spells remain **525 reviewed /323 pending**,249 standalone procedures and173 scoped accepted interfaces. No new rule, spell approval, cosmology choice or whole-game gate was adopted.

The previously agreed copy rules now have actual Shaman and Mirrorsage credentials, paid class ASIs, real rank/RP ceilings and all seven existing recipient adapters.205 checks across22 conditional histories pass. The Shaman copy uses Wisdom, shares the selected paid totem’s RP/cadence/Action state and adopted concentration, and neither receives nor consumes the ordinary totem vent. A subsequent actual ordinary Fate Coin receives its positive vent. Sustained copies end the actual totem before countering, without restoration. Bloodcaller cannot treat retained RP as ordinary Shaman rank permission; an independently paid feat-only Blast provider remains CHA/q0.

Mirrorsage copies use Intelligence without the class Echo first-release Refrain waiver. The same EchoLedger and wallet connect to the existing Beast-origin summon/command/payment boundary, proving mutual release-cap exclusion. The class record is an explicit independently acquired prior-record premise; full class Mirrorbind capture and class Echo strain/payload are NOT certified. Class advancement/training/hero acquisition, world geometry, full Ready transactions, source-specific price modifiers, general interceptors, wider suppression/body cleanup/save-load and shipped runtime remain open. The prior136 commitment and115 recipient checks also pass unchanged. Full source/code/evidence archives remain UNSENT to actual GPT.

The new six-spell source conference covers Deep Crust Spike, Molecular Destabilization, Soul Pyre, Incendiary Cloud, Dimensional Break and Illusory Wall of Doom. It preserves51 complete source files, six book placements,12 accepted counterpart cards/casebooks and20 unselected questions.240 source/authority/preservation checks pass; four records are tierB and two tierC. Incendiary Cloud’s repeated10d8 conflicts with its Instantaneous metadata; mixed-damage allocation, corpse consumption, exile, perception and duration require actual decisions. No new operational procedure or worked case is claimed. The packet is prepared UNSENT.

Continue from [checkpoint25]({CHECKPOINT}), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). Queue18 retains all323 pending identities, now148 in20 prepared/review groups and175 ungrouped. All75 full domain rows/gates remain unchanged. The latest allowance observation is46%remaining; continue until actual review completion or20%remaining.

GPT Part4 reached the explicit conversation-length limit. Part5 creation remains awaiting the owner’s response. No Illusion14 final, new submission or acceptance is inferred. The full handoff02 and both original Illusion conference/context archives remain ready; subsequent copy payload/class and rank-eight source archives are separately preserved. Resume full Illusion14 first, then CompanionExact05 with CR2 evidence; keep full context and scope distinctions. COPY-READY-ALLOWANCE-01 remains an unanswered exact-source timing question.

The [preservation manifest]({REPORT}/manifest.json) records selected source hashes and locally retained exclusions. Every prior tracked entry remains. Existing boundaries retain private configuration, unrelated browser captures, third-party references, imported assets, dependencies and mixed archives locally. No deletion, force push, history rewrite or remote import into the authoring folder occurs. This is a development backup, not publication, balance approval, human playtest or whole-game-flow approval.
'''
    evidence = {n: h.p.binding(f'{A}/{n}') for n in ['FEAT335_COPY_CLASSES_01_PREPARATION.json', 'FEAT335_COPY_CLASSES_01_CHECK.json',
        'RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_PREPARATION.json', 'RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_CHECK.json',
        'COPY_CLASSES_24_CHECK.json', 'RANK8_DAMAGE_25_CHECK.json', 'GPT_REVIEW_PART4_LENGTH_LIMIT_01_STATUS.json']}
    delivery = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'ownerInstruction': plan['ownerInstruction'], 'scope': SCOPE,
        'videoGameOnly': True, 'activeCheckpoint': h.p.binding(CHECKPOINT), 'evidence': evidence, 'authoredSpellCounts': index['authoredCounts'],
        'newRuleAdoptions': 0, 'sourceInformationDeleted': 0, 'wholeGameAcceptanceClaimed': False, 'pendingGptUpdateSent': False}
    manifest = dict(plan, assembledAtUtc=datetime.now(timezone.utc).isoformat(), deliveryOverlays=overlays,
        allSelectedSourcesHashedAtScan=True, changedSourcesReverifiedAtAssembly=True)
    extras = {STATUS: status.encode(), f'{REPORT}/DELIVERY_CHECKPOINT.json': jsraw(delivery), f'{REPORT}/manifest.json': jsraw(manifest),
              f'{REPORT}/delivery-script.py': Path(__file__).read_bytes()}
    for name, raw in extras.items(): write_new(D/name, raw); paths.append(name)
    for name in set(paths): expected[name] = h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json', jsraw(expected))
    write_new(W/'stage-paths.nul', b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed': len(plan['included']), 'changedSources': sum(x['changedFromBaseline'] for x in plan['included']),
                      'pathsToStage': len(set(paths)), 'counts': index['authoredCounts']}))


def verify_push():
    commit = git('rev-parse', 'HEAD').decode().strip(); remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    assert commit == remote and git('rev-parse', 'HEAD^').decode().strip() == BASE and git('status', '--porcelain=v1', '-z') == b''
    expected = json.loads((W/'expected-staged-blobs.json').read_bytes()); tree = h.oldtree(commit); baseline = h.oldtree(BASE)
    assert all(tree.get(n, {}).get('oid') == oid for n, oid in expected.items()) and set(baseline) <= set(tree)
    report = REPORT+'/STAGED_VERIFICATION.json'; assert tree[report]['oid'] == h.p.blob(lp(D/report).read_bytes())
    assert set(tree)-set(baseline)-set(expected) == {report}
    receipt = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'sourceRoot': str(G), 'deliveryRoot': str(D), 'baseCommit': BASE,
        'commit': commit, 'remoteMain': remote, 'url': f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}',
        'worktreeClean': True, 'expectedBlobsVerified': len(expected), 'totalCommitEntries': len(tree), 'priorTrackedEntriesPreserved': len(baseline),
        'trackedEntriesDeleted': 0, 'sourceInformationDeleted': 0, 'authoredCounts': {'reviewed': 525, 'pending': 323},
        'developmentContinues': True, 'wholeGameCompleted': False, 'scope': SCOPE}
    write_new(W/'push-receipt.json', jsraw(receipt)); write_new(G/REPORT/'PUSH_RECEIPT.json', jsraw(receipt)); print(json.dumps(receipt))


if __name__ == '__main__': {'scan': scan, 'assemble': assemble, 'verify': h.p.verify, 'verify-push': verify_push}[sys.argv[1]]()
