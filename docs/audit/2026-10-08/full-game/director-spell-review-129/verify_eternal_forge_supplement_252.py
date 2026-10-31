from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
PACKET = ROOT / "ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_252.json"
AUDIT = ROOT / "ETERNAL_FORGE_MF210_B01_SUPPLEMENT_252_INDEPENDENT_AUDIT.json"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def decode_pointer(path):
    if path == "":
        return []
    if not path.startswith("/"):
        raise AssertionError("invalid JSON pointer: " + path)
    return [part.replace("~1", "/").replace("~0", "~") for part in path[1:].split("/")]


def parent_at(root, parts):
    current = root
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current, parts[-1] if parts else None


def get_at(root, parts):
    current = root
    for part in parts:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def apply_ops(state, operations):
    current = copy.deepcopy(state)
    for operation in operations:
        op = operation["op"]
        parts = decode_pointer(operation["path"])
        if op == "test":
            actual = get_at(current, parts)
            if actual != operation["value"]:
                raise AssertionError(f"test failed at {operation['path']}")
        elif op == "replace":
            parent, key = parent_at(current, parts)
            value = copy.deepcopy(operation["value"])
            if isinstance(parent, list):
                parent[int(key)] = value
            else:
                if key not in parent:
                    raise AssertionError(f"replace path missing at {operation['path']}")
                parent[key] = value
        elif op == "add":
            parent, key = parent_at(current, parts)
            value = copy.deepcopy(operation["value"])
            if isinstance(parent, list):
                parent.insert(int(key), value)
            else:
                if key in parent:
                    raise AssertionError(f"add path already exists at {operation['path']}")
                parent[key] = value
        elif op == "remove":
            parent, key = parent_at(current, parts)
            if isinstance(parent, list):
                del parent[int(key)]
            else:
                del parent[key]
        else:
            raise AssertionError(f"unsupported patch operation {op}")
    return current


def replay_events(state, events, label):
    current = copy.deepcopy(state)
    reverse_snapshots = []
    for event in events:
        if sha(current) != event["beforeSHA256"]:
            raise AssertionError(f"{label}/{event['id']}: before hash mismatch")
        reverse_snapshots.append(copy.deepcopy(current))
        current = apply_ops(current, event["forward"])
        if sha(current) != event["afterSHA256"]:
            raise AssertionError(f"{label}/{event['id']}: after hash mismatch")
    for event, expected_before in zip(reversed(events), reversed(reverse_snapshots)):
        if sha(current) != event["afterSHA256"]:
            raise AssertionError(f"{label}/{event['id']}: inverse starts at wrong state")
        current = apply_ops(current, event["inverse"])
        if sha(current) != sha(expected_before):
            raise AssertionError(f"{label}/{event['id']}: inverse did not restore exact prior state")
    return current


def check(condition, message):
    if not condition:
        raise AssertionError(message)


packet_bytes = PACKET.read_bytes()
packet = json.loads(packet_bytes)
source_state = packet["priorCase"]["endState"]
check(sha(source_state) == packet["priorCase"]["endSnapshotSHA256"], "MF210-F01 source snapshot hash")
check(sha(source_state) == packet["eventReplay"]["baseStateSHA256"], "replay base hash")

common_events = packet["eventReplay"]["commonEvents"]
common_state = copy.deepcopy(source_state)
for event in common_events:
    check(sha(common_state) == event["beforeSHA256"], f"{event['id']} before state")
    common_state = apply_ops(common_state, event["forward"])
    check(sha(common_state) == event["afterSHA256"], f"{event['id']} after state")
check(sha(common_state) == packet["eventReplay"]["commonForkStateSHA256"], "common branch fork hash")
check(replay_events(source_state, common_events, "common") == source_state, "common inverse round trip")

