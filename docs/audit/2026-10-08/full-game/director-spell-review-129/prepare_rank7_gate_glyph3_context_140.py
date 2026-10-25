import hashlib,json,pathlib,zipfile
from datetime import datetime,timezone

R=pathlib.Path('C:/Github/DecenniumDescent')
A=R/'docs/audit/2026-10-08/full-game/director-spell-review-129'
IDX=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CAT=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE=A/'CURRENT_SPELL_QUEUE_140.json'
PA=A/'CURRENT162_PENDING_IDENTITY_AUDIT_140.json'
HAND=A/'CURRENT_HANDOFF_140.json'
CAND=R/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank7_gate_glyph_3_source_conference_01.json'
ARCH=R/'docs/audit/2026-10-08/full-game/DD_Rank7_Gate_Glyph_3_Source_Conference_01.zip'
PREV=R/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/materialterrain8_reviewed_140'
OUT=A/'DD_MaterialTerrain8_Applied_Rank7GateGlyph3_Context_140.zip'
REQ=A/'RANK7_GATE_GLYPH3_NEXT_REQUEST_140.txt'
DEL=A/'DD_MaterialTerrain8_Applied_Rank7GateGlyph3_Context_140_DELIVERY.json'
IDS=['chain-gate','symbol','symbol-of-death']
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}

idx=json.loads(IDX.read_text(encoding='utf-8'));q=json.loads(QUEUE.read_text(encoding='utf-8'));pa=json.loads(PA.read_text(encoding='utf-8'))
group=q['currentPendingGroups'][0]
assert group['group']=='rank7-gate-glyph3' and group['pendingIds']==IDS and group['pendingCount']==3
assert idx['authoredCounts']=={'reviewed':686,'pending':162} and pa['pendingCount']==162 and len(pa['pendingIds'])==162
assert bind(CAND)==group['candidate'] and bind(ARCH)==group['archive']
assert bind(IDX)==pa['indexBinding'] and bind(CAT)==pa['catalogBinding']

request=f'''DIRECTOR REQUEST — RANK7 GATE/GLYPH 3 — LIVE AUTHORITY 686/162

Review exactly these three still-pending ordinary spell identities: chain-gate, symbol, and symbol-of-death. You are the design/review director. Source proposal: {group['candidate']['path']} ({group['candidate']['bytes']} bytes, SHA-256 {group['candidate']['sha256']}). Exact source conference archive: {group['archive']['path']} ({group['archive']['bytes']} bytes, SHA-256 {group['archive']['sha256']}).

The attached context ZIP binds the current authored review index and catalog, current 162-identity audit, live queue and handoff, the exact source candidate/archive, and the immediately prior accepted Material/Terrain8 receipt/model/holds. The canonical current authority is 686 reviewed/applied, 162 pending, zero accepted-unapplied; complete reviewed standalone procedures: 410. The former 232 count is historical. Do not reopen feats, cohorts, the completed 335-feat review, completed 16 spells, or any applied batch.

Return a complete proposed authored operational procedure for each of the three identities, with explicit selections for every original question, exact source/native card and all class-access rows preserved, full-state reversible test/replace cases, original questions/scenarios/holds retained, and a source verification manifest. Use source-supported facts where present. Mark every local design choice as new spell-local authorship; do not promote it to global authority. Retain unresolved source and physical premises as whole-case or branch holds. Avoid game-wide balance, release, or runtime claims.

Do not execute source or historical programs, do not run the game, and do not change the canonical index/catalog. Return one clean ZIP with a complete exact member manifest and SHA-256 bindings, plus a separate delivery JSON bound to the ZIP. The return is proposed only: accepted=false and applied=false at 686/162. No hidden or temporary archive members. Report exact counts for procedures, questions, cases/branches, events, reversible operations, checks passed/failed, and holds. Keep all source archives and candidate data byte-exact.
'''
REQ.write_text(request,encoding='utf-8',newline='\n')
files=[
 ('authority/authored_review_index.json',IDX),('authority/catalog.json',CAT),
 ('authority/CURRENT_SPELL_QUEUE_140.json',QUEUE),('authority/CURRENT162_PENDING_IDENTITY_AUDIT_140.json',PA),('authority/CURRENT_HANDOFF_140.json',HAND),
 ('authority/materialterrain8/MODEL.json',PREV/'MODEL.json'),('authority/materialterrain8/EXACT_ACCEPTANCE.json',PREV/'EXACT_ACCEPTANCE.json'),
 ('authority/materialterrain8/HOLD_ADJUDICATION.json',PREV/'HOLD_ADJUDICATION.json'),('authority/materialterrain8/INDEPENDENT_AUDIT.json',PREV/'INDEPENDENT_AUDIT.json'),
 ('authority/materialterrain8/APPLICATION.json',A/'MATERIALTERRAIN8_APPLICATION_140.json'),
 ('source/rank7_gate_glyph_3_source_conference_01.json',CAND),('history/DD_Rank7_Gate_Glyph_3_Source_Conference_01.zip',ARCH),
 ('request/RANK7_GATE_GLYPH3_NEXT_REQUEST_140.txt',REQ)
]
members=[]
for arc,p in files:
 b=p.read_bytes();members.append({'path':arc,'bytes':len(b),'sha256':sha(b),'sourcePath':p.relative_to(R).as_posix()})
assert all(p.is_file() for _,p in files)
manifest={'id':'RANK7-GATE-GLYPH3-CONTEXT-MANIFEST-140','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'authority':{'reviewed':686,'pending':162,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':410},'scope':IDS,'members':members,'memberCount':len(members)}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for arc,p in files:z.write(p,arc)
 z.writestr('CONTEXT_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
blob=OUT.read_bytes()
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None and len(z.namelist())==len(members)+1
 for rec in members:
  b=z.read(rec['path']);assert len(b)==rec['bytes'] and sha(b)==rec['sha256']
delivery={'id':'RANK7-GATE-GLYPH3-CONTEXT-DELIVERY-140','file':OUT.name,'bytes':len(blob),'sha256':sha(blob),'members':len(members)+1,'manifestBindings':len(members),'authority':manifest['authority'],'scope':IDS,'requestBinding':next(x for x in members if x['path'].endswith('.txt')),'candidate':bind(CAND),'archive':bind(ARCH),'accepted':False,'applied':False}
DEL.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(delivery,ensure_ascii=False,indent=2))
