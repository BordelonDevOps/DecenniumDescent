# Actual parent-operation history: implementation review

Following our ten parent policies and Action-budget/cadence clarification, this is the first necessary implementation layer: history over actual canonical Druid/TransformationWorld operations. It does not restore parent state and is not yet an admitted TemporalKernel integration. All seven larger domains remain open; do not treat these tests as full Time Loop validation.

It observes the existing real objects before their first form/cast, uses the host's exact wallet registry, pins actual form/cast/link/body/concentration identities, and emits creation/renewal/stabilization/ending receipts from completed native calls. It cannot import current expiry/permanent flags as history. Queries neither reactivate forms nor restore resources. Outside cast origins are explicit, and initiative operations require the actual scheduler atomic event ID/time. Real Druid regular starts use the global marker; the journal does not tick during history queries.

38 methods pass. Current ordinary form and transformation helpers, the 50+76+22 reviewed temporal files, and frozen class rules are unchanged. This does not inherit any approval for the new module.

Please review the exact code below for whether the receipts genuinely prove the source operations claimed, whether canonical references/history can be accidentally replaced, and whether failed calls can be mistaken for successful payments. The native helpers still own ordinary target/save/geometry legality. The journal records and refuses temporal admission after a native call that fails after changing parent state or an observed wallet/Druid economy; it cannot roll back committed casts or reroll failed host save resolvers. Two tests explicitly preserve those exceptional cases, including an existing special() clock advance before an unavailable Action rejects. No failed operation receives a success receipt.

Remaining implementation: proposed parent/concentration restoration, reference-safe atomic field staging, geometry/meld/current-inventory reconciliation, persistent slots, external effects, full creature/device/other parent closures, iteration-qualified ordinary wrappers, and composition with the already-reviewed control world. The ordinary wrappers here deliberately retain their non-temporal numeric turn arguments; they are observed history, not claimed replay-safe operational Time Loop APIs. Commands not handled through this layer and unobserved lifecycle changes reject its evidence validation. Final game-wide flow/GitHub gate remains open.


## Exact tools/temporal_parent_history.py
SHA-256 `c16c2b4bea42a5bb8f012a3616739f57821de953a323fff7dcd2da952685d2dd`

