# Transformation correction review, then eight exact feat sources

## First: independently review the two actual corrections

Your full implementation findings are preserved as GPT_TRANSFORMATION_SPELL_IMPLEMENTATION_FINDINGS.md. Neither blocker was ignored or promoted. Both are corrected in the actual code below;191 existing checks now become216 with25 explicit regressions, and all729 Mass occupancy scenarios still pass. Source objects/class access/frozen class rules remain unchanged. The previously tested Druid guard and its165/1053 regression result are unchanged by this correction.

Blocker1 correction: preflight recognizes an active True object anatomy as an existing transformation record, so a legal True replacement does not require a false fresh-outside-object certificate. Genuinely fresh outside objects still require it. Creature-origin identity now retains its initial CON save against an unwilling creature-profile replacement even while expressed as an object. Object-output replacement of that person requires willingness. Object-origin identities retain all restrictions and slot behavior. Tests cover both save success/failure, unwilling/willing object replacement, original HP identity, no new companion slot for a person, and object-origin object recasting into a fresh companion manifestation.

Blocker2 correction: reject() admits suppressed links, then checks current expressed action capability and creature origin. Willing Polymorph/Mass/shaping-True recipients can spend their original regular-turn Action while root creature anatomy is expressed under suppression, including a suppressed creature→object form. Unsuppressed object anatomy stays actionless. Object-origin identities receive no player-style rejection. Shapechange continues to use concentration release and cannot internally switch while suppressed. Tests cover each case and registry cleanup.

The guide and candidate cards also explicitly preserve your six dispositions: projected-root preflight, sponsor/control separation, inaccessible original meld set under suppression, no suppressed internal Shapechange switch, same-anchor geometry handoff and no generic magical-attack bypass flag. The wider geometry/item/attack-taxonomy/runtime/balance/human-playtest dependencies remain open.

Please inspect the actual corrections and regressions, then state whether these FIVE bounded spells and12 profiles are REVIEWED / reference-VALIDATED for provisional catalog promotion, or identify any remaining reproducible blocker. Do not imply the wider catalogs or game are complete. We have not promoted these candidates yet.

## Second, only if the five-spell corrections close

Continue our user-authorized comprehensive game development by discussing the eight EXACT full-feat sources appended after the implementation. Those feats are the next named incomplete clauses from our buffer audit. This is source discussion and candidate design only, not feat promotion or implementation approval. If a transformation blocker remains, prioritize that finding and defer the feat conference until corrected.

## Corrected implementation manifest

[
  {
    "path": "tools/transformation_spell_playtest_rules.py",
    "sha256": "91697863f6d19043787e17f19b4c127e6c32de32ad3867393566212533081d39"
  },
  {
    "path": "tools/validate_transformation_spell_playtests.py",
    "sha256": "bce50db7956e858c9737336861b79859bff487bf0e9902547ea6d452709cf80c"
  },
  {
    "path": "docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md",
    "sha256": "db26d420684f6dac8daac4b927fbd930e25c313056e2e3581376df34d57238de"
  },
  {
    "path": "data/playtest/spell_drafts/candidate_transformations.json",
    "sha256": "791c4ade6a88319c7130dc4c80df237595a0e1ebc24102d7f25d8c66d02b35eb"
  },
  {
    "path": "data/playtest/spell_form_profiles.json",
    "sha256": "1a6692722b635d3cee1205cfd1eff10118e01696c4505b817b8c3b6cc5f0a2a7"
  },
  {
    "path": "docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json",
    "sha256": "022a461cd1d0f87a20013eb22550d380bde69ab517c4f7244501e4a45da66f46"
  }
]

## tools/transformation_spell_playtest_rules.py

```python
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

```

## tools/validate_transformation_spell_playtests.py

