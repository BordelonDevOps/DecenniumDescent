using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Immutable destination cost data. This technical record grants no terrain authority.</summary>
    public sealed class DeclaredTerrainCell
    {
        public int X { get; }
        public int Y { get; }
        public int CostPerFoot { get; }
        public DeclaredTerrainCell(int x, int y, int costPerFoot)
        {
            if (x < 0 || x >= 64 || y < 0 || y >= 64 || costPerFoot < 1 || costPerFoot > 3)
                throw new ArgumentException("Invalid declared terrain cell.");
            X = x; Y = y; CostPerFoot = costPerFoot;
        }
        public bool SameAs(DeclaredTerrainCell other) => other != null && X == other.X && Y == other.Y && CostPerFoot == other.CostPerFoot;
        internal string Binding => string.Join(",", new[] { X, Y, CostPerFoot }.Select(x => x.ToString(CultureInfo.InvariantCulture)));
    }

    /// <summary>Appended geometry binding, with no duplicate map. Observation fields own all bounds/cells.</summary>
    public sealed class DeclaredGeometryRecord
    {
        public string PredecessorFingerprint { get; }
        public string DeclarationDigest { get; }
        public ReadOnlyCollection<DeclaredTerrainCell> Terrain { get; }
        public DeclaredGeometryRecord(string predecessorFingerprint, string declarationDigest, IEnumerable<DeclaredTerrainCell> terrain)
        {
            var rows = (terrain ?? throw new ArgumentNullException(nameof(terrain))).ToArray();
            if (!DeclaredGeometryProfile.IsBishopPredecessor(predecessorFingerprint)
                || declarationDigest != DeclaredGeometryProfile.DeclarationDigest
                || rows.Length != DeclaredGeometryProfile.Terrain.Count
                || rows.Where((x, i) => !DeclaredGeometryProfile.Terrain[i].SameAs(x)).Any())
                throw new ArgumentException("Unsupported declared geometry binding.");
            PredecessorFingerprint = predecessorFingerprint; DeclarationDigest = declarationDigest;
            Terrain = Array.AsReadOnly(rows);
        }
        public bool SameAs(DeclaredGeometryRecord other) => other != null && PredecessorFingerprint == other.PredecessorFingerprint
            && DeclarationDigest == other.DeclarationDigest && Terrain.Count == other.Terrain.Count
            && Terrain.Zip(other.Terrain, (a, b) => a.SameAs(b)).All(x => x);
        public int TerrainCostAt(int x, int y) => Terrain.FirstOrDefault(t => t.X == x && t.Y == y)?.CostPerFoot ?? 1;
    }

    /// <summary>One reviewed TEST_ONLY composition, not an arbitrary scene or production registry.</summary>
    public static class DeclaredGeometryProfile
    {
        public const string Id = "TEST_ONLY.shared-declared-geometry.v1";
        public const string FingerprintPrefix = "TEST_ONLY.declared-geometry-v1-";
        public const string Approval = "187b46f8-dfeb-5c95-9554-6c7e0b6b9113";
        public const byte Marker = 18;
        public const int Width = 12, Height = 5;
        public const string Semantics = "chebyshev-5ft|exact-path-sight-intervals-v2|channels-independent|all-channel-anchor-support"
            + "|movement-two-unsupported-sides|ordinary-cardinal|tactical-diagonal|destination-terrain|known-static-map-only";
        public static IReadOnlyList<ObservationMapCellRecord> Cells { get; } = Array.AsReadOnly(new[] {
            new ObservationMapCellRecord(2,1,true,false,false,false),
            new ObservationMapCellRecord(6,1,false,false,true,false),
            new ObservationMapCellRecord(7,0,true,false,false,false),
            new ObservationMapCellRecord(9,0,false,true,false,false),
            new ObservationMapCellRecord(11,0,true,true,true,true)
        });
        public static IReadOnlyList<DeclaredTerrainCell> Terrain { get; } = Array.AsReadOnly(new[] {
            new DeclaredTerrainCell(5,2,2), new DeclaredTerrainCell(6,2,3)
        });
        public static string DeclarationDigest { get; } = Digest(string.Join("|", Id, Approval, Semantics, Width.ToString(CultureInfo.InvariantCulture) + "x" + Height.ToString(CultureInfo.InvariantCulture),
            string.Join(";", Cells.Select(x => string.Join(",", x.X.ToString(CultureInfo.InvariantCulture), x.Y.ToString(CultureInfo.InvariantCulture),
                x.BlocksSight ? "1" : "0", x.BlocksEffect ? "1" : "0", x.BlocksMovement ? "1" : "0", x.Solid ? "1" : "0"))),
            string.Join(";", Terrain.Select(x => x.Binding))));
        private static string Digest(string value)
        {
            using (var hash = SHA256.Create()) return string.Concat(hash.ComputeHash(Encoding.UTF8.GetBytes(value))
                .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
        internal static bool IsBishopPredecessor(string value) => value != null
            && value.StartsWith(BishopProfile.FingerprintPrefix, StringComparison.Ordinal)
            && value.Length == BishopProfile.FingerprintPrefix.Length + 64
            && value.Substring(BishopProfile.FingerprintPrefix.Length).All(x => x >= '0' && x <= '9' || x >= 'a' && x <= 'f');
        public static string BindFingerprint(string predecessor)
        {
            if (!IsBishopPredecessor(predecessor)) throw new ArgumentException("Declared geometry requires its exact Bishop predecessor.");
            return FingerprintPrefix + Digest(predecessor + "|" + DeclarationDigest);
        }
        public static DeclaredGeometryRecord Create(string predecessor)
            => new DeclaredGeometryRecord(predecessor, DeclarationDigest, Terrain);
        public static bool SelectedFingerprint(string value) => value != null && (value.StartsWith(FingerprintPrefix, StringComparison.Ordinal) || FerryWraithProfile.SelectedFingerprint(value));
        public static bool Selected(Snapshot s) => s.DeclaredGeometry != null || SelectedFingerprint(s.ContentFingerprint);
        public static bool HasExpectedLayout(Snapshot s) => s.ObservationMapWidth == Width && s.ObservationMapHeight == Height
            && s.ObservationCells != null && s.ObservationCells.Length == Cells.Count
            && s.ObservationCells.Where((x, i) => !Cells[i].SameAs(x)).Any() == false;
        public static bool SupportsAnchorAt(Snapshot s, int x, int y)
        {
            // Selected malformed data is never sent to the legacy five-by-five fallback.
            if (s.DeclaredGeometry == null || !HasExpectedLayout(s)) return false;
            return x >= 0 && x < s.ObservationMapWidth && y >= 0 && y < s.ObservationMapHeight
                && !s.ObservationCells.Any(c => c.X == x && c.Y == y && (c.BlocksSight || c.BlocksEffect || c.BlocksMovement));
        }
        public static int TerrainCostAt(Snapshot s, int x, int y)
        {
            if (!SupportsAnchorAt(s, x, y)) throw new ArgumentException("Declared terrain requires a supported destination.");
            return s.DeclaredGeometry.TerrainCostAt(x, y);
        }
        internal static void Validate(Snapshot s)
        {
            if ((s.DeclaredGeometry != null) != SelectedFingerprint(s.ContentFingerprint))
                throw new ArgumentException("Declared geometry profile envelope mismatch.");
            if (s.DeclaredGeometry == null) return;
            if (!s.TestOnly || s.SchemaVersion != Snapshot.SurpriseEntrySchema || s.BishopEntry == null
                || (s.FerryWraith==null?s.ContentFingerprint:s.FerryWraith.PredecessorFingerprint) != BindFingerprint(s.DeclaredGeometry.PredecessorFingerprint) || !HasExpectedLayout(s))
                throw new ArgumentException("Invalid trusted declared geometry composition.");
        }
    }
}
