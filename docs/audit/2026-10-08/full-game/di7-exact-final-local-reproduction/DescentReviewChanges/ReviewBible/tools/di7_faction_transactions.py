"""Paid Faction Omniscience and source-qualified conditional institutional feeds.

This executes the feed, not institutional actions or native protection grants.
Membership, organizational continuity and activity participation are explicit
Director-established hypothetical facts, distinct from a badge/enemy/string flag.
"""
from copy import deepcopy
import math
from di7_fate_transactions import FateTransactions
from di7_vision_transactions import ConditionalInformation


class FactionTransactions(FateTransactions):
    def __init__(self, *args, dossier, institutions, activities, **kwargs):
        super().__init__(*args, **kwargs)
        self.information = ConditionalInformation(dossier)
        self.institutions = deepcopy(institutions); self.activities = deepcopy(activities)
        self.feeds = {}; self.notices = {}; self.activity_events = []; self.last_activity_key = None
        for iid, institution in self.institutions.items():
            if institution['id'] != iid or not institution.get('continuityAuthority'):
                raise ValueError('Actual institutional identity and continuity premises required')
        for aid, activity in self.activities.items():
            if aid != activity['id'] or not activity.get('worldAuthorityVersion') or not activity.get('authorityEvent'):
                raise ValueError('Actual activity identity/version/event required')

    def snapshot(self):
        return {**super().snapshot(), 'institutions': deepcopy(self.institutions), 'activities': deepcopy(self.activities),
            'feeds': deepcopy(self.feeds), 'notices': deepcopy(self.notices), 'activityEvents': deepcopy(self.activity_events),
            'lastActivityKey': list(self.last_activity_key) if self.last_activity_key else None,
            'privateInformationDossier': deepcopy(self.information.data)}

    def _eligible_reference(self, cast):
        target = self.world['entities'][cast['request']['target']]
        fid = target.get('membershipFacts', {}).get(cast['request']['faction'])
        actual_fact = self.information.data['facts'].get(fid) if fid else None
        actual = actual_fact['publicFields'].get('value') if actual_fact and actual_fact['establishedAt'] <= self.now else None
        if not isinstance(actual, dict) or actual.get('factionId') != cast['request']['faction'] or actual.get('current') is not True:
            return False
        projected = self.information.project(fid, now=self.now) if fid else None
        value = projected.get('value') if projected else None
        return isinstance(value, dict) and value.get('factionId') == cast['request']['faction'] and value.get('current') is True

    def resolve_faction(self, cast_id):
        cast = self.casts[cast_id]
        if cast['spellId'] != 'faction-omniscience': raise ValueError('Actual pending paid Faction Omniscience required')
        receipt = self.take_payload_resolution(cast_id)
        if receipt['status'] != 'ready-for-payload': return None
        faction = cast['request']['faction']; institution = self.institutions.get(faction)
        if not institution or not institution['exists'] or not self._eligible_reference(cast):
            cast.update(status='resolved-no-feed', resolvedAt=self.now, publicResult='No usable institutional reading.', refund=0)
            return None
        feed = {'castId': cast_id, 'actor': cast['actor'], 'institution': faction, 'reference': cast['request']['target'],
            'startedAt': self.now, 'deadline': self.now + 60, 'status': 'active', 'suppressed': False,
            'receiving': True, 'publicKeys': {}, 'nextPublicKey': 1, 'lastRegister': None}
        self.feeds[cast_id] = feed
        cast.update(status='resolved', resolvedAt=self.now, castingCompletedAt=self.now, feedId=cast_id)
        self._publish(feed, 'initial-register'); return deepcopy(feed)

    def _receiving(self, feed):
        if feed['status'] != 'active': return False
        aid = feed['actor']; a = self.actors[aid]; body = a['body']; entity = self.world['entities'].get(aid)
        reason = None
        if self.now >= feed['deadline']: reason = 'expiry'
        elif not entity or entity.get('dead') or entity.get('destroyed') or entity.get('removed'): reason = 'caster-death-or-removal'
        elif not self.institutions[feed['institution']]['exists']: reason = 'original-institution-ceased'
        if reason:
            feed.update(status='ended', endReason=reason, endedAt=feed['deadline'] if reason == 'expiry' else self.now, receiving=False)
            return False
        return body['conscious'] and body['canAct'] and not feed['suppressed']

    def _register(self, feed):
        faction = feed['institution']; entries = []
        for aid, activity in self.activities.items():
            if not activity['startsAt'] <= self.now < activity['endsAt']: continue
            participation = activity['institutionalParticipation'].get(faction)
            if not participation or not participation['actualCausalAuthority'] or participation['basis'] not in {'office', 'resources', 'orders', 'coordinated-institutional-task'}:
                continue
            existence = self.information.project(participation['existenceFact'], now=self.now)
            if not existence or existence.get('value') is not True: continue
            fields = {}
            for name in ['objective', 'participantsAndRoles', 'location', 'stage', 'immediateActivity']:
                fid = participation['fieldFacts'].get(name)
                projected = self.information.project(fid, now=self.now) if fid else None
                value = projected.get('value') if projected else None
                fields[name] = 'Indeterminate' if value is None else value
            if aid not in feed['publicKeys']:
                feed['publicKeys'][aid] = 'activity-' + str(feed['nextPublicKey']); feed['nextPublicKey'] += 1
            entries.append({'reference': feed['publicKeys'][aid], 'kind': participation['readableKind'], **fields})
        # Grouping keeps every readable record; it imposes no count ceiling and
        # does not disclose internal ordering gaps or counts of hidden records.
        groups = {}
        for entry in entries: groups.setdefault(entry['kind'], []).append(entry)
        return {'institution': faction, 'groups': groups,
            'scope': 'Readable current institutional register; undefined or protected information is not certified absent.'}

    def _publish(self, feed, kind):
        if not self._receiving(feed): return
        register = self._register(feed)
        if kind in {'initial-register', 'resumed-current-register'} or register != feed['lastRegister']:
            self.notices.setdefault(feed['actor'], []).append({'feedCastId': feed['castId'], 'at': self.now, 'kind': kind, 'register': deepcopy(register)})
            feed['lastRegister'] = register

    def advance(self, now):
        if type(now) not in {int, float} or not math.isfinite(now) or now < self.now:
            raise ValueError('Ordered finite elapsed time required')
        boundaries = {now}
        for activity in self.activities.values():
            boundaries.update(x for x in [activity['startsAt'], activity['endsAt']] if self.now < x <= now)
        for protection in self.information.data['protections']:
            boundaries.update(x for x in [protection['activeFrom'], protection['activeUntil']] if self.now < x <= now)
        for feed in self.feeds.values():
            if self.now < feed['deadline'] <= now: boundaries.add(feed['deadline'])
        for boundary in sorted(boundaries):
            super().advance(boundary); self._refresh()

    def _refresh(self):
        for feed in self.feeds.values():
            was_receiving = feed['receiving']; receiving = self._receiving(feed)
            feed['receiving'] = receiving
            if receiving and not was_receiving: self._publish(feed, 'resumed-current-register')
            elif receiving: self._publish(feed, 'current-material-update')

    def receipt_state(self, cast_id, *, suppressed=None, conscious=None, can_act=None):
        feed = self.feeds[cast_id]; actor = self.actors[feed['actor']]
        for value in [suppressed, conscious, can_act]:
            if value is not None and type(value) is not bool: raise ValueError('Explicit actual receipt state required')
        if suppressed is not None: feed['suppressed'] = suppressed
        if conscious is not None: actor['body']['conscious'] = conscious
        if can_act is not None: actor['body']['canAct'] = can_act
        self.advance(self.now)

    def end_feed(self, cast_id, reason):
        feed = self.feeds[cast_id]
        if feed['status'] == 'active': feed.update(status='ended', endReason=reason, endedAt=self.now, receiving=False)

    def activity_event(self, event):
        event = deepcopy(event); at = event['at']
        if type(at) not in {int, float} or not math.isfinite(at) or at < self.now:
            raise ValueError('Actual ordered finite activity time required')
        if not event.get('id') or not event.get('authorityEvent') or event['id'] in [x['id'] for x in self.activity_events]:
            raise ValueError('Actual unique world event authority required')
        if type(event.get('phase')) is not int or event['phase'] < 0 or type(event.get('applicationSequence')) is not int or event['applicationSequence'] < 0:
            raise ValueError('Canonical phase and application sequence required')
        if type(event.get('applicationAt')) not in {int, float} or not math.isfinite(event['applicationAt']) or not 0 <= event['applicationAt'] <= at:
            raise ValueError('Actual source application time required')
        key = (at, event['phase'], event['applicationAt'], event['applicationSequence'], event['id'])
        if self.last_activity_key is not None and key <= self.last_activity_key:
            raise ValueError('Canonical activity events cannot be replayed or reordered')
        if event['kind'] == 'change-fact':
            fact = self.information.data['facts'][event['factId']]
            if fact['authorityVersion'] != event['expectedVersion'] or not event['newVersion']:
                raise ValueError('Actual fact version transition required')
        elif event['kind'] == 'end-activity':
            if event['activityId'] not in self.activities: raise ValueError('Actual existing activity required')
        elif event['kind'] == 'begin-activity':
            activity = event['activity']
            if activity['id'] in self.activities or activity['startsAt'] != at or not activity.get('authorityEvent') or not activity.get('worldAuthorityVersion'):
                raise ValueError('Actual new institutional activity required')
            for fid in event['newFacts']:
                if fid in self.information.data['facts']: raise ValueError('New facts must not overwrite unrelated evidence')
        else: raise ValueError('Unimplemented world event kind')
        self.advance(at)
        if event['kind'] == 'change-fact':
            fact.update(publicFields=deepcopy(event['newPublicFields']), authorityVersion=event['newVersion'],
                authorityEvent=event['authorityEvent'], establishedAt=at, actualTime=at)
        elif event['kind'] == 'end-activity': self.activities[event['activityId']]['endsAt'] = at
        else:
            self.activities[event['activity']['id']] = deepcopy(event['activity'])
            self.information.data['facts'].update(deepcopy(event['newFacts']))
        self.activity_events.append(event); self.last_activity_key = key
        for feed in self.feeds.values(): self._publish(feed, 'current-material-update')

    def public_notices(self, actor): return deepcopy(self.notices.get(actor, []))
