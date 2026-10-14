# Device, Totem and command lifecycle conference

Codex → Calibration Review. This is the next source discussion: **74 Tinker/Shaman passages and three preserved shared-rule paragraphs**. Seventy-three came from the 230-passage lexical inventory. Magnetic Wall is an explicit semantic addition: its operational text describes interception without using the words that matched the earlier searches. The other 157 lifecycle candidates will receive separate review.

Please keep the reply under 18,000 characters. Classify every supplied ID in a compact table, then give shared decisions and counterexamples. Keep every named ability tied to these supplied records or our prior discussions. Clearly label any new integration rule; do not invent additional abilities, spells or imported game rules. This conference does not approve whole cards.

1. **Entity states.** Distinguish functional, disabled, retracted, destroyed, expired and replaced. The Anacite Drone remains at 0 HP until a specific repair/rebuild; timed deployables retain original expiry and spent uses; Totems lose their aura at 0; ordinary standard companions disappear. Does expiry release capacity without creating a destruction event? Which objects persist physically afterward?

2. **Shared commands.** The frozen standard-companion rule gives one shared Bonus Action command and one damaging action per numbered round. Tinker engine1 says one damaging action per command per regular turn; engine6 also limits damaging triggers. Resolve these together for drones, turrets, Scraplings and multiclass companions. Separate support commands, defensive reactions, commanded movement, following and default Dodge. An extra full Action grants no Bonus Action, and extra turns do not reset regular or round allowances. Preserve expressly priced exceptions.

3. **Gadget Sync and multiple devices.** Its triggered shot replaces the ordinary commanded damaging action for that turn. State how an earlier command blocks it, and how using it first affects later damaging or support commands. Rocket Tower's two targets are one activation. Advanced Turret Bay creates two objects, but does not command both automatically. Preserve the precise Shock, Burn and control-module limits.

4. **Maximum and initial HP.** Drone: 5 + actual INT modifier + Tinker level, minimum1. Deployables: 2L, modified by Deployable Expertise where eligible. Totems: 2L and AC12+PB. Decide which values update when level, ability or controller changes and which are creation snapshots. Later capacity gains do not heal under the reviewed maximum-HP rule. Deployable Expertise's wording was outside the earlier 58-source selection, so integrate it explicitly. Objects use no organic Wounds, Stable state or death saves; legal temporary HP remains separate.

5. **Repair and reconstruction.** Functional Field Repair, destroyed-drone ten-minute repair, long-rest rebuild, Snap Rebuild and Repair Pulse are different permissions. At maximum1, a half-HP repair rounds to0: does reconstruction remain nonfunctional, or should an explicitly NEW viable-reconstruction minimum apply? Do not silently import the living-resurrection bridge. Reconfiguration preserves HP fraction: define rounding and viability without inventing damage or resetting spent uses.

6. **Capacity and replacement.** Resolve drone cap and Dual Drone Protocols; deployable slots by level; Advanced Turret Bay's one-slot fallback; Shaman's capacity1 rising to2 at13. The Totem text says a third replaces an existing Totem, but capacity1 also needs a coherent replacement rule. If placement replaces an old anchor, distinguish ending from hostile destruction. Echo costs an additional slot and cannot be created without capacity. Now decide whether destroying, expiring or replacing a parent ends its Echo, using exact evidence or an explicitly discussed new rule.

7. **Totem concentration and clocks.** All Totems share one concentration burden. Losing it ends all auras. State whether inert anchors remain and whether any repair can reactivate an ended effect. Totem movement costs a Bonus Action, follows an open route and preserves range, duration and pulse budgets. Non-Renewal Totems need no healing upkeep. Echo inherits the parent's remaining duration. Movement, repair or retraction must not silently restart any clock.

8. **Dissonance disablement.** The protected route disables movement, attacks, auras and triggers while duration keeps ticking. Field Repair names a functional damaged machine, but also expressly clears this disabled state: can it clear a disabled full-HP device without restoring HP? The tools option costs ten minutes and1RP. Clearing disabled at a completed short rest must not repair destruction, revive expiry or recharge uses.

9. **Destruction and salvage.** Define the qualifying hostile destruction event and exclude deliberate sacrifice, friendly damage, copies and secondary explosions where stated. Efficient Recycling consumes usable debris and cannot refund more than the actual deployment cost. Determine whether it competes with Scrap Salvage/Reaper for the same material and whether Volatile Components can coexist. Preserve object identity and used destruction entitlements through Snap Rebuild/Reconfiguration; prevent repeated debris, refund or replacement chains.

10. **Sacrifice and interception.** Remote Detonation, Overload Core and Catastrophic Overload end the device and prohibit additional destruction chains. Volatile Injection is a direct device-HP cost, with its strict survival requirement. Emergency Protocols retains the reviewed transfer rules. Magnetic Wall was absent from the earlier 39-record redirection review: decide its transfer stage, amount, type, second-defense restrictions and object consequences explicitly, then add a new source binding.

11. **Target eligibility and defenses.** The Drone is a construct with specific immunities, not universal condition immunity. Totems have their own object immunities. Does “vulnerable to ordinary weapon and other damage” mean ordinarily susceptible or double damage? Clarify without importing another game's terminology. A magical Totem is not automatically a mechanical device eligible for Tinker repairs. Keep organic constructs, machines and magical anchors distinct unless a source connects them.

12. **Reference model and remaining evidence.** Propose entity, capacity, command and debris records, then test maximum1, already-reused slots, expired reconstruction, both anchors destroyed, disabled full HP, lack of line of effect, multiple owners and extra turns. Identify any additional exact source needed. Other classes, items, spells and broader companion life remain open.

## Exact source procedures

### shaman.engine[0]

data/public/class_playtests/shaman.json

