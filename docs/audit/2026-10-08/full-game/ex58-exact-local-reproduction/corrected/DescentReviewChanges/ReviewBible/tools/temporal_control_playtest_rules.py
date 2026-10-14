"""Temporal control/pulse integration under construction, not full Time Loop.

This first bridge lets the existing pulse helper spend the canonical RP, RC and
Bonus Action. It owns no second resource pool and changes no source timing.
Remaining source policies require their actual notebook conference and review.
"""
from device_lifecycle_playtest_rules import Wallet
from healing_pulse_playtest_rules import PulseSeries, PROFILES
from spell_playtest_rules import integer
from temporal_playtest_rules import Scheduler, TemporalKernel, ident, require, shape


class CanonicalPulseWallet:
    """Duck-typed spend interface used by the reviewed PulseSeries helper.

Bind once to a known host actor. Every spend verifies that its scene, scheduler,
registry and Wallet aliases still designate those same canonical objects. RC
comes from Scheduler.rc, the encounter resource explicitly restored by the
kernel; RP/used-history remain on the real Wallet. There is no local balance.
"""
    def __init__(self, kernel, actor):
        require(isinstance(kernel, TemporalKernel), 'Canonical temporal host required')
        ident(actor)
        require(actor in kernel.wallets and actor in kernel.lives, 'Canonical pulse actor required')
        self.kernel = kernel
        self.actor = actor
        self._scheduler = kernel.scheduler
        self._registry = kernel.wallets
        self._wallet = kernel.wallets[actor]
        self._validate()

    def _validate(self):
        require(self.kernel.scheduler is self._scheduler and self.kernel.wallets is self._registry
                and self._registry.get(self.actor) is self._wallet,
                'Canonical pulse binding changed')
        require(self.actor in self.kernel.lives, 'Canonical pulse actor disappeared')
        require(len({id(w) for w in self._registry.values()}) == len(self._registry),
                'Pulse actors cannot share one Wallet')
        shape(self._scheduler, Scheduler)
        shape(self._wallet, Wallet)
        integer(self._wallet.rp, 'canonical RP', 0)
        require(type(self._wallet.bonus_action) is bool, 'Canonical Bonus Action must be boolean')
        require(type(self._scheduler.rc) is dict, 'Canonical RC registry required')

    @property
    def rp(self):
        self._validate()
        return self._wallet.rp

    @property
    def rc(self):
        self._validate()
        value = self._scheduler.rc.get(self.actor, 0)
        return integer(value, 'canonical RC', 0)

    @property
    def bonus_action(self):
        self._validate()
        return self._wallet.bonus_action

    def spend(self, amount, currency='RP', *, bonus_action=False):
        self._validate()
        integer(amount, 'pulse cost', 0)
        require(currency in ('RP', 'RC'), 'Unknown pulse currency')
        require(type(bonus_action) is bool, 'Explicit Bonus Action cost required')
        balance = self.rp if currency == 'RP' else self.rc
        require(balance >= amount, 'Required pulse resource unavailable')
        require(not bonus_action or self._wallet.bonus_action, 'Required pulse Bonus Action unavailable')
        # All checks precede mutation. Reference host holds its scene/event lock.
        if currency == 'RP':
            self._wallet.rp -= amount
        elif amount:
            self._scheduler.rc[self.actor] = balance - amount
        if bonus_action:
            self._wallet.bonus_action = False


# Zero-based pulse indexes. These keys identify conserved source opportunities,
# not new resource pools. Source acquisition/parent eligibility stay with host.
INDEPENDENT_OUTPUTS = {
    'transcendent-meditation': ('monk.hero.enlightened-master.transcendent-meditation',1,'Ki'),
    'sacred-chant': ('cleric.base.sacred-chant',2,'Conviction'),
}


class ConservedPulseOutputs:
    """Guard actual resolved outputs through the existing PulseSeries method.

This is the resolution boundary only. It does not restore series, validate their
parent concentration, or authorize a due marker. The eventual temporal source
adapter must provide those. It retains one canonical series object per identity
and never grants the same instance/index resource twice, even across iterations.

Returned allowances must be applied once in the host's same atomic event to its
real resource holder with the printed cap. This guard owns no Ki or Conviction.
Missed/expired clock events still require the source-clock adapter; no method
here fabricates an occurrence from an old committed state or a supplied receipt.
"""
    def __init__(self, kernel):
        require(isinstance(kernel, TemporalKernel),'Canonical temporal host required')
        self.kernel = kernel
        self.series = {}
        self.consumed = set()
        self.events = {}

    def register(self, series, owner, source_id):
        require(type(series) is PulseSeries, 'Canonical PulseSeries required')
        require(series.profile_name in INDEPENDENT_OUTPUTS,'Unsupported independent-output source')
        expected = INDEPENDENT_OUTPUTS[series.profile_name][0]
        require(source_id == expected,'Independent-output source/profile mismatch')
        ident(series.instance_id)
        require(series.instance_id not in self.series,'Canonical pulse identity already registered')
        CanonicalPulseWallet(self.kernel,owner)
        self.series[series.instance_id] = (series,owner,source_id,series.profile_name)

    def _binding(self, instance):
        require(instance in self.series,'Unknown independent-output instance')
        series,owner,source_id,profile = self.series[instance]
        require(type(series) is PulseSeries and series.instance_id == instance
                and series.profile_name == profile and series.profile == PROFILES[profile]
                and source_id == INDEPENDENT_OUTPUTS[profile][0],
                'Independent-output canonical binding changed')
        return series,owner,profile

    def resolve(self, instance, index, now, targets, *, event_id, round_number,
                real_encounter, regular=True, upkeep_legal=True,
                whole_effect_suppressed=False):
        ident(event_id)
        require(event_id not in self.events,'Independent-output event replay')
        require(type(real_encounter) is bool and type(whole_effect_suppressed) is bool,
                'Explicit encounter and suppression state required')
        series,owner,profile = self._binding(instance)
        wallet = CanonicalPulseWallet(self.kernel,owner)
        # This call actually resolves a pending opportunity; reading a historical
        # series state or passing a copied result is not sufficient.
        result = series.resolve(index,now,targets,wallet,round_number=round_number,
            regular=regular,upkeep_legal=upkeep_legal,
            whole_effect_suppressed=whole_effect_suppressed)
        _,output_index,resource = INDEPENDENT_OUTPUTS[profile]
        key = (instance,index,resource)
        allowance = 0
        if index == output_index:
            first = key not in self.consumed
            self.consumed.add(key)  # Suppressed/capped occurrences never bank.
            allowance = int(first and not whole_effect_suppressed
                            and (profile != 'sacred-chant' or real_encounter))
        # Replace the old helper's unguarded Ki flag rather than returning two
        # independently usable authorizations for the same resource component.
        result['independentKi'] = allowance if resource == 'Ki' else 0
        result['independentConviction'] = allowance if resource == 'Conviction' else 0
        result['resourceOwner'] = owner
        result['occurrenceId'] = event_id
        result['iteration'] = self.kernel.scheduler.iteration
        self.events[event_id] = {'instance':instance,'index':index,
            'iteration':self.kernel.scheduler.iteration,'resource':resource,
            'allowance':allowance,'wholeSuppressed':whole_effect_suppressed}
        return result
