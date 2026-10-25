from __future__ import annotations
import copy, hashlib, json, pathlib, sys, zipfile
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(r'C:\Github\DecenniumDescent')
A=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RET=A/'rank7gateglyph3_return01_141_repack01_received'
DEL=RET/'DIRECTOR_RETURN_DELIVERY.json'
OLDZIP=A/'rank7gateglyph3_return01_141_received/DD_Rank7GateGlyph3_Director_Return01_141.zip'
EXTRACT=A/'rank7gateglyph3_return01_141_extracted'
ZIP=RET/'DD_Rank7GateGlyph3_Director_Return01_141.zip'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE=A/'CURRENT_SPELL_QUEUE_140.json'
PENDING=A/'CURRENT162_PENDING_IDENTITY_AUDIT_140.json'
HANDOFF=A/'CURRENT_HANDOFF_140.json'
CAND=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank7_gate_glyph_3_source_conference_01.json'
SOURCEZIP=ROOT/'docs/audit/2026-10-08/full-game/DD_Rank7_Gate_Glyph_3_Source_Conference_01.zip'
IDS=['chain-gate','symbol','symbol-of-death']
EXPECTED_DELIVERY={'bytes':24346593,'sha256':'1b32037cb0898e199ee9a78c0a99faafb0389002473f25355e651a79da54abad','manifestSHA256':'7c01026ade45cb9e36ca5f74f11e7346118f1e65e71084d3a4ab2e5531844996','archiveMembers':168,'manifestBoundMembers':167}
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def bind(p):
 b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def getptr(doc,pointer):
 if pointer=='': return doc
 cur=doc
 for raw in pointer.lstrip('/').split('/'):
  part=raw.replace('~1','/').replace('~0','~')
  cur=cur[int(part)] if isinstance(cur,list) else cur[part]
 return cur
def setptr(doc,pointer,value):
 if pointer=='': return copy.deepcopy(value)
 parts=[x.replace('~1','/').replace('~0','~') for x in pointer.lstrip('/').split('/')]
 cur=doc
 for part in parts[:-1]: cur=cur[int(part)] if isinstance(cur,list) else cur[part]
 if isinstance(cur,list): cur[int(parts[-1])]=copy.deepcopy(value)
 else: cur[parts[-1]]=copy.deepcopy(value)
 return doc
def replay(doc,ops):
 out=copy.deepcopy(doc)
 for op in ops:
  actual=getptr(out,op['path'])
  if op['op']=='test': assert actual==op['value'],('test',op['path'])
  elif op['op']=='replace': out=setptr(out,op['path'],op['value'])
  else: raise AssertionError(('unknown op',op['op']))
 return out
# Outer delivery and complete member binding.
raw=ZIP.read_bytes(); assert len(raw)==EXPECTED_DELIVERY['bytes'] and sha(raw)==EXPECTED_DELIVERY['sha256']
delivery=json.loads(DEL.read_text(encoding='utf-8')); assert delivery['bytes']==len(raw) and delivery['sha256']==sha(raw)
assert delivery['manifestSHA256']==EXPECTED_DELIVERY['manifestSHA256'] and delivery['accepted'] is False and delivery['applied'] is False
assert delivery['authority']=={'reviewedApplied':686,'pending':162,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':410}
assert delivery['savedArtifactVerification']['matchesLocalZIP'] is True and delivery['savedArtifactVerification']['version']==2
assert delivery['savedArtifactVerification']['roundTripBytes']==len(raw) and delivery['savedArtifactVerification']['roundTripSHA256']==sha(raw)
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 names=z.namelist(); assert len(names)==EXPECTED_DELIVERY['archiveMembers']
 manifest=json.loads(z.read('MANIFEST.json')); assert sha(z.read('MANIFEST.json'))==EXPECTED_DELIVERY['manifestSHA256']
 recs=manifest['members']; assert len(recs)==EXPECTED_DELIVERY['manifestBoundMembers']
 byname={x['path']:x for x in recs}; assert len(byname)==len(recs)
 assert set(names)-{'MANIFEST.json'}==set(byname)
 assert manifest['memberCountIncludingSelf']==len(names) and manifest['boundMembers']==len(recs)
 hidden=[n for n in names if pathlib.PurePosixPath(n).name.startswith('.') or '.tmp' in pathlib.PurePosixPath(n).name.casefold() or '.partial' in pathlib.PurePosixPath(n).name.casefold()]
 assert not hidden,hidden
 payload={n:z.read(n) for n in names}
with zipfile.ZipFile(OLDZIP) as oldz:
 oldnames=set(oldz.namelist()); assert oldnames==set(names)
 changed=sorted(n for n in names if oldz.read(n)!=payload[n])
 assert changed==['ARTIFACT_BINDINGS.json','CASEBOOK.json','MANIFEST.json','cases/GG141-CHAIN-B.json','cases/GG141-DEATH-A__sixty-one.json']
 oldcb=json.loads(oldz.read('CASEBOOK.json')); newcb=json.loads(payload['CASEBOOK.json'])
 oldevents={e['id']:e for c in oldcb['allCases'] for e in c['events']}
 targets=[('GG141-CHAIN-B:3','afterSHA256'),('GG141-CHAIN-B:4','beforeSHA256'),('GG141-DEATH-A/sixty-one:9','afterSHA256')]
 for section in ['mainCases','branches','allCases']:
  for case in newcb[section]:
   for event in case['events']:
    for eid,key in targets:
     if event['id']==eid: event[key]=oldevents[eid][key]
 assert newcb==oldcb
 for rel in ['cases/GG141-CHAIN-B.json','cases/GG141-DEATH-A__sixty-one.json']:
  oldcase=json.loads(oldz.read(rel)); newcase=json.loads(payload[rel])
  oldevent={e['id']:e for e in oldcase['events']}
  for eid,key in targets:
   for event in newcase['events']:
    if event['id']==eid: event[key]=oldevent[eid][key]
  assert newcase==oldcase,rel
 for n,rec in byname.items():
  b=payload[n]; assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],n
