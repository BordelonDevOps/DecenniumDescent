"""Actual-operation history for the upcoming Time Loop parent adapter.

This observes the existing canonical Druid/TransformationWorld objects. It is
not a second world and does not restore anything. Begin observing before forms
or casts are created; historical import is deliberately not inferred from a
current expiry/state flag. A host holds its scene lock around each operation.

Ordinary source legality, saves and geometry remain the existing helper's host
inputs. A failing ordinary operation that already mutated state is recorded as
failed and poisons temporal admission; this module does not invent a rollback
for an already committed cast or reroll its save. No failed call earns a receipt.
"""
from dataclasses import fields, dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from control_playtest_rules import ClockMarker, clock_marker
from form_temphp_playtest_rules import DruidState, DruidStats, FormInstance, OwnerRechargeClock
from transformation_spell_playtest_rules import (
    TransformationWorld, ConcentrationLedger, Body, PhysicalOrigin, Cast, Link,
    CastStats, CastPrice, Selection,
)
from temporal_playtest_rules import ident, require, Wallet
from spell_playtest_rules import quote_cast, integer, SpellRuleError


@dataclass(frozen=True)
class CasterAuthority:
    """Host-owned current source inputs, bound once instead of supplied per cast.

    Source-specific discounts, free casts/copies, traumatic casting and cadence
    application need their own class transaction. A fabricated price or boolean
    discount flag cannot assert those permissions in this ordinary-price layer.
    """
    stats: CastStats
    class_level: int
    max_rp: int
    casting_modifier: int
    available_spell_ids: frozenset
    cadence: dict


_CATALOG_PATH=Path(__file__).resolve().parents[1]/'data/public/spell_playtests/catalog.json'
_CATALOG={s['id']:s for s in json.loads(_CATALOG_PATH.read_text(encoding='utf-8'))['spells']}


SCHEMAS = {
    TransformationWorld: frozenset('buffers concentration bodies casts links slots druids damage_rounds damage_events regular_ends commands events'.split()),
    ConcentrationLedger: frozenset(('current',)),
    DruidState: frozenset('owner circle buffers cadence creatures current instances long_epoch short_epoch regular_index recharges recharge_clock rest_uses attuned shifts buffer_capacity reserve surges surge_capacity'.split()),
    OwnerRechargeClock: frozenset('mode now next_tick ticks last_regular anchored'.split()),
}
VALUE_TYPES = (ClockMarker, FormInstance, PhysicalOrigin, Cast, Link, CastStats, DruidStats, Selection)
FINITE_DRUID_FIELDS = tuple('long_epoch short_epoch regular_index recharges rest_uses attuned shifts buffer_capacity reserve surges surge_capacity'.split())


def leaf(value):
    """Exact data projection, never deepcopy a world or callback."""
    if value is None or type(value) in (str, int, bool, Fraction):
        return value
    if type(value) in (tuple, list, set, frozenset):
        return type(value)(leaf(v) for v in value)
    if type(value) is dict:
        return {leaf(k): leaf(v) for k, v in value.items()}
    require(type(value) in VALUE_TYPES, 'Unclassified parent value: '+type(value).__name__)
    names = {f.name for f in fields(value)}
    require(set(vars(value)) == names, 'Unclassified parent value fields')
    return {f.name: leaf(getattr(value, f.name)) for f in fields(value)}


def wire(value):
    """Stable digest encoding, including sets, fractions and typed keys."""
    if value is None or type(value) in (str, int, bool):
        return value
    if type(value) is Fraction:
        return ['fraction', value.numerator, value.denominator]
    if type(value) is dict:
        pairs = [[wire(k), wire(v)] for k,v in value.items()]
        return ['dict', sorted(pairs, key=lambda v: json.dumps(v[0],sort_keys=True))]
    if type(value) in (tuple,list,set,frozenset):
        rows = [wire(v) for v in value]
        if type(value) in (set,frozenset): rows.sort(key=lambda v: json.dumps(v,sort_keys=True))
        return [type(value).__name__, rows]
    return wire(leaf(value))


def digest(value):
    return sha256(json.dumps(wire(value),separators=(',',':'),sort_keys=True).encode()).hexdigest()


def exact(holder, cls):
    require(type(holder) is cls, 'Wrong canonical parent holder type')
    expected = SCHEMAS.get(cls)
    if expected is None:
        expected = {f.name for f in fields(cls)}
    require(set(vars(holder)) == set(expected), 'Unclassified parent holder schema: '+cls.__name__)


