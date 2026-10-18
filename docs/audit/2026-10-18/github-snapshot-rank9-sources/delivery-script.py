"""Preserve source conferences through45 and reproduced copy defects; apply no rules."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('rank9_backup_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='1eb1a83f6b86934e5a97770f1d10c240c0f23216'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-rank9-sources'
REPORT='docs/audit/2026-10-18/github-snapshot-rank9-sources'
STATUS='SNAPSHOT_STATUS_2026-10-18_RANK9_SOURCES.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK9_CATASTROPHE_45.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for m in [h,h.p]:m.BASE,m.W,m.REPORT,m.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)
SCOPE='Preserve full rank8 planar5 and remaining4, rank9 catastrophe10 source conferences, queues35–37/checkpoints42–45, and four independently reproduced copied-feat reference-helper defects.39 accepted identities remain unapplied;525/323/249/173 applied counts unchanged. No rule/index/runtime or cosmology adoption.'

def scan():
    h.scan();p=W/'plan.json';v=json.loads(p.read_bytes())
    v.update(ownerInstruction='Standing owner requests to back up completed progress, preserve information and continue GPT-assisted video-game development until completion or20percent remaining.',scope=SCOPE)
    p.write_bytes(jsraw(v))

def assemble():
    plan=json.loads((W/'plan.json').read_bytes())
    assert not plan['credentialPatternAlerts'] and git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
    idx=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert idx['authoredCounts']=={'reviewed':525,'pending':323} and idx['representationCounts']['completeReviewedStandaloneProcedures']==249
    cp=h.p.read(CHECKPOINT);assert cp['newRuleAdoptions']==0 and cp['acceptedButUnapplied']['totalDistinctIdentities']==39 and not cp['wholeGameComplete']
    assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
    q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_37.json')
    assert len(q['groups'])==35 and q['preparedOrActualReviewIdentityCount']==221 and q['originalSourceOrReceiptWorkCount']==102
    for name,checks,questions in [('RANK8_PLANAR_5_SOURCE_CONFERENCE_01_CHECK.json',284,24),('RANK8_REMAINING_4_SOURCE_CONFERENCE_01_CHECK.json',320,22),('RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_01_CHECK.json',321,25)]:
        v=h.p.read(f'{A}/{name}');assert v['checkCount']==checks and v['questions']==questions and v['failures']==0 and v['newCurrentVectors']==0
    diagnostic=h.p.read(f'{A}/COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_01.json')
    assert len(diagnostic['cases'])==4 and diagnostic['sourcePythonFiles']==38 and not diagnostic['implementationApplied']
    expected={};paths=[]
    for row in plan['included']:
        expected[row['path']]=row['gitBlob']
        if row['changedFromBaseline']:
            raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path']
            target=lp(D/row['path']);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            assert digest(target.read_bytes())==row['sha256'];paths.append(row['path'])
    notice=f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 reviewed /323 pending;249 standalone.** Source preparation through checkpoint45 is preserved, with221 pending identities grouped and102 ungrouped rank9 identities.39 accepted spells remain unapplied. Four copied-feat defects were reproduced; final GPT corrections remain pending. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup —18 October2026 UTC

This backup preserves work after `{BASE}` through [checkpoint45]({CHECKPOINT}). Decennium Descent remains video-game-only. Applied membership is **525 reviewed /323 pending**,249 standalone procedures and173 scoped interfaces.39 exact accepted spell identities remain unapplied under the owner's reserved later implementation instruction. This push makes no gameplay rule, index, registry or runtime change.

The new full source conferences are rank8 planar5 (82 sources,24 questions,284 preservation checks), rank8 remaining4 (102 sources,22 questions,320 checks), and rank9 catastrophe10 (77 sources,12 placements,25 questions,321 checks). All rank8 identities now have a preparation/review group; this does not establish semantic acceptance. Queue37 groups221 pending identities across35 groups, leaving102 ungrouped rank9 identities. Every original source, native class-access row, placement and prior question remains preserved.

The catastrophe packet preserves the full printed scope: one-mile Cataclysm, four Meteor Swarm impacts, actual structural obliteration, lasting scorched terrain, random plural damage types and genuine self-sacrifice. Range, duration, damage allocation, overlap, material and survival conflicts are explicit unselected choices. No source benefit was reduced for tabletop convenience and no new cosmology identity was selected.

[Calibration Review Part5](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad4a867-f330-83e9-829e-bf2bb41a6c09) remains active on the copied-feat review at capture. Codex independently reproduced four reference-helper issues: private Reaction accounting leaves a second canonical payment available; Shaman unconsciousness after declaration is missed at resolution; Copied Step leaves class/aura coordinates stale; duplicate adapter construction gives a fresh per-instance round cap. The [diagnostic receipt]({A}/COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_01.json) contains exact inputs/outcomes and38 unchanged archived Python bindings. These are conditional local helper reproductions, not production-engine tests. No fixes or final GPT acceptance are claimed. The prepared follow-up remains unsent to avoid interrupting that active review.

Continue from [START_HERE.md](START_HERE.md), [REVIEW_MAP.html](REVIEW_MAP.html) and the current checkpoint. Latest allowance observation is24percent remaining; the user stopping threshold is20percent. Source preservation, semantic review, reference arithmetic, engine implementation, runtime/human testing, balance, cosmology,75-domain closure, whole-game completion and release remain separate gates.

The [manifest]({REPORT}/manifest.json) records source hashes and locally retained exclusions. All earlier tracked Git entries remain. Established exclusions retain private configuration, unrelated browser captures, external reference books, imported assets, dependencies and mixed immutable archives locally. No deletion, force push or history rewrite occurs; the authoring folder remains separate from the delivery checkout.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['ACTIVE_AUTHORING_CHECKPOINT_RANK9_CATASTROPHE_45_CHECK.json','RANK8_PLANAR_5_SOURCE_CONFERENCE_01_PREPARATION.json','RANK8_REMAINING_4_SOURCE_CONFERENCE_01_PREPARATION.json','RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_01_PREPARATION.json','COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_01.json','GPT_PART5_COPY_REVIEW_04_PROGRESS_44_NATIVE.json']}
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':idx['authoredCounts'],'exactAcceptedButUnappliedIdentities':39,'copiedFeatFinalReceivedAtCapture':False,'newRuleAdoptions':0,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'newRulesApplied':0}))

def verify_push():
    commit=git('rev-parse','HEAD').decode().strip();remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
    assert commit==remote and git('rev-parse','HEAD^').decode().strip()==BASE and git('status','--porcelain=v1','-z')==b''
    expected=json.loads((W/'expected-staged-blobs.json').read_bytes());tree=h.oldtree(commit);baseline=h.oldtree(BASE)
    assert all(tree.get(n,{}).get('oid')==oid for n,oid in expected.items()) and set(baseline)<=set(tree)
    report=REPORT+'/STAGED_VERIFICATION.json'
    assert tree[report]['oid']==h.p.blob(lp(D/report).read_bytes()) and set(tree)-set(baseline)-set(expected)=={report}
    receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRoot':str(G),'deliveryRoot':str(D),'baseCommit':BASE,'commit':commit,'remoteMain':remote,'url':f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}','worktreeClean':True,'expectedBlobsVerified':len(expected),'totalCommitEntries':len(tree),'priorTrackedEntriesPreserved':len(baseline),'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'authoredCounts':{'reviewed':525,'pending':323},'developmentContinues':True,'wholeGameCompleted':False,'scope':SCOPE}
    write_new(W/'push-receipt.json',jsraw(receipt));write_new(G/REPORT/'PUSH_RECEIPT.json',jsraw(receipt));print(json.dumps(receipt))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':verify_push}[sys.argv[1]]()
