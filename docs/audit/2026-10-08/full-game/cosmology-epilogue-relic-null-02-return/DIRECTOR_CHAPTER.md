# Director Chapter — EPI-08–14 Relics, Seeds, and Residual Null (Revision 02)

## Scope and authority

This is the complete playable **candidate** for EPI-08 through EPI-14 after RNX-01–14. It is NEW provisional authorship where the preserved manuscripts left operation undefined. It is **not adopted** until the owner/Codex review accepts it. Original source paragraphs and explicit owner decisions remain authoritative; this chapter does not choose the campaign epoch, identify unresolved cosmological entities, promote pending spells/bestiary, or approve environment/consumable/later-arc drafts. The source heading **Dungeon Seeds after Infinite Yield** remains preserved as evidence; use in another campaign frame requires the already-declared alternate-staging record rather than asserting Infinite Yield occurred.

## Relics

### Shard Pendant of Xi (`RELIC-XI-PENDANT-1`)

**Status.** NEW PROVISIONAL AUTHORSHIP completing preserved source relic

**Physical.** `{"form": "black-silver pendant on 24-inch cord", "weightLb": 0.2, "wearing": "neck slot; one free hand only to don/remove; passive/active require worn", "durability": "special relic; ordinary loss/destruction is real; no automatic respawn"}`

**Acquisition.** `{"scene": "CH11 Shardpool Confluence — Crystal Bastion landing cell", "stock": 1, "procedure": "On the Crystal Bastion landing cell, the one Xi reliquary has two opposed pressure plates. Press both plates simultaneously with two hands or two creatures (one Action) to open it. No roll. Once opened the pendant can be taken with an Action.", "depletion": "Reliquary opens once; item never respawns.", "initialCharge": "NEW: the unique pendant is discovered with charge=1. First bonding changes bearer eligibility only and never changes charge."}`

**Bond.** `{"required": true, "eligibility": "any class", "procedure": "1 uninterrupted active hour wearing/handling the actual pendant; no roll; not a rest. Transfer or 10+ minutes separation from the item ends bond. A new bearer repeats the hour.", "cap": "This module creates no universal attunement-slot cap."}`

**passive.** `{"name": "Motive-Certainty Refusal", "rule": "A magical information effect cannot return an output that claims the bearer's actual motive, fundamental desire, or intended reason with absolute certainty. It may still return emotions, surface thoughts, alignment, observable behavior, probabilities, or other information within its real scope. If only the prohibited field is blocked, other legal fields remain.", "examples": [{"spell": "Scribe Destiny", "catalogId": "scribe-destiny", "status": "reviewed", "result": "Blocked when it would return the bearer's fundamental motive; other spell limits remain."}, {"spell": "Read Surface Thoughts", "catalogId": "read-surface-thoughts", "status": "reviewed", "result": "Not blocked merely for reading one current thought; its own text expressly denies complete motive reading."}, {"spell": "Divine Truth", "catalogId": "divine-truth", "status": "pending", "result": "No new ruling and no promotion. Pendant interaction remains unimplemented until that spell is reviewed."}]}`

**active.** `{"name": "Declare Contradiction", "uses": "1 charge; refreshes only when the bonded bearer completes a beneficial Long Rest while possessing the pendant. Transfer, rebonding, removal, destruction/recovery, or another person's rest never refreshes it.", "activation": "Action", "range": "60 ft; bearer must perceive the selected creature and know which ongoing spell record is being addressed.", "target": "One ongoing spell-effect record currently affecting one creature. A fixed zone/area with no individual target record is ineligible. A multi-target spell can lose one independently tracked target branch without ending other branches.", "consent": "During the Action the actual caster and selected affected target must each knowingly agree. Consent is a fiction-level no-action response, not compelled communication. Dead, absent, unreachable, mindless, or unwilling caster/target means consent cannot be completed.", "commit": "The Action is spent on declaration. The charge is spent only when both consents are valid; then the selected ongoing effect branch ends immediately.", "concentration": "No RP/slot/action/use refund. If the ended branch was the last remaining effect of a concentration spell, concentration ends normally; otherwise other branches remain.", "ongoingDamage": "A continuing spell-created target record is eligible only while it is still an ongoing spell effect with identifiable caster and target. Damage already resolved is never rewound.", "failure": "Invalid target or missing/declined consent spends the Action but not the charge.", "initialState": "Item-bound charge starts at 1 when first taken from its reliquary."}`

**transfer.** `Bond ends on transfer. Charge state belongs to item identity and transfers with it; no reset.`

**duplicate.** `One actual item. Copies/illusions cannot duplicate passive, charge, or identity.`

### Concord Spear Fragment (`RELIC-CONCORD-SPEAR-1`)

**Status.** NEW PROVISIONAL AUTHORSHIP completing preserved source relic

**Physical.** `{"form": "Proof-War spear fragment mounted on serviceable 6-ft haft", "weightLb": 3, "hands": "one hand normally; two hands for versatile damage", "baseWeapon": "Spear: 1d6 piercing, versatile 1d8, thrown 20/60. Relic explicitly adds Finesse and Heavy for its attuned user.", "properties": ["Finesse", "Heavy", "Thrown 20/60", "Versatile 1d8"], "small": "Actual Heavy rule applies: Small creatures have disadvantage on attack rolls with it."}`

**Acquisition.** `{"scene": "CH10 Crimson Accord Arena", "stock": 1, "procedure": "Resolve the staged duel by either side-victory or neutral accord. If party prevents both projections from being reduced to 0 and completes the Accord option, spear fragment rises from center plinth automatically. Otherwise it appears after the projection duel ends but is sealed for 1 hour; then it can be taken. One actual fragment.", "depletion": "No respawn."}`

**Bond.** `{"required": true, "eligibility": "Paladin or Soldier class level >=1", "procedure": "1 uninterrupted active hour drilling forms with actual spear; no roll; not a rest.", "proficiency": "Eligibility does not grant spear proficiency. Use actual class/ancestry/feat proficiency; an unproficient wielder omits proficiency bonus as normal.", "cap": "No universal attunement cap."}`

**hesitation.** `{"activation": "Bonus Action before one actual attack with this spear on the same turn", "effect": "Charge that one declared attack with radiant bonus damage equal to floor(character level/2), minimum 0.", "scope": "Melee or thrown spear attack. The attack must occur before turn end; if not, charge expires. A miss consumes the charge. No idle precharge, rewind, or carryover.", "crit": "Radiant bonus is a flat number and is not multiplied by a critical hit unless a future exact rule explicitly multiplies flat bonuses.", "thrown": "Thrown spear remains where the attack places it and must be physically recovered; no magical return.", "resource": "No RP, Conviction, Soldier engine, planar authority, or divine spellcasting is granted."}`

**loss.** `If lost/destroyed, no replacement is generated.`

**duplicate.** `No copied fragment has powers.`

### Mirror of Potential Silence (`RELIC-MIRROR-SILENCE-1`)

**Status.** NEW PROVISIONAL AUTHORSHIP completing preserved source relic

**Physical.** `{"form": "oval hand mirror, black glass, silver rim", "weightLb": 1.0, "hands": "one hand to activate/touch; can be carried or stowed", "attunement": "none"}`

