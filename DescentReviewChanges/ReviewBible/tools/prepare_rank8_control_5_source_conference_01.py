"""Freeze five native control sources and the decisions still requiring GPT."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank8_control_5_questions_01 import IDS, ORIGINALS, TIERS, Q


def read(p):
    return json.loads(p.read_bytes())


def main():
    root = A/'rank8-control5-source-conference-01'
    out = R/'data/director/spell_review/rank8_control_5_source_conference_01.json'
    check = A/'RANK8_CONTROL_5_SOURCE_CONFERENCE_01_CHECK.json'
    prep = A/'RANK8_CONTROL_5_SOURCE_CONFERENCE_01_PREPARATION.json'
    request = A/'RANK8_CONTROL_5_SOURCE_CONFERENCE_01_REQUEST.txt'
    archive = A/'DD_Rank8_Control_5_Source_Conference_01.zip'
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
    qp = R/'data/director/spell_review/remaining_work_queue_22.json'
    rp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    catalog, index, queue, registry = map(read, [cp, ip, qp, rp])
    ck('525 reviewed323 pending', index['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    ck('173 accepted scoped interfaces', len(registry['entries']) == 173)
    for p in [cp, ip, qp, rp, Path(__file__), Path(__file__).with_name('rank8_control_5_questions_01.py'),
              R/'rulebook_output.txt', G/'docs/reference/Player_Rulebook_v6_source_text.txt',
              A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_RESOURCE_29.json',
              A/'LOW_RANK_136_EXACT_FULFILLMENT.json', A/'LANGUAGE_EXACT_FULFILLMENT.json',
              A/'GPT_CONTROL_FINAL_REVIEW.md', R/'data/playtest/control_state_bindings.json',
              R/'data/playtest/condition_playtests.json',
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
        ck('Exact native class set '+ident, set(card['classAccess']) == ({'Druid','Mage','Wizard'} if ident == 'frozen-time-prism' else {'Wizard'}))
        ck('No historical alias merged '+ident, card['source']['possibleHistoricalAliases'] == [])
        records.append({'spellId': ident, 'riskTier': TIERS[ident][0], 'riskReason': TIERS[ident][1],
            'completeCurrentCatalogSourceAndAccess': deepcopy(card), 'currentIndexEntry': deepcopy(entry),
            'originalQuestionSource': info(oldp), 'originalQuestionPointer': '/selectedSpells/'+str(n),
            'completeOriginalSourceQuestionUnchanged': deepcopy(historical),
            'completeHistoricalCommonQuestionUnchanged': old['commonOperationalQuestion'],
            'completeHistoricalScopeExceptionUnchanged': old['commonQuestionException'],
            'completeCurrentBookBindings': bb, 'earlierCompleteProcedures': [], 'earlierOperationalWorkedCases': [],
            'status': 'Source conference prepared UNSENT; no procedure/case adoption.'})
    for cls in ['paladin']:
        bind(R/('data/public/class_playtests/'+cls+'.json'))
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md', 'CLASS_PLAYTEST_RULES.md', 'SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md',
                 'HEALING_DEATH_PLAYTEST.md', 'DAMAGE_SHARING_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md',
                 'CRAFTING_HARVEST_PLAYTEST.md', 'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md',
                 'ANCESTRY_BACKGROUND_PLAYTEST.md', 'LANGUAGE_COMMUNICATION_PLAYTEST.md',
                 'ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md', 'CONDITION_RECOVERY_PLAYTEST.md',
                 'CONTROL_SOURCE_BINDINGS.md']:
        bind(R/'docs/mechanics'/name)
    inherited = []
    for n in list(range(0,12))+[13,14,15,17,19,36,39,40]+list(range(78,93))+list(range(108,117)):
        e = registry['entries'][n]
        b = e['currentAuthoritativeSource']
        actual = bind(G/b['path'])
        ck('Exact accepted interface hash '+str(n), all(actual[k] == b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer': '/entries/'+str(n), 'completeEntryUnchanged': deepcopy(e),
            'scopeLimit': 'Use only exact accepted scope. Current condition components, hard-denial history, typed clocks, genuine information protections and Null/life rules stay distinct. A source-specific private nightmare, perception predicate or initial-batch exception does not extend automatically to a different spell.'})
    counterparts = []
    counterpart_ids = ['hypnotic-pattern','slow','silence','phantasmal-killer','invisible-tide',
        'frost-nova','uncontrollable-laughter','blindness-deafness','counterspell','greater-dispel','antimagic-field-lesser']
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
    for group in ['control15','illusion-perception14','rank7-mechanics16','rank7-perception5','rank8-resource6']:
        g = next(g for g in queue['groups'] if g['group'] == group)
        b = bind(G/g['candidate']['path'])
        ck('Exact pending comparison '+group, b == g['candidate'])
        pending.append({'group': group, 'candidate': b, 'identities': g['identities'],
            'qualification': 'Full candidate file preserved for interaction comparison only; unselected choices are not accepted authority.'})
    questions = [{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,
        'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('18 distinct unselected questions', len(questions) == len({q['id'] for q in questions}) == 18)
    ck('All five identities have questions', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records))
    ck('ThreeB twoC actual risk', risk == {'C':2,'B':3})
    ck('Five identities and native placements', len(records) == sum(len(r['completeCurrentBookBindings']) for r in records) == 5)
    candidate = {'id':'RANK8-CONTROL-5-SOURCE-CONFERENCE-01', 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only',
        'records':records,'currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':counterparts,
        'pendingComparisonsNotAuthority':pending,'questions':questions,'riskCounts':risk,
        'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],
            'startingPoint':'Complete native source and old questions; no earlier complete procedure/cases.',
            'genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'sourceFindings':[
            'Prism freezes one creature in place for one round with WIS save ends; no named condition or temporal-clock suspension is supplied.',
            'Presence requires enemies actually seeing the caster, a WIS save and one-round Paralyzed. New observer triggers cannot be inferred from Instantaneous metadata.',
            'Power Word preserves150HP or less and actual Stunned; initial save, lifetime and precise HP measurement remain source decisions.',
            'Mental Collapse forbids all communication and spellcasting for one minute; it is broader than acoustic Silence and narrower than unspecified loss of all agency.',
            'Reality Rewrite changes one recipient’s experience and applies WIS-or-Stunned; it grants no physical reality or history rewrite.',
            'Current condition overlay applies the shared source-character/target/encounter guard across classes, spells and companions; source prevention and later suppression remain distinct.',
            'True Seeing and Hold Monster remain pending; their proposed rules do not govern these five identities.'],
        'earlierOperationalWorkedCases':[],'currentVectors':[],
        'futureCaseRequirements':[
            'After exact choices, supply at least two complete actual cases per identity and every new branch; native class/level/repertoire, actual ability/DC, exact price/cadence, components/concentration/counter history and source eligibility are mandatory facts.',
            'Prism: actual selected state, initial/ending WIS timing, normal/extra/virtual turns, support motion and forced movement, ongoing damage/life/concentration clocks, suppression and exact one-round cleanup. Do not invent temporal suspension or a collision shell.',
            'Presence: exact enemies and actual sight/line of effect, invisible/obscured/caster-image cases, real WIS results, immune components, previous hard-denial history, actual future target end, multiple targets and later sight changes without new unprinted triggers.',
            'Power Word: actual150boundary plus above/below, normal/temp/form HP, real changed HP before resolution, paid hidden-ineligible failure without diagnosis, chosen admission/recovery and no invented external save schedule.',
            'Mental Collapse: actual language/channel permissions and independent knowledge, speech/sign/writing/mental commands, component-free actual spells versus magical nonspells, pending cast versus paid Ready release, concentration, consent, actual companion command and expiry/suppression.',
            'Reality Rewrite: one actual subjective presentation, WIS and exact component defenses, existing hard-control history, real perception-model branches, finite lifetime and remembered experience without physical/historical edits.',
            'Verify separate prevention versus suppression, inherited condition immunities, source identity, costs/no refunds and clocks. Authored cases do not establish runtime, human playtest, balance, cosmology or whole-game approval.'],
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
        'sourceIdentities':5,'placements':5,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,
        'newCurrentVectors':0,'questions':18,'riskCounts':risk,'failures':0,
        'validationScope':'Exact source/access/authority comparison and preservation only; no semantic approval or gameplay execution.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),
        'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    (root/'README.md').write_text('# Five rank-eight control spells\n\nRead five complete native sources/placements,18 unselected questions,11 full reviewed counterpart cards and exact source envelopes/casebooks. Three tierB and two tierC. Retain ordinary rank8/base21/min15 access: Prism is Druid/Mage/Wizard; the other four are Wizard.\n\nReturn full source-faithful proposed procedures and every question disposition. Resolve Prism movement/action/time semantics; Presence actual-sight and one-shot/ongoing admission; Power Word150HP threshold/duration; Mental Collapse all-channel communication and actual-spell denial; Reality Rewrite subjective experience and Stunned. Existing condition, hard-control, clock and life contracts are reused within exact scope, not reopened. Every new choice is labeled.\n\nFull pending Control15/Illusion14/rank7/resource comparisons are not authority. No cases or procedures adopted;525reviewed/323pending unchanged. This complete packet is UNSENT. No runtime/human/balance/cosmology or whole-game approval.\n',encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in ['README.md','MANIFEST.json']: z.write(root/name,name)
        z.write(out,'CANDIDATE.json')
        z.write(check,'PREFLIGHT.json')
        for b in frozen: z.write(G/b['frozenCopy'],'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json') == out.read_bytes()
        for b in frozen: assert z.read('sources/'+b['path']) == (G/b['frozenCopy']).read_bytes()
    b = info(archive)
    request.write_text(f'Please review the five rank8 control identities in {archive.name}, {b["bytes"]}bytes SHA256{b["sha256"]}. Read18 unselected source questions, five native placements,11 reviewed counterparts/full source cases and exact accepted condition/control/time/life contracts. ThreeB/twoC. Preserve all printed benefits and real native access. Resolve each source gap explicitly; retain pending Control15/Illusion14/rank7/resource proposals as comparisons only. Return full proposed procedures and every question disposition; no cases or new rules adopted here,525/323unchanged.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),
        'check':info(check),'request':info(request),'sourceCount':len(sources),'allArchiveSourcesVerified':True,
        'riskCounts':risk,'status':'Prepared UNSENT; no actual GPT decision on this packet.','newRuleAdoptions':0}))
    print(json.dumps({'archive':b,'candidate':info(out),'sources':len(sources),'checks':len(checks),'questions':18,'riskCounts':risk,'operationalCases':0}))


if __name__ == '__main__':
    main()
