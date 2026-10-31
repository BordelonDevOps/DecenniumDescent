from __future__ import annotations
import copy, datetime, hashlib, json, pathlib, shutil, zlib
ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
D = A / 'rank9_ag190_b01_closure_delta_292'
BASE = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
PKG_REL = pathlib.Path('DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_absolutedomination_reviewed_292')
PKG = ROOT / PKG_REL
MANUSCRIPT = ROOT / 'DescentReviewChanges/ReviewBible/docs/spells/candidates/ABSOLUTE_DOMINATION_REVIEWED_292.md'
ID, NAME, BLOCKER = 'absolute-domination', 'Absolute Domination', 'AG190-B01'
NEXT, NEXT_BLOCKER, NEXT_GROUP = 'puppetmaster-s-realm', 'AG190-B02', 'rank9-agency-control9'
BEFORE = {'reviewedApplied':817,'pending':31,'acceptedUnapplied':0,'completeStandaloneProcedures':541,'scopedInterfaces':173}
AFTER = {'reviewedApplied':818,'pending':30,'acceptedUnapplied':0,'completeStandaloneProcedures':542,'scopedInterfaces':173}
URL = 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
DIRECTOR_TEXT = ('ACCEPT - absolute-domination / AG190-B01 only. accepted=true, applied=false. AG190-B01 is closed. '
'Verified Packet292 SHA-256 a966ca1366180ec0f21dc7cd791cf23f279a4e6c465632662ed125f349efb925. '
'The concentration correction passes. Both branches independently replay with 2 events, 11 forward operations and 11 inverse operations. '
'Member bindings and CRCs pass; the failure branch is byte-identical. No residual defect remains. '
'Acceptance covers the preserved procedure and corrected tests under AG291-OBLIGATION-REVISION-01. Retain AG190-H-SOURCE and all other AG190 qualifications. '
'This does not establish an actual extra-turn provider or close another spell. Now 817 applied, 1 accepted-unapplied, 30 other identities held. '
'Canonical index remains 817/31 until application. After application 818 applied / 30 pending / 0 accepted-unapplied, 542 procedures / 173 interfaces. '
'Next puppetmaster-s-realm / AG190-B02. No canonical changes, application, or downstream approval occurred in this review.')
QUALS = [
'Acceptance is limited to the preserved Absolute Domination procedure, corrected conditional inserted-turn END-save tests, and AG291-OBLIGATION-REVISION-01.',
'The conditional tests establish no actual inserted-turn provider, grant, acquisition, activation, eligible recipient, or gameplay history.',
'Actual gameplay using an inserted full turn still requires its separately authorized source, lawful acquisition, activation, and eligible recipient under AG190-H-SOURCE.',
'The native WIS save at END of every actual affected target turn remains unchanged; an inserted turn creates no command opportunity, regular budget, recharge, Reaction refresh, Ready change, or regular-clock tick.',
'AG190-H-SOURCE, AG190-H-PHYSICAL, AG190-H-CONTENT, AG190-H-LIFECYCLE, AG190-H-RUNTIME, AG190-H-PLAY, AG190-H-BALANCE, AG190-H-COSMOLOGY, AG190-H-DOMAIN, and AG190-H-RELEASE remain retained.',
'AG190-B02 remains open for Puppetmaster\'s Realm. Native catalog is byte-exact and runtime selection remains disabled; implementation, human-play, balance, cosmology, domain-closure, and release gates remain closed.'
]
def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def read(p: pathlib.Path): return json.loads(p.read_text(encoding='utf-8-sig'))
def encode(v) -> bytes: return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(p: pathlib.Path,v) -> None: p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(encode(v))
def bind(p: pathlib.Path,raw: bytes|None=None):
 b=p.read_bytes() if raw is None else raw
 return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
def find_id(o,want):
 if isinstance(o,dict):
  r=[o] if o.get('id')==want else []
  for v in o.values(): r+=find_id(v,want)
  return r
 if isinstance(o,list): return sum((find_id(v,want) for v in o),[])
 return []
def clean_groups(groups):
 out=[]
 for old in groups:
  row=copy.deepcopy(old)
  for k in ('pendingIds','identities','spellIds'):
   if k in row and isinstance(row[k],list): row[k]=[x for x in row[k] if x!=ID]
  key=next((k for k in ('pendingIds','identities','spellIds') if k in row),None)
  if key and not row[key]: continue
  if 'pendingCount' in row and key: row['pendingCount']=len(row[key])
  out.append(row)
 return out

