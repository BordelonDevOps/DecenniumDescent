"""Preserve accepted persistent20 and source/context work through checkpoint17."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('persistent20_delivery_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='3ece00cad106dfda0b86a6e84630b3d3e3253e1e'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-persistent20'
REPORT='docs/audit/2026-10-18/github-snapshot-persistent20'
STATUS='SNAPSHOT_STATUS_2026-10-18_PERSISTENT20.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_PLANAR_CONFERENCE_CONTEXT_17.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for module in [h,h.p]:module.BASE,module.W,module.REPORT,module.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)
SCOPE='Persistent20 actual Exact07 acceptance and verified application;525 reviewed/323 pending,249 standalone procedures,173 interfaces. Full Companion Current04 actually submitted. Mixed rank7 mechanics16 and travel6 source conferences prepared unsent. Current Control15/Illusion14 context,queue12/checkpoint17. No pending adoption or cosmology change.'

def scan():
 h.scan();path=W/'plan.json';plan=json.loads(path.read_bytes());plan.update(ownerInstruction='Preserve progress on GitHub, regularly confer with actual GPT, continue until review completion or20% allowance remains.',scope=SCOPE);path.write_bytes(jsraw(plan))

def assemble():
 plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts']
 assert git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
 expected,paths={},[]
 for row in plan['included']:
  expected[row['path']]=row['gitBlob']
  if row['changedFromBaseline']:
   raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path'];dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw);assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
 index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');assert index['authoredCounts']=={'reviewed':525,'pending':323}
 assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
 names=['PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_ACTUAL_GPT_FINAL.json','PERSISTENT_DAMAGE_20_EXACT07_RETURN_RECEIPT.json','PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_RECEIPT.json','PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_CHECK.json','PERSISTENT20_REGISTRY_QUEUE_06_CHECK.json','COMPANION_LIFE_10_CURRENT_04_ACTUAL_SUBMISSION.json','RANK7_MECHANICS_16_SOURCE_CONFERENCE_01_PREPARATION.json','PLANAR_TRAVEL_6_SOURCE_CONFERENCE_01_PREPARATION.json','CONTROL_ILLUSION_CURRENT_ACCEPTANCE_CONTEXT_01_PREPARATION.json','PLANAR_CONFERENCE_CONTEXT_17_CHECK.json']
 bindings={name:h.p.binding(f'{A}/{name}') for name in names}
 notice=f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 ordinary spells reviewed /323 pending.** Persistent20 exact acceptance and verified application are preserved. Full companion Current04 is under actual GPT review. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
 overlays=[]
 for name in ['README.md','START_HERE.md']:
  raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw);delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered);overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
 status=f'''# Decennium Descent development backup —18 October2026 UTC

Video-game development continues with the actual GPT notebook. This snapshot preserves progress since `{BASE}`: **525 ordinary spells reviewed /323 pending**,249 complete standalone procedures and173 scoped accepted interfaces.

GPT accepted all eight persistent20 Exact07 artifacts unchanged. The actual final and downloaded review archive are preserved. Local application copied the four canonical artifacts byte-for-byte and updated only20 spell memberships, preserving damage25's completed work and every other identity. The application passed1,108 checks. Its sole source-snapshot difference was the already accepted damage25 membership update; no earlier index overwrote that work. All20 procedures,21 placements,40 original scenarios and57 current cases remain available with their real conditional/source limitations. Registry06 retains143 prior interfaces and adds30 scoped persistent entries, including each complete procedure/root mapping. Ice Storm's mixed-defense allocation remains specific to that source.

Full Companion/life10 Current04 was actually submitted to Review Continuation Part4, user turn3215cb75-04cf-48fb-8d6b-9dbc93d04850. The packet contains10 procedures,20 original scenarios,27 current main cases,2 exactCR2 holds and5 explicit questions. No final has been recorded at this checkpoint. The sent message includes persistent20's acceptance and its application intent; successful local application now has its own verified receipt for the next GPT update.

Queue12 retains323 pending identities:112 in15 active/prepared groups and211 other original-source identities. The mixed rank-seven mechanics16 source conference preserves both eight-spell parent preparations and33 genuine questions, with individually assigned tiers1A/12B/3C. The six-spell travel conference follows the verified push and qualified planes review; it preserves77 complete sources,8 placements,17 questions and Blink's unchanged nonoperative receipt case. It uses5C/1B classifications. The original cosmology manuscripts and saved website retain separate authority. Both new packets remain UNSENT and unadopted.

Control15 and Illusion14 Current12 packets remain unchanged. A separate current-acceptance context proves the only live differences are membership/navigation, binds all45 recently accepted identities and preserves the108 old interfaces unchanged within173. Supply that context alongside each original full packet for its actual conference. No source question or preparation count is a completed operational review.

Continue from [checkpoint17]({CHECKPOINT}), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). The map checked1,356 distinct links with none missing. All75 domain gates retain their exact prior status, closure, human evidence and completion class. Authored acceptance does not establish runtime execution, human gameplay, numerical balance, final whole-game flow, cosmology canon or release readiness. Latest observed allowance59% remaining; continue until review completion or20% remains, keeping actual GPT regularly involved.

The [preservation manifest]({REPORT}/manifest.json) records selected hashes and retained local exclusions. Every prior tracked Git entry remains. Existing exclusions retain private configuration, unrelated browser/sidebar captures, third-party books, imported assets, dependencies and mixed archives locally. No source deletion, force push, history rewrite or remote import into the authoring folder occurs.
'''
 delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'status':'Active development; preservation snapshot','scope':SCOPE,'videoGameOnly':True,'authoredSpellCounts':index['authoredCounts'],'activeCheckpoint':h.p.binding(CHECKPOINT),'currentEvidence':bindings,'pendingCohortsAdopted':False,'sourceInformationDeleted':0,'historyRewritten':False,'wholeGameAcceptanceClaimed':False}
 manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
 extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
 for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
 for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
 write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0');print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'counts':index['authoredCounts']}))

def verify_push():
 commit=git('rev-parse','HEAD').decode().strip();remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
 assert commit==remote and git('rev-parse','HEAD^').decode().strip()==BASE and git('status','--porcelain=v1','-z')==b''
 expected=json.loads((W/'expected-staged-blobs.json').read_bytes());tree=h.oldtree(commit);baseline=h.oldtree(BASE)
 assert all(tree.get(n,{}).get('oid')==oid for n,oid in expected.items()) and set(baseline)<=set(tree)
 report=REPORT+'/STAGED_VERIFICATION.json';assert tree[report]['oid']==h.p.blob(lp(D/report).read_bytes());assert set(tree)-set(baseline)-set(expected)=={report}
 receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRoot':str(G),'deliveryRoot':str(D),'baseCommit':BASE,'commit':commit,'remoteMain':remote,'url':f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}','worktreeClean':True,'expectedBlobsVerified':len(expected),'totalCommitEntries':len(tree),'priorTrackedEntriesPreserved':len(baseline),'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'authoredCounts':{'reviewed':525,'pending':323},'developmentContinues':True,'wholeGameCompleted':False,'scope':SCOPE}
 write_new(W/'push-receipt.json',jsraw(receipt));write_new(G/REPORT/'PUSH_RECEIPT.json',jsraw(receipt));print(json.dumps(receipt))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':verify_push}[sys.argv[1]]()
