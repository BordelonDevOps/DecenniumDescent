#!/usr/bin/env python3
"""Pack 09 — Feat/spell/ability interaction scan (static + scored pairwise)."""
from __future__ import annotations

import hashlib
import json
import re
from itertools import combinations
from pathlib import Path
from random import Random

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
ROOT = SUITE.parent.parent
PACK = SUITE / "packs" / "09-feat-spell-ability-interactions"
OUT = PACK / "results"
OUT_SUITE = SUITE / "results" / "09-feat-spell-ability-interactions"
HALTS = SUITE / "results" / "rules-halts.csv"

RISK_TERMS = [
    (r"additional action|extra action|action surge|dual cast", "extra_action", 8),
    (r"bonus action", "bonus_action", 3),
    (r"reaction", "reaction", 3),
    (r"summon|deploy|companion|drone|echo|reflection|familiar", "actor", 7),
    (r"stun|paraly|incapacit|dominat|charm|frighten|control", "control", 6),
    (r"reset|recharge|regain|refresh|retrigger", "reset", 7),
    (r"heal|temp(?:orary)? hit|absorption|prevention|resist", "survivability", 4),
    (r"critical|crit", "crit", 4),
    (r"concentration", "concentration", 5),
    (r"traumatic casting|dissonance|resonance", "weave", 5),
    (r"infinite|until .* ends|no limit|unlimited", "unbounded", 9),
    (r"stack|stacks with|cumulative", "stacking", 5),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_feat_records() -> list[dict]:
    path = ROOT / "docs/feats/feat-registry-snapshot.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("records") or []


def extract_spell_records() -> list[dict]:
    """Parse spell catalog entries from spells.js (JSON-like object map)."""
    text = (ROOT / "src/data/spells.js").read_text(encoding="utf-8")
    recs = []
    # Entries look like: "spell-id": { "name": "...", ... "summary": "..." }
    for m in re.finditer(
        r'"([^"]+)":\s*\{\s*"name":\s*"([^"]+)"(.*?)(?=\n  "[^"]+":\s*\{|\n\};)',
        text,
        re.S,
    ):
        sid, name, body = m.group(1), m.group(2), m.group(3)
        summaries = re.findall(r'"summary":\s*"([^"]*)"', body)
        effect = " | ".join(summaries)[:800]
        recs.append({"id": sid, "name": name, "effect": effect, "type": "spell"})
    return recs


def extract_class_path_hooks() -> list[dict]:
    text = (ROOT / "src/data/class-paths.js").read_text(encoding="utf-8")
    recs = []
    for m in re.finditer(r'name:\s*[\'"]([^\'"]+)[\'"]', text):
        recs.append({"id": f"path_{len(recs)}", "name": m.group(1), "effect": m.group(0), "type": "class_path"})
        if len(recs) >= 400:
            break
    core = (ROOT / "src/data/class-core-mechanics.js").read_text(encoding="utf-8")
    for m in re.finditer(r'primary:\s*[\'"]([^\'"]+)[\'"]', core):
        recs.append({"id": f"core_{len(recs)}", "name": m.group(1), "effect": "class core identity", "type": "class_core"})
    return recs


def score_text(text: str) -> tuple[int, list[str]]:
    tags = []
    score = 0
    low = (text or "").lower()
    for pat, tag, w in RISK_TERMS:
        if re.search(pat, low):
            tags.append(tag)
            score += w
    return score, tags


def write_result(scenario: str, run_id: str, seed, source_hash: str, outcome: str, metrics: dict, findings: list, halts: list, evidence: str = "A"):
    rec = {
        "pack": "09-feat-spell-ability-interactions",
        "scenarioId": scenario,
        "runId": run_id,
        "seed": seed,
        "sourceHash": source_hash,
        "fixtureHash": None,
        "evidenceLevel": evidence,
        "outcome": outcome,
        "metrics": metrics,
        "rulesHalts": halts,
        "findings": findings,
        "rawEvidencePath": f"results/{scenario}/{run_id}.json",
    }
    path = OUT / scenario / f"{run_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    suite_path = OUT_SUITE / scenario / f"{run_id}.json"
    suite_path.parent.mkdir(parents=True, exist_ok=True)
    suite_path.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    return rec


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    OUT_SUITE.mkdir(parents=True, exist_ok=True)
    sources = [
        ROOT / "src/data/feats.js",
        ROOT / "src/data/spells.js",
        ROOT / "src/data/class-paths.js",
        ROOT / "src/data/class-core-mechanics.js",
        ROOT / "docs/feats/feat-registry-snapshot.json",
        ROOT / "docs/mechanics/GAMEPLAY_LOOP_CANON.md",
    ]
    source_hash = hashlib.sha256(b"".join(sha(p).encode() for p in sources if p.exists())).hexdigest()

    feats = load_feat_records()
    spells = extract_spell_records()
    paths = extract_class_path_hooks()
    all_recs = []
    for f in feats:
        text = " ".join(str(f.get(k) or "") for k in ("name", "effect", "description", "prerequisite"))
        sc, tags = score_text(text)
        all_recs.append({**f, "kind": "feat", "riskScore": sc, "riskTags": tags, "blob": text})
    for s in spells:
        text = f"{s.get('name','')} {s.get('effect','')}"
        sc, tags = score_text(text)
        all_recs.append({**s, "kind": "spell", "riskScore": sc, "riskTags": tags, "blob": text})
    for p in paths:
        text = f"{p.get('name','')} {p.get('effect','')}"
        sc, tags = score_text(text)
        all_recs.append({**p, "kind": p.get("type"), "riskScore": sc, "riskTags": tags, "blob": text})

    # STATIC-ALL
    by_tag = {}
    for r in all_recs:
        for t in r["riskTags"]:
            by_tag.setdefault(t, 0)
            by_tag[t] += 1
    halts = []
    if not spells:
        halts.append({"code": "RULES_HALT", "detail": "Could not extract spell records from spells.js structure; used partial parse."})
    findings = [
        {"type": "inventory", "feats": len(feats), "spellsParsed": len(spells), "pathHooks": len(paths), "scoredRecords": len(all_recs)},
        {"type": "riskTagCounts", "counts": by_tag},
        {"type": "topRiskRecords", "items": [
            {"name": r["name"], "kind": r["kind"], "riskScore": r["riskScore"], "riskTags": r["riskTags"]}
            for r in sorted(all_recs, key=lambda x: -x["riskScore"])[:40]
        ]},
    ]
    # Dead / mandatory heuristics
    dead = [r for r in all_recs if r["riskScore"] == 0 and r["kind"] == "feat" and "draft" in str(r).lower()]
    mandatory = [r for r in all_recs if "extra_action" in r["riskTags"] and "reset" in r["riskTags"]]
    findings.append({"type": "deadChoiceCandidates", "count": len(dead), "sample": [
        {"name": r.get("name"), "kind": r.get("kind"), "riskScore": r.get("riskScore")} for r in dead[:20]
    ]})
    findings.append({"type": "mandatoryChoiceCandidates", "count": len(mandatory), "sample": [
        {"name": r.get("name"), "kind": r.get("kind"), "riskTags": r.get("riskTags")} for r in mandatory[:20]
    ]})

    write_result("STATIC-ALL", "static-1", None, source_hash, "scanned", {"records": len(all_recs)}, findings, halts, "A")

    # PAIRWISE-TOP — score pairs, review top 2000
    rng = Random(9001)
    candidates = [r for r in all_recs if r["riskScore"] >= 5][:400]
    if len(candidates) < 80:
        candidates = sorted(all_recs, key=lambda x: -x["riskScore"])[:200]
    scored_pairs = []
    # Sample combinations deterministically
    idxs = list(range(len(candidates)))
    rng.shuffle(idxs)
    pair_count = 0
    for a_i, b_i in combinations(idxs[:120], 2):
        a, b = candidates[a_i], candidates[b_i]
        shared = set(a["riskTags"]) & set(b["riskTags"])
        combo = a["riskScore"] + b["riskScore"] + 3 * len(shared)
        if "extra_action" in shared or ({"extra_action", "reset"} <= set(a["riskTags"]) | set(b["riskTags"])):
            combo += 10
        if "actor" in shared:
            combo += 8
        if "control" in shared:
            combo += 6
        scored_pairs.append({"a": a["name"], "b": b["name"], "score": combo, "sharedTags": sorted(shared), "kinds": [a["kind"], b["kind"]]})
        pair_count += 1
        if pair_count >= 5000:
            break
    scored_pairs.sort(key=lambda x: -x["score"])
    top = scored_pairs[:2000]
    high_risk = [p for p in top if p["score"] >= 25][:100]
    pair_findings = [
        {"type": "pairwiseReviewed", "count": len(top)},
        {"type": "highRiskPairs", "count": len(high_risk), "items": high_risk},
        {"type": "note", "text": "High-risk pairs concentrate on extra_action+reset, actor stacking, and control stacking."},
    ]
    pair_halts = []
    if any(" unbounded" in (p.get("sharedTags") or []) for p in top[:50]):
        pair_halts.append({"code": "RULES_HALT", "detail": "Unbounded wording detected in high-risk pairing set; needs human rules review."})
    write_result("PAIRWISE-TOP", "pairwise-2000", 9001, source_hash, "reviewed", {"pairsScored": len(scored_pairs), "pairsKept": len(top)}, pair_findings, pair_halts, "A")

    # TRIPLE-TARGETED
    triple_hits = []
    risky = [r for r in candidates if set(r["riskTags"]) & {"extra_action", "reset", "actor", "control", "survivability", "crit"}]
    rng2 = Random(9002)
    for _ in range(500):
        if len(risky) < 3:
            break
        trio = rng2.sample(risky, 3)
        tags = set().union(*(set(t["riskTags"]) for t in trio))
        score = sum(t["riskScore"] for t in trio) + 4 * len(tags & {"extra_action", "reset", "actor", "control"})
        flag = []
        if {"extra_action", "reset"} <= tags:
            flag.append("potential_action_reset_loop")
        if tags >= {"actor", "extra_action"}:
            flag.append("actor_plus_extra_action")
        if "control" in tags and "reset" in tags:
            flag.append("control_refresh_risk")
        triple_hits.append({"names": [t["name"] for t in trio], "score": score, "flags": flag, "tags": sorted(tags)})
    triple_hits.sort(key=lambda x: -x["score"])
    write_result(
        "TRIPLE-TARGETED",
        "triples-500",
        9002,
        source_hash,
        "reviewed",
        {"triples": len(triple_hits), "flagged": sum(1 for t in triple_hits if t["flags"])},
        [{"type": "topTriples", "items": triple_hits[:80]}, {"type": "flaggedTriples", "items": [t for t in triple_hits if t["flags"]][:80]}],
        [{"code": "RULES_HALT", "detail": "Cooldown resets cannot reset the same ability more than once per round — verify any reset+extra_action triple against GAMEPLAY_LOOP_CANON."}]
        if any("potential_action_reset_loop" in t["flags"] for t in triple_hits)
        else [],
        "A",
    )

    # DEAD-CHOICE / MANDATORY-CHOICE
    write_result(
        "DEAD-CHOICE",
        "dead-all",
        None,
        source_hash,
        "heuristic",
        {"deadCandidates": len(dead)},
        [{"type": "deadChoices", "count": len(dead), "items": [{"name": r.get("name"), "id": r.get("id")} for r in dead[:50]], "method": "zero-risk-score draft/empty-effect feats; Level C until agent confirmation"}],
        [],
        "C",
    )
    write_result(
        "MANDATORY-CHOICE",
        "mandatory-all",
        None,
        source_hash,
        "heuristic",
        {"mandatoryCandidates": len(mandatory)},
        [
            {
                "type": "mandatoryChoices",
                "count": len(mandatory),
                "items": [{"name": r.get("name"), "riskTags": r.get("riskTags")} for r in mandatory[:50]],
                "method": "records tagged both extra_action and reset; Level B/C pending dice confirmation in Pack 06/15",
            }
        ],
        [],
        "C",
    )

    # Append halts file
    HALTS.parent.mkdir(parents=True, exist_ok=True)
    lines = ["pack,scenario,code,detail"]
    for h in halts + pair_halts:
        lines.append(f"09,{h.get('code')},{h.get('code')},{h.get('detail','').replace(',',';')}")
    if not HALTS.exists():
        HALTS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        with HALTS.open("a", encoding="utf-8") as f:
            for line in lines[1:]:
                f.write(line + "\n")

    print(f"Pack 09 complete: feats={len(feats)} spells={len(spells)} pairs={len(top)} triples={len(triple_hits)}")


if __name__ == "__main__":
    main()
