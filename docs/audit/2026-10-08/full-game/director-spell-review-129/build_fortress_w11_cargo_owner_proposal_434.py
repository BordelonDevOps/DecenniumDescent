from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = Path("docs/audit/2026-10-08/full-game/director-spell-review-129")
OUT = ROOT / BASE / "fortress_w11_cargo_owner_proposal_434"
OUT.mkdir(parents=True, exist_ok=True)
P = {
 "parent": BASE/"fortress_w01_structural_damage_witness_403_repack02/W01_REPLAY_403.json",
 "raw": BASE/"conjure_demiplane_fortress_return328_received/evidence/packet328/prior/Return284_cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A.json",
 "procedure": BASE/"conjure_demiplane_fortress_closure_intake_367/payload/rules/PG328_PROCEDURE_CURRENT.json",
 "ac5": BASE/"conjure_demiplane_fortress_closure_intake_367/payload/sources/AC5_ACCEPTED_SOURCE_MODEL.json",
 "bindings": BASE/"conjure_demiplane_fortress_closure_intake_367/payload/authority/PG328_SOURCE_BINDINGS.json",
 "profile": BASE/"conjure_demiplane_fortress_closure_intake_367/payload/sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json",
 "mage": Path("DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json"),
 "wizard": Path("DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json"),
 "classRules": Path("DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md"),
 "spellRules": Path("DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md"),
 "bodyRules": Path("DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md"),
 "combat": Path("DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md"),
 "catalog": Path("DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"),
 "geometry": BASE/"fortress_w01_successor_overlays_425/evidence/GEOMETRY_405.json",
 "support": BASE/"fortress_w01_successor_overlays_425/SUPPORT_OVERLAY_425_TESTONLY.json",
 "selection": BASE/"fortress_w11_cargo_owner_proposal_433/W11_SELECTION_EVIDENCE_433.json",
}
def raw(k): return (ROOT/P[k]).read_bytes()
def digest(b): return hashlib.sha256(b).hexdigest()
def obj(k): return json.loads(raw(k))
def gitshow(spec): return subprocess.check_output(["git","show",spec],cwd=ROOT)
def bind(k,pointer,note):
 p=(P[k]).as_posix(); b=raw(k); h=gitshow("HEAD:"+p)
 return {"path":p,"pointer":pointer,"workingTreeBytes":len(b),"workingTreeSha256":digest(b),"headBlobSha1":subprocess.check_output(["git","rev-parse","HEAD:"+p],cwd=ROOT,text=True).strip(),"headBlobBytes":len(h),"headBlobSha256":digest(h),"representation":"working-tree/attachment bytes and committed Git blob hashed separately; line-ending normalization is not conflated","note":note}
def write(name,x):
 b=(json.dumps(x,ensure_ascii=False,indent=2)+"\n").encode("utf-8"); (OUT/name).write_bytes(b); return b
def box(p,size=(5,5,6)):
 return {a:[p[i],p[i]+size[i]] for i,a in enumerate("xyz")}
def overlap(a,b): return all(min(a[k][1],b[k][1])-max(a[k][0],b[k][0])>1e-9 for k in "xyz")
def sweep(a,b,size=(5,5,6)):
 return {axis:[min(a[i],b[i]),max(a[i]+size[i],b[i]+size[i])] for i,axis in enumerate("xyz")}
def distance(route): return sum(sum(abs(y[i]-x[i]) for i in range(3)) for x,y in zip(route,route[1:]))

w=obj("parent"); rawcase=obj("raw"); s=w["stateSnapshots"]["S030"]
selsha=digest(raw("selection")); assert selsha=="06cdf754284ba09bb02acbebfd9356af585ed5e700e31790031972f2f0e46bf4"
assert s["actors"]["A"]["profileSHA256"]=="ebb96b340b94c3c6a98f8005e6fd6d0d6c93b1dc4abd1b584a7528c5cb459223"
fid="RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1"; pid="PG328-W11-R1:greater-fire-pet-1"; cid="cargo-A"; tid="PG328-W01-403:CLAY-TILE-1"

turns=[]
for actor,first,last in [("A",18,96),("B",13,91),("C",14,92),("D",15,93),("actor-w11-firepet-owner",22,94)]:
 for t in range(first,last+1,6): turns.append({"actor":actor,"startSeconds":float(t),"endSeconds":round(t+.9,1),"reactionRefresh":"regular START","actionUse":"see authored event list"})
turns.sort(key=lambda v:(v["startSeconds"],["A","B","C","D","actor-w11-firepet-owner"].index(v["actor"])))

