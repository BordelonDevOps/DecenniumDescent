from __future__ import annotations
import copy,hashlib,json,shutil,zipfile,zlib
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
A=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CAT=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
PKG_REL=Path('DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_unravel_reviewed_256')
PKG=ROOT/PKG_REL
MAN=ROOT/'DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_REVIEWED_256.md'
OLD=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_reviewed_196'
OP=OLD/'procedures/unravel-identity.json'; OM=OLD/'CANDIDATE_PACKAGE_MANIFEST.json'
PACK=A/'DD_Rank9_MemoryDenial6_UnravelIdentity_IntegratedWitness_256.zip'
DEL=A/'DD_Rank9_MemoryDenial6_UnravelIdentity_IntegratedWitness_256_DELIVERY.json'
MANIFEST=A/'UNRAVEL_IDENTITY_MD196_B02_SUBMISSION_MANIFEST_256.json'
PLAN=A/'UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256.json'
PA=A/'UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256_AUDIT.json'
REPLAY=A/'UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_256.json'
RA=A/'UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_256_AUDIT.json'
P0=A/'CURRENT36_PENDING_IDENTITY_AUDIT_250.json'; Q0=A/'CURRENT_SPELL_QUEUE_256.json'; H0=A/'CURRENT_HANDOFF_256.json'; Q250=A/'CURRENT_SPELL_QUEUE_250.json'
DEC=A/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_DIRECTOR_DECISION_256.json'
ACC=A/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_EXACT_ACCEPTANCE_256.json'
APP=A/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_APPLICATION_256.json'
OPS=A/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_INDEX_OPERATIONS_256.json'
BAK=A/'authored_review_index.before_unravel_identity_256.json'
P1=A/'CURRENT35_PENDING_IDENTITY_AUDIT_257.json'; Q1=A/'CURRENT_SPELL_QUEUE_257.json'; H1=A/'CURRENT_HANDOFF_257.json'
CORR=A/'CURRENT_REVIEW_STATE_CORRECTION_257.json'; VALID=A/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_APPLICATION_VALIDATION_256.json'
SNAP=A/'CURRENT_SPELL_REVIEW_SNAPSHOT_257.md'
ID='unravel-identity'; REVIEW='RANK9-MEMORYDENIAL6-UNRAVEL-IDENTITY-EXACT-AUTHORED-ACCEPTANCE-256'; APPID='RANK9-MEMORYDENIAL6-UNRAVEL-IDENTITY-APPLICATION-256'
HOLDS=['MD196-H01','MD196-H02','MD196-H03','MD196-H06','MD196-H08']; NEXT='rank9-material-forging2'
URL='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
def sha(b): return hashlib.sha256(b).hexdigest()
def rd(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def wr(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(enc(v))
def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def bind(p,raw=None):
 b=p.read_bytes() if raw is None else raw
 return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
OUT=[PKG,MAN,DEC,ACC,APP,OPS,BAK,P1,Q1,H1,CORR,VALID,SNAP]
assert all(not x.exists() for x in OUT),'Refuse to overwrite an existing application artifact'
delivery=rd(DEL); manifest=rd(MANIFEST); archive_hash=sha(PACK.read_bytes())
assert archive_hash==delivery['archive']['sha256']=='34d4224b4b7717193bc8ac352d128fcba517485de96b3c3c20ad6263f165f75d'
assert PACK.stat().st_size==delivery['archive']['bytes']==113352 and delivery['acceptanceRequested'] and not delivery['applicationRequested']
assert rd(PA)['status']=='PASS_WITH_DIRECTOR_RULINGS_PENDING' and rd(PA)['checksPassed']==rd(PA)['checkCount']==139
assert rd(RA)['status']=='PASS_WITH_DIRECTOR_RULINGS_PENDING' and rd(RA)['checksPassed']==rd(RA)['checkCount']==164
with zipfile.ZipFile(PACK) as z:
 assert z.testzip() is None and len(z.namelist())==11 and z.namelist()[-1]=='MANIFEST.json'
 assert json.loads(z.read('MANIFEST.json'))==manifest
 for m in manifest['members']:
  b=z.read(m['archivePath']); assert len(b)==m['bytes'] and sha(b)==m['sha256'] and f'{zlib.crc32(b)&0xffffffff:08x}'==m['crc32']
oldraw=OP.read_bytes(); old=rd(OP); om=rd(OM)
m=next(x for x in om['files'] if x['path'].endswith('procedures/unravel-identity.json'))
assert m['bytes']==len(oldraw) and m['sha256']==sha(oldraw)
assert old['id']==ID and old['accepted'] is False and old['applied'] is False and old['blockerIds']==['MD196-B02']
idxraw,catraw=INDEX.read_bytes(),CAT.read_bytes(); before,cat=rd(INDEX),rd(CAT)
p0,q0,h0,qbase=map(rd,(P0,Q0,H0,Q250))
entry=next(x for x in before['entries'] if x['id']==ID)
pending0={x['id'] for x in before['entries'] if x['authoredStatus']=='pending-authored-procedure'}
assert before['authoredCounts']=={'reviewed':812,'pending':36} and before['representationCounts']['completeReviewedStandaloneProcedures']==536
assert set(p0['pendingIds'])==pending0 and len(pending0)==36 and p0['indexBinding']['sha256']==sha(idxraw)
assert q0['currentIndexBinding']['sha256']==sha(idxraw) and q0['currentAuthority']=={'reviewedApplied':812,'pending':36,'acceptedUnapplied':0,'completeStandaloneProcedures':536,'scopedInterfaces':173}
assert entry['authoredStatus']=='pending-authored-procedure' and entry['sourceStatus']=='blocked-pending-operational-review'
assert ID in {x['id'] for x in cat['spells']}
assert {'mind-collapse',ID}<=set(next(g for g in qbase['currentPendingGroups'] if g['group']=='rank9-memory-denial6')['pendingIds'])
old_holds=[x for x in old['holdIds'] if x!='MD196-B02']; assert old_holds==HOLDS
caseidx=rd(OLD/'CASE_INDEX.json'); cases=[copy.deepcopy(x) for x in caseidx['cases'] if x.get('spellId')==ID]; assert len(cases)==14

response='''ACCEPT — unravel-identity: accepted=true, applied=false. MD196-B02 is closed.
Acceptance covers the preserved Unravel Identity procedure and Packet256’s integrated witness, including the explicitly spell-local form-loss and capability callbacks. It does not establish global class-suppression rules.
Packet256: 113,352 bytes; SHA-256 34d4224b4b7717193bc8ac352d128fcba517485de96b3c3c20ad6263f165f75d. Exact 11-member allowlist and payload hashes/CRCs pass. All 45 reversible transitions and 34 continuity links pass. Audits: 139/139 and 164/164.
T5 END :30 vents Dissonance without restoring capabilities; familiar command is unavailable at :30.1; natural recovery occurs at T6 END :36. Arch Dispel terminates the target at :28 while preserving the scheduled :36 deadline. Helper Actions, ordinary detect-magic and recharge 2→1→0 are preserved.
Nonblocking annotation erratum: /branchTurnLedgers/ARCH-DISPEL-REMOVAL/4/marker says Dissonance0→0; linked OP256-22-ARCH-DISPEL-T5-END correctly records 1→0. That transition is accepted.
Mind Blank remains conditional. MD196-H01/H02/H03/H06/H08 remain applicable. Runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates remain closed.
Canonical counts were 812 applied / 36 pending / 0 accepted-unapplied; this authorizes one acceptance awaiting application, with 35 other identities held. Expected after application: 813 / 35 / 0, 537 procedures / 173 interfaces.
Next priority: matter-conversion — rank9-material-forging2, blocker MF210-B02. Eternal Forge remains closed.'''
decision={'id':'RANK9-MEMORYDENIAL6-UNRAVEL-IDENTITY-GPT-DIRECTOR-DECISION-256','recordedAtUtc':now(),'decision':'EXACT_ACCEPT','identity':ID,'blockerClosed':'MD196-B02','accepted':True,'appliedAtDecision':False,'authorityAtDecision':{'reviewedApplied':812,'pending':36,'acceptedUnapplied':0,'completeStandaloneProcedures':536,'scopedInterfaces':173},'authorityAfterApplicationExpected':{'reviewedApplied':813,'pending':35,'acceptedUnapplied':0,'completeStandaloneProcedures':537,'scopedInterfaces':173},'source':{'service':'ChatGPT','conversationTitle':'Calibration review part 6','url':URL},'exactResponse':response,'packet':bind(PACK),'delivery':bind(DEL),'manifest':bind(MANIFEST),'witnessAudit':bind(PA),'replayAudit':bind(RA),'retainedQualifications':HOLDS,'nonblockingAnnotationErratum':{'pointer':'/branchTurnLedgers/ARCH-DISPEL-REMOVAL/4/marker','marker':'Dissonance0→0','linkedTransition':'OP256-22-ARCH-DISPEL-T5-END','acceptedResult':'1→0'},'nextPriority':{'identity':'matter-conversion','group':NEXT,'blocker':'MF210-B02','note':'Eternal Forge remains closed.'},'scope':'Static authored procedure only; no global class-suppression rule or downstream gate approval.'}
wr(DEC,decision); decbind=bind(DEC)
proc=copy.deepcopy(old); proc.update({'accepted':True,'applied':False,'status':'DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED','blockerIds':[],'closedBlockerIds':['MD196-B02'],'holdIds':HOLDS,'historicalQualificationsFromReturn196':copy.deepcopy(old['qualifications']),'qualifications':['Static authored procedure accepted and applied to authored review index only; runtime disabled.','MD196-H01, H02, H03, H06 and H08 remain applicable qualifications.','Mind Blank remains conditional; no successful suppression interval is accepted.','The tested form-loss and capability callback is spell-local; no global class-suppression rule is established.','No implementation, play, balance, cosmology, domain closure, completion or release approval is implied.'],'currentIndexEntryBeforeApplication':copy.deepcopy(entry),'directorDecisionBinding':decbind,'packet256Binding':bind(PACK),'witnessPlanBinding':bind(PLAN),'witnessAuditBinding':bind(PA),'integratedReplayBinding':bind(REPLAY),'replayAuditBinding':bind(RA),'priorProcedureRecordBinding':bind(OP),'priorCandidatePackageManifestBinding':bind(OM)})
coverage={'id':'MD196-UNRAVEL-CASE-COVERAGE-256','sourceCaseIndex':bind(OLD/'CASE_INDEX.json'),'sourceCasebook':bind(OLD/'CASEBOOK.json.gz'),'acceptedCaseCount':len(cases),'acceptedCaseIds':[x['id'] for x in cases],'acceptedSourceCaseIndexRows':cases,'witness':bind(PLAN),'replay':bind(REPLAY),'transitionCount':len(rd(REPLAY)['forwardInverseTransitions']),'wholeBranchContinuityLinks':34}
evidence={'id':'MD196-UNRAVEL-ACCEPTED-EVIDENCE-256','directorDecision':decbind,'packet':bind(PACK),'delivery':bind(DEL),'manifest':bind(MANIFEST),'plan':bind(PLAN),'planAudit':bind(PA),'replay':bind(REPLAY),'replayAudit':bind(RA),'supplementalFormSource':bind(ROOT/'DescentReviewChanges/ReviewBible/data/playtest/druid_form_profiles.json'),'priorProcedure':bind(OP),'priorPackageManifest':bind(OM),'priorCaseIndex':bind(OLD/'CASE_INDEX.json'),'priorCasebook':bind(OLD/'CASEBOOK.json.gz'),'retainedQualifications':HOLDS,'nonblockingErratum':decision['nonblockingAnnotationErratum']}
PKG.mkdir()
wr(PKG/'DIRECTOR_DECISION.json',decision); wr(PKG/'PROCEDURE_RECORD.json',proc); wr(PKG/'CASE_COVERAGE.json',coverage); wr(PKG/'EVIDENCE_BINDINGS.json',evidence)
wr(PKG/'RETAINED_QUALIFICATIONS.json',{'identity':ID,'ids':HOLDS,'mindBlankConditional':True,'globalClassSuppressionRuleEstablished':False})
model={'schemaVersion':1,'moduleId':'rank9memorydenial6-unravel-reviewed-256','status':'ONE_EXACT_STATIC_AUTHORED_PROCEDURE_APPLIED_WITH_FIVE_RETAINED_QUALIFICATIONS','scope':'Unravel Identity only; the preserved procedure is accepted with Packet256 witness/replay. Tested form-loss and capability callbacks are spell-local; no global class-suppression rule or catalog/class change.','acceptedIds':[ID],'unacceptedIds':[],'excludedPendingIds':sorted(pending0-{ID}),'unresolvedQualifications':{ID:HOLDS},'sharedRequirements':{'scope':'No global/shared rule changes; native card, catalog and class route unchanged.','runtimeSelectionEnabled':False},'spells':[{'id':ID,'name':entry['name'],'position':0,'procedure':{'id':'MD196-STATIC-UNRAVEL_IDENTITY','spellId':ID,'status':'director-accepted static authored procedure; applied to authored review index; runtime disabled','accepted':True,'applied':False,'nativeCardUnchanged':copy.deepcopy(old['completeSourceAndAccess']),'procedureContent':old['procedure'],'sharedRequirements':old['commonProcedure'],'spellLocalRequirements':copy.deepcopy(old['newChoices']),'qualifications':proc['qualifications'],'retainedQualificationIds':HOLDS,'closedBlockerIds':['MD196-B02'],'questionIds':copy.deepcopy(old['questionIds']),'caseIds':[x['id'] for x in cases],'directorDecisionId':decision['id'],'directorDecisionBinding':decbind,'evidenceBindingsFile':'EVIDENCE_BINDINGS.json','caseCoverageFile':'CASE_COVERAGE.json'},'directorProcedureRecord':proc,'nativeCardUnchanged':copy.deepcopy(old['completeSourceAndAccess']),'caseIds':[x['id'] for x in cases],'questionIds':copy.deepcopy(old['questionIds']),'holdIds':HOLDS,'runtimeSelectionEnabled':False}],'caseCoverage':{'caseCount':len(cases),'caseIds':[x['id'] for x in cases],'file':'CASE_COVERAGE.json'},'evidenceBindings':bind(PKG/'EVIDENCE_BINDINGS.json'),'directorDecision':decbind,'sourcePacket':bind(PACK),'witnessPlan':bind(PLAN),'integratedReplay':bind(REPLAY),'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'implementationApproved':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,'domainClosure':False}
wr(PKG/'MODEL.json',model)
text='# Unravel Identity — accepted static authored procedure 256\n\nAccepted under GPT director decision MD196-B02. This applies only to Unravel Identity and establishes no global class-suppression rule. Runtime, implementation, play, balance, cosmology, domain closure, completion and release gates remain closed.\n\n## Native card and access\n\n'+json.dumps(old['completeSourceAndAccess'],ensure_ascii=False,indent=2)+'\n\n## Shared procedure\n\n'+old['commonProcedure']+'\n\n## Unravel Identity procedure\n\n'+old['procedure']+'\n\n## Retained qualifications\n\n'+'\n'.join('- '+h for h in HOLDS)+'\n\nMind Blank remains conditional. The nonblocking marker erratum is preserved; the linked transition records Dissonance 1→0.\n'
(PKG/'STANDALONE_PROCEDURES.md').write_text(text,encoding='utf-8',newline='\n'); MAN.parent.mkdir(parents=True,exist_ok=True); MAN.write_bytes((PKG/'STANDALONE_PROCEDURES.md').read_bytes())
pm={'id':'RANK9-MEMORYDENIAL6-UNRAVEL-PACKAGE-MANIFEST-256','sourcePacket':bind(PACK),'directorDecision':decbind,'files':[]}
for f in sorted(x for x in PKG.rglob('*') if x.is_file() and x.name!='CANDIDATE_PACKAGE_MANIFEST.json'):
 b=f.read_bytes();pm['files'].append({'path':(PKG_REL/f.relative_to(PKG)).as_posix(),'bytes':len(b),'sha256':sha(b)})
wr(PKG/'CANDIDATE_PACKAGE_MANIFEST.json',pm)


modelbind=bind(PKG/'MODEL.json'); packagebind=bind(PKG/'CANDIDATE_PACKAGE_MANIFEST.json'); evidencebind=bind(PKG/'EVIDENCE_BINDINGS.json'); coveragebind=bind(PKG/'CASE_COVERAGE.json')
wr(ACC,{'id':REVIEW,'recordedAtUtc':now(),'status':'ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED','acceptedIds':[ID],'appliedIds':[],'closedBlockerIds':['MD196-B02'],'retainedQualificationIds':HOLDS,'directorDecision':decbind,'packet':bind(PACK),'delivery':bind(DEL),'audits':[bind(PA),bind(RA)],'candidateEnvelope':modelbind,'candidatePackageManifest':packagebind,'countsBefore':{'reviewed':812,'pending':36,'acceptedUnapplied':0},'countsAfterAcceptanceBeforeApplication':{'reviewed':812,'pending':35,'acceptedUnapplied':1},'scope':'Static Unravel Identity procedure only; runtime and shared rules unchanged.'})
accbind=bind(ACC)
receipt=A/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_RETURN256_RECEIPT.json'
wr(receipt,{'id':'RANK9-MEMORYDENIAL6-UNRAVEL-IDENTITY-RETURN256-RECEIPT','recordedAtUtc':now(),'status':'EXACT_ACCEPT_UNRAVEL_IDENTITY','acceptedIds':[ID],'appliedIds':[],'closedBlockerIds':['MD196-B02'],'retainedQualificationIds':HOLDS,'directorDecision':decbind,'acceptance':accbind,'packet':bind(PACK),'delivery':bind(DEL),'audits':[bind(PA),bind(RA)],'nextPriority':decision['nextPriority']})
recbind=bind(receipt)
shutil.copyfile(INDEX,BAK); assert BAK.read_bytes()==idxraw
pos=next(i for i,x in enumerate(before['entries']) if x['id']==ID)
after=copy.deepcopy(before)
new=copy.deepcopy(entry)
new.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/rank9memorydenial6_unravel_reviewed_256/MODEL.json','procedurePointer':'/spells/0/procedure','wholeCardPointer':'/spells/0','wholeCardIdField':'id','sourceCatalogWholeCardPointer':entry.get('sourceCatalogWholeCardPointer') or entry['wholeCardPointer'],'procedureTextPointer':'/spells/0/procedure/procedureContent','directorProcedureRecordPointer':'/spells/0/directorProcedureRecord','sharedRulesPointer':'/spells/0/procedure/sharedRequirements','spellLocalRequirementsPointer':'/spells/0/procedure/spellLocalRequirements','manuscript':'../../../docs/spells/candidates/RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_REVIEWED_256.md','reviewId':APPID,'runtimeSelectionEnabled':False,'historicalCandidateLabelsPreserved':True,'completeEvidenceRoot':PKG_REL.as_posix(),'completeEnvelopeBinding':modelbind,'caseEvidenceBindings':coveragebind,'sourceArchiveBinding':bind(PACK),'deliveryManifestBinding':bind(DEL),'candidatePackageManifestBinding':packagebind,'procedureSourceBinding':decbind,'authoredAcceptanceReceipt':accbind,'authoredApplicationReceipt':{'path':APP.relative_to(ROOT).as_posix()},'accepted':True,'applied':True,'closedBlockerIds':['MD196-B02'],'retainedQualificationIds':HOLDS})
assert new['sourceStatus']==entry['sourceStatus']=='blocked-pending-operational-review'
after['entries'][pos]=new
after['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/rank9memorydenial6_unravel_reviewed_256/MODEL.json','binding':modelbind,'reviewId':REVIEW,'acceptedIds':[ID],'unacceptedIds':[],'excludedPendingIds':sorted(pending0-{ID}),'authority':accbind,'applicationReceipt':APP.relative_to(ROOT).as_posix(),'directorDecision':decbind,'sourcePacket':bind(PACK),'deliveryManifest':bind(DEL),'evidenceBindings':evidencebind,'candidatePackageManifestBinding':packagebind,'scope':'ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED'})
after['authoredCounts']={'reviewed':813,'pending':35}; after['representationCounts']['completeReviewedStandaloneProcedures']=537
pending1={x['id'] for x in after['entries'] if x['authoredStatus']=='pending-authored-procedure'}
assert pending1==pending0-{ID} and len(pending1)==35
inverse=copy.deepcopy(after); inverse['entries'][pos]=copy.deepcopy(entry); inverse['additionalStandaloneEnvelopes']=inverse['additionalStandaloneEnvelopes'][:-1]; inverse['authoredCounts']=copy.deepcopy(before['authoredCounts']); inverse['representationCounts']=copy.deepcopy(before['representationCounts'])
assert inverse==before
wr(APP,{'id':APPID,'recordedAtUtc':now(),'status':'APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE','acceptedIds':[ID],'appliedIds':[ID],'closedBlockerIds':['MD196-B02'],'retainedQualificationIds':HOLDS,'ownerInstruction':'Apply each exact director-accepted ordinary spell identity and continue to the next GPT-directed pending review.','directorAcceptance':accbind,'directorDecision':decbind,'directorReturnReceipt':recbind,'packet':bind(PACK),'delivery':bind(DEL),'audits':[bind(PA),bind(RA)],'candidateEnvelope':modelbind,'candidatePackageManifest':packagebind,'evidenceBindings':evidencebind,'caseCoverage':coveragebind,'manuscript':bind(MAN),'indexBefore':bind(BAK,idxraw),'countsBefore':{'reviewed':812,'pending':36,'acceptedUnapplied':0},'countsAfter':{'reviewed':813,'pending':35,'acceptedUnapplied':0},'completeReviewedStandaloneProcedures':{'before':536,'after':537},'scopedInterfaces':173,'catalogChanged':False,'classAccessChanged':False,'sourceStatusPreservedAsBlocked':True,'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'independentValidationPath':VALID.relative_to(ROOT).as_posix()})
appbind=bind(APP); new['authoredApplicationReceipt']=appbind; after['entries'][pos]=new
inverse=copy.deepcopy(after); inverse['entries'][pos]=copy.deepcopy(entry); inverse['additionalStandaloneEnvelopes']=inverse['additionalStandaloneEnvelopes'][:-1]; inverse['authoredCounts']=copy.deepcopy(before['authoredCounts']); inverse['representationCounts']=copy.deepcopy(before['representationCounts']); assert inverse==before
afterraw=enc(after); tmp=INDEX.with_name('authored_review_index.unravel256.tmp'); tmp.write_bytes(afterraw); tmp.replace(INDEX); assert CAT.read_bytes()==catraw
wr(OPS,{'id':'RANK9-MEMORYDENIAL6-UNRAVEL-INDEX-OPERATIONS-256','before':bind(BAK,idxraw),'after':bind(INDEX,afterraw),'operations':[{'op':'replace-entry','identity':ID,'index':pos,'before':entry,'after':new},{'op':'append-envelope','identity':ID,'envelope':after['additionalStandaloneEnvelopes'][-1]},{'op':'update-counts','before':before['authoredCounts'],'after':after['authoredCounts'],'standaloneProcedures':{'before':536,'after':537}}],'onlyIdentityIds':[ID],'inverseSemanticExact':True,'catalogByteExact':True})


authority={'reviewedApplied':813,'pending':35,'acceptedUnapplied':0,'completeStandaloneProcedures':537,'scopedInterfaces':173}
groups=copy.deepcopy(qbase['currentPendingGroups'])
for g in groups:
 remain=[sid for sid in g['pendingIds'] if sid in pending1]
 g['pendingIds']=remain; g['pendingCount']=len(remain)
 if g['group']=='rank9-memory-denial6':
  g['status']='UNRAVEL_ACCEPTED_APPLIED_MIND_COLLAPSE_REMAINS_PENDING'
  g['currentDisposition']={'acceptedAppliedIds':[ID],'remainingPendingIds':remain,'closedBlockerIds':['MD196-B02']}
  g['freshPacketRequiredForCurrentAuthority']=True
 if g['group']==NEXT:
  g['status']='GPT_DIRECTED_NEXT_PRIORITY_FRESH_PACKET_REQUIRED_AT_813_35'
  g['freshPacketRequiredForCurrentAuthority']=True; g['sourceAuthority']=authority
assert set(s for g in groups for s in g['pendingIds'])==pending1
nextg=next(g for g in groups if g['group']==NEXT)
nextrec={'group':NEXT,'pendingIds':['matter-conversion'],'pendingCount':1,'blocker':'MF210-B02','status':'GPT_DIRECTED_FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED','freshPacketRequiredForCurrentAuthority':True,'candidate':nextg.get('candidate'),'archive':nextg.get('archive'),'nextAction':'Prepare Matter Conversion at authority 813/35/0, review MF210-B02 with GPT as director, and keep Eternal Forge closed.'}
p1=copy.deepcopy(p0); p1.update({'id':'CURRENT35-PENDING-IDENTITY-AUDIT-257','recordedAtUtc':now(),'status':'PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_UNRAVEL_IDENTITY_APPLICATION','authority':authority,'indexBinding':bind(INDEX,afterraw),'catalogBinding':bind(CAT,catraw),'pendingCount':35,'pendingIds':sorted(pending1),'acceptedIds':['eternal-forge',ID],'appliedIds':['eternal-forge',ID],'heldIds':sorted(pending1),'allPendingIdsExistInNativeCatalog':pending1<={x['id'] for x in cat['spells']},'noPendingTargetWasSilentlyAccepted':True,'allCurrentPendingIdentitiesReviewed':True,'unreviewedPendingIds':[],'closed335AndCompletedCohortsReopened':False,'applicationReceipt':appbind,'directorDecision':decbind,'nextBlockerPriority':{'identity':'matter-conversion','group':NEXT,'blockerId':'MF210-B02'},'groups':groups})
wr(P1,p1); p1bind=bind(P1)
q1=copy.deepcopy(q0); q1.update({'id':'CURRENT-SPELL-QUEUE-257','recordedAtUtc':now(),'supersedesQueue':'CURRENT_SPELL_QUEUE_256.json','currentAuthority':authority,'currentIndexBinding':bind(INDEX,afterraw),'currentCatalogBinding':bind(CAT,catraw),'currentPendingGroups':groups,'nextSuggestedGroups':[copy.deepcopy(nextg)],'nextGroup':NEXT,'next':nextrec,'nextPreparedRequest':nextrec,'pendingCount':35,'pendingIdentityAudit':{'path':P1.relative_to(ROOT).as_posix(),'bytes':P1.stat().st_size,'sha256':sha(P1.read_bytes())},'parentQueue':bind(Q0),'lastReviewedBatch':{'group':'rank9-memory-denial6','acceptedIds':[ID],'appliedIds':[ID],'heldIds':['mind-collapse'],'blockerIdsClosed':['MD196-B02']},'justAppliedBatch':{'reviewId':REVIEW,'applicationId':APPID,'ids':[ID],'count':1,'applicationReceipt':APP.relative_to(ROOT).as_posix(),'directorDecision':DEC.relative_to(ROOT).as_posix()},'packetStatus':'UNRAVEL_ACCEPTED_APPLIED_813_35_NEXT_MATTER_CONVERSION_MF210_B02','status':'UNRAVEL_ACCEPTED_APPLIED_NEXT_GPT_DIRECTED_MATTER_CONVERSION_813_35','recommendedClosurePriority':['matter-conversion'],'githubChanges':False,'currentAcceptedPacket':{'archive':bind(PACK),'delivery':bind(DEL),'decision':decbind,'application':appbind},'activeReview':{'identity':'matter-conversion','group':NEXT,'blocker':'MF210-B02','stage':'FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED'}})
wr(Q1,q1); q1bind=bind(Q1)
h1=copy.deepcopy(h0); h1.update({'id':'CURRENT-HANDOFF-257','recordedAtUtc':now(),'status':'UNRAVEL_ACCEPTED_APPLIED_NEXT_MATTER_CONVERSION_813_35','currentAuthority':authority,'currentIndexBinding':bind(INDEX,afterraw),'currentQueueBinding':q1bind,'currentQueue':Q1.relative_to(ROOT).as_posix(),'currentPendingIdentityAudit':P1.relative_to(ROOT).as_posix(),'appliedThisStep':{'identity':ID,'application':APP.relative_to(ROOT).as_posix(),'acceptance':ACC.relative_to(ROOT).as_posix()},'acceptedThisStep':[ID],'retainedQualificationIds':HOLDS,'nextStep':nextrec['nextAction'],'nextGroup':NEXT,'nextPendingCount':1,'nextPendingIds':['matter-conversion'],'currentBlocker':{'identity':'matter-conversion','group':NEXT,'blockerId':'MF210-B02'},'directorConnectionStatus':'GPT accepted and authorized Unravel Identity application; next priority Matter Conversion / MF210-B02; Eternal Forge remains closed.','githubChanges':False,'runtimeSelectionEnabled':False})
wr(H1,h1); h1bind=bind(H1)
wr(CORR,{'id':'CURRENT-REVIEW-STATE-CORRECTION-257','recordedAtUtc':now(),'status':'PASS_CURRENT_AUTHORITY_UPDATED_AFTER_EXPLICIT_GPT_ACCEPTANCE_AND_APPLICATION','supersedes':'CURRENT_REVIEW_STATE_CORRECTION_256.json','oldRecordsPreservedByteForByte':True,'acceptedIdentity':ID,'closedBlockerIds':['MD196-B02'],'directorDecision':decbind,'acceptance':accbind,'application':appbind,'indexOperations':bind(OPS),'authorityAfter':authority,'pendingAudit':p1bind,'queue':q1bind,'handoff':h1bind,'nextPriority':nextrec,'scope':'One static authored procedure only; no runtime/global rule change.'})
corrbind=bind(CORR)
# Freshly inspect canonical index, pending set, group coverage, and packet links.
afterread=rd(INDEX); newentry=next(x for x in afterread['entries'] if x['id']==ID)
checks=[
 ('packet SHA and size',bind(PACK)['sha256']==delivery['archive']['sha256'] and bind(PACK)['bytes']==delivery['archive']['bytes']),
 ('packet ZIP/member CRC and SHA checks',True),
 ('witness audit 139/139',rd(PA)['checksPassed']==rd(PA)['checkCount']==139),
 ('replay audit 164/164',rd(RA)['checksPassed']==rd(RA)['checkCount']==164),
 ('one accepted identity',newentry['id']==ID and newentry['accepted'] and newentry['applied']),
 ('authored index counts',afterread['authoredCounts']=={'reviewed':813,'pending':35}),
 ('standalone procedure count',afterread['representationCounts']['completeReviewedStandaloneProcedures']==537),
 ('pending set exact',pending1=={x['id'] for x in afterread['entries'] if x['authoredStatus']=='pending-authored-procedure'}),
 ('35 pending identities',len(pending1)==35),
 ('only Unravel left pending status',ID not in pending1),
 ('source status preserved',newentry['sourceStatus']=='blocked-pending-operational-review'),
 ('catalog byte exact',CAT.read_bytes()==catraw),
 ('index inverse exact',inverse==before),
 ('backup byte exact',BAK.read_bytes()==idxraw),
 ('all group members cover pending set',set(s for g in groups for s in g['pendingIds'])==pending1),
 ('next priority MF210-B02',q1['next']['blocker']=='MF210-B02' and q1['nextGroup']==NEXT),
 ('queue authority',q1['currentAuthority']==authority),
 ('handoff authority',h1['currentAuthority']==authority),
 ('five retained qualifications',newentry['retainedQualificationIds']==HOLDS),
 ('global suppression rule not accepted',model['sharedRequirements']['scope'].startswith('No global/shared')),
 ('manifest binds all package files',all((ROOT/x['path']).read_bytes() and len((ROOT/x['path']).read_bytes())==x['bytes'] and sha((ROOT/x['path']).read_bytes())==x['sha256'] for x in pm['files'])),
]
assert all(v for _,v in checks),[name for name,v in checks if not v]
wr(VALID,{'id':'RANK9-MEMORYDENIAL6-UNRAVEL-APPLICATION-VALIDATION-256','recordedAtUtc':now(),'status':'PASS','checksPassed':len(checks),'checkCount':len(checks),'checksFailed':0,'checks':[{'check':n,'passed':v} for n,v in checks],'acceptedIds':[ID],'appliedIds':[ID],'closedBlockerIds':['MD196-B02'],'retainedQualificationIds':HOLDS,'beforeIndex':bind(BAK,idxraw),'afterIndex':bind(INDEX,afterraw),'catalogByteExact':True,'sourceStatusPreservedAsBlocked':True,'runtimeSelectionEnabled':False,'witnessAudit':bind(PA),'replayAudit':bind(RA),'decision':decbind,'acceptance':accbind,'application':appbind,'pendingAudit':p1bind,'queue':q1bind,'handoff':h1bind,'correction':corrbind,'inverseSemanticExact':inverse==before,'nextPriority':nextrec})
(SNAP).write_text('# Current spell review snapshot 257\n\nAuthority: **813 applied / 35 pending / 0 accepted-unapplied; 537 complete standalone procedures / 173 scoped interfaces.**\n\nUnravel Identity / MD196-B02 was explicitly accepted by GPT and applied to the authored review index. MD196-H01/H02/H03/H06/H08 remain applicable qualifications; Mind Blank remains conditional. The nonblocking marker erratum and accepted transition result are preserved in the application evidence.\n\nNext GPT-directed priority: **Matter Conversion / MF210-B02**. Eternal Forge remains closed. Runtime and downstream approval gates remain closed.\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':'PASS','identity':ID,'applied':True,'counts':authority,'checks':len(checks),'next':nextrec,'validation':bind(VALID),'index':bind(INDEX)},indent=2))


