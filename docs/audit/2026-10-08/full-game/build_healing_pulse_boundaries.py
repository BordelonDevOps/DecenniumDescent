from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
support=json.loads((HERE/'HEALING_PULSE_SUPPORTING_SOURCES.json').read_text(encoding='utf-8'))
oracle=json.loads((ROOT/'data/public/class_playtests/oracle.json').read_text(encoding='utf-8'))
combat=(ROOT/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md').read_text(encoding='utf-8')
packet="""# Pulse source follow-up and boundary corrections

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
"""
lines=[packet]
for row in support:lines+=['### '+row['sourcePath']+' / '+str(row['selector']),'',json.dumps(row['value'],ensure_ascii=False,indent=2),'']
for i,text in enumerate(oracle['engine']):
    if text.startswith('HERO-STAGE PROGRESSION.'):
        lines+=['### oracle.engine['+str(i)+']','',text,'']
for paragraph in combat.split('\n\n'):
    if paragraph.startswith(('For a duration created','- A bare hostile','The shared limit is one','At a regular turn','At **end**')):
        lines+=['### Previously reviewed combat timing','',paragraph,'']
(HERE/'CODEX_HEALING_PULSE_BOUNDARIES.md').write_text('\n'.join(lines),encoding='utf-8')
print('Built pulse boundaries with exact supporting evidence.')
