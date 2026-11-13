"""Compare every public field in the accepted and optimized console histories."""

import argparse
import hashlib
import json
from pathlib import Path


def read(path):
    payload = path.read_bytes()
    return hashlib.sha256(payload).hexdigest(), [
        json.loads(line) for line in payload.decode("utf-8-sig").splitlines()
    ]


def canonical(row):
    return json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("connected", type=Path)
    args = parser.parse_args()
    evidence = Path(__file__).resolve().parent.parent
    profiles = {}
    for profile, accepted in (("Default", "2026-11-12-int03-charter-performance/baseline/Default/responses.jsonl"),
                              ("FishingTrap", "2026-11-12-mgt06-connected-trap/connected/responses.jsonl")):
        reference = evidence / accepted
        actual = args.connected / profile / "responses.jsonl"
        expected_hash, expected = read(reference)
        actual_hash, actual_rows = read(actual)
        if len(expected) != len(actual_rows):
            raise ValueError(f"{profile}: transcript lengths differ.")
        for i, (before, after) in enumerate(zip(expected, actual_rows), 1):
            if canonical(before) != canonical(after):
                fields = sorted(key for key in set(before) | set(after)
                                if key not in before or key not in after or canonical(before[key]) != canonical(after[key]))
                raise ValueError(f"{profile}: response {i} differs in {fields}.")
        profiles[profile] = {"reference": str(reference.relative_to(evidence)).replace("\\", "/"),
                             "referenceSha256": expected_hash, "actualSha256": actual_hash,
                             "comparedRows": len(expected), "views": sum("Enabled" in row for row in expected)}
    report = {"Status": "PASS", "IgnoredFields": [], "Profiles": profiles}
    (args.connected / "transcript-equivalence.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
