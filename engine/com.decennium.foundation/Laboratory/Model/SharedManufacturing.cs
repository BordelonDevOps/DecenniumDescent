#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One exact reviewed Alchemy card, two finite component sets, authored camp apparatus,
    /// and only the supplementary packaging required by that profile. Recipe-14 divisibility is an
    /// explicit occurrence-scoped prototype completion, not a material-category default.</summary>
    public sealed class SharedManufacturingFixture
    {
        public const string Packaging="manufacture.glass-vials";
        private readonly string[] recipeIds;
        public IReadOnlyList<string> RecipeIds { get; }
        public string RecipeId => recipeIds.Length==1?recipeIds[0]:null;
        public string PackagingLot { get { if(RecipeId==null)throw new InvalidOperationException("A multi-recipe fixture has no single packaging lot.");return PackagingFor(RecipeId); } }
        public int PackagingQuantity { get { if(RecipeId==null)throw new InvalidOperationException("A multi-recipe fixture has no single packaging quantity.");return PackagingQuantityFor(RecipeId); } }
        public int InitialLevel { get; } public int InitialXp { get; } public bool StationReady { get; }
        public bool ToolTrained { get; } public RuleTime BloodInterval { get; }
        public bool RecordedFailureObservation { get; } public bool CompatibleIngestion { get; }
        public SharedManufacturingFixture(int level=5,int xp=0,bool stationReady=true,bool toolTrained=true,long bloodIntervalSeconds=14400,bool recordedFailureObservation=false,bool compatibleIngestion=true,string recipeId=ManufacturingRules.Recipe4Id,IEnumerable<string> recipeIds=null)
        {
            var selected=(recipeIds??new[]{recipeId}).ToArray();
            if(recipeIds!=null&&recipeId!=ManufacturingRules.Recipe4Id||selected.Length<1||selected.Length>2
                ||level<1||level>9||xp<0||xp>=10+level||bloodIntervalSeconds<3600||bloodIntervalSeconds>14400
                ||selected.Any(x=>ManufacturingRules.Recipe(x)==null)||selected.Distinct(StringComparer.Ordinal).Count()!=selected.Length)
                throw new ArgumentException("Invalid supplied pre-specialty manufacturing facts.");
            this.recipeIds=selected.OrderBy(x=>x==ManufacturingRules.Recipe4Id?0:1).ToArray();RecipeIds=Array.AsReadOnly(this.recipeIds);
            InitialLevel=level;InitialXp=xp;StationReady=stationReady;ToolTrained=toolTrained;BloodInterval=new RuleTime(bloodIntervalSeconds);RecordedFailureObservation=recordedFailureObservation;CompatibleIngestion=compatibleIngestion;
        }
        public bool SupportsRecipe(string recipeId)=>recipeIds.Contains(recipeId,StringComparer.Ordinal);
        internal string Key
        {
            get {
                string facts=InitialLevel+"|"+InitialXp+"|"+StationReady+"|"+ToolTrained+"|"+BloodInterval+"|"+RecordedFailureObservation+"|"+CompatibleIngestion;
                if(RecipeId==ManufacturingRules.Recipe4Id)return "recipe4-manufacture-v1|public-reviewed-Alchemy|fortified-camp-bench-heat-glassware-sealed-apparatus|2-component-sets|4-glass-vials|divisible-fluids-0.01|blood-origin0|phase900-13500|"+facts;
                if(RecipeId==ManufacturingRules.Recipe14Id)return "recipe14-manufacture-v2|source-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|recipe-14-exact-occurrences|salts-and-spirits-measurable-bulk-0.01|2-component-sets|6-glass-vials|blood-origin0|phase900-13500|"+facts;
                return "manufacture-multi-v1|source-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|"+string.Join(",",recipeIds)+"|recipe-scoped-lots-and-vials|"+facts;
            }
        }
        public static string Lot(int set,int component)=>"manufacture.set"+set.ToString(CultureInfo.InvariantCulture)+".component"+component.ToString(CultureInfo.InvariantCulture);
        public static string Lot(string recipe,int set,int component)
            =>recipe==ManufacturingRules.Recipe4Id?Lot(set,component):recipe==ManufacturingRules.Recipe14Id
                ?"manufacture.recipe14.set"+set.ToString(CultureInfo.InvariantCulture)+".component"+component.ToString(CultureInfo.InvariantCulture)
                :throw new ArgumentException("Unknown manufacturing recipe.",nameof(recipe));
        public static string PackagingFor(string recipe)=>recipe==ManufacturingRules.Recipe4Id?Packaging:recipe==ManufacturingRules.Recipe14Id?"manufacture.recipe14.glass-vials":throw new ArgumentException("Unknown manufacturing recipe.",nameof(recipe));
        public static int PackagingQuantityFor(string recipe)=>recipe==ManufacturingRules.Recipe4Id?4:recipe==ManufacturingRules.Recipe14Id?6:throw new ArgumentException("Unknown manufacturing recipe.",nameof(recipe));
    }
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private readonly SharedManufacturingFixture manufacturing;
        private static string ManufacturingFingerprint(string prior,SharedManufacturingFixture facts)
        {using(var sha=SHA256.Create())return "TEST_ONLY.manufacture-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+facts.Key)).Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));}
        private void InitializeManufacturing(Snapshot s)
        {
            if(manufacturing==null)return;
            var lots=s.Work.Lots.ToList();var inventoryLots=s.InventoryLots.ToList();
            foreach(string recipeId in manufacturing.RecipeIds){
                var recipe=ManufacturingRules.Recipe(recipeId);
                for(int set=0;set<2;set++)for(int component=0;component<recipe.Components.Count;component++){
                    var definition=recipe.Components[component];string id=SharedManufacturingFixture.Lot(recipe.Id,set,component);int amount=definition.Quantity;
                    lots.Add(new ResourceLot(id,definition.Id,amount,TestOnlyCropPolicy.PlotId,TestOnlyPolicy.CompanionId));
                    inventoryLots.Add(new InventoryLotRecord(id,"",TestOnlyPolicy.CompanionId,new RuleQuantity(amount),default,NutritionKind.None,null,InventoryAccess.Ground));
                }
                string packaging=SharedManufacturingFixture.PackagingFor(recipeId);int packagingQuantity=SharedManufacturingFixture.PackagingQuantityFor(recipeId);
                lots.Add(new ResourceLot(packaging,"ordinary.glass-vial-1gp",packagingQuantity,TestOnlyCropPolicy.PlotId,TestOnlyPolicy.CompanionId));
                inventoryLots.Add(new InventoryLotRecord(packaging,"",TestOnlyPolicy.CompanionId,new RuleQuantity(packagingQuantity),default,NutritionKind.None,null,InventoryAccess.Ground));
            }
            s.Work=new WorkLedger(lots,s.Work.WorkerIntervals,s.Work.Reservations);s.InventoryLots=inventoryLots.ToArray();
            s.Trades=new[]{new TradeProgressRecord(TestOnlyPolicy.CompanionId,SharedCraftingFixture.TradeId,manufacturing.InitialLevel,manufacturing.InitialXp)};
        }
        private string ValidateManufacturingProfile(Snapshot s)
        {
            if(manufacturing==null)return s.ManufacturingOrders.Length==0&&s.Trades.Length==0&&s.AlchemyDoses.Length==0?null:"ManufacturingFixtureNotSelected";
            var recipes=manufacturing.RecipeIds.Select(ManufacturingRules.Recipe).ToArray();
            if(recipes.Length==0||recipes.Any(x=>x==null)||s.Trades.Length!=1||s.Trades[0].WorkerId!=TestOnlyPolicy.CompanionId||s.Trades[0].TradeId!=SharedCraftingFixture.TradeId
                ||s.ManufacturingOrders.Any(x=>!manufacturing.SupportsRecipe(x.RecipeId)||x.MaterialSet<0||x.MaterialSet>1
                    ||x.ExtraVials<ManufacturingRules.Recipe(x.RecipeId).MinimumSupplementaryVials||x.ExtraVials>ManufacturingRules.Recipe(x.RecipeId).MaximumSupplementaryVials)
                ||s.AlchemyDoses.Any(x=>!manufacturing.SupportsRecipe(x.RecipeId)))return "ManufacturingFixtureMismatch";
            foreach(var order in s.ManufacturingOrders){
                var recipe=ManufacturingRules.Recipe(order.RecipeId);
                for(int i=0;i<recipe.Components.Count;i++){
                    var reservation=s.Work.Reservations.Where(x=>x.JobId==order.Id&&x.Id==ComponentClaim(order,i)).ToArray();
                    if(reservation.Length!=1||reservation[0].LotId!=SharedManufacturingFixture.Lot(recipe.Id,order.MaterialSet,i)
                        ||reservation[0].Amount!=new RuleQuantity(recipe.Components[i].Quantity))return "ManufacturingFixtureMismatch";
                }
                var package=s.Work.Reservations.Where(x=>x.JobId==order.Id&&x.Id==order.Id+".packaging").ToArray();
                if(order.ExtraVials==0?package.Length!=0:package.Length!=1||package[0].LotId!=SharedManufacturingFixture.PackagingFor(recipe.Id)
                    ||package[0].Amount!=new RuleQuantity(order.ExtraVials))return "ManufacturingFixtureMismatch";
            }
            foreach(var recipe in recipes){
                foreach(var component in recipe.Components.Select((value,index)=>(value,index)))
                    for(int set=0;set<2;set++){
                        string id=SharedManufacturingFixture.Lot(recipe.Id,set,component.index);
                        if(!s.Work.Lots.Any(x=>x.Id==id&&x.UnitId==component.value.Id)
                            ||!s.InventoryLots.Any(x=>x.LotId==id&&x.OwnerId==TestOnlyPolicy.CompanionId))return "ManufacturingFixtureMismatch";
                    }
                string packagingId=SharedManufacturingFixture.PackagingFor(recipe.Id);
                if(!s.Work.Lots.Any(x=>x.Id==packagingId&&x.UnitId=="ordinary.glass-vial-1gp")
                    ||!s.InventoryLots.Any(x=>x.LotId==packagingId&&x.OwnerId==TestOnlyPolicy.CompanionId))return "ManufacturingFixtureMismatch";
                }
            return null;
        }
        private static bool ManufacturingCommand(CommandKind k)=>k==CommandKind.StartManufacturing||k==CommandKind.PauseManufacturing||k==CommandKind.ResumeManufacturing||k==CommandKind.CancelManufacturing||k==CommandKind.ResolveManufacturingQuality||k==CommandKind.UseAlchemyDose;
        private static bool ManufacturingChoicePending(Snapshot s)=>s.ManufacturingOrders.Any(x=>x.Status==ManufacturingStatus.AwaitingChoice);
        private static bool ActiveManufacturing(Snapshot s)=>s.ManufacturingOrders.Any(x=>x.Status==ManufacturingStatus.Working);
        private IEnumerable<Command> DiscoverManufacturingCommands(Snapshot s,string actor)
        {
            if(manufacturing==null||PendingCalendarChoice(s))yield break;
            int actorIndex=Array.FindIndex(s.Actors,x=>x.Id==actor);
            if(actorIndex<0)yield break;
            int controlIndex=0,qualityIndex=0;
            foreach(var order in s.ManufacturingOrders.Where(x=>x.WorkerId==actor&&x.Open)
                .OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                if(order.Status==ManufacturingStatus.Working) {
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+"."+actorIndex.ToString(CultureInfo.InvariantCulture)
                        +".manufacturing-control."+(controlIndex++).ToString(CultureInfo.InvariantCulture),actor,s.Revision,CommandKind.PauseManufacturing,order.Id);
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+"."+actorIndex.ToString(CultureInfo.InvariantCulture)
                        +".manufacturing-control."+(controlIndex++).ToString(CultureInfo.InvariantCulture),actor,s.Revision,CommandKind.CancelManufacturing,order.Id);
                    continue;
                }
                if(order.Status==ManufacturingStatus.Paused||order.Status==ManufacturingStatus.AwaitingCheck) {
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+"."+actorIndex.ToString(CultureInfo.InvariantCulture)
                        +".manufacturing-control."+(controlIndex++).ToString(CultureInfo.InvariantCulture),actor,s.Revision,CommandKind.ResumeManufacturing,order.Id);
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+"."+actorIndex.ToString(CultureInfo.InvariantCulture)
                        +".manufacturing-control."+(controlIndex++).ToString(CultureInfo.InvariantCulture),actor,s.Revision,CommandKind.CancelManufacturing,order.Id);
                    continue;
                }
                if(order.Status!=ManufacturingStatus.AwaitingChoice)continue;
                var profile=ManufacturingRules.Recipe(order.RecipeId);
                var catalysts=order.Quality==CraftQuality.Masterwork?profile.CatalystIndexes.ToArray():new[]{-1};
                foreach(var choice in new[]{CraftQualityChoice.Durability,CraftQualityChoice.FullYield})
                    foreach(int catalyst in catalysts)
                        yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+"."+actorIndex.ToString(CultureInfo.InvariantCulture)
                                +".manufacturing-quality."+(qualityIndex++).ToString(CultureInfo.InvariantCulture),actor,s.Revision,
                            CommandKind.ResolveManufacturingQuality,order.Id,(int)choice,catalyst+1);
            }
        }
        private CommandQueryResult QueryManufacturingQualityChoice(Snapshot s,Command c)
        {
            string failure=AssessManufacturingQualityChoice(s,c,out _,out _,out _);
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,Array.Empty<CommandCost>());
        }
        private string AssessManufacturingQualityChoice(Snapshot s,Command c,out ManufacturingOrderRecord current,
            out CraftQualityChoice choice,out int catalyst)
        {
            current=null;choice=default(CraftQualityChoice);catalyst=-1;
            if(manufacturing==null)return "ManufacturingNotSelected";
            if(c.Inventory!=null||c.Combat!=null)return "InvalidManufacturingRequest";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            current=s.ManufacturingOrders.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
            if(current==null)return "UnknownManufacturingOrder";
            if(!current.Open)return "ManufacturingOrderClosed";
            if(current.Status!=ManufacturingStatus.AwaitingChoice||c.X<1||c.X>2)return "NoManufacturingQualityChoice";
            choice=(CraftQualityChoice)c.X;catalyst=c.Y-1;
            var profile=ManufacturingRules.Recipe(current.RecipeId);
            if(profile==null)return "ManufacturingRecipeUnavailable";
            if(current.Quality==CraftQuality.Masterwork?!profile.CatalystIndexes.Contains(catalyst):catalyst!=-1)return "InvalidRetainedCatalyst";
            if(choice==CraftQualityChoice.FullYield&&!profile.CanYield(current.Quality,current.ExtraVials,catalyst))
                return "ManufacturingFullYieldUnavailable";
            return null;
        }
        private CommandQueryResult QueryManufacturingControl(Snapshot s,Command c)
        {
            string failure=AssessManufacturingControl(s,c,out _);
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,Array.Empty<CommandCost>());
        }
        private string AssessManufacturingControl(Snapshot s,Command c,out ManufacturingOrderRecord current)
        {
            current=null;
            if(manufacturing==null)return "ManufacturingNotSelected";
            if(c.Inventory!=null||c.Combat!=null)return "InvalidManufacturingRequest";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            current=s.ManufacturingOrders.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
            if(current==null)return "UnknownManufacturingOrder";
            if(!current.Open)return "ManufacturingOrderClosed";
            if(c.X!=0||c.Y!=0)return "InvalidManufacturingRequest";
            if(current.Status==ManufacturingStatus.AwaitingChoice)return "ManufacturingChoicePending";
            if(c.Kind==CommandKind.PauseManufacturing)
                return current.Status==ManufacturingStatus.Working?null:"ManufacturingNotWorking";
            if(c.Kind==CommandKind.CancelManufacturing)return null;
            if(c.Kind!=CommandKind.ResumeManufacturing)return "InvalidManufacturingRequest";
            if(current.Status==ManufacturingStatus.Working)return "ManufacturingAlreadyWorking";
            string access=ManufacturingAccess(s,c.Actor,current.Status!=ManufacturingStatus.AwaitingCheck,
                current.Status==ManufacturingStatus.AwaitingCheck,current.RecipeId);
            if(access!=null)return access;
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(!current.StabilizedAt.HasValue&&BloodUnprotectedAge(s,current.RecipeId,current.MaterialSet)>=BloodSpoils)return "ManufacturingIngredientSpoiled";
            return null;
        }
        private IEnumerable<string> ManufacturingOwners(Snapshot s,Command c)
        {
            if(manufacturing==null||!ManufacturingCommand(c.Kind))return Array.Empty<string>();
            if(c.Kind==CommandKind.UseAlchemyDose)return s.AlchemyDoses.Where(x=>x.Id==c.Target).Select(x=>x.OwnerId).ToArray();
            return s.Structures.Where(x=>x.Id==SharedCraftingFixture.ToolId).Select(x=>x.OwnerId)
                .Concat(s.InventoryLots.Where(x=>x.LotId.StartsWith("manufacture.",StringComparison.Ordinal)).Select(x=>x.OwnerId)).Distinct(StringComparer.Ordinal).ToArray();
        }
        private static TradeProgressRecord ManufacturingTrade(Snapshot s,string actor)=>s.Trades.Single(x=>x.WorkerId==actor&&x.TradeId==SharedCraftingFixture.TradeId);
        private static void PutOrder(Snapshot s,ManufacturingOrderRecord j)=>s.ManufacturingOrders=s.ManufacturingOrders.Select(x=>x.Id==j.Id?j:x).ToArray();
        private static ManufacturingOrderRecord ChangeOrder(Snapshot s,ManufacturingOrderRecord j,ManufacturingStatus status,ActiveWorkProgress work=null,RuleTime? stabilized=null,
            int? first=null,int? second=null,int? natural=null,CraftQuality? quality=null,CraftQualityChoice? choice=null,int? catalyst=null,int? mishap=null,int? xp=null,string finding=null,string incident=null)
            =>new ManufacturingOrderRecord(j.Id,j.WorkerId,j.RecipeId,j.MaterialSet,j.ExtraVials,j.TakeTen,status,work??j.Work,j.StartedAt,s.RuleClock,stabilized??j.StabilizedAt,
                first??j.First,second??j.Second,natural??j.Natural,quality??j.Quality,choice??j.Choice,catalyst??j.RetainedCatalyst,mishap??j.Mishap,xp??j.XpAward,finding??j.FindingId,incident??j.MishapIncidentId);
        private RuleTime BloodSpoils=>new RuleTime(checked(manufacturing.BloodInterval.Numerator*2),manufacturing.BloodInterval.Denominator);
        public RuleTime BloodUnprotectedAge(Snapshot s,int materialSet)
        {
            if(manufacturing==null||manufacturing.RecipeId==null)throw new ArgumentException("A recipe identity is required for a multi-recipe blood lot.");
            return BloodUnprotectedAge(s,manufacturing.RecipeId,materialSet);
        }
        public RuleTime BloodUnprotectedAge(Snapshot s,string recipeId,int materialSet)
        {
            if(manufacturing==null||materialSet<0||materialSet>1||!manufacturing.SupportsRecipe(recipeId))throw new ArgumentException("Unknown supplied blood lot.");
            RuleTime suspended=default;
            foreach(var j in s.ManufacturingOrders.Where(x=>x.RecipeId==recipeId&&x.MaterialSet==materialSet&&x.StabilizedAt.HasValue)){
                RuleTime end=j.Open?s.RuleClock:j.UpdatedAt;
                suspended=CampGreens.Add(suspended,CampGreens.Subtract(end,j.StabilizedAt.Value));
            }
            return CampGreens.Subtract(s.RuleClock,suspended);
        }
        private string ManufacturingAccess(Snapshot s,string actor,bool window,bool checking=false,string recipeId=ManufacturingRules.Recipe4Id)
        {
            var recipe=ManufacturingRules.Recipe(recipeId);if(recipe==null||!manufacturing.SupportsRecipe(recipeId))return "ManufacturingRecipeUnavailable";
            if(actor!=TestOnlyPolicy.CompanionId)return "ManufacturingCredentialMissing";
            var trade=ManufacturingTrade(s,actor);
            if(trade.Level>=10)return "ManufacturingSpecialtyNotImplemented";
            if(!ManufacturingRules.Eligible(trade.Level,recipe.SkillLevel,manufacturing.ToolTrained,FormulaResearchRules.Knows(s,actor,recipeId),true))return "ManufacturingCredentialMissing";
            if(!manufacturing.StationReady||CraftingRestrictions.OrderWorkBlocked(s,TestOnlyCropPolicy.PlotId))return "ManufacturingStationUnavailable";
            if(s.Structures.Single(x=>x.Id==SharedCraftingFixture.ToolId).Broken||TargetInActiveRepair(s,SharedCraftingFixture.ToolId))return "ManufacturingToolUnavailable";
            if(checking&&CraftingRestrictions.CraftingCheckBlocked(s,SharedCraftingFixture.ToolId))return "ManufacturingCalibrationRequired";
            if(s.CraftingIncidents.Any(x=>x.Result==2&&x.Workers.Count!=0))return "ManufacturingToolInCalibration";
            if(!CapableWorker(s,actor)||View(s,actor).BlocksSight||AvailableHands(s,actor)<1)return "ManufacturingWorkerIncapable";
            var body=s.Actors.Single(x=>x.Id==actor);
            if(s.WorldTraversals.Any(x=>x.ActorId==actor)||Math.Max(Math.Abs(body.X-3),Math.Abs(body.Y-3))>1)return "ManufacturingStationOutOfReach";
            if(s.InventoryCombat&&s.WorldSchedule.Order.Contains(actor))return "ManufacturingParticipantInCombat";
            if(window&&!ResearchWindowEnd(s.RuleClock).HasValue)return "ManufacturingWindowClosed";
            return null;
        }
        private static void BookManufacturing(Snapshot s,ManufacturingOrderRecord j)
        {
            RuleTime end=CampGreens.Add(s.RuleClock,j.Work.Remaining),window=ResearchWindowEnd(s.RuleClock).Value;if(window<end)end=window;
            s.Work=s.Work.Reserve(j.Id,new[]{new WorkerInterval(j.Id+".labor."+(s.Revision+1).ToString(CultureInfo.InvariantCulture),j.Id,j.WorkerId,s.RuleClock,end)},Array.Empty<ResourceReservation>());
        }
        private static void PauseManufacturing(Snapshot s,ManufacturingOrderRecord j)
        {if(j.Status!=ManufacturingStatus.Working)return;s.Work=s.Work.CancelFutureWork(j.Id,s.RuleClock);PutOrder(s,ChangeOrder(s,j,ManufacturingStatus.Paused,j.Work.Interrupt(true)));}
        private void PauseIncompatibleManufacturing(Snapshot s)
        {
            if(manufacturing==null)return;
            foreach(var j in s.ManufacturingOrders.Where(x=>x.Status==ManufacturingStatus.Working).ToArray())
                if(ManufacturingAccess(s,j.WorkerId,false,recipeId:j.RecipeId)!=null||!j.StabilizedAt.HasValue&&BloodUnprotectedAge(s,j.RecipeId,j.MaterialSet)>=BloodSpoils)PauseManufacturing(s,j);
        }
        private RuleTime? NextManufacturingBoundary(Snapshot s)
        {
            if(manufacturing==null)return null;var values=new List<RuleTime>();
            foreach(var j in s.ManufacturingOrders.Where(x=>x.Status==ManufacturingStatus.Working)){
                values.Add(s.Work.WorkerIntervals.Single(x=>x.JobId==j.Id&&x.Start<=s.RuleClock&&x.End>s.RuleClock).End);
                values.Add(CampGreens.Add(s.RuleClock,CampGreens.Subtract(j.Work.Phases[j.Work.CompletedPhases],j.Work.Partial)));
                var age=BloodUnprotectedAge(s,j.RecipeId,j.MaterialSet);
                if(!j.StabilizedAt.HasValue&&age<BloodSpoils)values.Add(CampGreens.Add(s.RuleClock,CampGreens.Subtract(BloodSpoils,age)));
            }
            return values.Count==0?(RuleTime?)null:values.Min();
        }
        private void CreditManufacturing(Snapshot s,RuleTime elapsed,ICollection<string> ready)
        {
            if(manufacturing==null)return;
            foreach(var j in s.ManufacturingOrders.Where(x=>x.Status==ManufacturingStatus.Working).ToArray()){
                var work=j.Work.Credit(elapsed);RuleTime? stabilized=j.StabilizedAt;
                // Raw blood must still be usable at stabilization; a deadline is exclusive.
                bool spoiled=!stabilized.HasValue&&BloodUnprotectedAge(s,j.RecipeId,j.MaterialSet)>=BloodSpoils;
                if(spoiled)work=new ActiveWorkProgress(work.Phases,0,default,work.Labor);
                else if(!stabilized.HasValue&&work.CompletedPhases>0)stabilized=s.RuleClock;
                var status=ManufacturingStatus.Working;
                if(work.Complete){status=ManufacturingStatus.AwaitingCheck;ready.Add(j.Id);}
                else if(spoiled||!s.Work.WorkerIntervals.Any(x=>x.JobId==j.Id&&x.End>s.RuleClock)){
                    status=ManufacturingStatus.Paused;work=work.Interrupt(true);s.Work=s.Work.CancelFutureWork(j.Id,s.RuleClock);
                }
                PutOrder(s,ChangeOrder(s,j,status,work,stabilized));
            }
        }
        private static string ComponentClaim(ManufacturingOrderRecord j,int component)=>j.Id+".component"+component.ToString(CultureInfo.InvariantCulture);
        private static void SettleClaim(Snapshot s,string job,string id,RuleQuantity consumed)
        {
            if(consumed>default(RuleQuantity))s.Work=s.Work.ConsumeThrough(job,id,consumed);
            if(s.Work.Reservations.Single(x=>x.JobId==job&&x.Id==id).RemainingAmount>default(RuleQuantity))s.Work=s.Work.Release(job,id);
        }
        private static void SettleManufacturingInputs(Snapshot s,ManufacturingOrderRecord j,CraftQualityChoice choice,int catalyst)
        {
            var recipe=ManufacturingRules.Recipe(j.RecipeId);if(recipe==null)throw new InvalidOperationException("ManufacturingRecipeUnavailable");
            int count=ManufacturingRules.Yield(j.Quality,recipe.StandardYield,choice);
            int extra=Math.Max(0,count-recipe.SourceVesselCount);
            for(int i=0;i<recipe.Components.Count;i++){
                var component=recipe.Components[i];var amount=new RuleQuantity(component.Quantity);RuleQuantity returned=default;
                if(j.Quality==CraftQuality.Failed)returned=ManufacturingRules.FailureRecovery(amount,component.Consumed,component.Catalyst,component.Divisible);
                else if(j.Quality==CraftQuality.Masterwork&&i==catalyst)returned=new RuleQuantity(1);
                SettleClaim(s,j.Id,ComponentClaim(j,i),amount-returned);
            }
            if(j.ExtraVials>0)SettleClaim(s,j.Id,j.Id+".packaging",new RuleQuantity(extra));
        }
        private void SettleManufacturing(Snapshot s,ManufacturingOrderRecord j,CraftQualityChoice choice,int catalyst,int mishap=0,bool inputsSettled=false)
        {
            if(!inputsSettled)SettleManufacturingInputs(s,j,choice,catalyst);
            var recipe=ManufacturingRules.Recipe(j.RecipeId);if(recipe==null)throw new InvalidOperationException("ManufacturingRecipeUnavailable");
            int count=ManufacturingRules.Yield(j.Quality,recipe.StandardYield,choice);
            var trade=ManufacturingTrade(s,j.WorkerId);string findingKey=j.RecipeId+".level"+trade.Level.ToString(CultureInfo.InvariantCulture);
            // Optional authored process evidence: sediment position and timing were measured and
            // written during this completed work, supporting a concretely different separation method.
            bool recorded=manufacturing.RecordedFailureObservation&&j.Quality<CraftQuality.Standard&&mishap!=6;
            int xp=ManufacturingRules.TradeAward(j.Quality,trade.Level,recipe.SkillLevel,10,manufacturing.ToolTrained,trade.SuccessfulRecipes.Contains(j.RecipeId),trade.Findings.Contains(findingKey),true,recorded,mishap);
            var next=ManufacturingRules.AdvanceTrade(trade.Level,trade.Xp,xp);var successes=trade.SuccessfulRecipes.ToList();
            var findings=trade.Findings.ToList();if(xp==1)findings.Add(findingKey);
            if(j.Quality>=CraftQuality.Standard&&!successes.Contains(j.RecipeId))successes.Add(j.RecipeId);
            s.Trades=s.Trades.Select(x=>x==trade?new TradeProgressRecord(trade.WorkerId,trade.TradeId,next.Level,next.Xp,successes,findings):x).ToArray();
            if(s.AlchemyDoses.Length+count>ManufacturingValidation.MaxDoses)throw new InvalidOperationException("Dose history capacity reached.");
            for(int i=0;i<count;i++){
                string id=j.Id+".dose"+i.ToString(CultureInfo.InvariantCulture);int hp=choice==CraftQualityChoice.Durability&&j.Quality>=CraftQuality.Exceptional?2:1;
                s.AlchemyDoses=s.AlchemyDoses.Concat(new[]{new AlchemyDoseRecord(id,j.Id,j.RecipeId,j.WorkerId,j.WorkerId,j.WorkerId,TestOnlyCropPolicy.PlotId,s.RuleClock,hp,hp)}).ToArray();
            }
            PutOrder(s,ChangeOrder(s,j,ManufacturingStatus.Complete,choice:choice,catalyst:catalyst,mishap:mishap,xp:xp,finding:recorded?"observation.sediment-timing":""));
        }
        private void FinishManufacturingCheck(Snapshot s,ManufacturingOrderRecord j)
        {
            // The accepted check may need one later quality command. Never commit a frozen
            // decision at the last available receipt/revision with no representable settlement.
            if(s.Receipts.Length>=511||s.Revision>=long.MaxValue-1)throw new InvalidOperationException("Manufacturing settlement receipt capacity reached.");
            if(s.AlchemyDoses.Length>ManufacturingValidation.MaxDoses-7||s.CraftingIncidents.Length==CraftingConsequenceValidation.MaxIncidents
                ||!TestOnlyClubAttackPolicy.DamageConditionCapacity(s,j.WorkerId))throw new InvalidOperationException("Manufacturing result capacity reached.");
            var character=s.Characters.Single(x=>x.ActorId==j.WorkerId);
            int modifier=PlaytestCharacters.AbilityModifier(character.Abilities[3])+PlaytestCharacters.ProficiencyBonus(character.Levels.Count)
                +PlaytestLife.AbilityCheckInjuryPenalty(ActorLifeRules.Read(s.Lives.Single(x=>x.ActorId==j.WorkerId)),3,toolCheck:true);
            var roll=PlaytestDice.RollD20(s.RandomState,disadvantageSources:View(s,j.WorkerId).Has(ConditionKind.Poisoned)?1:0);s.RandomState=roll.NextRandomState;
            var recipe=ManufacturingRules.Recipe(j.RecipeId);if(recipe==null)throw new InvalidOperationException("ManufacturingRecipeUnavailable");
            var quality=ManufacturingRules.Quality(roll.Natural,modifier,recipe.Difficulty);
            j=ChangeOrder(s,j,ManufacturingStatus.AwaitingChoice,first:roll.First,second:roll.Second??0,natural:roll.Natural,quality:quality);PutOrder(s,j);
            if(quality>=CraftQuality.Exceptional)return;
            if(quality==CraftQuality.Mishap){
                // Source ordering: actual consumed inputs are lost before the d6 and its consequences.
                SettleManufacturingInputs(s,j,CraftQualityChoice.StandardQuantity,-1);
                var d6=DiceStream.Draw(s.RandomState,6);s.RandomState=d6.NextState;
                string id=j.Id+".mishap";int suffix=0;
                while(s.CraftingIncidents.Any(x=>x.Id==id)||crafting.Events.Any(x=>x.Id==id))id=j.Id+".mishap."+(++suffix).ToString(CultureInfo.InvariantCulture);
                string error=ApplyCraftingMishap(s,new CraftingMishapFact(id,d6.Value+1,j.WorkerId,s.RuleClock));
                if(error!=null)throw new InvalidOperationException(error);
                j=ChangeOrder(s,j,ManufacturingStatus.AwaitingChoice,incident:id);
                SettleManufacturing(s,j,CraftQualityChoice.StandardQuantity,-1,d6.Value+1,true);
            }else SettleManufacturing(s,j,CraftQualityChoice.StandardQuantity,-1);
        }
        private string ResolveManufacturing(Snapshot s,Command c)
        {
            if(manufacturing==null)return "ManufacturingNotSelected";
            if(c.Kind==CommandKind.UseAlchemyDose)return UseAlchemy(s,c);
            if(c.Inventory!=null||c.Combat!=null)return "InvalidManufacturingRequest";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Kind==CommandKind.StartManufacturing){
                var recipe=ManufacturingRules.Recipe(c.Target);
                if(recipe==null||!manufacturing.SupportsRecipe(c.Target)||c.X<0||c.X>1||c.Y<recipe.MinimumSupplementaryVials||c.Y>recipe.MaximumSupplementaryVials)return "InvalidManufacturingRequest";
                string access=ManufacturingAccess(s,c.Actor,true,recipeId:recipe.Id);if(access!=null)return access;
                if(CraftingRestrictions.NewOrderBlocked(s,c.Actor,TestOnlyCropPolicy.PlotId,SharedCraftingFixture.TradeId))return "ManufacturingLogRequired";
                if(s.ManufacturingOrders.Any(x=>x.Open))return "ManufacturingApparatusClaimed";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                if(BloodUnprotectedAge(s,recipe.Id,c.X)>=BloodSpoils)return "ManufacturingIngredientSpoiled";
                if(s.ManufacturingOrders.Length==ManufacturingValidation.MaxOrders)return "ManufacturingHistoryFull";
                for(int i=0;i<recipe.Components.Count;i++)if(s.Work.AvailableAmount(SharedManufacturingFixture.Lot(recipe.Id,c.X,i))<new RuleQuantity(recipe.Components[i].Quantity))return "ManufacturingIngredientsUnavailable";
                string packaging=SharedManufacturingFixture.PackagingFor(recipe.Id);
                if(s.Work.AvailableAmount(packaging)<new RuleQuantity(c.Y))return "ManufacturingPackagingUnavailable";
                string id="manufacture.order."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
                var j=new ManufacturingOrderRecord(id,c.Actor,c.Target,c.X,c.Y,false,ManufacturingStatus.Working,new ActiveWorkProgress(new[]{recipe.FirstPhase,recipe.RemainingPhase}),s.RuleClock,s.RuleClock);
                var claims=Enumerable.Range(0,recipe.Components.Count).Select(i=>new ResourceReservation(ComponentClaim(j,i),id,SharedManufacturingFixture.Lot(recipe.Id,c.X,i),recipe.Components[i].Quantity)).ToList();
                if(c.Y>0)claims.Add(new ResourceReservation(id+".packaging",id,packaging,c.Y));
                s.Work=s.Work.Reserve(id,Array.Empty<WorkerInterval>(),claims);BookManufacturing(s,j);s.ManufacturingOrders=s.ManufacturingOrders.Concat(new[]{j}).ToArray();return null;
            }
            if(c.Kind==CommandKind.ResolveManufacturingQuality){
                var current=s.ManufacturingOrders.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);if(current==null)return "UnknownManufacturingOrder";
                if(!current.Open)return "ManufacturingOrderClosed";
                string choiceFailure=AssessManufacturingQualityChoice(s,c,out current,out var choice,out int catalyst);
                if(choiceFailure!=null)return choiceFailure;
                SettleManufacturing(s,current,choice,catalyst);return ResumeManufacturingAdvance(s);
            }
            string controlFailure=AssessManufacturingControl(s,c,out var controlled);
            if(controlFailure!=null)return controlFailure;
            if(c.Kind==CommandKind.PauseManufacturing){PauseManufacturing(s,controlled);return null;}
            if(c.Kind==CommandKind.CancelManufacturing){
                var recipe=ManufacturingRules.Recipe(controlled.RecipeId);if(recipe==null)return "ManufacturingRecipeUnavailable";
                s.Work=s.Work.CancelFutureWork(controlled.Id,s.RuleClock);
                for(int i=0;i<recipe.Components.Count;i++)SettleClaim(s,controlled.Id,ComponentClaim(controlled,i),controlled.Work.Labor==default?default:new RuleQuantity(recipe.Components[i].Quantity));
                if(controlled.ExtraVials>0)SettleClaim(s,controlled.Id,controlled.Id+".packaging",default);
                PutOrder(s,ChangeOrder(s,controlled,ManufacturingStatus.Cancelled));return null;
            }
            if(c.Kind==CommandKind.ResumeManufacturing){
                if(controlled.Status==ManufacturingStatus.AwaitingCheck){FinishManufacturingCheck(s,controlled);
                    if(ManufacturingChoicePending(s))s.ManufacturingAdvance=new ManufacturingAdvanceRecord(s.RuleClock,false,c.Id,s.Revision+1,"");return null;}
                BookManufacturing(s,controlled);PutOrder(s,ChangeOrder(s,controlled,ManufacturingStatus.Working));return null;
            }
            return "InvalidManufacturingRequest";
        }
        private string ResumeManufacturingAdvance(Snapshot s)
        {
            var pending=s.ManufacturingAdvance;if(pending==null)return null;s.ManufacturingAdvance=null;
            if(pending.Target>s.RuleClock){string failure=AdvanceTo(s,pending.Target,pending.ExitAfterSlot,continuation:pending);if(failure!=null)return failure;}
            if(s.ManufacturingAdvance==null&&pending.ExitAfterSlot&&ResolvedConflict(s)&&!PendingCalendarChoice(s)){
                s.InventoryCombat=false;s.InventoryTurnActor="";s.InventoryInteractions=0;
            }
            return null;
        }
        private string UseAlchemy(Snapshot s,Command c)
        {
            if(c.Combat!=null||c.Inventory==null||c.Inventory.Amount!=new RuleQuantity(1)||c.Inventory.Handling!=HandlingKind.Pickup||c.X!=0||c.Y!=0)return "InvalidAlchemyUse";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(!s.InventoryCombat||s.Encounter.CurrentActor!=c.Actor)return "AlchemyOwnTacticalTurnRequired";
            if(Interval(s,c.Actor).ActionSpent)return "ActionAlreadySpent";
            if(!Permissions(s,c.Actor).Action||AvailableHands(s,c.Actor)<1)return "AlchemyUserIncapable";
            var dose=s.AlchemyDoses.SingleOrDefault(x=>x.Id==c.Target);if(dose==null||dose.Spent||dose.Hp==0)return "AlchemyDoseUnavailable";
            var user=s.Actors.Single(x=>x.Id==c.Actor);var recipient=s.Actors.SingleOrDefault(x=>x.Id==c.Inventory.Destination);
            if(s.WorldTraversals.Any(x=>x.ActorId==c.Actor||x.ActorId==c.Inventory.Destination)||dose.LocationId!=TestOnlyCropPolicy.PlotId
                ||Math.Max(Math.Abs(user.X-3),Math.Abs(user.Y-3))>1)return "AlchemyDoseOutOfReach";
            if(recipient==null||Math.Max(Math.Abs(user.X-recipient.X),Math.Abs(user.Y-recipient.Y))>1)return "AlchemyRecipientOutOfReach";
            var before=s.Lives.Single(x=>x.ActorId==recipient.Id);
            if(before.Dead||!manufacturing.CompatibleIngestion)return "AlchemyRecipientCannotIngest";
            if(recipient.Id!=c.Actor&&recipient.Id!=TestOnlyPolicy.ActorId&&recipient.Id!=TestOnlyPolicy.CompanionId
                &&!View(s,recipient.Id).Clauses.Incapacitated&&!ActorLifeRules.ZeroHpUnconscious(s,recipient.Id))return "AlchemyRecipientUnwilling";
            SetInterval(s,Interval(s,c.Actor).PayAction());
            var first=DiceStream.Draw(s.RandomState,4);var second=DiceStream.Draw(first.NextState,4);s.RandomState=second.NextState;
            long potential=View(s,recipient.Id).HealingPotential(first.Value+second.Value+4);
            var healed=PlaytestLife.Heal(ActorLifeRules.Read(before),potential);TestOnlyClubAttackPolicy.ApplyLife(s,before,healed);
            s.AlchemyDoses=s.AlchemyDoses.Select(x=>x.Id==dose.Id?new AlchemyDoseRecord(x.Id,x.OrderId,x.RecipeId,x.MakerId,x.OwnerId,x.CustodianId,x.LocationId,x.CreatedAt,x.MaximumHp,x.Hp,
                s.RuleClock,c.Actor,recipient.Id,first.Value+1,second.Value+1,potential,healed.Hp-before.Hp):x).ToArray();
            ReconcileDyingCadences(s);PauseIncompatibleWork(s);return null;
        }
    }
}
#endif