{
  "text": "Wisdom is the class ability. Choose Elemental Affinity automatically at 1: Fire, Ice, Air or Earth. Spellcasting/RP remain separate from Totem objects and flasks. Totem capacity 1, rises 2 at 13; any third replaces one of your existing totems. A totem is a visible Tiny magical object: AC 12+PB, HP 2 L, immobile, immune to poison/psychic/conditions, vulnerable to ordinary weapon and other damage. At 0 HP its aura ends. A new totem appears within 30 ft; cannot occupy a creature's space, serve as a bridge, trap a creature without a save or move through walls."
}

### shaman.engine[1]

data/public/class_playtests/shaman.json

{
  "text": "Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack."
}

### shaman.engine[2]

data/public/class_playtests/shaman.json

{
  "text": "On your turn you may spend Bonus Action to move one totem up to 15 ft along unobstructed ground, remaining within 60 ft. This competes with healing maintenance, companion commands and advanced flasks. Moving an aura over a creature cannot trigger its once/round effect repeatedly. Totem destruction creates no resource return. Once per round, the first ordinary spell cast while inside your own active totem aura generates 1 less Dissonance, minimum 0; no RP reduction."
}

### shaman.engine[5]

data/public/class_playtests/shaman.json

{
  "text": "Choose Fire/Ice/Air/Earth bonuses through affinity card; Ember/Cold/Shock damage are fire/cold/lightning, Earth uses bludgeoning. Summoned elemental spirits use one standard companion each, maximum one normally; Elemental Chorus expressly summons a package of 4 but all share one Bonus Action command and a printed combined pulse. Companions cannot generate RP, trigger flask refunds or create corpse/kill farms."
}

### shaman.engine[6]

data/public/class_playtests/shaman.json

{
  "text": "Bloodcaller at Hero 10 transforms permanently into Hagraven, with the player choosing this class path and its stated loss of ordinary Shaman spellcasting. It does NOT lose its RP reservoir: printed Hagraven/Totem techniques still pay RP, but it cannot cast ordinary Shaman spells or advanced magical flasks. It retains prior totem/technique selections. The change is a class choice, not permission for involuntary player-character conversion; ancestry identity and player control remain. At long rest it can prepare mundane flasks only if Base Flask Use is known."
}

### shaman.base.totem-casting

data/public/class_playtests/shaman.json

{
  "name": "Totem Casting",
  "activation": "Action",
  "cost": "2 RP; Renewal upkeep 1 RP+Bonus Action",
  "rangeAndTarget": "One totem within 30 ft with 15 ft aura",
  "duration": "3 of your turns",
  "frequency": "Capacity 1, 2 at 13",
  "effect": "Place one Flame/Stone/Frost/Spirit/Renewal totem using the engine's exact profile. All your totems share concentration. Respect 3 creature aura/pulse limit; same-stat bonuses do not stack. Replacing a totem ends it without refund."
}

### shaman.base.spirit-shock

data/public/class_playtests/shaman.json

{
  "name": "Spirit Shock",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "One enemy within 60 ft",
  "duration": "Instant",
  "frequency": "Recharge 2",
  "effect": "Target makes DEX save: S d8 affinity damage, half on success. Affinity rider applies once; this printed technique is not an ordinary spell, cannot Overcast and does not generate a flask or totem."
}

### shaman.arch.extended-totem-duration

data/public/class_playtests/shaman.json

{
  "name": "Extended Totem Duration",
  "activation": "Passive",
  "cost": "0; full upkeep for extra Renewal pulse",
  "rangeAndTarget": "One of your totems",
  "duration": "Maximum 4 of your turns",
  "frequency": "Continuous",
  "effect": "Totems last 1 extra turn. Renewal may have a fourth pulse only if you pay Bonus Action+1 RP on that turn; no fifth pulse and no automatic free healing. Concentration still required."
}

### shaman.arch.spirit-cache

data/public/class_playtests/shaman.json

{
  "name": "Spirit Cache",
  "activation": "Triggered",
  "cost": "1 short-rest use",
  "rangeAndTarget": "One flask/to-tem effect you directly used",
  "duration": "Stored until encounter end",
  "frequency": "1/short rest",
  "effect": "Store its profile, not an active copy. On a later turn use normal Action/Bonus Action and pay all RP and a new flask unit or full totem cost to repeat it. Add 1d6 to one numerical damage/heal amount; no copy of refund/limited use."
}

### shaman.arch.totem-pulse

data/public/class_playtests/shaman.json

{
  "name": "Totem Pulse",
  "activation": "Passive",
  "cost": "1 RP optional",
  "rangeAndTarget": "Up to 3 creatures inside newly placed non-healing totem",
  "duration": "Instant",
  "frequency": "Once/turn",
  "effect": "On placement pay 1 RP: allies gain M temporary HP OR enemies make DEX save for S affinity damage, half on success. No immediate second Renewal healing pulse, no repeat from moving the totem."
}

### shaman.arch.spirit-saturation

data/public/class_playtests/shaman.json

{
  "name": "Spirit Saturation",
  "activation": "Triggered",
  "cost": "1 long-rest use",
  "rangeAndTarget": "One non-Renewal totem you place",
  "duration": "Normal duration",
  "frequency": "1/long rest",
  "effect": "Waive its 2 RP placement cost once. Still use Action, concentration, capacity and any added costs. Cannot create a healing totem or be cached/refunded to generate more free casts."
}

### shaman.arch.elemental-channeling

data/public/class_playtests/shaman.json

{
  "name": "Elemental Channeling",
  "activation": "Bonus Action",
  "cost": "2 RP",
  "rangeAndTarget": "Self",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 3",
  "effect": "Embody affinity: gain+10 ft Speed and once/turn add 1d4 affinity damage to a weapon hit. Fire/cold/lightning/bludgeoning by affinity. This concentration replaces your totem burden, so it is a tactical alternative."
}

### shaman.arch.ancestral-guardian

data/public/class_playtests/shaman.json

