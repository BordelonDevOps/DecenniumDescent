"""Author the twelve source-conferenced cards, without selecting/promoting them."""
import hashlib
import json
from pathlib import Path

GAME = Path(r"C:\Github\DecenniumDescent")
ROOT = GAME / "DescentReviewChanges/ReviewBible"
AUDIT = GAME / "docs/audit/2026-10-08/full-game"
catalog = json.loads((ROOT / "data/public/spell_playtests/catalog.json").read_text(encoding="utf-8-sig"))
sources = {s["id"]: s for s in catalog["spells"]}
source_review = "docs/audit/2026-10-08/full-game/GPT_CONJURATION_CANTRIP_SOURCE_CONFERENCE.md"
one_round = "If applied in initiative, expires at the caster's first future regular-start marker after application; preserve that virtual marker through initiative changes, departure or death. If applied outside initiative, expires 6 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts."
one_minute = "If applied in initiative, expires at the caster's tenth future regular-start marker after application; preserve that virtual source-start phase through initiative changes, departure or death. If applied outside initiative, expires 60 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts."
common = " Known/prepared access, class level, components, line of effect, cast costs, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. Total cover blocks direct targeting and the originating spell's line of effect. No automatic level scaling."
replacement = " A successful new application owns its own endpoint; stale expiration or consumption of an older application cannot remove its replacement. A countered new cast creates no replacement."
cards = []

def card(id, range_feet, targets, duration, concentration, components, resolution, effect, limitations, notes):
    source = sources[id]
    cards.append({
        "id": id, "activation": "Action", "rangeFeet": range_feet,
        "targets": targets, "duration": duration, "concentration": concentration,
        "components": components, "resolution": resolution, "effect": effect,
        "scaling": "None.", "limitations": limitations + common,
        "designNotes": notes,
        "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
        "sourceCoreEntries": source["source"]["coreEntries"],
        "sourcePlacements": source["source"]["original"]["placements"],
        "classAccessEvidence": source["classAccess"],
        "comparativeHistoricalCoreEntries": source["source"].get("possibleHistoricalAliases", []),
        "sourceReview": [source_review], "reviewEvidence": []
    })

card("dust-gust", 5,
     "Choose one mode: one discrete unattended, unsecured object you perceive, no larger than Small and no heavier than 10 pounds; or up to 10 pounds of existing loose nonmagical sand or dust contained within one 5-foot square. The selected object/material must be within range and line of effect.",
     "Instantaneous", False, ["V", "S"],
     "Automatic for an eligible object or selected loose material; no attack or save.",
     "Object mode pushes the object up to 5 feet directly away from you. Dust/sand mode scatters the selected loose material up to 5 feet away from you. Stop movement before solid terrain or illegal occupancy; ordinary loose material may settle on an accessible supporting surface.",
     "Worn, held, attached, restrained, locked, packed, structural or otherwise secured material is ineligible. Ordinary floor, table or shelf support alone is not security. The spell creates no material and grants no excavation, blindness, damage, disarm, collision damage or generated resource. Ordinary physical consequences, such as exposing a surface or removing support and beginning Falling, still follow. Moving some dust does not automatically erase tracks, remove a hazard or neutralize its independent effect.",
     "PRESERVED: Action, 5-foot range, V/S, instantaneous, object push or 5-foot sand/dust scatter. NEW: Small/10-pound ceiling, exact two modes, existing loose material, 5-foot displacement and custody/obstruction limits.")

card("lodestone-pull", 5,
     "One discrete unattended, unsecured object you perceive within range, no larger than Small and no heavier than 10 pounds, whose primary physical material is metal.",
     "Instantaneous", False, ["V", "S", "F"],
     "Automatic for an eligible object; no attack or save.",
     "Pull the object up to 5 feet directly toward you, stopping before your occupied space, solid terrain or illegal occupancy.",
     "Worn, held, attached, locked, anchored or otherwise secured objects are ineligible. Ordinary support alone is not security. A metal fitting on a primarily nonmetal object does not qualify the entire object. This gives one pull, no disarm, remote inventory access, sustained tether, repeated movement, collision damage or levitation; unsupported objects obey ordinary Falling. Taking the object into a hand requires ordinary legal object interaction.",
     "PRESERVED: Action, 5-foot range and single 5-foot metal-object pull; M/F uses the existing class focus. CONFLICT RULING: the singular movement controls; Core's concentration-up-to-1-minute metadata and Ward tag do not grant an ongoing or repeatable effect. NEW: instantaneous/no concentration, Small/10-pound ceiling, primary-metal and custody/stopping limits. Original metadata is preserved.")

