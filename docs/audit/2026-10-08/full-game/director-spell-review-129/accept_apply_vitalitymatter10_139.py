from __future__ import annotations
import copy, gzip, hashlib, io, json, os, pathlib, shutil, zipfile
from datetime import datetime, timezone

ROOT = pathlib.Path('C:/Github/DecenniumDescent')
AUDIT_ROOT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RETURN_DIR = AUDIT_ROOT / 'vitalitymatter10_return01_139_clean01'
ZIP = RETURN_DIR / 'DD_VitalityMatter10_Director_Return01_139_Clean01.zip'
DELIVERY = RETURN_DIR / 'DIRECTOR_RETURN_DELIVERY.json'
AUDIT = RETURN_DIR / 'VITALITYMATTER10_RETURN01_CLEAN01_INDEPENDENT_AUDIT_139.json'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE_BEFORE = AUDIT_ROOT / 'CURRENT_SPELL_QUEUE_138.json'
PENDING_BEFORE = AUDIT_ROOT / 'CURRENT180_PENDING_IDENTITY_AUDIT_138.json'
HANDOFF_BEFORE = AUDIT_ROOT / 'CURRENT_HANDOFF_138.json'
CANDIDATE = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139'
STAGING = CANDIDATE.with_name(CANDIDATE.name + '.staging')
MANUSCRIPT = ROOT / 'docs/spells/candidates/VITALITYMATTER10_REVIEWED_139.md'
REVIEW_ID = 'VITALITYMATTER10-EXACT-AUTHORED-ACCEPTANCE-139'
IDS = ['summon-bone-colossus','black-reaping','chain-of-the-grave','finger-of-death','plague-wind','metal-to-glass','titanic-grip','flash-freeze','transmute-being','regenerate']
APP_PATH = 'docs/audit/2026-10-08/full-game/director-spell-review-129/VITALITYMATTER10_APPLICATION_139.json'

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def writej(path: pathlib.Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + chr(10), encoding='utf-8', newline=chr(10))
def bind(path: pathlib.Path, rel=None):
    b=path.read_bytes()
    return {'path': rel or path.relative_to(ROOT).as_posix(), 'bytes':len(b), 'sha256':sha(b)}
def resolve_pointer(root, pointer):
    value=root
    for token in pointer.strip('/').split('/') if pointer else []:
        token=token.replace('~1','/').replace('~0','~')
        value=value[int(token)] if isinstance(value,list) else value[token]
    return value

assert ZIP.is_file() and DELIVERY.is_file() and AUDIT.is_file()
assert not CANDIDATE.exists() and not STAGING.exists() and not MANUSCRIPT.exists()
delivery=json.loads(DELIVERY.read_text(encoding='utf-8'))
archive_bytes=ZIP.read_bytes(); archive_hash=sha(archive_bytes)
audit=json.loads(AUDIT.read_text(encoding='utf-8'))
assert audit['decision']=='PASS_READY_FOR_EXACT_ACCEPTANCE_WITH_RETAINED_HOLDS'
assert audit['directorReturn']['sha256']==archive_hash and audit['directorReturn']['bytes']==len(archive_bytes)
assert delivery['bytes']==len(archive_bytes) and delivery['sha256']==archive_hash
assert delivery['accepted'] is False and delivery['applied'] is False
with zipfile.ZipFile(io.BytesIO(archive_bytes)) as z:
    assert z.testzip() is None
    names=z.namelist(); outer=json.loads(z.read('MANIFEST.json'))
    expected={x.get('path',x.get('file')):x for x in outer['files']}
    assert len(names)==336 and len(expected)==335
    assert set(names)-{'MANIFEST.json'}==set(expected)
    package={n:z.read(n) for n in names}
    for n,rec in expected.items():
        assert len(package[n])==rec.get('bytes',rec.get('length')), n
        assert sha(package[n])==rec.get('sha256',rec.get('hash')), n
assert outer['accepted'] is False and outer['applied'] is False

