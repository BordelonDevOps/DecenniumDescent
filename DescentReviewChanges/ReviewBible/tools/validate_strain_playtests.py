"""Bounded source/transition tests for the Strain candidate, not full game validation."""
from pathlib import Path
import hashlib
import json
from strain_playtest_rules import *
from core_playtest_rules import LifeState, healing_ceiling

ROOT=Path(__file__).resolve().parents[1]


def main():
    results=[]
    def check(name,actual,expected):
        results.append({'name':name,'pass':actual==expected,'actual':actual,'expected':expected})
    def rejects(name,operation):
        try:
            operation()
        except SpellRuleError:
            check(name,True,True)
        else:
            check(name,False,True)
    def points(n):
        return tuple(StrainPoint(f'p{i+1}','test-source') for i in range(n))
    bindings=json.loads((ROOT/'data/playtest/strain_bindings.json').read_text(encoding='utf-8'))
    packet=json.loads((ROOT.parents[1]/'docs/audit/2026-10-08/full-game/STRAIN_SOURCE_BINDINGS.json').read_text(encoding='utf-8'))
    warrior=json.loads((ROOT/packet['warriorPath']).read_text(encoding='utf-8'))
    live_cards={c['id']:c for c in warrior['cards']}
    exact_references=0
    for row in bindings['bindings']:
        source=row['source']
        if source['kind']=='engine':
            actual=warrior['engine'][source['index']]
            match=(actual==source['text'] and hashlib.sha256(actual.encode()).hexdigest()==source['textSha256'])
            expected_track=SERUM
        elif source['kind']=='card':
            actual=live_cards.get(source['card']['id'])
            match=(actual==source['card'] and hashlib.sha256(json.dumps(actual,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==source['sourceObjectSha256'])
            expected_track=SERUM
        elif source['kind']=='core-paragraph':
            original=next(r for r in packet['core']['paragraphs'] if r['paragraph']==source['paragraph'])
            match=(original['text']==source['text'] and hashlib.sha256((ROOT.parents[1]/source['path']).read_bytes()).hexdigest()==source['bookSha256'])
            expected_track=EXPEDITION
        elif source['kind']=='campaign-reference':
            match=hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256']
            expected_track=EXPEDITION
        else:
            match=False
            expected_track=None
        check('Exact reference and namespace: '+row['sourceId'],bool(match and row['trackId']==expected_track and row['role']=='namespace-reference'),True)
        exact_references+=1
    lookup={r['sourceId']:r['trackId'] for r in bindings['bindings']}
    check('Binding IDs unique',len(lookup),len(bindings['bindings']))
    check('Quickglass crash explicitly binds expedition',bind_strain('core.quickglass.crash',lookup),EXPEDITION)
    check('Treatment Critical Failure binds patient expedition track',bind_strain('recovery.wound-treatment.critical-failure',lookup),EXPEDITION)
    check('Serum Sharing reference binds recipient serum track',bind_strain('warrior.hero.wardborn.serum-sharing',lookup),SERUM)
    check('Serum Tolerance references serum track without granting immunity',bind_strain('warrior.base.serum-tolerance',lookup),SERUM)
    rejects('Ambiguous future Strain immunity cannot infer namespace',lambda:bind_strain('future.strain-immunity',lookup))
    rejects('Global Exhaustion source is not silently converted',lambda:bind_strain('core.exhaustion',lookup))

    state=StrainState(serum=3,points=points(2))
    automatic=serum_gain(state,1)
    check('Automatic serum overflow clamps independently',(automatic.serum,automatic.expedition),(3,2))
    rejects('Voluntary overcap cost cannot be clipped',lambda:serum_gain(StrainState(serum=2),2,explicit_overcap_illegal=True))
    reduced=serum_gain(StrainState(serum=2),2,reduction=1,minimum_gain=1,explicit_overcap_illegal=True)
    check('Legal gain modifier applies before voluntary cap check',reduced.serum,3)
    minimum=serum_gain(StrainState(),2,reduction=10,minimum_gain=1,explicit_overcap_illegal=True)
    check('Cocktail/Overload minimum gain remains1',minimum.serum,1)
    rejects('Activation lock persists even for zero computed gain',lambda:serum_gain(StrainState(serum=3),1,reduction=1,activation_locked=True))
    check('Sharing recipient at3 accepts clamped attempted gain',serum_gain(StrainState(serum=3),1).serum,3)

    alive=LifeState(20,12)
    s,hp,event=expedition_gain(StrainState(serum=3,points=points(5)),alive,1,event_id='six',source_id='ordinary')
    check('Sixth ordinary expedition point causes death',(hp.dead,hp.hp,s.expedition,s.serum),(True,0,6,3))
    check('Death endpoint report preserves attempted gain',event,{'attempted':1,'added':1,'endpoint':'death'})
    s,hp,event=expedition_gain(StrainState(points=points(5)),alive,1,event_id='collapse',source_id='explicit-nonlethal',nonlethal_source=True)
    check('Explicit nonlethal source preserves HP without granting Stable',(s.collapsed,hp.hp,hp.stable,hp.dead),(True,12,False,False))
    original=s
    s,hp,event=expedition_gain(s,hp,1,event_id='overflow',source_id='ordinary')
    check('Already collapsed6 can die from later ordinary overflow',(s.expedition,hp.dead,event['added']),(6,True,0))
    rejects('Nonlethal gain cannot revive dead creature',lambda:expedition_gain(s,hp,1,event_id='revive',source_id='nonlethal',nonlethal_source=True))
    s,hp,event=expedition_gain(original,alive,1,event_id='blocked',source_id='ordinary',prevented=True)
    check('Prevented overflow does not trigger death',(s.expedition,hp.dead,event['endpoint']),(6,False,'none'))
    rejects('Resolved gain event cannot replay',lambda:expedition_gain(s,hp,1,event_id='blocked',source_id='ordinary'))
    s,hp,event=expedition_gain(StrainState(points=points(5)),LifeState(20,0,death_failures=1),1,event_id='dying-collapse',source_id='nonlethal',nonlethal_source=True)
    check('Collapse leaves independent dying state and counters intact',(hp.hp,hp.stable,hp.death_failures,s.collapsed),(0,False,1,True))
    rejects('Point ID collision cannot duplicate record',lambda:expedition_gain(StrainState(points=(StrainPoint('event:1','old'),)),alive,1,event_id='event',source_id='new'))
    s,hp,event=expedition_gain(StrainState(),alive,20,event_id='large',source_id='ordinary')
    check('Large gain stores no seventh point',(s.expedition,event['attempted'],event['added'],hp.dead),(6,20,6,True))

    p=track_penalties(30,serum=2,expedition=2,exhaustion=2)
    check('Independent flat Speed reductions precede Exhaustion half',p['speed'],7)
    check('Source-correct expedition2 already penalizes attacks',p['attackModifier'],-1)
    check('Source-correct expedition2 already penalizes saves',p['saveModifier'],-1)
    check('Serum3 and expedition2 save penalties both apply',track_penalties(30,serum=3,expedition=2)['saveModifier'],-2)
    check('Mutation Adaptation ignores only serum Speed penalty',track_penalties(30,serum=3,expedition=2,ignore_serum_speed=True)['speed'],20)
    p=track_penalties(30,serum=0,expedition=5)
    check('Expedition5 blocks tactical movement without rewriting Speed',(p['speed'],p['incapacitated'],p['tacticalVoluntaryMovementAllowed']),(20,True,False))
    check('Expedition5 supplies one slow-travel multiplier',p['slowTravelMultiplier'],Fraction(1,2))
    check('Exhaustion5 separately sets Speed0',track_penalties(30,serum=0,expedition=2,exhaustion=5)['speed'],0)
    check('MaximumHP multiplies exact factors and floors once',combined_maximum_hp(100,expedition=4,exhaustion=4),37)
    check('Combined maximum has floor1',combined_maximum_hp(1,expedition=4,exhaustion=4),1)
    hp=apply_effective_maximum(LifeState(100,100,wounds=(None,None,None)),37)
    check('MaxHP clamp changes no Wounds',(hp.hp,hp.maximum_hp,len(hp.wounds)),(37,37,3))
    check('Critical healing ceiling applies after effective maximum',healing_ceiling(hp),36)
    hp=apply_effective_maximum(hp,100)
    check('Restoring maximum capacity does not heal',hp.hp,37)
    corpse=apply_effective_maximum(LifeState(100,0,dead=True),37)
    check('Maximum change cannot revive dead state',(corpse.dead,corpse.hp),(True,0))
    dying=apply_effective_maximum(LifeState(100,0,death_failures=2),37)
    check('Maximum change does not reset dying counters',dying.death_failures,2)
    invariant_states=0
    for base in range(1,102):
        for expedition in range(7):
            for exhaustion in range(7):
                maximum=combined_maximum_hp(base,expedition=expedition,exhaustion=exhaustion)
                old=LifeState(base,base)
                once=apply_effective_maximum(old,maximum)
                twice=apply_effective_maximum(once,maximum)
                restored=apply_effective_maximum(twice,base)
                assert 1<=maximum<=base and once.hp==twice.hp==restored.hp
                assert not once.wounds and not once.dead
                invariant_states+=1

    lock=ExpeditionDashLock()
    check('Own-turn Dash excludes current end3 and locks through9',lock.dash(3,1,in_initiative=True,end_marker_phase=3,excluded_current_end=3),9)
    rejects('Second same-turn Dash blocked',lambda:lock.dash(3,2,in_initiative=True,end_marker_phase=3,excluded_current_end=3))
    lock.reconcile(3,6)
    check('Round/extra-turn time before original endpoint does not clear',lock.until,9)
    lock.reconcile(3,9)
    check('Original next-turn end clears lock',lock.until,None)
    off=ExpeditionDashLock()
    check('Off-turn Dash locks through upcoming own regular end',off.dash(3,4,in_initiative=True,end_marker_phase=3),9)
    off.reconcile(3,8)
    check('Leaving initiative preserves original shorter remaining time',off.until,9)
    outside=ExpeditionDashLock()
    check('Out-of-initiative Dash records absolute six-second endpoint',outside.dash(3,4,in_initiative=False),10)
    outside.reconcile(3,9)
    check('Entering initiative does not reanchor outside lock',outside.until,10)
    outside.reconcile(2,9)
    check('Dropping below3 clears lock',outside.until,None)
    check('Returning to3 permits one new Dash',outside.dash(3,9,in_initiative=False),15)
    rejects('Expedition5 forbids Dash even if unlocked',lambda:ExpeditionDashLock().dash(5,0,in_initiative=False))

    gated=StrainState(points=(StrainPoint('free','ordinary'),StrainPoint('gate','illness',True,False),StrainPoint('special','curse',False,True)))
    recovered,removed=ordinary_recovery(gated,'haven')
    check('Haven removes only ordinary ungated points',(removed,[p.point_id for p in recovered.points]),(['free'],['gate','special']))
    rejects('Cannot choose blocked point for ordinary one-point cure',lambda:ordinary_recovery(gated,'long',selected_point='gate'))
    recovered,removed=ordinary_recovery(original,'long',selected_point='p1')
    check('Nonlethal collapsed6 cannot use generic Long Rest reduction',(recovered.expedition,removed),(6,[]))
    recovered,removed=ordinary_recovery(original,'haven')
    check('Eligible Haven care lowers below6 and ends only own collapse',(recovered.expedition,recovered.collapsed),(0,False))
    all_gated=StrainState(points=tuple(StrainPoint(f'b{i}','locked',True,False) for i in range(6)),collapsed=True)
    recovered,removed=ordinary_recovery(all_gated,'haven')
    check('All six blocked points keep collapse through Haven care',(recovered.expedition,recovered.collapsed),(6,True))

    history=RestHistory()
    state=StrainState(serum=3,points=points(4))
    state,event=history.complete(state,identity='short1',kind='short',start=0,end=3600,rest_debt=True)
    check('Serum Short Rest reduction does not remove expedition points',(state.serum,state.expedition,event['restDebt']),(2,4,True))
    state,event=history.complete(state,identity='short2',kind='short',start=3600,end=7200)
    state,event=history.complete(state,identity='short3',kind='short',start=7200,end=10800)
    check('Third Short Rest gives no extra serum recovery',(state.serum,history.short_count,event['beneficial']),(1,2,False))
    state,event=history.complete(state,identity='long1',kind='long',start=10800,end=39600,secure=True,rest_debt=True,selected_point='p1')
    check('Same safe RestWatch pays debt before its own reduction',(state.serum,state.expedition,event['restDebt']),(0,3,False))
    check('Beneficial Long Rest resets short-rest count',history.short_count,0)
    state=serum_gain(state,2)
    state,event=history.complete(state,identity='long-no-reward',kind='long',start=39600,end=68400,secure=True,rest_debt=True,selected_point='p2')
    check('Extra RestWatch clears debt but grants no second long reward',(state.serum,state.expedition,event['restDebt'],event['beneficial']),(2,3,False,False))
    check('Nonbeneficial watch does not move beneficial Long Rest clock',history.last_long_end,39600)
    rejects('Rest completion ID cannot replay',lambda:history.complete(state,identity='long1',kind='long',start=68400,end=97200))
    state,event=history.complete(state,identity='long2',kind='long',start=97200,end=126000,secure=True,selected_point='p2')
    check('Exactly24h between Long Rest completions permits benefit',(state.serum,state.expedition,event['beneficial']),(0,2,True))
    rejects('Activity overlap cannot grant repeat recovery',lambda:history.complete(state,identity='overlap',kind='morale',start=125000,end=140000,selected_point='p3'))
    rejects('Backdated completion cannot reset histories',lambda:history.complete(state,identity='backdated',kind='short',start=0,end=3600))

    care=RestHistory()
    state=StrainState(serum=3,points=points(4))
    state,event=care.complete(state,identity='recreation',kind='morale',start=0,end=14400,selected_point='p1')
    state,event=care.complete(state,identity='sleep',kind='long',start=14400,end=43200,secure=True,selected_point='p2')
    check('Separate Morale and secure Long Rest remove2 expedition points',(state.serum,state.expedition),(0,2))
    state,event=care.complete(state,identity='care-day',kind='haven',start=0,end=86400)
    check('Haven location-care window may contain distinct sleep/recreation',state.expedition,0)
    rejects('Two overlapping Haven windows cannot double-pay',lambda:care.complete(state,identity='overlap-care',kind='haven',start=43200,end=129600))

    interrupted=RestHistory()
    state,event=interrupted.complete(StrainState(points=points(2)),identity='broken-care',kind='haven',start=0,end=23*3600,interrupted=True)
    check('Interrupted23h care removes nothing',(state.expedition,event['beneficial']),(2,False))
    state,event=interrupted.complete(state,identity='restarted-care',kind='haven',start=23*3600,end=47*3600)
    check('Fresh complete24h care after interruption works',state.expedition,0)
    blocked=RestHistory()
    state,event=blocked.complete(StrainState(serum=3,points=points(2)),identity='food-block',kind='long',start=0,end=28800,secure=True,food_water=False,selected_point='p1')
    check('Persistent food/water block prevents expedition reduction',state.expedition,2)
    invalid=RestHistory()
    state,event=invalid.complete(StrainState(points=points(2)),identity='not-rest',kind='long',start=0,end=28800,safe=True,eligible_activity=False,rest_debt=True)
    check('Non-rest activity cannot pay Rest Debt merely by lasting8h',event['restDebt'],True)

    failures=[r['name'] for r in results if not r['pass']]
    report={'status':'FAIL' if failures else 'PASS','reviewStatus':bindings['status'],
            'scope':'Supplied Strain namespaces, selected cap/HP/Dash/recovery transitions and source metadata. Not full rest, travel, class, inventory or condition dispatch.',
            'namespaceBindings':len(lookup),'exactSourceReferences':exact_references,'checks':len(results),'transitionChecks':len(results)-exact_references,'maximumHpInvariantStates':invariant_states,
            'failures':failures,'results':results,
            'artifacts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'tools/strain_playtest_rules.py',ROOT/'docs/mechanics/STRAIN_PLAYTEST.md',ROOT/'data/playtest/strain_bindings.json']}}
    (ROOT/'docs/mechanics/STRAIN_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2,default=str)+'\n',encoding='utf-8')
    print(f"{report['status']}: {len(results)} checks; {invariant_states} maximumHP invariant states; {len(lookup)} namespace bindings; {bindings['status']}")
    for name in failures:
        print('FAIL:',name)
    if failures:
        raise SystemExit(1)


if __name__=='__main__':
    main()
