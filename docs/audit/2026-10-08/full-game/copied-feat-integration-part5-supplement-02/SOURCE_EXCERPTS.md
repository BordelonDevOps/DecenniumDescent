# Exact source excerpts

Each excerpt is linked to the complete unchanged or proposed file and its full-byte binding in SOURCE_REFERENCES.json.

## SRC-HEALING-LIVENESS

`sources/DescentReviewChanges/ReviewBible/tools/healing_playtest_rules.py`, lines 33–98; SHA256 `651cf7191b8619377b236a33470d5461fc92288f173308a5daae96331a8f7320`.

Existing pure arithmetic helper, caller-owned source consumption, live reducer filtering and candidate reporting.

```text
            if self.kind=='blight-totem' and self.value!=Fraction(1,2):
                raise SpellRuleError('Supplied Blight Totem profile is exactly one-half')
        else:integer(self.value,'healing reduction',0)


def healing_packet(state, base, *, dice_count=0, pre_flat_bonuses=(),
                   conditional_flat_bonuses=(), conditional_dice_total=0,
                   conditional_dice_count=0, per_die_bonus=0, per_die_bonus_cap=None,
                   systemic_factors=(), reductions=(), hp_gain_prohibited=False,
                   reserve=None):
    """Pure two-pass arithmetic for ALREADY ELIGIBLE modifiers/reducers.

    Base includes the printed formula and legal pre-resolution rolled dice.
    Flat class bonuses use strongest across pre/conditional sets. Callers own
    source limits, dice rolls, costs, next-heal consumption, copy/trigger rights,
    legal converters and per-round budgets. Excess is quantity, not permission.
    """
    for name,value in [('base',base),('dice count',dice_count),('conditional dice',conditional_dice_total),
                       ('conditional dice count',conditional_dice_count),('per-die bonus',per_die_bonus)]:
        integer(value,name,0)
    for value in tuple(pre_flat_bonuses)+tuple(conditional_flat_bonuses):integer(value,'flat bonus',0)
    if per_die_bonus_cap is not None:integer(per_die_bonus_cap,'per-die bonus cap',0)
    if reserve is not None:integer(reserve,'remaining recovery reserve',0)
    system=Fraction(1)
    for factor in systemic_factors:
        if not isinstance(factor,Fraction) or not 0<=factor<=1:
            raise SpellRuleError('Systemic factors require exact reduction fractions')
        system*=factor
    if len({r.application_id for r in reductions})!=len(reductions):
        raise SpellRuleError('One application may enter healing once')
    live=[r for r in reductions if r.present and not r.suppressed]
    groups={}
    for r in live:
        if r.group in groups and groups[r.group].kind!=r.kind:
            raise SpellRuleError('A reduction group cannot mix unreviewed profiles')
        previous=groups.get(r.group)
        if previous is None or (r.value<previous.value if r.kind in ('factor','blight-totem') else r.value>previous.value):
            groups[r.group]=r
    ordinary=[r for r in groups.values() if r.kind!='blight-totem']
    totem=any(r.kind=='blight-totem' for r in groups.values())
    def calculate(use_conditional):
        count=dice_count+(conditional_dice_count if use_conditional else 0)
        flat=max(tuple(pre_flat_bonuses)+(tuple(conditional_flat_bonuses) if use_conditional else ()),default=0)
        die_bonus=count*per_die_bonus
        if per_die_bonus_cap is not None:die_bonus=min(die_bonus,per_die_bonus_cap)
        potential=base+flat+die_bonus+(conditional_dice_total if use_conditional else 0)
        per_die=max((r.value for r in ordinary if r.kind=='per-die'),default=0)
        factor=system
        for r in ordinary:
            if r.kind=='factor':factor*=r.value
        adjusted=max(0,potential-count*per_die)
        ordinary_amount=max(0,(adjusted*factor).__floor__()-sum(r.value for r in ordinary if r.kind=='flat'))
        plans=[('compatible-local',ordinary_amount)]
        if totem:plans.append(('blight-totem-alone',(potential*system*Fraction(1,2)).__floor__()))
        branch,reduced=min(plans,key=lambda item:item[1])
        legal=0 if hp_gain_prohibited else reduced
        healed,report=ordinary_healing(state,legal,reserve=reserve)
        return {'state':healed,'positivePotential':potential,'postReductionAmount':reduced,
                'legalAmount':legal,'ordinaryMissingHp':state.maximum_hp-state.hp,
                'genuineExcess':max(0,legal-(state.maximum_hp-state.hp)),
                'reductionBranch':branch,'diceCount':count,**report}
    preview=calculate(False)
    eligible=preview['actualHpGained']>0
    final=calculate(True) if eligible else preview
    return {**final,'conditionalAddonsQualify':eligible,
            'previewActualHpGained':preview['actualHpGained'],
```

