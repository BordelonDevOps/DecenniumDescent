"""Freeze the complete EX58 candidate with all original V3 payloads intact."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G/'DescentReviewChanges/ReviewBible'
A = G/'docs/audit/2026-10-08/full-game'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def meta(b):
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def main():
    archive = A/'DD_EX58_Complete_Exact_Candidate_01.zip'
    receipt_path = A/'EX58_EXACT_CANDIDATE_PACKAGE.json'
    handoff = A/'EX58_EXACT_REVIEW_HANDOFF.md'
    assert not any(p.exists() for p in [archive, receipt_path, handoff]), 'Preserve existing freeze before revision.'
    validation = read(A/'EX58_EXACT_CANDIDATE_CHECK.json')
    assert validation['status'] == 'Pass' and not validation['failures']
    prep = read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')
    payload = {}
    zpath = G/prep['archive']['path']
    assert meta(zpath.read_bytes()) == {k: prep['archive'][k] for k in ['bytes', 'sha256']}
    with zipfile.ZipFile(zpath) as z:
        for name in z.namelist():
            if not name.endswith('/'):
                payload[name] = z.read(name)
    for name, expected in prep['manifest'].items():
        assert meta(payload[name]) == expected, name

    def add(p, expected=None):
        p = p.resolve()
        name = p.relative_to(G).as_posix()
        b = p.read_bytes()
        if expected:
            assert meta(b) == {k: expected[k] for k in ['bytes', 'sha256']}, name
        if name in payload:
            assert payload[name] == b, 'Frozen source collision: ' + name
        payload[name] = b

    # Include original ZIP as well as its extracted original payloads. This permits
    # checking both archive identity and immediate source access independently.
    add(zpath, prep['archive'])
    receipts = [f'EX58_CANDIDATE_PART{n:02d}_CHECK.json' for n in range(1,7)] + [
        'EX58_TRANSPORT_CATALOGUE_CANDIDATE_CHECK.json', 'EX58_INTEGRATED_FLOW_CANDIDATE_CHECK.json',
        'EX58_BOUNDARY_CANDIDATE_CHECK.json', 'EX58_SOCIAL_SCENARIO_CANDIDATE_CHECK.json',
        'EX58_EXACT_CANDIDATE_ASSEMBLY.json', 'EX58_EXACT_CANDIDATE_CHECK.json']
    for filename in receipts:
        p = A/filename
        item = read(p)
        add(p)
        for path, expected in item.get('outputs', item.get('outputsVerified', {})).items():
            add(G/path, expected)
        inputs = item.get('inputs', {})
        if isinstance(inputs, list):
            for source in inputs:
                add(G/source['path'], source)
        else:
            for path, expected in inputs.items():
                add(G/path, expected)
        for key in ['builder', 'validator']:
            if key in item:
                add(G/item[key]['path'], item[key])
    for directory in ['ex58-final-gpt-verdict', 'ex58-edit-01-offices', 'ex58-edit-02-assay']:
        for p in sorted((A/directory).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                add(p)
    for filename in ['EXPEDITION_INTEGRATED_V3_PREPARATION.json', 'EXPEDITION_INTEGRATED_V3_SOURCE_HISTORY.json',
                     'EX58_FINAL_RECEIPT_LOCAL.json', 'EX58_LOCAL_REPRODUCTION.json',
                     'EX58_EDIT_01_FULFILLMENT.json', 'EX58_EDIT_02_FULFILLMENT.json',
                     'EX58_EDIT_02_LOCAL_REPRODUCTION.json',
                     'DD_Expedition_58_Source_Verdict_and_Evidence_2026_10_11.zip',
                     'DD_EX58_EDIT_01_Offices_Addendum.zip', 'DD_EX58_EDIT_02_Assay_Addendum.zip']:
        add(A/filename)
    for p in sorted((R/'data/director/expedition_candidate').glob('source_*_corrected.json')):
        add(p)
    for filename in ['EX58_SOURCE_CONTRACTS_CORRECTED.md', 'EX58_SOURCE_VERDICT_CORRECTED.md']:
        add(R/'docs/mechanics/expedition'/filename)
    add(Path(__file__))
    handoff_text = '''# EX58 complete exact candidate 01

This is the complete expedition, transport, social and reputation candidate requested after EX58-SOURCE-2026-10-11. It is ready for an exact candidate review, not another preliminary source conference. The local validation is packaging/reference evidence, not independent semantic or runtime approval.

Start with these complete artifacts, all relative to the archive root:

- `DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md`
- `DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_DIRECTOR_BOOK.md`
- `DescentReviewChanges/ReviewBible/data/public/expedition_candidate/complete_candidate.json`
- `DescentReviewChanges/ReviewBible/data/director/expedition_candidate/complete_candidate.json`
- `docs/audit/2026-10-08/full-game/EX58_EXACT_CANDIDATE_CHECK.json`
- `docs/audit/2026-10-08/full-game/ex58-final-gpt-verdict/EX58_EXACT_CANDIDATE_CONTRACT.json`

All 58 directions are authored across six chapters. The candidate contains 190 chapter examples, all 29 transport profiles and four auxiliaries, the full 21-event expedition with fifteen contract families, 28 fully instantiated boundaries, and all 24 original social scenarios with actual records. The internal original source layers include all 44 faction records, twenty background clauses, twelve reputation probes and seventeen complete class datasets (1,223 cards and 94 selected comparisons). Their prior review labels are unchanged.

The five-office and assay corrections EX58-EDIT-01 and EX58-EDIT-02 are fulfilled in derived files with the original deliveries intact. Do not substitute the old erroneous office enumeration or ten-percent-cap sentence for the corrected current text.

Review FLOW-C01 explicitly: the original example omitted stationary animal feeding intervals. The candidate uses supported thirty-minute stops at departure and hour twelve; the second includes the existing one-minute refill. Net extra time is 3,540 seconds (59 minutes). Haven entry is 17:23:12; first safe Rest completion is 29:03:12. This is example-specific, not a universal meal-duration rule. FLOW-C02 supplies actual people, provider shifts, walking-driver and withdrawal geometry premises. Check the revised clock, consumption, reservations, actor turns, services, rest and financial history together.

The complete component objects retain historical notices such as “remaining examples” from their original authorship stages. Those are receipts, not the current completeness report. The top-level current reading object and combined books have all the finished instances. No original component was silently rewritten to appear newer.

Evaluate all fifteen ECX-01 through ECX-15 acceptance requirements and all fifty-eight directions against the complete actual text and records. Independently inspect semantic correctness rather than accepting aggregate counts. The separate validator reconstructs the entire public envelope from allowed internal component fields and checks complete rendering; it does not prove that an incorrectly authored rule is correct. Record any actual discrepancy with a precise file/pointer or section, original and replacement wording, affected examples, and a finite correction check. Distinguish exact acceptance, exact corrections needed, and genuinely unreviewed material.

Please return one complete exact-candidate verdict and downloadable machine-readable register/evidence package bound to this submission's manifest and hashes. An accepted synthetic premise does not authenticate an actual campaign provider, geography, ownership, save history or dice roll. Pending class/spell/feat content receives no implied promotion. Human playtesting and application runtime remain separate.

Preservation: all 304 V3 manifest payloads are present at their original archive paths and unchanged, alongside the original V3 ZIP itself. The original V3 FILE_MANIFEST remains historical. The new outer manifest is EX58_EXACT_FILE_MANIFEST.json. All historical source versions and unadopted proposal text remain available. No deletion has occurred.

Broader game work remains open, including the remaining spell/feat/Director catalogs and eventual final joint whole-game flow review. The user's order remains final joint whole-game flow agreement, authorized GitHub push, remote-commit verification, then careful cosmology review. This expedition review is not the final whole-game agreement and does not review cosmology.
'''
    handoff.write_text(handoff_text, encoding='utf-8', newline='\n')
    add(handoff)
    payload['EX58_EXACT_START_HERE.md'] = handoff_text.encode('utf-8')
    manifest = {name: meta(b) for name, b in sorted(payload.items())}
    outer = {'schemaVersion': 1, 'candidateId': 'EX58-EXACT-CANDIDATE-01', 'files': manifest,
             'sourceV3Payloads': 304, 'sourceV3Archive': prep['archive'],
             'manifestExcludesItself': True, 'exactReviewPending': True}
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, b in sorted(payload.items()):
            z.writestr(name, b)
        z.writestr('EX58_EXACT_FILE_MANIFEST.json', json.dumps(outer, ensure_ascii=False, indent=2)+'\n')
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == len(manifest)+1
        for name, expected in manifest.items():
            assert meta(z.read(name)) == expected, name
    receipt = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'Frozen exact candidate; not yet submitted',
               'archive': {'path': archive.relative_to(G).as_posix(), **meta(archive.read_bytes())},
               'payloadFiles': len(manifest), 'originalV3PayloadsPreserved': 304,
               'allPayloadRoundtripVerified': True, 'manifest': manifest,
               'submitted': False, 'exactGPTApproval': False, 'sourceInformationDeleted': 0,
               'pushPerformed': False, 'cosmologyReviewed': False}
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: receipt[k] for k in ['status', 'archive', 'payloadFiles', 'originalV3PayloadsPreserved']}, indent=2))


if __name__ == '__main__':
    main()
