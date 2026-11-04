#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Fixed resolved order and completed regular boundaries. This host admits no actor effects,
    /// surprise, reactions, extra turns or end-round events; those procedures cannot be skipped implicitly.
    /// Background crop/intake deadlines still use the existing exact shared timeline.</summary>
    public static class FixedEncounterRules
    {
        public static RuleTime Start(FixedEncounterRecord e,int ordinal)
        {
            if(e==null||ordinal<0)throw new ArgumentException("Invalid regular-turn ordinal.");
            return RuleTime.FromFraction((BigInteger)e.Origin.Numerator*e.Order.Count+(BigInteger)6*ordinal*e.Origin.Denominator,
                (BigInteger)e.Origin.Denominator*e.Order.Count);
        }
        internal static int TurnForRevision(FixedEncounterRecord e,long revision)
        {
            if(e==null||revision<=e.StartRevisions[0]||e.StartRevisions.Contains(revision))throw new ArgumentException("Action requires its own decision revision.");
            for(int i=e.StartRevisions.Count-1;i>=0;i--)if(revision>e.StartRevisions[i])return i;
            throw new ArgumentException("Missing regular start.");
        }
        internal static bool HistoricalHandling(Snapshot s,string job,string actor,RuleTime start,RuleTime end)
        {
            long revision=VesselHandling.CreationRevision(job);if(revision>s.Revision)return false;
            var e=EncounterHistory.AtRevision(s,revision);if(e==null)return false;
            int ordinal=TurnForRevision(e,revision);
            return start==end&&start==Start(e,ordinal)&&actor==e.Order[ordinal%e.Order.Count];
        }
        internal static int Interactions(Snapshot s,int ordinal)=>s.Handling.Count(h=>h.Tactical&&EncounterHistory.InCurrent(s,VesselHandling.CreationRevision(h.Id))&&TurnForRevision(s.Encounter,VesselHandling.CreationRevision(h.Id))==ordinal)
            +s.VesselMoves.Count(h=>h.Tactical&&EncounterHistory.InCurrent(s,VesselHandling.CreationRevision(h.Id))&&TurnForRevision(s.Encounter,VesselHandling.CreationRevision(h.Id))==ordinal);
        public static bool ActionSpent(Snapshot s)=>s.Encounter!=null&&(s.InventoryInteractions>1||s.EncounterDashes.Any(d=>d.TurnOrdinal==s.Encounter.TurnOrdinal&&EncounterHistory.InCurrent(s,d.Revision)));
        public static MovementLedger CurrentMovement(Snapshot s)
        {
            if(s.Encounter==null)throw new ArgumentException("No active encounter.");
            return new MovementLedger(0,s.EncounterDashes.Count(d=>d.TurnOrdinal==s.Encounter.TurnOrdinal&&EncounterHistory.InCurrent(s,d.Revision)));
        }
        private static string Number(long n)=>n.ToString(System.Globalization.CultureInfo.InvariantCulture);
        private static bool Receipt(Snapshot s,long revision,string actor,CommandKind kind,string target="",InventoryRequest request=null)
        {
            var receipt=s.Receipts.SingleOrDefault(r=>r.Revision==revision);
            return receipt!=null&&new Command(receipt.Id,actor,revision-1,kind,target,inventory:request).MatchesReceipt(receipt);
        }
        private static bool HistoryMatchesReceipts(Snapshot s)
        {
            var e=s.Encounter;var used=new System.Collections.Generic.HashSet<long>();
            if(s.Receipts.Select(r=>r.Revision).Distinct().Count()!=s.Receipts.Length)return false;
            for(int i=0;i<e.StartRevisions.Count;i++) {
                long revision=e.StartRevisions[i];used.Add(revision);
                if(!Receipt(s,revision,i==0?e.Order[0]:e.Order[(i-1)%e.Order.Count],
                    i==0?CommandKind.BeginFixedEncounter:CommandKind.EndRegularTurn,i==0?"":e.Id+".turn."+Number(i-1)))return false;
            }
            foreach(var h in s.Handling.Where(x=>x.Tactical)) {
                long revision=VesselHandling.CreationRevision(h.Id);
                if(revision>s.Revision||!used.Add(revision)||h.Id!="inventory."+Number(revision)+".handling"
                    ||h.ChildId!="inventory."+Number(revision)+".lot")return false;
                var child=s.InventoryLots.Single(x=>x.LotId==h.ChildId);var lot=s.Work.Lots.Single(x=>x.Id==h.ChildId);
                if(!Receipt(s,revision,h.ActorId,CommandKind.HandleInventory,h.SourceId,
                    new InventoryRequest(child.CreatedAmount,h.Kind==HandlingKind.Handover?lot.CustodianId:"",h.Kind)))return false;
            }
            foreach(var h in s.VesselMoves.Where(x=>x.Tactical)) {
                long revision=VesselHandling.CreationRevision(h.Id);
                if(revision>s.Revision||!used.Add(revision)||revision!=h.Sequence||h.Id!="inventory."+Number(revision)+".vessel-move"
                    ||!Receipt(s,revision,h.ActorId,CommandKind.HandleVessel,h.VesselId,
                        new InventoryRequest(new RuleQuantity(1),h.Kind==HandlingKind.Handover?h.ToCustodian:"",h.Kind)))return false;
            }
            foreach(var d in s.EncounterDashes) {
                if(!used.Add(d.Revision)||!Receipt(s,d.Revision,d.ActorId,CommandKind.EncounterDash,e.Id+".turn."+Number(d.TurnOrdinal)))return false;
            }
            // Every admitted encounter command leaves one record. Omitted spending must not restore a free Action.
            return s.Receipts.Count(r=>r.Revision>=e.StartRevisions[0])==used.Count
                &&s.Revision-e.StartRevisions[0]+1==used.Count;
        }
        internal static string Validate(Snapshot s,string[] order,bool actorLife=false)
        {
            if(s.SchemaVersion!=(actorLife?Snapshot.ActorLifeSchema:Snapshot.EncounterSchema))return "WrongEncounterSchema";
            var e=s.Encounter;if(e==null)return null;
            if(!HistoryMatchesReceipts(s))return "InvalidEncounterCommandHistory";
            if(!e.Order.SequenceEqual(order)||e.Id!="encounter."+e.StartRevisions[0].ToString(System.Globalization.CultureInfo.InvariantCulture)
                ||s.RuleClock!=Start(e,e.TurnOrdinal)||s.InventoryTurnActor!=e.CurrentActor||s.InventoryInteractions!=Interactions(s,e.TurnOrdinal)
                ||s.WaterFills.Any(j=>j.Pending))return "InvalidFixedEncounter";
            if(s.Work.WorkerIntervals.Any(w=>e.Order.Contains(w.WorkerId)&&w.End>e.Origin))return "EncounterWorkerConflict";
            foreach(var dash in s.EncounterDashes) {
                if(TurnForRevision(e,dash.Revision)!=dash.TurnOrdinal||e.StartRevisions.Contains(dash.Revision))return "InvalidDashHistory";
            }
            for(int i=0;i<e.StartRevisions.Count;i++) {
                int interactions=Interactions(s,i),dashes=s.EncounterDashes.Count(d=>d.TurnOrdinal==i);
                if(interactions>2||dashes>1||dashes+Math.Max(0,interactions-1)>1)return "OverspentRegularTurnAction";
            }
            return null;
        }
    }
    /// <summary>Supplied nonsurprised capable actors and an immutable already-adjudicated order.
    /// No automatic initiative tie policy, effects, attacks, reactions, joins/leaves, reorders or exit.
    /// Dash pays the same ordinary Action as a second object interaction; spatial execution remains gated.</summary>
    public sealed class TestOnlyEncounterPolicy : ICommandPolicy
    {
        private readonly TestOnlyFillingPolicy inventory=new TestOnlyFillingPolicy(movableVessels:true);
        private readonly string[] order;
        public TestOnlyEncounterPolicy(params string[] resolvedOrder):this(false,resolvedOrder) { }
        // Expanded order is only a dispatcher for the outer schema11 host, which supplies the third body.
        internal TestOnlyEncounterPolicy(bool tacticalHost,params string[] resolvedOrder)
        {
            order=resolvedOrder==null?throw new ArgumentNullException(nameof(resolvedOrder))
                :resolvedOrder.Length==0?new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId}:resolvedOrder.ToArray();
            if(order.Length<1||order.Length>(tacticalHost?3:2)||order.Distinct(StringComparer.Ordinal).Count()!=order.Length
                ||order.Any(x=>x!=TestOnlyPolicy.ActorId&&x!=TestOnlyPolicy.CompanionId&&(!tacticalHost||x!=AdditionalTacticalActor.Id)))throw new ArgumentException("Supply distinct fixture actors in resolved order.");
        }
        public bool TestOnly=>true;
        public string ContentFingerprint=>"TEST_ONLY.encounter-v1-"+string.Join("-",order.Select(x=>x==TestOnlyPolicy.ActorId?"a":x==TestOnlyPolicy.CompanionId?"c":"t"));
        public Snapshot Initial(){var s=inventory.Initial();s.SchemaVersion=Snapshot.EncounterSchema;s.ContentFingerprint=ContentFingerprint;return s;}
        public string Resolve(Snapshot s,Command c)
        {
            if(c.Kind==CommandKind.EnterInventoryCombat)return "UseFixedEncounterEntry";
            if(c.Kind==CommandKind.BeginFixedEncounter) {
                if(s.Encounter!=null||s.InventoryCombat||c.Inventory!=null||c.Target!=""||c.X!=0||c.Y!=0||c.Actor!=order[0])return "InvalidFixedEncounterEntry";
                if(s.WaterFills.Any(j=>j.Pending))return "PendingFillEncounterTransitionUnsupported";
                foreach(var intake in s.Intakes.Where(j=>j.Status==IntakeStatus.Working).ToArray())OrdinaryInventory.Interrupt(s,intake,IntakeStatus.CombatInterrupted);
                if(order.Any(actor=>OrdinaryInventory.Busy(s,actor)))return "EncounterWorkerBusy";
                s.Encounter=new FixedEncounterRecord("encounter."+(s.Revision+1).ToString(System.Globalization.CultureInfo.InvariantCulture),s.RuleClock,order,new[]{s.Revision+1});
                s.InventoryCombat=true;s.InventoryTurnActor=order[0];s.InventoryInteractions=0;return null;
            }
            if(c.Kind==CommandKind.EndRegularTurn||c.Kind==CommandKind.EncounterDash) {
                var e=s.Encounter;
                if(e==null||c.Inventory!=null||c.Actor!=e.CurrentActor||c.Target!=e.CurrentTurnId||c.X!=0||c.Y!=0)return "WrongRegularTurn";
                if(c.Kind==CommandKind.EncounterDash) {
                    if(FixedEncounterRules.ActionSpent(s))return "ActionAlreadySpent";
                    s.EncounterDashes=s.EncounterDashes.Concat(new[]{new EncounterDashRecord(s.Revision+1,e.TurnOrdinal,c.Actor)}).ToArray();return null;
                }
                if(e.StartRevisions.Count==128)return "EncounterHistoryCapacityReached";
                // No admitted actor End/Start effects or end-round events. Complete the outgoing slot,
                // including real background milestones, before recording the next regular Start.
                OrdinaryInventory.AdvanceTo(s,FixedEncounterRules.Start(e,e.TurnOrdinal+1));
                s.Encounter=new FixedEncounterRecord(e.Id,e.Origin,e.Order,e.StartRevisions.Concat(new[]{s.Revision+1}));
                s.InventoryTurnActor=s.Encounter.CurrentActor;s.InventoryInteractions=0;return null;
            }
            if(s.Encounter!=null) {
                if(c.Kind!=CommandKind.HandleInventory&&c.Kind!=CommandKind.HandleVessel)return "EncounterCommandNotImplemented";
                if(c.Actor!=s.Encounter.CurrentActor)return "WrongRegularTurn";
                if(s.InventoryInteractions>0&&FixedEncounterRules.ActionSpent(s))return "ActionAlreadySpent";
            }
            return inventory.Resolve(s,c);
        }
        public string ValidateState(Snapshot s)=>ValidateEncounterState(s);
        internal string ValidateEncounterState(Snapshot s,bool actorLife=false)
        {
            try {return FixedEncounterRules.Validate(s,order,actorLife)??inventory.ValidateFillingState(s,true,actorLife);}
            catch(Exception ex) when(ex is ArgumentException||ex is InvalidOperationException||ex is OverflowException){return "InvalidEncounterState";}
        }
    }
}
#endif
