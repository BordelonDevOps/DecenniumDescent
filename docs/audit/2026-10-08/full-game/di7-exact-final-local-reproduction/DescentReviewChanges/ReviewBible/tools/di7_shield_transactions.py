"""Paid Premonition Shield plus a bounded occurrence/prevention interface.

The ward and ordinary Fate Coin casts execute their source-bound acquisition,
payment and counter windows in FateTransactions. Incoming weapon/spell schedules,
retarget eligibility and transfer ownership remain explicit conditional upstream
premises. This is not a full attack, spell-damage or class-feature scheduler.
"""
from copy import deepcopy
from dataclasses import asdict
from di7_fate_transactions import FateTransactions
from redirection_playtest_rules import DamageRoot, AttackRetarget


def serial(value):
    if isinstance(value, dict): return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (set, frozenset)): return sorted(value)
    if isinstance(value, (list, tuple)): return [serial(v) for v in value]
    return value


class ShieldTransactions(FateTransactions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wards = {}; self.current_wards = {}; self.occurrences = {}; self.origin_keys = set()
        self.ward_events = []; self.packet_results = []; self.attack_results = []

    def snapshot(self):
        return {**super().snapshot(), 'wards': deepcopy(self.wards), 'currentWards': dict(self.current_wards),
            'occurrences': deepcopy(self.occurrences), 'originKeys': [list(x) for x in sorted(self.origin_keys)],
            'wardEvents': deepcopy(self.ward_events), 'packetResults': deepcopy(self.packet_results),
            'attackResults': deepcopy(self.attack_results)}

    def end_ward(self, cast_id, reason):
        ward = self.wards[cast_id]
        if ward['ended']: return
        ward.update(ended=True, endedAt=self.now, endedReason=reason)
        if self.current_wards.get(ward['target']) == cast_id: del self.current_wards[ward['target']]

    def _live(self, cast_id):
        ward = self.wards[cast_id]
        if not ward['ended']:
            target = self.world['entities'].get(ward['target'])
            if not target or target.get('dead') or target.get('destroyed') or target.get('removed'):
                self.end_ward(cast_id, 'recipient-ended-or-removed')
            elif self.now >= ward['deadline']:
                self.end_ward(cast_id, 'deadline')
                ward['endedAt'] = ward['deadline']
        return not ward['ended'] and not ward['suppressed']

    def advance(self, now):
        super().advance(now)
        for cast_id in self.wards: self._live(cast_id)

    def suppress_ward(self, cast_id, suppressed):
        if type(suppressed) is not bool: raise ValueError('Explicit suppression state required')
        self._live(cast_id)
        self.wards[cast_id]['suppressed'] = suppressed
        self.ward_events.append({'kind': 'suppression', 'ward': cast_id, 'at': self.now, 'suppressed': suppressed})

    def resolve_shield(self, cast_id):
        cast = self.casts[cast_id]
        if cast['spellId'] != 'premonition-shield': raise ValueError('Actual Shield cast required')
        receipt = self.take_payload_resolution(cast_id)
        if receipt['status'] != 'ready-for-payload': return None
        target = cast['request']['target']
        # A failed effect does not replace an existing ward. Recheck the actual
        # target predicate at this effect boundary, retaining all paid costs.
        try:
            _, op, _, _ = self.sources.spell('premonition-shield', cast['provider'])
            self._target(cast['actor'], 'premonition-shield', cast['request'], op)
            if any(self.world['entities'][target].get(k) for k in ['dead', 'destroyed', 'removed']):
                raise ValueError('Recipient no longer exists as a living target')
        except ValueError as error:
            cast.update(status='failed-payload-no-refund', failure=str(error)); return None
        old = self.current_wards.get(target)
        if old: self.end_ward(old, 'successful-same-family-replacement')
        ward = {'castId': cast_id, 'caster': cast['actor'], 'target': target, 'remaining': 2,
            'startedAt': self.now, 'deadline': self.now + 60, 'suppressed': False, 'ended': False,
            'claims': [], 'secondOccurrence': None, 'sourceBinding': deepcopy(cast['sourceBinding'])}
        self.wards[cast_id] = ward; self.current_wards[target] = cast_id
        cast.update(status='resolved', resolvedAt=self.now, castingCompletedAt=self.now, attachedWard=cast_id)
        return deepcopy(ward)

    def register_occurrence(self, receipt):
        """Register an immutable, explicitly conditional real upstream schedule.

        The origin/occasion key prevents relabeling a packet as a new occurrence.
        A genuinely later tick needs a distinct actual schedule fact. A source
        fact here is a premise, not evidence that an arbitrary spell was cast.
        """
        r = deepcopy(receipt); oid = r['id']; kind = r['kind']
        if kind not in {'nonspell-attack', 'spell-immediate', 'spell-scheduled'}:
            raise ValueError('Passive query/nonattack nonspell event is not an occurrence')
        if not r.get('sourceFact') or not r.get('originId') or not r.get('occasionId'):
            raise ValueError('Actual source and scheduled occasion premises required')
        if kind in {'nonspell-attack', 'spell-immediate'} and r['occasionId'] != 'immediate':
            raise ValueError('Immediate attack/cast cannot acquire a second renamed occasion')
        if not r.get('components') or len({x['id'] for x in r['components']}) != len(r['components']):
            raise ValueError('Unique fixed component schedule required')
        key = (r['originId'], r['occasionId'])
        if oid in self.occurrences or key in self.origin_keys: raise ValueError('Actual occurrence already registered')
        r.update(finished=False, claims={}, noClaimAtFirst={}, completedComponents=[], registeredAt=self.now)
        self.occurrences[oid] = r; self.origin_keys.add(key)
        return oid

    def _component(self, oid, component_id):
        occurrence = self.occurrences[oid]
        if occurrence['finished']: raise ValueError('Occurrence already finished')
        found = [x for x in occurrence['components'] if x['id'] == component_id]
        if len(found) != 1: raise ValueError('Not an actual component of this occurrence')
        if component_id in occurrence['completedComponents']: raise ValueError('Component already completed')
        return occurrence, found[0]

    def admit(self, oid, component_id, target, *, positive_pre_share=False):
        occurrence, component = self._component(oid, component_id)
        allowed = component['preShareTargets'] if positive_pre_share else component['directTargets']
        if target not in allowed: raise ValueError('Actual final recipient/source-qualified share required')
        if target in occurrence['claims']:
            wid = occurrence['claims'][target]
            return wid if self._live(wid) else None
        if target in occurrence['noClaimAtFirst']:
            # An unreviewed late-first-admission seam is rejected rather than
            # inventing a rule for a ward suppressed at the first component.
            wid = self.current_wards.get(target)
            if wid and self._live(wid) and self.wards[wid]['remaining']:
                raise ValueError('Late first admission after initially unavailable ward needs source clarification')
            return None
        wid = self.current_wards.get(target)
        if not occurrence['actualResolution'] or not wid or not self._live(wid) or not self.wards[wid]['remaining']:
            occurrence['noClaimAtFirst'][target] = self.now
            return None
        ward = self.wards[wid]; ward['remaining'] -= 1; ward['claims'].append(oid)
        if ward['remaining'] == 0: ward['secondOccurrence'] = oid
        occurrence['claims'][target] = wid
        self.ward_events.append({'kind': 'automatic-use', 'ward': wid, 'occurrence': oid,
            'target': target, 'at': self.now, 'remaining': ward['remaining']})
        return wid

    def complete_component(self, oid, component_id):
        occurrence, _ = self._component(oid, component_id)
        occurrence['completedComponents'].append(component_id)

    def finish_occurrence(self, oid):
        occurrence = self.occurrences[oid]
        if occurrence['finished'] or set(occurrence['completedComponents']) != {x['id'] for x in occurrence['components']}:
            raise ValueError('Finish each actual component exactly once first')
        occurrence.update(finished=True, finishedAt=self.now)
        for wid in occurrence['claims'].values():
            if self.wards[wid]['secondOccurrence'] == oid: self.end_ward(wid, 'second-occurrence-completed')

    def resolve_packet(self, oid, component_id, root, branch_id, life, *, defenses=None, life_options=None):
        occurrence, component = self._component(oid, component_id)
        if root.root_id != component['rootId']: raise ValueError('Separate source-bound damage root required')
        branch = root.pending(branch_id); before = asdict(branch); wid = None
        if branch.transferred and branch.stage == 'sealed':
            if 'noSecondMitigation' not in branch.flags: raise ValueError('Missing source transfer restriction')
            # These branches expressly bypass both consumption and prevention.
        else:
            if branch.stage != 'raw': raise ValueError('Exactly one ordinary defense stage required')
            if branch.transferred:
                if branch.amount > 0: wid = self.admit(oid, component_id, branch.target, positive_pre_share=True)
            else:
                if branch.target not in occurrence['claims'] and branch.target not in occurrence['noClaimAtFirst']:
                    raise ValueError('Direct automatic admission must precede hit/save consequences')
                wid = occurrence['claims'].get(branch.target)
            root.defend(branch_id, **(defenses or {}))
        after_defenses = root.branch(branch_id).amount; prevented = 0
        if wid and self._live(wid): prevented = root.prevent(branch_id, after_defenses, wid)
        after, event = root.resolve_living(branch_id, life, now_seconds=self.now, **(life_options or {}))
        self.packet_results.append({'occurrence': oid, 'component': component_id, 'root': root.root_id,
            'beforeBranch': serial(before), 'afterDefenses': after_defenses, 'prevented': prevented,
            'afterBranch': serial(asdict(root.branch(branch_id))), 'lifeBefore': asdict(life),
            'lifeAfter': asdict(after), 'event': serial(event)})
        return after, event

    def weapon_attack(self, attack_id, intended, *, natural, modifier, armor_class, amount,
                      life, guardian=None, source_fact, defenses=None, life_options=None):
        """One conditional legal weapon attack; actual roll/retarget/ward/life.

        Source legality and any Guardian Reaction/use are supplied upstream, not
        granted by this method. The already rolled natural die is retained.
        """
        attack = AttackRetarget(attack_id, intended)
        if guardian: attack.retarget(guardian)
        target = attack.current_target
        self.register_occurrence({'id': attack_id, 'kind': 'nonspell-attack', 'originId': attack_id,
            'occasionId': 'immediate', 'sourceFact': source_fact, 'actualResolution': True,
            'components': [{'id': 'hit', 'rootId': attack_id + '/root', 'directTargets': [target], 'preShareTargets': []}]})
        self.admit(attack_id, 'hit', target)
        outcome = attack.resolve(natural, modifier, armor_class)
        root = DamageRoot(attack_id + '/root', target, amount if outcome['hit'] else 0, 'physical',
            attack_hit=outcome['hit'], critical=outcome['critical'])
        after, event = self.resolve_packet(attack_id, 'hit', root, root.original_id, life,
            defenses=defenses, life_options=life_options)
        self.attack_results.append({'natural': natural, 'intended': intended, 'final': target, 'outcome': outcome})
        self.complete_component(attack_id, 'hit'); self.finish_occurrence(attack_id)
        return after, event, outcome

    def resolve_fate_coin(self, cast_id):
        cast = self.casts[cast_id]
        if cast['spellId'] != 'fate-coin' or cast['status'] != 'pending' or not self.stack or self.stack[-1] != cast_id:
            raise ValueError('Actual surviving Fate Coin cast required')
        _, op, _, _ = self.sources.spell('fate-coin', cast['provider'])
        try:
            body = self.actors[cast['actor']]['body']
            if not body['conscious'] or not body['canAct'] or body['ordinarySpellProhibited']:
                raise ValueError('Caster cannot resolve the effect')
            self._target(cast['actor'], 'fate-coin', cast['request'], op)
        except ValueError:
            return super().resolve_fate_coin(cast_id)
        target = cast['request']['target']; oid = 'coin-occurrence/' + cast_id
        self.register_occurrence({'id': oid, 'kind': 'spell-immediate', 'originId': cast_id,
            'occasionId': 'immediate', 'sourceFact': {'executedPaidCast': cast_id, 'binding': cast['sourceBinding']},
            'actualResolution': True, 'components': [{'id': 'coin', 'rootId': None, 'directTargets': [target], 'preShareTargets': []}]})
        self.admit(oid, 'coin', target)
        result = super().resolve_fate_coin(cast_id)
        self.complete_component(oid, 'coin'); self.finish_occurrence(oid)
        return result
