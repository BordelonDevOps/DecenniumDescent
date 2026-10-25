"""Fresh data-only Transport6 acceptance/application; no historical runner is executed."""
from pathlib import Path
import json,copy,hashlib,datetime,shutil
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-128';S=D/'transport6-return01'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def write(p,b):
 assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def ptr(v,p):
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
checks=read(D/'TRANSPORT6_DATA_CHECKS_128.json');native=read(D/'TRANSPORT6_CURRENT_AUTHORITY_CHECKS_128.json');assert not checks['findings'] and checks['checks']==23499;assert not native['findings'] and native['checks']==120
ids=['dimension-door','dimensional-shift','instant-summons','mystic-gate','teleport-object','teleportation-circle'];m=read(S/'MODEL.json');assert [x['spellId'] for x in m['records']]==ids
for row in read(S/'MANIFEST.json')['files']:
 raw=(S/row['path']).read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
ip=R/'data/public/spell_playtests/authored_review_index.json';raw=ip.read_bytes();old=read(ip);idx=copy.deepcopy(old);assert idx['authoredCounts']=={'reviewed':610,'pending':238}
assert sha(raw)=='7ef037430f6bc9f90b2e935039e49b0d83c22453ba31649292ecf08d0bb5aa4a'
for sid in ids:assert next(e for e in idx['entries'] if e['id']==sid)['authoredStatus']=='pending-authored-procedure'
arc=D/'DD_Transport6_Accepted_128.zip';download=D/'DD_Transport6_Latest_128_Download.zip';assert sha(download.read_bytes())=='584a91e6728b100fe30aac84af2d8df6a6dcd655ef2d841887bed39d56528e31';write(arc,download.read_bytes())
semantic={
'dimension-door':'Distinct Universal identity and all native access retained. Measured-vector selection is explicit new authorship; no passenger/path traversal/remote knowledge. Actual known wall traversal, hidden exact-arrival blockage, native Anchor and Counterspell, paid Ready release, and unsupported40ft arrival with ordinary later Falling were independently inspected.',
'dimensional-shift':'Complete disjoint graphs exchange anchors simultaneously; no independent aliasing, implicit inventory release, anchored-object ripping or imported size cap. CHA for every real resisting holder. Known overlapping graph/bolt preflight and paid unknown local ceiling are distinct; ceiling is explicitly knownByCaster=false. Actual40ft unsupported target arrival retains ordinary new Falling and real legal movement/grip handling.',
'instant-summons':'60ft preparation, same identity and current inclusive contents, one5280ft BA attempt before establishment+60 deadline. Original600ft route retains real two-interaction handling, nine60ft Dash budgets and57.4 release; actual START60/hand stow precedes60.1 recall and60.11 child completion before60.2 expiry. Exact-expiry no-debit, hidden holder, actual55lb change and conditional fragment cases inspected. Committed child survives spent-parent cleanup without duplication.',
'mystic-gate':'Fixed paired5x8 apertures and proper declared yaw. Two real5ft crossings use actual movement and no refreshed Action.12ft beam fits inlet projection but rotated receiver and all finite adjacent candidates fail against actual back wall. Actual10ft-range Lesser Antimagic suppresses local endpoint without resetting original clock. Original wagon remains conditional on authentic driver/puller/vehicle capability; pedestrian and beam are explicitly separate evidence.',
'teleport-object':'Native500lb whole noncreature object, all three100ft anchor bounds and actual perceived chest surface retained. Locked470lb positive preserves actual contents/lock, while hidden510lb or living body fail without diagnostics. Every real custodian makes WIS; one success blocks all, all failures clear both actual grips without changing ownership. Supported at-rest exact arrival does not grant momentum or falling attacks.',
'teleportation-circle':'Three paid600second casts plus two600second personal studies and1000 full work phase events inspected; no parallel work/rest/RP refill. Actual immutable source-ID knowledge and local receiving approval are separate. Three casts cost30RP; final18RP/3Dissonance/2Refrain follows real quiet-study vent. True radius5 disk rejects10x10frame; separate actual putdown allows later body-only use. Six-second origin cooldown starts at paid commitment, survives failed suppressed destination and cannot refresh by duplicate callback. Current native Lesser Antimagic source is exactly10ft away. Countered rebind retains completed sites/approvals. Mid-atomic independent event remains explicitly conditional, not a Ready interrupt.'}
acceptance={'id':'TRANSPORT6-EXACT-LOCAL-ACCEPTANCE-128','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'AUTHORED_REVIEW_ACCEPTED_WITH_RETAINED_CONTENT_AND_IMPLEMENTATION_HOLDS','acceptedIdentities':ids,'directorReturnMessage':'b333a20a-cc52-429a-b037-053d8328f8bb','deliveryRecoveryMessage':'fd68c6f9-f43a-4ebf-8533-ab0bcb925b2d','archive':bind(arc),'currentModel':bind(S/'MODEL.json'),'casebook':bind(S/'CASEBOOK.json'),'workPhaseHistory':bind(S/'WORK_PHASE_HISTORY.json'),'manifest':bind(S/'MANIFEST.json'),'independentDataChecks':bind(D/'TRANSPORT6_DATA_CHECKS_128.json'),'currentAuthorityChecks':bind(D/'TRANSPORT6_CURRENT_AUTHORITY_CHECKS_128.json'),'counts':checks['counts'],'sourcePreservation':{'manifestBindings':48,'outerBindings':47,'originalSourceBindings':29,'completeOriginalCandidateByteExact':True,'forwardAndReverseSevenAdditionsByteExact':True,'nativeAccessRowsUnchanged':42,'questionDispositions':21,'localRuleOrCaseChanges':0},'semanticReview':semantic,'holdDisposition':'All11 complete source/conditional/implementation hold records retained. Only independent exact-review reservation is discharged for these exact bytes. Current user authorizes canonical authored application. Vehicle, physical-break/potion, Paladin-positive and late-interrupt providers, inherited whole-case holds, real-world authentication, runtime, human/balance/cosmology and release remain qualified. Historical Body8/Time5 pending labels are superseded only by their exact126/127 receipts; Material8 remains unaccepted.','canonicalApplied':False,'runtimeExecuted':False,'noSelectedProcedureOrQuestionChanges':True}
ap=D/'TRANSPORT6_EXACT_ACCEPTANCE_128.json';write(ap,enc(acceptance));write(D/'authored_review_index.before_transport6_128.json',raw)
E=R/'data/public/spell_candidates/transport6_reviewed_128';assert not E.exists();shutil.copytree(S,E)
for p in S.rglob('*'):
 if p.is_file():assert p.read_bytes()==(E/p.relative_to(S)).read_bytes()
mp=E/'MODEL.json';cp=E/'CASEBOOK.json';hp=E/'HOLD_REGISTER.json';wp=E/'WORK_PHASE_HISTORY.json';tp=R/'docs/spells/candidates/TRANSPORT6_REVIEWED_128.md'
header='# Transport6 - applied authored review128\n\nThe six exact authored procedures are accepted by TRANSPORT6_EXACT_ACCEPTANCE_128.json and applied by TRANSPORT6_APPLICATION_128.json under the owner instruction to apply each accepted batch. All49 exact return files, including the1000 work-phase events, are preserved together under data/public/spell_candidates/transport6_reviewed_128 so internal evidence references remain resolvable. Historical pending labels are retained evidence, superseded by the current acceptance/application receipts. All stated content, conditional-case, implementation, human, balance, cosmology and release holds remain. No rule or case was changed locally.\n\n'
write(tp,header.encode()+(S/'OPERATIVE_TEXT.md').read_bytes())
receipt={'id':'TRANSPORT6-APPLICATION-128','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'APPLIED_AUTHORED_REVIEW_WITH_RETAINED_HOLDS','ownerInstruction':'Check GPT again for Transport6 and keep working through the remaining spells. Apply each batch once it is accepted.','acceptedIds':ids,'acceptedModelSource':bind(S/'MODEL.json'),'canonicalModel':bind(mp),'authority':bind(ap),'exactEvidenceRoot':E.relative_to(G).as_posix(),'evidenceManifest':bind(E/'MANIFEST.json'),'chapter':bind(tp),'casebook':bind(cp),'workPhaseHistory':bind(wp),'holds':bind(hp),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'historicalPendingLabelsPreserved':True,'scope':'Select exact accepted authored procedures and retain complete case/work/source evidence and all outstanding qualifications.','supersession':'Exact-review gate closed by acceptance128; canonical-integration reservation discharged by current user instruction. No other gate is closed.'}
rp=D/'TRANSPORT6_APPLICATION_128.json';write(rp,enc(receipt));ops=[]
for n,e in enumerate(idx['entries']):
 if e['id'] not in ids:continue
 prev=copy.deepcopy(e);i=ids.index(e['id']);pointer=f'/records/{i}/selectedOperationalProcedure126';assert ptr(m,pointer)['spellId']==e['id']
 e.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/transport6_reviewed_128/MODEL.json','sourceCatalogWholeCardPointer':prev['wholeCardPointer'],'wholeCardPointer':pointer,'wholeCardIdField':'spellId','procedurePointer':pointer,'procedureTextPointer':pointer+'/selectedProcedure','sharedRulesPointer':'/selectedReview126/sharedRules','manuscript':'../../../docs/spells/candidates/'+tp.name,'reviewId':receipt['id'],'runtimeSelectionEnabled':False,'completeEnvelopeBinding':bind(mp),'authoredAcceptanceReceipt':bind(ap),'authoredApplicationReceipt':bind(rp),'historicalCandidateLabelsPreserved':True,'casebookBinding':bind(cp),'retainedHoldsBinding':bind(hp),'workPhaseHistoryBinding':bind(wp),'completeEvidenceRoot':E.relative_to(G).as_posix()})
 ops.append({'pointer':f'/entries/{n}','before':prev,'after':copy.deepcopy(e)})
idx['authoredCounts']={'reviewed':616,'pending':232};idx['representationCounts']['completeReviewedStandaloneProcedures']=340
idx['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/transport6_reviewed_128/MODEL.json','binding':bind(mp),'reviewId':receipt['id'],'acceptedIds':ids,'authority':bind(ap),'receipt':bind(rp)})
for key in ['authoredCounts','representationCounts','additionalStandaloneEnvelopes']:ops.append({'pointer':'/'+key,'before':old[key],'after':idx[key]})
unchanged=0
for a,b in zip(old['entries'],idx['entries']):
 if a['id'] not in ids:assert a==b;unchanged+=1
reverse=copy.deepcopy(idx)
for op in reversed(ops):
 parts=op['pointer'].strip('/').split('/');v=reverse
 for k in parts[:-1]:v=v[int(k)] if isinstance(v,list) else v[k]
 k=int(parts[-1]) if isinstance(v,list) else parts[-1];assert v[k]==op['after'];v[k]=copy.deepcopy(op['before'])
assert reverse==old and unchanged==842
assert sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in idx['entries'])==616
for e in idx['entries']:
 if e['id'] in ids:
  p=(ip.parent/e['procedureFile']).resolve();v=read(p);assert ptr(v,e['wholeCardPointer'])['spellId']==e['id'];assert isinstance(ptr(v,e['procedureTextPointer']),str);assert len(ptr(v,e['sharedRulesPointer']))==6
out=enc(idx);write(D/'TRANSPORT6_INDEX_OPERATIONS_128.json',enc({'id':'TRANSPORT6-INDEX-APPLICATION-128','before':{'bytes':len(raw),'sha256':sha(raw),'backup':'authored_review_index.before_transport6_128.json'},'after':{'bytes':len(out),'sha256':sha(out)},'operations':ops,'reverseSemanticExact':True,'reverseByteExactBackup':True}))
assert ip.read_bytes()==raw;ip.write_bytes(out);assert read(ip)==idx
result={'id':'TRANSPORT6-APPLICATION-VALIDATION-128','passed':True,'acceptedIdentitiesApplied':6,'unrelatedIndexEntriesUnchanged':unchanged,'completeEvidenceFilesPreserved':49,'modelCasebookWorkAndHoldsByteExact':True,'forwardReverseIndexOperations':9,'counts':idx['authoredCounts'],'representationCounts':idx['representationCounts'],'index':bind(ip),'applicationReceipt':bind(rp),'acceptanceReceipt':bind(ap),'archive':bind(arc),'runtimeSelectionEnabled':False}
write(D/'TRANSPORT6_APPLICATION_VALIDATION_128.json',enc(result));print(json.dumps(result,indent=2))
