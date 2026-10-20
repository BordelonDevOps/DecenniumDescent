"""Freeze complete native sources and unselected rank-nine psychic/fear questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank9_psychic_fear_7_questions_01 import IDS, TIERS, Q


def read(p): return json.loads(p.read_bytes())


def main():
    stem = 'RANK9_PSYCHIC_FEAR_7_SOURCE_CONFERENCE_01'
    root = A / 'rank9-psychic-fear7-source-conference-01'
    out = R / 'data/director/spell_review/rank9_psychic_fear_7_source_conference_01.json'
    check, prep, request = [A / (stem + s) for s in ['_CHECK.json', '_PREPARATION.json', '_REQUEST.txt']]
    archive = A / 'DD_Rank9_Psychic_Fear_7_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources = {}; checks = []
    def ck(label, ok):
        checks.append({'check': label, 'passed': bool(ok)}); assert ok, label
    def bind(p):
        b = info(p); sources[b['path']] = b; return b
    catp = R / 'data/public/spell_playtests/catalog.json'
    ip = catp.parent / 'authored_review_index.json'
    qp = R / 'data/director/spell_review/remaining_work_queue_38.json'
    regp = R / 'data/director/spell_review/accepted_interface_registry_06.json'
    cov = R / 'data/playtest/game_development_coverage.json'
    protected = {p: p.read_bytes() for p in [catp, ip, qp, regp, cov]}
    catalog, index, queue, registry = map(read, [catp, ip, qp, regp])
    olds = [A / (s + '_RANK9_SOURCE_PREPARATION.json') for s in ['ENCHANTMENT', 'EVOCATION', 'ILLUSION', 'NECROMANCY']]
    histories = [read(p) for p in olds]
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_STORM_CONTROL_46.json'
    pushp = G / 'docs/audit/2026-10-18/github-snapshot-storm-control46/PUSH_RECEIPT.json'
    push = read(pushp)
    ck('Verified post-push gate', push['commit'] == push['remoteMain'] == 'ccb9047a76e9807250feee6d72285c268957d20b' and push['trackedEntriesDeleted'] == 0)
    ck('Applied index unchanged', index['authoredCounts'] == {'reviewed': 525, 'pending': 323} and index['representationCounts']['completeReviewedStandaloneProcedures'] == 249)
    ck('173 scoped interfaces', len(registry['entries']) == 173)
    for p in [catp, ip, qp, regp, cov, *olds, checkpoint, pushp, Path(__file__),
              Path(__file__).with_name('rank9_psychic_fear_7_questions_01.py'),
              R / 'rulebook_output.txt', G / 'docs/reference/Player_Rulebook_v6_source_text.txt',
              R / 'books/player/Decennium_Descent_Player_Rulebook_v6.docx']:
        bind(p)
    lines = (R / 'rulebook_output.txt').read_text('utf-16').splitlines()
    reference = (G / 'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf8').splitlines()
    records = []
    for ident in IDS:
        j = next(j for j, h in enumerate(histories) if any(s['spellId'] == ident for s in h['selectedSpells']))
        prior = histories[j]
        n = next(n for n, s in enumerate(prior['selectedSpells']) if s['spellId'] == ident)
        historical = prior['selectedSpells'][n]
        card = next(s for s in catalog['spells'] if s['id'] == ident)
        row = next(s for s in queue['rows'] if s['id'] == ident)
        entry = next(e for e in index['entries'] if e['id'] == ident)
        ck('Complete source/access equality ' + ident, historical['fullSourceAndCurrentAccessRecord'] == card == row['completeCurrentSourceAndAccess'])
        ck('No prior complete procedure ' + ident, row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Pending identity ' + ident, entry['authoredStatus'] == 'pending-authored-procedure')
        ck('Actual rank9 access and price ' + ident, all(a['rank'] == 9 and a['minimumClassLevel'] == 17 and a['baseRpCost'] == 26 for a in card['classAccess'].values()))
        books = [deepcopy(b) for b in prior['currentBookBindings'] if b['spellId'] == ident]
        ck('All school placements ' + ident, len(books) == len(card['source']['original']['placements']) == (3 if ident == 'psychic-scream' else 2 if ident == 'weird' else 1))
        for b in books:
            p = b['currentBookRow']['line'] - 1
            ck('Both manuscript lines exact ' + ident + ':' + str(p), lines[p] == b['currentBookRow']['exactText'] == reference[p])
        for k in ['catalog', 'core']:
            ck('Full underlying source ' + ident + ':' + k, bind(R / card['source'][k + 'Path'])['sha256'] == card['source'][k + 'Sha256'])
        for cls in card['classAccess']:
            bind(R / ('data/public/class_playtests/' + cls.lower() + '.json'))
        records.append({'spellId': ident, 'riskTier': TIERS[ident][0], 'riskReason': TIERS[ident][1],
            'completeCurrentCatalogSourceAndAccess': deepcopy(card), 'currentIndexEntry': deepcopy(entry),
            'originalQuestionSource': info(olds[j]), 'originalQuestionPointer': '/selectedSpells/' + str(n),
            'completeOriginalSourceQuestionUnchanged': deepcopy(historical),
            'completeHistoricalCommonQuestionUnchanged': prior['commonOperationalQuestion'],
            'completeHistoricalScopeExceptionUnchanged': prior['commonQuestionException'],
            'completeCurrentBookBindings': books, 'earlierCompleteProcedures': [], 'earlierOperationalWorkedCases': [],
            'status': 'Prepared source conference; questions unselected and no operational procedure adopted.'})
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md', 'CLASS_PLAYTEST_RULES.md', 'SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md',
                 'HEALING_DEATH_PLAYTEST.md', 'DAMAGE_SHARING_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md',
                 'FORM_TEMP_HP_PLAYTEST.md', 'MAXIMUM_HP_PLAYTEST.md', 'CRAFTING_HARVEST_PLAYTEST.md',
                 'EQUIPMENT_ITEM_PROCEDURES.md', 'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md']:
        bind(R / 'docs/mechanics' / name)
    bind(R / 'data/public/class_playtests/oracle.json')
    inherited = []
    for n in list(range(12)) + [13, 14, 16, 17, 18, 19, 36, 39, 40] + list(range(108, 117)) + [119] + list(range(143, 152)) + [169, 171]:
        entry = registry['entries'][n]; b = entry['currentAuthoritativeSource']; actual = bind(G / b['path'])
        ck('Current exact scoped interface ' + str(n), all(actual[k] == b[k] for k in ['bytes', 'sha256']))
        inherited.append({'registryPointer': '/entries/' + str(n), 'completeEntryUnchanged': deepcopy(entry),
            'scopeLimit': 'Only the named accepted scope. New school variant, head-destruction, nightmare, flight, secondary-effect, pulse and root extensions require explicit per-spell selection.'})
    counterparts = []
    for ident in ['fear', 'phantasmal-killer', 'greater-phantasmal-killer', 'synaptic-static',
                  'frozen-tomb', 'greater-dispel', 'antimagic-field-lesser']:
        e = next(e for e in index['entries'] if e['id'] == ident)
        ck('Actually applied counterpart ' + ident, e['authoredStatus'] == 'reviewed-authored-operational-playtest')
        p = (ip.parent / e['procedureFile']).resolve(); d = read(p); ptr = e.get('wholeCardPointer') or e['procedurePointer']; b = bind(p)
        if e.get('completeEnvelopeBinding'): ck('Exact envelope ' + ident, b == e['completeEnvelopeBinding'])
        if e.get('authoredAcceptanceReceipt'): ck('Exact acceptance receipt ' + ident, bind(G / e['authoredAcceptanceReceipt']['path']) == e['authoredAcceptanceReceipt'])
        for source in e.get('caseSourceReferenceAliases', {}).values(): bind(G / source)
        card = deepcopy(at(d, ptr)); op = card.get('operational')
        if isinstance(op, dict):
            for rel in op.get('sourceReview', []) + op.get('reviewEvidence', []): bind(G / rel)
            if op.get('authoringFile'): bind(R / op['authoringFile'])
        counterparts.append({'spellId': ident, 'source': b, 'pointer': ptr, 'completeCurrentCard': card,
            'completeSharedRules': deepcopy(at(d, e['sharedRulesPointer']) if e.get('sharedRulesPointer') else d.get('sharedRules', {})),
            'indexEntry': deepcopy(e), 'qualification': 'Exact applied source and acceptance control historical labels. This does not grant the new spell its counterpart’s source-specific exceptions.'})
    lore = []
    for name in ['The Cosmology of Decennium Descent.docx', 'The Decennium Descent and the Matrix of Oblivion.docx',
                 'The_World_of_Aethel_Lore.docx', 'webpage.html', 'docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md']:
        lore.append({'source': bind(G / name), 'scope': 'Full original source; later explicit owner corrections take precedence only where stated. No new plane identity, personal-time physics, storm divinity or Hunt exception is inferred.'})
    for name in ['CURRENT_COSMOLOGY_READ_FIRST.md', 'PLANES_REVIEWED_01.md', 'OWNER_RECONCILIATION_REVIEWED_01.md',
                 'HEARTCELL_OWNER_UPDATE_02.md', 'SOULS_RESEARCH_REVIEWED_01.md', 'EPILOGUE_RELIC_NULL_REVIEWED_01.md']:
        lore.append({'source': bind(R / 'docs/director-only/cosmology' / name), 'scope': 'Current bounded owner reconciliation or operational companion; historical pending workflow labels do not supersede actual later application records.'})
    for name in ['planes_reviewed_01.json', 'owner_reconciliation_reviewed_01.json', 'heartcell_owner_update_02.json',
                 'souls_research_reviewed_01.json', 'epilogue_relic_null_reviewed_01.json']:
        bind(R / 'data/director/cosmology' / name)
    pending = []
    for name in ['rank8-perception5', 'rank9-catastrophe10', 'rank9-storm-control6']:
        group = next(g for g in queue['groups'] if g['group'] == name)
        b = bind(G / group['candidate']['path']); ck('Exact pending comparison ' + name, b == group['candidate'])
        pending.append({'group': name, 'candidate': b, 'identities': group['identities'], 'qualification': 'Pending source conference only; none of its choices are adopted authority.'})
    control = {'receipt': bind(A / 'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json'),
        'selectedSuccessor': bind(A / 'control15-full-conference-part5-return-02/successor/CONTROL15_REVIEWED_SUCCESSOR13.json'),
        'reviewReceipt': bind(A / 'control15-full-conference-part5-return-02/REVIEW_RECEIPT.json'),
        'qualification': 'Exact full semantic acceptance but unapplied. Ordinary Ready and the distinct companion phase bridges are accepted only in the exact returned Control successor. They do not automatically select new flight/nightmare/secondary-effect rules or implement full copied Ready.'}
    questions = [{'id': qid, 'spellIds': ids, 'exactSourceOrConflict': src, 'options': options,
                  'recommendationAndConsequences': recommendation, 'decisionSelected': False}
                 for qid, ids, src, options, recommendation in Q]
    ck('23 unique unselected questions', len(questions) == len({q['id'] for q in questions}) == 23 and all(not q['decisionSelected'] for q in questions))
    ck('Every identity covered', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records)); ck('Individual risks four B three C', risk == {'B': 4, 'C': 3})
    ck('Seven complete identities ten placements', len(records) == 7 and sum(len(r['completeCurrentBookBindings']) for r in records) == 10)
    findings = [
        'All seven actual routes are rank9/minimumclasslevel17/base26RP; preserve Action,V/S/F and exact class-school access. Phantom Armageddon has Cleric/Druid/Wizard; Psychic Scream Mage Evocation/Wizard Enchantment; the other five are Wizard-only.',
        'Psychic Scream has three placements with14d6psychic/up to10creatures. Evocation supplies stun; Enchantment/Illusion possible head destruction. Neither a free school switch nor a union of riders is currently selected.',
        'Weird has two placements but one actual Wizard Enchantment route. Its30-foot radius,nightmare captivity and4d10perround are substantive; no existing finite duration or complete trapped state can be assumed.',
        'Phantom Armageddon preserves60-foot radius,12d10necrotic and fear to all enemies. Phantom Cataclysm preserves12d10psychic,one-round stun and subjective world-ending belief; no actual destruction or prophecy is granted.',
        'Frightful Sovereignty preserves one6d6psychic event and WIS-or-flee for three rounds. Successful-save damage and exact movement/Action obligations are explicit questions; ordinary Fear does not itself cause flight.',
        'Mass Phantom Killer preserves up tofive enemies,6d6psychic per round and WIS ending saves. Its independently ending applications are not free retargets; the title adds no instant death or fear.',
        'Reality Break preserves one10d12force event plus meaningful additional effects and WIS saves. A complete native finite effect table/schedule is missing and must be selected; no foreign table or world-rewrite power is assumed.',
        'Full Control15 and Illusion14 acceptances are preserved as exact accepted-but-unapplied context,not current registry changes.39 accepted identities remain unapplied; all23 new choices remain unselected.']
    cases = [
        'Create at least two full source-qualified cases per identity after decisions,plus each substantive school/state branch. Supply actual repertoire,class level,ability/PB,components,RP/cadence and concentration/counter/Ready history.',
        'Preserve whole occupied3D geometry,known hostility/perception,source IDs,original clocks,all RNG inputs,intermediate damage/condition/movement transactions and final states. No invented creature immunity,CR,attack profile or hidden information.',
        'Psychic Scream requires both actually accessible school variants,all14d6,positive head-remains and stun cases,and explicit headless/multihead/form/survival/Null branches. Do not replace one rider with the easier other one.',
        'Phantom Armageddon/Cataclysm require full actual enemy scope,independent damage/condition defenses and exact finite endpoints; the private catastrophe does not destroy physical terrain.',
        'Frightful Sovereignty requires real three-round flight,actual safe route and movement/Action expenditure,blocked/unknown-source paths and suppression preserving spent history.',
        'Mass Phantom Killer requires five independent applications/ending saves,real6d6pulses,initial versus later exposure,death/form changes and no extra entry/recast/turn pulses.',
        'Weird requires meaningful nightmare captivity with4d10recurrence,actual allied exposure,escape/help/TrueSeeing policies and a complete finite ending. Damage-only or rejection-only coverage is insufficient.',
        'Reality Break requires the full chosen additional-effect procedure,all random selection operands or declared choice,exact WIS timing,independent hard-control admission and source ending. No unspecified future effect can count as a complete case.',
        'Actual Null,temporaryHP,Wounds,death/concentration and source-qualified defenses must be applied at their accepted stages. Separate source preservation,authored semantics,arithmetic,engine/runtime,human play,balance,cosmology and release.']
    illusion = {'model': bind(A/'illusion-perception14-exact-13/SPELLS_MODEL.json'),
        'receipt': bind(A/'GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json'),
        'qualification': 'Full exact Illusion14 model and actual receipt,accepted but unapplied. True Seeing has only its selected source-specific recognition/removal scope; no blanket ending of all psychic damage.'}
    candidate = {'id': 'RANK9-PSYCHIC-FEAR7-SOURCE-CONFERENCE01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'SOURCE_CONFERENCE_PREPARED_UNSENT', 'developmentDirection': 'video-game-only',
        'records': records, 'currentAcceptedInterfaceComparisons': inherited, 'completeAppliedCounterparts': counterparts,
        'completeCosmologySourcesAndAuthority': lore, 'verifiedPriorPush': info(pushp),
        'pendingComparisonsNotAuthority': pending, 'acceptedIllusionContextUnapplied': illusion, 'controlReadyProposedContext': control,
        'questions': questions, 'riskCounts': risk, 'sourceFindings': findings,
        'semanticDelta': [{'spellId': r['spellId'], 'riskTier': r['riskTier'], 'riskReason': r['riskReason'],
            'startingPoint': 'Complete native source and old question; no earlier complete operational procedure or cases.',
            'genuineQuestionIds': [q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'futureCaseRequirements': cases, 'earlierOperationalWorkedCases': [], 'currentVectors': [],
        'countsUnchanged': deepcopy(index['authoredCounts']), 'sourceBindings': list(sources.values()),
        'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'humanPlaytests': 0, 'sourceInformationDeleted': 0,
        'cosmologyDecisions': 0, 'wholeGameComplete': False}
    root.mkdir(); frozen = []
    for b in sources.values():
        p = G / b['path']; ck('Current source exact ' + b['path'], info(p) == b)
        dst = root / 'sources' / b['path']; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(p.read_bytes())
        ck('Frozen complete bytes exact ' + b['path'], dst.read_bytes() == p.read_bytes())
        frozen.append({**b, 'frozenCopy': dst.relative_to(G).as_posix()})
    for p, raw in protected.items(): ck('Protected authority unchanged ' + p.name, p.read_bytes() == raw)
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate': info(out), 'checks': checks, 'checkCount': len(checks),
        'sourceCount': len(sources), 'sourceIdentities': 7, 'placements': 10, 'questions': 23,
        'riskCounts': risk, 'earlierCompleteProcedures': 0, 'earlierOperationalWorkedCases': 0,
        'newCurrentVectors': 0, 'failures': 0, 'validationScope': 'Full source/access/authority preservation only; no semantic adoption or game-engine test.'}))
    manifest = root / 'MANIFEST.json'
    manifest.write_bytes(encoded({'candidate': info(out), 'check': info(check), 'files': list(sources.values()),
        'frozenSources': frozen, 'sourceCount': len(sources), 'newRuleAdoptions': 0}))
    readme = ('Seven complete rank9 psychic/fear identities,ten native placements,23 unselected questions,seven applied counterparts and exact accepted-but-unapplied Control15/Illusion14 context. Four tierB and three tierC. Preserve all school variants,head consequences,actual fleeing,nightmare captivity and meaningful secondary effects. Full sources and original questions remain exact. No procedure,vector,index,runtime,balance or cosmology adoption.\n')
    (root / 'README.md').write_text(readme, encoding='utf8', newline='\n')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p, name in [(out, 'CANDIDATE.json'), (check, 'SOURCE_CHECK.json'), (manifest, 'MANIFEST.json')]: z.write(p, name)
        z.writestr('README.md', readme)
        for b in sources.values(): z.write(root / 'sources' / b['path'], 'sources/' + b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist())) and z.read('CANDIDATE.json') == out.read_bytes()
        for b in sources.values(): assert z.read('sources/' + b['path']) == (G / b['path']).read_bytes()
    ab = info(archive)
    request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Read all seven complete sources/ten placements,23 unselected questions,seven applied counterparts and exact accepted-but-unapplied Control15/Illusion14 context. Select explicit source-faithful decisions for enemy geometry,damage/save separation,school variants,actual head destruction,flight,nightmare captivity,recurring exposure and Reality Break secondary effects. Preserve all printed magnitudes and useful effects;no foreign spell tables or convenience reduction. Return full choices,operative procedures and qualified case obligations. Keep owner-reserved implementation,actual source ownership and all distinct validation gates. This preparation authorizes no rule/index/runtime or cosmology application.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'PREPARED_UNSENT',
        'candidate': info(out), 'archive': ab, 'manifest': info(manifest), 'check': info(check), 'request': info(request),
        'sourceCount': len(sources), 'identityCount': 7, 'placementCount': 10, 'questionCount': 23,
        'riskCounts': risk, 'allArchiveMembersVerified': True, 'newRuleAdoptions': 0, 'sourceInformationDeleted': 0}))
    print(json.dumps({'preparation': info(prep), 'candidate': info(out), 'archive': ab,
        'sources': len(sources), 'checks': len(checks), 'questions': 23, 'failures': 0}))


if __name__ == '__main__': main()
