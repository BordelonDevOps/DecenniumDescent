"""Preserve exact source evidence for the still-missing temporal control adapter."""
from pathlib import Path
import hashlib
import json

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[3]/'DescentReviewChanges/ReviewBible'

def main():
    output = AUDIT/'TEMPORAL_CONTROL_PULSE_POLICY_SOURCES_V3.json'
    assert not output.exists(), 'Preserve this preparation; use a revision filename'
    control = json.loads((ROOT/'data/playtest/control_state_bindings.json').read_text(encoding='utf-8'))
    pulse = json.loads((ROOT/'data/playtest/healing_pulse_bindings.json').read_text(encoding='utf-8'))
    profiles = json.loads((ROOT/'data/playtest/healing_pulse_profiles.json').read_text(encoding='utf-8'))
    selected = []
    for row in control['bindings']:
        procedure = row.get('sourceProcedure', {})
        text = json.dumps(procedure).lower()
        components = ' '.join(row.get('componentIds', [])).lower()
        if any(x in text for x in ('guiding star', 'guiding bolt', 'wrathful brand', 'divine judgment')) or 'speed' in components or 'slow' in components:
            selected.append(row)
    maps = {k:profiles[k] for k in ('profiles', 'nativeRecurrences', 'contactVariants')}
    profile_sources = {s for table in maps.values() for ids in table.values() for s in ids}
    # Engine rows preserve a numeric sourceId; bindingId is their qualified ID.
    pulse_rows = [row for row in pulse['bindings'] if row['bindingId'] in profile_sources]
    covered = {row['bindingId'] for row in pulse_rows}
    supplemental = []
    for source in sorted(profile_sources-covered):
        owner = source.split('.')[0]
        path = ROOT/'data/public/class_playtests'/f'{owner}.json'
        catalog = json.loads(path.read_text(encoding='utf-8'))
        if '.engine[' in source:
            index = int(source.split('[')[1].rstrip(']'))
            exact = {'engineIndex':index, 'text':catalog['engine'][index]}
        else:
            exact = next(c for c in catalog['cards'] if c['id'] == source)
        supplemental.append({'sourceId':source, 'sourcePath':str(path.relative_to(ROOT)),
                             'fileSha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                             'exactSource':exact})
    sources = [
        'data/playtest/control_state_bindings.json',
        'data/playtest/healing_pulse_bindings.json',
        'data/playtest/healing_pulse_profiles.json',
        'docs/mechanics/CONTROL_STATES_PLAYTEST.md',
        'docs/mechanics/HEALING_PULSE_PLAYTEST.md',
        'tools/control_playtest_rules.py', 'tools/healing_pulse_playtest_rules.py',
    ]
    report = {
        'status': 'PREPARED exact evidence; no new temporal source policy adopted',
        'purpose': 'Map the nine state-holder families requested by the twelve-boundary conference before admitting their temporal instances.',
        'sourceHashes': {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
        'controlBindings': selected,
        'pulseProfileMaps': maps,
        'pulseBindings': pulse_rows,
        'supplementalExactSources': supplemental,
        'profileSourcesNotInPulseBindingFile': sorted(profile_sources-covered),
        'unresolvedProfileSources': sorted(profile_sources-covered-{r['sourceId'] for r in supplemental}),
        'revisionNote': 'V1 and V2 are preserved. V3 includes all24 pulse,6 native recurrence and3 contact aliases, and the actual Guiding Bolt source behind the helper name GuidingStarMark. Engine rows match by qualified bindingId; absent rows are captured directly.',
        'questionsBeforeAdmission': [
            'Retain each exact source clock type: absolute world deadline versus source/target regular marker versus current actual turn end. ClockMarker numeric values alone do not classify it.',
            'A restored PulseSeries must not replay the initial cast pulse or already-consumed snapshot opportunity. Any later newly due paid pulse must fund from current conserved RP/RC under the source rule.',
            'Determine canonical pulse/derived-resource event identity across iterations; preserve historical independent Ki/resource occurrences so a timeline restore does not duplicate an old reward/resource event.',
            'GuidingStarMark pending attack tokens cannot be captured or restored mid-roll. Preserve canonical effect identity and advance token history without replaying an old attack.',
            'Generic OneShotRider requires a source-qualified parent record and endpoint; trigger_kind alone is not a temporal policy.',
            'BloomReserve is an effect-owned recorded missing-HP allocation, distinct from the conserved Lifeleech Recovery Reserve. Temporal consumption needs exact instance/index identity.',
            'FirstContactLedger records source-instance/recipient eligibility; distinguish effect one-shot restoration from real-rest family history.',
            'NativeOccurrenceLedger needs iteration-qualified actual regular events plus original source costs; no tick at the rewind instant.',
        ],
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'controlSources':len(selected), 'pulseSourceRows':len(pulse_rows),
                     'profileAliases':sum(len(v) for v in maps.values()), 'supplementalSources':len(supplemental),
                     'unresolvedSourceIds':report['unresolvedProfileSources'],
                     'bytes':output.stat().st_size}))

if __name__ == '__main__':
    main()
