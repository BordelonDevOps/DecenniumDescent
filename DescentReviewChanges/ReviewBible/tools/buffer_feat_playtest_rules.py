"""Eight source-discussed feat candidates; independent implementation review pending.

Use one FeatWorld with the world's canonical BufferLedger and HealingCommitLedger.
The host owns actual acquisition opportunities, geometry, inventory identity,
canonical turn/round/rest events, soul/hostility classification, attack/damage
attribution and all other sources. Certificates below attest those real events;
they are not permissions to invent targets, rounds, deaths or new summon roots.
No function edits the original feat registry or implements a complete game engine.
"""
from dataclasses import dataclass, field, replace
from fractions import Fraction
from core_playtest_rules import stabilize, heal
from form_temphp_playtest_rules import BufferGrant, BufferLedger, require
from healing_playtest_rules import HealingReduction, HealingCommitLedger, healing_packet
from control_playtest_rules import ClockMarker, clock_marker
from spell_playtest_rules import integer, SpellRuleError
from redirection_playtest_rules import identity

FEATS = frozenset(('chef', 'inspiring_leader', 'empowered_summoning', 'field_medic',
                  'blood_ritual', 'necrotic_affinity', 'lifeleech', 'soul_cage'))


@dataclass(frozen=True)
class FeatStats:
    level: int
    pb: int
    charisma_score: int = 10
    charisma_modifier: int = 0
    constitution_score: int = 10
    medicine: bool = False
    religion: bool = False
    # Actual granted casting-source ID -> current normal spell-save DC.
    casting: dict = field(default_factory=dict)

    def __post_init__(self):
        integer(self.level, 'character level', 1, 20)
        integer(self.pb, 'PB', 2, 6)
        for score in (self.charisma_score, self.constitution_score):
            integer(score, 'ability score', 1)
        require(type(self.charisma_modifier) is int, 'Use signed actual CHA modifier')
        for source, dc in self.casting.items():
            identity(source); integer(dc, 'actual source spell-save DC', 1)


@dataclass
class Owner:
    stats: FeatStats
    feats: set = field(default_factory=set)
    acquisition_events: set = field(default_factory=set)
    soul_dc_source: str | None = None
    soul_charges: int = 0
    recovery: int = 0
    recovery_capacity: int = 0
    last_rest: int = 0


@dataclass
class LongActivity:
    id: str
    owner: str
    feat: str
    started: Fraction
    ends: Fraction
    targets: tuple
    level: int
    pb: int
    charisma: int
    state: str = 'active'


@dataclass
class Kit:
    item_id: str
    uses: int

    def __post_init__(self):
        identity(self.item_id); integer(self.uses, 'actual recorded kit uses', 0)


@dataclass
class Rations:
    inventory_id: str
    servings: int

    def __post_init__(self):
        identity(self.inventory_id); integer(self.servings, 'actual ration equivalents', 0)


@dataclass(frozen=True)
class Stabilization:
    event_id: str
    owner: str
    target: str
    episode: str
    pb: int