{
  "name": "Ancestral Guardian",
  "activation": "Reaction",
  "cost": "2 RP",
  "rangeAndTarget": "Ally within 30 ft being damaged",
  "duration": "One damage instance",
  "frequency": "Recharge 3",
  "effect": "A guardian prevents S d8+M damage, minimum 0. It then vanishes and creates no companion action, corpse or refund. Cannot prevent sacrifice/trauma or redirect prevented damage into another trigger."
}

### shaman.arch.elemental-surge

data/public/class_playtests/shaman.json

{
  "name": "Elemental Surge",
  "activation": "Bonus Action",
  "cost": "2 RP",
  "rangeAndTarget": "One active totem within 60 ft",
  "duration": "Until start next turn",
  "frequency": "Recharge 3",
  "effect": "Choose one: aura radius+5 ft OR numerical flat benefit improves by 1. Renewal instead adds M HP to its next paid pulse, once, without adding a pulse. Same-name/stat stacking rules remain."
}

### shaman.hero.theurgist.echo-totem

data/public/class_playtests/shaman.json

{
  "name": "Echo Totem",
  "activation": "Triggered",
  "cost": "1 additional RP",
  "rangeAndTarget": "Adjacent empty space within 5 ft of newly placed totem",
  "duration": "Same remaining duration",
  "frequency": "Once/placement",
  "effect": "Create a weak echo anchor of that totem. It counts toward capacity; if no space in capacity, cannot create it. Its radius 10 ft and numerical bonuses/healing are half, rounded down. Shared concentration/upkeep and same-name nonstacking prevent double healing."
}

### shaman.hero.theurgist.elemental-harmony

data/public/class_playtests/shaman.json

{
  "name": "Elemental Harmony",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your summoned elemental",
  "duration": "Summon duration",
  "frequency": "Continuous",
  "effect": "Add class level to its maximum/current HP on creation and 1 turn duration, maximum 4 turns for class summons. Cannot extend once/day Chorus beyond 4 turns or restore an existing creature's lost HP."
}

### shaman.hero.theurgist.spiritual-resonance

data/public/class_playtests/shaman.json

{
  "name": "Spiritual Resonance",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Two of your active totems within 10 ft of one another",
  "duration": "While placement condition holds",
  "frequency": "Continuous",
  "effect": "Their aura radii increase 5 ft. No extra targets or extra pulses and overlapping same-name benefits do not stack. One totem and its echo still use normal capacity."
}

### shaman.hero.theurgist.summon-ice-wisp

data/public/class_playtests/shaman.json

{
  "name": "Summon Ice Wisp",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "One spirit in empty space within 30 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 4",
  "effect": "Summon standard Ice Wisp with fly 30 ft. Commanded attack deals cold; on hit target STR save or Speed 0 until end its next turn. No whole-turn freezing, bonus independent spells or multiple companion attacks."
}

### shaman.hero.theurgist.summon-airling

data/public/class_playtests/shaman.json

{
  "name": "Summon Airling",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "One spirit within 30 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 4",
  "effect": "Summon standard Airling with fly 40 ft. Commanded attack deals lightning; on hit target CON save or loses Reactions until end its next turn. Failure by 10 also Stunned, subject to the shared hard-denial guard across all the Shaman’s features. Companion Stun counts as the Shaman’s denial; if the target already suffered that denial this encounter, only damage and Reaction loss resolve. One shared companion command."
}

### shaman.hero.theurgist.summon-cinderflame

data/public/class_playtests/shaman.json

{
  "name": "Summon Cinderflame",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "One spirit within 30 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 4",
  "effect": "Summon standard Cinderflame. Commanded hit deals fire plus Burn 1d4 next target turn. On destruction only (not dismissal), up to 3 enemies within 5 ft make DEX save for S d4 fire, half. Explosion creates no further death/resource triggers."
}

### shaman.hero.theurgist.summon-stonekin

data/public/class_playtests/shaman.json

{
  "name": "Summon Stonekin",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "One spirit within 30 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 4",
  "effect": "Summon standard Stonekin. Command chooses bludgeoning attack with STR save or Prone on hit, OR gives up to 3 adjacent allies reduction 2 until start next turn. No simultaneous attack and protection command."
}

### shaman.hero.theurgist.elemental-chorus

data/public/class_playtests/shaman.json

{
  "name": "Elemental Chorus",
  "activation": "Action",
  "cost": "8 RP; 1 long-rest use",
  "rangeAndTarget": "Four spirits in 10 ft-radius zone within 30 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "1/long rest",
  "effect": "Summon a single Chorus package: four visible spirits share HP 4 L, AC 12+PB, immobile. Bonus Action command pulses up to 3 enemies: DEX save S d6 chosen affinity damage half; one failed target Speed-10 ft until end next turn. Four spirits do not make four separate attacks."
}

### shaman.hero.soothsayer.divining-totem

data/public/class_playtests/shaman.json

{
  "name": "Divining Totem",
  "activation": "Action",
  "cost": "3 RP",
  "rangeAndTarget": "One divining totem within 30 ft; observed enemy in aura",
  "duration": "3 of your turns",
  "frequency": "Capacity and concentration as totems",
  "effect": "Each own-turn start choose one visible enemy in 15 ft aura. First ally attack against it before your next turn gains+1 to hit; first attack it makes has-1. Predicts immediate intent, not guaranteed future actions; totem has ordinary object stats."
}

### shaman.hero.soothsayer.omen-loop

data/public/class_playtests/shaman.json

{
  "name": "Omen Loop",
  "activation": "Action",
  "cost": "Normal RP+2 RP; fresh flask if required; 1 long-rest use",
  "rangeAndTarget": "Your own qualifying effect used within previous 2 turns",
  "duration": "Normal effect duration",
  "frequency": "1/long rest",
  "effect": "Repeat one non-Finale, non-resource-restoring class flask/totem effect with normal targets and full costs. It replaces the current Action; cannot repeat another repeat, regain per-rest uses or exceed totem capacity. If effect required a flask, consume one now."
}

