from __future__ import annotations
import hashlib, io, json, pathlib, shutil, zipfile
from datetime import datetime, timezone

ROOT = pathlib.Path(r'C:\Github\DecenniumDescent')
AUDIT_ROOT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RETURN_DIR = AUDIT_ROOT / 'vitalitymatter10_return01_139_clean01'
ZIP = pathlib.Path(r'C:\Users\cbord\Downloads\DD_VitalityMatter10_Director_Return01_139_Clean01.zip')
DELIVERY = pathlib.Path(r'C:\Users\cbord\Downloads\DD_VitalityMatter10_Director_Return01_139_Clean01_DELIVERY.json')
PRIOR_ZIP = pathlib.Path(r'C:\Users\cbord\Downloads\DD_VitalityMatter10_Director_Return01_139.zip')
SOURCE_ZIP = AUDIT_ROOT.parent / 'DD_VitalityMatter10_Director_Conference_128.zip'
CONTEXT_ZIP = AUDIT_ROOT / 'DD_SoulContact6_Applied_VitalityMatter10_Context_138.zip'
REQUEST = AUDIT_ROOT / 'VITALITYMATTER10_NEXT_REQUEST_138.txt'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
EXPECTATIONS = AUDIT_ROOT / 'VITALITYMATTER10_RETURN_EXPECTATIONS_138.json'
COUNTERPARTS = AUDIT_ROOT / 'VITALITYMATTER10_REQUIRED_COUNTERPART_BINDINGS_138.json'

IDS = ['summon-bone-colossus','black-reaping','chain-of-the-grave','finger-of-death','plague-wind','metal-to-glass','titanic-grip','flash-freeze','transmute-being','regenerate']

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def j(data: bytes): return json.loads(data.decode('utf-8'))
def verify_nested_zip(data: bytes, expected_members: int | None = None):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == len(set(names))
        if expected_members is not None: assert len(names) == expected_members
        manifest_name = 'MANIFEST.json' if 'MANIFEST.json' in names else 'CONTEXT_MANIFEST.json'
        manifest = j(z.read(manifest_name))
        recs = {x.get('path', x.get('file')): x for x in manifest.get('files', [])}
        assert len(recs) == len(names) - 1
        assert set(names) - {manifest_name} == set(recs)
        for name, rec in recs.items():
            b = z.read(name)
            assert len(b) == rec.get('bytes', rec.get('length')), name
            assert sha(b) == rec.get('sha256', rec.get('hash')), name
        return names

assert ZIP.is_file() and DELIVERY.is_file() and PRIOR_ZIP.is_file()
delivery = json.loads(DELIVERY.read_text(encoding='utf-8'))
zip_bytes = ZIP.read_bytes(); zip_hash = sha(zip_bytes)
assert len(zip_bytes) == delivery['bytes'] and zip_hash == delivery['sha256']
assert delivery['counts'] == {'applied':668,'pending':180,'acceptedUnapplied':0}
assert delivery['accepted'] is False and delivery['applied'] is False
assert delivery['procedures'] == 10 and delivery['nativeClassAccessRows'] == 40
assert delivery['questionDispositions'] == 32 and delivery['originalMainCases'] == 21
assert delivery['additionalBranches'] == 23 and delivery['fullDataEvents'] == 176
assert delivery['fullForwardInverseEventOperations'] == 704 and delivery['originalFutureObligations'] == 9
assert delivery['packageCRCAndAllMemberHashesPassed'] is True
assert delivery['allRequiredSourceHoldsRetained'] is True
assert delivery['notAllUnavailableBranchesClaimedPassed'] is True

with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
    names = z.namelist(); assert len(names) == delivery['members'] == 336
    outer = j(z.read('MANIFEST.json'))
    assert outer['accepted'] is False and outer['applied'] is False
    recs = {x.get('path', x.get('file')): x for x in outer['files']}
    assert len(recs) == delivery['manifestBindings'] == 335
    assert set(names) - {'MANIFEST.json'} == set(recs)
    hidden = [n for n in names if pathlib.PurePosixPath(n).name.startswith('.') or '.tmp' in pathlib.PurePosixPath(n).name.casefold()]
    assert not hidden, hidden
    for name, rec in recs.items():
        b = z.read(name)
        assert len(b) == rec.get('bytes',rec.get('length')), name
        assert sha(b) == rec.get('sha256',rec.get('hash')), name
    package = {n:z.read(n) for n in names}

