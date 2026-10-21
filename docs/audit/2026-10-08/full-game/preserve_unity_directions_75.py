"""Preserve original notebook brief and a bounded, read-only local intake."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess
G=Path(r'C:\Github\DecenniumDescent')
W=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
D=W.parent/'github-delivery'
A=G/'docs/audit/2026-10-08/full-game'
O=A/'unity-development-directions-75'
report=A/'UNITY_DEVELOPMENT_DIRECTIONS_INTAKE_75.json'
assert not O.exists() and not report.exists()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(args,cwd=None):
 r=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
 return {'command':args,'cwd':str(cwd) if cwd else None,'exitCode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
files=['Decennium_Descent_Unity_Codex_Directions.md','Decennium_Descent_Codex_Start_Prompt.txt']
sources={n:Path(r'C:\Users\cbord\Downloads')/n for n in files}
sources.update({n:W/n for n in ['GPT_UNITY_OWNER_CONTEXT_75_NATIVE.json','CODEX_UNITY_DESIGN_CONTEXT_75_NATIVE.json']})
assert all(p.is_file() for p in sources.values())
native=json.loads(sources['GPT_UNITY_OWNER_CONTEXT_75_NATIVE.json'].read_bytes())
owner=[]
for t in native['turns']:
 for x in t['items']:
  if x['type']=='userMessage':owner.append({'id':x['id'],'text':'\n'.join(c['text'] for c in x['content'] if c['type']=='text')})
assert any(x['id']=='374b7d9e-41fd-42a4-934e-711ad616b4b9' and 'SNES Style CRPG' in x['text'] for x in owner)
assert any(x['id']=='41d5797f-d115-4cce-90fd-8ccc835b86cb' and 'Prepare a set of directions' in x['text'] for x in owner)
brief=sources[files[0]].read_text(encoding='utf-8')
assert all('## '+str(i)+'. ' in brief for i in range(1,19))
authority=[G/'CANON_MANIFEST.md',G/'docs/canon/CANON_MANIFEST.json',G/'docs/canon/REPOSITORY_PROMOTION.md',G/'docs/game-design/UNITY_DESIGN_EVALUATION.md',G/'docs/game-design/SOURCE_EVIDENCE.json',G/'DescentReviewChanges/ReviewBible/docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md',A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json']
bound=[info(p) for p in authority]
scans=[]
for root in [G,W.parent]:
 scans.append(run(['rg','--files','--hidden','-g','ProjectVersion.txt','-g','*.asmdef','-g','*.unity','-g','!**/.git/**',str(root)]))
assert all(s['exitCode']==1 and not s['stdout'] and not s['stderr'] for s in scans)
git={name:run(['git','-c','core.longpaths=true','-c','core.autocrlf=false',*args],D) for name,args in {'status':['status','--short'],'head':['rev-parse','HEAD'],'branch':['branch','--show-current'],'worktrees':['worktree','list'],'remotes':['remote','-v']}.items()}
assert all(v['exitCode']==0 for v in git.values())
author_git=run(['git','rev-parse','--show-toplevel'],G)
assert author_git['exitCode']!=0
dotnet=run([r'C:\Program Files\dotnet\dotnet.exe','--list-sdks'])
tool_paths=[Path(r'C:\Program Files\Unity\Hub\Editor'),Path(r'C:\Program Files\Unity\Editor\Unity.exe'),Path(r'C:\Program Files\Unity Hub\Unity Hub.exe')]
guidance=[]
for root in [Path('C:/'),Path('C:/Github'),G,G/'docs',G/'docs/audit',G/'docs/audit/2026-10-08',A]:
 for name in ['AGENTS.md','AGENTS.override.md']:
  p=root/name;guidance.append({'path':str(p),'exists':p.exists()})
assert not any(x['exists'] for x in guidance)
reuse={}
for rel in ['src','tools','DescentReviewChanges/ReviewBible/tools','DescentReviewChanges/ReviewBible/data/playtest','DescentReviewChanges/ReviewBible/data/director/spell_review']:
 p=G/rel;reuse[rel]={'fileCount':sum(x.is_file() for x in p.iterdir()),'assessment':'Existing source/data or tooling; not verified as Unity runtime. Do not rerun one-shot authoring/apply scripts.'}
O.mkdir()
for n,p in sources.items():
 shutil.copyfile(p,O/n)
 assert (O/n).read_bytes()==p.read_bytes()
result={
 'id':'UNITY-DEVELOPMENT-DIRECTIONS-INTAKE-75','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'PRESERVED_AND_READ_ONLY_INTAKE_COMPLETE; ENGINE_IMPLEMENTATION_NOT_STARTED',
 'scope':'Original two GPT artifacts, complete owner conversation context, prior Codex design discussion, and bounded local readiness evidence. This is not a complete Stage 0 engine audit or Stage 1 implementation.',
 'thread':{'id':'6ad64114-2364-83e9-8764-bc55988b0479','title':'Unity Development Setup','ownerRequest':'41d5797f-d115-4cce-90fd-8ccc835b86cb','assistantBrief':'b0572b7f-e15c-4d11-8353-86853e0329c6'},
 'artifacts':[info(O/n) for n in sources], 'briefSectionsRead':list(range(1,19)), 'ownerStatements':owner,
 'ownerEstablishedProductDirection':['Unity engine','SNES-style CRPG','Direct-control exploration with run/jump/contextual explore/dig/mark/open interactions','Tactical CRPG experience; Owlcat comparison does not independently replace existing cadence','Resource management with crafting, research and companion tasks; fishing/mining/farming examples','Ongoing AI-assisted rules-engine and engineering oversight'],
 'proposalBoundaries':['Shared simulation architecture is the proposed technical approach, not proof of an implemented runtime.','Host plus four guests is retained by the brief, but supporting owner decision must be independently traced before implementation.','Earlier Codex party-command/turn-based recommendation remains historical proposal; actual subsequent owner three-experience direction takes precedence.','Windows target, exact editor/render/input packages, pause/travel/time/encounter conversion, geometry adapters and jump policy need verified decisions before production behavior.','GPT starter-prompt text does not itself issue a new human implementation instruction. Existing owner implementation reservation retained.'],
 'authorityBindings':bound,'guidanceProbe':guidance,
 'unityProjectSearch':{'roots':[str(G),str(W.parent)],'observations':scans,'result':'No ProjectVersion.txt, .asmdef or .unity files found by rg in these two trees. Archives not expanded for this search; no claim about every machine directory. No verified Unity project root.'},
 'authoringTreeGit':author_git,'deliveryGit':git,
 'tooling':{'dotnetSdkInventory':dotnet,'defaultUnityLocations':[{'path':str(p),'exists':p.exists()} for p in tool_paths],'unityMcpToolsAvailableInCurrentSession':0,'license':'NOT VERIFIED','targetBuildModule':'NOT VERIFIED','matchingEditor':'NOT VERIFIED'},
 'reuseInventory':reuse,
 'firstProposedImplementationTask':'After a direct execution instruction and verified tooling/source boundaries: smallest isolated C# command/snapshot laboratory, explicitly TEST_ONLY where production policy is unresolved. Reuse exact current data and accepted contracts; no parallel rule authority.',
 'verification':{'originalFilesCopiedByteExactly':True,'complete18SectionBriefRead':True,'unityCompilation':'NOT RUN','editModeTests':'NOT RUN','playModeTests':'NOT RUN','standaloneBuild':'NOT RUN','gameplayObservation':'NOT RUN'},
 'sourceInformationDeleted':0,'canonicalRulesChanged':0,'unityProjectCreated':False,'downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'implementationApplied':False,'ownerImplementationReservationRetained':True,
 'nextAction':'Continue the current authored review and preserve the Rank7 deadline return; use this intake for later explicitly directed Unity implementation. Do not silently replace existing cadence or promote accepted review candidates.'}
report.write_bytes(enc(result))
for b in bound:assert info(G/b['path'])==b
(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
print(json.dumps({'report':info(report),'artifacts':result['artifacts'],'unityProjectFound':False,'dotnetSdks':dotnet['stdout'],'canonicalChanges':0}))
