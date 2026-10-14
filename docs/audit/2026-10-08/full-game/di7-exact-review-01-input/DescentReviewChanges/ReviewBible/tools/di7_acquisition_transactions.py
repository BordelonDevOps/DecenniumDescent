"""Known-spell replacement over conditional completed-own-rest premises.

This applies the existing same-or-lower rule; it neither simulates resting nor
creates a class19 learning grant. Ordinary Wizard book rules stay separate.
"""
from copy import deepcopy
from di7_cast_transactions import DI7CastTransactions
from spell_playtest_rules import integer


def same_or_lower(old_rank, new_rank):
    integer(old_rank, 'known rank', 0, 9); integer(new_rank, 'replacement rank', 0, 9)
    return new_rank <= old_rank


class AcquisitionTransactions(DI7CastTransactions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.replacement_history = []

    def snapshot(self):
        return {**super().snapshot(), 'replacementHistory': deepcopy(self.replacement_history)}

    def replace_known(self, actor_id, old_sid, new_sid, rest):
        actor = self.actors[actor_id]; provider = actor['provider']
        if provider not in {'Cleric', 'Mirrorsage', 'Shaman'}:
            raise ValueError('This fallback does not replace the Wizard book rules')
        if rest.get('kind') != 'conditional-actually-completed-own-long-rest' or rest.get('actor') != actor_id or not rest.get('id'):
            raise ValueError('Explicit actual own completed-rest premise required')
        if type(rest.get('completedAt')) not in {int, float} or not 0 <= rest['completedAt'] <= self.now:
            raise ValueError('Rest completion must precede this replacement')
        if any(x['rest']['id'] == rest['id'] and x['actor'] == actor_id for x in self.replacement_history):
            raise ValueError('One replacement at the same completed own rest')
        old = actor['learned'].get(old_sid)
        if not old or new_sid in actor['learned']:
            raise ValueError('Replace an actually known spell with a distinct not-known selection')
        old_card, _, old_binding, _ = self.sources.spell(old_sid, provider)
        if old['sourceBinding'] != old_binding or old['rank'] != old_card['classAccess'][provider]['rank']:
            raise ValueError('Old repertoire source history no longer matches')
        card, _, binding, candidate = self.sources.spell(new_sid, provider); placement = card['classAccess'][provider]
        if not same_or_lower(old['rank'], placement['rank']):
            raise ValueError('Known-spell replacement cannot increase rank')
        if placement['minimumClassLevel'] > actor['classLevel'] or placement['rank'] > self.sources.classes[provider]['maxSpellRankByClassLevel'][actor['classLevel'] - 1]:
            raise ValueError('Replacement selection fails the current ordinary class/rank gate')
        history = {'actor': actor_id, 'rest': deepcopy(rest), 'oldCredential': deepcopy(old), 'newSpellId': new_sid,
            'classLevelAtReplacement': actor['classLevel'], 'sourceBinding': binding}
        credential = {**deepcopy(old), 'spellId': new_sid, 'sourceBinding': binding, 'rank': placement['rank'],
            'kind': 'same-or-lower-known-spell-replacement', 'candidateSimulationOnly': candidate,
            'replacementAtClassLevel': actor['classLevel'], 'replacementRestId': rest['id'],
            'originalLearningOpportunityRetained': old['event']}
        del actor['learned'][old_sid]; actor['learned'][new_sid] = credential
        self.replacement_history.append(history)
        return deepcopy(credential)
