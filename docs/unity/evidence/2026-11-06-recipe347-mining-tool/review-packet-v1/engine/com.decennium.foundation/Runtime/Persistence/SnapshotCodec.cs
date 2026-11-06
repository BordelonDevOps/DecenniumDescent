using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    public sealed class SnapshotCodec
    {
        public const int LegacyMaxBytes = 1024 * 1024;
        public const int MaxBytes = 2 * 1024 * 1024;
        public const int ConditionMaxBytes = 6 * 1024 * 1024;
        private static int Limit(int schema) => schema >= Snapshot.ConditionSchema ? ConditionMaxBytes : schema >= Snapshot.ActorLifeSchema ? MaxBytes : LegacyMaxBytes;
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private const int Magic = 0x31464444; // DDF1, little endian. Checksum detects corruption, not tampering.
        public byte[] Encode(Snapshot state)
        {
            Validation.Snapshot(state);
            byte[] payload;
            using (var stream = new MemoryStream())
            using (var writer = new BinaryWriter(stream, Utf8, true))
            {
                writer.Write(Magic); writer.Write(state.SchemaVersion);
                WriteText(writer, state.ContentFingerprint); WriteText(writer, RandomV1.Algorithm);
                writer.Write(state.TestOnly); writer.Write(state.Revision); writer.Write(state.Clock); writer.Write(state.RandomState);
                writer.Write(state.Actors.Length);
                foreach (var a in state.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                { WriteText(writer, a.Id); writer.Write(a.X); writer.Write(a.Y); writer.Write(a.Tokens); }
                writer.Write(state.Objects.Length);
                foreach (var o in state.Objects.OrderBy(x => x.Id, StringComparer.Ordinal))
                { WriteText(writer, o.Id); writer.Write(o.X); writer.Write(o.Y); writer.Write(o.Opened); }
                writer.Write(state.Receipts.Length);
                foreach (var r in state.Receipts.OrderBy(x => x.Revision))
                { WriteText(writer, r.Principal); WriteText(writer, r.Id); WriteText(writer, r.Fingerprint); writer.Write(r.Revision); }
                if (state.SchemaVersion >= Snapshot.WorkSchema)
                {
                    writer.Write(state.RuleClock.Numerator); writer.Write(state.RuleClock.Denominator);
                    WriteText(writer, DiceStream.MappingVersion);
                    byte[] work = new WorkLedgerCodec().Encode(state.Work,state.SchemaVersion>=Snapshot.InventorySchema?2:1);
                    writer.Write(work.Length); writer.Write(work);
                }
                if (state.SchemaVersion >= Snapshot.CropSchema) CropRecordCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.InventorySchema) InventoryRecordCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.VesselSchema) WaterVesselCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.MovableVesselSchema) VesselHandlingCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.EncounterSchema) FixedEncounterCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.ActorLifeSchema) ActorLifeCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.ClubAttackSchema) ClubAttackCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.PostureSchema) ActorMovementCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.TacticalMovementSchema) TacticalMovementCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.ConditionSchema) {
                    writer.Write(state.Conditions.Length);
                    foreach (var journal in state.Conditions.OrderBy(x => x.Target, StringComparer.Ordinal)) {
                        byte[] component = new ConditionJournalCodec().Encode(journal); writer.Write(component.Length); writer.Write(component);
                    }
                }
                if (state.SchemaVersion >= Snapshot.SharedWorldSchema) {
                    writer.Write(state.ClosedEncounters.Length);
                    foreach (var closed in state.ClosedEncounters.OrderBy(x => x.Encounter.StartRevisions[0])) {
                        FixedEncounterCodec.WriteRecord(writer, closed.Encounter, state.SchemaVersion >= Snapshot.CalendarCombatSchema); writer.Write(closed.ClosedRevision);
                        writer.Write(closed.ClosedAt.Numerator); writer.Write(closed.ClosedAt.Denominator); WriteText(writer, closed.Reason);
                    }
                    WorldScheduleCodec.Write(writer, state);
                }
                if (state.SchemaVersion >= Snapshot.FormulaWorkSchema) FormulaWorkCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.CraftingConsequenceSchema) CraftingConsequenceCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.RepairWorkSchema) RepairWorkCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.ManufacturingSchema) ManufacturingCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.SupplyCacheSchema) SupplyCacheCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.PortableEquipmentSchema) PortableEquipmentCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.CharacterAdvancementSchema) CharacterAdvancementCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.RepeatingCrossbowSchema) RangedCombatCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.PeriodicRiderSchema) PeriodicRiderCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.OverwatchSchema) OverwatchCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.OverwatchExecutionSchema) OverwatchExecutionCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.SoldierInitialBuildSchema) CharacterAdvancementCodec.WriteInitialBuild(writer,state);
                if (state.SchemaVersion >= Snapshot.SoldierTacticalTechniquesSchema) SoldierTacticalFeatureCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.FishingTrapLegacySchema) FishingTrapCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.ExpeditionAssignmentSchema) ExpeditionAssignmentCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.OffCalendarActivitySchema) WorldActivityCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.HarvestSchema) HarvestCodec.Write(writer, state, state.SchemaVersion);
                if (state.SchemaVersion >= Snapshot.MiningSchema) MiningCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.ProspectingSchema) ProspectingCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.MiningAssaySchema) MiningAssayCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.DestructiveMiningAssaySchema) DestructiveMiningAssayCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.MineralPreparationSchema) MineralPreparationCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.MiningToolCandidateSchema) MiningToolCodec.Write(writer,state);
                writer.Flush(); payload = stream.ToArray();
            }
            if (payload.Length + 32 > Limit(state.SchemaVersion)) throw new InvalidDataException("Save exceeds schema size limit.");
            using (var hash = SHA256.Create()) return payload.Concat(hash.ComputeHash(payload)).ToArray();
        }
        public Snapshot Decode(byte[] data)
        {
            if (data == null || data.Length < 40 || data.Length > ConditionMaxBytes) throw new InvalidDataException("Invalid save length.");
            int length = data.Length - 32;
            using (var hash = SHA256.Create())
                if (!hash.ComputeHash(data, 0, length).SequenceEqual(data.Skip(length))) throw new InvalidDataException("Save checksum mismatch.");
            try
            {
                using (var stream = new MemoryStream(data, 0, length, false))
                using (var reader = new BinaryReader(stream, Utf8))
                {
                    if (reader.ReadInt32() != Magic) throw new InvalidDataException("Unsupported save format.");
                    int schema = reader.ReadInt32();
                    if (data.Length > Limit(schema)) throw new InvalidDataException("Save exceeds schema size limit.");
                    if (schema != Snapshot.MiningToolCandidateSchema && schema != Snapshot.MineralPreparationSchema && schema != Snapshot.MiningExpeditionAssignmentSchema && schema != Snapshot.DestructiveMiningAssaySchema && schema != Snapshot.MiningAssaySchema && schema != Snapshot.ProspectingSchema && schema != Snapshot.Schema && schema != Snapshot.WorkSchema && schema != Snapshot.CropSchema && schema != Snapshot.InventorySchema && schema != Snapshot.VesselSchema && schema != Snapshot.MovableVesselSchema && schema != Snapshot.EncounterSchema && schema != Snapshot.ActorLifeSchema && schema != Snapshot.ClubAttackSchema && schema != Snapshot.PostureSchema && schema != Snapshot.TacticalMovementSchema && schema != Snapshot.ConditionSchema && schema != Snapshot.SharedWorldSchema && schema != Snapshot.CalendarCombatSchema && schema != Snapshot.FormulaWorkSchema && schema != Snapshot.CraftingConsequenceSchema && schema != Snapshot.RepairWorkSchema && schema != Snapshot.ManufacturingSchema && schema != Snapshot.SupplyCacheSchema && schema != Snapshot.PortableEquipmentSchema && schema != Snapshot.CharacterAdvancementSchema && schema != Snapshot.RepeatingCrossbowSchema && schema != Snapshot.PeriodicRiderSchema && schema != Snapshot.SharedBonusActionSchema && schema != Snapshot.OverwatchSchema && schema != Snapshot.OverwatchExecutionSchema && schema != Snapshot.SoldierInitialLoadoutSchema && schema != Snapshot.SoldierInitialBuildSchema && schema != Snapshot.SoldierTacticalTechniquesSchema && schema != Snapshot.CharacterAdvancementHistorySchema && schema != Snapshot.TacticalAssessmentSchema && schema != Snapshot.CommandStepSchema && schema != Snapshot.SuppressionFireSchema && schema != Snapshot.DefensiveFormationSchema && schema != Snapshot.FishingTrapLegacySchema && schema != Snapshot.FishingTrapBaitSchema && schema != Snapshot.FishingTrapSchema && schema != Snapshot.FishingStockSchema && schema != Snapshot.ExpeditionAssignmentSchema && schema != Snapshot.OffCalendarActivitySchema && schema != Snapshot.HarvestSchema && schema != Snapshot.HarvestManifestSchema && schema != Snapshot.MiningSchema)
                        throw new InvalidDataException("Unsupported save schema.");
                    string fingerprint = ReadText(reader);
                    if (ReadText(reader) != RandomV1.Algorithm) throw new InvalidDataException("Unsupported RNG version.");
                    var s = new Snapshot { SchemaVersion = schema, ContentFingerprint = fingerprint, TestOnly = ReadBool(reader), Revision = reader.ReadInt64(),
                        Clock = reader.ReadInt64(), RandomState = reader.ReadUInt32() };
                    s.Actors = new ActorState[ReadCount(reader, 64)];
                    for (int i = 0; i < s.Actors.Length; i++) s.Actors[i] = new ActorState {
                        Id = ReadText(reader), X = reader.ReadInt32(), Y = reader.ReadInt32(), Tokens = reader.ReadInt32() };
                    s.Objects = new ObjectState[ReadCount(reader, 64)];
                    for (int i = 0; i < s.Objects.Length; i++) s.Objects[i] = new ObjectState {
                        Id = ReadText(reader), X = reader.ReadInt32(), Y = reader.ReadInt32(), Opened = ReadBool(reader) };
                    s.Receipts = new CommandReceipt[ReadCount(reader, Validation.MaxReceipts)];
                    for (int i = 0; i < s.Receipts.Length; i++) s.Receipts[i] = new CommandReceipt {
                        Principal = ReadText(reader), Id = ReadText(reader), Fingerprint = ReadText(reader), Revision = reader.ReadInt64() };
                    if (schema >= Snapshot.WorkSchema)
                    {
                        s.RuleClock = new RuleTime(reader.ReadInt64(), reader.ReadInt64());
                        if (ReadText(reader) != DiceStream.MappingVersion) throw new InvalidDataException("Unsupported dice mapping.");
                        int workLength = ReadCount(reader, WorkLedgerCodec.MaxBytes);
                        byte[] work = reader.ReadBytes(workLength);
                        if (work.Length != workLength) throw new EndOfStreamException();
                        s.Work = new WorkLedgerCodec().Decode(work,schema>=Snapshot.InventorySchema?2:1);
                    }
                    if (schema >= Snapshot.CropSchema) CropRecordCodec.Read(reader,s);
                    if (schema >= Snapshot.InventorySchema) InventoryRecordCodec.Read(reader,s);
                    if (schema >= Snapshot.VesselSchema) WaterVesselCodec.Read(reader,s);
                    if (schema >= Snapshot.MovableVesselSchema) VesselHandlingCodec.Read(reader,s);
                    if (schema >= Snapshot.EncounterSchema) FixedEncounterCodec.Read(reader,s);
                    if (schema >= Snapshot.ActorLifeSchema) ActorLifeCodec.Read(reader,s);
                    if (schema >= Snapshot.ClubAttackSchema) ClubAttackCodec.Read(reader,s);
                    if (schema >= Snapshot.PostureSchema) ActorMovementCodec.Read(reader,s);
                    if (schema >= Snapshot.TacticalMovementSchema) TacticalMovementCodec.Read(reader,s);
                    if (schema >= Snapshot.ConditionSchema) {
                        s.Conditions = new ConditionJournal[ReadCount(reader, Snapshot.MaxActors)];
                        for (int i = 0; i < s.Conditions.Length; i++) {
                            int count = ReadCount(reader, ConditionJournalCodec.MaxBytes); byte[] component = reader.ReadBytes(count);
                            if (component.Length != count) throw new EndOfStreamException();
                            s.Conditions[i] = new ConditionJournalCodec().Decode(component);
                        }
                    }
                    if (schema >= Snapshot.SharedWorldSchema) {
                        s.ClosedEncounters = new ClosedEncounterRecord[ReadCount(reader, EncounterHistory.MaxClosedEncounters)];
                        for (int i = 0; i < s.ClosedEncounters.Length; i++)
                            s.ClosedEncounters[i] = new ClosedEncounterRecord(FixedEncounterCodec.ReadRecord(reader, schema >= Snapshot.CalendarCombatSchema), reader.ReadInt64(),
                                new RuleTime(reader.ReadInt64(), reader.ReadInt64()), ReadText(reader));
                        WorldScheduleCodec.Read(reader, s);
                    }
                    if (schema >= Snapshot.FormulaWorkSchema) FormulaWorkCodec.Read(reader, s);
                    if (schema >= Snapshot.CraftingConsequenceSchema) CraftingConsequenceCodec.Read(reader, s);
                    if (schema >= Snapshot.RepairWorkSchema) RepairWorkCodec.Read(reader, s);
                    if(schema >= Snapshot.ManufacturingSchema)ManufacturingCodec.Read(reader,s);
                    if(schema >= Snapshot.SupplyCacheSchema)SupplyCacheCodec.Read(reader,s);
                    if(schema >= Snapshot.PortableEquipmentSchema)PortableEquipmentCodec.Read(reader,s);
                    if(schema >= Snapshot.CharacterAdvancementSchema)CharacterAdvancementCodec.Read(reader,s);
                    if(schema >= Snapshot.RepeatingCrossbowSchema)RangedCombatCodec.Read(reader,s);
                    if(schema >= Snapshot.PeriodicRiderSchema)PeriodicRiderCodec.Read(reader,s);
                    if(schema >= Snapshot.OverwatchSchema)OverwatchCodec.Read(reader,s);
                    if(schema >= Snapshot.OverwatchExecutionSchema)OverwatchExecutionCodec.Read(reader,s);
                    if(schema >= Snapshot.SoldierInitialBuildSchema)CharacterAdvancementCodec.ReadInitialBuild(reader,s);
                    if(schema >= Snapshot.SoldierTacticalTechniquesSchema)SoldierTacticalFeatureCodec.Read(reader,s);
                    if(schema >= Snapshot.FishingTrapLegacySchema)FishingTrapCodec.Read(reader,s,schema);
                    if(schema >= Snapshot.ExpeditionAssignmentSchema)ExpeditionAssignmentCodec.Read(reader,s);
                    if(schema >= Snapshot.OffCalendarActivitySchema)WorldActivityCodec.Read(reader,s);
                    if(schema >= Snapshot.HarvestSchema)HarvestCodec.Read(reader,s,schema);
                    if(schema >= Snapshot.MiningSchema)MiningCodec.Read(reader,s);
                    if(schema >= Snapshot.ProspectingSchema)ProspectingCodec.Read(reader,s);
                    if(schema >= Snapshot.MiningAssaySchema)MiningAssayCodec.Read(reader,s);
                    if(schema >= Snapshot.DestructiveMiningAssaySchema)DestructiveMiningAssayCodec.Read(reader,s);
                    if(schema >= Snapshot.MineralPreparationSchema)MineralPreparationCodec.Read(reader,s);
                    if(schema >= Snapshot.MiningToolCandidateSchema)MiningToolCodec.Read(reader,s);
                    if (stream.Position != length) throw new InvalidDataException("Unexpected trailing save data.");
                    Validation.Snapshot(s); return s;
                }
            }
            catch (Exception ex) when (ex is ArgumentException || ex is EndOfStreamException || ex is OverflowException)
            { throw new InvalidDataException("Malformed save.", ex); }
        }
        private static int ReadCount(BinaryReader reader, int maximum)
        { int n = reader.ReadInt32(); if (n < 0 || n > maximum) throw new InvalidDataException("Invalid collection length."); return n; }
        private static bool ReadBool(BinaryReader reader)
        { byte b = reader.ReadByte(); if (b > 1) throw new InvalidDataException("Invalid boolean."); return b == 1; }
        private static void WriteText(BinaryWriter writer, string value)
        { byte[] bytes = Utf8.GetBytes(value); writer.Write(bytes.Length); writer.Write(bytes); }
        private static string ReadText(BinaryReader reader)
        {
            int n = ReadCount(reader, 512); byte[] bytes = reader.ReadBytes(n);
            if (bytes.Length != n) throw new EndOfStreamException(); return Utf8.GetString(bytes);
        }
    }

    public interface IFileCommit
    {
        void Commit(string temporary, string destination, string backup);
    }
    public sealed class SameVolumeCommit : IFileCommit
    {
        public void Commit(string temporary, string destination, string backup)
        {
            if (File.Exists(destination)) File.Replace(temporary, destination, backup, true);
            else File.Move(temporary, destination);
        }
    }
    // Single writer, stable local path, completed-command boundaries only. No silent backup fallback.
    public sealed class FileSaveStore
    {
        private readonly SnapshotCodec codec = new SnapshotCodec();
        private readonly IFileCommit committer;
        public FileSaveStore() : this(new SameVolumeCommit()) { }
        public FileSaveStore(IFileCommit committer) { this.committer = committer ?? throw new ArgumentNullException(nameof(committer)); }
        public Snapshot Load(string path)
        {
            using (var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read))
            {
                if (stream.Length > SnapshotCodec.ConditionMaxBytes) throw new InvalidDataException("Save exceeds size limit.");
                using (var memory = new MemoryStream()) { stream.CopyTo(memory); return codec.Decode(memory.ToArray()); }
            }
        }
        public void Save(string path, Snapshot snapshot)
        {
            byte[] bytes = codec.Encode(snapshot);
            string full = Path.GetFullPath(path);
            Directory.CreateDirectory(Path.GetDirectoryName(full));
            // A corrupt current file must not replace the last-known-good backup.
            if (File.Exists(full))
            {
                Snapshot current = Load(full);
                if (current.SchemaVersion != snapshot.SchemaVersion || current.ContentFingerprint != snapshot.ContentFingerprint
                    || current.TestOnly != snapshot.TestOnly)
                    throw new InvalidDataException("Existing save has a different schema or content scope; use a separate destination.");
            }
            WriteAndCommit(full, bytes, full + ".bak");
        }
        // Explicit user recovery. Validate domain/content before writing; preserve both the
        // selected backup and the displaced primary. Caller must serialize all file operations.
        public string RecoverBackup(string path, Action<Snapshot> validate)
        {
            if (validate == null) throw new ArgumentNullException(nameof(validate));
            string full = Path.GetFullPath(path);
            Snapshot recovered = Load(full + ".bak");
            validate(recovered.Copy());
            string preserved = File.Exists(full) ? full + ".recovery-evidence-" + Guid.NewGuid().ToString("N") : null;
            WriteAndCommit(full, codec.Encode(recovered), preserved);
            return preserved;
        }
        private void WriteAndCommit(string full, byte[] bytes, string backup)
        {
            string temporary = full + ".tmp-" + Guid.NewGuid().ToString("N");
            try
            {
                using (var stream = new FileStream(temporary, FileMode.CreateNew, FileAccess.Write, FileShare.None))
                { stream.Write(bytes, 0, bytes.Length); stream.Flush(true); }
                Load(temporary);
                committer.Commit(temporary, full, backup);
            }
            finally { if (File.Exists(temporary)) File.Delete(temporary); }
        }
    }
}
