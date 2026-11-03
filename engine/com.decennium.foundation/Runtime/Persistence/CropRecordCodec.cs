using System;
using System.IO;
using System.Text;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Internal schema3 component. The enclosing snapshot owns integrity and the commit boundary.</summary>
    internal static class CropRecordCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter writer,Snapshot state)
        {
            writer.Write(state.CropPlots.Length);
            foreach(var plot in state.CropPlots.OrderBy(p=>p.Id,StringComparer.Ordinal)) {
                Text(writer,plot.Id);Text(writer,plot.OwnerId);writer.Write(plot.Suitable);
            }
            writer.Write(state.Crops.Length);
            foreach(var crop in state.Crops.OrderBy(c=>c.Id,StringComparer.Ordinal)) {
                Text(writer,crop.Id);Text(writer,crop.PlotId);Text(writer,crop.SeedLotId);Text(writer,crop.OwnerId);
                Time(writer,crop.CreatedAt);Time(writer,crop.UpdatedAt);writer.Write((int)crop.Stage);
                Time(writer,crop.Growth);Optional(writer,crop.CareUntil);Optional(writer,crop.UnsuitableSince);
                Optional(writer,crop.MaturedAt);Optional(writer,crop.ClosedAt);
                writer.Write(crop.Tasks.Count);
                foreach(var task in crop.Tasks) {
                    Text(writer,task.Id);Text(writer,task.WorkerId);writer.Write((int)task.Kind);writer.Write((int)task.Status);
                    Time(writer,task.StartedAt);Time(writer,task.Progress);Optional(writer,task.EndedAt);
                    writer.Write(task.InputReservations.Count);foreach(var id in task.InputReservations)Text(writer,id);
                }
            }
            writer.Write(state.CropFood.Length);
            foreach(var food in state.CropFood.OrderBy(f=>f.LotId,StringComparer.Ordinal)) {
                Text(writer,food.LotId);Text(writer,food.BatchId);Time(writer,food.FreshUntil);writer.Write(food.Expired);
            }
        }
        public static void Read(BinaryReader reader,Snapshot state)
        {
            state.CropPlots=new CropPlotRecord[Count(reader,Snapshot.MaxCropBatches)];
            for(int i=0;i<state.CropPlots.Length;i++)state.CropPlots[i]=new CropPlotRecord(Text(reader),Text(reader),Bool(reader));
            state.Crops=new CropBatchRecord[Count(reader,Snapshot.MaxCropBatches)];
            for(int i=0;i<state.Crops.Length;i++) {
                string id=Text(reader),plot=Text(reader),seed=Text(reader),owner=Text(reader);
                RuleTime created=Time(reader),updated=Time(reader);var stage=(CropStage)reader.ReadInt32();
                RuleTime growth=Time(reader);RuleTime? care=Optional(reader),blocked=Optional(reader),matured=Optional(reader),closed=Optional(reader);
                var tasks=new CropWorkRecord[Count(reader,CropBatchRecord.MaxTasks)];
                for(int j=0;j<tasks.Length;j++) {
                    string taskId=Text(reader),worker=Text(reader);var kind=(CropWorkKind)reader.ReadInt32();var status=(CropWorkStatus)reader.ReadInt32();
                    RuleTime start=Time(reader),progress=Time(reader);RuleTime? end=Optional(reader);
                    var inputs=new string[Count(reader,2)];for(int k=0;k<inputs.Length;k++)inputs[k]=Text(reader);
                    tasks[j]=new CropWorkRecord(taskId,worker,kind,status,start,progress,end,inputs);
                }
                state.Crops[i]=new CropBatchRecord(id,plot,seed,owner,created,updated,stage,growth,care,blocked,matured,closed,tasks);
            }
            state.CropFood=new CropFoodRecord[Count(reader,Snapshot.MaxCropBatches)];
            for(int i=0;i<state.CropFood.Length;i++) state.CropFood[i]=new CropFoodRecord(Text(reader),Text(reader),Time(reader),Bool(reader));
        }
        private static int Count(BinaryReader reader,int maximum)
        {int n=reader.ReadInt32();if(n<0||n>maximum)throw new InvalidDataException("Invalid crop collection length.");return n;}
        private static bool Bool(BinaryReader reader)
        {byte b=reader.ReadByte();if(b>1)throw new InvalidDataException("Invalid crop boolean.");return b==1;}
        private static void Text(BinaryWriter writer,string value)
        {byte[] bytes=Utf8.GetBytes(value);writer.Write(bytes.Length);writer.Write(bytes);}
        private static string Text(BinaryReader reader)
        {int n=Count(reader,96);if(n==0)throw new InvalidDataException("Empty crop identity.");byte[] bytes=reader.ReadBytes(n);if(bytes.Length!=n)throw new EndOfStreamException();return Utf8.GetString(bytes);}
        private static void Time(BinaryWriter writer,RuleTime time){writer.Write(time.Numerator);writer.Write(time.Denominator);}
        private static RuleTime Time(BinaryReader reader)=>new RuleTime(reader.ReadInt64(),reader.ReadInt64());
        private static void Optional(BinaryWriter writer,RuleTime? time){writer.Write(time.HasValue);if(time.HasValue)Time(writer,time.Value);}
        private static RuleTime? Optional(BinaryReader reader)=>Bool(reader)?Time(reader):(RuleTime?)null;
    }
}
