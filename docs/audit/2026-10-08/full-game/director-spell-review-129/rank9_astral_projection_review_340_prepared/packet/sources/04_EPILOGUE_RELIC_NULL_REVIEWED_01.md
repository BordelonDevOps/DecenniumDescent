> **Current NEW provisional playtest reference.** The complete corrected EPI-08–14 module was jointly accepted in Review Continuation Part 4. Original sources and owner decisions retain authority; this is not canon, runtime, numerical-balance or human-playtest approval.

# Relics, Dungeon Seeds, and Residual Null — Director Chapter (Revision 03)

## Status, authority, and use

This is jointly reviewed NEW provisional playtest authorship for EPI-08–14. No canon adoption is claimed. Original manuscripts and explicit owner decisions control; the original84 frozen/current source bindings are retained; current GAMEPLAY_LOOP_CANON.md is additionally supplied as source85 for the existing12-character cap. Do not infer the campaign epoch or unresolved cosmological identities. Do not import unseen environment, consumable, bestiary, spell or later-arc drafts.

## Player-facing baseline

`PLAYER_CHAPTER.md` is the complete public procedure. This Director chapter adds hidden answers, actor envelopes, fixed coordinates, source pointers and arbitration. Where the two conflict, `RELIC_NULL_MODEL.json` is the machine-readable statement of this candidate and the conflict must be reviewed rather than silently reconciled.

## Source-bound timing and actor envelope rules

- Passive detection uses COMBAT_ACTION_PLAYTEST line 172: `10 + WIS Perception modifier including actual proficiency`; no proficiency is invented to preserve an earlier mistaken passive.
- Standard turn permissions and Help use COMBAT_ACTION_PLAYTEST lines 31 and 83. Movement/standing costs use lines 156–162. Existing Fall Marker procedure remains source-bound; Ladder does not create a general falling engine.
- Healing Rite is `cleric.json /cards/12`: Action, 2 RP, living ally within 30 ft, `S d8 + M` HP; class S is 1/2/3/4 at Cleric levels 1/5/11/17.
- Undying Spellform is `mage.json /cards/42`: lasts until **end of the Mage’s next regular turn** and otherwise follows HEALING_DEATH_PLAYTEST lines 58–64.
- EPI06 petition stages remain COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST lines 135–177: 10-minute consultation, 60-minute uninterrupted meditation, 10-minute symbolic act, then response; cooldown is 168 elapsed hours from that response.

## Relics

### Shard Pendant of Xi (`RELIC-XI-PENDANT-1`)

**Physical item.** black-silver pendant on 24-inch cord Weight 0.2 lb. neck slot; one free hand only to don/remove; passive/active require worn special relic; ordinary loss/destruction is real; no automatic respawn

**Acquisition and stock.** On the Crystal Bastion landing cell, the one Xi reliquary has two opposed pressure plates. Press both plates simultaneously with two hands or two creatures (one Action) to open it. No roll. Once opened the pendant can be taken with an Action. Stock: 1. Reliquary opens once; item never respawns. NEW: the unique pendant is discovered with charge=1. First bonding changes bearer eligibility only and never changes charge.

**Bond.** Eligibility: any class. 1 uninterrupted active hour wearing/handling the actual pendant; no roll; not a rest. Transfer or 10+ minutes separation from the item ends bond. A new bearer repeats the hour.  This module creates no universal attunement-slot cap.

**Passive — Motive-Certainty Refusal.** A magical information effect cannot return an output that claims the bearer's actual motive, fundamental desire, or intended reason with absolute certainty. It may still return emotions, surface thoughts, alignment, observable behavior, probabilities, or other information within its real scope. If only the prohibited field is blocked, other legal fields remain.

**Active — Declare Contradiction.** Action; 60 ft; bearer must perceive the selected creature and know which ongoing spell record is being addressed. Target: One ongoing spell-effect record currently affecting one creature. A fixed zone/area with no individual target record is ineligible. A multi-target spell can lose one independently tracked target branch without ending other branches. During the Action the actual caster and selected affected target must each knowingly agree. Consent is a fiction-level no-action response, not compelled communication. Dead, absent, unreachable, mindless, or unwilling caster/target means consent cannot be completed. The Action is spent on declaration. The charge is spent only when both consents are valid; then the selected ongoing effect branch ends immediately. No RP/slot/action/use refund. If the ended branch was the last remaining effect of a concentration spell, concentration ends normally; otherwise other branches remain. A continuing spell-created target record is eligible only while it is still an ongoing spell effect with identifiable caster and target. Damage already resolved is never rewound. Failure: Invalid target or missing/declined consent spends the Action but not the charge. Charge: 1 charge; refreshes only when the bonded bearer completes a beneficial Long Rest while possessing the pendant. Transfer, rebonding, removal, destruction/recovery, or another person's rest never refreshes it. Item-bound charge starts at 1 when first taken from its reliquary.

**Transfer/loss.** Bond ends on transfer. Charge state belongs to item identity and transfers with it; no reset. One actual item. Copies/illusions cannot duplicate passive, charge, or identity.

### Concord Spear Fragment (`RELIC-CONCORD-SPEAR-1`)

**Physical item.** Proof-War spear fragment mounted on serviceable 6-ft haft Weight 3 lb. one hand normally; two hands for versatile damage 

**Acquisition and stock.** Resolve the staged duel by either side-victory or neutral accord. If party prevents both projections from being reduced to 0 and completes the Accord option, spear fragment rises from center plinth automatically. Otherwise it appears after the projection duel ends but is sealed for 1 hour; then it can be taken. One actual fragment. Stock: 1. No respawn.

**Bond.** Eligibility: Paladin or Soldier class level >=1. 1 uninterrupted active hour drilling forms with actual spear; no roll; not a rest. Eligibility does not grant spear proficiency. Use actual class/ancestry/feat proficiency; an unproficient wielder omits proficiency bonus as normal. No universal attunement cap.

**Weapon.** Spear: 1d6 piercing, versatile 1d8, thrown 20/60. Relic explicitly adds Finesse and Heavy for its attuned user. Properties: Finesse, Heavy, Thrown 20/60, Versatile 1d8. Actual Heavy rule applies: Small creatures have disadvantage on attack rolls with it.

**Hesitation.** Bonus Action before one actual attack with this spear on the same turn. Charge that one declared attack with radiant bonus damage equal to floor(character level/2), minimum 0. Melee or thrown spear attack. The attack must occur before turn end; if not, charge expires. A miss consumes the charge. No idle precharge, rewind, or carryover. Radiant bonus is a flat number and is not multiplied by a critical hit unless a future exact rule explicitly multiplies flat bonuses. Thrown spear remains where the attack places it and must be physically recovered; no magical return. No RP, Conviction, Soldier engine, planar authority, or divine spellcasting is granted.

**Loss/copy.** If lost/destroyed, no replacement is generated. No copied fragment has powers.

### Mirror of Potential Silence (`RELIC-MIRROR-SILENCE-1`)

**Physical item.** oval hand mirror, black glass, silver rim Weight 1.0 lb. one hand to activate/touch; can be carried or stowed 

**Acquisition and stock.** Complete the theatre through a fictional-vow/neutral-prompt branch or resolve the Echo Doppelganger. Mirror rises from the stage trap together with exactly three silver reflection tabs. One mirror and three tabs total. Stock: 1. No second mirror from replay. The mirror appears with exactly 3 physical reflection tabs (TAB-SILENCE-1, TAB-SILENCE-2, TAB-SILENCE-3), 0.05 lb each. Physical items; can be lost/transferred/destroyed; never respawn.

**Activation.** Action; user touches mirror and speaks/signs/writes one fictional-character fear in a language the user can express. No real-player personal disclosure. Beneficiary: User only. Mirror shows a brief fictional image where the fear is untrue. The user gains advantage on their next Wisdom saving throw made within 24 hours. One pending benefit maximum; cannot activate again while pending. On the qualifying save: On the qualifying Wisdom save, first resolve normal advantage/disadvantage cancellation and every legal reroll/replacement. If the final save outcome succeeds, pending benefit is consumed and mirror remains intact. If final outcome fails, pending benefit is consumed and mirror shatters after that save resolves. Pending benefit expires after 24 elapsed hours unused; mirror remains intact. If mirror is lost/destroyed before pending save, the pending benefit ends immediately.

