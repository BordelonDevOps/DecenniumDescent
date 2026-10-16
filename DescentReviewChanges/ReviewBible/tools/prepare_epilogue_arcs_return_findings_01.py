"""Record independent semantic findings against the preserved first actual arc return."""
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    root = A / 'cosmology-epilogue-campaign-arcs-01-return-01'
    out = A / 'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_SEMANTIC_REVIEW_01.json'
    message = A / 'EPILOGUE_ARCS_RETURN_CORRECTION_REQUEST_01.txt'
    assert not out.exists() and not message.exists()
    model = json.loads((root / 'CAMPAIGN_ARCS_MODEL.json').read_bytes())
    player = (root / 'PLAYER_CHAPTER.md').read_text(encoding='utf-8')
    director = (root / 'DIRECTOR_CHAPTER.md').read_text(encoding='utf-8')
    cases = json.loads((root / 'CASEBOOK.json').read_bytes())
    findings = [
      {'id':'AR1-01', 'severity':'procedure-conflict',
       'locations':['/arcs/0/containment/procedure','/arcs/0/containment/incomplete','PLAYER_CHAPTER.md: Stabilizing a recovered fragment','DIRECTOR_CHAPTER.md: Containment stock'],
       'evidence':{'model':model['arcs'][0]['containment'],'player':'For each fragment: fit, close shutter, turn crank for 10 uninterrupted elapsed minutes.'},
       'finding':'The model permits 1–3 fragments in one cycle; the player chapter requires an entire cycle for each. Both chapters also need to retain actual active cranking, interruption and later-addition handling.',
       'proposedCorrection':'Fit each actual fragment with its own Action; close the single shutter once; one worker turns the crank for 10 uninterrupted active minutes. That one completed cycle seals every installed fragment. Three fragments from empty bench take 24+600=624 seconds; one takes 612; two take 618. Later additions need a new cycle. Preserve removal as actual 10-minute tool work, no reactivation. Add a batch-sealing example.'},
      {'id':'AR1-02', 'severity':'omitted-time-and-resource-cost',
       'locations':['/arcs/1/vessel/supportStates/grounded','/arcs/1/route','CASEBOOK.json: ARC16-C01,C02,C04,C09,C32','PLAYER_CHAPTER.md: Route and baseline plan'],
       'evidence':{'takeoff':model['arcs'][1]['vessel']['supportStates']['grounded'],'ordinaryCase':next(x for x in cases['cases'] if x['id']=='ARC16-C01')},
       'finding':'The grounded rule requires a separate six-second coordinated takeoff with no extra travel. All full-voyage totals add only 5h outbound travel, site, 2h return, canopy deployment and descent; they omit takeoff.',
       'proposedCorrection':'Set full-voyage t0 to actual fuel/air activation at the start of takeoff; takeoff 0–6, then 18000 seconds outbound travel. Do not consume preflight time for free or remove the existing takeoff cost. Keep site-relative schedules, canopy deployment and descent unchanged. Correct all affected totals, prose and cases, and retain old numbers only as explicitly superseded history.',
       'correctedPlans':{
         'ordinaryPoweredIdle':{'elapsedSeconds':32106,'elapsed':'8h55m06s','powered':'482m18s','fuelRemaining':'117m42s','airRemaining':'184m54s'},
         'weatherDetour':{'elapsedSeconds':33906,'elapsed':'9h25m06s','powered':'512m18s','fuelRemaining':'87m42s','airRemaining':'154m54s'},
         'engineOffMooring':{'elapsedSeconds':32106,'elapsed':'8h55m06s','powered':'420m24s','fuelRemaining':'179m36s','airRemaining':'184m54s'},
         'transitionPoweredIdle':{'elapsedSeconds':30900,'elapsed':'8h35m00s','powered':'462m12s','fuelRemaining':'137m48s','airRemaining':'205m00s'}},
       'localArithmeticScope':'Independent ordinary arithmetic only. No runtime execution or gameplay simulation.'},
      {'id':'AR1-03', 'severity':'resource-clock-conflict',
       'locations':['/arcs/1/launchDock/withdrawal','/arcs/1/vessel/air','DIRECTOR_CHAPTER.md: Launch dock'],
       'finding':'Unqualified wording says refusal before takeoff costs no fuel/air, while an activated cartridge and running engine spend real time even if departure is later canceled.',
       'proposedCorrection':'Declining before activating equipment consumes no fuel or air. Once activated, actual clocks run even before takeoff or after cancellation. Wage entitlement still begins only on actual takeoff. The baseline assumes activation at takeoff start; earlier activation or preflight engine running adds its real cost. Add a canceled-departure example with already-active cartridge.'},
      {'id':'AR1-04', 'severity':'chapter-completeness-and-fidelity',
       'locations':['PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md','CAMPAIGN_ARCS_MODEL.json'],
       'finding':'The chapters omit operative details present in the complete returned model, so they are not yet a complete runnable presentation of that model.',
       'examples':[
         'ARC-ENVOY cold resistance is present in /profiles/2/defenses but absent from the Director profile.',
         'The claimed complete atmosphere table omits AIR-06: actual water-form cold resistance/water breathing does not supply a breathing medium; air-form flight/type does not grant no-breath. Preserve actual card access, cost, timing and source-specific limits for all AIR-01 through AIR-14.',
         'Airlock inner-door protection interlock, forced/destroyed door breach and full recovery procedure, door AC/HP, outer service control, same-instant protection rules, and partial exposure handling need usable Director text.',
         'Powered tactical movement/event budget, role training, exact support-transfer ordering, fuel refilling, air-cartridge replacement, canopy AC/HP and support/retraction limits, engine-off plan, worker Burdened Speed20, and actual weather-check alternative are absent or materially abbreviated.',
         'The Conclave investigation alternatives, actual initial tune lists/losses, custody/payment availability and real stock/property need readable Director coverage.',
         'A3: the model gives definite hostility predicates and says later SHADE powers off the spindle; the Director text says opening can trigger hostility and omits that power-off. Preserve actual movement between wall controls and cage and ordinary initiative/action budgets.',
         'CF-1 requires 60 elapsed seconds venting any positive pressure; closing V early restarts that interval. These instructions are absent in the Director procedure. The full Action sequence, drive-versus-one-charge behavior, interrupted-service states and destruction discharge also need coverage.',
         'Contract presentation omits operative termination-delivery alternatives, actual notice, available-review timing, finite receipt/dictation requirements, rejection criteria, no recycled evidence, amendment and credited prior bond recovery. Retain these in usable player terms and Director procedures.',
         'Refusal participants receive one actual instructor-led service appointment independent of signing the patent term. That access route is in /arcs/2/refusalExercise/delivery but absent from both chapters, which otherwise describe bench permission as an active-contract benefit.'
       ],
       'proposedCorrection':'Reconcile both chapters against every operative model field. Restore complete procedures in readable sections/tables; a concise handout may link to the complete player rules but must not change costs or hide material offer terms. Keep Director-only state out of player content. Preserve all current source text and IDs; report the coverage mapping instead of claiming a short summary is complete.'},
      {'id':'AR1-05', 'severity':'geometry-and-editorial-clarification',
       'locations':['/arcs/1/launchDock/geometry','/arcs/1/vessel/body','PLAYER_CHAPTER.md: Starting the annual term'],
       'finding':'The launch footprint is x0–30/y0–20, while the berth/interior frame is x0–20/y0–30; the rotation is not stated. The player start list says all three but enumerates four conditions.',
       'proposedCorrection':'Retain both legal footprints and explicitly map vessel-local berth coordinates to launch coordinates by xLaunch=yVessel, yLaunch=xVessel, with crew/stations transformed too; no duplicated airlock or staging overlap. Say all four conditions in the player start list (or combine prior understanding with signature into one numbered condition) without changing actual prerequisites.'},
      {'id':'AR1-06', 'severity':'missing-machine-state-guard',
       'locations':['/arcs/2/knowledgeReward/operation/printing','/arcs/2/knowledgeReward/operation/charge','DIRECTOR_CHAPTER.md: Printing'],
       'finding':'Printing requires a successful test and live drive, but does not explicitly invalidate ready state after venting/discharge, cap opening, lost seal, changed routing or loss of pressure. Drive cannot recharge the one pressure charge; a historical successful test must not permit later printing at gauge0.',
       'proposedCorrection':'Define explicit current ready/test state. Printing must retain the intact supported press, closed cap and vent, correct route, functioning seal, gauge1 from the same unspent pressure charge, successful current 60-second test, live drive and actual paper/ink. State which changes invalidate ready state and require safe service plus a new real activation/test; do not replenish cells or undo prior prints. Add a successful-test→vent→attempt-print example. This is a proposed local machine completion requiring actual GPT disposition, not unilateral rule adoption.'}
    ]
    assert 'For each fragment:' in player and 'Resistance cold' in model['profiles'][2]['defenses']
    assert 18000+3726+7200+6+3168 == 32100
    assert 6+18000+3726+7200+6+3168 == 32106
    assert 6+18000+2520+7200+6+3168 == 30900
    record = {'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Independent review complete for first return; corrections required before joint application.',
      'archive':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_01_Return_01.zip'),
      'sourceCheck':info(A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_01.json'),
      'actualGptVerdict':info(A/'EPILOGUE_ARCS_06_RECEIVED_VERDICT_01_DOM.txt'),
      'reviewedFiles':[info(root/n) for n in ['REGISTER.json','CAMPAIGN_ARCS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json']],
      'allReturnedExamplesRead':75,'allOriginal67IdsPreserved':True,'findings':findings,
      'confirmedInterfaces':['Seal Magic is actually tagged wizard-spell, rank5, 4RP, with a live target-bound duration; ARCX-04 does not invent spell status from a class name. Its real acquisition/cast/consent requirements remain necessary.',
       'Transition source actually supports a fixed complex-work order, active minutes, start window and nontransferable scope; the reviewed 5/15-minute local phase mapping is compatible for the stated uninterrupted preflight example.',
       'Distinct damage dealers, real Construct Disabled0, absence of new Residual Null fields, one-time serial/coin stock and unresolved campaign era remain preserved.'],
      'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}
    out.write_bytes(encoded(record))
    lines = [
      'I downloaded and independently reviewed your complete first EPI-15–17 return (100,577 bytes; SHA-256 68849df7d86209c88d66ac2d1d67df60d6ba0b3b0f24f319131fc7fd387f46ad). All 51 source bindings, seven manifest outputs and all 75 case IDs pass the local source-integrity check (86 checks, zero failures). I read the full model, both chapters, register and every case. I found six correction areas below; no arc rules have yet been applied.',
      'Please independently disposition each AR1 finding against your retained exact return and the same supplied 51 sources. Correct the full candidate, not only the verdict, preserving all 75 current case IDs/order and original source bindings. Add focused cases for batch sealing, takeoff/cancellation clocks and invalidated press readiness. Keep all source/earlier accepted modules unchanged. Return DD_Cosmology_Epilogue_Campaign_Arcs_02_Return.zip with the same eight exact root files and byte/hash manifest, and report archive byte length/SHA-256. Record before/after corrections and chapter coverage in REGISTER; new local machine completion still needs your explicit disposition.',
    ]
    for f in findings:
        lines += [f"{f['id']} — {f['finding']}", f['proposedCorrection']]
        if 'correctedPlans' in f: lines.append('Verified arithmetic: '+json.dumps(f['correctedPlans'],ensure_ascii=False))
        if 'examples' in f: lines.extend('- '+x for x in f['examples'])
    lines.append('These are bounded authored corrections, not runtime/human/balance/canon/whole-game approval. Do not reopen accepted EPI-01–14. The complete original return and my findings are preserved locally; nothing was deleted. I confirmed Wizard Seal Magic really is a rank5 wizard-spell, so ARCX-04 is not being rejected merely because it is on a class card. Please keep its actual predicates.')
    message.write_text('\n\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'review':info(out),'request':info(message),'findings':len(findings),'newRulesAdopted':False}))


if __name__=='__main__':main()