```
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
from dataclasses import fields
from fractions import Fraction
from hashlib import sha256
import json

from control_playtest_rules import ClockMarker, clock_marker
from form_temphp_playtest_rules import DruidState, FormInstance, OwnerRechargeClock
from transformation_spell_playtest_rules import (
    TransformationWorld, ConcentrationLedger, Body, PhysicalOrigin, Cast, Link,
    CastStats, CastPrice, Selection,
)
from temporal_playtest_rules import ident, require, Wallet


SCHEMAS = {
    TransformationWorld: frozenset('buffers concentration bodies casts links slots druids damage_rounds damage_events regular_ends commands events'.split()),
    ConcentrationLedger: frozenset(('current',)),
    DruidState: frozenset('owner circle buffers cadence creatures current instances long_epoch short_epoch regular_index recharges recharge_clock rest_uses attuned shifts buffer_capacity reserve surges surge_capacity'.split()),
    OwnerRechargeClock: frozenset('mode now next_tick ticks last_regular anchored'.split()),
}
VALUE_TYPES = (ClockMarker, FormInstance, PhysicalOrigin, Cast, Link, CastStats, Selection)


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
    def __init__(self, world, *, wallets, scheduler=None):
        exact(world, TransformationWorld);exact(world.concentration, ConcentrationLedger)
        require(not world.casts and not world.links and not world.concentration.current,
                'Observe before source creation; current state is not historical proof')
        require(all(d.current is None and not d.instances for d in world.druids.values()),
                'Observe Druid before first form; historical import requires a separate adapter')
        require(type(wallets) is dict and all(k in world.bodies for k in wallets),
                'Supply the actual host actor wallet registry')
        require(len({id(w) for w in wallets.values()})==len(wallets),'Distinct owners cannot alias wallets')
        for wallet in wallets.values():exact(wallet,Wallet)
        self.world=world;self.wallets=wallets;self.scheduler=scheduler;self.mode='outside'
        self.events=();self.receipts=();self.failures=();self.used=set()
        self.last_time=ClockMarker(0);self.chain='parent-history-v1'
        self._events=();self._receipts=();self._failures=();self._chain=self.chain
        self._mode=self.mode;self._last_time=self.last_time;self._scheduler_binding=None
        self._pins={};self._slot_pins={};self._initial=self._state()
        self._expected=leaf(self._initial)
        self._bind_world()
        self._pin_objects()

    def _bind_world(self):
        w=self.world
        self._world_binding=(w,w.buffers,w.concentration,w.bodies,w.druids,w.casts,w.links,self.wallets)
        self._wallet_bindings=dict(self.wallets)
        self._druid_bindings={a:(d,d.buffers,d.cadence,d.creatures,d.recharge_clock,d.instances)
                              for a,d in w.druids.items()}

    def _pin_objects(self):
        w=self.world
        for domain,registry in (('body',w.bodies),('cast',w.casts),('link',w.links)):
            for key,obj in registry.items():
                k=(domain,key)
                require(k not in self._pins or self._pins[k] is obj,'Canonical parent identity replaced')
                self._pins[k]=obj
        for owner,d in w.druids.items():
            for key,obj in d.instances.items():
                k=('form',owner,key)
                require(k not in self._pins or self._pins[k] is obj,'Canonical form identity replaced')
                self._pins[k]=obj
        for owner,slot in w.concentration.current.items():
            require(type(slot) is tuple and len(slot)==2 and type(slot[0]) is str and callable(slot[1]),
                    'Malformed actual concentration slot')
            self._slot_pins[id(slot)]=slot

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
            'druids':{a:{n:leaf(getattr(d,n)) for n in ('long_epoch','short_epoch','regular_index',
                       'recharges','rest_uses','attuned','shifts','buffer_capacity','reserve',
                       'surges','surge_capacity','cadence')}
                       | {'rechargeClock':leaf(vars(d.recharge_clock))}
                       for a,d in self.world.druids.items()}}

    def validate(self):
        w=self.world
        require(all(a is b for a,b in zip(self._world_binding,
                    (w,w.buffers,w.concentration,w.bodies,w.druids,w.casts,w.links,self.wallets))),
                'Canonical parent world alias changed')
        require(set(self.wallets)==set(self._wallet_bindings) and
                all(self.wallets[k] is v for k,v in self._wallet_bindings.items()),
                'Canonical parent wallet registry changed')
        for wallet in self.wallets.values():exact(wallet,Wallet)
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
        current=self._state()
        require(current==self._expected,'Unobserved parent lifecycle mutation; no historical receipt')
        for key,obj in self._pins.items():
            if key[0]=='form':current_obj=w.druids[key[1]].instances.get(key[2])
            else:current_obj={'body':w.bodies,'cast':w.casts,'link':w.links}[key[0]].get(key[1])
            require(current_obj is obj,'Canonical parent object was replaced or removed')
        for slot in w.concentration.current.values():
            require(self._slot_pins.get(id(slot)) is slot,'Unrecorded concentration slot identity')
        return current

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
            origin={'kind':'OUTSIDE_CAST','timestamp':leaf(marker)}
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
                        require(frame['operation']=='druid-renew','Only actual renewal may extend a form')
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
                    receipts.append({'kind':'cast-created','castId':cid,'initial':c,
                                     'origin':event['origin'],'concentrationBinding':slot})
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
        for row in receipts:row.update({'eventId':event['eventId'],'time':event['time']})
        self.used.add(event['eventId']);self.events=self.events+(leaf(event),)
        self.receipts=self.receipts+tuple(leaf(r) for r in receipts)
        if failed and (frame['before']!=after or before_economy!=event['economyAfter']):
            self.failures=self.failures+(event['eventId'],)
        self.chain=digest((self.chain,event,receipts))
        # Detached copies detect accidental mutation of public audit projections.
        self._events=leaf(self.events);self._receipts=leaf(self.receipts)
        self._failures=leaf(self.failures);self._chain=self.chain
        self._expected=leaf(after);self.last_time=frame['marker'];self._last_time=self.last_time;self._pin_objects()

    def _wallet(self,owner,wallet):
        require(owner in self.wallets and self.wallets[owner] is wallet,
                'Use the actual canonical owner wallet; duplicate payment balances are unsupported')
        return wallet

    def _run(self,event_id,now,operation,actor,call,*,wallets=()):
        frame=self._begin(event_id,now,operation,actor);economy=self._economy(wallets)
        try:result=call()
        except Exception:
            self._finish(frame,economy,wallets,failed=True)
            raise
        self._finish(frame,economy,wallets)
        return result

    def shift(self,event_id,stats,source_id,instance_id,now,wallet,**options):
        self._wallet(stats.owner,wallet)
        d=self.world.druids[stats.owner]
        return self._run(event_id,now,'druid-shift',stats.owner,
            lambda:d.shift(stats,source_id,instance_id,now,wallet,**options),wallets=(wallet,))

    def renew(self,event_id,stats,now,*,renew=True):
        d=self.world.druids[stats.owner]
        return self._run(event_id,now,'druid-renew',stats.owner,
            lambda:d.natural_endpoint(stats,now,renew=renew))

    def revert(self,event_id,owner,now,wallet,*,legal):
        self._wallet(owner,wallet)
        return self._run(event_id,now,'druid-revert',owner,
            lambda:self.world.druids[owner].revert(now,wallet,legal=legal),wallets=(wallet,))

    def special(self,event_id,stats,now,wallet,special_id,*,legal):
        self._wallet(stats.owner,wallet)
        return self._run(event_id,now,'druid-special',stats.owner,
            lambda:self.world.druids[stats.owner].special(stats,now,wallet,special_id,legal=legal),wallets=(wallet,))

    def mooncursed_howl(self,event_id,stats,now,wallet,recipients,shared_roll,grant_ids,*,legal):
        self._wallet(stats.owner,wallet)
        return self._run(event_id,now,'druid-mooncursed-howl',stats.owner,
            lambda:self.world.druids[stats.owner].mooncursed_howl(stats,now,wallet,recipients,shared_roll,grant_ids,legal=legal),
            wallets=(wallet,))

    def druid_attack(self,event_id,stats,now,wallet,*,legal):
        self._wallet(stats.owner,wallet)
        return self._run(event_id,now,'druid-attack',stats.owner,
            lambda:self.world.druids[stats.owner].attack(stats,now,wallet,legal=legal),wallets=(wallet,))

    def spell_form_attack(self,event_id,target,stats,now,wallet,*,legal):
        self._wallet(target,wallet)
        return self._run(event_id,now,'spell-form-attack',target,
            lambda:self.world.attack(target,stats,now,wallet,legal=legal),wallets=(wallet,))

    def cast(self,event_id,cast_id,spell_id,stats,price,wallet,selections,now,regular_index,**options):
        self._wallet(stats.owner,wallet)
        require(type(price) is CastPrice,'Actual canonical CastPrice required')
        return self._run(event_id,now,'spell-cast',stats.owner,
            lambda:self.world.cast(cast_id,spell_id,stats,price,wallet,selections,now,regular_index,**options),wallets=(wallet,))

    def checkpoint(self,event_id,now,*,started_packets_and_due_saves_finished):
        return self._run(event_id,now,'spell-checkpoint','world',
            lambda:self.world.checkpoint(now,started_packets_and_due_saves_finished=started_packets_and_due_saves_finished))

    def end_concentration(self,event_id,owner,now,*,reason):
        require(reason in ('failed-save','incapacitated','voluntary-release'),
                'Use the exact supported ordinary concentration ending')
        return self._run(event_id,now,'concentration-'+reason,owner,
            lambda:self.world.concentration.end(owner,reason))

    def dispel(self,event_id,actor,target,now,*,legal):
        return self._run(event_id,now,'spell-dispel',actor,lambda:self.world.dispel(target,legal=legal))

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
        require(kind in ('short','long'),'Actual short or long rest required')
        d=self.world.druids[stats.owner]
        call=(lambda:d.completed_long_rest(stats,epoch,attuned=attuned,actual_completed=actual_completed,now=now)) if kind=='long' else (
            lambda:d.completed_short_rest(epoch,actual_completed=actual_completed,now=now))
        return self._run(event_id,now,'druid-rest-'+kind,stats.owner,call)

    def records(self,kind,identity):
        self.validate()
        return tuple(leaf(r) for r in self.receipts if r['kind']==kind and
                     identity in (r.get('formId'),r.get('castId'),r.get('linkId')))

    def valid_form_deadline(self,owner,form_id,now):
        """Evidence for later planning, not permission to reactivate anatomy."""
        self.validate();d=self.world.druids[owner];f=d.instances[form_id]
        created=self.records('form-created',form_id)
        require(len(created)==1 and created[0]['owner']==owner,'Missing unique actual form creation')
        endpoint=created[0]['initial']['expiry']
        for row in self.records('form-renewed',form_id):
            require(row['owner']==owner and row['oldExpiry']==endpoint,'Broken same-instance renewal chain')
            endpoint=row['newExpiry']
        require(endpoint==leaf(f.expiry),'Current form endpoint lacks an actual renewal receipt')
        marker=ClockMarker(**endpoint)
        require(clock_marker(now)<marker,'Original/renewed form endpoint is no longer valid')
        return marker

    def permanent_link(self,link_id):
        """Historical stabilization survives dispel; no restore is performed."""
        self.validate();link=self.world.links[link_id]
        require(self.world.casts[link.cast_id].spell_id=='true-polymorph','Only True stabilizes')
        rows=self.records('link-stabilized',link_id)
        require(len(rows)<=1,'Original world checkpoint cannot resolve twice')
        return bool(rows)

```

