import gzip,hashlib,json,pathlib,zipfile,io,copy
R=pathlib.Path('C:/Github/DecenniumDescent')
D=R/'docs/audit/2026-10-08/full-game/director-spell-review-129'
I=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
C=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
P=R/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139'
IDS=['summon-bone-colossus','black-reaping','chain-of-the-grave','finger-of-death','plague-wind','metal-to-glass','titanic-grip','flash-freeze','transmute-being','regenerate']
REVIEW='VITALITYMATTER10-EXACT-AUTHORED-ACCEPTANCE-139'
def sha(b): return hashlib.sha256(b).hexdigest()
def j(p): return json.loads(p.read_text(encoding='utf-8'))
def checkbind(b):
 p=R/pathlib.PurePosixPath(b['path']); raw=p.read_bytes()
 assert len(raw)==b['bytes'] and sha(raw)==b['sha256'],b['path']
 return raw
before=D/'authored_review_index.before_vitalitymatter10_139.json'
before_bytes=before.read_bytes(); old=j(before); idx=j(I); catalog=j(C)
assert old['authoredCounts']=={'reviewed':668,'pending':180}
assert idx['authoredCounts']=={'reviewed':678,'pending':170}
assert idx['representationCounts']['completeReviewedStandaloneProcedures']==402
assert sha(C.read_bytes())==old['sourceCatalogSha256']==idx['sourceCatalogSha256']
ops=j(D/'VITALITYMATTER10_INDEX_OPERATIONS_139.json')
assert ops['before']['sha256']==sha(before_bytes) and ops['after']['sha256']==sha(I.read_bytes())
after_copy=copy.deepcopy(idx)
for op in ops['operations']:
 assert op['identity'] in IDS and idx['entries'][op['index']]==op['after']
 after_copy['entries'][op['index']]=op['before']
assert {x['identity'] for x in ops['operations']}==set(IDS)
after_copy['additionalStandaloneEnvelopes']=after_copy['additionalStandaloneEnvelopes'][:-1]
after_copy['authoredCounts']=copy.deepcopy(old['authoredCounts'])
after_copy['representationCounts']=copy.deepcopy(old['representationCounts'])
assert after_copy==old
backup=D/'authored_review_index.before_vitalitymatter10_139.json'
assert sha(before_bytes)==j(D/'vitalitymatter10_return01_139_clean01'/'VITALITYMATTER10_RETURN01_CLEAN01_INDEPENDENT_AUDIT_139.json')['authorityBefore']['indexSha256']
delivery=j(D/'vitalitymatter10_return01_139_clean01'/'DIRECTOR_RETURN_DELIVERY.json')
zip_path=D/'vitalitymatter10_return01_139_clean01'/'DD_VitalityMatter10_Director_Return01_139_Clean01.zip'
zip_bytes=zip_path.read_bytes(); assert len(zip_bytes)==delivery['bytes'] and sha(zip_bytes)==delivery['sha256']
with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
 assert z.testzip() is None
 package={n:z.read(n) for n in z.namelist()}
casebook=package['CASEBOOK.json']
assert gzip.decompress((P/'CASEBOOK.json.gz').read_bytes())==casebook
manifest=j(P/'CANDIDATE_PACKAGE_MANIFEST.json')
assert len(manifest['files'])==23
for rec in manifest['files']:
 raw=(P/rec['path']).read_bytes(); assert len(raw)==rec['bytes'] and sha(raw)==rec['sha256'],rec['path']
model=j(P/'MODEL.json'); receipt=j(D/f'{REVIEW}.json')
assert 'candidatePackageManifestBinding' not in model and 'candidatePackageManifestBinding' not in receipt
assert receipt['candidateEnvelopeBinding']['sha256']==sha((P/'MODEL.json').read_bytes())
membind={'path':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/CANDIDATE_PACKAGE_MANIFEST.json','bytes':(P/'CANDIDATE_PACKAGE_MANIFEST.json').stat().st_size,'sha256':sha((P/'CANDIDATE_PACKAGE_MANIFEST.json').read_bytes())}
assert all(e['candidatePackageManifestBinding']==membind for e in idx['entries'] if e['id'] in IDS)
assert len(j(P/'HOLD_REGISTER.json')['holds'])==19
assert j(D/'VITALITYMATTER10_APPLICATION_VALIDATION_139.json')['status']=='PASS'
app=j(D/'VITALITYMATTER10_APPLICATION_139.json')
assert app['counts']['after']=={'reviewed':678,'pending':170,'acceptedUnapplied':0}
assert all(next(e for e in idx['entries'] if e['id']==sid)['sourceStatus']=='blocked-pending-operational-review' for sid in IDS)
pending={e['id'] for e in idx['entries'] if e['authoredStatus']=='pending-authored-procedure'}
q=j(D/'CURRENT_SPELL_QUEUE_139.json'); pa=j(D/'CURRENT170_PENDING_IDENTITY_AUDIT_139.json')
assert q['currentAuthority']['pending']==pa['pendingCount']==len(pending)==170
assert set(pa['pendingIds'])==pending
gids=[sid for g in q['currentPendingGroups'] for sid in g['pendingIds']]
assert len(gids)==len(set(gids))==170 and set(gids)==pending
assert q['nextGroup']['group']==q['currentPendingGroups'][0]['group']=='material-terrain8'
assert q['currentAuthority']['reviewedApplied']==678 and q['currentAuthority']['acceptedUnapplied']==0
print(json.dumps({'status':'PASS','applied':len(IDS),'pending':len(pending),'sourceCatalogUnchanged':True,'candidateManifestFiles':len(manifest['files']),'returnZipBytes':len(zip_bytes),'returnZipSha256':sha(zip_bytes),'nextGroup':q['nextGroup']['group'],'nextCount':q['nextGroup']['pendingCount'],'checks':['inverse-index-replay','exact-source-card-preservation','package-manifest','candidate-manifest','all-current-pending-groups','queue-authority']},indent=2))