**Acquisition.** `{"scene": "CH12 Omega Theatre", "stock": 1, "procedure": "Complete the theatre through a fictional-vow/neutral-prompt branch or resolve the Echo Doppelganger. Mirror rises from the stage trap together with exactly three silver reflection tabs. One mirror and three tabs total.", "depletion": "No second mirror from replay.", "reflectionTabs": {"count": 3, "identity": ["TAB-SILENCE-1", "TAB-SILENCE-2", "TAB-SILENCE-3"], "weightLbEach": 0.05, "custody": "Physical items; can be lost/transferred/destroyed; never respawn."}}`

**activation.** `{"activation": "Action; user touches mirror and speaks/signs/writes one fictional-character fear in a language the user can express. No real-player personal disclosure.", "beneficiary": "User only.", "pending": "Mirror shows a brief fictional image where the fear is untrue. The user gains advantage on their next Wisdom saving throw made within 24 hours. One pending benefit maximum; cannot activate again while pending.", "resolution": "On the qualifying Wisdom save, first resolve normal advantage/disadvantage cancellation and every legal reroll/replacement. If the final save outcome succeeds, pending benefit is consumed and mirror remains intact. If final outcome fails, pending benefit is consumed and mirror shatters after that save resolves.", "expiry": "Pending benefit expires after 24 elapsed hours unused; mirror remains intact.", "away": "If mirror is lost/destroyed before pending save, the pending benefit ends immediately."}`

**reformation.** `{"status": "NEW narrowed operational interpretation of source Sentinel discretion; one repair opportunity for this mirror identity.", "scene": "CH12-GLASS-MENDER attached north backstage room of Omega Theatre.", "access": "After CH12 first resolves, the north backstage door remains an ordinary physical route from CH12 whenever the adopted dungeon location is physically reachable. Leaving the chamber does not delete the room or actor.", "actor": "ACT-GLASS-MENDER-SENTINEL", "availability": "At most once per mirror identity.", "stock": "All three exact silver reflection tabs and the recoverable shattered mirror identity are required.", "tabTransaction": "Sentinel inspects first. Refusal or missing stock consumes nothing. On acceptance, all three tabs transfer into the repair cradle and are consumed immediately; mirror pieces remain in Sentinel custody during work.", "procedure": "2 uninterrupted active hours of Sentinel work; no roll. Interruption resets accumulated repair-work time to 0 but does not recreate tabs. If the Sentinel and pieces remain available, work can restart without new tabs because the same consumed tabs remain committed in the cradle.", "discretion": "Sentinel accepts only the original mirror, all three tabs, unused lifetime repair, and a non-hostile requester. It refuses a counterfeit/copy, missing stock, a second repair, or a requester currently attacking/coercing it. A hostility refusal is final for that visit; after the scene returns to non-hostile status for 10 elapsed minutes, one new request may be made. The Sentinel may not invent additional moral tests or prices.", "completion": "Same mirror identity reforms. Pending mirror benefit is not restored. EPI07 Sentinel/history records are neither reset nor copied. A second shattering has no repair procedure in this module."}`

**duplicate.** `Reflections/copies are mundane images only.`

### Glove of Null Ink (`RELIC-NULL-GLOVE-1`)

**Status.** NEW PROVISIONAL AUTHORSHIP completing preserved source relic

**Physical.** `{"form": "single black glove with sealed ebony motes beneath translucent stitching", "weightLb": 0.5, "wearing": "one compatible hand; writing requires that hand free", "attunement": "none"}`

**Acquisition.** `{"scene": "CH03 Echoless Vault", "stock": 1, "procedure": "The glove is already crafted and sealed in a soundless reliquary. After the Silence Wraith is comforted/evaded/defeated, open the reliquary with an Action. This is an already-crafted relic; the module creates no Matrix-dust mining or crafting recipe.", "provenance": "A sealed label says the glove was made from dissolved Matrix dust; no loose usable dust remains.", "depletion": "One glove, no respawn."}`

**airWriting.** `{"activation": "Action", "range": "Choose a point within 10 ft and line of effect; write on a fixed or free-standing plane no larger than 10×10 ft.", "content": "Up to 25 words or equivalent simple symbols in one written language the wearer actually knows. One active inscription per glove; making a new one erases the old.", "duration": "10 elapsed minutes, then vanishes. Wearer can erase early with an Action within 10 ft.", "visibility": "A creature must be able to see the inscription. Blindness, total visual obstruction, and applicable darkness still matter.", "readability": "At observation time, a creature can derive the underlying text only if it currently and sincerely advocates a peaceful but passionless solution to the immediate dispute/topic addressed by the inscription. This is an established fictional stance, not alignment, faction, species, or secret cult membership. The glove never reports who qualifies.", "language": "Eligibility reveals the actual written words, not automatic translation. An eligible observer who does not know the chosen language still needs real language/translation rules.", "copying": "An eligible reader may remember or transcribe the understood ordinary text. An ineligible observer may copy visible shapes, but that copy is nonmagical meaningless glyph-shape data and does not later self-decode.", "limits": "No mind reading, loyalty test, compulsion, KT/PT protection, peacefulness certification, or hidden-identity revelation."}`

**duplicate.** `No inscription duplicates relic/resource/class effects.`

## Local actor profiles

### Memory Forge Toy Sentinel (`ACT-TOY-SENTINEL`)

**Status.** NEW provisional scene actor

**Life.** Construct creature; ordinary monster life-state. At 0 HP it is destroyed/inert unless a local Null rule applies.

**Profile.** Small; AC 15; HP 24; Speed 30 ft; Senses darkvision 60 ft; passive Perception 11; Proficiencies Perception +3; Defenses immune to poison and disease; no other immunity.

**Ability modifiers.** STR +2, DEX +3, CON +2, INT -1, WIS +1, CHA +0

**Actions.**

- **Tin Edge:** +6 melee, reach 5 ft, one target. 1d8+3 slashing

- **Clockwork Lunge:** +6 melee after moving at least 10 ft straight. 1d6+3 bludgeoning; target STR save DC14 or Prone

**Behavior.** Attacks the nearest creature carrying/touching a manifested toy. A successful Comfort action against it ends hostility permanently for this chamber.

### Silence Wraith (`ACT-SILENCE-WRAITH`)

**Status.** NEW provisional scene actor; not bestiary promotion

**Life.** Spirit creature; significant scene NPC using HP. At 0 HP disperses; no harvestable corpse or soul-claim.

**Profile.** Medium; AC 15; HP 58; Speed 30 ft, fly 30 ft (hover); Senses Heartbeat vibration sense 60 ft through contiguous CH03 stone/plate surfaces when the creature with a beating heart is physically supported by those surfaces; passive Perception 14. Motion does not switch off a heartbeat. A genuinely heartbeat-free creature creates no heartbeat signal solely from anatomy, but other ordinary perception remains possible. A flying/hovering creature with no contact to chamber surfaces transmits no heartbeat vibration through them.; Proficiencies Perception +7, Stealth +7; Defenses resistance to nonmagical bludgeoning/piercing/slashing; immune to Deafened.

**Ability modifiers.** STR +0, DEX +4, CON +2, INT +1, WIS +4, CHA +2

**Actions.**

- **Hush Claw:** +7 melee spell-like scene attack; reach 5 ft; one target. 2d6+4 cold; target CON save DC15 or cannot deliberately speak until end of that target’s next regular turn (outside initiative: 6 seconds absolute). This actor-specific speech loss is not the whole Silenced condition; it independently blocks V while it lasts because V requires actual audible speech.

- **Pulse Hunt:** Action; one creature whose heartbeat location the Wraith currently senses within 30 ft. WIS save DC15; failure: Frightened of the Wraith until end of that target’s next regular turn (outside initiative: 6 seconds absolute).

