"""Record completed EN6 authoring/navigation without adopting pending rules."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
R = G / 'DescentReviewChanges/ReviewBible'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}


target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EN6.json'
assert not target.exists(), 'Preserve the existing checkpoint; this is a one-use recorder.'
previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EV6.json'
state = read(previous)
receipt_path = A / 'ENCHANTMENT_RANK6_OPERATING_PROPOSAL_CHECK.json'
receipt = read(receipt_path)
index_path = A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'
index = read(index_path)
navigation = read(A / 'REVIEW_MAP_BUILD.json')
assert receipt['failures'] == index['failures'] == 0
assert index['counts']['completeUnadoptedProcedures'] == 138
assert not navigation['missingLinks']
assert navigation['existingDistinctLinks'] == 756
for rel, binding in {**receipt['artifacts'], **index['artifacts']}.items():
    actual = info(G / rel)
    assert actual['bytes'] == binding['bytes'] and actual['sha256'] == binding['sha256'], rel
assert info(G / navigation['artifact'])['sha256'] == navigation['sha256']
manifests = []
for folder in ['higher-spell-index-before-en6', 'navigation-before-en6-proposals']:
    p = A / folder / 'PRESERVATION_MANIFEST.json'
    for rel, binding in read(p).items():
        actual = info(G / binding['preservedCopy'])
        assert actual['bytes'] == binding['bytes'] and actual['sha256'] == binding['sha256'], rel
    manifests.append(info(p))
state.update({
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'goalTurnClassification': 'progress',
    'previousGoalTurnClassification': 'progress: eight EV6 procedures/16 examples, preserved source bindings and navigation completed.',
    'previousCheckpoint': info(previous),
    'status': 'Seven rank-six Enchantment procedures/14 examples completed and navigation refreshed. The same actual GPT feat continuation is active in the connector; the latest returned turn contains the continuation request and no final assistant verdict. The previously observed browser interruption is historical, not a new browser observation.',
    'newSpellCohort': {
        'reviewStatus': 'unadopted and not yet shared',
        'sourceIds': ['mass-charm', 'haze-of-forgetting', 'puppet-strings', 'willbreaker', 'mental-prison', 'mass-suggestion', 'irresistible-dance'],
        'completeProcedures': receipt['completeMechanicalProposals'],
        'authoredExamples': receipt['authoredExamples'],
        'untouchedPostPushReceipts': ['soul-cage'],
        'currentWholeCounterparts': receipt['completeCurrentCounterparts'],
        'reviewedCurrentCounterparts': receipt['reviewedCurrentCounterparts'],
        'pendingCurrentCounterparts': receipt['pendingCurrentCounterparts'],
        'earlierFullUnadoptedCounterparts': receipt['earlierFullUnadoptedCounterpartProposals'],
        'completeClassEnvelopes': receipt['completeComparisonClasses'],
        'newJointIssues': receipt['newJointIssues'],
        'checks': receipt['checks'],
        'plainArithmeticChecks': receipt['plainArithmeticChecks'],
        'boundedReferenceModelChecks': receipt['boundedReferenceModelChecks'],
        'fullSpellRuntimeCases': receipt['fullSpellRuntimeCases'],
        'receipt': info(receipt_path),
        'artifacts': receipt['artifacts']
    },
    'higherSpellCounts': index['counts'],
    'higherSpellIndex': info(R / 'data/director/higher_spell_operating_proposal_index.json'),
    'higherSpellIndexCheck': info(index_path),
    'indexChecks': index['checks'],
    'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'), 'links': navigation['existingDistinctLinks'], 'missingLinks': navigation['missingLinks']},
    'frozenVsCurrent': 'Original 707-payload feat ZIP unchanged. Higher index contains 138 unadopted procedures: 71 previously shared as feat comparisons and 67 unshared. EN6 adds seven. No dedicated higher-spell verdict. Previous index/navigation bytes preserved under higher-spell-index-before-en6 and navigation-before-en6-proposals.',
    'preservationManifests': manifests,
    'safeNextActions': [
        'Continue observing the existing GPT request a64ef367-c9d6-400f-8ba6-4a76dd7f8080; do not resend or restart merely because the connector returns a user-only turn.',
        'When an actual terminal feat verdict arrives, verify its complete evidence, all 327 dispositions and 15 FEX interfaces before implementing agreed changes.',
        'Continue the 250 remaining higher-spell mechanical procedures. Next: rank-six Illusion/Necromancy. Read complete sources/questions and governing counterparts before authoring.',
        'All 138 higher-spell proposals await dedicated actual GPT discussion. Ordinary spells remain 412 reviewed/436 pending; preserve 47 higher-spell post-push receipts and Blink.',
        'Do not rerun one-use cohort/index/navigation helpers over their outputs. Preserve current navigation before subsequent changes.',
        'Obtain actual final joint whole-game agreement before the authorized push; verify the remote commit before careful cosmology review.'
    ],
    'ownerAccessFailureClarification': 'The older expedition failure concerned missing GPT temporary draft files, with FileNotFoundError at the claimed paths; all 304 uploaded source payloads verified intact. EX58 was subsequently reconstructed and fulfilled. A separate later feat-review report describes unreadable file-tool results without an explicit missing-file or corruption error. No cause or repository damage is established by that report.'
})
state['activeGptReview']['currentAuthoritativeObservation'] = 'Connector read during this continuation reports Calibration Review Part 2 active; latest turn a64ef367-c9d6-400f-8ba6-4a76dd7f8080 contains the user continuation text, with no final assistant verdict returned. Previous Chrome Thinking/Stop/interrupted-connection observation remains historical.'
target.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'checkpoint': info(target), 'verifiedCohortAndIndexArtifacts': len(receipt['artifacts']) + len(index['artifacts']), 'preservationManifestsVerified': len(manifests), 'navigationLinks': navigation['existingDistinctLinks'], 'sourceInformationDeleted': 0, 'newRuleAdoptions': 0}, indent=2))
