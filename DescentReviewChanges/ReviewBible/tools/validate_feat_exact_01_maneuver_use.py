"""Execute all six maneuver transactions with actual paid feat selections."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from core_playtest_rules import LifeState, damage_event
from feat_exact_01_fixed_menus import FixedMenus
from feat_exact_01_casting_credential_model import CastingSources
from feat_exact_01_maneuver_use import ManeuverUse, PREFIX
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT_EXACT_01_MANEUVERS_USE_CHECK.json'; notes = A / 'FEAT_EXACT_01_MANEUVERS_USE_NOTES.md'
    assert not output.exists() and not notes.exists()
    paths = [Path(__file__), R / 'tools/feat_exact_01_maneuver_use.py',
        R / 'tools/feat_exact_01_fixed_menus.py', R / 'tools/feat_exact_01_remaining_owned_chains.py',
        R / 'tools/feat_exact_01_composite_casting_model.py', R / 'tools/feat_exact_01_casting_credential_model.py',
        R / 'tools/feat_exact_01_training_prerequisite_model.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'tools/feat_exact_01_initiate_acquisition_model.py', R / 'tools/core_playtest_rules.py',
        R / 'tools/combat_playtest_rules.py', R / 'tools/custom_condition_rules.py', R / 'tools/spell_playtest_rules.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/class_playtests/wizard.json',
        R / 'data/public/feat_candidates/exact_01/spell_dependencies.json',
        R / 'data/public/feat_candidates/exact_01/supplements.json', R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R / 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md']
    bindings = [info(p) for p in paths]
    foundation = read(paths[13]); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, names in foundation['skillAbilities'].items() for s in names}
    ancestry = read(paths[14]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[15])['records']}
    supplements = {x['id']: x['value'] for x in read(paths[18])['groups']}
    sources = CastingSources(G, read(paths[17])['spells'], supplements, read(paths[16]))
    contracts = {x['id']: x for x in read(paths[20])['records']}
    actor = deepcopy(read(paths[21])['actorSourceProjection'])
    actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
    menu = [x['id'] for x in supplements['SUP-03']]
    world = {'actors': {
        'owner': {'position': 0, 'size': 2, 'armorClass': 15, 'modes': {'walk': 30}, 'canAct': True, 'canReact': True,
            'reactionAvailable': True, 'ordinaryMovementSpent': 10, 'disengaged': False, 'ally': True, 'perceivesRally': True,
            'fear': [{'id': 'self-fear', 'condition': 'Frightened', 'active': True, 'sourceDC': 12}]},
        'enemy': {'position': 5, 'size': 3, 'armorClass': 16, 'ally': False, 'prone': False,
            'opposedModifiers': {'Athletics': 4, 'Acrobatics': 5}, 'reactionAvailable': True, 'canSeeOwner': True},
        'ally': {'position': 25, 'size': 2, 'armorClass': 12, 'ally': True, 'perceivesRally': True,
            'fear': [{'id': 'fear-A', 'condition': 'Frightened', 'active': True, 'sourceDC': 14},
                     {'id': 'fear-B', 'condition': 'Frightened', 'active': True, 'sourceDC': 12}]}},
        'items': {'owner-sword': {'heldBy': 'owner', 'owner': 'owner', 'attunedTo': None,
                                'profile': 'martial-melee-weapons.longsword', 'droppable': True, 'position': 0},
                  'enemy-blade': {'heldBy': 'enemy', 'owner': 'enemy', 'attunedTo': 'enemy',
                                  'profile': 'martial-melee-weapons.longsword', 'droppable': True,
                                  'magical': True, 'cursed': True, 'position': 5}}, 'walls': []}
    packet = {'id': 'incoming-root', 'kind': 'direct-damage', 'recipient': 'owner',
        'stage': 'after-passive-before-tempHP', 'recipientMitigationAllowed': True, 'originalHit': True,
        'components': [{'type': 'cold', 'amount': 4}, {'type': 'slashing', 'amount': 5}],
        'attachedConditions': ['conditional-frightened'], 'sourceRoot': 'conditional-hostile-source'}
    checks = []; traces = []

    def check(label, value):
        checks.append({'id': label, 'passed': bool(value)})
        if not value: raise AssertionError(label)

    def acquire(kind, advanced=False):
        h = FixedMenus(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        identity = PREFIX + kind; chosen = [identity] + [x for x in menu if x != identity][:1]
        h.advance(4); h.earn(4); h.acquire_menu('martialAdept', 4, chosen)
        if advanced:
            h.advance(8); h.earn(8); h.acquire_menu('martial_adept_advanced', 8, [x for x in menu if x not in chosen][:2])
        return ManeuverUse(h, world)

    def declare(m, kind, event='attempt', **overrides):
        kwargs = {
            'measured-strike': {'target': 'enemy', 'item': 'owner-sword'},
            'driving-shove': {'target': 'enemy', 'mode': 'push'},
            'disarming-feint': {'target': 'enemy', 'item': 'enemy-blade', 'style': 'Athletics'},
            'guarding-deflection': {'packet': packet},
            'measured-advance': {'mode': 'walk'},
            'rallying-signal': {'target': 'ally', 'fear': 'fear-A'}}[kind]
        kwargs.update(overrides)
        return m.declare(PREFIX+kind, event, **kwargs)

    def ready(kind, advanced=False):
        m = acquire(kind, advanced)
        if kind in {'measured-strike', 'driving-shove', 'disarming-feint'}: m.begin_attack_action()
        return m

    def reject(label, m, operation):
        before = m.snapshot()
        try: operation()
        except ValueError as error: checks.append({'id': label, 'passed': True, 'reason': str(error)})
        else: check(label, False)
        check(label + '/unchanged', before == m.snapshot())

    def record(label, before, m, **extra):
        traces.append({'id': label, 'before': before, 'after': m.snapshot(), **extra})

    check('six-complete-source-maneuvers', len(menu) == 6 and all(x['procedure'] and x['activation'] and x['cost'] for x in supplements['SUP-03']))
    for kind in [x.removeprefix(PREFIX) for x in menu]:
        for face in range(1, 7):
            m = ready(kind); before = m.snapshot(); event = declare(m, kind)
            check(kind+str(face)+'/committed-before-outcome', m.pool['current'] == 0 and event['status'] == 'committed-before-rolls' and 'die' not in m.events['attempt'])
            m.roll_die('attempt', face)
            if kind == 'measured-strike':
                result = m.resolve('attempt', actor_die=10)
                check(kind+str(face)+'/exact-attack-addition', result == {'total': 15+face, 'hit': True, 'critical': False, 'damageBonus': 0, 'additionalAttackGranted': False})
            elif kind in {'driving-shove', 'disarming-feint'}:
                result = m.resolve('attempt', actor_die=10, defender_die=10, defender_skill='Athletics', drop=10)
                check(kind+str(face)+'/ordinary-contest', result['actorTotal'] == 15+face and result['defenderTotal'] == 14 and result['changesState'] and result['damage'] == 0)
                if kind == 'driving-shove': check(kind+str(face)+'/only-push', m.target('enemy')['position'] == 10 and not m.target('enemy')['prone'])
                else: check(kind+str(face)+'/drop-not-custody-or-unbinding', m.world['items']['enemy-blade']['heldBy'] is None and m.world['items']['enemy-blade']['position'] == 10 and m.world['items']['enemy-blade']['owner'] == m.world['items']['enemy-blade']['attunedTo'] == 'enemy' and m.world['items']['enemy-blade']['cursed'])
            elif kind == 'guarding-deflection':
                result = m.resolve('attempt')
                amounts = [x['amount'] for x in result['packet']['components']]
                check(kind+str(face)+'/stable-component-reduction', amounts == [max(0, 4-face), 5-max(0, face-4)] and result['prevented'] == face)
                check(kind+str(face)+'/hit-and-attached-conditions-retained', result['packet']['originalHit'] and result['packet']['attachedConditions'] == packet['attachedConditions'] and not result['riposteParryTrigger'])
            elif kind == 'measured-advance':
                result = m.resolve('attempt')
                m.advance_step('attempt', -5, opportunity_outcome='decline'); m.finish_advance('attempt')
                check(kind+str(face)+'/separate-budget-not-speed-refill', result['separateMovementCostBudget'] == 5*face and m.actor['position'] == -5 and m.actor['ordinaryMovementSpent'] == 10 and m.events['attempt']['discardedDistance'] == 5*(face-1))
            else:
                result = m.resolve('attempt', actor_die=10)
                check(kind+str(face)+'/source-DC-and-one-fear-record', result['total'] == 13+face and result['success'] and not m.target('ally')['fear'][0]['active'] and m.target('ally')['fear'][1]['active'])
            check(kind+str(face)+'/cost-not-refunded-or-RP-created', m.pool['current'] == 0 and classes['Warrior']['rpByClassLevel'][3] == 0)
            record(kind+'/'+str(face), before, m, result=result)

    for natural, ac, hit, critical in [(1, 1, False, False), (20, 100, True, True), (19, 10, True, False), (2, 30, False, False)]:
        m = ready('measured-strike'); m.target('enemy')['armorClass'] = ac; before=m.snapshot()
        declare(m, 'measured-strike'); m.roll_die('attempt', 6); result=m.resolve('attempt', actor_die=natural)
        check('MeasuredStrike/native-face/'+str(natural), result['hit'] == hit and result['critical'] == critical and m.pool['current'] == 0)
        reject('MeasuredStrike/no-second-resolution/'+str(natural), m, lambda: m.resolve('attempt', actor_die=20))
        record('MeasuredStrike/native-face/'+str(natural), before, m, result=result)

    for kind in ['driving-shove','disarming-feint']:
        m=ready(kind); before=m.snapshot(); declare(m,kind);m.roll_die('attempt',1)
        result=m.resolve('attempt',actor_die=10,defender_die=11,defender_skill='Acrobatics')
        check(kind+'/tie-preserves-state',result['actorTotal']==result['defenderTotal']==16 and not result['changesState'] and m.target('enemy')['position']==5 and m.world['items']['enemy-blade']['heldBy']=='enemy')
        record(kind+'/tie',before,m,result=result)
        m=ready(kind);before=m.snapshot();declare(m,kind);m.roll_die('attempt',1)
        m.target('enemy')['opposedModifiers']['Athletics']=20
        result=m.resolve('attempt',actor_die=20,defender_die=20,defender_skill='Athletics')
        check(kind+'/natural20-does-not-auto-win',not result['changesState'] and m.pool['current']==0)
        record(kind+'/opposed-natural20',before,m,result=result)
    m=ready('driving-shove');before=m.snapshot();declare(m,'driving-shove',mode='prone');m.roll_die('attempt',2)
    m.resolve('attempt',actor_die=12,defender_die=5,defender_skill='Athletics')
    check('Shove-prone-without-push',m.target('enemy')['prone'] and m.target('enemy')['position']==5)
    record('Shove-prone-choice',before,m)
    m=ready('driving-shove');m.world['walls']=[10];before=m.snapshot();declare(m,'driving-shove');m.roll_die('attempt',6)
    result=m.resolve('attempt',actor_die=12,defender_die=5,defender_skill='Athletics')
    check('Shove-stops-at-obstacle-no-reward',m.target('enemy')['position']==5 and not m.target('enemy')['prone'] and m.pool['current']==0)
    record('Shove-blocked-displacement',before,m,result=result)
    for kind,change in [('driving-shove',lambda m:m.target('enemy').update(size=4)),
                        ('disarming-feint',lambda m:m.world['items']['enemy-blade'].update(droppable=False)),
                        ('disarming-feint',lambda m:m.world['items']['enemy-blade'].update(heldBy=None)),
                        ('measured-strike',lambda m:m.target('enemy').update(position=10))]:
        m=ready(kind);change(m);reject(kind+'/invalid-preflight/'+str(len(checks)),m,lambda:declare(m,kind))
    for style in ['save-based-Disarm','Whip-Control']:
        m=ready('disarming-feint');reject('Disarm/separate-route/'+style,m,lambda:declare(m,'disarming-feint',style=style))
    for style in ['Athletics','weapon-check']:
        m=ready('disarming-feint');m.target('enemy')['size']=5;m.world['walls']=[10]
        before=m.snapshot();declare(m,'disarming-feint',style=style);m.roll_die('attempt',6)
        m.resolve('attempt',actor_die=12,defender_die=1,defender_skill='Athletics',drop=5)
        check('Disarm/'+style+'/no-invented-size-cap-own-space-fallback',m.world['items']['enemy-blade']['position']==5 and m.world['items']['enemy-blade']['heldBy'] is None)
        record('Disarm/'+style+'/actual-ordinary-branch',before,m)

    m=ready('guarding-deflection');before=m.snapshot();declare(m,'guarding-deflection');m.roll_die('attempt',6)
    result=m.resolve('attempt');life=LifeState(maximum_hp=100,hp=40,temp_hp=4)
    after,damage_events=damage_event(life,sum(x['amount'] for x in result['packet']['components']))
    check('Guarding-before-tempHP-once',after.hp==40 and after.temp_hp==1 and life.temp_hp==4)
    record('Guarding-Core-tempHP-order',before,m,coreBefore=life.__dict__,coreAfter=after.__dict__,coreEvents=damage_events)
    m=ready('guarding-deflection');small=deepcopy(packet);small['components']=[{'type':'cold','amount':2}]
    before=m.snapshot();declare(m,'guarding-deflection',packet=small);m.roll_die('attempt',6);result=m.resolve('attempt')
    check('Guarding-no-negative-damage-or-extra-prevention-credit',result['packet']['components'][0]['amount']==0 and result['prevented']==2 and result['packet']['originalHit'])
    record('Guarding-complete-prevention',before,m,result=result)
    for field,value in [('kind','HP-sacrifice'),('kind','state-assignment'),('kind','direct-death'),
                        ('recipientMitigationAllowed',False),('stage','after-tempHP'),('recipient','ally')]:
        m=ready('guarding-deflection');bad=deepcopy(packet);bad[field]=value
        reject('Guarding/invalid/'+field+'/'+str(value),m,lambda:declare(m,'guarding-deflection',packet=bad))
    m=ready('guarding-deflection',True);m.own_turn=False;before=m.snapshot();declare(m,'guarding-deflection');m.roll_die('attempt',1);m.resolve('attempt')
    m.reaction.round_boundary();m.reaction.extra_turn()
    reject('Guarding-no-round-or-extra-turn-Reaction-refresh',m,lambda:declare(m,'guarding-deflection',event='second'))
    check('Guarding-still-one-die-not-two',m.pool['current']==1)
    m.reaction.regular_start(1);declare(m,'guarding-deflection',event='second');m.roll_die('second',1);m.resolve('second')
    check('Guarding-real-regular-start-refresh',m.pool['current']==0 and not m.reaction.available)
    record('Guarding-two-separate-Reaction-epochs',before,m)

    for source_dc,natural,face,success in [(None,6,1,True),(14,10,1,True),(14,1,6,False),(30,20,1,True),(40,20,1,False)]:
        m=ready('rallying-signal');m.target('ally')['fear'][0]['sourceDC']=source_dc
        before=m.snapshot();declare(m,'rallying-signal');m.roll_die('attempt',face);result=m.resolve('attempt',actor_die=natural)
        check('Rally/task/'+str((source_dc,natural,face)),result['success']==success and m.target('ally')['fear'][0]['active']!=success and m.target('ally')['fear'][1]['active'])
        record('Rally/task/'+str((source_dc,natural,face)),before,m,result=result)
    m=ready('rallying-signal');before=m.snapshot();declare(m,'rallying-signal',target='owner',fear='self-fear');m.roll_die('attempt',4);m.resolve('attempt',actor_die=10)
    check('Rally-self-eligible-actual-ally',not m.actor['fear'][0]['active']);record('Rally-self',before,m)
    for change in [lambda m:m.target('ally').update(position=35),lambda m:m.target('ally').update(perceivesRally=False),
                   lambda m:m.target('ally').update(ally=False),lambda m:m.target('ally')['fear'][0].update(active=False),
                   lambda m:m.target('ally')['fear'][0].update(condition='Charmed')]:
        m=ready('rallying-signal');change(m);reject('Rally/invalid/'+str(len(checks)),m,lambda:declare(m,'rallying-signal'))

    for terrain,crawl,squeeze,face,cost in [('normal',False,False,1,5),('difficult',False,False,2,10),
            ('severe',False,False,3,15),('difficult',True,False,3,15),('difficult',True,True,4,20)]:
        m=ready('measured-advance');before=m.snapshot();declare(m,'measured-advance');m.roll_die('attempt',face);m.resolve('attempt')
        preview=m.advance_step('attempt',-5,terrain=terrain,crawling=crawl,squeezing=squeeze)
        check('Advance/OA-before-exit/'+str(cost),preview['awaitingOpportunityResponseBeforeExit']==['enemy'] and m.actor['position']==0)
        result=m.advance_step('attempt',-5,terrain=terrain,crawling=crawl,squeezing=squeeze,opportunity_outcome='decline');m.finish_advance('attempt')
        check('Advance/actual-cost/'+str((terrain,crawl,squeeze)),result['cost']==cost and m.actor['ordinaryMovementSpent']==10 and m.actor['position']==-5)
        record('Advance/terrain/'+str((terrain,crawl,squeeze)),before,m,result=result)
    m=ready('measured-advance');before=m.snapshot();declare(m,'measured-advance');m.roll_die('attempt',6);m.resolve('attempt')
    result=m.advance_step('attempt',-5,opportunity_outcome='conditional-interruption')
    check('Advance-interrupted-before-exit-no-bank-or-refund',m.actor['position']==0 and m.pending_movement is None and m.pool['current']==0 and m.bonus_actions==0 and not m.target('enemy')['reactionAvailable'] and m.events['attempt']['movementRemaining']==0 and m.events['attempt']['discardedDistance']==30)
    record('Advance-explicit-conditional-OA-interruption',before,m,result=result,
        scope='The fixture supplies an interrupting OA consequence; its attack/damage was not executed. The real movement ordering, spent reaction and lost unused budget are represented.')
    m=ready('measured-advance');declare(m,'measured-advance');m.roll_die('attempt',1);m.resolve('attempt')
    reject('Advance-no-unaffordable-difficult-step',m,lambda:m.advance_step('attempt',-5,terrain='difficult'))
    reject('Advance-no-teleport-step',m,lambda:m.advance_step('attempt',-10))
    reject('Advance-no-occupied-endpoint',m,lambda:m.advance_step('attempt',5))
    for change in [lambda m:setattr(m,'regular_turn',False),lambda m:setattr(m,'own_turn',False),lambda m:m.actor['modes'].update(walk=0)]:
        m=ready('measured-advance');change(m);reject('Advance/invalid-activation/'+str(len(checks)),m,lambda:declare(m,'measured-advance'))
    m=ready('measured-advance');reject('Advance-no-new-flight',m,lambda:declare(m,'measured-advance',mode='fly'))

    for kind in [x.removeprefix(PREFIX) for x in menu]:
        m=ready(kind);before=m.snapshot();declare(m,kind);m.interrupt('attempt')
        check(kind+'/interrupted-commit-stays-spent',m.pool['current']==0 and m.events['attempt']['status']=='interrupted-costs-retained')
        reject(kind+'/no-outcome-after-interruption',m,lambda:m.resolve('attempt',actor_die=20))
        record(kind+'/interruption',before,m)
    m=ready('measured-strike');before=m.snapshot();declare(m,'measured-strike');m.roll_die('attempt',1);m.resolve('attempt',actor_die=1)
    h=m.acquired;h.advance(8);h.earn(8);prior=set(m.pool['maneuvers'])
    h.acquire_menu('martial_adept_advanced',8,[x for x in menu if x not in prior][:2])
    check('Advanced-adds-one-new-die-without-refilling-spent-parent',m.pool['maximum']==2 and m.pool['current']==1 and len(m.pool['maneuvers'])==4)
    m.attack_slots=1  # Explicit separate lawful Attack Action attack premise, not a granted extra action.
    reject('one-maneuver-per-underlying-event',m,lambda:declare(m,'measured-strike'))
    m.operative=False;reject('suppressed-maneuver-no-use',m,lambda:declare(m,'measured-strike',event='later'))
    m.operative=True;check('restoring-availability-does-not-refill',m.pool['current']==1)
    record('paid-Advanced-after-real-spend',before,m,
        scope='The repeated-event rejection supplies a distinct legal attack allowance conditionally; no extra Action is granted by that premise.')
    check('all-bound-sources-preserved',bindings==[info(p) for p in paths])
    report={'createdAtUtc':datetime.now(timezone.utc).isoformat(),'status':'six-maneuver-transaction-reference-pass',
        'checks':len(checks),'failures':[],'results':checks,'sourceBindings':bindings,'cohort':menu,
        'actorSourceProjection':actor,'conditionalWorldFixture':world,'conditionalIncomingPacket':packet,'traces':traces,
        'counts':{'maneuvers':6,'d6FacesEach':6,'recordedTraces':len(traces),'newPartialPrerequisiteIdentities':0},
        'limits':[
            'Actual paid Warrior Martial Adept/Advanced selections, abilities and Athletics/weapon training; not a complete character build or authenticated campaign.',
            'All bodies, item custody, obstacles, fear sources/DCs and incoming post-defense packets are explicit conditional encounter fixtures.',
            'Uses one legal ordinary Attack Action attack, one-dimensional five-foot geometry and the actual held longsword. Other attack profiles, Ready releases, extra Actions, complete map/anatomy and advantage-source evaluation remain outside this slice.',
            'Guarding performs typed reduction then one concrete Core HP/tempHP continuation. It does not re-execute passive defenses, every Wound/death interaction or attached condition application.',
            'Measured Advance exposes ordinary opportunity timing before exit; the single interrupting OA consequence is explicitly supplied, not a full OA attack/damage execution.',
            'Suppression and later legal-attack premises are conditional. Genuine rest recovery, all class interactions and complete feat use remain separate.',
            'No all-FXC04, all335-acquisition, full candidate, GPT, runtime, human balance, publication or cosmology approval claimed.'],
        'sourceInformationDeleted':False,'newRulesAdopted':False,'fullCandidateApproved':False}
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=serial)+'\n',encoding='utf-8',newline='\n')
    notes.write_text('# Six Martial Adept maneuver transactions\n\n'
        f'{len(checks)} checks passed across {len(traces)} recorded histories, covering all six maneuver identities and every d6 face. '
        'The histories pay real Warrior feat opportunities, spend the die and action/replaced attack before rolls, retain costs on failure/interruption, '
        'and preserve the parent pool when Advanced adds one new die.\n\n'
        'Core checks cover natural attack faces, opposed ties, separate Disarm methods, drop custody, stable typed prevention before tempHP, '
        'Reaction epochs, single-record Rally task degrees, separate terrain-paying movement and opportunity timing. '
        'The encounter world and interrupting OA result remain explicit conditional fixtures. Full maps, other weapon profiles, Ready/class interactions, '
        'genuine rest recovery and complete damage/condition dispatch are not claimed. No rules or selection flags changed.\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checks':len(checks),'failures':0,'counts':report['counts'],'report':info(output),'notes':info(notes)},indent=2))


if __name__=='__main__':main()
