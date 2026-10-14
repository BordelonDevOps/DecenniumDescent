"""FW08 descriptor adapter, not a combat engine or credential authenticator.

Callers supply genuine paid-acquisition and rest/clock/recipient identities from
their owning systems. This module cannot manufacture or authenticate those facts.
"""
from dataclasses import dataclass, field
from feat_exact_01_acquisition_models import FiniteFeatUse


@dataclass
class BoundAllowance:
    owner: str
    identity: str
    reset: str
    use: FiniteFeatUse
    last_spent_second: int | None = None
    seen_encounters: set = field(default_factory=set)

    @classmethod
    def initial(cls, owner, descriptor, pb):
        maximum = pb if descriptor['maximum'] == 'currentPB' else descriptor['maximum']
        if type(maximum) is not int or maximum < 1:
            raise ValueError('Positive finite maximum required')
        return cls(owner, descriptor['identity'], descriptor['recovery'], FiniteFeatUse(maximum, maximum))

    def spend(self, now=None):
        if self.reset == 'elapsed24h':
            if not self.use.operative:
                raise ValueError('Allowance is suppressed')
            if type(now) is not int or now < 0:
                raise ValueError('Actual monotonic elapsed second required')
            if self.last_spent_second is not None and now < self.last_spent_second + 86400:
                raise ValueError('24 elapsed hours have not passed')
            # Only the same single allowance becomes available; elapsed time is
            # not stock accumulation. A rest cannot take this path.
            self.use.current = 1
            self.use.spend()
            self.last_spent_second = now
        else:
            self.use.spend()

    def rest(self, owner, identity, kind, beneficial):
        if owner != self.owner or kind not in {'SR', 'LR'} or not beneficial:
            return False
        if self.reset not in {'SR_OR_LR', 'LR'}:
            return False
        if self.reset == 'LR' and kind != 'LR':
            return False
        # Identity excludes the SR/LR label: relabelling a completion cannot
        # make the same genuine rest complete twice.
        return self.use.rest((owner, identity), True)

    def enter_encounter(self, owner, identity):
        if self.reset != 'realEncounter' or owner != self.owner or identity in self.seen_encounters:
            return False
        self.seen_encounters.add(identity)
        self.use.current = self.use.maximum
        return True


@dataclass
class EpochClaims:
    """Finite identity algebra only. Epochs come from the existing actual clock.

    Keep prior epochs so reentry/replay cannot regain an entitlement. No call to
    this model changes initiative, ordinary Reactions, elapsed time or rests.
    """
    claims: set = field(default_factory=set)

    def claim(self, family, scope, epoch, maximum=1):
        if type(maximum) is not int or maximum < 1:
            raise ValueError('Positive maximum required')
        root = (family, tuple(scope), epoch)
        used = sum(1 for k in self.claims if k[:3] == root)
        if used >= maximum:
            return False
        self.claims.add((*root, used + 1))
        return True
