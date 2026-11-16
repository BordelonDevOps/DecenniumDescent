using System.IO;

namespace Decennium.Foundation
{
    internal static class PostRecoveryEncounterCodec
    {
        internal static void Write(BinaryWriter w, PostRecoveryEncounterRecord record)
        {
            w.Write(record.Definition.CompanionConsents); w.Write(record.Definition.DirectorAuthorizes);
            w.Write(record.Contacts.Count);
            foreach (var x in record.Contacts) {
                w.Write(x.ApproachRevision); w.Write(x.Revision); Text(w,x.CommandId); Time(w,x.At);
                Time(w,x.RequestedUntil); Text(w,x.Failure);
            }
            var a = record.Admission; w.Write(a != null); if (a == null) return;
            Time(w,a.Epoch.Origin); w.Write(a.Epoch.ProcessedSlot);
            foreach (string actor in a.Epoch.Order) Text(w,actor);
            Text(w,a.PreviousPartyEpochId); w.Write(a.PriorDefenderLocalStart);
            foreach (var draw in a.Draws) {
                Text(w,draw.ActorId); w.Write(draw.Natural); w.Write(draw.DexterityModifier); w.Write(draw.Bonus);
                w.Write(draw.RandomBefore); w.Write(draw.RandomAfter); w.Write(draw.WordsConsumed);
            }
            foreach (var carry in a.PartyCarried) {
                var x=carry.Interval; Text(w,x.ActorId); w.Write(x.LastStart); Quantity(w,x.MovementSpent);
                w.Write(x.ActionSpent); w.Write(x.DashPaid); w.Write(x.ReactionAvailable); w.Write(x.Interactions);
                w.Write(carry.BonusActionAvailable);
            }
            var activity=a.DefenderActivity;
            Text(w,activity.CalendarId); Text(w,activity.ActorId); w.Write(activity.IntervalIndex);
            Quantity(w,activity.MovementSpent); w.Write((int)activity.Action); Text(w,activity.ActionReference);
            w.Write(activity.ActionReferenceRevision);
            w.Write(a.InitialReactionActors.Count); foreach (string actor in a.InitialReactionActors) Text(w,actor);
        }

        internal static PostRecoveryEncounterRecord Read(BinaryReader r)
        {
            var definition=new PostRecoveryEncounterDefinition(Flag(r),Flag(r));
            var contacts=new PostRecoveryContact[SnapshotCodec.ReadCount(r,PostRecoveryEncounterRecord.MaxContacts)];
            for(int i=0;i<contacts.Length;i++) contacts[i]=new PostRecoveryContact(r.ReadInt64(),r.ReadInt64(),Text(r),Time(r),Time(r),Text(r));
            if(!Flag(r))return new PostRecoveryEncounterRecord(definition,contacts);
            var origin=Time(r); long slot=r.ReadInt64();
            var epoch=new WorldScheduleRecord(PostRecoveryEncounterDefinition.Calendar,origin,new[]{Text(r),Text(r),Text(r)},slot);
            string prior=Text(r);long marker=r.ReadInt64();
            var draws=new LaterInitiativeDraw[3];
            for(int i=0;i<draws.Length;i++)draws[i]=new LaterInitiativeDraw(Text(r),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),
                r.ReadUInt32(),r.ReadUInt32(),r.ReadInt32());
            var carried=new ReinforcementCarry[2];
            for(int i=0;i<carried.Length;i++)carried[i]=new ReinforcementCarry(new WorldIntervalRecord(Text(r),r.ReadInt64(),
                Quantity(r),Flag(r),Flag(r),Flag(r),r.ReadInt32()),Flag(r));
            var activity=new WorldActivityIntervalRecord(Text(r),Text(r),r.ReadInt64(),Quantity(r),
                (WorldActionCommitment)r.ReadInt32(),Text(r),r.ReadInt64());
            var reactions=new string[SnapshotCodec.ReadCount(r,3)];
            for(int i=0;i<reactions.Length;i++)reactions[i]=Text(r);
            return new PostRecoveryEncounterRecord(definition,contacts,new PostRecoveryAdmission(epoch,prior,marker,draws,carried,activity,reactions));
        }

        private static void Text(BinaryWriter w,string value)=>SnapshotCodec.WriteText(w,value);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
        private static bool Flag(BinaryReader r)=>SnapshotCodec.ReadBool(r);
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Quantity(BinaryWriter w,RuleQuantity value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
    }
}
