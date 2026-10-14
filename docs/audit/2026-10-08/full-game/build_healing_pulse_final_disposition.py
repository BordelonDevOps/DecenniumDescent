from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
header="""# Pulse implementation corrections and exact final disposition

Codex → Calibration Review. Please replyunder12,000characters withremainingconcretedefects orboundeddisposition.

Your exactimplementationreview was preserved separatelyfrom thelaternotebook provenance instruction. Implemented requiredfixes:

- Sequence/delayedsequence laterpaidmarker: iflegalwalletpaymentfails, effectendsatdue marker beforeanytargetledger/declarationcommit. Song/EnhancedSong/WoundEater cannotretrywithnewRCatsamemarker.
- Exactpaidmarker withupkeep_legal=False nowendsatthatduemarker. Oraclefund alsoendswhenactualrequiredsourceupkeepisillegal.
- regular=False onextra-turnattemptrejectswithoutendingattheactualsame pendingmarker; by-turn-endmaintenance failed early payment remainspendinguntildueend.
- Addedreplay, illegalupkeep, extrasourcecall andsuppressedCircle sharedbenefitledger regressions.
- EnhancedGarden entitlement nowlabeled NEWsource-specificmasteryintegration, asapproved; UnfinishedChorustwopulse/noBAandEchoRenewalvsBlightarbitrationdistinctionretained.

Current89targetedchecks+301reservepartitionsPASS. Addedexplicitprovenancemap:24scheduleprofiles+6nativeprofiles+3contactvariants=33alllinkedtoactualsupplied100+6sourceIDs. No newability/spellnamesorcontentintroduced. Internalshortlabelsarealiases, notadditionalcards. Originalsourceobjects/frozenclassguide remainunchanged. All priorcallerboundariesremain: actualinitialcosts, acquisition, source/target/sidecaplegality, originalvirtualmarkers, canonicalwallet/actioneconomy, objectlifeandcompanioncommandbudgets, andactualhealingpipeline/independentcomponentresolution.

Full correctedhelper/tests/guide/reports/mappings below. Original100sourcebindingtexts areunchanged fromexactpacket; sourceintegrityPASS100+6. Pleasecloseonlythe supplied scheduling/roleinterfaceifappropriate, leavingfullcards/companionlife/770unfinishedspells/othercatalogs/wholegameopen.

Nextpreparedreview:74device/Totem passages (73lexicalTinker/Shaman + explicitMagneticWallsemanticaddition) plus3frozenguidesources. MagneticWallwasnotinprior39redirectionset andwasmissedbyfuture230lexicalpattern; itisnowcapturedandhashverified explicitly. Noassumptionthatlexicalcountsmeantcompleteness.

"""
parts=[header]
for name in ('tools/healing_pulse_playtest_rules.py','tools/validate_healing_pulse_playtests.py',
             'docs/mechanics/HEALING_PULSE_PLAYTEST.md','docs/mechanics/HEALING_PULSE_PLAYTEST_VALIDATION.json',
             'data/playtest/healing_pulse_profiles.json','docs/mechanics/HEALING_PULSE_PROFILE_PROVENANCE.json',
             'docs/mechanics/HEALING_PULSE_SOURCE_VALIDATION.json','docs/mechanics/HEALING_PULSE_SUPPORT_VALIDATION.json'):
    parts+=['## '+name,'',(ROOT/name).read_text(encoding='utf-8'),'']
(HERE/'CODEX_HEALING_PULSE_FINAL_DISPOSITION.md').write_text('\n'.join(parts),encoding='utf-8')
print('Built89-check exact pulse correction packet.')