### shaman.hero.bloodcaller.hagraven-form

data/public/class_playtests/shaman.json

{
  "name": "Hagraven Form",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Permanent while Bloodcaller",
  "frequency": "Automatic on Hero entry",
  "effect": "Become Hagraven: retain player control/mental stats, light-armor use and ordinary movement; claws are finesse 1d6 slashing, darkvision 60 ft and poison resistance. Lose ordinary Shaman spellcasting/advanced magical flasks; retain RP for printed techniques and totems. No free flight or hidden monster stat block."
}

### shaman.hero.bloodcaller.blood-feast

data/public/class_playtests/shaman.json

{
  "name": "Blood Feast",
  "activation": "Triggered",
  "cost": "1 RP",
  "rangeAndTarget": "Self at start regular turn; hostile bleeding creature within 10 ft",
  "duration": "Instant",
  "frequency": "Once/turn",
  "effect": "Pay 1 RP to regain M HP. Bleeding allies, summons or staged captives cannot qualify. No healing while Downed; secondary heal creates no damage/resource triggers."
}

### shaman.hero.bloodcaller.blight-totem

data/public/class_playtests/shaman.json

{
  "name": "Blight Totem",
  "activation": "Action",
  "cost": "3 RP",
  "rangeAndTarget": "Totem within 30 ft; 15 ft aura affecting all creatures",
  "duration": "3 of your turns",
  "frequency": "Ordinary totem capacity/concentration",
  "effect": "HP healing received inside aura is halved, rounding down, including allies and you. Nonstacking with another healing reduction; temporary HP unaffected. This totem has standard object stats and grants no free damage/healing."
}

### shaman.supplement.elder-spirit-accord-new-hero-capstone

data/public/class_playtests/shaman.json

{
  "name": "Elder Spirit Accord — new Hero capstone",
  "activation": "Triggered",
  "cost": "1 long-rest use",
  "rangeAndTarget": "Your chosen Hero ultimate",
  "duration": "One activation",
  "frequency": "1/long rest",
  "effect": "When starting Elemental Chorus, Omen Loop or Bloodroot Trail, reduce its RP cost by 3, minimum 1, and add M to one damage/healing roll from that use. You must know that ability and still spend its own limited use. If you do not know it, instead reduce one known Hero technique's RP cost by 3, minimum 1. No extra duration, flask, totem, command or repeated cast."
}

### tinker.engine[0]

data/public/class_playtests/tinker.json

{
  "text": "Intelligence governs class DC/M, device attacks use PB+INT; Dexterity governs personal ranged weapons. Hit Die d8, light armor, shortbows/crossbows/simple weapons, tinkers tools and alchemist supplies. Technology is fictional equipment. Ordinary Tinker spells use RP/Dissonance; mundane bombs/devices with printed RP fuel costs are class techniques and do not separately count as spell casts."
}

### tinker.engine[1]

data/public/class_playtests/tinker.json

{
  "text": "At 1 automatically own one Anacite Drone: AC 13+INT modifier, HP 5+INT modifier+class level (minimum 1), flight 30 ft, ranged bolt 60 ft attack PB+INT for 1d6 piercing. Bonus Action commands one move and one attack or named module action; otherwise it Dodges and may follow you. On bolt hit roll d4; on 4 target CON save or cannot take Reactions through end next turn (Shock, no automatic Stun). All drones/turrets/scraplings share ONE damaging action per Bonus Action command per regular turn unless a card explicitly supplies a priced extra attack. No autonomous barrage. Drone is a construct, not immune to all conditions; poison/psychic immunity, no charm. Carry/retract it in 1 minute; no pocket extra world or passenger flight."
}

### tinker.engine[2]

data/public/class_playtests/tinker.json

{
  "text": "A destroyed drone remains 0 HP until repaired for 1 RP and 10 minutes with tools to half HP, once/short rest, or rebuilt during long rest to full. Ordinary repairing does not recharge devices, grant organic healing or trigger destruction bonuses. At 13 Dual Drone Protocols automatically chooses on each long rest either 2 basic drones each with one module, or one drone with 2 distinct modules. Still one command budget. Never more than 2 drones."
}

### tinker.engine[3]

data/public/class_playtests/tinker.json

{
  "text": "At 5 automatically gain one module slot; change module during long rest. Offensive: Burn Injector first bolt hit/turn causes 1d4 fire next 2 target turns; Poison Vents d4=4 on hit CON save or-1 attack rolls until end next turn; Concussive Bolt d4=4 on hit CON save or Stunned until end next turn, once/target/encounter shared denial guard and 1/short-rest successful Stun. Defensive: Target Taunter command action once/encounter WIS save one foe 30 ft or disadvantage attacking others until end next turn; Energy Shield command gives adjacent ally+2 AC until start next turn; Smoke Cloud command once/encounter creates 5 ft radius opaque smoke centered drone until start next turn. Support: Ammo Dispenser adjacent allies first ranged hit/turn+1 damage; Target Scanner command mark 1 visible foe 60 ft first ally attack before start next turn+1 hit; Tether Grappler command once/encounter pulls 1 willing ally 15 ft within 30 ft without opportunity attacks along open route."
}

### tinker.engine[5]

data/public/class_playtests/tinker.json

{
  "text": "Advanced bomb profiles replace basic rider: Thermobaric fire pushes 5 ft on failed STR save after damage; Cryo cold on failed DEX also Speed 0 until end next turn and d2=2 ignores 1 flat DR against this bomb; Shock lightning CON instead DEX, failure prevents verbal spellcasting until end next turn (construct instead loses Reactions), shared hard-denial guard; Glue no damage, 15 ft square difficult terrain 3 rounds and entering/starting DEX save or Speed-15 ft until end turn, once per creature/round. Overload Core destroys one commanded drone within 30 ft as part Action bomb, DEX save 2d6 lightning and no Reactions until end next turn on failure, half damage on success. Consumes stock/allowance; no further destruction proc."
}