card("minor-elemental-ward", 30,
     "One willing creature you can perceive within range, including yourself.",
     one_minute + " Ends earlier when consumed or concentration ends.", True, ["V", "S", "F"],
     "Automatic application after legal casting. The benefit modifies the target's next qualifying save; it creates no new save.",
     "The target gains +1 to its next saving throw against an effect whose resolution can deal acid, cold, fire, lightning or thunder damage. Consume the benefit after that qualifying save regardless of success/failure, damage prevented by another defense, or a stronger flat saving-throw bonus superseding this +1.",
     "Only the five listed damage types qualify; force, necrotic, radiant, poison, psychic, physical and Corruption damage do not qualify by themselves. Mixed effects qualify if their resolution can deal a listed type. A source with an elemental name but no such damage does not qualify. No immunity or resistance to damage/status is granted. One pending Minor Elemental Ward per target across all casters; a new application replaces the older one and releases only that older casting's concentration dependency. Each casting owns only its own concentration dependency." + replacement,
     "PRESERVED: Action, 30 feet, concentration up to 1 minute, +1 to next elemental-damage save, M/F as class focus. NEW: willing recipient, exact five-type eligibility, consumption, all-caster replacement and exact endpoint; deliberately distinct from the eight-type Protection from Energy list.")

card("flicker-flame", 30,
     "One fixed, unoccupied point you can perceive within range and line of effect.",
     "10 minutes (600 seconds) after application, preserving that absolute deadline through initiative changes.", False, ["V", "S"],
     "Automatic after legal casting; no attack or save.",
     "Create a harmless, nonphysical floating flame shedding dim light in a 10-foot radius about the fixed point. It can dance cosmetically within about 1 foot of that point; this does not move its illumination origin or provide controlled tactical movement.",
     "One Flicker Flame per caster; a successful new application ends that caster's older Flicker Flame. It does not attach to or follow a creature/object and produces no heat, damage, ignition, fuel, physical object, sunlight trait or tracking signal. Overlap follows ordinary illumination without adding radii or upgrading dim light to bright merely by stacking this spell. Opaque barriers block its ordinary light. It does not automatically dispel magical darkness, reveal Invisible creatures or end Hidden independently of normal sight rules." + replacement,
     "PRESERVED: Action, 30 feet, V/S, dim dancing light for 10 minutes. NEW: no concentration, fixed point, 10-foot dim radius, one-light cap, cosmetic motion and ordinary illumination boundaries.")

card("stone-skin-sliver", 30,
     "One willing creature you can perceive within range, including yourself.",
     one_round + " Ends earlier if concentration ends.", True, ["V", "S"],
     "Automatic after legal casting; no attack or save.",
     "The target gains +1 AC for the duration. Apply the strongest applicable same-stat flat bonus; this spell's bonus does not add to another flat AC bonus.",
     "This is a magical AC bonus, not stone anatomy, armor, equipment, weight, damage resistance, hardness or a body transformation. Separate casters may maintain independent nonstacking Slivers with their own endpoints and concentration. Ending one does not end another. No all-caster replacement rule is imposed. A caster still cannot maintain multiple ordinary concentration spells; starting this spell ends their incompatible earlier concentration even if the new cast is countered.",
     "PRESERVED: Action, 30 feet, V/S, +1 AC for 1 round; concentration is explicit in both effect summaries and remains required despite its omission from the Core duration field. NEW: willing target, exact source-start clock and independent nonstacking applications.")

