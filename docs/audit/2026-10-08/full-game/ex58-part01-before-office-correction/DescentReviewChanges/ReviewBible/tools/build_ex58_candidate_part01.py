"""Author the first seven EX58 directions as readable, unreviewed chapter modules.

Preserves the downloaded verdict unchanged. This is not the complete 58-question
candidate, a runtime implementation, or approval of any option.
"""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
from fractions import Fraction
import json
import re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
PKG = A / 'ex58-final-gpt-verdict'

def read(p):
    return json.loads(p.read_text('utf-8-sig'))

def info(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}

def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

SECTIONS = [
    {
        'id': 'FL-01', 'title': 'The rules used on an expedition',
        'player': '''Use the current [Core resolution](../CORE_RESOLUTION_PLAYTEST.md), [combat and actions](../COMBAT_ACTION_PLAYTEST.md), [conditions](../CONDITIONS_PLAYTEST.md), [healing and death](../HEALING_DEATH_PLAYTEST.md), and [creature lifecycle](../CREATURE_LIFECYCLE_PLAYTEST.md) chapters. Their detailed procedures also apply during travel, camp work and recovery. An expedition assignment supplies neither another Action nor a second resource allowance.

A dying creature makes its death save at the start of its regular turn; an extra turn supplies no additional death save. Wounds use the current damage-event save and retain their linked injuries. A Critical Wound reduces Speed by 10 and applies its current healing ceiling. Use the actual harvest's size, time, partial-work and hurried-work rules. Older summaries of end-turn death saves, automatic critical-hit Wounds, reduced Hit-Dice healing per Wound, half Speed at Critical Wounds, or a generic one-hour hurried harvest do not replace those procedures.

An exact activity keeps its own assistance, interruption, output, training and recovery rules. Apply only the abilities, spells, recipes and items your character has actually acquired and can currently use, with their real costs, components, charges and timing. A name on a comparison list does not grant it.''',
        'director': '''This module is an overlay beside the preserved original Loop v1.2. Keep the reviewed roll/damage/Wound/death, action/stance, condition/control, Strain/rest, body/equipment, creature/device lifecycle, language, recipe and acquired class/spell rules controlling within their own scope. Do not add generic team, critical-output or restoration rewards to an exact procedure.

The existing LAX, NWX, LRX and TEX fulfillments and 687 internal/433 public recipe scopes remain unchanged. The 136 reviewed standalone low-rank procedures require their complete authored representation and actual class access; do not invent a conversion into a different runtime. Blink remains null and unavailable. Pending cards stay pending; this module changes no class, feat or spell approval. Ordinary spell totals remain 412 reviewed and 436 pending.''',
    },
    {
        'id': 'FL-02', 'title': 'Members, teams and offices',
        'player': '''An Expedition has at most **12 member characters**, including recruited NPCs and hirelings assigned independent Expedition jobs. Small Expeditions can use fewer teams and undertake feasible solo tasks. The following sizes are recommendations, not entry requirements.

| Team | Suggested members | Work |
|---|---:|---|
| Combat | 4–6 | Threats, battles and immediate protection |
| Reconnaissance | 1–3 | Scouting and mapping |
| Research | 1–3 | Study and identification |
| Resource | 2–4 | Gathering, crafting and harvesting |
| Support | 1–3 | Camp, care, repair and transport |

Appoint the five source offices: **Expedition Leader**, **Quartermaster**, **Routekeeper**, **Surgeon**, and **Claimant of Record**. The Leader represents the company and records tied organizational decisions; the Quartermaster tracks provisions, Load, cargo priority, wages and losses; the Routekeeper maintains the map; the Surgeon directs Wound treatment and casualty transport; the Claimant of Record maintains provenance, contracts and ownership documents. One person can hold several offices. An office grants no skill, extra Action or power over another player's consent or another owner's property.

Before work, record each member's primary activity or Rest, location, intended result, lead and assistants, and actual start/end times. Short tasks may follow one another. A person cannot perform incompatible activities during the same seconds. For a generic expedition task, up to three trained assistants who provide meaningful help each add +1. Exact crafting, harvesting, preservation, social and companion procedures use their own assistance rules instead.

Porters, bearers, guards and drivers contracted as members occupy roster seats. A public ship or caravan's external crew stays on its own service record and is not additional party labor or automatic combat support. Animals and source-bound noncharacter companions/devices do not occupy character seats; an intelligent creature recruited as an autonomous expedition character does. Larger forces use distinct cooperating Expeditions with real communication, shared finite resources and the same world clock.''',
        'director': '''Check concurrent roster membership by actual role, not a convenient label. Track actual encounter participants separately from roster membership, with each companion's source caps. Holding two offices never creates two workers. A remote scout cannot transmit knowledge or lend a class/item benefit without actual communication and the relevant rule.

Resolve parallel teams chronologically. If one team's narrated activity reaches hour 8, resolve the other teams' events before hour 8 before advancing beyond it. Their work does not add another eight hours to the world.

The downloaded EC-01 contract mistakenly includes Lorekeeper and omits two source offices. The candidate uses the five offices quoted above from GAMEPLAY_LOOP_CANON.md section 3, as FL-02 directs. The original contract remains preserved; a narrow correction has been requested from GPT. This local correction is explicit and is not a claim that GPT has already confirmed it.''',
    },
    {
        'id': 'FL-03', 'title': 'One clock, work and rest',
        'player': '''The campaign uses one elapsed clock. A Watch is eight hours; a day contains Morning, Afternoon and Evening Watches. Combat rounds, rests, travel, treatment and work occupy their actual time within that clock. Completing a task does not add a second Watch. Entering Haven, changing teams or starting initiative does not reset elapsed time.

A generic Watch task needs **480 active minutes** before its completion check. Feasible unfinished work can continue in another Watch, without a proportional completion reward. Exact recipes, uninterrupted training, treatment, rest and spells keep their own interruption rules. Guarding, travelling, casting, directing, interpreting, assisting or working cannot also count as incompatible rest. Passive carriage qualifies for rest only when a genuinely suitable safe berth and the actual rest requirements are satisfied.

Plan at most two active work Watches and one Rest Watch per person each day. Evening is the default Rest slot; change it prospectively before that day's first assignment. Voluntary extra noncrafting travel or guard duty can replace Rest and incur its real costs and Rest Debt. This supplies no third crafting, training, research or harvesting Watch. Emergencies still consume time and interrupt the activity underway.

Missing a scheduled Rest creates **Rest Debt**. If an emergency interrupts Rest, the debt opens after that emergency ends; otherwise it opens when the missed Rest Watch ends. Complete a qualifying safe eight-hour Rest by the end of the second following canonical Watch. If the debt remains unpaid at that deadline, gain 1 Strain once for that due event and keep owing the Rest. Missing another scheduled Rest while indebted gives 1 Strain and resets the deadline. There is no automatic additional Strain every second or every Watch merely because the same debt remains.

A safe eight-hour Rest clears the debt even when you cannot receive another Long Rest's benefits. Keep the separate limits: one beneficial Long Rest per 24 elapsed hours, two beneficial Short Rests between beneficial Long Rests, the existing four-hour Morale Rest, and 24-hour Haven care. Trance reduces sleep, not the eight-hour Long-Rest requirement. Use the actual Strain and recovery chapter for what can be removed.''',
        'director': '''Record nonnegative integer seconds from one campaign epoch. Watch w is [epoch + 28,800w, epoch + 28,800(w + 1)); a day is 86,400 seconds. Preserve Opening 2,400 hours and Horn 1,200 hours as literal scheduling receipts only. The Opening start is one recorded epoch event, not a fresh clock for each entry. This module supplies no post-Opening access or next-Cycle renewal and interprets no cosmology.

Measure actual work to the second and display minutes/hours. Generic interrupted progress remains only while physically feasible; actual loss can undo it. Travel's nominal tranche is distinct from its adjusted elapsed duration. No general Watch label changes an exact procedure's active-work requirements or crafting's own two-Watch productive ceiling.

At equal timestamps, use this order outside initiative:

1. Finish actual transfers/consumption and protection endings under their precise endpoint rules.
2. Evaluate due food/water support and blocks.
3. Complete qualifying rest/treatment; a safe Rest can clear debt here.
4. Process a still-unpaid debt deadline.
5. Settle completed activity/travel.
6. Coalesce extraction checkpoints.
7. Apply once-per-event/Watch Pressure and its bounded complication batch.
8. Run due faction/checkpoint reporting.

Combat's own expiration, death, start and periodic ordering controls inside initiative. Do not backdate supplies, protection, rest or rewards after learning an outcome. Stable recovery retains its original absolute deadline and does not replay at a Watch boundary. Later route, Pressure and faction modules supply their full procedures; this partial module does not substitute for them.''',
    },
    {
        'id': 'FL-04', 'title': 'Supply and daily support',
        'player': '''**Supply is a basket of real goods:** 2 lb of ration-equivalent edible food, 8 pints of potable water, 1 pint of compatible lamp oil in its flask, and 0.25 lb of ordinary camp sundries. The food and water cover one Small or Medium character's daily demand; Large characters require twice those quantities. This is game accounting. Two pounds of food equal three reviewed Cooking servings; a Large food day is six servings.

Track food and water actually consumed, by recipient and lot. Ordinary partial rations credit their edible mass. A fractional magical meal never gives a fractional benefit unless its own source permits that. The same serving cannot be spent in a recipe and remain available to eat.

Oil and sundries are spent when actually used. Do not burn spare oil or throw away sound stock to satisfy an abstract daily debit. The source lamp burns one pint in six hours. One actual light may serve several people within its real illumination, with its fuel spent once. A sufficient daylight or other safe lighting plan can use no oil; extra darkness, heating or work needs its real equipment and fuel.

At each canonical 24-hour day endpoint, settle each recipient's actual food, water and necessary declared logistics support. A recipient short of any requirement gains **1 expedition Strain total for that day's shortfall**. Missing food and water does not give two Strain. Retain partial consumption credit. The unsupported day blocks Strain removal; that block can clear on a later day only with a real sufficient provisioning plan available and maintained. Crossing a gate does not erase needs: actual Haven/home support pays needs outside the expedition.

Allocate shortages before the deadline. Joining, leaving or changing size/form divides demand by actual time and diet; it never refunds goods already consumed. A diet exception removes only its stated obligation. It gives no transferable provisions, fuel or camp labor. Unsupported nonmount Tiny, Huge or Gargantuan diets require their real profiles; mounts use their separate profiles.

If an exact procedure charges **one whole Supply**, reserve and commit the entire physical basket, or a substitute that procedure actually permits. Wound treatment keeps its one-Supply cost at the start, even if treatment fails or is interrupted. Food or water genuinely consumed by its named patient or healer can credit that person's daily need once. The committed basket does not also remain in inventory or feed another person.''',
        'director': '''Model one canonical recipient/day settlement with unique consumption and shortfall events. Demand is proportional to actual seconds inside each interval; retain exact rational amounts rather than rounding at every transfer. With a changed dietary coefficient, integrate each coefficient over its real interval. Outside-expedition support is separate actual provisioning, not an exemption.

A missed necessary logistics task retains its actual exposure/visibility consequence and may leave that recipient unsupported. It does not universally cause hunger or automatically add another Strain. The once-daily shortfall includes all missing components. Later failure retains or creates its real event without refunding past consumption. Death/collapse still follows the reviewed Strain rule.

Food, water, fuel, containers and sundries remain distinct physical lots with origin, custody, mass, volume and clocks. Donations transfer stock; they do not replenish the donor's consumed history. A full procedural basket and nutrition credits must point to the same actual goods and use events. No virtual Supply token exists alongside the contents. Keep every no-resource, no-sale or similar source restriction through transfers and repacking.''',
    },
    {
        'id': 'FL-05', 'title': 'Buying, packing and keeping provisions',
        'player': '''Use actual stock and a provider's real quote. These reference prices do not guarantee a seller or inventory.

| Item | Source price | Source weight or capacity |
|---|---:|---|
| Rations, one day | 5 sp | 2 lb |
| Oil, full flask | 1 sp | 1 lb, flask included |
| Torch | 1 cp | 1 lb |
| Tinderbox | 5 sp | 1 lb |
| Waterskin | 2 sp | 1 lb empty; 4 pints capacity; 5 lb full |
| Bedroll | 1 gp | 7 lb |
| Blanket | 5 sp | 3 lb |
| Two-person tent | 2 gp | 20 lb |
| Hooded lantern | 5 gp | 2 lb empty |
| Bullseye lantern | 10 gp | 2 lb empty |

The new ordinary camp-sundry unit costs 2 cp and weighs 0.25 lb. It contains expendable cloth, twine and cleaning material; it provides no medical-kit charge, reagent, repair stock or magical effect. At the Core low-tier water reference (Tiers I–III), 1 cp buys 8 pints of actual clean water. At Tiers IV–VI, that quantity costs 10 cp. Containers are separate.

A standard low-tier basket refill costs **63 cp** and weighs **11.25 lb**, including its new full oil flask but excluding drinking-water containers. Two new empty waterskins add 40 cp and 2 lb, making the first portable basket **103 cp, 13.25 lb, or 1.325 Load**. At the high-tier water reference, the basket is 72 cp, or 112 cp with two new skins, before any other local price changes. Do not add a waterskin's full weight and its water again. Tents, tools, clothing, lighting apparatus and medical kits remain separate capital goods.

The Core ordinary meal reference buys one 2/3-lb serving: 2 cp at Tiers I–III or 5 sp at Tiers IV–VI. Three such servings supply a Small/Medium food day. These are immediate ordinary meals without spell/recipe benefits. Packing requires a real container and preserves the existing 24-hour cooked-food clock; a meal does not become a preserved ration by being purchased.

Ordinary dry sealed rations expire 30 elapsed days after actual packing unless their source lot supplies a different interval. Retain known prior age. Clean potable water has no arbitrary expiry while its suitable sealed container stays clean; contamination needs an actual event. Raw meat, organs, essences and cooked meals keep their own clocks. Check weight, volume, shape, closure and weather independently. Replacing packaging does not renew age.

Filling one skin/flask or issuing one standard basket takes one active minute per worker, sequentially. A sealed prepacked handover instead uses actual item-access time. The new ordinary oil-flask profile divides its printed 1 lb into 0.25 lb empty flask and 0.75 lb oil per full pint. With half a pint remaining, the intact flask weighs 0.625 lb. Keep an actually defined particular container's own tare when different. An empty flask is still that object; it has no automatic resale value or fuel credit.''',
        'director': '''The sundry price/mass, water and meal quantity mappings, ordinary ration expiry, handling minute and oil-flask tare split are explicit NEW EX58 choices beside the original source fields. Do not rewrite printed source values or turn absent fields into historical data. The low-tier basket arithmetic is 50 + 1 + 10 + 2 = 63 cp and 2 + 8 + 1 + 0.25 = 11.25 lb. Initial skins add 40 cp and 2 lb. A partial ordinary flask weighs 0.25 + 0.75 × remaining pints. A broken or burned vessel follows its actual loss without producing an intact duplicate.

Keep source-qualified magic finite:

- Purify Food and Drink removes only its reviewed nonmagical contaminants from one real separated food batch of at most 5 lb OR at most one gallon of drink. It creates no amount and does not reverse spoilage.
- Conjure Water retains its at-most-one-gallon output, one active batch, one-hour maximum, recall on recast and once-per-recipient/24-hour hydration. Credit only actual consumption before its endpoint. It creates no saleable stored stock, reagent or whole Supply.
- Shape Water moves actual eligible water. Water Breathing changes respiration, not hydration, swimming Speed or cargo capacity.
- Goodberry and all other sources keep their exact recipient, output, access, cost and lifetime. There is no general conversion from a food-spell name into Supply.

Holy water, oil or a named marrow is not edible by its label. A full medical kit and proper recipe material remain separately required. Actual support equipment may be shared only within its real functional limits. This comparison does not activate a pending spell or give a character unacquired access.''',
    },
    {
        'id': 'FL-06', 'title': 'Foraging a finite place',
        'player': '''A generic Forage attempt requires 480 active minutes, suitable gathering implements and access to a real opportunity. The lead makes WIS (Survival) against the route-tier DC; up to three trained assistants can provide meaningful +1 help unless an exact source changes that procedure.

The opportunity has an ordinary Sustenance allowance S from 0 to 4 and actual food, water and material quantities. Sustenance 0 gives no routine award. Success can recover up to S provision-equivalent units. Critical Success can recover up to **S + ceil(S/2)**, but the extra must come from an existing recorded reserve. A good roll cannot supply absent water, lamp oil, animals, herbs or industrial sundries.

Receive the actual gathered goods. A food-only site supplies food, not a complete basket. A complete Supply requires every component to exist and its real gathering/packing work to be completed. The recovered amount cannot exceed the site's real remaining allowance and matter.

Teams using the same opportunity share its allowance. Use one lead/check or genuinely disjoint portions allocated in advance, with no more total stock than the parent site contains. A new Watch, renamed site, new container or return visit does not replenish the place. Record gathered, ruined, inaccessible, forfeited and remaining quantities.

Failure gives nothing and ends that attempt; an unchanged immediate retry is unavailable. On Critical Failure, contaminate one actual selected ordinary provision unit only when a predeclared contamination hazard supports it; otherwise add 1 Pressure once for that cause. An actual class/background permission to gather during a beneficial Long Rest supplies only its named product and real components. It does not also complete generic Forage or create a second local pool.''',
        'director': '''Before the attempt, record the opportunity's site/route-segment ID, physical bounds, initial food/water/material vector, prior claims, ordinary S allowance and disjoint critical reserve. The sustainable physical limit is separate from S: S is the ordinary recoverable allowance, and the critical extra is at most ceil(S/2) from the pre-existing reserve. Do not infer matter from a route rating.

Simultaneous and serial claimants share the same unresolved claim. Any subdivisions preserve the parent's aggregate ordinary and extra allowances. Later genuine growth, delivery, replenishment or a newly accessible disjoint area can establish a new opportunity with its own physical quantity and lineage; a new map label or a Director boolean alone cannot.

Do not duplicate fishing, carcass, mining or salvage claims. A critical failure supplies no invented poison, property or nonexistent victim. Keep the once-per-cause Pressure event, rather than adding another because the same failure appears in a team summary.''',
    },
    {
        'id': 'FL-07', 'title': 'Building and using a camp',
        'player': '''Choose a legally accessible, stable 20 × 20 ft site with actual drainage, weather protection and space for the inhabitants and gear. A camp's name alone does not make it safe. An exposed bivouac needs no build task and has no certified storage; its real exposure remains.

One build task requires 480 active Support minutes and a STR or WIS check using an actually relevant tool/Survival proficiency against the tier DC. Up to three trained assistants can help. Success earns one build mark; Critical Success earns two; failure earns none. Reserve required materials before work and record their installation. Failure spends time and only goods actually damaged or used. Feasible unfinished physical progress survives a pause.

| Camp | Required work and new fixtures | Storage limit |
|---|---|---|
| Temporary Camp | 1 Support mark; real sleeping shelters; fitting pack, 20 lb/2 gp | 20 Load / 200 lb / 20 ft³ |
| Fortified Outpost | 3 total Support marks, including Temporary; additional timber/stone/fasteners, 300 lb/60 gp | 60 Load / 600 lb / 60 ft³ |
| Research Station | Fortified, plus 2 Research marks; desk/weatherproof record storage, 50 lb/25 gp | 60 Load / 600 lb / 60 ft³ |
| Forward Base | 8 total marks: 3 Fortified Support, 2 Research, 3 further Support; extra depot stock, 500 lb/100 gp; actual faction approval and a contracted functioning supply/evacuation line | 150 Load / 1,500 lb / 150 ft³ |

Each new storage limit replaces the previous limit. The Temporary fitting pack provides rope, pegs, ground covering and racks. Existing actual compatible fixtures may replace it by recorded quantities. Tents, bedrolls, tools, light and food are separate. The source two-person tent holds two Small/Medium sleeping places, or one Large place under this new rule.

An intact watched Fortified perimeter gives its warning benefit against attackers using that perimeter. It does not remove Surprise from betrayal, unseen infiltration, teleportation or an unwatched direction. A functioning Outpost gives the source +1 to feasible repair checks; it does not reduce hours or material costs or improve manufacture.

Research marks each require the completed Research work and an INT check using the actual relevant skill at the tier DC. A functioning Research Station gives +2 to legitimate research/identification checks. Libraries, instruments, evidence, active-core containment and exact recipe stations are still independently required. It supplies no universal knowledge or creation bonus.

A Forward Base's Haven link is the actual contracted service, with real carriers, crew, capacity, journey time, price and risk. It is not instant resupply, resurrection, teleportation or evacuation. None of these fixture kits is food, an independent recipe or an automatic salvage payout.''',
        'director': '''Maintain one build ledger per site. Teams can work on separate necessary portions; they cannot reroll a finished step for additional marks or fixtures. Record installed and surviving materials, marks, sleeping places, guards, alarms, lighting, care/work surfaces, closures and current hazards. Rest or Wound-treatment safety depends on those actual conditions. Camp tiers do not create every trade's workshop.

The supply-line record names endpoints, provider, carrier bodies/crew, trip capacity, paid charges, departure/arrival times, risk and missed deliveries. A depot label does not create a delivery.

A Severe complication can degrade exactly one achieved tier or require evacuation only when its actual damage/discovery supports that consequence. Preserve surviving materials and prior marks. Restore affected functionality through one newly necessary build task and actual lost-material replacement. Exposure removes concealment/warning predicates only as actually compromised. If storage capacity falls, relocate the excess; do not delete cargo. No replacement grants a duplicate intact item or resets a reward claim.''',
    },
]

