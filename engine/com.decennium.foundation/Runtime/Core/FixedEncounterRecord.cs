using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    public sealed class EncounterRosterPhase
    {
        public WorldScheduleRecord Epoch { get; }
        public int FirstTurn { get; }
        public long FirstRound { get; }

        public EncounterRosterPhase(WorldScheduleRecord epoch, int firstTurn, long firstRound)
        {
            if (epoch == null || firstTurn < 1 || firstRound < 2)
                throw new ArgumentException("Invalid prospective encounter roster phase.");
            Epoch = epoch;
            FirstTurn = firstTurn;
            FirstRound = firstRound;
        }

        public int GlobalTurn(long localTurn) => checked(FirstTurn + (int)localTurn);
        public bool Owns(int globalTurn) => globalTurn >= FirstTurn;
        public RuleTime Start(int globalTurn) => Epoch.Start(checked(globalTurn - FirstTurn));
        public long Round(int globalTurn) => checked(FirstRound + (globalTurn - FirstTurn) / Epoch.Order.Count);
        public string Actor(int globalTurn) => Epoch.Order[(globalTurn - FirstTurn) % Epoch.Order.Count];
    }

    /// <summary>Completed boundary transactions only. A start revision identifies one regular turn;
    /// earlier starts are retained so historical actions never bind to the current cursor.</summary>
    public sealed class FixedEncounterRecord
    {
        public string Id { get; }
        public RuleTime Origin { get; }
        public IReadOnlyList<string> InitialOrder { get; }
        public EncounterRosterPhase RosterPhase { get; }
        public EncounterRosterPhase InheritedPhase { get; }
        private EncounterRosterPhase TimingPhase => InheritedPhase ?? RosterPhase;
        public IReadOnlyList<string> Order => OrderAt(TurnOrdinal);
        public IReadOnlyList<long> StartRevisions { get; }
        // Schema14 can record sparse cursor observations against an established calendar. These
        // revisions are actual commands, not claims that every earlier Start was a new command.
        public IReadOnlyList<int> ObservedOrdinals { get; }
        public bool Sparse=>ObservedOrdinals.Where((n,i)=>n!=i).Any();
        public int TurnOrdinal=>ObservedOrdinals[ObservedOrdinals.Count-1];
        public long Round => RoundAt(TurnOrdinal);
        public string CurrentActor => ActorAt(TurnOrdinal);
        public IReadOnlyList<string> OrderAt(int ordinal) => TimingPhase?.Owns(ordinal) == true ? TimingPhase.Epoch.Order : InitialOrder;
        public long RoundAt(int ordinal) => TimingPhase?.Owns(ordinal) == true ? TimingPhase.Round(ordinal) : (long)ordinal / InitialOrder.Count + 1;
        public string ActorAt(int ordinal) => TimingPhase?.Owns(ordinal) == true ? TimingPhase.Actor(ordinal) : InitialOrder[ordinal % InitialOrder.Count];

        private RuleTime InitialStart(int ordinal)
            => RuleTime.FromFraction((BigInteger)Origin.Numerator * InitialOrder.Count + (BigInteger)6 * ordinal * Origin.Denominator,
                (BigInteger)Origin.Denominator * InitialOrder.Count);

        public RuleTime StartAt(int ordinal) => TimingPhase?.Owns(ordinal) == true ? TimingPhase.Start(ordinal) : InitialStart(ordinal);
        public RuleTime NextOwnStart(int originatingTurn)
        {
            int next = checked(originatingTurn + OrderAt(originatingTurn).Count);
            return TimingPhase?.Owns(originatingTurn) == true ? TimingPhase.Start(next) : InitialStart(next);
        }
        public string CurrentTurnId=>Id+".turn."+TurnOrdinal.ToString(System.Globalization.CultureInfo.InvariantCulture);
        public FixedEncounterRecord(string id,RuleTime origin,IEnumerable<string> order,IEnumerable<long> starts)
            :this(id,origin,order,starts,null) { }
        public FixedEncounterRecord(string id,RuleTime origin,IEnumerable<string> order,IEnumerable<long> starts,IEnumerable<int> observedOrdinals)
            : this(id, origin, order, starts, observedOrdinals, null) { }
        public FixedEncounterRecord(string id, RuleTime origin, IEnumerable<string> order, IEnumerable<long> starts,
            IEnumerable<int> observedOrdinals, EncounterRosterPhase rosterPhase)
            : this(id, origin, order, starts, observedOrdinals, rosterPhase, null) { }

        public FixedEncounterRecord(string id, RuleTime origin, IEnumerable<string> order, IEnumerable<long> starts,
            IEnumerable<int> observedOrdinals, EncounterRosterPhase rosterPhase, EncounterRosterPhase inheritedPhase)
        {
            if(!Validation.ValidId(id)||order==null||starts==null)throw new ArgumentException("Invalid encounter header.");
            var ids=order.ToArray();var revisions=starts.ToArray();
            var ordinals=observedOrdinals==null?Enumerable.Range(0,revisions.Length).ToArray():observedOrdinals.ToArray();
            if(ids.Length<1||ids.Length>64||ids.Any(x=>!Validation.ValidId(x))||ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length
                ||revisions.Length<1||revisions.Length>128||revisions.Any(x=>x<1)
                ||revisions.Where((x,i)=>i>0&&x<=revisions[i-1]).Any()||ordinals.Length!=revisions.Length||ordinals.Any(x=>x<0)
                ||ordinals.Where((x,i)=>i>0&&x<=ordinals[i-1]).Any())throw new ArgumentException("Invalid fixed roster or regular-start history.");
            if(!Validation.ValidId(id+".turn."+Math.Max(127,ordinals.Last()).ToString(System.Globalization.CultureInfo.InvariantCulture)))throw new ArgumentException("Encounter turn identity exceeds bounds.");
            Id=id;Origin=origin;InitialOrder=Array.AsReadOnly(ids);StartRevisions=Array.AsReadOnly(revisions);ObservedOrdinals=Array.AsReadOnly(ordinals);
            // The admission owns the live calendar cursor. Encounter history needs only the phase definition.
            RosterPhase = rosterPhase?.Epoch.ProcessedSlot > 0
                ? new EncounterRosterPhase(rosterPhase.Epoch.At(0), rosterPhase.FirstTurn, rosterPhase.FirstRound) : rosterPhase;
            if (rosterPhase != null && (rosterPhase.FirstTurn % InitialOrder.Count != 0
                || rosterPhase.FirstRound != rosterPhase.FirstTurn / InitialOrder.Count + 1L
                || !ordinals.Contains(rosterPhase.FirstTurn - 1) || !ordinals.Contains(rosterPhase.FirstTurn)
                || rosterPhase.Epoch.Origin != InitialStart(rosterPhase.FirstTurn)
                || !rosterPhase.Epoch.Order.Where(InitialOrder.Contains).SequenceEqual(InitialOrder)
                || rosterPhase.Epoch.Order.Count != InitialOrder.Count + 1))
                throw new ArgumentException("Invalid end-round roster transition.");
            if (inheritedPhase != null && (rosterPhase != null || !inheritedPhase.Owns(ordinals[0])
                || inheritedPhase.Start(ordinals[0]) != origin || !inheritedPhase.Epoch.Order.SequenceEqual(ids)
                || ordinals.Where((ordinal, i) => ordinal != ordinals[0] + i).Any()))
                throw new ArgumentException("Invalid inherited segment timing.");
            InheritedPhase = inheritedPhase == null ? null
                : new EncounterRosterPhase(inheritedPhase.Epoch.At(0), inheritedPhase.FirstTurn, inheritedPhase.FirstRound);
        }

        public FixedEncounterRecord Observe(long revision, int ordinal, EncounterRosterPhase phase = null)
            => new FixedEncounterRecord(Id, Origin, InitialOrder, StartRevisions.Append(revision),
                ObservedOrdinals.Append(ordinal), phase ?? RosterPhase, InheritedPhase);

        public FixedEncounterRecord BindRosterPhase(EncounterRosterPhase phase)
            => new FixedEncounterRecord(Id, Origin, InitialOrder, StartRevisions, ObservedOrdinals, phase);
        public FixedEncounterRecord BindInheritedPhase(EncounterRosterPhase phase)
            => new FixedEncounterRecord(Id, Origin, InitialOrder, StartRevisions, ObservedOrdinals, RosterPhase, phase);
    }
    public sealed class EncounterDashRecord
    {
        public long Revision { get; }
        public int TurnOrdinal { get; }
        public string ActorId { get; }
        public EncounterDashRecord(long revision,int turnOrdinal,string actor)
        {if(revision<1||turnOrdinal<0||!Validation.ValidId(actor))throw new ArgumentException("Invalid paid Dash.");Revision=revision;TurnOrdinal=turnOrdinal;ActorId=actor;}
    }
    public static class FixedEncounterValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.EncounterDashes==null||s.EncounterDashes.Length>128||s.EncounterDashes.Any(x=>x==null))throw new ArgumentException("Invalid encounter action collection.");
            if(s.SchemaVersion<Snapshot.EncounterSchema) {
                if(s.Encounter!=null||s.EncounterDashes.Length!=0)throw new ArgumentException("Fixed encounter requires schema7.");return;
            }
            var e=s.Encounter;
            if (s.SchemaVersion < Snapshot.ReinforcementSchema && EncounterHistory.All(s).Any(x => x.RosterPhase != null))
                throw new ArgumentException("Encounter roster phase requires schema 87.");
            if(s.SchemaVersion<Snapshot.CalendarCombatSchema&&EncounterHistory.All(s).Any(x=>x.Sparse))throw new ArgumentException("Sparse encounter cursor requires schema14.");
            bool world=s.SchemaVersion>=Snapshot.CalendarCombatSchema&&s.WorldSchedule!=null;
            if((world?s.InventoryCombat&&e==null:(e!=null)!=s.InventoryCombat)||s.SchemaVersion<Snapshot.SharedWorldSchema&&e==null&&s.EncounterDashes.Length!=0)throw new ArgumentException("Invalid encounter presence.");
            if(e!=null&&(e.Origin>s.RuleClock||e.StartRevisions.Any(r=>r>s.Revision)||e.Order.Any(id=>!s.Actors.Any(a=>a.Id==id))
                ||(s.InventoryCombat&&s.InventoryTurnActor!=e.CurrentActor))||s.EncounterDashes.Select(x=>x.Revision).Distinct().Count()!=s.EncounterDashes.Length
                ||s.EncounterDashes.Any(x=>x.Revision>s.Revision||!EncounterHistory.MatchesTurn(EncounterHistory.AtRevision(s,x.Revision),x.TurnOrdinal,x.ActorId)))
                throw new ArgumentException("Invalid encounter references.");
        }
    }
}
