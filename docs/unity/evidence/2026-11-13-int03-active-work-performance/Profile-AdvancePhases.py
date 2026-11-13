"""Build a temporary diagnostic LabModel copy with phase counters; leave engine source intact."""

import argparse
from pathlib import Path
import shutil


def replace_once(path, old, new):
    source = path.read_text(encoding="utf-8-sig")
    if source.count(old) != 1:
        raise ValueError(f"Expected one diagnostic hook in {path}: {old}")
    path.write_text(source.replace(old, new), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    model = args.destination
    shutil.copytree(args.model, model)
    scheduler = model / "TestOnlySharedWorldPolicy.cs"
    replace_once(scheduler, "while (s.RuleClock < target) {",
                 'while (s.RuleClock < target) {\n                using var segmentProbe = AdvancePhaseProbe.Enter("segment");\n'
                 '                using var selectionProbe = AdvancePhaseProbe.Enter("selection");')
    replace_once(scheduler, "var observationSegments = new System.Collections.Generic.List<ObservationMovementSegment>();",
                 'selectionProbe.Dispose();\n                using var movementProbe = AdvancePhaseProbe.Enter("movement");\n'
                 '                var observationSegments = new System.Collections.Generic.List<ObservationMovementSegment>();')
    replace_once(scheduler, "if(connectedCombat==null) {\n                    if(harvestFixture",
                 'movementProbe.Dispose();\n                using var workProbe = AdvancePhaseProbe.Enter("inventory-and-work");\n'
                 '                if(connectedCombat==null) {\n                    if(harvestFixture')
    replace_once(scheduler, "string deferredActivityActor = reinforcementEndRound",
                 'workProbe.Dispose();\n                using var finalProbe = AdvancePhaseProbe.Enter("settlement");\n'
                 '                string deferredActivityActor = reinforcementEndRound')
    replace_once(scheduler, "selectionProbe.Dispose();",
                 'AdvancePhaseProbe.Boundary(segmentStart, next);\n                selectionProbe.Dispose();')
    replace_once(scheduler, "foreach (var actor in s.Actors.Where(a => !CapableWorker(s, a.Id))) {",
                 'using var probe = AdvancePhaseProbe.Enter("pause-incompatible-work");\n'
                 '            foreach (var actor in s.Actors.Where(a => !CapableWorker(s, a.Id))) {')
    replace_once(model / "SharedFormulaResearch.cs", "foreach (var job in s.FormulaWork.Where(x => x.Status == FormulaWorkStatus.Working).ToArray()) {\n                if (job.Kind",
                 'using var probe = AdvancePhaseProbe.Enter("credit-formula");\n'
                 '            foreach (var job in s.FormulaWork.Where(x => x.Status == FormulaWorkStatus.Working).ToArray()) {\n                if (job.Kind')
    condition = model / "ConditionCombatPolicy.cs"
    if "ConditionResolutionScope.Project" in condition.read_text(encoding="utf-8-sig"):
        replace_once(condition, "var journal = s.Conditions.Single(x => x.Target == actor);\n            return ConditionResolutionScope.Project",
                     'using var probe = AdvancePhaseProbe.Enter("restore-and-project-conditions");\n'
                     '            var journal = s.Conditions.Single(x => x.Target == actor);\n'
                     '            return ConditionResolutionScope.Project')
    else:
        replace_once(condition, "var ledger = ConditionHistory.Restore(s.Conditions.Single(x => x.Target == actor)).Ledger;",
                     'using var probe = AdvancePhaseProbe.Enter("restore-and-project-conditions");\n'
                     '            var ledger = ConditionHistory.Restore(s.Conditions.Single(x => x.Target == actor)).Ledger;')
    replace_once(model / "ConditionHistory.cs", 'if (journal.PolicyId != PolicyId)',
                 'using var probe = AdvancePhaseProbe.Enter("journal-reconstruction");\n'
                 '            if (journal.PolicyId != PolicyId)')
    (model / "AdvancePhaseProbe.cs").write_text(
        """using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class AdvancePhaseProbe : IDisposable
    {
        private static Dictionary<string, (long Ticks, int Count)> phases;
        private static List<string> boundaries;
        private readonly string name;
        private readonly long started;
        private bool stopped;

        private AdvancePhaseProbe(string name)
        {
            this.name = name;
            started = Stopwatch.GetTimestamp();
        }

        public static void Reset()
        {
            phases = new Dictionary<string, (long, int)>();
            boundaries = new List<string>();
        }
        public static void Boundary(RuleTime from, RuleTime to) => boundaries?.Add($"{from}|{to}");
        public static string[] Boundaries() => boundaries.ToArray();
        public static AdvancePhaseProbe Enter(string name) => new AdvancePhaseProbe(name);
        public static string[] Results() => phases.Select(row => FormattableString.Invariant(
            $"{row.Key}|{row.Value.Count}|{row.Value.Ticks * 1000.0 / Stopwatch.Frequency}")).ToArray();

        public void Dispose()
        {
            if (stopped || phases == null) return;
            stopped = true;
            phases.TryGetValue(name, out var prior);
            phases[name] = (prior.Ticks + Stopwatch.GetTimestamp() - started, prior.Count + 1);
        }
    }
}
""", encoding="utf-8")


if __name__ == "__main__":
    main()
