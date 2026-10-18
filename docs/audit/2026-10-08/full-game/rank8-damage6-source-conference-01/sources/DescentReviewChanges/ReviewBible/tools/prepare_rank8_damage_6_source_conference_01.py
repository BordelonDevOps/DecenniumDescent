"""Preserve six complete native rank-eight sources and unselected decisions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank8_damage_6_questions_01 import IDS, ORIGINALS, TIERS, Q


def read(p): return json.loads(p.read_bytes())


def main():
    root = A/'rank8-damage6-source-conference-01'
    out = R/'data/director/spell_review/rank8_damage_6_source_conference_01.json'
    check = A/'RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_CHECK.json'
    prep = A/'RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_PREPARATION.json'
    request = A/'RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_REQUEST.txt'
    archive = A/'DD_Rank8_Damage_6_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources = {}; checks = []
    def ck(n, v): checks.append({'check': n, 'passed': bool(v)}); assert v, n
    def bind(p):
        b = info(p); sources[b['path']] = b; return b
    cp = R/'data/public/spell_playtests/catalog.json'; ip = cp.parent/'authored_review_index.json'
    qp = R/'data/director/spell_review/remaining_work_queue_17.json'
    rp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    catalog, index, queue, registry = map(read, [cp, ip, qp, rp])
    ck('525 reviewed323 pending', index['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    ck('173 existing exact interfaces', len(registry['entries']) == 173)
    for p in [cp, ip, qp, rp, Path(__file__), Path(__file__).with_name('rank8_damage_6_questions_01.py'),
              R/'rulebook_output.txt', G/'docs/reference/Player_Rulebook_v6_source_text.txt',
              A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_CLASSES_24.json',
              G/'docs/audit/2026-10-18/github-snapshot-copy-integration/PUSH_RECEIPT.json']: bind(p)
    lines = (R/'rulebook_output.txt').read_text('utf-16').splitlines()
    reference_lines = (G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf8').splitlines()
    records = []
    for ident in IDS:
        oldp = A/ORIGINALS[ident]; old = read(oldp); bind(oldp)
        n = next(n for n, s in enumerate(old['selectedSpells']) if s['spellId'] == ident); historical = old['selectedSpells'][n]
        card = next(s for s in catalog['spells'] if s['id'] == ident)
        row = next(s for s in queue['rows'] if s['id'] == ident)
        entry = next(e for e in index['entries'] if e['id'] == ident)
        ck('Complete original/current/queue equality '+ident, historical['fullSourceAndCurrentAccessRecord'] == card == row['completeCurrentSourceAndAccess'])
        ck('No earlier complete procedure '+ident, row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Pending exact identity '+ident, entry['authoredStatus'] == 'pending-authored-procedure')
        ck('Real rank8 price/access '+ident, all(v['rank'] == 8 and v['baseRpCost'] == 21 and v['minimumClassLevel'] == 15 for v in card['classAccess'].values()))
        bb = [deepcopy(b) for b in old['currentBookBindings'] if b['spellId'] == ident]
        ck('All native school placements '+ident, len(bb) == len(card['source']['original']['placements']))
        for b in bb:
            k = b['currentBookRow']['line']-1
            ck('Current exact book line '+ident, lines[k] == b['currentBookRow']['exactText'])
            ck('Preserved reference book line '+ident, reference_lines[k] == lines[k])
        for key in ['catalog', 'core']:
            ck('Full underlying source hash '+ident+key, bind(R/card['source'][key+'Path'])['sha256'] == card['source'][key+'Sha256'])
        for cls in card['classAccess']: bind(R/('data/public/class_playtests/'+cls.lower()+'.json'))
        records.append({'spellId': ident, 'riskTier': TIERS[ident][0], 'riskReason': TIERS[ident][1],
            'completeCurrentCatalogSourceAndAccess': deepcopy(card), 'currentIndexEntry': deepcopy(entry),
            'originalQuestionSource': info(oldp), 'originalQuestionPointer': '/selectedSpells/'+str(n),
            'completeOriginalSourceQuestionUnchanged': deepcopy(historical),
            'completeHistoricalCommonQuestionUnchanged': old['commonOperationalQuestion'],
            'completeHistoricalScopeExceptionUnchanged': old['commonQuestionException'],
            'completeCurrentBookBindings': bb, 'earlierCompleteProcedures': [], 'earlierOperationalWorkedCases': [],
            'status': 'Source conference prepared UNSENT; no operational procedure/case adoption.'})
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md', 'CLASS_PLAYTEST_RULES.md', 'SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md',
                 'HEALING_DEATH_PLAYTEST.md', 'DAMAGE_SHARING_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md',
                 'CRAFTING_HARVEST_PLAYTEST.md', 'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    inherited = []
    selected = list(range(0, 12))+[13, 18, 22, 36, 39, 40]+list(range(43, 49))+list(range(108, 117))+[142]+list(range(143, 152))+[172]
    for n in selected:
        e = registry['entries'][n]; b = e['currentAuthoritativeSource']; actual = bind(G/b['path'])
        ck('Current interface hash '+str(n), all(actual[k] == b[k] for k in ['bytes', 'sha256']))
        inherited.append({'registryPointer': '/entries/'+str(n), 'completeEntryUnchanged': deepcopy(e),
            'scopeLimit': 'Exact named accepted scope only. The new spell must expressly adopt any source-limited extension. Meteor/Ice Storm mixed-defense keys, Banishment cell/admission/closure, illusion predicates and Persistent20 exposures do not transfer silently.'})
    counterparts = []
    for ident in ['meteor-spear', 'ice-storm', 'vitriolic-sphere', 'rift-spiral', 'banishment',
                  'destructive-wave', 'invisible-tide', 'phantom-swarm', 'animate-dead',
                  'dimensional-anchor', 'greater-dispel', 'antimagic-field-lesser']:
        e = next(e for e in index['entries'] if e['id'] == ident)
        ck('Actually reviewed counterpart '+ident, e['authoredStatus'] == 'reviewed-authored-operational-playtest')
        path = (ip.parent/e['procedureFile']).resolve(); doc = read(path); ptr = e.get('wholeCardPointer', e['procedurePointer'])
        binding = bind(path)
        if e.get('completeEnvelopeBinding'): ck('Whole accepted envelope '+ident, binding == e['completeEnvelopeBinding'])
        if e.get('authoredAcceptanceReceipt'):
            b = e['authoredAcceptanceReceipt']; ck('Exact authored receipt '+ident, bind(G/b['path']) == b)
        for source in e.get('caseSourceReferenceAliases', {}).values(): bind(G/source)
        counterparts.append({'spellId': ident, 'source': binding, 'pointer': ptr,
            'completeCurrentCard': deepcopy(at(doc, ptr)), 'completeSharedRules': deepcopy(doc.get('sharedRules', {})),
            'indexEntry': deepcopy(e), 'qualification': 'Current acceptance receipt/index controls preserved historical candidate labels. This comparison grants no new source scope.'})
    questions = [{'id': i, 'spellIds': ids, 'exactSourceOrConflict': src, 'options': options,
                  'recommendationAndConsequences': rec, 'decisionSelected': False} for i, ids, src, options, rec in Q]
    ck('20 distinct unselected questions', len(questions) == len({q['id'] for q in questions}) == 20)
    ck('Every identity has exact questions', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records)); ck('FourB twoC actual risk', risk == {'B': 4, 'C': 2})
    ck('Six identities and placements', len(records) == 6 and sum(len(r['completeCurrentBookBindings']) for r in records) == 6)
    candidate = {'id': 'RANK8-DAMAGE-6-SOURCE-CONFERENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'SOURCE_CONFERENCE_PREPARED_UNSENT', 'developmentDirection': 'video-game-only',
        'records': records, 'currentAcceptedInterfaceComparisons': inherited, 'completeAcceptedCounterparts': counterparts,
        'questions': questions, 'riskCounts': risk,
        'semanticDelta': [{'spellId': r['spellId'], 'riskTier': r['riskTier'], 'riskReason': r['riskReason'],
            'startingPoint': 'Full original source and preserved old questions; no earlier complete procedure or operational case.',
            'genuineQuestionIds': [q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'pendingComparisonsNotAuthority': ['Illusion14 has no final acceptance; its proposed perception/completion choices are not imported.',
            'Disintegrate is pending in body-defense8; molecular damage receives no implicit disintegration rider.',
            'CompanionLife10 Exact05 is pending. Existing accepted body identity/consumption interfaces do not approve its proposed new companion profiles.',
            'Part4 reached its conversation-length limit. Part5 creation authorization remains pending; this packet has not been transmitted.'],
        'earlierOperationalWorkedCases': [], 'currentVectors': [],
        'futureCaseRequirements': [
            'After exact decisions, author at least two complete actual cases per spell and every distinct new branch. Do not invent outcomes for unanswered questions.',
            'Supply real class/level/native repertoire/ability, exact actual RP adjustments/components/cadence/concentration and counter timing; zero cost or generic provider fixtures are not actual source execution.',
            'Deep Crust: actual ground/air/body geometry and blocked path; chosen mixed/selected types with exact odd save rounding, strongest real reduction stages and typed immunity/transfer.',
            'Molecular: living versus independently admitted finite/form body; actual0HP/Wound/death-replacement and gear/remains preserved without a free disintegration rider.',
            'Soul Pyre: genuine original corpse with complete prior consumption/resurrection history; competing same-body claims, counter/late failure and exact residual matter/gear lineage; both types with one aggregate event.',
            'Cloud: actual creation and later timing, exposed large body, allies/caster, repeated entry, real companion attached phase, overlap across owners, suppression/resumption/deadline and initiative transition.',
            'Dimensional Break: independent damage/exile outcomes, real enemy admission/save/control ledger, blocker known before payment versus late, current body/custody, mandatory ending and occupied return space.',
            'Illusory Wall: chosen perceptual model, actual blindness/true perception/whole-effect immunity versus psychic/Prone immunity, one admitted collapse or exact recurring rule, standing/reentry and real supported flight.',
            'Use exact RNG operands and intermediate/final state records. Accepted counterpart worked cases remain intact; conditional new cases do not establish runtime, balance, gameplay or cosmology.'],
        'countsUnchanged': deepcopy(index['authoredCounts']), 'sourceBindings': list(sources.values()),
        'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'humanPlaytests': 0, 'sourceInformationDeleted': 0,
        'cosmologyDecisions': 0, 'wholeGameComplete': False}
    root.mkdir(); frozen = []
    for b in sources.values():
        p = G/b['path']; ck('Current source unchanged '+b['path'], info(p) == b)
        dst = root/'sources'/b['path']; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(p.read_bytes())
        ck('Frozen exact bytes '+b['path'], dst.read_bytes() == p.read_bytes())
        frozen.append({**b, 'frozenCopy': dst.relative_to(G).as_posix()})
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate': info(out), 'checks': checks, 'checkCount': len(checks), 'sourceCount': len(sources),
        'sourceIdentities': 6, 'placements': 6, 'earlierCompleteProcedures': 0, 'earlierOperationalWorkedCases': 0,
        'newCurrentVectors': 0, 'questions': 20, 'riskCounts': risk, 'failures': 0,
        'validationScope': 'Exact source, metadata/access/authority comparison and preservation only; no semantic approval or gameplay execution.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate': info(out), 'check': info(check), 'files': list(sources.values()),
        'frozenSources': frozen, 'sourceCount': len(sources), 'newRuleAdoptions': 0}))
    (root/'README.md').write_text('# Six rank-eight damage and interaction spells\n\nRead all six full sources, six book placements,20 unselected source questions,12 accepted counterpart cards and exact scoped interfaces. Four tierB/two tierC records; no earlier complete procedures or cases exist. Complete source files and accepted counterpart casebooks are included. Preserved historical candidate labels are governed by actual acceptance receipts.\n\nReturn source-faithful proposed procedures, every question disposition and genuine content holds. Keep printed magnitude/benefits and native class access. Resolve radius/range, duration, mixed damage, actual corpse consumption, temporary exile and illusion admission explicitly. Label all new decisions; do not infer a global extension of a named source-specific interface. Develop actual current cases after choices are settled.525reviewed/323pending remain unchanged. No source deletion, runtime/human/balance/cosmology or75-domain closure.\n', encoding='utf8', newline='\n')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in ['README.md', 'MANIFEST.json']: z.write(root/name, name)
        z.write(out, 'CANDIDATE.json'); z.write(check, 'PREFLIGHT.json')
        for b in frozen: z.write(G/b['frozenCopy'], 'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json') == out.read_bytes()
        for b in frozen: assert z.read('sources/'+b['path']) == (G/b['frozenCopy']).read_bytes()
    b = info(archive)
    request.write_text(f'Please conduct the six-spell rank8 damage/interaction source conference using {archive.name}, {b["bytes"]}bytes SHA256{b["sha256"]}. Read all six complete original/current sources,20 explicit unselected questions,12 accepted counterpart cards, full counterpart casebooks and scoped interfaces. Four tierB/two tierC. Return complete proposed procedures and every question disposition, preserving all original benefits and actual access. Mixed-defense, Banishment cell/closure and illusion perception rules need explicit new scope; pending Illusion14/Disintegrate/Companion05 are not authority. Incendiary Cloud repeats10d8per round despite Instantaneous metadata; resolve that conflict openly. No cases or rules have been adopted.525/323membership stays unchanged.\n', encoding='utf8', newline='\n')
    prep.write_bytes(encoded({'archive': b, 'candidate': info(out), 'manifest': info(root/'MANIFEST.json'),
        'check': info(check), 'request': info(request), 'sourceCount': len(sources), 'allArchiveSourcesVerified': True,
        'riskCounts': risk, 'status': 'Prepared UNSENT; no actual GPT decision on this packet.', 'newRuleAdoptions': 0}))
    print(json.dumps({'archive': b, 'candidate': info(out), 'sources': len(sources), 'checks': len(checks), 'questions': 20, 'riskCounts': risk, 'operationalCases': 0}))


if __name__ == '__main__': main()
