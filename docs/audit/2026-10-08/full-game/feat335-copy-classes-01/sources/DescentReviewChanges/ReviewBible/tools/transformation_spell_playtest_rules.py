"""Five-spell reference adapter. CANDIDATE: independent review pending.

Not a complete combat engine. Caller supplies canonical cast/access/geometry
legality, current caster statistics, actual save results, original-turn markers,
and already-finalized HP outcomes. One world/ledger per game; do not copy HP or
command ledgers. All preflight occurs before payment, then concentration ends,
then counters/saves resolve. Nothing here grants a class feature or source use.
"""
from dataclasses import dataclass, field
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import json

from spell_playtest_rules import SpellRuleError, integer
from form_temphp_playtest_rules import BufferLedger, BufferGrant, require
from redirection_playtest_rules import identity
from device_lifecycle_playtest_rules import Wallet, CommandLedger

PROFILES={p['id']:p for p in json.loads((Path(__file__).resolve().parents[1]/'data/playtest/spell_form_profiles.json').read_text(encoding='utf-8'))['profiles']}
SPELLS={'polymorph':4,'shapechange':9,'true-polymorph':9,'mass-polymorph':9}
SIZES=('Tiny','Small','Medium','Large','Huge','Gargantuan')
TEMPLATES=frozenset({'barrier/slab','ramp/wedge','open-container','static-furniture','simple-one-piece-tool'})


@dataclass(frozen=True)
class CastStats:
    owner: str
    source_class: str
    attack: int
    dc: int
    pb: int
    modifier: int

    def __post_init__(self):
        identity(self.owner);identity(self.source_class)
        require(type(self.attack) is int,'Actual signed spell attack required')
        integer(self.dc,'spell DC',1);integer(self.pb,'PB',2,6)
        integer(self.modifier,'M=max(1, casting modifier)',1)


@dataclass(frozen=True)
class CastPrice:
    spell_id: str
    rank: int
    base_paid: int
    other_paid: int
    quote: dict=field(compare=False)

    @classmethod
    def from_quote(cls,quote,*,actual_base_paid=None,exact_reduction_authorized=False):
        """Consume canonical quote_cast result; exact class discounts are external.

        This does not establish known/prepared access or grant a discount. Those
        gates must already have passed in the caller's source-qualified preflight.
        Refrain/Dissonance/trauma follow quote plus the canonical class interface.
        """
        base=integer(quote['baseRpCost'],'quoted base RP',0)
        extra=integer(quote['additionalRpCost'],'quoted additional RP',0)
        surcharge=integer(quote['surcharge'],'quoted surcharge',0)
        require(quote['cost']==base+extra+surcharge,'Inconsistent canonical quote')
        paid=base if actual_base_paid is None else integer(actual_base_paid,'actual base paid',0,base)
        require(paid==base or exact_reduction_authorized,'Exact base reduction authority required')
        identity(quote['spellId']);integer(quote['rank'],'rank',0,9)
        return cls(quote['spellId'],quote['rank'],paid,extra+surcharge,deepcopy(quote))

    @property
    def total(self):return self.base_paid+self.other_paid


def harmonic_bulwark(ledger,stats,price,wallet,grant_id,target,conversion,now,*,legal,countered=False):
    """Commit everything before countering/arbitration; return cadence quote.

    Exact free-copy permissions need their own source adapter. This method is a
    fresh paid cast and will not mint an offer with zero credited RP.
    """
    require(isinstance(ledger,BufferLedger) and isinstance(stats,CastStats),'Canonical state required')
    require(legal and price.spell_id=='harmonic-bulwark' and price.rank==3,'Legal Harmonic Bulwark cast required')
    integer(conversion,'conversion X',0,stats.pb)
    credited=price.base_paid+conversion
    require(credited>0,'Zero credited RP cannot create a fresh shield')
    if not hasattr(ledger,'ordinary_cast_events'):ledger.ordinary_cast_events=set()
    require(grant_id not in ledger.ordinary_cast_events,'Cast identity already committed, including countered casts')
    grant=BufferGrant(grant_id,'ordinary-spell:harmonic-bulwark',stats.owner,target,5*credited,
                      rest_epoch=ledger.rest_epochs.get(target,0))
    ledger.validate_offer(grant,now)
    wallet.validate(rp=price.total+conversion,action='action')
    wallet.pay(rp=price.total+conversion,action='action')
    ledger.ordinary_cast_events.add(grant_id)
    return {'paidRP':price.total+conversion,'creditedRP':credited,'cadenceQuote':deepcopy(price.quote),
            'offer':None if countered else ledger.offer(grant,now),'countered':bool(countered)}