### tinker.engine[6]

data/public/class_playtests/tinker.json

{
  "text": "Deployable slots start 1 at 6, 2 at 13, 3 at 17, separate from drone cap. Deploy Action 2 RP within 15 ft, fixed ground, AC 12+PB HP 2 L, duration 3 rounds, concentration not required; destroyed do not refund fuel. All share command budget. Sentry and Net require their cards. Additional engine profiles unlocked 6: Rocket Tower commanded attack 60 ft target DEX save S d6 fire/half success to up to 2 creatures within 5 ft, maximum 3 shots; Decoy Dummy one foe 30 ft WIS save when deployed or disadvantage on next attack against others, destruction S fire to one adjacent enemy no chain; Blast Wall 10-by 5 ft blocks LOS and movement, climb cost 10 ft. Net Trap one enemy entry STR save or Restrained, end turn repeat/Action escape DC, 3 round max then ends. One only fires when commanded except nonattack trap/decoy trigger; command budget limits damaging triggers too."
}

### tinker.engine[7]

data/public/class_playtests/tinker.json

{
  "text": "Base 1–2, Mechanist Arch 3–9, then Artificer/Techsmith/Warmachine Hero 10–20. Upgrade Slot 5 is automatic; Sentry and Net minimum 6, Remote Detonation 9. There is no source automatic Arch capstone. Mech Overdrive 20 is automatic: once/long rest when deploying choose one device whose duration becomes encounter end (maximum 1 minute), still command dependent, slot limited and destructible. No infinite pulses: healing effects keep original pulse cap and all per-use costs remain. Protected magic interface: once per short rest, as a Bonus Action route up to 2 current Dissonance into one of your active devices within 30 ft. Reduce Dissonance by that amount; the device is disabled and cannot move, attack, emit an aura or trigger effects until repaired or your next completed short rest. Its duration keeps ticking. Repair with an Action and 1 RP using Field Repair, or with 10 minutes and 1 RP using tinkers tools. No RP is created and no Refrain counter resets."
}

### tinker.base.mechanical-aptitude

data/public/class_playtests/tinker.json

{
  "name": "Mechanical Aptitude",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Mechanical devices you examine",
  "duration": "While using tools",
  "frequency": "Continuous",
  "effect": "Advantage on checks to understand, repair or disable mechanisms. Requires appropriate access and tools; no automatic control of enemy constructs."
}

### tinker.base.explosive-handling

data/public/class_playtests/tinker.json

{
  "name": "Explosive Handling",
  "activation": "Passive",
  "cost": "One bomb and encounter allowance",
  "rangeAndTarget": "Your bomb throw",
  "duration": "Instant",
  "frequency": "Once/own turn",
  "effect": "Throw a known prepared bomb as Bonus Action instead of Action. Removes ordinary accidental misfire, not Warmachine risk or enemy defenses. Cannot command a device with the same Bonus Action."
}

### tinker.base.quick-fingers

data/public/class_playtests/tinker.json

{
  "name": "Quick Fingers",
  "activation": "Bonus Action",
  "cost": "0",
  "rangeAndTarget": "One noncombat mechanism touched",
  "duration": "One manipulation",
  "frequency": "Once/turn",
  "effect": "Open unlocked latch, operate simple switch or retrieve a carried gadget. Does not activate damaging/healing devices, disarm a trap, reload every weapon or add another Bonus Action."
}

### tinker.base.deploy-anacite-drone

data/public/class_playtests/tinker.json

{
  "name": "Deploy Anacite Drone",
  "activation": "Action",
  "cost": "0 if functional; repairs as engine",
  "rangeAndTarget": "Your carried drone within 5 ft",
  "duration": "Until retracted/destroyed",
  "frequency": "One deployment per drone",
  "effect": "Drone is automatic class engine. Selecting this card instead upgrades deployment to Bonus Action and permits 5 ft free initial placement. No free attacks, repair or extra drone."
}

### tinker.base.field-repair

data/public/class_playtests/tinker.json

{
  "name": "Field Repair",
  "activation": "Action",
  "cost": "1 RP",
  "rangeAndTarget": "One construct/device touched",
  "duration": "Instant",
  "frequency": "Recharge 2",
  "effect": "Restore S d8+M HP, up to maximum, to functional damaged machine. Cannot revive destroyed objects, heal organic allies, reset duration or recharge limited uses. If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses."
}

### tinker.base.analyze-weakness

data/public/class_playtests/tinker.json

{
  "name": "Analyze Weakness",
  "activation": "Bonus Action",
  "cost": "0",
  "rangeAndTarget": "Visible target within 60 ft",
  "duration": "Until end next turn",
  "frequency": "Recharge 3",
  "effect": "Identify one visibly demonstrated damage resistance. Your next bomb/device damage against it ignores 2 flat DR, not resistance/immunity. No invented weakness or automatic secret knowledge."
}

### tinker.base.jury-rig

data/public/class_playtests/tinker.json

{
  "name": "Jury-rig",
  "activation": "Action",
  "cost": "1 RP",
  "rangeAndTarget": "One willing ally weapon/device touched",
  "duration": "3 rounds",
  "frequency": "Recharge 3",
  "effect": "Choose+1 first attack roll/turn or+5 ft device movement. One modification per item, no stack. Does not change weapon category, spell function, summon limit or command budget."
}

### tinker.arch.enhanced-drone-control

data/public/class_playtests/tinker.json

{
  "name": "Enhanced Drone Control",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your drones",
  "duration": "While active",
  "frequency": "Continuous",
  "effect": "Gain+1 attack roll and can follow simple move/dodge commands while within 120 ft. Attacks still require your Bonus Action and line of effect; no independent turn."
}

