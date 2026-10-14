"""Current Flora follow-through: Verdant depends on active body, not its actions.

The original descendant and186-check report remain immutable. Their tested
Verdant bodies were all capable; that evidence never covered incapacity.
"""
from feat335_flora_source_followthrough import FloraSourceFollowthrough as EarlierFlora


class FloraSourceFollowthrough(EarlierFlora):
    def verdant_spell_bonus(self, route, *, actual_legal_cast, copied=False):
        # Plant inability to act is not an ending. Actual suppression of this
        # Flora magic is still an explicit fixture fact with its stated scope.
        active = self.operative and any(p['active'] and self.now < p['deadline']
            and not p['suppressed'] for p in self.plants.values())
        return int(actual_legal_cast and not copied and active
            and self.acquired.pay.has('verdant_bond')
            and 'verdant_bond' not in self.acquired.pay.suppressed
            and route in self.acquired.casting.qualifying()
            and route.get('sourceClass') in {'Druid', 'Ranger', 'Shaman'})
