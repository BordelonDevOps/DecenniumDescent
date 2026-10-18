"""Preserve verified AC6/DE4 integration and ongoing source review in GitHub."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('progress_delivery_helpers',HERE/'deliver_progress_2026_10_16_video_game.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='c1e2b7dcec461bd51ec9f20cb23e87ab42eb9a92'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-de4'
REPORT='docs/audit/2026-10-18/github-snapshot-de4'
STATUS='SNAPSHOT_STATUS_2026-10-18_DE4.md'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for module in [h,h.p]:module.BASE,module.W,module.REPORT,module.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)

def scan():
 h.scan();p=W/'plan.json';plan=json.loads(p.read_bytes());plan.update(ownerInstruction='Preserve completed work on GitHub and continue developing with actual GPT until review completion or20% allowance remaining.',scope='Active video-game development snapshot: verified AC6 and DE4 adoption, current next25 conference, preserved persistent20 and illusion drafts.');p.write_bytes(jsraw(plan))

def assemble():
 plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts'];assert git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
 expected={};paths=[]
 for row in plan['included']:
  expected[row['path']]=row['gitBlob']
  if row['changedFromBaseline']:
   raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path'];dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw);assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
 index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');assert index['authoredCounts']=={'reviewed':480,'pending':368};assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
 checkpoint=h.p.read(f'{A}/ACTIVE_AUTHORING_CHECKPOINT_DE4_APPLIED_NEXT25_SUBMITTED_06.json');assert checkpoint['de4']['adopted'] and checkpoint['next25']['submitted'] and not checkpoint['next25']['adopted']
 notice=f'> **Latest development backup — 18 October2026 UTC:** Video-game development is active. **480 ordinary spells reviewed /368 pending**; AC6 and DE4 exact authored integration is complete. The next25 source conference is running with the actual GPT notebook. See [snapshot status]({STATUS}). Older backup/stop notices below are preserved history.\n\n'
 overlays=[]
 for name in ['README.md','START_HERE.md']:
  raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw);delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered);overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
 status=f'''# Decennium Descent development backup —18 October2026 UTC

Active development continues with the actual GPT notebook. The game is video-game-only. This verified progress snapshot preserves completed authored integration and pending development since `{BASE}`.

Ordinary spell accounting is **480 reviewed /368 pending** across848 identities, including204 complete standalone procedures. AC6’s14 identities and DE4’s15 identities are accepted and integrated with exact payload copies and preserved source versions. DE4 retains37 current cases,30 original texts and95 frozen sources. Its1,893 local application checks and249 registry/inventory checks pass; the current registry contains108 scoped accepted interfaces.

The next25 full source conference07 is actually submitted to Review Continuation Part4. It includes25 full procedures,36 original scenario vectors,15 high-rank supplements and nine substantive decisions. These25 are still pending. Persistent20 Current05 retains40 original vectors,7 supplements and8 adversarial cases. Illusion14 Current04 has14 full proposals,28 original texts and8 current vectors;20 remain to expand. Creation is preserved separately for economy/crafting review. All these pending cohorts retain earlier versions and exact source evidence.

Continue from the [active checkpoint]({A}/ACTIVE_AUTHORING_CHECKPOINT_DE4_APPLIED_NEXT25_SUBMITTED_06.json), [start guide](START_HERE.md), [development direction](DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md) or [review map](REVIEW_MAP.html). The map verified1,291 distinct links with none missing. All75 domain gates remain distinct and open according to their actual evidence.

The [manifest]({REPORT}/manifest.json) records exact included hashes and exclusions. Original material and every previously tracked Git entry are preserved. Established backup exclusions remain local: private configuration, unrelated browser/sidebar captures, third-party reference books, imported assets, dependencies, generated folders and immutable archives containing those materials. No force-push or source deletion is used. GitHub is a backup destination; no remote files are imported into the authoring folder.

Source review and file checks do not establish game implementation, runtime correctness, human gameplay, numerical balance, cosmology/canon, whole-game completion or release. Continue until the review is complete or any reported usage allowance reaches20% remaining; latest observed allowance was84% remaining. No prior stopped/paused status governs this active continuation.
'''
 delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'status':'Active development; verified preservation snapshot','videoGameOnly':True,'authoredSpellCounts':index['authoredCounts'],'activeCheckpoint':h.p.binding(f'{A}/ACTIVE_AUTHORING_CHECKPOINT_DE4_APPLIED_NEXT25_SUBMITTED_06.json'),'ac6Adopted':True,'de4Adopted':True,'next25ActuallySubmitted':True,'next25Adopted':False,'sourceInformationDeleted':0,'historyRewritten':False,'wholeGameAcceptanceClaimed':False}
 manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
 extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
 for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
 for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
 write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0');print(json.dumps({'sourceFilesHashedAtScan':len(plan['included']),'changedSourcesReverifiedAtAssembly':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'counts':index['authoredCounts']}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify}[sys.argv[1]]()
