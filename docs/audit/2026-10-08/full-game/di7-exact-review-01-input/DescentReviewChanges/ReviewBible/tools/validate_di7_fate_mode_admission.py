"""Close finite source-mode proof gaps without pretending to run every payload."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, V, info, encoded
from di7_area_fixtures import make as area_fixture
from di7_fate_mode_admission import AdmissionSources, FateAdmissionTransactions


def main():
    output = A/'DI7_FATE_MODE_ADMISSION_CHECK.json'; assert not output.exists()
    sources = AdmissionSources(); checks, histories, proofs = [], [], []
    def check(label, value): assert value, label; checks.append(label)
    def reject(label, m, fn, reason):
        before = m.snapshot()
        try: fn()
        except ValueError as error: check(label+'/specific-source-rejection', reason in str(error))
        else: raise AssertionError(label)
        check(label+'/no-RP-budget-strain-history-or-reservation-change', m.snapshot() == before)
    def make(provider='Wizard'):
        base,_ = area_fixture(sources, provider=provider)
        world = deepcopy(base.world)
        world['entities']['target'] = {'kind':'creature','positionFeet':25,'willing':True,'alliedTo':{},'relatedQuestions':[],
            'armor':{'value':15,'authorityEvent':'conditional-actual-unarmored-AC15'},'hp':40,'maximumHp':40,
            'hands':{'left':{'usable':True,'holding':None}}}
        world['alignmentActors']['target'] = {'underlying':{'order':'Chaotic','ethics':'Evil'},'immunities':[], 'permanentIdentity':{'id':'target'},'acquisitionSnapshots':[],'usedAllowances':{}}
        for aid in base.actors: world['relations'][aid+'>target'] = {'sourceFact':'conditional-perceived-open-local-target','perceived':True,'visible':True,'lineOfEffect':True}
        m = FateAdmissionTransactions(sources, base.actors, world)
        m.learn('owner','fate-echo',m.actors['owner']['classLevel'],'actual-owner-Fate-choice')
        m.learn('owner','fate-coin',1,'actual-owner-Coin-choice')
        for sid, level in [('counterspell',5),('lifedraw',1),('fate-coin',2)]: m.learn('counter',sid,level,'actual-counter-choice/'+sid)
        for aid, actor in m.actors.items():
            if actor['provider']=='Wizard': m.prepare_wizard(aid,list(actor['learned']),aid+'/study',{'actor':aid,'completedAt':0,'sourceEvent':'conditional-completed-own-rest'})
        return m
    def observe(m, cid):
        m.world['identificationFacts'][cid+'/direct'] = {'observer':'owner','castId':cid,'kind':'conditional-actual-direct-identification'}
        m.observe_cast('owner',cid,cid+'/direct')
    for provider in ['Wizard','Cleric','Mirrorsage','Shaman']:
        m = make(provider); m.begin_turn('owner','conditional-owner-first-turn')
        m.declare('owner','fate-coin','trigger',{'target':'target','hand':'left'})
        m.declare('counter','counterspell','original-Reaction',{'pendingCast':'trigger'}); observe(m,'original-Reaction')
        m.resolve_counter('original-Reaction',20)
        check(provider+'/real-Reaction-actually-resolved',m.casts['original-Reaction']['status']=='resolved' and m.casts['trigger']['status']=='countered' and m.actors['counter']['rp']<48)
        m.advance(3606); m.begin_turn('owner','conditional-owner-second-regular-turn')
        reject(provider+'/Reaction-cannot-be-Fate-original',m,lambda:m.begin_fate('owner','echo','original-Reaction',{'target':'target','hand':'left'}),'not-Action-or-Bonus-Action')
        histories.append({'id':'actual-Reaction-rejected/'+provider,'final':m.snapshot()})
        m = make(provider); m.begin_turn('counter','conditional-original-turn')
        m.declare('counter','lifedraw','damaging-original',{'target':'target'}); observe(m,'damaging-original')
        result=m.resolve_lifedraw_miss('damaging-original',natural=1)
        check(provider+'/actual-paid-damaging-miss-zero-result',not result['attack']['hit'] and result['damage']==0 and result['healing']==0 and m.actors['counter']['rp']==46 and m.world['entities']['target']['hp']==40)
        m.begin_turn('owner','conditional-owner-turn')
        reject(provider+'/miss-does-not-reclassify-mode',m,lambda:m.begin_fate('owner','echo','damaging-original',{'target':'target'}),'damaging-mode-even-when-missed')
        histories.append({'id':'actual-paid-damaging-miss-rejected/'+provider,'final':m.snapshot()})
    for sid, provider, reason in [
            ('shield','Wizard','not-Action-or-Bonus-Action'), ('counterspell','Wizard','not-Action-or-Bonus-Action'),
            ('lifedraw','Wizard','damaging-mode-even-when-missed'), ('ray-of-frost','Wizard','damaging-mode-even-when-missed'),
            ('summon-lesser-skeleton','Wizard','damaging-summon-mode'), ('arcane-echo','Wizard','further-casting-access-mode'),
            ('true-resurrection','Wizard','actual-rank-outside0-through7'), ('planar-binding','Wizard','no-complete-authorized-operative-adapter'),
            ('false-life','Wizard','indispensable-complete-payload-or-independent-entitlement-adapter-not-supplied')]:
        proof=sources.mode_gate(sid,provider)
        check(sid+'/exact-source-necessary-predicate',proof['admitted'] is False and proof['reason']==reason)
        proofs.append({**proof,'kind':'source-bound-necessary-admission-predicate-proof',
            'logic':'Every original using this exact source mode fails this necessary predicate independently of outcome. No unexecuted source casting, successful original history, damage, summon or recursive grant is asserted.'})
    for sid in ['fate-coin','alignment-suggestion']:
        proof=sources.mode_gate(sid,'Wizard')
        check(sid+'/actual-selected-complete-mode-no-fictional-charge',proof['admitted'] and proof['independentConsumedMaterials']==[] and proof['independentAcquiredUses']==[])
        source=sources.ordinary[sid]
        proofs.append({**proof,'kind':'complete-selected-mode-cost-and-permission-audit','completeOperativeSource':deepcopy(source['operational']),
            'costInterpretation':'Source requires ordinary V/S/F and real nested rank price/strain. Its complete procedure creates no separately consumed material or acquired charge. No donor object/resource is reused. This is not inferred merely from absent structured fields.',
            'remaining': 'No other mode is granted a cost waiver. A genuinely nonempty indispensable cost needs its actual source and complete adapter, otherwise the mode is inadmissible under the authored Fate rule.'})
    # A legal positive still commits the real outer/child. The source filter
    # must not turn ordinary permission absence into a prohibition on copies.
    for provider in ['Wizard','Cleric','Mirrorsage','Shaman']:
        m=make(provider); m.begin_turn('counter','conditional-original-turn')
        m.declare('counter','fate-coin','original',{'target':'target','hand':'left'}); observe(m,'original'); m.resolve_fate_coin('original')
        m.world['entities']['target']['hands']['right']={'usable':True,'holding':None}
        m.begin_turn('owner','conditional-echo-turn'); m.begin_fate('owner','echo','original',{'target':'target','hand':'right'})
        child=m.finish_fate_outer('echo'); m.resolve_fate_coin(child['id'])
        check(provider+'/positive-real-two-cast-cost',m.actors['owner']['rp']==m.actors['owner']['maxRP']-19 and m.actors['counter']['rp']==46)
        check(provider+'/original-coin-not-consumed-as-material',m.world['entities']['target']['hands']['left']['holding']=='coin/original' and m.world['entities']['target']['hands']['right']['holding']=='coin/echo/child')
        histories.append({'id':'positive-selected-mode/'+provider,'final':m.snapshot()})
    report={'status':'pass','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'historyCount':len(histories),
        'sourceBindings':sources.bindings+[info(p) for p in [R/'tools/di7_fate_mode_admission.py',R/'tools/validate_di7_fate_mode_admission.py',R/'tools/di7_alignment_transactions.py',R/'tools/di7_fate_transactions.py',R/'tools/di7_cast_transactions.py',R/'tools/di7_area_fixtures.py',R/'tools/core_playtest_rules.py',V/'DI7_NEXT_EXACT_ACCEPTANCE_CONTRACT.json']],
        'checkLabels':checks,'histories':histories,'modePredicateProofs':proofs,'failures':[],
        'sourceExpectationCoverage':{
            'D7T-08-02':{'executedHistories':[h['id'] for h in histories if not h['id'].startswith('positive')],
                'sourcePredicateProofs':[p['spellId'] for p in proofs if p['kind']=='source-bound-necessary-admission-predicate-proof'],
                'priorNullAndCopyEvidence':info(A/'DI7_FATE_TRANSACTIONS_CHECK.json'),
                'qualification':'Actual paid Counterspell Reaction and Lifedraw miss plus exact source necessary-condition proofs. Other rejected spell payloads are not claimed executed.'},
            'D7T-10-01':{'executedSelectedModes':['fate-coin','alignment-suggestion'],
                'priorOwnStatsAndSourceEvidence':[info(A/'DI7_FATE_TRANSACTIONS_CHECK.json'),info(A/'DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json')],
                'qualification':'Own stats/focus/price/fresh outcomes and empty independent cost sets for two complete selected modes are evidenced. Nonempty independent-entitlement payloads are not executed or supplied; they remain the exact acceptance contract bounded prerequisite, not a new source or universal waiver.'}},
        'scope':'Finite current-mode admission, paid Reaction/missed damaging originals and exact necessary source predicates; selected-mode independent-cost audit.',
        'conditionalPremises':['Attained actors/rest/turns, current AC, line/perception/identification and available body are explicit upstream conditional premises.',
            'Lifedraw miss branch executes a real attack roll and zero damage/healing. Hit damage/healing are deliberately unsupported and rejected by this narrow test adapter.',
            'Source-level negative proofs do not authenticate a spell cast or run the rejected summon/recursive payload. They establish a necessary admission failure independent of any original result.',
            'No nonempty special-material/acquired-charge child exists in these two chosen source modes. That future runtime remains unimplemented; the exact card explicitly makes such a payload inadmissible until actual source/adapter prerequisites exist.'],
        'remaining':['Prepare complete7 exact package and ask GPT to judge the evidence at these explicitly bounded scopes, including the independent-entitlement prerequisite.'],
        'full49Fulfilled':False,'full93Fulfilled':False,'exactApproved':False,'sourceInformationDeleted':0,'spellPromotions':0,'newRuleAdoptions':0}
    output.write_bytes(encoded(report)); print(json.dumps({'report':info(output),'checks':len(checks),'histories':len(histories),'sourceProofs':len(proofs)}))


if __name__=='__main__': main()
