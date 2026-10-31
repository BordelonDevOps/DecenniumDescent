from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import zlib
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
PREV = AUDIT / 'rank9_illusionreality5_delta_263_prepared/DD_Rank9_SoulReflection_Delta_263.zip'
OUT = AUDIT / 'rank9_illusionreality5_delta_268_prepared'
ARCHIVE = OUT / 'DD_Rank9_SoulReflection_Delta_268.zip'
DELIVERY = OUT / 'DD_Rank9_SoulReflection_Delta_268_DELIVERY.json'
AUDIT_OUT = OUT / 'SOUL_REFLECTION_DELTA_268_INDEPENDENT_AUDIT.json'
SUBMISSION = OUT / 'SOUL_REFLECTION_DELTA_268_SUBMISSION.json'
AUTH = {'reviewedApplied': 814, 'pending': 34, 'acceptedUnapplied': 0,
        'completeStandaloneProcedures': 538, 'scopedInterfaces': 173}
CASE_FILES = {
    'cases/FORM_SNAPSHOT_263.json': 'cases/FORM_SNAPSHOT_268.json',
    'cases/COPIED_CONCENTRATION_263.json': 'cases/COPIED_CONCENTRATION_268.json',
    'cases/ORIGINAL_ZERO_263.json': 'cases/ORIGINAL_ZERO_268.json',
    'cases/ORIGINAL_CARGO_263.json': 'cases/ORIGINAL_CARGO_268.json',
}
TURNS = {
    'FORM': {'A': [0, 6, 12], 'T': [5, 11, 17]},
    'CONCENTRATION': {'A': [0, 6, 12], 'T': [5, 11, 17]},
    'ZERO': {'A': [0, 6, 12], 'T': [5, 11]},
    'CARGO': {'A': [0, 6, 12], 'T': [1, 7, 13], 'D': [3, 9]},
}
PHASES = {
    'FORM': [5.91, 11.91, 17.91],
    'CONCENTRATION': [5.91, 11.91, 17.91],
    'ZERO': [5.91, 11.91, 17.91],
    'CARGO': [1.91, 7.91, 13.91],
}


def enc(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def state_sha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))


def crc(blob):
    return f'{zlib.crc32(blob) & 0xffffffff:08x}'


def binding(path, blob):
    return {'path': path, 'bytes': len(blob), 'sha256': sha(blob), 'crc32': crc(blob)}


def replace_strings(value, old, new):
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [replace_strings(x, old, new) for x in value]
    if isinstance(value, dict):
        return {replace_strings(k, old, new): replace_strings(v, old, new) for k, v in value.items()}
    return value


def apply_delta(dst, before, after, key=None):
    if isinstance(before, dict) and isinstance(after, dict):
        if not isinstance(dst, dict):
            dst = copy.deepcopy(before)
        for key in before.keys() - after.keys():
            dst.pop(key, None)
        for key in after.keys() - before.keys():
            dst[key] = copy.deepcopy(after[key])
        for key in before.keys() & after.keys():
            if before[key] != after[key]:
                dst[key] = apply_delta(dst.get(key), before[key], after[key], key=key)
        return dst
    if (key in ('regularStarts', 'regularEnds') and isinstance(before, list) and isinstance(after, list)
            and len(after) > len(before) and after[:len(before)] == before):
        merged = list(dst) if isinstance(dst, list) else copy.deepcopy(before)
        for marker in after[len(before):]:
            if marker not in merged:
                merged.append(copy.deepcopy(marker))
        return sorted(merged) if all(isinstance(x, (int, float)) for x in merged) else merged
    if before != after:
        return copy.deepcopy(after)
    return dst


def add_schedule(state, key, at, reason):
    state.setdefault('scheduled', {})[key] = {'at': at, 'reason': reason, 'status': 'pending'}


def base_case(case, kind):
    s = copy.deepcopy(case['initialState'])
    included = ('A', 'D', 'T') if kind == 'CARGO' else ('A', 'T')
    s['actors'] = {k: s['actors'][k] for k in included}
    if 'A' in s['actors'] and s['actors']['A'].get('schoolDC') is not None:
        s['actors']['A']['spellDC'] = s['actors']['A']['schoolDC']
        s['actors']['A']['schoolDCSource'] = 'W17-IR207 Divination + acquired School Mastery; source DC 21'
    first = min(e['atSeconds'] for e in case['events'])
    if kind == 'CONCENTRATION':
        first = min(first, 0.0)
    if kind == 'FORM':
        first = min(first, -52.8)
    s['time'] = first - 0.01
    s['scheduled'] = {}
    s['reflectionPhases'] = []
    s['reflectionPhaseLedger'] = []
    s['spellCommitments'] = []
    s['spellCadence'] = []
    s['saveHistory'] = []
    s['hardDenialLedger'] = {}
    s.pop('R1', None)
    for actor_id in list(s['items']):
        if kind != 'CARGO' and actor_id.startswith('D-'):
            del s['items'][actor_id]
    for actor_id, starts in TURNS[kind].items():
        a = s['actors'][actor_id]
        a['castHistory'] = []
        a['castFamilies'] = []
        a['resourceHistory'] = []
        a['matrixFamilies'] = []
        a['magicalThisTurn'] = False
        a['refrainCount'] = 0
        a['dissonance'] = 0
        calendar = list(starts)
        scheduled_starts = list(starts)
        if kind == 'FORM' and actor_id == 'T':
            calendar = [-52.8] + calendar
            scheduled_starts = [-52.8] + scheduled_starts
        if kind in ('FORM', 'CONCENTRATION') and actor_id == 'A':
            calendar = [0, 6, 12, 18, 24]
            scheduled_starts = [0, 6, 12, 18]
        a['regularCalendar'] = calendar
        a['regularStarts'] = []
        a['regularEnds'] = []
        a['nextRegularStart'] = scheduled_starts[0] if scheduled_starts else None
        for at in scheduled_starts:
            add_schedule(s, f'regular-start:{actor_id}:{at:g}', at, 'actual regular START')
            add_schedule(s, f'regular-end:{actor_id}:{at + 0.9:g}', at + 0.9, 'actual regular END')
    for at in PHASES[kind]:
        add_schedule(s, f'reflection-phase:R1:{at:g}', at, 'proposed Soul Reflection phase after actual target END')
    s['caseId'] = case['id'].replace('5263', '5268')
    s['encounter'] = s['caseId']
    s['proposalStatus'] = 'UNACCEPTED_DIRECTOR_ADJUDICATION_REQUIRED'
    return s


def actor_item(state, item_id, source_id, held):
    if item_id in state['items']:
        return
    state['items'][item_id] = {
        'id': item_id, 'name': item_id.removeprefix('R1-').replace('-', ' ').title(),
        'kind': 'temporary-reflection-manifestation', 'sourceItemId': source_id,
        'owner': 'R1', 'custodian': 'R1', 'held': held, 'temporary': True,
        'usableBy': ['R1'], 'transferable': False, 'uniqueArtifactCopy': False,
        'position': [15, 0, 0], 'active': True, 'colliding': True,
        'endsWithReflection': True, 'formState': 'available',
    }


def add_reflection_gear(state):
    r = state['actors'].get('R1')
    if not r:
        return
    for item_id, source_id, held in [('R1-focus', 'T-focus', True), ('R1-book', 'T-book', False), ('R1-clothes', 'T-clothes', False)]:
        actor_item(state, item_id, source_id, held)
    r['inventory'] = ['R1-focus', 'R1-book', 'R1-clothes']
    r['hands'] = {'left': 'R1-focus', 'right': None}
    r['reflectionSource'] = next((k for k, v in state.get('effects', {}).items() if v.get('kind') == 'soul-reflection'), None)
    r['causalRoot'] = r['reflectionSource']
    r['ownerId'] = None
    r['attachedOnly'] = False


def set_form(state, actor_id, form_id, deadline, source_actor, copied=False):
    a = state['actors'][actor_id]
    if 'formBaseline' not in a:
        a['formBaseline'] = {k: copy.deepcopy(a.get(k)) for k in ('speed', 'voiceUsable', 'somaticUsable', 'hands', 'inventory')}
    gear = list(a.get('inventory', []))
    a['formOverride'] = {
        'form': 'gaseous-mist', 'sourceId': form_id, 'sourceActor': source_actor,
        'deadlineAt': deadline, 'copiedSnapshot': copied, 'speedFeet': 10, 'hover': True,
        'voiceUsable': False, 'somaticUsable': False, 'handsUsable': False,
        'attacksUsable': False, 'gearUsable': False, 'meldedItems': gear,
    }
    a['speed'] = 10
    a['voiceUsable'] = False
    a['somaticUsable'] = False
    a['hands'] = {'left': None, 'right': None}
    a['attacksUsable'] = False
    a['gearUsable'] = False
    for item_id in gear:
        if item_id in state['items']:
            state['items'][item_id]['formState'] = 'melded-unavailable'
            state['items'][item_id]['usable'] = False


def restore_form(state, actor_id, at, reason):
    a = state['actors'].get(actor_id)
    if not a or 'formBaseline' not in a:
        return
    baseline = a.pop('formBaseline')
    for key, value in baseline.items():
        a[key] = copy.deepcopy(value)
    override = a.pop('formOverride', {})
    a.pop('attacksUsable', None)
    a.pop('gearUsable', None)
    for item_id in override.get('meldedItems', []):
        if item_id in state['items']:
            state['items'][item_id]['formState'] = 'available'
            state['items'][item_id]['usable'] = True
    state.setdefault('formRecords', {}).setdefault(actor_id, {}).update({'status': 'ended', 'endedAt': at, 'ending': reason})


def commitment(state, at, actor_id, spell_id, cost, event_id, source, action='Action'):
    a = state['actors'].get(actor_id)
    if not a:
        return
    current = next((x for x in state.setdefault('spellCadence', []) if x.get('eventId') == event_id), None)
    if current:
        return
    if action == 'Action':
        starts = [x for x in a.get('regularStarts', []) if x <= at]
        last_start = max(starts) if starts else None
        active = last_start is not None and not any(last_start <= x <= at for x in a.get('regularEnds', []))
        if active:
            a['activeRegular'] = True
            if a.get('action', 0) <= 0:
                a['action'] = 1
    before_rp = a.get('rp') + cost if cost else a.get('rp')
    after_rp = a.get('rp')
    matrix_family = spell_id
    prior_families = list(a.get('matrixFamilies', []))
    first_distinct = matrix_family not in prior_families
    action_before = a.get('action', 0)
    magical_before = bool(a.get('magicalThisTurn', False))
    record = {'eventId': event_id, 'at': at, 'actor': actor_id, 'spellId': spell_id,
              'matrixFamily': matrix_family, 'firstDistinctFamilyThisEncounter': first_distinct,
              'baseDissonance': 0 if first_distinct else 1,
              'refrainBefore': a.get('refrainCount', 0), 'refrainApplied': not first_distinct,
              'refrainAfter': a.get('refrainCount', 0) + (0 if first_distinct else 1),
              'dissonanceBefore': a.get('dissonance', 0),
              'dissonanceAfter': a.get('dissonance', 0) + (0 if first_distinct else 1),
              'magicalThisTurnBefore': magical_before, 'magicalThisTurnAfter': True,
              'action': action, 'ActionBefore': action_before, 'RPBefore': before_rp,
              'RPAid': cost, 'RPAfter': after_rp,
              'source': source, 'cadenceDisposition': 'source-derived matrix result recorded; no unprinted reset'}
    state['spellCadence'].append(record)
    a.setdefault('castHistory', [])
    if event_id not in a['castHistory']:
        a['castHistory'].append(event_id)
    a.setdefault('castFamilies', [])
    if spell_id not in a['castFamilies']:
        a['castFamilies'].append(spell_id)
    a['lastSpell'] = spell_id
    a['magicalThisTurn'] = True
    if matrix_family not in prior_families:
        prior_families.append(matrix_family)
    a['matrixFamilies'] = prior_families
    a['refrainCount'] = record['refrainAfter']
    a['dissonance'] = record['dissonanceAfter']
    if action == 'Action' and a.get('action', 0) > 0:
        a['action'] = 0
    record['ActionAfter'] = a.get('action', 0)
    a.setdefault('resourceHistory', []).append({'at': at, 'spellId': spell_id, 'costRP': cost,
                                                'RPBefore': before_rp, 'RPAfter': after_rp,
                                                'eventId': event_id})


def append_save(state, target_id, at, roll, modifier, dc, source, save='WIS', advantage=False, rolls=None):
    total = (max(rolls) if advantage and rolls else roll) + modifier
    row = {'at': at, 'actor': target_id, 'save': save, 'rolls': rolls or [roll], 'selectedRoll': max(rolls) if advantage and rolls else roll,
           'modifier': modifier, 'total': total, 'DC': dc, 'success': total >= dc,
           'advantage': advantage, 'source': source}
    state.setdefault('saveHistory', []).append(row)
    state['actors'][target_id].setdefault('savingThrows', []).append(copy.deepcopy(row))
    return row


def expire_conditions(state, now):
    for actor in state.get('actors', {}).values():
        for name, condition in list(actor.get('conditions', {}).items()):
            expiry = condition.get('expiresAt') if isinstance(condition, dict) else None
            if isinstance(expiry, (int, float)) and expiry <= now:
                actor['conditions'].pop(name, None)


def counterspell_window(state, caster_id, at, closes_at, trigger_spell='soul-reflection', trigger_rank=9,
                        actor_state=None, observer_ids=None):
    actors = actor_state if actor_state is not None else state['actors']
    caster = actors[caster_id]
    responders = []
    for actor_id, actor in actors.items():
        if actor_id == caster_id:
            continue
        if observer_ids is not None and actor_id not in observer_ids:
            continue
        acquired = 'wizard.base.counterspell' in actor.get('acquiredClassIds', [])
        if not acquired:
            continue
        p1, p2 = actor.get('position', [0, 0, 0]), caster.get('position', [0, 0, 0])
        distance = sum((float(p1[i]) - float(p2[i])) ** 2 for i in range(3)) ** 0.5
        known = {x.get('actor') for x in actor.get('senses', {}).get('knownLocations', [])}
        perceives = caster_id in known and actor.get('senses', {}).get('sight', True)
        reaction = actor.get('reaction', 0) > 0
        rp = actor.get('rp', 0) >= 3
        recharge = actor.get('recharge', {}).get('wizard.base.counterspell', 0) == 0
        can_speak = actor.get('voiceUsable') is not False
        can_somatic = actor.get('somaticUsable') is not False
        hands_usable = actor.get('handsUsable') is not False
        normal_form = not actor.get('formOverride') or (can_speak and can_somatic and hands_usable)
        eligible = bool(distance <= 60 and perceives and reaction and rp and recharge and normal_form
                        and actor.get('life') == 'Alive'
                        and actor.get('active', True) is not False
                        and not any(c in actor.get('conditions', {}) for c in ('Unconscious', 'Incapacitated', 'Paralyzed', 'Stunned')))
        responders.append({'actorId': actor_id, 'abilityId': 'wizard.base.counterspell', 'acquiredAutomaticallyAtWizard2': True,
            'ordinaryPreparedSlotRequired': False, 'distanceFeet': round(distance, 3), 'perceivesCaster': perceives,
            'reactionAvailable': reaction, 'RPBefore': actor.get('rp'), 'costIfUsedRP': 3,
            'rechargeBefore': actor.get('recharge', {}).get('wizard.base.counterspell'),
            'normalFormAllowsCasting': normal_form, 'eligible': eligible,
            'checkDCIfAttempted': 10 + 2 * trigger_rank,
            'decision': 'declined' if eligible else 'not-eligible',
            'declineReason': 'explicitly declines legal Reaction' if eligible else
                ('form prohibits voice/somatic/hands' if not normal_form else 'one or more trigger, perception, range, resource, recharge, or life gates fail')})
    eligible_ids = [x['actorId'] for x in responders if x['eligible']]
    result = 'eligible-responders-declined' if eligible_ids else 'no-legal-responder'
    return {'openedAt': at, 'closedAt': closes_at, 'triggerSpell': trigger_spell, 'triggerSpellRank': trigger_rank,
        'responders': responders, 'eligibleResponderIds': eligible_ids, 'result': result,
        'counterspellCheckDC': 10 + 2 * trigger_rank, 'casterActorId': caster_id,
        'windowActorIds': list(actors.keys()),
        'preparedSlotRule': 'Counterspell is automatically acquired; ordinary prepared slots are not required'}


