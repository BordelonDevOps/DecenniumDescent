from __future__ import annotations
import copy, hashlib, json, math, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import build_fortress_closure_intake_367 as intake
OUT=ROOT/"fortress_w08_occupied_antimagic_witness_412"
ZIP=OUT/"DD_Rank9_ConjureDemiplaneFortress_PG328_W08_OccupiedAntimagicWitness_412_TESTONLY.zip"
SPACE="RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic/cast1/space"
FORTRESS="RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic/cast1"
FIELD="PG328-W08/occupied-antimagic/antimagic-field-cast1"
ORIGIN="fixture:origin"

def sha(b): return hashlib.sha256(b).hexdigest()
def readj(z,p): return json.loads(z.read(p).decode("utf-8-sig"))
def main():
    delivery=json.loads((OUT/"DELIVERY_412.json").read_text(encoding="utf-8-sig"))
    assert sha(ZIP.read_bytes())==delivery["sha256"] and ZIP.stat().st_size==delivery["bytes"]
    with zipfile.ZipFile(ZIP) as z:
        assert z.testzip() is None
        names=set(z.namelist())
        manifest=readj(z,"MANIFEST_412.json")
        listed={f["path"] for f in manifest["files"]}
        assert names==listed|{"MANIFEST_412.json"}
        for f in manifest["files"]:
            b=z.read(f["path"]); assert len(b)==f["bytes"] and sha(b)==f["sha256"]
        bindings=manifest["sourceBindings"]
        ids={b["id"] for b in bindings}
        for b in bindings:
            content=z.read("payload/"+b["path"]) if not b["path"].startswith("payload/") else z.read(b["path"])
            assert len(content)==b["bytes"] and sha(content)==b["sha256"],b["path"]
            if b["pointers"]:
                d=json.loads(content.decode("utf-8-sig"))
                for p in b["pointers"]: intake.get_at_pointer(d,p)
        case=readj(z,"payload/case/PG328_W08_OCCUPIED_ANTIMAGIC_INTEGRATED_WITNESS_412_TESTONLY.json")
        assert set(case["sourceBindingIds"])<=ids
        parent=readj(z,"payload/parent/RETURN284_OCCUPIED_ANTIMAGIC_CASE.json")
        assert sha(z.read("payload/parent/RETURN284_OCCUPIED_ANTIMAGIC_CASE.json"))==case["parentBinding"]["parentCaseSha256"]
        assert intake.digest(parent["final"])==case["parentBinding"]["parentFinalStateSha256"]
        assert case["initial"]==parent["final"]
        s=copy.deepcopy(case["initial"])
        prev_time=s["time"]
        for e in case["events"]:
            assert e["sourceBindings"] and set(e["sourceBindings"])<=ids
            assert intake.digest(s)==e["beforeSHA256"]
            assert e["eventTime"]["initiativeSeconds"]>=prev_time-1e-9
            assert abs(e["eventTime"]["worldElapsedSeconds"]-e["eventTime"]["initiativeSeconds"]-0.1)<1e-6
            s=intake.apply_ops(s,e["forward"])
            assert s==e["after"] and intake.digest(s)==e["afterSHA256"]
            assert intake.apply_ops(e["after"],e["inverse"])==e["before"]
            prev_time=e["eventTime"]["initiativeSeconds"]
        assert s==case["final"] and intake.digest(s)==case["finalSHA256"]
        r=copy.deepcopy(s)
        for e in reversed(case["events"]):
            r=intake.apply_ops(r,e["inverse"]); assert r==e["before"]
        assert r==case["initial"]
        assert len(case["events"])==16
        actor=s["actors"]["A"]
        assert actor["plane"]==ORIGIN and actor["position"]==[15.0,0.0,0.0]
        assert actor["RP"]==33 and actor["lastSpell"]=="antimagic-field" and actor["concentration"] is None
        assert actor["regularSchedule"]["ends"][-1]==6.9
        assert actor["spellEfficiency"]==[{"family":"antimagic-field","until":12.9,"worldUntil":13.0,
            "triggeredByCastId":FIELD,"status":"TEST_ONLY_UNSPENT","noDiscountAppliedByThisCast":True,
            "noCanonicalStackingRuleAsserted":True}]
        assert s["effects"][FIELD]["active"] is False and s["effects"][FIELD]["deadline"]==66.1
        assert s["effects"][FIELD]["terminalReceipt"]["relocated"] is False
        assert s["effects"][FIELD]["terminalReceipt"]["refundRp"]==0
        assert s["effects"][FORTRESS]["active"] is False and not s["spaces"][SPACE]["exists"]
        for i in ("focus-A","pack-A","cargo-A"):
            assert s["items"][i]["exists"] and not s["items"][i]["consumed"]
            assert s["items"][i]["plane"]==ORIGIN and s["items"][i]["custodian"]=="A"
        for a,starts,ends in (("B",[1.0],[1.9]),("C",[2.0],[2.9]),("D",[3.0],[3.9]),("A",[0.0,6.0],[0.9,6.9])):
            assert s["actors"][a]["regularSchedule"]["starts"][-len(starts):]==starts
            assert s["actors"][a]["regularSchedule"]["ends"][-len(ends):]==ends
        queue=readj(z,"payload/authority/CURRENT_SPELL_QUEUE_404.json")
        assert queue["currentAuthority"]["reviewedApplied"]==829
        assert queue["currentAuthority"]["pending"]==19 and queue["currentAuthority"]["acceptedUnapplied"]==0
        adoption=readj(z,"payload/owner/OWNER_PG328_W08_TESTONLY_ADOPTION_412.json")
        assert len(adoption["adoptedTerms"])==3
        assert adoption["limits"]["identityAcceptedOrApplied"] is False
        suppression=next(e for e in case["events"] if e["kind"]=="TEST_ONLY_OCCUPIED_STRUCTURAL_EXPRESSION_SUPPRESSED")
        assert suppression["detail"]["panelPenetration"] is False and suppression["detail"]["hpChanged"] is False if "hpChanged" in suppression["detail"] else suppression["detail"]["damage"]==0
        assert case["scope"]["identityAcceptedOrApplied"] is False and case["scope"]["fortressAcceptedOrApplied"] is False
    result={"status":"PASS_INDEPENDENT_ARCHIVE_SOURCE_REPLAY_AND_LIFECYCLE_AUDIT",
            "artifact":ZIP.name,"sha256":delivery["sha256"],"bytes":delivery["bytes"],
            "members":delivery["members"],"sourceBindings":len(bindings),"events":len(case["events"]),
            "forwardReplay":True,"fullReverseRestoration":True,"parentImmutable":True,
            "geometryAndTerminalState":"PASS","queue":"829/19/0 unchanged"}
    (OUT/"INDEPENDENT_VERIFICATION_412.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()