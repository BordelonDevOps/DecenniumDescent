"""Record TU6 authoring and the downloaded, reproduced GPT feat source verdict."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text('utf-8'))
def info(p):
    b=p.read_bytes()
    return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_TU6.json'
assert not target.exists(),'One-use checkpoint; preserve existing output.'
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DI6.json'
state=read(previous)
rp=A/'TRANSMUTATION_UNIVERSAL_RANK6_OPERATING_PROPOSAL_CHECK.json';receipt=read(rp)
ip=A/'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json';index=read(ip)
np=A/'REVIEW_MAP_BUILD.json';navigation=read(np)
data=read(R/'data/director/spell_proposals/transmutation_universal_rank6.json')
assert receipt['failures']==index['failures']==0
assert receipt['checks']==675 and receipt['completeMechanicalProposals']==13 and receipt['authoredExamples']==26
assert index['counts']['completeUnadoptedProcedures']==180 and index['counts']['mechanicalProceduresStillToPropose']==208
assert not navigation['missingLinks'] and navigation['existingDistinctLinks']==767
for rel,binding in {**receipt['artifacts'],**index['artifacts']}.items():
    actual=info(G/rel);assert all(actual[k]==binding[k] for k in ['bytes','sha256']),rel
assert info(G/navigation['artifact'])['sha256']==navigation['sha256']
manifests=[]
for folder in ['higher-spell-index-before-tu6','navigation-before-tu6-proposals','navigation-before-feat327-source-verdict']:
    p=A/folder/'PRESERVATION_MANIFEST.json'
    for rel,binding in read(p).items():
        actual=info(G/binding['preservedCopy']);assert all(actual[k]==binding[k] for k in ['bytes','sha256']),rel
    manifests.append(info(p))
response=read(A/'FEAT327_SOURCE_VERDICT_RESPONSE.json')
download=read(A/'FEAT327_SOURCE_VERDICT_DOWNLOAD_CHECK.json')
repro=read(A/'FEAT327_SOURCE_VERDICT_LOCAL_REPRODUCTION.json')
assert response['replyId']==download['sourceReply']=='b50ec7da-7a7c-4975-82bb-b99d10a24134'
assert repro['checks']==repro['passed']==3884 and repro['failed']==0
verdict=A/'feat327-source-verdict'
for name,binding in download['files'].items():
    actual=info(verdict/name);assert all(actual[k]==binding[k] for k in ['bytes','sha256']),name
assert info(Path(download['archive']))['sha256']==download['archiveSha256']
state.update({
    'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
    'goalTurnClassification':'progress',
    'previousGoalTurnClassification':'progress: DI6 authored five procedures/ten examples; previous navigation preserved and map verified.',
    'previousCheckpoint':info(previous),
    'status':'Thirteen TU6 procedures/twenty-six examples completed locally, unadopted and unsent. Actual GPT feat source conference has now completed; its archive and all28 payloads verified, all3884 source/reference checks reproduced locally. Next work is the complete exact feat candidate under FXC-01–12, not another generic source conference. No catalog promotion or final whole-game approval.',
    'newSpellCohort':{
        'reviewStatus':'unadopted and not yet shared',
        'sourceIds':[p['spellId'] for p in data['records']],
        'completeProcedures':13,'authoredExamples':26,'untouchedPostPushReceipts':[],
        'currentWholeCounterparts':21,'reviewedCurrentCounterparts':11,'pendingCurrentCounterparts':10,
        'earlierFullUnadoptedCounterparts':10,'completeClassEnvelopes':17,'newJointIssues':17,
        'checks':675,'plainArithmeticChecks':39,'boundedReferenceModelChecks':0,'fullSpellRuntimeCases':0,
        'receipt':info(rp),'artifacts':receipt['artifacts'],
        'currentCounterpartCorrection':info(A/'TU6_CURRENT_COUNTERPART_CORRECTION.json')},
    'higherSpellCounts':index['counts'],
    'higherSpellIndex':info(R/'data/director/higher_spell_operating_proposal_index.json'),
    'higherSpellIndexCheck':info(ip),'indexChecks':index['checks'],
    'navigation':{'map':info(G/'REVIEW_MAP.html'),'receipt':info(np),'links':767,'missingLinks':[]},
    'frozenVsCurrent':'The original707-payload feat ZIP remains immutable. Higher index has180 unadopted procedures:71 shared only as feat comparisons and109 unshared. TU6 adds13. All await dedicated higher-spell review. Prior index/navigation bytes were preserved before both TU6 and terminal feat-verdict updates.',
    'preservationManifests':manifests,
    'featSourceVerdict':{
        'reviewId':'FEAT327-SOURCE-2026-10-11','replyId':response['replyId'],
        'response':info(A/'FEAT327_SOURCE_VERDICT_RESPONSE.json'),
        'archive':info(Path(download['archive'])),'downloadCheck':info(A/'FEAT327_SOURCE_VERDICT_DOWNLOAD_CHECK.json'),
        'localReproduction':info(A/'FEAT327_SOURCE_VERDICT_LOCAL_REPRODUCTION.json'),
        'payloadsVerified':28,'allExtractedMembersVerified':29,'localChecks':3884,'localFailures':0,
        'retainedProcedures':275,'revisedProcedures':50,'deferredNullWrappers':2,
        'exactFieldOperations':67,'originalExamplePositions':660,'correctedExamples':26,'additionalAuthoredCases':28,
        'sharedRules':16,'mappedConventionFields':91,'fexResolutions':15,
        'acceptanceContract':info(verdict/'FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md'),
        'candidateAssembled':False,'exactCandidateApproved':False,'catalogPromoted':False},
    'safeNextActions':[
        'Assemble the complete exact feat candidate under the actual FEAT327 source verdict and FXC-01–12 contract. The full verdict, contract and all16 FS rules were read. Read all67 field operations and finite supplement values as implemented; preserve old derived files before writing any descendants.',
        'Return all327 original IDs/questions/source objects,325 full procedures/two null wrappers,all335 original registry entries/eight reviewed unchanged,all91 convention dispositions/15FEX resolutions,complete supplement tables and full660+28 casebook. Generate full nine manuscripts and independently allowlisted internal/public candidates; do not substitute excerpt or title equality.',
        'Use actual current reviewed spell descendants for every curriculum/ritual placement, including standalone LRX operationalCandidate records. Do not use stale legacy operational=null as evidence of missing completed procedures. Keep original/public source mentions and private dossier membership boundaries distinct.',
        'Execute finite acquisition/capacity/time/Endurance/body/command/copy/settlement checks from FXC. Separate executed bounded calculations from authored adjudications and full runtime/human tests. Preserve all EX58 and previously fulfilled scopes.',
        'Submit the complete manifest-bound exact feat candidate to the same real GPT thread once locally ready. The source conference is completed; do not resend its old continuation or claim the exact review has happened.',
        'Use working Chrome tab125745656/featVerdictTab for next browser work; original user tab125745612 remains open but DOM observation timed out. The new tab successfully read the final response and downloaded the archive into Downloads. The browser download-event wait timed out even though the file arrived and verified.',
        'Continue208 remaining pre-push higher spell procedures after the active feat integration. All180 drafts still need dedicated actual GPT discussion; ordinary spells stay412 reviewed/436 pending. Preserve47 higher deferred receipts plus Blink.',
        'Do not rerun one-use TU6/navigation/checkpoint helpers over outputs. Old sources, before-correction builder, navigation and original returned verdict bytes are preserved.',
        'Final actual joint whole-game agreement precedes authorized GitHub push; verify remote commit before careful cosmology review. No deletion, catalog promotion, runtime/human approval or cosmology change occurred.'
    ],
    'ownerAccessFailureClarification':'The earlier failure was unreadable GPT temporary-workspace file-tool results, not loss of C:\\Github\\DecenniumDescent. GPT later reported restored access and a fresh707-payload verification. Its completed source-verdict archive was independently downloaded/hash-verified and its3884 read-only source/reference checks reproduced locally. No local source files were deleted.'
})
state['activeGptReview'].update({
    'tabId':'125745656','originalUserTabId':'125745612','requestStatus':'completed','replyId':response['replyId'],
    'currentAuthoritativeObservation':'Actual completed terminal source-authoring verdict received via read_thread and fresh Chrome DOM. Archive and all28 payloads verified locally;3884 checks reproduced. Complete assembled exact-candidate review remains outstanding.',
    'finalVerdictReceived':True,'finalVerdictScope':'source-authoring conference only; exact-candidate review pending',
    'liveObservation':info(A/'FEAT327_SOURCE_VERDICT_RESPONSE.json'),
    'browserScreenshot':info(A/'FEAT327_SOURCE_VERDICT_BROWSER.png'),
    'awaitingGptResponse':False
})
target.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checkpoint':info(target),'cohortChecks':675,'indexChecks':index['checks'],'navigationLinks':767,'verdictPayloadsVerified':28,'localReproductionChecks':3884,'sourceInformationDeleted':0,'catalogPromotions':0},indent=2))
