"""Preserve checkpoints47-48 and actual owner discussions; no gameplay application."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('backup46_helpers',HERE/'deliver_progress_2026_10_18_storm_control46.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
h=p.h
G,D,A=p.G,p.D,p.A
BASE='ccb9047a76e9807250feee6d72285c268957d20b'
W=HERE.parent/'audit_work/github-snapshot-2026-10-20-owner-direction48'
REPORT='docs/audit/2026-10-20/github-snapshot-owner-direction48'
STATUS='SNAPSHOT_STATUS_2026-10-20_OWNER_DIRECTION48.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_GPT_OWNER_DIRECTION_48.json'
SCOPE='Preserve rank9 psychic/fear7, copied-feat return01 and supplement02, actual owner decisions, three-mode SNES-style CRPG direction and checkpoint48. No canonical mechanic/index/runtime application; all history retained.'
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
    q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_39.json')
    assert len(q['groups'])==37 and q['preparedOrActualReviewIdentityCount']==234 and q['originalSourceOrReceiptWorkCount']==89
    for name,count in [('COPIED_FEAT_PART5_RETURN_01_LOCAL_PREFLIGHT.json',108),('COPIED_FEAT_PART5_SUPPLEMENT_02_LOCAL_PREFLIGHT.json',156)]:
        v=h.p.read(f'{A}/{name}');assert v['checkCount']==count and v['failures']==0 and not v['implementationApplied']
    expected={};paths=[]
    for row in plan['included']:
        expected[row['path']]=row['gitBlob']
        if row['changedFromBaseline']:
            raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path']
            target=lp(D/row['path']);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            assert digest(target.read_bytes())==row['sha256'];paths.append(row['path'])
    notice=f'> **Latest development backup —20 October2026:** Work through checkpoint48 is preserved. SNES-style CRPG: direct-control exploration, deep tactical combat and companion-driven resource management. Copied-feat Ready uses preparation-round-only allowances; exact successor review is active. Implementation remains reserved;525 reviewed/323 pending,249 standalone,173 interfaces,39 accepted-but-unapplied. See [snapshot status]({STATUS}). Older statements remain history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup —20 October2026

This backup preserves saved work after {BASE} through [checkpoint48]({CHECKPOINT}). Applied accounting remains525 reviewed/323 pending/249 standalone/173 interfaces;39 accepted spell identities remain unapplied. The owner's implementation reservation remains in force.

The [new decision ledger]({A}/PERTINENT_GPT_DECISIONS_2026_10_20_01.json) preserves actual discussions in Calibration Review Part5 and Unity Development Setup. Owner direction is an SNES-style CRPG combining direct-control exploration, deep tactical combat and companion-driven crafting/research/gathering, with sustained AI engineering and rules oversight and the owner retaining design authority. Shared Unity/C# simulation and a connected first playable loop are GPT architecture recommendations; exact time, traversal and implementation choices remain distinct.

The owner confirmed shared24-hour Mass Suggestion without an added consumed reagent and consistent True Seeing benefits across legitimate access. GPT's delegated Soulburn/Grand Reservoir recovery choice remains scoped. Copied-feat Ready now spends applicable allowances only at preparation; the old both-round proposal is superseded. GPT received the exact successor request; no rule changes have been applied.

The complete copied-feat Return01 and Supplement02 archives are preserved. Local verification passed108 and156 integrity/source/text checks respectively. Supplement02 corrects inactive healing-reducer rejection and preserves shared-buffer expiry instructions in proposed helper code. Active-source consumption and downstream choice/removal still require implementation. GPT-reported executable results are distinguished from our local text verification; no downloaded code was run.

The rank9 psychic/fear7 source packet retains84 complete sources,10 placements,23 unselected questions and303 source checks. Queue39 groups234 pending identities in37 groups, leaving89 ungrouped rank9 identities. Source preparation does not approve mechanics or cosmology.

The [manifest]({REPORT}/manifest.json) records hashed sources and established locally retained exclusions. All prior tracked Git entries remain; no deletions or force push. Private configuration, unrelated browser captures, imported assets, external reference books and mixed immutable archives remain local under the existing backup policy. All75-domain, engine/runtime, human-play, balance, cosmology, whole-game and release gates remain separate.
'''
    evidence={n:h.p.binding(f'{A}/{n}') for n in ['PERTINENT_GPT_DECISIONS_2026_10_20_01.json','COPIED_FEAT_PART5_RETURN_01_LOCAL_PREFLIGHT.json','COPIED_FEAT_PART5_SUPPLEMENT_02_LOCAL_PREFLIGHT.json','RANK9_PSYCHIC_FEAR_7_SOURCE_CONFERENCE_01_PREPARATION.json','GPT_PART5_OWNER_READY_SUCCESSOR_08_NATIVE.json']}
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],'exactAcceptedButUnappliedIdentities':39,'implementationApplied':False,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'newRulesApplied':0}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':p.verify_push}[sys.argv[1]]()

