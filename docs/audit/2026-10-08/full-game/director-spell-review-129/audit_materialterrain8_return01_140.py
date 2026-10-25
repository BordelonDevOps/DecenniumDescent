import copy,gzip,hashlib,io,json,pathlib,zipfile
from datetime import datetime,timezone
R=pathlib.Path('C:/Github/DecenniumDescent')
D=R/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RET=D/'materialterrain8_return01_140_received'
ZIP=RET/'DD_MaterialTerrain8_Director_Return01_140.zip'
DEL=RET/'DIRECTOR_RETURN_DELIVERY.json'
INDEX=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CAT=R/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
IDS=['control-water','fabricate','transmute-terrain','magnetize-field','passwall','transmute-rock','displace-structure','move-earth']
def sha(b):return hashlib.sha256(b).hexdigest()
def j(b):return json.loads(b.decode('utf-8'))
def pathbind(p):b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def ptr(root,p):
 x=root
 for t in p.strip('/').split('/') if p else []:
  t=t.replace('~1','/').replace('~0','~')
  x=x[int(t)] if isinstance(x,list) else x[t]
 return x
blob=ZIP.read_bytes();delivery=j(DEL.read_bytes())
assert len(blob)==delivery['bytes']==16979114
assert sha(blob)==delivery['sha256']=='2c43939f661d57edf08f2f624522972f45f3414ea58e7ab70ad682437d9a1ead'
assert delivery['accepted'] is False and delivery['applied'] is False
assert delivery['counts']=={'applied':678,'pending':170,'acceptedUnapplied':0}
with zipfile.ZipFile(io.BytesIO(blob)) as z:
 assert z.testzip() is None
 names=z.namelist(); assert len(names)==len(set(names))==112
 manifest=j(z.read('MANIFEST.json')); recs={x.get('path',x.get('file')):x for x in manifest['files']}
 assert manifest['accepted'] is False and manifest['applied'] is False
 assert set(names)-{'MANIFEST.json'}==set(recs) and len(recs)==111
 for n,rec in recs.items():
  b=z.read(n); assert len(b)==rec.get('bytes',rec.get('length')) and sha(b)==rec.get('sha256',rec.get('hash')),n
 pkg={n:z.read(n) for n in names}
hidden=[n for n in names if pathlib.PurePosixPath(n).name.startswith('.') or '.tmp' in pathlib.PurePosixPath(n).name.casefold()]
assert not hidden
index_raw=INDEX.read_bytes(); index=j(index_raw); cat_raw=CAT.read_bytes(); catalog=j(cat_raw)
assert index['authoredCounts']=={'reviewed':678,'pending':170}
assert index['representationCounts']['completeReviewedStandaloneProcedures']==402
assert pkg['authority/authored_review_index.json']==index_raw and pkg['authority/catalog.json']==cat_raw
assert pkg['authority/CURRENT_SPELL_QUEUE_139.json']==(D/'CURRENT_SPELL_QUEUE_139.json').read_bytes()
assert pkg['authority/CURRENT_HANDOFF_139.json']==(D/'CURRENT_HANDOFF_139.json').read_bytes()
assert pkg['authority/CURRENT170_PENDING_IDENTITY_AUDIT_139.json']==(D/'CURRENT170_PENDING_IDENTITY_AUDIT_139.json').read_bytes()
queue=j(pkg['authority/CURRENT_SPELL_QUEUE_139.json'])
pending={e['id'] for e in index['entries'] if e['authoredStatus']=='pending-authored-procedure'}
assert queue['currentAuthority']['pending']==len(pending)==170
mt=next(g for g in queue['currentPendingGroups'] if g['group']=='material-terrain8')
assert mt['pendingIds']==IDS
assert all(next(e for e in index['entries'] if e['id']==sid)['authoredStatus']=='pending-authored-procedure' for sid in IDS)
records=j(pkg['ORIGINAL_CONFERENCE_02.json'])
assert records['countsUnchanged']=={'reviewed':480,'pending':368} # historical packet counts explicitly superseded
assert pkg['history/DD_Material_Terrain_8_Conference_02.zip']==(R/'docs/audit/2026-10-08/full-game/DD_Material_Terrain_8_Conference_02.zip').read_bytes()
assert pkg['history/DD_VitalityMatter10_Applied_MaterialTerrain8_Context_139.zip']==(D/'DD_VitalityMatter10_Applied_MaterialTerrain8_Context_139.zip').read_bytes()
assert pkg['history/MATERIAL_TERRAIN8_NEXT_REQUEST_139.txt']==(D/'MATERIAL_TERRAIN8_NEXT_REQUEST_139.txt').read_bytes()
source_zip=R/'docs/audit/2026-10-08/full-game/DD_Material_Terrain_8_Conference_02.zip'
source_conf=R/'DescentReviewChanges/ReviewBible/data/director/spell_review/material_terrain_8_conference_02.json'
assert sha(source_zip.read_bytes())==next(g for g in queue['currentPendingGroups'] if g['group']=='material-terrain8')['archive']['sha256']
assert sha(source_conf.read_bytes())==next(g for g in queue['currentPendingGroups'] if g['group']=='material-terrain8')['candidate']['sha256']
# Verify the embedded conference and exact historical source archive.
source_audit=j(pkg['evidence/source02/LOCAL_PREFLIGHT.json'])
assert source_audit['failureCount']==0 and source_audit['runtimeTestsExecuted']==0
assert pkg['evidence/source02/sources/DescentReviewChanges/ReviewBible/data/director/spell_review/material_terrain_8_conference_02.json']==source_conf.read_bytes()
source_manifest=j(pkg['evidence/source02/MANIFEST.json'])
source_recs={x['archivePath']:x for x in source_manifest['sources']}
assert len(source_recs)==42
for n,rec in source_recs.items():
 b=pkg['evidence/source02/'+n]
 assert len(b)==rec.get('bytes',rec.get('length')) and sha(b)==rec.get('sha256',rec.get('hash')),n