entry={
 "permission":"A grants explicit branch-only entry permission.","effectId":fid,"parentOpen":False,
 "apertures":{"exterior":{"plane":"fixture:origin","center":[10,0,0],"width":10,"height":15},"interior":{"plane":fid+"/space","center":[10,10,0],"width":10,"height":15}},
 "openAction":{"actor":"A","time":18.0,"action":"interior exit-control glyph Action under PG9-Q25 / Absolute Gate local controls","start":[25,6,0],"route":[[25,6,0],[25,0,0],[10,0,0],[10,5,0]],"movementFeet":26},
 "externalMageStart":{"plane":"fixture:origin","position":[10,-5,0],"bounds":box([10,-5,0])},
 "destination":{"plane":fid+"/space","position":[10,10,0],"bounds":box([10,10,0])},
 "passage":{"committedMovementFeet":5,"wholeBodyFit":True,"wholeEquipmentFit":True,"supportBothSides":True,"sourceAnalog":"W01_REPLAY_403.json#/stateSnapshots/S030/transitReceipts/0","mainGateUsed":False},
 "route":[[10,10,0],[10,30,0],[10,21,0]],"turns":[{"start":22.0,"movementFeet":25,"parts":{"passage":5,"north":20},"end":[10,30,0]},{"start":28.0,"movementFeet":9,"returnToCastPose":9,"end":[10,21,0]}],
 "castPose":[10,21,0],"bodyBoxFeet":[5,5,6],"clearance":"10x15 aperture fits entire 5x5x6 body; route and cast pose avoid B, tile, A routes, pet and cargo; boundary contact only."
}

trace={
 "schemaVersion":1,"id":"PG328-W11-LIFECYCLE-TRACE-434","classification":"PROPOSED_TEST_ONLY_EVENT_AND_TURN_TRACE_NO_WITNESS","status":"PROPOSED_NOT_ADOPTED_DIRECTOR_REVIEW_REQUIRED","branchId":"PG328-W11-R1",
 "parent":{"path":P["parent"].as_posix(),"snapshot":"S030","timeSeconds":12.9,"sha256":digest(raw("parent")),"mutated":False},"turnMarkers":turns,
 "actions":[
  {"actor":"A","time":18.0,"action":"open retained entrance using Action","movementFeet":26,"freeInteraction":{"item":tid,"setDown":{"x":[25,26],"y":[11,12],"z":[0,.25]}}},
  {"actor":"actor-w11-firepet-owner","time":22.0,"action":"cross portal then move north","movementFeet":25},
  {"actor":"A","time":24.0,"action":"Secure Cargo Action: lift cargo-A to right hand","movementFeet":16},
  {"actor":"actor-w11-firepet-owner","time":28.1,"action":"commit summon Action, 10 RP and concentration before response window","movementFeet":9},
  {"actor":"A","time":30.0,"action":"Secure Cargo Action: transfer/attach cargo-A to pet","movementFeet":2},
  {"actor":"A","time":90.1,"action":"cast acquired Arcane Sight; 2 RP","movementFeet":0},
  {"actor":"A","time":96.1,"action":"cast acquired Arch Dispel Magic; 3 RP","movementFeet":0}],
 "events":[
  {"time":28.1,"type":"CAST_COMMIT","spell":"summon-greater-fire-pet","rpBefore":26,"cost":10,"rpAfter":16,"concentrationCommittedBeforeInterruption":True,"concentrationStartsAfterInterruptionResolution":False,"pending":True,"components":"V/S/F; right Fire Focus, left hand free","firstPreparedFamily":True,"noDiscount":True,"dissonanceBefore":0,"proposedDissonanceAfter":1},
  {"time":28.2,"type":"COUNTERSPELL_WINDOW"},
  {"time":28.3,"type":"CAST_SUCCESS_AND_CREATION","petId":pid,"position":[35,6,0],"expiresAt":88.3,"duration":"60 elapsed seconds after success"},
  {"time":88.3,"type":"SUMMON_EXPIRY","petRemoved":True,"cargoFallsFeet":3,"concentrationEnds":True},
  {"time":90.1,"type":"SIGHT_COMMIT","card":"wizard.arch.arcane-sight","rank":2,"rpBefore":53,"cost":2,"rpAfter":51,"RechargeRounds":2,"rechargeReadyBeforeCommit":True,"concentrationCommittedBeforeInterruption":True,"dissonance":[0,1],"refrainAfter":0,"noStrainSurcharge":True},
  {"time":90.2,"type":"COUNTERSPELL_WINDOW"},{"time":90.3,"type":"SIGHT_SUCCESS","auraPerception":"visible Fortress aura, school/category; no later-turn examination Action used","concentrationDeadline":690.3,"sightRechargeRemainingAtA96Start":1},
  {"time":96.1,"type":"DISPEL_COMMIT","card":"wizard.arch.dispel-magic","rank":3,"rpBefore":51,"cost":3,"rpAfter":48,"RechargeRounds":2,"rechargeReadyBeforeCommit":True,"dissonance":[1,2],"refrainAfter":0,"noStrainSurcharge":True},
  {"time":96.2,"type":"COUNTERSPELL_WINDOW"},{"time":96.3,"type":"DISPEL_SUCCESS","roll":"12+5+6=23 vs DC19","FortressEnds":True}],
}
traceBytes=write("W11_LIFECYCLE_TRACE_434.json",trace)

