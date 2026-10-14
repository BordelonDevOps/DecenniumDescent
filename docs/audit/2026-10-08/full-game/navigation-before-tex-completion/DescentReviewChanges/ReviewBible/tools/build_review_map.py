"""Build a read-only, offline navigation snapshot without changing game sources."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote, unquote, urlsplit
import hashlib
import json

G = Path(__file__).resolve().parents[3]
R = G / "DescentReviewChanges/ReviewBible"
A = G / "docs/audit/2026-10-08/full-game"
LEDGER = R / "data/playtest/game_development_coverage.json"
TEMPLATE = Path(__file__).with_name("review_map_template.html")
OUT = G / "REVIEW_MAP.html"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def group(number):
    if number in [0, 1, 4, 5, 6, 7, 8, 9, 10]:
        return "Game and characters"
    if 11 <= number <= 14:
        return "Magic and feats"
    if number in [2, 3] or 15 <= number <= 24:
        return "Checks and combat"
    if number <= 32:
        return "Equipment and crafting"
    if number <= 38:
        return "Creatures and encounters"
    if number <= 46:
        return "Expeditions and society"
    if number <= 52:
        return "World and cosmology"
    if number <= 57:
        return "Director procedures"
    if number <= 62:
        return "Teaching and reference"
    return "Software and delivery"


def main():
    ledger = read(LEDGER)
    frozen = read(A / "TEACHING_NAVIGATION_EXACT_V1_PREPARATION.json")["manifest"]
    unchanged = []
    for rel, expected in frozen.items():
        p = G / rel
        if rel == "README_TEACHING_EXACT_V1.md":
            assert not p.exists(), "Expected archive-only README"
            continue
        assert p.is_file() and digest(p) == expected["sha256"], rel
        unchanged.append(rel)
    assert len(unchanged) == 217
    areas = ledger["aspects"]
    assert len(areas) == 75 and len({x["id"] for x in areas}) == 75
    missing, links = [], set()

    def ref(rel):
        parts = urlsplit(rel)
        assert not parts.scheme and not parts.netloc, rel
        path = (G / unquote(parts.path)).resolve()
        assert path.is_relative_to(G.resolve()), rel
        exists = path.is_file() or path.is_dir()
        (links if exists else set()).add(rel)
        if not exists:
            missing.append(rel)
        return {"path": rel, "label": path.name + ("/" if path.is_dir() else ""), "url": quote(parts.path, safe="/") + ("/" if path.is_dir() else "") + ("#" + quote(parts.fragment) if parts.fragment else ""), "exists": exists}

    result = []
    fields = ["draftEvidence", "sourceEvidence", "reviewEvidence", "validationEvidence", "humanEvidence"]
    for area in areas:
        entry = {k: area.get(k, [] if k in ["completedScopes", "openIssues"] else "") for k in ["id", "number", "domain", "requiredCoverage", "acceptanceGate", "status", "closure", "completionClass", "completedScopes", "openIssues"]}
        entry["group"] = group(area["number"])
        entry["references"] = {key: [ref(p) for p in area.get(key, [])] for key in fields}
        result.append(entry)

    featured = [
        ("Start here", "START_HERE.md"),
        ("First Bard character", "DescentReviewChanges/ReviewBible/docs/playtest/FIRST_BARD_WALKTHROUGH.md"),
        ("All 17 class families", "DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_INDEX.md"),
        ("Paladin Oaths and Oathbreakers", "DescentReviewChanges/ReviewBible/docs/mechanics/PALADIN_OATHS_AND_OATHBREAKERS.md"),
        ("Reviewed spell index", "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"),
        ("Reviewed recipe index", "DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md"),
        ("Character sheet, awaiting teaching verdict", "DescentReviewChanges/ReviewBible/output/pdf/Decennium_Descent_Character_Sheet_Playtest.pdf"),
        ("Source authority", "docs/canon/CANON_MANIFEST.json"),
        ("Current notebook handoff", "docs/audit/2026-10-08/full-game/GPT_REVIEW_CONTINUATION_HANDOFF.md"),
    ]
    featured = [{**ref(p), "label": label} for label, p in featured]
    pending = [
        ("Teaching review submission", "TEACHING_NAVIGATION_EXACT_V1_SUBMISSION.json"),
        ("Social and faction source questions", "SOCIAL_FACTION_SOURCE_AUDIT.md"),
        ("Reputation preservation findings", "REPUTATION_PRESERVATION_SOURCE_ADDENDUM.md"),
        ("Joint flow and GitHub delivery", "FINAL_FLOW_AND_GITHUB_DELIVERY.md"),
    ]
    pending = [{**ref("docs/audit/2026-10-08/full-game/" + p), "label": label} for label, p in pending]
    data = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "ledgerSha256": digest(LEDGER),
        "areas": result,
        "featured": featured,
        "pending": pending,
        "ledger": ref(LEDGER.relative_to(G).as_posix()),
        "counts": {"aspects": len(result), "closed": sum(a["closure"] == "closed" for a in result), "spellsReviewed": ledger["activeLowRankSpellReview"]["ordinaryOperational"], "spellsPending": ledger["activeLowRankSpellReview"]["ordinaryPending"]},
    }
    assert not missing, "Unresolved ledger paths: " + repr(sorted(set(missing)))
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = TEMPLATE.read_text(encoding="utf-8")
    assert template.count("__REVIEW_DATA__") == 1
    OUT.write_text(template.replace("__REVIEW_DATA__", payload), encoding="utf-8", newline="\n")
    for rel in unchanged:
        assert digest(G / rel) == frozen[rel]["sha256"], rel
    receipt = {"generatedAtUtc": data["generatedAtUtc"], "artifact": OUT.relative_to(G).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT), "ledgerSha256": data["ledgerSha256"], "areas": len(result), "existingDistinctLinks": len(links), "missingLinks": missing, "unchangedLiveSubmissionFiles": len(unchanged), "purpose": "Offline owner navigation snapshot; no rule, approval, ledger, source, archive or save changes", "notebookReview": "Submitted teaching review; final verdict not yet recorded"}
    (A / "REVIEW_MAP_BUILD.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