sv=j(pkg['SOURCE_VERIFICATION.json'])
assert sv['liveAuthority']=={'applied':678,'pending':170,'acceptedUnapplied':0}
assert sv['nativeEnvelopesMatchLiveCatalog'] is True and sv['historicalCountsSuperseded'] is True and sv['suppliedHistoricalProgramsExecuted'] is False
matched=0; stale=[]
for rec in sv['exactBindings']:
 p=R/pathlib.PurePosixPath(rec['path']); b=p.read_bytes()
 if len(b)==rec['bytes'] and sha(b)==rec['sha256']:matched+=1
 else:stale.append(rec['path'])
assert len(sv['exactBindings'])==38 and matched==37 and stale==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json']
# The sole stale source binding is the historical index; the exact current index is bound above.
# Validate all eight live catalog cards/access rows and all 54 class-access records.
procedures=j(pkg['PROCEDURES.json']); assert [p['id'] for p in procedures]==IDS
native=j(pkg['NATIVE_SOURCE_ACCESS.json']); rows={e['id']:e for e in index['entries']}; cards={s['id']:s for s in catalog['spells']}
for p in procedures:
 sid=p['id']; row=rows[sid]
 assert row['authoredStatus']=='pending-authored-procedure' and row['sourceStatus']=='blocked-pending-operational-review'
 assert p['accepted'] is False and p['applied'] is False
 assert p['completeNativeSourceAndAccessUnchanged']==cards[sid]==native[sid]
 assert p['status']=='DIRECTOR_PROPOSED_PENDING_INDEPENDENT_EXACT_REVIEW'
assert sum(len(native[sid]['classAccess']) for sid in IDS)==54
# 18 inherited interfaces remain exact against current accepted registry06; 3 accepted counterparts are live.
reg=json.loads((R/'DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json').read_text(encoding='utf-8'))
assert len(records['inheritedAcceptedInterfaces'])==18
for x in records['inheritedAcceptedInterfaces']:assert ptr(reg,x['registryPointer'])==x['completeEntryUnchanged']
assert len(records['completeAcceptedCounterparts'])==3
for x in records['completeAcceptedCounterparts']:
 raw=(R/pathlib.PurePosixPath(x['source']['path'])).read_bytes()
 assert len(raw)==x['source']['bytes'] and sha(raw)==x['source']['sha256']
 assert ptr(j(raw),x['wholeCardPointer'])==x['completeCurrentCard']
 assert x['indexEntry']==next(e for e in index['entries'] if e['id']==x['spellId'])
