"""Paid copy-feat acquisition and finite source-bound capture histories.

Wizard and the explicit feat-only Eldritch Blast rank-zero routes are modeled.
This does not implement a general class repertoire, campaign scheduler, actual
perception, or paid copy release; those are separate integration requirements.
"""
from copy import deepcopy
from feat_exact_01_composite_casting_model import CompositeCastingHistory
from feat335_copy_source_components import integer


class CopyAcquisition(CompositeCastingHistory):
    def acquire_copy(self, sid, level):
        if sid not in {'eldritch_echo', 'mimicry', 'arcane_adaptation'}:
            raise ValueError('Outside copy acquisition scope')
        record = self.pay.commit(sid, self.first + ':' + str(level),
                                 prerequisites_met=self.prerequisite(sid))
        if sid == 'eldritch_echo':
            gid = sid + '/' + record['opportunity']
            self.casting.grants[gid] = {'source': 'actual-paid-Eldritch-Echo',
                'acquiredAt': self.casting.moment, 'payment': deepcopy(record)}
            self.casting.routes.append({**self.sources.blast(), 'grantId': gid,
                'kind': 'personal-feat', 'ability': 'CHA'})
        return record

    def provider(self, grant_id, rank):
        integer(rank, 'requested copy rank', 0, 9)
        g = self.casting.grants.get(grant_id)
        if not g or g['acquiredAt'] > self.casting.moment or any(
                key in g and g[key] <= self.casting.moment for key in ['removedAt', 'expiresAt']):
            raise ValueError('Actually retained personal casting grant required')
        if grant_id == 'Wizard/class-engine':
            level = self.pay.current_classes.get('Wizard', 0)
            if not level or not self.casting.wizard_level or g['source'] != 'actual-Wizard-level-and-repertoire-projection':
                raise ValueError('Actual acquired Wizard engine and attained class level required')
            maximum = self.sources.wizard['maxSpellRankByClassLevel'][level - 1]
            ability = 'INT'
        elif g['source'] in {'actual-paid-Forbidden-Pact', 'actual-paid-Eldritch-Echo'}:
            routes = [r for r in self.casting.qualifying() if r['grantId'] == grant_id]
            if not routes or any(r['spellId'] != self.sources.blast()['spellId'] or r['rank'] != 0 for r in routes):
                raise ValueError('Actual feat-only Eldritch Blast route required')
            maximum = 0; ability = 'CHA'
        else:
            raise ValueError('Other learnable-rank engines are outside this finite provider slice')
        if rank > maximum:
            raise ValueError('Copy rank exceeds this actual provider learnable ceiling')
        return {'grantId': grant_id, 'ability': ability, 'maximumLearnableRank': maximum,
                'rank': rank, 'grantsOriginalSpell': False}