## SRC-HEALING-RULE

`sources/DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md`, lines 70–80; SHA256 `8d68794687b97da70aaff9953f9724e31e9fa3c8568fd4c2f9e8fd05d34c93f7`.

Preserved healing rule: suppressed reducers do not participate; present operative applicable next-positive-healing source consumption remains source-owned.

```text
Pre-resolution modifiers include Words of Equilibrium's formula M, Zealot's Fervor +S, Throne's Grace +1/die capped S+M, Benevolent Spirits' eligible paid-technique +M, Life Prophecy maximizing dice, and Crane's applicable +S. Conditional add-ons include Ground, Radiance, Aura of Faith, Ember Mantle, Life Linked's rolled1d4, Ranger Healing Touch, Aura of Mercy, Garden's stored+1 and Tranquil Lotus Step.

First compute without conditional add-ons. Only if this preview actually restores at least1HP, recompute that same event once with its eligible add-ons. The preview changes no pools/uses. Base5 minus5 plus a conditional3 remains0; eligible pre-resolution Benevolent3 yields3. Multiple flat class bonuses use the strongest across both passes unless an explicit source exception allows stacking. Rolled extra dice/per-die changes are separate.

Within each permitted reduction plan: formula/bonuses; per-die adjustments; compatible exact fractional multipliers with one floor after multiplication; compatible flat reductions; floor at0; broad HP prohibition; maximum/Critical/reserve caps. Intrinsic Wound Eater and systemic Corrupted remain independent factors. Duplicate same-stat per-die penalties use the strongest. Dice remain dice when maximized/shared; flat Lay on Hands and stored numeric Echoes have zero healing dice.

Blight Totem cannot compound other local healing reducers. Compare systemic factors plus Totem-half alone against systemic factors plus all otherwise compatible local reducers; use the lower result. Compatible halves multiply, compatible distinct flat penalties add, duplicate same-profile groups use strongest. Suppressed reducers do not participate.

Every present, operative, applicable next-positive-healing reduction consumes exactly once when the final event commits if its pre-reduction HP potential was positive. This includes reducers whose arithmetic branch lost to Totem or whose actual gain was later blocked. Zero potential and suppressed records consume none. Two-pass preview never consumes twice.

Critical at3Wounds caps ordinary healing at max(1, effective maximum minus1); it is not a maximumHP reduction and healing cannot lower currentHP. Reserve spends only actualHP restored. A final heal8 with room3 spends3 reserve; blocked healing spends0, other activation costs remain paid. Revival/form changes/encounter starts do not replenish reserve.
```

## SRC-BUFFER-HANDOFF

`sources/DescentReviewChanges/ReviewBible/tools/form_temphp_playtest_rules.py`, lines 24–123; SHA256 `97566962d3eddeca5966b4b58bbb3a5e53dc34d529afb5de033d4358397e2151`.

Existing BufferGrant validation and BufferLedger source-owned natural-expiry instruction contract. No automatic cleanse or Oracle acquisition.

