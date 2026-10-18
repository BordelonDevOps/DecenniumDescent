"""Preserve storm/control sources through46 and all six reproduced copy defect groups; apply no rules."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('rank9_backup_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='372cb8a66d590811014ecbc8fc7c51ef5c67d955'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-storm-control46'
REPORT='docs/audit/2026-10-18/github-snapshot-storm-control46'
STATUS='SNAPSHOT_STATUS_2026-10-18_STORM_CONTROL46.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK9_STORM_CONTROL_46.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for m in [h,h.p]:m.BASE,m.W,m.REPORT,m.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)
SCOPE='Preserve six rank9 storm/control full sources and25 open decisions, Queue38/checkpoint46, two additional copied-feat diagnostic groups and GPT catch-up/recovery evidence. All prior sources retained;39 accepted spells remain unapplied and525/323/249/173 applied counts unchanged. No gameplay rule/index/runtime or cosmology adoption.'

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
    q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_38.json')
    assert len(q['groups'])==36 and q['preparedOrActualReviewIdentityCount']==227 and q['originalSourceOrReceiptWorkCount']==96
    for name,checks,questions in [('RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_01_CHECK.json',292,25)]:
        v=h.p.read(f'{A}/{name}');assert v['checkCount']==checks and v['questions']==questions and v['failures']==0 and v['newCurrentVectors']==0
    diagnostic=h.p.read(f'{A}/COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_01.json')
    assert len(diagnostic['cases'])==4 and diagnostic['sourcePythonFiles']==38 and not diagnostic['implementationApplied']
    diagnostic2=h.p.read(f'{A}/COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_02.json')
    assert len(diagnostic2['cases'])==3 and diagnostic2['unchangedArchivedPythonFiles']==38 and diagnostic2['totalLocallyReproducedDefectGroupsAcrossReceipts']==6 and not diagnostic2['implementationApplied']
    expected={};paths=[]
    for row in plan['included']:
        expected[row['path']]=row['gitBlob']
        if row['changedFromBaseline']:
            raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path']
            target=lp(D/row['path']);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            assert digest(target.read_bytes())==row['sha256'];paths.append(row['path'])
    notice=f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 reviewed /323 pending;249 standalone.** Source preparation through checkpoint46 is preserved, with227 pending identities grouped and96 ungrouped rank9 identities.39 accepted spells remain unapplied. Six copied-feat defect groups were independently reproduced; final GPT corrections remain pending. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup —18 October2026 UTC

This backup preserves work after `{BASE}` through [checkpoint46]({CHECKPOINT}). Decennium Descent remains video-game-only. Applied membership is **525 reviewed /323 pending**,249 standalone procedures and173 scoped interfaces.39 accepted spell identities remain unapplied under the owner's reserved later implementation instruction. This push applies no gameplay rule, index, registry or runtime change.

The new rank9 storm/control6 packet preserves78 complete sources,six native placements,10 applied counterparts and25 unselected decisions;292 source-preservation checks pass. The six identities are Cosmic Implosion,Frozen Eternity,Hellstorm,Storm of Vengeance,Thunder Wrath and Storm Cage. Queue38 groups227 pending identities across36 groups,leaving96 ungrouped rank9 identities. Preparation does not establish semantic acceptance. Full native source/access/history remains preserved.

The packet retains all-creature inward pull and15d10force,one-target time stop for three rounds with ending saves,three8d10fire pulses,a substantive massive varied multiround storm,five6d6lightning strikes per round,and cannot-escape electrical confinement. Actual geometry,source duration conflicts,personal clocks,strike control,damage events and containment choices are separately proposed. No source benefit is reduced for tabletop convenience and no new cosmology identity is selected.

[Calibration Review Part 5](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad4a867-f330-83e9-829e-bf2bb41a6c09) remains in its copied-feat review at capture. Its latest visible progress reports regression checks and preparation of a manifest-bound archive; the actual final archive has not been received. The new [diagnostic receipt02]({A}/COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_02.json) adds two reproduced defect groups: inactive healing reducers wrongly block Copied Mend,and copy-world clock advancement discards a shared Oracle buffer's natural-expiry instruction. Combined with preserved receipt01,this is seven cases across six groups. All38 archived Python files remain unchanged. These are conditional reference-helper reproductions,not production-engine tests or implemented fixes.

The latest follow-up remains unsent to avoid interrupting the active response. A temporary read rate limit cleared for the primary chat; the separate Review continuation part 5 could not yet be freshly read. New evidence distinguishes completed Control15 acceptance from pending copied-feat corrections. No whole-feature approval follows from the observed test counts.

Continue from [START_HERE.md](START_HERE.md),[REVIEW_MAP.html](REVIEW_MAP.html) and the current checkpoint. Latest allowance observation is22percent remaining; the owner's stopping threshold is20percent. Source preservation,semantic review,reference arithmetic,engine implementation,runtime/human testing,balance,cosmology,75-domain closure,whole-game completion and release remain separate gates.

The [manifest]({REPORT}/manifest.json) records source hashes and locally retained exclusions. All earlier tracked Git entries remain. Established exclusions retain private configuration,unrelated browser captures,external reference books,imported assets,dependencies and mixed immutable archives locally. No deletion,force push or history rewrite occurs;the authoring folder remains separate from the delivery checkout.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['ACTIVE_AUTHORING_CHECKPOINT_RANK9_STORM_CONTROL_46_CHECK.json','RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_01_PREPARATION.json','COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_01.json','COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_02.json','GPT_PART5_COPY_REVIEW_04_PROGRESS_46_UI.txt','GPT_PART5_PERTINENT_CHECK_02_RECOVERY_STATUS.json']}
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
