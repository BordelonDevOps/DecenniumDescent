"""Complete staleness watches for the current parent graph, before restoration.

This creates no snapshot or restore permission. The parent planner must first
prove source legality and then stage the complete state. It shares Transaction
with the kernel and preserves original holder identities throughout.
"""
from temporal_playtest_rules import require,Transaction
from temporal_parent_history import TemporalParentHistory


def watch_parent_graph(tx,journal):
    require(type(tx) is Transaction and type(journal) is TemporalParentHistory,
            'Actual shared transaction and reviewed parent history required')
    journal.validate()
    seen=set()

    def values(holder,label,*,bindings=(),registries=()):
        if id(holder) in seen:return
        seen.add(id(holder));tx.labels[id(holder)]=label;tx.watch_shape(holder)
        for name in vars(holder):
            if name in bindings:
                tx.watch_binding(holder,name)
                if name in registries:tx.watch_registry(getattr(holder,name))
            else:tx.watch(holder,name)

    j=journal;w=j.world
    # Reference roots and their exact registries are not deep-copied. Every
    # mutable value reached from them is watched explicitly below.
    reference_fields=('world','wallets','druid_stats','casters','scheduler',
        '_scheduler_binding','_pins','_slot_pins','_pin_manifest','_slot_manifest',
        '_world_binding','_wallet_bindings','_stat_registry','_caster_registry',
        '_stats_bindings','_caster_bindings','_druid_bindings')
    registry_fields=('wallets','druid_stats','casters','_pins','_slot_pins',
        '_pin_manifest','_slot_manifest','_wallet_bindings','_stat_registry',
        '_caster_registry','_stats_bindings','_caster_bindings','_druid_bindings')
    values(j,'parent-history',bindings=reference_fields,registries=registry_fields)
    if j.scheduler is not None:values(j.scheduler,'scheduler')
    for owner,wallet in j.wallets.items():values(wallet,'wallet:'+owner)
    for owner,stats in j.druid_stats.items():values(stats,'druid-stats:'+owner)
    for owner,authority in j.casters.items():
        values(authority,'caster-authority:'+owner,bindings=('stats',))
        tx.watch_binding(authority,'cadence')
        values(authority.stats,'caster-stats:'+owner)
    values(w,'transformation-world',bindings=('buffers','concentration','bodies','casts','links','druids'),
           registries=('bodies','casts','links','druids'))
    values(w.buffers,'buffers')
    values(w.concentration,'concentration',bindings=('current',),registries=('current',))
    for owner,b in w.bodies.items():
        values(b,'body:'+owner,bindings=('life','origin'))
        values(b.life,'life:'+owner)
        values(b.origin,'physical-origin:'+owner)
    for identity,c in w.casts.items():
        values(c,'cast:'+identity,bindings=('stats',));values(c.stats,'cast-stats:'+identity)
    for identity,link in w.links.items():values(link,'link:'+identity)
    for owner,d in w.druids.items():
        values(d,'druid:'+owner,bindings=('buffers','creatures','current','instances','recharge_clock'),
               registries=('instances',))
        tx.watch_binding(d,'cadence')
        values(d.recharge_clock,'druid-clock:'+owner)
        for identity,form in d.instances.items():values(form,'form:'+owner+':'+identity)
        # CreatureWorld is a shared graph with its own source admission and
        # child adapter. This watch layer may not hide its unhandled fields.
        require(d.creatures is None,'Parent creature dependency needs the actual creature graph adapter')