```text
class BufferGrant:
    grant_id: str
    source_id: str
    owner: str
    target: str
    remaining: int
    expiry: ClockMarker | None = None
    # None means an explicitly fixed/source-dependent lifetime, not default LR.
    rest_epoch: int | None = None
    dependencies: tuple = ()
    riders: set = field(default_factory=set)
    state: str = 'pending'

    def __post_init__(self):
        for v in (self.grant_id,self.source_id,self.owner,self.target): identity(v)
        integer(self.remaining,'offered temporary HP',0)
        if self.expiry is not None: require_deadline(self.expiry)
        if self.rest_epoch is not None: integer(self.rest_epoch,'recipient LR epoch',0)
        require(self.expiry is not None or self.rest_epoch is not None or self.dependencies,
                'Declare explicit expiry/dependency or default recipient LR epoch')
        for dep in self.dependencies: identity(dep)
        require(self.riders <= {'bloodshield-reaction','overflowing-cleanse'},'Unknown linked rider')
        if 'bloodshield-reaction' in self.riders:
            require(self.source_id=='crimson-agent.arch.veinweave-bloodshield','Wrong Bloodshield source')
        if 'overflowing-cleanse' in self.riders:
            require(self.source_id=='oracle.supplement.life.overflowing-light' and self.expiry is not None,
                    'Overflowing Light requires its explicit two-round endpoint')


class BufferLedger:
    """Grant identities persist after ending; no hidden shield or replay refill.

    expire() must run at actual scheduler deadlines. Side effects are returned
    as instructions; this helper never decides eligible conditions or cleanses
    automatically. A projection into Core is checked and reconciled atomically.
    """
    def __init__(self):
        self.grants={}; self.active={}; self.rest_epochs={}; self.damage_events=set()
        self.absorptions={}
        self.form_instances=set()
        self.spell_anatomies={}

    def amount(self,target):
        ident=self.active.get(target)
        return self.grants[ident].remaining if ident else 0

    def current(self,target):
        ident=self.active.get(target)
        return self.grants.get(ident)

    def validate_offer(self,grant,now):
        require(isinstance(grant,BufferGrant) and grant.state=='pending','Supply a new uncommitted grant')
        require(grant.grant_id not in self.grants,'Grant identity already processed')
        marker=clock_marker(now)
        if grant.expiry is not None: require(marker<grant.expiry,'Grant deadline already passed')
        if grant.rest_epoch is not None:
            require(grant.rest_epoch==self.rest_epochs.get(grant.target,0),'Stale recipient rest epoch')
        current=self.current(grant.target)
        if current and current.expiry is not None:
            require(marker<current.expiry,'Resolve existing scheduled expiry before offering a new grant')

    def offer(self,grant,now=0):
        """Caller pays the legal source BEFORE this nonstack comparison.

        No current reviewed source overrides equal-retains-existing. Noble's
        paired Smite components are merged BEFORE calling this method once.
        """
        self.validate_offer(grant,now)
        g=deepcopy(grant)
        if not g.remaining:
            return {'accepted':False,'amount':0,'grantId':None}
        self.grants[g.grant_id]=g
        current=self.current(g.target)
        if current and current.remaining>=g.remaining:
            g.state='rejected'; return {'accepted':False,'amount':g.remaining,'grantId':None}
        if current: self.end(g.target,'replaced')
        g.state='active'; self.active[g.target]=g.grant_id
        return {'accepted':True,'amount':g.remaining,'grantId':g.grant_id}

    def end(self,target,reason,*,now=None):
        require(reason in ('replaced','depleted','natural-expiry','long-rest','dependency-ended','body-ended'),
                'Unknown buffer ending')
        g=self.current(target)
        if g is None:return []
        if reason=='natural-expiry':
            require(now is not None and g.expiry is not None and clock_marker(now)>=g.expiry,
                    'Natural expiry requires the actual fixed deadline')
        events=[]
        if reason=='natural-expiry' and g.remaining>0 and 'overflowing-cleanse' in g.riders:
            events.append({'sourceId':g.source_id,'grantId':g.grant_id,'target':target,
                           'chooseUpTo':1,'eligibleConditions':('Frightened','Poisoned','Staggered')})
        g.state=reason; g.remaining=0; g.riders.clear(); del self.active[target]
        return events

    def expire(self,now):
        marker=clock_marker(now); events=[]
        for target in list(self.active):
            g=self.current(target)
            if g.expiry is not None and marker>=g.expiry: events+=self.end(target,'natural-expiry',now=marker)
        return events
```

## SRC-COPY-SCOPE

`baseline_return01/DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py`, lines 1–8; SHA256 `35e746cfe14b88073539eac763c063c5d05d630bc582ebd0c1187c6aba80f1e3`.

Copy adapter expressly mutates the canonical shared BufferLedger; world predicates do not authorize discarding returned instructions.

```text
"""SUP-07 recipient effects over actual paid CopyReleases.

Conditional world integration, not a complete game runtime. The caller owns
perception, body-space/range/LoE queries, explicit current target defenses,
turn markers, action frames and RNG visibility/interrupt scheduling. This
adapter executes bounded payload arithmetic, canonical LifeState/BufferLedger
mutations, source-owned slow/boon records, deadlines and concentration cleanup.
Ready and other unresolved provider/allowance integrations are excluded.
```

## SRC-OLD-ADVANCE

`baseline_return01/DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py`, lines 91–106; SHA256 `35e746cfe14b88073539eac763c063c5d05d630bc582ebd0c1187c6aba80f1e3`.

Return01 advance body discards BufferLedger.expire output.

```text
    def advance(self, now, releases):
        marker=clock_marker(now);require(marker>=self.now,'World time cannot move backward')
        # Bound all live copy sources to the same shared ledgers.
        by_owner={r.owner:r for r in releases}
        require(len(by_owner)==len(releases),'One copy engine per owner required')
        for e in self.effects.values():
            if e['active']:require(e['owner'] in by_owner and by_owner[e['owner']].world is self,'All live source engines required for expiry')
        for engine in releases:
            validate = getattr(engine.lifecycle.ledger, 'validate_current', None)
            if validate: validate()
        self.now=marker
        for effect in list(self.effects.values()):
            if effect['active'] and marker>=effect['deadline']:
                engine=by_owner[effect['owner']]
                engine.lifecycle.end_at_deadline(effect['cast'],actual_source_deadline=True)
        self.buffers.expire(marker);self.projection()
```

