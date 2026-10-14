"""Bounded manuscript reference, not the companion game runtime.

Source factories bind recipes/models. Per-item causal predicates, anatomical fit,
actual tools, legal actions and world placement are independently adjudicated
premises, not facts inferred by these arithmetic/ledger functions.
Callers apply each returned transition to one authoritative ledger; retaining an
old Python value does not fork an item's resource history or authorize rollback.
"""
from copy import deepcopy
from fractions import Fraction as F
from math import ceil
import tailoring_reference as tailor
import leatherworking_reference as leather
from build_jewelcrafting_recipe_candidate import SLOTS, EXCLUSIONS

# Ability/proficiency gates for the exact JC-D03 prose predicates. '*' means
# whatever proficiency the independent legitimate task actually authorizes.
CHECKS={
 'Stealth':[('DEX','Stealth','legal-hide-or-unnoticed-motion'),('DEX','Sleight of Hand','conceal-compatible-small-object')],
 'Flora':[('INT','Nature','assess-botanical-material'),('WIS','Survival','identify-or-avoid-harmful-growth'),('DEX','*','difficult-nonharvest-botanical-handling'),('STR','Athletics','climb-supporting-plant')],
 'Poison':[('INT','Nature','assess-actual-toxin'),('WIS','Medicine','diagnose-or-permitted-poison-treatment')],
 'Unholy':[('INT','Religion','documented-undead-curse-necrotic-knowledge'),('INT','Arcana','analyze-actual-undead-curse-necrotic-magic')],
 'Earth':[('INT','Nature','assess-rock-soil-mineral'),('WIS','Survival','present-earth-stone-hazard'),('STR','Athletics','climb-rock-stone-holds'),('DEX','Acrobatics','loose-shifting-earth-stone-footing')],
 'Strength':[('STR','Athletics','climb-swim-checked-jump-noncreature-cargo'),('STR',None,'force-hold-move-nonliving-fixture')],
 'Psychic':[('INT','Arcana','examine-actual-psychic-mental-magic'),('INT','Investigation','permitted-altered-perception-reality-test')],
 'Arcane':[('INT','Arcana','examine-actual-magic-inscription-mechanism'),('CASTING','*','required-counteract-dispel-check')],
 'Cold':[('INT','Nature','assess-cold-ice'),('WIS','Survival','manage-avoid-cold-exposure'),('DEX','Acrobatics','specifically-icy-footing'),('CON','*','governing-cold-exposure-endurance')],
 'Vitality':[('WIS','Medicine','permitted-diagnosis-first-aid-stabilization-treatment'),('CON','*','bodily-exertion-exposure-deprivation-endurance')],
 'Lightning':[('INT','Nature','assess-electricity'),('INT','Arcana','assess-magical-electricity'),('WIS','Survival','present-electrical-hazard'),('DEX','*','required-noncraft-energized-manipulation')],
 'Fire':[('INT','Nature','assess-flame-heat'),('INT','Arcana','assess-magical-flame-heat'),('WIS','Survival','present-fire-heat-hazard'),('STR','*','actual-fire-containment-extinguishing'),('DEX','*','actual-fire-containment-extinguishing'),('CON','*','heat-endurance')],
 'Water':[('INT','Nature','assess-water-currents-route'),('WIS','Survival','assess-water-currents-route'),('STR','Athletics','swim'),('DEX','Acrobatics','liquid-water-hazardous-footing')],
 'Acid':[('INT','Nature','assess-acid-corrosion'),('INT','Arcana','assess-magical-acid-corrosion'),('WIS','Survival','present-acid-exposure'),('DEX','*','difficult-noncraft-acid-vessel-handling')]}
SAVES={
 'Stealth':['explicit-detection-revelation-concealment-resistance'],
 'Flora':['direct-binding-obstructing-plants','actual-botanical-spore-toxin-exposure'],
 'Poison':['direct-poison-damage-condition-exposure-consequence'],
 'Unholy':['necrotic-damage','operative-curse','documented-undead-magical-charm-fear-command'],
 'Earth':['direct-earth-stone-collapse-movement-crushing','explicit-petrification'],
 'Strength':['physical-force-movement-prone-restraint'],
 'Psychic':['psychic-damage','magical-charm-fear','explicit-thought-memory-mental-intrusion-command'],
 'Arcane':['direct-resolved-spell','direct-expressly-magical-effect'],
 'Cold':['cold-damage','direct-freezing-chilling-exposure'],
 'Vitality':['disease-poison-wound-injury-bodily-exposure-suffocation-exertion'],
 'Lightning':['lightning-damage','explicit-electrical-shock'],
 'Fire':['fire-damage','direct-burning-heat'],
 'Water':['direct-water-pressure-current-engulfment-drowning'],
 'Acid':['acid-damage','actual-explicit-corrosive-effect']}