CASES = [
    {'id': 'EX01-01', 'questions': ['FL-02', 'FL-03'], 'given': 'Two teams each work from campaign hour 0 to hour 8.', 'expected': 'The world reaches hour 8, not hour 16. Each actual worker has one compatible interval; team labels create no extra hours.'},
    {'id': 'EX01-02', 'questions': ['FL-03'], 'given': 'A generic task has 300 active minutes, then resumes for 180 feasible active minutes in a later Watch.', 'expected': 'It reaches one 480-minute completion check. The earlier interruption gave no partial completion reward. An exact uninterrupted recipe or training source may behave differently.'},
    {'id': 'EX01-03', 'questions': ['FL-03'], 'given': 'An unpaid Rest Debt deadline and the completion of a qualifying safe eight-hour Rest are both at campaign second 144000.', 'expected': 'Complete the Rest and clear debt before processing the still-unpaid-debt step. That debt causes no deadline Strain. Long-Rest reward eligibility remains a separate clock.'},
    {'id': 'EX01-04', 'questions': ['FL-04'], 'given': 'A Medium recipient has no food and no potable water at the same daily settlement.', 'expected': 'One shortfall event gives 1 expedition Strain total and the unsupported-day block. It does not give one Strain for each missing component.'},
    {'id': 'EX01-05', 'questions': ['FL-04'], 'given': 'A recipient spends half a canonical day with the Medium coefficient and half with the Large coefficient.', 'expected': 'That day requires 3 lb food and 12 pints water. Goods already consumed remain consumed. No form-change refund or new daily window appears.'},
    {'id': 'EX01-06', 'questions': ['FL-04', 'FL-05'], 'given': 'Four people use one suitable actual lamp for six hours, with its light genuinely sufficient for all four.', 'expected': 'Spend one pint of lamp oil once. Do not charge four pints merely because four support records refer to that lamp.'},
    {'id': 'EX01-07', 'questions': ['FL-05'], 'given': 'Buy a standard low-tier basket and two new empty waterskins at the stated reference prices.', 'expected': 'Pay 103 cp and carry 13.25 lb after packing. The eight pints of water are counted once, plus two pounds of skin tare.'},
    {'id': 'EX01-08', 'questions': ['FL-05'], 'given': 'The ordinary new one-pint oil-flask profile has half a pint of oil remaining.', 'expected': 'It weighs 0.25 + 0.75 × 0.5 = 0.625 lb. The same intact flask remains; no duplicate empty flask is generated.'},
    {'id': 'EX01-09', 'questions': ['FL-06'], 'given': 'A Sustenance-3 opportunity contains its ordinary allocation and a real extra reserve equivalent to one unit. The check is a Critical Success.', 'expected': 'The formula permits at most two extra units, but the reserve permits only one. Recover at most four actual provision-equivalent units with their real component vector, not five invented baskets.'},
    {'id': 'EX01-10', 'questions': ['FL-06'], 'given': 'Two teams rename a depleted site and visit during the next Watch without actual replenishment.', 'expected': 'No new stock or allowance exists. Their changed labels and timing cannot support a second award.'},
    {'id': 'EX01-11', 'questions': ['FL-07'], 'given': 'An otherwise qualifying camp reaches Forward Base with all baseline new fixture packs.', 'expected': 'It has 8 required marks and 150 Load storage. The baseline packs total 870 lb/187 gp; prior capacities do not add to the new capacity. Shelter and real supply-line costs remain separate.'},
    {'id': 'EX01-12', 'questions': ['FL-01', 'FL-02'], 'given': 'A Quartermaster holds another office and reads a pending spell name in a supplies comparison.', 'expected': 'Neither the second office nor the comparison grants an extra work interval, spell acquisition, class access or pending-option approval.'},
]