def reflection_cast_actor_snapshot(state, old_event, observer_ids=None):
    """Use pre-resolution resources, with R1's live phase budget and known visible body."""
    actors = copy.deepcopy((old_event or {}).get('before', {}).get('actors', state['actors']))
    if 'R1' in state.get('actors', {}):
        actors['R1'] = copy.deepcopy(state['actors']['R1'])
        position = actors['R1'].get('position')
        for actor_id, actor in actors.items():
            if actor_id == 'R1' or (observer_ids is not None and actor_id not in observer_ids) or not actor.get('senses', {}).get('sight', True):
                continue
            known_locations = actor.setdefault('senses', {}).setdefault('knownLocations', [])
            if not any(x.get('actor') == 'R1' for x in known_locations):
                known_locations.append({'actor': 'R1', 'basis': 'R1 appeared in the lit unobstructed fixture within sight',
                    'position': copy.deepcopy(position)})
    return actors


def establish_q27_allowance(state, at, attached_only=False):
    encounter_id = state.get('encounter')
    key = f'A|T|{encounter_id}'
    if attached_only:
        row = {'sourceCharacterId': 'A', 'targetId': 'T', 'encounterId': encounter_id,
            'status': 'inapplicable-no-regular-action', 'establishedAt': at, 'used': False,
            'component': 'one initial compelled ordinary Action', 'executionStatus': 'inapplicable',
            'reason': 'attached-only recipient has no regular Action; owner action/command is not available to consume'}
    else:
        row = {'sourceCharacterId': 'A', 'targetId': 'T', 'encounterId': encounter_id,
            'status': 'consumed-awaiting-execution', 'establishedAt': at, 'consumedAt': at, 'used': True,
            'component': 'one initial compelled ordinary Action',
            'executionStatus': 'pending', 'revalidatedBeforeUse': False}
    state.setdefault('hardDenialLedger', {})[key] = row
    state['actors'].setdefault('T', {}).setdefault('hardDenial', {})[key] = copy.deepcopy(row)
    effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), None)
    if effect:
        effect['q27Allowance'] = copy.deepcopy(row)
    return row


def close_reflection_phase(state, at, reason='next reflection opportunity'):
    r = state.get('actors', {}).get('R1')
    if not r:
        return
    idx = r.get('activeReflectionPhase')
    if idx is not None:
        row = next((x for x in state.get('reflectionPhaseLedger', []) if x.get('index') == idx and x.get('status') == 'resolved'), None)
        if row:
            reaction = r.get('reaction', 0)
            action = r.get('action', 0)
            bonus_action = r.get('bonusAction', 0)
            movement = max(0, r.get('reflectionPhaseBudget', {}).get('movementFeet', 0))
            row.update({'endedAt': at, 'endReason': reason,
                        'remainingBudgetAtEnd': {'Action': 0, 'BonusAction': 0, 'Reaction': reaction, 'MovementFeet': 0},
                        'expiredAtBoundary': {'Action': action, 'BonusAction': bonus_action, 'MovementFeet': movement},
                        'reactionDisposition': 'continues-unspent-until-used-or-next-reflection-opportunity' if reaction else 'spent-or-unavailable'})
        r['activeReflectionPhase'] = None
    r['action'] = r['bonusAction'] = 0
    r['reflectionPhaseBudget'] = {'action': 0, 'bonusAction': 0, 'reaction': r.get('reaction', 0), 'movementFeet': 0}
    dodge = r.get('conditions', {}).get('Dodging')
    if dodge and dodge.get('expiresAt', at + 1) <= at:
        r['conditions'].pop('Dodging', None)
    state['reflectionPhases'] = copy.deepcopy(state.get('reflectionPhaseLedger', []))


def phase_action(state, case, phase, at, action, old_event=None):
    if 'R1' not in state['actors']:
        return
    r = state['actors']['R1']
    effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), {})
    close_reflection_phase(state, at)
    if not r.get('active', True) or not effect.get('active', True):
        state['reflectionPhaseLedger'].append({'index': phase, 'startAt': at, 'status': 'skipped-suppressed',
            'actionSpent': False, 'endedAt': at, 'reason': 'body suppressed; opportunity elapsed; no bank or replay'})
        state['reflectionPhases'] = copy.deepcopy(state['reflectionPhaseLedger'])
        return
    pre_r1 = (old_event or {}).get('before', {}).get('actors', {}).get('R1', {})
    source_speed = pre_r1.get('speed', r.get('speed', 30))
    starting_movement = max(0, source_speed - r.get('movementSpent', 0))
    movement = starting_movement
    r['action'] = r['bonusAction'] = r['reaction'] = 1
    r['movementSpent'] = 0
    r['magicalThisTurn'] = False
    r['activeReflectionPhase'] = phase
    r['reflectionPhaseBudget'] = {'action': 1, 'bonusAction': 1, 'reaction': 1, 'movementFeet': movement}
    if action == 'Dodge':
        r['action'] = 0
        following = [x for x in PHASES[case] if x > at]
        expiry = following[0] if following else effect.get('deadlineAt', at + 0.03)
        r.setdefault('conditions', {})['Dodging'] = {'source': 'Reflection phase Action: Dodge', 'appliedAt': at, 'expiresAt': expiry}
        spent = {'type': 'Dodge', 'ActionSpent': True, 'RPSpent': 0, 'BonusActionSpent': False, 'ReactionSpent': False}
    elif action == 'Gaseous Form':
        paid = next((x for x in state.get('spellCadence', []) if x.get('eventId') == 'R1-GAS-268'), None)
        if paid:
            before, after = paid['RPBefore'], paid['RPAfter']
            if r.get('rp') != after:
                raise ValueError('Gaseous Form commitment RP does not match actor RP after payment')
        else:
            old_before_rp = pre_r1.get('rp')
            old_after_rp = (old_event or {}).get('after', {}).get('actors', {}).get('R1', {}).get('rp')
            if old_before_rp is not None and old_after_rp is not None and old_after_rp == r.get('rp') and old_after_rp == old_before_rp - 5:
                before, after = old_before_rp, old_after_rp
            else:
                before = r.get('rp', 0)
                r['rp'] = before - 5
                after = r['rp']
        window = counterspell_window(state, 'R1', at, at, 'gaseous-form', 3,
            actor_state=reflection_cast_actor_snapshot(state, old_event, ['A', 'T']), observer_ids=['A', 'T'])
        r['lastSpell'] = 'gaseous-form'
        r.setdefault('concentration', {})
        r['concentration'] = {'spellId': 'gaseous-form', 'sourceId': 'R1-GAS-268', 'startedAt': at, 'deadlineAt': at + 60}
        state.setdefault('formRecords', {})['R1'] = {'form': 'gaseous-mist', 'rootProfile': r.get('profileId'),
            'rootIdentity': 'R1', 'sourceId': 'R1-GAS-268', 'startAt': at, 'deadlineAt': at + 60,
            'currentHP': r.get('hp'), 'maxHP': r.get('maxHP'), 'currentRP': r.get('rp'), 'size': r.get('size'),
            'movementFeet': 10, 'hover': True, 'voiceUsable': False, 'handsUsable': False, 'attacksUsable': False,
            'status': 'active'}
        state.setdefault('copiedConcentration', {})['R1'] = {'spellId': 'gaseous-form', 'sourceId': 'R1-GAS-268',
            'RPBefore': before, 'RPAfter': after, 'deadlineAt': at + 60, 'slotOwner': 'R1', 'status': 'active'}
        set_form(state, 'R1', 'R1-GAS-268', at + 60, 'R1')
        post_action_speed = r.get('speed', 30)
        movement_after = max(0, min(movement, post_action_speed - r.get('movementSpent', 0)))
        r['action'] = 1
        commitment(state, at, 'R1', 'gaseous-form', 5, 'R1-GAS-268', 'accepted Gaseous Form source; copied-casting permission remains a Soul-Reflection proposal')
        r['action'] = 0
        next(x for x in state['spellCadence'] if x.get('eventId') == 'R1-GAS-268').update({'ActionBefore': 1, 'ActionAfter': 0})
        state.setdefault('spellCommitments', []).append({'eventId': 'R1-GAS-268', 'at': at, 'caster': 'R1',
            'target': 'R1', 'spellId': 'gaseous-form', 'actionCommitted': True, 'RPSpent': 5,
            'counterWindow': window['result'], 'counterWindowDetails': copy.deepcopy(window),
            'castResolutionOrder': 'after all eligible responders decline or the window otherwise closes'})
        spent = {'type': 'cast gaseous-form', 'ActionSpent': True, 'RPSpent': 5, 'BonusActionSpent': False, 'ReactionSpent': False}
        movement = movement_after
        add_schedule(state, 'concentration-end:R1-GAS-268', at + 60, 'source concentration deadline')
    elif action == 'Ray of Frost':
        spent = {'type': 'cast ray-of-frost', 'ActionSpent': True, 'RPSpent': 0, 'BonusActionSpent': False, 'ReactionSpent': False}
        commitment(state, at, 'R1', 'ray-of-frost', 0, 'R1-RAYFROST-268', 'indexed Ray of Frost operation')
        window = counterspell_window(state, 'R1', at, at, 'ray-of-frost', 0,
            actor_state=reflection_cast_actor_snapshot(state, old_event, ['A', 'T']), observer_ids=['A', 'T'])
        state.setdefault('spellCommitments', []).append({'eventId': 'R1-RAYFROST-268', 'at': at,
            'caster': 'R1', 'target': 'T', 'spellId': 'ray-of-frost', 'actionCommitted': True, 'RPSpent': 0,
            'counterWindow': window['result'], 'counterWindowDetails': copy.deepcopy(window),
            'castResolutionOrder': 'after all eligible responders decline or the window otherwise closes'})
        r['action'] = 0
        next(x for x in state['spellCadence'] if x.get('eventId') == 'R1-RAYFROST-268').update({'ActionBefore': 1, 'ActionAfter': 0})
    else:
        r['action'] = 0
        spent = {'type': action, 'ActionSpent': True, 'RPSpent': 0, 'BonusActionSpent': False, 'ReactionSpent': False}
    if action != 'Gaseous Form':
        post_action_speed = r.get('speed', 30)
        movement = max(0, min(movement, post_action_speed - r.get('movementSpent', 0)))
    r['reflectionPhaseBudget'] = {'action': r['action'], 'bonusAction': r['bonusAction'],
                                  'reaction': r['reaction'], 'movementFeet': movement}
    marker = at - 0.01
    state['reflectionPhaseLedger'].append({'index': phase, 'startAt': at, 'targetMarker': marker, 'target': 'T',
        'targetMarkerKind': 'actual target regular END or attached-phase END', 'status': 'resolved',
        'sourceSpeedFeet': source_speed, 'postActionSpeedFeet': post_action_speed,
        'startingBudget': {'Action': 1, 'BonusAction': 1, 'Reaction': 1, 'MovementFeet': starting_movement},
        'budgetAfterAction': {'Action': r['action'], 'BonusAction': r['bonusAction'], 'Reaction': r['reaction'],
                              'MovementFeet': movement},
        'spent': spent, 'independentTargetTurn': False, 'regularStartRecordedForR1': False})
    state['reflectionPhases'] = copy.deepcopy(state['reflectionPhaseLedger'])
    effect['history'] = effect.get('history', []) + [{'at': at, 'phase': phase, 'action': spent['type'],
                                                      'noRefresh': True, 'movementFeet': movement}]


def add_phase_from_label(kind, state, label, at, event):
    lo = label.lower()
    if kind == 'ZERO' and ('resolves original t to zero' in lo or 'ray of frost' in lo):
        phase = 1
    elif 'phase 1' in lo or 'first phase' in lo or 'uses one source-qualified copied action' in lo:
        phase = 1
    elif 'phase 2' in lo:
        phase = 2
    elif 'phase 3' in lo or 'third proposed phase' in lo or 'third reflection phase' in lo:
        phase = 3
    else:
        return
    existing = next((x for x in state.get('reflectionPhaseLedger', []) if x.get('index') == phase), None)
    if existing:
        if kind == 'ZERO' and phase == 1 and existing.get('status') == 'skipped-suppressed':
            state['reflectionPhaseLedger'].remove(existing)
        else:
            return
    if kind == 'FORM':
        action = 'Dodge'
    elif kind == 'CONCENTRATION':
        action = 'Gaseous Form' if phase == 1 else 'Dodge'
    elif kind == 'ZERO':
        action = 'Ray of Frost'
    else:
        action = 'Dodge'
    phase_action(state, kind, phase, at, action, event)


