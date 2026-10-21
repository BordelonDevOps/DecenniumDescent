"""Correction02 full-fixture checks and isolated arithmetic; not runtime validation."""
import copy,json,unittest
from pathlib import Path
from correction_reference import *
ROOT=Path(__file__).resolve().parents[1]
MODEL=json.loads((ROOT/"MODEL.json").read_bytes())
OLD=json.loads((ROOT/"baseline/RETURN01_MODEL.json").read_bytes())
def cases(m):return {x["id"]:x for c in m["currentVectors"] for x in [c]+c["independentBranches"]}
NEW=cases(MODEL); BEFORE=cases(OLD)
ROWS=[("RIC5-01-B",3,"enemy"),("RIC5-02-A",2,"mage"),("RIC5-04-A",3,"enemy"),
      ("RIC5-04-B",3,"carrier"),("RIC5-05-B",5,"creator"),("RIC5-05-B",7,"creator"),
      ("RIC5-02-B-a",1,"wizard"),("RIC5-04-B-b",0,"caster")]
INIT={"STR":8,"DEX":14,"CON":14,"INT":16,"WIS":12,"CHA":8}
CHOICES=[{"classLevel":4,"kind":"asi","ability":"INT","amount":2},
         {"classLevel":8,"kind":"asi","ability":"STR","amount":2},
         {"classLevel":12,"kind":"feat","featId":"metamagicAdept","modes":["Reach","Sculpt"]}]
class Acquisition(unittest.TestCase):
 def test_old_milestones_cannot_supply_adept(self):
  old=BEFORE["RIC5-02-B-a"]["actorDefinitions"]["wizard"]["asiHistory"]
  self.assertFalse(any("metamagic" in str(v).lower() for v in old.values()))
 def test_positive_legal_replacement_scores(self):
  self.assertEqual(legal_advancement(INIT,CHOICES,operational_feat=True)["scores"],
                   {"STR":10,"DEX":14,"CON":14,"INT":18,"WIS":12,"CHA":8})
 def test_no_fourth_milestone(self):
  self.assertRaises(ValueError,legal_advancement,INIT,CHOICES+[{"classLevel":12,"kind":"asi","ability":"CHA","amount":2}],operational_feat=True)
 def test_future_milestone_cannot_pay_at13(self):
  self.assertRaises(ValueError,legal_advancement,INIT,[dict(CHOICES[-1],classLevel=16)],operational_feat=True)
 def test_availability_not_closed_by_fixture(self):
  self.assertRaises(ValueError,legal_advancement,INIT,CHOICES,operational_feat=False)
 def test_mode_choices_are_distinct(self):
  self.assertRaises(ValueError,legal_advancement,INIT,CHOICES[:2]+[dict(CHOICES[-1],modes=["Sculpt","Sculpt"])],operational_feat=True)
 def test_complete_wizard_variant(self):
  p=NEW["RIC5-02-B-a"]["actorDefinitions"]["wizard"]
  self.assertEqual((p["CHA"],p["saves"]["CHA"],p["spellDc"],p["schoolDc"],p["maxRp"],p["Limit"]),(8,-1,17,19,48,11))
  self.assertEqual(p["featAcquisition"]["chosenModes"],["Reach","Sculpt"])
  self.assertFalse(p["featAcquisition"]["completeSourceRecordUnchanged"]["selectionEnabled"])
 def test_complete_mage_variant(self):
  p=NEW["RIC5-02-B-b"]["actorDefinitions"]["mage"]
  self.assertEqual((p["CHA"],p["saves"]["CHA"],p["spellDc"],p["maxRp"]),(8,-1,17,38))
  self.assertTrue(p["metaspellMode"].startswith("Sculpt"))
  self.assertTrue(any(row["classLevel"]==5 and any(v["id"]=="mage.arch.metaspell-access" for v in row["cards"]) for row in p["selectedAcquisition"]))
 def test_positive_pool_not_refilled(self):
  a=NEW["RIC5-02-B-a"]["expectedFinalState"]["actors"]["wizard"]
  self.assertEqual((a["rp"],a["dissonance"],a["featSorceryPoints"]),(26,0,0))
 def test_two_provider_rejection_no_debits(self):
  e=NEW["RIC5-02-B-b"]["timeline"][0]
  self.assertEqual(e["before"],e["after"])
  a=e["after"]["actors"]["mage"]
  self.assertEqual((a["action"],a["rp"],a["metaspellUses"],a["featSorceryPoints"]),(True,38,1,2))
 def test_unrelated_charisma_not_changed(self):
  self.assertEqual(NEW["RIC5-02-B"]["actorDefinitions"]["mage"]["CHA"],10)
 def test_all_source_derived_saves(self):
  for cid,who in [("RIC5-02-B-a","wizard"),("RIC5-02-B-b","mage")]:
   p=NEW[cid]["actorDefinitions"][who]
   for ability in ["STR","DEX","CON","INT","WIS","CHA"]:
    self.assertEqual(p["saves"][ability],save_modifier(p[ability],p["PB"],ability in ["INT","WIS"]))
