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
            bool petrified=s.SchemaVersion>=Snapshot.ConditionSchema
                &&TestOnlyClubAttackPolicy.ConditionsFor(s,target).View().Has(ConditionKind.Petrified);
            var record=new TypedDamageRecord(eventId,s.Revision+1,s.RuleClock,target,type,raw,
                CharacterAdvancementRules.ReduceIncomingDamage(s,target,successfulSaveHalf?raw/2:raw),successfulSaveHalf,resistance,immunity,petrified);
            if(s.FerryWraith!=null) {
                if(s.TypedDamage.Length>=TypedDamageRecord.MaxRecords||s.TypedDamage.Any(x=>x.EventId==eventId&&x.TargetId==target))
                    throw new InvalidOperationException("Typed damage history unavailable.");
                s.TypedDamage=s.TypedDamage.Append(record).ToArray();
            }
            return record;
        }
    }
}
#endif
