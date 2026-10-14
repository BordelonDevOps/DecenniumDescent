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


def copper(value, buying=True):
    return F((ceil if buying else floor)(F(value)*100),100)


def finished_reference(recipe, body):
    return F(str(recipe['economy']['recommendedMarketValue'])) / recipe['quantity'] + F(str(body['baselinePriceGp']))


def structural_hp(ordinary, old_max, old_current, old_percent=0, new_percent=0, old_flaw=False, new_flaw=False):
    if ordinary<=0 or old_max<=0 or not 0<=old_current<=old_max:
        raise ValueError('Invalid recorded structural HP')
    if old_percent not in (0,25,50) or new_percent not in (0,25,50):
        raise ValueError('No admitted structural percentage')
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


def ordered_output(recipe, band, reserves, option='yield'):
    """Physical reserves are historical records; call only after lawful work.

    This checks the recorded stock, not the truth of a claim to own it. The caller
    must obtain these records from the actual governing inventory/work ledger.
    """
    out=quality(recipe,band,option);needed=out['maximumReserve']
    if len(reserves)!=needed or len({x['id'] for x in reserves})!=needed:
        raise ValueError('Exact exclusive ordered reserve required')
    for r in reserves:
        if not r.get('inventoryEvidenceRef') or not r.get('reservationEvidenceRef'):
            raise ValueError('Actual inventory and reservation records required')
        if r.get('ownerOrderId')!=reserves[0].get('ownerOrderId') or not r.get('ownerOrderId'):
            raise ValueError('One order must reserve all stock')
        if r['state']!='available-reserved' or r['grade']!='Standard' or r['priorMagicalAlteration']:
            raise ValueError('Unavailable or ineligible reserve pauses completion')
        if recipe['recipeFamily']=='Bait':
            if F(str(r['carrierLb']))!=F(1,10) or F(str(r['wrapperLb']))!=F(1,100) or r['materialCondition']=='Spoiled':
                raise ValueError('Actual eligible carrier and wrapper required')
        elif r['currentHP']<=0 or not r.get('originalConstituentIds'):
            raise ValueError('Incomplete or Broken body pauses completion')
    selected=deepcopy(reserves[:out['quantity']])
    for body in selected:
        if recipe['recipeFamily']!='Bait':
            body.update(structural_hp(5,body['maximumHP'],body['currentHP'],body['durabilityPercent'],out['durabilityPercent'],body['flawed'],out['addsFlaw']))
    return {'outcome':out,'selected':selected,'unused':deepcopy(reserves[out['quantity']:])}


def repair_quote(recipe, body, current_hp, maximum_hp, original_required, original_surviving):
    if recipe['recipeFamily']=='Bait':raise ValueError('Bait cannot be repaired')
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
        'successHP':maximum_hp,'refills':[]}


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
        r=deepcopy(self._records[key])
        if r['kind']!=kind or (checkpoint is not None and tuple(r['checkpoint'])!=tuple(checkpoint)):
            raise ValueError('Wrong kind or historical checkpoint')
        return r


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
            qualifies=(state['receiptAttemptId']==assembly['attemptId'] and
                tuple(state['exposedAt'])<=tuple(e['checkpoint'])<tuple(state['expiresAt']) and not state['assemblyBaitSuppressed'])
        else:
            qualifies=(state['currentHP']>0 and state['complete'] and not state['suppressed'] and not state['melded'])
        if qualifies:eligible.append((ident,r['mechanics']['fishingBonus'],r['mechanics']['extraYield'],r['mechanics']['attracts']))
    return {'bonus':max((x[1] for x in eligible),default=0),
        'extra':max((x[2] for x in eligible),default=0),'eligibleIds':[x[0] for x in eligible],
        'extraByPhysicalId':{x[0]:x[2] for x in eligible},'affinityByPhysicalId':{x[0]:x[3] for x in eligible}}