class CopyCaptures:
    def __init__(self, acquired, witnesses):
        self.acquired = acquired; self.witnesses = witnesses
        self.pending = None; self.adapted = {}; self.resistances = {}
        self.events = {}; self.rests = set(); self.regular_turns = {}; self.extra_turns = set(); self.regular_ordinal = 0
        self.current_turn = None; self.current_kind = None; self.current_round = None
        self.uses = {sid: 1 for sid in ['eldritch_echo', 'mimicry', 'arcane_adaptation'] if acquired.pay.has(sid)}
        self.reactions = 1; self.epoch = 0

    def snapshot(self):
        return deepcopy({k: v for k, v in self.__dict__.items() if k not in {'acquired', 'witnesses'}})

    def operative(self, sid):
        return self.acquired.pay.has(sid) and sid not in self.acquired.pay.suppressed

    def start_regular(self, turn, ordinal, numbered_round, *, actual_new_regular_start):
        if actual_new_regular_start is not True or turn in self.regular_turns or not turn or self.current_turn is not None:
            raise ValueError('Actual new regular-turn start identity required')
        if integer(ordinal, 'regular ordinal', 1) != self.regular_ordinal + 1:
            raise ValueError('Consecutive actual regular starts required in this finite timeline')
        integer(numbered_round, 'numbered round', 1)
        self.regular_ordinal = ordinal; self.regular_turns[turn] = {'ordinal': ordinal, 'ended': False}
        self.current_turn = turn; self.current_kind = 'regular'; self.current_round = numbered_round
        # The ordinary Reaction refresh is an explicit actual regular-start premise.
        self.reactions = 1
        for permission in self.adapted.values():
            if ordinal >= permission['expiresAtRegularStart']:
                permission['active'] = False

    def start_extra(self, turn, numbered_round, *, actual_extra_turn):
        if actual_extra_turn is not True or not turn or turn in self.regular_turns or turn in self.extra_turns or self.current_turn is not None:
            raise ValueError('Actual distinct extra turn required')
        integer(numbered_round, 'numbered round', 1)
        self.extra_turns.add(turn)
        self.current_turn = turn; self.current_kind = 'extra'; self.current_round = numbered_round

    def end_extra(self, turn, *, actual_extra_end):
        if actual_extra_end is not True or self.current_kind != 'extra' or self.current_turn != turn:
            raise ValueError('Actual currently pending extra-turn end required')
        self.current_turn = None; self.current_kind = None

    def end_regular(self, turn, *, actual_regular_end):
        record = self.regular_turns.get(turn)
        if actual_regular_end is not True or not record or record['ended'] or self.current_turn != turn or self.current_kind != 'regular':
            raise ValueError('Actual currently pending regular-turn end required')
        record['ended'] = True
        if self.pending and self.pending['feat'] == 'eldritch_echo' and self.pending['releaseRegularOrdinal'] == record['ordinal']:
            self.events[self.pending['captureEvent']]['recordStatus'] = 'expired-next-regular-end'
            self.pending = None
        for resistance in self.resistances.values():
            if record['ordinal'] >= resistance['expiresAtRegularEnd']:
                resistance['active'] = False
        self.current_turn = None; self.current_kind = None

    def capture(self, event, sid, source_event, profile, grant_id, geometry, *, replace=False, adapt=False):
        if not event or event in self.events:
            raise ValueError('New capture event identity required')
        if sid not in {'eldritch_echo', 'mimicry'} or not self.operative(sid) or self.uses.get(sid, 0) < 1:
            raise ValueError('Actually paid feat and its unspent capture use required')
        if type(replace) is not bool or type(adapt) is not bool:
            raise ValueError('Explicit replacement/adaptation decision required')
        fields = {'actualCaptureWindow', 'conscious', 'actualFeatAvailable', 'sourceCreatureDistance',
            'resolvedComponentDistance', 'sourcePerceived', 'effectPerceived', 'lineOfEffect',
            'usedAgainstOwner', 'sourceLawfulRange', 'actualReactionLegal'}
        if not isinstance(geometry, dict) or set(geometry) != fields:
            raise ValueError('Exact actual capture geometry and timing premises required')
        for field in fields - {'sourceCreatureDistance', 'resolvedComponentDistance'}:
            if type(geometry[field]) is not bool:
                raise ValueError('Actual Boolean capture premise required')
        for field in ['sourceCreatureDistance', 'resolvedComponentDistance']:
            integer(geometry[field], 'actual observed distance')
        if not all(geometry[k] for k in ['actualCaptureWindow', 'conscious', 'actualFeatAvailable', 'sourcePerceived', 'effectPerceived']):
            raise ValueError('Actual current perceived capture window and available feat required')
        if sid == 'eldritch_echo':
            if geometry['sourceCreatureDistance'] > 60 or not geometry['lineOfEffect'] or not geometry['actualReactionLegal'] or self.reactions < 1:
                raise ValueError('Echo needs actual within60ft line of effect and legal available Reaction')
        else:
            targeted = geometry['usedAgainstOwner'] and geometry['sourceLawfulRange']
            nearby = geometry['resolvedComponentDistance'] <= 30 and geometry['lineOfEffect']
            if not (targeted or nearby):
                raise ValueError('Mimicry needs lawful actual targeting or within30ft line-of-effect resolution')
        selected = self.witnesses.select(source_event, profile)
        provider = self.acquired.provider(grant_id, selected['copyRank'])
        if self.pending and not replace:
            raise ValueError('Explicitly replace and lose the existing one pending record')
        if adapt and (not self.operative('arcane_adaptation') or self.uses.get('arcane_adaptation', 0) < 1):
            raise ValueError('Paid Arcane Adaptation and unspent temporary-knowledge use required')

        record = {'captureEvent': event, 'feat': sid, 'component': selected, 'provider': provider,
            'capturedRestEpoch': self.epoch, 'capturedRegularOrdinal': self.regular_ordinal,
            'releaseRegularOrdinal': self.regular_ordinal + 1 if sid == 'eldritch_echo' else None,
            'recordStatus': 'pending', 'captureIsCast': False, 'grantsOriginalSpell': False,
            'geometry': deepcopy(geometry), 'scope': 'Capture only; full paid release remains required.'}
        if self.pending:
            self.events[self.pending['captureEvent']]['recordStatus'] = 'replaced-without-refund'
        self.uses[sid] -= 1
        if sid == 'eldritch_echo':self.reactions -= 1
        self.events[event] = deepcopy(record); self.pending = record
        if self.operative('arcane_adaptation') and 'damageType' in selected:
            self.resistances[event] = {'type': selected['damageType'], 'active': True,
                'expiresAtRegularEnd': self.regular_ordinal + 1, 'retroactive': False}
        if adapt:
            self.uses['arcane_adaptation'] -= 1
            self.adapted[event] = {'component': deepcopy(selected), 'provider': deepcopy(provider),
                'active': True, 'expiresAtRegularStart': self.regular_ordinal + 2,
                'newReleaseAllowance': False, 'grantsOriginalSpell': False}
        return deepcopy(record)

    def rest(self, event, *, kind, beneficial):
        if kind not in {'SR', 'LR'} or type(beneficial) is not bool:
            raise ValueError('Actual supported rest completion required')
        if not beneficial or event in self.rests:return False
        if not isinstance(event, str) or not event:
            raise ValueError('Actual rest identity required')
        self.rests.add(event);self.epoch += 1
        self.uses = {sid: 1 for sid in self.uses}
        if self.pending and self.pending['feat'] == 'mimicry':
            self.events[self.pending['captureEvent']]['recordStatus'] = 'expired-beneficial-rest'
            self.pending = None
        return True