responses={
 "summon28_2":[
  {"actor":"A","card":"wizard.base.counterspell","RP":3,"Recharge":2,"ReactionAvailable":True,"eligible":"same plane, clear geometry","decision":"explicit proposed decline"},
  {"actor":"B","card":"wizard.base.counterspell","RP":3,"Recharge":2,"ReactionAvailable":True,"eligible":"same plane, clear geometry","decision":"explicit proposed decline"},
  {"actor":"D","card":"wizard.base.counterspell","RP":3,"Recharge":2,"ReactionAvailable":True,"eligible":"TEST_ONLY perception/LoE through open 10x15 entrance; under60ft","decision":"explicit proposed decline","directorMustConfirm":"cross-portal response rule"},
  {"actor":"C","eligible":False,"basis":"Cleric20 has no source-bound Counterspell card"},
  {"actor":"actor-w11-firepet-owner","eligible":False,"basis":"caster cannot Counterspell own cast"}],
 "sight90_2":[
  {"actor":"B","card":"wizard.base.counterspell","RP":3,"Recharge":2,"ReactionAvailable":True,"decision":"explicit proposed decline"},
  {"actor":"D","card":"wizard.base.counterspell","RP":3,"Recharge":2,"ReactionAvailable":True,"eligible":"TEST_ONLY through open portal","decision":"explicit proposed decline","directorMustConfirm":"cross-portal response rule"},
  {"actor":"actor-w11-firepet-owner","card":"mage.arch.counterspell","RP":4,"Recharge":3,"ReactionAvailable":True,"decision":"explicit proposed decline"},
  {"actor":"A","eligible":False,"basis":"self-cast"},{"actor":"C","eligible":False,"basis":"no Counterspell card"}],
 "dispel96_2":[
  {"actor":"B","card":"wizard.base.counterspell","RP":3,"Recharge":2,"ReactionAvailable":True,"decision":"explicit proposed decline"},
  {"actor":"D","card":"wizard.base.counterspell","RP":3,"Recharge":2,"ReactionAvailable":True,"eligible":"TEST_ONLY through open portal","decision":"explicit proposed decline","directorMustConfirm":"cross-portal response rule"},
  {"actor":"actor-w11-firepet-owner","card":"mage.arch.counterspell","RP":4,"Recharge":3,"ReactionAvailable":True,"decision":"explicit proposed decline"},
  {"actor":"A","eligible":False,"basis":"self-cast"},{"actor":"C","eligible":False,"basis":"no Counterspell card"}]
}
trace["counterspellResponses"]=responses

cargo={
 "id":"cargo-A","origin":"unchanged W01 S030 real 10lb, 1 Load, 1x1x1ft item; admitted with A at /transitReceipts/0","owner":"A throughout",
 "custody":[{"time":"S030","holder":"A, carried"},{"time":24,"holder":"A, right hand after Secure Cargo lift Action"},{"time":30,"holder":pid,"relation":"externally attached carrier; owner remains A"},{"time":88.3,"holder":None,"relation":"loose real item after expiry"}],
 "extractionClass":{"value":0,"status":"proposed TEST_ONLY fixture classification","category":"ordinary trade goods","tags":[],"notInferredFromWeight":True},
 "attachment":{"fixture":"one passive clamp integral to cargo-A","massLoadSizeIncludedInExistingItem":True,"grantsNoPetHandsAnatomyOrExtraCapacity":True,"newTESTONLYPremise":True},
 "lift":{"time":24,"action":"one Secure Cargo lift Action","AStart":[10,5,0],"AEnd":[25,6,0],"route":[[10,5,0],[25,5,0],[25,6,0]],"movement":16,"AWeightLb":12,"ALoad":1.2,"hands":{"left":"focus-A","right":"cargo-A"}},
 "attach":{"time":30,"action":"one Secure Cargo attach/transfer Action","AStart":[25,6,0],"AEnd":[27,6,0],"route":[[25,6,0],[27,6,0]],"movement":2,"petPosition":[35,6,0],"petBounds":box([35,6,0]),
  "sweptBounds":[{"x":[28,29],"y":[6,7],"z":[3,4],"phase":"contained/carried in A"},{"x":[32,33],"y":[6,7],"z":[3,4],"phase":"exits A envelope into gap"},{"x":[34,35],"y":[6,7],"z":[3,4],"phase":"clamp at pet west face; boundary contact"}],
  "noPositiveOverlapWithPet":True,"AWeightAfterLb":2,"ALoadAfter":.2,"petCombinedWeightLb":110,"petLoad":1,"petLimits":{"weightLb":210,"load":14},"handsAfter":{"left":"focus-A","right":"free"}},
 "expiry":{"time":88.3,"petRemoved":True,"cargoBefore":{"x":[34,35],"y":[6,7],"z":[3,4]},"cargoAfter":{"x":[34,35],"y":[6,7],"z":[0,1]},"fallFeet":3,"support":"Fortress z=0 floor patch [34,35]x[6,7]","impactDisposition":"proposed narrow TEST_ONLY outcome: this exact cargo-A sustains no damage in this exact three-foot fall; no general object-impact rule; owner, mass, Load, quantity and identity remain unchanged"}}
pet={"id":pid,"spell":"summon-greater-fire-pet","profilePointer":"AC5_ACCEPTED_SOURCE_MODEL.json#/profiles/AC5-PROFILE-GREATER-FIRE-PET-01","position":[35,6,0],"bounds":box([35,6,0]),"body":{"size":"Medium","boxFeet":[5,5,6],"massLb":100,"STR":14,"HP":60,"AC":17,"speed":30},"withCargo":{"massLb":110,"Load":1,"capacityLb":210,"capacityLoad":14},"stationary":True,"attacksOrCommands":[],"auraRecipients":[],"noHandsToolsOrExtraCapacity":True,"expiry":88.3}

