"""Freeze six native resource sources and the decisions still requiring GPT."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank8_resource_6_questions_01 import IDS, ORIGINALS, TIERS, Q


def read(p):
    return json.loads(p.read_bytes())


def main():
    root = A/'rank8-resource6-source-conference-01'
    out = R/'data/director/spell_review/rank8_resource_6_source_conference_01.json'
    check = A/'RANK8_RESOURCE_6_SOURCE_CONFERENCE_01_CHECK.json'
    prep = A/'RANK8_RESOURCE_6_SOURCE_CONFERENCE_01_PREPARATION.json'
    request = A/'RANK8_RESOURCE_6_SOURCE_CONFERENCE_01_REQUEST.txt'
    archive = A/'DD_Rank8_Resource_6_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources, checks = {}, []
    def ck(n, v):
        checks.append({'check': n, 'passed': bool(v)})
        assert v, n
    def bind(p):
        b = info(p)
        sources[b['path']] = b
        return b
    cp = R/'data/public/spell_playtests/catalog.json'
    ip = cp.parent/'authored_review_index.json'
    qp = R/'data/director/spell_review/remaining_work_queue_21.json'
    rp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    catalog, index, queue, registry = map(read, [cp, ip, qp, rp])
    ck('525 reviewed323 pending', index['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    ck('173 accepted scoped interfaces', len(registry['entries']) == 173)
    for p in [cp, ip, qp, rp, Path(__file__), Path(__file__).with_name('rank8_resource_6_questions_01.py'),
              R/'rulebook_output.txt', G/'docs/reference/Player_Rulebook_v6_source_text.txt',
              A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_GATE_GLYPH_28.json',
              A/'LOW_RANK_136_EXACT_FULFILLMENT.json',
              G/'docs/audit/2026-10-18/github-snapshot-rank7-sources/PUSH_RECEIPT.json']:
        bind(p)
    lines = (R/'rulebook_output.txt').read_text('utf-16').splitlines()
    reference_lines = (G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf8').splitlines()
    records = []
    for ident in IDS:
        oldp = A/ORIGINALS[ident]
        old = read(oldp)
        bind(oldp)
        n = next(n for n, s in enumerate(old['selectedSpells']) if s['spellId'] == ident)
        historical = old['selectedSpells'][n]
        card = next(s for s in catalog['spells'] if s['id'] == ident)
        row = next(s for s in queue['rows'] if s['id'] == ident)
        entry = next(e for e in index['entries'] if e['id'] == ident)
        ck('Original/current/queue full equality '+ident, historical['fullSourceAndCurrentAccessRecord'] == card == row['completeCurrentSourceAndAccess'])
        ck('No earlier complete proposal '+ident, row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Still pending '+ident, entry['authoredStatus'] == 'pending-authored-procedure')
        ck('Actual rank8/21RP/min15 '+ident, all(v['rank'] == 8 and v['baseRpCost'] == 21 and v['minimumClassLevel'] == 15 for v in card['classAccess'].values()))
        bb = [deepcopy(b) for b in old['currentBookBindings'] if b['spellId'] == ident]
        ck('All native placements '+ident, len(bb) == len(card['source']['original']['placements']))
        for b in bb:
            k = b['currentBookRow']['line']-1
            ck('Exact current book line '+ident, lines[k] == b['currentBookRow']['exactText'])
            ck('Exact reference book line '+ident, reference_lines[k] == lines[k])
        for key in ['catalog', 'core']:
            ck('Full underlying source hash '+ident+key, bind(R/card['source'][key+'Path'])['sha256'] == card['source'][key+'Sha256'])
        for cls in card['classAccess']:
            bind(R/('data/public/class_playtests/'+cls.lower()+'.json'))
        if ident == 'resonance-furnace':
            ck('Furnace alias remains unassigned', card['source']['coreEntries'] == [] and len(card['source']['possibleHistoricalAliases']) == 1)
            alias = card['source']['possibleHistoricalAliases'][0]
            ck('Exact historical Mana Furnace PB limit', alias['index'] == 187 and alias['original']['name'] == 'Mana Furnace' and alias['original']['effect'] == 'Convert elemental damage taken into RP recovery, to a maximum of proficiency bonus RP per round.')
        if ident == 'leyline-flow':
            ck('Leyline current book cost retained', card['source']['original']['description'] == 'Choose 3 Resonance-using spellcasters; each recovers RP equal to the cost of one spell of Tier 5 or lower they can cast.')
            ck('Leyline conflicting flat10 retained', card['source']['coreEntries'][0]['original']['effect'] == 'Choose three spellcasters; each recovers 10 RP.')
        records.append({'spellId': ident, 'riskTier': TIERS[ident][0], 'riskReason': TIERS[ident][1],
            'completeCurrentCatalogSourceAndAccess': deepcopy(card), 'currentIndexEntry': deepcopy(entry),
            'originalQuestionSource': info(oldp), 'originalQuestionPointer': '/selectedSpells/'+str(n),
            'completeOriginalSourceQuestionUnchanged': deepcopy(historical),
            'completeHistoricalCommonQuestionUnchanged': old['commonOperationalQuestion'],
            'completeHistoricalScopeExceptionUnchanged': old['commonQuestionException'],
            'completeCurrentBookBindings': bb, 'earlierCompleteProcedures': [], 'earlierOperationalWorkedCases': [],
            'status': 'Source conference prepared UNSENT; no procedure/case adoption.'})
    for cls in ['shaman', 'mirrorsage', 'oracle']:
        bind(R/('data/public/class_playtests/'+cls+'.json'))
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md', 'CLASS_PLAYTEST_RULES.md', 'SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md',
                 'HEALING_DEATH_PLAYTEST.md', 'DAMAGE_SHARING_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md',
                 'CRAFTING_HARVEST_PLAYTEST.md', 'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md',
                 'ANCESTRY_BACKGROUND_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    inherited = []
    for n in list(range(0,12))+[13,14,23,24,26,35,36,39,40,41,49,50,58,67,75]:
        e = registry['entries'][n]
        b = e['currentAuthoritativeSource']
        actual = bind(G/b['path'])
        ck('Exact accepted interface hash '+str(n), all(actual[k] == b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer': '/entries/'+str(n), 'completeEntryUnchanged': deepcopy(e),
            'scopeLimit': 'Use only exact accepted scope. Barrier creditable-base accounting, protected principal, Forge cycles, Nexus/Influence order, Null and transfer restrictions are not universally extended or amended by these questions.'})
    counterparts = []
    counterpart_ids = ['resonance-kindle', 'resonance-well', 'resonance-conduit', 'resonance-nexus',
        'resonance-barrier', 'resonance-influence', 'absorb-elements', 'spell-mirror', 'soul-mirror',
        'counterspell', 'antimagic-field-lesser', 'greater-dispel', 'resonance-forge', 'resonance-seal',
        'resonance-sight-supreme', 'fate-echo']
    for ident in counterpart_ids:
        e = next(e for e in index['entries'] if e['id'] == ident)
        ck('Actually reviewed counterpart '+ident, e['authoredStatus'] == 'reviewed-authored-operational-playtest')
        path = (ip.parent/e['procedureFile']).resolve()
        doc = read(path)
        ptr = e.get('wholeCardPointer',e['procedurePointer'])
        binding = bind(path)
        if e.get('completeEnvelopeBinding'):
            ck('Exact complete accepted envelope '+ident, binding == e['completeEnvelopeBinding'])
        if e.get('authoredAcceptanceReceipt'):
            b = e['authoredAcceptanceReceipt']
            ck('Exact authored receipt '+ident, bind(G/b['path']) == b)
        for source in e.get('caseSourceReferenceAliases',{}).values():
            bind(G/source)
        counterparts.append({'spellId': ident, 'source': binding, 'pointer': ptr,
            'completeCurrentCard': deepcopy(at(doc,ptr)), 'completeSharedRules': deepcopy(doc.get('sharedRules',{})),
            'indexEntry': deepcopy(e), 'qualification': 'Actual acceptance/index controls historical candidate flags; exact current full envelopes and casebooks are included. No new scope is inherited automatically.'})
    pending = []
    for group in ['magic-modifiers7','rank7-identity-casting5']:
        g = next(g for g in queue['groups'] if g['group'] == group)
        b = bind(G/g['candidate']['path'])
        ck('Exact pending comparison '+group, b == g['candidate'])
        pending.append({'group': group, 'candidate': b, 'identities': g['identities'],
            'qualification': 'Full candidate file preserved for interaction comparison only; unselected choices are not accepted authority.'})
    questions = [{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,
        'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('24 distinct unselected questions', len(questions) == len({q['id'] for q in questions}) == 24)
    ck('All six identities have questions', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records))
    ck('OneB fiveC actual risk', risk == {'C':5,'B':1})
    ck('Six identities and native placements', len(records) == sum(len(r['completeCurrentBookBindings']) for r in records) == 6)
    candidate = {'id':'RANK8-RESOURCE-6-SOURCE-CONFERENCE-01', 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only',
        'records':records,'currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':counterparts,
        'pendingComparisonsNotAuthority':pending,'questions':questions,'riskCounts':risk,
        'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],
            'startingPoint':'Complete native source and old questions; no earlier complete procedure/cases.',
            'genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'sourceFindings':[
            'Furnace exact-name Core array is empty; Mana Furnace index187 retains PB RP per round. Source alias remains explicitly unassigned.',
            'Leyline book cost-of-eligible-Tier5-or-lower and Core flat10 remain distinct. Equal results for a rank5 base quote do not reconcile every context.',
            'Shield capacity100levels is not100RP and supplies no recovered amount without a conversion decision.',
            'Barrier paid-base credit and protectedX are distinct; Forge5RP cycle principal is a nonspell transaction. Matrix may not silently amend either.',
            'Well creation and receipt limits are separately scoped by beneficial long rest; Conduit conserves actual paid RP and grants no new pool.',
            'Fate Echo is actually accepted despite preserved draft labels; pending Cast Echo/Meta Surge/Resonance Communion proposals remain separate.',
            'A possible group recovery30 versus native price21 is a conditional arithmetic incentive, not a proved infinite loop or balance verdict.'],
        'earlierOperationalWorkedCases':[],'currentVectors':[],
        'futureCaseRequirements':[
            'After exact decisions, supply at least two complete actual cases per spell plus every distinct new branch; include native provider/grant, class/level/ability, real costs, cadence, components, concentration/counter history and exact outcome state.',
            'Shield: a real single-target/multitarget/area root, exact100 capacity ledger including boundary/cantrip behavior, real paid versus waived source, competing Mirror/Counterspell, separate prevention and recovery and no duplicated causal credits.',
            'Nullification: real initial save and60-second application, zero-price ranked cast versus a positive mandatory charge, existing paid Ready release, donor-committed transfer, blocked spell/rest gain, suppression and expiry without queued credit.',
            'Furnace: actual mixed typed event through mitigation/prevention/transfer/temp/form/normalHP, precise eligible funding total, real PB/cap/clock and ratio, concentration/death ordering, self/allied/environmental origin, same-round competing sources and Null lineage.',
            'Matrix: real casting-body position and field geometry at commitment, full price buckets/protected principal, actual Ready setup/release, self-concentration replacement versus another owner’s field, ranked Dissonance block despite0price and native recovery outputs.',
            'Mastery: an identified source and exact hypothetical casting context, actual base/extras/waivers/mandatory charges, current quote versus changed later price, useful authorized hidden-cost information and real defense, no querying side effects or fabricated unknown cost.',
            'Leyline: three real distinct eligible beneficiaries and independent RP pools, true acquired reference spells/native ranks, chosen quote timing, depleted versus currently affordable reference, self inclusion/overflow/late denial, actual party deltas over repeated paid and waived histories.',
            'Keep priced reference calculations, conditional authored encounters, actual engine execution, human playtests, balance and cosmology separate. Source preservation does not complete any of those gates.'],
        'gptCommunication':'Part4 is full; Part5 creation authorization remains pending. This packet is prepared UNSENT, not a GPT decision.',
        'countsUnchanged':deepcopy(index['authoredCounts']),'sourceBindings':list(sources.values()),
        'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,
        'cosmologyDecisions':0,'wholeGameComplete':False}
    root.mkdir()
    frozen = []
    for b in sources.values():
        p = G/b['path']
        ck('Current source unchanged '+b['path'],info(p) == b)
        dst = root/'sources'/b['path']
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(p.read_bytes())
        ck('Frozen exact bytes '+b['path'],dst.read_bytes() == p.read_bytes())
        frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),
        'sourceIdentities':6,'placements':6,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,
        'newCurrentVectors':0,'questions':24,'riskCounts':risk,'failures':0,
        'validationScope':'Exact source/access/authority comparison and preservation only; no semantic approval or gameplay execution.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),
        'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    (root/'README.md').write_text('# Six rank-eight resource spells\n\nRead the six complete native sources and placements,24 unselected questions,16 full accepted counterpart cards and their complete source envelopes/casebooks. Five tierC and one tierB. Explicitly resolve the Mana Furnace alias/PB cap and Leyline book/Core amount conflict. Preserve100 spell-level shield capacity, actual RP denial, damage conversion, a substantive Matrix waiver and useful precise Mastery information.\n\nReturn complete source-faithful proposed procedures and every question disposition. Any new anti-farm restriction, waiver priority, conversion ratio, duration or metadata replacement must be named NEW; counterpart contracts keep their existing scope. Complete actual cases follow decisions. No source deletion, rule promotion, runtime/human/balance/cosmology or whole-game approval.525reviewed/323pending stay unchanged. Part4 is full; this complete packet is UNSENT.\n',encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in ['README.md','MANIFEST.json']: z.write(root/name,name)
        z.write(out,'CANDIDATE.json')
        z.write(check,'PREFLIGHT.json')
        for b in frozen: z.write(G/b['frozenCopy'],'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json') == out.read_bytes()
        for b in frozen: assert z.read('sources/'+b['path']) == (G/b['frozenCopy']).read_bytes()
    b = info(archive)
    request.write_text(f'Please review all six rank8 resource identities in {archive.name}, {b["bytes"]}bytes SHA256{b["sha256"]}. Read the24 unselected questions, complete native sources and six book placements,16 accepted counterpart cards/full casebooks and exact scoped interfaces. FiveC/oneB. Settle historical Mana Furnace alias/PB cap and Leyline cost-reference versus flat10 explicitly. Preserve substantial shield/waiver/recovery/information benefits, with all new limits and genuine global amendments labeled. Resolve actual price/credit/denial/interception/Ready/Null/transfer interactions. No new procedures/cases have been adopted, and525/323 stays unchanged. Pending Cast Echo/Meta Surge/Resonance Communion are comparison only.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),
        'check':info(check),'request':info(request),'sourceCount':len(sources),'allArchiveSourcesVerified':True,
        'riskCounts':risk,'status':'Prepared UNSENT; no actual GPT decision on this packet.','newRuleAdoptions':0}))
    print(json.dumps({'archive':b,'candidate':info(out),'sources':len(sources),'checks':len(checks),'questions':24,'riskCounts':risk,'operationalCases':0}))


if __name__ == '__main__':
    main()
