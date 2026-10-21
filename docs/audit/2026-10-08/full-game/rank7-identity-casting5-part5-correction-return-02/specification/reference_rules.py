"""Isolated Rank7 authoring specifications. NOT project/game-runtime modules.

Only finite pure functions and explicit fixture operands are evaluated. Passing
these checks cannot establish actor acquisition, live geometry, a real action
opportunity, scheduler integration, persistence or encounter reachability.
"""
from copy import deepcopy
from math import isfinite
RP=(0,2,3,5,7,10,13,17,21,26)

def legal_original(*,age,resolved,observed,rank,descended=False,wrapper=False):
    return 0<=age<=18 and resolved and observed and 0<=rank<=9 and not descended and not wrapper

def cast_quote(rank,d,limit=11,extra=0):
    if not 0<=rank<=9 or extra<0:raise ValueError('Invalid source price')
    if rank and d>=limit+6:raise ValueError('Ranked casting blocked')
    sur=0 if rank==0 or d<limit else 1+(d-limit)//3
    return RP[rank]+sur+extra

def history(d,last,refrain,name,rank,first_matrix=False):
    nxt=min(3,refrain+1) if name==last else 0
    base=0 if rank==0 or first_matrix else (1 if rank<=5 else 2)
    return d+base+nxt,name,nxt

def echo_forecast(rp,d,child_rank,outer_first=True,last=None,refrain=0,child_extra=0):
    outer=cast_quote(7,d)
    d1,_,_=history(d,last,refrain,'cast-echo',7,outer_first)
    child=cast_quote(child_rank,d1,extra=child_extra)
    if rp<outer+child:raise ValueError('Combined shortfall')
    return {'outer':outer,'child':child,'outerD':d1,'remaining':rp-outer-child}

def complete_outer(rp,quote,countered=False):
    return {'rp':rp-quote['outer'],'childReservation':0 if countered else quote['child'],'childCommitted':False}

def commit_child(rp,d,rank,extra=0,blocked=False):
    if blocked:return {'rp':rp,'committed':False}
    cost=cast_quote(rank,d,extra=extra)
    if cost>rp:return {'rp':rp,'committed':False}
    return {'rp':rp-cost,'committed':True,'cost':cost}

def ready_release(now,deadline,*,reaction,concentration,source_legal,target_legal,perceived_trigger,child_kind='Action',native_window=False,trigger_completed=True):
    if now>=deadline or not all((reaction,concentration,source_legal,target_legal,perceived_trigger)):return False
    return native_window if child_kind=='Reaction' else trigger_completed

def long_completion(start,native_seconds,work_continuous=True,concentration=True):
    return start+native_seconds if work_continuous and concentration else None

def meta_commit(*,acquired,available,active_surge,mode_count=1,spell_price=0):
    if not acquired or mode_count!=1:raise ValueError('No source/mode permission')
    if not active_surge and available<1:raise ValueError('No charge')
    return {'spellCost':spell_price,'remaining':available if active_surge else available-1,'waivedAtCommitment':active_surge}

def masks_for(snapshot,recipient,perceivers):
    return {k:{eid for eid,v in snapshot.get(k,{}).items() if v['subject']==recipient} for k,v in perceivers.items() if k!=recipient and v['distance']<=120 and v['los'] and v['perceived']}

def recall(episodes,masks):
    covered=set().union(*masks) if masks else set()
    return {k:v for k,v in episodes.items() if k not in covered}

def erase_select(*,active,direct_new,existing=False,area=False):
    return not(active and direct_new and not existing and not area)

def seq_admit(now,deadline,willing,hard_free,inc_immune=False):
    return isfinite(deadline) and deadline>now and willing and hard_free and not inc_immune

def suspension_advance(bio,elapsed,deadline_remaining):
    if elapsed<0:raise ValueError('Backward time')
    return {'bio':deepcopy(bio),'worldElapsed':elapsed,'sourceRemaining':max(0,deadline_remaining-elapsed),'restCredit':0}

def seq_damage(hp,temp,post_defense):
    if post_defense<0:raise ValueError('Negative damage')
    used=min(temp,post_defense);loss=min(hp,post_defense-used)
    return {'hp':hp-loss,'temp':temp-used,'awake':post_defense>0,'damageEvent':post_defense}

def source_mask_end(episodes,source_masks,ending_id):
    masks={k:v for k,v in source_masks.items() if k!=ending_id}
    return recall(episodes,list(masks.values()))

def derivative_account(creator,donor,current,old=None):
    n=deepcopy(current);n['key']=(creator,donor)
    if old is not None:
        n['rp']=min(old['rp'],current['rp'],current['maxRp'])
        n['d']=max(old['d'],current['d']);n['cooldown']=max(old['cooldown'],current['cooldown'])
        n['last']=old['last'];n['refrain']=old['refrain'];n['used']=set(old['used'])|set(current['used'])
    return n

def create_body(donor,rp_after_payment,*,self_copy=False):
    if donor['actualDead']:return None
    n={k:deepcopy(donor[k]) for k in ('hp','maxHp','size','mass','wounds','critical','injury')}
    if n['hp']==0:return {'state':'immediate-finite-ending','liveReplacement':False,'loot':False}
    n.update(rp=rp_after_payment if self_copy else donor['rp'],state='active',temporaryHP=0,concentration=None,liveReplacement=True)
    return n

def replacement(old,new,paid=True):
    return new if paid and new and new.get('liveReplacement') else old

def active_rest(account,*,active,safe,supplied,beneficial_budget,hours):
    n=deepcopy(account)
    if all((active,safe,supplied,beneficial_budget)) and hours>=8:
        n.update(rp=n['maxRp'],d=0,last=None,refrain=0,used=set())
    return n

def projectile(ammo,*,lawful,offered_for_transfer=False):
    if offered_for_transfer:return {'ammo':ammo,'exists':False,'attack':False}
    if not lawful or ammo<=0:return {'ammo':ammo,'exists':False,'attack':False}
    return {'ammo':ammo-1,'existsThroughResolution':True,'endsAfterResolution':True,'recoverable':False,'attack':True}

def body_interiors_overlap(a,b,half=2.5):
    return all(abs(x-y)<2*half for x,y in zip(a,b))

def carrying(weight,load,strength,base_speed=30):
    if weight>15*strength or load>strength:raise ValueError('Over actual cap')
    return base_speed-10 if load>0 and load>=strength/2 else base_speed

def task_success(natural,modifier,dc):
    delta=natural+modifier-dc
    degree=2 if delta>=10 else 1 if delta>=0 else -2 if delta<=-10 else -1
    order=[-2,-1,1,2];j=order.index(degree)
    if natural==20:j=min(3,j+1)
    elif natural==1:j=max(0,j-1)
    return order[j]>0

def exact_mode_quote(rank,d,*,replacement_price=None,actual_class_entitlement=False,recharge=0):
    price=cast_quote(rank,d)
    if replacement_price is None:return price
    if not actual_class_entitlement or recharge>0:raise ValueError('Missing actual class-mode credential or available recharge')
    return price-RP[rank]+replacement_price
