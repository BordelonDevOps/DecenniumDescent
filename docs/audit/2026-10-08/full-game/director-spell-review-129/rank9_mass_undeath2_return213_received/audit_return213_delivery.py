from __future__ import annotations
import hashlib, json, zlib, zipfile
from pathlib import Path, PurePosixPath

root = Path.cwd()
base = root / 'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_mass_undeath2_return213_received'
archive = base / 'DD_Rank9_MassUndeath2_Director_Return213_HELD.zip'
delivery_path = base / 'DD_Rank9_MassUndeath2_Director_Return213_HELD_DELIVERY.json'
delivery = json.loads(delivery_path.read_text(encoding='utf-8-sig'))
errors: list[str] = []

def file_digest(path: Path) -> tuple[int, str, str]:
    h = hashlib.sha256(); crc = 0; size = 0
    with path.open('rb') as f:
        while chunk := f.read(1024 * 1024):
            size += len(chunk); h.update(chunk); crc = zlib.crc32(chunk, crc)
    return size, h.hexdigest(), f'{crc & 0xffffffff:08x}'

archive_size, archive_sha, archive_crc = file_digest(archive)
if archive_size != delivery['archive']['bytes']: errors.append('archive byte count mismatch')
if archive_sha != delivery['archive']['sha256']: errors.append('archive SHA-256 mismatch')
if archive_crc != delivery['archive']['crc32']: errors.append('archive CRC32 mismatch')

with zipfile.ZipFile(archive) as zf:
    infos = zf.infolist(); names = [x.filename for x in infos]
    if len(names) != len(set(names)): errors.append('duplicate ZIP member paths')
    if len(names) != delivery['archiveMemberCount']: errors.append('archive member count mismatch')
    for name in names:
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '\\' in name or (p.parts and ':' in p.parts[0]):
            errors.append(f'unsafe ZIP member path: {name}')
    if zf.testzip() is not None: errors.append('ZIP CRC test failed')
    mi = zf.getinfo(delivery['memberManifest']['path'])
    mm_size, mm_sha, mm_crc = delivery['memberManifest']['bytes'], delivery['memberManifest']['sha256'], delivery['memberManifest']['crc32']
    raw_manifest = zf.read(mi.filename)
    if len(raw_manifest) != mm_size: errors.append('member manifest byte count mismatch')
    if hashlib.sha256(raw_manifest).hexdigest() != mm_sha: errors.append('member manifest SHA-256 mismatch')
    if f'{zlib.crc32(raw_manifest) & 0xffffffff:08x}' != mm_crc: errors.append('member manifest CRC mismatch')
    manifest = json.loads(raw_manifest.decode('utf-8-sig'))
    expected = manifest['members']
    expected_names = {item['path'] for item in expected}
    actual_payload_names = set(names) - {mi.filename}
    if len(expected) != delivery['payloadMemberCount']: errors.append('payload manifest count mismatch')
    if expected_names != actual_payload_names: errors.append('payload member set mismatch')
    actual_meta = {x.filename: x for x in infos}
    for item in expected:
        name = item['path']; info = actual_meta.get(name)
        if info is None: errors.append(f'missing member: {name}'); continue
        if info.file_size != item['bytes']: errors.append(f'{name}: size mismatch')
        if f'{info.CRC:08x}' != item['crc32'].lower(): errors.append(f'{name}: ZIP CRC mismatch')
        h = hashlib.sha256(); crc = 0; size = 0
        with zf.open(name) as f:
            while chunk := f.read(1024 * 1024):
                size += len(chunk); h.update(chunk); crc = zlib.crc32(chunk, crc)
        if size != item['bytes']: errors.append(f'{name}: streamed size mismatch')
        if h.hexdigest() != item['sha256'].lower(): errors.append(f'{name}: SHA-256 mismatch')
        if f'{crc & 0xffffffff:08x}' != item['crc32'].lower(): errors.append(f'{name}: content CRC mismatch')
    checks = delivery.get('packageChecks', {})
    check_list = checks.get('checks', [])
    if not checks.get('passed'): errors.append('delivery packageChecks.passed is false')
    if len(check_list) != checks.get('checkCount'): errors.append('package check count mismatch')
    if any(not c.get('passed') for c in check_list): errors.append('one or more package checks failed')
    decision = json.loads(zf.read('DIRECTOR_DECISION.json'))
    authority = json.loads(zf.read('CURRENT_AUTHORITY.json'))
    holds = json.loads(zf.read('HOLD_REGISTER.json'))
    summary = {
      'archiveMemberCount': len(names), 'payloadMemberCount': len(expected),
      'packageChecks': {'count': len(check_list), 'passed': checks.get('passed') and all(c.get('passed') for c in check_list)},
      'decision': decision, 'authority': authority, 'holdRegister': holds,
      'failureReport': zf.read('INDEPENDENT_SEMANTIC_FAILURE_CHECK.json').decode('utf-8-sig'),
      'reviewReport': zf.read('README.md').decode('utf-8-sig') if 'README.md' in names else ''
    }

report = {
  'id': 'RETURN213-INDEPENDENT-AUDIT',
  'archive': {'path': archive.relative_to(root).as_posix(), 'bytes': archive_size, 'sha256': archive_sha, 'crc32': archive_crc},
  'deliveryManifest': {'path': delivery_path.relative_to(root).as_posix(), 'archiveMemberCount': delivery['archiveMemberCount'], 'payloadMemberCount': delivery['payloadMemberCount']},
  'packageChecks': summary['packageChecks'],
  'directorDecision': delivery['acceptedIds'],
  'heldIds': delivery['heldIds'],
  'authority': delivery['authority'],
  'counts': delivery['counts'],
  'decisionMember': summary['decision'],
  'authorityMember': summary['authority'],
  'holdRegisterMember': summary['holdRegister'],
  'errors': errors,
  'status': 'PASS' if not errors else 'FAIL'
}
report_path = base / 'RETURN213_INDEPENDENT_AUDIT.json'
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: report[k] for k in ['status','archive','deliveryManifest','packageChecks','heldIds','authority','counts','errors']}, indent=2))
print('DECISION_MEMBER_KEYS', list(summary['decision'].keys()) if isinstance(summary['decision'], dict) else type(summary['decision']).__name__)
print('FAILURE_CHECK_MEMBER_PREVIEW', summary['failureReport'][:6000])
