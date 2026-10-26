"""Freeze complete native sources and unselected rank-nine catastrophe questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank9_catastrophe_10_questions_01 import IDS, TIERS, Q


def read(p): return json.loads(p.read_bytes())


def main():
    stem = 'RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_01'
    root = A / 'rank9-catastrophe10-source-conference-01'
    out = R / 'data/director/spell_review/rank9_catastrophe_10_source_conference_01.json'
    check, prep, request = [A / (stem + s) for s in ['_CHECK.json', '_PREPARATION.json', '_REQUEST.txt']]
    archive = A / 'DD_Rank9_Catastrophe_10_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources = {}; checks = []
    def ck(label, ok):
        checks.append({'check': label, 'passed': bool(ok)}); assert ok, label
    def bind(p):
        b = info(p); sources[b['path']] = b; return b
    catp = R / 'data/public/spell_playtests/catalog.json'
    ip = catp.parent / 'authored_review_index.json'
    qp = R / 'data/director/spell_review/remaining_work_queue_36.json'
    regp = R / 'data/director/spell_review/accepted_interface_registry_06.json'
    cov = R / 'data/playtest/game_development_coverage.json'
    protected = {p: p.read_bytes() for p in [catp, ip, qp, regp, cov]}
    catalog, index, queue, registry = map(read, [catp, ip, qp, regp])
    olds = [A / (s + '_RANK9_SOURCE_PREPARATION.json') for s in ['CONJURATION', 'EVOCATION', 'TRANSMUTATION_UNIVERSAL']]
    histories = [read(p) for p in olds]
    checkpoint = A / 'ACTIVE_AUTHORING_CHECKPOINT_COPIED_FEAT_DIAGNOSTICS_44.json'
    pushp = G / 'docs/audit/2026-10-18/github-snapshot-control15-final/PUSH_RECEIPT.json'
    push = read(pushp)
    ck('Verified post-push gate', push['commit'] == push['remoteMain'] == '1eb1a83f6b86934e5a97770f1d10c240c0f23216' and push['trackedEntriesDeleted'] == 0)
    ck('Applied index unchanged', index['authoredCounts'] == {'reviewed': 525, 'pending': 323} and index['representationCounts']['completeReviewedStandaloneProcedures'] == 249)
    ck('173 scoped interfaces', len(registry['entries']) == 173)
    for p in [catp, ip, qp, regp, cov, *olds, checkpoint, pushp, Path(__file__),
              Path(__file__).with_name('rank9_catastrophe_10_questions_01.py'),
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
        ck('All school placements ' + ident, len(books) == len(card['source']['original']['placements']) == (3 if ident == 'meteor-swarm' else 1))
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
    for n in list(range(12)) + [13, 14, 36, 39, 40, 64] + list(range(108, 117)) + [142] + list(range(143, 152)) + [172]:
        entry = registry['entries'][n]; b = entry['currentAuthoritativeSource']; actual = bind(G / b['path'])
        ck('Current exact scoped interface ' + str(n), all(actual[k] == b[k] for k in ['bytes', 'sha256']))
        inherited.append({'registryPointer': '/entries/' + str(n), 'completeEntryUnchanged': deepcopy(entry),
            'scopeLimit': 'Only the named accepted scope. New area, mixed-defense, overlap, material destruction, sacrifice or persistent-event extensions require explicit per-spell selection.'})
    counterparts = []
    for ident in ['meteor-spear', 'ice-storm', 'elemental-devastation', 'destructive-wave',
                  'supernova-lance', 'sunburst', 'rift-spiral', 'arcane-mortar', 'death-ward',
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
        lore.append({'source': bind(G / name), 'scope': 'Full original source; later explicit owner corrections take precedence only where stated. No new plane identity, disaster canon or Hunt exception is inferred.'})
    for name in ['CURRENT_COSMOLOGY_READ_FIRST.md', 'PLANES_REVIEWED_01.md', 'OWNER_RECONCILIATION_REVIEWED_01.md',
                 'HEARTCELL_OWNER_UPDATE_02.md', 'SOULS_RESEARCH_REVIEWED_01.md', 'EPILOGUE_RELIC_NULL_REVIEWED_01.md']:
        lore.append({'source': bind(R / 'docs/director-only/cosmology' / name), 'scope': 'Current bounded owner reconciliation or operational companion; historical pending workflow labels do not supersede actual later application records.'})
    for name in ['planes_reviewed_01.json', 'owner_reconciliation_reviewed_01.json', 'heartcell_owner_update_02.json',
                 'souls_research_reviewed_01.json', 'epilogue_relic_null_reviewed_01.json']:
        bind(R / 'data/director/cosmology' / name)
    pending = []
    for name in ['rank8-damage6', 'rank8-environment3', 'rank8-summon-structure5', 'rank8-planar5']:
        group = next(g for g in queue['groups'] if g['group'] == name)
        b = bind(G / group['candidate']['path']); ck('Exact pending comparison ' + name, b == group['candidate'])
        pending.append({'group': name, 'candidate': b, 'identities': group['identities'], 'qualification': 'Pending source conference only; none of its choices are adopted authority.'})
    control = {'receipt': bind(A / 'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json'),
        'selectedSuccessor': bind(A / 'control15-full-conference-part5-return-02/successor/CONTROL15_REVIEWED_SUCCESSOR13.json'),
        'reviewReceipt': bind(A / 'control15-full-conference-part5-return-02/REVIEW_RECEIPT.json'),
        'qualification': 'Exact full semantic acceptance but unapplied. Ordinary Ready target timing does not settle Final Spark’s sacrifice timing or implement full copied Ready.'}
    questions = [{'id': qid, 'spellIds': ids, 'exactSourceOrConflict': src, 'options': options,
                  'recommendationAndConsequences': recommendation, 'decisionSelected': False}
                 for qid, ids, src, options, recommendation in Q]
    ck('25 unique unselected questions', len(questions) == len({q['id'] for q in questions}) == 25 and all(not q['decisionSelected'] for q in questions))
    ck('Every identity covered', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records)); ck('Individual risks three B seven C', risk == {'B': 3, 'C': 7})
    ck('Ten complete identities twelve placements', len(records) == 10 and sum(len(r['completeCurrentBookBindings']) for r in records) == 12)
    findings = [
        'All ten actual class routes are rank9, minimum class level17, base26RP; full actual class-specific access is retained. Standard Core Action and V/S/F are source metadata, not free repertoire or a complete payload procedure.',
        'Elemental Apocalypse is NOT simply an instantaneous blast: its Core concentration duration must be reconciled with a substantive event profile. Starfire Core’s Until dispelled versus permanent terrain clause is likewise unresolved.',
        'Meteor Swarm retains three school placements, four spheres, the explicit10d6+10d6 wording, ambiguous20d6 combined wording and20/120-foot range conflict. The20-foot sphere size still needs radius/diameter interpretation.',
        'Cataclysm retains its entire one-mile radius and120-foot source placement range. The separate Oracle Cataclysm Mystery grants no ordinary spell access or substitute procedure.',
        'Arcane Apocalypse structural obliteration and Starfire Core permanent scorching require actual positive world outcomes. Missing material adapters are content/implementation holds, not license to delete those benefits.',
        'Final Spark’s self-sacrifice is distinct from damage. Existing Null does not convert sacrificial costs; exact timing, survival interactions and what unavoidable bypasses remain explicit new choices.',
        'Planar Overload’s historical post-push receipt is preserved. The required backup now exists and is verified; this allows careful source review, not automatic cosmology approval or invented rift traversal.',
        'The owner reserved later implementation. Copied-feat review remains active;39 accepted spell identities stay unapplied. No current rule or index changes follow from this source packet.']
    cases = [
        'After choices, create at least two complete current cases per identity plus every distinct new branch, with actual native class access, acquired repertoire, level, ability/PB, components, price/cadence and concentration/counter history.',
        'Keep actual 3D occupied bodies, line-of-effect/cover, initial target snapshots, clocks, RNG operands, typed intermediate arithmetic, genuine source IDs, per-recipient events and exact final state. Include real Null and mitigation sources, not invented blanket defenses.',
        'Cataclysmic/Elemental/Planar: actual selected types, allies versus enemy selection, whole area geometry, missing-versus-present elemental substrate, selected duration and genuine endings; rift comparison cannot create a transport feature without its selected full procedure.',
        'Armageddon/Cataclysm: full300-foot and5,280-foot radius cases spanning genuine cover and distant actors. Software handles the entire scope; no offscreen omission. Distinguish independently admitted structures, terrain and later collapse.',
        'Arcane Apocalypse: one substantive eligible structural obliteration and one partial-boundary/protected-material case, with occupants, contents, support, debris, retained mass and exact subsequent falling. Rejection-only coverage is insufficient.',
        'Meteor Swarm: four actual impacts, at least one overlapping multi-sphere body, accepted typed arithmetic, range route reconciliation, declared centers and cover changing during the resolution; preserve the chosen overlap/event policy exactly.',
        'Starfire: a real full burst and persistent terrain consequence, then suppression/dispel/recast with retained physical history. Prove a useful positive terrain effect without restoring destroyed objects or spawning free material.',
        'Ragnarok: actual allies/caster/foes and vision/range predicates, complete random-type draws and all25dice, deterministic ordering, mixed defenses and recipient death/body replacement. Show repeated execution does not secretly reroll a favorable type.',
        'Final Spark: actual sacrifice with real preexisting life/form/survival state and200damage, counter/Ready/expiry branches, original-root Null behavior, actual death history and no duplicate reward or unearned resurrection. Sacrifice and damage are separate auditable events.',
        'These future vectors are obligations, not existing tests. Preserve every old source question/case; no new deterministic outcome is asserted before its open choice is selected.']
    candidate = {'id': 'RANK9-CATASTROPHE10-SOURCE-CONFERENCE01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'SOURCE_CONFERENCE_PREPARED_UNSENT', 'developmentDirection': 'video-game-only',
        'records': records, 'currentAcceptedInterfaceComparisons': inherited, 'completeAppliedCounterparts': counterparts,
        'completeCosmologySourcesAndAuthority': lore, 'verifiedPriorPush': info(pushp),
        'pendingComparisonsNotAuthority': pending, 'controlReadyProposedContext': control,
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
        'sourceCount': len(sources), 'sourceIdentities': 10, 'placements': 12, 'questions': 25,
        'riskCounts': risk, 'earlierCompleteProcedures': 0, 'earlierOperationalWorkedCases': 0,
        'newCurrentVectors': 0, 'failures': 0, 'validationScope': 'Full source/access/authority preservation only; no semantic adoption or game-engine test.'}))
    manifest = root / 'MANIFEST.json'
    manifest.write_bytes(encoded({'candidate': info(out), 'check': info(check), 'files': list(sources.values()),
        'frozenSources': frozen, 'sourceCount': len(sources), 'newRuleAdoptions': 0}))
    readme = ('Ten complete rank9 catastrophe sources, twelve placements,25 unselected decisions,11 applied counterparts and exact scoped interfaces. Three individually tierB and seven tierC. Preserve full magnitude, mile-scale areas, four meteors, structural obliteration, permanent scorching, random plural types and actual sacrifice. Resolve concentration/duration/range/source conflicts explicitly. Full native histories, manuscripts, original cosmology and owner updates are included. No procedure, current case, runtime, balance or cosmology adoption.39 accepted spells remain unapplied; current525/323/249 stays unchanged.\n')
    (root / 'README.md').write_text(readme, encoding='utf8', newline='\n')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p, name in [(out, 'CANDIDATE.json'), (check, 'SOURCE_CHECK.json'), (manifest, 'MANIFEST.json')]: z.write(p, name)
        z.writestr('README.md', readme)
        for b in sources.values(): z.write(root / 'sources' / b['path'], 'sources/' + b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist())) and z.read('CANDIDATE.json') == out.read_bytes()
        for b in sources.values(): assert z.read('sources/' + b['path']) == (G / b['path']).read_bytes()
    ab = info(archive)
    request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Read all ten complete native sources/twelve placements,25 unselected questions,11 applied counterparts and full source histories. Return source-faithful per-question choices and complete future-case obligations, preserving all printed magnitude and meaningful effects. Explicitly settle Elemental Apocalypse concentration, Meteor Swarm range/size/typing/overlap, Arcane Apocalypse structural obliteration, Starfire permanent terrain versus dispel, Ragnarok visible-all/random-types and Final Spark sacrifice/unavoidable defenses. No convenience scope reduction or silent global interface extension. The verified prior push permits careful planar-source review but supplies no new canon. No rule/index/runtime application is authorized by this preparation.\n', encoding='utf8', newline='\n')
    prep.write_bytes(encoded({'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'PREPARED_UNSENT',
        'candidate': info(out), 'archive': ab, 'manifest': info(manifest), 'check': info(check), 'request': info(request),
        'sourceCount': len(sources), 'identityCount': 10, 'placementCount': 12, 'questionCount': 25,
        'riskCounts': risk, 'allArchiveMembersVerified': True, 'newRuleAdoptions': 0, 'sourceInformationDeleted': 0}))
    print(json.dumps({'preparation': info(prep), 'candidate': info(out), 'archive': ab,
        'sources': len(sources), 'checks': len(checks), 'questions': 25, 'failures': 0}))


if __name__ == '__main__': main()
