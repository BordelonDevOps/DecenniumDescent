"""Back up preserved authoring through checkpoint61 without applying proposed mechanics."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('backup46_helpers',HERE/'deliver_progress_2026_10_18_storm_control46.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
h=p.h
G,D,A=p.G,p.D,p.A
BASE='0a9c7b2bc9adc0f6773f2cb64e2dbb3296843ccc'
W=HERE.parent/'audit_work/github-snapshot-2026-10-20-planar-gates61'
REPORT='docs/audit/2026-10-20/github-snapshot-planar-gates61'
STATUS='SNAPSHOT_STATUS_2026-10-20_PLANAR_GATES61.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK9_PLANAR_GATES_61.json'
SCOPE='Preserve checkpoints58-61: the complete Rank8Damage6 proposed return, independent integrity and semantic findings, the unsent bounded correction packet, and full rank9 knowledge/revelation5 and planar/gates5 source conferences. Preserve all histories; no canonical rule, index, helper, runtime or cosmology application. The39 accepted identities remain unapplied.'
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
    q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_50.json')
    assert len(q['groups'])==46 and q['preparedOrActualReviewIdentityCount']==291 and q['originalSourceOrReceiptWorkCount']==32
    checks=[('RANK9_KNOWLEDGE_REVELATION_5_SOURCE_CONFERENCE_01_CHECK.json',373),('RANK9_PLANAR_GATES_5_SOURCE_CONFERENCE_01_CHECK.json',406)]
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
    notice=f'> **Latest development backup — 20 October 2026:** Work through checkpoint 61 is preserved. The Rank 8 damage review has eight outstanding local findings; two new rank-9 source packets remain undecided. Applied counts remain 525 reviewed / 323 pending, with 249 standalone procedures, 173 interfaces and 39 accepted-but-unapplied identities. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup — 20 October 2026

This backup preserves work after `{BASE}` through [checkpoint 61]({CHECKPOINT}). The game is video-game-only. Applied membership remains **525 reviewed / 323 pending / 249 standalone procedures / 173 interfaces**. The 39 accepted identities and proposed Ready/copy corrections remain unapplied under the owner's implementation reservation. This push preserves development evidence; it grants no gameplay or release approval.

The completed Rank8Damage6 return preserves six proposed procedures, 20 decisions, 12 main encounters, 41 branches and 37 reversible full-value operations. Independent integrity and reconstruction review passed 559 checks. Separate local semantic review found eight issues: missing Ready concentration resolution, ineffective cover geometry, incomplete Greater Dispel capture, inconsistent actor/body values, invalid class/feature accounting, an unsupported movement opportunity, inconsistent strain wording, and an ambiguous wall establishment timestamp. Its finite diagnostics report 92 passes and four failures out of 96 checks. The six spells are **not locally accepted or applied**. The complete return, findings, proposed correction request and correction ZIP are preserved; correction dispatch waits for the ongoing Rank 7 response.

Two full source conferences are prepared and remain unsent:

| Conference | Identities | Complete sources | Native placements | Unselected questions | Source checks |
|---|---:|---:|---:|---:|---:|
| Knowledge/revelation | 5 | 126 | 5 | 26 | 373 |
| Planar/gates | 5 | 132 | 7 | 30 | 406 |

These source checks all passed. They establish preservation and packaging, not semantic acceptance or engine execution. The packets contain original source/access/history records, complete actual applied counterparts and full pending comparison archives. Cosmology sources, the saved website and later owner corrections remain distinct; no unselected question creates new canon. Knowledge benefits, truthful answers, permanent gates and fortresses, automatic banishment and planar immunity remain fully represented for review.

[Queue 50](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_50.json) groups 291 pending identities in 46 groups and leaves 32 rank-9 identities ungrouped. All 323 pending identities remain pending. The new bookkeeping checkpoint passed 665 preservation checks, without changing accepted or applied membership.

The [owner decision ledger]({A}/PERTINENT_GPT_DECISIONS_2026_10_20_02.json) retains the SNES-style three-mode game direction, continued AI engineering oversight, Mass Suggestion, True Seeing, scoped Soulburn/Reservoir and preparation-only copied-feat Ready choices. Full Ready implementation and the independent positive-content holds remain open. No downloaded Python was executed and canonical helpers remain unchanged.

The latest native observation reports Calibration Review Part 5 active on the delivered Rank7IdentityCasting5 request, with no completed assistant verdict. Its five identities are Cast Echo, Meta Surge, Erase from Reality, Sequester and Simulacrum. Review continuation part 5 remains standby. The pending Rank8 corrections and rank9 source conferences are not silently reviewed through summaries.

The [manifest]({REPORT}/manifest.json) records hashes and established locally retained exclusions. Newly encountered archive-depth exclusions receive a separate bounded, read-only recursive inspection; exact unchanged archives are included only when that inspection has no policy or credential issue. Its [receipt]({REPORT}/NESTED_ARCHIVE_ADDITIONAL_REVIEW.json) records each inspected archive and member. No archived code is executed. Existing tracked entries are retained. Private configuration, unrelated browser captures, imported assets, dependencies, external reference books and mixed immutable archives retain their established local-only treatment.

Source preservation, structural validation, authored semantic review, arithmetic/geometry checks, engine execution, human gameplay, balance, cosmology, all 75 domains, whole-game completion and release approval remain separate gates.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['PERTINENT_GPT_DECISIONS_2026_10_20_02.json', 'RANK8_DAMAGE6_PART5_RETURN_01_LOCAL_PREFLIGHT.json', 'RANK8_DAMAGE6_PART5_RETURN_01_SEMANTIC_REVIEW_59.json', 'RANK8_DAMAGE6_LOCAL_CORRECTIONS_01_PREPARATION.json', 'GPT_PART5_RANK8_DAMAGE_CORRECTIONS_11_REQUEST.txt', 'RANK9_KNOWLEDGE_REVELATION_5_SOURCE_CONFERENCE_01_PREPARATION.json', 'RANK9_PLANAR_GATES_5_SOURCE_CONFERENCE_01_PREPARATION.json', 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_PLANAR_GATES_61_CHECK.json', 'GPT_PART5_RANK7_LIVE_AT_PLANAR_GATES_61_NATIVE.json'] }
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],'exactAcceptedButUnappliedIdentities':39,'implementationApplied':False,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    extra_review=(W/'nested-archive-additional-review.json').read_bytes()
    assert digest(extra_review)==plan['additionalArchiveInspection']['receiptSha256']
    extras[f'{REPORT}/NESTED_ARCHIVE_ADDITIONAL_REVIEW.json']=extra_review
    extras[f'{REPORT}/archive-inspection-script.py']=(HERE/'review_nested_archives_backup61.py').read_bytes()
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'newRulesApplied':0}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':p.verify_push}[sys.argv[1]]()
