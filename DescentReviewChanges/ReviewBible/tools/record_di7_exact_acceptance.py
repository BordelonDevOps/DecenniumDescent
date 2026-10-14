"""Record the exact seven authored acceptances; preserve all submitted cards."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p): return json.loads(p.read_bytes())


def node(doc, pointer):
    for k in pointer.strip('/').split('/'):
        k = k.replace('~1', '/').replace('~0', '~')
        doc = doc[int(k)] if isinstance(doc, list) else doc[k]
    return doc


def main():
    V = A / 'di7-exact-final-verdict'
    receipt = A / 'DI7_EXACT_ACCEPTANCE_RECEIPT.json'
    delta = A / 'DI7_EXACT_ACCEPTANCE_RECORDING_OPERATIONS.json'
    preserved = A / 'source-before-di7-exact-acceptance-recording'
    assert not receipt.exists() and not delta.exists() and not preserved.exists()
    manifest = read(V / 'OUTPUT_MANIFEST.json')
    assert manifest['payloadCount'] == len(manifest['files']) == 36
    for b in manifest['files']:
        p = V / b['path']; assert p.resolve().is_relative_to(V.resolve())
        assert p.stat().st_size == b['bytes'] and digest(p.read_bytes()) == b['sha256']
    archive = A / 'DD_DI7_Exact_Review_Final_Verdict_and_Evidence.zip'
    assert archive.stat().st_size == 964355 and digest(archive.read_bytes()) == '38b27de8119d26813c8c3f81605163654b53f359ab72c790c1b7b9a26d726435'
    local_path = A / 'DI7_EXACT_FINAL_LOCAL_SUBMISSION_CHECK.json'; local = read(local_path)
    assert local['checks'] == local['passed'] == 1819 and not local['failed']
    authority_path = V / 'DI7_EXACT_ACCEPTANCE_AUTHORITY.json'; authority = read(authority_path)
    assert authority['decision'] == 'ACCEPT_SEVEN_EXACT_AUTHORED_OPERATIONAL_CANDIDATES'
    assert not authority['operativeCorrectionsRequired']
    submitted = authority['submission']; prior_submission = read(A / 'DI7_EXACT_REVIEW_01_SUBMISSION.json')
    assert submitted['archive']['sha256'] == prior_submission['archive']['sha256']
    assert submitted['manifest']['sha256'] == prior_submission['manifest']['sha256']
    assert submitted['payloadCount'] == prior_submission['payloadsVerified'] == 213
    for b in submitted['acceptedArtifacts']: assert info(G / b['path']) == b
    public_path = R / 'data/public/spell_candidates/divination_rank7_exact_01.json'
    internal_path = R / 'data/director/spell_candidates/divination_rank7_exact_01.json'
    public = read(public_path); internal = read(internal_path)
    ids = authority['acceptedSpellIds']; assert len(ids) == len(set(ids)) == 7
    assert [c['id'] for c in public['cards']] == ids and internal['completePublicEnvelope'] == public
    register = read(V / 'DI7_EXACT_CARD_REGISTER.json')
    assert [c['spellId'] for c in register['cards']] == ids
    for c in register['cards']:
        assert c['decision'] == 'ACCEPT_EXACT_AUTHORED_OPERATIONAL_SCOPE' and not c['operativeChangeRequired']
        pub_op = node(public, c['publicLocation']['pointer']); int_op = node(internal, c['internalLocation']['pointer'])
        assert pub_op == int_op and digest(pub_op['completeProcedure'].encode()) == c['completeProcedureUtf8Sha256']
    scope_path = V / 'DI7_EVIDENCE_SCOPE_ADDENDUM.json'; scope = read(scope_path)
    ev = scope['evidenceClarifications'][0]; assert ev['id'] == 'DI7-EV01'
    affected = ev['affectedEvidence']; evidence_path = G / affected['path']
    assert {k:v for k,v in info(evidence_path).items()} == {k:affected[k] for k in ['path','bytes','sha256']}
    assert node(read(evidence_path), affected['pointer']) == affected['guard']
    disposition_path = V / 'DI7_EXACT_CASE_DISPOSITIONS.json'; dispositions = read(disposition_path)
    expectations = read(R / 'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json')
    expected = {v['id']:v for group in expectations['groups'] + expectations['supplementalSourceExpectations'] for v in group['variants']}
    assert len(expected) == dispositions['totalCases'] == len(dispositions['rows']) == 93
    assert dispositions['allDisposed'] and not dispositions['all93AreFullSpellRuntimeTests']
    assert {x['id']:x['expectation'] for x in dispositions['rows']} == expected
    index_path = R / 'data/public/spell_playtests/authored_review_index.json'
    old = read(index_path); index = deepcopy(old)
    assert old['authoredCounts'] == {'reviewed':412,'pending':436}
    assert len(old['entries']) == 848 and len({x['id'] for x in old['entries']}) == 848
    current_catalog = R / 'data/public/spell_playtests/catalog.json'; catalog_binding = info(current_catalog)
    assert catalog_binding['sha256'] == old['sourceCatalogSha256']
    now = datetime.now(timezone.utc).isoformat()
    receipt_data = {'reviewId': authority['reviewId'], 'recordedAtUtc': now,
        'status': 'exact-authored-acceptance-recorded', 'archive': info(archive),
        'outputManifest': info(V / 'OUTPUT_MANIFEST.json'), 'payloadsVerified': 36,
        'submission': prior_submission['archive'], 'submissionManifest': prior_submission['manifest'],
        'acceptanceAuthority': info(authority_path), 'cardRegister': info(V / 'DI7_EXACT_CARD_REGISTER.json'),
        'caseDispositions': info(disposition_path), 'completeVerdict': info(V / 'DI7_EXACT_VERDICT.md'),
        'observedTerminalReply': info(A / 'DI7_EXACT_REVIEW_01_RECEIVED_DOM.txt'),
        'acceptedArtifactBindings': submitted['acceptedArtifacts'], 'acceptedSpellIds': ids,
        'operativeCorrections': 0, 'sourceFilesRewritten': False,
        'independentlyExecutedLocalChecks': {'report':info(local_path),'checks':1819,'failures':0},
        'reviewerReportedExecution': {'report':info(V / 'REPRODUCTION_RESULTS.json'),
            'boundedSuiteChecks':2108,'boundedSuites':15,'overlappingHistoryEntries':532,
            'notClaimedLocallyRerunByThisReceipt':True},
        'evidenceScopeAddendum': info(scope_path),
        'controllingEvidenceStatement': ev['controllingReceiptText'],
        'replacementEvidenceClassification': ev['replacementEvidenceClassification'],
        'historicalAffectedReportUnchanged': info(evidence_path),
        'authoredCountsBefore': old['authoredCounts'], 'authoredCountsAfter': {'reviewed':419,'pending':429},
        'runtimeSelectionEnabled': False, 'fullRuntimeCertified': False, 'humanBalanceApproved':False,
        'wholeGameFlowConfirmed':False,'pushed':False,'cosmologyReviewed':False,'sourceInformationDeleted':0}
    receipt.write_bytes(encoded(receipt_data))
    by_id = {c['spellId']:c for c in register['cards']}
    for entry in index['entries']:
        if entry['id'] not in by_id: continue
        assert entry['authoredStatus'] == 'pending-authored-procedure'
        c = by_id[entry['id']]
        entry['sourceCatalogWholeCardPointer'] = entry['wholeCardPointer']
        entry.update(authoredStatus='reviewed-authored-operational-playtest',
            procedureFile='../spell_candidates/divination_rank7_exact_01.json',
            procedurePointer=c['publicLocation']['pointer'],
            wholeCardPointer=c['publicLocation']['pointer'].rsplit('/',1)[0],
            sharedRulesPointer='/sharedOperatingRules',
            manuscript='../../../docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md',
            reviewId=authority['reviewId'], runtimeSelectionEnabled=False,
            completeEnvelopeBinding=info(public_path), authoredAcceptanceReceipt=info(receipt),
            historicalCandidateLabelsPreserved=True)
    index['authoredCounts'] = {'reviewed':419,'pending':429}
    index['representationCounts']['completeReviewedStandaloneProcedures'] = 143
    index['additionalStandaloneEnvelopes'] = [{'file':'../spell_candidates/divination_rank7_exact_01.json',
        'binding':info(public_path), 'reviewId':authority['reviewId'], 'acceptedIds':ids,
        'authority':info(authority_path), 'receipt':info(receipt)}]
    assert sum(x['authoredStatus']=='reviewed-authored-operational-playtest' for x in index['entries']) == 419
    for before, after in zip(old['entries'], index['entries']):
        if before['id'] not in ids: assert before == after
    # Preserve the only changed existing file and publish its exact operation.
    dest = preserved / index_path.relative_to(G); dest.parent.mkdir(parents=True)
    dest.write_bytes(index_path.read_bytes()); before_binding = info(index_path)
    assert dest.read_bytes() == index_path.read_bytes()
    (preserved / 'PRESERVATION_MANIFEST.json').write_bytes(encoded([{**before_binding,'preservedCopy':dest.relative_to(G).as_posix()}]))
    index_path.write_bytes(encoded(index))
    assert info(current_catalog) == catalog_binding
    for b in submitted['acceptedArtifacts']: assert info(G / b['path']) == b
    assert info(evidence_path) == receipt_data['historicalAffectedReportUnchanged']
    delta.write_bytes(encoded({'recordedAtUtc':now, 'changes':[{'before':{**before_binding,'preservedCopy':dest.relative_to(G).as_posix()},
        'after':info(index_path), 'acceptedIds':ids, 'scope':'Seven exact standalone authored-review memberships only.'}],
        'receipt':info(receipt),'oldMembershipsPreserved':True,'legacyCatalogUnchanged':catalog_binding,
        'acceptedCardFilesUnchanged':submitted['acceptedArtifacts'],'sourceInformationDeleted':0}))
    print(json.dumps({'receipt':info(receipt),'index':info(index_path),'reviewed':419,'pending':429,'payloadsVerified':36,'localChecks':1819}))


if __name__=='__main__':main()
