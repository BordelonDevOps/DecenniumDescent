"""Prepare a bounded source conference for remaining external credentials."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def binding(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def main():
    question = A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_QUESTION.txt'
    evidence = A / 'FEAT327_ACQ_04_SOURCE_EVIDENCE.json'
    archive = A / 'DD_FEAT327_ACQ04_External_Credentials_Source.zip'
    preparation = A / 'FEAT327_ACQ_04_PREPARATION.json'
    assert all(not path.exists() for path in [question, evidence, archive, preparation])
    foundation_path = R / 'data/playtest/character_foundation.json'
    ancestry_path = R / 'data/playtest/ancestry_background_candidate.json'
    contracts_path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    foundation = read(foundation_path); ancestry = read(ancestry_path)
    contracts = {c['id']: c for c in read(contracts_path)['records']}
    class_paths = [G / c['classCandidatePath'] for c in foundation['classes']]
    source_paths = [foundation_path, ancestry_path, contracts_path,
        R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        R / 'data/public/feat_candidates/exact_01/supplements.json',
        A / 'FEAT327_ACQ_03_GPT_ADDENDUM.md', A / 'FEAT327_ACQ_03_FINITE_FULFILLMENT.json',
        A / 'OWNER_CRPG_DIRECTION_VISIBLE_CAPTURE_2026-10-13.json', *class_paths]
    selected_cards = []
    for path in class_paths:
        for index, card in enumerate(read(path)['cards']):
            if card['id'] in {'druid.hero.moon.mooncursed', 'warrior.supplement.berserker-brew', 'paladin.supplement.oath-of-vengeance.vengeful-smite'}:
                selected_cards.append({'file': binding(path), 'pointer': '/cards/' + str(index), 'completeCard': card})
    assert len(selected_cards) == 3
    source = {
        'preparedAtUtc': datetime.now(timezone.utc).isoformat(), 'id': 'FEAT327-ACQ-04',
        'status': 'prepared-source-question-no-ruling-adopted', 'sourceBindings': [binding(p) for p in source_paths],
        'completeCredentialContracts': [contracts[s] for s in ['frenzied_rage', 'divine_favor', 'elemental_body', 'dragon_blood']],
        'completeBerserkerParent': contracts['berserker'], 'completeRelevantClassCards': selected_cards,
        'actualClassNames': [c['class'] for c in foundation['classes']],
        'actualLineages': [{'id': a['id'], 'name': a['name'], 'variants': [{'id': v['id'], 'name': v['name']} for v in a['variants']]} for a in ancestry['ancestries']],
        'observation': 'The supplied current Mooncursed procedure has a conditional bite damage die, not an expressly granted rage state. Its preserved original says Lunar Rage. Berserker Brew is a serum profile; Vengeful Smite uses rage only in a conduct clause. The complete17 class payloads are supplied so the reviewer can inspect beyond these search hits.',
        'limits': 'This packet asks for current-catalog eligibility and external-evidence fixture dispositions. It does not request a new class, ancestry, deity, plane, bloodline, world event, runtime or full feat approval.'}
    evidence.write_text(json.dumps(source, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    prompt = '''FEAT327-ACQ-04 — remaining external-credential dispositions

I have read the owner's newer CRPG direction and twelve-character/parallel-activity/host-permission correction. Carry those forward. We are finishing the same system specification; software conversion is later, and manual tabletop bookkeeping is not a completion gate. Completed crafting, language, teaching and EX58 scopes stay completed unless a concrete new conflict appears. Final joint flow agreement -> authorized push/commit -> verified remote -> careful cosmology review and preservation-based repository cleanup remain in their ordered phases.

ACQ-03 is fulfilled locally: eight exact source descendants,175 independent source checks and113 finite A-H/snapshot controls. A later local mixed-prerequisite pass records34 additional partial identities,336 checks and73 conditional snapshots. The ledger has326 partial prerequisite identities and9 remaining; these are NOT326 complete acquisitions or your approval of these newer reports. I am completing the ordinary parent choices and Tinkering progression independently.

This is one bounded request for dispositions needed to finish the four attached credential contracts. Please inspect FEAT327_ACQ_04_SOURCE_EVIDENCE.json and the full bound class/ancestry/shared sources in this ZIP. The packet includes17 complete current class payloads, the actual character foundation and14 ancestry/45 variant catalog, the current full335 contracts, current shared rules and supplements, and your actual ACQ-03 addendum/finite local receipt. No old source is deleted or replaced.

1. Frenzied Rage. The exact complete procedure already requires an actual acquired class feature expressly granting a rage state; it explicitly excludes name-only Mooncursed/Berserker Brew/prestige/damage-buff qualification. The attached full Mooncursed card's preserved original mentions Lunar Rage, while its operative effect is a bite die under a real full moon, without an expressly granted rage state. Berserker Brew is a serum buff and the Paladin rage hit is oath conduct prose. Please give the current-source disposition: can any actual supplied class card establish this branch, or should these specific candidates fail it while the real paid Berserker-feat route remains available? If a supplied card qualifies, identify its exact ID/pointer, operative grant and required acquisition history. Do not create a class rage, silently alias a name, remove the printed OR branch, or treat the separate CF-03 operating rage as its own acquisition proof.

2. Divine Favor and Elemental Body. Keep their already-established worship/actual exposure eligibility as literal source receipts. We must not name, select, invent or interpret a deity/plane/event before the ordered cosmology work. Does finishing this pre-push specification mean: validate the record contract using explicitly conditional, opaque test-world fixtures and reject missing/unbound/mismatched evidence, while never claiming that those fixtures establish actual campaign history or approve cosmology? Or is a different finite pre-push disposition required? Give the exact minimal fields and acceptance boundary if a completion is needed. An unchecked bool or a nonempty invented story label must not be sufficient. Character/world/authority linkage, timing before acquisition and exact predicate evidence should be distinguished from the existence of a source file.

3. Dragon Blood. Current supplied lineages/classes do not supply literal Dragonborn or Sorcerer as current options; Drakari, Mage and the feat-only Sorcerer curriculum are not aliases. The full procedure already says it is not selectable without a controlling source establishing the qualifying lineage/class-bloodline and one recorded damage type. Please confirm or correct a finite disposition that preserves the full feat and printed prerequisite, rejects current false aliases and stays unavailable to actors lacking the exact external source. If mechanically exercising a hypothetical imported legacy record is admissible as a conditional interface test, keep it visibly separate from granting a new selectable lineage/class or authenticating a campaign record.

4. Closure scope. Please distinguish a complete source/predicate-interface specification with honest conditional fixtures and guarded unavailable current content from an invented positive source or an incomplete branch hidden by tests. State what finite evidence closes these particular acquisition questions for the later exact feat review. Do not approve all335 acquisitions, resource/use procedures, the full candidate, gameplay implementation or human balance, and do not reopen ACQ-03 or require a generic unchanged archive review.

Prefer KEEP where the existing complete procedures already resolve the matter. If any NEW shared wording is necessary, supply exact text and exact minimal derived locations; preserve originals, Boolean alternatives, ability/payment gates, deferred payloads and all current approval/selection flags. No cosmology interpretation is requested or authorized here.
'''
    question.write_text(prompt, encoding='utf-8', newline='\n')
    payloads = source_paths + [evidence, question]
    assert len({p.relative_to(G).as_posix() for p in payloads}) == len(payloads)
    manifest = {p.relative_to(G).as_posix(): {'bytes': p.stat().st_size, 'sha256': binding(p)['sha256']} for p in payloads}
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in payloads:
            z.write(path, path.relative_to(G).as_posix())
        z.writestr('PACKAGE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    with zipfile.ZipFile(archive) as z:
        for name, expected in manifest.items():
            data = z.read(name)
            assert len(data) == expected['bytes'] and sha256(data).hexdigest() == expected['sha256']
    for path, before in zip(source_paths, source['sourceBindings']):
        assert binding(path) == before
    receipt = {'preparedAtUtc': datetime.now(timezone.utc).isoformat(), 'id': 'FEAT327-ACQ-04',
        'status': 'prepared-not-submitted', 'request': binding(question), 'sourceEvidence': binding(evidence),
        'archive': binding(archive), 'payloadCount': len(payloads), 'allPayloadsVerified': True,
        'sourceFilesUnchanged': len(source_paths), 'sourceInformationDeleted': False,
        'rulingAdopted': False, 'cosmologyReviewed': False}
    preparation.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
