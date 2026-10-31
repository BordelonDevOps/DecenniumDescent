from __future__ import annotations

import hashlib
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = AUDIT / 'rank9_illusionreality5_return246_received'
ARCHIVE = RECEIVED / 'DD_Rank9_SoulReflection_Director_Return246_HELD.zip'
DELIVERY = RECEIVED / 'DD_Rank9_SoulReflection_Director_Return246_DELIVERY.json'
SOURCE_PACKET = AUDIT / 'rank9_illusionreality5_current_source_246_prepared/DD_Rank9_IllusionReality5_CurrentSource_246.zip'
SOURCE_DELIVERY = AUDIT / 'rank9_illusionreality5_current_source_246_prepared/DD_Rank9_IllusionReality5_CurrentSource_246_DELIVERY.json'
SOURCE_AUDIT = AUDIT / 'RANK9ILLUSIONREALITY5_PACKET_246_INDEPENDENT_AUDIT.json'
SOURCE_RECEIPT = AUDIT / 'RANK9ILLUSIONREALITY5_PACKET_246_RECEIPT.json'
QUEUE = AUDIT / 'CURRENT_SPELL_QUEUE_246.json'
REPORT = AUDIT / 'RANK9ILLUSIONREALITY5_RETURN246_INDEPENDENT_AUDIT.json'
RECEIPT = AUDIT / 'RANK9ILLUSIONREALITY5_RETURN246_RECEIPT.json'
AUTH = {'reviewedApplied': 811, 'pending': 37, 'acceptedUnapplied': 0,
        'completeStandaloneProcedures': 535, 'scopedInterfaces': 173}
TARGET = ['soul-reflection']
BLOCKER = ['IR207-B02']
NEXT = {'group': 'rank9-material-forging2', 'pendingIds': ['eternal-forge', 'matter-conversion']}


def digest(path: Path):
    h = hashlib.sha256(); crc = 0; size = 0
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block); crc = zlib.crc32(block, crc); size += len(block)
    return size, h.hexdigest(), f'{crc & 0xffffffff:08x}'


def member_digest(z: zipfile.ZipFile, name: str):
    h = hashlib.sha256(); crc = 0; size = 0
    with z.open(name) as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block); crc = zlib.crc32(block, crc); size += len(block)
    return size, h.hexdigest(), f'{crc & 0xffffffff:08x}'


def readj(z, name):
    return json.loads(z.read(name).decode('utf-8-sig'))


def add(checks, name, passed, detail=None):
    checks.append({'check': name, 'passed': bool(passed), 'detail': detail})


