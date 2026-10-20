"""Back up preserved authoring through checkpoint72 without applying proposed mechanics."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('backup46_helpers',HERE/'deliver_progress_2026_10_18_storm_control46.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
h=p.h
G,D,A=p.G,p.D,p.A
BASE='10b299c4af637032f40fab1704f60548ef1a9a1a'
W=HERE.parent/'audit_work/github-snapshot-2026-10-20-material-forging72'
REPORT='docs/audit/2026-10-20/github-snapshot-material-forging72'
STATUS='SNAPSHOT_STATUS_2026-10-20_MATERIAL_FORGING72.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK9_MATERIAL_FORGING_72.json'
SCOPE='Preserve checkpoints66-72: complete Rank7 identity/casting return,independent semantic findings and actual correction dispatch; complete Rank8 correction return02,independent reconciliation and additional Anchor history qualification; full elemental-pets2 and material-forging2 source conferences. Preserve sources,owner choices and histories. No canonical gameplay,index,helper,runtime or cosmology application;39 accepted identities remain unapplied.'
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
    q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_59.json')
    assert len(q['groups'])==51 and q['preparedOrActualReviewIdentityCount']==309 and q['originalSourceOrReceiptWorkCount']==14
    checks=[('RANK9_ELEMENTAL_PETS_2_SOURCE_CONFERENCE_01_CHECK.json',337),('RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_01_CHECK.json',434),('ACTIVE_AUTHORING_CHECKPOINT_RANK9_MATERIAL_FORGING_72_CHECK.json',687)]
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
    notice=f'> **Latest development backup — 20 October 2026:** Work through checkpoint72 is preserved: full Rank7/Rank8 review histories and two new rank9 source packets. Applied525 reviewed/323 pending/249 standalone/173 interfaces and39 accepted-but-unapplied remain unchanged. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup — 20 October 2026

This backup preserves work after `{BASE}` through [checkpoint72]({CHECKPOINT}). Decennium Descent remains video-game-only. Applied membership remains **525 reviewed / 323 pending / 249 standalone procedures / 173 interfaces**. The39 accepted identities and proposed Ready/copy changes remain unapplied under the owner's implementation reservation. This is a development backup, not gameplay or release approval.

The complete Rank7 identity/casting return was preserved and reconstructed with577 independent checks. Local semantic review found three bounded groups: actual Metamagic Adept acquisition, eight Action debits and successful Erase casting history. The full correction12 packet was actually submitted to GPT. At the checkpoint72 observation the browser still showed generation and Stop; no completed correction return was claimed.

The complete Rank8 damage correction Return02 passed1060 independent preservation/reconstruction checks. Its eight original findings were independently reconciled, including the narrow Soul Pyre already-created blast completion after Ready concentration fails. The reconciled semantic report contains334 applicable diagnostics:333 passes and one additional Dimensional Anchor cast-history qualification. The original overstrict paragraph-comparison diagnostic is preserved with its reasoned reconciliation. The full follow-up13 archive is prepared UNSENT until Rank7 finishes. Neither spell cohort is independently accepted or applied.

| New source conference | Identities | Complete sources | Native placements | Unselected questions | Preservation checks |
|---|---:|---:|---:|---:|---:|
| Elemental pets | 2 | 107 | 2 | 24 | 337 |
| Material and forging | 2 | 166 | 2 | 24 | 434 |

Elemental Convergence retains all four actual base pets at once without concentration; Elemental Fusion retains genuine merging,shared statistics and a two-spell benefit with its printed concentration. Matter Conversion retains useful stone-to-mithril conversion; Eternal Forge retains permanent magical weapon or item creation and its unresolved Core dispel relationship. All added choices remain unselected. Exact access,full native sources,actual class records,accepted interfaces,complete applied comparisons and pending conference archives are preserved.

The material/forging conference binds the current **687 reviewed recipes**, all complete linked recipe cards and review records, two complete item examples and full shared body/use/economy profiles. Earlier initial unreviewed-output notes remain historical. Review status grants no automatic recipe knowledge,spell eligibility,free physical host,artifact authority or charge refresh.

[Queue59](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_59.json) groups309 pending identities across51 groups;14 rank9 identities still need source preparation. The323 pending entries include39 accepted-but-unapplied identities. Checkpoint72 bookkeeping passed687 preservation checks. Original manuscripts,saved website,owner cosmology corrections and sealed/public knowledge boundaries remain preserved.

The [owner decision ledger]({A}/PERTINENT_GPT_DECISIONS_2026_10_20_02.json) retains the SNES-style exploration/tactical/resource-management direction,continuing AI engineering assistance,Mass Suggestion,True Seeing,scoped Soulburn/Reservoir and preparation-only copied-feat Ready. Full Ready implementation and independent positive-content holds remain open. No downloaded Python was executed;canonical helpers remain unchanged.

The [manifest]({REPORT}/manifest.json) records exact source hashes and established locally retained exclusions. New archive-depth exclusions receive a separate bounded read-only inspection;its [receipt]({REPORT}/NESTED_ARCHIVE_ADDITIONAL_REVIEW.json) records the result. No archive code is executed. Earlier tracked entries remain preserved. Private configuration,unrelated browser captures,imported assets,dependencies,external reference books and mixed immutable archives retain their established local-only treatment.

Source preservation,structural checks,semantic review,arithmetic/geometry validation,engine execution,human gameplay,balance,cosmology,all75 domains,whole-game completion and release approval remain separate gates.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['PERTINENT_GPT_DECISIONS_2026_10_20_02.json', 'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_SEMANTIC_REVIEW_68.json', 'RANK7_IDENTITY_CASTING5_LOCAL_CORRECTIONS_01_PREPARATION.json', 'GPT_PART5_RANK7_IDENTITY_CORRECTIONS_12_DISPATCH_NATIVE.json', 'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json', 'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_70.json', 'RANK8_DAMAGE6_CAST_HISTORY_CORRECTION_02_PREPARATION.json', 'RANK9_ELEMENTAL_PETS_2_SOURCE_CONFERENCE_01_PREPARATION.json', 'RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_01_PREPARATION.json', 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MATERIAL_FORGING_72_CHECK.json', 'GPT_PART5_RANK7_CORRECTION_STATUS_72.json']}
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],'exactAcceptedButUnappliedIdentities':39,'implementationApplied':False,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    extra_review=(W/'nested-archive-additional-review.json').read_bytes()
    assert digest(extra_review)==plan['additionalArchiveInspection']['receiptSha256']
    extras[f'{REPORT}/NESTED_ARCHIVE_ADDITIONAL_REVIEW.json']=extra_review
    extras[f'{REPORT}/archive-inspection-script.py']=(HERE/'review_nested_archives_backup72.py').read_bytes()
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'newRulesApplied':0}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':p.verify_push}[sys.argv[1]]()
