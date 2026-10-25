import copy, hashlib, json, os, pathlib
from datetime import datetime, timezone
ROOT=pathlib.Path('C:/Github/DecenniumDescent')
D=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
C=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139'
I=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
IDS=['summon-bone-colossus','black-reaping','chain-of-the-grave','finger-of-death','plague-wind','metal-to-glass','titanic-grip','flash-freeze','transmute-being','regenerate']
REVIEW='VITALITYMATTER10-EXACT-AUTHORED-ACCEPTANCE-139'
def sha(b): return hashlib.sha256(b).hexdigest()
def writej(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def bind(p,rel=None):
 b=p.read_bytes(); return {'path':rel or p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def same(p,b): p.write_bytes(b)
raw=I.read_bytes(); idx=json.loads(raw)
assert idx['authoredCounts']=={'reviewed':678,'pending':170}
assert len([e for e in idx['entries'] if e['authoredStatus']=='pending-authored-procedure'])==170
assert all(next(e for e in idx['entries'] if e['id']==sid)['reviewId']==REVIEW for sid in IDS)
backup=D/'authored_review_index.before_vitalitymatter10_binding_repair_139.json'
assert not backup.exists(); backup.write_bytes(raw)
modelp=C/'MODEL.json'; model=json.loads(modelp.read_text(encoding='utf-8'))
assert 'candidatePackageManifestBinding' in model
model.pop('candidatePackageManifestBinding')
writej(modelp,model)
model_binding=bind(modelp,'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/MODEL.json')
receiptp=D/f'{REVIEW}.json'; receipt=json.loads(receiptp.read_text(encoding='utf-8'))
receipt.pop('candidatePackageManifestBinding',None)
receipt['candidateEnvelopeBinding']=model_binding
writej(receiptp,receipt); same(C/'EXACT_ACCEPTANCE.json',receiptp.read_bytes())
manifestp=C/'CANDIDATE_PACKAGE_MANIFEST.json'
def write_manifest():
 files=[]
 for p in sorted(C.iterdir(),key=lambda p:p.name):
  if p.is_file() and p.name!='CANDIDATE_PACKAGE_MANIFEST.json':
   b=p.read_bytes(); files.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
 writej(manifestp,{'id':'VITALITYMATTER10-CANDIDATE-PACKAGE-MANIFEST-139','files':files,'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'})
 return files
files=write_manifest()
manifest_binding=bind(manifestp,'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/CANDIDATE_PACKAGE_MANIFEST.json')
# The exact receipt contains no manifest hash, so this final manifest is stable and non-circular.
for rec in files:
 b=(C/rec['path']).read_bytes(); assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],rec['path']
receipt_binding=bind(receiptp)
old_after=copy.deepcopy(idx)
for row in idx['entries']:
 if row['id'] in IDS:
  row['completeEnvelopeBinding']=model_binding
  row['candidatePackageManifestBinding']=manifest_binding
  row['authoredAcceptanceReceipt']=receipt_binding
for env in idx['additionalStandaloneEnvelopes']:
 if env.get('reviewId')==REVIEW:
  env['binding']=model_binding
  env['candidatePackageManifestBinding']=manifest_binding
  env['authority']=receipt_binding
assert idx['authoredCounts']=={'reviewed':678,'pending':170}
tmp=I.with_suffix('.json.tmp'); writej(tmp,idx); os.replace(tmp,I)
ops_path=D/'VITALITYMATTER10_INDEX_OPERATIONS_139.json'
ops=json.loads(ops_path.read_text(encoding='utf-8'))
for op in ops['operations']:
 row=next(e for e in idx['entries'] if e['id']==op['identity'])
 op['after']=copy.deepcopy(row)
ops['after']=bind(I)
ops['bindingMetadataRepair']={'backup':backup.relative_to(ROOT).as_posix(),'before':{'bytes':len(raw),'sha256':sha(raw)},'after':bind(I)}
writej(ops_path,ops)
app_path=D/'VITALITYMATTER10_APPLICATION_139.json'; app=json.loads(app_path.read_text(encoding='utf-8'))
app['after']=bind(I); app['candidateEnvelope']=model_binding; app['candidatePackageManifest']=manifest_binding; app['acceptanceReceipt']=receipt_binding
app['metadataBindingRepair']={'backup':backup.relative_to(ROOT).as_posix(),'reason':'Removed circular self-reference from model/acceptance; candidate manifest now binds stable model and receipt bytes.'}
writej(app_path,app)
val_path=D/'VITALITYMATTER10_APPLICATION_VALIDATION_139.json'; val=json.loads(val_path.read_text(encoding='utf-8'))
val['afterIndexHash']=sha(I.read_bytes()); val['afterIndexBytes']=I.stat().st_size
val['candidateManifestBindingsPassed']=True
val['metadataBindingRepairValidated']=True
writej(val_path,val)
# Verify final index references all exact final files.
for sid in IDS:
 row=next(e for e in idx['entries'] if e['id']==sid)
 for key in ['completeEnvelopeBinding','candidatePackageManifestBinding','authoredAcceptanceReceipt']:
  bnd=row[key]; p=ROOT/pathlib.PurePosixPath(bnd['path']); assert p.stat().st_size==bnd['bytes'] and sha(p.read_bytes())==bnd['sha256'],(sid,key)
assert not json.loads(modelp.read_text()) .get('candidatePackageManifestBinding')
assert not json.loads(receiptp.read_text()).get('candidatePackageManifestBinding')
print(json.dumps({'status':'REPAIRED_AND_VERIFIED','model':model_binding,'manifest':manifest_binding,'receipt':receipt_binding,'index':bind(I),'candidateManifestFiles':len(files),'pending':170},indent=2))