card("resonance-kindle", 0,
     "Self only; the casting character's own RP pool.",
     "Instantaneous", False, ["V", "S"],
     "Automatic recovery only if this legal spell survives interruption and reaches resolution. Having no unused Kindle use makes the cast illegal before activation/payment.",
     "At the beginning of the legal cast, spend your one Kindle use before the Counterspell window. At resolution, restore 1 RP to yourself, capped by your actual RP maximum. One use per character across all class repertoires, copied access and historical aliases refreshes only upon an actual completed beneficial long rest under the shared recovery rules.",
     "A countered cast leaves the use spent and recovers 0 RP. A cast at maximum RP is legal, spends the use and restores 0 if still full at resolution. Repeated nonbeneficial rest attempts do not refresh it. It neither clears Dissonance/Refrain nor restores other resources, heals, grants a check, or targets an ally. Only casting this spell produces this recovery; casting another cantrip does not trigger it. Copied effects, duplicate access, form changes and proxies grant no extra uses or repeated resource recovery.",
     "PRESERVED: current catalog and V6 explicitly recover 1 RP after casting THIS cantrip, once per long rest. ALIAS RECONCILIATION: comparative Core Mana Kindle supports Action/V/S/instantaneous; its broader after-a-cantrip wording is not a repeatable trigger. Its historical 30-foot range remains evidence, while the operational range is Self. No exact-name Core block exists, and the comparative alias remains separately identified and preserved. NEW: character-wide use, begin-cast expenditure, beneficial-rest reset, cap and interruption handling.")

card("pebble-swarm", 5,
     "Every creature, including allies, in a 5-foot cone originating from your space in a chosen direction, with line of effect from that origin. On a standard 5-foot grid this bounded template is one adjacent 5-foot square you choose; it never includes your origin square or extends to a second square.",
     "Instantaneous", False, ["V", "S"],
     "Each affected creature makes a Dexterity save against your spell DC. Failure takes damage; success takes 0.",
     "Roll one shared 1d4 bludgeoning damage for the cast and apply that result to every creature that fails, using each creature's own applicable defenses. The conjured pebbles vanish after resolution.",
     "Total cover blocks an affected creature's line of effect. You cannot exclude an eligible ally in the cone. No spell attack, critical hit, ability modifier to damage, automatic object damage, persistent pebbles, ammunition or saleable/crafting material is supplied. Outside a square grid, use the same 5-foot-long cone with a maximum 5-foot-wide far end; agree its placement before saves rather than gaining a larger template by changing measurement systems.",
     "PRESERVED: Action, V/S, 1d4 bludgeoning and 5-foot cone. NEW: Dexterity-negates save, one shared damage roll, explicit creature/ally coverage, bounded one-square grid template and nonpersistent stones. Broader area-template rules remain a separate integration task.")

card("elemental-touch", 5,
     "One creature, or one unattended or willingly presented discrete object, within your body's actual normal touch reach. The 5-foot header is a normal-humanoid reference, not a grant of reach, a ranged touch or an override of actual anatomy.",
     "Damage is instantaneous. On a successful touch, the cosmetic mark lasts for the following one-minute clock: " + one_minute,
     False, ["V", "S"],
     "Against an unwilling creature, make a melee spell attack using the casting class's spellcasting ability + PB. A willing creature or eligible unattended/willingly presented object requires no attack roll. A missed attack produces neither damage nor mark.",
     "Choose acid, cold, fire, lightning or thunder when cast. A successful touch deals 1 flat damage of that type and leaves a harmless, visibly elemental mark on the touched target for 1 minute. A critical hit adds no damage dice and does not double the flat 1. Apply ordinary defenses; the mark appears even when the damage becomes 0.",
     "No ability modifier or automatic level scaling increases damage. Object damage requires an existing native track/rule that actually accepts this typed damage: reduce actual HP normally, or use an explicit native conversion if provided; never treat 1 damage as 1 Integrity stage or invent a conversion. The cosmetic mark is not the Marked condition, a tracker, beacon, extra damage, ignition, corrosion engine, parasite detector or another condition. It provides no magical information or extraordinary visibility through concealment; observers may see it normally. One mark from this caster on this target replaces that caster's prior Elemental Touch mark; marks from other casters remain separate." + replacement,
     "PRESERVED: Action, Touch, V/S, chosen-element 1 damage and a mark. NEW: melee spell attack against unwilling creatures, exact five types, object/native-track interface, 1-minute harmless mark, no concentration and per-caster/target replacement. rangeFeet=5 is a reference header; actual touch reach controls.")

