"""Add concrete scoped defense options and fix fixture-only class labels before conference."""
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def apportion(parts,reduction):
 total=sum(parts.values());budget=min(reduction,total)
 if not total:return dict(parts),{k:0 for k in parts}
 exact={k:Fraction(budget*x,total) for k,x in parts.items()};allocated={k:x.numerator//x.denominator for k,x in exact.items()}
 order=sorted(parts,key=lambda k:(-(exact[k]-allocated[k]),k))
 for k in order[:budget-sum(allocated.values())]:allocated[k]+=1
 return {k:x-allocated[k] for k,x in parts.items()},allocated

def main():
 oldp=R/'data/director/spell_proposals/damage_control_25_current_03.json';out=oldp.with_name('damage_control_25_current_04.json');report=A/'DAMAGE_CONTROL_25_CONFERENCE_OPTIONS_CHECK_04.json'
 assert not out.exists() and not report.exists();old=read(oldp);d=deepcopy(old);checks=[]
 def ck(label,ok):checks.append({'check':label,'passed':bool(ok)});assert ok,label
 correction=[]
 for c in d['currentDigitalVectors']:
  b=c['lawfulOriginalCastContext']
  if b['castingClass']!='Mage' and b['MageFocus'] is not None:
   correction.append({'caseId':c['id'],'before':b['MageFocus'],'after':None,'reason':'Fixture label only: this Wizard has no Mage Focus; no Focus bonus was applied.'});b['MageFocus']=None
 for s in d['spells']:
  if s['id']=='destructive-wave':s['unresolvedDecisionIds']=[x for x in s['unresolvedDecisionIds'] if x!='DC25-MIXED-DEFENSE-01']
 option='''NEW DC25-MIXED-DEFENSE-02, proposed ONLY for Meteor Spear's one mixed fire/bludgeoning packet. This supplies a deterministic distribution for an already legally applicable aggregate flat reduction; it does not grant a defense or change a defense source's applicability, strongest-source selection, use count, before/after-resistance timing or trigger. Resolve each typed raw amount's stated save rounding first. At an actual aggregate reduction stage, use its remaining eligible typed amounts and let B=min(the one applicable reduction, sum of those eligible amounts). Allocate B proportionally to those amounts using exact rational shares. Give each type its floor share, then distribute the remaining integer points to the largest fractional remainders; exact ties use canonical damage-type ID in lexical order fixed before the event. Aggregate all entries of the same type before allocating, so splitting a type into dice/rows cannot change allocation. Clamp no component below0. An amount already0 receives no allocation. No player chooses which type receives reduction and no allocation is optimized using a later resistance/immunity result.

For an ordinary strongest applicable class flat reduction use the accepted class stage before resistance/immunity; then apply each actual typed defense and its integer rounding. A source explicitly saying after resistance retains that stage instead. Never apply one source's flat amount once per component. This proposal does not decide how two different candidate defenses compete if their actual accepted sources leave that interaction undefined; report that source conflict separately. Keep residual typed lineage through any actual later prevention/transfer, then one grouped original-recipient HP/Wound/zero event. It supplies no second Wound save, split hit, copied payment, new cast or fresh Null root. Any wider use by other mixed-damage sources requires an explicit separately scoped extension.'''
 d['mixedDefenseConferenceOption04']={'id':'DC25-MIXED-DEFENSE-02','status':'Concrete NEW unadopted option, not an accepted global defense rule','completeProposedText':option,'whyNeeded':'Current class guide orders strongest ordinary flat reduction before resistance, and actual Warrior Spinal Plating explicitly acts after resistance. The sources found do not allocate a single aggregate reduction among simultaneous Meteor Spear damage types. The existing mixed resistance case with no flat DR remains unchanged.','actualSourceRefs':[{'path':(R/'docs/mechanics/CLASS_PLAYTEST_RULES.md').relative_to(G).as_posix(),'section':'Shared damage/condition integration: strongest flat reduction then resistance'},{'path':(R/'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md').relative_to(G).as_posix(),'section':'Actual original-target defenses and typed transfer'},{'path':(R/'data/public/class_playtests/warrior.json').relative_to(G).as_posix(),'pointer':'/cards/11','name':'Brutal Fortitude'},{'path':(R/'data/public/class_playtests/warrior.json').relative_to(G).as_posix(),'pointer':'/cards/15','name':'Adaptive Tissue'},{'path':(R/'data/public/class_playtests/warrior.json').relative_to(G).as_posix(),'pointer':'/cards/105','name':'Spinal Plating'}],'notYetIntegratedIntoSpellProcedure':True}
 a,aa=apportion({'fire':14,'bludgeoning':5},3);ck('Pre-resistance allocation',a=={'fire':12,'bludgeoning':4} and aa=={'fire':2,'bludgeoning':1});ck('Pre-resistance final damage',a['fire']//2+a['bludgeoning']==10)
 b,ba=apportion({'fire':7,'bludgeoning':5},2);ck('Explicit post-resistance allocation',b=={'fire':6,'bludgeoning':4} and ba=={'fire':1,'bludgeoning':1})
 _,zero=apportion({'fire':0,'bludgeoning':5},3);ck('Zero component no allocation',zero=={'fire':0,'bludgeoning':3})
 z,zz=apportion({'fire':14,'bludgeoning':5},100);ck('Capped reduction never negative',z=={'fire':0,'bludgeoning':0} and sum(zz.values())==19)
 t,tt=apportion({'fire':5,'bludgeoning':5},1);ck('Stable tie independent of insertion',tt=={'fire':0,'bludgeoning':1} and apportion({'bludgeoning':5,'fire':5},1)[1]==tt)
 d['mixedDefenseOptionVectors04']=[{'id':'DC25-MIX-01','initialState':{'target':'Warrior10 with acquired Brutal Fortitude and Adaptive Tissue','BT':3,'BrutalFortitudeDR':3,'AdaptiveTissueResistance':'fire, from a real preceding fire critical; no intervening replacement/rest','otherDamageModifiers':None,'targetDEX':'success','MeteorRaw':{'fire':29,'bludgeoning':11},'maxHP':105,'currentHP':105,'temporaryHP':0,'Wounds':0,'sourceDC':16},'expected':{'postSave':{'fire':14,'bludgeoning':5},'oneDRAllocation':aa,'afterDR':a,'afterResistance':{'fire':6,'bludgeoning':4},'groupedDamage':10,'currentHP':95,'WoundSaves':0,'originalRecipientDamageEvents':1}}, {'id':'DC25-MIX-02','initialState':{'target':'Independent Warrior10 with acquired/equipped operative Spinal Plating and prior Adaptive Tissue fire resistance','BT':0,'BrutalFortitudeDR':0,'SpinalPlating':{'amount':2,'stage':'after resistance','sourcePredicate':'actual area effect'},'targetDEX':'success','MeteorRaw':{'fire':29,'bludgeoning':11},'otherDamageModifiers':None},'expected':{'postSave':{'fire':14,'bludgeoning':5},'afterResistanceBeforeSpinal':{'fire':7,'bludgeoning':5},'onePostResistanceAllocation':ba,'finalTyped':b,'groupedDamage':10,'SpinalApplications':1}}, {'id':'DC25-MIX-03','initialState':{'typedAmountsAtStage':{'fire':5,'bludgeoning':5},'aggregateReduction':1,'laterFireImmunity':True,'typeOrderInput':['fire','bludgeoning']},'expected':{'reductionAllocated':tt,'beforeImmunity':t,'afterImmunity':{'fire':0,'bludgeoning':4},'reorderingInputChangesResult':False,'sourceStageMoved':False},'scope':'Mathematical allocation edge only; no new actor immunity is granted.'}]
 for c in d['conferenceDecisions']:
  if c['id']=='DC25-MIXED-DEFENSE-01':c.update(status='Existing source constraint plus concrete scoped option supplied for conference',proposal=option,nextRequiredWork='GPT disposition on DC25-MIXED-DEFENSE-02; then exact spell/source-specific integration, additional transfer/prevention vectors if required. Do not mark this accepted merely because allocation arithmetic passes.')
 d['digitalFixtureLabelCorrections04']=correction;d['previousCompleteDraft']=info(oldp);d.update(id='DAMAGE-CONTROL-25-CURRENT-04',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='UNADOPTED25-spell consolidated conference candidate;36 original examples mapped to digital vectors,10 other current cases,32 preserved alternatives. Concrete mixed-defense option remains unintegrated pending conference. Ice and other source-specific semantic choices remain pending.')
 for p in [oldp,R/'data/public/class_playtests/warrior.json']:
  if p.relative_to(G).as_posix() not in {x['path'] for x in d['sourceBindings']}:d['sourceBindings'].append(info(p))
 for x in d['sourceBindings']:ck('Exact current source '+x['path'],info(G/x['path'])==x)
 ck('All36 original cases retained',d['originalCohortCasesUnchanged']==old['originalCohortCasesUnchanged'])
 ck('No original procedure changed',all(a['procedure']==b['procedure'] for a,b in zip(d['spells'],old['spells'])))
 out.write_bytes(encoded(d));report.write_bytes(encoded({'draft':info(out),'checks':checks,'checkCount':len(checks),'failureCount':0,'fixtureLabelCorrections':correction,'sourceCount':len(d['sourceBindings']),'originalSpellProcedureChanges':0,'proposedScopedDefenseOption':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'scope':'Exact source/preservation and rational arithmetic for an unadopted option. No actual defense or game-engine execution.'}));print(json.dumps(read(report)|{'checks':'see report'}))

if __name__=='__main__':main()
