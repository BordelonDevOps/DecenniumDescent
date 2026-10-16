"""Apply the exact Part 3 confirmed EPI01-07 candidate, retaining every source."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    folder = A / 'cosmology-epilogue-character-01-local-candidate'
    candidate = folder / 'EPILOGUE_CHARACTER_MODEL.json'
    confirmation = A / 'COSMOLOGY_EPILOGUE_CHARACTER_01_LOCAL_PATCH_01_CONFIRMATION_DOM.txt'
    archive = A / 'DD_Cosmology_Epilogue_Character_01_Local_Patch_01.zip'
    source_check = A / 'COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_integrated.json'
    patch_check = A / 'COSMOLOGY_EPILOGUE_CHARACTER_01_LOCAL_PATCH_01_VALIDATION.json'
    target = R / 'data/director/cosmology/epilogue_character_reviewed_01.json'
    cases = R / 'data/director/cosmology/epilogue_character_cases_01.json'
    player = R / 'docs/mechanics/COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md'
    director = R / 'docs/director-only/cosmology/EPILOGUE_CHARACTER_REVIEWED_01.md'
    receipt = A / 'COSMOLOGY_EPILOGUE_CHARACTER_01_APPLICATION_CHECK.json'
    assert all(not p.exists() for p in [target, cases, player, director, receipt])
    assert info(candidate)['sha256'] == 'd1c05493cbdcaf891d512f9c77ddaf53da8d6b6d6a24405aa97fe0ead3ae7d6d'
    assert info(archive)['sha256'] == 'd5baaf59b18d06d736d71fb0b1ec137c9ea2b096b775e0c3349872b39d5137fb'
    seen = confirmation.read_text('utf-8')
    assert info(candidate)['sha256'] in seen and info(archive)['sha256'] in seen
    assert all(f'LP{i:02d} — CONFIRM.' in seen for i in range(1, 11))
    assert 'no concrete remaining blocker' in seen
    assert 'ACCEPT the exact local candidate' in seen
    assert read(source_check)['checkCount'] == 444 and read(source_check)['failureCount'] == 0
    assert read(patch_check)['checkCount'] == 11 and read(patch_check)['failureCount'] == 0
    original = read(candidate)
    model = deepcopy(original)
    before = model['status']
    model['status'] = 'Jointly confirmed and locally adopted NEW provisional EPI01–07 authored playtest module. Original sources and explicit owner corrections retain authority; all approval gates remain unchanged.'
    casebook = read(folder / 'CASEBOOK.json')
    assert casebook['count'] == 110 == len(casebook['cases'])
    prior = read(A / 'cosmology-epilogue-character-01-return-integrated/CASEBOOK.json')
    assert {x['id'] for x in prior['cases']} <= {x['id'] for x in casebook['cases']}
    assert len({x['id'] for x in casebook['cases']}) == 110
    now = datetime.now(timezone.utc).isoformat()
    data = {
        'id': 'COSMOLOGY-EPILOGUE-CHARACTER-REVIEWED-01', 'recordedAtUtc': now,
        'status': 'Current NEW provisional authored playtest reference, jointly reviewed in actual Calibration Review Part3.',
        'authority': 'Original manuscripts govern source reading subject to explicit owner corrections. New operating rules and scenes below are authored adaptations, not recovered cosmological canon.',
        'scope': 'EPI01–07: home affiliations, seven Choir motifs, personal vows, seventeen class mask keys, Conflict Die, Witness petitions and seven challenges, Concord visits, finite Sentinel information.',
        'confirmedCandidate': info(candidate), 'confirmedArchive': info(archive), 'confirmation': info(confirmation),
        'currentModule': model, 'statusLabelChangeOnly': {'before': before, 'after': model['status']},
        'casebook': info(folder / 'CASEBOOK.json'),
        'sourceBindings': read(folder / 'SOURCE_HASHES.json'),
        'validation': {'sourceChecks': 444, 'localPackagePreservationChecks': 11, 'failureCount': 0,
                       'sourceCheck': info(source_check), 'localCheck': info(patch_check),
                       'authoredCases': 110, 'runtimeTestsExecuted': 0, 'humanPlaytested': False},
        'preservedReturnHistory': [info(A / name) for name in [
            'DD_Cosmology_Epilogue_Character_01_Return_01.zip',
            'DD_Cosmology_Epilogue_Character_01_Return_revised.zip',
            'DD_Cosmology_Epilogue_Character_01_Return_integrated.zip']],
        'notAdopted': ['EPI08–17 mechanics', 'Campaign epoch', 'Cosmological identity resolutions',
                       'Pending spells or broader class, feat, bestiary or crafting approval',
                       'Runtime, human playtesting, balance, whole-game or publication approval'],
        'sourceInformationDeleted': 0, 'campaignEpochChosen': False, 'fullCosmologyClosed': False,
        'published': False,
    }
    for p in [target, cases, player, director]:
        p.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(encoded(data))
    cases.write_bytes((folder / 'CASEBOOK.json').read_bytes())
    player.write_bytes((folder / 'PLAYER_CHAPTER.md').read_bytes())
    director.write_bytes((folder / 'DIRECTOR_CHAPTER.md').read_bytes())
    saved = read(target)
    reverted = deepcopy(saved['currentModule'])
    reverted['status'] = before
    assert reverted == original
    assert saved['currentModule']['approvalGates'] == original['approvalGates']
    copies = [(cases, 'CASEBOOK.json'), (player, 'PLAYER_CHAPTER.md'), (director, 'DIRECTOR_CHAPTER.md')]
    checks = [
        {'name': 'Current model equals exact confirmed candidate except recorded status label', 'pass': reverted == original},
        {'name': 'Approval gates unchanged', 'pass': saved['currentModule']['approvalGates'] == original['approvalGates']},
        *[{'name': f'{name} byte-identical to confirmed candidate', 'pass': dest.read_bytes() == (folder / name).read_bytes()} for dest, name in copies],
        {'name': 'All107 integrated case IDs preserved among110 unique authored cases', 'pass': True},
    ]
    receipt.write_bytes(encoded({
        'recordedAtUtc': now, 'confirmation': info(confirmation), 'confirmedCandidate': info(candidate),
        'data': info(target), 'playerChapter': info(player), 'directorChapter': info(director), 'casebook': info(cases),
        'sourceCheck': info(source_check), 'localPackageCheck': info(patch_check),
        'applicationChecks': checks, 'applicationCheckCount': len(checks), 'failureCount': 0,
        'sourceChecks': 444, 'localPackagePreservationChecks': 11, 'authoredCases': 110,
        'newProvisionalModuleAdopted': True, 'sourceInformationDeleted': 0,
        'runtimeTestsExecuted': 0, 'humanPlaytested': False, 'campaignEpochChosen': False,
        'wholeGameApproved': False, 'fullCosmologyClosed': False, 'published': False,
    }))
    print(json.dumps({'application': info(receipt), 'data': info(target), 'player': info(player),
                      'director': info(director), 'casebook': info(cases), 'failureCount': 0}))


if __name__ == '__main__':
    main()
