"""Build a lossless Known Descent review registry; never install runtime data."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

from audit_bestiary_source_runtime import core, section

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def named_entries(block, heading):
    if heading not in block:
        return []
    part = block.split(heading, 1)[1].split('\n### ', 1)[0]
    return [{'name': m[1], 'sourceText': m[2].strip()} for m in re.finditer(
        r'^\*\*([^*]+)\.\*\*\s*(.*?)(?=^\*\*[^*]+\.\*\*|\Z)', part, re.M | re.S)]


def printed_defense(stat, heading):
    match = re.search(r'^\*\*' + re.escape(heading) + r'\*\* (.+)$', stat, re.M)
    assert match is not None, heading
    text = match[1].strip()
    return {'sourceText': text, 'labels': [] if text == 'None' else [s.strip() for s in text.split(',')]}


def harvest(text):
    block = section(text, 'Treasure and Harvest')
    if block is None:
        return None
    meta = re.search(r'\*\*Harvest skill:\*\* (.+?) · \*\*Harvest DC:\*\* (\d+) · \*\*Base time:\*\* (.+?)\s*$', block, re.M)
    components = []
    for index, line in enumerate(block.splitlines()):
        if not line.startswith('|') or '---' in line or line.startswith('| Component |'):
            continue
        cells = [x.strip() for x in line.strip('|').split('|')]
        assert len(cells) == 3, cells
        detail = re.fullmatch(r'(\d+)%, (\d+) gp base', cells[2])
        assert detail or cells[2] == 'Director-set', cells
        components.append({'sourceOrder': len(components), 'sectionLine': index + 1, 'sourceCells': cells,
                           'name': cells[0], 'printedTier': int(cells[1]), 'printedDropValue': cells[2],
                           'printedRatePercent': int(detail[1]) if detail else None,
                           'printedValueGp': int(detail[2]) if detail else None,
                           'printedValueQualifier': 'base' if detail else None,
                           'requiresDirectorValues': detail is None})
    return {'sourceText': block, 'skillLabel': meta[1] if meta else None,
            'printedDC': int(meta[2]) if meta else None, 'printedBaseTime': meta[3].strip() if meta else None,
            'procedureFieldsPrinted': bool(meta), 'components': components,
            'interpretationStatus': 'Source labels and printed numbers only; no quantity, roll, availability, extraction or market procedure inferred.'}


def main():
    status_path = AUDIT / 'BESTIARY_SOURCE_CANDIDATE_VALIDATION.json'
    if status_path.exists():
        previous = read(status_path)
        assert previous['reviewStatus'] == 'PREPARED_NOT_SENT', 'Preserve reviewed artifacts; prepare a separate revision.'
        assert all(sha(GAME / p) == h for p, h in previous['artifactHashes'].items()), 'Generated artifact changed; preserve it before rebuilding.'
    evidence_path = AUDIT / 'BESTIARY_SOURCE_RUNTIME_AUDIT.json'
    history_path = AUDIT / 'BESTIARY_HISTORY_PROVENANCE.json'
    evidence, history = read(evidence_path), read(history_path)
    baseline = evidence['sourceHashes'] | history['sourceHashes']
    baseline |= {evidence_path.relative_to(GAME).as_posix(): sha(evidence_path),
                 history_path.relative_to(GAME).as_posix(): sha(history_path)}
    assert all(sha(GAME / p) == h for p, h in baseline.items()), 'Reaudit changed sources before building.'
    old = read(GAME / history['retainedV6Projection']['path'])
    older_by_id = {r['id']: r for r in old}
    missing_actions = {r['name']: r['referencedButNotListedActions'] for r in evidence['sourceReferencesWithoutListedActions']}
    records = []
    for source in evidence['knownDossiers']:
        path = GAME / source['sourcePath']
        raw = path.read_bytes().decode('utf-8')
        text = raw.lstrip('\ufeff').replace('\r\n', '\n')
        stat = section(text, 'Stat Block')
        body = None
        issues = []
        if stat is not None:
            fields = core(stat)
            assert fields == source['sourceFields'], source['name']
            values = re.findall(r'\|\s*(-?\d+)\s*\(([+-]?\d+)\)\s*', stat)
            assert len(values) == 6, source['name']
            abilities = {key: {'score': int(score), 'printedModifier': int(mod)}
                         for key, (score, mod) in zip(('strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'), values)}
            defenses = {key: printed_defense(stat, heading) for key, heading in (
                ('resistanceLabels', 'Resistances'), ('immunityLabels', 'Immunities'),
                ('conditionImmunityLabels', 'Condition Immunities'))}
            vulnerability = re.search(r'^\*\*Tactical Vulnerability\*\* (.+)$', stat, re.M)
            body = {'printedCoreFields': fields, 'abilities': abilities, 'printedDefenses': defenses,
                    'tacticalVulnerabilityText': vulnerability[1].strip() if vulnerability else None,
                    'traits': named_entries(stat, '### Traits'), 'actions': named_entries(stat, '### Actions')}
            if 'disease' in defenses['immunityLabels']['labels']:
                issues.append({'kind': 'immunity-category-needs-mapping', 'sourceLabel': 'disease',
                               'note': 'Preserved under the source Immunities label; not converted into a damage type or an unprinted condition.'})
        route = source['buildFilterEntry']
        if route is None:
            issues.append({'kind': 'missing-existing-build-filter-route', 'note': 'Source classification retained; no public route inferred.'})
        if source['name'] in missing_actions:
            issues.append({'kind': 'tactics-refers-to-unlisted-action', 'names': missing_actions[source['name']]})
        drops = harvest(text)
        if drops and not drops['procedureFieldsPrinted']:
            issues.append({'kind': 'harvest-procedure-not-printed', 'note': 'No skill, DC or base time supplied by the source; fields remain null.'})
        aliases = older_by_id.get(source['slug'], {}).get('compatibilityAliases', [])
        if aliases:
            issues.append({'kind': 'retained-alias-also-has-separate-source-dossier', 'aliases': aliases,
                           'note': 'Existing V6 alias evidence retained; companion identity migration remains pending.'})
        records.append({'id': source['slug'], 'name': source['name'],
                        'recordKind': 'creature-source' if stat is not None else 'historical-record',
                        'reviewStatus': 'SOURCE_BOUND_NOT_OPERATIONALLY_REVIEWED',
                        'source': {'path': source['sourcePath'], 'sha256': sha(path), 'originalUtf8Text': raw},
                        'publication': {'sourceClassification': source['publicationClassification'],
                                        'existingBuildFilterEntry': route, 'buildBucket': route['buildBucket'] if route else None},
                        'bookBinding': source['bookBinding'], 'existingV6CompatibilityAliases': aliases,
                        'statBlock': body, 'harvest': drops, 'unresolvedSourceInterfaces': issues})

    identity_relations = [{'sourceId': r['id'], 'sourceName': r['name'], 'alias': alias,
                          'exactSourceIdsWithThatName': [other['id'] for other in records if other['name'] == alias],
                          'evidencePath': history['retainedV6Projection']['path'],
                          'disposition': 'preserve both dossiers; do not silently rewrite saved names or choose one record'}
                         for r in records for alias in r['existingV6CompatibilityAliases']]
    common = {'schemaVersion': 1, 'status': 'SOURCE CANDIDATE ONLY — no runtime installation or GPT approval',
              'purpose': 'Preserve and structure source evidence for exact review. Source action text is not an executable combat profile.',
              'cosmologyReview': 'deferred until after verified GitHub delivery', 'runtimeInstalled': False}
    internal = common | {'records': records, 'identityRelations': identity_relations,
                         'preservedSealedRoutesOnly': evidence['sealedRoutingOnly']}
    public_rows = [r for r in records if r['publication']['buildBucket'] == 'public']
    public = common | {'records': public_rows}
    internal_path = ROOT / 'data/director/bestiary_source_candidate_internal.json'
    public_path = ROOT / 'data/playtest/bestiary_public_source_candidate.json'
    guide_path = ROOT / 'docs/mechanics/BESTIARY_SOURCE_CANDIDATE.md'
    write(internal_path, internal)
    write(public_path, public)
    creature_rows = [r for r in records if r['statBlock']]
    components = [c for r in records if r['harvest'] for c in r['harvest']['components']]
    issue_counts = dict(Counter(i['kind'] for r in records for i in r['unresolvedSourceInterfaces']))
    guide = [
        '# Bestiary source candidate', '',
        '**Prepared for review; not installed in the companion and not operationally approved.**', '',
        'This candidate preserves all 67 Known Descent source dossiers, including 66 stat blocks and one historical record. It retains the exact UTF-8 source text and file hash for every dossier. The player projection includes only the 26 dossiers explicitly marked public by the existing build-filter index. The internal registry also retains 39 restricted dossiers, two dossiers lacking filter routes, and metadata for the five sealed routes; sealed contents are not transformed or reviewed.', '',
        'Each stat-bearing record includes the printed body/CR/XP/AC/HP/speed/Save DC fields, all six ability scores and printed modifiers, resistance/immunity labels, tactical-vulnerability text, traits and actions. These are source fields, not executable combat rules. Tactical vulnerability is not automatically a damage vulnerability; the four disease immunity labels remain literal source labels awaiting an effect-category binding.', '',
        'All 178 harvest-component occurrences remain in source order. Of these, 148 print a percentage and gp base value; 30 say Director-set and retain null numeric values. Crystal Shardling and Pact Automaton Sentinel provide no harvest skill/DC/base time, so those fields remain null. No output quantity, percentage roll procedure, availability, extraction weight or market price rule is inferred.', '',
        'The historical disaster record has statBlock: null and retains its existing restricted route. It cannot become a creature through default Medium/Unknown/CR0 values. Both Fracture-Kin compatibility aliases are retained with their existing V6 provenance; the classic-label source dossiers remain separate, preserving the identity question for migration review.', '',
        'Three source tactics references remain unresolved: Cave Bear/Bite, Dimetrodon/Tail Sweep and Giant Constrictor Snake/Constrict. No action was fabricated. The candidate also records two missing publication routes, two alias/source overlaps, four immunity-label mappings and two missing harvest procedures. Complete action timing, targeting, costs, encounter integration and balance remain open.', '',
        'The live 707-record dataset, its workbooks, current consumers and all original source dossiers are unchanged. Candidate generation does not call the existing ingestion or combat-generation scripts. Do not swap this file into the companion until GPT review, saved-identity migration, loot conversion and public/licensed/Director routing are resolved and validated.', '',
        '- Public candidate: `data/playtest/bestiary_public_source_candidate.json`.',
        '- Internal source registry: `data/director/bestiary_source_candidate_internal.json`.',
        '- Source and field validation: `docs/audit/2026-10-08/full-game/BESTIARY_SOURCE_CANDIDATE_VALIDATION.json`.',
        '- Rebuild with `tools/build_bestiary_source_candidate.py`; rebuilding refuses to overwrite altered candidate artifacts or a reviewed revision.', '',
        'No source deletion or GitHub push has occurred. Cosmology remains deferred until after verified delivery.', '',
    ]
    guide_path.write_text('\n'.join(guide), encoding='utf-8')
    # Verify emitted artifacts against independent stored source evidence and
    # exact original bytes, including intentionally missing source values.
    emitted, emitted_public = read(internal_path), read(public_path)
    source_by_slug = {r['slug']: r for r in evidence['knownDossiers']}
    clean_action = lambda text: ' '.join(text.replace('*', '').split())
    defense_pairs = {'resistanceLabels': 'resistances', 'immunityLabels': 'immunities',
                     'conditionImmunityLabels': 'conditionImmunities'}
    controls = {
        'all67OriginalDossiersReconstructExactUtf8Bytes': len(records) == 67 and all(
            r['source']['originalUtf8Text'].encode('utf-8') == (GAME / r['source']['path']).read_bytes() for r in emitted['records']),
        'allSourceIdsUniqueAndExistingV6IdsPreserved': len({r['id'] for r in records}) == 67 and set(older_by_id) <= {r['id'] for r in records},
        'all66PrintedCoreStatSetsMatchPriorSourceAudit': len(creature_rows) == 66 and all(
            r['statBlock']['printedCoreFields'] == next(s['sourceFields'] for s in evidence['knownDossiers'] if s['slug'] == r['id']) for r in creature_rows),
        'all396PrintedAbilityModifiersArithmeticallyConsistent': sum(len(r['statBlock']['abilities']) for r in creature_rows) == 396 and all(
            (v['score'] - 10) // 2 == v['printedModifier'] for r in creature_rows for v in r['statBlock']['abilities'].values()),
        'all162SourceActionsMatchPriorIndependentExtraction': sum(len(r['statBlock']['actions']) for r in creature_rows) == 162 and all(
            [(x['name'], clean_action(x['sourceText'])) for x in r['statBlock']['actions']] ==
            [(x['name'], clean_action(x['text'])) for x in source_by_slug[r['id']]['sourceActions']] for r in creature_rows),
        'allPreviouslyAuditedDefenseFieldsPreserved': all(
            r['statBlock']['printedDefenses'][new]['sourceText'] == source_by_slug[r['id']]['sourceDefenses'][old_key]
            for r in creature_rows if 'sourceDefenses' in source_by_slug[r['id']] for new, old_key in defense_pairs.items()),
        'publicProjectionContainsExactly26ExistingPublicRoutes': len(public_rows) == 26 and emitted_public['records'] == [r for r in emitted['records'] if r['publication']['buildBucket'] == 'public'],
        'all39ExistingRestrictedRoutesAndTwoMissingRoutesRetained': Counter(r['publication']['buildBucket'] for r in records) == {'public': 26, 'restricted': 39, None: 2},
        'historicalRecordHasNoInventedStatsAndKeepsRestrictedRoute': len(records) - len(creature_rows) == 1 and all(r['recordKind'] == 'historical-record' and r['publication']['buildBucket'] == 'restricted' for r in records if r['statBlock'] is None),
        'all178HarvestRowsRetainedIncluding30DirectorSetRows': len(components) == 178 and sum(c['requiresDirectorValues'] for c in components) == 30 and all(
            c['printedRatePercent'] is None and c['printedValueGp'] is None for c in components if c['requiresDirectorValues']),
        'bothAbsentHarvestProceduresRemainNull': {r['name'] for r in records if r['harvest'] and not r['harvest']['procedureFieldsPrinted']} == {'Crystal Shardling', 'Pact Automaton Sentinel'},
        'bothExistingAliasesRetainedWithBothOriginalDossiers': len(identity_relations) == 2 and all(len(r['exactSourceIdsWithThatName']) == 1 for r in identity_relations),
        'allThreeUnlistedSourceActionReferencesRemainFlagged': sum(i['kind'] == 'tactics-refers-to-unlisted-action' for r in records for i in r['unresolvedSourceInterfaces']) == 3,
        'allProtectedSourcesBuildInputsAndRuntimeConsumersUnchanged': all(sha(GAME / p) == h for p, h in baseline.items()),
    }
    manifest = {'status': 'PASS_SOURCE_PRESERVATION; OPERATIONAL_REVIEW_PENDING', 'reviewStatus': 'PREPARED_NOT_SENT',
                'sent': False, 'reviewVerdict': None, 'controls': controls, 'sourceHashes': baseline,
                'counts': {'knownDossiers': len(records), 'statBlocks': len(creature_rows), 'publicDossiers': len(public_rows),
                           'harvestComponentOccurrences': len(components), 'unresolvedInterfacesByKind': issue_counts},
                'artifactHashes': {p.relative_to(GAME).as_posix(): sha(p) for p in (internal_path, public_path, guide_path)},
                'noRuntimeInstallation': True, 'noSourceEdits': True, 'cosmologyReviewDeferred': True}
    write(status_path, manifest)
    print(json.dumps({'controls': controls, 'counts': manifest['counts'], 'protectedInputs': len(baseline)}))
    assert all(controls.values()), controls


if __name__ == '__main__':
    main()
