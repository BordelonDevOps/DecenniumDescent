"""Count restore replay visits in a temporary source copy."""

import argparse
from pathlib import Path
import shutil


def replace_once(file, before, after):
    source = file.read_text(encoding="utf-8-sig")
    if source.count(before) != 1:
        raise ValueError(f"Expected one probe location in {file}: {before}")
    file.write_text(source.replace(before, after), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    shutil.copytree(args.source, args.destination)
    policy = args.destination / "TestOnlySharedWorldPolicy.cs"
    replace_once(policy, 'if (!ReplayReceipt(replay, receipt)) return "InvalidSharedWorldHistory";',
                 'if (!RestoreReplayProbe.VisitOuter() || !ReplayReceipt(replay, receipt)) return "InvalidSharedWorldHistory";')
    planning = args.destination / "SharedNextCharterPlan.cs"
    replace_once(planning, "var traversal = PendingPlanningCrossing(replay, terms);",
                 "RestoreReplayProbe.Nested++;\n                var traversal = PendingPlanningCrossing(replay, terms);")
    sealing = args.destination / "VerifiedSharedWorldCheckpoint.cs"
    replace_once(sealing, "var traversal = known.PendingCrossing(replay, nextCharterPlanProfile.Terms);",
                 "RestoreReplayProbe.Seal++;\n                    var traversal = known.PendingCrossing(replay, nextCharterPlanProfile.Terms);")
    (args.destination / "RestoreReplayProbe.cs").write_text(
        """namespace Decennium.Foundation.Laboratory
{
    public static class RestoreReplayProbe
    {
        public static int Outer, Nested, Seal;
        public static void Reset() { Outer = 0; Nested = 0; Seal = 0; }
        public static bool VisitOuter() { Outer++; return true; }
    }
}
""", encoding="utf-8")


if __name__ == "__main__":
    main()