### tinker.arch.pet-upgrade-slot

data/public/class_playtests/tinker.json

{
  "name": "Pet Upgrade Slot",
  "activation": "Long rest choice",
  "cost": "0",
  "rangeAndTarget": "One drone module slot",
  "duration": "Until next reconfiguration",
  "frequency": "Automatic engine at 5",
  "effect": "Choose one of 9 bounded modules in engine. This automatic unlock is not a selected skill. At 13 use Dual Drone Protocols, still shared command budget."
}

### tinker.arch.deployable-expertise

data/public/class_playtests/tinker.json

{
  "name": "Deployable Expertise",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your deployables",
  "duration": "While deployed",
  "frequency": "Continuous",
  "effect": "Gain M maximum/initial HP and+1 AC. Does not heal existing damage when moved or grant additional slots. Drones excluded unless another card says otherwise."
}

### tinker.arch.remote-detonation

data/public/class_playtests/tinker.json

{
  "name": "Remote Detonation",
  "activation": "Bonus Action",
  "cost": "1 RP; sacrifice one device",
  "rangeAndTarget": "Device within 60 ft, 10 ft radius up to 3 creatures",
  "duration": "Instant",
  "frequency": "Recharge 3",
  "effect": "Destroy your device; DEX save 2 S d6 force, half success. Failed save also no Reactions until end next turn. Cannot trigger Volatile Components/Scrap Reaper or another destruction/copy chain; no resource refund."
}

### tinker.arch.deploy-sentry-turret

data/public/class_playtests/tinker.json

{
  "name": "Deploy Sentry Turret",
  "activation": "Action",
  "cost": "2 RP; one slot",
  "rangeAndTarget": "Empty ground within 15 ft",
  "duration": "3 rounds",
  "frequency": "Recharge 2",
  "effect": "Deploy Sentry engine profile: commanded attack range 25 ft PB+INT for 1d6 piercing. No auto fire, extra Bonus Action or shared budget exception. Durability AC 12+PB HP 2 L before upgrades."
}

### tinker.arch.deploy-net-trap

data/public/class_playtests/tinker.json

{
  "name": "Deploy Net Trap",
  "activation": "Action",
  "cost": "2 RP; one slot",
  "rangeAndTarget": "One 5 ft square within 15 ft",
  "duration": "3 rounds or trigger",
  "frequency": "Recharge 2",
  "effect": "Deploy visible Net Trap. First enemy entry STR save or Restrained, repeat end turn or Action escape against DC. Target Huge+instead speed-10 ft. No damage or continued rearming; ends after one creature escapes."
}

### tinker.arch.overcharge

data/public/class_playtests/tinker.json

{
  "name": "Overcharge",
  "activation": "Bonus Action",
  "cost": "1 RP",
  "rangeAndTarget": "One device within 30 ft",
  "duration": "Until end next turn",
  "frequency": "Recharge 3",
  "effect": "Next damaging activation adds S d6 to one target. One pending overcharge, no stacking, does not command device or grant attack. If device expires first cost lost."
}

### tinker.arch.recalibrate

data/public/class_playtests/tinker.json

{
  "name": "Recalibrate",
  "activation": "Bonus Action",
  "cost": "0",
  "rangeAndTarget": "One drone; one visible enemy 60 ft",
  "duration": "Until end next turn",
  "frequency": "Recharge 2",
  "effect": "Drone's next attack against chosen enemy has advantage. Still needs separate command; no automatic shot, enemy type wide permanent buff or crit conversion."
}

### tinker.arch.emergency-protocols

data/public/class_playtests/tinker.json

{
  "name": "Emergency Protocols",
  "activation": "Reaction",
  "cost": "1 encounter use",
  "rangeAndTarget": "Drone within 10 ft when attack hits you",
  "duration": "One hit",
  "frequency": "1/encounter",
  "effect": "Drone intercepts: reduce damage to you by S+M and takes same amount unmitigated. It must be active/conscious. Does not redirect again or trigger retaliation loops."
}

### tinker.hero.artificer.protective-programming

data/public/class_playtests/tinker.json

{
  "name": "Protective Programming",
  "activation": "Reaction",
  "cost": "1 RP",
  "rangeAndTarget": "Drone adjacent to ally hit by attack",
  "duration": "One hit",
  "frequency": "Once/round",
  "effect": "Drone grants ally S+M temporary HP before hit resolves. No heal or reversal of hit; max one protected ally, normal temporary HP nonstacking."
}

### tinker.hero.artificer.efficient-power-cells

data/public/class_playtests/tinker.json

{
  "name": "Efficient Power Cells",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your nonhealing deployables",
  "duration": "Deployment",
  "frequency": "Continuous",
  "effect": "A 3 round device lasts 4 rounds (50%rounded down). Healing pulse count unchanged, no extra ammunition or free commands. Does not extend spell concentration."
}

### tinker.hero.artificer.nano-aegis-drone

data/public/class_playtests/tinker.json

{
  "name": "Nano-Aegis Drone",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "Your drone within 15 ft",
  "duration": "3 rounds",
  "frequency": "Recharge 4",
  "effect": "Replace bolts with support mode. Each Bonus Action command pay 1 RP choose one ally 30 ft to heal S d6+M or grant 2 S+Mtemp HP. Maximum 3 pulses; organic healing explicit exception, no attack during mode."
}

### tinker.hero.artificer.repair-pulse

data/public/class_playtests/tinker.json

{
  "name": "Repair Pulse",
  "activation": "Action",
  "cost": "3 RP",
  "rangeAndTarget": "Upto 3 friendly devices within 30 ft",
  "duration": "Instant; AC until start next turn",
  "frequency": "1/short rest",
  "effect": "Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets."
}

### tinker.hero.artificer.restoration-field

