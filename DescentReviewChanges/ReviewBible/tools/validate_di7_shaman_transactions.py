"""Actual selected/paid totems and nine source-derived vent expectations."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from di7_area_fixtures import make as area_fixture
from di7_shaman_transactions import ShamanSources,ShamanTransactions


def main():
    output=A/'DI7_SHAMAN_TRANSACTIONS_CHECK.json'; assert not output.exists()
    sources=ShamanSources(); checks=[]; histories=[]; coverage={}
    def check(label,ok): assert ok,label; checks.append(label)
    def record(label,m): histories.append({'id':label,'final':m.snapshot()})
    def reject(label,m,fn):
        before=m.snapshot()
        try: fn()
        except ValueError as e: check(label+'/rejected',bool(str(e)))
        else: raise AssertionError(label)
        check(label+'/atomic',m.snapshot()==before)
    kit=['shaman.base.totem-casting','shaman.base.spirit-shock','shaman.base.flask-use','shaman.base.elemental-ward']
    def make(sid='mass-revelation',*,totem=True,start_position=0,kit_ids=None):
        base,_=area_fixture(sources,provider='Shaman'); world=deepcopy(base.world); actors=deepcopy(base.actors)
        actors['owner']['positionFeet']=start_position
        world['entities']['owner']['positionFeet']=start_position
        world['roundClock']={'origin':3600,'authorityEvent':'conditional-actual-encounter-round-clock'}
        world['auraLines']={}; world['totemSites']={}
        for site,pos in [('near',5),('near-two',10),('far',40),('blocked',15),('occupied',0)]:
            world['totemSites'][site]={'positionFeet':pos,'authorityEvent':'conditional-actual-ground-site/'+site,'perceived':True,
                'lineOfEffect':site!='blocked','groundSupportsTinyObject':True,'occupiedByCreature':site=='occupied'}
        world['entities']['target']={'kind':'creature','positionFeet':15,'willing':True,'alliedTo':{'owner':True},'relatedQuestions':['Where is the key?'],
            'hands':{'left':{'usable':True,'holding':None},'right':{'usable':True,'holding':None}}}
        world['alignmentActors']['target']={'underlying':{'order':'Chaotic','ethics':'Evil'},'immunities':[],'permanentIdentity':{'id':'target'},'acquisitionSnapshots':[],'usedAllowances':{}}
        for aid in actors:
            for target in world['entities']:
                world['relations'][aid+'>'+target]={'sourceFact':'conditional-actual-straight-line-reference','perceived':True,'visible':True,'lineOfEffect':True}
        world['entities']['point']['positionFeet']=30
        for e in world['entities'].values():
            e.update(actualPoisonRecords=[],poisonHistoryAuthority='conditional-actual-poison-free-body-object-record',explicitPoisonAbsenceOrCompleteRecords=True)
        actors['owner']['knownFactions']=['guild']; world['establishedFactions']=['guild']
        m=ShamanTransactions(sources,actors,world)
        m.select_base_kit('owner',kit if kit_ids is None else kit_ids,'actual-first-level-Base-selection',affinity='Earth')
        m.learn_cantrip('owner','detect-poison','actual-first-level-cantrip-choice')
        m.learn('owner',sid,20,'actual-level20-rank7-choice')
        m.learn('counter','counterspell',5,'actual-Counter-learning'); m.learn('counter','fate-coin',1,'actual-Coin-learning'); m.learn('counter','alignment-suggestion',1,'actual-Suggestion-learning')
        m.prepare_wizard('counter',list(m.actors['counter']['learned']),'counter-study',{'actor':'counter','completedAt':0,'sourceEvent':'conditional-completed-rest'})
        m.configure_clock('initiative-virtual-source-start',{'owner':0,'counter':2},{'id':'actual-clock','at':3600,'authorityEvent':'conditional-actual-order'})
        m.begin_turn('owner','owner-turn1')
        if totem:
            m.cast_totem('owner','totem','near'); m.world['auraLines']['owner>totem']={'authorityEvent':'conditional-open-own-aura','lineOfEffect':True}
        return m
    def next_turn(m): m.advance(3606); m.begin_turn('owner','owner-turn2')
    def extra(m,eid='extra-action'):
        m.conditional_extra_action('owner',{'id':eid,'authorityEvent':'conditional-actual-separately-legal-extra-full-Action',
            'sourceVersion':'explicit-upstream-extra-action-premise-v1','actualLegalGrant':True,
            'qualification':'Only this vent interface is executed; acquisition/payment of the external action grant remains an upstream conditional premise.'})
    def request(sid):
        if sid=='mass-revelation': return {'direction':[1,0,0]}
        if sid=='vision-quest': return {'target':'target','question':'Where is the key?'}
        if sid=='faction-omniscience': return {'target':'target','faction':'guild'}
        if sid=='resonance-sight-supreme': return {'target':'point'}
        return {'target':'target'}
    def ordinary(m,sid='mass-revelation',cid='spell'):
        m.declare('owner',sid,cid,request(sid)); return m.take_payload_resolution(cid)
    def original(m,sid='fate-coin'):
        m.begin_turn('counter','counter-original-turn')
        m.declare('counter',sid,'original',{'target':'target',**({'hand':'left'} if sid=='fate-coin' else {})})
        m.world['identificationFacts']['direct-original']={'observer':'owner','castId':'original','kind':'conditional-actual-direct-identification'}
        m.observe_cast('owner','original','direct-original')
        if sid=='fate-coin': m.resolve_fate_coin('original')
        else: m.resolve_alignment('original',face=1,modifier=0)
        next_turn(m)
    m=make(); t=m.totems['totem']
    check('actual-selected-four-Base-cards-with-two-active',len(m.selected_kits['owner']['choices'])==4 and 'shaman.base.totem-casting' in m.selected_kits['owner']['choices'])
    check('actual2RP-Action-visible-Tiny-physical-object',m.actors['owner']['rp']==56 and m.actors['owner']['actions']==0 and t['hp']==40 and t['ac']==18 and t['size']=='Tiny' and t['visible'])
    check('shared-concentration-original-three-source-starts',m.actors['owner']['concentration']=='totem-concentration/owner' and t['deadline']==3618)
    check('technique-not-ordinary-cast-or-strain',m.actors['owner']['dissonance']==0 and m.actors['owner']['previousSpell'] is None and not m.vent_uses)
    record('actual-selected-paid-totem',m)
    for site in ['far','blocked','occupied']:
        m=make(totem=False); reject('illegal-site/'+site,m,lambda:m.cast_totem('owner','illegal',site)); record('illegal-site/'+site,m)
    no_totem_kit=['shaman.base.spirit-sight','shaman.base.spirit-shock','shaman.base.flask-use','shaman.base.elemental-ward']
    m=make(totem=False,kit_ids=no_totem_kit); reject('unselected-totem-no-engine-grant',m,lambda:m.cast_totem('owner','illegal','near')); record('unacquired-feature',m)
    for sid in ['mass-revelation','premonition-shield','faction-omniscience','resonance-sight-supreme']:
        m=make(sid); next_turn(m); cast=ordinary(m,sid)
        check(sid+'/post-payment-step5-vent',cast['quote']['cost']==17 and cast['dissonanceAdded']==1 and m.actors['owner']['rp']==39 and m.actors['owner']['dissonance']==1)
        check(sid+'/actual-aura-still-live-and-round-occupied',m.totems['totem']['state']=='active' and m.vent_uses['owner']['1']['castId']=='spell')
        check(sid+'/payload-not-certified-by-casting-boundary',cast['status']=='ready-for-payload')
        record('ordinary-inside/'+sid,m)
    coverage['DI7-SHAMAN-VENT-ORDINARY']=['ordinary-inside/'+sid for sid in ['mass-revelation','premonition-shield','faction-omniscience','resonance-sight-supreme']]
    for sid in ['vision-quest','alignment-purge']:
        m=make(sid); next_turn(m); cast=ordinary(m,sid)
        check(sid+'/concentration-ends-aura-before-step5',m.totems['totem']['state']=='ended' and m.totems['totem']['endReason']=='concentration-displaced' and m.actors['owner']['concentration']=='spell')
        check(sid+'/no-vent-and-no-opportunity-spent',cast['dissonanceAdded']==2 and m.actors['owner']['dissonance']==2 and not m.vent_uses and m.actors['owner']['rp']==39)
        record('concentration/'+sid,m)
    coverage['DI7-SHAMAN-VENT-CONCENTRATION']=['concentration/vision-quest','concentration/alignment-purge']
    m=make(start_position=22); next_turn(m)
    m.declare('owner','detect-poison','outside-cantrip',{'target':'owner'}); m.resolve_detect_poison('outside-cantrip')
    check('outside-cantrip-no-vent-consumption',not m.vent_uses and m.actors['owner']['rp']==56)
    m.actors['owner']['positionFeet']=0; m.world['entities']['owner']['positionFeet']=0
    m.events.append({'event':'actual-ordinary22ft-walk','kind':'conditional-legal-movement','distanceFeet':22,'at':m.now})
    extra(m); cast=ordinary(m)
    check('later-inside-same-round-gets-first-opportunity',cast['dissonanceAdded']==1 and len(m.vent_events)==1 and m.vent_events[0]['castId']=='spell')
    record('outside-then-inside-same-round',m); coverage['DI7-SHAMAN-VENT-OUTSIDE-INSIDE']='outside-then-inside-same-round'
    m=make(); next_turn(m); m.actors['owner']['dissonance']=5
    m.events.append({'event':'actual-prior-strain-premise','kind':'conditional-upstream-stored-Dissonance','value':5})
    m.declare('owner','detect-poison','zero-cantrip',{'target':'owner'}); answer=m.resolve_detect_poison('zero-cantrip')
    check('zero-generated-cantrip-spends-opportunity-not-stored-strain',m.actors['owner']['dissonance']==5 and m.vent_uses['owner']['1']['reduction']==0 and answer=={'containsPoison':False})
    extra(m); cast=ordinary(m)
    check('later-ranked-cast-no-vent-after-zero',cast['dissonanceAdded']==2 and m.actors['owner']['dissonance']==7 and len(m.vent_events)==1)
    record('zero-first-cantrip',m); coverage['DI7-SHAMAN-VENT-ZERO']='zero-first-cantrip'
    m=make(); next_turn(m); m.declare('owner','mass-revelation','countered',request('mass-revelation'))
    m.declare('counter','counterspell','counter-it',{'pendingCast':'countered'}); m.resolve_counter('counter-it',20)
    check('countered-ordinary-keeps-cost-vent-history',m.actors['owner']['rp']==39 and m.actors['owner']['dissonance']==1 and m.vent_uses['owner']['1']['castId']=='countered' and m.totems['totem']['state']=='active')
    extra(m); cast=ordinary(m,cid='later')
    check('counter-no-new-opportunity-for-repeat',cast['dissonanceAdded']==3 and m.actors['owner']['dissonance']==4 and m.actors['owner']['rp']==22)
    record('countered-first-vent',m); coverage['DI7-SHAMAN-VENT-COUNTERED']='countered-first-vent'
    m=make(); extra(m); m.cast_totem('owner','second','near-two'); m.world['auraLines']['owner>second']={'authorityEvent':'conditional-open-own-second-aura','lineOfEffect':True}
    next_turn(m); cast=ordinary(m)
    check('two-own-overlapping-totems-one-vent',sum(t['state']=='active' for t in m.totems.values())==2 and cast['dissonanceAdded']==1 and len(m.vent_events)==1 and m.actors['owner']['rp']==37)
    record('two-own-overlapping',m); coverage['DI7-SHAMAN-VENT-OVERLAP']='two-own-overlapping'
    # A second Shaman also actually selects/pays its totem; ownership is not a
    # caller boolean standing in for an unacquired class engine.
    m=make(totem=False); template=deepcopy(m.actors['owner']); template['body']['focus']['owner']='other'; template['body']['focus']['id']='other-focus'
    template['learned']={}; template['turnHistory']=[]; template['positionFeet']=0; template['concentration']=None
    m.actors['other']=template; m.world['entities']['other']=deepcopy(m.world['entities']['owner'])
    m.select_base_kit('other',kit,'other-actual-Base-selection'); m.alignment.schedule['other']=0
    m.begin_turn('other','other-turn1'); m.cast_totem('other','others-totem','near')
    m.world['auraLines']['owner>others-totem']={'authorityEvent':'conditional-other-aura-contains-owner','lineOfEffect':True}
    next_turn(m); cast=ordinary(m)
    check('other-owning-Shaman-paid-object-but-no-vent',m.actors['other']['rp']==56 and cast['dissonanceAdded']==2 and not m.vent_uses)
    record('other-owners-paid-aura',m); coverage['DI7-SHAMAN-VENT-OTHER-OWNER']='other-owners-paid-aura'
    for child_sid in ['fate-coin','alignment-suggestion']:
        m=make('fate-echo'); original(m,child_sid)
        m.begin_fate('owner','echo','original',{'target':'target','hand':'right'}); child=m.finish_fate_outer('echo')
        check(child_sid+'/actual-outer-vent-child-none',m.casts['echo']['dissonanceAdded']==1 and child['dissonanceAdded']==1 and child['classHooks']==[] and len(m.vent_events)==1)
        check(child_sid+'/actual-two-costs-and-child-strain',m.actors['owner']['rp']==37 and m.actors['owner']['dissonance']==2)
        if child_sid=='fate-coin': m.resolve_fate_coin(child['id']); check('nonconcentration-child-keeps-totem',m.totems['totem']['state']=='active')
        else: m.resolve_alignment(child['id'],face=1,modifier=0); check('concentration-child-ends-totem-without-reversing-outer',m.totems['totem']['state']=='ended' and m.actors['owner']['dissonance']==2 and m.vent_uses['owner']['1']['castId']=='echo')
        record('Fate-child/'+child_sid,m)
    coverage['DI7-SHAMAN-VENT-FATE']=['Fate-child/fate-coin','Fate-child/alignment-suggestion']
    m=make('fate-echo'); original(m); m.begin_fate('owner','ready-echo','original',ready_trigger='bell')
    check('Ready-concentration-before-vent',m.totems['totem']['state']=='ended' and m.casts['ready-echo']['dissonanceAdded']==2 and not m.vent_uses and m.actors['owner']['concentration']=='ready-echo')
    check('Ready-no-self-displacement-duplicate',sum(x['replacedBy']=='ready-echo' for x in m.actors['owner']['endConcentrationHistory'])==1)
    m.finish_fate_outer('ready-echo'); m.advance(3607); m.world['triggerEvents']['bell-event']={'trigger':'bell','at':3607,'perceivedBy':{'owner':True}}
    child=m.release_fate_ready('owner','bell-event',{'target':'target','hand':'right'})
    check('Ready-release-no-new-outer-vent',m.casts['ready-echo']['dissonanceAdded']==2 and m.actors['owner']['dissonance']==3 and not m.vent_uses)
    m.resolve_fate_coin('ready-echo/child')
    check('Ready-actual-both-costs-and-one-release-Reaction',m.actors['owner']['rp']==37 and m.actors['owner']['reactions']==0)
    record('Ready-hold-and-release',m); coverage['DI7-SHAMAN-VENT-READY']='Ready-hold-and-release'
    m=make('fate-echo'); original(m); m.actors['owner']['dissonance']=16
    m.events.append({'event':'actual-preexisting-strain16','kind':'conditional-upstream-Dissonance','value':16})
    before=m.snapshot()
    reject('Ready-known-concentration-loss-forecast-block',m,lambda:m.begin_fate('owner','blocked-ready','original',ready_trigger='bell'))
    check('failed-forecast-preserves-actual-totem',m.totems['totem']['state']=='active' and m.actors['owner']['rp']==56)
    m.begin_fate('owner','legal-immediate','original',{'target':'target','hand':'right'}); child=m.finish_fate_outer('legal-immediate')
    check('immediate-actual-vent-affects-child-forecast',m.composites['legal-immediate']['forecast']['dissonance']==17 and child is not None and child['quote']['cost']==4 and m.actors['owner']['rp']==33)
    m.resolve_fate_coin(child['id']); record('chronological-Fate-forecast-with-real-vent',m)
    for reason in ['suppressed','expired','destroyed','incapacitated']:
        m=make(); next_turn(m)
        if reason=='suppressed': m.suppress_totem('totem',True)
        elif reason=='expired': m.advance(3618); m.begin_turn('owner','owner-expiry-turn')
        elif reason=='destroyed': m.totems['totem']['hp']=0; m.events.append({'event':'actual-destruction-premise','kind':'conditional-legal-object-damage-to0'}); m.advance(m.now)
        else:
            m.actors['owner']['body']['canAct']=False; m.advance(m.now); m.actors['owner']['body']['canAct']=True
        cast=ordinary(m)
        check(reason+'/no-active-own-aura-vent',cast['dissonanceAdded']==2 and not m.vent_uses)
        if reason=='suppressed':
            m.suppress_totem('totem',False); check('suppression-return-no-retroactive-checkpoint',m.casts['spell']['dissonanceAdded']==2 and m.totems['totem']['deadline']==3618)
        record('totem-state/'+reason,m)
    m=make(); next_turn(m); ordinary(m); m.advance(3612); m.begin_turn('owner','owner-turn3'); second=ordinary(m,cid='second-round')
    check('new-real-round-new-opportunity-original-Refrain-retained',second['dissonanceAdded']==2 and len(m.vent_uses['owner'])==2 and m.actors['owner']['refrain']==1)
    record('new-round-not-new-resource-pool',m)
    m=make(totem=False); m.actors['owner']['heroPath']='Bloodcaller'; m.cast_totem('owner','retained-technique','near'); next_turn(m)
    reject('Bloodcaller-keeps-technique-but-no-ordinary-rank7',m,lambda:ordinary(m)); reject('Bloodcaller-no-ordinary-cantrip',m,lambda:m.declare('owner','detect-poison','forbidden',{'target':'owner'}))
    check('Bloodcaller-keeps-real-RP-paid-totem',m.actors['owner']['rp']==56 and m.totems['retained-technique']['state']=='active'); record('retained-technique-not-ordinary-provider',m)
    expected={v['id'] for s in json.loads((R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json').read_bytes())['supplementalSourceExpectations'] if s['id']=='DI7-SHAMAN-VENT-01' for v in s['variants']}
    check('all9-Shaman-source-expectations-covered',set(coverage)==expected and len(expected)==9)
    bindings=sources.bindings+[info(p) for p in [R/'tools/di7_shaman_transactions.py',R/'tools/validate_di7_shaman_transactions.py',R/'tools/di7_alignment_clock.py',
        R/'tools/di7_fate_transactions.py',R/'tools/di7_cast_transactions.py',R/'tools/di7_area_fixtures.py',R/'tools/control_playtest_rules.py',
        A/'DI7_SHAMAN_VENT_RECEIVED.json',R/'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json']]
    report={'status':'pass','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'historyCount':len(histories),'sourceBindings':bindings,
        'checkLabels':checks,'histories':histories,'sourceExpectationCoverage':coverage,'failures':[],
        'scope':'Actual selected Base kit, actual paid Stone Totem Casting and active-object/concentration/round history; all7 ordinary DI7 commitment boundaries, actual rank0 Detect Poison, actual Fate child and Ready/forecast source-order vent expectations.',
        'conditionalPremises':['Actual attained caster/body/rest/world slices; full level-by-level character development remains upstream.',
            'Six-second round origin, legal extra Action grants and22ft movement, incoming totem destruction/incapacity/suppression and placement/aura line of effect are explicit upstream conditional premises. External action grants are not authenticated by this module.',
            'Stone placement/HP/AC/capacity/duration/concentration and vent are executed; Stone damage/shove bonuses, other totem profiles, healing and object attack resolution are not claimed executed.',
            'For non-Fate DI7 spells the report executes acquisition and paid casting/vent boundaries, leaving their already separately qualified payload reports distinct. Detect Poison consumes actual source/absence premises and returns only its permitted yes/no.'],
        'remaining':['Compile93 current finite source expectations against actual report histories and preserve all original examples/issues/source objects.',
            'Submit complete7 public/internal exact candidates for actual GPT exact acceptance; no source agreement alone promotes cards.'],
        'shaman9Executed':True,'candidateApproved':False,'full49Fulfilled':False,'humanPlaytest':False,'spellPromotions':0,'newRuleAdoptions':0}
    output.write_bytes(encoded(report)); print(json.dumps({'report':info(output),'checks':len(checks),'histories':len(histories),'shamanExpectationsExecuted':len(coverage)}))


if __name__=='__main__': main()