with zipfile.ZipFile(PRIOR_ZIP) as old:
    old_names = set(old.namelist())
    new_names = set(names)
    removed = old_names - new_names
    assert len(removed) == 5 and not new_names - old_names
    changed = [n for n in new_names - {'MANIFEST.json','ARTIFACT_BINDINGS.json'} if package[n] != old.read(n)]
    assert not changed, changed
    for name in ['.CASEBOOK.json.YfwJxe','cases/.VM128-FINGER-OF-DEATH-B__death-ward.json.gRaAhM','cases/.VM128-TRANSMUTE-BEING-C.json.z8chdD','evidence/director128-current/DescentReviewChanges/ReviewBible/data/public/spell_candidates/.rank7_identity_casting5_reviewed_122.json.7fIpAC','history/.DD_VitalityMatter10_Director_Conference_128.zip.SX1dxa']:
        assert name in removed

source_bytes = SOURCE_ZIP.read_bytes(); context_bytes = CONTEXT_ZIP.read_bytes()
expect = json.loads(EXPECTATIONS.read_text(encoding='utf-8'))
assert len(source_bytes) == expect['sourceArchive']['bytes'] == 59442222
assert sha(source_bytes) == expect['sourceArchive']['sha256'] == '1a1f35cfc4308c7e8c3481cd9e94cbefd1a098eb0157b4afa7eb6e0f44545f96'
assert package['history/DD_VitalityMatter10_Director_Conference_128.zip'] == source_bytes
assert package['history/DD_SoulContact6_Applied_VitalityMatter10_Context_138.zip'] == context_bytes
assert package['history/VITALITYMATTER10_NEXT_REQUEST_138.txt'] == REQUEST.read_bytes()
verify_nested_zip(source_bytes, 53)
verify_nested_zip(context_bytes, 49)
assert package['authority/CURRENT_HANDOFF_138.json'] == (AUDIT_ROOT/'CURRENT_HANDOFF_138.json').read_bytes()
assert package['authority/CURRENT_SPELL_QUEUE_138.json'] == (AUDIT_ROOT/'CURRENT_SPELL_QUEUE_138.json').read_bytes()
assert package['authority/CURRENT_PENDING_IDENTITY_AUDIT_138.json'] == (AUDIT_ROOT/'CURRENT180_PENDING_IDENTITY_AUDIT_138.json').read_bytes()

index_bytes = INDEX.read_bytes(); catalog_bytes = CATALOG.read_bytes()
before = json.loads(index_bytes); catalog = json.loads(catalog_bytes)
assert before['authoredCounts'] == {'reviewed':668,'pending':180}
assert before['representationCounts']['completeReviewedStandaloneProcedures'] == 392
assert package['authority/authored_review_index.json'] == index_bytes
assert package['authority/catalog.json'] == catalog_bytes
assert sha(catalog_bytes) == before['sourceCatalogSha256']
rows = {x['id']:x for x in before['entries']}
all_pending = [x for x in before['entries'] if x['authoredStatus']=='pending-authored-procedure']
assert len(all_pending) == 180
procs = j(package['PROCEDURES.json']); assert [x['id'] for x in procs] == IDS
native_records = j(package['NATIVE_ACCESS_RECORDS.json'])
current_cards = {x['id']:x for x in catalog['spells']}
for identity, p in zip(IDS,procs):
    row = rows[identity]
    assert row['authoredStatus'] == 'pending-authored-procedure'
    assert row['sourceStatus'] == 'blocked-pending-operational-review'
    assert p['status'] == 'PROPOSED_FOR_EXACT_INDEPENDENT_REVIEW'
    assert p['accepted'] is False and p['applied'] is False
    assert p['completeNativeSourceAndAccessUnchanged'] == current_cards[identity]
    assert native_records[identity] == current_cards[identity]
assert sum(len(native_records[i].get('classAccess',{})) for i in IDS) == 40

source_checks = j(package['SOURCE_VERIFICATION.json'])
assert len(source_checks['sourceBindingsVerified']) == 73
assert source_checks['liveCounts'] == {'reviewed':668,'pending':180}
assert source_checks['sourceProgramsExecuted'] is False
assert source_checks['tenPendingNativeEnvelopesMatchLiveCatalog'] is True
assert source_checks['historicalCountsDoNotOverrideLiveAuthority'] is True

# Independently bind the source conference, all 73 original inputs, 41 accepted interfaces, and 14 counterparts.
source_conference = j(package['ORIGINAL_SOURCE_CONFERENCE.json'])
with zipfile.ZipFile(io.BytesIO(context_bytes)) as context_archive:
    context_conference = context_archive.read('next/vitalitymatter10/vitality_matter_10_source_conference_01.json')
