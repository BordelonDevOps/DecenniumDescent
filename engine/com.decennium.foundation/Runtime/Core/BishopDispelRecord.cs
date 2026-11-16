using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>One observed own-Guidance effect ended by the actual acquired spell. Detect alone grants no rank knowledge.</summary>
    public sealed class BishopDispelRecord
    {
        public string CommandId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public string ActorId => ClericRpProfile.Actor;
        public string ObservationId { get; }
        public string DetectionEffectId { get; }
        public string EndedEffectId { get; }
        public string OriginalCastId { get; }
        public long OriginalCastRevision { get; }
        public string OriginalCastingClass => "Cleric";
        public int OriginalGeneratingRank => 0;
        public string OriginalSourceRevision => SpellSourceCatalog.SourceRevision;
        public string OriginalProcedureSha256 => SpellSourceCatalog.Get("guidance").ProcedureSha256;
        public BishopDispelRecord(string command,long revision,RuleTime at,string observation,string detection,string ended,string originalCast,long originalRevision)
        {
            if(new[]{command,observation,detection,ended,originalCast}.Any(x=>!Validation.ValidId(x))
                ||!observation.StartsWith("aura.",StringComparison.Ordinal)||revision<1||originalRevision<1||originalRevision>=revision)
                throw new ArgumentException("Invalid observed own-Guidance Dispel evidence.");
            CommandId=command;Revision=revision;At=at;ObservationId=observation;DetectionEffectId=detection;EndedEffectId=ended;
            OriginalCastId=originalCast;OriginalCastRevision=originalRevision;
        }
    }
    public static partial class BishopProfile
    {
        internal static void ValidateDispels(Snapshot s)
        {
            var uses=s.BishopEntry.Dispels;
            if(uses.Count>128||uses.Select(x=>x.CommandId).Distinct().Count()!=uses.Count||uses.Select(x=>x.EndedEffectId).Distinct().Count()!=uses.Count
                ||!uses.Select(x=>x.Revision).SequenceEqual(uses.Select(x=>x.Revision).OrderBy(x=>x)))throw new ArgumentException("Invalid Dispel history coverage.");
            foreach(var use in uses) {
                var cast=s.SpellCasts.SingleOrDefault(x=>x.CommandId==use.CommandId);
                var effect=s.SpellEffects.SingleOrDefault(x=>x.Id==use.EndedEffectId);
                var original=s.SpellCasts.SingleOrDefault(x=>x.CommandId==use.OriginalCastId);
                var detection=s.SpellEffects.SingleOrDefault(x=>x.Id==use.DetectionEffectId);
                if(!Earned(s)||use.Revision<=Advancement(s).Revision||use.Revision>s.Revision||use.At>s.RuleClock
                    ||cast==null||cast.SpellId!=Dispel||cast.Revision!=use.Revision||cast.At!=use.At||cast.ActorId!=use.ActorId
                    ||cast.TargetId!=use.ObservationId||cast.Rank!=2||cast.ClassLevel!=3||cast.BaseRp!=3||cast.EffectId!=""||cast.WordsConsumed!=0
                    ||effect==null||effect.SpellId!="guidance"||effect.CastId!=use.OriginalCastId||effect.CasterId!=use.ActorId
                    ||effect.EndReason!=SpellEffectEndReason.Dispelled||effect.EndCauseId!=use.CommandId||effect.EndRevision!=use.Revision||effect.EndedAt!=use.At
                    ||original==null||original.Revision!=use.OriginalCastRevision||original.SpellId!="guidance"||original.ActorId!=use.ActorId
                    ||original.EffectId!=effect.Id||original.Rank!=0||original.Revision>=use.Revision
                    ||detection==null||detection.CasterId!=use.ActorId||detection.SpellId!="detect-magic"||detection.CastRevision>=use.Revision
                    ||detection.StartedAt>use.At||detection.ExpiresAt<=use.At||detection.EndRevision!=0&&detection.EndRevision<=use.Revision)
                    throw new ArgumentException("Unattributed current observation, original rank or Dispel ending.");
            }
            if(s.SpellCasts.Count(x=>x.SpellId==Dispel)!=uses.Count
                ||s.SpellEffects.Count(x=>x.EndReason==SpellEffectEndReason.Dispelled)!=uses.Count)
                throw new ArgumentException("Dispel effects and paid casting history differ.");
        }
    }
}
