"""Replace Incomplete prestige feat stubs with draft entries grounded in prestige lore."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATS = ROOT / "src" / "data" / "feats.js"
LORE = ROOT / "src/data/prestige-lorebook.json"

DRAFT_META = {
    "draft": True,
    "source": "Draft — pending author review",
}

# prestige path -> feat names (from add_prestige_feat_stubs.py + lorebook)
PRESTIGE_REFS: dict[str, list[str]] = {}
def norm(s: str) -> str:
    return s.replace("\u2019", "'").replace("\u2018", "'")


for p in json.loads(LORE.read_text(encoding="utf-8")):
    req = p.get("requirements", "")
    m = re.search(r"Feats:\s*(.+?)\s*-\s*Skills:", req)
    if not m:
        continue
    for f in re.split(r",\s*", m.group(1).strip()):
        PRESTIGE_REFS.setdefault(norm(f.strip()), []).append(p["name"])

DRAFTS: dict[str, dict] = {
    "Anatomy Lore": {
        "description": "You have studied the weak joints, organs, and pressure points of giants, ogres, and other colossal foes common to Aethel's wilds.",
        "prerequisite": "Intelligence 13+, proficiency in Knowledge (Monstrous Humanoids) or Survival",
        "effect": "As a bonus action, you can identify one weak point on a Large or larger creature you can see. Your next attack against that creature deals +50% damage if it hits, or you gain advantage on the attack if the target is Huge or larger.",
        "type": "Skill",
    },
    "Arcane Adaptation": {
        "description": "Your magic bends to mirror what strikes you, letting you reshape your defenses after every reflected blow.",
        "prerequisite": "Spellcasting ability, Intelligence 13+",
        "effect": "When you successfully reflect or copy a spell or supernatural ability, you gain resistance to that damage type until the end of your next turn. Once per short rest, you may treat a copied effect as if you had always known it for 2 rounds.",
        "type": "Magic",
    },
    "Arcane Calculus": {
        "description": "You solve combat like an equation—measuring intervals, vectors, and the precise moment a spell must land.",
        "prerequisite": "Intelligence 15+, proficiency in Arcana",
        "effect": "You gain +2 to initiative while concentrating on a spell. Once per short rest, you may store one prepared spell's timing: cast it on a later turn without using an action, as if you had readied it mathematically.",
        "type": "Magic",
    },
    "Arcane Momentum": {
        "description": "Each sword stroke feeds your spellcraft. In Aethel's battlefields, steel and sigil are one rhythm.",
        "prerequisite": "Power Attack or Combat Casting, spellcasting ability",
        "effect": "When you hit with a melee weapon attack, gain 1 Momentum stack (max 3). Spend 1 stack to reduce the casting time of your next spell by one step, or spend all stacks to add +10% force damage per stack to a spell you cast before the end of your turn.",
        "type": "Magic",
    },
    "Beast Lore": {
        "description": "Tracks, calls, and temperaments— you read the wild the way scholars read ledgers.",
        "prerequisite": "Wisdom 13+, proficiency in Survival",
        "effect": "You have advantage on Animal Handling and Survival checks involving beasts. You can identify a beast's diet, temperament, and combat habits with a successful Survival check, granting allies +2 to hit that creature for 1 minute.",
        "type": "Skill",
    },
    "Blood Ritual": {
        "description": "Under the moon's gaze you bind flesh to curse through rites older than the cities of Aethel.",
        "prerequisite": "Constitution 13+, level 4+",
        "effect": "Once per long rest, as part of a 10-minute ritual using your blood, you gain temporary hit points equal to twice your level and advantage on the next saving throw against curse or disease effects. Required for many lycanthropic oaths.",
        "type": "Magic",
    },
    "Combat Engineering": {
        "description": "Walls, choke points, and kill-zones—you treat battlefields as structures waiting to be built or broken.",
        "prerequisite": "Intelligence 13+, proficiency in Engineering",
        "effect": "You can construct field fortifications, barricades, or emplaced cover in half the normal time. You gain +2 to Engineering checks involving siege devices, bridges, and structural weak points.",
        "type": "Skill",
    },
    "Companion Training": {
        "description": "Your beasts do not merely follow—they fight as extensions of your will.",
        "prerequisite": "Animal Companion feat or proficiency in Animal Handling",
        "effect": "Beast companions you command gain +2 to attack and damage rolls. You can command a companion to attack, dash, or help as a bonus action.",
        "type": "General",
    },
    "Conjure Flora": {
        "description": "Seeds answer your call, rooting as guardians, lashing as spears, blooming as verdict.",
        "prerequisite": "Spellcasting ability, proficiency in Nature",
        "effect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+.",
        "type": "Magic",
    },
    "Core Infusion": {
        "description": "You drive elemental or arcane cores into steel and stone until the metal remembers how to burn, freeze, or sing.",
        "prerequisite": "Proficiency in Craft (Blacksmith), spellcasting ability or Engineering",
        "effect": "When you finish a long rest, you may infuse one weapon or armor you crafted with a minor property (e.g., +1 fire damage, +1 AC, or resistance to one energy type) for 24 hours. Relic-tier work requires a forge and rare materials.",
        "type": "Magic",
    },
    "Curse Channeling": {
        "description": "Doom flows through your blade like ink through water—every cut writes a sentence the target cannot unread.",
        "prerequisite": "Spellcasting ability or proficiency in Arcana, level 6+",
        "effect": "When you hit a creature with a weapon attack, you can apply a Hex Mark. Marked creatures take +1d6 necrotic damage the next time they are hit before the start of your next turn. You can maintain one mark at a time; at level 10+, two.",
        "type": "Magic",
    },
    "Curse Weaving": {
        "description": "You knot malice into syllables, letting debuffs compound like threads pulled tight.",
        "prerequisite": "Spellcasting ability, Charisma 13+",
        "effect": "When you cast a spell that forces a saving throw, you may weave a curse: on a failed save, the target suffers an additional escalating debuff each round (–1 to attacks, then –1 to saves, then disadvantage on concentration) until they succeed on a save at the end of their turn.",
        "type": "Magic",
    },
    "Cursebound Flesh": {
        "description": "The moon's bite runs in your veins. Your body has learned to endure what would break mortal flesh.",
        "prerequisite": "Constitution 13+, level 6+",
        "effect": "While transformed or under a lycanthropic curse, you have resistance to nonmagical slashing damage and reduce damage from silver weapons by half. You have advantage on saves to resist involuntary transformation.",
        "type": "General",
    },
    "Dark Affinity": {
        "description": "Shadow clings to you willingly. The night recognizes its own.",
        "prerequisite": "Charisma 13+",
        "effect": "You have resistance to necrotic damage, darkvision out to 60 feet (or +30 feet if you already have it), and advantage on saving throws against charm effects from undead creatures.",
        "type": "Magic",
    },
    "Dark Binding": {
        "description": "You and your cursed weapon share one hunger. Neither leaves the other's grasp easily.",
        "prerequisite": "Curse Channeling or level 8+",
        "effect": "You bind to one cursed weapon over a blood ritual (1 hour). While bound, the weapon cannot be disarmed against your will and deals an additional 1d4 necrotic damage on hit. If the weapon is destroyed, you take 2d10 psychic damage and cannot rebind until you complete a new ritual.",
        "type": "Magic",
    },
    "Dark Fortitude": {
        "description": "Grave-cold and poison have tried to claim you. They learned your name and backed away.",
        "prerequisite": "Constitution 15+",
        "effect": "You have advantage on saving throws against poison and disease. Your hit point maximum increases by 2 per character level. When you take necrotic damage, you can use your reaction to reduce that instance by half (once per short rest).",
        "type": "General",
    },
    "Eldritch Combat": {
        "description": "Your strikes carry whispers from beyond the veil—steel and sigil in a single motion.",
        "prerequisite": "Spellcasting ability, proficiency with martial weapons",
        "effect": "When you take the Attack action, you can cast a cantrip or 1st-level spell with a range of touch or self as part of the same action without provoking opportunity attacks. The spell must target the same creature you hit or yourself.",
        "type": "Combat",
    },
    "Eldritch Echo": {
        "description": "Your patron's voice returns through you, repeating power that was never meant for mortal throats.",
        "prerequisite": "Forbidden Pact or spellcasting ability, level 3+",
        "effect": "You gain Eldritch Blast as a known cantrip if you do not already have it; it scales with your level. Once per short rest, when a creature within 60 feet casts a spell, you may echo a simplified version of that spell on your next turn (DM adjudicates equivalent level, usually half the original).",
        "type": "Magic",
    },
    "Favored Enemy (Dragon)": {
        "description": "You have studied scaled tyrants—their breath, their pride, the tell before the roar.",
        "prerequisite": "Proficiency in Survival, level 5+",
        "effect": "You deal +2 damage to dragons and dragonkin. You have advantage on Survival and Lore checks to identify dragon ancestry, breath type, and lair habits. You cannot be frightened by a dragon's presence for more than 1 round.",
        "type": "Combat",
    },
    "Forbidden Pact": {
        "description": "You signed in blood and silence. Something old signed back.",
        "prerequisite": "Charisma 13+, level 3+",
        "effect": "You forge a soul pact with an entity beyond the known planes. You gain Eldritch Blast and one pact sigil (e.g., shadowstep, hex bonus, or energy resistance) chosen with your DM. Once per encounter, you may spend hit points equal to twice the spell's level instead of a spell slot.",
        "type": "Magic",
    },
    "Frenzied Rage": {
        "description": "Rage becomes avalanche—each kill feeds the next swing until the world is only red and thunder.",
        "prerequisite": "Constitution 15+, Berserker feat or class rage ability",
        "effect": "While raging, you deal +3 damage with melee weapon attacks (instead of +2). When you reduce a creature to 0 hit points with a melee attack, you can make one additional melee attack or extend your rage duration by 1 round. Once per rage, you can charge through enemies, dazing those you pass.",
        "type": "Combat",
    },
    "Giant Slayer": {
        "description": "Colossi fall when the small learn where the giant bleeds.",
        "prerequisite": "Precision Strike or level 8+",
        "effect": "You deal +20% damage against Large or larger creatures. Once per short rest, when you hit a Huge or larger creature with a melee attack, you can cripple its movement, reducing speed by half until the end of its next turn.",
        "type": "Combat",
    },
    "Hardened Grip": {
        "description": "Forge heat and battle strain forged your hands into vices. Your weapon stays until you decide otherwise.",
        "prerequisite": "Strength 15+",
        "effect": "You cannot be disarmed while conscious. You gain +2 to Craft (Blacksmith) checks and can wield weapons one size category larger without the normal penalty.",
        "type": "Combat",
    },
    "Hemocraft": {
        "description": "Blood is ink, blade is quill—you write power in crimson script across flesh and air.",
        "prerequisite": "Intelligence or Charisma 13+",
        "effect": "When you score a critical hit with a melee attack, the target gains a Bleed stack (1d4 ongoing damage at the start of its turns). You can consume one Bleed stack from a creature within 30 feet to heal 1d8 hit points or deal 1d8 necrotic damage to that creature.",
        "type": "Magic",
    },
    "Life Drinker": {
        "description": "Every wound you open is a cup. You drink and stand taller.",
        "prerequisite": "Dark Affinity or Hemocraft",
        "effect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points, you regain hit points equal to your character level.",
        "type": "Combat",
    },
    "Lifeleech": {
        "description": "Your magic does not merely harm—it siphons the vigor that death has not yet claimed.",
        "prerequisite": "Spellcasting ability",
        "effect": "When you deal necrotic damage with a spell, you regain hit points equal to half the necrotic damage dealt. When a hostile creature dies within 30 feet, you absorb a soul spark, gaining 1 soul charge (max 3). Soul charges can power Soul Cage abilities.",
        "type": "Magic",
    },
    "Lightning Affinity": {
        "description": "Storm-blood runs quiet in you until the sky asks it to speak.",
        "prerequisite": "Spellcasting ability or proficiency in Nature",
        "effect": "You have resistance to lightning damage. Your lightning spells deal +1 damage per die. You have advantage on saving throws against electrical and paralyzing effects.",
        "type": "Magic",
    },
    "Master Smithing": {
        "description": "Kings queue for your steel. You measure temper, fold, and spell-work in the same breath.",
        "prerequisite": "Proficiency in Craft (Blacksmith), Intelligence 13+",
        "effect": "You can craft masterwork weapons and armor and work toward relic-tier items with appropriate materials. Armor you craft reduces armor check penalty by 1. Weapons you craft gain +1 to damage rolls.",
        "type": "Skill",
    },
    "Mimicry": {
        "description": "See it once, steal its thunder—your mirror learns faster than pride allows.",
        "prerequisite": "Spellcasting ability, Intelligence 15+",
        "effect": "When you witness a spell or monster ability used against you or within 30 feet, you can mimic a simplified version once before your next short rest. The mimicked effect lasts up to 2 rounds and is usually at half potency (DM adjudicates).",
        "type": "Magic",
    },
    "Necrotic Affinity": {
        "description": "Death's chill is an old friend. You channel it without flinching.",
        "prerequisite": "Proficiency in Religion or level 8+",
        "effect": "You have resistance to necrotic damage. Once per turn when you hit with a melee attack, you can deal an additional 1d6 necrotic damage.",
        "type": "Magic",
    },
    "Precision Strike": {
        "description": "One opening. One breath. One strike where the giant's armor forgot to cover bone.",
        "prerequisite": "Dexterity 13+ or Weapon Focus",
        "effect": "Once per turn when you make a weapon attack, you may take –2 to the attack roll to deal +50% damage on a hit. Against a restrained, grappled, or identified weak point (via Anatomy Lore), you may instead treat a hit as a critical hit once per short rest.",
        "type": "Combat",
    },
    "Primal Instinct": {
        "description": "The beast inside listens before the mind does. You trust that older voice.",
        "prerequisite": "Wisdom 13+, proficiency in Survival",
        "effect": "You have advantage on Wisdom (Perception) checks relying on hearing or smell. You cannot be surprised while conscious. You can track creatures across difficult terrain without penalty.",
        "type": "General",
    },
    "Quickened Thought": {
        "description": "Your mind outpaces the tick of the clock—ideas arrive finished, not forming.",
        "prerequisite": "Intelligence 15+, Arcane Calculus or Temporal Theory",
        "effect": "You gain +2 to initiative. Once per short rest, you may cast a spell of 2nd level or lower as a bonus action.",
        "type": "Magic",
    },
    "Siege Savant": {
        "description": "You read walls like books—knowing which stone sighs before it falls.",
        "prerequisite": "Proficiency in Engineering",
        "effect": "You deal +20% damage to constructs, fortifications, and siege engines. Explosives you deploy have +5 feet radius. You can identify structural weak points with a successful Engineering check, granting allies advantage on the next attack against that structure or construct.",
        "type": "Skill",
    },
    "Slayer\u2019s Resolve": {
        "description": "You have buried friends under dragonfire. Their memory is armor the wyrms cannot melt.",
        "prerequisite": "Favored Enemy (Dragon) or level 8+",
        "effect": "You are immune to the Frightful Presence of dragons. Allies within 30 feet of you have advantage on saving throws against fear effects while you are conscious. You gain +2 AC against attacks made by dragons.",
        "type": "Combat",
    },
    "Soul Cage": {
        "description": "You trap the departing in black crystal—voices pressed flat until you need their scream.",
        "prerequisite": "Lifeleech or spellcasting ability, level 8+",
        "effect": "When a hostile creature dies within 30 feet, you may bind its soul to a black crystal, storing up to 3 soul charges. Spend 1 charge to shield an ally for 2d8 temporary HP, or spend 2 charges to fire an Agony Lance (3d8 necrotic, save for half, and the target has disadvantage on the next healing it receives).",
        "type": "Magic",
    },
    "Spell Reflection": {
        "description": "What was sent returns wearing your sigil—mirrors do not forgive.",
        "prerequisite": "Spellcasting ability, level 8+",
        "effect": "Once per short rest, when you are targeted by a single-target spell, you may reflect it back at the caster as an immediate reaction (they make saving throws as if they had cast it on themselves). When you take spell damage, the attacker takes psychic damage equal to half the damage you received (once per round).",
        "type": "Magic",
    },
    "Stormcaller": {
        "description": "You whistle up weather like a shepherd calls dogs—clouds come hungry.",
        "prerequisite": "Spellcasting ability, proficiency in Nature or Spellcraft",
        "effect": "You can create a 15-foot Static Field as an action (once per short rest): creatures entering or starting their turn there take 1d6 lightning damage. Once per short rest, you may Stormstep up to 30 feet to a target you can see, dealing 1d8 thunder damage to adjacent creatures.",
        "type": "Magic",
    },
    "Temporal Theory": {
        "description": "Time is not a river—it is a ledger. You have learned to borrow from tomorrow and repay in fatigue.",
        "prerequisite": "Intelligence 15+, proficiency in Arcana, level 8+",
        "effect": "At the end of your turn, you may bank one unused action (move, object interaction, or bonus action if available), storing up to 2 banked actions. Spend banked actions on later turns. After spending 2 banked actions in one encounter, you gain one level of fatigue when combat ends.",
        "type": "Magic",
    },
    "Trapcasting": {
        "description": "Roots, thorns, and spore-mines—you sow violence that waits patiently to bloom.",
        "prerequisite": "Conjure Flora or Verdant Bond",
        "effect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot AoE, 2d6 damage, type chosen at conjuring).",
        "type": "Magic",
    },
    "Trapsetter": {
        "description": "Tripwire, caltrop, and charge—the ground remembers your name and bites when asked.",
        "prerequisite": "Proficiency in Engineering or Disable Device",
        "effect": "You can set a mechanical trap as a bonus action (once per short rest per trap type). Traps may stun, burn, or slow on a failed save. You gain advantage on checks to spot hidden traps and tunnels within 30 feet.",
        "type": "Skill",
    },
    "Undying Flesh": {
        "description": "Death tried to keep you. Your flesh negotiated a reprieve.",
        "prerequisite": "Constitution 15+, Necrotic Affinity or Dark Fortitude",
        "effect": "You have resistance to necrotic and poison damage. Once per long rest, when you are reduced to 0 hit points but not killed outright, you rise at 1 hit point at the start of your next turn with temporary necrotic bonuses (+2 damage for 1 minute).",
        "type": "General",
    },
    "Verdant Bond": {
        "description": "The green speaks to you in sap and silence. You answer with growth.",
        "prerequisite": "Proficiency in Nature, spellcasting ability",
        "effect": "You can communicate simple ideas to plants within 60 feet. While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells. You have advantage on Nature checks in wilderness terrain.",
        "type": "Magic",
    },
    "Voltyros Pact": {
        "description": "You bargained with the Plane of Storms itself—Voltyros marks you with copper taste and crown-light.",
        "prerequisite": "Stormcaller or Lightning Affinity, level 6+",
        "effect": "Your lightning spells chain to one additional target within 15 feet for half damage. While you remain stationary for a full round, you gain resistance to all damage until the start of your next turn and +2 to spell damage (Eye of the Tempest). Once per long rest, you may call a stormform burst: 30-foot line of lightning for 4d6 damage.",
        "type": "Magic",
    },
    "Wounding Magic": {
        "description": "Your spells leave wounds that resist closure—pain that outlasts the casting.",
        "prerequisite": "Spellcasting ability",
        "effect": "When you deal damage with a spell, you may leave an Agony wound: the target takes 1d4 necrotic damage at the start of each of its turns for 3 rounds (save ends). Wounded targets have disadvantage on Constitution saves to regain hit points and on saves against resurrection effects.",
        "type": "Magic",
    },
}


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def build_entry(name: str) -> str:
    d = DRAFTS[name]
    paths = PRESTIGE_REFS.get(norm(name), ["prestige paths"])
    path_note = ", ".join(paths)
    desc = (
        f"{d['description']} "
        f"(Prestige prerequisite: {path_note}. "
        f"Definition not in available canon sources; draft for review.)"
    )
    lines = [
        "  {",
        f'    "id": "{slug(name)}",',
        f'    "name": "{name}",',
        f'    "description": "{desc}",',
        f'    "prerequisite": "{d["prerequisite"]}",',
        f'    "effect": "{d["effect"]}",',
        f'    "type": "{d["type"]}",',
        f'    "draft": true,',
        f'    "source": "Draft — pending author review"',
        "  }",
    ]
    return "\n".join(lines)


def main() -> None:
    text = FEATS.read_text(encoding="utf-8")
    start = text.find('  {\n    "id": "anatomy_lore"')
    end = text.rfind("\n];\nexport default feats;")
    if start < 0 or end < 0:
        raise SystemExit("Could not locate stub block in feats.js")

    entries = [build_entry(name) for name in DRAFTS]
    new_block = ",\n".join(entries)
    updated = text[:start] + new_block + text[end:]
    FEATS.write_text(updated, encoding="utf-8")
    print(f"filled={len(DRAFTS)}")
    for n in DRAFTS:
        print(f"  {n}")


if __name__ == "__main__":
    main()