class ActionLedgers(unittest.TestCase):
 def test_original_eight_after_states_fail(self):
  self.assertEqual(sum(BEFORE[c]["timeline"][i]["after"]["actors"][a]["action"] is True for c,i,a in ROWS),8)
 def test_refresh_then_debit_not_refresh_after_debit(self):
  old=copy.deepcopy(BEFORE["RIC5-01-B"]["timeline"][2]["after"]["actors"]["enemy"])
  self.assertFalse(old["action"])
  refreshed=refresh_action(old,3,actual_regular_start=True)
  self.assertTrue(refreshed["action"])
  after=commit_action(refreshed)
  self.assertFalse(after["action"])
  self.assertEqual(after["regularStart"],3)
 def test_cannot_manufacture_start(self):
  self.assertRaises(ValueError,refresh_action,{"action":False,"nextRegularStart":6},6,actual_regular_start=False)
 def test_second_action_is_not_free(self):
  self.assertRaises(ValueError,commit_action,{"action":False})
 def test_invalid_declaration_is_unspent(self):
  self.assertEqual(commit_action({"action":True,"rp":20},legal=False),{"action":True,"rp":20})
 def test_spent_carries_through_enemy_counter_resolution(self):
  c=NEW["RIC5-01-B"]
  for i in (4,5):
   for side in ("before","after"):self.assertFalse(c["timeline"][i][side]["actors"]["enemy"]["action"])
  self.assertFalse(c["expectedFinalState"]["actors"]["enemy"]["action"])
 def test_mage_refresh_only_at_actual13(self):
  c=NEW["RIC5-02-A"]
  self.assertFalse(c["timeline"][3]["after"]["actors"]["mage"]["action"])
  self.assertTrue(c["timeline"][4]["before"]["actors"]["mage"]["action"])
  self.assertEqual(c["timeline"][4]["before"]["actors"]["mage"]["regularStart"],13)
 def test_carrier_later_actual_refresh_remains(self):
  c=NEW["RIC5-04-B"]
  self.assertFalse(c["timeline"][3]["after"]["actors"]["carrier"]["action"])
  self.assertTrue(c["timeline"][4]["before"]["actors"]["carrier"]["action"])
 def test_dismissal_spent_until_next_start(self):
  c=NEW["RIC5-05-B"]
  self.assertFalse(c["timeline"][6]["before"]["actors"]["creator"]["action"])
  self.assertFalse(c["timeline"][6]["after"]["actors"]["creator"]["action"])
  self.assertTrue(c["timeline"][7]["before"]["actors"]["creator"]["action"])
  self.assertFalse(c["expectedFinalState"]["actors"]["creator"]["action"])
 def test_donor_action_negative_time_precedes_actual_zero_refresh(self):
  c=NEW["RIC5-01-A-g"]
  e=c["timeline"][0]
  self.assertEqual((e["before"]["actors"]["donor"]["regularStart"],e["after"]["actors"]["donor"]["nextRegularStart"]),(-6,0))
  self.assertFalse(e["after"]["actors"]["donor"]["action"])
  self.assertEqual((c["timeline"][1]["before"]["actors"]["donor"]["regularStart"],c["timeline"][1]["before"]["actors"]["donor"]["action"]),(0,True))
 def test_no_action_refill_without_advancing_start(self):
  for c in NEW.values():
   previous=c["initialState"]
   for e in c["timeline"]:
    for who,old in previous["actors"].items():
     new=e["before"]["actors"][who]
     if not old["action"] and new["action"]:
      self.assertGreater(new["regularStart"],old["regularStart"],(c["id"],e["event"],who))
    previous=e["after"]
 def test_class_mode_branch_start_precedes_commitment(self):
  e=NEW["RIC5-01-B-f"]["timeline"][1]
  self.assertEqual((e["before"]["actors"]["enemy"]["regularStart"],e["before"]["actors"]["enemy"]["action"],e["after"]["actors"]["enemy"]["action"]),(3,True,False))
 def test_composite_child_no_second_action(self):
  for i in [2,3]:
   c=NEW["RIC5-01-A"]
   self.assertFalse(c["timeline"][i]["after"]["actors"]["echoer"]["action"])
  self.assertFalse(NEW["RIC5-01-A"]["timeline"][3]["before"]["actors"]["echoer"]["action"])
 def test_reaction_only_release_no_second_action(self):
  e=NEW["RIC5-01-B"]["timeline"][4]
  self.assertFalse(e["before"]["actors"]["echoer"]["action"])
  self.assertFalse(e["after"]["actors"]["echoer"]["action"])
  self.assertTrue(e["before"]["actors"]["echoer"]["reaction"])
  self.assertFalse(e["after"]["actors"]["echoer"]["reaction"])