case_by_id = {case["id"]: case for case in packet["witnessCases"]}
branch_summaries = []
event_total = len(common_events)
for branch in packet["eventReplay"]["branches"]:
    check(branch["baseStateSHA256"] == sha(common_state), f"{branch['id']} common fork")
    current = copy.deepcopy(common_state)
    events = branch["events"]
    event_total += len(events)
    for event in events:
        check(sha(current) == event["beforeSHA256"], f"{branch['id']}/{event['id']} before hash")
        current = apply_ops(current, event["forward"])
        check(sha(current) == event["afterSHA256"], f"{branch['id']}/{event['id']} after hash")
    check(sha(current) == branch["finalStateSHA256"], f"{branch['id']} final hash")
    final = branch["expectedFinal"]
    item = current["items"]["sword-1"]
    check(current["time"] == final["timeSeconds"], f"{branch['id']} final time")
    check(current["supplement"]["actorBalanceCp"] == final["actorBalanceCp"], f"{branch['id']} funds")
    check(item["HP"] == final["item"]["HP"], f"{branch['id']} item HP")
    check(item["owner"] == "A" and item["custodian"] == "WH250-01-workbench", f"{branch['id']} item ownership/custody")
    check(item["id"] == "sword-1" and item["recipe"] == "recipe-42", f"{branch['id']} item identity")
    check(item["provenance"] == ["castF1"] and item["imprintRoot"]["id"] == "castF1", f"{branch['id']} lineage")
    check(item["imprintRoot"]["active"] is True and item["imprintRoot"]["suppressed"] is False, f"{branch['id']} cast root status")
    check(item["imprintOperational"] is (item["HP"] > 0), f"{branch['id']} broken/root operation")
    check(item["mainBodyRecoverable"] is True, f"{branch['id']} main body retention")
    check(current["actors"]["A"]["HP"] == 104 and current["actors"]["B"]["HP"] == 98, f"{branch['id']} retained A/B HP")
    check(current["actors"]["B"]["maxHP"] == 104, f"{branch['id']} retained B max HP")
    check(current["actors"]["A"]["positionFeet"] == [0, 0, 0] and current["actors"]["B"]["positionFeet"] == [5, 0, 0], f"{branch['id']} no relocation")
    check(current["terminalCasts"]["castF1"]["status"] == "resolved", f"{branch['id']} source cast")
    check(current["supplement"]["initiativeStatus"].startswith("ended-at-12.3"), f"{branch['id']} initiative exit")
    check(current["actors"]["MF250-DWARF-WARRIOR1"]["carriedItems"]["adventuring-gear.acid-vial"]["quantity"] == 0, f"{branch['id']} vial consumption")
    check(current["actors"]["MF250-DWARF-WARRIOR1"]["carriedWeightLb"] == 8, f"{branch['id']} post-use carried weight")
    check(current["supplement"]["emptyVialDisposition"]["custodian"] == "WH250-01-empty-vial-bin", f"{branch['id']} empty vial custody")
    expected_structure = "functional" if item["HP"] == item["maxHP"] else "functional-damaged" if item["HP"] > 0 else "Broken"
    check(item["structuralState"] == expected_structure, f"{branch['id']} structural state follows HP")
    check(current["supplement"]["worksite"]["accessFeeCp"] == 0, f"{branch['id']} no unrecorded fee")
    check(current["supplement"]["worksite"]["availableThroughSeconds"] >= current["time"], f"{branch['id']} station interval")
    check(current["supplement"]["actorBalanceCp"] == current["actors"]["MF250-DWARF-WARRIOR1"]["balanceCp"], f"{branch['id']} duplicated cash ledgers")
    check(len(current["supplement"]["repairChecks"]) == len(case_by_id[branch["id"]]["materialLots"]), f"{branch['id']} check count")
    expected_cost = sum(
        375 if lot.endswith(("01", "02A", "02B")) else 2675
        for lot in case_by_id[branch["id"]]["materialLots"]
    )
    check(3500 - expected_cost == current["supplement"]["actorBalanceCp"], f"{branch['id']} source price arithmetic")
    used_lots = {tx["lotId"] for tx in current["supplement"]["branchTransactions"]}
    check(used_lots == set(case_by_id[branch["id"]]["materialLots"]), f"{branch['id']} actual lot usage")
    check(all(tx["sellerReceiptCp"] == tx["priceCp"] for tx in current["supplement"]["branchTransactions"]), f"{branch['id']} seller payment")
    check(all(tx["actorFundsBeforeCp"] - tx["actorFundsAfterCp"] == tx["priceCp"] for tx in current["supplement"]["branchTransactions"]), f"{branch['id']} buyer ledger")
    check(sum(tx["changeReturnedCp"] for tx in current["supplement"]["branchTransactions"]) <= 125, f"{branch['id']} finite change")
    for lot in current["supplement"]["worksite"]["materialLots"]:
        if lot["lotId"] in used_lots:
            check(lot["status"] == "consumed" and lot["owner"] == "MF250-DWARF-WARRIOR1", f"{branch['id']} lot custody/consumption")
        else:
            check(lot["status"] == "available" and lot["owner"] == "WH250-01-OPERATOR", f"{branch['id']} unused finite stock")
    # Reverse this branch independently and prove it returns to the common fork.
    reverse = copy.deepcopy(current)
    for event in reversed(events):
        check(sha(reverse) == event["afterSHA256"], f"{branch['id']}/{event['id']} inverse start")
        reverse = apply_ops(reverse, event["inverse"])
        check(sha(reverse) == event["beforeSHA256"], f"{branch['id']}/{event['id']} inverse result")
    check(sha(reverse) == sha(common_state), f"{branch['id']} inverse branch fork")
    branch_summaries.append({
        "branch": branch["id"], "events": len(events), "finalTimeSeconds": current["time"],
        "finalSwordHP": item["HP"], "balanceCp": current["supplement"]["actorBalanceCp"],
        "repairChecks": len(current["supplement"]["repairChecks"]), "usedLots": sorted(used_lots),
        "forwardPass": True, "inversePass": True,
    })

