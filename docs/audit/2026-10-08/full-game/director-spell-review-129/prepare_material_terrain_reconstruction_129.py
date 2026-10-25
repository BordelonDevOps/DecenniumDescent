"""Fresh source-only replacement conference; no unavailable return is fabricated or executed."""
from pathlib import Path
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-129'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda v:(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
qp=A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json';q=read(qp);g=next(g for g in q['groups'] if g['group']=='material-terrain8');assert g['currentPhase']=='unaccepted-return-artifacts-missing'
cp=G/g['candidate']['path'];c=read(cp);assert sha(cp.read_bytes())==g['candidate']['sha256']
orig=G/g['archive']['path'];assert sha(orig.read_bytes())==g['archive']['sha256'];checks=[]
with zipfile.ZipFile(orig) as z:
 assert z.testzip() is None
 for b in c['sourceBindings']:
  v=z.read('sources/'+b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256'];checks.append({'path':b['path'],'originalExact':True,'currentExact':sha((G/b['path']).read_bytes())==b['sha256']})
old=A/'DD_Material_Terrain8_Current_Conference_121.zip';assert old.stat().st_size==13225946 and sha(old.read_bytes())=='5246f111ce59395d9adb4d30ec79e7ed763d8324a55e3ac3c866ada0a4c30fb5'
with zipfile.ZipFile(old) as z:
 assert z.testzip() is None
 prior=read(A/'spell-review-resume-116/MATERIAL_TERRAIN8_PACKET_121.json')
 notes121=json.loads(z.read('notes/MATERIAL_TERRAIN8_NEXT_CONFERENCE_NOTES.json'))
current=read(G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json');byid={s['id']:s for s in current['spells']}
for r in c['records']:assert r['completeCurrentCatalogSourceAndAccess']==byid[r['spellId']]
extra=[
 {'id':'MT8-129-RETURN-PRESERVATION','question':'Prior121 return files remain unavailable after actual recovery attempts; all original inputs and visible summaries are preserved. Produce explicitly new source-faithful complete authorship from those actual originals and all24 conference questions. Do not claim byte-identical recovery or treat an unavailable summary as selected authority. Preserve all16 original obligations and mark genuinely substituted missing-premise examples separately.'},
 {'id':'MT8-129-DAMAGE-SOURCE','question':'The original Transmute Rock proposal is one4d6 bounded overhead burst, DEXhalf, within20vertical feet and no density/drop multiplier; original roll15 yields7. Prior published summary claimed300/150 and90HP+210overkill.300 cannot be4d6. Resolve the actual procedure/source rule expressly and use legal individual dice plus actual defense/Wound/Null/life ordering. A synthetic2000HP actor or correct subtraction does not validate an impossible damage source.'},
 {'id':'MT8-129-CURRENT-AUTHORITY','question':'Use current applied616/232 context, including actual Body8/Time5/Transport6 and applied72, superseding older pending labels only within exact receipts. Magic7 is still pending until supplied independent application. Preserve source-qualified normal Action/BA phases or real acquired providers, ordinary Ready after-trigger ordering, precise real actor progression and positive acquired casts, and per-recipient/numbered-round ledgers.'},
 {'id':'MT8-129-POSITIVE-CONCRETENESS','question':'Finish all eight useful complete procedures and all24 answers with actual positive operations, real material/recipe/body/support sources and full geometry, clocks, costs, custody and complete before/after reversible values. Synthetic scenario prerequisites without authentic content remain narrow holds; do not replace the whole native benefit with rejection examples or invent generalized physics, vehicle skill, source damage, crafting credentials or cosmology.'}
]
notes={'id':'MATERIAL8-FRESH-RECONSTRUCTION-CONFERENCE-129','status':'PREPARED_UNSENT_NOT_ACCEPTED','identities':g['identities'],'completeOriginalQuestionsUnchanged':c['conferenceQuestions'],'completePriorEightFollowupsUnchanged':notes121['additionalReviewQuestions'],'freshReconstructionFollowups':extra,'originalScenarioTextsUnchanged':c['all16HistoricalScenarioTexts'],'sourceChecks':checks,'priorReturnRecovered':False,'currentCounts':{'reviewedApplied':616,'pending':232,'acceptedUnapplied':0},'scope':'Fresh source-faithful authorship requested, not fabricated recovery. No new rule adoption or supplied/historical program execution. No runtime/human/balance/cosmology/release claim.'}
assert len(notes['completeOriginalQuestionsUnchanged'])==16 and len(notes['completePriorEightFollowupsUnchanged'])==8
files={}
with zipfile.ZipFile(A/'DD_VitalityMatter10_Director_Conference_128.zip') as z:
 for n in z.namelist():
  if n.startswith(('accepted-context/','accepted/','current/')):files[n]=z.read(n)
files['original/'+old.name]=old.read_bytes();files['ORIGINAL_CANDIDATE_02.json']=cp.read_bytes();files['INDEPENDENT_RECONSTRUCTION_129.json']=enc(notes)
for name,path in [('history/ORIGINAL_SEND_RECEIPT_121.json',A/'spell-review-resume-116/MATERIAL_TERRAIN8_PACKET_121.json'),('history/ORIGINAL_REQUEST_121.txt',A/'spell-review-resume-116/GPT_MATERIAL_TERRAIN8_ACTUAL_REQUEST_121.txt'),('history/MISSING_RETURN_123.txt',A/'director-spell-review-123/MATERIAL8_UNAVAILABLE_RETURN_AX.txt'),('history/PUBLISHED_RETURN_TRIAGE_123.json',A/'director-spell-review-123/MATERIAL8_TRIAGE.json')]:files[name]=path.read_bytes()
files['current/authored_review_index_129.json']=(G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json').read_bytes()
guard=read(D/'PENDING232_NATIVE_SOURCE_GUARD_129.json');guard['records']=[r for r in guard['records'] if r['id'] in g['identities']];files['NATIVE_SOURCE_GUARD_129.json']=enc(guard)
files['README.md']=b'Material/Terrain8 fresh reconstruction conference129. Read INDEPENDENT_RECONSTRUCTION_129.json and preserved original/current authorities.24 original questions plus4 focused followups;16 original scenario obligations. Previous return is unavailable, not accepted. Produce complete new source-faithful data-only review with no supplied or historical program execution. Current616applied/232pending; exact independent acceptance before application.\n'
manifest={'id':'MATERIAL8-RECONSTRUCTION-CONFERENCE-129-MANIFEST','files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in files.items()]};files['MANIFEST.json']=enc(manifest)
out=A/'DD_MaterialTerrain8_Reconstruction_Conference_129.zip';assert not out.exists()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in files.items():z.writestr(n,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for b in manifest['files']:v=z.read(b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256']
receipt={'id':'MATERIAL8-RECONSTRUCTION-PACKET-129','status':'PREPARED_NOT_SENT','archive':{'path':str(out),'bytes':out.stat().st_size,'sha256':sha(out.read_bytes())},'members':len(files),'bindings':len(manifest['files']),'questions':28,'requiredMainCases':16,'sourceChecks':len(checks),'priorReturnRecovered':False,'canonicalChanges':False}
(D/'MATERIAL8_RECONSTRUCTION_NOTES_129.json').write_bytes(enc(notes));rp=D/'MATERIAL8_RECONSTRUCTION_PACKET_129.json';rp.write_bytes(enc(receipt))
g['previousPhase']=g['currentPhase'];g['currentPhase']='fresh-reconstruction-conference-prepared-129-unsent';g['priorPreparedPackets']=[g['currentPacket']];g['currentPacket']=str(out);g['currentPacketBinding']=receipt['archive'];g['currentPacketReceipt']=str(rp);g['actuallySent']=False;g['nextAction']='Submit explicitly new source-faithful reconstruction with current applied context; previous return remains unavailable and unaccepted.';qp.write_bytes(enc(q))
print(json.dumps(receipt,indent=2))
