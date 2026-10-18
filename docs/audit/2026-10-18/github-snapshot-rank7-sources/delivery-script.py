"""Preserve three rank-seven source conferences and current GPT handoff."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('rank7_sources_delivery_helpers', HERE/'deliver_progress_2026_10_16_video_game.py')
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
G, D, A = h.G, h.D, h.A
BASE = '7142a4f7e9c6088dbd1c92bd2ea3bde3891f42a9'
W = HERE.parent/'audit_work/github-snapshot-2026-10-18-rank7-sources'
REPORT = 'docs/audit/2026-10-18/github-snapshot-rank7-sources'
STATUS = 'SNAPSHOT_STATUS_2026-10-18_RANK7_SOURCES.md'
CHECKPOINT = f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK7_GATE_GLYPH_28.json'
lp, git, digest, write_new, jsraw = h.lp, h.git, h.digest, h.write_new, h.jsraw
for module in [h, h.p]: module.BASE, module.W, module.REPORT, module.STATUS = BASE, W, REPORT, STATUS
h.p.tree = lambda ref=BASE: h.oldtree(ref)
SCOPE = 'Rank7 identity/casting5, perception5 and gate/glyph3 source conferences:13 identities,60 unselected questions, preserved full sources and277/236/308 checks. Queue21/checkpoint28; every pending rank7 access identity now has a review packet, not semantic approval. Handoff03 contains56 context sources and5 complete nested archives through checkpoint26, with later packets separate.525 reviewed323 pending unchanged. GPT updates UNSENT; Part4 full, Part5 creation authorization pending. No new rule, deletion or broad approval.'


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
    for filename, checks, questions in [
        ('RANK7_IDENTITY_CASTING_5_SOURCE_CONFERENCE_01_CHECK.json',277,24),
        ('RANK7_PERCEPTION_5_SOURCE_CONFERENCE_01_CHECK.json',236,21),
        ('RANK7_GATE_GLYPH_3_SOURCE_CONFERENCE_01_CHECK.json',308,15)]:
        conference = h.p.read(f'{A}/{filename}')
        assert conference['checkCount'] == checks and conference['questions'] == questions and conference['newCurrentVectors'] == 0 and conference['failures'] == 0
    checkpoint = h.p.read(CHECKPOINT)
    assert checkpoint['pendingRank7PreparationCoverage']['allHaveReviewPackets'] is True
    assert checkpoint['pendingRank7PreparationCoverage']['semanticApprovalClaimed'] is False
    handoff = h.p.read(f'{A}/GPT_CONTINUATION_05_HANDOFF_03_PREPARATION.json')
    assert handoff['sourceCount'] == 56 and handoff['nestedFullArchiveCount'] == 5 and handoff['allArchivedBytesVerified']
    notice = f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 ordinary spells reviewed /323 pending.** Three new rank-seven source conferences and GPT handoff03 are preserved through checkpoint28. Every pending rank-seven access identity has a source-review packet; none is promoted by preparation. GPT Part4 is full and Part5 creation remains pending. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays = []
    for name in ['README.md', 'START_HERE.md']:
        raw = lp(G/name).read_bytes(); preserved = f'{REPORT}/source-before/{name}'; write_new(D/preserved, raw)
        delivered = notice.encode()+raw; lp(D/name).write_bytes(delivered)
        overlays.append({'path': name, 'sourceSha256': digest(raw), 'deliveredSha256': digest(delivered), 'preservedSource': preserved}); paths.extend([name, preserved])
    status = f'''# Decennium Descent development backup —18 October2026 UTC

Video-game-only development continues. This backup preserves work after `{BASE}` through [checkpoint28]({CHECKPOINT}). Ordinary spells remain **525 reviewed /323 pending**, with249 standalone procedures and173 scoped accepted interfaces. No spell, new rule, cosmology choice or whole-game gate is promoted.

Three complete source conferences now cover13 more identities and60 unselected decisions:

- Identity/casting5: Cast Echo, Meta Surge, Erase from Reality, Sequester and Simulacrum.68 full sources, six placements,24 questions and277 source/access/authority/preservation checks; five individually tierC. Exact Fate Echo acceptance and complete DI7 cases, actual Mage/feat metamagic records and separate pending comparisons are retained.
- Perception5: Inescapable Labyrinth, Mindtrap Echo, Mirage Arcane, Mirage Legion and Perfect Veil.49 full sources, five placements,21 questions and236 checks; individually2B/3C. Tactile terrain, six images, complete unnoticeability, Speed0 and real historical action repetition retain their printed promises.
- Gate/glyph3: Chain Gate, Symbol and Symbol of Death.89 full sources, three placements,15 questions and308 checks; individually1B/2C. Original cosmology manuscripts and saved website are included with owner corrections and qualified planes review after verified push. Portal topology, native harmful payload and lethal threshold behavior remain unselected. Death Ward, genuine would-die replacements and Null damage-only rules keep their accepted scopes.

These are source conferences, with no newly adopted operational procedures or worked cases. Each full raw source and ZIP member is hash/byte verified. Queue21 retains all323 pending identities:161 in23 active/prepared groups and162 ungrouped. Every pending identity with any rank-seven class-access row now belongs to a review packet; this is source-preparation coverage, not semantic completion. All75 complete domain rows/gates are unchanged. The492/496 navigation checks for checkpoints27/28 and their1391/1394 existing links preserve older checkpoints and source records.

GPT Part4 reached its conversation-length limit; the existing request to create Part5 remains pending. No new chat, delivered update, Illusion14 final or acceptance is inferred. The refreshed handoff03 includes56 current-context source files and five full nested progress/source archives through checkpoint26. Perception5, gate/glyph3 and queues20–21/checkpoints27–28 are later supplements and are not claimed inside that frozen handoff. The first submission remains the full Illusion14 Current12 conference plus its acceptance-context archive and current handoff; CompanionExact05 plus expanded CR2 evidence follow separately. Actual copy commitments/recipient effects/class-provider integrations retain their previously reported bounded scopes and open Ready/class Echo/runtime limitations.

Continue from [START_HERE.md](START_HERE.md) and [REVIEW_MAP.html](REVIEW_MAP.html). Latest allowance observation43%remaining; work continues until actual review completion or20%remaining. Runtime, human gameplay, numerical balance, cosmology canon, campaign epoch, full-game flow and publication remain separate gates.

The [preservation manifest]({REPORT}/manifest.json) records selected source hashes and locally retained exclusions. Every prior tracked entry remains. Existing local exclusions retain private configuration, unrelated browser captures, third-party references, imported assets, dependencies and mixed archives. No deletion, force push or history rewrite is performed. This is a development backup, not a release.
'''
    evidence = {n: h.p.binding(f'{A}/{n}') for n in [
        'RANK7_IDENTITY_CASTING_5_SOURCE_CONFERENCE_01_PREPARATION.json', 'RANK7_IDENTITY_CASTING_5_SOURCE_CONFERENCE_01_CHECK.json',
        'RANK7_PERCEPTION_5_SOURCE_CONFERENCE_01_PREPARATION.json', 'RANK7_PERCEPTION_5_SOURCE_CONFERENCE_01_CHECK.json',
        'RANK7_GATE_GLYPH_3_SOURCE_CONFERENCE_01_PREPARATION.json', 'RANK7_GATE_GLYPH_3_SOURCE_CONFERENCE_01_CHECK.json',
        'RANK7_GATE_GLYPH_28_CHECK.json', 'GPT_CONTINUATION_05_HANDOFF_03_PREPARATION.json', 'GPT_REVIEW_PART4_LENGTH_LIMIT_01_STATUS.json']}
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
