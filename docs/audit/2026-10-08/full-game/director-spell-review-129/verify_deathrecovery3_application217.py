import copy
import hashlib
import json
import pathlib
import zlib

ROOT = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_217.json"
HANDOFF = BASE / "CURRENT_HANDOFF_217.json"
PENDING = BASE / "CURRENT40_PENDING_IDENTITY_AUDIT_217.json"
OPS = BASE / "RANK9DEATHRECOVERY3_INDEX_OPERATIONS_217.json"
BACKUP = BASE / "authored_review_index.before_deathrecovery3_217.json"
APP = BASE / "RANK9DEATHRECOVERY3_APPLICATION_217.json"
VALIDATION = BASE / "RANK9DEATHRECOVERY3_APPLICATION_VALIDATION_217.json"
AUDIT = BASE / "rank9_deathrecovery7_return217_received/RETURN217_INDEPENDENT_AUDIT.json"
MODEL = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9deathrecovery3_reviewed_217/MODEL.json"
OUT = BASE / "RANK9DEATHRECOVERY3_POST_APPLICATION_INDEPENDENT_AUDIT_217.json"

def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))

def bind(p):
    b = p.read_bytes()
    return {"path": p.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "crc32": f"{zlib.crc32(b) & 0xffffffff:08x}"}

checks=[]
def ck(name, ok, detail=None):
    checks.append({"check":name,"passed":bool(ok),**({"detail":detail} if detail is not None else {})})

index=read(INDEX); catalog=read(CATALOG); queue=read(QUEUE); handoff=read(HANDOFF); pending=read(PENDING); ops=read(OPS); app=read(APP); val=read(VALIDATION); model=read(MODEL); return_audit=read(BASE/"rank9_deathrecovery7_return217_received/RETURN217_INDEPENDENT_AUDIT.json")
current_index=bind(INDEX); current_catalog=bind(CATALOG)
ck("Return217 independent archive audit passed", return_audit.get("status")=="PASS" and all(x.get("passed") for x in return_audit.get("checks",[])))
ck("exact 808/40/0 authority in index, queue, handoff and application", index.get("authoredCounts")=={"reviewed":808,"pending":40} and queue.get("currentAuthority",{}).get("reviewedApplied")==808 and queue.get("currentAuthority",{}).get("pending")==40 and queue.get("currentAuthority",{}).get("acceptedUnapplied")==0 and handoff.get("currentAuthority")==queue.get("currentAuthority") and app.get("countsAfter")==queue.get("currentAuthority"), queue.get("currentAuthority"))
ck("index and handoff bind exact current index bytes", queue.get("currentIndexBinding")==current_index and handoff.get("currentIndexBinding")==current_index, current_index)
ck("catalog unchanged and bound at queue216 digest", current_catalog.get("sha256")=="773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b" and queue.get("currentCatalogBinding")==current_catalog and handoff.get("currentCatalogBinding")==current_catalog, current_catalog)
entries={e["id"]:e for e in index["entries"]}; crows={e["id"]:e for e in catalog["spells"]}
ck("only exact accepted identities have Return217 reviewed-authored rows", all(entries[s]["authoredStatus"]=="reviewed-authored-operational-playtest" and entries[s]["reviewId"]=="RANK9-DEATHRECOVERY3-APPLICATION-217" for s in ("doom","eternal-pact")) and entries["final-word"]["authoredStatus"]=="pending-authored-procedure", {s:entries[s]["authoredStatus"] for s in ("doom","final-word","eternal-pact")})
ck("accepted native source statuses and catalog rows remain unchanged", all(entries[s]["sourceStatus"]=="blocked-pending-operational-review" and crows[s]["operational"] is None for s in ("doom","eternal-pact")) and entries["final-word"]["sourceStatus"]=="blocked-pending-operational-review")
noncatalog=sum(e.get("authoredStatus")=="reviewed-authored-operational-playtest" and e.get("procedureFile")!="catalog.json" for e in index["entries"])
ck("complete standalone procedure count reconciles to exact 532 reviewed noncatalog entries", index.get("representationCounts",{}).get("completeReviewedStandaloneProcedures")==532 and noncatalog==532, {"stored":index.get("representationCounts",{}).get("completeReviewedStandaloneProcedures"),"recounted":noncatalog})
live_pending={e["id"] for e in index["entries"] if e.get("authoredStatus")=="pending-authored-procedure"}
queued=[sid for g in queue.get("currentPendingGroups",[]) for sid in g.get("pendingIds",[])]
ck("pending audit and queue list exactly the 40 pending index identities", pending.get("exactPendingCount")==40 and pending.get("pendingIds")==queued and len(queued)==len(set(queued))==40 and set(queued)==live_pending, {"auditCount":pending.get("exactPendingCount"),"queueCount":len(queued),"missing":sorted(live_pending-set(queued)),"extra":sorted(set(queued)-live_pending)})
death=next(g for g in queue["currentPendingGroups"] if g["group"]=="rank9-death-recovery7")
ck("held Final Word remains the only Death/Recovery pending identity", death.get("pendingIds")==["final-word"] and death.get("lastDirectorReturn",{}).get("heldIds")==["final-word"] and death.get("lastDirectorReturn",{}).get("blockers")==["DR217-B01"])
next_group=next(g for g in queue["currentPendingGroups"] if g["group"]=="rank9-defense-form8")
ck("next actionable group skips held batches and is Defense/Form8", queue.get("nextGroup")=="rank9-defense-form8" and next_group.get("pendingIds")==["absolute-immunity","elemental-shell","body-to-void","timeless-form","invulnerable-sphere"])
ck("application validation is PASS with every check passing", val.get("status")=="PASS" and all(x.get("pass") for x in val.get("checks",[])))
ck("operation inverse restores exact prior index object", ops.get("inverseSemanticExact") is True)
before=read(BACKUP); inverse=copy.deepcopy(index)
for op in ops["operations"]: inverse["entries"][op["index"]]=copy.deepcopy(op["before"])
inverse["additionalStandaloneEnvelopes"]=inverse["additionalStandaloneEnvelopes"][:-1]
inverse["authoredCounts"]=copy.deepcopy(before["authoredCounts"])
inverse["representationCounts"]=copy.deepcopy(before["representationCounts"])
ck("replayed index inverse exactly restores byte-baseline semantics", inverse==before)
ck("candidate pointers resolve and procedures match accepted archive records", all(entries[s]["procedureFile"]=="../spell_candidates/rank9deathrecovery3_reviewed_217/MODEL.json" and model["spells"][i]["id"]==s and model["spells"][i]["accepted"] is True for i,s in enumerate(("doom","eternal-pact"))))
ck("unrelated Psychic/Fear holds remain pending", set(["psychic-scream","mass-phantom-killer","weird"]).issubset(live_pending))

result={"id":"RANK9DEATHRECOVERY3-POST-APPLICATION-INDEPENDENT-AUDIT-217","status":"PASS" if all(x["passed"] for x in checks) else "FAIL","acceptedIds":["doom","eternal-pact"],"heldIds":["final-word"],"authority":queue.get("currentAuthority"),"index":current_index,"catalog":current_catalog,"checks":checks}
OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps({"status":result["status"],"checks":len(checks),"passed":sum(x["passed"] for x in checks),"authority":result["authority"],"nextGroup":queue.get("nextGroup"),"audit":str(OUT.relative_to(ROOT))},indent=2))
if result["status"]!="PASS": raise SystemExit(1)
