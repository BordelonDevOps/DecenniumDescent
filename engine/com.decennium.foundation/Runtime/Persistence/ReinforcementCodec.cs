using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class ReinforcementCodec
    {
        public static void Write(BinaryWriter writer, ReinforcementRecord record)
        {
            void Text(string value) => SnapshotCodec.WriteText(writer, value);
            void Time(RuleTime value) { writer.Write(value.Numerator); writer.Write(value.Denominator); }
            void Quantity(RuleQuantity value) { writer.Write(value.Numerator); writer.Write(value.Denominator); }

            var definition = record.Definition;
            foreach (string id in new[] { definition.Id, definition.EncounterId, definition.EpochId, definition.CompanionId,
                definition.AllyId, definition.ControllerId, definition.ParticipationMandateId, definition.AlliedSideId,
                definition.PlayerTieChoiceId, definition.DirectorTieChoiceId })
                Text(id);
            writer.Write(record.Events.Count);
            foreach (var entry in record.Events) {
                writer.Write((int)entry.Kind);
                writer.Write(entry.Revision);
                Text(entry.CommandId);
                Time(entry.At);
                Text(entry.Reason);
                Quantity(entry.Distance);
            }

            var admission = record.Admission;
            writer.Write(admission != null);
            if (admission == null) return;
            var phase = admission.Phase;
            Time(phase.Epoch.Origin);
            writer.Write(phase.Epoch.ProcessedSlot);
            foreach (string actor in phase.Epoch.Order) Text(actor);
            writer.Write(phase.FirstTurn);
            writer.Write(phase.FirstRound);
            var draw = admission.Draw;
            writer.Write(draw.Natural);
            writer.Write(draw.DexterityModifier);
            writer.Write(draw.Bonus);
            writer.Write(draw.RandomBefore);
            writer.Write(draw.RandomAfter);
            writer.Write(draw.WordsConsumed);
            foreach (var carry in admission.Carried) {
                var interval = carry.Interval;
                Text(interval.ActorId);
                writer.Write(interval.LastStart);
                Quantity(interval.MovementSpent);
                writer.Write(interval.ActionSpent);
                writer.Write(interval.DashPaid);
                writer.Write(interval.ReactionAvailable);
                writer.Write(interval.Interactions);
                writer.Write(carry.BonusActionAvailable);
            }
        }

        public static void Read(BinaryReader reader, Snapshot state)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
            RuleQuantity Quantity() => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());
            bool Flag() => SnapshotCodec.ReadBool(reader);

            var definition = new ReinforcementDefinition(Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text());
            var entries = new ReinforcementEvent[SnapshotCodec.ReadCount(reader, 2 * Validation.MaxReceipts)];
            for (int i = 0; i < entries.Length; i++)
                entries[i] = new ReinforcementEvent((ReinforcementEventKind)reader.ReadInt32(), reader.ReadInt64(),
                    Text(), Time(), Text(), Quantity());
            if (!Flag()) {
                state.Reinforcement = new ReinforcementRecord(definition, entries);
                return;
            }

            var at = Time();
            long slot = reader.ReadInt64();
            var epoch = new WorldScheduleRecord(definition.EpochId, at, new[] { Text(), Text(), Text() }, slot);
            var phase = new EncounterRosterPhase(epoch, reader.ReadInt32(), reader.ReadInt64());
            var draw = new LaterInitiativeDraw(definition.CompanionId, reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(),
                reader.ReadUInt32(), reader.ReadUInt32(), reader.ReadInt32());
            var carried = new ReinforcementCarry[3];
            for (int i = 0; i < carried.Length; i++)
                carried[i] = new ReinforcementCarry(new WorldIntervalRecord(Text(), reader.ReadInt64(), Quantity(),
                    Flag(), Flag(), Flag(), reader.ReadInt32()), Flag());
            state.Reinforcement = new ReinforcementRecord(definition, entries, new ReinforcementAdmission(phase, draw, carried));

            if (state.Encounter?.Id == definition.EncounterId) state.Encounter = state.Encounter.BindRosterPhase(phase);
            state.ClosedEncounters = state.ClosedEncounters.Select(closed => closed.Encounter.Id == definition.EncounterId
                ? new ClosedEncounterRecord(closed.Encounter.BindRosterPhase(phase), closed.ClosedRevision, closed.ClosedAt, closed.Reason)
                : closed).ToArray();
        }
    }
}
