"""Verify source integrity without promoting an unfinished rider registry."""
from pathlib import Path
import hashlib
import json
from core_playtest_rules import LifeState, damage_event
from custom_condition_rules import (qualifies_hook, bleed_marker_arbitration,
    brutality_pre_damage, consume_retribution, doomed_timestamp_expiry,
    hp_recovery, death_save_with_hp_prohibition, stable_recovery_with_hp_prohibition,
    periodic_marker_arbitration, healing_triggered_bleed_cure, refresh_bleed_duration,
    extinguishable_records, fire_ending_save_eligible, periodic_binding_for_component,
    arbitrate_periodic_applications, recipe_occupies_slot)
from spell_playtest_rules import SpellRuleError

ROOT = Path(__file__).resolve().parents[1]


def interface_checks():
    results = []
    def check(name, actual, expected):
        results.append({'name': name, 'pass': actual == expected, 'actual': actual, 'expected': expected})
    bleed = {'mechanicalId': 'crimson-agent.bleed', 'tags': ['family.bleeding'],
             'ownerCharacterId': 'A', 'sourceClass': 'Crimson Agent', 'sourceEngine': 'crimson-agent.bleed', 'active': True}
    check('Own multiclass Bleed can satisfy possessive Thief hook', qualifies_hook('thief.sneak-condition', bleed, 'A'), True)
    check('Another character Bleed does not satisfy your Thief hook', qualifies_hook('thief.sneak-condition', bleed, 'B'), False)
    check('Vile Tactics does not invent an owner restriction', qualifies_hook('thief.vile-tactics', bleed, 'B'), True)
    check('Owned Crimson instance qualifies its technical engine', qualifies_hook('crimson.bleed-engine', bleed, 'A'), True)
    check('Owned other-class Bleed is not a Crimson tick instance', qualifies_hook('crimson.bleed-engine', dict(bleed, sourceEngine='thief.bloodleech'), 'A'), False)
    weakened = {'mechanicalId': 'warrior.weakened', 'tags': ['eligibility.weakened'], 'active': True}
    check('Judging Light recognizes explicit weakened tag', qualifies_hook('cleric.judging-light', weakened, 'A'), True)
    check('Suppressed weakness cannot qualify', qualifies_hook('cleric.judging-light', dict(weakened, suppressed=True), 'A'), False)
    check('Immune weakness cannot qualify', qualifies_hook('cleric.judging-light', dict(weakened, immune=True), 'A'), False)
    check('Oracle Curse engine name is not an inflicted curse', qualifies_hook('cleric.judging-light', {'mechanicalId':'oracle.curse-engine','tags':[],'active':True}, 'A'), False)
    fear = {'mechanicalId':'core.frightened','sourceClass':'Warrior','ownerCharacterId':'A','active':True}
    check('Terror Engine uses own Warrior source', qualifies_hook('warrior.terror-engine', fear, 'A'), True)
    check('Terror Engine rejects same owner another class source', qualifies_hook('warrior.terror-engine', dict(fear, sourceClass='Cleric'), 'A'), False)
    check('Pending Disoriented cannot activate Terror Engine early', qualifies_hook('warrior.terror-engine', dict(fear, mechanicalId='warrior.disoriented.pending'), 'A'), False)
    check('Active Disoriented qualifies Terror Engine', qualifies_hook('warrior.terror-engine', dict(fear, mechanicalId='warrior.disoriented.active'), 'A'), True)
    check('Zero-Speed Grappled does not automatically qualify slowed hook', qualifies_hook('druid.snow-leopard', {'mechanicalId':'core.grappled','active':True,'tags':[]}, 'A'), False)
    check('Explicit hostile root tag qualifies slowed hook', qualifies_hook('druid.snow-leopard', {'mechanicalId':'shaman.root','active':True,'tags':['eligibility.slowed-foe']}, 'A'), True)
    groups = [{'stackGroupId':'crimson:A','expectedDamageTwice':10,'firstApplicationSequence':2},
              {'stackGroupId':'generic:B','expectedDamageTwice':8,'firstApplicationSequence':1}]
    outcome = bleed_marker_arbitration(groups)
    check('Permitted two Crimson instances compete as one group', outcome['damagingGroup'], 'crimson:A')
    check('Losing group consumes its tick instead of banking', outcome['consumedTickGroups'], ['crimson:A', 'generic:B'])
    groups[1]['expectedDamageTwice'] = 10
    check('Equal expected damage chooses earlier group', bleed_marker_arbitration(groups)['damagingGroup'], 'generic:B')
    check('No due Bleeds means no damaging group', bleed_marker_arbitration([])['damagingGroup'], None)
    flags = dict(perceived=True, hostile=True, distance=60)
    check('Quarter-HP boundary qualifies', brutality_pre_damage(25,100,**flags), True)
    check('26 of100 does not qualify', brutality_pre_damage(26,100,**flags), False)
    check('Correct notebook arithmetic:30 of100 does not qualify', brutality_pre_damage(30,100,**flags), False)
    check('Odd maximum uses exact quarter comparison', brutality_pre_damage(25,101,**flags), True)
    check('Out of range does not qualify', brutality_pre_damage(25,100,**dict(flags,distance=61)), False)
    mark = {'mechanicalId':'paladin.vengeance-mark.retribution','active':True,'ownerCharacterId':'A',
            'tags':['eligibility.paladin-vengeance-marked'],'opportunityAttackAdvantage':True,'expiry':200}
    spent = consume_retribution(mark)
    check('Spending Retribution die retains opportunity benefit', spent['opportunityAttackAdvantage'], True)
    check('Spending die retains Vengeance eligibility', qualifies_hook('paladin.vengeance', spent, 'A'), True)
    check('Spending die leaves expiry unchanged', spent['expiry'], 200)
    check('Another Paladin does not inherit the mark', qualifies_hook('paladin.vengeance', spent, 'B'), False)
    check('Doomed subtracts one round from finite buff deadline', doomed_timestamp_expiry(120,100,finite_positive_buff=True), 114)
    check('Duplicate Doomed cannot subtract twice that turn', doomed_timestamp_expiry(114,100,finite_positive_buff=True,already_accelerated_this_turn=True),114)
    check('Doomed does not alter permanent or recharge metadata', doomed_timestamp_expiry(120,100,finite_positive_buff=False),120)
    check('An advanced expiry in the past ends at this check', doomed_timestamp_expiry(103,100,finite_positive_buff=True)<=100,True)
    state=LifeState(20,0,death_failures=2)
    blocked=death_save_with_hp_prohibition(state,20,prohibited=True,regular_turn_id=1,stable_d4=2,now_seconds=50)
    check('Blocked natural20 stabilizes without HP', (blocked.hp,blocked.stable,blocked.death_successes,blocked.death_failures),(0,True,0,0))
    check('Blocked natural20 establishes one original deadline',blocked.stable_until_seconds,7250)
    due=stable_recovery_with_hp_prohibition(blocked,8000,prohibited=True)
    check('Due blocked recovery keeps original deadline',due.stable_until_seconds,7250)
    check('Due blocked recovery remains at zero',due.hp,0)
    released=stable_recovery_with_hp_prohibition(due,8001,prohibited=False)
    check('Removing prohibition resolves due HP once', (released.hp,released.stable,released.stable_until_seconds),(1,False,None))
    check('No second deferred HP from rechecking deadline',stable_recovery_with_hp_prohibition(released,9000).hp,1)
    damaged,_=damage_event(due,1)
    check('Damage cancels blocked Stable timer',damaged.stable_until_seconds,None)
    check('Later ending prohibition does not resurrect canceled recovery',stable_recovery_with_hp_prohibition(damaged,9000).hp,0)
    check('Ordinary HP prohibition blocks healing',hp_recovery(LifeState(20,3),10,prohibited=True).hp,3)
    check('Legal natural20 recovery remains normal',death_save_with_hp_prohibition(state,20,regular_turn_id=1).hp,1)
    fire_groups = [dict(g, family='family.ongoing-fire') for g in groups]
    check('Attached fire uses its own same-marker arbitration', periodic_marker_arbitration(fire_groups,family='family.ongoing-fire')['damagingGroup'],'generic:B')
    try:
        periodic_marker_arbitration(fire_groups,family='family.bleeding')
        rejected=False
    except SpellRuleError:
        rejected=True
    check('Fire groups cannot compete with Bleed groups',rejected,True)
    try:
        periodic_marker_arbitration([],family='fire-damage')
        rejected=False
    except SpellRuleError:
        rejected=True
    check('Fire damage alone cannot grant family arbitration',rejected,True)
    cure_record=dict(bleed,magicalHealingEndpoint='end')
    cure_args=dict(legal_effect=True,magical=True,potential=5,actual_hp_gained=0)
    check('Positive legal magical heal cures ordinary Bleed even at zero HP gained',healing_triggered_bleed_cure(cure_record,**cure_args),'end')
    check('Blood Curse gets CON save under blocked recovery',healing_triggered_bleed_cure(dict(cure_record,magicalHealingEndpoint='saveToEnd'),**cure_args),'saveToEnd')
    check('Explicit actual-HP prerequisite still matters',healing_triggered_bleed_cure(cure_record,**cure_args,remover_requires_actual_hp=True),'none')
    for field,value in [('legal_effect',False),('magical',False),('potential',0)]:
        check(f'Cure rejects {field}={value}',healing_triggered_bleed_cure(cure_record,**dict(cure_args,**{field:value})),'none')
    check('Display name alone cannot create healing cure',healing_triggered_bleed_cure(dict(cure_record,tags=[]),**cure_args),'none')
    check('Missing registered endpoint never silently imports generic cure',healing_triggered_bleed_cure(bleed,**cure_args),'none')
    check('Ordinary Persistent refreshes one remaining to two',refresh_bleed_duration(1,2),2)
    check('Ordinary Persistent never shortens three remaining',refresh_bleed_duration(3,2),3)
    check('Prolonged changes eligible refresh to four',refresh_bleed_duration(1,2,prolonged=True),4)
    check('Prolonged refresh is replacement not addition',refresh_bleed_duration(3,2,prolonged=True),4)
    check('Crimson base three is ineligible regardless remaining',refresh_bleed_duration(1,3,prolonged=True),2)
    check('A base duration alone does not cap Prolonged',refresh_bleed_duration(2,2,prolonged=True),4)
    check('An express cap limits an otherwise legal extension',refresh_bleed_duration(1,2,prolonged=True,explicit_hard_cap=3),3)
    check('Another owner cannot trigger your refresh',refresh_bleed_duration(1,2,owned=False,prolonged=True),1)
    check('An absent trigger does not grant a free refresh',refresh_bleed_duration(1,2,qualifying_trigger=False,prolonged=True),1)
    try:
        refresh_bleed_duration(0,2,prolonged=True)
        rejected=False
    except SpellRuleError:
        rejected=True
    check('Refresh cannot resurrect an expired record',rejected,True)
    fire={'mechanicalId':'mage.fire-focus.burn','applicationId':'fire1','tags':['family.ongoing-fire'],
          'active':True,'ordinaryExtinguishable':True,'genericDexEndingSave':True,'remainingTicks':1}
    protected=dict(fire,applicationId='protected',mundaneExtinguishingProhibited=True)
    fires=[fire,dict(fire,applicationId='fire2'),protected,
           dict(fire,applicationId='special',specialExtinguishingPrerequisiteUnmet=True),
           dict(fire,applicationId='ashblood',tags=[])]
    check('One extinguish action ends all ordinary eligible fires only',extinguishable_records(fires),['fire1','fire2'])
    check('Remaining future tick permits ending save',fire_ending_save_eligible(fire,regular_turn_end=True),True)
    check('Final consumed tick does not create pointless ending save',fire_ending_save_eligible(dict(fire,remainingTicks=0),regular_turn_end=True),False)
    check('Indefinite generic fire retains ending save',fire_ending_save_eligible(dict(fire,remainingTicks=None),regular_turn_end=True),True)
    check('Extra turn does not create a new ending save',fire_ending_save_eligible(fire,regular_turn_end=False),False)
    check('Mundane extinguish prohibition does not erase separate DEX endpoint',fire_ending_save_eligible(protected,regular_turn_end=True),True)
    check('Specific Bleed replaces rather than duplicates Core fallback',periodic_binding_for_component(specific_profile='dragoon.bleed',explicit_core_condition='core.bleeding'),'dragoon.bleed')
    check('Explicit Core-only application retains Core identity',periodic_binding_for_component(explicit_core_condition='core.burning'),'core.burning')
    check('A display name alone grants no implicit periodic record',periodic_binding_for_component(),None)
    check('Condition immunity prevents initial periodic record',periodic_binding_for_component(specific_profile='dragoon.bleed',explicit_core_condition='core.bleeding',condition_immune=True),None)
    a={'applicationId':'A','mechanicalId':'mage.fire-focus.burn','targetId':'victim','active':True,
       'tags':['family.ongoing-fire'],'dueMarker':'end1','stackGroupId':'mage:owner',
       'withinGroupPolicy':'strongest','instanceCap':1,'expectedDamageTwice':5,'applicationSequence':1}
    b=dict(a,applicationId='B',mechanicalId='mage.inferno-lance.burn',expectedDamageTwice=7,applicationSequence=2)
    c=dict(a,applicationId='C',mechanicalId='core.burning',stackGroupId='core:other',applicationSequence=3)
    resolved=arbitrate_periodic_applications([a,b,c],family='family.ongoing-fire',marker='end1')
    check('Mage internal maximum precedes global selection',resolved['damageApplications'],['B'])
    check('Every due application consumes its tick',resolved['consumedTickApplications'],['A','B','C'])
    resolved=arbitrate_periodic_applications([dict(a,suppressed=True),dict(b,suppressed=True),c],family='family.ongoing-fire',marker='end1')
    check('Suppressed high group cannot starve active Core fire',resolved['damageApplications'],['C'])
    check('Suppressed records still consume scheduled clocks',resolved['consumedTickApplications'],['A','B','C'])
    resolved=arbitrate_periodic_applications([a,dict(b,damageTypeImmune=True),c],family='family.ongoing-fire',marker='end1')
    check('Damage immunity alone does not exclude winner',resolved['damageApplications'],['B'])
    resolved=arbitrate_periodic_applications([a,dict(b,dueMarker='start2'),c],family='family.ongoing-fire',marker='end1')
    check('Different marker neither damages nor consumes early',resolved['consumedTickApplications'],['A','C'])
    crimson=[dict(a,applicationId='blood1',tags=['family.bleeding'],stackGroupId='crimson:A',withinGroupPolicy='sum-permitted',instanceCap=2),
             dict(a,applicationId='blood2',tags=['family.bleeding'],stackGroupId='crimson:A',withinGroupPolicy='sum-permitted',instanceCap=2,applicationSequence=2),
             dict(c,applicationId='blood3',tags=['family.bleeding'],expectedDamageTwice=8)]
    resolved=arbitrate_periodic_applications(crimson,family='family.bleeding',marker='end1')
    check('Two legal Crimson instances beat one PB4 Core group',resolved['damageApplications'],['blood1','blood2'])
    try:
        arbitrate_periodic_applications([a,a],family='family.ongoing-fire',marker='end1')
        rejected=False
    except SpellRuleError:
        rejected=True
    check('Duplicate record cannot create duplicate tick',rejected,True)
    check('Cured Bloodleech plus resolved critical heal leaves no recipe slot',recipe_occupies_slot([{'active':False,'ongoing':True},{'active':True,'ongoing':False}]),False)
    check('An actual other ongoing component retains recipe slot',recipe_occupies_slot([{'active':True,'ongoing':True}]),True)
    check('Suppressed ongoing component still retains recipe slot',recipe_occupies_slot([{'active':True,'ongoing':True,'suppressed':True}]),True)
    for flag in ('suppressed','immune'):
        held_bleed=dict(cure_record,**{flag:True})
        check(f'Present {flag} Bleed is cured by positive-potential magic',healing_triggered_bleed_cure(held_bleed,**cure_args),'end')
        check(f'Present {flag} Blood Curse retains its CON ending save',healing_triggered_bleed_cure(dict(held_bleed,magicalHealingEndpoint='saveToEnd'),**cure_args),'saveToEnd')
        check(f'Present {flag} fire may be extinguished',extinguishable_records([dict(fire,**{flag:True})]),['fire1'])
        check(f'Present {flag} fire may use its existing ending save',fire_ending_save_eligible(dict(fire,**{flag:True}),regular_turn_end=True),True)
        check(f'Cured {flag} Bleed never resumes eligibility',healing_triggered_bleed_cure(dict(held_bleed,active=False,**{flag:False}),**cure_args),'none')
    check('Ended fire is not a cure target',extinguishable_records([dict(fire,active=False)]),[])
    check('Suppression cannot bypass protected-fire cure',extinguishable_records([dict(protected,suppressed=True)]),[])
    check('Suppressed fire with no future ticks gets no ending save',fire_ending_save_eligible(dict(fire,suppressed=True,remainingTicks=0),regular_turn_end=True),False)
    check('Suppressed Bleed still honors explicit actual-gain cure prerequisite',healing_triggered_bleed_cure(dict(cure_record,suppressed=True),**cure_args,remover_requires_actual_hp=True),'none')
    return results


