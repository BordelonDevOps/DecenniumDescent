# Exact review: three selected healing extensions

Codex → Calibration Review. Please reply below15,000 characters. The39-source redirection implementation is underway from your corrections; this parallel bounded packet implements the THREE corrections from your131-source discussion. Review the exact helper/test/guide, challenge errors, then explicitly close only these interfaces if warranted.

1. Crown's Burn recipients: code requires predeclaration. Oracle.engine[26] says target choices fixed at activation; your earlier correction's numbered list selected after damage. Confirm before damage/rolls; no new opportunistic recipient change. Enhanced mastery only expands legal range.
2. Backlash minimum modifies resolved DAMAGE after ordinary defenses, not minimum surviving HP; suppression cancels whole packet. Pipeline caller supplies valid rolled/defended damage and actual suppressor.
3. Dual Echo permits TWO eligible Mend profiles from different creatures. Caller owns paid costs/record consumption, action/eligibility. Numeric halves floor once, zero new dice; explicit additional dice separately tracked.

These are reference primitives, not complete class engines. Broad131-source scope and fullgame remain open. Inputs already establish valid acquisition, ranges/targets, costs, rolls and history.


## Exact Oracle engine[26]

Oracle zone default: choose at most three allies and three enemies for each pulse or aura benefit, fixed at activation unless the card names fewer. Persistent damaging/healing zones require concentration and at most three pulses. Pay 1 RC before each pulse after the first, or end the effect; once-per-long-rest Finals include their printed pulses in that limited use. One pulse can affect a creature only once per round. Passive personal resistance and a single-target temporary buff are not zones.

## Exact oracle.supplement.flame.crown-s-burn

{"id": "oracle.supplement.flame.crown-s-burn", "name": "Crown's Burn", "className": "Oracle", "band": "Arch", "path": "Flame", "sourceKind": "tier-ii-revelation", "minimumClassLevel": 6, "acquisition": "choose first at Oracle 6; a distinct second at Oracle 13", "activation": "Action", "cost": "2 RC", "rangeAndTarget": "3-tile-radius burst centered within 4 tiles", "duration": "Damage/healing instantaneous; penalties until end of next turn", "frequency": "At will while RC remains", "effect": "Enemies in the burst make Dexterity saves, taking 2d6+M fire damage on failure or half on success. A failing enemy also has -1 on attack rolls until the end of its next turn. Total the actual fire damage dealt to meaningful hostile creatures, then divide by the number of allied recipients chosen in the burst; up to three living allies in the burst each regain the lesser of that share or S d6+M HP, minimum 1 if any qualifying damage was dealt. Each healed ally reduces the first fire damage it takes before your next turn by S.", "prerequisite": "Oracle 6; Mystery: Flame; selected Tier II Revelation", "source": {"line": null, "reference": "MYSTERIES.ORACLE_MYSTERIES[5].tierII[0]", "originalText": "", "status": "source-derived", "originalObjects": [{"reference": "MYSTERIES.ORACLE_MYSTERIES[5].tierII[0]", "value": {"name": "Crown's Burn", "charges": 2, "kind": "active", "description": "Spend 2 charges: unleash a 3-tile burst of shard-fire — enemies take 2d6 fire damage and must save or suffer −10% hit until end of next turn; allies in the burst heal half the total damage dealt to enemies (minimum 1d6), and the Crown's embers cling — allies healed this way gain +5% DR vs fire until start of your next turn."}}]}, "designStatus": "provisional-playtest", "spellRank": null}

## Exact oracle.supplement.flame.zealot-s-renewal

