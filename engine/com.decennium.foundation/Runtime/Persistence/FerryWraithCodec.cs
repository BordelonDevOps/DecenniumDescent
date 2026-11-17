using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class FerryWraithCodec
    {
        internal static void Write(BinaryWriter w,Snapshot state)
        {
            w.Write(state.Creatures.Length);
            foreach(var c in state.Creatures) {
                Text(w,c.ActorId);Text(w,c.SourceId);Text(w,c.SourceRevision);Text(w,c.SourcePath);Text(w,c.SourceSha256);
                foreach(int score in c.Abilities)w.Write(score);
                w.Write(c.ArmorClass);w.Write(c.MaximumHp);w.Write(c.WalkingSpeed);w.Write(c.ClassificationKnown);
                Names(w,c.Types);w.Write((int)c.LivingRecipient);Names(w,c.DamageResistances);Names(w,c.DamageImmunities);Names(w,c.ConditionImmunities);
            }
            var record=state.FerryWraith;
            Text(w,record.PredecessorFingerprint);w.Write(record.CompanionConsents);w.Write(record.DirectorAuthorizes);
            w.Write(record.Contacts.Count);
            foreach(var x in record.Contacts) {
                w.Write(x.ApproachRevision);w.Write(x.Revision);Text(w,x.CommandId);Time(w,x.At);Time(w,x.RequestedUntil);Text(w,x.Failure);
            }
            var a=record.Admission;w.Write(a!=null);
            if(a!=null) {
                Time(w,a.Epoch.Origin);w.Write(a.Epoch.ProcessedSlot);foreach(string actor in a.Epoch.Order)Text(w,actor);
                Text(w,a.PreviousPartyEpochId);w.Write(a.PriorDefenderLocalStart);
                foreach(var draw in a.Draws) {
                    Text(w,draw.ActorId);w.Write(draw.Natural);w.Write(draw.DexterityModifier);w.Write(draw.Bonus);
                    w.Write(draw.RandomBefore);w.Write(draw.RandomAfter);w.Write(draw.WordsConsumed);
                }
                foreach(var carry in a.PartyCarried) {
                    var x=carry.Interval;Text(w,x.ActorId);w.Write(x.LastStart);Quantity(w,x.MovementSpent);
                    w.Write(x.ActionSpent);w.Write(x.DashPaid);w.Write(x.ReactionAvailable);w.Write(x.Interactions);w.Write(carry.BonusActionAvailable);
                }
                var activity=a.CreatureActivity;Text(w,activity.CalendarId);Text(w,activity.ActorId);w.Write(activity.IntervalIndex);
                Quantity(w,activity.MovementSpent);w.Write((int)activity.Action);Text(w,activity.ActionReference);w.Write(activity.ActionReferenceRevision);
                Names(w,a.InitialReactionActors);
            }
            var rupture=record.Rupture;w.Write(rupture!=null);
            if(rupture!=null) {
                Text(w,rupture.CommandId);w.Write(rupture.Revision);Text(w,rupture.ActorId);w.Write(rupture.ActorX);w.Write(rupture.ActorY);
                Time(w,rupture.At);w.Write((int)rupture.ActionLedger);Text(w,rupture.ActionCalendarId);w.Write(rupture.ActionInterval);
                w.Write(rupture.InInitiative);Text(w,rupture.OriginalEpochId);Time(w,rupture.OriginalEpochOrigin);
                w.Write(rupture.OriginalCycle);Time(w,rupture.ExpiresAt);
            }
            w.Write(record.SuppressionExpiredRevision);
        }
        internal static void Read(BinaryReader r,Snapshot state)
        {
            var creatures=new CreatureActorRecord[SnapshotCodec.ReadCount(r,64)];
            for(int i=0;i<creatures.Length;i++) {
                string actor=Text(r),source=Text(r),revision=Text(r),path=Text(r),hash=Text(r);
                var abilities=Enumerable.Range(0,6).Select(_=>r.ReadInt32()).ToArray();
                int ac=r.ReadInt32();long hp=r.ReadInt64();int speed=r.ReadInt32();bool known=Flag(r);
                var types=Names(r);var living=(LivingRecipientQualification)r.ReadInt32();
                creatures[i]=new CreatureActorRecord(actor,source,revision,path,hash,abilities,ac,hp,speed,known,types,living,Names(r),Names(r),Names(r));
            }
            string predecessor=Text(r);bool consent=Flag(r),mandate=Flag(r);
            var contacts=new FerryWraithContact[SnapshotCodec.ReadCount(r,FerryWraithRecord.MaxContacts)];
            for(int i=0;i<contacts.Length;i++)contacts[i]=new FerryWraithContact(r.ReadInt64(),r.ReadInt64(),Text(r),Time(r),Time(r),Text(r));
            FerryWraithAdmission admission=null;
            if(Flag(r)) {
                var origin=Time(r);long slot=r.ReadInt64();
                var epoch=new WorldScheduleRecord(FerryWraithProfile.Calendar,origin,new[]{Text(r),Text(r),Text(r)},slot);
                string prior=Text(r);long marker=r.ReadInt64();var draws=new LaterInitiativeDraw[3];
                for(int i=0;i<draws.Length;i++)draws[i]=new LaterInitiativeDraw(Text(r),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt32());
                var carries=new ReinforcementCarry[2];
                for(int i=0;i<carries.Length;i++)carries[i]=new ReinforcementCarry(new WorldIntervalRecord(Text(r),r.ReadInt64(),Quantity(r),Flag(r),Flag(r),Flag(r),r.ReadInt32()),Flag(r));
                var activity=new WorldActivityIntervalRecord(Text(r),Text(r),r.ReadInt64(),Quantity(r),(WorldActionCommitment)r.ReadInt32(),Text(r),r.ReadInt64());
                admission=new FerryWraithAdmission(epoch,prior,marker,draws,carries,activity,Names(r));
            }
            SealRuptureRecord rupture=null;
            if(Flag(r))rupture=new SealRuptureRecord(Text(r),r.ReadInt64(),Text(r),r.ReadInt32(),r.ReadInt32(),Time(r),
                (SealActionLedger)r.ReadInt32(),Text(r),r.ReadInt64(),Flag(r),Text(r),Time(r),r.ReadInt64(),Time(r));
            state.Creatures=creatures;
            state.FerryWraith=new FerryWraithRecord(predecessor,consent,mandate,contacts,admission,rupture,r.ReadInt64());
        }
        private static void Names(BinaryWriter w,System.Collections.Generic.IReadOnlyList<string> rows)
        {w.Write(rows.Count);foreach(string value in rows)Text(w,value);}
        private static string[] Names(BinaryReader r)
        {var rows=new string[SnapshotCodec.ReadCount(r,32)];for(int i=0;i<rows.Length;i++)rows[i]=Text(r);return rows;}
        private static void Text(BinaryWriter w,string value)=>SnapshotCodec.WriteText(w,value);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
        private static bool Flag(BinaryReader r)=>SnapshotCodec.ReadBool(r);
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Quantity(BinaryWriter w,RuleQuantity value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
    }
}
