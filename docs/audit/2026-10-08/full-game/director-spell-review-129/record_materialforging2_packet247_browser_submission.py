from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT = BASE / 'rank9_materialforging2_current_source_247_prepared'
CHAT = 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def info(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest(), 'crc32': f'{zlib.crc32(raw) & 0xffffffff:08x}'}


def main():
    packet = read(BASE / 'RANK9MATERIALFORGING2_PACKET_247.json')
    audit = read(BASE / 'RANK9MATERIALFORGING2_PACKET_247_INDEPENDENT_AUDIT.json')
    receipt = read(BASE / 'RANK9MATERIALFORGING2_PACKET_247_RECEIPT.json')
    assert packet['status'] == 'PREPARED_AND_INDEPENDENTLY_AUDITED_UNSENT'
    assert packet['pendingIds'] == ['eternal-forge', 'matter-conversion']
    assert audit['status'] == receipt['status'] == 'PASS' and audit['checkCount'] == 16
    now = datetime.now(timezone.utc).isoformat()
    attached = [
        OUT / 'DD_Rank9_MaterialForging2_CurrentSource_247.zip',
        OUT / 'DD_Rank9_MaterialForging2_CurrentSource_247_DELIVERY.json',
        BASE / 'RANK9MATERIALFORGING2_PACKET_247_INDEPENDENT_AUDIT.json',
        BASE / 'RANK9MATERIALFORGING2_PACKET_247_RECEIPT.json',
    ]
    status = 'PACKET247_SUBMITTED_GPT_PENDING_811_37_0'
    submission_path = BASE / 'RANK9MATERIALFORGING2_PACKET_247_SUBMISSION.json'
    submission = {
        'id': 'RANK9MATERIALFORGING2-PACKET-247-SUBMISSION', 'recordedAtUtc': now,
        'status': status, 'group': packet['group'], 'targetIds': packet['pendingIds'],
        'authority': packet['sourceAuthority'], 'archive': packet['archive'],
        'deliveryManifest': packet['deliveryManifest'], 'independentAudit': info(BASE / 'RANK9MATERIALFORGING2_PACKET_247_INDEPENDENT_AUDIT.json'),
        'auditReceipt': info(BASE / 'RANK9MATERIALFORGING2_PACKET_247_RECEIPT.json'),
        'auditStatus': 'PASS', 'auditChecks': 16, 'auditFailures': 0,
        'acceptedIds': [], 'appliedIds': [], 'heldIds': [],
        'destination': 'GPT director conversation', 'conversationId': '6adc506d-8770-83ea-b64c-0345d9b9b682',
        'browserVerified': True, 'attachedFiles': [info(path) for path in attached],
        'submittedAtUtc': now, 'followUpPingsSent': 0, 'githubChanges': False,
        'browserEvidence': {'conversationTitle': 'Calibration review part 6', 'conversationUrl': CHAT,
                            'attachedFilesVisible': [path.name for path in attached],
                            'submittedMessageVisible': True, 'directorStatusVisible': 'Working'},
    }
    write(submission_path, submission)
    submission_info = info(submission_path)

    packet_path = BASE / 'RANK9MATERIALFORGING2_PACKET_247.json'
    packet = read(packet_path)
    packet.update({'status': status, 'submission': submission_info})
    write(packet_path, packet)

    pending_path = BASE / 'CURRENT37_PENDING_IDENTITY_AUDIT_247.json'
    pending = read(pending_path)
    pending.update({'recordedAtUtc': now, 'status': status})
    pending['preparedNextGroup'].update({'status': status, 'submittedAtUtc': now,
                                         'submission': submission_info})
    pending['lastSubmittedPacket'] = {'group': packet['group'], 'targetIds': packet['pendingIds'],
                                      'archive': packet['archive'], 'deliveryManifest': packet['deliveryManifest'],
                                      'independentAudit': submission['independentAudit'], 'receipt': submission['auditReceipt'],
                                      'acceptedIds': [], 'appliedIds': [], 'submittedAtUtc': now,
                                      'status': status, 'submission': submission_info}
    write(pending_path, pending)
    pending_info = info(pending_path)

    queue_path = BASE / 'CURRENT_SPELL_QUEUE_247.json'
    queue = read(queue_path)
    queue.update({'recordedAtUtc': now, 'status': status, 'packetStatus': status,
                  'pendingIdentityAudit': pending_info, 'currentSubmission': submission_info,
                  'submittedAtUtc': now, 'githubChanges': False})
    write(queue_path, queue)

    handoff_path = BASE / 'CURRENT_HANDOFF_247.json'
    handoff = read(handoff_path)
    handoff.update({'recordedAtUtc': now, 'status': status, 'pendingIdentityAudit': pending_info,
                    'queue': info(queue_path), 'currentQueueBinding': info(queue_path),
                    'currentSubmission': submission_info, 'submittedAtUtc': now,
                    'nextStep': 'Packet247 is submitted to GPT for exactly eternal-forge and matter-conversion. Monitor the browser, independently audit the sealed return, and apply only exact accepted IDs.'})
    write(handoff_path, handoff)

    print(json.dumps({'status': status, 'browserVerified': True, 'submittedAtUtc': now,
                      'submission': submission_info, 'pendingAudit': pending_info,
                      'queue': info(queue_path), 'handoff': info(handoff_path)}, indent=2))


if __name__ == '__main__':
    main()
