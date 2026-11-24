#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static string BishopDispelFailure(Snapshot s,Command c,out SpellEffectRecord effect)
            => BishopDispelConstraintV1(s,c,out effect)?.NativeCode;

        private static NativeCommandConstraintV1 BishopDispelConstraintV1(Snapshot s,Command c,out SpellEffectRecord effect)
        {
            effect=null;
            if(!BishopProfile.Earned(s)||c.Actor!=ClericRpProfile.Actor||c.SpellCast?.SpellId!=BishopProfile.Dispel)
                return new NativeCommandConstraintV1("DispelSourceUnsupported", "engine/com.decennium.foundation/Laboratory/Model/SharedBishopDispel.cs", 13);
            var detection=ActiveDetection(s,c.Actor);if(detection==null)return new NativeCommandConstraintV1("DetectMagicNotActive", "engine/com.decennium.foundation/Laboratory/Model/SharedBishopDispel.cs", 14);
            effect=s.SpellEffects.SingleOrDefault(x=>AuraPerceived(s,c.Actor,x)&&AuraObservationId(s,c.Actor,detection,x)==c.Target);
            if(effect==null)return new NativeCommandConstraintV1("AuraObservationUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedBishopDispel.cs", 16);
            string originalId=effect.CastId;
            var original=s.SpellCasts.SingleOrDefault(x=>x.CommandId==originalId);
            if(effect.SpellId!="guidance"||effect.CasterId!=c.Actor||original==null||original.ActorId!=c.Actor
                ||original.SpellId!="guidance"||original.Rank!=0||original.EffectId!=effect.Id||original.Revision!=effect.CastRevision
                ||!s.KnownSpells.Any(x=>x.ActorId==c.Actor&&x.SpellId=="guidance"&&x.MatchesSource()&&x.AcquiredRevision==original.KnownAcquiredRevision))
                return new NativeCommandConstraintV1("DispelRankKnowledgeUnsupported", "engine/com.decennium.foundation/Laboratory/Model/SharedBishopDispel.cs", 22);
            return s.BishopEntry.Dispels.Count>=128?new NativeCommandConstraintV1("DispelHistoryFull", "engine/com.decennium.foundation/Laboratory/Model/SharedBishopDispel.cs", 23):null;
        }
        private static void ResolveBishopDispel(Snapshot s,Command c)
        {
            string failure=BishopDispelFailure(s,c,out var effect);if(failure!=null)throw new ArgumentException(failure);
            var original=s.SpellCasts.Single(x=>x.CommandId==effect.CastId);var detection=ActiveDetection(s,c.Actor);
            EndSpellEffect(s,effect,c.Id,s.Revision+1,s.RuleClock,SpellEffectEndReason.Dispelled);
            var record=new BishopDispelRecord(c.Id,s.Revision+1,s.RuleClock,c.Target,detection.Id,effect.Id,original.CommandId,original.Revision);
            s.BishopEntry=s.BishopEntry.WithDispels(s.BishopEntry.Dispels.Append(record));
        }
    }
}
#endif
