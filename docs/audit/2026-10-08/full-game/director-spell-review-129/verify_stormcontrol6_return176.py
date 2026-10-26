from __future__ import annotations
import hashlib, json, zipfile, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
STATE = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = STATE / 'rank9_stormcontrol6_return176_received'
ZIP_PATH = RECEIVED / 'DD_Rank9_StormControl6_Director_Return176.zip'
DELIVERY_PATH = RECEIVED / 'DD_Rank9_StormControl6_Director_Return176_DELIVERY.json'
AUDIT_PATH = STATE / 'RANK9_STORMCONTROL6_RETURN176_INDEPENDENT_AUDIT.json'
SCOPE = ['cosmic-implosion', 'frozen-eternity', 'hellstorm', 'storm-of-vengeance', 'thunder-wrath', 'storm-cage']
EXPECTED_BLOCKERS = ['ST176-B01', 'ST176-B02', 'ST176-B03']
checks = []
def check(name: str, condition: bool, details=None):
    checks.append({'check': name, 'passed': bool(condition), 'details': details})
    if not condition:
        raise AssertionError(f'failed: {name}: {details}')
def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()
def load_member(z: zipfile.ZipFile, name: str):
    return json.loads(z.read(name).decode('utf-8'))

delivery_bytes = DELIVERY_PATH.read_bytes()
delivery = json.loads(delivery_bytes.decode('utf-8'))
archive_sha = sha_file(ZIP_PATH)
check('Saved archive has the director-reported byte length and SHA-256', ZIP_PATH.stat().st_size == delivery['archive']['bytes'] == 41980515 and archive_sha == delivery['archive']['sha256'] == 'd56a602ebea24db7d4b32cc63580a246c39c38bf1e750cddfc1606a7d3425f98', {'bytes': ZIP_PATH.stat().st_size, 'sha256': archive_sha})
check('Delivery manifest exact length/hash are recorded', len(delivery_bytes) == 23347 and sha_bytes(delivery_bytes) == 'db1857a953a8db0ac4bfd5f22178362dc760b6675bf6c55cb5032edaaae4a004', {'bytes': len(delivery_bytes), 'sha256': sha_bytes(delivery_bytes)})
check('Manifest identifies a nonaccepted, unapplied six-spell return', delivery['accepted'] is False and delivery['applied'] is False and delivery['acceptedIds'] == [] and delivery['reviewedIds'] == SCOPE, {'accepted': delivery['accepted'], 'applied': delivery['applied'], 'acceptedIds': delivery['acceptedIds'], 'reviewedIds': delivery['reviewedIds']})
check('Manifest authority preserves 749/99/0', delivery['authority']['appliedReviewed'] == 749 and delivery['authority']['pending'] == 99 and delivery['authority']['acceptedUnapplied'] == 0, delivery['authority'])
check('Manifest reports exact review/case/hold/check counts', delivery['memberCount'] == 96 and delivery['counts']['procedures'] == 6 and delivery['counts']['questions'] == 27 and delivery['counts']['mainCases'] == 12 and delivery['counts']['branches'] == 42 and delivery['counts']['caseRecords'] == 54 and delivery['counts']['events'] == 520 and delivery['counts']['eventOperations'] == 2080 and delivery['counts']['localHolds'] == 9 and delivery['counts']['inheritedHoldRecords'] == 87 and delivery['counts']['semanticBlockers'] == 3, delivery['counts'])

