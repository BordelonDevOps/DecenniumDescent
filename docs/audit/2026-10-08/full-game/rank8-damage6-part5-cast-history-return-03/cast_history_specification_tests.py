#!/usr/bin/env python3
"""Isolated Dimensional Anchor fixture specifications, not a game engine.

Only this already-acquired Wizard7 prepared spell is modeled. Initiative, perception,
line of effect, component availability and lack of interrupts are explicit fixture
inputs; this script neither proves their runtime reachability nor grants them.
"""
from __future__ import annotations
import argparse
import copy
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent

def load(name):
    return json.loads((ROOT/name).read_bytes())

def canonical_name(name):
    return str(name or '').lower().replace(' ', '-')

def price_and_cadence(actor):
    """Actual rank4 Anchor only; no optional discounts or traumatic exception."""
    modifier=(actor['abilityScores']['INT']-10)//2
    limit=max(4,2+actor['PB']+max(0,modifier))
    before=actor['Dissonance']
    if before>=limit+6:
        raise ValueError('Ordinary ranked cast blocked')
    surcharge=2 if before>=limit+3 else 1 if before>=limit else 0
    same=canonical_name(actor['previousSpell'])=='dimensional-anchor'
    repeat=min(3,actor['Refrain']+1) if same else 0
    base=1 if 'dimensional-anchor' in actor['matrixFamiliesUsed'] else 0
    return {'limit':limit,'RPcost':7+surcharge,'base':base,'repeat':repeat,
            'DissonanceAfter':before+base+repeat}

def commit_anchor(state, *, prepared=True, point_perceived=True,
                  line_of_effect=True, components=True, commit='6.05'):
    """Atomic finite fixture commit; valid timing is supplied, not generated."""
    a=state['actor'];o=a['diagnosticActionOpportunity'];t=Fraction(commit)
    if not (Fraction(str(o['start']))<=t<Fraction(str(o['end']))):
        raise ValueError('Outside actual supplied ordinary turn')
    if not a['actionAvailable'] or state['ordinaryActionCommittedThisTurn']:
        raise ValueError('No ordinary Action')
    if a['class']!='Wizard' or a['classLevel']<7 or not prepared:
        raise ValueError('Missing actual access/prepared matrix')
    if not (point_perceived and line_of_effect and components):
        raise ValueError('Missing actual source predicates')
    origin=a['spellOrigin'];point=(30,0,0)
    if sum((x-y)**2 for x,y in zip(origin,point))>60**2:
        raise ValueError('Actual selected point out of range')
    calc=price_and_cadence(a)
    if a['RP']<calc['RPcost']:
        raise ValueError('Unaffordable')
    out=copy.deepcopy(state);out['at']=float(t);b=out['actor']
    b['RP']-=calc['RPcost'];b['Dissonance']=calc['DissonanceAfter']
    b['Refrain']=calc['repeat'];b['previousSpell']='Dimensional Anchor'
    if 'dimensional-anchor' not in b['matrixFamiliesUsed']:
        b['matrixFamiliesUsed'].append('dimensional-anchor')
    b['actionAvailable']=False
    b['concentration']='prospective actual Dimensional Anchor committed at6.05'
    out['ordinaryActionCommittedThisTurn']=True
    out['RPspentThisDiagnostic']+=calc['RPcost']
    if out['field'] is not None:
        out['concentrationEndEvents'].append({'sourceId':out['field']['id'],
            'at':float(t),'cause':'new lawful concentration commitment',
            'originalDeadline':out['field']['originalDeadline'],'refund':False})
        out['field']['state']='ended-by-incompatible-new-concentration'
        out['field']['actualEndedAt']=float(t)
    return out

def resolve_anchor(state, *, countered=False):
    out=copy.deepcopy(state)
    if not state['ordinaryActionCommittedThisTurn']:
        raise ValueError('No paid commitment')
    if countered:
        out['at']=6.1;out['actor']['concentration']=None
        return out
    expiry=float(Fraction('6.1')+60)
    out['at']=6.1
    out['actor']['concentration']='new actual Anchor at[30,0,0],radius60,deadline66.1'
    out['field']={'id':'anchor-repeat-6_1','spellId':'dimensional-anchor',
        'owner':'anchorCaster','center':[30,0,0],'radius':60,'establishedAt':6.1,
        'originalDeadline':expiry,'state':'live','concentration':True}
    return out

def end_fixture_turn(state):
    if not state['ordinaryActionCommittedThisTurn']:
        raise ValueError('Only the supplied spell-casting turn is modeled')
    out=copy.deepcopy(state);out['at']=8;out['regularTurnEnded']=True
    # No idle/weapon-turn decay: a spell was actually cast this regular turn.
    return out