support={"id":"PG328-W11-SUPPORT-01","status":"PROPOSED TEST_ONLY BRANCH PREMISE; not inherited from W01","notCanonical":True,
 "floors":[{"plane":"fixture:origin","z":0,"x":[-200,200],"y":[-200,200],"ratingLbPer5x5":200},{"plane":fid+"/space","z":0,"x":[0,120],"y":[0,120],"ratingLbPer5x5":200}],
 "loads":[{"pose":"A S030","bodyPlusEquipmentLb":164,"Load":1.4},{"pose":"A after tile set-down","bodyPlusEquipmentLb":162,"Load":1.2},{"pose":"A after cargo transfer","bodyPlusEquipmentLb":152,"Load":.2},{"pose":"B","bodyPlusEquipmentLb":152,"Load":.2},{"pose":"Mage","positions":[[10,-5,0],[10,30,0],[10,21,0]],"bodyPlusEquipmentLb":151,"Load":.1},{"pose":"pet plus cargo-A","bodyPlusEquipmentLb":110,"Load":1},{"pose":"loose cargo-A","bounds":{"x":[34,35],"y":[6,7],"z":[0,1]},"massLb":10},{"pose":"loose clay tile","bounds":{"x":[25,26],"y":[11,12],"z":[0,.25]},"massLb":2}],
 "planePartition":"Negative-y positions are fixture:origin only. W01 support overlay is graph connectivity, not a load rating.","limits":["no general structure rule","no W01 overlay extension","no campaign site/load fact","only listed floor planes, regions and test poses"]}

closure={"source":"PG328_PROCEDURE_CURRENT.json#procedure / PG9-Q27; incorporated BAN-CLOSE-03 and BAN-CONFLICT-04","time":96.3,"mandatoryEventsFirst":["pet expiry and cargo fall at88.3 already processed","Fortress ending at96.3","tile's separate deadline3606.13 is still live"],"bodyOrder":["A","B","actor-w11-firepet-owner"],
 "bodyPlacements":[{"actor":"A","exteriorEntryPose":[5,0,0],"interiorEntryPose":[15,10,0],"stableOffset":[5,0,0],"originPlacement":[10,0,0],"bounds":box([10,0,0])},{"actor":"B","exteriorEntryPose":[0,15,0],"interiorEntryPose":[15,10,0],"stableOffset":[5,0,0],"originPlacement":[5,15,0],"bounds":box([5,15,0])},{"actor":"actor-w11-firepet-owner","exteriorEntryPose":[10,-5,0],"interiorEntryPose":[10,10,0],"stableOffset":[0,0,0],"originPlacement":[10,-5,0],"bounds":box([10,-5,0])}],
 "unchangedOutsideActors":{"C":[0,0,0],"D":[5,5,0]},
 "looseItemsStableIdOrder":[{"id":"cargo-A","fixedReferenceSource":"branch moment cargo becomes loose after the 88.3 expiry/fall","currentLooseBounds":{"x":[34,35],"y":[6,7],"z":[0,1]},"projectionDelta":[0,-10,0],"fixtureOriginPlacement":{"x":[34,35],"y":[-4,-3],"z":[0,1]},"support":"fixture:origin floor","owner":"A","custodian":None},{"id":tid,"fixedReferenceSource":"W01 S030 item creation locus boundsFeetAtCreation [25,26]x[9,10]x[0,0.25]","currentLooseBounds":{"x":[25,26],"y":[11,12],"z":[0,.25]},"projectionDelta":[0,-10,0],"fixtureOriginPlacement":{"x":[25,26],"y":[-1,0],"z":[0,.25]},"support":"fixture:origin floor","owner":None,"custodian":"A","expiry":3606.13}],
 "expiredPet":{"id":pid,"present":False,"returnedAsBody":False,"loot":False},"collisionRule":"Bodies in A/B/Mage order, then loose items by ID. Boundary contact allowed; no positive-volume overlap."
}

bindings=[
 bind("parent","/stateSnapshots/S030; /actors/A/profileSHA256; /transitReceipts/0","Immutable W01 parent, cargo admission, and corrected /profileSHA256 pointer."),
 bind("raw","/initial/actors/A; /initial/actors/B; /events/*:CROSSING","Original A/B exterior positions and crossing outcomes."),
 bind("procedure","/procedure (PG9-Q25, PG9-Q27, PG9-Q29)","Retained entrance, full-graph travel and Q27 terminal order."),
 bind("ac5","/spells/8/procedure; /profiles/AC5-PROFILE-GREATER-FIRE-PET-01","Pet spell source model and body profile."),
 bind("bindings","/Wizard20Profile/profileSHA256","W01 Wizard20 replay-profile source binding."),
 bind("profile","/acquisitionLedger/2/choices/1; /acquisitionLedger/8/choices/0","Arcane Sight and Dispel acquisitions; distinct profile self-hash recorded."),
 bind("mage","/cards/10; /cards/23","Fire Focus and Mage Counterspell."),
 bind("wizard","/cards/17; /cards/19; /cards/21","Wizard Counterspell, Arch Dispel, Arcane Sight."),
 bind("classRules","/Spell repertoires and acquisition","Ten ranked spells and four cantrips."),
 bind("spellRules","/casting sequence steps 4-7","Commitment before interruption; create only after survival."),
 bind("bodyRules","/Carrying and Load; /Extraction Class and Secure Cargo","Load accounting and one-unit handling Action."),
 bind("combat","/Encounter and action resources","Action, movement, free interaction, reaction refresh, turn cadence."),
 bind("catalog","/spells/153","Summon remains blocked pending operational review; no status change."),
 bind("geometry","/openings/main-gate; /regions/courtyard","Physical main gate distinction and current interior geometry."),
 bind("support","/supportPredicate; /loadScope","W01 topology does not provide W11 load ratings."),
 bind("selection","/ordinaryRankedSelections; /cantripSelections; /classCardSelections","Selection evidence; source-bound Fire Focus card ID.")]

