"""Prepare a source-complete citation and later-reading follow-up for actual GPT."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded

REQUEST = '''COSMOLOGY-GODS-PANTHEONS-FOLLOWUP-01 — citation repair and later-source reconciliation.

Codex downloaded your actual COSMOLOGY-GODS-PANTHEONS-01 archive (21,556 bytes; SHA-256 91025b239b19795b0e3e8ab9b85be0d0eace770e65025354fee2db6cccb5a5ba), verified its four payload hashes and all 71 current/frozen source hashes, and preserved the original response unchanged. No gods/pantheons companion has been assembled yet. Please review the attached self-contained packet before adoption.

The packet contains every byte of the original submitted package under original-packet/, the five returned evidence files under returned-review/, and local follow-up evidence under local-followup/. The original response remains immutable; return a separate corrected successor, not an overwritten original.

1. Repair the paragraph citations in all nine GP rows, inventories, coverage and summaries using the supplied exact paragraph indexes, including blanks/table paragraphs in word/document.xml. The current player book's P9996 is Copper Thread; P10082/P10084/P10090/P10092 are blank; P10087 is Age of Wonders. They do not support GP-04/GP-05 infernal terminology. The actual war exposition is P10319 and peace rumor P10327. GP-09 also includes blank and ancestry-creation references. COSMOLOGY_GODS_PANTHEONS_01_CITATION_CHECK.json supplies the actual text for every returned Player support and all actual War of Chains and Teeth/Nine Infernal Courts matches. Audit all other DOCX citations too; do not merely replace the six examples. For corrected evidence provide exact file, XML part, zero-based paragraph index and a short accurate excerpt. Distinguish a citation error from a substantive decision change.

2. Explicitly dispose of GPR-01 through GPR-08 in the local follow-up. These contain full exact source passages and hashes. In particular: Serit dies at original Cosmology P116 but later appears teaching at P129 and as Lantern Master at P166, with no supplied bridge. P163 uses Passion amid Choir deliberation; P279 says nine verses, one per virtue plus Omega, while P280/P292 list seven. P154 explicitly calls Ulnak the one mind of Old Ones fused after Sundering; preserve that original-source assertion while not promoting it to a new owner ruling or merging the separate Floor-97 Old God. Later Cania evidence does not identify a replacement Maladomini ruler. Narrative Pact-driven class/spell changes have mechanical implications but are not automatically current class rules. The full original's later public saga/Proof War and the seventeen epilogue rule groups require campaign-epoch, mechanics and revelation decisions; do not assume the present campaign takes place afterward. Remaining named-setting terminology should stay on the publication/naming queue without automatic renaming or legal conclusions.

3. The Matrix formula source check directly inspected 23 original DOCX paragraphs: their incomplete-looking plain-text fragments already exist in source XML; there are zero OMML objects and no media/embedded-object payloads that recover the missing formulas. Acknowledge this as a source gap correcting the earlier extractor caution. No formula reconstruction or mathematical approval is requested.

Please return COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_Addendum_and_Evidence.zip containing: a complete corrected COSMOLOGY_GODS_PANTHEONS_01_REGISTER_CORRECTED.json (all nine rows, four exact reviewed summaries, inventories and dependencies); FOLLOWUP_DISPOSITIONS.json for all eight GPR items, citation errors and Matrix source gap; VERDICT.md; SOURCE_HASHES.json for the same 71 original sources; SEMANTIC_COVERAGE.json; and EVIDENCE_MANIFEST.json with exact file hashes. State whether the four summary texts or substantive GP decisions need changes beyond citation corrections, and precisely record all retained dependencies. Do not label any new GPT proposal an owner lock. Do not alter originals, delete historical material, import outside rosters, change class mechanics/flags, certify public deployment, or claim full cosmology/whole-game approval. This is a bounded follow-up to make the authored gods/pantheons companion accurate and traceable. Owner decisions being developed separately are not presumed approved here.
'''


def main():
    root = A/'cosmology-gods-pantheons-followup-01'
    archive = A/'DD_Cosmology_Gods_Pantheons_Followup_01.zip'
    receipt = A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_PREPARATION.json'
    assert all(not p.exists() for p in [root, archive, receipt])
    payloads = {}
    original = A/'DD_Cosmology_Gods_Pantheons_01.zip'
    assert info(original)['sha256'] == '088f4f9246aa3580518e20cb500bebf9a92b6ceb855e0386c61b3180566c597a'
    with zipfile.ZipFile(original) as z:
        for name in z.namelist():
            assert not name.startswith('/') and '..' not in Path(name).parts
            payloads['original-packet/'+name] = z.read(name)
    returned = A/'COSMOLOGY_GODS_PANTHEONS_01_Addendum_and_Evidence.zip'
    with zipfile.ZipFile(returned) as z:
        for name in z.namelist(): payloads['returned-review/'+name] = z.read(name)
    followup_names = [
        'COSMOLOGY_GODS_PANTHEONS_01_RECEIVED_DECISION.json',
        'COSMOLOGY_GODS_PANTHEONS_01_CITATION_CHECK.json',
        'COSMOLOGY_GODS_PANTHEONS_01_LOCAL_FOLLOWUP_READING.json',
        'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json',
        'COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json',
    ]
    for name in followup_names: payloads['local-followup/'+name] = (A/name).read_bytes()
    payloads['REQUEST.txt'] = REQUEST.encode()
    payloads['prepare_cosmology_gods_pantheons_followup_01.py'] = Path(__file__).read_bytes()
    for binding in json.loads((A/'cosmology-gods-pantheons-01/SOURCE_BINDINGS.json').read_bytes()):
        assert info(G/binding['path']) == binding
    manifest = {
        'reviewId':'COSMOLOGY-GODS-PANTHEONS-FOLLOWUP-01',
        'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'originalSubmission':info(original), 'originalReturnedEvidence':info(returned),
        'latestGitBackup':info(G/'docs/audit/2026-10-15/github-snapshot-pantheons/PUSH_RECEIPT.json'),
        'sourceFilesUnchanged':71, 'sourceInformationDeleted':0,
        'payloads':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payloads.items())],
    }
    payloads['PACKAGE_MANIFEST.json'] = encoded(manifest)
    root.mkdir()
    (root/'REQUEST.txt').write_bytes(payloads['REQUEST.txt'])
    (root/'PACKAGE_MANIFEST.json').write_bytes(payloads['PACKAGE_MANIFEST.json'])
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for name,b in sorted(payloads.items()): z.writestr(name,b)
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(payloads)
        for row in manifest['payloads']:
            b=z.read(row['path'])
            assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    receipt.write_bytes(encoded({'reviewId':manifest['reviewId'],'recordedAtUtc':manifest['recordedAtUtc'],'archive':info(archive),'request':info(root/'REQUEST.txt'),'manifest':info(root/'PACKAGE_MANIFEST.json'),'payloadsVerified':len(manifest['payloads']),'originalSourcesUnchanged':71,'sourceInformationDeleted':0,'status':'prepared; not yet submitted'}))
    print(json.dumps({'archive':info(archive),'preparation':info(receipt),'payloadsVerified':len(manifest['payloads'])}))


if __name__ == '__main__': main()
