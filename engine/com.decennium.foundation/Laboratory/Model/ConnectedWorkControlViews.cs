#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class ExpeditionWorkClaimView
    {
        public string Id { get; }
        public string ResourceId { get; }
        public string OwnerId { get; }
        public string UnitId { get; }
        public RuleQuantity Amount { get; }
        public RuleQuantity Consumed { get; }
        public RuleQuantity Released { get; }
        public RuleQuantity Remaining { get; }
        public string Status { get; }
        internal ExpeditionWorkClaimView(ResourceReservation claim, ResourceLot lot, string owner)
        {
            Id = claim.Id; ResourceId = claim.LotId; OwnerId = owner; UnitId = lot.UnitId;
            Amount = claim.Amount; Consumed = claim.ConsumedAmount; Released = claim.ReleasedAmount;
            Remaining = claim.RemainingAmount; Status = claim.Status.ToString();
        }
    }

    public sealed class ExpeditionWorkBookingView
    {
        public string Id { get; }
        public RuleTime Start { get; }
        public RuleTime End { get; }
        public bool IncludesFutureTime { get; }
        internal ExpeditionWorkBookingView(WorkerInterval booking, RuleTime now)
        { Id = booking.Id; Start = booking.Start; End = booking.End; IncludesFutureTime = booking.End > now; }
    }

    public sealed class ExpeditionControlledWorkView
    {
        public string Id { get; }
        public string ActorId { get; }
        public string Kind { get; }
        public string Status { get; }
        public RuleTime StartedAt { get; }
        public RuleTime Labor { get; }
        public RuleTime Retained { get; }
        public RuleTime Required { get; }
        public RuleTime Remaining { get; }
        public string Stage { get; }
        public int? CompletedPhases { get; }
        public RuleTime? PartialPhase { get; }
        public IReadOnlyList<RuleTime> Phases { get; }
        public bool AwaitingCheck { get; }
        public bool AwaitingChoice { get; }
        public RuleTime? MiningCommittedAt { get; }
        public string CapacityVesselId { get; }
        public RuleQuantity? ReservedCapacityPints { get; }
        public bool OpeningInUse { get; }
        public IReadOnlyList<ExpeditionWorkClaimView> Claims { get; }
        public IReadOnlyList<ExpeditionWorkBookingView> Bookings { get; }
        public IReadOnlyList<CommandOption> Controls { get; }

        internal ExpeditionControlledWorkView(string id, string actor, string kind, string status, RuleTime started,
            RuleTime labor, RuleTime retained, RuleTime required, RuleTime remaining, string stage,
            ActiveWorkProgress progress, RuleTime? committed, string capacityVessel, RuleQuantity? reservedCapacity,
            bool openingInUse, IEnumerable<ExpeditionWorkClaimView> claims, IEnumerable<ExpeditionWorkBookingView> bookings,
            IEnumerable<CommandOption> controls)
        {
            Id = id; ActorId = actor; Kind = kind; Status = status; StartedAt = started;
            Labor = labor; Retained = retained; Required = required; Remaining = remaining; Stage = stage;
            CompletedPhases = progress?.CompletedPhases; PartialPhase = progress?.Partial;
            Phases = Array.AsReadOnly(progress == null ? Array.Empty<RuleTime>() : progress.Phases.ToArray());
            AwaitingCheck = status == "AwaitingCheck"; AwaitingChoice = status == "AwaitingChoice";
            MiningCommittedAt = committed; CapacityVesselId = capacityVessel; ReservedCapacityPints = reservedCapacity;
            OpeningInUse = openingInUse;
            Claims = Array.AsReadOnly(claims.OrderBy(x => x.Id, StringComparer.Ordinal).ToArray());
            Bookings = Array.AsReadOnly(bookings.OrderBy(x => x.Start).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray());
            Controls = Array.AsReadOnly(controls.ToArray());
        }
    }

    public sealed class ExpeditionFillParameters
    {
        public string SourceId { get; }
        public string DestinationId { get; }
        public string UnitId { get; }
        public RuleQuantity AvailableSource { get; }
        public RuleQuantity FreeDestinationCapacity { get; }
        public RuleQuantity StockCapacityBound { get; }
        public RuleTime RequiredActiveTime => new RuleTime(60);
        public string AmountRequirement => "Positive exact rational pints; examples are not exhaustive. Query the complete request for actual availability.";
        public IReadOnlyList<RuleQuantity> ExampleAmounts { get; }
        internal ExpeditionFillParameters(string source, string destination, string unit, RuleQuantity available, RuleQuantity capacity)
        {
            SourceId = source; DestinationId = destination; UnitId = unit;
            AvailableSource = available; FreeDestinationCapacity = capacity;
            StockCapacityBound = available < capacity ? available : capacity;
            ExampleAmounts = Array.AsReadOnly(new[] { new RuleQuantity(1, 2), new RuleQuantity(1), StockCapacityBound }
                .Where(x => x > default(RuleQuantity) && x <= StockCapacityBound).Distinct().OrderBy(x => x).ToArray());
        }
    }

    public sealed class ExpeditionMiningParameters
    {
        public string DepositId { get; }
        public string VersionId { get; }
        public bool? ClaimClosed { get; }
        public IReadOnlyList<string> CategoryIds { get; }
        public IReadOnlyList<ExpeditionMiningUnitView> Units { get; }
        public IReadOnlyList<MiningAbilityChoice> Abilities { get; }
        public IReadOnlyList<bool> HurriedChoices { get; }
        public string CategorySelection => "Select a nonempty distinct category set; each category includes all its units. The native request and query validate the complete selection.";
        public string PreferenceSelection => "Optional failure and critical preferences accept visible selected-unit IDs as inputs, subject to the native query. No value ranking, damaged-unit shortlist or outcome is disclosed.";
        public string AssistantSelection => "Empty; assistants are not selected by this profile.";
        internal ExpeditionMiningParameters(ExpeditionMiningSiteView site)
        {
            DepositId = site.DepositId; VersionId = site.VersionId; ClaimClosed = site.ClaimClosed;
            Units = Array.AsReadOnly(site.Units.OrderBy(x => x.Id, StringComparer.Ordinal).ToArray());
            CategoryIds = Array.AsReadOnly(site.Units.Select(x => x.CategoryId).Distinct(StringComparer.Ordinal)
                .OrderBy(x => x, StringComparer.Ordinal).ToArray());
            Abilities = Array.AsReadOnly(new[] { MiningAbilityChoice.Strength, MiningAbilityChoice.Wisdom });
            HurriedChoices = Array.AsReadOnly(new[] { false, true });
        }
    }

    public sealed class ExpeditionWorkObservation
    {
        public bool Enabled { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public IReadOnlyList<ExpeditionControlledWorkView> Jobs { get; }
        public IReadOnlyList<ExpeditionFillParameters> Filling { get; }
        public ExpeditionMiningParameters Mining { get; }
        internal ExpeditionWorkObservation(bool enabled, long revision, string actor,
            IEnumerable<ExpeditionControlledWorkView> jobs, IEnumerable<ExpeditionFillParameters> filling,
            ExpeditionMiningParameters mining)
        {
            Enabled = enabled; Revision = revision; ActorId = actor;
            Jobs = Array.AsReadOnly(jobs.OrderBy(x => x.Id, StringComparer.Ordinal).ToArray());
            Filling = Array.AsReadOnly(filling.OrderBy(x => x.SourceId, StringComparer.Ordinal)
                .ThenBy(x => x.DestinationId, StringComparer.Ordinal).ToArray());
            Mining = mining;
        }
    }
}
#endif
