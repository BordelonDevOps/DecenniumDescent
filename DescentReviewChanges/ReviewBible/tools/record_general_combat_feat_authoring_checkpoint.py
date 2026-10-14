"""Append a progress receipt without editing active expedition conference inputs."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
out=A/'EXPEDITION_ACTIVE_AUTHORING_CHECKPOINT_AFTER_GENERAL_COMBAT.json'
assert not out.exists()
proposal=read(A/'GENERAL_COMBAT_58_OPERATING_PROPOSAL_CHECK.json');index=read(A/'FEAT_OPERATING_PROPOSAL_INDEX_CHECK.json')
map_report=read(A/'REVIEW_MAP_BUILD.json');recovery=read(A/'EXPEDITION_V3_RECOVERY_REQUEST.json')
for receipt in [proposal,index]:
 assert receipt['failures']==0
 for path,expected in receipt['artifacts'].items():assert info(G/path)==expected,path
assert index['completeProposedProcedures']==245 and index['deferredPayloadGrantInterfaces']==2 and index['authoredExamples']==500
assert info(G/'REVIEW_MAP.html')['sha256']==map_report['sha256'] and not map_report['missingLinks']
for path,expected in read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
 if path!='README_EXPEDITION_INTEGRATED_V3.md':assert info(G/path)==expected,path
proof=A/'REVIEW_MAP_GENERAL_COMBAT_FEAT_PROPOSAL_BROWSER.png';assert proof.is_file()
result={
 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'Completed local general combat proposals and navigation update while actual expedition conference recovery remains live.',
 'gptThreadId':recovery['threadId'],'gptTitle':recovery['threadTitle'],'activeSavedRequest':recovery['requestId'],
 'activeRequestSentAtUtc':recovery['sentAtUtc'],
 'browserObservedAtUtc':'2026-10-11T15:04:00Z (approximately)',
 'browserObserved':'Live Thinking and Stop. File access recovered; submitted archive hash matched. Prior working directory absent. GPT reports first six authority/staffing/clock/Supply/procurement/Forage decisions saved and confirms Cult Escapee prose Disliked versus runtime religious-orders +1 conflict. No terminal58-question verdict or downloadable result yet.',
 'priorAccessFailurePreserved':'GPT_EXPEDITION_V3_ACCESS_FAILURE.md and EXPEDITION_V3_TERMINAL_RESPONSE.json retain the actual prior terminal reply; it is not a review verdict.',
 'sourceRecords':335,'reviewedFullFeats':8,'pendingFullFeats':327,
 'completeUnadoptedFeatProcedures':245,'deferredPayloadGrantOutlines':2,'sourceFeatsWithProposedTreatment':247,
 'remainingPreparedSourceOnly':80,'authoredExamples':500,'completeFeatRuntimeCases':0,
 'completedProposalCohorts':{'generalExploration':31,'skill':25,'crafting':24,'generalDefense':31,'magicCore':{'complete':29,'deferredGrantOnly':2},'combat':47,'generalCombat':58},
 'remainingCohorts':{'extendedMagic':58,'heritageMutation':22},
 'generalCombatProposal':{'completeProcedures':58,'authoredExamples':116,'finiteMagicInitiateCurricula':16,'realClassCurricula':14,
   'newLegacyCurricula':2,'fullCurrentSpellDependencies':275,'newAnimalProfiles':3,'newFeatManeuvers':6,
   'checks':proposal['checks'],'plainArithmeticChecks':proposal['plainArithmeticChecks'],'artifacts':proposal['artifacts']},
 'explicitProposedSourceDifferences':'Generic Magic Initiate expansion from the original six named choices to16 is explicitly NEW. The animal profile/bond and six-maneuver menu are new proposed completions, not recovered source rules. No source, public registry or class card was changed.',
 'selfReviewClarifications':'Preserved first five authoring files before clarifying owner-death animal profile restoration, already-issued commands during temporary owner incapacity, the NEW curriculum expansion and howling without articulated speech. Old files remain in general-combat-before-lifecycle-clarifications.',
 'nextHeritageInspection':'Read the22 exact source questions,12 Warrior counterparts and supplied ancestry evidence. No heritage operating proposal or source change has been authored. The active-versus-equipped distinction, restricted component-review scopes and standalone-versus-class conflicts require explicit reconciliation.',
 'supplementOutsideOriginal335':'One NEW unadopted Spell Focus prerequisite proposal remains separate from the original registry.',
 'indexChecks':index['checks'],'indexArtifacts':index['artifacts'],
 'reviewMap':{'sha256':map_report['sha256'],'bytes':map_report['bytes'],'links':map_report['existingDistinctLinks'],'missing':map_report['missingLinks']},
 'proof':{proof.relative_to(G).as_posix():info(proof)},
 'submittedCurrentFilesUnchanged':303,'archivePayloadFiles':304,'archiveReuploaded':False,'sourceInformationDeleted':0,'pushed':False,'cosmologyReviewed':False,
 'nextAction':'Prioritize the actual expedition terminal verdict and downloads when available; preserve/read every58 decision, then author the completed candidate for exact review. Meanwhile finish the remaining80 feat proposals outside frozen inputs. Reconcile with the real expedition decision and refresh the full feat packet before dispatch; do not send stalev2 as current.',
 'deliveryOrder':'Final joint whole-game flow agreement -> authorized GitHub push -> verified remote commit -> careful cosmology review',
 'frozenNavigationWarning':'START_HERE.md, GPT_REVIEW_CONTINUATION_HANDOFF.md and all303 submitted current files stay frozen. This appended checkpoint, feat index and map carry newer progress.',
 'goalAudit':'Meaningful independent authoring and verification completed. Current external review is live. Goal remains active, neither complete nor blocked.'
}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'checkpoint':str(out),'file':info(out),'completeProposals':245,'deferredOutlines':2,'authoredCases':500,'frozenFiles':303}))
