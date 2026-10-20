"""Back up preserved authoring through checkpoint57 without applying proposed mechanics."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('backup46_helpers',HERE/'deliver_progress_2026_10_18_storm_control46.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
h=p.h
G,D,A=p.G,p.D,p.A
BASE='867da46cfddbbdb26d7d63c228316a8e6014e971'
W=HERE.parent/'audit_work/github-snapshot-2026-10-20-memory-denial57'
REPORT='docs/audit/2026-10-20/github-snapshot-memory-denial57'
STATUS='SNAPSHOT_STATUS_2026-10-20_MEMORY_DENIAL57.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK9_MEMORY_DENIAL_57.json'
SCOPE='Preserve checkpoints53-57 and four complete rank9 agency/control9,time/fate6,casting/cost5 and memory/denial6 source conferences,all original histories,exact candidate/source archives and the recorded Windows path-length packaging recovery. No canonical mechanic/index/runtime or cosmology application;39 accepted identities remain unapplied.'
lp,git,digest,write_new,jsraw=p.lp,p.git,p.digest,p.write_new,p.jsraw
for m in [p,h,h.p]:m.BASE,m.W,m.REPORT,m.STATUS=BASE,W,REPORT,STATUS
p.SCOPE=SCOPE
h.p.tree=lambda ref=BASE:h.oldtree(ref)

def scan():
    h.scan()
    path=W/'plan.json';plan=json.loads(path.read_bytes())
    plan.update(ownerInstruction='Standing owner authorization to preserve progress on GitHub while continuing GPT-assisted video-game development.',scope=SCOPE)
    path.write_bytes(jsraw(plan))

def assemble():
    plan=json.loads((W/'plan.json').read_bytes())
    assert not plan['credentialPatternAlerts'] and git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
    cp=h.p.read(CHECKPOINT)
    assert cp['acceptedButUnapplied']==39 and not cp['implementationApplied'] and not cp['wholeGameComplete']
    index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249
    q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_47.json')
    assert len(q['groups'])==44 and q['preparedOrActualReviewIdentityCount']==281 and q['originalSourceOrReceiptWorkCount']==42
    checks=[('RANK9_AGENCY_CONTROL_9_SOURCE_CONFERENCE_01_CHECK.json',347),('RANK9_TIME_FATE_6_SOURCE_CONFERENCE_01_CHECK.json',415),('RANK9_CASTING_COST_5_SOURCE_CONFERENCE_01_CHECK.json',341),('RANK9_MEMORY_DENIAL_6_SOURCE_CONFERENCE_01_CHECK.json',370)]
    for name,count in checks:
        v=h.p.read(f'{A}/{name}');assert v['checkCount']==count and v['failures']==0,name
    assert not h.p.read(f'{A}/COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json')['implementationApplied']
    for b in cp['canonicalHelperBaselinesUnchanged']:
        assert h.p.binding(b['path'])==b,b['path']
    expected={};paths=[]
    for row in plan['included']:
        expected[row['path']]=row['gitBlob']
        if row['changedFromBaseline']:
            raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path']
            target=lp(D/row['path']);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            assert digest(target.read_bytes())==row['sha256'];paths.append(row['path'])
    notice=f'> **Latest development backup — 20 October 2026:** Work through checkpoint 57 is preserved. Four new rank-9 review packets cover 26 identities; their proposed decisions remain unselected. Applied counts remain 525 reviewed / 323 pending, with249 standalone procedures,173 interfaces and39 accepted-but-unapplied identities. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup — 20 October 2026

This backup preserves work after `{BASE}` through [checkpoint57]({CHECKPOINT}). The game is video-game-only. Applied membership remains **525 reviewed /323 pending /249 standalone procedures /173 interfaces**. The39 accepted identities and proposed Ready/copy corrections remain unapplied under the owner's implementation reservation. This push is preservation,not a gameplay release or semantic approval.

Four complete source conferences have been prepared:

| Conference | Identities | Complete sources | Native placements | Open questions | Source checks |
|---|---:|---:|---:|---:|---:|
| Agency/control |9|96|9|32|347|
| Time/fate |6|140|8|32|415|
| Casting/cost |5|117|5|32|341|
| Memory/ability denial |6|120|6|28|370|

The packets preserve complete original source/access records,historical questions,actual applied counterparts,full pending comparison archives and current accepted-but-unapplied context. None of their questions is selected merely by being packaged. [Queue47](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_47.json) groups281 pending identities in44 groups and leaves42 rank9identities ungrouped. These preparation counts are distinct from authored acceptance.

Key unresolved conflicts are retained explicitly: Time Stop's1d4+1round Action versus3-turn Reaction; Fate Rewrite's real past-event change and Eternal Prophecy's guaranteed future; Perfect Spell's any-spell/component/cost/time bypass; Ritual Mastery's instant effect versus10-minute Core activation; Resonance Perfection's exact available-RP pricing; Unholy Ascendance's complete transformation/free-necrotic benefit; Mind Wipe's permanent erasure versusUntilDispelled; and Unravel Identity's loss of all class abilities plus false-self belief. The last packet supplies all16 actual class records and their manifest. No foreign monster powers,hidden replacement mechanics or new cosmology facts are adopted.

The casting packet's first copy attempt reached Windows' path-length limit. Its52 partial copied files remain preserved as an incomplete attempt. The repaired own preparer used explicit long paths and a distinct complete output root; its complete archive and every bound source verified successfully. [The recovery receipt]({A}/RANK9_CASTING_COST_5_PACKAGING_RECOVERY_01.json) distinguishes the partial and complete attempts. No original information was removed.

The [current owner decision ledger]({A}/PERTINENT_GPT_DECISIONS_2026_10_20_02.json) remains authoritative for the three-mode Unity direction,continued AI engineering support,Mass Suggestion,True Seeing,scoped Soulburn/Reservoir and preparation-only copied-feat Ready choices. The existing751-check Ready receipt is retained; no downloaded code was executed or canonical helper correction applied. Whole Ready implementation and positive-content holds remain open.

At the latest native observation,Calibration Review Part5 still reported the delivered Rank8Damage6 request active with no completed assistant verdict. Rank7IdentityCasting5 is next; Review continuation part5 remains standby. Source packets are queued,not silently accepted from summaries.

The [manifest]({REPORT}/manifest.json) lists hashes and established locally retained exclusions. Newly encountered archive-depth exclusions receive a separate bounded,read-only recursive inspection; only exact unchanged archives with no policy/credential issue are added. Its [receipt]({REPORT}/NESTED_ARCHIVE_ADDITIONAL_REVIEW.json) records every inspected unique archive/member and the disposition. No archived code is executed. Prior tracked Git entries are retained. Private configuration,unrelated raw browser captures,imported assets,dependencies,external reference books and mixed immutable archives retain their established local-only treatment.

Source preservation,structural validation,authored semantic review,reference arithmetic,engine/runtime testing,human gameplay,balance,cosmology,all75domains,whole-game completion and release approval remain separate. No broad completion follows from these checks or this push.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['PERTINENT_GPT_DECISIONS_2026_10_20_02.json','RANK9_AGENCY_CONTROL_9_SOURCE_CONFERENCE_01_PREPARATION.json','RANK9_TIME_FATE_6_SOURCE_CONFERENCE_01_PREPARATION.json','RANK9_CASTING_COST_5_SOURCE_CONFERENCE_01_PREPARATION.json','RANK9_MEMORY_DENIAL_6_SOURCE_CONFERENCE_01_PREPARATION.json','RANK9_CASTING_COST_5_PACKAGING_RECOVERY_01.json','ACTIVE_AUTHORING_CHECKPOINT_RANK9_MEMORY_DENIAL_57_CHECK.json']}
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],'exactAcceptedButUnappliedIdentities':39,'implementationApplied':False,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    extra_review=(W/'nested-archive-additional-review.json').read_bytes()
    assert digest(extra_review)==plan['additionalArchiveInspection']['receiptSha256']
    extras[f'{REPORT}/NESTED_ARCHIVE_ADDITIONAL_REVIEW.json']=extra_review
    extras[f'{REPORT}/archive-inspection-script.py']=(HERE/'review_nested_archives_backup57.py').read_bytes()
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'newRulesApplied':0}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':p.verify_push}[sys.argv[1]]()