class TemporalParentHistory:
    """One observational journal over the actual shared parent objects.

    Event IDs are host IDs shared with the rest of the scene. They may never be
    reused here. In initiative the ID and time must equal the scheduler's actual
    active atomic event. Outside events are explicitly recorded before entering
    initiative, not relabeled as encounter turn zero.
    """
    def __init__(self, world, *, wallets, druid_stats, casters, scheduler=None):
        exact(world, TransformationWorld);exact(world.concentration, ConcentrationLedger)
        require(not world.casts and not world.links and not world.concentration.current,
                'Observe before source creation; current state is not historical proof')
        require(all(d.current is None and not d.instances for d in world.druids.values()),
                'Observe Druid before first form; historical import requires a separate adapter')
        require(type(wallets) is dict and all(k in world.bodies for k in wallets),
                'Supply the actual host actor wallet registry')
        require(len({id(w) for w in wallets.values()})==len(wallets),'Distinct owners cannot alias wallets')
        for wallet in wallets.values():exact(wallet,Wallet)
        require(type(druid_stats) is dict and set(druid_stats)==set(world.druids),'Bind every actual current Druid stat record')
        require(type(casters) is dict,'Bind the actual current caster authorities')
        self.world=world;self.wallets=wallets;self.druid_stats=druid_stats;self.casters=casters
        self.scheduler=scheduler;self.mode='outside'
        self.events=();self.receipts=();self.failures=();self.used=set()
        self.last_time=ClockMarker(0);self.chain='parent-history-v1'
        self._events=();self._receipts=();self._failures=();self._chain=self.chain
        self._mode=self.mode;self._last_time=self.last_time;self._scheduler_binding=None
        self._pins={};self._slot_pins={};self._pin_manifest={};self._slot_manifest={}
        self._initial=self._state()
        self._expected=leaf(self._initial)
        self._expected_finite=self._finite_state()
        self._bind_world()
        self._pin_objects()
        self._validate_authorities()

    def _bind_world(self):
        w=self.world
        self._world_binding=(w,w.buffers,w.concentration,w.bodies,w.druids,w.casts,w.links,self.wallets)
        self._wallet_bindings=dict(self.wallets)
        self._stat_registry=self.druid_stats;self._caster_registry=self.casters
        self._stats_bindings=dict(self.druid_stats);self._caster_bindings=dict(self.casters)
        self._stats_values={k:leaf(v) for k,v in self.druid_stats.items()}
        self._caster_values={k:(id(c.stats),leaf(c.stats),c.class_level,c.max_rp,c.casting_modifier,
                                leaf(c.available_spell_ids),id(c.cadence)) for k,c in self.casters.items()}
        self._druid_bindings={a:(d,d.buffers,d.cadence,d.creatures,d.recharge_clock,d.instances)
                              for a,d in w.druids.items()}

    def _pin_objects(self):
        self._validate_pin_manifests()
        w=self.world
        for domain,registry in (('body',w.bodies),('cast',w.casts),('link',w.links)):
            for key,obj in registry.items():
                k=(domain,key)
                require(k not in self._pins or self._pins[k] is obj,'Canonical parent identity replaced')
                self._pins[k]=obj
                self._pin_manifest.setdefault(k,obj)
        for owner,d in w.druids.items():
            for key,obj in d.instances.items():
                k=('form',owner,key)
                require(k not in self._pins or self._pins[k] is obj,'Canonical form identity replaced')
                self._pins[k]=obj
                self._pin_manifest.setdefault(k,obj)
        for owner,slot in w.concentration.current.items():
            require(type(slot) is tuple and len(slot)==2 and type(slot[0]) is str and callable(slot[1]),
                    'Malformed actual concentration slot')
            self._slot_pins[id(slot)]=slot
            self._slot_manifest.setdefault(id(slot),(slot,slot[1]))

    def _validate_pin_manifests(self):
        require(set(self._pins)==set(self._pin_manifest) and
                all(self._pins[k] is v for k,v in self._pin_manifest.items()),
                'Canonical parent pin manifest changed')
        require(set(self._slot_pins)==set(self._slot_manifest) and
                all(self._slot_pins[k] is slot and slot[1] is callback
                    for k,(slot,callback) in self._slot_manifest.items()),
                'Historical concentration pin manifest changed')

    def _state(self):
        w=self.world;exact(w,TransformationWorld);exact(w.concentration,ConcentrationLedger)
        for registry in (w.bodies,w.casts,w.links,w.slots,w.druids,w.commands,w.concentration.current):
            require(type(registry) is dict,'Parent registry must be a dictionary')
        require(all(type(getattr(w,n)) is set for n in ('damage_rounds','damage_events','regular_ends'))
                and type(w.events) is list,'Canonical transformation history collections required')
        bodies={}
        for key,b in w.bodies.items():
            exact(b,Body);exact(b.origin,PhysicalOrigin)
            require(key==b.identity,'Body dictionary/origin mismatch')
            require(all(type(getattr(b,n)) is set for n in ('equipment','melded','lost_items')),
                    'Canonical gear sets required')
            bodies[key]={n:leaf(v) for n,v in vars(b).items() if n!='life'}
            bodies[key]['lifeIdentity']=id(b.life)
            bodies[key]['originIdentity']=id(b.origin)
        druids={}
        for key,d in w.druids.items():
            exact(d,DruidState);exact(d.recharge_clock,OwnerRechargeClock)
            require(key==d.owner and key in w.bodies and d.buffers is w.buffers,'Druid owner/shared buffer alias mismatch')
            require(type(d.instances) is dict and type(d.rest_uses) is dict and type(d.recharges) is dict,
                    'Druid canonical dictionaries required')
            require(type(d.cadence) is dict and set(d.cadence)>={'refrain','rememberedSpell','dissonance'},
                    'Canonical current cadence required')
            for ident_,f in d.instances.items():
                exact(f,FormInstance)
                require(ident_==f.instance_id and type(f.spent) is set,'Form identity/permission set mismatch')
            require(d.current is None or d.instances.get(d.current.instance_id) is d.current,
                    'Current form is not the canonical instance')
            # Finite resources/cadence/clock stay current and are never a source
            # of fabricated renewal receipts. Their actual before/after values
            # are captured by each event, not reset to historical values.
            druids[key]={'current':None if d.current is None else d.current.instance_id,
                         'instances':{k:leaf(f) for k,f in d.instances.items()},
                         'owner':d.owner,'circle':d.circle}
        casts={};links={};concentration={}
        for key,c in w.casts.items():
            exact(c,Cast);require(key==c.identity,'Cast identity mismatch');casts[key]=leaf(c)
        for key,l in w.links.items():
            exact(l,Link);require(key==l.identity and l.cast_id in w.casts,'Link parent/identity mismatch')
            links[key]=leaf(l)
        for owner,slot in w.concentration.current.items():
            require(type(slot) is tuple and len(slot)==2 and type(slot[0]) is str and callable(slot[1]),
                    'Malformed actual concentration slot')
            concentration[owner]=(slot[0],id(slot),id(slot[1]))
        return {'bodies':bodies,'casts':casts,'links':links,'druids':druids,
                'slots':leaf(w.slots),'concentration':concentration,
                'formIdentities':leaf(w.buffers.form_instances),'spellAnatomies':leaf(w.buffers.spell_anatomies),
                'damageRounds':leaf(w.damage_rounds),'damageEvents':leaf(w.damage_events),
                'regularEnds':leaf(w.regular_ends),'commands':leaf(w.commands),'worldEvents':leaf(w.events)}

    def _economy(self, wallets=()):
        return {'wallets':tuple({k:leaf(v) for k,v in vars(w).items()} for w in wallets),
            'sourceAuthorities':{'druidStats':{k:leaf(v) for k,v in self.druid_stats.items()},
              'casters':{k:{'stats':leaf(c.stats),'classLevel':c.class_level,'maxRP':c.max_rp,
                          'castingModifier':c.casting_modifier,'available':leaf(c.available_spell_ids),
                          'cadence':leaf(c.cadence)} for k,c in self.casters.items()}},
            'druids':{a:{n:leaf(getattr(d,n)) for n in ('long_epoch','short_epoch','regular_index',
                       'recharges','rest_uses','attuned','shifts','buffer_capacity','reserve',
                       'surges','surge_capacity','cadence')}
                       | {'rechargeClock':leaf(vars(d.recharge_clock))}
                       for a,d in self.world.druids.items()}}

    def _finite_state(self):
        # Cadence belongs to the shared casting interface and may change there.
        # Druid-owned resources/rests/recharge must pass an observed operation.
        return {a:{n:leaf(getattr(d,n)) for n in FINITE_DRUID_FIELDS}
                  | {'rechargeClock':leaf(vars(d.recharge_clock))}
                for a,d in self.world.druids.items()}

    def validate(self):
        w=self.world
        require(all(a is b for a,b in zip(self._world_binding,
                    (w,w.buffers,w.concentration,w.bodies,w.druids,w.casts,w.links,self.wallets))),
                'Canonical parent world alias changed')
        require(set(self.wallets)==set(self._wallet_bindings) and
                all(self.wallets[k] is v for k,v in self._wallet_bindings.items()),
                'Canonical parent wallet registry changed')
        for wallet in self.wallets.values():exact(wallet,Wallet)
        self._validate_authorities()
        require(self.mode==self._mode and self.last_time==self._last_time,'Parent history clock/mode changed')
        if self.mode=='initiative':
            require(self.scheduler is self._scheduler_binding,'Canonical parent scheduler changed')
        require(set(w.druids)==set(self._druid_bindings),'Druid registry changed after observation began')
        for owner,bound in self._druid_bindings.items():
            d=w.druids[owner]
            require(all(a is b for a,b in zip(bound,(d,d.buffers,d.cadence,d.creatures,d.recharge_clock,d.instances))),
                    'Canonical Druid alias changed')
        require(self.events==self._events and self.receipts==self._receipts and self.failures==self._failures
                and self.chain==self._chain,'Parent historical record was replaced or edited')
        require(self.used=={e['eventId'] for e in self.events},'Parent event history mismatch')
        require(not self.failures,'Failed mutating source operation needs host reconciliation')
        self._validate_pin_manifests()
        current=self._state()
        require(current==self._expected,'Unobserved parent lifecycle mutation; no historical receipt')
        require(self._finite_state()==self._expected_finite,
                'Unobserved Druid finite economy or recharge mutation')
        for key,obj in self._pins.items():
            if key[0]=='form':current_obj=w.druids[key[1]].instances.get(key[2])
            else:current_obj={'body':w.bodies,'cast':w.casts,'link':w.links}[key[0]].get(key[1])
            require(current_obj is obj,'Canonical parent object was replaced or removed')
        for slot in w.concentration.current.values():
            require(self._slot_pins.get(id(slot)) is slot,'Unrecorded concentration slot identity')
        return current

    def _validate_authorities(self):
        require(self.druid_stats is self._stat_registry and self.casters is self._caster_registry,
                'Canonical stat authority registry changed')
        require(set(self.druid_stats)==set(self._stats_bindings) and set(self.casters)==set(self._caster_bindings),
                'Stat/source progression changed; exact update adapter required')
        for owner,stats_ in self.druid_stats.items():
            exact(stats_,DruidStats)
            require(stats_ is self._stats_bindings[owner] and leaf(stats_)==self._stats_values[owner]
                    and stats_.owner==owner,'Canonical current Druid stats changed')
        for owner,c in self.casters.items():
            exact(c,CasterAuthority);exact(c.stats,CastStats)
            require(c is self._caster_bindings[owner] and owner in self.wallets and c.stats.owner==owner,
                    'Canonical caster authority changed')
            current=(id(c.stats),leaf(c.stats),c.class_level,c.max_rp,c.casting_modifier,leaf(c.available_spell_ids),id(c.cadence))
            require(current==self._caster_values[owner],'Current caster source authority changed')
            integer(c.class_level,'class level',1,20);integer(c.max_rp,'max RP',0)
            integer(c.casting_modifier,'signed casting modifier',-5,10)
            require(c.stats.modifier==max(1,c.casting_modifier),'Caster M differs from current signed modifier')
            require(type(c.available_spell_ids) is frozenset and type(c.cadence) is dict
                    and set(c.cadence)>={'refrain','rememberedSpell','dissonance'},'Canonical repertoire/cadence required')
            if owner in self.world.druids:
                require(c.cadence is self.world.druids[owner].cadence,'Druid casting must use the same cadence')

    def _druid_stats(self,stats_):
        self._validate_authorities()
        require(type(stats_) is DruidStats and self.druid_stats.get(stats_.owner) is stats_,
                'Use the bound current Druid statistics, not per-call substitute statistics')

    def _cast_stats(self,stats_):
        self._validate_authorities()
        require(type(stats_) is CastStats and stats_.owner in self.casters
                and self.casters[stats_.owner].stats is stats_,'Use the bound current casting statistics')

    def quote_price(self,owner,spell_id):
        """Derive ordinary payment from actual catalog/current canonical inputs."""
        self.validate();require(owner in self.casters and spell_id in _CATALOG,'No bound ordinary casting source')
        c=self.casters[owner];cadence=c.cadence
        quote=quote_cast(_CATALOG[spell_id],c.stats.source_class,c.class_level,
            available_spell_ids=c.available_spell_ids,rp=self.wallets[owner].rp,max_rp=c.max_rp,
            dissonance=cadence['dissonance'],proficiency=c.stats.pb,casting_modifier=c.casting_modifier,
            previous_spell_id=cadence['rememberedSpell'],previous_refrain=cadence['refrain'])
        return CastPrice.from_quote(quote)

    def enter_initiative(self):
        self.validate();s=self.scheduler
        require(self.mode=='outside' and s is not None and s.atomic_event is None
                and not s.completed_events and s.iteration==0 and s.round==1 and s.turn_ordinal==0,
                'Enter only at the original complete initiative boundary')
        require(s.now>=self.last_time,'Initiative clock predates recorded source history')
        self.mode='initiative';self._mode=self.mode;self._scheduler_binding=s

    def _begin(self,event_id,now,operation,actor):
        current=self.validate();ident(event_id);ident(actor)
        marker=clock_marker(now)
        require(event_id not in self.used and marker>=self.last_time,'Repeated event or backward parent clock')
        if self.mode=='initiative':
            s=self.scheduler
            require(s.atomic_event==event_id and s.now==marker,'Actual canonical atomic parent event required')
            origin={'encounter':s.encounter,'iteration':s.iteration,'round':s.round,
                    'turn':None if s.active_regular is None else s.active_regular.token()}
        else:
            require(self.mode=='outside','Unknown parent history mode')
            origin={'kind':'OUTSIDE_EVENT','operation':operation,'timestamp':leaf(marker)}
        return {'eventId':event_id,'time':leaf(marker),'operation':operation,'actor':actor,
                'origin':origin,'before':current,'marker':marker}

    def _finish(self,frame,before_economy,wallets,*,failed=False):
        after=self._state();event={k:leaf(v) for k,v in frame.items() if k not in ('marker','before')}
        event.update({'beforeHash':digest(frame['before']),'afterHash':digest(after),
                      'economyBefore':before_economy,'economyAfter':self._economy(wallets),'failed':failed})
        receipts=[]
        if not failed:
            before=frame['before']
            for owner,row in after['druids'].items():
                old=before['druids'][owner]['instances']
                for fid,f in row['instances'].items():
                    prior=old.get(fid)
                    if prior is None:
                        receipts.append({'kind':'form-created','owner':owner,'formId':fid,'source':f['source_id'],
                                         'initial':f,'origin':event['origin']})
                    elif prior['expiry']!=f['expiry']:
                        receipts.append({'kind':'form-renewed','owner':owner,'formId':fid,
                            'oldExpiry':prior['expiry'],'newExpiry':f['expiry'],
                            'shiftBefore':before_economy['druids'][owner]['shifts'],
                            'shiftAfter':event['economyAfter']['druids'][owner]['shifts']})
                    if prior is not None and prior['state']!=f['state']:
                        receipts.append({'kind':'form-ended','owner':owner,'formId':fid,
                                         'oldState':prior['state'],'newState':f['state']})
            for cid,c in after['casts'].items():
                if cid not in before['casts']:
                    slot=after['concentration'].get(c['caster'])
                    cast_origin=leaf(event['origin'])
                    if cast_origin.get('kind')=='OUTSIDE_EVENT':cast_origin['kind']='OUTSIDE_CAST'
                    receipts.append({'kind':'cast-created','castId':cid,'initial':c,
                                     'origin':cast_origin,'concentrationBinding':slot})
            for lid,l in after['links'].items():
                prior=before['links'].get(lid)
                if prior is None:receipts.append({'kind':'link-created','linkId':lid,'initial':l})
                elif prior['state']!=l['state']:
                    receipts.append({'kind':'link-stabilized' if l['state']=='permanent' else 'link-ended',
                                     'linkId':lid,'oldState':prior['state'],'newState':l['state'],
                                     'originalDeadline':l['deadline']})
            for owner in before['concentration'].keys()|after['concentration'].keys():
                old=before['concentration'].get(owner);new=after['concentration'].get(owner)
                if old!=new:receipts.append({'kind':'concentration-transition','owner':owner,'old':old,'new':new})
        integrity_error=None
        if not failed:
            try:self._check_transitions(frame,after,receipts)
            except SpellRuleError as error:
                integrity_error=error;failed=True;event['failed']=True
                event['integrityFailure']=str(error);receipts=[]
        for row in receipts:row.update({'eventId':event['eventId'],'time':event['time'],
                                       'operation':event['operation']})
        self.used.add(event['eventId']);self.events=self.events+(leaf(event),)
        self.receipts=self.receipts+tuple(leaf(r) for r in receipts)
        if failed and (integrity_error is not None or frame['before']!=after or before_economy!=event['economyAfter']):
            self.failures=self.failures+(event['eventId'],)
        self.chain=digest((self.chain,event,receipts))
        # Detached copies detect accidental mutation of public audit projections.
        self._events=leaf(self.events);self._receipts=leaf(self.receipts)
        self._failures=leaf(self.failures);self._chain=self.chain
        self._expected=leaf(after);self.last_time=frame['marker'];self._last_time=self.last_time
        if not failed:self._pin_objects()
        self._expected_finite=self._finite_state()
        if integrity_error is not None:raise integrity_error

    def _check_transitions(self,frame,after,receipts):
        """Permit only lifecycle receipts caused by this exact native operation."""
        op=frame['operation'];actor=frame['actor'];before=frame['before'];request=frame['request']
        forms={};links={};new_forms=set();new_casts=set();new_links=set()
        if op=='druid-shift':
            new_forms.add((actor,request['formId']))
            old=before['druids'][actor]['current']
            if old:forms[(actor,old)]='changed'
        elif op in ('druid-renew','druid-revert','finalized-damage') and actor in before['druids']:
            old=before['druids'][actor]['current']
            if old:forms[(actor,old)]={'druid-renew':'expired','druid-revert':'voluntary-reversion',
                                      'finalized-damage':'forced-reversion'}[op]
        if op=='spell-cast':
            cid=request['castId'];new_casts.add(cid)
            new_links={cid+':'+target for target in request['targets']}
            old_slot=before['concentration'].get(actor)
            for lid,l in before['links'].items():
                if old_slot and l['cast_id']==old_slot[0] and l['state']=='shaping':links[lid]='new-concentration'
                elif l['target'] in request['targets'] and l['state'] in ('shaping','permanent'):links[lid]='replaced'
            for owner in request['targets']:
                if owner in before['druids']:
                    fid=before['druids'][owner]['current']
                    if fid:forms[(owner,fid)]='spell-transformation'
        elif op.startswith('concentration-'):
            slot=before['concentration'].get(actor)
            if slot:
                links={lid:op.removeprefix('concentration-') for lid,l in before['links'].items()
                       if l['cast_id']==slot[0] and l['state']=='shaping'}
        elif op=='spell-checkpoint':
            links={lid:'permanent' if before['casts'][l['cast_id']]['spell_id']=='true-polymorph' else 'expired'
                   for lid,l in before['links'].items()
                   if l['state']=='shaping' and frame['marker'].seconds>=l['deadline']}
        elif op in ('spell-dispel','spell-repeat-save','spell-willing-rejection','finalized-damage'):
            target=request.get('target',actor);lid=before['bodies'][target]['anatomy']
            if lid:
                links[lid]={'spell-dispel':'dispelled','spell-repeat-save':'repeat-save',
                            'spell-willing-rejection':'willing-rejection',
                            'finalized-damage':('physical-destruction','forced-reversion')}[op]
        allowed_concentration={before['casts'][before['links'][lid]['cast_id']]['caster'] for lid in links}
        if op=='spell-cast' or op.startswith('concentration-'):allowed_concentration.add(actor)
        for r in receipts:
            kind=r['kind'];allowed=False
            if kind=='form-created':allowed=(r['owner'],r['formId']) in new_forms
            elif kind=='form-renewed':
                allowed=(op=='druid-renew' and r['owner']==actor
                         and r['formId']==before['druids'][actor]['current'])
            elif kind=='form-ended':allowed=forms.get((r['owner'],r['formId']))==r['newState']
            elif kind=='cast-created':allowed=r['castId'] in new_casts and r['initial']['caster']==actor
            elif kind=='link-created':allowed=r['linkId'] in new_links and r['initial']['cast_id']==request['castId']
            elif kind in ('link-ended','link-stabilized'):
                expected=links.get(r['linkId'])
                allowed=r['newState'] in expected if type(expected) is tuple else r['newState']==expected
            elif kind=='concentration-transition':
                allowed=(r['owner'] in allowed_concentration and
                         (r['new'] is None or (op=='spell-cast' and r['owner']==actor and r['new'][0]==request['castId'])))
            require(allowed,'Unexpected parent transition for '+op+': '+kind)
        require(set(after['casts'])-set(before['casts'])==new_casts,'Unexpected cast creation count')
        if op=='druid-shift':
            require({(r['owner'],r['formId']) for r in receipts if r['kind']=='form-created'}==new_forms,
                    'Shift must create exactly its requested form')

    def _save_resolver(self,resolver):
        """A save may resolve its own combat history, but no parent operation.

        Detect actual nested native form/cast/resource mutations before they can
        be attributed to the enclosing cast. Partial committed calls stay failed.
        """
        def resolve(target,dc):
            before=(self._state(),self._economy(tuple(self.wallets.values())))
            result=resolver(target,dc)
            require(before==(self._state(),self._economy(tuple(self.wallets.values()))),
                    'Save resolver changed parent lifecycle or source economy')
            require(type(result) is bool,'Authoritative save resolver must return a boolean')
            return result
        return resolve

    def _wallet(self,owner,wallet):
        require(owner in self.wallets and self.wallets[owner] is wallet,
                'Use the actual canonical owner wallet; duplicate payment balances are unsupported')
        return wallet

    def _run(self,event_id,now,operation,actor,call,*,wallets=(),request=None):
        frame=self._begin(event_id,now,operation,actor);economy=self._economy(wallets)
        frame['request']=leaf({} if request is None else request)
        try:result=call()
        except Exception:
            self._finish(frame,economy,wallets,failed=True)
            raise
        self._finish(frame,economy,wallets)
        return result

    def shift(self,event_id,stats,source_id,instance_id,now,wallet,**options):
        self._druid_stats(stats)
        self._wallet(stats.owner,wallet)
        d=self.world.druids[stats.owner]
        return self._run(event_id,now,'druid-shift',stats.owner,
            lambda:d.shift(stats,source_id,instance_id,now,wallet,**options),wallets=(wallet,),request={'formId':instance_id})

    def renew(self,event_id,stats,now,*,renew=True):
        self._druid_stats(stats)
        d=self.world.druids[stats.owner]
        return self._run(event_id,now,'druid-renew',stats.owner,
            lambda:d.natural_endpoint(stats,now,renew=renew))

    def revert(self,event_id,owner,now,wallet,*,legal):
        self._wallet(owner,wallet)
        return self._run(event_id,now,'druid-revert',owner,
            lambda:self.world.druids[owner].revert(now,wallet,legal=legal),wallets=(wallet,))

    def special(self,event_id,stats,now,wallet,special_id,*,legal):
        self._druid_stats(stats)
        self._wallet(stats.owner,wallet)
        return self._run(event_id,now,'druid-special',stats.owner,
            lambda:self.world.druids[stats.owner].special(stats,now,wallet,special_id,legal=legal),wallets=(wallet,))

    def mooncursed_howl(self,event_id,stats,now,wallet,recipients,shared_roll,grant_ids,*,legal):
        self._druid_stats(stats)
        self._wallet(stats.owner,wallet)
        return self._run(event_id,now,'druid-mooncursed-howl',stats.owner,
            lambda:self.world.druids[stats.owner].mooncursed_howl(stats,now,wallet,recipients,shared_roll,grant_ids,legal=legal),
            wallets=(wallet,))

    def druid_attack(self,event_id,stats,now,wallet,*,legal):
        self._druid_stats(stats)
        self._wallet(stats.owner,wallet)
        return self._run(event_id,now,'druid-attack',stats.owner,
            lambda:self.world.druids[stats.owner].attack(stats,now,wallet,legal=legal),wallets=(wallet,))

    def spell_form_attack(self,event_id,target,stats,now,wallet,*,legal):
        self._cast_stats(stats)
        self._wallet(target,wallet)
        return self._run(event_id,now,'spell-form-attack',target,
            lambda:self.world.attack(target,stats,now,wallet,legal=legal),wallets=(wallet,))

    def cast(self,event_id,cast_id,spell_id,stats,price,wallet,selections,now,regular_index,**options):
        self._cast_stats(stats)
        self._wallet(stats.owner,wallet)
        require(type(price) is CastPrice,'Actual canonical CastPrice required')
        expected=self.quote_price(stats.owner,spell_id)
        require(digest(vars(price))==digest(vars(expected)),
                'Cast price must match current canonical ordinary quote; unsupported reduction or stale quote')
        options=dict(options);options['resolve_save']=self._save_resolver(options['resolve_save'])
        return self._run(event_id,now,'spell-cast',stats.owner,
            lambda:self.world.cast(cast_id,spell_id,stats,price,wallet,selections,now,regular_index,**options),wallets=(wallet,),
            request={'castId':cast_id,'spellId':spell_id,'targets':tuple(s.target for s in selections)})

    def checkpoint(self,event_id,now,*,started_packets_and_due_saves_finished):
        return self._run(event_id,now,'spell-checkpoint','world',
            lambda:self.world.checkpoint(now,started_packets_and_due_saves_finished=started_packets_and_due_saves_finished))

    def end_concentration(self,event_id,owner,now,*,reason):
        require(reason in ('failed-save','incapacitated','voluntary-release'),
                'Use the exact supported ordinary concentration ending')
        return self._run(event_id,now,'concentration-'+reason,owner,
            lambda:self.world.concentration.end(owner,reason))

    def dispel(self,event_id,actor,target,now,*,legal):
        return self._run(event_id,now,'spell-dispel',actor,lambda:self.world.dispel(target,legal=legal),request={'target':target})

    def set_suppressed(self,event_id,actor,target,now,*,suppressed,legal):
        return self._run(event_id,now,'spell-suppression',actor,
            lambda:self.world.set_suppressed(target,now,suppressed=suppressed,legal=legal))

    def finalize_damage(self,event_id,target,now,*,incapacitated,dead,destroyed=False,unsupported=False):
        body=self.world.bodies[target]
        hp=body.life['hp'] if type(body.life) is dict else body.life.hp
        def call():
            result=self.world.finalize_damage_state(target,actual_hp=hp,incapacitated=incapacitated,
                dead=dead,destroyed=destroyed,unsupported=unsupported)
            druid=self.world.druids.get(target)
            if druid:result['druid']=druid.finalize_damage_state(actual_hp=hp,incapacitated=incapacitated,dead=dead,unsupported=unsupported)
            return result
        return self._run(event_id,now,'finalized-damage',target,call)

    def repeat_save(self,event_id,target,stats,now,**options):
        self._cast_stats(stats)
        return self._run(event_id,now,'spell-repeat-save',target,
            lambda:self.world.repeat_save(target,stats,now,**options))

    def reject_spell(self,event_id,target,now,wallet,**options):
        self._wallet(target,wallet)
        return self._run(event_id,now,'spell-willing-rejection',target,
            lambda:self.world.reject(target,now,wallet,**options),wallets=(wallet,))

    def switch_shapechange(self,event_id,target,profile,now,regular_index,wallet,**options):
        self._wallet(target,wallet)
        return self._run(event_id,now,'shapechange-switch',target,
            lambda:self.world.switch_shapechange(target,profile,now,regular_index,wallet,**options),wallets=(wallet,))

    def acquire_gear(self,event_id,target,item_id,now,*,compatible_and_equipped):
        return self._run(event_id,now,'gear-acquired',target,
            lambda:self.world.acquire_external_gear(target,item_id,now,compatible_and_equipped=compatible_and_equipped))

    def lose_gear(self,event_id,target,item_id,now,*,actual_loss):
        return self._run(event_id,now,'gear-lost',target,
            lambda:self.world.mark_item_lost(target,item_id,actual_loss=actual_loss))

    def check_placement(self,event_id,target,now,*,fits_at_current_anchor):
        return self._run(event_id,now,'placement-check',target,
            lambda:self.world.check_reversion_placement(target,fits_at_current_anchor=fits_at_current_anchor))

    def clear_placement(self,event_id,target,now,*,canonical_resolution_completed):
        return self._run(event_id,now,'placement-resolved',target,
            lambda:self.world.clear_geometry_conflict(target,canonical_resolution_completed=canonical_resolution_completed))

    def druid_regular_start(self,event_id,owner):
        s=self.scheduler
        require(self.mode=='initiative' and s is not None and s.active_regular is not None
                and s.active_regular.actor==owner and s.active_regular.iteration==s.iteration
                and s.turn_phase=='start','Authenticated actual Druid regular start required')
        return self._run(event_id,s.now,'druid-regular-start',owner,
            lambda:self.world.druids[owner].regular_start(s.global_regular,s.now,actual_regular_marker=True))

    def druid_clock_transition(self,event_id,owner,now,*,transition):
        require(transition in ('leave','advance','enter'),'Exact ordinary initiative clock transition required')
        c=self.world.druids[owner].recharge_clock
        call={'leave':c.leave_initiative,'advance':c.advance_outside,'enter':c.enter_initiative}[transition]
        return self._run(event_id,now,'druid-clock-'+transition,owner,lambda:call(now))

    def druid_rest(self,event_id,stats,epoch,now,*,kind,attuned=(),actual_completed):
        self._druid_stats(stats)
        require(kind in ('short','long'),'Actual short or long rest required')
        d=self.world.druids[stats.owner]
        call=(lambda:d.completed_long_rest(stats,epoch,attuned=attuned,actual_completed=actual_completed,now=now)) if kind=='long' else (
            lambda:d.completed_short_rest(epoch,actual_completed=actual_completed,now=now))
        return self._run(event_id,now,'druid-rest-'+kind,stats.owner,call)

    def records(self,kind,identity):
        self.validate()
        return tuple(leaf(r) for r in self.receipts if r['kind']==kind and
                     identity in (r.get('formId'),r.get('castId'),r.get('linkId')))

    def _query_time(self,now):
        if self.mode=='initiative':
            marker=self.scheduler.now if now is None else clock_marker(now)
            require(marker==self.scheduler.now,'Evidence query must use current canonical scheduler time')
        else:
            require(now is not None,'Outside evidence query needs the actual world time')
            marker=clock_marker(now)
        require(marker>=self.last_time,'Evidence query cannot predate observed history')
        return marker

    def valid_form_deadline(self,owner,form_id,now=None):
        """Evidence for later planning, not permission to reactivate anatomy."""
        self.validate();current_time=self._query_time(now)
        d=self.world.druids[owner];f=d.instances[form_id]
        created=self.records('form-created',form_id)
        require(len(created)==1 and created[0]['owner']==owner,'Missing unique actual form creation')
        endpoint=created[0]['initial']['expiry']
        for row in self.records('form-renewed',form_id):
            require(row['owner']==owner and row['oldExpiry']==endpoint,'Broken same-instance renewal chain')
            endpoint=row['newExpiry']
        require(endpoint==leaf(f.expiry),'Current form endpoint lacks an actual renewal receipt')
        marker=ClockMarker(**endpoint)
        require(current_time<marker,'Original/renewed form endpoint is no longer valid')
        return marker

    def permanent_link(self,link_id):
        """Historical stabilization survives dispel; no restore is performed."""
        self.validate();link=self.world.links[link_id]
        require(self.world.casts[link.cast_id].spell_id=='true-polymorph','Only True stabilizes')
        rows=self.records('link-stabilized',link_id)
        require(len(rows)<=1,'Original world checkpoint cannot resolve twice')
        return bool(rows)