card("mist-veil", 5,
     "One fixed 5-foot cube of legal space, placed with its origin point you perceive within 5 feet and line of effect. Mist occupies only space the originating effect can reach; it does not extend through total cover.",
     one_minute + " Ends earlier if concentration ends or an effect explicitly disperses this magical mist.",
     True, ["V", "S"],
     "Automatic creation after legal casting; no attack or save. Occupancy by a creature does not itself make the cube illegal.",
     "The cube is heavily obscured for ordinary vision. Sight through its obscuring mist follows COMBAT_ACTION_PLAYTEST.md. The mist blocks no line of effect, creature or object movement and grants no physical support.",
     "It neither erases known locations nor makes a creature automatically Hidden. Hide still requires its ordinary action, eligibility and resolution. A known location does not satisfy a separate creature-you-can-see requirement. Apply existing unseen-attacker/target and perception rules only when their actual conditions hold, with ordinary advantage/disadvantage combination; the mist adds no new modifier or duplicated Invisible benefit. Extraordinary senses apply only as their own rules permit. One Mist Veil per caster; a successful new application replaces the prior one, and starting its concentration already ends incompatible old concentration. Ordinary wind or heat does not automatically end this magical mist; an effect expressly capable of dispersing magical mist may do so. No recoverable water or material is created." + replacement,
     "PRESERVED: Action, 5-foot range, V/S and 5-foot cube of obscuring mist. CONFLICT RULING: concentration up to 1 minute supplies an ongoing procedure instead of the unusable Instantaneous cloud metadata. NEW: fixed cube/origin, heavy obscurement, one-caster cap, magical dispersal and explicit sight/Hide interface.")

card("phantom-key", 30,
     "One perceived nonmagical, key-operated mechanical lock within range and line of effect; conjure its key into your free hand. A free hand able to receive/use an ordinary key is required at creation.",
     one_minute + " The temporary key vanishes at the endpoint, wherever it then is.",
     False, ["V", "S"],
     "Automatic creation for an eligible lock. Actual insertion and operation require ordinary legal physical object interaction; spellcasting does not include remote opening or an extra interaction.",
     "The temporary key works as the correct mundane key for that exact lock, requiring no lockpicking check. It can be handed to another creature and used normally for the duration, including locking or unlocking repeatedly if the actual mechanism and available interactions allow. It cannot operate another lock. Its vanishing does not retroactively undo the physical lock's resulting state.",
     "One Phantom Key per caster; a successful new application ends that caster's prior key. Ordinary hand, custody, carrying, access and object-interaction rules apply; a second interaction or a mechanism requiring an Action still costs that Action. It does not disable, detect or bypass traps, jams, barricades, combination/keyless locks or magical protections. A separable mundane physical mechanism on a magically warded lock can accept the key; the ward, including Arcane Lock, remains in force and requires its own permission or removal. A purely magical lock is ineligible. The key supplies no permanent key, harvestable/saleable material or automatic durable blueprint. Ordinary observations and deductions still work; no memory or inference is erased." + replacement,
     "PRESERVED: temporary key that WORKS on one nonmagical lock; Action/30 feet/V/S. NEW: key-operated mechanism, free-hand creation, finite 1-minute lifetime/no concentration, transferable custody, ordinary repeatable key use during that lifetime, one-key cap and trap/ward boundaries. The historical Instantaneous metadata is reconciled as creation followed by a finite temporary object. Thief Lockpick Mastery remains a separate +5 tool/check feature; the strong mundane-lock bypass is an explicit unresolved balance question, not silently rewritten into proficiency or advantage.")