def render_player(data):
    lines = ['# Expeditions — organization, time, provisions and camps', '', data['notice'], '']
    for section in data['sections']:
        lines.extend(['## ' + section['title'], '', section['text'], ''])
    return '\n'.join(lines)

def render_director(data):
    lines = ['# Director expedition procedures — organization, time, provisions and camps', '', data['notice'], '', 'Read the complete companion [player module](EXPEDITION_PART01_PLAYER.md) alongside this procedure module. Together these are the first seven source directions, not the complete expedition chapter.', '']
    for section in data['sections']:
        lines.extend(['## ' + section['title'], '', section['text'], ''])
    lines.extend(['## Authored boundary examples', '', 'These are expected tabletop outcomes. No full game runtime or human playtest has been executed by this module.', ''])
    for c in data['workedCases']:
        lines.extend(['### ' + c['id'], '', c['given'], '', c['expected'], ''])
    return '\n'.join(lines)

def main():
    output = {
        'internal': R / 'data/director/expedition_candidate/part01.json',
        'public': R / 'data/public/expedition_candidate/part01.json',
        'player': R / 'docs/mechanics/expedition/EXPEDITION_PART01_PLAYER.md',
        'director': R / 'docs/mechanics/expedition/EXPEDITION_PART01_DIRECTOR.md',
        'receipt': A / 'EX58_CANDIDATE_PART01_CHECK.json',
    }
    assert not any(p.exists() for p in output.values()), 'Preserve previous module artifacts before revision'
    checks = []
    def ck(name, result):
        checks.append({'name': name, 'pass': bool(result)})
        assert result, name
    manifest = read(PKG / 'FILE_MANIFEST.json')
    for x in manifest['files']:
        ck('GPT final payload preserved: ' + x['path'], info(PKG / x['path']) == {k: x[k] for k in ['bytes', 'sha256']})
    archive = A / 'DD_Expedition_58_Source_Verdict_and_Evidence_2026_10_11.zip'
    ck('Verified final archive unchanged', info(archive)['sha256'] == '98444b380e08aba6f3848cd2824245b52c8428e6a1b913907567dceeee04470e')
    all_directions = read(PKG / 'EX58_AUTHORING_REGISTER.json')['directions']
    source = {x['id']: x for x in all_directions}
    ids = [x['id'] for x in SECTIONS]
    ck('Exactly FL-01 through FL-07 authored', ids == [f'FL-{i:02d}' for i in range(1, 8)])
    contracts = [x for x in read(PKG / 'EX58_FIELD_CONTRACTS.json')['contracts'] if x['id'] in ['EC-01', 'EC-02', 'EC-03', 'EC-04']]
    loop = R / 'docs/mechanics/GAMEPLAY_LOOP_CANON.md'
    loop_text = loop.read_text('utf-8-sig')
    offices = ['Expedition Leader', 'Quartermaster', 'Routekeeper', 'Surgeon', 'Claimant of Record']
    for name in offices:
        ck('Source office preserved: ' + name, '- **' + name + ':**' in loop_text and '**' + name + '**' in SECTIONS[1]['player'])
    ck('Original contract inconsistency is preserved, not silently corrected', 'Lorekeeper' in contracts[0]['requiredFields']['offices'])
    public = {
        'schemaVersion': 1, 'moduleId': 'EX58-PART01', 'status': 'authored-partial-candidate-awaiting-exact-review',
        'notice': 'Working chapter module 1. This covers organization, time, provisions and camps. Route, extraction, transport, Haven, social and reputation chapters are still being assembled; this is not yet the complete expedition candidate.',
        'questionIds': ids, 'completeExpeditionCandidate': False, 'selectionEnabled': False,
        'sections': [{'id': x['id'], 'title': x['title'], 'text': x['player']} for x in SECTIONS],
    }
    director = {'notice': public['notice'], 'sections': [{'id': x['id'], 'title': x['title'], 'text': x['director']} for x in SECTIONS], 'workedCases': CASES}
    internal = {
        'schemaVersion': 1, 'moduleId': public['moduleId'], 'status': public['status'],
        'sourceReview': 'EX58-SOURCE-2026-10-11', 'sourceAssistantMessageId': 'f9effea2-510e-4529-a141-a3c1932008f3',
        'completeExpeditionCandidate': False, 'authoredQuestionIds': ids,
        'remainingSourceDirections': [x['id'] for x in all_directions if x['id'] not in ids],
        'publicEnvelope': public, 'directorModule': director,
        'completeOriginalDirections': [source[x] for x in ids], 'completeOriginalContracts': contracts,
        'sourceOfficeExcerpt': loop_text[loop_text.index('Every Expedition designates:'):loop_text.index('## 4. Expedition objectives')],
        'officeContractDiscrepancy': {
            'source': 'FL-02 requires the five named source offices; Loop section3 lists them exactly.',
            'originalEC01': contracts[0]['requiredFields']['offices'],
            'candidateOffices': offices,
            'proposedReplacement': 'Expedition Leader, Quartermaster, Routekeeper, Surgeon and Claimant of Record, bound to actual members. One member may hold several offices, but receives no extra skill, Action, authority over consent/property, or incompatible simultaneous work interval.',
            'gptCorrectionRequested': True, 'gptCorrectionConfirmedInThisModule': False,
        },
        'audienceBoundary': 'Public module contains general procedures only; no faction dossiers, secret plans, private backers, resonance keys or campaign records are copied from other package files.',
        'semanticCoverageNote': 'Manually authored against the seven complete directions. Structural and arithmetic checks do not certify semantic completeness; final full-candidate review remains required.',
        'examplesAreRuntimeTests': False, 'runtimeImplemented': False, 'newPromotions': 0,
    }
    frozen = read(A / 'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest']
    for rel, expected in frozen.items():
        if rel != 'README_EXPEDITION_INTEGRATED_V3.md':
            ck('Original submission current file preserved: ' + rel, info(G / rel) == expected)
    ck('Twelve authored cases cover every selected direction', len(CASES) == 12 and set(ids) <= {i for c in CASES for i in c['questions']})
    numbers = [
        ('eight-hour Watch seconds', 8 * 60 * 60, 28800),
        ('generic resumed minutes', 300 + 180, 480),
        ('low-tier basket cp', 50 + 1 + 10 + 2, 63),
        ('initial portable basket cp', 63 + 2 * 20, 103),
        ('high-tier basket cp', 50 + 10 + 10 + 2, 72),
        ('high-tier initial cp', 72 + 40, 112),
        ('basket pounds', Fraction(2 + 8 + 1) + Fraction(1, 4), Fraction(45, 4)),
        ('initial basket pounds', Fraction(45, 4) + 2, Fraction(53, 4)),
        ('initial basket Load', Fraction(53, 4) / 10, Fraction(53, 40)),
        ('half-pint full object pounds', Fraction(1, 4) + Fraction(3, 4) * Fraction(1, 2), Fraction(5, 8)),
        ('mixed-size food pounds', Fraction(1, 2) * 2 + Fraction(1, 2) * 4, 3),
        ('mixed-size water pints', Fraction(1, 2) * 8 + Fraction(1, 2) * 16, 12),
        ('finite critical forage', 3 + min(2, 1), 4),
        ('forward marks', 3 + 2 + 3, 8),
        ('all baseline fixture pounds', 20 + 300 + 50 + 500, 870),
        ('all baseline fixture gp', 2 + 60 + 25 + 100, 187),
    ]
    for label, actual, expected in numbers:
        ck('Plain arithmetic only: ' + label, actual == expected)
    save(output['internal'], internal)
    save(output['public'], public)
    for key, txt in [('player', render_player(public)), ('director', render_director(director))]:
        output[key].parent.mkdir(parents=True, exist_ok=True)
        output[key].write_text(txt, encoding='utf-8', newline='\n')
    ck('Full saved public envelope matches explicit projection', read(output['public']) == read(output['internal'])['publicEnvelope'])
    ck('Full player chapter matches saved public envelope', output['player'].read_text('utf8') == render_player(read(output['public'])))
    ck('Full Director chapter matches saved internal representation', output['director'].read_text('utf8') == render_director(read(output['internal'])['directorModule']))
    link_count = 0
    for key in ['player', 'director']:
        for target in re.findall(r'\]\(([^)]+)\)', output[key].read_text('utf8')):
            ck('Local chapter link: ' + target, (output[key].parent / target).resolve().is_file())
            link_count += 1
    for x in manifest['files']:
        ck('GPT payload unchanged after authoring: ' + x['path'], info(PKG / x['path']) == {k: x[k] for k in ['bytes', 'sha256']})
    receipt = {
        'generatedAtUtc': datetime.now(timezone.utc).isoformat(), 'moduleId': public['moduleId'],
        'status': 'Seven directions authored in two partial chapter modules; exact full candidate incomplete and unreviewed.',
        'questionIds': ids, 'remainingDirections': len(all_directions) - len(ids),
        'workedCases': len(CASES), 'arithmeticChecks': len(numbers), 'linkChecks': link_count,
        'checks': len(checks), 'failures': [x for x in checks if not x['pass']],
        'scope': 'Archive/source preservation, representation parity, real local links and plain arithmetic. Authored examples are not executed gameplay scenarios.',
        'outputs': {str(p.relative_to(G)).replace('\\', '/'): info(p) for k, p in output.items() if k != 'receipt'},
        'builder': {'path': Path(__file__).resolve().relative_to(G).as_posix(), **info(Path(__file__))},
        'officeCorrectionPending': True, 'runtimeTestsExecuted': 0, 'newPromotions': 0, 'sourceInformationDeleted': 0,
        'details': checks,
    }
    save(output['receipt'], receipt)
    print(json.dumps({k: receipt[k] for k in ['moduleId', 'questionIds', 'remainingDirections', 'workedCases', 'arithmeticChecks', 'checks', 'failures', 'outputs']}, indent=2))

if __name__ == '__main__':
    main()