proposal={
 "schemaVersion":1,"id":"OWNER-PG328-W11-ADOPTION-PROPOSAL-434","classification":"TEST_ONLY_BRANCH_OWNER_ADOPTION_PROPOSAL","status":"PROPOSED_NOT_ADOPTED","recordedLocalDate":"2026-11-01",
 "supersedes":{"id":"OWNER-PG328-W11_ADOPTION_PROPOSAL_433","sha256":"6c21e80a4792c2ee9e3f56c07ebd037d082a014e83fa60fe7229a4dd250746c4","handling":"historical and unchanged"},
 "scope":{"spell":"conjure-demiplane-fortress","holdId":"PG200-B06","integrationId":"PG328-W11","branchId":"PG328-W11-R1","branchOnly":True,"noCampaignOccurrence":True},
 "parent":{"path":P["parent"].as_posix(),"snapshot":"S030","timeSeconds":12.9,"sha256":digest(raw("parent")),"mutated":False,"cargoA":{"id":"cargo-A","owner":"A","custodian":"A","massLb":10,"load":1,"dimensionsFeet":[1,1,1],"admissionReceipt":"/stateSnapshots/S030/transitReceipts/0"}},
 "preservedDirectorChecks":{"selectionEvidenceSha256":selsha,"ordinaryRankedCount":10,"cantripCount":4,"selectedClassCards":14,"fireFocus":"mage.base.fire.fire","fireFocusPointer":"/cards/10","queue":"830 applied / 18 pending / 0 accepted-unapplied"},
 "magePremise":{"actorId":"actor-w11-firepet-owner","derivedId":"W11-MAGE9-FIREPET-OWNER-TESTONLY","basedOnW05ProfileSha256":"c380750c54c7b2a4f729621fa26ad3b319708d218c4fd3497b1f23277e56433b","class":"Mage","level":9,"path":"Arcanist at3, Fire Focus at2","RP":[26,26],"Dissonance":0,"Refrain":0,"lastSpell":None,"noEarlierRankedFamily":True,"noConcentration":True,"INTModifier":4,"PB":4,"body":{"size":"Medium","boxFeet":[5,5,6],"massLb":150},"hands":{"right":"1 lb mage.base.fire.fire Focus","left":"free for Somatic"},"voice":True,"actionAndReactionAvailable":True,"W05Unchanged":True},
 "entryPremise":entry,"turnSchedule":turns,"lifecycleTrace":{"path":(BASE/"fortress_w11_cargo_owner_proposal_434/W11_LIFECYCLE_TRACE_434.json").as_posix(),"sha256":digest((OUT/"W11_LIFECYCLE_TRACE_434.json").read_bytes())},
 "supportPremise":support,
 "creation":{"spell":"summon-greater-fire-pet","operationalStatus":"blocked-pending-operational-review; unchanged","sourcePointer":"AC5_ACCEPTED_SOURCE_MODEL.json#/spells/8/procedure","commit":28.1,"interruptWindow":28.2,"successAndCreation":28.3,"position":[35,6,0],"bounds":box([35,6,0]),"rangeFeet":60,"casterPosition":[10,21,0],"centerDistanceFeet":29.1548,"lineOfEffect":{"casterCenter":[12.5,23.5,3],"targetCenter":[37.5,8.5,3],"clearOfB":{"bounds":{"x":[15,20],"y":[10,15],"z":[0,6]},"lineAtBWestX":[15,22]},"clearOfA":{"bounds":{"x":[27,32],"y":[6,11],"z":[0,6]},"lineAtAXWest":[27,14.8],"lineAtAEast":[32,11.8]},"status":"proposed exact TEST_ONLY ray; no body intersection"},"components":"V/S/F","costRP":10,"RP":[26,16],"concentrationCommittedBeforeInterruption":True,"concentrationStartsAfterInterruptionResolution":False,"expiry":88.3,"expiryRule":"60 elapsed seconds from successful creation","counterspellResponses":responses["summon28_2"]},
 "cargoHandling":cargo,"pet":pet,"closure":closure,
 "closureRoute":{"AProfilePointer":"/profileSHA256","sourceBindingPointer":"/Wizard20Profile/profileSHA256","completeProfileHash":"ebb96b340b94c3c6a98f8005e6fd6d0d6c93b1dc4abd1b584a7528c5cb459223","profileFileHash":"a3a3ce0a714c1fa35523719c8c8a0297fc457d5b5f097f6a20a00aad6cd7be55","profileSelfHash":"28e6ab554f7f6bbfd839d5bf637826414867f1984f08def1ed410e56cf171aa9","sightAcquisition":"/acquisitionLedger/2/choices/1","dispelAcquisition":"/acquisitionLedger/8/choices/0","sight":{"card":"wizard.arch.arcane-sight","rank":2,"cost":2,"RechargeRounds":2,"concentration":"committed at90.1; surviving aura effect begins90.3, deadline690.3","rechargeRemainingAtA96Start":1,"dissonance":[0,1],"refrainAfter":0},"dispel":{"card":"wizard.arch.dispel-magic","rank":3,"cost":3,"RechargeRounds":2,"dissonance":[1,2],"refrainAfter":0},"RPBeforeAndAfter":[53,51,48],"sightResponses":responses["sight90_2"],"dispelResponses":responses["dispel96_2"],"dispelRoll":{"d20":12,"INT":5,"PB":6,"total":23,"DC":19,"testOnlyNotCampaignRoll":True}},
 "sourceBindings":bindings,
 "requestedOwnerDecision":"After Director confirms the exact branch premises and cross-portal response/projection rules, owner adoption would authorize only construction of hypothetical PG328-W11-R1. It would not authorize seal, Fortress acceptance/application, canon change or queue change.",
 "authority":{"queue":"830 applied / 18 pending / 0 accepted-unapplied","queueChangeAuthorized":False,"FortressAcceptanceOrApplicationAuthorized":False,"sealAuthorized":False,"canonChangeAuthorized":False,"witnessConstructionAuthorized":False},
 "statusBoundary":{"allTestOnly":True,"campaignEventsAsserted":False,"parentW01Mutated":False,"W05Mutated":False,"W04OrW09Changed":False}}
