"""Selected reviewed custom-rider interfaces, not a full effect engine."""
from dataclasses import replace
from core_playtest_rules import death_save, stable_recovery, stabilize, heal
from spell_playtest_rules import integer, SpellRuleError


def present_record(record):
    """The existing active field means unexpired/not-ended, even when suppressed.

    Suppression and acquired condition immunity disable effects, not record
    presence. Initial immunity that prevented application creates no record.
    """
    return record.get('active', False)


def active_record(record):
    return present_record(record) and not record.get('suppressed', False) and not record.get('immune', False)


def qualifies_hook(hook, record, actor):
    if not active_record(record):
        return False
    tags = set(record.get('tags', []))
    owned = record.get('ownerCharacterId') == actor
    ident = record['mechanicalId']
    if hook == 'cleric.judging-light':
        return bool(tags & {'eligibility.weakened', 'classification.curse'})
    if hook == 'thief.sneak-condition':
        return owned and ('family.bleeding' in tags or ident in ('core.poisoned', 'thief.crippled'))
    if hook == 'thief.vile-tactics':
        return 'family.bleeding' in tags or ident in ('core.poisoned', 'thief.crippled')
    if hook == 'crimson.bleed-engine':
        return owned and record.get('sourceEngine') == 'crimson-agent.bleed' and 'family.bleeding' in tags
    if hook == 'warrior.terror-engine':
        return owned and record.get('sourceClass') == 'Warrior' and ident in ('warrior.shaken', 'warrior.disoriented.active', 'core.frightened')
    if hook == 'druid.snow-leopard':
        return 'eligibility.slowed-foe' in tags
    if hook == 'paladin.vengeance':
        return owned and 'eligibility.paladin-vengeance-marked' in tags
    raise SpellRuleError('Unknown reviewed hook')


def periodic_marker_arbitration(groups, *, family):
    """Choose ONE due stack group in one family at one target timing marker.

    Caller has already applied each group's printed cap and determined its due
    records. Expected damage is doubled to keep arithmetic exact. All due groups
    consume their scheduled ticks; losing groups never bank postponed damage.
    Nonperiodic detonations, procs and later markers are outside this helper.
    """
    if family not in ('family.bleeding', 'family.ongoing-fire'):
        raise SpellRuleError('Only explicitly registered periodic families arbitrate')
    if any(group.get('family', family) != family for group in groups):
        raise SpellRuleError('Do not arbitrate different families together')
    if not groups:
        return {'damagingGroup': None, 'consumedTickGroups': []}
    ids, candidates = set(), []
    for group in groups:
        ident = group['stackGroupId']
        if ident in ids:
            raise SpellRuleError('Each stack group must be aggregated once')
        ids.add(ident)
        expected = integer(group['expectedDamageTwice'], 'twice expected group damage', 0)
        first = integer(group['firstApplicationSequence'], 'stable first-application sequence', 0)
        candidates.append((expected, -first, ident))
    # Sequence should normally be unique. ID is a deterministic final tie breaker.
    chosen = sorted(candidates, key=lambda x: (-x[0], -x[1], x[2]))[0][2]
    return {'damagingGroup': chosen, 'consumedTickGroups': [g['stackGroupId'] for g in groups]}


def bleed_marker_arbitration(groups):
    """Compatibility entry point for the reviewed Bleed interface."""
    return periodic_marker_arbitration(groups, family='family.bleeding')


def periodic_binding_for_component(*, specific_profile=None,
                                   explicit_core_condition=None,
                                   condition_immune=False):
    """One textual effect component creates at most one periodic identity.

    Call separately only when operative source text creates separate effects.
    Display-name matching or a family tag never independently creates a record.
    """
    if explicit_core_condition not in (None, 'core.bleeding', 'core.burning'):
        raise SpellRuleError('Unsupported explicit Core periodic fallback')
    if condition_immune:
        return None
    return specific_profile or explicit_core_condition