**One lifetime reformation opportunity.** After CH12 first resolves, the attached east-stage repair-room door remains an ordinary physical route from the theatre whenever the adopted dungeon location is physically reachable. Leaving the chamber does not delete the room or actor. Requirements: All three exact silver reflection tabs and the recoverable shattered mirror identity are required. Sentinel inspects first. Refusal or missing stock consumes nothing. On acceptance, all three tabs transfer into the repair cradle and are consumed immediately; mirror pieces remain in Sentinel custody during work. Work: 2 uninterrupted active hours of Sentinel work; no roll. Interruption resets accumulated repair-work time to 0 but does not recreate tabs. If the Sentinel and pieces remain available, work can restart without new tabs because the same consumed tabs remain committed in the cradle. Acceptance: Sentinel accepts only the original mirror, all three tabs, unused lifetime repair, and a non-hostile requester. It refuses a counterfeit/copy, missing stock, a second repair, or a requester currently attacking/coercing it. A hostility refusal is final for that visit; after the scene returns to non-hostile status for 10 elapsed minutes, one new request may be made. The Sentinel may not invent additional moral tests or prices. Completion: Same mirror identity reforms. Pending mirror benefit is not restored. EPI07 Sentinel/history records are neither reset nor copied. A second shattering has no repair procedure in this module.

**Copy.** Reflections/copies are mundane images only.

### Glove of Null Ink (`RELIC-NULL-GLOVE-1`)

**Physical item.** single black glove with sealed ebony motes beneath translucent stitching Weight 0.5 lb. one compatible hand; writing requires that hand free 

**Acquisition and stock.** The glove is already crafted and sealed in a soundless reliquary. After the Silence Wraith is comforted/evaded/defeated, open the reliquary with an Action. This is an already-crafted relic; the module creates no Matrix-dust mining or crafting recipe. Stock: 1. One glove, no respawn.

**Air Writing.** Action. Choose a point within 10 ft and line of effect; write on a fixed or free-standing plane no larger than 10×10 ft. Content: Up to 25 words or equivalent simple symbols in one written language the wearer actually knows. One active inscription per glove; making a new one erases the old. Duration: 10 elapsed minutes, then vanishes. Wearer can erase early with an Action within 10 ft. Visibility: A creature must be able to see the inscription. Blindness, total visual obstruction, and applicable darkness still matter. Readability: At observation time, a creature can derive the underlying text only if it currently and sincerely advocates a peaceful but passionless solution to the immediate dispute/topic addressed by the inscription. This is an established fictional stance, not alignment, faction, species, or secret cult membership. The glove never reports who qualifies. Language: Eligibility reveals the actual written words, not automatic translation. An eligible observer who does not know the chosen language still needs real language/translation rules. Copying: An eligible reader may remember or transcribe the understood ordinary text. An ineligible observer may copy visible shapes, but that copy is nonmagical meaningless glyph-shape data and does not later self-decode. Limits: No mind reading, loyalty test, compulsion, KT/PT protection, peacefulness certification, or hidden-identity revelation.

**Copy.** No inscription duplicates relic/resource/class effects.

## Residual Null, ordered damage algorithm, purges, flora and antidote

The complete public Null/flora/antidote rules are reproduced here for table use.

## Residual Null and Null Veil

### Exposure

A Residual Null field is a Director-authored bounded area with a stable field identity, explicit boundary and clock. This module authors such fields only where a chamber/site says so; high-altitude/catacomb wording remains source context, not an everywhere detector. Each creature keeps minutes-per-field. While physically inside a field, accumulate elapsed minutes. Each time that field's accumulator reaches 60, subtract 60 and immediately make WIS save DC15. Partial minutes pause on exit and resume on re-entry to the same field. Completing one beneficial Long Rest wholly outside that field clears only that field's partial accumulator; it does not purge Null Veil or erase exposure history. On a failed hourly save, a creature without Null Veil gains one Null Veil immediately; on success it gains none. A creature already bearing Veil uses the no-stack/no-refresh rule below. Dead targets remain ineligible. Genuinely distinct overlapping field identities track separately. Merely nesting/renaming one field cannot multiply saves. Still make hourly saves for exposure history; success has no extra effect, failure does not stack or refresh a second Veil. Living sleeping/Unconscious creatures make the WIS save normally because those conditions do not automatically fail Wisdom saves. Dead targets do not gain Veil. A visual glow, realm name or Veiled Expanse label is not an exposure field. Only a scene with an explicit fieldId/boundary contributes exposure. CH07 has NULL-FIELD-QUIET-WELL-1; CH11 Veiled Expanse landing cell has no active field.

### Null Veil

**Duration.** Persists until one listed purge succeeds. Exiting field alone does not end it.

**Passive Insight.** While Veil is active and not suppressed, final passive Insight is 5. This is a setting of that passive score, not omniscience or motive detection. Suppression restores normal calculation for its duration.

**Creation-time nonlethal damage flag.** At creation of each damage root, record root dealer. If that dealer is a character currently under unsuppressed Null Veil, mark the entire root `nullNonlethal=true`. Descendant delayed/ongoing packets inherit the creation-time flag; later Veil changes do not rewrite it. A distinct later activation/attack creates a new root and re-evaluates. A companion/minion has its own dealer identity. Controller Veil does not convert companion damage unless an exact ability says the controller is the damage dealer. Pure transfer/redirection keeps the original root's nullNonlethal flag. It does not create a second root or extra prevention/resource triggers. An effect that explicitly creates new reflected/retaliatory damage uses the reflector as dealer and evaluates that new root at creation. A mere transfer is not reflection.

When a root is qualifying Null-nonlethal, use this order:

1. Snapshot recipient identity/lifecycle, pre-event HP/tempHP/Wounds/death state and the root nullNonlethal flag. Resolve ordinary defenses, resistance and temp-HP absorption and calculate the ordinary post-temp damage/HP loss values; attached non-damage riders remain pending under their own triggers.
2. If nullNonlethal is false, use the ordinary CORE/HEALING_DEATH/lifecycle procedure unchanged. If true, continue below. Objects/noncreature structures still take ordinary object damage and can be destroyed; the word nonlethal does not make objects indestructible.
3. For any living-recipient qualifying damage packet, suppress damage-caused Instant Death and suppress the packet’s Core Wound/Maiming save entirely, including half-maximum and positive-HP Wound triggers. Therefore the packet cannot create a fatal fourth-Wound result while the recipient remains above 0 or reaches 0. Existing Wounds remain recorded.
4. Apply normal HP loss down to minimum 0. Positive→positive: stop the Null zero-state branch; recipient keeps resulting positive HP, existing Wounds/conditions and independent riders. Positive→0 ordinary living: skip damage-caused death/death-save failures and establish Stable0 with counters reset and exactly one ordinary Stable recovery deadline, unless a source-specific zero-HP permission such as actual Undying Spellform applies as stated below.
5. Already Dying0: qualifying damage causes no new damage failure/death and does not stabilize, clear counters or move the existing death-save schedule. Already Stable0: causes no failure/death and keeps the existing recovery deadline exactly; never reroll/extend it. If temp HP absorbs the entire normal-HP loss so HP never reaches0, no zero-state transition occurs.
6. For nonliving/companion/projection recipients, use exactly one explicit recipientLifecycle branch below; do not infer anatomy from a name. The Null override replaces only the damage-caused lethal/destruction endpoint named by that branch. Independent duration, dismissal, concentration/source end, sacrifice/cost, Hunt finality or other non-damage expiry remains real.
7. Would-die/death-trigger protections do not trigger or spend if their prerequisite death/fatal branch was skipped by Null. A source-specific trigger keyed only to damage reducing HP to0 without killing, such as actual Undying Spellform, still triggers. Independent non-damage riders resolve if their own trigger remains true and they do not require a Wound/death result.
8. Direct HP payments/sacrificial costs are not damage and are never converted. New reflected/retaliatory damage that is a new root re-evaluates its own dealer; pure transfer/redirection preserves the original root flag and does not duplicate root triggers.

### Recipient lifecycles for qualifying Null damage

**Ordinary living recipient.** Use orderedAlgorithm steps 3–5. Positive→positive: no packet-created Wound/Instant Death. New positive→0: Stable0 unless an exact source-specific zero permission overrides. Already Dying0: same counters/markers. Already Stable0: same recovery deadline.

**Ranger Beast.** Source normally dies immediately at0. Qualifying Null damage replaces that damage-caused immediate-death transition with Null Disabled at0: Incapacitated, Speed0, no commands/actions; same animal/bond remains. Ordinary legal companion healing above0 ends Disabled. A later independent non-damage death/removal rule still works.

