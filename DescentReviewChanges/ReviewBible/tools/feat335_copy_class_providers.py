"""Source-bound Shaman/Mirrorsage credentials for the agreed feat-copy route.

Conditional ability, level, known-spell and Base-choice projections, not a full
character builder. Training, hero-path acquisition and campaign occurrences
remain explicit upstream premises. No Wizard identity or feat-only alias is
used to impersonate either class.
"""
from copy import deepcopy
from hashlib import sha256
import json
from feat335_copy_capture import CopyAcquisition
from feat335_copy_source_components import integer
from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_casting_credential_model import CastingCredentials


ABILITIES = {'Shaman': 'WIS', 'Mirrorsage': 'INT'}


class NativeCredentials(CastingCredentials):
    def __init__(self, sources, owner):
        super().__init__(sources, sum(owner.actor['classLevels'].values()))
        self.native_owner = owner
        self.native_routes = []

    def snapshot(self):
        return deepcopy({k: v for k, v in self.__dict__.items()
                         if k not in {'sources', 'native_owner'}})

    def qualifying(self):
        result = super().qualifying()
        if self.native_owner.native_retained():
            result.extend(deepcopy(self.native_routes))
        return result


class ClassCopyAcquisition(CopyAcquisition):
    def __init__(self, actor, classes, equipment, skills, ancestry, backgrounds,
                 contracts, supplements, sources):
        self.actor = deepcopy(actor)
        self.classes = classes; self.equipment = equipment; self.skills = skills
        self.ancestry = ancestry; self.backgrounds = backgrounds
        self.contracts = contracts; self.supplements = supplements; self.sources = sources
        self.first = actor['firstClass']; self.initializations = {}
        if self.first not in ABILITIES or actor['priorFeatChoices'] or set(actor['classLevels']) != {self.first}:
            raise ValueError('One actual Shaman/Mirrorsage class and unspent feat history required')
        level = integer(actor['classLevels'][self.first], 'attained class level', 1, 20)
        if actor['ancestry'] != 'human' or actor['variant'] != 'imperial-human':
            raise ValueError('This ability slice uses the actual Human/Imperial source')
        h = next(x for x in ancestry['ancestries'] if x['id'] == 'human')
        variant = next(x for x in h['variants'] if x['id'] == 'imperial-human')
        rolls = actor['abilityRolls']
        if set(rolls) != {'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'} or any(
                len(d) != 4 or any(type(n) is not int or not 1 <= n <= 6 for n in d) for d in rolls.values()):
            raise ValueError('Six actual four-d6/drop-lowest ability premises required')
        scores = {a: sum(d) - min(d) + variant['combinedAbilityBonuses'][a] for a, d in rolls.items()}
        if scores != actor['permanentScores']:
            raise ValueError('Ability snapshot differs from actual ancestry and rolls')
        self.training_projection = None
        self.pay = PaidChoices({n: c['asiClassLevels'] for n, c in classes.items()}, {},
            deepcopy(actor['classLevels']), scores, set(contracts) | {'proposal_spell_focus'})
        self.class_path = sources.root / classes[self.first]['classCandidatePath']
        raw = self.class_path.read_bytes()
        self.class_binding = {'file': classes[self.first]['classCandidatePath'],
                              'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}
        if self.class_binding['sha256'] != classes[self.first]['classCandidateSha256']:
            raise ValueError('Class source must match actual character-foundation binding')
        self.class_source = json.loads(raw)
        if classes[self.first]['weaveTier'] != 'hybrid' or classes[self.first]['rpByClassLevel'] != self.class_source['rpByClassLevel']:
            raise ValueError('Exact hybrid chassis and RP progression required')
        self.native_state = {'provider': self.first, 'classLevel': level,
                             'providerRetained': True, 'heroPath': actor['heroPath']}
        self.casting = NativeCredentials(sources, self)
        self.base_kit = None

    def verify_class_source(self):
        raw = self.class_path.read_bytes()
        if len(raw) != self.class_binding['bytes'] or sha256(raw).hexdigest() != self.class_binding['sha256']:
            raise ValueError('Frozen class source changed; requalify before use')

    def native_retained(self):
        grant = self.casting.grants.get(self.first + '/class-engine')
        if not grant or grant['acquiredAt'] > self.casting.moment or any(
                key in grant and grant[key] <= self.casting.moment for key in ['removedAt', 'expiresAt']):
            return False
        state = self.native_state
        return (state['provider'] == self.first and state['providerRetained'] is True
                and state['classLevel'] == self.pay.current_classes[self.first]
                and not (self.first == 'Shaman' and state['heroPath'] == 'Bloodcaller'))

    def advance(self, level):
        super().advance(level)
        self.native_state['classLevel'] = level

    def bind_class_state(self, state):
        if state['provider'] != self.first or state['classLevel'] != self.pay.current_classes[self.first]:
            raise ValueError('Canonical class state must match attained class identity/level')
        if state['abilityScore'] != self.pay.scores[ABILITIES[self.first]]:
            raise ValueError('Canonical class ability must match permanent acquisition history')
        if type(state['providerRetained']) is not bool or not state['heroPath']:
            raise ValueError('Explicit current retained provider and path required')
        self.native_state = state

    def native_known(self, entries, event):
        """One supplied lawful known subset, with each real learning level."""
        self.verify_class_source()
        gid = self.first + '/class-engine'
        if gid in self.casting.grants or not event or not entries:
            raise ValueError('One nonempty actual native repertoire projection required')
        rows = []; ids = set(); level = self.pay.current_classes[self.first]
        for entry in entries:
            if set(entry) != {'spellId', 'atClassLevel', 'event'} or not entry['event'] or entry['spellId'] in ids:
                raise ValueError('Distinct source-linked native learning entries required')
            at_level = integer(entry['atClassLevel'], 'learning class level', 1, level)
            route = self.sources.ordinary(entry['spellId'], self.first)
            if route['minimumClassLevel'] > at_level or route['rank'] > self.class_source['maxSpellRankByClassLevel'][at_level - 1]:
                raise ValueError('Native learning exceeds actual placement/rank ceiling')
            rows.append({**route, 'grantId': gid, 'kind': 'native-known',
                         'ability': ABILITIES[self.first], 'learning': deepcopy(entry)})
            ids.add(entry['spellId'])
        for n in range(1, level + 1):
            attained = [r for r in rows if r['learning']['atClassLevel'] <= n]
            if sum(r['rank'] == 0 for r in attained) > (2 if n < 10 else 3) or sum(r['rank'] > 0 for r in attained) > 2 + n // 2:
                raise ValueError('Known subset exceeds source hybrid acquisition capacity')
        self.casting.grants[gid] = {'source': 'actual-' + self.first + '-level-and-known-repertoire-projection',
            'acquiredAt': self.casting.moment, 'event': event, 'classBinding': deepcopy(self.class_binding)}
        self.casting.native_routes = rows

    def select_base(self, ids, event):
        self.verify_class_source()
        schedule = self.class_source['schedule'][0]
        cards = {c['id']: c for c in self.class_source['cards']}
        if self.base_kit is not None or self.pay.current_classes[self.first] != 1 or not event:
            raise ValueError('One actual first-level Base selection opportunity required')
        if len(ids) != schedule['choose'] or len(set(ids)) != len(ids) or any(i not in cards for i in ids):
            raise ValueError('Exact distinct Base choices required')
        chosen = [cards[i] for i in ids]
        if any(c['acquisition'] != 'selection' or c['band'] not in schedule['bands'] or c['minimumClassLevel'] > 1 for c in chosen) or sum(c['sourceKind'] == 'active' for c in chosen) < schedule['minimumActives']:
            raise ValueError('Actual Base selection predicates/minimum actives required')
        self.base_kit = {'event': event, 'atClassLevel': 1, 'choices': list(ids),
                         'classBinding': deepcopy(self.class_binding)}

    def provider(self, grant_id, rank):
        if grant_id != self.first + '/class-engine':
            return super().provider(grant_id, rank)
        integer(rank, 'requested copy rank', 0, 9)
        self.verify_class_source()
        if not self.native_retained() or not self.casting.native_routes:
            raise ValueError('Actually retained native casting engine/repertoire required')
        maximum = self.class_source['maxSpellRankByClassLevel'][self.pay.current_classes[self.first] - 1]
        if rank > maximum:
            raise ValueError('Copy exceeds actual native learnable-rank ceiling')
        return {'grantId': grant_id, 'ability': ABILITIES[self.first],
                'maximumLearnableRank': maximum, 'rank': rank, 'grantsOriginalSpell': False,
                'classBinding': deepcopy(self.class_binding)}

    def snapshot(self):
        return {**super().snapshot(), 'nativeState': deepcopy(self.native_state),
                'baseKit': deepcopy(self.base_kit), 'classBinding': deepcopy(self.class_binding),
                'scope': 'Conditional ability/repertoire/paid-feat/Base-selection slice; no full training or hero acquisition.'}
