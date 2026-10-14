"""Bounded reference calculations for the authored Leatherworking manuscript.

Not the companion runtime. Physical fit/anatomy/permissions are explicit premises.
Box helpers prove specified orthogonal packing only, not arbitrary 3-D fitting.
"""
from fractions import Fraction as F
from itertools import permutations
from copy import deepcopy

SLOT_FAMILY={'back-cargo':{'Backpack','Harness'},'quiver':{'Quiver'},
             'waist-cargo':{'Belt'},'pouch-1':{'Pouch'},'pouch-2':{'Pouch'}}

def number(n): return F(str(n))

def custody(records):
    """Require an acyclic forest with one node and one parent per physical ID."""
    by={r['id']:r for r in records}
    if len(by)!=len(records): raise ValueError('duplicate physical identity')
    parent={}
    for r in records:
        if r.get('inclusiveGross') and r.get('contents'): raise ValueError('inclusive record also expanded')
        for child in r.get('contents',[]):
            if child not in by: raise ValueError('missing physical record')
            if child in parent: raise ValueError('multiple custody parents')
            parent[child]=r['id']
    done=set();visiting=set()
    def visit(id):
        if id in visiting: raise ValueError('cyclic custody')
        if id in done: return
        visiting.add(id)
        for child in by[id].get('contents',[]):visit(child)
        visiting.remove(id);done.add(id)
    for id in by:visit(id)
    return by,parent

def subtree(by,id):
    yield id
    for child in by[id].get('contents',[]):yield from subtree(by,child)

def inventory(records,bearer):
    by,parent=custody(records)
    roots=[r['id'] for r in records if r['id'] not in parent and r.get('bearer')==bearer]
    allids=[id for root in roots for id in subtree(by,root)]
    active=[];occupied={}
    for id in roots:
        r=by[id];slot=r.get('slot')
        # Invalid/incomplete held/worn assemblies never create magical permission.
        equipped=(r.get('state') in ('worn','held') and r.get('fit',False)
                  and (r.get('state')!='held' or r.get('handsSatisfied',False)))
        if equipped and slot in SLOT_FAMILY and r.get('family') in SLOT_FAMILY[slot]:
            if slot in occupied: raise ValueError('two occupants designated in one relief slot')
            occupied[slot]=id
            if r.get('hp',0)>=1 and not r.get('suppressed') and r.get('complete',True) and 'relief' in r: active.append(id)
    pounds=F(0);load=F(0);unknown=[]
    for id in allids:
        r=by[id];load+=number(r['load'])
        if r.get('weight') is None:unknown.append(id)
        else:pounds+=number(r['weight'])
    coverage={};credits={}
    for id in active:
        allowance=number(by[id]['relief'])
        for child in by[id].get('contents',[]):
            for cid in subtree(by,child):
                r=by[cid]
                if r.get('creatureBody') or r.get('weight') is None: continue
                # Every descendant belongs to only this root; body precedes children.
                covered=min(allowance,number(r['weight']));allowance-=covered
                coverage[cid]=covered;credits[cid]=min(number(r['load']),covered/10)
    return {'physicalPounds':None if unknown else pounds,'knownPoundsSubtotal':pounds,
      'canonicalLoad':load,'unknownWeightIds':unknown,'activeContainers':active,
      'coveredPoundsById':coverage,'loadCreditById':credits,
      'countedPounds':None if unknown else pounds-sum(coverage.values(),F(0)),
      'effectiveLoad':load-sum(credits.values(),F(0)),'physicalIds':allids}

def transfer(records,root,new_bearer,state='carried',slot=None,fit=False,hands=False):
    result=deepcopy(records);by,parent=custody(result)
    if root in parent: raise ValueError('remove from containing custody before direct transfer')
    by[root].update(bearer=new_bearer,state=state,slot=slot,fit=fit,handsSatisfied=hands)
    return result