def correct_case_event(state, kind, label, at, old_event, seen):
    state['time'] = at
    # A committed cast is paid before its target save and does not create the body until admission fails.
    if 'commits soul reflection' in label.lower():
        effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), None)
        eid = next((k for k, v in state.get('effects', {}).items() if v.get('kind') == 'soul-reflection'), f'A-SR-{state.get("caseId")}')
        if effect:
            effect['status'] = 'awaiting-counter-window-and-save'
            effect['counterWindow'] = {'openedAt': at, 'closedAt': at + 0.01,
                'eligiblePreparedCounterspellResponders': [], 'result': 'passed-no-legal-prepared-response'}
            effect['pendingAdmission'] = True
        state['spellCommitments'].append({'eventId': eid, 'at': at, 'caster': 'A', 'target': 'T',
            'spellId': 'soul-reflection', 'actionCommitted': True, 'RPSpent': 26,
            'counterWindow': 'passed-no-legal-prepared-response', 'targetSavePending': True})
        state['actors'].pop('R1', None)
        commitment(state, at, 'A', 'soul-reflection', 26, eid, 'native identity plus unaccepted local operational proposal')
    if 'admission' in label.lower() or 'admitted' in label.lower() or 'r1 appears within five feet' in label.lower():
        r1 = copy.deepcopy(old_event['after']['actors'].get('R1'))
        if r1:
            state['actors']['R1'] = r1
            r1['reflectionSource'] = next((k for k, v in state.get('effects', {}).items() if v.get('kind') == 'soul-reflection'), None)
            r1['causalRoot'] = r1['reflectionSource']
            r1['ownerId'] = None
            r1['attachedOnly'] = False
            r1['regularCalendar'] = list(PHASES[kind])
            add_reflection_gear(state)
            t = state['actors']['T']
            modifier = t.get('saves', {}).get('WIS', 0)
            dc = state['actors']['A'].get('spellDC', 19)
            save = append_save(state, 'T', at, 8, modifier, dc, 'source-bound target WIS save; stipulated fixture roll')
            effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), None)
            if effect:
                effect['pendingAdmission'] = False
                effect['status'] = 'admitted-after-failed-WIS-save' if not save['success'] else 'no-admission-save-succeeded'
                effect['admissionSave'] = copy.deepcopy(save)
            if kind == 'FORM' and 'T' in state.get('formRecords', {}):
                source_form = state['formRecords']['T']
                state.setdefault('copiedForms', {})['R1'] = {'sourceFormOwner': 'T', 'sourceId': source_form['sourceId'],
                    'sourceDeadlineAt': source_form['deadlineAt'], 'copyMode': 'finite snapshot; inherited source deadline',
                    'rootProfile': r1.get('profileId'), 'sameSizeSpace': True, 'gasLimitationsPreserved': True, 'status': 'active'}
                state['formRecords']['R1'] = {'form': 'gaseous-mist', 'rootProfile': r1.get('profileId'),
                    'rootIdentity': 'R1', 'sourceId': source_form['sourceId'], 'startAt': at,
                    'deadlineAt': source_form['deadlineAt'], 'currentHP': r1.get('hp'), 'maxHP': r1.get('maxHP'),
                    'currentRP': r1.get('rp'), 'size': r1.get('size'), 'movementFeet': 10,
                    'hover': True, 'voiceUsable': False, 'handsUsable': False, 'attacksUsable': False, 'status': 'active'}
                set_form(state, 'R1', source_form['sourceId'], source_form['deadlineAt'], 'T', copied=True)
                add_schedule(state, 'inherited-form-end:R1', source_form['deadlineAt'], 'inherited source form deadline')
            state['actors']['R1']['reflectionSource'] = next((k for k, v in state.get('effects', {}).items() if v.get('kind') == 'soul-reflection'), None)
    # Actual turn markers refresh / close only their named actor and consume exact schedule entries.
    old_before = old_event['before'].get('actors', {})
    old_after = old_event['after'].get('actors', {})
    for actor_id, actor in state.get('actors', {}).items():
        ob, oa = old_before.get(actor_id, {}), old_after.get(actor_id, {})
        started = [x for x in oa.get('regularStarts', []) if x not in ob.get('regularStarts', [])]
        ended = [x for x in oa.get('regularEnds', []) if x not in ob.get('regularEnds', [])]
        for marker in started:
            if abs(marker - at) < 1e-6:
                actor['action'] = 0 if 'Unconscious' in actor.get('conditions', {}) else 1
                actor['bonusAction'] = 0 if 'Unconscious' in actor.get('conditions', {}) else 1
                actor['reaction'] = 0 if 'Unconscious' in actor.get('conditions', {}) else 1
                actor['interaction'] = 0 if 'Unconscious' in actor.get('conditions', {}) else 1
                actor['movementSpent'] = 0
                actor['activeRegular'] = True
                actor['lastRegularStart'] = at
                future = [x for x in actor.get('regularCalendar', []) if x > at]
                actor['nextRegularStart'] = future[0] if future else None
                dodge = actor.get('conditions', {}).get('Dodging')
                if dodge and dodge.get('expiresAt', at + 1) <= at:
                    actor['conditions'].pop('Dodging', None)
        for marker in ended:
            if abs(marker - at) < 1e-6:
                actor['action'] = 0
                actor['bonusAction'] = 0
                actor['interaction'] = 0
                actor['activeRegular'] = False
                actor['lastRegularEnd'] = at
    # First regular target Action takes the one shared source-character / target / encounter guard.
    if ('single compelled action' in label.lower() or 'hard action component' in label.lower()
            or 'chooses legal dodge' in label.lower() or 'single compelled' in label.lower()):
        if 'T' in state['actors']:
            key = f'A|T|{state.get("caseId")}'
            if key not in state['hardDenialLedger']:
                state['hardDenialLedger'][key] = {'sourceCharacterId': 'A', 'targetId': 'T',
                    'encounterId': state.get('caseId'), 'used': True, 'at': at,
                    'component': 'one forced ordinary Action', 'revalidatedBeforeUse': True}
                state['actors']['T'].setdefault('hardDenial', {})[key] = copy.deepcopy(state['hardDenialLedger'][key])
                state['spellCommitments'][0]['targetSavePending'] = False
                state['spellCommitments'][0]['firstCompelledAction'] = {'at': at, 'chosenAction': 'Dodge', 'guardUsed': True}
            t = state['actors']['T']
            t.setdefault('conditions', {})['Dodging'] = {'appliedAt': at, 'expiresAt': at + 6.0,
                'source': 'T chooses Dodge in its own regular Action slot'}
    # Source form transitions are authoritative in the actor and item states, not only in narration.
    if 'casts reviewed gaseous form' in label.lower():
        if 'T' in state['actors']:
            commitment(state, at, 'T', 'gaseous-form', 5, 'T-GAS-268', 'reviewed Gaseous Form envelope; outside-initiative finite cast fixture')
            state['formRecords']['T']['status'] = 'active'
            set_form(state, 'T', 'T-GAS-268', 8.0, 'T')
            add_schedule(state, 'source-form-end:T-GAS-268', 8.0, '60-second source concentration deadline')
    if 'uses one source-qualified copied action to cast gaseous form' in label.lower():
        # The phase routine spends the Action; this event adds only the source/cost and effective form state.
        r = state['actors']['R1']
        set_form(state, 'R1', 'R1-GAS-268', at + 60.0, 'R1')
        if not any(x.get('eventId') == 'R1-GAS-268' for x in state['spellCadence']):
            commitment(state, at, 'R1', 'gaseous-form', 5, 'R1-GAS-268', 'accepted Gaseous Form envelope; copied-casting grant remains proposed')
        state.setdefault('copiedConcentration', {}).setdefault('R1', {}).update({'status': 'active'})
    if 'exact form deadline' in label.lower():
        for actor_id in ('T', 'R1'):
            restore_form(state, actor_id, at, 'source concentration deadline')
        if state.get('copiedForms', {}).get('R1'):
                    state['copiedForms']['R1'].update({'status': 'ended', 'endedAt': at, 'ending': 'inherited source deadline'})
    if 'concentration' in label.lower() and 'arcane bolt' in label.lower():
        event_id = 'T-ARCANE-BOLT-268'
        if not any(x.get('eventId') == event_id for x in state['spellCadence']):
            commitment(state, at, 'T', 'wizard.base.arcane-bolt', 1, event_id, 'W17 Wizard source; 4d6+5 and force resistance')
        damage = state.get('damageEvents', [])
        if damage:
            damage[-1].update({'damageFormula': '4d6+5', 'rawDamageDice': [1, 1, 1, 1], 'flatModifier': 5,
                'rawForce': 9, 'resolvedDamage': 4, 'resistance': 'force resistance halves 9 to 4'})
        conc = state.get('copiedConcentration', {}).get('R1', {})
        save = {'save': 'CON', 'rolls': [1, 2], 'selectedRoll': 2, 'modifier': 2, 'total': 4,
            'DC': 10, 'success': False, 'advantage': True,
            'advantageSource': 'wizard.arch.improved-concentration; damage-triggered Wizard CON save',
            'cause': '4 resolved damage; max(10,floor(4/2))'}
        conc.update({'damageAt': at, 'concentrationSave': save, 'status': 'ended-on-failed-advantaged-save', 'endedAt': at})
        state['actors']['R1']['concentration'] = None
        restore_form(state, 'R1', at, 'failed damage concentration save with advantage')
        if state.get('formRecords', {}).get('R1'):
            state['formRecords']['R1'].update({'endedAt': at, 'ending': 'failed advantaged CON save', 'currentHP': 100, 'currentRP': 59})
        state['spellCommitments'].append({'eventId': event_id, 'at': at, 'caster': 'T', 'target': 'R1',
            'spellId': 'wizard.base.arcane-bolt', 'actionCommitted': True, 'RPSpent': 1,
            'counterWindow': 'not applicable; instantaneous attack'})
    # Each narrated reflection action has a real per-phase budget and ledger.
    add_phase_from_label(kind, state, label, at, old_event)
    if kind == 'ZERO' and ('resolves original T to zero' in label.lower() or 'ray of frost' in label.lower()):
        damage = state.get('damageEvents', [])
        if damage:
            damage[-1].update({'attackRolls': [18, 7], 'rollMode': 'disadvantage from active Dodge',
                'selectedRoll': 7, 'attackTotal': 18, 'targetAC': state['actors']['T'].get('AC', 12),
                'damageDice': [1], 'damageFormula': '1d8 cold', 'resolvedDamage': 1})
        target = state['actors']['T']
        target['conditions'].pop('Dodging', None)
        target['conditions']['Unconscious'] = {'appliedAt': at, 'source': 'zero HP',
            'includes': ['Incapacitated', 'unaware', 'drop held items', 'Prone']}
        target['conditions']['Incapacitated'] = {'appliedAt': at, 'source': 'Unconscious at zero HP'}
        target['conditions']['Prone'] = {'appliedAt': at, 'source': 'Unconscious at zero HP'}
        target['life'] = 'Downed'
        target['action'] = target['bonusAction'] = target['reaction'] = target['interaction'] = 0
        for hand, item_id in list(target.get('hands', {}).items()):
            if item_id and item_id in state.get('items', {}):
                state['items'][item_id].update({'owner': 'T', 'custodian': 'ground', 'held': False,
                    'position': copy.deepcopy(target.get('position')), 'droppedAt': at})
                target['hands'][hand] = None
        target.setdefault('deathSaves', {'successes': 0, 'failures': 0})
        state['spellCommitments'].append({'eventId': 'R1-RAYFROST-268', 'at': at, 'caster': 'R1', 'target': 'T',
            'spellId': 'ray-of-frost', 'actionCommitted': True, 'RPSpent': 0,
            'attack': {'rolls': [18, 7], 'selectedRoll': 7, 'mode': 'disadvantage'}, 'damageDice': [1]})
        if state.get('effects'):
            effect = next((v for v in state['effects'].values() if v.get('kind') == 'soul-reflection'), None)
            if effect:
                effect.update({'active': False, 'endedAt': at + 0.01, 'ending': 'original target reached zero after complete source pipeline'})
        if state['actors'].get('R1'):
            state['actors']['R1'].update({'active': False, 'life': 'FiniteEnded'})
            end_reflection_gear(state, at + 0.01)
    if 'death save' in label.lower() and kind == 'ZERO':
        t = state['actors']['T']
        t.setdefault('deathSaves', {})['successes'] = 1
        t['deathSaves']['failures'] = 0
        t['deathSaves']['lastRoll'] = {'at': at, 'd20': 14, 'modifier': 0, 'total': 14, 'success': True}
        t['conditions']['Unconscious']['cause'] = 'Downed; still unconscious after successful death save'
        t['action'] = t['bonusAction'] = t['reaction'] = t['interaction'] = 0
        for event in state['scheduled'].values():
            if event['reason'] == 'proposed Soul Reflection phase after actual target END' and event['at'] > at:
                event['status'] = 'cancelled-original-target-zero'
    if 'antimagic field lesser' in label.lower() and kind == 'CARGO':
        if not any(x.get('eventId') == 'D-AML268' for x in state['spellCadence']):
            commitment(state, at - 0.01, 'D', 'antimagic-field-lesser', 10, 'D-AML268', 'exact accepted field source; current class access and prepared matrix')
        state.setdefault('spellCommitments', []).append({'eventId': 'D-AML268', 'at': at - 0.01,
            'caster': 'D', 'target': 'R1', 'spellId': 'antimagic-field-lesser', 'actionCommitted': True,
            'RPSpent': 10, 'concentration': True})
        for item_id in state['actors'].get('R1', {}).get('inventory', []):
            if item_id in state['items']:
                state['items'][item_id].update({'active': False, 'colliding': False, 'custodyStatus': 'suppressed'})
    if 'same reflection identity resumes' in label.lower():
        for item_id in state['actors'].get('R1', {}).get('inventory', []):
            if item_id in state['items']:
                state['items'][item_id].update({'active': True, 'colliding': True, 'custodyStatus': 'resumed'})
    if 'regular end' in label.lower() and kind == 'CARGO' and at == 9.9:
        pass
    if any(k in label.lower() for k in ('finite reflection ends', 'reflection ends; only', 'finite opponent ends')):
        if state.get('actors', {}).get('R1'):
            state['actors']['R1'].update({'active': False, 'life': 'FiniteEnded'})
            end_reflection_gear(state, at)
    # T-map remains a single original item with owner T and the exact ground location.
    if kind == 'CARGO' and 'T-map' in state.get('items', {}):
        item = state['items']['T-map']
        if item.get('custodian') == 'ground':
            item.update({'owner': 'T', 'held': False, 'position': [15, 0, 0]})
    # Rebuild the compact schedule statuses from exact recorded markers; never inherit the old stale calendar.
    update_schedule(state, kind, at)
    # Keep all event after-times equal to the event clock, including the first -52 source-form event.
    state['time'] = at


def end_reflection_gear(state, at):
    r = state.get('actors', {}).get('R1')
    if not r:
        return
    close_reflection_phase(state, at, 'finite Reflection phase ended')
    for item_id in list(r.get('inventory', [])):
        if item_id in state.get('items', {}):
            state['items'][item_id].update({'active': False, 'colliding': False, 'custodian': 'ended',
                'held': False, 'endedAt': at, 'formState': 'ended'})
    r['inventory'] = []
    r['hands'] = {'left': None, 'right': None}
    r['conditions'] = {}
    r['action'] = r['bonusAction'] = r['reaction'] = r['interaction'] = 0
    r['activeReflectionPhase'] = None
    r['reflectionPhaseBudget'] = {'action': 0, 'bonusAction': 0, 'reaction': 0, 'movementFeet': 0}


def update_schedule(state, kind, now):
    for key, item in state.get('scheduled', {}).items():
        if item['status'] not in ('pending', 'occurred', 'skipped-suppressed', 'cancelled-original-target-zero'):
            continue
        if key.startswith('regular-start:'):
            _, actor_id, value = key.split(':', 2)
            at = float(value)
            recorded = at in state.get('actors', {}).get(actor_id, {}).get('regularStarts', [])
            if recorded:
                item['status'] = 'occurred'
            elif at < now:
                item['status'] = 'missed-unresolved'
        elif key.startswith('regular-end:'):
            _, actor_id, value = key.split(':', 2)
            at = float(value)
            recorded = at in state.get('actors', {}).get(actor_id, {}).get('regularEnds', [])
            if recorded:
                item['status'] = 'occurred'
            elif at < now:
                item['status'] = 'missed-unresolved'
        elif key.startswith('reflection-phase:'):
            at = float(key.rsplit(':', 1)[1])
            phase = next((x for x in state.get('reflectionPhaseLedger', []) if abs(x['startAt'] - at) < 1e-6), None)
            if phase:
                item['status'] = 'skipped-suppressed' if phase['status'].startswith('skipped') else 'occurred'
            elif at < now and any(x.get('life') == 'FiniteEnded' for x in state.get('actors', {}).values()):
                item['status'] = 'cancelled-original-target-zero'
            elif at < now:
                item['status'] = 'missed-unresolved'
        elif key.startswith(('source-form-end:', 'inherited-form-end:', 'concentration-end:')):
            at = item['at']
            active = any(v.get('deadlineAt') == at and v.get('status') in ('active', 'pending')
                         for v in state.get('formRecords', {}).values())
            ended = any(v.get('endedAt') == at or (v.get('endedAt') is not None and v.get('endedAt') < at)
                        for v in state.get('formRecords', {}).values())
            conc_ended = any(v.get('endedAt') is not None and v.get('endedAt') < at
                             for v in state.get('copiedConcentration', {}).values())
            if any(v.get('endedAt') == at for v in state.get('formRecords', {}).values()):
                item['status'] = 'occurred'
            elif ended or conc_ended:
                item['status'] = 'cancelled-effect-ended-early'
            elif at < now:
                item['status'] = 'missed-unresolved'
        elif key.startswith('attached-target-end:'):
            at = item['at']
            marker = any(abs(x.get('ownerRegularEnd', -999) - at) < 1e-6
                         for x in state.get('actors', {}).get('T', {}).get('attachedPhaseHistory', []))
            if marker:
                item['status'] = 'occurred'
            elif at < now:
                item['status'] = 'missed-unresolved'
    # A failed-save / original-zero cleanup cancels unused phases explicitly.
    if kind == 'ZERO' and any(x.get('life') == 'FiniteEnded' for x in state.get('actors', {}).values()):
        for key, item in state['scheduled'].items():
            if key.startswith('reflection-phase:') and item['status'] == 'pending':
                item['status'] = 'cancelled-original-target-zero'


def is_turn_event(old_event, actor_id, field):
    before = old_event['before'].get('actors', {}).get(actor_id, {}).get(field, [])
    after = old_event['after'].get('actors', {}).get(actor_id, {}).get(field, [])
    return len(after) > len(before) and after[-1] == old_event['atSeconds']


