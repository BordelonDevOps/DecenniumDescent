"""Preserve actual GPT continuation and three complete rank8 source conferences."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('part5_delivery_helpers', HERE/'deliver_progress_2026_10_16_video_game.py')
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
G, D, A = h.G, h.D, h.A
BASE = '4e7ec8d2c9c77931ecc18e74dbcbf96eebd64cb1'
W = HERE.parent/'audit_work/github-snapshot-2026-10-18-part5-wards'
REPORT = 'docs/audit/2026-10-18/github-snapshot-part5-wards'
STATUS = 'SNAPSHOT_STATUS_2026-10-18_PART5_WARDS.md'
CHECKPOINT = f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK8_WARD_32.json'
lp, git, digest, write_new, jsraw = h.lp, h.git, h.digest, h.write_new, h.jsraw
for module in [h,h.p]: module.BASE, module.W, module.REPORT, module.STATUS = BASE,W,REPORT,STATUS
h.p.tree = lambda ref=BASE:h.oldtree(ref)
SCOPE = 'Actual Calibration Review Part5 continuation delivered; full Illusion14 review in progress at capture. Three rank8 source conferences cover16 identities and65 unselected questions; resource6/control5/ward5 have229/251/359 source checks. Queue25/checkpoint32,177 identities in26 groups,146 ungrouped.525reviewed323pending unchanged; no new rule, deletion or broad approval.'


def scan():
    h.scan()
    p = W/'plan.json'; plan = json.loads(p.read_bytes())
    plan.update(ownerInstruction='Preserve continuing development on GitHub, retain source information and keep actual GPT involved; continue to completion or20percent remaining.',scope=SCOPE)
    p.write_bytes(jsraw(plan))


def assemble():
    plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts']
    assert git('status','--porcelain=v1','-z') == b'' and git('rev-parse','HEAD').decode().strip() == BASE
    expected, paths = {}, []
    for row in plan['included']:
        expected[row['path']] = row['gitBlob']
        if row['changedFromBaseline']:
            raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path']
            dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
            assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
    index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts']=={'reviewed':525,'pending':323}
    assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
    for filename,checks,questions in [
        ('RANK8_RESOURCE_6_SOURCE_CONFERENCE_01_CHECK.json',229,24),
        ('RANK8_CONTROL_5_SOURCE_CONFERENCE_01_CHECK.json',251,18),
        ('RANK8_WARD_5_SOURCE_CONFERENCE_01_CHECK.json',359,23)]:
        conference=h.p.read(f'{A}/{filename}')
        assert conference['checkCount']==checks and conference['questions']==questions and conference['newCurrentVectors']==0 and conference['failures']==0
    checkpoint=h.p.read(CHECKPOINT)
    actual=h.p.read(f'{A}/GPT_CONTINUATION_05_ACTUAL_START_01.json')
    assert actual['chat']['threadId']=='6ad4a867-f330-83e9-829e-bf2bb41a6c09' and actual['actualUserTurn']=='49c773ce-baf8-44ed-9658-595d5a7e5b10'
    assert checkpoint['activeGptReview']==actual and not actual['semanticAcceptanceClaimed']
    queue=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_25.json')
    assert queue['preparedOrActualReviewIdentityCount']==177 and queue['originalSourceOrReceiptWorkCount']==146 and len(queue['groups'])==26
    notice=f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 ordinary spells reviewed /323 pending.** Calibration Review Part5 received the full handoff and Illusion14 review archives. New resource/control/ward source conferences and checkpoint32 are preserved. No new semantic approval is claimed. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup —18 October2026 UTC

This backup preserves video-game development after `{BASE}` through [checkpoint32]({CHECKPOINT}). Ordinary spells remain **525 reviewed /323 pending**, with249 standalone procedures and173 accepted scoped interfaces. Source preparation and actual delivery are distinct from semantic acceptance.

[Calibration Review Part5]({actual['chat']['url']}) received three full archives: handoff03, Illusion14 Current12 and its current-acceptance supplement. The saved user turn, exact request, attachment names, byte/hash bindings and visible live review are recorded in the [actual submission]({A}/GPT_CONTINUATION_05_ACTUAL_START_01.json). The old Part4 length-limit evidence is preserved. The additional continuation confirmation was an unnecessary Codex interpretation; the owner's standing instructions already authorized continued collaboration. No new human answer or automatic approval rejection is fabricated. GPT is actively reviewing14 full procedures and their cases; no final has yet been recorded. CompanionExact05 plus expanded CR2 evidence are next.

The complete copy commitment, recipient and class-provider integrations and two source conferences were delivered within handoff03 for awareness. Four later source conferences were summarized in the actual request. Their full packets still await delivery; the newest ward5 packet was prepared after that request and is also unsent. Historical UNSENT labels inside frozen preparations describe their original creation time.

Three complete rank8 source conferences are new since the prior backup:

- Resource6:52 full sources,24 questions and229 checks. Spell absorption, recovery, cost waivers and exact cost knowledge retain their source conflicts, including the unassigned Mana Furnace alias and Leyline Flow's differing recovery amounts.
- Control5:61 full sources,18 questions and251 checks. Frozen Time Prism, Paralyzing Presence, Power Word Stun, Mental Collapse and Reality Rewrite retain their exact native promises and open state/timing/channel decisions.
- Ward5:81 full sources,eight school placements,21 accepted counterparts,23 questions and359 checks. Alignment Immunity, Antilife Shell, Antimagic Field, Mind Blank and Reputation Fortress preserve distinct school text, class access and source-specific protection/geometry/suppression questions. Two individually tierB and three tierC; no procedure or case is adopted.

Queue25 retains all323 pending identities:177 in26 active/prepared groups and146 ungrouped. All75 full domain rows/gates remain unchanged. Checkpoint32 has520 source/preservation/navigation checks and1406 existing links with none missing. CompanionExact05's eight artifacts and both next-review archives were independently checked against their preserved hashes; no content hold was silently cleared.

Continue from [START_HERE.md](START_HERE.md) and [REVIEW_MAP.html](REVIEW_MAP.html). Latest allowance observation39percentremaining; continue to review completion or20percentremaining. Runtime, human gameplay, numerical balance, cosmology canon, whole-game flow and release are separate gates. This is a development backup.

The [preservation manifest]({REPORT}/manifest.json) records selected files and retained local exclusions. Every prior tracked Git entry remains. Existing exclusions keep private configuration, unrelated browser captures, third-party references, imported assets, dependencies and mixed archives locally. No deletion, force push or history rewrite is performed. The source authoring folder remains separate from the delivery checkout.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in [
        'RANK8_RESOURCE_6_SOURCE_CONFERENCE_01_PREPARATION.json','RANK8_RESOURCE_6_SOURCE_CONFERENCE_01_CHECK.json',
        'RANK8_CONTROL_5_SOURCE_CONFERENCE_01_PREPARATION.json','RANK8_CONTROL_5_SOURCE_CONFERENCE_01_CHECK.json',
        'RANK8_WARD_5_SOURCE_CONFERENCE_01_PREPARATION.json','RANK8_WARD_5_SOURCE_CONFERENCE_01_CHECK.json',
        'RANK8_WARD_32_CHECK.json','GPT_CONTINUATION_05_ACTUAL_START_01.json','GPT_PART5_REVIEW_31_CHECK.json','GPT_PART5_LABELS_31A_CHECK.json']}
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,
        'videoGameOnly':True,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],
        'newRuleAdoptions':0,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False,'actualGptContinuationDelivered':True,'illusionFinalReceived':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'counts':index['authoredCounts']}))


def verify_push():
    commit=git('rev-parse','HEAD').decode().strip();remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
    assert commit==remote and git('rev-parse','HEAD^').decode().strip()==BASE and git('status','--porcelain=v1','-z')==b''
    expected=json.loads((W/'expected-staged-blobs.json').read_bytes());tree=h.oldtree(commit);baseline=h.oldtree(BASE)
    assert all(tree.get(n,{}).get('oid')==oid for n,oid in expected.items()) and set(baseline)<=set(tree)
    report=REPORT+'/STAGED_VERIFICATION.json';assert tree[report]['oid']==h.p.blob(lp(D/report).read_bytes())
    assert set(tree)-set(baseline)-set(expected)=={report}
    receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRoot':str(G),'deliveryRoot':str(D),'baseCommit':BASE,
        'commit':commit,'remoteMain':remote,'url':f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}',
        'worktreeClean':True,'expectedBlobsVerified':len(expected),'totalCommitEntries':len(tree),'priorTrackedEntriesPreserved':len(baseline),
        'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'authoredCounts':{'reviewed':525,'pending':323},
        'developmentContinues':True,'wholeGameCompleted':False,'scope':SCOPE}
    write_new(W/'push-receipt.json',jsraw(receipt));write_new(G/REPORT/'PUSH_RECEIPT.json',jsraw(receipt));print(json.dumps(receipt))


if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':verify_push}[sys.argv[1]]()