## SRC-OLD-MEND-DECLARE

`baseline_return01/DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py`, lines 173–186; SHA256 `35e746cfe14b88073539eac763c063c5d05d630bc582ebd0c1187c6aba80f1e3`.

Return01 declaration guard blocks inactive next-healing records before payment.

```text
        self._selection(component,selection,preflight=True)
        owner=self.world.actors[self.owner]
        for frame_key,world_key in [('conscious','conscious'),('canAct','canAct'),('magicAllowed','magicAllowed'),('verbal','verbalAvailable'),('somatic','somaticAvailable')]:
            require(frame[frame_key] is owner[world_key],'Action frame must use canonical caster body state')
        for target in selection.get('targets',[]):
            actor=self.world.actors[target]
            # Named replacement/redirect/next-heal integrations need their own
            # real interruption and source-use engines, not Boolean free grants.
            require(actor['unsupportedInterceptors']==[],'Unintegrated active interceptors require their actual adapters')
            if component['profile']=='mend':
                require(not any(r.next_healing for r in actor['healingReductions']),'Next-healing consumption needs its source-owned adapter')
        receipt=super().commit(event,capture_event,permission=permission,grant_id=grant_id,frame=frame)
        self.selections[event]={'declared':deepcopy(selection),'current':deepcopy(selection),'declaredAt':self.world.now}
        return receipt
```

## SRC-OLD-MEND-PAYLOAD

`baseline_return01/DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py`, lines 249–256; SHA256 `35e746cfe14b88073539eac763c063c5d05d630bc582ebd0c1187c6aba80f1e3`.

Return01 paid-payload guard blocks inactive next-healing records.

```text
    def _payload(self,event,cast,selection,eligible,rolls):
        component=cast['component'];profile=component['profile'];owner=self.owner;world=self.world
        effect_id=owner+'::feat-copy::'+event;updates={};results={};effect=None;speed=None;offer=None
        preview=deepcopy(world.buffers);native=None
        for target in eligible:
            require(world.actors[target]['unsupportedInterceptors']==[],'Resolve newly active actual interceptors through their source adapters first')
        if profile=='mend':
            require(not any(r.next_healing for r in world.actors[eligible[0]]['healingReductions']),'New next-healing source needs its actual consumption adapter')
```

## SRC-NEW-ADVANCE

`successor/DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py`, lines 91–114; SHA256 `2b45d33ff0bdc6230aa4fbfd563f59bc0e2537616210ade940d2dd22954ccc1d`.

Narrow positive instruction handoff and explicit downstream boundary.

```text
    def advance(self, now, releases):
        """Advance supplied clocks and return source-owned expiry instructions.

        The caller must route every returned instruction to the actual source/
        target condition-choice adapter. This is an internal event handoff, not
        Oracle acquisition, automatic cleansing, or durable delivery/acknowledgment.
        An ignored instruction cannot be recovered by expiring the grant again.
        """
        marker=clock_marker(now);require(marker>=self.now,'World time cannot move backward')
        # Bound all live copy sources to the same shared ledgers.
        by_owner={r.owner:r for r in releases}
        require(len(by_owner)==len(releases),'One copy engine per owner required')
        for e in self.effects.values():
            if e['active']:require(e['owner'] in by_owner and by_owner[e['owner']].world is self,'All live source engines required for expiry')
        for engine in releases:
            validate = getattr(engine.lifecycle.ledger, 'validate_current', None)
            if validate: validate()
        self.now=marker
        for effect in list(self.effects.values()):
            if effect['active'] and marker>=effect['deadline']:
                engine=by_owner[effect['owner']]
                engine.lifecycle.end_at_deadline(effect['cast'],actual_source_deadline=True)
        instructions=self.buffers.expire(marker);self.projection()
        return instructions
```

## SRC-NEW-MEND-191

`successor/DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py`, lines 191–191; SHA256 `2b45d33ff0bdc6230aa4fbfd563f59bc0e2537616210ade940d2dd22954ccc1d`.

Exact live-only unsupported-next-healing guard, consistent with the existing arithmetic helper.

```text
                require(not any(r.present and not r.suppressed and r.next_healing for r in actor['healingReductions']),'Next-healing consumption needs its source-owned adapter')
```

## SRC-NEW-MEND-264

`successor/DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py`, lines 264–264; SHA256 `2b45d33ff0bdc6230aa4fbfd563f59bc0e2537616210ade940d2dd22954ccc1d`.

Exact live-only unsupported-next-healing guard, consistent with the existing arithmetic helper.

```text
            require(not any(r.present and not r.suppressed and r.next_healing for r in world.actors[eligible[0]]['healingReductions']),'New next-healing source needs its actual consumption adapter')
```
