from __future__ import annotations
import hashlib, json, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REVIEW=ROOT.parent
REPO=ROOT.parents[5]
PARENT=REVIEW/"fortress_w01_structural_damage_witness_403_repack02"/"W01_REPLAY_403.json"
P=ROOT/"OWNER_PG328_W11_ADOPTION_PROPOSAL_438.json"
O=ROOT/"OWNER_PG328_W11_ADOPTION_438_TESTONLY.json"
W=ROOT/"W11_WITNESS_456_TESTONLY.json"
T=ROOT/"W11_LIFECYCLE_TRACE_456.json"
V=ROOT/"BUILD_VALIDATION_456.json"
M=ROOT/"MANIFEST_456.json"
Z=ROOT/"DD_Fortress_W11_Witness_456_TESTONLY.zip"
D=ROOT/"DELIVERY_456.json"
R=REVIEW/"DIRECTOR_READBACK_454.json"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

p,o,w,t,v,parent=(load(x) for x in (P,O,W,T,V,PARENT))
s030=parent["stateSnapshots"]["S030"]
checks={
 "proposal and owner adoption exact":sha(P)=="44c150647453fb762aec288fc83ce2afe0a77c160ca810682919d320078ae3de" and o["scope"]["proposalSha256"]==sha(P) and sha(O)==w["adoption"]["sha256"],
 "parent replay hash separated from canonical S030 hash":sha(PARENT)==w["parent"]["replaySha256"] and hashlib.sha256(canon(s030)).hexdigest()==w["parent"]["snapshotSha256"]==w["parent"]["s030SnapshotSha256"],
 "trace payload and lineage bind":sha(T)==w["trace"]["sha256"] and w["trace"]["eventCount"]==len(t["events"])==30 and w["trace"]["events"]==t["events"] and w["supersedesWitness"]["sha256"]==sha(ROOT/"W11_WITNESS_449_TESTONLY.json"),
 "source-bound W11 turn/event/action/pet coverage preserved":len(t["turnMarkers"])==74 and len(t["events"])==30 and len(t["actions"])==10 and len(t["petPhases"])==10,
 "B hands record focus left and cargo right":t["actions"][1]["handsAfter"]=={"left":"focus-B","right":"cargo-B"} and "left hand remains occupied by focus-B" in t["actions"][1]["actionUse"],
 "Sight 600-second deadline begins at commit":t["events"][19]["time"]==96.3 and t["events"][19]["concentrationStartsAt"]==96.1 and t["events"][19]["concentrationDeadline"]==696.1 and t["events"][19]["auraPerceptionBeginsAt"]==96.3,
 "36.0 cargo-A transfer records owner and custody before/after":t["actions"][6]["cargoTransfer"]["before"]["custodian"]=="A" and t["actions"][6]["cargoTransfer"]["after"]["custodian"]=="PG328-W11-R1:greater-fire-pet-1" and t["actions"][6]["cargoTransfer"]["after"]["owner"]=="A",
 "94.3 expiry records supported 3-foot zero-damage fall":t["events"][15]["cargoFallsFeet"]==3 and t["events"][15]["cargoAfter"]["custodian"] is None and t["events"][15]["fallResult"]["damage"]==0 and bool(t["events"][15]["cargoAfter"]["support"]),
 "102.3 Q27 records root, body, and stable-ID item settlement":[x["type"] for x in t["events"][24:30]]==["Q27_FORTRESS_TERMINATION","Q27_BODY_RETURN","Q27_BODY_RETURN","Q27_BODY_RETURN","Q27_LOOSE_ITEM_SETTLEMENT","Q27_LOOSE_ITEM_SETTLEMENT"] and [x["itemId"] for x in t["events"][24:30] if x["type"]=="Q27_LOOSE_ITEM_SETTLEMENT"]==[x["id"] for x in p["closure"]["looseItemsStableIdOrder"]] and t["closureResults"]["bodyOrder"]==["A","B","actor-w11-firepet-owner"],
 "tile deadline preserved and expired pet excluded":t["closureResults"]["tileDeadline"]==3606.13 and t["closureResults"]["expiredPetReturnedAsBody"] is False and t["events"][15]["expiredPetLootCreated"] is False,
 "TEST_ONLY queue and authority boundaries unchanged":w["terminalAndQueueBoundary"]["queue"]=="830 applied / 18 pending / 0 accepted-unapplied" and all(w["terminalAndQueueBoundary"][x] is False for x in ("sealPresent","FortressAcceptedOrApplied","spellIdentityAcceptedOrApplied","canonicalRuleChanged","historicalParentMutated","campaignEventsAsserted","queueChanged")),
 "build validation binds current witness and trace":v["status"]=="PASS" and v["witnessSha256"]==sha(W) and v["traceSha256"]==sha(T) and v["failed"]==0 and v["passed"]==len(v["checks"]),
}
manifest=load(M); delivery=load(D)
member_paths={x["path"]:(R if x["path"]==R.name else ROOT/x["path"]) for x in manifest["files"]}
with zipfile.ZipFile(Z) as archive:
 checks["review archive exact member bytes and hashes"] = archive.testzip() is None and set(archive.namelist())==set(member_paths)|{M.name} and all(member_paths[name].stat().st_size==record["bytes"] and sha(member_paths[name])==record["sha256"] and archive.read(name)==member_paths[name].read_bytes() for name,record in ((x["path"],x) for x in manifest["files"]))
checks["delivery binds witness trace validation manifest and archive"] = delivery["witnessSha256"]==sha(W) and delivery["traceSha256"]==sha(T) and delivery["validationSha256"]==sha(V) and delivery["manifestSha256"]==sha(M) and delivery["archiveSha256"]==sha(Z)
for name,ok in checks.items(): print(("PASS" if ok else "FAIL")+": "+name)
if not all(checks.values()): raise SystemExit(1)
print(f"PASS: {sum(checks.values())}/{len(checks)} independent checks; W11 remains TEST_ONLY and unsealed.")