assert package['ORIGINAL_SOURCE_CONFERENCE.json'] == context_conference
assert source_conference['sourceBindings'] == source_checks['sourceBindingsVerified']
assert len(source_conference['records']) == 10
risk = {x['spellId']:x['riskTier'] for x in source_conference['records']}
assert set(risk) == set(IDS) and {tier:list(risk.values()).count(tier) for tier in set(risk.values())} == {'B':5,'C':5}
assert source_conference['riskCounts'] == {'C':5,'B':5}
pre_review = json.loads((AUDIT_ROOT/'VITALITYMATTER10_CURRENT_SOURCE_PREREVIEW_129.json').read_text(encoding='utf-8'))
assert len(pre_review['sourceBindings']) == 73 and all(x['archiveExact'] for x in pre_review['sourceBindings'])
source_outer_for_bindings = zipfile.ZipFile(io.BytesIO(source_bytes))
inner_source_zip = source_outer_for_bindings.read('original/DD_Vitality_Matter_10_Source_Conference_01.zip')
with zipfile.ZipFile(io.BytesIO(inner_source_zip)) as inner:
    assert inner.testzip() is None and len(inner.namelist()) == 77
    inner_manifest = j(inner.read('MANIFEST.json'))
    assert inner_manifest['sourceCount'] == 73 and len(inner_manifest['files']) == 73
    for rec in source_checks['sourceBindingsVerified']:
        member = 'sources/' + rec['path']; b = inner.read(member)
        assert len(b) == rec['bytes'] and sha(b) == rec['sha256'], member
    current_exact = [x['path'] for x in pre_review['sourceBindings'] if x['currentExact']]
    source_records_by_path = {x['path']:x for x in source_checks['sourceBindingsVerified']}
    for path in current_exact:
        b = (ROOT/pathlib.PurePosixPath(path)).read_bytes(); rec = source_records_by_path[path]
        assert len(b) == rec['bytes'] and sha(b) == rec['sha256'], path
assert len(current_exact) == 72
accepted_registry_path = ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json'
accepted_registry = json.loads(accepted_registry_path.read_text(encoding='utf-8'))
def resolve_pointer(root, pointer):
    value = root
    for token in pointer.strip('/').split('/') if pointer else []:
        token = token.replace('~1','/').replace('~0','~')
        value = value[int(token)] if isinstance(value,list) else value[token]
    return value
for comparison in source_conference['currentAcceptedInterfaceComparisons']:
    assert resolve_pointer(accepted_registry, comparison['registryPointer']) == comparison['completeEntryUnchanged']
    assert comparison['scopeLimit']
assert len(source_conference['currentAcceptedInterfaceComparisons']) == 41
current_rows_by_id = {x['id']:x for x in before['entries']}
for counterpart in source_conference['completeAcceptedCounterparts']:
    src = counterpart['source']; source_path = ROOT/pathlib.PurePosixPath(src['path']); b = source_path.read_bytes()
    assert len(b) == src['bytes'] and sha(b) == src['sha256'], src['path']
    assert resolve_pointer(j(b), counterpart['pointer']) == counterpart['completeCurrentCard'], counterpart['spellId']
    assert counterpart['indexEntry'] == current_rows_by_id[counterpart['spellId']], counterpart['spellId']
assert len(source_conference['completeAcceptedCounterparts']) == 14

# Check the exact source question/case/future-obligation records without executing supplied source programs.
source_outer = zipfile.ZipFile(io.BytesIO(source_bytes))
source_questions = j(source_outer.read('INDEPENDENT_QUESTIONS_128.json'))
original = j(package['ORIGINAL_QUESTIONS_CASES_AND_FUTURE_OBLIGATIONS.json'])
assert original['status'] == 'PREPARED_UNSENT_NOT_ACCEPTED'
assert original['sourceOnly'] is True and original['runtimeExecuted'] is False and original['sourceProgramsExecuted'] is False
assert len(source_questions['allQuestions']) == len(original['allQuestions']) == 32
assert original['allQuestions'] == source_questions['allQuestions']
assert original['requiredNewCases'] == source_questions['requiredNewCases']
assert original['originalFutureCaseRequirementsUnchanged'] == source_questions['originalFutureCaseRequirementsUnchanged']
assert len(original['requiredNewCases']) == 21 and len(original['originalFutureCaseRequirementsUnchanged']) == 9
qdisps = j(package['QUESTION_DISPOSITIONS.json']); assert len(qdisps) == 32
qmap = {q['id']:q for q in original['allQuestions']}
for q in qdisps:
    assert q['originalQuestionUnchanged'] == qmap[q['id']]
    assert q['accepted'] is False and q['applied'] is False
    assert q['completeSelectedProcedures']
