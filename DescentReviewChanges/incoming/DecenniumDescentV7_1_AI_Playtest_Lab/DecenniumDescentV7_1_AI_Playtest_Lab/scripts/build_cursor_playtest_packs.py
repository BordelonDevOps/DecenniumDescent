#!/usr/bin/env python3
from __future__ import annotations
import csv
import json
from pathlib import Path
import shutil
import textwrap
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "playtests/cursor-packs"
OUTPUT_ROOT = Path("/mnt/data")

DESIGN_RULE = "Decennium Descent should have 5e's readability and speed, Pathfinder 2e's tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems."

PLAYERS = [
    {
        "id":"bard","name":"Lyria Vox","class":"Bard","race":"Feykin","path":"Virtuoso",
        "background":"A Haven stage performer who became an expedition signal officer after surviving a caravan panic. Lyria sees every battle as a rhythm problem: establish tempo, protect the next ally's turn, and turn a small advantage into a chain.",
        "style":"Combination-focused support player; medium rules mastery; avoids hoarding resources when an ally can gain immediate tempo.",
        "interpretation":"Read the fight as an initiative and momentum puzzle. Track Crescendo, ally action access, repeated effects, and whether support decisions shorten the encounter without creating extra-action loops.",
        "tests":["Crescendo generation and loss","extra-action or cooldown-reset stacking","support contribution versus personal damage","turn time caused by sequencing"]
    },
    {
        "id":"cleric","name":"Durn Stonevow","class":"Cleric","race":"Dwarf","path":"Saint",
        "background":"A forge-cleric who served as a caravan surgeon and now judges success by how many people and how much cargo return alive.",
        "style":"Conservative support player; high system mastery; spends resources to prevent a collapse rather than topping off minor wounds.",
        "interpretation":"Read the fight through casualty prevention, Conviction economy, and recovery cost. Separate healing that changes outcomes from healing that merely inflates totals.",
        "tests":["healing per action","prevented damage","Conviction cadence","revival and wipe-prevention limits"]
    },
    {
        "id":"crimson-agent","name":"Vaela Redhand","class":"Crimson Agent","race":"Drow","path":"Thirstborn",
        "background":"A former house operative who joined the Haven undercity contracts and treats a battlefield as a network of blood states and execution windows.",
        "style":"Aggressive optimizer; high risk tolerance; prioritizes target isolation and bleed detonations.",
        "interpretation":"Read the fight as a timing exercise: establish Bleeds, decide whether to spend Blood Gauge now or compound it, and record when execution mechanics erase intended encounter phases.",
        "tests":["Bleed stacking","Blood Gauge generation/spend","execution thresholds","self-healing and snowball potential"]
    },
    {
        "id":"dragoon","name":"Kael Stormscale","class":"Dragoon","race":"Drakari","path":"Drake Rider",
        "background":"A storm-blooded courier trained to cross broken vertical routes while keeping a convoy's forward edge clear.",
        "style":"Mobile tactical player; medium-high mastery; values position and objective access over stationary damage.",
        "interpretation":"Read the fight spatially. Track Momentum earned from meaningful movement, leap access, terrain bypass, anti-air value, and whether mobility trivializes cargo or objective constraints.",
        "tests":["Momentum generation","leap range and action cost","terrain bypass","burst after movement"]
    },
    {
        "id":"druid","name":"Harka Reed","class":"Druid","race":"Amphibian","path":"Circle of the Moon",
        "background":"A marsh guide who became the expedition's emergency scout, carrier, and front-line beast when routes collapsed.",
        "style":"Flexible role-switcher; medium mastery; changes form to answer the scene rather than maximizing one damage routine.",
        "interpretation":"Read the fight by form value and transformation opportunity cost. Record effective HP, mobility, control, damage, and whether one form dominates every other option.",
        "tests":["form balance","temporary HP and healing interaction","action cost of changing form","spell-versus-form choice"]
    },
    {
        "id":"mage","name":"Ilyra Vale","class":"Mage","race":"Human","path":"Lich",
        "background":"An arcane researcher who chose the Lich path to survive long enough to solve the dungeon's violent magical problems. She is deliberately transgressive and evaluates magic by blunt effect.",
        "style":"High-system optimizer; accepts Dissonance and self-harm for decisive output; tests dark-path limits rather than playing safely.",
        "interpretation":"Read the fight as RP conversion into damage, control, and survival. Push Traumatic Casting until the system demonstrates a real stopping point; do not assume evil magic should be subtle.",
        "tests":["RP efficiency","Traumatic Casting costs","Dissonance ceiling","minion/action limits","burst versus other casters"]
    },
    {
        "id":"monk","name":"Sen Myr","class":"Monk","race":"Mycelian","path":"Iron Fist Master",
        "background":"A patient tunnel pilgrim who studies the exact moment a formation loses balance.",
        "style":"Technical melee player; high attention to reactions, positioning, and resource timing.",
        "interpretation":"Read the fight as a sequence of openings. Track movement, defensive reactions, control reliability, and whether repeated strikes or stuns monopolize table time.",
        "tests":["action density","stun/control repetition","mobility","defense without armor"]
    },
    {
        "id":"mirrorsage","name":"Orren Glass","class":"Mirrorsage","race":"Elf","path":"Shattered One",
        "background":"A failed court illusionist whose fractured reflections became useful for reconnaissance and battlefield misdirection.",
        "style":"Control-focused optimizer; high rules mastery; deliberately searches for targeting, duplicate, and line-of-sight exploits.",
        "interpretation":"Read the fight through information denial and action multiplication. Count every independent body, reaction, repeated effect, and targeting decision created by reflections.",
        "tests":["duplicate action economy","targeting ambiguity","defensive misdirection","control duration"]
    },
    {
        "id":"oracle","name":"Ysabel Threadseer","class":"Oracle","race":"Feykin","path":"Battle Mystery / Fate-Bound Curse",
        "background":"A Haven contract seer who receives accurate warnings only after the cost of avoiding them becomes visible.",
        "style":"Adaptive support-controller; medium mastery; treats the Curse as a real cost and Revelation Charges as scarce.",
        "interpretation":"Read the fight as uncertain future management. Track charge value, curse drawback frequency, information advantage, and whether prophecy removes meaningful risk.",
        "tests":["Revelation Charge cadence","Mystery/Curse tradeoff","prevention versus reaction","information power"]
    },
    {
        "id":"paladin","name":"Taran Ashward","class":"Paladin","race":"Human","path":"Oath of Chains Broken",
        "background":"A former captive escort who now protects porters, rescued prisoners, and anyone treated as cargo rather than a person.",
        "style":"Protective front-liner; medium mastery; prioritizes interception, rescue, and objective integrity.",
        "interpretation":"Read the fight by threatened allies, control of lanes, oath constraints, and the cost of smites. Record whether defense is proactive and tactically clear.",
        "tests":["interception economy","aura stacking","smite burst","oath restrictions and rewards"]
    },
    {
        "id":"ranger","name":"Pell Quickstep","class":"Ranger","race":"Elf","path":"Stalker",
        "background":"A route scout who has spent more time between the surface and Haven than inside either city.",
        "style":"Pragmatic skirmisher; medium-high mastery; prioritizes reconnaissance payoff and marked targets.",
        "interpretation":"Read the fight as the result of earlier scouting. Track first-round advantage, mark upkeep, range, ammunition, and whether exploration success translates into fair tactical benefit.",
        "tests":["mark economy","scouting-to-combat benefit","ranged sustained damage","terrain interaction"]
    },
    {
        "id":"shaman","name":"Grasha Bonewind","class":"Shaman","race":"Orc","path":"Theurgist",
        "background":"An ancestral speaker hired to keep expedition dead from becoming silent liabilities and to negotiate with spirits along old routes.",
        "style":"Zone-support player; medium mastery; places totems for team value rather than personal damage.",
        "interpretation":"Read the fight through zones, spirit access, and setup time. Count active totems, actions spent placing them, overlap, and whether the battlefield becomes too difficult to adjudicate.",
        "tests":["totem limit","zone stacking","setup payoff","summoned spirit actions"]
    },
    {
        "id":"soldier","name":"Mara Venn","class":"Soldier","race":"Human","path":"Champion",
        "background":"A professional expedition commander who believes every fight should have an objective, a reserve, and a retreat path.",
        "style":"Disciplined generalist; high tactical literacy; does not chase damage when Guard, formation, or cargo protection wins the scene.",
        "interpretation":"Read the fight as the baseline tactical class. Track commands, formation bonuses, weapon output, defense, and how quickly a new player can choose an effective action.",
        "tests":["baseline DPR","command value","formation clarity","turn speed"]
    },
    {
        "id":"thief","name":"Salira Dusk","class":"Thief","race":"Goblin","path":"Shadowblade",
        "background":"A route thief turned licensed recovery specialist who measures every room by exits, cover, locks, and unattended value.",
        "style":"Opportunistic player; medium mastery; seeks advantage but avoids suicidal isolation.",
        "interpretation":"Read the fight through access and escape. Track stealth reliability, bonus-action congestion, burst from advantage, objective interaction, and retreat contribution.",
        "tests":["stealth rules","burst setup","bonus-action competition","non-damage objectives"]
    },
    {
        "id":"tinker","name":"Zeetes","class":"Tinker","race":"Gnome","path":"Artificer",
        "background":"A workshop inventor who entered the dungeon to test devices under real conditions and now serves as a convoy engineer.",
        "style":"Creative systems player; high option count; tests gadgets exactly as written before proposing improvisation.",
        "interpretation":"Read the fight as an equipment and preparation test. Count setup actions, construct actions, repair value, consumable expenditure, and decision delay caused by too many options.",
        "tests":["construct command budget","gadget action cost","repair and cargo interaction","option overload"]
    },
    {
        "id":"warrior","name":"Orrik Stonewake","class":"Warrior","race":"Ogre","path":"Wardborn",
        "background":"A Haven gate laborer whose size and durability made him the person sent into collapsing passages first.",
        "style":"Low-complexity martial player; low-medium rules mastery; chooses the clearest strong action.",
        "interpretation":"Read the fight as the accessibility benchmark for melee play. Track damage, durability, forced movement, and whether the class has a meaningful decision beyond repeating attacks.",
        "tests":["simple-turn effectiveness","durability","forced movement","choice density"]
    },
    {
        "id":"wizard","name":"Edrin Vale","class":"Wizard","race":"Human","path":"Necromancer",
        "background":"A scholarly corpse-researcher who treats undeath as an engineering problem and is willing to use overwhelming necromantic trauma.",
        "style":"Planner and exploit hunter; high mastery; tests prepared spell breadth and minion constraints aggressively.",
        "interpretation":"Read the fight as spell preparation plus controlled-unit management. Push the Necromancer's blunt-force identity while logging every action, body, and decision added to the round.",
        "tests":["prepared spell dominance","undead action economy","summon cap","high-tier control and damage"]
    },
]


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip()+"\n", encoding="utf-8")


