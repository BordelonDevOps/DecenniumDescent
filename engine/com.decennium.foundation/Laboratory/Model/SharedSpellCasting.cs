#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedClericCasting;
        internal TestOnlySharedWorldPolicy EnableConnectedClericCasting(ClericInitialSelection initial,
            ClericRepertoireSelection repertoire,ClericMilestoneDeclaration declaration)
        {
            EnableConnectedClericSettlement(initial,repertoire,declaration);
            connectedClericCasting=true;
            ContentFingerprint=SpellCastingProfile.FingerprintPrefix+RetreatHash(string.Join("|",ContentFingerprint,
                SpellCastingProfile.ApprovalResponse,SpellSourceCatalog.SourceRevision,
                string.Join("|",SpellSourceCatalog.Definitions.Select(x=>x.Id+":"+x.ProcedureSha256)),
                SpellCastingProfile.FocusEquipmentSourceSha256,SpellCastingProfile.InitialPhysicalOrigin,
                SpellCastingProfile.FocusId,SpellCastingProfile.FocusProfileId,"worn|1lb|no-purchase|no-packed-volume",
                SpellCastingProfile.ClubPickupApproval,SpellCastingProfile.CompanionClubId,SpellCastingProfile.CompanionClubProfileId,
                SpellCastingProfile.ClubSourceId,SpellCastingProfile.ClubRulebookSha256,"source-line6766|2lb|derived-load|owned-ground3,3|paid1sec-held|no-storage",
                SpellCastingProfile.ContaminatedWaterId,SpellCastingProfile.ContaminationId,
                "TEST_ONLY.plot-flask|1pint|ordinary-poison|no-new-acquisition|no-unclean-propagation",
                "actual-reinforced-calendar|shared-rp-clock-rng|six-source-procedures|approval-amendments-v1"));
            return this;
        }
        private void InitializeClericCasting(Snapshot s)
        {
            if(!connectedClericCasting)return;
            const string actor=ClericRpProfile.Actor;
            s.ConnectedClericCasting=true;
            s.CastingStrain=new[]{new CastingStrainRecord(actor)};
            s.PortableEquipment=s.PortableEquipment.Append(new PortableEquipmentRecord(SpellCastingProfile.FocusId,
                SpellCastingProfile.FocusProfileId,actor,actor,"",PortablePlacement.Worn,PortableLinkKind.None,"",
                PortableMassBasis.Fixed,new RuleQuantity(1),new RuleQuantity(1),wearable:true)).ToArray();
            s.Work=new WorkLedger(s.Work.Lots.Append(new ResourceLot(SpellCastingProfile.ContaminatedWaterId,
                TestOnlyInventoryPolicy.WaterUnit,1,TestOnlyFillingPolicy.FlaskId,actor)),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Append(new InventoryLotRecord(SpellCastingProfile.ContaminatedWaterId,"",actor,
                new RuleQuantity(1),default,NutritionKind.WaterPints,null,InventoryAccess.Ground)).ToArray();
            s.VesselContents=s.VesselContents.Append(new VesselContentRecord(SpellCastingProfile.ContaminatedWaterId,TestOnlyFillingPolicy.FlaskId)).ToArray();
            s.ConsumableContamination=new[]{new ConsumableContaminationRecord(SpellCastingProfile.ContaminationId,
                SpellCastingProfile.ContaminatedWaterId,SpellCastingProfile.InitialPhysicalOrigin,0,ConsumableContaminationKind.OrdinaryPoison)};
        }
        internal static void DropCastingFocus(Snapshot s,ActorState actor)
        {
            if(!s.ConnectedClericCasting)return;
            s.PortableEquipment=s.PortableEquipment.Select(x=>SpellCastingProfile.IsFocus(s,x)
                && x.CustodianId==actor.Id && x.HeldHands==1
                ?x.With(placement:PortablePlacement.Ground,groundX:actor.X,groundY:actor.Y,heldHands:0):x).ToArray();
        }

        private static SpellTurnIdentity CurrentCastingTurn(Snapshot s,string actor)
        {
            var epoch=WorldTiming.ForActor(s,actor); var admission=s.Reinforcement?.Admission;
            if(PostRecoveryProfile.IsEpoch(s,epoch?.Id)) {
                long current=epoch.LatestStart(actor,epoch.ProcessedSlot);
                var recoveryEntry=s.PostRecoveryEncounter;
                return current>=0 ? new SpellTurnIdentity(actor,epoch.Id,current,checked((int)current))
                    :new SpellTurnIdentity(actor,epoch.Id,-1,recoveryEntry.Admission.CarriedInterval(actor).LastStart,recoveryEntry.Entered.Revision);
            }
            if(epoch==null || epoch.Id!=admission?.Phase.Epoch.Id)return null;
            long local=epoch.LatestStart(actor,epoch.ProcessedSlot);
            if(local>=0)return new SpellTurnIdentity(actor,epoch.Id,local,admission.Phase.GlobalTurn(local));
            var entry=s.Reinforcement.Events.Single(x=>x.Kind==ReinforcementEventKind.Admitted);
            return new SpellTurnIdentity(actor,epoch.Id,-1,admission.Carried.Single(x=>x.Interval.ActorId==actor).Interval.LastStart,entry.Revision);
        }

        private string CastingActionFailure(Snapshot s,Command c)
        {
            if(!s.ConnectedClericCasting || c.Actor!=ClericRpProfile.Actor)return "OrdinarySpellcastingUnsupported";
            var epoch=WorldTiming.ForActor(s,c.Actor); var phase=s.Reinforcement?.Admission?.Phase;
            bool recovery=PostRecoveryProfile.IsEpoch(s,epoch?.Id);
            if(epoch==null || !recovery && epoch.Id!=phase?.Epoch.Id)return "SpellcastingCalendarUnsupported";
            string encounter=recovery?PostRecoveryEncounterDefinition.Encounter:s.Reinforcement.Definition.EncounterId;
            if(s.InventoryCombat ? s.Encounter?.Id!=encounter
                :s.Encounter!=null || !s.ClosedEncounters.Any(x=>x.Encounter.Id==encounter))
                return "SpellcastingContextUnsupported";
            long local=epoch.SlotAt(s.RuleClock);
            if(local!=epoch.ProcessedSlot || epoch.LatestStart(c.Actor,local)!=local
                || Interval(s,c.Actor).LastStart!=WorldTiming.TurnOrdinal(s,epoch.Id,local)
                || s.InventoryCombat && (s.Encounter.CurrentActor!=c.Actor || s.InventoryTurnActor!=c.Actor))return "WrongRegularTurn";
            if(PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s) || s.ManufacturingAdvance!=null)
                return "TacticalChoicePending";
            if(TestOnlyClubAttackPolicy.HasUnprocessedConditionDeadline(s)
                || s.FrightenedTimings.Any(x=>x.RepeatAt.Time<=s.RuleClock && !s.FrightenedSaves.Any(y=>y.Repeat&&y.ApplicationId==x.ApplicationId)
                    && !ClericSettlementProfile.CuredBeforeRepeat(s,x)))return "ConditionBoundaryPending";
            if(Interval(s,c.Actor).ActionSpent)return "ActionAlreadySpent";
            if(!CapableWorker(s,c.Actor) || !Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(OrdinaryInventory.Busy(s,c.Actor) || CharacterAdvancementRules.Busy(s,c.Actor)
                || s.WorldTraversals.Any(x=>x.ActorId==c.Actor))return "SpellcastingRequiresStationaryAccess";
            if(s.InventoryCombat && !TestOnlyClubAttackPolicy.HasStance(s))return "StanceRequired";
            return s.CastingActivities.Length>=SpellCastingProfile.MaxActivities?"CastingHistoryFull":null;
        }

        private static bool UsesSpellFocus(string spell)=>spell!="guidance" && spell!="spare-the-dying";
        private static bool ConcentratingSpell(string spell)=>spell=="sanctuary" || spell=="detect-magic";
        private static bool PersistentSpell(string spell)=>spell=="arcane-ward" || spell=="guidance" || ConcentratingSpell(spell);

        private string AssessSpellCast(Snapshot s,Command c)
        {
            string shape=SpellCastingProfile.PayloadFailure(s,c); if(shape!=null)return shape;
            if(c.Kind!=CommandKind.CastKnownSpell || c.SpellCast==null)return "SpellCastSelectionRequired";
            string action=CastingActionFailure(s,c); if(action!=null)return action;
            string spell=c.SpellCast.SpellId;
            var character=s.Characters.Single(x=>x.ActorId==c.Actor); int level=character.Levels.Count(x=>x.ClassName=="Cleric");
            string access=ClericRepertoireProfile.AssessChoice(spell,level); if(access!=null)return access;
            var known=s.KnownSpells.SingleOrDefault(x=>x.ActorId==c.Actor && x.SpellId==spell && x.ClassName=="Cleric");
            if(known==null || known.AcquiredRevision>s.Revision || !known.MatchesSource())return "SpellNotKnown";
            // Every admitted spell has V. Use the shared active condition projection;
            // hearing loss is separate from the inability to provide a verbal component.
            if(View(s,c.Actor).BlocksAudibleFeatures)return "SpellVerbalComponentUnavailable";
            bool needsFocus=UsesSpellFocus(spell);
            var focus=s.PortableEquipment.SingleOrDefault(x=>x.Id==c.SpellCast.FocusItemId);
            bool held=focus?.HeldHands==1 && focus.CustodianId==c.Actor && focus.Placement==PortablePlacement.Carried;
            if(needsFocus) {
                if(!SpellCastingProfile.IsFocus(s,focus) || focus.CustodianId!=c.Actor || focus.ParentId!=""
                    || focus.Placement!=PortablePlacement.Worn && !held)return "SpellFocusUnavailable";
            } else if(c.SpellCast.FocusItemId!="")return "UnexpectedSpellFocusSelection";
            if(AvailableHands(s,c.Actor)<1 && !(needsFocus&&held))return "SpellSomaticHandUnavailable";
            var stance=TestOnlyClubAttackPolicy.ActiveStance(s,c.Actor);
            if(c.SpellCast.ElectFocusedDc && (spell!="sanctuary" || stance?.Kind!=CombatStance.Focused
                || s.SpellCasts.Any(x=>x.FocusedDcElected&&x.StanceRevision==stance.Revision)))return "FocusedSpellBenefitUnavailable";
            bool willing=spell=="arcane-ward" || spell=="guidance" || spell=="sanctuary";
            if(c.SpellCast.WillingTarget!=willing)return "SpellWillingTargetSelectionRequired";
            if(spell=="purify-food-and-drink") {
                string batch=PurifyBatchFailure(s,c); if(batch!=null)return batch;
            } else {
                var target=s.Actors.SingleOrDefault(x=>x.Id==c.Target);
                if(target==null || willing && c.Target!=TestOnlyPolicy.ActorId && c.Target!=ClericRpProfile.Actor
                    || spell=="detect-magic" && c.Target!=c.Actor)return "SpellTargetUnavailable";
                if(s.WorldTraversals.Any(x=>x.ActorId==c.Target))return "SpellTargetTraversalUnsupported";
                var actor=s.Actors.Single(x=>x.Id==c.Actor); var life=s.Lives.Single(x=>x.ActorId==c.Target);
                if(life.Dead || PlanarCombatGeometry.DistanceFeet(new CombatCell(actor.X,actor.Y),new CombatCell(target.X,target.Y))>30
                    || !ObservationGeometry.LineOfEffectClear(s,c.Actor,c.Target))return "SpellTargetUnavailable";
                if(c.Target!=c.Actor && !ObservationRules.CanSee(s,c.Actor,c.Target)
                    || spell=="arcane-ward" && View(s,c.Actor).Has(ConditionKind.Blinded))return "SpellTargetNotPerceived";
                if(spell=="spare-the-dying" && (life.Hp!=0 || life.Stable))return "StabilizationTargetNotDying";
            }
            var facts=CharacterRuleFacts.ForActor(s,c.Actor); var strain=s.CastingStrain.Single(x=>x.ActorId==c.Actor);
            var source=SpellSourceCatalog.Get(spell).AccessFor("Cleric"); int modifier=facts.AbilityModifier(CharacterAbility.Wisdom);
            if(source.Rank>0 && strain.RankedBlocked(facts.ProficiencyBonus,modifier))return "RankedCastingBlockedByDissonance";
            int surcharge=source.Rank==0?0:strain.RankedSurcharge(facts.ProficiencyBonus,modifier);
            var pool=s.ResonancePools.SingleOrDefault(x=>x.ActorId==c.Actor);
            if(pool==null || pool.Maximum!=DeriveResonanceMaximum(character))return "ResonancePoolUnavailable";
            if(pool.Current<source.BaseRpCost+surcharge)return "InsufficientResonance";
            if(s.SpellCasts.Length>=SpellCastingProfile.MaxCasts || PersistentSpell(spell)&&s.SpellEffects.Length>=SpellCastingProfile.MaxEffects
                || s.CastingTurnEnds.Length>=SpellCastingProfile.MaxTurnEnds || strain.Dissonance>int.MaxValue-4
                || !Validation.ValidId(c.Id+".effect"))return "CastingHistoryFull";
            return null;
        }

        private static string PurifyBatchFailure(Snapshot s,Command c)
        {
            var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==c.Target); var meta=s.InventoryLots.SingleOrDefault(x=>x.LotId==c.Target);
            if(lot==null || meta==null || lot.Amount==default || (meta.Nutrition==NutritionKind.WaterPints
                ?lot.UnitId!=TestOnlyInventoryPolicy.WaterUnit || lot.Amount>new RuleQuantity(8)
                :meta.Nutrition!=NutritionKind.FoodPounds || lot.Amount>new RuleQuantity(5)))return "PurifyBatchUnsupported";
            if(s.Work.AvailableAmount(lot.Id)!=lot.Amount || s.WaterFills.Any(x=>x.Pending&&(x.SourceLotId==lot.Id||x.DestinationId==lot.LocationId)))
                return "PurifyBatchBusy";
            string location=lot.LocationId; var vessel=s.Vessels.SingleOrDefault(x=>x.Id==location);
            if(vessel!=null && s.VesselContents.Any(x=>x.VesselId==vessel.Id&&x.LotId!=lot.Id
                &&s.Work.Lots.Single(l=>l.Id==x.LotId).Amount!=default))return "PurifyBatchNotSeparated";
            // Target the whole physical vessel for drink, or the actual food item. Handling
            // reach/ownership is not a spell-range rule; closed enclosing containers still
            // block access to that target. Follow its real placement instead of stale lot labels.
            var physical=s.PortableEquipment.SingleOrDefault(x=>vessel!=null
                ?x.LinkKind==PortableLinkKind.WaterVessel&&x.LinkedId==vessel.Id
                :x.LinkKind==PortableLinkKind.InventoryLot&&x.LinkedId==lot.Id);
            while(physical!=null&&physical.ParentId!="") {
                var parent=s.PortableEquipment.Single(x=>x.Id==physical.ParentId);
                if(physical.Placement==PortablePlacement.Contained&&!parent.Open)return "PurifyBatchEnclosed";
                physical=parent;
            }
            if(vessel!=null)location=vessel.LocationId;
            if(physical!=null&&physical.Placement!=PortablePlacement.Ground)location=physical.CustodianId;
            var body=s.Actors.SingleOrDefault(x=>x.Id==location); int x,y;
            if(physical?.Placement==PortablePlacement.Ground){x=physical.GroundX;y=physical.GroundY;}
            else if(body!=null) {x=body.X;y=body.Y;if(s.WorldTraversals.Any(t=>t.ActorId==body.Id))return "SpellTargetTraversalUnsupported";}
            else if(location==TestOnlyCropPolicy.PlotId){x=3;y=3;}
            else return "PurifyBatchLocationUnsupported";
            var actor=s.Actors.Single(a=>a.Id==c.Actor);
            if(PlanarCombatGeometry.DistanceFeet(new CombatCell(actor.X,actor.Y),new CombatCell(x,y))>30
                || !ObservationGeometry.LineOfEffectClearToCell(s,c.Actor,x,y))return "SpellTargetUnavailable";
            if(View(s,c.Actor).Has(ConditionKind.Blinded) || !ObservationGeometry.GeometricSight(s,c.Actor,ObservationGeometry.Position(s,c.Actor),
                new ObservationPoint(new RuleQuantity(x),new RuleQuantity(y))))return "SpellTargetNotPerceived";
            return null;
        }

        private static void RecordCastingActivity(Snapshot s,Command c,CastingActivityKind kind)
        {
            if(!s.ConnectedClericCasting)return;
            s.CastingActivities=s.CastingActivities.Append(new CastingActivityRecord(c.Id,s.Revision+1,
                CurrentCastingTurn(s,c.Actor),s.RuleClock,kind)).ToArray();
        }
        private static void EndSpellEffect(Snapshot s,SpellEffectRecord effect,string cause,long revision,RuleTime at,SpellEffectEndReason reason)
        {
            if(!effect.Present)return;
            s.SpellEffects=s.SpellEffects.Select(x=>x.Id==effect.Id?x.End(cause,revision,at,reason):x).ToArray();
        }

        private string ResolveSpellCast(Snapshot s,Command c)
        {
            string failure=AssessSpellCast(s,c); if(failure!=null)return failure;
            string spell=c.SpellCast.SpellId; long revision=s.Revision+1; var turn=CurrentCastingTurn(s,c.Actor);
            var source=SpellSourceCatalog.Get(spell).AccessFor("Cleric"); var facts=CharacterRuleFacts.ForActor(s,c.Actor);
            var prior=s.CastingStrain.Single(x=>x.ActorId==c.Actor); var next=prior.BeginAdmittedCast(spell,source.Rank,revision);
            int modifier=facts.AbilityModifier(CharacterAbility.Wisdom),pb=facts.ProficiencyBonus;
            int surcharge=source.Rank==0?0:prior.RankedSurcharge(pb,modifier); var pool=s.ResonancePools.Single(x=>x.ActorId==c.Actor);
            var focus=s.PortableEquipment.SingleOrDefault(x=>x.Id==c.SpellCast.FocusItemId); var stance=TestOnlyClubAttackPolicy.ActiveStance(s,c.Actor);
            int hands=AvailableHands(s,c.Actor); uint random=s.RandomState; long words=0; int stableD4=0;
            SetInterval(s,Interval(s,c.Actor).PayAction());
            s.ResonancePools=s.ResonancePools.Select(x=>x.ActorId==c.Actor && source.BaseRpCost+surcharge>0?x.Pay(source.BaseRpCost+surcharge):x).ToArray();
            s.CastingStrain=s.CastingStrain.Select(x=>x.ActorId==c.Actor?next:x).ToArray();
            RecordCastingActivity(s,c,CastingActivityKind.Spell);
            if(ConcentratingSpell(spell))foreach(var old in s.SpellEffects.Where(x=>x.Present&&x.CasterId==c.Actor&&x.RequiresConcentration).ToArray())
                EndSpellEffect(s,old,c.Id,revision,s.RuleClock,SpellEffectEndReason.Replaced);
            string effectId=PersistentSpell(spell)?c.Id+".effect":"";
            if(PersistentSpell(spell)) {
                bool ward=spell=="arcane-ward"; var epoch=WorldTiming.ForActor(s,c.Actor); long local=turn.LocalStart+epoch.Order.Count;
                var expiry=ward?epoch.Start(local):s.RuleClock.AddSeconds(spell=="detect-magic"?600:60);
                var expiryTurn=ward?new SpellTurnIdentity(c.Actor,epoch.Id,local,WorldTiming.TurnOrdinal(s,epoch.Id,local)):null;
                var effect=new SpellEffectRecord(effectId,c.Id,revision,spell,c.Actor,c.Target,s.RuleClock,expiry,
                    ward?SpellExpiryKind.NextCasterStart:SpellExpiryKind.Absolute,expiryTurn,ConcentratingSpell(spell));
                foreach(var old in s.SpellEffects.Where(x=>x.Present&&x.SpellId==spell&&x.TargetId==c.Target).ToArray()) {
                    if(old.ExpiresAt>expiry)effect=effect.End(c.Id,revision,s.RuleClock,SpellEffectEndReason.Replaced);
                    else EndSpellEffect(s,old,c.Id,revision,s.RuleClock,SpellEffectEndReason.Replaced);
                }
                s.SpellEffects=s.SpellEffects.Append(effect).ToArray();
            } else if(spell=="spare-the-dying") {
                var before=s.Lives.Single(x=>x.ActorId==c.Target); var draw=DiceStream.Draw(s.RandomState,4);
                stableD4=draw.Value+1; words=draw.WordsConsumed; s.RandomState=draw.NextState;
                TestOnlyClubAttackPolicy.ApplyLife(s,before,PlaytestLife.StabilizeAt(ActorLifeRules.ReadForResolution(s,before),stableD4,s.RuleClock));
                ReconcileDyingCadences(s);
            } else if(spell=="purify-food-and-drink") {
                s.ConsumableContamination=s.ConsumableContamination.Select(x=>x.LotId==c.Target&&x.Present&&x.Purifiable?x.Destroy(c.Id,revision):x).ToArray();
            }
            s.SpellCasts=s.SpellCasts.Append(new SpellCastRecord(c.Id,revision,c.Actor,c.Target,spell,
                s.KnownSpells.Single(x=>x.ActorId==c.Actor&&x.SpellId==spell).AcquiredRevision,
                s.Characters.Single(x=>x.ActorId==c.Actor).Levels.Count(x=>x.ClassName=="Cleric"),source.Rank,pb,modifier,
                8+pb+modifier+(c.SpellCast.ElectFocusedDc?1:0),stance?.Revision??0,c.SpellCast.ElectFocusedDc,c.SpellCast.FocusItemId,
                focus?.HeldHands==1,hands,c.SpellCast.WillingTarget,turn,s.RuleClock,pool.Current,source.BaseRpCost,surcharge,
                pool.Current-source.BaseRpCost-surcharge,prior.Dissonance,next.Dissonance,next.Refrain,effectId,stableD4,random,s.RandomState,words)).ToArray();
            return null;
        }

        private CommandQueryResult QuerySpellCast(Snapshot s,Command c)
        {
            string failure=AssessSpellCast(s,c); if(failure!=null)return new CommandQueryResult(true,false,failure,s.Revision);
            var source=SpellSourceCatalog.Get(c.SpellCast.SpellId).AccessFor("Cleric"); var facts=CharacterRuleFacts.ForActor(s,c.Actor);
            int surcharge=source.Rank==0?0:s.CastingStrain.Single(x=>x.ActorId==c.Actor).RankedSurcharge(facts.ProficiencyBonus,facts.AbilityModifier(CharacterAbility.Wisdom));
            int rp=source.BaseRpCost+surcharge;
            var costs=rp==0?new[]{new CommandCost("action","",1)}:new[]{new CommandCost("action","",1),new CommandCost("rp",c.Actor,rp)};
            return new CommandQueryResult(true,true,"Available",s.Revision,costs);
        }

        private IEnumerable<Command> DiscoverCastingCommands(Snapshot s,Authority authority,string actor)
        {
            if(!s.ConnectedClericCasting||!authority.Controls(actor))yield break;
            int index=0;string Id()=>"option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".casting."+(++index).ToString(CultureInfo.InvariantCulture);
            var pending=PendingSanctuary(s);
            if(pending!=null) {
                if(pending.ActorId!=actor)yield break;
                yield return new Command(Id(),actor,s.Revision,CommandKind.RespondSanctuary,pending.Id,
                    sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Forgo));
                if(pending.Source==SanctuaryAttackSource.RegularMelee||pending.Source==SanctuaryAttackSource.RegularUnarmed)
                    foreach(string target in s.Encounter.Order.Where(x=>x!=actor&&x!=pending.OriginalTargetId&&ObservationRules.CanSee(s,actor,x)))
                        yield return new Command(Id(),actor,s.Revision,CommandKind.RespondSanctuary,pending.Id,
                            sanctuaryResponse:new SanctuaryResponseRequest(SanctuaryResponseKind.Retarget,target));
                yield break;
            }
            if(actor==ClericRpProfile.Actor) {
                foreach(var known in s.KnownSpells.Where(x=>x.ActorId==actor).OrderBy(x=>x.SpellId,StringComparer.Ordinal)) {
                    string spell=known.SpellId;bool willing=spell=="arcane-ward"||spell=="guidance"||spell=="sanctuary";
                    IEnumerable<string> targets=spell=="detect-magic"?new[]{actor}:spell=="purify-food-and-drink"
                        ?s.InventoryLots.Where(x=>authority.MayUseInventory(x.OwnerId)&&(x.Nutrition==NutritionKind.WaterPints||x.Nutrition==NutritionKind.FoodPounds)).Select(x=>x.LotId)
                        :s.Actors.Where(x=>(x.Id==actor||ObservationRules.CanSee(s,actor,x.Id))
                            &&(!willing||authority.Controls(x.Id)&&(x.Id==TestOnlyPolicy.ActorId||x.Id==ClericRpProfile.Actor))).Select(x=>x.Id);
                    foreach(string target in targets) {
                        yield return new Command(Id(),actor,s.Revision,CommandKind.CastKnownSpell,target,
                            spellCast:new SpellCastRequest(spell,UsesSpellFocus(spell)?SpellCastingProfile.FocusId:"",willing));
                        if(spell=="sanctuary"&&TestOnlyClubAttackPolicy.ActiveStance(s,actor)?.Kind==CombatStance.Focused)
                            yield return new Command(Id(),actor,s.Revision,CommandKind.CastKnownSpell,target,
                                spellCast:new SpellCastRequest(spell,SpellCastingProfile.FocusId,true,true));
                    }
                }
                yield return new Command(Id(),actor,s.Revision,CommandKind.GroundCastingStrain);
                foreach(var concentration in s.SpellEffects.Where(x=>x.Present&&x.RequiresConcentration&&x.CasterId==actor))
                    yield return new Command(Id(),actor,s.Revision,CommandKind.EndSpellConcentration,concentration.Id);
                foreach(var aura in ObserveCasting(s,actor).Auras)
                    yield return new Command(Id(),actor,s.Revision,CommandKind.FocusDetectedAura,aura.ObservationId);
            }
            if(!s.InventoryCombat||s.Encounter?.CurrentActor!=actor)yield break;
            var benefits=s.SpellEffects.Where(x=>x.Present&&x.SpellId=="guidance"&&x.TargetId==actor&&x.ExpiresAt>s.RuleClock).ToArray();
            yield return new Command(Id(),actor,s.Revision,CommandKind.Hide,s.Encounter.CurrentTurnId);
            if(actor==ConnectedExpeditionSession.Hero)
                yield return new Command(Id(),actor,s.Revision,CommandKind.StabilizeCompanion,ClericRpProfile.Actor);
            foreach(var benefit in benefits) {
                var choice=new GuidanceChoice(benefit.Id);
                yield return new Command(Id(),actor,s.Revision,CommandKind.Hide,s.Encounter.CurrentTurnId,guidance:choice);
                foreach(var search in DiscoverObservationSearchCommands(s,actor))
                    yield return new Command(Id(),actor,s.Revision,CommandKind.Search,search.Target,search.X,search.Y,guidance:choice);
                if(actor==ConnectedExpeditionSession.Hero)
                    yield return new Command(Id(),actor,s.Revision,CommandKind.StabilizeCompanion,ClericRpProfile.Actor,guidance:choice);
            }
        }

        private static string AuraObservationId(Snapshot s,string actor,SpellEffectRecord detection,SpellEffectRecord aura)
            => "aura."+RetreatHash(string.Join("|",s.ContentFingerprint,actor,detection.Id,aura.Id)).Substring(0,32);
        private static SpellEffectRecord ActiveDetection(Snapshot s,string actor)=>s.SpellEffects.SingleOrDefault(x=>x.Present
            && x.SpellId=="detect-magic" && x.CasterId==actor && x.ExpiresAt>s.RuleClock);
        internal static ExpeditionCastingView ObserveCasting(Snapshot s,string actor)
        {
            var detection=ActiveDetection(s,actor);
            var auras=detection==null?Array.Empty<ExpeditionMagicAuraView>():s.SpellEffects.Where(x=>AuraPerceived(s,actor,x))
                .Select(x=>{
                    string id=AuraObservationId(s,actor,detection,x);var position=s.Actors.Single(a=>a.Id==x.TargetId);
                    var focus=s.DetectMagicFocuses.LastOrDefault(f=>f.ActorId==actor&&f.ObservationId==id);
                    return new ExpeditionMagicAuraView(id,position.X,position.Y,focus!=null,
                        focus==null?"":focus.SchoolWithheld?"Unavailable":focus.BroadSchool);
                }).OrderBy(x=>x.ObservationId,StringComparer.Ordinal).ToArray();
            return new ExpeditionCastingView(s,actor,auras);
        }
        private static bool AuraPerceived(Snapshot s,string actor,SpellEffectRecord effect)
        {
            if(!effect.Present || effect.ExpiresAt<=s.RuleClock || !SpellCastingProfile.IsAdmittedSpell(effect.SpellId)
                || !s.SpellCasts.Any(x=>x.CommandId==effect.CastId&&x.EffectId==effect.Id))return false;
            var source=s.Actors.SingleOrDefault(x=>x.Id==effect.TargetId); var observer=s.Actors.Single(x=>x.Id==actor);
            if(source==null || s.WorldTraversals.Any(x=>x.ActorId==source.Id || x.ActorId==actor)
                || PlanarCombatGeometry.DistanceFeet(new CombatCell(observer.X,observer.Y),new CombatCell(source.X,source.Y))>30
                || !ObservationGeometry.LineOfEffectClear(s,actor,source.Id))return false;
            return SpellCastingProfile.AuraOutlinePermitted(true,source.Id==actor || ObservationRules.CanSee(s,actor,source.Id),true,true,false);
        }
        private string AssessCastingUtility(Snapshot s,Command c)
        {
            string shape=SpellCastingProfile.PayloadFailure(s,c);if(shape!=null)return shape;
            if(!s.ConnectedClericCasting || c.Actor!=ClericRpProfile.Actor)return "OrdinarySpellcastingUnsupported";
            if(c.Kind==CommandKind.EndSpellConcentration) {
                if(PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s))return "TacticalChoicePending";
                return s.SpellEffects.Any(x=>x.Id==c.Target&&x.CasterId==c.Actor&&x.Present&&x.RequiresConcentration)
                    ?null:"ConcentrationUnavailable";
            }
            if(c.Kind==CommandKind.RespondSanctuary)return "SanctuaryAdmissionUnavailable";
            string action=CastingActionFailure(s,c); if(action!=null)return action;
            if(c.Kind==CommandKind.GroundCastingStrain)return c.Target==""?null:"UnexpectedGroundingTarget";
            if(c.Kind!=CommandKind.FocusDetectedAura)return "OrdinarySpellUtilityUnsupported";
            var detection=ActiveDetection(s,c.Actor);
            if(detection==null)return "DetectMagicNotActive";
            if(!s.SpellEffects.Any(x=>AuraPerceived(s,c.Actor,x)&&AuraObservationId(s,c.Actor,detection,x)==c.Target))
                return "AuraObservationUnavailable";
            return s.DetectMagicFocuses.Length>=SpellCastingProfile.MaxFocuses?"CastingHistoryFull":null;
        }
        private string ResolveCastingUtility(Snapshot s,Command c,bool schoolWithheldForDetachedControl=false)
        {
            string failure=AssessCastingUtility(s,c);if(failure!=null)return failure;
            if(c.Kind==CommandKind.EndSpellConcentration) {
                EndSpellEffect(s,s.SpellEffects.Single(x=>x.Id==c.Target),c.Id,s.Revision+1,s.RuleClock,SpellEffectEndReason.Voluntary);
                return null;
            }
            SetInterval(s,Interval(s,c.Actor).PayAction());
            if(c.Kind==CommandKind.GroundCastingStrain) {
                RecordCastingActivity(s,c,CastingActivityKind.Grounding);return null;
            }
            var detection=ActiveDetection(s,c.Actor);
            var aura=s.SpellEffects.Single(x=>AuraPerceived(s,c.Actor,x)&&AuraObservationId(s,c.Actor,detection,x)==c.Target);
            // This source cohort has no admitted school-protection producer. An unknown item/property
            // never becomes an aura merely by passing a name to this command.
            string school=SpellCastingProfile.FocusedAuraSchool(SpellSourceCatalog.Get(aura.SpellId).AccessFor("Cleric").School,
                schoolWithheldForDetachedControl);
            s.DetectMagicFocuses=s.DetectMagicFocuses.Append(new DetectMagicFocusRecord(c.Id,s.Revision+1,c.Actor,detection.Id,aura.Id,
                c.Target,CurrentCastingTurn(s,c.Actor),s.RuleClock,schoolWithheldForDetachedControl,school)).ToArray();
            RecordCastingActivity(s,c,CastingActivityKind.DetectFocus);return null;
        }
        private CommandQueryResult QueryCastingUtility(Snapshot s,Command c)
        {
            string failure=AssessCastingUtility(s,c);
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,
                failure==null && c.Kind!=CommandKind.EndSpellConcentration?new[]{new CommandCost("action","",1)}:null);
        }

        private static RuleTime? NextCastingBoundary(Snapshot s)
        {
            if(!s.ConnectedClericCasting)return null;
            RuleTime? due=s.SpellEffects.Where(x=>x.Present).Select(x=>(RuleTime?)x.ExpiresAt).OrderBy(x=>x).FirstOrDefault();
            var epoch=WorldTiming.ForActor(s,ClericRpProfile.Actor);
            if(epoch==null || !PostRecoveryProfile.IsEpoch(s,epoch.Id) && epoch.Id!=s.Reinforcement?.Admission?.Phase.Epoch.Id)return due;
            long local=epoch.LatestStart(ClericRpProfile.Actor,epoch.SlotAt(s.RuleClock));
            if(local<0)return due;
            var end=epoch.Start(local+1);
            if(end<=s.RuleClock){local+=epoch.Order.Count;end=epoch.Start(local+1);}
            if(s.CastingStrain[0].Dissonance>0 || s.CastingActivities.Any(x=>x.Turn.EpochId==epoch.Id&&x.Turn.LocalStart==local))
                if(!due.HasValue || end<due.Value)due=end;
            return due;
        }

        // Runs before other endpoint events. No per-turn loop is needed once an idle cadence reaches zero.
        private static void SettleCastingTime(Snapshot s,RuleTime from,RuleTime to,Command cause)
        {
            if(!s.ConnectedClericCasting)return;
            foreach(var effect in s.SpellEffects.Where(x=>x.Present&&x.ExpiresAt<=to).OrderBy(x=>x.ExpiresAt).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray()) {
                if(cause==null)throw new ArgumentException("Casting deadline requires the actual advancing command.");
                EndSpellEffect(s,effect,cause.Id,s.Revision+1,effect.ExpiresAt,SpellEffectEndReason.Expired);
            }
            var epoch=WorldTiming.ForActor(s,ClericRpProfile.Actor); var phase=s.Reinforcement?.Admission?.Phase;
            if(epoch==null || !PostRecoveryProfile.IsEpoch(s,epoch.Id) && epoch.Id!=phase?.Epoch.Id || from<epoch.Origin)return;
            long local=epoch.LatestStart(ClericRpProfile.Actor,epoch.SlotAt(from));
            if(local<0)local=Enumerable.Range(0,epoch.Order.Count).Single(x=>epoch.Order[x]==ClericRpProfile.Actor);
            if(epoch.Start(local+1)<=from)local+=epoch.Order.Count;
            while(epoch.Start(local+1)<=to) {
                var current=s.CastingStrain[0]; var turn=new SpellTurnIdentity(ClericRpProfile.Actor,epoch.Id,local,WorldTiming.TurnOrdinal(s,epoch.Id,local));
                var activities=s.CastingActivities.Where(x=>x.Turn.SameAs(turn)).ToArray();
                if(current.Dissonance==0 && activities.Length==0)break;
                if(cause==null || s.CastingTurnEnds.Length>=SpellCastingProfile.MaxTurnEnds)throw new ArgumentException("Casting End history capacity or command unavailable.");
                bool magic=activities.Any(x=>x.IsMagical),ground=activities.Any(x=>x.Kind==CastingActivityKind.Grounding);
                int pb=CharacterRuleFacts.ForActor(s,ClericRpProfile.Actor).ProficiencyBonus;
                var reduced=current.ReduceAtSettledEnd(magic?0:ground?pb:1);
                s.CastingStrain=new[]{reduced};
                s.CastingTurnEnds=s.CastingTurnEnds.Append(new CastingTurnEndRecord(turn,cause.Id,s.Revision+1,epoch.Start(local+1),
                    current.Dissonance,reduced.Dissonance,magic,ground,pb)).ToArray();
                local=checked(local+epoch.Order.Count);
            }
        }
    }
}
#endif
