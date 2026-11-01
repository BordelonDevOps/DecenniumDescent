from __future__ import annotations
import copy, hashlib, json, math, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
REPO = REVIEW.parents[4]
PROPOSAL_PATH = REVIEW / "fortress_w05_w10_joint_preflight_443" / "PG328_W05_W10_JOINT_PROPOSAL_443_TESTONLY.json"
ADOPTION_PATH = REVIEW / "fortress_w05_w10_joint_preflight_443" / "OWNER_PG328_W05_W10_ADOPTION_443_TESTONLY.json"
PARENT_PATH = REVIEW / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
WITNESS_PATH = ROOT / "W05_W10_WITNESS_453_TESTONLY.json"
VALIDATION_PATH = ROOT / "BUILD_VALIDATION_453.json"
VERIFY_PATH = ROOT / "VERIFY_W05_W10_WITNESS_453.py"
README_PATH = ROOT / "README_WITNESS_453.md"
BUILDER_PATH = ROOT / "BUILD_W05_W10_WITNESS_453.py"
MANIFEST_PATH = ROOT / "MANIFEST_453.json"
ARCHIVE_PATH = ROOT / "DD_Fortress_W05_W10_Witness_453_TESTONLY.zip"
DELIVERY_PATH = ROOT / "DELIVERY_453.json"
EXPECTED_PROPOSAL_SHA = "1fd045800181958d34e141763e07fe230a2261a3879e8115869551c2a6d20b85"
EXPECTED_PARENT_SHA = "2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb"
ROOT_EFFECT_ID = "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1"
SPACE_ID = ROOT_EFFECT_ID + "/space"
TILE_ID = "PG328-W01-403:CLAY-TILE-1"

def canonical(value): return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def sha_bytes(data): return hashlib.sha256(data).hexdigest()
def sha(path): return sha_bytes(path.read_bytes())
def sha_obj(value): return sha_bytes(canonical(value))
def rel(path): return path.relative_to(REVIEW).as_posix()
def dump(path, value): path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
def ptr(parts):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)
def diff_ops(old, new, path=None):
    path = [] if path is None else path
    if isinstance(old, dict) and isinstance(new, dict):
        ops=[]
        for k in old:
            if k not in new: ops.append({"op":"remove","path":ptr(path+[k]),"oldValue":copy.deepcopy(old[k])})
        for k in new:
            if k not in old: ops.append({"op":"add","path":ptr(path+[k]),"value":copy.deepcopy(new[k])})
            else: ops.extend(diff_ops(old[k],new[k],path+[k]))
        return ops
    if isinstance(old,list) and isinstance(new,list):
        if len(old)<=len(new) and old==new[:len(old)]:
            return [{"op":"add","path":ptr(path+[i]),"value":copy.deepcopy(new[i])} for i in range(len(old),len(new))]
        if len(new)<=len(old) and new==old[:len(new)]:
            return [{"op":"remove","path":ptr(path+[i]),"oldValue":copy.deepcopy(old[i])} for i in range(len(old)-1,len(new)-1,-1)]
        return [] if old==new else [{"op":"replace","path":ptr(path),"oldValue":copy.deepcopy(old),"value":copy.deepcopy(new)}]
    return [] if old==new else [{"op":"replace","path":ptr(path),"oldValue":copy.deepcopy(old),"value":copy.deepcopy(new)}]
def inverses(forward):
    out=[]
    for op in reversed(forward):
        if op["op"]=="add": out.append({"op":"remove","path":op["path"],"oldValue":copy.deepcopy(op["value"])})
        elif op["op"]=="remove": out.append({"op":"add","path":op["path"],"value":copy.deepcopy(op["oldValue"])})
        else: out.append({"op":"replace","path":op["path"],"oldValue":copy.deepcopy(op["value"]),"value":copy.deepcopy(op["oldValue"])})
    return out
def apply_ops(doc, operations):
    doc=copy.deepcopy(doc)
    for op in operations:
        parts=[x.replace("~1","/").replace("~0","~") for x in op["path"].lstrip("/").split("/")]
        parent=doc
        for part in parts[:-1]: parent=parent[int(part)] if isinstance(parent,list) else parent[part]
        leaf=parts[-1]
        if isinstance(parent,list):
            i=int(leaf)
            if op["op"]=="add": parent.insert(i,copy.deepcopy(op["value"]))
            elif op["op"]=="remove": parent.pop(i)
            else: parent[i]=copy.deepcopy(op["value"])
        elif op["op"]=="add": parent[leaf]=copy.deepcopy(op["value"])
        elif op["op"]=="remove": del parent[leaf]
        else: parent[leaf]=copy.deepcopy(op["value"])
    return doc
def add_spec(specs,time,order,kind,details): specs.append({"timeSeconds":float(time),"orderAtTime":order,"kind":kind,"details":details})
def actor_center(actor): return [actor["position"][i]+actor["bodyBox"][i]/2 for i in range(3)]
def dist(a,b): return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