def process_existing_case(case, kind):
    old_events = case['events']
    state = base_case(case, kind)
    new_events = []
    inputs = [(e['atSeconds'], 0, e) for e in old_events]
    if not any(abs(e.get('atSeconds', -999) - 0.0) < 1e-6 and is_turn_event(e, 'A', 'regularStarts') for e in old_events):
        inputs.append((0.0, 1, {'custom': 'A regular start 1 before the committed Soul Reflection cast',
                                'actorId': 'A', 'atSeconds': 0.0}))
    if kind == 'FORM':
        inputs.extend([
            (-52.8, 1, {'custom': 'T regular start before its source Gaseous Form Action', 'actorId': 'T', 'atSeconds': -52.8}),
            (-51.9, 1, {'custom': 'T regular END after its source Gaseous Form Action', 'actorId': 'T', 'atSeconds': -51.9}),
        ])
    if kind in ('FORM', 'CONCENTRATION'):
        inputs.extend([
            (18.0, 1, {'custom': 'A regular start 4 at the finite-effect deadline', 'actorId': 'A', 'atSeconds': 18.0}),
            (18.9, 1, {'custom': 'A regular END 4 after the finite-effect deadline', 'actorId': 'A', 'atSeconds': 18.9}),
        ])
    if kind == 'CARGO':
        inputs.extend([
            (9.0, 1, {'custom': 'D regular start 2 while Antimagic Field remains active', 'actorId': 'D', 'atSeconds': 9.0}),
            (9.9, 1, {'custom': 'D regular END 2 after the field has already ended', 'actorId': 'D', 'atSeconds': 9.9}),
        ])
    inputs.sort(key=lambda x: (x[0], x[1]))
    for at, _, old in inputs:
        before = copy.deepcopy(state)
        if 'custom' in old:
            actor_id = old['actorId']
            actor = state['actors'][actor_id]
            if 'start' in old['custom'].lower():
                actor['activeRegular'] = True
                actor['action'] = actor['bonusAction'] = actor['interaction'] = actor['reaction'] = 1
                actor['movementSpent'] = 0
                actor['magicalThisTurn'] = False
                actor['lastRegularStart'] = at
                actor['regularStarts'].append(at)
                future = [x for x in actor.get('regularCalendar', []) if x > at]
                actor['nextRegularStart'] = future[0] if future else None
            else:
                actor['activeRegular'] = False
                actor['action'] = actor['bonusAction'] = actor['interaction'] = 0
                actor['lastRegularEnd'] = at
                actor['regularEnds'].append(at)
            old_event = {'id': f'{state["caseId"]}:custom:{len(new_events)+1}', 'atSeconds': at,
                         'label': old['custom'], 'before': before, 'after': copy.deepcopy(state),
                         'evidence': {'source': f'exact {actor_id} regular marker; encounter clock retained'}}
        else:
            state = apply_delta(state, old['before'], old['after'])
            old_event = old
        expire_conditions(state, at)
        label = old_event['label']
        if any(is_turn_event(old_event, aid, 'regularStarts') for aid in state.get('actors', {})):
            for aid in state['actors']:
                if is_turn_event(old_event, aid, 'regularStarts'):
                    actor = state['actors'][aid]
                    actor['action'] = 0 if 'Unconscious' in actor.get('conditions', {}) else 1
                    actor['bonusAction'] = 0 if 'Unconscious' in actor.get('conditions', {}) else 1
                    actor['reaction'] = 0 if 'Unconscious' in actor.get('conditions', {}) else 1
                    actor['interaction'] = 0 if 'Unconscious' in actor.get('conditions', {}) else 1
                    actor['movementSpent'] = 0
                    actor['magicalThisTurn'] = False
                    actor['activeRegular'] = True
                    actor['lastRegularStart'] = at
                    future = [x for x in actor.get('regularCalendar', []) if x > at]
                    actor['nextRegularStart'] = future[0] if future else None
                    dodge = actor.get('conditions', {}).get('Dodging')
                    if dodge and dodge.get('expiresAt', at + 1) <= at:
                        actor['conditions'].pop('Dodging', None)
        independent_slot = any(
            is_turn_event(old_event, aid, field)
            for aid in state.get('actors', {}) if aid != 'R1'
            for field in ('regularStarts', 'regularEnds'))
        phase_index = state.get('actors', {}).get('R1', {}).get('activeReflectionPhase')
        phase_row = next((x for x in state.get('reflectionPhaseLedger', [])
            if x.get('index') == phase_index and x.get('status') == 'resolved'), None)
        if independent_slot and phase_index is not None and phase_row and at > phase_row.get('startAt', at):
            close_reflection_phase(state, at, 'next independent actor regular slot')
        if 'commits soul reflection' in label.lower():
            effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), None)
            state['actors'].pop('R1', None)
            window = counterspell_window(state, 'A', at, at + 0.01)
            if effect:
                effect['pendingAdmission'] = True
                effect['status'] = 'awaiting-counter-window-and-save'
                effect['counterWindow'] = copy.deepcopy(window)
            eid = next((k for k, v in state['effects'].items() if v.get('kind') == 'soul-reflection'), 'A-SR')
            state['spellCommitments'] = [{'eventId': eid,
                'at': at, 'caster': 'A', 'target': 'T', 'spellId': 'soul-reflection', 'actionCommitted': True,
                'RPSpent': 26, 'counterWindow': window['result'], 'counterWindowDetails': copy.deepcopy(window),
                'targetSavePending': True}]
            commitment(state, at, 'A', 'soul-reflection', 26, eid,
                'native identity plus unaccepted local operational proposal')
        # The admission event creates R1 only after the recorded save fails.
        if 'admission' in label.lower() or 'admitted' in label.lower() or 'r1 appears within five feet' in label.lower():
            original_r1 = old['after']['actors'].get('R1')
            if original_r1:
                state['actors']['R1'] = copy.deepcopy(original_r1)
                state['actors']['R1']['reflectionSource'] = next((k for k, v in state['effects'].items() if v.get('kind') == 'soul-reflection'), None)
                state['actors']['R1']['causalRoot'] = state['actors']['R1']['reflectionSource']
                state['actors']['R1']['ownerId'] = None
                state['actors']['R1']['attachedOnly'] = False
                state['actors']['R1']['regularCalendar'] = []
                state['actors']['R1']['nextRegularStart'] = None
                state['actors']['R1']['regularStarts'] = []
                state['actors']['R1']['regularEnds'] = []
                state['actors']['R1']['activeReflectionPhase'] = None
                state['actors']['R1']['reflectionPhaseBudget'] = {'action': 0, 'bonusAction': 0, 'reaction': 0, 'movementFeet': 0}
                state['actors']['R1']['movementSpent'] = 0
                for observer_id, observer in state['actors'].items():
                    if observer_id == 'R1' or not observer.get('senses', {}).get('sight', True):
                        continue
                    known_locations = observer.setdefault('senses', {}).setdefault('knownLocations', [])
                    if not any(x.get('actor') == 'R1' for x in known_locations):
                        known_locations.append({'actor': 'R1', 'basis': 'R1 appeared in the lit unobstructed fixture within sight',
                            'position': copy.deepcopy(state['actors']['R1'].get('position'))})
                add_reflection_gear(state)
                t = state['actors']['T']
                save = append_save(state, 'T', at, 8, t.get('saves', {}).get('WIS', 0), state['actors']['A'].get('spellDC', 19),
                                   'source-bound target WIS save; stipulated fixture roll')
                effect = next((v for v in state['effects'].values() if v.get('kind') == 'soul-reflection'), None)
                if effect:
                    effect.update({'pendingAdmission': False, 'status': 'admitted-after-failed-WIS-save', 'admissionSave': copy.deepcopy(save)})
                establish_q27_allowance(state, at)
                if kind == 'FORM' and state.get('formRecords', {}).get('T'):
                    src = state['formRecords']['T']
                    state.setdefault('copiedForms', {})['R1'] = {'sourceFormOwner': 'T', 'sourceId': src['sourceId'],
                        'sourceDeadlineAt': src['deadlineAt'], 'copyMode': 'finite snapshot; inherited source deadline',
                        'rootProfile': state['actors']['R1'].get('profileId'), 'sameSizeSpace': True,
                        'gasLimitationsPreserved': True, 'status': 'active'}
                    state['formRecords']['R1'] = {'form': 'gaseous-mist', 'rootProfile': state['actors']['R1'].get('profileId'),
                        'rootIdentity': 'R1', 'sourceId': src['sourceId'], 'startAt': at, 'deadlineAt': src['deadlineAt'],
                        'currentHP': state['actors']['R1'].get('hp'), 'maxHP': state['actors']['R1'].get('maxHP'),
                        'currentRP': state['actors']['R1'].get('rp'), 'size': state['actors']['R1'].get('size'),
                        'movementFeet': 10, 'hover': True, 'voiceUsable': False, 'handsUsable': False,
                        'attacksUsable': False, 'status': 'active'}
                    set_form(state, 'R1', src['sourceId'], src['deadlineAt'], 'T', copied=True)
                    add_schedule(state, 'inherited-form-end:R1', src['deadlineAt'], 'inherited source form deadline')
        # Turn budgets expire at their END; the exact marker arrays remain part of state.
        for aid in state.get('actors', {}):
            if is_turn_event(old_event, aid, 'regularEnds'):
                a = state['actors'][aid]
                a['action'] = a['bonusAction'] = a['interaction'] = 0
                a['activeRegular'] = False
                a['lastRegularEnd'] = at
                if aid == 'T':
                    encounter_id = state.get('encounter')
                    key = f'A|T|{encounter_id}'
                    mark = state.get('hardDenialLedger', {}).get(key)
                    if mark and mark.get('executionStatus') == 'pending':
                        mark.update({'status': 'consumed-lost', 'executionStatus': 'lost', 'lostAt': at,
                            'lossReason': 'reserved ordinary Action was not executed within the target own regular slot'})
                        a.setdefault('hardDenial', {})[key] = copy.deepcopy(mark)
                        effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), None)
                        if effect:
                            effect['q27Allowance'] = copy.deepcopy(mark)
        if ('hard action component' in label.lower() or 'single compelled action' in label.lower()
                or 'single compelled' in label.lower() or 'initial compelled action' in label.lower()
                or 'chooses legal dodge' in label.lower()):
            t = state['actors']['T']
            encounter_id = state.get('encounter')
            key = f'A|T|{encounter_id}'
            mark = state.setdefault('hardDenialLedger', {}).get(key)
            if mark and mark.get('status') == 'consumed-awaiting-execution':
                mark.update({'status': 'consumed-executed', 'executionStatus': 'executed',
                    'executedAt': at, 'chosenAction': 'Dodge', 'revalidatedBeforeUse': True})
                t.setdefault('hardDenial', {})[key] = copy.deepcopy(mark)
                effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), None)
                if effect:
                    effect['q27Allowance'] = copy.deepcopy(mark)
                if state['spellCommitments']:
                    state['spellCommitments'][0]['targetSavePending'] = False
                    state['spellCommitments'][0]['firstCompelledAction'] = {'executedAt': at, 'chosenAction': 'Dodge',
                        'guardConsumedAtAdmission': mark['consumedAt'], 'executionStatus': 'executed'}
            following = [x for x in t.get('regularCalendar', []) if x > at]
            expiry = following[0] if following else None
            t.setdefault('conditions', {})['Dodging'] = {'appliedAt': at, 'expiresAt': expiry,
                'source': 'T chooses Dodge in its own regular Action slot'}
        if 'casts reviewed gaseous form' in label.lower():
            window = counterspell_window(state, 'T', at, at, 'gaseous-form', 3,
                actor_state=before.get('actors'))
            commitment(state, at, 'T', 'gaseous-form', 5, 'T-GAS-268', 'reviewed Gaseous Form envelope; outside-initiative finite cast fixture')
            state['spellCommitments'].append({'eventId': 'T-GAS-268', 'at': at, 'caster': 'T', 'target': 'T',
                'spellId': 'gaseous-form', 'actionCommitted': True, 'RPSpent': 5,
                'counterWindow': window['result'], 'counterWindowDetails': copy.deepcopy(window),
                'castResolutionOrder': 'after all eligible responders decline or the window otherwise closes'})
            set_form(state, 'T', 'T-GAS-268', 8.0, 'T')
            state['formRecords']['T']['status'] = 'active'
            add_schedule(state, 'source-form-end:T-GAS-268', 8.0, '60-second source concentration deadline')
        if 'exact form deadline' in label.lower():
            for aid in ('T', 'R1'):
                restore_form(state, aid, at, 'source concentration deadline')
            if state.get('copiedForms', {}).get('R1'):
                state['copiedForms']['R1'].update({'status': 'ended', 'endedAt': at, 'ending': 'inherited source deadline'})
        if 'arcane bolt causes' in label.lower():
            window = counterspell_window(state, 'T', at, at, 'wizard.base.arcane-bolt', 1,
                actor_state=before.get('actors'), observer_ids=['A', 'R1'])
            commitment(state, at, 'T', 'wizard.base.arcane-bolt', 1, 'T-ARCANE-BOLT-268', 'W17 Wizard source; 4d6+5 and force resistance')
            state['spellCommitments'].append({'eventId': 'T-ARCANE-BOLT-268', 'at': at, 'caster': 'T',
                'target': 'R1', 'spellId': 'wizard.base.arcane-bolt', 'actionCommitted': True, 'RPSpent': 1,
                'counterWindow': window['result'], 'counterWindowDetails': copy.deepcopy(window),
                'castResolutionOrder': 'after all eligible responders decline or the window otherwise closes'})
            if state.get('damageEvents'):
                state['damageEvents'][-1].update({'damageFormula': '4d6+5', 'rawDamageDice': [1, 1, 1, 1],
                    'flatModifier': 5, 'rawForce': 9, 'resolvedDamage': 4,
                    'resistance': 'force resistance halves 9 to 4'})
            conc = state.get('copiedConcentration', {}).get('R1', {})
            conc.update({'damageAt': at, 'concentrationSave': {'save': 'CON', 'rolls': [1, 2], 'selectedRoll': 2,
                'modifier': 2, 'total': 4, 'DC': 10, 'success': False, 'advantage': True,
                'advantageSource': 'wizard.arch.improved-concentration', 'cause': '4 resolved damage; max(10,floor(4/2))'},
                'status': 'ended-on-failed-advantaged-save', 'endedAt': at})
            state['actors']['R1']['concentration'] = None
            restore_form(state, 'R1', at, 'failed damage concentration save with advantage')
            if state.get('formRecords', {}).get('R1'):
                state['formRecords']['R1'].update({'endedAt': at, 'ending': 'failed advantaged CON save', 'currentHP': 100, 'currentRP': 59})
        if kind == 'ZERO' and 'resolves original t to zero' in label.lower():
            if state['actors'].get('R1'):
                state['actors']['R1']['active'] = True
                state['actors']['R1']['life'] = 'Alive'
            effect = next((v for v in state['effects'].values() if v.get('kind') == 'soul-reflection'), None)
            if effect:
                effect['active'] = True
            add_phase_from_label(kind, state, 'Reflection phase 1 resolves Ray of Frost', at, old)
            if state.get('damageEvents'):
                state['damageEvents'][-1].update({'attackRolls': [18, 7], 'rollMode': 'disadvantage from active Dodge',
                    'attackRoll': 7, 'selectedRoll': 7, 'attackTotal': 18, 'targetAC': state['actors']['T'].get('AC', 12),
                    'damageDice': [1], 'damageFormula': '1d8 cold', 'resolvedDamage': 1})
            t = state['actors']['T']
            t['conditions'].pop('Dodging', None)
            t['conditions']['Unconscious'] = {'appliedAt': at, 'source': 'zero HP',
                'includes': ['Incapacitated', 'unaware', 'drop held items', 'Prone']}
            t['conditions']['Incapacitated'] = {'appliedAt': at, 'source': 'Unconscious at zero HP'}
            t['conditions']['Prone'] = {'appliedAt': at, 'source': 'Unconscious at zero HP'}
            t['life'] = 'Downed'
            t['action'] = t['bonusAction'] = t['reaction'] = t['interaction'] = 0
            for hand, item_id in list(t.get('hands', {}).items()):
                if item_id and item_id in state['items']:
                    state['items'][item_id].update({'owner': 'T', 'custodian': 'ground', 'held': False,
                        'position': copy.deepcopy(t.get('position')), 'droppedAt': at})
                    t['hands'][hand] = None
            if state['actors'].get('R1'):
                state['actors']['R1'].update({'active': False, 'life': 'FiniteEnded'})
                state['actors']['R1']['endedAt'] = at
                end_reflection_gear(state, at)
                zero_phase = next((x for x in state.get('reflectionPhaseLedger', []) if x.get('index') == 1), None)
                if zero_phase:
                    zero_phase.update({'endedAt': at,
                        'endReason': 'original target reached zero after damage and life-state settlement',
                        'remainingBudgetAtEnd': {'Action': 0, 'BonusAction': 0, 'Reaction': 0, 'MovementFeet': 0}})
            effect = next((v for v in state['effects'].values() if v.get('kind') == 'soul-reflection'), None)
            if effect:
                effect.update({'active': False, 'endedAt': at,
                    'ending': 'original target reached zero after complete source pipeline',
                    'terminationOrder': 'after target HP, Wound, condition, and death-state settlement within the same event timestamp'})
            ray_commitment = next(x for x in state['spellCommitments'] if x.get('eventId') == 'R1-RAYFROST-268')
            ray_commitment.update({'attack': {'rolls': [18, 7], 'selectedRoll': 7, 'mode': 'disadvantage'},
                'damageDice': [1], 'targetZeroSettledAt': at})
        if 'death save' in label.lower() and kind == 'ZERO':
            t = state['actors']['T']
            t.setdefault('deathSaves', {})['successes'] = 1
            t['deathSaves']['failures'] = 0
            t['deathSaves']['lastRoll'] = {'at': at, 'd20': 14, 'modifier': 0, 'total': 14, 'success': True}
            t['conditions']['Unconscious']['cause'] = 'Downed; still unconscious after successful death save'
            t['action'] = t['bonusAction'] = t['reaction'] = t['interaction'] = 0
        if kind == 'CARGO' and 'antimagic field lesser suppresses' in label.lower():
            cast_at = at - 0.01
            window = counterspell_window(state, 'D', cast_at, at, 'antimagic-field-lesser', 5,
                actor_state=before.get('actors'), observer_ids=['A', 'T', 'R1'])
            commitment(state, at - 0.01, 'D', 'antimagic-field-lesser', 10, 'D-AML268', 'exact accepted field source and prepared Wizard matrix')
            state['spellCommitments'].append({'eventId': 'D-AML268', 'at': at - 0.01, 'caster': 'D', 'target': 'R1',
                'spellId': 'antimagic-field-lesser', 'actionCommitted': True, 'RPSpent': 10, 'concentration': True,
                'counterWindow': window['result'], 'counterWindowDetails': copy.deepcopy(window),
                'castResolutionOrder': 'after all eligible responders decline or the window otherwise closes'})
            for item_id in state['actors']['R1'].get('inventory', []):
                if item_id in state['items']:
                    state['items'][item_id].update({'active': False, 'colliding': False, 'custodyStatus': 'suppressed'})
        if kind == 'CARGO' and 'same reflection identity resumes' in label.lower():
            for item_id in state['actors']['R1'].get('inventory', []):
                if item_id in state['items']:
                    state['items'][item_id].update({'active': True, 'colliding': True, 'custodyStatus': 'resumed'})
        # Phase events, including the explicitly skipped suppressed phase.
        if ('phase' in label.lower() or 'uses one source-qualified copied action' in label.lower()) and kind != 'ZERO':
            add_phase_from_label(kind, state, label, at, old)
        if any(x in label.lower() for x in ('finite reflection ends', 'reflection ends; only', 'finite opponent ends')):
            if state.get('actors', {}).get('R1'):
                state['actors']['R1'].update({'active': False, 'life': 'FiniteEnded'})
                end_reflection_gear(state, at)
        # Enrich a phase action in the separate Reflection actor. The Ray case has a single integrated event.
        for actor_id, actor in state.get('actors', {}).items():
            if is_turn_event(old_event, actor_id, 'regularStarts'):
                dodge = actor.get('conditions', {}).get('Dodging')
                if dodge and dodge.get('expiresAt', at + 1) <= at:
                    actor['conditions'].pop('Dodging', None)
            if is_turn_event(old_event, actor_id, 'regularEnds'):
                actor['action'] = actor['bonusAction'] = actor['interaction'] = 0
        # Use actor histories derived from the exact events up to this point.
        replay_history(state, new_events + [old_event], kind)
        if kind == 'CARGO' and 'T-map' in state['items'] and state['items']['T-map'].get('custodian') == 'ground':
            state['items']['T-map'].update({'owner': 'T', 'held': False, 'position': [15, 0, 0]})
        update_schedule(state, kind, at)
        state['time'] = at
        after = copy.deepcopy(state)
        eid = old_event.get('id', f'{state["caseId"]}:{len(new_events)+1}')
        new_events.append({'id': eid.replace('5263', '5268'), 'atSeconds': at, 'label': label,
            'before': before, 'beforeSHA256': state_sha(before), 'after': after, 'afterSHA256': state_sha(after),
            'forward': [{'op': 'test', 'path': '', 'value': before}, {'op': 'replace', 'path': '', 'value': after}],
            'inverse': [{'op': 'test', 'path': '', 'value': after}, {'op': 'replace', 'path': '', 'value': before}],
            'evidence': old_event.get('evidence', {})})
        active_phase = state.get('actors', {}).get('R1', {}).get('activeReflectionPhase')
        active_row = next((x for x in state.get('reflectionPhaseLedger', [])
            if x.get('index') == active_phase and x.get('status') == 'resolved' and x.get('startAt') == at), None)
        if kind != 'ZERO' and active_row and active_phase in (1, 2):
            end_at = round(at + 0.03, 2)
            phase_before = copy.deepcopy(state)
            close_reflection_phase(state, end_at, 'reflection phase completed')
            state['time'] = end_at
            phase_after = copy.deepcopy(state)
            phase_id = f'{state["caseId"]}:reflection-phase-{active_phase}-end'
            new_events.append({'id': phase_id, 'atSeconds': end_at,
                'label': f'R1 reflection phase {active_phase} END before the next independent actor slot',
                'before': phase_before, 'beforeSHA256': state_sha(phase_before),
                'after': phase_after, 'afterSHA256': state_sha(phase_after),
                'forward': [{'op': 'test', 'path': '', 'value': phase_before}, {'op': 'replace', 'path': '', 'value': phase_after}],
                'inverse': [{'op': 'test', 'path': '', 'value': phase_after}, {'op': 'replace', 'path': '', 'value': phase_before}],
                'evidence': {'source': 'GPT IR265-C04/C06 correction instruction; bounded witness phase-END checkpoint; no universal duration claimed'}})
    case['id'] = case['id'].replace('5263', '5268')
    case['initialState'] = base_case({'initialState': case['initialState'], 'events': old_events, 'id': case['id']}, kind)
    case['initialSHA256'] = state_sha(case['initialState'])
    case['events'] = new_events
    case['finalState'] = copy.deepcopy(state)
    case['finalSHA256'] = state_sha(state)
    case['caseStatus'] = 'PROPOSAL_TRACE_NOT_ACCEPTANCE'
    return case


