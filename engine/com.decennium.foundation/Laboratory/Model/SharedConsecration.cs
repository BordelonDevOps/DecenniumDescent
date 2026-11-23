#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    internal static class ConsecrationRules
    {
        internal static bool Owns(Snapshot s, string actor, string feature) => s.Consecration != null
            && s.CharacterFeatureGrants.Any(x => x.ActorId == actor && x.FeatureId == feature && ClericRpProfile.ValidInitialGrant(s,x));
        internal static bool PerceivesCenter(Snapshot s, string actor, int x, int y)
        {
            if (!SharedDeclaredGeometry.SupportsAnchorAt(s,x,y) || !s.Actors.Any(a => a.Id == actor)) return false;
            var view = TestOnlyClubAttackPolicy.ConditionsFor(s,actor).View();
            return !view.Unaware && !view.BlocksSight && ObservationGeometry.GeometricSight(s,actor,
                ObservationGeometry.Position(s,actor),new ObservationPoint(new RuleQuantity(x),new RuleQuantity(y)));
        }
        internal static bool Contains(Snapshot s, ConsecrationZone zone, string actor)
        {
            if (!zone.Present(s.RuleClock) || !s.Actors.Any(x => x.Id == actor)) return false;
            var point = ObservationGeometry.Position(s,actor);
            var dx = point.X >= new RuleQuantity(zone.X) ? point.X - new RuleQuantity(zone.X) : new RuleQuantity(zone.X) - point.X;
            var dy = point.Y >= new RuleQuantity(zone.Y) ? point.Y - new RuleQuantity(zone.Y) : new RuleQuantity(zone.Y) - point.Y;
            return dx <= new RuleQuantity(3) && dy <= new RuleQuantity(3)
                && ObservationGeometry.LineOfEffectClearFromCell(s,zone.X,zone.Y,actor);
        }
        internal static int AttackModifier(Snapshot s, string actor)
        {
            if (s.Consecration == null) return 0;
            var creature = s.Creatures.SingleOrDefault(x => x.ActorId == actor);
            bool undead;
            if (creature != null) {
                if (!creature.ClassificationKnown) throw new InvalidOperationException("Consecration attacker classification is unknown.");
                undead = creature.Types.Contains("Undead");
            } else if (s.Consecration.HumanoidActors.Contains(actor)) undead = false;
            else throw new InvalidOperationException("Consecration attacker has no qualified type origin.");
            return undead && s.Consecration.Zones.Any(x => Contains(s,x,actor)) ? -1 : 0;
        }
        internal static void RecordAttack(Snapshot s, string attackId, string actor, int totalModifier)
        {
            if(s.Consecration==null)return;
            int contribution=AttackModifier(s,actor);
            var zone=contribution==0?null:s.Consecration.Zones.First(x => Contains(s,x,actor));
            var point=ObservationGeometry.Position(s,actor);
            var audit=new ConsecrationAttackContribution(attackId,s.Revision+1,s.RuleClock,actor,point.X,point.Y,
                actor==FerryWraithProfile.Actor,zone?.CommandId??"",totalModifier);
            s.Consecration=s.Consecration.WithAttacks(s.Consecration.Attacks.Append(audit));
        }
        internal static void HealAfterRite(Snapshot s, Command c, HealingRiteRecord rite)
        {
            if (rite == null) throw new ArgumentNullException(nameof(rite));
            if (rite.ActualGain <= 0 || !Owns(s,c.Actor,ConsecrationProfile.Ground)
                || !s.Consecration.HumanoidActors.Contains(c.Target)) return;
            var zone = s.Consecration.Zones.SingleOrDefault(x => x.OwnerId == c.Actor && Contains(s,x,c.Target));
            if (zone == null) return;
            var before = s.Lives.Single(x => x.ActorId == c.Target);
            ValidatePaidTrigger(s,c,rite);
            if (before.Dead || s.Consecration.Healing.Any(x => x.RiteCommandId == c.Id))
                throw new InvalidOperationException("Ground requires a single live positive Rite trigger.");
            if (before.Hp != rite.HpAfter) throw new InvalidOperationException("Ground lost its actual base Rite predecessor.");
            long potential = TestOnlyClubAttackPolicy.ConditionsFor(s,c.Target).View().HealingPotential(1);
            var healed = PlaytestLife.Heal(ActorLifeRules.ReadForResolution(s,before),potential);
            var point = ObservationGeometry.Position(s,c.Target);
            var record = new ConsecratedGroundHealing(c.Id,zone.CommandId,s.Revision+1,s.RuleClock,c.Actor,c.Target,
                point.X,point.Y,before.Hp,potential,healed.Hp);
            TestOnlyClubAttackPolicy.ApplyLife(s,before,healed);
            s.Consecration = s.Consecration.WithHealing(s.Consecration.Healing.Append(record));
        }
        private static void ValidatePaidTrigger(Snapshot s, Command c, HealingRiteRecord rite)
        {
            if (c.Kind != CommandKind.UseHealingRite || c.ExpectedRevision != s.Revision
                || !s.HealingRites.Contains(rite) || rite.CommandId != c.Id || rite.Revision != s.Revision+1
                || rite.ActorId != c.Actor || rite.TargetId != c.Target || rite.At != s.RuleClock
                || rite.SourceId != ClericRpProfile.HealingRite || rite.SourceRevision != ClericRpProfile.SourceRevision
                || rite.RpPaid != 2 || rite.ActualGain <= 0 || s.RandomState != rite.RandomAfter
                || s.ResonancePools.Single(x => x.ActorId == c.Actor).Current != rite.RpAfter
                || !s.WorldIntervals.Single(x => x.ActorId == c.Actor).ActionSpent
                || s.Lives.Single(x => x.ActorId == c.Target).Dead || s.Lives.Single(x => x.ActorId == c.Target).Hp != rite.HpAfter
                || !Owns(s,c.Actor,ClericRpProfile.HealingRite)
                || rite.Modifier != Math.Max(1,CharacterRuleFacts.ForActor(s,c.Actor).AbilityModifier(CharacterAbility.Wisdom)))
                throw new ArgumentException("Ground requires its actual staged paid Rite producer.");
            var draw = DiceStream.Draw(rite.RandomBefore,8);
            if (draw.Value+1 != rite.Die || draw.NextState != rite.RandomAfter || draw.WordsConsumed != rite.WordsConsumed)
                throw new ArgumentException("Ground Rite draw does not match its payment record.");
        }
        internal static bool PayloadValid(Command c) => c != null && c.GetConsecrateRequest() != null && c.Kind == CommandKind.UseConsecrate
            && c.Target == "" && c.X == 0 && c.Y == 0 && c.Inventory == null && c.Combat == null && c.Advancement == null
            && c.Ranged == null && c.OverwatchRider == OverwatchRider.None && c.SuppressionFire == null && c.DefensiveFormation == null
            && c.ExpeditionAssignment == null && c.HarvestSelection == null && c.MiningSelection == null && c.ProspectingExposure == null
            && c.RouteMappingWork == null && c.IntimidatingPresence == null && c.HealingRite == null && c.SpellCast == null
            && c.Guidance == null && c.SanctuaryResponse == null && c.DivineInvocation == null;
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private ConsecrationRecord consecrationDeclaration;
        internal TestOnlySharedWorldPolicy EnableConsecration()
        {
            if (initializationStarted || ferryDeclaration == null || consecrationDeclaration != null)
                throw new InvalidOperationException("Select Consecration once on a fresh Ferry expedition.");
            consecrationDeclaration = new ConsecrationRecord(ContentFingerprint,ConsecrationProfile.HumanoidActors);
            ContentFingerprint = ConsecrationProfile.BindFingerprint(ContentFingerprint);
            return this;
        }
        private string AssessConsecrate(Snapshot s, Command c)
        {
            if (s.Consecration == null) return "ConsecrationUnavailable";
            if (!ConsecrationRules.PayloadValid(c)) return "InvalidConsecrateRequest";
            if (!ConsecrationRules.Owns(s,c.Actor,ConsecrationProfile.Consecrate)) return "ConsecrateNotOwned";
            var character = s.Characters.Single(x => x.ActorId == c.Actor);
            int level = character.Levels.Count(x => x.ClassName == "Cleric");
            if (level < 1 || level > 3) return "ConsecrateClassUnsupported";
            if(s.OrdinaryMagic!=null) {
                string context=AssessMagicalActivityContext(s,c.Actor); if(context!=null)return context;
            } else {
                var epoch = WorldTiming.ForActor(s,c.Actor);
                var turn = CurrentCastingTurn(s,c.Actor);
                if (epoch == null || turn == null || turn.LocalStart < 0) return "ConsecrateCalendarUnavailable";
                long slot = epoch.SlotAt(s.RuleClock);
                if (slot != epoch.ProcessedSlot || epoch.LatestStart(c.Actor,slot) != slot
                    || s.RuleClock >= epoch.Start(checked(slot+1))
                    || Interval(s,c.Actor).LastStart != WorldTiming.TurnOrdinal(s,epoch.Id,slot)
                    || s.CastingTurnEnds.Any(x => x.Turn.SameAs(turn))) return "ConsecrateOpenOwnerSlotRequired";
                if (s.InventoryCombat && (s.Encounter?.CurrentActor != c.Actor || s.InventoryTurnActor != c.Actor)) return "WrongRegularTurn";
                if (!s.InventoryCombat && s.Encounter != null) return "ConsecrateContextUnsupported";
            }
            if (PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s) || s.ManufacturingAdvance != null)
                return "TacticalChoicePending";
            if (TestOnlyClubAttackPolicy.HasUnprocessedConditionDeadline(s)) return "ConditionBoundaryPending";
            if (!CapableWorker(s,c.Actor) || !Permissions(s,c.Actor).Action) return "ConditionPreventsAction";
            if (Interval(s,c.Actor).ActionSpent) return "ActionAlreadySpent";
            if (OrdinaryInventory.Busy(s,c.Actor) || CharacterAdvancementRules.Busy(s,c.Actor)
                || s.WorldTraversals.Any(x => x.ActorId == c.Actor)) return "ConsecrateRequiresStationaryAccess";
            if (s.AbilityRecharges.Any(x => x.ActorId == c.Actor && x.AbilityId == ConsecrationProfile.Consecrate && x.Remaining > 0))
                return "ConsecrateRecharging";
            int x = c.GetConsecrateRequest().X, y = c.GetConsecrateRequest().Y;
            var body = s.Actors.Single(a => a.Id == c.Actor);
            if (!ConsecrationRules.PerceivesCenter(s,c.Actor,x,y)
                || Math.Max(Math.Abs((long)body.X-x),Math.Abs((long)body.Y-y)) > 6
                || !ObservationGeometry.LineOfEffectClearToCell(s,c.Actor,x,y)) return "ConsecratePointUnavailable";
            var pool = s.ResonancePools.SingleOrDefault(p => p.ActorId == c.Actor);
            if (pool == null || pool.Maximum != DeriveResonanceMaximum(character)) return "ResonancePoolUnavailable";
            if (pool.Current < 2) return "InsufficientResonance";
            if (s.Consecration.Zones.Count >= ConsecrationRecord.MaxZones) return "ConsecrationHistoryFull";
            if (s.CastingActivities.Length >= SpellCastingProfile.MaxActivities) return "CastingHistoryFull";
            return null;
        }
        private string ResolveConsecrate(Snapshot s, Command c)
        {
            string failure = AssessConsecrate(s,c); if (failure != null) return failure;
            var origin=CurrentMagicalActionOrigin(s,c.Actor);
            var epoch = s.OrdinaryMagic==null ? WorldTiming.ForActor(s,c.Actor) : WorldTiming.FindEpoch(s,origin.EpochId);
            var pool = s.ResonancePools.Single(x => x.ActorId == c.Actor);
            long local = s.OrdinaryMagic==null ? epoch.LatestStart(c.Actor,epoch.ProcessedSlot) : origin.LocalStart;
            var deadline = s.InventoryCombat ? epoch.Start(checked(local+3L*epoch.Order.Count)) : s.RuleClock.AddSeconds(18);
            var zone = new ConsecrationZone(c.Id,s.Revision+1,c.Actor,c.GetConsecrateRequest().X,c.GetConsecrateRequest().Y,s.RuleClock,
                s.InventoryCombat,epoch.Id,local,deadline,pool.Current);
            var zones = s.Consecration.Zones.Select(x => x.End != ConsecrationEnd.Active ? x
                : x.ExpiresAt <= s.RuleClock ? x.Finish(ConsecrationEnd.Expiry,s.Revision+1,x.ExpiresAt)
                : x.Finish(ConsecrationEnd.Replacement,s.Revision+1,s.RuleClock)).Append(zone);
            SetInterval(s,Interval(s,c.Actor).PayAction());
            s.ResonancePools = s.ResonancePools.Select(x => x.ActorId == c.Actor ? x.Pay(2) : x).ToArray();
            s.Consecration = s.Consecration.WithZones(zones);
            RecordCastingActivity(s,c,CastingActivityKind.MagicalClassAbility);
            s.AbilityRecharges = s.AbilityRecharges.Where(x => x.ActorId != c.Actor || x.AbilityId != ConsecrationProfile.Consecrate)
                .Append(new CharacterAbilityRechargeRecord(c.Actor,ConsecrationProfile.Consecrate,epoch.Id,local,epoch.Start(local),3)).ToArray();
            return null;
        }
        private CommandQueryResult QueryConsecrate(Snapshot s, Command c)
        {
            string failure = AssessConsecrate(s,c);
            return new CommandQueryResult(true,failure == null,failure ?? "Available",s.Revision,failure == null
                ? new[] { new CommandCost("action","",1), new CommandCost("rp",c.Actor,2) } : null);
        }
        private IEnumerable<Command> DiscoverConsecrate(Snapshot s, string actor)
        {
            if (!ConsecrationRules.Owns(s,actor,ConsecrationProfile.Consecrate)) yield break;
            for (int y=0; y<DeclaredGeometryProfile.Height; y++)
                for (int x=0; x<DeclaredGeometryProfile.Width; x++)
                    if (ConsecrationRules.PerceivesCenter(s,actor,x,y))
                        yield return new Command("query.consecrate."+s.Revision+"."+x+"."+y,actor,s.Revision,CommandKind.UseConsecrate,
                            consecrate:new ConsecrateRequest(x,y));
        }
        private static RuleTime? NextConsecrationBoundary(Snapshot s)
            => s.Consecration?.Zones.Where(x => x.End == ConsecrationEnd.Active).Select(x => (RuleTime?)x.ExpiresAt).Min();
        private static void ExpireConsecration(Snapshot s)
        {
            if (s.Consecration == null || !s.Consecration.Zones.Any(x => x.End == ConsecrationEnd.Active && x.ExpiresAt <= s.RuleClock)) return;
            s.Consecration = s.Consecration.WithZones(s.Consecration.Zones.Select(x => x.End == ConsecrationEnd.Active && x.ExpiresAt <= s.RuleClock
                ? x.Finish(ConsecrationEnd.Expiry,s.Revision+1,x.ExpiresAt) : x));
        }
    }

    public sealed class ConsecrationZoneView
    {
        public string OwnerId { get; }
        public int X { get; }
        public int Y { get; }
        public int RadiusFeet => 15;
        public RuleTime ExpiresAt { get; }
        internal ConsecrationZoneView(ConsecrationZone zone, bool ownerVisible)
        { OwnerId=ownerVisible?zone.OwnerId:""; X=zone.X; Y=zone.Y; ExpiresAt=zone.ExpiresAt; }
    }
    public sealed class ConsecrationHealingView
    {
        public string CommandId { get; }
        public string TargetId { get; }
        public long BaseBefore { get; }
        public long BaseAfter { get; }
        public ConsecratedGroundHealing Ground { get; }
        public long RadianceBefore { get; }
        public long RadianceAfter { get; }
        public long AuraAfter { get; }
        internal ConsecrationHealingView(Snapshot s, HealingRiteRecord rite)
        {
            CommandId=rite.CommandId; TargetId=rite.TargetId; BaseBefore=rite.HpBefore; BaseAfter=rite.HpAfter;
            Ground=s.Consecration.Healing.SingleOrDefault(x=>x.RiteCommandId==rite.CommandId);
            var radiance=s.RadianceUses.SingleOrDefault(x=>x.RiteCommandId==rite.CommandId);
            RadianceBefore=radiance?.PreRadianceHp()??Ground?.HpAfter??rite.HpAfter;
            RadianceAfter=radiance?.HpAfter??RadianceBefore;
            AuraAfter=s.BishopEntry?.AuraHealing.SingleOrDefault(x=>x.RiteCommandId==rite.CommandId)?.HpAfter??RadianceAfter;
        }
    }
    public sealed partial class ConnectedExpeditionSession
    {
        public IReadOnlyList<ConsecrationHealingView> ObserveConsecrationHealing(ExpeditionSeat seat, string actor)
        {
            lock(gate) {
                var s=simulation.Capture(); var grant=SeatGrant(seat);
                if(s.Consecration==null || grant==null || !grant.Controls(actor))
                    return Array.AsReadOnly(Array.Empty<ConsecrationHealingView>());
                return Array.AsReadOnly(s.HealingRites.Where(x=>x.ActorId==actor && grant.Controls(x.TargetId))
                    .Select(x=>new ConsecrationHealingView(s,x)).ToArray());
            }
        }
        public IReadOnlyList<ConsecrationZoneView> ObserveConsecration(ExpeditionSeat seat, string actor)
        {
            lock(gate) {
                var s=simulation.Capture(); var grant=SeatGrant(seat);
                if (s.Consecration == null || grant == null || !grant.Controls(actor))
                    return Array.AsReadOnly(Array.Empty<ConsecrationZoneView>());
                return Array.AsReadOnly(s.Consecration.Zones.Where(x => x.Present(s.RuleClock)
                    && (x.OwnerId==actor || ConsecrationRules.PerceivesCenter(s,actor,x.X,x.Y)))
                    .Select(x => new ConsecrationZoneView(x,x.OwnerId==actor || ObservationRules.CanSee(s,actor,x.OwnerId))).ToArray());
            }
        }
    }
}
#endif
