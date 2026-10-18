"""Freeze complete native sources and unselected rank-nine storm/control questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank9_storm_control_6_questions_01 import IDS, TIERS, Q


def read(p): return json.loads(p.read_bytes())


def main():
    stem = 'RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_01'
    root = A / 'rank9-storm-control6-source-conference-01'
    out = R / 'data/director/spell_review/rank9_storm_control_6_source_conference_01.json'
    check, prep, request = [A / (stem + s) for s in ['_CHECK.json', '_PREPARATION.json', '_REQUEST.txt']]
    archive = A / 'DD_Rank9_Storm_Control_6_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources = {}; checks = []
    def ck(label, ok):
        checks.append({'check': label, 'passed': bool(ok)}); assert ok, label
    def bind(p):
        b = info(p); sources[b['path']] = b; return b
    catp = R / 'data/public/spell_playtests/catalog.json'
    ip = catp.parent / 'authored_review_index.json'
    qp = R / 'data/director/spell_review/remaining_work_queue_37.json'
    regp = R / 'data/director/spell_review/accepted_interface_registry_06.json'
    cov = R / 'data/playtest/game_development_coverage.json'
    protected = {p: p.read_bytes() for p in [catp, ip, qp, regp, cov]}
    catalog, index, queue, registry = map(read, [catp, ip, qp, regp])
    olds = [A / (s + '_RANK9_SOURCE_PREPARATION.json') for s in ['CONJURATION', 'EVOCATION', 'TRANSMUTATION_UNIVERSAL']]
    histories = [read(p) for p in olds]
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_CATASTROPHE_45.json'
    pushp = G / 'docs/audit/2026-10-18/github-snapshot-rank9-sources/PUSH_RECEIPT.json'
    push = read(pushp)
    ck('Verified post-push gate', push['commit'] == push['remoteMain'] == '372cb8a66d590811014ecbc8fc7c51ef5c67d955' and push['trackedEntriesDeleted'] == 0)
    ck('Applied index unchanged', index['authoredCounts'] == {'reviewed': 525, 'pending': 323} and index['representationCounts']['completeReviewedStandaloneProcedures'] == 249)
    ck('173 scoped interfaces', len(registry['entries']) == 173)
    for p in [catp, ip, qp, regp, cov, *olds, checkpoint, pushp, Path(__file__),
              Path(__file__).with_name('rank9_storm_control_6_questions_01.py'),
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
        ck('All school placements ' + ident, len(books) == len(card['source']['original']['placements']) == 1)
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
    for n in list(range(12)) + [13, 14, 17, 18, 19, 22, 36, 37, 39, 40] + list(range(108, 117)) + [119] + list(range(143, 152)) + [157, 158]:
        entry = registry['entries'][n]; b = entry['currentAuthoritativeSource']; actual = bind(G / b['path'])
        ck('Current exact scoped interface ' + str(n), all(actual[k] == b[k] for k in ['bytes', 'sha256']))
        inherited.append({'registryPointer': '/entries/' + str(n), 'completeEntryUnchanged': deepcopy(entry),
            'scopeLimit': 'Only the named accepted scope. New area, pull, stasis, containment, five-strike, pulse, overlap and root extensions require explicit per-spell selection.'})
    counterparts = []
    for ident in ['frozen-tomb', 'slow', 'storm-sphere', 'flame-typhoon', 'inferno-wave',
                  'wall-of-force', 'dimensional-anchor', 'rift-spiral',
                  'greater-dispel', 'antimagic-field-lesser']:
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
    for name in ['rank8-environment3', 'rank8-information-time4', 'rank9-catastrophe10']:
        group = next(g for g in queue['groups'] if g['group'] == name)
        b = bind(G / group['candidate']['path']); ck('Exact pending comparison ' + name, b == group['candidate'])
        pending.append({'group': name, 'candidate': b, 'identities': group['identities'], 'qualification': 'Pending source conference only; none of its choices are adopted authority.'})
    control = {'receipt': bind(A / 'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json'),
        'selectedSuccessor': bind(A / 'control15-full-conference-part5-return-02/successor/CONTROL15_REVIEWED_SUCCESSOR13.json'),
        'reviewReceipt': bind(A / 'control15-full-conference-part5-return-02/REVIEW_RECEIPT.json'),
        'qualification': 'Exact full semantic acceptance but unapplied. Ordinary Ready and the distinct companion phase bridges are accepted only in the exact returned Control successor. They do not automatically select new stasis/containment rules or implement full copied Ready.'}
    questions = [{'id': qid, 'spellIds': ids, 'exactSourceOrConflict': src, 'options': options,
                  'recommendationAndConsequences': recommendation, 'decisionSelected': False}
                 for qid, ids, src, options, recommendation in Q]
    ck('25 unique unselected questions', len(questions) == len({q['id'] for q in questions}) == 25 and all(not q['decisionSelected'] for q in questions))
    ck('Every identity covered', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records)); ck('Individual risks two B four C', risk == {'B': 2, 'C': 4})
    ck('Six complete identities six placements', len(records) == 6 and sum(len(r['completeCurrentBookBindings']) for r in records) == 6)
    findings = [
        'All six actual routes are rank9/minimum class level17/base26RP. Five Mage/Wizard Evocation identities remain separate from Druid/Mage/Wizard Conjuration Storm Cage. Cosmic Implosion has V/S/M/F; the other five V/S/F.',
        'Cosmic Implosion preserves ALL creatures within100feet, inward pull,15d10force and Core concentration up to one minute. A repeated15d10 event or one-shot-plus-continuation must be selected explicitly; concentration alone supplies neither.',
        'Frozen Eternity preserves a single target, time stop/no action, three rounds and WIS save ends. It is not already Paralyzed or ordinary Time Stop. Senses, movement, incoming effects and personal/external clocks need separate explicit decisions.',
        'Hellstorm preserves8d10fire per round for exactly three rounds. Over100feet is not unambiguously radius or diameter, and its100-foot casting range is a separate quantity. No concentration is printed.',
        'Storm of Vengeance requires a substantive massive multiround storm with varied damage types. Its Instantaneous metadata cannot silently erase that behavior. The complete finite schedule and dimensions are NEW authorship, not a foreign storm table.',
        'Thunder Wrath preserves five separate6d6lightning strikes per round. Storm Sphere supplies a scoped comparison, not a one-bolt restriction or free Bonus Actions. Creation, command, repeated targets, group interruptions and source clocks remain unselected.',
        'Storm Cage preserves one trapped creature,8d6perround and cannot escape. A repeat-save escape, generic restraint fallback, arbitrary size immunity or damage immunity automatically ending containment would be a substantive new choice, not native wording.',
        'Real source/recipient suppression, original deadlines, hard-control history and shared damage provenance remain distinct. Pending Time Stop/Time Echo/environment conferences are not operative authority.',
        'The owner reserved later implementation.39 exact accepted spell identities remain unapplied; source preparation changes no catalog/index/registry, cosmology or game runtime.']
    cases = [
        'After decisions, create at least two full cases per identity plus all distinct semantic branches. Use actual native route, acquired spell, owner state, components,26baseRP plus real pricing/cadence, concentration and counter history.',
        'Record full occupied3D bodies, source and recipient IDs, current visibility/line of effect/cover, selected origins, all timestamps and RNG inputs, intermediate typed arithmetic, true defense consumption, movement/control and exact ending state.',
        'Cosmic Implosion: retain caster/allies/hidden eligible bodies in the all-creatures area, anchored and unsupported recipients, occupied-center stopping, actual falling and the full selected continuing concentration benefit. No artificial physics or erased displacement.',
        'Frozen Eternity: one useful positive full temporal state, one initial-save or used-hard-control rejection, actual ending WIS saves including suppression, third-round deadline, underway/extra/attached phases and independently running or specifically paused clocks. Any deferred incoming event must execute exactly once or have a justified outcome.',
        'Hellstorm: all three printed8d10 pulses with real cover and entry/reentry, suppressed middle pulse, initiative changes and exact expiry. No fourth ending pulse or entry damage invented from proximity.',
        'Storm of Vengeance: the entire selected multistage table with at least two genuinely different damage types and a full massive volume, changing cover/recipient positions and interrupted concentration. Future stage cancellation does not erase prior material history.',
        'Thunder Wrath: five real6d6 lightning strikes in an eligible round, actual repeat-target permission, distinct attack/save and damage event arithmetic, owner control expenditure, kill/source-ending during a group, recast/extra-turn limits and no fourth group from deadline or numbering artifacts.',
        'Storm Cage: useful established confinement and repeated8d6, real attempted voluntary/forced/teleport escape under selected rules, outside assistance, actual actions retained inside, partial suppression and occupied resumption. No positive-content closure from rejection-only tests.',
        'Cross-source cases need actual qualified Null, healing, tempHP, death/form and condition defenses. Independent control and damage histories remain separate. Do not fabricate a CR, attack profile, immunity or acquired feature to close a held premise.',
        'These are future vector obligations only. The source packet contains no adopted procedure, current operational example, numerical-balance claim or engine test.']
    native_comparisons = []
    for ident in ['time-stop', 'time-echo']:
        c = next(s for s in catalog['spells'] if s['id'] == ident)
        e = next(e for e in index['entries'] if e['id'] == ident)
        ck('Pending native comparison ' + ident, e['authoredStatus'] == 'pending-authored-procedure')
        native_comparisons.append({'spellId': ident, 'completeCurrentSourceAndAccess': deepcopy(c),
            'indexEntry': deepcopy(e), 'qualification': 'Native source comparison only; no accepted procedure or permission for Frozen Eternity.'})
    candidate = {'id': 'RANK9-STORM-CONTROL6-SOURCE-CONFERENCE01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'SOURCE_CONFERENCE_PREPARED_UNSENT', 'developmentDirection': 'video-game-only',
        'records': records, 'currentAcceptedInterfaceComparisons': inherited, 'completeAppliedCounterparts': counterparts,
        'completeCosmologySourcesAndAuthority': lore, 'verifiedPriorPush': info(pushp),
        'pendingComparisonsNotAuthority': pending, 'pendingNativeComparisons': native_comparisons, 'controlReadyProposedContext': control,
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
        'sourceCount': len(sources), 'sourceIdentities': 6, 'placements': 6, 'questions': 25,
        'riskCounts': risk, 'earlierCompleteProcedures': 0, 'earlierOperationalWorkedCases': 0,
        'newCurrentVectors': 0, 'failures': 0, 'validationScope': 'Full source/access/authority preservation only; no semantic adoption or game-engine test.'}))
    manifest = root / 'MANIFEST.json'
    manifest.write_bytes(encoded({'candidate': info(out), 'check': info(check), 'files': list(sources.values()),
        'frozenSources': frozen, 'sourceCount': len(sources), 'newRuleAdoptions': 0}))
    readme = ('Six complete rank9 storm/control sources, six placements,25 unselected decisions,10 applied counterparts and exact scoped interfaces. Two individually tierB and four tierC. Preserve all-creature pull, full temporal suspension question, three fire pulses, varied multistage storm, five lightning strikes per round and real cannot-escape confinement. Resolve source duration/geometry/targeting conflicts explicitly. Full original questions, manuscripts, source history and owner cosmology context are included. No procedure, current case, runtime, balance or cosmology adoption.39 accepted spells remain unapplied; current525/323/249 stays unchanged.\n')
    (root / 'README.md').write_text(readme, encoding='utf8', newline='\n')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p, name in [(out, 'CANDIDATE.json'), (check, 'SOURCE_CHECK.json'), (manifest, 'MANIFEST.json')]: z.write(p, name)
        z.writestr('README.md', readme)
        for b in sources.values(): z.write(root / 'sources' / b['path'], 'sources/' + b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist())) and z.read('CANDIDATE.json') == out.read_bytes()
        for b in sources.values(): assert z.read('sources/' + b['path']) == (G / b['path']).read_bytes()
    ab = info(archive)
    request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Read all six complete native sources/six placements,25 unselected questions,10 applied counterparts, exact Control15 accepted-but-unapplied context and full histories. Select each local source reconciliation explicitly before operational procedure/case authorship. Preserve Cosmic Implosion all-creature pull and continuing benefit, Frozen Eternity time-stop/three-round/ending-save meaning, Hellstorm three8d10 pulses, Vengeance full varied storm schedule, Thunder Wrath five6d6lightning strikes per round and Storm Cage actual cannot-escape containment. NEW proposals in the question set are discussion candidates, not adopted rules or balanced values. No silent foreign mechanics, convenience scope reduction or global interface extension. The verified prior push allows careful context review but supplies no new canon. Return complete choices, operative text and source-qualified future vectors; keep implementation reservation and all actual content holds. No rule/index/runtime application is authorized by this source preparation.\n', encoding='utf8', newline='\n')
    prep.write_bytes(encoded({'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'PREPARED_UNSENT',
        'candidate': info(out), 'archive': ab, 'manifest': info(manifest), 'check': info(check), 'request': info(request),
        'sourceCount': len(sources), 'identityCount': 6, 'placementCount': 6, 'questionCount': 25,
        'riskCounts': risk, 'allArchiveMembersVerified': True, 'newRuleAdoptions': 0, 'sourceInformationDeleted': 0}))
    print(json.dumps({'preparation': info(prep), 'candidate': info(out), 'archive': ab,
        'sources': len(sources), 'checks': len(checks), 'questions': 25, 'failures': 0}))


if __name__ == '__main__': main()
