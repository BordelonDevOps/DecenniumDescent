"""Record current local progress without editing any frozen conference payload."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
out=A/'EXPEDITION_ACTIVE_AUTHORING_CHECKPOINT_AFTER_COMBAT.json'
assert not out.exists()
magic=read(A/'MAGIC_CORE_31_OPERATING_PROPOSAL_CHECK.json')
combat=read(A/'COMBAT_47_OPERATING_PROPOSAL_CHECK.json')
index=read(A/'FEAT_OPERATING_PROPOSAL_INDEX_CHECK.json')
map_report=read(A/'REVIEW_MAP_BUILD.json')
recovery=read(A/'EXPEDITION_V3_RECOVERY_REQUEST.json')
for c in [magic,combat,index]:assert c['failures']==0
for rel,expected in read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
 if rel!='README_EXPEDITION_INTEGRATED_V3.md':assert info(G/rel)==expected,rel
for c in [magic,combat,index]:
 for rel,expected in c['artifacts'].items():assert info(G/rel)==expected,rel
assert info(G/'REVIEW_MAP.html')['sha256']==map_report['sha256']
assert index['completeProposedProcedures']==187 and index['deferredPayloadGrantInterfaces']==2 and index['authoredExamples']==384
result={
 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'Substantive magic/combat authoring progress; same expedition source conference is now in a live recovery continuation.',
 'gptThreadId':recovery['threadId'],'gptTitle':recovery['threadTitle'],'activeSavedRequest':recovery['requestId'],
 'activeRequestSentAtUtc':recovery['sentAtUtc'],
 'originalRequest':'999dd180-8e31-48be-ad59-58f8f65e1a1c',
 'originalTerminalReply':'7ae8c2b8-9405-419c-8f74-be88505b96bb',
 'originalTerminalOutcome':'Retained304-payload validation and book inspection; file tools failed after long work; no complete58-question verdict or final evidence files returned. Actual full reply and browser capture preserved.',
 'recoveryBrowserObserved':'Stop control and live Thinking. GPT reports file access recovered, archive hash matches, but prior working directory absent; reconstructing from unchanged attachment and saving outputs incrementally. Latest visible progress included supply accounting and logistics.',
 'connectorObserved':'Saved recovery user message verified byte-equivalent after trailing-newline normalization; synchronized idle user-only snapshot is not treated as a final response.',
 'sourceRecords':335,'reviewedFullFeats':8,'pendingFullFeats':327,
 'completeUnadoptedFeatProcedures':187,'deferredPayloadGrantOutlines':2,'sourceFeatsWithProposedTreatment':189,'authoredExamples':384,
 'remainingPreparedSourceOnly':138,
 'proposalCohorts':{'generalExploration':31,'skill':25,'crafting':24,'generalDefense':31,'magicCore':{'complete':29,'deferredGrantOnly':2},'combat':47},
 'remainingCohorts':{'extendedMagic':58,'heritageMutation':22,'generalCombat':58},
 'supplementsOutside335OriginalSourceFeats':{'newUnadoptedSpellFocusPrerequisite':1,'publicRegistryChanged':False},
 'magicChecks':magic['checks'],'magicPlainArithmeticChecks':magic['plainArithmeticChecks'],'magicReviewedComponentQueries':magic['existingReviewedComponentQueries'],
 'combatChecks':combat['checks'],'combatPlainArithmeticChecks':combat['plainArithmeticChecks'],'completeFeatRuntimeCases':0,
 'indexChecks':index['checks'],'allCurrentChecksFailures':0,
 'magicArtifacts':magic['artifacts'],'combatArtifacts':combat['artifacts'],'indexArtifacts':index['artifacts'],
 'sureShotCorrection':'Physical suit contribution excludes DEX and magic enhancement; leather11+DEX5 AC16 compares at15, not14. Complete old draft/data/manuscript/receipt/builder preserved in combat-feats-before-armor-attribution-correction. All94 examples retained; one arithmetic assertion added.',
 'reviewMap':{'sha256':map_report['sha256'],'bytes':map_report['bytes'],'links':map_report['existingDistinctLinks'],'missing':map_report['missingLinks']},
 'proofs':['docs/audit/2026-10-08/full-game/EXPEDITION_V3_RECOVERY_REQUEST_BROWSER.png','docs/audit/2026-10-08/full-game/REVIEW_MAP_COMBAT_FEAT_PROPOSAL_BROWSER.png'],
 'submittedCurrentFilesUnchanged':303,'archivePayloadFiles':304,'archiveReuploaded':False,'sourceInformationDeleted':0,'pushed':False,'cosmologyReviewed':False,
 'nextAction':'Prioritize the actual final expedition verdict and downloads when available: preserve and verify full package, read every58 decision, reconcile actual source conflicts, then author completed candidate chapters and records for exact review. Meanwhile finish the remaining138 original feat procedures where not cosmology-dependent. Before feat dispatch, reconcile all327 original pending entries and current proposals against the actual expedition verdict and refresh the full-file packet; never send the stalev2feat archive as current.',
 'deliveryOrder':'Final joint whole-game flow agreement -> authorized GitHub push -> verified remote commit -> careful cosmology review',
 'frozenNavigationWarning':'START_HERE.md, GPT_REVIEW_CONTINUATION_HANDOFF.md and all303 submitted current payloads remain frozen. This checkpoint, the feat index and review map carry newer work.',
 'goalAudit':'Meaningful independent authoring occurred and file access has recovered. No repeated unavoidable blocking condition; goal remains active, not complete.'
}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'checkpoint':str(out),'file':info(out),'completeProposals':187,'deferredOutlines':2,'authoredCases':384,'frozenFiles':303}))