expected_members = {m['path']: m for m in delivery['members']}
with zipfile.ZipFile(ZIP_PATH, 'r') as z:
    infos = z.infolist()
    names = [x.filename for x in infos]
    check('Archive has exactly 96 unique allowlisted members', len(infos) == 96 and len(set(names)) == 96 and set(names) == set(expected_members), {'actual': len(infos), 'manifest': len(expected_members)})
    bad_names = [n for n in names if n.startswith(('/', '\\')) or '..' in Path(n).parts or '__MACOSX' in n or Path(n).name.startswith('.') or 'tmp' in Path(n).name.lower()]
    check('Archive has no path traversal, hidden, or temporary members', not bad_names, bad_names)
    check('Archive CRC pass completes', z.testzip() is None)
    for info in infos:
        meta = expected_members[info.filename]
        check(f'{info.filename}: byte length and CRC match delivery', info.file_size == meta['bytes'] and f'{info.CRC:08x}' == meta['crc32'].lower(), {'bytes': info.file_size, 'crc32': f'{info.CRC:08x}'})
        digest = hashlib.sha256(); total = 0
        with z.open(info, 'r') as f:
            for b in iter(lambda: f.read(1024 * 1024), b''):
                digest.update(b); total += len(b)
        check(f'{info.filename}: SHA-256 matches delivery', total == meta['bytes'] and digest.hexdigest() == meta['sha256'], {'bytes': total, 'sha256': digest.hexdigest()})
    decision = load_member(z, 'DIRECTOR_DECISION.json')
    semantic = load_member(z, 'SEMANTIC_FAILURE_CHECK.json')
    clocks = load_member(z, 'REGULAR_CLOCK_FAILURE_CHECK.json')
    procedures = load_member(z, 'PROCEDURES.json')['procedures']
    questions = load_member(z, 'QUESTION_DISPOSITIONS.json')['questions']
    source = load_member(z, 'SOURCE_VERIFICATION.json')
    data = load_member(z, 'DATA_VALIDATION.json')
    holds = load_member(z, 'HOLD_REGISTER.json')
    candidate_bytes = z.read('SOURCE_CONFERENCE_CANDIDATE.json')
    source_packet_bytes = z.read('SOURCE_CONFERENCE_ARCHIVE.zip')
    check('Inner source packet candidate and archive bind the exact submitted packet', sha_bytes(candidate_bytes) == '1689f6a7181327a4853bba56845c519e45b6e8b0e99127396386f2366487fe1d' and len(source_packet_bytes) == 27959906 and sha_bytes(source_packet_bytes) == '00f539c422a318a45f2db3b49d96604f11fe3468493a6fb7d001ef6bb2c6c660', {'candidateSha256': sha_bytes(candidate_bytes), 'sourcePacketBytes': len(source_packet_bytes), 'sourcePacketSha256': sha_bytes(source_packet_bytes)})
    check('Director decision and semantic failure check agree on no acceptance and exact blockers', decision['accepted'] is False and decision['applied'] is False and decision['acceptedIds'] == [] and semantic['passed'] is False and semantic['acceptedIds'] == [] and [b['id'] for b in decision['blockers']] == EXPECTED_BLOCKERS and [b['id'] for b in semantic['blockers']] == EXPECTED_BLOCKERS)
    check('Return retains exact authority and six spell scope', decision['authority']['appliedReviewed'] == 749 and decision['authority']['pending'] == 99 and decision['reviewedIds'] == SCOPE and delivery['reviewedIds'] == SCOPE)
    check('All six procedure records remain unaccepted and unapplied', len(procedures) == 6 and [p['spellId'] for p in procedures] == SCOPE and all(p['accepted'] is False and p['applied'] is False for p in procedures))
    check('All 27 original/focused question dispositions are present', len(questions) == 27 and sum(bool(q.get('decisionSelected')) for q in questions) == 27)
    check('Source verification report has 311 passing checks and no failures', source['passed'] is True and source['checkCount'] == 311 and source['failures'] == [] and all(x['passed'] for x in source['checks']))
    check('Data validation reports 20,814 passes and no failures', data['passedCount'] == 20814 and data['failedCount'] == 0 and data['failures'] == [] and all(x['passed'] for x in data['checks']))
    check('Regular-clock blocker covers 43 case records and 213 actors', clocks['passed'] is False and clocks['blockerId'] == 'ST176-B03' and clocks['affectedCaseCount'] == 43 and clocks['affectedActorRecords'] == 213 and len(clocks['findings']) == 43)
    check('Local and inherited scoped holds remain separately preserved', len(holds['localHolds']) == 9 and len(holds['inheritedExactScopeRecords']) == 87 and holds['counts']['totalScopedRecords'] == 96)

