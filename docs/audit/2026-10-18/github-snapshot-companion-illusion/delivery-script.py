"""Preserve companion exact05, active illusion review and source work through checkpoint19."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('companion_illusion_delivery_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='032bc7e33d941d7e635efa8b9a8b060f9f1742f8'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-companion-illusion'
REPORT='docs/audit/2026-10-18/github-snapshot-companion-illusion'
STATUS='SNAPSHOT_STATUS_2026-10-18_COMPANION_ILLUSION.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_COMPANION_EXACT_ILLUSION_ACTIVE_19.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for module in [h,h.p]:module.BASE,module.W,module.REPORT,module.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)
SCOPE='Actual Companion04 final and nine-operation Current05 replay, complete exact05 package UNSENT; actual Illusion14 Current12 plus current acceptance context submitted. Vitality/matter10 source conference and bounded CR2 source search. Queue14/checkpoint19.525 reviewed/323 pending,249 standalone,173 interfaces unchanged. No pending adoption or cosmology change.'

def scan():
 h.scan();p=W/'plan.json';plan=json.loads(p.read_bytes());plan.update(ownerInstruction='Preserve progress on GitHub, regularly confer with actual GPT, continue until review completion or20% allowance remains.',scope=SCOPE);p.write_bytes(jsraw(plan))

def assemble():
 plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts'];assert git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
 expected,paths={},[]
 for row in plan['included']:
  expected[row['path']]=row['gitBlob']
  if row['changedFromBaseline']:
   raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path'];dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw);assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
 index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');assert index['authoredCounts']=={'reviewed':525,'pending':323};assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
 names=['COMPANION_LIFE_10_CURRENT_04_ACTUAL_GPT_FINAL.json','COMPANION_LIFE_10_CURRENT_04_RETURN_RECEIPT.json','COMPANION_LIFE_10_CURRENT_05_REPLAY_CHECK.json','COMPANION_LIFE_10_CURRENT_05_PROPOSAL_APPLICATION.json','COMPANION_LIFE_10_EXACT_05_PREPARATION.json','COMPANION_LIFE_10_EXACT_05_CHECK.json','ILLUSION_PERCEPTION_14_CONFERENCE_12_ACTUAL_SUBMISSION.json','COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_01.json','VITALITY_MATTER_10_SOURCE_CONFERENCE_01_PREPARATION.json','COMPANION_EXACT_ILLUSION_ACTIVE_19_CHECK.json'];bindings={n:h.p.binding(f'{A}/{n}') for n in names}
 notice=f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 ordinary spells reviewed /323 pending.** Companion Current04 decisions are preserved in a complete exact05 draft awaiting review; Illusion14 is under actual GPT review. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n';overlays=[]
 for name in ['README.md','START_HERE.md']:
  raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw);delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered);overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
 status=f'''# Decennium Descent development backup —18 October2026 UTC

Video-game development continues with the actual GPT notebook. This snapshot preserves progress since `{BASE}`. Membership remains **525 ordinary spells reviewed /323 pending**,249 complete standalone procedures and173 scoped accepted interfaces.

The actual Companion/life10 Current04 final is preserved with its verified eight-file returned archive. All nine proposed operations replay and reverse exactly into Current05, with308 checks passing. Codex concurs for drafting with the four explicit choices for Soulburn/Grand Reservoir, wraith handling, wraith mass and Ghast cone, plus the Ready-field timing repair. The complete exact05 package has eight current files: all ten selected full procedures, six shared rules, four scoped new choices,20 original scenarios,27 main cases and38 independent branches.158 source/render/package checks pass.108 current source files and63 exact historical files are supplied separately. This packet remains UNSENT and unadopted at the snapshot.

Both positive Command Undeath cases retain whole-case content holds. The spell requires exactCR2, not a lower rating or an unrated conjured profile. A bounded search preserved11 JSON bestiary sources:9 parseable and2 already-truncated historical files. No exactCR2 Undead was found in the parseable subset. This is not whole-archive absence, and no NPC rating was invented. A separate complete native NPC/rating review remains required.

Illusion/perception14 Current12 and the current acceptance context were actually submitted together to Review Continuation Part4, user turn99c03218-f9ed-4545-8792-d4d87ec6e4fb. GPT is visibly reviewing full cases. No final or approval is inferred. Its update includes accepted persistent20, the earlier verified backup and the companion return/integration plan. Companion's completed replay and exact package are queued for the next handoff.

Vitality/matter10 source preparation supplies73 complete sources,10 placements and25 explicit questions with5B/5C classifications. No complete earlier operational procedures or cases exist for those ten identities; no new rule is adopted by preparation. Travel6, mixed rank7 mechanics16 and the other prepared conferences retain their individual unsubmitted status. The ward7 question draft is preliminary preparation only.

Continue from [checkpoint19]({CHECKPOINT}), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). Queue14 retains323 pending identities:122 in16 active/prepared groups and201 ungrouped.447 navigation checks and1,364 distinct links pass with no missing link. All75 domain rows remain unchanged. Authored review is distinct from runtime implementation/testing, human gameplay, numerical balance, cosmology, whole-game flow and release. Latest observed allowance55% remaining; continue until review completes or20% remains.

The [preservation manifest]({REPORT}/manifest.json) records selected hashes and locally retained exclusions. Every prior tracked entry remains. Existing exclusions preserve private configuration, unrelated browser/sidebar captures, third-party books, imported assets, dependencies and mixed archives locally. No source deletion, force push, history rewrite or remote import into the authoring folder occurs.
'''
 delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'status':'Active development; preservation snapshot','scope':SCOPE,'videoGameOnly':True,'authoredSpellCounts':index['authoredCounts'],'activeCheckpoint':h.p.binding(CHECKPOINT),'currentEvidence':bindings,'pendingCohortsAdopted':False,'sourceInformationDeleted':0,'historyRewritten':False,'wholeGameAcceptanceClaimed':False}
 manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True);extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
 for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
 for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
 write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0');print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'counts':index['authoredCounts']}))

def verify_push():
 commit=git('rev-parse','HEAD').decode().strip();remote=git('ls-remote','origin','refs/heads/main').decode().split()[0];assert commit==remote and git('rev-parse','HEAD^').decode().strip()==BASE and git('status','--porcelain=v1','-z')==b''
 expected=json.loads((W/'expected-staged-blobs.json').read_bytes());tree=h.oldtree(commit);baseline=h.oldtree(BASE);assert all(tree.get(n,{}).get('oid')==oid for n,oid in expected.items()) and set(baseline)<=set(tree)
 report=REPORT+'/STAGED_VERIFICATION.json';assert tree[report]['oid']==h.p.blob(lp(D/report).read_bytes());assert set(tree)-set(baseline)-set(expected)=={report}
 receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRoot':str(G),'deliveryRoot':str(D),'baseCommit':BASE,'commit':commit,'remoteMain':remote,'url':f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}','worktreeClean':True,'expectedBlobsVerified':len(expected),'totalCommitEntries':len(tree),'priorTrackedEntriesPreserved':len(baseline),'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'authoredCounts':{'reviewed':525,'pending':323},'developmentContinues':True,'wholeGameCompleted':False,'scope':SCOPE};write_new(W/'push-receipt.json',jsraw(receipt));write_new(G/REPORT/'PUSH_RECEIPT.json',jsraw(receipt));print(json.dumps(receipt))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':verify_push}[sys.argv[1]]()
