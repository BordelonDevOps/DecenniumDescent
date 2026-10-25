import hashlib,json,zipfile,datetime
from pathlib import Path
BASE=Path(r'C:\Github\DecenniumDescent')
AUD=BASE/'docs/audit/2026-10-08/full-game/director-spell-review-129'
EVID=BASE/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/information8_reviewed_129'
OUT=AUD/'DD_FindThePath_Applied_Context_129.zip'
INDEX=BASE/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
QUEUE=BASE/'docs/audit/2026-10-08/full-game/spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json'
EYE=BASE/'docs/audit/2026-10-08/full-game/DD_EyeJudgement1_Director_Conference_127.zip'
EYE_REQ=AUD/'INFORMATION8_EYE1_NEXT_REQUEST_129.txt'
UPLOAD=AUD/'INFORMATION8_EYE1_LIBRARY_UPLOAD_129.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return Path(p).read_bytes()
source={'id':'INFORMATION8-FINDPATH-APPLIED-CONTEXT-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'currentCounts':{'applied':636,'pending':212,'standalone':360,'scopedInterfaces':173,'acceptedUnapplied':0},'newlyAppliedIds':['find-the-path'],'previouslyAppliedInformation8Ids':['arcane-eye','concordant-mindlink','faction-prophecy','faction-destiny','legend-lore','prophetic-frenzy','resonance-prophecy'],'retainedHolds':['PROTECTED-SHORTER-TERRAIN','GENERIC-CAMPAIGN-CONTENT','all previously established source/content/runtime/human/balance/cosmology/temporal/release holds'],'recipientOutput':'Indeterminate','privateTopologyQualificationPreserved':True,'runtimeSelectionEnabled':False,'closedCohortsReopened':False,'exactReturn03':{'name':'DD_Information8_Director_Return03_131.zip','bytes':492999414,'sha256':'007ef53858a6f5bc69d7811b58d18d19f8434821362977a4a310a831a5c8fad3'},'nextConference':{'name':EYE.name,'localPath':str(EYE),'bytes':EYE.stat().st_size,'sha256':sha(EYE.read_bytes()),'alreadyUploadedLibraryId':'libfile_b1d703fd1cac8191a09589e80ca9e1e0','directorRequestPreviouslySent':False},'authority':'Current authored_review_index.json and this packet supersede all historical pending labels.'}
files={
 'APPLIED_CONTEXT.json':json.dumps(source,ensure_ascii=False,indent=2).encode()+b'\n',
 'INFORMATION8_EXACT_ACCEPTANCE_129.json':read(AUD/'INFORMATION8_EXACT_ACCEPTANCE_129.json'),
 'INFORMATION8_RETURN03_INDEPENDENT_EXACT_AUDIT_129.json':read(AUD/'INFORMATION8_RETURN03_INDEPENDENT_EXACT_AUDIT_129.json'),
 'INFORMATION8_FINDTHEPATH_APPLICATION_129.json':read(AUD/'INFORMATION8_FINDTHEPATH_APPLICATION_129.json'),
 'INFORMATION8_FINDPATH_APPLICATION_VALIDATION_129.json':read(AUD/'INFORMATION8_FINDPATH_APPLICATION_VALIDATION_129.json'),
 'INFORMATION8_FINDPATH_INDEX_OPERATIONS_129.json':read(AUD/'INFORMATION8_FINDPATH_INDEX_OPERATIONS_129.json'),
 'INFORMATION8_FINDPATH_EXACT_REFERENCE_MODEL_129.json':read(AUD/'INFORMATION8_FINDPATH_EXACT_REFERENCE_MODEL_129.json'),
 'CURRENT212_PENDING_IDENTITY_AUDIT_129.json':read(AUD/'CURRENT212_PENDING_IDENTITY_AUDIT_129.json'),
 'CURRENT_SPELL_QUEUE_129.json':read(QUEUE),
 'CURRENT_HANDOFF_129.json':read(AUD/'CURRENT_HANDOFF_129.json'),
 'authored_review_index.json':read(INDEX),
 'INFORMATION8_PROCEDURES.json':read(EVID/'PROCEDURES.json'),
 'INFORMATION8_SHARED_RULES.json':read(EVID/'SHARED_RULES.json'),
 'INFORMATION8_NATIVE_ACCESS_RECORDS.json':read(EVID/'NATIVE_ACCESS_RECORDS.json'),
 'INFORMATION8_HOLDS.json':read(EVID/'HOLDS.json'),
 'INFORMATION8_ORIGINAL_CASE_DISPOSITIONS.json':read(EVID/'ORIGINAL_CASE_DISPOSITIONS.json'),
 'INFORMATION8_QUESTION_DISPOSITIONS.json':read(EVID/'QUESTION_DISPOSITIONS.json'),
 'INFORMATION8_CASE_DI6-04-A.json':read(EVID/'cases/DI6-04-A.json'),
 'INFORMATION8_CASE_DI6-04-B.json':read(EVID/'cases/DI6-04-B.json'),
 'EYE1_CURRENT_SOURCE_BASELINE.json':read(AUD/'EYE1_CURRENT_CLASS_SOURCE_BASELINE_129.json'),
 'EYE1_LIBRARY_UPLOAD_RECEIPT.json':read(UPLOAD),
 'EYE1_PENDING_REQUEST_DRAFT.txt':read(EYE_REQ),
}
ops=json.loads(read(EVID/'EVENT_OPERATIONS.json'))
selected=[x for x in ops if x['eventId']=='DI6-04-B/actual-crossbar-after-snapshot:12']
assert len(selected)==1
files['INFORMATION8_FINDPATH_CORRECTED_EVENT_OPERATION.json']=(json.dumps(selected[0],ensure_ascii=False,indent=2)+'\n').encode()
manifest={'algorithm':'SHA-256','excludedSelf':'MANIFEST.json','members':[{'path':name,'bytes':len(data),'sha256':sha(data)} for name,data in sorted(files.items())]}
files['MANIFEST.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name,data in files.items(): z.writestr(name,data)
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)
 loaded=json.loads(z.read('MANIFEST.json'))
 for m in loaded['members']:
  b=z.read(m['path']);assert len(b)==m['bytes'] and sha(b)==m['sha256']
print(json.dumps({'path':str(OUT),'bytes':OUT.stat().st_size,'sha256':sha(OUT.read_bytes()),'members':len(files),'nextConference':source['nextConference'],'counts':source['currentCounts']},ensure_ascii=False,indent=2))
