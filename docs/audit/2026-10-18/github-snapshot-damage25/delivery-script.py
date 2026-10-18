"""Preservation snapshot through damage25 acceptance and source conferences15."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('damage25_delivery_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='19423ad41f9d66ec95121c671fcaf01c9798db29'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-damage25'
REPORT='docs/audit/2026-10-18/github-snapshot-damage25'
STATUS='SNAPSHOT_STATUS_2026-10-18_DAMAGE25.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_SOURCE_CONFERENCES_15.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for module in [h,h.p]:module.BASE,module.W,module.REPORT,module.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)
SCOPE='Damage25 actual exact10 acceptance and byte-identical application,505 reviewed/343 pending,229 standalone,143 interfaces; persistent20 exact07 actual submission; Information8/Eye1/Evocation8 source conferences,queue10/checkpoint15. All pending packets remain unadopted.'

def scan():
 h.scan();path=W/'plan.json';plan=json.loads(path.read_bytes())
 plan.update(ownerInstruction='Preserve progress on GitHub, keep actual GPT involved, continue until review completion or20% allowance remains.',scope=SCOPE);path.write_bytes(jsraw(plan))

def assemble():
 plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts']
 assert git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
 expected,paths={},[]
 for row in plan['included']:
  expected[row['path']]=row['gitBlob']
  if row['changedFromBaseline']:
   raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path']
   dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
   assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
 index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');assert index['authoredCounts']=={'reviewed':505,'pending':343}
 assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
 bindings={name:h.p.binding(f'{A}/{name}') for name in ['DAMAGE_CONTROL_25_EXACT_REBOUND_10_ACTUAL_GPT_FINAL.json','DAMAGE_CONTROL_25_EXACT10_RETURN_RECEIPT.json','DAMAGE_CONTROL_25_EXACT10_APPLICATION_RECEIPT.json','DAMAGE_CONTROL_25_EXACT10_APPLICATION_CHECK.json','DAMAGE25_REGISTRY_QUEUE_05_CHECK.json','PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_ACTUAL_SUBMISSION.json','INFORMATION_8_CONFERENCE_01_PREPARATION.json','EYE_JUDGEMENT_1_CONFERENCE_01_PREPARATION.json','EVOCATION_RANK7_8_CONFERENCE_01_PREPARATION.json','SOURCE_CONFERENCES_15_CHECK.json']}
 notice=f'> **Latest development backup —18 October2026 UTC:** Video-game-only. **505 ordinary spells reviewed /343 pending.** Damage/control25 exact acceptance and verified application are preserved. Persistent20 remains under actual GPT review; companion and source packets remain pending. See [snapshot status]({STATUS}). Earlier notices are retained history.\n\n'
 overlays=[]
 for name in ['README.md','START_HERE.md']:
  raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw)
  delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered);overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
 status=f'''# Decennium Descent development backup —18 October2026 UTC

Video-game development continues with the actual GPT notebook. This snapshot preserves work since `{BASE}`. **505 ordinary spells reviewed /343 pending**,229 standalone procedures and143 scoped accepted interfaces. The review has not established runtime execution, human gameplay, numerical balance, whole-game flow, cosmology approval or release readiness.

GPT accepted all eight damage/control25 Exact10 artifacts unchanged. The actual return archive and final message are preserved. Local application copied four canonical artifacts byte-for-byte, updated only the25 exact memberships and associated discovery records, and passed1,039 application checks with zero source-snapshot drift. All25 procedures,26 placements,70 authored cases,36 original scenarios and77 complete sources remain available. The cases retain their actual scope limitations; numerical checks are not runtime tests. All108 prior interfaces remain identical, with35 newly indexed damage25 entries. Meteor Spear's mixed-defense rule remains source-specific; the Fate presentation whitelist is unchanged.

Persistent20 Exact07 was actually submitted in Review Continuation Part4 and was still under review at the snapshot boundary. Its frozen480/368 membership snapshot remains historical; the current505/343 index is authoritative. The twenty spells are not adopted without their own verified exact final. Companion Current04,27 main cases,two exactCR2 holds and five questions remains the next full conference. GPT has received its progress summary, not the full packet.

Queue10 retains343 pending identities:118 in15active/prepared groups and225 other source/receipt items. Information8 and Eye of Judgement1 preserve all nine remaining earlier complete proposals, eighteen original cases and31 questions. The new rank-seven Evocation8 packet contains eight source-only records and16 questions; no earlier complete procedures or worked cases are claimed. All three new source conferences remain UNSENT. Preparing questions does not approve mechanics.

Continue from [checkpoint15]({CHECKPOINT}), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). The map checked1,344 distinct links with none missing. All75 domain gates are unchanged. The latest observed allowance was62% remaining; continue until review completion or20% remains, keeping actual GPT regularly involved.

The [preservation manifest]({REPORT}/manifest.json) records selected source hashes and locally retained exclusions. Every prior tracked Git entry is retained. Established exclusions keep private configuration, unrelated browser/sidebar captures, third-party source books, imported assets, dependencies and mixed archives containing excluded material local. No source deletion, force push, history rewrite or remote import into the authoring folder occurs.
'''
 delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'status':'Active development; preservation snapshot','scope':SCOPE,'videoGameOnly':True,'authoredSpellCounts':index['authoredCounts'],'activeCheckpoint':h.p.binding(CHECKPOINT),'currentEvidence':bindings,'pendingCohortsAdopted':False,'sourceInformationDeleted':0,'historyRewritten':False,'wholeGameAcceptanceClaimed':False}
 manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
 extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
 for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
 for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
 write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
 print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'counts':index['authoredCounts']}))

def verify_push():
 commit=git('rev-parse','HEAD').decode().strip();remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
 assert commit==remote and git('rev-parse','HEAD^').decode().strip()==BASE
 assert git('status','--porcelain=v1','-z')==b''
 expected=json.loads((W/'expected-staged-blobs.json').read_bytes());tree=h.oldtree(commit);baseline=h.oldtree(BASE)
 assert all(tree.get(n,{}).get('oid')==oid for n,oid in expected.items());assert set(baseline)<=set(tree)
 report=REPORT+'/STAGED_VERIFICATION.json';assert tree[report]['oid']==h.p.blob(lp(D/report).read_bytes())
 assert set(tree)-set(baseline)-set(expected)=={report}
 receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRoot':str(G),'deliveryRoot':str(D),'baseCommit':BASE,'commit':commit,'remoteMain':remote,'url':f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}','worktreeClean':True,'expectedBlobsVerified':len(expected),'totalCommitEntries':len(tree),'priorTrackedEntriesPreserved':len(baseline),'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'authoredCounts':{'reviewed':505,'pending':343},'developmentContinues':True,'wholeGameCompleted':False,'scope':SCOPE}
 write_new(W/'push-receipt.json',jsraw(receipt));write_new(G/REPORT/'PUSH_RECEIPT.json',jsraw(receipt));print(json.dumps(receipt))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':verify_push}[sys.argv[1]]()