def validate_designations(items):
    occupied={};hands=set();seen=set();counts={}
    for r in items:
        if r['id'] in seen:raise ValueError('duplicate physical identity')
        seen.add(r['id'])
        if r.get('state')!='worn' or not r.get('slotValid'):continue
        slot=r.get('slot');wearer=r.get('wearer');key=(wearer,slot)
        if key in occupied:raise ValueError('competing designated benefits')
        occupied[key]=r['id']
        if r.get('trade')!='Jewelcrafting':continue
        if slot not in SLOTS[r['family']]:raise ValueError('wrong jewel position')
        if not r.get('physicalCompatibilityEstablished'):raise ValueError('physical fit/anatomy/clearance not established')
        counts[wearer]=counts.get(wearer,0)+1
        if counts[wearer]>7:raise ValueError('too many active jewels')
        if r['family']=='Ring':
            hand=r.get('actualCompatibleHand')
            if not hand or (wearer,hand) in hands:raise ValueError('rings require different compatible hands')
            hands.add((wearer,hand))
    return occupied

def predicate_eligible(item,event):
    if not event.get('actualRoll') or event.get('automaticResult'):return False
    if set(event.get('categories',())).intersection(EXCLUSIONS):return False
    own=event.get('itemPremises',{}).get(item['id'],{})
    if not own.get('actualCausalPredicateEstablished'):return False
    predicates=set(own.get('predicateIds',()))
    tag=item['tag'];kind=event.get('kind');ability=event.get('ability');skill=event.get('proficiency')
    if kind=='ability-check':
        for a,s,p in CHECKS[tag]:
            amatch=ability==a if a!='CASTING' else event.get('actualSpellcastingAbilityCheck') is True
            if amatch and (s=='*' or skill==s) and p in predicates:return True
        return False
    if kind=='saving-throw':
        if tag=='Strength' and ability!='STR':return False
        if tag=='Vitality' and ability!='CON':return False
        return bool(predicates.intersection(SAVES[tag]))
    return False

def qualifies(item,event):
    return (item.get('trade')=='Jewelcrafting' and item.get('state')=='worn'
      and item.get('complete') and item.get('hp',0)>0 and not item.get('suppressed')
      and item.get('fit') and item.get('slotValid') and item.get('wearer')==event.get('actor')
      and item.get('physicalCompatibilityEstablished')
      and (item['family'] not in ('Brooch','Gem') or item.get('actualHostSupport'))
      and predicate_eligible(item,event))

def jewel_flat_bonus(items,event):
    validate_designations(items)
    return max((r['bonus'] for r in items if qualifies(r,event)),default=0)

def combined_check_bonus(items,event,older_trade_task,leather_task_ids=()):
    validate_designations(items)
    if not event.get('id') or event['id']!=older_trade_task.get('id'):raise ValueError('missing or different canonical roll identity')
    if event.get('kind')!='ability-check' or older_trade_task.get('kind')!='ability-check':raise ValueError('older trades have no save route')
    if any(k not in event or k not in older_trade_task or event[k]!=older_trade_task[k] for k in ('actor','ability','proficiency','automaticResult')):raise ValueError('inconsistent canonical roll descriptors')
    if event.get('actualRoll') is not True or older_trade_task.get('actualCheck') is not True or event['automaticResult'] is not False:raise ValueError('requires an actual nonautomatic check')
    # Both itemPremises maps are current-event views keyed by the same canonical
    # ID. Their domain vocabulary may differ; neither map borrows old premises.
    others=[r for r in items if r.get('trade')!='Jewelcrafting']
    return max(jewel_flat_bonus(items,event),tailor.cross_trade_task_bonus(others,older_trade_task,leather_task_ids))

def new_ledger(campaign,epoch):
    return {'campaignId':campaign,'epoch':epoch,'items':{},'rollSpenders':{},'rollEffects':{}}

def checked_checkpoint(ledger,point,at_time=None):
    """External scheduler premise: stable order at a timestamp and due dawns.

    processedDawnThrough is the last dawn preceding this event (inclusive for a
    dawn transition itself). At a dawn timestamp it distinguishes the actual
    before/after scheduler order. This helper does not manufacture that premise.
    """
    if not isinstance(point,dict) or point.get('campaignId')!=ledger['campaignId'] or point.get('epoch')!=ledger['epoch']:raise ValueError('wrong campaign or fixed epoch')
    if any(k not in point for k in ('time','order','processedDawnThrough')):raise ValueError('missing authoritative event checkpoint')
    t=point['time'];order=point['order'];through=point['processedDawnThrough']
    if isinstance(t,bool) or not isinstance(t,(int,F)) or isinstance(order,bool) or not isinstance(order,int):raise ValueError('invalid campaign event position')
    if at_time is not None and t!=at_time:raise ValueError('event timestamp mismatch')
    n=(t-ledger['epoch'])//86400
    allowed={None} if n<0 else {n}
    if n>=0 and t==ledger['epoch']+n*86400:allowed.add(n-1 if n else None)
    if isinstance(through,bool) or (through is not None and not isinstance(through,int)) or through not in allowed:raise ValueError('incorrect preceding-dawn checkpoint')
    return deepcopy(point)