def weighted_response(world, evidence_id, selected_affinity, draw):
    e=world.record(evidence_id,'response-candidates')
    candidates=sorted(e['candidates'],key=lambda c:c['physicalId'])
    if len({c['physicalId'] for c in candidates})!=len(candidates):raise ValueError('Duplicate real creature')
    total=0;rows=[]
    for c in candidates:
        profile=world.record(c['profileEvidenceId'],'ordinary-prey-profile')
        path=world.record(c['responseEvidenceId'],'response-path',e['checkpoint'])
        if profile['physicalId']!=c['physicalId'] or path['physicalId']!=c['physicalId']:
            raise ValueError('Profile or path belongs to another creature')
        if profile['captureProcedure']!='ordinary-provision' or path['responseDisposition']!='receptive':
            raise ValueError('Encounter resistance or rejection is not ordinary prey response')
        if path['unobstructedWaterPathFeet']<0:raise ValueError('Negative path length')
        # An approved response record is an external premise, not something a
        # caller's `willing=True` flag can substitute for here.
        weight=2 if selected_affinity in profile['approvedAffinities'] and path['unobstructedWaterPathFeet']<=30 else 1
        total+=weight;rows.append((c['physicalId'],weight,total))
    if not rows:
        if draw is not None:raise ValueError('Empty site has no response draw')
        return {'physicalId':None,'weights':[],'draw':None}
    if not isinstance(draw,int) or isinstance(draw,bool) or not 1<=draw<=total:
        raise ValueError('One supplied uniform integer draw must fit the finite pool')
    return {'physicalId':next(i for i,w,end in rows if draw<=end),'weights':[(i,w) for i,w,end in rows],'draw':draw}