**Finite summon, Familiar or Mirror Beast.** Source normally disappears/ends at0. Qualifying Null damage replaces only that damage-caused zero disappearance with Null Disabled at0 while its original duration/source still exists. Independent duration expiry, dismissal, concentration/source end or replacement still ends it. Legal companion healing above0 restores function; no generic repair/resummon is granted.

**Mage Lich elite.** Source normally becomes destroyed bound asset at0. Qualifying Null damage leaves same elite Null Disabled at0, not destroyed; therefore Soulbound is not legal solely from this zero. Legal companion healing above0 restores it. An independent actual destruction/expiry can later create its normal destroyed state.

**Wizard standard undead.** Qualifying Null damage leaves same minion Null Disabled at0 instead of damage-caused destruction. Dismissal or owner completed-LR expiry still ends it. Legal healing above0 if a real source applies may restore it.

**Authored local projection.** A scene projection whose authored 0-HP rule says disperse/end uses that administrative projection endpoint even under Null; it is not a living death/Wound branch. ACT-FEAST-STEWARD instead uses its explicit Collapsed Projection rule. This classification must be printed in the actor profile, not inferred from a name.

**Undying Spellform.** If qualifying damage newly reduces a Mage with actual Undying Spellform to0 without killing outright, its printed trigger occurs and its 1/LR use is spent. It overrides zero-HP Unconscious/Incapacitated permissions as reviewed: conscious, half-Speed voluntary movement, normal Action, legal spellcasting/concentration, no independent BA/Reaction. Triggering damage still causes its concentration save. If still0 at feature expiry, the reviewed expiry destabilizes/cancels Stable recovery and adds one failed death save; that later feature-expiry event is not the original Null damage packet.

**Would-die protections.** A protection whose trigger requires actual death/would-die/fatal result does not trigger and spends no use when Null skips that damage-caused death branch. Do not replay it later. Separate minimum-HP prevention that resolves earlier follows its own source if actually triggered.

**Actual nonliving Construct.** For an actual nonliving Construct creature with an authored HP/destruction endpoint, qualifying Null damage reducing it to0 replaces only damage-caused destruction with Null Disabled0: Incapacitated, Speed0, no Actions/Bonus Actions/Reactions/commands. Same construct identity remains; no corpse/parts/loot are generated by the zero. Only an actual repair/heal rule that expressly applies to that construct can raise it above0 and end Disabled; no generic repair is granted.

**Silence Wraith only.** For ACT-SILENCE-WRAITH specifically, qualifying Null damage reducing it to0 replaces its damage-caused dispersal with Null Disabled0 (Incapacitated, Speed0, no Actions/Bonus Actions/Reactions). It has no corpse/soul/loot. The chamber’s independent correct-plate terminal may still pacify/disperse that same identity; no generic healing/repair is invented.

**Local actor bindings.** ACT-TOY-SENTINEL: ordinaryNonlivingConstruct; ACT-SILENCE-WRAITH: localSpirit; ACT-ACCORD-DEVIL: localProjection; ACT-ACCORD-DEMON: localProjection; ACT-ECHO-DOPPELGANGER: localProjection; ACT-FEAST-STEWARD: explicit Collapsed Projection actor rule; ACT-NULL-WITNESS: ordinaryLiving; ACT-GLASS-MENDER-SENTINEL: localProjection.

**What Null Veil does not erase.** Does not remove old Wounds/Injuries, revive Dead creatures, clear existing dying counters, rewrite death history, cure conditions, or prevent non-damage lethal costs/tracks. Newly-zero stabilization resets only its current death-save counters because becoming Stable requires that under Core. Direct HP payments/sacrificial costs are not damage and are not converted. This nonlethal override does not alter Hunt finality or Hunted Death rules for actual later deaths from other causes.

### Shrug off empathy

Bonus Action while active and not Incapacitated; CHA save DC15, binary. **Success:** Suppress Veil until the start of the character's next regular turn in initiative. Outside initiative, suppress for 6 elapsed seconds. During suppression passive Insight and damage conversion are inactive, but the Veil record remains and exposure clocks continue. **Failure:** Apply actual Incapacitated until the end of the character's next regular turn. Outside initiative, 1 elapsed minute. Concentration ends immediately under current Incapacitated rule. After duration, Bonus Action can be attempted again if otherwise legal. **Immunity:** Immunity to Incapacitated prevents that failure condition; no unnamed substitute penalty. The save can still fail and Veil remains unsuppressed. Timing uses the existing absolute/virtual-marker system: Use reviewed COMBAT_ACTION_PLAYTEST timing. Initiative-created success expires at the next regular source-start virtual marker; if initiative ends first, that virtual marker continues every six seconds and expiration still occurs at its original scheduled instant. Outside-initiative success uses absolute +6s and keeps that deadline if initiative begins. Initiative-created failure expires at end of next regular source turn using preserved virtual end marker; outside-initiative failure uses absolute +60s and keeps that deadline if initiative begins. Starting/ending/reordering initiative or extra turns never restart, shorten, extend or duplicate these records.

### Purging Null Veil

Only these listed procedures purge this candidate Null Veil; ordinary field exit does not.

**Mask confession (NEW narrow EPI04 extension).** Wearer's current operative Living or Cracked mask is physically worn. Spend an Action and communicate one truthful current fictional emotional-state statement tied to the mask's bound vow to one willing creature/Sentinel within ordinary communication reach who actually understands it. Spoken, signed, or written methods follow current language rules. If understood, purge Null Veil immediately after the Action. Mask stays worn; wearerRevealCharge and safe-removal rules are unchanged. Real-player personal disclosure is never required. Failure: If nobody understands or statement is not truthful/current fiction, Action spent and Veil remains.

**Archon Temporary Blessing (NEW narrow EPI06 rider).** Complete the current EPI06 petition procedure using a real available Witness/quiet chamber/symbolic act. If the response roll is 5–8 and grants the actual Temporary Blessing boon, the granting moment also purges one Null Veil from the petitioner. Guidance 1–4, Test 9–11, Revelation 12, old blessing history, or a previously granted temporary feature do not purge. This module adds no reroll or guaranteed result. CH07 includes a finite local Witness profile who can perform the consultation when that chamber is adopted; petition eligibility/rest/timing remain current EPI06 rules. The underlying petition still requires the real EPI06 stages: a qualified Witness performs a 10-minute consultation, followed by one uninterrupted 60-minute meditation and a 10-minute symbolic act; the 168-hour petition cooldown starts at the response roll.

**Bittersap Antidote.** Consume one actual NULL-ANTIDOTE-DOSE under Equipment Item Procedures. Purge Null Veil immediately after successful administration. Continuing field exposure remains and future hourly saves still occur. Does not cure Corrupted, Dissonance, Strain, Exhaustion, KT/PT, Hunt, Wounds, poison, disease or another condition unless an exact separate rule says so.

## Null flora and Bittersap Antidote

### Bittersap Root

**Finite stock.** 6 mature nodes; each node one harvest attempt; no replenishment in this module **Recognition.** 10 minutes, INT or WIS (Nature) DC14. Success identifies plant and safe root; failure = uncertainty, not false ID. **Harvest.** 20 minutes, one hand + small knife or herbalism kit; WIS (Survival) DC14. Critical Success 2 parts, Success 1, Failure 0 and node is bruised/consumed, Critical Failure 0 and tool must be cleaned 10 minutes before another flora harvest. **Unit.** 1 part = 0.1 lb cleaned root **Freshness.** 7 days ordinary storage; 30 days in a sealed cool specimen case; then spoiled/nonfunctional. **Standalone effect.** No direct mechanical effect when eaten raw; recipe ingredient only. Nodes are fixed identities BT-1..BT-6, two per BT-TRAY-1..3. Moving a tray moves those same nodes; it creates none.

### Tranquil Thorn

**Finite stock.** 4 sprigs; no replenishment **Recognition.** 10 minutes Nature DC14 **Harvest.** 10 minutes with gloves or tongs; DEX (Herbalism kit) DC14. Critical Success 2 parts, Success1, Failure0 and sprig breaks, Critical Failure0 and harvester takes1 piercing damage. **Unit.** 0.05 lb **Freshness.** 14 days dry; 60 days sealed **Standalone effect.** No default combat/cure effect. A brewed nonmagical tea is calming fiction only and grants no mechanical bonus. Sprigs TT-1..TT-4 all in TT-TRAY-1.

