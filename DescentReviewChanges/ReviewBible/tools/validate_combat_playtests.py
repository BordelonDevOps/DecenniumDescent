"""Adversarial checks for the bounded combat reference, not a full game engine."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
from combat_playtest_rules import *
from core_playtest_rules import LifeState, task_check, opposed_check

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

    clock=ReactionClock()
    clock.spend()
    check('Initial reaction can be spent before first regular turn',clock.available,False)
    clock.regular_start(0)
    clock.spend()
    check('First regular start refreshes despite same numbered round',clock.available,False)
    clock.round_boundary()
    clock.extra_turn()
    check('Neither round boundary nor extra turn refreshes Reaction',clock.available,False)
    rejects('Repeated regular marker cannot refresh twice',lambda:clock.regular_start(0))
    surprised=ReactionClock(surprise_pending=True)
    surprised.regular_start(0)
    rejects('Surprised first turn refresh does not permit Reaction',surprised.spend)
    surprised.end_first_regular_turn()
    surprised.spend()
    check('Surprise ending unlocks one available Reaction',surprised.available,False)
    extra=ExtraActionClock()
    extra.spend(1)
    rejects('Second extra full Action in same numbered round rejected',lambda:extra.spend(1))
    rejects('Extra Action cannot recursively grant another',lambda:extra.spend(2,granted_by_extra_action=True))
    extra.spend(2)
    check('New numbered round allows a separately granted extra Action',extra.spent_rounds,{1,2})
    check('Midround entrant with upcoming slot acts now',reinforcement_first_round(3,slot_still_upcoming=True),3)
    check('Exact/passed slot entrant waits until next round',reinforcement_first_round(3,slot_still_upcoming=False),4)
    check('End-round entry always first acts next round',reinforcement_first_round(3,slot_still_upcoming=True,end_round_entry=True),4)

    move=MovementLedger()
    move.spend(movement_cost(10,'difficult'),30)
    check('Difficult terrain cost retained on switch to Fly30',move.remaining(30),10)
    move.dash()
    check('First legal Dash adds another current Speed',move.remaining(30),40)
    move.dash()
    check('Second legal Dash adds Speed again',move.remaining(30),70)
    move=MovementLedger()
    move.stand(30)
    check('Standing expenditure is retained on switching modes',move.remaining(30),15)
    move=MovementLedger(spent=20)
    check('Speed reduction does not create negative remaining budget',move.remaining(15),0)
    check('Restored Speed restores only genuinely unspent budget',move.remaining(30),10)
    check('Speed increase expands cap without refunding spent cost',move.remaining(40),20)
    rejects('Over-budget movement is rejected',lambda:move.spend(11,30))
    check('Rejected movement leaves ledger unchanged',move.spent,20)
    rejects('Cannot stand at Speed0',lambda:move.stand(0))
    check('Crawl and squeeze in difficult terrain add costs',movement_cost(5,'difficult',crawling=True,squeezing=True),20)
    check('Severe plus crawling costs4 per foot',movement_cost(5,'severe',crawling=True),20)
    check('Interpose5 cannot enter difficult tile costing10',can_special_move('interpose',30,5,'difficult'),False)
    check('Press5 can follow one normal tile',can_special_move('press',30,5),True)
    check('Speed0 blocks positive special movement',can_special_move('press',0,5),False)
    check('Interpose may stay in place at Speed0 if legally positioned',can_special_move('interpose',0,0),True)
    check('Ready movement uses current Speed at release',special_movement_budget('ready',20),20)
    check('Withdraw odd Speed uses floor half budget',special_movement_budget('withdraw',25),12)
    check('Separate movement grant leaves ordinary ledger unchanged',move.spent,20)

    # Independent invariant: mode changes cannot reduce the paid-cost ledger.
    movement_states=0
    for spent in range(0,91,5):
        for speed in (0,5,15,30,60):
            for dashes in (0,1,2):
                m=MovementLedger(spent,dashes)
                old_spent=m.spent
                cap=(1+dashes)*speed
                remaining=m.remaining(speed)
                assert remaining>=0 and remaining<=cap
                assert remaining+spent==max(cap,spent)
                m.remaining(0)
                m.remaining(60)
                assert m.spent==old_spent
                movement_states+=1

    check('Two future target ends count two preserved markers',marker_deadline(1,3,2),9)
    check('Current in-progress target end excluded from two-turn duration',marker_deadline(1,3,2,excluded_current_marker=3),15)
    check('Three-round self effect during turn1 expires at turn4 start',marker_deadline(Fraction(1,2),0,3),18)
    check('Exact application/start tie means next future start',marker_deadline(0,0,1),6)
    check('Explicit next-turn end excludes current in-progress end',marker_deadline(1,3,1,excluded_current_marker=3),9)
    check('Application after excluded end does not skip another marker',marker_deadline(4,3,excluded_current_marker=3),9)
    check('Exact end-marker application does not skip twice',marker_deadline(3,3,excluded_current_marker=3),9)
    deadline=marker_deadline(1,3,2)
    check('Leaving initiative preserves original absolute marker deadline',deadline,9)
    check('Out-of-initiative duration remains absolute through entry',absolute_duration(2,3),20)
    check('Readied three-round elapsed effect starts at release',ready_effect_deadline(0,4,3),22)
    check('Readied target-marker duration counts future markers from release',ready_effect_deadline(1,4,3,marker_phase=3),21)
    rejects('Effect cannot release before its preparation',lambda:ready_effect_deadline(4,1,3))

    ready=ReadyController(10,concentration='old-spell')
    ready.prepare('held','spell',rp_cost=3)
    check('Ordinarily nonconcentration held spell replaces old concentration',ready.concentration,'held')
    check('Readied spell pays RP and casts at preparation', (ready.rp,ready.cast_events),(7,1))
    rx=ReactionClock()
    check('Illegal release leaves pending spell and Reaction intact',ready.release(rx,trigger_matches=True,legal_target=False),None)
    check('Invalid release does not refund or repay', (ready.rp,ready.pending['id'],rx.available),(7,'held',True))
    out=ready.release(rx,trigger_matches=True)
    check('Nonconcentration spell releases holding concentration',(out['id'],ready.concentration),('held',None))
    check('Release consumes Reaction but does not recast',(rx.available,ready.rp,ready.cast_events),(False,7,1))
    check('No second release from consumed Ready',ready.release(ReactionClock(),trigger_matches=True),None)
    ready.prepare('sustained','spell',rp_cost=2,ongoing_concentration=True)
    ready.release(ReactionClock(),trigger_matches=True)
    check('Concentration spell continues seamlessly after release',ready.concentration,'sustained')
    ready.prepare('discarded','spell',rp_cost=1)
    ready.prepare('replacement','attack',ordinary_attack_count=2)
    check('Replacing held spell loses costs and held concentration',(ready.rp,ready.concentration),(4,None))
    attacks=ready.release(ReactionClock(),trigger_matches=True)
    check('Readied ordinary Attack retains legal multiple attacks',attacks['attacks'],2)
    ready.prepare('expired','spell',rp_cost=1)
    ready.cancel()
    check('Ready expiry loses held spell without refund',(ready.pending,ready.rp,ready.concentration),(None,3,None))
    rejects('Cannot Ready a Bonus Action spell',lambda:ready.prepare('bad','spell',activation='Bonus Action'))
    check('Failed prepare does not charge setup action',ready.setup_actions,5)
    ready.prepare('lost','spell',rp_cost=1)
    ready.lose_concentration()
    check('Lost concentration loses held spell and costs',(ready.pending,ready.rp),(None,2))
    ready.prepare('wait','attack')
    spent_rx=ReactionClock(available=False)
    check('Used Reaction prevents Ready release',ready.release(spent_rx,trigger_matches=True),None)
    check('Unreleased action remains pending',ready.pending['id'],'wait')
    check('Focused Reaction restriction also blocks ordinary Ready release',ready.release(ReactionClock(),trigger_matches=True,reaction_prohibited=True),None)
    check('Blocked Ready release retains its pending state',ready.pending['id'],'wait')

    guard=GuardState()
    guard.activate()
    check('Guard and Guarded combine for first attack',guard.attacked(guarded_stance=True),3)
    check('Miss also consumes Guard first-attack benefit',guard.attacked(guarded_stance=True),1)
    check('Spent first-attack bonus preserves Interpose Guard state',guard.active,True)
    guard.end()
    check('Break Formation/end clears Guard state',guard.active,False)
    press=PressState()
    press.arm('A',own_regular_turn=True,qualifying_melee_hit=True)
    press.arm('B',own_regular_turn=True,qualifying_melee_hit=True)
    check('Unspent Press can change target',press.target,'B')
    check('Forced retreat cannot trigger Press',press.follow('B',voluntary_retreat=False,legal_movement=True),False)
    check('Legal voluntary retreat consumes Press',press.follow('B',voluntary_retreat=True,legal_movement=True),True)
    rejects('Cannot rearm spent Press on same regular turn',lambda:press.arm('A',own_regular_turn=True,qualifying_melee_hit=True))
    rejects('Extra turn cannot arm fresh Press',lambda:PressState().arm('A',own_regular_turn=False,qualifying_melee_hit=True))
    check('Multiple Pins use single penalty and highest DC',pin_state([{'dc':12},{'dc':16}]),{'speedPenalty':10,'dc':16})
    check('Suppressed Pin does not raise effective DC',pin_state([{'dc':12},{'dc':16,'suppressed':True}]),{'speedPenalty':10,'dc':12})
    check('Silence hit at zero damage forces one DC10 concentration save',silence_concentration(0,concentrating=True),{'saves':1,'dc':10})
    check('Silence positive damage produces one concentration save',silence_concentration(31,concentrating=True),{'saves':1,'dc':15})
    check('No concentration means no gratuitous concentration check',silence_concentration(31,concentrating=False),{'saves':0,'dc':None})
    check('Opposed Grapple tie preserves state',opposed_check(15,3,12,6)['changesState'],False)
    attempts=ManeuverAttempts()
    attempts.regular_start(0)
    check('Legal Pin attempt charges accuracy before hit outcome',attempts.declare_and_roll('pin'),-2)
    rejects('A miss still consumes Pin interval token',lambda:attempts.declare_and_roll('pin'))
    attempts.extra_turn()
    attempts.round_boundary()
    rejects('Extra turn and numbered-round boundary do not refresh attempt',lambda:attempts.declare_and_roll('pin'))
    check('Independent unused Silence token works on legal off-turn attack',attempts.declare_and_roll('silence-the-caster'),-2)
    attempts.regular_start(1)
    check('Regular start refreshes both maneuver tokens',attempts.used,set())
    rejects('Illegal attack consumes no maneuver token',lambda:attempts.declare_and_roll('pin',legal_attack=False))
    check('Illegal declaration retains token',attempts.used,set())
    rejects('Cannot add another optional maneuver to same attack',lambda:attempts.declare_and_roll('pin',other_optional_maneuver=True))
    check('Unspent interval token works on legal readied attack',attempts.declare_and_roll('pin'),-2)
    rejects('Repeated regular marker cannot reset spent attempt',lambda:attempts.regular_start(1))
    check('Mobile steps base dice only and keeps d4 floor',mobile_base_dice([6,6,4]),[4,4,4])

    observers=[{'id':'A','canAttemptHide':True,'perceptionModifier':4},
               {'id':'B','canAttemptHide':True,'perceptionModifier':8},
               {'id':'C','canAttemptHide':False,'perceptionModifier':0}]
    check('One Hide roll resolves observer DCs and eligibility separately',hide_results(10,4,observers),{'A':True,'B':False,'C':False})
    check('Natural1 shifts meet-DC Hide to failure',hide_results(1,13,observers)['A'],False)
    check('Natural20 may lift below-DC result to success',hide_results(20,-3,observers)['B'],True)
    check('Search static-DC tie succeeds before natural adjustment',task_check(10,4,14)['success'],True)
    check('Search natural1 can downgrade static-DC success',task_check(1,13,14)['success'],False)
    check('Cover uses best value, never adds2and5',best_cover(['half','three-quarters']),{'directTargetLegal':True,'bonus':5})
    check('Total cover from actual origin bars target',best_cover(['half','total'])['directTargetLegal'],False)
    check('Normal range boundary legal without range disadvantage',ranged_range(60,60,120),{'legal':True,'disadvantage':False})
    check('Long range boundary legal with disadvantage',ranged_range(120,60,120),{'legal':True,'disadvantage':True})
    check('Beyond long range illegal',ranged_range(125,60,120)['legal'],False)
    oa=dict(seen=True,hostile=True,voluntary=True,exits_reach=True)
    check('Seen voluntary exit provokes',opportunity_trigger(**oa),True)
    check('Forced exit does not provoke',opportunity_trigger(**dict(oa,voluntary=False)),False)
    check('Teleport does not provoke',opportunity_trigger(**oa,teleported=True),False)
    check('Disengage prevents ordinary opportunity trigger',opportunity_trigger(**oa,disengaged=True),False)
    check('Unseen exit does not provoke ordinary opportunity attack',opportunity_trigger(**dict(oa,seen=False)),False)

    def effect(identity,kind,amount,order=0,**opts):
        return {'applicationId':identity,'mechanicalId':identity,'appliedAt':0,
                'applicationSequence':order,'kind':kind,'amount':amount,'damageOptions':opts}
    s,log=start_life_sequence(LifeState(20,0),regular_turn_id=1,now_seconds=6,death_natural=5,effects=[effect('heal','heal',4)])
    check('Dying death save precedes ordinary start healing',log,['death-save','heal'])
    check('Later start healing restores HP and clears failed death save',(s.hp,s.death_failures),(4,0))
    s,log=start_life_sequence(LifeState(20,0,death_failures=2),regular_turn_id=1,now_seconds=6,death_natural=5,effects=[effect('heal','heal',4)])
    check('Fatal death save cannot be reversed by later ordinary healing',(s.dead,log),(True,['death-save','heal:dead-target-skipped']))
    s,log=start_life_sequence(LifeState(20,0,stable=True,stable_until_seconds=3600),regular_turn_id=1,now_seconds=6,effects=[effect('bleed','damage',1)])
    check('Stable victim skips death save before start damage',(log,s.stable,s.death_failures),(['bleed'],False,1))
    s,log=start_life_sequence(LifeState(20,0),regular_turn_id=1,now_seconds=6,death_natural=20,effects=[effect('bleed','damage',1,wound_natural=20)])
    check('Natural20 then Bleed is new drop not already-zero failure',(s.hp,s.death_failures,log),(0,0,['death-save','bleed']))
    stable=LifeState(20,0,stable=True,stable_until_seconds=5)
    s,log=start_life_sequence(stable,regular_turn_id=1,now_seconds=6,hp_prohibited=True,prohibition_expires=True)
    check('Expired prohibition permits due Stable recovery before death phase',(s.hp,log),(1,['due-stable-recovery']))
    s,log=start_life_sequence(stable,regular_turn_id=1,now_seconds=6,hp_prohibited=True)
    check('Still-blocked Stable timer retains original deadline',(s.hp,s.stable_until_seconds,log),(0,5,[]))
    healing=effect('first-heal','heal',2,0)
    damage=effect('later-damage','damage',3,1,wound_natural=20)
    s,log=start_life_sequence(LifeState(20,1),regular_turn_id=1,now_seconds=6,effects=[damage,healing])
    check('Application sequence overrides caller list order',log,['first-heal','later-damage'])
    check('Start effect newly dropping to0 does not add second start save',(s.hp,s.last_death_turn),(0,0))
    rejects('Duplicate application cannot dispatch twice',lambda:ordered_effects([healing,healing]))

    failed=[r['name'] for r in results if not r['pass']]
    report={'status':'FAIL' if failed else 'PASS','reviewStatus':'REVIEWED / reference-VALIDATED in supplied bounded scope',
            'scope':'Selected combat reference budgets, marker calculations, Ready state and HP ordering. Not a full engine, all-source semantic audit or balance test.',
            'checks':len(results),'movementInvariantStates':movement_states,'failed':failed,'results':results,
            'artifacts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'tools/combat_playtest_rules.py',ROOT/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md']}}
    (ROOT/'docs/mechanics/COMBAT_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2,default=lambda v:sorted(v) if isinstance(v,set) else str(v))+'\n',encoding='utf-8')
    print(f"{report['status']}: {len(results)} checks; {movement_states} movement-cost invariant states")
    for name in failed:
        print('FAIL:',name)
    if failed:
        raise SystemExit(1)


if __name__=='__main__':
    main()