```python
"""Adversarial candidate contract scenarios, not balance or complete runtime tests."""
from dataclasses import replace
from pathlib import Path
from itertools import product
from copy import deepcopy
import json, hashlib
from transformation_spell_playtest_rules import *
from spell_playtest_rules import quote_cast, access_for
from core_playtest_rules import LifeState
from form_temphp_playtest_rules import DruidState, DruidStats

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
sources=json.loads((AUDIT/'TRANSFORMATION_SPELL_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
fixtures={s['id']:deepcopy(s['wholeOverlaySnapshot']) for s in sources['spells']}
for f in fixtures.values():f['status']='operational-playtest-draft'  # in-memory candidate fixture only
checks=0

def check(value,label):
    global checks
    assert value,label
    checks+=1

def rejects(fn,label):
    try:fn()
    except SpellRuleError:check(True,label)
    else:raise AssertionError(label)

def stats(owner='a',attack=10,dc=18,pb=6,modifier=4):return CastStats(owner,'Wizard',attack,dc,pb,modifier)

def price(spell,*,paid=None,surcharge=False):
    q=quote_cast(fixtures[spell],'Wizard',20,available_spell_ids={spell},rp=100,max_rp=100,
                 dissonance=12 if surcharge else 0,proficiency=6,casting_modifier=4)
    return CastPrice.from_quote(q,actual_base_paid=paid,exact_reduction_authorized=paid is not None)

def world(ids=('a','b','c'),objects=()):
    w=TransformationWorld(BufferLedger(),ConcentrationLedger())
    for ident in ids+tuple(objects):
        obj=ident in objects
        origin=PhysicalOrigin(ident,'object' if obj else 'creature','Medium',frozenset() if obj else frozenset({'humanoid'}),100,20 if obj else None)
        life={'hp':20,'maximum_hp':20} if obj else LifeState(40,31,wounds=(None,))
        w.add_body(Body(origin,life,'Medium',100,equipment=set() if obj else {ident+':coat'}))
    return w

def select(target='b',profile='spellform.predator',willing=True,cell=None,**kwargs):
    return Selection(target,profile,willing,frozenset({cell or target}),frozenset({cell or target}),True,**kwargs)

def cast(w,spell='polymorph',target='b',profile='spellform.predator',*,ident='cast',owner='a',now=0,index=1,willing=True,selections=None,save=False,countered=False,wallet=None,**selection_options):
    return w.cast(ident,spell,stats(owner),price(spell),wallet or Wallet(rp=100),
                  selections or [select(target,profile,willing,**selection_options)],now,index,
                  legal=True,resolve_save=lambda target,dc:save,countered=countered)

def main():
    global checks
    # Actual class gates/price rows, tested through the ordinary cast pricer.
    for spell,f in fixtures.items():
        for cls,a in f['classAccess'].items():
            check(access_for(f,cls,a['minimumClassLevel'])==a,spell+' actual class gate')
            if a['minimumClassLevel']>1:rejects(lambda:access_for(f,cls,a['minimumClassLevel']-1),'Underlevel rejected')
            q=quote_cast(f,cls,20,available_spell_ids={spell},rp=100,max_rp=100,dissonance=0,proficiency=6,casting_modifier=4)
            check(q['baseRpCost']==a['baseRpCost'] and q['rank']==a['rank'],'Preserved class-specific price/rank')
        rejects(lambda:quote_cast(f,'Wizard',20,available_spell_ids=set(),rp=100,max_rp=100,dissonance=0,proficiency=6,casting_modifier=4),'Known/prepared gate remains')
    b=BufferLedger();w=Wallet(rp=100)
    result=harmonic_bulwark(b,stats(),price('harmonic-bulwark',paid=3,surcharge=True),w,'h1','b',2,0,legal=True)
    check(result['creditedRP']==5 and b.amount('b')==25 and result['paidRP']==6,'Base discount+X+surcharge credit separation')
    check(w.rp==94 and w.actions==0,'All actual RP and Action committed')
    w=Wallet(rp=100);harmonic_bulwark(b,stats(),price('harmonic-bulwark'),w,'h2','b',0,0,legal=True)
    check(b.current('b').grant_id=='h1' and w.rp==95,'Equal shield retains original after payment')
    w=Wallet(rp=6);rejects(lambda:harmonic_bulwark(b,stats(),price('harmonic-bulwark'),w,'bad','b',2,0,legal=True),'Cannot pay full transaction')
    check(w.rp==6 and w.actions==1,'Invalid transaction spends nothing')
    rejects(lambda:harmonic_bulwark(b,stats(),price('harmonic-bulwark',paid=0),Wallet(rp=10),'free','b',0,0,legal=True),'Zero credit blocked')
    r=harmonic_bulwark(b,stats(),price('harmonic-bulwark',paid=0),Wallet(rp=10),'convert','c',2,0,legal=True)
    check(r['paidRP']==2 and b.amount('c')==10,'Free base plus paid X valid')
    w=Wallet(rp=100);r=harmonic_bulwark(b,stats(),price('harmonic-bulwark'),w,'counter','c',3,0,legal=True,countered=True)
    check(w.rp==92 and r['offer'] is None and b.amount('c')==10,'Counter spends base and X but offers no shield')
    rejects(lambda:harmonic_bulwark(b,stats(),price('harmonic-bulwark'),Wallet(rp=100),'counter','c',3,0,legal=True),'Countered ID cannot replay')
    b.completed_long_rest('c',1);check(b.amount('c')==0,'Recipient long-rest clock')

    # Same-source concentration ends at commit; another source ends on success.
    w=world();cast(w,'mass-polymorph',selections=[select('b'),select('c')],ident='mass')
    order=[];wallet=Wallet(rp=100)
    def saves(target,dc):
        order.append((target,w.current('b'),w.current('c'),wallet.rp,wallet.actions));return True
    w.cast('next','polymorph',stats(),price('polymorph'),wallet,[select('b',willing=False)],1,2,legal=True,resolve_save=saves)
    check(order[0][1:]==(None,None,93,0),'Old Mass ends and full payment precedes save')
    check(w.current('b') is None and 'a' not in w.concentration.current,'Save never restores old concentration')
    w=world();cast(w,ident='old');cast(w,ident='failed-other',owner='c',willing=False,save=True)
    check(w.current('b').cast_id=='old','Other caster failed replacement leaves anatomy')
    cast(w,ident='new-other',owner='c');check(w.current('b').cast_id=='new-other' and w.links['old:b'].state=='replaced','Success replaces exactly one record')
    w.concentration.end('c','actual-failed-check');check(w.current('b') is None,'Old form does not reappear')
    w=world();cast(w,ident='old');cast(w,ident='countered',countered=True)
    check(w.current('b') is None,'Countered new own concentration still ends old')
    w=world();cast(w,'shapechange',target='a',ident='high')
    rejects(lambda:cast(w,target='a',owner='c',ident='low'),'Other lower rank cannot overwrite')
    cast(w,target='a',owner='a',ident='ownlower');check(w.current('a').cast_id=='ownlower','Own old concentration ends before lower-rank application')

    # Profiles and ownership of actual attack events.
    w=world();life=w.bodies['b'].life;cast(w)
    attack=w.attack('b',stats(attack=12,modifier=5),1,Wallet(),legal=True)
    check((attack['attacker'],attack['statProvider'],attack['attack'],attack['modifier'])==('b','a',12,5),'Current caster stats, subject event ownership')
    check(not attack['spellcast'] and not attack['directCasterSpellDamage'] and not attack['weaponOnlyFeaturesAuthorized'],'No spellcast/caster/weapon trigger laundering')
    check(w.bodies['b'].life is life and life.hp==31 and life.wounds==(None,),'Same HP/Wounds object retained')
    p=w.profile('b',stats(),1,12,ac_components_certified=True)
    check(p['typeTags']==['humanoid'] and p['ac']==13 and not p['grantsMultiattack'],'Original type; selected AC; no Multiattack')
    rejects(lambda:w.profile('b',stats(),1,20,ac_components_certified=False),'Melded AC cannot silently apply')
    for profile,p in PROFILES.items():
        t=world();cast(t,'true-polymorph',profile=profile)
        row=t.profile('b',stats(attack=20,modifier=10),1,12,ac_components_certified=True)
        check(row['attack']['attack']==10 and row['attack']['modifier']==4 and row['attack']['reachFeet']==5,profile+' True snapshots and reach')
    w=world();cast(w,'true-polymorph');w.checkpoint(60,started_packets_and_due_saves_finished=True)
    check(w.current('b').state=='permanent' and not w.concentration.current,'True stable, concentration released')
    rejects(lambda:cast(w,owner='c',ident='ordinary'),'Ordinary spell cannot overwrite permanence')
    cast(w,'true-polymorph',owner='c',ident='newtrue');w.concentration.end('c','release')
    check(w.current('b') is None,'New True has no hidden old permanent record')

    # Hostile saves, damage rounds and final timestamp ordering.
    w=world();cast(w,willing=False)
    rejects(lambda:w.repeat_save('b',stats(),1,trigger='damage',event_or_turn='hp0',round_number=1,normal_hp_damage=0,success=False),'Temporary-HP-only loss gives no repeat')
    r=w.repeat_save('b',stats(dc=20),1,trigger='damage',event_or_turn='hit',round_number=1,normal_hp_damage=2,success=False)
    check(r['dc']==20,'Polymorph repeat uses current DC')
    rejects(lambda:w.repeat_save('b',stats(),2,trigger='damage',event_or_turn='hit2',round_number=1,normal_hp_damage=2,success=False),'One positive damage repeat per numbered round')
    rejects(lambda:w.repeat_save('b',stats(),2,trigger='damage',event_or_turn='hit',round_number=2,normal_hp_damage=2,success=False),'No cross-round event replay')
    w.repeat_save('b',stats(),6,trigger='regular-end',event_or_turn='turn1',success=False)
    rejects(lambda:w.repeat_save('b',stats(),6,trigger='regular-end',event_or_turn='turn1',success=False),'No extra-turn/repeated regular endpoint')
    w=world();cast(w,'true-polymorph',willing=False)
    r=w.repeat_save('b',stats(dc=25),60,trigger='regular-end',event_or_turn='last',success=True)
    w.checkpoint(60,started_packets_and_due_saves_finished=True)
    check(r['dc']==18 and w.current('b') is None,'True snapshot final save prevents stabilization')
    w=world();cast(w);rejects(lambda:w.checkpoint(60,started_packets_and_due_saves_finished=False),'Cannot stabilize/expire before pending packet/saves')
    rejects(lambda:w.attack('b',stats(),60,Wallet(),legal=True),'No actions past unresolved deadline')
    w.checkpoint(60,started_packets_and_due_saves_finished=True);check(w.current('b') is None,'Exact60-second temporary expiry')
    w=world();cast(w);rejects(lambda:w.repeat_save('b',stats(),1,trigger='regular-end',event_or_turn='willing',success=True),'Willing waiver does not become hostile repeat')
    wallet=Wallet();w.reject('b',1,wallet,actual_regular_turn=True,legal=True)
    check(wallet.actions==0 and w.current('b') is None,'Willing temporary rejection pays Action')

    # True object anatomy, immutable origins, sponsor and commands.
    objargs=dict(object_template='open-container',object_size='Medium',object_mass=80,object_value=0,mundane_output_certified=True)
    w=world();cast(w,'true-polymorph',target='a',profile=None,**objargs)
    p=w.profile('a',stats(),1,12,ac_components_certified=True)
    check(p['actionlessObjectAnatomy'] and not p['appliesIncapacitated'] and 'a' in w.concentration.current,'Self object can concentrate while actionless')
    check(not w.healing_target_eligible('a',native_eligible=True),'Creature-origin object cannot be newly healed as creature')
    rejects(lambda:w.reject('a',1,Wallet(),actual_regular_turn=True,legal=True),'Object anatomy cannot pay rejection Action')
    w.bodies['a'].life=replace(w.bodies['a'].life,hp=0)
    w.finalize_damage_state('a',actual_hp=0,incapacitated=False,dead=False)
    check(w.current('a') is None,'Actual0 ends object shaping even if not incapacitated')
    w=world();cast(w,'true-polymorph',profile=None,**objargs);w.checkpoint(60,started_packets_and_due_saves_finished=True)
    w.bodies['b'].life=replace(w.bodies['b'].life,hp=0,dead=True)
    w.finalize_damage_state('b',actual_hp=0,incapacitated=True,dead=True)
    check(w.current('b').state=='permanent','Permanent creature-origin object does not auto-revert at death')
    w.dispel('b',legal=True);check(w.bodies['b'].life.hp==0 and w.bodies['b'].life.dead,'Dispel retains actual dead HP state without healing')
    # Input lives below are structural dictionaries, never creature death ledgers.
    w=world(objects=('o','p'));cast(w,'true-polymorph',target='o',object_input_eligible=True)
    check(w.slots=={'a':'o'} and not w.healing_target_eligible('o',native_eligible=True),'Slot reserved during shaping; no ordinary healing')
    p=w.profile('o',stats(),1,10,ac_components_certified=True)
    check(p['typeTags']==['transformed-object'] and p['saves']==6 and not p['deathSaves'] and not p['soul'],'Object origin baseline and saves')
    rejects(lambda:cast(w,'true-polymorph',target='o',profile='spellform.humanoid',owner='c',ident='launder'),'Origin survives cross-caster humanoid laundering')
    cast(w,'true-polymorph',target='p',object_input_eligible=True,ident='second-shaping')
    check(w.slots=={'a':'p'} and w.current('o') is None,'Own concentration replacement releases shaping slot before new creation')
    w.checkpoint(60,started_packets_and_due_saves_finished=True)
    wallet=Wallet(rp=100)
    rejects(lambda:cast(w,'true-polymorph',target='o',object_input_eligible=True,ident='army',wallet=wallet),'Permanent slot blocks second distinct creature')
    check(wallet.rp==100 and wallet.actions==1,'Occupied permanent slot rejected before payment')
    cast(w,'true-polymorph',target='p',owner='c',ident='other')
    check(w.slots=={'a':'p'} and w.bodies['p'].controller=='a','Other caster recast preserves sponsor and controller')
    ledger=CommandLedger('a');wallet=Wallet()
    rejects(lambda:w.attack('p',stats('c'),1,Wallet(),legal=True),'Object creature cannot take independent attack turn')
    w.command('p','order',1,1,ledger,wallet,mode='attack',legal=True,distance=60,owner_perceives=True)
    r=w.resolve_command('order',stats('c'),1,attached_phase=True,still_legal=True)
    check(not wallet.bonus_action and r['attack']['attacker']=='p' and r['attack']['statProvider']=='c','Owner BA, attached subject attack, new caster stat snapshot')
    rejects(lambda:ledger.activate(1,'attack',Wallet()),'No second companion offensive/command allowance')
    rejects(lambda:w.resolve_command('order',stats('c'),1,attached_phase=True,still_legal=True),'No command replay')
    check(w.uncommanded('p',1)['options']==['move','Dodge'],'Uncommanded defense only')
    w.bodies['p'].life['hp']=0
    w.finalize_damage_state('p',actual_hp=0,incapacitated=False,dead=False)
    check(w.bodies['p'].destroyed and not w.slots and w.current('p') is None,'Structural0 destroys manifestation and frees slot')
    rejects(lambda:cast(w,'true-polymorph',target='p',object_input_eligible=True,ident='resurrect'),'Destroyed object cannot be reconstructed by casting')

    # Invalid objects and economic outputs fail before any payment.
    for options in [dict(object_mass=101),dict(object_size='Huge'),dict(object_template='key'),dict(mundane_output_certified=False),dict(object_value=5)]:
        w=world();params=dict(objargs);params.update(options);wallet=Wallet(rp=100)
        rejects(lambda:cast(w,'true-polymorph',profile=None,wallet=wallet,**params),'Bounded creature-object input/output')
        check(wallet.rp==100 and wallet.actions==1,'Object preflight atomic')
    w=world(objects=('o',));rejects(lambda:cast(w,'true-polymorph',target='o'),'Object eligibility must certify no corpse/magic/carried/structural input')
    missing=PhysicalOrigin('unknown','object','Medium');w.add_body(Body(missing,{'hp':2,'maximum_hp':2},'Medium'))
    rejects(lambda:cast(w,'true-polymorph',target='unknown',profile=None,object_input_eligible=True,**objargs),'Missing mass/value prevents fabricated object')

    # Suppression preserves clocks/slots and True may stabilize while suppressed.
    for spell in ('polymorph','mass-polymorph','shapechange','true-polymorph'):
        w=world();target='a' if spell=='shapechange' else 'b';cast(w,spell,target=target)
        w.set_suppressed(target,10,suppressed=True,legal=True)
        check(w.current(target).suppressed and w.current(target).deadline==60 and 'a' in w.concentration.current,spell+' keeps concentration/clock under suppression')
        w.checkpoint(60,started_packets_and_due_saves_finished=True)
        if spell=='true-polymorph':
            check(w.current(target).state=='permanent' and w.current(target).suppressed,'True stabilizes while suppressed')
            w.set_suppressed(target,61,suppressed=False,legal=True)
            w.check_reversion_placement(target,fits_at_current_anchor=True)
            check(w.profile(target,stats(),61,12,ac_components_certified=True)['attack']['attack']==10,'Same stable record resumes')
        else:check(w.current(target) is None,spell+' expires while suppressed')
    w=world(objects=('o','p'));cast(w,'true-polymorph',target='o',object_input_eligible=True);w.checkpoint(60,started_packets_and_due_saves_finished=True)
    w.set_suppressed('o',61,suppressed=True,legal=True)
    rejects(lambda:cast(w,'true-polymorph',target='p',object_input_eligible=True,ident='suppression-army',now=61),'Suppression cannot free permanent slot')
    check(w.slots=={'a':'o'},'Sponsor survives suppression')

    # Independent-review blocker1: active True object replacement and retained agency.
    w=world();original_life=w.bodies['b'].life
    cast(w,'true-polymorph',profile=None,**objargs);w.checkpoint(60,started_packets_and_due_saves_finished=True)
    wallet=Wallet(rp=100)
    r=cast(w,'true-polymorph',ident='unwilling-saved',owner='c',now=61,willing=False,save=True,wallet=wallet)
    check(not r['links'] and wallet.rp==74 and wallet.actions==0,'Unwilling original person retains paid CON save while object-shaped')
    check(w.current('b').cast_id=='cast' and w.current('b').state=='permanent','Successful recast save retains old True object')
    r=cast(w,'true-polymorph',ident='unwilling-failed',owner='c',now=62,willing=False,save=False)
    check(len(r['links'])==1 and w.current('b').profile=='spellform.predator','Failed save permits creature-origin object-to-creature recast without fresh-object certification')
    check(w.bodies['b'].life is original_life and w.bodies['b'].origin.kind=='creature' and not w.slots,'Same creature HP and origin; no companion slot')
    check(w.healing_target_eligible('b',native_eligible=True),'Creature healing eligibility returns with creature anatomy')
    w=world();cast(w,'true-polymorph',profile=None,**objargs);w.checkpoint(60,started_packets_and_due_saves_finished=True)
    wallet=Wallet(rp=100)
    rejects(lambda:cast(w,'true-polymorph',profile=None,ident='hostile-object',owner='c',now=61,willing=False,wallet=wallet,**objargs),'Original person cannot be forced into another object profile')
    check(wallet.rp==100 and wallet.actions==1 and w.current('b').cast_id=='cast','Object consent failure is unpaid and leaves old record')
    cast(w,'true-polymorph',profile=None,ident='willing-object',owner='c',now=61,**objargs)
    check(w.current('b').cast_id=='willing-object' and w.current('b').profile is None,'Willing active True object-to-object recast needs no fresh admission')
    w=world(objects=('o',));cast(w,'true-polymorph',target='o',profile=None,object_input_eligible=True,**objargs)
    w.checkpoint(60,started_packets_and_due_saves_finished=True)
    cast(w,'true-polymorph',target='o',ident='object-recast',owner='c',now=61,willing=False,save=True)
    check(w.current('o').profile=='spellform.predator' and w.bodies['o'].origin.kind=='object','Object-origin registered object recast needs no fresh outside-object certificate or creature-origin save')
    check(w.slots=={'c':'o'} and not w.healing_target_eligible('o',native_eligible=True),'Fresh creature manifestation uses new caster slot; origin restrictions persist')
    # A genuinely fresh outside object still cannot bypass the original gate.
    w=world(objects=('o',));wallet=Wallet(rp=100)
    rejects(lambda:cast(w,'true-polymorph',target='o',ident='fresh-bypass',wallet=wallet),'Registered body alone does not waive fresh outside-object admission')
    check(wallet.rp==100,'Fresh object admission failure pays nothing')

    # Independent-review blocker2: agency belongs to expressed anatomy while suppressed.
    for spell,profile in [('polymorph','spellform.predator'),('mass-polymorph','spellform.predator'),
                          ('true-polymorph','spellform.predator'),('true-polymorph',None)]:
        w=world();cast(w,spell,profile=profile,**(objargs if profile is None else {}))
        w.set_suppressed('b',1,suppressed=True,legal=True)
        wallet=Wallet();w.reject('b',2,wallet,actual_regular_turn=True,legal=True)
        check(wallet.actions==0 and w.current('b') is None,spell+str(profile)+' suppressed willing regular Action rejection')
        check('b' not in w.buffers.spell_anatomies,'Rejection actually frees Druid admission registry')
    w=world();cast(w,'true-polymorph',profile=None,**objargs)
    rejects(lambda:w.reject('b',1,Wallet(),actual_regular_turn=True,legal=True),'Unsuppressed creature-object remains actionless')
    w=world(objects=('o',));cast(w,'true-polymorph',target='o',object_input_eligible=True)
    rejects(lambda:w.reject('o',1,Wallet(),actual_regular_turn=True,legal=True),'Object-origin creature has no player-style rejection entitlement')
    w.set_suppressed('o',1,suppressed=True,legal=True)
    rejects(lambda:w.reject('o',2,Wallet(),actual_regular_turn=True,legal=True),'Object-origin root stays actionless under suppression')
    w=world();cast(w,'shapechange',target='a');w.set_suppressed('a',1,suppressed=True,legal=True)
    rejects(lambda:w.switch_shapechange('a','spellform.brute',6,2,Wallet(),original_regular_turn=True,legal=True,retained_gear=set(),drop_placement_legal=True),'Suppression blocks internal Shapechange switch')
    check(w.bodies['a'].melded=={'a:coat'} and not w.bodies['a'].equipment,'Original meld set stays inaccessible while suppressed')

    # Real gear identities across switching, replacement, loss and reversion.
    w=world();cast(w,'shapechange',target='a',profile='spellform.humanoid')
    w.acquire_external_gear('a','external-shield',1,compatible_and_equipped=True)
    wallet=Wallet()
    rejects(lambda:w.switch_shapechange('a','spellform.predator',1,1,wallet,original_regular_turn=True,legal=True,retained_gear=set(),drop_placement_legal=True),'No casting-turn switch')
    rejects(lambda:w.switch_shapechange('a','spellform.predator',1,2,wallet,original_regular_turn=False,legal=True,retained_gear=set(),drop_placement_legal=True),'No extra-turn switch')
    r=w.switch_shapechange('a','spellform.predator',6,2,wallet,original_regular_turn=True,legal=True,retained_gear=set(),drop_placement_legal=True)
    check(r['droppedItemIds']==['external-shield'] and not wallet.bonus_action and not r['spellcast'],'Incompatible external gear drops; BA only')
    rejects(lambda:w.switch_shapechange('a','spellform.brute',6,2,Wallet(),original_regular_turn=True,legal=True,retained_gear=set(),drop_placement_legal=True),'One switch per original regular turn')
    w.mark_item_lost('a','a:coat',actual_loss=True);w.concentration.end('a','release')
    check(not w.bodies['a'].equipment,'No lost melded coat or dropped shield reappears')
    w=world();cast(w,profile='spellform.humanoid');w.acquire_external_gear('b','new-sword',1,compatible_and_equipped=True)
    cast(w,owner='c',ident='replacement')
    check(w.bodies['b'].melded=={'b:coat','new-sword'},'Close-and-recapture includes still-existing original and external gear exactly once')
    w.dispel('b',legal=True)
    check(w.bodies['b'].equipment=={'b:coat','new-sword'} and not w.bodies['b'].melded,'Real identities return once')
    conflict=w.check_reversion_placement('b',fits_at_current_anchor=False)
    check(conflict['placementConflict'] and not conflict['automaticRelocation'] and conflict['automaticDamage']==0,'Blocked mandatory reversion handed to geometry')

    # Druid bridge uses existing finite resource/dependency engine.
    w=world(ids=('a','d'));ds=DruidStats('d',20,6,4,4,4)
    druid=DruidState(ds,'Moon',w.buffers,{'refrain':0,'rememberedSpell':None,'dissonance':0})
    w.druids['d']=druid
    formid='druid.base.bear-form-tank'
    druid.shift(ds,formid,'druid-bear',0,Wallet(),legal=True)
    reserve=druid.reserve;surges=druid.surges
    cast(w,target='d')
    check(druid.current is None and druid.reserve==reserve and druid.surges==surges,'Spell ends Druid form without resource refund')
    check(w.buffers.amount('d')==0,'Druid form-dependent entry buffer actually ends')
    rejects(lambda:druid.shift(ds,formid,'escape',1,Wallet(),legal=True),'Druid cannot escape spell with shift')
    w.set_suppressed('d',1,suppressed=True,legal=True)
    rejects(lambda:druid.shift(ds,formid,'suppressed-escape',1,Wallet(),legal=True),'Suppressed spell still occupies anatomy slot')

    # Pairwise Mass preflight agrees with full independent-outcome enumeration.
    scenarios=0
    for cells in product(range(3),repeat=6):
        selections=[select(str(i),cell='x') for i in range(3)]
        selections=[replace(s,original_cells=frozenset({cells[2*i]}),transformed_cells=frozenset({cells[2*i+1]})) for i,s in enumerate(selections)]
        brute=all(len({cells[2*i+choice[i]] for i in range(3)})==3 for choice in product(range(2),repeat=3))
        try:validate_mass_space(selections);pairwise=True
        except SpellRuleError:pairwise=False
        assert pairwise==brute,'Mass spatial independent-outcome mismatch'
        scenarios+=1
    check(scenarios==729,'729 occupancy cases compare against exhaustive outcomes')
    ids=tuple('t'+str(i) for i in range(10));w=world(ids=('a',)+ids)
    r=w.cast('ten','mass-polymorph',stats(),price('mass-polymorph'),Wallet(rp=100),[select(t,willing=False) for t in ids],0,1,
             legal=True,resolve_save=lambda target,dc:int(target[1:])%2==0)
    check(len(r['links'])==5 and len([i for i in ids if w.current(i)])==5,'Ten Mass targets with independent mixed saves')
    w.concentration.end('a','release');check(all(w.current(i) is None for i in ids),'One concentration ends all surviving links')

    frozen=ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md'
    check(hashlib.sha256(frozen.read_bytes()).hexdigest()=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81','Frozen class packet unchanged')
    report={'status':'PASS','checks':checks,'massOccupancyScenarios':scenarios,'profiles':len(PROFILES),'spellCandidates':len(fixtures),
            'reviewStatus':'Candidate implementation; independent GPT review pending','scope':'Bounded reference contracts; not full runtime, geometry engine or balance certification'}
    (ROOT/'docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':main()

```

## docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md

```markdown
# Transformation and Harmonic Bulwark playtest candidate

**Status: discussed draft; implementation review pending.** This guide supplies five ordinary spell overlays and twelve finite forms. It does not yet add them to the operational catalog. Original spells, class access, printed schools, base RP and the frozen class packet remain preserved. All new boundaries below are provisional design decisions agreed in the notebook, not recovered original rules. Numerical balance and table playtesting remain outstanding.

## Cast summary

All five use an Action and V/S/F. Ordinary known/prepared access, class-level gates, base RP, component legality, Dissonance/Refrain, exact class modifications, countering and concentration damage checks remain mandatory.

| Spell | Operational range/targets | Base RP | Effect clock |
|---|---|---:|---|
| Harmonic Bulwark |60ft; one willing perceived creature|5 plus chosen X|Cast instantaneous; accepted shield to depletion/replacement/recipient's completed long rest|
| Polymorph |60ft; one perceived physical creature|7|Concentration60seconds|
| Shapechange |Self|26|Concentration60seconds|
| True Polymorph |120ft; one eligible physical creature or discrete object|26|Concentration60seconds, then until dispelled without concentration|
| Mass Polymorph |120ft;1–10 distinct perceived physical creatures|26|One concentration record,60seconds|

These are the selected spells' unchanged base costs; exact class access is read from the preserved catalog. Shapechange's printed120-foot source field remains in provenance; operational Self is explicitly NEW. Harmonic Bulwark's Action/range/components are NEW design, not a proven merge with the older Mana Shield name.

Before paying, choose legal targets, output profiles/templates and all spatial placements. For a concentration spell, account for the original anatomy that will return when your own old concentration ends. That projected anatomy must still be eligible for the prospective cast. Check all costs and components. Then:

1. Commit Action and actual RP payment, with ordinary class cadence consequences.
2. End your previous concentration, including all remaining Mass links, even if the new spell subsequently fails.
3. Resolve countering and initial saves. No post-commit refund.
4. Apply successful transformations. An anatomy maintained by another source persists until a successful legal replacement. No displaced anatomy remains underneath the new form.

Beginning an unrelated concentration spell does not end an already permanent True Polymorph. Starting any new concentration spell must use the shared concentration ledger, including spells outside this packet.

## Harmonic Bulwark

Choose additional conversion payment X from0 through current PB before commitment. The shield offered to the chosen recipient is **5 × (actual base RP paid + X)**. An exact legal discount can reduce the base payment. X is additional, actually paid and never discounted. Dissonance or other surcharge payments add no shield credit. Refrain affects post-cast Dissonance under ordinary rules; this spell invents no immediate Refrain surcharge.

A zero-credit fresh cast is illegal. Free casts do not mint shield value. An exact effect copying an already-resolved buffer event needs its own explicit permission. Pay Action, actual cast cost and X before countering and the normal strongest-only comparison. A stronger or equal existing shield stays, but the entire payment remains spent. A countered spell produces no offer. The accepted shield belongs to the recipient, does not heal, and normally ends at that recipient's next completed long rest.

Example: actual base payment3, X2 and surcharge2 costs7RP and offers25temporaryHP. It does not offer35. If the recipient already has25 or more, their current grant stays with its original lifetime.

## The finite spell forms

The profiles below are NEW bounded spell rules. They are not monster stat blocks or Druid forms. Polymorph and Mass use only R4. Shapechange and True may use R4 or R9. The names do not grant creature-type tags.

| Profile | Tier | Size | Movement (ft) | Speech/hands | AC | One natural attack | Additional anatomy |
|---|---|---|---|---|---|---|---|
| Humanoid |R4|Medium|walk30|yes/yes|normal|1d6+M bludgeoning|—|
| Predator |R4|Medium|walk40|no/no|max(normal,13)|1d8+M slashing|—|
| Brute |R4|Large|walk30|no/no|max(normal,15)|2d6+M bludgeoning|—|
| Avian |R4|Small|walk10, fly50|no/no|max(normal,13)|1d6+M slashing|—|
| Aquatic |R4|Medium|walk20, swim50|no/no|max(normal,14)|1d8+M piercing|water breathing|
| Burrower |R4|Medium|walk30, loose-soil burrow15|no/no|max(normal,14)|1d8+M bludgeoning|—|
| Greater brute |R9|Large|walk40|no/no|max(normal,17)|2d8+M bludgeoning|—|
| Greater winged |R9|Large|walk20, fly60|no/no|max(normal,16)|2d8+M slashing|—|
| Elemental air |R9|Medium|fly60, hover|no/no|16|2d8+M lightning|lightning resistance|
| Elemental earth |R9|Large|walk30, loose-soil burrow20|no/no|17|2d8+M bludgeoning|—|
| Elemental fire |R9|Medium|walk40|no/no|16|2d8+M fire|fire resistance|
| Elemental water |R9|Medium|walk20, swim60|no/no|16|2d8+M cold|cold resistance, water breathing|

All supplied attacks have5-foot reach and one attack per ordinary Attack Action. No Multiattack, legendary action, class, resource pool or monster ability is imported. Exact existing subject features may modify the action only when they explicitly apply to natural/form attacks or the Attack Action without an unavailable weapon/anatomical requirement. Weapon-only features remain gated. Being granted by a spell does not automatically make an attack magical for resistance/immunity bypass; no generic magical-attack flag is granted. Broader taxonomy remains a separate exact-source interface.

“Normal” AC excludes melded armor/shields and includes only certified compatible passives and actually worn compatible external equipment. Fixed elemental AC remains the specified value. Ordinary sight/hearing remain; no special senses are granted. The chosen anatomy replaces size, movement, anatomical senses, speech, hands, original anatomical attacks and anatomy-dependent defenses. Original wings/claws/gills do not persist underneath an incompatible form unless their exact source says otherwise. Nonanatomical features retain their own predicates.

## Identity, attack statistics and equipment

Keep one physical identity and one current/max HP ledger, current temporary-HP grant, Wounds/injuries, death state, conditions, actual attributes, PB, class resources, rest/recharge uses, initiative, concentration and independent effect clocks. A form is never a second HP pool. Body matter lost or destroyed remains lost. Existing class abilities use the subject's normal statistics when anatomy permits them.

The transformed subject owns its attacks, damage and kills. Polymorph, Mass and Shapechange supplied attacks use the original caster's **current** spell attack and M=max(1, casting modifier). True snapshots caster spell attack, DC, PB, M and source class at casting, throughout shaping and permanence. Supplied natural attacks are not spell casts and do not automatically trigger caster “your spell deals damage,” spell-kill or per-cast resource features.

Creature-origin subjects retain their original creature-type, ancestry, class and soul identity. Object-origin manifestations have the `transformed-object` origin tag; profile names grant no humanoid/beast/elemental/undead tag. Immutable earliest origin follows every chain of transformations and control changes.

Original carried/equipped gear melds into a record and is unavailable for ordinary weapon/shield/component use. Compatible certified passive bonuses may remain. A handed form can acquire and use real external gear normally. On an internal Shapechange switch, keep compatible external items and drop incompatible items in the current space or nearest legal adjacent space; never add them to the old meld set. Dropped items remain there.

When a different successful transformation replaces a record, atomically close the old record, restore its still-existing original meld set, include legitimate currently equipped external items, and capture that resulting gear as the new record's meld set. There is no intervening action/reaction/targeting window. Destroyed, consumed, dropped or lost items are never recreated. This also applies when a spell ends a Druid form. Suppression is not record closure and never recaptures gear. Original melded gear remains inaccessible while suppressed, including weapons, armor and material components. External gear remains real and usable only when root anatomy is certified compatible.

## Initial saves, repeats and agency

Polymorph, Mass and True creature→creature allow a willing recipient to waive the initial CON save. Otherwise resolve CON against the original caster's current DC (True uses its casting snapshot). Success leaves the target unchanged. Exact transformation immunity and legendary defenses still apply.

Each unwilling transformed target may repeat that save at each original regular-turn end, and after the first event in each numbered round that causes **positive actual normal HP damage**, after all prevention and temporary HP. Temporary-HP-only loss does not qualify. Each target has a separate round ledger; a recast does not create a second damage-triggered save from the same round. Finish the actual packet and all same-packet death prevention before deciding whether a link remains for its repeat save.

The subject retains its decisions and an ordinary form attack. Losing hands/speech may restrict particular abilities, but the transformation does not impose whole-Action denial. A willing temporary creature-origin recipient with action-capable expressed anatomy can reject Polymorph, Mass or shaping True with its Action on its original regular turn. This permission remains while suppressed: a creature-origin object form temporarily expressing its root creature anatomy can reject then. Unsuppressed object anatomy is actionless and cannot reject; object-origin identities gain no player-style rejection right. Changing one's mind does not create hostile repeat saves. Shapechange uses ordinary concentration release and cannot invoke its internal switch while suppressed.

Mass makes independent saves for1–10 targets using preselected R4 profiles. For each target, O is the footprint remaining on a successful save and T is the footprint on failure/waiver. Before paying, every pair must support O/O, O/T, T/O and T/T without illegal overlap; each individual footprint must also fit terrain/other bodies. A target's own O/T may overlap. Apply successful changes simultaneously. Ending/replacing one target link leaves other links intact. There is no ongoing range tether.

## Endings, switching, suppression and geometry

Polymorph, Mass and Shapechange end at cast time+60seconds. True's stabilization checkpoint is the same absolute60seconds. Extra turns never extend these clocks. At a shared timestamp: finish an already-started event packet; process due hostile repeats; end successful saves; then expire temporary spells or stabilize surviving True links; then administrative cleanup. A successful final repeat prevents permanence.

Actual0HP, death or external Incapacitated after every same-packet replacement ends temporary spell anatomy, including both creature→creature and creature→object during True shaping. A legal “remain at1” keeps the form. Reversion never heals, clears Wounds, restores temporary HP or rerolls damage. Permanent True does not end merely at0/death; later dispel returns a still-dead/damaged original body and cannot recreate missing matter. Structural0 destroys an object-origin manifestation and releases its slot.

Shapechange's internal switch costs a Bonus Action, requires a different legal profile and space, and occurs at most once on each later original regular turn. It cannot occur on the casting turn, including a cast on an extra turn, and never occurs on an extra turn. It pays no new RP, makes no spellcast/Refrain event, resets no resources, and grants no free attack. Losing unsupported flight invokes ordinary falling.

A spell may successfully replace a Druid form, ending actual form-dependent effects without refunds. A Druid cannot Shapeshift while any spell-transformation record is active, including suppressed or permanent records. Temporary replacement requires at least the existing rank. Permanent True requires another successful True or an exact named exception. Same-profile new casts remain legal paid casts. These precedence checks apply to an old record that survives commitment; your own concentration record already ends when the new concentration cast commits.

Antimagic suppresses every transformation without ending its record. The root anatomy is expressed, concentration remains required where applicable, and the original clock continues. Temporary spells may expire while suppressed. True may stabilize while suppressed if concentration remains valid, then resume its permanent anatomy later. Suppression never releases a companion slot or creates a second hidden form. A suppressed record still follows the same replacement precedence.

Mandatory reversion uses the **same spatial anchor**. If root anatomy cannot fit, report `placementConflict` to canonical geometry. No automatic teleport through walls, free relocation or invented crushing damage occurs. Until resolved, overlap cannot establish legal movement/targeting through a barrier. **Open whole-game dependency:** the general mandatory-reversion geometry conflict procedure. The helper exposes this boundary rather than claiming that geometry subsystem is complete.

## True Polymorph object modes

True allows creature→creature, willing creature→object, eligible object→creature, and eligible object→object. Only one object/body is produced. Object input must be a discrete nonmagical, unattended, uncarried, unworn, unattuned Large-or-smaller object with canonical current/max structural HP. Artifacts, active magical devices, terrain/building structures, corpses/significant remains and undefined-durability objects are ineligible.

Those fresh-object admission checks apply to introducing an ordinary outside object. An already-active True Polymorph object anatomy can be replaced by another legal True Polymorph without pretending it is an unattended nonmagical outside object. A creature-origin person in object anatomy retains agency: creature-profile replacement permits a willing waiver or requires a CON save if unwilling; object-profile replacement requires willingness. Returning that person to creature anatomy preserves their original HP/Wounds/class/soul and creates no companion slot. Object-origin recasts retain all origin, value and slot constraints.

Object outputs are Tiny through Large, within one size category of the actual input, AC12, inert and nonmagical. Allowed templates: barrier/slab, ramp/wedge, open-container, static-furniture, simple-one-piece-tool. Static joined pieces and open hollow containers are allowed; actuated mechanisms, working hinges/latches/locks/keys, gears/clocks/traps, precision instruments, pressure vessels and documents/credentials are not. No output grants material resistance/immunity.

Require documented physical mass. Output mass cannot exceed the current input mass or earliest origin ceiling. Object-origin recoverable/sale value cannot exceed its earliest documented value; missing necessary mass/value makes that mode ineligible. Creature-origin object anatomy has no independent sale/salvage/harvest value. No mode produces food, medicine, ammunition, currency, gemstones, rare crafting material, valuables, consumable stock or magical properties. Chains never rebase the ceilings upward.

Creature→object retains the same character HP/Wounds/resources/history but supplies speed0, no Actions/Bonus Actions/Reactions, no speech/senses/hands. This is `actionlessObjectAnatomy`, **not** an automatic Incapacitated condition. A caster can therefore maintain their self-targeted shaping spell. Actual external Incapacitated still ends concentration/shaping normally. Permanent object anatomy has no voluntary rejection.

Object→creature uses a non-humanoid finite profile and exactly its existing structural current/max HP ledger. It has ordinary sight/hearing, saves equal to captured caster PB, ordinary unproficient checks+0, no special senses unless listed, no Wounds/death saves/Stable/dying state, soul, class/rest resources, reproduction, resurrection or XP/loot/corpse entitlement. At structural0, it is destroyed; dispel does not rebuild it. Temporary HP may protect it. Ordinary healing cannot repair it, even after later transformations; exact nonorganic repair is a separate source interface.

Creature-origin currently in object anatomy cannot newly receive effects requiring a creature/living creature/ally creature. Ordinary healing eligibility returns with creature anatomy if other requirements permit it. Already-attached effects retain their own exact lifetimes; a pulse needing fresh creature eligibility must recheck it. Transformation does not convert healing into object repair.

## Object companions

A successful object→creature application reserves one object-creature slot immediately, including shaping. It belongs to the original creating caster and stays occupied through stabilization, suppression, control changes and legal creature-profile replacements by other casters. Recasting the same body consumes no second slot and does not transfer control or sponsorship. A distinct second permanent creature cannot be created while the slot is occupied.

Release the slot only on actual ending/dispel to the original object, physical destruction or an allowed replacement into object anatomy. A later fresh object→creature casting after such an ending uses its new creating caster's slot. No free dismissal exists after stabilization. Existing companion transformations do not automatically change their owner/allegiance.

Use the current controller's **shared** companion Bonus Action command and one offensive-companion allowance,60-foot command range and actual perception, attached resolution, and uncommanded move+Dodge. No separate full damaging turn appears. Source-qualified exceptions remain exact. If an issued command becomes illegal, resources stay spent and the order does not execute. Supplied attacks still belong to the subject, with the original transformation caster's statistics.

## Evidence and implementation boundary

Notebook decisions are preserved in `docs/audit/2026-10-08/full-game/GPT_TRANSFORMATION_SPELL_FIRST_REVIEW.md`, `GPT_TRANSFORMATION_SPELL_BOUNDARIES.md` and `GPT_TRANSFORMATION_SPELL_FINAL_INTERFACES.md` in the main project. Exact source objects/hashes are in `TRANSFORMATION_SPELL_SOURCE_CANDIDATES.json`. The profiles carry evidence hashes. `candidate_transformations.json` remains inactive.

`transformation_spell_playtest_rules.py` is a bounded contract reference. The caller owns actual known/prepared access, range/LOS/components, canonical price/class cadence, rolls, geometry, same-packet prevention, concentration damage saves, turn/round calendar and source eligibility. It receives actual finalized HP state and never owns a second HP pool. All adapters must share one concentration ledger, buffer ledger, form identity registry and controller command ledger. The Druid guard is the only integration change to the existing form helper. Independent review must examine this actual code and its tests before catalog promotion.

```

