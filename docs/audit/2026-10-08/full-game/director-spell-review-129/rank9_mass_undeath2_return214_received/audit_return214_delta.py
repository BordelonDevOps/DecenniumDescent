import hashlib, json, os, pathlib, re, zlib, zipfile

repo = pathlib.Path(r"C:\\Github\\DecenniumDescent-review-push-134")
recv = repo / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_mass_undeath2_return214_received"
delta = recv / "DD_Rank9_MassUndeath2_Director_Return214_DELTA.zip"
delivery_path = recv / "DD_Rank9_MassUndeath2_Director_Return214_DELTA_DELIVERY.json"
original_delivery_path = recv / "DD_Rank9_MassUndeath2_Director_Return214_DELIVERY.json"
prior = repo / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_mass_undeath2_return213_received/DD_Rank9_MassUndeath2_Director_Return213_HELD.zip"
prior_delivery = repo / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_mass_undeath2_return213_received/DD_Rank9_MassUndeath2_Director_Return213_HELD_DELIVERY.json"
source02 = repo / "docs/audit/2026-10-08/full-game/DD_Rank9_Mass_Undeath_2_Source_Conference_02.zip"

def file_hashes(path):
    h = hashlib.sha256()
    c = 0
    n = 0
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            n += len(b)
            h.update(b)
            c = zlib.crc32(b, c)
    return {"bytes": n, "sha256": h.hexdigest(), "crc32": f"{c & 0xffffffff:08x}"}

d = json.loads(delivery_path.read_text(encoding="utf-8-sig"))
o = json.loads(original_delivery_path.read_text(encoding="utf-8-sig"))
checks = []
def check(name, ok, detail=None):
    checks.append({"check": name, "passed": bool(ok), **({"detail": detail} if detail is not None else {})})

# Outer artifact and delivery binding
actual_delta = file_hashes(delta)
check("delta archive size/SHA256/CRC32", actual_delta["bytes"] == d.get("bytes") and actual_delta["sha256"] == d.get("sha256") and actual_delta["crc32"] == d.get("crc32"), {"actual": actual_delta, "expected": {k: d.get(k) for k in ("bytes", "sha256", "crc32")}})
orig_delivery_actual = file_hashes(original_delivery_path)
check("source delivery manifest byte binding", orig_delivery_actual["bytes"] == d["sourceDelivery"]["bytes"] and orig_delivery_actual["sha256"] == d["sourceDelivery"]["sha256"] and orig_delivery_actual["crc32"] == d["sourceDelivery"]["crc32"], {"actual": orig_delivery_actual, "expected": d["sourceDelivery"]})
check("accepted IDs and unapplied state", d.get("accepted") is True and d.get("acceptedIds") == ["field-of-endless-dead", "plague-of-undeath"] and d.get("applied") is False and d.get("appliedIds") == [] and d.get("heldTargetIds") == [], {"acceptedIds": d.get("acceptedIds"), "applied": d.get("applied"), "appliedIds": d.get("appliedIds"), "heldTargetIds": d.get("heldTargetIds")})
auth = d["authoritySnapshotUnchanged"]["authority"]
check("authority snapshot 804/44/0", auth == {"reviewedApplied": 804, "pending": 44, "acceptedUnapplied": 0, "completeStandaloneProcedures": 528, "scopedInterfaces": 173}, auth)
check("package verification claims all pass", d["packageVerification"].get("passed") is True and all(c.get("passed") is True for c in d["packageVerification"].get("checks", [])) and len(d["packageVerification"].get("checks", [])) == d["packageVerification"].get("checkCount"), {"claimedCount": d["packageVerification"].get("checkCount"), "observedCount": len(d["packageVerification"].get("checks", []))})
check("unchanged case/semantic contents claim", d.get("reviewSemanticsChanged") is False and d.get("canonicalChanges") is False and d.get("githubChanges") is False)

# Verify omitted external member against both delivery and local byte-exact copy
external = d["externalRequiredMembers"]
external_entry = next((x for x in external if x.get("path") == "prior/Return213.zip"), None)
prior_actual = file_hashes(prior)
check("omitted prior archive exact local binding", external_entry is not None and prior_actual["bytes"] == external_entry.get("bytes") == o["priorArchiveByteExact"]["bytes"] and prior_actual["sha256"] == external_entry.get("sha256") == o["priorArchiveByteExact"]["sha256"] and prior_actual["crc32"] == external_entry.get("crc32"), {"actual": prior_actual, "external": external_entry, "original": o["priorArchiveByteExact"]})
prior_delivery_actual = file_hashes(prior_delivery)
prior_delivery_member = next((x for x in d["members"] if x.get("path") == "prior/Return213_DELIVERY.json"), None)
check("prior delivery member matches local evidence", prior_delivery_member is not None and prior_delivery_actual["bytes"] == prior_delivery_member.get("bytes") and prior_delivery_actual["sha256"] == prior_delivery_member.get("sha256") and prior_delivery_actual["crc32"] == prior_delivery_member.get("crc32"), {"actual": prior_delivery_actual, "member": prior_delivery_member})

# Verify current source conference binding against local packet and original manifest claim
source_actual = file_hashes(source02)
source_binding = o.get("nestedSourceArchiveByteExact", {})
check("Source Conference 02 archive exact local binding", source_actual["bytes"] == source_binding.get("bytes") == 291977874 and source_actual["sha256"] == source_binding.get("sha256") == "4af12a5cd32fc8cbdab98e204ef21965d11d1a3fa178bbcff64ddc64deac779d", {"actual": source_actual, "originalClaim": source_binding})