class FeatWorld:
    def __init__(self, buffers=None, healing_commits=None):
        self.buffers = buffers if buffers is not None else BufferLedger()
        self.healing_commits = healing_commits if healing_commits is not None else HealingCommitLedger()
        self.owners = {}
        self.activities = {}
        self.family_uses = set()
        self.blood_uses = set()
        self.blood_advantage = {}
        self.summon_lineages = {}
        self.summon_damage = set()
        self.stabilizations = {}
        self.stabilization_episodes = set()
        self.finished_stabilizations = set()
        self.melee_turns = set()
        self.seals = {}
        self.ended_deaths = set()
        self.removed_seals = set()
        self.drain_selections = {}
        self.drain_used = set()
        self.soul_events = set()
        self.soul_bodies = set()
        self.spends = {}
        self.agony = {}
        self.agony_generation = 0
        self.chef_attempts = {}
        self.chef_completed = set()
        self.servings = {}

    def register(self, owner, stats):
        identity(owner)
        require(owner not in self.owners and isinstance(stats, FeatStats), 'Register one canonical owner')
        self.owners[owner] = Owner(stats, last_rest=self.epoch(owner))

    def epoch(self, target):
        return self.buffers.rest_epochs.get(target, 0)

    def has(self, owner, feat):
        return owner in self.owners and feat in self.owners[owner].feats

    def require_feat(self, owner, feat):
        require(self.has(owner, feat), 'Actual feat ownership required')
        return self.owners[owner]

    def acquire(self, owner, feat, event_id, *, legal_selection, dc_source=None):
        identity(event_id)
        require(owner in self.owners and feat in FEATS, 'Known owner and feat required')
        o = self.owners[owner]; s = o.stats
        require(legal_selection and event_id not in o.acquisition_events and feat not in o.feats,
                'Actual unspent class feat selection and nonrepeatable feat required')
        gates = {'chef': True, 'inspiring_leader': s.charisma_score >= 13,
                 'empowered_summoning': s.charisma_score >= 14, 'field_medic': s.medicine,
                 'blood_ritual': s.constitution_score >= 13 and s.level >= 4,
                 'necrotic_affinity': s.religion or s.level >= 8,
                 'lifeleech': bool(s.casting),
                 'soul_cage': s.level >= 8 and ('lifeleech' in o.feats or bool(s.casting))}
        require(gates[feat], 'Printed prerequisite not met at acquisition')
        if feat == 'soul_cage':
            require(dc_source in s.casting, 'Lock one actually possessed casting source/ability')
        o.feats.add(feat); o.acquisition_events.add(event_id)
        if feat == 'soul_cage': o.soul_dc_source = dc_source

    def completed_rest(self, owner, epoch):
        """Host calls exactly once for an ACTUAL completed LR, before tie activations.

        This wrapper processes the canonical BufferLedger epoch; do not also call
        BufferLedger.completed_long_rest separately for the same rest.
        """
        self.buffers.completed_long_rest(owner, epoch)
        self.blood_advantage.pop(owner, None)
        if owner in self.owners:
            o = self.owners[owner]; o.last_rest = epoch
            if 'lifeleech' in o.feats:
                o.recovery = o.recovery_capacity = 2 * o.stats.level

    def grant(self, grant_id, feat, owner, target, amount, *, expiry=None, dependencies=()):
        return BufferGrant(grant_id, 'feat:' + feat, owner, target, amount,
                           expiry=expiry, rest_epoch=None if expiry is not None else self.epoch(target),
                           dependencies=dependencies)

    def family_key(self, feat, target):
        return feat, target, self.epoch(target)

    def start_cooking(self, owner, rest_attempt, count, now, *, legal_rest_activity, utensils):
        o = self.require_feat(owner, 'chef'); identity(rest_attempt)
        integer(count, 'intended servings', 1, o.stats.pb)
        key = owner, rest_attempt
        require(key not in self.chef_attempts and legal_rest_activity and utensils,
                'One designated batch per real rest attempt; actual utensils/light-activity allowance required')
        self.chef_attempts[key] = {'count':count, 'start':clock_marker(now).seconds,
                                  'epoch':self.epoch(owner), 'state':'cooking', 'items':[]}

    def finish_cooking(self, owner, rest_attempt, inventory, item_ids, now, *, uninterrupted):
        r = self.chef_attempts[(owner, rest_attempt)]; item_ids = tuple(item_ids)
        require(r['state'] == 'cooking' and uninterrupted and clock_marker(now).seconds >= r['start']+3600,
                'One actual uninterrupted cooking hour required')
        require(inventory.servings >= r['count'] and len(item_ids) == r['count']
                and len(set(item_ids)) == len(item_ids) and not set(item_ids).intersection(self.servings),
                'Pay one real ration equivalent for each unique prepared item')
        for item in item_ids: identity(item)
        inventory.servings -= r['count']; r['state'] = 'prepared'; r['items'] = list(item_ids)
        for item in item_ids:
            self.servings[item] = {'owner':owner, 'state':'ordinary', 'amount':0, 'expiry':None,
                                   'creationEpoch':None}
        return item_ids

    def abort_cooking_rest(self, owner, rest_attempt):
        r = self.chef_attempts[(owner, rest_attempt)]
        require(r['state'] in ('cooking','prepared'), 'Batch already settled')
        r['state'] = 'aborted'  # Already cooked/paid food stays ordinary.

    def finalize_chef(self, owner, rest_attempt, now, *, actual_successful_rest):
        o = self.require_feat(owner, 'chef'); r = self.chef_attempts[(owner, rest_attempt)]
        epoch = self.epoch(owner); key = owner, epoch
        require(actual_successful_rest and r['state'] == 'prepared' and epoch == r['epoch']+1
                and key not in self.chef_completed, 'Finalize one prepared batch just AFTER its actual successful LR')
        items = [i for i in r['items'] if self.servings[i]['state'] == 'ordinary']
        chosen = items[:o.stats.pb]; t = clock_marker(now).seconds
        for item in chosen:
            self.servings[item].update(state='potent', amount=2*o.stats.pb, expiry=t+86400,
                                      creationEpoch=epoch)
        r['state'] = 'finalized'; self.chef_completed.add(key)
        return tuple(chosen)

    def serving_potent(self, item, now):
        s = self.servings[item]
        return (s['state'] == 'potent' and clock_marker(now).seconds < s['expiry']
                and self.epoch(s['owner']) == s['creationEpoch'])

    def consume_chef(self, event_id, item, target, started, now, *, legal_uninterrupted_consumption):
        identity(event_id); identity(target)
        s = self.servings[item]; key = self.family_key('chef', target)
        require(legal_uninterrupted_consumption and clock_marker(now).seconds >= clock_marker(started).seconds+60,
                'Actual legal possession and one uninterrupted minute eating required')
        require(self.serving_potent(item, now) and key not in self.family_uses,
                'Unused potent serving and unused recipient Chef entitlement required')
        g = self.grant(event_id, 'chef', s['owner'], target, s['amount'])
        self.buffers.validate_offer(g, now)
        s['state'] = 'consumed'; self.family_uses.add(key)
        return self.buffers.offer(g, now)

    def retire_serving(self, item, *, actually_consumed_or_discarded):
        require(actually_consumed_or_discarded and self.servings[item]['state'] not in ('consumed','discarded'),
                'Only an actual unconsumed food item can be retired')
        self.servings[item]['state'] = 'discarded'

    def start_activity(self, event_id, owner, feat, targets, now, *, legal):
        o = self.require_feat(owner, feat); identity(event_id)
        require(feat in ('inspiring_leader', 'blood_ritual'), 'Use exact long activation')
        targets = tuple(targets); s = o.stats
        require(legal and event_id not in self.activities, 'Unique legal activation required')
        require(len(set(targets)) == len(targets) and owner not in targets and len(targets) <= s.pb,
                'Select at most PB distinct OTHER recipients at start')
        for target in targets: identity(target)
        if feat == 'inspiring_leader':
            require(all(self.family_key(feat, t) not in self.family_uses for t in targets),
                    'Recipient already received a legal offer this rest')
        else:
            key = owner, self.epoch(owner)
            require(key not in self.blood_uses, 'Blood Ritual already used this rest')
            self.blood_uses.add(key)
        start = clock_marker(now).seconds
        self.activities[event_id] = LongActivity(event_id, owner, feat, start, start+600,
                                                 targets, s.level, s.pb, s.charisma_modifier)
        return self.activities[event_id]

    def interrupt_activity(self, event_id):
        a = self.activities[event_id]
        require(a.state == 'active', 'Activity already settled')
        a.state = 'interrupted'

    def finish_activity(self, event_id, now, *, continuously_eligible):
        """Host tracked each selected recipient throughout; never replace a dropout.

        Owner interruption MUST call interrupt_activity. For exact LR timestamp
        ties host completes the rest first. Offers preflight together before any
        mutation; rejected strongest-only offers still spend family entitlement.
        """
        a = self.activities[event_id]; t = clock_marker(now).seconds
        require(a.state == 'active' and t >= a.ends, 'Actual uninterrupted ten minutes required')
        eligible = set(continuously_eligible)
        require(eligible <= set(a.targets), 'No retargeting during a long activation')
        offers = []
        if a.feat == 'inspiring_leader':
            for target in a.targets:
                if target in eligible and self.family_key(a.feat, target) not in self.family_uses:
                    offers.append(self.grant(a.id+':'+target, a.feat, a.owner, target,
                                             max(1, a.level+a.charisma)))
        else:
            offers.append(self.grant(a.id+':self', a.feat, a.owner, a.owner, 2*a.level))
            for target in a.targets:
                if target in eligible:
                    offers.append(self.grant(a.id+':'+target, a.feat, a.owner, target, a.level,
                                             expiry=ClockMarker(t+3600)))
        for g in offers: self.buffers.validate_offer(g, now)
        a.state = 'completed'
        result = []
        for g in offers:
            if a.feat == 'inspiring_leader': self.family_uses.add(self.family_key(a.feat, g.target))
            result.append(self.buffers.offer(g, now))
        if a.feat == 'blood_ritual': self.blood_advantage[a.owner] = self.epoch(a.owner)
        return result

    def blood_save(self, owner, *, actual_save_rolled, curse_or_disease):
        available = self.blood_advantage.get(owner) == self.epoch(owner)
        if available and actual_save_rolled and curse_or_disease:
            del self.blood_advantage[owner]
            return True
        return False

    def summon_created(self, event_id, owner, source_root, creation_slot, creature, now,
                       *, qualifying_creation, actual_paid_source_activation):
        o = self.require_feat(owner, 'empowered_summoning')
        for value in (event_id, source_root, creation_slot, creature): identity(value)
        require(qualifying_creation and actual_paid_source_activation,
                'Actual finite creature creation by owner, not return/rebuild/device')
        key = owner, source_root, creation_slot
        if key in self.summon_lineages: return None
        g = self.grant(event_id, 'empowered_summoning', owner, creature, 2*o.stats.pb,
                       dependencies=(creature,))
        self.buffers.validate_offer(g, now)
        self.summon_lineages[key] = creature
        return self.buffers.offer(g, now)

    def summon_damage_bonus(self, owner, source_root, creation_slot, round_window, *, actual_damage_roll):
        o = self.require_feat(owner, 'empowered_summoning'); identity(round_window)
        lineage = owner, source_root, creation_slot
        require(lineage in self.summon_lineages, 'Qualifying creation lineage required')
        key = lineage, round_window
        if not actual_damage_roll or key in self.summon_damage: return 0
        self.summon_damage.add(key)
        return o.stats.pb

    def record_stabilization(self, event_id, owner, target, episode, before, after, *, owner_caused):
        o = self.require_feat(owner, 'field_medic')
        for value in (event_id, target, episode): identity(value)
        key = target, episode, owner
        require(owner_caused and not before.dead and before.hp == 0 and not before.stable
                and not after.dead and after.hp == 0 and after.stable,
                'Capture the actual dying-to-Stable transition before later independent healing')
        require(event_id not in self.stabilizations and key not in self.stabilization_episodes,
                'This actual stabilization/owner episode was already recorded')
        record = Stabilization(event_id, owner, target, episode, o.stats.pb)
        self.stabilizations[event_id] = record; self.stabilization_episodes.add(key)
        return record

    def kit_stabilize(self, event_id, owner, target, episode, life, kit, wallet,
                      now, d4, *, legal):
        self.require_feat(owner, 'field_medic')
        require(legal and kit.uses > 0, 'Actual reachable dying target and stocked kit required')
        require(event_id not in self.stabilizations and (target, episode, owner) not in self.stabilization_episodes,
                'Stabilization replay')
        wallet.validate(action='bonus')
        out = replace(life); stabilize(out, d4, now)
        # Validate record identifiers before any resource is spent.
        for value in (event_id, target, episode): identity(value)
        wallet.pay(action='bonus'); kit.uses -= 1
        self.record_stabilization(event_id, owner, target, episode, life, out, owner_caused=True)
        return out

    def finish_stabilization(self, event_id, now, *, living_target):
        r = self.stabilizations[event_id]
        require(event_id not in self.finished_stabilizations, 'Stabilization already finished')
        g = self.grant(event_id+':buffer', 'field_medic', r.owner, r.target, r.pb)
        if living_target: self.buffers.validate_offer(g, now)
        self.finished_stabilizations.add(event_id)
        return self.buffers.offer(g, now) if living_target else None

    def melee_necrotic(self, owner, turn_id, dice, *, melee_hit, opted_in, critical=False):
        self.require_feat(owner, 'necrotic_affinity'); identity(turn_id)
        key = owner, turn_id
        if not (melee_hit and opted_in) or key in self.melee_turns: return 0
        require(len(dice) == (2 if critical else 1), 'One feat d6; two on critical')
        for die in dice: integer(die, 'necrotic d6', 1, 6)
        self.melee_turns.add(key)
        return sum(dice)

    def seal_death(self, owner, death_instance, now, *, actual_dead, owned_necrotic_fatal_root):
        self.require_feat(owner, 'necrotic_affinity'); identity(death_instance)
        require(actual_dead and owned_necrotic_fatal_root and death_instance not in self.ended_deaths,
                'Actual death with positive owned necrotic harm in canonical fatal root required')
        key = owner, death_instance
        if key in self.seals: return False
        self.seals[key] = clock_marker(now).seconds+86400
        return True

    def resurrection_sealed(self, death_instance, now, actual_rank):
        if actual_rank is None or death_instance in self.ended_deaths: return False
        integer(actual_rank, 'actual spell/effective rank', 0)
        if actual_rank > 5: return False
        t = clock_marker(now).seconds
        return any(d == death_instance and t < expiry and (owner, d) not in self.removed_seals
                   for (owner, d), expiry in self.seals.items())

    def remove_seal(self, owner, death_instance, *, explicit_removal):
        require(explicit_removal and (owner, death_instance) in self.seals,
                'Exact source capable of removing this resurrection blocker required')
        self.removed_seals.add((owner, death_instance))

    def returned_to_life(self, death_instance, *, actual_legal_return):
        require(actual_legal_return, 'Only completed legal resurrection ends this death instance')
        self.ended_deaths.add(death_instance)

    def select_drain(self, owner, spell_root, round_window, target, *, eligible_before_damage):
        self.require_feat(owner, 'lifeleech')
        for value in (spell_root, round_window, target): identity(value)
        key = owner, spell_root, round_window
        require(eligible_before_damage and key not in self.drain_selections,
                'Designate one genuine hostile before damage; no retargeting/farming')
        self.drain_selections[key] = target

    def drain(self, event_id, owner, spell_root, round_window, target, life, actual_necrotic_damage,
              *, own_spell_damage, hostile_not_farmed, parent_flags=frozenset(), **healing_options):
        """Commit a finite Lifeleech child heal and return its new canonical life state.

        Damage is the already-resolved necrotic component: actual THP absorption
        plus actual normal HP lost, no overkill. Host uses one canonical six-second
        round-window ID across initiative changes. No copied/Agony/natural-attack
        event may masquerade as owner spell damage. The caller must publish the
        returned state exactly once; no second ordinary healing operation.
        """
        o = self.require_feat(owner, 'lifeleech'); identity(event_id)
        integer(actual_necrotic_damage, 'actual necrotic damage dealt', 0)
        key = owner, spell_root, round_window
        require(self.drain_selections.get(key) == target, 'Use the one target designated before resolution')
        require(own_spell_damage and hostile_not_farmed, 'Actual eligible personal spell damage required')
        require('reserve' not in healing_options, 'The feat owns its one finite reserve')
        if 'noLifeleechRetrigger' in parent_flags or key in self.drain_used or actual_necrotic_damage == 0:
            return None
        if life.dead:
            self.drain_used.add(key)
            return {'state':replace(life), 'fundedAmount':0, 'actualHpGained':0, 'genuineExcess':0,
                    'reserveSpent':0, 'reserveRemaining':o.recovery, 'doesNotResurrect':True}
        packet = healing_packet(life, actual_necrotic_damage//2, reserve=o.recovery, **healing_options)
        funded = min(packet['legalAmount'], o.recovery)
        out = heal(life, funded)
        packet.update(state=out, legalAmount=funded, fundedAmount=funded,
                      preFundingLegalAmount=packet['legalAmount'], actualHpGained=out.hp-life.hp,
                      genuineExcess=max(0, funded-(life.maximum_hp-life.hp)),
                      reserveSpent=funded, reserveRemaining=o.recovery-funded,
                      flags=frozenset(parent_flags)|frozenset(('noLifeleechRetrigger',
                               'blockHealCopyTriggers','blockResourceTriggers')),
                      explicitFundedExcessConversionPermitted=True)
        self.commit_healing(event_id, packet)
        self.drain_used.add(key); o.recovery -= funded
        return packet

    def death_checkpoint(self, owner, event_id, body_id, *, actual_new_death_checkpoint,
                         qualifying_hostile_soul, legal_range_perception_line,
                         crystal_available=False, accept=True):
        """Residue only: no Soul Bind removal, soul custody or resurrection block.

        Even an ineligible checkpoint is permanently evaluated for that owner.
        Eligible decline/full-capacity also reserves that body for the owner LR.
        Canonical immutable body IDs persist through transforms/resurrection.
        """
        require(owner in self.owners and actual_new_death_checkpoint, 'Actual death checkpoint required')
        for value in (event_id, body_id): identity(value)
        event_key = owner, event_id
        require(event_key not in self.soul_events, 'This death event was already evaluated')
        o = self.owners[owner]
        automatic = 'lifeleech' in o.feats
        source = automatic or ('soul_cage' in o.feats and crystal_available)
        eligible = source and qualifying_hostile_soul and legal_range_perception_line
        body_key = owner, body_id, self.epoch(owner)
        self.soul_events.add(event_key)
        if not eligible or body_key in self.soul_bodies: return 0
        self.soul_bodies.add(body_key)
        gained = int(o.soul_charges < 3 and (automatic or accept))
        o.soul_charges += gained
        return gained

    def begin_soul_ability(self, event_id, owner, target, mode, wallet, *, legal, crystal_available):
        o = self.require_feat(owner, 'soul_cage')
        for value in (event_id, target): identity(value)
        require(mode in ('shield', 'agony') and legal and crystal_available,
                'Actual black crystal and source-specific legal creature target required')
        require(event_id not in self.spends, 'Soul ability event replay')
        cost = 1 if mode == 'shield' else 2; action = 'bonus' if mode == 'shield' else 'action'
        require(o.soul_charges >= cost, 'Insufficient actual Soul Charges')
        dc = None
        if mode == 'agony':
            require(o.soul_dc_source in o.stats.casting, 'Locked DC source must supply actual current DC')
            dc = o.stats.casting[o.soul_dc_source]
        wallet.validate(action=action)
        wallet.pay(action=action); o.soul_charges -= cost
        self.spends[event_id] = {'owner':owner, 'target':target, 'mode':mode, 'dc':dc, 'finished':False}
        return {'chargesPaid':cost, 'dc':dc, 'damageOwner':owner, 'sourceKind':'feat'}

    def finish_soul_shield(self, event_id, dice, now):
        p = self.spends[event_id]
        require(p['mode'] == 'shield' and not p['finished'], 'Pending paid shield required')
        require(len(dice) == 2, 'Roll exactly 2d8')
        for die in dice: integer(die, 'shield d8', 1, 8)
        g = self.grant(event_id, 'soul_cage', p['owner'], p['target'], sum(dice))
        self.buffers.validate_offer(g, now)
        p['finished'] = True
        return self.buffers.offer(g, now)

    def finish_agony(self, event_id, dice, now, *, con_save_success):
        """Return the single damage instruction, before defenses/Core resolution.

        The separate healing rider applies regardless of save/immunity; source
        targeting legality was established before payment. Never deal the returned
        damage a second time when committing the caller's canonical damage event.
        """
        p = self.spends[event_id]
        require(p['mode'] == 'agony' and not p['finished'], 'Pending paid Agony Lance required')
        require(len(dice) == 3 and type(con_save_success) is bool, 'Actual CON result and 3d8 required')
        for die in dice: integer(die, 'Agony d8', 1, 8)
        t = clock_marker(now).seconds
        old = self.agony.get(p['target'])
        if old is not None and old['expires'] > t:
            old['expires'] = max(old['expires'], t+60)
            old['owner'] = p['owner']; old['contributors'].append(event_id)
        else:
            self.agony_generation += 1
            self.agony[p['target']] = {'id':'agony-healing:'+str(self.agony_generation),
                 'expires':t+60, 'owner':p['owner'], 'contributors':[event_id]}
        p['finished'] = True
        return {'damage':sum(dice)//2 if con_save_success else sum(dice), 'type':'necrotic',
                'damageOwner':p['owner'], 'sourceKind':'feat', 'spellRoot':None}

    def agony_reduction(self, target, now, *, suppressed=False):
        r = self.agony.get(target)
        if r is None or clock_marker(now).seconds >= r['expires']: return None
        return HealingReduction(r['id'], 'feat:soul_cage:agony', 'factor', Fraction(1,2),
                                suppressed=suppressed, next_healing=True)

    def commit_healing(self, event_id, packet):
        ids = self.healing_commits.commit(event_id, packet)
        self.agony = {t:r for t,r in self.agony.items() if r['id'] not in ids}
        return ids

    def remove_agony(self, target, *, explicit_removal):
        require(explicit_removal, 'Exact removal of magical healing suppression required')
        return self.agony.pop(target, None)

    def release_souls(self, owner, amount, *, actual_quiet_minute, crystal_available):
        o = self.require_feat(owner, 'soul_cage'); integer(amount, 'charges released', 1, 3)
        require(actual_quiet_minute and crystal_available and o.soul_charges >= amount,
                'Actual one-minute crystal handling and owned charges required')
        o.soul_charges -= amount