def evidence():
    d=load('CAST_HISTORY_DIAGNOSTIC.json');s=d['initialState']
    committed=commit_anchor(s);resolved=resolve_anchor(committed);ended=end_fixture_turn(resolved)
    broken=copy.deepcopy(s);broken['actor']['matrixFamiliesUsed']=[]
    broken_calc=price_and_cadence(broken['actor'])
    old=load('history/return02/MODEL.json')['currentVectors'][9]
    new=load('MODEL.json')['currentVectors'][9]
    predicate=lambda c:all(x['actorSheets']['anchorCaster']['matrixFamiliesUsed']==['dimensional-anchor']
                           for x in [c]+c['independentBranches'])
    return {'id':'RD8-CAST-HISTORY-INDEPENDENT-NUMERICAL-STATE-EVIDENCE-13',
      'scope':'Isolated source-qualified fixture, not project runtime or action-reachability evidence.',
      'oldNineSheetPredicate':predicate(old),'newNineSheetPredicate':predicate(new),
      'geometry':{'distanceSquared':sum((x-y)**2 for x,y in zip(s['actor']['spellOrigin'],(30,0,0))),
                  'maxDistanceSquared':60**2},
      'actualOpportunity':d['actualOpportunity'],'initialState':s,
      'independentlyComputedCommitment':committed,'independentlyComputedResolution':resolved,
      'independentlyComputedFinal':ended,
      'matchesFullAuthoredCommitment':committed==d['timeline'][1]['after'],
      'matchesFullAuthoredResolution':resolved==d['timeline'][2]['after'],
      'matchesFullAuthoredFinal':ended==d['expectedFinalState'],
      'oldOmissionCounterfactual':{'base':broken_calc['base'],'Refrain':broken_calc['repeat'],
                                  'DissonanceAfter':broken_calc['DissonanceAfter'],
                                  'authorizedAlternative':False},
      'requiredRepeatedBase':1,'actualRepeatedRefrain':1,'correctDissonanceAfter':2,
      'priorFirstCastBaseRemainsZero':d['prefix']['baseDissonance']==0,
      'originalDeadlinePreservedInEndedRecord':committed['field']['originalDeadline'],
      'newPaidFieldDeadlineExact':str(Fraction('6.1')+60),
      'projectRuntimeTests':0,'projectChanges':0,'newRules':0}