## data/playtest/spell_drafts/candidate_transformations.json

```json
{
  "status": "CANDIDATE; independent implementation review pending",
  "spells": [
    {
      "id": "harmonic-bulwark",
      "activation": "Action",
      "rangeFeet": 60,
      "targets": "One willing creature you can perceive within 60 feet",
      "duration": "Cast instantaneous; accepted temporary HP last until depleted, replaced, or the recipient completes a long rest",
      "concentration": false,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Automatic after legal payment; temporary-HP strongest-only arbitration then applies.",
      "effect": "The chosen willing recipient receives a temporary-HP offer equal to 5 times credited RP. Credited RP is actual base RP paid after exact legal base-cost reductions plus chosen additional X from0..PB. X cannot be discounted. Ordinary surcharges never count toward credited RP. Use canonical ordinary-cast pricing; Refrain changes post-cast Dissonance and is not a new RP surcharge.",
      "scaling": "5 temporary HP per credited RP. Additional conversion RP X is capped by proficiency bonus and must actually be paid.",
      "limitations": "Additional conversion RP cannot itself be discounted. Payment occurs before nonstack arbitration and is not refunded when a stronger or equal shield remains. A cast with zero credited RP is illegal. Free casts/copies that spend no credited RP create no fresh Harmonic Bulwark shield unless their own exact copy rule expressly copies an already-resolved temporary-HP event. Temporary HP are not healing and use the canonical one-active-buffer rule. Choose X before commitment. Commit Action plus quoted casting payment plus X before countering or arbitration; no post-commit refund. A countered spell offers nothing.",
      "designNotes": "PRESERVED: Harmonic Bulwark identity, Universal Rank 3, class access/learn levels/base 5 RP, and 5 temporary HP per RP source wording. NEW: Action, 60-foot range, one willing target, V/S/F components, PB cap on discretionary RP, exact credited-RP accounting, and V6-default shield lifetime. Action/range/components resemble the unproven Mana Shield candidate but are adopted only as provisional Harmonic Bulwark design choices; the alias is not treated as source identity.",
      "implementationStatus": "candidate; independent implementation review pending",
      "procedureReference": "docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md"
    },
    {
      "id": "polymorph",
      "activation": "Action",
      "rangeFeet": 60,
      "targets": "One physical creature you can perceive within 60 feet",
      "duration": "Concentration, up to 1 minute; absolute checkpoint at casting timestamp +60 seconds, never extended by extra turns",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Choose one legal R4 spell-form profile and validate its space before payment. A willing target may waive its save. An unwilling target makes a Constitution save against your spell DC. On failure it transforms. At the end of each of its original regular turns, and once per numbered round after it suffers positive actual HP damage, it may repeat the save; success ends the transformation. Use the complete TRANSFORMATION_SPELL_PLAYTEST.md procedure and finite spell_form_profiles.json register. Preflight all targets, anatomy, space and access before committing Action/RP; commit ends your old concentration before counters or saves. A failed or countered new spell does not restore old concentration. An anatomy from another source is replaced only on actual success. No displaced form remains underneath.",
      "effect": "Replace the target's current anatomy with the chosen R4 spell-form profile while preserving one body, current/max HP, temporary HP, Wounds, conditions, attributes, proficiency, identity, resources, initiative and condition clocks. The supplied form attack uses the original caster's current spell attack bonus and M. Equipment melds and is unavailable unless a separate anatomy-compatible passive bonus is certified. The target retains control of all decisions.",
      "scaling": "No automatic profile, damage, target-count or duration scaling. Use only the bounded R4 spell-form register.",
      "limitations": "No monster stat block, multiattack, class spellcasting, legendary power, new resource pool or second HP pool is gained. Speech, hands and movement come only from the selected profile. A willing target may spend its Action on its regular turn to end its own Polymorph. Actual 0 HP, death or Incapacitated after same-packet prevention resolves ends the spell without healing. Explicit transformation immunity and legendary defenses apply normally. Natural/form attacks do not automatically qualify for unrelated weapon-only features. The subject owns supplied natural-attack events; the original caster supplies attack statistics. These attacks are not spell casts or automatically caster spell-damage/kill triggers. A Druid cannot enter Shapeshift while a spell anatomy is active. Temporary lower-rank spells cannot replace higher-rank anatomy. Only a successful True Polymorph or an exact named exception can replace permanent True anatomy. Antimagic suppresses the same record while concentration and its absolute clock continue; True Polymorph can stabilize while suppressed. Suppression never frees an object-companion slot or resets gear. Creature-origin type tags remain unchanged; profile names confer no creature type. Every supplied attack has5-foot reach. Original anatomical abilities unavailable in the selected profile do not persist underneath it. A successful new transformation closes the old record and atomically restores/recaptures still-existing original gear; internal profile switches instead retain the same meld set and drop incompatible external gear. Mandatory reversion returns at the same anchor; blocked placement is referred to canonical geometry without automatic teleport or crushing damage. Original melded gear remains inaccessible under antimagic. A willing temporary creature-origin recipient can use its regular-turn rejection Action while suppressed if its root creature anatomy can act; object-origin identities gain no rejection right. No generic magical-attack bypass flag is granted.",
      "designNotes": "PRESERVED: Polymorph identity, Transmutation Rank 4, exact class access, Action, 60 feet, V/S/F and base 7 RP. NEW: one-minute concentration, target/save/repeat-save procedure, R4 finite profile list, same-body state retention, caster-derived form attack, equipment/anatomy rules and zero-HP reversion.",
      "implementationStatus": "candidate; independent implementation review pending",
      "procedureReference": "docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md"
    },
    {
      "id": "shapechange",
      "activation": "Action",
      "rangeFeet": 0,
      "targets": "Self",
      "duration": "Concentration, up to 1 minute; absolute checkpoint at casting timestamp +60 seconds, never extended by extra turns",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Choose one legal R4 or R9 spell-form profile on cast. No save. Once on each of your original regular turns afterward, you may use a Bonus Action to switch to a different legal profile. The new anatomy must fit the available space. Use the complete TRANSFORMATION_SPELL_PLAYTEST.md procedure and finite spell_form_profiles.json register. Preflight all targets, anatomy, space and access before committing Action/RP; commit ends your old concentration before counters or saves. A failed or countered new spell does not restore old concentration. An anatomy from another source is replaced only on actual success. No displaced form remains underneath. No internal switch on the casting turn or an extra turn; first switch is the next original regular turn, then at most one on each later original regular turn.",
      "effect": "You retain your identity, current/max HP, temporary HP, Wounds, conditions, attributes, proficiency, resources, initiative and existing effects. Only your current anatomy/profile changes. Each supplied natural attack uses your current spell attack bonus and M. Profile switching does not create a new body, heal, refresh resources, restore temporary HP or reset rest/recharge uses.",
      "scaling": "No automatic scaling beyond the bounded R4+R9 profile register.",
      "limitations": "Only one Shapechange anatomy exists at a time. An identical-profile switch is rejected before Bonus Action payment. Internal switches are not spell casts and do not create new Dissonance or Refrain events. Equipment remains melded through switches. Losing flight while unsupported begins ordinary falling. Actual 0 HP, death or Incapacitated after same-packet prevention ends Shapechange without healing. The spell grants no Druid Buffer Reserve, Form Surge, Shapeshift use or Druid form features. The subject owns supplied natural-attack events; the original caster supplies attack statistics. These attacks are not spell casts or automatically caster spell-damage/kill triggers. A Druid cannot enter Shapeshift while a spell anatomy is active. Temporary lower-rank spells cannot replace higher-rank anatomy. Only a successful True Polymorph or an exact named exception can replace permanent True anatomy. Antimagic suppresses the same record while concentration and its absolute clock continue; True Polymorph can stabilize while suppressed. Suppression never frees an object-companion slot or resets gear. Creature-origin type tags remain unchanged; profile names confer no creature type. Every supplied attack has5-foot reach. Original anatomical abilities unavailable in the selected profile do not persist underneath it. A successful new transformation closes the old record and atomically restores/recaptures still-existing original gear; internal profile switches instead retain the same meld set and drop incompatible external gear. Mandatory reversion returns at the same anchor; blocked placement is referred to canonical geometry without automatic teleport or crushing damage. Original melded gear remains inaccessible under antimagic. A willing temporary creature-origin recipient can use its regular-turn rejection Action while suppressed if its root creature anatomy can act; object-origin identities gain no rejection right. No generic magical-attack bypass flag is granted.",
      "designNotes": "PRESERVED: Shapechange identity, Rank 9, Druid/Mage/Wizard access and class-specific schools, Action, source 120-foot metadata, V/S/F, base 26 RP, and the core concept of changing creature form each round. NEW: operational target narrowed to Self, one-minute concentration, Bonus Action once-per-original-regular-turn switching, finite R4/R9 profiles and same-body state rules. The original 120-foot source field remains preserved in provenance despite the self-target operational narrowing.",
      "implementationStatus": "candidate; independent implementation review pending",
      "procedureReference": "docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md"
    },
    {
      "id": "true-polymorph",
      "activation": "Action",
      "rangeFeet": 120,
      "targets": "One eligible physical creature or one eligible discrete nonmagical unattended object within 120 feet",
      "duration": "Concentration during a 1-minute shaping period; if maintained for the full minute, the transformation persists until dispelled without further concentration; absolute checkpoint at casting timestamp +60 seconds, never extended by extra turns",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Choose creature-to-creature, willing-creature-to-object, object-to-creature, or object-to-object before payment. Creature-to-creature may affect an unwilling target on a failed Constitution save; while shaping, that target repeats the save at each original regular end and once per numbered round after positive actual HP damage. Creature-to-object requires willingness. Objects make no save. If concentration survives the full shaping minute, the result becomes persistent until dispelled. Use the complete TRANSFORMATION_SPELL_PLAYTEST.md procedure and finite spell_form_profiles.json register. Preflight all targets, anatomy, space and access before committing Action/RP; commit ends your old concentration before counters or saves. A failed or countered new spell does not restore old concentration. An anatomy from another source is replaced only on actual success. No displaced form remains underneath.",
      "effect": "Creature transformations retain one identity and one HP/durability history. Creature-to-creature uses any legal R4 or R9 spell-form profile. Creature-to-object creates one inert mundane object anatomy without healing or a new durability pool. Object-to-creature uses the object's existing structural HP as its one durability ledger and creates a controlled no-soul companion using an eligible non-humanoid R4/R9 profile and the caster's snapshotted spell statistics. Object-to-object changes only mundane form/material within the bounded utility restrictions.",
      "scaling": "No automatic scaling. Permanent attack/DC values supplied by this spell snapshot the original caster's spell attack, spell DC and M when cast. Snapshot PB and source class as well. All True Polymorph supplied attack/DC values use this snapshot from casting, including shaping.",
      "limitations": "No mode creates XP, loot, a soul, resurrection entitlement, valuable material, consumable stock, ammunition, currency, medicine, food or magical properties. Carried, worn, attuned, magical, artifact, structural-terrain and undefined-durability objects are ineligible. Object-origin creatures cannot receive ordinary HP healing as a means of repairing their source object. Only one active object-origin True Polymorph creature per caster is permitted. Such a creature shares the owner's companion Bonus Action/offensive budget and gains no independent turn/resources. Permanent True Polymorph does not end at 0 HP merely to restore the original form. Death/destruction remains real; later dispelling changes anatomy only and never heals, resurrects or recreates missing matter. The subject owns supplied natural-attack events; the original caster supplies attack statistics. These attacks are not spell casts or automatically caster spell-damage/kill triggers. A Druid cannot enter Shapeshift while a spell anatomy is active. Temporary lower-rank spells cannot replace higher-rank anatomy. Only a successful True Polymorph or an exact named exception can replace permanent True anatomy. Antimagic suppresses the same record while concentration and its absolute clock continue; True Polymorph can stabilize while suppressed. Suppression never frees an object-companion slot or resets gear. Creature-origin type tags remain unchanged; profile names confer no creature type. Every supplied attack has5-foot reach. Original anatomical abilities unavailable in the selected profile do not persist underneath it. A successful new transformation closes the old record and atomically restores/recaptures still-existing original gear; internal profile switches instead retain the same meld set and drop incompatible external gear. Mandatory reversion returns at the same anchor; blocked placement is referred to canonical geometry without automatic teleport or crushing damage. Original melded gear remains inaccessible under antimagic. A willing temporary creature-origin recipient can use its regular-turn rejection Action while suppressed if its root creature anatomy can act; object-origin identities gain no rejection right. No generic magical-attack bypass flag is granted. Object origin and earliest physical identity persist through every transformation chain. Object-origin creatures never gain a humanoid profile, soul, ordinary healing, resurrection or biological/class/rest resources. Use one actual structural HP ledger; structural0 destroys the object and ends its creature manifestation. Creature-origin object anatomy is actionless, not automatically Incapacitated. Allowed object templates are barrier/slab, ramp/wedge, open-container, static-furniture or simple-one-piece-tool; no actuated mechanism, magical or valuable output. Output size Tiny..Large and within one category of input; output mass cannot exceed recorded input or earliest origin mass; value cannot exceed original documented ceiling. Corpses/remains, magical/attuned/carried/worn/attended/structural objects and undefined structural durability are ineligible. An object-creature reserves its original caster slot on successful shaping; suppression/control change never frees it. At the60-second boundary finish damage, resolve due repeat save, then stabilize only surviving links. Replacing an active True object anatomy requires legal True replacement, not fresh nonmagical/unattended outside-object admission. Creature-origin people retain their CON save against unwilling creature-profile recasts and must consent to object-profile recasts. Returning them to creature anatomy grants no companion slot.",
      "designNotes": "PRESERVED: True Polymorph identity, Rank 9, exact class access/schools, Action, 120 feet, V/S/F, base 26 RP, creature/object scope and meaningful until-dispelled permanence. NEW: one-minute shaping/stabilization procedure, save/agency rules, bounded form register, object eligibility/size/value rules, object-origin companion contract, one controlled-object-creature cap, durability conservation and destruction/dispel semantics.",
      "implementationStatus": "candidate; independent implementation review pending",
      "procedureReference": "docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md",
      "concentrationAfterStabilization": false
    },
    {
      "id": "mass-polymorph",
      "activation": "Action",
      "rangeFeet": 120,
      "targets": "Up to 10 distinct physical creatures you can perceive within 120 feet",
      "duration": "Concentration, up to 1 minute; absolute checkpoint at casting timestamp +60 seconds, never extended by extra turns",
      "concentration": true,
      "components": [
        "V",
        "S",
        "F"
      ],
      "resolution": "Before payment choose 1-10 targets and one legal R4 spell-form profile for each, validating each possible anatomy's space. Willing targets may waive saves. Each unwilling target independently makes a Constitution save. Failure creates that target's transformation link. Each hostile transformed target repeats the save at its original regular-turn end and once per numbered round after positive actual HP damage. Success ends only that target's link. Use the complete TRANSFORMATION_SPELL_PLAYTEST.md procedure and finite spell_form_profiles.json register. Preflight all targets, anatomy, space and access before committing Action/RP; commit ends your old concentration before counters or saves. A failed or countered new spell does not restore old concentration. An anatomy from another source is replaced only on actual success. No displaced form remains underneath. Before payment validate O/O, O/T, T/O and T/T footprint compatibility for every pair of targets; saves resolve independently and successful anatomy changes apply simultaneously.",
      "effect": "Each failed/waived target gains exactly one selected R4 anatomy while retaining its own identity, current/max HP, temporary HP, Wounds, conditions, attributes, proficiency, resources, initiative and condition clocks. Each target's supplied natural attack uses the original caster's current spell attack bonus and M. All transformed targets share one concentration record but otherwise resolve their own transformation endings independently.",
      "scaling": "Exactly up to 10 creatures. No generic three-target cap and no automatic access to the R9-only greater/elemental profiles.",
      "limitations": "Casting range and line of effect are checked only when the spell is committed; there is no ongoing range tether. One target ending does not end another. Concentration ending removes every remaining target transformation. No target gains monster stat blocks, multiattack, resources, class features or a second HP pool. Equipment/anatomy, natural-attack taxonomy, damage/reversion and agency follow the shared spell-transformation chassis. The subject owns supplied natural-attack events; the original caster supplies attack statistics. These attacks are not spell casts or automatically caster spell-damage/kill triggers. A Druid cannot enter Shapeshift while a spell anatomy is active. Temporary lower-rank spells cannot replace higher-rank anatomy. Only a successful True Polymorph or an exact named exception can replace permanent True anatomy. Antimagic suppresses the same record while concentration and its absolute clock continue; True Polymorph can stabilize while suppressed. Suppression never frees an object-companion slot or resets gear. Creature-origin type tags remain unchanged; profile names confer no creature type. Every supplied attack has5-foot reach. Original anatomical abilities unavailable in the selected profile do not persist underneath it. A successful new transformation closes the old record and atomically restores/recaptures still-existing original gear; internal profile switches instead retain the same meld set and drop incompatible external gear. Mandatory reversion returns at the same anchor; blocked placement is referred to canonical geometry without automatic teleport or crushing damage. Original melded gear remains inaccessible under antimagic. A willing temporary creature-origin recipient can use its regular-turn rejection Action while suppressed if its root creature anatomy can act; object-origin identities gain no rejection right. No generic magical-attack bypass flag is granted.",
      "designNotes": "PRESERVED: Mass Polymorph identity, Transmutation Rank 9, Druid/Mage/Wizard level-17 access, Action, 120 feet, V/S/F, base 26 RP and explicit up-to-10-creature scope. NEW: one-minute concentration, preselected per-target R4 profiles, independent saves/endings, no ongoing tether and shared same-body transformation rules.",
      "implementationStatus": "candidate; independent implementation review pending",
      "procedureReference": "docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md"
    }
  ]
}

```