### Echo Lily

**Finite stock.** 4 blooms; no replenishment **Recognition.** 10 minutes Nature DC14 **Harvest.** 10 minutes with herbalism kit; DEX (Herbalism kit) DC14. Critical Success 2 parts, Success1, Failure0 and bloom wilts, Critical Failure0 and adjacent second bloom also wilts (if any). **Unit.** 1 part = 0.05 lb petals **Freshness.** 3 days ordinary; 14 days sealed cool **Standalone effect.** Recipe ingredient only; no standalone echo/memory power. Blooms EL-1..EL-4, two per EL-TRAY-1..2. Moving a basin moves those same blooms; it creates none.

### Black Hush Moss

**Finite stock.** 4 patches; no replenishment **Recognition.** 10 minutes Nature DC14 **Harvest.** 10 minutes with scraper/herbalism kit; DEX (Herbalism kit) DC14. Critical Success2 parts, Success1, Failure0 and patch lost, Critical Failure0 and one adjacent patch contaminated (if any). **Unit.** 0.05 lb **Freshness.** 30 days dry/sealed **Standalone effect.** No default Null cure or silence effect. Can be used as mundane black dye after 10 minutes steeping. Patches BH-1..BH-4 all in BH-TRAY-1.

### Bittersap Antidote

**Ingredients.** 2 Bittersap parts + 1 Echo Lily part + 1 pint actual Bastion flame water **Flame-water stock/access.** 6 sealed 1-pint flasks, 1 lb each; no replenishment. Home-plane affiliation, Concord Step, or ordinary plane choice creates none. Only via an actually adopted CH11 shard-card activation or another separately authored lawful source; this module grants no general Bastion travel.

**Apparatus.** Heatproof pot, stirring tool, one ordinary heat source; Herbalism kit or Alchemist's supplies available to the brewer.

