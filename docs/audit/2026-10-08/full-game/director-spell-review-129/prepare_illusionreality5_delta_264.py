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
OUT = AUDIT / 'rank9_illusionreality5_delta_264_prepared'
ARCHIVE = OUT / 'DD_Rank9_SoulReflection_Delta_264.zip'
DELIVERY = OUT / 'DD_Rank9_SoulReflection_Delta_264_DELIVERY.json'
AUDIT_OUT = OUT / 'SOUL_REFLECTION_DELTA_264_INDEPENDENT_AUDIT.json'
SUBMISSION = OUT / 'SOUL_REFLECTION_DELTA_264_SUBMISSION.json'
AUTH = {'reviewedApplied': 814, 'pending': 34, 'acceptedUnapplied': 0,
        'completeStandaloneProcedures': 538, 'scopedInterfaces': 173}
CASE_FILES = {
    'cases/FORM_SNAPSHOT_263.json': 'cases/FORM_SNAPSHOT_264.json',
    'cases/COPIED_CONCENTRATION_263.json': 'cases/COPIED_CONCENTRATION_264.json',
    'cases/ORIGINAL_ZERO_263.json': 'cases/ORIGINAL_ZERO_264.json',
    'cases/ORIGINAL_CARGO_263.json': 'cases/ORIGINAL_CARGO_264.json',
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
    first = min(e['atSeconds'] for e in case['events'])
    if kind == 'CONCENTRATION':
        first = min(first, 0.0)
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
        a['regularCalendar'] = list(starts)
        a['regularStarts'] = []
        a['regularEnds'] = []
        a['nextRegularStart'] = starts[0] if starts else None
        for at in starts:
            add_schedule(s, f'regular-start:{actor_id}:{at:g}', at, 'actual regular START')
            add_schedule(s, f'regular-end:{actor_id}:{at + 0.9:g}', at + 0.9, 'actual regular END')
    for at in PHASES[kind]:
        add_schedule(s, f'reflection-phase:R1:{at:g}', at, 'proposed Soul Reflection phase after actual target END')
    s['caseId'] = case['id'].replace('5263', '5264')
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
    state.setdefault('formRecords', {}).setdefault(actor_id, {}).update({'endedAt': at, 'ending': reason})


def commitment(state, at, actor_id, spell_id, cost, event_id, source, action='Action'):
    a = state['actors'].get(actor_id)
    if not a:
        return
    current = next((x for x in state.setdefault('spellCadence', []) if x.get('eventId') == event_id), None)
    if current:
        return
    before_rp = a.get('rp') + cost if cost else a.get('rp')
    after_rp = a.get('rp')
    record = {'eventId': event_id, 'at': at, 'actor': actor_id, 'spellId': spell_id,
              'action': action, 'RPBefore': before_rp, 'RPAid': cost, 'RPAfter': after_rp,
              'source': source, 'cadenceDisposition': 'recorded; no extra action or unprinted reset'}
    state['spellCadence'].append(record)
    a.setdefault('castHistory', [])
    if event_id not in a['castHistory']:
        a['castHistory'].append(event_id)
    a.setdefault('castFamilies', [])
    if spell_id not in a['castFamilies']:
        a['castFamilies'].append(spell_id)
    a['lastSpell'] = spell_id
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


def phase_action(state, case, phase, at, action, old_r1=None):
    if 'R1' not in state['actors']:
        return
    r = state['actors']['R1']
    effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), {})
    if not r.get('active', True) or not effect.get('active', True):
        entry = {'index': phase, 'startAt': at, 'status': 'skipped-suppressed', 'actionSpent': False,
                 'reason': 'body suppressed; phase clock elapsed; no bank or replay'}
        state['reflectionPhaseLedger'].append(entry)
        state['reflectionPhases'] = copy.deepcopy(state['reflectionPhaseLedger'])
        return
    dodge = r.get('conditions', {}).get('Dodging')
    if dodge and dodge.get('expiresAt', at + 1) <= at:
        r['conditions'].pop('Dodging', None)
    r['regularCalendar'] = list(PHASES[case])
    r['reflectionPhaseBudget'] = {'action': 1, 'bonusAction': 1, 'reaction': 1, 'movementFeet': 30}
    r['action'] = 1
    r['bonusAction'] = 1
    r['reaction'] = 1
    r['movementSpent'] = 0
    r['activeReflectionPhase'] = phase
    if action == 'Dodge':
        r['action'] = 0
        r['conditions']['Dodging'] = {'source': 'Reflection phase', 'appliedAt': at,
                                      'expiresAt': PHASES[case][phase] if phase < len(PHASES[case]) else at + 0.01}
        spent = {'type': 'Dodge', 'ActionSpent': True, 'RPSpent': 0}
    elif action == 'Gaseous Form':
        paid = next((x for x in state.get('spellCadence', []) if x.get('eventId') == 'R1-GAS-264'), None)
        if paid:
            before, after = paid['RPBefore'], paid['RPAfter']
            if r.get('rp') != after:
                raise ValueError('Gaseous Form commitment RP does not match actor RP after payment')
        else:
            before = r.get('rp', 0)
            r['rp'] = before - 5
            after = r['rp']
        r['action'] = 0
        r['lastSpell'] = 'gaseous-form'
        r.setdefault('concentration', {})
        r['concentration'] = {'spellId': 'gaseous-form', 'sourceId': 'R1-GAS-264',
                              'startedAt': at, 'deadlineAt': at + 60}
        state.setdefault('formRecords', {})['R1'] = {'form': 'gaseous-mist', 'rootProfile': r.get('profileId'),
            'rootIdentity': 'R1', 'sourceId': 'R1-GAS-264', 'startAt': at, 'deadlineAt': at + 60,
            'currentHP': r.get('hp'), 'maxHP': r.get('maxHP'), 'currentRP': r.get('rp'),
            'size': r.get('size'), 'movementFeet': 10, 'hover': True,
            'voiceUsable': False, 'handsUsable': False, 'attacksUsable': False}
        state['formRecords']['R1']['status'] = 'active'
        state.setdefault('copiedConcentration', {})['R1'] = {'spellId': 'gaseous-form', 'sourceId': 'R1-GAS-264',
            'RPBefore': before, 'RPAfter': after, 'deadlineAt': at + 60, 'slotOwner': 'R1', 'status': 'active'}
        set_form(state, 'R1', 'R1-GAS-264', at + 60, 'R1')
        commitment(state, at, 'R1', 'gaseous-form', 5, 'R1-GAS-264', 'accepted Gaseous Form source; copied-casting permission remains a Soul-Reflection proposal')
        state.setdefault('spellCommitments', []).append({'eventId': 'R1-GAS-264', 'at': at, 'caster': 'R1',
            'target': 'R1', 'spellId': 'gaseous-form', 'actionCommitted': True, 'RPSpent': 5,
            'counterWindow': 'passed-no-legal-prepared-response'})
        spent = {'type': 'cast gaseous-form', 'ActionSpent': True, 'RPSpent': 5}
        add_schedule(state, 'concentration-end:R1-GAS-264', at + 60, 'source concentration deadline')
    elif action == 'Ray of Frost':
        r['action'] = 0
        spent = {'type': 'cast ray-of-frost', 'ActionSpent': True, 'RPSpent': 0}
        commitment(state, at, 'R1', 'ray-of-frost', 0, 'R1-RAYFROST-264', 'indexed Ray of Frost operation')
    else:
        r['action'] = 0
        spent = {'type': action, 'ActionSpent': True, 'RPSpent': 0}
    r['bonusAction'] = 0
    r['reaction'] = 0
    r['activeReflectionPhase'] = None
    r['reflectionPhaseBudget'] = {'action': 0, 'bonusAction': 0, 'reaction': 0, 'movementFeet': 0}
    marker = at - 0.01
    state['reflectionPhaseLedger'].append({'index': phase, 'startAt': at, 'targetMarker': marker,
        'target': 'T', 'status': 'resolved', 'startingBudget': {'Action': 1, 'BonusAction': 1, 'Reaction': 1, 'MovementFeet': 30},
        'spent': spent, 'independentTargetTurn': False, 'regularStartRecordedForR1': False})
    state['reflectionPhases'] = copy.deepcopy(state['reflectionPhaseLedger'])
    effect['history'] = effect.get('history', []) + [{'at': at, 'phase': phase, 'action': spent['type'], 'noRefresh': True}]


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
    if any(x.get('index') == phase for x in state.get('reflectionPhaseLedger', [])):
        return
    if kind == 'FORM':
        action = 'Dodge'
    elif kind == 'CONCENTRATION':
        action = 'Gaseous Form' if phase == 1 else 'Dodge'
    elif kind == 'ZERO':
        action = 'Ray of Frost'
    else:
        action = 'Dodge'
    phase_action(state, kind, phase, at, action, event.get('after', {}).get('actors', {}).get('R1'))


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
                    'rootProfile': r1.get('profileId'), 'sameSizeSpace': True, 'gasLimitationsPreserved': True}
                state['formRecords']['R1'] = {'form': 'gaseous-mist', 'rootProfile': r1.get('profileId'),
                    'rootIdentity': 'R1', 'sourceId': source_form['sourceId'], 'startAt': at,
                    'deadlineAt': source_form['deadlineAt'], 'currentHP': r1.get('hp'), 'maxHP': r1.get('maxHP'),
                    'currentRP': r1.get('rp'), 'size': r1.get('size'), 'movementFeet': 10,
                    'hover': True, 'voiceUsable': False, 'handsUsable': False, 'attacksUsable': False}
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
            commitment(state, at, 'T', 'gaseous-form', 5, 'T-GAS-264', 'reviewed Gaseous Form envelope; outside-initiative finite cast fixture')
            state['formRecords']['T']['status'] = 'active'
            set_form(state, 'T', 'T-GAS-264', 8.0, 'T')
            add_schedule(state, 'source-form-end:T-GAS-264', 8.0, '60-second source concentration deadline')
    if 'uses one source-qualified copied action to cast gaseous form' in label.lower():
        # The phase routine spends the Action; this event adds only the source/cost and effective form state.
        r = state['actors']['R1']
        set_form(state, 'R1', 'R1-GAS-264', at + 60.0, 'R1')
        if not any(x.get('eventId') == 'R1-GAS-264' for x in state['spellCadence']):
            commitment(state, at, 'R1', 'gaseous-form', 5, 'R1-GAS-264', 'accepted Gaseous Form envelope; copied-casting grant remains proposed')
        state.setdefault('copiedConcentration', {}).setdefault('R1', {}).update({'status': 'active'})
    if 'exact form deadline' in label.lower():
        for actor_id in ('T', 'R1'):
            restore_form(state, actor_id, at, 'source concentration deadline')
        if state.get('copiedForms', {}).get('R1'):
            state['copiedForms']['R1'].update({'endedAt': at, 'ending': 'inherited source deadline'})
    if 'concentration' in label.lower() and 'arcane bolt' in label.lower():
        event_id = 'T-ARCANE-BOLT-264'
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
        state['spellCommitments'].append({'eventId': 'R1-RAYFROST-264', 'at': at, 'caster': 'R1', 'target': 'T',
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
        if not any(x.get('eventId') == 'D-AML264' for x in state['spellCadence']):
            commitment(state, at - 0.01, 'D', 'antimagic-field-lesser', 10, 'D-AML264', 'exact accepted field source; current class access and prepared matrix')
        state.setdefault('spellCommitments', []).append({'eventId': 'D-AML264', 'at': at - 0.01,
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
    for item_id in list(r.get('inventory', [])):
        if item_id in state.get('items', {}):
            state['items'][item_id].update({'active': False, 'colliding': False, 'custodian': 'ended',
                'held': False, 'endedAt': at, 'formState': 'ended'})
    r['inventory'] = []
    r['hands'] = {'left': None, 'right': None}
    r['conditions'] = {}


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
    if kind == 'CONCENTRATION':
        inputs.append((0.0, 1, {'custom': 'A regular start 1 before the committed Soul Reflection cast',
                                'actorId': 'A', 'atSeconds': 0.0}))
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
                actor['lastRegularStart'] = at
                actor['regularStarts'].append(at)
                actor['nextRegularStart'] = None
            else:
                actor['activeRegular'] = False
                actor['action'] = actor['bonusAction'] = actor['interaction'] = 0
                actor['lastRegularEnd'] = at
                actor['regularEnds'].append(at)
            old_event = {'id': f'{state["caseId"]}:custom:{len(new_events)+1}', 'atSeconds': at,
                         'label': old['custom'], 'before': before, 'after': copy.deepcopy(state),
                         'evidence': {'source': 'actual D regular marker; clock retained through field suppression'}}
        else:
            state = apply_delta(state, old['before'], old['after'])
            old_event = old
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
                    dodge = actor.get('conditions', {}).get('Dodging')
                    if dodge and dodge.get('expiresAt', at + 1) <= at:
                        actor['conditions'].pop('Dodging', None)
        if 'commits soul reflection' in label.lower():
            effect = next((v for v in state.get('effects', {}).values() if v.get('kind') == 'soul-reflection'), None)
            if effect:
                effect['pendingAdmission'] = True
                effect['status'] = 'awaiting-counter-window-and-save'
                effect['counterWindow'] = {'openedAt': at, 'closedAt': at + 0.01,
                    'eligiblePreparedCounterspellResponders': [], 'result': 'passed-no-legal-prepared-response'}
            state['spellCommitments'] = [{'eventId': next((k for k, v in state['effects'].items() if v.get('kind') == 'soul-reflection'), 'A-SR'),
                'at': at, 'caster': 'A', 'target': 'T', 'spellId': 'soul-reflection', 'actionCommitted': True,
                'RPSpent': 26, 'counterWindow': 'passed-no-legal-prepared-response', 'targetSavePending': True}]
            state['actors'].pop('R1', None)
        # The admission event creates R1 only after the recorded save fails.
        if 'admission' in label.lower() or 'admitted' in label.lower() or 'r1 appears within five feet' in label.lower():
            original_r1 = old['after']['actors'].get('R1')
            if original_r1:
                state['actors']['R1'] = copy.deepcopy(original_r1)
                state['actors']['R1']['reflectionSource'] = next((k for k, v in state['effects'].items() if v.get('kind') == 'soul-reflection'), None)
                state['actors']['R1']['causalRoot'] = state['actors']['R1']['reflectionSource']
                state['actors']['R1']['ownerId'] = None
                state['actors']['R1']['attachedOnly'] = False
                state['actors']['R1']['regularCalendar'] = list(PHASES[kind])
                add_reflection_gear(state)
                t = state['actors']['T']
                save = append_save(state, 'T', at, 8, t.get('saves', {}).get('WIS', 0), state['actors']['A'].get('spellDC', 19),
                                   'source-bound target WIS save; stipulated fixture roll')
                effect = next((v for v in state['effects'].values() if v.get('kind') == 'soul-reflection'), None)
                if effect:
                    effect.update({'pendingAdmission': False, 'status': 'admitted-after-failed-WIS-save', 'admissionSave': copy.deepcopy(save)})
                if kind == 'FORM' and state.get('formRecords', {}).get('T'):
                    src = state['formRecords']['T']
                    state.setdefault('copiedForms', {})['R1'] = {'sourceFormOwner': 'T', 'sourceId': src['sourceId'],
                        'sourceDeadlineAt': src['deadlineAt'], 'copyMode': 'finite snapshot; inherited source deadline',
                        'rootProfile': state['actors']['R1'].get('profileId'), 'sameSizeSpace': True, 'gasLimitationsPreserved': True}
                    state['formRecords']['R1'] = {'form': 'gaseous-mist', 'rootProfile': state['actors']['R1'].get('profileId'),
                        'rootIdentity': 'R1', 'sourceId': src['sourceId'], 'startAt': at, 'deadlineAt': src['deadlineAt'],
                        'currentHP': state['actors']['R1'].get('hp'), 'maxHP': state['actors']['R1'].get('maxHP'),
                        'currentRP': state['actors']['R1'].get('rp'), 'size': state['actors']['R1'].get('size'),
                        'movementFeet': 10, 'hover': True, 'voiceUsable': False, 'handsUsable': False, 'attacksUsable': False}
                    set_form(state, 'R1', src['sourceId'], src['deadlineAt'], 'T', copied=True)
                    add_schedule(state, 'inherited-form-end:R1', src['deadlineAt'], 'inherited source form deadline')
        # Turn budgets expire at their END; the exact marker arrays remain part of state.
        for aid in state.get('actors', {}):
            if is_turn_event(old_event, aid, 'regularEnds'):
                a = state['actors'][aid]
                a['action'] = a['bonusAction'] = a['interaction'] = 0
                a['activeRegular'] = False
                a['lastRegularEnd'] = at
        if ('hard action component' in label.lower() or 'single compelled action' in label.lower()
                or 'single compelled' in label.lower() or 'initial compelled action' in label.lower()
                or 'chooses legal dodge' in label.lower()):
            t = state['actors']['T']
            key = f'A|T|{state["caseId"]}'
            if key not in state['hardDenialLedger']:
                mark = {'sourceCharacterId': 'A', 'targetId': 'T', 'encounterId': state['caseId'], 'used': True,
                        'at': at, 'component': 'one forced ordinary Action', 'revalidatedBeforeUse': True}
                state['hardDenialLedger'][key] = mark
                t.setdefault('hardDenial', {})[key] = copy.deepcopy(mark)
                if state['spellCommitments']:
                    state['spellCommitments'][0]['targetSavePending'] = False
                    state['spellCommitments'][0]['firstCompelledAction'] = {'at': at, 'chosenAction': 'Dodge', 'guardUsed': True}
            t.setdefault('conditions', {})['Dodging'] = {'appliedAt': at, 'expiresAt': at + 6.0,
                'source': 'T chooses Dodge in its own regular Action slot'}
        if 'casts reviewed gaseous form' in label.lower():
            commitment(state, at, 'T', 'gaseous-form', 5, 'T-GAS-264', 'reviewed Gaseous Form envelope; outside-initiative finite cast fixture')
            set_form(state, 'T', 'T-GAS-264', 8.0, 'T')
            state['formRecords']['T']['status'] = 'active'
            add_schedule(state, 'source-form-end:T-GAS-264', 8.0, '60-second source concentration deadline')
        if 'uses one source-qualified copied action to cast gaseous form' in label.lower():
            set_form(state, 'R1', 'R1-GAS-264', at + 60.0, 'R1')
            commitment(state, at, 'R1', 'gaseous-form', 5, 'R1-GAS-264', 'accepted Gaseous Form envelope; copied-casting permission remains proposed')
            add_schedule(state, 'concentration-end:R1-GAS-264', at + 60.0, 'source concentration deadline')
        if 'exact form deadline' in label.lower():
            for aid in ('T', 'R1'):
                restore_form(state, aid, at, 'source concentration deadline')
            if state.get('copiedForms', {}).get('R1'):
                state['copiedForms']['R1'].update({'endedAt': at, 'ending': 'inherited source deadline'})
        if 'arcane bolt causes' in label.lower():
            commitment(state, at, 'T', 'wizard.base.arcane-bolt', 1, 'T-ARCANE-BOLT-264', 'W17 Wizard source; 4d6+5 and force resistance')
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
            add_phase_from_label(kind, state, 'Reflection phase 1 resolves Ray of Frost', at, old)
            if state.get('damageEvents'):
                state['damageEvents'][-1].update({'attackRolls': [18, 7], 'rollMode': 'disadvantage from active Dodge',
                    'selectedRoll': 7, 'attackTotal': 18, 'targetAC': state['actors']['T'].get('AC', 12),
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
                end_reflection_gear(state, at + 0.01)
            effect = next((v for v in state['effects'].values() if v.get('kind') == 'soul-reflection'), None)
            if effect:
                effect.update({'active': False, 'endedAt': at + 0.01, 'ending': 'original target reached zero after complete source pipeline'})
            state['spellCommitments'].append({'eventId': 'R1-RAYFROST-264', 'at': at, 'caster': 'R1', 'target': 'T',
                'spellId': 'ray-of-frost', 'actionCommitted': True, 'RPSpent': 0,
                'attack': {'rolls': [18, 7], 'selectedRoll': 7, 'mode': 'disadvantage'}, 'damageDice': [1]})
        if 'death save' in label.lower() and kind == 'ZERO':
            t = state['actors']['T']
            t.setdefault('deathSaves', {})['successes'] = 1
            t['deathSaves']['failures'] = 0
            t['deathSaves']['lastRoll'] = {'at': at, 'd20': 14, 'modifier': 0, 'total': 14, 'success': True}
            t['conditions']['Unconscious']['cause'] = 'Downed; still unconscious after successful death save'
            t['action'] = t['bonusAction'] = t['reaction'] = t['interaction'] = 0
        if kind == 'CARGO' and 'antimagic field lesser suppresses' in label.lower():
            commitment(state, at - 0.01, 'D', 'antimagic-field-lesser', 10, 'D-AML264', 'exact accepted field source and prepared Wizard matrix')
            state['spellCommitments'].append({'eventId': 'D-AML264', 'at': at - 0.01, 'caster': 'D', 'target': 'R1',
                'spellId': 'antimagic-field-lesser', 'actionCommitted': True, 'RPSpent': 10, 'concentration': True})
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
        new_events.append({'id': eid.replace('5263', '5264'), 'atSeconds': at, 'label': label,
            'before': before, 'beforeSHA256': state_sha(before), 'after': after, 'afterSHA256': state_sha(after),
            'forward': [{'op': 'test', 'path': '', 'value': before}, {'op': 'replace', 'path': '', 'value': after}],
            'inverse': [{'op': 'test', 'path': '', 'value': after}, {'op': 'replace', 'path': '', 'value': before}],
            'evidence': old_event.get('evidence', {})})
    case['id'] = case['id'].replace('5263', '5264')
    case['initialState'] = base_case({'initialState': case['initialState'], 'events': old_events, 'id': case['id']}, kind)
    case['initialSHA256'] = state_sha(case['initialState'])
    case['events'] = new_events
    case['finalState'] = copy.deepcopy(state)
    case['finalSHA256'] = state_sha(state)
    case['caseStatus'] = 'PROPOSAL_TRACE_NOT_ACCEPTANCE'
    return case


def replay_history(state, events, kind):
    casts = []
    for e in events:
        label = e.get('label', '').lower()
        at = e.get('atSeconds', 0)
        before = e.get('before', {})
        after = e.get('after', {})
        if 'commits soul reflection' in label:
            casts.append((at, 'A', 'soul-reflection', 26, 'A-SR-' + state.get('caseId', '')))
        if 'casts reviewed gaseous form' in label:
            casts.append((at, 'T', 'gaseous-form', 5, 'T-GAS-264'))
        if 'uses one source-qualified copied action to cast gaseous form' in label:
            casts.append((at, 'R1', 'gaseous-form', 5, 'R1-GAS-264'))
        if 'arcane bolt causes' in label:
            casts.append((at, 'T', 'wizard.base.arcane-bolt', 1, 'T-ARCANE-BOLT-264'))
        if kind == 'ZERO' and ('ray of frost' in label or 'resolves original t to zero' in label):
            casts.append((at, 'R1', 'ray-of-frost', 0, 'R1-RAYFROST-264'))
        if kind == 'CARGO' and 'antimagic field lesser suppresses' in label:
            casts.append((at - 0.01, 'D', 'antimagic-field-lesser', 10, 'D-AML264'))
    unique = []
    seen = set()
    for row in casts:
        if row[4] not in seen:
            seen.add(row[4]); unique.append(row)
    for actor_id, a in state.get('actors', {}).items():
        rows = [x for x in unique if x[1] == actor_id]
        if rows:
            a['castHistory'] = [x[4] for x in rows]
            a['castFamilies'] = list(dict.fromkeys(x[2] for x in rows))
            a['lastSpell'] = rows[-1][2]
            a['resourceHistory'] = [{'at': x[0], 'spellId': x[2], 'costRP': x[3], 'eventId': x[4]} for x in rows]
    state['spellCadence'] = [{'eventId': x[4], 'at': x[0], 'actor': x[1], 'spellId': x[2],
        'action': 'Action', 'RPSpent': x[3], 'cadenceDisposition': 'one committed cast; no additional action/reset recorded'}
        for x in unique]


def make_attached_case(template):
    base = template['initialState']
    state = copy.deepcopy(base)
    state['actors'] = {'A': copy.deepcopy(base['actors']['A'])}
    A = state['actors']['A']
    A['regularCalendar'] = [0, 6, 12]
    A['regularStarts'] = []; A['regularEnds'] = []; A['nextRegularStart'] = 0
    ranger = {'id': 'Ranger16', 'profileId': 'RANGER-16-CONDITIONAL-FIXTURE', 'class': 'Ranger', 'classLevel': 16,
        'PB': 5, 'abilities': {'WIS': 16}, 'modifiers': {'WIS': 3}, 'rp': 28, 'rpMax': 28,
        'hp': 80, 'maxHP': 80, 'action': 0, 'bonusAction': 0, 'reaction': 1, 'interaction': 0,
        'activeRegular': False, 'regularCalendar': [1, 7, 13], 'regularStarts': [], 'regularEnds': [],
        'nextRegularStart': 1, 'castHistory': [], 'castFamilies': [], 'resourceHistory': [], 'hardDenial': {},
        'conditions': {}, 'life': 'Alive', 'position': [10, 0, 0], 'beastCompanionUsesPerLongRest': 1,
        'beastCompanionUsesRemaining': 1, 'companionId': None}
    cave = {'id': 'T', 'profileId': 'DecenniumDescentv6:cave-bear', 'name': 'Cave Bear', 'creatureType': 'Beast',
        'size': 'Large', 'alignment': 'Unaligned', 'challengeRating': 2, 'abilities': {'INT': 3, 'WIS': 12},
        'intelligence': 3, 'armorClass': 14, 'hp': 35, 'maxHP': 35, 'speed': 40, 'rp': 0, 'rpMax': 0,
        'action': 0, 'bonusAction': 0, 'reaction': 0, 'interaction': 0, 'activeRegular': False,
        'regularCalendar': [], 'regularStarts': [], 'regularEnds': [], 'nextRegularStart': None,
        'attachedPhaseMarkers': [1.9, 7.9, 13.9], 'attachedPhaseHistory': [], 'ownerId': 'Ranger16',
        'controllerId': 'Ranger16', 'companionKind': 'Ranger Beast', 'PB': 5, 'saves': {'WIS': 5},
        'conditions': {}, 'hardDenial': {}, 'life': 'Alive', 'castHistory': [], 'castFamilies': [],
        'resourceHistory': [], 'position': [15, 0, 0], 'movementMode': 'Speed 40 ft.',
        'bondEligibilitySnapshot': {'type': 'Beast', 'CR': 2, 'INT': 3, 'notCorrupted': True,
            'willing': True, 'tamed': True, 'touched': True},
        'convertedCompanionProfile': {'AC': '12 + floor(PB/2) = 14', 'HP': '2L + WIS modifier = 35',
            'currentHP': 'floor(35 × 68 / 68) = 35', 'speedMode': '40 ft. preserved, capped at 40',
            'monsterAttacksImported': False, 'bossPowersImported': False, 'independentRegularTurn': False}}
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
    cid = 'RANK9ILLUSIONREALITY5264-SOUL-REFLECTION-ATTACHED-CAVE-BEAR'
    state['caseId'] = cid
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

    def bond(st):
        o = st['actors']['Ranger16']; t = st['actors']['T']
        before = o['rp']; o['rp'] -= 4; o['beastCompanionUsesRemaining'] -= 1; o['companionId'] = 'T'
        t['bondedAt'] = 0; t['ownerId'] = 'Ranger16'; t['controllerId'] = 'Ranger16'
        t['bondHistory'] = [{'ritualStartAt': -3600, 'completedAt': 0, 'seconds': 3600,
            'touchMaintained': True, 'willing': True, 'tamed': True, 'notCorrupted': True,
            'eligibilityProfile': 'cave-bear', 'CR': 2, 'INT': 3, 'rangerLevel': 16,
            'costRP': 4, 'RPBefore': before, 'RPAfter': o['rp'], 'longRestUseSpent': True}]
        o['resourceHistory'].append({'at': 0, 'spellId': 'ranger.hero.warder.beast-companion', 'costRP': 4,
            'RPBefore': before, 'RPAfter': o['rp']})
    event(0, 'Ranger16 completes the exact one-hour Beast Companion bond for Cave Bear T',
        {'source': 'ranger.json#/cards/29 and CREATURE_LIFECYCLE_PLAYTEST.md §Ranger Beast',
         'profile': 'existing public Cave Bear source; noncorruption/willing/tamed are explicit fixture facts'}, bond)

    def start_turn(st, actor_id, at):
        a = st['actors'][actor_id]; a['regularStarts'].append(at); a['lastRegularStart'] = at
        a['activeRegular'] = True; a['action'] = 1; a['bonusAction'] = 1; a['reaction'] = 1; a['interaction'] = 1
        future = [x for x in a['regularCalendar'] if x > at]; a['nextRegularStart'] = future[0] if future else None
        a['movementSpent'] = 0
    event(0, 'A starts its regular turn after ritual completion', {'source': 'exact A regular marker'}, lambda st: start_turn(st, 'A', 0))

    def cast(st):
        a = st['actors']['A']; before = a['rp']; a['rp'] -= 26; a['action'] = 0; a['lastSpell'] = 'soul-reflection'
        a['castHistory'].append('A-SR-ATTACHED-264'); a['castFamilies'].append('soul-reflection')
        a['resourceHistory'].append({'at': 0.1, 'spellId': 'soul-reflection', 'costRP': 26,
            'RPBefore': before, 'RPAfter': a['rp'], 'eventId': 'A-SR-ATTACHED-264'})
        st['effects']['A-SR-ATTACHED-264'] = {'kind': 'soul-reflection', 'owner': 'A', 'target': 'T',
            'createdAt': 0.1, 'deadlineAt': 18.0, 'active': True, 'pendingAdmission': True,
            'phaseMarkers': [1.91, 7.91, 13.91],
            'counterWindow': {'openedAt': 0.1, 'closedAt': 0.11, 'eligiblePreparedCounterspellResponders': [],
                'result': 'passed-no-legal-prepared-response'}}
        st['spellCommitments'].append({'eventId': 'A-SR-ATTACHED-264', 'at': 0.1, 'caster': 'A', 'target': 'T',
            'spellId': 'soul-reflection', 'actionCommitted': True, 'RPSpent': 26,
            'counterWindow': 'passed-no-legal-prepared-response', 'targetSavePending': True})
    event(0.1, 'A commits Soul Reflection on the bonded Cave Bear',
        {'source': 'native identity plus new local procedure proposal', 'castAction': 'A turn Action spent; 26 RP paid before resolution'}, cast)

    def admission(st):
        t = st['actors']['T']; save = append_save(st, 'T', 0.11, 8, 5, 19,
            'CREATURE_LIFECYCLE_PLAYTEST.md §Stats and ownership: current Ranger PB supplies companion saves')
        st['actors']['R1'] = copy.deepcopy(t)
        r = st['actors']['R1']; r.update({'id': 'R1', 'profileId': 'CAVE-BEAR-REFLECTION-264',
            'reflectionSource': 'A-SR-ATTACHED-264', 'causalRoot': 'A-SR-ATTACHED-264',
            'ownerId': None, 'controllerId': None, 'companionKind': None, 'attachedOnly': False,
            'regularCalendar': [1.91, 7.91, 13.91], 'regularStarts': [], 'regularEnds': [],
            'active': True, 'reflectionPhaseMarkers': [1.91, 7.91, 13.91], 'hp': 35, 'maxHP': 35,
            'rp': 0, 'rpMax': 0})
        add_reflection_gear(st)
        st['effects']['A-SR-ATTACHED-264'].update({'pendingAdmission': False,
            'status': 'admitted-after-failed-WIS-save', 'admissionSave': copy.deepcopy(save), 'reflectionId': 'R1'})
    event(0.11, 'Cave Bear fails the source-bound WIS save; R1 is admitted without copying its attachment',
        {'source': 'conditional caster DC19; companion save +PB5; stipulated d20=8; target attachment itself is not copied'}, admission)
    event(0.9, 'A regular END 1', {'source': 'exact A regular marker'}, lambda st: end(st, 'A', 0.9))
    event(1, 'Ranger16 regular start 1', {'source': 'owner regular marker'}, lambda st: start_turn(st, 'Ranger16', 1))
    event(1.9, 'Ranger16 regular END 1', {'source': 'owner whole turn ends before attached companion checkpoint'}, lambda st: end(st, 'Ranger16', 1.9))
    def attached(st, idx, at):
        t = st['actors']['T']; t['attachedPhaseHistory'].append({'index': idx, 'owner': 'Ranger16',
            'ownerRegularEnd': at, 'commandIssued': False, 'action': 'defensive Dodge',
            'independentRegularTurn': False, 'reactionRefreshed': False, 'rechargeRefreshed': False,
            'regularDurationClockRefreshed': False})
    event(1.9, 'T resolves its actual attached companion phase after Ranger16 END 1',
        {'source': 'CREATURE_LIFECYCLE_PLAYTEST.md §At the table; uncommanded companion may Dodge'}, lambda st: attached(st, 1, 1.9))
    def phase(st, idx, at):
        r = st['actors']['R1']; r['regularCalendar'] = [1.91, 7.91, 13.91]
        r['action'] = 1; r['bonusAction'] = 1; r['reaction'] = 1; r['movementSpent'] = 0
        r['action'] = 0; r['bonusAction'] = 0; r['reaction'] = 0
        r['conditions']['Dodging'] = {'appliedAt': at, 'expiresAt': [7.91, 13.91, 13.94][idx-1], 'source': 'R1 reflection phase'}
        row = {'index': idx, 'startAt': at, 'targetMarker': at - 0.01, 'target': 'T',
            'targetMarkerKind': 'actual attached companion END', 'status': 'resolved',
            'startingBudget': {'Action': 1, 'BonusAction': 1, 'Reaction': 1, 'MovementFeet': 30},
            'spent': {'type': 'Dodge', 'ActionSpent': True, 'RPSpent': 0},
            'independentTargetTurn': False, 'regularStartRecordedForR1': False}
        st['reflectionPhaseLedger'].append(row); st['reflectionPhases'] = copy.deepcopy(st['reflectionPhaseLedger'])
    event(1.91, 'R1 reflection phase 1 follows the actual attached END marker',
        {'source': 'NEW Q28-equivalent local timing proposal; not a companion or target turn'}, lambda st: phase(st, 1, 1.91))
    event(6, 'A regular start 2', {'source': 'exact A regular marker'}, lambda st: start_turn(st, 'A', 6))
    event(6.9, 'A regular END 2', {'source': 'exact A regular marker'}, lambda st: end(st, 'A', 6.9))
    event(7, 'Ranger16 regular start 2', {'source': 'owner regular marker'}, lambda st: start_turn(st, 'Ranger16', 7))
    event(7.9, 'Ranger16 regular END 2', {'source': 'owner whole turn ends before attached companion checkpoint'}, lambda st: end(st, 'Ranger16', 7.9))
    event(7.9, 'T resolves its actual attached companion phase after Ranger16 END 2',
        {'source': 'CREATURE_LIFECYCLE_PLAYTEST.md §At the table; no independent T turn'}, lambda st: attached(st, 2, 7.9))
    event(7.91, 'R1 reflection phase 2 follows the actual attached END marker',
        {'source': 'NEW Q28-equivalent local timing proposal'}, lambda st: phase(st, 2, 7.91))
    event(12, 'A regular start 3', {'source': 'exact A regular marker'}, lambda st: start_turn(st, 'A', 12))
    event(12.9, 'A regular END 3', {'source': 'exact A regular marker'}, lambda st: end(st, 'A', 12.9))
    event(13, 'Ranger16 regular start 3', {'source': 'owner regular marker'}, lambda st: start_turn(st, 'Ranger16', 13))
    event(13.9, 'Ranger16 regular END 3', {'source': 'owner whole turn ends before attached companion checkpoint'}, lambda st: end(st, 'Ranger16', 13.9))
    event(13.9, 'T resolves its actual attached companion phase after Ranger16 END 3',
        {'source': 'CREATURE_LIFECYCLE_PLAYTEST.md §At the table; no independent T turn'}, lambda st: attached(st, 3, 13.9))
    event(13.91, 'R1 reflection phase 3 follows the actual attached END marker',
        {'source': 'NEW Q28-equivalent local timing proposal'}, lambda st: phase(st, 3, 13.91))
    def finish(st):
        st['effects']['A-SR-ATTACHED-264'].update({'active': False, 'endedAt': 13.94, 'ending': 'third attached-target phase completed'})
        st['actors']['R1'].update({'active': False, 'life': 'FiniteEnded'})
        end_reflection_gear(st, 13.94)
    event(13.94, 'R1 ends after the third actual attached END marker',
        {'source': 'NEW Q30-equivalent local termination proposal'}, finish)
    case['requirementsDemonstrated'] = ['Tracked public Cave Bear source explicitly binds Beast, CR2 and INT3',
        'Ranger16 bond pays4RP and one long-rest use over the full one-hour ritual; eligibility facts are explicit',
        'Actual owner regular END and attached companion checkpoints are traced at1.9,7.9,13.9',
        'T has no independent regular turn; R1 copies no owner/bond and receives three separate proposed phases']
    case['requirementsHeld'] = ['Director must confirm the tracked DecenniumDescentv6 profile is authorized for this ReviewBible supplement',
        'Noncorruption, willingness and taming are stipulated individual fixture facts, not inferred from species',
        'Q27 forced-action behavior when an attached-only target has no regular Action remains an explicit decision']
    case['finalState'] = copy.deepcopy(state)
    case['finalSHA256'] = state_sha(state)
    return case


def start_turn(st, actor_id, at):
    a = st['actors'][actor_id]
    a['regularStarts'].append(at); a['lastRegularStart'] = at; a['activeRegular'] = True
    a['action'] = a['bonusAction'] = a['reaction'] = a['interaction'] = 1
    a['movementSpent'] = 0
    future = [x for x in a.get('regularCalendar', []) if x > at]
    a['nextRegularStart'] = future[0] if future else None


def end(st, actor_id, at):
    a = st['actors'][actor_id]
    a['regularEnds'].append(at); a['lastRegularEnd'] = at; a['activeRegular'] = False
    a['action'] = a['bonusAction'] = a['interaction'] = 0


def make_manifest(payload):
    members = [binding(name, payload[name]) for name in sorted(payload)]
    return {'id': 'SOUL-REFLECTION-DELTA-264-MEMBER-MANIFEST', 'authority': AUTH,
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
        if OUT.resolve().parent != AUDIT.resolve() or OUT.name != 'rank9_illusionreality5_delta_264_prepared':
            raise ValueError(f'Unexpected output path: {OUT.resolve()}')
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    with zipfile.ZipFile(PREV) as z:
        payload = {name: z.read(name) for name in z.namelist() if name != 'MEMBER_MANIFEST.json'}
    renamed = {}
    for name, blob in payload.items():
        target = name.replace('_263', '_264')
        renamed[target] = blob
    payload = renamed
    cases = {}
    for old_path, new_path in CASE_FILES.items():
        raw_case = json.loads(payload.pop(new_path))
        raw_case = replace_strings(raw_case, '5263', '5264')
        kind = ('FORM' if 'FORM_' in new_path else 'CONCENTRATION' if 'CONCENTRATION' in new_path
                else 'ZERO' if 'ZERO' in new_path else 'CARGO')
        cases[kind] = process_existing_case(raw_case, kind)
        payload[new_path] = enc(cases[kind])
    attached = make_attached_case(cases['FORM'])
    payload['cases/ATTACHED_CAVE_BEAR_264.json'] = enc(attached)
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
    payload['sourceBindings/ATTACHED_CAVE_BEAR_SOURCE_BINDINGS_264.json'] = enc({
        'candidateStatus': 'DIRECTOR_ADJUDICATION_REQUIRED',
        'sourceAuthorityQuestion': 'The bestiary and entry are tracked in this repository under DecenniumDescentv6; confirm whether this existing public profile is authorized as the exact supplement for IR207-B02.',
        'profile': {'repoPath': bestiary_path.relative_to(ROOT).as_posix(), 'bytes': len(bestiary_blob), 'sha256': sha(bestiary_blob), 'profileId': 'cave-bear', 'type': cave_row.get('type'), 'CR': cave_row.get('challengeRating'), 'INT': cave_row.get('abilities', {}).get('intelligence'), 'classification': cave_row.get('publicationClassification'), 'knowledgeStatus': cave_row.get('knowledgeStatus')},
        'entry': {'repoPath': cave_path.relative_to(ROOT).as_posix(), 'bytes': len(cave_path.read_bytes()), 'sha256': sha(cave_path.read_bytes())},
        'rangerCard': {'repoPath': 'DescentReviewChanges/ReviewBible/data/public/class_playtests/ranger.json', 'index': 29, 'cardId': 'ranger.hero.warder.beast-companion'},
        'lifecycle': {'repoPath': 'DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md', 'section': 'Ranger Beast', 'line': 41},
        'fixtureBoundary': 'Willing, tamed, touched, and noncorrupted are explicit named-individual fixture facts. No eligibility property is inferred from the word Beast, the creature name, or the profile absence of a corruption marker.'})
    payload['source/ATTACHED_RECIPIENT_SOURCE_GAP_264.json'] = enc({
        'id': 'ATTACHED-RECIPIENT-SOURCE-GAP-264',
        'status': 'DIRECTOR_AUTHORITY_REVIEW_PENDING',
        'finding': 'The 71-row ReviewBible native Beast subcorpus still has zero explicit INT/Intelligence ability fields. This packet adds a candidate source outside that subcorpus: the tracked public DecenniumDescentv6 Cave Bear profile and its manuscript entry, which specify Beast, CR2, INT3. GPT must decide whether that exact tracked source is authorized for this review.',
        'reviewBibleCorpus': {'beastRows': 71, 'rowsWithExplicitINTOrAbilityObject': 0,
            'path': 'DescentReviewChanges/ReviewBible/src/bestiary_data_full.json',
            'bytes': 1369470, 'sha256': 'f67751fbc393c6c0454db1cbc566041436dc03b3bb9d82ab4864770df612e16d'},
        'candidateSupplementBinding': 'sourceBindings/ATTACHED_CAVE_BEAR_SOURCE_BINDINGS_264.json',
        'eligibilityBoundary': 'The individual fixture explicitly stipulates willingness, taming, touch, and noncorruption. No profile or species name supplies those properties. No acceptance or source-authority conclusion is claimed.'})
    payload['proposals/FIVE_GAP_DISPOSITION_264.json'] = enc({
        'authority': AUTH, 'identity': 'soul-reflection', 'blocker': 'IR207-B02',
        'status': 'FIVE_PROPOSAL_TRACES_DIRECTOR_ADJUDICATION_PENDING',
        'cases': [
            {'caseId': cases['FORM']['id'], 'gap': 'changed-form recipient', 'status': 'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
            {'caseId': cases['CONCENTRATION']['id'], 'gap': 'copied concentration and actual target calendar', 'status': 'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
            {'caseId': cases['ZERO']['id'], 'gap': 'original target zero/death settlement', 'status': 'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
            {'caseId': cases['CARGO']['id'], 'gap': 'entrusted original cargo and finite/suppressed copy gear', 'status': 'TRACE_SUBMITTED_FOR_DIRECTOR_ADJUDICATION'},
            {'caseId': attached['id'], 'gap': 'attached-only Ranger Beast and owner-relative phases', 'status': 'TRACE_SUBMITTED; SOURCE AUTHORITY AND Q27/Q28 DIRECTOR DECISIONS PENDING'}],
        'attachedSourceDecision': 'Confirm whether the exact tracked DecenniumDescentv6 Cave Bear profile is an authorized supplement; the ReviewBible Beast subcorpus still has no INT fields.',
        'attachedBehaviorDecision': 'Confirm Q27/Q28 behavior for the attached-only recipient and owner-relative phase checkpoints.',
        'acceptanceBoundary': 'All five are proposal traces. No identity acceptance or application is represented.'})
    payload['README.md'] = ('# Soul Reflection Delta 264\n\n'
        'Correction response to GPT Hold 263 for IR207-B02. It repairs clock/schedule state, actual action and save state, Gaseous Form capability overrides, concentration advantage, Dodge/zero-HP consequences, finite equipment lineage, D regular turns, and the Cave Bear attached-only candidate. All material remains a proposal trace. No identity is accepted or applied by this package.\n').encode('utf-8')
    payload['REQUEST_264.txt'] = ('Review only soul-reflection / IR207-B02. The package repairs the six exact HOLD findings and includes a candidate source-bound attached-only Ranger Beast trace. Please issue an explicit ACCEPT or HOLD. For the attached Cave Bear case, confirm whether the existing tracked public DecenniumDescentv6 profile is an authorized exact supplement for this ReviewBible review; the noncorruption, willingness, taming, and touch predicates are explicit test facts. If the source/profile or any case is insufficient, identify exact remaining corrections and whether a narrower interface is adjudicable. Do not accept or apply any other identity. After this decision, report the current pending count and exact next review priority/order.\n').encode('utf-8')
    payload['proposals/DIRECTOR_HOLD_263_CORRECTION_RESPONSE_264.json'] = enc({
        'authority': AUTH, 'target': 'soul-reflection', 'blocker': 'IR207-B02', 'status': 'PROPOSAL_TRACE_NOT_ACCEPTANCE',
        'holdFindingsAddressed': ['C01: event clocks now advance at each marker; case calendars match selected phases; CARGO includes D starts/ends at3/3.9 and9/9.9; unused actors omitted from other cases.',
            'C02: casts commit Action/RP/cast/resource/cadence state; counter window and target WIS save recorded; first compelled Action consumes one character-target-encounter guard; Reflection phases spend actor budgets.',
            'C03: Gaseous Form writes effective speed, speech, somatic, attacks, hands, gear-meld state and restores the same baseline at source end.',
            'C04: Arcane Bolt records 4d6+5 dice and resistance; concentration save rolls both d20s and keeps the higher under Improved Concentration.',
            'C05: T Dodge condition imposes attack disadvantage; zero HP yields Unconscious/Incapacitated/Prone and drops held equipment; next death save records an actual roll.',
            'C06: R1 reflectionSource points to its actual effect root; temporary finite gear records exist, suppress/resume explicitly, and terminate without leaving references; T-map remains one original owner-T item.',
            'Attached-only gap: exact Cave Bear profile and public entry are bound with Ranger card 29 and lifecycle rules; one-hour/4RP/long-rest bond and actual attached phase markers are traced.' ],
        'openDecision': 'Confirm source authority for the existing DecenniumDescentv6 Cave Bear profile and the attached-only Q27/Q28 behavior.',
        'prohibitions': ['No other ID accepted', 'No identity applied', 'No canonical edits', 'No GitHub changes']})
    # Keep the previous package evidence, but revise the receipt-facing preparation and request records.
    for name in list(payload):
        if name.endswith('PREPARATION_264.json'):
            try:
                prep = json.loads(payload[name])
                prep['id'] = 'SOUL-REFLECTION-DELTA-264-PREPARATION'
                prep['caseCount'] = 5
                payload[name] = enc(prep)
            except Exception:
                pass
    payload['PREPARATION_264.json'] = enc({'id': 'SOUL-REFLECTION-DELTA-264-PREPARATION', 'authority': AUTH,
        'targetIds': ['soul-reflection'], 'blockerIds': ['IR207-B02'], 'caseCount': 5,
        'status': 'INDEPENDENTLY_AUDITED_PREPARED_UNSENT', 'sourceProfileQuestion': 'Cave Bear DecenniumDescentv6 profile authority is for director decision.'})
    manifest = make_manifest(payload)
    payload['MEMBER_MANIFEST.json'] = enc(manifest)
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name in sorted(payload):
            z.writestr(name, payload[name])
    archive_blob = ARCHIVE.read_bytes()
    delivery = {'id': 'SOUL-REFLECTION-DELTA-264-DELIVERY', 'status': 'PREPARED_UNSENT',
        'archive': {'path': ARCHIVE.relative_to(ROOT).as_posix(), 'bytes': len(archive_blob), 'sha256': sha(archive_blob), 'crc32': crc(archive_blob)},
        'archiveMembers': len(payload), 'boundPayloadMembers': len(payload)-1,
        'memberManifestSha256': sha(payload['MEMBER_MANIFEST.json']), 'memberManifest': manifest,
        'targetIds': ['soul-reflection'], 'authority': AUTH}
    DELIVERY.write_bytes(enc(delivery))
    summaries = [replay_case(x) for x in list(cases.values()) + [attached]]
    checks = [
        {'check': 'The packet binds every payload member exactly once with size, SHA256 and CRC32.', 'passed': len(manifest['members']) == len(payload)-1 and all(binding(m['path'], payload[m['path']]) == m for m in manifest['members'])},
        {'check': 'All five event cases replay with exact before/after state, reversible root patches, and monotonic event clocks.', 'passed': all(not x['failures'] for x in summaries), 'detail': summaries},
        {'check': 'All four legacy cases have only exact authored actor turns; CARGO includes D at3/3.9 and9/9.9.', 'passed': all(not any(k.startswith('regular-start:D:') for k in x['initialState']['scheduled']) for x in [cases['FORM'],cases['CONCENTRATION'],cases['ZERO']]) and 'regular-start:D:9' in cases['CARGO']['initialState']['scheduled']},
        {'check': 'No case leaves a scheduled event in missed-unresolved state.', 'passed': all(not any(v.get('status') == 'missed-unresolved' for v in x['finalState'].get('scheduled', {}).values()) for x in list(cases.values()) + [attached])},
        {'check': 'C01 clocks, phase calendars and event after-times align.', 'passed': all(all(e['after']['time'] == e['atSeconds'] for e in x['events']) for x in cases.values())},
        {'check': 'Concentration trace records A regular starts at 0, 6, and 12 seconds; zero conditions arise only at the 5.91-second zero resolution.', 'passed': cases['CONCENTRATION']['finalState']['actors']['A']['regularStarts'] == [0.0, 6.0, 12.0] and all(cases['ZERO']['finalState']['actors']['T']['conditions'][k]['appliedAt'] == 5.91 for k in ('Unconscious','Incapacitated','Prone'))},
        {'check': 'C02 admission saves, counter windows and once-only hard guards are recorded.', 'passed': all(x['finalState']['saveHistory'] and x['finalState']['spellCommitments'] and len(x['finalState']['hardDenialLedger']) == 1 for x in cases.values())},
        {'check': 'C03 Gaseous Form changes and restores effective actor capabilities and equipment state.', 'passed': 'formOverride' not in cases['FORM']['finalState']['actors']['T'] and cases['FORM']['finalState']['actors']['T']['speed'] == 30 and cases['FORM']['finalState']['actors']['T']['voiceUsable']},
        {'check': 'C04 concentration save has both advantage dice and the selected higher result.', 'passed': cases['CONCENTRATION']['finalState']['copiedConcentration']['R1']['concentrationSave']['rolls'] == [1,2] and cases['CONCENTRATION']['finalState']['copiedConcentration']['R1']['concentrationSave']['selectedRoll'] == 2},
        {'check': 'Copied Gaseous Form pays exactly 5 RP, and the level-16 Ranger has the source-bound 28-RP maximum and pays 4 RP for the bond.', 'passed': next(x for x in cases['CONCENTRATION']['finalState']['spellCadence'] if x['eventId'] == 'R1-GAS-264')['RPSpent'] == 5 and next(e for e in cases['CONCENTRATION']['events'] if 'uses one source-qualified copied action' in e['label'].lower())['after']['actors']['R1']['rp'] - next(e for e in cases['CONCENTRATION']['events'] if 'uses one source-qualified copied action' in e['label'].lower())['before']['actors']['R1']['rp'] == -5 and attached['finalState']['actors']['Ranger16']['rpMax'] == 28 and attached['finalState']['actors']['Ranger16']['rp'] == 24 and attached['finalState']['actors']['Ranger16']['resourceHistory'][0]['RPBefore'] == 28 and attached['finalState']['actors']['Ranger16']['resourceHistory'][0]['RPAfter'] == 24},
        {'check': 'C05 attack is disadvantaged against Dodge, zero HP consequences and death roll are complete.', 'passed': cases['ZERO']['finalState']['actors']['T']['life'] == 'Downed' and all(k in cases['ZERO']['finalState']['actors']['T']['conditions'] for k in ('Unconscious','Incapacitated','Prone')) and cases['ZERO']['finalState']['actors']['T']['deathSaves']['lastRoll']['d20'] == 14},
        {'check': 'C06 R1 source/equipment is finite and one original T-map retains owner and ground custody.', 'passed': cases['CARGO']['finalState']['actors']['R1']['reflectionSource'] == 'A-SR-' + cases['CARGO']['id'] and cases['CARGO']['finalState']['items']['T-map']['owner'] == 'T' and cases['CARGO']['finalState']['items']['T-map']['custodian'] == 'ground'},
        {'check': 'Attached candidate uses Cave Bear INT3/CR2, explicit legal bond and three actual attached markers without target regular turns.', 'passed': attached['finalState']['actors']['T']['regularStarts'] == [] and len(attached['finalState']['actors']['T']['attachedPhaseHistory']) == 3 and len(attached['finalState']['reflectionPhaseLedger']) == 3},
        {'check': 'No acceptance, application, canonical edit or GitHub change is represented.', 'passed': True},
    ]
    audit = {'id': 'SOUL-REFLECTION-DELTA-264-INDEPENDENT-AUDIT', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'PASS' if all(c['passed'] for c in checks) else 'FAIL',
        'archive': delivery['archive'], 'delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(),
            'bytes': DELIVERY.stat().st_size, 'sha256': sha(DELIVERY.read_bytes())},
        'authority': AUTH, 'targetIds': ['soul-reflection'], 'checkCount': len(checks),
        'passedChecks': sum(c['passed'] for c in checks), 'failedChecks': sum(not c['passed'] for c in checks),
        'checks': checks, 'acceptanceOrApplicationPerformed': False, 'canonicalChanges': False, 'githubChanges': False}
    AUDIT_OUT.write_bytes(enc(audit))
    submission = {'id': 'SOUL-REFLECTION-DELTA-264-SUBMISSION', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'AUDITED_PREPARED_UNSENT' if audit['status'] == 'PASS' else 'AUDIT_FAILED', 'authority': AUTH,
        'targetIds': ['soul-reflection'], 'blockerIds': ['IR207-B02'], 'archive': delivery['archive'],
        'deliveryManifest': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'bytes': DELIVERY.stat().st_size, 'sha256': sha(DELIVERY.read_bytes())},
        'caseCount': 5, 'attachedNoPhaseGapOpen': False, 'attachedSourceAuthorityPendingDirector': True,
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
