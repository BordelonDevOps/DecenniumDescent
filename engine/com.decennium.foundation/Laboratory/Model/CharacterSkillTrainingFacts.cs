#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Read-only lookups over the persisted SkillTrainingRecord authority.</summary>
    public static class CharacterSkillTrainingFacts
    {
        public static SkillTrainingRecord Find(Snapshot snapshot, string actorId, string skillId)
        {
            if (snapshot == null) throw new ArgumentNullException(nameof(snapshot));
            if (!Validation.ValidId(actorId)) throw new ArgumentException("Actor identity is required.", nameof(actorId));
            if (!Validation.ValidId(skillId)) throw new ArgumentException("Skill identity is required.", nameof(skillId));
            if (snapshot.SkillTraining == null) throw new InvalidOperationException("Skill-training state is unavailable.");
            var matches = snapshot.SkillTraining.Where(x => x != null && x.ActorId == actorId && x.SkillId == skillId)
                .Take(2).ToArray();
            if (matches.Length > 1) throw new InvalidOperationException("Skill training must resolve exactly once.");
            return matches.Length == 0 ? null : matches[0];
        }

        public static int ProficiencyRank(Snapshot snapshot, string actorId, string skillId)
            => Find(snapshot, actorId, skillId)?.ProficiencyRank ?? 0;

        public static bool IsTrained(Snapshot snapshot, string actorId, string skillId)
            => ProficiencyRank(snapshot, actorId, skillId) > 0;
    }
}
#endif
