using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Schema72 append-only payload for the bounded recipe-347 TEST_ONLY module.</summary>
    internal static class Recipe347Codec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static int Count(BinaryReader r, int max)
        {
            int n = r.ReadInt32();
            if (n < 0 || n > max) throw new InvalidDataException("Invalid recipe-347 collection length.");
            return n;
        }
        private static void Text(BinaryWriter w, string value)
        {
            byte[] b = Utf8.GetBytes(value); w.Write(b.Length); w.Write(b);
        }
        private static string Text(BinaryReader r)
        {
            int n = Count(r, 96); byte[] b = r.ReadBytes(n);
            if (b.Length != n) throw new EndOfStreamException(); return Utf8.GetString(b);
        }
        private static bool Bool(BinaryReader r)
        {
            byte b = r.ReadByte(); if (b > 1) throw new InvalidDataException("Invalid recipe-347 boolean."); return b == 1;
        }
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void Strings(BinaryWriter w, System.Collections.Generic.IReadOnlyList<string> values)
        {
            w.Write(values.Count); foreach (string value in values) Text(w, value);
        }
        private static string[] Strings(BinaryReader r, int max)
        {
            var values = new string[Count(r, max)];
            for (int i = 0; i < values.Length; i++) values[i] = Text(r);
            return values;
        }
        private static void Progress(BinaryWriter w, ActiveWorkProgress work)
        {
            w.Write(work.Phases.Count); foreach (RuleTime phase in work.Phases) Time(w, phase);
            w.Write(work.CompletedPhases); Time(w, work.Partial); Time(w, work.Labor);
        }
        private static ActiveWorkProgress Progress(BinaryReader r)
        {
            var phases = new RuleTime[Count(r, ActiveWorkProgress.MaxPhases)];
            for (int i = 0; i < phases.Length; i++) phases[i] = Time(r);
            return new ActiveWorkProgress(phases, r.ReadInt32(), Time(r), Time(r));
        }

        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.Recipe347FormulaAccess.Length);
            foreach (var x in s.Recipe347FormulaAccess.OrderBy(x => x.Id, StringComparer.Ordinal))
            { Text(w, x.Id); Text(w, x.ActorId); Text(w, x.RecipeId); Text(w, x.AccessSourceId); }
            w.Write(s.Recipe347TradeSpecialties.Length);
            foreach (var x in s.Recipe347TradeSpecialties.OrderBy(x => x.Id, StringComparer.Ordinal))
            { Text(w, x.Id); Text(w, x.ActorId); Text(w, x.TradeId); Text(w, x.ScopeId); Text(w, x.SourceId); }
            w.Write(s.Recipe347Workshops.Length);
            foreach (var x in s.Recipe347Workshops.OrderBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.SiteId); w.Write(x.SiteX); w.Write(x.SiteY); Text(w, x.StationId);
                Text(w, x.StationStructureId); w.Write((int)x.StationKind); Strings(w, x.ImplementIds); w.Write(x.ProperWorkshop);
            }
            w.Write(s.Recipe347WorkOrders.Length);
            foreach (var x in s.Recipe347WorkOrders.OrderBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.WorkerId); Text(w, x.RecipeId); w.Write((int)x.Ability);
                Text(w, x.FormulaAccessId); Text(w, x.SpecialtyId); Text(w, x.WorkshopId);
                Text(w, x.BodyItemId); Text(w, x.BodyStructureId); Text(w, x.BodyLotId);
                Strings(w, x.ComponentLotIds); Strings(w, x.ImplementIds); w.Write((int)x.Status); Progress(w, x.Work);
                Time(w, x.StartedAt); Time(w, x.UpdatedAt); w.Write(x.CheckModifier); w.Write(x.First); w.Write(x.Second);
                w.Write(x.Natural); w.Write(x.Difficulty); w.Write(x.RandomBefore); w.Write(x.RandomAfter); w.Write(x.WordsConsumed);
                w.Write((int)x.Quality); w.Write((int)x.Choice); w.Write(x.MishapResult); w.Write(x.XpAward);
                Text(w, x.IncidentId); Text(w, x.OutputProvenanceId);
            }
            w.Write(s.Recipe347Outputs.Length);
            foreach (var x in s.Recipe347Outputs.OrderBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.OrderId); Text(w, x.ItemId); Text(w, x.StructureId); Time(w, x.CreatedAt);
                w.Write(x.Revision); w.Write((int)x.Quality); w.Write((int)x.Choice); w.Write(x.PreviousMaximumHp);
                w.Write(x.PreviousHp); w.Write(x.MaximumHp); w.Write(x.Hp);
            }
            w.Write(s.Recipe347MiningToolProfiles.Length);
            foreach (var x in s.Recipe347MiningToolProfiles.OrderBy(x => x.Id, StringComparer.Ordinal))
            { Text(w, x.Id); Text(w, x.ProvenanceId); Text(w, x.ItemId); Text(w, x.StructureId); w.Write(x.MaximumHp); }
            w.Write(s.Recipe347MiningToolUseEvidence.Length);
            foreach (var x in s.Recipe347MiningToolUseEvidence.OrderBy(x => x.Id, StringComparer.Ordinal))
            {
                Text(w, x.Id); Text(w, x.AttemptId); Text(w, x.ProfileId); Text(w, x.ItemId); Text(w, x.DepositId);
                Text(w, x.DepositVersionId); Text(w, x.WorkerId); Time(w, x.CapturedAt); w.Write(x.WorkerX); w.Write(x.WorkerY);
                Text(w, x.OwnerId); Text(w, x.CustodianId); w.Write((int)x.Placement); w.Write(x.GroundX); w.Write(x.GroundY);
                w.Write(x.StructureHp); w.Write(x.StructureMaximumHp); Text(w, x.StructureLocationId); Text(w, x.WorkSurfaceId);
                w.Write(x.WorkSurfaceBroken); Text(w, x.ReceiverId); w.Write(x.ReceiverOpen); w.Write(x.AvailableHands);
                Strings(w, x.SelectedUnitIds);
            }
            w.Write(s.Recipe347MiningToolWorkSegments.Length);
            foreach (var x in s.Recipe347MiningToolWorkSegments.OrderBy(x => x.AttemptId, StringComparer.Ordinal).ThenBy(x => x.Start))
            { Text(w, x.AttemptId); Time(w, x.Start); Time(w, x.End); }
        }

        public static void Read(BinaryReader r, Snapshot s)
        {
            s.Recipe347FormulaAccess = new TestOnlyRecipe347FormulaAccessRecord[Count(r, Recipe347Validation.MaxRecords)];
            for (int i = 0; i < s.Recipe347FormulaAccess.Length; i++)
                s.Recipe347FormulaAccess[i] = new TestOnlyRecipe347FormulaAccessRecord(Text(r), Text(r), Text(r), Text(r));
            s.Recipe347TradeSpecialties = new TestOnlyTradeSpecialtyRecord[Count(r, Recipe347Validation.MaxRecords)];
            for (int i = 0; i < s.Recipe347TradeSpecialties.Length; i++)
                s.Recipe347TradeSpecialties[i] = new TestOnlyTradeSpecialtyRecord(Text(r), Text(r), Text(r), Text(r), Text(r));
            s.Recipe347Workshops = new TestOnlyRecipe347WorkshopRecord[Count(r, Recipe347Validation.MaxRecords)];
            for (int i = 0; i < s.Recipe347Workshops.Length; i++)
                s.Recipe347Workshops[i] = new TestOnlyRecipe347WorkshopRecord(Text(r), Text(r), r.ReadInt32(), r.ReadInt32(),
                    Text(r), Text(r), (Recipe347StationKind)r.ReadInt32(), Strings(r, 16), Bool(r));
            s.Recipe347WorkOrders = new Recipe347WorkOrderRecord[Count(r, Recipe347Validation.MaxRecords)];
            for (int i = 0; i < s.Recipe347WorkOrders.Length; i++)
            {
                string id = Text(r), worker = Text(r), recipe = Text(r); var ability = (CharacterAbility)r.ReadInt32();
                string access = Text(r), specialty = Text(r), workshop = Text(r), bodyItem = Text(r), bodyStructure = Text(r), bodyLot = Text(r);
                string[] components = Strings(r, 8), implements = Strings(r, 16); var status = (Recipe347OrderStatus)r.ReadInt32();
                var work = Progress(r); var started = Time(r); var updated = Time(r); int modifier = r.ReadInt32(), first = r.ReadInt32(), second = r.ReadInt32();
                int natural = r.ReadInt32(), difficulty = r.ReadInt32(); uint before = r.ReadUInt32(), after = r.ReadUInt32(); long words = r.ReadInt64();
                var quality = (CraftQuality)r.ReadInt32(); var choice = (CraftQualityChoice)r.ReadInt32(); int mishap = r.ReadInt32(), xp = r.ReadInt32();
                string incident = Text(r), output = Text(r);
                s.Recipe347WorkOrders[i] = new Recipe347WorkOrderRecord(id, worker, recipe, ability, access, specialty, workshop,
                    bodyItem, bodyStructure, bodyLot, components, implements, status, work, started, updated, modifier,
                    first, second, natural, difficulty, before, after, words, quality, choice, mishap, xp, incident, output);
            }
            s.Recipe347Outputs = new Recipe347OutputProvenanceRecord[Count(r, Recipe347Validation.MaxRecords)];
            for (int i = 0; i < s.Recipe347Outputs.Length; i++)
                s.Recipe347Outputs[i] = new Recipe347OutputProvenanceRecord(Text(r), Text(r), Text(r), Text(r), Time(r), r.ReadInt64(),
                    (CraftQuality)r.ReadInt32(), (CraftQualityChoice)r.ReadInt32(), r.ReadInt64(), r.ReadInt64(), r.ReadInt64(), r.ReadInt64());
            s.Recipe347MiningToolProfiles = new Recipe347MiningToolProfileRecord[Count(r, Recipe347Validation.MaxRecords)];
            for (int i = 0; i < s.Recipe347MiningToolProfiles.Length; i++)
                s.Recipe347MiningToolProfiles[i] = new Recipe347MiningToolProfileRecord(Text(r), Text(r), Text(r), Text(r), r.ReadInt64());
            s.Recipe347MiningToolUseEvidence = new Recipe347MiningToolUseEvidenceRecord[Count(r, Recipe347Validation.MaxRecords)];
            for (int i = 0; i < s.Recipe347MiningToolUseEvidence.Length; i++)
                s.Recipe347MiningToolUseEvidence[i] = new Recipe347MiningToolUseEvidenceRecord(Text(r), Text(r), Text(r), Text(r), Text(r),
                    Text(r), Text(r), Time(r), r.ReadInt32(), r.ReadInt32(), Text(r), Text(r), (PortablePlacement)r.ReadInt32(),
                    r.ReadInt32(), r.ReadInt32(), r.ReadInt64(), r.ReadInt64(), Text(r), Text(r), Bool(r), Text(r), Bool(r),
                    r.ReadInt32(), Strings(r, 128));
            s.Recipe347MiningToolWorkSegments = new Recipe347MiningToolWorkSegmentRecord[Count(r, Recipe347Validation.MaxRecords)];
            for (int i = 0; i < s.Recipe347MiningToolWorkSegments.Length; i++)
                s.Recipe347MiningToolWorkSegments[i] = new Recipe347MiningToolWorkSegmentRecord(Text(r), Time(r), Time(r));
        }
    }
}