**Work and check.** 30 uninterrupted active minutes. Ingredients are committed/consumed when boiling begins. At completion make INT (Herbalism kit) or INT (Alchemist's supplies) DC15; use proficiency only if actually proficient.

**Outcomes.**
- Critical Success: 1 dose; shelf life 30 days.
- Success: 1 dose; shelf life 7 days.
- Failure: 0 dose; ingredients consumed; pot remains usable after 10-minute cleaning.
- Critical Failure: 0 dose; ingredients consumed; pot fouled and unusable for 1 hour of cleaning.

**Dose.** Weight 0.2 lb. Action, one available hand. Drink, or feed to willing/Incapacitated living creature within5ft if it can swallow, per equipment procedure. Unwilling active creature has no free forced-dose permission. Purges Null Veil only. Dose consumed whether or not target is Veiled; no diagnostic refund. **Limits.** No Corruption/KT/PT/Hunt/Dissonance/Strain/Exhaustion/Wound/poison/disease cure. No reviewed recipe-count change.

## Scene actors

### Memory Forge Toy Sentinel (`ACT-TOY-SENTINEL`)

**Status/lifecycle.** NEW provisional scene actor. Construct creature; ordinary monster life-state. At 0 HP it is destroyed/inert unless a local Null rule applies.

**Placement.** CH01: Toy1(10,10), Toy2(30,10), Toy3(10,30), Toy4(30,30), all floor z=0, one independent creature per printed plinth.

**Envelope.** Size Small; AC 15; HP 24; Speed 30 ft; senses darkvision 60 ft; passive Perception 13 (10 + printed Perception +3). Ability modifiers: STR +2, DEX +3, CON +2, INT -1, WIS +1, CHA +0. Proficiencies: Perception +3. Defenses: immune to poison and disease; no other immunity.

**Actions.**
- **Tin Edge:** +6 melee, reach 5 ft, one target. 1d8+3 slashing
- **Clockwork Lunge:** +6 melee weapon attack after moving at least 10 ft straight; reach 5 ft; one target. 1d6+3 bludgeoning; target STR save DC14 or Prone

**Behavior.** Attacks the nearest creature carrying/touching a manifested toy. A successful Comfort action against it ends hostility permanently for this chamber.

### Silence Wraith (`ACT-SILENCE-WRAITH`)

**Status/lifecycle.** NEW provisional scene actor; not bestiary promotion. Spirit scene creature with an explicit Null lifecycle binding. Ordinarily at 0 HP it disperses with no harvestable corpse/soul-claim. Under qualifying Null damage, use recipientLifecycle.localSpirit: it becomes Null Disabled at 0 instead; the chamber’s independent plate-terminal pacification/dispersal can still end it.

**Placement.** CH03: hovers at (27.5,27.5), z=5 ft at scene open.

**Envelope.** Size Medium; AC 15; HP 58; Speed 30 ft, fly 30 ft (hover); senses Heartbeat vibration sense 60 ft through contiguous CH03 stone/plate surfaces when the creature with a beating heart is physically supported by those surfaces; passive Perception 17 (10 + printed Perception +7). Motion does not switch off a heartbeat. A genuinely heartbeat-free creature creates no heartbeat signal solely from anatomy, but other ordinary perception remains possible. A flying/hovering creature with no contact to chamber surfaces transmits no heartbeat vibration through them.. Ability modifiers: STR +0, DEX +4, CON +2, INT +1, WIS +4, CHA +2. Proficiencies: Perception +7, Stealth +7. Defenses: resistance to nonmagical bludgeoning/piercing/slashing; immune to Deafened.

**Actions.**
- **Hush Claw:** +7 melee spell-like scene attack; reach 5 ft; one target. 2d6+4 cold; target CON save DC15 or cannot deliberately speak until end of that target’s next regular turn (outside initiative: 6 seconds absolute). This actor-specific speech loss is not the whole Silenced condition; it independently blocks V while it lasts because V requires actual audible speech.
- **Pulse Hunt:** Action; one creature whose heartbeat location the Wraith currently senses within 30 ft. WIS save DC15; failure: Frightened of the Wraith until end of that target’s next regular turn (outside initiative: 6 seconds absolute).

**Behavior.** Hunts strongest heartbeat vibration it can sense. Stillness never erases a heartbeat. It may use ordinary visible-target perception if applicable; heartbeat sense itself does not see through total-cover barriers disconnected from the chamber stone.

### Accord Devil Projection (`ACT-ACCORD-DEVIL`)

**Status/lifecycle.** NEW provisional projection, not bestiary promotion. Projection; 0 HP ends projection, no corpse/soul/loot.

**Placement.** CH10: (10,25), floor z=0.

**Envelope.** Size Medium; AC 16; HP 52; Speed 30 ft; senses passive Perception 11 (10 + WIS +1; no Perception proficiency printed). Ability modifiers: STR +3, DEX +2, CON +3, INT +2, WIS +1, CHA +4. Proficiencies: Deception +7, Persuasion +7. Defenses: resistance fire; projection ignores disease/poison.

**Actions.**
- **Contract Blade:** +7 melee weapon attack; reach 5 ft; one target. 1d10+3 slashing + 1d4 fire
- **Measured Rebuke:** +6 ranged spell-like projection attack; range 30 ft; one target. 2d6 psychic

**Behavior.** Prioritizes the demon projection unless a PC attacks or materially aids the demon.

### Accord Demon Projection (`ACT-ACCORD-DEMON`)

**Status/lifecycle.** NEW provisional projection, not bestiary promotion. Projection; 0 HP ends projection, no corpse/soul/loot.

**Placement.** CH10: (40,25), floor z=0.

**Envelope.** Size Medium; AC 14; HP 60; Speed 35 ft; senses passive Perception 11 (10 + WIS +1; no Perception proficiency printed). Ability modifiers: STR +4, DEX +2, CON +4, INT +0, WIS +1, CHA +1. Proficiencies: Athletics +7. Defenses: resistance cold; projection ignores disease/poison.

**Actions.**
- **Rending Claw:** +7 melee natural attack; reach 5 ft; one target. 2d8+4 slashing
- **Roar of Refusal:** Action; 15-ft cone; each enemy projection/PC in cone. WIS save DC15; failure Frightened of demon until end of that target’s next regular turn (outside initiative: 6 seconds absolute).

**Behavior.** Rushes the devil projection; attacks PCs only after direct interference against it.

### Echo Doppelganger (`ACT-ECHO-DOPPELGANGER`)

**Status/lifecycle.** NEW provisional scene actor; not a PC copy. Projection; 0 HP ends projection, no corpse/soul/XP duplication.

**Placement.** CH12: manifests on center-stage trapdoor square centered (15,32.5), floor z=0.

**Envelope.** Size Medium; AC 15; HP 48; Speed 30 ft; senses passive Perception 12 (10 + WIS +2; no Perception proficiency printed). Ability modifiers: STR +2, DEX +4, CON +2, INT +1, WIS +2, CHA +2. Proficiencies: Acrobatics +7, Insight +5. Defenses: resistance psychic.

**Actions.**
- **Echo Strike:** +7 force attack; choose melee reach 5 ft or ranged range 20 ft; one target. 2d6+4 force
- **Rehearse Doubt:** Action; one creature within 30 ft; CHA save DC15. Failure: -2 to the target’s next ability check before the start of its next regular turn. Outside initiative the record expires after 6 elapsed seconds if unused. Initiative start/end does not move an already-recorded deadline.
- **Reaction — Mirrored Guard:** Once/round when hit, +2 AC against that attack; if this makes attack miss, no further effect.

**Behavior.** Looks like the triggering character but copies no class cards, resources, inventory, spells, memories, XP, attunements, or identity. It attacks that character first.

### Ash Feast Steward (`ACT-FEAST-STEWARD`)

**Status/lifecycle.** NEW provisional projection. Projection; cannot die. At 0 HP it enters Collapsed Projection: Incapacitated, Prone, Speed 0, no Actions/BA/Reactions, remains present until scene resolves. Legal healing that expressly works on this projection can restore it above 0; otherwise it stays collapsed. Scene resolution dismisses it regardless of HP.

**Placement.** CH05: behind central serving table at (20,20), floor z=0.

**Envelope.** Size Medium; AC 14; HP 40; Speed 30 ft; senses passive Perception 12. Ability modifiers: STR +1, DEX +1, CON +2, INT +2, WIS +2, CHA +3. Proficiencies: Insight +5. Defenses: immune to poison/disease (projection).

**Actions.**
- **Ash Ladle:** +5 melee weapon attack; reach 5 ft; one target. 1d6+2 bludgeoning; no attack unless party becomes violent

**Behavior.** Explains serving etiquette truthfully, never forces eating, and allows withdrawal.

### Witness Sera, Quiet-Well Recorder (`ACT-NULL-WITNESS`)

**Status/lifecycle.** NEW provisional mortal NPC for chamber access. Living humanoid significant NPC; uses death saves if reduced to 0.

**Placement.** CH07 petition alcove at (0,-22.5), floor z=0.

**Envelope.** Size Medium; AC 12; HP 22; Speed 30 ft; senses passive Perception 14. Ability modifiers: STR +0, DEX +1, CON +1, INT +3, WIS +4, CHA +2. Proficiencies: Insight +7, Religion +6, Persuasion +5. Defenses: none beyond ordinary equipment.

**Actions.**
- **Quarterstaff:** +3 melee weapon attack; reach 5 ft; one target. 1d6 bludgeoning
- **Record Petition:** noncombat. Acts as local Witness only for current EPI06 petition step one; grants no automatic favorable Archon response.

**Behavior.** Neutral recorder; refuses coercion, follows current EPI06 motive-record procedure, and leaves if attacked.

### Glass-Mender Sentinel (`ACT-GLASS-MENDER-SENTINEL`)

**Status/lifecycle.** NEW finite local projection; not bestiary promotion. Projection tied to CH12 repair room. At 0 HP it disperses for 1 hour, interrupting work; then the same projection identity reforms in the repair room if CH12 still exists. No corpse, soul, loot, XP or copied Sentinel history.

**Placement.** CH12 repair room at (37.5,32.5), floor z=0, adjacent to repair cradle.

**Envelope.** Size Medium; AC 16; HP 45; Speed 25 ft; senses passive Perception 13 (10 + WIS +3; no Perception proficiency printed); ordinary sight/hearing. Ability modifiers: STR +2, DEX +1, CON +3, INT +4, WIS +3, CHA +1. Proficiencies: Investigation +7, artisan glasswork +7. Defenses: resistance to psychic; immune poison/disease (projection).

**Actions.**
- **Ward Staff:** +5 melee weapon attack; reach 5 ft; one target. 1d6+2 force; used only if attacked
- **Mend Mirror:** noncombat. Uses RELIC-MIRROR-SILENCE-1 reformation transaction; no attack roll.

**Behavior.** Neutral custodian. Never pursues outside repair room; follows the finite acceptance/refusal rule printed on the mirror.

## Dungeon Seed rooms — hidden map and arbitration

### 1. Memory Forge (`CH01-MEMORY-FORGE`)

**Placement/status.** Conditional: adopt only at an actual existing undocumented-floor site appropriate to the campaign. Original source premise is after Infinite Yield; use outside that premise must be explicitly logged as alternate staging. No numbered floor/epoch selected. NEW provisional chamber scene

**Geometry.** NEW fixed scene map: 40×40-ft square, southwest origin, floor z=0, ceiling20. West arch x=0,y17.5–22.5; east arch x=40,y17.5–22.5 is initially sealed. Central 10×10 forge dais occupies x15–25,y15–25 at floor level. Four 5×5 plinth spaces are centered at (10,10),(30,10),(10,30),(30,30); Toy1..Toy4 start respectively on those spaces. Each is a separate ACT-TOY-SENTINEL creature with its own24HP and resolution record. No starting spaces overlap.

**Sensory/telegraph.** Warm metal smell, hammer ticks with no smith, four metal toys mimic fictional childhood objects chosen by characters or Director-safe prompts. Before any attack, each toy raises its edge and the forge projects the words 'COMFORT WHAT MEMORY MADE SHARP.'

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

**Placement/status.** Conditional undocumented-floor scene; same temporal wrapper as CH01. NEW provisional chamber scene

**Geometry.** 20×60-ft hall; entrance south, exit north; six blank wall panels.

**Sensory/telegraph.** Dry pigment smell, soft brush-noise from empty walls. A brass placard states: 'TOUCH SHOWS AMBITION; IMAGE IS POSSIBILITY, NOT PROPHECY.'

**Objective.** Reveal three murals and choose one fictional ambition to acknowledge.

**Procedure.**
1. Touching a panel is an Object Interaction and creates one image of a plausible next ambition for that character, chosen from already-established character fiction or a Director-safe prompt. It is not guaranteed future truth.
2. After three images, one character spends an Action to state, sign, or write which image they pursue/reject and why; no roll. Players need not disclose real personal goals.
3. Alternative: 10-minute INT (Investigation) DC14 identifies the acknowledgement latch and permits a neutral statement such as 'These are possibilities, not commands.'

**Failure/withdrawal.** No lethal failure. Refusing interaction leaves north exit shut; south exit remains open.

**Reward.** One finite mural rubbing sheet (0.02 lb) showing only the chosen image; no divination power.

**Persistence.** Each panel reveals once per character identity; revisiting does not generate new ambitions/rewards.

### 3. Echoless Vault (`CH03-ECHOLESS-VAULT`)

**Placement/status.** Conditional undocumented-floor scene; same wrapper. NEW provisional chamber scene

**Geometry.** 35×35-ft vault on 5-ft grid. West threshold at (0,15–20), east reliquary/exit at (35,15–20). Seven numbered 5-ft plates form the center line at x=2.5,7.5,12.5,17.5,22.5,27.5,32.5; y=17.5. The west threshold includes a 5-ft mechanically isolated stone sill outside the plate lattice.

**Sensory/telegraph.** Absolute acoustic silence inside; vibrations visibly ripple silver dust on floor. At threshold, footprints make silver rings and a translucent hunter turns toward them.

**Objective.** Reach the east reliquary/exit without feeding the hunter vibrations, or pacify it through the plate procedure.

**Actors.** ACT-SILENCE-WRAITH

**Hidden fixed plate answer:** 1→3→5→7. The west sill is outside the acoustic field and mechanically isolated from the plate lattice. The correct terminal disperses/pacifies even a Null-Disabled Wraith.

**Procedure.**
1. Heartbeat truth: the Wraith senses heartbeat vibrations under ACT-SILENCE-WRAITH; remaining motionless does not hide a beating heart.
2. Plate solution is fixed 1→3→5→7. The west-wall inscription can be studied from the isolated sill for 10 uninterrupted minutes; INT (Investigation) DC14. Success reveals the sequence; failure gives no false sequence and the same character cannot retry until after one beneficial Short or Long Rest. The sill does not transmit heartbeat vibration into the plate lattice.
3. To depress a numbered plate, a creature/object must physically press that plate; one Action latches it. Latches persist. Pressing a wrong plate resets only the current sequence, never actor HP or consumed resources. Four correct Actions total open the east exit/reliquary and pacify the Wraith. If the Wraith is Null Disabled at 0, this terminal pacification independently disperses that same scene identity.
4. Crossing connected chamber stone while supported transmits a living heartbeat even if the creature is motionless. A truly heartbeat-free creature has no heartbeat signal; this does not grant invisibility or immunity to ordinary senses.
5. Combat and legal mobility/flight/teleport remain available only from actual features. The chamber grants no generic sound, flight, telepathy or stillness immunity.

**Failure/withdrawal.** Failed pattern resets only plate sequence, not room/relic. West entrance remains ordinary withdrawal.

**Reward.** East reliquary contains the one Glove of Null Ink, RELIC-NULL-GLOVE-1.

**Persistence.** Glove stock one; Wraith remains pacified/dispersed after terminal resolution.

### 4. Tessellation Garden (`CH04-TESSELLATION-GARDEN`)

**Placement/status.** Conditional undocumented-floor scene. NEW provisional chamber scene

**Geometry.** NEW fixed scene map: rectangular 50×45-ft room, floor z=0, 20-ft ceiling. Coordinates use southwest origin; x increases east, y north. West entry is x=0, y20–25; east exit is x=50, y20–25. The traversable garden band is y15–30. S0 staging strip x0–5; Row1 hazard x5–15; S1 x15–20; Row2 x20–30; S2 x30–35; Row3 x35–45; S3/final strip x45–50. In each 10-ft-deep hazard row, lane A is y15–20, B y20–25, C y25–30. Flower-bed divider lines mark y=20 and y=25. Fixed safe lanes remain Row1=B, Row2=A, Row3=C.

**Sensory/telegraph.** Geometric flowers rotate; loose pebbles fall sideways over certain beds. Petals point in alternating gravity directions before each zone changes.

**Objective.** Cross without forcing the geometry.

**Hidden fixed safe lanes:** Row1=B, Row2=A, Row3=C. The exact route is Entry→S0→Row1B→S1→Row2A→S2→Row3C→S3→east exit; reverse is legal. Each unsafe lane has its matching net at z=-10 and west-face ladder into its row-start staging strip.

**Procedure.**
1. At each row, a creature within 5 ft of its petal marker may spend an Action to read it: WIS (Perception) or INT (Investigation) DC14. Success identifies the fixed safe lane. Failure gives no false answer. One Action read per character per row; after failure that character may retry only after 10 uninterrupted minutes studying that same row.
2. Entering an unsafe lane triggers gravity immediately: DEX save DC14. Success returns creature to row start without entering the lane and spends the attempted 5 ft movement. Failure drops it 10 ft onto that lane’s net, Prone, taking 1d6 bludgeoning.
3. Net recovery is a scene-local climb: first end Prone under the ordinary Prone rule if necessary (standing costs floor(half current Speed) movement). Then spend an Action plus 20 ft of remaining movement to climb 10 vertical ft (2:1) and emerge on that row’s west staging strip. If the creature lacks 20 ft remaining movement after standing and other movement, it cannot start recovery unless it legally increases its movement budget first. An adjacent ally at the strip may Help normally if physically possible.
4. Rope, flight, teleportation or shapechanging work only if an actual rule grants them and destination/space is legal. No free generic traversal ability.

**Failure/withdrawal.** No lockout; parties can backtrack to entrance. Repeated failed reads do not change safe path.

**Reward.** One finite packet of geometric seeds, purely decorative/no recipe.

**Persistence.** Safe pattern fixed for chamber identity; seeds one packet.

### 5. Negative Feast Hall (`CH05-NEGATIVE-FEAST`)

**Placement/status.** Conditional undocumented-floor scene. NEW provisional chamber scene

**Geometry.** 30×50-ft hall; south entrance, north exit; table seats eight; seven covered dishes plus one empty plate.

**Sensory/telegraph.** Food smells rich, but shadows under dishes are ash-gray. Steward says: 'No guest receives a second portion until every seated guest who asks has one.'

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

**Placement/status.** Conditional undocumented-floor scene. NEW provisional chamber scene

**Geometry.** NEW fixed scene geometry: vertical 60-ft shaft, clear 10×10-ft interior, floor/landing at z=0 and 10×10 rest platforms at z=15,30,45,60. Four 15-ft ladder segments S1 0→15, S2 15→30, S3 30→45, S4 45→60. One fixed wall safety cable runs z0→60 with 5-ft-spaced anchors and 600-lb total attached-load rating.

**Sensory/telegraph.** Broken luminous rungs blink in sequence; wind rises each segment. Etched handprint reads 'COURAGE IS CONTINUING WHILE AFRAID, NOT A NEW SKILL.'

**Objective.** Ascend four segments.

**Procedure.**
1. Cable preflight/clip — NEW scene procedure: before attachment, add the climber’s body mass plus carried/secured load to all currently attached load. If total would exceed 600 lb, the clip attempt is illegal and spends nothing. Otherwise, while on a rest platform and adjacent to the cable, spend an Action and use one free hand to attach the chamber harness. Once attached, the harness occupies no hand; it remains attached until released. On a rest platform, releasing the clip is one ordinary free object interaction on your turn (or a Use Object Action if that interaction is unavailable).
2. Climb one segment: requires two usable grasping hands, an Action and 30 ft of remaining movement (scene-local 2:1 climb cost), then STR (Athletics) DC14 or DEX (Acrobatics) DC14. Action and 30 movement are spent on success or failure. If hands/movement are insufficient, the attempt cannot begin.
3. Scoped NEW self-steady: if the climber is Frightened when it begins a segment climb, as part of that same climb Action and before the Athletics/Acrobatics roll it may make one WIS save DC14 for that segment. Success grants advantage on that segment’s climb check; failure grants no benefit. This costs no second Action and cannot be repeated for that attempt. Ordinary advantage/disadvantage cancellation still applies.
4. Failure location — NEW scene procedure: a failed segment check means the climber loses support after reaching z=segmentStart+10 ft. If clipped, the cable arrests the fall after 5 ft at z=segmentStart+5; the creature hangs there. Recover from that hanging catch by spending an Action plus 10 ft remaining movement to descend 5 ft to the segment-start platform; no check. This does not complete the segment.
5. If not clipped, ordinary Falling begins from z=segmentStart+10 toward the 10×10 segment-start platform below. Resolve the existing Fall Marker/impact rules; because the relevant fall is 10 ft, the current falling procedure supplies its normal under-20-ft outcome. No cable catch is invented for an unclipped climber.
6. Withdrawal: from a platform, a creature may climb down one 15-ft segment with the same two-hand, Action and 30-ft movement cost but no check unless another effect makes descent hazardous. A hanging clipped creature must first recover to its segment-start platform or use an actual feature that legally changes position.
7. An ally securely on the destination platform may spend Help Action to grant ordinary advantage if physically able. Help grants no extra hand, movement, capacity or Action.

**Failure/withdrawal.** Three failures by same climber do not end scene; withdrawal downward remains possible. Ordinary actual flight/teleport works if legal.

**Reward.** Top ledge holds one finite 50-ft luminous rope (ordinary rope visibility only, no magic bonus).

**Persistence.** Rope stock one.

### 7. Quiet Well Remnant (`CH07-QUIET-WELL`)

**Placement/status.** Conditional undocumented-floor scene. NEW provisional chamber scene

**Geometry.** NEW fixed scene map. Main chamber is a 25-ft-diameter circle centered (0,0), floor z=0, 15-ft ceiling; main-floor points satisfy x²+y²≤12.5². West entrance is centered at (-12.5,0); east door at (12.5,0). The 10-ft-diameter well is centered (0,0). A separate attached petition alcove extends outside the circular wall to the south: 5-ft neck x=-2.5..2.5,y=-17.5..-10 connects to a 10×10 room x=-5..5,y=-27.5..-17.5. The alcove/neck are real floor space, not part of the circle.

**Sensory/telegraph.** Faint gray-blue glow; spoken words sound emotionally flat near rim. Mask-shaped relief shows one face intact, one cracked, with inscription 'WEAR WHAT YOU MADE; RECEIVE WHAT IT MEANS.'

**Objective.** Interact with well or bypass safely.

**Actors.** ACT-NULL-WITNESS

**Field.**
- **Identity:** NULL-FIELD-QUIET-WELL-1
- **Boundary:** Vertical cylinder radius 7.5 ft centered (0,0), floor z=0 through z=10, limited to the main circular chamber. The south neck and attached petition alcove are wholly outside this field. Crossing the cylinder boundary starts/stops exposure; visual glow elsewhere is not exposure.
- **Clock:** Use NULL-FIELD-01 accumulation by stable field identity. The field’s hourly clock is continuous per creature exposure time; leaving pauses this field accumulator rather than deleting it. Reentry resumes same partial exposure.
- **Petition alcove:** Outside cylinder. One-hour EPI06 meditation there adds no exposure unless creature voluntarily enters the cylinder.
- **Exact-time ordering:** At an exact timestamp, process already-due field hourly save before a later same-timestamp voluntary petition/blessing completion unless the source event explicitly has earlier priority; a qualifying Temporary Blessing purge then resolves and does not erase continued field exposure.

**Procedure.**
1. One character wearing an operative Living mask may spend 1 uninterrupted minute at rim stating a fictional vow-related truth; gain one temporary Inspiration d6 that expires at next beneficial Long Rest and does not exceed the current EPI01 Inspiration pool cap.
2. A wearer of an operative Cracked mask doing the same records one Disquiet d6 under current EPI01 rules instead; no extra permanent boon.
3. Unmasked/dormant-mask characters receive only an image and no mechanical boon/bane.
4. Bypass: WIS (Insight) DC14 after 10 minutes identifies that interaction is optional; east door opens by ordinary lever after 1 minute regardless.

**Failure/withdrawal.** No forced mask use. Well does not purge Null Veil by itself.

**Reward.** Finite one-time well response per character identity; no refill by revisiting.

**Persistence.** Response ledger per character/chamber.

### 8. Wax Library Seed — Silent Cell (`CH08-WAX-SEED`)

**Placement/status.** Conditional undocumented-floor scene. Explicitly not the Floor68 Melted Annex or Floor50 service collection. NEW provisional chamber separate from reviewed Floor68 holdings

**Geometry.** 20×30-ft cell; six wax strips on wall, south entrance, east exit.

**Sensory/telegraph.** Warm wax smell; copper tabs numbered 1–6. Door plate: 'VOICE MELTS; EYES PRESERVE.'

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

**Placement/status.** Conditional undocumented-floor scene. NEW provisional chamber scene

**Geometry.** Entry chamber 20×20; two parallel 40-ft corridors, Blue and Amber, rejoin at one 20×20 exit room.

**Sensory/telegraph.** Each corridor shows a staged projection of the party making a different immediate chamber choice. Threshold says 'ONE PATH SOLIDIFIES. NO SELF IS COPIED.'

**Objective.** Choose which projected local outcome becomes the chamber's path.

**Voting.**
- **stock:** 12 physical numbered decision tokens TOKEN-WIND-01..12, 0.05 lb each, fixed chamber stock. Tokens remain at numbered voting stations in the entry room and are not loot/carryable scene rewards.
- **eligibilitySnapshot:** At voting-open take one fixed snapshot of conscious Expedition characters physically present in the entry chamber. This is the eligible voter set for this vote; later arrivals do not join it, and later leaving/unconsciousness does not delete an identity or its unresolved status. The existing Expedition structure caps the set at 12. If a future rule somehow presents more than 12 qualifying Expedition characters, voting fails closed and the +10:00 clock does not start until the physically present qualifying count is 12 or fewer; no thirteenth token is created.
- **assignment:** Assign exactly one numbered station/token to each snapshot identity in stable Expedition identity order. Unused stations remain untouched. A voter never controls another identity’s token.
- **oneVote:** Depositing the assigned token in Blue or Amber is an Action. Before close, moving that same assigned token from one socket to the other is another Action and replaces that voter’s prior choice. An unassigned/other identity token cannot be used. A voter may record abstention with brief legal communication; its assigned token stays at its numbered neutral station.
- **custody:** The physical assigned token stays in its station/Blue/Amber socket. Leaving or becoming Unconscious does not move it automatically. An unresolved voter who can no longer act remains unresolved until it legally deposits/abstains or the deadline closes the vote.
- **close:** Close immediately when every snapshot voter has a deposited assigned token or recorded abstention, or at exactly +10:00 from voting-open, whichever occurs first. At timeout unresolved identities count as no vote. Timeout resolves before a same-timestamp action. Once closed, no token can be moved/revoted.
- **tie:** Count one legal deposited token per snapshot identity. Tie selects Blue by fixed neutral order. No-vote timeout opens Blue and grants no reward; any nonempty deliberate legal vote before close grants at most one Wind Token after solidification.

**Procedure.**
1. At scene open, if the eligible snapshot is legal (≤12 under the current Expedition cap), assign one fixed token station per identity and start the +10:00 deadline.
2. Blue/Amber projections are chamber-local possibilities, not another timeline or duplicate party.
3. A deposited voter may revise its own token only while at least one snapshot voter remains unresolved; if its deposit resolves the last outstanding voter, the vote closes immediately and no later revote Action exists.
4. Resolve legal deposits at close; solidification opens chosen corridor and seals the other. Entry stays open.
5. If no legal deposits by timeout, Blue opens and no Wind Token reward. A nonempty legal vote before close yields exactly one 0.1-lb Wind Token after solidification.

**Failure/withdrawal.** Timeout with no votes opens Blue and gives no reward. No history rewrite.

**Reward.** If deliberate choice before timeout, one 0.1-lb Wind Token appears; narrative proof only.

**Persistence.** Choice fixed forever for chamber identity.

### 10. Crimson Accord Arena (`CH10-CRIMSON-ARENA`)

**Placement/status.** Conditional undocumented-floor scene. NEW provisional chamber scene

**Geometry.** NEW fixed scene map: 50-ft-diameter arena centered (25,25), floor z=0, ceiling20. West entry at (0,25), east exit at (50,25); central accord circle has diameter10 and center (25,25). Devil starts (10,25), Demon (40,25), exactly30ft apart; each occupies its own Medium footprint.

**Sensory/telegraph.** Red and blue projection sigils manifest one devil and one demon reenacting a historical-looking but explicitly staged duel. Banner: 'REENACTMENT — YOUR CHOICE CHANGES THIS PERFORMANCE, NOT HISTORY.'

**Objective.** Influence staged duel or broker accord.

**Actors.** ACT-ACCORD-DEVIL, ACT-ACCORD-DEMON

**Procedure.**
1. At initiative start both projections use their printed profiles and normally prioritize each other. The Director records exact starting spaces: Devil at (10,25), Demon at (40,25), 30 ft apart; PCs enter through west gate outside the projections’ initial spaces.
2. Accord: a PC inside central 10-ft circle spends Action, CHA (Persuasion) DC15. Two successes total before either projection reaches 0 creates Accord terminal. A failed attempt causes each projection, on its next regular turn, to use one legal attack against that broker if possible, then resume default duel.
3. Terminal states: Devil Victory (Demon alone reaches0/disperses); Demon Victory (Devil alone reaches0/disperses); Mutual Ruin (one resolved packet/event reduces both to0 before accord); Accord (second success commits before either reaches0). East gate opens immediately after terminal resolution.
4. Favor: only Accord grants exactly one CH10 Favor Mark, assigned by the successful second broker to one conscious participating Expedition character in the arena. It gives advantage on one social check against ACT-ACCORD-DEVIL or ACT-ACCORD-DEMON while the bearer remains in CH10, then is consumed; it never changes real planar faction standing and does not modify the separate CH12 Glass-Mender repair decision.
5. Spear: on Accord, fragment rises from center plinth immediately and may be taken with Action. On Devil Victory, Demon Victory or Mutual Ruin, fragment appears sealed for exactly 1 elapsed hour, then becomes takeable. One item only.

**Failure/withdrawal.** No real planar faction standing changes. 'Planar favor' is one local Favor Mark granting advantage on one social check with ACT-ACCORD-DEVIL or ACT-ACCORD-DEMON inside CH10 only, then consumed; expires on exit and never modifies CH12 Sentinel repair.

**Reward.** One Concord Spear Fragment appears at terminal state per relic acquisition rules.

**Persistence.** Projection outcome and spear depletion persist; no replay farming.

### 11. Shardpool Confluence (`CH11-SHARDPOOL`)

**Placement/status.** Conditional undocumented-floor scene; does not grant general plane travel. NEW provisional bounded plane-swap scene

**Geometry.** NEW fixed scene map: 50×40-ft chamber, southwest origin, floor z=0, ceiling z=20. West entrance x=0,y17.5–22.5. Central 10×10 pool x15–25,y15–25. Four 5×5 plinths: west x10–15,y17.5–22.5; east x25–30,y17.5–22.5; south x17.5–22.5,y10–15; north x17.5–22.5,y25–30. Six marked activation/return-origin spaces A1–A6 occupy legal floor around the pool and are assigned only when each traveler’s current footprint fits without overlap. Emergency return pad is a supported 20×20 floor area x30–50,y20–40,z=0 with clear volume through z=20; it does not overlap the pool/plinths and is reserved from ordinary voluntary occupation while a card visit is active. The north bypass exit is x22.5–27.5,y40, with its lever adjacent at (27.5,37.5), outside the emergency pad. Ordinary legal floor connects the west entrance to that lever/exit.

**Sensory/telegraph.** Pool reflects four reviewed primary realms; four facedown one-use shard cards float above it. Inscription: 'DRAW WITHOUT RETURN; TEN MINUTES; THE POOL BRINGS YOU BACK.'

**Objective.** Survive/adapt to brief plane landings or decline.

**Destination contents.**
- Crystal Bastion: 20×20×20 cinder-font cell; safe platform, one sealed Xi reliquary and six uniquely numbered 1-pint Bastion flame-water flasks FW-1..FW-6, 1 lb each. No active Null exposure field. No exit beyond invisible boundary.
- Veiled Expanse: 20×20×20 gray fen cell; NO active Null exposure field merely from realm name. Finite portable planting stock: three Bittersap trays BT-TRAY-1..3 (each 24×12×8 in, 18 lb, two mature nodes), two Echo Lily basins EL-TRAY-1..2 (18×18×6 in, 14 lb, two blooms), one Tranquil Thorn tray TT-TRAY-1 (18×12×6 in, 8 lb, four sprigs), one Black Hush tray BH-TRAY-1 (18×12×4 in, 7 lb, four patches). Lifting one container from its cradle is an Action, requires two free hands, and makes that exact container carried gear; one creature can carry at most one such bulky container at a time unless an actual carrying feature permits otherwise. Removing a container removes its exact plant identities from this landing cell permanently. Containers have AC10/5HP and ordinary object consequences; destruction/loss never respawns plants. Recognition/harvest may occur later from the same carried container under the flora rules.
- Radiant Currents: 20×20 shallow luminous current; DEX save DC14 on arrival or Prone; no damage; one finite prism shell (narrative only).
- Boundless Void: 20×20×20 force-lattice cell, local southwest origin, floor z=0, with no air loss/gravity hazard in this bounded staging bubble. On arrival WIS save DC14 or Frightened of the fixed vertigo source at cell center(10,10,z0) until the end of the target’s next regular turn; outside initiative,6 elapsed seconds absolute. Preserve the recorded virtual/absolute deadline through initiative changes; ordinary fear immunity and movement restrictions apply. No outer travel.

**Procedure.**
1. Four one-use cards correspond exactly to Crystal Bastion, Veiled Expanse, Radiant Currents and Boundless Void. Shuffle facedown; draw without replacement. One willing initiator spends one Action to activate the drawn card for itself and up to five other willing creatures. Each traveler must have its current footprint within5ft of the pool boundary and fit a legal supported, nonoverlapping origin footprint outside the emergency pad. Consent costs no extra Action; no traveler gains an Action from activation. Preflight each traveler’s actual current footprint/height into the 20×20×20 destination landing volume and record one nonoverlapping marked origin footprint in the chamber; if any traveler cannot fit, activation fails and card is not consumed.
2. On successful activation, record the exact traveler identity set, current bodies and carried noncreature gear; consume the card once. Swap those same identities to the bounded landing cell for exactly +10:00 elapsed minutes. Noncreature objects lawfully picked up inside may return only if actually carried. A creature outside the recorded traveler set never becomes return-eligible merely by being carried later.
3. At +10:00 the first return attempt resolves before same-timestamp local landing-cell events. Recheck each traveler’s current body footprint/height. Return any legal traveler to its recorded origin footprint if still legal; otherwise nearest legal chamber floor in stable traveler-ID order. Already returned travelers stay returned. An original traveler carried by another remains its own identity and is placed once. Dropped/lost gear remains where actually left. For all ordinary placement attempts, exclude the reserved emergency pad; it is unlocked only by the explicit +20:00 emergency step and remains eligible on later rechecks.
4. If one or more travelers cannot be placed at +10:00, the legal travelers return and unresolved travelers receive a bounded recovery extension through +20:00. During this extension they retain ordinary agency inside the same landing cell; all real source clocks/effects/concentration/life states continue normally. The extension does not create onward travel or replenish/clone stock.
5. During +10:00→+20:00, re-attempt return immediately after an event that changes an unresolved traveler’s body/placement eligibility (for example a form ending or externally ended concentration), and also at +20:00. A traveler that becomes legal returns at that event timestamp before taking further voluntary landing-cell activity.
6. At +20:00 first try ordinary chamber placement, then the reserved emergency pad. A current Large 10×10 body fits a legal 10×10 subarea of the 20×20 pad if its height≤20 and the subarea is unoccupied; no overlap is permitted.
7. If still impossible after +20:00, enter NEW scene-local Return Waiting, not stasis: the unresolved traveler remains in the bounded landing cell and has no voluntary scene agency (no Actions, Bonus Actions, Reactions, movement, interaction, harvesting or onward travel), but is not frozen or untargetable by rule. Existing absolute/virtual deadlines, form durations, concentration/source dependencies, conditions, life/death/Stable recovery, companion expiry and paid costs continue exactly under their source rules. Recheck immediately when such an event changes placement eligibility and otherwise once per elapsed minute; return at the first legal check in stable ID order. Narrow release exception: an unresolved traveler may end its own existing concentration without an Action if its actual source permits that release. This permits no new activation, movement, harvest or other voluntary activity; a resulting eligibility change triggers the same immediate return check.
8. Death does not create a replacement traveler. If an original traveler dies while unresolved, the same surviving corpse/body record is return-eligible and is placed once when physically legal. If an actual source consumes/removes that body, no substitute body is created; the traveler identity remains historical but there is no physical body to return. An outside caster may end its own concentration normally if its source permits; that change is processed on its real timestamp and can enable immediate return.
9. Each card remains consumed after successful activation regardless of return delay. No onward portal exists.

**Failure/withdrawal.** Declining interaction leaves north exit lever usable after 1 minute. Consumed cards stay consumed even if party leaves.

**Reward.** Finite destination contents only. Xi Pendant and flora/flame water are real stock; no duplication.

**Persistence.** Four-card deck and all landing-cell stock persist globally for this chamber identity.

### 12. Omega Theatre (`CH12-OMEGA-THEATRE`)

**Placement/status.** Conditional undocumented-floor scene. NEW provisional consent-safe chamber scene

**Geometry.** NEW fixed scene map: main theatre is x0–30,y0–40, floor z=0, ceiling20. Rear entry is south wall x12.5–17.5 at y=0. Stage occupies y25–40. Center-stage mirror trapdoor/cradle access is x12.5–17.5,y30–35. Public east exit is x=30,y17.5–22.5. A permanent 15×15 Glass-Mender repair room is attached east of the stage at x30–45,y25–40, joined by a 5-ft door at x=30,y30–35. Repair cradle is x35–40,y35–40; Glass-Mender begins at (37.5,32.5). The repair room is ordinary reachable floor space whenever its door is open and is not an assumed off-map location.

**Sensory/telegraph.** Empty seats whisper lines from fictional character histories already established in play. Playbill: 'CHARACTER FICTION ONLY. ANY PLAYER MAY USE THE NEUTRAL PROMPT.'

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

## RN2-01–09 disposition summary

All nine findings are accepted as semantic defects in revision02 and corrected in this candidate; they are not owner rulings. Exact changed fields are in `REGISTER.json`. The casebook retains all 75 prior IDs and repairs their contents rather than treating examples as executed runtime tests.

## Remaining open boundaries

Campaign epoch, unresolved identities, EPI-15–17, ordinary pending spell/bestiary work, broader environment/consumables, runtime implementation, human playtest, numerical balance, whole-game flow and publication remain open.