def break_container(records,id,retained=(),same_location_legal=True,adjacent_legal=True):
    """Placement premises are supplied by the reviewed board/placement system."""
    result=deepcopy(records);by,parent=custody(result);r=by[id];r['hp']=0
    old=list(r.get('contents',[]));r['contents']=[]
    # retained maps children to independently recorded supporting parent IDs.
    retained=dict(retained);released=[]
    for child in old:
        if child in retained:
            support=by[retained[child]]
            if support['id']==id or support.get('hp',0)<1 or not support.get('independentSupport'):
                raise ValueError('no genuine independent intact restraint')
            support.setdefault('contents',[]).append(child);continue
        by[child].update(bearer=None,slot=None,state='placed' if same_location_legal or adjacent_legal else 'pending-placement',
                         location=r.get('location') if same_location_legal else 'nearest-legal-adjacent' if adjacent_legal else None)
        released.append(child)
    custody(result)
    return result,released

def maximum_hp(ordinary,percent=0,flawed=False):
    if ordinary<1 or percent not in (0,25,50):raise ValueError('invalid structural layer')
    improved=ordinary+(max(1,ordinary*percent//100) if percent else 0)
    return max(1,improved//2) if flawed else improved

def apply_quality(ordinary,old_percent,old_flaw,old_current,new_percent=0,new_flaw=False):
    oldmax=maximum_hp(ordinary,old_percent,old_flaw)
    if not 0<=old_current<=oldmax:raise ValueError('invalid current structural HP')
    p=max(old_percent,new_percent);flaw=old_flaw or new_flaw;newmax=maximum_hp(ordinary,p,flaw)
    return {'ordinaryHP':ordinary,'percent':p,'flaw':flaw,'maximum':newmax,'current':max(0,newmax-(oldmax-old_current))}

def complete_order(reserves,q,outcome,option='yield'):
    """Reserves are the latest lawful completion records in predeclared order."""
    if len(reserves)!=3*q//2:raise ValueError('wrong maximum reserve count')
    if len({r['id'] for r in reserves})!=len(reserves):raise ValueError('shared body')
    for r in reserves:
        if r.get('missing') or r.get('committedElsewhere') or r.get('imprint') or not r.get('complete',True) or r['current']<1 or r.get('contents'):
            raise ValueError('pause before completion check')
    if len({(r['model'],r['size'],r['grade']) for r in reserves})!=1:raise ValueError('batch model size grade differs')
    n={'Standard':q,'Exceptional':5*q//4,'Masterwork':3*q//2,'Flawed':q//2 if q>=2 else 1,'Failed':0,'Mishap':0}[outcome]
    pct=0
    if outcome in ('Exceptional','Masterwork') and option=='durability':n=q;pct=25 if outcome=='Exceptional' else 50
    output=[]
    for r in reserves[:n]:
        z=deepcopy(r);z.update(apply_quality(r['ordinaryHP'],r['percent'],r['flaw'],r['current'],pct,outcome=='Flawed' and q==1));z['imprint']=True;output.append(z)
    return output,deepcopy(reserves[n:])

def repair_terms(current,maximum,base_value,finished_value,dc,pair=False,recoverable=True,both_members=True):
    if not recoverable or pair and not both_members:raise ValueError('generic reconstruction unavailable')
    if not 0<=current<=maximum:raise ValueError('invalid HP')
    return {'DC':10 if current>=1 else dc,'hours':max(F(1 if current>=1 else 8),F(maximum,10)),
            'materialsGp':number(base_value if current>=1 else finished_value)/4,'restoredMaximum':maximum}

def defense(suit_grade,items):
    candidates=[] if suit_grade is None else [suit_grade];res=set()
    for r in items:
        worn=r.get('state')=='worn' and r.get('fit') and r.get('complete') and r.get('hp',0)>=1 and not r.get('suppressed') and (r.get('family')=='Armor' or r.get('slotValid'))
        if not worn:continue
        if r.get('resistance'):res.add(r['resistance'])
        if r.get('armorBonus',0)>0 and (r.get('family')!='Armor' or r.get('selectedArmorFormula')):
            candidates.append(r['armorBonus'])
    return {'enhancement':max(candidates) if candidates else None,'resistances':sorted(res)}

TASK_IDS={
 'Boots':{'foothold-climb','checked-jump','foot-balance'},
 'Gloves':{'handhold-climb','rope-grip','manual-cargo-retention','manual-cargo-position','nonlocking-fitting','jammed-small-object'},
 'Leather Gear':{'climb','checked-cramped-passage'},
 'Armor':{'climb','checked-cramped-passage'},'Coat':{'climb','checked-cramped-passage'},
 'container':{'secure-closure','cargo-handling','unlocked-retrieval','jammed-content','tangled-content'}}

def task_bonus(items,actual_check,task_ids,physical_noncreature=True):
    if not actual_check or not physical_noncreature:return 0
    candidates=[]
    for r in items:
        family=r['family'];container=family in ('Backpack','Pouch','Quiver','Belt','Harness')
        state=(r.get('accessible') and r.get('state')!='melded') if container else (r.get('state')=='worn' and r.get('slotValid') and r.get('fit'))
        if state and r.get('complete') and r.get('hp',0)>=1 and not r.get('suppressed') and TASK_IDS['container' if container else family].intersection(task_ids):candidates.append(r['bonus'])
    return max(candidates,default=0)

def orthogonal_box_fit(dimensions,interior,opening,opening_axes=(1,2)):
    """Existence proof for a rigid box in one orthogonal loading orientation."""
    return any(all(a<=b for a,b in zip(p,interior)) and p[opening_axes[0]]<=opening[0] and p[opening_axes[1]]<=opening[1]
               for p in set(permutations(dimensions)))

def compartment_limits(model,placements):
    """Check explicit non-overlapping orthogonal placements; no packing search."""
    count=model['compartmentCount'];totw=F(0);totv=F(0)
    volume=lambda d:F(d['numerator'],d['denominator'])
    for i in range(count):
        ps=[p for p in placements if p['compartment']==i]
        if any(not orthogonal_box_fit(p['dimensions'],model['interiorInches'],model['openingInches'],model['openingAxes']) for p in ps):return False
        if any(any(x<0 or x+d>limit for x,d,limit in zip(p['position'],p['dimensions'],model['interiorInches'])) for p in ps):return False
        for a_index,a in enumerate(ps):
            for b in ps[a_index+1:]:
                if all(a['position'][k]<b['position'][k]+b['dimensions'][k] and b['position'][k]<a['position'][k]+a['dimensions'][k] for k in range(3)):return False
        w=sum((number(p['weight']) for p in ps),F(0));v=sum((number(p['volumeFt3']) for p in ps),F(0))
        if w>model['compartmentWeightLimitLb'] or v>volume(model['compartmentVolumeFt3']):return False
        totw+=w;totv+=v
    return (all(0<=p['compartment']<count for p in placements) and totw<=model['physicalContentWeightLimitLb'] and totv<=volume(model['physicalContentVolumeFt3']))

def meld_preflight(records,root_ids,pound_ceiling,load_ceiling):
    by,_=custody(records);seen=set()
    for id in root_ids:
        ids=set(subtree(by,id))
        if seen.intersection(ids):raise ValueError('subtree selected twice')
        seen.update(ids)
    if any(by[id].get('weight') is None for id in seen):raise ValueError('known mass required for meld preflight')
    pounds=sum((number(by[id]['weight']) for id in seen),F(0));load=sum((number(by[id]['load']) for id in seen),F(0))
    return {'pounds':pounds,'load':load,'fits':pounds<=number(pound_ceiling) and load<=number(load_ceiling),'physicalIds':sorted(seen)}
