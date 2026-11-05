using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum SoldierTacticalEffectKind { WarningShot, CoveringFire }
    public enum SoldierTacticalEffectStatus { Active, Consumed, Expired, Replaced }
    public enum SoldierTacticalEffectPhase { Start, End }
    public enum TacticalAssessmentStatus { Active, Consumed, Expired }

    /// <summary>Paid Tactical Assessment observation and one ally's pending next-attack bonus.
    /// The observation values are recorded so a presentation can reveal only facts earned by this
    /// activation; they are derived by the fixture resolver, never supplied by the command.</summary>
    public sealed class TacticalAssessmentRecord
    {
        public string Id { get; }
        public string SourceActorId { get; }
        public string AllyActorId { get; }
        public string EnemyActorId { get; }
        public long AppliedRevision { get; }
        public RuleTime AppliedAt { get; }
        public long ExpirySlot { get; }
        public string ArmorCategory { get; }
        public bool HasCover { get; }
        public TacticalAssessmentStatus Status { get; }
        public long ResolvedRevision { get; }
        public string ResolutionId { get; }

        public TacticalAssessmentRecord(string id,string sourceActorId,string allyActorId,string enemyActorId,long appliedRevision,
            RuleTime appliedAt,long expirySlot,string armorCategory,bool hasCover,TacticalAssessmentStatus status=TacticalAssessmentStatus.Active,
            long resolvedRevision=0,string resolutionId="")
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(sourceActorId)||!Validation.ValidId(allyActorId)||!Validation.ValidId(enemyActorId)
                ||sourceActorId==allyActorId||sourceActorId==enemyActorId||allyActorId==enemyActorId||appliedRevision<1||expirySlot<0
                ||(armorCategory!="unarmored"&&armorCategory!="heavy")||!Enum.IsDefined(typeof(TacticalAssessmentStatus),status)
                ||resolvedRevision<0||status==TacticalAssessmentStatus.Active&&(resolvedRevision!=0||resolutionId!="")
                ||status!=TacticalAssessmentStatus.Active&&(resolvedRevision<appliedRevision||!Validation.ValidId(resolutionId)))
                throw new ArgumentException("Invalid Tactical Assessment record.");
            Id=id;SourceActorId=sourceActorId;AllyActorId=allyActorId;EnemyActorId=enemyActorId;AppliedRevision=appliedRevision;
            AppliedAt=appliedAt;ExpirySlot=expirySlot;ArmorCategory=armorCategory;HasCover=hasCover;Status=status;
            ResolvedRevision=resolvedRevision;ResolutionId=resolutionId;
        }
        public TacticalAssessmentRecord Resolve(TacticalAssessmentStatus status,long revision,string resolutionId)
        {
            if(Status!=TacticalAssessmentStatus.Active||status==TacticalAssessmentStatus.Active)
                throw new InvalidOperationException("Only an active Tactical Assessment can resolve.");
            return new TacticalAssessmentRecord(Id,SourceActorId,AllyActorId,EnemyActorId,AppliedRevision,AppliedAt,ExpirySlot,
                ArmorCategory,HasCover,status,revision,resolutionId);
        }
        public bool SameAs(TacticalAssessmentRecord x)=>x!=null&&Id==x.Id&&SourceActorId==x.SourceActorId&&AllyActorId==x.AllyActorId
            &&EnemyActorId==x.EnemyActorId&&AppliedRevision==x.AppliedRevision&&AppliedAt==x.AppliedAt&&ExpirySlot==x.ExpirySlot
            &&ArmorCategory==x.ArmorCategory&&HasCover==x.HasCover&&Status==x.Status&&ResolvedRevision==x.ResolvedRevision&&ResolutionId==x.ResolutionId;
    }

    /// <summary>Explicit test-fixture evidence that two actors are allies for Covering Fire.</summary>
    public sealed class TacticalAllyRecord
    {
        public string FirstActorId { get; }
        public string SecondActorId { get; }
        public TacticalAllyRecord(string firstActorId,string secondActorId)
        {
            if(!Validation.ValidId(firstActorId)||!Validation.ValidId(secondActorId)||firstActorId==secondActorId)
                throw new ArgumentException("Invalid tactical ally relationship.");
            if(string.CompareOrdinal(firstActorId,secondActorId)>0){string swap=firstActorId;firstActorId=secondActorId;secondActorId=swap;}
            FirstActorId=firstActorId;SecondActorId=secondActorId;
        }
        public bool Includes(string actor)=>FirstActorId==actor||SecondActorId==actor;
        public string Other(string actor)=>FirstActorId==actor?SecondActorId:SecondActorId==actor?FirstActorId:"";
        public bool SameAs(TacticalAllyRecord x)=>x!=null&&FirstActorId==x.FirstActorId&&SecondActorId==x.SecondActorId;
    }

    /// <summary>A finite next-attack effect from one admitted Soldier card. The virtual expiry
    /// marker is captured when applied; source death and combat exit do not rewrite it.</summary>
    public sealed class SoldierTacticalEffectRecord
    {
        public string Id { get; }
        public SoldierTacticalEffectKind Kind { get; }
        public string SourceActorId { get; }
        public string TargetActorId { get; }
        public string OriginAttackId { get; }
        public long ApplicationOrder { get; }
        public long AppliedRevision { get; }
        public RuleTime AppliedAt { get; }
        public string ExpiryActorId { get; }
        public long ExpirySlot { get; }
        public SoldierTacticalEffectPhase ExpiryPhase { get; }
        public SoldierTacticalEffectStatus Status { get; }
        public long ResolvedRevision { get; }
        public string ResolutionId { get; }

        public SoldierTacticalEffectRecord(string id,SoldierTacticalEffectKind kind,string sourceActorId,string targetActorId,
            string originAttackId,long applicationOrder,long appliedRevision,RuleTime appliedAt,string expiryActorId,long expirySlot,
            SoldierTacticalEffectPhase expiryPhase,SoldierTacticalEffectStatus status=SoldierTacticalEffectStatus.Active,
            long resolvedRevision=0,string resolutionId="")
        {
            if(!Validation.ValidId(id)||!Enum.IsDefined(typeof(SoldierTacticalEffectKind),kind)||!Validation.ValidId(sourceActorId)
                ||!Validation.ValidId(targetActorId)||sourceActorId==targetActorId||!Validation.ValidId(originAttackId)||applicationOrder<0
                ||appliedRevision<1||!Validation.ValidId(expiryActorId)||expirySlot<0||!Enum.IsDefined(typeof(SoldierTacticalEffectPhase),expiryPhase)
                ||!Enum.IsDefined(typeof(SoldierTacticalEffectStatus),status)||resolvedRevision<0
                ||status==SoldierTacticalEffectStatus.Active&&(resolvedRevision!=0||resolutionId!="")
                ||status!=SoldierTacticalEffectStatus.Active&&(resolvedRevision<appliedRevision||!Validation.ValidId(resolutionId)))
                throw new ArgumentException("Invalid Soldier tactical effect.");
            Id=id;Kind=kind;SourceActorId=sourceActorId;TargetActorId=targetActorId;OriginAttackId=originAttackId;
            ApplicationOrder=applicationOrder;AppliedRevision=appliedRevision;AppliedAt=appliedAt;ExpiryActorId=expiryActorId;
            ExpirySlot=expirySlot;ExpiryPhase=expiryPhase;Status=status;ResolvedRevision=resolvedRevision;ResolutionId=resolutionId;
        }
        public SoldierTacticalEffectRecord Resolve(SoldierTacticalEffectStatus status,long revision,string resolutionId)
        {
            if(Status!=SoldierTacticalEffectStatus.Active||status==SoldierTacticalEffectStatus.Active)
                throw new InvalidOperationException("Only an active tactical effect can resolve.");
            return new SoldierTacticalEffectRecord(Id,Kind,SourceActorId,TargetActorId,OriginAttackId,ApplicationOrder,AppliedRevision,
                AppliedAt,ExpiryActorId,ExpirySlot,ExpiryPhase,status,revision,resolutionId);
        }
        public bool SameAs(SoldierTacticalEffectRecord x)=>x!=null&&Id==x.Id&&Kind==x.Kind&&SourceActorId==x.SourceActorId
            &&TargetActorId==x.TargetActorId&&OriginAttackId==x.OriginAttackId&&ApplicationOrder==x.ApplicationOrder
            &&AppliedRevision==x.AppliedRevision&&AppliedAt==x.AppliedAt&&ExpiryActorId==x.ExpiryActorId&&ExpirySlot==x.ExpirySlot
            &&ExpiryPhase==x.ExpiryPhase&&Status==x.Status&&ResolvedRevision==x.ResolvedRevision&&ResolutionId==x.ResolutionId;
    }

    /// <summary>Audit join from every admitted attack roll to its technique and consumed riders.</summary>
    public sealed class TacticalAttackAuditRecord
    {
        private readonly string[] consumedEffectIds;
        public string AttackId { get; }
        public string AttackerId { get; }
        public string TargetId { get; }
        public string TechniqueFeatureId { get; }
        public string[] ConsumedEffectIds=>consumedEffectIds.ToArray();
        public TacticalAttackAuditRecord(string attackId,string attackerId,string targetId,string techniqueFeatureId,string[] consumedEffectIds)
        {
            var used=consumedEffectIds??Array.Empty<string>();
            if(!Validation.ValidId(attackId)||!Validation.ValidId(attackerId)||!Validation.ValidId(targetId)||attackerId==targetId
                ||techniqueFeatureId==null||techniqueFeatureId!=""&&techniqueFeatureId!=CharacterFeatureIds.WarningShot&&techniqueFeatureId!=CharacterFeatureIds.CoveringFire
                ||used.Length>64||used.Any(x=>!Validation.ValidId(x))||used.Distinct(StringComparer.Ordinal).Count()!=used.Length)
                throw new ArgumentException("Invalid tactical attack audit.");
            AttackId=attackId;AttackerId=attackerId;TargetId=targetId;TechniqueFeatureId=techniqueFeatureId;this.consumedEffectIds=used.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
        }
        public bool SameAs(TacticalAttackAuditRecord x)=>x!=null&&AttackId==x.AttackId&&AttackerId==x.AttackerId&&TargetId==x.TargetId
            &&TechniqueFeatureId==x.TechniqueFeatureId&&consumedEffectIds.SequenceEqual(x.consumedEffectIds);
    }

    public sealed class SuppressionFireTargetResult
    {
        public string TargetActorId { get; }
        public int TargetX { get; }
        public int TargetY { get; }
        public int SaveNatural { get; }
        public int SaveModifier { get; }
        public long SaveTotal { get; }
        public bool SaveSucceeded { get; }
        public long Damage { get; }
        public long AfterDefense { get; }
        public uint SaveRandomBefore { get; }
        public uint SaveRandomAfter { get; }
        public long SaveWords { get; }
        public uint LifeRandomBefore { get; }
        public uint LifeRandomAfter { get; }
        public long LifeWords { get; }
        public bool SlowApplied=>!SaveSucceeded;
        public SuppressionFireTargetResult(string targetActorId,int targetX,int targetY,int saveNatural,int saveModifier,long saveTotal,bool saveSucceeded,long damage,
            long afterDefense,uint saveRandomBefore,uint saveRandomAfter,long saveWords,uint lifeRandomBefore,uint lifeRandomAfter,long lifeWords)
        {
            if(!Validation.ValidId(targetActorId)||targetX<0||targetY<0||saveNatural<0||saveNatural>20||saveModifier< -100||saveModifier>100
                ||saveNatural==0&&(saveTotal!=0||saveSucceeded||saveWords!=0||saveRandomBefore!=saveRandomAfter)
                ||saveNatural!=0&&saveTotal!=(long)saveNatural+saveModifier
                ||damage<0||afterDefense<0||afterDefense>damage||saveRandomBefore==0||saveRandomAfter==0
                ||lifeRandomBefore==0||lifeRandomAfter==0||saveWords<0||lifeWords<0)
                throw new ArgumentException("Invalid Suppression Fire target result.");
            TargetActorId=targetActorId;TargetX=targetX;TargetY=targetY;SaveNatural=saveNatural;SaveModifier=saveModifier;SaveTotal=saveTotal;SaveSucceeded=saveSucceeded;
            Damage=damage;AfterDefense=afterDefense;SaveRandomBefore=saveRandomBefore;SaveRandomAfter=saveRandomAfter;SaveWords=saveWords;
            LifeRandomBefore=lifeRandomBefore;LifeRandomAfter=lifeRandomAfter;LifeWords=lifeWords;
        }
        public bool SameAs(SuppressionFireTargetResult x)=>x!=null&&TargetActorId==x.TargetActorId&&TargetX==x.TargetX&&TargetY==x.TargetY&&SaveNatural==x.SaveNatural
            &&SaveModifier==x.SaveModifier&&SaveTotal==x.SaveTotal&&SaveSucceeded==x.SaveSucceeded&&Damage==x.Damage&&AfterDefense==x.AfterDefense
            &&SaveRandomBefore==x.SaveRandomBefore&&SaveRandomAfter==x.SaveRandomAfter&&SaveWords==x.SaveWords
            &&LifeRandomBefore==x.LifeRandomBefore&&LifeRandomAfter==x.LifeRandomAfter&&LifeWords==x.LifeWords;
    }

    public sealed class SuppressionFireVolleyRecord
    {
        private readonly string[] ammunitionLotIds;
        private readonly SuppressionFireTargetResult[] targets;
        private readonly int[] damageDice;
        public string Id { get; }
        public long Revision { get; }
        public int TurnOrdinal { get; }
        public string SourceActorId { get; }
        public string WeaponId { get; }
        public string[] AmmunitionLotIds=>(string[])ammunitionLotIds.Clone();
        public RuleTime At { get; }
        public int CenterX { get; }
        public int CenterY { get; }
        public int ClassLevel { get; }
        public int SaveDc { get; }
        public int[] DamageDice=>(int[])damageDice.Clone();
        public long DamageTotal { get; }
        public uint DamageRandomBefore { get; }
        public uint DamageRandomAfter { get; }
        public long DamageWords { get; }
        public SuppressionFireTargetResult[] Targets=>targets.ToArray();
        public SuppressionFireVolleyRecord(string id,long revision,int turnOrdinal,string sourceActorId,string weaponId,string[] ammunitionLotIds,
            RuleTime at,int centerX,int centerY,int classLevel,int saveDc,int[] damageDice,long damageTotal,uint damageRandomBefore,
            uint damageRandomAfter,long damageWords,SuppressionFireTargetResult[] targets)
        {
            var lots=ammunitionLotIds??Array.Empty<string>();var dice=damageDice??Array.Empty<int>();var hitTargets=targets??Array.Empty<SuppressionFireTargetResult>();
            if(!Validation.ValidId(id)||revision<1||turnOrdinal<0||!Validation.ValidId(sourceActorId)||!Validation.ValidId(weaponId)
                ||lots.Length!=3||lots.Any(x=>!Validation.ValidId(x))||centerX<0||centerY<0
                ||classLevel<1||classLevel>20||saveDc<0||dice.Length!=classLevel||dice.Any(x=>x<1||x>6)
                ||damageTotal!=dice.Sum(x=>(long)x)||damageRandomBefore==0||damageRandomAfter==0||damageWords<0
                ||hitTargets.Length<1||hitTargets.Length>3||hitTargets.Any(x=>x==null)
                ||hitTargets.Select(x=>x.TargetActorId).Distinct(StringComparer.Ordinal).Count()!=hitTargets.Length
                ||!hitTargets.Select(x=>x.TargetActorId).SequenceEqual(hitTargets.Select(x=>x.TargetActorId).OrderBy(x=>x,StringComparer.Ordinal)))
                throw new ArgumentException("Invalid Suppression Fire volley.");
            Id=id;Revision=revision;TurnOrdinal=turnOrdinal;SourceActorId=sourceActorId;WeaponId=weaponId;this.ammunitionLotIds=lots.ToArray();At=at;
            CenterX=centerX;CenterY=centerY;ClassLevel=classLevel;SaveDc=saveDc;this.damageDice=dice.ToArray();DamageTotal=damageTotal;
            DamageRandomBefore=damageRandomBefore;DamageRandomAfter=damageRandomAfter;DamageWords=damageWords;this.targets=hitTargets.ToArray();
        }
        public bool SameAs(SuppressionFireVolleyRecord x)=>x!=null&&Id==x.Id&&Revision==x.Revision&&TurnOrdinal==x.TurnOrdinal
            &&SourceActorId==x.SourceActorId&&WeaponId==x.WeaponId&&ammunitionLotIds.SequenceEqual(x.ammunitionLotIds)&&At==x.At
            &&CenterX==x.CenterX&&CenterY==x.CenterY&&ClassLevel==x.ClassLevel&&SaveDc==x.SaveDc&&damageDice.SequenceEqual(x.damageDice)
            &&DamageTotal==x.DamageTotal&&DamageRandomBefore==x.DamageRandomBefore&&DamageRandomAfter==x.DamageRandomAfter&&DamageWords==x.DamageWords
            &&targets.Length==x.targets.Length&&targets.Zip(x.targets,(a,b)=>a.SameAs(b)).All(v=>v);
    }

    public enum SuppressionSlowStatus { Active, Expired }
    public sealed class SuppressionSlowRecord
    {
        public string Id { get; }
        public string VolleyId { get; }
        public string SourceActorId { get; }
        public string TargetActorId { get; }
        public long AppliedRevision { get; }
        public long ExpirySlot { get; }
        public SuppressionSlowStatus Status { get; }
        public long ResolvedRevision { get; }
        public string ResolutionId { get; }
        public SuppressionSlowRecord(string id,string volleyId,string sourceActorId,string targetActorId,long appliedRevision,long expirySlot,
            SuppressionSlowStatus status=SuppressionSlowStatus.Active,long resolvedRevision=0,string resolutionId="")
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(volleyId)||!Validation.ValidId(sourceActorId)||!Validation.ValidId(targetActorId)
                ||sourceActorId==targetActorId||appliedRevision<1||expirySlot<0||!Enum.IsDefined(typeof(SuppressionSlowStatus),status)
                ||resolvedRevision<0||status==SuppressionSlowStatus.Active&&(resolvedRevision!=0||resolutionId!="")
                ||status==SuppressionSlowStatus.Expired&&(resolvedRevision<appliedRevision||!Validation.ValidId(resolutionId)))
                throw new ArgumentException("Invalid Suppression Fire slow.");
            Id=id;VolleyId=volleyId;SourceActorId=sourceActorId;TargetActorId=targetActorId;AppliedRevision=appliedRevision;ExpirySlot=expirySlot;
            Status=status;ResolvedRevision=resolvedRevision;ResolutionId=resolutionId;
        }
        public SuppressionSlowRecord Expire(long revision,string marker)
        {if(Status!=SuppressionSlowStatus.Active)throw new InvalidOperationException("Suppression slow already ended.");
            return new SuppressionSlowRecord(Id,VolleyId,SourceActorId,TargetActorId,AppliedRevision,ExpirySlot,SuppressionSlowStatus.Expired,revision,marker);}
        public bool SameAs(SuppressionSlowRecord x)=>x!=null&&Id==x.Id&&VolleyId==x.VolleyId&&SourceActorId==x.SourceActorId
            &&TargetActorId==x.TargetActorId&&AppliedRevision==x.AppliedRevision&&ExpirySlot==x.ExpirySlot&&Status==x.Status
            &&ResolvedRevision==x.ResolvedRevision&&ResolutionId==x.ResolutionId;
    }

    public static class SoldierTacticalFeatureValidation
    {
        public const int MaxEffects=256,MaxAttackAudits=256,MaxAllies=64,MaxAssessments=128,MaxSuppressionVolleys=128,MaxSuppressionSlows=384;
        public static void Validate(Snapshot s)
        {
            if(s.TacticalAllies==null||s.SoldierTacticalEffects==null||s.TacticalAttackAudits==null||s.TacticalAssessments==null
                ||s.SuppressionFireVolleys==null||s.SuppressionSlows==null
                ||s.TacticalAllies.Length>MaxAllies||s.SoldierTacticalEffects.Length>MaxEffects||s.TacticalAttackAudits.Length>MaxAttackAudits
                ||s.TacticalAssessments.Length>MaxAssessments||s.SuppressionFireVolleys.Length>MaxSuppressionVolleys
                ||s.SuppressionSlows.Length>MaxSuppressionSlows||s.TacticalAllies.Any(x=>x==null)||s.SoldierTacticalEffects.Any(x=>x==null)
                ||s.TacticalAttackAudits.Any(x=>x==null)||s.TacticalAssessments.Any(x=>x==null)||s.SuppressionFireVolleys.Any(x=>x==null)
                ||s.SuppressionSlows.Any(x=>x==null))
                throw new ArgumentException("Invalid Soldier tactical feature collections.");
            if(s.SchemaVersion<Snapshot.SoldierTacticalTechniquesSchema) {
                if(s.TacticalAllies.Length+s.SoldierTacticalEffects.Length+s.TacticalAttackAudits.Length+s.TacticalAssessments.Length
                    +s.SuppressionFireVolleys.Length+s.SuppressionSlows.Length!=0
                    ||s.CharacterFeatureRuntime.Any(x=>x.WarningShotRechargeRemaining!=0||x.CoveringFireRechargeRemaining!=0
                        ||x.TacticalAssessmentRechargeRemaining!=0||x.SuppressionFireRechargeRemaining!=0))
                    throw new ArgumentException("Soldier tactical techniques require schema29.");
                return;
            }
            if(s.SchemaVersion<Snapshot.TacticalAssessmentSchema&&(s.TacticalAssessments.Length!=0
                ||s.CharacterFeatureRuntime.Any(x=>x.TacticalAssessmentRechargeRemaining!=0)))
                throw new ArgumentException("Tactical Assessment requires schema31.");
            if(s.SchemaVersion<Snapshot.SuppressionFireSchema&&(s.SuppressionFireVolleys.Length+s.SuppressionSlows.Length!=0
                ||s.CharacterFeatureRuntime.Any(x=>x.SuppressionFireRechargeRemaining!=0)))
                throw new ArgumentException("Suppression Fire requires schema33.");
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            bool Ally(string first,string second)=>first==second||s.TacticalAllies.Any(x=>x.Includes(first)&&x.Other(first)==second);
            long FutureStartSlot(string actor,long currentSlot)
            {
                int index=Array.IndexOf(s.WorldSchedule.Order.ToArray(),actor);if(index<0)return -1;
                long count=s.WorldSchedule.Order.Count,candidate=index;
                if(candidate<=currentSlot)candidate=checked(candidate+checked(((currentSlot-candidate)/count+1)*count));
                return candidate;
            }
            var audits=s.TacticalAttackAudits.ToDictionary(x=>x.AttackId,StringComparer.Ordinal);
            var attacks=s.RangedAttacks.Select(x=>new {x.Id,x.Revision,x.AttackerId,x.TargetId,x.Attack.Hit,x.At})
                .Concat(s.MeleeAttacks.Select(x=>new {x.Id,x.Revision,x.AttackerId,x.TargetId,x.Attack.Hit,x.At})).ToArray();
            bool ValidTechniqueAudit(TacticalAttackAuditRecord audit)
            {
                if(audit.TechniqueFeatureId=="")return true;
                var attack=s.RangedAttacks.SingleOrDefault(x=>x.Id==audit.AttackId);
                if(attack==null||!s.CharacterFeatureGrants.Any(g=>g.ActorId==audit.AttackerId&&g.FeatureId==audit.TechniqueFeatureId
                    &&g.Origin==CharacterFeatureGrantOrigin.InitialClassSelection))return false;
                var kind=audit.TechniqueFeatureId==CharacterFeatureIds.WarningShot?SoldierTacticalEffectKind.WarningShot:SoldierTacticalEffectKind.CoveringFire;
                return s.SoldierTacticalEffects.Count(x=>x.OriginAttackId==audit.AttackId&&x.Kind==kind)==(attack.Attack.Hit?1:0);
            }
            bool ValidEffect(SoldierTacticalEffectRecord effect)
            {
                long appliedSlot=s.WorldSchedule.SlotAt(effect.AppliedAt);
                string expectedExpiryActor=effect.Kind==SoldierTacticalEffectKind.WarningShot?effect.TargetActorId:effect.SourceActorId;
                long expectedExpirySlot=FutureStartSlot(expectedExpiryActor,appliedSlot);
                if(!Actor(effect.SourceActorId)||!Actor(effect.TargetActorId)||!Actor(effect.ExpiryActorId)||effect.AppliedRevision>s.Revision
                    ||effect.ResolvedRevision>s.Revision||effect.AppliedAt>s.RuleClock||!s.WorldSchedule.Order.Contains(effect.ExpiryActorId)
                    ||effect.ExpiryActorId!=expectedExpiryActor||effect.ExpirySlot!=expectedExpirySlot)return false;
                if(!audits.TryGetValue(effect.OriginAttackId,out var origin)||origin.AttackerId!=effect.SourceActorId||origin.TargetId!=effect.TargetActorId
                    ||origin.TechniqueFeatureId!=(effect.Kind==SoldierTacticalEffectKind.WarningShot?CharacterFeatureIds.WarningShot:CharacterFeatureIds.CoveringFire)
                    ||!s.CharacterFeatureGrants.Any(g=>g.ActorId==effect.SourceActorId&&g.FeatureId==origin.TechniqueFeatureId
                        &&g.Origin==CharacterFeatureGrantOrigin.InitialClassSelection)
                    ||!attacks.Any(a=>a.Id==effect.OriginAttackId&&a.Hit&&a.Revision==effect.AppliedRevision&&a.At==effect.AppliedAt))return false;
                if(effect.Kind==SoldierTacticalEffectKind.WarningShot&&(effect.ExpiryActorId!=effect.TargetActorId||effect.ExpiryPhase!=SoldierTacticalEffectPhase.End))return false;
                if(effect.Kind==SoldierTacticalEffectKind.CoveringFire&&(effect.ExpiryActorId!=effect.SourceActorId||effect.ExpiryPhase!=SoldierTacticalEffectPhase.Start))return false;
                if(effect.Status==SoldierTacticalEffectStatus.Active)
                    return effect.ExpiryPhase==SoldierTacticalEffectPhase.Start?s.WorldSchedule.ProcessedSlot<effect.ExpirySlot
                        :s.WorldSchedule.ProcessedSlot<=effect.ExpirySlot;
                if(effect.Status==SoldierTacticalEffectStatus.Consumed) {
                    var consumingAttack=attacks.SingleOrDefault(a=>a.Id==effect.ResolutionId);
                    return audits.TryGetValue(effect.ResolutionId,out var consumer)&&consumer.AttackerId==effect.TargetActorId
                        &&consumer.ConsumedEffectIds.Contains(effect.Id,StringComparer.Ordinal)&&consumingAttack!=null
                        &&consumingAttack.Revision==effect.ResolvedRevision&&consumingAttack.Revision>effect.AppliedRevision
                        &&(effect.Kind!=SoldierTacticalEffectKind.CoveringFire
                            ||consumingAttack.TargetId!=effect.SourceActorId&&Ally(effect.SourceActorId,consumingAttack.TargetId))
                        &&consumingAttack.At<s.WorldSchedule.Start(effect.ExpiryPhase==SoldierTacticalEffectPhase.End
                            ?checked(effect.ExpirySlot+1):effect.ExpirySlot);
                }
                if(effect.Status==SoldierTacticalEffectStatus.Replaced)
                    return effect.Kind==SoldierTacticalEffectKind.CoveringFire&&s.SoldierTacticalEffects.Any(n=>n.Id==effect.ResolutionId
                        &&n.Kind==SoldierTacticalEffectKind.CoveringFire&&n.TargetActorId==effect.TargetActorId&&n.AppliedRevision==effect.ResolvedRevision
                        &&n.AppliedRevision>effect.AppliedRevision&&n.ApplicationOrder>effect.ApplicationOrder);
                string expected=effect.ExpiryPhase==SoldierTacticalEffectPhase.End
                    ?s.WorldSchedule.MarkerId(effect.ExpirySlot+1)+".end":s.WorldSchedule.MarkerId(effect.ExpirySlot)+".start";
                return effect.Status==SoldierTacticalEffectStatus.Expired&&effect.ResolutionId==expected
                    &&(effect.ExpiryPhase==SoldierTacticalEffectPhase.Start?s.WorldSchedule.ProcessedSlot>=effect.ExpirySlot
                        :s.WorldSchedule.ProcessedSlot>effect.ExpirySlot);
            }
            bool ValidAssessment(TacticalAssessmentRecord assessment)
            {
                if(s.SchemaVersion<Snapshot.TacticalAssessmentSchema||!Actor(assessment.SourceActorId)||!Actor(assessment.AllyActorId)
                    ||!Actor(assessment.EnemyActorId)||!Ally(assessment.SourceActorId,assessment.AllyActorId)
                    ||assessment.AppliedRevision>s.Revision||assessment.ResolvedRevision>s.Revision||assessment.AppliedAt>s.RuleClock
                    ||!s.CharacterFeatureGrants.Any(g=>g.ActorId==assessment.SourceActorId&&g.FeatureId==CharacterFeatureIds.TacticalAssessment
                        &&g.Origin==CharacterFeatureGrantOrigin.SelectedCard&&g.ClassLevel==3))return false;
                var receipt=s.Receipts.SingleOrDefault(r=>r.Id==assessment.Id&&r.Revision==assessment.AppliedRevision);
                if(receipt==null)return false;
                var command=CommandHistory.Read(receipt);
                long appliedSlot=s.WorldSchedule.SlotAt(assessment.AppliedAt);
                if(command.Kind!=CommandKind.TacticalAssessment||command.Actor!=assessment.SourceActorId||command.Target!=assessment.EnemyActorId
                    ||command.Combat==null||command.Combat.WeaponId!=assessment.AllyActorId||command.Combat.TurnId==""
                    ||assessment.ExpirySlot!=FutureStartSlot(assessment.SourceActorId,appliedSlot))return false;
                if(assessment.Status==TacticalAssessmentStatus.Active)return s.WorldSchedule.ProcessedSlot<=assessment.ExpirySlot;
                if(assessment.Status==TacticalAssessmentStatus.Consumed) {
                    var attack=attacks.SingleOrDefault(a=>a.Id==assessment.ResolutionId);
                    return attack!=null&&attack.AttackerId==assessment.AllyActorId&&attack.TargetId==assessment.EnemyActorId
                        &&attack.Revision==assessment.ResolvedRevision&&attack.Revision>assessment.AppliedRevision
                        &&audits.TryGetValue(assessment.ResolutionId,out var audit)&&audit.ConsumedEffectIds.Contains(assessment.Id,StringComparer.Ordinal)
                        &&attack.At<s.WorldSchedule.Start(checked(assessment.ExpirySlot+1));
                }
                string expected=s.WorldSchedule.MarkerId(checked(assessment.ExpirySlot+1))+".end";
                return assessment.Status==TacticalAssessmentStatus.Expired&&assessment.ResolutionId==expected
                    &&s.WorldSchedule.ProcessedSlot>assessment.ExpirySlot;
            }
            bool ValidSuppressionVolley(SuppressionFireVolleyRecord volley)
            {
                if(s.SchemaVersion<Snapshot.SuppressionFireSchema||!Actor(volley.SourceActorId)||!s.WorldSchedule.Order.Contains(volley.SourceActorId)
                    ||volley.Revision>s.Revision||volley.At>s.RuleClock||volley.TurnOrdinal<0
                    ||!s.CharacterFeatureGrants.Any(g=>g.ActorId==volley.SourceActorId&&g.FeatureId==CharacterFeatureIds.SuppressionFire
                        &&g.ClassName=="Soldier"&&g.ClassLevel==3&&g.Origin==CharacterFeatureGrantOrigin.SelectedCard))return false;
                var receipt=s.Receipts.SingleOrDefault(r=>r.Id==volley.Id&&r.Revision==volley.Revision);if(receipt==null)return false;
                Command command;try{command=CommandHistory.Read(receipt);}catch(ArgumentException){return false;}
                if(command.Kind!=CommandKind.SuppressionFire||command.Actor!=volley.SourceActorId||command.SuppressionFire==null
                    ||command.SuppressionFire.WeaponId!=volley.WeaponId||command.X!=volley.CenterX||command.Y!=volley.CenterY
                    ||!command.SuppressionFire.TargetIds.SequenceEqual(volley.Targets.Select(x=>x.TargetActorId),StringComparer.Ordinal)
                    ||volley.WeaponId!="TEST_ONLY.actor-repeating-crossbow")return false;
                if(volley.ClassLevel!=3||volley.SaveDc<8||volley.DamageDice.Length!=volley.ClassLevel)return false;
                uint damageState=volley.DamageRandomBefore;long damageWords=0;
                foreach(int die in volley.DamageDice){var draw=DiceStream.Draw(damageState,6);if(draw.Value+1!=die)return false;damageState=draw.NextState;damageWords=checked(damageWords+draw.WordsConsumed);}
                if(damageState!=volley.DamageRandomAfter||damageWords!=volley.DamageWords)return false;
                long appliedSlot=s.WorldSchedule.SlotAt(volley.At),expiry=FutureStartSlot(volley.SourceActorId,appliedSlot);
                if(expiry<0)return false;
                uint sequence=volley.DamageRandomAfter;
                foreach(var targetResult in volley.Targets) {
                    string targetId=targetResult.TargetActorId;
                    if(!Actor(targetId)||targetId==volley.SourceActorId||Ally(volley.SourceActorId,targetId)
                        ||!s.WorldSchedule.Order.Contains(targetId)||Math.Abs((long)targetResult.TargetX-volley.CenterX)>1
                        ||Math.Abs((long)targetResult.TargetY-volley.CenterY)>1
                        ||targetResult.SaveTotal!=(targetResult.SaveNatural==0?0L:(long)targetResult.SaveNatural+targetResult.SaveModifier)
                        ||targetResult.SaveSucceeded!=(targetResult.SaveTotal>=volley.SaveDc)
                        ||targetResult.Damage!=(targetResult.SaveSucceeded?volley.DamageTotal/2:volley.DamageTotal)
                        ||targetResult.SaveRandomBefore!=sequence||targetResult.LifeRandomBefore!=targetResult.SaveRandomAfter)return false;
                    if(targetResult.SaveNatural==0) {
                        if(targetResult.SaveSucceeded||targetResult.SaveWords!=0||targetResult.SaveRandomBefore!=targetResult.SaveRandomAfter)return false;
                    } else {
                        var save=DiceStream.Draw(sequence,20);
                        if(save.Value+1!=targetResult.SaveNatural||save.NextState!=targetResult.SaveRandomAfter||save.WordsConsumed!=targetResult.SaveWords)return false;
                    }
                    sequence=targetResult.LifeRandomAfter;
                }
                return true;
            }
            bool ValidSuppressionSlow(SuppressionSlowRecord slow)
            {
                var volley=s.SuppressionFireVolleys.SingleOrDefault(x=>x.Id==slow.VolleyId);
                if(volley==null||slow.SourceActorId!=volley.SourceActorId||slow.AppliedRevision!=volley.Revision
                    ||!volley.Targets.Any(x=>x.TargetActorId==slow.TargetActorId&&!x.SaveSucceeded)
                    ||slow.ExpirySlot!=FutureStartSlot(slow.SourceActorId,s.WorldSchedule.SlotAt(volley.At)))return false;
                if(slow.Status==SuppressionSlowStatus.Active)return s.WorldSchedule.ProcessedSlot<=slow.ExpirySlot;
                string expected=s.WorldSchedule.MarkerId(checked(slow.ExpirySlot+1))+".end";
                return slow.ResolutionId==expected&&slow.ResolvedRevision<=s.Revision&&s.WorldSchedule.ProcessedSlot>slow.ExpirySlot;
            }
            if(s.TacticalAllies.Select(x=>x.FirstActorId+"|"+x.SecondActorId).Distinct(StringComparer.Ordinal).Count()!=s.TacticalAllies.Length
                ||s.TacticalAllies.Any(x=>!Actor(x.FirstActorId)||!Actor(x.SecondActorId))
                ||s.TacticalAttackAudits.Select(x=>x.AttackId).Distinct(StringComparer.Ordinal).Count()!=s.TacticalAttackAudits.Length
                ||attacks.Length!=s.TacticalAttackAudits.Length
                ||s.TacticalAttackAudits.Any(x=>!Actor(x.AttackerId)||!Actor(x.TargetId)||!attacks.Any(a=>a.Id==x.AttackId&&a.AttackerId==x.AttackerId
                    &&a.TargetId==x.TargetId&&a.Revision<=s.Revision)||x.ConsumedEffectIds.Any(id=>
                        !s.SoldierTacticalEffects.Any(e=>e.Id==id&&e.Status==SoldierTacticalEffectStatus.Consumed&&e.ResolutionId==x.AttackId)
                        &&!s.TacticalAssessments.Any(e=>e.Id==id&&e.Status==TacticalAssessmentStatus.Consumed&&e.ResolutionId==x.AttackId))
                    ||!ValidTechniqueAudit(x)
                    ||x.TechniqueFeatureId!=""&&(!s.RangedAttacks.Any(a=>a.Id==x.AttackId)
                        ||!s.CharacterFeatureGrants.Any(g=>g.ActorId==x.AttackerId&&g.FeatureId==x.TechniqueFeatureId
                            &&g.Origin==CharacterFeatureGrantOrigin.InitialClassSelection)))
                ||s.SoldierTacticalEffects.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.SoldierTacticalEffects.Length
                ||s.SoldierTacticalEffects.Select(x=>x.ApplicationOrder).Distinct().Count()!=s.SoldierTacticalEffects.Length
                ||s.SoldierTacticalEffects.Any(x=>!ValidEffect(x))
                ||s.TacticalAssessments.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.TacticalAssessments.Length
                ||s.TacticalAssessments.Any(x=>!ValidAssessment(x))
                ||s.SuppressionFireVolleys.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.SuppressionFireVolleys.Length
                ||s.SuppressionFireVolleys.Select(x=>x.Revision).Distinct().Count()!=s.SuppressionFireVolleys.Length
                ||s.SuppressionFireVolleys.Any(x=>!ValidSuppressionVolley(x))
                ||s.SuppressionSlows.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.SuppressionSlows.Length
                ||s.SuppressionSlows.Any(x=>!ValidSuppressionSlow(x))
                ||s.SuppressionSlows.Where(x=>x.Status==SuppressionSlowStatus.Active).GroupBy(x=>x.TargetActorId,StringComparer.Ordinal)
                    .Any(g=>g.Count()>1)
                ||s.SoldierTacticalEffects.Where(x=>x.Status==SoldierTacticalEffectStatus.Active&&x.Kind==SoldierTacticalEffectKind.CoveringFire)
                    .GroupBy(x=>x.TargetActorId,StringComparer.Ordinal).Any(x=>x.Count()>1))
                throw new ArgumentException("Invalid Soldier tactical feature history.");
            foreach(var runtime in s.CharacterFeatureRuntime) {
                if((runtime.WarningShotRechargeRemaining>0&&!s.CharacterFeatureGrants.Any(x=>x.ActorId==runtime.ActorId&&x.FeatureId==CharacterFeatureIds.WarningShot
                        &&x.Origin==CharacterFeatureGrantOrigin.InitialClassSelection))
                    ||(runtime.CoveringFireRechargeRemaining>0&&!s.CharacterFeatureGrants.Any(x=>x.ActorId==runtime.ActorId&&x.FeatureId==CharacterFeatureIds.CoveringFire
                        &&x.Origin==CharacterFeatureGrantOrigin.InitialClassSelection))
                    ||(runtime.TacticalAssessmentRechargeRemaining>0&&!s.CharacterFeatureGrants.Any(x=>x.ActorId==runtime.ActorId
                        &&x.FeatureId==CharacterFeatureIds.TacticalAssessment&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard))
                    ||(runtime.SuppressionFireRechargeRemaining>0&&!s.CharacterFeatureGrants.Any(x=>x.ActorId==runtime.ActorId
                        &&x.FeatureId==CharacterFeatureIds.SuppressionFire&&x.ClassLevel==3&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard)))
                    throw new ArgumentException("Unowned Soldier tactical feature has recharge state.");
            }
        }
    }
}
