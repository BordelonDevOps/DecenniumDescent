from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
ROOT=A/'bestiary-current-ex58-context-82';ZIP=A/'DD_Bestiary_Current_EX58_Context_82.zip';RECEIPT=A/'BESTIARY_CURRENT_EX58_CONTEXT_82_PREPARATION.json';CHECK=A/'BESTIARY_CURRENT_EX58_CONTEXT_82_CHECK.json';REQUEST=A/'CODEX_BESTIARY_V3_CURRENT_DISPATCH_REQUEST_82.txt';SAVED=A/Path(__file__).name
for p in [ROOT,ZIP,RECEIPT,CHECK,REQUEST,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(s,b):
 checks.append({'check':s,'pass':bool(b)})
 if not b:raise AssertionError(s)
v3=A/'BESTIARY_COMPLETE_FILE_HANDOFF_V3_PREPARATION_81.json';v=j(v3)
ck('Exact V3 archive retained',info(G/v['archive']['path'])==v['archive'])
labels=A/'EX58_REVIEW_LABEL_NORMALIZATION.json';lab=j(labels);paths=[G/p for p in lab['currentEightCandidateFiles']]
for p in paths:
 a=info(p);expect=lab['currentEightCandidateFiles'][a['path']];ck('Exact current EX58 artifact '+a['path'],a['bytes']==expect['bytes'] and a['sha256']==expect['sha256'])
paths += [labels,A/'EX58_X01_FULFILLMENT.json',A/'EX58_COVERAGE_ADDENDUM.json',R/'docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json',A/'EX58_EXACT_VERDICT_LOCAL_RECEIPT.json',A/'EX58_FINAL_RECEIPT_LOCAL.json',A/'EX58_EDIT_01_FULFILLMENT.json',A/'EX58_EDIT_02_FULFILLMENT.json',A/'FULL_GAME_CURRENT_EVIDENCE_FRONTIER_82.json',A/'FULL_GAME_CURRENT_REVIEW_MAP_82.md',A/'FULL_GAME_CURRENT_EVIDENCE_FRONTIER_82_CHECK.json',v3,A/'ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REFRESH_81.json']
for receipt,key in [('EX58_FINAL_RECEIPT_LOCAL.json','archive'),('EX58_EXACT_VERDICT_LOCAL_RECEIPT.json','package')]:
 b=j(A/receipt)[key];p=G/b['path'];ck('Original actual EX58 return '+p.name,info(p)==b);paths.append(p)
ck('EX58 fulfilled after original conditional verdict',j(A/'EX58_X01_FULFILLMENT.json')['exactCandidateAuthoredApproval'] is True)
payload={};sources=[]
for p in paths:
 i=info(p);b=p.read_bytes();n='sources/'+i['path'];ck('Unique context source '+n,n not in payload);payload[n]=b;sources.append(i)
context={'id':'BESTIARY-CURRENT-EX58-CONTEXT-82','status':'PREPARED_UNSENT_DEPENDENCY_SUPPLEMENT','primaryBestiaryArchive':v['archive'],'purpose':'Carry complete current exact-approved EX58 expedition/transport/social/reputation rules into bestiary source review, including harvest/loot custody, reward valuation/settlement, actual transport bodies and crew/actor budgets. No creature or global rule approval is added.',
 'exactCurrentEX58Artifacts':[info(G/p) for p in lab['currentEightCandidateFiles']],
 'whySeparate':'V3 is preserved byte-for-byte. The later full-game evidence audit traced historical expedition26 unsent notes to the fulfilled EX58 successor. Current eight artifacts and exact receipt chain supplement V3 rather than rewriting its history.',
 'sourceStatusPrecedence':'EX58 exact verdict was conditional; the supplied subsequent X01 fulfillment and reversible final-label proof establish the accepted authored scope. Do not stop at the earlier localFulfillmentComplete:false receipt. Full current candidate bytes match the final labels.',
 'scopeCounts':{k:j(A/'EX58_X01_FULFILLMENT.json')[k] for k in ['sourceDirectionsRetained','chapterExamples','transportProfiles','auxiliaries','integratedEvents','contractFamilies','boundaryCases','socialScenarios']},
 'notNewMechanics':True,'canonicalIntegrationReserved':True,'appliedSpellCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},'acceptedButUnapplied':50,
 'allWholePositiveCaseHoldsRetained':['IN6-09A','IN6-09B','EN5-01A','EN5-01B','EN6-03B'],'gatesNotAdvanced':['creature exact authorship','canonical application','runtime execution','human testing','balance','new cosmology canon','whole-game flow','release'],
 'questionDependencyMap':{'BV3-01':'EX58 source precedence and typed provenance','BV3-02':'Actual body/geometry and actor budgets; no copied transport defaults for monsters','BV3-16':'Distributed creature-body procedure remains NEW despite real-actor transport precedents','BV3-23':'Harvest containers, inventory/cargo custody and elapsed time use current operational interfaces','BV3-24':'Loot reward valuation, input/output units and settlement domains remain distinct','BV3-25':'Knowledge and social/reputation consequences preserve current exact procedures','BV3-27':'Full encounters and aftermath should carry actual expedition actors, resources, retreat and settlement state'},
 'fullGameMapLimits':'All75requirements and1135listed reference paths are preserved/bound. This navigation audit is not full semantic revalidation or a percentage-complete claim.',
 'sourceBindings':sources,'sent':False,'newApprovals':0,'sourceInformationDeleted':0}
request=(A/'CODEX_BESTIARY_V3_SOURCE_REQUEST_PREPARED_81.txt').read_text(encoding='utf-8')
request+='\nCURRENT DEPENDENCY SUPPLEMENT82: Also read the attached DD_Bestiary_Current_EX58_Context_82.zip in full. It adds all eight exact current EX58 candidate artifacts, the original source and exact-review return archives, the later fulfilled X01 correction, final label/projection proof and scoped coverage addendum. The earlier expedition26 prepared/unsent status is historical; do not repeat that preliminary conference or treat the earlier conditional verdict as still unfulfilled. Preserve the current transport, loot custody/valuation, settlement, social/reputation, resources and retreat contracts. The whole-game map preserves all75requirements with1135verified evidence paths, and does not confer semantic, runtime or whole-domain approval. Resolve the bestiary questions using these complete current dependencies; no new cosmology or canonical application is requested.\n'
payload['CURRENT_CONTEXT.json']=enc(context);payload['SOURCE_CONFERENCE_REQUEST.txt']=request.encode('utf-8')
payload['README.md']=b'# Current EX58 context for the complete bestiary V3 conference\n\nRead CURRENT_CONTEXT.json, then the complete eight current artifacts and receipt chain. Pair this supplement with the exact original V3 archive named in context. Earlier expedition26 preliminary labels are history; the later fulfilled EX58 authored scope controls. All creature questions remain unselected. No downloaded code should be executed.\n'
payload['prepare_bestiary_ex58_context_82.py']=Path(__file__).read_bytes()
manifest={n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payload.items())};payload['MANIFEST.json']=enc(manifest)
ROOT.mkdir()
for n,b in payload.items():
 p=Path('\\\\?\\'+str((ROOT/n).resolve()));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in sorted(payload.items()):z.writestr(n,b)
