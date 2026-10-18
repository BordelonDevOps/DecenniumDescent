"""Conditional class/scene witnesses; no real campaign history asserted."""
from copy import deepcopy
from fractions import Fraction
from feat335_copy_payload_fixtures import CopyPayloadFixtures, R, G, A
from feat335_copy_class_providers import ClassCopyAcquisition, ABILITIES
from feat335_copy_class_release import ClassCopyPayloadReleases, ShamanConcentrationBridge
from feat335_copy_capture import CopyCaptures
from creature_lifecycle_playtest_rules import EchoLedger
from transformation_spell_playtest_rules import ConcentrationLedger
from di7_area_fixtures import make as area_fixture
from di7_shaman_transactions import ShamanSources, ShamanTransactions

KITS = {
    'Shaman': ['shaman.base.totem-casting', 'shaman.base.spirit-shock', 'shaman.base.flask-use', 'shaman.base.elemental-ward'],
    'Mirrorsage': ['mirrorsage.base.mirrorbind', 'mirrorsage.base.echo-release', 'mirrorsage.base.mirror-beast-summon', 'mirrorsage.base.reflective-shield']}


class ClassCopyFixtures(CopyPayloadFixtures):
    def class_acquisition(self, name, level=12, *, learn=True, select=True):
        actor = deepcopy(self.actor)
        actor.update(firstClass=name, classLevels={name: 1}, heroPath='conditional-pre-Hero-ordinary-provider')
        ability = ABILITIES[name]; other = 'INT' if name == 'Shaman' else 'WIS'
        actor['abilityRolls'][ability] = [1, 5, 6, 6]; actor['permanentScores'][ability] = 18
        actor['abilityRolls'][other] = [1, 3, 6, 6] if name == 'Shaman' else [1, 1, 6, 6]
        actor['permanentScores'][other] = 16 if name == 'Shaman' else 14
        h = ClassCopyAcquisition(actor, self.classes, self.equipment, self.skills, self.ancestry,
                                self.backgrounds, self.contracts, self.supplements, self.sources)
        if select: h.select_base(KITS[name], 'conditional-actual-first-level-Base-selection')
        if learn:
            sid = 'lifedraw' if name == 'Shaman' else 'shield'
            h.native_known([{'spellId': sid, 'atClassLevel': 1, 'event': 'conditional-native-learning/' + sid}], 'conditional-native-repertoire')
        for sid, n in [('eldritch_echo', 4), ('mimicry', 8), ('arcane_adaptation', 12)]:
            if n <= level:
                h.advance(n); h.earn(n); h.acquire_copy(sid, n)
        h.advance(level)
        if level >= 10: h.native_state['heroPath'] = 'Soothsayer' if name == 'Shaman' else 'Light Weaver'
        return h

    def class_make(self, name, *, level=12, shaman=False):
        h = self.class_acquisition(name, level)
        old = self.make()
        pool = {'owner': 'owner', 'source': name + '/class-engine',
                'rp': h.class_source['rpByClassLevel'][level - 1],
                'maxRP': h.class_source['rpByClassLevel'][level - 1],
                'actions': 1, 'turnId': 'turn1', 'bonus_action': True, 'reaction': True}
        cadence = {'dissonance': 0, 'previousSpell': None, 'refrain': 0, 'classRecords': {}}
        ledger = ConcentrationLedger(); integration = None
        if shaman:
            if name != 'Shaman': raise ValueError('Actual Shaman source required')
            integration = self.shaman(h); pool = integration.actors['owner']; cadence = pool
            pool.update(owner='owner', source='Shaman/class-engine')
            ledger = ShamanConcentrationBridge(integration, 'owner')
        m = ClassCopyPayloadReleases(CopyCaptures(h, old.captures.witnesses), 'owner', pool, cadence, ledger, old.world,
            echoes=EchoLedger('owner') if name == 'Mirrorsage' else None, action_account=pool)
        m.captures.start_regular(pool['turnId'], 1, 1, actual_new_regular_start=True)
        m.world.advance(Fraction(36061, 10) if shaman else Fraction(61, 10), [m])
        if shaman: m.world.actors['owner']['inProgressRegularEnd'] = Fraction(14425, 4)
        return m, integration

    def shaman(self, h):
        sources = ShamanSources(); base, _ = area_fixture(sources, provider='Shaman')
        actors = deepcopy(base.actors); world = deepcopy(base.world)
        actors['owner'].update(classLevel=h.pay.current_classes['Shaman'], totalLevel=h.pay.current_classes['Shaman'],
                               abilityScore=h.pay.scores['WIS'], heroPath=h.native_state['heroPath'])
        world['roundClock'] = {'origin': 3600, 'authorityEvent': 'conditional-six-second-clock'}
        world['auraLines'] = {}
        world['totemSites'] = {'near': {'positionFeet': 5, 'authorityEvent': 'conditional-actual-ground-site',
            'perceived': True, 'lineOfEffect': True, 'groundSupportsTinyObject': True, 'occupiedByCreature': False}}
        for entity in world['entities'].values():
            entity.update(actualPoisonRecords=[], poisonHistoryAuthority='conditional-actual-poison-absence', explicitPoisonAbsenceOrCompleteRecords=True)
        m = ShamanTransactions(sources, actors, world)
        m.select_base_kit('owner', h.base_kit['choices'], h.base_kit['event'], affinity='Earth')
        m.learn_cantrip('owner', 'detect-poison', 'conditional-actual-first-access-cantrip-choice')
        m.configure_clock('initiative-virtual-source-start', {'owner': 0, 'counter': 2},
                          {'id': 'clock', 'at': 3600, 'authorityEvent': 'conditional-actual-turn-order'})
        m.begin_turn('owner', 'totem-turn'); m.cast_totem('owner', 'totem', 'near')
        m.world['auraLines']['owner>totem'] = {'authorityEvent': 'conditional-open-own-aura', 'lineOfEffect': True}
        m.advance(3606); m.begin_turn('owner', 'turn1')
        h.bind_class_state(m.actors['owner'])
        return m

    @staticmethod
    def capture_class(m, profile, event='capture', *, sid='mimicry', adapt=False, grant=None):
        geo = dict(actualCaptureWindow=True, conscious=True, actualFeatAvailable=True, sourceCreatureDistance=30,
            resolvedComponentDistance=30, sourcePerceived=True, effectPerceived=True, lineOfEffect=True,
            usedAgainstOwner=False, sourceLawfulRange=True, actualReactionLegal=True)
        return m.captures.capture(event, sid, 'source-' + profile, profile,
            grant or m.captures.acquired.first + '/class-engine', geo, adapt=adapt)

    def declare_class(self, m, profile, event='cast', cap='capture', *, permission='pending', grant=None):
        frame = self.frame(m); frame['actions'] = m.action_account['actions']
        return m.declare(event, cap, permission=permission, grant_id=grant or m.captures.acquired.first + '/class-engine',
                         frame=frame, selection=self.selection(profile))