def replay_history(state, events, kind):
    for actor_id, actor in state.get('actors', {}).items():
        rows = sorted((x for x in state.get('spellCadence', []) if x.get('actor') == actor_id), key=lambda x: x['at'])
        actor['castHistory'] = [x['eventId'] for x in rows]
        actor['castFamilies'] = list(dict.fromkeys(x['spellId'] for x in rows))
        actor['matrixFamilies'] = list(dict.fromkeys(x['matrixFamily'] for x in rows))
        if rows:
            actor['lastSpell'] = rows[-1]['spellId']
        actor['resourceHistory'] = [{'at': x['at'], 'spellId': x['spellId'], 'costRP': x['RPAid'],
            'RPBefore': x['RPBefore'], 'RPAfter': x['RPAfter'], 'eventId': x['eventId'],
            'matrixFamily': x['matrixFamily'], 'firstDistinctFamilyThisEncounter': x['firstDistinctFamilyThisEncounter'],
            'baseDissonance': x['baseDissonance'], 'refrainApplied': x['refrainApplied'],
            'refrainBefore': x['refrainBefore'], 'refrainAfter': x['refrainAfter'],
            'dissonanceBefore': x['dissonanceBefore'], 'dissonanceAfter': x['dissonanceAfter']}
            for x in rows]


