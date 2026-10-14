from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
data=json.loads((ROOT/'data/playtest/healing_pulse_bindings.json').read_text(encoding='utf-8'))
for row in data['bindings']:
    if 'GPT_HEALING_PULSE_BOUNDARIES.md' not in row['reviewEvidence']:row['reviewEvidence'].append('GPT_HEALING_PULSE_BOUNDARIES.md')
    if not any('BOUNDARY CORRECTION' in v for v in row['operationalOverrides']):
        row['operationalOverrides'].append('BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.')
(ROOT/'data/playtest/healing_pulse_bindings.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header="""# Exact pulse implementation review

Codex → Calibration Review. Reply below15,000 characters. Review exacthelper/tests/guide against100 suppliedclassrecords plus6supportingpassages. Source integrity passes;71targetedchecks and301 reservepartitions pass. Original books/cards/frozenclassguide unchanged. Broader gameopen.

Implemented families: maintained BA windowsincludingLifewellfirstBA; Song/EnhancedlaterRC; prepaidMeditation/Bloom; delayedWoundEater/Hemostasis; Oraclefundedtargetwindows; Nano commandcap; fixed/repickedrecipients; Circle globalnamedbudget versus Field/Oracle/Renewalfamilyinstance; nativecadence withoutthreecap;finiteBloompartitions; Garden/Seedcontactentitlements; sourcebaseRenewal/Echo alternatives.

Caller boundary is deliberate: exact original virtualmarkers and actualsourceauthorizedexpiry; canonicalRP/RC andBAavailability; initialcosts alreadycommitted; actualsourceownership/targetlegality andsidecaps (3allies+3enemies, never6allies); range/alive/line-of-effect; allowedsuppression/maintenance; concentration/source-death state; olddeviceanchorlifeandcommandbudget. This is a boundedreference, notfullclassexecution. BlockedHP/Decay/fullHP doesnotbecomewhole_effect_suppressed.

Specific reviewquestions:
1. EnhancedGarden says 'firstGardenpulse' whilebasecure saysfirstentryORstart. Candidate treatsEnhancedvariant asreplacingbasecontact entitlement withfirst-pulse cureboth (oneentitlement, noentrycurethenextraenhancedcure). Explicitlyproposedin guide; please confirmorcorrect.
2. Entireeffectsuppressed scheduledoccurrence stillconsumesownopportunity/window, butgrantsno namedbenefit anddoesnotclaimglobalCirclebenefitledger; onlyHPgainblocked stillclaimsthenormalbenefitbudget. Confirm.
3. UnfinishedChorus ownturn drain is modeledinitialincluded, one laterownregularturnpaid1RC withnoBA, fixedroster≤3+3 butoneenemy/onehealdestinationperpulsecheckedbycaller. Firstreplysourceclassification saidincludedfirstsource-turnpulse. Please verifyexacttiming/end.
4. Earlierwording invoked 'alreadyreviewedhealing/totemarbitration' forEcho. Actual existinghealing_packet Totembranch rule is BLIGHT reduction, notEchoRenewal. I have explicitlylabeledEcho shared-family/strongestpreview assource-specificintegration ratherthanpretendingexistinghelperalreadyimplementsit. renewal_branch_bases returns2parent/1Echo alternatives ONLY; callerpreviewsappropriatelymodifiedbranchesandcommitsone. Parentdestruction remainsdeferred.
5. Sameopportunity independentRenewals strongestnonstack isguide/callerarbitration; helperreceivesalreadywinnerlegalapplication. Separateinstancesatdifferenttimesmayeachhealsameround. NoinventedglobalRenewalroundcap.

Please identifyconcretedefects beforeboundeddisposition, includingclocksatlateobservations, paymentfailures, fixedrosters, missedpulses, suppression andsubtle sourceexceptions. All100classificationrows staydiscussionroleonlypendingthisreview; closure ifgrantedappliesonlysuppliedroles/schedulerprimitive, notwholecards. Broadercompanion230candidateinventory awaitsnextconference.

"""
parts=[header]
for name in ('docs/mechanics/HEALING_PULSE_PLAYTEST.md','tools/healing_pulse_playtest_rules.py','tools/validate_healing_pulse_playtests.py','docs/mechanics/HEALING_PULSE_PLAYTEST_VALIDATION.json','docs/mechanics/HEALING_PULSE_SOURCE_VALIDATION.json','docs/mechanics/HEALING_PULSE_SUPPORT_VALIDATION.json'):
    parts+=['## '+name,'',(ROOT/name).read_text(encoding='utf-8'),'']
parts+=['## Complete100 source-role bindings','',json.dumps(data,ensure_ascii=False,indent=2),'']
(HERE/'CODEX_HEALING_PULSE_IMPLEMENTATION_REVIEW.md').write_text('\n'.join(parts),encoding='utf-8')
print('Built exact pulse implementation review.')
