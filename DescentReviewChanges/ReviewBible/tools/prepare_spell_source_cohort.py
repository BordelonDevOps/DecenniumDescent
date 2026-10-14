"""Shared preservation writer for new, explicitly specified source cohorts.

The writer only collects existing evidence and authored questions. It does not
change operational catalogs, infer an approval, or send a notebook message.
"""
from copy import deepcopy
import json
from prepare_low_illusion_spell_source_audit import ROOT, GAME, AUDIT, current_book_rows, digest
from prepare_low_necromancy_spell_source_audit import sha, dump
from prepare_combat_feat_source_audit import section


def prepare(*, prefix, title, questions, selector, expected_count, question_prefix,
            prior_files, expected_prior_count, counterpart_ids, pending_ids,
            extra_excerpts, introduction, deferred_ids=(), expected_conflict_ids=(),
            expected_alias_ids=(), expected_class_mentions=None,
            unresolved_name_references=(), future_dispatch=None):
    for suffix in ('SOURCE_PREPARATION.json', 'SOURCE_AUDIT.md', 'SOURCE_STATUS.json'):
        assert not (AUDIT / f'{prefix}_{suffix}').exists(), 'Preserve existing source preparation; use a new revision.'
    assert not (AUDIT / f'CODEX_{prefix}_SOURCE_PREPARED.txt').exists()
    inherited = json.loads((AUDIT / 'LOW_ILLUSION_SPELL_SOURCE_PREPARATION.json').read_text(encoding='utf-8'))
    protected = deepcopy(inherited['protectedFiles'])
    assert all(sha(GAME / p) == h for p, h in protected.items())

    def read(path):
        protected[path.relative_to(GAME).as_posix()] = sha(path)
        return json.loads(path.read_text(encoding='utf-8-sig'))

    catalog = read(ROOT / 'data/public/spell_playtests/catalog.json'); rows = catalog['spells']; by = {r['id']: r for r in rows}
    selected = [r for r in rows if selector(r)]
    assert len(selected) == expected_count and {r['id'] for r in selected} == set(questions)
    assert set(deferred_ids).issubset(questions)
    original = read(ROOT / 'data/playtest/spell_sources/catalog.json')
    core = read(ROOT / 'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    book = current_book_rows(); bindings = []; differences = []; aliases = []; core_count = 0
    for row in selected:
        assert row['source']['original'] == original[row['id']]
        for entry in row['source']['coreEntries'] + row['source']['possibleHistoricalAliases']:
            assert entry['original'] == core['spells'][entry['index']]
        core_count += len(row['source']['coreEntries'])
        if row['source']['possibleHistoricalAliases']:
            aliases.append({'spellId': row['id'], 'possibleHistoricalAliases': row['source']['possibleHistoricalAliases'],
                            'scope': 'Preserved comparison only; not an automatic identity merge or new operational permission.'})
        for placement in row['source']['original']['placements']:
            matches = [b for b in book if b['name'] == row['name'] and b['school'] == placement['school'] and b['level'] == placement['level']]
            assert len(matches) == 1, (row['id'], placement)
            bindings.append({'spellId': row['id'], 'catalogPlacement': placement, 'currentBookRow': matches[0],
                             'summaryDifferencePreserved': placement['summary'] != matches[0]['summary']})
            for entry in row['source']['coreEntries']:
                e = entry['original']
                if e['school'] == placement['school'] and e['level'] == placement['level'] and e['effect'] != placement['summary']:
                    differences.append({'spellId': row['id'], 'catalogPlacement': placement, 'coreEntry': entry})
    unresolved = []
    for reference in unresolved_name_references:
        name = reference['name'].casefold()
        matches = {'catalogIds': [r['id'] for r in rows if r['name'].casefold() == name],
                   'coreIndices': [i for i, r in enumerate(core['spells']) if r['name'].casefold() == name],
                   'bookRows': [r for r in book if r['name'].casefold() == name]}
        assert reference['referencedBy'] in questions
        assert all(not v for v in matches.values()), (reference, matches)
        unresolved.append({**reference, 'exactCaseInsensitiveNameMatches': matches,
                           'searchedCatalogIdentities': len(rows), 'searchedCoreEntries': len(core['spells']),
                           'searchedBookRows': len(book),
                           'scope': 'Absent exact-name reference in these current spell registries. No external spell imported and no similarly named identity merged.'})
    assert all(by[x]['operational'] is not None for x in counterpart_ids)
    assert all(by[x]['operational'] is None for x in pending_ids)
    assert not set(questions).intersection(counterpart_ids + pending_ids)
    assert len(set(counterpart_ids + pending_ids)) == len(counterpart_ids + pending_ids)
    counterparts = [by[x] for x in counterpart_ids + pending_ids]
    mentions = [m for m in read(ROOT / 'data/public/spell_playtests/class_name_mentions_for_review.json') if m.get('spellId') in questions and m['spellId'] not in deferred_ids]
    manifest = read(ROOT / 'data/public/class_playtests/manifest.json'); classes = {r['class']: r for r in manifest['classes']}; class_records = []
    for m in mentions:
        path = (ROOT / 'docs/mechanics' / classes[m['class']]['data']).resolve(); data = read(path)
        if m['location'] == 'engine': record = {'engine': data.get('engine', [])}
        else:
            found = [c for c in data['cards'] if c['id'] == m['location']]; assert len(found) == 1; record = {'card': found[0]}
        class_records.append({'mention': m, **record, 'file': path.relative_to(GAME).as_posix(),
                              'scope': 'Textual comparison only, not an automatic spell grant or identity merge. Historical cosmological flavor remains unchanged and unreviewed.'})
    excerpts = deepcopy(inherited['currentGoverningExcerpts'])
    for name, headings in extra_excerpts.items():
        path = ROOT / 'docs/mechanics' / name; text = path.read_text(encoding='utf-8')
        protected[path.relative_to(GAME).as_posix()] = sha(path)
        for heading in headings or [None]:
            excerpts.append({'file': path.relative_to(GAME).as_posix(), 'sha256': sha(path),
                             'heading': heading or 'entire guide', 'exactText': section(text, heading) if heading else text})
    prior_records = []; prior_bindings = []
    for filename in prior_files:
        prior = read(AUDIT / filename); prior_records += prior['selectedSpells']; prior_bindings += prior['currentBookBindings']
    prior_ids = [r['spellId'] for r in prior_records]
    records = [{'spellId': r['id'], 'questionId': f'{question_prefix}-{i+1:02}',
                'scope': 'post-push receipt only' if r['id'] in deferred_ids else 'pre-push mechanical source question',
                'fullSourceAndCurrentAccessRecord': r, 'recordSha256': digest(r),
                'individualQuestion': questions[r['id']]} for i, r in enumerate(selected)]
    combined = prior_records + records; combined_deferred = [r['spellId'] for r in combined if r.get('scope') == 'post-push receipt only']
    checks = [
        ('Exact selected identity set and full individual source questions', len(records) == expected_count and all(len(r['individualQuestion']) > 240 for r in records)),
        ('Complete catalog, Core and historical-alias objects match their source registries', all(r['source']['original'] == original[r['id']] for r in selected)),
        ('Every catalog placement has one exact current-book binding', len(bindings) == sum(len(r['source']['original']['placements']) for r in selected)),
        ('Expected catalog/Core literal conflicts retained', {r['spellId'] for r in differences} == set(expected_conflict_ids)),
        ('Expected historical aliases preserved without merging', {r['spellId'] for r in aliases} == set(expected_alias_ids)),
        ('Reviewed and pending complete comparisons retain their distinct current status', len(counterparts) == len(counterpart_ids) + len(pending_ids)),
        ('Every nondeferred registered class mention retains its complete record', len(class_records) == len(mentions) and (expected_class_mentions is None or len(class_records) == expected_class_mentions)),
        ('No duplicate with prior prepared identities', len(prior_ids) == len(set(prior_ids)) == expected_prior_count and not set(prior_ids).intersection(questions)),
        ('Ordinary catalog remains276 operational and572 pending', len(rows) == 848 and sum(r['operational'] is None for r in rows) == 572),
        ('All exact governing excerpts are current', all(e['exactText'] in (GAME / e['file']).read_text(encoding='utf-8') for e in excerpts)),
        ('Every protected input remains unchanged', all(sha(GAME / p) == h for p, h in protected.items())),
    ]
    if unresolved:
        checks.append(('Named missing references checked against catalog, Core and current book',
                       all(all(not v for v in r['exactCaseInsensitiveNameMatches'].values()) for r in unresolved)))
    assert all(ok for _, ok in checks), [n for n, ok in checks if not ok]
    counts = {'selectedSources': len(records), 'prePushMechanicalQuestions': len(records)-len(deferred_ids),
              'postPushReceiptOnly': len(deferred_ids), 'sourceSpells': 848, 'operationalSpells': 276, 'remaining': 572,
              'exactCoreEntries': core_count, 'historicalAliasEntries': sum(len(a['possibleHistoricalAliases']) for a in aliases),
              'currentBookBindings': len(bindings), 'catalogCoreEffectDifferences': len(differences),
              'reviewedCounterparts': len(counterpart_ids), 'pendingCounterparts': len(pending_ids),
              'classComparisonRecords': len(class_records), 'governingExcerpts': len(excerpts),
              'focusedPendingSourceIdentitiesIncludingThisCohort': len(combined),
              'currentBookBindingsIncludingThisCohort': len(prior_bindings)+len(bindings),
              'prePushPreparedSpellQuestionsIncludingThisCohort': len(combined)-len(combined_deferred),
              'postPushReceiptsIncludingThisCohort': len(combined_deferred),
              'unresolvedNamedReferences': len(unresolved)}
    data = {'status': 'prepared-not-sent; source questions only; no approvals',
            'commonOperationalQuestion': inherited['commonOperationalQuestion'],
            'commonQuestionException': 'Post-push receipts are preserved only, excluded from current mechanical authoring. Existing faction/alignment/location records do not authorize new cosmology, theology or lore.',
            'selectedSpells': records, 'currentBookBindings': bindings, 'completeCounterparts': counterparts,
            'classComparisonRecords': class_records, 'catalogCoreEffectDifferences': differences,
            'preservedHistoricalAliases': aliases, 'unresolvedNamedReferences': unresolved,
            'currentGoverningExcerpts': excerpts,
            'currentRankCosts': catalog['costByRank'], 'currentClassProgression': catalog['classProgression'],
            'counts': counts, 'checks': [{'name': n, 'pass': ok} for n, ok in checks], 'protectedFiles': protected,
            'spellsApproved': 0, 'sourceInformationDeleted': 0, 'cosmology': 'post-push only',
            'futureDispatch': future_dispatch or 'Rebase relevant dependencies before dispatch and preserve these revisions. Source decisions precede authored cards and separate exact review.'}
    dump(AUDIT / f'{prefix}_SOURCE_PREPARATION.json', data)
    lines = ['# ' + title, '', data['status'], '', introduction, '',
             '| Case | Spell | Scope and source question |', '|---|---|---|']
    lines += [f"| {r['questionId']} | {r['fullSourceAndCurrentAccessRecord']['name']} | {r['scope']}: {r['individualQuestion']} |" for r in records]
    lines += ['', f"Across {len(prior_files)+1} prepared cohorts: {len(combined)} distinct pending identities, {len(prior_bindings)+len(bindings)} book bindings, {len(combined)-len(combined_deferred)} mechanical questions, and {len(combined_deferred)} post-push receipts. Ordinary totals stay276 operational/572 pending. No source information deleted or approval granted.", '']
    report = '\n'.join(lines); (AUDIT / f'{prefix}_SOURCE_AUDIT.md').write_text(report, encoding='utf-8', newline='\n')
    packet = 'PREPARED SOURCE CONFERENCE — NOT SENT: ' + title + '\n\n' + report + '\nCOMPLETE SOURCE AND CURRENT DEPENDENCY EVIDENCE\n' + json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    path = AUDIT / f'CODEX_{prefix}_SOURCE_PREPARED.txt'; path.write_text(packet, encoding='utf-8', newline='\n')
    status = {'status': data['status'], 'packetFile': path.name, 'characters': len(packet), 'packetSha256': sha(path),
              'counts': counts, 'checkCount': len(checks), 'protectedFilesUnchanged': len(protected),
              'spellsApproved': 0, 'sourceInformationDeleted': 0, 'cosmology': 'post-push only'}
    dump(AUDIT / f'{prefix}_SOURCE_STATUS.json', status); print(json.dumps(status))