def generic_result_schema(function_name: str):
    return {
        "$schema":"https://json-schema.org/draft/2020-12/schema",
        "title":f"Decennium Descent {function_name} Playtest Result",
        "type":"object",
        "required":["pack","scenarioId","agentId","observations","metrics","rulesQuestions","exploits","recommendations"],
        "properties":{
            "pack":{"type":"string"},"scenarioId":{"type":"string"},"agentId":{"type":"string"},
            "seed":{"type":["integer","string","null"]},
            "observations":{"type":"array","items":{"type":"string"}},
            "metrics":{"type":"object","additionalProperties":True},
            "rulesQuestions":{"type":"array","items":{"type":"string"}},
            "exploits":{"type":"array","items":{"type":"string"}},
            "recommendations":{"type":"array","items":{"type":"string"}},
            "confidence":{"type":"string","enum":["low","medium","high"]}
        }
    }


def compile_script():
    return r'''#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent
results = sorted((ROOT / "results").rglob("*.json"))
report = ROOT / "COMPILED_REPORT.md"
rows = []
for path in results:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append((path, data))
    except Exception as exc:
        rows.append((path, {"agentId":"PARSE_ERROR","scenarioId":"unknown","observations":[str(exc)],"metrics":{},"rulesQuestions":[],"exploits":[],"recommendations":[]}))

questions = Counter()
exploits = Counter()
recommendations = Counter()
by_scenario = defaultdict(list)
for path, data in rows:
    by_scenario[data.get("scenarioId","unknown")].append(data)
    questions.update(data.get("rulesQuestions",[]))
    exploits.update(data.get("exploits",[]))
    recommendations.update(data.get("recommendations",[]))

lines = ["# Compiled Cursor Multi-Agent Playtest Report", "", f"Result files: **{len(rows)}**", ""]
for scenario, entries in sorted(by_scenario.items()):
    lines += [f"## Scenario: {scenario}", ""]
    for entry in entries:
        lines += [f"### Agent: {entry.get('agentId','unknown')}", ""]
        metrics = entry.get("metrics",{})
        if metrics:
            lines.append("**Metrics**")
            for k,v in metrics.items(): lines.append(f"- {k}: {v}")
        for title, key in [("Observations","observations"),("Rules questions","rulesQuestions"),("Exploits","exploits"),("Recommendations","recommendations")]:
            vals = entry.get(key,[])
            if vals:
                lines.append(f"**{title}**")
                lines += [f"- {v}" for v in vals]
        lines.append("")

def top(counter, title):
    lines.extend([f"## {title}", ""])
    if not counter:
        lines.append("- None reported.")
    else:
        for item,count in counter.most_common(30): lines.append(f"- ({count}) {item}")
    lines.append("")

top(questions,"Repeated rules questions")
top(exploits,"Repeated exploit findings")
top(recommendations,"Repeated recommendations")
report.write_text("\n".join(lines)+"\n", encoding="utf-8")
print(report)
'''


