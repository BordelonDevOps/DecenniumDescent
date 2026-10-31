from __future__ import annotations

import hashlib
import io
import json
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = AUDIT / 'rank9_materialforging2_return247_received'
ARCHIVE = RECEIVED / 'DD_Rank9_MaterialForging2_Director_Return247_HELD.zip'
DELIVERY = RECEIVED / 'DD_Rank9_MaterialForging2_Director_Return247_DELIVERY.json'
SOURCE_PACKET = AUDIT / 'rank9_materialforging2_current_source_247_prepared/DD_Rank9_MaterialForging2_CurrentSource_247.zip'
SOURCE_DELIVERY = AUDIT / 'rank9_materialforging2_current_source_247_prepared/DD_Rank9_MaterialForging2_CurrentSource_247_DELIVERY.json'
SOURCE_AUDIT = AUDIT / 'RANK9MATERIALFORGING2_PACKET_247_INDEPENDENT_AUDIT.json'
SOURCE_RECEIPT = AUDIT / 'RANK9MATERIALFORGING2_PACKET_247_RECEIPT.json'
RETURN246 = AUDIT / 'rank9_illusionreality5_return246_received/DD_Rank9_SoulReflection_Director_Return246_HELD.zip'
RETURN246_AUDIT = AUDIT / 'RANK9ILLUSIONREALITY5_RETURN246_INDEPENDENT_AUDIT.json'
RETURN210 = AUDIT / 'rank9_materialforging2_return210_received/DD_Rank9_MaterialForging2_Director_Return210.zip'
PACKET_QUEUE = 'current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_247.json'
REPORT = AUDIT / 'RANK9MATERIALFORGING2_RETURN247_INDEPENDENT_AUDIT.json'
RECEIPT = AUDIT / 'RANK9MATERIALFORGING2_RETURN247_RECEIPT.json'
AUTH = {'reviewedApplied': 811, 'pending': 37, 'acceptedUnapplied': 0,
        'completeStandaloneProcedures': 535, 'scopedInterfaces': 173}