## data/playtest/spell_form_profiles.json

```json
{
  "status": "candidate; implementation review pending",
  "profiles": [
    {
      "id": "spellform.humanoid",
      "tier": "R4",
      "size": "Medium",
      "movement": {
        "walk": 30
      },
      "speech": true,
      "hands": true,
      "ac": {
        "mode": "normal",
        "amount": 0
      },
      "attack": {
        "dice": "1d6",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.humanoid",
        "tier": "R4",
        "size": "Medium",
        "movement": "walk 30",
        "speechHands": "yes / yes",
        "ac": "formNormalAC",
        "naturalAttack": "1d6+M bludgeoning",
        "passiveAnatomy": "none"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.predator",
      "tier": "R4",
      "size": "Medium",
      "movement": {
        "walk": 40
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 13
      },
      "attack": {
        "dice": "1d8",
        "damageType": "slashing",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.predator",
        "tier": "R4",
        "size": "Medium",
        "movement": "walk 40",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,13)",
        "naturalAttack": "1d8+M slashing",
        "passiveAnatomy": "none"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.brute",
      "tier": "R4",
      "size": "Large",
      "movement": {
        "walk": 30
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 15
      },
      "attack": {
        "dice": "2d6",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.brute",
        "tier": "R4",
        "size": "Large",
        "movement": "walk 30",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,15)",
        "naturalAttack": "2d6+M bludgeoning",
        "passiveAnatomy": "none"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.avian",
      "tier": "R4",
      "size": "Small",
      "movement": {
        "walk": 10,
        "fly": 50
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 13
      },
      "attack": {
        "dice": "1d6",
        "damageType": "slashing",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.avian",
        "tier": "R4",
        "size": "Small",
        "movement": "walk 10, fly 50",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,13)",
        "naturalAttack": "1d6+M slashing",
        "passiveAnatomy": "flight"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.aquatic",
      "tier": "R4",
      "size": "Medium",
      "movement": {
        "walk": 20,
        "swim": 50
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 14
      },
      "attack": {
        "dice": "1d8",
        "damageType": "piercing",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": true,
      "sourceProposal": {
        "id": "spellform.aquatic",
        "tier": "R4",
        "size": "Medium",
        "movement": "walk 20, swim 50",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,14)",
        "naturalAttack": "1d8+M piercing",
        "passiveAnatomy": "water breathing"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.burrower",
      "tier": "R4",
      "size": "Medium",
      "movement": {
        "walk": 30,
        "burrowLooseSoil": 15
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 14
      },
      "attack": {
        "dice": "1d8",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.burrower",
        "tier": "R4",
        "size": "Medium",
        "movement": "walk 30, burrow 15 through loose soil",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,14)",
        "naturalAttack": "1d8+M bludgeoning",
        "passiveAnatomy": "loose-soil burrow"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.greater-brute",
      "tier": "R9",
      "size": "Large",
      "movement": {
        "walk": 40
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 17
      },
      "attack": {
        "dice": "2d8",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.greater-brute",
        "tier": "R9",
        "size": "Large",
        "movement": "walk 40",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,17)",
        "naturalAttack": "2d8+M bludgeoning",
        "passiveAnatomy": "none"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.greater-winged",
      "tier": "R9",
      "size": "Large",
      "movement": {
        "walk": 20,
        "fly": 60
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "floor",
        "amount": 16
      },
      "attack": {
        "dice": "2d8",
        "damageType": "slashing",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.greater-winged",
        "tier": "R9",
        "size": "Large",
        "movement": "walk 20, fly 60",
        "speechHands": "no / no",
        "ac": "max(formNormalAC,16)",
        "naturalAttack": "2d8+M slashing",
        "passiveAnatomy": "flight"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.elemental-air",
      "tier": "R9",
      "size": "Medium",
      "movement": {
        "fly": 60,
        "hover": true
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "fixed",
        "amount": 16
      },
      "attack": {
        "dice": "2d8",
        "damageType": "lightning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [
        "lightning"
      ],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.elemental-air",
        "tier": "R9",
        "size": "Medium",
        "movement": "fly 60, hover",
        "speechHands": "no / no",
        "ac": "16",
        "naturalAttack": "2d8+M lightning",
        "passiveAnatomy": "lightning resistance"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.elemental-earth",
      "tier": "R9",
      "size": "Large",
      "movement": {
        "walk": 30,
        "burrowLooseSoil": 20
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "fixed",
        "amount": 17
      },
      "attack": {
        "dice": "2d8",
        "damageType": "bludgeoning",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.elemental-earth",
        "tier": "R9",
        "size": "Large",
        "movement": "walk 30, burrow 20 loose soil",
        "speechHands": "no / no",
        "ac": "17",
        "naturalAttack": "2d8+M bludgeoning",
        "passiveAnatomy": "loose-soil burrow"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.elemental-fire",
      "tier": "R9",
      "size": "Medium",
      "movement": {
        "walk": 40
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "fixed",
        "amount": 16
      },
      "attack": {
        "dice": "2d8",
        "damageType": "fire",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [
        "fire"
      ],
      "waterBreathing": false,
      "sourceProposal": {
        "id": "spellform.elemental-fire",
        "tier": "R9",
        "size": "Medium",
        "movement": "walk 40",
        "speechHands": "no / no",
        "ac": "16",
        "naturalAttack": "2d8+M fire",
        "passiveAnatomy": "fire resistance"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    },
    {
      "id": "spellform.elemental-water",
      "tier": "R9",
      "size": "Medium",
      "movement": {
        "walk": 20,
        "swim": 60
      },
      "speech": false,
      "hands": false,
      "ac": {
        "mode": "fixed",
        "amount": 16
      },
      "attack": {
        "dice": "2d8",
        "damageType": "cold",
        "category": "natural/form",
        "count": 1,
        "reachFeet": 5
      },
      "resistances": [
        "cold"
      ],
      "waterBreathing": true,
      "sourceProposal": {
        "id": "spellform.elemental-water",
        "tier": "R9",
        "size": "Medium",
        "movement": "walk 20, swim 60",
        "speechHands": "no / no",
        "ac": "16",
        "naturalAttack": "2d8+M cold",
        "passiveAnatomy": "cold resistance, water breathing"
      },
      "provenance": "NEW finite spell profile agreed with GPT; not a Druid or bestiary stat block"
    }
  ],
  "evidence": [
    {
      "path": "GPT_TRANSFORMATION_SPELL_FIRST_REVIEW.md",
      "sha256": "2d70c89fc53db4e4498c1c0e4a603bfe57e7b02e3d0583330899fd63d7e5009d"
    },
    {
      "path": "GPT_TRANSFORMATION_SPELL_BOUNDARIES.md",
      "sha256": "83e76eb5f04e2b02a0948f95d0d9e72db19d522c0372520cedf01b0b733b927d"
    },
    {
      "path": "GPT_TRANSFORMATION_SPELL_FINAL_INTERFACES.md",
      "sha256": "192f5eadabd7f0f502ea5d831016a17e3eeb22860bf8e4ddb847e38cce91935d"
    }
  ]
}

```

## docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json

```json
{
  "status": "PASS",
  "checks": 216,
  "massOccupancyScenarios": 729,
  "profiles": 12,
  "spellCandidates": 5,
  "reviewStatus": "Candidate implementation; independent GPT review pending",
  "scope": "Bounded reference contracts; not full runtime, geometry engine or balance certification"
}

```

# NEXT CONFERENCE — exact8 feats and prior reviewed interfaces

# Eight named feats — full-clause source conference

**Prepared conference packet; submission is recorded only after visible browser confirmation. No feat is promoted by this packet.** The form/buffer conference reviewed selected components of seven feats. Completing Soul Cage also requires the existing Lifeleech feat: its printed soul charges explicitly power Soul Cage. This is a semantic dependency supplement, not a new feat. All335 registry records remain preserved.

Questions for the later full-clause conference:

1. Chef needs an actual food quantity, ingredients/tool use, recipients, shield amount, consumption action/time, shelf life and rest eligibility. Prevent portable infinite rest-food caches while preserving the source's long-rest cooking role. Distinguish necessary food consumption from trading surplus meal items in the existing economy.
2. Inspiring Leader needs exact recipient count, self eligibility, hearing/language/range, interruption, shield amount and per-recipient refresh frequency. Preserve the printed ten minutes and Charisma13 prerequisite. Repeated speeches should not evade a shared source-family limit.
3. Empowered Summoning retains Charisma14, creation-time2PB shield, and PB on each summoned creature's first damage roll per round. Define actual summons versus bound/returned existing creatures, caster/source attribution, area damage, shared rolls, attacks versus damage ticks and multiclass companions. Do not multiply one roll's PB over all targets or refresh it by dismissal/recreation. Keep the existing shared command budget.
4. Field Medic retains Medicine training, a Bonus Action option to use a healer's kit and PB shield after actual stabilization. The reviewed Core kit use automatically stabilizes one living dying creature and consumes one actual kit use; replayed stabilization of an already Stable target is illegal. Does the feat's second sentence apply to all actual stabilization by this owner, including a Medicine Action or spell, or only the kit? State one source-faithful interpretation and any new restriction explicitly.
5. Blood Ritual retains Constitution13, level4, ten minutes and1/LR. Self offer2×level and each eligible ally offerlevel are already agreed; allies last1 hour, self uses default recipient LR. Complete target count, blood-sharing consent, presence/range/interruption, the independent curse/disease save advantage's deadline and its next-save scope. No HP loss is printed for the drop of blood. Do not grant any actual lycanthropic oath merely from its thematic prerequisite language.
6. Necrotic Affinity retains Religion proficiency OR level8. Its resistance/Reaction prevention/post-packet shield is already reviewed; complete the separate melee-hit1d6 once-per-turn and24-hour anti-resurrection clauses. Clarify own turn versus every actual turn, natural melee attacks, extra Actions, damage provenance and final killer attribution. Translate “effects of fifth level or lower” to this game's actual rank/access system, including class abilities without spell ranks. No copied kill, staged target or temporary form should create a new corpse or soul entitlement.
7. Lifeleech's necrotic spell healing requires actual damage, eligibility, target and pulse limits, excess handling and the existing Critical/healing-prohibition procedures. Its soul spark and Soul Cage capture need one owner charge pool and one entitlement per real eligible death. Preserve cap3; do not double a kill's charge from both feats. Specify party/created/summoned/revived target exclusions explicitly as new integration where absent.
8. Soul Cage requires Lifeleech OR spellcasting ability plus level8. Clarify the exact prerequisite grammar. Complete black-crystal requirements, ownership, soul consent/eligibility, capture action and timing, range/perception, competing captors, resurrection/Soul Bind interaction, soul release and charge decay. Is a charge truly the trapped soul or a residue that does not prevent resurrection? Avoid leaving that world consequence implicit.
9. Soul Cage's one-charge2d8 shield and two-charge3d8 necrotic Agony Lance need activation, target, range, DC/stat owner, save, lifetime, per-use frequency and paid-failure rules. “Disadvantage on the next healing it receives” has no defined generic healing roll: choose and label an operational conversion, not a silently assumed half-heal. Specify how fixed healing, rolled healing, stabilization, shields and resurrection interact.
10. Present full source-qualified feat objects with prerequisites, acquisition/repeatability, every action/cost/target/deadline/frequency and each clause. Preserve original and legacy text. Identify prior reviewed interfaces, genuinely new design choices and remaining external catalog dependencies. Full object drafting and bounded validation precede promotion; passing old buffer tests is not full-feat approval.