def main():
 assert not PKG.exists() and not MANUSCRIPT.exists(), 'Refusing to overwrite application outputs.'
 delta_path=D/'AG190_B01_CLOSURE_DELTA_292.json'; audit_path=D/'AG190_B01_CLOSURE_DELTA_INDEPENDENT_AUDIT_292.json'
 delta_raw=delta_path.read_bytes(); audit_raw=audit_path.read_bytes(); delta=read(delta_path); audit=read(audit_path)
 assert sha((D/'DD_Rank9_AgencyControl9_AbsoluteDomination_ClosureDelta_292.zip').read_bytes())=='a966ca1366180ec0f21dc7cd791cf23f279a4e6c465632662ed125f349efb925'
 assert audit['status']=='PASS' and audit['passedChecks']==23 and not audit['failedChecks']
 assert delta['directorRuling']['selectedObligationRevision']['id']=='AG291-OBLIGATION-REVISION-01'
 source_path=BASE/'procedures/absolute-domination.json'; source_raw=source_path.read_bytes(); source=read(source_path)
 proc=copy.deepcopy(source['procedure'])
 old='A genuine inserted-turn positive case stays held unless the complete granting source and legal acquisition actually exist.'
 new='Under AG291-OBLIGATION-REVISION-01, the two conditional inserted-turn END-save tests satisfy the external-provider review obligation for authored-procedure acceptance only. Actual gameplay using an inserted full turn still requires its separately authorized source, lawful acquisition, activation, eligible recipient, and actual actor history under AG190-H-SOURCE.'
 assert old in proc['saves']; proc['saves']=proc['saves'].replace(old,new)
 retained=[x for x in source['holdIds'] if x!=BLOCKER]; assert 'AG190-H-SOURCE' in retained
 index_raw=INDEX.read_bytes(); catalog_raw=CATALOG.read_bytes(); index0=read(INDEX); catalog0=read(CATALOG)
 p0=read(A/'CURRENT31_PENDING_IDENTITY_AUDIT_291.json'); q0=read(A/'CURRENT_SPELL_QUEUE_291.json'); h0=read(A/'CURRENT_HANDOFF_291.json')
 assert sha(index_raw)==p0['indexBinding']['sha256']==q0['currentIndexBinding']['sha256']
 assert index0['authoredCounts']=={'reviewed':817,'pending':31} and index0['representationCounts']['completeReviewedStandaloneProcedures']==541
 assert p0['authority']==q0['currentAuthority']==h0['currentAuthority']==BEFORE
 entry0=copy.deepcopy(next(x for x in index0['entries'] if x['id']==ID)); live0={x['id'] for x in index0['entries'] if x['authoredStatus']=='pending-authored-procedure'}
 assert ID in live0 and len(live0)==31 and catalog0['spells'][386]['id']==ID
 return_path=A/'rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip'
 delivery_path=A/'rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json'
 case_dir=BASE/'cases'
 case_names=['RANK9AGENCYCONTROL9129-ABSOLUTE-DOMINATION-A.json','RANK9AGENCYCONTROL9129-ABSOLUTE-DOMINATION-A__genuine-extra-turn.json','RANK9AGENCYCONTROL9129-ABSOLUTE-DOMINATION-B.json','RANK9AGENCYCONTROL9129-ABSOLUTE-DOMINATION-B__paid-countered-ready.json','RANK9AGENCYCONTROL9129-ABSOLUTE-DOMINATION-B__mind-blank-initial-prevention.json','RANK9AGENCYCONTROL9129-ABSOLUTE-DOMINATION-B__true-seeing-no-restoration.json','RANK9AGENCYCONTROL9129-ABSOLUTE-DOMINATION-A__actual-regular-END.json','RANK9AGENCYCONTROL9129-ABSOLUTE-DOMINATION-A__current-turn-END.json']
 case_refs=[bind(case_dir/n) for n in case_names]
 branches=[]
 for cid in ('AG190-B01-CI-INSERTED-END-FAILURE','AG190-B01-CI-INSERTED-END-SUCCESS'):
  f=D/f'{cid}.json'; c=read(f); ev=c['events'][0]
  branches.append({'id':cid,'binding':bind(f),'stateBeforeSHA256':c['initialStateSHA256'],'stateAfterSHA256':c['finalStateSHA256'],'forwardOperations':len(ev['forward']),'inverseOperations':len(ev['inverse']),'outcome':c['outcome']})
 success=read(D/'AG190-B01-CI-INSERTED-END-SUCCESS.json'); assert success['finalState']['actors']['C']['concentration'] is None
 stamp=now(); decision_id='RANK9-AGENCYCONTROL9-ABSOLUTE-DOMINATION-DIRECTOR-DECISION-292'; acceptance_id='RANK9-AGENCYCONTROL9-ABSOLUTE-DOMINATION-ACCEPTANCE-292'; app_id='RANK9-AGENCYCONTROL9-ABSOLUTE-DOMINATION-APPLICATION-292'
 decision={'id':decision_id,'recordedAtUtc':stamp,'decision':'EXACT_ACCEPT','identity':ID,'closedBlockerIds':[BLOCKER],'accepted':True,'appliedAtDecision':False,'source':{'service':'ChatGPT','conversationTitle':'Calibration review part 6','url':URL},'exactDirectorResponse':DIRECTOR_TEXT,'directorObligationRevision':delta['directorRuling']['selectedObligationRevision'],'delta':bind(delta_path),'independentAudit':bind(audit_path),'directorReturnReceipt':bind(D/'DIRECTOR_RETURN_291.json'),'authorityAtDecision':{'reviewedApplied':817,'pending':31,'acceptedUnapplied':1,'completeStandaloneProcedures':541,'scopedInterfaces':173},'authorityAfterApplicationExpected':AFTER,'acceptanceScope':'Preserved Absolute Domination procedure and corrected conditional END-save tests under AG291-OBLIGATION-REVISION-01 only.','retainedQualifications':QUALS,'retainedHoldIds':retained,'nextPriority':{'identity':NEXT,'blocker':NEXT_BLOCKER,'group':NEXT_GROUP,'requirement':'Complete native Multiattack members/reaches, lawful admission, and actual command/resource history; exact Cave Bear source has unresolved reach/Bite fields.'},'otherSpellAccepted':False,'canonicalFilesChangedByDirector':False,'gatesStillClosed':['runtime','implementation','human-play','balance','cosmology','domain-closure','release']}
 decision_path=A/'ABSOLUTE_DOMINATION_DIRECTOR_DECISION_292.json'; write(decision_path,decision); decision_ref=bind(decision_path)
 PKG.mkdir(parents=True)
 proc_record=copy.deepcopy(source); proc_record['procedure']=proc
 proc_record.update({'status':'DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED','accepted':True,'applied':True,'blockerIds':[],'closedBlockerIds':[BLOCKER],'resolvedBlockerIds':[BLOCKER],'directorObligationRevision':delta['directorRuling']['selectedObligationRevision'],'closureDeltaBinding':bind(delta_path),'closureDeltaAuditBinding':bind(audit_path),'directorDecisionBinding':decision_ref,'retainedQualifications':QUALS,'holdIds':retained,'scope':'Absolute Domination only; preserved procedure and two corrected conditional END-save interface branches; runtime disabled.'})
 # Copy the Director-reviewed evidence into a self-contained package.
 for cid in ('AG190-B01-CI-INSERTED-END-FAILURE','AG190-B01-CI-INSERTED-END-SUCCESS'):
  shutil.copy2(D/f'{cid}.json',PKG/f'{cid}.json')
 coverage={'id':'ABSOLUTE-DOMINATION-CASE-COVERAGE-292','spellId':ID,'preservedCases':{'bindings':case_refs,'count':8,'unchanged':True},'acceptedConditionalInterfaceCases':branches,'lifecycleAssertions':{'failureLeavesApplicationAndPendingOrder':True,'successEndsApplicationAndPendingOrder':True,'successClearsCasterConcentration':True,'budgetsAndRegularClocksUnchanged':True,'noAcquiredProviderAsserted':True},'scope':'Static authored cases; no runtime or actual gameplay grant.'}
 write(PKG/'CASE_COVERAGE.json',coverage)
 evidence={'id':'ABSOLUTE-DOMINATION-ACCEPTED-EVIDENCE-292','sourceProcedure':bind(source_path),'return238':bind(return_path),'return238Delivery':bind(delivery_path),'directorDecision':decision_ref,'directorReturnReceipt':bind(D/'DIRECTOR_RETURN_291.json'),'closureDelta':bind(delta_path),'independentAudit':bind(audit_path),'preservedCases':case_refs,'conditionalBranches':branches,'retainedQualifications':QUALS,'retainedHoldIds':retained}
 write(PKG/'EVIDENCE_BINDINGS.json',evidence)
 write(PKG/'DIRECTOR_DECISION.json',decision); write(PKG/'PREVIOUS_PROCEDURE_RECORD.json',source); write(PKG/'PROCEDURE_RECORD.json',proc_record)
 (PKG/'AG190_B01_CLOSURE_DELTA_292.json').write_bytes(delta_raw); (PKG/'AG190_B01_CLOSURE_DELTA_INDEPENDENT_AUDIT_292.json').write_bytes(audit_raw)
 procedure_content=json.dumps(proc,ensure_ascii=False,indent=2)
 model={'schemaVersion':1,'moduleId':'rank9agencycontrol9-absolutedomination-reviewed-292','status':'ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED','scope':'Absolute Domination only; accepted preserved procedure plus corrected conditional END-save cases under AG291-OBLIGATION-REVISION-01. Native catalog and runtime remain unchanged.','acceptedIds':[ID],'unacceptedIds':[],'excludedPendingIds':sorted(live0-{ID}),'unresolvedQualifications':{ID:QUALS},'sharedRequirements':{'scope':'No global/shared rule changes; native catalog unchanged; runtime selection disabled.','runtimeSelectionEnabled':False},'spells':[{'id':ID,'name':NAME,'position':0,'procedure':{'id':'AG190-STATIC-ABSOLUTE-DOMINATION-292','spellId':ID,'status':'director-accepted static authored procedure; applied to authored review index; runtime disabled','accepted':True,'applied':True,'nativeCardUnchanged':copy.deepcopy(source['nativeCardUnchanged']),'procedureContent':procedure_content,'procedureRecordFile':'PROCEDURE_RECORD.json','directorObligationRevision':delta['directorRuling']['selectedObligationRevision'],'retainedQualifications':QUALS,'closedBlockerIds':[BLOCKER],'retainedHoldIds':retained,'caseIds':source['caseIds']+['AG190-B01-CI-INSERTED-END-FAILURE','AG190-B01-CI-INSERTED-END-SUCCESS'],'directorDecisionId':decision_id,'evidenceBindingsFile':'EVIDENCE_BINDINGS.json','caseCoverageFile':'CASE_COVERAGE.json'},'directorProcedureRecord':proc_record,'previousProcedureRecord':source,'nativeCardUnchanged':copy.deepcopy(source['nativeCardUnchanged']),'caseIds':source['caseIds']+['AG190-B01-CI-INSERTED-END-FAILURE','AG190-B01-CI-INSERTED-END-SUCCESS'],'retainedHoldIds':retained,'runtimeSelectionEnabled':False}],'sourceProcedure':bind(source_path),'return238':bind(return_path),'directorDecision':decision_ref,'closureDelta':bind(delta_path),'independentAudit':bind(audit_path),'caseCoverage':coverage,'evidenceBindings':evidence,'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'implementationApproved':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'domainClosure':False,'releaseApproved':False}
 write(PKG/'MODEL.json',model)
 manuscript=('# Absolute Domination — accepted static authored procedure 292\n\nGPT accepted Absolute Domination / AG190-B01 only after verifying the corrected conditional END-save branches. This updates the authored review index; the native spell catalog, runtime selection, and downstream gates remain unchanged.\n\n## Preserved native card and procedure\n\n'+json.dumps(source['nativeCardUnchanged'],ensure_ascii=False,indent=2)+'\n\n'+procedure_content+'\n\n## Accepted conditional closure tests\n\n- Failure branch: WIS 1 + 7 = 8 vs. DC 19; control and pending regular Dodge remain.\n- Success branch: WIS 12 + 7 = 19 vs. DC 19; the application, pending order, and caster concentration pointer end.\n- The branches establish no actual provider or gameplay turn.\n\n## Retained qualifications\n\n'+'\n'.join('- '+x for x in QUALS)+'\n')
 (PKG/'STANDALONE_PROCEDURES.md').write_text(manuscript,encoding='utf-8',newline='\n')
 MANUSCRIPT.parent.mkdir(parents=True,exist_ok=True); MANUSCRIPT.write_text(manuscript,encoding='utf-8',newline='\n')
 manifest={'id':'ABSOLUTE-DOMINATION-PACKAGE-MANIFEST-292','directorDecision':decision_ref,'sourceProcedure':bind(source_path),'return238':bind(return_path),'closureDelta':bind(delta_path),'files':[]}
 for f in sorted(x for x in PKG.rglob('*') if x.is_file() and x.name!='CANDIDATE_PACKAGE_MANIFEST.json'):
  manifest['files'].append({'path':(PKG_REL/f.relative_to(PKG)).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())})
 write(PKG/'CANDIDATE_PACKAGE_MANIFEST.json',manifest)
 model_ref=bind(PKG/'MODEL.json'); package_ref=bind(PKG/'CANDIDATE_PACKAGE_MANIFEST.json'); coverage_ref=bind(PKG/'CASE_COVERAGE.json'); evidence_ref=bind(PKG/'EVIDENCE_BINDINGS.json'); manuscript_ref=bind(MANUSCRIPT)
 acceptance_id='RANK9-AGENCYCONTROL9-ABSOLUTE-DOMINATION-ACCEPTANCE-292'; app_id='RANK9-AGENCYCONTROL9-ABSOLUTE-DOMINATION-APPLICATION-292'
 acceptance={'id':acceptance_id,'recordedAtUtc':stamp,'status':'ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED','acceptedIds':[ID],'appliedIds':[],'closedBlockerIds':[BLOCKER],'directorDecision':decision_ref,'sourceProcedure':bind(source_path),'return238':bind(return_path),'closureDelta':bind(delta_path),'independentAudit':bind(audit_path),'candidateEnvelope':model_ref,'candidatePackageManifest':package_ref,'evidenceBindings':evidence_ref,'caseCoverage':coverage_ref,'countsBefore':{'reviewedApplied':817,'pending':31,'acceptedUnapplied':0},'countsAfterAcceptanceBeforeApplication':{'reviewedApplied':817,'pending':31,'acceptedUnapplied':1},'retainedQualifications':QUALS,'retainedHoldIds':retained}
 acceptance_path=A/'ABSOLUTE_DOMINATION_ACCEPTANCE_292.json'; write(acceptance_path,acceptance); acceptance_ref=bind(acceptance_path)
 receipt={'id':'RANK9-AGENCYCONTROL9-ABSOLUTE-DOMINATION-RETURN292-RECEIPT','recordedAtUtc':stamp,'status':'EXACT_ACCEPT_ABSOLUTE_DOMINATION_AG190_B01_ONLY','acceptedIds':[ID],'appliedIds':[],'closedBlockerIds':[BLOCKER],'directorDecision':decision_ref,'acceptance':acceptance_ref,'sourceProcedure':bind(source_path),'closureDelta':bind(delta_path),'independentAudit':bind(audit_path),'nextPriority':decision['nextPriority'],'retainedHoldIds':retained,'sourceResponse':DIRECTOR_TEXT}
 receipt_path=A/'ABSOLUTE_DOMINATION_RETURN292_RECEIPT.json'; write(receipt_path,receipt); receipt_ref=bind(receipt_path)
 index1=copy.deepcopy(index0); entry1=copy.deepcopy(entry0)
 entry1.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/rank9agencycontrol9_absolutedomination_reviewed_292/MODEL.json','procedurePointer':'/spells/0/procedure','wholeCardPointer':'/spells/0','wholeCardIdField':'id','sourceCatalogWholeCardPointer':entry0.get('sourceCatalogWholeCardPointer') or entry0['wholeCardPointer'],'procedureTextPointer':'/spells/0/procedure/procedureContent','directorProcedureRecordPointer':'/spells/0/directorProcedureRecord','sharedRulesPointer':'/sharedRequirements','spellLocalRequirementsPointer':'/spells/0/procedure','manuscript':'../../../docs/spells/candidates/ABSOLUTE_DOMINATION_REVIEWED_292.md','reviewId':app_id,'runtimeSelectionEnabled':False,'historicalCandidateLabelsPreserved':True,'completeEvidenceRoot':PKG_REL.as_posix(),'completeEnvelopeBinding':model_ref,'caseEvidenceBindings':coverage_ref,'sourceArchiveBinding':bind(return_path),'deliveryManifestBinding':bind(delivery_path),'candidatePackageManifestBinding':package_ref,'procedureSourceBinding':decision_ref,'authoredAcceptanceReceipt':acceptance_ref,'authoredApplicationReceipt':app_id+'.json','directorReturnReceipt':receipt_ref,'accepted':True,'applied':True,'closedBlockerIds':[BLOCKER],'retainedQualifications':QUALS,'retainedHoldIds':retained})
 entry_i=next(i for i,x in enumerate(index1['entries']) if x['id']==ID); index1['entries'][entry_i]=entry1
 assert not any(ID in x.get('acceptedIds',[]) for x in index1['additionalStandaloneEnvelopes'])
 envelope={'file':'../spell_candidates/rank9agencycontrol9_absolutedomination_reviewed_292/MODEL.json','binding':model_ref,'reviewId':acceptance_id,'acceptedIds':[ID],'unacceptedIds':[],'excludedPendingIds':sorted(live0-{ID}),'authority':acceptance_ref,'applicationReceipt':app_id+'.json','directorDecision':decision_ref,'directorReturnReceipt':receipt_ref,'sourceProcedure':bind(source_path),'caseCoverage':coverage_ref,'candidatePackageManifestBinding':package_ref,'closureDelta':bind(delta_path),'independentAudit':bind(audit_path),'scope':'ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED'}
 index1['additionalStandaloneEnvelopes'].append(envelope); index1['authoredCounts']={'reviewed':818,'pending':30}; index1['representationCounts']['completeReviewedStandaloneProcedures']=542
 live1={x['id'] for x in index1['entries'] if x['authoredStatus']=='pending-authored-procedure'}; assert live1==live0-{ID} and len(live1)==30 and NEXT in live1
 backup=A/'authored_review_index.before_absolute_domination_292.json'; backup.write_bytes(index_raw)
 write(INDEX,index1); index_core_ref=bind(INDEX)
 application={'id':app_id,'recordedAtUtc':stamp,'status':'APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE','acceptedIds':[ID],'appliedIds':[ID],'closedBlockerIds':[BLOCKER],'directorAcceptance':acceptance_ref,'directorDecision':decision_ref,'directorReturnReceipt':receipt_ref,'sourceProcedure':bind(source_path),'closureDelta':bind(delta_path),'independentAudit':bind(audit_path),'candidateEnvelope':model_ref,'candidatePackageManifest':package_ref,'evidenceBindings':evidence_ref,'caseCoverage':coverage_ref,'manuscript':manuscript_ref,'indexBefore':bind(backup,index_raw),'indexAfterCoreUpdate':index_core_ref,'countsBefore':BEFORE,'countsAfter':AFTER,'completeReviewedStandaloneProcedures':{'before':541,'after':542},'scopedInterfaces':173,'catalogChanged':False,'sourceStatusPreservedAsBlocked':True,'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'implementationApproved':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'domainClosure':False,'releaseApproved':False}
 app_path=A/'ABSOLUTE_DOMINATION_APPLICATION_292.json'; write(app_path,application); app_ref=bind(app_path)
 entry1['authoredApplicationReceipt']=app_ref; index1['entries'][entry_i]=entry1
 index1['additionalStandaloneEnvelopes'][-1]['applicationReceipt']=app_ref
 write(INDEX,index1); index_ref=bind(INDEX)
 ops_path=A/'ABSOLUTE_DOMINATION_INDEX_OPERATIONS_292.json'
 write(ops_path,{'id':'ABSOLUTE-DOMINATION-INDEX-OPERATIONS-292','recordedAtUtc':stamp,'before':bind(backup,index_raw),'after':index_ref,'operations':[{'op':'update-entry','id':ID,'before':entry0,'after':entry1},{'op':'append-standalone-envelope','acceptedIds':[ID]},{'op':'update-authored-counts','before':{'reviewed':817,'pending':31},'after':{'reviewed':818,'pending':30}},{'op':'increment-complete-procedure-count','before':541,'after':542}],'inverse':[{'op':'restore-entry','id':ID,'value':entry0},{'op':'remove-appended-standalone-envelope','acceptedIds':[ID]},{'op':'restore-authored-counts','value':{'reviewed':817,'pending':31}},{'op':'restore-complete-procedure-count','value':541},{'op':'restore-byte-exact-index-from-backup','backup':bind(backup,index_raw)}],'catalogByteExact':CATALOG.read_bytes()==catalog_raw,'nativeCardUnchanged':True,'sourceStatusPreservedAsBlocked':True,'inverseRestoresExactIndex':backup.read_bytes()==index_raw})
 authority=copy.deepcopy(AFTER); groups=clean_groups(p0['groups'])
 order=[]
 for oldrow in q0['recommendedClosureOrder']:
  row=copy.deepcopy(oldrow)
  for key in ('identities','pendingIds','spellIds'):
   if key in row: row[key]=[x for x in row[key] if x!=ID]
  key=next((k for k in ('identities','pendingIds','spellIds') if k in row),None)
  if key and not row[key]: continue
  row['priority']=len(order)+1; order.append(row)
 next_requirement='Complete native Multiattack members and reaches, lawful admission, and actual command/resource history; do not infer missing Cave Bear attack details.'
 next_row={'group':NEXT_GROUP,'pendingIds':[NEXT],'pendingCount':1,'status':'DIRECTOR_NEXT_IDENTITY_AFTER_ABSOLUTE_DOMINATION_292','freshPacketRequiredForCurrentAuthority':True,'directorRequirement':next_requirement}
 pending1=copy.deepcopy(p0)
 pending1.update({'id':'CURRENT30_PENDING_IDENTITY_AUDIT_292','recordedAtUtc':stamp,'status':'PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_ABSOLUTE_DOMINATION_APPLICATION_292','authority':authority,'indexBinding':index_ref,'catalogBinding':bind(CATALOG,catalog_raw),'pendingCount':30,'pendingIds':sorted(live1),'groups':groups,'heldIds':sorted(set(p0.get('heldIds',[]))-{ID}),'acceptedIds':sorted(set(p0.get('acceptedIds',[]))|{ID}),'appliedIds':sorted(set(p0.get('appliedIds',[]))|{ID}),'applicationReceipt':app_ref,'directorDecision':decision_ref,'acceptanceReceipt':acceptance_ref,'closedBlockerIdsThisStep':sorted(set(p0.get('closedBlockerIdsThisStep',[]))|{BLOCKER}),'lastDirectorReturn':{'decisionId':decision_id,'acceptedIds':[ID],'appliedIds':[ID],'heldIds':[],'closedBlockerIds':[BLOCKER],'delta':bind(delta_path),'independentAudit':bind(audit_path)},'nextBlockerPriority':[x for x in q0['recommendedClosurePriority'] if x!=ID],'preparedNextGroup':{'group':NEXT_GROUP,'pendingIds':[NEXT],'freshPacketRequiredForCurrentAuthority':True,'directorRequirement':next_requirement},'remainingPendingCount':30,'pendingIdentityCount':30})
 pending_path=A/'CURRENT30_PENDING_IDENTITY_AUDIT_292.json'; write(pending_path,pending1); pending_ref=bind(pending_path)
 queue1=copy.deepcopy(q0)
 next_item={'group':NEXT_GROUP,'pendingIds':[NEXT],'pendingCount':1,'status':'DIRECTOR_NEXT_IDENTITY_AFTER_ABSOLUTE_DOMINATION_292','freshPacketRequiredForCurrentAuthority':True,'directorRequirement':next_requirement}
 queue1.update({'id':'SPELL-REVIEW-QUEUE-292','recordedAtUtc':stamp,'supersedesQueue':bind(A/'CURRENT_SPELL_QUEUE_291.json'),'parentQueue':bind(A/'CURRENT_SPELL_QUEUE_291.json'),'currentAuthority':authority,'currentIndexBinding':index_ref,'pendingIdentityAudit':pending_ref,'pendingCount':30,'nextGroup':NEXT_GROUP,'next':next_item,'nextPendingIds':[NEXT],'currentPendingGroups':groups,'nextSuggestedGroups':[next_item],'recommendedClosureOrder':order,'recommendedClosurePriority':[x for x in q0['recommendedClosurePriority'] if x!=ID],'lastReviewedBatch':{'group':'rank9-agency-control9','acceptedIds':[ID],'appliedIds':[ID],'heldIds':[],'closedBlockerIds':[BLOCKER]},'justAppliedBatch':{'reviewId':acceptance_id,'applicationId':app_id,'ids':[ID],'count':1,'applicationReceipt':app_ref,'directorDecision':decision_ref,'closureDelta':bind(delta_path),'independentAudit':bind(audit_path)},'packetStatus':'ABSOLUTE_DOMINATION_AG190_B01_ACCEPTED_AND_APPLIED; NEXT_PUPPETMASTERS_REALM_AG190_B02','currentAcceptedPacket':{'sourceProcedure':bind(source_path),'directorDecision':decision_ref,'acceptance':acceptance_ref,'application':app_ref,'closureDelta':bind(delta_path),'independentAudit':bind(audit_path)},'currentDirectorPosition':{'stage':'ABSOLUTE_DOMINATION_ACCEPTED_AG190_B01; PUPPETMASTERS_REALM_NEXT','acceptedIds':[ID],'appliedIds':[ID],'heldIds':sorted(live1),'blockers':{NEXT:[NEXT_BLOCKER]},'nextPendingGroup':{'group':NEXT_GROUP,'pendingIds':[NEXT],'pendingCount':1,'reportedByDirector':True}},'nextPriorityContext':{'identity':NEXT,'blocker':NEXT_BLOCKER,'requirement':next_requirement},'githubChanges':False,'canonicalRuntimeApplicationPerformed':False,'afterNextAcceptedAppliedForecast':{'remainingIdentities':29}})
 queue_path=A/'CURRENT_SPELL_QUEUE_292.json'; write(queue_path,queue1); queue_ref=bind(queue_path)
 handoff=copy.deepcopy(h0)
 handoff.update({'id':'CURRENT-HANDOFF-292','recordedAtUtc':stamp,'supersedes':h0['id'],'status':'ABSOLUTE_DOMINATION_APPLIED_NEXT_PUPPETMASTERS_REALM_818_30','authority':authority,'currentAuthority':authority,'indexBinding':index_ref,'queueBinding':queue_ref,'queue':queue_path.relative_to(ROOT).as_posix(),'pendingIdentityAudit':pending_ref,'appliedThisStep':True,'acceptedThisStep':[ID],'appliedThisStepRecord':{'identity':ID,'application':app_path.relative_to(ROOT).as_posix(),'applicationBinding':app_ref,'closedBlockerIds':[BLOCKER]},'nextStep':next_item,'nextGroup':NEXT_GROUP,'nextPendingCount':1,'nextPendingIds':[NEXT],'currentBlocker':{'identity':NEXT,'group':NEXT_GROUP,'blockerId':NEXT_BLOCKER},'directorConnectionStatus':'GPT explicitly accepted Absolute Domination / AG190-B01 only; next is Puppetmaster\'s Realm / AG190-B02.','githubChanges':False,'latestBatch':{'accepted':[ID],'applied':[ID],'closed':[BLOCKER]},'currentPreparation':next_item,'canonicalRuntimeApplicationPerformed':False,'nextStepText':'Use the exact native Multiattack source and full actor history, or request a spell-local Director revision that retains AG190-H-SOURCE.'})
 handoff_path=A/'CURRENT_HANDOFF_292.json'; write(handoff_path,handoff); handoff_ref=bind(handoff_path)
 checks=[
 ('Director explicitly accepted only Absolute Domination / AG190-B01',decision['accepted'] and decision['closedBlockerIds']==[BLOCKER]),
 ('Packet292 exact ZIP hash and independent audit pass',sha((D/'DD_Rank9_AgencyControl9_AbsoluteDomination_ClosureDelta_292.zip').read_bytes())=='a966ca1366180ec0f21dc7cd791cf23f279a4e6c465632662ed125f349efb925' and audit['status']=='PASS' and audit['passedChecks']==23),
 ('Both test branches share the same state; success clears caster concentration',branches[0]['stateBeforeSHA256']==branches[1]['stateBeforeSHA256'] and success['finalState']['actors']['C']['concentration'] is None),
 ('Only Absolute Domination leaves the pending set',live1==live0-{ID} and len(live1)==30 and NEXT in live1),
 ('Authority advances to 818/30/0 and 542/173',index1['authoredCounts']=={'reviewed':818,'pending':30} and index1['representationCounts']['completeReviewedStandaloneProcedures']==542 and authority==AFTER),
 ('Native catalog byte-exact and sourceStatus remains blocked',CATALOG.read_bytes()==catalog_raw and index1['entries'][entry_i]['sourceStatus']=='blocked-pending-operational-review'),
 ('Runtime and downstream gates remain disabled',model['runtimeSelectionEnabled'] is False and model['implementationApproved'] is False and model['releaseApproved'] is False),
 ('Next identity is Puppetmaster\'s Realm / AG190-B02',queue1['next']['pendingIds']==[NEXT] and queue1['nextGroup']==NEXT_GROUP and decision['nextPriority']['blocker']==NEXT_BLOCKER),
 ('Backup restores the exact original index bytes',backup.read_bytes()==index_raw),
 ('Pending audit, queue, and handoff bind the final index',pending1['indexBinding']['sha256']==index_ref['sha256'] and queue1['currentIndexBinding']['sha256']==index_ref['sha256'] and handoff['indexBinding']['sha256']==index_ref['sha256']),
 ]
 assert all(ok for _,ok in checks),[x for x in checks if not x[1]]
 validation={'id':'ABSOLUTE-DOMINATION-APPLICATION-VALIDATION-292','recordedAtUtc':stamp,'status':'PASS','checks':[{'check':k,'passed':ok} for k,ok in checks],'checkCount':len(checks),'failedChecks':0,'acceptedIds':[ID],'appliedIds':[ID],'authority':authority,'index':index_ref,'application':app_ref,'pendingIdentityAudit':pending_ref,'queue':queue_ref,'handoff':handoff_ref,'indexOperations':bind(ops_path),'catalogByteExact':True,'sourceStatusPreservedAsBlocked':True,'runtimeSelectionEnabled':False}
 validation_path=A/'ABSOLUTE_DOMINATION_APPLICATION_VALIDATION_292.json'; write(validation_path,validation); validation_ref=bind(validation_path)
 snapshot_path=A/'CURRENT_SPELL_REVIEW_SNAPSHOT_292.md'
 snapshot_path.write_text('# Spell Review Snapshot - Absolute Domination Application 292\n\nAuthority: **818 applied / 30 pending / 0 accepted-unapplied; 542 complete standalone procedures / 173 scoped interfaces.**\n\nAbsolute Domination / AG190-B01 was explicitly accepted by GPT and applied to the authored review index using corrected conditional END-save tests under AG291-OBLIGATION-REVISION-01. AG190-H-SOURCE and all other qualifications remain. The native spell catalog and runtime selection are unchanged.\n\nNext priority: **puppetmaster-s-realm / AG190-B02**. The Director requires complete native Multiattack members and reaches, lawful admission, and actual command/resource history.\n\nValidation: '+validation_ref['path']+' ('+validation_ref['sha256']+').\n',encoding='utf-8',newline='\n')
 assert sha(INDEX.read_bytes())==index_ref['sha256'] and CATALOG.read_bytes()==catalog_raw and backup.read_bytes()==index_raw
 print(json.dumps({'status':'PASS','acceptedApplied':ID,'authority':AFTER,'index':index_ref,'package':package_ref,'application':app_ref,'validation':validation_ref,'pendingAudit':pending_ref,'queue':queue_ref,'handoff':handoff_ref,'next':decision['nextPriority']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
