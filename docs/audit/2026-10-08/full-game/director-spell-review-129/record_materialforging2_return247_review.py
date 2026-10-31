from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = BASE / 'rank9_materialforging2_return247_received'
TARGET = ['eternal-forge', 'matter-conversion']
BLOCKERS = {'eternal-forge': ['MF210-B01'], 'matter-conversion': ['MF210-B02']}
NEXT = {'group': 'rank9-alignment-faction-purification5', 'pendingIds': [
    'alignment-ascension', 'alignment-perfection', 'faction-incarnate', 'faction-perfection', 'corruption-purification']}
STATUS = 'RETURN247_AUDITED_HELD_NEXT_ALIGNMENT_FACTION_PURIFICATION5_811_37_0'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def info(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest(), 'crc32': f'{zlib.crc32(raw) & 0xffffffff:08x}'}


def main():
    audit_path = BASE / 'RANK9MATERIALFORGING2_RETURN247_INDEPENDENT_AUDIT.json'
    receipt_path = BASE / 'RANK9MATERIALFORGING2_RETURN247_RECEIPT.json'
    audit, receipt = read(audit_path), read(receipt_path)
    assert audit['status'] == receipt['status'] == 'PASS'
    assert audit['checkCount'] == audit['passedChecks'] == 19 and audit['failedChecks'] == 0
    archive = RECEIVED / 'DD_Rank9_MaterialForging2_Director_Return247_HELD.zip'
    delivery = RECEIVED / 'DD_Rank9_MaterialForging2_Director_Return247_DELIVERY.json'
    delivery_body = read(delivery)
    assert delivery_body['heldIds'] == TARGET and delivery_body['blockerIds'] == ['MF210-B01', 'MF210-B02']
    assert delivery_body['nextPendingGroup']['group'] == NEXT['group']
    assert delivery_body['nextPendingGroup']['pendingIds'] == NEXT['pendingIds']
    archive_info, delivery_info = info(archive), info(delivery)
    audit_info, receipt_info = info(audit_path), info(receipt_path)
    qualifications = delivery_body['qualificationIds']
    now = datetime.now(timezone.utc).isoformat()

    submission_path = BASE / 'RANK9MATERIALFORGING2_PACKET_247_SUBMISSION.json'
    submission = read(submission_path)
    assert submission['browserVerified'] is True
    submission.update({'status': STATUS, 'return': 247, 'returnArchive': archive_info,
                       'returnDeliveryManifest': delivery_info, 'returnAudit': audit_info,
                       'returnAuditReceipt': receipt_info, 'acceptedIds': [], 'appliedIds': [],
                       'heldIds': TARGET, 'blockers': BLOCKERS,
                       'conditionalQualifications': qualifications, 'nextGroup': NEXT,
                       'returnedAtUtc': now, 'canonicalChanges': False, 'githubChanges': False})
    write(submission_path, submission)

    packet_path = BASE / 'RANK9MATERIALFORGING2_PACKET_247.json'
    packet = read(packet_path)
    packet.update({'status': STATUS, 'return': 247, 'returnArchive': archive_info,
                   'returnDeliveryManifest': delivery_info, 'returnAudit': audit_info,
                   'returnAuditReceipt': receipt_info, 'acceptedIds': [], 'appliedIds': [],
                   'heldIds': TARGET, 'blockers': BLOCKERS, 'nextGroup': NEXT})
    write(packet_path, packet)

    pending_path = BASE / 'CURRENT37_PENDING_IDENTITY_AUDIT_247.json'
    pending = read(pending_path)
    pending.update({'recordedAtUtc': now, 'status': STATUS, 'acceptedIds': [],
                    'appliedIds': [], 'heldIds': TARGET,
                    'lastDirectorReturn': {'return': 247, 'group': 'rank9-material-forging2',
                        'targetIds': TARGET, 'acceptedIds': [], 'appliedIds': [], 'heldIds': TARGET,
                        'blockers': BLOCKERS, 'conditionalQualifications': qualifications,
                        'independentAudit': audit_info, 'receipt': receipt_info,
                        'archive': archive_info, 'deliveryManifest': delivery_info, 'nextGroup': NEXT},
                    'preparedNextGroup': {'group': NEXT['group'], 'pendingIds': NEXT['pendingIds'],
                        'pendingCount': len(NEXT['pendingIds']), 'status': 'DIRECTOR_SELECTED_NEXT_AFTER_RETURN247',
                        'freshPacketRequiredForCurrentAuthority': True}})
    write(pending_path, pending)

    submission_info = info(submission_path)
    queue_path = BASE / 'CURRENT_SPELL_QUEUE_247.json'
    queue = read(queue_path)
    queue.update({'recordedAtUtc': now, 'status': STATUS, 'packetStatus': STATUS,
                  'pendingIdentityAudit': info(pending_path), 'currentSubmission': submission_info,
                  'currentReturnAudit': audit_info, 'currentReturnAuditReceipt': receipt_info,
                  'currentReturnBinding': archive_info, 'currentReturnDelivery': delivery_info,
                  'nextGroup': NEXT['group'], 'nextPendingIds': NEXT['pendingIds'],
                  'currentReturnAcceptedIds': [], 'currentReturnAppliedIds': [],
                  'currentReturnHeldIds': TARGET, 'currentReturnBlockers': BLOCKERS,
                  'currentReturn': archive_info, 'currentReturnAuditStatus': 'PASS',
                  'currentReturnAuditChecks': 19, 'currentReturnAuditFailures': 0, 'githubChanges': False})
    for row in queue.get('currentPendingGroups', []):
        if row.get('group') == 'rank9-material-forging2':
            row.update({'status': STATUS, 'heldIds': TARGET, 'blockers': BLOCKERS})
        if row.get('group') == NEXT['group']:
            row.update({'status': 'DIRECTOR_SELECTED_NEXT_AFTER_RETURN247',
                        'freshPacketRequiredForCurrentAuthority': True})
    write(queue_path, queue)

    handoff_path = BASE / 'CURRENT_HANDOFF_247.json'
    handoff = read(handoff_path)
    handoff.update({'recordedAtUtc': now, 'status': STATUS, 'pendingIdentityAudit': info(pending_path),
                    'queue': info(queue_path), 'currentQueueBinding': info(queue_path),
                    'currentSubmission': submission_info, 'currentReturnAudit': audit_info,
                    'currentReturnAuditReceipt': receipt_info, 'currentReturnBinding': archive_info,
                    'currentReturnDelivery': delivery_info, 'currentReturnArchive': archive_info,
                    'currentReturn': archive_info, 'currentReturnAuditStatus': 'PASS',
                    'currentReturnAuditChecks': 19, 'currentReturnAuditFailures': 0,
                    'latestBatch': {'return': 247, 'group': 'rank9-material-forging2', 'ids': TARGET,
                        'acceptedIds': [], 'appliedIds': [], 'heldIds': TARGET, 'blockers': BLOCKERS,
                        'conditionalQualifications': qualifications, 'independentAudit': audit_info,
                        'receipt': receipt_info},
                    'nextGroup': NEXT['group'], 'nextPendingIds': NEXT['pendingIds'],
                    'nextPendingCount': len(NEXT['pendingIds']),
                    'nextStep': 'Prepare a fresh current-source packet for rank9-alignment-faction-purification5; preserve the two Material Forging holds and all other holds, independently audit GPT’s sealed return, and apply only exact accepted IDs.',
                    'resumePriority': 'Return247 passed 19 independent checks. Eternal Forge remains held under MF210-B01: the sword and bracelet use traces pass, but actual damage plus repair/sale, and the complete charged-item transfer/dawn/suppression/recast lifecycles remain incomplete. Matter Conversion remains held under MF210-B02: no physical output profile/compatible recipe or complete paid conversion encounter has been shown. Authority remains 811/37/0. Continue with the five AFP identities.'})
    write(handoff_path, handoff)

    snapshot = BASE / 'CURRENT_SPELL_REVIEW_SNAPSHOT_247.md'
    snapshot.write_text(
        '# Current Ordinary Spell Review Snapshot 247\n\n'
        'Return247 was independently audited PASS 19/19. Eternal Forge remains held under MF210-B01: source item profiles, repair and charge rules, and paid casting/use traces are established, but actual weapon damage followed by lawful repair/sale and the complete charged-item transfer/dawn/suppression/recast lifecycle are still missing. Matter Conversion remains held under MF210-B02: the mithril price row does not establish physical output or recipe compatibility, and the required paid conversion encounters remain incomplete. No acceptance or application occurred.\n\n'
        'Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied** (535 complete standalone procedures; 173 scoped interfaces). GPT selected **Rank9 Alignment/Faction/Purification5** next: alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection, and corruption-purification. The Soul Reflection hold under IR207-B02 and all other unrelated holds remain preserved.\n\n'
        'No canonical changes, GitHub changes, runtime execution, implementation approval, human playtest, balance, cosmology, domain closure, completion, or release approval are inferred.\n', encoding='utf-8')

    start = ROOT / 'START_HERE.md'
    lines = start.read_text(encoding='utf-8-sig').splitlines()
    lines[0] = (f"**Current ordinary spell-review handoff [248](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_248.json):** "
                 f"Return247 is independently audited PASS 19/19; eternal-forge and matter-conversion remain held under MF210-B01/B02. Authority is **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. "
                 f"Preparing a fresh current-source packet248 for the five alignment/faction/purification identities; preserve both Material Forging holds and all unrelated holds.")
    start.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(json.dumps({'status': STATUS, 'archive': archive_info, 'delivery': delivery_info,
                      'audit': audit_info, 'receipt': receipt_info, 'acceptedIds': [],
                      'appliedIds': [], 'heldIds': TARGET, 'blockers': BLOCKERS,
                      'nextGroup': NEXT, 'queue': info(queue_path), 'handoff': info(handoff_path)}, indent=2))


if __name__ == '__main__':
    main()
