"""Freeze complete rank-seven sources and unselected identity/casting questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank7_identity_casting_5_questions_01 import IDS, ORIGINALS, TIERS, Q


def read(p): return json.loads(p.read_bytes())


def main():
    stem = 'RANK7_IDENTITY_CASTING_5_SOURCE_CONFERENCE_01'
    root = A/'rank7-identity-casting5-source-conference-01'
    out = R/'data/director/spell_review/rank7_identity_casting_5_source_conference_01.json'
    check, prep, request = [A/(stem+s) for s in ['_CHECK.json', '_PREPARATION.json', '_REQUEST.txt']]
    archive = A/'DD_Rank7_Identity_Casting_5_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources = {}; checks = []
    def ck(n, v): checks.append({'check': n, 'passed': bool(v)}); assert v, n
    def bind(p):
        b = info(p); sources[b['path']] = b; return b
    cp = R/'data/public/spell_playtests/catalog.json'; ip = cp.parent/'authored_review_index.json'
    qp = R/'data/director/spell_review/remaining_work_queue_18.json'
    rp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    catalog, index, queue, registry = map(read, [cp, ip, qp, rp])
    ck('Current membership525/323', index['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    ck('173 exact scoped interfaces', len(registry['entries']) == 173)
    for p in [cp, ip, qp, rp, Path(__file__), Path(__file__).with_name('rank7_identity_casting_5_questions_01.py'),
              R/'rulebook_output.txt', G/'docs/reference/Player_Rulebook_v6_source_text.txt',
              A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_DAMAGE_25.json',
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
        ck('All real native routes '+ident, set(card['classAccess']) == {'Bard', 'Cleric', 'Mage', 'Mirrorsage', 'Wizard'})
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
    selected = list(range(0, 15))+[23, 24, 36, 39, 40]+list(range(78, 93))+list(range(108, 117))+list(range(143, 152))
    for n in selected:
        e = registry['entries'][n]; b = e['currentAuthoritativeSource']; actual = bind(G/b['path'])
        ck('Exact current interface '+str(n), all(actual[k] == b[k] for k in ['bytes', 'sha256']))
        inherited.append({'registryPointer': '/entries/'+str(n), 'completeEntryUnchanged': deepcopy(e),
            'scopeLimit': 'Retain exact named scope. Extending a source-limited price, clock, body, companion, RNG or copying rule needs explicit new concurrence; no global extension is inferred.'})
    counterparts = []
    names = ['fate-echo', 'echo-cast', 'cantrip-echo', 'arcane-echo', 'invisibility', 'gentle-repose',
             'mirror-image', 'disrupt-memory', 'greater-dispel', 'antimagic-field-lesser', 'haste']
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
    # Include full accepted DI7 Director cases and actual review authority, not a shorthand Fate card alone.
    di7 = read(A/'DI7_EXACT_ACCEPTANCE_RECEIPT.json')
    for b in di7['acceptedArtifactBindings']+[di7[k] for k in ['acceptanceAuthority', 'cardRegister', 'caseDispositions', 'completeVerdict', 'evidenceScopeAddendum']]:
        ck('Exact DI7 full counterpart evidence '+b['path'], bind(G/b['path']) == b)
    for name in ['LOW_RANK_136_EXACT_FULFILLMENT.json', 'FEAT327_SOURCE_VERDICT_RESPONSE.json',
                 'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json',
                 'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json',
                 'BESTIARY_SPELL_PROFILE_DEPENDENCY_INDEX.md']: bind(A/name)
    # Preserve complete sources while exposing only the precise metamagic comparison in the candidate.
    magep = R/'data/public/class_playtests/mage.json'; featp = R/'data/director/feat_candidates/exact_01/cohorts/magic_core.json'
    featcat = R/'data/public/feat_playtests/catalog.json'; mage, feats, featcatalog = map(read, [magep, featp, featcat])
    for p in [featp, featcat, R/'src/data/feats.js']: bind(p)
    mn = next(n for n, c in enumerate(mage['cards']) if c['id'] == 'mage.arch.metaspell-access')
    fn = next(n for n, c in enumerate(feats['records']) if c['featId'] == 'metamagicAdept')
    sn = next(n for n, c in enumerate(featcatalog['feats']) if c['id'] == 'metamagicAdept')
    ck('Full metamagic original preserved', feats['records'][fn]['sourceObject'] == featcatalog['feats'][sn]['sourceObject'])
    metamagic = [
        {'kind': 'Current provisional class card; no new class-wide approval', 'source': info(magep), 'pointer': '/cards/'+str(mn), 'completeRecord': mage['cards'][mn]},
        {'kind': 'Source-directed full feat candidate; exact whole-feat review/runtime still pending', 'source': info(featp), 'pointer': '/records/'+str(fn), 'completeRecord': feats['records'][fn]},
        {'kind': 'Unchanged original feat catalog source; historical flags do not establish acceptance', 'source': info(featcat), 'pointer': '/feats/'+str(sn), 'completeRecord': featcatalog['feats'][sn]}]
    pending = []
    for groupname in ['memory2', 'time-cast5', 'magic-modifiers7']:
        g = next(g for g in queue['groups'] if g['group'] == groupname); b = g['candidate']
        ck('Exact pending comparison '+groupname, bind(G/b['path']) == b)
        pending.append({'group': groupname, 'candidate': deepcopy(b), 'identities': deepcopy(g['identities']),
            'scope': 'Full source/proposal/question file included for reconciliation only; unadopted proposals are not accepted authority.'})
    questions = [{'id': i, 'spellIds': ids, 'exactSourceOrConflict': src, 'options': options,
                  'recommendationAndConsequences': rec, 'decisionSelected': False} for i, ids, src, options, rec in Q]
    ck('24 distinct unselected questions', len(questions) == len({q['id'] for q in questions}) == 24 and not any(q['decisionSelected'] for q in questions))
    ck('All five identities questioned', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records)); ck('Five individually justified tierC', risk == {'C': 5})
    placements = sum(len(r['completeCurrentBookBindings']) for r in records)
    ck('Five identities six native placements', len(records) == 5 and placements == 6)
    candidate = {'id': 'RANK7-IDENTITY-CASTING-5-SOURCE-CONFERENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'SOURCE_CONFERENCE_PREPARED_UNSENT', 'developmentDirection': 'video-game-only',
        'records': records, 'currentAcceptedInterfaceComparisons': inherited, 'completeAcceptedCounterparts': counterparts,
        'completeMetamagicComparisons': metamagic, 'pendingComparisonSources': pending,
        'questions': questions, 'riskCounts': risk,
        'semanticDelta': [{'spellId': r['spellId'], 'riskTier': r['riskTier'], 'riskReason': r['riskReason'],
            'startingPoint': 'Full original source and old questions; no earlier complete procedure or operational case.',
            'genuineQuestionIds': [q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'importantScopeBoundaries': [
            'Fate Echo IS authored-reviewed under actual DI7 exact acceptance, despite older candidate/approved:false labels preserved in its frozen document. It is narrower than Cast Echo; its finite local evaluator coverage does not define the complete eligible authored payload set.',
            'Arcane Echo expressly permits its own normal fresh-cast hooks; Fate Echo explicitly limits copy procs. Neither is a universal rule for every echo.',
            'Metamagic Adept has actual source-directed procedure evidence but complete exact feat review/runtime remain pending. Meta Surge cannot rewrite its points or Mage uses without an explicit scoped decision.',
            'Both Simulacrum school placements are retained under one identity; no full body, equipment, resource, soul or bestiary profile is invented.',
            'Memory2, TimeCast5 and MagicModifiers7 proposals are included intact but unadopted. Chrono Lock, Arcane Clone and Spell Sculptor cannot silently govern these new sources.',
            'Part4 reached the conversation-length limit. Part5 creation authorization remains pending; no new chat/message/archive transmission or GPT review is claimed.'],
        'earlierOperationalWorkedCases': [], 'currentVectors': [],
        'futureCaseRequirements': [
            'After actual source choices, author at least two complete real-source cases per spell and every materially distinct new branch. Preserve source cards and historical questions; never count this conference as semantic acceptance.',
            'All cases require genuinely acquired native class route/repertoire, level/PB/ability, actual RP and class Dissonance, real components/actions/counter chronology, current source versions and complete intermediate/final state.',
            'Cast Echo: inclusive freshness versus expired actual observed original; chosen rank/timing categories; damage miss/save/counter distinction; two-stage cost threshold and intervening Reaction; exact paid Ready reservation/release; concentration, new targets, actual resources, lineage and copied summon/damage output under the chosen admission policy.',
            'Meta Surge: real selected Mage mode with unused and exhausted LongRest use; actual feat acquisition/mode selection with1and0points; suppress/expire between paid Ready and release; quote/refund order and overlapping sources without fabricated new options.',
            'Erase: hostile/friendly/self direct targeting, existing attachments versus fresh selected area, actual physical body and projectile; exact affected observer/memory scope and new perception; independent prior memory edits on expiry/suppression with agency/grants/history retained.',
            'Sequester: injured actual living body with real ongoing effect/breath/disease/death/recovery clocks; no source-free invented disease; drag/carry/support/falling/gear lineage, damage and wake ordering, interrupted suppression/expiry/trigger, no elapsed resource/refund farming.',
            'Simulacrum: authoritative native creature/class snapshot including spent resources and actual inventory; creation placement/admission/counter; selected command/agency costs, recovery and ending/remains; true original versus duplicate lineage, recursive abilities and independent school routes. Missing source profiles are explicit holds.',
            'Use deterministic input/RNG and actual accepted source operands. Authored conditional cases are not live engine execution, human playtesting, numerical balance or cosmology approval.'],
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
        'newCurrentVectors': 0, 'questions': 24, 'riskCounts': risk, 'failures': 0,
        'validationScope': 'Exact source, native metadata/access, accepted/pending comparison separation and byte preservation only; no new semantic or runtime approval.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate': info(out), 'check': info(check), 'files': list(sources.values()),
        'frozenSources': frozen, 'sourceCount': len(sources), 'newRuleAdoptions': 0}))
    (root/'README.md').write_text('# Five rank-seven identity and casting sources\n\nRead CANDIDATE.json and all full sources. Five identities, six school placements,24 unselected questions,11 reviewed spell comparisons, full actual DI7 Director cases/authority and three exact metamagic records. Each new spell is individually tierC. Fate Echo is actually reviewed; its older frozen labels are historical. Pending memory/time/modifier proposals and full-feat exact status remain distinct.\n\nReturn complete source-faithful proposed procedures and all question dispositions. Preserve every printed benefit, actual access and alternate placement. Do not silently restrict Cast Echo to Fate Echo or feat-copy rules, redefine all metamagic as points only, or invent Simulacrum soul/equipment/bestiary authority. Any new completion or restriction must be explicit and scoped. Author operational cases after choices are made. No rules, procedures or cases have been adopted, no packets sent, and525reviewed/323pending remain unchanged.\n', encoding='utf8', newline='\n')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in ['README.md', 'MANIFEST.json']: z.write(root/name, name)
        z.write(out, 'CANDIDATE.json'); z.write(check, 'PREFLIGHT.json')
        for b in frozen: z.write(G/b['frozenCopy'], 'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json') == out.read_bytes()
        for b in frozen: assert z.read('sources/'+b['path']) == (G/b['frozenCopy']).read_bytes()
    b = info(archive)
    request.write_text(f'Please conduct the five-spell rank7 identity/casting source conference using {archive.name}, {b["bytes"]}bytes SHA256{b["sha256"]}. Read all complete sources, six native placements,24 unselected decisions,11 reviewed counterparts, exact DI7 cases/acceptance and actual Mage/feat metamagic evidence. All five are individually tierC. Fate Echo is reviewed, but its narrower eligibility does not automatically restrict Cast Echo. Meta Surge needs a precise waiver across real points and class-use ledgers. Erase, Sequester and Simulacrum require explicit body, agency, memory, clock, resource and lifecycle decisions without new cosmology. Pending comparison proposals are not authority. Return all dispositions and full proposed procedures; no new procedures/cases/rules are adopted and525/323membership remains unchanged.\n', encoding='utf8', newline='\n')
    prep.write_bytes(encoded({'archive': b, 'candidate': info(out), 'manifest': info(root/'MANIFEST.json'),
        'check': info(check), 'request': info(request), 'sourceCount': len(sources), 'allArchiveSourcesVerified': True,
        'riskCounts': risk, 'status': 'Prepared UNSENT; no actual GPT decision on this packet.', 'newRuleAdoptions': 0}))
    print(json.dumps({'archive': b, 'candidate': info(out), 'sources': len(sources), 'checks': len(checks), 'questions': 24, 'riskCounts': risk, 'operationalCases': 0}))


if __name__ == '__main__': main()
