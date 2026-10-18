"""Preserve exact Part5 returns, unapplied staging and complete new source reviews."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,sys
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('part5_returns_helpers',HERE/'deliver_progress_2026_10_16_video_game.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
G,D,A=h.G,h.D,h.A
BASE='c9c9ffb759f3c48ce47a814f03c4e53b2cfeb2a0'
W=HERE.parent/'audit_work/github-snapshot-2026-10-18-part5-returns'
REPORT='docs/audit/2026-10-18/github-snapshot-part5-returns'
STATUS='SNAPSHOT_STATUS_2026-10-18_PART5_RETURNS.md'
CHECKPOINT=f'{A}/ACTIVE_AUTHORING_CHECKPOINT_RANK8_SUMMON_STRUCTURE_37.json'
lp,git,digest,write_new,jsraw=h.lp,h.git,h.digest,h.write_new,h.jsraw
for m in [h,h.p]:m.BASE,m.W,m.REPORT,m.STATUS=BASE,W,REPORT,STATUS
h.p.tree=lambda ref=BASE:h.oldtree(ref)
SCOPE='Preserve actual Companion10/Illusion14 exact acceptances and six proposed Control/Ready corrections, recovered Control15 sources and active conference evidence, staged24 integration and new memory/control4,life/form4,summon/structure5 source conferences through checkpoint37. Applied525/323/249 unchanged; no rule/index implementation or whole-game approval.'

def scan():
 h.scan();p=W/'plan.json';v=json.loads(p.read_bytes());v.update(ownerInstruction='Standing owner requests to push completed progress, preserve all information and continue GPT-assisted development until completion or20percent remaining.',scope=SCOPE);p.write_bytes(jsraw(v))

def assemble():
 plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts'];assert git('status','--porcelain=v1','-z')==b'' and git('rev-parse','HEAD').decode().strip()==BASE
 index=h.p.read('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');assert index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249
 assert h.p.read('DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json')['developmentDirection']['product']=='video-game-only'
 cp=h.p.read(CHECKPOINT);assert cp['newRuleAdoptions']==0 and cp['all75DomainGatesUnchanged'] and not cp['wholeGameComplete']
 q=h.p.read('DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_30.json');assert len(q['groups'])==29 and q['preparedOrActualReviewIdentityCount']==190 and q['originalSourceOrReceiptWorkCount']==133
 staged=h.p.read(f'{A}/PART5_ACCEPTED24_INTEGRATION_STAGING_01_CHECK.json');assert staged['checkCount']==831 and staged['failureCount']==0 and staged['appliedCounts']=={'reviewed':525,'pending':323,'standalone':249}
 integration=h.p.read(f'{A}/part5-accepted24-integration-staging-01/INTEGRATION_PLAN.json');assert not integration['liveIndexModified'] and not integration['canonicalDestinationsCreated'] and len(integration['canonicalCopies'])==8 and len(integration['membershipChanges'])==24
 for name,checks,questions in [('RANK8_MEMORY_CONTROL_4_SOURCE_CONFERENCE_01_CHECK.json',235,21),('RANK8_LIFE_FORM_4_SOURCE_CONFERENCE_01_CHECK.json',206,24),('RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_01_CHECK.json',256,20)]:
  v=h.p.read(f'{A}/{name}');assert v['checkCount']==checks and v['questions']==questions and v['failures']==0 and v['newCurrentVectors']==0
 expected={};paths=[]
 for row in plan['included']:
  expected[row['path']]=row['gitBlob']
  if row['changedFromBaseline']:
   b=lp(G/row['path']).read_bytes();assert digest(b)==row['sha256'],row['path'];p=lp(D/row['path']);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);assert digest(p.read_bytes())==row['sha256'];paths.append(row['path'])
 notice=f'> **Latest development backup —18 October2026 UTC:** Video game only. **525 ordinary spells reviewed /323 pending;249 standalone.** Actual GPT accepted24 additional spells with holds; exact integration is staged, not applied. Proposed Control/Ready corrections and three new source conferences are preserved through checkpoint37. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
 overlays=[]
 for name in ['README.md','START_HERE.md']:
  raw=lp(G/name).read_bytes();preserved=f'{REPORT}/source-before/{name}';write_new(D/preserved,raw);delivered=notice.encode()+raw;lp(D/name).write_bytes(delivered);overlays.append({'path':name,'sourceSha256':digest(raw),'deliveredSha256':digest(delivered),'preservedSource':preserved});paths.extend([name,preserved])
 status=f'''# Decennium Descent development backup —18 October2026 UTC

This progress backup preserves video-game work after `{BASE}` through [checkpoint37]({CHECKPOINT}). Applied ordinary-spell membership remains **525 reviewed /323 pending**, with249 standalone procedures and173 scoped accepted interfaces. It performs no rule/index/runtime implementation and claims no whole-game or release approval.

Actual [Calibration Review Part5](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad4a867-f330-83e9-829e-bf2bb41a6c09) accepted Companion10 Exact05 and Illusion14 Exact13 with all16 exact submitted artifacts unchanged and their holds retained. The [actual-return receipt]({A}/GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json) preserves messages, archives and manifest comparisons. The [integration staging]({A}/part5-accepted24-integration-staging-01/INTEGRATION_PLAN.json) contains eight byte-identical proposed canonical files and24 full entry changes;831 preservation/reference checks pass. **549/299/273 is only a projection after future verified application.** Both exactCR2 Command Undeath whole-case holds retain zero completion credit; all nine Illusion holds remain.

GPT's six Control/Ready corrections are separately preserved. Read-only local preflight matched five live baselines and reproduced/reversed all22 operations exactly, without applying them. The owner reserved implementation for a later instruction. All19 missing Control15 bindings were recovered; the complete original94-member archive includes all54 expected sources. The full15-procedure/30-case/13-question conference is active at capture, with GPT generating its return archive. No full Control15 final or acceptance is claimed by this snapshot. The separate Review continuation part5 remains standby after the owner continued in Calibration Review Part5.

Three full source conferences covering13 more identities are prepared and remain unsent: memory/control4 (68sources,21questions,235checks), life/form4 (58sources,24questions,206checks), and summon/structure5 (68sources,20questions,256checks). All printed benefits, access rows, complete historical sources and scoped counterpart authorities remain preserved. These are unresolved choices and preparation coverage, not newly accepted procedures. Queue30 retains323 pending identities:190 in29 prepared/active groups and133 ungrouped.

Continue from [START_HERE.md](START_HERE.md) and [REVIEW_MAP.html](REVIEW_MAP.html). Latest recorded allowance32percent remaining; continue to review completion or20percent remaining. Runtime, human gameplay, numerical balance, cosmology canon,75-domain closure, whole-game flow and release remain separate gates.

The [manifest]({REPORT}/manifest.json) records selected files and exclusions preserved locally. Every prior tracked Git entry remains. Established exclusions retain private configuration, unrelated browser captures, third-party reference books, imported assets, dependencies and mixed immutable archives locally. No deletion, force push or history rewrite is performed. The source authoring folder remains separate from the delivery checkout.
'''
 evidence={n:h.p.binding(f'{A}/{n}') for n in ['GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json','PART5_CORRECTIONS_LOCAL_PREFLIGHT_01.json','CONTROL15_PART5_RECOVERED_SOURCES_01_RECEIPT.json','PART5_ACCEPTED24_INTEGRATION_STAGING_01_CHECK.json','RANK8_MEMORY_CONTROL_4_SOURCE_CONFERENCE_01_PREPARATION.json','RANK8_LIFE_FORM_4_SOURCE_CONFERENCE_01_PREPARATION.json','RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_01_PREPARATION.json','ACTIVE_AUTHORING_CHECKPOINT_RANK8_SUMMON_STRUCTURE_37_CHECK.json']}
 delivery={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':plan['ownerInstruction'],'scope':SCOPE,'videoGameOnly':True,'activeCheckpoint':h.p.binding(CHECKPOINT),'evidence':evidence,'authoredSpellCounts':index['authoredCounts'],'exactAcceptedButUnappliedIdentities':24,'newRuleAdoptions':0,'sourceInformationDeleted':0,'wholeGameAcceptanceClaimed':False,'control15FinalReceivedAtCapture':False}
 manifest=dict(plan,assembledAtUtc=datetime.now(timezone.utc).isoformat(),deliveryOverlays=overlays,allSelectedSourcesHashedAtScan=True,changedSourcesReverifiedAtAssembly=True)
 extras={STATUS:status.encode(),f'{REPORT}/DELIVERY_CHECKPOINT.json':jsraw(delivery),f'{REPORT}/manifest.json':jsraw(manifest),f'{REPORT}/delivery-script.py':Path(__file__).read_bytes()}
 for name,raw in extras.items():write_new(D/name,raw);paths.append(name)
 for name in set(paths):expected[name]=h.p.blob(lp(D/name).read_bytes())
 write_new(W/'expected-staged-blobs.json',jsraw(expected));write_new(W/'stage-paths.nul',b'\0'.join(n.encode() for n in sorted(set(paths)))+b'\0');print(json.dumps({'sourceFilesHashed':len(plan['included']),'changedSources':sum(x['changedFromBaseline'] for x in plan['included']),'pathsToStage':len(set(paths)),'counts':index['authoredCounts']}))

def verify_push():
 commit=git('rev-parse','HEAD').decode().strip();remote=git('ls-remote','origin','refs/heads/main').decode().split()[0];assert commit==remote and git('rev-parse','HEAD^').decode().strip()==BASE and git('status','--porcelain=v1','-z')==b''
 expected=json.loads((W/'expected-staged-blobs.json').read_bytes());tree=h.oldtree(commit);baseline=h.oldtree(BASE);assert all(tree.get(n,{}).get('oid')==oid for n,oid in expected.items()) and set(baseline)<=set(tree)
 report=REPORT+'/STAGED_VERIFICATION.json';assert tree[report]['oid']==h.p.blob(lp(D/report).read_bytes()) and set(tree)-set(baseline)-set(expected)=={report}
 receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRoot':str(G),'deliveryRoot':str(D),'baseCommit':BASE,'commit':commit,'remoteMain':remote,'url':f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{commit}','worktreeClean':True,'expectedBlobsVerified':len(expected),'totalCommitEntries':len(tree),'priorTrackedEntriesPreserved':len(baseline),'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'authoredCounts':{'reviewed':525,'pending':323},'developmentContinues':True,'wholeGameCompleted':False,'scope':SCOPE}
 write_new(W/'push-receipt.json',jsraw(receipt));write_new(G/REPORT/'PUSH_RECEIPT.json',jsraw(receipt));print(json.dumps(receipt))

if __name__=='__main__':{'scan':scan,'assemble':assemble,'verify':h.p.verify,'verify-push':verify_push}[sys.argv[1]]()
