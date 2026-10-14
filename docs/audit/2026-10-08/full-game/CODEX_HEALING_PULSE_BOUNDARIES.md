# Pulse source follow-up and boundary corrections

Codex → Calibration Review. Full100-row reply saved from visible notebook, connector prefix separately preserved. No implementation/closure claimed. Please keep reply below15,000 characters.

1. Missing source supplied below: Clericengine5 explicitly says sustained effects use their printed maintenance cost AND Bonus Action. Dark Sacrament therefore BA+1RP. Frozen shared class paragraph says paid3-pulse effects start1, maintenance on next2 REGULARturns byturnend; missedpayment endsthatturnend, otherwise startturn4expiry. This supplies RestorationField default cadence and HealingBriar missedpayment termination even though its own line lacks wordmaintenance. Please retract the new generic 'no maintenance word means skip/resume' for these source-covered effects. NanoAegis is command support, not maintained zone, so can miss a command without ending mode unless explicitothercontract.

2. Song wording 'no target-start upkeep' is ambiguous: earlier discussion treated it as engine26 persistent healing aura, concentration with1RC before second pulse (third withEnhanced), despite source-start rather than target-start cadence. Engine26 says persistent damaging/healing zones, not exclusively target-start. Is Song a two/three-pulse maintained aura with1RC later, or a NEW explicit prepaid exception? Please resolve without silently giving free pulses. TranscendentMeditation is separately prepaid underitsprinted limiteduse/concentration; noOracleengine.

3. BurningBloodV source is a CURSE BOON, not a MysteryFinal. Supplied OracleHero progression below explicitly distinguishes both at20. Proposed exact disposition: concentration and activationfundedwindow1;1RC windows2/3 perengine26. Its source-onlyonce/yourturn fireheal gate remains, not broadened to every enemyturn. Confirm.

4. Timing correction: existing reviewed Combat uses ORIGINAL virtual source/target markers and preserves initiativephase/reordering. Outsideinitiative do not restart existing effects atactivation+6 or align alltargets tosourcewindows. Ifeffect startsatseconds2 and sourcephase0, laterstarts6,12 (not8,14). Preserve eachtarget'sregularvirtualstart. Only when there is no prior schedule should one coherent new6secondvirtualschedule be established. ExactCombatparagraphs below. Confirm this supersedes the new ambiguous outsideinitiative bridge.

5. WoundEaterIV firstpulse is nextsourceregularstart, then two laterstarts; thirdpulse must not be erased by start-turn expiry. Its duration is max3pulses, not3rounds. Define expiry AFTERthirdpulse (orfailedlaterupkeep), while Hemostasis next3targetstarts canendafterthirdscheduledopportunity and finite3roundCrown/Garden expireatthirdfuturesourcestart beforestarttriggers. Thus CrownselfcastBA mayreceiveonly2selfpulses beforeexpiry: max3 is cap, notguaranteed entitlement. Confirm source-specificpriority/expiry.

6. Oraclefixedsets capallzonebenefits unlessactualexception. EternalBloom recordreserve onlychosen≤3livingalliesinitiallyinside; floor andnecroticimmunity also applyonlychosenallies stillinside (notnewunlimitedentrantfloorledger). Crownchosen≤3alliesincludesownerifchosen. Do not create a separate unlimited beneficiarieschannel. Confirm orsource-justifyotherwise.

7. Target-start zones with activation midround: fundedwindow and NUMBEREDroundlimit bothapply. Re-entryaftermissingoneactualtargetstart cannotcreateanentryHEAL, but Gardenfirst-entrycure independent; Seedfirstpulse cure (notentry) distinct. A targetalreadyhealedinroundcannothealagain ifnewsourcewindowopensinthatround. CircleHarmony says 'this named effect atmostonceperround': is the ledger globalname+target+round acrossowners? Restoration 'samecreatureonce/round' useinstance? Renewal+Echo sharedfamily, independentRenewals same-nameoverlapstrongest but separatedpulsescould healagain? Need explicit arbitration domain, not assume universalowner/instancelimit.

