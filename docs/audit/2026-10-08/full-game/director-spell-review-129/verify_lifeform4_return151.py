from __future__ import annotations
import copy
import hashlib
import json
import zlib
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / 'docs/audit/2026-10-08/full-game'
AUDIT = FULL / 'director-spell-review-129'
RECEIVED = AUDIT / 'rank8lifeform4_return151_received'
ARCHIVE = RECEIVED / 'DD_Rank8_LifeForm4_Director_Return151.zip'
DELIVERY = RECEIVED / 'DIRECTOR_RETURN_DELIVERY.json'
IDS = ['animal-shapes', 'clone', 'flesh-to-grave', 'perfect-form']
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
CANDIDATE = ROOT / 'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_life_form_4_source_conference_02.json'
SOURCE_ARCHIVE = FULL / 'DD_Rank8_Life_Form_4_Source_Conference_02.zip'
QUEUE = AUDIT / 'CURRENT_SPELL_QUEUE_150.json'
PENDING = AUDIT / 'CURRENT139_PENDING_IDENTITY_AUDIT_150.json'
HANDOFF = AUDIT / 'CURRENT_HANDOFF_150.json'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def binding_matches(path: Path, binding: dict) -> bool:
    raw = path.read_bytes()
    return len(raw) == binding['bytes'] and sha(raw) == binding['sha256']


def apply_root_patch(state, ops):
    result = copy.deepcopy(state)
    for op in ops:
        assert op['path'] == '', f"Unexpected non-root operation path: {op['path']}"
        if op['op'] == 'test':
            assert result == op['value'], 'Root test operation does not match state'
        elif op['op'] == 'replace':
            result = copy.deepcopy(op['value'])
        else:
            raise AssertionError(f"Unexpected operation type: {op['op']}")
    return result


