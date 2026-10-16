# Relics, Dungeon Seeds, and Residual Null — Player Chapter (Revision 02)

## Optional NEW provisional EPI-08–14 module

This chapter is a complete playable candidate, not adopted canon. Your Director should use it only when this EPI-08–14 module is deliberately enabled. It does not decide the campaign epoch, reveal unresolved cosmological identities, or grant access to unfinished spell/bestiary/environment/consumable/later-arc material.

## Relic bond

1 uninterrupted active hour with the actual item; not a rest; no check. Item-specific class eligibility still applies. Transfer or separation for10+ minutes ends bond. No universal attunement-slot cap is created.

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

## Dungeon Seeds

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

### 3. Echoless Vault

Inside the vault ordinary sound does not transmit. This is physical acoustic suppression, not blanket antimagic or the full Silenced condition: audible V casting and features requiring an audible performance/hearing path do not function through the suppressed area; writing/signs/mental effects can still work if their own rules allow them. The Wraith hunts heartbeat vibration through connected chamber stone; merely holding still does not stop a heartbeat. The wall inscription can be investigated from the isolated west sill for10 minutes at INT (Investigation) DC14. The seven plates have one fixed sequence; correct latches persist.

### 4. Tessellation Garden

Three rows each present lanes A/B/C. Reading a row marker costs an Action and uses WIS (Perception) or INT (Investigation) DC14. Success identifies that row’s safe lane; failure gives no false answer and you may retry only after 10 uninterrupted minutes studying that row. Entering an unsafe lane triggers DEX DC14; on failure fall10ft to a net, take1d6 bludgeoning and become Prone. Net recovery costs an Action +20ft movement to climb10ft to the row staging strip. The pattern is fixed, so a truthful earlier observation remains truthful. Actual rope/flight/teleport/shapechanging can work if you really have it.

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

## Residual Null Fields

Only a location with an explicitly mapped Null field counts as exposure. A gray glow, the words “Veiled Expanse,” or a realm name by itself does not. The Quiet Well’s active field is the 7.5-ft-radius cylinder around the well; its petition alcove is outside. The Shardpool Veiled Expanse landing cell has no active Null exposure field.

### Null Veil damage

After ordinary mitigation/temp HP, a qualifying packet may reduce a living recipient to 0. If it was positive before the packet and becomes 0, skip damage-caused Instant Death, Wound/Maiming creation, death-save failures and ordinary death; it becomes Stable0 with death successes/failures reset under Core and receives exactly one normal Stable recovery deadline. If it was already Dying0, the packet adds no damage-caused failure but DOES NOT stabilize it, clear counters or change its existing death-save schedule. If already Stable0, it remains Stable and keeps its existing absolute recovery deadline; do not reroll/extend it. If temporary HP absorbs all HP loss and normal HP never reaches0, no zero-state transition occurs.

Companions and created creatures use their real source lifecycles. A qualifying Null packet prevents only the damage-caused lethal/zero transition expressly replaced in the Director lifecycle table; independent duration expiry/dismissal/sacrifice still happens. A would-die protection is not spent if no death trigger occurs. Actual Mage Undying Spellform still triggers when its own “damage reduces you to0 without killing outright” condition is met.

### Shrug Off Empathy

Bonus Action while active and not Incapacitated; CHA save DC15, binary. Suppress Veil until the start of the character's next regular turn in initiative. Outside initiative, suppress for 6 elapsed seconds. During suppression passive Insight and damage conversion are inactive, but the Veil record remains and exposure clocks continue. Apply actual Incapacitated until the end of the character's next regular turn. Outside initiative, 1 elapsed minute. Concentration ends immediately under current Incapacitated rule. After duration, Bonus Action can be attempted again if otherwise legal.

Initiative changes never reset these durations: reviewed virtual turn markers and absolute deadlines are preserved.

### Purging Null Veil

A Veil can be purged only by the listed operative-mask confession route, an actual qualifying EPI-06 Temporary Blessing result, or one real Bittersap antidote dose. Leaving a field does not itself purge Veil.

## Null Flora and Bittersap Antidote

Flora is finite. In the Shardpool’s ten-minute Veiled Expanse visit, entire numbered planting containers may be lifted with an Action and two free hands, then returned as carried gear. This moves the same plant identities; it never copies them or extends planar access. Recognition and harvest can occur later from those exact containers. Failed or critical-failed harvests consume the exact printed node/bloom/patch and never respawn it.

**Bittersap Antidote:** 2 Bittersap parts +1 Echo Lily part +1 pint actual Bastion flame water; 30 uninterrupted active minutes; INT (Herbalism kit) or INT (Alchemist’s supplies) DC15 at completion. Ingredients commit when boiling begins. Success creates one dose; failure consumes ingredients. One dose purges Null Veil only.
