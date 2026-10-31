import copy,hashlib,json,pathlib,zipfile,zlib
ROOT=pathlib.Path.cwd();A=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129';D=A/'rank9_mass_phantom_killer_delta_299';PKG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9massphantomkiller_reviewed_299';ID='mass-phantom-killer';AFTER={'reviewedApplied':821,'pending':27,'acceptedUnapplied':0,'completeStandaloneProcedures':545,'scopedInterfaces':173}
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def bind(p,raw=None):
 p=pathlib.Path(p);b=p.read_bytes() if raw is None else raw
 return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
idxp=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json';catp=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
idxraw=idxp.read_bytes();idx=read(idxp);catraw=catp.read_bytes();cat=read(catp)
backup=A/'authored_review_index.before_mass_phantom_killer_299.json';before=read(backup);app=read(A/'MASS_PHANTOM_KILLER_APPLICATION_299.json');accept=read(A/'MASS_PHANTOM_KILLER_ACCEPTANCE_299.json');decision=read(A/'MASS_PHANTOM_KILLER_DIRECTOR_DECISION_299.json');ops=read(A/'MASS_PHANTOM_KILLER_INDEX_OPERATIONS_299.json');pending=read(A/'CURRENT27_PENDING_IDENTITY_AUDIT_299.json');queue=read(A/'CURRENT_SPELL_QUEUE_299.json');hand=read(A/'CURRENT_HANDOFF_299.json');model=read(PKG/'MODEL.json');proc=read(PKG/'PROCEDURE_RECORD.json');coverage=read(PKG/'CASE_COVERAGE.json');evidence=read(PKG/'EVIDENCE_BINDINGS.json');manifest=read(PKG/'CANDIDATE_PACKAGE_MANIFEST.json')
with zipfile.ZipFile(D/'DD_Rank9_MassPhantomKiller_ReviewDelta_299.zip') as z:
 assert z.testzip() is None
 auth=json.loads(z.read('CURRENT_AUTHORITY_299.json'));replay=json.loads(z.read('FRESH_REPLAY_AUDIT_299.json'));trace=json.loads(z.read('CI-04_ATTACHED_PHASE_DEDUPLICATION_TRACE_299.json'))
 assert sha(backup.read_bytes())==sha(z.read('current/authored_review_index.json'))
 assert sha(catraw)==sha(z.read('current/catalog.json'))
 for x in auth['embeddedExactAuthorityBytes']:
  assert sha(z.read(x['archivePath']))==x['sha256']
  if x['archivePath']=='current/authored_review_index.json':assert sha(backup.read_bytes())==x['sha256']
  else:assert sha(pathlib.Path(x['sourcePath']).read_bytes())==x['sha256']
