"""FT84 isolated work specifications. Standard library only; no game/source imports.
These supplied actor/access/stock premises are conditional fixtures, not authenticated
campaign acquisitions or an executable world scheduler. Output is read-only unless
an explicit fresh output directory is requested.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from math import ceil
from pathlib import Path
import argparse,json


def wire(x):
    if isinstance(x,F): return int(x) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
    if isinstance(x,dict):return {k:wire(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [wire(v) for v in x]
    return x

def material_bill(rows,discount):
    """Quantities before aggregate purchase rounding; unknown means no discount."""
    out=[];cost=F(0)
    for r in rows:
        q=F(r['quantity']);factor=F(3,4) if discount and r['category']=='mundane' else F(1)
        need=q*factor
        if r.get('indivisible',False):need=F(ceil(need))
        price=need*F(r['unitCp']);cost+=price
        out.append({**deepcopy(r),'required':need,'lineExactCp':price,'reductionFactor':factor})
    return {'lines':out,'exactTotalCp':cost,'finalPurchaseCp':ceil(cost)}


def phase_trace(required_seconds,segments,initial_credit=0,quantum=900):
    """Local work ledger; no global clock or roll/XP engine. Complete phases only."""
    required=ceil(F(required_seconds));credit=initial_credit;pending=0;lost=0;active=0;tr=[];last_end=0
    if not 0<=credit<=required:raise ValueError('Invalid credited work')
    for seg in segments:
        start=seg['start'];seconds=seg['seconds']
        if start<last_end or seconds<0:raise ValueError('Overlapping or invalid actual work')
        before={'creditSeconds':credit,'pendingSeconds':pending,'lostSeconds':lost,'activeSeconds':active,'time':last_end}
        remain=seconds;active+=seconds
        while remain and credit<required:
            phase=min(quantum,required-credit)
            take=min(remain,phase-pending);pending+=take;remain-=take
            if pending==phase:credit+=phase;pending=0
        if remain:raise ValueError('No unclaimed surplus task work in this fixture')
        if seg.get('interrupt',False):lost+=pending;pending=0
        last_end=start+seconds
        after={'creditSeconds':credit,'pendingSeconds':pending,'lostSeconds':lost,'activeSeconds':active,'time':last_end}
        tr.append({'event':deepcopy(seg),'before':before,'after':after})
    return {'requiredSeconds':required,'creditedSeconds':credit,'pendingSeconds':pending,'lostSeconds':lost,'actualActiveSeconds':active,'elapsedSeconds':last_end,'complete':credit==required,'completionOpportunities':int(credit==required),'trace':tr}


def gadget(before,request):
    s=deepcopy(before);timeline=[]
    needed=300 if request['craftsmanPersonalLead'] else 600
    eligible=all(request[k] for k in ['sourceGranted','gnome','tools','partsOwned','lawfulWork']) and request['start']>=s['nextUseAt'] and s['partsLots']>=1 and request['eventId'] not in s['receipts']
    if not eligible:return {'status':'REJECT_BEFORE_COMMIT','before':before,'after':s,'timeline':[],'rollCount':0,'requiredSeconds':needed}
    old=deepcopy(s);s['partsLots']-=1;s['useSpent']+=1;s['nextUseAt']=request['start']+86400;s['receipts'].append(request['eventId']);s['activeGadget']=None
    timeline.append({'time':request['start'],'event':'commit actual stock and24h use; end prior same-owner gadget if any','before':old,'after':deepcopy(s)})
    sec=request.get('interruptAfter',needed);s['actualWorkSeconds']+=sec
    if sec<needed:
        timeline.append({'time':request['start']+sec,'event':'actual interruption; entire committed attempt lost','after':deepcopy(s)})
        return {'status':'INTERRUPTED_NO_GADGET','before':before,'after':s,'timeline':timeline,'rollCount':0,'requiredSeconds':needed}
    if sec!=needed:raise ValueError('This finite fixture does not fabricate excess work')
    if request['d4']!=3:raise ValueError('Only the source-worked clamp outcome is exercised here')
    done=request['start']+needed
    s['activeGadget']={'id':request['eventId']+'-body','profile':'clamp (source worked-case d4=3; activation not tested)','weightLb':1,'AC':10,'HP':1,'createdAt':done,'expiresAt':done+3600,'holder':s['owner'],'activationExecuted':False}
    timeline.append({'time':done,'event':'complete once; real d4=3; no activation','after':deepcopy(s)})
    return {'status':'CREATED','before':before,'after':s,'timeline':timeline,'rollCount':1,'requiredSeconds':needed}


def kit(before,craftsman,attempts,die):
    s=deepcopy(before);need=900 if craftsman else 1800;active=0;trace=[];now=0
    s.setdefault('usableWorkSeconds',0)
    for a in attempts:
        start=a.get('start',now);sec=a['seconds']
        if start<now or sec<0 or s['usableWorkSeconds']+sec>need:raise ValueError('Invalid actual work segment')
        old=deepcopy(s);active+=sec;s['actualWorkSeconds']+=sec;s['usableWorkSeconds']+=sec;now=start+sec
        if a.get('interrupt'):
            if s['usableWorkSeconds']>=need:raise ValueError('Not a pause during unfinished work')
            trace.append({'start':start,'end':now,'event':'pause; actual usable partial assembly and stock persist without protection or a functioning kit','before':old,'after':deepcopy(s)});continue
        if s['usableWorkSeconds']!=need:raise ValueError('Whole adjusted active work is required before completion roll')
        total=die+3+3;success=total>=12
        if success:
            s['cordLb']=0;s['frameLb']=0;s['kits'].append({'id':'kit-1','type':'snare','weightLb':2,'armed':False,'setter':None})
        else:s['cordLb']=0 # actual expended cord; real frame retained
        s['attemptClosed']=True
        trace.append({'start':start,'end':now,'event':'complete binary task check; history retained, not reusable new-job credit','die':die,'INT':3,'PB':3,'total':total,'DC':12,'success':success,'before':old,'after':deepcopy(s)})
        return {'status':'KIT_CREATED' if success else 'FAILED','requiredSeconds':need,'before':before,'after':s,'timeline':trace,'completionRolls':1,'actualWorkSeconds':active,'elapsedSeconds':now}
    return {'status':'INCOMPLETE','requiredSeconds':need,'before':before,'after':s,'timeline':trace,'completionRolls':0,'actualWorkSeconds':active,'elapsedSeconds':now}


def run():
    cases=[];checks=[]
    def check(name,actual,expected):
        actual=wire(actual);expected=wire(expected);ok=actual==expected;checks.append({'assertion':name,'pass':ok,'actual':actual,'expected':expected})
        if not ok:raise AssertionError(checks[-1])
    def add(cid,title,question,premises,initial,events,final,expectations,scope='SOURCE_QUALIFIED_ISOLATED_SPECIFICATION'):
        case={'id':cid,'title':title,'question':question,'scope':scope,'premises':premises,'initialState':initial,'events':events,'finalState':final,'expectedAssertions':expectations,'runtimeExecuted':False}
        cases.append(wire(case))
        for k,actual,expected in expectations:check(cid+' '+k,actual,expected)
        return case
    scholar={'id':'TEST-scholar','scope':'paid-acquisition/ability slice, not full authenticated character','class':'Wizard','level':12,'INT':16,'PB':4,'Arcana':7,'History':7,'paidMilestones':{'4':'Ritual Caster: INT chosen','8':'Spell Scribe','12':'Diligent Researcher'},'noASIIncreasesAtThoseMilestones':True,'actualBook':'book-S','tools':'usable writing kit','RP':0,'spellcastingExecuted':False}
    supplies=[{'id':'paper-A','category':'mundane','quantity':4,'unitCp':25,'indivisible':True}, {'id':'ink-A','category':'mundane','quantity':5,'unitCp':100,'indivisible':False},{'id':'rare-ink-R','category':'rare','quantity':4,'unitCp':100,'indivisible':False}]
    for mode,discount,time,expectedCost in [('written',True,14400,850),('teacher',False,28800,1000),('written-tutor-present',True,14400,850)]:
        bill=material_bill(supplies,discount);ph=phase_trace(time,[{'start':0,'seconds':time}]);fee=960 if mode=='teacher' else 0
        ini={'actor':scholar,'walletCp':4000,'bookEntries':[],'materialLots':supplies,'source':{'exactRitual':'Detect Magic, rank1 Wizard placement named by Ritual Caster overlay','completeLegitimateText':mode!='teacher','actualQualifiedTeacher':mode in ['teacher','written-tutor-present'],'languageNotationUsable':True,'bookAlreadyOwned':True,'billNominalCp':1000},'creditSeconds':0}
        fin={'walletCp':4000-bill['finalPurchaseCp']-fee,'materialsConsumed':bill,'materialsRemaining':[{'id':r['id'],'quantity':F(r['quantity'])-r['required']} for r in bill['lines']],'teacherFeeCp':fee,'bookEntries':['Detect Magic ritual-record only'],'normalWizardBookAcquisition':False,'credits':ph,'RP':0,'noCastOrXP':True}
        add('FT84-01-'+mode,'Rank-one learning uses its real route','FT84-Q01',{'learningRollRequired':False,'safeRelevantWorksite':True,'oneWorkWatch':'0..28800 seconds','sourceContentIsFixture':True,'itemizedBillIsFixtureNotUniversalSplit':True,'teacherContract':'teacher-only:2cp/active minute; written tutor voluntarily advisory, no compulsory paid instruction'},ini,ph['trace'],fin,[('time',ph['actualActiveSeconds'],time),('cost',bill['finalPurchaseCp'],expectedCost),('rare units',bill['lines'][2]['required'],4),('no ordinary Wizard acquisition',fin['normalWizardBookAcquisition'],False)])
    bill=material_bill([{'id':'genuine-unclassified-route-bundle','category':'unknown','quantity':1,'unitCp':1000,'indivisible':True}],True)
    add('FT84-01-ambiguous-full-price','Unclassified material price does not block valid half-time work','FT84-Q01',{'completeWrittenSource':True,'actualCompleteRequiredBundleSupplied':True,'classificationUnknown':True}, {'walletCp':2000,'bookEntries':[]}, [{'event':'supply real full bundle and do240 active minutes','activeSeconds':14400,'consumedBundle':1}],{'walletCp':1000,'bookEntries':['Detect Magic ritual-record'],'activeSeconds':14400,'materialDiscount':0},[('full bill',bill['finalPurchaseCp'],1000),('written time unaffected',14400,14400)])
    for problem in ['missing-source','no-readable-language','no-real-book','missing-rare-stock','unpaid-Spell-Scribe','unqualified-teacher']:
        effect='no-copy-discount; use otherwise-legal baseline' if problem=='unpaid-Spell-Scribe' else 'no-learning-progress'
        add('FT84-01-'+problem,'No new prerequisite or stock from a discount','FT84-Q01',{'isolatedAbsentPredicate':problem,'allOtherActualRequirements':'supplied only for this negative input'}, {'walletCp':2000,'creditSeconds':0,'bookEntries':[]},[{'event':'pre-work validation','result':effect}],{'walletCp':2000,'creditSeconds':0,'bookEntries':[],'adjudication':effect}, [('no spent validation',2000,2000),('no phantom entry',[],[])],scope='NEGATIVE_PREDICATE_NOT_WHOLE_LEARNING_IMPLEMENTATION')
    ph=phase_trace(14400,[{'start':0,'seconds':1500,'interrupt':True},{'start':1800,'seconds':13500}])
    add('FT84-01-interruption','Written study retains completed15-minute credit and real used stock','FT84-Q01',{'actor':scholar,'completeTextAndSafeResumption':True,'stockUse':'fixture:0.25 ordinary ink unit is irrecoverably used in lost work, additional to successful-copy3.75units; adequate5unit lot genuinely supplied','noAutomaticGlobalConsumptionRule':True}, {'inkUnits':5,'creditSeconds':0,'bookEntries':[]},ph['trace'],{'credit':ph,'inkConsumed':4,'inkRemaining':1,'bookEntries':['Detect Magic ritual-record']},[('credit',ph['creditedSeconds'],14400),('actual',ph['actualActiveSeconds'],15000),('elapsed including gap',ph['elapsedSeconds'],15300),('lost',ph['lostSeconds'],600),('no returned ink',1,1)])
    rounding=material_bill([{'id':'tinyA','category':'mundane','quantity':2,'unitCp':1,'indivisible':False},{'id':'tinyB','category':'mundane','quantity':2,'unitCp':1,'indivisible':False},{'id':'protected','category':'unique','quantity':1,'unitCp':1,'indivisible':True}],True)
    add('FT84-01-rounding','Final purchase and time ceilings, not per-line or per-phase','FT84-Q01',{'actualAuthorizedCopy':'arithmetic fixture only;not a newly granted ritual','sameCategoryReductions':'one strongest factor'}, {'baseMinutes':121,'materialLines':'2+2 mundane cp and1protected cp'},[],{'minutes':ceil(F(121,2)),'bill':rounding,'oneIndivisibleSheetRequired':ceil(F(3,4))},[('time ceil',ceil(F(121,2)),61),('aggregate cost',rounding['finalPurchaseCp'],4),('single sheet',ceil(F(3,4)),1)],scope='PURE_ROUNDING_BOUNDARY_WITHOUT_NEW_COPY_PERMISSION')
    add('FT84-01-wizard-route','Wizard Spell Scribing remains its own found-spell procedure','FT84-Q01',{'actualSelectedClassCard':'wizard.base.spell-scribing','rank2FoundWizardSpellActuallyLegal':True,'copyNotRitualLearning':True,'SpellScribeAlsoOwned':True}, {'baselineMinutes':240,'baselineCp':10000},[],{'activeMinutes':120,'costCp':5000,'RitualBookEntryGranted':False},[('strongest time',120,120),('strongest cost',5000,5000)],scope='EXISTING_SOURCE_WORKED_COMPARISON_NOT_CLASS_ACQUISITION_EXECUTION')
    add('FT84-01-method-switch','A later complete text changes only the unworked phase-aligned remainder','FT84-Q01',{'completedTeacherPhases':8,'completeLegitimateTextArrivesAtBoundary':True,'noNewFeatGrant':True,'billNoRetroactiveDiscountOnConsumedStock':True}, {'baselineMinutes':480,'actualTeacherMinutes':120,'creditedBaselineMinutes':120},[{'timeMinute':120,'event':'prospective route switch;360unworked baseline minutes become180written work'}],{'actualWorkMinutes':300,'completedRitualRecords':1,'retroactiveRefundCp':0},[('actual total',120+360/2,300),('no quartering',360/2,180)])
    # Two new locally phased research routes.
    for which in ['translate','formula']:
        ph=phase_trace(14400,[{'start':0,'seconds':1500,'interrupt':True},{'start':1800,'seconds':13500}])
        isT=which=='translate';dice=7 if isT else 5;pb=4 if isT else 3;dc=15 if isT else 8;assist=1 if isT else 0;total=dice+3+pb+assist
        ini={'actor':'TEST-research-lead','class':'Wizard','level':12 if isT else 8,'INT':16,'PB':pb,'actualResearcherFeat':{'paidMilestone':'Wizard:4','INTPrerequisite':True},'creditSeconds':0,'walletCp':2000,'workingStock':{'ordinaryNotesSheets':4,'reagentLotsConsumed':0},'source':{'route':'LA07 ordinary related-dialect Translate/Decipher' if isT else 'existing available recipe-121 formula research','baselineMinutes':480,'actualMinimumResearchHours':None if isT else 0,'actualSkillCredential':'History proficiency' if isT else 'actual Enchanting4 and relevant trade proficiency, no second PB contribution','passage':'TEST_ONLY supported target: The eastern gate closes at dusk.' if isT else None,'evidence':'real adequate parallel/grammatical evidence and author-held supported meaning' if isT else 'actually accessible damaged partial formula plus sufficient genuine sample/evidence;not already-legible simple-copy route','libraryOrFacility':True,'assistant':'one actual qualified participant for all250active minutes' if isT else None,'manufactureStockNotSpent':{'crystals':2,'rib':1,'hosts':6} if not isT else None}}
        bill=500 if isT else 200 # fixture actual access/assistance agreement, not a rule price
        fin={'progress':ph,'walletCp':2000-bill,'actualAgreedFeeCp':bill,'notesSheetsUsed':1,'notesSheetsRemaining':3,'completionCheck':{'die':dice,'INT':3,'PB':pb,'assistant':assist,'total':total,'DC':dc,'success':True},'result':'one supported preregistered passage' if isT else 'usable exact recipe-121 transcription only','XP':0,'RP':0,'manufactureInputsConsumed':0,'newLanguageOrItem':False}
        add('FT84-02-'+which,'Named research preserves completed phase credit and exact single result','FT84-Q02',{'worksiteEvidenceAndPaidAcquisition':'explicit source-qualified fixture premises,not world authentication','normalPhases':900,'maxActiveWorkWatches':2,'feeContract':'Translate:2cp per actual attended work minute;formula:flat200cp agreed facility access;not source-universal fees','noManufacturingIncorporation':True},ini,ph['trace']+[{'time':15300,'event':'one ordinary completion task roll','result':fin['completionCheck']}],fin,[('required',ph['requiredSeconds'],14400),('actual',ph['actualActiveSeconds'],15000),('lost',ph['lostSeconds'],600),('success',total>=dc,True),('check once',ph['completionOpportunities'],1),('XP',fin['XP'],0)])
    for assisted in [True,False]:
        total=7+3+4+int(assisted)
        add('FT84-02-assistant-'+str(assisted),'Assistant contribution requires all adjusted successful work','FT84-Q02',{'sameTranslateCase':'independent reset','actualEligibleAssistantAllWork':assisted,'noSecondProficiency':True}, {'creditedSeconds':14400},[{'event':'one completion roll','die':7,'INT':3,'PB':4,'assistant':int(assisted),'DC':15}], {'total':total,'success':total>=15,'result':'supported passage' if total>=15 else 'notes only','retryWithoutNewEvidenceOrMethod':False},[('sum',total,15 if assisted else 14),('success',total>=15,assisted)])
    ph=phase_trace(14430,[{'start':0,'seconds':14400},{'start':14400,'seconds':30}])
    add('FT84-02-final-fraction','A source-qualified final30seconds is a real shorter final phase','FT84-Q02',{'ordinaryFormulaProjectMinimumMinutes':481,'independentlyAuthorizedSourceMinimum':'arithmetic fixture,not a new recipe','eligibleFactor':'1/2'}, {'creditSeconds':0},ph['trace'],ph,[('required',ph['requiredSeconds'],14430),('complete',ph['complete'],True),('no padding',ph['actualActiveSeconds'],14430)],scope='FINITE_PHASE_BOUNDARY_WITH_SOURCE_MINIMUM_PREMISE')
    ph=phase_trace(14400,[{'start':0,'seconds':300}],initial_credit=14100)
    add('FT84-02-real-progress-loss','A genuine prior loss leaves a5-minute final remainder','FT84-Q02',{'priorSourceQualifiedLoss':'external source must genuinely supply this;not granted here','originalCompletedCreditSeconds':14400,'actualLossSeconds':300}, {'creditedSeconds':14100},ph['trace'],ph,[('remainder',ph['actualActiveSeconds'],300),('complete',ph['complete'],True)],scope='CONDITIONAL_PROGRESS_LOSS_BOUNDARY_NOT_NEW_LOSS_SOURCE')
    for activity,minutes in [('ordinary-language-course',19200),('RitualCaster-teacher-learning',480),('ordinary-formula-copy',60),('Scribing-Insight-specific-spend',480),('fixed-curing-wait',1440),('unrelated-research-clock',None)]:
        add('FT84-02-exclude-'+activity,'Named research completion does not leak into another procedure','FT84-Q02',{'actualActivity':activity,'DiligentResearcherOwned':True}, {'requiredMinutes':minutes},[],{'requiredMinutes':minutes,'newPhaseClockApplied':False,'newEvidenceGranted':False},[('unchanged time',minutes,minutes),('no new clock',False,False)],scope='SCOPED_CLASSIFICATION_BOUNDARY')
    for reason in ['unsupported-meaning','missing-archive-access','unchanged-evidence-retry','third-active-work-Watch','same-minute-training-and-research']:
        add('FT84-02-invalid-'+reason,'An actual project gate remains required','FT84-Q02',{'absentPermission':reason}, {'creditSeconds':0,'stock':4},[{'event':'attempted work/check admission','admitted':False}],{'creditSeconds':0,'stock':4,'extraRoll':False,'extraWorkWatch':False},[('no invented credit',0,0),('no extra roll',False,False)],scope='PREDICATE_DIAGNOSTIC_NOT_FULL_PROJECT_REJECTION_ENGINE')
    gb={'owner':'TEST-Gnome-maker','partsLots':2,'lotPriceCp':500,'useSpent':0,'nextUseAt':0,'receipts':[],'actualWorkSeconds':0,'activeGadget':None,'currencyCp':0,'RP':0,'otherItemCharges':2}
    rq={'sourceGranted':True,'gnome':True,'tools':True,'partsOwned':True,'lawfulWork':True,'craftsmanPersonalLead':True,'start':0,'eventId':'build-1','d4':3}
    craftPrem={'actualGnomeAndTools':'explicit conditional world premise','paidFeatHistory':{'Wizard:4':'Craftsman, chooses actual carpenters tools','Wizard:8':'Contraption Crafter'},'INT':16,'noToolProficiencyFromContraption':True,'partsLots':'two actual5gp lots,not currency converted to stock','noClampActivationClaim':True}
    for cm in [False,True]:
        rr={**rq,'craftsmanPersonalLead':cm};res=gadget(gb,rr);s=res['after']
        add('FT84-03-gadget-'+str(cm),'Complete real gadget construction','FT84-Q03',{**craftPrem,'operativeCraftsmanForThisComparator':cm,'baselineComparator':'same source procedure before actually acquiring Craftsman; class4 choice is not operative in this independent comparator' if not cm else 'personally led creation with paid feat'},gb,res['timeline'],s,[('duration',res['requiredSeconds'],300 if cm else 600),('parts',s['partsLots'],1),('use',s['useSpent'],1),('RNG once',res['rollCount'],1),('expiry',s['activeGadget']['expiresAt'],3900 if cm else 4200),('24h not reduced',s['nextUseAt'],86400)])
    res=gadget(gb,{**rq,'interruptAfter':240});s=res['after']
    add('FT84-03-gadget-interrupt','Four minutes cannot be banked into a later gadget','FT84-Q03',craftPrem,gb,res['timeline'],s,[('no gadget',s['activeGadget'],None),('parts spent',s['partsLots'],1),('use spent',s['useSpent'],1),('no d4',res['rollCount'],0),('only actual work',s['actualWorkSeconds'],240)])
    retry=gadget(s,{**rq,'start':300,'eventId':'build-2'})
    add('FT84-03-gadget-immediate-retry','Remaining parts do not reset the spent24h use','FT84-Q03',craftPrem,s,retry['timeline'],retry['after'],[('rejected',retry['status'],'REJECT_BEFORE_COMMIT'),('no duplicate parts charge',retry['after'],s)])
    later=gadget(s,{**rq,'start':86400,'eventId':'build-2'})
    add('FT84-03-gadget-later-use','A real next24h use needs a fresh full5-minute job and parts','FT84-Q03',craftPrem,s,later['timeline'],later['after'],[('parts exhausted',later['after']['partsLots'],0),('work totals',later['after']['actualWorkSeconds'],540),('new expiry',later['after']['activeGadget']['expiresAt'],90300),('second deadline',later['after']['nextUseAt'],172800)])
    live=gadget(gb,rq)['after'];replayed=gadget(live,rq)
    add('FT84-03-gadget-replay','A repeated build receipt does not roll or grant another body','FT84-Q03',craftPrem,live,[],replayed['after'],[('same state',replayed['after'],live),('no roll',replayed['rollCount'],0)])
    gift=deepcopy(live);gift['activeGadget']['holder']='actual-recipient'
    add('FT84-03-gadget-custody','Actual transfer preserves identity, expiry and construction use','FT84-Q03',{'lawfulHandsAndObjectTransfer':'fixture premise;no free Action granted','time':600},live,[{'event':'actual completed handoff','time':600}],gift,[('same ID',gift['activeGadget']['id'],live['activeGadget']['id']),('same expiry',gift['activeGadget']['expiresAt'],3900),('same use',gift['nextUseAt'],86400)])
    for flag in ['sourceGranted','gnome','tools','partsOwned','lawfulWork']:
        rr={**rq,flag:False};res=gadget(gb,rr)
        add('FT84-03-gadget-missing-'+flag,'No permission or stock generated by Craftsman','FT84-Q03',{'missingActualPredicate':flag},gb,res['timeline'],res['after'],[('status',res['status'],'REJECT_BEFORE_COMMIT'),('same before state',res['after'],gb)],scope='PREDICATE_DIAGNOSTIC_NOT_ACQUISITION_ENGINE')
    kb={'owner':'TEST-kit-maker','cordLb':F(3,2),'frameLb':F(1,2),'fixtureKitNominalPriceCp':500,'kits':[],'actualWorkSeconds':0,'quickPlacementUses':{'snare':1,'caltrop':1,'charge':1},'armedSlots':{'snare':None,'caltrop':None,'charge':None},'hardDenialHistory':['preserved-prior']}
    kp={'INT':16,'PB':3,'actualEngineeringProficiency':'admitted use-time prerequisite;its independent grant is TEST_ONLY,not fabricated here','paidFeatOpportunitySlices':{'Wizard:4':'Craftsman','Wizard:8':'Trapsetter'},'sourceClassSchedule':'actual supplied Wizard ASI schedule;Wizard8 INT16/PB3 slice,not full campaign acquisition validation','realMaterials':'measured actual fixture0.5lb frame plus1.5lb cord=2lb source snare kit;no universal bill of materials inferred','actualToolsAndWorksite':True}
    for name,attempts,die,expect in [('success',[{'seconds':900}],8,'KIT_CREATED'),('failure',[{'seconds':900}],5,'FAILED'),('interruption',[{'start':0,'seconds':420,'interrupt':True},{'start':480,'seconds':480}],8,'KIT_CREATED')]:
        res=kit(kb,True,attempts,die)
        add('FT84-03-kit-'+name,'Half-time prepared snare retains actual stock and check','FT84-Q03',kp,kb,res['timeline'],res['after'],[('status',res['status'],expect),('work',res['actualWorkSeconds'],900),('elapsed',res['elapsedSeconds'],960 if name=='interruption' else 900),('one check',res['completionRolls'],1),('no quick use',res['after']['quickPlacementUses'],kb['quickPlacementUses']),('hard history',res['after']['hardDenialHistory'],kb['hardDenialHistory']),('frame',res['after']['frameLb'],F(1,2) if name=='failure' else 0)])
    for activity,base,factors,expected in [('barricade',60,[F(1,2),F(1,2)],30),('explicit-temper',480,[],480),('explicit-killzone',10,[],10),('collect-caltrops',1,[],1),('authorized-full-repair',120,[],120),('recipe121',240,[F(3,4),F(1,2)],120)]:
        actual=F(base)*min([F(1)]+factors)
        add('FT84-03-category-'+activity,'Actual source category controls the factor','FT84-Q03',{'activity':activity,'noStockOrOutputInvented':True,'factorsIndependentlyEligibleWhereListed':True,'separateWaitComparator':'hypothetical actually supplied independent1440-minute wait to test nonreduction;not a new wait requirement on any named process'}, {'baseMinutes':base,'fixedWaitMinutes':1440},[],{'activeMinutes':actual,'fixedWaitMinutes':1440},[('minutes',actual,expected),('no wait reduction',1440,1440)],scope='CATEGORY_AND_ARITHMETIC_BOUNDARY_NOT_COMPLETE_MANUFACTURE')
    # Existing recipe121 physical work has a distinct incorporation rule.
    plan=[900,6300];seq=[(0,600,False),(0,900,True),(1,1800,False),(1,6300,True)];a=credit=0;trace=[]
    for step,sec,done in seq:
        a+=sec
        if done:credit+=plan[step]
        trace.append({'phase':step,'workSeconds':sec,'completed':done,'actualSeconds':a,'creditedSeconds':credit})
    add('FT84-03-recipe121-phases','Research and short kits do not erase actual manufacture incorporation','FT84-Q03',{'completeRecipe121':'full source retained','actualMaterialsBodiesAndStation':'source-qualified premises;not created by this case','requiredStock':{'LuminousCrystal':2,'bronzeDragonRib':1,'completeNeverMagicallyAlteredHosts':6},'maximumAssistants':0}, {'requiredCreditSeconds':7200,'phaseSeconds':plan},trace,{'creditedSeconds':credit,'actualSeconds':a,'completionCheckNowDue':True,'outputsAlreadyGranted':0},[('actual',a,9600),('credit',credit,7200),('no assistant',0,0)],scope='COMPLETE_WORK_LEDGER_ONLY_NO_MANUFACTURE_ROLL_OR_OUTPUT')
    for minutes,inside,bonus in [(20,20,3),(30,30,3),(31,30,0),(480,20,0)]:
        eligible=minutes<=30 and minutes==inside;addhp=3 if eligible else 0
        add(f'FT84-03-rest-whole-{minutes}','FA13 whole-job boundary remains unchanged','FT84-Q03',{'baseRepair':'actual independently authorized FA13-style partial repair','PB':3,'complexBodyToolsMaterialsAndSafeOwnerRest':'TEST_ONLY premises','durationVariantsAreBoundaryFixturesNotNewRecipes':True}, {'HP':2,'maxHP':10,'charges':1,'service':4,'fuel':3,'materialCp':100},[{'event':'actual authorized successful repair','wholeJobMinutes':minutes,'insideRestMinutes':inside,'actualBaseRestoration':2,'spentMaterialCp':20}], {'HP':4+addhp,'maxHP':10,'charges':1,'service':4,'fuel':3,'materialCp':80,'beneficialRestGrantedByThisTest':False},[('bonus',addhp,bonus),('actual HP',4+addhp,4+bonus),('whole job exception',eligible,bonus>0)],scope='RETAINED_WHOLE_JOB_BOUNDARY_NOT_REST_OR_REPAIR_ENGINE')
    return {'id':'FT84-NEW-ISOLATED-WORK-CASES-01','cases':cases,'caseCount':len(cases),'assertions':checks,'assertionCount':len(checks),'failures':sum(not c['pass'] for c in checks),'scope':'Only new standard-library finite specifications executed. Actual permissions, content, class milestones, stock/worksites and safety are disclosed premises; no game runtime or supplied project module is imported.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();r=wire(run());b=(json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode()
    if args.output:
        with args.output.open('xb') as f:f.write(b)
    print(json.dumps({'cases':r['caseCount'],'assertions':r['assertionCount'],'failures':r['failures']}))