def arbitrate_periodic_applications(records, *, family, marker):
    """Resolve eligible due records for ONE target and marker, without dice.

    All active due clocks consume a tick, including suppressed records. Active
    means an existing, not-expired record here; suppressed/immune is separate.
    Caller has already enforced application/refresh caps, source costs and time.
    Damage-type defenses are intentionally not used until damage resolution.
    """
    if family not in ('family.bleeding', 'family.ongoing-fire'):
        raise SpellRuleError('Unsupported periodic family')
    due=[r for r in records if r.get('active',False)
         and family in r.get('tags',[]) and r.get('dueMarker')==marker]
    if len({r['targetId'] for r in due})>1:
        raise SpellRuleError('Arbitrate one target at a time')
    ids=[r['applicationId'] for r in due]
    if len(ids)!=len(set(ids)):
        raise SpellRuleError('Duplicate application cannot create duplicate ticks')
    groups={}
    for r in due:
        if not active_record(r):
            continue
        integer(r['expectedDamageTwice'],'twice expected damage',0)
        integer(r['applicationSequence'],'application sequence',0)
        groups.setdefault(r['stackGroupId'],[]).append(r)
    candidates=[]
    permitted={}
    for group, members in groups.items():
        policies={r['withinGroupPolicy'] for r in members}
        caps={integer(r['instanceCap'],'instance cap',1) for r in members}
        if len(policies)!=1 or len(caps)!=1:
            raise SpellRuleError('One group requires one reviewed policy and cap')
        policy=next(iter(policies))
        if policy=='strongest':
            chosen=[min(members,key=lambda r:(-r['expectedDamageTwice'],r['applicationSequence'],r['applicationId']))]
        elif policy=='sum-permitted':
            if len(members)>next(iter(caps)):
                raise SpellRuleError('Apply source instance cap before arbitration')
            chosen=members
        else:
            raise SpellRuleError('Unknown source-group damage policy')
        permitted[group]=[r['applicationId'] for r in chosen]
        candidates.append({'stackGroupId':group,'family':family,
            'expectedDamageTwice':sum(r['expectedDamageTwice'] for r in chosen),
            'firstApplicationSequence':min(r['applicationSequence'] for r in members)})
    winner=periodic_marker_arbitration(candidates,family=family)['damagingGroup']
    return {'damagingGroup':winner,'damageApplications':permitted.get(winner,[]),
            'consumedTickApplications':ids}


def recipe_occupies_slot(components):
    """Suppressed ongoing components still occupy; resolved one-time riders do not."""
    return any(c.get('active',False) and c.get('ongoing',False) for c in components)


def healing_triggered_bleed_cure(record, *, legal_effect, magical,
                                 potential, actual_hp_gained=0,
                                 remover_requires_actual_hp=False):
    """Return the applicable cure procedure, without rolling or mutating records.

    Potential is the positive rolled/calculated amount before HP caps, reductions
    or prohibitions. A caller must validate targets, pay costs and resolve the
    healing effect; this helper never makes an illegal heal legal.
    """
    integer(potential, 'pre-cap healing potential', 0)
    integer(actual_hp_gained, 'actual HP gained', 0)
    if (not present_record(record) or not legal_effect or not magical or potential == 0
            or 'family.bleeding' not in record.get('tags', [])
            or (remover_requires_actual_hp and actual_hp_gained == 0)):
        return 'none'
    # The registry, not a guessed display name, must provide the endpoint.
    endpoint = record.get('magicalHealingEndpoint', 'none')
    if endpoint not in ('end', 'saveToEnd', 'none'):
        raise SpellRuleError('Unknown healing cure endpoint')
    return endpoint


