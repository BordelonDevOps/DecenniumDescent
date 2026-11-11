using System.IO;

namespace Decennium.Foundation
{
    internal static class LaterEncounterCodec
    {
        public static void Write(BinaryWriter writer, LaterEncounterRecord record)
        {
            var definition = record.Definition;
            void Text(string value) => SnapshotCodec.WriteText(writer, value);
            void Time(RuleTime value) { writer.Write(value.Numerator); writer.Write(value.Denominator); }

            foreach (string id in new[] { definition.EncounterId, definition.EpochId, definition.HeroId, definition.DefenderId,
                definition.DefenderClubId, definition.CharacterProfileId, definition.EngagementId, definition.TieDecisionId })
                Text(id);
            var first = record.FirstExit;
            writer.Write(first != null);
            if (first != null) {
                FixedEncounterCodec.WriteRecord(writer, first.Encounter, true);
                writer.Write(first.ClosedRevision);
                Time(first.ClosedAt);
                Text(first.Reason);
            }

            writer.Write(record.Interruptions.Count);
            foreach (var stop in record.Interruptions) {
                writer.Write(stop.ApproachRevision);
                writer.Write(stop.Revision);
                Text(stop.CommandId);
                Time(stop.At);
                Text(stop.Reason);
            }

            var entry = record.Entry;
            writer.Write(entry != null);
            if (entry == null) return;
            Time(entry.Epoch.Origin);
            writer.Write(entry.Epoch.ProcessedSlot);
            foreach (string actor in entry.Epoch.Order) Text(actor);
            writer.Write(entry.ApproachRevision);
            writer.Write(entry.ArrivalRevision);
            Text(entry.ArrivalCommandId);
            Time(entry.RequestedUntil);
            foreach (var draw in entry.Draws) {
                Text(draw.ActorId);
                writer.Write(draw.Natural);
                writer.Write(draw.DexterityModifier);
                writer.Write(draw.Bonus);
                writer.Write(draw.RandomBefore);
                writer.Write(draw.RandomAfter);
                writer.Write(draw.WordsConsumed);
            }
            var spent = entry.HeroExpenditureAtArrival;
            writer.Write(spent.LastStart);
            writer.Write(spent.MovementSpent.Numerator);
            writer.Write(spent.MovementSpent.Denominator);
            writer.Write(spent.ActionSpent);
            writer.Write(spent.DashPaid);
            writer.Write(spent.ReactionAvailable);
            writer.Write(spent.Interactions);
        }

        public static LaterEncounterRecord Read(BinaryReader reader)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
            bool Flag() => SnapshotCodec.ReadBool(reader);

            var definition = new LaterEncounterDefinition(Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text());
            var first = Flag() ? new ClosedEncounterRecord(FixedEncounterCodec.ReadRecord(reader, true),
                reader.ReadInt64(), Time(), Text()) : null;
            var stops = new LaterEncounterInterruption[SnapshotCodec.ReadCount(reader, Validation.MaxReceipts)];
            for (int i = 0; i < stops.Length; i++)
                stops[i] = new LaterEncounterInterruption(reader.ReadInt64(), reader.ReadInt64(), Text(), Time(), Text());
            if (!Flag()) return new LaterEncounterRecord(definition, first, interruptions: stops);
            var at = Time();
            long slot = reader.ReadInt64();
            var epoch = new WorldScheduleRecord(definition.EpochId, at, new[] { Text(), Text() }, slot);
            long approach = reader.ReadInt64(), arrival = reader.ReadInt64();
            string cause = Text();
            var requested = Time();
            var draws = new LaterInitiativeDraw[2];
            for (int i = 0; i < draws.Length; i++)
                draws[i] = new LaterInitiativeDraw(Text(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(),
                    reader.ReadUInt32(), reader.ReadUInt32(), reader.ReadInt32());
            var spent = new WorldIntervalRecord(definition.HeroId, reader.ReadInt64(),
                new RuleQuantity(reader.ReadInt64(), reader.ReadInt64()), Flag(), Flag(), Flag(), reader.ReadInt32());
            return new LaterEncounterRecord(definition, first,
                new LaterEncounterEntry(epoch, approach, arrival, cause, requested, draws, spent), stops);
        }
    }
}
