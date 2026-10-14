"""Record current acquisition work and the fulfilled actual GPT narrow addendum."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,subprocess,sys

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}

target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_ACQUISITION.json';assert not target.exists()
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_BOUNDARIES.json'
contracts=read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')
history=read(A/'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json')
fulfillment=read(A/'FEAT327_ACQ_01_DERIVED_FULFILLMENT.json');independent=read(A/'FEAT327_ACQ_01_INDEPENDENT_CHECK.json')
response=read(A/'FEAT327_ACQ_01_GPT_RESPONSE.json')
assert history['failureCount']==fulfillment['failureCount']==independent['failureCount']==0
assert response['status']=='completed' and response['replyId']=='70d1835d-4e41-41dd-9646-d07e22e442cc'
for b in history['sourceBindings']:assert info(G/b['path'])==b
for rel,b in fulfillment['measuredCurrentDescendants'].items():assert info(G/rel)==b
nav=R/'tools/build_review_map.py';s=nav.read_text('utf-8');anchor='    pending = [\n';assert s.count(anchor)==1
new=''.join(f'        ("{label}", "{name}"),\n' for label,name in [
 ('Feat prerequisites — all335 exact source contracts','FEAT_EXACT_01_ACQUISITION_CONTRACTS.md'),
 ('Feat acquisition history — current reference checks','FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json'),
 ('GPT weapon-prerequisite addendum — exact ruling','FEAT327_ACQ_01_GPT_ADDENDUM.md'),
 ('Weapon-prerequisite addendum — fulfilled derived correction','FEAT327_ACQ_01_DERIVED_FULFILLMENT.json'),
 ('Weapon-prerequisite correction — independent whole-file checks','FEAT327_ACQ_01_INDEPENDENT_CHECK.json')])
s=s.replace(anchor,anchor+new)
anchor='The remaining finite acceptance evidence, full package and actual exact review remain outstanding.';assert s.count(anchor)==1
s=s.replace(anchor,'All335 prerequisite identities are now normalized into175 exact printed forms with full original/procedure retention,12 shared Warrior paid identities and6 fixed training entries. Current acquisition-history evidence has897 passing checks (176 bounded reference,6 input integrity,36 source-data and679 source-integrity), without claiming full335 legal-actor coverage. Actual GPT addendum FEAT327-ACQ-01, reply70d1835d-4e41-41dd-9646-d07e22e442cc, closes the omitted weapon prerequisite bridge through one exact FS-02 paragraph and four convention references. Its finite130 checks and independent481 whole-file/source checks pass. Nine derived/audit descendants are bound with prior bytes preserved; the seven changed candidate files supersede their historical assembly hashes only through this measured correction receipt. Original objects, individual feat procedures, eight reviewed feats, null deferred payloads and comparison catalogs remain unchanged. The remaining finite acceptance evidence, full package and actual exact review remain outstanding.')
compile(s,str(nav),'exec')
folder=A/'navigation-before-feat-exact-01-acquisition';assert not folder.exists();manifest={}
for p in [nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
    b=info(p);q=folder/b['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert q.read_bytes()==p.read_bytes()
    manifest[b['path']]={**b,'preservedCopy':q.relative_to(G).as_posix()}
(folder/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
nav.write_text(s,encoding='utf-8',newline='\n')
ran=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
if ran.returncode:print(ran.stderr);raise SystemExit(ran.returncode)
n=read(A/'REVIEW_MAP_BUILD.json');assert not n['missingLinks'] and info(G/'REVIEW_MAP.html')['sha256']==n['sha256']
state=read(previous)
state.update({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'goalTurnClassification':'progress',
 'previousGoalTurnClassification':'progress:362 bounded/source checks across28 additional FA groups; no complete335 acquisition or660 example claim.',
 'previousCheckpoint':info(previous),
 'status':'All335 prerequisite contracts normalized; actual GPT weapon-bridge gap resolved through precise addendum and nine preserved derived/audit descendants.130 finite correction checks,481 independent whole-file/source checks and897 current acquisition-history checks pass. Exhaustive source-qualified actor fixtures and remaining FXC work still precede exact submission.',
 'featAcquisitionWork':{'contracts':info(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'),
   'manuscript':info(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md'),'counts':contracts['counts'],
   'historyCheck':info(A/'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json'),
   'historyChecks':history['checks'],'historyCheckKinds':history['checkKinds'],
   'all335ActualAcquisitionBoundaryCasesExecuted':False,'candidateReadyForSubmission':False,
   'notableBoundaries':'Class-specific Oracle4/8/14/19 and ordinary4/8/12/16/19; no total-level ASI shortcut; same opportunity/identity persists; twelve paid Warrior aliases only; actual separate Mage Elemental Affinity cannot be bought as a feat; pureASI full allocation; four repeatable identities; same-curriculum generic/named Initiate; six training snapshots; permanent skill/ability gates; fixed darkvision and finite-use histories.'},
 'featAcquisitionAddendum':{'id':'FEAT327-ACQ-01','request':info(A/'FEAT327_ACQUISITION_BRIDGE_EXACT_QUESTION.txt'),
   'requestId':response['requestId'],'replyId':response['replyId'],'response':info(A/'FEAT327_ACQ_01_GPT_RESPONSE.json'),
   'addendum':info(A/'FEAT327_ACQ_01_GPT_ADDENDUM.md'),'screenshot':info(A/'FEAT327_ACQ_01_GPT_VERDICT.png'),
   'fulfillment':info(A/'FEAT327_ACQ_01_DERIVED_FULFILLMENT.json'),'independentCheck':info(A/'FEAT327_ACQ_01_INDEPENDENT_CHECK.json'),
   'finiteChecks':130,'independentChecks':481,'sourceExpectations':9,'onlyThisNamedIssueClosed':True,
   'measuredCurrentDescendants':fulfillment['measuredCurrentDescendants'],'originalSourceArchiveUnchanged':True,
   'separateNormalizationFix':'Dragon Blood actual recorded damage type now explicitly required on either lineage branch under its existing source-directed procedure.',
   'verificationRecovery':'Initial apply wrote9 correct descendants then hit a local verifier variable-shadowing error. All10 intermediate files/script preserved under feat-acq01-before-verifier-variable-correction; fixed verifier resumed read-only comparison with --verify-already-applied, no repeated mutation.130 and independent481 checks then passed.'},
 'navigation':{'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':n['existingDistinctLinks'],'missingLinks':[]}})
state['activeGptReview'].update({'requestId':response['requestId'],'replyId':response['replyId'],'requestStatus':'completed',
 'finalVerdictScope':'Narrow source correction FEAT327-ACQ-01 only, now fulfilled locally; whole feat exact review remains pending.',
 'currentAuthoritativeObservation':'Actual GPT completed the weapon bridge addendum and named finite fulfillment path. All operations and checks completed locally. No active unanswered request.',
 'awaitingGptResponse':False,'liveObservation':info(A/'FEAT327_ACQ_01_GPT_RESPONSE.json')})
state['featExactCandidateAssembly']['currentDescendantBindingReceipt']=info(A/'FEAT327_ACQ_01_DERIVED_FULFILLMENT.json')
state['featExactCandidateAssembly']['historicalAssemblyHashesRemainPreserved']=True
state['safeNextActions']=[
 'Prioritize complete FXC-05 legal-actor boundary cases using FEAT_EXACT_01_ACQUISITION_CONTRACTS.json:335IDs/175printed forms. The normalization and897 acquisition-history checks do not prove all335 actor prerequisites. Require real class level/opportunity, actual ability/skill/proficiency/source receipt, legal mutation slots and AND/OR branch histories; no all-heritage test actor.',
 'The actual GPT gap FEAT327-ACQ-01 is already resolved, applied and independently checked. No pending weapon-bridge question remains. FS-02 includes exact proficiency/profile classification; nine affected records plus explicit neighboring cases keep original use-time exceptions.17 normalized weapon contracts reference the addendum. Do not reopen this generic issue.',
 'Use FEAT327_ACQ_01_DERIVED_FULFILLMENT.json measuredCurrentDescendants as the authoritative override for7 changed candidate files and2 acquisition-audit files. Original final archive/verdict/register and all other candidate artifacts remain unchanged. The original assembly,structure andfirst28FA reports are historical before this legitimate derived correction. Do not rerun their old binding checks blindly or rewrite old hashes.',
 'The independent ACQ descendant validator reconstructs exact whole-file differences from preserved inputs;481 checks pass. Current acquisition-history report897 passes and binds current model/validator/contracts/cohorts. Each supports only its stated scope; none promotes the candidate or proves all660 authored cases.',
 'Pure source normalization also added Dragon Blood’s existing final recorded-damage-type prerequisite to both ancestry branches. Its original object and full procedure are unchanged. The earlier history identity-only placeholder was replaced with a real verified Mage Elemental Affinity comparison, and the model now rejects class IDs as feat purchases except12 explicit aliases.',
 'Remaining FXC-04–10: all finite supplement operative qualification; full acquisition fixtures including eight reviewed and all named choices; task/natural-shift/opposed/save/reroll, native damage/healing/causal source budgets; actual physical/social premises; casting/Ready/concentration/ritual/QuickenedThought/plant/Trapcasting sequences;660 original case premise audit. Preserve scope and distinguish source adjudication from executed bounded models.',
 'Do not rerun one-use builders/apply scripts over emitted files. Initial ACQ apply hit a verifier variable-name error after correct writes; intermediate files were preserved. Corrected --verify-already-applied finished by comparison only and its final receipt now exists; independent validator passes. Further reruns need new report paths, not overwritten evidence.',
 'When finite acceptance evidence is complete, package full exact files and issue actual GPT exact review to Calibration Review Part2, thread6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b. Working browserfeatVerdictTab/tab125745656; original user tab125745612 left open. Last newrequestf00740d3-9ccb-47b1-b808-347818c0e1d5 completed withreply70d1835d-4e41-41dd-9646-d07e22e442cc. No active unanswered request; do not resend.',
 'Higher spells remain180 complete unadopted proposals/360examples with208 additional pre-push procedures; all need dedicated GPT review. Preserve47 higher deferred receipts plus Blink. Ordinary spells412reviewed/436pending. Other catalogs,whole-game flow and human/runtime gates remain open.',
 'Final actual joint whole-game confirmation precedes already-authorized GitHub push and verified remote commit; cosmology only afterward. No source deletion,promotion,push or cosmology review occurred.'
]
for name in ['feat-exact-01-before-acq01','feat-acq01-before-verifier-variable-correction','navigation-before-feat-exact-01-acquisition']:
    state.setdefault('preservationManifests',[]).append(info(A/name/'PRESERVATION_MANIFEST.json'))
target.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checkpoint':info(target),'navigationLinks':n['existingDistinctLinks'],'sourceCorrectionFulfilled':True,'candidateReadyForSubmission':False,'wholeGameComplete':False},indent=2))