**Behavior.** Hunts strongest heartbeat vibration it can sense. Stillness never erases a heartbeat. It may use ordinary visible-target perception if applicable; heartbeat sense itself does not see through total-cover barriers disconnected from the chamber stone.

### Accord Devil Projection (`ACT-ACCORD-DEVIL`)

**Status.** NEW provisional projection, not bestiary promotion

**Life.** Projection; 0 HP ends projection, no corpse/soul/loot.

**Profile.** Medium; AC 16; HP 52; Speed 30 ft; Senses passive Perception 13; Proficiencies Deception +7, Persuasion +7; Defenses resistance fire; projection ignores disease/poison.

**Ability modifiers.** STR +3, DEX +2, CON +3, INT +2, WIS +1, CHA +4

**Actions.**

- **Contract Blade:** +7 melee weapon attack; reach 5 ft; one target. 1d10+3 slashing + 1d4 fire

- **Measured Rebuke:** +6 ranged spell-like projection attack; range 30 ft; one target. 2d6 psychic

**Behavior.** Prioritizes the demon projection unless a PC attacks or materially aids the demon.

### Accord Demon Projection (`ACT-ACCORD-DEMON`)

**Status.** NEW provisional projection, not bestiary promotion

**Life.** Projection; 0 HP ends projection, no corpse/soul/loot.

**Profile.** Medium; AC 14; HP 60; Speed 35 ft; Senses passive Perception 12; Proficiencies Athletics +7; Defenses resistance cold; projection ignores disease/poison.

**Ability modifiers.** STR +4, DEX +2, CON +4, INT +0, WIS +1, CHA +1

**Actions.**

- **Rending Claw:** +7 melee natural attack; reach 5 ft; one target. 2d8+4 slashing

- **Roar of Refusal:** Action; 15-ft cone; each enemy projection/PC in cone. WIS save DC15; failure Frightened of demon until end of that target’s next regular turn (outside initiative: 6 seconds absolute).

**Behavior.** Rushes the devil projection; attacks PCs only after direct interference against it.

### Echo Doppelganger (`ACT-ECHO-DOPPELGANGER`)

**Status.** NEW provisional scene actor; not a PC copy

**Life.** Projection; 0 HP ends projection, no corpse/soul/XP duplication.

**Profile.** Medium; AC 15; HP 48; Speed 30 ft; Senses passive Perception 13; Proficiencies Acrobatics +7, Insight +5; Defenses resistance psychic.

**Ability modifiers.** STR +2, DEX +4, CON +2, INT +1, WIS +2, CHA +2

**Actions.**

- **Echo Strike:** +7 melee or ranged 20 ft. 2d6+4 force

- **Rehearse Doubt:** one creature within 30 ft. CHA save DC15; failure -2 to next ability check before end next turn

**Behavior.** Looks like the triggering character but copies no class cards, resources, inventory, spells, memories, XP, attunements, or identity. It attacks that character first.

### Ash Feast Steward (`ACT-FEAST-STEWARD`)

**Status.** NEW provisional projection

**Life.** Projection; cannot die. At 0 HP it enters Collapsed Projection: Incapacitated, Prone, Speed 0, no Actions/BA/Reactions, remains present until scene resolves. Legal healing that expressly works on this projection can restore it above 0; otherwise it stays collapsed. Scene resolution dismisses it regardless of HP.

**Profile.** Medium; AC 14; HP 40; Speed 30 ft; Senses passive Perception 12; Proficiencies Insight +5; Defenses immune to poison/disease (projection).

**Ability modifiers.** STR +1, DEX +1, CON +2, INT +2, WIS +2, CHA +3

**Actions.**

- **Ash Ladle:** +5 melee weapon attack; reach 5 ft; one target. 1d6+2 bludgeoning; no attack unless party becomes violent

**Behavior.** Explains serving etiquette truthfully, never forces eating, and allows withdrawal.

### Witness Sera, Quiet-Well Recorder (`ACT-NULL-WITNESS`)

**Status.** NEW provisional mortal NPC for chamber access

**Life.** Living humanoid significant NPC; uses death saves if reduced to 0.

**Profile.** Medium; AC 12; HP 22; Speed 30 ft; Senses passive Perception 14; Proficiencies Insight +7, Religion +6, Persuasion +5; Defenses none beyond ordinary equipment.

**Ability modifiers.** STR +0, DEX +1, CON +1, INT +3, WIS +4, CHA +2

**Actions.**

- **Quarterstaff:** +3 melee. 1d6 bludgeoning

- **Record Petition:** noncombat. Acts as local Witness only for current EPI06 petition step one; grants no automatic favorable Archon response.

**Behavior.** Neutral recorder; refuses coercion, follows current EPI06 motive-record procedure, and leaves if attacked.

### Glass-Mender Sentinel (`ACT-GLASS-MENDER-SENTINEL`)

**Status.** NEW finite local projection; not bestiary promotion

**Life.** Projection tied to CH12 repair room. At 0 HP it disperses for 1 hour, interrupting work; then the same projection identity reforms in the repair room if CH12 still exists. No corpse, soul, loot, XP or copied Sentinel history.

**Profile.** Medium; AC 16; HP 45; Speed 25 ft; Senses passive Perception 15; ordinary sight/hearing; Proficiencies Investigation +7, artisan glasswork +7; Defenses resistance to psychic; immune poison/disease (projection).

**Ability modifiers.** STR +2, DEX +1, CON +3, INT +4, WIS +3, CHA +1

**Actions.**

- **Ward Staff:** +5 melee weapon attack; reach 5 ft; one target. 1d6+2 force; used only if attacked

- **Mend Mirror:** noncombat. Uses RELIC-MIRROR-SILENCE-1 reformation transaction; no attack roll.

**Behavior.** Neutral custodian. Never pursues outside repair room; follows the finite acceptance/refusal rule printed on the mirror.

## Twelve chamber seeds

### 1. Memory Forge (`CH01-MEMORY-FORGE`)

**Status/placement.** NEW provisional chamber scene Conditional: adopt only at an actual existing undocumented-floor site appropriate to the campaign. Original source premise is after Infinite Yield; use outside that premise must be explicitly logged as alternate staging. No numbered floor/epoch selected.

**Geometry.** 40×40-ft square; west arch entrance, east arch ordinary exit initially sealed; central 10-ft forge dais; four 5-ft toy plinths.

**What is perceived.** Warm metal smell, hammer ticks with no smith, four metal toys mimic fictional childhood objects chosen by characters or Director-safe prompts.

**Danger telegraph.** Before any attack, each toy raises its edge and the forge projects the words 'COMFORT WHAT MEMORY MADE SHARP.'

**Objective.** Open east exit by calming or disabling all four toys.

**Actors.** ACT-TOY-SENTINEL

**Procedure.**

1. Comfort: Action within 5 ft, CHA (Persuasion) or WIS (Insight) DC14 using fictional character context; success permanently calms one toy. A character may instead place the toy on forge dais and spend 1 minute repairing/arranging it with INT (Engineering) DC14; success calms it.

2. Combat is legal. At 0 HP a toy is inert and counts resolved.

3. Withdrawal: west entrance remains open; unresolved toys do not pursue beyond room.

**Failure/withdrawal.** A failed Comfort check provokes that toy's next attack against the acting character; no infinite escalating DC.