def base_readme(title: str, function: str, result_name: str):
    return f'''# {title}

## Purpose

This pack covers the gameplay function that cannot be completed through authorship alone: **{function}**.

The written rules are canonical. This pack tests whether the numbers, timing, clarity, incentives, and edge cases work in repeated play.

## Required repository

Run from the root of **DecenniumDescent V7 Gameplay Complete**. Read first:

1. `AGENTS.md`
2. `CANON_MANIFEST.json`
3. `docs/mechanics/DESIGN_DOCTRINE.md`
4. `docs/mechanics/GAMEPLAY_LOOP_CANON.md`
5. The sources listed in `SOURCE_MANIFEST.json`

## Cursor workflow

1. Unzip this pack into `playtests/runs/{result_name}/`.
2. Open the repository root in Cursor.
3. Start one orchestrator agent using `CURSOR_ORCHESTRATOR_PROMPT.md`.
4. Create the specialist agents listed in `AGENT_ROSTER.md`.
5. Give each agent only its dedicated file plus the scenario and canonical sources it needs.
6. Agents must write JSON results under `results/<scenario-id>/<agent-id>.json` using `RESULT_SCHEMA.json`.
7. Do not let agents edit canon files during testing.
8. Run `python compile_results.py`.
9. Return `COMPILED_REPORT.md`, the raw `results/` directory, and any proposed patches separately.

## Governing rule

> {DESIGN_RULE}

## Evidence standard

- Distinguish observed behavior from prediction.
- Record the exact rule and file path behind every finding.
- Use fixed seeds or a written deterministic decision order when possible.
- Never call a rule balanced because one simulation succeeded.
- Do not rewrite lore or reveal Director-only information in public tests.
'''