# Character and authority boundary checks.
review_actor = packet["repairActor"]
check(review_actor["pointsSpent"] == 23, "point buy cost")
check(review_actor["finalAbilityScores"] == {"STR": 12, "DEX": 14, "CON": 14, "INT": 13, "WIS": 12, "CHA": 9}, "final ability scores")
check(review_actor["classSkillSelection"]["selectedSkills"] == ["Intimidation", "Survival"], "selected class skills")
check(set(review_actor["classSkillSelection"]["selectedSkills"]).issubset(set(review_actor["classSkillSelection"]["candidateSkills"])), "class skills are in bound Warrior list")
check(not set(review_actor["classSkillSelection"]["selectedSkills"]) & {"Athletics", "Insight"}, "no duplicate background skill")
check(review_actor["startingWealth"]["totalGp"] == 80, "Warrior starting wealth")
serum_choice = review_actor["serumLoadout"]["preparedDoses"][0]
check(serum_choice["id"] == "warrior.supplement.overdrive" and serum_choice["chosenAbility"] in {"STR", "DEX"}, "Overdrive preparation-time ability choice")
common_actor = common_state["actors"]["MF250-DWARF-WARRIOR1"]["classResources"]["preparedSerums"][0]
check(common_actor["id"] == serum_choice["id"] and common_actor["chosenAbility"] == serum_choice["chosenAbility"], "Overdrive preparation choice mirrors replay profile")
check(review_actor["classLevel"] == 1 and review_actor["proficiencyBonus"] == 2 and review_actor["hp"] == 14, "Warrior level 1 derived stats")
check(packet["authority"] == {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0}, "authority count")
check(packet["acceptedIds"] == [] and packet["appliedIds"] == [], "no acceptance/application")
check(packet["canonicalChanges"] is False and packet["applicationChanges"] is False and packet["githubChanges"] is False, "no promoted/canonical change")

binding_results = []
for binding in packet["sourceBindings"]:
    path = pathlib.Path(binding["path"])
    if not path.exists():
        binding_results.append({"path": binding["path"], "exists": False})
        continue
    raw = path.read_bytes()
    binding_results.append({
        "path": binding["path"], "exists": True,
        "bytesMatch": len(raw) == binding["bytes"],
        "sha256Match": hashlib.sha256(raw).hexdigest() == binding["sha256"],
    })
check(all(item.get("exists") and item.get("bytesMatch") and item.get("sha256Match") for item in binding_results), "all source bindings match current files")

check(event_total == packet["eventReplay"]["eventCount"], "event count")
result = {
    "auditId": "ETERNAL-FORGE-MF210-B01-SUPPLEMENT-252-INDEPENDENT-CONSISTENCY-AUDIT",
    "status": "PASS_LOCAL_FORWARD_INVERSE_AND_TRANSACTION_CONSISTENCY; NOT_DIRECTOR_ACCEPTANCE",
    "packet": PACKET.name,
    "packetBytes": len(packet_bytes),
    "packetSha256": hashlib.sha256(packet_bytes).hexdigest(),
    "sourceBaseStateSha256": sha(source_state),
    "branchForkStateSha256": sha(common_state),
    "commonEvents": len(common_events),
    "totalEventApplicationsAcrossAlternativeBranches": event_total,
    "branchResults": branch_summaries,
    "sourceBindings": binding_results,
    "checks": [
        "All common and branch event before/after hashes matched.",
        "Every forward patch applied, and each inverse restored the exact branch predecessor/fork.",
        "All five alternatives retain sword-1, owner A, recipe-42, castF1, and B's 98/104 HP state.",
        "Acid attack outcomes, correct structural state, vial/container custody and carried weight, repair/reconstruction checks, material consumption, cash, finite change and clocks reconcile.",
        "Warrior point-buy, skills, wealth, HP, proficiency, Overdrive preparation choice and pending/accepted/apply authority reconcile.",
    ],
    "limitations": [
        "This is a local mechanical consistency audit, not an independent rules adjudication or GPT decision.",
        "W1 remains pending director acceptance; separate MF247-F-W2 and all other held identities remain open.",
    ],
}
AUDIT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
