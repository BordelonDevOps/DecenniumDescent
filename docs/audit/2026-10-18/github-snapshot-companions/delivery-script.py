"""Preserve current companion authorship and source conferences without promotion."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('companion_delivery_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='dcf2fc47a507795d093745968d37c8934cc98368'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-companions'
REPORT='docs/audit/2026-10-18/github-snapshot-companions'
STATUS='SNAPSHOT_STATUS_2026-10-18_COMPANIONS.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_COMPANION_CURRENT_DRAFT_13.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for module in [h,h.p]:module.BASE,module.W,module.REPORT,module.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)

def scan():
    h.scan();path=W/'plan.json';plan=json.loads(path.read_bytes())
    plan.update(ownerInstruction='Preserve progress on GitHub, keep actual GPT involved, and continue until review completion or20% allowance remains.',scope='Actual companion conference receipt/applied layer, Current03/04 cases and five questions, new source conferences, damage25 exact10 actual submission, queue08/checkpoint13. No pending spell adoption.')
    path.write_bytes(jsraw(plan))

def assemble():
    plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts']
    assert git('status','--porcelain=v1','-z')==b''
    assert git('rev-parse','HEAD').decode().strip()==BASE
    expected,paths={},[]
    for row in plan['included']:
        expected[row['path']]=row['gitBlob']
        if row['changedFromBaseline']:
            raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path']
            dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
            assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
    index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts']=={'reviewed':480,'pending':368}
    assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
    bindings={name:h.p.binding(f'{A}/{name}') for name in [
        'COMPANION_LIFE_10_CONFERENCE_01_RECEIPT.json','COMPANION_LIFE_10_CONFERENCE_APPLIED_02.json',
        'COMPANION_LIFE_10_CURRENT_04_PREPARATION.json','COMPANION_LIFE_10_CURRENT_04_LOCAL_DELTAS.json',
        'COMPANION_LIFE_10_CURRENT_04_PREFLIGHT.json','ILLUSION_PERCEPTION_14_CONFERENCE_12_PREPARATION.json',
        'BODY_DEFENSE_8_CONFERENCE_01_PREPARATION.json','TIME_CAST_5_CONFERENCE_01_PREPARATION.json',
        'TRANSPORT_6_CONFERENCE_01_PREPARATION.json','MAGIC_MODIFIERS_7_CONFERENCE_01_PREPARATION.json',
        'LIFE_MATTER_5_CONFERENCE_01_PREPARATION.json','DAMAGE_CONTROL_25_EXACT_REBOUND_10_ACTUAL_SUBMISSION.json',
        'REMAINING_WORK_QUEUE_08_CHECK.json','COMPANION_CURRENT_DRAFT_13_NAVIGATION_CHECK.json']}
    notice=f'> **Latest development backup —18 October2026 UTC:** Video-game development continues with actual GPT. **480 ordinary spells reviewed /368 pending.** Companion Current04,27 authored cases and five explicit questions are preserved alongside all earlier sources. See [snapshot status]({STATUS}). Earlier notices below are retained history.\n\n'
    overlays=[]
    for name in ['README.md','START_HERE.md']:
        raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
        delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered)
        overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
    status=f'''# Decennium Descent development backup —18 October2026 UTC

Active video-game development continues with the actual GPT notebook. This snapshot preserves work since `{BASE}`. Ordinary spell accounting remains **480 reviewed /368 pending**, with204 complete standalone procedures and108 accepted interfaces. No pending cohort is adopted by this backup.

Companion/life10’s actual Conference01 final and returned archive are preserved. Its eleven additions were replayed into a new layer and reversed exactly. Current03/04 now contain27 main authored cases covering all20 original obligations plus seven supplemental cases. The two positive Command Undeath cases remain conditional because no full authoritative exactCR2 Undead profile has been supplied. Five explicit questions concern Soulburn/GrandReservoir, Wraith handling and physical mass, Ghast cone geometry, and the missing NPC profile. These are unsent authorship drafts, not final exact acceptance. The335 initial and92 subsequent local checks cover integrity, source access, selected arithmetic/geometry and preservation, not game execution.

Current04 preserves three complete local before/after repairs: actual Ghast padded armor and its real AC/proficiency effects, a fully specified countering Wizard and range, and a genuinely paid command preceding a readied suppression release. All ten full returned procedures, original source/access records, twenty historical scenario texts and every prior version remain retained. Shared companion ownership, command limits, real cargo, corpse matter, ordinary/Null endings and distinct suppression branches remain source-specific.

The source-conference queue also preserves illusion14 conference12, body/defense8, time/casting5, transport6, magic-modifiers7 and life/matter5, including original complete proposals and unresolved design choices. Damage/control25 exact10 is actually submitted to Review Continuation Part4 and was still actively generating at this snapshot boundary. No acceptance is inferred. Persistent20 exact07 remains ready for the next actual exchange unless the returned damage25 findings require priority.

Continue from the [active checkpoint]({CHECKPOINT}), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). Queue08 keeps126 pending identities in13 development groups, nine other earlier complete proposals and233 source/receipt work items. Navigation checked1,332 distinct links with none missing. All75 domain gates retain their actual status, human-evidence and closure requirements.

The [preservation manifest]({REPORT}/manifest.json) records selected file hashes and locally retained exclusions. Every prior tracked Git entry is retained. Established exclusions keep private configuration, unrelated browser/sidebar captures, third-party source books, imported assets, dependencies and excluded mixed archives local. No source deletion, force push or remote import into the authoring folder occurs.

This backup does not establish runtime implementation, human playtesting, balance, cosmology/canon, whole-game flow or release approval. Continue actual GPT collaboration until review completion or20% allowance remains; the latest observed allowance was65% remaining.
'''
    delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'status':'Active development; preservation snapshot','videoGameOnly':True,'authoredSpellCounts':index['authoredCounts'],'activeCheckpoint':h.p.binding(CHECKPOINT),'currentEvidence':bindings,'pendingCohortsAdopted':False,'sourceInformationDeleted':0,'historyRewritten':False,'wholeGameAcceptanceClaimed':False}
    manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
    extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
    for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
    for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
    write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
    print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'counts':index['authoredCounts']}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify}[sys.argv[1]]()
