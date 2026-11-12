#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class ExpeditionVisibleActor
    {
        public string Id { get; }
        public int X { get; }
        public int Y { get; }

        internal ExpeditionVisibleActor(ActorState actor)
        {
            Id = actor.Id;
            X = actor.X;
            Y = actor.Y;
        }
    }

    public sealed class ExpeditionOwnActor
    {
        public ExpeditionVisibleActor Position { get; }
        public long Hp { get; }
        public long MaximumHp { get; }
        public bool Dead { get; }
        public IReadOnlyList<ConditionClause> Conditions { get; }
        public IReadOnlyList<string> HeldItems { get; }
        public IReadOnlyList<ExpeditionVisibleActor> VisibleOpponents { get; }
        public string Travel { get; }

        internal ExpeditionOwnActor(Snapshot state, ActorState actor, Authority grant)
        {
            Position = new ExpeditionVisibleActor(actor);
            var life = state.Lives.Single(x => x.ActorId == actor.Id);
            Hp = life.Hp;
            MaximumHp = life.MaximumHp;
            Dead = life.Dead;
            Conditions = Array.AsReadOnly(TestOnlyClubAttackPolicy.CombatConditions(state, actor.Id).Active.ToArray());
            HeldItems = Array.AsReadOnly(life.HeldItems.ToArray());
            var roster = state.InventoryCombat ? state.Encounter.Order : Array.Empty<string>();
            VisibleOpponents = Array.AsReadOnly(state.Actors.Where(x => !grant.Controls(x.Id) && roster.Contains(x.Id)
                && roster.Contains(actor.Id) && ObservationRules.CanSee(state, actor.Id, x.Id))
                .Select(x => new ExpeditionVisibleActor(x)).ToArray());
            var edge = state.WorldTraversals.SingleOrDefault(x => x.ActorId == actor.Id);
            Travel = edge == null ? "" : FormattableString.Invariant(
                $"Toward ({edge.ToX}, {edge.ToY}), {edge.DistanceFeet} of 5 feet, {edge.Status}");
        }
    }

    public sealed class ExpeditionOwnedItem
    {
        public string Id { get; }
        public string OwnerId { get; }
        public RuleQuantity? Available { get; }
        public string Placement { get; }
        public bool? Open { get; }

        internal ExpeditionOwnedItem(string id, string ownerId, RuleQuantity? available, string placement, bool? open = null)
        {
            Id = id;
            OwnerId = ownerId;
            Available = available;
            Placement = placement;
            Open = open;
        }
    }

    public sealed class ExpeditionWorkStatus
    {
        public string Id { get; }
        public string ActorId { get; }
        public string Kind { get; }
        public string Status { get; }
        public RuleTime? Remaining { get; }

        internal ExpeditionWorkStatus(string id, string actorId, string kind, string status, RuleTime? remaining = null)
        {
            Id = id;
            ActorId = actorId;
            Kind = kind;
            Status = status;
            Remaining = remaining;
        }
    }

    public sealed class ExpeditionSeatView
    {
        public string Profile => ConnectedExpeditionSession.Profile;
        public bool TestOnly => true;
        public bool Enabled { get; }
        public long Revision { get; }
        public RuleTime Clock { get; }
        public bool InEncounter { get; }
        public ExpeditionTurnSeat NextSeat { get; }
        public ExpeditionDecisionKind PendingDecision { get; }
        public bool OpportunityPending => PendingDecision == ExpeditionDecisionKind.Opportunity;
        public string ActingActorId { get; }
        public string TurnId { get; }
        public string DecisionId { get; }
        public string OpportunityId => OpportunityPending ? DecisionId : "";
        public IReadOnlyList<ExpeditionOwnActor> Actors { get; }
        public IReadOnlyList<ExpeditionOwnedItem> Items { get; }
        public IReadOnlyList<ExpeditionWorkStatus> Work { get; }
        public IReadOnlyList<CommandKind> Commands { get; }
        public IReadOnlyDictionary<CommandKind, string> KnownTargets { get; }
        public long HistoricalSaleCopper { get; }

        internal ExpeditionSeatView(ExpeditionActionResult position, bool enabled, bool combat, string actorId,
            string turnId, string decisionId, IEnumerable<ExpeditionOwnActor> actors,
            IEnumerable<ExpeditionOwnedItem> items, IEnumerable<ExpeditionWorkStatus> work,
            IEnumerable<CommandKind> commands, IReadOnlyDictionary<CommandKind, string> knownTargets,
            long historicalSaleCopper)
        {
            Enabled = enabled;
            Revision = position.Revision;
            Clock = position.Clock;
            InEncounter = combat;
            NextSeat = enabled ? position.NextSeat : ExpeditionTurnSeat.Unavailable;
            PendingDecision = position.PendingDecision;
            ActingActorId = actorId;
            TurnId = turnId;
            DecisionId = decisionId;
            Actors = Array.AsReadOnly(actors.ToArray());
            Items = Array.AsReadOnly(items.ToArray());
            Work = Array.AsReadOnly(work.ToArray());
            Commands = Array.AsReadOnly(commands.ToArray());
            KnownTargets = knownTargets;
            HistoricalSaleCopper = historicalSaleCopper;
        }
    }

    public sealed partial class ConnectedExpeditionSession
    {
        private static readonly IReadOnlyDictionary<CommandKind, string> NoKnownTargets =
            new ReadOnlyDictionary<CommandKind, string>(new Dictionary<CommandKind, string>());

        /// <summary>Projects only the granted actors, their resources and jobs, and actual sight of tactical opponents.
        /// Command families and named services are supported inputs. The resolver determines current availability.</summary>
        public ExpeditionSeatView View(ExpeditionSeat seat)
        {
            lock (gate) {
                var state = simulation.Capture();
                var grant = SeatGrant(seat);
                bool player = seat == ExpeditionSeat.Player;
                bool discloseTacticalSlot = grant != null && (player || FirstEncounterActive(state));
                var position = new ExpeditionActionResult(ExpeditionResponse.Waiting, state, discloseTacticalSlot);
                if (grant == null)
                    return new ExpeditionSeatView(position, false, false, "", "", "", Array.Empty<ExpeditionOwnActor>(),
                        Array.Empty<ExpeditionOwnedItem>(), Array.Empty<ExpeditionWorkStatus>(), Array.Empty<CommandKind>(),
                        NoKnownTargets, 0);
                string acting = ActingActor(state, out _, out string decisionId);
                string ownedActing = grant.Controls(acting) ? acting : "";
                string ownedDecision = ownedActing != "" ? decisionId : "";
                string turn = state.InventoryCombat && grant.Controls(state.Encounter.CurrentActor) ? state.Encounter.CurrentTurnId : "";
                return new ExpeditionSeatView(position, true, discloseTacticalSlot && state.InventoryCombat,
                    ownedActing, turn, ownedDecision,
                    state.Actors.Where(x => grant.Controls(x.Id)).Select(x => new ExpeditionOwnActor(state, x, grant)),
                    ProjectItems(state, grant), player ? ProjectWork(state, grant) : Array.Empty<ExpeditionWorkStatus>(),
                    player ? CombatCommands.Concat(PartyCommands) : CombatCommands,
                    player ? KnownServices : NoKnownTargets,
                    player ? state.HavenSales.Where(x => grant.Controls(x.Basis.SellerId)).Sum(x => x.PaymentCopper ?? 0) : 0);
            }
        }

        private static IEnumerable<ExpeditionOwnedItem> ProjectItems(Snapshot state, Authority grant)
        {
            foreach (var item in state.PortableEquipment.Where(x => grant.MayUseInventory(x.OwnerId)
                && grant.Controls(x.CustodianId))) {
                var lot = state.InventoryLots.FirstOrDefault(x => x.LotId == item.LinkedId && grant.MayUseInventory(x.OwnerId));
                yield return new ExpeditionOwnedItem(item.Id, item.OwnerId, lot == null ? (RuleQuantity?)null
                    : state.Work.AvailableAmount(lot.LotId), item.Placement.ToString(), item.Open);
            }
            foreach (var item in state.Clubs.Where(x => grant.MayUseInventory(x.OwnerId) && grant.Controls(x.CustodianId)))
                yield return new ExpeditionOwnedItem(item.Id, item.OwnerId, null, item.HeldBy == "" ? "Ground" : "Held");
            foreach (var lot in state.InventoryLots.Where(x => grant.MayUseInventory(x.OwnerId)
                && !state.PortableEquipment.Any(i => i.Id == x.LotId || i.LinkedId == x.LotId))) {
                if (state.Work.Lots.Any(x => x.Id == lot.LotId && grant.Controls(x.CustodianId)))
                    yield return new ExpeditionOwnedItem(lot.LotId, lot.OwnerId, state.Work.AvailableAmount(lot.LotId),
                        lot.Access.ToString());
            }
            foreach (var dose in state.AlchemyDoses.Where(x => grant.MayUseInventory(x.OwnerId)
                && grant.Controls(x.CustodianId) && !x.Spent))
                yield return new ExpeditionOwnedItem(dose.Id, dose.OwnerId, new RuleQuantity(1), "Dose");
        }

        private static IEnumerable<ExpeditionWorkStatus> ProjectWork(Snapshot state, Authority grant)
        {
            foreach (var job in state.MiningAttempts.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Mining", job.Status.ToString());
            foreach (var job in state.Intakes.Where(x => grant.Controls(x.ActorId)))
                yield return new ExpeditionWorkStatus(job.Id, job.ActorId, "Intake", job.Status.ToString());
            foreach (var job in state.HavenAppraisals.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Appraisal", job.Status.ToString(), job.Work.Remaining);
            foreach (var job in state.ExpeditionBills.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Bill", job.Status.ToString(), job.Work.Remaining);
            foreach (var job in state.HavenSales.Where(x => grant.Controls(x.Basis.SellerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.Basis.SellerId, "Sale", job.Status.ToString(), job.Work.Remaining);
            if (state.CharterAttempt != null && grant.Controls(Hero))
                yield return new ExpeditionWorkStatus(state.CharterAttempt.Id, Hero, "Charter", state.CharterAttempt.Outcome.ToString());
            foreach (var job in state.FormulaWork.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Formula", job.Status.ToString(), job.Work.Remaining);
            foreach (var job in state.ManufacturingOrders.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Manufacturing", job.Status.ToString(), job.Work.Remaining);
        }
    }
}
#endif
