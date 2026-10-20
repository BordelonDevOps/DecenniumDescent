"""Back up preserved authoring through checkpoint65 without applying proposed mechanics."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('backup46_helpers',HERE/'deliver_progress_2026_10_18_storm_control46.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
h=p.h
G,D,A=p.G,p.D,p.A
BASE='111a098b52763862ac4c98f7803e8c1d556668e2'
W=HERE.parent/'audit_work/github-snapshot-2026-10-20-illusion-reality65'
REPORT='docs/audit/2026-10-20/github-snapshot-illusion-reality65'
STATUS='SNAPSHOT_STATUS_2026-10-20_ILLUSION_REALITY65.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK9_ILLUSION_REALITY_65.json'
SCOPE='Preserve checkpoints62-65 and three full source conferences: rank9 summon-hosts5,impact-exile4 and illusion-reality5. Preserve original histories,owner choices,complete comparison evidence and unresolved questions. No canonical rule,index,helper,runtime or cosmology application;39 accepted identities remain unapplied.'
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
    q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_53.json')
    assert len(q['groups'])==49 and q['preparedOrActualReviewIdentityCount']==305 and q['originalSourceOrReceiptWorkCount']==18
    checks=[('RANK9_SUMMON_HOSTS_5_SOURCE_CONFERENCE_01_CHECK.json',579),('RANK9_IMPACT_EXILE_4_SOURCE_CONFERENCE_01_CHECK.json',452),('RANK9_ILLUSION_REALITY_5_SOURCE_CONFERENCE_01_CHECK.json',485)]
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
    notice=f'> **Latest development backup — 20 October 2026:** Work through checkpoint 65 is preserved. Three new rank-9 source conferences remain undecided. Applied counts remain 525 reviewed / 323 pending, with 249 standalone procedures, 173 interfaces and 39 accepted-but-unapplied identities. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup — 20 October 2026

This backup preserves work after `{BASE}` through [checkpoint65]({CHECKPOINT}). Decennium Descent remains video-game-only. Applied membership remains **525 reviewed / 323 pending / 249 standalone procedures / 173 interfaces**. The39 accepted identities and proposed Ready/copy changes remain unapplied under the owner's implementation reservation. This is a development backup, not gameplay or release approval.

Three complete source conferences were prepared since the preceding backup:

| Conference | Identities | Complete sources | Native placements | Unselected questions | Preservation checks |
|---|---:|---:|---:|---:|---:|
| Summon/hosts | 5 | 210 | 5 | 32 | 579 |
| Impact/exile | 4 | 149 | 4 | 26 | 452 |
| Illusion/reality | 5 | 157 | 5 | 31 | 485 |

All listed checks passed. They verify source/access/history preservation and packaging, not selected mechanics or engine execution. The full packets include complete applied comparisons, pending comparison archives and original questions. Summon hosts retain actual avatar/army/herald capabilities and full bestiary evidence. Impact/exile retains damage, Stunned, lift/Falling, resistance bypass, Prone and banishment. Illusion/reality retains broad belief-based spell imitation, two-roll attacks, the50percent miss ambiguity, substantive partial reality and a three-round self-reflection fight. No question is silently resolved by analogy.

[Queue53](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_53.json) groups305 pending identities across49 groups;18 rank9 identities still need source packets. The323 pending entries include39 accepted-but-unapplied identities. Current bookkeeping passed672 preservation checks. Original manuscripts, saved website, owner cosmology corrections and sealed/public knowledge boundaries remain preserved.

The completed Rank8Damage6 proposed return remains unaccepted with eight local findings. Its complete correction archive and request remain queued until the current Rank7 response is received. The latest successful native Rank7 observation is checkpoint64; fresh native reads at65 returned Too many requests. The browser still displayed a Stop control and no final response. A transient observation failure is not evidence the review stopped, and no interruption or replacement request was sent.

The [owner decision ledger]({A}/PERTINENT_GPT_DECISIONS_2026_10_20_02.json) retains the SNES-style exploration/tactical/resource-management direction, continuing AI engineering assistance, Mass Suggestion, True Seeing, scoped Soulburn/Reservoir and preparation-only copied-feat Ready. Full Ready implementation and independent positive-content holds remain open. No downloaded Python was executed, and canonical helpers remain unchanged.

The [manifest]({REPORT}/manifest.json) records exact source hashes and established locally retained exclusions. Any new archive-depth exclusions receive a separate bounded read-only inspection; its [receipt]({REPORT}/NESTED_ARCHIVE_ADDITIONAL_REVIEW.json) records the result. No archive code is executed. Existing tracked entries remain preserved. Private configuration, unrelated browser captures, imported assets, dependencies, external reference books and mixed immutable archives retain their established local-only treatment.

Source preservation, structural checks, semantic review, arithmetic/geometry validation, engine execution, human gameplay, balance, cosmology, all75 domains, whole-game completion and release approval remain separate gates.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['PERTINENT_GPT_DECISIONS_2026_10_20_02.json', 'RANK8_DAMAGE6_PART5_RETURN_01_SEMANTIC_REVIEW_59.json', 'RANK8_DAMAGE6_LOCAL_CORRECTIONS_01_PREPARATION.json', 'GPT_PART5_RANK8_DAMAGE_CORRECTIONS_11_REQUEST.txt', 'RANK9_SUMMON_HOSTS_5_SOURCE_CONFERENCE_01_PREPARATION.json', 'RANK9_IMPACT_EXILE_4_SOURCE_CONFERENCE_01_PREPARATION.json', 'RANK9_ILLUSION_REALITY_5_SOURCE_CONFERENCE_01_PREPARATION.json', 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_ILLUSION_REALITY_65_CHECK.json', 'GPT_PART5_RANK7_BROWSER_STATUS_65.json', 'GPT_PART5_RANK7_LIVE_AT_IMPACT_EXILE_64_NATIVE.json']}
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],'exactAcceptedButUnappliedIdentities':39,'implementationApplied':False,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    extra_review=(W/'nested-archive-additional-review.json').read_bytes()
    assert digest(extra_review)==plan['additionalArchiveInspection']['receiptSha256']
    extras[f'{REPORT}/NESTED_ARCHIVE_ADDITIONAL_REVIEW.json']=extra_review
    extras[f'{REPORT}/archive-inspection-script.py']=(HERE/'review_nested_archives_backup65.py').read_bytes()
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'newRulesApplied':0}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':p.verify_push}[sys.argv[1]]()
