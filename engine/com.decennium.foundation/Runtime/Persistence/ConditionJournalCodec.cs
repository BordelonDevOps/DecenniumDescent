using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Versioned component payload, not a game snapshot or migration. Decoding validates
    /// structure only; the selected rules interpreter must replay and validate the history.</summary>
    public sealed class ConditionJournalCodec
    {
        public const int MaxBytes = 1024 * 1024;
        private const int Magic = 0x314A4344; // DCJ1
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        public byte[] Encode(ConditionJournal journal)
        {
            if (journal == null) throw new ArgumentNullException(nameof(journal));
            byte[] payload;
            using (var stream = new MemoryStream()) using (var w = new BinaryWriter(stream, Utf8, true)) {
                w.Write(Magic); w.Write(1); Text(w, journal.PolicyId); Text(w, journal.Target); Stamp(w, journal.Origin);
                w.Write(journal.Operations.Count);
                foreach (var operation in journal.Operations) {
                    Text(w, operation.Id); Stamp(w, operation.At); w.Write((int)operation.Kind);
                    switch (operation.Kind) {
                        case ConditionOperationKind.Apply:
                            var a = operation.Application;
                            Text(w, a.Id); Text(w, a.Owner); Text(w, a.Source); Text(w, a.Kind); OptionalStamp(w, a.Expires);
                            Text(w, a.EndingMethod); w.Write(a.GenericCureAllowed); w.Write(a.InheritedCureAllowed.HasValue);
                            if (a.InheritedCureAllowed.HasValue) w.Write(a.InheritedCureAllowed.Value);
                            w.Write(a.ApplyingDc.HasValue); if (a.ApplyingDc.HasValue) w.Write(a.ApplyingDc.Value);
                            w.Write(a.Magnitude.HasValue); if (a.Magnitude.HasValue) w.Write(a.Magnitude.Value);
                            Text(w, operation.Subject); break;
                        case ConditionOperationKind.GrantImmunity:
                            var g = operation.Immunity;
                            Text(w, g.Id); Text(w, g.Owner); Text(w, g.Source); w.Write(g.Kinds.Count);
                            foreach (string kind in g.Kinds) Text(w, kind);
                            OptionalStamp(w, g.Expires); Text(w, g.EndingMethod); break;
                        case ConditionOperationKind.Suppress: Text(w, operation.Subject); w.Write(operation.Suppressed); break;
                        case ConditionOperationKind.EndApplication:
                        case ConditionOperationKind.EndImmunity: Text(w, operation.Subject); Text(w, operation.Reason); break;
                        case ConditionOperationKind.Cure: Text(w, operation.Subject); break;
                        case ConditionOperationKind.Advance: break;
                        default: throw new InvalidDataException("Unsupported condition operation.");
                    }
                }
                w.Flush(); payload = stream.ToArray();
            }
            if (payload.Length > MaxBytes - 32) throw new InvalidDataException("Condition journal size limit reached.");
            using (var hash = SHA256.Create()) return payload.Concat(hash.ComputeHash(payload)).ToArray();
        }
        public ConditionJournal Decode(byte[] bytes)
        {
            if (bytes == null || bytes.Length < 74 || bytes.Length > MaxBytes) throw new InvalidDataException("Invalid condition journal length.");
            int length = bytes.Length - 32;
            using (var hash = SHA256.Create())
                if (!hash.ComputeHash(bytes, 0, length).SequenceEqual(bytes.Skip(length))) throw new InvalidDataException("Condition journal checksum mismatch.");
            try {
                using (var stream = new MemoryStream(bytes, 0, length, false)) using (var r = new BinaryReader(stream, Utf8)) {
                    if (r.ReadInt32() != Magic || r.ReadInt32() != 1) throw new InvalidDataException("Unsupported condition journal version.");
                    string policy = Text(r), target = Text(r); var origin = Stamp(r);
                    var operations = new ConditionOperation[Count(r, ConditionJournal.MaxOperations)];
                    for (int i = 0; i < operations.Length; i++) {
                        string id = Text(r); var at = Stamp(r); var kind = (ConditionOperationKind)r.ReadInt32();
                        switch (kind) {
                            case ConditionOperationKind.Apply:
                                string appId = Text(r), owner = Text(r), source = Text(r), name = Text(r); var expires = OptionalStamp(r);
                                string ending = Text(r); bool cure = Bool(r); bool? inherited = Bool(r) ? Bool(r) : (bool?)null;
                                int? dc = Bool(r) ? r.ReadInt32() : (int?)null; long? magnitude = Bool(r) ? r.ReadInt64() : (long?)null;
                                operations[i] = ConditionOperation.Apply(id, at, new ConditionApplicationData(appId, owner, source, name, expires, ending, cure, dc, magnitude, inherited), Text(r, true)); break;
                            case ConditionOperationKind.GrantImmunity:
                                string grantId = Text(r), grantOwner = Text(r), grantSource = Text(r); var kinds = new string[Count(r, 14)];
                                for (int j = 0; j < kinds.Length; j++) kinds[j] = Text(r);
                                operations[i] = ConditionOperation.Grant(id, at, new ConditionImmunityData(grantId, grantOwner, grantSource, kinds, OptionalStamp(r), Text(r))); break;
                            case ConditionOperationKind.Suppress: operations[i] = ConditionOperation.Suppress(id, at, Text(r), Bool(r)); break;
                            case ConditionOperationKind.EndApplication: operations[i] = ConditionOperation.End(id, at, Text(r), Text(r)); break;
                            case ConditionOperationKind.EndImmunity: operations[i] = ConditionOperation.EndGrant(id, at, Text(r), Text(r)); break;
                            case ConditionOperationKind.Cure: operations[i] = ConditionOperation.Cure(id, at, Text(r)); break;
                            case ConditionOperationKind.Advance: operations[i] = ConditionOperation.Advance(id, at); break;
                            default: throw new InvalidDataException("Unknown condition operation tag.");
                        }
                    }
                    if (stream.Position != length) throw new InvalidDataException("Trailing condition journal bytes.");
                    var result = new ConditionJournal(policy, target, origin, operations);
                    // Reject alternate rational encodings and immunity ordering, rather than
                    // silently rewriting the exact persisted component on the next save.
                    if (!Encode(result).SequenceEqual(bytes)) throw new InvalidDataException("Noncanonical condition journal encoding.");
                    return result;
                }
            } catch (Exception ex) when (ex is ArgumentException || ex is EndOfStreamException || ex is OverflowException) {
                throw new InvalidDataException("Malformed condition journal.", ex);
            }
        }
        private static void Text(BinaryWriter w, string value) { byte[] bytes = Utf8.GetBytes(value); w.Write(bytes.Length); w.Write(bytes); }
        private static string Text(BinaryReader r, bool empty = false)
        {
            int count = Count(r, 96); if (count == 0 && !empty) throw new InvalidDataException("Empty condition identity.");
            byte[] bytes = r.ReadBytes(count); if (bytes.Length != count) throw new EndOfStreamException(); return Utf8.GetString(bytes);
        }
        private static int Count(BinaryReader r, int max)
        { int count = r.ReadInt32(); if (count < 0 || count > max) throw new InvalidDataException("Invalid condition journal count."); return count; }
        private static bool Bool(BinaryReader r)
        { byte value = r.ReadByte(); if (value > 1) throw new InvalidDataException("Invalid condition journal flag."); return value == 1; }
        private static void Stamp(BinaryWriter w, ConditionStamp value) { w.Write(value.Time.Numerator); w.Write(value.Time.Denominator); w.Write(value.Phase); }
        private static ConditionStamp Stamp(BinaryReader r) => new ConditionStamp(new RuleTime(r.ReadInt64(), r.ReadInt64()), r.ReadInt32());
        private static void OptionalStamp(BinaryWriter w, ConditionStamp? value) { w.Write(value.HasValue); if (value.HasValue) Stamp(w, value.Value); }
        private static ConditionStamp? OptionalStamp(BinaryReader r) => Bool(r) ? Stamp(r) : (ConditionStamp?)null;
    }
}
