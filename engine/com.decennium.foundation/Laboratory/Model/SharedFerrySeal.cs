#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Only directly perceived physical facts; no creature association or suppression clock.</summary>
    public sealed class ExposedSealView
    {
        public string Id => FerryWraithProfile.Seal;
        public string Description => "Exposed paper seal on a fixed post";
        public int X => 9;
        public int Y => 3;
        public bool Torn { get; }
        internal ExposedSealView(bool torn) { Torn=torn; }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        internal static bool CanSeeFerrySeal(Snapshot s,string actor)
        {
            if(s.FerryWraith==null||!s.Actors.Any(x=>x.Id==actor)||!ActorLifeRules.CanAct(s,actor))return false;
            var view=View(s,actor);
            return !view.Unaware&&!view.BlocksSight&&ObservationGeometry.GeometricSight(s,actor,
                ObservationGeometry.Position(s,actor),new ObservationPoint(new RuleQuantity(9),new RuleQuantity(3)));
        }

        private string AssessFerrySeal(Snapshot s,Command c)
        {
            if(s.FerryWraith==null)return "ExposedSealUnavailable";
            if(!FerryWraithProfile.SealPayloadValid(c))return "InvalidSealRequest";
            if(!CanSeeFerrySeal(s,c.Actor))return "ExposedSealUnavailable";
            if(s.FerryWraith.SealDestroyed)return "ExposedSealAlreadyTorn";
            if(PendingCalendarChoice(s)||ManufacturingChoicePending(s)||HasPendingRecoveryOffer(s)||s.ManufacturingAdvance!=null)
                return "TacticalChoicePending";
            if(TestOnlyClubAttackPolicy.HasUnprocessedConditionDeadline(s))return "ConditionBoundaryPending";
            var body=s.Actors.Single(x=>x.Id==c.Actor);
            if(!SharedDeclaredGeometry.SupportsAnchorAt(s,body.X,body.Y))return "SealActorUnsupported";
            if(Math.Max(Math.Abs((long)body.X-9),Math.Abs((long)body.Y-3))>1)return "SealOutOfReach";
            if(!ObservationGeometry.LineOfEffectClearToCell(s,c.Actor,9,3))return "SealEffectLineBlocked";
            if(!CapableWorker(s,c.Actor)||!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(AvailableHands(s,c.Actor)<1)return "UsableHandRequired";
            if(OrdinaryInventory.Busy(s,c.Actor)||CharacterAdvancementRules.Busy(s,c.Actor)
                ||s.WorldTraversals.Any(x=>x.ActorId==c.Actor)||IsOffCalendarActivity(s,c.Actor)&&ActivityHasLabor(s,c.Actor)
                ||s.ExplorationSearch?.Pending!=null&&s.ExplorationSearch.Definition.SearcherId==c.Actor
                ||s.ExplorationHide?.Pending!=null&&s.ExplorationHide.Definition.HiderId==c.Actor)
                return "SealRequiresStationaryAccess";
            var epoch=WorldTiming.ForActor(s,c.Actor);
            if(s.InventoryCombat&&(epoch==null||s.Encounter?.CurrentActor!=c.Actor||s.InventoryTurnActor!=c.Actor))
                return "WrongRegularTurn";
            if(epoch!=null)return Interval(s,c.Actor).ActionSpent?"ActionAlreadySpent":null;
            if(!IsOffCalendarActivity(s,c.Actor))return "SealActionLedgerUnavailable";
            return ActivityInterval(s,c.Actor).Action!=WorldActionCommitment.None?"OffCalendarActionAlreadySpent":null;
        }

        private string ResolveFerrySeal(Snapshot s,Command c,bool assess)
        {
            string failure=AssessFerrySeal(s,c);if(failure!=null||assess)return failure;
            var body=s.Actors.Single(x=>x.Id==c.Actor);var epoch=WorldTiming.ForActor(s,c.Actor);
            bool scheduled=epoch!=null;
            string calendar=scheduled?epoch.Id:ActivityInterval(s,c.Actor).CalendarId;
            long interval=scheduled?Interval(s,c.Actor).LastStart:ActivityInterval(s,c.Actor).IntervalIndex;
            var original=s.InventoryCombat?WorldTiming.ForEncounter(s):null;
            long cycle=original==null?-1:original.SlotAt(s.RuleClock)/original.Order.Count;
            var rupture=new SealRuptureRecord(c.Id,s.Revision+1,c.Actor,body.X,body.Y,s.RuleClock,
                scheduled?SealActionLedger.Scheduled:SealActionLedger.OffCalendar,calendar,interval,s.InventoryCombat,
                original?.Id??"",original?.Origin??default,cycle,
                original==null?s.RuleClock.AddSeconds(6):original.Origin.AddSeconds(checked((cycle+2)*6)));
            if(scheduled)SetInterval(s,Interval(s,c.Actor).PayAction());
            else SetActivityInterval(s,ActivityInterval(s,c.Actor).PaySealTear(c.Id,s.Revision+1));
            s.FerryWraith=s.FerryWraith.Tear(rupture);
            return null;
        }

        private static RuleTime? NextFerrySealBoundary(Snapshot s)
            =>s.FerryWraith?.ClawSuppressed==true?(RuleTime?)s.FerryWraith.Rupture.ExpiresAt:null;

        // Called after due Ends, before any scheduled or off-calendar Start refresh.
        private static void ExpireFerrySealSuppression(Snapshot s)
        {
            if(s.FerryWraith?.ClawSuppressed==true&&s.RuleClock>=s.FerryWraith.Rupture.ExpiresAt)
                s.FerryWraith=s.FerryWraith.Expire(s.Revision+1);
        }

        private IEnumerable<Command> DiscoverFerrySeal(Snapshot s,string actor)
        {
            if(!CanSeeFerrySeal(s,actor)||s.FerryWraith.SealDestroyed)yield break;
            yield return new Command("query.seal.tear",actor,s.Revision,CommandKind.TearExposedSeal,FerryWraithProfile.Seal);
        }
    }

    public sealed partial class ConnectedExpeditionSession
    {
        public ExposedSealView ObserveExposedSeal(ExpeditionSeat seat,string actor)
        {
            lock(gate) {
                var state=simulation.Capture();var grant=SeatGrant(seat);
                return grant!=null&&grant.Controls(actor)&&TestOnlySharedWorldPolicy.CanSeeFerrySeal(state,actor)
                    ?new ExposedSealView(state.FerryWraith.SealDestroyed):null;
            }
        }
    }
}
#endif
