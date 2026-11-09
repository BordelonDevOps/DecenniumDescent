using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class PortableEquipmentCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.PortableEquipment.Length);
            foreach(var x in s.PortableEquipment.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ProfileId);Text(w,x.OwnerId);Text(w,x.CustodianId);Text(w,x.ParentId);
                w.Write((int)x.Placement);w.Write((int)x.LinkKind);Text(w,x.LinkedId);w.Write((int)x.MassBasis);
                Optional(w,x.SourceWeightLb);Optional(w,x.OperationalWeightLb);Optional(w,x.PrintedLoad);
                Optional(w,x.CapacityPounds);Optional(w,x.CapacityCubicFeet);w.Write(x.Wearable);w.Write(x.Open);Text(w,x.FitRuleId);
                w.Write(x.FitMemberIds.Count);foreach(string id in x.FitMemberIds.OrderBy(v=>v,StringComparer.Ordinal))Text(w,id);
                w.Write(x.GroundX);w.Write(x.GroundY);
                if(s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema)w.Write(x.HeldHands);
            }
            w.Write(s.PortableHandling.Length);
            foreach(var x in s.PortableHandling.OrderBy(x=>x.Revision)) {
                Text(w,x.Id);w.Write(x.Revision);Text(w,x.ActorId);Text(w,x.ItemId);Text(w,x.FromParentId);Text(w,x.ToParentId);Text(w,x.RecipientId);
                w.Write((int)x.Operation);w.Write((int)x.Before);w.Write((int)x.After);Time(w,x.StartedAt);Time(w,x.EndedAt);w.Write(x.Tactical);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.PortableEquipment=new PortableEquipmentRecord[Count(r,PortableEquipmentValidation.MaxItems)];
            for(int i=0;i<s.PortableEquipment.Length;i++) {
                string id=Text(r),profile=Text(r),owner=Text(r),custodian=Text(r),parent=Text(r);
                var placement=(PortablePlacement)r.ReadInt32();var kind=(PortableLinkKind)r.ReadInt32();string linked=Text(r);var basis=(PortableMassBasis)r.ReadInt32();
                var source=Optional(r);var operational=Optional(r);var load=Optional(r);var pounds=Optional(r);var volume=Optional(r);
                bool wearable=Bool(r),open=Bool(r);string fit=Text(r);string[] members=new string[Count(r,32)];
                for(int j=0;j<members.Length;j++)members[j]=Text(r);
                int groundX=r.ReadInt32(),groundY=r.ReadInt32();int heldHands=s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema?r.ReadInt32():0;
                s.PortableEquipment[i]=new PortableEquipmentRecord(id,profile,owner,custodian,parent,placement,kind,linked,basis,source,operational,load,
                    pounds,volume,wearable,open,fit,members,groundX,groundY,heldHands);
            }
            s.PortableHandling=new PortableHandlingRecord[Count(r,PortableEquipmentValidation.MaxHandling)];
            for(int i=0;i<s.PortableHandling.Length;i++)s.PortableHandling[i]=new PortableHandlingRecord(Text(r),r.ReadInt64(),Text(r),Text(r),Text(r),Text(r),Text(r),
                (PortableOperation)r.ReadInt32(),(PortablePlacement)r.ReadInt32(),(PortablePlacement)r.ReadInt32(),Time(r),Time(r),Bool(r));
        }
        public static void WriteStorageProfiles(BinaryWriter w,Snapshot s)
        {
            w.Write(s.PortableStorageProfiles.Length);
            foreach(var x in s.PortableStorageProfiles.OrderBy(x=>x.ProfileId,StringComparer.Ordinal)) {
                Text(w,x.ProfileId);Text(w,x.QuantityUnitId);Optional(w,x.PackedVolumePerUnitCubicFeet);
                w.Write(x.AllowedContainedProfileIds.Count);
                foreach(string id in x.AllowedContainedProfileIds.OrderBy(v=>v,StringComparer.Ordinal))Text(w,id);
                w.Write(x.RequiresInstalledTemporaryCamp);
            }
        }
        public static void ReadStorageProfiles(BinaryReader r,Snapshot s)
        {
            s.PortableStorageProfiles=new PortableStorageProfileRecord[Count(r,PortableStorageProfileValidation.MaxProfiles)];
            for(int i=0;i<s.PortableStorageProfiles.Length;i++) {
                string profile=Text(r),unit=Text(r);var volume=Optional(r);string[] allowed=new string[Count(r,64)];
                for(int j=0;j<allowed.Length;j++)allowed[j]=Text(r);
                s.PortableStorageProfiles[i]=new PortableStorageProfileRecord(profile,unit,volume,allowed,Bool(r));
            }
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid portable record length.");return n;}
        private static void Text(BinaryWriter w,string value){byte[] b=Utf8.GetBytes(value);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,512);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid portable boolean.");return b==1;}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Quantity(BinaryWriter w,RuleQuantity q){w.Write(q.Numerator);w.Write(q.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
        private static void Optional(BinaryWriter w,RuleQuantity? q){w.Write(q.HasValue);if(q.HasValue)Quantity(w,q.Value);}
        private static RuleQuantity? Optional(BinaryReader r)=>Bool(r)?Quantity(r):(RuleQuantity?)null;
    }
}
