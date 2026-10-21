from pathlib import Path
import json,hashlib,re,datetime
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';P=A/'feat335-assembly-106'
OUT=A/'FEAT335_ACCEPTANCE_EVIDENCE_MAP_107.json';assert not OUT.exists()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def binding(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def evidence(p,pointer,scope):
    obj=j(p)
    for key in pointer.strip('/').split('/') if pointer else []:obj=obj[int(key)] if isinstance(obj,list) else obj[key]
    return {'binding':binding(p),'pointer':pointer,'scope':scope,'doesNotInferRuntimeOrGateAcceptance':True}
contract=A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md'
text=contract.read_text(encoding='utf-8-sig')
parts=re.split(r'^## (FXC-\d+) — ([^\n]+)\n',text,flags=re.M)
requirements={parts[i]:{'title':parts[i+1],'completeOriginalRequirement':parts[i+2].strip()} for i in range(1,len(parts),3)}
assert len(requirements)==12
cohort=j(A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_105.json')
case_reports=[evidence(G/r['path'],'','Complete preserved authored cohort review; original cases and bounded calculations remain separately labeled.') for r in cohort['reviewReports']]
assembly=evidence(P/'ASSEMBLY_REPORT.json','','Current derived335 identity/source/text/mirror assembly;3149 checks, no parent acceptance.')
acquisition=evidence(A/'feat335-acquisition-106/EVIDENCE_REPORT.json','','Current335 acquisition entries,177 allowance descriptors and15 exact historical evidence files;1976 reference/mirror checks.')
dependency=evidence(A/'feat335-spell-dependencies-107/AUDIT_REPORT.json','','All1845 selected placements exact;283of284 complete dependency cards match; Planar Binding reference requires explicit reconciliation.')
time=evidence(A/'FEAT335_TIME_PROVISIONS_CASES_83.json','/cases','28 bounded Endurance/provision/rest/forage cases; source/world premises explicit.')
work=evidence(A/'FEAT335_WORK_COMPOSITIONS_84.json','/cases','78 historical work cases; read with subsequent FT84 decisions, not as acceptance of superseded choices.')
ft84=evidence(A/'FEAT335_FT84_DERIVED_MIRROR_RECONCILIATION_92.json','','Six accepted FT84 successors carried in derived full files; original operations and limited acceptance retained.')
resolution=evidence(A/'FEAT335_RESOLUTION_CASES_85.json','/cases','36 bounded roll/numeric cases; native operations and real qualifications remain in full sources.')
healing=evidence(A/'FEAT335_HEALING_COMPOSITIONS_89.json','/cases','56 bounded healing compositions; nested dispatch/runtime and actual world histories not implied.')
physical=evidence(A/'FEAT335_PHYSICAL_SOCIAL_COMPOSITIONS_91.json','/cases','77 physical/social cases:76 calculations and one source-adjudicated scheduler case.')
copy=evidence(A/'copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json','','Exact owner-selected COPY-READY-ALLOWANCE-02; paid preparation only, actual Reaction release, original deadlines.')
originals=evidence(P/'after/data/director/feat_candidates/exact_01/candidate.json','/records','All327 exact original objects/questions/source decisions/current procedures; historical sourceDirection preserved.')
conventions=evidence(P/'after/data/director/feat_candidates/exact_01/convention_dispositions.json','/entries','All91 complete original convention dispositions.')
fex=evidence(P/'after/data/director/feat_candidates/exact_01/fex_dispositions.json','/issues','All15 full original FEX questions and resolutions.')
conflicts=evidence(P/'after/data/director/feat_candidates/exact_01/source_conflict_dispositions.json','/conflicts','All159 preserved conflict entries; original text remains, current superseding procedures separately identified.')
supp=evidence(P/'after/data/public/feat_candidates/exact_01/supplements.json','/groups','Full explicit allowlist of9 finite supplement groups; current7copy profiles include concentration, family, strain and preparation-only policy.')
cases=evidence(P/'ALL_CASE_REVIEWS.json','','Complete660 original positions and28 boundaries joined to exact complete authored reviews; no runtime inference.')
proposal=evidence(A/'feat335-spell-dependencies-107/PLANAR_DEPENDENCY_PROPOSAL.json','','Complete before/current/proposed Planar Binding references; null feat preserved; no source or106 modification yet.')
rows={
'FXC-01':([assembly,originals], 'Complete identity/source assembly evidenced; parent verdict remains separate.', [], 'LOCAL_SOURCE_AND_IDENTITY_EVIDENCE_COMPLETE'),
'FXC-02':([assembly,ft84,copy,proposal], 'Full nine current chapters and source-audit chapters exist; copied-feat and mental predicate mirrors resolved in106.', ['Carry any agreed107 dependency-status correction through full private/public procedures, source-audit/current manuscripts and acquisition mirrors without overwriting source history.'], 'CURRENT_REFERENCE_CORRECTION_OPEN'),
'FXC-03':([conventions,fex,conflicts]+case_reports, 'Original conventions/conflicts remain complete. Cohort reports supply current family/stacking/counterpart adjudications.', ['Finish explicit field-to-current-procedure map for the eight named extended-magic conflicts and twelve Warrior counterpart pairs before claiming the whole gate fulfilled.'], 'EVIDENCE_ASSEMBLED_FIELD_MAP_PENDING'),
'FXC-04':([supp,dependency]+case_reports, 'All named finite tables exist;1845 actual selected class/rank/school rows pass current-source equality. Deferred wrappers are absent from those selected rows.', ['Resolve current ordinary Planar Binding reference while retaining separate null feat boundary.','Finalize the finite-table operation/lifecycle evidence mapping; table existence alone is not full procedure acceptance.'], 'BOUNDED_DEPENDENCY_QUESTION_OPEN'),
'FXC-05':([acquisition]+case_reports, 'All335 current acquisition records,177 descriptors and15 historical source-qualified evidence files are preserved. Three copy allowance descriptors now follow preparation-only policy.', ['Join each finite acquisition branch to current requirements, class tables and retained history evidence; preserve existing credential qualifications.','Do not treat all335FullAcquisitionsExecuted=false as runtime evidence or fabricate campaign receipts to make it true.'], 'CURRENT_EVIDENCE_MAPPING_PENDING'),
'FXC-06':([time,work,ft84]+case_reports, 'Endurance/provision/rest cases and work compositions are supplied; six later FT84 procedures control current work timing.', ['Mark exact historical work outcomes superseded by FT84 and point to accepted replacement cases; do not infer all old78 pass unchanged.'], 'SUPERSESSION_MAP_PENDING'),
'FXC-07':([resolution,healing]+case_reports, 'Bounded numeric/calculation and full stated-case reviews cover the named roll, damage and healing families with actual qualifications.', ['Finish named-boundary evidence map and preserve the declared limitation on combined healing dispatch versus isolated vectors.'], 'BOUNDARY_MAP_PENDING'),
'FXC-08':([physical]+case_reports, 'Full caltrop sequence, locks, transport, social/fee cases and later cohort readings are preserved.', ['Finish exact source/event mapping for all named physical/social requirements; FP91-M13 remains source-adjudicated, not scheduler execution.'], 'BOUNDARY_MAP_PENDING'),
'FXC-09':([copy,supp,acquisition]+case_reports, 'Current copy/Ready policy, all7profiles and finite commands are assembled. Existing four helpers remain unchanged and cannot establish Ready implementation.', ['Map full current authored copy/command/ritual/Quickened/plant cases, including valid competing-use premises and original deadlines.','Treat old helper results and 71 higher drafts only in their exact historical/comparison scope.'], 'CURRENT_CASE_MAP_PENDING'),
'FXC-10':([cases]+case_reports, 'All660 original positions and28 added boundaries have complete preserved semantic reviews, with bounded arithmetic separately recorded.', [], 'LOCAL_FULL_STATED_CASE_REVIEW_COMPLETE'),
'FXC-11':([assembly,supp,dependency,proposal], 'Explicit public allowlist reconstruction equals selected public operative sources;335 identities preserved, two null wrappers and disabled selection remain.', ['Reconcile the later ordinary Planar Binding record without treating it as automatic feat acceptance or changing deferred flags.'], 'DEPENDENCY_PRESENTATION_OPEN'),
'FXC-12':([assembly,acquisition,dependency], 'Actual packages, manifests, full sources and new data-only reproduction scripts exist. Parent exact request has not been sent.', ['Complete the remaining finite gate mappings, incorporate agreed corrections and bind one final candidate plus exact evidence package before requesting acceptance.','Keep actual runtime/human/balance/publication/whole-game gates distinct. Joint whole-game agreement and verified GitHub push must precede cosmology review.'], 'FINAL_SUBMISSION_OPEN')}
gates=[]
for ident,req in requirements.items():
    ev,assessment,remaining,status=rows[ident]
    gates.append({'id':ident,**req,'currentEvidence':ev,'assessment':assessment,'remaining':remaining,'status':status,'exactGateAccepted':False})
group={x['id']:x['value'] for x in j(P/'after/data/public/feat_candidates/exact_01/supplements.json')['groups']}
finite={'curricula':len(group['SUP-04']),'animalChassis':len(group['SUP-02']),'maneuvers':len(group['SUP-03']),'gadgets':len(group['SUP-08']),'borrowedStunts':len(group['SUP-09']),'copyProfiles':len(group['SUP-07']['copyProfileContract']['profiles']),'plantModes':len(group['SUP-07']['floraBody']['modes']),'pactSigils':len(group['SUP-07']['pactSigils']),'minorBuffTransfers':len([k for k in group['SUP-07']['minorBuffTransfer'] if k!='finalClarification']),'timeTags':len(group['SUP-07']['timeTagOverlay']['spellIds']),'natureRoutes':len(group['SUP-07']['naturePredicate']['castingClassRoutes']),'ritualPlacements':len(group['SUP-06'])}
expected={'curricula':16,'animalChassis':3,'maneuvers':6,'gadgets':4,'borrowedStunts':12,'copyProfiles':7,'plantModes':3,'pactSigils':3,'minorBuffTransfers':3,'timeTags':3,'natureRoutes':3,'ritualPlacements':7};assert finite==expected
report={'id':'FEAT335-FXC-EVIDENCE-MAP-107','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'contract':binding(contract),
    'classification':'Requirement/evidence map, not a new blanket semantic verdict. Statuses deliberately distinguish complete local evidence from remaining exact fulfillment.',
    'gates':gates,'finiteTableCounts':finite,'historicalOrdinaryCountsInContract':{'reviewed':412,'pending':436,'disposition':'Preserved historical wording; does not override current525/323 authored index or53accepted-unapplied.'},
    'currentIndex':binding(G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'),
    'fullGoalStillOpen':True,'allFXCGatesFulfilled':False,'canonicalApplied':False,'historicalProgramsRerun':False,'runtimeExecuted':False,'cosmologyReviewed':False}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'map':binding(OUT),'gates':len(gates),'finiteTableCounts':finite,'allFXCGatesFulfilled':False}))
