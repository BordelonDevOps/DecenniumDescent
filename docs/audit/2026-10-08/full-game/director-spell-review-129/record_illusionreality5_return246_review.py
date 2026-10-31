from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = BASE / 'rank9_illusionreality5_return246_received'
TARGET = ['soul-reflection']
BLOCKERS = {'soul-reflection': ['IR207-B02']}
NEXT = {'group': 'rank9-material-forging2', 'pendingIds': ['eternal-forge', 'matter-conversion']}
QUALIFICATIONS = [
    'IR207-H-SOURCE', 'IR207-H-CONTENT', 'IR207-H-PHYSICAL', 'IR207-H-NULL-SCENE',
    'IR207-Q-RUNTIME', 'IR207-Q-IMPLEMENTATION', 'IR207-Q-PLAY', 'IR207-Q-BALANCE',
    'IR207-Q-COSMOLOGY', 'IR207-Q-DOMAIN', 'IR207-Q-COMPLETION', 'IR207-Q-RELEASE',
    'IR207-H-REFLECTION-PROFILES',
]
STATUS = 'RETURN246_AUDITED_HELD_NEXT_MATERIAL_FORGING2_811_37_0'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def info(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest(), 'crc32': f'{zlib.crc32(raw) & 0xffffffff:08x}'}