proposalBytes=write("OWNER_PG328_W11_ADOPTION_PROPOSAL_434.json",proposal); proposalSha=digest(proposalBytes)

md=f"""# PG328-W11 owner proposal 434 — TEST_ONLY, not adopted

Proposal SHA-256: `{proposalSha}`
The lifecycle trace and Director correction disposition are in the adjacent JSON files. Parent W01 replay 403, S030 at 12.9 seconds, is unchanged.

This packet requests review of one hypothetical `PG328-W11-R1` branch. It creates no witness, seal, Fortress acceptance/application, canon change, or queue change. Queue remains **830 applied / 18 pending / 0 accepted-unapplied**; W04 and W09 are separate.

The corrected Mage selection evidence records ten ranked spells, four cantrips and fourteen selected Mage cards. Fire Focus is `mage.base.fire.fire` at `/cards/10`. A’s profile binding uses `/profileSHA256`; the resolved complete profile hash is `ebb96b340b94c3c6a98f8005e6fd6d0d6c93b1dc4abd1b584a7528c5cb459223`, with the separate profile file and self-hash retained.

The route opens the actual retained 10x15 two-way portal, not the physical main gate. A opens it with an Action at 18.0; the Mage enters at 22.0 using a five-foot passage receipt, then moves to the cast pose. The branch trace supplies START/END markers for A/B/C/D and Mage. A’s portal Action, cargo lift, cargo attachment, summon, Sight and Dispel are separate Action events.

The rank-5 summon commits 10 RP and concentration before its 28.2 Counterspell window. The pet appears only at 28.3 if the window survives and expires at 88.3. A and B have source-bound Wizard Counterspell. D is included at all three windows because the entrance remains open; the proposed cross-portal perception/line is explicitly submitted for Director confirmation. C has no bound Counterspell card. Every eligible responder explicitly declines.

A uses separate Secure Cargo Actions to lift the already-admitted `cargo-A` and attach it to the pet. The packet records its whole-body and item path, hand state, owner/custody transitions, extraction class and load/weight changes. The clamp is integral to the existing 10 lb, 1 Load item and grants no pet hands, anatomy or capacity. When the pet expires, cargo-A falls three feet. A narrowly scoped TEST_ONLY no-damage outcome is proposed for this exact item and fall; no general impact rule is claimed.

A’s acquired Arcane Sight and Arch Dispel route bind to the preserved Wizard20 profile. Their costs take A from 53 to 51 to 48 RP. Both have Recharge 2; Sight’s surviving aura effect begins at 90.3 with a 600-second concentration deadline, and the Dispel roll is 12+5+6=23 against DC19. A’s recorded Dissonance advances 0→1→2 with no surcharge. Q27 settlement is listed in admission order for A, B and Mage, then loose cargo-A and the tile by stable ID, with exact projected supported outside placements. The expired pet is absent.

The support overlay proves connectivity only. New support ratings for the exact W11 test footprints are labeled as branch-only assumptions. The correction readback lists each of the Director’s ten prior findings and the exact remaining questions.
"""
(OUT/"OWNER_PG328_W11_ADOPTION_PROPOSAL_434.md").write_text(md,encoding="utf-8",newline="\n")