class ConcentrationLedger:
    """One ledger shared by ALL concentration spells, including other adapters.

    Each entry's end callback must be total/nonthrowing after valid preflight.
    Starting after payment always destroys the former entry, even if the new
    spell is countered or every target saves. Call end on actual concentration
    failure/incapacitation or a legal voluntary release.
    """
    def __init__(self):self.current={}

    def end(self,owner,reason):
        old=self.current.pop(owner,None)
        if old:old[1](reason)
        return old[0] if old else None

    def start_committed(self,owner,cast_id,on_end):
        old=self.end(owner,'new-concentration')
        self.current[owner]=(cast_id,on_end)
        return old

    def detach(self,owner,cast_id):
        if self.current.get(owner,(None,))[0]==cast_id:del self.current[owner]


@dataclass(frozen=True)
class PhysicalOrigin:
    identity: str
    kind: str
    size: str
    type_tags: frozenset=frozenset()
    mass: int | None=None
    value: int | None=None

    def __post_init__(self):
        identity(self.identity);require(self.kind in ('creature','object'),'Immutable origin kind required')
        require(self.size in SIZES,'Actual original size required')
        if self.mass is not None:integer(self.mass,'recorded origin mass',1)
        if self.value is not None:integer(self.value,'documented original value',0)


@dataclass
class Body:
    """Single underlying physical identity. No transformation HP field exists.

    life is the actual mutable/canonical character or structural ledger object;
    the adapter never heals, reconstructs or replaces it. Origin is immutable.
    Gear IDs and availability represent real items, not inventory creation.
    """
    origin: PhysicalOrigin
    life: object
    size: str
    mass: int | None=None
    equipment: set=field(default_factory=set)
    melded: set=field(default_factory=set)
    lost_items: set=field(default_factory=set)
    destroyed: bool=False
    anatomy: str | None=None
    slot_sponsor: str | None=None
    controller: str | None=None
    placement_pending: bool=False
    placement_conflict: bool=False

    @property
    def identity(self):return self.origin.identity


@dataclass(frozen=True)
class Selection:
    target: str
    profile: str | None
    willing: bool
    # Geometry caller supplies occupied cells at the post-concentration-save
    # stage; every possible unchanged/transformed shape must individually fit.
    original_cells: frozenset
    transformed_cells: frozenset
    legal: bool
    object_template: str | None=None
    object_size: str | None=None
    object_mass: int | None=None
    object_value: int | None=None
    object_input_eligible: bool=False
    mundane_output_certified: bool=False


@dataclass
class Link:
    identity: str
    cast_id: str
    target: str
    profile: str | None
    willing: bool
    deadline: int
    state: str='shaping'
    object_template: str | None=None
    object_size: str | None=None
    object_mass: int | None=None
    last_switch: int | None=None
    suppressed: bool=False


@dataclass
class Cast:
    identity: str
    spell_id: str
    caster: str
    rank: int
    stats: CastStats
    casting_regular_index: int
    links: list=field(default_factory=list)
    state: str='committed'