def main():
    audit_path = BASE / 'RANK9ILLUSIONREALITY5_RETURN246_INDEPENDENT_AUDIT.json'
    receipt_path = BASE / 'RANK9ILLUSIONREALITY5_RETURN246_RECEIPT.json'
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit['status'] == receipt['status'] == 'PASS'
    assert audit['checkCount'] == audit['passedChecks'] == 16 and audit['failedChecks'] == 0
    archive = RECEIVED / 'DD_Rank9_SoulReflection_Director_Return246_HELD.zip'
    delivery = RECEIVED / 'DD_Rank9_SoulReflection_Director_Return246_DELIVERY.json'
    archive_info, delivery_info = info(archive), info(delivery)
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    now = datetime.now(timezone.utc).isoformat()

    submission_path = BASE / 'RANK9ILLUSIONREALITY5_PACKET_246_SUBMISSION.json'
    submission = read(submission_path)
    assert submission['browserVerified'] is True
    submission.update({
        'status': STATUS, 'return': 246, 'returnArchive': archive_info,
        'returnDeliveryManifest': delivery_info, 'returnAudit': audit_info,
        'returnAuditReceipt': receipt_info, 'acceptedIds': [], 'appliedIds': [],
        'heldIds': TARGET, 'blockers': BLOCKERS, 'conditionalQualifications': QUALIFICATIONS,
        'nextGroup': NEXT, 'returnedAtUtc': now, 'canonicalChanges': False, 'githubChanges': False,
    })
    write(submission_path, submission)

    packet_path = BASE / 'RANK9ILLUSIONREALITY5_PACKET_246.json'
    packet = read(packet_path)
    packet.update({'status': STATUS, 'return': 246, 'returnArchive': archive_info,
                   'returnDeliveryManifest': delivery_info, 'returnAudit': audit_info,
                   'returnAuditReceipt': receipt_info, 'acceptedIds': [], 'appliedIds': [],
                   'heldIds': TARGET, 'blockers': BLOCKERS, 'nextGroup': NEXT})
    write(packet_path, packet)

    pending_path = BASE / 'CURRENT37_PENDING_IDENTITY_AUDIT_246.json'
    pending = read(pending_path)
    pending.update({
        'recordedAtUtc': now, 'status': STATUS, 'acceptedIds': [], 'appliedIds': [], 'heldIds': TARGET,
        'lastDirectorReturn': {
            'return': 246, 'group': 'rank9-illusion-reality5', 'targetIds': TARGET,
            'acceptedIds': [], 'appliedIds': [], 'heldIds': TARGET, 'blockers': BLOCKERS,
            'conditionalQualifications': QUALIFICATIONS, 'independentAudit': audit_info,
            'receipt': receipt_info, 'archive': archive_info, 'deliveryManifest': delivery_info,
            'nextGroup': NEXT,
        },
        'preparedNextGroup': {'group': NEXT['group'], 'pendingIds': NEXT['pendingIds'],
                              'pendingCount': len(NEXT['pendingIds']),
                              'status': 'DIRECTOR_SELECTED_NEXT_AFTER_RETURN246',
                              'freshPacketRequiredForCurrentAuthority': True},
    })
    write(pending_path, pending)

    submission_info = info(submission_path)
    queue_path = BASE / 'CURRENT_SPELL_QUEUE_246.json'
    queue = read(queue_path)
    queue.update({
        'recordedAtUtc': now, 'status': STATUS, 'packetStatus': STATUS,
        'pendingIdentityAudit': info(pending_path), 'currentSubmission': submission_info,
        'currentReturnAudit': audit_info, 'currentReturnAuditReceipt': receipt_info,
        'currentReturnBinding': archive_info, 'currentReturnDelivery': delivery_info,
        'nextGroup': NEXT['group'], 'nextPendingIds': NEXT['pendingIds'],
        'currentReturnAcceptedIds': [], 'currentReturnAppliedIds': [],
        'currentReturnHeldIds': TARGET, 'currentReturnBlockers': BLOCKERS,
        'currentReturn': archive_info, 'currentReturnAuditStatus': 'PASS',
        'currentReturnAuditChecks': 16, 'currentReturnAuditFailures': 0,
        'githubChanges': False,
    })
    for row in queue.get('currentPendingGroups', []):
        if row.get('group') == 'rank9-illusion-reality5':
            row.update({'status': STATUS, 'heldIds': TARGET, 'blockers': BLOCKERS})
        if row.get('group') == NEXT['group']:
            row.update({'status': 'DIRECTOR_SELECTED_NEXT_AFTER_RETURN246',
                        'freshPacketRequiredForCurrentAuthority': True})
    write(queue_path, queue)

    handoff_path = BASE / 'CURRENT_HANDOFF_246.json'
    handoff = read(handoff_path)
    handoff.update({
        'recordedAtUtc': now, 'status': STATUS, 'pendingIdentityAudit': info(pending_path),
        'queue': info(queue_path), 'currentQueueBinding': info(queue_path),
        'currentSubmission': submission_info, 'currentReturnAudit': audit_info,
        'currentReturnAuditReceipt': receipt_info, 'currentReturnBinding': archive_info,
        'currentReturnDelivery': delivery_info, 'currentReturnArchive': archive_info,
        'currentReturn': archive_info, 'currentReturnAuditStatus': 'PASS',
        'currentReturnAuditChecks': 16, 'currentReturnAuditFailures': 0,
        'latestBatch': {
            'return': 246, 'group': 'rank9-illusion-reality5', 'ids': TARGET,
            'acceptedIds': [], 'appliedIds': [], 'heldIds': TARGET, 'blockers': BLOCKERS,
            'conditionalQualifications': QUALIFICATIONS, 'independentAudit': audit_info,
            'receipt': receipt_info,
        },
        'nextGroup': NEXT['group'], 'nextPendingIds': NEXT['pendingIds'],
        'nextPendingCount': len(NEXT['pendingIds']),
        'nextStep': 'Prepare a fresh current-source packet for Eternal Forge and Matter Conversion; preserve the Soul Reflection hold, independently audit GPT’s sealed return, and apply only exact accepted IDs.',
        'resumePriority': 'Return246 passed 16 independent checks. Soul Reflection remains held under IR207-B02 because changed-form, attached/no-phase, original-target zero/death, copied concentration ending, and entrusted original-cargo witnesses remain missing. Authority stays 811/37/0. Continue with rank9-material-forging2.',
    })
    write(handoff_path, handoff)

    snapshot = BASE / 'CURRENT_SPELL_REVIEW_SNAPSHOT_246.md'
    snapshot.write_text(
        '# Current Ordinary Spell Review Snapshot 246\n\n'
        'Return246 was independently audited PASS 16/16. Soul Reflection remains held under IR207-B02: the return demonstrated that the ten preserved case replays pass, but the integrated changed-form, attached/no-phase, original-target zero/death, copied concentration ending, and entrusted original-cargo witnesses are still absent. No acceptance or application occurred.\n\n'
        'Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied** (535 complete standalone procedures; 173 scoped interfaces). GPT selected **Rank9 Material Forging2** next: `eternal-forge` and `matter-conversion`, reassessing MF210-B01 and MF210-B02 against refreshed current sources. Return245’s reverse-gravity-field hold under IE204-B02 and all other unrelated holds remain preserved.\n\n'
        'No canonical changes, GitHub changes, runtime execution, implementation approval, human playtest, balance, cosmology, domain closure, completion, or release approval are inferred.\n', encoding='utf-8')

    start = ROOT / 'START_HERE.md'
    lines = start.read_text(encoding='utf-8-sig').splitlines()
    lines[0] = (f"**Current ordinary spell-review handoff [247](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_247.json):** "
                 f"Return246 is independently audited PASS 16/16; soul-reflection remains held under IR207-B02. Authority is **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. "
                 f"Preparing a fresh current-source packet247 for only eternal-forge and matter-conversion; preserve both MF210 holds and all unrelated holds.")
    start.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(json.dumps({'status': STATUS, 'archive': archive_info, 'delivery': delivery_info,
                      'audit': audit_info, 'receipt': receipt_info,
                      'acceptedIds': [], 'appliedIds': [], 'heldIds': TARGET, 'blockers': BLOCKERS,
                      'nextGroup': NEXT, 'queue': info(queue_path), 'handoff': info(handoff_path)}, indent=2))


if __name__ == '__main__':
    main()