def main():
    checks = []
    delivery = json.loads(DELIVERY.read_text(encoding='utf-8-sig'))
    packet_audit = json.loads(SOURCE_AUDIT.read_text(encoding='utf-8-sig'))
    packet_receipt = json.loads(SOURCE_RECEIPT.read_text(encoding='utf-8-sig'))
    archive_n, archive_sha, archive_crc = digest(ARCHIVE)
    delivery_n, delivery_sha, delivery_crc = digest(DELIVERY)
    source_n, source_sha, source_crc = digest(SOURCE_PACKET)
    source_delivery_n, source_delivery_sha, source_delivery_crc = digest(SOURCE_DELIVERY)

    add(checks, 'Return246 archive bytes, SHA-256 and CRC32 match its delivery binding',
        (archive_n, archive_sha, archive_crc) ==
        (delivery['archive']['bytes'], delivery['archive']['sha256'], delivery['archive']['crc32'].lower()),
        {'bytes': archive_n, 'sha256': archive_sha, 'crc32': archive_crc})
    add(checks, 'The submitted delivery manifest is preserved and independently hashed',
        delivery['id'] == 'RETURN246-DELIVERY' and delivery_n > 0,
        {'bytes': delivery_n, 'sha256': delivery_sha, 'crc32': delivery_crc})
    add(checks, 'Return246 is bound to the independently audited and received Packet246 source archive',
        (source_n, source_sha, source_crc) ==
        (delivery['externalSourceArchive']['bytes'], delivery['externalSourceArchive']['sha256'], delivery['externalSourceArchive']['crc32'].lower())
        and packet_audit['status'] == packet_receipt['status'] == 'PASS'
        and packet_audit['archive']['sha256'] == source_sha
        and packet_receipt['archive']['sha256'] == source_sha
        and packet_audit['delivery']['sha256'] == source_delivery_sha
        and packet_receipt['delivery']['sha256'] == source_delivery_sha
        and source_delivery_n > 0 and source_delivery_crc,
        {'sourceBytes': source_n, 'sourceSha256': source_sha, 'packetAudit': packet_audit['status'], 'sourceDeliverySha256': source_delivery_sha})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        rows = {row['path']: row for row in delivery['members']}
        unsafe = [name for name in names if '\\' in name or PurePosixPath(name).is_absolute()
                  or '..' in PurePosixPath(name).parts or name.startswith('/')]
        add(checks, 'ZIP contains exactly 71 unique safe members matching the sealed allowlist',
            len(names) == len(set(names)) == delivery['memberCount'] == 71
            and set(names) == set(delivery['exactAllowlist']) == set(rows)
            and not unsafe and z.testzip() is None,
            {'members': len(names), 'allowlist': len(rows), 'unsafePaths': unsafe[:5]})

        failures = []
        for name, row in rows.items():
            actual = member_digest(z, name)
            if actual != (row['bytes'], row['sha256'], row['crc32'].lower()):
                failures.append(name)
            info = z.getinfo(name)
            if info.CRC != int(row['crc32'], 16):
                failures.append(name + ':central-crc')
        add(checks, 'Every archive member matches the external delivery size/SHA/CRC and ZIP CRC',
            not failures, {'checked': len(rows), 'failures': failures[:10]})

        internal = readj(z, 'MEMBER_MANIFEST.json')
        internal_rows = {row['path']: row for row in internal['members']}
        payload = set(names) - {'MEMBER_MANIFEST.json'}
        self_binding = internal.get('selfBinding')
        internal_bytes, internal_sha, internal_crc = member_digest(z, 'MEMBER_MANIFEST.json')
        add(checks, 'Internal manifest has an exact payload inventory and valid self-binding',
            internal['memberCountExcludingSelf'] == 70 and set(internal_rows) == payload
            and self_binding == 'Bound by the external delivery and ZIP central directory, excluded only from its own list.'
            and rows['MEMBER_MANIFEST.json']['bytes'] == internal_bytes
            and rows['MEMBER_MANIFEST.json']['sha256'] == internal_sha
            and rows['MEMBER_MANIFEST.json']['crc32'].lower() == internal_crc,
            {'payload': len(payload), 'manifestRows': len(internal_rows), 'selfSha256': internal_sha})
        bad_internal = [name for name, row in internal_rows.items()
                        if member_digest(z, name) != (row['bytes'], row['sha256'], row['crc32'].lower())]
        add(checks, 'Every payload member also matches the internal manifest', not bad_internal,
            {'checked': len(internal_rows), 'failures': bad_internal[:10]})

        decision = readj(z, 'DIRECTOR_DECISION.json')
        counts = readj(z, 'COUNTS.json')
        semantic = readj(z, 'INDEPENDENT_SEMANTIC_FAILURE_CHECK.json')
        replay = readj(z, 'CASE_REPLAY.json')
        preservation = readj(z, 'PRESERVATION.json')
        next_group = readj(z, 'NEXT_PENDING_GROUP.json')
        source_reassessment = readj(z, 'SOURCE_REASSESSMENT.json')
        data = readj(z, 'DATA_INTEGRITY_CHECK.json')
        validation = readj(z, 'VALIDATION.json')

        add(checks, 'Decision holds only Soul Reflection with no acceptance or application and unchanged authority',
            delivery['authority'] == AUTH and delivery['accepted'] is False and delivery['applied'] is False
            and delivery['acceptedIds'] == delivery['appliedIds'] == [] and delivery['held'] is True
            and delivery['heldIds'] == TARGET and delivery['blockerIds'] == BLOCKER
            and decision['scope'] == TARGET and decision['authority'] == AUTH
            and decision['accepted'] is False and decision['applied'] is False
            and decision['heldIds'] == TARGET and decision['canonicalFilesChanged'] is False
            and decision['githubChanges'] is False,
            {'authority': delivery['authority'], 'heldIds': delivery['heldIds'], 'blockers': delivery['blockerIds']})
        identity = decision['perIdentity'][0]
        missing = identity['minimumMissingWitnesses']
        expected = ['changed-form recipient', 'attached/no-phase recipients', 'original target zero/death settlement',
                    'concentration ending', 'entrusted original cargo']
        add(checks, 'IR207-B02 remains grounded in the five exact missing lifecycle witnesses',
            identity['spellId'] == TARGET[0] and identity['blockerIds'] == BLOCKER
            and [x['component'] for x in missing] == expected
            and semantic['wholeSpellResult'] == 'HELD_IR207_B02'
            and semantic['dataReplayResult'] == 'PASS'
            and semantic['blocker']['id'] == 'IR207-B02'
            and semantic['numericSuccessIsNotSemanticCompletion'] is True,
            {'witnessComponents': [x['component'] for x in missing]})
        cases = replay['cases']
        add(checks, 'All ten preserved cases replay with no replay failures while the whole spell stays held',
            len(cases) == counts['targetCasesReplayed'] == 10
            and all(row.get('freshReplay') == 'PASS' for row in cases)
            and replay['auxiliaryNullHistoryReplay'].get('freshReplay') == 'PASS',
            {'cases': len(cases), 'allPassed': all(row.get('freshReplay') == 'PASS' for row in cases)})
        totals = (sum(x.get('events', 0) for x in cases), sum(x.get('forwardOperations', 0) for x in cases),
                  sum(x.get('inverseOperations', 0) for x in cases))
        add(checks, 'Main case event and reversible-operation totals reconcile',
            totals == (331, 662, 662) and (counts['targetEvents'], counts['targetForwardOperations'], counts['targetInverseOperations']) == totals
            and counts['targetEventOperations'] == 1324,
            {'events': totals[0], 'forward': totals[1], 'inverse': totals[2]})
        add(checks, 'Fresh data/source/clock checks and independent package checks all pass',
            data['status'] == 'PASS' and data['checkCount'] == 14505 and data['failures'] == []
            and counts['freshAuditChecks'] == counts['freshAuditPassed'] == 14505 and counts['freshAuditFailures'] == 0
            and delivery['packageChecks']['status'] == 'PASS'
            and delivery['packageChecks']['checkCount'] == delivery['packageChecks']['passed'] == 292
            and delivery['packageChecks']['failed'] == 0
            and all(row['passed'] is True for row in delivery['packageChecks']['checks'])
            and validation['status'].startswith('PASS_FOR_SOURCE_PRESERVATION_AND_STATIC_REPLAY')
            and validation['dataAudit']['sha256'] == hashlib.sha256(z.read('DATA_INTEGRITY_CHECK.json')).hexdigest(),
            {'dataChecks': data['checkCount'], 'packageChecks': delivery['packageChecks']['passed']})
        add(checks, 'Original questions, addenda, main cases and future requirements remain preserved',
            counts['originalQuestionsPreserved'] == 31 and counts['focusedAddendaPreserved'] == 2
            and counts['originalRequiredMainCasesPreserved'] == 10 and counts['futureRequirementsPreserved'] == 5
            and len(preservation['files']) >= 7
            and preservation['noOtherProceduresReassessed'] is True,
            {'questions': counts['originalQuestionsPreserved'], 'addenda': counts['focusedAddendaPreserved'],
             'mainCases': counts['originalRequiredMainCasesPreserved'], 'futureRequirements': counts['futureRequirementsPreserved']})
        add(checks, 'Return246 binds the correct next pending group and current queue position',
            next_group['group'] == NEXT['group'] and next_group['pendingIds'] == NEXT['pendingIds']
            and delivery['nextPendingGroup']['group'] == NEXT['group']
            and delivery['nextPendingGroup']['pendingIds'] == NEXT['pendingIds']
            and delivery['nextPendingGroup']['sourcePath'].endswith('CURRENT_SPELL_QUEUE_246.json'),
            {'nextGroup': next_group['group'], 'nextIds': next_group['pendingIds']})
        queue = json.loads(QUEUE.read_text(encoding='utf-8-sig'))
        queue_rows = queue['currentPendingGroups']
        illusion_pos = next(i for i, row in enumerate(queue_rows) if row['group'] == 'rank9-illusion-reality5')
        queue_next = queue_rows[illusion_pos + 1]
        add(checks, 'The named group is the actual next row in the packet-bound current queue',
            queue_next['group'] == NEXT['group'] and queue_next['pendingIds'] == NEXT['pendingIds']
            and delivery['nextPendingGroup']['pointer'] == f'/currentPendingGroups/{illusion_pos + 1}',
            {'queueNext': queue_next['group'], 'queueIds': queue_next['pendingIds']})
        add(checks, 'Packet246 source archive and delivery are self-consistent with Return246 source reassessment',
            source_reassessment['sourcePacket']['filename'] == SOURCE_PACKET.name
            and source_reassessment['sourcePacket']['bytes'] == source_n
            and source_reassessment['sourcePacket']['sha256'] == source_sha
            and source_reassessment['authority'] == AUTH
            and counts['sourceBindingsVerified'] == 157,
            {'sourceBindings': counts['sourceBindingsVerified'], 'sourcePacketSha256': source_sha})

    passed = sum(row['passed'] for row in checks)
    report = {
        'id': 'RANK9ILLUSIONREALITY5-RETURN246-INDEPENDENT-AUDIT',
        'status': 'PASS' if passed == len(checks) else 'FAIL',
        'checkedAtUtc': datetime.now(timezone.utc).isoformat(),
        'archive': {'path': ARCHIVE.relative_to(ROOT).as_posix(), 'bytes': archive_n, 'sha256': archive_sha, 'crc32': archive_crc},
        'delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'bytes': delivery_n, 'sha256': delivery_sha, 'crc32': delivery_crc},
        'sourcePacket': {'path': SOURCE_PACKET.relative_to(ROOT).as_posix(), 'bytes': source_n, 'sha256': source_sha},
        'authority': AUTH, 'targetIds': TARGET, 'acceptedIds': delivery['acceptedIds'], 'appliedIds': delivery['appliedIds'],
        'heldIds': delivery['heldIds'], 'blockerIds': delivery['blockerIds'], 'counts': delivery['counts'],
        'nextPendingGroup': NEXT, 'checkCount': len(checks), 'passedChecks': passed,
        'failedChecks': len(checks) - passed, 'checks': checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report_n, report_sha, report_crc = digest(REPORT)
    receipt = {'id': 'RANK9ILLUSIONREALITY5-RETURN246-RECEIPT', 'status': report['status'],
               'archive': report['archive'], 'delivery': report['delivery'],
               'independentAudit': {'path': REPORT.relative_to(ROOT).as_posix(), 'bytes': report_n,
                                    'sha256': report_sha, 'crc32': report_crc},
               'checkCount': len(checks), 'passedChecks': passed, 'failedChecks': len(checks) - passed}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'checkCount': len(checks), 'passedChecks': passed,
                      'failedChecks': len(checks) - passed, 'report': str(REPORT), 'receipt': str(RECEIPT),
                      'failed': [row for row in checks if not row['passed']]}, ensure_ascii=False, indent=2))
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
