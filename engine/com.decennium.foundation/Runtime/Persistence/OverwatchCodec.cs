using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class OverwatchCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.OverwatchIntervals.Length);
            foreach(var x in s.OverwatchIntervals.OrderBy(x=>x.ActorId,StringComparer.Ordinal).ThenBy(x=>x.LastRegularStart)) {
                Text(w,x.ActorId);w.Write(x.LastRegularStart);w.Write((int)x.ShotStatus);
            }
            w.Write(s.OverwatchDesignations.Length);
            foreach(var x in s.OverwatchDesignations.OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.OwnerId);w.Write(x.LastRegularStart);w.Write(x.X0);w.Write(x.Y0);w.Write(x.CreatedRevision);
                w.Write((int)x.Status);w.Write(x.EndedRevision);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.OverwatchIntervals=new OverwatchIntervalRecord[Count(r,OverwatchValidation.MaxIntervals)];
            for(int i=0;i<s.OverwatchIntervals.Length;i++)s.OverwatchIntervals[i]=new OverwatchIntervalRecord(Text(r),r.ReadInt32(),(OverwatchShotStatus)r.ReadInt32());
            s.OverwatchDesignations=new OverwatchDesignationRecord[Count(r,OverwatchValidation.MaxDesignations)];
            for(int i=0;i<s.OverwatchDesignations.Length;i++)s.OverwatchDesignations[i]=new OverwatchDesignationRecord(Text(r),Text(r),r.ReadInt32(),
                r.ReadInt32(),r.ReadInt32(),r.ReadInt64(),(OverwatchDesignationStatus)r.ReadInt32(),r.ReadInt64());
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid Overwatch count.");return n;}
        private static void Text(BinaryWriter w,string x){byte[] b=Utf8.GetBytes(x);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
