"""Read-only source/runtime audit; does not publish or replace any bestiary."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
PACK = Path('docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack')
KNOWN = 'Monster_Manual_of_the_Known_Descent_Source'
SEALED = 'Directors_Sealed_Bestiary_Source'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section(text, heading):
    marker = '## ' + heading + '\n'
    if marker not in text:
        return None
    return text.split(marker, 1)[1].split('\n## ', 1)[0].strip()


def clean(text):
    return ' '.join(text.replace('*', '').split())


def core(text):
    plain = text.replace('**', '')
    body = re.search(r'(Tiny|Small|Medium|Large|Huge|Gargantuan) (.+?), ([^\n]+?)(?:\s+Challenge|$)', plain, re.M)
    cr = re.search(r'Challenge\s+([0-9/]+)\s+\((\d+) XP budget\)', plain)
    stats = re.search(r'Armor\s+(\d+)\s+·\s+Hit Points\s+(\d+)\s+·\s+Speed\s+([^\n]+)', plain)
    dc = re.search(r'Save DC\s+(\d+)', plain)
    if not all((body, cr, stats, dc)):
        return None
    return dict(size=body[1], type=body[2], alignment=body[3].strip(), challengeRating=cr[1],
                xp=int(cr[2]), armorClass=int(stats[1]), hitPoints=int(stats[2]),
                speed=stats[3].strip(), saveDc=int(dc[1]))


def source_defenses(stat):
    return {key: re.search(r'^\*\*' + label + r'\*\* (.+)$', stat, re.M)[1].strip()
            for key, label in [('resistances', 'Resistances'), ('immunities', 'Immunities'),
                               ('conditionImmunities', 'Condition Immunities')]}


def source_actions(stat):
    if '### Actions' not in stat:
        return []
    block = stat.split('### Actions', 1)[1].split('\n### ', 1)[0]
    return [{'name': m[1], 'text': m[2].strip()} for m in re.finditer(r'^\*\*(.+?)\.\*\*\s*([^\n]+)', block, re.M)]


def paragraphs(path):
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    with zipfile.ZipFile(path) as z:
        doc = ET.fromstring(z.read('word/document.xml'))
    rows = []
    for i, p in enumerate(doc.iter(w + 'p')):
        style = p.find(w + 'pPr/' + w + 'pStyle')
        rows.append({'index': i, 'style': style.get(w + 'val') if style is not None else None,
                     'text': ''.join(t.text or '' for t in p.iter(w + 't'))})
    return rows


def book_binding(ps, name):
    starts = [p['index'] for p in ps if p['style'] == 'Heading1' and p['text'] == name]
    if not starts:
        return None
    assert len(starts) == 1, name
    start = starts[0]
    end = next((i for i in range(start + 1, len(ps)) if ps[i]['style'] == 'Heading1'), len(ps))
    stats = [p['index'] for p in ps[start:end] if p['style'] == 'Heading2' and p['text'] == 'Stat Block']
    if not stats:
        return {'headingParagraphIndex': start, 'nextHeadingParagraphIndex': end, 'statBlock': None}
    assert len(stats) == 1
    at = stats[0]
    stop = next((i for i in range(at + 1, end) if ps[i]['style'] == 'Heading2'), end)
    block = ps[at + 1:stop]
    fight_start = next((i for i in range(stop, end) if ps[i]['text'] == 'How It Fights' and ps[i]['style'] == 'Heading2'), None)
    fight = []
    if fight_start is not None:
        fight_end = next((i for i in range(fight_start + 1, end) if ps[i]['style'] == 'Heading2'), end)
        fight = ps[fight_start + 1:fight_end]
    return {'headingParagraphIndex': start, 'nextHeadingParagraphIndex': end,
            'statBlockHeadingParagraphIndex': at, 'statBlock': block, 'howItFights': fight}


def main():
    pack = GAME / PACK
    files = sorted(p for p in pack.rglob('*') if p.is_file())
    original_paths = files + [ROOT / p.relative_to(GAME) for p in files]
    book = GAME / 'books/player/Decennium_Descent_Monster_Manual_of_the_Known_Descent_v2.docx'
    runtime_path = ROOT / 'src/bestiary_data_full.json'
    original_paths += [book, runtime_path, GAME / 'src/bestiary_data_full.json', GAME / 'docs/canon/CANON_MANIFEST.json']
    baseline = {p.relative_to(GAME).as_posix(): sha(p) for p in original_paths}
    filters = read(pack / 'build-filters.json')
    filter_by_slug = {r['slug']: r for r in filters['entries']}
    runtime = read(runtime_path)
    by_name = {r['name']: r for r in runtime}
    assert len(by_name) == len(runtime)
    ps = paragraphs(book)
    rows, source_field_differences, book_differences, undefined_actions = [], [], [], []
    for p in sorted((pack / KNOWN / 'entries').glob('*.md')):
        text = p.read_text(encoding='utf-8')
        name = text.splitlines()[0][2:]
        classification = re.search(r'^\*\*Publication classification:\*\* (.+)$', text, re.M)[1].strip()
        stat = section(text, 'Stat Block')
        actions = source_actions(stat) if stat else []
        fields = core(stat) if stat else None
        assert not stat or fields is not None, name
        binding = book_binding(ps, name)
        row = {'slug': p.stem, 'name': name, 'sourcePath': p.relative_to(GAME).as_posix(),
               'sourceSha256': sha(p), 'publicationClassification': classification,
               'buildFilterEntry': filter_by_slug.get(p.stem), 'sourceStatBlock': stat,
               'sourceFields': fields, 'sourceActions': actions, 'bookBinding': binding,
               'runtimeIndex': next((i for i, r in enumerate(runtime) if r['name'] == name), None),
               'runtimeRecord': by_name.get(name), 'matchingPolicy': 'exact name only; no identity merge inferred'}
        if fields and binding and binding['statBlock']:
            book_fields = core('\n'.join(x['text'] for x in binding['statBlock']))
            assert book_fields is not None, name
            row['bookCoreFields'] = book_fields
            row['bookActionComparisons'] = []
            for key, value in fields.items():
                if book_fields[key] != value:
                    book_differences.append({'name': name, 'field': key, 'markdown': value, 'book': book_fields[key]})
            for action in actions:
                exact = action['name'] + '. ' + clean(action['text'])
                found = [x for x in binding['statBlock'] if clean(x['text']) == exact]
                row['bookActionComparisons'].append({'name': action['name'], 'sameText': bool(found),
                                                      'paragraphIndexes': [x['index'] for x in found]})
                if not found:
                    book_differences.append({'name': name, 'field': 'action:' + action['name'], 'markdown': exact,
                                            'book': 'No matching action paragraph; actual stat paragraphs retained above.'})
        if fields and name in by_name:
            actual = by_name[name]
            comparisons = []
            for key, value in fields.items():
                stored = actual.get(key)
                if key == 'saveDc':
                    stored = actual.get('saveDc', actual.get('combat', {}).get('saveDc'))
                comparisons.append({'field': key, 'source': value, 'runtime': stored, 'same': value == stored})
            defs = source_defenses(stat)
            row['sourceDefenses'] = defs
            for key, value in defs.items():
                # Only literal, case-insensitive names are compared. Qualifiers remain text.
                expected = [] if value == 'None' else [x.strip().lower() for x in value.split(',')]
                stored = actual.get('combat', {}).get('defenses', {}).get(key)
                normalized = sorted(str(x).lower() for x in stored) if isinstance(stored, list) else None
                comparisons.append({'field': key, 'sourceText': value, 'source': sorted(expected),
                                    'runtime': stored, 'same': sorted(expected) == normalized})
            row['runtimeFieldComparisons'] = comparisons
            source_field_differences.extend({'name': name, **c} for c in comparisons if not c['same'])
            source_names = [a['name'] for a in actions if a['name'] != 'Multiattack']
            runtime_names = [a.get('name') for a in actual.get('combat', {}).get('attacks', [])]
            row['attackNameComparison'] = {'sourceActionNamesExceptMultiattack': source_names,
                                          'runtimeAttackNames': runtime_names,
                                          'sameNamesInOrder': source_names == runtime_names,
                                          'scope': 'Name comparison only; not complete action semantics.'}
        fight = section(text, 'How It Fights')
        if fight and actions:
            references = re.findall(r'(?:opens with|uses) \*\*([^*]+)\*\*', fight)
            missing = [x for x in references if x not in {a['name'] for a in actions}]
            if missing:
                undefined_actions.append({'name': name, 'sourcePath': row['sourcePath'],
                                          'referencedButNotListedActions': missing,
                                          'actualSourceActions': actions, 'howItFights': fight,
                                          'bookHowItFights': binding.get('howItFights') if binding else None})
        rows.append(row)

    # Sealed files are inventoried for publication routing only; no sealed lore or
    # cosmology content is interpreted or turned into new game mechanics here.
    sealed = []
    for p in sorted((pack / SEALED / 'entries').glob('*.md')):
        name = p.read_text(encoding='utf-8').splitlines()[0][2:]
        sealed.append({'slug': p.stem, 'name': name, 'sourceSha256': sha(p),
                       'buildFilterEntry': filter_by_slug.get(p.stem),
                       'runtimeIndex': next((i for i, r in enumerate(runtime) if r['name'] == name), None)})
    imported = []
    for p in sorted((ROOT / 'src').rglob('*')):
        if p.suffix not in {'.js', '.jsx', '.mjs', '.ts', '.tsx'}:
            continue
        before_read = sha(p)
        lines = p.read_text(encoding='utf-8').splitlines()
        for index, line in enumerate(lines):
            if re.search(r'^import .*bestiary_data_full\.json', line):
                original_paths.append(p)
                baseline[p.relative_to(GAME).as_posix()] = before_read
                uses = []
                for i, s in enumerate(lines):
                    if re.search(r'(monstersData|bestiaryData|return monsters\.filter|return matchesSearch|\[.tier1.|\.forEach\(\(monster)', s):
                        uses.append({'line': i + 1, 'text': s})
                imported.append({'path': p.relative_to(GAME).as_posix(), 'sha256': sha(p),
                                 'importLine': index + 1, 'importText': line, 'selectedUsageLines': uses})
    known_names = {r['name'] for r in rows}
    sealed_names = {r['name'] for r in sealed}
    names_not_in_pack = [r['name'] for r in runtime if r['name'] not in known_names | sealed_names]
    stats_rows = [r for r in rows if r['sourceFields']]
    controls = {
        'all85PackFilesInventoried': len(files) == 85,
        'mainAndReviewPackByteIdentical': all(p.read_bytes() == (ROOT / p.relative_to(GAME)).read_bytes() for p in files),
        'mainAndReview707RuntimeByteIdentical': runtime_path.read_bytes() == (GAME / 'src/bestiary_data_full.json').read_bytes(),
        'all67KnownDossiersAndFiveSealedRoutesIndexed': len(rows) == 67 and len(sealed) == 5,
        'all66KnownStatBlocksParsed': len(stats_rows) == 66 and all(r['sourceFields'] for r in stats_rows),
        'all65BookDossierNamesBound': sum(r['bookBinding'] is not None for r in rows) == 65,
        'all64BookStatCoreFieldsAndListedActionTextsMatchMarkdown': not book_differences and sum(bool(r.get('bookCoreFields')) for r in rows) == 64,
        'all707RuntimeNamesUnique': len(by_name) == len(runtime) == 707,
        'fourDirectRuntimeConsumersLocated': len(imported) == 4,
        'originalSourcesAndRuntimeConsumersUnchanged': all(sha(GAME / p) == h for p, h in baseline.items()),
    }
    report = {'status': 'SOURCE AUDIT ONLY; no runtime replacement, rule promotion or cosmology review',
              'scope': 'Known Descent core statistics, listed action text, exact-name runtime correspondence and publication routing. Sealed dossier contents are not reviewed. No aliases or creature identities are merged.',
              'sourceHashes': baseline, 'controls': controls,
              'inventory': {'packFiles': len(files), 'knownDossiers': len(rows), 'knownStatBlocks': len(stats_rows),
                            'sealedDossiers': len(sealed), 'bookDossierBindings': sum(r['bookBinding'] is not None for r in rows),
                            'filterRows': len(filters['entries']), 'storedFilterCounts': filters['counts'],
                            'actualFilterCounts': dict(Counter(r['buildBucket'] for r in filters['entries'])),
                            'missingFilterSlugs': [r['slug'] for r in rows if r['buildFilterEntry'] is None]},
              'runtimeSummary': {'records': len(runtime), 'exactKnownNameMatches': sum(r['runtimeRecord'] is not None for r in rows),
                                 'exactSealedNameMatches': sum(r['runtimeIndex'] is not None for r in sealed),
                                 'remainingNamesWithoutExactPackMatch': names_not_in_pack,
                                 'combatSourceLabels': dict(Counter(r['combat'].get('source') for r in runtime)),
                                 'combatDraftFlags': dict(Counter(str(r['combat'].get('draft')) for r in runtime))},
              'bookDifferences': book_differences, 'runtimeFieldDifferences': source_field_differences,
              'runtimeFieldDifferenceCounts': dict(Counter(r['field'] for r in source_field_differences)),
              'sourceReferencesWithoutListedActions': undefined_actions,
              'knownDossiers': rows, 'sealedRoutingOnly': sealed, 'runtimeConsumers': imported,
              'noSourceEdits': True, 'noRuntimeEdits': True, 'noDeletion': True, 'cosmologyReviewDeferred': True}
    path = AUDIT / 'BESTIARY_SOURCE_RUNTIME_AUDIT.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    assert all(controls.values()), controls
    print(json.dumps({'controls': controls, 'inventory': report['inventory'], 'runtimeFieldDifferenceCounts': report['runtimeFieldDifferenceCounts'],
                      'bookDifferences': book_differences, 'runtimeKnownMatches': report['runtimeSummary']['exactKnownNameMatches'],
                      'runtimeSealedMatches': report['runtimeSummary']['exactSealedNameMatches'], 'otherRuntimeNames': len(names_not_in_pack),
                      'sourceUnlistedActionReferences': [{k: x[k] for k in ('name', 'referencedButNotListedActions')} for x in undefined_actions],
                      'attackNameDifferences': sum(not r['attackNameComparison']['sameNamesInOrder'] for r in rows if 'attackNameComparison' in r)}))


if __name__ == '__main__':
    main()