{"id": "oracle.supplement.flame.zealot-s-renewal", "name": "Zealot's Renewal", "className": "Oracle", "band": "Arch", "path": "Flame", "sourceKind": "tier-ii-revelation", "minimumClassLevel": 6, "acquisition": "choose first at Oracle 6; a distinct second at Oracle 13", "activation": "Action", "cost": "2 RC", "rangeAndTarget": "One living ally within 3 tiles; adjacent enemies", "duration": "Instantaneous; fire ward until start of your next turn", "frequency": "At will while RC remains", "effect": "The ally regains 2 S d8+M HP, then takes 1d4 fire backlash that cannot be reduced below 1 unless First Flame Convergence suppresses it. It may end Poisoned or immediately repeat one disease save. Until the start of your next turn it reduces the first fire damage it takes by S. Hostile creatures adjacent to the healed ally take 1d4 fire damage once from scattering embers.", "prerequisite": "Oracle 6; Mystery: Flame; selected Tier II Revelation", "source": {"line": null, "reference": "MYSTERIES.ORACLE_MYSTERIES[5].tierII[1]", "originalText": "", "status": "source-derived", "originalObjects": [{"reference": "MYSTERIES.ORACLE_MYSTERIES[5].tierII[1]", "value": {"name": "Zealot's Renewal", "charges": 2, "kind": "active", "description": "Spend 2 charges: one ally within 3 tiles regains HP equal to your Charisma modifier × level tier (minimum 1d8) but takes 1d4 fire backlash — wrathful healing; the Crown's embers cling — they end one minor poison or disease, gain +5% DR vs fire until start of your next turn, and adjacent enemies take 1d4 fire as cursed ash scatters from the renewal."}}]}, "designStatus": "provisional-playtest", "spellRank": null}

## Exact tools/healing_source_extensions.py

"""Selected131-source extensions under exact review; not complete class execution."""
from dataclasses import dataclass
from spell_playtest_rules import integer,SpellRuleError


def zealot_backlash(after_fire_defenses, *, explicitly_suppressed=False):
    """Separate packet after heal ATTEMPT, not conditional on actualHP restored.

    The source minimum modifies resolved DAMAGE, not survivingHP. Caller rolls
    1d4, applies defenses, establishes an actual suppression source, then sends
    this result through ordinary tempHP/HP/Wound/death handling.
    """
    integer(after_fire_defenses,'backlash after ordinary fire defenses',0)
    return 0 if explicitly_suppressed else max(1,after_fire_defenses)


