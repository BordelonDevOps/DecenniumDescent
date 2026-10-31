from __future__ import annotations

import copy
import hashlib
import json
import os
import pathlib
import shutil
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
INDEX = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG = ROOT / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
ARCHIVE = BASE / 'rank9_materialforging2_return247_received/DD_Rank9_MaterialForging2_Director_Return247_HELD.zip'
DELIVERY = BASE / 'rank9_materialforging2_return247_received/DD_Rank9_MaterialForging2_Director_Return247_DELIVERY.json'
RETURN_AUDIT = BASE / 'RANK9MATERIALFORGING2_RETURN247_INDEPENDENT_AUDIT.json'
RETURN_RECEIPT = BASE / 'RANK9MATERIALFORGING2_RETURN247_RECEIPT.json'
W1 = BASE / 'ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_253.json'
W1_AUDIT = BASE / 'ETERNAL_FORGE_MF210_B01_SUPPLEMENT_253_INDEPENDENT_AUDIT.json'
W2 = BASE / 'ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_255.json'
W2_AUDIT = BASE / 'ETERNAL_FORGE_MF210_B01_SUPPLEMENT_255_INDEPENDENT_AUDIT.json'
QUEUE0 = BASE / 'CURRENT_SPELL_QUEUE_249.json'
HANDOFF0 = BASE / 'CURRENT_HANDOFF_249.json'
PENDING0 = BASE / 'CURRENT37_PENDING_IDENTITY_AUDIT_249.json'
PKG_REL = pathlib.Path('DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255')
PKG = ROOT / PKG_REL
STAGE = PKG.with_name(PKG.name + '.staging')
MANUSCRIPT = ROOT / 'DescentReviewChanges/ReviewBible/docs/spells/candidates/ETERNAL_FORGE_REVIEWED_255.md'
REVIEW = 'ETERNAL-FORGE-EXACT-AUTHORED-ACCEPTANCE-255'
AUTHORITY = {'reviewedApplied': 811, 'pending': 37, 'acceptedUnapplied': 0,
             'completeStandaloneProcedures': 535, 'scopedInterfaces': 173}
AUTHORITY_AFTER = {'reviewedApplied': 812, 'pending': 36, 'acceptedUnapplied': 0,
                   'completeStandaloneProcedures': 536, 'scopedInterfaces': 173}
ACCEPTED = ['eternal-forge']


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def readj(path: pathlib.Path):
    return json.loads(path.read_text(encoding='utf-8'))


def bind(path: pathlib.Path, rel=None):
    raw = path.read_bytes()
    return {'path': rel or path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': sha(raw),
            'crc32': f'{zlib.crc32(raw) & 0xffffffff:08x}'}


def writej(path: pathlib.Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded(value))