class ReadyCadence(unittest.TestCase):
 def test_original_release_equal_deadline_is_not_legal(self):
  e=BEFORE["RIC5-02-A-a"]["timeline"][2]
  self.assertFalse(ready_before_deadline(e["timeSeconds"],61,trigger_complete=True,reaction=True,concentration=True))
 def test_new_release_after_surge_before_start(self):
  e=NEW["RIC5-02-A-a"]["timeline"][2]
  self.assertTrue(60.5<e["timeSeconds"]<61)
  self.assertTrue(ready_before_deadline(e["timeSeconds"],61,trigger_complete=True,reaction=True,concentration=True))
 def test_no_new_start_in_release_event(self):
  e=NEW["RIC5-02-A-a"]["timeline"][2]
  self.assertEqual(e["regularStartsBeforeEvent"],[])
  self.assertEqual((e["before"]["actors"]["mage"]["regularStart"],e["before"]["actors"]["mage"]["nextRegularStart"]),(55,61))
 def test_reaction_only_keeps_prepared_action_spent(self):
  e=NEW["RIC5-02-A-a"]["timeline"][2]
  self.assertEqual((e["before"]["actors"]["mage"]["action"],e["after"]["actors"]["mage"]["action"]),(False,False))
  self.assertEqual((e["before"]["actors"]["mage"]["reaction"],e["after"]["actors"]["mage"]["reaction"]),(True,False))
 def test_deadline_and_gate_failures(self):
  self.assertFalse(ready_before_deadline(61,61,trigger_complete=True,reaction=True,concentration=True))
  self.assertFalse(ready_before_deadline(60.9,61,trigger_complete=False,reaction=True,concentration=True))
  self.assertFalse(ready_before_deadline(60.9,61,trigger_complete=True,reaction=False,concentration=True))
  self.assertFalse(ready_before_deadline(60.9,61,trigger_complete=True,reaction=True,concentration=False))
