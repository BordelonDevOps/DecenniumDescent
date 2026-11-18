"""Read-only documentation/source-binding verification. No compilation or gameplay."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
BASE = "e7378d055f8bb354312e48de8fb0d70314f4d05d"

def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def check(condition, label):
    if not condition:
        raise AssertionError(label)
    checks.append(label)

checks = []
before = json.loads(git("show", BASE + ":docs/unity/IMPLEMENTATION_STATUS.json"))
after = read("docs/unity/IMPLEMENTATION_STATUS.json")
check(git("branch", "--show-current").decode().strip() == "Engine", "Engine branch")
check(before["workItems"] == after["workItems"], "All workstream fields, acceptance texts and evidence unchanged")
check(len(after["workItems"]) == 49, "49 original workstreams")
check(sum(len(x["dependencies"]) for x in after["workItems"]) == 120, "120 original direct edges")
check(sum(len(x["completionCriteria"]) for x in after["workItems"]) == 100, "100 original completion obligations")
for key in ["readiness", "completionContract", "activeImplementation", "frozenRuntime", "qualifiedConsoleHost", "priorAcceptedBaseline"]:
    check(before[key] == after[key], key + " unchanged")
for name in ["PRE_UNITY_COMPLETION_CONTRACT.md", "PRE_UNITY_COMPLETION_CONTRACT.json"]:
    check((ROOT / "docs/unity" / name).read_bytes() == git("show", BASE + ":docs/unity/" + name), name + " byte-identical")
check(not git("diff", BASE, "--name-only", "--", "engine").strip(), "No tracked engine changes from accepted baseline")
check(git("rev-parse", "HEAD:engine").decode().strip() == "6cce215d2ce46bebcfd15f69f61dc324545c23d7", "Accepted engine tree unchanged")
for name in ["DEVELOPMENT_HANDOFF.md", "IMPLEMENTATION_TRACE.md", "DEVELOPMENT_BRIEF.md"]:
    old = git("show", BASE + ":docs/unity/" + name)
    new = (ROOT / "docs/unity" / name).read_bytes()
    pos = old.index(b"\n") + 1
    check(new.startswith(old[:pos]) and new.endswith(old[pos:]), name + " historical body preserved byte-for-byte")

bindings = read("docs/unity/evidence/2026-11-17-next-module-contract/SOURCE_BINDINGS.json")["bindings"]
for binding in bindings:
    ref = binding["revision"] + ":" + binding["path"]
    data = git("show", ref)
    check(digest(data) == binding["sha256"] and len(data) == binding["bytes"], "Pinned source bytes: " + binding["path"])
    check(git("rev-parse", ref).decode().strip() == binding["gitBlob"], "Pinned Git blob: " + binding["path"])
    if "responseId" in binding:
        check(binding["responseId"].encode() in data, "Actual prerequisite response: " + binding["responseId"])
text = (PACKET / "MODULE_DEFINITION.md").read_text(encoding="utf-8")
check(len(set(re.findall(r"OMA-\d{2}", text))) == 10, "Ten named runtime acceptance criteria")
check(set(re.findall(r"CAL-\d{2}", text)) == {"CAL-01","CAL-02","CAL-03","CAL-04","CAL-05"}, "Five explicit open calendar decisions")
for target in re.findall(r"\]\(([^)]+)\)", text):
    if not target.startswith(("https:", "http:")):
        check((PACKET / target.split("#")[0]).is_file(), "Definition link exists: " + target)
n = after["nextModule"]
check(not n["implementationAuthorized"] and not n["runtimeAccepted"] and not n["sourceApiCalendarAmendmentAccepted"], "Definition/runtime/source-API authority separated")
check(n["profileId"] is None and not n["profileAvailabilityChecked"], "No successor profile reserved")
check(all(x["status"] == "OPEN" for x in n["preimplementationDecisions"]), "Calendar amendment remains open")
acceptance = json.loads((PACKET / "PLANNING_ACCEPTANCE.json").read_text())
if acceptance["definitionAccepted"]:
    check(n["status"] == "ACCEPTED_DEFINITION_CALENDAR_AMENDMENT_OPEN", "Accepted definition status matches")
    review = json.loads((PACKET / "GPT_PLANNING_REVIEW.json").read_text())
    message = [x for x in review["turn"]["items"] if x["type"] == "agentMessage" and x["id"] == acceptance["gptResponseId"]]
    check(len(message) == 1, "Actual GPT planning response retained")
    check(acceptance["definitionSha256"] == digest((PACKET / "MODULE_DEFINITION.md").read_bytes()), "Accepted definition SHA matches")
check(not acceptance["sourceApiCalendarAmendmentAccepted"] and not acceptance["runtimeAccepted"] and not acceptance["implementationAuthorized"], "No false implementation acceptance")
subprocess.run(["git", "-C", str(ROOT), "diff", "--check"], check=True)
check(True, "Tracked diff whitespace check")
print(json.dumps({
    "status": "PASS_DOCUMENTATION_CHECKS_ONLY",
    "checkedUtc": datetime.now(timezone.utc).isoformat(),
    "baseline": BASE, "branch": "Engine",
    "definitionSha256": digest((PACKET / "MODULE_DEFINITION.md").read_bytes()),
    "sourceBindingsSha256": digest((PACKET / "SOURCE_BINDINGS.json").read_bytes()),
    "checks": checks,
    "sourceBindings": len(bindings),
    "newCompilation": "NOT_RUN_DOCUMENTATION_ONLY",
    "newGameplayTests": "NOT_RUN_DOCUMENTATION_ONLY",
    "newBenchmarks": "NOT_RUN_DOCUMENTATION_ONLY",
    "scope": "Document consistency, retained source identities and unchanged accepted state; not semantic gameplay qualification."
}, indent=2))
