import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / 'docs/unity/evidence/2026-11-23-int05-admitted-command-surface'
ART = Path(__file__).resolve().parent
PAIRS = [
    ('outer-admission-cross-review-01.json', 'OUTER_ADMISSION_CROSS_REVIEW_01.json', '1592ee93289c437282ad1d311850ee1030a8a80b757c1ae380e7e80afdb9adca'),
    ('all-profile-read-copy-audit.json', 'ALL_PROFILE_READ_COPY_AUDIT.json', '72e70517282c9d63f4978296c38e86c0d9155661cd31023e81f9776f3d220280'),
]
for original, retained, expected in PAIRS:
    data = (ART / original).read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    assert actual == expected, original
    (PACKET / retained).write_bytes(data)
    print(f'{retained}: {actual}')

handoff_path = ROOT / 'engine/artifacts/connected-work-control/CURRENT_WORK_HANDOFF.json'
handoff = json.loads(handoff_path.read_text(encoding='utf-8-sig'))
review = json.loads((PACKET / 'GPT_ARCHITECTURE_REVIEW_07.json').read_text(encoding='utf-8'))
handoff['pendingGptRequest'] = None
handoff['pendingGptReview'] = None
handoff['latestActualInt05Review'] = {k: review[k] for k in ['requestId', 'responseId', 'status', 'scope']}
handoff['pendingIndependentAudit'] = {
    'audit_magic': 'Magic/care exact branch qualification plan; all-profile condition/input closure retained.',
    'audit_management': 'Frozen owned-lot-unit cross-review then management/work exact branch qualification plan.',
    'review_consecration': 'Finite safe V1 denial vocabulary; outer admission cross-review retained.',
}
handoff['currentDesignWork'] = {
    'valueDefinitions': 1097, 'operationFieldReferences': 2850,
    'exampleCandidateKinds': 78, 'operatorKinds': 2, 'exampleVariants': 145, 'candidateAxes': 204,
    'runtimeStarted': False, 'sourceApiAccepted': False,
    'completed': 'GPT07 bounded representations retained; all-family examples reconciled; outer admission and all-profile condition/input closure independently reviewed.',
    'next': 'Correct exact owned-lot unit field applicability; finish finite branch/profile/five-path allocations and public denial codes; actual complete HC review before runtime.',
}
handoff_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