**Reward.** When all four resolve, east exit opens and one 0.5-lb Memory Ingot appears. It is a mundane narrative relic with no recipe/power and never respawns.

**Persistence.** Calmed/destroyed toys remain resolved; ingot appears once.

### 2. Gallery of Unpainted Murals (`CH02-UNPAINTED-GALLERY`)

**Status/placement.** NEW provisional chamber scene Conditional undocumented-floor scene; same temporal wrapper as CH01.

**Geometry.** 20×60-ft hall; entrance south, exit north; six blank wall panels.

**What is perceived.** Dry pigment smell, soft brush-noise from empty walls.

**Danger telegraph.** A brass placard states: 'TOUCH SHOWS AMBITION; IMAGE IS POSSIBILITY, NOT PROPHECY.'

**Objective.** Reveal three murals and choose one fictional ambition to acknowledge.

**Procedure.**

1. Touching a panel is an Object Interaction and creates one image of a plausible next ambition for that character, chosen from already-established character fiction or a Director-safe prompt. It is not guaranteed future truth.

2. After three images, one character spends an Action to state, sign, or write which image they pursue/reject and why; no roll. Players need not disclose real personal goals.

3. Alternative: 10-minute INT (Investigation) DC14 identifies the acknowledgement latch and permits a neutral statement such as 'These are possibilities, not commands.'

**Failure/withdrawal.** No lethal failure. Refusing interaction leaves north exit shut; south exit remains open.

**Reward.** One finite mural rubbing sheet (0.02 lb) showing only the chosen image; no divination power.

**Persistence.** Each panel reveals once per character identity; revisiting does not generate new ambitions/rewards.

### 3. Echoless Vault (`CH03-ECHOLESS-VAULT`)

**Status/placement.** NEW provisional chamber scene Conditional undocumented-floor scene; same wrapper.

**Geometry.** 35×35-ft vault on 5-ft grid. West threshold at (0,15–20), east reliquary/exit at (35,15–20). Seven numbered 5-ft plates form the center line at x=2.5,7.5,12.5,17.5,22.5,27.5,32.5; y=17.5. The west threshold includes a 5-ft mechanically isolated stone sill outside the plate lattice.

**What is perceived.** Absolute acoustic silence inside; vibrations visibly ripple silver dust on floor.

**Danger telegraph.** At threshold, footprints make silver rings and a translucent hunter turns toward them.

**Objective.** Reach east reliquary or open north exit without feeding the hunter vibrations.

**Actors.** ACT-SILENCE-WRAITH

**acousticField.**
```json
{
  "status": "NEW scene-local physical sound-suppression field, not global Silenced condition",
  "boundary": "Entire interior volume east of the west threshold plane through the east wall, floor-to-20-ft ceiling. Threshold plane itself is boundary; exterior west sill is outside.",
  "rule": "Ordinary sound does not transmit within the field or across any path segment inside it. A creature inside cannot produce an audible V component; Action-time and Reaction V casting fail before costs that commit only on a legal cast. Audible Bard/command/hearing features fail when their required sound path lies inside. Thought, sight, writing and signs remain possible under actual language rules. No antimagic, thunder immunity or automatic comprehension."
}
```

**Procedure.**

1. Heartbeat truth: the Wraith senses heartbeat vibrations under ACT-SILENCE-WRAITH; remaining motionless does not hide a beating heart.

2. Plate solution is fixed 1→3→5→7. The west-wall inscription can be studied from the isolated sill for 10 uninterrupted minutes; INT (Investigation) DC14. Success reveals the sequence; failure gives no false sequence and the same character cannot retry until after one beneficial Short or Long Rest. The sill does not transmit heartbeat vibration into the plate lattice.

3. To depress a numbered plate, a creature/object must physically press that plate; one Action latches it. Latches persist. Pressing a wrong plate resets only the current sequence, never actor HP or consumed resources. Four correct Actions total open east exit and pacify Wraith.

4. Crossing connected chamber stone while supported transmits a living heartbeat even if the creature is motionless. A truly heartbeat-free creature has no heartbeat signal; this does not grant invisibility or immunity to ordinary senses.

5. Combat and legal mobility/flight/teleport remain available only from actual features. The chamber grants no generic sound, flight, telepathy or stillness immunity.

**Failure/withdrawal.** Failed pattern resets only plate sequence, not room/relic. West entrance remains ordinary withdrawal.

**Reward.** East reliquary contains the one Glove of Null Ink, RELIC-NULL-GLOVE-1.

**Persistence.** Glove stock one; Wraith remains pacified/dispersed after terminal resolution.

### 4. Tessellation Garden (`CH04-TESSELLATION-GARDEN`)

**Status/placement.** NEW provisional chamber scene Conditional undocumented-floor scene.

**Geometry.** 45×45-ft garden. Three 10-ft-deep traversal rows run west→east. Each row has three 5-ft lanes A/B/C separated by flower beds. Fixed safe lanes: Row1=B, Row2=A, Row3=C. Each unsafe lane has a catch net 10 ft below that lane and a fixed return ladder to that row’s west staging strip.

**What is perceived.** Geometric flowers rotate; loose pebbles fall sideways over certain beds.

**Danger telegraph.** Petals point in alternating gravity directions before each zone changes.

**Objective.** Cross without forcing the geometry.

**map.**
```json
{
  "row1": {
    "safe": "B"
  },
  "row2": {
    "safe": "A"
  },
  "row3": {
    "safe": "C"
  },
  "persistence": "Fixed for this chamber identity; observation never rerolls it."
}
```

**Procedure.**

1. At each row, a creature within 5 ft of its petal marker may spend an Action to read it: WIS (Perception) or INT (Investigation) DC14. Success identifies the fixed safe lane. Failure gives no false answer. One Action read per character per row; after failure that character may retry only after 10 uninterrupted minutes studying that same row.

2. Entering an unsafe lane triggers gravity immediately: DEX save DC14. Success returns creature to row start without entering the lane and spends the attempted 5 ft movement. Failure drops it 10 ft onto that lane’s net, Prone, taking 1d6 bludgeoning.

3. Net recovery is a scene-local climb: Action plus 20 ft of remaining movement to climb 10 vertical ft (2:1) and emerge on that row’s west staging strip. If the creature lacks 20 ft remaining movement, it cannot start recovery unless it legally increases its movement budget first. An adjacent ally at the strip may Help normally if physically possible.

4. Rope, flight, teleportation or shapechanging work only if an actual rule grants them and destination/space is legal. No free generic traversal ability.

**Failure/withdrawal.** No lockout; parties can backtrack to entrance. Repeated failed reads do not change safe path.

**Reward.** One finite packet of geometric seeds, purely decorative/no recipe.

**Persistence.** Safe pattern fixed for chamber identity; seeds one packet.

### 5. Negative Feast Hall (`CH05-NEGATIVE-FEAST`)

**Status/placement.** NEW provisional chamber scene Conditional undocumented-floor scene.

**Geometry.** 30×50-ft hall; south entrance, north exit; table seats eight; seven covered dishes plus one empty plate.

**What is perceived.** Food smells rich, but shadows under dishes are ash-gray.

**Danger telegraph.** Steward says: 'No guest receives a second portion until every seated guest who asks has one.'

**Objective.** Demonstrate restraint and distribute first portions fairly.

**Actors.** ACT-FEAST-STEWARD

**Procedure.**

1. Eight first portions exist. Any willing creature may sit; no one is compelled to eat. Serve no creature a second portion until every seated creature that requested food has one. Serving is an Action.

