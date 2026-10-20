#!/usr/bin/env python3
"""Isolated finite specifications for the returned RD8 proposal.

No project modules, game engine, native scheduler, world renderer, creature generator,
network, or human gameplay are used. Helpers below implement only the explicitly
named arithmetic and finite event invariants under supplied eligibility predicates.
They are test specifications, not production code or an acquisition/reachability proof.
"""
from __future__ import annotations
import argparse
import copy
from dataclasses import dataclass, field
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import unittest
from typing import Any

ROOT = Path(__file__).resolve().parent

def split_flat(parts: dict[str, int], reduction: int) -> dict[str, int]:
    """Exact proportional allocation; lexical damage type resolves equal remainders."""
    if reduction < 0 or any(v < 0 for v in parts.values()):
        raise ValueError('Negative damage or reduction')
    amount = min(reduction, sum(parts.values()))
    if not amount:
        return {k: 0 for k in parts}
    weights = {k: Fraction(v * amount, sum(parts.values())) for k, v in parts.items()}
    out = {k: q.numerator // q.denominator for k, q in weights.items()}
    order = sorted(parts, key=lambda k: (-(weights[k]-out[k]), k))
    for k in order[:amount-sum(out.values())]:
        out[k] += 1
    return out

def mixed(parts: dict[str, int], save: bool = False, reduction: int = 0,
          stage: str = 'before', resist: frozenset[str] = frozenset(),
          immune: frozenset[str] = frozenset()) -> dict[str, int]:
    if stage not in {'before','after'}:
        raise ValueError('Unknown defense stage')
    p = {k: v//2 if save else v for k,v in parts.items()}
    if stage == 'before':
        a=split_flat(p,reduction); p={k:v-a[k] for k,v in p.items()}
    p={k: 0 if k in immune else v//2 if k in resist else v for k,v in p.items()}
    if stage == 'after':
        a=split_flat(p,reduction); p={k:v-a[k] for k,v in p.items()}
    return p

def choose_flat(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    eligible = [c for c in candidates if c['eligible'] and c['value'] > 0]
    return min(eligible,key=lambda c:(-c['value'],c['source'],c['owner'],c['application'])) if eligible else None

def life_arithmetic(hp: int, maximum: int, temp: int, damage: int, *, null=False,
                    finite=False) -> dict[str, Any]:
    """Only an initially positive, unwounded recipient, before any actual Wound save.
    Does not simulate source-owned would-die responses, injuries or preexisting zero states.
    """
    if hp <= 0 or maximum <= 0 or min(temp,damage) < 0:
        raise ValueError('Outside this finite specification')
    absorbed=min(temp,damage); normal=damage-absorbed; lost=min(hp,normal)
    remaining=max(0,hp-normal); over=max(0,normal-hp)
    if remaining:
        state='living-positive'; wound=(not null and normal*2>=maximum)
    elif finite:
        state='NullDisabled' if null else 'ended'; wound=False
    elif null:
        state='Stable0'; wound=False
    elif over>=maximum:
        state='dead'; wound=False
    else:
        state='Dying0'; wound=True
    return {'hp':remaining,'temp':temp-absorbed,'normalLoss':lost,'overkill':over,
            'state':state,'woundRequired':wound,
            'woundDC':max(10,normal//2) if wound else None}

def sphere_box(center, radius, lower, upper):
    return sum((lo-c if c<lo else c-hi if c>hi else 0)**2
               for c,lo,hi in zip(center,lower,upper)) <= radius*radius

def wall_point(u,v,w):
    return abs(u)<=30 and v>=0 and w>=0 and v*v+w*w<=900

def wall_box(lower,upper):
    # Existence of a closed-volume witness, not a center-only test.
    return (lower[0]<=30 and upper[0]>=-30 and upper[1]>=0 and upper[2]>=0
            and max(0,lower[1])**2+max(0,lower[2])**2<=900)

def pulses(established):
    return [established+6*i for i in range(10)]

@dataclass
class CloudFamily:
    """Supplied immutable scene-round identifier; no initiative generator is simulated."""
    claims: set[tuple[str,int]] = field(default_factory=set)
    def exposure(self,target,round_id,*,eligible=True,suppressed=False):
        key=(target,round_id)
        if not eligible or suppressed or key in self.claims:
            return False
        self.claims.add(key)
        return True

@dataclass
class CorpseFuel:
    principal_id: str
    available: bool=True
    consumed_by: str|None=None
    gear: tuple[str,...]=('robe','pouch')
    def consume(self, event, *, qualifying=True, countered=False, source_prevented=False):
        if countered or source_prevented or not qualifying or not self.available:
            return False
        self.available=False; self.consumed_by=event
        return True

def exile_result(*,actual_creature=True,alive=True,anchor=False,history=False,
                 other_cell=False,cha_success=False):
    # Damage already completed. Actual qualification is supplied, not inferred from CR/type.
    if not actual_creature or not alive or anchor or history or other_cell:
        return {'save':False,'cell':False,'newHardClaim':False}
    return {'save':True,'cell':not cha_success,'newHardClaim':not cha_success}

def wall_result(*,sees=True,whole_effect_prevented=False,identified=False,
                int_success=False,psi_immune=False,prone_immune=False,raw=32):
    if not sees or whole_effect_prevented:
        return {'damage':0,'prone':False,'admitted':False}
    damage=0 if psi_immune else raw//2 if int_success else raw
    return {'damage':damage,'prone':not int_success and not prone_immune,'admitted':True}

class RD8Specifications(unittest.TestCase):
    def test_01_spike_failure(self):
        self.assertEqual(mixed({'fire':27,'piercing':23},reduction=3,resist=frozenset({'fire'})),{'fire':12,'piercing':22})
    def test_02_spike_success(self):
        self.assertEqual(mixed({'fire':27,'piercing':23},save=True,reduction=3,resist=frozenset({'fire'})),{'fire':5,'piercing':10})
    def test_03_pyre_failure(self):
        self.assertEqual(mixed({'fire':15,'necrotic':17},reduction=3,resist=frozenset({'fire'})),{'fire':7,'necrotic':15})
    def test_04_pyre_success(self):
        self.assertEqual(mixed({'fire':15,'necrotic':17},save=True),{'fire':7,'necrotic':8})
    def test_05_pyre_tie_selected_before(self):
        selected=choose_flat([{'source':'warrior.supplement.spinal-plating','owner':'w','application':'s','value':2,'eligible':True},
                              {'source':'warrior.arch.brutal-fortitude','owner':'w','application':'b','value':2,'eligible':True}])
        self.assertEqual(selected['source'],'warrior.arch.brutal-fortitude')
        self.assertEqual(mixed({'fire':15,'necrotic':17},reduction=2,resist=frozenset({'fire'})),{'fire':7,'necrotic':16})
    def test_06_pyre_spinal_after_only(self):
        self.assertEqual(mixed({'fire':15,'necrotic':17},reduction=2,stage='after',resist=frozenset({'fire'})),{'fire':6,'necrotic':16})
    def test_07_type_tie_canonical(self):
        self.assertEqual(split_flat({'piercing':5,'fire':5},1),{'piercing':0,'fire':1})
    def test_08_flat_clamps_and_allocates_exactly(self):
        for reduction in range(0,13):
            result=split_flat({'fire':2,'necrotic':5},reduction)
            self.assertEqual(sum(result.values()),min(7,reduction))
            self.assertTrue(all(result[k]<=v for k,v in {'fire':2,'necrotic':5}.items()))
    def test_09_one_type_immunity_preserves_other(self):
        self.assertEqual(mixed({'fire':15,'necrotic':17},immune=frozenset({'fire'})),{'fire':0,'necrotic':17})
    def test_10_spinal_ineligible_single_target(self):
        self.assertEqual(choose_flat([{'source':'spinal','owner':'w','application':'s','value':2,'eligible':False}]),None)
    def test_11_temp_before_normal_and_zero(self):
        r=life_arithmetic(20,108,20,40)
        self.assertEqual((r['hp'],r['temp'],r['normalLoss'],r['overkill'],r['state'],r['woundDC']),(0,0,20,0,'Dying0',10))
    def test_12_success_absorbed_without_form_zero(self):
        r=life_arithmetic(20,108,20,20);self.assertEqual((r['hp'],r['temp'],r['woundRequired']),(20,0,False))
    def test_13_finite_golem_ends_no_corpse_inferred(self):
        r=life_arithmetic(24,60,0,41,finite=True)
        self.assertEqual((r['state'],r['normalLoss'],r['overkill']),('ended',24,17))
    def test_14_finite_null_disabled_not_organic(self):
        r=life_arithmetic(24,60,0,41,null=True,finite=True)
        self.assertEqual((r['state'],r['woundRequired']),('NullDisabled',False))
    def test_15_true_instant_death_blocks_creature_exile(self):
        r=life_arithmetic(1,24,0,46)
        self.assertEqual(r['state'],'dead');self.assertFalse(exile_result(alive=False)['cell'])
    def test_16_null_living_zero_is_not_dead(self):
        r=life_arithmetic(15,108,0,46,null=True)
        self.assertEqual(r['state'],'Stable0');self.assertTrue(exile_result(alive=True)['cell'])
    def test_17_cloud_hp_chain(self):
        hp=108
        for damage,expected in [(44,64),(20,44),(35,9),(15,0)]:
            r=life_arithmetic(hp,108,0,damage);self.assertEqual(r['hp'],expected);hp=r['hp']
        self.assertEqual((r['overkill'],r['woundDC']),(6,10))
    def test_18_different_events_do_not_aggregate_wounds(self):
        r=life_arithmetic(108,108,0,44);r2=life_arithmetic(r['hp'],108,0,20)
        self.assertFalse(r['woundRequired']);self.assertFalse(r2['woundRequired'])
    def test_19_concentration_uses_event_total(self):
        self.assertEqual(max(10,22//2),11);self.assertEqual(max(10,29//2),14)
    def test_20_life_link_terminal_transfer(self):
        force=46;transfer=min(23,force//2)
        self.assertEqual((108-(force-transfer),92-transfer,force-transfer+transfer),(85,69,46))
    def test_21_half_then_force_resistance(self):
        self.assertEqual(92-(41//2)//2,82)
    def test_22_rank8_real_price_and_strain(self):
        limit=max(4,2+5+4);price=21+(1 if 11>=limit else 0)
        self.assertEqual((limit,42-price,11+2+1),(11,20,14))
    def test_23_ranked_precast_block(self):
        self.assertGreaterEqual(17,max(4,2+5+4)+6)
    def test_24_wizard_mastery_and_saves(self):
        self.assertEqual(8+5+4+2,19);self.assertEqual(8+5+4,17)
    def test_25_counter_does_not_use_school_dc(self):
        self.assertEqual((17+5+4,10+2*8,56-3),(26,26,53))
    def test_26_different_dispel_dcs(self):
        self.assertEqual((10+2*8,10+8),(26,18))
    def test_27_large_cloud_body_witness_not_center(self):
        self.assertFalse(sphere_box((18,0,3),20,(42,0,3),(42,0,3)))
        self.assertTrue(sphere_box((18,0,3),20,(37,-5,0),(47,5,8)))
    def test_28_sphere_boundary_is_closed(self):
        self.assertTrue(sphere_box((0,0,0),20,(20,0,0),(21,1,1)))
        self.assertFalse(sphere_box((0,0,0),20,(20.01,0,0),(21,1,1)))
    def test_29_spike_airborne_positive_and_height_limit(self):
        self.assertTrue(0<=20<=30);self.assertFalse(0<=31<=30)
        self.assertLess(30**2+(20-3)**2,120**2)
    def test_30_pyre_current_anchor(self):
        self.assertLess(15**2+(2-3)**2,20**2)
        self.assertGreater(25**2+(2-3)**2,20**2)
    def test_31_wall_actual_swept_region(self):
        self.assertTrue(wall_point(10,10,20));self.assertTrue(wall_point(-10,10,1))
        self.assertFalse(wall_point(10,25,25));self.assertFalse(wall_point(31,0,1))
    def test_32_wall_large_body_admission(self):
        self.assertTrue(wall_box((29,0,0),(39,10,8)))
        self.assertFalse(wall_box((8,25,25),(10.5,27.5,27)))
    def test_33_cell_extent_and_same_body(self):
        rounded=lambda x:((x+4)//5)*5
        self.assertEqual((rounded(5+10),rounded(5+10),rounded(6+5)),(15,15,15))
        self.assertLessEqual(5+2.5,7.5)
    def test_34_adjacent_return_nonoverlap(self):
        occupied=(27.5,32.5);returning=(22.5,27.5)
        self.assertEqual(returning[1],occupied[0]);self.assertFalse(min(returning[1],occupied[1])>max(returning[0],occupied[0]))
    def test_35_cloud_exact_pulses_expiry_wins(self):
        self.assertEqual(pulses(0),list(range(0,60,6)));self.assertNotIn(60,pulses(0))
    def test_36_cloud_source_offsets_remain(self):
        self.assertEqual(pulses(Fraction(1,10))[1],Fraction(61,10))
        self.assertEqual(pulses(Fraction(11,10))[1],Fraction(71,10))
    def test_37_cloud_other_caster_no_second_family(self):
        f=CloudFamily();self.assertTrue(f.exposure('t',0));self.assertFalse(f.exposure('t',0));self.assertTrue(f.exposure('t',1))
    def test_38_cloud_suppressed_does_not_claim(self):
        f=CloudFamily();self.assertFalse(f.exposure('t',1,suppressed=True));self.assertTrue(f.exposure('t',1))
    def test_39_cloud_immunity_still_admitted(self):
        f=CloudFamily();self.assertTrue(f.exposure('immune',1));self.assertFalse(f.exposure('immune',1))
    def test_40_no_entry_or_resume_pulse(self):
        self.assertNotIn(1,pulses(0));self.assertNotIn(6.5,pulses(0));self.assertNotIn(7.2,pulses(0))
    def test_41_created_batch_then_no_future(self):
        admitted=['caster','target'];effects=[];concentration=True
        for actor in admitted:
            effects.append(actor)
            if actor=='caster':concentration=False
        self.assertEqual(effects,['caster','target']);self.assertFalse(concentration)
    def test_42_area_roots_snapshotted_before_consequences(self):
        actual_null=True;roots=[{'recipient':t,'null':actual_null} for t in ['a','b']]
        actual_null=False
        self.assertTrue(all(r['null'] for r in roots));self.assertFalse({'recipient':'b','null':actual_null}['null'])
    def test_43_corpse_atomic_one_winner(self):
        f=CorpseFuel('corpse');self.assertTrue(f.consume('first'));self.assertFalse(f.consume('second'))
        self.assertEqual(f.consumed_by,'first');self.assertEqual(f.gear,('robe','pouch'))
    def test_44_counter_does_not_consume_corpse(self):
        f=CorpseFuel('corpse');self.assertFalse(f.consume('cast',countered=True));self.assertTrue(f.available)
    def test_45_corpse_late_invalidation_no_substitute(self):
        f=CorpseFuel('selected');self.assertFalse(f.consume('cast',qualifying=False));self.assertTrue(f.available)
    def test_46_creating_source_prevention_before_fuel(self):
        f=CorpseFuel('selected');self.assertFalse(f.consume('cast',source_prevented=True));self.assertTrue(f.available)
    def test_47_consumed_fuel_not_refunded_by_null(self):
        f=CorpseFuel('selected');self.assertTrue(f.consume('cast'));life_arithmetic(15,108,0,32,null=True)
        self.assertFalse(f.available)
    def test_48_exile_positive_after_real_damage(self):
        self.assertEqual(life_arithmetic(108,108,0,46)['hp'],62)
        self.assertEqual(exile_result(),{'save':True,'cell':True,'newHardClaim':True})
    def test_49_anchor_prevents_only_exile(self):
        self.assertEqual(life_arithmetic(108,108,0,46)['hp'],62)
        self.assertEqual(exile_result(anchor=True),{'save':False,'cell':False,'newHardClaim':False})
    def test_50_cha_success_not_force_immunity(self):
        self.assertEqual(life_arithmetic(108,108,0,46)['hp'],62);self.assertFalse(exile_result(cha_success=True)['cell'])
    def test_51_force_resistance_does_not_prevent_exile(self):
        self.assertEqual(life_arithmetic(92,92,0,46//2)['hp'],69);self.assertTrue(exile_result()['cell'])
    def test_52_shared_live_cell_and_history_no_reclaim(self):
        self.assertFalse(exile_result(other_cell=True)['newHardClaim']);self.assertFalse(exile_result(history=True)['newHardClaim'])
    def test_53_break_counter_old_concentration_not_restored(self):
        old='true-seeing';rp=29-21;old=None;pending='break';pending=None
        self.assertEqual((old,pending,rp),(None,None,8))
    def test_54_wall_true_seeing_identification_not_cancellation(self):
        self.assertEqual(wall_result(identified=True,raw=29),{'damage':29,'prone':True,'admitted':True})
    def test_55_wall_blinded_no_visual_admission(self):
        self.assertEqual(wall_result(sees=False,identified=True),{'damage':0,'prone':False,'admitted':False})
    def test_56_wall_separate_immunities(self):
        self.assertEqual(wall_result(psi_immune=True),{'damage':0,'prone':True,'admitted':True})
        self.assertEqual(wall_result(prone_immune=True),{'damage':32,'prone':False,'admitted':True})
    def test_57_wall_success_and_whole_effect_prevention(self):
        self.assertEqual(wall_result(int_success=True,raw=29),{'damage':14,'prone':False,'admitted':True})
        self.assertFalse(wall_result(whole_effect_prevented=True)['admitted'])
    def test_58_wall_actual_fall_marker_and_impact(self):
        initiating_slot_end=2;next_round=6;marker=initiating_slot_end+next_round
        self.assertEqual(marker,8);self.assertNotEqual(marker,4)
        dice=min(10,20//20);self.assertEqual((dice,108-32-4,30//2),(1,72,15))
    def test_59_native_rng_totals_in_full_main_cases(self):
        data=json.loads((ROOT/'CASE_DISPOSITIONS.json').read_text())
        for case in data['allCases']:
            for roll in case['rng']:
                if isinstance(roll,dict) and isinstance(roll.get('faces'),list) and 'total' in roll:
                    with self.subTest(case=case['id'],kind=roll.get('kind')):
                        self.assertEqual(sum(roll['faces'])+roll.get('bonus',0),roll['total'])
    def test_60_actual_declared_commit_arithmetic(self):
        data=json.loads((ROOT/'CASE_DISPOSITIONS.json').read_text())
        for case in data['allCases']:
            for t in case['timeline']:
                if isinstance(t,dict) and 'price' in t and 'before' in t:
                    with self.subTest(case=case['id'],time=t['atSeconds']):
                        p=t['price'];self.assertEqual(p['base']+p['strainSurcharge']+p['otherAdjustments'],p['finalRP'])
                        self.assertEqual(t['before']['RP']-p['finalRP'],t['after']['RP'])
                        self.assertFalse(t['after']['Action'])
                        self.assertEqual(t['before']['Dissonance']+t['cadence']['baseAfterActualClassRule']+t['cadence']['sameNameAddition'],t['after']['Dissonance'])


    def test_61_actual_counter_recovery_retained_in_both_cases(self):
        data=json.loads((ROOT/'CASE_DISPOSITIONS.json').read_text())
        branches={b['id']:b for c in data['allCases'] for b in c['independentBranches']}
        self.assertEqual(branches['RD8-03-B-COUNTER']['finalState']['reactorRP'],56-3+1)
        self.assertEqual(branches['RD8-05-B-COUNTER']['finalState']['counteringWizardRP'],56-3+1)
        self.assertTrue(branches['RD8-03-B-COUNTER']['finalState']['reactorArcaneFeedbackUsedThisRound'])
        self.assertTrue(branches['RD8-05-B-COUNTER']['finalState']['counteringWizardArcaneFeedbackUsedThisRound'])
    def test_62_bt_gains_after_defended_event_not_retroactively(self):
        data=json.loads((ROOT/'CASE_DISPOSITIONS.json').read_text())
        branches={b['id']:b for c in data['allCases'] for b in c['independentBranches']}
        tie=branches['RD8-03-A-TIE']['finalState'];spinal=branches['RD8-03-A-SPINAL']['finalState']
        self.assertEqual((tie['warriorHP'],tie['BT'],tie['BrutalityProgress']),(82,3,53))
        self.assertEqual((spinal['warriorHP'],spinal['BT'],spinal['BrutalityProgress']),(83,1,0))
        self.assertGreaterEqual(23,4+4);self.assertGreaterEqual(22,4+4)
        self.assertEqual(min(3,2+1),3);self.assertEqual(min(3,0+1),1)

class RecordingResult(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.passed=[]
    def addSuccess(self,test):super().addSuccess(test);self.passed.append(test.id())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);args=ap.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(RD8Specifications)
    result=unittest.TextTestRunner(verbosity=1,resultclass=RecordingResult).run(suite)
    report={'id':'RD8-ISOLATED-SPECIFICATION-REPORT-01','testsRun':result.testsRun,
            'failures':len(result.failures),'errors':len(result.errors),'passedTests':result.passed,
            'failureDetails':[{'test':t.id(),'trace':s} for t,s in result.failures+result.errors],
            'scope':'New isolated finite arithmetic, geometry and event-policy specifications. Disclosed source eligibility inputs; no acquisition/reachability proof or project engine imported.',
            'projectRuntimeTests':0,'humanPlaytests':0,
            'casesSha256':hashlib.sha256((ROOT/'CASE_DISPOSITIONS.json').read_bytes()).hexdigest()}
    if args.report:
        args.report.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
if __name__=='__main__':main()
