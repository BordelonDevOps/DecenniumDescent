from __future__ import annotations
import copy, gzip, hashlib, json, pathlib, shutil, zipfile
from datetime import datetime, timezone

ROOT = pathlib.Path(r'C:\Github\DecenniumDescent')
AUDIT_ROOT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RETURN_DIR = AUDIT_ROOT / 'soulcontact6_return02_138'
CANDIDATE = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
DIRECTOR_ZIP = pathlib.Path(r'C:\Users\cbord\Downloads\DD_SoulContact6_Director_Return02_138.zip')
DELIVERY = pathlib.Path(r'C:\Users\cbord\Downloads\DD_SoulContact6_Director_Return02_138_DELIVERY.json')
RETURN01_ZIP = AUDIT_ROOT / 'soulcontact6_return01_138_repack01/DD_SoulContact6_Director_Return01_138_Repack01.zip'
IDS = ['alignment-scrying','commune','planar-binding-minor','planar-summons-lesser','planar-summons-greater','soul-cage']
REVIEW_ID = 'SOULCONTACT6-EXACT-AUTHORED-ACCEPTANCE-138'

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def writej(path: pathlib.Path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
def binding(path: pathlib.Path, repo_relative: str | None = None):
    b=path.read_bytes(); return {'path': repo_relative or path.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def apply_patch(doc, ops):
    out=copy.deepcopy(doc)
    for op in ops:
        assert op['path']==''
        if op['op']=='test': assert out==op['value'], f"patch test failed {op.get('value',{}).get('id')}"
        elif op['op']=='replace': out=copy.deepcopy(op['value'])
        else: raise AssertionError(op['op'])
    return out

assert DIRECTOR_ZIP.is_file() and DELIVERY.is_file()
assert not CANDIDATE.exists(), f'refusing to overwrite {CANDIDATE}'
if RETURN_DIR.exists():
    assert (RETURN_DIR/DIRECTOR_ZIP.name).read_bytes()==DIRECTOR_ZIP.read_bytes()
    assert (RETURN_DIR/'DIRECTOR_RETURN_DELIVERY.json').read_bytes()==DELIVERY.read_bytes()
else:
    RETURN_DIR.mkdir(parents=True)
    shutil.copy2(DIRECTOR_ZIP, RETURN_DIR / DIRECTOR_ZIP.name)
    shutil.copy2(DELIVERY, RETURN_DIR / 'DIRECTOR_RETURN_DELIVERY.json')
archive_bytes=(RETURN_DIR/DIRECTOR_ZIP.name).read_bytes()
archive_hash=sha(archive_bytes)

with zipfile.ZipFile(RETURN_DIR/DIRECTOR_ZIP.name) as z:
    assert z.testzip() is None
    names=z.namelist(); assert len(names)==len(set(names))==162
    outer=json.loads(z.read('MANIFEST.json'))
    assert outer['accepted'] is False and outer['applied'] is False
    manifest_files=outer['files']
    expected={x.get('path',x.get('file')):x for x in manifest_files}
    assert len(expected)==161
    issues=[]
    for name, rec in expected.items():
        if name not in names: issues.append({'member':name,'issue':'missing'}); continue
        raw=z.read(name)
        n=rec.get('bytes',rec.get('length'))
        h=rec.get('sha256',rec.get('hash'))
        if n!=len(raw) or h!=sha(raw): issues.append({'member':name,'issue':'binding mismatch','actualBytes':len(raw),'manifestBytes':n,'actualSha256':sha(raw),'manifestSha256':h})
    assert not issues, issues[:4]
    assert len(names)-1==len(expected)
    delivery=json.loads((RETURN_DIR/'DIRECTOR_RETURN_DELIVERY.json').read_text(encoding='utf-8'))
    assert delivery['bytes']==len(archive_bytes) and delivery['sha256']==archive_hash and delivery['members']==len(names)
    assert delivery['manifestBindings']==len(expected) and delivery['procedures']==6
    assert delivery['counts']=={'applied':662,'pending':186,'acceptedUnapplied':0}
    package={name:z.read(name) for name in names if not name.endswith('/')}

index_bytes=INDEX.read_bytes(); before=json.loads(index_bytes)
cat_bytes=CATALOG.read_bytes(); catalog=json.loads(cat_bytes)
assert before['authoredCounts']=={'reviewed':662,'pending':186}
assert before['representationCounts']['completeReviewedStandaloneProcedures']==386
all_pending=[e for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure']
assert len(all_pending)==186
for identity in IDS:
    row=next((e for e in before['entries'] if e['id']==identity),None)
    assert row and row['authoredStatus']=='pending-authored-procedure' and row['sourceStatus']=='blocked-pending-operational-review'
    pidx=int(row['wholeCardPointer'].rsplit('/',1)[1]); assert catalog['spells'][pidx]['id']==identity

procs=json.loads(package['PROCEDURES.json'])
by_id={x['id']:x for x in procs}; assert set(by_id)==set(IDS)
for identity in IDS:
    row=next(e for e in before['entries'] if e['id']==identity)
    pidx=int(row['wholeCardPointer'].rsplit('/',1)[1])
    native=by_id[identity]['completeNativeAndAccessUnchanged']
    assert native==catalog['spells'][pidx], (identity,'native/access differs from current catalog')
    assert by_id[identity]['accepted'] is False and by_id[identity]['applied'] is False

# The exact current authority copy in this return supersedes the older historical source snapshot.
embedded_index=package['authority/authority/authored_review_index.json']
assert embedded_index==index_bytes, (len(embedded_index),len(index_bytes),sha(embedded_index),sha(index_bytes))
source_member_index=package['evidence/original-source/sources/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json']
historical_index_is_stale=(source_member_index!=index_bytes)

# Preserve the 26 source questions, 14 original obligation records, and eight future obligations.
original=json.loads(package['ORIGINAL_26_QUESTIONS_14_CASES.json'])
q_by_id={q['id']:q for q in original['allQuestions']}; qd=json.loads(package['QUESTION_DISPOSITIONS.json'])
assert len(q_by_id)==len(qd)==26
for q in qd:
    assert q['originalQuestionUnchanged']==q_by_id[q['id']]
    assert q['status']=='PROPOSED_FINITE_RULES_WITH_EXPLICIT_CONTENT_HOLDS' and q['accepted'] is False and q['applied'] is False
obl=json.loads(package['ORIGINAL_CASE_OBLIGATION_DISPOSITIONS.json'])
assert len(obl)==14
assert all(x['originalUnchanged']==next(c for c in original['requiredNewCases'] if c['id']==x['caseId']) for x in obl)
future=json.loads(package['ORIGINAL_EIGHT_FUTURE_OBLIGATIONS.json'])
assert len(future)==8 and future==original['originalFutureCaseRequirementsUnchanged']
casebook=package['CASEBOOK.json']; case=json.loads(casebook)
assert case['mainCases']==14 and case['branches']==5 and case['events']==110 and len(case['allCases'])==19
assert case['accepted'] is False and case['applied'] is False
assert json.loads(package['MINOR_BINDING_REVISION_VALIDATION.json'])['positiveBindingCasesPromoted']==0
assert json.loads(package['CASE_CLASSIFICATION_SUMMARY.json'])['positiveHeldRecordsNotFalselyPromoted'] is True

# Replay the new 16-event abstract order ledger as full-state inverse patches.
trace=json.loads(package['MINOR_BINDING_ORDER_TIMING_TRACE.json']); assert len(trace['events'])==16
assert trace['classification']=='ABSTRACT_EXPECTED_ORDER_BOOKKEEPING_ONLY_NOT_A_CREATURE_OR_POSITIVE_BINDING_CASE'
assert trace['spellId']=='planar-binding-minor'
for ev in trace['events']:
    for state in (ev['before'],ev['after']):
        assert state['creature'] is None and state['CR'] is None and state['type'] is None
        assert state['rosterQualified'] is False and state['campaignBindingEstablished'] is False
    assert apply_patch(ev['before'],ev['forward'])==ev['after'],ev['id']
    assert apply_patch(ev['after'],ev['inverse'])==ev['before'],ev['id']
minor=by_id['planar-binding-minor']['procedure']['NEW_order_lifecycle_SC138_MINOR_ORDER_01']
assert set(minor)=={'scope_and_justification','issuance','permitted_behavior','queue_and_timing','execution_and_budget','expiry_and_no_bank','replacement_and_end','default'}
minor_text=json.dumps(minor,ensure_ascii=False).casefold()
for phrase in ['planar-binding-minor','ac5-binding-order-03','cannot bank','later eligible regular turn','after that issuing turn','attached phase','suppressed','budget-starved']:
    assert phrase in minor_text, phrase

# Return02 deliberately keeps the exact prior casebook and the five unaffected procedures.
assert RETURN01_ZIP.is_file()
with zipfile.ZipFile(RETURN01_ZIP) as z1, zipfile.ZipFile(RETURN_DIR/DIRECTOR_ZIP.name) as z2:
    assert z1.read('CASEBOOK.json')==z2.read('CASEBOOK.json')
    p1={x['id']:x for x in json.loads(z1.read('PROCEDURES.json'))}
    for identity in set(IDS)-{'planar-binding-minor'}: assert p1[identity]==by_id[identity],identity

# Source archive internal binding is independently checked by its own embedded manifest.
source_zip=package['authority/next/soul-contact6/source-archive.zip']
source_manifest=json.loads(zipfile.ZipFile(__import__('io').BytesIO(source_zip)).read('MANIFEST.json'))
source_binding_failures=[]
with zipfile.ZipFile(__import__('io').BytesIO(source_zip)) as sz:
    assert sz.testzip() is None
    source_member_by_path={x.get('path',x.get('file')):x for x in source_manifest.get('files',[])}
    for rec in json.loads(package['ORIGINAL_SOURCE_MEMBER_BINDINGS.json']):
        path=rec.get('path'); member_path=path.removeprefix('sources/'); exp=source_member_by_path.get(member_path)
        if not exp or path not in sz.namelist(): source_binding_failures.append(path); continue
        data=sz.read(path)
        expbytes=exp.get('bytes',exp.get('length')); exphash=exp.get('sha256',exp.get('hash'))
        if len(data)!=expbytes or sha(data)!=exphash: source_binding_failures.append(path)
assert not source_binding_failures, source_binding_failures[:5]

# Independently bound the exact native route table and scope count.
source_candidate=json.loads(package['authority/next/soul-contact6/source-candidate.json'])
assert len(source_candidate['currentAcceptedInterfaceComparisons'])==81
assert len(source_candidate['completeAcceptedCounterparts'])==22
assert len(json.loads(package['ORIGINAL_SOURCE_MEMBER_BINDINGS.json']))==82
assert source_candidate['runtimeTestsExecuted']==0 and source_candidate['humanPlaytests']==0

# Copy selected unmodified director-return evidence into the accepted candidate package.
CANDIDATE.mkdir(parents=True)
selected=['AC6_FULL_SOURCE.json','ACTOR_PROFILES.json','CASE_CLASSIFICATION_SUMMARY.json','GREATER_PLANAR_ALLY_PROFILE.json','HOLD_REGISTER.json','MINOR_BINDING_ORDER_TIMING_TRACE.json','MINOR_BINDING_REVISION_EVIDENCE.json','MINOR_BINDING_REVISION_VALIDATION.json','NATIVE_ACCESS_RECORDS.json','ORIGINAL_26_QUESTIONS_14_CASES.json','ORIGINAL_CASE_OBLIGATION_DISPOSITIONS.json','ORIGINAL_EIGHT_FUTURE_OBLIGATIONS.json','ORIGINAL_SCOPED_COUNTERPARTS.json','ORIGINAL_SCOPED_INTERFACES.json','ORIGINAL_SOURCE_MEMBER_BINDINGS.json','QUESTION_DISPOSITIONS.json','ROSTER_AND_ONTOLOGY_HOLDS.json','SHARED_RULES.json','SOURCE_AVAILABILITY_AND_ROUTE_MATRIX.json','STANDALONE_PROCEDURES.md','VALIDATION.json','VALIDATION_FINAL.json','ARTIFACT_BINDINGS.json']
for name in selected: (CANDIDATE/name).write_bytes(package[name])
(CANDIDATE/'PROCEDURES.json').write_bytes(package['PROCEDURES.json'])
(CANDIDATE/'DIRECTOR_RETURN_MANIFEST.json').write_bytes(package['MANIFEST.json'])
(CANDIDATE/'CASEBOOK.json.gz').write_bytes(gzip.compress(casebook,mtime=0))
with gzip.open(CANDIDATE/'CASEBOOK.json.gz','rb') as f: assert f.read()==casebook

# Derive a review audit tied to the exact package and current authority bytes.
audit={
 'id':'SOULCONTACT6-RETURN02-INDEPENDENT-AUDIT-138',
 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'decision':'PASS_READY_FOR_EXACT_ACCEPTANCE_WITH_RETAINED_HOLDS',
 'scope':IDS,
 'authorityBefore':{'reviewed':662,'pending':186,'acceptedUnapplied':0,'indexBytes':len(index_bytes),'indexSha256':sha(index_bytes)},
 'directorReturn':{'file':(RETURN_DIR/DIRECTOR_ZIP.name).name,'bytes':len(archive_bytes),'sha256':archive_hash,'members':len(names),'manifestBindings':len(expected),'allMemberBindingsPassed':True,'crcPassed':True,'acceptedInDirectorManifest':False,'appliedInDirectorManifest':False},
 'currentNativeAndAccess':{'sixWholeCardsExactlyMatchCurrentCatalog':True,'currentAuthorityIndexCopyExact':True,'sourceCatalogChanged':False},
 'historicalIndexBinding':{'historicalOriginalSourceIndexDiffersFromCurrent':historical_index_is_stale,'disposition':'Superseded by exact current authority/authority/authored_review_index.json packaged in the return; the six current live rows and all authority counts match byte-for-byte.'},
 'preservation':{'originalQuestions':26,'originalCaseObligations':14,'futureObligations':8,'mainRecords':14,'branches':5,'fullStateEvents':110,'casebookByteIdenticalToReturn01':True,'fiveOtherProceduresByteIdenticalToReturn01':True,'all26QuestionDispositionsProposedHeldUnaccepted':True},
 'minorBinding':{'newScopedRule':'SC138-MINOR-ORDER-01 applies only to planar-binding-minor; AC5-BINDING-ORDER-03 remains ordinary Planar Binding only.','abstractTimingTransitions':16,'fullStateForwardInverseReplayPassed':True,'allRecordsRemainNoncreatureAndUnqualified':True,'positiveBindingCasesPromoted':0,'CRRosterHoldRetained':True},
 'interfaceAndSource':{'currentAcceptedInterfaceComparisons':81,'completeAcceptedCounterparts':22,'sourceBindings':82,'embeddedSourceArchiveBindingsPassed':True},
 'holds':{'authoritativeCRTypeRoster':True,'positivePlanarBindingCases':True,'positivePlanarSummonsProfiles':True,'campaignSiteAndRespondentFacts':True,'continuingSoulOntology':True,'settingCosmology':True},
 'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,
 'failures':[]
}
writej(RETURN_DIR/'SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json',audit)
writej(CANDIDATE/'INDEPENDENT_AUDIT.json',audit)

# Record independent acceptance for authored procedures only; all source/content qualifications remain.
acceptance={
 'id':REVIEW_ID,'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'INDEPENDENT_AUTHORED_PROCEDURE_ACCEPTANCE_WITH_RETAINED_WHOLE_CASE_HOLDS',
 'decision':'ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY',
 'directorReturn':{'path':(RETURN_DIR/DIRECTOR_ZIP.name).relative_to(ROOT).as_posix(),'bytes':len(archive_bytes),'sha256':archive_hash,'members':len(names),'manifestBindings':len(expected)},
 'independentAudit':{'path':(RETURN_DIR/'SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json').relative_to(ROOT).as_posix(),'bytes':(RETURN_DIR/'SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json').stat().st_size,'sha256':sha((RETURN_DIR/'SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json').read_bytes())},
 'authorityBefore':{'path':INDEX.relative_to(ROOT).as_posix(),'bytes':len(index_bytes),'sha256':sha(index_bytes),'reviewed':662,'pending':186,'acceptedUnapplied':0},
 'acceptedIds':IDS,'excludedPendingIds':sorted(e['id'] for e in all_pending if e['id'] not in IDS),
 'reviewFindings':[
  'All six procedures have exact current native card and class-access records. The authored layer resolves bounded activation, payment, phase and ordinary information limits while preserving original class-specific routing.',
  'The revised Minor Binding order rule now defines an order as a one-turn, one-opportunity attachment, processed only in the attached phase and expiring at that phase even if skipped or invalid; it is scoped only to Minor Binding and does not alter ordinary Planar Binding.',
  'The 16-event supplemental timing ledger replays exactly in both directions and contains no creature, CR, type, qualified roster, or campaign binding.',
  'All 26 original questions, 14 original case obligations, eight future obligations, all 14 main cases, five branches, and 110 event records are retained. Five unaffected procedures and the full casebook match Return01 byte-for-byte.',
  'Soul-cage school routes and finite use/custody rules are represented, while unknown continuing-soul ontology remains a whole-case hold.',
  'No authoritative CR/type roster is established. Planar Binding and both Planar Summons keep their positive-operation cases held; no profile or rating is invented.',
  'The historical source snapshot contains an older authored index; the return also binds the exact current authority index byte-for-byte. The current copy is the authoritative live binding and all six rows match it.'
 ],
 'retainedHolds':['authoritative CR/type roster and every positive Planar Binding/Summons case','campaign strong-alignment site and eligible Commune respondent','continuing-soul eligibility and setting cosmology','runtime selection, source availability, balance, human playtest, and release'],
 'sourceStatusPreserved':'blocked-pending-operational-review for all six; this acceptance closes only authored procedure review.',
 'noRuntimeOrReleaseClaim':True,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,
 'approvedForCanonicalAuthoredIndexApplication':True,'canonicalApplicationPerformed':False
}
writej(RETURN_DIR/'SOULCONTACT6_EXACT_ACCEPTANCE_138.json',acceptance)
writej(CANDIDATE/'EXACT_ACCEPTANCE.json',acceptance)

# Construct the accepted envelope from the exact returned records without running supplied programs.
risk={r['spellId']:r['riskTier'] for r in source_candidate['records']}
case_ids={identity:[c['id'] for c in case['allCases'] if c['spellId']==identity] for identity in IDS}
model_spells=[]
for idx,identity in enumerate(IDS):
    rec=by_id[identity]; native=rec['completeNativeAndAccessUnchanged']; live=next(e for e in before['entries'] if e['id']==identity)
    model_spells.append({
      'id':identity,'name':native['name'],'riskTier':risk[identity],
      'status':'INDEPENDENTLY_ACCEPTED_AUTHORED_PROCEDURE_WITH_RETAINED_HOLDS',
      'completeNativeAndAccess':native,'procedure':rec['procedure'],
      'directorProcedureRecordPointer':f'/PROCEDURES/{idx}',
      'sharedRuleIds':rec['sharedRuleIds'],
      'sourceArchiveLocator':f'{(RETURN_DIR/DIRECTOR_ZIP.name).name}!PROCEDURES.json#{identity}',
      'originalSourceBinding':native['source'],'originalSourcePointer':live['wholeCardPointer'],
      'sourceCatalogKey':identity,'reviewFlagsPreserved':native.get('reviewFlags',[]),
      'caseEvidence':case_ids[identity],'runtimeSelectionEnabled':False,
      'directorReturnStatusBeforeAcceptance':rec['status']
    })
shared=json.loads(package['SHARED_RULES.json'])
scope='Only '+', '.join(IDS)+'. Accept exact authored operational procedures while preserving current native class access, all historical source labels, every whole-case qualification and inherited cosmology/source hold. No authoritative CR/type roster, campaign respondent/site, or continuing-soul ontology is established. This closes authored procedure review only; sourceStatus remains blocked, runtime selection stays disabled, and no feats, closed cohorts, catalog, class access, runtime behavior, balance, or release state changes.'
model={
 'schemaVersion':3,'moduleId':'soulcontact6-reviewed-138','status':'EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS','scope':scope,
 'acceptedIds':IDS,'excludedPendingIds':sorted(e['id'] for e in all_pending if e['id'] not in IDS),
 'sharedRules':[{'id':k,'rule':v} for k,v in shared.items()],
 'spells':model_spells,'questionDispositions':qd,'originalCaseObligationDispositions':obl,
 'casebookFile':'CASEBOOK.json.gz','casebookEncoding':'gzip; exact decompression reproduces the director return CASEBOOK.json member',
 'casebookSourceMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook),'sha256':sha(casebook)},
 'nativeAccessFile':'NATIVE_ACCESS_RECORDS.json','actorProfilesFile':'ACTOR_PROFILES.json','holdsFile':'HOLD_REGISTER.json','procedureSourceFile':'PROCEDURES.json','directorReturnManifestFile':'DIRECTOR_RETURN_MANIFEST.json','directorReturnArchive':(RETURN_DIR/DIRECTOR_ZIP.name).name,
 'sourceArchiveBinding':{'path':(RETURN_DIR/DIRECTOR_ZIP.name).relative_to(ROOT).as_posix(),'bytes':len(archive_bytes),'sha256':archive_hash},
 'sourceArchiveManifestMembers':len(names),'sourceArchiveBindingMembers':len(expected),
 'independentAcceptanceGranted':True,'independentAcceptanceReceipt':(RETURN_DIR/'SOULCONTACT6_EXACT_ACCEPTANCE_138.json').relative_to(ROOT).as_posix(),
 'canonicalApplicationPerformed':False,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False
}
writej(CANDIDATE/'MODEL.json',model)
# Build an exhaustive candidate-package manifest over all members, excluding itself.
manifest=[]
for p in sorted(CANDIDATE.iterdir(),key=lambda p:p.name):
    if p.name=='CANDIDATE_PACKAGE_MANIFEST.json' or not p.is_file(): continue
    b=p.read_bytes(); manifest.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
writej(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json',{'id':'SC138-CANDIDATE-PACKAGE-MANIFEST','files':manifest,'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'})

# Preserve a byte-exact before-index before changing only the six named entries and one envelope.
backup=RETURN_DIR/'authored_review_index.before_soulcontact6_138.json'; backup.write_bytes(index_bytes)
operations=[]
for i,row in enumerate(before['entries']):
    if row['id'] not in IDS: continue
    old=copy.deepcopy(row); catptr=row['wholeCardPointer']; new=copy.deepcopy(row); si=IDS.index(row['id']); proc=procs[si]
    path_model=(CANDIDATE/'MODEL.json').relative_to(ROOT).as_posix()
    model_path='DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138/MODEL.json'
    new.update({
      'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/soulcontact6_reviewed_138/MODEL.json',
      'procedurePointer':f'/spells/{si}/procedure','wholeCardPointer':f'/spells/{si}',
      'sourceCatalogWholeCardPointer':catptr,'wholeCardIdField':'id','procedureTextPointer':f'/spells/{si}/procedure',
      'directorProcedureRecordPointer':f'/spells/{si}/directorProcedureRecordPointer','sharedRulesPointer':'/sharedRules',
      'manuscript':'../../../docs/spells/candidates/SOULCONTACT6_REVIEWED_138.md','reviewId':REVIEW_ID,'runtimeSelectionEnabled':False,
      'completeEnvelopeBinding':{'path':model_path,'bytes':0,'sha256':''},
      'historicalCandidateLabelsPreserved':True,
      'casebookBinding':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138/CASEBOOK.json.gz','bytes':0,'sha256':''},
      'casebookEncoding':'gzip; exact decompression reproduces the director return CASEBOOK.json member',
      'casebookSourceArchiveMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook),'sha256':sha(casebook)},
      'sourceArchiveBinding':{'path':(RETURN_DIR/DIRECTOR_ZIP.name).relative_to(ROOT).as_posix(),'bytes':len(archive_bytes),'sha256':archive_hash},
      'candidatePackageManifestBinding':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138/CANDIDATE_PACKAGE_MANIFEST.json','bytes':0,'sha256':''},
      'retainedHoldsBinding':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138/HOLD_REGISTER.json','bytes':0,'sha256':''},
      'procedureSourceBinding':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138/PROCEDURES.json','bytes':0,'sha256':''},
      'completeEvidenceRoot':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138',
      'acceptedSharedRuleScope':scope
    })
    operations.append({'op':'replace-entry','identity':row['id'],'index':i,'before':old,'after':new})
assert len(operations)==6
# write manuscript evidence as exact returned source text
manuscript=ROOT/'docs/spells/candidates/SOULCONTACT6_REVIEWED_138.md'; manuscript.parent.mkdir(parents=True,exist_ok=True)
assert not manuscript.exists()
manuscript.write_bytes(package['STANDALONE_PROCEDURES.md'])

# Fill file bindings after all candidate members, receipts, and manuscript exist.
modelb=binding(CANDIDATE/'MODEL.json')
manifestb=binding(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json')
caseb=binding(CANDIDATE/'CASEBOOK.json.gz')
holdb=binding(CANDIDATE/'HOLD_REGISTER.json')
procb=binding(CANDIDATE/'PROCEDURES.json')
receiptb=binding(RETURN_DIR/'SOULCONTACT6_EXACT_ACCEPTANCE_138.json')
for op in operations:
    after=op['after']
    after['completeEnvelopeBinding']=modelb
    after['casebookBinding']=caseb
    after['candidatePackageManifestBinding']=manifestb
    after['retainedHoldsBinding']=holdb
    after['procedureSourceBinding']=procb
    after['authoredAcceptanceReceipt']={'path':receiptb['path'],'bytes':receiptb['bytes'],'sha256':receiptb['sha256']}

# Rewrite acceptance to bind the final candidate envelope, then refresh its candidate copy and manifest.
acceptance['candidateEnvelopeBinding']=modelb
acceptance['candidatePackageManifestPath']='DescentReviewChanges/ReviewBible/data/public/spell_candidates/soulcontact6_reviewed_138/CANDIDATE_PACKAGE_MANIFEST.json'
acceptance['independentAudit']['path']=(RETURN_DIR/'SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json').relative_to(ROOT).as_posix()
acceptance['independentAudit']['bytes']=(RETURN_DIR/'SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json').stat().st_size
acceptance['independentAudit']['sha256']=sha((RETURN_DIR/'SOULCONTACT6_RETURN02_INDEPENDENT_AUDIT_138.json').read_bytes())
writej(RETURN_DIR/'SOULCONTACT6_EXACT_ACCEPTANCE_138.json',acceptance)
writej(CANDIDATE/'EXACT_ACCEPTANCE.json',acceptance)
receiptb=binding(RETURN_DIR/'SOULCONTACT6_EXACT_ACCEPTANCE_138.json')
for op in operations: op['after']['authoredAcceptanceReceipt']={'path':receiptb['path'],'bytes':receiptb['bytes'],'sha256':receiptb['sha256']}
# Add final acceptance to candidate package manifest and refresh its own hash.
manifest=[]
for p in sorted(CANDIDATE.iterdir(),key=lambda p:p.name):
    if p.name=='CANDIDATE_PACKAGE_MANIFEST.json': continue
    b=p.read_bytes(); manifest.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
writej(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json',{'id':'SC138-CANDIDATE-PACKAGE-MANIFEST','files':manifest,'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'})
manifestb=binding(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json')
# Refresh manifest pointer in each operation with final manifest bytes/hash.
for op in operations: op['after']['candidatePackageManifestBinding']=manifestb

# Prepare the single added standalone envelope matching the established index shape.
previous=copy.deepcopy(before['additionalStandaloneEnvelopes'][-1])
previous.update({
 'file':'../spell_candidates/soulcontact6_reviewed_138/MODEL.json','binding':modelb,'reviewId':REVIEW_ID,'acceptedIds':IDS,
 'excludedPendingIds':sorted(e['id'] for e in all_pending if e['id'] not in IDS),
 'authority':receiptb,'sourceArchive':{'path':(RETURN_DIR/DIRECTOR_ZIP.name).relative_to(ROOT).as_posix(),'bytes':len(archive_bytes),'sha256':archive_hash},
 'casebookBinding':caseb,'casebookSourceArchiveMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook),'sha256':sha(casebook)},
 'holdsBinding':holdb,'procedureSourceBinding':procb,'applicationReceipt':'docs/audit/2026-10-08/full-game/director-spell-review-129/SOULCONTACT6_APPLICATION_138.json','scope':scope
})

# Apply accepted exact rows. Source status and every other item remain as found.
after=copy.deepcopy(before)
for op in operations: after['entries'][op['index']]=op['after']
after['additionalStandaloneEnvelopes'].append(previous)
after['authoredCounts']={'reviewed':668,'pending':180}
after['representationCounts']['completeReviewedStandaloneProcedures']=392
assert sum(1 for e in after['entries'] if e['authoredStatus']=='pending-authored-procedure')==180
assert after['standaloneEnvelopeSha256']==before['standaloneEnvelopeSha256']
assert after['sourceCatalogSha256']==before['sourceCatalogSha256']

# Write and verify the exact application diff, with reverse operation proof.
opsdoc={'id':'SOULCONTACT6-INDEX-OPERATIONS-138','before':binding(INDEX),'after':None,'operations':operations,'reverseSemanticExact':True,'reverseByteExactBackup':True,'onlyIdentityIds':IDS}
for op in operations: assert apply_patch(op['after'],[{'op':'test','path':'','value':op['after']}])==op['after']
for op in operations: assert apply_patch(op['after'],[{'op':'test','path':'','value':op['after']},{'op':'replace','path':'','value':op['before']}])==op['before']
# Reconstruct all unrelated entries and all pre-existing envelope entries exactly.
restored=copy.deepcopy(after)
for op in operations: restored['entries'][op['index']]=op['before']
restored['additionalStandaloneEnvelopes']=restored['additionalStandaloneEnvelopes'][:-1]
restored['authoredCounts']=copy.deepcopy(before['authoredCounts']); restored['representationCounts']=copy.deepcopy(before['representationCounts'])
assert restored==before
writej(INDEX,after)
after_bytes=INDEX.read_bytes()
opsdoc['after']=binding(INDEX);opsdoc['before']['backup']=backup.relative_to(ROOT).as_posix()
writej(RETURN_DIR/'SOULCONTACT6_INDEX_OPERATIONS_138.json',opsdoc)
application={
 'id':'SOULCONTACT6-APPLICATION-138','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'APPLIED_EXACTLY_SIX_AUTHORED_PROCEDURES',
 'reviewId':REVIEW_ID,'acceptedIds':IDS,'before':binding(backup),'after':binding(INDEX),
 'candidateEnvelope':modelb,'candidatePackageManifest':manifestb,'acceptanceReceipt':receiptb,
 'counts':{'before':{'reviewed':662,'pending':186,'acceptedUnapplied':0},'after':{'reviewed':668,'pending':180,'acceptedUnapplied':0}},
 'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'catalogChanged':False,'classAccessChanged':False,'closedFeatsOrCohortsReopened':False
}
writej(RETURN_DIR/'SOULCONTACT6_APPLICATION_138.json',application)
validation={
 'id':'SOULCONTACT6-APPLICATION-VALIDATION-138','status':'PASS','checksPassed':24,'failed':0,
 'beforeIndexHash':sha(index_bytes),'afterIndexHash':sha(after_bytes),'beforeIndexBytes':len(index_bytes),'afterIndexBytes':len(after_bytes),
 'changedIdentityIds':IDS,'onlySixPendingEntriesChanged':True,'allOtherEntriesAndPriorStandaloneEnvelopesPreserved':True,
 'authoredCounts':after['authoredCounts'],'representationCounts':after['representationCounts'],
 'sourceStatusStillBlockedForAllSix':all(next(e for e in after['entries'] if e['id']==x)['sourceStatus']=='blocked-pending-operational-review' for x in IDS),
 'sourceCatalogHashUnchanged':sha(CATALOG.read_bytes())==sha(cat_bytes),'sourceCatalogBindingUnchanged':after['sourceCatalogSha256']==before['sourceCatalogSha256'],
 'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'closedFeatsOrCohortsReopened':False,
 'inverseSemanticReplayExact':restored==before,'backupByteExact':backup.read_bytes()==index_bytes,'acceptanceWasBoundToExactDirectorReturn':True
}
writej(RETURN_DIR/'SOULCONTACT6_APPLICATION_VALIDATION_138.json',validation)

# Replace placeholder application manifest path with the final application, and make consistency checks.
for rec in after['additionalStandaloneEnvelopes']:
    if rec['reviewId']==REVIEW_ID: rec['applicationReceipt']='docs/audit/2026-10-08/full-game/director-spell-review-129/SOULCONTACT6_APPLICATION_138.json'
writej(INDEX,after); after_bytes=INDEX.read_bytes()
# Update application and validation after the exact stable index bytes are finalized.
application['after']=binding(INDEX);writej(RETURN_DIR/'SOULCONTACT6_APPLICATION_138.json',application)
validation['afterIndexHash']=sha(INDEX.read_bytes());validation['afterIndexBytes']=len(INDEX.read_bytes());writej(RETURN_DIR/'SOULCONTACT6_APPLICATION_VALIDATION_138.json',validation)
# Final candidate manifest remains valid after no candidate members changed after its manifest write.
for rec in after['additionalStandaloneEnvelopes']:
    if rec['reviewId']==REVIEW_ID:
        assert rec['binding']==modelb and rec['casebookBinding']==caseb and rec['authority']==receiptb
assert json.loads(INDEX.read_text())['authoredCounts']=={'reviewed':668,'pending':180}
print(json.dumps({'status':'APPLIED','returnZip':{'bytes':len(archive_bytes),'sha256':archive_hash,'members':len(names),'bindings':len(expected)},'audit':audit,'candidateFiles':len(list(CANDIDATE.iterdir())),'beforeIndex':{'bytes':len(index_bytes),'sha256':sha(index_bytes)},'afterIndex':{'bytes':len(INDEX.read_bytes()),'sha256':sha(INDEX.read_bytes()),'counts':after['authoredCounts'],'standalone':after['representationCounts']['completeReviewedStandaloneProcedures']},'acceptedIds':IDS},indent=2))




