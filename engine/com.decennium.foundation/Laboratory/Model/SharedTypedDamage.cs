#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Resolve defenses once before life/temporary HP/concentration settlement.
    /// Pending knockout consumes the retained effective amount and never calls this again.</summary>
    public static class SharedTypedDamage
    {
        public static TypedDamageRecord Resolve(Snapshot s,string eventId,string target,string type,long raw,bool successfulSaveHalf=false)
        {
            if(s==null||!TypedDamageRecord.SupportedType(type)||!s.Lives.Any(x=>x.ActorId==target))
                throw new ArgumentException("Unsupported damage source or target.");
            var creature=s.Creatures.SingleOrDefault(x=>x.ActorId==target);
            string resistance=creature!=null&&creature.DamageResistances.Contains(type)?creature.SourceId:"";
            string immunity=creature!=null&&creature.DamageImmunities.Contains(type)?creature.SourceId:"";
            var ledger=s.SchemaVersion>=Snapshot.ConditionSchema?TestOnlyClubAttackPolicy.ConditionsFor(s,target):null;
            var view=ledger?.View();
            bool petrified=view?.Has(ConditionKind.Petrified)==true;
            var journal=s.Conditions.SingleOrDefault(x=>x.Target==target);
            // The additive Ferry path supplies condition poison immunity. Supported95-113
            // profiles retain their historical behavior and wire representation.
            if(s.FerryWraith!=null&&petrified&&type=="poison"&&immunity=="")immunity=TypedDamageRecord.PetrifiedPoisonSource;
            var record=new TypedDamageRecord(eventId,s.Revision+1,s.RuleClock,target,type,raw,
                CharacterAdvancementRules.ReduceIncomingDamage(s,target,successfulSaveHalf?raw/2:raw),successfulSaveHalf,resistance,immunity,petrified,
                s.FerryWraith==null?-1:journal.Operations.Count,s.FerryWraith==null?null:view.Sources(ConditionKind.Petrified)
                    .Distinct(StringComparer.Ordinal).OrderBy(x=>x,StringComparer.Ordinal),
                s.FerryWraith==null?"":journal.PolicyId,s.FerryWraith==null?default:journal.Origin,
                s.FerryWraith==null?default:ConditionHistory.Stamp(ledger.Now));
            if(s.FerryWraith!=null) {
                if(s.TypedDamage.Length>=TypedDamageRecord.MaxRecords||s.TypedDamage.Any(x=>x.EventId==eventId&&x.TargetId==target))
                    throw new InvalidOperationException("Typed damage history unavailable.");
                s.TypedDamage=s.TypedDamage.Append(record).ToArray();
            }
            return record;
        }
        public static void ValidateConditionHistory(Snapshot s)
        {
            foreach(var damage in s.TypedDamage) {
                var journal=s.Conditions.Single(x=>x.Target==damage.TargetId);
                if(damage.ConditionOperationCount<0||damage.ConditionOperationCount>journal.Operations.Count
                    ||damage.ConditionPolicyId!=journal.PolicyId||!damage.ConditionOrigin.Equals(journal.Origin))
                    throw new ArgumentException("Typed damage lacks its event-time condition prefix.");
                var prefix=new ConditionJournal(journal.PolicyId,journal.Target,journal.Origin,journal.Operations.Take(damage.ConditionOperationCount));
                var ledger=ConditionHistory.Restore(prefix).Ledger;
                var at=new EffectClockMarker(damage.ConditionEvaluation.Time,damage.ConditionEvaluation.Phase);
                if(ledger.Now.CompareTo(at)>0)throw new ArgumentException("Damage evaluation predates its retained condition prefix.");
                if(ledger.Now.CompareTo(at)<0)ledger=ledger.AdvanceTo(at).State;
                var view=ledger.View();
                if(view.Has(ConditionKind.Petrified)!=damage.Petrified
                    ||!view.Sources(ConditionKind.Petrified).Distinct(StringComparer.Ordinal).OrderBy(x=>x,StringComparer.Ordinal)
                        .SequenceEqual(damage.PetrifiedApplicationIds))
                    throw new ArgumentException("Typed damage condition protection differs from its event-time journal prefix.");
            }
        }
    }
}
#endif
