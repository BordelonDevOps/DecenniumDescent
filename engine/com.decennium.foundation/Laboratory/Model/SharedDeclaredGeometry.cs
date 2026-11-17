#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Shared declared floor/cost adapter. Legacy observations are opted in at each old caller.</summary>
    public static class SharedDeclaredGeometry
    {
        public static bool SupportsAnchorAt(Snapshot state, int x, int y, bool legacyObservation = false)
            => DeclaredGeometryProfile.Selected(state) ? DeclaredGeometryProfile.SupportsAnchorAt(state, x, y)
                : TestOnlyPolicy.Walkable(x, y) && (!legacyObservation || ObservationGeometry.SupportsAnchorAt(state, x, y));
        internal static TerrainCost TerrainAt(Snapshot state, TacticalCombatFixture legacy, int x, int y)
            => DeclaredGeometryProfile.Selected(state) ? (TerrainCost)DeclaredGeometryProfile.TerrainCostAt(state, x, y) : legacy.At(x, y);
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private DeclaredGeometryRecord declaredGeometry;
        internal TestOnlySharedWorldPolicy EnableDeclaredGeometry()
        {
            if (initializationStarted || declaredGeometry != null || bishopDeclaration == null || observationFixture == null
                || observationAlgorithmVersion != ObservationAlgorithmVersion.ExactPathIntervalsV2 || terrain.Terrain.Count != 0)
                throw new InvalidOperationException("Select declared geometry once on a fresh Bishop expedition with its exact inherited floor.");
            var binding = DeclaredGeometryProfile.Create(ContentFingerprint);
            observationFixture = new ObservationFixture(DeclaredGeometryProfile.Width, DeclaredGeometryProfile.Height,
                DeclaredGeometryProfile.Cells.Select(x => new ObservationGridCell(x.X, x.Y, x.BlocksSight, x.BlocksEffect, x.BlocksMovement, x.Solid)),
                observationFixture.Profiles);
            declaredGeometry = binding;
            ContentFingerprint = DeclaredGeometryProfile.BindFingerprint(binding.PredecessorFingerprint);
            return this;
        }
    }
}
#endif