def main():
    output_files = [
        BASE / 'ETERNAL_FORGE_DIRECTOR_ACCEPTANCE_255.json',
        BASE / 'ETERNAL_FORGE_EXACT_ACCEPTANCE_255.json',
        BASE / 'ETERNAL_FORGE_APPLICATION_255.json',
        BASE / 'ETERNAL_FORGE_INDEX_OPERATIONS_255.json',
        BASE / 'ETERNAL_FORGE_APPLICATION_VALIDATION_255.json',
        BASE / 'authored_review_index.before_eternalforge_255.json',
        BASE / 'CURRENT36_PENDING_IDENTITY_AUDIT_250.json',
        BASE / 'CURRENT_SPELL_QUEUE_250.json',
        BASE / 'CURRENT_HANDOFF_250.json',
        BASE / 'CURRENT_SPELL_REVIEW_SNAPSHOT_250.md',
    ]
    assert all(not p.exists() for p in output_files), 'Refusing to overwrite an application artifact.'
    assert not PKG.exists() and not STAGE.exists() and not MANUSCRIPT.exists(), 'Refusing to overwrite candidate outputs.'
    for p in [INDEX, CATALOG, ARCHIVE, DELIVERY, RETURN_AUDIT, RETURN_RECEIPT, W1, W1_AUDIT, W2, W2_AUDIT,
              QUEUE0, HANDOFF0, PENDING0]:
        assert p.is_file(), f'Missing required application input: {p}'

    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = readj(INDEX), readj(CATALOG)
    queue0, handoff0, pending0 = readj(QUEUE0), readj(HANDOFF0), readj(PENDING0)
    assert before['authoredCounts'] == {'reviewed': 811, 'pending': 37}
    assert before['representationCounts']['completeReviewedStandaloneProcedures'] == 535
    assert queue0['currentAuthority'] == handoff0['currentAuthority'] == pending0['authority'] == AUTHORITY
    for path, snapshot in [(INDEX, queue0['currentIndexBinding']), (CATALOG, queue0['currentCatalogBinding'])]:
        actual = bind(path)
        assert all(actual[k] == snapshot[k] for k in ['path', 'bytes', 'sha256', 'crc32'])
    assert pending0['pendingCount'] == 37 and len(pending0['pendingIds']) == 37
    pending_before = {e['id'] for e in before['entries'] if e['authoredStatus'] == 'pending-authored-procedure'}
    assert pending_before == set(pending0['pendingIds'])
    rows = {e['id']: e for e in before['entries']}
    cards = {e['id']: e for e in catalog['spells']}
    assert rows['eternal-forge']['authoredStatus'] == 'pending-authored-procedure'
    assert rows['eternal-forge']['sourceStatus'] == 'blocked-pending-operational-review'
    assert 'eternal-forge' in pending_before

    return_audit, return_delivery, receipt = readj(RETURN_AUDIT), readj(DELIVERY), readj(RETURN_RECEIPT)
    archive_raw = ARCHIVE.read_bytes()
    archive_sha = sha(archive_raw)
    assert return_audit['status'] == receipt['status'] == 'PASS'
    assert return_audit['checkCount'] == return_audit['passedChecks'] == 19 and return_audit['failedChecks'] == 0
    assert return_audit['archive']['bytes'] == len(archive_raw) and return_audit['archive']['sha256'] == archive_sha
    assert receipt['independentAudit']['sha256'] == sha(RETURN_AUDIT.read_bytes())
    assert return_delivery['accepted'] is False and return_delivery['applied'] is False
    assert return_delivery['acceptedIds'] == return_delivery['appliedIds'] == []
    assert return_delivery['heldIds'] == ['eternal-forge', 'matter-conversion']
    with zipfile.ZipFile(ARCHIVE) as zf:
        assert zf.testzip() is None
        director = json.loads(zf.read('DIRECTOR_DECISION.json'))
        procedures = {x['id']: x for x in json.loads(zf.read('PROCEDURES.json'))}
        source_hold = json.loads(zf.read('HOLD_REGISTER.json'))
        assert director['acceptedIds'] == director['appliedIds'] == []
        assert director['heldIds'] == ['eternal-forge', 'matter-conversion']
        assert director['authority']['reviewedApplied'] == 811 and director['authority']['pending'] == 37
        assert procedures['eternal-forge']['accepted'] is False and procedures['eternal-forge']['applied'] is False
        assert any(x['id'] == 'MF210-B01' for x in source_hold['blockers'])
    assert procedures['eternal-forge']['nativeSourceUnchanged']['completeCurrentCatalogSourceAndAccess'] == cards['eternal-forge']
    assert readj(W1)['id'] == 'ETERNAL-FORGE-MF210-B01-WITNESS-SUPPLEMENT-253'
    assert readj(W1_AUDIT)['status'].startswith('PASS_')
    assert readj(W2)['id'] == 'ETERNAL-FORGE-MF210-B01-WITNESS-SUPPLEMENT-255'
    assert readj(W2_AUDIT)['status'].startswith('CORRECTION_LOCAL_FORWARD_INVERSE_SOURCE_AND_SEMANTIC_CHECKS_PASS')
    assert sha(W2.read_bytes()) == '6def9f2a2ba8a3298c1a0c51f1a065aa0de8b043596bc143d8b1618219d8d441'

    # This exact director decision was visibly returned in Calibration review part 6.
    director_acceptance = {
        'id': 'ETERNAL-FORGE-DIRECTOR-ACCEPTANCE-255', 'recordedAtUtc': now(),
        'source': {'surface': 'GPT browser thread', 'threadTitle': 'Calibration review part 6',
                   'url': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'},
        'decision': 'ACCEPTED_FOR_STATIC_AUTHORED_REVIEW', 'acceptedIds': ACCEPTED,
        'appliedIds': [], 'closedBlockerIds': ['MF210-B01'],
        'completedWitnessIds': ['MF247-F-W1', 'MF247-F-W2'],
        'acceptedPacket': {'path': W2.relative_to(ROOT).as_posix(), 'bytes': W2.stat().st_size, 'sha256': sha(W2.read_bytes()),
                           'finalStateSHA256': readj(W2)['eventReplay']['branches'][0]['finalStateSHA256']},
        'recheck': {'MF254-W2-C01': 'closed; family history persists; castF3 firstFamily=false, baseDissonance=2, RefrainAdded=0; mirrors consistent',
                    'MF254-W2-C02': 'closed; A attacks at 86460.1, B starts at 86460.2, encounter closes at 86460.3',
                    'MF254-W2-C03': 'closed; paid commits set turnCast=true and A’s next actual regular start resets it',
                    'regularStartsProcessed': 'cumulative original and later starts preserved',
                    'registry': {'bytes': 236021, 'sha256': '40fe3da68084e8c9b875f5d21c5ff607867147153ab4f9f7e483f35b2c5fd1f6'}},
        'independentVerification': {'events': 24, 'forwardOperations': 395, 'inverseOperations': 410,
                                    'eventStateHashes': 48, 'reverseTraversalToExactF02Endpoint': True,
                                    'sourceBindingsMatched': 14},
        'countsAfterDirectorDecision': {'reviewedApplied': 811, 'held': 36, 'acceptedUnapplied': 1,
                                        'canonicalIndexStillPending': 37, 'completeStandaloneProcedures': 535,
                                        'scopedInterfaces': 173},
        'expectedCountsAfterApplication': AUTHORITY_AFTER,
        'remainingHeldIds': sorted(pending_before - set(ACCEPTED)),
        'retainedGates': ['source/access qualifications', 'runtime', 'implementation', 'human-play', 'balance',
                          'cosmology', 'domain-closure', 'completion', 'release'],
        'applicationAuthorizedByUserInstruction': 'Apply each batch once GPT accepts it.',
        'githubChanges': False, 'runtimeSelectionEnabled': False,
    }
    assert director_acceptance['acceptedIds'] == ['eternal-forge']
    assert director_acceptance['remainingHeldIds'] == sorted(pending_before - {'eternal-forge'})
    acceptance_path = BASE / 'ETERNAL_FORGE_DIRECTOR_ACCEPTANCE_255.json'
    writej(acceptance_path, director_acceptance)

    STAGE.mkdir(parents=True)
    stage_files = {
        'DIRECTOR_ACCEPTANCE.json': acceptance_path,
        'RETURN247.zip': ARCHIVE, 'RETURN247_DELIVERY.json': DELIVERY,
        'RETURN247_INDEPENDENT_AUDIT.json': RETURN_AUDIT, 'RETURN247_RECEIPT.json': RETURN_RECEIPT,
        'SUPPLEMENT253_W1.json': W1, 'SUPPLEMENT253_INDEPENDENT_AUDIT.json': W1_AUDIT,
        'SUPPLEMENT255_W2.json': W2, 'SUPPLEMENT255_INDEPENDENT_AUDIT.json': W2_AUDIT,
    }
    for dest, src in stage_files.items():
        shutil.copyfile(src, STAGE / dest)
    procedure = procedures['eternal-forge']
    scope = ('Only Eternal Forge’s static authored operational procedure is accepted and applied to the authored review index. '
             'Return247’s source/access record and the original item-body rules remain unchanged. MF210-B01 is closed by the completed W1 and W2 witnesses. '
             'Matter Conversion and all other pending identities remain held. This does not enable runtime selection or close source/access, implementation, '
             'human-play, balance, cosmology, domain-closure, completion, or release gates.')
    source_record = procedure['nativeSourceUnchanged']['completeCurrentCatalogSourceAndAccess']
    procedure_text = ['Eternal Forge — accepted static authored procedure',
                      'The following text is transcribed from Return247’s accepted spell-local proposal; headings identify source object keys.']
    for section_name in ['sharedProcedure', 'spellLocalNEW']:
        for key, value in procedure[section_name].items():
            procedure_text += ['', f'## {section_name}.{key}', '', str(value)]
    acceptance_receipt = {
        'id': REVIEW, 'recordedAtUtc': now(), 'status': 'EXACT_AUTHORED_PROCEDURE_ACCEPTED_WITH_RETAINED_SOURCE_AND_RELEASE_GATES',
        'decision': 'ACCEPTED_FOR_STATIC_AUTHORED_REVIEW_ONLY', 'approvedForCanonicalAuthoredIndexApplication': True,
        'directorDecision': bind(acceptance_path), 'acceptedIds': ACCEPTED, 'appliedIds': [],
        'closedBlockerIds': ['MF210-B01'], 'completedWitnessIds': ['MF247-F-W1', 'MF247-F-W2'],
        'directorReturn': bind(ARCHIVE), 'directorReturnAudit': bind(RETURN_AUDIT),
        'witnessW1': bind(W1), 'witnessW1Audit': bind(W1_AUDIT), 'witnessW2': bind(W2), 'witnessW2Audit': bind(W2_AUDIT),
        'countsBeforeApplication': director_acceptance['countsAfterDirectorDecision'],
        'expectedCountsAfterApplication': AUTHORITY_AFTER, 'scope': scope,
        'sourceStatusPreserved': 'blocked-pending-operational-review', 'runtimeSelectionEnabled': False,
        'sourceProgramsExecuted': False, 'runtimeTestsExecuted': False, 'humanPlaytested': False,
        'balanceApproved': False, 'cosmologyModified': False, 'releaseApproved': False,
    }
    writej(STAGE / 'EXACT_ACCEPTANCE.json', acceptance_receipt)
    writej(BASE / 'ETERNAL_FORGE_EXACT_ACCEPTANCE_255.json', acceptance_receipt)

    manifest_files = [bind(p, rel=p.name) for p in sorted(STAGE.iterdir(), key=lambda x: x.name) if p.is_file()]
    package_manifest = {'id': 'ETERNALFORGE-CANDIDATE-PACKAGE-MANIFEST-255', 'files': manifest_files,
                        'excludedFromBindings': ['CANDIDATE_PACKAGE_MANIFEST.json', 'MODEL.json'],
                        'selfExcluded': 'CANDIDATE_PACKAGE_MANIFEST.json'}
    writej(STAGE / 'CANDIDATE_PACKAGE_MANIFEST.json', package_manifest)
    manifest_binding = bind(STAGE / 'CANDIDATE_PACKAGE_MANIFEST.json', (PKG_REL / 'CANDIDATE_PACKAGE_MANIFEST.json').as_posix())
    model = {
        'schemaVersion': 3, 'moduleId': 'eternalforge-reviewed-255',
        'status': 'EXACT_AUTHORED_PROCEDURE_ACCEPTED_WITH_RETAINED_SOURCE_AND_RELEASE_GATES',
        'scope': scope, 'acceptedIds': ACCEPTED, 'heldIds': [], 'excludedPendingIds': director_acceptance['remainingHeldIds'],
        'sharedProcedure': procedure['sharedProcedure'], 'spells': [{
            'id': 'eternal-forge', 'name': 'Eternal Forge', 'status': 'ACCEPTED_STATIC_AUTHORED_REVIEW',
            'completeNativeSourceAndAccess': source_record,
            'procedure': {'sharedProcedure': procedure['sharedProcedure'], 'spellLocalNEW': procedure['spellLocalNEW']},
            'procedureText': '\n'.join(procedure_text),
            'directorProcedureRecord': procedure, 'sourceStatusPreserved': source_record['status'],
            'sourceCatalogPointer': rows['eternal-forge']['wholeCardPointer'],
            'completedWitnessIds': ['MF247-F-W1', 'MF247-F-W2'],
            'witnessBindings': {'W1': bind(W1), 'W2': bind(W2)},
            'retainedQualifications': procedure['qualifications'], 'runtimeSelectionEnabled': False,
        }],
        'directorAcceptanceFile': 'EXACT_ACCEPTANCE.json',
        'directorReturnArchive': bind(ARCHIVE), 'directorReturnAudit': bind(RETURN_AUDIT),
        'witnessW1': bind(W1), 'witnessW1Audit': bind(W1_AUDIT), 'witnessW2': bind(W2), 'witnessW2Audit': bind(W2_AUDIT),
        'candidatePackageManifestPath': (PKG_REL / 'CANDIDATE_PACKAGE_MANIFEST.json').as_posix(),
        'candidatePackageManifestBinding': manifest_binding,
        'canonicalSourceCatalogChanged': False, 'runtimeSelectionEnabled': False,
        'runtimeTestsExecuted': False, 'sourceProgramsExecuted': False, 'humanPlaytested': False,
        'balanceApproved': False, 'cosmologyModified': False, 'releaseApproved': False,
    }
    writej(STAGE / 'MODEL.json', model)
    model_binding = bind(STAGE / 'MODEL.json', (PKG_REL / 'MODEL.json').as_posix())
    os.replace(STAGE, PKG)
    manuscript = '# Eternal Forge — authored review 255\n\n' + scope + '\n\n' + model['spells'][0]['procedureText'] + '\n'
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript, encoding='utf-8', newline='\n')

    acceptance_binding = bind(BASE / 'ETERNAL_FORGE_EXACT_ACCEPTANCE_255.json')
    after = copy.deepcopy(before)
    operations = []
    for i, row in enumerate(before['entries']):
        if row['id'] != 'eternal-forge':
            continue
        old_row, new_row = copy.deepcopy(row), copy.deepcopy(row)
        source_pointer = row.get('sourceCatalogWholeCardPointer') or row['wholeCardPointer']
        new_row.update({
            'authoredStatus': 'reviewed-authored-operational-playtest',
            'procedureFile': '../spell_candidates/eternalforge_reviewed_255/MODEL.json',
            'procedurePointer': '/spells/0/procedure', 'structuredProcedurePointer': '/spells/0/procedure',
            'procedureTextPointer': '/spells/0/procedureText', 'wholeCardPointer': '/spells/0',
            'sourceCatalogWholeCardPointer': source_pointer, 'wholeCardIdField': 'id',
            'sharedRulesPointer': '/sharedProcedure',
            'manuscript': '../../../docs/spells/candidates/ETERNAL_FORGE_REVIEWED_255.md',
            'reviewId': REVIEW, 'runtimeSelectionEnabled': False, 'completeEnvelopeBinding': model_binding,
            'authoredAcceptanceReceipt': acceptance_binding, 'historicalCandidateLabelsPreserved': True,
            'directorReturnArchiveBinding': bind(ARCHIVE), 'witnessW1Binding': bind(W1), 'witnessW2Binding': bind(W2),
            'witnessW1AuditBinding': bind(W1_AUDIT), 'witnessW2AuditBinding': bind(W2_AUDIT),
            'retainedQualifications': procedure['qualifications'], 'acceptedSharedRuleScope': scope,
        })
        operations.append({'op': 'replace-entry', 'identity': 'eternal-forge', 'index': i,
                           'before': old_row, 'after': copy.deepcopy(new_row)})
        after['entries'][i] = new_row
    assert len(operations) == 1
    after['authoredCounts'] = {'reviewed': 812, 'pending': 36}
    after['representationCounts']['completeReviewedStandaloneProcedures'] = 536
    envelope = {'file': '../spell_candidates/eternalforge_reviewed_255/MODEL.json', 'binding': model_binding,
                'reviewId': REVIEW, 'acceptedIds': ACCEPTED, 'heldIds': [], 'authority': acceptance_binding,
                'directorReturn': bind(ARCHIVE), 'witnessW1': bind(W1), 'witnessW2': bind(W2),
                'applicationReceipt': 'docs/audit/2026-10-08/full-game/director-spell-review-129/ETERNAL_FORGE_APPLICATION_255.json',
                'scope': scope}
    after['additionalStandaloneEnvelopes'].append(envelope)
    pending_after = {e['id'] for e in after['entries'] if e['authoredStatus'] == 'pending-authored-procedure'}
    assert pending_after == pending_before - {'eternal-forge'} and len(pending_after) == 36
    assert after['sourceCatalogSha256'] == before['sourceCatalogSha256']
    assert after['standaloneEnvelopeSha256'] == before['standaloneEnvelopeSha256']
    restored = copy.deepcopy(after)
    for op in operations:
        restored['entries'][op['index']] = op['before']
    restored['authoredCounts'] = copy.deepcopy(before['authoredCounts'])
    restored['representationCounts'] = copy.deepcopy(before['representationCounts'])
    restored['additionalStandaloneEnvelopes'] = restored['additionalStandaloneEnvelopes'][:-1]
    assert restored == before
    backup = BASE / 'authored_review_index.before_eternalforge_255.json'
    backup.write_bytes(index_raw)
    index_after = encoded(after)
    temp = INDEX.with_suffix('.json.eternalforge255.tmp')
    temp.write_bytes(index_after)
    os.replace(temp, INDEX)
    assert INDEX.read_bytes() == index_after
    operations_doc = {'id': 'ETERNAL-FORGE-INDEX-OPERATIONS-255', 'before': bind(backup), 'after': bind(INDEX),
                      'operations': operations, 'reverseSemanticExact': True, 'reverseByteExactBackup': True,
                      'onlyIdentityIds': ACCEPTED, 'sourceCatalogUnchanged': True}
    writej(BASE / 'ETERNAL_FORGE_INDEX_OPERATIONS_255.json', operations_doc)
    application = {
        'id': 'ETERNAL-FORGE-APPLICATION-255', 'recordedAtUtc': now(),
        'status': 'APPLIED_ETERNAL_FORGE_AUTHORED_REVIEW_WITH_SOURCE_QUALIFICATIONS_RETAINED',
        'reviewId': REVIEW, 'acceptedIds': ACCEPTED, 'before': bind(backup), 'after': bind(INDEX),
        'candidateEnvelope': model_binding, 'candidatePackageManifest': manifest_binding,
        'acceptanceReceipt': acceptance_binding, 'directorAcceptance': bind(acceptance_path),
        'directorReturn': bind(ARCHIVE), 'witnessW1': bind(W1), 'witnessW2': bind(W2),
        'counts': {'before': AUTHORITY, 'after': AUTHORITY_AFTER}, 'sourceCatalogUnchanged': CATALOG.read_bytes() == catalog_raw,
        'sourceStatusPreserved': 'blocked-pending-operational-review', 'runtimeSelectionEnabled': False,
        'runtimeTestsExecuted': False, 'sourceProgramsExecuted': False, 'humanPlaytested': False,
        'balanceApproved': False, 'cosmologyModified': False, 'releaseApproved': False,
        'githubChanges': False, 'scope': scope,
    }
    writej(BASE / 'ETERNAL_FORGE_APPLICATION_255.json', application)

    after_binding = bind(INDEX)
    remaining = sorted(pending_after)
    groups = []
    for old_group in pending0['groups']:
        new_ids = [sid for sid in old_group['pendingIds'] if sid in pending_after]
        if new_ids:
            group = copy.deepcopy(old_group)
            group['pendingIds'] = new_ids
            group['pendingCount'] = len(new_ids)
            groups.append(group)
    pending_audit = {
        'id': 'CURRENT36-PENDING-IDENTITY-AUDIT-250', 'recordedAtUtc': now(),
        'status': 'PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_ETERNAL_FORGE_APPLICATION',
        'authority': AUTHORITY_AFTER, 'indexBinding': after_binding, 'catalogBinding': bind(CATALOG),
        'pendingCount': len(remaining), 'pendingIds': remaining, 'groups': groups,
        'allPendingIdsExistInNativeCatalog': all(sid in cards for sid in remaining),
        'noPendingTargetWasSilentlyAccepted': True, 'acceptedIds': ACCEPTED, 'appliedIds': ACCEPTED,
        'heldIds': remaining, 'allCurrentPendingIdentitiesReviewed': True, 'unreviewedPendingIds': [],
        'closed335AndCompletedCohortsReopened': False,
        'nextBlockerPriority': {'identity': 'unravel-identity', 'blockerId': 'MD196-B02'},
    }
    writej(BASE / 'CURRENT36_PENDING_IDENTITY_AUDIT_250.json', pending_audit)
    queue1 = copy.deepcopy(queue0)
    queue1.update({'id': 'CURRENT-SPELL-QUEUE-250', 'recordedAtUtc': now(), 'supersedesQueue': QUEUE0.name,
                   'currentAuthority': AUTHORITY_AFTER, 'currentIndexBinding': after_binding,
                   'currentCatalogBinding': bind(CATALOG), 'currentPendingGroups': groups,
                   'nextSuggestedGroups': [], 'nextGroup': None, 'next': {
                       'group': None, 'pendingIds': [], 'pendingCount': 0,
                       'status': 'ALL_CURRENT_PENDING_GROUPS_HAVE_SEALED_DIRECTOR_DISPOSITIONS',
                       'nextAction': 'DIRECTOR_CONFERENCE_ON_REMAINING_HELD_WITNESSES'},
                   'pendingCount': 36, 'pendingIdentityAudit': {
                       'path': 'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT36_PENDING_IDENTITY_AUDIT_250.json',
                       'pending': 36, 'sha256': sha(encoded(pending_audit))},
                   'justAppliedBatch': {'reviewId': REVIEW, 'ids': ACCEPTED, 'count': 1,
                       'applicationReceipt': 'docs/audit/2026-10-08/full-game/director-spell-review-129/ETERNAL_FORGE_APPLICATION_255.json'},
                   'lastReviewedBatch': {'group': 'rank9-material-forging2', 'acceptedIds': ACCEPTED,
                       'appliedIds': ACCEPTED, 'heldIds': ['matter-conversion'], 'blockerIdsClosed': ['MF210-B01']},
                   'currentReturnAcceptedIds': ACCEPTED, 'currentReturnAppliedIds': ACCEPTED,
                   'currentReturnHeldIds': ['matter-conversion'], 'unreviewedPendingIds': [],
                   'recommendedClosurePriority': ['unravel-identity'], 'status': 'ETERNAL_FORGE_APPLIED_36_HELD_IDENTITIES_REMAIN'})
    queue_path = BASE / 'CURRENT_SPELL_QUEUE_250.json'
    writej(queue_path, queue1)
    handoff1 = copy.deepcopy(handoff0)
    handoff1.update({'id': 'CURRENT-HANDOFF-250', 'recordedAtUtc': now(),
                     'status': 'ETERNAL_FORGE_ACCEPTED_APPLIED_NEXT_UNRAVEL_IDENTITY_MD196_B02',
                     'currentAuthority': AUTHORITY_AFTER,
                     'latestBatch': {'reviewId': REVIEW, 'ids': ACCEPTED, 'applicationReceipt': application['id']},
                     'appliedThisStep': {'reviewId': REVIEW, 'acceptedIds': ACCEPTED, 'appliedIds': ACCEPTED},
                     'pendingIdentityAudit': {'id': pending_audit['id'],
                                              'path': 'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT36_PENDING_IDENTITY_AUDIT_250.json',
                                              'pendingCount': 36, 'sha256': sha(encoded(pending_audit))},
                     'queue': {'path': queue_path.relative_to(ROOT).as_posix(), 'sha256': sha(queue_path.read_bytes())},
                     'nextGroup': None, 'nextPendingCount': 0,
                     'nextStep': 'Continue blocker-resolution with Unravel Identity MD196-B02; use GPT as director and apply only after exact acceptance.',
                     'recommendedClosurePriority': ['unravel-identity'],
                     'resumePriority': 'No first-review tasks remain. Eternal Forge MF210-B01 is accepted and applied; proceed to Unravel Identity MD196-B02 using its exact blocker witness, then obtain GPT acceptance and independently audit before application.',
                     'allCurrentPendingIdentitiesReviewed': True, 'unreviewedPendingIds': [],
                     'canonicalChanges': True, 'applicationChanges': True, 'githubChanges': False,
                     'runtimeSelectionEnabled': False, 'canonicalRuntimeApplicationPerformed': False})
    writej(BASE / 'CURRENT_HANDOFF_250.json', handoff1)
    snapshot = ('# Ordinary spell review snapshot 250\n\n'
                '**Authority:** 812 reviewed/applied / 36 pending / 0 accepted-unapplied; 536 complete standalone procedures / 173 scoped interfaces.\n\n'
                '**Applied:** Eternal Forge (MF210-B01) after GPT acceptance; W1 and W2 complete.\n\n'
                '**Next blocker:** Unravel Identity (MD196-B02).\n\n'
                '**Other gates:** runtime selection, implementation, human play, balance, cosmology, domain closure, completion, and release remain closed.\n')
    (BASE / 'CURRENT_SPELL_REVIEW_SNAPSHOT_250.md').write_text(snapshot, encoding='utf-8', newline='\n')

    result = {
        'id': 'ETERNAL-FORGE-APPLICATION-VALIDATION-255', 'status': 'PASS',
        'acceptedAndAppliedIds': ACCEPTED, 'closedBlockerIds': ['MF210-B01'],
        'authority': AUTHORITY_AFTER, 'pendingCount': len(remaining), 'pendingIds': remaining,
        'changedIdentityCount': 1, 'unrelatedIndexEntriesUnchanged': sum(
            x['id'] != 'eternal-forge' and x == y for x, y in zip(before['entries'], after['entries'])),
        'sourceCatalogUnchanged': CATALOG.read_bytes() == catalog_raw,
        'sourceStatusPreserved': rows['eternal-forge']['sourceStatus'] == after['entries'][next(i for i, e in enumerate(after['entries']) if e['id'] == 'eternal-forge')]['sourceStatus'],
        'onlyAcceptedIdentityChanged': set(ACCEPTED) == {o['identity'] for o in operations},
        'reverseSemanticExact': restored == before, 'backupByteExact': backup.read_bytes() == index_raw,
        'runtimeSelectionEnabled': False, 'githubChanges': False,
        'indexBinding': after_binding, 'applicationReceipt': bind(BASE / 'ETERNAL_FORGE_APPLICATION_255.json'),
        'acceptanceReceipt': acceptance_binding, 'candidateEnvelope': model_binding,
    }
    writej(BASE / 'ETERNAL_FORGE_APPLICATION_VALIDATION_255.json', result)
    assert result['unrelatedIndexEntriesUnchanged'] == len(before['entries']) - 1
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