2. Success after all requested first portions are distributed and party waits 1 minute without taking a second.

3. Investigation DC14 after 10 minutes states the rule plainly. Characters may also leave seats empty.

**Failure/withdrawal.** If a second portion is taken early, all remaining food turns to ash; scene fails but south exit stays open. No poisoning or forced starvation.

**Reward.** Success opens north exit and leaves two mundane 1-day ration packs; finite.

**Persistence.** Food/rations do not replenish.

### 6. Ladder Debris Shaft (`CH06-LADDER-DEBRIS`)

**Status/placement.** NEW provisional chamber scene Conditional undocumented-floor scene.

**Geometry.** 60-ft shaft, 10×10-ft clear interior. Bottom ledge z=0–5 ft, top ledge z=60 ft. Four 15-ft rung segments: S1 z0→15, S2 15→30, S3 30→45, S4 45→60. One fixed wall cable runs z=0→60 with clips at every 5 ft; rated 600 lb total attached load. One creature occupies a rung segment at a time unless actual size/space permits otherwise.

**What is perceived.** Broken luminous rungs blink in sequence; wind rises each segment.

**Danger telegraph.** Etched handprint reads 'COURAGE IS CONTINUING WHILE AFRAID, NOT A NEW SKILL.'

**Objective.** Ascend four segments.

**Procedure.**

1. Clip to safety cable: Action at bottom/top or while adjacent to cable; one free hand. Harness/clip is chamber stock and stays on cable. An attached creature and carried load count against 600-lb capacity.

2. Climb one 15-ft segment: requires an Action, 30 ft of remaining movement (scene-local 2:1 climb cost), and STR (Athletics) DC14 or DEX (Acrobatics) DC14. The Action and 30 movement are both spent on success or failure. If insufficient movement remains, the attempt cannot begin.

3. A frightened climber may spend an Action once for that segment to make WIS save DC14. Success grants advantage on its next check for that segment before its next regular turn starts (outside initiative: within 6 seconds); failure grants nothing. This is not the climb Action.

4. Failure while clipped deals 1d6 bludgeoning and catches at max(0, segmentStartZ−5). Thus S1 failure catches on bottom ledge z=0, never below floor. For S2–S4 the creature hangs 5 ft below segment start.

5. Recover from a hanging catch above z0: Action plus 10 ft remaining movement to climb 5 ft back to segment-start ledge; no check. This is not a free ascent and does not complete the failed segment.

6. An ally securely on the destination ledge/segment top may spend Help Action to grant ordinary advantage if physically able; the old +2 is removed to use the current Help interface and avoid stacking a duplicate assistance engine.

**Failure/withdrawal.** Three failures by same climber do not end scene; withdrawal downward remains possible. Ordinary actual flight/teleport works if legal.

**Reward.** Top ledge holds one finite 50-ft luminous rope (ordinary rope visibility only, no magic bonus).

**Persistence.** Rope stock one.

### 7. Quiet Well Remnant (`CH07-QUIET-WELL`)

**Status/placement.** NEW provisional chamber scene Conditional undocumented-floor scene.

**Geometry.** 25-ft circular chamber with 10-ft-diameter well centered at origin. Entrance west; east door opposite. A marked 10×10 petition alcove occupies the southwest wall and is outside the active Null field.

**What is perceived.** Faint gray-blue glow; spoken words sound emotionally flat near rim.

**Danger telegraph.** Mask-shaped relief shows one face intact, one cracked, with inscription 'WEAR WHAT YOU MADE; RECEIVE WHAT IT MEANS.'

**Objective.** Interact with well or bypass safely.

**Actors.** ACT-NULL-WITNESS

**nullField.**
```json
{
  "fieldId": "NULL-FIELD-QUIET-WELL-1",
  "status": "NEW operational boundary for the source small Null glow",
  "boundary": "Vertical cylinder radius 7.5 ft centered on well, floor to 10 ft above floor. Crossing boundary starts/stops exposure; visual glow outside that cylinder is not exposure.",
  "clock": "Use NULL-FIELD-01 accumulation by stable field identity. The field’s hourly clock is continuous per creature exposure time; leaving pauses this field accumulator rather than deleting it. Reentry resumes same partial exposure.",
  "petitionAlcove": "Outside cylinder. One-hour EPI06 meditation there adds no exposure unless creature voluntarily enters the cylinder.",
  "order": "At an exact timestamp, process already-due field hourly save before a later same-timestamp voluntary petition/blessing completion unless the source event explicitly has earlier priority; a qualifying Temporary Blessing purge then resolves and does not erase continued field exposure."
}
```

**Procedure.**

1. One character wearing an operative Living mask may spend 1 uninterrupted minute at rim stating a fictional vow-related truth; gain one temporary Inspiration d6 that expires at next beneficial Long Rest and does not exceed the current EPI01 Inspiration pool cap.

2. A wearer of an operative Cracked mask doing the same records one Disquiet d6 under current EPI01 rules instead; no extra permanent boon.

3. Unmasked/dormant-mask characters receive only an image and no mechanical boon/bane.

4. Bypass: WIS (Insight) DC14 after 10 minutes identifies that interaction is optional; east door opens by ordinary lever after 1 minute regardless.

**Witness.** Witness Sera is present once per chamber adoption and can fulfill EPI06 consultation step one for otherwise eligible petitioners. The chamber provides a 10×10 quiet alcove for the one-hour meditation, but petition timing/result remain current EPI06.

**Failure/withdrawal.** No forced mask use. Well does not purge Null Veil by itself.

**Reward.** Finite one-time well response per character identity; no refill by revisiting.

**Persistence.** Response ledger per character/chamber.

### 8. Wax Library Seed — Silent Cell (`CH08-WAX-SEED`)

**Status/placement.** NEW provisional chamber separate from reviewed Floor68 holdings Conditional undocumented-floor scene. Explicitly not the Floor68 Melted Annex or Floor50 service collection.

**Geometry.** 20×30-ft cell; six wax strips on wall, south entrance, east exit.

**What is perceived.** Warm wax smell; copper tabs numbered 1–6.

**Danger telegraph.** Door plate: 'VOICE MELTS; EYES PRESERVE.'

**Objective.** Silently preserve four harmless strips or solve copper-tab fallback.

**Procedure.**

1. Each strip has 20 words of NEW harmless local maintenance poetry, not Equation evidence. Silent reading in known language takes 1 minute/strip and may be copied normally.

2. Reading a strip aloud starts 60-second irreversible melt of that strip. Stopping speech does not reverse it.

3. After four strips are silently read/coped, east exit opens.

4. Fallback if fewer than four strips remain: 10-minute INT (Investigation) DC15 on copper tabs; success derives mechanical tab sequence 2-5-1-6 and opens exit. Failure gives no false sequence; Critical Failure locks tab panel 1 hour.

**Failure/withdrawal.** Destroyed strips never respawn and cannot satisfy any Matrix research/library prerequisite.

**Reward.** One mundane wax-seal kit with six seals; no recipe/evidence power.

**Persistence.** Strip destruction/copies and seal stock persist.

### 9. Twin Wind Passages (`CH09-TWIN-WIND`)

**Status/placement.** NEW provisional chamber scene Conditional undocumented-floor scene.

**Geometry.** Entry chamber 20×20; two parallel 40-ft corridors, Blue and Amber, rejoin at one 20×20 exit room.