def verify() -> dict:
    archive_bytes = ARCHIVE.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes.decode('utf-8-sig'))
    assert len(archive_bytes) == delivery['archive']['bytes'] == 14_849_228
    assert sha(archive_bytes) == delivery['archive']['sha256'] == 'faccf1d6869c46d2ea77756fe1b4b79a89b9ce57ff40b6a64af337609dd08abd'
    assert delivery['archive']['filename'] == ARCHIVE.name
    assert delivery['archive']['members'] == 210
    assert delivery['accepted'] is True and delivery['applied'] is False
    assert delivery['acceptedIds'] == IDS
    assert delivery['externalDecisionAcceptedUnapplied'] == 4
    expected_auth = {'reviewedApplied': 709, 'pending': 139, 'acceptedUnapplied': 0, 'completeReviewedStandaloneProcedures': 433}
    assert delivery['inputAuthority'] == expected_auth
    assert delivery['canonicalAuthorityUnchanged'] == {'reviewedApplied': 709, 'pending': 139, 'acceptedUnapplied': 0}

    live_bindings = {
        'index': INDEX,
        'catalog': CATALOG,
        'currentQueue': QUEUE,
        'pendingIdentityAudit': PENDING,
        'priorHandoff': HANDOFF,
    }
    live = {}
    for key, path in live_bindings.items():
        raw = path.read_bytes()
        declared = delivery['inputAuthority'].get(key) or None
        live[key] = raw
    assert len(INDEX.read_bytes()) == 1_084_957 and sha(INDEX.read_bytes()) == 'e3b83266c03d6883133bd81fb49ea3d45435bd0fbf19f296d12de52927989b68'
    assert len(CATALOG.read_bytes()) == 5_085_187 and sha(CATALOG.read_bytes()) == '773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b'
    candidate_raw = CANDIDATE.read_bytes()
    assert len(candidate_raw) == 792_314 and sha(candidate_raw) == 'bd2cd21a508a3527e2a219fd650b9cb6cc406abbfe5b6103c44226e7f73cdd47'
    assert binding_matches(SOURCE_ARCHIVE, {'bytes': 3_980_281, 'sha256': '7c2a57f58166ab5a4d11e5aef499a357f335d5b55ce6efaf75240aa375d36014'})
    assert len(QUEUE.read_bytes()) == 30_276 and sha(QUEUE.read_bytes()) == '1d1f4c701c2540814debab20dcba052056cd54d69e92599628c717f5b4b4109f'
    assert len(PENDING.read_bytes()) == 4_102 and sha(PENDING.read_bytes()) == '679d468890b8876ca28eb7ea3178bc5493748a099599a36166dd3c8641958a47'
    assert len(HANDOFF.read_bytes()) == 2_509 and sha(HANDOFF.read_bytes()) == 'd0733be60a724721a16115478cca38f69ddb9e9543d2f37929fbdfb0fdab018e'

    before = read_json(INDEX)
    catalog = read_json(CATALOG)
    queue = read_json(QUEUE)
    pending_doc = read_json(PENDING)
    candidate = read_json(CANDIDATE)
    assert before['authoredCounts'] == {'reviewed': 709, 'pending': 139}
    assert before['representationCounts']['completeReviewedStandaloneProcedures'] == 433
    live_pending = {row['id'] for row in before['entries'] if row['authoredStatus'] == 'pending-authored-procedure'}
    assert len(live_pending) == 139 and set(IDS) <= live_pending
    assert set(pending_doc['pendingIds']) == live_pending and pending_doc['pendingCount'] == 139
    assert queue['currentAuthority']['reviewedApplied'] == 709 and queue['currentAuthority']['pending'] == 139
    first_group = queue['currentPendingGroups'][0]
    assert first_group['group'] == 'rank8-life-form4' and first_group['pendingIds'] == IDS
    assert candidate['currentAuthority']['reviewedApplied'] == 709 and candidate['currentAuthority']['pending'] == 139
    assert [r['spellId'] for r in candidate['records'] if r['spellId'] in IDS] == IDS

    with ZipFile(ARCHIVE) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) == 210 and z.testzip() is None
        for name in names:
            p = PurePosixPath(name)
            assert name and not p.is_absolute() and '..' not in p.parts and '\\' not in name
            assert not name.startswith('/') and not any(part.startswith('.') for part in p.parts)
        binding_rows = {row['path']: row for row in delivery['memberBindings']}
        assert len(binding_rows) == 210 and set(binding_rows) == set(names)
        raw_members = {}
        for name in names:
            raw = z.read(name)
            row = binding_rows[name]
            crc = f'{z.getinfo(name).CRC:08x}'
            assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
            assert crc == row['crc32'].lower()
            raw_members[name] = raw
        manifest = json.loads(raw_members['MEMBER_MANIFEST.json'])
        assert manifest['archiveMemberCount'] == 210 and manifest['payloadMemberCount'] == 209
        assert manifest['hiddenOrTemporaryMembersAllowed'] is False
        assert set(manifest['allowlist']) == set(names)
        payload_rows = {row['path']: row for row in manifest['payloadMembers']}
        assert len(payload_rows) == 209 and set(payload_rows) == set(names) - {'MEMBER_MANIFEST.json'}
        for name, row in payload_rows.items():
            assert len(raw_members[name]) == row['bytes'] and sha(raw_members[name]) == row['sha256']
            assert binding_rows[name]['crc32'].lower() == row['crc32'].lower()

        decision = json.loads(raw_members['DIRECTOR_DECISION.json'])
        model = json.loads(raw_members['MODEL.json'])
        counts = json.loads(raw_members['COUNTS.json'])
        validation = json.loads(raw_members['VALIDATION.json'])
        failure = json.loads(raw_members['INDEPENDENT_FAILURE_CHECK.json'])
        dispositions = json.loads(raw_members['QUESTION_DISPOSITIONS.json'])
        original_dispositions = json.loads(raw_members['ORIGINAL_IDENTITY_DISPOSITIONS.json'])
        holds = json.loads(raw_members['HOLDS.json'])
        proposal_ops = json.loads(raw_members['PROPOSAL_OPERATIONS.json'])
        source_verification = json.loads(raw_members['SOURCE_VERIFICATION.json'])
        source2_candidate = json.loads(raw_members['evidence/source02/CANDIDATE.json'])

        assert decision['accepted'] is True and decision['applied'] is False
        assert decision['acceptedIds'] == IDS and decision['blockers'] == []
        assert decision['inputAuthority'] == expected_auth
        assert decision['canonicalAuthorityUnchanged'] == {'reviewedApplied': 709, 'pending': 139, 'acceptedUnapplied': 0}
        assert decision['decisionAcceptedUnappliedIdentityCount'] == 4
        assert model['accepted'] is True and model['applied'] is False and model['canonicalMutation'] is False
        assert list(model['spells']) == IDS
        assert set(model['spells']) == set(IDS)
        assert decision['procedureCanonicalHashes'].keys() == model['spells'].keys()
        for sid in IDS:
            proc = json.loads(raw_members[f'procedures/{sid}.json'])
            assert proc == model['spells'][sid]
            assert sha(canonical(proc)) == decision['procedureCanonicalHashes'][sid]
            assert proc['nativeUnchanged']['id'] == sid
            current_card = next(row for row in catalog['spells'] if row['id'] == sid)
            source_record = next(row for row in candidate['records'] if row['spellId'] == sid)['completeCurrentCatalogSourceAndAccess']
            assert proc['nativeUnchanged'] == source_record == current_card

        assert counts == delivery['counts']
        assert counts['conferenceQuestions'] == counts['answeredConferenceDispositions'] == 24
        assert counts['originalIdentityQuestionsPreservedAndAnswered'] == 4 and counts['futureObligationsRetained'] == 6
        assert counts['mainCases'] == 8 and counts['branches'] == 90 and counts['totalCases'] == 98
        assert counts['completeStaticFixtures'] == 58 and counts['heldDependentBranches'] == 40
        assert counts['events'] == 471 and counts['eventOperations'] == 1884 and counts['proposalOperations'] == 16
        assert counts['retainedHoldDefinitions'] == 13 and counts['independentStaticChecks'] == 21_481 and counts['independentStaticFailures'] == 0
        assert counts['sourceBoundFiles'] == 67 and counts['sourceZIPMembers'] == 71
        assert validation['passed'] is True and validation['canonicalFilesUntouched'] is True
        assert validation['counts'] == counts
        assert failure['passed'] == 21_481 and failure['failed'] == 0 and failure['blockers'] == []
        assert failure['runtimeExecuted'] is False and failure['humanPlay'] is False and failure['canonicalModified'] is False
        assert len(dispositions) == 24 and all(row.get('decisionSelected') is True for row in dispositions)
        expected_questions = {row['id'] for row in source2_candidate['questions']}
        assert {row['id'] for row in dispositions} == expected_questions and len(expected_questions) == 24
        assert len(original_dispositions) == 4
        assert len(holds) == 13 and all(row['retained'] is True for row in holds)
        assert len(proposal_ops) == 4 and [row['id'] for row in proposal_ops] == IDS
        assert all(row['target'] == 'isolated-proposal-only' for row in proposal_ops)
        assert all(row['before']['native'] == row['after']['native'] for row in proposal_ops)
        assert source_verification['archive']['bytes'] == 3_980_281
        assert source_verification['archive']['sha256'] == '7c2a57f58166ab5a4d11e5aef499a357f335d5b55ce6efaf75240aa375d36014'
        assert source_verification['archive']['publicDownloadIdentical'] is True
        assert source_verification['inputAuthorityUnchanged']['index']['sha256'] == sha(INDEX.read_bytes())
        assert source_verification['inputAuthorityUnchanged']['catalog']['sha256'] == sha(CATALOG.read_bytes())
        assert source_verification['inputAuthorityUnchanged']['currentQueue']['sha256'] == sha(QUEUE.read_bytes())
        assert source_verification['inputAuthorityUnchanged']['pendingIdentityAudit']['sha256'] == sha(PENDING.read_bytes())
        assert source_verification['inputAuthorityUnchanged']['priorHandoff']['sha256'] == sha(HANDOFF.read_bytes())
        assert source_verification['inputAuthorityUnchanged']['reviewedApplied'] == 709
        assert source_verification['inputAuthorityUnchanged']['pending'] == 139
        source_bindings = source_verification['boundSourceFiles']
        assert len(source_bindings) == 67 and all(row['verified'] is True for row in source_bindings)
        assert len(source2_candidate['sourceBindings']) == 67
        source_rows = {row['path']: row for row in source2_candidate['sourceBindings']}
        for row in source_bindings:
            assert row['path'] in source_rows
            assert row['bytes'] == source_rows[row['path']]['bytes'] and row['sha256'] == source_rows[row['path']]['sha256']
            payload = raw_members[row['packaged']]
            assert len(payload) == row['bytes'] and sha(payload) == row['sha256']
        assert raw_members['history/DD_Rank8_Life_Form_4_Source_Conference_02.zip'] == SOURCE_ARCHIVE.read_bytes()

        casebook = json.loads(raw_members['CASEBOOK.json'])
        assert len(casebook) == 98
        main_cases = [case for case in casebook if case['kind'] == 'main']
        branches = [case for case in casebook if case['kind'] == 'branch']
        assert len(main_cases) == 8 and len(branches) == 90
        assert sum(case['status'] == 'complete-static-fixture' for case in casebook) == 58
        assert sum(case['status'] == 'held-dependent-branch' for case in casebook) == 40
        assert sum(len(case['events']) for case in casebook) == 471
        assert sum(len(event['forward']) + len(event['inverse']) for case in casebook for event in case['events']) == 1_884
        replayed_events = 0
        for case in casebook:
            events = case['events']
            if events:
                assert case['initialState'] == events[0]['before']
                assert case['finalState'] == events[-1]['after']
            previous = case.get('initialState')
            for event in events:
                assert previous == event['before'], f"State continuity failed at {event['id']}"
                assert sha(canonical(event['before'])) == event['beforeSHA256']
                assert sha(canonical(event['after'])) == event['afterSHA256']
                assert event['forward'][0] == {'op': 'test', 'path': '', 'value': event['before']}
                assert apply_root_patch(event['before'], event['forward']) == event['after']
                assert event['inverse'][0] == {'op': 'test', 'path': '', 'value': event['after']}
                assert apply_root_patch(event['after'], event['inverse']) == event['before']
                previous = event['after']
                replayed_events += 1

    return {
        'id': 'LIFEFORM4-RETURN151-INDEPENDENT-VERIFICATION',
        'status': 'PASS',
        'archiveBytes': len(archive_bytes),
        'archiveSha256': sha(archive_bytes),
        'deliverySha256': sha(delivery_bytes),
        'acceptedIds': IDS,
        'inputAuthority': expected_auth,
        'sourceBindingsVerified': 67,
        'archiveMembersVerified': 210,
        'questionDispositionsVerified': 24,
        'heldDefinitionsRetained': 13,
        'completeStaticFixtures': 58,
        'heldDependentBranches': 40,
        'eventStatesAndHashesReplayed': replayed_events,
        'forwardAndInverseReplaysPassed': replayed_events * 2,
        'catalogUnchangedAtInput': True,
        'canonicalIndexUnchangedAtInput': True,
        'runtimeTests': 0,
        'failures': 0,
    }


if __name__ == '__main__':
    report = verify()
    out = AUDIT / 'LIFEFORM4_RETURN151_INDEPENDENT_VERIFICATION.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
