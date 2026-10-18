"""Freeze complete rank-seven sources and unselected perception/control questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank7_perception_5_questions_01 import IDS, ORIGINALS, TIERS, Q


def read(p): return json.loads(p.read_bytes())


def main():
    stem = 'RANK7_PERCEPTION_5_SOURCE_CONFERENCE_01'
    root = A/'rank7-perception5-source-conference-01'
    out = R/'data/director/spell_review/rank7_perception_5_source_conference_01.json'
    check, prep, request = [A/(stem+s) for s in ['_CHECK.json', '_PREPARATION.json', '_REQUEST.txt']]
    archive = A/'DD_Rank7_Perception_5_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources = {}; checks = []
    def ck(n, v): checks.append({'check': n, 'passed': bool(v)}); assert v, n
    def bind(p):
        b = info(p); sources[b['path']] = b; return b
    cp = R/'data/public/spell_playtests/catalog.json'; ip = cp.parent/'authored_review_index.json'
    qp = R/'data/director/spell_review/remaining_work_queue_19.json'
    rp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    catalog, index, queue, registry = map(read, [cp, ip, qp, rp])
    ck('Current membership525/323', index['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    ck('173 exact scoped interfaces', len(registry['entries']) == 173)
    for p in [cp, ip, qp, rp, Path(__file__), Path(__file__).with_name('rank7_perception_5_questions_01.py'),
              R/'rulebook_output.txt', G/'docs/reference/Player_Rulebook_v6_source_text.txt',
              A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_IDENTITY_CASTING_26.json',
              G/'docs/audit/2026-10-18/github-snapshot-classes-rank8/PUSH_RECEIPT.json']: bind(p)
    lines = (R/'rulebook_output.txt').read_text('utf-16').splitlines()
    reference_lines = (G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf8').splitlines()
    records = []
    for ident in IDS:
        oldp = A/ORIGINALS[ident]; old = read(oldp); bind(oldp)
        n = next(n for n, s in enumerate(old['selectedSpells']) if s['spellId'] == ident)
        historical = old['selectedSpells'][n]; card = next(s for s in catalog['spells'] if s['id'] == ident)
        row = next(s for s in queue['rows'] if s['id'] == ident); entry = next(e for e in index['entries'] if e['id'] == ident)
        ck('Original/current/queue source equality '+ident, historical['fullSourceAndCurrentAccessRecord'] == card == row['completeCurrentSourceAndAccess'])
        ck('No earlier complete procedure '+ident, row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Exact pending identity '+ident, entry['authoredStatus'] == 'pending-authored-procedure')
        ck('All real native routes '+ident, set(card['classAccess']) == {'Bard', 'Mirrorsage', 'Wizard'})
        ck('Real native rank7 prices and levels '+ident, all(v['rank'] == 7 and v['baseRpCost'] == 17 and v['minimumClassLevel'] == (19 if k in ['Bard', 'Mirrorsage'] else 13) for k, v in card['classAccess'].items()))
        bb = [deepcopy(b) for b in old['currentBookBindings'] if b['spellId'] == ident]
        ck('Every original placement '+ident, len(bb) == len(card['source']['original']['placements']))
        for b in bb:
            k = b['currentBookRow']['line']-1
            ck('Exact current book line '+ident+str(k), lines[k] == b['currentBookRow']['exactText'])
            ck('Exact preserved reference line '+ident+str(k), reference_lines[k] == lines[k])
        for key in ['catalog', 'core']:
            ck('Underlying source hash '+ident+key, bind(R/card['source'][key+'Path'])['sha256'] == card['source'][key+'Sha256'])
        for cls in card['classAccess']:
            bind(R/('data/public/Decennium_Descent_Bard_Playtest_v0_1.json' if cls == 'Bard' else 'data/public/class_playtests/'+cls.lower()+'.json'))
        records.append({'spellId': ident, 'riskTier': TIERS[ident][0], 'riskReason': TIERS[ident][1],
            'completeCurrentCatalogSourceAndAccess': deepcopy(card), 'currentIndexEntry': deepcopy(entry),
            'originalQuestionSource': info(oldp), 'originalQuestionPointer': '/selectedSpells/'+str(n),
            'completeOriginalSourceQuestionUnchanged': deepcopy(historical),
            'completeHistoricalCommonQuestionUnchanged': old['commonOperationalQuestion'],
            'completeHistoricalScopeExceptionUnchanged': old['commonQuestionException'],
            'completeCurrentBookBindings': bb, 'earlierCompleteProcedures': [], 'earlierOperationalWorkedCases': [],
            'status': 'Prepared UNSENT; no operational procedure/case adoption.'})
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md', 'CLASS_PLAYTEST_RULES.md', 'SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md',
                 'HEALING_DEATH_PLAYTEST.md', 'DAMAGE_SHARING_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md',
                 'CRAFTING_HARVEST_PLAYTEST.md', 'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    inherited = []
    selected = list(range(0, 20))+[36, 39, 40]+list(range(78, 93))+list(range(108, 117))+[145, 149, 150, 151]
    for n in selected:
        e = registry['entries'][n]; b = e['currentAuthoritativeSource']; actual = bind(G/b['path'])
        ck('Exact current interface '+str(n), all(actual[k] == b[k] for k in ['bytes', 'sha256']))
        inherited.append({'registryPointer': '/entries/'+str(n), 'completeEntryUnchanged': deepcopy(e),
            'scopeLimit': 'Retain exact named scope. Extending a source-limited price, clock, body, companion, RNG or copying rule needs explicit new concurrence; no global extension is inferred.'})
    counterparts = []
    names = ['confusion', 'dominate-person', 'compulsion', 'phantasmal-killer', 'invisible-tide', 'major-image',
             'minor-illusion', 'silent-image', 'disguise-self', 'invisibility', 'mirror-image', 'greater-dispel', 'antimagic-field-lesser']
    for ident in names:
        e = next(e for e in index['entries'] if e['id'] == ident)
        ck('Reviewed counterpart '+ident, e['authoredStatus'] == 'reviewed-authored-operational-playtest')
        path = (ip.parent/e['procedureFile']).resolve(); doc = read(path); ptr = e.get('wholeCardPointer', e['procedurePointer'])
        binding = bind(path)
        if e.get('completeEnvelopeBinding'): ck('Whole accepted envelope '+ident, binding == e['completeEnvelopeBinding'])
        if e.get('authoredAcceptanceReceipt'):
            b = e['authoredAcceptanceReceipt']; ck('Exact authored receipt '+ident, bind(G/b['path']) == b)
        for source in e.get('caseSourceReferenceAliases', {}).values(): bind(G/source)
        shared = at(doc, e['sharedRulesPointer']) if e.get('sharedRulesPointer') else doc.get('sharedRules', {})
        card = at(doc, ptr)
        for key in ['sourceReview', 'reviewEvidence']:
            if isinstance(card.get('operational', {}).get(key), list):
                for name in card['operational'][key]: bind(G/name)
        counterparts.append({'spellId': ident, 'source': binding, 'pointer': ptr,
            'completeCurrentCard': deepcopy(card), 'completeSharedRules': deepcopy(shared), 'indexEntry': deepcopy(e),
            'qualification': 'Actual current index/acceptance governs preserved older candidate labels. Comparison does not extend eligibility to any new spell.'})
    # Reviewed counterparts retain full cards/shared rules and actual receipt/case aliases.
    bind(A/'LOW_RANK_136_EXACT_FULFILLMENT.json')
    pending = []
    for groupname in ['illusion-perception14', 'control15', 'material-terrain8', 'rank7-mechanics16']:
        g = next(g for g in queue['groups'] if g['group'] == groupname); b = g['candidate']
        ck('Exact pending comparison '+groupname, bind(G/b['path']) == b)
        pending.append({'group': groupname, 'candidate': deepcopy(b), 'identities': deepcopy(g['identities']),
            'scope': 'Full source/proposal/question file included for reconciliation only; unadopted proposals are not accepted authority.'})
    questions = [{'id': i, 'spellIds': ids, 'exactSourceOrConflict': src, 'options': options,
                  'recommendationAndConsequences': rec, 'decisionSelected': False} for i, ids, src, options, rec in Q]
    ck('21 distinct unselected questions', len(questions) == len({q['id'] for q in questions}) == 21 and not any(q['decisionSelected'] for q in questions))
    ck('All five identities questioned', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records)); ck('TwoB threeC individually justified', risk == {'B': 2, 'C': 3})
    placements = sum(len(r['completeCurrentBookBindings']) for r in records)
    ck('Five identities five native placements', len(records) == 5 and placements == 5)
    candidate = {'id': 'RANK7-PERCEPTION-5-SOURCE-CONFERENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'SOURCE_CONFERENCE_PREPARED_UNSENT', 'developmentDirection': 'video-game-only',
        'records': records, 'currentAcceptedInterfaceComparisons': inherited, 'completeAcceptedCounterparts': counterparts,
        'pendingComparisonSources': pending,
        'questions': questions, 'riskCounts': risk,
        'semanticDelta': [{'spellId': r['spellId'], 'riskTier': r['riskTier'], 'riskReason': r['riskReason'],
            'startingPoint': 'Full original source and old questions; no earlier complete procedure or operational case.',
            'genuineQuestionIds': [q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'importantScopeBoundaries': [
            'Reviewed Phantasmal Killer uses a private mental nightmare; Invisible Tide separately applies a nonvisual balance disruption. Neither creates a universal illusion-admission rule.',
            'Reviewed Minor/Major/Silent Image and Mirror Image have their own sensory, movement, decoy and interaction scopes. Mirage Arcane retains tactile sensation; Mirage Legion retains six apparent harmless casters.',
            'Perfect Veil promises complete unnoticeability unless interaction; a Stealth bonus or ordinary Invisibility is not a complete substitution. Body, memory and mechanical targeting must be separately resolved.',
            'Mindtrap repetition does not itself print free resources or new action budget. Any extension beyond reviewed compelled-budget/spending restrictions must be explicit and preserve actual source history.',
            'Illusion14, Control15, MaterialTerrain8 and Rank7Mechanics16 remain pending comparison sources. True Seeing, Hallucinatory Terrain and Project Image do not supply accepted new mechanics here.',
            'Part4 reached the conversation-length limit. Part5 creation authorization remains pending; no new chat/message/archive transmission or GPT review is claimed.'],
        'earlierOperationalWorkedCases': [], 'currentVectors': [],
        'futureCaseRequirements': [
            'After actual source choices, author at least two complete real-source cases per spell and every distinct new branch. Preserve all originals; conference preparation is not semantic acceptance.',
            'Every case needs genuine acquired class/repertoire, actual level/PB/ability, RP and class strain/history, components/actions, counter chronology and exact source bindings. Conditional premise and runtime coverage remain separate.',
            'Labyrinth: real WIS failure/success, blinded or otherwise qualified perception; current versus future clocks, actual walking/standing/flying support, forced movement and teleport source, overlapping Speed0 and dispel/suppression without new terrain.',
            'Mindtrap: a fully sourced actual prior spell/action with real spent resources and timeline; legal repeat versus lost target/repertoire/components/budget, mandatory costly spell and optional augmentation distinction, current/extra/companion opportunity, competing control guard and exact fallback.',
            'Mirage Arcane: explicit continuous terrain geometry, tactile surface and a real gap/obstacle/hazard; multichannel observer paths, contact/recognition, movement and supported body state, partial suppression and overlap retaining original clocks. No fictional bridge or material yield.',
            'Mirage Legion: all six actual image positions/scripts and one real controller budget; true spell versus apparent performance, actual attack selection if adopted, physical contact and separate observers, overlap with Mirror Image, image ending/recognition across suppression.',
            'Perfect Veil: caster plus three genuinely allied recipients with actual gear transfers; observers using different senses and real interaction branches, remembered knowledge/testimony/known-location targeting, single-versus-group revelation, recast and partial suppression with exact retained identities.',
            'Pending True Seeing/Hallucinatory Terrain/Project Image interactions remain conditional until their own actual acceptance. Use no invented acquired counterpart or unsourced environment ability to satisfy a test.',
            'Record real deterministic operands, RNG/visibility, intermediate/final state and losses at each boundary. No source deletion, runtime/human/balance/cosmology or whole-game gate is implied.'],
        'countsUnchanged': deepcopy(index['authoredCounts']), 'sourceBindings': list(sources.values()),
        'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'humanPlaytests': 0, 'sourceInformationDeleted': 0,
        'cosmologyDecisions': 0, 'wholeGameComplete': False}
    # All adaptive semantic/source inspection above occurs before creating any output artifact.
    root.mkdir(); frozen = []
    for b in sources.values():
        p = G/b['path']; ck('Current source unchanged '+b['path'], info(p) == b)
        dst = root/'sources'/b['path']; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(p.read_bytes())
        ck('Frozen exact source '+b['path'], dst.read_bytes() == p.read_bytes())
        frozen.append({**b, 'frozenCopy': dst.relative_to(G).as_posix()})
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate': info(out), 'checks': checks, 'checkCount': len(checks), 'sourceCount': len(sources),
        'sourceIdentities': 5, 'placements': placements, 'earlierCompleteProcedures': 0, 'earlierOperationalWorkedCases': 0,
        'newCurrentVectors': 0, 'questions': 21, 'riskCounts': risk, 'failures': 0,
        'validationScope': 'Exact source, native metadata/access, accepted/pending comparison separation and byte preservation only; no new semantic or runtime approval.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate': info(out), 'check': info(check), 'files': list(sources.values()),
        'frozenSources': frozen, 'sourceCount': len(sources), 'newRuleAdoptions': 0}))
    (root/'README.md').write_text('# Five rank-seven perception and control sources\n\nRead CANDIDATE.json and all full sources: five identities/five school placements,21 unselected questions and13 reviewed counterpart spells with complete shared rules and available exact receipts/casebooks. Each new spell has an individual risk reason:2B/3C. Pending Illusion14/Control15/MaterialTerrain8/Rank7Mechanics16 are comparisons only.\n\nReturn complete source-faithful proposed procedures and every question disposition. Preserve Mirage Arcane tactile sensation, six Mirage Legion spell-performing images, Perfect Veil complete unnoticeability, Labyrinth WIS/Speed0 and Mindtrap real historical repetition. Do not silently import a universal illusion rule or unresolved True Seeing authority. Explicitly identify each new duration, geometry, control, perception and interaction completion. No operational cases or rules are adopted;525reviewed/323pending remain unchanged.\n', encoding='utf8', newline='\n')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in ['README.md', 'MANIFEST.json']: z.write(root/name, name)
        z.write(out, 'CANDIDATE.json'); z.write(check, 'PREFLIGHT.json')
        for b in frozen: z.write(G/b['frozenCopy'], 'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json') == out.read_bytes()
        for b in frozen: assert z.read('sources/'+b['path']) == (G/b['frozenCopy']).read_bytes()
    b = info(archive)
    request.write_text(f'Please conduct the five-spell rank7 perception/control source conference using {archive.name}, {b["bytes"]}bytes SHA256{b["sha256"]}. Read all complete original/current sources and five placements,21 unselected decisions,13 reviewed counterparts and complete pending comparison records. Risks2B/3C. Preserve tactile terrain, six apparent harmless casters, complete unnoticeability, WIS/Speed0 and real historical action repetition. Resolve precise clocks, perception, body geometry, actual resources and control admission explicitly; pending True Seeing/Hallucinatory Terrain/Project Image are not authority. Return every disposition and complete proposed procedures. No new rules/cases/procedures or525/323membership changes are adopted.\n', encoding='utf8', newline='\n')
    prep.write_bytes(encoded({'archive': b, 'candidate': info(out), 'manifest': info(root/'MANIFEST.json'),
        'check': info(check), 'request': info(request), 'sourceCount': len(sources), 'allArchiveSourcesVerified': True,
        'riskCounts': risk, 'status': 'Prepared UNSENT; no actual GPT decision on this packet.', 'newRuleAdoptions': 0}))
    print(json.dumps({'archive': b, 'candidate': info(out), 'sources': len(sources), 'checks': len(checks), 'questions': 21, 'riskCounts': risk, 'operationalCases': 0}))


if __name__ == '__main__': main()
