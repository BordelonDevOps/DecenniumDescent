using System;
using System.IO;

namespace Decennium.Foundation
{
    internal static class SpellCastingCodec
    {
        internal static void Write(BinaryWriter w, Snapshot s)
        {
            Text(w,SpellCastingProfile.ApprovalResponse); Text(w,SpellSourceCatalog.SourceRevision);
            Rows(w,s.CastingStrain,x => { Text(w,x.ActorId); w.Write(x.Dissonance); Text(w,x.LastSpellId); w.Write(x.Refrain); w.Write(x.LastCastRevision); });
            Rows(w,s.SpellCasts,x => {
                Text(w,x.CommandId); w.Write(x.Revision); Text(w,x.ActorId); Text(w,x.TargetId); Text(w,x.SpellId);
                Text(w,x.SourceRevision); Text(w,x.ProcedureSha256); w.Write(x.KnownAcquiredRevision); w.Write(x.ClassLevel);
                w.Write(x.Rank); w.Write(x.Proficiency); w.Write(x.CastingModifier); w.Write(x.SpellDc); w.Write(x.StanceRevision);
                w.Write(x.FocusedDcElected); Text(w,x.FocusItemId); w.Write(x.FocusHeld); w.Write(x.AvailableHands); w.Write(x.WillingTarget);
                Turn(w,x.Turn); Time(w,x.At); w.Write(x.RpBefore); w.Write(x.BaseRp); w.Write(x.Surcharge); w.Write(x.RpAfter);
                w.Write(x.DissonanceBefore); w.Write(x.DissonanceAfter); w.Write(x.AppliedRefrain); Text(w,x.EffectId);
                w.Write(x.StableRecoveryD4); w.Write(x.RandomBefore); w.Write(x.RandomAfter); w.Write(x.WordsConsumed);
            });
            Rows(w,s.CastingActivities,x => { Text(w,x.CommandId); w.Write(x.Revision); Turn(w,x.Turn); Time(w,x.At); w.Write((int)x.Kind); });
            Rows(w,s.CastingTurnEnds,x => { Turn(w,x.Turn); Text(w,x.CauseId); w.Write(x.Revision); Time(w,x.At);
                w.Write(x.Before); w.Write(x.After); w.Write(x.MagicalActivity); w.Write(x.Grounding); w.Write(x.Proficiency); });
            Rows(w,s.SpellEffects,x => {
                Text(w,x.Id); Text(w,x.CastId); w.Write(x.CastRevision); Text(w,x.SpellId); Text(w,x.CasterId); Text(w,x.TargetId);
                Time(w,x.StartedAt); Time(w,x.ExpiresAt); w.Write((int)x.ExpiryKind); OptionalTurn(w,x.ExpiryTurn);
                w.Write(x.RequiresConcentration); Text(w,x.EndCauseId); w.Write(x.EndRevision); w.Write(x.EndedAt.HasValue);
                if(x.EndedAt.HasValue)Time(w,x.EndedAt.Value); w.Write((int)x.EndReason);
            });
            Rows(w,s.GuidanceUses,x => { Text(w,x.EffectId); Text(w,x.ActorId); Text(w,x.CommandId); w.Write(x.Revision); Text(w,x.CheckId);
                w.Write((int)x.CheckKind); Time(w,x.At); w.Write(x.D4); w.Write(x.RandomBefore); w.Write(x.RandomAfter); w.Write(x.WordsConsumed); });
            Rows(w,s.SpellSaves,x => {
                Text(w,x.Id); w.Write((int)x.Kind); Text(w,x.EffectId); Text(w,x.SubjectId); Text(w,x.CauseId); w.Write(x.Revision); Time(w,x.At);
                OptionalTurn(w,x.AttackerTurn); w.Write(x.Damage); w.Write(x.Dc); w.Write(x.Modifier); w.Write(x.First); w.Write(x.Second);
                w.Write(x.Natural); w.Write(x.Success); w.Write(x.RandomBefore); w.Write(x.RandomAfter); w.Write(x.WordsConsumed);
            });
            Rows(w,s.SanctuaryAdmissions,x => {
                Text(w,x.Id); Text(w,x.SaveId); Text(w,x.ActorId); Text(w,x.OriginalTargetId); Text(w,x.SourceCommandId); w.Write(x.SourceRevision);
                Text(w,x.SourceFingerprint); w.Write((int)x.Source); Text(w,x.OpportunityId); w.Write((int)x.Status);
                Text(w,x.ResolvedTargetId); Text(w,x.ResolutionCauseId); w.Write(x.ResolvedRevision);
            });
            Rows(w,s.DetectMagicFocuses,x => {
                Text(w,x.CommandId); w.Write(x.Revision); Text(w,x.ActorId); Text(w,x.DetectionEffectId); Text(w,x.ObservedEffectId);
                Text(w,x.ObservationId); Turn(w,x.Turn); Time(w,x.At); w.Write(x.SchoolWithheld); Text(w,x.BroadSchool);
            });
            Rows(w,s.ConsumableContamination,x => { Text(w,x.Id); Text(w,x.LotId); Text(w,x.OriginId); w.Write(x.OriginRevision);
                w.Write((int)x.Kind); Text(w,x.DestroyedByCastId); w.Write(x.DestroyedRevision); });
            CompanionStabilizationCodec.Write(w,s.CompanionStabilizations);
        }

