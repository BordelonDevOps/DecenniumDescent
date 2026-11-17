using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum LivingRecipientQualification { Unknown, Living, NotLiving }

    /// <summary>Immutable source facts, separate from attained character levels. Trusted profile
    /// validation is required before these records confer any runtime capability.</summary>
    public sealed class CreatureActorRecord
    {
        public string ActorId { get; }
        public string SourceId { get; }
        public string SourceRevision { get; }
        public string SourcePath { get; }
        public string SourceSha256 { get; }
        public IReadOnlyList<int> Abilities { get; }
        public int ArmorClass { get; }
        public long MaximumHp { get; }
        public int WalkingSpeed { get; }
        public bool ClassificationKnown { get; }
        public IReadOnlyList<string> Types { get; }
        public LivingRecipientQualification LivingRecipient { get; }
        public IReadOnlyList<string> DamageResistances { get; }
        public IReadOnlyList<string> DamageImmunities { get; }
        public IReadOnlyList<string> ConditionImmunities { get; }

        public CreatureActorRecord(string actorId, string sourceId, string sourceRevision, string sourcePath,
            string sourceSha256, IEnumerable<int> abilities, int armorClass, long maximumHp, int walkingSpeed,
            bool classificationKnown, IEnumerable<string> types, LivingRecipientQualification livingRecipient,
            IEnumerable<string> damageResistances, IEnumerable<string> damageImmunities, IEnumerable<string> conditionImmunities)
        {
            var scores = abilities?.ToArray();
            if (!Validation.ValidId(actorId) || !Validation.ValidId(sourceId) || !Hex(sourceRevision,40)
                || string.IsNullOrEmpty(sourcePath) || sourcePath.Length > 1024 || sourcePath.Any(c => c < 32 || c > 126)
                || !Hex(sourceSha256,64) || scores == null || scores.Length != 6 || scores.Any(x => x < 1)
                || armorClass < 0 || maximumHp < 1 || walkingSpeed < 0 || !Enum.IsDefined(typeof(LivingRecipientQualification),livingRecipient))
                throw new ArgumentException("Invalid creature source facts.");
            ActorId=actorId; SourceId=sourceId; SourceRevision=sourceRevision; SourcePath=sourcePath; SourceSha256=sourceSha256;
            Abilities=Array.AsReadOnly(scores); ArmorClass=armorClass; MaximumHp=maximumHp; WalkingSpeed=walkingSpeed;
            ClassificationKnown=classificationKnown; Types=Names(types); LivingRecipient=livingRecipient;
            DamageResistances=Names(damageResistances); DamageImmunities=Names(damageImmunities); ConditionImmunities=Names(conditionImmunities);
            if (!classificationKnown && Types.Count != 0 || classificationKnown && Types.Count == 0)
                throw new ArgumentException("Creature classification knowledge mismatch.");
        }

        private static IReadOnlyList<string> Names(IEnumerable<string> values)
        {
            var rows=values?.ToArray();
            if(rows==null || rows.Length>32 || rows.Any(x=>!Validation.ValidId(x))
                || !rows.SequenceEqual(rows.Distinct(StringComparer.Ordinal).OrderBy(x=>x,StringComparer.Ordinal)))
                throw new ArgumentException("Invalid ordered creature source names.");
            return Array.AsReadOnly(rows);
        }
        internal static bool Hex(string value,int length) => value!=null && value.Length==length
            && value.All(c=>c>='0'&&c<='9'||c>='a'&&c<='f');
        public bool SameAs(CreatureActorRecord other) => other!=null && ActorId==other.ActorId && SourceId==other.SourceId
            && SourceRevision==other.SourceRevision && SourcePath==other.SourcePath && SourceSha256==other.SourceSha256
            && Abilities.SequenceEqual(other.Abilities) && ArmorClass==other.ArmorClass && MaximumHp==other.MaximumHp
            && WalkingSpeed==other.WalkingSpeed && ClassificationKnown==other.ClassificationKnown && Types.SequenceEqual(other.Types)
            && LivingRecipient==other.LivingRecipient && DamageResistances.SequenceEqual(other.DamageResistances)
            && DamageImmunities.SequenceEqual(other.DamageImmunities) && ConditionImmunities.SequenceEqual(other.ConditionImmunities);
    }
}