case_disps = j(package['ORIGINAL_MAIN_CASE_DISPOSITIONS.json']); assert len(case_disps) == 21
source_cases = {c['id']:c for c in original['requiredNewCases']}
for d in case_disps:
    assert d['originalUnchanged'] == source_cases[d['caseId']]
    assert d['unavailableOriginalNotReplacedBySubstitute'] is True
future_disps = j(package['ORIGINAL_FUTURE_OBLIGATION_DISPOSITIONS.json']); assert len(future_disps) == 9
for d, source in zip(future_disps, original['originalFutureCaseRequirementsUnchanged']):
    assert d['originalUnchanged'] == source and d['noClaimThatUnavailableBranchesPassed'] is True

casebook = j(package['CASEBOOK.json'])
main_ids = [x['id'] for x in casebook['mainCases']]
branch_ids = [x['id'] for x in casebook['branches']]
assert main_ids == [x['id'] for x in original['requiredNewCases']]
assert len(main_ids) == 21 and len(branch_ids) == 23 and len(casebook['allCases']) == 44
assert casebook['accepted'] is False and casebook['applied'] is False
case_by_id = {c['id']:c for c in casebook['allCases']}
assert set(case_by_id) == set(main_ids + branch_ids)
event_count = 0; op_count = 0; event_ids = set()
for case in casebook['allCases']:
    assert case['accepted'] is False and case['applied'] is False
    events = case['events']; event_count += len(events)
    if events:
        assert case['initial'] == events[0]['before']
        assert case['final'] == events[-1]['after']
    prev = case['initial']; prev_at = float('-inf')
    for e in events:
        assert e['id'] not in event_ids; event_ids.add(e['id'])
        assert e['before'] == prev
        assert e['at'] >= prev_at
        assert e['after']['time'] == e['at']
        assert len(e['forward']) == 2 and len(e['inverse']) == 2
        assert e['forward'][0] == {'op':'test','path':'','value':e['before']}
        assert e['forward'][1] == {'op':'replace','path':'','value':e['after']}
        assert e['inverse'][0] == {'op':'test','path':'','value':e['after']}
        assert e['inverse'][1] == {'op':'replace','path':'','value':e['before']}
        op_count += len(e['forward']) + len(e['inverse'])
        prev = e['after']; prev_at = e['at']
assert event_count == 176 and op_count == 704
validation = j(package['VALIDATION.json']); final_validation = j(package['VALIDATION_FINAL.json'])
assert validation['failed'] == 0 and validation['checksPassed'] == 2985
assert validation['sourceProgramsExecuted'] is False and validation['runtimeExecuted'] is False
assert validation['accepted'] is False and validation['applied'] is False
assert final_validation['eventsChecked'] == 176 and final_validation['failed'] == 0
assert final_validation['eventChronologySorted'] is True and final_validation['allEventFullValueOpsRefreshed'] is True
assert final_validation['noSuppliedHistoricalProgramsExecuted'] is True and final_validation['runtimeExecuted'] is False

# Confirm required complete authored profiles are present, separately from source-discovered facts.
profiles = j(package['NEW_NATIVE_PROFILES.json'])
assert set(profiles) == {'colossus','zombie','Elemental','Beast','Ooze'}
for key, required in {
    'colossus':['provenance','size','boxFeet','massLb','abilities','AC','baseHP','saves','speed','support','senses','grippers','speech','reach','slam','cleave'],
    'zombie':['provenance','size','boxFeet','massLb','abilities','AC','baseHP','saves','speed','support','senses','grippers','speech','attack','lifetimeSeconds'],
    'Elemental':['provenance','size','boxFeet','massLb','abilityAssignments','maxHP','AC','speed','hands','speech','senses','support','attacks','immunities','resistances','needs','gear','carry'],
    'Beast':['provenance','size','boxFeet','massLb','abilityAssignments','maxHP','AC','speed','hands','speech','senses','support','attacks','immunities','resistances','needs','gear','carry'],
    'Ooze':['provenance','size','boxFeet','massLb','abilityAssignments','maxHP','AC','speed','hands','speech','senses','support','attacks','immunities','resistances','needs','gear','carry'],
}.items():
    assert set(required) <= set(profiles[key]), (key, set(required)-set(profiles[key]))
assert profiles['colossus']['baseHP'] == 140 and profiles['zombie']['baseHP'] == 30

holds = j(package['HOLD_REGISTER.json'])
assert holds['accepted'] is False and holds['applied'] is False
assert len(holds['holds']) == 19
hold_text = json.dumps(holds,ensure_ascii=False).casefold()
for phrase in ['vm139-high-native-str','vm139-structural-support','vm139-circle-sites','vm139-carried-transport','vm139-null-access','vm139-independent-immunities','vm139-warrior-injection','vm139-healing-touch','vm139-cellular-recipient','vm139-freeze-immunities','vm139-reattach-route']:
    assert phrase in hold_text, phrase

