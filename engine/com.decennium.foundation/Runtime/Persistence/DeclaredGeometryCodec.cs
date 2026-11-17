using System.IO;

namespace Decennium.Foundation
{
    internal static class DeclaredGeometryCodec
    {
        internal static void Write(BinaryWriter writer, DeclaredGeometryRecord geometry)
        {
            SnapshotCodec.WriteText(writer, geometry.PredecessorFingerprint);
            SnapshotCodec.WriteText(writer, geometry.DeclarationDigest);
            writer.Write(geometry.Terrain.Count);
            foreach (var cell in geometry.Terrain) { writer.Write(cell.X); writer.Write(cell.Y); writer.Write(cell.CostPerFoot); }
        }
        internal static DeclaredGeometryRecord Read(BinaryReader reader)
        {
            string predecessor = SnapshotCodec.ReadText(reader), digest = SnapshotCodec.ReadText(reader);
            var cells = new DeclaredTerrainCell[SnapshotCodec.ReadCount(reader, 4096)];
            for (int i = 0; i < cells.Length; i++) cells[i] = new DeclaredTerrainCell(reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32());
            return new DeclaredGeometryRecord(predecessor, digest, cells);
        }
    }
}
