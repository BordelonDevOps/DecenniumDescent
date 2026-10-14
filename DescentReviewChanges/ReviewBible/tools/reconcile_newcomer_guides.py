"""Repair onboarding summaries using the existing candidate rule authorities.

Preserve all prior guide bytes. This makes no new mechanical decision and does
not certify the companion, human balance, or whole-game flow.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
AUTHORITY = ['CHARACTER_CREATION_PLAYTEST.md', 'CHARACTER_FOUNDATION_TABLES.md',
             'CLASS_PLAYTEST_RULES.md', 'SPELL_INTEGRATION_RULES.md',
             'COMBAT_ACTION_PLAYTEST.md', 'CORE_RESOLUTION_PLAYTEST.md',
             'HEALING_DEATH_PLAYTEST.md', 'STRAIN_PLAYTEST.md', 'classes/oracle.md',
             'ANCESTRY_BACKGROUND_PLAYTEST.md', 'EQUIPMENT_STARTING_PACKAGES.md']

PLAYER = '''# Newcomer player guide — Decennium Descent

Use this guide for the current authored playtest candidate. Keep your class cards beside your character sheet. The [main start page](../../../../START_HERE.md) identifies the active rules and remaining development work.

## Make your first character

Start at level 1 with one Base class. **Base, Arch and Hero are stages of that class.** Its schedule tells you when to select features and paths. The [Base-class guide](../mechanics/BASE_CLASSES_START_HERE.md) and [class library](../mechanics/CLASS_PLAYTEST_INDEX.md) lead to all 17 classes; [Paladin paths](../mechanics/PALADIN_OATHS_AND_OATHBREAKERS.md) contain the ten Oath/Oathbreaker pairs.

Follow [character creation](../mechanics/CHARACTER_CREATION_PLAYTEST.md) in order:

1. Generate and assign your six ability scores using one permitted method. Apply your ancestry's actual increases once.
2. Choose an [ancestry, required variant and background](../mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md). Record each trait's full procedure, skills, languages and tools.
3. Take your first class's training and starting HP from the [foundation tables](../mechanics/CHARACTER_FOUNDATION_TABLES.md). At level 1, HP is the maximum face of its Hit Die plus CON modifier, minimum 1; proficiency bonus is +2.
4. Follow the class's actual level-1 schedule. Some classes use scheduled selections; Druid, Oracle and Paladin have specific schedules. Feature names in an older sheet add no extra grants.
5. Record each class resource and its current and maximum amounts. For ordinary spells, record the casting class, legal rank, and known/prepared or spellbook choices. Use operational spell cards; an unfinished catalog entry supplies no usable effect.
6. Take the class and background [equipment packages](../mechanics/EQUIPMENT_STARTING_PACKAGES.md), or the permitted rolled starting wealth instead of all package equipment and package money. Record purchases, coins, containers, ammunition and actual carrying load.
7. Write your AC, Speed, attack bonuses, damage, saves and class DCs. Keep the source card beside any special number. Choose one legal AC formula.

The Director helps identify any unresolved choice before play. A saved companion character does not by itself establish that every option has current rules.

## What happens on your turn

Combat uses initiative and roughly six-second rounds. Your normal turn permits:

| Resource | What you can do |
|---|---|
| Movement | Move up to your available Speed, paying terrain costs. You can divide ordinary movement around your actions. |
| One Action | Attack, use an Action-time spell or feature, Dash, Dodge, Help, or take another legal Action. |
| One Bonus Action | Use it when a rule you possess grants a specific use. |
| One free object interaction | Perform one ordinary interaction; another ordinary interaction or an Action-time activation needs an Action. |
| Reaction | Use a legal trigger when the resource is available. It refreshes at your regular turn's start. |

A Reaction does not refresh at the round boundary or on an extra turn. All sources share a limit of **one extra full Action per creature per round**. An extra Action supplies no extra Bonus Action or Reaction and cannot generate another extra Action. Read the [combat guide](../mechanics/COMBAT_ACTION_PLAYTEST.md) for surprise, movement, Help, Ready and exact timing.

Before rolling, say what you intend and identify the roll. Attacks meet AC to hit; ordinary saves meet their DC to succeed. Task checks use degrees of success. These are separate procedures in [core resolution](../mechanics/CORE_RESOLUTION_PLAYTEST.md). Add proficiency once when it applies.

## Magic and class resources

Weave spells spend **Resonance Points (RP)**. Use your casting class's rank and the current Core V2 cost table: ranks 0–9 cost **0, 2, 3, 5, 7, 10, 13, 17, 21, 26 RP**; Grand costs 32. Access, preparation, components, costs and targets must all be legal. Having enough RP grants no extra rank or spell.

**Dissonance** records casting strain; **Refrain** records repetition. Repeating the same ordinary spell adds strain even for cantrips. Casting a different spell resets the repetition counter, while accumulated Dissonance remains. Idle or weapon turns do not automatically clear Refrain. Generic Overcast options are outside this candidate configuration; use only an actual feature's stated permissions.

Keep the [Resonance reference](RESONANCE_CHEATSHEET.md) nearby for the exact cost, strain and recovery procedure. Class resources such as Crescendo, Ki, Conviction and Blood Gauge keep their own rules.

**Oracle Revelations use Revelation Charges (RC).** In the current Oracle candidate, a beneficial completed short rest restores 1 spent RC and a beneficial completed long rest restores RC to maximum. Actual Prophecy and combat recovery obey the engine's shared cap and qualifying-event rules. The [Oracle guide](../mechanics/classes/oracle.md) supplies the RC schedule, Mystery and Curse. Revelations do not become ordinary Weave spells. Any Weave casting earned through another class keeps that class's separate access and strain rules.

## Rest and recovery

A short rest takes one uninterrupted hour; a long rest takes an eight-hour Rest Watch. There are at most **two beneficial short rests between beneficial long rests**, and **one beneficial long rest per 24 elapsed hours**. The [Strain guide](../mechanics/STRAIN_PLAYTEST.md) explains safety, interruption, Rest Debt and these limits. Supplies, travel and work still use real time.

Retune at an eligible short-rest completion restores the amount on the Resonance reference and clears Dissonance. A beneficial long rest restores the RP pool and clears Dissonance. Other resources recover only by their own rules. Rest, healing and leveling are different events; gaining a level does not refill spent resources or current HP.

## Help someone at zero HP

Tell the Director when damage could drop a creature to zero, cause a Wound or kill it. Resolve the full damage procedure before assuming it is merely unconscious. Instant Death and fatal Wounds can prevent death saves.

A surviving dying character at zero HP makes a death save at each **regular** turn's start: natural 20 restores 1 HP; natural 1 adds two failures; other 10+ results add a success and 9 or less a failure. Three successes establish Stable; three failures kill. Specific recovery blockers or features can change the result as described in [healing and death](../mechanics/HEALING_DEATH_PLAYTEST.md).

Use an Action and a DC 10 Wisdom (Medicine) check to stabilize a living dying creature, or an Action and one healer's-kit use for automatic stabilization. A Stable creature remains at zero HP and unconscious, without death saves. Record its 1d4-hour recovery deadline. Further damage reaching normal HP can resume dying. Temporary HP does not stabilize or wake it. Ordinary healing cannot revive a dead creature; Wounds require their own treatment.

## Bring to the table

Keep your sheet, selected cards, dice and a way to track current HP, temporary HP, Wounds, resources, concentration, conditions and spent uses. State what you are trying to do, then resolve the matching procedure with the Director. Share decisions and spotlight with the other players.

Before the first session, agree on the objective, party jobs, content boundaries, retreat plan and which unfinished choices are excluded. The Director provides the expedition brief. Full expedition/Haven integration and final whole-game review are still underway. The companion can assist with tracking; use the current cards and guides when an older display disagrees.

The previous newcomer text, including its historical advice and examples, is preserved in the [onboarding archive](../../../../docs/audit/2026-10-08/full-game/onboarding-before-reconciliation/). This revision updates summaries of existing candidate rules; it creates no new class, spell or recovery permission.
'''

DIRECTOR = '''# Newcomer Director guide — Decennium Descent

Run the current authored playtest candidate from the [main start page](../../../../START_HERE.md). This guide connects existing procedures for a first session. Final whole-game flow, human balance and full companion parity remain open.

## Prepare a session

1. Agree on the session's purpose, tone, content boundaries, player agency and how to pause play. State the expedition objective, known hazards, retreat conditions and the consequences the characters could reasonably know.
2. Check each sheet against [character creation](../mechanics/CHARACTER_CREATION_PLAYTEST.md), its [class schedule](../mechanics/CLASS_PLAYTEST_INDEX.md), [ancestry/background](../mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md), and [equipment packages](../mechanics/EQUIPMENT_STARTING_PACKAGES.md). Arch and Hero are later class stages. A later multiclass entry grants its actual entry package rather than a second full starting package.
3. Resolve starting choices explicitly. Use operational spell and feat options, full item profiles and actual known/prepared choices. A named source entry, proficiency or possession of a book grants no unspecified effect or automatic access.
4. Prepare the encounter's terrain, light, exits, objectives and complete creature procedures. Check actual attacks, saves, damage, defenses and movement before using a creature. An app placeholder or imported name is insufficient. Keep restricted creature, formula and setting material within its established audience.
5. Record current HP, temporary HP, Wounds, resources, concentration, recharge and uses. For the expedition, record actual elapsed time, inventory, custody and the applicable brief. The [expedition/Haven source cases](../../../../docs/audit/2026-10-08/full-game/EXPEDITION_HAVEN_FLOW_SOURCE_AUDIT.md) identify open integration questions; older quickstart defaults do not settle those conflicts.

Use the [player guide](NEWCOMER_PLAYER_GUIDE.md) and [Resonance reference](RESONANCE_CHEATSHEET.md) for the briefing. Characters may be tracked on paper. Do not require a particular app workflow before the tabletop procedures are usable.

## Teach the current magic configuration

Use Core V2 class RP tables and rank prices, with the candidate Dissonance layer. A rank-3 spell costs **5 RP before applicable modifiers**. A rank-2 spell costs 3. Older rank-times-two pricing and generic Overcast menus remain historical alternatives.

Declare the casting class first. It must independently have access, the required class level, known/prepared status and components. A character has one merged RP pool under the [foundation formula](../mechanics/CHARACTER_CREATION_PLAYTEST.md), and one shared Dissonance/Refrain history. Other named resources retain their own rules. Changing class or casting a different spell does not erase accumulated strain.

Oracle Revelations use RC. The current [Oracle engine](../mechanics/classes/oracle.md) expressly chooses 1 RC from a beneficial short rest and full RC from a beneficial long rest. Its capacities are 3 at Oracle levels 1–2, 4 at 3–5, 5 at 6–8, 6 at 9–10 and 7 at 11+. Combat-generated refunds share at most one recovered RC per round and require their real qualifying event. Preserve the printed exceptions and encounter-start procedure; staged encounters grant no recovery.

The [Strain guide](../mechanics/STRAIN_PLAYTEST.md) caps beneficial rests: two short rests between beneficial long rests, and one long rest per 24 elapsed hours. Track completion times. An additional safe Rest Watch can clear eligible Rest Debt without granting another resource refill. Rest does not automatically remove Wounds or resolve supply and security questions.

## Resolve a scene

Establish awareness, then roll initiative as described in [combat and timing](../mechanics/COMBAT_ACTION_PLAYTEST.md). Players choose player/player ties; you resolve ties involving NPCs. Keep the ordered slots and regular-turn markers.

For each declared action, check actual acquisition, prerequisites, target, range, line of effect, action resource and cost. An illegal activation spends nothing. A legal paid attempt that misses or is resisted still spends its cost. Resolve the exact card and record its limits.

At a regular turn's start, follow the combat guide's ordered processing: expire start-ending effects, refresh Reaction and tick eligible clocks, process due recovery, make a required death save, then resolve other start effects before voluntary choices. Extra turns do not refresh these regular-turn clocks by themselves. Changing initiative never restarts an existing duration.

Use [core resolution](../mechanics/CORE_RESOLUTION_PLAYTEST.md) to distinguish attacks, ordinary saves and task degrees. Use the [condition reference](../mechanics/CONDITIONS_PLAYTEST.md) and a feature's actual ending procedure. Conditions, damage, concealment and control permissions are separate effects; a descriptive name supplies none of them automatically.

## Damage, Wounds and dying

Apply the complete [healing/death integration](../mechanics/HEALING_DEATH_PLAYTEST.md) and core damage procedure. Keep the incoming resolved damage, temporary HP absorbed, uncapped post-temporary-HP damage and actual normal HP lost distinct.

Instant Death checks whether **post-temporary-HP damage minus pre-hit HP is at least effective maximum HP** when reduced to zero. For example, with 3 HP and maximum 10, a post-temporary-HP packet of 12 has excess 9 and does not meet this threshold; a packet of 13 has excess 10 and does. These examples isolate that threshold; explicit survival features and the rest of the injury procedure still apply.

When Instant Death does not apply, the actual positive-to-zero, half-maximum-damage or Maiming triggers require one Wound save for that damage event. Use the existing save, Injury and Critical procedures; a new Wound does not penalize its own creating save. The next failed Wound save after already having three Wounds is fatal.

A living dying character rolls a death save at a regular turn's start. Stabilization clears counters and establishes its recorded 1d4-hour recovery deadline. Ordinary healing, temporary HP, direct state recovery and resurrection are distinct procedures. Use the precise source when a special feature changes one branch; do not apply skipped death branches again after a replacement.

## Keep the expedition and records coherent

Use one elapsed-time record for travel, work, rests, treatment and recovery. Do not spend the same active hours twice. Record actual items, components, charges and custody. A move, sale, rest, repair or change of owner does not reset a use budget unless its procedure expressly allows that reset.

For crafting, consult the [recipe review index](../mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md). A reviewed recipe effect does not prove ingredient availability. Preserve the boundary between player information and Director verification of exact stock. The remaining advanced recipes and the full expedition/Haven loop retain their review gates.

Opening campaigns use milestones under [advancement](../mechanics/CHARACTER_CREATION_PLAYTEST.md). Process one gained class level at a time; maintain the chronological level record and current spent resources. A companion XP estimate is not an extra award rule.

Record each unresolved table question with the actual source/card, state before the event, roll or choice, ruling and resulting state. Report a contradiction instead of silently combining incompatible versions. After play, gather both rules problems and player experience; numerical scripts do not establish fun or human balance.

Historical app instructions, prior pool examples and previous newcomer wording remain in the [onboarding archive](../../../../docs/audit/2026-10-08/full-game/onboarding-before-reconciliation/). This revision summarizes existing candidate decisions. The final joint flow review remains ahead of GitHub delivery; cosmology review remains after the verified push.
'''

CHEAT = '''# Resonance and Revelation — current playtest reference

Use [shared class rules](../mechanics/CLASS_PLAYTEST_RULES.md), [spell integration](../mechanics/SPELL_INTEGRATION_RULES.md), and the [character foundation](../mechanics/CHARACTER_CREATION_PLAYTEST.md). This sheet summarizes their active candidate configuration. Individual cards keep their exact prerequisites, costs and exceptions.

## Before casting

Declare the casting class. Check its own class level, school/rank access and known/prepared or spellbook requirements. Select an operational spell, then check components, target, range, action availability and payable cost. Sufficient RP does not unlock access. A class feature with the same name remains a separate feature.

## Base RP prices

| Rank | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | Grand |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RP | 0 | 2 | 3 | 5 | 7 | 10 | 13 | 17 | 21 | 26 | 32 |

Apply the current Dissonance surcharge and only actual card-authorized modifiers. Generic Overcast options are excluded from this configuration. A named class feature such as Overchannel follows its own card.

## Dissonance and Refrain

`Limit = max(4, 2 + total-character PB + max(0, casting-class ability modifier))`.

Evaluate the current strain before a ranked cast:

| Current Dissonance | Surcharge | Ordinary ranked casting |
|---|---:|---|
| Below Limit | 0 RP | Permitted if otherwise legal |
| Limit through Limit+2 | +1 RP | Permitted if otherwise legal |
| Limit+3 through Limit+5 | +2 RP | Permitted if otherwise legal |
| Limit+6 or higher | +3 RP for an expressly permitted exception | Ordinary rank-1-or-higher casting is unavailable |

A cast then adds base Dissonance: 0 for rank 0, 1 for ranks 1–5, and 2 for ranks 6–9. Immediately repeating the same named spell adds Refrain of +1, then +2, then +3 maximum on subsequent repeats; repeated cantrips also count. Apply the class's exact cadence reductions or vents.

Casting a different named spell resets the repetition counter but leaves accumulated Dissonance. Idle or weapon turns preserve Refrain unless an actual class rule clears it. Switching casting class clears neither history. Printed class techniques pay their printed costs and generate no automatic spell strain unless expressly covered by the casting rules.

Lich/Necromancer have an explicit ranked-casting exception through Fracture. They still need access and RP; direct Traumatic Casting uses their printed procedure and the pre-cast strain state. This exception does not reintroduce the excluded generic Overcast menu.

## Recovery

| Event | Candidate procedure |
|---|---|
| Regular turn without a spell or magical class ability | Lose 1 Dissonance. |
| Action spent Grounding without casting | Lose PB Dissonance instead of the idle-turn reduction. |
| Beneficial completed short rest | Retune once: recover `max(0, round-half-up(maximum RP / 4) + primary RP class casting modifier)`, capped at maximum; clear Dissonance. |
| Beneficial completed long rest | Restore RP to maximum and clear Dissonance. |
| Optional ten-minute meditation, once per day | Recover the primary RP class's positive casting modifier in RP; reduce Dissonance by PB plus that positive modifier. |

The [rest rules](../mechanics/STRAIN_PLAYTEST.md) require one hour for a short rest, eight hours for a long rest, at most two beneficial short rests between beneficial long rests and one beneficial long rest per 24 elapsed hours. Interruption and campaign requirements still apply. Ending an encounter alone does not clear Dissonance. Do not infer a separate class-resource recovery from Retune.

## Multiclass characters

Use one merged RP pool: the selected primary class's full pool plus `ceil(secondary pool / 4)` from at most one secondary class. Select contributors by the foundation's tier, class-level, pool and acquisition-order rules; do not choose a different primary per cast. Oracle, Soldier and Warrior contribute no RP pool. Each casting class still satisfies its own repertoire and rank gate. Keep one character-wide Dissonance/Refrain history and one ordinary concentration slot, with only explicit exceptions.

## Oracle Revelations

The [Oracle engine](../mechanics/classes/oracle.md) uses RC for Revelations: capacities 3 at Oracle levels 1–2, 4 at 3–5, 5 at 6–8, 6 at 9–10 and 7 at 11+. A beneficial short rest restores 1 spent RC; a beneficial long rest restores RC to maximum. Combat-generated refunds share at most 1 RC per round and require genuine qualifying events. Follow the engine for its encounter-start floor and limited special refills.

Revelations use their printed RC costs and do not generate ordinary Weave Dissonance or clear another class's existing strain/Refrain. Increasing a resource maximum through advancement does not refill current resources. The [previous reference](../../../../docs/audit/2026-10-08/full-game/onboarding-before-reconciliation/DescentReviewChanges/ReviewBible/docs/playtest/RESONANCE_CHEATSHEET.md) preserves the earlier alternative pricing and Overcast text.
'''

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p):
    return p.relative_to(G).as_posix()

def main():
    receipt = A / 'ONBOARDING_RULE_SUMMARY_RECONCILIATION.json'
    assert not receipt.exists(), 'Preserve completed revision; do not overwrite its receipt'
    protected = {rel(R / 'docs/mechanics' / p): sha(R / 'docs/mechanics' / p) for p in AUTHORITY}
    texts = {'NEWCOMER_PLAYER_GUIDE.md': PLAYER, 'NEWCOMER_DIRECTOR_GUIDE.md': DIRECTOR,
             'RESONANCE_CHEATSHEET.md': CHEAT}
    before, after = {}, {}
    archive = A / 'onboarding-before-reconciliation'
    for name in texts:
        p = R / 'docs/playtest' / name
        dest = archive / rel(p)
        assert p.exists() and not dest.exists()
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
        assert p.read_bytes() == dest.read_bytes()
        before[rel(p)] = {'sha256': sha(p), 'archive': rel(dest)}
    for name, content in texts.items():
        p = R / 'docs/playtest' / name
        p.write_text(content, encoding='utf-8')
        after[rel(p)] = sha(p)
    links = []
    for name in texts:
        p = R / 'docs/playtest' / name
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            q = (p.parent / target.split('#', 1)[0]).resolve()
            assert q.is_relative_to(G) and q.exists(), (name, target)
            links.append({'from': rel(p), 'target': target, 'exists': True})
    assert all(sha(G / p) == h for p, h in protected.items())
    # Preserve the already submitted conference and prepared spell snapshots.
    unchanged = {}
    for name in ['ADVANCED_CRAFT_JOINT_SUBMISSION.json', 'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json']:
        d = json.loads((A / name).read_text(encoding='utf-8'))
        assert all(sha(G / p) == h for p, h in d['currentFileHashes'].items())
        unchanged[name] = len(d['currentFileHashes'])
    data = {'status': 'editorial reconciliation of existing candidate authorities; joint whole-game flow still open',
            'atUtc': datetime.now(timezone.utc).isoformat(), 'before': before, 'after': after,
            'protectedRuleAuthorities': protected, 'ruleAuthoritiesUnchanged': True,
            'preservedConferencePayloads': unchanged, 'localLinks': links,
            'corrections': [
                'Core V2 rank prices replace historical rank-times-two teaching',
                'Generic Overcast menu excluded per shared candidate configuration',
                'Oracle current RC caps and explicit rest recovery replace historical source/companion alternatives',
                'Regular-own-turn Reaction refresh replaces a generic one-per-round shortcut',
                'Refrain reset distinguished from accumulated Dissonance reduction',
                'Beneficial-rest limits, completed time and primary-class Retune formula made explicit',
                'Instant Death excess-damage threshold and Wound/death sequence linked correctly',
                'Current class acquisition and advancement replace old pool examples and feature strings',
                'Historical simulation recommendations and unverified app instructions retained in archive, outside current player guidance'],
            'newMechanics': False, 'newApprovals': 0, 'sourceInformationDeleted': 0,
            'runtimeChangedOrVerified': False, 'cosmologyReviewed': False,
            'futureReview': 'Include these current onboarding summaries in the next refreshed spell handoff and final joint whole-game flow review'}
    receipt.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'guidesUpdated': len(texts), 'priorGuidesPreserved': len(before),
                      'unchangedRuleAuthorities': len(protected), 'verifiedLocalLinks': len(links),
                      'conferencePayloadsUnchanged': unchanged, 'newMechanics': False}))

if __name__ == '__main__':
    main()
