"""Check EX58 preservation, audience projection and complete rendering.

The projection below reads the complete Director candidate, never the assembled
public candidate. Equality is a packaging check, not proof of mechanical balance.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import copy
import importlib.util
import json
import re
import zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
D = R / 'docs/mechanics/expedition'
NAMES = [f'part{n:02d}' for n in range(1, 7)] + ['transport_profiles', 'integrated_flow', 'boundary_records', 'social_scenarios']
BASE = 'schemaVersion moduleId status notice questionIds completeExpeditionCandidate selectionEnabled sections'.split()
FIELDS = {f'part{n:02d}': BASE[:] for n in range(1, 7)}
FIELDS['part05'] += ['catalogue']
FIELDS['part06'] += ['backgroundStartingRules']
FIELDS['transport_profiles'] = 'schemaVersion moduleId status notice selectionEnabled newPromotions profiles auxiliaryProfiles'.split()
FIELDS['integrated_flow'] = 'schemaVersion id status completeExpeditionCandidate selectionEnabled evidenceBoundary readingNote correctionsToOriginalWorkedOutline rosterAndBodies offices provisions consumption lighting route retreat extraction HavenSteps providers money standing factionWork rest nextProcurement events contractInstances actorReservations finalState remainingExamples sourceBindings'.split()
FIELDS['boundary_records'] = 'schemaVersion status selectionEnabled completeExpeditionCandidate evidenceScope cases sourceBindings sourceSpecificDependencies remainingAssembly'.split()
FIELDS['social_scenarios'] = 'schemaVersion status selectionEnabled completeExpeditionCandidate cases sourceBindings evidenceScope remainingWork'.split()
TITLES = ['Charters, time and provisions', 'Routes, extraction and retreat', 'Haven, settlement and advancement', 'Social scenes and faction work', 'Mounts, vehicles and transport', 'Reputation and background standing']


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def info(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def project(internal):
    components = {}
    assert set(internal['completeComponents']) == set(NAMES)
    for name in NAMES:
        candidate = internal['completeComponents'][name]['publicEnvelope']
        if set(candidate) != set(FIELDS[name]):
            raise ValueError('Unexpected public fields in ' + name)
        components[name] = {k: copy.deepcopy(candidate[k]) for k in FIELDS[name]}
    flow = components['integrated_flow']
    reading = {
        'chapters': [{'id': f'EX58-CHAPTER-{i+1:02d}', 'title': TITLES[i],
                      'sections': copy.deepcopy(components[f'part{i+1:02d}']['sections'])}
                     for i in range(6)],
        'backgroundStartingRules': copy.deepcopy(components['part06']['backgroundStartingRules']),
        'transportProfiles': copy.deepcopy(components['transport_profiles']['profiles']),
        'auxiliaryProfiles': copy.deepcopy(components['transport_profiles']['auxiliaryProfiles']),
        'integratedFlow': {k: copy.deepcopy(flow[k]) for k in FIELDS['integrated_flow']
                           if k not in ['status', 'completeExpeditionCandidate', 'remainingExamples', 'readingNote']},
        'boundaryCases': copy.deepcopy(components['boundary_records']['cases']),
        'socialCases': copy.deepcopy(components['social_scenarios']['cases']),
    }
    return {
        'schemaVersion': 'EX58-complete-candidate-v1', 'id': 'EX58-EXACT-CANDIDATE-01',
        'status': 'Complete EX58 authored assembly; exact GPT candidate review pending',
        'selectionEnabled': False, 'newPromotions': 0, 'completeExpeditionAuthoredAssembly': True,
        'exactCandidateApproved': False, 'runtimeImplemented': False, 'humanPlaytestConfirmed': False,
        'componentNoticePolicy': 'Complete component envelopes are historical receipts. Their notices describe the stage when each was authored. The reading object is the current assembled reading path; no historical text was overwritten.',
        'components': components, 'reading': reading,
    }


def main():
    checks = []
    def check(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
    assembly = read(A / 'EX58_EXACT_CANDIDATE_ASSEMBLY.json')
    for path, expected in assembly['inputs'].items():
        check('Assembly input bytes unchanged: ' + path, info(G/path) == expected)
    for path, expected in assembly['outputs'].items():
        check('Assembly output bytes match receipt: ' + path, info(G/path) == expected)
    public = read(R/'data/public/expedition_candidate/complete_candidate.json')
    internal = read(R/'data/director/expedition_candidate/complete_candidate.json')
    reconstructed = project(internal)
    check('Complete independently reconstructed public JSON, including every field and metadata value', public == reconstructed)
    # An extra Director-only root must have no public effect. Unknown public fields fail closed.
    probe = copy.deepcopy(internal)
    probe['completeComponents']['part04']['PRIVATE_AUDIENCE_PROBE'] = {'secret': 'PRIVATE-EX58-DO-NOT-PUBLISH'}
    check('Director-only extra data excluded from whole projection', project(probe) == reconstructed)
    probe['completeComponents']['part04']['publicEnvelope']['PRIVATE_AUDIENCE_PROBE'] = 'reject'
    try:
        project(probe)
        rejects_unknown = False
    except ValueError:
        rejects_unknown = True
    check('Unexpected public field rejects projection', rejects_unknown)
    del probe
    for name in NAMES:
        check('Entire public component retained: ' + name, public['components'][name] == read(R/f'data/public/expedition_candidate/{name}.json'))
        check('Entire Director component retained: ' + name, internal['completeComponents'][name] == read(R/f'data/director/expedition_candidate/{name}.json'))
    for target, name in [('currentCorrectedContracts', 'source_contracts_corrected'),
                          ('currentCorrectedRegister', 'source_register_corrected'),
                          ('currentCorrectedConflicts', 'source_conflicts_corrected')]:
        check('Complete current source ' + target, internal[target] == read(R/f'data/director/expedition_candidate/{name}.json'))
    expected_ids = [f'FL-{n:02d}' for n in range(1, 27)] + [f'SO-{n:02d}' for n in range(1, 13)] + [f'TR-{n:02d}' for n in range(1, 15)] + [f'RP-A{n:02d}' for n in range(1, 7)]
    section_ids = [s['id'] for ch in public['reading']['chapters'] for s in ch['sections']]
    check('All 58 distinct directions in source reading order', section_ids == expected_ids)
    player_text = (D/'EXPEDITION_PLAYER_BOOK.md').read_text(encoding='utf-8')
    director_text = (D/'EXPEDITION_DIRECTOR_BOOK.md').read_text(encoding='utf-8')
    for n in range(1, 7):
        name = f'part{n:02d}'
        for s in public['components'][name]['sections']:
            check('Complete player section text ' + s['id'], s['text'] in player_text)
        for s in internal['completeComponents'][name]['directorModule']['sections']:
            check('Complete Director section text ' + s['id'], s['text'] in director_text)
    chapter_cases = []
    for n in range(1, 7):
        module = internal['completeComponents'][f'part{n:02d}']['directorModule']
        chapter_cases += module['workedCases']
        for family in module.get('familyCases', []):
            chapter_cases += family['cases']
    check('All 190 distinct chapter cases retained', len(chapter_cases) == len({c['id'] for c in chapter_cases}) == 190)
    for c in chapter_cases:
        check('Full situation and outcome rendered ' + c['id'], c['given'] in director_text and c['expected'] in director_text)
    for name, count in [('boundary_records', 28), ('social_scenarios', 24)]:
        cases = public['components'][name]['cases']
        check('All distinct ' + name, len(cases) == len({c['id'] for c in cases}) == count)
        for c in cases:
            check('Complete worked record and explanation ' + c['id'], c['readerExplanation'] in player_text and json.dumps(c, ensure_ascii=False, indent=2) in director_text)
    flow = public['reading']['integratedFlow']
    check('All 21 distinct expedition events', len(flow['events']) == len({e['id'] for e in flow['events']}) == 21)
    check('All 15 exact contract families', set(flow['contractInstances']) == {f'EC-{n:02d}' for n in range(1, 16)})
    for c in internal['currentCorrectedContracts']['contracts']:
        check('Complete corrected contract rendered ' + c['id'], json.dumps(c, ensure_ascii=False, indent=2) in director_text)
        check('Actual flow contract contains every required field ' + c['id'], set(c['requiredFields']).issubset(flow['contractInstances'][c['id']]['fields']))
    correction = flow['correctionsToOriginalWorkedOutline'][0]
    check('Feeding correction kept explicit and pending', correction['id'] == 'FLOW-C01' and correction['result']['netAdditionalSecondsToHaven'] == 3540 and 'pending' in correction['status'])
    source_profiles = internal['completeComponents']['transport_profiles']['completeOriginalProfileEnvelope']
    check('All 29 profiles and 4 auxiliaries', len(public['reading']['transportProfiles']) == 29 and len(public['reading']['auxiliaryProfiles']) == 4)
    for original, candidate in zip(source_profiles['profiles'], public['reading']['transportProfiles']):
        check('All transport operating fields ' + candidate['id'], candidate == {k: original[k] for k in ['id', 'name', 'kind', 'operationalStatus', 'operational']})
    check('Complete auxiliary values', public['reading']['auxiliaryProfiles'] == source_profiles['auxiliaryProfiles'])
    cls = internal['completeComponents']['part04']['completeClassDatasetEnvelopes']
    check('All 17 class envelopes and 1223 cards', len(cls) == 17 and sum(len(c['completeEnvelope']['cards']) for c in cls) == 1223)
    for c in cls:
        check('Full class source bytes ' + c['path'], info(G/c['path']) == {k: c[k] for k in ['bytes', 'sha256']})
        check('Full class source object ' + c['path'], read(G/c['path']) == c['completeEnvelope'])
    interfaces = internal['completeComponents']['part04']['completeClassInterfaceDisposition']['classFiles']
    check('All 94 selected full class comparisons', sum(len(c['selectedFullCards']) for c in interfaces) == 94)
    rep = internal['completeComponents']['part06']['completeReputationSourceBinding']
    check('All 44 full faction records, 20 backgrounds and 12 source probes', len(rep['fullOriginalFactionRecords']) == 44 and len(rep['backgrounds']) == 20 and len(rep['rawSourceProbes']) == 12)
    check('All 20 public background clauses', len(public['reading']['backgroundStartingRules']) == 20)
    public_serialized = json.dumps(public, ensure_ascii=False, sort_keys=True)
    for i, dossier in enumerate(rep['fullOriginalFactionRecords']):
        check('Full private faction dossier absent from public ' + str(i+1), json.dumps(dossier, ensure_ascii=False, sort_keys=True) not in public_serialized)
    check('Private rival frame absent from public', json.dumps(internal['completeComponents']['boundary_records']['privateSyntheticRivalFrameForW27'], ensure_ascii=False, sort_keys=True) not in public_serialized)
    # The separate renderers consume the independently reconstructed full projection.
    spec = importlib.util.spec_from_file_location('ex58_assembly_renderer', Path(__file__).with_name('assemble_ex58_exact_candidate.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    check('Entire player book rendering from reconstructed projection', player_text == mod.render_player(reconstructed))
    check('Entire Director book rendering from complete internal object', director_text == mod.render_director(internal))
    # The frozen archive is a separate authority from current component copies.
    prep = read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')
    source_zip = G/prep['archive']['path']
    check('Original V3 ZIP exact bytes', info(source_zip) == {k: prep['archive'][k] for k in ['bytes', 'sha256']})
    with zipfile.ZipFile(source_zip) as z:
        check('Exactly 304 original source payloads', len(prep['manifest']) == 304)
        for path, expected in prep['manifest'].items():
            b = z.read(path)
            check('Original source archive payload ' + path, {'bytes': len(b), 'sha256': sha256(b).hexdigest()} == expected)
            if (G/path).is_file():
                check('Original local source payload ' + path, info(G/path) == expected)
    manifest = read(A/'ex58-final-gpt-verdict/FILE_MANIFEST.json')
    for item in manifest['files']:
        check('Original GPT final payload ' + item['path'], info(A/'ex58-final-gpt-verdict'/item['path']) == {k: item[k] for k in ['bytes', 'sha256']})
    for path, expected in assembly['inputs'].items():
        check('Source stable through validation ' + path, info(G/path) == expected)
    failures = [x for x in checks if not x['passed']]
    result = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'candidateId': public['id'],
        'status': 'Pass' if not failures else 'FAIL', 'checks': len(checks), 'failures': failures,
        'scope': 'Complete source/component byte preservation, exact whole public allowlist projection, all section/case rendering, complete profile/class/faction receipt equality and frozen-source integrity. These are packaging and reference checks, not an independent semantic verdict, gameplay execution, save migration or human balance evidence.',
        'counts': {'sourceDirections': 58, 'chapterExamples': 190, 'integratedEvents': 21, 'contractFamilies': 15, 'boundaryInstances': 28, 'originalSocialInstances': 24, 'profiles': 29, 'auxiliaries': 4, 'factionRecords': 44, 'backgrounds': 20, 'sourceReputationProbes': 12, 'classEnvelopes': 17, 'classCards': 1223, 'selectedClassCards': 94},
        'outputsVerified': assembly['outputs'],
        'validator': {'path': Path(__file__).resolve().relative_to(G).as_posix(), **info(Path(__file__))},
        'newPromotions': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0,
        'exactGPTReviewCompleted': False, 'pushPerformed': False, 'cosmologyReviewed': False,
        'details': checks,
    }
    target = A/'EX58_EXACT_CANDIDATE_CHECK.json'
    assert not target.exists(), 'Preserve previous validation receipt before replacing.'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: result[k] for k in ['status', 'checks', 'failures', 'counts']}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
