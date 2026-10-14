"""Independent source/envelope audit and bounded existing-helper reference cases.

No spell effect runtime is implemented or certified here. Quotation fixtures exist
only in memory; all actual source/catalog rows remain blocked.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from spell_playtest_rules import access_for, quote_cast, SpellRuleError
from core_playtest_rules import attack_roll, saving_throw, task_check, LifeState, damage_event
from combat_playtest_rules import marker_deadline, ExtraActionClock, ReactionClock, MovementLedger

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'low-rank137-source-reviewer-files'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def rejected(fn):
    try:
        fn()
    except SpellRuleError:
        return True
    return False


def expected_effect(text):
    # Deliberately independent of the generator/imports; only these editorial
    # prefixes are permitted to differ from the authoritative full paragraph.
    prefixes = ['Adopt the supplied Silent Echo proposal as NEW authoring direction. ',
                'Adopt the supplied Blurred Visage proposal. ',
                'Adopt the supplied minor-disguise proposal: ',
                'Adopt the supplied Silence proposal. ', 'Adopt the proposal: ']
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):]
            return text[0].upper() + text[1:]
    return text


def validate_card(c, r):
    assert c['id'] == r['spellId'] and c['name'] == r['name']
    assert c['sourceQuestionId'] == r['questionId'] and c['sourceDecisionId'] == r['decisionId']
    assert c['sourceReceipt'] == r['fullSourceAndCurrentAccessRecord']
    assert c['selectionEnabled'] is False and c['visibility'] == 'public-source-review'
    for key in ['classAccess', 'additionalRpCost']:
        assert (key in c) == (key in c['sourceReceipt'])
        if key in c:
            assert c[key] == c['sourceReceipt'][key]
    for key in ['bookBindings', 'sourceModeBindings', 'sourceBookMentionDoesNotGrantAcquisition']:
        assert c[key] == r[key]
    assert c['sharedRuleIds'] == r['sharedPolicyRefs']
    assert c['sourceConflicts'] == r['explicitConflictDispositions']
    assert c['operationPrerequisites'] == r['particularOperationPrerequisites']
    assert c['authoredBoundary'] == r['workedBoundary']
    assert c['sourceReceipt']['operational'] is None
    assert c['sourceReceipt']['status'] == 'blocked-pending-operational-review'
    assert c['reviewEvidence'] == {
        'sourceReviewId': 'LR-SOURCE-2026-10-11', 'exactCandidateApproval': False,
        'catalogPromotionAuthorized': False, 'runtimeVerified': False, 'humanPlaytested': False}
    op = c['operationalCandidate']
    if r['authoring'] is None:
        assert c['id'] == 'blink' and op is None and c['newDecisionNotice'] is None
        assert c['status'] == 'receipt-only-post-push-cosmology'
        return
    assert c['status'] == 'candidate-exact-review-pending'
    assert c['newDecisionNotice'] == r['authoring']['newDecisionNotice']
    mapping = [('castingTime','activation'),('range','range'),('components','components'),
               ('targets','target'),('duration','duration'),('resolution','resolution'),
               ('limitations','limitsAndLifecycle'),('numericParameters','numericParameters')]
    assert set(op) == {x[0] for x in mapping} | {'effect','costProcedure'}
    for dest, source in mapping:
        assert op[dest] == r['authoring'][source], (c['id'], dest)
    assert op['effect'] == expected_effect(r['authoring']['procedure'])
    assert all(isinstance(v, str) and v.strip() for k,v in op.items() if k != 'numericParameters')


def main():
    results = []
    def check(name, actual, expected=True, kind='static-source-envelope'):
        result = {'name': name, 'kind': kind, 'pass': actual == expected,
                  'actual': actual, 'expected': expected}
        results.append(result)
        assert result['pass'], result
    register = read(P / 'LR_137_AUTHORING_REGISTER.json')['records']
    internal_path = R / 'data/playtest/spell_drafts/candidate_low_rank_136.json'
    public_path = R / 'data/public/spell_playtests/candidate_low_rank_136.json'
    internal, public = read(internal_path), read(public_path)
    catalog = read(R / 'data/public/spell_playtests/catalog.json')
    actual = {s['id']: s for s in catalog['spells']}
    check('137 unique ordered candidate identities', [s['id'] for s in public['spells']], [r['spellId'] for r in register])
    check('136 actual full procedures', sum(s['operationalCandidate'] is not None for s in public['spells']), 136)
    allowed = {'id','name','status','selectionEnabled','visibility','sourceQuestionId','sourceDecisionId',
               'sourceReceipt','classAccess','additionalRpCost','bookBindings','sourceModeBindings',
               'sourceBookMentionDoesNotGrantAcquisition','operationalCandidate','sharedRuleIds',
               'sourceConflicts','operationPrerequisites','authoredBoundary','newDecisionNotice','reviewEvidence'}
    assert len(internal['spells']) == 137
    for c, inside, source in zip(public['spells'], internal['spells'], register):
        validate_card(c, source)
        assert not (set(c) - allowed)
        assert inside['internalSourceAuthoringRecord'] == source
        assert c == {k:v for k,v in inside.items() if k != 'internalSourceAuthoringRecord'}
        assert c['sourceReceipt'] == actual[c['id']]
    check('All 137 whole source records and operational cards match authority and exact public projection', True)
    check('All 141 original book bindings preserved', sum(len(c['bookBindings']) for c in public['spells']), 141)
    check('Full envelope metadata projection', {k:v for k,v in public.items() if k != 'spells'}, {k:v for k,v in internal.items() if k != 'spells'})
    check('Every complete shared rule equals final direction', public['sharedRules'], read(P / 'LR_SHARED_OPERATING_DIRECTIONS.json')['policies'])
    doc = (R / 'docs/playtest/LOW_RANK_136_CANDIDATE.md').read_text(encoding='utf-8')
    check('Actual public manuscript byte equality', digest(R / 'docs/playtest/LOW_RANK_136_CANDIDATE.md'), digest(public_path.with_suffix('.md')))
    for rule in public['sharedRules']:
        assert rule['wording'] in doc
    for c in public['spells']:
        heading = f"### {c['sourceQuestionId']} — {c['name']}\n"
        section = doc.split(heading, 1)[1].split('\n### ', 1)[0]
        if c['operationalCandidate']:
            for key, value in c['operationalCandidate'].items():
                assert (json.dumps(value, ensure_ascii=False, indent=2) if key == 'numericParameters' else value) in section, (c['id'], key)
        assert json.dumps(c['sourceModeBindings'], ensure_ascii=False, indent=2) in section
    check('All full operative paragraphs and parameters appear in each correct manuscript section', True)
    check('Live catalog remains 276 operational and 572 pending', [sum(s['operational'] is not None for s in actual.values()),sum(s['operational'] is None for s in actual.values())], [276,572])
    from manifest_loader import load_protected_manifest
    protected = load_protected_manifest(G)
    check('Every one of 342 submitted files remains byte-identical', all(digest(G / k) == v for k,v in protected.items()) and len(protected) == 342)
    cases_path = R / 'data/playtest/spell_drafts/low_rank_137_authored_boundaries.json'
    cases = read(cases_path)['cases']
    worked = read(P / 'LR_WORKED_BOUNDARIES.json')
    proposals = read(P / 'LR_8_PROPOSAL_DISPOSITIONS.json')['records']
    expected_cases = worked['perSpellBoundaries'] + worked['jointBoundaries'] + [b for p in proposals for b in p['boundaryDispositions']]
    check('All 187 full boundary records independently reconstructed from the final directions', [c['authoredExpectation'] for c in cases], expected_cases)
    check('All boundary IDs unique and explicitly non-runtime',len({c['id'] for c in cases}) == 187 and all(c['runtimePassed'] is False for c in cases))
    check('Actual public casebook JSON equals internal casebook',read(R / 'data/public/spell_playtests/low_rank_137_authored_boundaries.json'),read(cases_path))
    case_doc = (R / 'docs/playtest/LOW_RANK_137_AUTHORED_BOUNDARIES.md').read_text(encoding='utf-8')
    check('All complete boundary scenarios rendered in casebook',all(json.dumps(c['authoredExpectation'],ensure_ascii=False,indent=2) in case_doc for c in cases))
    check('Actual public casebook manuscript byte equality',digest(R / 'data/public/spell_playtests/low_rank_137_authored_boundaries.md'),digest(R / 'docs/playtest/LOW_RANK_137_AUTHORED_BOUNDARIES.md'))
    question_map = read(A / 'LOW_RANK_136_CANDIDATE_QUESTION_MAP.json')['records']
    check('Every original question maps to its full exact card and manuscript',len(question_map)==137 and all(m['questionId']==r['questionId'] and m['sourceQuestion']==r['sourceQuestion'] and m['fullOperationalPointer']==f'/spells/{i}/operationalCandidate' for i,(m,r) in enumerate(zip(question_map,register))))

    # Meaningful fault injection: reject missing text, altered school modes/access,
    # absent/null changes and accidental promotion even when counts still match.
    mutations = [
        ('effect paragraph removed', 0, lambda c: c['operationalCandidate'].__setitem__('effect','')),
        ('range changed', 0, lambda c: c['operationalCandidate'].__setitem__('range','300 feet')),
        ('source field added as null', 0, lambda c: c['sourceReceipt'].__setitem__('inventedAbsentField',None)),
        ('access rank changed', 0, lambda c: c['classAccess']['Bard'].__setitem__('rank',9)),
        ('second school mode deleted', 5, lambda c: c['sourceModeBindings'].pop()),
        ('public exact approval invented', 0, lambda c: c['reviewEvidence'].__setitem__('exactCandidateApproval',True)),
        ('Blink made operational', next(i for i,r in enumerate(register) if r['spellId']=='blink'), lambda c: c.__setitem__('operationalCandidate',{})),
    ]
    for label,index,edit in mutations:
        mutant = deepcopy(public['spells'][index]); edit(mutant)
        caught = False
        try:
            validate_card(mutant, register[index])
        except AssertionError:
            caught = True
        check('Reject corruption: ' + label, caught, kind='fault-injection')

    # Existing ordinary pricing helper: no fake approved record is saved.
    access_trials = 0
    quote_trials = 0
    for c in public['spells']:
        s = c['sourceReceipt']
        for cls,grant in s['classAccess'].items():
            assert rejected(lambda: access_for(s, cls, 20))
            for level in range(1,21):
                access_trials += 1
                assert (not rejected(lambda: access_for(s, cls, level, require_operational=False))) == (level >= grant['minimumClassLevel'])
            if c['id'] == 'blink':
                continue
            fixture = deepcopy(s)
            fixture['status'] = 'operational-playtest-draft'  # In-memory quotation assumption only.
            kwargs = dict(class_name=cls,class_level=20,available_spell_ids={s['id']},rp=100,max_rp=100,dissonance=0,proficiency=2,casting_modifier=3)
            for dissonance,surcharge in [(0,0),(7,1),(10,2)]:
                quote_trials += 1
                q = quote_cast(fixture, **{**kwargs,'dissonance':dissonance})
                assert q['cost'] == grant['baseRpCost'] + s['additionalRpCost'] + (surcharge if grant['rank'] else 0)
            assert rejected(lambda: quote_cast(fixture, **{**kwargs,'available_spell_ids':set()}))
            assert rejected(lambda: quote_cast(fixture, **{**kwargs,'class_name':'Oracle'}))
            if grant['baseRpCost'] + s['additionalRpCost'] > 0:
                assert rejected(lambda: quote_cast(fixture, **{**kwargs,'rp':0}))
            q = quote_cast(fixture, **{**kwargs,'previous_spell_id':s['id'],'previous_refrain':3})
            assert q['refrain'] == 3
            if grant['rank']:
                assert rejected(lambda: quote_cast(fixture, **{**kwargs,'dissonance':13}))
    check('Actual class/level gates evaluated without enabling source spells', access_trials, access_trials, 'existing-helper-reference')
    check('Base/additional RP and strain states evaluated on explicitly hypothetical in-memory quotation fixtures', quote_trials, quote_trials, 'existing-helper-reference')

    def ref(name, actual_value, expected_value):
        check(name,actual_value,expected_value,'existing-helper-reference')
    ref('NE-05 natural 1 misses despite high modifier',attack_roll(1,40,12)['hit'],False)
    ref('NE-05 natural 20 critical despite high AC',attack_roll(20,0,50)['critical'],True)
    ref('IL-03 ordinary roll misses by one',attack_roll(7,4,12)['hit'],False)
    ref('IL-03 ordinary roll meets AC',attack_roll(8,4,12)['hit'],True)
    ref('NE-18 natural 20 save is not automatic',saving_throw(20,0,21)['success'],False)
    ref('NE-18 natural 1 save is not automatic failure',saving_throw(1,20,21)['success'],True)
    ref('IL-24 Investigation natural 20 improves task degree',task_check(20,0,21)['success'],True)
    ref('IL-24 Investigation natural 1 reduces task degree',task_check(1,20,21)['success'],False)
    ref('NE-01 excludes current target end and fixes third future end',str(marker_deadline(5,0,3,excluded_current_marker=6)),'24')
    ref('IL-01 at regular start expires at next future start',str(marker_deadline(6,0,1)),'12')
    ref('IL-15 three future caster starts retain original phase',str(marker_deadline(5,0,3)),'18')
    extra = ExtraActionClock(); extra.spend(2)
    ref('R3 Haste second full extra Action in same numbered round rejected',rejected(lambda: extra.spend(2)),True)
    ref('R3 Haste recursive extra Action rejected',rejected(lambda: extra.spend(3,granted_by_extra_action=True)),True)
    reaction = ReactionClock(); reaction.spend(); reaction.extra_turn()
    ref('UN-13 extra turn does not refill relay Reaction',rejected(lambda: reaction.spend()),True)
    move = MovementLedger(); move.spend(20,30); move.dash()
    ref('TR-16 later actual Dash retains spent movement at doubled Speed',move.remaining(60),100)
    victim = LifeState(10,10,temp_hp=3)
    after,events = damage_event(victim,4)
    ref('NE-02 one point normal loss after three temporary points', [after.hp,after.temp_hp,events['woundSaves']], [9,0,0])
    after,events = damage_event(victim,3)
    ref('NE-02 all temporary absorption funds no normal HP loss', [after.hp,after.temp_hp], [10,0])
    after,events = damage_event(LifeState(10,4),4,constitution_save_modifier=2,wound_natural=8)
    ref('NE damage reaches zero and makes one Wound save', [after.hp,events['woundSaves'],after.dead], [0,1,False])
    after,events = damage_event(LifeState(10,4),14)
    ref('NE excess damage resolves instant death before Wound save',[after.dead,events['instantDeath'],events['woundSaves']],[True,True,0])
    after,events = damage_event(LifeState(10,0,death_failures=1),1,critical=True)
    ref('NE critical while already dying adds two death failures',[after.dead,events['deathFailuresAdded']],[True,2])
    # Transparent numerical expectations only, not spell execution.
    check('TR-19 original ten pounds uses 27/8 and 1/8 factors',[10*27/8,10/8],[33.75,1.25],'arithmetic-only')
    check('NE-15 save amount then flat reduction then resistance floor',max(0,9-2)//2,3,'arithmetic-only')
    check('NE-16 donor RP debit bounded by actual caster capacity after payment',min(4,5,6-(6-2)),2,'arithmetic-only')
    check('TR-13 mixed physical/fire packet keeps fire separate',[9//2,6],[4,6],'arithmetic-only')

    report = {'status':'passed-bounded-local-checks-exact-review-pending',
              'scope':'Full static source/envelope preservation, deliberate corruption detection, existing access/pricing/Core/clock helper cases and explicit arithmetic. '
                      'Does not execute the 136 spell procedures, authenticate world premises, implement wrapper/sensor/summon controllers, certify class-specific hooks or human balance.',
              'sourceRecordsPromoted':0,'exactCandidateApproval':False,'runtimeVerified':False,
              'accessBoundaryTrials':access_trials,'ordinaryPriceTrials':quote_trials,
              'checks':results,
              'candidateHashes':{str(p.relative_to(G)).replace('\\','/'):digest(p) for p in [internal_path,public_path]},
              'helperHashes':{p.name:digest(p) for p in [Path(__file__),R/'tools/spell_playtest_rules.py',R/'tools/core_playtest_rules.py',R/'tools/combat_playtest_rules.py']}}
    (A/'LOW_RANK_136_CANDIDATE_LOCAL_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'checks':len(results),'accessBoundaryTrials':access_trials,'ordinaryPriceTrials':quote_trials,'status':report['status']}))


if __name__ == '__main__':
    main()
