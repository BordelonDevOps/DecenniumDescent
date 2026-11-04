using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class OverwatchExecutionCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.OverwatchOffers.Length);
            foreach(var x in s.OverwatchOffers.OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.MoveId);Text(w,x.OwnerId);Text(w,x.TargetId);Text(w,x.DesignationId);w.Write(x.CreatedRevision);
                w.Write(x.SourceAppliedRevision);w.Write((int)x.Status);w.Write(x.ResolvedRevision);Text(w,x.AttackId);
            }
            w.Write(s.OverwatchRiderChoices.Length);
            foreach(var x in s.OverwatchRiderChoices.OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.OfferId);Text(w,x.AttackId);Text(w,x.OwnerId);Text(w,x.TargetId);w.Write(x.CreatedRevision);
                w.Write((int)x.Status);w.Write((int)x.Choice);w.Write(x.ResolvedRevision);w.Write(x.ExpiresAfterTurnOrdinal);
                w.Write(x.SaveNatural);w.Write(x.SaveModifier);w.Write(x.SaveDc);w.Write(x.SaveTotal);w.Write(x.SaveSucceeded);
                w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.RandomWordsConsumed);
                w.Write(x.FromX);w.Write(x.FromY);w.Write(x.ToX);w.Write(x.ToY);w.Write(x.MovedFeet);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.OverwatchOffers=new OverwatchOfferRecord[Count(r,OverwatchExecutionValidation.MaxOffers)];
            for(int i=0;i<s.OverwatchOffers.Length;i++) {
                string id=Text(r),move=Text(r),owner=Text(r),target=Text(r),zone=Text(r);long created=r.ReadInt64(),applied=r.ReadInt64();
                var status=(OverwatchOfferStatus)r.ReadInt32();long resolved=r.ReadInt64();string attack=Text(r);
                s.OverwatchOffers[i]=new OverwatchOfferRecord(id,move,owner,target,zone,created,applied,status,resolved,attack);
            }
            s.OverwatchRiderChoices=new OverwatchRiderChoiceRecord[Count(r,OverwatchExecutionValidation.MaxRiderChoices)];
            for(int i=0;i<s.OverwatchRiderChoices.Length;i++) {
                string id=Text(r),offer=Text(r),attack=Text(r),owner=Text(r),target=Text(r);long created=r.ReadInt64();
                var status=(OverwatchRiderChoiceStatus)r.ReadInt32();var choice=(OverwatchRider)r.ReadInt32();long resolved=r.ReadInt64();
                int expires=r.ReadInt32(),natural=r.ReadInt32(),modifier=r.ReadInt32(),dc=r.ReadInt32();long total=r.ReadInt64();bool success=Bool(r);
                uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();int fromX=r.ReadInt32(),fromY=r.ReadInt32(),toX=r.ReadInt32(),toY=r.ReadInt32(),moved=r.ReadInt32();
                s.OverwatchRiderChoices[i]=new OverwatchRiderChoiceRecord(id,offer,attack,owner,target,created,status,choice,resolved,expires,
                    natural,modifier,dc,total,success,before,after,words,fromX,fromY,toX,toY,moved);
            }
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid Overwatch execution count.");return n;}
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid Overwatch execution flag.");return b==1;}
        private static void Text(BinaryWriter w,string x){byte[] b=Utf8.GetBytes(x);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
