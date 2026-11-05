#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Content identity for the bounded schema29 Soldier card procedures. Binding this
    /// fixture changes only the schema29 Soldier build fingerprint.</summary>
    internal static class SoldierTacticalTechniqueFixture
    {
        public const string SourceRevision="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        internal const string SourceReferences="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json@c414a1d9ba2ce37cde89d0ef73265821bb74ac2d#sha256=ab9cd3bd64355166dceb5a09e1ddab98443a957bb4bcdce813f1ad294ec048f0#/cards/5#/cards/7;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md@5a446dd0dabae096e51f419b5e71756e0169bb3b#sha256=adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81#action-and-timing-limits;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md@72bcb58af57f8bfe27596ec0b1467e4c780a6ef8#sha256=f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6#encounter-and-action-resources#standard-actions#cover-sight-and-search;"
            +"Engine:docs/unity/SOLDIER_TACTICAL_TECHNIQUE_RULE_DECISIONS.md@1bec16aa488bdd3987b483f47efcaa4004dff369#sha256=a42a8204c5f46e4aa754390ec725ff6d268c84da638c2116af2da375b4d577a5";

        internal static string BindFingerprint(string prior)
        {
            if(!Validation.ValidId(prior))throw new ArgumentException("Invalid prior Soldier content fingerprint.",nameof(prior));
            using(var sha=SHA256.Create())return "TEST_ONLY.soldier-techniques-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(
                prior+"|schema29|selected=WarningShot,CoveringFire|source="+SourceRevision+"|"+SourceReferences))
                .Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
    }
}
#endif