# Check accepted-counterpart and actual class-source bindings against the live workspace.
base = json.loads(COUNTERPARTS.read_text(encoding='utf-8'))
assert base['currentAuthority'] == {'reviewed':668,'pending':180,'acceptedUnapplied':0}
for group in ['acceptedCounterparts','classCardSources']:
    for item in base[group]:
        bnd = item.get('file') or item.get('modelFile') or item
        path = ROOT / pathlib.PurePosixPath(bnd['path'])
        b = path.read_bytes()
        assert len(b) == bnd['bytes'] and sha(b) == bnd['sha256'], bnd['path']

# The package's own delivery inventory and scope statements are independently consistent.
contents = j(package['DELIVERY_CONTENTS.json'])
assert contents['identities'] == IDS
assert contents['procedures'] == 10 and contents['originalQuestions'] == 32
assert contents['requiredMainCases'] == 21 and contents['additionalBranches'] == 23
assert contents['events'] == 176 and contents['fullForwardInverseEventOperations'] == 704
assert contents['originalFutureObligations'] == 9 and contents['nativeClassAccessRows'] == 40
assert contents['authority'] == {'applied':668,'pending':180,'acceptedUnapplied':0}
assert contents['accepted'] is False and contents['applied'] is False
assert contents['runtimeExecuted'] is False and contents['humanPlayClaim'] is False
assert contents['balanceClaim'] is False and contents['cosmologyClaim'] is False and contents['releaseClaim'] is False

RETURN_DIR.mkdir(parents=True,exist_ok=True)
shutil.copy2(ZIP,RETURN_DIR/ZIP.name); shutil.copy2(DELIVERY,RETURN_DIR/'DIRECTOR_RETURN_DELIVERY.json')
report = {
 'id':'VITALITYMATTER10-RETURN01-CLEAN01-INDEPENDENT-AUDIT-139',
 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'decision':'PASS_READY_FOR_EXACT_ACCEPTANCE_WITH_RETAINED_HOLDS',
 'scope':IDS,
 'authorityBefore':{'reviewed':668,'pending':180,'acceptedUnapplied':0,'indexBytes':len(index_bytes),'indexSha256':sha(index_bytes)},
 'directorReturn':{'file':ZIP.name,'bytes':len(zip_bytes),'sha256':zip_hash,'members':len(names),'manifestBindings':len(recs),'allMemberBindingsPassed':True,'crcPassed':True,'hiddenOrPartialMembersPresent':False,'packagingOnlyRepairPreservedCanonicalBytes':True},
 'sourceAuthority':{'sourceConferenceBytes':len(source_bytes),'sourceConferenceSha256':sha(source_bytes),'sourceConferenceMemberBindingsPassed':True,'appliedContextBytes':len(context_bytes),'appliedContextSha256':sha(context_bytes),'appliedContextMemberBindingsPassed':True,'sourceBindings':73,'nativeClassAccessRows':40},
 'currentNativeAndAccess':{'tenWholeCardsExactlyMatchCurrentCatalog':True,'currentAuthorityIndexCopyExact':True,'currentCatalogCopyExact':True,'pendingRowsPreserved':True},
 'preservation':{'originalQuestions':32,'originalMainCases':21,'additionalBranches':23,'futureObligations':9,'fullStateEvents':event_count,'fullForwardInverseEventOperations':op_count,'eventStateChainsAndInverseOperationsPassed':True},
 'profilesAndHolds':{'completeNewProfiles':['colossus','zombie','Elemental','Beast','Ooze'],'openSourceAndUnavailableBranchHolds':len(holds['holds']),'requiredHoldIdsRetained':True,'unavailableBranchesClaimedPassed':False},
 'validation':{'directorFocusedChecks':validation['checksPassed'],'directorFailures':validation['failed'],'independentStructuralChecksPassed':True,'sourceProgramsExecuted':False,'runtimeExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False},
 'failures':[]
}
report_path = RETURN_DIR/'VITALITYMATTER10_RETURN01_CLEAN01_INDEPENDENT_AUDIT_139.json'
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'decision':report['decision'],'zipBytes':len(zip_bytes),'zipSha256':zip_hash,'members':len(names),'manifestBindings':len(recs),'sourceBindings':73,'questions':32,'mainCases':21,'branches':23,'events':event_count,'operations':op_count,'holds':len(holds['holds']),'audit':str(report_path)},indent=2))