def require_later(state,point):
    old=state['lastCheckpoint']
    if (point['time'],point['order'])<=(old['time'],old['order']):raise ValueError('replayed or earlier campaign event')

def initialize(ledger,item,creation_id,created_at,*,processed_dawn_through,checkpoint):
    if item['id'] in ledger['items']:raise ValueError('physical imprint already initialized')
    maximum=item['maximumCharges']
    if not isinstance(maximum,int) or not 1<=maximum<=6:raise ValueError('invalid source charge maximum')
    # The authoritative campaign scheduler supplies its already-processed
    # checkpoint, especially when creation coincides with a dawn timestamp.
    n=(created_at-ledger['epoch'])//86400
    allowed={None} if n<0 else {n}
    if created_at==ledger['epoch']+n*86400 and n>=0:allowed.add(n-1 if n else None)
    if processed_dawn_through not in allowed:raise ValueError('creation lacks correct campaign dawn checkpoint')
    point=checked_checkpoint(ledger,checkpoint,created_at)
    if point['processedDawnThrough']!=processed_dawn_through:raise ValueError('creation checkpoint disagreement')
    d=deepcopy(ledger);d['items'][item['id']]={'recipeId':item['recipeId'],'maximum':maximum,'current':maximum,'creationId':creation_id,'createdAt':created_at,'createdAfterProcessedDawn':processed_dawn_through,'lastDawn':processed_dawn_through,'lastCheckpoint':point,'dawnEvents':[],'spends':[]};return d

def commit_charge(ledger,items,item_id,event):
    validate_designations(items)
    chosen=next((r for r in items if r['id']==item_id),None)
    if not chosen or not qualifies(chosen,event):raise ValueError('ineligible item or event')
    if not event.get('conscious') or event.get('incapacitated') or not event.get('voluntaryActivationAllowed'):raise ValueError('voluntary activation unavailable')
    if event.get('phase')!='before-commit' or event.get('resultRevealed'):raise ValueError('too late')
    if not event.get('id'):raise ValueError('missing actual roll identity')
    if event['id'] in ledger['rollSpenders']:raise ValueError('event already has a Jewelcrafting expenditure')
    state=ledger['items'].get(item_id)
    if not state or state['recipeId']!=chosen['recipeId'] or state['maximum']!=chosen['maximumCharges'] or state['current']<1:raise ValueError('charge unavailable or imprint mismatch')
    point=checked_checkpoint(ledger,event.get('checkpoint'))
    require_later(state,point)
    if state['lastDawn']!=point['processedDawnThrough']:raise ValueError('resolve all preceding dawn states before spending')
    if event.get('canceledBeforeCommit'):return deepcopy(ledger)
    d=deepcopy(ledger);d['items'][item_id]['current']-=1;d['items'][item_id]['spends'].append({'rollId':event['id'],'checkpoint':point});d['items'][item_id]['lastCheckpoint']=point;d['rollSpenders'][event['id']]=item_id
    d['rollEffects'][event['id']]={'advantageGranted':True,'sourcePhysicalItem':item_id,'sameEventSecondExpenditureAllowed':False,'scope':'ordinary cancellation and replacement procedure govern dice'}
    return d

def dawn(ledger,item_id,index,at_time,actual_state_at_event,*,checkpoint):
    if not isinstance(index,int) or index<0 or at_time!=ledger['epoch']+index*86400:raise ValueError('not an authoritative dawn event')
    s=ledger['items'][item_id]
    point=checked_checkpoint(ledger,checkpoint,at_time)
    if point['processedDawnThrough']!=index:raise ValueError('dawn checkpoint index mismatch')
    require_later(s,point)
    if at_time<s['createdAt']:raise ValueError('dawn predates imprint')
    if s['lastDawn'] is not None and index<=s['lastDawn']:raise ValueError('replayed or out-of-order dawn')
    if actual_state_at_event.get('id')!=item_id or actual_state_at_event.get('recordedAt')!=at_time:raise ValueError('missing actual event-state history')
    if any(k not in actual_state_at_event for k in ('complete','hp','suppressed','primaryDestroyed')):raise ValueError('incomplete historical state')
    if s['lastDawn'] is not None and index!=s['lastDawn']+1:raise ValueError('resolve intervening dawn states first')
    first=max(0,ceil(F(s['createdAt']-ledger['epoch'],86400)))
    if s['lastDawn'] is None and index!=first:raise ValueError('resolve first elapsed dawn before later events')
    state=actual_state_at_event
    eligible=(state.get('complete') and state.get('hp',0)>0 and not state.get('suppressed') and not state.get('primaryDestroyed'))
    d=deepcopy(ledger);z=d['items'][item_id];z['lastDawn']=index;z['lastCheckpoint']=point;z['dawnEvents'].append({'index':index,'time':at_time,'checkpoint':point,'refilled':bool(eligible),'state':deepcopy(state)})
    if eligible:z['current']=z['maximum']
    return d