def validate_material_manifest(manifest):
    groups=('baseline','extraReserve','damagedBaseline','unique')
    units=[u for k in groups for u in manifest[k]]
    if len({u['id'] for u in units})!=len(units):raise ValueError('Anatomy units must be disjoint')
    mass=sum((F(str(u['massLb'])) for u in units),F(0))
    if any(F(str(u['massLb']))<=0 for u in units) or mass>F(str(manifest['bodyMassLb'])):
        raise ValueError('Units exceed actual physical body mass')
    for u in manifest['extraReserve']:
        if u['material']=='ordinary-fish-meat' and F(str(u['massLb']))!=1:
            raise ValueError('Extra ordinary-meat unit requires one real pound')
    return True


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
    captured=world.record(recovery['manifestEvidenceId'],'material-manifest')
    choice=world.record(event['choiceEvidenceId'],'harvest-category-choice')
    if any(z['physicalId']!=donor for z in (prerequisite,manifest,captured,choice)) or tuple(choice['checkpoint'])>=tuple(cp):
        raise ValueError('Actual donor-bound prerequisites and prior category choice required')
    validate_material_manifest(manifest)
    for group in ('baseline','extraReserve','damagedBaseline','unique'):
        before={u['id']:u for u in captured[group]}
        for u in manifest[group]:
            if u['id'] not in before or any(u[k]!=before[u['id']][k] for k in ('material','category')) or F(str(u['massLb']))>F(str(before[u['id']]['massLb'])):
                raise ValueError('Later harvest cannot invent or enlarge captured anatomical units')
    if event['degree'] not in ('Critical Success','Success','Failure','Critical Failure'):
        raise ValueError('Use the resolved governing harvesting degree')
    categories=set(choice['categories']);authorized=set(recovery['authorizedUnitIds'])
    ordinary=manifest['baseline']+[u for u in manifest['extraReserve'] if u['id'] in authorized]
    all_ordinary=manifest['baseline']+manifest['extraReserve']+manifest['damagedBaseline']
    if not categories<=set(u['category'] for u in all_ordinary):raise ValueError('Unknown category cannot be selected')
    selected=[u['id'] for u in ordinary if u['category'] in categories and u['state']=='available']
    permitted=manifest['resourcePolicy']=='permitted' and captured['resourcePolicy']=='permitted'
    if event['degree'] not in ('Critical Success','Success') or not permitted:selected=[]
    damaged=event.get('damagedBaselineUnitId')
    if damaged is not None:
        candidates={u['id'] for u in manifest['damagedBaseline'] if u['category'] in categories and u['state']=='available'}
        if event['degree']!='Critical Success' or damaged not in candidates or not permitted:
            raise ValueError('Critical recovery needs its separate eligible damaged baseline unit')
        selected.append(damaged)
    if len(selected)!=len(set(selected)):raise ValueError('Duplicate extracted anatomy unit')
    out=deepcopy(history)
    out[donor]={'resolvedDegree':event['degree'],'authorizedExtractedUnitIds':selected,
        'forfeitedUnselectedOrdinaryUnitIds':[u['id'] for u in all_ordinary if u['category'] not in categories],
        'uniqueDropsAuthorized':[],'inventoryCreated':[],'deathOrRemovalTime':prerequisite['deathOrRemovalTime'],
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


def physical_admission(world, admission_id, method, checkpoint):
    """Check fixed limits on an externally adjudicated apparatus/prey record.

    Shape, support, access, containment and behavior still need that record's
    cited adjudication. Numerical fit alone does not establish admission.
    """
    a=world.record(admission_id,'physical-admission',checkpoint)
    if a['method']!=method or a['disposition']!='admitted':raise ValueError('Method not physically admitted')
    if not a['apparatusStateIds']:raise ValueError('Actual capture apparatus history required')
    for key in a['apparatusStateIds']:
        body=world.record(key,'item-state',checkpoint)
        if body['currentHP']<=0 or not body['complete'] or body['melded']:
            raise ValueError('Indispensable capture apparatus is Broken, incomplete or melded')
    if a['preyMassLb']>10 or a['preyMassLb']<0 or a['preyMassLb']>a['handlingLimitLb']:
        raise ValueError('Catch exceeds admitted mass/handling limit')
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
            'baitUses':[],'recoveries':{},'due':{},'poolRoutes':{}}

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
        if set(assembly['participatingItemIds'])!=set(a['gear']) or assembly['itemRecipeIds']!=a['itemRecipeIds']:
            raise ValueError('Deployment candidates cannot be replaced after commitment')
        if e['roll']!=a['canonicalRoll']:raise ValueError('Changed canonical current roll')
        out=effect_candidates(world,evidence_id,self.cards)
        # The receipt is an assembly effect; a caller cannot reactivate a spent
        # or expired dose by presenting a copied pre-expiry item snapshot.
        if a['baitId'] and not a['receiptActive']:
            out['extraByPhysicalId'].pop(a['baitId'],None)
            out['affinityByPhysicalId'].pop(a['baitId'],None)
            out['eligibleIds']=[x for x in out['eligibleIds'] if x!=a['baitId']]
            out['extra']=max(out['extraByPhysicalId'].values(),default=0)
            out['bonus']=max((self.cards[a['itemRecipeIds'][x]]['sourceRecipe']['mechanics']['fishingBonus'] for x in out['eligibleIds']),default=0)
        return out

    def _assembly(self, world, assembly, cp, attraction=False):
        admission=physical_admission(world,assembly['admissionEvidenceId'],assembly['method'],cp)
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
        if assembly['method'] in ('Rod','Trap') or attraction:
            presentation=world.record(assembly['presentationEvidenceId'],'bait-presentation',cp)
            if presentation['attemptId']!=assembly['attemptId'] or not presentation['sourcePhysicalIds']:
                raise ValueError('Actual bait/Lure presentation required')
            allowed={'ordinary-bait','finished-Bait','Lure'} if assembly['method']!='Trap' else {'ordinary-bait','finished-Bait'}
            if not allowed.intersection(presentation['forms']):raise ValueError('Required actual bait is missing')
            if not set(presentation['sourcePhysicalIds'])<=set(assembly['participatingItemIds'])|set(presentation['ordinaryBaitLotIds']):
                raise ValueError('Presentation must bind actual apparatus or ordinary bait lot')
        return admission

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
            if pool in s['poolRoutes'] and s['poolRoutes'][pool]!='Forage':raise ValueError('Overlapping Fishing stock')
            s['poolRoutes'][pool]='Forage'
        elif op=='commit':
            if aid in s['attempts']:raise ValueError('Attempt already exists')
            if any(a['lead']==e['lead'] and a['state']!='closed' for a in s['attempts'].values()):
                raise ValueError('Lead already has an unresolved deployment')
            opportunity=world.record(e['opportunityEvidenceId'],'opportunity',cp)
            assembly=world.record(e['assemblyEvidenceId'],'assembly',cp)
            if opportunity['opportunityId'] in s['opportunities'] or assembly['attemptId']!=aid or assembly['lead']!=e['lead']:
                raise ValueError('Spent opportunity or wrong assembly/lead')
            if opportunity['disposition'] not in ('available-stock','exploratory'):
                raise ValueError('Known empty or impossible site cannot commit')
            self._assembly(world,assembly,cp,attraction=e.get('attractionPhysicalId') is not None)
            gear=assembly['participatingItemIds']
            if len(set(gear))!=len(gear) or set(assembly['itemRecipeIds'])!=set(gear) or any(g in s['equipmentReservations'] for g in gear):
                raise ValueError('Wrong or already reserved apparatus')
            if any(rid is not None and rid not in self.cards for rid in assembly['itemRecipeIds'].values()):
                raise ValueError('Unknown actual recipe')
            if len({g for g,rid in assembly['itemRecipeIds'].items() if rid and self.cards[rid]['sourceRecipe']['recipeFamily']=='Bait'})>1:
                raise ValueError('At most one finished Bait receipt')
            pool=(opportunity['sharedStockId'],opportunity['allocationPartitionId'],opportunity['watchId'])
            # A partition is a cited, authoritative disjoint allocation, never a
            # caller-created alternate name for overlapping physical stock.
            allocation=world.record(opportunity['allocationEvidenceId'],'stock-allocation')
            if (allocation['sharedStockId'],allocation['partitionId'])!=pool[:2]:raise ValueError('Wrong stock allocation')
            if s['poolRoutes'].get(pool,'Fishing')!='Fishing':raise ValueError('Overlapping Forage stock route')
            a={'id':aid,'lead':e['lead'],'method':assembly['method'],'state':'committed',
                'gear':deepcopy(gear),'itemRecipeIds':deepcopy(assembly['itemRecipeIds']),
                'baitId':e.get('baitId'),'receiptActive':False,'checkEligible':{},'checkId':None,
                'startedAt':cp,'canonicalRoll':deepcopy(e['canonicalRoll']),
                'manifestEvidenceId':None,'selectedCreatureId':None,'checkAt':tuple(e['checkCheckpoint'])}
            if a['canonicalRoll']['actor']!=e['lead']:raise ValueError('Wrong canonical actor/setter')
            if a['baitId']:
                dose=world.record(e['baitEvidenceId'],'unused-bait',cp);bid=a['baitId']
                if bid not in gear or not assembly['itemRecipeIds'][bid] or self.cards[assembly['itemRecipeIds'][bid]]['sourceRecipe']['recipeFamily']!='Bait':
                    raise ValueError('Dose is not the registered finished Bait')
                if dose['physicalId']!=bid or bid in s['baitUses'] or not 0<=dose['unprotectedHours']<24 or dose['condition']!='eligible':
                    raise ValueError('Bait is spent, spoiled or unavailable')
                s['baitUses'].append(bid);a['receiptActive']=True
                self._schedule(s,'bait:'+aid,aid,'bait-expiry',e['baitExpiryCheckpoint'],cp,cp[0]+3600)
            effects=self._effects(world,e['equipmentEvidenceId'],a,cp)
            chosen=e.get('attractionPhysicalId')
            if chosen is not None and chosen not in effects['affinityByPhysicalId']:
                raise ValueError('Chosen attraction source does not independently qualify')
            response=world.record(e['responseEvidenceId'],'response-candidates',cp)
            if response['opportunityId']!=opportunity['opportunityId'] or {x['physicalId'] for x in response['candidates']}!=set(opportunity['candidateCreatureIds']):
                raise ValueError('Response list is not the actual opportunity version')
            result=weighted_response(world,e['responseEvidenceId'],effects['affinityByPhysicalId'].get(chosen),e.get('responseDraw'))
            creature=result['physicalId']
            if creature and creature in s['creatureReservations']:raise ValueError('Prey already reserved')
            if not creature and opportunity['disposition']!='exploratory':raise ValueError('Known empty stock cannot commit')
            a['selectedCreatureId']=creature;a['response']=result;a['attractionPhysicalId']=chosen
            if creature:
                a['manifestEvidenceId']=opportunity['manifestByCreatureId'][creature]
                manifest=world.record(a['manifestEvidenceId'],'material-manifest')
                validate_material_manifest(manifest)
                if manifest['physicalId']!=creature or tuple(manifest['checkpoint'])>cp:raise ValueError('Anatomy must predate the attempt')
                s['creatureReservations'][creature]=aid
            self._schedule(s,'check:'+aid,aid,'check',e['checkCheckpoint'],cp,cp[0]+3300)
            s['attempts'][aid]=a;s['opportunities'].append(opportunity['opportunityId']);s['poolRoutes'][pool]='Fishing'
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
                work=world.record(result['workEvidenceId'],'work-record',cp)
                required=300 if a['method']=='Trap' else 3300
                if work['worker']!=a['lead'] or active_work_seconds(work,a['startedAt'][0],cp[0])<required:
                    raise ValueError('Actual required setup/fishing work not completed')
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
                physical_admission(world,result['admissionEvidenceId'],a['method'],cp)
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
            elif op=='close':
                if a['state']=='closed':raise ValueError('Attempt already closed')
                disposition=world.record(e['dispositionEvidenceId'],'actual-disposition',cp)
                if disposition['attemptId']!=aid or disposition['physicalId']!=a['selectedCreatureId']:
                    raise ValueError('Actual creature/apparatus disposition required')
                if disposition['reason'] not in ('retrieved','lawful-handover','abandoned','failed','empty','escaped','deadline'):
                    raise ValueError('Unknown closure reason')
                if due_record and disposition['reason']!='deadline':raise ValueError('Scheduled closure is the deadline')
                if not due_record and disposition['reason']=='deadline':raise ValueError('Cannot invent an earlier deadline')
                a['disposition']=disposition;a['state']='closed';a['receiptActive']=False
                for key in list(s['due']):
                    if s['due'][key]['attemptId']==aid:del s['due'][key]
                for g in a['gear']:s['equipmentReservations'].pop(g,None)
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
        physical_admission(world,placement['admissionEvidenceId'],a['method'],cp)
        if a['method']!='Trap':
            closure=s['due'].get('closure:'+aid)
            if not closure or cp>=tuple(closure['at']):raise ValueError('Retrieval entitlement has closed')
            work=world.record(placement['retrievalWorkEvidenceId'],'work-record',cp)
            if active_work_seconds(work,a['checkAt'][0],cp[0])<300:raise ValueError('Five actual retrieval minutes required')
        current=world.record(placement['manifestEvidenceId'],'material-manifest',cp)
        initial=world.record(a['manifestEvidenceId'],'material-manifest')
        validate_material_manifest(current)
        if current['physicalId']!=creature:raise ValueError('Wrong anatomy')
        for group in ('baseline','extraReserve','damagedBaseline','unique'):
            before={u['id']:u for u in initial[group]}
            for unit in current[group]:
                if unit['id'] not in before or any(unit.get(k)!=before[unit['id']].get(k) for k in ('material','category')) or F(str(unit['massLb']))>F(str(before[unit['id']]['massLb'])):
                    raise ValueError('Capture cannot add or enlarge anatomical units')
        order=world.record(placement['recoveryOrderEvidenceId'],'recovery-order')
        if order['attemptId']!=aid or tuple(order['checkpoint'])>=a['checkAt']:
            raise ValueError('Recovery order must be fixed before the check')
        initial_ids=[u['id'] for u in initial['extraReserve']]
        if len(set(order['unitIds']))!=len(order['unitIds']) or set(order['unitIds'])!=set(initial_ids):
            raise ValueError('Order must cover the actual original reserve once')
        effects=self._effects(world,placement['equipmentEvidenceId'],a,cp)
        extra=max((v for i,v in a['checkEligible'].items() if effects['extraByPhysicalId'].get(i)==v),default=0)
        if creature not in s['recoveries']:
            available={u['id'] for u in current['extraReserve'] if u['state']=='available'}
            reserve=[i for i in order['unitIds'] if i in available]
            if current['resourcePolicy']!='permitted':reserve=[]
            s['recoveries'][creature]={'firstAttemptId':aid,'sourceExtra':extra,
                'authorizedUnitIds':reserve[:extra],'inventoryCreated':[],
                'lifeStateAtCapture':placement['lifeState'],'evaluatedIncludingZero':True,
                'manifestEvidenceId':placement['manifestEvidenceId']}
        a['state']='captured';a['captureEvidenceId']=placement['id']
