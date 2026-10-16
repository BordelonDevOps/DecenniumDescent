"""Prepare reviewable corrections; do not adopt the candidate or alter any source archive."""
from copy import deepcopy
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib, json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def main():
    source = A/'cosmology-chronology-research-route-01-return-integrated/TIMELINE_AND_RESEARCH_ROUTE.json'
    target = A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_PROPOSAL.json'
    candidate = A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_CANDIDATE.json'
    assert not target.exists() and not candidate.exists()
    model = json.loads(source.read_bytes()); route = model['researchRoute']; changes=[]
    def replace(path, value):
        parts=path.strip('/').split('/'); parent=model
        for part in parts[:-1]: parent=parent[int(part)] if isinstance(parent,list) else parent[part]
        key=int(parts[-1]) if isinstance(parent,list) else parts[-1]
        old=deepcopy(parent.get(key)) if isinstance(parent,dict) else deepcopy(parent[key])
        changes.append({'path':path,'before':old,'after':deepcopy(value)})
        parent[key]=value
    def rr(path,value):replace('/researchRoute/'+path,value)
    def node(i,key,value):rr(f'nodes/{i}/{key}',value)
    issues=[
      'LP01: replace seconds/minutes mistakes, missing authentication time and overlapping observation/research with an exact nonoverlapping schedule.',
      'LP02: reconcile remaining duplicate RR04/RR06 and taint fields; retain the current structured-test KT3 episode rule, KT2 symptom and equivalent-knowledge rule.',
      'LP03: make MECH-PLATE-1 a front service plaque visible after grille access so safe operation does not require the later rear-plate task.',
      'LP04: specify actual LOAD, RETURN, lockout and catch timings; distinguish named instructional states from unsafe lock; no automatic observations.',
      'LP05: complete fallback Q-NAT-1 and prediction substitutions using finite CG records; no lost Wax facts fabricated.',
      'LP06: all ten findings are the unmarked Bard path; current Expertise qualification remains valid.',
      'LP07: fix text lineage, finite melting deadline, exact source-theme citations and actual physical evidence for the polishing inference.',
      'LP08: source manuscript priority is subject to explicit owner corrections, not the reverse; no calendar/epoch adoption.'
    ]
    replace('/authorityNote','Original manuscripts govern source reading, subject to explicit owner corrections where stated. Current applied souls/research rules govern operations. This route is NEW provisional authorship pending GPT confirmation/local adoption; it recovers no lost formula, resolves no identities and selects no epoch.')
    rr('status','LOCAL INTEGRATION PROPOSAL for GPT review; NOT ADOPTED. Original integrated return remains immutable history.')
    rr('handouts/regulatorPlate/provenance','MECH-PLATE-1 is the fixed FRONT service plaque behind the RR03 inspection grille, visible before LOAD or rear-plate work. It bears the three-notch maker mark and an etched abort timing table. Rear maintenance panels are separate objects.')
    rr('handouts/regulatorPlate/text','PAIR A / PAIR B / QUIET / ABORT. Captive keeper installed. For this fixture: maintained A=3/B=1 is the service hold. On controlled release, QUIET at second30; begin ABORT by second36; completed ABORT at second42 resolves before lock. Do not remove parts under load. Rear maintenance catch blocks LOAD.')
    rr('handouts/regulatorPlate/states',{
      'idle':'PAIR A/B and QUIET dark; captive keeper retracted; no load.',
      'loaded-separated':'The authored two-groove hold gives A=3/B=1, QUIET dark, third witness steady, captive keeper at1/3.',
      'converging':'Controlled-release second18 A=3/B=2; at30 A=3/B=3, QUIET bright, third witness pales, keeper2/3.',
      'abort-safe':'ABORT/RETURN completes, load vents and keeper retracts;10-minute LOAD lockout begins at completion.',
      'quiet-lock':'Without timely ABORT, second42 seats the captive keeper, disables LOAD/maintenance access for10minutes, then automatically vents/retracts to IDLE. No additional force-damage effect is authored in this version.'})
    rr('handouts/waxTeachingCopies/0/text','Teaching copy of WL-O1 unloaded heat reference and maintained-separation observation; copy seal names O1. This is one derivative text, not another observation.')
    rr('handouts/fracturedKey/description',route['handouts']['fracturedKey']['description']+' A fine later seat-polish film crosses the old fracture edge; deeper earlier wear stops short of full seating. These visible layers support only relative use history, never an absolute date or proof of a complete seat event.')
    source_doc=A/'cosmology-chronology-research-route-01/sources/The Decennium Descent and the Matrix of Oblivion.docx'
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with ZipFile(source_doc) as z:root=E.fromstring(z.read('word/document.xml'))
    paras=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in root.findall('.//w:p',ns)]
    rr('handouts/matrixPrimer/sourceThemeCitations',[{'path':'The Decennium Descent and the Matrix of Oblivion.docx','part':'word/document.xml','paragraphIndexZeroBased':i,'excerpt':paras[i],'textSha256':hashlib.sha256(paras[i].encode()).hexdigest(),'scope':'Theme support only; the local teaching primer is newly authored.'} for i in [53,79,81]])
    node(0,'finiteReceipts',route['nodes'][0]['finiteReceipts']+['CA-OFFICE-1','CA-PRIMER-1'])
    node(1,'finiteReceipts',route['nodes'][1]['finiteReceipts']+['WL-RUBRIC-1'])
    node(1,'roomRule','Reading the surviving words of one particular wax text aloud begins irreversible softening of that text. Exactly60seconds after the reading starts its wax inscription is lost. Stopping speech does not reverse the triggered melting. Already completed lawful copies preserve only what they actually recorded and keep the same underlying identity. Silent reading and applicable comprehension remain legal; unrelated speech does not trigger melting. Copper backing/strip, tooth and maker stamps are not erased by this inscription effect.')
    rr('mechanismSettings/maintainedSeparation/end','At pulse second60 BEGIN ABORT/RETURN; outside initiative its6seconds complete at66. Only at completion is IDLE restored and the10-minute LOAD lockout started. In initiative pay one actual Action under current action rules; the published countdown is a fixture procedure, not a new universal six-second action-duration rule.')
    rr('mechanismSettings/controlledRelease/preload','From IDLE after lockout, LOAD costs one Action/6seconds outside initiative. Observe12loaded seconds until A=3/B=1 is verified, then RELEASE costs one Action/6seconds. Controlled-release second0 is RELEASE completion. Do not silently preload or count both actions as one.')
    rr('mechanismSettings/controlledRelease/ignoredAbort','If ABORT has not completed by controlled-release second42, resolve any timely completed ABORT first; otherwise captive keeper seats and QUIET LOCK disables LOAD/maintenance access for10minutes. At lock expiry the fixture vents/retracts to IDLE. No force damage, Hunt, PT or protected Pact effect is added. Objects deliberately inserted remain where the actual fixture holds them until access is restored; no unique loot respawns.')
    rr('mechanismSettings/controlledRelease/abortDeadline','Outside initiative begin the6second ABORT no later than second36. It completes by42 and resolves before lock at that exact timestamp. In initiative announce the cue before the operator\'s regular turn at the corresponding30second boundary; allow the actual Action and resolve it before the42second lock boundary. Each genuinely later operation retains its own actual action legality and any KT3 episode save; no reaction or free extra Action is granted.')
    observation={'pre':'Observe continuously from10minutes before the opening through its start using the fixed marked temperature/reference gauge. Record PRE-n:92°F/0.0mm then104°F/+0.2mm.',
      'post':'Continue through minute20 (112°F/+0.4mm), close at40 (100°F/+0.1mm), and20minutes after close (94°F/0.0mm). This full70minute observation records POST-n; IDLE luminous indicators remain dark.',
      'duration':'70 actual minutes from -10 to +60 relative to opening; active observation cannot overlap another research block, rest, travel or guard.',
      'question':'Q-NAT-2','fixtures':'The alcove has a fixed engraved temperature scale and0.1mm reference gauge; these NEW observation fixtures provide the printed readings and are not free portable item-catalogue additions.'}
    node(3,'partyObservation',observation);rr('localChangeWindow/partyObservation',observation)
    rr('localChangeWindow/values/midWindow','minute20: surface112°F; unloaded reference-groove offset+0.4mm; amber/white/black rods are soft (their opening offsets are0/10/20minutes respectively); luminous PAIR/QUIET remain dark when IDLE.')
    node(3,'schedule',deepcopy(route['localChangeWindow']))
    rr('qualificationFindings/4/alternateEvidenceIds',['WL-PHYS-A','CG-M2'])
    rr('qualificationFindings/4/routeAvailability','RR02, or the surviving physical WL-PHYS-A plus authenticated CG-M2 from the finite Floor50 collection. CG-M2 supports historical material change only; it does not replace the party\'s separate Q-NAT-2 observation.')
    rr('qualificationFindings/9/finding','The two actual observations support stable maintained separation and convergence followed by timely abort. The42second lock deadline is an authenticated service-plaque/historical prediction unless an ignored-abort trial actually observed it. Successful safe trials do not retroactively observe an unsafe lock. These are bounded KT1 findings, not a complete Functional Model or KT3.')
    rr('qualificationFindings/9/evidenceIds',['OBS-SEP-1','OBS-CONV-1','MECH-PLATE-1'])
    rr('qualificationFindings/9/alternateEvidenceIds',['CG-M1','OBS-SEP-1','OBS-CONV-1','MECH-PLATE-1'])
    rr('alternateLibraries/0/holdings/1/supports',['Q-NAT-1 alternate historical material-change support with surviving WL-PHYS-A','Q-NAT-2 contextual comparison only; an actual new party PRE/POST pair remains required.'])
    rr('predictionTests/0/alternateEvidence',['OBS-SEP-1','MECH-PLATE-1','successful RR06 model; WL-O4 is supplementary and not mandatory when destroyed'])
    rr('predictionTests/1/alternateProposition',{'when':'Wax text including WL-T2/O3 was destroyed before a copy.',
      'A':'Physical copies of CG-M1 each create an independent Gate-service observation.',
      'B':'CG-M1 is one Gate-service observation; its later copies retain that one identity. CG-M4 is a separate inventory record, not an eyewitness repeat of CG-M1 or recovered lost Wax text.',
      'C':'CG-M4 recreates every lost word of the Wax tablets.',
      'correct':'B','evidence':['CG-M1','CG-M4','CA-W2','CA-W4'],'time':'10minute comparison; roll only for genuine supported uncertainty under the existing test procedure.'})
    rr('predictionTests/2/alternateEvidence',['OBS-CONV-1','MECH-PLATE-1','CA-W2','CG-M1; lost WL-O3 is not required and is not recreated'])
    node(5,'prerequisites','Same lead owns all five Advanced marks and currently has all five proficiencies throughout work; all five evidence categories authenticated. Ten findings are the complete path for a lead starting with no marks. Exact existing Expertise or other already-earned qualifying marks remain valid; this route does not require re-earning them.')
    node(5,'defaultQuestion',route['nodes'][5]['synthesisQuestion']);node(5,'fixedOutcomes',deepcopy(route['nodes'][5]['outcomes']))
    node(5,'result','Success establishes this bounded KT2 model. Initial KT3 requires all three settled post-model prediction propositions under the current demonstration procedure; no one preliminary mechanism run certifies it.')
    rr('ktProgression/knowledgeEquivalence','These gates describe this authored path. Equivalent verified dangerous knowledge obtained by another lawful path retains the corresponding KT state under the current model; paperwork, missing route attendance or refusal to roll cannot suppress actual knowledge/taint. Blind execution does not create understanding.')
    rr('ktProgression/KT2','For this route, successful RR06 establishes the bounded Functional Model. Equivalent lawful supported knowledge is governed by currentStateModel, not denied by an administrative route requirement.')
    rr('ktProgression/laterOperations','At already KT3, each separately preregistered Demonstrated Operational Understanding prediction test, including its cross-source interpretation test, is one current operational-commitment episode with at most one pre-cost DC15WIS save. Casual reading or ordinary documentary research outside a registered test is not such an episode. Each real later separate operation also follows its actual episode rule; pauses do not create rerolls.')
    rr('ktProgression/KT2Symptom','KT2/KT3 inherit KT1 pending-check/grounding. After a failed Matrix Synthesis, no providing or receiving generic research assistance until10uninterrupted minutes outside active synthesis/qualifying exposure. Findings and stage history remain. Re-indexing imposed by this route is active work and cannot overlap that mitigation interval.')
    rr('taintAndProtection/KT2',route['ktProgression']['KT2']+' '+route['ktProgression']['KT2Symptom'])
    rr('taintAndProtection/KT3','Initial KT3 requires the three settled post-model tests, not one demonstration. At already KT3, each distinct registered test (including cross-source interpretation) or other qualifying concrete operation receives at most one pre-cost DC15WIS Corruption-effect save. Current actual Dazed duration/action scope, immunity, grounding and no-same-episode reroll remain unchanged.')
    rr('predictionTests/1/execution','This test does not execute the mechanism. Nevertheless, when deliberately run as one of the registered Demonstrated Operational Understanding tests by an already-KT3 researcher, it is an episode under the current predictionTests rule and takes its single pre-cost DC15WIS save. Ordinary reading/provenance work outside that structured test does not. Initial acquisition after all three settled tests is not retroactively saved against.')
    rr('languageAndReading/knowledgeTransfer','Knowledge Transfer lends only the donor\'s actual spoken competence and only reading/writing/script modes the donor actually owns for that language, for its real1hour, Action/2RP/touch/willing/1-per-short-rest scope. It never creates literacy the donor lacks, marks, memories, secrets or missing text.')
    rr('borrowedProficiencyFourWindowExample/day1Grounding',{'time':'Day1 07:50:00–08:00:00','event':'If a KT1 pending symptom exists, ground for10actual minutes before the first loan. Day1 otherwise begins after the stated04:00 beneficial Long Rest; no time is counted as synthesis.'})

    # Exact example intervals use seconds, so overlapping work or missing time is checkable.
    schedule=[]
    def sec(t):
        a=[int(v) for v in t.split(':')];return a[0]*3600+a[1]*60+(a[2] if len(a)>2 else 0)
    def add(phase,day,start,end,activity,kind='work'):
        a=sec(start);b=sec(end);assert b>a
        schedule.append({'phase':phase,'day':day,'start':start,'end':end,'seconds':b-a,'activity':activity,'kind':kind})
    add('F47',1,'04:00','04:30','RR01 intake: access/provenance register for all8receipts. No automatic historical/technical conclusion.')
    add('F47',1,'04:30','06:45','135minutes: CA-W1/2/3 physical comparisons20m each; CA-W4 lineage20m; CA-W5 record10m; office20m; primer20m; index5m. Worked successful authentication where a real check is required; known Common/Old Choir cant reading premise.')
    for s,e,q in [('06:45','10:45','Q-HIS-1'),('10:45','14:45','Q-REL-1'),('14:45','18:45','Q-ARC-1')]:add('F47',1,s,e,q+' —240active minutes; worked Success.')
    add('F47',1,'18:45','20:00','Meals/logistics; no research credit.','other')
    add('F47',1,'20:00','28:00','Legal8hour Rest; previous beneficial Rest ended day1 04:00.','rest')
    add('F47',2,'04:00','04:10','KT1 grounding after Rest.','grounding')
    add('R68',1,'04:00','04:10','KT1 grounding after the separately completed arrival Rest.','grounding')
    add('R68',1,'04:10','04:40','RR02 door bypass30minutes, worked Success.')
    add('R68',1,'04:40','07:50','190minutes of distinct Wax access/authentication:4originals25m each,3copies10m each,5damaged fragments5m each, tooth10m, rubric25m; known-language premise. No shared-time discount.')
    for s,e,q in [('07:50','11:50','Q-HIS-2'),('11:50','15:50','Q-REL-2'),('15:50','19:50','Q-NAT-1')]:add('R68',1,s,e,q+' —240active minutes; worked Success.')
    add('R68',1,'19:50','20:00','Return to already secured adjacent camp; no new Haven granted.','other')
    add('R68',1,'20:00','28:00','Legal8hour Rest at previously secured camp.','rest')
    add('R68',2,'04:00','04:10','Grounding.','grounding')
    add('R68',2,'04:10','04:22','Actually traverse12minute passage to RR03.','travel')
    add('R68',2,'04:22','04:32','Authenticated calibration tooth opens grille in10minutes.')
    add('R68',2,'04:32','04:42','Record front plaque, direct state and fixed environmental gauges in10minutes.')
    add('R68',2,'04:42:00','04:42:06','LOAD Action/6seconds outside initiative.')
    add('R68',2,'04:42:06','04:43:06','OBS-SEP-1:60second maintained pulse.')
    add('R68',2,'04:43:06','04:43:12','ABORT/RETURN Action; IDLE/lockout starts on completion.')
    add('R68',2,'04:43:12','04:53:12','10minute LOAD lockout.','wait')
    add('R68',2,'04:53:12','04:53:18','LOAD for second trial.')
    add('R68',2,'04:53:18','04:53:30','Verify12loaded seconds of A3/B1 hold.')
    add('R68',2,'04:53:30','04:53:36','RELEASE Action; release second0 at completion.')
    add('R68',2,'04:53:36','04:54:12','OBS-CONV-1: cue at04:54:06 (second30); begin abort at04:54:12 (second36).')
    add('R68',2,'04:54:12','04:54:18','ABORT completes at release second42 before lock.')
    add('R68',2,'04:54:18','05:04:18','10minute lockout.','wait')
    add('R68',2,'05:04:18','05:04:24','Maintenance catch Action/6seconds; blocks LOAD.')
    add('R68',2,'05:04:24','05:24:24','RR05-PLATE20minute task, worked Success.')
    add('R68',2,'05:24:24','05:34:24','Authenticate actual fractured spare and installed keeper distinction10minutes.')
    add('R68',2,'05:34:24','05:34:30','Release catch/reseat plate Action/6seconds.')
    add('R68',2,'05:34:30','07:50','Wait/logistics, no research credit.','wait')
    add('R68',2,'07:50','09:00','RR04 first full70minute PRE1/POST1 observation; opening08:00, cooling08:40, last post09:00.','observation')
    add('R68',2,'09:00','13:00','Q-ARC-2 —240active minutes; worked Success.')
    add('R68',2,'13:00','17:00','Q-ENG-1 —240active minutes; worked Success.')
    add('R68',2,'17:00','20:00','Return12minutes to secured camp plus meals/logistics.','other')
    add('R68',2,'20:00','28:00','Legal8hour Rest;20:00 window deliberately missed.','rest')
    add('R68',3,'04:00','04:10','Grounding.','grounding')
    add('R68',3,'04:10','08:10','Q-NAT-2 on actual PRE1/POST1 —240active minutes; worked Failure.08:00window is missed while researching.')
    add('R68',3,'08:10','12:10','Q-ENG-2 —240active minutes using already authenticated spare and recorded captive geometry; worked Success.')
    add('R68',3,'12:10','20:00','Logistics/wait; no rewording retry or free new observation.','other')
    add('R68',3,'20:00','28:00','Legal8hour Rest.','rest')
    add('R68',4,'04:00','04:10','Grounding.','grounding')
    add('R68',4,'04:10','04:22','Return12minute passage to RR03.','travel')
    add('R68',4,'04:22','07:50','Wait for actual next usable window.','wait')
    add('R68',4,'07:50','09:00','New actual70minute PRE2/POST2 pair. Same12hour cycle; several intervening windows were missed.','observation')
    add('R68',4,'09:00','13:00','Q-NAT-2 retry240active minutes; new evidence identity permits retry; worked Success. All10findings now complete.')
    add('R68',4,'13:00','17:00','RR06 synthesis240active minutes; worked Success establishes KT2.')
    add('R68',4,'17:00','17:01','TEST-MECH-1: correct explained proposition from actual settled evidence, no extra roll.')
    add('R68',4,'17:01','17:11','TEST-XREF-1:10minute actual lineage comparison, correct explanation, no extra roll.')
    add('R68',4,'17:11','17:12','TEST-SAFE-1: correct deadline proposition; all3settled establishes initialKT3 after17:12, no retroactive save.')
    add('R68',4,'17:12','20:00','Return/logistics; no extra work credit.','other')
    add('R68',4,'20:00','28:00','Next legal8hour Rest.','rest')
    grouped={}
    for x in schedule:grouped.setdefault((x['phase'],x['day']),[]).append(x)
    for key,rows in grouped.items():
        assert all(sec(a['end'])<=sec(b['start']) for a,b in zip(rows,rows[1:])),key
        assert sum(x['seconds'] for x in rows if x['kind'] in ['work','observation'])<=16*3600,key
        assert all(sec(x['end'])<=20*3600 for x in rows if x['kind'] in ['work','observation']),key
    rr('qualificationSchedule',{'status':'NEW worked example, locally calculated; subject to GPT review.',
      'character':'One Bard, personally proficient in all5disciplines, starts with noAdvancedmarks, has actual legal Common and Old Choir cant reading competence and ordinary suitable tools. This is a complete acquisition path, not a mandate to repeat findings when Expertise/already-earned marks qualify.',
      'clockPremises':'For this example declare daily productive Watches04:00–12:00 and12:00–20:00, Rest20:00–04:00 prospectively. F47phase begins Opening hour264; R68phase begins Opening hour480 after actual successful ordinary descent and a beneficial Rest ending04:00. That inter-phase travel/gate/camp log is a prerequisite from ordinary campaign play, not authored/approved here.',
      'safetyPremise':'The campaign has already secured a legal adjacent camp and the research alcove for this sample. No new Haven, protection, gate traversal or safe rest is created by this example. If interrupted, log the actual added time and use current rules.',
      'readiness':'All prerequisite authentication checks succeed in this worked path. Language projects, contested authentication, additional failures or unsafe camping require their real extra time. No lost text or failed check is silently passed.',
      'intervals':schedule,'completion':'R68Day4 17:12, Opening hour565.2; before1200hourHorn and2400hourclosure in this explicitly bounded sample.40hours of successful finding work plus4hours failed Nature attempt,4hours synthesis and all separate access/observation/travel/rest are recorded.',
      'failedRetry':'PRE1/POST1 observed RDay2; Q-NAT-2 fails RDay3. Actual new RDay4 PRE2/POST2 permits fresh240minute attempt; intervening missed windows do not create receipts.',
      'validation':{'overlappingIntervals':0,'workOrObservationOver16Hours':0,'successfulFindingHours':40,'failedFindingHours':4,'synthesisHours':4,'observedWindowMinutes':140,'computedOpeningHourAtCompletion':480+3*24+13.2},
      'limits':'Schedule/arithmetic validation only; not simulation of fullT6–7, actual gameplay, balance or rest-security evidence.'})
    proposal={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Proposed exact local patch; not adopted and not yet GPT-confirmed.',
      'source':info(source),'sourceArchive':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Integrated_Addendum_and_Evidence.zip'),
      'sourceCheck':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_RETURN_SOURCE_CHECK_integrated.json'),
      'issues':issues,'changes':changes,'currentCandidate':candidate.relative_to(G).as_posix(),
      'casebookRule':'All original return files and original identifiers remain preserved. Earlier route examples are NONOPERATIVE historical proposals where superseded. Author current examples from this exact schedule/fixture; do not silently present old contradictory examples as current.',
      'newRulesAdopted':False,'sourceInformationDeleted':0,'campaignEpochChosen':False}
    candidate.write_bytes(encoded(model));target.write_bytes(encoded(proposal))
    print(json.dumps({'proposal':info(target),'candidate':info(candidate),'changes':len(changes),'scheduleIntervals':len(schedule),'overlaps':0,'dailyWorkCeilingFailures':0}))

if __name__=='__main__':main()