# All original conference questions, scenarios, findings and corrected procedures are preserved.
questions=j(pkg['ORIGINAL_16_QUESTIONS.json']); scenarios=j(pkg['ORIGINAL_16_SCENARIOS.json'])
assert len(questions)==len(scenarios)==16
assert questions==records['conferenceQuestions'] and scenarios==records['all16HistoricalScenarioTexts']
qdisps=j(pkg['QUESTION_DISPOSITIONS.json']);assert len(qdisps)==16
qmap={q['id']:q for q in questions}
for q in qdisps:
 assert q['originalQuestionUnchanged']==qmap[q['id']]
 assert q['accepted'] is False and q['applied'] is False and q['sourceContentGapsRetained'] is True
findings=j(pkg['FINDING_DISPOSITIONS.json']);assert len(findings)==10 and all(not x['accepted'] and not x['applied'] for x in findings)
scenario_disps=j(pkg['SCENARIO_DISPOSITIONS.json']);assert len(scenario_disps)==16
smap={s['id']:s for s in scenarios}
for d in scenario_disps:
 assert d['originalScenarioUnchanged']==smap[d['caseId']]
 assert d['notOperationalCampaignProof'] is True
casebook=j(pkg['CASEBOOK.json'])
assert len(casebook['mainCases'])==16 and len(casebook['additionalBranches'])==8 and len(casebook['allCases'])==24
assert casebook['accepted'] is False and casebook['applied'] is False
assert [c['id'] for c in casebook['mainCases']]==[s['id'] for s in scenarios]
assert {c['id'] for c in casebook['allCases']}=={c['id'] for c in casebook['mainCases']+casebook['additionalBranches']}
# Full-state chains: state continuity, sorted time and exact forward/inverse test-replace operations.
event_count=0; operation_count=0; event_ids=set()
for c in casebook['allCases']:
 assert c['accepted'] is False and c['applied'] is False
 evs=c['events'];event_count+=len(evs)
 if evs:
  assert c['initial']==evs[0]['before'] and c['final']==evs[-1]['after']
 prev=c.get('initial');previous_time=float('-inf')
 for e in evs:
  assert e['id'] not in event_ids;event_ids.add(e['id'])
  assert e['before']==prev and e['time']>=previous_time
  assert e['after']['time']==e['time']
  assert e['forward']==[{'op':'test','path':'','value':e['before']},{'op':'replace','path':'','value':e['after']}]
  assert e['inverse']==[{'op':'test','path':'','value':e['after']},{'op':'replace','path':'','value':e['before']}]
  prev=e['after'];previous_time=e['time'];operation_count+=len(e['forward'])+len(e['inverse'])
assert event_count==52 and operation_count==208
# Compare exact procedure source records and ensure changes are expressly proposed, not silently attributed to source.
pmap={p['id']:p for p in procedures}
for rec in records['records']:
 sid=rec['spellId'];p=pmap[sid]
 assert p['originalProcedureUnchanged']==rec['completeEarlierRecordUnchanged']['procedure']
 assert p['accepted'] is False and p['applied'] is False
