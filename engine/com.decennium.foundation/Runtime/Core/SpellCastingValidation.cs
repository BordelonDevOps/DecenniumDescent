using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static partial class SpellCastingProfile
    {
        // The selected policy also reconstructs every accepted command. These checks prevent a
        // structurally inconsistent envelope from being treated as a candidate for that replay.
        internal static void Validate(Snapshot s)
        {
            bool selected=SelectedFingerprint(s.ContentFingerprint);
            if(s.ConnectedClericCasting!=selected)throw new ArgumentException("Invalid casting envelope selection.");
            Rows(s.CastingStrain,1,selected); Rows(s.SpellCasts,MaxCasts,selected); Rows(s.CastingActivities,MaxActivities,selected);
            Rows(s.CastingTurnEnds,MaxTurnEnds,selected); Rows(s.SpellEffects,MaxEffects,selected); Rows(s.GuidanceUses,MaxGuidanceUses,selected);
            Rows(s.SpellSaves,MaxSaves,selected); Rows(s.SanctuaryAdmissions,MaxAdmissions,selected);
            Rows(s.DetectMagicFocuses,MaxFocuses,selected); Rows(s.ConsumableContamination,MaxContamination,selected);
            if(!selected)return;
            if(!s.TestOnly || !s.ConnectedClericSettlement || s.SchemaVersion!=Snapshot.SurpriseEntrySchema
                || s.CastingStrain.Length!=1 || s.CastingStrain[0].ActorId!=ClericRpProfile.Actor)
                throw new ArgumentException("Casting requires its exact connected character and history.");
            ValidateCompanionClubPickup(s);
            var focusItem=s.PortableEquipment.SingleOrDefault(x=>x.Id==FocusId);
            if(!IsFocus(s,focusItem) || focusItem.OwnerId!=ClericRpProfile.Actor || focusItem.ParentId!=""
                || focusItem.LinkKind!=PortableLinkKind.None || focusItem.MassBasis!=PortableMassBasis.Fixed
                || focusItem.SourceWeightLb!=new RuleQuantity(1) || focusItem.OperationalWeightLb!=new RuleQuantity(1)
                || focusItem.PrintedLoad.HasValue || focusItem.CapacityPounds.HasValue || !focusItem.Wearable || focusItem.Open
                || focusItem.FitRuleId!="" || focusItem.Placement==PortablePlacement.Contained || focusItem.Placement==PortablePlacement.Attached
                || focusItem.HeldHands!=(focusItem.Placement==PortablePlacement.Carried?1:0))
                throw new ArgumentException("Invalid declared physical focus.");
            var water=s.InventoryLots.SingleOrDefault(x=>x.LotId==ContaminatedWaterId);
            if(water==null || water.ParentId!="" || water.CreatedAmount!=new RuleQuantity(1) || water.CreatedAt!=default
                || water.OwnerId!=ClericRpProfile.Actor || water.Nutrition!=NutritionKind.WaterPints || water.FreshUntil.HasValue)
                throw new ArgumentException("Invalid finite initial contaminated-water origin.");
            Unique(s.SpellCasts.Select(x=>x.CommandId)); Unique(s.SpellEffects.Select(x=>x.Id)); Unique(s.GuidanceUses.Select(x=>x.EffectId));
            Unique(s.CastingActivities.Select(x=>x.CommandId)); Unique(s.CastingTurnEnds.Select(x=>x.Turn.Binding));
            Unique(s.SpellSaves.Select(x=>x.Id)); Unique(s.SanctuaryAdmissions.Select(x=>x.Id)); Unique(s.DetectMagicFocuses.Select(x=>x.CommandId));
            Unique(s.ConsumableContamination.Select(x=>x.Id));
            Ordered(s.SpellCasts.Select(x=>x.Revision)); Ordered(s.CastingActivities.Select(x=>x.Revision));
            Ordered(s.CastingTurnEnds.Select(x=>x.Revision)); Ordered(s.SpellSaves.Select(x=>x.Revision));
            Ordered(s.GuidanceUses.Select(x=>x.Revision)); Ordered(s.DetectMagicFocuses.Select(x=>x.Revision));
            foreach(var cast in s.SpellCasts) {
                var command=Receipt(s,cast.CommandId,cast.Revision);
                var known=s.KnownSpells.SingleOrDefault(x=>x.ActorId==cast.ActorId && x.SpellId==cast.SpellId);
                int level=1+s.CharacterAdvancements.Count(x=>x.ActorId==cast.ActorId && x.Revision<cast.Revision);
                if(command.Kind!=CommandKind.CastKnownSpell || command.Actor!=cast.ActorId || command.Target!=cast.TargetId
                    || command.SpellCast==null || command.SpellCast.SpellId!=cast.SpellId || command.SpellCast.FocusItemId!=cast.FocusItemId
                    || command.SpellCast.ElectFocusedDc!=cast.FocusedDcElected || command.SpellCast.WillingTarget!=cast.WillingTarget
                    || cast.ActorId!=ClericRpProfile.Actor || known==null || known.AcquiredRevision!=cast.KnownAcquiredRevision
                    || known.AcquiredRevision>=cast.Revision || cast.ClassLevel!=level || cast.Proficiency!=2 || cast.CastingModifier!=2
                    || cast.At>s.RuleClock || cast.FocusItemId!="" && cast.FocusItemId!=FocusId
                    || !ValidTurn(s,cast.Turn,cast.At,true))throw new ArgumentException("Unqualified casting payment or historical access.");
                var activity=s.CastingActivities.SingleOrDefault(x=>x.CommandId==cast.CommandId);
                if(activity==null || activity.Kind!=CastingActivityKind.Spell || activity.Revision!=cast.Revision
                    || !activity.Turn.SameAs(cast.Turn) || activity.At!=cast.At)throw new ArgumentException("Missing cast activity.");
                if(cast.EffectId!="" && !s.SpellEffects.Any(x=>x.Id==cast.EffectId && x.CastId==cast.CommandId))
                    throw new ArgumentException("Missing cast effect.");
                if(cast.SpellId=="spare-the-dying") {
                    var draw=DiceStream.Draw(cast.RandomBefore,4);
                    if(draw.Value+1!=cast.StableRecoveryD4 || draw.NextState!=cast.RandomAfter || draw.WordsConsumed!=cast.WordsConsumed)
                        throw new ArgumentException("Invalid Stable recovery draw.");
                } else if(cast.WordsConsumed!=0)throw new ArgumentException("An automatic spell fabricated a cast draw.");
            }
            if(s.Receipts.Count(x=>CommandHistory.Read(x).Kind==CommandKind.CastKnownSpell)!=s.SpellCasts.Length)
                throw new ArgumentException("Casting receipts differ from settled casts.");
            if(s.BishopEntry==null&&(s.SpellCasts.Any(x=>x.ClassLevel>2||x.SpellId==BishopProfile.Dispel)
                ||s.SpellEffects.Any(x=>x.EndReason==SpellEffectEndReason.Dispelled)))throw new ArgumentException("Bishop casting requires its explicit profile.");
            foreach(var effect in s.SpellEffects) {
                var cast=s.SpellCasts.SingleOrDefault(x=>x.CommandId==effect.CastId);
                bool concentration=effect.SpellId=="sanctuary" || effect.SpellId=="detect-magic";
                if(cast==null || cast.EffectId!=effect.Id || cast.Revision!=effect.CastRevision || cast.SpellId!=effect.SpellId
                    || cast.ActorId!=effect.CasterId || cast.TargetId!=effect.TargetId || cast.At!=effect.StartedAt
                    || effect.RequiresConcentration!=concentration || effect.Present && effect.ExpiresAt<=s.RuleClock)
                    throw new ArgumentException("Unattributed or expired spell effect.");
                if(effect.SpellId=="arcane-ward") {
                    var epoch=WorldTiming.FindEpoch(s,cast.Turn.EpochId);
                    long next=checked(cast.Turn.LocalStart+epoch.Order.Count);
                    if(effect.ExpiryKind!=SpellExpiryKind.NextCasterStart || effect.ExpiryTurn.EpochId!=epoch.Id
                        || effect.ExpiryTurn.LocalStart!=next || !ValidTurn(s,effect.ExpiryTurn,effect.ExpiresAt,true)
                        || epoch.Start(next)!=effect.ExpiresAt)throw new ArgumentException("Ward expiry differs from its next caster Start.");
                } else if(effect.SpellId!="guidance" && !concentration || effect.ExpiryKind!=SpellExpiryKind.Absolute
                    || effect.ExpiresAt!=effect.StartedAt.AddSeconds(effect.SpellId=="detect-magic"?600:60))
                    throw new ArgumentException("Unsupported spell duration.");
                if(!effect.Present) {
                    bool consequence=effect.EndReason==SpellEffectEndReason.Incapacitated || effect.EndReason==SpellEffectEndReason.Dead;
                    bool actualCause=effect.EndCauseId==LifeEndingCause(effect.EndRevision,effect.CasterId)
                        ||s.Conditions.Any(x=>x.Target==effect.CasterId&&x.Operations.Any(o=>o.Id==effect.EndCauseId));
                    if(consequence&&actualCause) {
                        if(!s.Receipts.Any(x=>x.Revision==effect.EndRevision))throw new ArgumentException("Missing concentration-ending command.");
                    } else Receipt(s,effect.EndCauseId,effect.EndRevision);
                    if(effect.EndedAt>s.RuleClock || effect.EndReason==SpellEffectEndReason.Expired && effect.EndedAt!=effect.ExpiresAt)
                        throw new ArgumentException("Unqualified effect ending.");
                }
            }
            if(s.SpellEffects.Where(x=>x.Present && x.RequiresConcentration).GroupBy(x=>x.CasterId).Any(x=>x.Count()>1)
                || s.SpellEffects.Where(x=>x.Present).GroupBy(x=>x.SpellId+"|"+x.TargetId).Any(x=>x.Count()>1))
                throw new ArgumentException("Duplicate active concentration or same-name effect.");
            foreach(var activity in s.CastingActivities) {
                var command=Receipt(s,activity.CommandId,activity.Revision);
                var kind=activity.Kind==CastingActivityKind.Spell?CommandKind.CastKnownSpell
                    :activity.Kind==CastingActivityKind.MagicalClassAbility?(command.Kind==CommandKind.UseDivineInvocation&&s.BishopEntry!=null?CommandKind.UseDivineInvocation:CommandKind.UseHealingRite)
                    :activity.Kind==CastingActivityKind.DetectFocus?CommandKind.FocusDetectedAura:CommandKind.GroundCastingStrain;
                if(command.Kind!=kind || command.Actor!=activity.Turn.ActorId || activity.Turn.ActorId!=ClericRpProfile.Actor
                    || activity.At>s.RuleClock || !ValidTurn(s,activity.Turn,activity.At,true))throw new ArgumentException("Unattributed magical activity.");
            }
            foreach(var end in s.CastingTurnEnds) {
                Receipt(s,end.CauseId,end.Revision); var epoch=WorldTiming.FindEpoch(s,end.Turn.EpochId);
                var activities=s.CastingActivities.Where(x=>x.Turn.SameAs(end.Turn)).ToArray();
                if(epoch==null || !ValidTurn(s,end.Turn,epoch.Start(end.Turn.LocalStart),true)
                    || end.At!=epoch.Start(checked(end.Turn.LocalStart+1)) || end.At>s.RuleClock
                    || end.Proficiency!=2 || end.MagicalActivity!=activities.Any(x=>x.IsMagical)
                    || end.Grounding!=activities.Any(x=>x.Kind==CastingActivityKind.Grounding))throw new ArgumentException("Invalid settled regular End.");
            }
            ValidateStrain(s);
            foreach(var use in s.GuidanceUses) {
                var command=Receipt(s,use.CommandId,use.Revision); var effect=s.SpellEffects.SingleOrDefault(x=>x.Id==use.EffectId);
                var kind=use.CheckKind==GuidanceCheckKind.Hide?CommandKind.Hide:use.CheckKind==GuidanceCheckKind.Search?CommandKind.Search:CommandKind.StabilizeCompanion;
                var draw=DiceStream.Draw(use.RandomBefore,4);
                if(command.Kind!=kind || command.Actor!=use.ActorId || command.Guidance?.EffectId!=use.EffectId
                    || effect==null || effect.SpellId!="guidance" || effect.TargetId!=use.ActorId || effect.EndReason!=SpellEffectEndReason.GuidanceConsumed
                    || effect.EndCauseId!=use.CommandId || effect.EndRevision!=use.Revision || effect.EndedAt!=use.At
                    || draw.Value+1!=use.D4 || draw.NextState!=use.RandomAfter || draw.WordsConsumed!=use.WordsConsumed)
                    throw new ArgumentException("Invalid recipient-controlled Guidance consumption.");
                if(use.CheckKind==GuidanceCheckKind.MedicineStabilization) {
                    var check=s.CompanionStabilizations.SingleOrDefault(x=>x.CommandId==use.CommandId);
                    if(check==null || use.CheckId!=use.CommandId+".medicine" || check.Revision!=use.Revision
                        || check.ActorId!=use.ActorId || check.At!=use.At || check.RandomBefore!=use.RandomAfter)
                        throw new ArgumentException("Guidance lacks its actual subsequent Medicine check.");
                } else {
                    var check=s.ObservationActions.SingleOrDefault(x=>x.Id==use.CheckId);
                    if(check==null || check.ActorId!=use.ActorId || check.Revision!=use.Revision || check.At!=use.At
                        || check.Kind!=(use.CheckKind==GuidanceCheckKind.Hide?ObservationActionKind.Hide:ObservationActionKind.Search)
                        || check.WordsConsumed==0 || check.RandomBefore!=use.RandomAfter)
                        throw new ArgumentException("Guidance lacks its actual subsequent observation check.");
                }
            }
            if(s.GuidanceUses.GroupBy(x=>x.CheckId,StringComparer.Ordinal).Any(x=>x.Count()>1)
                || s.GuidanceUses.GroupBy(x=>x.EffectId,StringComparer.Ordinal).Any(x=>x.Count()>1))
                throw new ArgumentException("Guidance was consumed more than once.");
            foreach(var save in s.SpellSaves) {
                Receipt(s,save.CauseId,save.Revision); var effect=s.SpellEffects.SingleOrDefault(x=>x.Id==save.EffectId);
                if(effect==null || save.At<effect.StartedAt || save.At>=effect.ExpiresAt || save.At>s.RuleClock
                    || effect.EndedAt.HasValue && save.At>effect.EndedAt.Value
                    || save.Kind==SpellSaveKind.SanctuaryWisdom && (effect.SpellId!="sanctuary" || !ValidTurn(s,save.AttackerTurn,save.At,false))
                    || save.Kind==SpellSaveKind.ConcentrationConstitution && (!effect.RequiresConcentration || save.SubjectId!=effect.CasterId))
                    throw new ArgumentException("Unqualified spell save.");
                if(save.Kind==SpellSaveKind.SanctuaryWisdom) {
                    var cast=s.SpellCasts.Single(x=>x.CommandId==effect.CastId);
                    if(save.Dc!=cast.SpellDc || save.Success && !s.MeleeAttacks.Any(x=>x.Revision==save.Revision
                        &&x.AttackerId==save.SubjectId&&x.TargetId==effect.TargetId&&x.Attack.RandomBefore==save.RandomAfter)
                        || !save.Success && !s.SanctuaryAdmissions.Any(x=>x.SaveId==save.Id))
                        throw new ArgumentException("Sanctuary save differs from its generating DC or actual attack admission.");
                }
                var first=DiceStream.Draw(save.RandomBefore,20); var second=save.Second==0?first:DiceStream.Draw(first.NextState,20);
                long words=first.WordsConsumed+(save.Second==0?0:second.WordsConsumed);
                if(first.Value+1!=save.First || save.Second!=0 && second.Value+1!=save.Second || second.NextState!=save.RandomAfter || words!=save.WordsConsumed)
                    throw new ArgumentException("Spell save draw history differs.");
            }
            if(s.SpellSaves.Where(x=>x.Kind==SpellSaveKind.SanctuaryWisdom)
                .GroupBy(x=>x.EffectId+"|"+x.AttackerTurn.Binding).Any(x=>x.Count()>1))throw new ArgumentException("Repeated Sanctuary interval save.");
            foreach(var pending in s.SanctuaryAdmissions) {
                var source=Receipt(s,pending.SourceCommandId,pending.SourceRevision);
                var save=s.SpellSaves.SingleOrDefault(x=>x.Id==pending.SaveId);
                if(source.Fingerprint!=pending.SourceFingerprint || source.Actor!=pending.ActorId || save==null || save.Success
                    || save.Kind!=SpellSaveKind.SanctuaryWisdom || save.SubjectId!=pending.ActorId || save.Revision!=pending.SourceRevision
                    || !s.SpellEffects.Any(x=>x.Id==save.EffectId && x.TargetId==pending.OriginalTargetId))throw new ArgumentException("Invalid pending ward admission.");
                var expected=pending.Source==SanctuaryAttackSource.RegularMelee?CommandKind.AttackClub
                    :pending.Source==SanctuaryAttackSource.RegularUnarmed?CommandKind.AttackUnarmed
                    :pending.Source==SanctuaryAttackSource.RegularCreatureFeature?CommandKind.AttackCreatureFeature:CommandKind.RespondOpportunityAttack;
                if(pending.Source!=SanctuaryAttackSource.RegularMelee&&pending.Source!=SanctuaryAttackSource.RegularUnarmed
                    &&pending.Source!=SanctuaryAttackSource.RegularCreatureFeature&&pending.Source!=SanctuaryAttackSource.Opportunity
                    || source.Kind!=expected || source.Combat==null
                    ||(pending.Source==SanctuaryAttackSource.Opportunity
                        ? source.Kind!=CommandKind.RespondOpportunityAttack || source.Combat?.Choice!=true || source.Target!=pending.OpportunityId
                        : source.Target!=pending.OriginalTargetId))
                    throw new ArgumentException("Sanctuary continuation changed its original attack source.");
                if((pending.Source==SanctuaryAttackSource.RegularCreatureFeature||source.Combat.FeatureId!="")
                    &&(s.FerryWraith==null||source.Actor!=FerryWraithProfile.Actor||source.Combat.FeatureId!=FerryWraithProfile.Feature
                        ||source.Combat.WeaponId!=""))throw new ArgumentException("Sanctuary lost the owned creature attack payload.");
                if(s.MeleeAttacks.Any(x=>x.Revision==pending.SourceRevision))throw new ArgumentException("A failed ward gate also resolved an attack.");
                if(!pending.Pending) {
                    var response=Receipt(s,pending.ResolutionCauseId,pending.ResolvedRevision);
                    if(response.Kind!=CommandKind.RespondSanctuary || response.Actor!=pending.ActorId || response.Target!=pending.Id
                        || response.SanctuaryResponse==null || pending.Status==SanctuaryAdmissionStatus.Invalidated
                        || (pending.Status==SanctuaryAdmissionStatus.Retargeted)!=(response.SanctuaryResponse.Kind==SanctuaryResponseKind.Retarget)
                        || response.SanctuaryResponse.TargetId!=pending.ResolvedTargetId)
                        throw new ArgumentException("Unattributed Sanctuary response.");
                    if(pending.Status==SanctuaryAdmissionStatus.Retargeted && (pending.Source==SanctuaryAttackSource.Opportunity
                        || !s.MeleeAttacks.Any(x=>x.Revision==pending.ResolvedRevision&&x.AttackerId==pending.ActorId
                            &&x.TargetId==pending.ResolvedTargetId&&x.Attack.RandomBefore==save.RandomAfter
                            &&x.Instruction==source.Combat.Knockout&&x.PressInstruction==source.Combat.PressInstruction
                            &&x.WeaponId==(source.Combat.FeatureId!=""?source.Combat.FeatureId
                                :source.Kind==CommandKind.AttackUnarmed?CombatProfileIds.OrdinaryUnarmed:source.Combat.WeaponId))))
                        throw new ArgumentException("Sanctuary retarget did not settle the original attack entitlement.");
                } else if(s.RuleClock!=save.At || !s.Receipts.Any(x=>x.Revision==s.Revision&&x.Id==pending.SourceCommandId))
                    throw new ArgumentException("A voluntary command passed an unresolved Sanctuary admission.");
            }
            if(s.SanctuaryAdmissions.Count(x=>x.Pending)>1)throw new ArgumentException("Multiple unresolved ward choices.");
            foreach(var focus in s.DetectMagicFocuses) {
                var command=Receipt(s,focus.CommandId,focus.Revision);
                var detection=s.SpellEffects.SingleOrDefault(x=>x.Id==focus.DetectionEffectId);
                var observed=s.SpellEffects.SingleOrDefault(x=>x.Id==focus.ObservedEffectId);
                if(command.Kind!=CommandKind.FocusDetectedAura || command.Actor!=focus.ActorId || command.Target!=focus.ObservationId
                    || !ValidTurn(s,focus.Turn,focus.At,true) || detection==null || detection.SpellId!="detect-magic" || detection.CasterId!=focus.ActorId
                    || observed==null || !PresentAt(detection,focus.At,focus.Revision) || !PresentAt(observed,focus.At,focus.Revision)
                    || !focus.SchoolWithheld && focus.BroadSchool!=SpellSourceCatalog.Get(observed.SpellId).AccessFor("Cleric").School
                    || !s.CastingActivities.Any(x=>x.CommandId==focus.CommandId && x.Kind==CastingActivityKind.DetectFocus))
                    throw new ArgumentException("Unqualified paid aura focus.");
            }
            if(s.ConsumableContamination.Length!=1)throw new ArgumentException("Missing finite declared contamination.");
            var contamination=s.ConsumableContamination[0];
            if(contamination.Id!=ContaminationId || contamination.LotId!=ContaminatedWaterId || contamination.OriginId!=InitialPhysicalOrigin
                || contamination.OriginRevision!=0 || contamination.Kind!=ConsumableContaminationKind.OrdinaryPoison
                || !contamination.Present && !s.SpellCasts.Any(x=>x.CommandId==contamination.DestroyedByCastId && x.Revision==contamination.DestroyedRevision
                    && x.SpellId=="purify-food-and-drink" && x.TargetId==contamination.LotId))throw new ArgumentException("Unqualified contamination origin or destruction.");
        }

        private static bool PresentAt(SpellEffectRecord effect,RuleTime at,long revision)=>effect.StartedAt<=at && effect.ExpiresAt>at
            && effect.CastRevision<revision && (effect.EndRevision==0 || effect.EndRevision>revision);
        private static void ValidateStrain(Snapshot s)
        {
            var current=new CastingStrainRecord(ClericRpProfile.Actor);
            var events=s.SpellCasts.Select(x=>(at:x.At,revision:x.Revision,cast:x,end:(CastingTurnEndRecord)null,rest:(ClericLongRestSettlementRecord)null,vent:(DivineInvocationRecord)null))
                .Concat(s.CastingTurnEnds.Select(x=>(at:x.At,revision:x.Revision,cast:(SpellCastRecord)null,end:x,rest:(ClericLongRestSettlementRecord)null,vent:(DivineInvocationRecord)null)))
                .Concat(s.ClericLongRestSettlements.Select(x=>(at:x.At,revision:x.Revision,cast:(SpellCastRecord)null,end:(CastingTurnEndRecord)null,rest:x,vent:(DivineInvocationRecord)null)))
                .Concat(BishopProfile.Invocations(s).Select(x=>(at:x.At,revision:x.Revision,cast:(SpellCastRecord)null,end:(CastingTurnEndRecord)null,rest:(ClericLongRestSettlementRecord)null,vent:x)))
                .OrderBy(x=>x.at).ThenBy(x=>x.revision).ThenBy(x=>x.rest==null?0:1).ToArray();
            foreach(var e in events) {
                if(e.cast!=null) {
                    var cast=e.cast;
                    if(cast.DissonanceBefore!=current.Dissonance || cast.Rank>0 && current.RankedBlocked(cast.Proficiency,cast.CastingModifier)
                        || cast.Surcharge!=(cast.Rank==0?0:current.RankedSurcharge(cast.Proficiency,cast.CastingModifier)))
                        throw new ArgumentException("Invalid historical spell strain cost.");
                    current=current.BeginAdmittedCast(cast.SpellId,cast.Rank,cast.Revision,s.BishopEntry!=null);
                    if(current.Dissonance!=cast.DissonanceAfter || current.Refrain!=cast.AppliedRefrain)throw new ArgumentException("Invalid Refrain history.");
                } else if(e.vent!=null) {
                    if(e.vent.DissonanceBefore!=current.Dissonance)throw new ArgumentException("Invalid pre-Invocation Dissonance.");
                    current=current.ReduceAtSettledEnd(1);
                    if(e.vent.DissonanceAfter!=current.Dissonance)throw new ArgumentException("Invalid protected Conviction vent.");
                } else if(e.rest!=null) {
                    var rest=e.rest;
                    if(rest.DissonanceBefore!=current.Dissonance || rest.LastSpellId!=current.LastSpellId
                        || rest.Refrain!=current.Refrain || rest.LastCastRevision!=current.LastCastRevision)
                        throw new ArgumentException("Invalid pre-rest casting history.");
                    current=new CastingStrainRecord(current.ActorId,rest.Benefit==ClericLongRestBenefit.Eligible?0:current.Dissonance,
                        current.LastSpellId,current.Refrain,current.LastCastRevision);
                    if(rest.DissonanceAfter!=current.Dissonance)throw new ArgumentException("Invalid rest Dissonance settlement.");
                } else {
                    if(e.end.Before!=current.Dissonance)throw new ArgumentException("Invalid Dissonance before End.");
                    current=current.ReduceAtSettledEnd(e.end.MagicalActivity?0:e.end.Grounding?e.end.Proficiency:1);
                    if(e.end.After!=current.Dissonance)throw new ArgumentException("Invalid Dissonance after End.");
                }
            }
            var actual=s.CastingStrain[0];
            if(actual.Dissonance!=current.Dissonance || actual.LastSpellId!=current.LastSpellId || actual.Refrain!=current.Refrain
                || actual.LastCastRevision!=current.LastCastRevision)throw new ArgumentException("Casting cadence does not reconcile.");
        }
        internal static bool ValidTurn(Snapshot s,SpellTurnIdentity turn,RuleTime at,bool ownAction)
        {
            if(turn==null)return false;
            var epoch=WorldTiming.FindEpoch(s,turn.EpochId); var admission=s.Reinforcement?.Admission;
            if(epoch==null || !PostRecoveryProfile.IsEpoch(s,epoch.Id) && epoch.Id!=admission?.Phase.Epoch.Id
                || !epoch.Order.Contains(turn.ActorId) || at<epoch.Origin)return false;
            long local=epoch.LatestStart(turn.ActorId,epoch.SlotAt(at));
            if(turn.IsCarried && PostRecoveryProfile.IsEpoch(s,epoch.Id)) {
                var entry=s.PostRecoveryEncounter;
                return !ownAction && local<0 && turn.CarriedAdmissionRevision==entry.Entered.Revision
                    && turn.GlobalStart==entry.Admission.CarriedInterval(turn.ActorId).LastStart;
            }
            if(turn.IsCarried) {
                var entered=s.Reinforcement.Events.SingleOrDefault(x=>x.Kind==ReinforcementEventKind.Admitted);
                return !ownAction && local<0 && entered!=null && turn.CarriedAdmissionRevision==entered.Revision
                    && turn.GlobalStart==admission.Carried.Single(x=>x.Interval.ActorId==turn.ActorId).Interval.LastStart;
            }
            return turn.LocalStart==local && turn.GlobalStart==WorldTiming.TurnOrdinal(s,epoch.Id,local)
                && (!ownAction || epoch.SlotAt(at)==local);
        }
        private static void ValidateCompanionClubPickup(Snapshot s)
        {
            var club=s.Clubs.SingleOrDefault(x=>x.Id==CompanionClubId);
            var pickups=s.PortableHandling.Where(x=>x.ItemId==CompanionClubId).ToArray();
            if(club==null||club.ProfileId!=CompanionClubProfileId||club.OwnerId!=ClericRpProfile.Actor
                ||club.CustodianId!=ClericRpProfile.Actor||club.HeldBy!=""&&club.HeldBy!=ClericRpProfile.Actor
                ||s.PortableEquipment.Any(x=>x.Id==CompanionClubId)
                ||pickups.Length==0&&(club.HeldBy!=""||club.CellX!=3||club.CellY!=3))
                throw new ArgumentException("Invalid casting Club physical authority.");
            foreach(var pickup in pickups) {
                var receipt=s.Receipts.SingleOrDefault(x=>x.Revision==pickup.Revision);
                if(receipt==null)throw new ArgumentException("Missing casting Club pickup command.");
                var command=CommandHistory.Read(receipt);
                if(command.Kind!=CommandKind.HandlePortableEquipment||command.Actor!=pickup.ActorId||command.Target!=club.Id
                    ||command.Inventory==null||command.Inventory.Amount!=new RuleQuantity(1)
                    ||command.Inventory.Handling!=HandlingKind.Pickup||command.Inventory.Destination!=""
                    ||command.Combat!=null||command.X!=0||command.Y!=0)
                    throw new ArgumentException("Casting Club pickup command differs from handling.");
            }
            if(s.Receipts.Count(x=>{var c=CommandHistory.Read(x);return c.Kind==CommandKind.HandlePortableEquipment&&c.Target==club.Id;})!=pickups.Length)
                throw new ArgumentException("Casting Club pickup receipts differ from handling.");
        }
        private static Command Receipt(Snapshot s,string id,long revision)
        {
            var receipt=s.Receipts.SingleOrDefault(x=>x.Id==id && x.Revision==revision);
            if(receipt==null || revision>s.Revision)throw new ArgumentException("Missing casting history receipt.");
            return CommandHistory.Read(receipt);
        }
        private static void Rows<T>(T[] rows,int maximum,bool selected) where T:class
        {if(rows==null || rows.Length>maximum || rows.Any(x=>x==null) || !selected && rows.Length!=0)throw new ArgumentException("Invalid casting history capacity or envelope.");}
        private static void Unique(System.Collections.Generic.IEnumerable<string> ids)
        {var rows=ids.ToArray();if(rows.Distinct(StringComparer.Ordinal).Count()!=rows.Length)throw new ArgumentException("Duplicate casting history identity.");}
        private static void Ordered(System.Collections.Generic.IEnumerable<long> revisions)
        {if(!revisions.SequenceEqual(revisions.OrderBy(x=>x)))throw new ArgumentException("Unordered casting history.");}
    }
}
