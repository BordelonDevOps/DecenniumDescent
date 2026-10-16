"""Preserve the returned gods review; do not adopt it before citation follow-up."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    download = Path('C:/Users/cbord/Downloads/COSMOLOGY_GODS_PANTHEONS_01_Addendum_and_Evidence.zip')
    archive = A/download.name
    root = A/'cosmology-gods-pantheons-01-received'
    receipt = A/'COSMOLOGY_GODS_PANTHEONS_01_RECEIVED_DECISION.json'
    citation_path = A/'COSMOLOGY_GODS_PANTHEONS_01_CITATION_CHECK.json'
    assert all(not x.exists() for x in [archive, root, receipt, citation_path])
    raw = download.read_bytes()
    assert len(raw) == 21556 and hashlib.sha256(raw).hexdigest() == '91025b239b19795b0e3e8ab9b85be0d0eace770e65025354fee2db6cccb5a5ba'
    names = {'COSMOLOGY_GODS_PANTHEONS_01_REGISTER.json', 'COSMOLOGY_GODS_PANTHEONS_01_VERDICT.md', 'SOURCE_HASHES.json', 'SEMANTIC_COVERAGE.json', 'EVIDENCE_MANIFEST.json'}
    with zipfile.ZipFile(download) as z:
        assert set(z.namelist()) == names and len(z.namelist()) == len(names)
        payloads = {name:z.read(name) for name in names}
    manifest = json.loads(payloads['EVIDENCE_MANIFEST.json'])
    assert len(manifest['files']) == 4
    for row in manifest['files']:
        b = payloads[row['filename']]
        assert len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256']
    submitted = A/'DD_Cosmology_Gods_Pantheons_01.zip'
    assert info(submitted)['sha256'] == manifest['submission']['sha256']
    hashes = json.loads(payloads['SOURCE_HASHES.json'])
    expected_hashes = json.loads((A/'cosmology-gods-pantheons-01/SOURCE_HASHES.json').read_bytes())
    assert hashes == expected_hashes and len(hashes) == 71
    for name, sha in hashes.items():
        assert hashlib.sha256((G/name).read_bytes()).hexdigest() == sha, name
        assert hashlib.sha256((A/'cosmology-gods-pantheons-01/sources'/name).read_bytes()).hexdigest() == sha, name
    register = json.loads(payloads['COSMOLOGY_GODS_PANTHEONS_01_REGISTER.json'])
    assert len(register['rows']) == 9 and len(register['reviewedSummaries']) == 4
    dom = A/'COSMOLOGY_GODS_PANTHEONS_01_RETURNED_DOM.txt'
    assert download.name in dom.read_text(encoding='utf-8')
    assert 'bounded verdict' in dom.read_text(encoding='utf-8')
    pub = json.loads((A/'cosmology-gods-pantheons-01/EXACT_PUBLICATION_PASSAGES.json').read_bytes())
    paragraphs = {r['paragraphIndexZeroBased']:r for r in pub['playerAppendixB']['paragraphs']}
    cited = []
    for row in register['rows']:
        for support in row['support']:
            if support['path'] != 'books/player/Decennium_Descent_Player_Rulebook_v6.docx':
                continue
            numbers = list(support.get('paragraphs', []))
            for key in ['paragraph', 'paragraphIndexZeroBased']:
                if key in support: numbers.append(support[key])
            if 'paragraphRangeZeroBased' in support:
                first, last = support['paragraphRangeZeroBased']
                numbers.extend(range(first, last+1))
            cited.append({'rowId':row['id'], 'returnedSupport':support, 'actualParagraphs':[paragraphs[n] for n in numbers]})
    bad = [9996,10082,10084,10087,10090,10092]
    assert 'Copper Thread' in paragraphs[9996]['text']
    assert 'Age of Wonders' in paragraphs[10087]['text']
    assert all(not paragraphs[n]['text'].strip() for n in [10082,10084,10090,10092])
    actual_terms = [r for r in paragraphs.values() if any(t in r['text'] for t in ['War of Chains and Teeth','Nine Infernal Courts'])]
    now = datetime.now(timezone.utc).isoformat()
    citation = {
        'checkId':'COSMOLOGY-GODS-PANTHEONS-01-CITATION-CHECK', 'recordedAtUtc':now,
        'source':info(G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx'),
        'index':info(A/'cosmology-gods-pantheons-01/EXACT_PUBLICATION_PASSAGES.json'),
        'indexConvention':'zero-based paragraph indices in word/document.xml, including blank and table paragraphs; use the supplied exact index, not a differently filtered enumeration',
        'verifiedCitationErrors':[{'rows':['GP-04','GP-05'],'paragraphs':bad,'finding':'These paragraphs are Copper Thread, blank, or Age of Wonders, not the asserted infernal terminology.'}],
        'additionalCitationConcerns':'GP-09 lists several blank and ancestry-creation paragraphs among its court/ascendant references. Audit all returned paragraph citations before adopting the register.',
        'allReturnedPlayerSupportsWithActualText':cited,
        'actualInfernalTerminologyParagraphs':actual_terms,
        'semanticRepairPerformed':False, 'sourceInformationDeleted':0,
    }
    archive.write_bytes(raw)
    root.mkdir()
    for name, b in payloads.items(): (root/name).write_bytes(b)
    citation_path.write_bytes(encoded(citation))
    decision = {
        'reviewId':register['reviewId'], 'recordedAtUtc':now,
        'status':'returned evidence verified; citation corrections and later-source follow-up required before candidate assembly',
        'submission':info(A/'COSMOLOGY_GODS_PANTHEONS_01_SUBMISSION.json'),
        'archive':info(archive), 'files':[info(root/n) for n in sorted(names)],
        'receivedDOM':info(dom), 'visibleProof':info(A/'COSMOLOGY_GODS_PANTHEONS_01_RETURNED.png'),
        'manifestPayloadsVerified':4, 'currentAndFrozenSourceHashesVerified':len(hashes),
        'rowDispositions':[{'id':r['id'],'disposition':r['disposition']} for r in register['rows']],
        'summaryDispositions':{k:v['verdict'] for k,v in register['reviewedSummaries'].items()},
        'citationCheck':info(citation_path),
        'localFollowup':info(A/'COSMOLOGY_GODS_PANTHEONS_01_LOCAL_FOLLOWUP_READING.json'),
        'candidateAssembled':False, 'sourceDoctrineChanges':0, 'sourceInformationDeleted':0,
        'fullCosmologyApproved':False, 'wholeGameApproved':False,
    }
    receipt.write_bytes(encoded(decision))
    print(json.dumps({'receipt':info(receipt),'citationCheck':info(citation_path),'sourceHashesVerified':len(hashes),'candidateAssembled':False}))


if __name__ == '__main__': main()
