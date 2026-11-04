#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One explicitly supplied lawful test event. It grants no spell acquisition,
    /// player Action, target selection, application cost or general source eligibility.</summary>
    public sealed class ConditionFixtureEvent
    {
        public string Target { get; }
        public ConditionOperation Operation { get; }
        public ConditionFixtureEvent(string target, ConditionOperation operation)
        {
            if (!Validation.ValidId(target) || operation == null || !operation.Id.StartsWith("event.", StringComparison.Ordinal)
                || operation.Kind == ConditionOperationKind.Advance || operation.At.Phase != 0
                || operation.Application?.Expires?.Phase > 0 || operation.Immunity?.Expires?.Phase > 0)
                throw new ArgumentException("Supply a named test event with absolute phase-zero timing.");
            if (operation.Application?.Kind == "Prone" && (operation.Application.Expires.HasValue || !operation.Application.GenericCureAllowed))
                throw new ArgumentException("This host admits ordinary stand-or-cure Prone only.");
            Target = target; Operation = operation;
        }
    }

    /// <summary>Known locations, ordinary sight only, no concentration or source-specific body
    /// exceptions. Events are fixed host fixtures, not arbitrarily submitted condition payloads.</summary>
    public sealed class ConditionCombatFixture
    {
        public IReadOnlyList<ConditionFixtureEvent> Events { get; }
        public string Fingerprint { get; }
        public ConditionCombatFixture(params ConditionFixtureEvent[] events)
        {
            if (events == null || events.Length > 128 || events.Any(x => x == null)
                || events.Select(x => x.Operation.Id).Distinct(StringComparer.Ordinal).Count() != events.Length)
                throw new ArgumentException("Invalid condition fixture events.");
            Events = Array.AsReadOnly(events.OrderBy(x => x.Operation.Id, StringComparer.Ordinal).ToArray());
            string key = "condition-host-v1|absolute-phase0|known-locations|no-concentration|safe-choice-events|residual-body-prohibition|paid-suppressed-stand|"
                + string.Join(";", Events.Select(x => x.Target + "|" + x.Operation.StructuralKey));
            using (var sha = SHA256.Create()) Fingerprint = "conditions-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }
}
#endif