def complete_order(reserves,recipe,outcome,option,declared_ids):
    """Latest-state inputs must retain their predeclared physical ordering."""
    if [r['id'] for r in reserves]!=declared_ids:raise ValueError('changed reserve order or identity')
    expected='jewelcrafting.'+('mounted-gem' if recipe['recipeFamily']=='Gem' else recipe['recipeFamily'].lower())
    for r in reserves:
        if r.get('model')!=expected or r.get('grade')!='Standard' or r.get('size') not in ('Tiny','Small','Medium','Large'):raise ValueError('unadmitted body')
        if r.get('complete') is not True or r.get('available') is not True or r.get('otherMagicalAlteration'):raise ValueError('body premise missing')
        ordinary=10 if r['size']=='Large' else 5
        if r.get('ordinaryHP')!=ordinary or r.get('maximum')!=structural_maximum(ordinary,r['percent'],r['flaw']):raise ValueError('body structural record inconsistent')
    if option not in ('yield','durability'):raise ValueError('no charge improvement option')
    return leather.complete_order(reserves,recipe['quantity'],outcome,option)

def catalyst_return(recipe,actual_units,outcome,selected_ids):
    """Select the one actual participant returned; not a harvest/aging engine."""
    if len(selected_ids)>1 or len(set(u['id'] for u in actual_units))!=len(actual_units):raise ValueError('nonunique unit or too many returns')
    if not selected_ids:return []
    if outcome!='Masterwork':raise ValueError('only actual Masterwork returns catalyst')
    selected=[u for u in actual_units if u['id'] in selected_ids]
    if len(selected)!=1:raise ValueError('actual unit absent')
    u=selected[0];i=u['componentIndex']
    if u.get('recipeId')!=recipe['id'] or not isinstance(i,int) or not 0<=i<len(recipe['components']):raise ValueError('wrong recipe participation')
    component=recipe['components'][i]
    if component['role']!='catalyst' or not component['consumed'] or u.get('componentId')!=component['id']:raise ValueError('not an actual eligible catalyst occurrence')
    if not u.get('lawfullyPreservedParticipant') or u.get('alreadyDestroyed'):raise ValueError('cannot manufacture a replacement participant')
    return deepcopy(selected)

def structural_maximum(ordinary,percent=0,flawed=False):
    if ordinary not in (5,10) or percent not in (0,25,50):raise ValueError('unadmitted structural premise')
    improved=ordinary+(max(1,ordinary*percent//100) if percent else 0)
    return max(1,improved//2) if flawed else improved

def quality_structure(ordinary,old_percent,old_flawed,old_current,new_percent=0,add_flaw=False):
    oldmax=structural_maximum(ordinary,old_percent,old_flawed)
    if not 1<=old_current<=oldmax:raise ValueError('reserve must be functional at completion')
    percent=max(old_percent,new_percent);flaw=old_flawed or add_flaw;maximum=structural_maximum(ordinary,percent,flaw)
    return {'maximum':maximum,'current':max(0,min(maximum,maximum-(oldmax-old_current))),'durabilityPercent':percent,'flawed':flaw}

def repair_quote(item,base_value,finished_value,recipe_dc,premises):
    """Return a quotation only after supplied original-assembly/tool gates.
    No clock, material inventory, actual work or charge ledger is mutated.
    """
    required=['trained','actualToolkit','actualBench','actualFineFiles','actualLens','recoverableOriginalPrimary','requiredOriginalStonesSettingsPresent']
    if any(premises.get(k) is not True for k in required):raise ValueError('missing actual repair premise')
    if premises.get('ability') not in ('DEX','INT'):raise ValueError('choose DEX or INT')
    if item['family']=='Gem' and not (premises.get('originalCrystal') and premises.get('originalPrimaryMount')):raise ValueError('original Gem assembly missing')
    return leather.repair_terms(item['hp'],item['maximumHP'],base_value,finished_value,recipe_dc,recoverable=True)
