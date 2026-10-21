from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile

A = Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
R = A/'rank9-resonance-fields3-part5-return-01'
P = A/'resonance-fields3-receipt-followthrough-86'
Z = A/'DD_Resonance_Fields3_Receipt_Followthrough_86.zip'
REQUEST = A/'GPT_RESONANCE_FIELDS3_RECEIPT_REQUEST_86.txt'
RECEIPT = A/'RESONANCE_FIELDS3_RECEIPT_FOLLOWTHROUGH_PREPARATION_86.json'
SCRIPT = A/Path(__file__).name
for path in [P,Z,REQUEST,RECEIPT,SCRIPT]:
    assert not path.exists(), path
def info(path):
    b=path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def encode(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
diag=json.loads((A/'RANK9_RESONANCE_FIELDS3_INDEPENDENT_SEMANTIC_CHECK_86.json').read_text(encoding='utf-8'))
assert diag['checkCount']==3099 and not diag['failures'] and len(diag['openFindings'])==2
files={}
names=['MODEL.json','PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','CASE_DISPOSITIONS.json','ACTOR_TEMPLATES.json','ACTOR_FEATURE_ACCOUNTING.json','SOURCE_REFERENCES.json','HOLD_REGISTER.json','EXACT_OPERATIONS_FROM_SOURCE.json','ARTIFACT_BINDINGS.json','IMPLEMENTATION_BOUNDARIES.json','REVIEW_RECEIPT.json','MANIFEST.json']
for name in names: files['received-return01/'+name]=(R/name).read_bytes()
refs=json.loads((R/'SOURCE_REFERENCES.json').read_text(encoding='utf-8'))['aliases']
for name in ['wizard','classRules','casting']:
    b=refs[name]
    with zipfile.ZipFile(R/b['archive']) as source:
        raw=source.read(b['member'])
    assert hashlib.sha256(raw).hexdigest()==b['sha256']
    files['complete-sources/'+name+Path(b['member']).suffix]=raw
with zipfile.ZipFile(R/'input/DD_Rank9_Resonance_Fields_3_Source_Conference_01.zip') as source:
    files['original-CANDIDATE.json']=source.read('CANDIDATE.json')
assert hashlib.sha256(files['original-CANDIDATE.json']).hexdigest()=='317cc5338ba34e22ee4ed7e22a5a497250e8cad5a6692945b879a8629a7b8262'
files['LOCAL_DIAGNOSTICS.json']=(A/'RANK9_RESONANCE_FIELDS3_INDEPENDENT_SEMANTIC_CHECK_86.json').read_bytes()
files['LOCAL_RECONSTRUCTION.json']=(A/'RANK9_RESONANCE_FIELDS3_INDEPENDENT_RECONSTRUCTION_85.json').read_bytes()
request='''Independent Resonance Fields3 review follow-through: I have read the three procedures, six shared rules, all24 dispositions, all7 main cases and28 branches, and checked the relevant complete class/spell sources. The returned MODEL still reconstructs and reverses exactly. My new independent standard-library diagnostics passed3099 checks covering6 actor templates,134 full-state transitions,56 paid/zero-price commitments,22 damage applications and16 conversion settlements. These are authored-fixture/source/arithmetic checks, not game runtime execution or balance approval. All four external conditional branches and earlier whole-positive-case holds remain.

One narrow durable-history question remains before independent exact acceptance: wizard#/cards/60 makes Arcane Feedback at most once per round. RF9-NS-A-counter timeline0 awards E1RP after Counter1, but the full after-state actor E limitedUses remains {}. RF9-NS-B-counterpulse timeline1 awards B1RP after ClassCounter, but B limitedUses contains only counterpulse-round1:spent. The awards are numerically represented in observations; neither snapshot explicitly records Feedback's once-per-round consumption. This could be deliberately derived from durable source history, so please verify that interpretation rather than treating my question as a selected defect or new rule.

If an exact durable derivation is already supplied, identify its complete state fields and deterministic rule for round identity, duplicate callback/save-reload, and a later qualifying counter in the same round; observational narration alone should not be an executable permission to repay. Otherwise supply the narrow missing spent/source receipt and propagate it through every affected complete model/case/Director artifact. Preserve native successful-counter qualification, actual1RP cap, existing recovery prohibitions and next-round eligibility. A duplicate callback does not grant another Reaction. A same-round second-counter diagnostic may explicitly disclose an actual otherwise-lawful provider prerequisite; do not invent a Reaction source. Show a useful numerical payment/award transition plus replay/round-boundary behavior with sufficient durable state.

Attached packet retains the complete received MODEL/cases/procedures/questions/templates and relevant complete class/rule source files, original CANDIDATE bytes, full independent diagnostic report and reconstruction receipt. It is a focused follow-through packet; all other source bytes and both original archives remain preserved in your full Return01 and my original54,459,580-byte download SHA25609e6ea3b629723294d0da5f5551a460c9146e9f428471c8fe359bc394955f30d. Original manifests are historical evidence; the packet has its own current manifest. No supplied code needs to be run.

Return the full exact corrected or explicitly confirmed authoring model with full affected artifacts and reversible complete-before/after references. Do not reopen settled benefits, reduce all-magic scope, alter class recovery law, replace scenarios with rejection-only examples or promote the parent335 feat candidate. Applied525/323/249/173 and50accepted-unapplied remain unchanged; these3remain proposed until this follow-through is independently reconciled. Canonical implementation remains owner-reserved; runtime, human, balance, canon and release gates stay separate.
'''
files['REQUEST.txt']=request.encode('utf-8')
manifest={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT_WHILE_FEAT_REVIEW_ACTIVE','fullOriginalReturnArchive':info(A/'DD_Rank9_Resonance_Fields_3_Part5_Conference_Return_01.zip'),'files':[{'path':k,'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()} for k,v in sorted(files.items())]}
files['PACKET_MANIFEST.json']=encode(manifest)
P.mkdir()
for name,content in files.items():
    dest=P/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
with zipfile.ZipFile(Z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,content in files.items():z.writestr(name,content)
with zipfile.ZipFile(Z) as z:
    assert z.testzip() is None and len(z.namelist())==len(files)
    for name,content in files.items():assert z.read(name)==content
REQUEST.write_bytes(files['REQUEST.txt'])
SCRIPT.write_bytes(Path(__file__).read_bytes())
RECEIPT.write_bytes(encode({'status':'PREPARED_UNSENT','archive':info(Z),'request':info(REQUEST),'manifest':info(P/'PACKET_MANIFEST.json'),'fileCount':len(files),'sourceBindingsVerified':3,'exactOriginalCandidateRetained':True,'localChecks':3099,'localFailures':0,'openFindingLocations':2,'canonicalApplied':False,'sourceInformationDeleted':0}))
print(json.dumps({'receipt':info(RECEIPT),'archive':info(Z),'files':len(files)}))