# Verify exact 40-member delta allowlist, member data SHA/size/CRC, CRC-checking decompression
members_expected = {x["path"]: x for x in d["members"]}
allowlist = d["allowlist"]
check("manifest member count/allowlist shape", len(members_expected) == d.get("memberCount") == 40 and len(allowlist) == 40 and set(members_expected) == set(allowlist) and len(set(allowlist)) == len(allowlist), {"manifestMembers": len(members_expected), "allowlist": len(allowlist), "memberCount": d.get("memberCount")})
member_results = []
zip_errors = []
with zipfile.ZipFile(delta, "r") as zf:
    names = zf.namelist()
    check("archive exact allowlist, unique names", len(names) == 40 and len(names) == len(set(names)) and set(names) == set(allowlist), {"archiveMembers": len(names), "unique": len(names) == len(set(names)), "missing": sorted(set(allowlist) - set(names)), "extra": sorted(set(names) - set(allowlist))})
    unsafe = [n for n in names if pathlib.PurePosixPath(n).is_absolute() or ".." in pathlib.PurePosixPath(n).parts or "\\" in n or n.startswith(".")]
    check("archive paths have no traversal/hidden members", not unsafe, unsafe)
    for name in names:
        exp = members_expected.get(name)
        if exp is None:
            continue
        h = hashlib.sha256(); crc = 0; size = 0
        try:
            with zf.open(name, "r") as f:
                while True:
                    b = f.read(1024 * 1024)
                    if not b:
                        break
                    size += len(b); h.update(b); crc = zlib.crc32(b, crc)
            actual = {"path": name, "bytes": size, "sha256": h.hexdigest(), "crc32": f"{crc & 0xffffffff:08x}"}
            ok = size == exp.get("bytes") and actual["sha256"] == exp.get("sha256") and actual["crc32"] == str(exp.get("crc32", "")).lower()
            member_results.append({**actual, "expected": exp, "passed": ok})
            if not ok:
                zip_errors.append(name)
        except Exception as e:
            zip_errors.append(name + ": " + repr(e))
    try:
        bad = zf.testzip()
    except Exception as e:
        bad = repr(e)
    check("ZIP CRC/decompression test", bad is None, bad)
check("all delta member size/SHA256/CRC32 bindings", len(member_results) == 40 and not zip_errors and all(x["passed"] for x in member_results), {"verified": len(member_results), "errors": zip_errors[:20]})

# Compare every transmitted member with the original full Return214 delivery manifest;
# the only omitted original member must be the explicitly bound Return213 archive.
orig_members = {x["path"]: x for x in o["members"]}
expected_delta_from_original = set(orig_members) - {"prior/Return213.zip"}
check("delta members equal original logical allowlist minus only prior archive", set(members_expected) == expected_delta_from_original, {"originalCount": len(orig_members), "deltaCount": len(members_expected), "omitted": sorted(set(orig_members) - set(members_expected)), "unexpected": sorted(set(members_expected) - set(orig_members))})
member_diffs = []
for name, actual_entry in members_expected.items():
    old = orig_members.get(name)
    if old is None or any(actual_entry.get(k) != old.get(k) for k in ("bytes", "sha256", "crc32")):
        member_diffs.append({"path": name, "delta": actual_entry, "original": old})
check("all retained members byte-identical to original delivery manifest", not member_diffs, member_diffs[:5])
check("external omission exactly equals original Return213 member", external_entry is not None and orig_members.get("prior/Return213.zip") is not None and all(external_entry.get(k) == orig_members["prior/Return213.zip"].get(k) for k in ("bytes", "sha256", "crc32")))

# Extract exact checked members for the semantic review and the eventual index application.
extract_root = recv / "extracted"
if all(c["passed"] for c in checks):
    with zipfile.ZipFile(delta, "r") as zf:
        for name in allowlist:
            target = (extract_root / pathlib.PurePosixPath(name)).resolve()
            if not target.is_relative_to(extract_root.resolve()):
                raise RuntimeError("Unsafe extraction path: " + name)
        zf.extractall(extract_root)
    extracted = True
else:
    extracted = False

result = {
    "id": "RETURN214-DELTA-INDEPENDENT-AUDIT",
    "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
    "archive": {"path": str(delta.relative_to(repo)), **actual_delta},
    "deliveryManifest": {"path": str(delivery_path.relative_to(repo)), "bytes": delivery_path.stat().st_size, "sha256": hashlib.sha256(delivery_path.read_bytes()).hexdigest()},
    "acceptedIds": d.get("acceptedIds"),
    "applied": d.get("applied"),
    "authorityBeforeApplication": auth,
    "externalOmissions": external,
    "checks": checks,
    "verifiedMemberCount": len(member_results),
    "extracted": extracted,
    "extractionRoot": str(extract_root.relative_to(repo)) if extracted else None,
    "memberResults": member_results,
}
out = recv / "RETURN214_DELTA_INDEPENDENT_AUDIT.json"
out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"status": result["status"], "checkCount": len(checks), "checksPassed": sum(c["passed"] for c in checks), "verifiedMembers": len(member_results), "acceptedIds": d.get("acceptedIds"), "authority": auth, "audit": str(out), "extracted": extracted}, indent=2))
if result["status"] != "PASS":
    sys.exit(1)
