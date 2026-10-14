from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
lines=['''# Exact maximumHP implementation review

Codex → Calibration Review. Please reply below15,000 characters. Review the exact helper, tests, guide and58 role bindings below against your source discussion and five boundary corrections. Current60checks/909systemicstatesPASS;58sourcehashes/liveobjects match. Challenge concrete defects before boundedclosure.

Implemented: unmodifiedbase+compatiblebonuses−GLOBALstrongestMonk then rationalfactorproduct flooronce; max/currentclamp non-damage; independent application clocks/suppression/targetrest; sameFleshAscendantengine/cardidentity; explicitNEWWizardstackexception; Conjurationcreationlevelsnapshot; dynamicotherbonusformulas; Toughacquisitionsnapshot; strictfirstfallcrossingsusingeventmax; genuinehealed-abovehalfexit; historicalRewindpredicate; percentageamountswithsourceownedminimum; priorCoreWound/HP/concentrationmetricsfrozenbeforeMonktrauma.

Caller boundary: record numericamount must be built from a legal actualsource/formula and eligibility; helper doesnotinferownership/control/equipment/acquisition, performcompanioncreation, payactions/costs, generateclockmarkers, consume firstfalluses orrefillHP. Source_amount computes documentedformulas andcallerrefreshesdynamicbonuseswhenlevelchanges. A record's suppliedearlierendpoint is allowed ONLYif anotheractualsource providesit; no invented earlierend for theseMonkcards. Preserverest-endingrecords evenwhensuppressed; do notmergeseparateapplications.

Narrow predicatecheck: HpEventSnapshot.damage_left_below_half for Rewind means realHPdamagedecrease leavingrecordedtargetbelowhalf, notnecessarilycrossingfromabove. Its source says 'if recorded damage had reduced it below half' without 'first fall'; broaderearlierhealinginterface didnotrequirefirstcrossing. Confirm orcorrectthisprecisedifference fromfourfirstfallcards.

The58recordscope includesguards,percentages andthresholds; itdoesnotpromoteentireLifeDrinker/familiar/featclass engines. Otherdomainsincludingallunsuppliedmodifiers,devicehalfmax1viability,levelupbaseHP/multiclassconstitution,companionlife/control,featretraining andrealbalance remainopen.
''']
data=json.loads((ROOT/'data/playtest/maximum_hp_bindings.json').read_text(encoding='utf-8'))
lines += ['## Exact58 role bindings',json.dumps(data,ensure_ascii=False,indent=2)]
for path in ('tools/maximum_hp_playtest_rules.py','tools/validate_maximum_hp_playtests.py',
             'docs/mechanics/MAXIMUM_HP_PLAYTEST.md','docs/mechanics/MAXIMUM_HP_PLAYTEST_VALIDATION.json',
             'docs/mechanics/MAXIMUM_HP_SOURCE_VALIDATION.json'):
    lines += ['## Exact '+path,(ROOT/path).read_text(encoding='utf-8')]
(HERE/'CODEX_MAXIMUM_HP_IMPLEMENTATION_REVIEW.md').write_text('\n\n'.join(lines),encoding='utf-8')
print('Prepared maximumHP exact implementation60checks/909states; not yet closed.')