card("resonance-mote", 30,
     "One willing creature you can perceive within range, including yourself.",
     one_minute + " Ends earlier when the next qualifying check consumes the Mote; its light ends with it.",
     False, ["V", "S"],
     "Automatic application. The target's next actual qualifying task check uses its existing source's ability/tool, DC and Core task-degree procedure, with this flat bonus subject to the strongest-bonus rule.",
     "A small, nonphysical mote follows within the recipient's space and sheds dim light in a 5-foot radius under ordinary illumination rules. Grant +1 to the recipient's next source-authorized task/ability/tool check explicitly concerned with manipulating, diagnosing, stabilizing, calibrating or otherwise directly interacting with Resonance/the Weave, or explicitly named a Resonance check by its source. Consume the Mote after that roll regardless of success/failure or a stronger flat bonus superseding its +1.",
     "This bridge does not create a check, permission, DC, hidden information or subsystem. A merely magical topic or spending RP does not qualify without the stated actual task. It does not modify spell attacks, saves, concentration checks, Counterspell, ordinary casting, RP costs, Dissonance or Refrain; old Burn/fizzle mechanics remain inactive. If no qualifying task occurs, the Mote simply expires. One pending Mote per target across all casters; a successful new application replaces the old benefit and light. It grants no physical object, heat, extra perception, tracking, sunlight or automatic revelation of Invisible/Hidden creatures; ordinary light/cover and observer deductions still apply." + replacement,
     "PRESERVED: Action/30 feet/V/S, floating light and +1 next Resonance check. NEW BRIDGE: exact source-authorized task interface without resurrecting legacy casting failures; 1-minute/consumption clock replaces unusable Instantaneous metadata, no concentration, willing recipient, 5-foot dim radius and all-caster replacement. No generic Resonance-check procedure was found in the bounded active-source search; task sources still own their actual permission/ability/DC/outcomes.")

card("faction-emblem", 30,
     "Choose one exact canonical factionId for which your current actual reputation is +1, +2 or +3. Choose a perceived nonliving surface, or a fixed point, within range and line of effect for its visible emblem.",
     "10 minutes (600 seconds) after application, preserving that absolute deadline through initiative changes.",
     False, ["V", "S"],
     "Verify the exact positive reputation gate before activation/payment. Missing, 0 or negative reputation is ineligible. Automatic display after a legal surviving cast; no attack or save.",
     "Create the faction's recognizable visible emblem, no larger than 1 foot across, as a nonphysical display at the selected point or on the selected surface. A surface-mounted emblem moves with that object; a free-standing emblem remains fixed. The display does not emit light unless a separate actual light source illuminates it; it is seen under ordinary vision rules. If no visual emblem is yet described for that faction, the Director may describe its ordinary recognized symbol without granting institutional authority.",
     "One Faction Emblem per caster; a successful new application ends that caster's prior emblem. Positive reputation is the source-authorized gate; Faction Seal's separate invocation-permission requirement is not imported. Later reputation changes do not retroactively end this valid application. The emblem grants no membership, rank, credentials, legal authority, persuasion bonus, protection, RP discount or mutable official-seal power. It is not harvestable/saleable matter or a permanent crafting symbol. Observers can draw ordinary social deductions from it; it neither guarantees belief nor erases memory or inference." + replacement,
     "PRESERVED: Action/30 feet/V/S and a symbol of a faction with positive reputation. NEW: exact canonical +1..+3 gate, 1-foot recognizable nonphysical symbol, fixed/surface placement and movement, 10-minute duration/no concentration, one-caster cap, later-standing and authority boundaries. Instantaneous metadata is reconciled as creation of a finite display.")

candidate = {
    "status": "LOCAL CANDIDATE — SOURCE-RECONCILED; exact manuscript review pending; NOT SELECTABLE",
    "scope": "Twelve remaining Conjuration cantrip identities; twelve placements, eleven exact-name Core blocks and one separately preserved comparative Mana Kindle block. No runtime/balance/whole-game approval.",
    "reviewEvidence": [source_review], "spells": cards
}
path = ROOT / "data/playtest/spell_drafts/candidate_conjuration_cantrips.json"
if path.exists():
    raise SystemExit(f"Refusing to overwrite existing candidate: {path}")