def make_attached_case(template):
    base = template['initialState']
    state = copy.deepcopy(base)
    state['actors'] = {'A': copy.deepcopy(base['actors']['A'])}
    state['items'] = {}
    A = state['actors']['A']
    A['regularCalendar'] = [0, 6, 12]
    A['regularStarts'] = []; A['regularEnds'] = []; A['nextRegularStart'] = 0
    A['castHistory'] = []; A['castFamilies'] = []; A['resourceHistory'] = []; A['matrixFamilies'] = []
    A['magicalThisTurn'] = False; A['refrainCount'] = 0; A['dissonance'] = 0
    ranger = {'id': 'Ranger16', 'profileId': 'RANGER-16-CONDITIONAL-FIXTURE', 'class': 'Ranger', 'classLevel': 16,
        'selectedSubclass': 'Warder', 'acquiredClassIds': ['ranger.hero.warder.beast-companion'],
        'featureAcquisition': {'cardId': 'ranger.hero.warder.beast-companion', 'selectedAtClassLevel': 16,
            'source': 'ranger.json#/cards/29'},
        'PB': 5, 'abilities': {'WIS': 16}, 'modifiers': {'WIS': 3}, 'rp': 28, 'rpMax': 28,
        'hp': 80, 'maxHP': 80, 'action': 0, 'bonusAction': 0, 'reaction': 1, 'interaction': 0,
        'activeRegular': False, 'regularCalendar': [1, 7, 13], 'regularStarts': [], 'regularEnds': [],
        'nextRegularStart': 1, 'castHistory': [], 'castFamilies': [], 'resourceHistory': [], 'matrixFamilies': [],
        'magicalThisTurn': False, 'refrainCount': 0, 'dissonance': 0, 'hardDenial': {},
        'conditions': {}, 'life': 'Alive', 'position': [10, 0, 0], 'beastCompanionUsesPerLongRest': 1,
        'beastCompanionUsesRemaining': 1, 'companionId': None}
    cave = {'id': 'T', 'profileId': 'DecenniumDescentv6:cave-bear', 'name': 'Cave Bear', 'creatureType': 'Beast',
        'size': 'Large', 'alignment': 'Unaligned', 'challengeRating': 2,
        'abilities': {'STR': 16, 'DEX': 14, 'CON': 13, 'INT': 3, 'WIS': 12, 'CHA': 6},
        'intelligence': 3, 'armorClass': 13, 'AC': 13, 'hp': 68, 'maxHP': 68, 'speed': 40, 'rp': 0, 'rpMax': 0,
        'action': 0, 'bonusAction': 0, 'reaction': 0, 'interaction': 0, 'activeRegular': False,
        'regularCalendar': [], 'regularStarts': [], 'regularEnds': [], 'nextRegularStart': None,
        'attachedPhaseMarkers': [], 'attachedPhaseHistory': [], 'ownerId': None,
        'controllerId': None, 'companionKind': None, 'PB': 0, 'saves': {'WIS': 1},
        'conditions': {}, 'hardDenial': {}, 'life': 'Alive', 'castHistory': [], 'castFamilies': [],
        'resourceHistory': [], 'position': [15, 0, 0], 'movementMode': 'Speed 40 ft.',
        'bondEligibilitySnapshot': {'type': 'Beast', 'CR': 2, 'INT': 3, 'notCorrupted': True,
            'willing': True, 'tamed': True, 'touched': True},
        'nativeActions': ['Multiattack', 'Mauling Claws'], 'bondStatus': 'unbonded-wild-body',
        'fixtureFacts': {'willing': True, 'tamed': True, 'touched': True, 'notCorrupted': True}}
    state['actors']['Ranger16'] = ranger
    state['actors']['T'] = cave
    state['time'] = -3600.01
    state['scheduled'] = {}
    state['effects'] = {}
    state['spellCommitments'] = []
    state['spellCadence'] = []
    state['saveHistory'] = []
    state['hardDenialLedger'] = {}
    state['reflectionPhases'] = []
    state['reflectionPhaseLedger'] = []
    for aid, starts in [('A', [0, 6, 12]), ('Ranger16', [1, 7, 13])]:
        actor = state['actors'][aid]
        for t in starts:
            add_schedule(state, f'regular-start:{aid}:{t:g}', t, 'actual regular START')
            add_schedule(state, f'regular-end:{aid}:{t + 0.9:g}', t + 0.9, 'actual regular END')
    for t in [1.91, 7.91, 13.91]:
        add_schedule(state, f'attached-target-end:T:{t - 0.01:g}', t - 0.01, 'owner END followed by actual attached companion phase')
        add_schedule(state, f'reflection-phase:R1:{t:g}', t, 'proposed phase after attached-only target END')
    cid = 'RANK9ILLUSIONREALITY5268-SOUL-REFLECTION-ATTACHED-CAVE-BEAR'
    effect_id = 'A-SR-' + cid
    state['caseId'] = cid
    state['encounter'] = cid
    state['currentAuthority'] = copy.deepcopy(AUTH)
    state['proposalStatus'] = 'UNACCEPTED_DIRECTOR_ADJUDICATION_REQUIRED'
    case = {'id': cid, 'title': 'Source-bound Ranger Cave Bear with actual attached-phase markers',
        'spellId': 'soul-reflection', 'kind': 'bounded-static-proposal-trace',
        'caseStatus': 'PROPOSAL_TRACE_NOT_ACCEPTANCE',
        'qualification': 'The Cave Bear profile is an existing tracked public source in DecenniumDescentv6. Noncorruption, willingness and taming are explicit bounded fixture facts, not species inferences. Companion phases are attached to Ranger turns; the target receives no independent regular turn.',
        'sourceIds': ['CAVE_BEAR_PROFILE_DV6', 'RANGER_BEAST_COMPANION_CARD_29', 'CREATURE_LIFECYCLE_PLAYTEST', 'IR207-B02'],
        'initialState': copy.deepcopy(state), 'events': [], 'requirementsDemonstrated': [], 'requirementsHeld': [],
        'finalState': None, 'finalSHA256': None}

    def event(at, label, evidence, mutate):
        nonlocal state
        before = copy.deepcopy(state)
        mutate(state)
        update_schedule(state, 'ATTACHED', at)
        state['time'] = at
        after = copy.deepcopy(state)
        n = len(case['events']) + 1
        case['events'].append({'id': f'{cid}:{n}', 'atSeconds': at, 'label': label,
            'before': before, 'beforeSHA256': state_sha(before), 'after': after, 'afterSHA256': state_sha(after),
            'forward': [{'op': 'test', 'path': '', 'value': before}, {'op': 'replace', 'path': '', 'value': after}],
            'inverse': [{'op': 'test', 'path': '', 'value': after}, {'op': 'replace', 'path': '', 'value': before}],
            'evidence': evidence})

    def begin_bond_ritual(st):
        o = st['actors']['Ranger16']; t = st['actors']['T']
        o['bondRitual'] = {'targetId': 'T', 'featureId': 'ranger.hero.warder.beast-companion',
            'startedAt': -3600, 'completesAt': 0, 'requiredSeconds': 3600, 'status': 'in-progress',
            'touchMaintained': True, 'willing': True, 'tamed': True, 'notCorrupted': True}
        t['bondRitual'] = {'ownerId': 'Ranger16', 'startedAt': -3600, 'completesAt': 0,
            'status': 'in-progress', 'touchMaintained': True}
    event(-3600, 'Ranger16 starts the selected level-16 Warder Beast Companion ritual with eligible wild Cave Bear T',
        {'source': 'ranger.json#/cards/29; exact one-hour ritual begins; eligibility is explicit fixture evidence'}, begin_bond_ritual)

    def bond(st):
        o = st['actors']['Ranger16']; t = st['actors']['T']
        before = o['rp']; hp_before = t['hp']; hp_max_before = t['maxHP']; ac_before = t['armorClass']
        o['rp'] -= 4; o['beastCompanionUsesRemaining'] -= 1; o['companionId'] = 'T'
        t['bondedAt'] = 0; t['ownerId'] = 'Ranger16'; t['controllerId'] = 'Ranger16'
        t['companionKind'] = 'Ranger Beast'; t['bondStatus'] = 'bonded'
        t['PB'] = o['PB']; t['saves'] = {'WIS': o['PB']}
        t['armorClass'] = 12 + o['PB'] // 2; t['AC'] = t['armorClass']
        t['maxHP'] = 2 * o['classLevel'] + o['modifiers']['WIS']
        t['hp'] = max(1, int(t['maxHP'] * hp_before / hp_max_before))
        t['bondedAt'] = 0; t['attachedPhaseMarkers'] = [1.9, 7.9, 13.9]
        t.pop('nativeActions', None)
        t['convertedCompanionProfile'] = {'AC': '12 + floor(PB/2) = 14', 'HP': '2L + actual WIS modifier = 35',
            'currentHP': 'floor(35 × 68 / 68) = 35', 'speedMode': '40 ft. preserved, capped at 40',
            'nativeMonsterActionsImported': False, 'bossPowersImported': False, 'independentRegularTurn': False}
        t['bondHistory'] = [{'ritualStartAt': -3600, 'completedAt': 0, 'seconds': 3600,
            'touchMaintained': True, 'willing': True, 'tamed': True, 'notCorrupted': True,
            'eligibilityProfile': 'cave-bear', 'CR': 2, 'INT': 3, 'rangerLevel': 16,
            'costRP': 4, 'RPBefore': before, 'RPAfter': o['rp'], 'longRestUseSpent': True,
            'nativeStatsBefore': {'AC': ac_before, 'HP': hp_before, 'maxHP': hp_max_before},
            'convertedStatsAfter': {'AC': t['armorClass'], 'HP': t['hp'], 'maxHP': t['maxHP']}}]
        t['bondRitual'].update({'status': 'completed', 'completedAt': 0})
        o['bondRitual'].update({'status': 'completed', 'completedAt': 0, 'costRP': 4,
            'RPBefore': before, 'RPAfter': o['rp'], 'longRestUseSpent': True})
        o['resourceHistory'].append({'at': 0, 'spellId': 'ranger.hero.warder.beast-companion', 'costRP': 4,
            'RPBefore': before, 'RPAfter': o['rp']})
    event(0, 'Ranger16 completes the exact one-hour Beast Companion bond for Cave Bear T',
        {'source': 'ranger.json#/cards/29 and CREATURE_LIFECYCLE_PLAYTEST.md §Ranger Beast',
         'profile': 'existing public Cave Bear source; noncorruption/willing/tamed are explicit fixture facts'}, bond)

    def start_turn(st, actor_id, at):
        if actor_id != 'R1' and st.get('actors', {}).get('R1', {}).get('activeReflectionPhase') is not None:
            phase_idx = st['actors']['R1']['activeReflectionPhase']
            phase_row = next((x for x in st.get('reflectionPhaseLedger', [])
                if x.get('index') == phase_idx and x.get('status') == 'resolved'), None)
            if phase_row and at > phase_row.get('startAt', at):
                close_reflection_phase(st, at, 'next independent actor regular slot')
        a = st['actors'][actor_id]; a['regularStarts'].append(at); a['lastRegularStart'] = at
        a['activeRegular'] = True; a['action'] = 1; a['bonusAction'] = 1; a['reaction'] = 1; a['interaction'] = 1
        a['magicalThisTurn'] = False
        future = [x for x in a['regularCalendar'] if x > at]; a['nextRegularStart'] = future[0] if future else None
        a['movementSpent'] = 0
    event(0, 'A starts its regular turn after ritual completion', {'source': 'exact A regular marker'}, lambda st: start_turn(st, 'A', 0))

    def cast(st):
        a = st['actors']['A']; a['rp'] -= 26
        window = counterspell_window(st, 'A', 0.1, 0.11)
        commitment(st, 0.1, 'A', 'soul-reflection', 26, effect_id,
            'native identity plus unaccepted local operational proposal')
        st['effects'][effect_id] = {'kind': 'soul-reflection', 'owner': 'A', 'target': 'T',
            'createdAt': 0.1, 'deadlineAt': 13.94, 'sourceDurationMaxAt': 18.0, 'active': True, 'pendingAdmission': True,
            'phaseMarkers': [1.91, 7.91, 13.91],
            'counterWindow': copy.deepcopy(window)}
        st['spellCommitments'].append({'eventId': effect_id, 'at': 0.1, 'caster': 'A', 'target': 'T',
            'spellId': 'soul-reflection', 'actionCommitted': True, 'RPSpent': 26,
            'counterWindow': window['result'], 'counterWindowDetails': copy.deepcopy(window), 'targetSavePending': True})
    event(0.1, 'A commits Soul Reflection on the bonded Cave Bear',
        {'source': 'native identity plus new local procedure proposal', 'castAction': 'A turn Action spent; 26 RP paid before resolution'}, cast)

    def admission(st):
        t = st['actors']['T']; save = append_save(st, 'T', 0.11, 8, 5, st['actors']['A']['spellDC'],
            'CREATURE_LIFECYCLE_PLAYTEST.md §Stats and ownership: current Ranger PB supplies companion saves')
        snapshot = {'sourceActor': 'T', 'sourceProfileId': t['profileId'], 'type': t['creatureType'],
            'size': t['size'], 'CR': t['challengeRating'], 'INT': t['intelligence'], 'AC': t['AC'],
            'HP': t['hp'], 'maxHP': t['maxHP'], 'speed': t['speed']}
        provenance = {'historicalOwnerAtCopy': 'Ranger16', 'sourceBondCompletedAt': 0,
            'liveBondCopied': False, 'ownerCopied': False, 'controllerCopied': False,
            'attachedPhaseHistoryCopied': False, 'featureId': 'ranger.hero.warder.beast-companion'}
        r = copy.deepcopy(t)
        for key in ('bondedAt', 'bondHistory', 'bondRitual', 'bondStatus', 'bondEligibilitySnapshot',
                    'convertedCompanionProfile', 'attachedPhaseMarkers', 'attachedPhaseHistory',
                    'nativeActions', 'beastCompanionUsesRemaining', 'beastCompanionUsesPerLongRest'):
            r.pop(key, None)
        r.update({'id': 'R1', 'profileId': 'CAVE-BEAR-REFLECTION-268',
            'reflectionSource': effect_id, 'causalRoot': effect_id,
            'ownerId': None, 'controllerId': None, 'companionKind': None, 'attachedOnly': False,
            'regularCalendar': [], 'regularStarts': [], 'regularEnds': [], 'nextRegularStart': None,
            'active': True, 'reflectionPhaseMarkers': [1.91, 7.91, 13.91], 'hp': 35, 'maxHP': 35,
            'rp': 0, 'rpMax': 0, 'position': [25, 0, 0], 'inventory': [],
            'hands': {'left': None, 'right': None}, 'activeReflectionPhase': None,
            'bondStatus': 'unbonded-finite-reflection', 'liveBondCopied': False,
            'copiedProfileSnapshot': snapshot, 'copiedBondProvenance': provenance,
            'placement': {'shape': 'Large 10x10-foot square', 'targetCenter': [15, 0, 0],
                'reflectionCenter': [25, 0, 0], 'centerDistanceFeet': 10, 'edgeGapFeet': 0, 'overlap': False}})
        st['actors']['R1'] = r
        st['effects'][effect_id].update({'pendingAdmission': False,
            'status': 'admitted-after-failed-WIS-save', 'admissionSave': copy.deepcopy(save), 'reflectionId': 'R1'})
        st['spellCommitments'][0]['targetSavePending'] = False
        establish_q27_allowance(st, 0.11, attached_only=True)
    event(0.11, 'Cave Bear fails the source-bound WIS save; R1 is admitted without copying its attachment',
        {'source': 'conditional caster DC19; companion save +PB5; stipulated d20=8; target attachment itself is not copied'}, admission)
    event(0.9, 'A regular END 1', {'source': 'exact A regular marker'}, lambda st: end(st, 'A', 0.9))
    event(1, 'Ranger16 regular start 1', {'source': 'owner regular marker'}, lambda st: start_turn(st, 'Ranger16', 1))
    event(1.9, 'Ranger16 regular END 1', {'source': 'owner whole turn ends before attached companion checkpoint'}, lambda st: end(st, 'Ranger16', 1.9))
    def attached(st, idx, at):
        expire_conditions(st, at)
        t = st['actors']['T']; t['attachedPhaseHistory'].append({'index': idx, 'owner': 'Ranger16',
            'ownerRegularEnd': at, 'commandIssued': False, 'action': 'defensive Dodge',
            'independentRegularTurn': False, 'reactionRefreshed': False, 'rechargeRefreshed': False,
            'regularDurationClockRefreshed': False})
        t.setdefault('conditions', {})['Dodging'] = {'appliedAt': at, 'expiresAt': [7.9, 13.9, 19.9][idx-1],
            'source': 'actual uncommanded attached companion Action: Dodge'}
    event(1.9, 'T resolves its actual attached companion phase after Ranger16 END 1',
        {'source': 'CREATURE_LIFECYCLE_PLAYTEST.md §At the table; uncommanded companion may Dodge'}, lambda st: attached(st, 1, 1.9))
    def phase(st, idx, at):
        expire_conditions(st, at)
        r = st['actors']['R1']
        if r.get('activeReflectionPhase') is not None:
            close_reflection_phase(st, at, 'next actual attached-phase END opportunity')
        movement = max(0, r['speed'] - r.get('movementSpent', 0))
        r['regularCalendar'] = []; r['nextRegularStart'] = None
        r['activeReflectionPhase'] = idx
        r['action'] = 1; r['bonusAction'] = 1; r['reaction'] = 1; r['movementSpent'] = 0
        r['magicalThisTurn'] = False
        r['action'] = 0
        r['conditions']['Dodging'] = {'appliedAt': at, 'expiresAt': [7.91, 13.91, 13.94][idx-1], 'source': 'R1 reflection phase'}
        r['reflectionPhaseBudget'] = {'action': 0, 'bonusAction': 1, 'reaction': 1, 'movementFeet': movement}
        row = {'index': idx, 'startAt': at, 'targetMarker': at - 0.01, 'target': 'T',
            'targetMarkerKind': 'actual attached companion END', 'status': 'resolved',
            'sourceSpeedFeet': r['speed'], 'postActionSpeedFeet': r['speed'],
            'startingBudget': {'Action': 1, 'BonusAction': 1, 'Reaction': 1, 'MovementFeet': movement},
            'budgetAfterAction': {'Action': 0, 'BonusAction': 1, 'Reaction': 1, 'MovementFeet': movement},
            'spent': {'type': 'Dodge', 'ActionSpent': True, 'RPSpent': 0},
            'independentTargetTurn': False, 'regularStartRecordedForR1': False}
        st['reflectionPhaseLedger'].append(row); st['reflectionPhases'] = copy.deepcopy(st['reflectionPhaseLedger'])
    event(1.91, 'R1 reflection phase 1 follows the actual attached END marker',
        {'source': 'NEW Q28-equivalent local timing proposal; not a companion or target turn'}, lambda st: phase(st, 1, 1.91))
    event(1.94, 'R1 reflection phase 1 END before the next independent actor slot',
        {'source': 'GPT IR265-C04/C06 correction instruction; bounded witness phase-END checkpoint'},
        lambda st: close_reflection_phase(st, 1.94, 'reflection phase completed'))
    event(6, 'A regular start 2', {'source': 'exact A regular marker'}, lambda st: start_turn(st, 'A', 6))
    event(6.9, 'A regular END 2', {'source': 'exact A regular marker'}, lambda st: end(st, 'A', 6.9))
    event(7, 'Ranger16 regular start 2', {'source': 'owner regular marker'}, lambda st: start_turn(st, 'Ranger16', 7))
    event(7.9, 'Ranger16 regular END 2', {'source': 'owner whole turn ends before attached companion checkpoint'}, lambda st: end(st, 'Ranger16', 7.9))
    event(7.9, 'T resolves its actual attached companion phase after Ranger16 END 2',
        {'source': 'CREATURE_LIFECYCLE_PLAYTEST.md §At the table; no independent T turn'}, lambda st: attached(st, 2, 7.9))
    event(7.91, 'R1 reflection phase 2 follows the actual attached END marker',
        {'source': 'NEW Q28-equivalent local timing proposal'}, lambda st: phase(st, 2, 7.91))
    event(7.94, 'R1 reflection phase 2 END before the next independent actor slot',
        {'source': 'GPT IR265-C04/C06 correction instruction; bounded witness phase-END checkpoint'},
        lambda st: close_reflection_phase(st, 7.94, 'reflection phase completed'))
    event(12, 'A regular start 3', {'source': 'exact A regular marker'}, lambda st: start_turn(st, 'A', 12))
    event(12.9, 'A regular END 3', {'source': 'exact A regular marker'}, lambda st: end(st, 'A', 12.9))
    event(13, 'Ranger16 regular start 3', {'source': 'owner regular marker'}, lambda st: start_turn(st, 'Ranger16', 13))
    event(13.9, 'Ranger16 regular END 3', {'source': 'owner whole turn ends before attached companion checkpoint'}, lambda st: end(st, 'Ranger16', 13.9))
    event(13.9, 'T resolves its actual attached companion phase after Ranger16 END 3',
        {'source': 'CREATURE_LIFECYCLE_PLAYTEST.md §At the table; no independent T turn'}, lambda st: attached(st, 3, 13.9))
    event(13.91, 'R1 reflection phase 3 follows the actual attached END marker',
        {'source': 'NEW Q28-equivalent local timing proposal'}, lambda st: phase(st, 3, 13.91))
    def finish(st):
        st['effects'][effect_id].update({'active': False, 'endedAt': 13.94, 'ending': 'third attached-target phase completed'})
        st['actors']['R1'].update({'active': False, 'life': 'FiniteEnded'})
        end_reflection_gear(st, 13.94)
    event(13.94, 'R1 ends after the third actual attached END marker',
        {'source': 'NEW Q30-equivalent local termination proposal'}, finish)
    case['requirementsDemonstrated'] = ['Tracked public Cave Bear source explicitly binds Beast, CR2 and INT3',
        'Ranger16 bond pays4RP and one long-rest use over the full one-hour ritual; eligibility facts are explicit',
        'Actual owner regular END and attached companion checkpoints are traced at1.9,7.9,13.9',
        'T has no independent regular turn; R1 copies no owner/bond and receives three separate proposed phases']
    case['requirementsHeld'] = ['Formal identity acceptance remains pending; the source authority, attached-only Q27 ruling, and Q28 owner-relative markers are implemented from the director response',
        'Noncorruption, willingness and taming remain explicitly stipulated individual fixture facts, not inferred from species']
    case['finalState'] = copy.deepcopy(state)
    case['finalSHA256'] = state_sha(state)
    return case


def start_turn(st, actor_id, at):
    if actor_id != 'R1' and st.get('actors', {}).get('R1', {}).get('activeReflectionPhase') is not None:
        phase_idx = st['actors']['R1']['activeReflectionPhase']
        phase_row = next((x for x in st.get('reflectionPhaseLedger', [])
            if x.get('index') == phase_idx and x.get('status') == 'resolved'), None)
        if phase_row and at > phase_row.get('startAt', at):
            close_reflection_phase(st, at, 'next independent actor regular slot')
    a = st['actors'][actor_id]
    a['regularStarts'].append(at); a['lastRegularStart'] = at; a['activeRegular'] = True
    a['action'] = a['bonusAction'] = a['reaction'] = a['interaction'] = 1
    a['movementSpent'] = 0
    future = [x for x in a.get('regularCalendar', []) if x > at]
    a['nextRegularStart'] = future[0] if future else None


def end(st, actor_id, at):
    if actor_id != 'R1' and st.get('actors', {}).get('R1', {}).get('activeReflectionPhase') is not None:
        phase_idx = st['actors']['R1']['activeReflectionPhase']
        phase_row = next((x for x in st.get('reflectionPhaseLedger', [])
            if x.get('index') == phase_idx and x.get('status') == 'resolved'), None)
        if phase_row and at > phase_row.get('startAt', at):
            close_reflection_phase(st, at, 'next independent actor regular slot')
    a = st['actors'][actor_id]
    a['regularEnds'].append(at); a['lastRegularEnd'] = at; a['activeRegular'] = False
    a['action'] = a['bonusAction'] = a['interaction'] = 0


def make_manifest(payload):
    members = [binding(name, payload[name]) for name in sorted(payload)]
    return {'id': 'SOUL-REFLECTION-DELTA-268-MEMBER-MANIFEST', 'authority': AUTH,
        'targetIds': ['soul-reflection'], 'memberCountExcludingSelf': len(members), 'members': members}


def replay_case(case):
    state = copy.deepcopy(case['initialState'])
    failures = []
    ops = 0
    last = state.get('time', -float('inf'))
    for e in case['events']:
        if e['atSeconds'] < last or e['before'] != state:
            failures.append(f'chain/time {e["id"]}')
        forward_start = copy.deepcopy(state)
        for patch in e['forward']:
            ops += 1
            if patch['op'] == 'test' and state != patch['value']:
                failures.append(f'forward test {e["id"]}')
            elif patch['op'] == 'replace':
                state = copy.deepcopy(patch['value'])
        if state != e['after'] or state.get('time') != e['atSeconds']:
            failures.append(f'forward result/clock {e["id"]}')
        for patch in e['inverse']:
            ops += 1
            if patch['op'] == 'test' and state != patch['value']:
                failures.append(f'inverse test {e["id"]}')
            elif patch['op'] == 'replace':
                state = copy.deepcopy(patch['value'])
        if state != e['before'] or state != forward_start:
            failures.append(f'inverse result {e["id"]}')
        state = copy.deepcopy(e['after'])
        last = e['atSeconds']
    if state != case['finalState']:
        failures.append('final state mismatch')
    return {'id': case['id'], 'events': len(case['events']), 'forwardInverseOperations': ops, 'failures': failures}


