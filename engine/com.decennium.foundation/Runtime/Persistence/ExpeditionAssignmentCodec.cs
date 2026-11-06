using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ExpeditionAssignmentCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static void Text(BinaryWriter writer, string value)
        {
            byte[] bytes = Utf8.GetBytes(value);
            writer.Write(bytes.Length); writer.Write(bytes);
        }
        private static string Text(BinaryReader reader)
        {
            int length = reader.ReadInt32();
            if (length < 0 || length > 512) throw new InvalidDataException("Invalid expedition assignment text length.");
            byte[] bytes = reader.ReadBytes(length);
            if (bytes.Length != length) throw new EndOfStreamException();
            return Utf8.GetString(bytes);
        }
        private static RuleTime Time(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
        private static void Time(BinaryWriter writer, RuleTime value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }
        private static bool Bool(BinaryReader reader)
        { byte value=reader.ReadByte();if(value>1)throw new InvalidDataException("Invalid expedition assignment boolean.");return value==1; }
        private static void MiningSelection(BinaryWriter writer, MiningSelectionRequest value)
        {
            Text(writer,value.DepositVersionId);writer.Write((int)value.Ability);writer.Write(value.Hurried);
            string[] categories=value.CategoryIds;writer.Write(categories.Length);foreach(string id in categories)Text(writer,id);
            Text(writer,value.FailureVictimPreference);Text(writer,value.CriticalRecoveryPreference);
        }
        private static MiningSelectionRequest MiningSelection(BinaryReader reader)
        {
            string version=Text(reader);var ability=(MiningAbilityChoice)reader.ReadInt32();bool hurried=Bool(reader);
            int count=reader.ReadInt32();if(count<1||count>MiningValidation.MaxRecords)throw new InvalidDataException("Invalid assigned mining category count.");
            var categories=new string[count];for(int i=0;i<count;i++)categories[i]=Text(reader);
            string failure=Text(reader),critical=Text(reader);
            return new MiningSelectionRequest(version,categories,ability,hurried,failure,critical);
        }
        public static void Write(BinaryWriter writer, Snapshot state)
        {
            writer.Write(state.ExpeditionAssignments.Length);
            foreach (var x in state.ExpeditionAssignments.OrderBy(x => x.AssignedAt).ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(writer, x.Id); Text(writer, x.WorkerId); writer.Write((int)x.Procedure); Text(writer, x.TargetId);
                Text(writer, x.DestinationId); writer.Write(x.SiteX); writer.Write(x.SiteY); Time(writer, x.AssignedAt);
                Time(writer, x.UpdatedAt); writer.Write((int)x.Status); Text(writer, x.WorkId);
                if(state.SchemaVersion>=Snapshot.MiningExpeditionAssignmentSchema) {
                    writer.Write(x.MiningSelection!=null);
                    if(x.MiningSelection!=null)MiningSelection(writer,x.MiningSelection);
                }
            }
        }
        public static void Read(BinaryReader reader, Snapshot state)
        {
            int count = reader.ReadInt32();
            if (count < 0 || count > ExpeditionAssignmentValidation.MaxAssignments)
                throw new InvalidDataException("Invalid expedition assignment count.");
            state.ExpeditionAssignments = new ExpeditionWorkAssignmentRecord[count];
            for (int i = 0; i < count; i++)
            {
                string id = Text(reader), worker = Text(reader); var procedure = (ExpeditionWorkProcedure)reader.ReadInt32();
                string target = Text(reader), destination = Text(reader); int siteX = reader.ReadInt32(), siteY = reader.ReadInt32();
                RuleTime assigned = Time(reader), updated = Time(reader); var status = (ExpeditionAssignmentStatus)reader.ReadInt32();
                string work = Text(reader);
                MiningSelectionRequest selection=state.SchemaVersion>=Snapshot.MiningExpeditionAssignmentSchema&&Bool(reader)
                    ?MiningSelection(reader):null;
                state.ExpeditionAssignments[i] = new ExpeditionWorkAssignmentRecord(id, worker, procedure, target, destination,
                    siteX, siteY, assigned, updated, status, work, selection);
            }
        }
    }
}
