"""Publish a preservation-based development snapshot without resuming game authoring."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import importlib.util,json,subprocess,sys,zipfile,io
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('snapshot_helpers',HERE/'deliver_progress_2026_10_15_cosmology.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
p.W=HERE.parent/'audit_work/github-snapshot-2026-10-16-video-game'
p.REPORT='docs/audit/2026-10-16/github-snapshot-video-game'
p.BASE='18c6e3ae8b3c1d391dd91121693931657ae9c98f'
p.STATUS='SNAPSHOT_STATUS_2026-10-16_VIDEO_GAME.md'
G,D,W,REPORT,A,BASE,STATUS=p.G,p.D,p.W,p.REPORT,p.A,p.BASE,p.STATUS
lp,git,digest,write_new,jsraw=p.lp,p.git,p.digest,p.write_new,p.jsraw
oldtree=p.tree;p.tree=lambda ref=BASE:oldtree(ref)

def raw_capture(raw):
 return b'App navigation' in raw and b'Toggle sidebar' in raw and b'Chat actions' in raw

def member_issue(name,raw,depth=0):
 why=p.policy.reason(name)
 if why and not why.startswith('generated'):return why
 suffix=Path(name).suffix.lower()
 if suffix in p.policy.TEXT:
  if raw_capture(raw):return 'raw browser capture includes unrelated sidebar information; retained locally'
  if any(rx.search(raw) for rx in p.policy.SECRET):return 'credential-pattern review required; retained locally'
 if suffix=='.zip':
  if depth>=5:return 'nested archive depth requires separate review; retained locally'
  try:
   with zipfile.ZipFile(io.BytesIO(raw)) as z:
    for item in z.infolist():
     if not item.is_dir():
      reason=member_issue(item.filename,z.read(item),depth+1)
      if reason:return 'nested archive contains locally retained material: '+reason
  except zipfile.BadZipFile:return 'archive inspection failed; retained locally'
 return None

def scan():
 assert git('status','--porcelain=v1','-z')==b''
 assert git('rev-parse','HEAD').decode().strip()==BASE
 assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==BASE
 assert not W.exists()
 baseline=p.tree();args=['rg','--files','--hidden','--no-ignore','-g','!Descent assets/**']
 for part in p.policy.SKIP:args+=['-g',f'!**/{part}/**']
 names=sorted(n.replace('\\','/') for n in subprocess.run(args,cwd=G,capture_output=True,text=True,encoding='utf8',check=True).stdout.splitlines())
 included=[];excluded=[];alerts=[]
 for i,n in enumerate(names):
  path=lp(G/n);assert not path.is_symlink(),n
  before=path.stat();raw=path.read_bytes();assert (before.st_size,before.st_mtime_ns)==(path.stat().st_size,path.stat().st_mtime_ns)
  row={'path':n,'bytes':len(raw),'sha256':digest(raw),'gitBlob':p.blob(raw)}
  changed=baseline.get(n,{}).get('oid')!=row['gitBlob']
  why=p.policy.reason(n)
  if not why and changed:why=member_issue(n,raw)
  if not why and len(raw)>=100*1024*1024:why='oversized regular Git blob; preserved locally'
  if why:
   row['reason']=why;excluded.append(row)
   if 'credential-pattern' in why:alerts.append(n)
  else:row['changedFromBaseline']=changed;included.append(row)
  if i and i%5000==0:print(json.dumps({'filesInspected':i}),flush=True)
 plan={'createdAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':'push them. I dont want github interferring with this.','scope':'Backup saved work through the video-game-only direction; development remains paused.','sourceRoot':str(G),'deliveryRoot':str(D),'baseCommit':BASE,'included':included,'excluded':excluded,'excludedTreesPreservedLocally':['Descent assets',*p.policy.SKIP],'credentialPatternAlerts':alerts,'sourceInformationDeleted':0,'historicalGitEntriesPreserved':True}
 write_new(W/'plan.json',jsraw(plan));write_new(W/'changed-source-paths.json',jsraw([x['path'] for x in included if x['changedFromBaseline']]))
 print(json.dumps({'included':len(included),'changed':sum(x['changedFromBaseline'] for x in included),'includedBytes':sum(x['bytes'] for x in included),'excluded':len(excluded),'reasons':dict(Counter(x['reason'] for x in excluded)),'credentialAlertCount':len(alerts)}))

def assemble():
 plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts']
 assert git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
 expected={};paths=[]
 for row in plan['included']:
  raw=lp(G/row['path']).read_bytes();assert digest(raw)==row['sha256'],row['path'];expected[row['path']]=row['gitBlob']
  if row['changedFromBaseline']:
   dst=lp(D/row['path']);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw);assert digest(dst.read_bytes())==row['sha256'];paths.append(row['path'])
 index=p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');assert index['authoredCounts']=={'reviewed':451,'pending':397}
 direction=p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection'];assert direction['product']=='video-game-only'
 checkpoint=p.read(f'{A}/ACTIVE_AUTHORING_CHECKPOINT_VIDEO_GAME_ONLY_01.json');assert checkpoint['newRuleAdoptions']==0
 notice=f'> **Latest backup — 16 October 2026:** Decennium Descent is **video-game-only**. The active plan and current saved work are included; development remains paused. **451 ordinary spells reviewed / 397 pending.** AC6 is not locally adopted. See [snapshot status]({STATUS}). Earlier snapshot statements below are preserved history.\n\n'
 overlays=[]
 for name in ['README.md','START_HERE.md']:
  original=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,original)
  delivered=notice.encode()+original;lp(D/name).write_bytes(delivered)
  overlays.append({'path':name,'sourceSha256':digest(original),'deliveredSha256':digest(delivered),'preservedSource':preserved,'change':'Delivery notice prepended; source bytes preserved verbatim.'});paths.extend([name,preserved])
 status=f'''# Decennium Descent backup — 16 October 2026

Decennium Descent is now **video-game-only**. This owner-requested push saves the completed local work and existing proposals. Development remains paused; this delivery does not resume authoring or adopt pending spells.

The [active development plan](DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md), [verbatim directive](DescentReviewChanges/ReviewBible/docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md), [75-area coverage ledger](DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json) and [latest checkpoint]({A}/ACTIVE_AUTHORING_CHECKPOINT_VIDEO_GAME_ONLY_01.json) govern current work. Tabletop-only production is retired; original sources and prior review history remain preserved.

The backup includes saved work since `{BASE}`, including the later scoped cosmology records, accepted AC4/Banishment/AC5 work, unadopted AC6 and DE4 drafts, accelerated review protocol, 49-entry interface registry and prepared 25-spell semantic delta. Current ordinary-spell accounting is **451 reviewed / 397 pending** across 848 identities. AC6 exact Current06 acceptance still needs recovery and verification before local adoption.

Source preservation, structural checks, authored semantic review, arithmetic/geometry validation, engine implementation, runtime tests, human gameplay, balance, cosmology canon, whole-game completion and release approval remain distinct. This push does not complete any of those gates by itself.

The [manifest]({REPORT}/manifest.json) records included file hashes and material retained locally under the established backup boundaries. Raw browser captures with unrelated sidebar content, private configuration, third-party reference books, imported asset workbench, dependencies and generated folders remain local. An immutable archive containing locally retained material is preserved locally rather than rewritten. Existing tracked Git entries and history are retained without deletion or force-push. This repository is a development backup containing internal game material.

GitHub remains the backup destination. The active authoring folder remains `C:\\Github\\DecenniumDescent`; syncing this backup does not pull remote files into that folder or change its rules.
'''
 delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'status':'Development paused; authorized backup only','authoredSpellCounts':index['authoredCounts'],'videoGameOnly':True,'activeCheckpoint':p.binding(f'{A}/ACTIVE_AUTHORING_CHECKPOINT_VIDEO_GAME_ONLY_01.json'),'direction':p.binding('DescentReviewChanges/ReviewBible/docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md'),'newRuleAdoptions':0,'wholeGameAcceptanceClaimed':False,'sourceInformationDeleted':0,'gitHistoryRewritten':False}
 manifest=dict(plan);manifest.update(assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesReverified=True)
 extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
 for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
 for name in set(paths):expected[name]=p.blob(lp(D/name).read_bytes())
 write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0')
 print(json.dumps({'sourceFilesReverified':len(plan['included']),'pathsToStage':len(set(paths)),'newRulesAdopted':0,'sourceInformationDeleted':0}))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':p.verify}[sys.argv[1]]()
