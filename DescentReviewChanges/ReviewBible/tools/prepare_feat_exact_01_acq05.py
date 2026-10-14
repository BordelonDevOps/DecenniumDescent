"""Prepare the concrete Animal Companion payment/attempt/transfer question."""
from datetime import datetime, timezone
import json
from pathlib import Path
import zipfile
from record_feat_exact_01_acq03_fulfillment import read, info, write_new

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    request = A / 'FEAT327_ACQ_05_COMPANION_TIMING_QUESTION.txt'
    archive = A / 'DD_FEAT327_ACQ05_Companion_Timing_Source.zip'
    receipt = A / 'FEAT327_ACQ_05_PREPARATION.json'
    assert all(not p.exists() for p in [request, archive, receipt])
    prompt = '''FEAT327-ACQ-05 — Animal Companion purchase, attempt and transfer boundaries

ACQ-04 is fulfilled locally: your exact five-file additions plus policy file,161 independent source checks, and524 finite checks across all16 named groups/140 cases. All263 fixture records remain conditional; no actual campaign credential, class/lineage option or cosmology was created. No unchanged ACQ-04 re-review is requested.

The remaining partial prerequisite identity now has110 local checks: four successful Animal Companion completed-hour histories with the actual finite body templates and separately paid Warrior4 parent/Warrior8 Companion Training child;30 total recorded histories. All335 original identities now have disjoint finite partial prerequisite evidence. This is NOT335 complete acquisitions, full use validation or your approval of these newer local reports.

While moving from successful acquisition witnesses to complete use/attempt procedures, I found three concrete boundaries in the existing Animal Companion wording that the successful-hour tests deliberately do not decide. Please resolve this narrow operational question from the attached full sources, preferring KEEP and an exact source citation where already controlled. The packet includes both full335 candidate envelopes, complete current contracts/shared rules/supplements, the complete general-combat reader/source-audit chapters, current Ranger class, reviewed expedition books, and the full local companion report/model. Prior originals and flags remain unchanged.

1. First purchase versus first bond. The procedure starts “NEW acquisition: with actual Animal Handling proficiency, select one already real willing/tamed Beast…” and then requires an uninterrupted touch hour, one bond attempt per completedLR. FS-01 requires a real earned unspent feat opportunity; FS-06 initializes limited-use feats with their full finite allowance. At which exact boundary is the feat opportunity committed and permanent feat ownership established? Can the feat be purchased before an eligible animal is available, with no companion until a later valid hour, or are eligible body and completed hour conditions of the purchase itself? If an hour is part of initial acquisition, specify reservation/commit/cancellation semantics only as needed. Do not invent an animal, access, consent or a bonus feat opportunity.

2. Bond attempt timing and interruption. At which exact event does the one attempt become spent? What persists if contact/access/willingness/body eligibility is lost or the owner is incapacitated during the hour? Is another attempt possible in that same allowance epoch, and what happens to any old bond if a replacement attempt fails? Resolve initial allowance versus a genuinely new completed beneficial Long Rest without scene/reset exploits. Retain the actual hour, physical body/ordinary HP/conditions and finite rest limits. Do not silently turn validation rejection of a claimed completed record into an actual attempt refund: the attached model expressly makes no such assertion.

3. Transfer/rebond versus nonrepeatability. The same procedure says “transferring requires actual release and new paid acquisition,” while FS-01 makes Animal Companion nonrepeatable and the procedure permits a new real animal plus full hour after release/death and a new completedLR. Identify what “paid acquisition” means for (a) an existing feat owner replacing a released/dead companion, (b) a different owner who already owns this feat, and (c) a receiving owner without this feat or using a Ranger bond. A replacement must not require an illegal second purchase of the same nonrepeatable feat, yet cannot create a free receiver feat, animal, Ranger grant, healing, or extra body/controller/phase. Keep each receiving engine's actual costs and permissions; do not invent a universal transfer currency or reopen reviewed EX58 command/mount rules.

Please give a single deterministic lifecycle covering a successful first bond, interrupted first attempt, retry before/after a beneficialLR, replacement with an existing bond, release/death, and a transfer with/without the receiving feat. If existing text is sufficient, cite the complete controlling clauses. If an explicit NEW completion or wording repair is necessary, provide exact minimal text and guarded derived locations, preserving originalObject, prerequisite trees, historical text, all unrelated cards and approval/selection flags. Give finite acceptance expectations; distinguish authored expectations from tests you actually executed. Do not approve the whole feat candidate, implement the CRPG, create an extra owner-confirmation gate or reopen ACQ-03/04.

The owner CRPG direction and unchanged twelve-character/parallel-activity/host-permission expedition remain controlling. Completed scopes carry forward. Final actual joint whole-game flow -> authorized commit/push -> verified remote -> careful cosmology and preservation-based cleanup remain in their agreed phases.
'''
    request.write_text(prompt, encoding='utf-8', newline='\n')
    files = [request,
        R / 'data/public/feat_candidates/exact_01/candidate.json', R / 'data/director/feat_candidates/exact_01/candidate.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json', R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'docs/feats/exact-candidate-01/GENERAL_COMBAT.md', R / 'docs/feats/exact-candidate-01/source-audit/GENERAL_COMBAT.md',
        R / 'data/playtest/character_foundation.json', R / 'data/public/class_playtests/ranger.json',
        R / 'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md', R / 'docs/mechanics/expedition/EXPEDITION_DIRECTOR_BOOK.md',
        R / 'docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT327_ACQ_04_FINITE_FULFILLMENT.json',
        A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_POLICY.json', A / 'FEAT_EXACT_01_COMPANION_ACQUISITION_CHECK.json',
        A / 'FEAT_EXACT_01_COMPANION_ACQUISITION_NOTES.md', R / 'tools/feat_exact_01_companion_acquisition_model.py',
        R / 'tools/validate_feat_exact_01_companion_acquisitions.py',
        A / 'FEAT_EXACT_01_PARTIAL_PREREQUISITE_COVERAGE_INDEX.json', A / 'OWNER_CRPG_DIRECTION_VISIBLE_CAPTURE_2026-10-13.json']
    manifest = {p.relative_to(G).as_posix(): {k: v for k, v in info(p).items() if k != 'path'} for p in files}
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.writestr(p.relative_to(G).as_posix(), p.read_bytes())
        z.writestr('PACKAGE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist()) == set(manifest) | {'PACKAGE_MANIFEST.json'}
        for p in files:
            assert z.read(p.relative_to(G).as_posix()) == p.read_bytes()
    write_new(receipt, {'preparedAtUtc': datetime.now(timezone.utc).isoformat(), 'id': 'FEAT327-ACQ-05',
        'status': 'prepared-not-submitted', 'request': info(request), 'archive': info(archive),
        'payloads': len(files), 'manifest': manifest, 'newRuleAdopted': False, 'sourceInformationDeleted': False})
    print(json.dumps({'request': info(request), 'archive': info(archive), 'payloads': len(files), 'receipt': info(receipt)}, indent=2))


if __name__ == '__main__':
    main()
