"""Assemble the saved EX58 drafts without rewriting any component or source.

This publishes a local review candidate, not a rules approval or a game runtime.
Run validate_ex58_exact_candidate.py separately after assembly.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import copy
import importlib.util
import json
import re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
D = R / 'docs/mechanics/expedition'
NAMES = [f'part{n:02d}' for n in range(1, 7)] + [
    'transport_profiles', 'integrated_flow', 'boundary_records', 'social_scenarios']
TITLES = ['Charters, time and provisions', 'Routes, extraction and retreat',
          'Haven, settlement and advancement', 'Social scenes and faction work',
          'Mounts, vehicles and transport', 'Reputation and background standing']
STATUS = 'Complete EX58 authored assembly; exact GPT candidate review pending'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def info(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def binding(p):
    return {'path': p.relative_to(G).as_posix(), **info(p)}


def anchor(s):
    return re.sub(r'[^a-z0-9-]', '', s.lower())


def label(s):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', s).replace('_', ' ').capitalize()


def pretty(v):
    return json.dumps(v, ensure_ascii=False, indent=2)


def record(v):
    return ['```json', pretty(v), '```', '']


def clock(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f'{h:02}:{m:02}:{s:02}'


def current_reading(components):
    """Select current content, leaving historical completion notices in receipts."""
    return {
        'chapters': [dict(id=f'EX58-CHAPTER-{n:02d}', title=TITLES[n-1],
                          sections=copy.deepcopy(components[f'part{n:02d}']['sections']))
                     for n in range(1, 7)],
        'backgroundStartingRules': copy.deepcopy(components['part06']['backgroundStartingRules']),
        'transportProfiles': copy.deepcopy(components['transport_profiles']['profiles']),
        'auxiliaryProfiles': copy.deepcopy(components['transport_profiles']['auxiliaryProfiles']),
        'integratedFlow': {k: copy.deepcopy(v) for k, v in components['integrated_flow'].items()
                           if k not in {'status', 'completeExpeditionCandidate', 'remainingExamples', 'readingNote'}},
        'boundaryCases': copy.deepcopy(components['boundary_records']['cases']),
        'socialCases': copy.deepcopy(components['social_scenarios']['cases']),
    }


def render_player(public):
    p = public['reading']
    out = ['# Decennium Descent — Expedition Player Book', '',
           'Review candidate. These six chapters form one reading path for expedition play, transport, social scenes and standing. Exact GPT review remains pending. Use the existing Core rules alongside this book.', '',
           'The worked records describe synthetic situations. They demonstrate intended rules and accounting; they are not playtest results.', '',
           '## Reading order', '']
    for n, ch in enumerate(p['chapters'], 1):
        out += [f'{n}. [{ch["title"]}](#chapter-{n})']
    out += ['7. [Complete transport catalogue](#transport-catalogue)',
            '8. [One complete expedition](#complete-expedition)',
            '9. [Boundary walkthroughs](#boundary-walkthroughs)',
            '10. [Social walkthroughs](#social-walkthroughs)', '',
            '## Timing change awaiting review', '',
            'The integrated example explicitly reserves two 30-minute feeding stops. One includes a previously counted one-minute lamp refill, so the itinerary gains 59 minutes. Haven entry becomes 17:23:12 and the first safe Rest finishes at 29:03:12. These are the circumstances of this example; they do not establish a universal meal duration.', '']
    for n, ch in enumerate(p['chapters'], 1):
        out += [f'<a id="chapter-{n}"></a>', f'## {n}. {ch["title"]}', '']
        for s in ch['sections']:
            out += [f'<a id="{anchor(s["id"])}"></a>', f'### {s["id"]} — {s["title"]}', '', s['text'], '']
    out += ['### Complete background starting clauses', '',
            'The following clauses retain their full records and source wording. Apply the standing procedure above; the records do not initialize a character twice.', '']
    for b in p['backgroundStartingRules']:
        out += record(b)
    # Reuse only the catalogue renderer, not its main() mutation path.
    spec = importlib.util.spec_from_file_location('ex58_catalogue_renderer', Path(__file__).with_name('build_ex58_transport_catalogue_candidate.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    catalogue = mod.render({'notice': '', 'profiles': p['transportProfiles'], 'auxiliaryProfiles': p['auxiliaryProfiles']})
    catalogue = catalogue[catalogue.index('## Catalogue index'):]
    out += ['<a id="transport-catalogue"></a>', '## Complete transport catalogue', '',
            'Use these provisional game profiles with Chapter 5. A price or listed crew requirement does not supply an actual animal, body, crew or berth. Each profile labels new operating values; original source rows and their blanks remain preserved in the Director data.', '', catalogue, '',
            '<a id="complete-expedition"></a>', '## One complete expedition', '',
            'Arin is Leader and Quartermaster; Bea is Routekeeper and walking driver; Cora is Claimant of Record; Dane is Surgeon. The mule pulls the cart. Named outside providers use their own contracted time.', '',
            '| Event | Start | Finish | What happens |', '|---|---|---|---|']
    flow = p['integratedFlow']
    for e in flow['events']:
        out += [f'| {e["id"]} | {clock(e["relativeStart"])} | {clock(e["relativeEnd"])} | {e["currentCandidateNarrative"].replace("|", "\\|")} |']
    out += ['', '### Settlement', ''] + record(flow['money'])
    out += ['### State before the next descent', ''] + record(flow['finalState'])
    out += ['The complete interval, supply, turn, policy, provider and contract records are preserved in the [public candidate data](../../../data/public/expedition_candidate/complete_candidate.json).', '',
            '<a id="boundary-walkthroughs"></a>', '## Boundary walkthroughs', '']
    for c in p['boundaryCases']:
        out += [f'### {c["id"]} — {c["title"]}', '', c['actualSyntheticPremises'], '', c['readerExplanation'], '',
                '**Recorded outcome**', ''] + record(c['expectedOutcomes'])
    out += ['<a id="social-walkthroughs"></a>', '## Social walkthroughs', '']
    for c in p['socialCases']:
        out += [f'### {c["id"]} — {c["title"]}', '', c['readerExplanation'], '',
                '**Recorded outcome**', ''] + record(c['expectedFinalState'])
    return '\n'.join(out).rstrip() + '\n'


def render_director(internal):
    out = ['# Decennium Descent — Expedition Director Book', '',
           'Read the [Expedition Player Book](EXPEDITION_PLAYER_BOOK.md) for the complete player procedures. This companion holds all Director procedures, worked chapter cases, record contracts and complete integrated examples. Exact GPT review remains pending.', '',
           'Source faction dossiers, full class envelopes, original proposals and conflict history remain in the [complete Director data](../../../data/director/expedition_candidate/complete_candidate.json). They are preserved as source evidence, not public player knowledge.', '',
           '## Reading order', '']
    for n, title in enumerate(TITLES, 1):
        out += [f'{n}. [{title}](#director-chapter-{n})']
    out += ['7. [Record contracts](#record-contracts)', '8. [Complete expedition records](#expedition-records)',
            '9. [Boundary records](#boundary-records)', '10. [Social records](#social-records)', '',
            '## Explicit review issue', '',
            'FLOW-C01 adds two supported feeding intervals to the preserved original example. Net elapsed time increases by 59 minutes. Review the entire revised chronology, including rest, light, provisions, faction work and provider schedules. The original outline is retained in completeComponents.integrated_flow.originalGPTIntegratedSequence.', '']
    for n, title in enumerate(TITLES, 1):
        d = internal['completeComponents'][f'part{n:02d}']['directorModule']
        out += [f'<a id="director-chapter-{n}"></a>', f'## {n}. {title}', '']
        for s in d['sections']:
            out += [f'### {s["id"]} — {s["title"]}', '', s['text'], '']
        out += ['### Worked chapter cases', '']
        for c in d['workedCases']:
            out += [f'#### {c["id"]}', '', '**Situation:** ' + c['given'], '', '**Expected result:** ' + c['expected'], '']
        for family in d.get('familyCases', []):
            out += [f'### {family["id"]}', '']
            for c in family['cases']:
                out += [f'#### {c["id"]} — {c["boundary"]}', '', '**Situation:** ' + c['given'], '', '**Expected result:** ' + c['expected'], '']
        for k in ['originalProposalScenarios', 'originalProbeBindings']:
            if k in d:
                out += [f'### {label(k)}', ''] + record(d[k])
    contracts = internal['currentCorrectedContracts']
    out += ['<a id="record-contracts"></a>', '## Record contracts', '',
            'These specify the candidate record fields. They are not an implemented application or save adapter.', '',
            '### Shared envelope', ''] + record(contracts['sharedRecordEnvelope'])
    out += ['### Numeric format', ''] + record(contracts['numericFormat'])
    for c in contracts['contracts']:
        out += [f'### {c["id"]} — {c["name"]}', ''] + record(c)
    out += ['<a id="expedition-records"></a>', '## Complete expedition records', '',
            'All event state, reservations, supplies, accounts and fifteen contract instances follow. Times share the stated epoch; reference arithmetic is distinct from execution in a game runtime.', '']
    flow = internal['completeComponents']['integrated_flow']['publicEnvelope']
    for k, v in flow.items():
        if k not in {'status', 'completeExpeditionCandidate', 'remainingExamples', 'readingNote'}:
            out += ['### ' + label(k), ''] + record(v)
    for name, title, aid in [('boundary_records', 'Boundary records', 'boundary-records'),
                             ('social_scenarios', 'Social records', 'social-records')]:
        out += [f'<a id="{aid}"></a>', '## ' + title, '']
        for c in internal['completeComponents'][name]['publicEnvelope']['cases']:
            out += [f'### {c["id"]} — {c["title"]}', ''] + record(c)
    return '\n'.join(out).rstrip() + '\n'


def main():
    outputs = {
        'public': R / 'data/public/expedition_candidate/complete_candidate.json',
        'director': R / 'data/director/expedition_candidate/complete_candidate.json',
        'playerBook': D / 'EXPEDITION_PLAYER_BOOK.md',
        'directorBook': D / 'EXPEDITION_DIRECTOR_BOOK.md',
        'assemblyReceipt': A / 'EX58_EXACT_CANDIDATE_ASSEMBLY.json',
    }
    assert not any(p.exists() for p in outputs.values()), 'Preserve the existing assembly before revision.'
    inputs = {}
    public_components, internal_components = {}, {}
    for name in NAMES:
        pp = R / f'data/public/expedition_candidate/{name}.json'
        dp = R / f'data/director/expedition_candidate/{name}.json'
        public_components[name], internal_components[name] = read(pp), read(dp)
        assert public_components[name] == internal_components[name]['publicEnvelope'], name
        inputs.update({p.relative_to(G).as_posix(): info(p) for p in [pp, dp]})
    for name in ['source_contracts_corrected', 'source_register_corrected', 'source_conflicts_corrected']:
        p = R / f'data/director/expedition_candidate/{name}.json'
        inputs[p.relative_to(G).as_posix()] = info(p)
    public = {
        'schemaVersion': 'EX58-complete-candidate-v1', 'id': 'EX58-EXACT-CANDIDATE-01',
        'status': STATUS, 'selectionEnabled': False, 'newPromotions': 0,
        'completeExpeditionAuthoredAssembly': True, 'exactCandidateApproved': False,
        'runtimeImplemented': False, 'humanPlaytestConfirmed': False,
        'componentNoticePolicy': 'Complete component envelopes are historical receipts. Their notices describe the stage when each was authored. The reading object is the current assembled reading path; no historical text was overwritten.',
        'components': public_components, 'reading': current_reading(public_components),
    }
    internal = {
        'schemaVersion': 'EX58-complete-director-candidate-v1', 'id': public['id'], 'status': STATUS,
        'completeComponents': internal_components,
        'currentCorrectedContracts': read(R / 'data/director/expedition_candidate/source_contracts_corrected.json'),
        'currentCorrectedRegister': read(R / 'data/director/expedition_candidate/source_register_corrected.json'),
        'currentCorrectedConflicts': read(R / 'data/director/expedition_candidate/source_conflicts_corrected.json'),
        'exactAcceptanceContract': read(A / 'ex58-final-gpt-verdict/EX58_EXACT_CANDIDATE_CONTRACT.json'),
        'componentBindings': inputs, 'publicProjectionPolicy': 'Reconstruct the complete public file from each explicitly allowed public component envelope. Validate the whole JSON and both complete rendered books separately. Never serialize completeComponents into a player artifact.',
        'newPromotions': 0, 'sourceInformationDeleted': 0, 'runtimeImplemented': False,
        'humanPlaytestConfirmed': False, 'wholeGameFlowConfirmed': False,
        'pushPerformed': False, 'cosmologyReviewed': False,
    }
    save(outputs['public'], public)
    save(outputs['director'], internal)
    outputs['playerBook'].write_text(render_player(public), encoding='utf-8', newline='\n')
    outputs['directorBook'].write_text(render_director(internal), encoding='utf-8', newline='\n')
    assert all(info(G / path) == expected for path, expected in inputs.items())
    receipt = {
        'generatedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': STATUS,
        'id': public['id'], 'independentValidation': 'Required next: validate_ex58_exact_candidate.py',
        'inputs': inputs, 'outputs': {p.relative_to(G).as_posix(): info(p) for k, p in outputs.items() if k != 'assemblyReceipt'},
        'builder': binding(Path(__file__).resolve()),
        'scope': 'Lossless assembly of existing authored candidate components and current player/Director reading paths. No new game rules, approvals, source deletion, push or cosmology review.',
    }
    save(outputs['assemblyReceipt'], receipt)
    print(pretty({k: receipt[k] for k in ['status', 'outputs']}))


if __name__ == '__main__':
    main()
