#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>A fixed source event delivered by an upstream feature adapter. This is an
    /// occurred-event fixture only; it does not execute Overwatch, an attack, or its trigger.</summary>
    public sealed class PeriodicRiderApplicationFact
    {
        public string EventId { get; }
        public string RiderId { get; }
        public string OwnerId { get; }
        public string TargetId { get; }
        public int ApplyingDc { get; }
        public RuleTime At { get; }
        public PeriodicRiderApplicationFact(string eventId,string riderId,string ownerId,string targetId,int applyingDc,RuleTime at=default)
        {
            foreach(string value in new[]{eventId,riderId,ownerId,targetId})if(!Validation.ValidId(value))throw new ArgumentException("Invalid registered rider event.");
            if(applyingDc<5||applyingDc>30)throw new ArgumentOutOfRangeException(nameof(applyingDc));
            EventId=eventId;RiderId=riderId;OwnerId=ownerId;TargetId=targetId;ApplyingDc=applyingDc;At=at;
        }
        internal string Key=>EventId+"|"+RiderId+"|"+OwnerId+"|"+TargetId+"|"+ApplyingDc.ToString(CultureInfo.InvariantCulture)+"|"+At;
    }

    public sealed class PeriodicMedicineFact
    {
        public string ActorId { get; }
        public int ProficiencyRank { get; }
        public PeriodicMedicineFact(string actorId,int proficiencyRank)
        {
            if(!Validation.ValidId(actorId)||proficiencyRank<0||proficiencyRank>2)throw new ArgumentException("Invalid Medicine training fact.");
            ActorId=actorId;ProficiencyRank=proficiencyRank;
        }
        internal string Key=>ActorId+"|"+ProficiencyRank.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>One bounded, positive-potential magical-healing event. Its id, caster, recipient,
    /// and potential are fixture facts, not player-selected spell inputs.</summary>
    public sealed class PeriodicHealingFact
    {
        public string EventId { get; }
        public string CasterId { get; }
        public string TargetId { get; }
        public long Potential { get; }
        public PeriodicHealingFact(string eventId,string casterId,string targetId,long potential)
        {
            if(!Validation.ValidId(eventId)||!Validation.ValidId(casterId)||!Validation.ValidId(targetId)||potential<1||potential>1000)
                throw new ArgumentException("Invalid healing occurrence fixture.");
            EventId=eventId;CasterId=casterId;TargetId=targetId;Potential=potential;
        }
        internal string Key=>EventId+"|"+CasterId+"|"+TargetId+"|"+Potential.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Source-bound schema23 registration. Only the Soldier Overwatch Bleed profile is
    /// admitted; family competitors, status changes, Medicine and healing use explicit events.</summary>
    public sealed class PeriodicRiderFixture
    {
        public const string ProfileId="soldier.overwatch.bleed";
        public const string FamilyId="family.bleeding";
        public const string SourceId="soldier.overwatch";
        private readonly PeriodicRiderApplicationFact[] applications;
        private readonly PeriodicMedicineFact[] medicine;
        private readonly PeriodicRiderRecord[] initialRiders;
        public System.Collections.Generic.IReadOnlyList<PeriodicRiderApplicationFact> Applications { get; }
        public System.Collections.Generic.IReadOnlyList<PeriodicMedicineFact> Medicine { get; }
        public System.Collections.Generic.IReadOnlyList<PeriodicRiderRecord> InitialRiders { get; }
        public PeriodicHealingFact Healing { get; }
        public PeriodicRiderFixture(PeriodicRiderApplicationFact[] applications,PeriodicMedicineFact[] medicine=null,PeriodicHealingFact healing=null,
            PeriodicRiderRecord[] initialRiders=null)
        {
            var apps=applications??Array.Empty<PeriodicRiderApplicationFact>();var skills=medicine??Array.Empty<PeriodicMedicineFact>();
            var active=initialRiders??Array.Empty<PeriodicRiderRecord>();
            if(apps.Length<1||apps.Length>16||apps.Any(x=>x==null)||skills.Length>64||skills.Any(x=>x==null)
                ||apps.Select(x=>x.EventId).Distinct(StringComparer.Ordinal).Count()!=apps.Length
                ||skills.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Count()!=skills.Length
                ||apps.Select(x=>x.RiderId).Distinct(StringComparer.Ordinal).Count()!=apps.Length
                ||active.Length>16||active.Any(x=>x==null||!x.Present||x.ProfileId!=ProfileId||x.FamilyId!=FamilyId||x.SourceId!=SourceId
                    ||x.DamageType!="piercing"||x.RemainingTicks!=1||x.ApplicationOrder!=0||x.AppliedAt!=default)
                ||active.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=active.Length
                ||active.Select(x=>x.TargetId+"|"+x.OwnerId+"|"+x.SourceId).Distinct(StringComparer.Ordinal).Count()!=active.Length
                ||apps.Any(a=>active.Any(x=>x.Id==a.RiderId)))
                throw new ArgumentException("Invalid periodic rider fixture inventory.");
            this.applications=apps.ToArray();this.medicine=skills.ToArray();this.initialRiders=active.ToArray();
            Applications=Array.AsReadOnly(this.applications);Medicine=Array.AsReadOnly(this.medicine);InitialRiders=Array.AsReadOnly(this.initialRiders);Healing=healing;
        }
        internal string Key=>"periodic-rider-schema23-v1|"+string.Join(";",applications.Select(x=>x.Key))+"|medicine="
            +string.Join(";",medicine.OrderBy(x=>x.ActorId,StringComparer.Ordinal).Select(x=>x.Key))+"|healing="+(Healing?.Key??"none")
            +"|initial="+string.Join(";",initialRiders.OrderBy(x=>x.Id,StringComparer.Ordinal).Select(x=>x.Id+"|"+x.OwnerId+"|"+x.TargetId+"|"
                +x.OriginEventId+"|"+x.ApplyingDc.ToString(CultureInfo.InvariantCulture)+"|"+x.NextStartSlot.ToString(CultureInfo.InvariantCulture)+"|"+(x.Suppressed?"1":"0")))
            +"|profile="+ProfileId+"|family="+FamilyId+"|source="+SourceId+"|damage=piercing|ticks=1|sources="+SourceReferences;
        internal string BindFingerprint(string prior)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.periodic-rider-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+Key))
                .Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
        internal const string SourceReferences="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/data/playtest/custom_condition_bindings.json@47605df81404d19f96e943dc06f61b9ac43ce34d#sha256=453a805fabc86a1f1961f285960acc0457b57bd45c2fa570793d7ff8387d5ce5#/definitions/38;/familyRules/2;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/data/public/class_playtests/soldier.json@c414a1d9ba2ce37cde89d0ef73265821bb74ac2d#sha256=ab9cd3bd64355166dceb5a09e1ddab98443a957bb4bcdce813f1ad294ec048f0#/engine/1;"
            +"46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/tools/custom_condition_rules.py@122de7ca4cefbf2401eefca6bbe8e848b25f5ff2#sha256=3708ff099026a66288fdb791a129e5ce57a1bd3eefa47cd8d7bb3fbbaf20dfd4#arbitrate_periodic_applications:91-114;"
            +"Engine:docs/unity/OVERWATCH_RULE_DECISIONS.md@52ae6c03b1ab46f149ce09acff087eaa6f0df991#sha256=810a0bbd1f5824515d99995f2496ca70bc46abeee7307f0aeac3f2da3a2d7130";
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private PeriodicRiderFixture periodicRider;
        public TestOnlySharedWorldPolicy(PeriodicRiderFixture periodic,CharacterAdvancementFixture advancement,SharedCombatFixture combat,
            int walkingSpeed=30,ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(advancement,combat,walkingSpeed,conditions,terrain)
        {
            periodicRider=periodic??throw new ArgumentNullException(nameof(periodic));
            ContentFingerprint=periodicRider.BindFingerprint(ContentFingerprint);
        }
        public TestOnlySharedWorldPolicy(PeriodicRiderFixture periodic,CharacterAdvancementFixture advancement,SharedCombatFixture combat,
            SharedResearchFixture research,int walkingSpeed=30,ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(combat,research,(SharedCraftingFixture)null,(SharedRepairFixture)null,(SharedManufacturingFixture)null,(SupplyCacheFixture)null,
                walkingSpeed,conditions,terrain)
        {
            characterAdvancement=advancement??throw new ArgumentNullException(nameof(advancement));
            periodicRider=periodic??throw new ArgumentNullException(nameof(periodic));
            if(combat==null)throw new ArgumentNullException(nameof(combat));
            ContentFingerprint=characterAdvancement.BindFingerprint(ContentFingerprint);
            ContentFingerprint=periodicRider.BindFingerprint(ContentFingerprint);
        }
        private void InitializePeriodicRider(Snapshot s)
        {
            if(periodicRider==null)return;
            if(s.SchemaVersion<Snapshot.PeriodicRiderSchema||s.WorldSchedule==null)throw new ArgumentException("Periodic rider requires the shared schema23-or-later calendar.");
            foreach(var fact in periodicRider.Applications)
                if(!s.WorldSchedule.Order.Contains(fact.OwnerId)||!s.WorldSchedule.Order.Contains(fact.TargetId))
                    throw new ArgumentException("Periodic event actors must belong to the admitted encounter calendar.");
            foreach(var rider in periodicRider.InitialRiders)
                if(!s.WorldSchedule.Order.Contains(rider.OwnerId)||!s.WorldSchedule.Order.Contains(rider.TargetId)
                    ||rider.AppliedAt>s.RuleClock||rider.NextStartSlot<=s.WorldSchedule.ProcessedSlot)
                    throw new ArgumentException("Initial periodic riders must reference calendar actors and a future marker.");
            if(periodicRider.Healing!=null&&(!s.Actors.Any(x=>x.Id==periodicRider.Healing.CasterId)||!s.Actors.Any(x=>x.Id==periodicRider.Healing.TargetId)))
                throw new ArgumentException("Healing event actors must belong to the fixture roster.");
            s.SkillTraining=s.Characters.Select(c=>new SkillTrainingRecord(c.ActorId,"medicine",0)).ToArray();
            s.SkillTraining=s.SkillTraining.Select(skill=>periodicRider.Medicine.Any(x=>x.ActorId==skill.ActorId)
                ?new SkillTrainingRecord(skill.ActorId,"medicine",periodicRider.Medicine.Single(x=>x.ActorId==skill.ActorId).ProficiencyRank):skill).ToArray();
            if(periodicRider.Medicine.Any(x=>!s.Characters.Any(c=>c.ActorId==x.ActorId)))throw new ArgumentException("Medicine training references an unknown character.");
            s.PeriodicRiders=periodicRider.InitialRiders.ToArray();
        }
    }
}
#endif
