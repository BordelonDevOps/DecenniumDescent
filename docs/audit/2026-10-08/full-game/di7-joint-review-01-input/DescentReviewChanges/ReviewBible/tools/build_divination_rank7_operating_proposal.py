"""One-use preservation and manuscript build for seven unadopted DI7 proposals."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
import re
from divination_rank7_proposals import SHARED, PROPOSALS, ISSUES

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text('utf-8-sig'))


def info(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    draft = A / 'DIVINATION_RANK7_OPERATING_PROPOSALS.json'
    out = R / 'data/director/spell_proposals/divination_rank7.json'
    doc = R / 'docs/spells/proposals/DIVINATION_RANK7.md'
    receipt = A / 'DIVINATION_RANK7_OPERATING_PROPOSAL_CHECK.json'
    outputs = [draft, out, doc, receipt]
    assert not any(p.exists() for p in outputs), 'Preserve existing outputs; this is a one-use build.'
    prep_path = A / 'DIVINATION_RANK7_SOURCE_PREPARATION.json'
    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    index_path = catalog_path.with_name('authored_review_index.json')
    higher_path = R / 'data/director/higher_spell_operating_proposal_index.json'
    core_path = R / 'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
    inputs = {prep_path, catalog_path, index_path, higher_path, core_path,
              Path(__file__).resolve(), Path(__file__).with_name('divination_rank7_proposals.py')}
    prep, index, higher, core = (read(p) for p in [prep_path, index_path, higher_path, core_path])
    catalog = {s['id']: s for s in read(catalog_path)['spells']}
    entries = {s['id']: s for s in index['entries']}
    higher_entries = {s['spellId']: s for s in higher['entries']}
    selected = {s['spellId']: s for s in prep['selectedSpells'] if s['scope'] == 'pre-push mechanical source question'}
    deferred = [s for s in prep['selectedSpells'] if s['scope'] == 'post-push receipt only']
    checks = []

    def check(name, passed):
        checks.append({'name': name, 'pass': bool(passed)})
        assert passed, name

    check('Exactly seven DI7 mechanical identities and one deferred source',
          len(PROPOSALS) == len(selected) == 7 and {p['spellId'] for p in PROPOSALS} == set(selected) and len(deferred) == 1)
    check('Ordinary catalog still848, reviewed412, pending436',
          len(catalog) == 848 and index['authoredCounts'] == {'reviewed': 412, 'pending': 436})
    check('Actual Wizard13 maximum48 and Cleric13 maximum36',
          core['caster_pools']['Wizard'][12] == 48 and core['caster_pools']['Cleric'][12] == 36)
    expected_access = {name: {'rank': 7, 'minimumClassLevel': level, 'school': 'Divination', 'baseRpCost': 17}
                       for name, level in [('Cleric', 13), ('Mirrorsage', 19), ('Shaman', 19), ('Wizard', 13)]}
    records = []
    for proposal in PROPOSALS:
        sid = proposal['spellId']
        source, prepared = catalog[sid], selected[sid]
        digest = sha256(json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        check(sid + ' complete source record and prepared digest', source == prepared['fullSourceAndCurrentAccessRecord'] and digest == prepared['recordSha256'])
        check(sid + ' exact four-class rank7 access', source['classAccess'] == expected_access)
        check(sid + ' ordinary spell remains pending with no operation', source['operational'] is None and entries[sid]['authoredStatus'] == 'pending-authored-procedure')
        check(sid + ' original Core entry preserved', all(core['spells'][e['index']] == e['original'] for e in source['source']['coreEntries'] + source['source']['possibleHistoricalAliases']))
        check(sid + ' procedure, two authored examples and explicit new decisions present',
              bool(proposal['procedure'].strip()) and len(proposal['workedCases']) == 2 and all(c.strip() for c in proposal['workedCases']) and proposal['newChoices'].startswith('NEW'))
        records.append({**proposal, 'questionId': prepared['questionId'], 'originalQuestion': prepared['individualQuestion'],
                        'fullSourceAndCurrentAccessRecord': source, 'sourceRecordSha256': digest,
                        'status': 'unadopted-unsent-operating-proposal', 'examplesAreRuntimeTests': False})
    check('Seven complete mechanical Core entries', sum(len(r['fullSourceAndCurrentAccessRecord']['source']['coreEntries']) for r in records) == 7)
    for item in deferred:
        sid = item['spellId']
        check(sid + ' complete deferred receipt unchanged and without operation',
              item['fullSourceAndCurrentAccessRecord'] == catalog[sid] and catalog[sid]['operational'] is None and sid not in selected)
        check(sid + ' full literal Core entry retained', all(core['spells'][e['index']] == e['original'] for e in catalog[sid]['source']['coreEntries']))
    check('Greater Planar Summons remains literal CR8-each two allies',
          deferred[0]['spellId'] == 'planar-summons-greater' and 'CR 8' in catalog['planar-summons-greater']['source']['coreEntries'][0]['original']['effect'])

    cids = sorted({s['id'] for s in prep['completeCounterparts']} | {'counterspell', 'greater-dispel', 'resonance-sight-greater'})
    counterparts, earlier, pending, unresolved = [], [], [], []
    for sid in cids:
        entry = entries[sid]
        path = catalog_path.parent / entry['procedureFile']
        whole = read(path)
        inputs.add(path)
        for key in entry['wholeCardPointer'].strip('/').split('/'):
            whole = whole[int(key)] if isinstance(whole, list) else whole[key]
        check(sid + ' current whole counterpart identity', whole.get('id', whole.get('spellId')) == sid)
        operation = whole.get('operational', whole.get('operationalCandidate'))
        reviewed = entry['authoredStatus'] == 'reviewed-authored-operational-playtest'
        check(sid + ' current counterpart status agrees with whole record',
              (reviewed and isinstance(operation, dict)) or (entry['authoredStatus'] == 'pending-authored-procedure' and whole.get('operational') is None))
        counterparts.append({'id': sid, 'completePreparedComparisonOccurrences': [s for s in prep['completeCounterparts'] if s['id'] == sid],
                             'currentSourceCatalogRecord': catalog[sid], 'currentAuthoredIndexEntry': entry, 'completeCurrentAuthoredRecord': whole})
        if not reviewed:
            pending.append(sid)
            prior_entry = higher_entries[sid]
            if prior_entry['proposalState'] != 'complete-unadopted-proposal':
                check(sid + ' explicitly retains its unresolved procedure status', prior_entry['proposalState'] == 'source-question-prepared-procedure-not-yet-proposed')
                source_path = G / prior_entry['preparationFile']
                source_prep = read(source_path)
                inputs.add(source_path)
                source_questions = [s for s in source_prep['selectedSpells'] if s['spellId'] == sid]
                check(sid + ' complete unresolved source question retained', len(source_questions) == 1)
                unresolved.append({'id': sid, 'currentHigherIndexEntry': prior_entry, 'completeSourceQuestion': source_questions[0],
                                   'status': 'No complete procedure exists yet; comparison is source-only and supplies no approved rule.'})
                continue
            path = G / prior_entry['proposalFile']
            prior = read(path)
            inputs.add(path)
            matches = [r for r in prior['records'] if r['spellId'] == sid]
            check(sid + ' one full earlier unadopted counterpart', len(matches) == 1)
            earlier.append({'proposalFile': path.relative_to(G).as_posix(), 'completeSharedProposal': prior['sharedProposal'], 'completeProposalRecord': matches[0]})
    check('All fourteen current counterparts and each pending state retained', len(counterparts) == 14 and len(earlier) + len(unresolved) == len(pending))
    guides = {}
    for excerpt in prep['currentGoverningExcerpts']:
        path = G / excerpt['file']
        inputs.add(path)
        guides.setdefault(excerpt['file'], {'currentFile': info(path), 'fullCurrentText': path.read_text('utf-8'), 'preparedExcerpts': []})['preparedExcerpts'].append(excerpt)
    for name in ['CLASS_PLAYTEST_RULES.md', 'MAXIMUM_HP_PLAYTEST.md', 'ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md',
                 'expedition/EXPEDITION_PLAYER_BOOK.md', 'expedition/EXPEDITION_DIRECTOR_BOOK.md']:
        path = R / 'docs/mechanics' / name
        inputs.add(path)
        guides.setdefault(path.relative_to(G).as_posix(), {'currentFile': info(path), 'fullCurrentText': path.read_text('utf-8'), 'preparedExcerpts': []})
    classes = []
    for slug in ['bard', 'cleric', 'crimson-agent', 'dragoon', 'druid', 'mage', 'mirrorsage', 'monk', 'oracle', 'paladin', 'ranger', 'shaman', 'soldier', 'thief', 'tinker', 'warrior', 'wizard']:
        path = R / 'data/public/Decennium_Descent_Bard_Playtest_v0_1.json' if slug == 'bard' else R / f'data/public/class_playtests/{slug}.json'
        inputs.add(path)
        classes.append({'path': path.relative_to(G).as_posix(), **info(path), 'completeCurrentEnvelope': read(path)})
    check('All17 class envelopes included without promotion', len(classes) == 17)
    check('Prepared textual class comparisons are preserved as actually empty', prep['classComparisonRecords'] == [])
    arithmetic = [('Base-price rank7 cast remainder', 48 - 17, 31),
                  ('Two separately priced casts before modifiers or independent costs', 48 - 17 - 2, 29),
                  ('Wizard13 save DC', 8 + 5 + 4, 17),
                  ('Proposed three-round elapsed lookback', 3 * 6, 18)]
    for name, actual, expected in arithmetic:
        check(name, actual == expected)
    now = datetime.now(timezone.utc).isoformat()
    source_info = {p.relative_to(G).as_posix(): info(p) for p in sorted(inputs)}
    save(draft, {'status': SHARED['status'], 'createdAtUtc': now, 'sharedProposal': SHARED, 'proposals': PROPOSALS, 'explicitJointIssues': ISSUES})
    save(out, {'status': SHARED['status'], 'createdAtUtc': now, 'sharedProposal': SHARED, 'records': records,
               'explicitJointIssues': ISSUES, 'completeCurrentCounterparts': counterparts,
               'earlierUnadoptedCounterpartProposals': earlier, 'unresolvedCounterpartQuestions': unresolved, 'completeClassComparisons': classes,
               'preservedTextualClassComparisons': prep['classComparisonRecords'], 'currentGoverningDocuments': guides,
               'completeOriginalPreparations': [prep], 'completeUntouchedDeferredReceipts': deferred,
               'originalBookBindings': prep['currentBookBindings'], 'sourceFiles': source_info,
               'runtimeImplemented': False, 'cosmologyReviewed': False, 'sourceInformationDeleted': 0, 'pushed': False})
    def link(path):
        return Path(os.path.relpath(path, doc.parent)).as_posix()
    lines = ['# Rank-seven Divination operating proposals', '', '**' + SHARED['status'] + '**', '',
             '[Complete structured proposal and source context](' + link(out) + ') · [Source and rendering checks](' + link(receipt) + ')', '', '## Shared procedures', '']
    for key, value in SHARED.items():
        if key != 'status':
            lines += ['### ' + key, '', value, '']
    lines += ['## Questions for joint review', '']
    for issue in ISSUES:
        lines += ['- **' + issue['id'] + '** — ' + issue['issue'], '']
    for record in records:
        lines += ['## ' + record['questionId'] + ' — ' + record['fullSourceAndCurrentAccessRecord']['name'], '',
                  '**Original question:** ' + record['originalQuestion'], '', record['procedure'], '',
                  '**New decisions:** ' + record['newChoices'], '', '### Authored examples', '']
        for case in record['workedCases']:
            lines += [case, '']
        lines += ['### Complete preserved source and access', '', '```json',
                  json.dumps(record['fullSourceAndCurrentAccessRecord'], ensure_ascii=False, indent=2), '```', '']
    lines += ['## Literal post-push receipt', '']
    for item in deferred:
        lines += [item['questionId'] + ' — ' + item['fullSourceAndCurrentAccessRecord']['name'], '', item['individualQuestion'], '',
                  '```json', json.dumps(item['fullSourceAndCurrentAccessRecord'], ensure_ascii=False, indent=2), '```', '']
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    rendered = doc.read_text('utf-8')
    for record in records:
        check(record['spellId'] + ' full procedure/source and examples rendered',
              record['procedure'] in rendered and all(c in rendered for c in record['workedCases']) and
              json.dumps(record['fullSourceAndCurrentAccessRecord'], ensure_ascii=False, indent=2) in rendered)
    for item in deferred:
        check(item['spellId'] + ' complete deferred receipt rendered', json.dumps(item['fullSourceAndCurrentAccessRecord'], ensure_ascii=False, indent=2) in rendered)
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', rendered):
        check('Local manuscript link: ' + target, (doc.parent / target).resolve().is_file() or (doc.parent / target).resolve() == receipt)
    check('Saved structured records and deferred receipts round-trip', read(out)['records'] == records and read(out)['completeUntouchedDeferredReceipts'] == deferred)
    for name, binding in source_info.items():
        check('Source unchanged: ' + name, info(G / name) == binding)
    result = {'createdAtUtc': now, 'status': SHARED['status'], 'completeMechanicalProposals': len(records),
              'authoredExamples': sum(len(r['workedCases']) for r in records), 'untouchedPostPushReceipts': len(deferred),
              'completeCurrentCounterparts': len(counterparts), 'reviewedCurrentCounterparts': len(counterparts) - len(pending),
              'pendingCurrentCounterparts': len(pending), 'earlierFullUnadoptedCounterpartProposals': len(earlier),
              'counterpartsWithoutCompleteProposal': [u['id'] for u in unresolved],
              'completeComparisonClasses': len(classes), 'newJointIssues': len(ISSUES), 'checks': len(checks), 'failures': 0,
              'plainArithmeticChecks': len(arithmetic), 'boundedReferenceModelChecks': 0, 'fullSpellRuntimeCases': 0,
              'ordinarySpellsReviewedUnchanged': 412, 'ordinarySpellsPendingUnchanged': 436,
              'artifacts': {p.relative_to(G).as_posix(): info(p) for p in [draft, out, doc]},
              'scope': 'Original source/Core/access preservation, current comparison and class context, complete manuscript rendering and four plain arithmetic examples. No independent semantic approval, GPT decision, runtime verification or human balance test.',
              'sourceInformationDeleted': 0, 'cosmologyReviewed': False, 'pushed': False, 'details': checks}
    save(receipt, result)
    print(json.dumps({k: v for k, v in result.items() if k != 'details'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