path.write_text(json.dumps(candidate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
digest = hashlib.sha256(path.read_bytes()).hexdigest()
packet = """# Twelve Conjuration cantrips — exact manuscript review

Here are the exact twelve authored cards following your source conference. Please review all card text against your conference and the current shared casting/sight/object/recovery rules. Approve or provide exact required textual repairs. Review manuscript playability and source reconciliation, not unimplemented runtime behavior or balance certification. Please keep the response under 15,000 characters.

Counts remain 120 reviewed / 728 unfinished until approval and promotion. All twelve retain only their actual seven class-access rows, rank 0, Dragoon minimum class 3 and the other six class 1. Twelve source placements, eleven exact-name Core blocks and the comparative Mana Kindle block are unchanged. The latter remains separate from exact-name sourceCoreEntries; no source deletion/rename. Full original evidence is in your preceding packet.

Explicit authored clarifications to check:
- Successful new application, not a countered attempt, replaces nonconcentration one-per-caster or one-per-target effects. Concentration still commits at begin-cast and ends incompatible old concentration before any counter.
- Kindle resets only after a BENEFICIAL completed long rest (one per 24 hours under current shared recovery), is illegal with no unused use, and consumes its use at legal cast start; full pool remains legal and may restore 0.
- Flicker cosmetic motion does not move the illumination origin; overlapping dim sources do not upgrade brightness merely through copies. Mote ends its light when consumed. Emblem is visible but not a light source.
- Pebble uses the approved one-adjacent-square 5-foot cone, plus the bounded 5-foot-long/5-foot-far-width off-grid description; total cover blocks targets and allies cannot be excluded.
- Touch's rangeFeet=5 is only the ordinary-humanoid header; actual normal touch reach controls. Native objects accept typed damage only through their actual damage rule/track, never an invented Integrity conversion. The harmless visible mark still appears when damage is prevented.
- Mist's chosen cube origin must be perceived/in-range/in-line-of-effect; no mist through total cover, creature occupancy allowed. Current heavy-obscurement/known-location/Hide/extraordinary-sense rules remain intact.
- Phantom Key works repeatedly during its finite duration using ordinary interactions, can be transferred, and vanishing does not re-lock/unlock the mechanism. Only a separable mundane lock mechanism can be operated beneath a remaining magical ward. Balance with Thief remains explicitly open.
- All one-round/one-minute effects use agreed fixed source-start/out-of-initiative clocks; independent Slivers and replacements own their individual endpoints.

Please explicitly confirm whether these twelve are suitable for promotion to the authored operational-playtest catalog after any exact repairs. Full game, runtime, balance and final GitHub delivery remain open.

## Exact candidate

"""
packet += f"Candidate byte SHA256: `{digest}`\n\n"
packet += "```json\n" + json.dumps(candidate, indent=2, ensure_ascii=False) + "\n```\n"
packet_path = AUDIT / "CODEX_CONJURATION_CANTRIP_EXACT_REVIEW.md"
packet_path.write_text(packet, encoding="utf-8")
submission = {"status": "prepared for exact manuscript review; not yet promoted", "ids": [c["id"] for c in cards], "candidatePath": str(path), "candidateSha256BeforeReview": digest, "packetPath": str(packet_path), "packetSha256": hashlib.sha256(packet_path.read_bytes()).hexdigest(), "operationalBefore": 120, "unfinishedBefore": 728}
(AUDIT / "CONJURATION_CANTRIP_EXACT_SUBMISSION.json").write_text(json.dumps(submission, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"candidateCards": len(cards), "candidateSha256": digest, "packetCharacters": len(packet), "sourcePlacements": sum(len(c['sourcePlacements']) for c in cards), "exactCoreBlocks": sum(len(c['sourceCoreEntries']) for c in cards), "comparativeCoreBlocks": sum(len(c['comparativeHistoricalCoreEntries']) for c in cards)}, indent=2))