with zipfile.ZipFile(ZIP) as z:
 ck('Unique complete safe context member names',len(z.namelist())==len(payload) and set(z.namelist())==set(payload) and all('..' not in Path(n).parts and not n.startswith('/') for n in z.namelist()))
 ck('Context CRC',z.testzip() is None)
 for n,b in payload.items():ck('Complete context roundtrip '+n,z.read(n)==b)
for before in sources:ck('Source remains unchanged '+before['path'],info(G/before['path'])==before)
ck('Original bestiary V3 still byte-identical',info(G/v['archive']['path'])==v['archive'])
REQUEST.write_text(request,encoding='utf-8');SAVED.write_bytes(Path(__file__).read_bytes())
CHECK.write_bytes(enc({'checkCount':len(checks),'failures':0,'checks':checks,'scope':'Complete byte preservation, exact current EX58 artifact binding and archive roundtrip. No original reviewer script or runtime was executed.'}))
receipt={'id':context['id'],'preparedAtUtc':datetime.now(timezone.utc).isoformat(),'status':context['status'],'primary':v['archive'],'supplement':info(ZIP),'request':info(REQUEST),'sourceFiles':len(paths),'members':len(payload),'check':info(CHECK),'checks':len(checks),'failures':0,'sent':False,'newRuleAdoptions':0,'sourceInformationDeleted':0,'nextAction':'After the current live ResonanceFields3 reply is resolved, dispatch the exact bestiary V3 and this full current EX58 context together. Check for intervening substantive authority changes; preserve both original archives.'}
RECEIPT.write_bytes(enc(receipt));print(json.dumps({'receipt':info(RECEIPT),'supplement':info(ZIP),'sourceFiles':len(paths),'checks':len(checks),'failures':0}))
