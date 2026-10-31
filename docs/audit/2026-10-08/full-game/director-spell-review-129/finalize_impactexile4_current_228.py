from __future__ import annotations
import copy, hashlib, json, zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/"docs/audit/2026-10-08/full-game/director-spell-review-129"
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f"{zlib.crc32(b)&0xffffffff:08x}"
def dump(v): return (json.dumps(v,ensure_ascii=False,indent=2)+"\n").encode()
def info(p):
    b=p.read_bytes()
    return {"path":p.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":sha(b),"crc32":crc(b)}
def main():
    q227,h227,p228=read(AUDIT/"CURRENT_SPELL_QUEUE_227.json"),read(AUDIT/"CURRENT_HANDOFF_227.json"),read(AUDIT/"CURRENT37_PENDING_IDENTITY_AUDIT_228.json")
    delivery=read(AUDIT/"rank9_impactexile4_current_source_228_prepared/DD_Rank9_ImpactExile4_CurrentSource_228_DELIVERY.json")
    receipt=read(AUDIT/"RANK9SUMMONHOSTS5_RETURN227_RECEIPT.json")
    audit=read(AUDIT/"RANK9SUMMONHOSTS5_RETURN227_INDEPENDENT_AUDIT.json")
    prep=read(AUDIT/"RANK9IMPACTEXILE4_SOURCE_PREPARATION_228.json")
    packet=read(AUDIT/"RANK9IMPACTEXILE4_PACKET_228.json")
    auth={"reviewedApplied":811,"pending":37,"acceptedUnapplied":0,"completeStandaloneProcedures":535,"scopedInterfaces":173}
    targets=["reverse-gravity-field"]
    group=next(x for x in q227["currentPendingGroups"] if x["group"]=="rank9-impact-exile4")
    assert delivery["sourceAuthority"]==auth and delivery["pendingIds"]==targets and audit["status"]=="PASS"
    assert prep["status"]=="PASS" and packet["archive"]["sha256"]==delivery["archive"]["sha256"]
    assert receipt["heldIds"]==["summon-elemental-avatar","summon-herald-of-the-planes","summon-avatar-of-decay"]
    now=datetime.now(timezone.utc).isoformat()
    prepared={"group":"rank9-impact-exile4","pendingIds":targets,"pendingCount":1,
        "status":"CURRENT_SOURCE_PACKET_228_PREPARED_UNSENT","freshPacketRequiredForCurrentAuthority":True,
        "packet":delivery["archive"],"deliveryManifest":info(AUDIT/"rank9_impactexile4_current_source_228_prepared/DD_Rank9_ImpactExile4_CurrentSource_228_DELIVERY.json")}
    q=copy.deepcopy(q227)
    q.update({"id":"SPELL-REVIEW-QUEUE-228","recordedAtUtc":now,"supersedesQueue":info(AUDIT/"CURRENT_SPELL_QUEUE_227.json"),
        "nextGroup":"rank9-impact-exile4","next":prepared,"nextPreparedRequest":prepared,
        "packetStatus":"RANK9_IMPACT_EXILE4_PACKET_228_PREPARED_UNSENT_811_37"})
    for row in q["currentPendingGroups"]:
        if row["group"]=="rank9-summon-hosts5":
            row.update({"status":"HELD_RETURN227_INDEPENDENTLY_AUDITED","freshPacketRequiredForCurrentAuthority":True,
                "lastDirectorReturn":{"return":227,"acceptedIds":[],"appliedIds":[],"heldIds":receipt["heldIds"],
                    "blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
                    "independentAudit":info(AUDIT/"RANK9SUMMONHOSTS5_RETURN227_INDEPENDENT_AUDIT.json"),
                    "auditReceipt":info(AUDIT/"RANK9SUMMONHOSTS5_RETURN227_RECEIPT.json")}})
        if row["group"]=="rank9-impact-exile4":
            row.update({"status":"CURRENT_SOURCE_PACKET_228_PREPARED_UNSENT_811_37","pendingIds":targets,
                "pendingCount":1,"freshPacketRequiredForCurrentAuthority":True,"preparedPacket":delivery["archive"],
                "preparedDelivery":prepared["deliveryManifest"],
                "lastDirectorReturn":{"return":205,"acceptedIds":["eternal-anvil","transmute-flesh-to-energy","planar-collapse"],
                    "appliedIds":["eternal-anvil","transmute-flesh-to-energy","planar-collapse"],"heldIds":targets,
                    "blockers":{"reverse-gravity-field":["IE204-B02"]},
                    "independentAudit":info(AUDIT/"RANK9IMPACTEXILE4_RETURN205_INDEPENDENT_AUDIT.json")}})
    q["next"]={**prepared,"historicalCandidate":group.get("candidate"),"historicalArchive":group.get("archive")}
    q["currentPacket"],q["currentPacketDelivery"],q["currentPreparation"]=delivery["archive"],prepared["deliveryManifest"],info(AUDIT/"RANK9IMPACTEXILE4_SOURCE_PREPARATION_228.json")
    q["pendingIdentityAudit"]={"id":p228["id"],"path":(AUDIT/"CURRENT37_PENDING_IDENTITY_AUDIT_228.json").relative_to(ROOT).as_posix(),"pendingCount":37,"sha256":sha((AUDIT/"CURRENT37_PENDING_IDENTITY_AUDIT_228.json").read_bytes())}
    q["currentReturnArchive"]=info(AUDIT/"rank9_summonhosts5_return227_received/DD_Rank9_SummonHosts3_Director_Return227.zip")
    q["currentReturnDelivery"]=info(AUDIT/"rank9_summonhosts5_return227_received/DD_Rank9_SummonHosts3_Director_Return227_DELIVERY.json")
    q["currentReturnAudit"]=info(AUDIT/"RANK9SUMMONHOSTS5_RETURN227_INDEPENDENT_AUDIT.json")
    q["currentReturnReceipt"]=info(AUDIT/"RANK9SUMMONHOSTS5_RETURN227_RECEIPT.json")
    q["lastReviewedBatch"]={"return":227,"group":"rank9-summon-hosts5","acceptedIds":[],"appliedIds":[],"heldIds":receipt["heldIds"],
        "blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
        "independentAudit":q["currentReturnAudit"],"auditReceipt":q["currentReturnReceipt"]}
    (AUDIT/"CURRENT_SPELL_QUEUE_228.json").write_bytes(dump(q))
    h=copy.deepcopy(h227)
    h.update({"id":"CURRENT-HANDOFF-228","recordedAtUtc":now,"status":"RETURN227_AUDITED_HELD_NEXT_IMPACTEXILE4_PACKET_228_PREPARED_UNSENT_811_37"})
    h["latestBatch"]={"return":227,"group":"rank9-summon-hosts5","ids":receipt["heldIds"],"acceptedIds":[],"appliedIds":[],
        "heldIds":receipt["heldIds"],"blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
        "independentAudit":q["currentReturnAudit"],"auditReceipt":q["currentReturnReceipt"],
        "archiveLabelNote":"Returned ZIP label says SummonHosts3; SH227 manifest, exact target IDs, decisions and hashes independently validate."}
    h["nextStep"]={"group":"rank9-impact-exile4","pendingIds":targets,"pendingCount":1,
        "status":"CURRENT_SOURCE_PACKET_228_PREPARED_UNSENT_AT_AUTHORITY_811_37_0","freshPacketRequiredForCurrentAuthority":True,
        "candidate":group.get("candidate"),"archive":group.get("archive"),"packet":delivery["archive"],"deliveryManifest":prepared["deliveryManifest"]}
    h["nextGroup"],h["nextPendingCount"]="rank9-impact-exile4",1
    h["pendingIdentityAudit"]=q["pendingIdentityAudit"]
    h["queue"]=info(AUDIT/"CURRENT_SPELL_QUEUE_228.json"); h["currentQueueBinding"]=h["queue"]
    h["currentPacket"],h["currentPacketDelivery"],h["currentPreparation"]=delivery["archive"],prepared["deliveryManifest"],q["currentPreparation"]
    h["currentReturnBinding"],h["currentReturnDelivery"],h["currentReturnAudit"],h["currentReturnReceipt"]=q["currentReturnArchive"],q["currentReturnDelivery"],q["currentReturnAudit"],q["currentReturnReceipt"]
    h["nextPreparedRequest"]=prepared
    h["resumePriority"]="Submit packet228 for exactly reverse-gravity-field to GPT, ping if stalled, independently audit its return, and apply only an exact accepted identity."
    (AUDIT/"CURRENT_HANDOFF_228.json").write_bytes(dump(h))
    (AUDIT/"CURRENT_SPELL_REVIEW_SNAPSHOT_228.md").write_text("# Current ordinary spell-review checkpoint 228\n\n"
        "Return227 was independently audited and held exactly the three Summon Hosts5 identities. Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied** "
        "(535 complete standalone procedures; 173 scoped interfaces). The next fresh packet is rank9-impact-exile4, scoped to reverse-gravity-field; the Return205 acceptances remain closed.\n",
        encoding="utf-8",newline="\n")
    print(json.dumps({"status":"PASS","authority":auth,"nextGroup":h["nextStep"],"packet":delivery["archive"],"deliveryManifest":prepared["deliveryManifest"]},indent=2))
if __name__=="__main__": main()