assert sha(idxraw)==bind(idxp)['sha256'] and idx['authoredCounts']=={'reviewed':821,'pending':27} and idx['representationCounts']['completeReviewedStandaloneProcedures']==545
assert before['authoredCounts']=={'reviewed':820,'pending':28} and len([x for x in before['entries'] if x['authoredStatus']=='pending-authored-procedure'])==28
changed=[x['id'] for x in before['entries'] if x not in idx['entries']];assert changed==[ID]
assert len(idx['additionalStandaloneEnvelopes'])==len(before['additionalStandaloneEnvelopes'])+1
entry=next(x for x in idx['entries'] if x['id']==ID);assert entry['accepted'] and entry['applied'] and entry['sourceStatus']=='blocked-pending-operational-review' and entry['runtimeSelectionEnabled'] is False
pending_ids=sorted(x['id'] for x in idx['entries'] if x.get('authoredStatus')=='pending-authored-procedure');assert pending_ids==pending['pendingIds'] and len(pending_ids)==27 and 'weird' in pending_ids and ID not in pending_ids
assert pending['authority']==queue['currentAuthority']==hand['currentAuthority']==AFTER
assert pending['indexBinding']['sha256']==queue['currentIndexBinding']['sha256']==hand['indexBinding']['sha256']==sha(idxraw)
assert queue['recommendedClosurePriority'][:2]==['weird','final-word'] and queue['next']['pendingIds']==['weird'] and hand['nextPendingIds']==['weird']
assert accept['acceptedIds']==[ID] and accept['appliedIds']==[] and decision['identity']==ID and decision['accepted'] and decision['appliedAtDecision'] is False and decision['noOtherIdentityAcceptedOrApplied']
assert app['acceptedIds']==app['appliedIds']==[ID] and app['closedBlockerIds']==['PF182-B02'] and app['countsBefore']['acceptedUnapplied']==1 and app['countsAfter']==AFTER
assert cat['spells'][576]['id']==ID and cat['spells'][576]['operational'] is None and app['catalogByteExact'] and app['runtimeSelectionEnabled'] is False
assert proc['sourceProcedureBytesPreserved'] and proc['localProcedure']==proc['sourceProcedureRecord']['localProcedure'] and proc['runtimeSelectionEnabled'] is False
assert coverage['historicalCaseCount']==13 and coverage['historicalEventCount']==1183 and coverage['historicalForwardOperations']==2366 and coverage['historicalInverseOperations']==2366
assert replay['mpkCaseCount']==13 and replay['eventCount']==1183 and replay['allInitialStatesRestored'] and trace['assertions']['noDuplicateFamilyExposure'] is True
assert ops['inverseRestoresExactIndex']
assert bind(backup)['sha256']==app['indexBefore']['sha256'] and bind(idxp)['sha256']==ops['after']['sha256']
assert model['runtimeSelectionEnabled'] is False and model['implementationApproved'] is False and model['releaseApproved'] is False
assert sha(catraw)==evidence['currentCatalog']['sha256'] and sha(backup.read_bytes())==evidence['currentIndexSHA256']
checks=['acceptance and archive hashes match Director','only MPK changed in authored index','exact pending set is 27 with Weird still pending','queue/handoff/pending audit agree on 821/27/0 and next Weird','native catalog remains byte-exact and runtime disabled','13 cases / 1,183 events / reversible CI traces remain bound','pre-application index backup restores byte-exact source']
validation={'id':'MASS-PHANTOM-KILLER-APPLICATION-VALIDATION-299','status':'PASS','checks':[{'check':x,'passed':True} for x in checks],'checkCount':len(checks),'failedChecks':0,'acceptedIds':[ID],'appliedIds':[ID],'closedBlockerIds':['PF182-B02'],'authority':AFTER,'index':bind(idxp),'application':bind(A/'MASS_PHANTOM_KILLER_APPLICATION_299.json'),'acceptance':bind(A/'MASS_PHANTOM_KILLER_ACCEPTANCE_299.json'),'pendingIdentityAudit':bind(A/'CURRENT27_PENDING_IDENTITY_AUDIT_299.json'),'queue':bind(A/'CURRENT_SPELL_QUEUE_299.json'),'handoff':bind(A/'CURRENT_HANDOFF_299.json'),'indexOperations':bind(A/'MASS_PHANTOM_KILLER_INDEX_OPERATIONS_299.json'),'candidatePackage':bind(PKG/'MODEL.json'),'candidatePackageManifest':bind(PKG/'CANDIDATE_PACKAGE_MANIFEST.json'),'catalogByteExact':True,'sourceStatusPreservedAsBlocked':True,'runtimeSelectionEnabled':False}
v=A/'MASS_PHANTOM_KILLER_APPLICATION_VALIDATION_299.json';v.write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
snap=A/'CURRENT_SPELL_REVIEW_SNAPSHOT_299.md';snap.write_text('# Spell Review Snapshot — Mass Phantom Killer Application 299\n\nAuthority: **821 applied / 27 pending / 0 accepted-unapplied; 545 complete standalone procedures / 173 scoped interfaces.**\n\nMass Phantom Killer / PF182-B02 was accepted for authored-procedure review under PF297-MPK-EXTERNAL-PROVIDER-REVIEW-REVISION-01 and applied to the authored review index. PF181-H05 remains for actual gameplay. The native catalog remains unchanged, source status remains blocked, and runtime selection is disabled.\n\nNext: **Weird / PF182-B02**, then **Final Word / DR217-B01**. The MPK acceptance does not revise Weird’s obligation or incapacity rules; check current requirements with the Director.\n\nValidation: '+bind(v)['path']+' ('+bind(v)['sha256']+').\n',encoding='utf-8')
print(json.dumps({'status':'PASS','checks':len(checks),'validation':bind(v),'authority':AFTER,'next':['weird','final-word']},indent=2))
