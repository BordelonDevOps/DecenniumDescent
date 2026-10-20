"""Back up preserved authoring through checkpoint52 without applying proposed mechanics."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('backup46_helpers',HERE/'deliver_progress_2026_10_18_storm_control46.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
h=p.h
G,D,A=p.G,p.D,p.A
BASE='7f31e24274b216470ccce57d4e456d7bdc585961'
W=HERE.parent/'audit_work/github-snapshot-2026-10-20-ward-control52'
REPORT='docs/audit/2026-10-20/github-snapshot-ward-control52'
STATUS='SNAPSHOT_STATUS_2026-10-20_WARD_CONTROL52.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK9_WARD_CONTROL_52.json'
SCOPE='Preserve checkpoints49-52, full rank9 death/recovery7, defense/form8 and ward/control6 source conferences, the verified preparation-only copied-Ready proposed successor, owner ledger02 and reconciled Unity design direction. No canonical mechanic/index/runtime application; all prior history retained.'
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
    q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_43.json')
    assert len(q['groups'])==40 and q['preparedOrActualReviewIdentityCount']==255 and q['originalSourceOrReceiptWorkCount']==68
    checks=[('COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json',751),('RANK9_DEATH_RECOVERY_7_SOURCE_CONFERENCE_01_CHECK.json',265),('RANK9_DEFENSE_FORM_8_SOURCE_CONFERENCE_01_CHECK.json',312),('RANK9_WARD_CONTROL_6_SOURCE_CONFERENCE_01_CHECK.json',319)]
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
    notice=f'> **Latest development backup — 20 October 2026:** Work through checkpoint 52 is preserved. The preparation-only copied-Ready proposal passed 751 local structural/reconstruction checks and remains unapplied. Three new rank-9 source conferences cover 21 identities. Applied counts remain 525 reviewed / 323 pending, with 249 standalone procedures, 173 interfaces and 39 accepted-but-unapplied identities. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup — 20 October 2026

This backup preserves saved work after `{BASE}` through [checkpoint 52]({CHECKPOINT}). Applied accounting remains **525 reviewed / 323 pending / 249 standalone procedures / 173 interfaces**. The 39 accepted spell identities remain unapplied under the owner's implementation reservation.

The [current decision ledger]({A}/PERTINENT_GPT_DECISIONS_2026_10_20_02.json) retains the actual owner discussions: an SNES-style CRPG with direct-control exploration, deep tactical combat and companion-driven crafting, research and gathering. The owner directs design while AI supplies continuing engineering, rules review and testing assistance. Shared C# simulation and Unity presentation remain architecture proposals; exact timing, traversal and encounter-transition policies still require reconciliation.

The owner's four settled choices remain recorded: shared 24-hour nonconcentration Mass Suggestion without an added consumed reagent; consistent printed True Seeing benefits across legitimate access; preparation-only copy allowances; and the scoped Soulburn/Grand Reservoir recovery choice. The Unity design assessment now points to this direction while retaining its complete original bytes as history.

The [complete preparation-only Ready successor]({A}/copy-ready-preparation-only-part5-successor-01/CODEX_HANDOFF.md) has been downloaded, preserved and checked locally. **751 local checks passed** across manifest integrity, actual source bindings, complete forward/inverse reconstruction, retained native data, 42 case-data traces and 160 declared expectations. These are structural and specification-data checks, not game-runtime or action-reachability tests. Downloaded code was not executed. The full archive, baselines, successor files, exact operations and original examples remain preserved.

`COPY-READY-ALLOWANCE-02` applies only to the seven scoped copied-feat profiles. Applicable feat and actually owned Mirrorsage allowances are spent at preparation. A valid release consumes its real Reaction and paid hold without a second copy allowance or payment/history transaction. Actual trigger, source, target, concentration, Action and expiry restrictions remain. The 30-operation proposal path and alternative 26-operation original-feat path are alternatives, never cumulative. Control successor14 changes references and metadata only; all 15 Control spell objects and their full cases remain unchanged. Full Ready, native transitions and remaining positive-content holds are still open.

Three complete rank-9 source conferences were prepared without selecting their open rules:

| Conference | Identities | Full sources | Native placements | Open questions | Local source checks |
|---|---:|---:|---:|---:|---:|
| Death/recovery | 7 | 74 | 10 | 22 | 265 |
| Defense/form | 8 | 87 | 8 | 26 | 312 |
| Ward/control | 6 | 91 | 7 | 24 | 319 |

Each preserves source text, access, histories, complete counterparts and scoped consequential questions. Queue43 groups 255 pending identities in 40 groups and leaves 68 rank-9 identities ungrouped. Source preparation is not semantic acceptance or cosmology adoption.

At the latest observed GPT check, **Calibration Review Part 5** was still responding to the delivered Rank8Damage6 conference. Rank7IdentityCasting5 follows. The separately named **Review continuation part 5** remains on standby. This backup makes no claim that either conference has completed.

The [manifest]({REPORT}/manifest.json) records hashed sources and established locally retained exclusions. The complete Ready return initially reached the generic nested-archive inspection limit; a separate bounded read-only inspection of all 17 nested archive occurrences and 767 member occurrences found no policy or credential issues, so its original bytes are included. The [additional inspection receipt]({REPORT}/READY_ARCHIVE_ADDITIONAL_REVIEW.json) preserves that evidence. All prior tracked Git entries remain. Private configuration, unrelated raw browser captures, imported assets, dependencies, external reference books and mixed immutable archives remain local under the existing backup policy. No source information is deleted. All 75-domain, engine/runtime, human-play, balance, cosmology, whole-game and release gates remain separate.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['PERTINENT_GPT_DECISIONS_2026_10_20_02.json','COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json','RANK9_DEATH_RECOVERY_7_SOURCE_CONFERENCE_01_PREPARATION.json','RANK9_DEFENSE_FORM_8_SOURCE_CONFERENCE_01_PREPARATION.json','RANK9_WARD_CONTROL_6_SOURCE_CONFERENCE_01_PREPARATION.json','GPT_DIRECTION_AND_UNITY_ASSESSMENT_RECONCILIATION_50.json','ACTIVE_AUTHORING_CHECKPOINT_RANK9_WARD_CONTROL_52_CHECK.json']}
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],'exactAcceptedButUnappliedIdentities':39,'implementationApplied':False,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    extra_review=(W/'ready-archive-additional-review.json').read_bytes()
    assert digest(extra_review)==plan['separatelyReviewedArchives'][0]['receiptSha256']
    extras[f'{REPORT}/READY_ARCHIVE_ADDITIONAL_REVIEW.json']=extra_review
    extras[f'{REPORT}/archive-inspection-script.py']=(HERE/'review_ready_archive_backup52.py').read_bytes()
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'newRulesApplied':0}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':p.verify_push}[sys.argv[1]]()