class CastHistorySpecifications(unittest.TestCase):
    def setUp(self):
        self.d=load('CAST_HISTORY_DIAGNOSTIC.json');self.s=copy.deepcopy(self.d['initialState'])
    def test_01_original_nine_records_reproduce_omission(self):
        c=load('history/return02/MODEL.json')['currentVectors'][9]
        self.assertEqual(len(c['independentBranches'])+1,9)
        for x in [c]+c['independentBranches']:
            self.assertEqual(x['actorSheets']['anchorCaster']['matrixFamiliesUsed'],[])
            self.assertIn('At-1 paid actual Dimensional Anchor',x['actorSheets']['anchorCaster']['initialSetup'])
    def test_02_nine_successor_records_spent(self):
        c=load('MODEL.json')['currentVectors'][9]
        for x in [c]+c['independentBranches']:
            a=x['actorSheets']['anchorCaster']
            self.assertEqual(a['matrixFamiliesUsed'],['dimensional-anchor'])
            self.assertIn('SAME-ENCOUNTER QUALIFICATION',a['initialSetup'])
            self.assertEqual((a['RP'],a['Dissonance'],a['Refrain']),(17,0,0))
    def test_03_actual_first_cast_remains_exempt(self):
        a=copy.deepcopy(self.s['actor']);a.update(RP=24,previousSpell=None,matrixFamiliesUsed=[])
        c=price_and_cadence(a)
        self.assertEqual((c['base'],c['repeat'],c['DissonanceAfter'],24-c['RPcost']),(0,0,0,17))
    def test_04_later_same_family_real_price_and_cadence(self):
        c=price_and_cadence(self.s['actor'])
        self.assertEqual(c,{'limit':9,'RPcost':7,'base':1,'repeat':1,'DissonanceAfter':2})
    def test_05_original_omission_is_one_not_zero_strain(self):
        a=copy.deepcopy(self.s['actor']);a['matrixFamiliesUsed']=[]
        c=price_and_cadence(a)
        self.assertEqual((c['base'],c['repeat'],c['DissonanceAfter']),(0,1,1))
    def test_06_full_committed_state_matches(self):
        self.assertEqual(commit_anchor(self.s),self.d['timeline'][1]['after'])
    def test_07_full_resolved_and_final_states_match(self):
        c=commit_anchor(self.s);r=resolve_anchor(c);f=end_fixture_turn(r)
        self.assertEqual(r,self.d['timeline'][2]['after']);self.assertEqual(f,self.d['expectedFinalState'])
    def test_08_one_real_action_no_reaction_or_bonus_debit(self):
        a=commit_anchor(self.s)['actor']
        self.assertFalse(a['actionAvailable'])
        self.assertEqual(a['reactionAvailable'],self.s['actor']['reactionAvailable'])
        self.assertEqual(a['bonusActionAvailable'],self.s['actor']['bonusActionAvailable'])
    def test_09_missing_action_is_atomic(self):
        self.s['actor']['actionAvailable']=False;before=copy.deepcopy(self.s)
        with self.assertRaises(ValueError):commit_anchor(self.s)
        self.assertEqual(self.s,before)
    def test_10_missing_prepared_source_is_atomic(self):
        before=copy.deepcopy(self.s)
        with self.assertRaises(ValueError):commit_anchor(self.s,prepared=False)
        self.assertEqual(self.s,before)
    def test_11_missing_perception_components_or_loe_is_atomic(self):
        for kwargs in [{'point_perceived':False},{'components':False},{'line_of_effect':False}]:
            before=copy.deepcopy(self.s)
            with self.assertRaises(ValueError):commit_anchor(self.s,**kwargs)
            self.assertEqual(self.s,before)
    def test_12_unaffordable_is_atomic(self):
        self.s['actor']['RP']=6;before=copy.deepcopy(self.s)
        with self.assertRaises(ValueError):commit_anchor(self.s)
        self.assertEqual(self.s,before)
    def test_13_geometry_is_measured_not_flag_only(self):
        self.assertEqual(sum((x-y)**2 for x,y in zip(self.s['actor']['spellOrigin'],(30,0,0))),109)
        self.s['actor']['spellOrigin']=[100,0,3];before=copy.deepcopy(self.s)
        with self.assertRaises(ValueError):commit_anchor(self.s)
        self.assertEqual(self.s,before)
    def test_14_actual_ordinary_slot_is_required(self):
        self.assertLessEqual(6,6.05);self.assertLess(6.05,6.1);self.assertLess(6.1,8)
        with self.assertRaises(ValueError):commit_anchor(self.s,commit='8')
        with self.assertRaises(ValueError):commit_anchor(self.s,commit='5.9')
    def test_15_old_concentration_ends_at_new_commit(self):
        c=commit_anchor(self.s)
        self.assertEqual((c['field']['originalDeadline'],c['field']['actualEndedAt']),(59,6.05))
        self.assertEqual(len(c['concentrationEndEvents']),1)
        self.assertFalse(c['concentrationEndEvents'][0]['refund'])
    def test_16_new_deadline_belongs_to_new_instance(self):
        c=commit_anchor(self.s);r=resolve_anchor(c)
        self.assertNotEqual(c['field']['id'],r['field']['id'])
        self.assertEqual(Fraction(str(r['field']['originalDeadline']))-Fraction(str(r['field']['establishedAt'])),60)
        self.assertEqual(r['field']['originalDeadline'],66.1)
    def test_17_counter_after_commit_cannot_refund_or_restore(self):
        r=resolve_anchor(commit_anchor(self.s),countered=True)
        self.assertEqual((r['actor']['RP'],r['actor']['Dissonance'],r['actor']['Refrain']),(10,2,1))
        self.assertIsNone(r['actor']['concentration']);self.assertNotEqual(r['field']['state'],'live')
    def test_18_no_idle_end_reduction_on_casting_turn(self):
        f=end_fixture_turn(resolve_anchor(commit_anchor(self.s)))
        self.assertEqual(f['actor']['Dissonance'],2)
    def test_19_family_record_not_duplicated(self):
        c=commit_anchor(self.s)
        self.assertEqual(c['actor']['matrixFamiliesUsed'],['dimensional-anchor'])
        self.assertEqual(self.s['actor']['matrixFamiliesUsed'],['dimensional-anchor'])
    def test_20_different_name_resets_refrain_not_used_family(self):
        a=copy.deepcopy(self.s['actor']);a['previousSpell']='another actually cast spell'
        c=price_and_cadence(a);self.assertEqual((c['base'],c['repeat'],c['DissonanceAfter']),(1,0,1))
    def test_21_core_outcomes_and_branch_count_unchanged(self):
        a=load('history/return02/MODEL.json');b=load('MODEL.json')
        self.assertEqual(sum(len(c['independentBranches']) for c in b['currentVectors']),42)
        for i,(x,y) in enumerate(zip(a['currentVectors'],b['currentVectors'])):
            if i!=9:self.assertEqual(x,y)
            else:
                for old,new in zip([x]+x['independentBranches'],[y]+y['independentBranches']):
                    for key in old:
                        if key!='actorSheets':self.assertEqual(old[key],new[key]) if key!='independentBranches' else None
                    oa=copy.deepcopy(old['actorSheets']);na=copy.deepcopy(new['actorSheets'])
                    for sheet in [oa['anchorCaster'],na['anchorCaster']]:
                        sheet.pop('matrixFamiliesUsed');sheet.pop('initialSetup')
                    self.assertEqual(oa,na)
    def test_22_procedures_rules_and_questions_unchanged(self):
        a=load('history/return02/MODEL.json');b=load('MODEL.json')
        for key in ['records','selectedSharedRules','reviewQuestionDispositions02','reviewBoundaries02','boundedCorrectionConference03']:
            self.assertEqual(a[key],b[key])
    def test_23_all_current_case_mirrors_are_full(self):
        m=load('MODEL.json');c=load('CASE_DISPOSITIONS.json')
        self.assertEqual(m['currentVectors'],c['allCases'])
        self.assertIn(json.dumps(c,indent=2,ensure_ascii=False),(ROOT/'DIRECTOR_REVIEW.md').read_text())
    def test_24_no_encounter_boundary_or_new_rule(self):
        self.assertEqual(self.d['initialState']['encounterBoundariesSinceMinus1'],[])
        self.assertFalse(self.d['prefix']['crossingTimeZeroResetsHistory'])
        self.assertFalse(self.d['newGlobalRule']);self.assertFalse(self.d['runtimeExecuted'])
    def test_25_branch_source_absence_is_not_cast_erasure(self):
        c=load('MODEL.json')['currentVectors'][9]
        for b in c['independentBranches']:
            if b.get('explicitChangedInputs',{}).get('Anchor','notOverridden') is None:
                self.assertEqual(b['actorSheets']['anchorCaster']['matrixFamiliesUsed'],['dimensional-anchor'])
    def test_26_actual_wizard_rank_and_rp_source(self):
        w=load('cast_history_source/sources/wizard.json')
        self.assertEqual(w['rpByClassLevel'][6],24);self.assertEqual(w['maxSpellRankByClassLevel'][6],4)
        self.assertIn('first cast of each different prepared matrix family',w['engine'][11])
        self.assertEqual(self.d['initialActor']['hero'],None)
    def test_27_original_reports_not_relabelled_passes(self):
        r=load('cast_history_source/LOCAL_SEMANTIC_RECONCILIATION.json')
        self.assertEqual((r['diagnosticCheckCount'],r['diagnosticFailures']),(334,1))
        self.assertEqual(sum(not c['passed'] for c in r['diagnosticChecks']),1)
        self.assertIn('over-strict',r['diagnosticScopeCorrection']['reason'])
    def test_28_success_does_not_roll_or_heal_or_move(self):
        f=end_fixture_turn(resolve_anchor(commit_anchor(self.s)))
        self.assertEqual(f['rngDraws'],0)
        for key in ['hp','maxHP','tempHP','Wounds','body','conditions','abilityScores','saveBonuses','stage','hero']:
            self.assertEqual(f['actor'][key],self.s['actor'][key])