## Exact tools/validate_temporal_parent_history.py
SHA-256 `04eca3dd1f71003eb7718656e6bb191a8359e4aa4d23f62550d0a8c585dd2953`

```
"""Actual-operation journal checks; not Time Loop parent restoration tests."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest

from temporal_parent_history import TemporalParentHistory, leaf
from validate_transformation_spell_playtests import world,stats,price,select
from form_temphp_playtest_rules import DruidState,DruidStats
from transformation_spell_playtest_rules import Body,PhysicalOrigin
from temporal_playtest_rules import Scheduler,Wallet,ClockMarker,SpellRuleError


def fixture(level=14):
    w=world();ds=DruidStats('a',level,6,4,4,4)
    d=DruidState(ds,'Moon',w.buffers,{'refrain':2,'rememberedSpell':'x','dissonance':8})
    w.druids['a']=d
    return w,ds,d,TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies})


def shift(j,ds,*,fid='F',source='druid.base.bear-form-tank',now=0,event='shift'):
    wallet=j.wallets[ds.owner];wallet.bonus_action=True
    return j.shift(event,ds,source,fid,now,wallet,legal=True)


def cast(j,*,spell='polymorph',cid='C',event='cast',now=0,target='b',owner='a',save=False,countered=False):
    return j.cast(event,cid,spell,stats(owner),price(spell),j.wallets[owner],[select(target)],now,0,
                  legal=True,resolve_save=lambda t,dc:save,countered=countered)


class ParentHistoryTests(unittest.TestCase):
    def test_paid_renewal_keeps_same_form_and_actual_payment(self):
        w,ds,d,j=fixture();shift(j,ds);f=d.current;before=d.shifts
        j.renew('renew',ds,600)
        self.assertIs(d.current,f);self.assertEqual(d.shifts,before-1)
        r=j.records('form-renewed','F')[0]
        self.assertEqual((r['oldExpiry']['seconds'],r['newExpiry']['seconds']),(600,1200))
        self.assertEqual((r['shiftBefore'],r['shiftAfter']),(before,before-1))
        self.assertEqual(j.valid_form_deadline('a','F',601),ClockMarker(1200))

    def test_level20_zero_shift_renewal_still_requires_real_endpoint_event(self):
        w,ds,d,j=fixture(20);shift(j,ds);before=d.shifts
        with self.assertRaises(SpellRuleError):j.renew('early',ds,599)
        self.assertFalse(j.records('form-renewed','F'))
        j.renew('on-time',ds,600)
        self.assertEqual(d.shifts,before);self.assertEqual(len(j.records('form-renewed','F')),1)

    def test_renewal_chain_survives_later_real_reversion_without_reactivation(self):
        w,ds,d,j=fixture();shift(j,ds);j.renew('r1',ds,600);j.renew('r2',ds,1200)
        j.wallets['a'].bonus_action=True;j.revert('revert','a',1201,j.wallets['a'],legal=True)
        before=deepcopy((d.reserve,d.surges,d.shifts,d.instances['F'].state))
        self.assertEqual(j.valid_form_deadline('a','F',1202),ClockMarker(1800))
        self.assertIsNone(d.current);self.assertEqual((d.reserve,d.surges,d.shifts,d.instances['F'].state),before)
        with self.assertRaises(SpellRuleError):j.valid_form_deadline('a','F',1800)

    def test_new_instance_does_not_borrow_old_renewal(self):
        w,ds,d,j=fixture();shift(j,ds);j.renew('renew',ds,600)
        shift(j,ds,fid='G',source='druid.base.wolf-form-striker',now=601,event='wolf')
        self.assertFalse(j.records('form-renewed','G'))
        self.assertEqual(j.valid_form_deadline('a','G',602),ClockMarker(1201))
        self.assertEqual(d.instances['F'].state,'changed')

    def test_unobserved_native_renewal_is_not_accepted_as_evidence(self):
        w,ds,d,j=fixture();shift(j,ds);d.natural_endpoint(ds,600,renew=True)
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.valid_form_deadline('a','F',601)

    def test_direct_expiry_edit_cannot_fabricate_paid_extension(self):
        w,ds,d,j=fixture();shift(j,ds);d.current.expiry=ClockMarker(900)
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.validate()

    def test_public_receipt_edit_is_detected(self):
        w,ds,d,j=fixture();shift(j,ds);j.renew('renew',ds,600)
        j.receipts[-1]['newExpiry']['seconds']=1800
        with self.assertRaisesRegex(SpellRuleError,'historical'):j.validate()

    def test_returned_receipt_copy_cannot_mutate_journal(self):
        w,ds,d,j=fixture();shift(j,ds);r=j.records('form-created','F')[0]
        r['initial']['expiry']['seconds']=9999
        self.assertEqual(j.valid_form_deadline('a','F',1),ClockMarker(600))

    def test_event_deletion_and_duplicate_id_reject(self):
        w,ds,d,j=fixture();shift(j,ds)
        with self.assertRaisesRegex(SpellRuleError,'Repeated'):j.renew('shift',ds,600)
        j.events=()
        with self.assertRaisesRegex(SpellRuleError,'historical'):j.validate()

    def test_form_identity_replacement_rejects_even_equal_fields(self):
        w,ds,d,j=fixture();shift(j,ds);f=deepcopy(d.current)
        d.instances['F']=f;d.current=f
        with self.assertRaisesRegex(SpellRuleError,'object was replaced'):j.validate()

    def test_shared_world_and_cadence_aliases_must_remain_canonical(self):
        w,ds,d,j=fixture();d.cadence=dict(d.cadence)
        with self.assertRaisesRegex(SpellRuleError,'alias'):j.validate()

    def test_actual_casting_cadence_changes_remain_current(self):
        w,ds,d,j=fixture();shift(j,ds)
        d.cadence.update(refrain=3,rememberedSpell='later-spell',dissonance=19)
        j.validate();j.valid_form_deadline('a','F',1)
        self.assertEqual(d.cadence,{'refrain':3,'rememberedSpell':'later-spell','dissonance':19})

    def test_observation_cannot_start_from_existing_cast_or_form(self):
        w,ds,d,j=fixture();shift(j,ds)
        with self.assertRaisesRegex(SpellRuleError,'before first form'):TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies})
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j)
        with self.assertRaisesRegex(SpellRuleError,'before source creation'):TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies})

    def test_original_concentration_callback_retained_after_real_end(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j);slot=w.concentration.current['a']
        j.end_concentration('failure','a',1,reason='failed-save')
        self.assertEqual(w.links['C:b'].state,'failed-save')
        self.assertIs(j._slot_pins[id(slot)],slot)
        self.assertEqual(j.records('cast-created','C')[0]['concentrationBinding'][1:],(id(slot),id(slot[1])))
        self.assertNotIn('a',w.concentration.current)

    def test_same_id_replaced_callback_detected(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j)
        w.concentration.current['a']=('C',lambda reason:None)
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.validate()

    def test_true_stabilization_proof_survives_dispel(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j,spell='true-polymorph')
        self.assertFalse(j.permanent_link('C:b'))
        j.checkpoint('checkpoint',60,started_packets_and_due_saves_finished=True)
        self.assertTrue(j.permanent_link('C:b'));self.assertNotIn('a',w.concentration.current)
        j.dispel('dispel','c','b',61,legal=True)
        before=deepcopy((w.links['C:b'].state,w.bodies['b'].anatomy,w.bodies['b'].equipment))
        self.assertTrue(j.permanent_link('C:b'))
        self.assertEqual((w.links['C:b'].state,w.bodies['b'].anatomy,w.bodies['b'].equipment),before)

    def test_fabricated_permanent_flag_is_not_stabilization(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j,spell='true-polymorph')
        w.links['C:b'].state='permanent'
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.permanent_link('C:b')

    def test_checkpoint_cannot_resolve_same_link_twice(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j,spell='true-polymorph')
        j.checkpoint('checkpoint',60,started_packets_and_due_saves_finished=True)
        j.checkpoint('later',61,started_packets_and_due_saves_finished=True)
        self.assertEqual(len(j.records('link-stabilized','C:b')),1)

    def test_expiring_polymorph_is_not_permanent(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j)
        j.checkpoint('checkpoint',60,started_packets_and_due_saves_finished=True)
        self.assertEqual(w.links['C:b'].state,'expired')
        self.assertEqual(j.records('link-ended','C:b')[0]['newState'],'expired')
        with self.assertRaises(SpellRuleError):j.permanent_link('C:b')

    def test_countered_cast_records_real_cost_but_no_link(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});result=cast(j,countered=True)
        self.assertTrue(result['countered']);self.assertEqual(w.links,{})
        self.assertIsNone(j.records('cast-created','C')[0]['concentrationBinding'])
        e=j.events[0]
        self.assertLess(e['economyAfter']['wallets'][0]['rp'],e['economyBefore']['wallets'][0]['rp'])

    def test_failing_save_callback_taints_partial_committed_cast(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});wallet=j.wallets['a']
        def broken(target,dc):raise RuntimeError('authoritative resolver failed')
        with self.assertRaises(RuntimeError):j.cast('broken','C','polymorph',stats(),price('polymorph'),
            wallet,[select(willing=False)],0,0,legal=True,resolve_save=broken)
        self.assertLess(wallet.rp,100);self.assertTrue(j.events[0]['failed']);self.assertEqual(j.receipts,())
        with self.assertRaisesRegex(SpellRuleError,'host reconciliation'):j.validate()

    def test_failed_unpaid_operation_produces_no_success_receipt(self):
        w,ds,d,j=fixture();before=d.shifts
        with self.assertRaises(SpellRuleError):j.shift('illegal',ds,'druid.base.bear-form-tank','F',0,j.wallets['a'],legal=False)
        self.assertEqual(d.shifts,before);self.assertEqual(j.receipts,());j.validate()

    def test_failure_after_clock_only_mutation_also_taints(self):
        w,ds,d,j=fixture(20)
        source=next(k for k in __import__('form_temphp_playtest_rules').PROFILES if k.endswith('mooncursed'))
        shift(j,ds,source=source)
        j.wallets['a'].actions=0
        with self.assertRaises(SpellRuleError):j.special('bad-payment',ds,1,j.wallets['a'],'howl',legal=True)
        self.assertEqual(d.recharge_clock.now,ClockMarker(1))
        with self.assertRaisesRegex(SpellRuleError,'host reconciliation'):j.validate()

    def test_unknown_holder_fields_reject_before_source_cost(self):
        w,ds,d,j=fixture();d.unknown_state=True;wallet=Wallet();before=deepcopy(vars(wallet))
        with self.assertRaisesRegex(SpellRuleError,'schema'):shift(j,ds)
        self.assertEqual(vars(wallet),before);self.assertFalse(d.instances)

    def test_same_hp_holder_required_but_actual_damage_may_change_hp(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j);life=w.bodies['b'].life
        life.hp=0;j.finalize_damage('damage','b',1,incapacitated=False,dead=False)
        self.assertEqual(w.links['C:b'].state,'forced-reversion');self.assertIs(w.bodies['b'].life,life)
        w.bodies['b'].life=deepcopy(life)
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.validate()

    def test_cast_ends_actual_druid_and_records_both_sources(self):
        w,ds,d,j=fixture();shift(j,ds)
        cast(j,target='a',owner='b',now=1)
        self.assertIsNone(d.current)
        self.assertEqual(j.records('form-ended','F')[0]['newState'],'spell-transformation')
        self.assertEqual(w.bodies['a'].anatomy,'C:a')

    def test_outside_origin_and_authenticated_initiative_are_distinct(self):
        w=world();s=Scheduler('enc',('a','b','c'),now=ClockMarker(10));j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies},scheduler=s)
        cast(j,now=9);self.assertEqual(j.records('cast-created','C')[0]['origin']['kind'],'OUTSIDE_CAST')
        j.enter_initiative()
        with self.assertRaisesRegex(SpellRuleError,'atomic'):j.end_concentration('fake','a',10,reason='failed-save')
        s.begin_event('real');j.end_concentration('real','a',10,reason='failed-save');s.finish_event('real')
        self.assertEqual(j.events[-1]['origin']['encounter'],'enc')

    def test_recharge_query_never_ticks_but_authentic_due_start_does(self):
        w,ds,d,j=fixture();shift(j,ds)
        d.recharge_clock.use(0);s=Scheduler('enc',('a','b','c'),now=ClockMarker(6));j.scheduler=s;j.enter_initiative()
        self.assertEqual(d.recharge_clock.ticks,0);j.valid_form_deadline('a','F',6)
        self.assertEqual(d.recharge_clock.ticks,0)
        s._regular_start('a',Wallet(),6);s.begin_event('start',phase='start')
        j.druid_regular_start('start','a');self.assertEqual(d.recharge_clock.ticks,1)
        self.assertEqual(d.regular_index,s.global_regular)

    def test_fake_recharge_marker_or_body_phase_rejects(self):
        w,ds,d,j=fixture();s=Scheduler('enc',('a','b','c'));j.scheduler=s;j.enter_initiative()
        with self.assertRaisesRegex(SpellRuleError,'Authenticated'):j.druid_regular_start('fake','a')
        s._regular_start('a',Wallet(),0);s.begin_event('body')
        with self.assertRaisesRegex(SpellRuleError,'Authenticated'):j.druid_regular_start('body','a')
        self.assertEqual(d.regular_index,0)

    def test_actual_gear_loss_is_preserved_and_not_restored_by_history_queries(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j)
        j.lose_gear('lost','b','b:coat',1,actual_loss=True)
        j.end_concentration('end','a',2,reason='voluntary-release')
        self.assertNotIn('b:coat',w.bodies['b'].equipment)
        self.assertIn('b:coat',w.bodies['b'].lost_items);j.validate()

    def test_duplicate_wallet_cannot_manufacture_cast_payment_history(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies})
        fake=Wallet(rp=100);before=deepcopy(vars(fake))
        with self.assertRaisesRegex(SpellRuleError,'canonical owner wallet'):
            j.cast('fake','C','polymorph',stats(),price('polymorph'),fake,[select()],0,0,
                   legal=True,resolve_save=lambda t,dc:False)
        self.assertEqual(vars(fake),before);self.assertEqual(j.events,());self.assertEqual(w.casts,{})

    def test_wallet_registry_replacement_detected_before_payment(self):
        w,ds,d,j=fixture();j.wallets['a']=Wallet(rp=100)
        with self.assertRaisesRegex(SpellRuleError,'wallet registry'):shift(j,ds)
        self.assertFalse(d.instances)

    def test_shared_wallet_between_two_owners_rejects_at_binding(self):
        w=world();wallet=Wallet()
        with self.assertRaisesRegex(SpellRuleError,'alias wallets'):TemporalParentHistory(w,wallets={'a':wallet,'b':wallet})

    def test_scheduler_replacement_and_history_mode_edits_reject(self):
        w,ds,d,j=fixture();s=Scheduler('enc',('a','b','c'));j.scheduler=s;j.enter_initiative()
        j.scheduler=deepcopy(s)
        with self.assertRaisesRegex(SpellRuleError,'scheduler changed'):j.validate()
        j.scheduler=s;j.mode='outside'
        with self.assertRaisesRegex(SpellRuleError,'clock/mode'):j.validate()

    def test_clock_tampering_cannot_backdate_a_receipt(self):
        w,ds,d,j=fixture();shift(j,ds,now=10);j.last_time=ClockMarker(0)
        with self.assertRaisesRegex(SpellRuleError,'clock/mode'):j.validate()

    def test_native_successful_repeat_save_records_actual_ending(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies})
        j.cast('cast','C','polymorph',stats(),price('polymorph'),j.wallets['a'],[select(willing=False)],0,0,
               legal=True,resolve_save=lambda t,dc:False)
        j.repeat_save('repeat','b',stats(),1,trigger='damage',event_or_turn='hit',round_number=1,normal_hp_damage=2,success=True)
        self.assertEqual(j.records('link-ended','C:b')[0]['newState'],'repeat-save')
        self.assertIn(('b','hit'),w.damage_events);j.validate()

    def test_unobserved_repeat_history_edit_rejects(self):
        w=world();j=TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies});cast(j)
        w.damage_rounds.add(('b',99))
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.validate()

    def test_mooncursed_grant_keeps_actual_recipient_rest_lifetime(self):
        w,ds,d,j=fixture(20);shift(j,ds,source='druid.hero.moon.mooncursed')
        before=d.surges
        j.mooncursed_howl('howl',ds,1,j.wallets['a'],['b'],8,['howl:b'],legal=True)
        grant=w.buffers.current('b');self.assertEqual(grant.dependencies,())
        self.assertEqual(grant.rest_epoch,0);self.assertEqual(d.surges,before-1)
        j.wallets['a'].bonus_action=True;j.revert('revert','a',2,j.wallets['a'],legal=True)
        self.assertIs(w.buffers.current('b'),grant);j.validate()


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ParentHistoryTests)
    count=suite.countTestCases();result=unittest.TextTestRunner(verbosity=2).run(suite)
    root=Path(__file__).resolve().parents[1]
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','testMethods':count,
        'scope':'Actual native-operation source history only; no parent restoration/geometry/commit implementation',
        'helperSha256':hashlib.sha256((root/'tools/temporal_parent_history.py').read_bytes()).hexdigest(),
        'parentRuntimeIntegrated':False,'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,
        'failures':len(result.failures),'errors':len(result.errors)}
    (root/'docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)

```

## Exact docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json
SHA-256 `d915ffdc78d4ca47bc4a02e5c8f979768963415477946d0a648a0b5406091fbb`

```
{
  "status": "PASS",
  "testMethods": 38,
  "scope": "Actual native-operation source history only; no parent restoration/geometry/commit implementation",
  "helperSha256": "c16c2b4bea42a5bb8f012a3616739f57821de953a323fff7dcd2da952685d2dd",
  "parentRuntimeIntegrated": false,
  "fullTimeLoopOperational": false,
  "remainingMajorIntegrations": 7,
  "failures": 0,
  "errors": 0
}

```

## Unchanged ordinary source hashes already supplied in the parent conference

{
  "tools/form_temphp_playtest_rules.py": "97566962d3eddeca5966b4b58bbb3a5e53dc34d529afb5de033d4358397e2151",
  "tools/transformation_spell_playtest_rules.py": "91697863f6d19043787e17f19b4c127e6c32de32ad3867393566212533081d39"
}