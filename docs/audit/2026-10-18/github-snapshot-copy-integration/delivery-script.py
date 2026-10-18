"""Preserve approved-rule copy integrations and truthful GPT continuation status."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('copy_integration_delivery_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='f919c20a62b98d4c65e38320954185f00e3b1f2b'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-copy-integration'
REPORT='docs/audit/2026-10-18/github-snapshot-copy-integration'
STATUS='SNAPSHOT_STATUS_2026-10-18_COPY_INTEGRATION.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_COPY_PAYLOADS_23.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for module in [h,h.p]:module.BASE,module.W,module.REPORT,module.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)
SCOPE='Previously agreed feat-copy commitment and recipient effects;136 commitment checks and115 recipient checks/27 conditional payload histories. GPT Part4 conversation-length limit diagnosed; full continuation handoff02 prepared UNSENT pending owner authorization. Queue17/checkpoint23;525 reviewed323 pending unchanged. No new rules, domain approvals or source deletions.'


def scan():
    h.scan();p=W/'plan.json';plan=json.loads(p.read_bytes())
    plan.update(ownerInstruction='Preserve continuing work on GitHub, keep actual GPT involved, continue until review complete or20percent allowance remains. Preserve all original information.',scope=SCOPE)
    p.write_bytes(jsraw(plan))


def assemble():
    plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts']
    assert git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
    expected={};paths=[]
    for row in plan['included']:
        expected[row['path']]=row['gitBlob']
        if row['changedFromBaseline']:
            raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path']
            dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
            assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
    index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts']=={'reviewed':525,'pending':323}
    assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
    for name,count in [('FEAT335_COPY_RELEASE_01_CHECK.json',136),('FEAT335_COPY_PAYLOADS_01_CHECK.json',115)]:
        result=h.p.read(f'{A}/{name}');assert result['checks']==count and not result['failures'] and result['runtimeApproved'] is False
    notice=f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 ordinary spells reviewed /323 pending.** Agreed copied-spell commitment and recipient effects are implemented in bounded Python integrations. GPT Part4 reached its conversation-length limit; continuation approval is pending. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup —18 October2026 UTC

Video-game-only development continues. This snapshot preserves work after `{BASE}`. Ordinary-spell membership remains **525 reviewed /323 pending**,249 standalone procedures and173 scoped accepted interfaces. No new spell, feat, cosmology decision or whole-game gate is adopted by this push.

The previously agreed CRS-01..03 feat-copy rules now have a direct-Action commitment adapter: actual paid Echo/Mimicry/Adaptation acquisitions and captured components feed existing RP, shared chronological Dissonance/Refrain, provider checks, permission consumption, owner-round cap and the canonical concentration ledger.136 checks cover19 conditional histories and all seven profiles. Ready concentration is separately tested from an already-paid preparation premise; no complete Ready payment/trigger/Reaction/cap transaction is asserted. Actual Shaman/Mirrorsage provider and class shared-allowance integrations remain open.

A subsequent recipient adapter adds115 checks over27 conditional paid histories. It uses canonical LifeState HP/Wounds/death, the single BufferLedger, ordinary healing reductions/prohibitions/Critical caps, strongest slow arbitration, new-Reaction restriction, one Boon AC family and same-body personal teleport. Tests cover a shared Burst roll with independent defenses, critical damage caps, rejected shield offers, exact supplied expiry markers and removal of a real shield at concentration commitment even when the new spell is countered. Full source/code/evidence archives are preserved and remain UNSENT to actual GPT. Geometry/perception/action/marker fixtures, full runtime, general interceptors, price modifiers, suppression/dispels, body-end cleanup, save/load and other explicitly listed integrations remain open. Passing Python checks do not approve the335-feat catalog, human gameplay, balance, canon or release.

Part4's actual ChatGPT UI reported: “The conversation is too long, please start a new one.” This supersedes the earlier connection-only diagnosis. The responsive Dungeon Crawler project still showed Review Continuation Part4, and no Illusion14 final exists. The user has been asked to authorize Calibration Review Part5; no answer or new chat creation is inferred. Full continuation handoff02 and the two original full Illusion review archives are ready. Preserve Part4 and use the complete source archives after authorization. The newer payload progress archive follows the still-outstanding Illusion14/Companion05 conference sequence; it is not a substitute for those semantic reviews.

Continue from [checkpoint23]({CHECKPOINT}), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). Queue17 retains142 identities in19 prepared/review groups and181 ungrouped, with all323 pending identities preserved. All75 complete domain rows and gates remain unchanged. The latest allowance observation is49%remaining; the user requests continuing until review completion or20%remaining. The concrete COPY-READY-ALLOWANCE-01 source question remains queued for actual GPT; no missing rule was silently selected.

The [preservation manifest]({REPORT}/manifest.json) records every selected source hash and locally retained exclusion. Every prior tracked entry remains. Existing boundaries retain private configuration, unrelated browser captures, third-party references, imported assets, dependencies and mixed archives locally. No deletion, force push, history rewrite or remote import into the authoring folder occurs. This is a development backup, not publication or whole-game-flow approval.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['FEAT335_COPY_RELEASE_01_PREPARATION.json','FEAT335_COPY_RELEASE_01_CHECK.json','FEAT335_COPY_PAYLOADS_01_PREPARATION.json','FEAT335_COPY_PAYLOADS_01_CHECK.json','GPT_REVIEW_PART4_LENGTH_LIMIT_01_STATUS.json','GPT_CONTINUATION_05_HANDOFF_02_PREPARATION.json','COPY_PAYLOADS_23_CHECK.json']}
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'videoGameOnly':True,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],'newRuleAdoptions':0,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False,'pendingGptUpdateSent':False}
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
    receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRoot':str(G),'deliveryRoot':str(D),'baseCommit':BASE,'commit':commit,'remoteMain':remote,'url':f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}','worktreeClean':True,'expectedBlobsVerified':len(expected),'totalCommitEntries':len(tree),'priorTrackedEntriesPreserved':len(baseline),'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'authoredCounts':{'reviewed':525,'pending':323},'developmentContinues':True,'wholeGameCompleted':False,'scope':SCOPE}
    write_new(W/'push-receipt.json',jsraw(receipt));write_new(G/REPORT/'PUSH_RECEIPT.json',jsraw(receipt));print(json.dumps(receipt))


if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':verify_push}[sys.argv[1]]()
