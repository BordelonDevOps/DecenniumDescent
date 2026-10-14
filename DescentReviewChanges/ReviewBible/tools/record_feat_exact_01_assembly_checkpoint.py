"""Checkpoint full feat assembly and remaining finite exact-acceptance work."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text('utf-8'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_TU6.json'
target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_ASSEMBLY.json';assert not target.exists()
state=read(previous);bp=A/'FEAT_EXACT_CANDIDATE_01_BUILD.json';vp=A/'FEAT_EXACT_CANDIDATE_01_STRUCTURE_CHECK.json';b=read(bp);v=read(vp)
assert b['failures']==v['failures']==0 and b['checks']==9061 and v['checks']==6826
assert v['candidateBuild']=={k:info(bp)[k] for k in ['bytes','sha256']}
for rel,binding in b['artifacts'].items():
    current=info(G/rel);assert all(current[k]==binding[k] for k in ['bytes','sha256']),rel
for folder in ['feat-exact-01-source-preservation','feat-exact-01-before-question-render-correction','navigation-before-feat-exact-01-assembly']:
    for rel,binding in read(A/folder/'PRESERVATION_MANIFEST.json').items():
        current=info(G/binding['preservedCopy']);assert all(current[k]==binding[k] for k in ['bytes','sha256']),rel
nav=read(A/'REVIEW_MAP_BUILD.json');assert nav['existingDistinctLinks']==770 and not nav['missingLinks']
assert info(G/'REVIEW_MAP.html')['sha256']==nav['sha256']
state.update({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'goalTurnClassification':'progress',
 'previousGoalTurnClassification':'progress: TU6 completed13 source proposals/26 cases; actual GPT FEAT327 source verdict downloaded, all28 payloads verified and3884 checks reproduced.',
 'previousCheckpoint':info(previous),
 'status':'Complete feat text/envelopes assembled from actual GPT source directions. All335 originals preserved, eight reviewed unchanged,325 procedures plus two null wrappers, full nine reader/audit chapters and660+28 casebook. Assembly and independent structure/projection checks pass. Finite FXC state-boundary acceptance work remains; candidate has not been submitted or approved.',
 'featExactCandidateAssembly':{'readerIndex':info(R/'docs/feats/exact-candidate-01/README.md'),
    'internalEnvelope':info(R/'data/director/feat_candidates/exact_01/candidate.json'),
    'publicEnvelope':info(R/'data/public/feat_candidates/exact_01/candidate.json'),
    'build':info(bp),'independentStructureCheck':info(vp),'assemblyChecks':9061,'independentChecks':6826,
    'completeProcedures':325,'nullWrappers':2,'unchangedReviewed':8,'originalRegistryEntries':335,
    'readerChapters':9,'sourceAuditChapters':9,'originalCases':660,'additionalAuthoredCases':28,
    'curriculumPlacements':1838,'ritualPlacements':7,'currentReviewedSpellReferences':282,'literalDeferredSpellReceipts':2,
    'sharedRules':16,'conventionDispositions':91,'fexResolutions':15,'sourceFieldOperations':67,
    'acquisitionInventory':info(A/'FEAT_EXACT_01_ACQUISITION_INVENTORY.json'),
    'distinctPrintedPrerequisiteValues':175,'prerequisiteSemanticsValidated':False,
    'readyForSubmission':False,'submitted':False,'exactApproved':False},
 'navigation':{'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':770,'missingLinks':[]},
 'safeNextActions':[
    'Continue complete finite FXC acceptance validation, not another source conference. Read FEAT_EXACT_CANDIDATE_01_STRUCTURE_CHECK.json remainingAcceptanceWork and the actual FXC-01–12 contract. All67 replacement operations, complete supplement operational values (except exhaustive1838 choice listing already bound), all15FEX, all16FS and all28FA expectations have now been read.',
    'Begin FXC-05 with exhaustive FEAT_EXACT_01_ACQUISITION_INVENTORY.json:335 IDs,175 distinct printed prerequisite values. Combine exact printed gates with actual final per-feat directions, six fixed training branches and twelve Warrior class-level/equipped/active identity pairs. Do not interpret inventory coverage as successful eligibility tests or invent an impossible all-heritage actor.',
    'Complete FXC-04–10 state boundaries using actual source-qualified actor/resource/body/clock fixtures: Endurance separate counters under canonical24/40/48/56-hour events; suppression/acquisition and safe rest; actual Mage3max8/Dragoon8max7/Warrior7zeroRP; percentage order and mixed typed allocation; strongest slows; persistent caltrops; ally/self/ranged breath; mount/companion/plant shared phases; whole-job30-minute repair; Haven/assay; paid copy vs echo; actual current Invisibility; ritual floors; mutation activity; source no-resource flags. Keep bounded reference checks distinct from authored full-game expectations/runtime.',
    'All exact candidate files are under data/director/feat_candidates/exact_01, data/public/feat_candidates/exact_01 and docs/feats/exact-candidate-01. Existing catalogs and original nine proposal files were not overwritten. The current public candidate includes335 original entries while only327 are newly directed; full reviewed eight records remain exact.',
    'The one-use builder completed after a structured-question rendering fix. Thirty-two partial files including the old builder were preserved under feat-exact-01-before-question-render-correction. Do not rerun its initial/resume mode over emitted outputs. Preserve exact current bytes and create a new correction receipt before later edits; existing build/source-verdict archives remain historical evidence.',
    'Independent validator imports no builder. It checks full field allowlists, whole procedure/case equality, all source/questions, original335/eight reviewed,91 conventions,67 operations,all supplement values,284 current spell envelopes including two null receipts,1845 exact grant placements and all688 casebook records. Its6826 passing checks do not close missing state-case work.',
    'Only after all finite acceptance evidence is complete, create a manifest-bound complete package and precise exact-candidate request for actual GPT Calibration Review Part2. Working browser handle featVerdictTab/tab125745656; original user tab125745612 left open. No request is currently in progress and no new GPT message was sent this turn.',
    'All180 higher-spell drafts still await dedicated actual GPT discussion;208 further pre-push procedures remain. Preserve47 higher deferred receipts plus Blink. Ordinary spells remain412 reviewed/436 pending. Other catalogs,whole-game flow,runtime/human gates remain open.',
    'After final actual joint whole-game agreement, perform the already-authorized GitHub push and verify remote commit. Only then carefully review cosmology. No source deletion or catalog promotion has occurred.'
 ]})
state['featSourceVerdict']['candidateAssembled']=True
state['featSourceVerdict']['candidateReadyForSubmission']=False
state['activeGptReview']['currentAuthoritativeObservation']='The source conference is completed and its returned archive verified. Full local candidate text is assembled; acceptance-state work precedes the next exact-review submission. No active unanswered GPT request.'
target.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checkpoint':info(target),'artifactsVerified':len(b['artifacts']),'navigationLinks':770,'readyForSubmission':False,'catalogPromotions':0,'sourceInformationDeleted':0},indent=2))
