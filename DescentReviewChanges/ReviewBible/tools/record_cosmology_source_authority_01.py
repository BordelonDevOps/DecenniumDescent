"""Preserve the received first cosmology authority verdict without adopting doctrine."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, A, info, encoded

def main():
    downloaded = Path('C:/Users/cbord/Downloads/COSMOLOGY_SOURCE_AUTHORITY_01_Addendum_and_Evidence.zip')
    archive = A / downloaded.name
    unpacked = A / 'cosmology-source-authority-01-received'
    submission_path = A / 'COSMOLOGY_SOURCE_AUTHORITY_01_SUBMISSION.json'
    receipt_path = A / 'COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DECISION.json'
    assert all(not p.exists() for p in [archive, unpacked, submission_path, receipt_path])
    raw = downloaded.read_bytes()
    assert len(raw) == 16412 and hashlib.sha256(raw).hexdigest() == '01ad34da60b7c8e32d19c997991ed7f0511372d2c57e2c8a8fadf6e6bb057936'
    with zipfile.ZipFile(downloaded) as z:
        expected = {'COSMOLOGY_SOURCE_AUTHORITY_01_REGISTER.json', 'COSMOLOGY_SOURCE_AUTHORITY_01_VERDICT.md', 'EVIDENCE_MANIFEST.json', 'SEMANTIC_COVERAGE.json', 'SOURCE_HASHES.json'}
        assert set(z.namelist()) == expected and len(z.namelist()) == len(expected)
        payloads = {n: z.read(n) for n in expected}
    manifest = json.loads(payloads['EVIDENCE_MANIFEST.json'])
    for row in manifest['files']:
        b = payloads[row['file']]
        assert len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256']
    register = json.loads(payloads['COSMOLOGY_SOURCE_AUTHORITY_01_REGISTER.json'])
    source_hashes = json.loads(payloads['SOURCE_HASHES.json'])
    for name, sha in source_hashes.items():
        assert hashlib.sha256((G/name).read_bytes()).hexdigest() == sha, name
        assert hashlib.sha256((A/'cosmology-source-authority-01/sources'/name).read_bytes()).hexdigest() == sha, name
    passage_index = json.loads((A/'cosmology-source-authority-01/DOCX_PASSAGE_INDEX.json').read_bytes())['documents']
    cited_paragraphs = []
    for issue in register['issues']:
        for support in issue['support']:
            if 'paragraphSha256' in support:
                rows = [p for p in passage_index[support['path']] if p['part'] == 'word/document.xml' and p['paragraphIndexZeroBased'] == support['paragraph']]
                assert len(rows) == 1 and rows[0]['textSha256'] == support['paragraphSha256']
                cited_paragraphs.append({'issue': issue['id'], 'path': support['path'], 'paragraph': support['paragraph'], 'fullParagraphHashVerified': True, 'reviewerTextIsExactFullParagraph': support.get('text') == rows[0]['text']})
    prep = json.loads((A/'COSMOLOGY_SOURCE_AUTHORITY_01_PREPARATION.json').read_bytes())
    assert register['submissionVerification']['sha256'] == prep['archive']['sha256']
    assert register['submissionVerification']['manifestEntries'] == 40
    assert register['baselineCommit'] == 'a3f75a0ce577f51bd39153a872ef05ba9e877642'
    assert len(register['issues']) == 6 and register['noChanges']['cosmologyCompleted'] is False
    sent = A/'COSMOLOGY_SOURCE_AUTHORITY_01_SENT_DOM.txt'
    received = A/'COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DOM.txt'
    assert 'DD_Cosmology_Source_Authority_01.zip' in sent.read_text(encoding='utf-8')
    assert 'ChatGPT is responding' in sent.read_text(encoding='utf-8')
    observed = received.read_text(encoding='utf-8')
    assert 'Response complete' in observed and downloaded.name in observed
    now = datetime.now(timezone.utc).isoformat()
    archive.write_bytes(raw); unpacked.mkdir()
    for name, b in payloads.items(): (unpacked/name).write_bytes(b)
    submission = {'reviewId': register['reviewId'], 'recordedAtUtc': now, 'recordingScope': 'Retrospective record of the preserved actual send observation; no second submission.', 'statusAtSend': 'response-running', 'archive': prep['archive'], 'preparation': info(A/'COSMOLOGY_SOURCE_AUTHORITY_01_PREPARATION.json'), 'request': prep['request'], 'sentDOM': info(sent), 'sentProof': info(A/'COSMOLOGY_SOURCE_AUTHORITY_01_SENT.png'), 'browserId': '3', 'tabId': '125745968', 'conversationUrl': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b', 'sourceFiles': 34, 'payloads': 40, 'newDoctrine': 0}
    submission_path.write_bytes(encoded(submission))
    receipt = {'reviewId': register['reviewId'], 'recordedAtUtc': now, 'status': 'first-authority-conference-received; six findings dispositioned; full cosmology remains open', 'submission': info(submission_path), 'archive': info(archive), 'files': [info(unpacked/n) for n in sorted(payloads)], 'receivedDOM': info(received), 'visibleProof': info(A/'COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED.png'), 'exactEvidenceFilesVerified': 4, 'currentAndFrozenSourceHashesVerified': len(source_hashes), 'paragraphBindingsVerified': cited_paragraphs, 'scope': register['scope'], 'baselineCommit': register['baselineCommit'], 'issues': [{'id': x['id'], 'disposition': x['disposition'], 'dependency': x['dependency']} for x in register['issues']], 'semanticCoverage': info(unpacked/'SEMANTIC_COVERAGE.json'), 'nextOrderedComparisonWork': register['nextOrderedComparisonWork'], 'localInterpretationLimits': ['COS-A06 ownerChoiceRequiredNow=true is qualified by its own prose: only if mechanics require an operational threshold. No immediate owner question is necessary for the source comparison.', 'The outside-packet Directors Crucible prose is a reviewer-reported notebook source, not yet independently file-bound in this receipt.', 'The reviewer text fields accompanying full-paragraph hashes may summarize the paragraph; do not present them as exact full-paragraph quotations.', 'Hash and manifest checks establish file identity, not complete semantic reading or whole-cosmology approval.'], 'sourceReplacements': 0, 'sourceInformationDeleted': 0, 'publicProjection': False, 'generalCosmologyDomainCreated': False, 'cosmologyCompleted': False, 'wholeGameAccepted': False}
    receipt_path.write_bytes(encoded(receipt))
    print(json.dumps({'receipt': info(receipt_path), 'sourceHashesVerified': len(source_hashes), 'issues': len(register['issues']), 'doctrineChanges': 0, 'cosmologyCompleted': False}))

if __name__ == '__main__': main()