data/public/class_playtests/tinker.json

{
  "name": "Restoration Field",
  "activation": "Action",
  "cost": "3 RP start; 1 RP maintenance; one slot",
  "rangeAndTarget": "10 ft radius within 30 ft",
  "duration": "Maximum 3 pulses",
  "frequency": "Recharge 4",
  "effect": "Concentration. Initial and paid Bonus Action pulse heals up to 3 living allies/devices S d6 HP. Devices must not be destroyed. Same creature once/round, no extra autonomous healing or longer Efficient Cells."
}

### tinker.hero.artificer.overload-suppression

data/public/class_playtests/tinker.json

{
  "name": "Overload Suppression",
  "activation": "Action",
  "cost": "3 RP",
  "rangeAndTarget": "One enemy construct/device within 30 ft",
  "duration": "Until end next target turn",
  "frequency": "1/short rest",
  "effect": "CON save or fails its next Reaction and has disadvantage on attacks. On failure by 5 also Stunned, shared hard-denial guard. No automatic permanent deactivation, hacking allegiance or ignoring boss immunity."
}

### tinker.hero.techsmith.automated-field-kit

data/public/class_playtests/tinker.json

{
  "name": "Automated Field Kit",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "While known",
  "frequency": "Continuous",
  "effect": "Bomb stock cap/refill+1; encounter allowance unchanged. Reduce deployable card recharge by 1 minimum 1, on setting counter only. Never refresh rest uses or trigger repeated counter reductions."
}

### tinker.hero.techsmith.enhanced-targeting

data/public/class_playtests/tinker.json

{
  "name": "Enhanced Targeting",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your turret attacks",
  "duration": "While active",
  "frequency": "Continuous",
  "effect": "Gain+1 to hit. Does not stack with Enhanced Drone Control if profile ever counts both, and does not impose save penalties."
}

### tinker.hero.techsmith.efficient-recycling

data/public/class_playtests/tinker.json

{
  "name": "Efficient Recycling",
  "activation": "Triggered",
  "cost": "One destroyed device remains",
  "rangeAndTarget": "Your destroyed device within reach",
  "duration": "After combat 1 minute",
  "frequency": "1/short rest",
  "effect": "Recover 1 RP spent on deploying it, never more than its actual paid cost. Deliberate sacrifice or copy does not qualify. Consume usable debris; no repeated salvage from same object."
}

### tinker.hero.techsmith.technical-mastery

data/public/class_playtests/tinker.json

{
  "name": "Technical Mastery",
  "activation": "Triggered",
  "cost": "1 RP",
  "rangeAndTarget": "Your damaging device activation",
  "duration": "One target",
  "frequency": "Once/own turn",
  "effect": "After damage rolld 10; on 10 you may pay 1 RP to add half its unmodified damage dice total rounded down to one target. No second activation, commands, procs, resources or healing duplication."
}

### tinker.hero.techsmith.advanced-turret-bay

data/public/class_playtests/tinker.json

{
  "name": "Advanced Turret Bay",
  "activation": "Action",
  "cost": "4 RP; two slots",
  "rangeAndTarget": "Two empty ground spaces within 15 ft",
  "duration": "3 rounds",
  "frequency": "Recharge 4",
  "effect": "Requires 2 available slots (normally 13); if only one, deploy one for 2 RP. Sniper command attack 90 ft S d6 piercing; Burst command DEX save S d4 piercing to 2 targets within 5 ftat 30 ft. One commanded turret per Bonus Action, not both automatically."
}

### tinker.hero.techsmith.gadget-sync-protocol

data/public/class_playtests/tinker.json

{
  "name": "Gadget Sync Protocol",
  "activation": "Triggered",
  "cost": "1 RP",
  "rangeAndTarget": "One turret within 60 ft after your bomb throw",
  "duration": "One attack",
  "frequency": "Once/own turn",
  "effect": "Turret makes one ordinary shot at surviving bomb target. Replaces its normal commanded damaging action for that turn; cannot combine with another device attack from Bonus Action. No chains or additional bombs."
}

### tinker.hero.techsmith.snap-rebuild

data/public/class_playtests/tinker.json

{
  "name": "Snap Rebuild",
  "activation": "Bonus Action",
  "cost": "2 RP; 1 encounter use",
  "rangeAndTarget": "One destroyed device/drone within 15 ft",
  "duration": "Remaining original duration",
  "frequency": "1/encounter",
  "effect": "Restore half its maximum HP. Uses original slot and original expiry; expired devices ineligible. Does not reset limited uses, modules, Overdrive, destruction triggers or bomb stock."
}

### tinker.hero.techsmith.reconfiguration

data/public/class_playtests/tinker.json

{
  "name": "Reconfiguration",
  "activation": "Action",
  "cost": "1 RP",
  "rangeAndTarget": "One deployed device within 15 ft",
  "duration": "Remaining duration",
  "frequency": "Recharge 3",
  "effect": "Change between known nonhealing profiles using same HP fraction, slot, expiry and spent uses. Cannot turn a 1 slot device into two, refill ammo, reset trap, create fresh death trigger or morph drone into free bomb."
}

### tinker.hero.warmachine.malfunction-field

data/public/class_playtests/tinker.json

{
  "name": "Malfunction Field",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Enemy within 5 ft of your device",
  "duration": "While device active",
  "frequency": "Once/round total",
  "effect": "First spell attack by one enemy has disadvantage. Multiple devices do not multiply effect; area/spell-saves unchanged. Does not create antimagic zone."
}

### tinker.hero.warmachine.volatile-components

data/public/class_playtests/tinker.json

{
  "name": "Volatile Components",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "One device destroyed by enemy; one enemy within 5 ft",
  "duration": "Instant",
  "frequency": "Once/round",
  "effect": "Deal S fire to that enemy. Deliberate sacrifices, copied objects, friendly damage and secondary explosions cannot trigger. No other procs/resources from damage."
}

