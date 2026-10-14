"""FW05 finite shared-owner initialization, not a casting/death/rest engine.

Source-qualified paid acquisitions are real within each synthetic character
history. Prior spending and cast/death/body journals are explicitly conditional
fixture inputs, not authenticated campaign events. Both grants retain one blast
route and identity; historical paid source records remain distinct.
"""
from copy import deepcopy
from feat_exact_01_casting_selections import CastingSelections

BLAST = 'feat-supplement.eldritch-blast'
SHARED_BLAST = BLAST+'/shared-owner'


class SharedAcquisitionStates(CastingSelections):
    def _validate_soul_pool(self):
        if 'sharedSoulCharges' not in self.initializations:
            return
        pool = self.initializations['sharedSoulCharges']
        if (not isinstance(pool, dict) or type(pool.get('maximum')) is not int or pool['maximum'] != 3
                or type(pool.get('current')) is not int or not 0 <= pool['current'] <= 3
                or not isinstance(pool.get('evaluatedDeathEvents'), list)
                or not isinstance(pool.get('bodyEpochEntitlements'), list)):
            raise ValueError('A valid existing shared Soul Charge pool and retained journals are required')
        if not (self.pay.has('lifeleech') or self.pay.has('soul_cage')):
            raise ValueError('Existing shared pool needs its actual prior paid source in this history')

    def acquire_soul_source(self, sid, level, choice=None):
        if sid not in {'lifeleech', 'soul_cage'}:
            raise ValueError('Outside the two actual shared Soul Charge sources')
        self._validate_soul_pool()
        if sid == 'soul_cage':
            return self.acquire_casting_selection(sid, level, choice)
        # Parent validates the real casting credential, absent choice and payment.
        grant = self.acquire_parent(sid, level, choice)
        self.initializations.setdefault('sharedSoulCharges', {
            'maximum': 3, 'current': 0, 'evaluatedDeathEvents': [], 'bodyEpochEntitlements': []})
        return grant

    def _preflight_blast(self):
        profile = self.sources.blast()
        if (profile['spellId'] != BLAST or profile['rank'] != 0 or 'school' in profile
                or profile['completeProfile']['castingAbility'] !=
                'CHA; both feat grants share this one source ability/identity, not two selectable histories.'):
            raise ValueError('Exact current shared Eldritch Blast source required')
        if SHARED_BLAST in self.casting.grants and any(k in self.casting.grants[SHARED_BLAST] for k in ['removedAt', 'expiresAt']):
            raise ValueError('Individual source-removal/reacquisition is outside this retained-source witness')
        for route in self.casting.routes:
            if route['spellId'] == BLAST and (route.get('completeProfile') != profile['completeProfile']
                    or route.get('ability') != 'CHA' or route.get('rank') != 0 or 'school' in route):
                raise ValueError('Prior blast must be the same exact ability/profile, not an invented alternate')
        return profile

    def _join_blast(self, profile):
        sources = [deepcopy(x) for x in self.pay.grants if x['identity'] in {'forbidden_pact', 'eldritch_echo'}]
        if SHARED_BLAST not in self.casting.grants:
            self.casting.grants[SHARED_BLAST] = {'source': 'actual-paid-shared-feat-cantrip',
                'acquiredAt': self.casting.moment, 'spellId': BLAST, 'ability': 'CHA'}
        self.casting.grants[SHARED_BLAST]['paidSources'] = sources
        # Retain the original distinct payment/grant journals, but expose one route.
        self.casting.routes[:] = [r for r in self.casting.routes if r['spellId'] != BLAST]
        self.casting.routes.append({**deepcopy(profile), 'grantId': SHARED_BLAST,
                                   'kind': 'personal-feat', 'ability': 'CHA', 'entitlement': 'feat-cantrip'})

    def acquire_blast_source(self, sid, level, choice=None):
        if sid not in {'forbidden_pact', 'eldritch_echo'}:
            raise ValueError('Outside the two actual shared blast sources')
        profile = self._preflight_blast()
        if sid == 'forbidden_pact':
            grant = self.acquire_casting_selection(sid, level, choice)
        else:
            if choice is not None:
                raise ValueError('Eldritch Echo has no permanent acquisition menu')
            grant = self.pay.commit(sid, self.first+':'+str(level), prerequisites_met=self.prerequisite(sid))
            self.initializations[sid] = {'captureUses': {'maximum': 1, 'current': 1,
                'recovery': 'beneficial-owner-SR-or-LR'}}
            self.initializations.setdefault('pendingFeatCopy', None)
            self.casting.grants[sid+'/'+grant['opportunity']] = {
                'source': 'actual-paid-feat-complete-controlling-procedure',
                'acquiredAt': self.casting.moment, 'payment': deepcopy(grant)}
        self._join_blast(profile)
        return grant
