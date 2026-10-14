"""Bounded manuscript calculations, not companion-runtime implementation.

Actual task circumstances, physical fit, anatomy, tool equivalence and board
placement are explicit premises established by their governing procedures.
"""
from copy import deepcopy
from fractions import Fraction as F
from math import ceil
import leatherworking_reference as lw
from build_tailoring_recipe_candidate import FAMILY_TASKS, SLOTS

def inventory(records,bearer):
    transformed=deepcopy(records)
    for r in transformed:
        if r.get('family')=='Bag':
            cap=r['bodyCapacityLb']
            if cap not in (10,30,40,50):raise ValueError('unadmitted Bag model')
            r['family']='Pouch' if cap==10 else 'Backpack'
    return lw.inventory(transformed,bearer)

def wearing_eligible(r):
    return (r.get('state')=='worn' and r.get('complete',False)
        and r.get('hp',0)>=1 and not r.get('suppressed',False)
        and r.get('fit',False) and r.get('slotValid',False))

def validate_designated_slots(items):
    occupied={}
    for r in items:
        # Broken and suppressed bodies do not automatically vacate a designation.
        if r.get('state')!='worn' or not r.get('slotValid'):continue
        slot=r.get('slot')
        if r.get('trade')=='Tailoring' and r.get('family')!='Bag':
            if slot!=SLOTS[r['family']]:raise ValueError('incorrect Tailoring position')
        key=(r.get('wearer'),slot)
        if key in occupied:raise ValueError('competing designated benefits')
        occupied[key]=r['id']
    return occupied

def tailoring_task_bonus(items,task):
    if not task.get('actualCheck') or task.get('kind')!='ability-check':return 0
    domain=task['domain']
    if not task.get('domainCriteriaMet') or not task.get('actualContribution'):return 0
    ability=task['ability'];proficiency=task.get('proficiency')
    valid={
      'presentation':(ability=='CHA' and proficiency in ('Persuasion','Deception','Performance') and task.get('visibleAttire')) or (ability=='DEX' and proficiency=='disguise-kit' and task.get('ownAlreadyWornArrangement')),
      'visual-concealment':ability=='DEX' and proficiency=='Stealth' and task.get('legalHiding'),
      'quiet-clothing-motion':ability=='DEX' and proficiency=='Stealth',
      'discreet-handwork':ability=='DEX' and proficiency=='Sleight of Hand',
      'weather-arrangement':(ability=='WIS' and proficiency=='Survival') or (ability=='DEX' and task.get('ownOrdinaryFastenings')),
      'exposure':ability=='CON' and task.get('independentExposureProcedureAllowsClothing'),
      'conceal-contents':ability=='DEX' and task.get('noncreatureCargo'),
      'organize-contents':ability in ('INT','DEX') and task.get('noncreatureCargo')}
    if not valid.get(domain,False):return 0
    scores=[]
    for r in items:
        if r.get('trade')!='Tailoring' or domain not in FAMILY_TASKS[r['family']]:continue
        if r['family']=='Bag':
            eligible=(r.get('complete') and r.get('hp',0)>=1 and not r.get('suppressed')
              and r.get('state')!='melded' and r.get('accessible')
              and r.get('operator')==task.get('actor'))
        else:
            eligible=wearing_eligible(r) and r.get('wearer')==task.get('actor') and task.get('coverageSufficient')
        if eligible:scores.append(r['bonus'])
    return max(scores,default=0)

def cross_trade_task_bonus(items,task,leather_task_ids=()):
    """Both domain sets must describe this same independently required check."""
    validate_designated_slots(items)
    tailoring=tailoring_task_bonus(items,task)
    leather=[r for r in items if r.get('trade')=='Leatherworking']
    leather_score=0
    if task.get('kind')=='ability-check' and task.get('actualCheck') and task.get('leatherCriteriaMet'):
        eligible=[r for r in leather if r.get('wearer',r.get('operator'))==task.get('actor')]
        leather_score=lw.task_bonus(eligible,True,set(leather_task_ids),task.get('noncreatureCargo',True))
    return max(tailoring,leather_score)

def defense(suit_grade,items):
    validate_designated_slots(items)
    # Tailoring is absent from the AC candidate set, including when all items fail.
    rest=[r for r in items if r.get('trade')!='Tailoring']
    result=lw.defense(suit_grade,rest)
    resistances=set(result['resistances'])
    for r in items:
        if r.get('trade')=='Tailoring' and wearing_eligible(r) and r.get('resistance'):
            resistances.add(r['resistance'])
    result['resistances']=sorted(resistances)
    return result

def repair_terms(current,maximum,base_value,finished_value,dc,original_body=True,
                 required_constituents_present=True):
    if not required_constituents_present:raise ValueError('missing original member/constituent')
    return lw.repair_terms(current,maximum,base_value,finished_value,dc,recoverable=original_body)

def tool_reservation(tool_id,active_order_ids,new_order_id,qualified_profile):
    if not qualified_profile:raise ValueError('source profile or legal substitute absent')
    if set(active_order_ids)-{new_order_id}:raise ValueError('tool reserved for overlapping work')
    return {'physicalToolId':tool_id,'orderId':new_order_id}

def creation_minutes(source_hours,forge_dwarf=False):
    actual=F(1920) if source_hours is None else F(str(source_hours))
    return ceil(actual*(45 if forge_dwarf else 60))

def purchase_cp(reference_gp):
    return ceil(F(str(reference_gp))*100)

