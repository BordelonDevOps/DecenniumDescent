"""Bounded Fishing arithmetic and evidence transactions, not a game runtime.

WorldEvidence contains externally governed, cited historical records. This helper
can check references, quantities and chronology, but cannot authenticate a Director,
invent local stock or establish real behavior, fit, legal access or placement.
Synthetic records in validation are explicitly fixtures, never campaign evidence.
No boolean supplied by a caller is accepted as proof of those world facts.
"""
from copy import deepcopy
from fractions import Fraction as F
from math import floor, ceil

CANONICAL = ('id','kind','actor','ability','proficiency','actualRoll','automaticResult','taskCategory')
METHODS = {'Rod':{'Rod','Line','Hook','Tackle','Lure','Bait','Rig'},
           'Net':{'Net','Lure','Bait','Rig'}, 'Trap':{'Trap','Lure','Bait','Rig'}}
PRIMARY_ROLES = {'Hook':{'hook-body'},'Line':{'functional-span'},'Lure':{'core-body'},
    'Rod':{'shaft'},'Tackle':{'control-board','winder'},'Net':{'hoop','primary-mesh','handle'},
    'Trap':{'basket-frame','funnel'},'Rig':{'canister','primary-mount'},'Bait':{'carrier','wrapper'}}


def copper(value, buying=True):
    return F((ceil if buying else floor)(F(value)*100),100)


def finished_reference(recipe, body):
    return F(str(recipe['economy']['recommendedMarketValue'])) / recipe['quantity'] + F(str(body['baselinePriceGp']))