def refresh_bleed_duration(remaining, base_duration, *, requested=2,
                           prolonged=False, owned=True, qualifying_trigger=True,
                           explicit_hard_cap=None):
    """Refresh an EXISTING finite Bleed; base duration is never itself a cap."""
    integer(remaining, 'existing remaining ticks', 1)
    integer(base_duration, 'printed base duration', 1)
    integer(requested, 'requested legal refresh duration', 1)
    if explicit_hard_cap is not None:
        integer(explicit_hard_cap, 'express source hard cap', 1)
        if remaining > explicit_hard_cap:
            raise SpellRuleError('Existing duration already exceeds its stated hard cap')
    if not owned or not qualifying_trigger:
        return remaining
    replacement = max(requested, 4 if prolonged and base_duration == 2 else 0)
    refreshed = max(remaining, replacement)
    return min(refreshed, explicit_hard_cap) if explicit_hard_cap is not None else refreshed


def extinguishable_records(records):
    """IDs ended by one legal Action/full immersion; caller validates that action."""
    return [r['applicationId'] for r in records if present_record(r)
            and 'family.ongoing-fire' in r.get('tags', [])
            and r.get('ordinaryExtinguishable', False)
            and not r.get('mundaneExtinguishingProhibited', False)
            and not r.get('specialExtinguishingPrerequisiteUnmet', False)]


def fire_ending_save_eligible(record, *, regular_turn_end):
    """Called after due damage/tick consumption; None ticks means indefinite."""
    if not regular_turn_end or not present_record(record) or 'family.ongoing-fire' not in record.get('tags', []):
        return False
    remaining = record.get('remainingTicks')
    if remaining is not None:
        integer(remaining, 'remaining scheduled ticks', 0)
    return record.get('genericDexEndingSave', False) and (remaining is None or remaining > 0)


def brutality_pre_damage(hp, maximum_hp, *, perceived, hostile, distance, operative=True):
    integer(maximum_hp, 'maximum HP', 1)
    integer(hp, 'pre-damage current HP', 0, maximum_hp)
    integer(distance, 'distance', 0)
    return operative and perceived and hostile and distance <= 60 and 4*hp <= maximum_hp


def consume_retribution(record):
    if record['mechanicalId'] != 'paladin.vengeance-mark.retribution' or not active_record(record):
        raise SpellRuleError('An active Retribution mark is required')
    if record.get('nextSmiteBonusSpent', False):
        raise SpellRuleError('Retribution die already spent')
    # Preserve expiry, opportunity benefit, eligibility and unrelated marks.
    return dict(record, nextSmiteBonusSpent=True)


def doomed_timestamp_expiry(expiry, now, *, finite_positive_buff, already_accelerated_this_turn=False):
    integer(expiry, 'buff expiry timestamp', 0)
    integer(now, 'current timestamp', 0)
    if not finite_positive_buff or already_accelerated_this_turn:
        return expiry
    return max(0, expiry-6)


def hp_recovery(state, amount, *, prohibited=False):
    integer(amount, 'HP restoration amount', 0)
    return heal(state, 0 if prohibited else amount)


def death_save_with_hp_prohibition(state, natural, *, prohibited=False, **kwargs):
    """Keep core legal-roll/turn validation; replace only blocked natural-20 gain.

    No intermediate result is published and no healing/condition hooks fire here.
    For a blocked natural20, kwargs must supply stable_d4 and now_seconds as for
    ordinary stabilization; the original state remains unchanged.
    """
    out = death_save(state, natural, **kwargs)
    if natural == 20 and prohibited:
        out = replace(out, hp=0)
        stabilize(out, kwargs.get('stable_d4'), kwargs.get('now_seconds', 0))
    return out


def stable_recovery_with_hp_prohibition(state, now_seconds, *, prohibited=False):
    integer(now_seconds, 'current timestamp', 0)
    if prohibited:
        # Preserve the original deadline even when already due. Core damage/death
        # handling cancels it if stability is lost; ending prohibition can retry it.
        return replace(state)
    return stable_recovery(state, now_seconds)