assert manifest['accepted'] is False and manifest['applied'] is False
assert manifest['authority']=={'reviewedApplied':686,'pending':162,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':410}
# Exact live authority snapshot and source bytes.
ib=INDEX.read_bytes(); cb=CATALOG.read_bytes(); qb=QUEUE.read_bytes(); pb=PENDING.read_bytes(); hb=HANDOFF.read_bytes()
assert payload['authority/authored_review_index.json']==ib
assert payload['authority/catalog.json']==cb
assert payload['authority/CURRENT_SPELL_QUEUE_140.json']==qb
assert payload['authority/CURRENT162_PENDING_IDENTITY_AUDIT_140.json']==pb
assert payload['authority/CURRENT_HANDOFF_140.json']==hb
assert payload['source/rank7_gate_glyph_3_source_conference_01.json']==CAND.read_bytes()
assert payload['history/DD_Rank7_Gate_Glyph_3_Source_Conference_01.zip']==SOURCEZIP.read_bytes()
index=json.loads(ib); catalog=json.loads(cb); queue=json.loads(qb); pending=json.loads(pb)
assert index['authoredCounts']=={'reviewed':686,'pending':162}
assert index['representationCounts']['completeReviewedStandaloneProcedures']==410
assert pending['pendingCount']==162 and pending.get('acceptedUnapplied',0)==0
assert queue['currentPendingGroups'][0]['group']=='rank7-gate-glyph3'
assert queue['currentPendingGroups'][0]['pendingIds']==IDS
pending_ids={e['id'] for e in index['entries'] if e['authoredStatus']=='pending-authored-procedure'}
assert len(pending_ids)==162 and not (set(IDS)&(set(pending_ids)-set(IDS)))
rows={e['id']:e for e in index['entries']}; cards={s['id']:s for s in catalog['spells']}
assert all(rows[sid]['authoredStatus']=='pending-authored-procedure' and rows[sid]['sourceStatus']=='blocked-pending-operational-review' for sid in IDS)
# Native identity/access envelopes, unchanged source questions and requirements.
procedures=json.loads(payload['PROCEDURES.json'])
assert [p['id'] for p in procedures]==IDS
access_rows=0
for p in procedures:
 sid=p['id']; assert p['accepted'] is False and p['applied'] is False
 assert p['completeNativeCardAndAccessUnchanged']==cards[sid]
 assert p['completeNativeCardAndAccessUnchanged']['operational'] is None
 access_rows+=len(cards[sid]['classAccess'])
assert access_rows==14
source=json.loads(CAND.read_text(encoding='utf-8'))
assert payload['ORIGINAL_15_CONFERENCE_QUESTIONS.json']==canon(source['questions']) or json.loads(payload['ORIGINAL_15_CONFERENCE_QUESTIONS.json'])==source['questions']
assert json.loads(payload['ORIGINAL_FUTURE_CASE_REQUIREMENTS.json'])==source['futureCaseRequirements']
assert len(json.loads(payload['ORIGINAL_IDENTITY_QUESTIONS_AND_SCOPE.json']))==3
qdisp=json.loads(payload['QUESTION_DISPOSITIONS.json']); assert len(qdisp)==18
assert len([q for q in qdisp if q['questionKind']=='conference'])==15
# Every question choice is explicit; exact source text preserved per ID.
source_questions={q['id']:q for q in source['questions']}
for q in qdisp:
 if q['questionKind']=='conference': assert q['originalQuestionUnchanged']==source_questions[q['id']]
 assert q.get('selection') and ('selectedOption' in q or 'completeSelectedProcedure' in q)
# Case and operation ledgers: exact counts, continuity, hash binding, and forward/inverse replay.
casebook=json.loads(payload['CASEBOOK.json']); main=casebook['mainCases']; branches=casebook['branches']; cases=casebook['allCases']
assert (len(main),len(branches),len(cases))==(6,27,33)
assert len({c['id'] for c in cases})==33
assert all(c['spellId'] in IDS for c in cases)
assert sum(len(c['events']) for c in cases)==159
assert len([c for c in cases if c['caseKind']=='main'])==6
case_ids={c['id'] for c in cases}
for c in cases:
 assert c['events'] and c['initial']==c['events'][0]['before'] and c['final']==c['events'][-1]['after'],c['id']
 for i,e in enumerate(c['events']):
  assert e['beforeSHA256']==sha(canon(e['before'])) and e['afterSHA256']==sha(canon(e['after'])),e['id']
  assert replay(e['before'],e['forward'])==e['after'],e['id']
  assert replay(e['after'],e['inverse'])==e['before'],e['id']
  assert e['at']==e['after']['time'] and e['at']>=e['before']['time'],e['id']
  if i: assert c['events'][i-1]['after']==e['before'],(c['id'],e['id'])
  for op in (e['forward']+e['inverse']): assert op['op'] in ('test','replace')
assert sum(len(e['forward']) for c in cases for e in c['events'])==318
assert sum(len(e['inverse']) for c in cases for e in c['events'])==318
caseops=json.loads(payload['CASE_AUTHORING_OPERATIONS.json'])['operations']
procops=json.loads(payload['PROCEDURE_AUTHORING_OPERATIONS.json'])['operations']
assert len(caseops)==33 and len(procops)==3
for op in caseops:
 assert op['id'] in case_ids
 assert replay({'operational':None},op['forward'])['operational']['id']==op['id']
 assert replay(replay({'operational':None},op['forward']),op['inverse'])=={'operational':None}
for op in procops:
 assert op['id'] in IDS and op['sourceCardUnchanged']==cards[op['id']]
 assert replay({'operational':None},op['forward'])['operational'] is not None
 assert replay(replay({'operational':None},op['forward']),op['inverse'])=={'operational':None}
# Case-file mirrors and retained whole-case holds.
for c in cases:
 path='cases/'+c['id'].replace('/','__')+'.json'
 assert path in payload
 assert json.loads(payload[path])==c
holds=json.loads(payload['HOLD_REGISTER.json']); hold_ids={h['id'] for h in holds['holds']}
assert holds['counts']=={'returnHoldRecords':9,'contentHolds':7,'reviewAndInheritedBoundaryHolds':2,'caseHoldReferences':15}
assert holds['accepted'] is False and holds['applied'] is False
assert {'H-NONLIVING-PROFILE','H-ZERO-STATE-ORIGIN'}<=hold_ids
assert all(set(c.get('holdIds',[]))<=hold_ids for c in cases)
assert sum(1 for c in cases if 'H-GATE-SITES' in c.get('holdIds',[]))==8
# Required provenance/control boundaries and explicit no-runtime claims.
validation=json.loads(payload['VALIDATION.json']); counts=json.loads(payload['EXACT_COUNTS.json'])
assert validation['checksPassed']==3051 and validation['checksFailed']==0
assert validation['accepted'] is False and validation['applied'] is False
assert validation['sourceProgramsExecuted'] is False and validation['historicalProgramsExecuted'] is False and validation['gameRuntimeExecuted'] is False
assert counts['originalScenarios']==0 and counts['originalFutureCaseRequirements']==8
assert json.loads(payload['ACTOR_PROFILES.json'])['W1']['campaignAuthenticated'] is False
assert json.loads(payload['ACTOR_PROFILES.json'])['W13']['campaignAuthenticated'] is False
assert json.loads(payload['ACTOR_PROFILES.json'])['CL16']['campaignAuthenticated'] is False
# Positive case conditions that must remain local/conditional are retained explicitly.
chain_hold=next(h for h in holds['holds'] if h['id']=='H-GATE-SITES')
assert len(chain_hold['caseReferences'])==8
assert 'not canonical planes' in chain_hold['text']
assert all(c['classification']!='FULL_EXPECTED_DATA_ONLY' for c in cases if c['spellId']=='chain-gate')
# Symbol and Death explicit thresholds and payload details are documented, while missing identities remain held.
proc_text=payload['STANDALONE_PROCEDURES.md'].decode('utf-8')
for needle in ['6d8','10-foot-radius','60 seconds','normal HP','Death Ward','A→B→C→A']:
 assert needle.casefold() in proc_text.casefold(),needle
# Summary: additional delivery JSON was reviewed in the GPT Library UI and matched exact local ZIP size/hash.
report={
 'id':'RANK7-GATEGlyph3-RETURN01-INDEPENDENT-AUDIT-141',
 'status':'PASS_READY_FOR_EXACT_AUTHORED_PROCEDURE_ACCEPTANCE_WITH_RETAINED_SOURCE_CASE_HOLDS',
 'decision':'ACCEPT_FOR_AUTHORED_PROCEDURE_REVIEW_ONLY_AND_APPLY_EXACTLY_THREE_IDENTITIES',
 'directorReturn':{'path':ZIP.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':sha(raw),'manifestSHA256':sha(payload['MANIFEST.json']),'memberCount':len(names),'boundMembers':len(recs),'hiddenOrTemporaryMembers':len(hidden),'integrityOnlyChangedMembersComparedWithOriginal':changed},
 'separateDeliveryManifest':{'path':DEL.relative_to(ROOT).as_posix(),'binding':bind(DEL),'reviewedInChatGPTLibrary':True,**EXPECTED_DELIVERY,'matchesLocalZIP':True},
 'authorityBefore':bind(INDEX),'countsBefore':{'reviewed':686,'pending':162,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':410},
 'acceptedIds':IDS,'independentCheckGroupsPassed':12,'independentCheckGroupsFailed':0,
 'checks':{'exactOuterZIPAndMemberHashes':True,'exactLiveIndexCatalogQueuePendingAuditAndHandoff':True,'exactSourceCandidateAndConferenceArchive':True,'sourceQuestionDispositionsPreserved':True,'nativeCardsAndClassAccessExact':True,'casebookSixMainTwentySevenBranches':True,'fullStateEventContinuityAndReversibleOperations':True,'exactCaseMirrorFiles':True,'nineHoldsRetained':True,'chainSitesRemainWholeCaseHeld':True,'actorsAreFixtureOnly':True,'nonlivingAndZeroStateHoldsPreserved':True,'noSuppliedHistoricalOrRuntimeProgramsExecuted':True},
 'counts':{'procedures':3,'nativeClassAccessRows':access_rows,'conferenceQuestionDispositions':15,'originalIdentitySourceQuestionDispositions':3,'futureRequirementsPreserved':8,'mainCases':6,'branches':27,'totalCases':33,'events':159,'eventForwardOperations':318,'eventInverseOperations':318,'procedureProposalForwardInverseOperations':sum(len(o['forward'])+len(o['inverse']) for o in procops),'caseProposalForwardInverseOperations':sum(len(o['forward'])+len(o['inverse']) for o in caseops),'validationClaimedPassed':3051,'validationClaimedFailed':0,'holds':len(holds['holds'])},
 'reviewFindings':[
  'The ZIP, internal manifest, all 167 member bindings, CRC, and the exact live authority snapshot pass. The return preserves exact current source candidate and source conference archive bytes.',
  'All three complete native cards and all 14 class-access rows match the live catalog; all 18 dispositions preserve their source questions and make explicit selections.',
  'Six main cases and 27 branches use complete-state event records. All 159 transitions pass independent hash, time-order, continuity, and reversible test/replace replay checks; case-file mirrors match exactly.',
  'The three Chain Gate positive mappings remain local and all eight endpoint-dependent cases retain H-GATE-SITES as whole-case conditional. Symbol payload behavior remains explicit local authorship. Symbol of Death preserves direct-death semantics and missing nonliving/zero-origin source holds.',
  'Actor fixtures are explicitly unauthenticated campaign fixtures. No campaign actors, sites, cosmological mappings, acquisition, runtime, balance, or release claims are promoted.'
 ],
 'retainedHoldCount':9,'rawHoldRegisterPreserved':True,'sourceStatusPreserved':'blocked-pending-operational-review for all three','runtimeSelectionEnabled':False,'sourceProgramsExecuted':False,'historicalProgramsExecuted':False,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,
 'accepted':True,'applied':False
}
(A/'RANK7_GATEGlyph3_RETURN01_INDEPENDENT_AUDIT_141.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(report,ensure_ascii=False,indent=2))