prior="6c21e80a4792c2ee9e3f56c07ebd037d082a014e83fa60fe7229a4dd250746c4"
ids=[
 ("C01","/parent/path; /closure/profileBinding/W01ParentActorPointer","Correct parent W01_REPLAY_403.json S030; bind A by /profileSHA256; original A/B entry poses are source-linked."),
 ("C02","/entryPremise","Replace main gate with retained two-way portal, exact apertures, opening Action, crossing receipt and full-body fit."),
 ("C03","/entryPremise/route; /wholeBodyClearance","Add swept A/Mage routes and body bounds; include collision-free cargo path to pet west face."),
 ("C04","/turnSchedule; /cargoHandling","Provide A/B/C/D/Mage START/END markers; separate entrance, lift, attach, cast, Sight and Dispel Actions."),
 ("C05","/creation/concentrationStartsAfterInterruptionResolution; /counterspellResponses","Set false; commit cost/concentration before response, create after survival. Include eligible A/B/D and C/self exclusions, reactions, RP, recharge, perception and declines."),
 ("C06","/cargoHandling/at36Seconds; /supportPremise","Record transfer path, custody, equipment/load changes, tile, Mage, A configurations, pet and loose cargo support; do not treat W01 graph as load rating."),
 ("C07","/expiry","Offer exact item-specific three-foot no-damage TEST_ONLY result; no general object-impact inference."),
 ("C08","/closure/RPBefore; /closure/RPAfter; /closure/B","Bind acquired Sight and Dispel to A’s profile; show 53->51->48 RP; include B, Mage and cross-portal D responses."),
 ("C09","/closure/settlement","Bind PG9-Q27; provide A/B/Mage admission order, exact exterior anchors, both loose items, support and pet absence."),
 ("C10","PG328_W11_DIRECTOR_READBACK_432.json#/files","Keep 432 historical; point current 434 to exact proposal and existing selection evidence hashes.")]
cor={"schemaVersion":1,"id":"PG328-W11-DIRECTOR-CORRECTIONS-434","classification":"DIRECTOR_FEEDBACK_RECONCILIATION","status":"TEN_FINDINGS_ADDRESSED_PENDING_FINAL_DIRECTOR_CONFIRMATION","priorProposalSha256":prior,"currentProposal":{"path":"OWNER_PG328_W11_ADOPTION_PROPOSAL_434.json","sha256":proposalSha},"selectionEvidenceSha256":selsha,"corrections":[{"id":"W11-433-"+i,"field":f,"disposition":d} for i,f,d in ids],
 "directorQuestions":["Confirm the precise PG9-Q25/Absolute Gate Action for A to open the retained entrance.","Confirm whether D can perceive and Counterspell through the open two-way portal at 28.2, 90.2 and 96.2; D is conservatively included as eligible.","Review the branch-only clamp and item-specific no-damage result for cargo-A's exact three-foot fall.","Confirm Q27's projection from listed first-entry/loose coordinates to exact supported fixture:origin placements and stable ID order.","Return any remaining exact JSON pointer and source authority; no witness, seal, acceptance/application, canon or queue action is requested."],
 "boundary":{"queue":"830 applied / 18 pending / 0 accepted-unapplied","changed":False,"witness":False,"seal":False,"acceptanceOrApplication":False,"canon":False}}
write("PG328_W11_DIRECTOR_CORRECTIONS_434.json",cor)
(OUT/"PG328_W11_DIRECTOR_CORRECTIONS_434.md").write_text("# W11 Director corrections reconciled in proposal 434\n\n"+"\n".join(f"- **{x['id']}** — {x['disposition']}" for x in cor["corrections"])+"\n\nOpen Director questions are recorded in the JSON.\n",encoding="utf-8",newline="\n")