        internal static void Read(BinaryReader r, Snapshot s)
        {
            if(Text(r)!=SpellCastingProfile.ApprovalResponse || Text(r)!=SpellSourceCatalog.SourceRevision)
                throw new InvalidDataException("Unsupported casting policy or source revision.");
            s.CastingStrain=Rows(r,1,() => new CastingStrainRecord(Text(r),r.ReadInt32(),Text(r),r.ReadInt32(),r.ReadInt64()));
            s.SpellCasts=Rows(r,SpellCastingProfile.MaxCasts,() => {
                string id=Text(r); long revision=r.ReadInt64(); string actor=Text(r),target=Text(r),spell=Text(r),source=Text(r),hash=Text(r);
                if(source!=SpellSourceCatalog.SourceRevision || hash!=SpellSourceCatalog.Get(spell)?.ProcedureSha256)
                    throw new InvalidDataException("Casting source binding differs from the retained procedure.");
                return new SpellCastRecord(id,revision,actor,target,spell,r.ReadInt64(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),
                    r.ReadInt32(),r.ReadInt64(),Bool(r),Text(r),Bool(r),r.ReadInt32(),Bool(r),Turn(r),Time(r),r.ReadInt32(),r.ReadInt32(),
                    r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),Text(r),r.ReadInt32(),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64());
            });
            s.CastingActivities=Rows(r,SpellCastingProfile.MaxActivities,() =>
                new CastingActivityRecord(Text(r),r.ReadInt64(),Turn(r),Time(r),(CastingActivityKind)r.ReadInt32()));
            s.CastingTurnEnds=Rows(r,SpellCastingProfile.MaxTurnEnds,() =>
                new CastingTurnEndRecord(Turn(r),Text(r),r.ReadInt64(),Time(r),r.ReadInt32(),r.ReadInt32(),Bool(r),Bool(r),r.ReadInt32()));
            s.SpellEffects=Rows(r,SpellCastingProfile.MaxEffects,() => {
                string id=Text(r),cast=Text(r); long revision=r.ReadInt64(); string spell=Text(r),caster=Text(r),target=Text(r);
                var start=Time(r); var expiry=Time(r); var kind=(SpellExpiryKind)r.ReadInt32(); var turn=OptionalTurn(r);
                bool concentration=Bool(r); string cause=Text(r); long endedRevision=r.ReadInt64(); RuleTime? ended=Bool(r)?Time(r):(RuleTime?)null;
                return new SpellEffectRecord(id,cast,revision,spell,caster,target,start,expiry,kind,turn,concentration,cause,endedRevision,ended,(SpellEffectEndReason)r.ReadInt32());
            });
            s.GuidanceUses=Rows(r,SpellCastingProfile.MaxGuidanceUses,() => new GuidanceUseRecord(Text(r),Text(r),Text(r),r.ReadInt64(),Text(r),
                (GuidanceCheckKind)r.ReadInt32(),Time(r),r.ReadInt32(),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64()));
            s.SpellSaves=Rows(r,SpellCastingProfile.MaxSaves,() => new SpellSaveRecord(Text(r),(SpellSaveKind)r.ReadInt32(),Text(r),Text(r),Text(r),
                r.ReadInt64(),Time(r),OptionalTurn(r),r.ReadInt64(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),
                Bool(r),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64()));
            s.SanctuaryAdmissions=Rows(r,SpellCastingProfile.MaxAdmissions,() => new SanctuaryAdmissionRecord(Text(r),Text(r),Text(r),Text(r),Text(r),
                r.ReadInt64(),Text(r),(SanctuaryAttackSource)r.ReadInt32(),Text(r),(SanctuaryAdmissionStatus)r.ReadInt32(),Text(r),Text(r),r.ReadInt64()));
            s.DetectMagicFocuses=Rows(r,SpellCastingProfile.MaxFocuses,() => new DetectMagicFocusRecord(Text(r),r.ReadInt64(),Text(r),Text(r),Text(r),
                Text(r),Turn(r),Time(r),Bool(r),Text(r)));
            s.ConsumableContamination=Rows(r,SpellCastingProfile.MaxContamination,() => new ConsumableContaminationRecord(Text(r),Text(r),Text(r),
                r.ReadInt64(),(ConsumableContaminationKind)r.ReadInt32(),Text(r),r.ReadInt64()));
            s.CompanionStabilizations=CompanionStabilizationCodec.Read(r);
        }
        private static void Rows<T>(BinaryWriter w,T[] rows,Action<T> write){w.Write(rows.Length);foreach(var row in rows)write(row);}
        private static T[] Rows<T>(BinaryReader r,int maximum,Func<T> read){var rows=new T[SnapshotCodec.ReadCount(r,maximum)];for(int i=0;i<rows.Length;i++)rows[i]=read();return rows;}
        private static void Text(BinaryWriter w,string value)=>SnapshotCodec.WriteText(w,value);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
        private static bool Bool(BinaryReader r)=>SnapshotCodec.ReadBool(r);
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Turn(BinaryWriter w,SpellTurnIdentity x){Text(w,x.ActorId);Text(w,x.EpochId);w.Write(x.LocalStart);w.Write(x.GlobalStart);w.Write(x.CarriedAdmissionRevision);}
        private static SpellTurnIdentity Turn(BinaryReader r)=>new SpellTurnIdentity(Text(r),Text(r),r.ReadInt64(),r.ReadInt64(),r.ReadInt64());
        private static void OptionalTurn(BinaryWriter w,SpellTurnIdentity x){w.Write(x!=null);if(x!=null)Turn(w,x);}
        private static SpellTurnIdentity OptionalTurn(BinaryReader r)=>Bool(r)?Turn(r):null;
    }
}
