import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
REPO = REVIEW.parents[4]
PROPOSAL = ROOT / "OWNER_DF218_B01_TEST_SOURCE_PROPOSAL_478_TESTONLY.json"
PREFLIGHT = ROOT / "SOURCE_GEOMETRY_PREFLIGHT_478.json"
README = ROOT / "README_PROPOSAL_478.md"
VALIDATION = ROOT / "INDEPENDENT_VALIDATION_478.json"
DELIVERY = ROOT / "DELIVERY_478.json"
MANIFEST = ROOT / "MANIFEST_478.json"
ARCHIVE = ROOT / "DD_ElementalShell_B01_TestSource_Proposal_478_TESTONLY.zip"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    return sha(path.read_bytes())


def within(inner, outer):
    return all(outer[axis][0] <= inner[axis][0] and inner[axis][1] <= outer[axis][1] for axis in ("x", "y", "z"))


def main():
    p = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    g = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    v = json.loads(VALIDATION.read_text(encoding="utf-8"))
    d = json.loads(DELIVERY.read_text(encoding="utf-8"))
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    passed = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        passed.append(name)

    read_commit = p["readAtCommit"]
    verified_bindings = []
    for binding in p["sourceBindings"]:
        raw = subprocess.check_output(["git", "show", f"{read_commit}:{binding['path']}"], cwd=REPO)
        blob = subprocess.check_output(["git", "hash-object", "--stdin"], input=raw, cwd=REPO).decode().strip()
        work = (REPO / binding["path"]).read_bytes()
        line_only = work == raw or work.replace(b"\r\n", b"\n") == raw.replace(b"\r\n", b"\n")
        check(f"source binding {binding['path']}", sha(raw) == binding["sha256"] and len(raw) == binding["bytes"] and blob == binding["gitBlobSha1"] and line_only and binding["lineEndingConversionOnly"])
        verified_bindings.append(binding["path"])

    check("proposal scope is B01-only and branch-local", p["scope"]["blocker"] == "DF218-B01-only" and p["scope"]["branchId"] == "DF218-SHELL-B01-TESTONLY-R1" and p["scope"]["onlyThisBranch"] and p["scope"]["separateFromB02"])
    check("prior B01 source audit remains a negative finding", p["sourceReview"]["result"] == "NO_QUALIFYING_SOURCE_FOUND")
    check("ownerless source is explicitly newly authored TEST_ONLY data", p["ownerProposedInputs"]["sourceContract"]["status"] == "NEW_AUTHORED_TEST_ONLY_SOURCE_PREMISE_NOT_A_RECOVERED_SOURCE_FACT" and p["ownerProposedInputs"]["sourceContract"]["responsibleCreatureDealer"] is None)
    check("Proposal468 is reused only as caster subpart and separate B01 adoption is required", p["ownerProposedInputs"]["casterQualificationReuse"]["newB01AdoptionMustSeparatelyPermitUse"] and p["ownerProposedInputs"]["casterQualificationReuse"]["noCurrentResourcesOrEncounterReadinessInferredFrom468"])

    actor = p["ownerProposedInputs"]["actor"]
    source = p["ownerProposedInputs"]["sourceContract"]
    event = source["event"]
    bounds = actor["bodyBoundsFeet"]
    focus = p["ownerProposedInputs"]["equipmentAndHands"]["focus"]["boundsFeet"]
    exposure = event["exposureVolumeFeet"]
    check("body fully lies in exposure volume", within(bounds, exposure))
    check("focus fully lies in exposure volume", within(focus, exposure))
    ground = p["ownerProposedInputs"]["scene"]["groundSupport"]
    check("ground support patch covers bearer footprint and body rests at z=0", ground["boundsFeet"]["x"][0] <= bounds["x"][0] and ground["boundsFeet"]["x"][1] >= bounds["x"][1] and ground["boundsFeet"]["y"][0] <= bounds["y"][0] and ground["boundsFeet"]["y"][1] >= bounds["y"][1] and bounds["z"][0] == ground["topZFeet"])
    check("left focus, right somatic hand, and voice are specified", p["ownerProposedInputs"]["equipmentAndHands"]["focus"]["leftHandCustody"] and p["ownerProposedInputs"]["equipmentAndHands"]["rightHand"] == "free for the S component" and p["ownerProposedInputs"]["equipmentAndHands"]["verbalComponent"] == "available and audible")

    cast = p["ownerProposedInputs"]["shellCast"]
    check("cast commits before manifestation and damage follows manifest", cast["startSeconds"] < cast["commitSeconds"] < cast["manifestationSeconds"] < event["timeSeconds"])
    check("damage event precedes original deadline", event["timeSeconds"] < cast["deadlineSeconds"])
    check("RP cost and first-family Dissonance values reconcile", cast["preCastRP"] - cast["rpCost"] == cast["postCastRP"] and cast["firstDistinctPreparedFamilyBaseDissonance"] == 0 and cast["postCastDissonance"] == 0)
    settle = p["ownerProposedInputs"]["expectedSettlementIfThesePremisesAreAdopted"]
    check("single 7-fire component is prevented without HP loss", event["damageType"] == "fire" and event["rawAmount"] == 7 and settle["shellPreventsOriginalFire"] == 7 and settle["HPDamage"] == 0 and settle["HPBefore"] == settle["HPAfter"])
    check("dealerless source emits no reflection recipient, packet, or nominal root", settle["reflectionRecipient"] is None and settle["reflectedPacketEmitted"] is False and settle["nominalOrBankedReflectionRootCreated"] is False)

    q = json.loads((REPO / "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_476_REPACK01.json").read_text(encoding="utf-8"))
    check("authority remains 831 applied / 17 pending / 0 accepted-unapplied", q["currentAuthority"] == {k: q["currentAuthority"][k] for k in ("reviewedApplied", "pending", "acceptedUnapplied", "completeStandaloneProcedures", "scopedInterfaces")} and q["currentAuthority"]["reviewedApplied"] == 831 and q["currentAuthority"]["pending"] == 17 and q["currentAuthority"]["acceptedUnapplied"] == 0)
    check("queue next identity and blockers remain Elemental Shell B01/B02", q["nextIdentity"] == "elemental-shell" and q["nextBlockerIds"] == ["DF218-B01", "DF218-B02"])
    boundary = p["decisionBoundary"]
    check("no adoption, actor, cast, event, encounter, witness, acceptance, canon, queue, or campaign effect", all(value is False for key, value in boundary.items() if key != "identityAcceptedOrApplied") and boundary["identityAcceptedOrApplied"] is False)

    manifest_paths = {item["path"]: item for item in m["files"]}
    expected_files = [PROPOSAL, PREFLIGHT, README]
    check("manifest binds exact proposal, geometry preflight, and README bytes", set(manifest_paths) == {x.name for x in expected_files} and all(manifest_paths[x.name]["bytes"] == x.stat().st_size and manifest_paths[x.name]["sha256"] == file_sha(x) for x in expected_files))
    with zipfile.ZipFile(ARCHIVE, "r") as archive:
        names = set(archive.namelist())
        check("ZIP has exactly proposal, preflight, README, and manifest", names == {x.name for x in [*expected_files, MANIFEST]})
        check("ZIP payload bytes match the packet files", all(archive.read(x.name) == x.read_bytes() for x in [*expected_files, MANIFEST]))
    check("delivery record binds archive and proposal", d["proposalSha256"] == file_sha(PROPOSAL) and d["archiveBytes"] == ARCHIVE.stat().st_size and d["archiveSha256"] == file_sha(ARCHIVE) and d["preflightSha256"] == file_sha(PREFLIGHT))
    check("independent validation binds all delivered artifacts", v["proposalSha256"] == file_sha(PROPOSAL) and v["preflightSha256"] == file_sha(PREFLIGHT) and v["archiveSha256"] == file_sha(ARCHIVE) and v["manifestSha256"] == file_sha(MANIFEST) and v["deliverySha256"] == file_sha(DELIVERY))
    check("proposal validation remains pre-adoption only", v["status"] == "PASS_PRE_ADOPTION_PREFLIGHT" and v["ownerAdoptionRecorded"] is False and v["witnessConstructed"] is False)

    result = {
        "id": "DF218-B01-TEST-SOURCE-PROPOSAL-478-INDEPENDENT-VALIDATION",
        "status": "PASS",
        "checksPassed": len(passed),
        "checksFailed": 0,
        "checks": passed,
        "sourceBindingsVerified": len(verified_bindings),
        "proposalSha256": file_sha(PROPOSAL),
        "preflightSha256": file_sha(PREFLIGHT),
        "archiveSha256": file_sha(ARCHIVE),
        "authority": p["currentAuthority"],
        "ownerAdoptionRecorded": False,
        "witnessConstructed": False,
    }
    VALIDATION.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