**What is perceived.** Each corridor shows a staged projection of the party making a different immediate chamber choice.

**Danger telegraph.** Threshold says 'ONE PATH SOLIDIFIES. NO SELF IS COPIED.'

**Objective.** Choose which projected local outcome becomes the chamber's path.

**voting.**
```json
{
  "stock": "12 physical numbered decision tokens, TOKEN-WIND-01..12, 0.05 lb each, fixed chamber stock. At voting-open assign at most one token to each eligible voter in stable Expedition identity order; unused tokens remain in bowl.",
  "eligibility": "Conscious Expedition character physically present in the entry chamber before voting closes. Temporary summons, pets, companions, minions, projections and scene actors are not voters unless they are independently recorded Expedition characters. A late qualifying Expedition character arriving before closure may receive one unused token; arrival at/after closing timestamp is too late.",
  "oneVote": "Each assigned identity controls one token. Depositing it in Blue/Amber is an Action. Moving that same token to the other socket before close is another Action and changes the vote. Duplicate/unassigned deposits are rejected and do not count. An eligible voter may declare abstention with brief communication; its token returns to bowl.",
  "close": "Closes immediately when every then-eligible voter has either a deposited token or recorded abstention, or at exactly +10:00 from scene opening, whichever occurs first. At the exact timeout, close happens before a same-timestamp late arrival/deposit.",
  "tie": "Count one deposited token per eligible identity. Tie selects Blue by fixed neutral order. One corridor solidifies once; one Wind Token reward at most once."
}
```

**Procedure.**

1. At scene open, initialize the finite voting ledger and +10:00 deadline under the voting rule.

2. Blue/Amber projections are chamber-local possibilities, not another timeline or duplicate party.

3. Resolve deposited one-identity votes at close. Solidification opens chosen corridor and seals the other. Entry stays open.

4. If no votes before timeout, Blue opens and no Wind Token reward. A deliberate nonempty vote before timeout produces the one 0.1-lb Wind Token after solidification.

**Failure/withdrawal.** Timeout with no votes opens Blue and gives no reward. No history rewrite.

**Reward.** If deliberate choice before timeout, one 0.1-lb Wind Token appears; narrative proof only.

**Persistence.** Choice fixed forever for chamber identity.

### 10. Crimson Accord Arena (`CH10-CRIMSON-ARENA`)

**Status/placement.** NEW provisional chamber scene Conditional undocumented-floor scene.

**Geometry.** 50-ft-diameter arena; west entry gate, east exit gate, central 10-ft accord circle.

**What is perceived.** Red and blue projection sigils manifest one devil and one demon reenacting a historical-looking but explicitly staged duel.

**Danger telegraph.** Banner: 'REENACTMENT — YOUR CHOICE CHANGES THIS PERFORMANCE, NOT HISTORY.'

**Objective.** Influence staged duel or broker accord.

**Actors.** ACT-ACCORD-DEVIL, ACT-ACCORD-DEMON

**Procedure.**

1. At initiative start both projections use their printed profiles and normally prioritize each other. The Director records exact starting spaces: Devil at west inner edge, Demon at east inner edge, 30 ft apart; PCs enter through west gate outside the projections’ initial spaces.

2. Accord: a PC inside central 10-ft circle spends Action, CHA (Persuasion) DC15. Two successes total before either projection reaches 0 creates Accord terminal. A failed attempt causes each projection, on its next regular turn, to use one legal attack against that broker if possible, then resume default duel.

3. Terminal states: Devil Victory (Demon alone reaches0/disperses); Demon Victory (Devil alone reaches0/disperses); Mutual Ruin (one resolved packet/event reduces both to0 before accord); Accord (second success commits before either reaches0). East gate opens immediately after terminal resolution.

4. Favor: only Accord grants exactly one CH10 Favor Mark, assigned by the successful second broker to one conscious participating Expedition character in the arena. It gives advantage on one social check against ACT-ACCORD-DEVIL, ACT-ACCORD-DEMON or ACT-GLASS-MENDER-SENTINEL before leaving CH10/CH12 seed complex, then is consumed; it never changes real planar faction standing.

5. Spear: on Accord, fragment rises from center plinth immediately and may be taken with Action. On Devil Victory, Demon Victory or Mutual Ruin, fragment appears sealed for exactly 1 elapsed hour, then becomes takeable. One item only.

**Failure/withdrawal.** No real planar faction standing changes. 'Planar favor' is one local Favor Mark granting advantage on one social check with a projection/Sentinel inside this chamber only, then consumed; expires on exit.

**Reward.** One Concord Spear Fragment appears at terminal state per relic acquisition rules.

**Persistence.** Projection outcome and spear depletion persist; no replay farming.

### 11. Shardpool Confluence (`CH11-SHARDPOOL`)

**Status/placement.** NEW provisional bounded plane-swap scene Conditional undocumented-floor scene; does not grant general plane travel.

**Geometry.** 30×30-ft pool chamber. Central 10×10 pool. Four 5-ft plinths at cardinal points. Emergency return pad is a marked 20×20×20-ft volume occupying the northeast chamber quadrant/overhead return volume; while any card visit is active it is a reserved destination and ordinary voluntary placement into it is illegal.

**What is perceived.** Pool reflects four reviewed primary realms; four facedown one-use shard cards float above it.

**Danger telegraph.** Inscription: 'DRAW WITHOUT RETURN; TEN MINUTES; THE POOL BRINGS YOU BACK.'

**Objective.** Survive/adapt to brief plane landings or decline.

**Procedure.**

1. Four one-use cards correspond exactly to Crystal Bastion, Veiled Expanse, Radiant Currents and Boundless Void. Shuffle facedown; draw without replacement. Action by willing group up to six adjacent creatures activates drawn card. All must fit destination 20×20×20 landing volume at activation; otherwise activation fails and card is not consumed.

2. On successful activation, record traveler identity set, their current body footprints/heights and carried noncreature gear; consume card once. They swap to bounded landing cell for exactly 10:00 elapsed minutes. Noncreature objects lawfully picked up inside a landing cell may return if physically carried at return. A creature not in the recorded traveler set never becomes return-eligible merely by being carried later.

3. At +10:00 return attempt resolves before same-timestamp local events. Recheck each recorded traveler’s current footprint/height. Place into original marked footprint if legal; otherwise nearest legal chamber placements in stable traveler-ID order. Return of one traveler does not duplicate/remove another. An original traveler being physically carried by another is still placed once as its own traveler identity. Lost/dropped gear stays where actually left.

4. If any traveler cannot be legally placed, already placed travelers remain returned; unresolved travelers stay in landing cell for a recovery extension of at most 10 minutes with ordinary agency. At +20:00 make second attempt.

5. If still impossible at +20:00, use emergency pad if current body fits and pad is legal. If pad is physically impossible despite reservation, unresolved travelers enter Return Hold in their landing cell: they are frozen, cannot act/move/interact/harvest or be targeted, and no local clocks/effects newly advance for them. Recheck legal chamber placement every 1 elapsed minute and place them at first legal opportunity in stable ID order. Return Hold grants no continued plane access or onward travel.

6. Each card remains consumed after successful activation regardless of return delay. No onward portal exists.

**Destinations.**

- **Crystal Bastion:** 20×20×20 cinder-font cell; safe platform, one sealed Xi reliquary and six uniquely numbered 1-pint Bastion flame-water flasks FW-1..FW-6, 1 lb each. No active Null exposure field. No exit beyond invisible boundary.

