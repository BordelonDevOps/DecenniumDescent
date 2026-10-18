"""Preserve source conferences, expanded bestiary evidence and truthful review-recovery status."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('sources_recovery_delivery_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='c9c99f1e477b073efdde469d25fb348fcff72c89'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-sources-recovery'
REPORT='docs/audit/2026-10-18/github-snapshot-sources-recovery'
STATUS='SNAPSHOT_STATUS_2026-10-18_SOURCES_RECOVERY.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_SOUL_CONTACT_RECOVERY_21.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for module in [h,h.p]:module.BASE,module.W,module.REPORT,module.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)
SCOPE='Ward7, Manifestation7 and Soul/contact6 complete source conferences UNSENT; expanded workbook/manuscript CR2 evidence and companion supplement UNSENT; preserved interrupted Illusion14 review and explicitly unconfirmed recovery attempt. Queue16/checkpoint21.525 reviewed/323 pending,249 standalone,173 interfaces unchanged. No new adoption or cosmology decision.'

def scan():
 h.scan();p=W/'plan.json';plan=json.loads(p.read_bytes());plan.update(ownerInstruction='Preserve ongoing progress on GitHub, confer regularly with actual GPT, continue until review completes or20%allowance remains; preserve all original information.',scope=SCOPE);p.write_bytes(jsraw(plan))

def assemble():
 plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts'];assert git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
 expected,paths={},[]
 for row in plan['included']:
  expected[row['path']]=row['gitBlob']
  if row['changedFromBaseline']:
   raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path'];dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw);assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
 index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');assert index['authoredCounts']=={'reviewed':525,'pending':323};assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
 names=['WARD_7_SOURCE_CONFERENCE_01_PREPARATION.json','MANIFESTATION_7_SOURCE_CONFERENCE_01_PREPARATION.json','SOUL_CONTACT_6_SOURCE_CONFERENCE_01_PREPARATION.json','COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_03.json','COMMAND_UNDEATH_CONTENT_EVIDENCE_01_PREPARATION.json','ILLUSION_PERCEPTION_14_RECOVERY_PROGRESS_01_STATUS.json','SOUL_CONTACT_RECOVERY_21_CHECK.json'];bindings={n:h.p.binding(f'{A}/{n}') for n in names}
 notice=f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 ordinary spells reviewed /323 pending.** New source conferences and expanded bestiary evidence are preserved. Actual GPT review is interrupted; recovery delivery is unconfirmed. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n';overlays=[]
 for name in ['README.md','START_HERE.md']:
  raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw);delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered);overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
 status=f'''# Decennium Descent development backup —18 October2026 UTC

Video-game-only development continues. This snapshot preserves progress since `{BASE}`. Membership remains **525 ordinary spells reviewed /323 pending**,249 complete standalone procedures and173 scoped accepted interfaces. No new spell, cosmology identity or domain gate is adopted here.

Ward7 preserves seven identities/eight placements,20 questions,50 sources and255 checks; Manifestation7 preserves seven identities/seven placements,23 questions,60 sources and283 checks. Each has three individually assessed tierB and four tierC spells. Soul/contact6 adds six identities/seven school placements,20 questions,82 complete sources and363 checks with threeB/threeC. These are full source conferences prepared UNSENT. They include exact originals, current accepted comparisons and genuine questions; no complete earlier operational scenarios or new accepted procedures are claimed. Soul Cage's creature/humanoid school distinction and Action/Dying timing remain explicit unresolved decisions. Original manuscripts, saved cosmology website, owner qualifications and current soul/death model remain separate authorities.

The expanded Command Undeath search checked24 byte-distinct bestiary XLSX across31 paths and144 Known/Sealed manuscript entries without editing workbooks. All182 sources and416 checks are preserved. Eight historical exactCR2 Undead rows are variants of one Marut/Order-Drone identity. Both current workbooks classify that identity as Construct; conflicting HP, generator text and review warnings survive. No operative CR2 Undead is cleared. The separate evidence supplement preserves full old/current rows, explicit rename code and187 source files;188 checks pass. It remains UNSENT alongside the complete CompanionExact05 package, with two whole-case content holds intact. The failed deep-path02 attempt is retained as history; successful03 is the completed search.

Illusion14 Current12 was actually submitted in Review Continuation Part4, user turn99c03218-f9ed-4545-8792-d4d87ec6e4fb. The browser later reported a connection interruption and native chat status systemError. No completed assistant final is present in the checked history. A recovery/progress request was attempted through the chat tool and browser, but its delivery is **not confirmed**. The file named ILLUSION_PERCEPTION_14_RECOVERY_PROGRESS_01_ACTUAL_SUBMISSION.json contains an earlier native read response, not proof of the recovery message. Its misleading filename is explicitly qualified in ILLUSION_PERCEPTION_14_RECOVERY_PROGRESS_01_STATUS.json; both files remain preserved. A browser draft may remain. Inspect actual saved history before resubmitting to avoid duplicates. No interrupted review is counted as acceptance.

Continue from [checkpoint21]({CHECKPOINT}), [start guide](START_HERE.md) and [review map](REVIEW_MAP.html). Queue16 retains323 pending identities:142 in19 active/prepared groups and181 ungrouped.468 navigation checks and1,373 distinct links pass; all75 full aspect rows are unchanged. The latest allowance observation is52%remaining. Restore actual GPT collaboration, resume the full Illusion conference, then send CompanionExact05 with the separate CR2 evidence. The user's stop condition remains review completion or20%allowance remaining; no whole-game completion is claimed.

The [preservation manifest]({REPORT}/manifest.json) records every selected hash and locally retained exclusion. Every prior tracked entry remains. Existing exclusions keep private configuration, unrelated captures, third-party books, imported assets, dependencies and mixed archives locally. No deletion, force push, history rewrite or remote import into the authoring folder occurs. Authored review, implementation/runtime, human gameplay, balance, cosmology, whole-game flow and release remain distinct.
'''
 delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'status':'Development preservation; actual GPT connection requires recovery','scope':SCOPE,'videoGameOnly':True,'authoredSpellCounts':index['authoredCounts'],'activeCheckpoint':h.p.binding(CHECKPOINT),'currentEvidence':bindings,'pendingCohortsAdopted':False,'sourceInformationDeleted':0,'historyRewritten':False,'wholeGameAcceptanceClaimed':False}
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