assert len(j(pkg['PROCEDURE_REVISION_OPERATIONS.json'])['operations'])==8
assert len(j(pkg['CASE_AUTHORING_OPERATIONS.json'])['operations'])==24
holds=j(pkg['HOLD_REGISTER.json'])
assert holds['accepted'] is False and holds['applied'] is False and len(holds['sourceHolds'])==28
assert all(h['wholeCaseOrRequiredBranch'] is True and h['originalNotPromoted'] is True for h in holds['sourceHolds'])
validation=j(pkg['VALIDATION.json'])
assert validation['checksPassed']==1161 and validation['failed']==0 and validation['runtimeExecuted'] is False
assert validation['accepted'] is False and validation['applied'] is False and validation['mainCases']==16 and validation['additionalBranches']==8 and validation['events']==52
# Exact geometry reconciliation retained and described as conditional rather than authority.
geometry=records['occupiedSpaceReconciliation02']
assert geometry['previousCandidate']=={'path':'DescentReviewChanges/ReviewBible/data/director/spell_review/material_terrain_8_conference_01.json','bytes':598586,'sha256':'641431e47ed00daf65530d6117315265d73ab9c9c9b0366a36214bb4027ad1b2'}
assert geometry['fullDelta']=={'path':'docs/audit/2026-10-08/full-game/MATERIAL_TERRAIN_8_GEOMETRY_DELTA_02.json','bytes':35858,'sha256':'4e226332aa6ca144d386605d712418e32cd7aa4211c158ca15a0beb9e1ef6122'}
assert geometry['previousMetadataUnchanged']=={'id':'MATERIAL-TERRAIN-8-CONFERENCE-01','recordedAtUtc':'2026-10-18T04:59:09.969712+00:00','status':'UNSENT / UNADOPTED design conference before substantial new systemic rules.'}
assert geometry['actualGPTConcurrence'] is False
assert pkg['evidence/source02/sources/docs/audit/2026-10-08/full-game/MATERIAL_TERRAIN_8_GEOMETRY_DELTA_02.json']==(R/'docs/audit/2026-10-08/full-game/MATERIAL_TERRAIN_8_GEOMETRY_DELTA_02.json').read_bytes()
assert len(pkg['evidence/source02/sources/docs/audit/2026-10-08/full-game/MATERIAL_TERRAIN_8_GEOMETRY_DELTA_02.json'])==geometry['fullDelta']['bytes']
assert sha(pkg['evidence/source02/sources/docs/audit/2026-10-08/full-game/MATERIAL_TERRAIN_8_GEOMETRY_DELTA_02.json'])==geometry['fullDelta']['sha256']
assert 'actualGPTConcurrence' in geometry
assert j(pkg['NEXT_GROUP_BOUNDARY.json'])['closedCohortsOrFeatsReopened'] is False
report={
 'id':'MATERIALTERRAIN8-RETURN01-INDEPENDENT-AUDIT-140',
 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'decision':'PASS_READY_FOR_EXACT_AUTHORED_PROCEDURE_ACCEPTANCE_WITH_RETAINED_SOURCE_CASE_HOLDS',
 'scope':IDS,
 'authorityBefore':{'reviewed':678,'pending':170,'acceptedUnapplied':0,'indexBytes':len(index_raw),'indexSha256':sha(index_raw)},
 'directorReturn':{'file':ZIP.name,'bytes':len(blob),'sha256':sha(blob),'members':len(names),'manifestBindings':len(recs),'crcPassed':True,'allMemberHashesPassed':True,'hiddenTemporaryMembers':0,'acceptedInReturn':False,'appliedInReturn':False},
 'sourceAuthority':{'sourceConference02Exact':True,'sourceConferenceArchiveExact':True,'sourceManifestBindings':42,'sourceVerificationBindings':38,'liveExact':matched,'oneHistoricalIndexSnapshotSuperseded':stale[0],'currentAuthorityCopyExact':True,'currentQueueHandoffAndPendingAuditExact':True},
 'currentNativeAndAccess':{'eightCardsAndAccessExactlyMatchLiveCatalog':True,'classAccessRows':54,'pendingRowsRemainBlocked':True},
 'acceptedInterfacesAndCounterparts':{'registry06PointersChecked':18,'currentAcceptedCounterpartsChecked':3},
 'preservation':{'originalQuestions':16,'originalScenarios':16,'mainCases':16,'additionalBranches':8,'events':event_count,'forwardInverseOperations':operation_count,'exactOriginalRecordsPreserved':True},
 'focusedValidation':{'directorChecks':1161,'directorFailures':0,'independentStructuralChecksPassed':True,'sourceProgramsExecuted':False,'runtimeExecuted':False},
 'holds':{'explicitWholeCaseOrRequiredBranchHolds':len(holds['sourceHolds']),'allOriginalSourceScenariosRemainUnpromoted':True,'missingPhysicalProfilesAndWorkOrdersHeld':True,'geometryCorrectionGPTConcurrence':False,'geometryDeltaExact':True},
 'failures':[]
}
(D/'MATERIALTERRAIN8_RETURN01_INDEPENDENT_AUDIT_140.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