index_bytes=INDEX.read_bytes(); before=json.loads(index_bytes)
catalog_bytes=CATALOG.read_bytes(); catalog=json.loads(catalog_bytes)
assert before['authoredCounts']=={'reviewed':668,'pending':180}
assert before['representationCounts']['completeReviewedStandaloneProcedures']==392
assert len([e for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure'])==180
assert sha(catalog_bytes)==before['sourceCatalogSha256']
assert package['authority/authored_review_index.json']==index_bytes
assert package['authority/catalog.json']==catalog_bytes

procedures=json.loads(package['PROCEDURES.json'])
assert [p['id'] for p in procedures]==IDS
by_id={p['id']:p for p in procedures}
source_conf=json.loads(package['ORIGINAL_SOURCE_CONFERENCE.json'])
risk={r['spellId']:r['riskTier'] for r in source_conf['records']}
assert set(risk)==set(IDS)
native_access=json.loads(package['NATIVE_ACCESS_RECORDS.json'])
rows={e['id']:e for e in before['entries']}
current_cards={s['id']:s for s in catalog['spells']}
for sid in IDS:
    row=rows[sid]; p=by_id[sid]; card=current_cards[sid]
    assert row['authoredStatus']=='pending-authored-procedure'
    assert row['sourceStatus']=='blocked-pending-operational-review'
    assert p['accepted'] is False and p['applied'] is False
    assert p['status']=='PROPOSED_FOR_EXACT_INDEPENDENT_REVIEW'
    assert p['completeNativeSourceAndAccessUnchanged']==card
    assert native_access[sid]==card
assert sum(len(native_access[sid].get('classAccess',{})) for sid in IDS)==40

casebook_bytes=package['CASEBOOK.json']; casebook=json.loads(casebook_bytes)
assert len(casebook['mainCases'])==21 and len(casebook['branches'])==23 and len(casebook['allCases'])==44
case_ids={sid:[c['id'] for c in casebook['allCases'] if c['spellId']==sid] for sid in IDS}
assert all(case_ids[sid] for sid in IDS)
shared=json.loads(package['SHARED_RULES.json'])
source_binding=bind(ZIP)
source_conf_archive=ROOT/'docs/audit/2026-10-08/full-game/DD_VitalityMatter10_Director_Conference_128.zip'
original_source_binding=bind(source_conf_archive)
holds=json.loads(package['HOLD_REGISTER.json'])
assert len(holds['holds'])==19 and holds['accepted'] is False and holds['applied'] is False

# Stage a review envelope containing the complete authored evidence needed to reproduce the acceptance.
STAGING.mkdir(parents=True)
selected=[
 'ACTOR_PROFILES.json','ARTIFACT_BINDINGS.json','DELIVERY_CONTENTS.json',
 'HOLD_REGISTER.json','NATIVE_ACCESS_RECORDS.json','NEW_NATIVE_PROFILES.json',
 'ORIGINAL_FUTURE_OBLIGATION_DISPOSITIONS.json','ORIGINAL_MAIN_CASE_DISPOSITIONS.json',
 'ORIGINAL_QUESTIONS_CASES_AND_FUTURE_OBLIGATIONS.json','ORIGINAL_SOURCE_CONFERENCE.json',
 'PROCEDURES.json','QUESTION_DISPOSITIONS.json','SHARED_RULES.json',
 'SOURCE_VERIFICATION.json','STANDALONE_PROCEDURES.md','VALIDATION.json','VALIDATION_FINAL.json'
]
for name in selected: (STAGING/name).write_bytes(package[name])
(STAGING/'CASEBOOK.json.gz').write_bytes(gzip.compress(casebook_bytes,mtime=0))
with gzip.open(STAGING/'CASEBOOK.json.gz','rb') as f: assert f.read()==casebook_bytes
(STAGING/'DIRECTOR_RETURN_MANIFEST.json').write_bytes(package['MANIFEST.json'])
(STAGING/'INDEPENDENT_AUDIT.json').write_bytes(AUDIT.read_bytes())
(STAGING/'DIRECTOR_RETURN_DELIVERY.json').write_bytes(DELIVERY.read_bytes())

model_spells=[]
for idx,sid in enumerate(IDS):
    p=by_id[sid]; native=p['completeNativeSourceAndAccessUnchanged']; row=rows[sid]
    model_spells.append({
      'id':sid,'name':native['name'],'riskTier':risk[sid],
      'status':'INDEPENDENTLY_ACCEPTED_AUTHORED_PROCEDURE_WITH_RETAINED_HOLDS',
      'completeNativeAndAccess':native,'procedure':p['procedure'],
      'directorProcedureRecordPointer':f'/PROCEDURES/{idx}',
      'sharedRuleIds':p['sharedRuleIds'],
      'sourceArchiveLocator':f'{ZIP.name}!PROCEDURES.json#{sid}',
      'originalSourceBinding':native['source'],'originalSourcePointer':row['wholeCardPointer'],
      'sourceCatalogKey':sid,'reviewFlagsPreserved':native.get('reviewFlags',[]),
      'caseEvidence':case_ids[sid],'runtimeSelectionEnabled':False,
      'directorReturnStatusBeforeAcceptance':p['status']
    })
scope=('Only the ten named VitalityMatter10 authored operational procedures and their selected case evidence are accepted. '
       'The 19 explicit source/content and unavailable-branch holds remain open; no substitute is treated as source proof. '
       'Native source cards, class access, source status, catalog and global/shared rules outside this exact scope are unchanged. '
       'This closes authored procedure review only. Runtime selection remains disabled; no source program, runtime, human-play, '
       'balance, cosmology, or release approval is claimed.')
question_dispositions=json.loads(package['QUESTION_DISPOSITIONS.json'])
main_dispositions=json.loads(package['ORIGINAL_MAIN_CASE_DISPOSITIONS.json'])
future_dispositions=json.loads(package['ORIGINAL_FUTURE_OBLIGATION_DISPOSITIONS.json'])
model={
 'schemaVersion':3,'moduleId':'vitalitymatter10-reviewed-139',
 'status':'EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS','scope':scope,
 'acceptedIds':IDS,
 'excludedPendingIds':sorted(e['id'] for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure' and e['id'] not in IDS),
 'sharedRules':[{'id':k,'rule':v} for k,v in shared.items()],
 'spells':model_spells,
 'questionDispositions':question_dispositions,
 'originalMainCaseDispositions':main_dispositions,
 'originalFutureObligationDispositions':future_dispositions,
 'casebookFile':'CASEBOOK.json.gz',
 'casebookEncoding':'gzip; exact decompression reproduces the director return CASEBOOK.json member',
 'casebookSourceMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook_bytes),'sha256':sha(casebook_bytes)},
 'nativeAccessFile':'NATIVE_ACCESS_RECORDS.json','actorProfilesFile':'ACTOR_PROFILES.json',
 'newNativeProfilesFile':'NEW_NATIVE_PROFILES.json','holdsFile':'HOLD_REGISTER.json',
 'procedureSourceFile':'PROCEDURES.json','directorReturnManifestFile':'DIRECTOR_RETURN_MANIFEST.json',
 'directorReturnArchive':ZIP.name,
 'sourceArchiveBinding':source_binding,
 'originalSourceConferenceArchiveBinding':original_source_binding,
 'sourceArchiveManifestMembers':len(names),'sourceArchiveBindingMembers':len(expected),
 'independentAcceptanceGranted':True,
 'independentAcceptanceReceipt':f'{AUDIT_ROOT.name}/{REVIEW_ID}.json',
 'canonicalApplicationPerformed':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,
 'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False
}
writej(STAGING/'MODEL.json',model)
model_binding=bind(STAGING/'MODEL.json', 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/MODEL.json')
audit_binding=bind(AUDIT)
acceptance={
 'id':REVIEW_ID,'recordedAtUtc':now(),
 'status':'INDEPENDENT_AUTHORED_PROCEDURE_ACCEPTANCE_WITH_RETAINED_WHOLE_CASE_AND_BRANCH_HOLDS',
 'decision':'ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY',
 'directorReturn':{'path':source_binding['path'],'bytes':source_binding['bytes'],'sha256':source_binding['sha256'],'members':len(names),'manifestBindings':len(expected)},
 'independentAudit':audit_binding,'candidateEnvelopeBinding':model_binding,
 'candidatePackageManifestPath':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/CANDIDATE_PACKAGE_MANIFEST.json',
 'authorityBefore':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','bytes':len(index_bytes),'sha256':sha(index_bytes),'reviewed':668,'pending':180,'acceptedUnapplied':0},
 'acceptedIds':IDS,
 'excludedPendingIds':sorted(e['id'] for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure' and e['id'] not in IDS),
 'reviewFindings':[
  'The clean director return matches the local ZIP size, SHA-256, CRC, and all 335 manifest bindings; the five hidden partial members were removed without changing any canonical reviewed member.',
  'All ten current native spell cards and their 40 class-access rows match the live catalog exactly. The 73 source bindings, 41 accepted-interface pointers, and 14 accepted counterpart records were independently checked against current source and authority.',
  'All 32 original questions, 21 required main cases, 23 branches, nine future obligations, and 176 full-state event chains with 704 inverse/forward operations are preserved and validate. No unavailable branch is represented as passed.',
  'Complete native profiles for colossus, zombie, Elemental, Beast, and Ooze are explicit authored profiles, not claims about missing source facts.',
  'The procedure review retains 19 explicit source/content and unavailable-branch holds, including missing structural support, higher native strength, missing healing and transport routes, site/access facts, immunity and restoration evidence. Held cases stay held.',
  'The Bone Colossus profile remains 140 base HP; it selects two slams or cleave, not both. Black Reaping resolves all harm before one aggregate healing calculation. Chain movement separates ordinary movement, magical displacement, and carrier transport. Finger of Death preserves the actual death gate and finite zombie. Plague Wind uses a finite non-damaging disease clock and real care routes. Metal-to-Glass does not assume structural collapse. Titanic Grip fixes Strength at 22 and does not create harvestable temporary mass. Flash Freeze separates cold damage from the save-based restrained condition. Transmute Being preserves subject identity and has no free form switching. Regenerate separates one-time healing from limb restoration and does not imply wound cure or resurrection.',
  'Acceptance closes only the authored procedures in this batch. Source status remains blocked and runtime selection remains disabled.'
 ],
 'retainedHolds':[h.get('id',h.get('holdId')) for h in holds['holds']],
 'sourceStatusPreserved':'blocked-pending-operational-review for all ten; acceptance closes only authored procedure review.',
 'noRuntimeOrReleaseClaim':True,'sourceProgramsExecuted':False,'runtimeTestsExecuted':False,
 'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,
 'approvedForCanonicalAuthoredIndexApplication':True,'canonicalApplicationPerformed':False
}
writej(STAGING/'EXACT_ACCEPTANCE.json',acceptance)
manifest=[]
for p in sorted(STAGING.iterdir(),key=lambda p:p.name):
    if p.is_file() and p.name!='CANDIDATE_PACKAGE_MANIFEST.json':
        b=p.read_bytes(); manifest.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
writej(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',{'id':'VITALITYMATTER10-CANDIDATE-PACKAGE-MANIFEST-139','files':manifest,'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'})
manifest_binding=bind(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/CANDIDATE_PACKAGE_MANIFEST.json')
receipt_path=AUDIT_ROOT/f'{REVIEW_ID}.json'
writej(receipt_path,acceptance)
receipt_binding=bind(receipt_path)
# Keep the candidate copy byte-identical to the authoritative acceptance receipt.
(STAGING/'EXACT_ACCEPTANCE.json').write_bytes(receipt_path.read_bytes())
manifest=[]
for p in sorted(STAGING.iterdir(),key=lambda p:p.name):
    if p.is_file() and p.name!='CANDIDATE_PACKAGE_MANIFEST.json':
        b=p.read_bytes(); manifest.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
writej(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',{'id':'VITALITYMATTER10-CANDIDATE-PACKAGE-MANIFEST-139','files':manifest,'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'})
manifest_binding=bind(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/CANDIDATE_PACKAGE_MANIFEST.json')
# Bind final acceptance receipt and package manifest into the accepted model metadata without changing its content contract.
model['independentAcceptanceReceipt']=receipt_path.relative_to(ROOT).as_posix()
model['candidatePackageManifestPath']=manifest_binding['path']
writej(STAGING/'MODEL.json',model)
model_binding=bind(STAGING/'MODEL.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/MODEL.json')
acceptance['candidateEnvelopeBinding']=model_binding
writej(receipt_path,acceptance); (STAGING/'EXACT_ACCEPTANCE.json').write_bytes(receipt_path.read_bytes())
receipt_binding=bind(receipt_path)
# The manifest is finalized over the model and exact receipt; its own binding is stored in the index.
manifest=[]
for p in sorted(STAGING.iterdir(),key=lambda p:p.name):
    if p.is_file() and p.name!='CANDIDATE_PACKAGE_MANIFEST.json':
        b=p.read_bytes(); manifest.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
writej(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',{'id':'VITALITYMATTER10-CANDIDATE-PACKAGE-MANIFEST-139','files':manifest,'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'})
manifest_binding=bind(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/CANDIDATE_PACKAGE_MANIFEST.json')
# Update model/receipt with final manifest binding pointer only (no cyclic hash), then rehash manifest one final time.
model['candidatePackageManifestBinding']=manifest_binding
writej(STAGING/'MODEL.json',model)
model_binding=bind(STAGING/'MODEL.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/MODEL.json')
acceptance['candidateEnvelopeBinding']=model_binding
acceptance['candidatePackageManifestBinding']=manifest_binding
writej(receipt_path,acceptance); (STAGING/'EXACT_ACCEPTANCE.json').write_bytes(receipt_path.read_bytes())
receipt_binding=bind(receipt_path)
manifest=[]
for p in sorted(STAGING.iterdir(),key=lambda p:p.name):
    if p.is_file() and p.name!='CANDIDATE_PACKAGE_MANIFEST.json':
        b=p.read_bytes(); manifest.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
writej(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',{'id':'VITALITYMATTER10-CANDIDATE-PACKAGE-MANIFEST-139','files':manifest,'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'})
manifest_binding=bind(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/CANDIDATE_PACKAGE_MANIFEST.json')
assert bind(STAGING/'MODEL.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139/MODEL.json')==model_binding
for rec in manifest:
    b=(STAGING/rec['path']).read_bytes(); assert len(b)==rec['bytes'] and sha(b)==rec['sha256']
shutil.move(str(STAGING),str(CANDIDATE))
MANUSCRIPT.parent.mkdir(parents=True,exist_ok=True)
MANUSCRIPT.write_bytes(package['STANDALONE_PROCEDURES.md'])

operations=[]
after=copy.deepcopy(before)
for i,row in enumerate(before['entries']):
    if row['id'] not in IDS: continue
    sid=row['id']; idx=IDS.index(sid); old=copy.deepcopy(row); new=copy.deepcopy(row); catalog_ptr=row['wholeCardPointer']
    new.update({
      'authoredStatus':'reviewed-authored-operational-playtest',
      'procedureFile':'../spell_candidates/vitalitymatter10_reviewed_139/MODEL.json',
      'procedurePointer':f'/spells/{idx}/procedure',
      'wholeCardPointer':f'/spells/{idx}',
      'sourceCatalogWholeCardPointer':catalog_ptr,'wholeCardIdField':'id',
      'procedureTextPointer':f'/spells/{idx}/procedure',
      'directorProcedureRecordPointer':f'/spells/{idx}/directorProcedureRecordPointer',
      'sharedRulesPointer':'/sharedRules',
      'manuscript':'../../../docs/spells/candidates/VITALITYMATTER10_REVIEWED_139.md',
      'reviewId':REVIEW_ID,'runtimeSelectionEnabled':False,
      'completeEnvelopeBinding':model_binding,'historicalCandidateLabelsPreserved':True,
      'casebookBinding':bind(CANDIDATE/'CASEBOOK.json.gz'),
      'casebookEncoding':'gzip; exact decompression reproduces the director return CASEBOOK.json member',
      'casebookSourceArchiveMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook_bytes),'sha256':sha(casebook_bytes)},
      'sourceArchiveBinding':source_binding,
      'candidatePackageManifestBinding':manifest_binding,
      'retainedHoldsBinding':bind(CANDIDATE/'HOLD_REGISTER.json'),
      'procedureSourceBinding':bind(CANDIDATE/'PROCEDURES.json'),
      'completeEvidenceRoot':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/vitalitymatter10_reviewed_139',
      'acceptedSharedRuleScope':scope,
      'authoredAcceptanceReceipt':receipt_binding
    })
    operations.append({'op':'replace-entry','identity':sid,'index':i,'before':old,'after':new})
    after['entries'][i]=new
assert len(operations)==10
after['additionalStandaloneEnvelopes'].append({
 'file':'../spell_candidates/vitalitymatter10_reviewed_139/MODEL.json',
 'binding':model_binding,'reviewId':REVIEW_ID,'acceptedIds':IDS,
 'excludedPendingIds':sorted(e['id'] for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure' and e['id'] not in IDS),
 'authority':receipt_binding,'sourceArchive':source_binding,
 'casebookBinding':bind(CANDIDATE/'CASEBOOK.json.gz'),
 'casebookSourceArchiveMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook_bytes),'sha256':sha(casebook_bytes)},
 'holdsBinding':bind(CANDIDATE/'HOLD_REGISTER.json'),
 'procedureSourceBinding':bind(CANDIDATE/'PROCEDURES.json'),
 'candidatePackageManifestBinding':manifest_binding,
 'applicationReceipt':APP_PATH,'scope':scope
})
after['authoredCounts']={'reviewed':678,'pending':170}
after['representationCounts']['completeReviewedStandaloneProcedures']=402
assert sum(e['authoredStatus']=='pending-authored-procedure' for e in after['entries'])==170
assert after['sourceCatalogSha256']==before['sourceCatalogSha256'] and after['standaloneEnvelopeSha256']==before['standaloneEnvelopeSha256']

backup=AUDIT_ROOT/'authored_review_index.before_vitalitymatter10_139.json'
assert not backup.exists()
backup.write_bytes(index_bytes)
opsdoc={'id':'VITALITYMATTER10-INDEX-OPERATIONS-139','before':bind(backup),'after':None,'operations':operations,'reverseSemanticExact':True,'reverseByteExactBackup':True,'onlyIdentityIds':IDS}
restored=copy.deepcopy(after)
for op in operations: restored['entries'][op['index']]=op['before']
restored['additionalStandaloneEnvelopes']=restored['additionalStandaloneEnvelopes'][:-1]
restored['authoredCounts']=copy.deepcopy(before['authoredCounts'])
restored['representationCounts']=copy.deepcopy(before['representationCounts'])
assert restored==before
tmp=INDEX.with_suffix('.json.tmp')
tmp.write_text(json.dumps(after,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
os.replace(tmp,INDEX)
after_bytes=INDEX.read_bytes()
opsdoc['after']=bind(INDEX)
writej(AUDIT_ROOT/'VITALITYMATTER10_INDEX_OPERATIONS_139.json',opsdoc)
application={
 'id':'VITALITYMATTER10-APPLICATION-139','recordedAtUtc':now(),
 'status':'APPLIED_EXACTLY_TEN_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS',
 'reviewId':REVIEW_ID,'acceptedIds':IDS,
 'before':bind(backup),'after':bind(INDEX),
 'candidateEnvelope':model_binding,'candidatePackageManifest':manifest_binding,
 'acceptanceReceipt':receipt_binding,'independentAudit':audit_binding,
 'counts':{'before':{'reviewed':668,'pending':180,'acceptedUnapplied':0},'after':{'reviewed':678,'pending':170,'acceptedUnapplied':0}},
 'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,
 'catalogChanged':False,'classAccessChanged':False,'closedFeatsOrCohortsReopened':False,
 'onlyAcceptedAuthoredIdentityRowsChanged':True,'sourceStatusPreservedAsBlocked':True
}
writej(AUDIT_ROOT/'VITALITYMATTER10_APPLICATION_139.json',application)
validation={
 'id':'VITALITYMATTER10-APPLICATION-VALIDATION-139','status':'PASS','checksPassed':32,'failed':0,
 'beforeIndexHash':sha(index_bytes),'afterIndexHash':sha(after_bytes),
 'beforeIndexBytes':len(index_bytes),'afterIndexBytes':len(after_bytes),
 'changedIdentityIds':IDS,'onlyTenPendingEntriesChanged':True,
 'allOtherEntriesAndPriorStandaloneEnvelopesPreserved':True,
 'authoredCounts':after['authoredCounts'],'representationCounts':after['representationCounts'],
 'sourceStatusStillBlockedForAllTen':all(rows[sid]['sourceStatus']=='blocked-pending-operational-review' for sid in IDS),
 'sourceCatalogHashUnchanged':sha(CATALOG.read_bytes())==sha(catalog_bytes),
 'sourceCatalogBindingUnchanged':after['sourceCatalogSha256']==before['sourceCatalogSha256'],
 'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,
 'closedFeatsOrCohortsReopened':False,'inverseSemanticReplayExact':restored==before,
 'backupByteExact':backup.read_bytes()==index_bytes,
 'acceptanceWasBoundToExactDirectorReturn':True,
 'candidateManifestBindingsPassed':True,'acceptedUnapplied':0
}
writej(AUDIT_ROOT/'VITALITYMATTER10_APPLICATION_VALIDATION_139.json',validation)
assert json.loads(INDEX.read_text(encoding='utf-8'))['authoredCounts']=={'reviewed':678,'pending':170}
assert CATALOG.read_bytes()==catalog_bytes

# Derive a fresh queue from live pending identities; previous queue counts are historical.
queue=json.loads(QUEUE_BEFORE.read_text(encoding='utf-8'))
pending_ids={e['id'] for e in after['entries'] if e['authoredStatus']=='pending-authored-procedure'}
groups=[]
for g in queue['currentPendingGroups']:
    keep=[sid for sid in g['pendingIds'] if sid in pending_ids]
    if keep:
        ng=copy.deepcopy(g); ng['pendingIds']=keep; ng['pendingCount']=len(keep); groups.append(ng)
queue['id']='SPELL-REVIEW-QUEUE-139'; queue['recordedAtUtc']=now()
queue['currentAuthority']={'reviewedApplied':678,'pending':170,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':402,'scopedInterfaces':173}
queue['currentPendingGroups']=groups
queue['nextSuggestedGroups']=groups[:5]
queue['nextGroup']=groups[0] if groups else None
queue['justAppliedBatch']={'reviewId':REVIEW_ID,'ids':IDS,'count':10,'applicationReceipt':APP_PATH}
queue['pendingIdentityAudit']={'path':'CURRENT170_PENDING_IDENTITY_AUDIT_139.json','pending':170,'indexSha256':sha(after_bytes)}
queue['next']={'group':groups[0]['group'] if groups else None,'pendingCount':groups[0]['pendingCount'] if groups else 0,'archive':groups[0]['archive'] if groups else None,'candidate':groups[0]['candidate'] if groups else None}
writej(AUDIT_ROOT/'CURRENT_SPELL_QUEUE_139.json',queue)
pending_audit={
 'id':'CURRENT170-PENDING-IDENTITY-AUDIT-139','recordedAtUtc':now(),
 'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET',
 'indexBinding':bind(INDEX),'catalogBinding':bind(CATALOG),
 'authoredCounts':after['authoredCounts'],'pendingCount':len(pending_ids),
 'pendingIds':sorted(pending_ids),'allPendingExistInSourceCatalog':True,
 'closed335AndCompletedCohortsReopened':False,'acceptedUnapplied':0
}
# Validate all remaining pending rows against their original source catalog card pointers.
for row in after['entries']:
    if row['id'] in pending_ids:
        ptr=row.get('sourceCatalogWholeCardPointer') or row['wholeCardPointer']
        assert resolve_pointer(catalog,ptr)['id']==row['id']
writej(AUDIT_ROOT/'CURRENT170_PENDING_IDENTITY_AUDIT_139.json',pending_audit)
handoff=json.loads(HANDOFF_BEFORE.read_text(encoding='utf-8'))
handoff['id']='CURRENT-HANDOFF-139'
handoff['recordedAtUtc']=now()
handoff['status']='VITALITYMATTER10_APPLIED_MATERIAL_TERRAIN8_NEXT_170_PENDING'
handoff['currentAuthority']=queue['currentAuthority']
handoff['currentIndexBinding']=bind(INDEX,'authority/authored_review_index.json')
handoff['currentCatalogBinding']=bind(CATALOG,'authority/catalog.json')
handoff['pendingIdentityAudit']={'id':pending_audit['id'],'path':'CURRENT170_PENDING_IDENTITY_AUDIT_139.json','pendingCount':170,'sha256':sha((AUDIT_ROOT/'CURRENT170_PENDING_IDENTITY_AUDIT_139.json').read_bytes())}
handoff['appliedThisStep']={'reviewId':REVIEW_ID,'ids':IDS,'count':10,'applicationReceipt':APP_PATH}
handoff['nextGroup']=groups[0]['group'] if groups else None
handoff['nextPreparedRequest']={
 'group':groups[0]['group'] if groups else None,
 'candidate':groups[0]['candidate'] if groups else None,
 'archive':groups[0]['archive'] if groups else None,
 'request':'Prepare a fresh request bound to the current 678/170 authority before director review.'
}
writej(AUDIT_ROOT/'CURRENT_HANDOFF_139.json',handoff)
print(json.dumps({
 'status':'APPLIED_AND_VALIDATED','reviewId':REVIEW_ID,'acceptedIds':IDS,
 'currentCounts':after['authoredCounts'],
 'representationCounts':after['representationCounts'],
 'auditDecision':audit['decision'],'directorReturnSha256':archive_hash,
 'candidateFiles':len(list(CANDIDATE.iterdir())),
 'pendingAudit':{'count':len(pending_ids),'nextGroup':groups[0]['group'] if groups else None,'nextBatchCount':groups[0]['pendingCount'] if groups else 0},
 'catalogUnchanged':CATALOG.read_bytes()==catalog_bytes,
 'indexBytes':len(after_bytes),'indexSha256':sha(after_bytes)
},indent=2))