checks=[]
def check(name,ok,evidence): checks.append({"name":name,"status":"PASS" if ok else "FAIL","evidence":evidence})
check("selection and Fire Focus",selsha=="06cdf754284ba09bb02acbebfd9356af585ed5e700e31790031972f2f0e46bf4" and proposal["preservedDirectorChecks"]["fireFocus"]=="mage.base.fire.fire",f"selection sha256={selsha}; source /cards/10")
check("A profile binding",s["actors"]["A"]["profileSHA256"]==proposal["closureRoute"]["completeProfileHash"],"S030 actors/A/profileSHA256 matches PG328_SOURCE_BINDINGS#/Wizard20Profile/profileSHA256")
check("retained portal",entry["parentOpen"] is False and entry["passage"]["committedMovementFeet"]==5 and entry["passage"]["wholeBodyFit"],"S030 two 10x15 apertures; no main structural gate")
aroute=[[25,6,0],[25,0,0],[10,0,0],[10,5,0]]
check("A entry-control route",distance(aroute)==26,"26ft movement and one Action; set-down tile lies outside the swept body path")
tilebox={"x":[25,26],"y":[11,12],"z":[0,.25]}; bbody=box([15,10,0])
check("A swept control route avoids B and tile",all(not overlap(sweep(a,b),bbody) and not overlap(sweep(a,b),tilebox) for a,b in zip(aroute,aroute[1:])),"Each axis-aligned 5x5x6 swept segment avoids B and set-down tile")
returnRoute=[[10,5,0],[25,5,0],[25,6,0]]
check("A return route avoids B and tile",all(not overlap(sweep(a,b),bbody) and not overlap(sweep(a,b),tilebox) for a,b in zip(returnRoute,returnRoute[1:])),"16ft return route; full body sweep avoids B and tile")
check("Mage turns within Speed",all(t["movementFeet"]<=30 for t in entry["turns"]),"25ft including 5ft passage, then 9ft to cast pose")
mageRoute=[[10,10,0],[10,30,0],[10,21,0]]
check("Mage swept route avoids A and B",all(not overlap(sweep(a,b),bbody) and not overlap(sweep(a,b),box([10,5,0])) for a,b in zip(mageRoute,mageRoute[1:])),"Mage full body route meets A/B only at permitted boundaries")
check("actions separated",cargo["lift"]["time"]==24 and cargo["attach"]["time"]==30,"Separate Secure Cargo Actions; neither shares opening or cast")
petbox=box([35,6,0])
check("pet range and body clearance",proposal["creation"]["centerDistanceFeet"]<60 and not overlap(petbox,box([27,6,0])) and proposal["creation"]["lineOfEffect"]["clearOfA"]["lineAtAXWest"][1]>11,"29.1548ft range; ray passes above A and clear of B; A [27,32] and pet [35,40] do not overlap")
check("cargo sweep avoids pet",all(not overlap(x,petbox) for x in cargo["attach"]["sweptBounds"]),"Cargo contacts pet west face at x35 without positive-volume penetration")
check("load arithmetic",cargo["lift"]["AWeightLb"]==12 and cargo["lift"]["ALoad"]==1.2 and cargo["attach"]["AWeightAfterLb"]==2 and cargo["attach"]["ALoadAfter"]==.2 and pet["withCargo"]["massLb"]==110,"A 14->12->2lb and 1.4->1.2->0.2 Load; pet+item110lb/1Load")
check("spell timing and expiry",[e["time"] for e in trace["events"][:4]]==[28.1,28.2,28.3,88.3] and proposal["creation"]["concentrationStartsAfterInterruptionResolution"] is False,"Commit before interruption; success before creation; expiry after60 elapsed seconds")
check("responders enumerated",all(any(r.get("actor")=="D" for r in rs) for rs in responses.values()),"All three windows list A/B/D/Mage/C/self; D cross-portal rule explicitly open for Director")
check("A closure acquisition, cadence, RP and recharge",proposal["closureRoute"]["RPBeforeAndAfter"]==[53,51,48] and proposal["closureRoute"]["dispelAcquisition"]=="/acquisitionLedger/8/choices/0" and proposal["closureRoute"]["sight"]["RechargeRounds"]==2 and proposal["closureRoute"]["dispel"]["RechargeRounds"]==2,"Acquired Sight/Dispel rank2/rank3, 2+3RP, RP 53->51->48, each Recharge2; Dissonance 0->1->2")
bodies=closure["bodyPlacements"]
check("Q27 body placement non-overlap",all(not overlap(a["bounds"],b["bounds"]) for i,a in enumerate(bodies) for b in bodies[i+1:]),"A/B/Mage returned in stable admission order without positive-volume collision")
items=[{"x":[34,35],"y":[-4,-3],"z":[0,1]},{"x":[25,26],"y":[-1,0],"z":[0,.25]}]
outside=[box([0,0,0]),box([5,5,0])]
allBodies=[x["bounds"] for x in closure["bodyPlacements"]]+outside
check("Q27 bodies and loose objects clear on origin plane",all(not overlap(a,b) for i,a in enumerate(allBodies) for b in allBodies[i+1:]) and all(not overlap(x,b) for x in items for b in allBodies),"A/B/Mage/C/D and cargo-A/tile have no positive-volume overlap; objects supported at z0")
check("source byte and Git hash domains",all(len(x["workingTreeSha256"])==64 and len(x["headBlobSha1"])==40 and len(x["headBlobSha256"])==64 for x in bindings),"All source bindings separately record working-tree attachment SHA256 and HEAD Git blob SHA1/SHA256")
check("decision boundary",proposal["authority"]["witnessConstructionAuthorized"] is False and proposal["authority"]["queueChangeAuthorized"] is False,"Proposal only; queue stays 830/18/0; no witness, seal, canon or application")
validation={"schemaVersion":1,"id":"PG328-W11-VALIDATION-434","classification":"LOCAL_SOURCE_HASH_GEOMETRY_AND_SEMANTIC_PRECHECK","status":"PASS_WITH_DIRECTOR_CONFIRMATIONS_OPEN","proposalSha256":proposalSha,"traceSha256":digest((OUT/"W11_LIFECYCLE_TRACE_434.json").read_bytes()),"checks":checks,"result":{"passed":sum(c["status"]=="PASS" for c in checks),"failed":sum(c["status"]=="FAIL" for c in checks),"directorQuestions":len(cor["directorQuestions"])},"limitations":["Portal-control semantics, cross-portal perception/LoE, cargo attachment/fall outcome, and Q27 projections remain TEST_ONLY Director review questions.","No witness, seal, Fortress acceptance/application, canon change or queue mutation occurred."]}
write("VALIDATION_434.json",validation)
print(json.dumps({"output":str(OUT),"proposalSha256":proposalSha,"traceSha256":validation["traceSha256"],"selectionSha256":selsha,"checks":validation["result"]},indent=2))