def validate_mass_space(selections):
    require(1<=len(selections)<=10 and len({s.target for s in selections})==len(selections),
            'Choose1..10 distinct physical targets')
    for s in selections:
        require(s.legal and s.original_cells and s.transformed_cells,'Both possible footprints must individually fit')
    for a,b in combinations(selections,2):
        for aa,bb in product((a.original_cells,a.transformed_cells),(b.original_cells,b.transformed_cells)):
            require(aa.isdisjoint(bb),'Independent Mass outcomes could overlap')


class TransformationWorld:
    """Bounded anatomy/concentration bridge; no hidden previous-form stack."""
    def __init__(self,buffers,concentration):
        require(isinstance(buffers,BufferLedger) and isinstance(concentration,ConcentrationLedger),'Canonical shared ledgers required')
        self.buffers=buffers;self.concentration=concentration
        self.bodies={};self.casts={};self.links={};self.slots={};self.druids={}
        self.damage_rounds=set();self.damage_events=set();self.regular_ends=set();self.commands={}
        self.events=[]
        # Shared with the Druid admission bridge, including suppressed records.
        if not hasattr(buffers,'spell_anatomies'):buffers.spell_anatomies={}

    def add_body(self,body,*,druid=None):
        require(isinstance(body,Body) and body.identity not in self.bodies,'Register each physical identity once')
        require(body.size in SIZES and body.life is not None,'Actual anatomy and HP ledger required')
        require(not body.anatomy and not body.melded and not body.slot_sponsor,'Register at original anatomy, or restore complete serialized world')
        self.bodies[body.identity]=body
        if druid is not None:
            require(druid.owner==body.identity and druid.buffers is self.buffers,'Druid must share world and owner')
            self.druids[body.identity]=druid

    def current(self,target):
        body=self.bodies[target]
        return self.links.get(body.anatomy)

    def _current_creature(self,body):
        link=self.current(body.identity)
        if link and not link.suppressed:return link.profile is not None
        return body.origin.kind=='creature'

    def _validate_selection(self,spell_id,rank,s,caster):
        identity(s.target);require(s.target in self.bodies,'Known physical target required')
        b=self.bodies[s.target];old=self.current(s.target)
        require(s.legal and not b.destroyed,'Legal live physical target required')
        require(s.original_cells and s.transformed_cells,'Both individually legal footprints required')
        ends_own_concentration=bool(old and old.state=='shaping' and self.casts[old.cast_id].caster==caster)
        active_transformed_object=bool(old and old.profile is None and self.casts[old.cast_id].spell_id=='true-polymorph')
        # Validate target anatomy after the mandatory end of own concentration.
        creature=b.origin.kind=='creature' if ends_own_concentration else self._current_creature(b)
        if spell_id!='true-polymorph':require(creature,'This spell requires creature anatomy')
        if spell_id=='shapechange':require(s.target==caster and s.willing,'Shapechange is self only')
        if old and not ends_own_concentration:
            if old.state=='permanent':
                require(spell_id=='true-polymorph','Permanent True anatomy requires a new True Polymorph')
            else:require(rank>=self.casts[old.cast_id].rank,'New rank cannot replace higher-rank anatomy')
        if s.profile is not None:
            require(s.profile in PROFILES,'Unknown finite spell profile')
            p=PROFILES[s.profile]
            require(spell_id not in ('polymorph','mass-polymorph') or p['tier']=='R4','R9 profile unavailable')
            require(b.origin.kind!='object' or s.profile!='spellform.humanoid','Object origin cannot gain humanoid profile')
        else:
            require(spell_id=='true-polymorph' and (not (creature or b.origin.kind=='creature') or s.willing),
                    'Object output requires True and willingness of a retained creature-origin person')
            require(s.object_template in TEMPLATES and s.mundane_output_certified,'Bounded inert mundane template required')
            input_size=b.origin.size if ends_own_concentration else b.size
            input_mass=b.origin.mass if ends_own_concentration else b.mass
            require(s.object_size in SIZES[:4] and abs(SIZES.index(s.object_size)-SIZES.index(input_size))<=1,'Object output size illegal')
            require(input_mass is not None and b.origin.mass is not None,'Canonical current/origin mass required')
            integer(s.object_mass,'output mass',1,min(input_mass,b.origin.mass))
            if b.origin.kind=='object':
                require(b.origin.value is not None,'Original documented value required')
                integer(s.object_value,'output value',0,b.origin.value)
            else:require(s.object_value==0,'Creature body has no independent recoverable/sale value')
        if not creature:
            require(spell_id=='true-polymorph' and (active_transformed_object or s.object_input_eligible),
                    'Fresh outside objects require eligibility; an active True object record uses legal replacement')
        if b.origin.kind=='object' and s.profile is not None:
            sponsor=caster if ends_own_concentration else b.slot_sponsor or caster
            occupant=self.slots.get(sponsor)
            occupied_link=self.current(occupant) if occupant is not None else None
            freed_by_commit=bool(occupied_link and occupied_link.state=='shaping' and self.casts[occupied_link.cast_id].caster==caster)
            require(occupant in (None,b.identity) or freed_by_commit,'Original caster object-creature slot occupied')
        return b

    def cast(self,cast_id,spell_id,stats,price,wallet,selections,now,regular_index,*,legal,resolve_save,countered=False):
        """resolve_save(target, DC) executes only AFTER committed payment.

        It returns True on success (or an exact legendary defense); False on
        failure. Caller must provide a nonthrowing authoritative resolver. All
        actual die rolls/target condition legality remain in the combat engine.
        """
        identity(cast_id);integer(now,'cast timestamp',0);integer(regular_index,'original regular index',0)
        require(legal and spell_id in SPELLS and price.spell_id==spell_id and price.rank==SPELLS[spell_id],'Legal canonical quote/access required')
        require(cast_id not in self.casts and cast_id not in self.buffers.form_instances,'Cast identity already used')
        require(len(selections)==1 or spell_id=='mass-polymorph','Single-target spell')
        if spell_id=='mass-polymorph':validate_mass_space(selections)
        else:require(len(selections)==1,'Exactly one target required')
        for s in selections:
            self._validate_selection(spell_id,price.rank,s,stats.owner)
            require(cast_id+':'+s.target not in self.buffers.form_instances,'World form/link identity already used')
        wallet.validate(rp=price.total,action='action')
        # All potentially invalid requests rejected above. No refunds below.
        wallet.pay(rp=price.total,action='action')
        record=Cast(cast_id,spell_id,stats.owner,price.rank,stats,regular_index)
        self.casts[cast_id]=record;self.buffers.form_instances.add(cast_id)
        self.concentration.start_committed(stats.owner,cast_id,lambda reason:self._end_cast(cast_id,reason))
        if countered:
            record.state='countered';self.concentration.detach(stats.owner,cast_id)
            return {'castId':cast_id,'links':[],'paidRP':price.total,'countered':True,'cadenceQuote':deepcopy(price.quote)}
        successful=[]
        for s in selections:
            body=self.bodies[s.target]
            # Object anatomy never strips a retained creature-origin person's
            # save. Object-origin creature targets retain normal current-form saves.
            needs_save=(self._current_creature(body) or body.origin.kind=='creature') and not s.willing
            if not needs_save or not resolve_save(s.target,stats.dc):successful.append(s)
        # Choices are fixed before rolling; no sequential geometry re-evaluation.
        for s in successful:self._apply(record,s,now)
        record.state='active' if record.links else 'no-target-links'
        if not record.links:self.concentration.detach(stats.owner,cast_id)
        return {'castId':cast_id,'links':list(record.links),'paidRP':price.total,'countered':False,'cadenceQuote':deepcopy(price.quote)}

    def _apply(self,record,s,now):
        b=self.bodies[s.target]
        old=self.current(s.target)
        if old:self._end_link(old,'replaced',continuous=True)
        druid=self.druids.get(s.target)
        if druid and druid.current:druid._end('spell-transformation')
        link_id=record.identity+':'+s.target
        link=Link(link_id,record.identity,s.target,s.profile,s.willing,now+60,
                  object_template=s.object_template,object_size=s.object_size,object_mass=s.object_mass)
        self.links[link_id]=link;record.links.append(link_id);self.buffers.form_instances.add(link_id)
        b.anatomy=link_id
        self.buffers.spell_anatomies[b.identity]=link_id
        b.placement_pending=False;b.placement_conflict=False
        # Close-and-recapture: old record restores still-existing meld items,
        # then this new record captures them without an intervening action window.
        b.melded.update(b.equipment);b.equipment.clear()
        b.size=PROFILES[s.profile]['size'] if s.profile else s.object_size
        if s.profile is None:b.mass=s.object_mass
        if b.origin.kind=='object' and s.profile:
            if b.slot_sponsor is None:b.slot_sponsor=record.caster;b.controller=record.caster
            self.slots[b.slot_sponsor]=b.identity
        elif b.slot_sponsor:self._release_slot(b)

    def _release_slot(self,b):
        if b.slot_sponsor and self.slots.get(b.slot_sponsor)==b.identity:del self.slots[b.slot_sponsor]
        b.slot_sponsor=None

    def _end_link(self,link,reason,*,continuous=False):
        if link.state not in ('shaping','permanent'):return
        b=self.bodies[link.target];record=self.casts[link.cast_id]
        link.state=reason
        if b.anatomy==link.identity:b.anatomy=None
        if self.buffers.spell_anatomies.get(b.identity)==link.identity:
            del self.buffers.spell_anatomies[b.identity]
        self.buffers.end_dependency(link.identity)
        b.equipment.update(b.melded-b.lost_items);b.melded.clear()
        b.size=b.origin.size;b.mass=b.origin.mass
        if not continuous:self._release_slot(b)
        if not continuous:
            b.placement_pending=True
            self.events.append({'target':b.identity,'reason':reason,'sameSpatialAnchor':True,
                                'placementCheckRequired':True,'noHealingOrAutomaticMovement':True})
        if not any(self.links[i].state=='shaping' for i in record.links):
            self.concentration.detach(record.caster,record.identity)

    def _end_cast(self,cast_id,reason):
        record=self.casts[cast_id]
        for ident in record.links:
            link=self.links[ident]
            if link.state=='shaping':self._end_link(link,reason)
        record.state=reason

    def _active(self,target,now,*,allow_boundary=False,allow_suppressed=False):
        link=self.current(target)
        require(link is not None and link.state in ('shaping','permanent'),'No operative spell anatomy')
        require(allow_suppressed or not link.suppressed,'Anatomy is currently suppressed')
        if link.state=='shaping':
            require(now<=link.deadline if allow_boundary else now<link.deadline,'Resolve actual60-second checkpoint first')
        return link

    def repeat_save(self,target,stats,now,*,trigger,event_or_turn,round_number=None,normal_hp_damage=0,success):
        link=self._active(target,now,allow_boundary=True,allow_suppressed=True);record=self.casts[link.cast_id]
        require(link.state=='shaping' and not link.willing and link.profile is not None,'No hostile repeat-save permission')
        require(stats.owner==record.caster,'Original caster statistics required')
        identity(event_or_turn)
        if trigger=='regular-end':
            key=(target,event_or_turn)
            require(key not in self.regular_ends,'Original regular endpoint already handled')
            self.regular_ends.add(key)
        elif trigger=='damage':
            integer(normal_hp_damage,'actual normal HP damage',1);integer(round_number,'numbered round',1)
            key=(target,round_number)
            require(key not in self.damage_rounds,'First positive HP damage repeat already used this round')
            require((target,event_or_turn) not in self.damage_events,'Damage event already processed')
            self.damage_rounds.add(key)
            self.damage_events.add((target,event_or_turn))
        else:raise SpellRuleError('Only actual original regular end or first positive normal-HP damage')
        dc=record.stats.dc if record.spell_id=='true-polymorph' else stats.dc
        if success:self._end_link(link,'repeat-save')
        return {'dc':dc,'ended':bool(success),'target':target}

    def checkpoint(self,now,*,started_packets_and_due_saves_finished):
        integer(now,'absolute checkpoint',0)
        require(started_packets_and_due_saves_finished,'Finish packets and due repeat saves before checkpoint')
        result=[]
        for link in self.links.values():
            if link.state!='shaping' or now<link.deadline:continue
            record=self.casts[link.cast_id]
            if record.spell_id=='true-polymorph':
                link.state='permanent';self.concentration.detach(record.caster,record.identity)
                result.append({'link':link.identity,'state':'permanent'})
            else:
                self._end_link(link,'expired');result.append({'link':link.identity,'state':'expired'})
        return result

    def reject(self,target,now,wallet,*,actual_regular_turn,legal):
        link=self._active(target,now,allow_suppressed=True);record=self.casts[link.cast_id];b=self.bodies[target]
        action_capable=(not link.suppressed and link.profile is not None) or (link.suppressed and b.origin.kind=='creature')
        require(link.state=='shaping' and link.willing and b.origin.kind=='creature' and action_capable and legal and actual_regular_turn,
                'Only a willing temporary creature-origin recipient with expressed action-capable anatomy may reject')
        require(record.spell_id!='shapechange','Shapechange uses ordinary concentration release')
        wallet.validate(action='action');wallet.pay(action='action');self._end_link(link,'willing-rejection')

    def finalize_damage_state(self,target,*,actual_hp,incapacitated,dead,destroyed=False,unsupported=False):
        """After Core damage and ALL same-packet replacement/prevention. No reroll."""
        integer(actual_hp,'actual final HP',0);b=self.bodies[target];link=self.current(target)
        recorded_hp=b.life.get('hp') if isinstance(b.life,dict) else b.life.hp
        require(recorded_hp==actual_hp,'Project the actual finalized canonical HP ledger before anatomy cleanup')
        if b.origin.kind=='object' and actual_hp==0:
            b.destroyed=True
            if link:self._end_link(link,'physical-destruction')
        elif destroyed:
            b.destroyed=True
            if link and link.state=='shaping':self._end_link(link,'physical-destruction')
        elif link and link.state=='shaping' and (actual_hp==0 or incapacitated or dead):self._end_link(link,'forced-reversion')
        return {'sameHPLedger':b.life,'beginOrdinaryFall':bool(unsupported),'secondDamageResolution':False}

    def check_reversion_placement(self,target,*,fits_at_current_anchor):
        b=self.bodies[target]
        require(b.placement_pending,'No pending root-anatomy placement check')
        b.placement_pending=False;b.placement_conflict=not fits_at_current_anchor
        return {'placementConflict':b.placement_conflict,'sameSpatialAnchor':True,
                'requiresCanonicalGeometryResolution':b.placement_conflict,'automaticDamage':0,'automaticRelocation':False}

    def clear_geometry_conflict(self,target,*,canonical_resolution_completed):
        require(canonical_resolution_completed,'Actual canonical geometry resolution required')
        self.bodies[target].placement_pending=False;self.bodies[target].placement_conflict=False

    def dispel(self,target,*,legal):
        require(legal and self.current(target) is not None,'Actual successful dispel required')
        self._end_link(self.current(target),'dispelled')

    def set_suppressed(self,target,now,*,suppressed,legal):
        link=self._active(target,now,allow_suppressed=True);b=self.bodies[target]
        require(legal and link.suppressed!=suppressed,'Actual changed antimagic state required')
        link.suppressed=bool(suppressed)
        b.size=b.origin.size if suppressed else PROFILES[link.profile]['size'] if link.profile else link.object_size
        b.mass=b.origin.mass if suppressed or link.profile else link.object_mass
        # No gear recapture, slot release, benefit entry, HP change or clock reset.
        b.placement_pending=True
        return {'sameRecord':link.identity,'deadline':link.deadline,'placementCheckRequired':True,
                'sameMeldSet':frozenset(b.melded),'slotSponsor':b.slot_sponsor}

    def _stats_for(self,link,stats):
        record=self.casts[link.cast_id]
        require(isinstance(stats,CastStats) and stats.owner==record.caster,'Use original caster statistics')
        return record.stats if record.spell_id=='true-polymorph' else stats

    def profile(self,target,stats,now,form_normal_ac,*,ac_components_certified):
        link=self._active(target,now);b=self.bodies[target]
        require(not b.placement_pending and not b.placement_conflict,'Resolve physical placement before movement/targeting')
        integer(form_normal_ac,'operative form normal AC',0)
        require(ac_components_certified,'Exclude melded armor/shield; certify compatible passives/external equipment')
        types=sorted(b.origin.type_tags) if b.origin.kind=='creature' else ['transformed-object']
        if link.profile is None:
            return {'ac':12,'size':link.object_size,'movement':{},'speech':False,'hands':False,
                    'ordinarySenses':False,'actions':False,'bonusActions':False,'reactions':False,
                    'actionlessObjectAnatomy':True,'appliesIncapacitated':False,'targetKind':'object',
                    'originTypeTags':types,'grantedResistances':[],'sameHPLedger':b.life}
        p=deepcopy(PROFILES[link.profile]);mode=p['ac']['mode'];amount=p['ac']['amount']
        p['ac']=form_normal_ac if mode=='normal' else max(form_normal_ac,amount) if mode=='floor' else amount
        provider=self._stats_for(link,stats)
        p['attack'].update({'attack':provider.attack,'modifier':provider.modifier,'reachFeet':5,
                            'attacker':target,'statProvider':provider.owner,'spellcast':False,
                            'directCasterSpellDamage':False,'sourceSpell':self.casts[link.cast_id].spell_id,
                            'sourceLink':link.identity})
        p.update({'targetKind':'creature','typeTags':types,'sameHPLedger':b.life,'ordinarySenses':True,
                  'grantsSpecialSenses':False,'grantsResources':False,'grantsMultiattack':False})
        if b.origin.kind=='object':p.update({'saves':provider.pb,'ordinaryChecks':0,'soul':False,
            'wounds':False,'deathSaves':False,'resurrection':False,'ordinaryHealing':False,
            'companionPhase':'attached','uncommanded':['move','Dodge']})
        return p

    def healing_target_eligible(self,target,*,native_eligible):
        b=self.bodies[target]
        return bool(native_eligible and not b.destroyed and b.origin.kind=='creature' and self._current_creature(b))

    def acquire_external_gear(self,target,item_id,now,*,compatible_and_equipped):
        link=self._active(target,now);b=self.bodies[target];identity(item_id)
        require(link.profile is not None and PROFILES[link.profile]['hands'] and compatible_and_equipped,
                'Actual compatible external equipment required')
        require(item_id not in b.melded and item_id not in b.equipment and item_id not in b.lost_items,'Item identity unavailable/already recorded')
        b.equipment.add(item_id)

    def mark_item_lost(self,target,item_id,*,actual_loss):
        require(actual_loss,'Actual destroyed/consumed/lost item event required')
        b=self.bodies[target];require(item_id in b.melded or item_id in b.equipment,'Unknown held/melded item')
        b.equipment.discard(item_id);b.melded.discard(item_id);b.lost_items.add(item_id)

    def switch_shapechange(self,target,profile,now,regular_index,wallet,*,original_regular_turn,legal,retained_gear,drop_placement_legal,unsupported=False):
        link=self._active(target,now);record=self.casts[link.cast_id];b=self.bodies[target]
        require(record.spell_id=='shapechange' and record.caster==target,'Only actual self Shapechange may switch')
        require(original_regular_turn and regular_index>record.casting_regular_index and regular_index!=link.last_switch,
                'Switch once on a later original regular turn only')
        require(profile in PROFILES and profile!=link.profile and legal,'Different legal finite profile required')
        require(b.origin.kind!='object' or profile!='spellform.humanoid','Object-origin humanoid prohibited')
        keep=set(retained_gear)
        require(keep<=b.equipment and (not keep or PROFILES[profile]['hands']),'Only certified anatomy-compatible external gear may remain')
        dropped=b.equipment-keep
        require(not dropped or drop_placement_legal,'Resolve legal current/nearest adjacent item placement before switch')
        wallet.validate(action='bonus');wallet.pay(action='bonus')
        b.equipment=keep;link.profile=profile;link.last_switch=regular_index;b.size=PROFILES[profile]['size']
        return {'sameRecord':link.identity,'droppedItemIds':sorted(dropped),'spellcast':False,'paidRP':0,
                'refrainEvent':False,'beginOrdinaryFall':bool(unsupported and not PROFILES[profile]['movement'].get('fly'))}

    def attack(self,target,stats,now,wallet,*,legal):
        link=self._active(target,now);b=self.bodies[target]
        require(legal and b.origin.kind=='creature' and link.profile is not None,'Legal subject natural attack required; object companions use command adapter')
        require(not b.placement_pending and not b.placement_conflict,'Unresolved placement cannot authorize targeting')
        provider=self._stats_for(link,stats)
        wallet.validate(action='action');wallet.pay(action='action')
        return self._attack_packet(link,provider)

    def _attack_packet(self,link,provider):
        attack=deepcopy(PROFILES[link.profile]['attack'])
        attack.update({'reachFeet':5,'attacker':link.target,'statProvider':provider.owner,'attack':provider.attack,
                       'modifier':provider.modifier,'sourceSpell':self.casts[link.cast_id].spell_id,
                       'sourceLink':link.identity,'spellcast':False,'directCasterSpellDamage':False,
                       'importsMultiattack':False,'weaponOnlyFeaturesAuthorized':False})
        return attack

    def command(self,target,order_id,now,round_number,ledger,wallet,*,mode,legal,distance,owner_perceives):
        link=self._active(target,now);b=self.bodies[target];identity(order_id)
        require(b.origin.kind=='object' and link.profile is not None and b.slot_sponsor is not None,'Active object-origin creature required')
        require(isinstance(ledger,CommandLedger) and ledger.owner==b.controller,'Current controller canonical shared command ledger required')
        require(not b.placement_pending and not b.placement_conflict,'Resolve placement before issuing a command')
        require(legal and owner_perceives and 0<=distance<=60,'Actual60-foot command legality required')
        require(mode in ('support','attack','control') and order_id not in self.commands,'Fresh supported command required')
        ledger.activate(round_number,mode,wallet)
        self.commands[order_id]={'target':target,'link':link.identity,'controller':b.controller,'mode':mode,'resolved':False}
        return {'orderId':order_id,'phase':'attached','independentTurn':False}

    def resolve_command(self,order_id,stats,now,*,attached_phase,still_legal):
        order=self.commands.get(order_id)
        require(order is not None and not order['resolved'] and attached_phase,'Actual unresolved attached command required')
        b=self.bodies[order['target']];link=self.current(b.identity)
        order['resolved']=True
        if (not still_legal or not link or link.identity!=order['link'] or link.suppressed
            or b.controller!=order['controller'] or b.destroyed or b.placement_pending or b.placement_conflict
            or (link.state=='shaping' and now>=link.deadline)):
            return {'executed':False,'refunded':False}
        self._active(b.identity,now)
        if order['mode']=='attack':return {'executed':True,'attack':self._attack_packet(link,self._stats_for(link,stats))}
        return {'executed':True,'mode':order['mode'],'damageAuthorized':False,'profileGrantsNoExtraControlPower':True}

    def uncommanded(self,target,now):
        link=self._active(target,now);b=self.bodies[target]
        require(b.origin.kind=='object' and link.profile is not None,'Actual object companion required')
        return {'options':['move','Dodge'],'damageAuthorized':False,'independentTurn':False}