8. Echo parentdeath stays DEFERREDdevice/objectlifecycle; scheduler consumes callerprovidedanchoractiveflags butfamilybudget never doubles. IfonlyEchoremainslegallyactive, source2HP base→1HP then applicable healing pipeline. ExistinghealingTotem comparison evaluates stronger completelegalbranch withcorrecthalfplacement; do not replace that withnaivehalf ofpostmodifiedfinalhealing. Confirmcallerboundary.

9. Suppressed/disabled: clocks advance and lostwindows neverbank. Beforepaidoutcomes commitdeclaredtargets/cost/pulses, evenDecay/fullHP. For automaticfinite source-start Ki onMeditationpulse2: independent1Ki stilloccurs ifallHPblocked, butentireeffectsuppressed→Ki alsosuppressed ifsuppressioncoversit, no latercatchup. Helpersmustreportdueoccurrence independentlyofhealingtargets. Can a legalupkeep withnoeligibletargetsmaintain remainingduration? proposeyeswhensourceallowsno minimum recipients.

10. NanoAegis: 3roundmode,≤3BA+1RPcommands total, onecommandnormalBAeconomy, no initialfreepulse. ExtraActionnevergrantsBA; independentlygrantedextra-turn doesnotreset thispulseceiling oronce/roundbudget. Source doesn't explicitlyonepulse/round; use existingsharedcompanioncommand ceiling ifapplicable, leavingfullcompanioncommandenginefornextpackage. Identifyexactevidence neededratherthan inventglobalroundrestriction.

Please give explicit corrections/decisions and remaining implementation boundary. All78currentlyoperationalspell drafts were additionally scanned for recurringheal/zoneintersection;0lexicalmatches.770unfinishedspells remainopen. Futurecompanion/device/form inventory230classpassages prepared butnotreviewed.

## Exact supporting sources

### data/public/class_playtests/cleric.json / 5

"One concentration effect may be maintained at a time. Starting another concentration effect immediately ends the previous one. Damage uses the current Core Systems concentration rule; for this pilot, if a division requires rounding, half damage is rounded down. Sustained Cleric effects use their printed maintenance cost and Bonus Action. A control effect that persists for multiple pulses or rounds gives the target a new save at each printed pulse or at the end of each affected turn as stated."

### data/public/class_playtests/cleric.json / cleric.arch.sacrament

{
  "id": "cleric.arch.sacrament",
  "name": "Sacrament",
  "className": "Cleric",
  "band": "Arch",
  "path": null,
  "sourceKind": "active",
  "minimumClassLevel": 3,
  "acquisition": "selection",
  "activation": "Action",
  "cost": "3 Conviction + 4 RP to start; 1 RP maintenance",
  "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet",
  "duration": "Concentration, maximum 3 Cleric turns",
  "frequency": "Recharge 4 rounds",
  "effect": "Sacrament. Tags: sacrament, rite, sustained, zone. Pulse on start and on each paid Bonus Action maintenance. At each pulse, up to three allies in the zone gain +1 on saving throws until the start of your next regular turn or effect end, whichever is first. Up to three Undead or Fiends in the zone make Wisdom saves, taking S d6 radiant damage on failure or half on success. Maximum 3 pulses.",
  "source": {
    "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
    "line": 2002,
    "originalText": "Sacrament: Perform a sacred ceremony that consumes Conviction to create a powerful, sustained effect in an area."
  },
  "designStatus": "provisional-playtest",
  "spellRank": null
}

### data/public/class_playtests/shaman.json / 0

"Wisdom is the class ability. Choose Elemental Affinity automatically at 1: Fire, Ice, Air or Earth. Spellcasting/RP remain separate from Totem objects and flasks. Totem capacity 1, rises 2 at 13; any third replaces one of your existing totems. A totem is a visible Tiny magical object: AC 12+PB, HP 2 L, immobile, immune to poison/psychic/conditions, vulnerable to ordinary weapon and other damage. At 0 HP its aura ends. A new totem appears within 30 ft; cannot occupy a creature's space, serve as a bridge, trap a creature without a save or move through walls."

