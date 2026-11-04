using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ActorMovementCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.ActorMovement.Length);
            foreach(var m in s.ActorMovement.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                var b=Utf8.GetBytes(m.ActorId);w.Write(b.Length);w.Write(b);w.Write(m.BaseWalkingSpeed);w.Write(m.TurnOrdinal);w.Write(m.Spent);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            int count=r.ReadInt32();if(count<0||count>64)throw new InvalidDataException("Invalid movement count.");s.ActorMovement=new ActorMovementRecord[count];
            for(int i=0;i<count;i++) {
                int length=r.ReadInt32();if(length<1||length>96)throw new InvalidDataException("Invalid movement actor.");
                var b=r.ReadBytes(length);if(b.Length!=length)throw new EndOfStreamException();
                s.ActorMovement[i]=new ActorMovementRecord(Utf8.GetString(b),r.ReadInt32(),r.ReadInt32(),r.ReadInt64());
            }
        }
    }
}