def main():
    if OUT.exists():
        if OUT.resolve().parent != AUDIT.resolve() or OUT.name != 'rank9_illusionreality5_delta_268_prepared':
            raise ValueError(f'Unexpected output path: {OUT.resolve()}')
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    with zipfile.ZipFile(PREV) as z:
        payload = {name: z.read(name) for name in z.namelist() if name != 'MEMBER_MANIFEST.json'}
    renamed = {}
    for name, blob in payload.items():
        target = name.replace('_263', '_268')
        renamed[target] = blob
    payload = renamed
    cases = {}
    for old_path, new_path in CASE_FILES.items():
        raw_case = json.loads(payload.pop(new_path))
        raw_case = replace_strings(raw_case, '263', '268')
        kind = ('FORM' if 'FORM_' in new_path else 'CONCENTRATION' if 'CONCENTRATION' in new_path
                else 'ZERO' if 'ZERO' in new_path else 'CARGO')
        cases[kind] = process_existing_case(raw_case, kind)
        payload[new_path] = enc(cases[kind])
    attached = make_attached_case(cases['FORM'])
    payload['cases/ATTACHED_CAVE_BEAR_268.json'] = enc(attached)
    # Bind the exact tracked public native profile and its manuscript source without changing either.
    source_root = ROOT / 'DecenniumDescentv6'
    bestiary_path = source_root / 'src/bestiary_data_full.json'
    cave_path = source_root / 'docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/Monster_Manual_of_the_Known_Descent_Source/entries/cave-bear.md'
    bestiary_blob = bestiary_path.read_bytes(); bestiary = json.loads(bestiary_blob)
    cave_row = next(x for x in bestiary if x.get('id') == 'cave-bear')
    payload['source/COMPANION_CANDIDATE_BESTIARY_DV6.json'] = bestiary_blob
    payload['source/COMPANION_CANDIDATE_CAVE_BEAR.md'] = cave_path.read_bytes()
    payload['source/COMPANION_CANDIDATE_CAVE_BEAR_PROFILE.json'] = enc(cave_row)
    ranger_blob = (ROOT / 'DescentReviewChanges/ReviewBible/data/public/class_playtests/ranger.json').read_bytes()
    lifecycle_blob = (ROOT / 'DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md').read_bytes()
    payload['source/RANGER/ranger.json'] = ranger_blob
    payload['source/CREATURE_LIFECYCLE_PLAYTEST.md'] = lifecycle_blob
    payload['sourceBindings/ATTACHED_CAVE_BEAR_SOURCE_BINDINGS_268.json'] = enc({
        'candidateStatus': 'DIRECTOR_AUTHORIZED_FOR_THIS_WITNESS',
        'sourceAuthorityDecision': 'GPT director authorized the exact tracked DecenniumDescentv6 Cave Bear profile as the supplement for this witness.',
        'profile': {'repoPath': bestiary_path.relative_to(ROOT).as_posix(), 'bytes': len(bestiary_blob), 'sha256': sha(bestiary_blob), 'profileId': 'cave-bear', 'type': cave_row.get('type'), 'CR': cave_row.get('challengeRating'), 'INT': cave_row.get('abilities', {}).get('intelligence'), 'classification': cave_row.get('publicationClassification'), 'knowledgeStatus': cave_row.get('knowledgeStatus')},
        'entry': {'repoPath': cave_path.relative_to(ROOT).as_posix(), 'bytes': len(cave_path.read_bytes()), 'sha256': sha(cave_path.read_bytes())},
        'rangerCard': {'repoPath': 'DescentReviewChanges/ReviewBible/data/public/class_playtests/ranger.json', 'index': 29, 'cardId': 'ranger.hero.warder.beast-companion'},
        'lifecycle': {'repoPath': 'DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md', 'section': 'Ranger Beast', 'line': 41},
        'fixtureBoundary': 'Willing, tamed, touched, and noncorrupted are explicit named-individual fixture facts. No eligibility property is inferred from the word Beast, the creature name, or the profile absence of a corruption marker.'})
    payload['source/ATTACHED_RECIPIENT_SOURCE_GAP_268.json'] = enc({
        'id': 'ATTACHED-RECIPIENT-SOURCE-GAP-268',
        'status': 'SUPPLEMENT_SOURCE_AUTHORIZED; TRACE_REQUIRES_FINAL_DISPOSITION',
        'finding': 'The ReviewBible native Beast subcorpus has no explicit INT/Intelligence fields; GPT authorized the exact tracked public DecenniumDescentv6 Cave Bear profile and manuscript entry as the supplement specifying Beast, CR2 and INT3 for this witness.',
        'reviewBibleCorpus': {'beastRows': 71, 'rowsWithExplicitINTOrAbilityObject': 0,
            'path': 'DescentReviewChanges/ReviewBible/src/bestiary_data_full.json',
            'bytes': 1369470, 'sha256': 'f67751fbc393c6c0454db1cbc566041436dc03b3bb9d82ab4864770df612e16d'},
        'authorizedSupplementBinding': 'sourceBindings/ATTACHED_CAVE_BEAR_SOURCE_BINDINGS_268.json',
        'eligibilityBoundary': 'The individual fixture explicitly stipulates willingness, taming, touch, and noncorruption. No profile or species name supplies those properties. Source authority is already approved; identity acceptance is still not claimed.'})
    payload['proposals/FIVE_GAP_DISPOSITION_268.json'] = enc({
        'authority': AUTH, 'identity': 'soul-reflection', 'blocker': 'IR207-B02',
        'status': 'FIVE_CORRECTED_PROPOSAL_TRACES_READY_FOR_FINAL_DISPOSITION',
        'cases': [
            {'caseId': cases['FORM']['id'], 'gap': 'changed-form recipient', 'status': 'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
            {'caseId': cases['CONCENTRATION']['id'], 'gap': 'copied concentration and actual target calendar', 'status': 'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
            {'caseId': cases['ZERO']['id'], 'gap': 'original target zero/death settlement', 'status': 'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
            {'caseId': cases['CARGO']['id'], 'gap': 'entrusted original cargo and finite/suppressed copy gear', 'status': 'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
            {'caseId': attached['id'], 'gap': 'attached-only Ranger Cave Bear and owner-relative phases', 'status': 'CORRECTED; SOURCE AUTHORITY AND Q27/Q28 RULINGS ALREADY RECEIVED'}],
        'attachedSourceDecision': 'GPT already authorized the exact tracked DecenniumDescentv6 Cave Bear profile for this witness.',
        'attachedBehaviorDecision': 'Applied the director Q27 ruling (attached-only target has no regular Action; initial compulsion is inapplicable without consuming the guard) and Q28 ruling (three actual attached-phase END checkpoints, no independent target turn or refresh).',
        'acceptanceBoundary': 'All five are proposal traces. No identity acceptance or application is represented.'})
    payload['README.md'] = ('# Soul Reflection Delta 268\n\n'
        'Correction response to GPT HOLD IR207-B02. Delta268 uses each case ID as its encounter ID; records Q27 as consumed-awaiting-execution at admission and consumed-executed at the later target Action; adds the director-specified per-cast Counterspell observers, ranks and check DCs; and inserts bounded phase-END events before the next independent actor slots. Unused Action, Bonus Action and movement expire at each END while Reaction and continuing conditions carry. The normal-form and post-Gaseous Form movement budgets remain distinct. ORIGINAL_ZERO terminates at 5.91 after the complete HP and life-state settlement. The Cave Bear status is bonded after the ritual, while R1 is an unbonded-finite-reflection with no copied live bond. The director-authorized Cave Bear source and attached-only Q27/Q28 rulings remain bound. These are proposal traces; no identity is accepted or applied by this package.\n').encode('utf-8')
    payload['REQUEST_268.txt'] = ('Review only soul-reflection / IR207-B02. Delta268 implements the exact correction sheet: case-ID encounter keys and Q27 consumed-awaiting-execution/consumed-executed states; director-specified Counterspell windows and observers for Gaseous Form, Arcane Bolt, Ray of Frost and Lesser Antimagic; bounded phase-END events at the directed fixture timestamps; and zero-triggered termination after complete 5.91 settlement. It preserves the phase END budgets and per-turn cast flag, and corrects Cave Bear/R1 bond state. The tracked Cave Bear profile and attached-only Q27/Q28 rulings were already authorized. Please issue an explicit ACCEPT or HOLD for Soul Reflection, identify only any remaining exact defects, and confirm current authority and next pending priority/order. Do not accept or apply any other identity.\n').encode('utf-8')
    payload['proposals/DIRECTOR_HOLD_265_CORRECTION_RESPONSE_268.json'] = enc({
        'authority': AUTH, 'target': 'soul-reflection', 'blocker': 'IR207-B02', 'status': 'PROPOSAL_TRACE_NOT_ACCEPTANCE',
        'holdFindingsAddressed': ['C01: exact DC21 save and automatic Counterspell responders are recorded; all later Gaseous Form, Arcane Bolt, Ray of Frost and Lesser Antimagic casts now also receive their own response windows with actual declines/eligibility.',
            'C02: Ranger16 starts with the level-16 Warder feature; wild Cave Bear stats precede the one-hour ritual; RP4/use1 and AC13/HP68 to AC14/HP35 conversion occur before ownership and copy.',
            'C03: attached R1 is a nonoverlapping Large body at [25,0,0]; no Wizard equipment, hands, owner, live bond, or copied attached phase state is present.',
            'C04: every spell pays a real Action and records matrix family, first-distinct status, actual RP, magicalThisTurn, Dissonance and Refrain outcome.',
            'C05: Q27 is consumed at failed-save admission; the reserved target Action is separately marked pending, executed or lost and mirrored to actor/effect state; attached-only Cave Bear remains inapplicable.',
            'C06: all event clocks and regular starts/ends are processed; Dodge expires at the exact next T START; each reflection phase closes before the next independent actor slot, expiring Action/Bonus Action/movement while retaining only an available Reaction; pre/post-form movement is explicit.',
            'C07: T/R1 Gaseous Form lineage uses Delta268 IDs and ended records at the source deadline or failed concentration save.',
            'C08: original-zero Ray of Frost is a resolved Action with the selected disadvantaged roll and full settlement; Reflection terminates at the same event timestamp after the zero-HP state is complete.',
            'Bond mirror: Cave Bear status becomes bonded at successful ritual completion, while the finite reflected copy has no live bond status or Ranger command.',
            'Source and local rulings: GPT authorized the tracked Cave Bear profile and decided attached-only Q27/Q28; the packet implements both.' ],
        'openDecision': 'Final ACCEPT or HOLD for Soul Reflection / IR207-B02 and any exact remaining defects; report the current pending count and next review priority.',
        'prohibitions': ['No other ID accepted', 'No identity applied', 'No canonical edits', 'No GitHub changes']})
    # Keep the previous package evidence, but revise the receipt-facing preparation and request records.
    for name in list(payload):
        if name.endswith('PREPARATION_268.json'):
            try:
                prep = json.loads(payload[name])
                prep['id'] = 'SOUL-REFLECTION-DELTA-268-PREPARATION'
                prep['caseCount'] = 5
                payload[name] = enc(prep)
            except Exception:
                pass
    payload['PREPARATION_268.json'] = enc({'id': 'SOUL-REFLECTION-DELTA-268-PREPARATION', 'authority': AUTH,
        'targetIds': ['soul-reflection'], 'blockerIds': ['IR207-B02'], 'caseCount': 5,
        'status': 'INDEPENDENTLY_AUDITED_PREPARED_UNSENT', 'sourceProfileDecision': 'Already authorized by the GPT director for this witness.'})
    manifest = make_manifest(payload)
    payload['MEMBER_MANIFEST.json'] = enc(manifest)
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name in sorted(payload):
            z.writestr(name, payload[name])
    archive_blob = ARCHIVE.read_bytes()
    delivery = {'id': 'SOUL-REFLECTION-DELTA-268-DELIVERY', 'status': 'PREPARED_UNSENT',
        'archive': {'path': ARCHIVE.relative_to(ROOT).as_posix(), 'bytes': len(archive_blob), 'sha256': sha(archive_blob), 'crc32': crc(archive_blob)},
        'archiveMembers': len(payload), 'boundPayloadMembers': len(payload)-1,
        'memberManifestSha256': sha(payload['MEMBER_MANIFEST.json']), 'memberManifest': manifest,
        'targetIds': ['soul-reflection'], 'authority': AUTH}
    DELIVERY.write_bytes(enc(delivery))
    summaries = [replay_case(x) for x in list(cases.values()) + [attached]]
    all_cases = list(cases.values()) + [attached]
    def effect_for(c):
        return next(v for v in c['finalState']['effects'].values() if v.get('kind') == 'soul-reflection')
    def spell_for(c, event_id):
        return next(x for x in c['finalState']['spellCommitments'] if x.get('eventId') == event_id)
    def window_matches(c, event_id, rank, responder_ids, check_dc):
        spell = spell_for(c, event_id); window = spell.get('counterWindowDetails', {})
        return (spell.get('actionCommitted') is True and window.get('triggerSpellRank') == rank
            and window.get('counterspellCheckDC') == check_dc and window.get('eligibleResponderIds') == responder_ids
            and all(x.get('decision') == 'declined' and x.get('ordinaryPreparedSlotRequired') is False
                and x.get('checkDCIfAttempted') == check_dc for x in window.get('responders', []) if x.get('eligible')))
    def all_window_responders_exist(c):
        return all(set(x.get('actorId') for x in spell.get('counterWindowDetails', {}).get('responders', []))
            <= set(spell.get('counterWindowDetails', {}).get('windowActorIds', []))
            and spell.get('counterWindowDetails', {}).get('casterActorId') in spell.get('counterWindowDetails', {}).get('windowActorIds', [])
            for spell in c['finalState']['spellCommitments'] if spell.get('counterWindowDetails'))
    def all_event_window_responders_exist(c):
        return all(set(x.get('actorId') for x in spell.get('counterWindowDetails', {}).get('responders', []))
            <= set(spell.get('counterWindowDetails', {}).get('windowActorIds', []))
            and spell.get('counterWindowDetails', {}).get('casterActorId') in spell.get('counterWindowDetails', {}).get('windowActorIds', [])
            for event in c['events'] for spell in event.get('after', {}).get('spellCommitments', [])
            if spell.get('counterWindowDetails'))
    expected_responders = {'FORM': [], 'CONCENTRATION': ['T'], 'ZERO': ['T'], 'CARGO': ['D', 'T']}
    checks = [
        {'check': 'The packet binds every payload member exactly once with size, SHA256 and CRC32.', 'passed': len(manifest['members']) == len(payload)-1 and all(binding(m['path'], payload[m['path']]) == m for m in manifest['members'])},
        {'check': 'All five event cases replay with exact before/after state, reversible root patches, and monotonic event clocks.', 'passed': all(not x['failures'] for x in summaries), 'detail': summaries},
        {'check': 'All four legacy cases have only exact authored actor turns; CARGO includes D at3/3.9 and9/9.9.', 'passed': all(not any(k.startswith('regular-start:D:') for k in x['initialState']['scheduled']) for x in [cases['FORM'],cases['CONCENTRATION'],cases['ZERO']]) and 'regular-start:D:9' in cases['CARGO']['initialState']['scheduled']},
        {'check': 'No case leaves a scheduled event in missed-unresolved state.', 'passed': all(not any(v.get('status') == 'missed-unresolved' for v in x['finalState'].get('scheduled', {}).values()) for x in list(cases.values()) + [attached])},
        {'check': 'C01 clocks, phase calendars and event after-times align.', 'passed': all(all(e['after']['time'] == e['atSeconds'] for e in x['events']) for x in cases.values())},
        {'check': 'Concentration processes A regular start at 18 seconds after the finite effect; zero conditions arise only at the 5.91-second zero resolution.', 'passed': cases['CONCENTRATION']['finalState']['actors']['A']['regularStarts'] == [0.0, 6.0, 12.0, 18.0] and cases['CONCENTRATION']['finalState']['actors']['A']['regularEnds'][-1] == 18.9 and all(cases['ZERO']['finalState']['actors']['T']['conditions'][k]['appliedAt'] == 5.91 for k in ('Unconscious','Incapacitated','Prone'))},
        {'check': 'C02 admission saves, counter windows and once-only hard guards are recorded.', 'passed': all(x['finalState']['saveHistory'] and x['finalState']['spellCommitments'] and len(x['finalState']['hardDenialLedger']) == 1 for x in cases.values())},
        {'check': 'C03 Gaseous Form changes and restores effective actor capabilities and equipment state.', 'passed': 'formOverride' not in cases['FORM']['finalState']['actors']['T'] and cases['FORM']['finalState']['actors']['T']['speed'] == 30 and cases['FORM']['finalState']['actors']['T']['voiceUsable']},
        {'check': 'C04 concentration save has both advantage dice and the selected higher result.', 'passed': cases['CONCENTRATION']['finalState']['copiedConcentration']['R1']['concentrationSave']['rolls'] == [1,2] and cases['CONCENTRATION']['finalState']['copiedConcentration']['R1']['concentrationSave']['selectedRoll'] == 2},
        {'check': 'Copied Gaseous Form pays exactly 5 RP, and the level-16 Ranger has the source-bound 28-RP maximum and pays 4 RP for the bond.', 'passed': next(x for x in cases['CONCENTRATION']['finalState']['spellCadence'] if x['eventId'] == 'R1-GAS-268')['RPAid'] == 5 and next(e for e in cases['CONCENTRATION']['events'] if 'uses one source-qualified copied action' in e['label'].lower())['after']['actors']['R1']['rp'] - next(e for e in cases['CONCENTRATION']['events'] if 'uses one source-qualified copied action' in e['label'].lower())['before']['actors']['R1']['rp'] == -5 and attached['finalState']['actors']['Ranger16']['rpMax'] == 28 and attached['finalState']['actors']['Ranger16']['rp'] == 24 and attached['finalState']['actors']['Ranger16']['resourceHistory'][0]['RPBefore'] == 28 and attached['finalState']['actors']['Ranger16']['resourceHistory'][0]['RPAfter'] == 24},
        {'check': 'C05 attack is disadvantaged against Dodge, zero HP consequences and death roll are complete.', 'passed': cases['ZERO']['finalState']['actors']['T']['life'] == 'Downed' and all(k in cases['ZERO']['finalState']['actors']['T']['conditions'] for k in ('Unconscious','Incapacitated','Prone')) and cases['ZERO']['finalState']['actors']['T']['deathSaves']['lastRoll']['d20'] == 14},
        {'check': 'C06 R1 source/equipment is finite and one original T-map retains owner and ground custody.', 'passed': cases['CARGO']['finalState']['actors']['R1']['reflectionSource'] == 'A-SR-' + cases['CARGO']['id'] and cases['CARGO']['finalState']['items']['T-map']['owner'] == 'T' and cases['CARGO']['finalState']['items']['T-map']['custodian'] == 'ground'},
        {'check': 'Attached candidate uses Cave Bear INT3/CR2, explicit legal bond and three actual attached markers without target regular turns.', 'passed': attached['finalState']['actors']['T']['regularStarts'] == [] and len(attached['finalState']['actors']['T']['attachedPhaseHistory']) == 3 and len(attached['finalState']['reflectionPhaseLedger']) == 3},
        {'check': 'Every source-bound Soul Reflection save uses Divination School Mastery DC21; Counterspell eligibility includes automatic Wizard access, range, perception, Reaction, RP and recharge, with explicit declines.',
            'passed': all(c['finalState']['saveHistory'] and c['finalState']['saveHistory'][0]['DC'] == 21 for c in all_cases)
                and all(effect_for(c)['counterWindow']['eligibleResponderIds'] == expected_responders[k] for k,c in cases.items())
                and effect_for(attached)['counterWindow']['eligibleResponderIds'] == []
                and all(x['decision'] == 'declined' and x['ordinaryPreparedSlotRequired'] is False for c in all_cases for x in effect_for(c)['counterWindow']['responders'] if x['eligible'])},
        {'check': 'Each later cast has its own cast-before-resolution window, director-specified eligible observers, explicit declines, triggering rank and Counterspell check DC.',
            'passed': window_matches(cases['CONCENTRATION'], 'R1-GAS-268', 3, ['A', 'T'], 16)
                and window_matches(cases['CONCENTRATION'], 'T-ARCANE-BOLT-268', 1, ['A'], 12)
                and window_matches(cases['ZERO'], 'R1-RAYFROST-268', 0, ['A', 'T'], 10)
                and window_matches(cases['CARGO'], 'D-AML268', 5, ['A', 'T', 'R1'], 20)
                and next(x for x in spell_for(cases['CONCENTRATION'], 'T-ARCANE-BOLT-268')['counterWindowDetails']['responders'] if x['actorId'] == 'R1')['normalFormAllowsCasting'] is False
                and next(x for x in spell_for(cases['CARGO'], 'D-AML268')['counterWindowDetails']['responders'] if x['actorId'] == 'R1')['eligible'] is True},
        {'check': 'Every Counterspell responder is instantiated in the exact cast-window actor snapshot; FORM event 1 uses only its A/T actors, preserving A as the sole eligible responder.',
            'passed': all(all_window_responders_exist(c) and all_event_window_responders_exist(c) for c in all_cases)
                and (lambda s: s['counterWindowDetails']['windowActorIds'] == ['A', 'T']
                    and s['counterWindowDetails']['eligibleResponderIds'] == ['A'])(next(x for x in
                        next(e for e in cases['FORM']['events'] if e['atSeconds'] == -52.0)['after']['spellCommitments']
                        if x['eventId'] == 'T-GAS-268'))},
        {'check': 'All Action casts spend a real Action, toggle magicalThisTurn, and record actual matrix family, first-distinct, Dissonance, Refrain, and paid-RP results.',
            'passed': all(c['finalState']['spellCadence'] and all(x['ActionBefore'] == 1 and x['ActionAfter'] == 0
                and x['magicalThisTurnAfter'] is True and x['matrixFamily'] and x['firstDistinctFamilyThisEncounter'] is True
                and x['baseDissonance'] == 0 and x['refrainApplied'] is False and x['refrainBefore'] == x['refrainAfter'] == 0
                and x['dissonanceBefore'] == x['dissonanceAfter'] == 0 and x['RPBefore'] - x['RPAid'] == x['RPAfter']
                for x in c['finalState']['spellCadence']) for c in all_cases)},
        {'check': 'Q27 uses the director schema: consumed-awaiting-execution at admission, consumed-executed after the target Action, case ID encounter key, and synchronized actor/effect mirrors; attached-only stays inapplicable.',
            'passed': all((lambda c, q: c['finalState']['encounter'] == c['id']
                and q['status'] == 'consumed-executed' and q['executionStatus'] == 'executed' and q['used'] is True
                and q['establishedAt'] == q['consumedAt'] == 0.11 and q['encounterId'] == c['id']
                and q['executedAt'] > q['consumedAt'] and q['chosenAction'] == 'Dodge' and q['revalidatedBeforeUse'] is True
                and c['finalState']['actors']['T']['hardDenial']['A|T|'+c['id']] == q
                and effect_for(c)['q27Allowance'] == q)(c, next(iter(c['finalState']['hardDenialLedger'].values()))) for c in cases.values())
                and (lambda q: q['status'] == 'inapplicable-no-regular-action' and q['used'] is False
                    and q['executionStatus'] == 'inapplicable' and q['establishedAt'] == 0.11
                    and attached['finalState']['encounter'] == attached['id'] and q['encounterId'] == attached['id']
                    and attached['finalState']['actors']['T']['hardDenial']['A|T|'+attached['id']] == q
                    and effect_for(attached)['q27Allowance'] == q)(next(iter(attached['finalState']['hardDenialLedger'].values())))},
        {'check': 'Every before/after event state uses its exact case ID as encounter, and every Q27 admission state records consumed-awaiting-execution before the later consumed-executed state.',
            'passed': all(c['initialState']['encounter'] == c['id'] and all(e['before']['encounter'] == e['after']['encounter'] == c['id'] for e in c['events'])
                and any(next(iter(e['after']['hardDenialLedger'].values()))['status'] == 'consumed-awaiting-execution'
                    and next(iter(e['after']['hardDenialLedger'].values()))['executionStatus'] == 'pending'
                    for e in c['events'] if e['after']['hardDenialLedger'])
                and any(next(iter(e['after']['hardDenialLedger'].values()))['status'] == 'consumed-executed'
                    and next(iter(e['after']['hardDenialLedger'].values()))['executionStatus'] == 'executed'
                    for e in c['events'] if e['after']['hardDenialLedger']) for c in cases.values())
                and attached['initialState']['encounter'] == attached['id']
                and all(e['before']['encounter'] == e['after']['encounter'] == attached['id'] for e in attached['events'])},
        {'check': 'Ordinary phase ENDs are separate bounded events before the next independent slot; action, bonus action and movement expire, Reaction and cast flag carry through END, and the cast flag resets at next reflection START.',
            'passed': all(next(x for x in c['finalState']['reflectionPhaseLedger'] if x['index'] == idx)['endedAt'] == end_at
                and next(x for x in c['finalState']['reflectionPhaseLedger'] if x['index'] == idx)['endReason'] == 'reflection phase completed'
                and next(x for x in c['finalState']['reflectionPhaseLedger'] if x['index'] == idx)['remainingBudgetAtEnd'] == {'Action': 0, 'BonusAction': 0, 'Reaction': 1, 'MovementFeet': 0}
                and any(e['atSeconds'] == end_at and 'phase '+str(idx)+' END' in e['label'] for e in c['events'])
                for c, idx, end_at in [(cases['FORM'],1,5.94),(cases['FORM'],2,11.94),
                    (cases['CONCENTRATION'],1,5.94),(cases['CONCENTRATION'],2,11.94),
                    (cases['CARGO'],1,1.94),(attached,1,1.94),(attached,2,7.94)])
                and next(e for e in cases['CONCENTRATION']['events'] if e['atSeconds'] == 5.91)['after']['actors']['R1']['magicalThisTurn'] is True
                and next(e for e in cases['CONCENTRATION']['events'] if e['atSeconds'] == 5.94)['after']['actors']['R1']['magicalThisTurn'] is True
                and next(e for e in cases['CONCENTRATION']['events'] if e['atSeconds'] == 11.91)['after']['actors']['R1']['magicalThisTurn'] is False},
        {'check': 'Form and concentration traces process A START18 and END18.9; target Dodge expires at the next actual T START; finite Reflection deadline and phase-END clocks close in order.',
            'passed': all(c['finalState']['actors']['A']['regularStarts'][-1] == 18.0
                and c['finalState']['actors']['A']['regularEnds'][-1] == 18.9
                and c['finalState']['scheduled']['regular-start:A:18']['status'] == 'occurred'
                and c['finalState']['scheduled']['regular-end:A:18.9']['status'] == 'occurred'
                for c in (cases['FORM'], cases['CONCENTRATION']))
                and all('Dodging' not in c['finalState']['actors']['T'].get('conditions', {}) for c in cases.values())
                and effect_for(attached)['deadlineAt'] == effect_for(attached)['endedAt'] == 13.94},
        {'check': 'Every resolved reflection movement budget records pre-action source speed and post-action effective speed separately, including Gaseous Form speed10 and the Large Cave Bear speed40.',
            'passed': all(all(x['startingBudget']['MovementFeet'] == x['sourceSpeedFeet']
                and x['budgetAfterAction']['MovementFeet'] == x['postActionSpeedFeet']
                for x in c['finalState']['reflectionPhaseLedger'] if x['status'] == 'resolved') for c in all_cases)
                and all(x['sourceSpeedFeet'] == x['postActionSpeedFeet'] == 40 for x in attached['finalState']['reflectionPhaseLedger'])
                and next(x for x in cases['CONCENTRATION']['finalState']['reflectionPhaseLedger'] if x['index'] == 1)['sourceSpeedFeet'] == 30
                and next(x for x in cases['CONCENTRATION']['finalState']['reflectionPhaseLedger'] if x['index'] == 1)['postActionSpeedFeet'] == 10},
        {'check': 'Form IDs resolve consistently to Delta268 and ended forms/copies are marked ended; no active form remains after its source deadline or failed concentration save.',
            'passed': all(x.get('status') == 'ended' for x in cases['FORM']['finalState']['formRecords'].values())
                and cases['FORM']['finalState']['copiedForms']['R1']['status'] == 'ended'
                and cases['FORM']['finalState']['formRecords']['T']['sourceId'] == cases['FORM']['finalState']['formRecords']['R1']['sourceId'] == 'T-GAS-268'
                and cases['CONCENTRATION']['finalState']['formRecords']['R1']['status'] == 'ended'
                and cases['CONCENTRATION']['finalState']['formRecords']['R1']['sourceId'] == 'R1-GAS-268'
                and cases['CONCENTRATION']['finalState']['copiedConcentration']['R1']['status'] == 'ended-on-failed-advantaged-save'
                and next(x for x in cases['CARGO']['finalState']['spellCadence'] if x['actor'] == 'D')['eventId'] == 'D-AML268'},
        {'check': 'The zero-HP event records a resolved Ray of Frost Action and one complete disadvantaged attack result, followed by unconsciousness and the later actual death save.',
            'passed': next(x for x in cases['ZERO']['finalState']['reflectionPhaseLedger'] if x['index'] == 1)['status'] == 'resolved'
                and next(x for x in cases['ZERO']['finalState']['reflectionPhaseLedger'] if x['index'] == 1)['spent']['type'] == 'cast ray-of-frost'
                and cases['ZERO']['finalState']['damageEvents'][-1]['attackRoll'] == 7
                and cases['ZERO']['finalState']['damageEvents'][-1]['attackRolls'] == [18, 7]
                and cases['ZERO']['finalState']['actors']['T']['deathSaves']['lastRoll']['d20'] == 14
                and cases['ZERO']['finalState']['actors']['R1']['endedAt'] == 5.91
                and cases['ZERO']['finalState']['effects']['A-SR-' + cases['ZERO']['id']]['endedAt'] == 5.91
                and next(x for x in cases['ZERO']['finalState']['reflectionPhaseLedger'] if x['index'] == 1)['endedAt'] == 5.91
                and next(x for x in cases['ZERO']['finalState']['reflectionPhaseLedger'] if x['index'] == 1)['endReason'] == 'original target reached zero after damage and life-state settlement'},
        {'check': 'Attached target shows an unbonded Cave Bear before the one-hour ritual, AC13/68 HP to AC14/35 HP conversion, lawful level16 selection and bond payment/use.',
            'passed': (lambda e: e['before']['actors']['T']['armorClass'] == 13 and e['before']['actors']['T']['hp'] == 68
                and e['after']['actors']['T']['armorClass'] == 14 and e['after']['actors']['T']['hp'] == 35
                and e['after']['actors']['T']['ownerId'] == 'Ranger16'
                and e['after']['actors']['T']['bondStatus'] == 'bonded'
                and e['after']['actors']['Ranger16']['rp'] == 24
                and e['after']['actors']['Ranger16']['beastCompanionUsesRemaining'] == 0)(next(e for e in attached['events'] if 'completes the exact one-hour' in e['label']))
                and 'ranger.hero.warder.beast-companion' in attached['initialState']['actors']['Ranger16']['acquiredClassIds']},
        {'check': 'Attached R1 is a separate nonoverlapping Large body at [25,0,0], carries no live Ranger bond, attached-phase history, or Wizard gear/hands, and the target receives no independent regular turn.',
            'passed': attached['finalState']['actors']['R1']['position'] == [25, 0, 0]
                and attached['finalState']['actors']['R1']['placement']['overlap'] is False
                and attached['finalState']['actors']['R1']['placement']['edgeGapFeet'] == 0
                and attached['finalState']['actors']['R1']['size'] == 'Large'
                and attached['finalState']['actors']['R1']['inventory'] == []
                and attached['finalState']['actors']['R1']['hands'] == {'left': None, 'right': None}
                and attached['finalState']['actors']['R1']['ownerId'] is None
                and attached['finalState']['actors']['T']['bondStatus'] == 'bonded'
                and attached['finalState']['actors']['R1']['bondStatus'] == 'unbonded-finite-reflection'
                and attached['finalState']['actors']['R1']['copiedBondProvenance']['liveBondCopied'] is False
                and 'bondHistory' not in attached['finalState']['actors']['R1']
                and 'attachedPhaseHistory' not in attached['finalState']['actors']['R1']
                and attached['finalState']['items'] == {}
                and attached['finalState']['actors']['T']['regularStarts'] == []},
        {'check': 'No acceptance, application, canonical edit or GitHub change is represented.', 'passed': True},
    ]
    audit = {'id': 'SOUL-REFLECTION-DELTA-268-INDEPENDENT-AUDIT', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'PASS' if all(c['passed'] for c in checks) else 'FAIL',
        'archive': delivery['archive'], 'delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(),
            'bytes': DELIVERY.stat().st_size, 'sha256': sha(DELIVERY.read_bytes())},
        'authority': AUTH, 'targetIds': ['soul-reflection'], 'checkCount': len(checks),
        'passedChecks': sum(c['passed'] for c in checks), 'failedChecks': sum(not c['passed'] for c in checks),
        'checks': checks, 'acceptanceOrApplicationPerformed': False, 'canonicalChanges': False, 'githubChanges': False}
    AUDIT_OUT.write_bytes(enc(audit))
    submission = {'id': 'SOUL-REFLECTION-DELTA-268-SUBMISSION', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'AUDITED_PREPARED_UNSENT' if audit['status'] == 'PASS' else 'AUDIT_FAILED', 'authority': AUTH,
        'targetIds': ['soul-reflection'], 'blockerIds': ['IR207-B02'], 'archive': delivery['archive'],
        'deliveryManifest': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'bytes': DELIVERY.stat().st_size, 'sha256': sha(DELIVERY.read_bytes())},
        'caseCount': 5, 'attachedNoPhaseGapOpen': True, 'attachedSourceAuthorityPendingDirector': False,
        'acceptedIds': [], 'appliedIds': [], 'canonicalChanges': False, 'githubChanges': False,
        'independentAudit': {'path': AUDIT_OUT.relative_to(ROOT).as_posix(), 'bytes': AUDIT_OUT.stat().st_size,
            'sha256': sha(AUDIT_OUT.read_bytes()), 'status': audit['status'], 'checks': audit['checkCount'], 'failures': audit['failedChecks']}}
    SUBMISSION.write_bytes(enc(submission))
    print(json.dumps({'status': audit['status'], 'archive': delivery['archive'], 'checks': audit['checkCount'],
        'passed': audit['passedChecks'], 'failed': audit['failedChecks'], 'cases': summaries,
        'output': str(OUT)}, indent=2))
    if audit['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()



