using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Versioned component payload. Not a complete game save or migration of fixture schema1.</summary>
    public sealed class WorkLedgerCodec
    {
        public const int MaxBytes=1024*1024;
        private const int Magic=0x314C5744; // DWL1
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public byte[] Encode(WorkLedger ledger)
        {
            if(ledger==null) throw new ArgumentNullException(nameof(ledger));
            byte[] payload;
            using(var stream=new MemoryStream()) using(var writer=new BinaryWriter(stream,Utf8,true)) {
                writer.Write(Magic);writer.Write(1);
                writer.Write(ledger.Lots.Count);
                foreach(var lot in ledger.Lots) {
                    Text(writer,lot.Id);Text(writer,lot.UnitId);writer.Write(lot.Quantity);
                    Text(writer,lot.LocationId);Text(writer,lot.CustodianId);
                }
                writer.Write(ledger.WorkerIntervals.Count);
                foreach(var interval in ledger.WorkerIntervals) {
                    Text(writer,interval.Id);Text(writer,interval.JobId);Text(writer,interval.WorkerId);
                    Time(writer,interval.Start);Time(writer,interval.End);
                }
                writer.Write(ledger.Reservations.Count);
                foreach(var claim in ledger.Reservations) {
                    Text(writer,claim.Id);Text(writer,claim.JobId);Text(writer,claim.LotId);
                    writer.Write(claim.Quantity);writer.Write((int)claim.Status);
                }
                writer.Flush();payload=stream.ToArray();
            }
            if(payload.Length>MaxBytes-32) throw new InvalidDataException("Work ledger exceeds serialized size limit.");
            using(var hash=SHA256.Create()) return payload.Concat(hash.ComputeHash(payload)).ToArray();
        }
        public WorkLedger Decode(byte[] bytes)
        {
            if(bytes==null || bytes.Length<52 || bytes.Length>MaxBytes) throw new InvalidDataException("Invalid work-ledger length.");
            int length=bytes.Length-32;
            using(var hash=SHA256.Create())
                if(!hash.ComputeHash(bytes,0,length).SequenceEqual(bytes.Skip(length))) throw new InvalidDataException("Work-ledger checksum mismatch.");
            try {
                using(var stream=new MemoryStream(bytes,0,length,false)) using(var reader=new BinaryReader(stream,Utf8)) {
                    if(reader.ReadInt32()!=Magic || reader.ReadInt32()!=1) throw new InvalidDataException("Unsupported work-ledger schema.");
                    var lots=new ResourceLot[Count(reader)];
                    for(int i=0;i<lots.Length;i++) lots[i]=new ResourceLot(Text(reader),Text(reader),reader.ReadInt64(),Text(reader),Text(reader));
                    var workers=new WorkerInterval[Count(reader)];
                    for(int i=0;i<workers.Length;i++) workers[i]=new WorkerInterval(Text(reader),Text(reader),Text(reader),Time(reader),Time(reader));
                    var claims=new ResourceReservation[Count(reader)];
                    for(int i=0;i<claims.Length;i++) claims[i]=new ResourceReservation(Text(reader),Text(reader),Text(reader),reader.ReadInt64(),(ReservationStatus)reader.ReadInt32());
                    if(stream.Position!=length) throw new InvalidDataException("Trailing work-ledger data.");
                    return new WorkLedger(lots,workers,claims);
                }
            } catch(Exception ex) when(ex is ArgumentException || ex is EndOfStreamException || ex is OverflowException) {
                throw new InvalidDataException("Malformed work ledger.",ex);
            }
        }
        private static int Count(BinaryReader reader)
        {
            int value=reader.ReadInt32();
            if(value<0 || value>WorkLedger.MaxRecords) throw new InvalidDataException("Invalid work-ledger count.");
            return value;
        }
        private static void Text(BinaryWriter writer,string value)
        { byte[] encoded=Utf8.GetBytes(value);writer.Write(encoded.Length);writer.Write(encoded); }
        private static string Text(BinaryReader reader)
        {
            int count=reader.ReadInt32();
            if(count<1 || count>96) throw new InvalidDataException("Invalid work-ledger string length.");
            byte[] data=reader.ReadBytes(count);if(data.Length!=count) throw new EndOfStreamException();
            return Utf8.GetString(data);
        }
        private static void Time(BinaryWriter writer,RuleTime value) {writer.Write(value.Numerator);writer.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader reader) => new RuleTime(reader.ReadInt64(),reader.ReadInt64());
    }
}
