using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Event-time qualification. Current conditions and geometry are never substituted for these historical facts.</summary>
    public sealed class AuraOfFaithQualification
    {
        public string OwnerId => ClericRpProfile.Actor;
        public string SourceId => BishopProfile.Aura;
        public string SourceRevision => ClericRpProfile.SourceRevision;
        public long AcquiredRevision { get; }
        public string TargetId { get; }
        public bool OwnerConscious { get; }
        public bool Allied { get; }
        public bool RecipientConscious { get; }
        public bool Perceived { get; }
        public RuleQuantity OwnerX { get; }
        public RuleQuantity OwnerY { get; }
        public RuleQuantity TargetX { get; }
        public RuleQuantity TargetY { get; }
        public RuleQuantity DistanceFeet { get; }
        public bool Qualified => OwnerConscious&&Allied&&RecipientConscious&&Perceived&&DistanceFeet<=new RuleQuantity(15);
        public int Bonus => Qualified?1:0;
        public AuraOfFaithQualification(long acquired,string target,bool ownerConscious,bool allied,bool recipientConscious,bool perceived,
            RuleQuantity ownerX,RuleQuantity ownerY,RuleQuantity targetX,RuleQuantity targetY)
        {
            if(acquired<1||!Validation.ValidId(target)||perceived&&!recipientConscious)throw new ArgumentException("Invalid Aura qualification.");
            AcquiredRevision=acquired;TargetId=target;OwnerConscious=ownerConscious;Allied=allied;RecipientConscious=recipientConscious;Perceived=perceived;
            OwnerX=ownerX;OwnerY=ownerY;TargetX=targetX;TargetY=targetY;
            var dx=ownerX>=targetX?ownerX-targetX:targetX-ownerX;var dy=ownerY>=targetY?ownerY-targetY:targetY-ownerY;
            DistanceFeet=(dx>=dy?dx:dy).Scale(5);
        }
    }
    public enum AuraSaveConsumer { Frightened, Sanctuary, Concentration, Wound, Push, SuppressionFire, HuntingTrap }
    public sealed class AuraOfFaithSaveRecord
    {
        public string Id { get; }
        public string CauseId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public AuraSaveConsumer Consumer { get; }
        public AuraOfFaithQualification Qualification { get; }
        public int BaseModifier { get; }
        public int OtherTemporaryBonus { get; }
        public int EffectiveTemporaryBonus => Math.Max(OtherTemporaryBonus,Qualification.Bonus);
        public int AuraContribution => EffectiveTemporaryBonus-OtherTemporaryBonus;
        public int Modifier => checked(BaseModifier+EffectiveTemporaryBonus);
        public long Dc { get; }
        public int Natural { get; }
        public long Total => AutomaticFailure?0:(long)Natural+Modifier;
        public bool AutomaticFailure { get; }
        public bool Success { get; }
        public bool OutcomeChangedByAura => !AutomaticFailure&&Success&&(long)Natural+BaseModifier+OtherTemporaryBonus<Dc;
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public AuraOfFaithSaveRecord(string id,string cause,long revision,RuleTime at,AuraSaveConsumer consumer,AuraOfFaithQualification qualification,
            int basis,int otherTemporary,long dc,int natural,bool automatic,bool success,uint randomBefore,uint randomAfter,long words)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(cause)||revision<1||qualification==null||!Enum.IsDefined(typeof(AuraSaveConsumer),consumer)
                ||otherTemporary<0||dc<0||words<0||automatic&&(natural!=0||success||words!=0||randomBefore!=randomAfter)
                ||!automatic&&(natural<1||natural>20||words<1||success!=((long)natural+basis+Math.Max(otherTemporary,qualification.Bonus)>=dc)))
                throw new ArgumentException("Invalid Aura saving-throw settlement.");
            Id=id;CauseId=cause;Revision=revision;At=at;Consumer=consumer;Qualification=qualification;BaseModifier=basis;OtherTemporaryBonus=otherTemporary;
            Dc=dc;Natural=natural;AutomaticFailure=automatic;Success=success;RandomBefore=randomBefore;RandomAfter=randomAfter;WordsConsumed=words;
        }
    }
    public sealed class AuraOfFaithHealingRecord
    {
        public string RiteCommandId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public AuraOfFaithQualification Qualification { get; }
        public long BaseGain { get; }
        public long HpBefore { get; }
        public long Requested => Qualification.Bonus;
        public long Potential { get; }
        public long HpAfter { get; }
        public long ActualGain => HpAfter-HpBefore;
        public AuraOfFaithHealingRecord(string rite,long revision,RuleTime at,AuraOfFaithQualification qualification,long baseGain,long before,long potential,long after)
        {
            if(!Validation.ValidId(rite)||revision<1||qualification==null||baseGain<1||before<0||potential<0||potential>qualification.Bonus
                ||after<before||after-before>potential)throw new ArgumentException("Invalid Aura Rite healing settlement.");
            RiteCommandId=rite;Revision=revision;At=at;Qualification=qualification;BaseGain=baseGain;HpBefore=before;Potential=potential;HpAfter=after;
        }
    }
    public static partial class BishopProfile
    {
        internal static void ValidateAura(Snapshot s)
        {
            var saves=s.BishopEntry.AuraSaves;var heals=s.BishopEntry.AuraHealing;
            if(saves.Count>2048||heals.Count>128||saves.Select(x=>x.Id).Distinct().Count()!=saves.Count
                ||heals.Select(x=>x.RiteCommandId).Distinct().Count()!=heals.Count
                ||!saves.Select(x=>x.Revision).SequenceEqual(saves.Select(x=>x.Revision).OrderBy(x=>x))
                ||!heals.Select(x=>x.Revision).SequenceEqual(heals.Select(x=>x.Revision).OrderBy(x=>x)))throw new ArgumentException("Invalid Aura history coverage.");
            void Qualified(AuraOfFaithQualification q,long revision,RuleTime at) {
                if(!Earned(s)||q.AcquiredRevision!=Advancement(s).Revision||revision<=q.AcquiredRevision||revision>s.Revision||at>s.RuleClock
                    ||!s.Actors.Any(x=>x.Id==q.TargetId)||!s.Receipts.Any(x=>x.Revision==revision))throw new ArgumentException("Unattributed Aura event.");
            }
            foreach(var save in saves) {
                Qualified(save.Qualification,save.Revision,save.At);
                // Exact source save, sensory facts, strongest-flat arbitration and pending Wound identity are replayed by the selected policy.
                if(save.Consumer==AuraSaveConsumer.Frightened&&!s.FrightenedSaves.Any(x=>x.Id==save.CauseId&&x.Revision==save.Revision
                    &&x.TargetId==save.Qualification.TargetId&&x.Modifier==save.Modifier&&x.Natural==save.Natural&&x.Success==save.Success)
                    ||(save.Consumer==AuraSaveConsumer.Concentration||save.Consumer==AuraSaveConsumer.Sanctuary)
                        &&!s.SpellSaves.Any(x=>x.Id==save.CauseId&&x.Revision==save.Revision&&x.SubjectId==save.Qualification.TargetId
                            &&x.Modifier==save.Modifier&&x.Natural==save.Natural&&x.Success==save.Success))
                    throw new ArgumentException("Aura contribution lacks its actual source save.");
            }
            foreach(var heal in heals) {
                Qualified(heal.Qualification,heal.Revision,heal.At);
                var rite=s.HealingRites.SingleOrDefault(x=>x.CommandId==heal.RiteCommandId);
                var radiance=s.RadianceUses.SingleOrDefault(x=>x.RiteCommandId==heal.RiteCommandId);
                if(rite==null||rite.Revision!=heal.Revision||rite.At!=heal.At||rite.TargetId!=heal.Qualification.TargetId
                    ||rite.ActualGain!=heal.BaseGain||heal.HpBefore!=(radiance?.HpAfter??ConsecrationProfile.AfterGround(s,rite)))throw new ArgumentException("Aura healing did not follow its positive base Rite and Radiance.");
            }
        }
    }
}
