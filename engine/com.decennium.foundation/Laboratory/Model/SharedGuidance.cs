#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static string GuidanceChoiceFailure(Snapshot s,Command c)
            => GuidanceChoiceConstraintV1(s,c)?.NativeCode;
        private static NativeCommandConstraintV1 GuidanceChoiceConstraintV1(Snapshot s,Command c)
        {
            const string source = "engine/com.decennium.foundation/Laboratory/Model/SharedGuidance.cs";
            if(c.Guidance==null)return null;
            if(!s.ConnectedClericCasting || !s.InventoryCombat || (c.Kind!=CommandKind.Hide&&c.Kind!=CommandKind.Search&&c.Kind!=CommandKind.StabilizeCompanion))
                return new NativeCommandConstraintV1("GuidanceConsumerUnsupported", source, 13);
            var effect=s.SpellEffects.SingleOrDefault(x=>x.Id==c.Guidance.EffectId);
            if(effect==null || !effect.Present || effect.SpellId!="guidance" || effect.TargetId!=c.Actor || effect.ExpiresAt<=s.RuleClock)
                return new NativeCommandConstraintV1("GuidanceBenefitUnavailable", source, 16);
            if(s.GuidanceUses.Length>=SpellCastingProfile.MaxGuidanceUses || !Validation.ValidId(c.Id+".medicine"))
                return new NativeCommandConstraintV1("CastingHistoryFull", source, 17);
            return null;
        }
        // Invoke only after every actual check prerequisite has passed, immediately before its d20.
        private static int ConsumeGuidance(Snapshot s,Command c,string checkId,GuidanceCheckKind kind)
        {
            if(c?.Guidance==null)return 0;
            string failure=GuidanceChoiceFailure(s,c);if(failure!=null)throw new ArgumentException(failure);
            var effect=s.SpellEffects.Single(x=>x.Id==c.Guidance.EffectId); uint before=s.RandomState;
            var die=DiceStream.Draw(before,4);s.RandomState=die.NextState;
            s.GuidanceUses=s.GuidanceUses.Append(new GuidanceUseRecord(effect.Id,c.Actor,c.Id,s.Revision+1,checkId,kind,s.RuleClock,
                die.Value+1,before,die.NextState,die.WordsConsumed)).ToArray();
            EndSpellEffect(s,effect,c.Id,s.Revision+1,s.RuleClock,SpellEffectEndReason.GuidanceConsumed);
            return die.Value+1;
        }
        private static int HistoricalGuidance(Snapshot s,string checkId)=>s.ConnectedClericCasting
            ?s.GuidanceUses.SingleOrDefault(x=>x.CheckId==checkId)?.D4??0:0;
    }
}
#endif
