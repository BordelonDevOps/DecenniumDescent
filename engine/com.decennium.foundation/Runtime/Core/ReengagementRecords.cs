using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public sealed class ReengagementDefinition
    {
        public string RootId { get; }
        public string SegmentId { get; }
        public string LeadId { get; }
        public string CompanionId { get; }
        public string DefenderId { get; }
        public string ControllerId { get; }
        public string ConsentId { get; }
        public string DirectorMandateId { get; }

        public ReengagementDefinition(string rootId, string segmentId, string leadId, string companionId, string defenderId,
            string controllerId, string consentId, string directorMandateId)
        {
            if (new[] { rootId, segmentId, leadId, companionId, defenderId, controllerId }.Any(x => !Validation.ValidId(x))
                || rootId == segmentId || new[] { leadId, companionId, defenderId }.Distinct(StringComparer.Ordinal).Count() != 3
                || consentId != "" && !Validation.ValidId(consentId) || directorMandateId != "" && !Validation.ValidId(directorMandateId))
                throw new ArgumentException("Invalid re-engagement definition.");
            RootId = rootId;
            SegmentId = segmentId;
            LeadId = leadId;
            CompanionId = companionId;
            DefenderId = defenderId;
            ControllerId = controllerId;
            ConsentId = consentId;
            DirectorMandateId = directorMandateId;
        }

        public bool IsParticipant(string actor) => actor == LeadId || actor == CompanionId || actor == DefenderId;

        public bool IsWalk(Command command) => command.Kind == CommandKind.BeginWorldStep && command.Actor == LeadId
            && command.Target == "walk" && command.X == 0 && command.Y == 1;

        public bool IsApproach(WorldTraversalRecord edge) => edge != null && edge.ActorId == LeadId && !edge.Running
            && edge.FromX == 0 && edge.FromY == 0 && edge.ToX == 0 && edge.ToY == 1;

        public bool IsApproachCommand(Snapshot s, Command command) => s.Retreat?.SuccessfulExit != null && !s.InventoryCombat
            && s.Reengagement.Entry == null && IsWalk(command)
            && s.Actors.Any(a => a.Id == LeadId && a.X == 0 && a.Y == 0);
    }

    public sealed class ReengagementContact
    {
        public long ApproachRevision { get; }
        public long ArrivalRevision { get; }
        public string ArrivalCommandId { get; }
        public RuleTime At { get; }
        public int MarkerOrdinal { get; }
        public RuleQuantity DistanceFeet { get; }
        public string Failure { get; }
        public bool Entered => Failure == "";

        public ReengagementContact(long approachRevision, long arrivalRevision, string arrivalCommandId,
            RuleTime at, int markerOrdinal, RuleQuantity distanceFeet, string failure)
        {
            if (approachRevision < 1 || arrivalRevision <= approachRevision || !Validation.ValidId(arrivalCommandId)
                || markerOrdinal < -1 || distanceFeet != new RuleQuantity(5)
                || (failure == "" ? markerOrdinal < 0 : !Validation.ValidId(failure)))
                throw new ArgumentException("Invalid re-engagement contact.");
            ApproachRevision = approachRevision;
            ArrivalRevision = arrivalRevision;
            ArrivalCommandId = arrivalCommandId;
            At = at;
            MarkerOrdinal = markerOrdinal;
            DistanceFeet = distanceFeet;
            Failure = failure;
        }
    }

    public sealed class ReengagementRecord
    {
        public const int MaxContacts = 16;
        public ReengagementDefinition Definition { get; }
        public IReadOnlyList<ReengagementContact> Contacts { get; }
        public ReengagementContact Entry => Contacts.LastOrDefault()?.Entered == true ? Contacts.Last() : null;

        public ReengagementRecord(ReengagementDefinition definition, IEnumerable<ReengagementContact> contacts = null)
        {
            Definition = definition ?? throw new ArgumentNullException(nameof(definition));
            var rows = (contacts ?? Array.Empty<ReengagementContact>()).ToArray();
            if (rows.Length > MaxContacts || rows.Any(x => x == null)
                || rows.Skip(1).Where((x, i) => rows[i].Entered || x.ApproachRevision <= rows[i].ArrivalRevision || x.At <= rows[i].At).Any())
                throw new ArgumentException("Invalid re-engagement contact history.");
            Contacts = Array.AsReadOnly(rows);
        }

        public ReengagementRecord Append(ReengagementContact contact) => new ReengagementRecord(Definition, Contacts.Append(contact));
        public bool IsSegment(string id) => Entry != null && id == Definition.SegmentId;
    }
}