### tinker.hero.warmachine.scrap-salvage

data/public/class_playtests/tinker.json

{
  "name": "Scrap Salvage",
  "activation": "Action",
  "cost": "1 RP; enemy-destroyed device debris",
  "rangeAndTarget": "Empty space within 5 ft of debris",
  "duration": "3 rounds",
  "frequency": "1/encounter",
  "effect": "Create one Scrapling AC 12 HP L Speed 20 ft, commanded melee attack PB+INT for 1d6 bludgeoning. Counts as deployable slot/shared command. Consumed debris cannot be salvaged again; cannot spawn its own replacement."
}

### tinker.hero.warmachine.boomcore-drone

data/public/class_playtests/tinker.json

{
  "name": "Boomcore Drone",
  "activation": "Bonus Action",
  "cost": "2 RP",
  "rangeAndTarget": "One drone within 30 ft",
  "duration": "3 rounds",
  "frequency": "Recharge 4",
  "effect": "Commanded bolts add 1d6 fire and on hit STR save or push 5 ft. Still one command and normal attack budget; no free activation attack or unlimited stacking."
}

### tinker.hero.warmachine.scrap-reaper

data/public/class_playtests/tinker.json

{
  "name": "Scrap Reaper",
  "activation": "Reaction",
  "cost": "2 RP; one destroyed enemy-hit device",
  "rangeAndTarget": "Debris within 30 ft",
  "duration": "Until end next turn",
  "frequency": "1/short rest",
  "effect": "Create one Scrapling Speed 30, AC 12 HP L; next Bonus Action command moves and detonates within 5 ft one enemy for 2 S d6 fire DEX half. Uses one command budget and ends. No chain from deliberate sacrifice or its own death."
}

### tinker.hero.warmachine.volatile-injection

data/public/class_playtests/tinker.json

{
  "name": "Volatile Injection",
  "activation": "Bonus Action",
  "cost": "1 RP; device loses MHP",
  "rangeAndTarget": "One functional device within 30 ft",
  "duration": "Until end next turn",
  "frequency": "Recharge 3",
  "effect": "Must have strictly more HP than cost. Its next damaging activation adds S d6 to one target; cannot combine with Overcharge, damage cannot be refunded by same activation. No resources gained from self damage."
}

### tinker.hero.warmachine.catastrophic-overload

data/public/class_playtests/tinker.json

{
  "name": "Catastrophic Overload",
  "activation": "Action",
  "cost": "4 RP; sacrifice one device",
  "rangeAndTarget": "10 ft radius about device within 60 ft",
  "duration": "Instant",
  "frequency": "1/long rest",
  "effect": "All creatures including allies DEX save, 3 S d6 fire plus 3 S d6 force on failure, half success. No critical hit, additional destruction proc, salvage, automatic stun or copied damage. Device ends before blast; no Safety exclusion."
}

### tinker.supplement.mech-overdrive

data/public/class_playtests/tinker.json

{
  "name": "Mech Overdrive",
  "activation": "Triggered on deploying a device",
  "cost": "1 long-rest use plus original deployment cost",
  "rangeAndTarget": "One of your newly deployed devices",
  "duration": "Until encounter end, maximum 1 minute",
  "frequency": "1/long rest; automatic Hero capstone",
  "effect": "Source-derived level 20 feature: extend device duration only. It still occupies its slot, requires normal commands and payments, and is destructible. Healing devices keep maximum 3 pulses; bombs, spent uses and expended charges never refill. Does not create permanent equipment."
}

### tinker.hero.artificer.magnetic-wall

data/public/class_playtests/tinker.json

{
  "name": "Magnetic Wall",
  "activation": "Action",
  "cost": "3 RP; one slot",
  "rangeAndTarget": "10-by 5 ft wall within 15 ft",
  "duration": "3 rounds",
  "frequency": "Recharge 4",
  "effect": "AC 12+PB HP 2 L, blocks LOS/movement. Reaction when ranged weapon hit ally within 5 ft of wall reduce its damage by S+M and wall takes reduction amount. Requires line between attack and wall; no automatic all-shot absorption."
}

### docs/mechanics/CLASS_PLAYTEST_RULES.md

Where a class card calls for a **standard companion** without a more specific profile, use: Small or Medium; AC 12+floor(PB/2); HP 2 L; walking Speed 30 ft; saves equal owner's PB; one melee or ranged attack (reach 5 ft/range 30 ft) at owner's class attack bonus, damage S d6 of the printed type. It has no independent class features, resources, loot, death triggers or extra turns. All companions belonging to one character share one Bonus Action command and **one damaging attack/action total per round** unless a specifically priced feature grants more. Without a command they move and Dodge. Act immediately after owner. A standard companion lasts 1 minute, disappears at 0 HP and cannot be healed for free by dismissing/resummoning. The creation cost must be paid again. Creature-specific stat blocks override this profile only where explicitly printed.

### docs/mechanics/CLASS_PLAYTEST_RULES.md

One regular Action, one Bonus Action if a feature permits it, normal movement and one Reaction between starts of your turns. A free trigger costs no Action only if expressly stated. All grants share **one extra full Action per creature per round**. An extra Action cannot grant another Action, recharge itself, or start another extra-Action grant. It supplies no extra Bonus Action or Reaction. A card granting additional attacks is not permission to repeat all class riders on every hit: obey each rider's frequency.

### docs/mechanics/CLASS_PLAYTEST_RULES.md

No damage/healing copy repeats the source's costs, procs, resource generation, critical bonus dice, buffs, actions, cooldown resets or duration. Compute fractions once, capped at 100% of one stored source unless an explicit card states a separately priced higher amount. Copies still cause ordinary damage consequences, concentration checks and death. A copy cannot copy another copy. A target/source record must refer to an actual resolved event, not merely a known ability name.