index_path = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
catalog_path = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
index_bytes = index_path.read_bytes(); catalog_bytes = catalog_path.read_bytes()
index = json.loads(index_bytes.decode('utf-8'))
index_blob = subprocess.check_output(['git', 'cat-file', 'blob', 'HEAD:DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'], cwd=ROOT)
catalog_blob = subprocess.check_output(['git', 'cat-file', 'blob', 'HEAD:DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'], cwd=ROOT)
index_from_blob = json.loads(index_blob.decode('utf-8')); catalog_from_blob = json.loads(catalog_blob.decode('utf-8'))
pending_ids = sorted(e['id'] for e in index['entries'] if e['authoredStatus'] == 'pending-authored-procedure')
check('Current authored index/catalog Git blobs remain byte-exact to reviewed base', sha_bytes(index_blob) == 'd7157bb971283767404868ca6e3c662feb38b3d5e5c2a73fcd3980486ca65bdb' and sha_bytes(catalog_blob) == 'f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8', {'indexBlobSha256': sha_bytes(index_blob), 'catalogBlobSha256': sha_bytes(catalog_blob)})
check('Checkout index/catalog parse to the same content as committed Git blobs', json.loads(index_bytes.decode('utf-8')) == index_from_blob and json.loads(catalog_bytes.decode('utf-8')) == catalog_from_blob, {'workingTreeCatalogRawSha256': sha_bytes(catalog_bytes), 'reason': 'Windows checkout line endings differ; committed Git blobs remain exact'})
check('Live index remains 749 reviewed/99 pending with all six identities pending', index['authoredCounts'] == {'reviewed': 749, 'pending': 99} and len(pending_ids) == 99 and all(x in pending_ids for x in SCOPE), {'authoredCounts': index['authoredCounts'], 'pendingCount': len(pending_ids)})

result = {
  'id': 'RANK9-STORMCONTROL6-RETURN176-INDEPENDENT-AUDIT',
  'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
  'status': 'PACKAGE_AND_DECISION_BINDINGS_PASS; SEMANTIC_ACCEPTANCE_FAILS_WITH_THREE_BLOCKERS',
  'packageIntegrityPassed': True,
  'semanticAcceptancePassed': False,
  'accepted': False,
  'applied': False,
  'acceptedIds': [],
  'blockerIds': EXPECTED_BLOCKERS,
  'authority': {'appliedReviewed': 749, 'pending': 99, 'acceptedUnapplied': 0},
  'reviewIds': SCOPE,
  'archive': {'path': ZIP_PATH.relative_to(ROOT).as_posix(), 'bytes': ZIP_PATH.stat().st_size, 'sha256': archive_sha, 'memberCount': 96},
  'delivery': {'path': DELIVERY_PATH.relative_to(ROOT).as_posix(), 'bytes': len(delivery_bytes), 'sha256': sha_bytes(delivery_bytes)},
  'checksPassed': len(checks),
  'checksFailed': 0,
  'checks': checks,
  'semanticFindings': {
    'ST176-B01': 'Six required genuine extra-turn traces lack verified source/access evidence.',
    'ST176-B02': 'Monk anchoring/immunity fixture has unresolved level-three acquisition classification.',
    'ST176-B03': '43 traces (213 actor records) omit elapsed regular-turn/resource/lifecycle accounting.'
  },
  'qualification': 'Integrity verification does not waive the director’s semantic blockers. No IDs accepted or applied; canonical index/catalog unchanged.'
}
AUDIT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({'auditPath': AUDIT_PATH.relative_to(ROOT).as_posix(), 'checksPassed': len(checks), 'checksFailed': 0, 'archiveSha256': archive_sha, 'deliverySha256': sha_bytes(delivery_bytes), 'accepted': False, 'blockers': EXPECTED_BLOCKERS}, indent=2))