TARGETS = ['eternal-forge', 'matter-conversion']
BLOCKERS = ['MF210-B01', 'MF210-B02']
NEXT = {'group': 'rank9-alignment-faction-purification5', 'pendingIds': [
    'alignment-ascension', 'alignment-perfection', 'faction-incarnate', 'faction-perfection', 'corruption-purification']}


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
    return246_n, return246_sha, return246_crc = digest(RETURN246)
    return246_audit = json.loads(RETURN246_AUDIT.read_text(encoding='utf-8-sig'))

    add(checks, 'Return247 archive bytes/SHA-256/CRC32 match the final repaired delivery binding',
        delivery['id'] == 'RETURN247-DELIVERY'
        and (archive_n, archive_sha, archive_crc) ==
        (delivery['archive']['bytes'], delivery['archive']['sha256'], delivery['archive']['crc32'].lower())
        and delivery['archive']['filename'] == ARCHIVE.name,
        {'bytes': archive_n, 'sha256': archive_sha, 'crc32': archive_crc,
         'compression': delivery.get('archiveCompression'), 'repair': delivery.get('deliveryRepair')})
    add(checks, 'Return247 external delivery manifest is intact and parsed from the received file',
        delivery_n > 0 and delivery['memberCount'] == 84 and delivery['accepted'] is False
        and delivery['applied'] is False and delivery['held'] is True,
        {'bytes': delivery_n, 'sha256': delivery_sha, 'crc32': delivery_crc})
    add(checks, 'Return247 binds to the exact independently audited Packet247 archive and delivery',
        (source_n, source_sha, source_crc) ==
        (delivery['externalSourceArchive']['bytes'], delivery['externalSourceArchive']['sha256'], delivery['externalSourceArchive']['crc32'].lower())
        and packet_audit['status'] == packet_receipt['status'] == 'PASS'
        and packet_audit['archive']['sha256'] == packet_receipt['archive']['sha256'] == source_sha
        and packet_audit['delivery']['sha256'] == packet_receipt['delivery']['sha256'] == source_delivery_sha
        and source_delivery_n > 0 and bool(source_delivery_crc),
        {'sourceBytes': source_n, 'sourceSha256': source_sha, 'packetChecks': packet_audit['passedChecks']})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        external_rows = {row['path']: row for row in delivery['members']}
        unsafe = [name for name in names if '\\' in name or PurePosixPath(name).is_absolute()
                  or '..' in PurePosixPath(name).parts or name.startswith('/')]
        add(checks, 'ZIP has exactly 84 unique safe members matching the delivery allowlist',
            len(names) == len(set(names)) == delivery['memberCount'] == 84
            and set(names) == set(delivery['exactAllowlist']) == set(external_rows)
            and not unsafe and z.testzip() is None,
            {'members': len(names), 'allowlist': len(external_rows), 'unsafePaths': unsafe[:8]})
        bad_external = []
        for name, row in external_rows.items():
            if member_digest(z, name) != (row['bytes'], row['sha256'], row['crc32'].lower()):
                bad_external.append(name)
            if z.getinfo(name).CRC != int(row['crc32'], 16):
                bad_external.append(name + ':central-crc')
        add(checks, 'All 84 members independently match delivery size/SHA/CRC and central CRC',
            not bad_external, {'checked': len(external_rows), 'failures': bad_external[:12]})

        manifest = readj(z, 'MEMBER_MANIFEST.json')
        internal_rows = {row['path']: row for row in manifest['members']}
        payload = set(names) - {'MEMBER_MANIFEST.json'}
        manifest_n, manifest_sha, manifest_crc = member_digest(z, 'MEMBER_MANIFEST.json')
        add(checks, 'Internal manifest inventories all 83 payload members and binds to external delivery',
            manifest['memberCountExcludingSelf'] == 83 and set(internal_rows) == payload
            and manifest['selfBinding'] == 'External delivery lists this manifest as a regular member; no self-hash.'
            and manifest['sourcePacketExternalBinding']['filename'] == SOURCE_PACKET.name
            and manifest['sourcePacketExternalBinding']['bytes'] == source_n
            and manifest['sourcePacketExternalBinding']['sha256'] == source_sha
            and external_rows['MEMBER_MANIFEST.json']['bytes'] == manifest_n
            and external_rows['MEMBER_MANIFEST.json']['sha256'] == manifest_sha
            and external_rows['MEMBER_MANIFEST.json']['crc32'].lower() == manifest_crc,
            {'payloadMembers': len(payload), 'manifestRows': len(internal_rows), 'manifestSha256': manifest_sha})
        bad_internal = [name for name, row in internal_rows.items()
                        if member_digest(z, name) != (row['bytes'], row['sha256'], row['crc32'].lower())]
        add(checks, 'Every payload member also matches the internal manifest', not bad_internal,
            {'checked': len(internal_rows), 'failures': bad_internal[:12]})

        decision = readj(z, 'DIRECTOR_DECISION.json')
        blockers = readj(z, 'HOLD_REGISTER.json')['blockers']
        semantic = readj(z, 'INDEPENDENT_SEMANTIC_FAILURE_CHECK.json')
        replay = readj(z, 'CASE_REPLAY.json')
        coverage = readj(z, 'COVERAGE_AND_FUTURE_DISPOSITIONS.json')
        data = readj(z, 'DATA_INTEGRITY_CHECK.json')
        bindings = readj(z, 'SOURCE_BINDINGS.json')
        preservation = readj(z, 'PRESERVATION_MANIFEST.json')
        validation = readj(z, 'VALIDATION.json')

        add(checks, 'Both exact identities remain held; none is accepted or applied',
            delivery['authority'] == AUTH and delivery['acceptedIds'] == delivery['appliedIds'] == []
            and delivery['heldIds'] == TARGETS and delivery['blockerIds'] == BLOCKERS
            and decision['authority'] == AUTH and decision['accepted'] is False and decision['applied'] is False
            and decision['acceptedIds'] == decision['appliedIds'] == [] and decision['heldIds'] == TARGETS
            and [(x['id'], x['blockerIds'], x['accepted'], x['applied'], x['held']) for x in decision['perIdentity']]
            == [('eternal-forge', ['MF210-B01'], False, False, True),
                ('matter-conversion', ['MF210-B02'], False, False, True)]
            and decision['canonicalChanges'] is False and decision['githubChanges'] is False
            and delivery['canonicalChanges'] is False and delivery['githubChanges'] is False,
            {'authority': delivery['authority'], 'heldIds': delivery['heldIds'], 'blockers': delivery['blockerIds']})
        missing_by_id = {x['id']: x['minimumMissingWitnesses'] for x in decision['perIdentity']}
        add(checks, 'MF210 blockers retain four distinct incomplete minimum-witness records',
            set(missing_by_id) == set(TARGETS)
            and [x['id'] for x in missing_by_id['eternal-forge']] == ['MF247-F-W1', 'MF247-F-W2']
            and [x['id'] for x in missing_by_id['matter-conversion']] == ['MF247-M-W1', 'MF247-M-W2']
            and all(x['mainCase'] for rows in missing_by_id.values() for x in rows)
            and {x['id'] for x in blockers} == set(BLOCKERS)
            and all(x['accepted'] is False and 'required-integrated-witness-coverage' in x['kind'] for x in blockers),
            {'witnesses': {k: [x['id'] for x in v] for k, v in missing_by_id.items()}})
        reassessment = readj(z, 'SOURCE_REASSESSMENT.json')
        add(checks, 'Source reassessment preserves proven item and casting facts separately from missing lifecycle coverage',
            len(reassessment['scope']) == 2 and set(reassessment['scope']) == set(TARGETS)
            and len(reassessment['anchors']) >= 3 and all(x.get('binding') and x.get('finding') for x in reassessment['anchors'])
            and {x['id'] for x in reassessment['blockers']} == set(BLOCKERS)
            and all(x.get('demonstrated') and x.get('minimumMissingWitnesses') for x in reassessment['blockers'])
            and 'not a missing-recipe or missing-repair-rule' in reassessment['blockers'][0]['reassessment']
            and len(bindings['bindings']) == 174 and bindings['sourcePacket']['sha256'] == source_sha,
            {'sourceBindings': len(bindings['bindings']), 'sourceAnchors': len(reassessment['anchors']),
             'reassessmentBlockers': [x['id'] for x in reassessment['blockers']]})

        cases = replay['cases']
        totals = (sum(x['events'] for x in cases), sum(x['forwardOperations'] for x in cases),
                  sum(x['inverseOperations'] for x in cases))
        add(checks, 'All 27 preserved traces replay, with 50 events and 100 reversible operations each way',
            len(cases) == 27 and all(x['freshReplay'] == 'PASS' for x in cases)
            and totals == (50, 100, 100)
            and replay['wholePositiveMainCasesComplete'] == 0
            and (delivery['counts']['cases'], delivery['counts']['events'], delivery['counts']['forwardOperations'],
                 delivery['counts']['inverseOperations']) == (27, 50, 100, 100),
            {'cases': len(cases), 'events': totals[0], 'forward': totals[1], 'inverse': totals[2]})
        main_cases = coverage['requiredMainCases']
        add(checks, 'All four required end-to-end main witnesses remain explicitly incomplete',
            len(main_cases) == 4 and coverage['allFourMainCasesComplete'] is False
            and all(x.get('status') == 'INCOMPLETE' for x in main_cases)
            and delivery['counts']['requiredMainCases'] == 4
            and delivery['counts']['completeRequiredMainCases'] == 0,
            {'mainCases': [x['id'] for x in main_cases], 'complete': 0})
        add(checks, 'All 24 original questions, two addenda and five future requirements remain present',
            len(readj(z, 'ORIGINAL_QUESTIONS.json')) == 24
            and delivery['counts']['originalQuestions'] == 24
            and delivery['counts']['focusedAddenda'] == 2
            and len(readj(z, 'ORIGINAL_FUTURE_REQUIREMENTS.json')) == 5
            and delivery['counts']['futureRequirements'] == 5
            and delivery['counts']['selectedDispositions'] == 26,
            {'questions': 24, 'addenda': 2, 'futureRequirements': 5})
        semantic_checks = semantic['checks']
        add(checks, 'Fresh data audit and independent semantic pass have no failures',
            data['status'] == 'PASS' and data['summary']['checks'] == data['summary']['passed'] == 3015
            and data['summary']['failed'] == 0 and all(x['passed'] is True for x in data['checks'])
            and semantic['componentCheckStatus'] == 'PASS'
            and semantic['wholeSpellAcceptanceStatus'] == 'FAIL_REQUIRED_WITNESSES_INCOMPLETE'
            and len(semantic_checks) == 18 and all(x['passed'] is True for x in semantic_checks)
            and delivery['counts']['semanticCrossChecks'] == 18
            and delivery['counts']['semanticCrossCheckFailures'] == 0
            and validation['status'].startswith('PASS_STATIC_PRESERVATION_REPLAY'),
            {'dataChecks': data['summary']['checks'], 'semanticCrossChecks': len(semantic_checks),
             'wholeSpellAcceptance': semantic['wholeSpellAcceptanceStatus']})
        add(checks, 'All 344 package checks pass, and the final repaired ZIP opens as LZMA-compressed archive',
            delivery['packageChecks']['status'] == 'PASS'
            and delivery['packageChecks']['checkCount'] == delivery['packageChecks']['passed'] == 344
            and delivery['packageChecks']['failed'] == 0
            and all(x['passed'] is True for x in delivery['packageChecks']['checks'])
            and str(delivery.get('archiveCompression', '')).startswith('ZIP method14 LZMA')
            and len({x.compress_type for x in z.infolist()}) == 1
            and z.infolist()[0].compress_type == zipfile.ZIP_LZMA,
            {'packageChecks': delivery['packageChecks']['passed'], 'compression': delivery.get('archiveCompression')})

    # Verify the 174 source contract rows against Packet247, its in-archive copy, and the current checkout.
    source_bad = []
    with zipfile.ZipFile(SOURCE_PACKET) as pz:
        for row in bindings['bindings']:
            packed_name = 'sources_current/' + row['path']
            try:
                packed = member_digest(pz, packed_name)
            except KeyError:
                source_bad.append(row['path'] + ':missing'); continue
            current_path = ROOT / row['path']
            if packed[:2] != (row['bytes'], row['sha256']) or not current_path.exists() \
                    or digest(current_path)[:2] != (row['bytes'], row['sha256']):
                source_bad.append(row['path'])
    add(checks, 'All 174 refreshed source bindings match Packet247 and current working-tree bytes',
        len(bindings['bindings']) == 174 and not source_bad,
        {'checked': len(bindings['bindings']), 'failures': source_bad[:10]})

    # Return210 is bound in the source packet; every preserved return member is checked byte-for-byte.
    old = preservation['externalPriorArchive']
    local_prior = digest(RETURN210)
    with zipfile.ZipFile(SOURCE_PACKET) as pz:
        prior_bytes, prior_sha, prior_crc = member_digest(pz, old['packetMember'])
        with zipfile.ZipFile(io.BytesIO(pz.read(old['packetMember']))) as prior_zip:
            preserved_bad = []
            with zipfile.ZipFile(ARCHIVE) as z:
                for row in preservation['preservedMembers']:
                    actual = member_digest(z, row['path'])
                    original = member_digest(prior_zip, row['originalMember'])
                    if actual != (row['bytes'], row['sha256'], row['crc32'].lower()) or original != actual:
                        preserved_bad.append(row['path'])
    add(checks, 'Return210 external archive binding and all 40 preserved members match byte-for-byte',
        (prior_bytes, prior_sha, prior_crc) == (old['bytes'], old['sha256'], old['crc32'].lower())
        and local_prior == (prior_bytes, prior_sha, prior_crc)
        and len(preservation['preservedMembers']) == 40 and not preserved_bad,
        {'priorBytes': prior_bytes, 'priorSha256': prior_sha, 'preservedMembers': len(preservation['preservedMembers']),
         'failures': preserved_bad[:10]})

    # The director's next-group pointer is validated against the queue snapshot bound into Packet247.
    with zipfile.ZipFile(SOURCE_PACKET) as pz:
        queue_raw = pz.read(PACKET_QUEUE)
        queue_snapshot = json.loads(queue_raw.decode('utf-8-sig'))
        next_binding = delivery['nextPendingGroup']['sourceBinding']
        queue_hash = (len(queue_raw), hashlib.sha256(queue_raw).hexdigest(), f'{zlib.crc32(queue_raw) & 0xffffffff:08x}')
    groups = queue_snapshot['currentPendingGroups']
    group_index = next(i for i, x in enumerate(groups) if x['group'] == 'rank9-material-forging2')
    actual_next = groups[group_index + 1]
    add(checks, 'Next pending group and queue snapshot pointer are exact',
        next_binding['path'].endswith('CURRENT_SPELL_QUEUE_247.json')
        and queue_hash == (next_binding['bytes'], next_binding['sha256'], next_binding['crc32'].lower())
        and delivery['nextPendingGroup']['pointer'] == f'/currentPendingGroups/{group_index + 1}'
        and delivery['nextPendingGroup']['group'] == NEXT['group']
        and delivery['nextPendingGroup']['pendingIds'] == NEXT['pendingIds']
        and actual_next['group'] == NEXT['group'] and actual_next['pendingIds'] == NEXT['pendingIds'],
        {'queueHash': queue_hash[1], 'nextGroup': actual_next['group'], 'nextIds': actual_next['pendingIds']})

    # Confirm the immediately preceding Return246 hold was carried into the bound current queue.
    with zipfile.ZipFile(SOURCE_PACKET) as pz:
        previous_queue = queue_snapshot
        previous = previous_queue.get('lastReviewedBatch', {})
        return246_copy = 'current/' + return246_audit['archive']['path']
        return246_packed = member_digest(pz, return246_copy)
    add(checks, 'Soul Reflection hold from independently audited Return246 remains preserved outside scope',
        return246_audit['status'] == 'PASS' and return246_audit['failedChecks'] == 0
        and (return246_n, return246_sha, return246_crc) == return246_packed
        and previous.get('group') == 'rank9-illusion-reality5'
        and previous.get('heldIds') == ['soul-reflection'] and previous.get('blockerIds') == ['IR207-B02']
        and previous.get('acceptedIds') == previous.get('appliedIds') == [],
        {'previousHeld': previous.get('heldIds'), 'previousBlockers': previous.get('blockerIds'),
         'return246Sha256': return246_sha})

    passed = sum(row['passed'] for row in checks)
    report = {
        'id': 'RANK9MATERIALFORGING2-RETURN247-INDEPENDENT-AUDIT',
        'status': 'PASS' if passed == len(checks) else 'FAIL',
        'checkedAtUtc': datetime.now(timezone.utc).isoformat(),
        'archive': {'path': ARCHIVE.relative_to(ROOT).as_posix(), 'bytes': archive_n, 'sha256': archive_sha, 'crc32': archive_crc},
        'delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'bytes': delivery_n, 'sha256': delivery_sha, 'crc32': delivery_crc},
        'sourcePacket': {'path': SOURCE_PACKET.relative_to(ROOT).as_posix(), 'bytes': source_n, 'sha256': source_sha},
        'authority': AUTH, 'targetIds': TARGETS, 'acceptedIds': delivery['acceptedIds'],
        'appliedIds': delivery['appliedIds'], 'heldIds': delivery['heldIds'], 'blockerIds': delivery['blockerIds'],
        'counts': delivery['counts'], 'nextPendingGroup': NEXT, 'checkCount': len(checks),
        'passedChecks': passed, 'failedChecks': len(checks) - passed, 'checks': checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report_n, report_sha, report_crc = digest(REPORT)
    receipt = {'id': 'RANK9MATERIALFORGING2-RETURN247-RECEIPT', 'status': report['status'],
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
