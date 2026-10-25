"""Refresh the four rank-eight memory/control source conference for 705/143."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import zipfile


G = Path(__file__).resolve().parents[3]
R = G / 'DescentReviewChanges/ReviewBible'
AUDIT = G / 'docs/audit/2026-10-08/full-game'
OLD = R / 'data/director/spell_review/rank8_memory_control_4_source_conference_01.json'
INDEX = R / 'data/public/spell_playtests/authored_review_index.json'
CATALOG = R / 'data/public/spell_playtests/catalog.json'
QUEUE = AUDIT / 'director-spell-review-129/CURRENT_SPELL_QUEUE_149.json'
HANDOFF = AUDIT / 'director-spell-review-129/CURRENT_HANDOFF_149.json'
PENDING_AUDIT = AUDIT / 'director-spell-review-129/CURRENT143_PENDING_IDENTITY_AUDIT_149.json'
OUT = R / 'data/director/spell_review/rank8_memory_control_4_source_conference_02.json'
ROOT = AUDIT / 'rank8-memory-control4-source-conference-02'
ARCHIVE = AUDIT / 'DD_Rank8_Memory_Control_4_Source_Conference_02.zip'
CHECK = AUDIT / 'RANK8_MEMORY_CONTROL4_SOURCE_CONFERENCE_02_CHECK.json'
PREP = AUDIT / 'RANK8_MEMORY_CONTROL4_SOURCE_CONFERENCE_02_PREPARATION.json'
REQUEST = AUDIT / 'RANK8_MEMORY_CONTROL4_SOURCE_CONFERENCE_02_REQUEST.txt'

CURRENT_GROUP = {
    'group': 'rank8-memory-control4',
    'ids': ['erase-mind', 'feeblemind', 'mass-dominate', 'mind-ravel'],
}

COMPLETED_GROUPS = [
    {
        'group': 'memory2',
        'receipt': AUDIT / 'accepted72-application-122/memory-creation3_APPLICATION.json',
        'model': R / 'data/public/spell_candidates/memory_creation3_reviewed_122.json',
        'directorAcceptance': None,
    },
    {
        'group': 'control15',
        'receipt': AUDIT / 'accepted72-application-122/control15-ready14_APPLICATION.json',
        'model': R / 'data/public/spell_candidates/control15_ready14_reviewed_122.json',
        'directorAcceptance': None,
    },
    {
        'group': 'companion-life10',
        'receipt': AUDIT / 'accepted72-application-122/companion-life10-exact-05_APPLICATION.json',
        'model': R / 'data/public/spell_candidates/companion_life_10_reviewed_05.json',
        'directorAcceptance': None,
    },
    {
        'group': 'rank8-control5',
        'receipt': AUDIT / 'director-spell-review-129/RANK8_CONTROL5_APPLICATION_148.json',
        'model': R / 'data/public/spell_candidates/rank8control5_reviewed_148/MODEL.json',
        'directorAcceptance': AUDIT / 'director-spell-review-129/RANK8_CONTROL5_EXACT_ACCEPTANCE_148.json',
    },
    {
        'group': 'rank8-ward5',
        'receipt': AUDIT / 'director-spell-review-129/RANK8_WARD5_APPLICATION_149.json',
        'model': R / 'data/public/spell_candidates/rank8ward5_reviewed_149/MODEL.json',
        'directorAcceptance': AUDIT / 'director-spell-review-129/RANK8_WARD5_EXACT_ACCEPTANCE_149.json',
    },
]


def read(path):
    return json.loads(path.read_bytes())


def info(path):
    data = path.read_bytes()
    return {'path': path.resolve().relative_to(G).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def at(document, pointer):
    node = document
    for part in pointer.strip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def main():
    for path in [OUT, ROOT, ARCHIVE, CHECK, PREP, REQUEST]:
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite {path}')

    old, index, catalog = map(read, [OLD, INDEX, CATALOG])
    queue, handoff, pending_audit = map(read, [QUEUE, HANDOFF, PENDING_AUDIT])
    checks = []
    sources = {}

    def ck(name, condition):
        checks.append({'check': name, 'passed': bool(condition)})
        if not condition:
            raise AssertionError(name)

    def bind(path):
        path = path.resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        binding = info(path)
        sources[binding['path']] = binding
        return binding

    ck('Current authority is 705 reviewed / 143 pending', index.get('authoredCounts') == {'reviewed': 705, 'pending': 143})
    ck('Current pending audit binds exact index', pending_audit['indexBinding']['sha256'] == info(INDEX)['sha256'])
    ck('Current pending audit counts agree', pending_audit['authoredCounts'] == index['authoredCounts'])
    ck('Ward5 next handoff is Memory/Control4', handoff['nextGroup'] == CURRENT_GROUP['group'])
    group = next(g for g in queue['currentPendingGroups'] if g['group'] == CURRENT_GROUP['group'])
    ck('Queue names exact four pending identities', group['pendingIds'] == CURRENT_GROUP['ids'])
    ck('Pending set audit has four target IDs', set(CURRENT_GROUP['ids']).issubset(set(pending_audit['pendingIds'])))
    ck('No accepted-unapplied batch', handoff['currentAuthority']['acceptedUnapplied'] == 0)

    ix = {e['id']: e for e in index['entries']}
    cards = {s['id']: s for s in catalog['spells']}
    ck('All four target index rows remain pending', all(ix[i]['authoredStatus'] == 'pending-authored-procedure' for i in CURRENT_GROUP['ids']))
    ck('All four target source cards exist', all(i in cards for i in CURRENT_GROUP['ids']))

    for name, obj in [('index', INDEX), ('catalog', CATALOG), ('queue', QUEUE), ('handoff', HANDOFF), ('pending identity audit', PENDING_AUDIT)]:
        bind(obj)

    candidate = deepcopy(old)
    candidate['id'] = 'RANK8-MEMORY-CONTROL4-SOURCE-CONFERENCE02'
    candidate['recordedAtUtc'] = datetime.now(timezone.utc).isoformat()
    candidate['status'] = 'SOURCE_CONFERENCE_PREPARED_UNSENT'
    candidate['supersedes'] = bind(OLD)
    candidate['currentAuthority'] = {
        'reviewedApplied': 705,
        'pending': 143,
        'acceptedUnapplied': 0,
        'completeReviewedStandaloneProcedures': handoff['currentAuthority']['completeReviewedStandaloneProcedures'],
        'scopedInterfaces': handoff['currentAuthority']['scopedInterfaces'],
        'index': bind(INDEX),
        'catalog': bind(CATALOG),
        'queue': bind(QUEUE),
        'handoff': bind(HANDOFF),
        'pendingIdentityAudit': bind(PENDING_AUDIT),
    }
    candidate['targetGroup'] = CURRENT_GROUP
    candidate['countsUnchanged'] = deepcopy(index['authoredCounts'])
    candidate['closedCohortBoundary'] = 'Do not reopen feat335, completed16/72, or any accepted/applied spell cohort. The five completed comparison groups below are context only.'
    bind(Path(__file__))

    # Refresh the four selected records from the live catalog and index.
    for record in candidate['records']:
        ident = record['spellId']
        live_card = cards[ident]
        live_entry = ix[ident]
        ck(f'Current source card unchanged for {ident}', record['completeCurrentCatalogSourceAndAccess'] == live_card)
        ck(f'Current index row pending for {ident}', live_entry['authoredStatus'] == 'pending-authored-procedure')
        record['completeCurrentCatalogSourceAndAccess'] = deepcopy(live_card)
        record['currentIndexEntry'] = deepcopy(live_entry)

    # Build exact completion evidence for comparison cohorts that are already applied.
    completed = []
    for item in COMPLETED_GROUPS:
        receipt = read(item['receipt'])
        model_binding = bind(item['model'])
        receipt_binding = bind(item['receipt'])
        acceptance_binding = bind(item['directorAcceptance']) if item['directorAcceptance'] else None
        accepted_ids = receipt['acceptedIds']
        ck(f"{item['group']} receipt lists accepted IDs", bool(accepted_ids))
        ck(f"{item['group']} identities are already reviewed", all(ix[sid]['authoredStatus'] == 'reviewed-authored-operational-playtest' for sid in accepted_ids if sid in ix))
        ck(f"{item['group']} model receipt hash matches", receipt.get('canonicalModel', {}).get('sha256', model_binding['sha256']) == model_binding['sha256'])
        completed.append({
            'group': item['group'],
            'status': 'APPLIED_COMPLETED_COMPARISON_ONLY',
            'acceptedIds': accepted_ids,
            'applicationReceipt': receipt_binding,
            'canonicalModel': model_binding,
            'directorAcceptance': acceptance_binding,
            'qualification': 'Exact previously accepted/applied authored scope supplied as a closed comparison. Do not reopen, re-review, import unaccepted alternatives, or extend it by analogy.',
        })
    candidate['historicalCompletedComparisonGroups'] = completed
    candidate['pendingComparisonsNotAuthority'] = []

    # Refresh existing evidence bindings, replacing the obsolete live queue and
    # superseded comparison candidates with the current state and applied proof.
    obsolete_fragments = [
        'remaining_work_queue_26.json',
        'memory_2_conference_02.json',
        'control_15_current_12.json',
        'rank8_control_5_source_conference_01.json',
        'rank8_ward_5_source_conference_01.json',
        'companion_life_10_current_05.json',
    ]
    refreshed = {}
    for prior in old['sourceBindings']:
        if any(fragment in prior['path'] for fragment in obsolete_fragments):
            continue
        path = G / prior['path']
        if path.is_file():
            refreshed[prior['path']] = bind(path)
    for entry in candidate['currentAcceptedInterfaceComparisons']:
        source = entry['completeEntryUnchanged']['currentAuthoritativeSource']
        live = bind(G / source['path'])
        entry['liveCurrentBackingSource'] = live
        entry['currentBackingMatchesAcceptedSnapshot'] = live['sha256'] == source['sha256'] and live['bytes'] == source['bytes']
        entry['qualification'] = (
            'The complete registry entry and its exactAuthority text are the accepted comparison. '
            'The live backing file is separately bound; if its hash differs, later edits are not imported as accepted authority.'
        )
        ck(f"Accepted interface embeds exact accepted text {entry['registryPointer']}", bool(entry['completeEntryUnchanged'].get('exactAuthority')))

    # Re-resolve counterpart cards and their current acceptance evidence.
    for counterpart in candidate['completeAcceptedCounterparts']:
        ident = counterpart['spellId']
        live_entry = ix[ident]
        ck(f'Counterpart remains reviewed: {ident}', live_entry['authoredStatus'] == 'reviewed-authored-operational-playtest')
        src_path = G / counterpart['source']['path']
        document = read(src_path)
        ptr = live_entry.get('wholeCardPointer', live_entry.get('procedurePointer'))
        ck(f'Counterpart pointer available: {ident}', bool(ptr))
        prior_card = deepcopy(counterpart['completeCurrentCard'])
        prior_shared = deepcopy(counterpart['completeSharedRules'])
        live_card = deepcopy(at(document, ptr))
        live_binding = bind(src_path)
        counterpart['priorConferenceSourceBinding'] = deepcopy(counterpart['source'])
        counterpart['liveCurrentSourceBinding'] = live_binding
        counterpart['currentLiveCard'] = live_card
        counterpart['currentLiveSharedRules'] = deepcopy(document.get('sharedRules', {}))
        counterpart['currentLiveCardMatchesPriorConferenceSnapshot'] = live_card == prior_card
        counterpart['currentLiveSharedRulesMatchPriorConferenceSnapshot'] = counterpart['currentLiveSharedRules'] == prior_shared
        counterpart['currentLiveSourceMatchesRecordedAcceptedEnvelope'] = None
        if live_entry.get('completeEnvelopeBinding'):
            binding = live_entry['completeEnvelopeBinding']
            counterpart['currentLiveSourceMatchesRecordedAcceptedEnvelope'] = live_binding['bytes'] == binding['bytes'] and live_binding['sha256'] == binding['sha256']
        counterpart['source'] = live_binding
        counterpart['pointer'] = ptr
        counterpart['indexEntry'] = deepcopy(live_entry)
        if live_entry.get('completeEnvelopeBinding'):
            binding = live_entry['completeEnvelopeBinding']
            actual = bind(G / binding['path'])
            counterpart['recordedAcceptedEnvelopeCurrentFileBinding'] = actual
            ck(f'Counterpart accepted envelope path exists: {ident}', actual['path'] == binding['path'])
        if live_entry.get('authoredAcceptanceReceipt'):
            receipt_binding = live_entry['authoredAcceptanceReceipt']
            actual = bind(G / receipt_binding['path'])
            counterpart['recordedAcceptanceReceiptBinding'] = deepcopy(receipt_binding)
            counterpart['liveAcceptanceReceiptFileBinding'] = actual
            counterpart['liveAcceptanceReceiptMatchesRecordedBinding'] = actual['bytes'] == receipt_binding['bytes'] and actual['sha256'] == receipt_binding['sha256']
            ck(f'Counterpart acceptance receipt path exists: {ident}', actual['path'] == receipt_binding['path'])
        for ref in live_entry.get('caseSourceReferenceAliases', {}).values():
            bind(G / ref)
        for rel in counterpart['completeCurrentCard'].get('operational', {}).get('sourceReview', []) + counterpart['completeCurrentCard'].get('operational', {}).get('reviewEvidence', []):
            bind(G / rel)
        counterpart['qualification'] = (
            'The prior conference card snapshot is preserved as the exact comparison supplied at that time. '
            'Live source and index/acceptance bindings are also supplied; changes in the live file do not silently expand the accepted scope.'
        )

    # Reassert exact original source placements and manuscript quotations.
    lines = (R / 'rulebook_output.txt').read_text('utf-16').splitlines()
    reference = (G / 'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf-8').splitlines()
    bind(R / 'rulebook_output.txt')
    bind(G / 'docs/reference/Player_Rulebook_v6_source_text.txt')
    for record in candidate['records']:
        ident = record['spellId']
        placements = record['completeCurrentBookBindings']
        ck(f'Exact native placement count: {ident}', len(placements) == 1 == len(cards[ident]['source']['original']['placements']))
        for placement in placements:
            pos = placement['currentBookRow']['line'] - 1
            ck(f'Exact manuscript line in both copies: {ident}', lines[pos] == placement['currentBookRow']['exactText'] == reference[pos])

    # MC8-X01 was true when the first packet was prepared. Replace it with the
    # current, exact closed-comparison state.
    x01 = next(q for q in candidate['questions'] if q['id'] == 'MC8-X01')
    x01['exactSourceOrConflict'] = 'Mind Blank (Ward5), Mental Collapse (Control5), Memory/Creation3 (including Woven Threads and Haze of Forgetting), Control15, and Companion/Life10 have all been accepted and applied. Their exact application/model evidence is attached as closed comparisons; none supplies broader authority to these four cards.'
    x01['options'] = [
        'State component predicates and exact cross-source boundaries; cite the five completed comparison groups only within their accepted and applied scope.',
        'Reopen a prior accepted interface only on a concrete conflicting actual passage, preserving that passage and decision history.'
    ]
    x01['recommendationAndConsequences'] = 'Use the first. A mental-themed name or Divination school does not grant immunity, a memory readout, action denial, restoration, inaccessible knowledge, or a cosmology decision. Do not reopen any completed group.'

    # 21 original source questions remain unselected; only their current context
    # changes, not the proposed answers or unresolved decisions.
    ck('Exactly 21 unique, unselected questions', len(candidate['questions']) == 21 and len({q['id'] for q in candidate['questions']}) == 21 and all(q['decisionSelected'] is False for q in candidate['questions']))
    ck('Every target identity appears in the questions', set().union(*(set(q['spellIds']) for q in candidate['questions'])) == set(CURRENT_GROUP['ids']))
    ck('Four exact identities and four source placements', len(candidate['records']) == 4 and sum(len(r['completeCurrentBookBindings']) for r in candidate['records']) == 4)
    ck('No completed comparison cohort overlaps current targets', not set(CURRENT_GROUP['ids']).intersection(*(set(x['acceptedIds']) for x in completed)))

    candidate['sourceFindings'] = [
        'Erase Mind event/lookback and identity rider remain undefined; no full-world history erasure is printed.',
        'Feeblemind fixes actual INT/CHA scores to 1, not modifiers. No initial save or named recovery is printed; reconcile its Instantaneous metadata with continuing restrictions.',
        'Mass Dominate keeps up to 3 actual CR<=10 creatures, WIS each turn and concentration for 1 minute; no guessed class-level-to-CR conversion or new finite-resource control.',
        'Mind Ravel has an exact last-5-minute memory scope and WIS save, but no operational confusion lifetime; memory and control defenses/ending need separate treatment.',
        'Disrupt Memory is accepted instantaneous firsthand loss with world-state preservation. Memory/Creation3 has now accepted and applied Woven Threads/Haze of Forgetting; use only its exact received scope and do not generalize recovery.',
        'Actual Dominate Person and Confusion complete native procedures and RNG/presentation scopes are supplied. Any extension requires a specific per-card decision.',
        'Wizard prepared matrices, negative actual modifiers, and Tinker controller prerequisites retain actual source timing; score changes are not automatic repertoire erasure or resource refunds.',
        'Identity shaken is not a Unity Exposure, Corruption, alignment, or cosmological identity change. No cosmology decision is made.',
        'Memory/Creation3, Control15, Companion/Life10, Rank8 Control5, and Rank8 Ward5 are accepted and applied comparison groups. Their current receipts/models are included; none remains pending.'
    ]
    candidate['gptCommunication'] = 'Prepared for Calibration review part 6 against 705 applied / 143 pending / 0 accepted-unapplied. The earlier _01 source conference is superseded. GPT remains the source/procedure authoring director; this _02 packet has not been delivered or decided.'
    candidate['currentVectors'] = []
    candidate['earlierOperationalWorkedCases'] = []
    candidate['newRuleAdoptions'] = 0
    candidate['runtimeTestsExecuted'] = 0
    candidate['humanPlaytests'] = 0
    candidate['sourceInformationDeleted'] = 0
    candidate['cosmologyDecisions'] = 0
    candidate['wholeGameComplete'] = False

    # Bind the refreshed set rather than retaining hashes from the stale packet.
    for path_text, binding in refreshed.items():
        path = G / path_text
        ck(f'Source unchanged while refreshing: {path_text}', info(path) == binding)
    candidate['sourceBindings'] = sorted(sources.values(), key=lambda b: b['path'])

    ROOT.mkdir(parents=True)
    frozen_sources = []
    for binding in candidate['sourceBindings']:
        source_path = G / binding['path']
        ck(f'Live source hash exact: {binding["path"]}', info(source_path) == binding)
        frozen = ROOT / 'sources' / binding['path']
        frozen.parent.mkdir(parents=True, exist_ok=True)
        frozen.write_bytes(source_path.read_bytes())
        ck(f'Frozen source bytes exact: {binding["path"]}', frozen.read_bytes() == source_path.read_bytes())
        frozen_sources.append({**binding, 'frozenCopy': frozen.relative_to(G).as_posix()})

    OUT.write_bytes(encoded(candidate))
    source_check = {
        'candidate': info(OUT),
        'checkCount': len(checks),
        'checks': checks,
        'sourceCount': len(sources),
        'targetIdentityCount': len(CURRENT_GROUP['ids']),
        'questionCount': len(candidate['questions']),
        'completedComparisonGroups': len(completed),
        'failures': 0,
        'validationScope': 'Current authority, exact source/access/index bindings, closed comparison receipts, manuscript placement and preservation only; no semantic adoption or runtime execution.'
    }
    CHECK.write_bytes(encoded(source_check))
    manifest = ROOT / 'MANIFEST.json'
    manifest.write_bytes(encoded({
        'candidate': info(OUT),
        'check': info(CHECK),
        'files': candidate['sourceBindings'],
        'frozenSources': frozen_sources,
        'sourceCount': len(sources),
        'targetIdentityCount': len(CURRENT_GROUP['ids']),
        'questionCount': len(candidate['questions']),
        'completedComparisonGroups': [g['group'] for g in completed],
        'newRuleAdoptions': 0,
    }))
    readme = (
        'Fresh 705/143 source conference for four exact rank-eight Memory/Control spell identities. '
        'Read CANDIDATE.json and the frozen source files. All 21 source questions remain unselected. '
        'The five listed prior cohorts are accepted and applied closed comparisons; do not reopen them or infer expanded approval. '
        'No new operative rule, case, runtime result, human-play result, balance decision, cosmology decision, or release approval is adopted here.\n'
    )
    (ROOT / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    with zipfile.ZipFile(ARCHIVE, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(OUT, 'CANDIDATE.json')
        z.write(CHECK, 'SOURCE_CHECK.json')
        z.write(manifest, 'MANIFEST.json')
        z.writestr('README.md', readme)
        for binding in candidate['sourceBindings']:
            z.write(ROOT / 'sources' / binding['path'], 'sources/' + binding['path'])
    with zipfile.ZipFile(ARCHIVE) as z:
        ck('Archive integrity', z.testzip() is None)
        ck('Archive member paths unique', len(z.namelist()) == len(set(z.namelist())))
        ck('Candidate bytes round-trip', z.read('CANDIDATE.json') == OUT.read_bytes())
        ck('All frozen sources round-trip', all(z.read('sources/' + b['path']) == (G / b['path']).read_bytes() for b in candidate['sourceBindings']))

    archive_info = info(ARCHIVE)
    request = (
        f"GPT — review the exact fresh Memory/Control4 source conference packet attached: {ARCHIVE.name}, "
        f"{archive_info['bytes']} bytes, SHA-256 {archive_info['sha256']}. It is bound to 705 applied / 143 pending / "
        '0 accepted-unapplied. Review only erase-mind, feeblemind, mass-dominate, and mind-ravel. Resolve all 21 source questions; '
        'return complete source-faithful procedures, all dispositions, and independently checked operational cases/branches. '
        'Use the attached Memory/Creation3, Control15, Companion/Life10, Rank8 Control5, and Rank8 Ward5 records only as exact completed comparisons; '
        'do not reopen or broaden those accepted/applied cohorts. Preserve all source, access, content, physical, runtime, cosmology, and release holds. '
        'If the exact submitted package passes, state accepted=true and applied=false for only the exact accepted IDs; if anything fails, leave it unaccepted/unapplied and identify exact blockers. '
        'Do not edit or apply canonical files. Feat335, completed16/72, and all other completed spell cohorts remain closed.\n'
    )
    REQUEST.write_text(request, encoding='utf-8', newline='\n')
    PREP.write_bytes(encoded({
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'PREPARED_UNSENT',
        'candidate': info(OUT),
        'archive': archive_info,
        'manifest': info(manifest),
        'check': info(CHECK),
        'request': info(REQUEST),
        'sourceCount': len(sources),
        'identityCount': len(CURRENT_GROUP['ids']),
        'questionCount': len(candidate['questions']),
        'completedComparisonGroups': len(completed),
        'allArchiveMembersVerified': True,
        'newRuleAdoptions': 0,
        'sourceInformationDeleted': 0,
    }))
    print(json.dumps({'candidate': info(OUT), 'archive': archive_info, 'checks': len(checks), 'sources': len(sources), 'questions': len(candidate['questions']), 'completedComparisonGroups': len(completed), 'failures': 0}, indent=2))


if __name__ == '__main__':
    main()