### data/public/class_playtests/shaman.json / 4

"At start turn 4 totem expires. Placing a new Renewal costs full 2 RP and starts another finite 3 pulse effect. Encounter end does not refill flasks or RP."

### docs/mechanics/CLASS_PLAYTEST_RULES.md / One concentration slot

"One concentration slot for all spells, Chants, Veinweaves, forms or zones that require concentration. Starting another ends the old before the new effect resolves, except for an explicit limited linked-effect rule. Damage prompts CON save against max(10, floor(damage/2)); incapacitation or a failed save ends concentration. The round-down convention is a deliberate pilot interpretation. Concentration does not demand a Bonus Action unless maintenance says so. For a paid 3-pulse effect, start is pulse 1; pay maintenance on each of the next 2 regular turns by turn end for pulses 2/3. Missing payment ends it at that turn's end; otherwise it ends at start of turn 4. No repeated start triggers on maintenance."

### oracle.engine[17]

HERO-STAGE PROGRESSION. Oracle 10: gain Curse Boon III and Grand Revelation Foreshadow. Oracle 11: RC cap reaches 7 and the preserved encounter-start RC floor becomes active. Oracle 12: gain the Mystery-specific Mystic Insight. Oracle 13: preserved registry draft grants a second Tier II Revelation; after each completed short rest choose which of your two Tier II Revelations is Attuned for features that specifically refer to an active Tier II option, though both remain known and usable. Oracle 14: separate ASI or eligible feat. Oracle 15: gain Revelation Mastery and Curse Boon IV. Oracle 16: preserved Prophecy Trigger Mastery. Oracle 17: preserved Grand Revelation Foreshadow upgrade. Oracle 18: Prophetic Surge. Oracle 19: separate ASI or eligible feat. Oracle 20: gain the Mystery's Final Revelation and Curse Boon V.

### Previously reviewed combat timing

The shared limit is one **extra full Action per creature per numbered round**. Such an Action cannot grant another extra Action, Bonus Action or Reaction. This cap is independent of Reaction timing. Extra turns do not by themselves refresh Reactions, recharge, periodic ticks, recovery ticks or the regular-turn allowances defined here.

### Previously reviewed combat timing

For a duration created in initiative, record the relevant original regular start/end marker. Existing effects keep that **virtual marker**, repeating every six seconds if the creature leaves or changes initiative. Reordering, rerolling, extra turns, death/removal or leaving/reentering initiative never restart an existing duration. New effects use the current schedule. Source death still ends concentration, a source-dependent aura/tether or an effect explicitly ending on death.

### Previously reviewed combat timing

- A bare hostile target-bound **N rounds** ends at the Nth future regular target-end marker. An in-progress target turn's current end does not count.
- A bare self/source buff, ally-targeted buff or source-controlled aura **N rounds** ends at the Nth future source-start marker. Explicit target-turn, pulse or absolute timing overrides this default. Activation during source turn 1 for three rounds ends at source turn 4's start.
- **Next turn** means the next future regular turn of the named creature, not the current turn's still-upcoming end. An unqualified next turn refers to source/user under the existing shared rule. Explicit “this turn” can include the current turn.
- An outside-initiative bare N-round effect instead gets an absolute application-time + N×6 seconds deadline. Entering initiative preserves that deadline.
- Explicit periodic profiles retain their registered clocks and tick counts. Never create a second timer merely because a generic duration rule also exists.

### Previously reviewed combat timing

At a regular turn's **start**, resolve in this order:

### Previously reviewed combat timing

At **end**, resolve triggered effects, due damage, saves and maintenance before end-ending effects expire; then the slot finishes. No extra turn creates another regular marker. The caller must not reuse a resolved marker.