def structural_hp(ordinary, old_max, old_current, old_percent=0, new_percent=0, old_flaw=False, new_flaw=False):
    if ordinary<=0 or old_max<=0 or not 0<=old_current<=old_max:
        raise ValueError('Invalid recorded structural HP')
    if old_percent not in (0,25,50) or new_percent not in (0,25,50):
        raise ValueError('No admitted structural percentage')
    expected_old=ordinary+(max(1,floor(ordinary*old_percent/100)) if old_percent else 0)
    if old_flaw:expected_old=max(1,expected_old//2)
    if old_max!=expected_old:
        raise ValueError('Recorded maximum contradicts ordinary HP, improvement and flaw')
    p=max(old_percent,new_percent)
    maximum=ordinary+(max(1,floor(ordinary*p/100)) if p else 0)
    if old_flaw or new_flaw:maximum=max(1,maximum//2)
    current=max(0,min(maximum,maximum-(old_max-old_current)))
    return {'maximumHP':maximum,'currentHP':current,'durabilityPercent':p,'flawed':old_flaw or new_flaw}


def quality(recipe, band, option='yield'):
    """Counts only. This does not establish reserve ownership or incorporation."""
    q=recipe['quantity'];bait=recipe['recipeFamily']=='Bait'
    if option not in ('yield','property'):raise ValueError('Unknown batch choice')
    if band not in ('Standard','Exceptional','Masterwork','Flawed','Failed','Mishap'):
        raise ValueError('Use the separate crafting framework to resolve the quality band')
    resolved='Failed' if band=='Flawed' and bait and q==1 else band
    n={'Standard':q,'Exceptional':5*q//4,'Masterwork':3*q//2,
       'Flawed':q//2 if q>=2 else 1,'Failed':0,'Mishap':0}[resolved]
    percent=0
    if resolved in ('Exceptional','Masterwork') and option=='property':
        n=q
        if not bait:percent=25 if resolved=='Exceptional' else 50
    return {'resolvedBand':resolved,'quantity':n,'durabilityPercent':percent,
        'addsFlaw':resolved=='Flawed' and q==1 and not bait,'catalystsReturned':0,
        'failedRecovery':resolved=='Failed','maximumReserve':3*q//2}


def bound_body(world, state, models, checkpoint):
    """Validate one current physical body against its creation and inventory.

    These are externally governed records. Matching a model or an inventory
    relationship does not authenticate ownership or generate a missing part.
    """
    if world.record(state['id'],'crafting-body-state',checkpoint)!=state:
        raise ValueError('Current body state must be the actual governing record')
    creation=world.record(state['creationEvidenceId'],'body-creation')
    if (tuple(creation['checkpoint'])>tuple(checkpoint) or
            creation['physicalId']!=state['physicalId'] or creation['bodyModelId']!=state['bodyModelId'] or
            creation['recipeId']!=state['recipeId']):
        raise ValueError('Body differs from its original physical creation record')
    model=models[creation['bodyModelId']]
    if creation['bodyProfile']!=model or state['grade']!=model['grade']:
        raise ValueError('Actual body profile differs from its admitted fixed model')
    primary=creation['primaryConstituents']
    roles=set(primary);packaged=model['family']=='Bait' and roles=={'exclusive-package'}
    if not packaged and roles!=PRIMARY_ROLES[model['family']]:
        raise ValueError('Creation record lacks the modeled original primary assembly')
    original=[ident for ids in primary.values() for ident in ids]+creation.get('additionalIrreplaceableConstituentIds',[])
    if any(len(ids)!=1 for ids in primary.values()) or len(set(original))!=len(original):
        raise ValueError('Original constituent identities must be complete and distinct')
    inventory=world.record(state['inventoryEvidenceId'],'body-inventory',checkpoint)
    if inventory['physicalId']!=state['physicalId'] or inventory['availability']!=state['state']:
        raise ValueError('Inventory belongs to another physical body')
    constituents=inventory['constituents']
    ids=[p['physicalId'] for p in constituents]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate physical constituent in inventory')
    by_id={p['physicalId']:p for p in constituents}
    if not set(original)<=set(by_id):raise ValueError('Actual original primary constituent is missing')
    for ident in original:
        part=by_id[ident]
        if part['originalBodyId']!=creation['physicalId'] or part['condition'] not in ('intact','damaged','broken'):
            raise ValueError('Original material is unavailable, destroyed or substituted')
    if model['family']!='Bait':
        if (creation['strongestDurabilityPercent']!=state['durabilityPercent'] or
                creation['persistentFlaw']!=state['flawed']):
            raise ValueError('Structural improvement and persistent flaw contradict the body record')
        structural_hp(model['ordinaryMaximumStructuralHP'],state['maximumHP'],state['currentHP'],
            state['durabilityPercent'],0,state['flawed'],False)
    return creation,model,inventory,by_id,packaged


def ordered_output(recipe, band, reserves, option='yield', *, world=None, order_evidence_id=None, models=None):
    """Physical reserves are historical records; call only after lawful work.

    This checks the recorded stock, not the truth of a claim to own it. The caller
    must obtain these records from the actual governing inventory/work ledger.
    """
    if world is None or models is None or not order_evidence_id:
        raise ValueError('Actual order, creation, inventory and reservation records are required')
    order=world.record(order_evidence_id,'fishing-crafting-order');cp=order['checkpoint']
    mid='fishing.'+('bait-dose' if recipe['recipeFamily']=='Bait' else recipe['recipeFamily'].lower())
    if order['recipeId']!=recipe['id'] or order['bodyModelId']!=mid:
        raise ValueError('Order recipe and admitted body model must agree')
    resolution=world.record(order['qualityResolutionEvidenceId'],'crafting-quality-resolution',cp)
    if (resolution['orderId']!=order['id'] or resolution['recipeId']!=recipe['id'] or
            resolution['band']!=band or resolution['option']!=option):
        raise ValueError('Use the actual separately resolved crafting outcome')
    if order['orderedBodyStateIds']!=[r['id'] for r in reserves]:
        raise ValueError('Physical reserve order cannot be changed after the outcome')
    out=quality(recipe,band,option);needed=out['maximumReserve']
    if len(reserves)!=needed or len({x['id'] for x in reserves})!=needed:
        raise ValueError('Exact exclusive ordered reserve required')
    occupied=set()
    for r in reserves:
        creation,model,inventory,parts,packaged=bound_body(world,r,models,cp)
        if model['id']!=mid or creation['recipeId'] is not None:
            raise ValueError('Reserve must be the actual admitted mundane body family')
        reservation=world.record(r['reservationEvidenceId'],'body-reservation',cp)
        if (reservation['physicalId']!=r['physicalId'] or reservation['orderId']!=order['id'] or
                reservation['state']!='active' or inventory['reservedForOrderId']!=order['id']):
            raise ValueError('Every physical reserve must belong exclusively to this order')
        physical=set(parts)|{r['physicalId']}|{z['physicalId'] for p in parts.values() for z in p.get('recoveredOriginalSections',[])}
        if occupied&physical:raise ValueError('Reserve bodies cannot share physical constituents')
        occupied.update(physical)
        if r['state']!='available-reserved' or r['grade']!='Standard' or r['priorMagicalAlteration']:
            raise ValueError('Unavailable or ineligible reserve pauses completion')
        if recipe['recipeFamily']=='Bait':
            if not r['complete'] or r['materialCondition']!='eligible':
                raise ValueError('Actual eligible carrier and wrapper required')
            primary=creation['primaryConstituents']
            if packaged:
                if len(primary['exclusive-package'])!=1:raise ValueError('One exclusive physical packet required')
                packet=parts[primary['exclusive-package'][0]]
                if (not packet['exclusivePackagedStock'] or packet['carrierCondition']!='eligible' or
                        packet['wrapperCondition']!='eligible' or F(str(packet['carrierLb']))!=F(1,10) or
                        F(str(packet['wrapperLb']))!=F(1,100)):
                    raise ValueError('Packaged carrier/wrapper is ineligible')
            else:
                for role,mass in [('carrier',F(1,10)),('wrapper',F(1,100))]:
                    if len(primary[role])!=1:raise ValueError('One actual carrier and wrapper per dose blank')
                    part=parts[primary[role][0]]
                    if part['materialCondition']!='eligible' or F(str(part['massLb']))!=mass:
                        raise ValueError('Carrier or wrapper is destroyed, spoiled or wrong mass')
        elif r['currentHP']<=0 or not r['complete']:
            raise ValueError('Incomplete or Broken body pauses completion')
    selected=deepcopy(reserves[:out['quantity']])
    for body in selected:
        if recipe['recipeFamily']!='Bait':
            body.update(structural_hp(models[mid]['ordinaryMaximumStructuralHP'],body['maximumHP'],body['currentHP'],body['durabilityPercent'],out['durabilityPercent'],body['flawed'],out['addsFlaw']))
    return {'outcome':out,'selected':selected,'unused':deepcopy(reserves[out['quantity']:])}


def repair_quote(recipe, body, current_hp, maximum_hp, original_required, original_surviving):
    """Arithmetic only. Use qualified_repair_quote for an actual repair route.

    Lists here are calculator premises, not proof of an item's primary assembly.
    """
    if recipe['recipeFamily']=='Bait':raise ValueError('Bait cannot be repaired')
    if body['family']!=recipe['recipeFamily']:raise ValueError('Wrong body family for recipe quotation')
    if not original_required or len(set(original_required))!=len(original_required):
        raise ValueError('Prerecorded original primary assembly is required')
    if not set(original_required)<=set(original_surviving):
        raise ValueError('Missing original primary constituent')
    if maximum_hp<=0 or not 0<=current_hp<=maximum_hp:raise ValueError('Invalid HP record')
    broken=current_hp==0
    value=finished_reference(recipe,body) if broken else F(str(body['baselinePriceGp']))
    return {'dc':recipe['craftingCheck']['targetDC'] if broken else 10,
        'hours':max(F(8 if broken else 1),F(maximum_hp,10)),
        'materialReferenceGp':value/4,'purchaseGp':copper(value/4),
        'successHP':maximum_hp,'refills':[],'qualification':'arithmetic-only'}


def qualified_repair_quote(world, state_id, cards, models):
    """Qualify original material/model/recipe before returning the fixed quote.

    This records no completed repair and grants no restored HP or inventory.
    Actual lawful repair work and its resolved outcome remain separate.
    """
    state=world.record(state_id,'crafting-body-state');cp=state['checkpoint']
    creation,model,inventory,parts,packaged=bound_body(world,state,models,cp)
    if model['family']=='Bait':raise ValueError('Bait cannot be repaired')
    if not creation['recipeId'] or state['recipeId']!=creation['recipeId'] or not state['priorMagicalAlteration']:
        raise ValueError('Repair must bind the actual finished item recipe')
    recipe=cards[creation['recipeId']]['sourceRecipe']
    mid='fishing.'+recipe['recipeFamily'].lower()
    if model['id']!=mid:raise ValueError('Actual finished recipe and body model disagree')
    if state['state']!='available-for-repair' or inventory['reservedForOrderId'] is not None:
        raise ValueError('Body is not available for this repair')
    if model['family']=='Line':
        for ident in creation['primaryConstituents']['functional-span']:
            part=parts[ident];sections=part['recoveredOriginalSections']
            if not sections or len({z['physicalId'] for z in sections})!=len(sections):
                raise ValueError('Actual original Line sections required')
            end=F(0)
            for section in sorted(sections,key=lambda z:F(str(z['startFeet']))):
                if (section['originalConstituentId']!=ident or section['condition'] not in ('intact','damaged','broken') or
                        F(str(section['startFeet']))!=end or F(str(section['endFeet']))<=end):
                    raise ValueError('Original Line span has a missing, substituted or overlapping section')
                end=F(str(section['endFeet']))
            if end!=50:raise ValueError('Complete original fifty-foot Line span required')
    required=[p for ids in creation['primaryConstituents'].values() for p in ids]+creation.get('additionalIrreplaceableConstituentIds',[])
    quote=repair_quote(recipe,model,state['currentHP'],state['maximumHP'],required,list(parts))
    quote.update({'qualification':'governing body/model/recipe/inventory records checked',
        'physicalId':state['physicalId'],'creationEvidenceId':creation['id'],
        'stateEvidenceId':state['id'],'recipeId':recipe['id'],'bodyModelId':model['id'],
        'persistentFlaw':state['flawed'],'requiredOriginalIds':required,'repairCompleted':False})
    return quote


class WorldEvidence:
    """Read-only supplied records; never a world-fact generator or authenticator.

    Each record names its governing authority, exact checkpoint and citations.
    Evidence itself must establish actual apparatus geometry, receptive prey,
    access, hazards and receiving placement. This class only requires that those
    independently reviewed records are present. Production callers must supply
    real campaign authority; test_fixture=True deliberately cannot certify play.
    """
    def __init__(self, records, *, test_fixture=False):
        self._records=deepcopy(records);self.test_fixture=test_fixture
        for key,r in self._records.items():
            if not isinstance(r,dict) or r.get('id')!=key or not r.get('authority') or not r.get('citations'):
                raise ValueError('Cited governing record, not a caller assertion, is required')
            if r.get('fixture',False) and not test_fixture:raise ValueError('Synthetic record is not campaign evidence')
            if len(r.get('checkpoint',()))!=3:raise ValueError('Historical time/phase/sequence required')

    def record(self, key, kind, checkpoint=None):
        if key not in self._records:raise ValueError('Missing actual governing record')
        r=deepcopy(self._records[key])
        if r['kind']!=kind or (checkpoint is not None and tuple(r['checkpoint'])!=tuple(checkpoint)):
            raise ValueError('Wrong kind or historical checkpoint')
        return r

    def applicable_record(self, key, kind, checkpoint):
        r=self.record(key,kind);cp=tuple(checkpoint)
        if tuple(r['checkpoint'])>cp or tuple(r.get('effectiveFrom',r['checkpoint']))>cp or (
                r.get('effectiveUntil') is not None and cp>=tuple(r['effectiveUntil'])):
            raise ValueError('Governing record is not applicable at this historical checkpoint')
        return r


def unused_bait_qualification(world, evidence_id, checkpoint):
    dose=world.record(evidence_id,'unused-bait',checkpoint)
    history=world.record(dose['storageHistoryEvidenceId'],'bait-storage-history',checkpoint)
    completion=world.record(history['completionEvidenceId'],'finished-bait-completion')
    for record in (history,completion):
        if record['physicalId']!=dose['physicalId'] or record['recipeId']!=dose['recipeId']:
            raise ValueError('Bait storage and completion must belong to this actual dose')
    if completion['quantity']!=1 or F(str(completion['carrierLb']))!=F(1,10):
        raise ValueError('One actually completed whole Bait dose required')
    last=tuple(completion['checkpoint']);unprotected=0
    for span in history['intervals']:
        start,end=tuple(span['start']),tuple(span['end'])
        if start!=last or end<start or end>tuple(checkpoint):
            raise ValueError('Bait age history must cover its whole life without gaps or resets')
        protection=span.get('preservationEvidenceId')
        if protection:
            premise=world.applicable_record(protection,'compatible-bait-preservation',start)
            if (premise['physicalId']!=dose['physicalId'] or premise['recipeId']!=dose['recipeId'] or
                    not premise['existingProcedureRef'] or premise['disposition']!='compatible-active' or
                    tuple(premise['effectiveUntil'])<end):
                raise ValueError('Protected age requires an actual compatible existing preservation record')
        else:unprotected+=end[0]-start[0]
        last=end
    if last!=tuple(checkpoint) or F(str(dose['unprotectedHours']))*3600!=unprotected:
        raise ValueError('Rewrapping, opening or transfer cannot reset accumulated bait age')
    if (dose['condition']!='eligible' or dose['quantity']!=1 or F(str(dose['carrierLb']))!=F(1,10) or
            not 0<=unprotected<86400):
        raise ValueError('Bait dose is spoiled, destroyed, fractional or unavailable')
    return dose,unprotected


def bait_receipt(world, exposure_id, assembly):
    exposure=world.record(exposure_id,'bait-exposure')
    if (exposure['attemptId']!=assembly['attemptId'] or exposure['assemblyId']!=assembly['assemblyId'] or
            assembly['itemRecipeIds'].get(exposure['physicalId'])!=exposure['recipeId'] or
            assembly['itemFamilyById'].get(exposure['physicalId'])!='Bait'):
        raise ValueError('Bait receipt must bind the actual registered dose, recipe, attempt and assembly')
    use=world.record(exposure['inventoryUseEvidenceId'],'bait-inventory-use',exposure['checkpoint'])
    fields=('physicalId','recipeId','attemptId','assemblyId','locationId','locationKind')
    if any(use[k]!=exposure[k] for k in fields) or use['quantity']!=1 or F(str(use['carrierLb']))!=F(1,10) or use['purpose']!='fishing-bait-exposure':
        raise ValueError('Receipt must match the actual one-dose inventory expenditure and location')
    if tuple(exposure['expiresAt'])<=tuple(exposure['checkpoint']) or exposure['expiresAt'][0]!=exposure['checkpoint'][0]+3600:
        raise ValueError('Receipt expiry is sixty elapsed minutes from actual exposure')
    return exposure,use


def rig_deployment(world, assembly):
    """Bind actual Rig support, one physical load, mount work and dispersal."""
    ident=next((i for i,f in assembly['itemFamilyById'].items() if f=='Rig'),None)
    if ident is None:return None
    if not assembly.get('rigDeploymentEvidenceId'):raise ValueError('Rig benefits require its actual deployment record')
    deployment=world.record(assembly['rigDeploymentEvidenceId'],'rig-deployment');cp=deployment['checkpoint']
    if (deployment['attemptId']!=assembly['attemptId'] or deployment['assemblyId']!=assembly['assemblyId'] or
            deployment['dispenserPhysicalId']!=ident):
        raise ValueError('Rig deployment belongs to another attempt, assembly or dispenser')
    reservation=world.record(deployment['reservationEvidenceId'],'fishing-reservation')
    if (reservation['attemptId']!=assembly['attemptId'] or
            reservation.get('rigMountWorkByPhysicalId',{}).get(ident)!=deployment['mountWorkEvidenceId']):
        raise ValueError('Rig deployment must retain its actual pre-setup mounting')
    mount=world.record(deployment['mountWorkEvidenceId'],'work-record')
    if (mount['physicalId']!=ident or mount['attemptId']!=assembly['attemptId'] or mount['phase']!='rig-mount' or
            tuple(mount['checkpoint'])>tuple(reservation['checkpoint']) or
            active_work_seconds(mount,mount['startedAtSeconds'],reservation['checkpoint'][0])!=300):
        raise ValueError('Rig mounting needs five additional actual minutes before main setup')
    support=world.record(deployment['supportEvidenceId'],'rig-support',cp)
    presentation=world.record(deployment['presentationEvidenceId'],'bait-presentation',cp)
    if (support['dispenserPhysicalId']!=ident or support['assemblyId']!=assembly['assemblyId'] or
            not support['supportPhysicalId'] or support['disposition']!='stable-compatible' or
            not 0<=support['tetherPathFeet']<=10 or not 0<=support['distanceToAssemblyPointFeet']<=5 or
            support['assemblyPointId']!=presentation['responsePointId'] or
            support['dispenserPointId']!=deployment['dispenserPointId'] or
            presentation['assemblyId']!=assembly['assemblyId']):
        raise ValueError('Rig needs actual support, legal tether and proximity to this presentation')
    load=world.record(deployment.get('loadEvidenceId'),'rig-chum-load',cp)
    use=world.record(deployment['chumUseEvidenceId'],'rig-chum-use',cp)
    if (load['dispenserPhysicalId']!=ident or load['attemptId']!=assembly['attemptId'] or
            load['assemblyId']!=assembly['assemblyId'] or load['compatibility']!='compatible' or
            not 0<F(str(load['occupiedVolumePints']))<=1 or F(str(load['totalMassLb']))!=1 or
            F(str(load['wrapperMassIncludedLb']))!=0):
        raise ValueError('Rig requires one compatible pound within one pint, with wrapper excluded')
    portions=[];mass=F(0)
    for key in load['ordinaryPortionEvidenceIds']:
        stock=world.record(key,'chum-inventory',cp)
        if (stock['stockClass']!='ordinary-compatible-chum' or stock['state']!='available-unspent' or
                stock['materialCondition']!='eligible' or F(str(stock['massLb']))<=0):
            raise ValueError('Actual eligible ordinary chum stock is required')
        portions.append(stock['physicalId']);mass+=F(str(stock['massLb']))
    if len(set(portions))!=len(portions):raise ValueError('Chum portions must be physically distinct')
    bid=load['finishedBaitPhysicalId']
    if bid is not None:
        exposure,_=bait_receipt(world,load['finishedBaitExposureEvidenceId'],assembly)
        if (exposure['physicalId']!=bid or tuple(exposure['checkpoint'])!=tuple(cp) or
                exposure['locationKind']!='rig-chum' or exposure['locationId']!=deployment['dispenserPointId'] or
                bid in portions or F(str(load['finishedBaitCarrierLb']))!=F(1,10) or mass!=F(9,10)):
            raise ValueError('Rig Bait substitution is one tenth pound plus nine tenths actual ordinary chum')
        mass+=F(1,10)
    elif load['finishedBaitExposureEvidenceId'] is not None or F(str(load['finishedBaitCarrierLb']))!=0:
        raise ValueError('Undeclared finished Bait cannot fill a Rig load')
    if mass!=1:raise ValueError('Actual chum allotment does not total one pound')
    if (deployment['finishedBaitPhysicalId']!=bid or deployment['finishedBaitExposureEvidenceId']!=load['finishedBaitExposureEvidenceId'] or
            use['deploymentEvidenceId']!=deployment['id'] or use['loadEvidenceId']!=load['id'] or
            use['dispenserPhysicalId']!=ident or use['attemptId']!=assembly['attemptId'] or use['assemblyId']!=assembly['assemblyId'] or
            use['ordinaryPortionIds']!=portions or use['finishedBaitPhysicalId']!=bid or
            F(str(use['committedMassLb']))!=1 or use['disposition']!='opened-dispersal'):
        raise ValueError('Opening dispersal must bind one actual committed chum allotment')
    return {'deployment':deployment,'load':load,'use':use,'ordinaryPortionIds':portions,'support':support,'mount':mount}


def rig_current_eligibility(world, assembly, body, checkpoint):
    bound=rig_deployment(world,assembly);deployment=bound['deployment']
    if tuple(deployment['checkpoint'])>tuple(checkpoint):raise ValueError('Rig cannot operate before its actual deployment')
    state=world.record(assembly['rigStateEvidenceId'],'rig-operational-state',checkpoint)
    if (state['deploymentEvidenceId']!=deployment['id'] or state['dispenserPhysicalId']!=body['physicalId'] or
            state['attemptId']!=assembly['attemptId'] or state['assemblyId']!=assembly['assemblyId'] or
            state['itemStateEvidenceId']!=body['id'] or not state['locationId'] or
            state['assemblyPointId']!=bound['support']['assemblyPointId']):
        raise ValueError('Current Rig state must bind its actual deployment and physical body')
    if state['disposition'] not in ('deployed','spilled','detached','retrieved','abandoned'):
        raise ValueError('Unknown actual Rig disposition')
    if body['currentHP']==0 and state['disposition']=='deployed':
        raise ValueError('Broken deployed Rig must preserve the actual spilled-chum disposition')
    if state['disposition']!='deployed':return False
    support=world.record(state['supportEvidenceId'],'rig-support',checkpoint)
    if support['dispenserPhysicalId']!=body['physicalId'] or support['assemblyId']!=assembly['assemblyId']:
        raise ValueError('Current support belongs to another Rig or assembly')
    return (support['disposition']=='stable-compatible' and bool(support['supportPhysicalId']) and
        0<=support['tetherPathFeet']<=10 and 0<=support['distanceToAssemblyPointFeet']<=5 and
        support['assemblyPointId']==state['assemblyPointId'] and support['dispenserPointId']==deployment['dispenserPointId'])


def effect_candidates(world, evidence_id, cards):
    e=world.record(evidence_id,'catch-roll')
    roll=e['roll'];assembly=world.record(e['assemblyEvidenceId'],'assembly',e['checkpoint'])
    if tuple(roll)!=CANONICAL and set(roll)!=set(CANONICAL):
        raise ValueError('Complete canonical roll descriptor required')
    if assembly['method'] not in METHODS:raise ValueError('Unsupported capture method')
    if roll['kind']!='ability-check' or roll['ability']!='WIS' or roll['proficiency']!='Fishing tackle' or roll['taskCategory']!='ordinary-provision-catch':
        return {'bonus':0,'extra':0,'eligibleIds':[],'extraByPhysicalId':{},'affinityByPhysicalId':{}}
    if not roll['actualRoll'] or roll['automaticResult']:
        return {'bonus':0,'extra':0,'eligibleIds':[],'extraByPhysicalId':{},'affinityByPhysicalId':{}}
    registered={ident for ident,rid in assembly['itemRecipeIds'].items() if rid is not None}
    if {view['physicalId'] for view in e['items']}!=registered:
        raise ValueError('Every registered magical candidate needs its own current view')
    eligible=[];families=set();ids=set()
    for view in e['items']:
        if any(view['roll'].get(k)!=roll[k] for k in CANONICAL):
            raise ValueError('Every item must describe the same current roll')
        ident=view['physicalId']
        if ident in ids:raise ValueError('Duplicate physical item')
        ids.add(ident)
        if assembly['itemRecipeIds'].get(ident)!=view['recipeId']:
            raise ValueError('Item recipe differs from the governing assembly record')
        c=cards[view['recipeId']];r=c['sourceRecipe'];fam=r['recipeFamily']
        if ident not in assembly['participatingItemIds'] or fam not in METHODS[assembly['method']]:continue
        if fam in families:raise ValueError('One contributing candidate per family')
        families.add(fam)
        state=world.record(view['stateEvidenceId'],'item-state',e['checkpoint'])
        if state['physicalId']!=ident:raise ValueError('Wrong physical item history')
        if fam=='Bait':
            receipt_id=assembly.get('baitExposureEvidenceId')
            if not receipt_id:
                if state.get('exposureEvidenceId') or state.get('receiptAttemptId'):
                    raise ValueError('Unexposed Bait cannot carry a copied receipt claim')
                qualifies=False
            else:
                exposure,use=bait_receipt(world,receipt_id,assembly)
                effect=world.record(state['baitEffectStateEvidenceId'],'assembly-bait-state',e['checkpoint'])
                if (exposure['physicalId']!=ident or state['exposureEvidenceId']!=receipt_id or
                        state['receiptAttemptId']!=assembly['attemptId'] or state['exposedAt']!=exposure['checkpoint'] or
                        state['expiresAt']!=exposure['expiresAt'] or effect['exposureEvidenceId']!=receipt_id or
                        effect['assemblyId']!=assembly['assemblyId'] or effect['attemptId']!=assembly['attemptId'] or
                        effect['suppressed']!=state['assemblyBaitSuppressed']):
                    raise ValueError('Current receipt, age and suppression must concern this assembly bait effect')
                qualifies=tuple(exposure['checkpoint'])<=tuple(e['checkpoint'])<tuple(exposure['expiresAt']) and not effect['suppressed']
        else:
            qualifies=(state['currentHP']>0 and state['complete'] and not state['suppressed'] and not state['melded'] and
                state['participatingAttemptId']==assembly['attemptId'])
            if fam=='Rig':qualifies=rig_current_eligibility(world,assembly,state,e['checkpoint']) and qualifies
        if qualifies:eligible.append((ident,r['mechanics']['fishingBonus'],r['mechanics']['extraYield'],r['mechanics']['attracts']))
    return {'bonus':max((x[1] for x in eligible),default=0),
        'extra':max((x[2] for x in eligible),default=0),'eligibleIds':[x[0] for x in eligible],
        'extraByPhysicalId':{x[0]:x[2] for x in eligible},'affinityByPhysicalId':{x[0]:x[3] for x in eligible}}


def require_catch_roll(roll, actor):
    """A zero equipment selector result does not admit an unrelated event."""
    if (set(roll)!=set(CANONICAL) or not isinstance(roll.get('id'),str) or not roll['id'] or
            roll.get('actor')!=actor or roll.get('kind')!='ability-check' or
            roll.get('ability')!='WIS' or roll.get('proficiency')!='Fishing tackle' or
            roll.get('taskCategory')!='ordinary-provision-catch' or
            roll.get('actualRoll') is not True or roll.get('automaticResult') is not False):
        raise ValueError('An actual canonical WIS/Fishing-tackle catch check is required')


def declared_catch_profile(world, evidence_id, method, checkpoint):
    profile=world.record(evidence_id,'catch-profile')
    if tuple(profile['checkpoint'])>tuple(checkpoint) or profile['method']!=method:
        raise ValueError('Catch profile must be declared for this method before commitment')
    dc=profile['dc']
    if not isinstance(dc,int) or isinstance(dc,bool) or dc<=0:
        raise ValueError('Invalid declared catch DC')
    if dc not in (12,15,18):
        if not profile.get('reviewedOverrideEvidenceId'):
            raise ValueError('Nonordinary DC lacks independently reviewed override evidence')
        override=world.record(profile['reviewedOverrideEvidenceId'],'reviewed-catch-dc')
        if (override['catchProfileEvidenceId']!=profile['id'] or override['dc']!=dc or
                override['method']!=method or override['reviewStatus']!='reviewed' or
                tuple(override['checkpoint'])>tuple(checkpoint)):
            raise ValueError('Nonordinary DC requires its independent reviewed profile override')
    return profile


def validate_catch_resolution(world, result, attempt, checkpoint):
    """Consume separately resolved Core and credential records, not dice rules.

    Fishing recognizes only WIS and one applicable PB/expertise contribution as
    personal terms. Other lawful ordinary bonuses need their own bound records.
    An unattended Trap snapshots just WIS and proficiency, never those bonuses.
    """
    require_catch_roll(result['canonicalRoll'],attempt['lead'])
    core=world.record(result['coreResolutionEvidenceId'],'core-check-resolution',checkpoint)
    if (core['attemptId']!=attempt['id'] or core['canonicalRoll']!=attempt['canonicalRoll'] or
            core['catchProfileEvidenceId']!=attempt['catchProfileEvidenceId'] or
            core['dc']!=attempt['catchDC'] or result['dc']!=attempt['catchDC'] or
            result['catchProfileEvidenceId']!=attempt['catchProfileEvidenceId'] or
            core['degree']!=result['degree'] or core['physicalId']!=attempt['selectedCreatureId'] or
            core['personalContributions']!=result['personalContributions'] or
            core['equipmentBonus']!=result['equipmentBonus'] or
            core['assistantBonus']!=result['assistantBonus'] or
            core['credentialEvidenceId']!=result['credentialEvidenceId']):
        raise ValueError('Catch resolution differs from its declared profile or resolved Core record')
    credential=world.record(result['credentialEvidenceId'],'fishing-credential')
    credential_cp=checkpoint
    if attempt['method']=='Trap':
        config=world.record(result['setterConfigurationEvidenceId'],'trap-configuration')
        credential_cp=config['checkpoint']
        if config['credentialEvidenceId']!=credential['id']:
            raise ValueError('Trap must retain its governing setup credential')
    if tuple(credential['checkpoint'])!=tuple(credential_cp) or credential['actor']!=attempt['lead']:
        raise ValueError('Credential belongs to another actor or historical configuration')
    if credential['ability']!='WIS' or credential['proficiency']!='Fishing tackle':
        raise ValueError('Wrong ability or tool credential')
    training=credential['training'];pb=credential['proficiencyBonus'];wis=credential['wisModifier']
    if (training not in ('untrained','trained','expertise') or
            not isinstance(pb,int) or isinstance(pb,bool) or pb<0 or
            not isinstance(wis,int) or isinstance(wis,bool)):
        raise ValueError('Invalid governing proficiency or WIS record')
    personal={'WIS':wis,'Fishing':0 if training=='untrained' else pb*(2 if training=='expertise' else 1)}
    if result['personalContributions']!=personal:
        raise ValueError('Use WIS and one PB or replacing expertise contribution, without extra fields')
    if core['untrainedDisadvantageApplied'] is not (training=='untrained'):
        raise ValueError('Core must include the actual untrained Fishing disadvantage source')
    bonus_ids=core.get('otherBonusEvidenceIds',[])
    if attempt['method']=='Trap' and bonus_ids:
        raise ValueError('Trap personal configuration has no additional bonuses')
    if len(set(bonus_ids))!=len(bonus_ids):raise ValueError('Duplicate personal bonus evidence')
    for key in bonus_ids:
        bonus=world.record(key,'catch-personal-bonus',checkpoint)
        if (bonus['actor']!=attempt['lead'] or bonus['rollId']!=attempt['canonicalRoll']['id'] or
                bonus['approvedTaskCategory']!='ordinary-provision-catch'):
            raise ValueError('Additional bonus is not governed for this actual catch check')
    return core


def bound_stock_allocation(world, record, checkpoint):
    """Resolve finite physical membership from the applicable stock version."""
    manifest=world.applicable_record(record.get('stockManifestEvidenceId'),'finite-stock-manifest',checkpoint)
    allocation=world.applicable_record(record.get('allocationEvidenceId'),'stock-allocation',checkpoint)
    members=manifest['memberPhysicalIds'];footprint=allocation['memberPhysicalIds']
    if (manifest['sharedStockId']!=record['sharedStockId'] or not manifest['siteId'] or
            manifest['version']!=record['stockVersion'] or
            allocation['stockManifestEvidenceId']!=manifest['id'] or allocation['stockVersion']!=manifest['version'] or
            allocation['sharedStockId']!=manifest['sharedStockId'] or
            allocation['partitionId']!=record['allocationPartitionId'] or
            len(set(members))!=len(members) or len(set(footprint))!=len(footprint) or
            not set(footprint)<=set(members) or allocation['scope'] not in ('all-members','physical-members') or
            (allocation['scope']=='all-members' and set(footprint)!=set(members))):
        raise ValueError('Allocation must bind actual finite physical membership and its applicable stock version')
    if 'candidateCreatureIds' in record:
        candidates=record['candidateCreatureIds']
        if len(set(candidates))!=len(candidates) or not set(candidates)<=set(footprint):
            raise ValueError('Opportunity candidates must belong to the actual allocated stock')
    return {'manifest':manifest,'allocation':allocation,'physicalIds':sorted(footprint)}


def weighted_response(world, evidence_id, selected_affinity, draw):
    """Allocate once from a bound opportunity, never from an invented radius.

    The origin is the governing physical presentation/capture point, not the
    angler. Selected-attraction allocation excludes paths over thirty feet.
    Ordinary visible response is a separate recorded procedure, with no magic
    preference; its physical method limits are checked by the catch journal.
    """
    e=world.record(evidence_id,'response-candidates')
    cp=e['checkpoint']
    opportunity=world.record(e['opportunityEvidenceId'],'opportunity',cp)
    bound_stock_allocation(world,opportunity,cp)
    assembly=world.record(e['assemblyEvidenceId'],'assembly',cp)
    origin=world.record(e['originEvidenceId'],'response-origin',cp)
    attracted=selected_affinity is not None
    if e['allocationProcedure']!=('selected-attraction' if attracted else 'ordinary-visible-response'):
        raise ValueError('Response procedure differs from the committed attraction choice')
    if (e['opportunityId']!=opportunity['opportunityId'] or
            origin['opportunityId']!=opportunity['opportunityId'] or
            origin['attemptId']!=assembly['attemptId'] or
            origin['assemblyEvidenceId']!=assembly['id']):
        raise ValueError('Response origin, assembly and opportunity must agree')
    if attracted:
        source=e['attractionPhysicalId']
        if source not in assembly['participatingItemIds']:
            raise ValueError('Attraction source is not part of this assembly')
        if assembly['itemFamilyById'][source]=='Rig':
            deployment=world.record(assembly['rigDeploymentEvidenceId'],'rig-deployment',cp)
            if (origin['pointKind']!='rig-dispenser' or
                    deployment['attemptId']!=assembly['attemptId'] or
                    deployment['dispenserPhysicalId']!=source or
                    origin['pointId']!=deployment['dispenserPointId']):
                raise ValueError('Response must originate at the actual Rig dispenser')
        else:
            presentation=world.record(assembly['presentationEvidenceId'],'bait-presentation',cp)
            if (origin['pointKind']!='bait-lure-point' or
                    presentation['attemptId']!=assembly['attemptId'] or
                    not presentation['sourcePhysicalIds'] or
                    origin['pointId']!=presentation['responsePointId']):
                raise ValueError('Response must originate at the actual bait/Lure point')
    else:
        admission=world.record(assembly['admissionEvidenceId'],'physical-admission',cp)
        if (e['attractionPhysicalId'] is not None or origin['pointKind']!='ordinary-capture-point' or
                origin['pointId']!=admission['capturePointId']):
            raise ValueError('Ordinary response requires its own actual capture point')
    candidates=sorted(e['candidates'],key=lambda c:c['physicalId'])
    if len({c['physicalId'] for c in candidates})!=len(candidates):raise ValueError('Duplicate real creature')
    if {c['physicalId'] for c in candidates}!=set(opportunity['candidateCreatureIds']):
        raise ValueError('Response candidates differ from the governing opportunity')
    total=0;rows=[]
    for c in candidates:
        profile=world.applicable_record(c['profileEvidenceId'],'ordinary-prey-profile',cp)
        path=world.record(c['responseEvidenceId'],'response-path',e['checkpoint'])
        if profile['physicalId']!=c['physicalId'] or path['physicalId']!=c['physicalId']:
            raise ValueError('Profile or path belongs to another creature')
        if path['originEvidenceId']!=origin['id'] or path['opportunityId']!=opportunity['opportunityId']:
            raise ValueError('Response path belongs to another origin or opportunity')
        if profile['captureProcedure']!='ordinary-provision' or path['responseDisposition']!='receptive':
            raise ValueError('Encounter resistance or rejection is not ordinary prey response')
        if path['unobstructedWaterPathFeet']<0:raise ValueError('Negative path length')
        # An approved response record is an external premise, not something a
        # caller's `willing=True` flag can substitute for here.
        if attracted and path['unobstructedWaterPathFeet']>30:continue
        weight=2 if attracted and selected_affinity in profile['approvedAffinities'] else 1
        total+=weight;rows.append((c['physicalId'],weight,total))
    if not rows:
        if draw is not None:raise ValueError('Empty site has no response draw')
        return {'physicalId':None,'weights':[],'draw':None}
    if not isinstance(draw,int) or isinstance(draw,bool) or not 1<=draw<=total:
        raise ValueError('One supplied uniform integer draw must fit the finite pool')
    return {'physicalId':next(i for i,w,end in rows if draw<=end),'weights':[(i,w) for i,w,end in rows],'draw':draw}


MATERIAL_GROUPS=('baseline','extraReserve','damagedBaseline','unique')
IRREVERSIBLE_MATERIAL_STATES={'lost','destroyed','removed','spent','forfeited'}


def material_origin_restrictions(manifest):
    restrictions=set(manifest.get('originRestrictions',[]))
    legacy=manifest['resourcePolicy']
    if legacy not in ('permitted','access-denied'):restrictions.add(legacy)
    return restrictions


def material_access_permitted(manifest):
    return manifest.get('accessPermission','permitted' if manifest['resourcePolicy']=='permitted' else 'denied')=='permitted'


def validate_material_manifest(manifest, *, initial=True):
    groups=('baseline','extraReserve','damagedBaseline','unique')
    units=[u for k in groups for u in manifest[k]]
    if len({u['id'] for u in units})!=len(units):raise ValueError('Anatomy units must be disjoint')
    mass=sum((F(str(u['massLb'])) for u in units),F(0))
    if any(F(str(u['massLb']))<0 or (F(str(u['massLb']))==0 and u['state'] not in IRREVERSIBLE_MATERIAL_STATES) for u in units) or mass>F(str(manifest['bodyMassLb'])):
        raise ValueError('Units exceed actual physical body mass')
    for u in units:
        if u['state'] not in IRREVERSIBLE_MATERIAL_STATES|{'available','damaged','spoiled','unavailable'}:
            raise ValueError('Unknown material condition cannot establish availability')
        if u.get('deathOrRemovalTime') is not None and u['deathOrRemovalTime']>manifest['checkpoint'][0]:
            raise ValueError('Recorded material clock cannot begin in this snapshot\'s future')
    for u in manifest['extraReserve']:
        if initial and u['material']=='ordinary-fish-meat' and F(str(u['massLb']))!=1:
            raise ValueError('Extra ordinary-meat unit requires one real pound')
    return True


def validate_material_successor(world, previous, current):
    """Keep finite anatomy and its actual loss/condition history across versions."""
    validate_material_manifest(current,initial=False)
    if (current['physicalId']!=previous['physicalId'] or tuple(current['checkpoint'])<tuple(previous['checkpoint']) or
            current.get('previousManifestEvidenceId')!=previous['id'] or
            not material_origin_restrictions(previous)<=material_origin_restrictions(current)):
        raise ValueError('Material version must retain actual predecessor, donor and immutable origin restrictions')
    before={u['id']:(g,u) for g in MATERIAL_GROUPS for u in previous[g]}
    after={u['id']:(g,u) for g in MATERIAL_GROUPS for u in current[g]}
    if set(before)!=set(after):raise ValueError('Material identities remain recorded even after loss or forfeiture')
    changes={}
    for key,(group,unit) in after.items():
        old_group,old=before[key]
        if (group!=old_group or any(unit[k]!=old[k] for k in ('material','category')) or
                F(str(unit['massLb']))>F(str(old['massLb'])) or
                (old['state'] in IRREVERSIBLE_MATERIAL_STATES and unit['state'] not in IRREVERSIBLE_MATERIAL_STATES)):
            raise ValueError('Material cannot change identity, grow, or return after irreversible loss')
        if unit!=old:changes[key]=(old,unit)
    proved={}
    for key in current.get('transitionEvidenceIds',[]):
        transition=world.applicable_record(key,'material-state-transition',current['checkpoint'])
        if (transition['physicalId']!=current['physicalId'] or transition['fromManifestEvidenceId']!=previous['id'] or
                transition['toManifestEvidenceId']!=current['id'] or not transition['governingProcedure'] or
                tuple(transition['checkpoint'])<=tuple(previous['checkpoint'])):
            raise ValueError('Material change requires its actual governing transition between these versions')
        for change in transition['unitChanges']:
            ident=change['unitId']
            if ident in proved or ident not in changes or (change['fromUnit'],change['toUnit'])!=changes[ident]:
                raise ValueError('Governing transition must bind the exact old and new finite unit')
            old,unit=changes[ident]
            if old['state']!=unit['state'] and unit['state']=='available' and transition.get('conditionChangeDisposition')!='lawful-under-governing-procedure':
                raise ValueError('A new available label is not evidence of an allowed condition treatment')
            if old.get('deathOrRemovalTime')!=unit.get('deathOrRemovalTime'):
                lifecycle=world.applicable_record(change.get('lifecycleEvidenceId'),'material-lifecycle',current['checkpoint'])
                if (lifecycle['physicalId']!=current['physicalId'] or ident not in lifecycle['unitIds'] or
                        lifecycle['deathOrRemovalTime']!=unit.get('deathOrRemovalTime') or
                        lifecycle['priorDeathOrRemovalTime']!=old.get('deathOrRemovalTime') or
                        not lifecycle['governingProcedure'] or unit.get('deathOrRemovalTime') is None or
                        lifecycle['deathOrRemovalTime']>lifecycle['checkpoint'][0] or
                        lifecycle['eventKind'] not in ('death','removal','documented-clock-correction') or
                        (old.get('deathOrRemovalTime') is not None and lifecycle['eventKind']!='documented-clock-correction')):
                    raise ValueError('Established material clocks require their actual governing lifecycle record')
            proved[ident]=key
    if set(proved)!=set(changes):raise ValueError('Changed material snapshot lacks its actual loss or condition transition')
    return current


def material_history_to(world, captured, current):
    chain=[];seen=set();cursor=current
    while cursor['id']!=captured['id']:
        if cursor['id'] in seen:raise ValueError('Material history cannot loop')
        seen.add(cursor['id']);chain.append(cursor)
        cursor=world.record(cursor.get('previousManifestEvidenceId'),'material-manifest')
    if cursor!=captured:raise ValueError('Captured material snapshot cannot be rewritten')
    previous=captured
    for successor in reversed(chain):previous=validate_material_successor(world,previous,successor)
    return previous


def resolve_ordinary_harvest_units(world, evidence_id, recovery, history):
    """Conserve units after an externally resolved lawful harvesting procedure.

    This boundary does not determine legality, life/death, extraction DC/time,
    safety, valuation, unique-drop conditions or actual inventory. Those remain
    in the cited governing harvesting/creature records. Ordinary body resolution
    and partial-category forfeiture cannot be repeated by changing harvesters.
    """
    event=world.record(evidence_id,'resolved-ordinary-harvest')
    donor=event['physicalId'];cp=event['checkpoint']
    if donor in history:raise ValueError('Ordinary harvest already resolved for this physical body')
    prerequisite=world.record(event['lawfulExtractionEvidenceId'],'lawful-extraction',cp)
    manifest=world.record(event['manifestEvidenceId'],'material-manifest',cp)
    captured=recovery['manifestSnapshot']
    capture=world.record(recovery['captureEvidenceId'],'secure-capture')
    if (capture!=recovery['captureSnapshot'] or tuple(recovery['capturedAt'])>tuple(cp) or
            tuple(captured['checkpoint'])>tuple(cp) or tuple(capture['checkpoint'])>tuple(cp)):
        raise ValueError('Actual capture and recovery authorization must exist by extraction')
    choice=world.record(event['choiceEvidenceId'],'harvest-category-choice')
    if any(z['physicalId']!=donor for z in (prerequisite,manifest,captured,choice)) or tuple(choice['checkpoint'])>=tuple(cp):
        raise ValueError('Actual donor-bound prerequisites and prior category choice required')
    material_history_to(world,captured,manifest)
    if not set(recovery['originRestrictions'])<=material_origin_restrictions(manifest):
        raise ValueError('Harvest cannot erase the original source-origin restriction')
    if event['degree'] not in ('Critical Success','Success','Failure','Critical Failure'):
        raise ValueError('Use the resolved governing harvesting degree')
    categories=set(choice['categories']);authorized=set(recovery['authorizedUnitIds'])
    ordinary=manifest['baseline']+[u for u in manifest['extraReserve'] if u['id'] in authorized]
    all_ordinary=manifest['baseline']+manifest['extraReserve']+manifest['damagedBaseline']
    if not categories<=set(u['category'] for u in all_ordinary):raise ValueError('Unknown category cannot be selected')
    selected=[u['id'] for u in ordinary if u['category'] in categories and u['state']=='available']
    permitted=not recovery['originRestrictions'] and not material_origin_restrictions(manifest) and material_access_permitted(manifest)
    if event['degree'] not in ('Critical Success','Success') or not permitted:selected=[]
    damaged=event.get('damagedBaselineUnitId')
    if damaged is not None:
        candidates={u['id'] for u in manifest['damagedBaseline'] if u['category'] in categories and u['state']=='available'}
        if event['degree']!='Critical Success' or damaged not in candidates or not permitted:
            raise ValueError('Critical recovery needs its separate eligible damaged baseline unit')
        selected.append(damaged)
    if len(selected)!=len(set(selected)):raise ValueError('Duplicate extracted anatomy unit')
    lifecycle=world.applicable_record(prerequisite.get('lifecycleEvidenceId'),'material-lifecycle',cp)
    actual_time=prerequisite['deathOrRemovalTime']
    if (lifecycle['physicalId']!=donor or lifecycle['deathOrRemovalTime']!=actual_time or
            not isinstance(actual_time,(int,float)) or actual_time>cp[0] or actual_time>lifecycle['checkpoint'][0] or
            not lifecycle['governingProcedure'] or lifecycle['eventKind'] not in ('death','removal','documented-clock-correction') or
            not set(selected)<=set(lifecycle['unitIds']) or
            (lifecycle['eventKind']=='death' and actual_time<capture['checkpoint'][0] and capture['lifeState']=='alive')):
        raise ValueError('Extraction requires the actual donor/unit lifecycle and an existing death or removal time')
    all_by_id={u['id']:u for g in MATERIAL_GROUPS for u in manifest[g]}
    previous_clocks={}
    for ident in selected:
        previous=all_by_id[ident].get('deathOrRemovalTime')
        if previous is not None and previous!=actual_time:
            if lifecycle['eventKind']!='documented-clock-correction' or lifecycle['priorDeathOrRemovalTime']!=previous:
                raise ValueError('Extraction cannot replace an established death/removal timestamp')
            previous_clocks[ident]=previous
    out=deepcopy(history)
    out[donor]={'resolvedDegree':event['degree'],'authorizedExtractedUnitIds':selected,
        'forfeitedUnselectedOrdinaryUnitIds':[u['id'] for u in all_ordinary if u['category'] not in categories],
        'uniqueDropsAuthorized':[],'inventoryCreated':[],'deathOrRemovalTime':actual_time,
        'authorizedExtractedMassLbByUnitId':{i:all_by_id[i]['massLb'] for i in selected},
        'priorCorrectedClocksByUnitId':previous_clocks,'lifecycleEvidenceId':lifecycle['id'],
        'foodServingCredit':0,'completeSupplyUnits':0,'evidenceId':evidence_id}
    return out


def active_work_seconds(record, start, end, required_hands=2):
    """Check recorded nonoverlapping work intervals, not actual human behavior."""
    spans=sorted(record['intervals'],key=lambda z:z['startSeconds'])
    total=0;last=start
    for span in spans:
        a,b=span['startSeconds'],span['endSeconds']
        if a<last or b<a or b>end or span['hands']<required_hands or span['actions']*6<b-a:
            raise ValueError('Work overlaps, exceeds the window, or lacks recorded hands/Actions')
        total+=b-a;last=b
    return total


def physical_admission(world, admission_id, method, checkpoint, assembly, *, creature_id=None, manifest_id=None):
    """Check fixed limits on an externally adjudicated apparatus/prey record.

    Shape, support, access, containment and behavior still need that record's
    cited adjudication. Numerical fit alone does not establish admission.
    """
    a=world.record(admission_id,'physical-admission',checkpoint)
    if method not in METHODS:raise ValueError('Rig is not a capture method')
    if a['method']!=method or a['disposition']!='admitted':raise ValueError('Method not physically admitted')
    if a['attemptId']!=assembly['attemptId'] or a['assemblyEvidenceId']!=assembly['id'] or assembly['method']!=method:
        raise ValueError('Physical admission must bind this attempt, method and current assembly')
    if creature_id is not None and a['physicalId']!=creature_id:
        raise ValueError('Physical admission belongs to another selected creature')
    profile=world.applicable_record(a['preyProfileEvidenceId'],'ordinary-prey-profile',checkpoint)
    if (profile['physicalId']!=a['physicalId'] or F(str(profile['bodyMassLb']))!=F(str(a['preyMassLb'])) or
            F(str(profile['bodyVolumeCubicFeet']))!=F(str(a['preyVolumeCubicFeet'])) or
            not profile['geometry'] or profile['geometry']!=a['preyGeometry']):
        raise ValueError('Admission mass and geometry must come from the same actual creature profile')
    if manifest_id is not None:
        manifest=world.applicable_record(manifest_id,'material-manifest',checkpoint)
        if manifest['physicalId']!=a['physicalId'] or F(str(manifest['bodyMassLb']))!=F(str(profile['bodyMassLb'])):
            raise ValueError('Anatomical mass differs from the admitted physical creature')
    required={'Rod':{'Rod','Line','Hook'},'Net':{'Net'},'Trap':{'Trap'}}[method]
    families=assembly['itemFamilyById']
    if not required<=set(families.values()):raise ValueError('Missing indispensable apparatus family')
    indispensable={ident for ident,family in families.items() if family in required}
    if not a['apparatusStateIds']:raise ValueError('Actual capture apparatus history required')
    physical_ids=[]
    for key in a['apparatusStateIds']:
        body=world.record(key,'item-state',checkpoint)
        physical_ids.append(body['physicalId'])
        if (body['currentHP']<=0 or not body['complete'] or body['melded'] or
                body['participatingAttemptId']!=assembly['attemptId']):
            raise ValueError('Indispensable capture apparatus is Broken, incomplete or melded')
    if len(set(physical_ids))!=len(physical_ids) or set(physical_ids)!=indispensable:
        raise ValueError('Every indispensable registered body requires exactly one current physical state')
    if a['preyMassLb']>10 or a['preyMassLb']<0 or a['preyMassLb']>a['handlingLimitLb']:
        raise ValueError('Catch exceeds admitted mass/handling limit')
    if any(a[k]<0 for k in ('wholeLinePathFeet','reachFeet','preyVolumeCubicFeet','recoveryPathFeet')):
        raise ValueError('Physical path and volume cannot be negative')
    if method=='Rod' and a['wholeLinePathFeet']>50:raise ValueError('Line path too long')
    if method=='Net' and (a['reachFeet']>6 or a['preyVolumeCubicFeet']>.5):raise ValueError('Net reach/volume exceeded')
    if method=='Trap' and (a['recoveryPathFeet']>20 or a['preyVolumeCubicFeet']>1):raise ValueError('Trap path/volume exceeded')
    if method not in METHODS:raise ValueError('Rig is not a capture method')
    return a


class FishingLedger:
    """Bounded journal over cited, externally adjudicated campaign records.

    Enforces source item amounts, fixed attempt timing, unique opportunities,
    atomic reservations, historical event order and first-capture recovery.
    It does not authenticate the Director/world records, resolve Core dice,
    simulate bodies, grant inventory, run harvesting or implement the companion.
    """
    def __init__(self, cards):
        self.cards=deepcopy(cards)
        self.state={'version':0,'checkpoint':(-1,0,0),'seen':[], 'opportunities':[],
            'attempts':{},'creatureReservations':{},'equipmentReservations':{},
            'baitUses':[],'recoveries':{},'due':{},'poolRoutes':{},'rollAttempts':{},
            'reservationHistory':{},'preExposureCancellations':{},'baitDebits':{},'ordinaryBaitUses':{},'chumUses':{},'chumUseIds':{},
            'stockRoutes':[],'stockVersions':{},'creatureAttempts':{},'availabilityUses':{},'renewalCauseUses':{},
            'opportunityHistory':[],'materialStates':{}}

    @staticmethod
    def _stock_route(state, world, record, route, checkpoint):
        binding=bound_stock_allocation(world,record,checkpoint)
        manifest=binding['manifest'];key=(manifest['sharedStockId'],manifest['version'])
        version={'siteId':manifest['siteId'],'members':sorted(manifest['memberPhysicalIds'])}
        if key in state['stockVersions'] and state['stockVersions'][key]!=version:
            raise ValueError('A stock version cannot be rewritten under another evidence ID')
        state['stockVersions'][key]=version
        for previous in state['stockRoutes']:
            if (previous['watchId']==record['watchId'] and previous['route']!=route and
                    set(previous['physicalIds']) & set(binding['physicalIds'])):
                raise ValueError('Fishing and Forage cannot use overlapping actual stock during the same Watch')
        state['stockRoutes'].append({'route':route,'watchId':record['watchId'],
            'physicalIds':binding['physicalIds'],'binding':deepcopy(binding),'recordId':record['id']})
        return binding

    @staticmethod
    def _stock_availability(state, world, opportunity, binding, creature, checkpoint, attempt_id):
        availability=world.record(opportunity.get('availabilityEvidenceId'),'stock-availability',checkpoint)
        if (availability['opportunityId']!=opportunity['opportunityId'] or
                availability['stockManifestEvidenceId']!=binding['manifest']['id'] or
                availability['candidateCreatureIds']!=opportunity['candidateCreatureIds'] or
                availability['id'] in state['availabilityUses']):
            raise ValueError('An opportunity requires its own actual stock-availability relationship')
        prior_id=state['creatureAttempts'].get(creature) if creature else None
        if not creature:
            previous=[r for r in state['opportunityHistory'] if r['selectedCreatureId'] is None and
                r['sharedStockId']==opportunity['sharedStockId'] and r['physicalIds']==binding['physicalIds']]
            if previous:prior_id=previous[-1]['attemptId']
        cause=availability['cause']
        if cause=='initial-recorded-stock':
            if prior_id:raise ValueError('A new hour, Watch, name or record does not renew an already used opportunity')
        else:
            renewal=world.applicable_record(availability.get('causeEvidenceId'),'stock-reavailability',checkpoint)
            when=tuple(renewal['occurredAt'])
            if cause in ('release','escape') and not prior_id:
                raise ValueError('A claimed release or escape must reference its actual preceding captured deployment')
            if (cause not in ('release','escape','arrival','newly-accessible-stock','materially-new-approach') or
                    renewal['cause']!=cause or renewal['opportunityId']!=opportunity['opportunityId'] or
                    renewal['stockManifestEvidenceId']!=binding['manifest']['id'] or
                    renewal['physicalId']!=creature or renewal['previousAttemptId']!=prior_id or
                    not renewal['governingCause'] or when>tuple(checkpoint) or when>tuple(renewal['checkpoint']) or
                    renewal['id'] in state['renewalCauseUses']):
                raise ValueError('Renewal needs its actual cause, time, same creature and preceding attempt')
            if prior_id:
                previous=state['attempts'][prior_id]
                if when<=previous['committedAt']:
                    raise ValueError('A prior event cannot justify a later fresh opportunity')
                capture_id=previous.get('captureEvidenceId')
                if capture_id:
                    capture=world.record(capture_id,'secure-capture')
                    custody=world.applicable_record(renewal.get('custodyEvidenceId'),'creature-custody-transition',when)
                    if (custody['physicalId']!=creature or custody['previousAttemptId']!=prior_id or
                            custody['captureEvidenceId']!=capture_id or
                            custody['fromCustody'] not in ('held','contained','transferred') or
                            custody['toCustody'] not in ('released','escaped') or not custody['locationId'] or
                            not isinstance(custody['elevationFeet'],(int,float)) or
                            tuple(custody['checkpoint'])<tuple(capture['checkpoint']) or
                            (cause in ('release','escape') and custody['toCustody']!=('released' if cause=='release' else 'escaped'))):
                        raise ValueError('Recapture requires the actual intervening release or escape from prior custody')
                elif cause in ('release','escape'):
                    raise ValueError('A never-captured response has no captured custody to release')
            state['renewalCauseUses'][renewal['id']]=attempt_id
        state['availabilityUses'][availability['id']]=attempt_id
        state['opportunityHistory'].append({'attemptId':attempt_id,'sharedStockId':opportunity['sharedStockId'],
            'physicalIds':binding['physicalIds'],'selectedCreatureId':creature,'availabilityEvidenceId':availability['id']})
        if creature:state['creatureAttempts'][creature]=attempt_id

    def _reservation(self, world, event, state, checkpoint):
        receipt=world.record(event['reservationEvidenceId'],'fishing-reservation')
        disposition=world.record(event['reservationDispositionEvidenceId'],'fishing-reservation-disposition',checkpoint)
        if (receipt['attemptId']!=event['attemptId'] or receipt['lead']!=event['lead'] or
                tuple(receipt['checkpoint'])>tuple(checkpoint) or receipt['id'] in state['reservationHistory'] or
                receipt['attemptId'] in state['preExposureCancellations']):
            raise ValueError('Actual unused pre-setup reservation receipt required')
        if (disposition['reservationEvidenceId']!=receipt['id'] or
                disposition['attemptId']!=receipt['attemptId'] or disposition['lead']!=receipt['lead']):
            raise ValueError('Reservation disposition belongs to another receipt, attempt or lead')
        resources=receipt['reservedResourceIds']
        if len(set(resources))!=len(resources) or not set(receipt['equipmentIds'])<=set(resources):
            raise ValueError('Reservation must identify every physical resource once')
        rig_ids={i for i,rid in receipt['itemRecipeIds'].items() if rid and self.cards[rid]['sourceRecipe']['recipeFamily']=='Rig'}
        mounts=receipt.get('rigMountWorkByPhysicalId',{})
        if set(mounts)!=rig_ids:raise ValueError('Every Rig requires its separate prior mounting record')
        for ident,key in mounts.items():
            mount=world.record(key,'work-record')
            if (tuple(mount['checkpoint'])>tuple(receipt['checkpoint']) or mount['attemptId']!=receipt['attemptId'] or
                    mount['physicalId']!=ident or mount['phase']!='rig-mount' or not mount['worker'] or
                    active_work_seconds(mount,mount['startedAtSeconds'],receipt['checkpoint'][0])!=300):
                raise ValueError('Rig mounting needs five separate actual minutes before main setup')
        return receipt,disposition

    def _setup_and_fishing(self, world, result, attempt, checkpoint):
        start=attempt['startedAt'][0];setup_end=start+300
        setup=world.record(result['setupWorkEvidenceId'],'work-record',checkpoint)
        if (setup['attemptId']!=attempt['id'] or setup['worker']!=attempt['lead'] or setup['phase']!='setup' or
                active_work_seconds(setup,start,setup_end)!=300):
            raise ValueError('Five actual setup minutes must finish before the fifty-minute fishing phase')
        if attempt['method']=='Trap':
            soak=world.record(result['soakEvidenceId'],'trap-soak',checkpoint)
            if (soak['attemptId']!=attempt['id'] or soak['reservationEvidenceId']!=attempt['reservationEvidenceId'] or
                    soak['setupWorkEvidenceId']!=setup['id'] or soak['startSeconds']!=setup_end or
                    soak['endSeconds']!=checkpoint[0] or soak['endSeconds']-soak['startSeconds']!=3000 or
                    soak['disposition']!='continuously-deployed'):
                raise ValueError('Trap requires its actual fifty-minute deployed soak after setup')
        else:
            work=world.record(result['workEvidenceId'],'work-record',checkpoint)
            if (work['attemptId']!=attempt['id'] or work['worker']!=attempt['lead'] or work['phase']!='fishing' or
                    active_work_seconds(work,setup_end,checkpoint[0])!=3000):
                raise ValueError('Lead must complete the actual fifty-minute attended fishing phase')
        return setup

    @staticmethod
    def _schedule(s, key, aid, kind, at, now, exact_time):
        at=tuple(at)
        if len(at)!=3 or at[0]!=exact_time or at<=now or key in s['due']:
            raise ValueError('Wrong scheduled time or duplicate event')
        if any(tuple(z['at'])==at for z in s['due'].values()):
            raise ValueError('Authoritative phase/sequence must order simultaneous events')
        s['due'][key]={'at':at,'attemptId':aid,'kind':kind}

    def _effects(self, world, evidence_id, a, cp):
        e=world.record(evidence_id,'catch-roll',cp)
        assembly=world.record(e['assemblyEvidenceId'],'assembly',cp)
        if assembly['attemptId']!=a['id'] or assembly['lead']!=a['lead'] or assembly['method']!=a['method']:
            raise ValueError('Wrong attempt/lead/method in equipment view')
        if assembly['assemblyId']!=a['assemblyId']:raise ValueError('Cannot transfer receipt to a different physical assembly')
        if (set(assembly['participatingItemIds'])!=set(a['gear']) or assembly['itemRecipeIds']!=a['itemRecipeIds'] or
                assembly['itemFamilyById']!=a['itemFamilyById']):
            raise ValueError('Deployment candidates cannot be replaced after commitment')
        if e['roll']!=a['canonicalRoll']:raise ValueError('Changed canonical current roll')
        receipt_id=assembly.get('baitExposureEvidenceId')
        if a['baitId'] is None:
            if receipt_id:raise ValueError('Null baitId cannot receive a finished-Bait receipt or contribution')
        elif not a.get('baitDebit') or a['baitDebit']['exposureEvidenceId']!=receipt_id:
            raise ValueError('Assembly receipt is not this journal attempt\'s actual bait debit')
        else:
            exposure,use=bait_receipt(world,receipt_id,assembly);debit=a['baitDebit']
            if (any(exposure[k]!=debit[k] for k in ('physicalId','recipeId','attemptId','assemblyId')) or
                    tuple(exposure['checkpoint'])!=debit['exposedAt'] or tuple(exposure['expiresAt'])!=debit['expiresAt'] or
                    exposure['inventoryUseEvidenceId']!=debit['inventoryUseEvidenceId'] or
                    use['unusedBaitEvidenceId']!=debit['unusedBaitEvidenceId']):
                raise ValueError('Later world evidence cannot rewrite the recorded bait expenditure or clocks')
        admission=world.record(assembly['admissionEvidenceId'],'physical-admission',cp)
        physical={world.record(key,'item-state',cp)['physicalId']:key for key in admission['apparatusStateIds']}
        for view in e['items']:
            if view['physicalId'] in physical and view['stateEvidenceId']!=physical[view['physicalId']]:
                raise ValueError('Physical admission and magic view cannot use contradictory histories for one body')
        out=effect_candidates(world,evidence_id,self.cards)
        if a.get('rigBinding'):
            binding=rig_deployment(world,assembly)
            if binding!=a['rigBinding']:raise ValueError('Initial Rig load, mounting and dispersal cannot be rewritten after expenditure')
            current=world.record(assembly['rigStateEvidenceId'],'rig-operational-state',cp)
            ident=binding['deployment']['dispenserPhysicalId'];handling=a['rigHandling']
            if handling['state'] in ('retrieved','abandoned','spilled') and ident in out['eligibleIds']:
                raise ValueError('A reconciled or spilled Rig cannot regain benefits from spent chum')
            if handling['state']=='deployed':
                handling['locationId']=current['locationId'];handling['lastOperationalStateEvidenceId']=current['id']
                if current['disposition']=='spilled':handling['state']='spilled'
        # The receipt is an assembly effect; a caller cannot reactivate a spent
        # or expired dose by presenting a copied pre-expiry item snapshot.
        if a['baitId'] and not a['receiptActive']:
            out['extraByPhysicalId'].pop(a['baitId'],None)
            out['affinityByPhysicalId'].pop(a['baitId'],None)
            out['eligibleIds']=[x for x in out['eligibleIds'] if x!=a['baitId']]
            out['extra']=max(out['extraByPhysicalId'].values(),default=0)
            out['bonus']=max((self.cards[a['itemRecipeIds'][x]]['sourceRecipe']['mechanics']['fishingBonus'] for x in out['eligibleIds']),default=0)
        return out

    def _register_rig(self, state, attempt, world, assembly, checkpoint, reservation):
        bound=rig_deployment(world,assembly)
        attempt['rigBinding']=deepcopy(bound)
        if bound is None:return
        deployment,load,use=bound['deployment'],bound['load'],bound['use']
        if tuple(deployment['checkpoint'])!=tuple(checkpoint) or deployment['reservationEvidenceId']!=reservation['id']:
            raise ValueError('Rig opening belongs to this deployment commitment and reservation')
        current=world.record(assembly.get('rigStateEvidenceId'),'rig-operational-state',checkpoint)
        body=world.record(current['itemStateEvidenceId'],'item-state',checkpoint)
        if (current['disposition']!='deployed' or body['physicalId']!=deployment['dispenserPhysicalId'] or
                body['currentHP']<=0 or not body['complete'] or body['melded'] or body['participatingAttemptId']!=attempt['id']):
            raise ValueError('First Rig deployment requires a physically functional registered dispenser')
        if use['id'] in state['chumUseIds']:raise ValueError('Rig allotment dispersal already committed')
        for ident in bound['ordinaryPortionIds']:
            if (ident not in reservation['reservedResourceIds'] or ident in attempt['gear'] or
                    ident in state['chumUses'] or ident in state['ordinaryBaitUses'] or ident in state['baitUses']):
                raise ValueError('Chum must be actual reserved material not already used at another physical location')
        if load['finishedBaitPhysicalId'] is not None and (load['finishedBaitPhysicalId']!=attempt['baitId'] or
                not attempt.get('baitDebit') or attempt['baitDebit']['exposureEvidenceId']!=load['finishedBaitExposureEvidenceId']):
            raise ValueError('Rig substitution must be this attempt\'s one actual Bait debit')
        for ident in bound['ordinaryPortionIds']:
            state['chumUses'][ident]={'attemptId':attempt['id'],'chumUseEvidenceId':use['id']}
        state['chumUseIds'][use['id']]=attempt['id']
        attempt['rigHandling']={'state':'deployed','physicalId':deployment['dispenserPhysicalId'],
            'locationId':deployment['dispenserPointId'],'allotmentSpent':True,'inventoryCreated':[]}

    @staticmethod
    def _separate_work(world, work, other_ids):
        for key in other_ids:
            other=world.record(key,'work-record')
            if other['worker']!=work['worker']:continue
            for a in work['intervals']:
                for b in other['intervals']:
                    if max(a['startSeconds'],b['startSeconds'])<min(a['endSeconds'],b['endSeconds']):
                        raise ValueError('Additional handling work cannot reuse this worker\'s other active minutes')

    def _reconcile_rig(self, state, attempt, world, evidence_id, checkpoint):
        if not attempt.get('rigBinding') or attempt['rigHandling']['state'] in ('retrieved','abandoned'):
            raise ValueError('No unresolved Rig handling obligation')
        disposition=world.record(evidence_id,'rig-disposition',checkpoint)
        ident=attempt['rigHandling']['physicalId']
        if (disposition['attemptId']!=attempt['id'] or disposition['dispenserPhysicalId']!=ident or
                not disposition['locationId'] or not isinstance(disposition['elevationFeet'],(int,float))):
            raise ValueError('Actual Rig identity and receiving/disposition location required')
        reason=disposition['reason']
        if reason=='retrieved':
            work=world.record(disposition['workEvidenceId'],'work-record',checkpoint)
            admission=world.record(disposition['handlingEvidenceId'],'rig-handling-admission',checkpoint)
            if (not work['worker'] or work['attemptId']!=attempt['id'] or work['physicalId']!=ident or work['phase']!='rig-retrieval' or
                    active_work_seconds(work,attempt['committedAt'][0],checkpoint[0])<300 or
                    admission['worker']!=work['worker'] or admission['attemptId']!=attempt['id'] or
                    admission['dispenserPhysicalId']!=ident or admission['disposition']!='admitted' or
                    admission['pathDisposition']!='admitted' or admission['handledMassLb']<=0 or
                    admission['handledMassLb']>admission['handlingCapacityLb'] or
                    admission['receivingLocationId']!=disposition['locationId']):
                raise ValueError('Rig retrieval needs its own five actual minutes, hands, access and receiving capacity')
            self._separate_work(world,work,attempt.get('workEvidenceIds',[]))
            attempt.setdefault('workEvidenceIds',[]).append(work['id'])
            attempt['rigRetrievalWorkEvidenceId']=work['id']
        elif reason=='abandoned':
            if disposition['locationId']!=attempt['rigHandling']['locationId']:
                raise ValueError('Abandonment cannot move the Rig from its actual recorded location')
        else:raise ValueError('Rig requires actual retrieval or explicit abandonment')
        attempt['rigHandling'].update({'state':reason,'locationId':disposition['locationId'],
            'elevationFeet':disposition['elevationFeet'],'dispositionEvidenceId':disposition['id'],
            'inventoryCreated':[],'allotmentSpent':True})
        state['equipmentReservations'].pop(ident,None)

    @staticmethod
    def _allowance_occupied(state, actor, except_attempt=None):
        return any(a['id']!=except_attempt and a['responsibleActor']==actor and
            not a['deploymentReconciled'] for a in state['attempts'].values())

    @staticmethod
    def _trap_configuration(world, attempt, checkpoint, evidence_id=None):
        key=attempt['setterConfigurationEvidenceId']
        if evidence_id is not None and evidence_id!=key:
            raise ValueError('Handover cannot substitute another setter configuration')
        config=world.applicable_record(key,'trap-configuration',checkpoint)
        credential=world.record(config['credentialEvidenceId'],'fishing-credential',config['checkpoint'])
        if (config['attemptId']!=attempt['id'] or config['setter']!=attempt['lead'] or
                tuple(config['checkpoint'])!=attempt['setupCompletedAt'] or credential['actor']!=attempt['lead']):
            raise ValueError('Trap retains its actual original setup configuration and credential')
        binding={'configuration':config,'credential':credential}
        if attempt.get('setterBinding') is not None and attempt['setterBinding']!=binding:
            raise ValueError('Original setter configuration cannot be rewritten after handover')
        attempt['setterBinding']=deepcopy(binding)
        return config

    def _close_trap(self, state, attempt, world, disposition, checkpoint):
        """A claim, responsibility, apparatus and catch are separate records.

        Resolved world records establish actual handling; this is neither a
        custody simulator nor a grant of carried equipment or inventory.
        """
        if attempt['deploymentReconciled']:
            raise ValueError('Trap deployment was already physically reconciled or abandoned')
        reason=disposition['reason'];aid=attempt['id'];ident=attempt['trapHandling']['physicalId']
        location=world.record(disposition.get('trapStateEvidenceId'),'trap-disposition-state',checkpoint)
        captured=attempt.get('captureEvidenceId')
        if (location['attemptId']!=aid or location['trapPhysicalId']!=ident or
                not location['apparatusLocationId'] or not isinstance(location['apparatusElevationFeet'],(int,float)) or
                location['captureEvidenceId']!=captured or
                location['catchPhysicalId']!=(attempt['selectedCreatureId'] if captured else None)):
            raise ValueError('Actual Trap and existing catch identities and locations must remain recorded')
        if captured:
            if (not location['catchLocationId'] or not isinstance(location['catchElevationFeet'],(int,float)) or
                    location['lifeState'] not in ('alive','dead') or
                    location['custody'] not in ('contained','held','released','escaped','transferred')):
                raise ValueError('Existing captured animal keeps actual life, custody and placement')
        elif any(location.get(k) is not None for k in ('catchLocationId','catchElevationFeet','lifeState','custody')):
            raise ValueError('Retrieving an empty Trap cannot materialize its selected prey as a catch')

        if reason=='lawful-handover':
            handover=world.record(disposition.get('handoverEvidenceId'),'trap-handover',checkpoint)
            receiver=handover['toActor']
            if (not receiver or receiver==attempt['responsibleActor'] or handover['fromActor']!=attempt['responsibleActor'] or
                    handover['attemptId']!=aid or handover['trapPhysicalId']!=ident or
                    handover['opportunityId']!=attempt['opportunityId'] or
                    handover['selectedCreatureId']!=attempt['selectedCreatureId'] or
                    handover['canonicalRollId']!=attempt['canonicalRoll']['id'] or
                    handover['disposition']!='lawful-accepted' or handover['trapStateEvidenceId']!=location['id'] or
                    self._allowance_occupied(state,receiver,aid)):
                raise ValueError('Lawful handover retains the same deployment and requires a free receiving allowance')
            self._trap_configuration(world,attempt,checkpoint,handover['setterConfigurationEvidenceId'])
            if location['apparatusDisposition']!='deployed':raise ValueError('Handover is not automatic retrieval')
            attempt.setdefault('handovers',[]).append(deepcopy(handover))
            attempt['responsibleActor']=receiver
            attempt['trapHandling'].update({'state':'deployed','locationId':location['apparatusLocationId'],
                'elevationFeet':location['apparatusElevationFeet'],'latestStateEvidenceId':location['id'],'inventoryCreated':[]})
            attempt['latestTrapDisposition']=deepcopy(disposition)
            # Deliberately retain claim state, receipt, reservations and due events.
            return

        if reason=='retrieved':
            work=world.record(disposition.get('retrievalWorkEvidenceId'),'work-record',checkpoint)
            admission=world.record(disposition.get('handlingEvidenceId'),'trap-handling-admission',checkpoint)
            load=world.record(admission['loadEvidenceId'],'trap-handling-load',checkpoint)
            earliest=world.record(captured,'secure-capture')['checkpoint'][0] if captured else attempt['setupCompletedAt'][0]
            if (not work['worker'] or work['attemptId']!=aid or work['physicalId']!=ident or work['phase']!='trap-retrieval' or
                    active_work_seconds(work,earliest,checkpoint[0])<300 or
                    admission['attemptId']!=aid or admission['trapPhysicalId']!=ident or admission['worker']!=work['worker'] or
                    admission['disposition']!='admitted' or admission['pathDisposition']!='admitted' or
                    not 0<=admission['recoveryPathFeet']<=20 or admission['trapStateEvidenceId']!=location['id'] or
                    load['attemptId']!=aid or load['trapPhysicalId']!=ident or load['trapStateEvidenceId']!=location['id'] or
                    load['catchPhysicalId']!=location['catchPhysicalId'] or load['apparatusMassLb']<4 or
                    load['otherContentsMassLb']<0 or load['catchMassLb']<0):
                raise ValueError('Trap retrieval requires its capable worker, five active minutes, hands, path and actual load')
            if captured and load['catchTransported'] is True:
                prey=world.applicable_record(load['catchProfileEvidenceId'],'ordinary-prey-profile',checkpoint)
                if prey['physicalId']!=location['catchPhysicalId'] or prey['bodyMassLb']!=load['catchMassLb']:
                    raise ValueError('Handling must account for the existing actual catch mass')
                if location['custody'] in ('released','escaped'):
                    raise ValueError('Released or escaped prey is not a transported catch')
            elif (load['catchTransported'] is not False or load['catchMassLb']!=0 or
                    (captured and location['custody'] not in ('released','escaped'))):
                raise ValueError('Only an actual empty Trap or separately released/escaped catch has zero catch load')
            total=sum(F(str(load[k])) for k in ('apparatusMassLb','otherContentsMassLb','catchMassLb'))
            if (F(str(admission['handledMassLb']))!=total or total>F(str(admission['handlingCapacityLb'])) or
                    location['apparatusDisposition']!='retrieved'):
                raise ValueError('Actual total Trap load must fit the retriever and receiving placement')
            self._separate_work(world,work,attempt['workEvidenceIds'])
            attempt['workEvidenceIds'].append(work['id'])
            attempt['trapRetrievalWorkEvidenceId']=work['id']
        elif reason=='abandoned':
            if location['apparatusDisposition']!='abandoned':raise ValueError('Express Trap abandonment requires its actual placement')
        elif reason in ('failed','empty','escaped','finished'):
            if (attempt['state'] in ('committed','closed') or location['apparatusDisposition']!='deployed' or
                    (reason in ('failed','empty') and attempt['state']!='no-catch') or
                    (reason in ('finished','escaped') and not captured)):
                raise ValueError('Claim closure cannot cancel a pending check or pretend to retrieve a Trap')
            if reason=='escaped' and location['custody']!='escaped':raise ValueError('Escape needs actual creature disposition')
        else:raise ValueError('Trap requires an actual claim or deployment disposition')

        attempt['disposition']=deepcopy(disposition);attempt['state']='closed';attempt['receiptActive']=False
        reconciled=reason in ('retrieved','abandoned')
        attempt['deploymentReconciled']=reconciled
        attempt['trapHandling'].update({'state':reason if reconciled else 'deployed',
            'locationId':location['apparatusLocationId'],'elevationFeet':location['apparatusElevationFeet'],
            'latestStateEvidenceId':location['id'],'inventoryCreated':[]})
        attempt['creatureDisposition']=deepcopy(location) if captured else None
        for key in list(state['due']):
            if state['due'][key]['attemptId']==aid:del state['due'][key]
        if reconciled:
            for g in attempt['gear']:
                if attempt.get('rigHandling') and g==attempt['rigHandling']['physicalId'] and attempt['rigHandling']['state'] not in ('retrieved','abandoned'):continue
                state['equipmentReservations'].pop(g,None)
        if attempt['selectedCreatureId'] and (reconciled or not captured or reason=='escaped'):
            state['creatureReservations'].pop(attempt['selectedCreatureId'],None)

    def _presentation(self, world, assembly, cp, required):
        presentation=world.record(assembly['presentationEvidenceId'],'bait-presentation',cp)
        sources=presentation['sources'];forms=[s['form'] for s in sources];ids=[s['physicalId'] for s in sources]
        if (presentation['attemptId']!=assembly['attemptId'] or presentation['assemblyId']!=assembly['assemblyId'] or
                len(set(ids))!=len(ids) or presentation['forms']!=forms or presentation['sourcePhysicalIds']!=ids or
                presentation['ordinaryBaitLotIds']!=[s['physicalId'] for s in sources if s['form']=='ordinary-bait']):
            raise ValueError('Presentation forms must name their actual distinct physical sources')
        allowed={'ordinary-bait','finished-Bait','Lure'} if assembly['method']!='Trap' else {'ordinary-bait','finished-Bait'}
        if required and not allowed.intersection(forms):raise ValueError('Method requires actual compatible bait or admitted Lure')
        main_location={'Rod':'rod-presentation','Net':'net-clip','Trap':'trap-holder'}[assembly['method']]
        ordinary=[]
        for source in sources:
            ident=source['physicalId'];form=source['form']
            if form=='ordinary-bait':
                use=world.record(source['useEvidenceId'],'ordinary-bait-use',cp)
                stock=world.record(use['inventoryEvidenceId'],'ordinary-bait-inventory',cp)
                if (stock['physicalId']!=ident or stock['stockClass']!='ordinary-angling-bait' or
                        stock['state']!='available-unspent' or stock['materialCondition']!='eligible' or
                        F(str(stock['massLb']))!=F(1,10) or use['purpose']!='angling-presentation' or
                        use['disposition']!='committed-exposure' or use['compatibility']!='compatible'):
                    raise ValueError('Ordinary bait requires an actual eligible portion and inventory use, not a process ingredient')
                ordinary.append(use)
            elif form=='finished-Bait':
                if source['useEvidenceId']!=assembly.get('baitExposureEvidenceId'):
                    raise ValueError('Finished bait presentation must use this assembly\'s actual exposure')
                use,_=bait_receipt(world,source['useEvidenceId'],assembly)
                if tuple(use['checkpoint'])!=tuple(cp):raise ValueError('Presentation must bind first actual exposure')
            elif form=='Lure':
                if assembly['itemFamilyById'].get(ident)!='Lure':raise ValueError('A non-Lure body cannot supply a Lure presentation')
                use=world.record(source['useEvidenceId'],'lure-presentation',cp)
                state=world.record(use['stateEvidenceId'],'item-state',cp)
                if (state['physicalId']!=ident or state['participatingAttemptId']!=assembly['attemptId'] or
                        state['currentHP']<=0 or not state['complete'] or state['melded']):
                    raise ValueError('Actual complete attached Lure body is required')
            else:raise ValueError('Unknown physical bait presentation form')
            if (use['physicalId']!=ident or use['attemptId']!=assembly['attemptId'] or
                    use['assemblyId']!=assembly['assemblyId'] or use['locationId']!=presentation['responsePointId'] or
                    use['locationKind']!=main_location):
                raise ValueError('Bait or Lure must occupy the actual method presentation point')
        return ordinary

    def _assembly(self, world, assembly, cp, attraction=False):
        admission=physical_admission(world,assembly['admissionEvidenceId'],assembly['method'],cp,assembly)
        families=assembly['itemFamilyById']
        if set(families)!=set(assembly['participatingItemIds']):raise ValueError('Actual physical families required')
        for ident,rid in assembly['itemRecipeIds'].items():
            if rid is not None and self.cards[rid]['sourceRecipe']['recipeFamily']!=families[ident]:
                raise ValueError('Physical family does not match actual recipe')
        required={'Rod':{'Rod','Line','Hook'},'Net':{'Net'},'Trap':{'Trap'}}[assembly['method']]
        if not required<=set(families.values()):raise ValueError('Missing required capture assembly component')
        state_ids={world.record(key,'item-state',cp)['physicalId'] for key in admission['apparatusStateIds']}
        if not {i for i,f in families.items() if f in required}<=state_ids:
            raise ValueError('Admission omits indispensable capture body history')
        return self._presentation(world,assembly,cp,assembly['method'] in ('Rod','Trap') or attraction)

    def _physical_checkpoint(self, world, admission_id, equipment_id, attempt, cp, manifest_id):
        view=world.record(equipment_id,'catch-roll',cp)
        assembly=world.record(view['assemblyEvidenceId'],'assembly',cp)
        if (assembly['attemptId']!=attempt['id'] or assembly['lead']!=attempt['lead'] or
                set(assembly['participatingItemIds'])!=set(attempt['gear']) or
                assembly['itemRecipeIds']!=attempt['itemRecipeIds'] or
                assembly['itemFamilyById']!=attempt['itemFamilyById'] or
                assembly['admissionEvidenceId']!=admission_id):
            raise ValueError('Physical checkpoint cannot substitute another admission or registered apparatus')
        return physical_admission(world,admission_id,attempt['method'],cp,assembly,
            creature_id=attempt['selectedCreatureId'],manifest_id=manifest_id)

    def apply(self, world, evidence_id, expected_version):
        e=world.record(evidence_id,'fishing-transition');cp=tuple(e['checkpoint']);s=deepcopy(self.state)
        if expected_version!=s['version'] or cp<=tuple(s['checkpoint']) or e['id'] in s['seen']:
            raise ValueError('Stale, replayed, or out-of-order transaction')
        if 'schedule' in e or 'cancelDue' in e:
            raise ValueError('Generic scheduling/cancellation cannot bypass attempt events')
        op=e['operation'];aid=e.get('attemptId');due=e.get('dueId');due_record=None
        if s['due']:
            first=min(s['due'],key=lambda k:tuple(s['due'][k]['at']))
            if tuple(s['due'][first]['at'])<=cp:
                if due!=first or tuple(s['due'][first]['at'])!=cp:
                    raise ValueError('Resolve the actual historical due event first')
        if due is not None:
            due_record=s['due'].get(due)
            if not due_record or tuple(due_record['at'])!=cp or due_record['attemptId']!=aid:
                raise ValueError('No matching due event for this attempt')
            allowed={'check':{'check','no-check'},'bait-expiry':{'expire-bait'},'closure':{'close'}}
            if op not in allowed[due_record['kind']]:raise ValueError('Wrong operation for scheduled event')
            del s['due'][due]
        if op=='forage-route':
            route=world.record(e['routeEvidenceId'],'production-route',cp)
            if route['route']!='Forage':raise ValueError('Wrong route')
            pool=(route['sharedStockId'],route['allocationPartitionId'],route['watchId'])
            self._stock_route(s,world,route,'Forage',cp)
            s['poolRoutes'][pool]='Forage'
        elif op=='cancel-setup':
            if aid in s['attempts']:raise ValueError('Committed attempt cannot use pre-exposure cancellation')
            receipt,disposition=self._reservation(world,e,s,cp)
            if receipt['opportunityId'] in s['opportunities'] or any(x in s['equipmentReservations'] or x in s['baitUses'] or x in s['ordinaryBaitUses'] or x in s['chumUses'] for x in receipt['reservedResourceIds']):
                raise ValueError('Pre-exposure cancellation cannot release already spent or committed resources')
            work=world.record(e['workEvidenceId'],'work-record',cp)
            if work['attemptId']!=aid or work['worker']!=e['lead'] or work['phase']!='setup':
                raise ValueError('Actual worked setup time must remain recorded on cancellation')
            worked=active_work_seconds(work,receipt['checkpoint'][0],cp[0])
            released=disposition['releasedUnspentResourceIds'];spent=disposition['spentOrDestroyedResourceIds']
            if (disposition['status']!='cancelled-before-exposure' or
                    disposition['releasedOpportunityId']!=receipt['opportunityId'] or
                    len(set(released+spent))!=len(released+spent) or
                    set(released+spent)!=set(receipt['reservedResourceIds'])):
                raise ValueError('Cancellation must release only actual unspent reservations and preserve losses')
            s['preExposureCancellations'][aid]={'reservationEvidenceId':receipt['id'],
                'startedAt':tuple(receipt['checkpoint']),'cancelledAt':cp,'workedSeconds':worked,
                'workEvidenceId':work['id'],'dispositionEvidenceId':disposition['id'],
                'priorMountWorkEvidenceIds':list(receipt.get('rigMountWorkByPhysicalId',{}).values()),
                'priorMountWorkedSeconds':300*len(receipt.get('rigMountWorkByPhysicalId',{})),
                'releasedUnspentResourceIds':released,'spentOrDestroyedResourceIds':spent,
                'opportunityId':receipt['opportunityId'],'inventoryCreated':[]}
            s['reservationHistory'][receipt['id']]={'attemptId':aid,'outcome':'cancelled-before-exposure'}
        elif op=='commit':
            if aid in s['attempts']:raise ValueError('Attempt already exists')
            receipt,reservation=self._reservation(world,e,s,cp)
            start=tuple(receipt['checkpoint'])
            if (reservation['status']!='reserved-unspent' or
                    not start[0]<=cp[0]<=start[0]+300):
                raise ValueError('First deployment/exposure belongs to the five-minute setup phase')
            require_catch_roll(e['canonicalRoll'],e['lead'])
            if e['canonicalRoll']['id'] in s['rollAttempts']:
                raise ValueError('A canonical roll ID belongs to exactly one attempt')
            if self._allowance_occupied(s,e['lead']):
                raise ValueError('Lead already has an unresolved deployment')
            opportunity=world.record(e['opportunityEvidenceId'],'opportunity',cp)
            assembly=world.record(e['assemblyEvidenceId'],'assembly',cp)
            profile=declared_catch_profile(world,e['catchProfileEvidenceId'],assembly['method'],start)
            if opportunity['catchProfileEvidenceId']!=profile['id']:
                raise ValueError('Opportunity differs from declared catch profile')
            if opportunity['opportunityId'] in s['opportunities'] or assembly['attemptId']!=aid or assembly['lead']!=e['lead']:
                raise ValueError('Spent opportunity or wrong assembly/lead')
            if opportunity['disposition'] not in ('available-stock','exploratory'):
                raise ValueError('Known empty or impossible site cannot commit')
            ordinary_uses=self._assembly(world,assembly,cp,attraction=e.get('attractionPhysicalId') is not None)
            for use in ordinary_uses:
                if use['physicalId'] in s['ordinaryBaitUses'] or use['physicalId'] in s['chumUses'] or use['physicalId'] in s['baitUses']:
                    raise ValueError('Bait or chum material has already spent its usable entitlement')
                if use['physicalId'] not in receipt['reservedResourceIds']:raise ValueError('Ordinary bait was not actually reserved before setup')
                s['ordinaryBaitUses'][use['physicalId']]={'attemptId':aid,'useEvidenceId':use['id']}
            gear=assembly['participatingItemIds']
            if (receipt['method']!=assembly['method'] or receipt['opportunityId']!=opportunity['opportunityId'] or
                    receipt['catchProfileEvidenceId']!=profile['id'] or set(receipt['equipmentIds'])!=set(gear) or
                    receipt['itemRecipeIds']!=assembly['itemRecipeIds']):
                raise ValueError('Committed method, profile, opportunity and equipment must match pre-setup reservation')
            if len(set(gear))!=len(gear) or set(assembly['itemRecipeIds'])!=set(gear) or any(g in s['equipmentReservations'] for g in gear):
                raise ValueError('Wrong or already reserved apparatus')
            if any(rid is not None and rid not in self.cards for rid in assembly['itemRecipeIds'].values()):
                raise ValueError('Unknown actual recipe')
            if len({g for g,rid in assembly['itemRecipeIds'].items() if rid and self.cards[rid]['sourceRecipe']['recipeFamily']=='Bait'})>1:
                raise ValueError('At most one finished Bait receipt')
            pool=(opportunity['sharedStockId'],opportunity['allocationPartitionId'],opportunity['watchId'])
            stock_binding=self._stock_route(s,world,opportunity,'Fishing',cp)
            a={'id':aid,'lead':e['lead'],'responsibleActor':e['lead'],'deploymentReconciled':False,
                'opportunityId':opportunity['opportunityId'],
                'method':assembly['method'],'state':'committed','assemblyId':assembly['assemblyId'],
                'gear':deepcopy(gear),'itemRecipeIds':deepcopy(assembly['itemRecipeIds']),
                'itemFamilyById':deepcopy(assembly['itemFamilyById']),
                'baitId':e.get('baitId'),'receiptActive':False,'checkEligible':{},'checkId':None,
                'startedAt':start,'committedAt':cp,'canonicalRoll':deepcopy(e['canonicalRoll']),
                'reservationEvidenceId':receipt['id'],'setupCompletedAt':(start[0]+300,0,0),
                'workEvidenceIds':list(receipt.get('rigMountWorkByPhysicalId',{}).values()),
                'catchProfileEvidenceId':profile['id'],'catchDC':profile['dc'],
                'manifestEvidenceId':None,'selectedCreatureId':None,'checkAt':tuple(e['checkCheckpoint'])}
            if a['canonicalRoll']['actor']!=e['lead']:raise ValueError('Wrong canonical actor/setter')
            if a['method']=='Trap':
                trap=world.record(e.get('trapDeploymentEvidenceId'),'trap-deployment',cp)
                ident=next(i for i,family in a['itemFamilyById'].items() if family=='Trap')
                if (trap['attemptId']!=aid or trap['trapPhysicalId']!=ident or trap['assemblyId']!=a['assemblyId'] or
                        not trap['locationId'] or not isinstance(trap['elevationFeet'],(int,float)) or
                        not e.get('setterConfigurationEvidenceId')):
                    raise ValueError('Trap deployment must retain actual apparatus location and original configuration identity')
                a['trapHandling']={'physicalId':ident,'state':'deployed','locationId':trap['locationId'],
                    'elevationFeet':trap['elevationFeet'],'deploymentEvidenceId':trap['id'],'inventoryCreated':[]}
                a['setterConfigurationEvidenceId']=e['setterConfigurationEvidenceId']
                if cp>=a['setupCompletedAt']:self._trap_configuration(world,a,cp)
            if a['baitId']:
                dose,age=unused_bait_qualification(world,e['baitEvidenceId'],cp);bid=a['baitId']
                if bid not in gear or not assembly['itemRecipeIds'][bid] or self.cards[assembly['itemRecipeIds'][bid]]['sourceRecipe']['recipeFamily']!='Bait':
                    raise ValueError('Dose is not the registered finished Bait')
                if dose['physicalId']!=bid or dose['recipeId']!=assembly['itemRecipeIds'][bid] or bid in s['baitUses']:
                    raise ValueError('Bait is spent, spoiled or unavailable')
                if e['baitExposureEvidenceId']!=assembly.get('baitExposureEvidenceId'):
                    raise ValueError('Actual exposure must be registered on this assembly')
                exposure,use=bait_receipt(world,e['baitExposureEvidenceId'],assembly)
                if (exposure['physicalId']!=bid or tuple(exposure['checkpoint'])!=cp or
                        exposure['expiresAt']!=e['baitExpiryCheckpoint'] or use['unusedBaitEvidenceId']!=dose['id']):
                    raise ValueError('Exposure must consume this journal\'s actual unused dose at its registered expiry')
                if exposure['locationKind']=='rig-chum':
                    rig=world.record(assembly['rigDeploymentEvidenceId'],'rig-deployment',cp)
                    if (assembly['itemFamilyById'].get(rig['dispenserPhysicalId'])!='Rig' or
                            rig['attemptId']!=aid or rig['dispenserPointId']!=exposure['locationId'] or
                            rig['finishedBaitPhysicalId']!=bid or rig['finishedBaitExposureEvidenceId']!=exposure['id']):
                        raise ValueError('Rig-substituted dose must occupy that actual registered dispenser load')
                else:
                    presentation=world.record(assembly['presentationEvidenceId'],'bait-presentation',cp)
                    if not any(z['physicalId']==bid and z['form']=='finished-Bait' and z['useEvidenceId']==exposure['id'] for z in presentation['sources']):
                        raise ValueError('Exposed dose must appear at the actual recorded method presentation point')
                a['baitDebit']={'physicalId':bid,'recipeId':dose['recipeId'],'attemptId':aid,'assemblyId':a['assemblyId'],
                    'exposureEvidenceId':exposure['id'],'inventoryUseEvidenceId':use['id'],
                    'unusedBaitEvidenceId':dose['id'],
                    'exposedAt':cp,'expiresAt':tuple(exposure['expiresAt']),'unprotectedAgeSecondsAtExposure':age}
                s['baitDebits'][bid]=deepcopy(a['baitDebit'])
                s['baitUses'].append(bid);a['receiptActive']=True
                self._schedule(s,'bait:'+aid,aid,'bait-expiry',e['baitExpiryCheckpoint'],cp,cp[0]+3600)
            self._register_rig(s,a,world,assembly,cp,receipt)
            effects=self._effects(world,e['equipmentEvidenceId'],a,cp)
            chosen=e.get('attractionPhysicalId')
            if chosen is not None and chosen not in effects['affinityByPhysicalId']:
                raise ValueError('Chosen attraction source does not independently qualify')
            response=world.record(e['responseEvidenceId'],'response-candidates',cp)
            if (response['opportunityEvidenceId']!=opportunity['id'] or
                    response['assemblyEvidenceId']!=assembly['id'] or
                    response['attractionPhysicalId']!=chosen or
                    response['opportunityId']!=opportunity['opportunityId'] or
                    {x['physicalId'] for x in response['candidates']}!=set(opportunity['candidateCreatureIds'])):
                raise ValueError('Response list is not the actual opportunity version')
            result=weighted_response(world,e['responseEvidenceId'],effects['affinityByPhysicalId'].get(chosen),e.get('responseDraw'))
            creature=result['physicalId']
            if creature and creature in s['creatureReservations']:raise ValueError('Prey already reserved')
            if not creature and opportunity['disposition']!='exploratory':raise ValueError('Known empty stock cannot commit')
            self._stock_availability(s,world,opportunity,stock_binding,creature,cp,aid)
            a['selectedCreatureId']=creature;a['response']=result;a['attractionPhysicalId']=chosen
            if creature:
                a['manifestEvidenceId']=opportunity['manifestByCreatureId'][creature]
                manifest=world.record(a['manifestEvidenceId'],'material-manifest')
                validate_material_manifest(manifest,initial=creature not in s['materialStates'])
                if creature in s['materialStates']:material_history_to(world,s['materialStates'][creature],manifest)
                if manifest['physicalId']!=creature or tuple(manifest['checkpoint'])>cp:raise ValueError('Anatomy must predate the attempt')
                a['initialManifestSnapshot']=deepcopy(manifest)
                a['originRestrictions']=sorted(material_origin_restrictions(manifest))
                s['materialStates'][creature]=deepcopy(manifest)
                self._physical_checkpoint(world,assembly['admissionEvidenceId'],e['equipmentEvidenceId'],a,cp,a['manifestEvidenceId'])
                s['creatureReservations'][creature]=aid
            self._schedule(s,'check:'+aid,aid,'check',e['checkCheckpoint'],cp,start[0]+3300)
            s['attempts'][aid]=a;s['opportunities'].append(opportunity['opportunityId']);s['poolRoutes'][pool]='Fishing'
            s['rollAttempts'][a['canonicalRoll']['id']]=aid
            s['reservationHistory'][receipt['id']]={'attemptId':aid,'outcome':'committed','committedAt':cp}
            for g in gear:s['equipmentReservations'][g]=aid
        elif aid not in s['attempts']:raise ValueError('Unknown attempt')
        else:
            a=s['attempts'][aid]
            if op=='check':
                if not due_record or a['state']!='committed' or a['checkId'] is not None:raise ValueError('Exactly one due check')
                result=world.record(e['catchResolutionEvidenceId'],'catch-resolution',cp)
                if result['attemptId']!=aid or result['canonicalRoll']!=a['canonicalRoll'] or result['physicalId']!=a['selectedCreatureId']:
                    raise ValueError('Resolved check belongs to another attempt/roll/creature')
                if not a['selectedCreatureId']:raise ValueError('Empty opportunity has no catch roll; close it')
                if result['degree'] not in ('Critical Success','Success','Failure','Critical Failure'):
                    raise ValueError('Use the separately resolved Core task degree')
                if a['method']=='Trap':self._trap_configuration(world,a,cp,result['setterConfigurationEvidenceId'])
                validate_catch_resolution(world,result,a,cp)
                self._setup_and_fishing(world,result,a,cp)
                for key in [result['setupWorkEvidenceId']]+([] if a['method']=='Trap' else [result['workEvidenceId']]):
                    work=world.record(key,'work-record',cp)
                    self._separate_work(world,work,a['workEvidenceIds'])
                    a['workEvidenceIds'].append(key)
                if a['method']=='Trap':
                    configuration=world.record(result['setterConfigurationEvidenceId'],'trap-configuration')
                    if configuration['attemptId']!=aid or configuration['setter']!=a['lead'] or configuration['checkpoint'][0]!=a['startedAt'][0]+300:
                        raise ValueError('Wrong historical setter configuration')
                    if result['personalContributions']!=configuration['personalContributions'] or result['assistantBonus']!=0:
                        raise ValueError('Unattended Trap uses only setup WIS/proficiency and no assistant')
                elif result['assistantBonus']:
                    if result['assistantBonus']!=1:raise ValueError('At most one trained assistant grants +1')
                    assistant=world.record(result['assistantEvidenceId'],'fishing-assistant',cp)
                    assistant_work=world.record(assistant['workEvidenceId'],'work-record',cp)
                    if assistant['attemptId']!=aid or assistant['trainedCredential']!='Fishing tackle' or assistant['worker']==a['lead'] or assistant_work['worker']!=assistant['worker'] or active_work_seconds(assistant_work,a['startedAt'][0],cp[0])<3300:
                        raise ValueError('One trained distinct assistant must work all pre-check minutes')
                self._physical_checkpoint(world,result['admissionEvidenceId'],result['equipmentEvidenceId'],a,cp,a['manifestEvidenceId'])
                effects=self._effects(world,result['equipmentEvidenceId'],a,cp)
                if result['equipmentBonus']!=effects['bonus']:raise ValueError('Resolved check uses wrong source item bonus')
                a['checkId']=a['canonicalRoll']['id'];a['checkEligible']=effects['extraByPhysicalId']
                a['state']='intercepted' if result['degree'] in ('Success','Critical Success') else 'no-catch'
                if a['method']=='Trap' and a['state']=='intercepted':self._capture(s,a,e,world,cp)
                elif a['state']=='intercepted':
                    self._schedule(s,'closure:'+aid,aid,'closure',e['closureCheckpoint'],cp,cp[0]+600)
            elif op=='no-check':
                if not due_record or due_record['kind']!='check' or a['state']!='committed':
                    raise ValueError('No unresolved due check')
                failure=world.record(e['noCatchEvidenceId'],'no-catch-resolution',cp)
                if failure['attemptId']!=aid or failure['reason'] not in ('empty','prey-unavailable','assembly-inoperable','insufficient-work','impossible-access'):
                    raise ValueError('Actual governing no-check cause required')
                a['state']='no-catch';a['noCatchEvidenceId']=failure['id']
            elif op=='capture':
                if a['state']!='intercepted' or a['method']=='Trap':raise ValueError('No attended unresolved interception')
                self._capture(s,a,e,world,cp)
            elif op=='expire-bait':
                if not due_record or not a['baitId'] or not a['receiptActive']:raise ValueError('No live due receipt')
                a['receiptActive']=False
            elif op=='reconcile-rig':
                self._reconcile_rig(s,a,world,e['rigDispositionEvidenceId'],cp)
            elif op=='close':
                if a['state']=='closed' and (a['method']!='Trap' or a['deploymentReconciled']):raise ValueError('Attempt already closed')
                disposition=world.record(e['dispositionEvidenceId'],'actual-disposition',cp)
                if disposition['attemptId']!=aid or disposition['physicalId']!=a['selectedCreatureId']:
                    raise ValueError('Actual creature/apparatus disposition required')
                if disposition['reason'] not in ('retrieved','lawful-handover','abandoned','failed','empty','escaped','deadline','finished'):
                    raise ValueError('Unknown closure reason')
                if due_record and disposition['reason']!='deadline':raise ValueError('Scheduled closure is the deadline')
                if not due_record and disposition['reason']=='deadline':raise ValueError('Cannot invent an earlier deadline')
                if e.get('rigDispositionEvidenceId'):
                    self._reconcile_rig(s,a,world,e['rigDispositionEvidenceId'],cp)
                if a['method']=='Trap':self._close_trap(s,a,world,disposition,cp)
                else:
                    a['disposition']=disposition;a['state']='closed';a['receiptActive']=False;a['deploymentReconciled']=True
                    for key in list(s['due']):
                        if s['due'][key]['attemptId']==aid:del s['due'][key]
                    for g in a['gear']:
                        if a.get('rigHandling') and g==a['rigHandling']['physicalId'] and a['rigHandling']['state'] not in ('retrieved','abandoned'):continue
                        s['equipmentReservations'].pop(g,None)
                    if a['selectedCreatureId']:s['creatureReservations'].pop(a['selectedCreatureId'],None)
            elif op=='checkpoint':
                event=world.record(e['stateEvidenceId'],'state-transition',cp)
                if event['attemptId']!=aid:raise ValueError('Wrong state transition')
                # Explicitly no changes to dice, due events, resources or anatomy.
            else:raise ValueError('Unsupported bounded operation')
        s['version']+=1;s['checkpoint']=cp;s['seen'].append(e['id']);self.state=s
        return deepcopy(s)

    def _capture(self,s,a,e,world,cp):
        placement=world.record(e['captureEvidenceId'],'secure-capture',cp);aid=a['id'];creature=a['selectedCreatureId']
        if placement['physicalId']!=creature or placement['attemptId']!=aid:
            raise ValueError('Capture must bind actual creature and attempt')
        if not placement['location'] or not isinstance(placement['elevationFeet'],(int,float)):
            raise ValueError('Actual receiving location and elevation required')
        self._physical_checkpoint(world,placement['admissionEvidenceId'],placement['equipmentEvidenceId'],a,cp,placement['manifestEvidenceId'])
        if a['method']!='Trap':
            closure=s['due'].get('closure:'+aid)
            if not closure or cp>=tuple(closure['at']):raise ValueError('Retrieval entitlement has closed')
            work=world.record(placement['retrievalWorkEvidenceId'],'work-record',cp)
            if (work['worker']!=a['lead'] or work['attemptId']!=aid or work['phase']!='retrieval' or
                    active_work_seconds(work,a['checkAt'][0],cp[0])<300):
                raise ValueError('Lead must supply both hands and five actual retrieval minutes')
            self._separate_work(world,work,a['workEvidenceIds'])
            a['workEvidenceIds'].append(work['id'])
            a['retrievalWorkEvidenceId']=work['id']
        current=world.record(placement['manifestEvidenceId'],'material-manifest',cp)
        initial=a['initialManifestSnapshot']
        if world.record(a['manifestEvidenceId'],'material-manifest')!=initial:
            raise ValueError('Pre-attempt material snapshot cannot be rewritten after commitment')
        material_history_to(world,initial,current)
        s['materialStates'][creature]=deepcopy(current)
        if current['physicalId']!=creature:raise ValueError('Wrong anatomy')
        order=world.record(placement['recoveryOrderEvidenceId'],'recovery-order')
        if order['attemptId']!=aid or tuple(order['checkpoint'])>=a['checkAt']:
            raise ValueError('Recovery order must be fixed before the check')
        initial_ids=[u['id'] for u in initial['extraReserve']]
        if len(set(order['unitIds']))!=len(order['unitIds']) or set(order['unitIds'])!=set(initial_ids):
            raise ValueError('Order must cover the actual original reserve once')
        effects=self._effects(world,placement['equipmentEvidenceId'],a,cp)
        extra=max((v for i,v in a['checkEligible'].items() if effects['extraByPhysicalId'].get(i)==v),default=0)
        if creature not in s['recoveries']:
            available={u['id'] for u in current['extraReserve'] if u['state']=='available' and
                (u['material']!='ordinary-fish-meat' or F(str(u['massLb']))==1)}
            reserve=[i for i in order['unitIds'] if i in available]
            restrictions=set(a['originRestrictions'])|material_origin_restrictions(current)
            if restrictions or not material_access_permitted(current):reserve=[]
            s['recoveries'][creature]={'firstAttemptId':aid,'sourceExtra':extra,
                'authorizedUnitIds':reserve[:extra],'inventoryCreated':[],
                'lifeStateAtCapture':placement['lifeState'],'evaluatedIncludingZero':True,
                'manifestEvidenceId':placement['manifestEvidenceId'],'manifestSnapshot':deepcopy(current),
                'captureEvidenceId':placement['id'],'captureSnapshot':deepcopy(placement),'capturedAt':cp,
                'originRestrictions':sorted(restrictions)}
        a['state']='captured';a['captureEvidenceId']=placement['id']