## chef
```json
{
  "id": "chef",
  "sourceObject": {
    "id": "chef",
    "name": "Chef",
    "description": "You are an accomplished cook.",
    "prerequisite": "None",
    "effect": "You can cook special food during a long rest that provides temporary hit points to your party.",
    "type": "General",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "sourceObjectSha256": "0e5b2a5c446a30438540005e0f2bc1754523b0c07f23a3d58d9738758d823de0"
}
```

## inspiring_leader
```json
{
  "id": "inspiring_leader",
  "sourceObject": {
    "id": "inspiring_leader",
    "name": "Inspiring Leader",
    "description": "You can inspire others through stirring words.",
    "prerequisite": "Charisma 13 or higher",
    "effect": "You can spend 10 minutes inspiring your companions, giving them temporary hit points.",
    "type": "General",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "sourceObjectSha256": "ccf20f2fc5f38ad47473a963c27e49c6cfd5be9d2f2da6b314d71ba583e47d3e"
}
```

## empowered_summoning
```json
{
  "id": "empowered_summoning",
  "sourceObject": {
    "id": "empowered_summoning",
    "name": "Empowered Summoning",
    "description": "A charismatic summoner calls allies with increased health and damage.",
    "prerequisite": "Charisma 14+",
    "effect": "Creatures you summon gain temporary hit points equal to twice your proficiency bonus and add your proficiency bonus to the first damage roll they make each round.",
    "type": "Magic",
    "legacyEffect": "Summoned allies +10% HP and damage",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "afba301851de043876c6bb7d07d91ea717dd38a05ef6f2609540f0588a6bc31c"
}
```

## field_medic
```json
{
  "id": "field_medic",
  "sourceObject": {
    "id": "field_medic",
    "name": "Field Medic",
    "description": "Trained medical care stabilizes allies faster during combat.",
    "prerequisite": "Trained in Medicine",
    "effect": "You may use a healer’s kit as a bonus action. When you stabilize a creature, it gains temporary hit points equal to your proficiency bonus.",
    "type": "General",
    "legacyEffect": "Stabilize allies in combat faster",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "e12c23ca62a26cc73da76870d8066b93ea9e29e1518604d0e1e76b354ebc3dab"
}
```

