from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import zipfile
from datetime import datetime, timezone


HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "fortress_w08_fixed_entry_anchor_repair_396"
OUT = HERE / "fortress_w08_manifest_binding_repair_397"
SOURCE_ZIP = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_FixedEntryAnchor396_TESTONLY.zip"
ZIP_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_FixedEntryAnchor396_ManifestRepair397_TESTONLY.zip"
MANIFEST = "PG328-W08_PREBUILD_SOURCE_BINDINGS_396.json"
DELIVERY = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_FixedEntryAnchor396_ManifestRepair397_TESTONLY_DELIVERY.json"
REPAIR = "PG328-W08_MANIFEST_MEMBER_PATH_REPAIR_397.json"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jb(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    old_delivery = json.loads((SOURCE / "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_FixedEntryAnchor396_TESTONLY_DELIVERY.json").read_text(encoding="utf-8"))
    old_zip_path = SOURCE / SOURCE_ZIP
    with zipfile.ZipFile(old_zip_path) as z:
        old_files = {n: z.read(n) for n in z.namelist()}
    old_manifest_member = "authority/" + MANIFEST
    old_manifest_raw = old_files[old_manifest_member]
    m = json.loads(old_manifest_raw)
    old_proposals = copy.deepcopy(m.get("reviewProposals", []))
    old_request = copy.deepcopy(m.get("reviewRequest", {}))
    expected_current = set(old_files)
    missing = []
    for item in old_proposals:
        if item.get("name", "").endswith("_395_TESTONLY.json"):
            member = item.get("bundleMember", "")
            if member not in expected_current:
                missing.append(member)
                item["bundleMember"] = "prior395/" + member
                item["status"] = "SUPERSEDED; RETAINED UNDER prior395/"
    if old_request.get("bundleMember") and old_request["bundleMember"] not in expected_current:
        missing.append(old_request["bundleMember"])
        old_request["bundleMember"] = "prior395/" + old_request["bundleMember"]
        old_request["status"] = "SUPERSEDED; RETAINED UNDER prior395/"
    assert len(missing) == 4, missing

    m["supersededReviewProposals395"] = old_proposals
    m["supersededReviewRequest395"] = old_request
    # The generic current-schema keys now point only at the 396 artifacts that are in this bundle.
    m["reviewProposals"] = copy.deepcopy(m["reviewProposals396"])
    m["reviewRequest"] = copy.deepcopy(m["reviewRequest396"])
    m["manifestPathRepair397"] = {
        "sourceManifestSha256": sha(old_manifest_raw),
        "sourcePackageSha256": old_delivery["sha256"],
        "correctedAbsent395Members": missing,
        "correction": "Keep superseded 395 records under prior395/ and point generic current manifest keys at the present 396 payload members.",
        "currentMemberPointersVerifiedAgainstBundle": True,
    }
    manifest_raw = jb(m)

    repair = {
        "id": "PG328-W08-MANIFEST-MEMBER-PATH-REPAIR-397",
        "createdAtUtc": NOW,
        "status": "PACKAGING_ONLY_POINTER_REPAIR_NO_SUBSTANTIVE_PROPOSAL_CHANGE",
        "sourcePackage": {"artifact": old_delivery["artifact"], "sha256": old_delivery["sha256"]},
        "sourceManifestSha256": sha(old_manifest_raw),
        "correctedManifestSha256": sha(manifest_raw),
        "missingOldReferences": missing,
        "correctedOldReferences": ["prior395/" + x for x in missing],
        "currentProposalMembers": [x["bundleMember"] for x in m["reviewProposals"]],
        "currentReviewRequestMember": m["reviewRequest"]["bundleMember"],
        "unchangedSubstantive396Files": True,
        "inheritedCaseSha256": old_delivery["originalCaseMemberSha256"],
        "fixtureMutated": False,
        "actualCast": False,
        "ownerAdoptionOf396": False,
        "queue": old_delivery["ordinaryQueue"],
    }
    repair_raw = jb(repair)

    current_manifest_member = "authority/" + MANIFEST
    previous_manifest_member = "prior396/authority/" + MANIFEST
    with zipfile.ZipFile(OUT / ZIP_NAME, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in old_files.items():
            z.writestr(previous_manifest_member if name == current_manifest_member else name, raw)
        z.writestr(current_manifest_member, manifest_raw)
        z.writestr("payload/reviews/" + REPAIR, repair_raw)

    zip_path = OUT / ZIP_NAME
    with zipfile.ZipFile(zip_path) as z:
        assert z.testzip() is None
        names = set(z.namelist())
        assert len(names) == len(z.namelist())
        current = json.loads(z.read(current_manifest_member))
        assert all(p["bundleMember"] in names for p in current["reviewProposals"])
        assert current["reviewRequest"]["bundleMember"] in names
        assert all(p["bundleMember"] in names for p in current["supersededReviewProposals395"])
        assert current["supersededReviewRequest395"]["bundleMember"] in names
        assert z.read("payload/cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json") == old_files["payload/cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json"]
        assert z.read("payload/PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json") == old_files["payload/PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json"]

    # Sidecars needed to inspect the repair without unpacking the ZIP.
    (OUT / MANIFEST).write_bytes(manifest_raw)
    (OUT / REPAIR).write_bytes(repair_raw)
    delivery = {
        "id": "DD-RANK9-PG328-W08-396-MANIFEST-REPAIR-397-TESTONLY-DELIVERY",
        "createdAtUtc": NOW,
        "status": "READY_FOR_DIRECTOR_CONSISTENCY_REVIEW_PENDING_TRANSMISSION",
        "supersedesPackage": {"artifact": old_delivery["artifact"], "sha256": old_delivery["sha256"]},
        "artifact": ZIP_NAME,
        "sha256": sha(zip_path.read_bytes()),
        "bytes": zip_path.stat().st_size,
        "bundleMemberCount": len(zipfile.ZipFile(zip_path).infolist()),
        "manifestSha256": sha(manifest_raw),
        "repairRecordSha256": sha(repair_raw),
        "prebuildSha256Unchanged": old_delivery["prebuildSha256"],
        "sourceBindingsSha256": sha(manifest_raw),
        "inheritedCaseSha256Unchanged": old_delivery["originalCaseMemberSha256"],
        "substantive396PayloadUnchanged": True,
        "ownerAdoptionOf396": False,
        "proposal386Sha256": old_delivery["terminationProposal386Sha256"],
        "ordinaryQueue": old_delivery["ordinaryQueue"],
        "fixtureMutated": False,
        "actualCast": False,
        "q27Settlement": False,
        "transmissionStatus": "NOT_YET_SENT",
    }
    delivery_path = OUT / DELIVERY
    delivery_path.write_bytes(jb(delivery))
    print(json.dumps({"zip": str(zip_path), "sha256": delivery["sha256"], "bytes": delivery["bytes"],
                      "members": delivery["bundleMemberCount"], "manifestSha256": delivery["manifestSha256"],
                      "fixedReferences": missing, "integrity": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
