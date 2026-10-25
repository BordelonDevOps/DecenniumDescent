"""Freeze five native ward sources and the decisions still requiring GPT."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank8_ward_5_questions_01 import IDS, ORIGINALS, TIERS, Q


def read(p):
    return json.loads(p.read_bytes())


def main():
    root = A/'rank8-ward5-source-conference-02'
    out = R/'data/director/spell_review/rank8_ward_5_source_conference_02.json'
    check = A/'RANK8_WARD_5_SOURCE_CONFERENCE_02_CHECK.json'
    prep = A/'RANK8_WARD_5_SOURCE_CONFERENCE_02_PREPARATION.json'
    request = A/'RANK8_WARD_5_SOURCE_CONFERENCE_02_REQUEST.txt'
    archive = A/'DD_Rank8_Ward_5_Source_Conference_02.zip'
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
    qp = R/'data/director/spell_review/remaining_work_queue_24.json'
    rp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    catalog, index, queue, registry = map(read, [cp, ip, qp, rp])
    ck('700 reviewed148 pending', index['authoredCounts'] == {'reviewed': 700, 'pending': 148})
    ck('173 accepted scoped interfaces', len(registry['entries']) == 173)
    for p in [cp, ip, qp, rp, A/'director-spell-review-129/CURRENT_HANDOFF_148.json', A/'director-spell-review-129/CURRENT148_PENDING_IDENTITY_AUDIT_148.json', A/'director-spell-review-129/CURRENT_SPELL_QUEUE_148.json', A/'director-spell-review-129/RANK8_CONTROL5_APPLICATION_148.json', A/'director-spell-review-129/RANK8_CONTROL5_APPLICATION_VALIDATION_148.json', A/'director-spell-review-129/RANK8_CONTROL5_EXACT_ACCEPTANCE_148.json', A/'director-spell-review-129/GPT_DIRECTOR_DECISION_RANK8_CONTROL5_148.json', R/'data/public/spell_candidates/rank8control5_reviewed_148/MODEL.json', R/'data/public/spell_candidates/rank8control5_reviewed_148/CANDIDATE_PACKAGE_MANIFEST.json', Path(__file__), Path(__file__).with_name('rank8_ward_5_questions_01.py'),
              R/'rulebook_output.txt', G/'docs/reference/Player_Rulebook_v6_source_text.txt',
              A/'ACTIVE_AUTHORING_CHECKPOINT_GPT_PART5_REVIEW_31.json',
              A/'LOW_RANK_136_EXACT_FULFILLMENT.json', A/'LANGUAGE_EXACT_FULFILLMENT.json',
              A/'GPT_CONTROL_FINAL_REVIEW.md', A/'GPT_CONTINUATION_05_ACTUAL_START_01.json',
              A/'CODEX_EX58_X01_FULFILLMENT_RECEIPT.txt', R/'docs/mechanics/expedition/EX58_SOURCE_CONTRACTS_CORRECTED.md',
              R/'src/data/reputation.js', R/'data/playtest/control_state_bindings.json',
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
        ck('Exact native class set '+ident, set(card['classAccess']) == ({'Cleric','Druid','Wizard'} if ident == 'antilife-shell' else {'Cleric','Druid','Mage','Wizard'}))
        ck('No historical alias merged '+ident, card['source']['possibleHistoricalAliases'] == [])
        records.append({'spellId': ident, 'riskTier': TIERS[ident][0], 'riskReason': TIERS[ident][1],
            'completeCurrentCatalogSourceAndAccess': deepcopy(card), 'currentIndexEntry': deepcopy(entry),
            'originalQuestionSource': info(oldp), 'originalQuestionPointer': '/selectedSpells/'+str(n),
            'completeOriginalSourceQuestionUnchanged': deepcopy(historical),
            'completeHistoricalCommonQuestionUnchanged': old['commonOperationalQuestion'],
            'completeHistoricalScopeExceptionUnchanged': old['commonQuestionException'],
            'completeCurrentBookBindings': bb, 'earlierCompleteProcedures': [], 'earlierOperationalWorkedCases': [],
            'status': 'Source conference prepared UNSENT; no procedure/case adoption.'})
    for cls in ['paladin','oracle','ranger']:
        bind(R/('data/public/class_playtests/'+cls+'.json'))
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md', 'CLASS_PLAYTEST_RULES.md', 'SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md', 'CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'CREATURE_LIFECYCLE_PLAYTEST.md',
                 'HEALING_DEATH_PLAYTEST.md', 'DAMAGE_SHARING_PLAYTEST.md', 'TRANSFORMATION_SPELL_PLAYTEST.md',
                 'CRAFTING_HARVEST_PLAYTEST.md', 'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md',
                 'ANCESTRY_BACKGROUND_PLAYTEST.md', 'LANGUAGE_COMMUNICATION_PLAYTEST.md',
                 'ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md', 'CONDITION_RECOVERY_PLAYTEST.md',
                 'CONTROL_SOURCE_BINDINGS.md','REPUTATION.md','EQUIPMENT_ITEM_PROCEDURES.md']:
        bind(R/'docs/mechanics'/name)
    inherited = []
    for n in list(range(0,12))+[13,14,15,16,17,19,20,29,31,36,37,39,40]+list(range(43,54))+list(range(64,69))+list(range(78,93))+list(range(108,117))+list(range(143,152)):
        e = registry['entries'][n]
        b = e['currentAuthoritativeSource']
        actual = bind(G/b['path'])
        ck('Exact accepted interface hash '+str(n), all(actual[k] == b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer': '/entries/'+str(n), 'completeEntryUnchanged': deepcopy(e),
            'scopeLimit': 'Use only exact accepted scope. Actual alignment overlays, institutional standing, life/body eligibility, local-expression suppression, information protection, clocks and hard-control histories stay distinct. Scope extensions to these new ward identities require explicit decisions; names or ranks do not grant them.'})
    counterparts = []
    counterpart_ids = ['antimagic-field-lesser', 'greater-dispel', 'counterspell', 'wall-of-force', 'globe-of-invulnerability', 'alignment-lock', 'alignment-anchor', 'alignment-sanctuary', 'alignment-purge', 'alignment-suggestion', 'faction-seal', 'faction-sanctuary', 'reputation-shield', 'protection-from-scrying', 'dominate-person', 'erase-emotion', 'hypnotic-pattern', 'phantasmal-killer', 'greater-phantasmal-killer', 'mental-bomb', 'synaptic-static']
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
    for group in ['ward7','illusion-perception14','companion-life10','rank8-control5','rank7-gate-glyph3']:
        g = next(g for g in queue['groups'] if g['group'] == group)
        b = bind(G/g['candidate']['path'])
        ck('Exact pending comparison '+group, b == g['candidate'])
        pending.append({'group': group, 'candidate': b, 'identities': g['identities'],
            'qualification': 'Full candidate file preserved for interaction comparison only; unselected choices are not accepted authority.'})
    questions = [{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,
        'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('23 distinct unselected questions', len(questions) == len({q['id'] for q in questions}) == 23)
    ck('All five identities have questions', set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    risk = dict(Counter(r['riskTier'] for r in records))
    ck('TwoB threeC actual risk', risk == {'B':2,'C':3})
    ck('Five identities and native placements', len(records) == 5 and sum(len(r['completeCurrentBookBindings']) for r in records) == 8)
    candidate = {'id':'RANK8-WARD-5-SOURCE-CONFERENCE-02', 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only',
        'records':records,'currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':counterparts,
        'pendingComparisonsNotAuthority':pending,'questions':questions,'riskCounts':risk,
        'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],
            'startingPoint':'Complete native source and old questions; no earlier complete procedure/cases.',
            'genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'sourceFindings':['Mind Blank has three different school descriptions; Antimagic Field has two sphere/range descriptions. Actual classAccess still selects Abjuration for both. No union or new mode access is adopted.', 'Alignment Immunity preserves24hours, while alignment-based eligibility/change/benefit and prior-record handling require exact scope decisions.', 'Antilife Shell preserves10feet and concentration minute; living-body eligibility, finite geometry, moving/fixed origin and boundary channels remain explicit choices.', 'Current Lesser Antimagic includes AC5-ANTIMAGIC-IO-04: no imaginary outside-to-outside teleport beam, actual local manifestation, exact captured removal operations and intrinsic exceptions. This is not automatically the rank8 spell’s contract.', 'Reputation Fortress uses negative institutional standing, not alignment or hostility; faction invocation, membership and standing are distinct existing records.', 'Full pending companion/illusion/ward7/control/gate-glyph candidates remain comparisons only; actual Part5 is reviewing Illusion14 with no final at this packet preparation.'],
        'earlierOperationalWorkedCases':[],'currentVectors':[],
        'futureCaseRequirements':['After decisions, supply at least two complete deterministic cases per identity plus all new branches, actual native access/provider/DC, prices/cadence, components, concentration/counter history and private eligibility.', 'Alignment Immunity:24-hour boundary, effective versus underlying axis records, unknown axes, harmful/beneficial classification, initial versus existing effects, protected ward entry and genuine nonalignment restrictions.', 'Antilife Shell:real living0HP and nonliving bodies, carried targets, actual boundary geometry, initial occupants, forced crossing/teleport/Falling, reach/projectiles, moving support and safe resumption.', 'Antimagic Field:each actual placement and accessible mode, lifetime, local manifestations, two field families, overlap establishment/removal, paid casts, real nonspell/Oracle/Spell Preservation exceptions, old distant concentration and no fabricated teleport trajectory.', 'Mind Blank:three native school rows, psychic damage versus control components, divination against a person versus room/witness, past knowledge, friendly communication, actual mental-effect predicates, existing effects, suppression and hard-control history.', 'Reputation Fortress:one actual faction selection,−1/0/+1 standing, unknown entries, real changes/Shield prevention, carried bodies and independent companions, boundary channels and occupancy; no score/membership disclosure or invented moral judgment.', 'No case count or source check asserts runtime, human play, numerical balance, cosmology canon or75-domain closure.'],
        'gptCommunication':'GPT is the source and procedure director. Return148 was accepted and applied before this fresh Ward5 packet was prepared. This Ward5 packet is prepared UNSENT; its choices are not GPT decisions.',
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
        'sourceIdentities':5,'placements':8,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,
        'newCurrentVectors':0,'questions':23,'riskCounts':risk,'failures':0,
        'validationScope':'Exact source/access/authority comparison and preservation only; no semantic approval or gameplay execution.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),
        'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    (root/'README.md').write_text('# Five rank-eight ward sources\n\nRead five full native identities/eight school placements and23 unselected questions. Two tierB and three tierC. The21 reviewed counterpart cards, full envelopes/casebooks and exact interfaces are supplied; historical pending flags inside accepted records are controlled by actual acceptance evidence.\n\nPreserve school-specific Mind Blank and Antimagic descriptions and real Abjuration class access. Resolve Alignment Immunity scope, Antilife Shell geometry/living predicates, distinct antimagic-family overlaps, Mind Blank protections and Reputation Fortress institutional-standing admission. Preserve all printed benefits; new choices need explicit disposition.\n\nNo procedures or cases are adopted by this source packet. Current authority is 700 applied-reviewed / 148 pending / 0 accepted-unapplied. GPT accepted and Codex applied Return148 before this fresh Ward5 packet. Pending comparisons are evidence, not authority. No whole-game, runtime, balance, gameplay or cosmology approval.\n',encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in ['README.md','MANIFEST.json']: z.write(root/name,name)
        z.write(out,'CANDIDATE.json')
        z.write(check,'PREFLIGHT.json')
        for b in frozen: z.write(G/b['frozenCopy'],'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json') == out.read_bytes()
        for b in frozen: assert z.read('sources/'+b['path']) == (G/b['frozenCopy']).read_bytes()
    b = info(archive)
    request.write_text(f"""GPT — please independently review the fresh Rank8 Ward5 source conference packet {archive.name} ({b["bytes"]} bytes; SHA-256 {b["sha256"]}) against the exact current authority of 700 applied-reviewed / 148 pending / 0 accepted-unapplied. The packet includes the current pending identity audit, queue and handoff, plus Return148 director acceptance, application receipt and validation. Review only alignment-immunity, antilife-shell, antimagic-field, mind-blank and reputation-fortress; preserve closed feat335 and all completed/applied spell cohorts. Resolve all 23 unselected questions, return complete source-faithful procedures and every disposition, and run your independent failure check. If it passes, state accepted=true and applied=false for the exact IDs; if not, keep the batch unaccepted/unapplied and list exact blockers. Do not edit or apply canonical files. Preserve all source/content/access/runtime holds and distinguish authored static review from runtime, human play, balance, cosmology and release approval.\n""", encoding='utf8', newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),
        'check':info(check),'request':info(request),'sourceCount':len(sources),'allArchiveSourcesVerified':True,
        'riskCounts':risk,'status':'Prepared UNSENT; no actual GPT decision on this packet.','newRuleAdoptions':0}))
    print(json.dumps({'archive':b,'candidate':info(out),'sources':len(sources),'checks':len(checks),'questions':23,'riskCounts':risk,'operationalCases':0}))


if __name__ == '__main__':
    main()