class Result(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.passed=[]
    def addSuccess(self,test):super().addSuccess(test);self.passed.append(test.id())

def write_once(path,value):
    if path is not None:
        with path.open('x',encoding='utf8') as h:h.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path);p.add_argument('--evidence',type=Path);a=p.parse_args()
    r=unittest.TextTestRunner(verbosity=1,resultclass=Result).run(unittest.defaultTestLoader.loadTestsFromTestCase(CastHistorySpecifications))
    report={'id':'RD8-CAST-HISTORY-ISOLATED-SPECIFICATION-13','testsRun':r.testsRun,
      'failures':len(r.failures),'errors':len(r.errors),'passedTests':r.passed,
      'failureDetails':[{'test':t.id(),'trace':trace} for t,trace in r.failures+r.errors],
      'scope':'Isolated finite fixture specifications; no game/project module imported or native scheduler executed.',
      'projectRuntimeTests':0,'humanPlaytests':0,'diagnosticSha256':sha256((ROOT/'CAST_HISTORY_DIAGNOSTIC.json').read_bytes()).hexdigest(),
      'modelSha256':sha256((ROOT/'MODEL.json').read_bytes()).hexdigest()}
    write_once(a.report,report);write_once(a.evidence,evidence())
    raise SystemExit(0 if r.wasSuccessful() else 1)

if __name__=='__main__':main()