- **Veiled Expanse:** 20×20×20 gray fen cell; NO active Null exposure field merely from realm name. Finite portable planting stock: three Bittersap trays BT-TRAY-1..3 (each 24×12×8 in, 18 lb, two mature nodes), two Echo Lily basins EL-TRAY-1..2 (18×18×6 in, 14 lb, two blooms), one Tranquil Thorn tray TT-TRAY-1 (18×12×6 in, 8 lb, four sprigs), one Black Hush tray BH-TRAY-1 (18×12×4 in, 7 lb, four patches). Lifting one container from its cradle is an Action, requires two free hands, and makes that exact container carried gear; one creature can carry at most one such bulky container at a time unless an actual carrying feature permits otherwise. Removing a container removes its exact plant identities from this landing cell permanently. Containers have AC10/5HP and ordinary object consequences; destruction/loss never respawns plants. Recognition/harvest may occur later from the same carried container under the flora rules.

- **Radiant Currents:** 20×20 shallow luminous current; DEX save DC14 on arrival or Prone; no damage; one finite prism shell (narrative only).

- **Boundless Void:** 20×20 force-lattice cell with no air loss/gravity hazard in this bounded staging bubble; WIS save DC14 or Frightened until end of next turn from vertigo. No outer travel.

**Failure/withdrawal.** Declining interaction leaves north exit lever usable after 1 minute. Consumed cards stay consumed even if party leaves.

**Reward.** Finite destination contents only. Xi Pendant and flora/flame water are real stock; no duplication.

**Persistence.** Four-card deck and all landing-cell stock persist globally for this chamber identity.

### 12. Omega Theatre (`CH12-OMEGA-THEATRE`)

**Status/placement.** NEW provisional consent-safe chamber scene Conditional undocumented-floor scene.

**Geometry.** 30×40-ft theatre; entry rear, stage front, east exit; one mirror trapdoor center stage.

**What is perceived.** Empty seats whisper lines from fictional character histories already established in play.

**Danger telegraph.** Playbill: 'CHARACTER FICTION ONLY. ANY PLAYER MAY USE THE NEUTRAL PROMPT.'

**Objective.** Narrate or otherwise acknowledge one unresolved fictional vow, or face/resolve Echo Doppelganger.

**Actors.** ACT-ECHO-DOPPELGANGER

**Procedure.**

1. Each participating character chooses: (A) state/sign/write one fact about their current fictional unfinished vow; (B) use neutral prompt 'My character admits the vow is unresolved'; or (C) decline.

2. No real-world personal disclosure is ever required. Current EPI03 vow record supplies fiction if player chooses.

3. If at least one participating character completes A/B, theatre accepts and exit opens after 1 minute. Characters who decline suffer no penalty.

4. If all present decline, one Echo Doppelganger projection manifests for one randomly selected willing-to-engage character; if nobody consents to combat, theatre instead opens exit after 10 minutes with no relic reward.

5. Combat terminal: Doppelganger at 0 disperses; alternatively its target can spend Action and complete neutral prompt, causing projection to disperse.

**Failure/withdrawal.** No character is compelled to speak. Exit always available through consent-safe terminal branch.

**Reward.** Mirror of Potential Silence plus exactly three silver reflection tabs appears only if scene resolves through A/B or Doppelganger resolution; not on 10-minute no-engagement exit.

**Persistence.** One mirror total; one lifetime Sentinel reformation stock bundled with it.

## Residual Null adjudication

Only an explicitly mapped field contributes exposure. Visual vocabulary or a realm name does not. A visual glow, realm name or Veiled Expanse label is not an exposure field. Only a scene with an explicit fieldId/boundary contributes exposure. CH07 has NULL-FIELD-QUIET-WELL-1; CH11 Veiled Expanse landing cell has no active field.

### Null Veil — damage roots and source lifecycles

Qualifying damage is flagged at root creation as already specified in the model. Delayed descendants retain the creation-time flag; transfers preserve it; true reflected/new damage evaluates the new dealer. The following recipient branches are controlling:

```json
{
  "ordinaryLiving": "New positive→0: Stable0 as above. Already Dying0: remains Dying with same counters/deadline markers. Already Stable0: remains Stable with same recovery deadline.",
  "rangerBeast": "Source normally dies immediately at0. Qualifying Null damage replaces that damage-caused immediate-death transition with Null Disabled at0: Incapacitated, Speed0, no commands/actions; same animal/bond remains. Ordinary legal companion healing above0 ends Disabled. A later independent non-damage death/removal rule still works.",
  "finiteSummonFamiliarMirrorBeast": "Source normally disappears/ends at0. Qualifying Null damage replaces only that damage-caused zero disappearance with Null Disabled at0 while its original duration/source still exists. Independent duration expiry, dismissal, concentration/source end or replacement still ends it. Legal companion healing above0 restores function; no generic repair/resummon is granted.",
  "mageLichElite": "Source normally becomes destroyed bound asset at0. Qualifying Null damage leaves same elite Null Disabled at0, not destroyed; therefore Soulbound is not legal solely from this zero. Legal companion healing above0 restores it. An independent actual destruction/expiry can later create its normal destroyed state.",
  "wizardStandardUndead": "Qualifying Null damage leaves same minion Null Disabled at0 instead of damage-caused destruction. Dismissal or owner completed-LR expiry still ends it. Legal healing above0 if a real source applies may restore it.",
  "localProjection": "A scene projection whose printed 0-HP rule says disperse/end uses that administrative projection endpoint. This is not a living death/corpse transition and is not converted into Stable/Disabled unless that specific actor says so. ACT-FEAST-STEWARD is the explicit exception with Collapsed Projection.",
  "undyingSpellform": "If qualifying damage newly reduces a Mage with actual Undying Spellform to0 without killing outright, its printed trigger occurs and its 1/LR use is spent. It overrides zero-HP Unconscious/Incapacitated permissions as reviewed: conscious, half-Speed voluntary movement, normal Action, legal spellcasting/concentration, no independent BA/Reaction. Triggering damage still causes its concentration save. If still0 at feature expiry, the reviewed expiry destabilizes/cancels Stable recovery and adds one failed death save; that later feature-expiry event is not the original Null damage packet.",
  "wouldDieProtections": "A protection whose trigger requires actual death/would-die/fatal result does not trigger and spends no use when Null skips that damage-caused death branch. Do not replay it later. Separate minimum-HP prevention that resolves earlier follows its own source if actually triggered."
}
```

**Living branch.** After ordinary mitigation/temp HP, a qualifying packet may reduce a living recipient to 0. If it was positive before the packet and becomes 0, skip damage-caused Instant Death, Wound/Maiming creation, death-save failures and ordinary death; it becomes Stable0 with death successes/failures reset under Core and receives exactly one normal Stable recovery deadline. If it was already Dying0, the packet adds no damage-caused failure but DOES NOT stabilize it, clear counters or change its existing death-save schedule. If already Stable0, it remains Stable and keeps its existing absolute recovery deadline; do not reroll/extend it. If temporary HP absorbs all HP loss and normal HP never reaches0, no zero-state transition occurs.

**Preexisting history.** Does not remove old Wounds/Injuries, revive Dead creatures, clear existing dying counters, rewrite death history, cure conditions, or prevent non-damage lethal costs/tracks. Newly-zero stabilization resets only its current death-save counters because becoming Stable requires that under Core.

### Shrug Off Empathy timing

