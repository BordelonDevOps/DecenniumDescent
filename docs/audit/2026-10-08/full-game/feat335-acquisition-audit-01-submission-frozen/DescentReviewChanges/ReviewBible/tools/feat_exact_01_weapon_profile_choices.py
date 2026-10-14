"""Paid permanent weapon choices and a bounded attack-modifier projection.

Actual equipment, action, target, range and body legality are supplied premises
of the modifier query. This does not create attacks or simulate damage.
"""
from copy import deepcopy
from feat_exact_01_half_feat_choices import HalfFeatChoices


UNARMED = 'simple-melee-weapons.unarmed-strike'


class WeaponProfileChoices(HalfFeatChoices):
    def __init__(self, *args):
        super().__init__(*args)
        self.profile_receipts = {
            wid: {'profile': wid, 'grant': self.first + '/first-class-weapons',
                  'sourceClause': self.chassis['weapons'], 'conditional': False}
            for wid in self.weapons
        }
        self.pay.weapon_proficiencies = set(self.weapons)
        self.conditional_profiles = {}

    def acquire_half(self, sid, level, ability, weapons=None):
        event = super().acquire(sid, level, ability, weapons)
        if sid == 'weapon_master':
            for wid in weapons:
                self.profile_receipts.setdefault(wid, {
                    'profile': wid, 'grant': event['grant'], 'conditional': False})
        self.pay.weapon_proficiencies = set(self.weapons)
        return event

    def acquire_profile(self, sid, level, profile):
        if sid not in {'weaponFocus', 'weapon_mastery'}:
            raise ValueError('Not one of these two exact profile-selection feats')
        if not isinstance(profile, str):
            raise ValueError('One permanent exact profile identity is required')
        if profile not in self.weapon_choices and profile not in self.conditional_profiles:
            if not (sid == 'weaponFocus' and profile == UNARMED and profile in self.equipment):
                raise ValueError('Profile outside this evidence slice; no general prohibition inferred')
        qualified = profile in self.weapons and profile in self.profile_receipts
        if sid == 'weapon_mastery':
            qualified = qualified and sum(self.pay.current_classes.values()) >= 6
        if not qualified:
            raise ValueError('Actual selected-profile proficiency and printed level gates required')
        grant = self.pay.commit(sid, self.first + ':' + str(level), choice=profile,
                                prerequisites_met=qualified)
        event = {'kind': 'weapon-profile-selection', 'feat': sid, 'grant': grant,
                 'selectedProfile': profile, 'acquisitionProfile': deepcopy(self.profile(profile)),
                 'proficiencyReceipt': deepcopy(self.profile_receipts[profile]),
                 'totalCharacterLevel': sum(self.pay.current_classes.values()),
                 'equipmentGranted': [], 'proficiencyGranted': []}
        self.events.append(event)
        return deepcopy(event)

    def acquire_precision_throw(self, level):
        node = self.contracts['precision_throw']['requirements']
        if node != {'kind': 'permanentAbility', 'ability': 'DEX', 'minimum': 13}:
            raise ValueError('Unexpected exact Precision Throw gate')
        grant = self.pay.commit('precision_throw', self.first + ':' + str(level),
                                prerequisites_met=self.pay.scores['DEX'] >= 13)
        self.events.append({'kind': 'precision-throw', 'grant': grant})
        return grant

    def profile(self, profile):
        if profile in self.weapon_choices:
            return self.weapon_choices[profile]
        if profile in self.conditional_profiles:
            return self.conditional_profiles[profile]
        if profile == UNARMED:
            return self.equipment[profile]
        raise ValueError('No named profile in this bounded source projection')

    def conditional_natural_body(self, trait, proficiency_receipt=None):
        """Conditional external body/training premise, never an earned grant.

        The real Troll Claws payload is retained; this method does NOT supply
        a transformation, ancestry selection or authenticated proficiency.
        """
        if trait['id'] != 'troll--claws' or 'Your claws are natural weapons' not in trait['text']:
            raise ValueError('Only the explicitly bound real natural profile is represented')
        profile = trait['id']
        self.conditional_profiles[profile] = {
            'id': profile, 'category': 'specific natural melee weapon',
            'trait': deepcopy(trait), 'conditionalBodyPresent': True}
        event = {'kind': 'conditional-external-body-premise', 'profile': profile,
                 'actualAncestryOrTransformationAuthenticated': False,
                 'actualProficiencySourceAuthenticated': False}
        if proficiency_receipt is not None:
            if proficiency_receipt != {'profile': profile, 'conditionalSeparatelyAuthorizedProficiency': True}:
                raise ValueError('A family label is not an exact-profile proficiency receipt')
            self.weapons.add(profile); self.pay.weapon_proficiencies.add(profile)
            self.profile_receipts[profile] = {
                'profile': profile, 'grant': deepcopy(proficiency_receipt), 'conditional': True}
        self.events.append(event)

    def conditional_proficiency_state(self, profile, operative):
        if profile not in self.profile_receipts:
            raise ValueError('No existing profile receipt to suppress or restore')
        if operative:
            self.weapons.add(profile); self.pay.weapon_proficiencies.add(profile)
        else:
            self.weapons.discard(profile); self.pay.weapon_proficiencies.discard(profile)
        self.events.append({'kind': 'conditional-proficiency-state', 'profile': profile,
                            'operative': operative, 'sourceOfChangeNotCreated': True})

    def adjustments(self, profile, delivery, retains_profile=True, usable=True,
                    other_critical_thresholds=()):
        if delivery not in {'melee', 'thrown', 'projectile'}:
            raise ValueError('Unsupported delivery')
        row = self.profile(profile)
        category = row['category'].lower()
        fields = row.get('sourceFields') or {}
        properties = fields.get('Properties', row.get('profile', '')).lower()
        thrown = 'thrown' in properties
        if retains_profile and usable:
            if delivery == 'thrown' and not thrown:
                raise ValueError('Throwing this profile requires the improvised branch')
            if delivery == 'melee' and 'melee' not in category:
                raise ValueError('Melee use does not retain this ranged profile')
            if delivery == 'projectile' and ('ranged' not in category or thrown):
                raise ValueError('This is not a projectile-delivery weapon profile')
        active = retains_profile and usable
        focus = int(active and self.pay.weapon_focus_operative(profile))
        precision = int(active and thrown and delivery == 'thrown' and
                        self.pay.has('precision_throw') and 'precision_throw' not in self.pay.suppressed)
        mastery = active and sum(self.pay.current_classes.values()) >= 6 and \
            'weapon_mastery' not in self.pay.suppressed and any(
                x['identity'] == 'weapon_mastery' and x['choice'] == profile for x in self.pay.grants)
        # Unlike Focus, Mastery does not add a continuing-proficiency predicate.
        # The acquisition credential was recorded when the permanent choice paid.
        if any(type(n) is not int or not 2 <= n <= 20 for n in other_critical_thresholds):
            raise ValueError('Invalid conditional independently applicable critical threshold')
        return {'focusAttackBonus': focus, 'precisionThrowAttackBonus': precision,
                'totalModeledFeatAttackBonus': focus + precision, 'flatDamageBonus': 0,
                'criticalThreshold': min([19 if mastery else 20, *other_critical_thresholds]),
                'attackOrDamagePerformed': False}

    def snapshot(self):
        state = super().snapshot()
        state.update(profileReceipts=deepcopy(getattr(self, 'profile_receipts', {})),
                     conditionalProfiles=deepcopy(getattr(self, 'conditional_profiles', {})))
        return state


def resolve_kept_attack(kept_die, ordinary_modifier, ac, adjustments):
    """Core hit/critical classification only; roll/target legality is conditional."""
    if type(kept_die) is not int or not 1 <= kept_die <= 20:
        raise ValueError('An actual kept d20 face is required')
    total = kept_die + ordinary_modifier + adjustments['totalModeledFeatAttackBonus']
    hit = kept_die != 1 and (kept_die == 20 or total >= ac)
    return {'keptDie': kept_die, 'total': total, 'hit': hit,
            'critical': hit and kept_die >= adjustments['criticalThreshold'],
            'damageResolved': False}
