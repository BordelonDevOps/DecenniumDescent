using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static partial class OrdinaryMagicProfile
    {
        internal static void ValidateStrain(Snapshot s)
        {
            var current=new CastingStrainRecord(ClericRpProfile.Actor);
            var events=s.SpellCasts.Select(x=>(at:x.At,revision:x.Revision,cast:x,end:(MagicalSettlementRecord)null,rest:(ClericLongRestSettlementRecord)null,vent:(DivineInvocationRecord)null))
                .Concat(s.OrdinaryMagic.Settlements.Select(x=>(at:x.At,revision:x.Revision,cast:(SpellCastRecord)null,end:x,rest:(ClericLongRestSettlementRecord)null,vent:(DivineInvocationRecord)null)))
                .Concat(s.ClericLongRestSettlements.Select(x=>(at:x.At,revision:x.Revision,cast:(SpellCastRecord)null,end:(MagicalSettlementRecord)null,rest:x,vent:(DivineInvocationRecord)null)))
                .Concat(BishopProfile.Invocations(s).Select(x=>(at:x.At,revision:x.Revision,cast:(SpellCastRecord)null,end:(MagicalSettlementRecord)null,rest:(ClericLongRestSettlementRecord)null,vent:x)))
                .OrderBy(x=>x.at).ThenBy(x=>x.revision).ThenBy(x=>x.rest==null?0:1).ToArray();
            foreach(var e in events) {
                if(e.cast!=null) {
                    var cast=e.cast;
                    if(cast.DissonanceBefore!=current.Dissonance || cast.Rank>0 && current.RankedBlocked(cast.Proficiency,cast.CastingModifier)
                        || cast.Surcharge!=(cast.Rank==0?0:current.RankedSurcharge(cast.Proficiency,cast.CastingModifier)))
                        throw new ArgumentException("Invalid historical spell strain cost.");
                    current=current.BeginAdmittedCast(cast.SpellId,cast.Rank,cast.Revision,s.BishopEntry!=null);
                    if(current.Dissonance!=cast.DissonanceAfter || current.Refrain!=cast.AppliedRefrain)throw new ArgumentException("Invalid Refrain history.");
                } else if(e.vent!=null) {
                    if(e.vent.DissonanceBefore!=current.Dissonance)throw new ArgumentException("Invalid pre-Invocation Dissonance.");
                    current=current.ReduceAtSettledEnd(1);
                    if(e.vent.DissonanceAfter!=current.Dissonance)throw new ArgumentException("Invalid protected Conviction vent.");
                } else if(e.rest!=null) {
                    var rest=e.rest;
                    if(rest.DissonanceBefore!=current.Dissonance || rest.LastSpellId!=current.LastSpellId
                        || rest.Refrain!=current.Refrain || rest.LastCastRevision!=current.LastCastRevision)
                        throw new ArgumentException("Invalid pre-rest casting history.");
                    current=new CastingStrainRecord(current.ActorId,rest.Benefit==ClericLongRestBenefit.Eligible?0:current.Dissonance,
                        current.LastSpellId,current.Refrain,current.LastCastRevision);
                    if(rest.DissonanceAfter!=current.Dissonance)throw new ArgumentException("Invalid rest Dissonance settlement.");
                } else {
                    if(e.end.Before!=current.Dissonance)throw new ArgumentException("Invalid Dissonance before End.");
                    current=current.ReduceAtSettledEnd(e.end.Reduction);
                    if(e.end.After!=current.Dissonance)throw new ArgumentException("Invalid Dissonance after End.");
                }
            }
            var actual=s.CastingStrain[0];
            if(actual.Dissonance!=current.Dissonance || actual.LastSpellId!=current.LastSpellId || actual.Refrain!=current.Refrain
                || actual.LastCastRevision!=current.LastCastRevision)throw new ArgumentException("Casting cadence does not reconcile.");
        }
    }
}