def main():
    packet = json.loads((ROOT / 'data/playtest/custom_condition_bindings.json').read_text(encoding='utf-8'))
    seen, references, issues, source_cache = set(), 0, [], {}
    entries = [('definition', d['mechanicalId'], d, d['applicationSources']) for d in packet['definitions']]
    entries += [('hook', h['id'], h, h['sourceReferences']) for h in packet['hooks']]
    for entry_kind, ident, definition, sources in entries:
        if ident in seen:
            issues.append(f'Duplicate mechanical ID: {ident}')
        seen.add(ident)
        required = ['displayName', 'kind', 'status', 'effect', 'ending', 'stacking', 'immunityRule'] if entry_kind == 'definition' else ['rule']
        for field in required:
            if not definition.get(field):
                issues.append(f'{ident}: missing {field}')
        if not sources:
            issues.append(f'{ident}: no source')
        for evidence in definition.get('reviewEvidence', []):
            if not (ROOT.parents[1] / evidence).exists():
                issues.append(f'{ident}: missing review evidence {evidence}')
        periodic=definition.get('periodic')
        if periodic:
            for field in ['dice','damageType','ticks','marker','stackGroupTemplate','maximumDamagingInstancesPerGroup','replacementTiming','extraTurnTicks','baseDurationTicks']:
                if field not in periodic:
                    issues.append(f'{ident}: missing periodic field {field}')
            if definition.get('cure',{}).get('status'):
                issues.append(f'{ident}: unresolved cure profile')
            if 'family.bleeding' in definition['familyTags'] and definition['cure'].get('magicalHealingEndpoint') not in ['end','saveToEnd','none']:
                issues.append(f'{ident}: invalid cure endpoint')
        for source in sources:
            path = source['path']
            if path not in source_cache:
                source_cache[path] = json.loads((ROOT / path).read_text(encoding='utf-8'))
            actual = source_cache[path]
            if source['kind'] == 'card':
                card = next((c for c in actual['cards'] if c['id'] == source['cardId']), None)
                if card is None:
                    issues.append(f"{ident}: missing source card {source['cardId']}")
                    continue
                digest = hashlib.sha256(json.dumps(card, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                if digest != source['sourceObjectSha256'] or card['effect'] != source['effect'] or card['duration'] != source['duration']:
                    issues.append(f'{ident}: source card changed; review required')
            elif source['kind'] == 'engine':
                text = actual['engine'][source['engineIndex']]
                if text != source['text'] or hashlib.sha256(text.encode()).hexdigest() != source['textSha256']:
                    issues.append(f'{ident}: source engine changed; review required')
            elif source['kind'] == 'operational-spell':
                spell=next((s for s in actual['spells'] if s['id']==source['spellId']),None)
                if not spell or spell.get('status')!='operational-playtest-draft':
                    issues.append(f'{ident}: missing operational spell')
                elif spell['operational'] != source['operational'] or hashlib.sha256(json.dumps(spell['operational'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()!=source['operationalSha256']:
                    issues.append(f'{ident}: operational spell changed; review required')
            elif source['kind'] == 'core-condition':
                condition=next((c for c in actual['conditions'] if c['id']==source['conditionId']),None)
                if condition != source['condition'] or hashlib.sha256(json.dumps(condition,sort_keys=True,ensure_ascii=False).encode()).hexdigest()!=source['conditionSha256']:
                    issues.append(f'{ident}: generic condition overlay changed; alignment review required')
            else:
                issues.append(f'{ident}: unknown source kind')
            references += 1
    scenarios = interface_checks()
    failures = [case for case in scenarios if not case['pass']]
    report = {'sourceIntegrityStatus': 'PASS' if not issues else 'FAIL',
              'interfaceStatus': 'PASS' if not failures else 'FAIL', 'interfaceChecks': len(scenarios),
              'interfaceFailures': failures, 'interfaceResults': scenarios,
              'registryStatus': packet['status'], 'definitions': len(packet['definitions']), 'hooks':len(packet['hooks']),
              'sourceReferencesVerified': references, 'sourceIssues': issues,
              'openIntegrationIssues': packet['openIssues'],
              'scope': 'Exact card/engine references and selected ownership, stacking, snapshot, buff-expiry and blocked-HP interfaces. Not exhaustive semantic coverage, completed hook integration, a full runtime or balance validation.'}
    (ROOT / 'docs/mechanics/CUSTOM_CONDITION_BINDING_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f"{report['sourceIntegrityStatus']} source integrity: {len(packet['definitions'])} definitions, {len(packet['hooks'])} hooks, {references} references; {report['interfaceStatus']} {len(scenarios)} interface checks; registry {packet['status']}")
    if issues or failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