def crown_burn_healing(total_actual_fire_damage, recipient_ids, *, shared_cap_total,
                       scale, roll_instance_id):
    """Source base only: predeclared legal recipients; caller validates range/use.

    Numeric qualifying fire damage, not merely positive packet existence. Each
    resulting base runs its own healing pipeline. The source minimum is before
    target reductions/prohibitions; it does not promise1 actualHP through Decay.
    One shared cap roll retains S healing dice for per-die modifiers.
    """
    integer(total_actual_fire_damage,'qualifying numeric actual fire damage',0)
    integer(shared_cap_total,'shared Sd6+M healing-cap result',1)
    integer(scale,'class scaling S',1,4)
    if not roll_instance_id:raise SpellRuleError('Shared healing roll needs identity')
    ids=tuple(recipient_ids)
    if len(ids)>3 or len(ids)!=len(set(ids)):
        raise SpellRuleError('Crown Burn requires0–3 distinct legal recipients')
    if not ids or total_actual_fire_damage==0:return []
    amount=max(1,min(total_actual_fire_damage//len(ids),shared_cap_total))
    return [{'targetId':ident,'sourceBase':amount,'diceCount':scale,
             'rollInstanceId':roll_instance_id} for ident in ids]


@dataclass(frozen=True)
class MendRecord:
    record_id: str
    source_creature_id: str
    target_id: str
    rolled_profile_amount: int
    source_roll_id: str

    def __post_init__(self):
        if not all((self.record_id,self.source_creature_id,self.target_id,self.source_roll_id)):
            raise SpellRuleError('Mend record requires source/record/target/roll identities')
        integer(self.rolled_profile_amount,'legal rolled Mend profile amount',0)


def dual_mend_components(records):
    """Selected two-Mend case of Dual Echo Cast, NOT Echo Fusion.

    Caller pays both RP costs, consumes both eligible captured records and spends
    the one combined release/action before resolving these components. Inputs
    are each legal printed profile total; no critical dice/resource/rider copy.
    Both may target the same legal ally. Numeric halves are flat copied amounts;
    later explicitly added real dice remain a separately tracked modifier.
    """
    if len(records)!=2 or len({r.record_id for r in records})!=2:
        raise SpellRuleError('Dual Echo Cast needs2 distinct records')
    if len({r.source_creature_id for r in records})!=2:
        raise SpellRuleError('Dual Echo Cast records must come from different creatures')
    return [{'targetId':r.target_id,'sourceBase':r.rolled_profile_amount//2,
             'diceCount':0,'recordId':r.record_id,'sourceRollId':r.source_roll_id,
             'copiedNumeric':True} for r in records]


## Exact tools/validate_healing_extensions.py

from pathlib import Path
import json
from healing_source_extensions import *
from healing_playtest_rules import LifeState,survival_damage_event,healing_packet,HealingReduction
ROOT=Path(__file__).resolve().parents[1]

def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append(name)
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append(name)
        else:raise AssertionError(name)
    check('Immunity0 cannot remove explicit minimum backlash damage',zealot_backlash(0),1)
    check('An actual suppression source cancels the whole backlash',zealot_backlash(4,explicitly_suppressed=True),0)
    out,event=survival_damage_event(LifeState(20,1),zealot_backlash(0),wound_natural=20)
    check('Backlash is not survival floor and can drop ally to0',(out.hp,out.dead,event['woundSaves']),(0,False,1))
    out,event=survival_damage_event(LifeState(20,1,temp_hp=1),zealot_backlash(0))
    check('TemporaryHP still absorbs resolved minimum backlash',(out.hp,out.temp_hp,event['actualDamageDealt']),(1,0,1))
    healed=healing_packet(LifeState(20,1),8,hp_gain_prohibited=True)['state']
    out,event=survival_damage_event(healed,zealot_backlash(2),wound_natural=20)
    check('Blocked healing does not cancel later backlash',(out.hp,event['resolvedDamage']),(0,2))
    kw=dict(shared_cap_total=7,scale=2,roll_instance_id='cap-roll')
    check('No recipients skips division and healing',crown_burn_healing(20,[],**kw),[])
    check('Positive packet numeric0 generates no Crown healing',crown_burn_healing(0,['a'],**kw),[])
    rows=crown_burn_healing(23,['a','b','c'],**kw)
    check('Shared cap applies equally against floored share',[r['sourceBase'] for r in rows],[7,7,7])
    check('One shared roll with real S dice survives provenance',[(r['rollInstanceId'],r['diceCount']) for r in rows],[('cap-roll',2)]*3)
    rows=crown_burn_healing(5,['a','b'],**kw)
    check('Damage share is floored once before recipient pipeline',[r['sourceBase'] for r in rows],[2,2])
    rows=crown_burn_healing(1,['a','b','c'],**kw)
    check('Positive numeric pool invokes printed source minimum1',[r['sourceBase'] for r in rows],[1,1,1])
    check('Source minimum cannot bypass recipient healing prohibition',healing_packet(LifeState(20,1),rows[0]['sourceBase'],hp_gain_prohibited=True)['actualHpGained'],0)
    rejects('Recipients cannot be duplicated to change division',lambda:crown_burn_healing(10,['a','a'],**kw))
    rejects('More than3 recipients remains illegal',lambda:crown_burn_healing(10,list('abcd'),**kw))
    records=[MendRecord('one','creature-A','ally',9,'roll-one'),MendRecord('two','creature-B','ally',7,'roll-two')]
    components=dual_mend_components(records)
    check('Two paid eligible Mend profiles survive Dual Echo classification',[r['sourceBase'] for r in components],[4,3])
    check('Same ally may receive both supplied components',[r['targetId'] for r in components],['ally','ally'])
    check('Copied half amounts carry zero new dice',[r['diceCount'] for r in components],[0,0])
    target=LifeState(20,1)
    penalty=HealingReduction('desecrated','desecrated','per-die',1)
    for c in components:target=healing_packet(target,c['sourceBase'],dice_count=c['diceCount'],reductions=[penalty])['state']
    check('Per-die penalty cannot invent dice on flat half copies',target.hp,8)
    rejects('Same source creature cannot supply both captures',lambda:dual_mend_components([records[0],MendRecord('two','creature-A','ally',7,'two-roll')]))
    rejects('Same record cannot be consumed twice',lambda:dual_mend_components([records[0],records[0]]))
    report={'status':'PASS','reviewStatus':'IN_REVIEW; exact extension implementation pending',
            'scope':'Three corrected source interfaces only: Zealot backlash, Crown Burn pooled/shared healing and Dual Echo two-Mend numeric components. Caller ownership/cost/action, scheduler and broader copy lifecycle are not implemented here.',
            'checkCount':len(checks),'checks':checks}
    (ROOT/'docs/mechanics/HEALING_EXTENSION_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS{len(checks)} selected healing-extension checks; exact review pending.')
if __name__=='__main__':main()


## Exact docs/mechanics/HEALING_EXTENSION_VALIDATION.json

{
  "status": "PASS",
  "reviewStatus": "IN_REVIEW; exact extension implementation pending",
  "scope": "Three corrected source interfaces only: Zealot backlash, Crown Burn pooled/shared healing and Dual Echo two-Mend numeric components. Caller ownership/cost/action, scheduler and broader copy lifecycle are not implemented here.",
  "checkCount": 20,
  "checks": [
    "Immunity0 cannot remove explicit minimum backlash damage",
    "An actual suppression source cancels the whole backlash",
    "Backlash is not survival floor and can drop ally to0",
    "TemporaryHP still absorbs resolved minimum backlash",
    "Blocked healing does not cancel later backlash",
    "No recipients skips division and healing",
    "Positive packet numeric0 generates no Crown healing",
    "Shared cap applies equally against floored share",
    "One shared roll with real S dice survives provenance",
    "Damage share is floored once before recipient pipeline",
    "Positive numeric pool invokes printed source minimum1",
    "Source minimum cannot bypass recipient healing prohibition",
    "Recipients cannot be duplicated to change division",
    "More than3 recipients remains illegal",
    "Two paid eligible Mend profiles survive Dual Echo classification",
    "Same ally may receive both supplied components",
    "Copied half amounts carry zero new dice",
    "Per-die penalty cannot invent dice on flat half copies",
    "Same source creature cannot supply both captures",
    "Same record cannot be consumed twice"
  ]
}


## Exact docs/mechanics/HEALING_SOURCE_EXTENSIONS.md

# Healing source extensions — remaining class passages

**Discussed, implementation review in progress.** All131 remaining class passages have individual roles in the [source register](HEALING_REMAINING_SOURCE_BINDINGS.md), with [exact-source verification](HEALING_REMAINING_SOURCE_VALIDATION.json). This does not close every listed card. Read the [first captured discussion](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_REMAINING_REVIEW_PARTIAL.md) together with the [complete tail and corrections](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_REMAINING_CORRECTIONS.md); the first capture alone is incomplete.

The previously reviewed [153-source interface](HEALING_DEATH_PLAYTEST.md) remains the arithmetic/life-state reference, with the narrow Paladin Wave cadence amendment below. Original sources and earlier interpretations remain preserved.

## Three corrected source procedures

### Zealot's Renewal backlash

Attempt the healing first. Its Poisoned/disease option is an independent component, so lack of actual HP gain does not prevent that option. Unless a printed Convergence/Prophecy feature suppresses the backlash, roll its separate1d4 fire packet, apply ordinary defenses, then enforce at least1 resolved backlash damage. Fire immunity alone therefore does not eliminate this particular source's minimum.

This minimum concerns damage, not the creature's surviving HP. Then temporary HP, normal HP loss, Wounds and dying/death apply normally. A creature at1HP without temporary HP can fall to0 from the backlash; a legal temporary-HP buffer can absorb it. A blocked heal still has its backlash unless expressly suppressed.

### Crown's Burn pooled healing

Use the numeric actual fire damage dealt to qualifying meaningful hostile creatures, including absorbed temporary HP and excluding overkill as defined in the reviewed interface. A positive packet that inflicts zero numeric actual damage contributes zero.

For up to3 distinct legal allied recipients, divide the total by the recipient count and round down. Use one shared `S d6 + M` healing-cap roll for the burst. If the numeric total is positive, each recipient's source base is `max(1, min(share, sharedCapRoll))`. With no recipients, skip healing; with numeric total0, generate no healing application.

Each resulting target application then receives its own ordinary healing modifiers/restrictions. The source minimum does not bypass Decay or guarantee actual HP gain. Retain the same roll identity and S healing dice for each target's per-die adjustments.

The reference accepts recipients already declared legally before resolution. The corrected notebook list placed recipient selection after damage; its earlier list and Oracle's fixed-at-activation target rule support predeclaration. Confirm that narrow ordering point in exact implementation review rather than granting a new after-results target choice implicitly.

### Dual Echo Cast with two Mend profiles

Two otherwise eligible Mend records from different source creatures may both be used. Pay both RP costs, consume both records and spend the single combined release/action. Halve each legal profile's rolled amount independently, rounding down once. The resulting halves are copied numeric amounts with zero newly rolled healing dice; separately authorized additional dice retain their actual provenance.

The two components may heal the same legal ally. They are distinct supplied components; neither is erased just because both use Mend. Preserve ordinary copy/no-resource/no-recursion restrictions and shared-root causal limits. No extra release is created.

Echo Fusion's printed “only one may be healing” restriction belongs to Echo Fusion. It is not a Dual Echo Cast limitation.

The [20 extension checks](HEALING_EXTENSION_VALIDATION.json) test these selected boundaries. Full record acquisition, RP spending, target legality and command/release lifecycle remain caller/source responsibilities; these helpers are not complete class execution.

## Paladin cadence amendment

The explicit reconciliation in `paladin.engine[13]` sets level17 Full Cleansing Wave to **once per long rest**, superseding the preserved Hero card and the earlier healing guide's once-per-short-rest wording. Retain its entire remaining pool cost, target limits, cleansing option and corresponding Oathbreaker mode. Switching Oath state does not refill the pool.

Paid Smite obeys both own-turn eligibility and the shared **one paid Smite per numbered round**, including an independently allowed Reaction Smite. An off-turn Smite can therefore consume the round's allowance before the Paladin's regular turn. The Reaction source supplies that specific permission; the general rule adds no new off-turn trigger.

## Other discussed interfaces

| Source or family | Agreed direction | Remaining work |
|---|---|---|
| Divine Invocation Renewal | Printed5 Stamina co-resolves independently of actual HP gain; base Renewal retains its actual-gain requirement | Integrate exact finite Stamina resource rules |
| Purging Flame / Zealot's Renewal | Printed cure option independent of actual HP gained | Preserve each disease's actual permitted save/cure |
| Bloodbond / Flame Prophecy / Enhanced Convergence | Healing-trigger branches require actual HP restoration; Flame's damage branch uses positive fire packet | Source provenance/cadence implementation |
| Lifewell | Action+4RP+allBG establishes it; even first pulse needs same-turn BA+1RP; without that pulse, end at turn end | Paid pulse scheduler |
| Healing Briar / Restoration Field | Activation includes first pulse; later pulses require printed maintenance | Paid pulse scheduler |
| Oracle target-start healing zones | Proposed source-owned funded windows: activation window, then1RC at each next source regular start; not per ally | Exact schedule/expiry/target cap review |
| Crown Restored / Eternal Bloom Finals | Printed finite pulses included in limited use; no generic extra RC upkeep | Final-specific clocks and pulse limits |
| Renewal / Echo Totem | Shared upkeep/concentration; same-name overlap uses stronger application; fourth pulse requires paid BA+1RP | Exact echo/parent lifecycle and schedule |
| Monk maximum-HP effects | Stat changes clamp currentHP without damage/healing/Wounds; restoring maximum does not heal | Composition with other owners, bonuses and systemic multipliers |
| Veinburst Requiem | Post-damage set-to0 is a separate state component; no second Wound save or added damage metric | Broad versus damage-only floor scope and zero-state transition |
| Devices, companions and forms | Separate organic healing, functional repair, destroyed reconstruction, initialHP and finite tempHP reserves | Individual lifecycle/source evidence |
| Copies and added dice | Copied numeric halves have zero new dice; actual added dice and shared roll identities persist | Complete roll/copy provenance interface |

## Next review packages

1. Damage sharing/redirection:39 source candidates, including retargeting, prevention, prohibited transfers and actual redirection. Resolve exact pre/post-defense sequence and inherited consequences.
2. Maximum-HP composition: Monk, Flesh Warden, Exhaustion, Expedition and other exact sources.
3. Sustained zones and pulse scheduling: activation, paid source-turn windows, target-start and entry events, capacity and expiry.
4. Companion/device/temp-HP lifecycle: living companions, destroyed reconstruction, Druid Buffer Reserve and nonstacking.
5. Roll/copy provenance: exact numeric components, dice, per-die modifiers, eligible copied restrictions and shared causal limits.

Discussion dispositions identify the work; they do not replace those remaining implementation reviews or human playtesting.