## blood_ritual
```json
{
  "id": "blood_ritual",
  "sourceObject": {
    "id": "blood_ritual",
    "name": "Blood Ritual",
    "description": "Under the moon's gaze you bind flesh to curse through rites older than the cities of Aethel. Prestige lineage: Mooncursed. completed from the existing development record.)",
    "prerequisite": "Constitution 13+, level 4+",
    "effect": "Once per long rest, as part of a 10-minute ritual using your blood, you gain temporary hit points equal to twice your level and advantage on the next saving throw against curse or disease effects. Required for many lycanthropic oaths. Allies who witness the ritual and share a drop of blood gain half your temporary hit points (rounded down) for 1 hour.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "Once per long rest, as part of a 10-minute ritual using your blood, you gain temporary hit points equal to twice your level and advantage on the next saving throw against curse or disease effects. Required for many lycanthropic oaths. Allies who witness the ritual and share a drop of blood gain half your temporary hit points (rounded down) for 1 hour.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "5aaa8868de08ed8e614580b12164631975ce589856efeaf5c015ab44505904f7"
}
```

## necrotic_affinity
```json
{
  "id": "necrotic_affinity",
  "sourceObject": {
    "id": "necrotic_affinity",
    "name": "Necrotic Affinity",
    "description": "Death's chill is an old friend on Aethel's battlefields—you channel grave-cold through fist and focus without flinching, as if the Binding left a door ajar in your marrow. Prestige lineage: Gravetouched. completed from the existing development record.)",
    "prerequisite": "Proficiency in Religion or level 8+",
    "effect": "You have resistance to necrotic damage. Once per turn when you hit with a melee attack, you can deal an additional 1d6 necrotic damage. When you take necrotic damage from a spell or supernatural effect, you can use your reaction to absorb half of it (rounded down) and add that amount as temporary hit points until the end of your next turn. Creatures you kill with necrotic damage cannot be raised by effects of 5th level or lower for 24 hours.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You have resistance to necrotic damage. Once per turn when you hit with a melee attack, you can deal an additional 1d6 necrotic damage. When you take necrotic damage from a spell or supernatural effect, you can use your reaction to absorb half of it (rounded down) and add that amount as temporary hit points until the end of your next turn. Creatures you kill with necrotic damage cannot be raised by effects of 5th level or lower for 24 hours.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "c179a7e4246e9e668e859a699a56179c5ae85fe69d22691d7e9fda1cfe0b23ea"
}
```

## soul_cage
```json
{
  "id": "soul_cage",
  "sourceObject": {
    "id": "soul_cage",
    "name": "Soul Cage",
    "description": "You trap the departing in black crystal—voices pressed flat until you need their scream. Prestige lineage: Soulrender. completed from the existing development record.)",
    "prerequisite": "Lifeleech or spellcasting ability, level 8+",
    "effect": "When a hostile creature dies within 30 feet, you may bind its soul to a black crystal, storing up to 3 soul charges. Spend 1 charge to shield an ally for 2d8 temporary HP, or spend 2 charges to fire an Agony Lance (3d8 necrotic, save for half, and the target has disadvantage on the next healing it receives).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When a hostile creature dies within 30 feet, you may bind its soul to a black crystal, storing up to 3 soul charges. Spend 1 charge to shield an ally for 2d8 temporary HP, or spend 2 charges to fire an Agony Lance (3d8 necrotic, save for half, and the target has disadvantage on the next healing it receives).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "34a051cc5c242b04c7a7b784acbf69249adc0042ba2a27721ba3433283c9d1fc"
}
```

## lifeleech
```json
{
  "id": "lifeleech",
  "sourceObject": {
    "id": "lifeleech",
    "name": "Lifeleech",
    "description": "Your magic does not merely harm—it siphons the vigor that death has not yet claimed. Prestige lineage: Soulrender. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability",
    "effect": "When you deal necrotic damage with a spell, you regain hit points equal to half the necrotic damage dealt. When a hostile creature dies within 30 feet, you absorb a soul spark, gaining 1 soul charge (max 3). Soul charges can power Soul Cage abilities.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you deal necrotic damage with a spell, you regain hit points equal to half the necrotic damage dealt. When a hostile creature dies within 30 feet, you absorb a soul spark, gaining 1 soul charge (max 3). Soul charges can power Soul Cage abilities.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "sourceObjectSha256": "1ec74c9ea62fd5d8cd1ee136c1589d4b6b752b55adb162c35d54c783321fc932"
}
```

## Existing reviewed interfaces — preserve these while completing missing clauses


### docs/mechanics/FORM_TEMP_HP_PLAYTEST.md

File SHA256: b1b418b9ea9725e42f3c82d7abd41d049d4d534b6497cccc836b6ce250510096

Line91: Empowered Summoning offers2PB at actual creation, using default lifetime and removal if the recipient entity ends; later PB changes do not refill it. Field Medic's actual healer-kit stabilization happens first, then itsPB grant. Blood Ritual offers2×level to self and exactlylevel to each eligible witnessing/blood-sharing ally, independent of whatever shield wins the self comparison. Allies' lifetime is1 hour; self uses default. No HP payment is invented for a drop of blood. Blood Ritual target-count completion remains visible. Chef, Inspiring Leader and Soul Cage need their named completion batches; no unknown quantities or “healing disadvantage” are silently filled in.

Line93: **Necrotic Affinity's new pipeline bridge:** after ordinary defenses and passive necrotic resistance, letD be qualifying spell/supernatural necrotic damage before existing temporary HP. A legal Reaction preventsfloor(D/2). Existing shields then absorb the remaining packet, and ordinary HP/death/Wounds/prevention settle. If still a legal living holder, offerfloor(D/2) afterward until the holder's next regular end. This is prevention, not healing/transfer. D=1 can spend the Reaction but creates no grant. An actual death creates no corpse shield; living0 can receive it without stabilization. The event may invoke this transaction only once. Other feat clauses are outside this selected component review.


### docs/mechanics/HEALING_DEATH_PLAYTEST.md

File SHA256: 8d68794687b97da70aaff9953f9724e31e9fa3c8568fd4c2f9e8fd05d34c93f7

Line28: | actualHpDamage | NormalHP lost to the packet after true prevention; recovery and state-assignment loss excluded |

Line29: | actualDamageDealt | NEW anti-overkill bridge: tempAbsorbed plus actualHpDamage; numeric actual-damage drains/reflections |

Line31: Ordinary “damages,” “takes damage” and “damaging hit” predicates use a positive resolved packet. Actual-HP wording (Burning Blood/Rewind Wound) uses actualHpDamage. Numeric actual-damage wording (Sanguine Rite/Echo Leech/Merciful Smite/Wound Eater/Gravebrand) uses actualDamageDealt. Source attack/hit predicates remain distinct.

Line33: Example: HP10/temp10 takes5: numeric actual damage5, actualHP damage0, positive packet. HP1 under a floor takes5: numeric0 but positive packet. HP3 takes12: numeric3, raw post-temp12. HP0 takes1: numeric0, positive packet and normal death-failure consequences.

Line74: Within each permitted reduction plan: formula/bonuses; per-die adjustments; compatible exact fractional multipliers with one floor after multiplication; compatible flat reductions; floor at0; broad HP prohibition; maximum/Critical/reserve caps. Intrinsic Wound Eater and systemic Corrupted remain independent factors. Duplicate same-stat per-die penalties use the strongest. Dice remain dice when maximized/shared; flat Lay on Hands and stored numeric Echoes have zero healing dice.

Line78: Every present, operative, applicable next-positive-healing reduction consumes exactly once when the final event commits if its pre-reduction HP potential was positive. This includes reducers whose arithmetic branch lost to Totem or whose actual gain was later blocked. Zero potential and suppressed records consume none. Two-pass preview never consumes twice.

Line80: Critical at3Wounds caps ordinary healing at max(1, effective maximum minus1); it is not a maximumHP reduction and healing cannot lower currentHP. Reserve spends only actualHP restored. A final heal8 with room3 spends3 reserve; blocked healing spends0, other activation costs remain paid. Revival/form changes/encounter starts do not replenish reserve.

Line86: Actual positiveHP restoration is required for Radiance's cure, Renewal's Stamina, Sanctified Reprisal and Life Prophecy's RC trigger. Meditative Healing's laterKi and Transcendent Meditation's second-pulseKi are independent components and still resolve when healing caps/blocks. Blood Tithe uses its actual qualifying hostile Bleed-death trigger and finite use; not staged farming.

Line96: Stronger source flags override generic provenance: Vitality Link's child blocks every further link; Echo Leech blocks secondary healing/resource triggers; Blood Feast blocks damage/resource triggers; Merciful Smite blocks Smite/heal-copy chains; Crown Undying blocks redirection/heal-copy chains; Echoes/Spiral copies retain their explicit exclusions. Source payment and direct/actual-gain predicates still apply before a child exists.

Line100: OrdinaryMissingHP = effective maximum minus currentHP. Genuine excess is max(0, legal post-reduction healing minus OrdinaryMissingHP). Broad HP prohibition makes legal healing and excess0. Critical's ceiling does not redefine missingHP: max20/HP19/Critical/legalheal10 restores0 but has9 genuine excess; the missing1 is not excess. At HP20, legalheal10 has10 excess.

Line102: This quantity alone grants no conversion. A legal converter must satisfy its own costs/caps/cadences. One excess point can fund only one conversion. Source-internal Overflowing Light resolves before outside Cosmic Equilibrium uses remaining excess. Channel Life attaches a packet-wide prohibition on ALL excess-to-tempHP conversion, including another owner's feature. It permits an otherwise eligible Cosmic damage conversion.

Line104: **NEW agreed source exclusion:** Unpaid passive regeneration bounded by Mutation Recovery Reserve cannot supply excess-healing conversions unless a future source explicitly grants an exception. This covers Bloodthick Node, Rapid Coagulation, Regenerative Mutation and Bio-Stabilizer as a Bloodthick modifier. FullHP/Critical may compute mathematical excess but grants no Cosmic conversion and spends no Reserve. Do not extend this exclusion to otherwise eligible paid/finite healing merely because it restores0HP.


## Dependency and preservation check

All8 original feat objects and all335 registry entries remain preserved and byte-identical in the main project and review copy. Feat file SHA256842d14e868aa93d51fc6f21e39bc9dd3a1b872cdffcf467ffaa99a4cc3f779b6. Soul Cage explicitly names Lifeleech in prerequisites; Lifeleech explicitly says its charges power Soul Cage. Treat them together; do not create a second charge resource merely because they are two feats.

The new transformation conference also established immutable earliest physical origin: an object-origin creature cannot produce a soul, ordinary healing or corpse entitlement through anatomy changes. Creature-origin identity persists through object anatomy and back. No transformed object is an eligible manufactured soul farm. These remain constraints, not permission to invent a new generic soul economy.

Please answer the ten source questions with complete operational candidate objects for every clause of all eight feats, using exact source IDs, prerequisites and provenance. Identify any truly new numbers, durations, costs and anti-farm restrictions. Preserve distinctions between temporary HP, ordinary healing, stabilization, resurrection prohibition and actual soul custody. Point out new dependent sources that must be read rather than silently copying their effects. The complete objects, code and tests will return for independent implementation review before promotion.
