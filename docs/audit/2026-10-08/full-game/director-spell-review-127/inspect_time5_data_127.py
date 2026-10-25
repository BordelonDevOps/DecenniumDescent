"""Fresh independent serialized-data inspector; never executes delivered code or gameplay."""
import json
import math
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
casebook = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
findings = []
counts = dict(cases=0, events=0, states=0, casts=0, damageRecords=0)


def issue(case, where, check, actual=None, expected=None):
    findings.append(dict(case=case, where=where, check=check, actual=actual, expected=expected))


def inspect(case):
    cid = case["id"]
    counts["cases"] += 1
    timeline = case.get("timeline", [])
    prev = case.get("initial")
    for n, event in enumerate(timeline):
        counts["events"] += 1
        where = f"timeline/{n}"
        if prev != event["before"]:
            issue(cid, where, "full-value chain mismatch")
        prev = event["after"]
        if event["time"] != prev["time"] or event["before"]["time"] > event["time"]:
            issue(cid, where, "event clock mismatch")
        for state_name in ("before", "after"):
            state = event[state_name]
            counts["states"] += 1
            for aid, actor in state["actors"].items():
                at = f"{where}/{state_name}/actors/{aid}"
                for value, cap in (("hp", "effectiveMaxHp"), ("rp", "maxRp")):
                    if not 0 <= actor[value] <= actor[cap]:
                        issue(cid, at, value + " outside actual cap", actor[value], actor[cap])
                if actor["tempHp"] < 0 or actor["dissonance"] < 0 or not 0 <= actor["wounds"] <= 3:
                    issue(cid, at, "invalid resource/life scalar")
                if (actor["life"] == "dead") == actor["alive"]:
                    issue(cid, at, "alive/life disagree")
                schedule = actor.get("schedule", {})
                if all(k in schedule for k in ("regularStart", "regularEnd", "turnActive")):
                    active = schedule["regularStart"] <= state["time"] < schedule["regularEnd"]
                    if active != schedule["turnActive"]:
                        issue(cid, at, "stored turnActive differs from exact phase", schedule["turnActive"], active)
        obs = event.get("observations", {})
        cast = obs.get("commitment")
        if cast:
            counts["casts"] += 1
            a = event["before"]["actors"][cast["caster"]]
            family = {"class-counter": "wizard.base.counterspell", "arcane-bolt": "wizard.base.arcane-bolt"}.get(cast["spellId"], cast["spellId"])
            base = 0 if cast["rank"] == 0 or family not in a["preparedFamiliesUsed"] else (1 if cast["rank"] <= 5 else 2)
            if cast["baseDissonance"] != base:
                issue(cid, where, "Wizard native repeated-family base Dissonance", cast["baseDissonance"], base)
            refrain = min(3, a["refrain"] + 1) if a["lastSpell"] == family else 0
            if cast["refrainIncrement"] != refrain:
                issue(cid, where, "native Refrain increment", cast["refrainIncrement"], refrain)
            if cast["rpBefore"] - cast["actualPaidRP"] != cast["rpAfter"]:
                issue(cid, where, "paid RP arithmetic")
            if cast["hpBefore"] - cast["hpCost"] != cast["hpAfter"]:
                issue(cid, where, "HP cost arithmetic")
            template = case.get("actorDefinitions", {}).get(cast["caster"], {})
            limit = template.get("limit")
            if limit is not None:
                before_d = a["dissonance"]
                surcharge = 3 if before_d >= limit + 6 else 2 if before_d >= limit + 3 else 1 if before_d >= limit else 0
                if cast["surcharge"] != surcharge:
                    issue(cid, where, "ranked cast strain surcharge (verify same-event phase effects)", cast["surcharge"], surcharge)
        for damage in obs.get("damage", []):
            counts["damageRecords"] += 1
            raw = sum(damage.get("dice", [])) + damage.get("flat", 0)
            if raw != damage["raw"]:
                issue(cid, where, "damage raw arithmetic", damage["raw"], raw)
            if "postTemp" in damage:
                if damage["resolved"] - damage["tempAbsorbed"] != damage["postTemp"]:
                    issue(cid, where, "post-temp arithmetic")
                if damage["hpBefore"] - damage["normalHpLost"] != damage["hpAfter"]:
                    issue(cid, where, "normal HP damage arithmetic")
                if damage["postTemp"] - damage["normalHpLost"] != damage["overkill"]:
                    issue(cid, where, "overkill arithmetic")
    if prev != case.get("final"):
        issue(cid, "final", "final state differs from final event")
    for branch in case.get("branches", []):
        inspect(branch)


for item in casebook["cases"]:
    inspect(item)
result = dict(scope="Independent static data inspection, not runtime or acceptance; findings require current final-data semantic review.", counts=counts, findings=findings)
if len(sys.argv) > 2:
    pathlib.Path(sys.argv[2]).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