def create_combat_pack():
    pack = PACK_ROOT / "01-combat-class-balance"
    shutil.rmtree(pack, ignore_errors=True)
    (pack / "agents/players").mkdir(parents=True)
    write(pack/"README_FIRST.md", base_readme("Combat and Class Balance Pack", "combat timing, class output, spell/feat interactions, summons, control, bosses, and retreat", "combat"))
    write(pack/"CURSOR_ORCHESTRATOR_PROMPT.md", f'''# Orchestrator Prompt

You are the lead playtest coordinator. Do not modify canonical rules.

Read the scenario matrix, Director protocol, Observer protocol, exploit protocol, and every selected player's dedicated file. For each scenario:

1. Spawn one Director agent.
2. Spawn one Rules Observer agent.
3. Spawn one Combat Metrics agent.
4. Spawn the player agents listed by class in the scenario.
5. Run at least 10 seeds for Standard and Hard encounters and at least 5 seeds for Severe/Boss encounters.
6. Each player decides only from its own knowledge and persona. The Director does not optimize players.
7. Record every turn, action, bonus action, reaction, movement, resource spend, condition, summon action, damage, healing, objective progress, and retreat decision.
8. Require result JSON from every agent.
9. Stop and flag a scenario when an infinite loop, automatic win, unavoidable loss, or rules deadlock is demonstrated.
10. Compile the results but do not average away outliers.

Primary questions:

- Are turns readable and fast?
- Are action costs and triggers explicit?
- Does every class have a meaningful recurring decision?
- Do extra actions, cooldown resets, summons, control, or healing break the round?
- Do encounter budgets predict actual danger?
- Can retreat and cargo-defense objectives function without improvised rules?

Governing rule: {DESIGN_RULE}
''')
    write(pack/"AGENT_ROSTER.md", "# Agent Roster\n\n- `agents/director.md`\n- `agents/rules-observer.md`\n- `agents/combat-metrics.md`\n- `agents/exploit-hunter.md`\n- One dedicated file under `agents/players/` for every class participating in a scenario.\n")
    write(pack/"agents/director.md", '''# Director Agent

Run enemies and terrain faithfully, not vindictively. State objectives, visible hazards, exits, cargo, and telegraphs before the first turn. Use the listed encounter budget and creature rules. Do not alter HP or damage to force a desired result. Log all adjudications, unclear triggers, and moments when the intended difficulty diverges from actual play.
''')
    write(pack/"agents/rules-observer.md", '''# Rules Observer Agent

Do not make player decisions. Track every lookup, ambiguous timing word, undefined condition, stacking question, and disagreement. Measure time-to-resolution in decision steps: a decision made from one obvious rule is 1; each additional cross-reference adds 1. Flag any turn requiring more than three source lookups.
''')
    write(pack/"agents/combat-metrics.md", '''# Combat Metrics Agent

Record rounds, turns, actions, bonus actions, reactions, movement, damage, healing, prevented damage, temporary HP, RP/RC/other resource spend, conditions applied, full turns denied, summons active, objective progress, retreat progress, knockouts, Wounds, and real or estimated decision time. Calculate DPR and effective damage prevented separately.
''')
    write(pack/"agents/exploit-hunter.md", '''# Exploit Hunter Agent

Search specifically for infinite or repeatable action loops, cooldown reset loops, summon multiplication, permanent control, immunity stacking, healing-resource loops, forced-movement loops, unavoidable executions, and combinations that bypass cargo or encounter objectives. Demonstrate an exploit with an exact turn sequence and file references; do not report vague suspicion as proof.
''')

    player_index=[]
    for p in PLAYERS:
        filename=f"player-{p['id']}.md"
        player_index.append({"id":p['id'],"class":p['class'],"file":f"agents/players/{filename}"})
        write(pack/"agents/players"/filename, f'''# Player Agent: {p['name']} — {p['class']}

## Character background

{p['background']}

## Build identity

- Race: {p['race']}
- Class: {p['class']}
- High-level path used when available: {p['path']}
- Player style: {p['style']}

## How this player interprets fights

{p['interpretation']}

## Decision protocol

1. Read the visible objective, terrain, allies, enemies, and known resources.
2. State the intended outcome of the turn before choosing mechanics.
3. Choose a legal Action, Bonus Action if granted, Movement, and Reaction plan.
4. Do not use information the character has not learned.
5. Do not choose a deliberately weak option unless the persona or fiction supports it.
6. Do not coordinate through hidden omniscient information.
7. Declare retreat when the character's background and visible risk justify it.
8. Record why the chosen option was clearer or stronger than alternatives.

## Required class-specific tests

{chr(10).join('- '+x for x in p['tests'])}

## Required combat-loop output

Write `results/<scenario-id>/{p['id']}.json` with:

- Actions by round.
- Resource totals before and after.
- Damage, healing, prevention, control, and objective contribution.
- Number of rule lookups.
- Any moment the player lacked a meaningful choice.
- Any option that was always correct or never rational.
- Any rule that slowed the turn.
- Confidence and recommended change.
''')
    write(pack/"PLAYER_INDEX.json", json.dumps(player_index,indent=2))

    scenarios = [
      ["CMB-L1-BASE","1","Standard","Soldier,Cleric,Thief,Mage","2 equal-level foes","Open chamber; kill or rout","20"],
      ["CMB-L3-CARGO","3","Hard","Paladin,Ranger,Tinker,Warrior","mixed foes","Protect 12-Load medicine crate for 4 rounds","20"],
      ["CMB-L5-MOBILITY","5","Hard","Dragoon,Monk,Thief,Crimson Agent","mobile skirmishers","Control three elevated objectives","15"],
      ["CMB-L5-SUPPORT","5","Hard","Bard,Cleric,Oracle,Soldier","two-wave opposition","Measure tempo, healing, and extra-action pressure","15"],
      ["CMB-L10-DARK","10","Severe","Mage,Wizard,Mirrorsage,Shaman,Tinker","boss plus adds","Stress summons, duplicates, Traumatic Casting, control","10"],
      ["CMB-L10-BOSS","10","Boss","Soldier,Paladin,Druid,Ranger,Bard,Cleric","two-phase boss","Objective, telegraphs, Tenacity, retreat state","10"],
      ["CMB-L15-CONTROL","15","Severe","Monk,Mirrorsage,Oracle,Wizard","elite enemies","Attempt full-turn denial chains","10"],
      ["CMB-L15-ATTRITION","15","Hard","Warrior,Dragoon,Crimson Agent,Cleric","three sequential encounters","No Long Rest; track resource curve","10"],
      ["CMB-L20-CEILING","20","Catastrophic","all classes in rotating 6-PC parties","high-level boss suites","Find ceilings, loops, and dead options","5 per party"],
      ["CMB-RETREAT","8","Severe","Ranger,Thief,Soldier,Tinker","unkillable pursuer proxy","Use three-success Retreat procedure","15"],
    ]
    with (pack/"SCENARIO_MATRIX.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["scenarioId","level","difficulty","players","opposition","objective","iterations"]); w.writerows(scenarios)
    write(pack/"SOURCE_MANIFEST.json", json.dumps({"required":[
        "docs/mechanics/GAMEPLAY_LOOP_CANON.md","data/public/Decennium_Descent_Gameplay_Loop_v1.json","src/data/class-core-mechanics.js","src/data/class-details.js","src/data/class-paths.js","src/data/feats.js","src/data/spells.js","src/data/spell-placements.json","data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json","src/bestiary_data_full.json"
    ]},indent=2))
    write(pack/"RESULT_SCHEMA.json", json.dumps(generic_result_schema("Combat"),indent=2))
    write(pack/"REPORT_TEMPLATE.md", '''# Combat Playtest Executive Summary

## Tested scenarios
## Class findings
## Action-economy findings
## Encounter-budget accuracy
## Summon/control/healing exploit findings
## Readability and turn-speed findings
## Proposed numerical changes
## Proposed wording changes
## Rules left unchanged and why
''')
    write(pack/"compile_results.py", compile_script())
    (pack/"results").mkdir()


def create_expedition_pack():
    pack=PACK_ROOT/"02-expedition-extraction"
    shutil.rmtree(pack,ignore_errors=True); (pack/"agents/players").mkdir(parents=True)
    write(pack/"README_FIRST.md",base_readme("Expedition and Extraction Pack","Watch assignments, routes, Pressure, Supply, camps, cargo, casualties, retreat, and extraction decisions","expedition"))
    write(pack/"CURSOR_ORCHESTRATOR_PROMPT.md",f'''# Orchestrator Prompt

Run complete expeditions from preparation through Haven arrival. Use twelve separate player agents. Each agent receives one roster file. The Director resolves routes and complications without protecting the party from declared consequences.

For every scenario:

1. Record sponsor, treasury, objective, abort conditions, starting Supply, free Load, route Length/Risk/Mapping/Capacity, and clock hour.
2. Run every eight-hour Watch with assignments for all twelve members.
3. Resolve Pressure openly.
4. Require cargo priority before extraction.
5. State at-risk cargo before each extraction response.
6. Continue until Haven arrival, abandonment, total failure, or seal.
7. Run at least 10 iterations per scenario.
8. Compile profitability, casualties, elapsed hours, Pressure, unused team roles, and decision bottlenecks.

Governing rule: {DESIGN_RULE}
''')
    roster=[
      ("01-mara-vann.md","Mara Venn","Soldier","Combat","Expedition Leader","Protect mission objective and maintain a reserve. Interpret fights as obstacles to the declared expedition objective, not opportunities to chase kills."),
      ("02-orrik-stonewake.md","Orrik Stonewake","Warrior","Combat","Rear Guard","Hold narrow routes and carry casualties. In fights, prioritize lane control and survival over damage racing."),
      ("03-taran-ashward.md","Taran Ashward","Paladin","Combat","Escort Lead","Protect porters and rescued people. Interpret every fight through who is threatened and what must be extracted."),
      ("04-salira-dusk.md","Salira Dusk","Thief","Reconnaissance","Routekeeper","Find exits and alternate routes. In fights, prioritize objectives, locks, cover, and escape setup."),
      ("05-pell-quickstep.md","Pell Quickstep","Ranger","Reconnaissance","Scout","Convert scouting into fair tactical advantage and warn when continuing is irrational."),
      ("06-edrin-vale.md","Edrin Vale","Wizard","Research","Claimant of Record","Identify risks and provenance. In fights, spend magic to protect irreplaceable information and samples."),
      ("07-ysabel-threadseer.md","Ysabel Threadseer","Oracle","Research","Risk Analyst","Use warnings without erasing uncertainty. Interpret fights through predicted failure states and remaining charges."),
      ("08-harka-reed.md","Harka Reed","Druid","Resource","Harvester","Preserve ecosystem knowledge and useful materials. In fights, choose forms that protect harvest access and retreat."),
      ("09-zeetes.md","Zeetes","Tinker","Support","Quartermaster","Track every Load, Supply, tool, and repair. In fights, protect transport and test whether cargo actions are worth their Action cost."),
      ("10-durn-stonevow.md","Durn Stonevow","Cleric","Support","Surgeon","Track Wounds and casualty capacity. In fights, intervene only when it changes survival or extraction."),
      ("11-ilse-harrow.md","Ilse Harrow","Porter Captain","Support","Transport Chief","Represent non-class specialists and labor limits. In fights, seek cover, secure cargo, and refuse implausible heroic behavior."),
      ("12-toma-glass.md","Toma Glass","Alchemist","Resource","Preservation Lead","Protect perishable and volatile cargo. In fights, assess whether substances and consumables create profitable or abusive loops."),
    ]
    for fn,name,cls,team,office,interp in roster:
        write(pack/"agents/players"/fn,f'''# Expedition Player: {name}

- Class or specialty: {cls}
- Team: {team}
- Office: {office}

## Background

{name} is a working member of a Haven-bound company whose reputation depends on bringing people, records, and cargo back rather than merely reaching depth.

## How to interpret fights

{interp}

## Watch protocol

- Choose one legal team activity each Watch.
- State the expected benefit and opportunity cost.
- Track personal Strain, Wounds, Load, and rest debt.
- Do not use information from other teams until shared in play.
- Record whether the assignment felt meaningful.
- During combat, log whether expedition stakes changed target choice, action choice, or retreat timing.
''')
    write(pack/"AGENT_ROSTER.md","# Agent Roster\n\nUse all twelve files under `agents/players/`, plus a Director, Quartermaster Auditor, and Rules Observer.\n")
    write(pack/"agents/director.md","# Director\n\nCreate routes and complications according to the canonical procedure. State risks before choices. Never hide random cargo deletion. Track the Opening clock and public knowledge boundary.\n")
    write(pack/"agents/quartermaster-auditor.md","# Quartermaster Auditor\n\nIndependently recalculate Supply, Load, Capacity, Extraction Class, sponsor shares, cargo priority, and losses. Report every mismatch.\n")
    write(pack/"agents/rules-observer.md","# Rules Observer\n\nTrack whether all twelve players have meaningful Watch decisions, whether parallel resolution is manageable, and every rule lookup or ambiguity.\n")
    scenarios=[
      ["EXP-T1-PROFIT","Tier I","12 days","Mapped Risk 1 route","Reach first Gate region, return profitable","10"],
      ["EXP-HAVEN-RUN","Tier II/Haven","20 days","Mixed mapped/sketched routes","Deliver inward cargo; extract 8,000 gp","10"],
      ["EXP-T3-LONG","Tier III","30 days","Sketched Risk 3 route","Survey and return with one Rare lot","10"],
      ["EXP-T4-DARK","Tier IV","18 days","Unknown Risk 4 route","Investigate symptoms without confirming hidden lore","10"],
      ["EXP-HORN-RACE","Tier II","Hour 1080","Mapped route becomes compromised","Extract before Hour 1200","15"],
      ["EXP-CASUALTY","Tier III","14 days","Capacity constrained","Return with two Downed members and Living cargo","10"],
    ]
    with (pack/"SCENARIO_MATRIX.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["scenarioId","depth","durationOrStart","route","objective","iterations"]);w.writerows(scenarios)
    write(pack/"SOURCE_MANIFEST.json",json.dumps({"required":["docs/mechanics/GAMEPLAY_LOOP_CANON.md","src/data/gameplay-loop.json","src/data/haven.json","src/data/dungeon-mechanics.json","src/components/ExpeditionTracker.tsx"]},indent=2))
    write(pack/"RESULT_SCHEMA.json",json.dumps(generic_result_schema("Expedition Extraction"),indent=2))
    write(pack/"REPORT_TEMPLATE.md","# Expedition and Extraction Report\n\n## Scenario outcomes\n## Watch participation\n## Pressure behavior\n## Supply and rest curve\n## Cargo and casualty decisions\n## Profitability\n## Rules questions\n## Recommended changes\n")
    write(pack/"compile_results.py",compile_script());(pack/"results").mkdir()


def create_haven_pack():
    pack=PACK_ROOT/"03-haven-economy-social"
    shutil.rmtree(pack,ignore_errors=True); (pack/"agents").mkdir(parents=True)
    write(pack/"README_FIRST.md",base_readme("Haven Economy and Social Pack","appraisal, provenance, contracts, sponsors, banking, smuggling, labor, trafficking, sex-work institutions, magical substances, brewing, and faction standing","haven"))
    write(pack/"CURSOR_ORCHESTRATOR_PROMPT.md",f'''# Orchestrator Prompt

Simulate complete Haven resolution turns. Keep consensual adult sex work distinct from coercion and trafficking. Treat slavery, debt bondage, and trafficking as systems with victims, resistance, law, reputation, and rescue consequences—not decorative price tables.

Run each market scenario with all institutional agents. Track gross value, taxes, sponsor share, wages, repair, storage, debt, bribes, legal risk, reputation, and player choice. Search for infinite profit, appraisal loops, consequence-free crime, or markets that make extraction irrelevant.

Run at least 20 price/contract seeds and 5 narrative resolutions per scenario.

Governing rule: {DESIGN_RULE}
''')
    agents={
      "expedition-quartermaster":"Represents players selling cargo and paying real expedition costs. Refuses to ignore wages, losses, or reserve capital.",
      "artifact-appraiser":"Applies provenance, condition, demand, and urgency multipliers and records uncertainty.",
      "goblin-banker":"Tests lending, reminting, assay, shaved coin detection, collateral, and compounding debt without assuming every goblin is knowingly corrupt.",
      "guild-sponsor":"Tests sponsor support and shares, including whether one sponsor option is always correct.",
      "haven-magistrate":"Applies taxes, licenses, quarantine, seizure, criminal law, and due process.",
      "smuggler":"Tests contraband routes, bribes, laundering, and risk-adjusted profit.",
      "labor-organizer":"Tests wages, porter conditions, debt bondage, emancipation, strike, and reputation consequences.",
      "anti-trafficking-investigator":"Tests rescue, evidence, prosecution, victim agency, and whether trafficking can be gamed as consequence-free commerce.",
      "pleasure-house-operator":"Tests consensual adult hospitality, information, patronage, worker protection, and blackmail without conflating it with trafficking.",
      "brewer-alchemist":"Tests brewing, magical substances, dependence, withdrawal, licensing, and consumable profit.",
      "faction-broker":"Tracks reputation changes and access across Haven institutions.",
      "market-auditor":"Independently recomputes every transaction and identifies arbitrage or missing costs."
    }
    for aid,desc in agents.items():
        write(pack/"agents"/f"{aid}.md",f"# Agent: {aid.replace('-',' ').title()}\n\n{desc}\n\nWrite one result JSON per scenario. Cite exact formulas and record both economic and narrative consequences.\n")
    write(pack/"AGENT_ROSTER.md","# Agent Roster\n\n"+"\n".join(f"- `agents/{a}.md`" for a in agents))
    scenarios=[
      ["HAV-APPRAISAL","Documented damaged rare artifact","patient auction","test sale formula and information failure"],
      ["HAV-SPONSOR","Three expedition profiles","all sponsor types","compare net return and risk"],
      ["HAV-COIN","Mixed shaved and counterfeit coin batch","Iron Ledger Houses","test detection and reminting"],
      ["HAV-SUBSTANCE","Quickglass/Redwake/Ghostwine trade","licensed and black markets","test dependence and profit"],
      ["HAV-BREWING","Small brewery expansion","Makers and Lantern districts","test production and demand"],
      ["HAV-SMUGGLE","Contraband artifact","undercity route","test risk-adjusted return"],
      ["HAV-LABOR","Porter debt contract","labor market","test coercion, resistance, rescue, law"],
      ["HAV-TRAFFICKING","Captured sentient persons","inspection and claims","test safeguards and consequences"],
      ["HAV-PLEASURE","Consensual adult pleasure house","information and patronage","test agency and blackmail systems"],
      ["HAV-MARKET-SHOCK","Large Tier II material influx","whole Haven","test price collapse and next-descent incentives"],
    ]
    with (pack/"SCENARIO_MATRIX.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(["scenarioId","subject","venue","focus"]);w.writerows(scenarios)
    write(pack/"SOURCE_MANIFEST.json",json.dumps({"required":["docs/mechanics/GAMEPLAY_LOOP_CANON.md","src/data/haven.json","src/data/reputation.js","data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json","data/crafting/Decennium_Descent_Crafting_Bible_v4.json"]},indent=2))
    write(pack/"RESULT_SCHEMA.json",json.dumps(generic_result_schema("Haven Economy"),indent=2))
    write(pack/"REPORT_TEMPLATE.md","# Haven Economy and Social Report\n\n## Transaction math\n## Sponsor comparison\n## Market exploits\n## Legal and faction consequences\n## Labor and trafficking safeguards\n## Brewing and substance findings\n## Recommended changes\n")
    write(pack/"compile_results.py",compile_script());(pack/"results").mkdir()


def create_seasonal_pack():
    pack=PACK_ROOT/"04-seasonal-decennial-persistence"
    shutil.rmtree(pack,ignore_errors=True);(pack/"agents").mkdir(parents=True)
    write(pack/"README_FIRST.md",base_readme("Seasonal and Decennial Persistence Pack","end-of-Opening records, ten-year change, Haven persistence, map value, economic shocks, heirs, institutions, and repeat-campaign incentives","seasonal"))
    write(pack/"CURSOR_ORCHESTRATOR_PROMPT.md",f'''# Orchestrator Prompt

Simulate at least three consecutive Openings separated by ten years. Use the same Cycle Record as the sole basis for persistent changes. Do not expose Director-only truth in public records.

For each Opening:

1. Run a representative expedition outcome supplied by the scenario.
2. Create the full Cycle Record.
3. Apply one change each to Geography, Ecology, Economy, Politics, and Resonance.
4. Advance characters, institutions, heirs, debts, and Haven conditions ten years.
5. Start the next Opening and measure whether prior accomplishments matter without making exploration trivial.
6. Record contradictions, runaway wealth, irrelevant maps, or persistence that invalidates replenishment.

Run 10 three-Cycle campaigns and 3 five-Cycle stress campaigns.

Governing rule: {DESIGN_RULE}
''')
    agents={
      "cycle-director":"Applies replenishment and hidden consequences consistently while preserving public uncertainty.",
      "campaign-chronicler":"Maintains the Cycle Record and checks that every later change has an earlier cause.",
      "haven-council":"Models permanent civic institutions, district damage, growth, law, and political memory.",
      "market-historian":"Models scarcity, gluts, artifact monopolies, and the ten-year effect of prior extraction.",
      "expedition-dynasty":"Models surviving characters, retirement, heirs, apprentices, property, and reputation.",
      "new-player-company":"Models a new group entering a world changed by prior campaigns without inheriting unbeatable advantages.",
      "map-and-route-auditor":"Tests how much old maps help after replenishment and whether secured-route principles remain valuable.",
      "canon-boundary-auditor":"Ensures public records never confirm unknown tiers, Marquis truth, claimant succession, or crystal path."
    }
    for aid,desc in agents.items():write(pack/"agents"/f"{aid}.md",f"# Agent: {aid.replace('-',' ').title()}\n\n{desc}\n\nWrite one result JSON per campaign seed with exact Cycle-to-Cycle changes.\n")
    write(pack/"AGENT_ROSTER.md","# Agent Roster\n\n"+"\n".join(f"- `agents/{a}.md`" for a in agents))
    scenarios=[
      ["SEA-HAVEN-BOOM","Profitable Haven route becomes institutionalized","test persistence without solved dungeon"],
      ["SEA-MARKET-GLUT","One material floods surface markets","test next-Cycle demand and crafting"],
      ["SEA-FAILED-DEPTH","Famous Tier IV expedition disappears","test rumor, politics, and route abandonment"],
      ["SEA-FACTION-WAR","Two sponsors contest provenance and district control","test political persistence"],
      ["SEA-DYNASTY","Veterans retire and heirs lead next Opening","test legacy rewards"],
      ["SEA-HAVEN-DAMAGE","Haven district is damaged during the Opening","test civic recovery over ten years"],
    ]
    with (pack/"SCENARIO_MATRIX.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(["scenarioId","premise","focus"]);w.writerows(scenarios)
    write(pack/"SOURCE_MANIFEST.json",json.dumps({"required":["docs/mechanics/GAMEPLAY_LOOP_CANON.md","src/data/haven.json","src/data/dungeon-mechanics.json","CANON_MANIFEST.json","docs/director-only/continuity/"]},indent=2))
    write(pack/"RESULT_SCHEMA.json",json.dumps(generic_result_schema("Seasonal Persistence"),indent=2))
    write(pack/"REPORT_TEMPLATE.md","# Seasonal and Decennial Report\n\n## Cycle summaries\n## Persistence that mattered\n## Replenishment that restored uncertainty\n## Economic and political trajectories\n## New-player accessibility\n## Canon-boundary findings\n## Recommended changes\n")
    write(pack/"compile_results.py",compile_script());(pack/"results").mkdir()


def create_usability_pack():
    pack=PACK_ROOT/"05-readability-speed-onboarding"
    shutil.rmtree(pack,ignore_errors=True);(pack/"agents/users").mkdir(parents=True)
    write(pack/"README_FIRST.md",base_readme("Readability, Speed, and Onboarding Pack","first-session comprehension, lookup burden, turn speed, terminology, accessibility, and comparison to the governing design rule","usability"))
    write(pack/"CURSOR_ORCHESTRATOR_PROMPT.md",f'''# Orchestrator Prompt

Give each user agent only the public Gameplay Loop Bible, the relevant character sheet, and the scenario handout. Do not explain rules unless the scenario tells the facilitator to answer a question.

Measure:

- Time or decision steps to create an Expedition.
- Number of rule lookups per Watch and combat turn.
- Misread terms.
- Invalid actions attempted.
- Time to understand Pressure, Load, Extraction Class, retreat, and Haven settlement.
- Whether a player can state the full gameplay loop after play.

Run each profile through the Quickstart scenario twice: first without coaching, then after one rules summary. Separate writing problems from mathematical balance problems.

Governing rule: {DESIGN_RULE}
''')
    users={
      "new-ttrpg-player":"Has never played a tabletop RPG. Needs concrete verbs, visible choices, and minimal assumed terminology.",
      "casual-5e-player":"Knows action, bonus action, reaction, AC, and d20 checks. May import assumptions that are not written.",
      "pathfinder-2e-player":"Expects explicit traits, degrees of success, encounter math, and tactical precision. May overcomplicate a simpler rule.",
      "mmo-player":"Understands cooldowns, roles, rotations, and aggro but not freeform adjudication.",
      "narrative-player":"Prioritizes character intention and fiction; avoids heavy optimization and notices rules that interrupt story flow.",
      "rules-lawyer":"Cross-references exact wording and searches for contradictions, undefined timing, and stacking exploits.",
      "logistics-gamer":"Enjoys cargo, supply, routes, and economy; tests whether the loop offers real planning rather than bookkeeping for its own sake.",
      "low-working-memory-player":"Needs short references, consistent terminology, and low state-tracking burden. Flags accessibility barriers without being treated as less capable."
    }
    for aid,desc in users.items():write(pack/"agents/users"/f"{aid}.md",f"# User Agent: {aid.replace('-',' ').title()}\n\n{desc}\n\nDo not pretend to understand an undefined term. Record the exact sentence that caused confusion and the minimum wording change that would fix it.\n")
    write(pack/"AGENT_ROSTER.md","# Agent Roster\n\n"+"\n".join(f"- `agents/users/{a}.md`" for a in users)+"\n- Facilitator\n- Timing observer\n- Accessibility observer\n")
    write(pack/"agents/facilitator.md","# Facilitator\n\nRun the scenario exactly. Answer questions only by pointing to a rule; do not paraphrase on the first run. On the second run, provide the one-page quick reference.\n")
    write(pack/"agents/timing-observer.md","# Timing Observer\n\nCount decision steps, lookups, invalid actions, and repeated questions. Estimate whether each round and Watch resolution meets the speed target.\n")
    write(pack/"agents/accessibility-observer.md","# Accessibility Observer\n\nReview terminology, visual hierarchy, table density, cognitive load, and whether state can be externalized through the companion.\n")
    scenarios=[
      ["USE-CHARGEN","Create a level 1 character and explain its recurring combat decision"],
      ["USE-PREP","Build a six-person expedition objective, abort conditions, Supply, and cargo reserve"],
      ["USE-WATCH","Resolve three Watches including one Pressure complication"],
      ["USE-COMBAT","Run a Standard cargo-defense encounter"],
      ["USE-RETREAT","Use the three-success Retreat procedure"],
      ["USE-EXTRACT","Prioritize cargo and resolve one failed Extraction Test"],
      ["USE-HAVEN","Appraise, sell, pay sponsor, recover, and choose next objective"],
      ["USE-RECALL","Explain the complete gameplay loop without looking"],
    ]
    with (pack/"SCENARIO_MATRIX.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(["scenarioId","task"]);w.writerows(scenarios)
    write(pack/"SOURCE_MANIFEST.json",json.dumps({"required":["books/player/Decennium_Descent_Gameplay_Loop_Bible_v1.docx","docs/mechanics/GAMEPLAY_LOOP_CANON.md","src/components/ExpeditionTracker.tsx","books/player/Decennium_Descent_Player_Rulebook_v6.docx"]},indent=2))
    write(pack/"RESULT_SCHEMA.json",json.dumps(generic_result_schema("Usability"),indent=2))
    write(pack/"REPORT_TEMPLATE.md","# Readability and Speed Report\n\n## First-run comprehension\n## Second-run improvement\n## Lookup burden\n## Turn and Watch speed\n## Terminology problems\n## Accessibility findings\n## Minimum wording/UI changes\n")
    write(pack/"compile_results.py",compile_script());(pack/"results").mkdir()


def zip_pack(pack: Path, filename: str):
    target=OUTPUT_ROOT/filename
    if target.exists(): target.unlink()
    with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED) as z:
        for path in sorted(pack.rglob('*')):
            if path.is_file(): z.write(path,path.relative_to(pack.parent))
    return target


def main():
    shutil.rmtree(PACK_ROOT,ignore_errors=True); PACK_ROOT.mkdir(parents=True)
    create_combat_pack();create_expedition_pack();create_haven_pack();create_seasonal_pack();create_usability_pack()
    outputs=[]
    outputs.append(zip_pack(PACK_ROOT/"01-combat-class-balance","DD_V7_Cursor_01_Combat_Class_Balance.zip"))
    outputs.append(zip_pack(PACK_ROOT/"02-expedition-extraction","DD_V7_Cursor_02_Expedition_Extraction.zip"))
    outputs.append(zip_pack(PACK_ROOT/"03-haven-economy-social","DD_V7_Cursor_03_Haven_Economy_Social.zip"))
    outputs.append(zip_pack(PACK_ROOT/"04-seasonal-decennial-persistence","DD_V7_Cursor_04_Seasonal_Decennial.zip"))
    outputs.append(zip_pack(PACK_ROOT/"05-readability-speed-onboarding","DD_V7_Cursor_05_Readability_Speed.zip"))
    for p in outputs: print(p)

if __name__=="__main__":main()