def main():
    proposal=json.loads(PROPOSAL_PATH.read_text(encoding="utf-8")); adoption=json.loads(ADOPTION_PATH.read_text(encoding="utf-8")); parent=json.loads(PARENT_PATH.read_text(encoding="utf-8"))
    inputs=proposal["ownerProposedInputs"]; initial=copy.deepcopy(parent["stateSnapshots"]["S030"]); initial_sha=sha_obj(initial)
    bindings=[]
    for item in proposal["sourceBindings"]:
        actual=sha(REPO/item["path"]); bindings.append({**item,"actualSha256":actual,"matches":actual==item["sha256"]})
    specs=[]
    # Complete regular markers through the ordered terminal event; B's terminal turn is intentionally open.
    for aid, stop in {"A":126.0,"B":133.0,"C":128.0,"D":129.0}.items():
        schedule=initial["actors"][aid]["regularSchedule"]; start=float(schedule["nextStart"])
        while start<=stop+1e-9:
            add_spec(specs,start,10,"REGULAR_TURN_START",{"actorId":aid,"turnStart":start})
            end=start+float(schedule["endOffset"])
            if end<=inputs["localGeometry"]["dispel"]["counterspellWindow"]+1e-9: add_spec(specs,end,90,"REGULAR_TURN_END",{"actorId":aid,"turnStart":start,"turnEnd":end})
            start+=float(schedule["period"])
    add_spec(specs,inputs["localGeometry"]["focusSetDown"]["time"],20,"FOCUS_CONTROLLED_SETDOWN",inputs["localGeometry"]["focusSetDown"])
    bolt=inputs["bolts"]
    for n,start in enumerate(bolt["starts"],1):
        add_spec(specs,start+bolt["eventOffsets"]["commit"],10,"ARCANE_BOLT_COMMIT",{"ordinal":n,"startSeconds":start})
        add_spec(specs,start+bolt["eventOffsets"]["counterspellWindow"],10,"COUNTERSPELL_WINDOW",{"sourceSpell":"wizard.base.arcane-bolt","ordinal":n,"startSeconds":start})
        add_spec(specs,start+bolt["eventOffsets"]["resolve"],10,"ARCANE_BOLT_ATTACK_ROLL",{"ordinal":n,"startSeconds":start})
        add_spec(specs,start+bolt["eventOffsets"]["resolve"],20,"ARCANE_SHIELD_RESPONSE",{"ordinal":n,"startSeconds":start})
        add_spec(specs,start+bolt["eventOffsets"]["resolve"],30,"ARCANE_BOLT_DAMAGE_RESOLUTION",{"ordinal":n,"startSeconds":start})
        if n < 9:
            add_spec(specs,start+bolt["eventOffsets"]["resolve"],40,"ARCANE_BOLT_CAST_RESOLUTION",{"ordinal":n,"startSeconds":start,"resolutionBoundary":"damage-resolved"})
    save=inputs["woundSave"]
    add_spec(specs,save["event"],40,"WOUND_SAVE",save)
    add_spec(specs,save["event"],50,"ZERO_HP_CALLBACKS_AND_TILE_RELEASE",{"rule":save["orderedDamageSettlement"][2]["rule"],"tileDrop":inputs["localGeometry"]["tileDrop"]})
    add_spec(specs,save["event"],60,"ARCANE_BOLT_CAST_RESOLUTION",{"ordinal":9,"startSeconds":bolt["starts"][8],"resolutionBoundary":"wound-and-zero-hp-callbacks-complete"})
    for n,start in enumerate(inputs["cadence"]["groundingStarts"],1): add_spec(specs,start,20,"GROUNDING_ACTION",{"ordinal":n,"rule":inputs["cadence"]["grounding"]})
    for start in bolt["starts"]:
        if start+6.9<=inputs["localGeometry"]["dispel"]["counterspellWindow"]+1e-9:
            add_spec(specs,start+6.9,70,"SPELL_EFFICIENCY_WINDOW_EXPIRY",{"originatingSpell":"wizard.base.arcane-bolt","castAt":start+0.1,"expiresAt":start+6.9})
    for start in [inputs["cadence"]["idleStart"],121.0]: add_spec(specs,start+0.9,70,"IDLE_TURN_END_CHECK",{"actorId":"B","turnStart":start,"reason":"No spell or magical class ability; no death intervention is chosen."})
    for n,start in enumerate(inputs["deathSaves"]["starts"],1):
        add_spec(specs,start,20,"DEATH_SAVE",{"ordinal":n,**inputs["deathSaves"]})
        if n==3: add_spec(specs,start,30,"A_BECOMES_DEAD",{"result":inputs["deathSaves"]["result"],"persistence":inputs["persistence"]})
    sight=inputs["localGeometry"]["sight"]; dispel=inputs["localGeometry"]["dispel"]
    add_spec(specs,sight["time"],20,"ARCANE_SIGHT_COMMIT",sight)
    add_spec(specs,sight["counterspellWindow"],10,"COUNTERSPELL_WINDOW",{"sourceSpell":"wizard.arch.arcane-sight","responders":sight["responders"]})
    add_spec(specs,sight["counterspellWindow"],20,"ARCANE_SIGHT_RESOLUTION",sight)
    add_spec(specs,dispel["time"],20,"DISPEL_MAGIC_COMMIT",dispel)
    add_spec(specs,dispel["counterspellWindow"],10,"COUNTERSPELL_WINDOW",{"sourceSpell":"wizard.arch.dispel-magic","responders":dispel["responders"]})
    add_spec(specs,dispel["counterspellWindow"],20,"DISPEL_MAGIC_SUCCESSFUL_RESOLUTION",dispel)
    add_spec(specs,dispel["counterspellWindow"],30,"FORTRESS_ROOT_TERMINATION",inputs["localGeometry"]["q27Projection"])
    add_spec(specs,dispel["counterspellWindow"],40,"Q27_BODY_CLOSURE_A",inputs["localGeometry"]["q27Projection"]["A"])
    add_spec(specs,dispel["counterspellWindow"],50,"Q27_BODY_CLOSURE_B",inputs["localGeometry"]["q27Projection"]["B"])
    for n,item in enumerate(inputs["localGeometry"]["q27Projection"]["loose"],1): add_spec(specs,dispel["counterspellWindow"],60+n,"Q27_LOOSE_ITEM_SETTLEMENT",{"ordinal":n,**item})
    specs.sort(key=lambda e:(e["timeSeconds"],e["orderAtTime"],e["kind"]))
    state=copy.deepcopy(initial); initial_clock=copy.deepcopy(initial["clock"]); initial_time=float(initial["time"]); turns={}; events=[]
    spell_info={
      "ARCANE_BOLT_COMMIT":{"spellId":"wizard.base.arcane-bolt","school":"Universal","rank":1,"cost":1,"recharge":None,"target":"A"},
      "ARCANE_SIGHT_COMMIT":{"spellId":"wizard.arch.arcane-sight","school":"Divination","rank":2,"cost":2,"recharge":2,"target":"self"},
      "DISPEL_MAGIC_COMMIT":{"spellId":"wizard.arch.dispel-magic","school":"Abjuration","rank":3,"cost":3,"recharge":2,"target":ROOT_EFFECT_ID},
    }
    def commit_spell(kind,event):
        actor=state["actors"]["B"]; info=spell_info[kind]; sid=info["spellId"]; t=event["timeSeconds"]; ctx=turns["B"]
        cast_id=f"PG328-W05-W10-R2:{sid}:{event['details'].get('ordinal','single')}"
        if actor["action"]!=1: raise ValueError(f"B has no Action for {sid} at {t}")
        actor["action"]=0; ctx["actionSpent"]=1; ctx["actionKind"]="CAST"; actor["magicThisTurn"]=True
        rp_before=actor["RP"]; dis_before=actor["Dissonance"]
        pending=[w for w in actor.get("testOnlySpellEfficiencyHistory",[]) if w["family"]==sid and w["status"]=="PENDING" and t<=w["expiresAt"]]
        discount=bool(pending); base_cost=max(1,info["cost"]-(1 if discount else 0))
        first=sid not in actor["preparedFamiliesUsed"]
        base_strain=0 if first else (1 if info["rank"]<=5 else 2 if info["rank"]<=9 else 0)
        refrain=min(3,actor["Refrain"]+1) if actor["lastSpell"]==sid else 0
        limit=max(4,2+actor["PB"]+max(0,actor["M"]))
        surcharge=1 if dis_before>=limit else 2 if dis_before>=limit+3 else 3 if dis_before>=limit+6 else 0
        cost=base_cost+surcharge
        if rp_before<cost: raise ValueError(f"B lacks RP for {sid} at {t}")
        actor["RP"]=rp_before-cost; actor["Dissonance"]=dis_before+base_strain+refrain; actor["Refrain"]=refrain; actor["lastSpell"]=sid
        if first: actor["preparedFamiliesUsed"].append(sid)
        next_end=ctx["turnStart"]+actor["regularSchedule"]["period"]+actor["regularSchedule"]["endOffset"]
        hist={"castId":cast_id,"spellId":sid,"class":"Wizard","school":info["school"],"rank":info["rank"],"time":t,"cost":cost,"firstPreparedFamily":first,"baseDissonance":base_strain,"Refrain":refrain,"originPlane":actor["plane"],"target":info["target"]}
        if sid=="wizard.arch.arcane-sight": hist["concentration"]={"activeFromCommit":True,"startedAt":t,"maximumDurationSeconds":600,"deadline":t+600,"auraPerceptionAfterResolution":True}
        actor["spellHistory"].append(hist)
        actor["resourceHistory"].append({"event":cast_id,"RP":-cost,"poolAfter":actor["RP"],"discount":discount and base_cost==info["cost"]-1,"spellId":sid,"DissonanceBefore":dis_before,"DissonanceAfter":actor["Dissonance"],"Refrain":refrain,"surchargeRP":surcharge})
        actor.setdefault("testOnlySpellEfficiencyHistory",[]).append({"family":sid,"castId":cast_id,"createdAt":t,"expiresAt":float(next_end),"discountRP":1,"minimumCostRP":1,"status":"PENDING","consumedAt":None})
        if info["recharge"]: actor["recharge"][sid]=info["recharge"]
        state["pendingCast"]={"castId":cast_id,"spellId":sid,"caster":"B","target":info["target"],"commitTime":t,"costCommitted":cost,"status":"PENDING_RESOLUTION","classification":"TEST_ONLY_HYPOTHETICAL_BRANCH"}
        if sid=="wizard.arch.arcane-sight":
            state["actors"]["B"]["concentration"]={"spellId":sid,"active":True,"startedAt":t,"maximumDurationSeconds":600,"deadline":t+600,"classification":"TEST_ONLY_HYPOTHETICAL_BRANCH"}
        event["details"].update({"castId":cast_id,"spellId":sid,"costRP":cost,"baseCostRP":info["cost"],"rpBefore":rp_before,"rpAfter":actor["RP"],"dissonanceBefore":dis_before,"firstPreparedFamily":first,"baseDissonance":base_strain,"refrainAdded":refrain,"dissonanceAfter":actor["Dissonance"],"dissonanceLimit":limit,"strainSurchargeRP":surcharge,"spellEfficiencyDiscountApplied":base_cost<info["cost"],"spellEfficiencyWindowExpiresAt":next_end,"actionSpent":1,"magicThisTurn":True,"rechargeAfterCommit":actor["recharge"].get(sid),"pendingCastAfterCommit":copy.deepcopy(state["pendingCast"])})
        if sid=="wizard.arch.arcane-sight": event["details"]["concentrationAfterCommit"] = copy.deepcopy(state["actors"]["B"]["concentration"])

    def mutate(event):
        kind=event["kind"]; d=event["details"]; t=event["timeSeconds"]
        state["time"]=t; delta=t-initial_time; state["clock"]["elapsedSeconds"]=initial_clock["elapsedSeconds"]+delta
        for key in ("OpeningRemaining","HornRemaining"):
            if key in initial_clock and initial_clock[key] is not None: state["clock"][key]=initial_clock[key]-delta
        if kind=="REGULAR_TURN_START":
            aid=d["actorId"]
            if aid in turns: raise ValueError(f"Overlapping turn: {aid}")
            a=state["actors"][aid]; s=a["regularSchedule"]; rb=copy.deepcopy(a["recharge"])
            for key,value in list(a["recharge"].items()): a["recharge"][key]=max(0,int(value)-1)
            s["starts"].append(t); s["nextStart"]=t+s["period"]; s["nextEnd"]=t+s["endOffset"]
            a["action"]=1; a["bonusAction"]=1; a["reaction"]=1; a["movement"]=30; a["magicThisTurn"]=False
            turns[aid]={"turnStart":t,"actionSpent":0,"bonusActionSpent":0,"reactionSpent":0,"movementSpent":0,"actionKind":None}
            d.update({"budgetsAfterStart":{"Action":1,"BonusAction":1,"Reaction":1,"MovementFeet":30},"rechargeBeforeTick":rb,"rechargeAfterTick":copy.deepcopy(a["recharge"]),"magicThisTurn":False,"deathStatusAtStart":a["death"]["status"],"HPAtStart":a["HP"]})
        elif kind=="REGULAR_TURN_END":
            aid=d["actorId"]; a=state["actors"][aid]; ctx=turns.pop(aid); dis_before=a["Dissonance"]
            decay=ctx["actionKind"] not in ("CAST","GROUNDING") and not ctx.get("idleDecayHandled",False)
            if decay: a["Dissonance"]=max(0,dis_before-1)
            s=a["regularSchedule"]; s["ends"].append(t)
            end={"regularTurnEndedAt":t,"recordedAt":t,"Action":{"spent":ctx["actionSpent"],"unusedExpired":1-ctx["actionSpent"]},"BonusAction":{"spent":ctx["bonusActionSpent"],"unusedExpired":1-ctx["bonusActionSpent"]},"Reaction":{"spent":ctx["reactionSpent"],"availableOffTurnUntilSpentOrNextOwnStart":a["reaction"]==1},"MovementFeet":{"granted":30,"spent":ctx["movementSpent"],"unusedExpired":30-ctx["movementSpent"]}}
            s["budgetHistory"].append({"time":ctx["turnStart"],"action":1,"BA":1,"Reaction":1,"Move":30,"recharge":copy.deepcopy(a["recharge"]),"endDisposition":end})
            for w in a.get("testOnlySpellEfficiencyHistory",[]):
                if w["status"]=="PENDING" and w["expiresAt"]<=t+1e-9: w["status"]="EXPIRED_UNUSED"
            a["action"]=0; a["bonusAction"]=0; a["movement"]=0; a["magicThisTurn"]=False; s["nextEnd"]=None
            d.update({"actionSpent":ctx["actionSpent"],"actionKind":ctx["actionKind"],"bonusActionSpent":ctx["bonusActionSpent"],"reactionSpent":ctx["reactionSpent"],"movementSpentFeet":ctx["movementSpent"],"dissonanceBeforeEnd":dis_before,"dissonanceAfterEnd":a["Dissonance"],"idleDecayApplied":decay or ctx.get("idleDecayHandled",False),"unusedBudgetDisposition":copy.deepcopy(end)})
        elif kind=="FOCUS_CONTROLLED_SETDOWN":
            a=state["actors"]["A"]; item=state["items"]["focus-A"]; item["custodian"]=None; item["position"]=copy.deepcopy(d["finalPosition"])
            item["testOnlyGeometry"]["currentBoundsFeet"]=[[24.5,25.0],[10.0,10.5],[0.0,0.5]]
            a["equipment"]=[x for x in a["equipment"] if x!="focus-A"]; a["carriedWeightLb"]=13; a["carriedLoad"]=1.3; a["focusAccessible"]=False; a["w01HandState"]["left"]="free"
            turns["A"]["actionKind"]="FREE_INTERACTION"
            d.update({"ownerAfter":item["owner"],"custodianAfter":item["custodian"],"positionAfter":item["position"],"heldHandAfter":copy.deepcopy(a["w01HandState"]),"carriedWeightAfterLb":13,"carriedLoadAfter":1.3,"focusAccessibleAfter":False,"ActionSpent":0,"freeObjectInteractionUsed":True})
        elif kind=="GROUNDING_ACTION":
            a=state["actors"]["B"]; ctx=turns["B"]
            if a["action"]!=1: raise ValueError("Grounding requires an available Action")
            before=a["Dissonance"]; refrain=a["Refrain"]; a["action"]=0; ctx["actionSpent"]=1; ctx["actionKind"]="GROUNDING"; a["Dissonance"]=max(0,before-a["PB"])
            d.update({"actorId":"B","dissonanceBefore":before,"groundingReduction":a["PB"],"dissonanceAfter":a["Dissonance"],"RefrainBefore":refrain,"RefrainAfter":a["Refrain"],"RPBefore":a["RP"],"RPAfter":a["RP"],"ActionSpent":1,"movementSpentFeet":0,"positionAfter":copy.deepcopy(a["position"])})
        elif kind=="SPELL_EFFICIENCY_WINDOW_EXPIRY":
            a=state["actors"]["B"]; matches=[w for w in a.get("testOnlySpellEfficiencyHistory",[]) if w["family"]==d["originatingSpell"] and w["createdAt"]==d["castAt"] and w["status"]=="PENDING"]
            for w in matches: w["status"]="EXPIRED_UNUSED"
            d.update({"expiredWindowCount":len(matches),"noRPDiscountConsumed":True})
        elif kind=="IDLE_TURN_END_CHECK":
            a=state["actors"][d["actorId"]]; ctx=turns[d["actorId"]]; before=a["Dissonance"]; a["Dissonance"]=max(0,before-1); ctx["actionKind"]="IDLE_DECAY"; ctx["idleDecayHandled"]=True
            d.update({"DissonanceBefore":before,"DissonanceAfter":a["Dissonance"],"RefrainBefore":a["Refrain"],"RefrainAfter":a["Refrain"],"RPBefore":a["RP"],"RPAfter":a["RP"],"noHealStabilizeOrEntryChosen":True})
        elif kind in spell_info: commit_spell(kind,event)
        elif kind=="COUNTERSPELL_WINDOW":
            sid=d["sourceSpell"]
            if sid=="wizard.base.arcane-bolt":
                n=d["ordinal"]; a=state["actors"]["A"]; b=state["actors"]["B"]; r=dist(actor_center(a),actor_center(b)); alive=a["death"]["status"]=="alive"; same=a["plane"]==b["plane"]; hand=a["w01HandState"]["left"]=="free" or a["w01HandState"]["right"]=="free"
                eligible=alive and same and r<=60 and a["reaction"]==1 and a["RP"]>=3 and hand and n!=1
                checks=[{"actorId":"A","wizard20":True,"automaticCounterspellAccess":True,"aliveAtWindow":alive,"samePlane":same,"centerDistanceFt":round(r,6),"within60Ft":r<=60,"reactionAvailable":a["reaction"]==1,"RPAvailable":a["RP"],"freeHand":hand,"eligible":eligible,"disposition":"INELIGIBLE_BOTH_HANDS_OCCUPIED" if n==1 else ("DECLINES_NO_COST_OR_REACTION_SPENT" if eligible else "INELIGIBLE")},{"actorId":"B","attempted":False,"eligibility":"NOT_ADJUDICATED","reason":"B makes no attempt; bound sources do not adjudicate self-counter eligibility.","reactionSpent":False,"RPSpent":0},{"actorId":"C","eligible":False,"reason":"remains on fixture:origin across the plane boundary"},{"actorId":"D","eligible":False,"reason":"remains on fixture:origin across the plane boundary"}]
            else:
                checks=[{"actorId":"A","eligible":False,"reason":"Dead at this counter window"},{"actorId":"B","attempted":False,"eligibility":"NOT_ADJUDICATED","reason":"B makes no attempt; bound sources do not adjudicate self-counter eligibility.","reactionSpent":False,"RPSpent":0},{"actorId":"C","eligible":False,"reason":"remains on fixture:origin across the plane boundary"},{"actorId":"D","eligible":False,"reason":"remains on fixture:origin across the plane boundary"}]
            d["responders"]="B makes no attempt and self-counter eligibility is not adjudicated; A's status and the C/D plane boundary are recorded individually in actualResponderChecks. No responder spends a reaction or RP."
            d.update({"actualResponderChecks":checks,"pendingCast":copy.deepcopy(state["pendingCast"]),"noReactionOrRPSpent":True})
        elif kind=="ARCANE_BOLT_ATTACK_ROLL": d.update({"attacker":"B","target":"A","attack":bolt["attack"],"A_AC":state["actors"]["A"]["AC"],"hit":True,"postRollProtectionTrigger":"Attack roll would hit A; offer Arcane Shield before damage resolution."})
        elif kind=="ARCANE_SHIELD_RESPONSE":
            a=state["actors"]["A"]; n=d["ordinal"]; r=dist(actor_center(a),actor_center(state["actors"]["B"])); alive=a["death"]["status"]=="alive"; same=a["plane"]==state["actors"]["B"]["plane"]; hand=a["w01HandState"]["left"]=="free" or a["w01HandState"]["right"]=="free"; eligible=alive and same and r<=60 and a["reaction"]==1 and a["RP"]>=2 and hand and n!=1
            d.update({"actualResponderChecks":[{"actorId":"A","arcaneShieldAccessInAdoptedScenario":True,"attackWouldHit":True,"aliveAtTrigger":alive,"samePlane":same,"centerDistanceFt":round(r,6),"within60Ft":r<=60,"reactionAvailable":a["reaction"]==1,"RPAvailable":a["RP"],"freeHand":hand,"eligible":eligible,"disposition":"INELIGIBLE_BOTH_HANDS_OCCUPIED" if n==1 else ("DECLINES_NO_COST_OR_REACTION_SPENT" if eligible else "INELIGIBLE")}]})
        elif kind=="ARCANE_BOLT_DAMAGE_RESOLUTION":
            a=state["actors"]["A"]; n=d["ordinal"]; before=a["HP"]; expected=bolt["hpSequence"]
            if before!=expected[n-1]: raise ValueError(f"A HP mismatch at bolt {n}: {before}")
            a["HP"]=expected[n]; d.update({"damageRoll":bolt["damage"],"forceResistanceApplied":True,"forceDamageAfterResistance":14,"hpBefore":before,"hpAfter":a["HP"],"overflow":bolt["overflow"] if n==9 else 0,"instantDeath":False,"WoundsAfter":a["wounds"],"targetRemainsSameBody":True})
        elif kind=="ARCANE_BOLT_CAST_RESOLUTION":
            n=d["ordinal"]; pending=state["pendingCast"]
            expected_cast_id=f"PG328-W05-W10-R2:wizard.base.arcane-bolt:{n}"
            if not pending or pending["castId"]!=expected_cast_id or pending["status"]!="PENDING_RESOLUTION": raise ValueError(f"Bolt {n} is not the pending cast at resolution")
            if n==9 and (not state["actors"]["A"].get("testOnlyWoundSaveHistory") or "Unconscious" not in state["actors"]["A"]["conditions"] or state["items"][TILE_ID]["custodian"] is not None): raise ValueError("Ninth Bolt cast cannot close before Wound/zero-HP callbacks and tile release")
            state["pendingCast"]=None
            hist=next(x for x in reversed(state["actors"]["B"]["spellHistory"]) if x["castId"]==expected_cast_id)
            hist["resolutionStatus"]="SUCCESSFUL"
            hist["resolvedAt"]=t
            d.update({"castId":expected_cast_id,"spellId":"wizard.base.arcane-bolt","resolutionStatus":"SUCCESSFUL","pendingCastAfterResolution":None,"paidCastHistoryPreserved":True,"callbacksCompleteBeforeNinthResolution":n!=9 or (bool(state["actors"]["A"].get("testOnlyWoundSaveHistory")) and "Unconscious" in state["actors"]["A"]["conditions"] and state["items"][TILE_ID]["custodian"] is None)})
        elif kind=="WOUND_SAVE":
            a=state["actors"]["A"]; a.setdefault("testOnlyWoundSaveHistory",[]).append(copy.deepcopy(d)); d.update({"A_WoundsBefore":a["wounds"],"A_WoundsAfter":a["wounds"],"saveTotal":save["total"],"success":True})
        elif kind=="ZERO_HP_CALLBACKS_AND_TILE_RELEASE":
            a=state["actors"]["A"]; tile=state["items"][TILE_ID]
            if "Unconscious" not in a["conditions"]: a["conditions"].append("Unconscious")
            if "Prone" not in a["conditions"]: a["conditions"].append("Prone")
            a["testOnlyPose"]=copy.deepcopy(inputs["localGeometry"]["bodyPoseAtZero"]); a["carriedWeightLb"]=11; a["carriedLoad"]=1.1; a["equipment"]=[x for x in a["equipment"] if x!=TILE_ID]; a["w01HandState"]["right"]="free"
            tile["custodian"]=None; tile["position"]=[25,5,0]; tile["heldBy"]=None; tile["heldBoundsFeet"]=None; tile.setdefault("testOnlyGeometry",{})["currentBoundsFeet"]=copy.deepcopy(d["tileDrop"]["heldBounds"])
            d.update({"HP":a["HP"],"conditionsAfter":copy.deepcopy(a["conditions"]),"woundCount":a["wounds"],"tileId":tile["id"],"tileCustodianAfter":tile["custodian"],"tilePositionAfter":tile["position"],"tileExpiryPreserved":tile["expiresAtEventTime"],"carriedWeightAfterLb":11,"carriedLoadAfter":1.1,"heldItemsAfter":copy.deepcopy(a["equipment"]),"sameAIdentity":a["id"]=="A"})
        elif kind=="DEATH_SAVE":
            a=state["actors"]["A"]
            if a["HP"]!=0 or a["death"]["status"]!="alive": raise ValueError("Death save is not legal")
            roll={"time":t,"d20":inputs["deathSaves"]["dieFaceEach"],"modifier":inputs["deathSaves"]["modifier"],"result":"failure","failuresAfter":a["death"]["failures"]+1}; a["death"]["failures"]+=1; a["death"]["saveInputs"].append(roll)
            d.update({"actorId":"A","HP":0,"deathStatusBefore":"alive","deathStatusAfter":"alive","dieFace":2,"modifier":0,"result":"failure","successesAfter":a["death"]["successes"],"failuresAfter":a["death"]["failures"],"saveInput":roll,"sameBodyPersists":True})
        elif kind=="A_BECOMES_DEAD":
            a=state["actors"]["A"]
            if a["death"]["failures"]!=3 or a["HP"]!=0: raise ValueError("Dead transition before three failed saves")
            a["death"]["status"]="dead"; d.update({"deathStatusBefore":"alive","deathStatusAfter":"dead","HP":0,"successes":0,"failures":3,"bodyPersists":True,"equipmentCustodyPersists":True})
        elif kind=="ARCANE_SIGHT_RESOLUTION":
            b=state["actors"]["B"]
            if b["concentration"]!={"spellId":"wizard.arch.arcane-sight","active":True,"startedAt":127.1,"maximumDurationSeconds":600,"deadline":727.1,"classification":"TEST_ONLY_HYPOTHETICAL_BRANCH"}: raise ValueError("Arcane Sight concentration must begin at commit before interruption")
            state["pendingCast"]=None
            obs={"time":t,"observer":"B","spellId":"wizard.arch.arcane-sight","subject":ROOT_EFFECT_ID,"auraPoint":copy.deepcopy(inputs["localGeometry"]["sight"]["toAuraPoint"]),"distanceFt":inputs["localGeometry"]["sight"]["distanceFt"],"samePlane":True,"totalCover":False,"lineClear":True,"knownCategory":"Conjuration","laterTurnAuraExaminationClaimed":False}
            state["observations"].append(obs); d.update({"resolutionStatus":"SUCCESSFUL","pendingCastAfterResolution":None,"concentrationAfter":copy.deepcopy(b["concentration"]),"auraPerceptionBeginsAt":t,"observation":obs,"rpAfter":b["RP"],"rootRemainsActive":state["effects"][ROOT_EFFECT_ID]["active"],"noExtraElapsedTimeAdded":True})
        elif kind=="DISPEL_MAGIC_SUCCESSFUL_RESOLUTION":
            b=state["actors"]["B"]; state["pendingCast"]=None; d.update({"resolutionStatus":"SUCCESSFUL","checkRoll":"d20 12 + INT5 + PB6 = 23 vs DC19","checkTotal":23,"dc":19,"margin":4,"spellRankTarget":9,"targetEffect":ROOT_EFFECT_ID,"endingSucceeded":True,"pendingCastAfterResolution":None,"B_RPAfter":b["RP"],"B_concentrationPreserved":copy.deepcopy(b["concentration"]),"noExtraElapsedTimeAdded":True})
        elif kind=="FORTRESS_ROOT_TERMINATION":
            effect=state["effects"][ROOT_EFFECT_ID]; effect["active"]=False; effect["open"]=False; effect["terminalReceipt"]={"time":t,"status":"ENDED_BY_SUCCESSFUL_DISPEL","spellId":"wizard.arch.dispel-magic","castId":state["actors"]["B"]["spellHistory"][-1]["castId"],"scope":"TEST_ONLY branch PG328-W05-W10-R1"}
            space=state["spaces"][SPACE_ID]; space["exists"]=False
            for door in space.get("doors",[]): door["open"]=False
            d.update({"rootEffectId":ROOT_EFFECT_ID,"activeAfter":False,"terminalReceipt":copy.deepcopy(effect["terminalReceipt"]),"spaceExistsAfter":False,"closureSequence":["A body","B body","loose items in adopted stable-ID order"],"campaignEventAsserted":False})
        elif kind=="Q27_BODY_CLOSURE_A":
            a=state["actors"]["A"]; a["plane"]="fixture:origin"; a["position"]=copy.deepcopy(d["fixedClosureReference"]); a["testOnlyPose"]["bounds"]=copy.deepcopy(d["bodyBounds"]); a["testOnlyPose"]["support"]=d["support"]; a["testOnlyPose"]["closureSupportPatch"]="ORIGIN-A-CORPSE-GROUND-443"
            for item_id,key in (("pack-A","packA"),("cargo-A","cargoA")):
                it=state["items"][item_id]; it["plane"]="fixture:origin"; it.setdefault("testOnlyGeometry",{})["currentBoundsFeet"]=copy.deepcopy(d[key])
            d.update({"actorId":"A","deathStatus":a["death"]["status"],"HP":a["HP"],"planeAfter":a["plane"],"positionAfter":a["position"],"bodyBoundsAfter":a["testOnlyPose"]["bounds"],"packCustodian":state["items"]["pack-A"]["custodian"],"cargoCustodian":state["items"]["cargo-A"]["custodian"],"sameBodyAndGear":True})
        elif kind=="Q27_BODY_CLOSURE_B":
            b=state["actors"]["B"]; b["plane"]="fixture:origin"; b["position"]=copy.deepcopy(d["fixedClosureReference"]); b["testOnlyClosurePose"]={"bounds":copy.deepcopy(d["bodyBounds"]),"support":d["support"],"supportPatchId":"ORIGIN-B-BODY-GROUND-443"}
            for item_id,item_data in d["carriedItems"].items(): state["items"][item_id]["plane"]="fixture:origin"; state["items"][item_id].setdefault("testOnlyGeometry",{})["currentBoundsFeet"]=copy.deepcopy(item_data["worldBoundsAtClosure"])
            d.update({"actorId":"B","planeAfter":b["plane"],"positionAfter":b["position"],"bodyBoundsAfter":b["testOnlyClosurePose"]["bounds"],"supportPatchId":"ORIGIN-B-BODY-GROUND-443","carriedCustodyPreserved":{i:state["items"][i]["custodian"] for i in d["carriedItems"]}})
        elif kind=="Q27_LOOSE_ITEM_SETTLEMENT":
            it=state["items"][d["id"]]; it["plane"]="fixture:origin"; it["position"]=copy.deepcopy(d["outside"]); it["custodian"]=None; it.setdefault("testOnlyGeometry",{})["currentBoundsFeet"]=copy.deepcopy(d["bounds"])
            d.update({"itemId":it["id"],"ownerAfter":it["owner"],"custodianAfter":None,"planeAfter":it["plane"],"positionAfter":it["position"],"expiryAfter":it.get("expiresAtEventTime"),"settlementOrder":d["ordinal"]})
        else: raise ValueError(f"Unhandled event kind {kind}")
        event["eventId"]=f"PG328-W05-W10-R2-E{len(events)+1:03d}"; state["processedEventIds"].append(event["eventId"])

    for spec in specs:
        before=copy.deepcopy(state); event=copy.deepcopy(spec); mutate(event); forward=diff_ops(before,state)
        event["stateTransition"]={"beforeStateSha256":sha_obj(before),"afterStateSha256":sha_obj(state),"forwardOperations":forward,"inverseOperations":inverses(forward)}
        events.append(event)
    if state["time"]!=inputs["localGeometry"]["dispel"]["counterspellWindow"]: raise ValueError("Terminal branch time mismatch")
    if set(turns)!={"B"}: raise ValueError(f"Unexpected open turns: {list(turns)}")
    events_by_kind={}
    for e in events: events_by_kind.setdefault(e["kind"],[]).append(e)
    # Independently exercise every forward and inverse transition before writing the packet.
    forward_state=copy.deepcopy(initial); forward_ok=True
    for e in events:
        tr=e["stateTransition"]
        if sha_obj(forward_state)!=tr["beforeStateSha256"]: forward_ok=False; break
        forward_state=apply_ops(forward_state,tr["forwardOperations"])
        if sha_obj(forward_state)!=tr["afterStateSha256"]: forward_ok=False; break
    forward_ok=forward_ok and forward_state==state and sha_obj(forward_state)==sha_obj(state)
    reverse_state=copy.deepcopy(state); reverse_ok=True
    for e in reversed(events):
        tr=e["stateTransition"]
        if sha_obj(reverse_state)!=tr["afterStateSha256"]: reverse_ok=False; break
        reverse_state=apply_ops(reverse_state,tr["inverseOperations"])
        if sha_obj(reverse_state)!=tr["beforeStateSha256"]: reverse_ok=False; break
    reverse_ok=reverse_ok and reverse_state==initial and sha_obj(reverse_state)==initial_sha
    ground=[e for e in events if e["kind"]=="GROUNDING_ACTION"]
    for e in ground:
        expected=80-sum(1 for start in bolt["starts"] if start+0.1<e["timeSeconds"])
        if e["details"]["RPAfter"]!=expected: raise ValueError(f"Incorrect Grounding RP at {e['timeSeconds']}")
    if state["actors"]["B"]["RP"]!=66: raise ValueError("B terminal RP must be66")
    if state["actors"]["A"]["death"]["status"]!="dead" or state["actors"]["A"]["HP"]!=0: raise ValueError("A terminal state mismatch")
    transition={"classification":"TEST_ONLY_REVERSIBLE_BRANCH_STATE_RECONSTRUCTION","initialStatePath":rel(PARENT_PATH)+"#/stateSnapshots/S030","initialState":initial,"initialStateSha256":initial_sha,"terminalState":state,"terminalStateSha256":sha_obj(state),"eventsAreAppliedInOrder":True,"forwardOperationsTotal":sum(len(e["stateTransition"]["forwardOperations"]) for e in events),"inverseOperationsTotal":sum(len(e["stateTransition"]["inverseOperations"]) for e in events),"reverseRestorationExpectedSha256":initial_sha,"forwardReplayPass":forward_ok,"inverseReplayPass":reverse_ok,"scope":"One adopted hypothetical PG328-W05-W10-R1 branch; no campaign execution or authority mutation."}
    prev=REVIEW/"fortress_w05_w10_joint_witness_452"/"W05_W10_WITNESS_452_TESTONLY.json"
    witness={"schemaVersion":2,"id":"PG328-W05-W10-WITNESS-453","supersedesWitness":{"path":rel(prev),"sha256":sha(prev)},"classification":"TEST_ONLY_HYPOTHETICAL_BRANCH_WITNESS","status":"TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW","branchId":proposal["scope"]["branch"],"components":proposal["scope"]["components"],"spell":proposal["scope"]["spell"],"identityHold":proposal["scope"]["hold"],"hypotheticalOnly":True,"campaignOccurrenceAsserted":False,
      "adoption":{"path":rel(ADOPTION_PATH),"sha256":sha(ADOPTION_PATH),"proposalPath":rel(PROPOSAL_PATH),"proposalSha256":sha(PROPOSAL_PATH),"exactProposalAdopted":adoption["scope"]["proposalSha256"]==sha(PROPOSAL_PATH),"ownerAuthorization":adoption["ownerAuthorization"]["verbatim"],"directorStatus":adoption["directorReview"]["status"]},
      "parent":{"path":rel(PARENT_PATH),"pointer":"#/stateSnapshots/S030","replaySha256":sha(PARENT_PATH),"snapshotSha256":initial_sha,"timeSeconds":proposal["scope"]["parentTime"],"parentMutated":False},"sourceBindings":bindings,"adoptedScenario":inputs,
      "eventTrace":{"semantics":"Ordered reversible hypothetical state reconstruction from exact S030 and proposal443; addresses Director corrections W452-C01 through C03; no runtime execution or campaign assertion.","eventCount":len(events),"regularTurnStartCount":sum(e["kind"]=="REGULAR_TURN_START" for e in events),"regularTurnEndCount":sum(e["kind"]=="REGULAR_TURN_END" for e in events),"events":events,"terminalResolution":{"dispelSuccessfulAt":inputs["localGeometry"]["dispel"]["counterspellWindow"],"rootTerminationFollowsDispel":True,"bodyClosureOrder":inputs["localGeometry"]["q27Projection"]["bodyPlacementOrder"],"looseItemOrder":inputs["localGeometry"]["q27Projection"]["looseItemOrderByStableId"],"sameWorldTimeOrderedSubsteps":True,"campaignOccurrenceAsserted":False},"terminalProjection":inputs["localGeometry"]["q27Projection"]},
      "stateTransitionReplay":transition,"groundingResourceReadings":[{"eventId":e["eventId"],"timeSeconds":e["timeSeconds"],"rpAfterBolts":e["details"]["RPAfter"],"expected":80-sum(1 for st in bolt["starts"] if st+0.1<e["timeSeconds"])} for e in ground],
      "queueAtAdoption":{"reviewedApplied":adoption["queueAuthorityAtAdoption"]["reviewedApplied"],"pending":adoption["queueAuthorityAtAdoption"]["pending"],"acceptedUnapplied":adoption["queueAuthorityAtAdoption"]["acceptedUnapplied"],"mutation":False,"identityAcceptedOrApplied":False},
      "scopeBoundary":{"testOnly":True,"sealPresent":False,"FortressAcceptedOrApplied":False,"spellIdentityAcceptedOrApplied":False,"PG200_B06Closed":False,"canonicalRuleChanged":False,"historicalParentMutated":False,"campaignEventsAsserted":False,"queueChanged":False,"generalizationBeyondW05W10":False}}
    dump(WITNESS_PATH,witness)
    checks={
      "exact proposal and owner adoption hashes":sha(PROPOSAL_PATH)==EXPECTED_PROPOSAL_SHA and adoption["scope"]["proposalSha256"]==sha(PROPOSAL_PATH),
      "exact parent and S030 hashes":sha(PARENT_PATH)==EXPECTED_PARENT_SHA==proposal["scope"]["parentSha256"] and initial_sha==witness["parent"]["snapshotSha256"],
      "all 12 adopted source bindings match":len(bindings)==12 and all(x["matches"] for x in bindings),
      "adopted scenario copied exactly":witness["adoptedScenario"]==inputs,
      "nine bolts have commit/window/attack/shield/damage/resolution records":len(events_by_kind["ARCANE_BOLT_COMMIT"])==9 and sum(e["details"].get("sourceSpell")=="wizard.base.arcane-bolt" for e in events_by_kind["COUNTERSPELL_WINDOW"])==9 and all(len(events_by_kind[k])==9 for k in ["ARCANE_BOLT_ATTACK_ROLL","ARCANE_SHIELD_RESPONSE","ARCANE_BOLT_DAMAGE_RESOLUTION","ARCANE_BOLT_CAST_RESOLUTION"]),
      "eight Grounding RP balances are correct":[e["details"]["RPAfter"] for e in ground]==[78,77,76,75,74,73,72,71],
      "actual responders are recorded without unsupported self-counter prohibition":events_by_kind["COUNTERSPELL_WINDOW"][0]["details"]["actualResponderChecks"][0]["eligible"] is False and all(e["details"]["actualResponderChecks"][0]["eligible"] for e in events_by_kind["COUNTERSPELL_WINDOW"][1:9]) and events_by_kind["ARCANE_SHIELD_RESPONSE"][0]["details"]["actualResponderChecks"][0]["eligible"] is False and all(e["details"]["actualResponderChecks"][0]["eligible"] for e in events_by_kind["ARCANE_SHIELD_RESPONSE"][1:]) and all(e["details"]["actualResponderChecks"][1]["attempted"] is False and e["details"]["actualResponderChecks"][1]["eligibility"]=="NOT_ADJUDICATED" for e in events_by_kind["COUNTERSPELL_WINDOW"]) and "cannot counter its own" not in json.dumps(events),
      "ninth Bolt resolves only after Wound/zero-HP callbacks; all pending casts close":[e["kind"] for e in events if e["timeSeconds"]==save["event"] and e["kind"] in ["ARCANE_BOLT_DAMAGE_RESOLUTION","WOUND_SAVE","ZERO_HP_CALLBACKS_AND_TILE_RELEASE","ARCANE_BOLT_CAST_RESOLUTION"]]==["ARCANE_BOLT_DAMAGE_RESOLUTION","WOUND_SAVE","ZERO_HP_CALLBACKS_AND_TILE_RELEASE","ARCANE_BOLT_CAST_RESOLUTION"] and all(e["stateTransition"]["afterStateSha256"]!=e["stateTransition"]["beforeStateSha256"] for e in events_by_kind["ARCANE_BOLT_CAST_RESOLUTION"]) and all(e["details"]["pendingCastAfterResolution"] is None and e["details"]["resolutionStatus"]=="SUCCESSFUL" and any(op["path"]=="/pendingCast" and op["op"]=="replace" and op["value"] is None for op in e["stateTransition"]["forwardOperations"]) for e in events_by_kind["ARCANE_BOLT_CAST_RESOLUTION"]) and events_by_kind["ARCANE_BOLT_CAST_RESOLUTION"][-1]["details"]["callbacksCompleteBeforeNinthResolution"] is True and state["pendingCast"] is None and state["items"][TILE_ID]["expiresAtEventTime"]==3606.13,
      "three failed death saves and Dead transition are recorded":[e["timeSeconds"] for e in events_by_kind["DEATH_SAVE"]]==inputs["deathSaves"]["starts"] and [e["timeSeconds"] for e in events_by_kind["A_BECOMES_DEAD"]]==[126.0],
      "regular markers complete through terminal closure":witness["eventTrace"]["regularTurnStartCount"]==80 and witness["eventTrace"]["regularTurnEndCount"]==79,
      "Sight concentration begins at commit before interruption; perception waits for successful resolution":next(e for e in events if e["kind"]=="ARCANE_SIGHT_COMMIT")["stateTransition"]["afterStateSha256"]==next(e for e in events if e["kind"]=="COUNTERSPELL_WINDOW" and e["details"].get("sourceSpell")=="wizard.arch.arcane-sight")["stateTransition"]["beforeStateSha256"] and next(e for e in events if e["kind"]=="ARCANE_SIGHT_COMMIT")["details"]["concentrationAfterCommit"]["startedAt"]==127.1 and next(e for e in events if e["kind"]=="ARCANE_SIGHT_COMMIT")["details"]["concentrationAfterCommit"]["deadline"]==727.1 and next(e for e in events if e["kind"]=="ARCANE_SIGHT_RESOLUTION")["details"]["auraPerceptionBeginsAt"]==127.2 and [e["kind"] for e in events if e["timeSeconds"]==sight["counterspellWindow"] and e["kind"] in ["COUNTERSPELL_WINDOW","ARCANE_SIGHT_RESOLUTION"]]==["COUNTERSPELL_WINDOW","ARCANE_SIGHT_RESOLUTION"] and [e["kind"] for e in events if e["timeSeconds"]==dispel["counterspellWindow"] and e["kind"] in ["COUNTERSPELL_WINDOW","DISPEL_MAGIC_SUCCESSFUL_RESOLUTION","FORTRESS_ROOT_TERMINATION","Q27_BODY_CLOSURE_A","Q27_BODY_CLOSURE_B","Q27_LOOSE_ITEM_SETTLEMENT"]]==["COUNTERSPELL_WINDOW","DISPEL_MAGIC_SUCCESSFUL_RESOLUTION","FORTRESS_ROOT_TERMINATION","Q27_BODY_CLOSURE_A","Q27_BODY_CLOSURE_B","Q27_LOOSE_ITEM_SETTLEMENT","Q27_LOOSE_ITEM_SETTLEMENT","Q27_LOOSE_ITEM_SETTLEMENT"],
      "forward state replay reproduces the terminal state":forward_ok,
      "inverse replay restores exact S030":reverse_ok,
      "Q27 root/body/item order matches adopted terms":not state["effects"][ROOT_EFFECT_ID]["active"] and not state["spaces"][SPACE_ID]["exists"] and [e["details"]["id"] for e in events_by_kind["Q27_LOOSE_ITEM_SETTLEMENT"]]==inputs["localGeometry"]["q27Projection"]["looseItemOrderByStableId"],
      "RP, concentration, recharge, Refrain and Spell Efficiency history complete":state["actors"]["B"]["RP"]==66 and state["actors"]["B"]["concentration"]["spellId"]=="wizard.arch.arcane-sight" and state["actors"]["B"]["recharge"]["wizard.arch.arcane-sight"]==1 and state["actors"]["B"]["recharge"]["wizard.arch.dispel-magic"]==2 and len(state["actors"]["B"]["testOnlySpellEfficiencyHistory"])==11,
      "queue and no-effect boundaries remain 830/18/0":witness["queueAtAdoption"]=={"reviewedApplied":830,"pending":18,"acceptedUnapplied":0,"mutation":False,"identityAcceptedOrApplied":False} and all(v is False for k,v in witness["scopeBoundary"].items() if k!="testOnly")}
    validation={"id":"PG328-W05-W10-BUILD-VALIDATION-453","classification":"TEST_ONLY_WITNESS_BUILD_VALIDATION","status":"PASS" if all(checks.values()) else "FAIL","witnessPath":rel(WITNESS_PATH),"witnessSha256":sha(WITNESS_PATH),"eventCount":len(events),"regularTurnStartCount":witness["eventTrace"]["regularTurnStartCount"],"regularTurnEndCount":witness["eventTrace"]["regularTurnEndCount"],"forwardOperations":transition["forwardOperationsTotal"],"inverseOperations":transition["inverseOperationsTotal"],"checks":checks,"passed":sum(checks.values()),"failed":sum(not v for v in checks.values()),"boundary":"W05/W10 hypothetical witness only; no seal, Fortress identity acceptance/application, canon, campaign fact, parent mutation, or queue mutation."}
    dump(VALIDATION_PATH,validation)
    if not all(checks.values()): raise SystemExit("Build validation failed; inspect BUILD_VALIDATION_453.json")
    README_PATH.write_text("# W05/W10 reversible hypothetical witness 453\n\nThis TEST_ONLY successor uses exact owner-adopted proposal443 and reconstructs one branch from unchanged W01-403 S030. Every event carries before/after state hashes, forward operations, and inverse operations. The verifier replays the branch, then reverses every operation to reproduce the exact S030 snapshot.\n\nThe trace includes all regular markers, budgets, recharge, spell and Dissonance/Refrain history, Spell Efficiency windows, death saves, custody, corrected Grounding RP balances, and all three Director corrections: each Bolt cast is explicitly resolved while preserving its paid history; Arcane Sight concentration starts at commit 127.1 and aura perception begins only after successful resolution at 127.2; B makes no Counterspell attempt, leaving self-counter eligibility unadjudicated. The successful Dispel, root termination, and ordered Q27 body/item settlement preserve the adopted scope.\n\nNo campaign occurrence, seal, Fortress identity acceptance/application, canon change, parent mutation, or queue mutation is asserted. Authority remains 830/18/0; Fortress remains held under PG200-B06.\n\nRun `python VERIFY_W05_W10_WITNESS_453.py` from this directory.\n",encoding="utf-8",newline="\n")
    package=[BUILDER_PATH,VERIFY_PATH,PROPOSAL_PATH,ADOPTION_PATH,WITNESS_PATH,VALIDATION_PATH,README_PATH]
    manifest={"id":"PG328-W05-W10-MANIFEST-453","classification":"TEST_ONLY_REVIEW_PACKAGE","files":[{"path":rel(p),"bytes":p.stat().st_size,"sha256":sha(p)} for p in package]}; dump(MANIFEST_PATH,manifest); package.append(MANIFEST_PATH)
    with zipfile.ZipFile(ARCHIVE_PATH,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for p in package: z.write(p,arcname=p.name)
    dump(DELIVERY_PATH,{"id":"PG328-W05-W10-DELIVERY-453","classification":"TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW","supersedesWitnessSha256":witness["supersedesWitness"]["sha256"],"witnessPath":rel(WITNESS_PATH),"witnessBytes":WITNESS_PATH.stat().st_size,"witnessSha256":sha(WITNESS_PATH),"archivePath":rel(ARCHIVE_PATH),"archiveBytes":ARCHIVE_PATH.stat().st_size,"archiveSha256":sha(ARCHIVE_PATH),"manifestPath":rel(MANIFEST_PATH),"validationPath":rel(VALIDATION_PATH),"validationSha256":sha(VALIDATION_PATH),"queue":{"reviewedApplied":830,"pending":18,"acceptedUnapplied":0,"changed":False},"directorReviewRequested":True})
    print(json.dumps({"status":validation["status"],"passed":validation["passed"],"failed":validation["failed"],"events":len(events),"starts":validation["regularTurnStartCount"],"ends":validation["regularTurnEndCount"],"forward":validation["forwardOperations"],"inverse":validation["inverseOperations"],"witnessSha256":sha(WITNESS_PATH),"archiveSha256":sha(ARCHIVE_PATH)},indent=2))

if __name__=="__main__": main()