class EraseHistory(unittest.TestCase):
 def test_original_omitted_both_fields(self):
  a=BEFORE["RIC5-03-B-a"]["expectedFinalState"]["actors"]["caster"]
  self.assertIsNone(a["lastSpell"]);self.assertEqual(a["preparedFamiliesUsed"],[])
 def test_first_prepared_commit_matches_full_actor(self):
  c=NEW["RIC5-03-B-a"]
  self.assertEqual(commit_erase_matrix(c["initialState"]["actors"]["caster"]),c["expectedFinalState"]["actors"]["caster"])
 def test_real_first_base_remains_zero(self):
  a=NEW["RIC5-03-B-a"]["expectedFinalState"]["actors"]["caster"]
  self.assertEqual((a["rp"],a["dissonance"],a["refrain"]),(31,0,0))
 def test_next_repeated_cast_spends_family_and_refrain(self):
  a=NEW["RIC5-03-B-a"]["expectedFinalState"]["actors"]["caster"]
  nextturn=refresh_action(a,6,actual_regular_start=True)
  out=commit_erase_matrix(nextturn)
  self.assertEqual((out["rp"],out["dissonance"],out["refrain"],out["preparedFamiliesUsed"]),(14,3,1,["erase-from-reality"]))
 def test_duplicate_family_does_not_refresh_exemption(self):
  a=NEW["RIC5-03-B-a"]["expectedFinalState"]["actors"]["caster"]
  self.assertEqual(commit_erase_matrix(refresh_action(a,6,actual_regular_start=True))["dissonance"],3)
 def test_next_history_not_cleared_by_idle_or_wall(self):
  c=NEW["RIC5-03-B-a"]
  self.assertEqual(c["expectedFinalState"]["applications"],BEFORE[c["id"]]["expectedFinalState"]["applications"])
  self.assertEqual(c["expectedFinalState"]["privateMemories"],BEFORE[c["id"]]["expectedFinalState"]["privateMemories"])
 def test_no_second_action_before_refresh(self):
  self.assertRaises(ValueError,commit_erase_matrix,NEW["RIC5-03-B-a"]["expectedFinalState"]["actors"]["caster"])
class PreservedScope(unittest.TestCase):
 def test_all_five_procedures_and_native_records_exact(self):
  self.assertEqual(MODEL["records"],OLD["records"])
 def test_all_24_answers_and_shared_rules_exact(self):
  self.assertEqual(MODEL["selectedQuestionDispositions"],OLD["selectedQuestionDispositions"])
  self.assertEqual(MODEL["selectedSharedRules"],OLD["selectedSharedRules"])
 def test_all11_conditional_records_exact(self):
  self.assertEqual(MODEL["conditionalBranchRegister"],OLD["conditionalBranchRegister"])
  self.assertEqual(len(MODEL["conditionalBranchRegister"]),11)
 def test_every_complete_terminal_matches(self):
  for c in NEW.values():self.assertEqual(c["expectedFinalState"],c["timeline"][-1]["after"],c["id"])
 def test_full_case_and_current_evidence_mirrors(self):
  self.assertEqual(MODEL["currentVectors"],json.loads((ROOT/"CASE_DISPOSITIONS.json").read_bytes())["cases"])
  self.assertEqual(MODEL["currentVectors"],json.loads((ROOT/"evidence/worked_cases.json").read_bytes()))
 def test_all_class_engines_unchanged(self):
  for cid in NEW:
   for who,a in NEW[cid]["actorDefinitions"].items():self.assertEqual(a["completeEngine"],BEFORE[cid]["actorDefinitions"][who]["completeEngine"])
for idx,(cid,event,who) in enumerate(ROWS,1):
 def method(self,cid=cid,event=event,who=who):
  e=NEW[cid]["timeline"][event]
  self.assertTrue(e["before"]["actors"][who]["action"])
  self.assertFalse(e["after"]["actors"][who]["action"])
 setattr(ActionLedgers,f"test_exact_debit_{idx:02d}",method)
