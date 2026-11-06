using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class MiningCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static bool Bool(BinaryReader r)
        {byte value=r.ReadByte();if(value>1)throw new InvalidDataException("Invalid mining boolean.");return value==1;}
        private static void Text(BinaryWriter w,string value)
        {var bytes=Utf8.GetBytes(value);w.Write(bytes.Length);w.Write(bytes);}
        private static string Text(BinaryReader r)
        {int length=r.ReadInt32();if(length<0||length>512)throw new InvalidDataException("Invalid mining text length.");var bytes=r.ReadBytes(length);if(bytes.Length!=length)throw new EndOfStreamException();return Utf8.GetString(bytes);}
        private static int Count(BinaryReader r)
        {int count=r.ReadInt32();if(count<0||count>MiningValidation.MaxRecords)throw new InvalidDataException("Invalid mining record count.");return count;}
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void NullableTime(BinaryWriter w,RuleTime? value){w.Write(value.HasValue);if(value.HasValue)Time(w,value.Value);}
        private static RuleTime? NullableTime(BinaryReader r)=>Bool(r)?Time(r):(RuleTime?)null;
        private static void Quantity(BinaryWriter w,RuleQuantity value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
        private static void Ids(BinaryWriter w,string[] values){w.Write(values.Length);foreach(string value in values)Text(w,value);}
        private static string[] Ids(BinaryReader r,int minimum=0){int count=Count(r);if(count<minimum)throw new InvalidDataException("Invalid mining identity list.");var result=new string[count];for(int i=0;i<count;i++)result[i]=Text(r);return result;}

        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.MiningDeposits.Length);
            foreach(var x in s.MiningDeposits.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.VersionId);Text(w,x.SiteId);Text(w,x.OwnerId);w.Write(x.SiteX);w.Write(x.SiteY);
                Text(w,x.MiningToolsId);Text(w,x.PickId);Text(w,x.ReceiverId);Text(w,x.WorkSurfaceId);
                w.Write(x.ExactCheckDc.HasValue);if(x.ExactCheckDc.HasValue)w.Write(x.ExactCheckDc.Value);w.Write(x.HurryFeasible);
            }
            w.Write(s.MiningCategories.Length);
            foreach(var x in s.MiningCategories.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.DepositId);Text(w,x.MaterialId);w.Write(x.Tier);w.Write(x.Accessible);Ids(w,x.UnitIds);
            }
            w.Write(s.MiningUnits.Length);
            foreach(var x in s.MiningUnits.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.DepositId);Text(w,x.CategoryId);Quantity(w,x.MassPounds);Quantity(w,x.VolumeCubicFeet);
                w.Write(x.ValueCopper.HasValue);if(x.ValueCopper.HasValue)w.Write(x.ValueCopper.Value);
                w.Write((int)x.Condition);w.Write((int)x.Status);Text(w,x.ReceivedLotId);Text(w,x.ReceivedContainerId);
            }
            w.Write(s.MiningAttempts.Length);
            foreach(var x in s.MiningAttempts.OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.WorkerId);Text(w,x.DepositId);Text(w,x.DepositVersionId);w.Write(x.AccessibleCategoryCount);
                w.Write((int)x.Ability);w.Write(x.Hurried);Ids(w,x.SelectedCategoryIds);Ids(w,x.SelectedUnitIds);Text(w,x.FailureVictimPreference);
                Time(w,x.StartedAt);Time(w,x.UpdatedAt);w.Write(x.DurationSeconds);w.Write(x.SetupSeconds);w.Write(x.RemovalSeconds);w.Write(x.SortingSeconds);
                Time(w,x.WorkDone);NullableTime(w,x.CommittedAt);w.Write((int)x.Status);w.Write(x.AbilityModifier);w.Write(x.ProficiencyRank);
                w.Write(x.ProficiencyBonus);w.Write(x.CheckDc);NullableTime(w,x.ResolvedAt);NullableTime(w,x.ClosedAt);
                w.Write((int)x.Degree);w.Write((int)x.DiceSelection);w.Write(x.FirstDie);w.Write(x.SecondDie);w.Write(x.Natural);
                w.Write(x.CheckModifier);w.Write(x.D4Rolled);w.Write(x.DamageApplied);Text(w,x.AccidentDamageType);
                w.Write(x.WoundRoll);w.Write(x.InjuryRoll);w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.WordsConsumed);
                Text(w,x.CriticalRecoveryPreference);
            }
        }

        public static void Read(BinaryReader r,Snapshot s)
        {
            s.MiningDeposits=new MiningDepositRecord[Count(r)];
            for(int i=0;i<s.MiningDeposits.Length;i++) {
                string id=Text(r),version=Text(r),site=Text(r),owner=Text(r);int x=r.ReadInt32(),y=r.ReadInt32();
                string tools=Text(r),pick=Text(r),receiver=Text(r),surface=Text(r);int? dc=Bool(r)?r.ReadInt32():(int?)null;bool hurryFeasible=Bool(r);
                s.MiningDeposits[i]=new MiningDepositRecord(id,version,site,owner,x,y,tools,pick,receiver,surface,dc,hurryFeasible);
            }
            s.MiningCategories=new MiningCategoryRecord[Count(r)];
            for(int i=0;i<s.MiningCategories.Length;i++)s.MiningCategories[i]=new MiningCategoryRecord(Text(r),Text(r),Text(r),r.ReadInt32(),Bool(r),Ids(r,1));
            s.MiningUnits=new MiningMaterialUnitRecord[Count(r)];
            for(int i=0;i<s.MiningUnits.Length;i++) {
                string id=Text(r),deposit=Text(r),category=Text(r);var mass=Quantity(r);var volume=Quantity(r);
                long? value=Bool(r)?r.ReadInt64():(long?)null;
                s.MiningUnits[i]=new MiningMaterialUnitRecord(id,deposit,category,mass,volume,value,
                    (MiningUnitCondition)r.ReadInt32(),(MiningUnitStatus)r.ReadInt32(),Text(r),Text(r));
            }
            s.MiningAttempts=new MiningAttemptRecord[Count(r)];
            for(int i=0;i<s.MiningAttempts.Length;i++) {
                string id=Text(r),worker=Text(r),deposit=Text(r),version=Text(r);int accessible=r.ReadInt32();
                var ability=(MiningAbilityChoice)r.ReadInt32();bool hurried=Bool(r);var categories=Ids(r,1);var units=Ids(r,1);string preference=Text(r);
                RuleTime started=Time(r),updated=Time(r);int duration=r.ReadInt32(),setup=r.ReadInt32(),removal=r.ReadInt32(),sorting=r.ReadInt32();
                RuleTime work=Time(r);RuleTime? committed=NullableTime(r);var status=(MiningAttemptStatus)r.ReadInt32();
                int abilityModifier=r.ReadInt32(),rank=r.ReadInt32(),pb=r.ReadInt32(),dc=r.ReadInt32();
                RuleTime? resolved=NullableTime(r),closed=NullableTime(r);var degree=(MiningCheckDegree)r.ReadInt32();
                var selection=(MiningDiceSelection)r.ReadInt32();int first=r.ReadInt32(),second=r.ReadInt32(),natural=r.ReadInt32();
                int modifier=r.ReadInt32(),d4=r.ReadInt32();long damage=r.ReadInt64();string damageType=Text(r);
                int wound=r.ReadInt32(),injury=r.ReadInt32();uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();
                string recoveryPreference=Text(r);
                s.MiningAttempts[i]=new MiningAttemptRecord(id,worker,deposit,version,accessible,ability,hurried,categories,units,preference,
                    started,updated,duration,setup,removal,sorting,work,committed,status,abilityModifier,rank,pb,dc,resolved,closed,
                    degree,selection,first,second,natural,modifier,d4,damage,damageType,wound,injury,before,after,words,recoveryPreference);
            }
        }
    }

    internal static class MineralPreparationCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string value){var bytes=Utf8.GetBytes(value);w.Write(bytes.Length);w.Write(bytes);}
        private static string Text(BinaryReader r){int n=r.ReadInt32();if(n<0||n>512)throw new InvalidDataException("Invalid mineral-preparation text length.");
            var bytes=r.ReadBytes(n);if(bytes.Length!=n)throw new EndOfStreamException();return Utf8.GetString(bytes);}
        private static int Count(BinaryReader r){int n=r.ReadInt32();if(n<0||n>MineralPreparationValidation.MaxRecords)throw new InvalidDataException("Invalid mineral-preparation record count.");return n;}
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid mineral-preparation boolean.");return b==1;}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Quantity(BinaryWriter w,RuleQuantity q){w.Write(q.Numerator);w.Write(q.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());

        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.MineralPreparationProfiles.Length);
            foreach(var x in s.MineralPreparationProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.UnitId);Quantity(w,x.GangueWastePounds);Text(w,x.DressedItemProfileId);Text(w,x.GangueItemProfileId);
            }
            w.Write(s.MineralPreparationAttempts.Length);
            foreach(var x in s.MineralPreparationAttempts.OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.WorkerId);Text(w,x.ProfileId);Text(w,x.UnitId);Text(w,x.SourceLotId);Text(w,x.ReservationId);
                Quantity(w,x.InputMassPounds);Quantity(w,x.GangueWastePounds);Quantity(w,x.RetainedMassPounds);
                Time(w,x.StartedAt);Time(w,x.UpdatedAt);Time(w,x.WorkDone);w.Write((int)x.Status);Text(w,x.RetainedLotId);Text(w,x.GangueLotId);
            }
        }

        public static void Read(BinaryReader r,Snapshot s)
        {
            s.MineralPreparationProfiles=new MineralPreparationProfileRecord[Count(r)];
            for(int i=0;i<s.MineralPreparationProfiles.Length;i++)
                s.MineralPreparationProfiles[i]=new MineralPreparationProfileRecord(Text(r),Text(r),Quantity(r),Text(r),Text(r));
            s.MineralPreparationAttempts=new MineralPreparationAttemptRecord[Count(r)];
            for(int i=0;i<s.MineralPreparationAttempts.Length;i++)
                s.MineralPreparationAttempts[i]=new MineralPreparationAttemptRecord(Text(r),Text(r),Text(r),Text(r),Text(r),Text(r),
                    Quantity(r),Quantity(r),Quantity(r),Time(r),Time(r),Time(r),(MineralPreparationStatus)r.ReadInt32(),Text(r),Text(r));
        }
    }

    internal static class MiningToolCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string value){var bytes=Utf8.GetBytes(value);w.Write(bytes.Length);w.Write(bytes);}
        private static string Text(BinaryReader r){int n=r.ReadInt32();if(n<0||n>512)throw new InvalidDataException("Invalid mining-tool text length.");
            var bytes=r.ReadBytes(n);if(bytes.Length!=n)throw new EndOfStreamException();return Utf8.GetString(bytes);}
        private static int Count(BinaryReader r){int n=r.ReadInt32();if(n<0||n>MiningToolValidation.MaxRecords)throw new InvalidDataException("Invalid mining-tool record count.");return n;}
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid mining-tool boolean.");return b==1;}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());

        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.MiningToolCandidateProfiles.Length);
            foreach(var x in s.MiningToolCandidateProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.DepositId);Text(w,x.ToolItemId);Text(w,x.ToolItemProfileId);Text(w,x.StructureId);Text(w,x.StructureProfileId);
                Text(w,x.PreparationProfileId);Text(w,x.PreparationUnitId);Text(w,x.ReserveUnitId);
            }
            w.Write(s.MiningToolInstanceStates.Length);
            foreach(var x in s.MiningToolInstanceStates.OrderBy(x=>x.ProfileId,StringComparer.Ordinal)) {
                Text(w,x.ProfileId);Text(w,x.ToolItemId);w.Write(x.MissingMemberIds.Length);
                foreach(string member in x.MissingMemberIds)Text(w,member);
                w.Write(x.Suppressed);w.Write(x.Melded);
            }
            w.Write(s.MiningToolUses.Length);
            foreach(var x in s.MiningToolUses.OrderBy(x=>x.MiningAttemptId,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.MiningAttemptId);Text(w,x.ProfileId);Text(w,x.WorkerId);Text(w,x.PreparedUnitId);Text(w,x.ReservedUnitId);
                Time(w,x.ToolWorkDone);Time(w,x.PreparationWorkDone);w.Write(x.PreparationCompletedAt.HasValue);
                if(x.PreparationCompletedAt.HasValue)Time(w,x.PreparationCompletedAt.Value);
                Text(w,x.RetainedLotId);Text(w,x.GangueLotId);w.Write(x.CheckBonusApplied);
                Text(w,x.CriticalReserveAwardedUnitId);w.Write(x.DressedBenefitAwarded);
            }
        }

        public static void Read(BinaryReader r,Snapshot s)
        {
            s.MiningToolCandidateProfiles=new MiningToolCandidateProfileRecord[Count(r)];
            for(int i=0;i<s.MiningToolCandidateProfiles.Length;i++)s.MiningToolCandidateProfiles[i]=new MiningToolCandidateProfileRecord(
                Text(r),Text(r),Text(r),Text(r),Text(r),Text(r),Text(r),Text(r),Text(r));
            s.MiningToolInstanceStates=new MiningToolInstanceStateRecord[Count(r)];
            for(int i=0;i<s.MiningToolInstanceStates.Length;i++) {
                string profile=Text(r),item=Text(r);int count=r.ReadInt32();if(count<0||count>8)throw new InvalidDataException("Invalid mining-tool member count.");
                var missing=new string[count];for(int j=0;j<count;j++)missing[j]=Text(r);
                s.MiningToolInstanceStates[i]=new MiningToolInstanceStateRecord(profile,item,missing,Bool(r),Bool(r));
            }
            s.MiningToolUses=new MiningToolUseRecord[Count(r)];
            for(int i=0;i<s.MiningToolUses.Length;i++) {
                string id=Text(r),attempt=Text(r),profile=Text(r),worker=Text(r),prepared=Text(r),reserved=Text(r);
                RuleTime toolWork=Time(r),preparationWork=Time(r);RuleTime? completed=Bool(r)?Time(r):(RuleTime?)null;
                s.MiningToolUses[i]=new MiningToolUseRecord(id,attempt,profile,worker,prepared,reserved,toolWork,preparationWork,
                    completed,Text(r),Text(r),Bool(r),Text(r),Bool(r));
            }
        }
    }
}
