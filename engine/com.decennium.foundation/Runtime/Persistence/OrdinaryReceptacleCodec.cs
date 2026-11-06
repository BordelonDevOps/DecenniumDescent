using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class OrdinaryReceptacleCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string value){byte[] bytes=Utf8.GetBytes(value);w.Write(bytes.Length);w.Write(bytes);}
        private static string Text(BinaryReader r){int length=r.ReadInt32();if(length<0||length>512)throw new InvalidDataException("Invalid receptacle text length.");byte[] bytes=r.ReadBytes(length);if(bytes.Length!=length)throw new EndOfStreamException();return Utf8.GetString(bytes);}
        private static bool Bool(BinaryReader r){byte value=r.ReadByte();if(value>1)throw new InvalidDataException("Invalid receptacle boolean.");return value==1;}
        private static int Count(BinaryReader r,int maximum){int count=r.ReadInt32();if(count<0||count>maximum)throw new InvalidDataException("Invalid receptacle record count.");return count;}
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());

        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.OrdinaryReceptacleLocks.Length);
            foreach(var item in s.OrdinaryReceptacleLocks.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,item.Id);Text(w,item.ContainerId);Text(w,item.OwnerId);Text(w,item.KeyItemId);Text(w,item.ToolsItemId);w.Write(item.Locked);
            }
            w.Write(s.OrdinaryReceptacleAttempts.Length);
            foreach(var attempt in s.OrdinaryReceptacleAttempts.OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,attempt.Id);Text(w,attempt.LockId);Text(w,attempt.ActorId);Text(w,attempt.CredentialItemId);
                w.Write((int)attempt.Method);Time(w,attempt.StartedAt);w.Write(attempt.EndedAt.HasValue);
                if(attempt.EndedAt.HasValue)Time(w,attempt.EndedAt.Value);
                w.Write((int)attempt.Status);w.Write(attempt.Natural);w.Write(attempt.Modifier);w.Write(attempt.Tactical);w.Write(attempt.AutomaticFailure);
            }
        }

        public static void Read(BinaryReader r,Snapshot s)
        {
            s.OrdinaryReceptacleLocks=new OrdinaryReceptacleLockRecord[Count(r,OrdinaryReceptacleValidation.MaxLocks)];
            for(int i=0;i<s.OrdinaryReceptacleLocks.Length;i++)
                s.OrdinaryReceptacleLocks[i]=new OrdinaryReceptacleLockRecord(Text(r),Text(r),Text(r),Text(r),Text(r),Bool(r));
            s.OrdinaryReceptacleAttempts=new OrdinaryReceptacleAttemptRecord[Count(r,OrdinaryReceptacleValidation.MaxAttempts)];
            for(int i=0;i<s.OrdinaryReceptacleAttempts.Length;i++) {
                string id=Text(r),lockId=Text(r),actor=Text(r),credential=Text(r);var method=(OrdinaryReceptacleMethod)r.ReadInt32();
                RuleTime started=Time(r);RuleTime? ended=Bool(r)?Time(r):(RuleTime?)null;
                var status=(OrdinaryReceptacleAttemptStatus)r.ReadInt32();int natural=r.ReadInt32(),modifier=r.ReadInt32();
                bool tactical=Bool(r),automaticFailure=Bool(r);
                s.OrdinaryReceptacleAttempts[i]=new OrdinaryReceptacleAttemptRecord(id,lockId,actor,credential,method,started,ended,
                    status,natural,modifier,tactical,automaticFailure);
            }
        }
    }
}