Use reviewed COMBAT_ACTION_PLAYTEST timing. Initiative-created success expires at the next regular source-start virtual marker; if initiative ends first, that virtual marker continues every six seconds and expiration still occurs at its original scheduled instant. Outside-initiative success uses absolute +6s and keeps that deadline if initiative begins. Initiative-created failure expires at end of next regular source turn using preserved virtual end marker; outside-initiative failure uses absolute +60s and keeps that deadline if initiative begins. Starting/ending/reordering initiative or extra turns never restart, shorten, extend or duplicate these records.

**Activation.** Bonus Action while active and not Incapacitated; CHA save DC15, binary.

**Success.** Suppress Veil until the start of the character's next regular turn in initiative. Outside initiative, suppress for 6 elapsed seconds. During suppression passive Insight and damage conversion are inactive, but the Veil record remains and exposure clocks continue.

**Failure.** Apply actual Incapacitated until the end of the character's next regular turn. Outside initiative, 1 elapsed minute. Concentration ends immediately under current Incapacitated rule. After duration, Bonus Action can be attempted again if otherwise legal.

### Purging Null Veil

Use only the three printed purge avenues in the model: operative-mask confession extension, an actual EPI-06 Temporary Blessing result 5–8, or one real Bittersap antidote dose. Purge removes Veil; it does not erase field exposure, Wounds, Corruption, Hunt, Strain, Dissonance or unrelated conditions.

## Flora and antidote

### Bittersap Root (`FLORA-BITTERSAP`)

**Habitat/stock.** CH11 Veiled Expanse landing cell, damp gray loam; 6 mature nodes; each node one harvest attempt; no replenishment in this module

**Portable identity.** Nodes are fixed identities BT-1..BT-6, two per BT-TRAY-1..3. Moving a tray moves those same nodes; it creates none.

**Recognition.** 10 minutes, INT or WIS (Nature) DC14. Success identifies plant and safe root; failure = uncertainty, not false ID.

**Harvest.** 20 minutes, one hand + small knife or herbalism kit; WIS (Survival) DC14. Critical Success 2 parts, Success 1, Failure 0 and node is bruised/consumed, Critical Failure 0 and tool must be cleaned 10 minutes before another flora harvest.

**Unit/freshness.** 1 part = 0.1 lb cleaned root; 7 days ordinary storage; 30 days in a sealed cool specimen case; then spoiled/nonfunctional.

**Effect.** No direct mechanical effect when eaten raw; recipe ingredient only.

### Tranquil Thorn (`FLORA-TRANQUILTHORN`)

**Habitat/stock.** CH11 Veiled Expanse landing cell, dry raised stones; 4 sprigs; no replenishment

**Portable identity.** Sprigs TT-1..TT-4 all in TT-TRAY-1.

**Recognition.** 10 minutes Nature DC14

**Harvest.** 10 minutes with gloves or tongs; DEX (Herbalism kit) DC14. Critical Success 2 parts, Success1, Failure0 and sprig breaks, Critical Failure0 and harvester takes1 piercing damage.

**Unit/freshness.** 0.05 lb; 14 days dry; 60 days sealed

**Effect.** No default combat/cure effect. A brewed nonmagical tea is calming fiction only and grants no mechanical bonus.

### Echo Lily (`FLORA-ECHOLILY`)

**Habitat/stock.** CH11 Veiled Expanse landing cell, shallow reflective water; 4 blooms; no replenishment

**Portable identity.** Blooms EL-1..EL-4, two per EL-TRAY-1..2. Moving a basin moves those same blooms; it creates none.

**Recognition.** 10 minutes Nature DC14

**Harvest.** 10 minutes with herbalism kit; DEX (Herbalism kit) DC14. Critical Success 2 parts, Success1, Failure0 and bloom wilts, Critical Failure0 and adjacent second bloom also wilts (if any).

**Unit/freshness.** 1 part = 0.05 lb petals; 3 days ordinary; 14 days sealed cool

**Effect.** Recipe ingredient only; no standalone echo/memory power.

### Black Hush Moss (`FLORA-BLACKHUSH`)

**Habitat/stock.** CH11 Veiled Expanse landing cell, shaded stone edge; 4 patches; no replenishment

**Portable identity.** Patches BH-1..BH-4 all in BH-TRAY-1.

**Recognition.** 10 minutes Nature DC14

**Harvest.** 10 minutes with scraper/herbalism kit; DEX (Herbalism kit) DC14. Critical Success2 parts, Success1, Failure0 and patch lost, Critical Failure0 and one adjacent patch contaminated (if any).

**Unit/freshness.** 0.05 lb; 30 days dry/sealed

**Effect.** No default Null cure or silence effect. Can be used as mundane black dye after 10 minutes steeping.

### Bittersap Antidote

**id.** NULL-ANTIDOTE-01

**name.** Bittersap Antidote

**status.** NEW special procedure; not added to 687 reviewed trade recipes

**ingredients.** 2 Bittersap parts + 1 Echo Lily part + 1 pint actual Bastion flame water

**flameWater.** `{"source": "CH11 Crystal Bastion landing cell", "stock": "6 sealed 1-pint flasks, 1 lb each; no replenishment. Home-plane affiliation, Concord Step, or ordinary plane choice creates none.", "access": "Only via an actually adopted CH11 shard-card activation or another separately authored lawful source; this module grants no general Bastion travel."}`

**apparatus.** Heatproof pot, stirring tool, one ordinary heat source; Herbalism kit or Alchemist's supplies available to the brewer.

**work.** 30 uninterrupted active minutes. Ingredients are committed/consumed when boiling begins. At completion make INT (Herbalism kit) or INT (Alchemist's supplies) DC15; use proficiency only if actually proficient.

**outcomes.** `{"Critical Success": "1 dose; shelf life 30 days.", "Success": "1 dose; shelf life 7 days.", "Failure": "0 dose; ingredients consumed; pot remains usable after 10-minute cleaning.", "Critical Failure": "0 dose; ingredients consumed; pot fouled and unusable for 1 hour of cleaning."}`

**dose.** `{"weightLb": 0.2, "administration": "Action, one available hand. Drink, or feed to willing/Incapacitated living creature within5ft if it can swallow, per equipment procedure. Unwilling active creature has no free forced-dose permission.", "effect": "Purges Null Veil only. Dose consumed whether or not target is Veiled; no diagnostic refund."}`

**limits.** No Corruption/KT/PT/Hunt/Dissonance/Strain/Exhaustion/Wound/poison/disease cure. No reviewed recipe-count change.

## Persistence ledger

- Every relic, shard card, reflection tab, flame-water flask, planting tray, plant node/bloom/sprig/patch, voting token and one-time chamber reward has one physical/scene identity. Loss, destruction, failed harvest, transfer and depletion never create replacements unless an exact rule above says so.
- Scene actors and projections use their explicit lifecycle; do not import pending bestiary dossiers.
- All elapsed-time and initiative durations use the current combat/action timing interface; initiative changes do not refresh virtual markers or absolute deadlines.
- Character-fiction prompts always retain neutral/decline routes; no real-player personal disclosure is required.

## Remaining boundaries

- Campaign chronology/epoch remains open.
- Hidden Heartcell/Old One/other identities remain open.
- EPI-15–17 remain out of scope.
- Runtime, human playtest, numerical balance, complete whole-game flow and publication remain open.
- Ordinary spell and bestiary reviews retain their actual statuses; this chapter grants no pending content.
